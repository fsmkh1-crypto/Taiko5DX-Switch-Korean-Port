from __future__ import annotations

from dataclasses import asdict, dataclass
from collections import Counter
import hashlib
import json
import struct
from typing import Sequence

from builder.selective_event import ParsedEventTs5, SelectiveEventError

CANONICAL_PC_KO_SIZE = 1_156_480
CANONICAL_PC_KO_SHA256 = '0899bf81789acfbd243d43be209a8a3960933fa090960ac8c753c63f95f07bbe'
LEXICAL_ROWS = 12
LEXICAL_GROWTH = 200
LEXICAL_APP_SHA256 = 'd0c6bf82792f1edbcc04363205c7b11f0ce11293ebb3c8dffa56761aa0b87edd'
V346_INCLUDE_ROWSET_SHA256 = '2e3b5b7981ee6b096a3dcc971fb5169cc8ff691c15f98132ef088e8cb07a4014'
LEXICAL_ALLOWED_OPCODES = frozenset((0x11, 0x13))
EXPECTED_ROW_IDS = (
    6383, 6408, 8526, 8543, 11056, 11759,
    11788, 12355, 12370, 13045, 13048, 13064,
)

@dataclass(frozen=True)
class LexicalApplicabilityRecord:
    row_id: int
    partition: int
    original_offset: int
    ko_offset: int
    opcode: int
    original_command_length: int
    ko_command_length: int
    escape: str
    original_sha256: str
    ko_sha256: str
    growth: int

@dataclass(frozen=True)
class LexicalOverlayReport:
    rows: int
    raw_ko_bytes: int
    original_bytes: int
    payload_growth: int
    opcode_counts: dict[int, int]
    rowset_sha256: str
    transformed_corpus_sha256: str

    def to_dict(self) -> dict:
        return asdict(self)


def _fail(code: str, detail: str) -> None:
    raise SelectiveEventError(code, detail)


def _sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def _int(obj: dict, name: str, code: str) -> int:
    v = obj.get(name)
    if not isinstance(v, int) or isinstance(v, bool):
        _fail(code, f'{name}={v!r}')
    return v


