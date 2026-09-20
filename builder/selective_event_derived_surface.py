from __future__ import annotations

from collections import Counter, defaultdict
from dataclasses import asdict, dataclass
import hashlib
import json
import struct
from typing import Sequence

from builder.selective_event import ParsedEventTs5, SelectiveEventError

CANONICAL_PC_KO_SIZE = 1_156_480
CANONICAL_PC_KO_SHA256 = '0899bf81789acfbd243d43be209a8a3960933fa090960ac8c753c63f95f07bbe'
V351_ROWS_SHA256 = '7f394033fa56796d6822cb9403a027d6674d0a0e0a357c4981392da798306f5f'
V351_OCCURRENCES_SHA256 = '90b39ed75e738cf31906db3570a45bcc5175428d8904f46149e1ac906b3da4a6'
V351_MIXED_SHA256 = 'bbfbd910cfa3955e89d650c3408c12c96b31778101c7ef16c8605237a177a423'
V352_BINDINGS_SHA256 = '95f2b98120ddf20f287321393a9d2a52b6f7704d37786df0ef228ae50a47d15f'
V334_ROWS_SHA256 = 'aef17d206559ec548a5fb3c2414d8a1f17832f7e4c2df03b8468240926c11b65'
DERIVED_ROWS = 61
DERIVED_PURE_ROWS = 59
DERIVED_MIXED_ROWS = 2
DERIVED_OCCURRENCES = 62
MIXED_DIRECT_EDITS = 3
DERIVED_ORIGINAL_BYTES = 3_132
DERIVED_RAW_KO_BYTES = 4_104
DERIVED_PAYLOAD_GROWTH = 972
DERIVED_ALLOWED_OPCODES = frozenset((0x11, 0x12, 0x13))
EXPECTED_OPCODE_COUNTS = {0x11: 32, 0x12: 5, 0x13: 24}
EXPECTED_MIXED_ROW_IDS = (12476, 13029)
EXPECTED_V334_MAPPING_METHOD_COUNTS = {
    'EDITOR_TARGET_ORDINAL': 58,
    'EDITOR_TARGET_ALIGNMENT': 3,
}

PARTICLE_BYTES = {
    '이': bytes.fromhex('f36b'),
    '가': bytes.fromhex('eb40'),
    '을': bytes.fromhex('f35a'),
    '를': bytes.fromhex('ef45'),
}

@dataclass(frozen=True)
class DerivedBindingRecord:
    row_id: int
    partition: int
    original_offset: int
    ko_offset: int
    opcode: int
    original_command_length: int
    ko_command_length: int
    original_sha256: str
    ko_sha256: str
    v351_class: str
    implementation_profile: str
    raw_growth: int

@dataclass(frozen=True)
class DerivedOccurrenceRecord:
    row_id: int
    hit_index: int
    escape: str
    pc_authored_surface: str
    normalization_authorized: bool
    pronunciation_singleton_safe: bool

@dataclass(frozen=True)
class MixedDirectEdit:
    row_id: int
    hit_index: int
    escape: str
    source_particle: str
    target_particle: str

@dataclass(frozen=True)
class DerivedSurfaceReport:
    rows: int
    pure_rows: int
    mixed_rows: int
    derived_occurrences: int
    mixed_direct_edits: int
    original_bytes: int
    raw_ko_bytes: int
    transformed_bytes: int
    payload_growth_vs_original: int
    opcode_counts: dict[int, int]
    transformed_corpus_sha256: str
    rowset_sha256: str

    def to_dict(self) -> dict:
        return asdict(self)


def _fail(code: str, detail: str) -> None:
    raise SelectiveEventError(code, detail)


def _sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def _jsonl(blob: bytes, code: str) -> list[dict]:
    try:
        text = blob.decode('utf-8')
    except UnicodeDecodeError as exc:
        _fail(code, f'utf8:{exc}')
    out = []
    for line_no, line in enumerate(text.splitlines(), 1):
        if not line:
            continue
        try:
            obj = json.loads(line)
        except json.JSONDecodeError as exc:
            _fail(code, f'line={line_no} json:{exc}')
        if not isinstance(obj, dict):
            _fail(code, f'line={line_no} not-object')
        out.append(obj)
    return out


