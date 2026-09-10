#!/usr/bin/env python3
from __future__ import annotations

import argparse
import bisect
import hashlib
import json
from collections import Counter, defaultdict
from pathlib import Path

from build import RODATA_MEM_OFF, RODATA_SIZE, decompress_nso, open_payload
from t5k import extract_t5k_rcdata, find_pattern_occurrences, parse_t5k_resource, select_safe_inline_patches

MAPPING_COUNT_UTF16_TO_GAME_OFF = 0x4303AC
MAPPING_COUNT_GAME_TO_UTF16_OFF = 0x430624
EXPECTED_MOV_7494_W26 = bytes.fromhex("daa88352")
EXPECTED_MOV_7494_W24 = bytes.fromhex("d8a88352")


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for block in iter(lambda: f.read(1024 * 1024), b""):
            h.update(block)
    return h.hexdigest()


def strict_lis_length(values: list[int]) -> int:
    tails: list[int] = []
    for value in values:
        pos = bisect.bisect_left(tails, value)
        if pos == len(tails):
            tails.append(value)
        else:
            tails[pos] = value
    return len(tails)


def monotonic_run_lengths(values: list[int]) -> list[int]:
    if not values:
        return []
    out: list[int] = []
    start = 0
    for i in range(1, len(values)):
        if values[i] <= values[i - 1]:
            out.append(i - start)
            start = i
    out.append(len(values) - start)
    return sorted(out, reverse=True)


