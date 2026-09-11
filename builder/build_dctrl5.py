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
from dataclasses import dataclass
from pathlib import Path

TEST_ID = "DCTRL5"
TITLE_ID = "0100346017304000"
SWITCH_VERSION = "1.1.3"
BUILD_ID_NAME = "D9120950C258610A746F4A31CE3A3B376DE393D9"
BUILD_ID_FULL = bytes.fromhex(BUILD_ID_NAME + "000000000000000000000000")

TEXT_MEM_OFF = 0x000000
TEXT_SIZE = 0x58CE60
RODATA_MEM_OFF = 0x58D000
RODATA_SIZE = 0x432018
DATA_MEM_OFF = 0x9C0000
DATA_SIZE = 0x60430
IPS_IMAGE_HEADER_SIZE = 0x100

GETFONT_OFFSET = 0x44650C
GETFONT_ORIGINAL = bytes.fromhex(
    "690a4011293d00123ffd2b7168010054093940510ae09b1208010a0b"
    "3f01007108b1891a087d0813007d0011"
)
GETFONT_KOREAN = bytes.fromhex(
    "693e08532a8103515f610071680100545f29007168000054407d0011"
    "0400001440990011020000141f2003d5"
)

PC_PATCH_SHA256 = "df1b62de95e992369e9686c9731d814e7a7e4634888f610430635429e24f7cec"
PC_DLL_SHA256 = "ffe7e9da8e00c96bec631b45a3e9c4d3f314551623351f3e7024e0318913c6b7"
T5K_SHA256 = "5c6f4eba8c6f0516365e4518f27e9d8c840aead463b5a2938dd1e08b99726d29"
PATCHED_FONT_SHA256 = "c82d80dada61ce80db42f948eafd3eb5b8f3bed5725ceebbc1c0897246166932"
SWITCH_MAIN_COMPRESSED_SHA256 = "b366e692208f3c0cc18bc1884ef95689b6b11d722fa2d749b8500abccbc3109b"

T5K_MAGIC = b"T5K121R\x00"
T5K_EXPECTED_INLINE_COUNT = 17_103
T5K_EXPECTED_POINTER_COUNT = 56
T5K_EXPECTED_RUNTIME_COUNT = 11
T5K_EXPECTED_EXE_SIZE = 18_685_960
T5K_MAPPING_COUNT = 10_036

TARGETS = (
    ("月", 0x68925A),
    ("年", 0x69785A),
    ("はい", 0x6A15A5),
    ("城", 0x6A15DC),
    ("日", 0x6A3CC6),
)

REQUIRED_PAYLOAD = {
    "dinput8.dll",
    "data/FONT/FONT_JPN.G1T",
    "data/EVENT/EC500000.TS5",
}


@dataclass(frozen=True)
class InlinePatchRecord:
    pc_rva: int
    length: int
    original: bytes
    replacement: bytes


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for block in iter(lambda: f.read(1024 * 1024), b""):
            h.update(block)
    return h.hexdigest()


def u16(data: bytes, off: int) -> int:
    return struct.unpack_from("<H", data, off)[0]


def u32(data: bytes, off: int) -> int:
    return struct.unpack_from("<I", data, off)[0]


def rva_to_file_offset(pe: bytes, rva: int) -> int:
    if pe[:2] != b"MZ":
        raise RuntimeError("not a PE image")
    pe_off = u32(pe, 0x3C)
    if pe[pe_off:pe_off + 4] != b"PE\x00\x00":
        raise RuntimeError("invalid PE signature")
    coff = pe_off + 4
    section_count = u16(pe, coff + 2)
    optional_size = u16(pe, coff + 16)
    section_table = coff + 20 + optional_size
    for i in range(section_count):
        off = section_table + i * 40
        virtual_size = u32(pe, off + 8)
        virtual_address = u32(pe, off + 12)
        raw_size = u32(pe, off + 16)
        raw_pointer = u32(pe, off + 20)
        span = max(virtual_size, raw_size)
        if virtual_address <= rva < virtual_address + span:
            return raw_pointer + (rva - virtual_address)
    raise RuntimeError(f"RVA 0x{rva:X} outside PE sections")


