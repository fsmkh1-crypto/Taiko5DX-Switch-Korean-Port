from __future__ import annotations

from collections import Counter
from dataclasses import asdict, dataclass
import hashlib
import struct
from typing import Iterable, Sequence

from builder.selective_event import ParsedEventTs5, SelectiveEventError


PARTICLE_LEDGER_RECORD = struct.Struct('<IHIIBBBBxHH')
PARTICLE_LEDGER_RECORD_COUNT = 1_251
PARTICLE_LEDGER_SHA256 = 'b6d228b6b1e8e23285763b88d5d5eda6064153433123283217c4ea955d550a4d'
PARTICLE_ROWSET_SHA256 = '8282d175c6666f8fa4700a28f4917ea32abe3d315d0b7a98ebdee53650831aa7'
PARTICLE_TRANSFORMED_CORPUS_SHA256 = 'f86a4f49f18c741445dcf9fc69390b818be5feba7f256973a9a69cdbd33368c5'
PARTICLE_OCCURRENCES = 1_389
PARTICLE_AGGREGATE_SHRINK = 5_556
PARTICLE_CODE3_ROWS = 1_226
PARTICLE_CHOICE_OVERLAP_ROWS = 25
CANONICAL_PC_KO_SIZE = 1_156_480
CANONICAL_PC_KO_SHA256 = '0899bf81789acfbd243d43be209a8a3960933fa090960ac8c753c63f95f07bbe'

SEMANTIC_INCLUDE_KO_CHOICE = 2
SEMANTIC_INCLUDE_KO_FIXED_SURFACE_PARTICLE = 3

# Exact compact-Korean byte surfaces proven by V344.
PARTICLE_REPLACEMENTS = (
    (bytes.fromhex('f35928ed6129'), bytes.fromhex('ed61'), '은(는)'),
    (bytes.fromhex('f36b28eb4029'), bytes.fromhex('eb40'), '이(가)'),
    (bytes.fromhex('f35a28ef4529'), bytes.fromhex('ef45'), '을(를)'),
    (bytes.fromhex('eb9a28f2cb29'), bytes.fromhex('f2cb'), '과(와)'),
    (bytes.fromhex('f2cb28eb9a29'), bytes.fromhex('f2cb'), '와(과)'),
    (bytes.fromhex('28f35729eecc'), bytes.fromhex('eecc'), '(으)로'),
)
EXPECTED_LITERAL_COUNTS = {
    '은(는)': 521,
    '이(가)': 395,
    '을(를)': 358,
    '과(와)': 41,
    '와(과)': 51,
    '(으)로': 23,
}


@dataclass(frozen=True)
class ParticleLedgerRecord:
    row_id: int
    partition: int
    original_offset: int
    ko_offset: int
    opcode: int
    semantic_code: int
    occurrence_count: int
    choice_overlap: int
    ko_length: int
    transformed_length: int


@dataclass(frozen=True)
class ParticleTransformReport:
    rows: int
    occurrences: int
    code3_rows: int
    choice_overlap_rows: int
    raw_ko_bytes: int
    transformed_bytes: int
    aggregate_shrink_bytes: int
    literal_counts: dict[str, int]
    transformed_corpus_sha256: str

    def to_dict(self) -> dict:
        return asdict(self)


def _fail(code: str, detail: str) -> None:
    raise SelectiveEventError(code, detail)


def _sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def _align4(value: int) -> int:
    return (value + 3) & ~3


def _rowset_sha256(rows: Sequence[ParticleLedgerRecord]) -> str:
    payload = bytearray()
    for row in rows:
        payload += struct.pack('<III', row.row_id, row.original_offset, row.ko_offset)
    return _sha256(bytes(payload))


