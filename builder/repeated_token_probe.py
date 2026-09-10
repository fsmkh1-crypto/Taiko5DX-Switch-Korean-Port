#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from pathlib import Path

from build import RODATA_MEM_OFF, RODATA_SIZE, decompress_nso, find_main, open_payload
from t5k import extract_t5k_rcdata, parse_t5k_resource

TARGETS = ("はい", "いいえ", "年", "月", "日", "貫", "文", "城", "清洲")


def all_occurrences(haystack: bytes, needle: bytes) -> list[int]:
    out: list[int] = []
    start = 0
    while True:
        pos = haystack.find(needle, start)
        if pos < 0:
            return out
        out.append(pos)
        start = pos + 1


def pointer_refs(flat: bytes, target: int) -> list[int]:
    return all_occurrences(flat, target.to_bytes(8, "little"))


def main() -> None:
    ap = argparse.ArgumentParser(description="Probe repeated short UI tokens as Switch string objects, not raw substring matches")
    ap.add_argument("--switch-dump", required=True, type=Path)
    ap.add_argument("--pc-patcher", required=True, type=Path)
    ap.add_argument("--output", type=Path)
    args = ap.parse_args()

    _build_id, flat = decompress_nso(find_main(args.switch_dump.resolve()))
    payload = open_payload(args.pc_patcher)
    t5k = parse_t5k_resource(extract_t5k_rcdata(payload.read("dinput8.dll")))

    ro_start = RODATA_MEM_OFF
    ro_end = RODATA_MEM_OFF + RODATA_SIZE
    results: dict[str, object] = {}

    for text in TARGETS:
        raw = text.encode("cp932")
        raw_ro = [p for p in all_occurrences(flat, raw) if ro_start <= p < ro_end]
        standalone = [
            p for p in raw_ro
            if p > ro_start
            and p + len(raw) < ro_end
            and flat[p - 1] == 0
            and flat[p + len(raw)] == 0
        ]

        # T5K may store the object with trailing NUL/padding rather than only the visible bytes.
        pc_records = []
        for idx, rec in enumerate(t5k.inline_records, start=1):
            visible = rec.original.rstrip(b"\x00")
            if visible == raw:
                pc_records.append({
                    "record_id": idx,
                    "pc_rva": f"0x{rec.pc_rva:X}",
                    "length": rec.length,
                    "original_hex": rec.original.hex(),
                    "replacement_hex": rec.replacement.hex(),
                })

        results[text] = {
            "raw_hex": raw.hex(),
            "raw_rodata_occurrence_count": len(raw_ro),
            "raw_rodata_occurrences": [f"0x{x:X}" for x in raw_ro],
            "nul_delimited_standalone_count": len(standalone),
            "nul_delimited_standalone": [
                {
                    "mapped_offset": f"0x{x:X}",
                    "pointer_refs": [f"0x{r:X}" for r in pointer_refs(flat, x)],
                }
                for x in standalone
            ],
            "pc_t5k_records": pc_records,
            "pc_replacements_agree": len({r["replacement_hex"] for r in pc_records}) <= 1,
        }

    # `清洲` is stored as a padded fixed-field object on both sides, so report exact
    # padded candidates for its T5K records in addition to raw visible substring hits.
    kiy = results["清洲"]
    padded = []
    for idx, rec in enumerate(t5k.inline_records, start=1):
        if rec.original.rstrip(b"\x00") != "清洲".encode("cp932"):
            continue
        locs = [p for p in all_occurrences(flat, rec.original) if ro_start <= p < ro_end]
        padded.append({
            "record_id": idx,
            "pattern_hex": rec.original.hex(),
            "replacement_hex": rec.replacement.hex(),
            "switch_exact_padded_occurrences": [f"0x{x:X}" for x in locs],
        })
    kiy["padded_field_evidence"] = padded

    report = {
        "purpose": "Separate true Switch string objects from substring collisions for repeated short T5K patterns.",
        "coordinate_system": "mapped flat NSO offsets; add 0x100 only when serializing Eden classic IPS",
        "results": results,
    }

    text = json.dumps(report, ensure_ascii=False, indent=2)
    if args.output:
        args.output.write_text(text, encoding="utf-8")
    print(text)


if __name__ == "__main__":
    main()
