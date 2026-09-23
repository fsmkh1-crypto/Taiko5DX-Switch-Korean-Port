"""Guarded caller-local redesign; no file writer or implicit scope expansion."""
import hashlib,json
from dataclasses import dataclass

def digest(data):return hashlib.sha256(data).hexdigest()
class Rejected(ValueError):pass
def require(ok,why):
    if not ok:raise Rejected(why)
@dataclass(frozen=True)
class Result:
    owner:str
    before:bytes
    after:bytes
    edits:tuple
    content_end:int
    def project(self,start,end):
        require(0<=start<end<=self.content_end,'INVALID_OR_PADDING_RANGE')
        require(all(end<=a or start>=z for a,z,_ in self.edits),'REFERENCE_INTERSECTS_REDESIGN')
        delta=sum(len(new)-(z-a) for a,z,new in self.edits if z<=start)
        return start+delta,end+delta
    def directive(self,authority,ranges=()):
        from builder.selective_event_contracts import Span
        from builder.selective_event_overlap import PayloadDirective,PreparedProjection
        projections=tuple(PreparedProjection(Span(a,z),Span(*self.project(a,z)),authority) for a,z in ranges)
        return PayloadDirective(self.owner,digest(self.before),self.after,authority,projections=projections)
class Redesign:
    def __init__(self,ledger_bytes,mapping_bytes,ledger_sha256,mapping_sha256):
        require(digest(ledger_bytes)==ledger_sha256,'LEDGER_IDENTITY')
        require(digest(mapping_bytes)==mapping_sha256,'MAPPING_IDENTITY')
        self.rows={};self.reverse={}
        for code,value in json.loads(mapping_bytes)['entries']:
            self.reverse.setdefault(chr(value),[]).append(code.to_bytes(2,'big'))
        for row in json.loads(ledger_bytes):self.rows.setdefault(row['owner'],[]).append(row)
    def encode(self,text):
        out=[]
        for c in text:
            if ord(c)<128:out.append(bytes([ord(c)]))
            else:
                codes=self.reverse.get(c,[])
                require(len(codes)==1,'MISSING_OR_AMBIGUOUS_GLYPH:'+c);out.append(codes[0])
        return b''.join(out)
    def apply(self,owner,source,pc,prepared):
        require(owner in self.rows,'OWNER_NOT_ADMITTED');rows=self.rows[owner]
        require(all(r['design_status']=='BOUNDARY_DESIGN_DECIDED' and not r['source_hold'] for r in rows),'SOURCE_OR_DESIGN_HOLD')
        require(type(source) is bytes and type(pc) is bytes and type(prepared) is bytes,'IMMUTABLE_BYTES_REQUIRED')
        for r in rows:
            b=r['binding'];require(digest(source)==b['source_sha256'],'SOURCE_PREIMAGE')
            require(digest(pc)==b['pc_sha256'],'PC_PREIMAGE')
        # This bounded adapter does not guess composition with earlier transforms.
        require(prepared==pc,'PREPARED_COMPOSITION_REQUIRED')
        require(source[:4]==pc[:4] and len(pc)%4==0,'HEADER_OR_ALIGNMENT')
        nul=pc.find(b'\0',4);require(nul>=4 and not any(pc[nul:]),'UNSUPPORTED_COMMAND_TAIL')
        edits=[]
        for r in rows:
            e=r['edit'];a,z=e['original_relative_span'];old=self.encode(e['old_display']);new=self.encode(e['new_display'])
            require(4<=a<z<=nul and pc[a:z]==old,'EDIT_PREIMAGE_OR_RANGE')
            require(b'\0' not in new,'INTERIOR_NUL');edits.append((a,z,new))
        edits.sort();require(all(edits[i][1]<=edits[i+1][0] for i in range(len(edits)-1)),'OVERLAPPING_EDITS')
        chunks=[];last=0
        for a,z,new in edits:chunks.extend((pc[last:a],new));last=z
        chunks.append(pc[last:nul+1]);after=b''.join(chunks);after+=b'\0'*((-len(after))%4)
        require(after[:4]==source[:4],'HEADER_CHANGED')
        return Result(owner,prepared,after,tuple(edits),nul+1)
