from __future__ import annotations

from collections import Counter
from dataclasses import asdict, dataclass
import argparse
import hashlib
import json
from pathlib import Path
import struct
from typing import AbstractSet, Sequence

STOCK_SIZE = 931_936
STOCK_SHA256 = "bbaaff8dc552da17a49ea2e6ce49a76da662541ee22fdec7dc7933046430bf09"
ENTRYPOINT_COUNT = 782
OFFSET_COUNT = ENTRYPOINT_COUNT + 1
HEADER_SIZE = 0xC44

TEXTISH_OPCODES = frozenset({0x11, 0x12, 0x13, 0x1E})
TARGET_OPCODES = frozenset({0x11, 0x12, 0x13, 0x15})
TEXT_MERGE_TRAP_STARTS = frozenset({0x11, 0x12, 0x13, 0x1E, 0x15, 0x04, 0x06, 0x07, 0x08, 0x09, 0x3C})
BRANCH_ANALYSIS_ORDER = (0x02, 0x04, 0x06, 0x07, 0x08, 0x09)
MAX_BRANCH_STAGE_ITEMS = 2000

# V334 original-side counterparts. S2 never repairs these through the generic pass.
DYNAMIC_SWITCH_SPAN_ORIGINAL_STARTS = frozenset({0xCBBB0, 0x65F40, 0x7E1B0})
FALSE_EVENT_02_EXPRESSION_ORIGINAL_STARTS = frozenset({0xAC470, 0x980C0})
GENERIC_BRANCH_EXCLUDED_ORIGINAL_STARTS = (
    DYNAMIC_SWITCH_SPAN_ORIGINAL_STARTS | FALSE_EVENT_02_EXPRESSION_ORIGINAL_STARTS
)


class SelectiveEventError(RuntimeError):
    def __init__(self, code: str, detail: str):
        self.code = code
        self.detail = detail
        super().__init__(f"{code}: {detail}")


@dataclass(frozen=True)
class GroupedItem:
    start: int
    data: bytes
    disguised_15: bool = False
    guard_merge: str | None = None

    @property
    def opcode(self) -> int:
        return self.data[0]


@dataclass(frozen=True)
class BranchRepairPlan:
    opcode: int
    item_index: int
    stage_count: int
    intrusion: int
    original_span: int
    original_start: int


@dataclass(frozen=True)
class EventPartition:
    index: int
    start: int
    end: int
    data: bytes
    grouped_items: tuple[GroupedItem, ...]


@dataclass(frozen=True)
class ParsedEventTs5:
    prefix: bytes
    count: int
    offsets: tuple[int, ...]
    partitions: tuple[EventPartition, ...]


@dataclass(frozen=True)
class NoopSerializationReport:
    input_size: int
    input_sha256: str
    output_size: int
    output_sha256: str
    byte_exact: bool
    entrypoints: int
    offsets: int
    first_offset: int
    last_offset: int
    grouped_items: int
    target_looking_items: int
    disguised_15: int
    guard_merge_counts: dict[str, int]

    def to_dict(self) -> dict:
        return asdict(self)


def _fail(code: str, detail: str) -> None:
    raise SelectiveEventError(code, detail)


def _sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def _read_u32(data: bytes, offset: int) -> int:
    if offset < 0 or offset + 4 > len(data):
        _fail("TS5_HEADER_TRUNCATED", f"u32 read outside file at {offset:#x}")
    return struct.unpack_from("<I", data, offset)[0]


def _chunks4(data: bytes, absolute_start: int) -> list[GroupedItem]:
    if len(data) % 4:
        _fail("PARTITION_ALIGNMENT_FAIL", f"partition at {absolute_start:#x} has {len(data)} bytes")
    return [GroupedItem(absolute_start + pos, data[pos:pos + 4]) for pos in range(0, len(data), 4)]


