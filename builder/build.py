#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import io
import json
import mmap
import shutil
import struct
import tempfile
import zipfile
from pathlib import Path

from t5k import extract_t5k_rcdata, parse_t5k_resource, select_safe_inline_patches

TITLE_ID = "0100346017304000"
BUILD_ID_FULL = bytes.fromhex(
    "d9120950c258610a746f4a31ce3a3b376de393d9"
    "000000000000000000000000"
)
BUILD_ID_NAME = "D9120950C258610A746F4A31CE3A3B376DE393D9"

TEXT_MEM_OFF = 0x000000
TEXT_SIZE = 0x58CE60
RODATA_MEM_OFF = 0x58D000
RODATA_SIZE = 0x432018
DATA_MEM_OFF = 0x9C0000
DATA_SIZE = 0x60430

GETFONT_OFFSET = 0x44650C
GETFONT_ORIGINAL = bytes.fromhex(
    "690a4011293d00123ffd2b7168010054093940510ae09b1208010a0b"
    "3f01007108b1891a087d0813007d0011"
)
GETFONT_KOREAN = bytes.fromhex(
    "693e08532a8103515f610071680100545f29007168000054407d0011"
    "0400001440990011020000141f2003d5"
)

SWITCH_FONT_ORIGINAL_SHA256 = "9c886848c31c31d09aeeed0ac5c44b909d561220110ca04da0f7fa32d3a0083e"
PATCHED_FONT_SHA256 = "c82d80dada61ce80db42f948eafd3eb5b8f3bed5725ceebbc1c0897246166932"
SWITCH_CWTDAT_SIZE = 480_382
REQUIRED_PAYLOAD = {
    "dinput8.dll",
    "data/FONT/FONT_JPN.G1T",
    "data/EVENT/EC500000.TS5",
}


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for block in iter(lambda: f.read(1024 * 1024), b""):
            h.update(block)
    return h.hexdigest()


def find_main(dump_root: Path) -> Path:
    candidates = [
        dump_root / "exefs" / "main",
        dump_root / "ExeFS" / "main",
        dump_root / "EXEFS" / "main",
        dump_root / "main",
    ]
    for p in candidates:
        if p.is_file():
            with p.open("rb") as f:
                if f.read(4) == b"NSO0":
                    return p
    for p in dump_root.rglob("main"):
        if p.is_file():
            with p.open("rb") as f:
                if f.read(4) == b"NSO0":
                    return p
    raise RuntimeError("Could not locate Switch ExeFS/main NSO in dump root")


def find_romfs(dump_root: Path) -> Path:
    candidates = [dump_root / "romfs", dump_root / "RomFS", dump_root / "ROMFS"]
    for p in candidates:
        if (p / "FONT" / "FONT_JPN.G1T").is_file():
            return p
    for font in dump_root.rglob("FONT_JPN.G1T"):
        if font.parent.name.upper() == "FONT":
            return font.parent.parent
    raise RuntimeError("Could not locate Switch RomFS root in dump root")


def decompress_nso(path: Path) -> tuple[bytes, bytes]:
    blob = path.read_bytes()
    if blob[:4] != b"NSO0":
        raise RuntimeError("main is not an NSO0 file")

    try:
        import lz4.block
    except ImportError as exc:
        raise RuntimeError("Install dependency: pip install lz4") from exc

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

    expected_segments = [
        (TEXT_MEM_OFF, TEXT_SIZE),
        (RODATA_MEM_OFF, RODATA_SIZE),
        (DATA_MEM_OFF, DATA_SIZE),
    ]
    actual_segments = [(off, len(data)) for off, data in segments]
    if actual_segments != expected_segments:
        raise RuntimeError(f"Unexpected NSO segment layout: {actual_segments!r}")

    size = max(off + len(data) for off, data in segments)
    flat = bytearray(size)
    for off, data in segments:
        flat[off:off + len(data)] = data
    return build_id, bytes(flat)


