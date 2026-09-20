from __future__ import annotations

from collections import Counter, defaultdict
from dataclasses import asdict, dataclass
import hashlib
import json
import struct
from typing import Sequence

from builder.selective_event import ParsedEventTs5, SelectiveEventError

CANONICAL_PC_KO_SIZE = 1_156_480
CANONICAL_PC_KO_SHA256 = "0899bf81789acfbd243d43be209a8a3960933fa090960ac8c753c63f95f07bbe"
DIRECT_APPLICABILITY_ROWS = 350
DIRECT_OCCURRENCES = 386
DIRECT_SUBSTITUTIONS = 117
DIRECT_NORMALIZATION_ROWS = 108
DIRECT_PAYLOAD_GROWTH = 5_584
DIRECT_APP_SHA256 = "7f2d632d3ccdcf9244c40b82f8b82714d048203bce7e88d0de9a1df532257097"
DIRECT_OCC_SHA256 = "76593511a4886ad00f2bb57758e4fb86ef6378664163b8a700dda5f40b2d0575"
DIRECT_ROWSET_SHA256 = "295ba0bbed34d36bcca584646a08df42b3e61b38af0ea4c6f89880fecc2aad70"
DIRECT_TRANSFORMED_CORPUS_SHA256 = "01157230d52e5ae23ede0c03fc3eda5cc090540254b354e73d720fe5189980ee"
DIRECT_ALLOWED_OPCODES = frozenset((0x11, 0x12, 0x13))

PARTICLE_BYTES = {
    "은": bytes.fromhex("f359"),
    "는": bytes.fromhex("ed61"),
    "이": bytes.fromhex("f36b"),
    "가": bytes.fromhex("eb40"),
    "을": bytes.fromhex("f35a"),
    "를": bytes.fromhex("ef45"),
    "과": bytes.fromhex("eb9a"),
    "와": bytes.fromhex("f2cb"),
    "로": bytes.fromhex("eecc"),
}
TARGET_PARTICLE = {
    "은": "는", "는": "는",
    "이": "가", "가": "가",
    "을": "를", "를": "를",
    "과": "와", "와": "와",
    "로": "로",
}
EXPECTED_SOURCE_COUNTS = {
    "가": 104, "과": 9, "는": 81, "로": 10, "를": 47,
    "와": 27, "은": 50, "을": 13, "이": 45,
}
EXPECTED_TARGET_COUNTS = {"가": 149, "는": 131, "로": 10, "를": 60, "와": 36}
EXPECTED_SUBSTITUTION_COUNTS = {"과->와": 9, "은->는": 50, "을->를": 13, "이->가": 45}


@dataclass(frozen=True)
class DirectApplicabilityRecord:
    row_id: int
    partition: int
    original_offset: int
    ko_offset: int
    opcode: int
    original_command_length: int
    ko_command_length: int
    direct_occurrences: int
    normalization_occurrences: int


@dataclass(frozen=True)
class DirectOccurrenceRecord:
    row_id: int
    partition: int
    original_offset: int
    ko_offset: int
    opcode: int
    hit_index: int
    field_index: int
    decoded_char_offset: int
    escape: str
    source_particle: str
    target_particle: str
    source_particle_bytes: bytes
    target_particle_bytes: bytes
    substitute: bool


@dataclass(frozen=True)
class DirectEscapeParticleReport:
    rows: int
    occurrences: int
    substitutions: int
    normalization_candidate_rows: int
    raw_ko_bytes: int
    transformed_bytes: int
    payload_growth_vs_original: int
    source_counts: dict[str, int]
    target_counts: dict[str, int]
    substitution_counts: dict[str, int]
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
        text = blob.decode("utf-8")
    except UnicodeDecodeError as exc:
        _fail(code, f"utf8:{exc}")
    rows: list[dict] = []
    for line_no, line in enumerate(text.splitlines(), 1):
        if not line:
            continue
        try:
            value = json.loads(line)
        except json.JSONDecodeError as exc:
            _fail(code, f"line={line_no} json:{exc}")
        if not isinstance(value, dict):
            _fail(code, f"line={line_no} not-object")
        rows.append(value)
    return rows


def _int_field(obj: dict, name: str, code: str) -> int:
    value = obj.get(name)
    if not isinstance(value, int) or isinstance(value, bool):
        _fail(code, f"{name}={value!r}")
    return value