def group_partition(data: bytes, absolute_start: int = 0) -> tuple[GroupedItem, ...]:
    """Replay PC editor v0.30 CombineDialogueBytes grouping without mutating bytes."""
    items = _chunks4(data, absolute_start)
    i = 0
    while i < len(items):
        current = items[i]
        current_bytes = current.data
        opcode = current_bytes[0]

        if opcode in TEXTISH_OPCODES:
            combined = bytearray(current_bytes)
            j = i + 1
            last = i
            while j < len(items):
                following = items[j].data
                if following[0] in TEXT_MERGE_TRAP_STARTS:
                    break
                combined += following
                last = j
                if following[3] == 0:
                    break
                j += 1
            items[i] = GroupedItem(current.start, bytes(combined))
            if last >= i + 1:
                del items[i + 1:last + 1]

        elif opcode == 0x15:
            combined = bytearray(current_bytes)
            choice_count = current_bytes[1]
            disguised = current_bytes[3] == 0x03
            if disguised:
                items[i] = GroupedItem(current.start, bytes(combined), disguised_15=True)
            else:
                completed = 0
                j = i + 1
                last = i
                while j < len(items):
                    following = items[j].data
                    combined += following
                    last = j
                    if following == b"\x0A\x80\x1C\x00":
                        completed = choice_count
                    elif following[3] == 0 and completed < choice_count:
                        completed += 1
                    if completed == choice_count:
                        break
                    j += 1
                items[i] = GroupedItem(current.start, bytes(combined))
                if last >= i + 1:
                    del items[i + 1:last + 1]

        elif opcode in (0x16, 0x17, 0x18):
            if i + 1 < len(items) and items[i + 1].data[0] == 0x04:
                items[i] = GroupedItem(
                    current.start,
                    current.data + items[i + 1].data,
                    guard_merge="16_18_plus_04",
                )
                del items[i + 1]

        elif current_bytes[0] == 0x0B and current_bytes[2] == 0x17 and current_bytes[3] == 0x00:
            if i + 1 < len(items):
                following = items[i + 1].data
                if following[0] == 0x04 and following[1] == 0x00:
                    items[i] = GroupedItem(
                        current.start,
                        current.data + following,
                        guard_merge="0b17_plus_0400",
                    )
                    del items[i + 1]

        elif current_bytes[0] == 0x04 and current_bytes[1] == 0x00 and current_bytes[3] == 0x0E:
            if i + 1 < len(items):
                following = items[i + 1].data
                if following[0] == 0x04 and following[1] == 0x00 and following[3] == 0x0E:
                    items[i] = GroupedItem(
                        current.start,
                        current.data + following,
                        guard_merge="04000e_pair",
                    )
                    del items[i + 1]

        elif opcode == 0x5A:
            combined = bytearray(current_bytes)
            completed = 0
            j = i + 1
            last = i
            while j < len(items):
                following = items[j].data
                combined += following
                last = j
                if following[3] == 0 and completed < 3:
                    completed += 1
                if completed == 3:
                    break
                j += 1
            items[i] = GroupedItem(current.start, bytes(combined))
            if last >= i + 1:
                del items[i + 1:last + 1]

        elif opcode == 0x3C:
            combined = bytearray(current_bytes)
            completed = 0
            j = i + 1
            last = i
            while j < len(items):
                following = items[j].data
                combined += following
                last = j
                if following == b"\x00" * 4 and completed < 4:
                    completed += 1
                elif following[3] == 0 and completed < 4:
                    completed += 1
                if completed == 4:
                    break
                j += 1
            items[i] = GroupedItem(current.start, bytes(combined))
            if last >= i + 1:
                del items[i + 1:last + 1]

        i += 1

    rebuilt = b"".join(item.data for item in items)
    if rebuilt != data:
        _fail("GROUPING_BYTE_PRESERVATION_FAIL", f"grouping changed bytes at partition {absolute_start:#x}")
    expected = absolute_start
    for item in items:
        if item.start != expected:
            _fail("GROUPING_CONTIGUITY_FAIL", f"item starts at {item.start:#x}, expected {expected:#x}")
        expected += len(item.data)
    if expected != absolute_start + len(data):
        _fail("GROUPING_CONTIGUITY_FAIL", f"grouped extent ends at {expected:#x}")
    return tuple(items)


def _pc_editor_04_second_byte_matches(value: int) -> bool:
    # The VB source uses Regex("[0-4]{2}") for the rendered byte text.
    rendered = f"{value:02X}"
    return rendered[0] in "01234" and rendered[1] in "01234"


