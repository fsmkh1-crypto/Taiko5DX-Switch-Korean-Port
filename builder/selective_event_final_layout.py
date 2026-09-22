"""IM03: deterministic TS5 shape, explicit interior maps and reconciled writers.

Only caller-supplied, reviewed payload/field proposals are assembled. This module
never infers a source owner, a PC recipe boundary or a relocation permission from
an opcode/NUL scan. Buffers stay in memory; game-file export and V371 acceptance
are separate, deliberately unavailable here.
"""
from __future__ import annotations

from bisect import bisect_right
from collections import defaultdict
from dataclasses import dataclass, field
from types import MappingProxyType
from typing import Iterable, Mapping
import struct

from .selective_event_contracts import ContractError, Proof, Span, require, sha256, valid_sha
from .selective_event_obligation_catalog import canonical_json


@dataclass(frozen=True)
class SourceIdentity:
    file: str
    size: int
    sha256: str
    authority: Proof

    def verify(self, file: str, data: bytes) -> None:
        require(type(data) is bytes and file == self.file and type(self.size) is int
                and self.size == len(data) and valid_sha(self.sha256)
                and sha256(data) == self.sha256 and isinstance(self.authority, Proof),
                'SOURCE_FILE_AUTHORITY_MISMATCH', file)


@dataclass(frozen=True)
class Geometry:
    prefix: bytes
    offsets: tuple[int, ...]

    @property
    def count(self) -> int:
        return len(self.offsets) - 1

    @property
    def table_end(self) -> int:
        return 8 + 4 * (self.count + 1)

    @classmethod
    def read(cls, data: bytes) -> Geometry:
        # Geometry inherited from pinned builder/selective_event.py: parse_event_ts5.
        # Grouping is intentionally not needed for table/partition serialization.
        require(type(data) is bytes and len(data) >= 12, 'TS5_HEADER_TRUNCATED', '')
        count = struct.unpack_from('<I', data, 4)[0]
        end = 8 + 4 * (count + 1)
        require(end <= len(data), 'TS5_OFFSET_TABLE_TRUNCATED', end)
        offsets = struct.unpack_from(f'<{count+1}I', data, 8)
        require(offsets[0] == end and offsets[-1] == len(data), 'TS5_TABLE_ENDPOINTS', offsets[:1])
        require(all(a < b for a, b in zip(offsets, offsets[1:])), 'TS5_OFFSET_ORDER', '')
        require(all(x % 4 == 0 for x in offsets), 'TS5_OFFSET_ALIGNMENT', '')
        return cls(data[:4], tuple(offsets))

    def contains(self, partition: int, span: Span) -> bool:
        return (type(partition) is int and 0 <= partition < self.count
                and self.offsets[partition] <= span.start < span.end <= self.offsets[partition+1])

    def locate(self, offset: int, *, boundary_partition: int | None = None) -> int:
        require(type(offset) is int and self.table_end <= offset <= self.offsets[-1],
                'PARTITION_ANCHOR_RANGE', offset)
        if boundary_partition is not None:
            p = boundary_partition
            require(type(p) is int and 0 <= p < self.count
                    and self.offsets[p] <= offset <= self.offsets[p+1],
                    'ANCHOR_PARTITION_MISMATCH', (p, offset))
            return p
        require(offset < self.offsets[-1], 'EOF_HAS_NO_CONTAINING_PARTITION', offset)
        return bisect_right(self.offsets, offset) - 1


@dataclass(frozen=True)
class MapPoint:
    """Reviewed absolute-source -> relative-materialized coordinate assertion.

    A hash/Proof identifies a supplied authority; it cannot establish arbitrary
    semantic mapping claims by itself. Identity regions need no invented point.
    """
    source: int
    relative: int
    authority: Proof


@dataclass(frozen=True)
class FieldSlot:
    field: str
    source_span: Span
    relative: int
    authority: Proof

    def __post_init__(self):
        require(bool(self.field) and self.source_span.size == 4
                and type(self.relative) is int and self.relative >= 0 and self.relative % 4 == 0
                and isinstance(self.authority, Proof), 'INVALID_INTERIOR_SLOT', self.field)


