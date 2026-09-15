from __future__ import annotations

from collections import defaultdict, deque
from dataclasses import dataclass
import struct
from typing import Iterable

T5K_MAGIC = b"T5K121R\x00"
T5K_VERSION = 1
T5K_MAPPING_COUNT = 10_036
T5K_ORIGINAL_MAPPING_COUNT = 7_494
T5K_KOREAN_ADDITION_COUNT = 2_542
T5K_EXPECTED_INLINE_COUNT = 17_103
T5K_EXPECTED_POINTER_COUNT = 56
T5K_EXPECTED_RUNTIME_COUNT = 11
T5K_EXPECTED_EXE_SIZE = 18_685_960


@dataclass(frozen=True)
class InlinePatchRecord:
    pc_rva: int
    length: int
    original: bytes
    replacement: bytes
    resource_offset: int


@dataclass(frozen=True)
class PointerPatchRecord:
    pc_slot_rva: int
    pc_original_target_rva: int
    mode: int
    string_offset: int


@dataclass(frozen=True)
class T5KResource:
    version: int
    inline_count: int
    pointer_count: int
    runtime_count: int
    prefix_size: int
    runtime_blob_size: int
    target_exe_size: int
    target_exe_sha256: bytes
    mapping_entries: tuple[tuple[int, int], ...]
    pointer_string_pool: bytes
    runtime_helper_blob: bytes
    inline_records: tuple[InlinePatchRecord, ...]
    pointer_records: tuple[PointerPatchRecord, ...]
    runtime_descriptor_blob: bytes

    @property
    def original_mapping_entries(self) -> tuple[tuple[int, int], ...]:
        return self.mapping_entries[:T5K_ORIGINAL_MAPPING_COUNT]

    @property
    def korean_mapping_entries(self) -> tuple[tuple[int, int], ...]:
        return self.mapping_entries[T5K_ORIGINAL_MAPPING_COUNT:]


def _u16(data: bytes, off: int) -> int:
    return struct.unpack_from("<H", data, off)[0]


def _u32(data: bytes, off: int) -> int:
    return struct.unpack_from("<I", data, off)[0]


def _rva_to_file_offset(pe: bytes, rva: int) -> int:
    if pe[:2] != b"MZ":
        raise RuntimeError("dinput8.dll is not a PE image")
    pe_off = _u32(pe, 0x3C)
    if pe[pe_off:pe_off + 4] != b"PE\x00\x00":
        raise RuntimeError("invalid PE signature")
    coff = pe_off + 4
    section_count = _u16(pe, coff + 2)
    optional_size = _u16(pe, coff + 16)
    section_table = coff + 20 + optional_size
    for i in range(section_count):
        off = section_table + i * 40
        virtual_size = _u32(pe, off + 8)
        virtual_address = _u32(pe, off + 12)
        raw_size = _u32(pe, off + 16)
        raw_pointer = _u32(pe, off + 20)
        span = max(virtual_size, raw_size)
        if virtual_address <= rva < virtual_address + span:
            return raw_pointer + (rva - virtual_address)
    raise RuntimeError(f"RVA 0x{rva:X} is outside PE sections")


def extract_t5k_rcdata(dll: bytes, resource_id: int = 101) -> bytes:
    """Extract RT_RCDATA/<resource_id> from the PC patch dinput8.dll."""
    if dll[:2] != b"MZ":
        raise RuntimeError("dinput8.dll is not a PE image")
    pe_off = _u32(dll, 0x3C)
    coff = pe_off + 4
    optional_size = _u16(dll, coff + 16)
    optional = coff + 20
    magic = _u16(dll, optional)
    if magic == 0x20B:
        data_dir = optional + 112
    elif magic == 0x10B:
        data_dir = optional + 96
    else:
        raise RuntimeError(f"unsupported PE optional-header magic 0x{magic:X}")

    resource_rva = _u32(dll, data_dir + 2 * 8)
    resource_size = _u32(dll, data_dir + 2 * 8 + 4)
    if not resource_rva or not resource_size:
        raise RuntimeError("PE has no resource directory")
    root = _rva_to_file_offset(dll, resource_rva)

    def directory_entries(rel: int) -> list[tuple[int, int]]:
        base = root + rel
        named = _u16(dll, base + 12)
        ids = _u16(dll, base + 14)
        out: list[tuple[int, int]] = []
        p = base + 16
        for _ in range(named + ids):
            out.append((_u32(dll, p), _u32(dll, p + 4)))
            p += 8
        return out

    type_target = None
    for name_or_id, target in directory_entries(0):
        if not (name_or_id & 0x80000000) and name_or_id == 10:
            type_target = target
            break
    if type_target is None or not (type_target & 0x80000000):
        raise RuntimeError("RT_RCDATA resource directory not found")

    id_target = None
    for name_or_id, target in directory_entries(type_target & 0x7FFFFFFF):
        if not (name_or_id & 0x80000000) and name_or_id == resource_id:
            id_target = target
            break
    if id_target is None or not (id_target & 0x80000000):
        raise RuntimeError(f"RT_RCDATA/{resource_id} not found")

    lang_entries = directory_entries(id_target & 0x7FFFFFFF)
    if not lang_entries:
        raise RuntimeError("resource has no language entry")
    leaf = lang_entries[0][1]
    if leaf & 0x80000000:
        raise RuntimeError("unexpected extra resource-directory level")
    data_entry = root + leaf
    payload_rva = _u32(dll, data_entry)
    payload_size = _u32(dll, data_entry + 4)
    payload_off = _rva_to_file_offset(dll, payload_rva)
    payload = dll[payload_off:payload_off + payload_size]
    if len(payload) != payload_size:
        raise RuntimeError("truncated RT_RCDATA payload")
    return payload