def load_lexical_applicability(blob: bytes, *, require_canonical: bool = True) -> tuple[LexicalApplicabilityRecord, ...]:
    if require_canonical and _sha256(blob) != LEXICAL_APP_SHA256:
        _fail('LEXICAL_APP_SHA_FAIL', _sha256(blob))
    try:
        text = blob.decode('utf-8')
    except UnicodeDecodeError as exc:
        _fail('LEXICAL_APP_UTF8_FAIL', str(exc))
    rows = []
    for line_no, line in enumerate(text.splitlines(), 1):
        if not line:
            continue
        try:
            obj = json.loads(line)
        except json.JSONDecodeError as exc:
            _fail('LEXICAL_APP_JSON_FAIL', f'line={line_no} {exc}')
        if obj.get('class') != 'LEXICAL_FALSE_POSITIVE_GAMUN' or obj.get('product') != 'INCLUDE_KO':
            _fail('LEXICAL_APP_CLASS_FAIL', f'line={line_no}')
        if obj.get('surface') != '가문':
            _fail('LEXICAL_APP_SURFACE_FAIL', f'line={line_no} surface={obj.get("surface")!r}')
        escape = obj.get('escape')
        if not isinstance(escape, str) or not escape.startswith('\\#'):
            _fail('LEXICAL_APP_ESCAPE_FAIL', f'line={line_no} escape={escape!r}')
        try:
            escape.encode('ascii')
        except UnicodeEncodeError:
            _fail('LEXICAL_APP_ESCAPE_FAIL', f'line={line_no} escape={escape!r}')
        r = LexicalApplicabilityRecord(
            row_id=_int(obj,'row_id','LEXICAL_APP_FIELD_FAIL'),
            partition=_int(obj,'partition','LEXICAL_APP_FIELD_FAIL'),
            original_offset=_int(obj,'original_offset','LEXICAL_APP_FIELD_FAIL'),
            ko_offset=_int(obj,'ko_offset','LEXICAL_APP_FIELD_FAIL'),
            opcode=_int(obj,'opcode','LEXICAL_APP_FIELD_FAIL'),
            original_command_length=_int(obj,'original_command_length','LEXICAL_APP_FIELD_FAIL'),
            ko_command_length=_int(obj,'ko_command_length','LEXICAL_APP_FIELD_FAIL'),
            escape=escape,
            original_sha256=obj.get('original_sha256'),
            ko_sha256=obj.get('ko_sha256'),
            growth=_int(obj,'growth','LEXICAL_APP_FIELD_FAIL'),
        )
        if r.opcode not in LEXICAL_ALLOWED_OPCODES:
            _fail('LEXICAL_APP_OPCODE_FAIL', f'row={r.row_id} opcode={r.opcode:#x}')
        if r.original_command_length <= 0 or r.ko_command_length <= 0:
            _fail('LEXICAL_APP_LENGTH_FAIL', f'row={r.row_id}')
        if r.original_command_length % 4 or r.ko_command_length % 4:
            _fail('LEXICAL_APP_ALIGNMENT_FAIL', f'row={r.row_id}')
        if r.growth != r.ko_command_length - r.original_command_length:
            _fail('LEXICAL_APP_GROWTH_FAIL', f'row={r.row_id}')
        for name, value in (('original_sha256',r.original_sha256),('ko_sha256',r.ko_sha256)):
            if not isinstance(value, str) or len(value) != 64:
                _fail('LEXICAL_APP_HASH_FIELD_FAIL', f'row={r.row_id} {name}={value!r}')
        rows.append(r)
    if len({r.row_id for r in rows}) != len(rows):
        _fail('LEXICAL_APP_ROW_COLLISION', 'duplicate row_id')
    if len({(r.partition,r.original_offset) for r in rows}) != len(rows):
        _fail('LEXICAL_APP_ORIGINAL_COLLISION', 'duplicate original binding')
    if len({r.ko_offset for r in rows}) != len(rows):
        _fail('LEXICAL_APP_KO_COLLISION', 'duplicate KO binding')

    rowset = b''.join(struct.pack('<IIIBBBB',r.row_id,r.original_offset,r.ko_offset,r.opcode,4,1,0) for r in rows)
    if require_canonical:
        if len(rows) != LEXICAL_ROWS:
            _fail('LEXICAL_APP_COUNT_FAIL', str(len(rows)))
        if tuple(r.row_id for r in rows) != EXPECTED_ROW_IDS:
            _fail('LEXICAL_APP_ROW_IDS_FAIL', repr(tuple(r.row_id for r in rows)))
        if sum(r.growth for r in rows) != LEXICAL_GROWTH:
            _fail('LEXICAL_APP_TOTAL_GROWTH_FAIL', str(sum(r.growth for r in rows)))
        if _sha256(rowset) != V346_INCLUDE_ROWSET_SHA256:
            _fail('LEXICAL_APP_V346_ROWSET_FAIL', _sha256(rowset))
    return tuple(rows)


def _index_grouped_items(parsed: ParsedEventTs5) -> dict[tuple[int,int], tuple[int,bytes]]:
    result = {}
    for partition in parsed.partitions:
        for item_index, item in enumerate(partition.grouped_items):
            result[(partition.index,item.start)] = (item_index,item.data)
    return result


