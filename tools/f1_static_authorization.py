#!/usr/bin/env python3
from __future__ import annotations

import argparse
import gzip
from collections import Counter, defaultdict
import hashlib
import json
from pathlib import Path
import struct

import lz4.block

CANONICAL_MAIN_SHA256 = "b366e692208f3c0cc18bc1884ef95689b6b11d722fa2d749b8500abccbc3109b"
CANONICAL_BUILD_ID = bytes.fromhex("d9120950c258610a746f4a31ce3a3b376de393d9000000000000000000000000")
CANONICAL_SOURCE_LEDGER_SHA256 = "0ef81c629adb2e348a72922efcb030908c76fb3cff964804948bf84cd7fd1570"
CANONICAL_EXCEPTIONS_SHA256 = "10b13fe7156225109d86f8d0707dd385d3c24c66dcbe590ae56425e1dc936257"
CANONICAL_LOCALIZATION_INVENTORY_SHA256 = "d7b90f7f7f1e43c54b87d97524b14b1582f390aa8a4672e25c2c48d2f9fac550"

TEXT_MEM_OFF = 0x000000
TEXT_SIZE = 0x58CE60
RODATA_MEM_OFF = 0x58D000
RODATA_SIZE = 0x432018
DATA_MEM_OFF = 0x9C0000
DATA_SIZE = 0x60430
LOCALIZATION_JP_BASE = 0x9C0008
LOCALIZATION_DEST_BASE = 0xA210E0
LOCALIZATION_COUNT = 3803
PC_SCOPE_END = 3250
MIN_SEARCH_RUN = 5
MIN_FINAL_INTERVAL = 5
MIN_ANCHOR_BYTES = 8

# V082 canonical Stage-2 affine blocks, 1-based PC record numbers.
STAGE2_BLOCKS = [
    (3251, 3875, -0x4A3890),
    (3876, 3996, -0x476E80),
    (3997, 4188, -0x476700),
    (4189, 4417, -0x4769E0),
    (4418, 4569, -0x477074),
    (4570, 14429, -0x4AE480),
    (14430, 14541, -0x4A4EAC),
    (14551, 14683, -0x4C3A6E),
    (14737, 15462, -0x4C6E50),
    (15463, 15613, -0x4C8A34),
    (15614, 15619, -0x4C9584),
    (15620, 15679, -0x4C8DD7),
    (15680, 15719, -0x4C909A),
    (15720, 15927, -0x4B5869),
    (15928, 16229, -0x4CF306),
    (16230, 16284, -0x4D8311),
    (16285, 16367, -0x4D84D4),
    (16368, 16427, -0x4D878C),
    (16428, 16446, -0x4D87CF),
    (16467, 16872, -0x67C7CC),
    (16873, 16902, -0x6804B8),
    (16903, 17103, -0x680238),
]

EXPECTED = {
    "search_segments": 142,
    "trimmed_mapped_rows": 1402,
    "trimmed_residual_rows": 278,
    "accepted_segments": 112,
    "accepted_mapped_rows": 1311,
    "accepted_residual_rows": 262,
    "rejected_residual_rows": 16,
    "full_window_all": 197,
    "padding_all": 81,
    "full_window_accepted": 187,
    "padding_accepted": 75,
    "capacity_fail": 4,
    "shared_owner_blocker": 25,
    "static_authorized": 158,
}
EXPECTED_CAPACITY_FAIL = {2674, 2684, 2712, 3142}
EXPECTED_REJECTED_RESIDUAL = {
    284, 286, 821, 1275, 1985, 1986, 1987, 2014,
    2015, 2161, 2253, 2425, 2426, 2480, 3181, 3182,
}


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def decompress_nso(path: Path) -> tuple[bytes, bytes]:
    blob = path.read_bytes()
    if blob[:4] != b"NSO0":
        raise RuntimeError("main is not NSO0")
    flags = struct.unpack_from("<I", blob, 0x0C)[0]
    build_id = blob[0x40:0x60]
    segments = []
    for index, (hdr, comp_off) in enumerate(((0x10, 0x60), (0x20, 0x64), (0x30, 0x68))):
        file_off, mem_off, decomp_size = struct.unpack_from("<III", blob, hdr)
        comp_size = struct.unpack_from("<I", blob, comp_off)[0]
        stored = blob[file_off:file_off + comp_size]
        data = lz4.block.decompress(stored, uncompressed_size=decomp_size) if flags & (1 << index) else stored
        if len(data) != decomp_size:
            raise RuntimeError(f"NSO segment {index} size mismatch")
        segments.append((mem_off, data))
    expected = [(TEXT_MEM_OFF, TEXT_SIZE), (RODATA_MEM_OFF, RODATA_SIZE), (DATA_MEM_OFF, DATA_SIZE)]
    actual = [(off, len(data)) for off, data in segments]
    if actual != expected:
        raise RuntimeError(f"unexpected NSO segment layout: {actual!r}")
    size = max(off + len(data) for off, data in segments)
    flat = bytearray(size)
    for off, data in segments:
        flat[off:off + len(data)] = data
    return build_id, bytes(flat)