def probe(args: argparse.Namespace) -> None:
    build_id, flat = decompress_nso(args.main)
    payload = open_payload(args.pc_patcher)
    dll = payload.read("dinput8.dll")
    rcdata = extract_t5k_rcdata(dll)
    t5k = parse_t5k_resource(rcdata)

    groups = defaultdict(list)
    for index, rec in enumerate(t5k.inline_records):
        groups[rec.original].append((index, rec))

    patterns = list(groups)
    occurrences = find_pattern_occurrences(flat, patterns, cap=5)
    pattern_locs = dict(zip(patterns, occurrences))

    occurrence_histogram = Counter(len(locs) for locs in occurrences)
    record_count_ge5 = sum(len(groups[p]) for p, locs in pattern_locs.items() if len(locs) >= 5)
    pattern_count_ge5 = sum(1 for locs in occurrences if len(locs) >= 5)

    unique_record_pairs: list[tuple[int, int]] = []
    unique_pattern_pairs: list[tuple[int, int]] = []
    unique_rodata_patterns = 0
    unique_outside_rodata_patterns = 0
    ro_end = RODATA_MEM_OFF + RODATA_SIZE

    for pattern, locs in pattern_locs.items():
        if len(locs) != 1:
            continue
        switch_off = locs[0]
        recs = groups[pattern]
        unique_pattern_pairs.append((min(rec.pc_rva for _, rec in recs), switch_off))
        unique_record_pairs.extend((rec.pc_rva, switch_off) for _, rec in recs)
        if RODATA_MEM_OFF <= switch_off and switch_off + len(pattern) <= ro_end:
            unique_rodata_patterns += 1
        else:
            unique_outside_rodata_patterns += 1

    unique_record_pairs.sort()
    unique_pattern_pairs.sort()
    record_switch_offsets = [off for _, off in unique_record_pairs]
    pattern_switch_offsets = [off for _, off in unique_pattern_pairs]

    nul_cover = 0
    nul_none = 0
    nul_position_changed = 0
    unique_after_full_record_nonzero = 0
    any_candidate_after_full_record_nonzero_records = 0
    candidate_instances_after_full_record_nonzero = 0

    for rec in t5k.inline_records:
        has_orig_nul = b"\x00" in rec.original
        has_repl_nul = b"\x00" in rec.replacement
        if not has_orig_nul:
            nul_none += 1
        if has_orig_nul and not has_repl_nul:
            nul_cover += 1
        if has_orig_nul and has_repl_nul and rec.original.find(b"\x00") != rec.replacement.find(b"\x00"):
            nul_position_changed += 1

        locs = pattern_locs[rec.original]
        if has_orig_nul and not has_repl_nul:
            instance_flags = [
                off + rec.length < len(flat) and flat[off + rec.length] != 0
                for off in locs
            ]
            if len(locs) == 1 and instance_flags and instance_flags[0]:
                unique_after_full_record_nonzero += 1
            if any(instance_flags):
                any_candidate_after_full_record_nonzero_records += 1
            candidate_instances_after_full_record_nonzero += sum(instance_flags)

    old_selected, old_stats = select_safe_inline_patches(
        flat,
        t5k.inline_records,
        RODATA_MEM_OFF,
        ro_end,
    )

    count_words = {
        "utf16_to_game_0x4303AC": flat[MAPPING_COUNT_UTF16_TO_GAME_OFF:MAPPING_COUNT_UTF16_TO_GAME_OFF + 4].hex(),
        "game_to_utf16_0x430624": flat[MAPPING_COUNT_GAME_TO_UTF16_OFF:MAPPING_COUNT_GAME_TO_UTF16_OFF + 4].hex(),
    }
    count_guards_pass = (
        flat[MAPPING_COUNT_UTF16_TO_GAME_OFF:MAPPING_COUNT_UTF16_TO_GAME_OFF + 4] == EXPECTED_MOV_7494_W26
        and flat[MAPPING_COUNT_GAME_TO_UTF16_OFF:MAPPING_COUNT_GAME_TO_UTF16_OFF + 4] == EXPECTED_MOV_7494_W24
    )

    report = {
        "input_identity": {
            "switch_main_sha256": sha256_file(args.main),
            "switch_build_id": build_id.hex(),
            "pc_patcher_zip_sha256": sha256_file(args.pc_patcher),
            "dinput8_sha256": hashlib.sha256(dll).hexdigest(),
            "t5k_rcdata_sha256": hashlib.sha256(rcdata).hexdigest(),
            "t5k_target_exe_size": t5k.target_exe_size,
            "t5k_target_exe_sha256": t5k.target_exe_sha256.hex(),
        },
        "canonical_units": {
            "inline_records": len(t5k.inline_records),
            "unique_original_patterns": len(patterns),
            "unique_match_records": len(unique_record_pairs),
            "unique_match_patterns": len(unique_pattern_pairs),
            "unique_rodata_patterns": unique_rodata_patterns,
            "unique_match_outside_rodata_patterns": unique_outside_rodata_patterns,
        },
        "occurrence_counts_capped_at_5": {
            "patterns_0": occurrence_histogram[0],
            "patterns_1": occurrence_histogram[1],
            "patterns_2": occurrence_histogram[2],
            "patterns_3": occurrence_histogram[3],
            "patterns_4": occurrence_histogram[4],
            "patterns_ge_5": pattern_count_ge5,
            "records_whose_pattern_occurs_ge_5": record_count_ge5,
        },
        "nul_metrics": {
            "records_original_has_nul_replacement_has_none": nul_cover,
            "records_original_has_no_nul": nul_none,
            "records_both_have_nul_but_first_nul_position_changes": nul_position_changed,
            "records_unique_match_and_byte_after_full_record_nonzero": unique_after_full_record_nonzero,
            "records_any_capped_candidate_and_byte_after_full_record_nonzero": any_candidate_after_full_record_nonzero_records,
            "capped_candidate_instances_byte_after_full_record_nonzero": candidate_instances_after_full_record_nonzero,
        },
        "collinearity_reference_only": {
            "record_level_unique_pairs": len(unique_record_pairs),
            "record_level_lis_length": strict_lis_length(record_switch_offsets),
            "record_level_lis_outside_count": len(unique_record_pairs) - strict_lis_length(record_switch_offsets),
            "record_level_top_monotonic_runs": monotonic_run_lengths(record_switch_offsets)[:20],
            "pattern_level_unique_pairs": len(unique_pattern_pairs),
            "pattern_level_lis_length": strict_lis_length(pattern_switch_offsets),
            "pattern_level_lis_outside_count": len(unique_pattern_pairs) - strict_lis_length(pattern_switch_offsets),
            "pattern_level_top_monotonic_runs": monotonic_run_lengths(pattern_switch_offsets)[:20],
            "warning": "Global LIS is a measurement/reference, not a release hard gate. Use piecewise/local structural blocks.",
        },
        "old_selector_regression": {
            **old_stats,
            "actual_selected_tuple_count": len(old_selected),
            "warning": "Historical regression only. This selector is not a safety classifier.",
        },
        "switch_mapping_lookup_guard": {
            "expected_original_mapping_count": 7494,
            "instruction_words_le": count_words,
            "guard_pass": count_guards_pass,
            "note": "Both known conversion loops still carry the original 0x1D46 (7,494) limit. Miss-path semantics require separate disassembly/provenance before deciding crash causality.",
        },
    }

    if args.pc_exe:
        report["input_identity"].update({
            "provided_pc_exe_sha256": sha256_file(args.pc_exe),
            "provided_pc_exe_size": args.pc_exe.stat().st_size,
            "provided_pc_exe_matches_t5k_target": (
                args.pc_exe.stat().st_size == t5k.target_exe_size
                and bytes.fromhex(sha256_file(args.pc_exe)) == t5k.target_exe_sha256
            ),
        })

    args.report.parent.mkdir(parents=True, exist_ok=True)
    args.report.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps(report, ensure_ascii=False, indent=2))


def main() -> None:
    ap = argparse.ArgumentParser(description="Reproducible Phase-0 measurements for Taiko5DX inline-port diagnosis")
    ap.add_argument("--main", type=Path, required=True, help="Switch v1.1.3 compressed ExeFS/main NSO")
    ap.add_argument("--pc-patcher", type=Path, required=True, help="Taiko5DX_Korean_Patcher_v1.02.zip")
    ap.add_argument("--pc-exe", type=Path, help="Optional PC original executable; compared against the T5K target identity")
    ap.add_argument("--report", type=Path, required=True, help="Output JSON report")
    probe(ap.parse_args())


if __name__ == "__main__":
    main()
