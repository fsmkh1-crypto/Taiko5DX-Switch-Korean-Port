from __future__ import annotations

from collections import Counter, defaultdict
from dataclasses import asdict, dataclass
import hashlib
import struct
from typing import Sequence

from builder.selective_event import (
    ParsedEventTs5,
    SelectiveEventError,
    STOCK_SHA256,
    STOCK_SIZE,
    analyze_generic_branch_plans,
    analyze_switch_special_span_plans,
    repair_generic_branch_items,
    repair_switch_special_span_items,
    rebuild_event_ts5,
)

PC_KO_SIZE = 1_156_480
PC_KO_SHA256 = "0899bf81789acfbd243d43be209a8a3960933fa090960ac8c753c63f95f07bbe"
FIVEA_MAPPING_RECORD = struct.Struct("<HHIIHH")
FIVEA_MAPPING_RECORD_COUNT = 1_088
FIVEA_MAPPING_SHA256 = "6aafe3b284e3ec65a7f2928334bffa9a81b15b54d47c85928484a3b59058c97e"
FIVEA_MAPPING_ROWSET_SHA256 = "255a1b40ad776ac55f3d034f64075782c4e51f51227747180237df134694a774"
EXPECTED_TRANSLATED = 1_074
EXPECTED_NAME_ONLY = 14
EXPECTED_ORIGINAL_TARGET = 1_058
EXPECTED_CHOICE_NEXT_START = 15
EXPECTED_ZERO_NEXT_TERMINATOR = 1
EXPECTED_MODIFIED = 82
EXPECTED_MODIFIED_ROWSET_SHA256 = "26bc49d7a19cafa2e75aed11be2fa2f3874442b07cb55db92f1e7f7dd2b3d016"
EXPECTED_DIALOGUE_PAD_ROWSET_SHA256 = "00bef7fff43008f41014f358611d890c6ac4e7857502c026f2afc6bc6c47eead"
EXPECTED_CHOICE_ROWSET_SHA256 = "0579d61f80c791e041c056e9a83fce785e5af8b1edf101a91a910b63dd8d0446"
EXPECTED_ZERO_ROWSET_SHA256 = "538065cd4a3886366d236e574bd9010306867409e4bd7b698ae9b40d5a7ae9eb"


@dataclass(frozen=True)
class FiveAMappingRecord:
    partition: int
    ordinal: int
    original_offset: int
    ko_offset: int
    original_length: int
    ko_length: int


@dataclass(frozen=True)
class FiveAResolution:
    partition: int
    item_index: int
    original_offset: int
    ko_offset: int
    kind: str
    name2_spaces: int
    dialogue_spaces: int


@dataclass(frozen=True)
class FiveACompositeReport:
    mapping_rows: int
    translated_rows: int
    name_only_preserved_rows: int
    original_target_rows: int
    choice_next_start_rows: int
    zero_next_terminator_rows: int
    unmodified_translated_rows: int
    dialogue_pad_1_rows: int
    dialogue_pad_2_rows: int
    dialogue_pad_3_rows: int
    name2_pad_2_rows: int
    modified_rows: int
    modified_rowset_sha256: str
    dialogue_pad_rowset_sha256: str
    choice_rowset_sha256: str
    zero_rowset_sha256: str
    verification_violations: int

    def to_dict(self) -> dict:
        return asdict(self)


def _fail(code: str, detail: str) -> None:
    raise SelectiveEventError(code, detail)


def _sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def _align4(value: int) -> int:
    return (value + 3) & ~3


def load_fivea_mapping(blob: bytes, *, require_canonical: bool = True) -> tuple[FiveAMappingRecord, ...]:
    if len(blob) % FIVEA_MAPPING_RECORD.size:
        _fail("FIVEA_MAPPING_SIZE_FAIL", f"bytes={len(blob)}")
    if require_canonical:
        if len(blob) != FIVEA_MAPPING_RECORD_COUNT * FIVEA_MAPPING_RECORD.size:
            _fail("FIVEA_MAPPING_COUNT_FAIL", f"bytes={len(blob)}")
        actual = _sha256(blob)
        if actual != FIVEA_MAPPING_SHA256:
            _fail("FIVEA_MAPPING_SHA_FAIL", f"sha256={actual}")

    rows = tuple(FiveAMappingRecord(*values) for values in FIVEA_MAPPING_RECORD.iter_unpack(blob))
    if require_canonical and len(rows) != FIVEA_MAPPING_RECORD_COUNT:
        _fail("FIVEA_MAPPING_COUNT_FAIL", f"rows={len(rows)}")
    if len({row.original_offset for row in rows}) != len(rows):
        _fail("FIVEA_MAPPING_ORIGINAL_COLLISION", "duplicate original offset")
    if len({row.ko_offset for row in rows}) != len(rows):
        _fail("FIVEA_MAPPING_KO_COLLISION", "duplicate KO offset")
    rowset = b"".join(struct.pack("<II", row.partition, row.original_offset) for row in rows)
    if require_canonical and _sha256(rowset) != FIVEA_MAPPING_ROWSET_SHA256:
        _fail("FIVEA_MAPPING_ROWSET_SHA_FAIL", _sha256(rowset))
    return rows


