#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import shutil
from pathlib import Path

from build import (
    BUILD_ID_FULL,
    BUILD_ID_NAME,
    GETFONT_KOREAN,
    GETFONT_OFFSET,
    GETFONT_ORIGINAL,
    PATCHED_FONT_SHA256,
    RODATA_MEM_OFF,
    RODATA_SIZE,
    PatchPlan,
    decompress_nso,
    find_main,
    find_romfs,
    mapped_to_ips_offset,
    open_payload,
    sha256_file,
    write_ips,
)
from t5k import extract_t5k_rcdata, parse_t5k_resource


def _find_all(haystack: bytes, needle: bytes, cap: int = 3) -> list[int]:
    out: list[int] = []
    pos = 0
    while len(out) < cap:
        hit = haystack.find(needle, pos)
        if hit < 0:
            break
        out.append(hit)
        pos = hit + 1
    return out


def build(args: argparse.Namespace) -> None:
    dump_root = args.switch_dump.resolve()
    main_path = find_main(dump_root)
    romfs_root = find_romfs(dump_root)
    build_id, flat = decompress_nso(main_path)
    if build_id != BUILD_ID_FULL:
        raise RuntimeError(f"Unexpected Switch main Build ID: {build_id.hex()}")

    payload = open_payload(args.pc_patcher)
    t5k = parse_t5k_resource(extract_t5k_rcdata(payload.read("dinput8.dll")))

    requested = sorted(set(args.record_id))
    selected: list[dict[str, object]] = []
    for record_id in requested:
        if not 1 <= record_id <= len(t5k.inline_records):
            raise RuntimeError(f"record ID out of range: {record_id}")
        rec = t5k.inline_records[record_id - 1]
        locs = _find_all(flat, rec.original, cap=3)
        if len(locs) != 1:
            raise RuntimeError(
                f"R{record_id:06d}: MVI builder requires one exact Switch occurrence; got {len(locs)}+"
                if len(locs) == 3 else
                f"R{record_id:06d}: MVI builder requires one exact Switch occurrence; got {len(locs)}"
            )
        mapped = locs[0]
        if not (RODATA_MEM_OFF <= mapped and mapped + rec.length <= RODATA_MEM_OFF + RODATA_SIZE):
            raise RuntimeError(f"R{record_id:06d}: unique occurrence is outside Switch rodata at 0x{mapped:X}")
        selected.append({
            "record_id": record_id,
            "pc_rva": rec.pc_rva,
            "length": rec.length,
            "mapped_offset": mapped,
            "ips_offset": mapped_to_ips_offset(mapped),
            "original_hex": rec.original.hex(),
            "replacement_hex": rec.replacement.hex(),
            "record": rec,
        })

    out = args.output.resolve()
    if out.exists():
        shutil.rmtree(out)
    mod_root = out / args.mod_name
    exefs_out = mod_root / "exefs"
    romfs_out = mod_root / "romfs"

    plan = PatchPlan(flat)
    plan.add(GETFONT_OFFSET, GETFONT_ORIGINAL, GETFONT_KOREAN, "runtime_page_mapper")
    for item in selected:
        rec = item["record"]
        assert hasattr(rec, "original")
        plan.add(
            int(item["mapped_offset"]),
            rec.original,
            rec.replacement,
            f"MVI_R{int(item['record_id']):06d}",
        )

    ips_path = exefs_out / f"{BUILD_ID_NAME}.ips"
    write_ips(plan.records, ips_path)

    copied = 0
    for name in payload.namelist():
        if not name.startswith("data/") or name.endswith("/"):
            continue
        rel = Path(name[5:])
        if rel.as_posix() == "CMENU/CWTDAT_JP.TR5":
            continue
        dst = romfs_out / rel
        dst.parent.mkdir(parents=True, exist_ok=True)
        dst.write_bytes(payload.read(name))
        copied += 1

    patched_font = romfs_out / "FONT" / "FONT_JPN.G1T"
    if sha256_file(patched_font) != PATCHED_FONT_SHA256:
        raise RuntimeError("Patched font hash guard failed")

    report_records = []
    for item in selected:
        report_records.append({k: v for k, v in item.items() if k != "record"})
    report = {
        "status": "ok",
        "test_id": args.test_id,
        "purpose": "Minimal Viable Inline diagnostic using corrected Eden/Yuzu +0x100 IPS coordinates.",
        "switch_build_id": BUILD_ID_NAME,
        "romfs_payload_files_copied": copied,
        "ips_records_total": len(plan.records),
        "page_mapper_mapped_offset": GETFONT_OFFSET,
        "page_mapper_ips_offset": mapped_to_ips_offset(GETFONT_OFFSET),
        "inline_records": report_records,
        "warning": "MVI inclusion is diagnostic only and does not promote a record to release SAFE.",
    }
    (out / f"{args.test_id}_BUILD_REPORT.json").write_text(
        json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    print(json.dumps(report, ensure_ascii=False, indent=2))


def main() -> None:
    ap = argparse.ArgumentParser(description="Build corrected-offset Minimal Viable Inline Eden diagnostic mods")
    ap.add_argument("--switch-dump", required=True, type=Path)
    ap.add_argument("--pc-patcher", required=True, type=Path)
    ap.add_argument("--output", required=True, type=Path)
    ap.add_argument("--record-id", required=True, action="append", type=int,
                    help="1-based T5K inline record ID; repeat for 10/100-record MVI builds")
    ap.add_argument("--test-id", required=True)
    ap.add_argument("--mod-name", required=True)
    build(ap.parse_args())


if __name__ == "__main__":
    main()