@dataclass(frozen=True)
class PayloadEdit:
    owner: str
    source_span: Span
    data: bytes
    partition: int
    writer: str
    unit: str | None
    source_sha256: str
    authority: Proof
    points: tuple[MapPoint, ...] = ()
    slots: tuple[FieldSlot, ...] = ()

    def __post_init__(self):
        object.__setattr__(self, 'points', tuple(self.points))
        object.__setattr__(self, 'slots', tuple(self.slots))
        require(bool(self.owner) and bool(self.writer) and type(self.data) is bytes
                and len(self.data) >= 4 and len(self.data) % 4 == 0
                and self.source_span.start % 4 == self.source_span.end % 4 == 0
                and self.source_span.size >= 4 and valid_sha(self.source_sha256)
                and isinstance(self.authority, Proof), 'INVALID_PAYLOAD_EDIT', self.owner)
        require(len({s.field for s in self.slots}) == len(self.slots), 'DUPLICATE_INTERIOR_SLOT', self.owner)


@dataclass(frozen=True)
class FieldWrite:
    field: str
    source_span: Span
    before: bytes
    after: bytes
    partition: int
    unit: str | None
    authority: Proof
    allowed_mask: int
    outcome: str

    def __post_init__(self):
        require(type(self.before) is bytes and type(self.after) is bytes
                and len(self.before) == len(self.after) == self.source_span.size == 4
                and type(self.allowed_mask) is int and 0 <= self.allowed_mask <= 0xffffffff
                and isinstance(self.authority, Proof) and bool(self.outcome),
                'INVALID_FIXED_WIDTH_FIELD', self.field)
        changed = int.from_bytes(self.before, 'little') ^ int.from_bytes(self.after, 'little')
        require(changed & ~self.allowed_mask == 0, 'FIELD_CHANGED_PROTECTED_BITS', self.field)


@dataclass(frozen=True)
class ResponsibilityRegion:
    """One exact cluster union, never the gap between a pair of clusters."""
    cluster: str
    unit: str
    source_span: Span
    partition: int
    authority: Proof

    def __post_init__(self):
        require(type(self.cluster) is str and bool(self.cluster) and type(self.unit) is str
                and bool(self.unit) and type(self.partition) is int and self.partition>=0
                and isinstance(self.source_span,Span) and isinstance(self.authority,Proof),
                'INVALID_RESPONSIBILITY_REGION',self.cluster)


@dataclass(frozen=True)
class JournalStep:
    id: str
    kind: str
    final_span: Span
    data: bytes
    source_span: Span | None
    writer: str
    unit: str | None
    authority: Proof
    supersedes: tuple[str, ...] = ()
    logical_mask: int | None = None
    changed_offsets: tuple[int, ...] = ()

    def to_dict(self) -> dict:
        return {'id':self.id, 'kind':self.kind,
                'final_span':[self.final_span.start,self.final_span.end],
                'source_span':None if self.source_span is None else [self.source_span.start,self.source_span.end],
                'data_sha256':sha256(self.data), 'writer':self.writer, 'unit':self.unit,
                'authority':{'document':self.authority.document,'sha256':self.authority.sha256,
                             'claim':self.authority.claim,'row':self.authority.row},
                'supersedes':list(self.supersedes),'logical_mask':self.logical_mask,
                'actual_changed_offsets':list(self.changed_offsets)}


@dataclass(frozen=True)
class FinalOwnership:
    final_span: Span
    step: str
    writer: str
    unit: str | None
    responsibility_proof: Proof


@dataclass(frozen=True)
class LayoutAudit:
    output_bytes: int
    assigned_bytes: int
    unassigned_bytes: int
    multiply_assigned_bytes: int
    conflicting_bytes: int
    errors: tuple[str, ...]
    table_offsets: tuple[int, ...] | None
    local_complete: bool
    product_accepted: bool = field(default=False, init=False)

    def __bool__(self):
        raise TypeError('Use local_complete. Layout correctness is not V371 acceptance.')

    def to_dict(self) -> dict:
        return {'output_bytes':self.output_bytes,'assigned_bytes':self.assigned_bytes,
                'unassigned_bytes':self.unassigned_bytes,'multiply_assigned_bytes':self.multiply_assigned_bytes,
                'conflicting_bytes':self.conflicting_bytes,'errors':list(self.errors),
                'table_offsets':None if self.table_offsets is None else list(self.table_offsets),
                'local_complete':self.local_complete,'product_accepted':False}