def locate_payload_zip(patcher_exe: Path) -> bytes:
    with patcher_exe.open("rb") as f, mmap.mmap(f.fileno(), 0, access=mmap.ACCESS_READ) as mm:
        end = len(mm)
        while True:
            eocd = mm.rfind(b"PK\x05\x06", 0, end)
            if eocd < 0:
                break
            try:
                vals = struct.unpack_from("<4s4H2IH", mm, eocd)
                cd_size, cd_offset, comment_len = vals[-3], vals[-2], vals[-1]
                start = eocd - cd_size - cd_offset
                stop = eocd + 22 + comment_len
                if start >= 0 and stop <= len(mm):
                    candidate = bytes(mm[start:stop])
                    with zipfile.ZipFile(io.BytesIO(candidate)) as z:
                        if REQUIRED_PAYLOAD.issubset(set(z.namelist())):
                            return candidate
            except (struct.error, zipfile.BadZipFile):
                pass
            end = eocd
    raise RuntimeError("Could not locate embedded patch_payload.zip")


def open_payload(outer_zip: Path) -> zipfile.ZipFile:
    with tempfile.TemporaryDirectory(prefix="taiko_pcpatch_") as td:
        exe = Path(td) / "patcher.exe"
        with zipfile.ZipFile(outer_zip) as z:
            names = [n for n in z.namelist() if n.lower().endswith(".exe")]
            if not names:
                raise RuntimeError("No patcher EXE found inside PC patch ZIP")
            exe.write_bytes(z.read(names[0]))
        payload = locate_payload_zip(exe)
    return zipfile.ZipFile(io.BytesIO(payload))


class PatchPlan:
    def __init__(self, flat_nso: bytes):
        self.flat = flat_nso
        self.records: list[tuple[int, bytes, bytes, str]] = []

    def add(self, offset: int, original: bytes, replacement: bytes, module: str) -> None:
        if len(original) != len(replacement):
            raise RuntimeError(f"{module}: in-place length mismatch")
        actual = self.flat[offset:offset + len(original)]
        if actual != original:
            raise RuntimeError(
                f"{module}: original-byte guard failed at 0x{offset:X}\n"
                f"expected={original.hex()}\nactual={actual.hex()}"
            )
        start, end = offset, offset + len(original)
        for old_off, old_original, _old_replacement, old_module in self.records:
            old_start, old_end = old_off, old_off + len(old_original)
            if max(start, old_start) < min(end, old_end):
                raise RuntimeError(
                    f"patch collision: {module}@0x{offset:X} overlaps "
                    f"{old_module}@0x{old_off:X}"
                )
        self.records.append((offset, original, replacement, module))


def write_ips(records: list[tuple[int, bytes, bytes, str]], out: Path) -> None:
    records = sorted(records, key=lambda r: r[0])
    out.parent.mkdir(parents=True, exist_ok=True)
    with out.open("wb") as f:
        f.write(b"PATCH")
        for offset, _original, replacement, _module in records:
            if offset > 0xFFFFFF:
                raise RuntimeError(f"IPS offset 0x{offset:X} exceeds classic IPS range")
            if len(replacement) > 0xFFFF:
                raise RuntimeError("IPS record exceeds 16-bit record length")
            if offset == 0x454F46:
                raise RuntimeError("IPS record offset collides with EOF marker; IPS32 required")
            f.write(offset.to_bytes(3, "big"))
            f.write(len(replacement).to_bytes(2, "big"))
            f.write(replacement)
        f.write(b"EOF")