def parse_t5k_resource(blob: bytes) -> T5KResource:
    if len(blob) < 0x48 or blob[:8] != T5K_MAGIC:
        raise RuntimeError("invalid T5K121R resource")

    version = _u32(blob, 0x08)
    inline_count = _u32(blob, 0x0C)
    pointer_count = _u32(blob, 0x10)
    runtime_count = _u32(blob, 0x14)
    prefix_size = _u32(blob, 0x18)
    runtime_blob_size = _u32(blob, 0x1C)
    target_exe_size = _u32(blob, 0x20)
    target_exe_sha = blob[0x28:0x48]

    if not (
        version == T5K_VERSION
        and inline_count == T5K_EXPECTED_INLINE_COUNT
        and pointer_count == T5K_EXPECTED_POINTER_COUNT
        and runtime_count == T5K_EXPECTED_RUNTIME_COUNT
        and target_exe_size == T5K_EXPECTED_EXE_SIZE
    ):
        raise RuntimeError(
            "unsupported T5K121R layout: "
            f"version={version}, inline={inline_count}, pointer={pointer_count}, "
            f"runtime={runtime_count}, exe_size={target_exe_size}"
        )

    mapping_start = 0x48
    mapping_end = mapping_start + T5K_MAPPING_COUNT * 4
    prefix_end = mapping_start + prefix_size
    helper_end = prefix_end + runtime_blob_size
    if not (mapping_start <= mapping_end <= prefix_end <= helper_end <= len(blob)):
        raise RuntimeError("T5K121R section bounds are invalid")

    mapping = tuple(
        struct.unpack_from("<HH", blob, mapping_start + i * 4)
        for i in range(T5K_MAPPING_COUNT)
    )
    pointer_string_pool = blob[mapping_end:prefix_end]
    helper_blob = blob[prefix_end:helper_end]

    pos = helper_end
    inline: list[InlinePatchRecord] = []
    for _ in range(inline_count):
        if pos + 8 > len(blob):
            raise RuntimeError("truncated inline-patch table")
        pc_rva, length = struct.unpack_from("<II", blob, pos)
        end = pos + 8 + length * 2
        if length == 0 or end > len(blob):
            raise RuntimeError(f"invalid inline record at 0x{pos:X}")
        original = blob[pos + 8:pos + 8 + length]
        replacement = blob[pos + 8 + length:end]
        inline.append(InlinePatchRecord(pc_rva, length, original, replacement, pos))
        pos = end

    pointer: list[PointerPatchRecord] = []
    for _ in range(pointer_count):
        if pos + 16 > len(blob):
            raise RuntimeError("truncated pointer-patch table")
        pointer.append(PointerPatchRecord(*struct.unpack_from("<IIII", blob, pos)))
        pos += 16

    runtime_descriptor_blob = blob[pos:]
    for name in (
        b"ui_width_1", b"ui_width_2", b"ui_width_3", b"ui_width_4",
        b"description_font_1", b"description_font_2",
        b"mapping_lookup_1A", b"mapping_lookup_2A",
        b"runtime_byte_validation", b"font_page_limit", b"runtime_page_mapper",
    ):
        if name not in runtime_descriptor_blob:
            raise RuntimeError(f"runtime descriptor missing: {name.decode()}")

    return T5KResource(
        version=version,
        inline_count=inline_count,
        pointer_count=pointer_count,
        runtime_count=runtime_count,
        prefix_size=prefix_size,
        runtime_blob_size=runtime_blob_size,
        target_exe_size=target_exe_size,
        target_exe_sha256=target_exe_sha,
        mapping_entries=mapping,
        pointer_string_pool=pointer_string_pool,
        runtime_helper_blob=helper_blob,
        inline_records=tuple(inline),
        pointer_records=tuple(pointer),
        runtime_descriptor_blob=runtime_descriptor_blob,
    )