def cstr(flat: bytes, off: int) -> bytes:
    end = flat.find(b"\0", off)
    if end < 0:
        raise RuntimeError(f"unterminated string at 0x{off:X}")
    return flat[off:end]


def pc_logical(original: bytes) -> tuple[bytes, bool]:
    try:
        nul = original.index(0)
    except ValueError:
        return original, True
    return original[:nul], all(b == 0 for b in original[nul:])


def ranges_overlap(a0: int, a1: int, b0: int, b1: int) -> bool:
    return max(a0, b0) < min(a1, b1)


def load_inputs(reports: Path):
    source_path = reports / "source_ledger.jsonl"
    exc_path = reports / "exceptions.jsonl"
    loc_path = reports / "localization_language_inventory.json"
    if sha256_file(source_path) != CANONICAL_SOURCE_LEDGER_SHA256:
        raise RuntimeError("source_ledger.jsonl canonical hash mismatch")
    if sha256_file(exc_path) != CANONICAL_EXCEPTIONS_SHA256:
        raise RuntimeError("exceptions.jsonl canonical hash mismatch")
    if sha256_file(loc_path) != CANONICAL_LOCALIZATION_INVENTORY_SHA256:
        raise RuntimeError("localization inventory canonical hash mismatch")

    inline = []
    with source_path.open(encoding="utf-8") as f:
        for line in f:
            row = json.loads(line)
            if row["source_family"] == "inline":
                inline.append(row)
    if len(inline) != 17103:
        raise RuntimeError(f"unexpected inline count {len(inline)}")

    exceptions = []
    with exc_path.open(encoding="utf-8") as f:
        for line in f:
            exceptions.append(json.loads(line))

    loc = json.loads(loc_path.read_text(encoding="utf-8"))
    jp = loc["table_entries"]["JP"]
    if len(jp) != LOCALIZATION_COUNT:
        raise RuntimeError(f"unexpected JP localization count {len(jp)}")
    return inline, exceptions, loc, jp