def _split_field(data: bytes, position: int) -> tuple[bytes, bytes, int]:
    try:
        end = data.index(0, position)
    except ValueError:
        _fail("FIVEA_FIELD_TERMINATOR_MISSING", f"position={position}")
    stop = position + _align4(end - position + 1)
    if stop > len(data):
        _fail("FIVEA_FIELD_ALIGNMENT_FAIL", f"stop={stop} len={len(data)}")
    return data[position:end], data[position:stop], stop


def split_fivea_fields(data: bytes) -> tuple[tuple[bytes, bytes], tuple[bytes, bytes], tuple[bytes, bytes]]:
    if len(data) < 16 or data[0] != 0x5A or len(data) % 4:
        _fail("FIVEA_ITEM_FORMAT_FAIL", f"len={len(data)} head={data[:4].hex()}")
    pos = 4
    result = []
    for _ in range(3):
        visible, encoded, pos = _split_field(data, pos)
        result.append((visible, encoded))
    if pos != len(data):
        _fail("FIVEA_ITEM_TRAILING_BYTES", f"parsed={pos} len={len(data)}")
    return tuple(result)  # type: ignore[return-value]


def _encode_field(visible: bytes, spaces: int) -> bytes:
    if spaces < 0:
        _fail("FIVEA_NEGATIVE_PADDING", str(spaces))
    raw = visible + (b" " * spaces) + b"\x00"
    return raw + b"\x00" * ((-len(raw)) % 4)


def compose_fivea(
    original_data: bytes,
    ko_data: bytes,
    *,
    name2_spaces: int = 0,
    dialogue_spaces: int = 0,
) -> bytes:
    original = split_fivea_fields(original_data)
    ko = split_fivea_fields(ko_data)
    if original_data[:4] != ko_data[:4]:
        _fail(
            "FIVEA_HEADER_MISMATCH",
            f"original={original_data[:4].hex()} ko={ko_data[:4].hex()}",
        )
    name1 = original[0][1]
    name2 = original[1][1] if name2_spaces == 0 else _encode_field(original[1][0], name2_spaces)
    dialogue = ko[2][1] if dialogue_spaces == 0 else _encode_field(ko[2][0], dialogue_spaces)
    result = original_data[:4] + name1 + name2 + dialogue
    if len(result) % 4:
        _fail("FIVEA_COMPOSITE_ALIGNMENT_FAIL", f"len={len(result)}")
    return result


def switch_fivea_runtime_length(data: bytes, position: int = 0) -> int:
    if position < 0 or position + 4 > len(data) or data[position] != 0x5A:
        _fail("FIVEA_RUNTIME_HEADER_FAIL", f"position={position}")
    p0 = position
    x24 = position + 4
    try:
        end1 = data.index(0, x24) + 1
        rel1 = _align4(end1 - p0 - 1)
        x25 = x24 + rel1
        end2 = data.index(0, x25) + 1
        rel2 = _align4(end2 - p0 - 1)
        x23 = x24 + rel2
        w26 = x23 - x24
        end3 = data.index(0, x23)
    except ValueError:
        _fail("FIVEA_RUNTIME_TERMINATOR_MISSING", f"position={position}")
    n3 = end3 - x23
    a3 = (n3 + 4) & ~3
    return w26 + a3 + 4


def _find_exact_item(items, offset: int, expected_length: int, opcode: int = 0x5A) -> int:
    for index, item in enumerate(items):
        if item.start == offset:
            if item.opcode != opcode:
                _fail("FIVEA_MAPPING_OPCODE_FAIL", f"offset={offset:#x} opcode={item.opcode:#x}")
            if len(item.data) != expected_length:
                _fail(
                    "FIVEA_MAPPING_LENGTH_FAIL",
                    f"offset={offset:#x} len={len(item.data)} expected={expected_length}",
                )
            return index
    _fail("FIVEA_MAPPING_ITEM_NOT_FOUND", f"offset={offset:#x}")