def build_aho(patterns: list[bytes]):
    nexts: list[dict[int, int]] = [{}]
    fail: list[int] = [0]
    outs: list[list[int]] = [[]]
    for pid, pattern in enumerate(patterns):
        state = 0
        for byte in pattern:
            nxt = nexts[state].get(byte)
            if nxt is None:
                nxt = len(nexts)
                nexts[state][byte] = nxt
                nexts.append({})
                fail.append(0)
                outs.append([])
            state = nxt
        outs[state].append(pid)

    queue = deque(nexts[0].values())
    while queue:
        r = queue.popleft()
        for byte, state in nexts[r].items():
            queue.append(state)
            f = fail[r]
            while f and byte not in nexts[f]:
                f = fail[f]
            fail[state] = nexts[f].get(byte, 0)
            if outs[fail[state]]:
                outs[state].extend(outs[fail[state]])
    return nexts, fail, outs


def find_pattern_occurrences(haystack: bytes, patterns: list[bytes], cap: int = 2) -> list[list[int]]:
    if not patterns:
        return []
    nexts, fail, outs = build_aho(patterns)
    found: list[list[int]] = [[] for _ in patterns]
    state = 0
    for i, byte in enumerate(haystack):
        while state and byte not in nexts[state]:
            state = fail[state]
        state = nexts[state].get(byte, 0)
        if outs[state]:
            for pid in outs[state]:
                if len(found[pid]) < cap:
                    found[pid].append(i - len(patterns[pid]) + 1)
    return found


def select_safe_inline_patches(
    flat_nso: bytes,
    records: Iterable[InlinePatchRecord],
    allowed_start: int,
    allowed_end: int,
) -> tuple[list[tuple[int, bytes, bytes]], dict[str, int]]:
    """Map exact-unique PC replacement records into Switch rodata without guessing."""
    groups: dict[bytes, list[InlinePatchRecord]] = defaultdict(list)
    for rec in records:
        groups[rec.original].append(rec)

    patterns = list(groups)
    occurrences = find_pattern_occurrences(flat_nso, patterns, cap=2)
    candidates: list[tuple[int, bytes, bytes]] = []
    stats = {
        "pc_records_total": sum(len(v) for v in groups.values()),
        "pc_unique_original_patterns": len(patterns),
        "no_switch_match": 0,
        "multiple_switch_matches": 0,
        "conflicting_pc_replacements": 0,
        "unique_match_outside_rodata": 0,
        "candidate_patterns": 0,
        "selected_patterns": 0,
        "selected_pc_records_covered": 0,
        "overlap_skipped": 0,
    }

    pattern_to_pc_count = {p: len(groups[p]) for p in patterns}
    for pattern, locs in zip(patterns, occurrences):
        if not locs:
            stats["no_switch_match"] += 1
            continue
        if len(locs) != 1:
            stats["multiple_switch_matches"] += 1
            continue
        replacements = {r.replacement for r in groups[pattern]}
        if len(replacements) != 1:
            stats["conflicting_pc_replacements"] += 1
            continue
        offset = locs[0]
        if not (allowed_start <= offset and offset + len(pattern) <= allowed_end):
            stats["unique_match_outside_rodata"] += 1
            continue
        candidates.append((offset, pattern, next(iter(replacements))))

    stats["candidate_patterns"] = len(candidates)
    selected: list[tuple[int, bytes, bytes]] = []
    occupied: list[tuple[int, int]] = []
    for offset, original, replacement in sorted(candidates, key=lambda x: (-len(x[1]), x[0])):
        start, end = offset, offset + len(original)
        if any(max(start, a) < min(end, b) for a, b in occupied):
            stats["overlap_skipped"] += 1
            continue
        selected.append((offset, original, replacement))
        occupied.append((start, end))
        stats["selected_pc_records_covered"] += pattern_to_pc_count[original]

    selected.sort(key=lambda x: x[0])
    stats["selected_patterns"] = len(selected)
    return selected, stats