def load_particle_ledger(blob: bytes, *, require_canonical: bool = True) -> tuple[ParticleLedgerRecord, ...]:
    if len(blob) % PARTICLE_LEDGER_RECORD.size:
        _fail('PARTICLE_LEDGER_SIZE_FAIL', f'bytes={len(blob)}')
    if require_canonical:
        if len(blob) != PARTICLE_LEDGER_RECORD_COUNT * PARTICLE_LEDGER_RECORD.size:
            _fail('PARTICLE_LEDGER_COUNT_FAIL', f'bytes={len(blob)}')
        actual_sha = _sha256(blob)
        if actual_sha != PARTICLE_LEDGER_SHA256:
            _fail('PARTICLE_LEDGER_SHA_FAIL', actual_sha)

    rows = tuple(ParticleLedgerRecord(*values) for values in PARTICLE_LEDGER_RECORD.iter_unpack(blob))
    if len({row.row_id for row in rows}) != len(rows):
        _fail('PARTICLE_LEDGER_ROW_ID_COLLISION', 'duplicate row_id')
    if len({(row.partition, row.original_offset) for row in rows}) != len(rows):
        _fail('PARTICLE_LEDGER_ORIGINAL_COLLISION', 'duplicate original binding')
    if len({row.ko_offset for row in rows}) != len(rows):
        _fail('PARTICLE_LEDGER_KO_COLLISION', 'duplicate KO binding')

    for row in rows:
        if row.opcode not in (0x11, 0x12, 0x13, 0x15):
            _fail('PARTICLE_LEDGER_OPCODE_FAIL', f'row={row.row_id} opcode={row.opcode:#x}')
        if row.semantic_code not in (SEMANTIC_INCLUDE_KO_CHOICE, SEMANTIC_INCLUDE_KO_FIXED_SURFACE_PARTICLE):
            _fail('PARTICLE_LEDGER_SEMANTIC_CODE_FAIL', f'row={row.row_id} code={row.semantic_code}')
        expected_choice = int(row.semantic_code == SEMANTIC_INCLUDE_KO_CHOICE)
        if row.choice_overlap != expected_choice:
            _fail('PARTICLE_LEDGER_CHOICE_FLAG_FAIL', f'row={row.row_id}')
        if row.occurrence_count < 1:
            _fail('PARTICLE_LEDGER_OCCURRENCE_FAIL', f'row={row.row_id}')
        if row.ko_length - row.transformed_length != 4 * row.occurrence_count:
            _fail('PARTICLE_LEDGER_LENGTH_DELTA_FAIL', f'row={row.row_id}')
        if row.ko_length % 4 or row.transformed_length % 4:
            _fail('PARTICLE_LEDGER_ALIGNMENT_FAIL', f'row={row.row_id}')

    if require_canonical:
        if _rowset_sha256(rows) != PARTICLE_ROWSET_SHA256:
            _fail('PARTICLE_LEDGER_ROWSET_SHA_FAIL', _rowset_sha256(rows))
        counts = Counter(row.semantic_code for row in rows)
        if counts != Counter({SEMANTIC_INCLUDE_KO_FIXED_SURFACE_PARTICLE: PARTICLE_CODE3_ROWS,
                              SEMANTIC_INCLUDE_KO_CHOICE: PARTICLE_CHOICE_OVERLAP_ROWS}):
            _fail('PARTICLE_LEDGER_SEMANTIC_COUNTS_FAIL', repr(dict(counts)))
        if sum(row.occurrence_count for row in rows) != PARTICLE_OCCURRENCES:
            _fail('PARTICLE_LEDGER_OCCURRENCE_TOTAL_FAIL', str(sum(row.occurrence_count for row in rows)))
        if sum(row.ko_length - row.transformed_length for row in rows) != PARTICLE_AGGREGATE_SHRINK:
            _fail('PARTICLE_LEDGER_SHRINK_TOTAL_FAIL', 'aggregate shrink mismatch')
    return rows


def _message_ranges(command: bytes) -> tuple[tuple[int, int], ...]:
    if len(command) < 4:
        _fail('PARTICLE_COMMAND_TRUNCATED', f'len={len(command)}')
    opcode = command[0]
    if opcode in (0x11, 0x12, 0x13):
        try:
            end = command.index(0, 4)
        except ValueError:
            _fail('PARTICLE_STRING_TERMINATOR_MISSING', f'opcode={opcode:#x}')
        return ((4, end),)
    if opcode == 0x15:
        choice_count = command[1]
        position = 4
        result: list[tuple[int, int]] = []
        for choice in range(choice_count):
            try:
                end = command.index(0, position)
            except ValueError:
                _fail('PARTICLE_CHOICE_TERMINATOR_MISSING', f'choice={choice}')
            result.append((position, end))
            position += _align4(end - position + 1)
            if position > len(command):
                _fail('PARTICLE_CHOICE_RANGE_FAIL', f'choice={choice}')
        return tuple(result)
    _fail('PARTICLE_COMMAND_OPCODE_FAIL', f'opcode={opcode:#x}')


