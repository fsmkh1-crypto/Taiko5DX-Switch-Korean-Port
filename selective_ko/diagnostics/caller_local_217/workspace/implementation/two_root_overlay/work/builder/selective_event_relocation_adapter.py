"""Explicitly provisioned field rule bridge; no opcode/family-based admission.

Arithmetic is inherited from pinned selective_event.py (blob
809932cf863459db1cc71f35d9f802d112f0234a). The registry grants NOTHING by default.
An exact field/source/target/unit scoped, reviewed applicability authority must be
supplied. Matching an encoding formula is not proof of executable applicability.
"""
from dataclasses import dataclass
from .selective_event_contracts import (
    FieldContract,FieldState,FieldProposal,Proof,ReviewedInteriorRecipe,
    Result,Status,Span,require,sha256,
)

@dataclass(frozen=True)
class ReviewedFieldRule:
    field: str
    codec: str
    source_word_sha256: str
    source_target: int
    partition: int
    unit: str|None
    intrusion: int
    authority: Proof

    def mask(self):
        if self.codec in ('EVENT04_BITS19','SWITCH09_BITS19'):return 0xfff80000
        if self.codec=='PC_EDITOR02':return 0x00ffff00
        if self.codec in ('PC_EDITOR04','PC_EDITOR08','PC_EDITOR09','SPECIAL04'):return 0xffff0000
        if self.codec in ('PC_EDITOR06','PC_EDITOR07'):return 0xffffff00
        require(False,'UNSUPPORTED_REVIEWED_FIELD_CODEC',self.codec)

    def encode(self,word:bytes,delta:int):
        require(type(word) is bytes and len(word)==4 and type(delta) is int and delta>=4 and delta%4==0,
                'REVIEWED_FIELD_SPAN_UNREPRESENTABLE',self.field)
        require(type(self.intrusion) is int and 0<=self.intrusion<=3,'INVALID_FIELD_INTRUSION',self.field)
        op={'EVENT04_BITS19':4,'SWITCH09_BITS19':9,'SPECIAL04':4,
            **{f'PC_EDITOR{x:02}':x for x in (2,4,6,7,8,9)}}.get(self.codec)
        require(op is not None and word[0]==op,'REVIEWED_FIELD_OPCODE_SCOPE',self.field)
        out=bytearray(word)
        if self.codec in ('EVENT04_BITS19','SWITCH09_BITS19'):
            require(self.intrusion==0 and delta<=32764,'REVIEWED_BITFIELD_RANGE',self.field)
            return ((int.from_bytes(word,'little')&0x0007ffff)|((delta//4)<<19)).to_bytes(4,'little')
        if op in (2,8):
            require(self.intrusion==0,'UNEXPECTED_FIELD_INTRUSION',self.field)
            value=delta//4;start=1 if op==2 else 2;width=2
        elif op==4:
            require(self.intrusion==0,'UNEXPECTED_FIELD_INTRUSION',self.field)
            value=delta*2;start=2;width=2
        elif op in (6,7):
            require((delta+self.intrusion)%2==0,'FIELD_INTRUSION_NOT_REPRESENTABLE',self.field)
            value=(delta+self.intrusion)//2;start=1;width=3
        else:value=delta*2+self.intrusion;start=2;width=2
        require(value < 1<<(8*width),'REVIEWED_FIELD_OVERFLOW',self.field)
        out[start:start+width]=value.to_bytes(width,'little');return bytes(out)

    def propose(self,c:FieldContract,anchors,interior:ReviewedInteriorRecipe|None=None):
        require(isinstance(self.authority,Proof) and self.field==c.field and self.source_word_sha256==sha256(c.source_header)
                and self.source_target==c.source_target and self.partition==c.partition and self.unit==c.unit,
                'REVIEWED_FIELD_AUTHORITY_SCOPE',c.field)
        allowed = c.state in (FieldState.CONTEXT,FieldState.UNKNOWN,FieldState.SPECIAL)
        allowed = allowed or (c.state == FieldState.BRANCH04 and self.codec == 'EVENT04_BITS19')
        require(allowed,'REVIEWED_RULE_CANNOT_OVERRIDE_PROTECTED_ROLE',c.field)
        if c.interior_recipe_ids:
            require(interior is not None,'H01_INTERIOR_ROLE_CONTRACT_NOT_DISCHARGED',c.field)
            interior.validate_field(c,self)
        else:
            require(interior is None,'UNEXPECTED_INTERIOR_CONTRACT_FOR_FIELD',c.field)
        require(anchors.field==c.field and anchors.source_field==c.source_span.start
                and anchors.source_target==c.source_target and anchors.source_partition==c.partition
                and anchors.final_field_partition==c.partition and anchors.final_target_partition==c.partition
                and anchors.final_field%4==0 and anchors.final_storage_end==anchors.final_field+4
                and anchors.unit==c.unit,'REVIEWED_FIELD_FINAL_ANCHORS',c.field)
        require(self.encode(c.source_header,c.source_target-c.source_span.start)==c.source_header,
                'REVIEWED_FIELD_SOURCE_DECODE_MISMATCH',c.field)
        return self.encode(c.source_header,anchors.final_target-anchors.final_field)

    def check(self,c:FieldContract,p:FieldProposal,interior:ReviewedInteriorRecipe|None=None):
        require(p.anchors is not None,'MISSING_FINAL_ANCHOR_PROOF',c.field)
        require(p.before==c.source_header and p.after==self.propose(c,p.anchors,interior),'REVIEWED_FIELD_EFFECT_MISMATCH',c.field)
        require(len({d.id for d in p.dependencies})==len(p.dependencies)
                and {d.id for d in p.dependencies}==set(c.dependency_ids),
                'REVIEWED_FIELD_DEPENDENCY_COMPLETENESS',c.field)
        for r in c.protected_ranges+p.additional_protections:
            lo=max(c.source_span.start,r.source_span.start);hi=min(c.source_span.end,r.source_span.end)
            if lo<hi:
                expected=r.expected[lo-r.source_span.start:hi-r.source_span.start]
                require(p.before[lo-c.source_span.start:hi-c.source_span.start]==expected
                        and p.after[lo-c.source_span.start:hi-c.source_span.start]==expected,
                        'BLOCK_CONFLICT_PROTECTED_VIEW',r.id)
        evidence=(c.proof,self.authority,p.anchors.proof)
        if interior is not None:evidence += (interior.proof,)
        return Result('FIELD:'+c.field,Status.SATISFIED,evidence=evidence,
            details={'codec':self.codec,'final_span':p.anchors.final_target-p.anchors.final_field,
                     'typed_applicability':'EXPLICITLY_PROVISIONED_NOT_INFERRED',
                     'required_view_ids':list(c.required_view_ids),'product_accepted':False})