def load_direct_escape_ledgers(
    applicability_blob: bytes,
    occurrences_blob: bytes,
    *,
    require_canonical: bool = True,
) -> tuple[tuple[DirectApplicabilityRecord, ...], tuple[DirectOccurrenceRecord, ...]]:
    if require_canonical:
        if _sha256(applicability_blob) != DIRECT_APP_SHA256:
            _fail("DIRECT_APP_SHA_FAIL", _sha256(applicability_blob))
        if _sha256(occurrences_blob) != DIRECT_OCC_SHA256:
            _fail("DIRECT_OCC_SHA_FAIL", _sha256(occurrences_blob))

    app_values = _jsonl(applicability_blob, "DIRECT_APP_JSON_FAIL")
    occ_values = _jsonl(occurrences_blob, "DIRECT_OCC_JSON_FAIL")

    applicability: list[DirectApplicabilityRecord] = []
    for obj in app_values:
        if obj.get("class") != "DIRECT_PARTICLE_ONLY":
            _fail("DIRECT_APP_CLASS_FAIL", repr(obj.get("class")))
        row = DirectApplicabilityRecord(
            row_id=_int_field(obj, "row_id", "DIRECT_APP_FIELD_FAIL"),
            partition=_int_field(obj, "partition", "DIRECT_APP_FIELD_FAIL"),
            original_offset=_int_field(obj, "original_offset", "DIRECT_APP_FIELD_FAIL"),
            ko_offset=_int_field(obj, "ko_offset", "DIRECT_APP_FIELD_FAIL"),
            opcode=_int_field(obj, "opcode", "DIRECT_APP_FIELD_FAIL"),
            original_command_length=_int_field(obj, "original_command_length", "DIRECT_APP_FIELD_FAIL"),
            ko_command_length=_int_field(obj, "ko_command_length", "DIRECT_APP_FIELD_FAIL"),
            direct_occurrences=_int_field(obj, "direct_occurrences", "DIRECT_APP_FIELD_FAIL"),
            normalization_occurrences=_int_field(obj, "normalization_occurrences", "DIRECT_APP_FIELD_FAIL"),
        )
        if row.opcode not in DIRECT_ALLOWED_OPCODES:
            _fail("DIRECT_APP_OPCODE_FAIL", f"row={row.row_id} opcode={row.opcode:#x}")
        if row.original_command_length <= 0 or row.ko_command_length <= 0:
            _fail("DIRECT_APP_LENGTH_FAIL", f"row={row.row_id}")
        if row.ko_command_length % 4 or row.original_command_length % 4:
            _fail("DIRECT_APP_ALIGNMENT_FAIL", f"row={row.row_id}")
        if row.direct_occurrences < 1 or not 0 <= row.normalization_occurrences <= row.direct_occurrences:
            _fail("DIRECT_APP_OCCURRENCE_COUNT_FAIL", f"row={row.row_id}")
        applicability.append(row)

    occurrences: list[DirectOccurrenceRecord] = []
    for obj in occ_values:
        source = obj.get("source_particle")
        target = obj.get("target_particle")
        if source not in TARGET_PARTICLE or target != TARGET_PARTICLE[source]:
            _fail("DIRECT_OCC_PARTICLE_PAIR_FAIL", f"source={source!r} target={target!r}")
        source_hex = obj.get("source_particle_bytes_hex")
        target_hex = obj.get("target_particle_bytes_hex")
        if not isinstance(source_hex, str) or not isinstance(target_hex, str):
            _fail("DIRECT_OCC_BYTE_FIELD_FAIL", repr((source_hex, target_hex)))
        try:
            source_bytes = bytes.fromhex(source_hex)
            target_bytes = bytes.fromhex(target_hex)
        except ValueError as exc:
            _fail("DIRECT_OCC_BYTE_FIELD_FAIL", repr(exc))
        if source_bytes != PARTICLE_BYTES[source] or target_bytes != PARTICLE_BYTES[target]:
            _fail("DIRECT_OCC_BYTE_MISMATCH", f"source={source!r} target={target!r}")
        escape = obj.get("escape")
        if not isinstance(escape, str) or not escape.startswith("\\"):
            _fail("DIRECT_OCC_ESCAPE_FAIL", repr(escape))
        try:
            escape.encode("ascii")
        except UnicodeEncodeError:
            _fail("DIRECT_OCC_ESCAPE_FAIL", repr(escape))
        substitute = obj.get("substitute")
        if not isinstance(substitute, bool) or substitute != (source != target):
            _fail("DIRECT_OCC_SUBSTITUTE_FLAG_FAIL", f"row={obj.get('row_id')}")
        occurrence = DirectOccurrenceRecord(
            row_id=_int_field(obj, "row_id", "DIRECT_OCC_FIELD_FAIL"),
            partition=_int_field(obj, "partition", "DIRECT_OCC_FIELD_FAIL"),
            original_offset=_int_field(obj, "original_offset", "DIRECT_OCC_FIELD_FAIL"),
            ko_offset=_int_field(obj, "ko_offset", "DIRECT_OCC_FIELD_FAIL"),
            opcode=_int_field(obj, "opcode", "DIRECT_OCC_FIELD_FAIL"),
            hit_index=_int_field(obj, "hit_index", "DIRECT_OCC_FIELD_FAIL"),
            field_index=_int_field(obj, "field_index", "DIRECT_OCC_FIELD_FAIL"),
            decoded_char_offset=_int_field(obj, "decoded_char_offset", "DIRECT_OCC_FIELD_FAIL"),
            escape=escape,
            source_particle=source,
            target_particle=target,
            source_particle_bytes=source_bytes,
            target_particle_bytes=target_bytes,
            substitute=substitute,
        )
        if occurrence.hit_index < 0 or occurrence.field_index < 0 or occurrence.decoded_char_offset < 0:
            _fail("DIRECT_OCC_NEGATIVE_LOCATOR", f"row={occurrence.row_id}")
        occurrences.append(occurrence)

    app_by_id = {row.row_id: row for row in applicability}
    if len(app_by_id) != len(applicability):
        _fail("DIRECT_APP_ROW_COLLISION", "duplicate row_id")
    if len({(r.partition, r.original_offset) for r in applicability}) != len(applicability):
        _fail("DIRECT_APP_ORIGINAL_COLLISION", "duplicate original binding")
    if len({r.ko_offset for r in applicability}) != len(applicability):
        _fail("DIRECT_APP_KO_COLLISION", "duplicate KO binding")

    grouped: dict[int, list[DirectOccurrenceRecord]] = defaultdict(list)
    for occurrence in occurrences:
        if occurrence.row_id not in app_by_id:
            _fail("DIRECT_OCC_ORPHAN_ROW", str(occurrence.row_id))
        grouped[occurrence.row_id].append(occurrence)

    for row in applicability:
        xs = sorted(grouped.get(row.row_id, ()), key=lambda x: x.hit_index)
        if [x.hit_index for x in xs] != list(range(row.direct_occurrences)):
            _fail("DIRECT_OCC_HIT_INDEX_FAIL", f"row={row.row_id}")
        if len(xs) != row.direct_occurrences:
            _fail("DIRECT_OCC_ROW_COUNT_FAIL", f"row={row.row_id}")
        for occurrence in xs:
            if (occurrence.partition, occurrence.original_offset, occurrence.ko_offset, occurrence.opcode) != (
                row.partition, row.original_offset, row.ko_offset, row.opcode
            ):
                _fail("DIRECT_OCC_ROW_BINDING_FAIL", f"row={row.row_id} hit={occurrence.hit_index}")
        for left, right in zip(xs, xs[1:]):
            if left.field_index == right.field_index and left.decoded_char_offset >= right.decoded_char_offset:
                _fail("DIRECT_OCC_DECODED_ORDER_FAIL", f"row={row.row_id}")
        if sum(x.substitute for x in xs) != row.normalization_occurrences:
            _fail("DIRECT_OCC_NORMALIZATION_COUNT_FAIL", f"row={row.row_id}")

    rowset = b"".join(
        struct.pack("<III", row.row_id, row.original_offset, row.ko_offset)
        for row in applicability
    )
    source_counts = Counter(x.source_particle for x in occurrences)
    target_counts = Counter(x.target_particle for x in occurrences)
    substitution_counts = Counter(
        f"{x.source_particle}->{x.target_particle}" for x in occurrences if x.substitute
    )

    if require_canonical:
        if len(applicability) != DIRECT_APPLICABILITY_ROWS:
            _fail("DIRECT_APP_CANONICAL_COUNT_FAIL", str(len(applicability)))
        if len(occurrences) != DIRECT_OCCURRENCES:
            _fail("DIRECT_OCC_CANONICAL_COUNT_FAIL", str(len(occurrences)))
        if sum(x.substitute for x in occurrences) != DIRECT_SUBSTITUTIONS:
            _fail("DIRECT_SUBSTITUTION_TOTAL_FAIL", str(sum(x.substitute for x in occurrences)))
        if sum(row.normalization_occurrences > 0 for row in applicability) != DIRECT_NORMALIZATION_ROWS:
            _fail("DIRECT_NORMALIZATION_ROW_TOTAL_FAIL", "row total mismatch")
        if dict(sorted(source_counts.items())) != EXPECTED_SOURCE_COUNTS:
            _fail("DIRECT_SOURCE_COUNTS_FAIL", repr(dict(source_counts)))
        if dict(sorted(target_counts.items())) != EXPECTED_TARGET_COUNTS:
            _fail("DIRECT_TARGET_COUNTS_FAIL", repr(dict(target_counts)))
        if dict(sorted(substitution_counts.items())) != EXPECTED_SUBSTITUTION_COUNTS:
            _fail("DIRECT_SUBSTITUTION_COUNTS_FAIL", repr(dict(substitution_counts)))
        if _sha256(rowset) != DIRECT_ROWSET_SHA256:
            _fail("DIRECT_ROWSET_SHA_FAIL", _sha256(rowset))
        if sum(row.ko_command_length - row.original_command_length for row in applicability) != DIRECT_PAYLOAD_GROWTH:
            _fail("DIRECT_PAYLOAD_GROWTH_FAIL", "aggregate growth mismatch")

    return tuple(applicability), tuple(occurrences)


