from __future__ import annotations

import argparse
import hashlib
import json
import shutil
import zipfile
from pathlib import Path

from build import (
    BUILD_ID_FULL,
    BUILD_ID_NAME,
    GETFONT_KOREAN,
    GETFONT_OFFSET,
    GETFONT_ORIGINAL,
    IPS_IMAGE_HEADER_SIZE,
    PATCHED_FONT_SHA256,
    PatchPlan,
    decompress_nso,
    mapped_to_ips_offset,
    open_payload,
    sha256_file,
    write_ips,
)
from t5k import extract_t5k_rcdata, parse_t5k_resource

TEST_ID = "DCTRL5"
TITLE_ID = "0100346017304000"
SWITCH_VERSION = "1.1.3"

PC_PATCH_SHA256 = "df1b62de95e992369e9686c9731d814e7a7e4634888f610430635429e24f7cec"
PC_DLL_SHA256 = "ffe7e9da8e00c96bec631b45a3e9c4d3f314551623351f3e7024e0318913c6b7"
T5K_SHA256 = "5c6f4eba8c6f0516365e4518f27e9d8c840aead463b5a2938dd1e08b99726d29"
SWITCH_MAIN_COMPRESSED_SHA256 = "b366e692208f3c0cc18bc1884ef95689b6b11d722fa2d749b8500abccbc3109b"

TARGETS = (
    ("月", 0x68925A),
    ("年", 0x69785A),
    ("はい", 0x6A15A5),
    ("城", 0x6A15DC),
    ("日", 0x6A3CC6),
)


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def parse_ips(blob: bytes) -> list[tuple[int, bytes]]:
    if not blob.startswith(b"PATCH") or not blob.endswith(b"EOF"):
        raise RuntimeError("invalid classic IPS envelope")
    pos = 5
    out: list[tuple[int, bytes]] = []
    while blob[pos:pos + 3] != b"EOF":
        if pos + 5 > len(blob):
            raise RuntimeError("truncated IPS record header")
        off = int.from_bytes(blob[pos:pos + 3], "big")
        size = int.from_bytes(blob[pos + 3:pos + 5], "big")
        pos += 5
        if size == 0:
            if pos + 3 > len(blob):
                raise RuntimeError("truncated IPS RLE record")
            run = int.from_bytes(blob[pos:pos + 2], "big")
            value = blob[pos + 2]
            pos += 3
            data = bytes([value]) * run
        else:
            data = blob[pos:pos + size]
            if len(data) != size:
                raise RuntimeError("truncated IPS payload")
            pos += size
        out.append((off, data))
    if pos + 3 != len(blob):
        raise RuntimeError("unexpected trailing bytes after IPS EOF")
    return out


def deterministic_zip_dir(root: Path, out_zip: Path) -> None:
    out_zip.parent.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(out_zip, "w", compression=zipfile.ZIP_DEFLATED, compresslevel=9) as zout:
        for path in sorted(p for p in root.rglob("*") if p.is_file()):
            arcname = path.relative_to(root.parent).as_posix()
            info = zipfile.ZipInfo(arcname, date_time=(1980, 1, 1, 0, 0, 0))
            info.compress_type = zipfile.ZIP_DEFLATED
            info.external_attr = 0o100644 << 16
            zout.writestr(info, path.read_bytes())


def select_source_grounded_replacement(t5k, text: str) -> tuple[bytes, list[dict[str, object]]]:
    raw = text.encode("cp932")
    records = []
    replacements = set()
    for idx, rec in enumerate(t5k.inline_records, start=1):
        if rec.original.rstrip(b"\x00") != raw:
            continue
        records.append(
            {
                "record_id": idx,
                "pc_rva": f"0x{rec.pc_rva:X}",
                "length": rec.length,
                "original_hex": rec.original.hex(),
                "replacement_hex": rec.replacement.hex(),
            }
        )
        replacements.add(rec.replacement)

    if not records:
        raise RuntimeError(f"{text}: no PC T5K inline source record")
    if len(replacements) != 1:
        raise RuntimeError(f"{text}: conflicting PC replacements across source records")

    replacement = next(iter(replacements))
    if len(replacement) != len(raw):
        raise RuntimeError(
            f"{text}: source-grounded replacement length {len(replacement)} "
            f"does not equal Switch object length {len(raw)}"
        )
    if any(r["length"] != len(raw) for r in records):
        raise RuntimeError(f"{text}: at least one matching PC source record has a different field length")
    return replacement, records