def transform_particle_command(command: bytes) -> tuple[bytes, Counter[str]]:
    ranges = _message_ranges(command)
    occurrences: list[tuple[int, int, str, bytes]] = []
    for pattern, replacement, name in PARTICLE_REPLACEMENTS:
        for start, end in ranges:
            position = start
            while True:
                found = command.find(pattern, position, end)
                if found < 0:
                    break
                occurrences.append((found, found + len(pattern), name, replacement))
                position = found + 1
    occurrences.sort(key=lambda item: item[0])
    for left, right in zip(occurrences, occurrences[1:]):
        if left[1] > right[0]:
            _fail('PARTICLE_LITERAL_OVERLAP', f'{left[0]:#x}/{right[0]:#x}')
    if not occurrences:
        _fail('PARTICLE_LITERAL_MISSING', f'opcode={command[0]:#x}')

    by_start = {start: (end, name, replacement) for start, end, name, replacement in occurrences}
    output = bytearray()
    position = 0
    while position < len(command):
        entry = by_start.get(position)
        if entry is None:
            output.append(command[position])
            position += 1
            continue
        end, _name, replacement = entry
        output += replacement
        position = end
    transformed = bytes(output)
    counts = Counter(name for _start, _end, name, _replacement in occurrences)

    if transformed[:4] != command[:4]:
        _fail('PARTICLE_COMMAND_HEADER_MUTATED', command[:4].hex())
    if len(transformed) != len(command) - 4 * len(occurrences):
        _fail('PARTICLE_TRANSFORM_LENGTH_FAIL', f'before={len(command)} after={len(transformed)}')
    if len(transformed) % 4:
        _fail('PARTICLE_TRANSFORM_ALIGNMENT_FAIL', f'len={len(transformed)}')
    if len(_message_ranges(transformed)) != len(ranges):
        _fail('PARTICLE_STRING_COUNT_MUTATED', f'opcode={command[0]:#x}')
    for pattern, _replacement, name in PARTICLE_REPLACEMENTS:
        for start, end in _message_ranges(transformed):
            if transformed.find(pattern, start, end) >= 0:
                _fail('PARTICLE_LITERAL_REMAINS', name)
    return transformed, counts


def _index_grouped_items(parsed: ParsedEventTs5) -> dict[tuple[int, int], tuple[int, bytes]]:
    result: dict[tuple[int, int], tuple[int, bytes]] = {}
    for partition in parsed.partitions:
        for item_index, item in enumerate(partition.grouped_items):
            result[(partition.index, item.start)] = (item_index, item.data)
    return result


