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

TITLE_ID = "0100346017304000"
BUILD_ID_FULL = bytes.fromhex(
    "d9120950c258610a746f4a31ce3a3b376de393d9"
    "000000000000000000000000"
)
BUILD_ID_NAME = "D9120950C258610A746F4A31CE3A3B376DE393D9"

GETFONT_OFFSET = 0x44650C
GETFONT_ORIGINAL = bytes.fromhex(
    "690a4011293d00123ffd2b7168010054093940510ae09b1208010a0b"
    "3f01007108b1891a087d0813007d0011"
)
GETFONT_KOREAN = bytes.fromhex(
    "693e08532a8103515f610071680100545f29007168000054407d0011"
    "0400001440990011020000141f2003d5"
)

PATCHED_FONT_SHA256 = "c82d80dada61ce80db42f948eafd3eb5b8f3bed5725ceebbc1c0897246166932"
REQUIRED_PAYLOAD = {
    "dinput8.dll",
    "data/FONT/FONT_JPN.G1T",
    "data/EVENT/EC500000.TS5",
}


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def find_main(dump_root: Path) -> Path:
    candidates = [
        dump_root / "exefs" / "main",
        dump_root / "ExeFS" / "main",
        dump_root / "EXEFS" / "main",
        dump_root / "main",
    ]
    for p in candidates:
        if p.is_file() and p.read_bytes()[:4] == b"NSO0":
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


def write_ips(offset: int, data: bytes, out: Path) -> None:
    if offset > 0xFFFFFF or len(data) > 0xFFFF:
        raise RuntimeError("Current patch does not fit classic IPS")
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_bytes(b"PATCH" + offset.to_bytes(3, "big") + len(data).to_bytes(2, "big") + data + b"EOF")


def build(args: argparse.Namespace) -> None:
    dump_root = args.switch_dump.resolve()
    main_path = find_main(dump_root)
    romfs_root = find_romfs(dump_root)

    build_id, flat = decompress_nso(main_path)
    if build_id != BUILD_ID_FULL:
        raise RuntimeError(f"Unexpected Switch main Build ID: {build_id.hex()}")

    actual = flat[GETFONT_OFFSET:GETFONT_OFFSET + len(GETFONT_ORIGINAL)]
    if actual != GETFONT_ORIGINAL:
        raise RuntimeError(
            f"GetFontTexIndex original-byte guard failed at 0x{GETFONT_OFFSET:X}\n"
            f"expected={GETFONT_ORIGINAL.hex()}\nactual={actual.hex()}"
        )

    original_font = romfs_root / "FONT" / "FONT_JPN.G1T"
    if not original_font.is_file():
        raise RuntimeError("Switch original FONT/FONT_JPN.G1T missing from dump")

    original_cwtdat = romfs_root / "CMENU" / "CWTDAT_JP.TR5"
    if not original_cwtdat.is_file():
        raise RuntimeError("Switch original CMENU/CWTDAT_JP.TR5 missing from dump")

    payload = open_payload(args.pc_patcher)
    names = payload.namelist()

    out = args.output.resolve()
    if out.exists():
        shutil.rmtree(out)
    mod_root = out / args.mod_name
    exefs_out = mod_root / "exefs"
    romfs_out = mod_root / "romfs"

    write_ips(GETFONT_OFFSET, GETFONT_KOREAN, exefs_out / f"{BUILD_ID_NAME}.ips")

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
    if sha256(patched_font.read_bytes()) != PATCHED_FONT_SHA256:
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
        "implemented_code_modules": ["font_page_mapper"],
        "pending_code_modules": [
            "unicode_mapping_10036",
            "runtime_byte_validation",
            "font_page_threshold",
            "description_font_1_2",
            "ui_width_1_4",
            "inline_text_17103",
            "pointer_patch_56",
            "switch_native_cwtdat",
        ],
    }
    (out / "BUILD_REPORT.json").write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")

    print(f"Built Eden development mod: {mod_root}")
    print(f"Copied PC payload files: {copied}")
    print("Skipped PC CWTDAT_JP.TR5 intentionally; Switch-native reconstruction is pending.")


def main() -> None:
    ap = argparse.ArgumentParser(description="Taiko5DX Switch Korean-port development builder")
    ap.add_argument("--switch-dump", required=True, type=Path, help="Root of complete extracted Switch v1.1.3 dump")
    ap.add_argument("--pc-patcher", required=True, type=Path, help="Taiko5DX_Korean_Patcher_v1.02.zip")
    ap.add_argument("--output", required=True, type=Path, help="Output directory")
    ap.add_argument("--mod-name", default="Taiko5DX_KR_DEV", help="Eden mod folder name")
    build(ap.parse_args())


if __name__ == "__main__":
    main()