def _is_pc_editor_branch_candidate(opcode: int, item: GroupedItem) -> bool:
    data = item.data
    if len(data) < 4 or data[0] != opcode:
        return False
    if opcode == 0x02:
        return data[3] == 0
    if opcode == 0x04:
        return len(data) == 4 and _pc_editor_04_second_byte_matches(data[1])
    return opcode in BRANCH_ANALYSIS_ORDER


def _decode_pc_editor_branch_span(opcode: int, header: bytes) -> tuple[int, int] | None:
    if len(header) < 4 or header[0] != opcode:
        _fail("BRANCH_HEADER_MISMATCH", f"opcode={opcode:#x} header={header[:4].hex()}")

    if opcode == 0x02:
        return int.from_bytes(header[1:3], "little") * 4, 0
    if opcode == 0x04:
        encoded = int.from_bytes(header[2:4], "little")
        if encoded % 2:
            return None
        return encoded // 2, 0
    if opcode in (0x06, 0x07):
        physical = int.from_bytes(header[1:4], "little") * 2
        intrusion = physical % 4
        return physical - intrusion, intrusion
    if opcode == 0x08:
        return int.from_bytes(header[2:4], "little") * 4, 0
    if opcode == 0x09:
        encoded = int.from_bytes(header[2:4], "little")
        intrusion = encoded % 4
        return (encoded - intrusion) // 2, intrusion
    _fail("UNSUPPORTED_BRANCH_OPCODE", f"opcode={opcode:#x}")


def _find_pc_editor_stage_count(
    items: Sequence[GroupedItem],
    item_index: int,
    original_span: int,
) -> int:
    total = 0
    for step in range(MAX_BRANCH_STAGE_ITEMS):
        current = item_index + step
        if current >= len(items):
            return 0
        total += len(items[current].data)
        if total == original_span:
            return step + 1
        if total > original_span:
            return 0
    return 0


def analyze_generic_branch_plans(
    items: Sequence[GroupedItem],
    *,
    excluded_starts: AbstractSet[int] = GENERIC_BRANCH_EXCLUDED_ORIGINAL_STARTS,
) -> tuple[BranchRepairPlan, ...]:
    """Freeze PC-editor branch ownership from original grouped items.

    Ownership is source-item-count based, not final-byte reparsing. Known
    Switch dynamic-span and false EVENT-02 expression starts are kept out of
    this generic S2 pass.
    """
    plans: list[BranchRepairPlan] = []
    for opcode in BRANCH_ANALYSIS_ORDER:
        for item_index, item in enumerate(items):
            if item.start in excluded_starts:
                continue
            if not _is_pc_editor_branch_candidate(opcode, item):
                continue
            decoded = _decode_pc_editor_branch_span(opcode, item.data[:4])
            if decoded is None:
                continue
            original_span, intrusion = decoded
            stage_count = _find_pc_editor_stage_count(items, item_index, original_span)
            if not stage_count:
                continue
            plans.append(
                BranchRepairPlan(
                    opcode=opcode,
                    item_index=item_index,
                    stage_count=stage_count,
                    intrusion=intrusion,
                    original_span=original_span,
                    original_start=item.start,
                )
            )
    return tuple(plans)


def _encode_pc_editor_branch_span(
    opcode: int,
    owner: bytes,
    current_span: int,
    intrusion: int,
) -> bytes:
    if len(owner) < 4 or owner[0] != opcode:
        _fail("BRANCH_OWNER_MUTATED", f"opcode={opcode:#x} owner={owner[:4].hex()}")

    updated = bytearray(owner)
    if opcode in (0x02, 0x08):
        if current_span % 4:
            _fail(
                "BRANCH_SPAN_NOT_REPRESENTABLE",
                f"opcode={opcode:#x} span={current_span} is not divisible by 4",
            )
        encoded = current_span // 4
        if encoded > 0xFFFF:
            _fail("BRANCH_FIELD_OVERFLOW", f"opcode={opcode:#x} encoded={encoded:#x}")
        if opcode == 0x02:
            updated[1:3] = encoded.to_bytes(2, "little")
        else:
            updated[2:4] = encoded.to_bytes(2, "little")
    elif opcode == 0x04:
        encoded = current_span * 2
        if encoded > 0xFFFF:
            _fail("BRANCH_FIELD_OVERFLOW", f"opcode=0x04 encoded={encoded:#x}")
        updated[2:4] = encoded.to_bytes(2, "little")
    elif opcode in (0x06, 0x07):
        physical = current_span + intrusion
        if physical % 2:
            _fail(
                "BRANCH_SPAN_NOT_REPRESENTABLE",
                f"opcode={opcode:#x} span={current_span} intrusion={intrusion}",
            )
        encoded = physical // 2
        if encoded > 0xFFFFFF:
            _fail("BRANCH_FIELD_OVERFLOW", f"opcode={opcode:#x} encoded={encoded:#x}")
        updated[1:4] = encoded.to_bytes(3, "little")
    elif opcode == 0x09:
        encoded = current_span * 2 + intrusion
        if encoded > 0xFFFF:
            _fail("BRANCH_FIELD_OVERFLOW", f"opcode=0x09 encoded={encoded:#x}")
        updated[2:4] = encoded.to_bytes(2, "little")
    else:
        _fail("UNSUPPORTED_BRANCH_OPCODE", f"opcode={opcode:#x}")

    return bytes(updated)


