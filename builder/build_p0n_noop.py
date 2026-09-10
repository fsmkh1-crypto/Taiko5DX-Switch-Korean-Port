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
    IPS_IMAGE_HEADER_SIZE,
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
from t5k import extract_t5k_rcdata, parse_t5k_resource, select_safe_inline_patches

TEST_ID = "P0N2"


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
        raise RuntimeError(f"P0N2 requires historical 5,519-set; got {len(historical)}")

    out = args.output.resolve()
    if out.exists():
        shutil.rmtree(out)
    mod_root = out / args.mod_name
    exefs_out = mod_root / "exefs"
    romfs_out = mod_root / "romfs"

    plan = PatchPlan(flat)
    plan.add(GETFONT_OFFSET, GETFONT_ORIGINAL, GETFONT_KOREAN, "runtime_page_mapper")
    for offset, original, _replacement in historical:
        plan.add(offset, original, original, "P0N2_inline_noop")

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

    blob = ips_path.read_bytes()
    if not blob.startswith(b"PATCH") or not blob.endswith(b"EOF"):
        raise RuntimeError("Malformed P0N2 IPS envelope")
    pos = 5
    parsed: list[tuple[int, bytes]] = []
    while blob[pos:pos + 3] != b"EOF":
        ips_offset = int.from_bytes(blob[pos:pos + 3], "big")
        length = int.from_bytes(blob[pos + 3:pos + 5], "big")
        pos += 5
        data = blob[pos:pos + length]
        pos += length
        if len(data) != length:
            raise RuntimeError("Truncated P0N2 IPS record")
        parsed.append((ips_offset, data))

    if len(parsed) != 5520:
        raise RuntimeError(f"Expected 5,520 P0N2 IPS records, got {len(parsed)}")

    expected = sorted(
        (mapped_to_ips_offset(off), repl)
        for off, _orig, repl, _module in plan.records
    )
    if parsed != expected:
        raise RuntimeError("P0N2 emitted IPS does not round-trip to mapped plan + 0x100")

    noop_checked = 0
    mapper_checked = False
    for ips_offset, data in parsed:
        mapped_offset = ips_offset - IPS_IMAGE_HEADER_SIZE
        if mapped_offset == GETFONT_OFFSET:
            if data != GETFONT_KOREAN:
                raise RuntimeError("P0N2 page mapper payload mismatch")
            mapper_checked = True
            continue
        if mapped_offset < 0 or flat[mapped_offset:mapped_offset + len(data)] != data:
            raise RuntimeError(
                f"P0N2 record IPS 0x{ips_offset:X} / mapped 0x{mapped_offset:X} is not a true no-op"
            )
        noop_checked += 1

    if not mapper_checked:
        raise RuntimeError("P0N2 page mapper record missing")
    if noop_checked != 5519:
        raise RuntimeError(f"Expected 5,519 verified no-op records, got {noop_checked}")

    report = {
        "test_id": TEST_ID,
        "purpose": "Corrected Eden build-layer control after discovering the required +0x100 NSO-header IPS shift.",
        "switch_main": str(main_path),
        "switch_build_id": BUILD_ID_NAME,
        "ips_offset_shift": IPS_IMAGE_HEADER_SIZE,
        "page_mapper_mapped_offset": GETFONT_OFFSET,
        "page_mapper_ips_offset": mapped_to_ips_offset(GETFONT_OFFSET),
        "historical_selector": stats,
        "noop_inline_records": noop_checked,
        "ips_records_total": len(parsed),
        "romfs_payload_files_copied": copied,
        "roundtrip_patch_plan_verified": True,
        "interpretation": {
            "boots_like_no_inline": "Corrected large no-op IPS path works; old P0N freeze was explained by the offset bug. Proceed to corrected semantic/MVI tests.",
            "fails": "The +0x100 correction alone is insufficient; isolate corrected page mapper versus no-op record count/application next.",
        },
    }
    (out / "P0N2_BUILD_REPORT.json").write_text(
        json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    print(json.dumps(report, ensure_ascii=False, indent=2))


def main() -> None:
    ap = argparse.ArgumentParser(description="Build P0N2: corrected Eden +0x100 offsets, NO-INLINE baseline + 5,519 true no-op records")
    ap.add_argument("--switch-dump", required=True, type=Path)
    ap.add_argument("--pc-patcher", required=True, type=Path)
    ap.add_argument("--output", required=True, type=Path)
    ap.add_argument("--mod-name", default="Taiko5DX_KR_DBG_P0N2")
    build(ap.parse_args())


if __name__ == "__main__":
    main()