def _int(obj: dict, name: str, code: str) -> int:
    value = obj.get(name)
    if not isinstance(value, int) or isinstance(value, bool):
        _fail(code, f'{name}={value!r}')
    return value


def load_derived_surface_authority(
    rows_blob: bytes,
    occurrences_blob: bytes,
    mixed_blob: bytes,
    bindings_blob: bytes,
    *,
    require_canonical: bool = True,
) -> tuple[tuple[DerivedBindingRecord, ...], tuple[DerivedOccurrenceRecord, ...], tuple[MixedDirectEdit, ...]]:
    if require_canonical:
        checks = (
            ('DERIVED_ROWS_SHA_FAIL', rows_blob, V351_ROWS_SHA256),
            ('DERIVED_OCC_SHA_FAIL', occurrences_blob, V351_OCCURRENCES_SHA256),
            ('DERIVED_MIXED_SHA_FAIL', mixed_blob, V351_MIXED_SHA256),
            ('DERIVED_BINDINGS_SHA_FAIL', bindings_blob, V352_BINDINGS_SHA256),
        )
        for code, blob, expected in checks:
            actual = _sha256(blob)
            if actual != expected:
                _fail(code, actual)

    rows_values = _jsonl(rows_blob, 'DERIVED_ROWS_JSON_FAIL')
    occurrence_values = _jsonl(occurrences_blob, 'DERIVED_OCC_JSON_FAIL')
    mixed_values = _jsonl(mixed_blob, 'DERIVED_MIXED_JSON_FAIL')
    binding_values = _jsonl(bindings_blob, 'DERIVED_BINDINGS_JSON_FAIL')

    rows_by_id: dict[int, dict] = {}
    for obj in rows_values:
        row_id = _int(obj, 'row_id', 'DERIVED_ROWS_FIELD_FAIL')
        if row_id in rows_by_id:
            _fail('DERIVED_ROWS_DUPLICATE', str(row_id))
        if obj.get('policy') != 'PC_AUTHORED_DERIVED_SURFACE_V1':
            _fail('DERIVED_ROWS_POLICY_FAIL', str(row_id))
        if obj.get('product_disposition') != 'INCLUDE_KO_NOT_IMPLEMENTED':
            _fail('DERIVED_ROWS_DISPOSITION_FAIL', str(row_id))
        klass = obj.get('v346_class')
        profile = obj.get('implementation_profile')
        if klass == 'COPULA_DERIVED_ONLY':
            if profile != 'RAW_PC_KO_PRESERVE_AUTHORED_DERIVED_SURFACE':
                _fail('DERIVED_ROWS_PROFILE_FAIL', str(row_id))
        elif klass == 'MIXED_DIRECT_AND_DERIVED_RISK':
            if profile != 'RAW_PC_KO_THEN_EXACT_DIRECT_PARTICLE_NORMALIZATION':
                _fail('DERIVED_ROWS_PROFILE_FAIL', str(row_id))
        else:
            _fail('DERIVED_ROWS_CLASS_FAIL', f'row={row_id} class={klass!r}')
        rows_by_id[row_id] = obj

    bindings: list[DerivedBindingRecord] = []
    for obj in binding_values:
        row_id = _int(obj, 'row_id', 'DERIVED_BINDING_FIELD_FAIL')
        source = rows_by_id.get(row_id)
        if source is None:
            _fail('DERIVED_BINDING_ROW_MISSING', str(row_id))
        names = ('partition','original_offset','ko_offset','opcode','original_command_length','ko_command_length','raw_growth')
        for name in names:
            if _int(obj, name, 'DERIVED_BINDING_FIELD_FAIL') != _int(source, name, 'DERIVED_ROWS_FIELD_FAIL'):
                _fail('DERIVED_BINDING_V351_MISMATCH', f'row={row_id} field={name}')
        if obj.get('v351_class') != source.get('v346_class') or obj.get('implementation_profile') != source.get('implementation_profile'):
            _fail('DERIVED_BINDING_PROFILE_MISMATCH', str(row_id))
        if obj.get('v334_mapping_method') not in {'EDITOR_TARGET_ORDINAL','EDITOR_TARGET_ALIGNMENT'}:
            _fail('DERIVED_BINDING_MAPPING_METHOD_FAIL', str(row_id))
        if obj.get('v334_disposition') != 'REPLACE_FROM_PC_KO':
            _fail('DERIVED_BINDING_DISPOSITION_FAIL', str(row_id))
        oh = obj.get('original_sha256'); kh = obj.get('ko_sha256')
        if not isinstance(oh, str) or len(oh) != 64 or not isinstance(kh, str) or len(kh) != 64:
            _fail('DERIVED_BINDING_HASH_FIELD_FAIL', str(row_id))
        r = DerivedBindingRecord(
            row_id=row_id,
            partition=_int(obj,'partition','DERIVED_BINDING_FIELD_FAIL'),
            original_offset=_int(obj,'original_offset','DERIVED_BINDING_FIELD_FAIL'),
            ko_offset=_int(obj,'ko_offset','DERIVED_BINDING_FIELD_FAIL'),
            opcode=_int(obj,'opcode','DERIVED_BINDING_FIELD_FAIL'),
            original_command_length=_int(obj,'original_command_length','DERIVED_BINDING_FIELD_FAIL'),
            ko_command_length=_int(obj,'ko_command_length','DERIVED_BINDING_FIELD_FAIL'),
            original_sha256=oh,
            ko_sha256=kh,
            v351_class=obj.get('v351_class'),
            implementation_profile=obj.get('implementation_profile'),
            raw_growth=_int(obj,'raw_growth','DERIVED_BINDING_FIELD_FAIL'),
        )
        if r.opcode not in DERIVED_ALLOWED_OPCODES:
            _fail('DERIVED_BINDING_OPCODE_FAIL', f'row={row_id} opcode={r.opcode:#x}')
        if r.original_command_length <= 0 or r.ko_command_length <= 0 or r.original_command_length % 4 or r.ko_command_length % 4:
            _fail('DERIVED_BINDING_LENGTH_FAIL', str(row_id))
        if r.raw_growth != r.ko_command_length-r.original_command_length:
            _fail('DERIVED_BINDING_GROWTH_FAIL', str(row_id))
        bindings.append(r)

    occurrences: list[DerivedOccurrenceRecord] = []
    occ_counts = Counter()
    for obj in occurrence_values:
        row_id = _int(obj,'row_id','DERIVED_OCC_FIELD_FAIL')
        if row_id not in rows_by_id:
            _fail('DERIVED_OCC_ROW_FAIL', str(row_id))
        if obj.get('occurrence_kind') != 'PC_AUTHORED_DERIVED_SURFACE' or obj.get('policy') != 'PC_AUTHORED_DERIVED_SURFACE_V1':
            _fail('DERIVED_OCC_POLICY_FAIL', str(row_id))
        if obj.get('normalization_authorized') is not False or obj.get('pronunciation_singleton_safe') is not False:
            _fail('DERIVED_OCC_NORMALIZATION_FAIL', str(row_id))
        escape=obj.get('escape'); surface=obj.get('pc_authored_surface')
        if not isinstance(escape,str) or not escape.startswith('\\') or not isinstance(surface,str) or not surface:
            _fail('DERIVED_OCC_TEXT_FAIL', str(row_id))
        occurrences.append(DerivedOccurrenceRecord(row_id,_int(obj,'hit_index','DERIVED_OCC_FIELD_FAIL'),escape,surface,False,False))
        occ_counts[row_id] += 1

    edits: list[MixedDirectEdit] = []
    mixed_ids=[]
    for obj in mixed_values:
        row_id=_int(obj,'row_id','DERIVED_MIXED_FIELD_FAIL'); mixed_ids.append(row_id)
        if obj.get('profile')!='V351_MIXED_COMPOSITE_V1' or obj.get('raw_pc_ko_first') is not True:
            _fail('DERIVED_MIXED_PROFILE_FAIL', str(row_id))
        if obj.get('transform_order') != ['RAW_PC_KO_COMMAND_OVERLAY','EXACT_DIRECT_PARTICLE_NORMALIZATION','INHERITED_EVENT_RELOCATION_AND_VALIDATION']:
            _fail('DERIVED_MIXED_ORDER_FAIL', str(row_id))
        norms=obj.get('direct_normalizations')
        if not isinstance(norms,list) or len(norms)!=_int(obj,'direct_edit_count','DERIVED_MIXED_FIELD_FAIL'):
            _fail('DERIVED_MIXED_COUNT_FAIL', str(row_id))
        for n in norms:
            source=n.get('source_particle'); target=n.get('target_particle'); escape=n.get('escape')
            if (source,target) not in {('이','가'),('을','를')} or not isinstance(escape,str) or not escape.startswith('\\'):
                _fail('DERIVED_MIXED_EDIT_FAIL', str(row_id))
            edits.append(MixedDirectEdit(row_id,_int(n,'hit_index','DERIVED_MIXED_FIELD_FAIL'),escape,source,target))

    if len({r.row_id for r in bindings}) != len(bindings):
        _fail('DERIVED_BINDING_DUPLICATE', 'row_id')
    if set(rows_by_id) != {r.row_id for r in bindings}:
        _fail('DERIVED_BINDING_COVERAGE_FAIL', 'rowset')

    if require_canonical:
        pure=sum(r.v351_class=='COPULA_DERIVED_ONLY' for r in bindings)
        mixed=sum(r.v351_class=='MIXED_DIRECT_AND_DERIVED_RISK' for r in bindings)
        if (len(bindings),pure,mixed,len(occurrences),len(edits)) != (DERIVED_ROWS,DERIVED_PURE_ROWS,DERIVED_MIXED_ROWS,DERIVED_OCCURRENCES,MIXED_DIRECT_EDITS):
            _fail('DERIVED_CANONICAL_COUNT_FAIL', repr((len(bindings),pure,mixed,len(occurrences),len(edits))))
        if tuple(mixed_ids) != EXPECTED_MIXED_ROW_IDS:
            _fail('DERIVED_MIXED_ROW_IDS_FAIL', repr(tuple(mixed_ids)))
        if sum(r.original_command_length for r in bindings) != DERIVED_ORIGINAL_BYTES or sum(r.ko_command_length for r in bindings) != DERIVED_RAW_KO_BYTES:
            _fail('DERIVED_CANONICAL_BYTE_TOTAL_FAIL', 'totals')
        if sum(r.raw_growth for r in bindings) != DERIVED_PAYLOAD_GROWTH:
            _fail('DERIVED_CANONICAL_GROWTH_FAIL', str(sum(r.raw_growth for r in bindings)))
        if dict(sorted(Counter(r.opcode for r in bindings).items())) != EXPECTED_OPCODE_COUNTS:
            _fail('DERIVED_CANONICAL_OPCODE_COUNTS_FAIL', repr(Counter(r.opcode for r in bindings)))
        method_counts = Counter(obj.get('v334_mapping_method') for obj in binding_values)
        if dict(method_counts) != EXPECTED_V334_MAPPING_METHOD_COUNTS:
            _fail('DERIVED_CANONICAL_MAPPING_METHOD_COUNTS_FAIL', repr(dict(method_counts)))
        if Counter(o.row_id for o in occurrences) != Counter({rid:_int(rows_by_id[rid],'derived_occurrences','DERIVED_ROWS_FIELD_FAIL') for rid in rows_by_id}):
            _fail('DERIVED_OCC_ROW_COUNT_FAIL', 'per-row')
    return tuple(bindings), tuple(occurrences), tuple(edits)


