from __future__ import annotations

import argparse
import json
import shutil
from pathlib import Path

import build_dctrl5 as d5

TEST_ID = "DCTRL7"
MOD_ROOT_NAME = "Taiko5DX_KR_DBG_DCTRL7"
PACKAGE_NAME = "DCTRL7_Taiko5DX_KR_EDEN.zip"

R489_RECORD_ID = 489
R489_PC_RVA = 0xB20748
R489_SWITCH_MAPPED = 0x69B6A1
R489_TEXT = "シナリオを選んでください"


def select_r489(inline_records: list[d5.InlinePatchRecord]) -> tuple[d5.InlinePatchRecord, bytes]:
    if len(inline_records) < R489_RECORD_ID:
        raise RuntimeError("T5K inline table is shorter than R489")
    rec = inline_records[R489_RECORD_ID - 1]
    expected_original = R489_TEXT.encode("cp932")
    if rec.pc_rva != R489_PC_RVA:
        raise RuntimeError(f"R489 PC RVA guard failed: 0x{rec.pc_rva:X}")
    if rec.original != expected_original:
        raise RuntimeError(
            "R489 PC original guard failed: "
            f"expected={expected_original.hex()} actual={rec.original.hex()}"
        )
    if rec.length != len(expected_original) or len(rec.replacement) != rec.length:
        raise RuntimeError("R489 PC record length guard failed")
    return rec, expected_original


def independently_serialize_expected(
    plan_records: list[tuple[int, bytes, bytes, str]],
) -> bytes:
    out = bytearray(b"PATCH")
    for mapped, _original, replacement, _module in sorted(plan_records, key=lambda r: r[0]):
        emitted = mapped + 0x100
        if emitted > 0xFFFFFF or emitted == 0x454F46:
            raise RuntimeError(f"independent IPS offset invalid: 0x{emitted:X}")
        if not replacement or len(replacement) > 0xFFFF:
            raise RuntimeError("independent IPS payload length invalid")
        out.extend(emitted.to_bytes(3, "big"))
        out.extend(len(replacement).to_bytes(2, "big"))
        out.extend(replacement)
    out.extend(b"EOF")
    return bytes(out)