def extract_t5k_rcdata(dll: bytes, resource_id: int = 101) -> bytes:
    pe_off = u32(dll, 0x3C)
    coff = pe_off + 4
    optional = coff + 20
    magic = u16(dll, optional)
    if magic == 0x20B:
        data_dir = optional + 112
    elif magic == 0x10B:
        data_dir = optional + 96
    else:
        raise RuntimeError(f"unsupported PE optional-header magic 0x{magic:X}")

    resource_rva = u32(dll, data_dir + 2 * 8)
    resource_size = u32(dll, data_dir + 2 * 8 + 4)
    if not resource_rva or not resource_size:
        raise RuntimeError("PE has no resource directory")
    root = rva_to_file_offset(dll, resource_rva)

    def entries(rel: int) -> list[tuple[int, int]]:
        base = root + rel
        count = u16(dll, base + 12) + u16(dll, base + 14)
        p = base + 16
        return [(u32(dll, p + i * 8), u32(dll, p + i * 8 + 4)) for i in range(count)]

    type_target = next(
        (target for name_or_id, target in entries(0)
         if not (name_or_id & 0x80000000) and name_or_id == 10),
        None,
    )
    if type_target is None or not (type_target & 0x80000000):
        raise RuntimeError("RT_RCDATA not found")

    id_target = next(
        (target for name_or_id, target in entries(type_target & 0x7FFFFFFF)
         if not (name_or_id & 0x80000000) and name_or_id == resource_id),
        None,
    )
    if id_target is None or not (id_target & 0x80000000):
        raise RuntimeError(f"RT_RCDATA/{resource_id} not found")

    lang_entries = entries(id_target & 0x7FFFFFFF)
    if not lang_entries:
        raise RuntimeError("resource has no language entry")
    leaf = lang_entries[0][1]
    if leaf & 0x80000000:
        raise RuntimeError("unexpected extra resource-directory level")

    data_entry = root + leaf
    payload_rva = u32(dll, data_entry)
    payload_size = u32(dll, data_entry + 4)
    payload_off = rva_to_file_offset(dll, payload_rva)
    payload = dll[payload_off:payload_off + payload_size]
    if len(payload) != payload_size:
        raise RuntimeError("truncated RT_RCDATA payload")
    return payload


def parse_t5k_inline(blob: bytes) -> list[InlinePatchRecord]:
    if len(blob) < 0x48 or blob[:8] != T5K_MAGIC:
        raise RuntimeError("invalid T5K121R resource")

    version = u32(blob, 0x08)
    inline_count = u32(blob, 0x0C)
    pointer_count = u32(blob, 0x10)
    runtime_count = u32(blob, 0x14)
    prefix_size = u32(blob, 0x18)
    runtime_blob_size = u32(blob, 0x1C)
    target_exe_size = u32(blob, 0x20)

    if (
        version != 1
        or inline_count != T5K_EXPECTED_INLINE_COUNT
        or pointer_count != T5K_EXPECTED_POINTER_COUNT
        or runtime_count != T5K_EXPECTED_RUNTIME_COUNT
        or target_exe_size != T5K_EXPECTED_EXE_SIZE
    ):
        raise RuntimeError(
            "unsupported T5K identity: "
            f"version={version} inline={inline_count} pointer={pointer_count} "
            f"runtime={runtime_count} exe_size={target_exe_size}"
        )

    mapping_start = 0x48
    mapping_end = mapping_start + T5K_MAPPING_COUNT * 4
    prefix_end = mapping_start + prefix_size
    helper_end = prefix_end + runtime_blob_size
    if not (mapping_start <= mapping_end <= prefix_end <= helper_end <= len(blob)):
        raise RuntimeError("invalid T5K section bounds")

    pos = helper_end
    inline: list[InlinePatchRecord] = []
    for _ in range(inline_count):
        if pos + 8 > len(blob):
            raise RuntimeError("truncated inline table")
        pc_rva, length = struct.unpack_from("<II", blob, pos)
        end = pos + 8 + length * 2
        if length == 0 or end > len(blob):
            raise RuntimeError(f"invalid inline record at 0x{pos:X}")
        inline.append(
            InlinePatchRecord(
                pc_rva=pc_rva,
                length=length,
                original=blob[pos + 8:pos + 8 + length],
                replacement=blob[pos + 8 + length:end],
            )
        )
        pos = end
    return inline


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
    raise RuntimeError("embedded patch_payload.zip not found")


