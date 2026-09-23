"""Second-stage caller-local transform, guarded by exact post142 identity."""
import json,re
from dataclasses import dataclass
from caller_local import Result,require,digest
@dataclass(frozen=True)
class Chained:
    first:object
    second:Result
    @property
    def after(self):return self.second.after
    def project(self,a,z):return self.second.project(*self.first.project(a,z))
class Residual:
    def __init__(self,data,expected_sha256,encode):
        require(digest(data)==expected_sha256,'RESIDUAL_LEDGER_IDENTITY');self.rows={};self.encode=encode
        for r in json.loads(data):
            require(r['disposition']=='BOUNDARY_DESIGN_DECIDED','UNDECIDED_RESIDUAL')
            self.rows.setdefault(r['owner'],[]).append(r)
    def apply(self,owner,first):
        require(owner in self.rows,'RESIDUAL_OWNER_NOT_ADMITTED')
        b=first.after;require(type(b) is bytes and len(b)%4==0,'RESIDUAL_ALIGNMENT')
        end=b.find(b'\0',4);require(end>=4 and not any(b[end:]),'RESIDUAL_TAIL')
        edits=[]
        for r in self.rows[owner]:
            e=r['edit'];require(e['baseline']=='POST142_COMPOSED_FINAL_COMMAND' and digest(b)==e['baseline_sha256'],'POST142_PREIMAGE')
            a,z=e['relative_span'];old=self.encode(e['old_display']);new=self.encode(e['new_display'])
            require(4<=a<z<=end and b[a:z]==old,'RESIDUAL_EDIT_PREIMAGE')
            require(b'\0' not in new,'RESIDUAL_INTERIOR_NUL');edits.append((a,z,new))
        edits.sort();require(all(edits[i][1]<=edits[i+1][0] for i in range(len(edits)-1)),'RESIDUAL_OVERLAP')
        parts=[];p=0
        for a,z,new in edits:parts.extend((b[p:a],new));p=z
        parts.append(b[p:end+1]);after=b''.join(parts);after+=b'\0'*((-len(after))%4)
        require(after[:4]==b[:4],'RESIDUAL_HEADER')
        # Newline comparison must use token-aware decoding at the caller; raw 0A may occur as a DBCS trail.
        dynamic=re.compile(rb'\\(?:%(?:00|01|02|03|04)(?:[0-9A-Fa-f]{3})?|#[0-9A-Fa-f]{4}|>[0-9A-Fa-f]{3}|D[0-9A-Fa-f]{3}|[0-9A-Fa-f]{4})')
        require(dynamic.findall(after[4:])==dynamic.findall(b[4:]),'DYNAMIC_REFERENCE_CHANGED')
        return Chained(first,Result(owner,b,after,tuple(edits),end+1))