def apply_fixed_surface_particles(
    original: ParsedEventTs5,
    korean_blob: bytes,
    current_item_bytes: Sequence[Sequence[bytes]],
    ledger: Sequence[ParticleLedgerRecord],
    *,
    require_canonical: bool = True,
) -> tuple[tuple[tuple[bytes, ...], ...], ParticleTransformReport]:
    if len(current_item_bytes) != len(original.partitions):
        _fail('PARTICLE_PARTITION_COUNT_FAIL', f'current={len(current_item_bytes)} original={len(original.partitions)}')

    original_index = _index_grouped_items(original)
    if require_canonical:
        if len(korean_blob) != CANONICAL_PC_KO_SIZE:
            _fail('PARTICLE_KO_FILE_SIZE_FAIL', f'bytes={len(korean_blob)}')
        if _sha256(korean_blob) != CANONICAL_PC_KO_SHA256:
            _fail('PARTICLE_KO_FILE_SHA_FAIL', _sha256(korean_blob))
    current = [list(map(bytes, items)) for items in current_item_bytes]
    literal_counts: Counter[str] = Counter()
    transformed_hash = hashlib.sha256()
    raw_ko_bytes = 0
    transformed_bytes = 0
    code3_rows = 0
    choice_rows = 0

    for row in ledger:
        original_entry = original_index.get((row.partition, row.original_offset))
        if original_entry is None:
            _fail('PARTICLE_ORIGINAL_BINDING_MISSING', f'row={row.row_id} offset={row.original_offset:#x}')
        if row.ko_offset < 0 or row.ko_offset + row.ko_length > len(korean_blob):
            _fail('PARTICLE_KO_BINDING_RANGE_FAIL', f'row={row.row_id} offset={row.ko_offset:#x}')
        original_item_index, original_item = original_entry
        ko_item = korean_blob[row.ko_offset:row.ko_offset + row.ko_length]
        if original_item[0] != row.opcode or ko_item[0] != row.opcode:
            _fail('PARTICLE_OPCODE_BINDING_FAIL', f'row={row.row_id}')
        if len(ko_item) != row.ko_length:
            _fail('PARTICLE_KO_LENGTH_FAIL', f'row={row.row_id} got={len(ko_item)} expected={row.ko_length}')
        if original_item_index >= len(current[row.partition]):
            _fail('PARTICLE_CURRENT_ITEM_RANGE_FAIL', f'row={row.row_id}')

        before = current[row.partition][original_item_index]
        if row.semantic_code == SEMANTIC_INCLUDE_KO_FIXED_SURFACE_PARTICLE:
            code3_rows += 1
            if before != original_item:
                _fail('PARTICLE_CODE3_BASELINE_FAIL', f'row={row.row_id} offset={row.original_offset:#x}')
        elif row.semantic_code == SEMANTIC_INCLUDE_KO_CHOICE:
            choice_rows += 1
            if before != ko_item:
                _fail('PARTICLE_CHOICE_BASELINE_FAIL', f'row={row.row_id} offset={row.original_offset:#x}')
        else:  # guarded by ledger load, retained for noncanonical tests
            _fail('PARTICLE_SEMANTIC_CODE_FAIL', f'row={row.row_id}')

        transformed, counts = transform_particle_command(ko_item)
        if sum(counts.values()) != row.occurrence_count:
            _fail('PARTICLE_OCCURRENCE_BINDING_FAIL', f'row={row.row_id}')
        if len(transformed) != row.transformed_length:
            _fail('PARTICLE_TRANSFORMED_LENGTH_FAIL', f'row={row.row_id}')
        current[row.partition][original_item_index] = transformed
        literal_counts.update(counts)
        raw_ko_bytes += len(ko_item)
        transformed_bytes += len(transformed)
        transformed_hash.update(struct.pack('<IIIH', row.row_id, row.original_offset, row.ko_offset, len(transformed)))
        transformed_hash.update(hashlib.sha256(transformed).digest())

    report = ParticleTransformReport(
        rows=len(ledger),
        occurrences=sum(literal_counts.values()),
        code3_rows=code3_rows,
        choice_overlap_rows=choice_rows,
        raw_ko_bytes=raw_ko_bytes,
        transformed_bytes=transformed_bytes,
        aggregate_shrink_bytes=raw_ko_bytes - transformed_bytes,
        literal_counts=dict(sorted(literal_counts.items())),
        transformed_corpus_sha256=transformed_hash.hexdigest(),
    )

    if require_canonical:
        if report.rows != PARTICLE_LEDGER_RECORD_COUNT:
            _fail('PARTICLE_APPLY_ROW_COUNT_FAIL', str(report.rows))
        if report.occurrences != PARTICLE_OCCURRENCES:
            _fail('PARTICLE_APPLY_OCCURRENCE_COUNT_FAIL', str(report.occurrences))
        if report.code3_rows != PARTICLE_CODE3_ROWS or report.choice_overlap_rows != PARTICLE_CHOICE_OVERLAP_ROWS:
            _fail('PARTICLE_APPLY_SEMANTIC_COUNTS_FAIL', repr((report.code3_rows, report.choice_overlap_rows)))
        if report.aggregate_shrink_bytes != PARTICLE_AGGREGATE_SHRINK:
            _fail('PARTICLE_APPLY_SHRINK_FAIL', str(report.aggregate_shrink_bytes))
        if report.literal_counts != EXPECTED_LITERAL_COUNTS:
            _fail('PARTICLE_APPLY_LITERAL_COUNTS_FAIL', repr(report.literal_counts))
        if report.transformed_corpus_sha256 != PARTICLE_TRANSFORMED_CORPUS_SHA256:
            _fail('PARTICLE_TRANSFORMED_CORPUS_SHA_FAIL', report.transformed_corpus_sha256)

    return tuple(tuple(items) for items in current), report