def main() -> None:
    ap = argparse.ArgumentParser(description="Reproduce F1 row-level static write authorization from canonical read-only inputs")
    ap.add_argument("--reports-dir", required=True, type=Path)
    ap.add_argument("--main", required=True, type=Path)
    ap.add_argument("--manifest", required=True, type=Path)
    ap.add_argument("--summary", required=True, type=Path)
    args = ap.parse_args()

    if sha256_file(args.main) != CANONICAL_MAIN_SHA256:
        raise RuntimeError("Switch main canonical hash mismatch")
    build_id, flat = decompress_nso(args.main)
    if build_id != CANONICAL_BUILD_ID:
        raise RuntimeError(f"Switch Build ID mismatch: {build_id.hex()}")

    inline, exceptions, loc, jp = load_inputs(args.reports_dir)
    jp_objects = [row["object"] for row in jp]
    if any(x is None for x in jp_objects):
        raise RuntimeError("JP localization table has missing object")
    jp_strings = [cstr(flat, off) for off in jp_objects]

    jp_by_value = defaultdict(list)
    for idx, value in enumerate(jp_strings):
        jp_by_value[value].append(idx)
    jp_value_count = Counter(jp_strings)

    logicals = []
    for row in inline:
        logicals.append(pc_logical(bytes.fromhex(row["original"])))

    pc_scope_values = Counter(
        logicals[r - 1][0]
        for r in range(1, PC_SCOPE_END + 1)
        if logicals[r - 1][1]
    )

    # Canonical Stage-2 residual exception population.
    stage2_covered = set()
    for start, end, _delta in STAGE2_BLOCKS:
        stage2_covered.update(range(start, end + 1))
    exception_rnums = {int(e["source_id"].split(":")[1]) + 1 for e in exceptions}
    residual_rnums = exception_rnums - stage2_covered
    if len(residual_rnums) != 1248:
        raise RuntimeError(f"Stage-2 residual mismatch: {len(residual_rnums)}")

    # F1 anchors: R1-R3250, logical value >=8 bytes, exactly once in PC scope,
    # exactly once among all 3,803 JP logical entries, and no nonzero bytes after
    # the first PC NUL.
    anchors = {}
    for rnum in range(1, PC_SCOPE_END + 1):
        logical, post_nul_ok = logicals[rnum - 1]
        if (
            post_nul_ok
            and len(logical) >= MIN_ANCHOR_BYTES
            and pc_scope_values[logical] == 1
            and jp_value_count[logical] == 1
        ):
            jp_id = jp_by_value[logical][0]
            anchors[rnum] = (jp_id, jp_id - rnum)

    # Enumerate all valid PC-row -> JP-ID logical correspondences inside R1-R3250.
    positions_by_delta = defaultdict(list)
    for rnum in range(1, PC_SCOPE_END + 1):
        logical, post_nul_ok = logicals[rnum - 1]
        if not post_nul_ok:
            continue
        for jp_id in jp_by_value.get(logical, ()):
            positions_by_delta[jp_id - rnum].append(rnum)

    # Search segments are maximal consecutive correspondence runs of >=5 rows
    # with >=2 valid anchors for the same delta. They do not cross a candidate
    # gap or a delta reset.
    search = []
    for delta, positions in positions_by_delta.items():
        positions = sorted(positions)
        if not positions:
            continue
        start = prev = positions[0]
        runs = []
        for rnum in positions[1:]:
            if rnum == prev + 1:
                prev = rnum
            else:
                if prev - start + 1 >= MIN_SEARCH_RUN:
                    runs.append((start, prev))
                start = prev = rnum
        if prev - start + 1 >= MIN_SEARCH_RUN:
            runs.append((start, prev))
        for start, end in runs:
            a = [r for r in range(start, end + 1) if r in anchors and anchors[r][1] == delta]
            if len(a) >= 2:
                search.append({
                    "search_start": start,
                    "search_end": end,
                    "delta": delta,
                    "anchors": a,
                })
    search.sort(key=lambda x: (x["search_start"], x["search_end"], x["delta"]))
    if len(search) != EXPECTED["search_segments"]:
        raise RuntimeError(f"F1 search segment mismatch: {len(search)}")

    # Historical F1 mapped only the interval bounded by first/last accepted anchors.
    trimmed = []
    for item in search:
        start = item["anchors"][0]
        end = item["anchors"][-1]
        trimmed.append({**item, "start": start, "end": end, "rows": end - start + 1})
    trimmed_rows = {r for s in trimmed for r in range(s["start"], s["end"] + 1)}
    if len(trimmed_rows) != EXPECTED["trimmed_mapped_rows"]:
        raise RuntimeError(f"F1 trimmed mapped-row mismatch: {len(trimmed_rows)}")
    trimmed_residual = trimmed_rows & residual_rnums
    if len(trimmed_residual) != EXPECTED["trimmed_residual_rows"]:
        raise RuntimeError(f"F1 trimmed residual mismatch: {len(trimmed_residual)}")

    accepted = [s for s in trimmed if s["rows"] >= MIN_FINAL_INTERVAL]
    if len(accepted) != EXPECTED["accepted_segments"]:
        raise RuntimeError(f"F1 accepted segment mismatch: {len(accepted)}")
    accepted_rows = {r for s in accepted for r in range(s["start"], s["end"] + 1)}
    if len(accepted_rows) != EXPECTED["accepted_mapped_rows"]:
        raise RuntimeError(f"F1 accepted mapped-row mismatch: {len(accepted_rows)}")
    accepted_residual = accepted_rows & residual_rnums
    rejected_residual = trimmed_residual - accepted_residual
    if len(accepted_residual) != EXPECTED["accepted_residual_rows"]:
        raise RuntimeError(f"F1 accepted residual mismatch: {len(accepted_residual)}")
    if rejected_residual != EXPECTED_REJECTED_RESIDUAL:
        raise RuntimeError(f"F1 rejected residual set mismatch: {sorted(rejected_residual)}")

    # Stable accepted segment IDs by ascending bounded interval.
    accepted.sort(key=lambda x: (x["start"], x["end"], x["delta"]))
    row_map = {}
    for seg_no, seg in enumerate(accepted, start=1):
        seg_id = f"F1S{seg_no:03d}"
        for rnum in range(seg["start"], seg["end"] + 1):
            if rnum in row_map:
                raise RuntimeError(f"F1 accepted segment overlap at R{rnum}")
            row_map[rnum] = (seg_id, seg)

    owners_by_object = defaultdict(list)
    for jp_id, off in enumerate(jp_objects):
        owners_by_object[off].append(jp_id)

    # Stage-2 target intervals for overlap proof.
    stage2_intervals = []
    for start, end, delta in STAGE2_BLOCKS:
        for rnum in range(start, end + 1):
            row = inline[rnum - 1]
            target = row["pc_location_or_index"] + delta
            stage2_intervals.append((target, target + row["length"], rnum))

    full_all = []
    padding_all = []
    for rnum in sorted(trimmed_residual):
        # Use the corresponding trimmed segment delta; intervals are non-overlapping.
        seg = next(s for s in trimmed if s["start"] <= rnum <= s["end"])
        jp_id = rnum + seg["delta"]
        row = inline[rnum - 1]
        orig = bytes.fromhex(row["original"])
        obj = jp_objects[jp_id]
        (full_all if flat[obj:obj + len(orig)] == orig else padding_all).append(rnum)
    if len(full_all) != EXPECTED["full_window_all"] or len(padding_all) != EXPECTED["padding_all"]:
        raise RuntimeError("historical F1 full-window/padding split mismatch")

    full_accepted = []
    padding_accepted = []
    capacity_fail = set()
    shared_blocker = set()

    for rnum in sorted(accepted_residual):
        seg_id, seg = row_map[rnum]
        jp_id = rnum + seg["delta"]
        row = inline[rnum - 1]
        orig = bytes.fromhex(row["original"])
        repl = bytes.fromhex(row["replacement"])
        obj = jp_objects[jp_id]
        full_guard = flat[obj:obj + len(orig)] == orig
        if not full_guard:
            padding_accepted.append(rnum)
            continue
        full_accepted.append(rnum)

        # Capacity/NUL rule: if replacement has no NUL but the PC window itself
        # contained the original terminator, the write consumes that terminator
        # and needs one extra byte. F1 canonical audit proves the four resulting
        # next bytes are occupied by the next JP object.
        if 0 not in repl and 0 in orig:
            capacity_fail.add(rnum)
            continue
        if len(owners_by_object[obj]) > 1:
            shared_blocker.add(rnum)

    if len(full_accepted) != EXPECTED["full_window_accepted"] or len(padding_accepted) != EXPECTED["padding_accepted"]:
        raise RuntimeError("accepted F1 full-window/padding split mismatch")
    if capacity_fail != EXPECTED_CAPACITY_FAIL:
        raise RuntimeError(f"capacity-fail set mismatch: {sorted(capacity_fail)}")
    if len(shared_blocker) != EXPECTED["shared_owner_blocker"]:
        raise RuntimeError(f"shared-owner blocker mismatch: {len(shared_blocker)}")

    authorized = sorted(set(full_accepted) - capacity_fail - shared_blocker)
    if len(authorized) != EXPECTED["static_authorized"]:
        raise RuntimeError(f"static authorization count mismatch: {len(authorized)}")

    # Full-window overlap proof used by V089: all 197 historical full-window rows
    # are mutually non-overlapping, and all are disjoint from Stage-2 targets.
    full_windows = []
    for rnum in full_all:
        seg = next(s for s in trimmed if s["start"] <= rnum <= s["end"])
        jp_id = rnum + seg["delta"]
        obj = jp_objects[jp_id]
        length = inline[rnum - 1]["length"]
        full_windows.append((obj, obj + length, rnum))
    for i, (a0, a1, ar) in enumerate(full_windows):
        for b0, b1, br in full_windows[i + 1:]:
            if ranges_overlap(a0, a1, b0, b1):
                raise RuntimeError(f"unexpected F1 full-window overlap R{ar}/R{br}")
        for b0, b1, br in stage2_intervals:
            if ranges_overlap(a0, a1, b0, b1):
                raise RuntimeError(f"unexpected F1/Stage2 overlap R{ar}/R{br}")

    manifest_rows = []
    for rnum in authorized:
        seg_id, seg = row_map[rnum]
        jp_id = rnum + seg["delta"]
        row = inline[rnum - 1]
        orig = bytes.fromhex(row["original"])
        repl = bytes.fromhex(row["replacement"])
        logical, post_nul_ok = logicals[rnum - 1]
        obj = jp_objects[jp_id]
        owners = owners_by_object[obj]
        domain = loc["domain_class_by_object"].get(f"0x{obj:X}", "UNKNOWN")
        if domain != "JP_ONLY" or len(owners) != 1 or owners[0] != jp_id:
            raise RuntimeError(f"authorization owner/domain failure at R{rnum}")
        if flat[obj:obj + len(orig)] != orig:
            raise RuntimeError(f"authorization original guard failure at R{rnum}")

        repl_nul = repl.find(b"\0")
        if repl_nul >= 0:
            terminator_offset = obj + repl_nul
            terminator_mode = "REPLACEMENT_CONTAINS_NUL"
            terminator_guard = True
        else:
            # Safe authorized no-NUL replacement must leave the existing target
            # NUL immediately after the unchanged-length write window untouched.
            if 0 in orig or flat[obj + len(repl)] != 0:
                raise RuntimeError(f"authorization NUL preservation failure at R{rnum}")
            terminator_offset = obj + len(repl)
            terminator_mode = "EXISTING_NUL_AFTER_WRITE"
            terminator_guard = True

        action_id = f"F1STATIC:R{rnum:04d}:ID{jp_id:04d}"
        manifest_rows.append({
            "schema": "F1_STATIC_WRITE_AUTHORIZATION_V1",
            "authorization_action_id": action_id,
            "source_family": "inline",
            "source_id": row["source_id"],
            "pc_record": f"R{rnum}",
            "pc_rva": row["pc_location_or_index"],
            "pc_rva_hex": row["pc_location_hex"],
            "original_hex": row["original"],
            "replacement_hex": row["replacement"],
            "window_length": row["length"],
            "pc_logical_length": len(logical),
            "post_nul_zero_only": post_nul_ok,
            "f1_segment_id": seg_id,
            "f1_search_start": seg["search_start"],
            "f1_search_end": seg["search_end"],
            "f1_interval_start": seg["start"],
            "f1_interval_end": seg["end"],
            "f1_interval_rows": seg["rows"],
            "f1_delta": seg["delta"],
            "f1_first_anchor": seg["anchors"][0],
            "f1_last_anchor": seg["anchors"][-1],
            "f1_anchor_count": len(seg["anchors"]),
            "localization_id": jp_id,
            "jp_source_slot": LOCALIZATION_JP_BASE + jp_id * 8,
            "jp_source_slot_hex": f"0x{LOCALIZATION_JP_BASE + jp_id * 8:X}",
            "runtime_destination_cell": LOCALIZATION_DEST_BASE + jp_id * 8,
            "runtime_destination_cell_hex": f"0x{LOCALIZATION_DEST_BASE + jp_id * 8:X}",
            "target_object": obj,
            "target_object_hex": f"0x{obj:X}",
            "target_logical_hex": jp_strings[jp_id].hex(),
            "target_logical_length": len(jp_strings[jp_id]),
            "language_domain": domain,
            "logical_owner_ids": owners,
            "logical_owner_count": len(owners),
            "storage_class": "STATIC_RODATA",
            "window_object_cardinality": "1:1",
            "write_start": obj,
            "write_start_hex": f"0x{obj:X}",
            "write_end_exclusive": obj + len(repl),
            "write_end_exclusive_hex": f"0x{obj + len(repl):X}",
            "original_guard_exact": True,
            "terminator_mode": terminator_mode,
            "terminator_offset": terminator_offset,
            "terminator_offset_hex": f"0x{terminator_offset:X}",
            "terminator_preserved": terminator_guard,
            "f1_full_window_overlap": False,
            "stage2_overlap": False,
            "terminal_disposition_overlay": "DIRECT_PORT",
            "action_family": "F1_LOCALIZATION_STATIC_DIRECT",
            "action_status": "STATIC_WRITE_AUTHORIZED_NOT_IMPLEMENTED",
            "apply_priority": 0,
            "runtime_validation_required": False,
            "evidence_ids": ["V088", "V089", "V093", "V094"],
            "evidence_scope": "STATIC_ONLY",
            "falsification_condition": "Any canonical input/hash, F1 selector count, target ID/object, language ownership, original guard, NUL/capacity, owner cardinality, or overlap proof changes or fails.",
        })

    args.manifest.parent.mkdir(parents=True, exist_ok=True)
    manifest_bytes = b"".join(
        (json.dumps(row, ensure_ascii=False, sort_keys=True) + "\n").encode("utf-8")
        for row in manifest_rows
    )
    manifest_content_sha256 = hashlib.sha256(manifest_bytes).hexdigest()
    if args.manifest.suffix == ".gz":
        with args.manifest.open("wb") as raw:
            with gzip.GzipFile(filename="", mode="wb", fileobj=raw, mtime=0, compresslevel=9) as gz:
                gz.write(manifest_bytes)
        manifest_transport_format = "DETERMINISTIC_GZIP_JSONL"
        manifest_transport_status = "HISTORICAL_CANONICAL_TRANSPORT_PROVENANCE"
    else:
        args.manifest.write_bytes(manifest_bytes)
        manifest_transport_format = "PLAIN_JSONL"
        manifest_transport_status = "GENERATED_OUTPUT_TRANSPORT"

    summary = {
        "schema": "F1_STATIC_WRITE_AUTHORIZATION_SUMMARY_V2",
        "artifact_role": "HISTORICAL_REPORTING_VIEW_NOT_CANONICAL_ACTION_AUTHORITY",
        "canonical_main_sha256": CANONICAL_MAIN_SHA256,
        "canonical_build_id": build_id.hex().upper(),
        "source_ledger_sha256": CANONICAL_SOURCE_LEDGER_SHA256,
        "exceptions_sha256": CANONICAL_EXCEPTIONS_SHA256,
        "localization_inventory_sha256": CANONICAL_LOCALIZATION_INVENTORY_SHA256,
        "anchor_rule": {
            "pc_scope": "R1-R3250",
            "minimum_anchor_bytes": MIN_ANCHOR_BYTES,
            "pc_scope_occurrences": 1,
            "jp_logical_entry_occurrences": 1,
            "post_first_nul": "zero-only",
        },
        "segment_rule": {
            "minimum_search_run_rows": MIN_SEARCH_RUN,
            "minimum_anchors": 2,
            "mapping": "localization_id = pc_record_number + segment_delta",
            "gap_or_delta_reset_crossing": False,
            "mapped_interval": "first accepted anchor through last accepted anchor",
            "minimum_final_interval_rows": MIN_FINAL_INTERVAL,
        },
        "counts": {
            "search_segments": len(search),
            "trimmed_mapped_rows": len(trimmed_rows),
            "trimmed_residual_rows": len(trimmed_residual),
            "accepted_segments": len(accepted),
            "accepted_mapped_rows": len(accepted_rows),
            "accepted_residual_rows": len(accepted_residual),
            "rejected_residual_rows": len(rejected_residual),
            "full_window_all": len(full_all),
            "padding_all": len(padding_all),
            "full_window_accepted": len(full_accepted),
            "padding_accepted": len(padding_accepted),
            "capacity_fail": len(capacity_fail),
            "shared_owner_blocker": len(shared_blocker),
            "static_authorized": len(manifest_rows),
        },
        "capacity_fail_rows": [f"R{x}" for x in sorted(capacity_fail)],
        "shared_owner_blocker_rows": [f"R{x}" for x in sorted(shared_blocker)],
        "rejected_residual_rows": [f"R{x}" for x in sorted(rejected_residual)],
        "authorized_source_ids_sha256": hashlib.sha256("\n".join(row["source_id"] for row in manifest_rows).encode()).hexdigest(),
        "manifest_content_sha256": manifest_content_sha256,
        "manifest_content_sha256_semantics": "SEMANTIC_LOGICAL_JSONL_SHA256",
        "manifest_transport": {
            "format": manifest_transport_format,
            "sha256": sha256_file(args.manifest),
            "status": manifest_transport_status,
        },
    }
    args.summary.write_text(json.dumps(summary, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(summary, ensure_ascii=False, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