def build(args: argparse.Namespace) -> None:
    dump_root = args.switch_dump.resolve()
    main_path = find_main(dump_root)
    romfs_root = find_romfs(dump_root)

    build_id, flat = decompress_nso(main_path)
    if build_id != BUILD_ID_FULL:
        raise RuntimeError(f"Unexpected Switch main Build ID: {build_id.hex()}")

    original_font = romfs_root / "FONT" / "FONT_JPN.G1T"
    if not original_font.is_file():
        raise RuntimeError("Switch original FONT/FONT_JPN.G1T missing from dump")
    if sha256_file(original_font) != SWITCH_FONT_ORIGINAL_SHA256:
        raise RuntimeError("Switch original FONT_JPN.G1T hash guard failed")

    original_cwtdat = romfs_root / "CMENU" / "CWTDAT_JP.TR5"
    if not original_cwtdat.is_file():
        raise RuntimeError("Switch original CMENU/CWTDAT_JP.TR5 missing from dump")
    if original_cwtdat.stat().st_size != SWITCH_CWTDAT_SIZE:
        raise RuntimeError("Switch CWTDAT_JP.TR5 size guard failed")

    payload = open_payload(args.pc_patcher)
    names = payload.namelist()
    t5k = parse_t5k_resource(extract_t5k_rcdata(payload.read("dinput8.dll")))

    out = args.output.resolve()
    if out.exists():
        shutil.rmtree(out)
    mod_root = out / args.mod_name
    exefs_out = mod_root / "exefs"
    romfs_out = mod_root / "romfs"

    plan = PatchPlan(flat)
    plan.add(GETFONT_OFFSET, GETFONT_ORIGINAL, GETFONT_KOREAN, "runtime_page_mapper")

    safe_inline, inline_stats = select_safe_inline_patches(
        flat,
        t5k.inline_records,
        RODATA_MEM_OFF,
        RODATA_MEM_OFF + RODATA_SIZE,
    )
    for offset, original, replacement in safe_inline:
        plan.add(offset, original, replacement, "inline_text_unique_rodata")

    write_ips(plan.records, exefs_out / f"{BUILD_ID_NAME}.ips")

    copied = 0
    skipped = []
    for name in names:
        if not name.startswith("data/") or name.endswith("/"):
            continue
        rel = Path(name[5:])
        if rel.as_posix() == "CMENU/CWTDAT_JP.TR5":
            skipped.append(rel.as_posix())
            continue
        data = payload.read(name)
        dst = romfs_out / rel
        dst.parent.mkdir(parents=True, exist_ok=True)
        dst.write_bytes(data)
        copied += 1

    patched_font = romfs_out / "FONT" / "FONT_JPN.G1T"
    if sha256_file(patched_font) != PATCHED_FONT_SHA256:
        raise RuntimeError("Patched FONT_JPN.G1T hash guard failed")

    report = {
        "status": "ok",
        "title_id": TITLE_ID,
        "switch_version": "1.1.3",
        "build_id": BUILD_ID_NAME,
        "switch_dump_root": str(dump_root),
        "main": str(main_path),
        "romfs": str(romfs_root),
        "romfs_payload_files_copied": copied,
        "romfs_payload_files_skipped": skipped,
        "ips_record_count": len(plan.records),
        "ips_payload_bytes": sum(len(r[2]) for r in plan.records),
        "implemented_code_modules": [
            "runtime_page_mapper",
            "inline_text_unique_rodata",
        ],
        "t5k_resource": {
            "mapping_entries": len(t5k.mapping_entries),
            "original_mapping_entries": len(t5k.original_mapping_entries),
            "korean_mapping_entries": len(t5k.korean_mapping_entries),
            "inline_records": len(t5k.inline_records),
            "pointer_records": len(t5k.pointer_records),
            "runtime_descriptors": t5k.runtime_count,
            "pointer_string_pool_bytes": len(t5k.pointer_string_pool),
            "runtime_helper_blob_bytes": len(t5k.runtime_helper_blob),
        },
        "inline_mapping": inline_stats,
        "pending_modules": [
            "unicode_mapping_10036_switch_relocation",
            "runtime_byte_validation_if_runtime_test_requires",
            "font_page_threshold_if_runtime_test_requires",
            "description_font_1_2",
            "ui_width_1_4",
            "pointer_patch_56_switch_mapping",
            "switch_native_cwtdat",
        ],
        "notes": [
            "The integrated dev build applies exact-unique T5K inline originals found in Switch rodata.",
            "Ambiguous/missing matches remain in BUILD_REPORT statistics instead of being guessed.",
            "CWTDAT_JP.TR5 is excluded until reconstructed on the Switch-native structure.",
        ],
    }
    (out / "BUILD_REPORT.json").write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")

    print(f"Built Eden development mod: {mod_root}")
    print(f"Copied PC payload files: {copied}")
    print(f"IPS records: {len(plan.records)} ({inline_stats['selected_patterns']} mapped inline patterns + page mapper)")
    print(f"Mapped PC inline records covered: {inline_stats['selected_pc_records_covered']} / {inline_stats['pc_records_total']}")
    print("Skipped PC CWTDAT_JP.TR5 intentionally; Switch-native reconstruction is pending.")


def main() -> None:
    ap = argparse.ArgumentParser(description="Taiko5DX Switch Korean-port integrated development builder")
    ap.add_argument("--switch-dump", required=True, type=Path, help="Root of complete extracted Switch v1.1.3 dump")
    ap.add_argument("--pc-patcher", required=True, type=Path, help="Taiko5DX_Korean_Patcher_v1.02.zip")
    ap.add_argument("--output", required=True, type=Path, help="Output directory")
    ap.add_argument("--mod-name", default="Taiko5DX_KR_DEV", help="Eden mod folder name")
    build(ap.parse_args())


if __name__ == "__main__":
    main()
