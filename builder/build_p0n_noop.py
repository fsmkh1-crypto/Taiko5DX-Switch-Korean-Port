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
    open_payload,
    sha256_file,
    write_ips,
)
from t5k import extract_t5k_rcdata, parse_t5k_resource, select_safe_inline_patches

TEST_ID = "P0N"


def build(args: argparse.Namespace) -> None:
    dump_root = args.switch_dump.resolve()
    main_path = find_main(dump_root)
    romfs_root = find_romfs(dump_root)
    build_id, flat = decompress_nso(main_path)
    if build_id != BUILD_ID_FULL:
        raise RuntimeError(f"Unexpected Switch main Build ID: {build_id.hex()}")

    payload = open_payload(args.pc_patcher)
    t5k = parse_t5k_resource(extract_t5k_rcdata(payload.read("dinput8.dll")))
    historical, stats = select_safe_inline_patches(
        flat,
        t5k.inline_records,
        RODATA_MEM_OFF,
        RODATA_MEM_OFF + RODATA_SIZE,
    )
    if len(historical) != 5519:
        raise RuntimeError(f"P0N requires historical 5,519-set; got {len(historical)}")

    out = args.output.resolve()
    if out.exists():
        shutil.rmtree(out)
    mod_root = out / args.mod_name
    exefs_out = mod_root / "exefs"
    romfs_out = mod_root / "romfs"

    plan = PatchPlan(flat)
    plan.add(GETFONT_OFFSET, GETFONT_ORIGINAL, GETFONT_KOREAN, "runtime_page_mapper")
    for offset, original, _replacement in historical:
        plan.add(offset, original, original, "P0N_inline_noop")

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

    # Reparse the emitted classic IPS and prove that every no-op record writes
    # the exact original flat-image bytes. This checks the generator output,
    # while Eden runtime testing checks the loader/application path.
    blob = ips_path.read_bytes()
    if not blob.startswith(b"PATCH") or not blob.endswith(b"EOF"):
        raise RuntimeError("Malformed P0N IPS envelope")
    pos = 5
    parsed: list[tuple[int, bytes]] = []
    while blob[pos:pos + 3] != b"EOF":
        offset = int.from_bytes(blob[pos:pos + 3], "big")
        length = int.from_bytes(blob[pos + 3:pos + 5], "big")
        pos += 5
        data = blob[pos:pos + length]
        pos += length
        if len(data) != length:
            raise RuntimeError("Truncated P0N IPS record")
        parsed.append((offset, data))

    if len(parsed) != 5520:
        raise RuntimeError(f"Expected 5,520 P0N IPS records, got {len(parsed)}")

    expected = sorted((off, repl) for off, _orig, repl, _module in plan.records)
    if parsed != expected:
        raise RuntimeError("P0N emitted IPS does not round-trip to the patch plan")

    noop_checked = 0
    for offset, data in parsed:
        if offset == GETFONT_OFFSET:
            continue
        if flat[offset:offset + len(data)] != data:
            raise RuntimeError(f"P0N record at 0x{offset:X} is not a true no-op")
        noop_checked += 1
    if noop_checked != 5519:
        raise RuntimeError(f"Expected 5,519 verified no-op records, got {noop_checked}")

    report = {
        "test_id": TEST_ID,
        "purpose": "Distinguish large-IPS/build-loader failure from inline-content failure.",
        "switch_main": str(main_path),
        "switch_build_id": BUILD_ID_NAME,
        "historical_selector": stats,
        "noop_inline_records": noop_checked,
        "ips_records_total": len(parsed),
        "romfs_payload_files_copied": copied,
        "roundtrip_patch_plan_verified": True,
        "interpretation": {
            "boots_like_no_inline": "Large IPS record count/format/application is not the current failure cause; proceed to MVI content tests.",
            "fails": "Stop semantic-validator work and investigate IPS/build-loader/application path first.",
        },
    }
    (out / "P0N_BUILD_REPORT.json").write_text(
        json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    print(json.dumps(report, ensure_ascii=False, indent=2))


def main() -> None:
    ap = argparse.ArgumentParser(description="Build P0N: NO-INLINE baseline + 5,519 true no-op IPS records")
    ap.add_argument("--switch-dump", required=True, type=Path)
    ap.add_argument("--pc-patcher", required=True, type=Path)
    ap.add_argument("--output", required=True, type=Path)
    ap.add_argument("--mod-name", default="Taiko5DX_KR_DBG_P0N")
    build(ap.parse_args())


if __name__ == "__main__":
    main()