def _message_ranges(command: bytes) -> tuple[tuple[int, int], ...]:
    if len(command) < 4 or command[0] not in DIRECT_ALLOWED_OPCODES:
        _fail("DIRECT_COMMAND_OPCODE_FAIL", command[:4].hex())
    try:
        end = command.index(0, 4)
    except ValueError:
        _fail("DIRECT_STRING_TERMINATOR_MISSING", f"opcode={command[0]:#x}")
    if any(command[end + 1:]):
        _fail("DIRECT_COMMAND_TRAILING_BYTES_FAIL", f"opcode={command[0]:#x}")
    return ((4, end),)


def transform_direct_escape_command(
    command: bytes,
    occurrences: Sequence[DirectOccurrenceRecord],
) -> tuple[bytes, Counter[str], Counter[str]]:
    ranges = _message_ranges(command)
    ordered = sorted(occurrences, key=lambda x: (x.field_index, x.decoded_char_offset, x.hit_index))
    if not ordered:
        _fail("DIRECT_OCCURRENCES_MISSING", f"opcode={command[0]:#x}")

    # Bind every expected exact needle to its full candidate set before mutation.
    candidates: dict[tuple[int, bytes], tuple[int, ...]] = {}
    expected_multiplicity: Counter[tuple[int, bytes]] = Counter()
    for occurrence in ordered:
        if occurrence.field_index >= len(ranges):
            _fail("DIRECT_FIELD_INDEX_FAIL", f"row={occurrence.row_id} field={occurrence.field_index}")
        needle = occurrence.escape.encode("ascii") + occurrence.source_particle_bytes
        expected_multiplicity[(occurrence.field_index, needle)] += 1

    for key, expected in expected_multiplicity.items():
        field_index, needle = key
        start, end = ranges[field_index]
        found: list[int] = []
        position = start
        while True:
            offset = command.find(needle, position, end)
            if offset < 0:
                break
            found.append(offset)
            position = offset + 1
        if len(found) != expected:
            _fail(
                "DIRECT_RAW_NEEDLE_MULTIPLICITY_FAIL",
                f"field={field_index} needle={needle.hex()} found={len(found)} expected={expected}",
            )
        candidates[key] = tuple(found)

    ordinals: Counter[tuple[int, bytes]] = Counter()
    edits: list[tuple[int, DirectOccurrenceRecord]] = []
    last_position_by_field: dict[int, int] = {}
    for occurrence in ordered:
        needle = occurrence.escape.encode("ascii") + occurrence.source_particle_bytes
        key = (occurrence.field_index, needle)
        ordinal = ordinals[key]
        ordinals[key] += 1
        start = candidates[key][ordinal]
        prior = last_position_by_field.get(occurrence.field_index, -1)
        if start <= prior:
            _fail("DIRECT_OCCURRENCE_ORDER_FAIL", f"row={occurrence.row_id} hit={occurrence.hit_index}")
        last_position_by_field[occurrence.field_index] = start
        particle_position = start + len(occurrence.escape)
        if command[particle_position:particle_position + 2] != occurrence.source_particle_bytes:
            _fail("DIRECT_SOURCE_BYTES_FAIL", f"row={occurrence.row_id} hit={occurrence.hit_index}")
        edits.append((particle_position, occurrence))

    if len({position for position, _ in edits}) != len(edits):
        _fail("DIRECT_EDIT_COLLISION", "duplicate particle byte position")

    output = bytearray(command)
    source_counts: Counter[str] = Counter()
    target_counts: Counter[str] = Counter()
    for position, occurrence in edits:
        output[position:position + 2] = occurrence.target_particle_bytes
        source_counts[occurrence.source_particle] += 1
        target_counts[occurrence.target_particle] += 1

    transformed = bytes(output)
    if len(transformed) != len(command):
        _fail("DIRECT_TRANSFORM_LENGTH_FAIL", f"before={len(command)} after={len(transformed)}")
    if transformed[:4] != command[:4]:
        _fail("DIRECT_COMMAND_HEADER_MUTATED", command[:4].hex())
    if len(_message_ranges(transformed)) != len(ranges):
        _fail("DIRECT_STRING_COUNT_MUTATED", f"opcode={command[0]:#x}")
    return transformed, source_counts, target_counts