def repair_generic_branch_items(
    original_items: Sequence[GroupedItem],
    current_item_bytes: Sequence[bytes],
    *,
    plans: Sequence[BranchRepairPlan] | None = None,
) -> tuple[bytes, ...]:
    """Apply source-proven PC-editor generic branch arithmetic.

    The original item partition/order is authority. Current bytes may change
    length, but the serializer never fresh-reparses them to rediscover branch
    ownership.
    """
    if len(original_items) != len(current_item_bytes):
        _fail(
            "GROUPED_ITEM_COUNT_MISMATCH",
            f"original={len(original_items)} current={len(current_item_bytes)}",
        )

    current = [bytes(data) for data in current_item_bytes]
    active_plans = (
        analyze_generic_branch_plans(original_items)
        if plans is None
        else tuple(plans)
    )
    family_rank = {opcode: rank for rank, opcode in enumerate(BRANCH_ANALYSIS_ORDER)}

    for plan in sorted(active_plans, key=lambda x: (family_rank[x.opcode], x.item_index)):
        stop = plan.item_index + plan.stage_count
        if stop > len(current):
            _fail(
                "BRANCH_STAGE_RANGE_FAIL",
                f"start={plan.original_start:#x} stop_item={stop} count={len(current)}",
            )
        owner = current[plan.item_index]
        if len(owner) < 4 or owner[0] != plan.opcode:
            _fail(
                "BRANCH_OWNER_MUTATED",
                f"start={plan.original_start:#x} opcode={plan.opcode:#x}",
            )
        current_span = sum(len(current[i]) for i in range(plan.item_index, stop))
        current[plan.item_index] = _encode_pc_editor_branch_span(
            plan.opcode,
            owner,
            current_span,
            plan.intrusion,
        )

    return tuple(current)


def parse_event_ts5(blob: bytes, *, require_stock_identity: bool = False) -> ParsedEventTs5:
    if require_stock_identity and (len(blob) != STOCK_SIZE or _sha256(blob) != STOCK_SHA256):
        _fail("STOCK_IDENTITY_MISMATCH", f"size={len(blob)} sha256={_sha256(blob)}")
    if len(blob) < 12:
        _fail("TS5_HEADER_TRUNCATED", "file shorter than count/offset header")

    count = _read_u32(blob, 4)
    table_end = 8 + 4 * (count + 1)
    if table_end > len(blob):
        _fail("TS5_OFFSET_TABLE_TRUNCATED", f"table end {table_end:#x} exceeds file")
    offsets = tuple(_read_u32(blob, 8 + 4 * i) for i in range(count + 1))
    if not offsets:
        _fail("TS5_OFFSET_TABLE_EMPTY", "no offsets")
    if offsets[0] != table_end:
        _fail("TS5_FIRST_OFFSET_FAIL", f"first={offsets[0]:#x} expected={table_end:#x}")
    if offsets[-1] != len(blob):
        _fail("TS5_EOF_OFFSET_FAIL", f"last={offsets[-1]:#x} eof={len(blob):#x}")
    if any(a >= b for a, b in zip(offsets, offsets[1:])):
        _fail("TS5_OFFSET_ORDER_FAIL", "offsets are not strictly increasing")
    if any(offset % 4 for offset in offsets):
        _fail("TS5_OFFSET_ALIGNMENT_FAIL", "one or more offsets are not 4-byte aligned")

    partitions: list[EventPartition] = []
    for index in range(count):
        start, end = offsets[index], offsets[index + 1]
        data = blob[start:end]
        grouped = group_partition(data, start)
        partitions.append(EventPartition(index=index, start=start, end=end, data=data, grouped_items=grouped))

    parsed = ParsedEventTs5(prefix=blob[:4], count=count, offsets=offsets, partitions=tuple(partitions))
    if require_stock_identity:
        if parsed.count != ENTRYPOINT_COUNT:
            _fail("STOCK_STRUCTURE_MISMATCH", f"count={parsed.count}")
        if len(parsed.offsets) != OFFSET_COUNT or parsed.offsets[0] != HEADER_SIZE:
            _fail("STOCK_STRUCTURE_MISMATCH", "stock count/offset-table geometry mismatch")
    return parsed