def apply_lexical_false_positive_rows(
    original: ParsedEventTs5,
    korean_blob: bytes,
    current_item_bytes: Sequence[Sequence[bytes]],
    applicability: Sequence[LexicalApplicabilityRecord],
    *,
    require_canonical: bool = True,
) -> tuple[tuple[tuple[bytes,...],...], LexicalOverlayReport]:
    if len(current_item_bytes) != len(original.partitions):
        _fail('LEXICAL_PARTITION_COUNT_FAIL', f'current={len(current_item_bytes)} original={len(original.partitions)}')
    if require_canonical:
        if len(korean_blob) != CANONICAL_PC_KO_SIZE:
            _fail('LEXICAL_KO_FILE_SIZE_FAIL', str(len(korean_blob)))
        if _sha256(korean_blob) != CANONICAL_PC_KO_SHA256:
            _fail('LEXICAL_KO_FILE_SHA_FAIL', _sha256(korean_blob))

    original_index = _index_grouped_items(original)
    current = [list(map(bytes, part)) for part in current_item_bytes]
    opcounts = Counter()
    h = hashlib.sha256()
    raw = 0
    orig = 0

    for row in applicability:
        binding = original_index.get((row.partition,row.original_offset))
        if binding is None:
            _fail('LEXICAL_ORIGINAL_BINDING_MISSING', f'row={row.row_id}')
        item_index, original_item = binding
        if item_index >= len(current[row.partition]):
            _fail('LEXICAL_CURRENT_ITEM_RANGE_FAIL', f'row={row.row_id}')
        if len(original_item) != row.original_command_length or original_item[0] != row.opcode:
            _fail('LEXICAL_ORIGINAL_BINDING_FAIL', f'row={row.row_id}')
        if _sha256(original_item) != row.original_sha256:
            _fail('LEXICAL_ORIGINAL_HASH_FAIL', f'row={row.row_id}')
        if current[row.partition][item_index] != original_item:
            _fail('LEXICAL_BASELINE_FAIL', f'row={row.row_id} offset={row.original_offset:#x}')
        if row.ko_offset < 0 or row.ko_offset + row.ko_command_length > len(korean_blob):
            _fail('LEXICAL_KO_BINDING_RANGE_FAIL', f'row={row.row_id}')
        ko_item = korean_blob[row.ko_offset:row.ko_offset+row.ko_command_length]
        if len(ko_item) != row.ko_command_length or not ko_item or ko_item[0] != row.opcode:
            _fail('LEXICAL_KO_BINDING_FAIL', f'row={row.row_id}')
        if _sha256(ko_item) != row.ko_sha256:
            _fail('LEXICAL_KO_HASH_FAIL', f'row={row.row_id}')
        current[row.partition][item_index] = ko_item
        raw += len(ko_item)
        orig += len(original_item)
        opcounts[row.opcode] += 1
        h.update(struct.pack('<IIIH',row.row_id,row.original_offset,row.ko_offset,len(ko_item)))
        h.update(hashlib.sha256(ko_item).digest())

    rowset = b''.join(struct.pack('<IIIBBBB',r.row_id,r.original_offset,r.ko_offset,r.opcode,4,1,0) for r in applicability)
    report = LexicalOverlayReport(
        rows=len(applicability),
        raw_ko_bytes=raw,
        original_bytes=orig,
        payload_growth=raw-orig,
        opcode_counts=dict(sorted(opcounts.items())),
        rowset_sha256=_sha256(rowset),
        transformed_corpus_sha256=h.hexdigest(),
    )
    if require_canonical:
        if report.rows != LEXICAL_ROWS:
            _fail('LEXICAL_REPORT_COUNT_FAIL', str(report.rows))
        if report.payload_growth != LEXICAL_GROWTH:
            _fail('LEXICAL_REPORT_GROWTH_FAIL', str(report.payload_growth))
        if report.opcode_counts != {0x11:4,0x13:8}:
            _fail('LEXICAL_REPORT_OPCODE_COUNTS_FAIL', repr(report.opcode_counts))
        if report.rowset_sha256 != V346_INCLUDE_ROWSET_SHA256:
            _fail('LEXICAL_REPORT_ROWSET_FAIL', report.rowset_sha256)
    return tuple(tuple(part) for part in current), report