def _message_range(command: bytes) -> tuple[int,int]:
    if len(command) < 4 or command[0] not in DERIVED_ALLOWED_OPCODES:
        _fail('DERIVED_COMMAND_OPCODE_FAIL', command[:4].hex())
    try:
        end=command.index(0,4)
    except ValueError:
        _fail('DERIVED_STRING_TERMINATOR_MISSING', f'opcode={command[0]:#x}')
    if any(command[end+1:]):
        _fail('DERIVED_TRAILING_BYTES_FAIL', f'opcode={command[0]:#x}')
    return 4,end


def _transform_mixed_command(command: bytes, edits: Sequence[MixedDirectEdit]) -> bytes:
    start,end=_message_range(command)
    output=bytearray(command)
    positions=[]
    for edit in sorted(edits,key=lambda x:x.hit_index):
        source=PARTICLE_BYTES[edit.source_particle]; target=PARTICLE_BYTES[edit.target_particle]
        needle=edit.escape.encode('ascii')+source
        found=[]; p=start
        while True:
            q=command.find(needle,p,end)
            if q<0: break
            found.append(q); p=q+1
        if len(found)!=1:
            _fail('DERIVED_MIXED_NEEDLE_MULTIPLICITY_FAIL', f'row={edit.row_id} needle={needle.hex()} found={len(found)}')
        pos=found[0]+len(edit.escape)
        positions.append(pos)
        if command[pos:pos+2]!=source:
            _fail('DERIVED_MIXED_SOURCE_BYTES_FAIL', f'row={edit.row_id}')
        output[pos:pos+2]=target
    if len(set(positions))!=len(positions):
        _fail('DERIVED_MIXED_EDIT_COLLISION', repr(positions))
    transformed=bytes(output)
    if len(transformed)!=len(command) or transformed[:4]!=command[:4] or _message_range(transformed)!=(start,end):
        _fail('DERIVED_MIXED_TRANSFORM_SHAPE_FAIL', f'opcode={command[0]:#x}')
    return transformed