def rebuild_event_ts5(parsed: ParsedEventTs5, partitions: Sequence[bytes] | None = None) -> bytes:
    payloads = tuple(partitions) if partitions is not None else tuple(part.data for part in parsed.partitions)
    if len(payloads) != parsed.count:
        _fail("PARTITION_COUNT_MISMATCH", f"payloads={len(payloads)} count={parsed.count}")
    if any(len(payload) % 4 for payload in payloads):
        _fail("PARTITION_ALIGNMENT_FAIL", "rebuilt partition length is not 4-byte aligned")

    table_end = 8 + 4 * (parsed.count + 1)
    offsets = [table_end]
    for payload in payloads:
        offsets.append(offsets[-1] + len(payload))

    out = bytearray()
    out += parsed.prefix
    out += struct.pack("<I", parsed.count)
    for offset in offsets:
        out += struct.pack("<I", offset)
    for payload in payloads:
        out += payload
    if len(out) != offsets[-1]:
        _fail("REBUILD_EOF_MISMATCH", f"serialized={len(out):#x} last_offset={offsets[-1]:#x}")
    return bytes(out)


def serialize_noop(blob: bytes, *, require_stock_identity: bool = True) -> tuple[bytes, NoopSerializationReport]:
    parsed = parse_event_ts5(blob, require_stock_identity=require_stock_identity)
    output = rebuild_event_ts5(parsed)
    guard_counts = Counter(
        item.guard_merge
        for partition in parsed.partitions
        for item in partition.grouped_items
        if item.guard_merge is not None
    )
    grouped_items = sum(len(partition.grouped_items) for partition in parsed.partitions)
    target_looking = sum(
        item.opcode in TARGET_OPCODES
        for partition in parsed.partitions
        for item in partition.grouped_items
    )
    disguised = sum(
        item.disguised_15
        for partition in parsed.partitions
        for item in partition.grouped_items
    )
    report = NoopSerializationReport(
        input_size=len(blob),
        input_sha256=_sha256(blob),
        output_size=len(output),
        output_sha256=_sha256(output),
        byte_exact=output == blob,
        entrypoints=parsed.count,
        offsets=len(parsed.offsets),
        first_offset=parsed.offsets[0],
        last_offset=parsed.offsets[-1],
        grouped_items=grouped_items,
        target_looking_items=target_looking,
        disguised_15=disguised,
        guard_merge_counts=dict(sorted(guard_counts.items())),
    )
    if require_stock_identity and not report.byte_exact:
        _fail("ZERO_REPLACEMENT_IDENTITY_REBUILD_FAIL", "no-op rebuild differs from stock")
    return output, report


def main() -> None:
    parser = argparse.ArgumentParser(description="ECF00000 TS5 no-op serializer core validation")
    parser.add_argument("--input", required=True, type=Path)
    parser.add_argument("--output", type=Path)
    parser.add_argument("--report", type=Path)
    args = parser.parse_args()

    source = args.input.read_bytes()
    output, report = serialize_noop(source, require_stock_identity=True)
    if args.output is not None:
        args.output.write_bytes(output)
    payload = json.dumps(report.to_dict(), ensure_ascii=False, sort_keys=True, indent=2) + "\n"
    if args.report is not None:
        args.report.write_text(payload, encoding="utf-8")
    print(payload, end="")


if __name__ == "__main__":
    main()