def _find_target_anchor(items, target: int) -> tuple[int, int]:
    for index, item in enumerate(items):
        if target == item.start:
            return index, 0
        end = item.start + len(item.data)
        if item.start < target < end:
            return index, target - item.start
        if target == end:
            return index + 1, 0
    _fail("FIVEA_TARGET_ANCHOR_NOT_FOUND", f"target={target:#x}")


def _rowset_hash(resolutions: Sequence[FiveAResolution]) -> str:
    blob = b"".join(
        struct.pack("<II", row.partition, row.original_offset)
        for row in sorted(resolutions, key=lambda row: (row.partition, row.original_offset))
    )
    return _sha256(blob)


def _structure_repairer(original: ParsedEventTs5):
    generic = {
        partition.index: analyze_generic_branch_plans(partition.grouped_items)
        for partition in original.partitions
    }
    special_by_partition = defaultdict(list)
    for plan in analyze_switch_special_span_plans(original):
        special_by_partition[plan.partition_index].append(plan)

    def repair(partition_index: int, current: Sequence[bytes]) -> tuple[bytes, ...]:
        partition = original.partitions[partition_index]
        repaired = repair_generic_branch_items(
            partition.grouped_items,
            current,
            plans=generic[partition_index],
        )
        return repair_switch_special_span_items(
            partition.grouped_items,
            repaired,
            special_by_partition.get(partition_index, ()),
        )

    return repair