def _index_grouped_items(parsed: ParsedEventTs5) -> dict[tuple[int,int], tuple[int,bytes]]:
    out={}
    for partition in parsed.partitions:
        for item_index,item in enumerate(partition.grouped_items):
            out[(partition.index,item.start)] = (item_index,item.data)
    return out


def apply_pc_authored_derived_surfaces(
    original: ParsedEventTs5,
    korean_blob: bytes,
    current_item_bytes: Sequence[Sequence[bytes]],
    bindings: Sequence[DerivedBindingRecord],
    occurrences: Sequence[DerivedOccurrenceRecord],
    mixed_edits: Sequence[MixedDirectEdit],
    *,
    require_canonical: bool = True,
) -> tuple[tuple[tuple[bytes,...],...], DerivedSurfaceReport]:
    if len(current_item_bytes)!=len(original.partitions):
        _fail('DERIVED_PARTITION_COUNT_FAIL', f'current={len(current_item_bytes)} original={len(original.partitions)}')
    if require_canonical:
        if len(korean_blob)!=CANONICAL_PC_KO_SIZE:
            _fail('DERIVED_KO_SIZE_FAIL', str(len(korean_blob)))
        if _sha256(korean_blob)!=CANONICAL_PC_KO_SHA256:
            _fail('DERIVED_KO_SHA_FAIL', _sha256(korean_blob))

    original_index=_index_grouped_items(original)
    current=[list(map(bytes,part)) for part in current_item_bytes]
    occ_by_row=defaultdict(list)
    for o in occurrences: occ_by_row[o.row_id].append(o)
    edit_by_row=defaultdict(list)
    for e in mixed_edits: edit_by_row[e.row_id].append(e)
    h=hashlib.sha256(); opcounts=Counter(); raw=orig=transformed_total=0

    for row in bindings:
        binding=original_index.get((row.partition,row.original_offset))
        if binding is None:
            _fail('DERIVED_ORIGINAL_BINDING_MISSING', f'row={row.row_id}')
        item_index,original_item=binding
        if item_index>=len(current[row.partition]):
            _fail('DERIVED_CURRENT_ITEM_RANGE_FAIL', f'row={row.row_id}')
        if len(original_item)!=row.original_command_length or not original_item or original_item[0]!=row.opcode:
            _fail('DERIVED_ORIGINAL_BINDING_FAIL', f'row={row.row_id}')
        if _sha256(original_item)!=row.original_sha256:
            _fail('DERIVED_ORIGINAL_HASH_FAIL', f'row={row.row_id}')
        if current[row.partition][item_index]!=original_item:
            _fail('DERIVED_BASELINE_FAIL', f'row={row.row_id} offset={row.original_offset:#x}')
        if row.ko_offset<0 or row.ko_offset+row.ko_command_length>len(korean_blob):
            _fail('DERIVED_KO_RANGE_FAIL', f'row={row.row_id}')
        ko_item=korean_blob[row.ko_offset:row.ko_offset+row.ko_command_length]
        if len(ko_item)!=row.ko_command_length or not ko_item or ko_item[0]!=row.opcode:
            _fail('DERIVED_KO_BINDING_FAIL', f'row={row.row_id}')
        if _sha256(ko_item)!=row.ko_sha256:
            _fail('DERIVED_KO_HASH_FAIL', f'row={row.row_id}')
        expected_occ=len(occ_by_row[row.row_id])
        if expected_occ<1:
            _fail('DERIVED_OCCURRENCE_BINDING_FAIL', f'row={row.row_id}')
        edits=edit_by_row.get(row.row_id,())
        if row.v351_class=='COPULA_DERIVED_ONLY':
            if edits:
                _fail('DERIVED_PURE_HAS_DIRECT_EDIT', f'row={row.row_id}')
            transformed=ko_item
        else:
            if not edits:
                _fail('DERIVED_MIXED_EDIT_MISSING', f'row={row.row_id}')
            transformed=_transform_mixed_command(ko_item,edits)
        current[row.partition][item_index]=transformed
        raw+=len(ko_item); orig+=len(original_item); transformed_total+=len(transformed); opcounts[row.opcode]+=1
        h.update(struct.pack('<IIIH',row.row_id,row.original_offset,row.ko_offset,len(transformed)))
        h.update(hashlib.sha256(transformed).digest())

    rowset=b''.join(struct.pack('<III',r.row_id,r.original_offset,r.ko_offset) for r in bindings)
    report=DerivedSurfaceReport(
        rows=len(bindings),
        pure_rows=sum(r.v351_class=='COPULA_DERIVED_ONLY' for r in bindings),
        mixed_rows=sum(r.v351_class=='MIXED_DIRECT_AND_DERIVED_RISK' for r in bindings),
        derived_occurrences=len(occurrences),
        mixed_direct_edits=len(mixed_edits),
        original_bytes=orig,
        raw_ko_bytes=raw,
        transformed_bytes=transformed_total,
        payload_growth_vs_original=transformed_total-orig,
        opcode_counts=dict(sorted(opcounts.items())),
        transformed_corpus_sha256=h.hexdigest(),
        rowset_sha256=_sha256(rowset),
    )
    if require_canonical:
        expected={'rows':61,'pure_rows':59,'mixed_rows':2,'derived_occurrences':62,'mixed_direct_edits':3,'original_bytes':3132,'raw_ko_bytes':4104,'transformed_bytes':4104,'payload_growth_vs_original':972,'opcode_counts':EXPECTED_OPCODE_COUNTS}
        for field,value in expected.items():
            actual=getattr(report,field)
            if actual!=value:
                _fail('DERIVED_CANONICAL_REPORT_FAIL', f'{field}={actual!r} expected={value!r}')
    return tuple(tuple(part) for part in current), report