def open_payload(outer_zip: Path) -> zipfile.ZipFile:
    with tempfile.TemporaryDirectory(prefix="taiko_dctrl5_") as td:
        exe = Path(td) / "patcher.exe"
        with zipfile.ZipFile(outer_zip) as z:
            names = [n for n in z.namelist() if n.lower().endswith(".exe")]
            if len(names) != 1:
                raise RuntimeError(f"expected one patcher EXE, got {names}")
            exe.write_bytes(z.read(names[0]))
        payload = locate_payload_zip(exe)
    return zipfile.ZipFile(io.BytesIO(payload))


def decompress_nso(path: Path) -> tuple[bytes, bytes]:
    blob = path.read_bytes()
    if blob[:4] != b"NSO0":
        raise RuntimeError("Switch main is not NSO0")

    try:
        import lz4.block
    except ImportError as exc:
        raise RuntimeError("dependency missing: pip install lz4") from exc

    flags = struct.unpack_from("<I", blob, 0x0C)[0]
    build_id = blob[0x40:0x60]
    segments: list[tuple[int, bytes]] = []
    for index, (hdr, comp_off) in enumerate(((0x10, 0x60), (0x20, 0x64), (0x30, 0x68))):
        file_off, mem_off, decomp_size = struct.unpack_from("<III", blob, hdr)
        comp_size = struct.unpack_from("<I", blob, comp_off)[0]
        stored = blob[file_off:file_off + comp_size]
        data = (
            lz4.block.decompress(stored, uncompressed_size=decomp_size)
            if flags & (1 << index)
            else stored
        )
        if len(data) != decomp_size:
            raise RuntimeError(f"NSO segment {index} size mismatch")
        segments.append((mem_off, data))

    expected = [
        (TEXT_MEM_OFF, TEXT_SIZE),
        (RODATA_MEM_OFF, RODATA_SIZE),
        (DATA_MEM_OFF, DATA_SIZE),
    ]
    actual = [(off, len(data)) for off, data in segments]
    if actual != expected:
        raise RuntimeError(f"unexpected NSO layout: {actual!r}")

    size = max(off + len(data) for off, data in segments)
    flat = bytearray(size)
    for off, data in segments:
        flat[off:off + len(data)] = data
    return build_id, bytes(flat)