def solve_fivea_composites(
    original: ParsedEventTs5,
    pc_ko: ParsedEventTs5,
    current_item_bytes: Sequence[Sequence[bytes]],
    mapping: Sequence[FiveAMappingRecord],
    *,
    require_canonical_counts: bool = True,
    structure_repair=None,
) -> tuple[tuple[tuple[bytes, ...], ...], FiveACompositeReport, tuple[FiveAResolution, ...]]:
    if len(original.partitions) != len(pc_ko.partitions) or len(current_item_bytes) != len(original.partitions):
        _fail("FIVEA_PARTITION_COUNT_FAIL", "partition count mismatch")
    if require_canonical_counts:
        original_blob = rebuild_event_ts5(original)
        ko_blob = rebuild_event_ts5(pc_ko)
        if len(original_blob) != STOCK_SIZE or _sha256(original_blob) != STOCK_SHA256:
            _fail("FIVEA_ORIGINAL_IDENTITY_FAIL", f"size={len(original_blob)} sha256={_sha256(original_blob)}")
        if len(ko_blob) != PC_KO_SIZE or _sha256(ko_blob) != PC_KO_SHA256:
            _fail("FIVEA_PC_KO_IDENTITY_FAIL", f"size={len(ko_blob)} sha256={_sha256(ko_blob)}")

    repair_structure = _structure_repairer(original) if structure_repair is None else structure_repair
    current = [list(map(bytes, items)) for items in current_item_bytes]
    metadata_by_partition = defaultdict(dict)
    translated = []
    name_only = []

    for record in mapping:
        if record.partition >= len(original.partitions):
            _fail("FIVEA_MAPPING_PARTITION_FAIL", str(record.partition))
        opart = original.partitions[record.partition]
        kpart = pc_ko.partitions[record.partition]
        if len(current[record.partition]) != len(opart.grouped_items):
            _fail("FIVEA_CURRENT_ITEM_COUNT_FAIL", f"partition={record.partition}")
        oidx = _find_exact_item(opart.grouped_items, record.original_offset, record.original_length)
        kidx = _find_exact_item(kpart.grouped_items, record.ko_offset, record.ko_length)
        original_fivea_ordinal = sum(item.opcode == 0x5A for item in opart.grouped_items[:oidx])
        ko_fivea_ordinal = sum(item.opcode == 0x5A for item in kpart.grouped_items[:kidx])
        if original_fivea_ordinal != record.ordinal or ko_fivea_ordinal != record.ordinal:
            _fail(
                "FIVEA_MAPPING_ORDINAL_FAIL",
                f"partition={record.partition} expected={record.ordinal} original={original_fivea_ordinal} ko={ko_fivea_ordinal}",
            )
        oitem = opart.grouped_items[oidx]
        kitem = kpart.grouped_items[kidx]
        ofields = split_fivea_fields(oitem.data)
        kfields = split_fivea_fields(kitem.data)
        original_runtime = switch_fivea_runtime_length(
            opart.data,
            record.original_offset - opart.start,
        )
        target_index, target_inner = _find_target_anchor(
            opart.grouped_items,
            record.original_offset + original_runtime,
        )
        meta = {
            "record": record,
            "oidx": oidx,
            "kidx": kidx,
            "oitem": oitem,
            "kitem": kitem,
            "ofields": ofields,
            "kfields": kfields,
            "target_index": target_index,
            "target_inner": target_inner,
        }
        metadata_by_partition[record.partition][oidx] = meta
        if ofields[2][1] == kfields[2][1]:
            name_only.append(meta)
            current[record.partition][oidx] = oitem.data
        else:
            translated.append(meta)
            current[record.partition][oidx] = compose_fivea(oitem.data, kitem.data)

    if require_canonical_counts and (len(translated), len(name_only)) != (EXPECTED_TRANSLATED, EXPECTED_NAME_ONLY):
        _fail(
            "FIVEA_CLASSIFICATION_COUNT_FAIL",
            f"translated={len(translated)} name_only={len(name_only)}",
        )

    resolutions = []
    no_solution = []

    def evaluate(meta, candidate: bytes):
        pi = meta["record"].partition
        idx = meta["oidx"]
        trial = list(current[pi])
        trial[idx] = candidate
        structural = repair_structure(pi, trial)
        prefix = [0]
        for item in trial:
            prefix.append(prefix[-1] + len(item))
        desired_original = (
            prefix[meta["target_index"]]
            + meta["target_inner"]
            - prefix[idx]
        )
        tail = candidate + b"".join(structural[idx + 1 :])
        runtime = switch_fivea_runtime_length(tail, 0)
        return runtime, desired_original

    for partition_index in sorted(metadata_by_partition):
        metas = [
            meta
            for meta in metadata_by_partition[partition_index].values()
            if meta in translated
        ]
        for meta in sorted(metas, key=lambda value: value["oidx"], reverse=True):
            record = meta["record"]
            idx = meta["oidx"]
            found = None
            for dialogue_spaces in (0, 1, 2, 3):
                candidate = compose_fivea(
                    meta["oitem"].data,
                    meta["kitem"].data,
                    dialogue_spaces=dialogue_spaces,
                )
                runtime, desired = evaluate(meta, candidate)
                if runtime == desired:
                    found = ("ORIGINAL_TARGET", 0, dialogue_spaces, candidate)
                    break

            if found is None:
                opart = original.partitions[partition_index]
                kpart = pc_ko.partitions[partition_index]
                next_original_opcode = (
                    opart.grouped_items[idx + 1].opcode
                    if idx + 1 < len(opart.grouped_items)
                    else None
                )
                next_ko_opcode = (
                    kpart.grouped_items[meta["kidx"] + 1].opcode
                    if meta["kidx"] + 1 < len(kpart.grouped_items)
                    else None
                )
                ko_self_contained = switch_fivea_runtime_length(meta["kitem"].data, 0) == len(meta["kitem"].data)
                choice_eligible = (
                    meta["target_index"] == idx + 1
                    and meta["target_inner"] > 0
                    and next_original_opcode == 0x15
                    and next_ko_opcode == 0x15
                    and ko_self_contained
                )
                if choice_eligible:
                    candidate = compose_fivea(
                        meta["oitem"].data,
                        meta["kitem"].data,
                        name2_spaces=2,
                    )
                    runtime, _ = evaluate(meta, candidate)
                    if runtime == len(candidate):
                        found = ("CHOICE_NEXT_START", 2, 0, candidate)

            if found is None:
                opart = original.partitions[partition_index]
                next_original_opcode = (
                    opart.grouped_items[idx + 1].opcode
                    if idx + 1 < len(opart.grouped_items)
                    else None
                )
                ko_self_contained = switch_fivea_runtime_length(meta["kitem"].data, 0) == len(meta["kitem"].data)
                zero_eligible = next_original_opcode == 0x00 and ko_self_contained
                if zero_eligible:
                    candidate = compose_fivea(
                        meta["oitem"].data,
                        meta["kitem"].data,
                        name2_spaces=2,
                    )
                    runtime, _ = evaluate(meta, candidate)
                    if runtime == len(candidate):
                        found = ("ZERO_NEXT_TERMINATOR", 2, 0, candidate)

            if found is None:
                no_solution.append((partition_index, record.original_offset))
                continue

            kind, name2_spaces, dialogue_spaces, candidate = found
            current[partition_index][idx] = candidate
            resolutions.append(
                FiveAResolution(
                    partition=partition_index,
                    item_index=idx,
                    original_offset=record.original_offset,
                    ko_offset=record.ko_offset,
                    kind=kind,
                    name2_spaces=name2_spaces,
                    dialogue_spaces=dialogue_spaces,
                )
            )

    if no_solution:
        _fail("FIVEA_NO_SOLUTION", repr(no_solution[:20]))

    final_repaired = [repair_structure(pi, items) for pi, items in enumerate(current)]
    resolution_by_offset = {row.original_offset: row for row in resolutions}
    violations = []
    for meta in translated:
        record = meta["record"]
        resolution = resolution_by_offset.get(record.original_offset)
        if resolution is None:
            violations.append((record.partition, record.original_offset, "MISSING_RESOLUTION"))
            continue
        items = final_repaired[record.partition]
        prefix = [0]
        for item in items:
            prefix.append(prefix[-1] + len(item))
        idx = meta["oidx"]
        runtime = switch_fivea_runtime_length(b"".join(items[idx:]), 0)
        if resolution.kind == "ORIGINAL_TARGET":
            desired = prefix[meta["target_index"]] + meta["target_inner"] - prefix[idx]
        else:
            desired = len(items[idx])
        if runtime != desired:
            violations.append((record.partition, record.original_offset, resolution.kind, runtime, desired))

    counts = Counter(row.kind for row in resolutions)
    pads = Counter((row.name2_spaces, row.dialogue_spaces) for row in resolutions)
    modified = [row for row in resolutions if row.name2_spaces or row.dialogue_spaces]
    dialogue_pad = [row for row in resolutions if row.dialogue_spaces]
    choice = [row for row in resolutions if row.kind == "CHOICE_NEXT_START"]
    zero = [row for row in resolutions if row.kind == "ZERO_NEXT_TERMINATOR"]

    report = FiveACompositeReport(
        mapping_rows=len(mapping),
        translated_rows=len(translated),
        name_only_preserved_rows=len(name_only),
        original_target_rows=counts["ORIGINAL_TARGET"],
        choice_next_start_rows=counts["CHOICE_NEXT_START"],
        zero_next_terminator_rows=counts["ZERO_NEXT_TERMINATOR"],
        unmodified_translated_rows=pads[(0, 0)],
        dialogue_pad_1_rows=pads[(0, 1)],
        dialogue_pad_2_rows=pads[(0, 2)],
        dialogue_pad_3_rows=pads[(0, 3)],
        name2_pad_2_rows=pads[(2, 0)],
        modified_rows=len(modified),
        modified_rowset_sha256=_rowset_hash(modified),
        dialogue_pad_rowset_sha256=_rowset_hash(dialogue_pad),
        choice_rowset_sha256=_rowset_hash(choice),
        zero_rowset_sha256=_rowset_hash(zero),
        verification_violations=len(violations),
    )

    if require_canonical_counts:
        expected = {
            "original_target_rows": EXPECTED_ORIGINAL_TARGET,
            "choice_next_start_rows": EXPECTED_CHOICE_NEXT_START,
            "zero_next_terminator_rows": EXPECTED_ZERO_NEXT_TERMINATOR,
            "unmodified_translated_rows": 992,
            "dialogue_pad_1_rows": 40,
            "dialogue_pad_2_rows": 15,
            "dialogue_pad_3_rows": 11,
            "name2_pad_2_rows": 16,
            "modified_rows": EXPECTED_MODIFIED,
            "verification_violations": 0,
        }
        for field, value in expected.items():
            actual = getattr(report, field)
            if actual != value:
                _fail("FIVEA_CANONICAL_COUNT_FAIL", f"{field}={actual} expected={value}")
        hashes = {
            "modified_rowset_sha256": EXPECTED_MODIFIED_ROWSET_SHA256,
            "dialogue_pad_rowset_sha256": EXPECTED_DIALOGUE_PAD_ROWSET_SHA256,
            "choice_rowset_sha256": EXPECTED_CHOICE_ROWSET_SHA256,
            "zero_rowset_sha256": EXPECTED_ZERO_ROWSET_SHA256,
        }
        for field, value in hashes.items():
            actual = getattr(report, field)
            if actual != value:
                _fail("FIVEA_CANONICAL_ROWSET_FAIL", f"{field}={actual} expected={value}")

    return tuple(tuple(items) for items in current), report, tuple(resolutions)