def _index_grouped_items(parsed: ParsedEventTs5) -> dict[tuple[int, int], tuple[int, bytes]]:
    result: dict[tuple[int, int], tuple[int, bytes]] = {}
    for partition in parsed.partitions:
        for item_index, item in enumerate(partition.grouped_items):
            result[(partition.index, item.start)] = (item_index, item.data)
    return result


def apply_direct_escape_particles(
    original: ParsedEventTs5,
    korean_blob: bytes,
    current_item_bytes: Sequence[Sequence[bytes]],
    applicability: Sequence[DirectApplicabilityRecord],
    occurrences: Sequence[DirectOccurrenceRecord],
    *,
    require_canonical: bool = True,
) -> tuple[tuple[tuple[bytes, ...], ...], DirectEscapeParticleReport]:
    if len(current_item_bytes) != len(original.partitions):
        _fail("DIRECT_PARTITION_COUNT_FAIL", f"current={len(current_item_bytes)} original={len(original.partitions)}")
    if require_canonical:
        if len(korean_blob) != CANONICAL_PC_KO_SIZE:
            _fail("DIRECT_KO_FILE_SIZE_FAIL", f"bytes={len(korean_blob)}")
        if _sha256(korean_blob) != CANONICAL_PC_KO_SHA256:
            _fail("DIRECT_KO_FILE_SHA_FAIL", _sha256(korean_blob))

    original_index = _index_grouped_items(original)
    current = [list(map(bytes, part)) for part in current_item_bytes]
    occ_by_row: dict[int, list[DirectOccurrenceRecord]] = defaultdict(list)
    for occurrence in occurrences:
        occ_by_row[occurrence.row_id].append(occurrence)

    source_counts: Counter[str] = Counter()
    target_counts: Counter[str] = Counter()
    substitution_counts: Counter[str] = Counter()
    raw_ko_bytes = 0
    transformed_bytes = 0
    transformed_hash = hashlib.sha256()
    normalization_rows = 0

    for row in applicability:
        binding = original_index.get((row.partition, row.original_offset))
        if binding is None:
            _fail("DIRECT_ORIGINAL_BINDING_MISSING", f"row={row.row_id} offset={row.original_offset:#x}")
        item_index, original_item = binding
        if item_index >= len(current[row.partition]):
            _fail("DIRECT_CURRENT_ITEM_RANGE_FAIL", f"row={row.row_id}")
        if len(original_item) != row.original_command_length or original_item[0] != row.opcode:
            _fail("DIRECT_ORIGINAL_BINDING_FAIL", f"row={row.row_id}")
        if row.ko_offset < 0 or row.ko_offset + row.ko_command_length > len(korean_blob):
            _fail("DIRECT_KO_BINDING_RANGE_FAIL", f"row={row.row_id} offset={row.ko_offset:#x}")
        ko_item = korean_blob[row.ko_offset:row.ko_offset + row.ko_command_length]
        if len(ko_item) != row.ko_command_length or not ko_item or ko_item[0] != row.opcode:
            _fail("DIRECT_KO_BINDING_FAIL", f"row={row.row_id}")
        if current[row.partition][item_index] != original_item:
            _fail("DIRECT_BASELINE_FAIL", f"row={row.row_id} offset={row.original_offset:#x}")

        row_occurrences = sorted(occ_by_row.get(row.row_id, ()), key=lambda x: x.hit_index)
        if len(row_occurrences) != row.direct_occurrences:
            _fail("DIRECT_OCCURRENCE_BINDING_FAIL", f"row={row.row_id}")
        transformed, row_source, row_target = transform_direct_escape_command(ko_item, row_occurrences)
        if len(transformed) != row.ko_command_length:
            _fail("DIRECT_TRANSFORMED_LENGTH_FAIL", f"row={row.row_id}")

        current[row.partition][item_index] = transformed
        source_counts.update(row_source)
        target_counts.update(row_target)
        for occurrence in row_occurrences:
            if occurrence.substitute:
                substitution_counts[f"{occurrence.source_particle}->{occurrence.target_particle}"] += 1
        if row.normalization_occurrences:
            normalization_rows += 1
        raw_ko_bytes += len(ko_item)
        transformed_bytes += len(transformed)
        transformed_hash.update(struct.pack("<IIIH", row.row_id, row.original_offset, row.ko_offset, len(transformed)))
        transformed_hash.update(hashlib.sha256(transformed).digest())

    rowset = b"".join(
        struct.pack("<III", row.row_id, row.original_offset, row.ko_offset)
        for row in applicability
    )
    report = DirectEscapeParticleReport(
        rows=len(applicability),
        occurrences=sum(source_counts.values()),
        substitutions=sum(substitution_counts.values()),
        normalization_candidate_rows=normalization_rows,
        raw_ko_bytes=raw_ko_bytes,
        transformed_bytes=transformed_bytes,
        payload_growth_vs_original=sum(row.ko_command_length - row.original_command_length for row in applicability),
        source_counts=dict(sorted(source_counts.items())),
        target_counts=dict(sorted(target_counts.items())),
        substitution_counts=dict(sorted(substitution_counts.items())),
        transformed_corpus_sha256=transformed_hash.hexdigest(),
        rowset_sha256=_sha256(rowset),
    )

    if require_canonical:
        expected = {
            "rows": DIRECT_APPLICABILITY_ROWS,
            "occurrences": DIRECT_OCCURRENCES,
            "substitutions": DIRECT_SUBSTITUTIONS,
            "normalization_candidate_rows": DIRECT_NORMALIZATION_ROWS,
            "payload_growth_vs_original": DIRECT_PAYLOAD_GROWTH,
            "source_counts": EXPECTED_SOURCE_COUNTS,
            "target_counts": EXPECTED_TARGET_COUNTS,
            "substitution_counts": EXPECTED_SUBSTITUTION_COUNTS,
            "transformed_corpus_sha256": DIRECT_TRANSFORMED_CORPUS_SHA256,
            "rowset_sha256": DIRECT_ROWSET_SHA256,
        }
        for field, value in expected.items():
            actual = getattr(report, field)
            if actual != value:
                _fail("DIRECT_CANONICAL_REPORT_FAIL", f"{field}={actual!r} expected={value!r}")
        if report.raw_ko_bytes != report.transformed_bytes:
            _fail("DIRECT_PARTICLE_DELTA_FAIL", f"raw={report.raw_ko_bytes} transformed={report.transformed_bytes}")

    return tuple(tuple(part) for part in current), report
