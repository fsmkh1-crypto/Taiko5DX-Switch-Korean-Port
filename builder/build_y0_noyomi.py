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
from t5k import extract_t5k_rcdata, parse_t5k_resource, select_safe_inline_patches

TEST_ID = "Y0"

# Direct callers of the shared name+yomi renderer that explicitly enable the
# auxiliary reading line with `mov w6,#1` before BL 0x45B0F8.
YOMI_ENABLE_MAPPED_OFFSETS = (
    0x2A0ABC,
    0x2A565C,
    0x2A6F4C,
    0x2A7720,
    0x2A7FE4,
    0x2ADE5C,
    0x2BC1A0,
    0x2BD5C8,
)
MOV_W6_1 = bytes.fromhex("26008052")
MOV_W6_WZR = bytes.fromhex("e6031f2a")


def is_halfwidth_yomi_field(original: bytes) -> bool:
    """Diagnostic classifier for historical inline fields made only of halfwidth kana + NUL padding."""
    nonzero = [b for b in original if b]
    return bool(nonzero) and all(0xA1 <= b <= 0xDF for b in nonzero)


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
        raise RuntimeError(f"Y0 requires the historical 5,519-set; got {len(historical)}")

    kept: list[tuple[int, bytes, bytes]] = []
    removed_yomi: list[tuple[int, bytes, bytes]] = []
    for offset, original, replacement in historical:
        if is_halfwidth_yomi_field(original):
            removed_yomi.append((offset, original, replacement))
        else:
            kept.append((offset, original, replacement))

    if len(removed_yomi) != 2099 or len(kept) != 3420:
        raise RuntimeError(
            f"Unexpected Y0 split: removed_yomi={len(removed_yomi)}, kept={len(kept)}"
        )

    out = args.output.resolve()
    if out.exists():
        shutil.rmtree(out)
    mod_root = out / args.mod_name
    exefs_out = mod_root / "exefs"
    romfs_out = mod_root / "romfs"

    plan = PatchPlan(flat)
    plan.add(GETFONT_OFFSET, GETFONT_ORIGINAL, GETFONT_KOREAN, "runtime_page_mapper")

    for offset, original, replacement in kept:
        plan.add(offset, original, replacement, "historical_inline_non_yomi")

    for offset in YOMI_ENABLE_MAPPED_OFFSETS:
        plan.add(offset, MOV_W6_1, MOV_W6_WZR, "disable_visible_yomi_line")

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

    # Reparse the emitted classic IPS and verify the Eden coordinate system.
    blob = ips_path.read_bytes()
    if not blob.startswith(b"PATCH") or not blob.endswith(b"EOF"):
        raise RuntimeError("Malformed Y0 IPS envelope")
    pos = 5
    parsed: list[tuple[int, bytes]] = []
    while blob[pos:pos + 3] != b"EOF":
        ips_offset = int.from_bytes(blob[pos:pos + 3], "big")
        length = int.from_bytes(blob[pos + 3:pos + 5], "big")
        pos += 5
        if length == 0:
            raise RuntimeError("Y0 builder does not expect RLE records")
        data = blob[pos:pos + length]
        pos += length
        if len(data) != length:
            raise RuntimeError("Truncated Y0 IPS record")
        parsed.append((ips_offset, data))

    expected = sorted(
        (mapped_to_ips_offset(off), replacement)
        for off, _original, replacement, _module in plan.records
    )
    if parsed != expected:
        raise RuntimeError("Y0 emitted IPS does not round-trip to mapped plan + 0x100")

    report = {
        "test_id": TEST_ID,
        "purpose": "Preserve internal Japanese yomi while suppressing the unnecessary visible reading line in Korean UI.",
        "historical_selector": stats,
        "historical_real_inline_records": 5519,
        "removed_halfwidth_yomi_inline_records": len(removed_yomi),
        "retained_non_yomi_inline_records": len(kept),
        "yomi_ui_callsite_patches": len(YOMI_ENABLE_MAPPED_OFFSETS),
        "yomi_draw_routine_mapped": "0x45B0F8",
        "callsite_mapped_offsets": [f"0x{x:X}" for x in YOMI_ENABLE_MAPPED_OFFSETS],
        "callsite_patch": {
            "before": MOV_W6_1.hex(),
            "before_asm": "mov w6, #1",
            "after": MOV_W6_WZR.hex(),
            "after_asm": "mov w6, wzr",
        },
        "ips_records_total": len(parsed),
        "romfs_payload_files_copied": copied,
        "ips_coordinate_rule": "emitted = mapped + 0x100",
        "roundtrip_verified": True,
        "expected_runtime": [
            "Korean main names remain visible",
            "garbled small reading/yomi line disappears on targeted name UIs",
            "original Japanese halfwidth yomi remains available internally",
        ],
        "non_goals": [
            "This diagnostic does not recover repeated short UI tokens such as はい/年/月/日/貫/文/城.",
            "This diagnostic does not certify the retained historical inline set as release-safe.",
        ],
    }
    (out / "Y0_BUILD_REPORT.json").write_text(
        json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8"
    )

    print(json.dumps(report, ensure_ascii=False, indent=2))


def main() -> None:
    ap = argparse.ArgumentParser(description="Build Y0: corrected Eden Korean diagnostic with internal yomi preserved and visible yomi suppressed")
    ap.add_argument("--switch-dump", required=True, type=Path)
    ap.add_argument("--pc-patcher", required=True, type=Path)
    ap.add_argument("--output", required=True, type=Path)
    ap.add_argument("--mod-name", default="Taiko5DX_KR_DBG_Y0")
    build(ap.parse_args())


if __name__ == "__main__":
    main()