class FinalLayout:
    """One immutable source/shape coordinate system; values are written later."""
    def __setattr__(self, name, value):
        if getattr(self, '_sealed', False):
            raise AttributeError('FinalLayout is an immutable shape snapshot')
        object.__setattr__(self, name, value)

    def __init__(self, file: str, source: bytes, identity: SourceIdentity,
                 edits: Iterable[PayloadEdit] = (), regions: Iterable[ResponsibilityRegion] = ()):
        identity.verify(file, source)
        self.file = file; self.source = source; self.identity = identity
        self.geometry = Geometry.read(source)
        self.edits = tuple(sorted(edits, key=lambda e:(e.source_span.start,e.source_span.end,e.owner)))
        require(len({e.owner for e in self.edits}) == len(self.edits), 'DUPLICATE_PAYLOAD_OWNER', file)
        self.regions = tuple(sorted(regions, key=lambda r:(r.source_span.start,r.source_span.end,r.cluster)))
        require(len({r.cluster for r in self.regions}) == len(self.regions), 'DUPLICATE_CLUSTER_REGION', file)
        prior = self.geometry.table_end
        points = {}; slotmap = {}; placements = {}; delta = 0
        self._starts=[]; self._deltas=[]; identity_edits=set()
        for e in self.edits:
            require(self.geometry.contains(e.partition,e.source_span), 'PAYLOAD_CROSSES_PARTITION_OR_TABLE', e.owner)
            require(prior <= e.source_span.start, 'INDEPENDENT_PAYLOAD_OVERLAP', e.owner)
            require(sha256(source[e.source_span.start:e.source_span.end]) == e.source_sha256,
                    'PAYLOAD_SOURCE_HASH', e.owner)
            require(e.data[:4] == source[e.source_span.start:e.source_span.start+4],
                    'PAYLOAD_SOURCE_HEADER', e.owner)
            final_start=e.source_span.start+delta
            placements[e.owner]=Span(final_start,final_start+len(e.data))
            self._starts.append(e.source_span.start);self._deltas.append(delta)
            is_identity=e.data == source[e.source_span.start:e.source_span.end]
            if is_identity: identity_edits.add(e.owner)
            pp={e.source_span.start:0,e.source_span.start+4:4,e.source_span.end:len(e.data)}
            def point(s:int,r:int):
                require(type(s) is int and type(r) is int and e.source_span.start <= s <= e.source_span.end
                        and 0 <= r <= len(e.data), 'INTERIOR_POINT_RANGE', (e.owner,s,r))
                require(s not in pp or pp[s] == r, 'CONFLICTING_INTERIOR_POINT', (e.owner,s))
                require(not is_identity or r == s-e.source_span.start,
                        'IDENTITY_MAP_CANNOT_REMAP_BYTES', (e.owner,s,r))
                pp[s]=r
            for p in e.points:
                require(isinstance(p,MapPoint) and isinstance(p.authority,Proof), 'INTERIOR_POINT_AUTHORITY', e.owner)
                point(p.source,p.relative)
            slot_spans=[]
            for slot in e.slots:
                require(slot.field not in slotmap and e.source_span.start+4 <= slot.source_span.start
                        and slot.source_span.end <= e.source_span.end and slot.relative >= 4
                        and slot.relative+4 <= len(e.data), 'INTERIOR_SLOT_RANGE_OR_IDENTITY', slot.field)
                local=Span(slot.relative,slot.relative+4)
                require(not any(local.overlaps(x) for x in slot_spans), 'OVERLAPPING_INTERIOR_SLOTS', e.owner)
                slot_spans.append(local);slotmap[slot.field]=(e,slot)
                point(slot.source_span.start,slot.relative);point(slot.source_span.end,slot.relative+4)
            ordered=sorted(pp.items())
            require(all(a[1] <= b[1] for a,b in zip(ordered,ordered[1:])),
                    'NONMONOTONE_SOURCE_MAP', e.owner)
            points[e.owner]=MappingProxyType(pp)
            delta += len(e.data)-e.source_span.size;prior=e.source_span.end
        self._points=MappingProxyType(points);self._slots=MappingProxyType(slotmap)
        self._identity_edits=frozenset(identity_edits);self.placements=MappingProxyType(placements)
        self.final_size=len(source)+delta
        require(self.final_size <= 0xffffffff, 'TS5_FINAL_SIZE_OVERFLOW', self.final_size)
        self.final_offsets=tuple(self.anchor(o) for o in self.geometry.offsets)
        require(self.final_offsets[0] == self.geometry.table_end
                and self.final_offsets[-1] == self.final_size
                and all(a < b for a,b in zip(self.final_offsets,self.final_offsets[1:]))
                and all(x%4==0 for x in self.final_offsets), 'FINAL_PARTITION_GEOMETRY', file)
        # Source and destination cluster unions must both remain disjoint.
        self.final_regions=[]; prev_src=prev_final=self.geometry.table_end
        for r in self.regions:
            require(isinstance(r.authority,Proof) and self.geometry.contains(r.partition,r.source_span)
                    and r.source_span.start >= prev_src, 'OVERLAPPING_OR_INVALID_CLUSTER_UNION', r.cluster)
            f=self.project(r.source_span)
            require(f.start >= prev_final and self.final_offsets[r.partition] <= f.start < f.end
                    <= self.final_offsets[r.partition+1], 'FINAL_CLUSTER_UNION_GEOMETRY', r.cluster)
            self.final_regions.append((r,f));prev_src=r.source_span.end;prev_final=f.end
        self.final_regions=tuple(self.final_regions)
        self.fingerprint=sha256(canonical_json({'file':file,'source':identity.sha256,
            'edits':[{'owner':e.owner,'source':[e.source_span.start,e.source_span.end],
                      'data':sha256(e.data),'writer':e.writer,'unit':e.unit,
                      'authority':e.authority.__dict__,
                      'points':[(p.source,p.relative,p.authority.__dict__) for p in e.points],
                      'slots':[(s.field,s.source_span.start,s.source_span.end,s.relative,s.authority.__dict__) for s in e.slots]}
                     for e in self.edits],
            'regions':[(r.cluster,r.unit,r.source_span.start,r.source_span.end,r.authority.__dict__) for r in self.regions],
            'final_offsets':self.final_offsets}))
        self.mapping_proof=Proof('IM03_COORDINATE_MAP:'+file,self.fingerprint,
                                 'DERIVED_FROM_PINNED_SOURCE_AND_EXPLICIT_RECIPE_SHAPES_NOT_A_RUNTIME_PROOF')
        self._starts=tuple(self._starts);self._deltas=tuple(self._deltas);self._sealed=True

    def edit_at(self, offset: int) -> PayloadEdit | None:
        i=bisect_right(self._starts,offset)-1
        if i >= 0 and offset < self.edits[i].source_span.end: return self.edits[i]
        return None

    def anchor(self, offset: int) -> int:
        require(type(offset) is int and 0 <= offset <= len(self.source), 'SOURCE_ANCHOR_RANGE', offset)
        i=bisect_right(self._starts,offset)-1
        if i < 0: return offset
        e=self.edits[i];d=self._deltas[i]
        if offset >= e.source_span.end: return offset+d+len(e.data)-e.source_span.size
        if e.owner in self._identity_edits or offset <= e.source_span.start+4: return offset+d
        require(offset in self._points[e.owner], 'UNPROVEN_INTERIOR_ANCHOR', (e.owner,offset))
        return self.placements[e.owner].start+self._points[e.owner][offset]

    def project(self, span: Span) -> Span:
        return Span(self.anchor(span.start),self.anchor(span.end))

    def field_position(self, field: FieldWrite) -> tuple[Span, PayloadEdit | None]:
        require(self.geometry.contains(field.partition,field.source_span), 'FIELD_PARTITION', field.field)
        require(self.source[field.source_span.start:field.source_span.end] == field.before,
                'FIELD_ORIGINAL_BYTES', field.field)
        loc=self.project(field.source_span)
        require(loc.size==4 and loc.start%4==0, 'FIELD_FINAL_STORAGE_WIDTH', field.field)
        require(self.final_offsets[field.partition] <= loc.start < loc.end <= self.final_offsets[field.partition+1],
                'FIELD_FINAL_PARTITION', field.field)
        e=self.edit_at(field.source_span.start)
        if e is not None:
            require(field.source_span.end <= e.source_span.end, 'FIELD_STRADDLES_RECIPE_BOUNDARY', field.field)
            binding=self._slots.get(field.field)
            require(binding is not None and binding[0].owner==e.owner and binding[1].source_span==field.source_span,
                    'INTERIOR_FIELD_SLOT_NOT_RESERVED', field.field)
            require(field.unit==e.unit, 'INTERIOR_WRITER_RESPONSIBILITY_CONFLICT', field.field)
        else:
            nxt=bisect_right(self._starts,field.source_span.start)
            require(nxt==len(self.edits) or self.edits[nxt].source_span.start>=field.source_span.end,
                    'FIELD_STRADDLES_RECIPE_BOUNDARY', field.field)
        return loc,e

    def assemble(self, fields: Iterable[FieldWrite] = ()) -> AssembledFile:
        fields=tuple(sorted(fields,key=lambda f:(f.source_span.start,f.field)))
        require(len({f.field for f in fields})==len(fields), 'DUPLICATE_FIELD_OPERATION', self.file)
        require(set(self._slots) <= {f.field for f in fields}, 'RESERVED_FIELD_NOT_PROPOSED', self.file)
        source=self.source;out=bytearray();journal=[]
        def base(s:Span,data:bytes,kind:str,writer:str,unit:str|None,proof:Proof):
            start=len(out);out.extend(data)
            step=JournalStep(f'BASE:{len(journal)}',kind,Span(start,len(out)),data,s,writer,unit,proof)
            journal.append(step)
        cursor=0
        for e in self.edits:
            if cursor < e.source_span.start:
                base(Span(cursor,e.source_span.start),source[cursor:e.source_span.start],
                     'SOURCE_COPY','FILE_PRESERVATION',None,self.identity.authority)
            base(e.source_span,e.data,'PREPARED_PAYLOAD',e.writer,e.unit,e.authority)
            cursor=e.source_span.end
        if cursor<len(source):
            base(Span(cursor,len(source)),source[cursor:],'SOURCE_COPY','FILE_PRESERVATION',None,self.identity.authority)
        require(len(out)==self.final_size,'SHAPE_ASSEMBLY_SIZE',self.file)
        bases=tuple(journal);base_starts=[b.final_span.start for b in bases]
        overlays=[];last_end=-1
        for f in fields:
            loc,e=self.field_position(f)
            require(loc.start >= last_end,'DUPLICATE_FINAL_FIELD_WRITER',f.field);last_end=loc.end
            parent=bases[bisect_right(base_starts,loc.start)-1]
            require(loc.end<=parent.final_span.end,'FIELD_SPANS_BASE_WRITERS',f.field)
            if e is None:
                require(bytes(out[loc.start:loc.end])==f.before,'PRESERVATION_BASE_FIELD_PREIMAGE',f.field)
            else:
                # The actual field proposal is subordinate to the containing
                # composed payload, not an independent overlapping replacement.
                require(parent.writer==e.writer and parent.unit==e.unit,'SLOT_PARENT_IDENTITY',f.field)
            old=bytes(out[loc.start:loc.end]);out[loc.start:loc.end]=f.after
            step=JournalStep('FIELD:'+f.field,'FIELD_SLOT' if e else 'FIELD',loc,f.after,f.source_span,
                    e.writer if e else 'FIELD:'+f.field, f.unit,f.authority,(parent.id,),f.allowed_mask,
                    tuple(loc.start+i for i in range(4) if old[i]!=f.after[i]))
            overlays.append(step);journal.append(step)
        # Last writer owns the FINAL header/count/offset table, not an old copy.
        table=source[:4]+struct.pack('<I',self.geometry.count)+struct.pack(f'<{len(self.final_offsets)}I',*self.final_offsets)
        ts=Span(0,self.geometry.table_end);before=bytes(out[:ts.end]);out[:ts.end]=table
        table_parents=tuple(b.id for b in bases if b.final_span.overlaps(ts))
        table_proof=Proof('IM03_FINAL_TABLE:'+self.file,sha256(table),
                         'INHERITED_TS5_GEOMETRY_FINAL_PARTITION_PREFIX_SUMS; '+self.fingerprint)
        step=JournalStep('TABLE:'+self.file,'FINAL_TABLE',ts,table,ts,'FINAL_TABLE',None,table_proof,
                        table_parents,None,tuple(i for i in range(ts.end) if before[i]!=table[i]))
        overlays.append(step);journal.append(step)
        require(len(out)==self.final_size,'LATE_WRITER_CHANGED_SHAPE',self.file)
        all_points={0,len(out)}
        for b in bases+tuple(overlays):all_points.update((b.final_span.start,b.final_span.end))
        for _,r in self.final_regions:all_points.update((r.start,r.end))
        points=sorted(all_points);overlays.sort(key=lambda x:x.final_span.start)
        os=[x.final_span.start for x in overlays];regs=self.final_regions;rs=[x[1].start for x in regs]
        ownership=[]
        for lo,hi in zip(points,points[1:]):
            i=bisect_right(os,lo)-1
            winner=overlays[i] if i>=0 and lo<overlays[i].final_span.end else bases[bisect_right(base_starts,lo)-1]
            unit=winner.unit;rp=winner.authority
            rix=bisect_right(rs,lo)-1
            if rix>=0 and lo<regs[rix][1].end:
                r,_=regs[rix]
                require(unit is None or unit==r.unit,'CLUSTER_FINAL_RESPONSIBILITY_CONFLICT',(winner.id,r.unit))
                unit=r.unit;rp=r.authority
            ownership.append(FinalOwnership(Span(lo,hi),winner.id,winner.writer,unit,rp))
        data=bytes(out)
        audit=audit_output(data,tuple(journal),tuple(ownership),self.final_offsets,self.geometry.prefix,self.final_regions)
        require(audit.local_complete,'FINAL_WRITER_RECONCILIATION_FAILED',audit.to_dict())
        return AssembledFile(self.file,data,self,tuple(journal),tuple(ownership),audit)