def main() -> int:
    ap = argparse.ArgumentParser(description="Build DCTRL5 Eden delivery-control diagnostic")
    ap.add_argument("--switch-main", required=True, type=Path, help="compressed Switch v1.1.3 ExeFS main")
    ap.add_argument("--pc-patcher", required=True, type=Path, help="Taiko5DX_Korean_Patcher_v1.02.zip")
    ap.add_argument("--output", required=True, type=Path)
    ap.add_argument("--builder-source-commit", required=True)
    args = ap.parse_args()

    switch_main = args.switch_main.resolve()
    pc_patcher = args.pc_patcher.resolve()
    out = args.output.resolve()

    if sha256_file(switch_main) != SWITCH_MAIN_COMPRESSED_SHA256:
        raise RuntimeError("Switch main compressed SHA-256 guard failed")
    if sha256_file(pc_patcher) != PC_PATCH_SHA256:
        raise RuntimeError("PC patch ZIP SHA-256 guard failed")

    build_id, flat = decompress_nso(switch_main)
    if build_id != BUILD_ID_FULL:
        raise RuntimeError(f"Unexpected Switch Build ID: {build_id.hex()}")

    payload = open_payload(pc_patcher)
    dll = payload.read("dinput8.dll")
    if sha256_bytes(dll) != PC_DLL_SHA256:
        raise RuntimeError("PC dinput8.dll SHA-256 guard failed")
    t5k_blob = extract_t5k_rcdata(dll)
    if sha256_bytes(t5k_blob) != T5K_SHA256:
        raise RuntimeError("T5K resource SHA-256 guard failed")
    t5k = parse_t5k_resource(t5k_blob)

    patched_font = payload.read("data/FONT/FONT_JPN.G1T")
    if sha256_bytes(patched_font) != PATCHED_FONT_SHA256:
        raise RuntimeError("PC Korean FONT_JPN.G1T SHA-256 guard failed")

    if out.exists():
        shutil.rmtree(out)
    out.mkdir(parents=True)

    mod_root = out / "Taiko5DX_KR_DBG_DCTRL5"
    exefs = mod_root / "exefs"
    romfs_font = mod_root / "romfs" / "FONT"
    exefs.mkdir(parents=True)
    romfs_font.mkdir(parents=True)

    plan = PatchPlan(flat)
    emit_records: list[dict[str, object]] = []

    plan.add(GETFONT_OFFSET, GETFONT_ORIGINAL, GETFONT_KOREAN, "runtime_page_mapper")
    emit_records.append(
        {
            "family": "runtime_page_mapper",
            "role": "prerequisite",
            "source_provenance": "V006 / canonical builder constants",
            "mapped_offset": f"0x{GETFONT_OFFSET:X}",
            "emitted_offset": f"0x{mapped_to_ips_offset(GETFONT_OFFSET):X}",
            "original_hex": GETFONT_ORIGINAL.hex(),
            "replacement_hex": GETFONT_KOREAN.hex(),
            "guard_result": "PASS",
            "payload_length": len(GETFONT_KOREAN),
        }
    )

    diagnostic_source_records: dict[str, list[dict[str, object]]] = {}
    for text, mapped in TARGETS:
        raw = text.encode("cp932")
        actual = flat[mapped:mapped + len(raw)]
        if actual != raw:
            raise RuntimeError(
                f"{text}: Switch original-byte guard failed at 0x{mapped:X}; "
                f"expected={raw.hex()} actual={actual.hex()}"
            )
        replacement, pc_records = select_source_grounded_replacement(t5k, text)
        diagnostic_source_records[text] = pc_records
        plan.add(mapped, raw, replacement, f"DCTRL5_{text}")
        emit_records.append(
            {
                "family": "repeated_short_object",
                "role": "diagnostic",
                "text": text,
                "source_provenance": {
                    "validation": "V024",
                    "pc_t5k_records": pc_records,
                },
                "mapped_offset": f"0x{mapped:X}",
                "emitted_offset": f"0x{mapped_to_ips_offset(mapped):X}",
                "original_hex": raw.hex(),
                "replacement_hex": replacement.hex(),
                "guard_result": "PASS",
                "payload_length": len(replacement),
            }
        )

    if len(plan.records) != 6:
        raise RuntimeError(f"DCTRL5 requires exactly 6 patch-plan records; got {len(plan.records)}")

    ips_path = exefs / f"{BUILD_ID_NAME}.ips"
    write_ips(plan.records, ips_path)
    reparsed = parse_ips(ips_path.read_bytes())
    expected = sorted(
        (mapped_to_ips_offset(off), repl)
        for off, _orig, repl, _module in plan.records
    )
    if reparsed != expected:
        raise RuntimeError("DCTRL5 emitted IPS failed exact self-reparse round-trip")
    if len(reparsed) != 6:
        raise RuntimeError(f"DCTRL5 emitted IPS requires exactly 6 records; got {len(reparsed)}")

    (romfs_font / "FONT_JPN.G1T").write_bytes(patched_font)
    if sha256_file(romfs_font / "FONT_JPN.G1T") != PATCHED_FONT_SHA256:
        raise RuntimeError("written Korean font hash mismatch")

    ips_sha = sha256_file(ips_path)

    build_info = {
        "test_id": TEST_ID,
        "purpose": "Eden delivery-control diagnostic: verified page mapper plus five V024 short string objects.",
        "builder_source_commit": args.builder_source_commit,
        "switch": {
            "title_id": TITLE_ID,
            "version": SWITCH_VERSION,
            "build_id": BUILD_ID_NAME,
            "compressed_main_sha256": SWITCH_MAIN_COMPRESSED_SHA256,
        },
        "pc_reference": {
            "patch_zip_sha256": PC_PATCH_SHA256,
            "dinput8_sha256": PC_DLL_SHA256,
            "t5k_sha256": T5K_SHA256,
            "patched_font_sha256": PATCHED_FONT_SHA256,
        },
        "records": emit_records,
        "counts": {
            "diagnostic_records": 5,
            "prerequisite_records": 1,
            "total_records": 6,
            "guard_pass": 6,
            "guard_fail": 0,
            "guard_skip": 0,
            "extra_records": 0,
        },
        "verification": {
            "ips_format": "classic IPS for Eden/Yuzu NSO artificial image",
            "ips_offset_shift": IPS_IMAGE_HEADER_SIZE,
            "self_reparse_exact": True,
            "coordinate_roundtrip_exact": True,
            "reparsed_record_count": len(reparsed),
        },
        "artifacts": {
            "ips_filename": ips_path.name,
            "ips_sha256": ips_sha,
            "package_filename": "DCTRL5_Taiko5DX_KR_EDEN.zip",
            "package_sha256": None,
            "drive_location": "태합입지전 포팅/Eden_Builds/DCTRL5_Taiko5DX_KR_EDEN.zip",
        },
        "provenance_report_commit": None,
    }

    (mod_root / "DCTRL5_BUILD_INFO.json").write_text(
        json.dumps(build_info, ensure_ascii=False, indent=2), encoding="utf-8"
    )

    package_path = out / "DCTRL5_Taiko5DX_KR_EDEN.zip"
    deterministic_zip_dir(mod_root, package_path)
    package_sha = sha256_file(package_path)
    build_info["artifacts"]["package_sha256"] = package_sha

    report_path = out / "DCTRL5_BUILD_REPORT.json"
    emit_log_path = out / "DCTRL5_EMIT_LOG.json"
    report_path.write_text(json.dumps(build_info, ensure_ascii=False, indent=2), encoding="utf-8")
    emit_log_path.write_text(
        json.dumps(
            {
                "test_id": TEST_ID,
                "builder_source_commit": args.builder_source_commit,
                "records": emit_records,
                "reparsed_records": [
                    {"emitted_offset": f"0x{off:X}", "payload_hex": data.hex()}
                    for off, data in reparsed
                ],
                "expected_equals_reparsed": reparsed == expected,
                "ips_sha256": ips_sha,
                "package_sha256": package_sha,
            },
            ensure_ascii=False,
            indent=2,
        ),
        encoding="utf-8",
    )

    print(json.dumps(build_info, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