def main() -> int:
    ap = argparse.ArgumentParser(
        description="Build DCTRL7 Eden diagnostic with V019 R489 positive control"
    )
    ap.add_argument("--switch-main", required=True, type=Path)
    ap.add_argument("--pc-patcher", required=True, type=Path)
    ap.add_argument("--output", required=True, type=Path)
    ap.add_argument("--builder-source-commit", required=True)
    args = ap.parse_args()

    switch_main = args.switch_main.resolve()
    pc_patcher = args.pc_patcher.resolve()
    out = args.output.resolve()

    if d5.sha256_file(switch_main) != d5.SWITCH_MAIN_COMPRESSED_SHA256:
        raise RuntimeError("Switch main SHA-256 guard failed")
    if d5.sha256_file(pc_patcher) != d5.PC_PATCH_SHA256:
        raise RuntimeError("PC patch ZIP SHA-256 guard failed")

    build_id, flat = d5.decompress_nso(switch_main)
    if build_id != d5.BUILD_ID_FULL:
        raise RuntimeError(f"Switch Build ID guard failed: {build_id.hex()}")

    payload = d5.open_payload(pc_patcher)
    dll = payload.read("dinput8.dll")
    if d5.sha256_bytes(dll) != d5.PC_DLL_SHA256:
        raise RuntimeError("dinput8.dll SHA-256 guard failed")

    t5k_blob = d5.extract_t5k_rcdata(dll)
    if d5.sha256_bytes(t5k_blob) != d5.T5K_SHA256:
        raise RuntimeError("T5K SHA-256 guard failed")
    inline_records = d5.parse_t5k_inline(t5k_blob)

    patched_font = payload.read("data/FONT/FONT_JPN.G1T")
    if d5.sha256_bytes(patched_font) != d5.PATCHED_FONT_SHA256:
        raise RuntimeError("Korean font SHA-256 guard failed")

    if out.exists():
        shutil.rmtree(out)
    out.mkdir(parents=True)

    mod_root = out / MOD_ROOT_NAME
    exefs = mod_root / "exefs"
    font_dir = mod_root / "romfs" / "FONT"
    exefs.mkdir(parents=True)
    font_dir.mkdir(parents=True)

    plan = d5.PatchPlan(flat)
    emit_records: list[dict[str, object]] = []

    # Already-verified rendering prerequisite.
    plan.add(d5.GETFONT_OFFSET, d5.GETFONT_ORIGINAL, d5.GETFONT_KOREAN, "runtime_page_mapper")
    emit_records.append(
        {
            "family": "runtime_page_mapper",
            "role": "prerequisite",
            "source_provenance": "V006",
            "mapped_offset": f"0x{d5.GETFONT_OFFSET:X}",
            "emitted_offset": f"0x{d5.mapped_to_ips_offset(d5.GETFONT_OFFSET):X}",
            "original_hex": d5.GETFONT_ORIGINAL.hex(),
            "replacement_hex": d5.GETFONT_KOREAN.hex(),
            "guard_result": "PASS",
            "payload_length": len(d5.GETFONT_KOREAN),
        }
    )

    # Runtime-confirmed positive control. Replacement bytes are read from actual T5K R489.
    r489, r489_original = select_r489(inline_records)
    actual_r489 = flat[R489_SWITCH_MAPPED:R489_SWITCH_MAPPED + len(r489_original)]
    if actual_r489 != r489_original:
        raise RuntimeError(
            "R489 Switch preimage guard failed at 0x69B6A1; "
            f"expected={r489_original.hex()} actual={actual_r489.hex()}"
        )
    plan.add(R489_SWITCH_MAPPED, r489_original, r489.replacement, "positive_control_R489")
    emit_records.append(
        {
            "family": "runtime_confirmed_inline",
            "role": "positive_control",
            "text": R489_TEXT,
            "source_provenance": {
                "validation": "V019",
                "pc_t5k_record": {
                    "record_id": R489_RECORD_ID,
                    "pc_rva": f"0x{r489.pc_rva:X}",
                    "length": r489.length,
                    "original_hex": r489.original.hex(),
                    "replacement_hex": r489.replacement.hex(),
                },
            },
            "mapped_offset": f"0x{R489_SWITCH_MAPPED:X}",
            "emitted_offset": f"0x{d5.mapped_to_ips_offset(R489_SWITCH_MAPPED):X}",
            "original_hex": r489_original.hex(),
            "replacement_hex": r489.replacement.hex(),
            "guard_result": "PASS",
            "payload_length": len(r489.replacement),
        }
    )

    # DCTRL5 repeated-object family under test.
    for text, mapped in d5.TARGETS:
        raw = text.encode("cp932")
        actual = flat[mapped:mapped + len(raw)]
        if actual != raw:
            raise RuntimeError(
                f"{text}: Switch object guard failed at 0x{mapped:X}; "
                f"expected={raw.hex()} actual={actual.hex()}"
            )
        replacement, pc_records = d5.select_source_grounded_replacement(inline_records, text)
        plan.add(mapped, raw, replacement, f"DCTRL7_{text}")
        emit_records.append(
            {
                "family": "repeated_short_object",
                "role": "diagnostic",
                "text": text,
                "source_provenance": {"validation": "V024", "pc_t5k_records": pc_records},
                "mapped_offset": f"0x{mapped:X}",
                "emitted_offset": f"0x{d5.mapped_to_ips_offset(mapped):X}",
                "original_hex": raw.hex(),
                "replacement_hex": replacement.hex(),
                "guard_result": "PASS",
                "payload_length": len(replacement),
            }
        )

    if len(plan.records) != 7:
        raise RuntimeError(f"expected 7 plan records, got {len(plan.records)}")

    ips_path = exefs / f"{d5.BUILD_ID_NAME}.ips"
    d5.write_ips(plan.records, ips_path)
    ips_blob = ips_path.read_bytes()

    # Existing parser round-trip.
    reparsed = d5.parse_ips(ips_blob)
    expected_records = sorted(
        (d5.mapped_to_ips_offset(off), replacement)
        for off, _original, replacement, _module in plan.records
    )
    if reparsed != expected_records:
        raise RuntimeError("emitted IPS failed exact self-reparse")
    if len(reparsed) != 7:
        raise RuntimeError(f"expected 7 reparsed records, got {len(reparsed)}")

    # Independent raw byte construction so writer/parser cannot agree on the same bad serialization.
    independent_expected_blob = independently_serialize_expected(plan.records)
    if ips_blob != independent_expected_blob:
        raise RuntimeError("emitted IPS differs from independently serialized classic IPS bytes")

    expected_size = 5 + sum(5 + len(payload_bytes) for _off, payload_bytes in expected_records) + 3
    if len(ips_blob) != expected_size:
        raise RuntimeError(f"IPS size mismatch: expected {expected_size}, got {len(ips_blob)}")

    (font_dir / "FONT_JPN.G1T").write_bytes(patched_font)
    if d5.sha256_file(font_dir / "FONT_JPN.G1T") != d5.PATCHED_FONT_SHA256:
        raise RuntimeError("written Korean font SHA-256 mismatch")

    ips_sha = d5.sha256_file(ips_path)

    build_info = {
        "test_id": TEST_ID,
        "purpose": (
            "Eden delivery discriminator: V006 mapper + V019 R489 positive control + "
            "five V024 repeated short objects."
        ),
        "builder_source_commit": args.builder_source_commit,
        "provenance_report_commit": None,
        "inputs": {
            "switch": {
                "title_id": d5.TITLE_ID,
                "version": d5.SWITCH_VERSION,
                "build_id": d5.BUILD_ID_NAME,
                "compressed_main_sha256": d5.SWITCH_MAIN_COMPRESSED_SHA256,
            },
            "pc_reference": {
                "patch_zip_sha256": d5.PC_PATCH_SHA256,
                "dinput8_sha256": d5.PC_DLL_SHA256,
                "t5k_sha256": d5.T5K_SHA256,
            },
            "font": {"korean_font_sha256": d5.PATCHED_FONT_SHA256},
        },
        "records": emit_records,
        "counts": {
            "diagnostic_records": 5,
            "positive_control_records": 1,
            "prerequisite_records": 1,
            "total_records": 7,
            "guard_pass": 7,
            "guard_fail": 0,
            "guard_skip": 0,
            "extra_records": 0,
        },
        "verification": {
            "target": "Eden classic IPS",
            "ips_offset_shift": d5.IPS_IMAGE_HEADER_SIZE,
            "self_reparse_exact": True,
            "independent_raw_serialization_exact": True,
            "coordinate_roundtrip_exact": True,
            "reparsed_record_count": len(reparsed),
            "ips_actual_size": len(ips_blob),
            "ips_expected_size": expected_size,
            "rle_records": 0,
        },
        "artifacts": {
            "ips_filename": ips_path.name,
            "ips_sha256": ips_sha,
            "package_filename": PACKAGE_NAME,
            "package_sha256": None,
            "drive_location": f"태합입지전 포팅/Eden_Builds/{PACKAGE_NAME}",
        },
    }

    (mod_root / "DCTRL7_BUILD_INFO.json").write_text(
        json.dumps(build_info, ensure_ascii=False, indent=2), encoding="utf-8"
    )

    package_path = out / PACKAGE_NAME
    d5.deterministic_zip_dir(mod_root, package_path)
    package_sha = d5.sha256_file(package_path)
    build_info["artifacts"]["package_sha256"] = package_sha

    (out / "DCTRL7_BUILD_REPORT.json").write_text(
        json.dumps(build_info, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    (out / "DCTRL7_EMIT_LOG.json").write_text(
        json.dumps(
            {
                "test_id": TEST_ID,
                "builder_source_commit": args.builder_source_commit,
                "records": emit_records,
                "reparsed_records": [
                    {"emitted_offset": f"0x{off:X}", "payload_hex": data.hex()}
                    for off, data in reparsed
                ],
                "expected_equals_reparsed": reparsed == expected_records,
                "independent_raw_serialization_exact": ips_blob == independent_expected_blob,
                "ips_actual_size": len(ips_blob),
                "ips_expected_size": expected_size,
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