def audit_output(data: bytes, journal: tuple[JournalStep,...], ownership: tuple[FinalOwnership,...],
                 expected_offsets: tuple[int,...], expected_prefix: bytes,
                 regions: tuple[tuple[ResponsibilityRegion,Span],...]=()) -> LayoutAudit:
    """Re-measure coverage and winning bytes AFTER all stages including table.

    Equal overlapping declarations still count as multiple responsibility. A
    staging parent may be superseded, but the chosen final step must really be
    the last writer of its bytes. No literal zero counters are returned.
    """
    n=len(data);errors=[];events=defaultdict(lambda:[[],[]]);by={}
    for i,j in enumerate(journal):
        if j.id in by:errors.append('DUPLICATE_JOURNAL_ID:'+j.id)
        if len(j.data)!=j.final_span.size or j.final_span.end>n:errors.append('JOURNAL_RANGE:'+j.id)
        parents=[by.get(k) for k in j.supersedes]
        if any(p is None for p in parents):errors.append('MISSING_OR_FUTURE_STAGING_PARENT:'+j.id)
        if j.kind in ('FIELD','FIELD_SLOT','FINAL_TABLE'):
            live=[p for p in parents if p is not None]
            points=sorted({j.final_span.start,j.final_span.end,
                           *(max(j.final_span.start,p.final_span.start) for p in live if p.final_span.overlaps(j.final_span)),
                           *(min(j.final_span.end,p.final_span.end) for p in live if p.final_span.overlaps(j.final_span))})
            if not live or any(sum(p.final_span.start<=a<b<=p.final_span.end for p in live)!=1
                               for a,b in zip(points,points[1:])):
                errors.append('INCOMPLETE_STAGING_LINEAGE:'+j.id)
        by[j.id]=j
    for i,r in enumerate(ownership):
        if r.final_span.start<0 or r.final_span.end>n:errors.append('OWNERSHIP_RANGE:'+str(i));continue
        events[r.final_span.start][0].append(i);events[r.final_span.end][1].append(i)
    points=sorted({0,n,*events});active=set();assigned=unassigned=multiple=conflicting=0
    # Separate sweep over actual chronological write steps verifies last-writer identity.
    jevents=defaultdict(lambda:[[],[]])
    for i,j in enumerate(journal):
        jevents[j.final_span.start][0].append(i);jevents[j.final_span.end][1].append(i)
    points=sorted(set(points)|set(jevents));jactive=set()
    for lo,hi in zip(points,points[1:]):
        active.difference_update(events[lo][1]);active.update(events[lo][0])
        jactive.difference_update(jevents[lo][1]);jactive.update(jevents[lo][0])
        if not (0<=lo<hi<=n):continue
        if not active:unassigned+=hi-lo;continue
        assigned+=hi-lo
        if len(active)>1:multiple+=hi-lo
        mismatches=set();last=None if not jactive else journal[max(jactive)].id
        for i in active:
            r=ownership[i];j=by.get(r.step)
            if j is None or not (j.final_span.start<=lo<hi<=j.final_span.end):
                errors.append('OWNERSHIP_STEP_RANGE:'+r.step);mismatches.update(range(lo,hi));continue
            if r.step!=last:errors.append('STALE_FINAL_WRITER:'+r.step)
            if r.writer!=j.writer:errors.append('FINAL_WRITER_NAME_MISMATCH:'+r.step)
            allowed=[rr for rr,ss in regions if ss.start<=lo<hi<=ss.end]
            expected_unit=allowed[0].unit if len(allowed)==1 else j.unit
            if len(allowed)>1 or r.unit!=expected_unit:errors.append('FINAL_RESPONSIBILITY_UNIT_MISMATCH:'+r.step)
            expected=j.data[lo-j.final_span.start:hi-j.final_span.start]
            actual=data[lo:hi]
            if actual!=expected:mismatches.update(lo+k for k,(a,b) in enumerate(zip(actual,expected)) if a!=b)
        conflicting+=len(mismatches)
    try:
        g=Geometry.read(data);offsets=g.offsets
        if offsets!=expected_offsets:errors.append('FINAL_TABLE_PREFIX_SUM_MISMATCH')
        if g.prefix!=expected_prefix:errors.append('FINAL_PREFIX_MUTATION')
    except ContractError as ex:
        offsets=None;errors.append(ex.code)
    table=[j for j in journal if j.kind=='FINAL_TABLE']
    if len(table)!=1 or not journal or journal[-1].kind!='FINAL_TABLE':errors.append('FINAL_TABLE_NOT_LAST_UNIQUE_WRITER')
    elif table[0].final_span!=Span(0,8+4*len(expected_offsets)):errors.append('FINAL_TABLE_ENVELOPE')
    errors=tuple(sorted(set(errors)))
    good=not errors and unassigned==multiple==conflicting==0 and assigned==n
    return LayoutAudit(n,assigned,unassigned,multiple,conflicting,errors,offsets,good)


@dataclass(frozen=True)
class AssembledFile:
    file: str
    data: bytes
    layout: FinalLayout
    journal: tuple[JournalStep,...]
    ownership: tuple[FinalOwnership,...]
    audit: LayoutAudit
    product_accepted: bool = field(default=False,init=False)

    def __bool__(self):
        raise TypeError('An assembled in-memory file is not a validated product.')

    def emit_product(self,*args,**kwargs):
        raise ContractError('PRODUCT_EXPORT_REQUIRES_VAL01','No game-file export is available in IM03.')