class PatchPlan:
    def __init__(self, flat: bytes):
        self.flat = flat
        self.records: list[tuple[int, bytes, bytes, str]] = []

    def add(self, offset: int, original: bytes, replacement: bytes, module: str) -> None:
        if len(original) != len(replacement):
            raise RuntimeError(f"{module}: in-place length mismatch")
        actual = self.flat[offset:offset + len(original)]
        if actual != original:
            raise RuntimeError(
                f"{module}: original-byte guard failed at 0x{offset:X}; "
                f"expected={original.hex()} actual={actual.hex()}"
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


def mapped_to_ips_offset(mapped: int) -> int:
    return mapped + IPS_IMAGE_HEADER_SIZE


def write_ips(records: list[tuple[int, bytes, bytes, str]], out: Path) -> None:
    with out.open("wb") as f:
        f.write(b"PATCH")
        for mapped, _original, replacement, _module in sorted(records, key=lambda r: r[0]):
            off = mapped_to_ips_offset(mapped)
            if off > 0xFFFFFF or off == 0x454F46:
                raise RuntimeError(f"classic IPS offset invalid: 0x{off:X}")
            if not replacement or len(replacement) > 0xFFFF:
                raise RuntimeError("invalid classic IPS payload length")
            f.write(off.to_bytes(3, "big"))
            f.write(len(replacement).to_bytes(2, "big"))
            f.write(replacement)
        f.write(b"EOF")


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


def select_source_grounded_replacement(
    inline_records: list[InlinePatchRecord], text: str
) -> tuple[bytes, list[dict[str, object]]]:
    raw = text.encode("cp932")
    matches: list[dict[str, object]] = []
    replacements: set[bytes] = set()

    for idx, rec in enumerate(inline_records, start=1):
        if rec.original.rstrip(b"\x00") != raw:
            continue
        matches.append(
            {
                "record_id": idx,
                "pc_rva": f"0x{rec.pc_rva:X}",
                "length": rec.length,
                "original_hex": rec.original.hex(),
                "replacement_hex": rec.replacement.hex(),
            }
        )
        replacements.add(rec.replacement)

    if not matches:
        raise RuntimeError(f"{text}: no PC T5K source record")
    if len(replacements) != 1:
        raise RuntimeError(f"{text}: conflicting PC replacements")
    if any(m["length"] != len(raw) for m in matches):
        raise RuntimeError(f"{text}: matching PC source records do not preserve the Switch field length")

    replacement = next(iter(replacements))
    if len(replacement) != len(raw):
        raise RuntimeError(
            f"{text}: replacement length {len(replacement)} != Switch object length {len(raw)}"
        )
    return replacement, matches


def deterministic_zip_dir(root: Path, out_zip: Path) -> None:
    with zipfile.ZipFile(out_zip, "w", compression=zipfile.ZIP_DEFLATED, compresslevel=9) as zout:
        for path in sorted(p for p in root.rglob("*") if p.is_file()):
            arcname = path.relative_to(root.parent).as_posix()
            info = zipfile.ZipInfo(arcname, date_time=(1980, 1, 1, 0, 0, 0))
            info.compress_type = zipfile.ZIP_DEFLATED
            info.external_attr = 0o100644 << 16
            zout.writestr(info, path.read_bytes())


def main() -> int:
    ap = argparse.ArgumentParser(description="Build standalone DCTRL5 Eden delivery-control diagnostic")
    ap.add_argument("--switch-main", required=True, type=Path)
    ap.add_argument("--pc-patcher", required=True, type=Path)
    ap.add_argument("--output", required=True, type=Path)
    ap.add_argument("--builder-source-commit", required=True)
    args = ap.parse_args()

    switch_main = args.switch_main.resolve()
    pc_patcher = args.pc_patcher.resolve()
    out = args.output.resolve()

    if sha256_file(switch_main) != SWITCH_MAIN_COMPRESSED_SHA256:
        raise RuntimeError("Switch main SHA-256 guard failed")
    if sha256_file(pc_patcher) != PC_PATCH_SHA256:
        raise RuntimeError("PC patch ZIP SHA-256 guard failed")

    build_id, flat = decompress_nso(switch_main)
    if build_id != BUILD_ID_FULL:
        raise RuntimeError(f"Switch Build ID guard failed: {build_id.hex()}")

    payload = open_payload(pc_patcher)
    dll = payload.read("dinput8.dll")
    if sha256_bytes(dll) != PC_DLL_SHA256:
        raise RuntimeError("dinput8.dll SHA-256 guard failed")

    t5k_blob = extract_t5k_rcdata(dll)
    if sha256_bytes(t5k_blob) != T5K_SHA256:
        raise RuntimeError("T5K SHA-256 guard failed")
    inline_records = parse_t5k_inline(t5k_blob)

    patched_font = payload.read("data/FONT/FONT_JPN.G1T")
    if sha256_bytes(patched_font) != PATCHED_FONT_SHA256:
        raise RuntimeError("Korean font SHA-256 guard failed")

    if out.exists():
        shutil.rmtree(out)
    out.mkdir(parents=True)

    mod_root = out / "Taiko5DX_KR_DBG_DCTRL5"
    exefs = mod_root / "exefs"
    font_dir = mod_root / "romfs" / "FONT"
    exefs.mkdir(parents=True)
    font_dir.mkdir(parents=True)

    plan = PatchPlan(flat)
    emit_records: list[dict[str, object]] = []

    plan.add(GETFONT_OFFSET, GETFONT_ORIGINAL, GETFONT_KOREAN, "runtime_page_mapper")
    emit_records.append(
        {
            "family": "runtime_page_mapper",
            "role": "prerequisite",
            "source_provenance": "V006",
            "mapped_offset": f"0x{GETFONT_OFFSET:X}",
            "emitted_offset": f"0x{mapped_to_ips_offset(GETFONT_OFFSET):X}",
            "original_hex": GETFONT_ORIGINAL.hex(),
            "replacement_hex": GETFONT_KOREAN.hex(),
            "guard_result": "PASS",
            "payload_length": len(GETFONT_KOREAN),
        }
    )

    for text, mapped in TARGETS:
        raw = text.encode("cp932")
        actual = flat[mapped:mapped + len(raw)]
        if actual != raw:
            raise RuntimeError(
                f"{text}: Switch object guard failed at 0x{mapped:X}; "
                f"expected={raw.hex()} actual={actual.hex()}"
            )
        replacement, pc_records = select_source_grounded_replacement(inline_records, text)
        plan.add(mapped, raw, replacement, f"DCTRL5_{text}")
        emit_records.append(
            {
                "family": "repeated_short_object",
                "role": "diagnostic",
                "text": text,
                "source_provenance": {"validation": "V024", "pc_t5k_records": pc_records},
                "mapped_offset": f"0x{mapped:X}",
                "emitted_offset": f"0x{mapped_to_ips_offset(mapped):X}",
                "original_hex": raw.hex(),
                "replacement_hex": replacement.hex(),
                "guard_result": "PASS",
                "payload_length": len(replacement),
            }
        )

    if len(plan.records) != 6:
        raise RuntimeError(f"expected 6 plan records, got {len(plan.records)}")

    ips_path = exefs / f"{BUILD_ID_NAME}.ips"
    write_ips(plan.records, ips_path)

    reparsed = parse_ips(ips_path.read_bytes())
    expected = sorted(
        (mapped_to_ips_offset(off), replacement)
        for off, _original, replacement, _module in plan.records
    )
    if reparsed != expected:
        raise RuntimeError("emitted IPS failed exact self-reparse")
    if len(reparsed) != 6:
        raise RuntimeError(f"expected 6 reparsed records, got {len(reparsed)}")

    (font_dir / "FONT_JPN.G1T").write_bytes(patched_font)
    if sha256_file(font_dir / "FONT_JPN.G1T") != PATCHED_FONT_SHA256:
        raise RuntimeError("written Korean font SHA-256 mismatch")

    ips_sha = sha256_file(ips_path)

    build_info = {
        "test_id": TEST_ID,
        "purpose": "Eden delivery-control diagnostic: V006 mapper + five V024 objects.",
        "builder_source_commit": args.builder_source_commit,
        "provenance_report_commit": None,
        "inputs": {
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
            },
            "font": {"korean_font_sha256": PATCHED_FONT_SHA256},
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
            "target": "Eden classic IPS",
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
    }

    (mod_root / "DCTRL5_BUILD_INFO.json").write_text(
        json.dumps(build_info, ensure_ascii=False, indent=2), encoding="utf-8"
    )

    package_path = out / "DCTRL5_Taiko5DX_KR_EDEN.zip"
    deterministic_zip_dir(mod_root, package_path)
    package_sha = sha256_file(package_path)
    build_info["artifacts"]["package_sha256"] = package_sha

    (out / "DCTRL5_BUILD_REPORT.json").write_text(
        json.dumps(build_info, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    (out / "DCTRL5_EMIT_LOG.json").write_text(
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
