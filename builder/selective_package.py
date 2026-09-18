from __future__ import annotations

import argparse
from dataclasses import asdict, dataclass
import hashlib
import io
import json
from pathlib import Path
import struct
import zipfile

from builder.selective_tai5msg import (
    EXPECTED_DIAGNOSTIC_SHA256,
    EXPECTED_FINAL_SIZE,
    mapping_code_set,
    reconstruct_selective_tai5msg,
)
from builder.t5k import extract_t5k_rcdata, parse_t5k_resource

TITLE_ID = "0100346017304000"
VERSION = "1.1.3"
BUILD_ID_NAME = "D9120950C258610A746F4A31CE3A3B376DE393D9"
BUILD_ID_FULL = bytes.fromhex(BUILD_ID_NAME + "000000000000000000000000")
MAIN_SHA256 = "b366e692208f3c0cc18bc1884ef95689b6b11d722fa2d749b8500abccbc3109b"
PC_DINPUT8_SHA256 = "ffe7e9da8e00c96bec631b45a3e9c4d3f314551623351f3e7024e0318913c6b7"
MAPPING_IPS_SHA256 = "6ff4b07db9b83b22197009206e21b5023ad02e62458e8597bac219a3c0faa120"

TEXT_MEM_OFF, TEXT_SIZE = 0x000000, 0x58CE60
RODATA_MEM_OFF, RODATA_SIZE = 0x58D000, 0x432018
DATA_MEM_OFF, DATA_SIZE = 0x9C0000, 0x60430
IPS_SHIFT = 0x100

PAGE_MAPPER_SITE = 0x44650C
PAGE_MAPPER_ORIGINAL = bytes.fromhex(
    "690a4011293d00123ffd2b7168010054093940510ae09b1208010a0b"
    "3f01007108b1891a087d0813007d0011"
)
PAGE_MAPPER_REPLACEMENT = bytes.fromhex(
    "693e08532a8103515f610071680100545f29007168000054407d0011"
    "0400001440990011020000141f2003d5"
)
PAGE_MAPPER_ORIGINAL_SHA256 = "7fbdbe36095e02fd55ffd69dd671250c369be1e3b4cce68e576cab98082ade3b"
PAGE_MAPPER_REPLACEMENT_SHA256 = "f548a5c3ce313c1b578fe4867045c96abfae8b41ea76df09732baafb2fdbe050"

KOREAN_FONT_SIZE = 16_779_036
KOREAN_FONT_SHA256 = "c82d80dada61ce80db42f948eafd3eb5b8f3bed5725ceebbc1c0897246166932"
V291_PART00_SIZE = 50_331_648
V291_PART00_SHA256 = "04db6aea9dd18b686be4f500473493fbdaddcca0a6126f09ca48f227341053c9"
V291_FONT_LOCAL_HEADER_OFFSET = 27_513_210
V291_FONT_MEMBER = "Taiko5DX_KR_V291_GRAMMAR125_HWTEST/romfs/FONT/FONT_JPN.G1T"

EXPECTED_IPS_RECORDS = 5
EXPECTED_IPS_SIZE = 2_742
PACKAGE_ROOT = "Taiko5DX_KR_SELECTIVE"
IPS_RELATIVE_PATH = f"exefs/{BUILD_ID_NAME}.ips"
TAI5MSG_RELATIVE_PATH = "romfs/TAI5MSG_JP.DAT"
FONT_RELATIVE_PATH = "romfs/FONT/FONT_JPN.G1T"
INFO_RELATIVE_PATH = "SELECTIVE_PACKAGE_INFO.json"
PACKAGE_ALLOWLIST = frozenset({IPS_RELATIVE_PATH, TAI5MSG_RELATIVE_PATH, FONT_RELATIVE_PATH, INFO_RELATIVE_PATH})


class SelectivePackageError(RuntimeError):
    def __init__(self, code: str, detail: str):
        self.code = code
        self.detail = detail
        super().__init__(f"{code}: {detail}")


def _fail(code: str, detail: str) -> None:
    raise SelectivePackageError(code, detail)


def _sha(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


@dataclass(frozen=True)
class ActionSpec:
    action_id: str
    mapped_offset: int
    size: int
    guard_sha256: str
    payload_sha256: str


MAPPING_ACTIONS = (
    ActionSpec("MAP10036_FWD_MISS_HOOK_V1", 0x4304E0, 4,
               "98813cf6edbe59d962385f8bf0f1badd2557cf12ef0c35bc588aa9104f21d45b",
               "2df5115d570e7775ce72bee4b267ffdc1f771f4e4feafcee253c72745f997d2d"),
    ActionSpec("MAP10036_REV_MISS_HOOK_V1", 0x430798, 4,
               "196b4f3803e4f689fd5a889e142a35311b7bc5fcccabc1b700c39ebf406a1561",
               "c92c275afc2d98a43dc2a0f7008bcd62bd4dda07fe4e540e45d33b5c7a80df7d"),
    ActionSpec("MAP10036_HELPER_TEXT_V2", 0x58CE60, 308,
               "9575b2125169377b2ade7b401ea36c81228331d971f49664d9648d4f255d4868",
               "f472326cab461ac8258282d5795031c33bcc52c9d2f1cd821b8eb6c94352f493"),
    ActionSpec("MAP10036_DELTA_RODATA_V1", 0x9BF018, 2349,
               "9bff4e0fc43a214b9efe2fddbcd29b1d1d61d2d278f89d34f9cd8b9c0f11516a",
               "ddedc507fa892a5b5be6f35ab24f0a0e5fac0d71e633134712b33bd4c6a2088f"),
)


@dataclass(frozen=True)
class OfflineIntegrationReport:
    main_sha256: str
    t5k_mapping_entries: int
    t5k_unique_game_codes: int
    tai5msg_sha256: str
    tai5msg_size: int
    tai5msg_selected_rows: int
    tai5msg_unselected_rows: int
    font_sha256: str
    font_size: int
    mapping_ips_sha256: str
    integrated_ips_sha256: str
    integrated_ips_size: int
    integrated_ips_records: int
    page_mapper_mapped_offset: int
    package_allowlist: tuple[str, ...]
    staged_file_count: int
    info_sha256: str
    published_package: bool

    def to_dict(self) -> dict:
        return asdict(self)


def decompress_nso(main_blob: bytes) -> tuple[bytes, bytes]:
    if _sha(main_blob) != MAIN_SHA256:
        _fail("SWITCH_MAIN_IDENTITY_MISMATCH", "compressed main SHA-256 mismatch")
    if main_blob[:4] != b"NSO0":
        _fail("SWITCH_MAIN_IDENTITY_MISMATCH", "main is not NSO0")
    try:
        import lz4.block
    except ImportError as exc:
        raise RuntimeError("Install dependency: pip install lz4") from exc
    flags = struct.unpack_from("<I", main_blob, 0x0C)[0]
    build_id = main_blob[0x40:0x60]
    if build_id != BUILD_ID_FULL:
        _fail("SWITCH_MAIN_IDENTITY_MISMATCH", f"Build ID mismatch: {build_id.hex()}")
    segments = []
    for index, (hdr, comp_off) in enumerate(((0x10, 0x60), (0x20, 0x64), (0x30, 0x68))):
        file_off, mem_off, decomp_size = struct.unpack_from("<III", main_blob, hdr)
        comp_size = struct.unpack_from("<I", main_blob, comp_off)[0]
        stored = main_blob[file_off:file_off + comp_size]
        data = lz4.block.decompress(stored, uncompressed_size=decomp_size) if flags & (1 << index) else stored
        if len(data) != decomp_size:
            _fail("SWITCH_MAIN_IDENTITY_MISMATCH", f"segment {index} size mismatch")
        segments.append((mem_off, data))
    expected = [(TEXT_MEM_OFF, TEXT_SIZE), (RODATA_MEM_OFF, RODATA_SIZE), (DATA_MEM_OFF, DATA_SIZE)]
    if [(off, len(data)) for off, data in segments] != expected:
        _fail("SWITCH_MAIN_IDENTITY_MISMATCH", "unexpected NSO segment layout")
    flat = bytearray(max(off + len(data) for off, data in segments))
    for off, data in segments:
        flat[off:off + len(data)] = data
    return build_id, bytes(flat)


def parse_ips(blob: bytes) -> list[tuple[int, bytes]]:
    if not blob.startswith(b"PATCH") or not blob.endswith(b"EOF"):
        _fail("IPS_REPARSE_FAIL", "bad classic-IPS framing")
    pos = 5
    end = len(blob) - 3
    out: list[tuple[int, bytes]] = []
    while pos < end:
        if pos + 5 > end:
            _fail("IPS_REPARSE_FAIL", "truncated IPS record header")
        off = int.from_bytes(blob[pos:pos + 3], "big")
        pos += 3
        size = int.from_bytes(blob[pos:pos + 2], "big")
        pos += 2
        if size == 0:
            _fail("IPS_RECORD_SET_MISMATCH", "RLE records are forbidden")
        payload = blob[pos:pos + size]
        pos += size
        if len(payload) != size:
            _fail("IPS_REPARSE_FAIL", "truncated IPS payload")
        out.append((off, payload))
    if pos != end:
        _fail("IPS_REPARSE_FAIL", "IPS parse boundary mismatch")
    return out


def serialize_mapped_ips(records: list[tuple[int, bytes]]) -> bytes:
    out = bytearray(b"PATCH")
    for mapped, payload in sorted(records):
        emitted = mapped + IPS_SHIFT
        if emitted > 0xFFFFFF or emitted == 0x454F46 or not payload or len(payload) > 0xFFFF:
            _fail("IPS_RECORD_SET_MISMATCH", f"invalid record at mapped 0x{mapped:X}")
        out += emitted.to_bytes(3, "big") + len(payload).to_bytes(2, "big") + payload
    out += b"EOF"
    return bytes(out)


def _assert_nonoverlap(records: list[tuple[int, bytes]]) -> None:
    spans: list[tuple[int, int]] = []
    for mapped, payload in sorted(records):
        span = (mapped, mapped + len(payload))
        for old in spans:
            if max(span[0], old[0]) < min(span[1], old[1]):
                _fail("EXEFS_ACTION_OVERLAP", f"0x{span[0]:X}..0x{span[1]:X} overlaps 0x{old[0]:X}..0x{old[1]:X}")
        spans.append(span)


def _extract_mapping_ips(mapping_package_blob: bytes) -> bytes:
    try:
        with zipfile.ZipFile(io.BytesIO(mapping_package_blob)) as z:
            ips_names = [name for name in z.namelist() if name.lower().endswith(".ips")]
            if len(ips_names) != 1:
                _fail("IPS_RECORD_SET_MISMATCH", f"expected one mapping IPS, got {ips_names}")
            ips = z.read(ips_names[0])
    except zipfile.BadZipFile as exc:
        _fail("IPS_REPARSE_FAIL", f"mapping artifact is not a valid ZIP: {exc}")
    if _sha(ips) != MAPPING_IPS_SHA256:
        _fail("IPS_RECORD_SET_MISMATCH", "mapping-only IPS identity mismatch")
    return ips


def _verified_mapping_records(mapping_package_blob: bytes, flat_main: bytes) -> list[tuple[int, bytes]]:
    ips = _extract_mapping_ips(mapping_package_blob)
    records = parse_ips(ips)
    if len(records) != len(MAPPING_ACTIONS):
        _fail("IPS_RECORD_SET_MISMATCH", f"mapping record count {len(records)} != {len(MAPPING_ACTIONS)}")
    by_emitted = {off: payload for off, payload in records}
    if len(by_emitted) != len(records):
        _fail("IPS_RECORD_SET_MISMATCH", "duplicate mapping IPS offset")
    mapped_records: list[tuple[int, bytes]] = []
    for spec in MAPPING_ACTIONS:
        emitted = spec.mapped_offset + IPS_SHIFT
        payload = by_emitted.get(emitted)
        if payload is None or len(payload) != spec.size:
            _fail("IPS_RECORD_SET_MISMATCH", f"missing/size mismatch: {spec.action_id}")
        if _sha(payload) != spec.payload_sha256:
            _fail("MAPPING_ACTION_PAYLOAD_FAIL", spec.action_id)
        preimage = flat_main[spec.mapped_offset:spec.mapped_offset + spec.size]
        if len(preimage) != spec.size or _sha(preimage) != spec.guard_sha256:
            _fail("MAPPING_ACTION_GUARD_FAIL", spec.action_id)
        mapped_records.append((spec.mapped_offset, payload))
    if set(by_emitted) != {spec.mapped_offset + IPS_SHIFT for spec in MAPPING_ACTIONS}:
        _fail("IPS_RECORD_SET_MISMATCH", "mapping IPS contains an extra record")
    return mapped_records


def _page_mapper_record(flat_main: bytes) -> tuple[int, bytes]:
    actual = flat_main[PAGE_MAPPER_SITE:PAGE_MAPPER_SITE + len(PAGE_MAPPER_ORIGINAL)]
    if actual != PAGE_MAPPER_ORIGINAL or _sha(actual) != PAGE_MAPPER_ORIGINAL_SHA256:
        _fail("PAGE_MAPPER_GUARD_FAIL", f"mapped 0x{PAGE_MAPPER_SITE:X}")
    if _sha(PAGE_MAPPER_REPLACEMENT) != PAGE_MAPPER_REPLACEMENT_SHA256:
        _fail("PAGE_MAPPER_PAYLOAD_FAIL", "replacement identity mismatch")
    return PAGE_MAPPER_SITE, PAGE_MAPPER_REPLACEMENT


def build_integrated_ips(main_blob: bytes, mapping_package_blob: bytes) -> tuple[bytes, bytes]:
    _build_id, flat = decompress_nso(main_blob)
    records = _verified_mapping_records(mapping_package_blob, flat)
    records.append(_page_mapper_record(flat))
    _assert_nonoverlap(records)
    ips = serialize_mapped_ips(records)
    if len(ips) != EXPECTED_IPS_SIZE:
        _fail("IPS_RECORD_SET_MISMATCH", f"integrated IPS size {len(ips)} != {EXPECTED_IPS_SIZE}")
    parsed = parse_ips(ips)
    expected = sorted((mapped + IPS_SHIFT, payload) for mapped, payload in records)
    if len(parsed) != EXPECTED_IPS_RECORDS or parsed != expected:
        _fail("IPS_RECORD_SET_MISMATCH", "integrated five-record set mismatch")
    if serialize_mapped_ips(records) != ips:
        _fail("IPS_REPARSE_FAIL", "independent reserialization mismatch")
    return ips, flat


def _extract_stored_local_member(
    blob: bytes,
    local_header_offset: int,
    expected_name: str,
    expected_size: int,
    expected_sha256: str,
) -> bytes:
    if blob[local_header_offset:local_header_offset + 4] != b"PK\x03\x04":
        _fail("FONT_IDENTITY_MISMATCH", "local ZIP header signature mismatch")
    if local_header_offset + 30 > len(blob):
        _fail("FONT_IDENTITY_MISMATCH", "truncated local ZIP header")
    _sig, _ver, flags, method, _mtime, _mdate, _crc, comp_size, uncomp_size, name_len, extra_len = struct.unpack_from(
        "<IHHHHHIIIHH", blob, local_header_offset
    )
    if flags != 0 or method != 0:
        _fail("FONT_IDENTITY_MISMATCH", f"expected stored unflagged member, flags={flags}, method={method}")
    name_start = local_header_offset + 30
    name_end = name_start + name_len
    try:
        name = blob[name_start:name_end].decode("utf-8")
    except UnicodeDecodeError as exc:
        _fail("FONT_IDENTITY_MISMATCH", f"member-name decode failed: {exc}")
    if name != expected_name:
        _fail("FONT_IDENTITY_MISMATCH", f"unexpected member {name!r}")
    if comp_size != expected_size or uncomp_size != expected_size:
        _fail("FONT_IDENTITY_MISMATCH", "font member size mismatch")
    data_start = name_end + extra_len
    data = blob[data_start:data_start + expected_size]
    if len(data) != expected_size or _sha(data) != expected_sha256:
        _fail("FONT_IDENTITY_MISMATCH", "font payload identity mismatch")
    return data


def recover_canonical_font(part00_blob: bytes) -> bytes:
    if len(part00_blob) != V291_PART00_SIZE or _sha(part00_blob) != V291_PART00_SHA256:
        _fail("FONT_IDENTITY_MISMATCH", "V291 part00 identity mismatch")
    return _extract_stored_local_member(
        part00_blob,
        V291_FONT_LOCAL_HEADER_OFFSET,
        V291_FONT_MEMBER,
        KOREAN_FONT_SIZE,
        KOREAN_FONT_SHA256,
    )


def validate_package_allowlist(paths) -> None:
    actual = frozenset(str(p).replace("\\", "/").lstrip("/") for p in paths)
    if actual != PACKAGE_ALLOWLIST:
        extra = sorted(actual - PACKAGE_ALLOWLIST)
        missing = sorted(PACKAGE_ALLOWLIST - actual)
        _fail("PACKAGE_ALLOWLIST_FAIL", f"extra={extra} missing={missing}")


def _mapping_codes_from_pc_dinput8(pc_dinput8: bytes) -> tuple[frozenset[int], int]:
    if _sha(pc_dinput8) != PC_DINPUT8_SHA256:
        _fail("PC_PATCH_MAPPING_SOURCE_MISMATCH", "PC dinput8.dll identity mismatch")
    resource = parse_t5k_resource(extract_t5k_rcdata(pc_dinput8))
    if len(resource.mapping_entries) != 10_036:
        _fail("MAPPING_ACTION_PAYLOAD_FAIL", "T5K Mapping count mismatch")
    return mapping_code_set(resource.mapping_entries), len(resource.mapping_entries)


def offline_validate(
    *,
    main_blob: bytes,
    stock_tai5msg: bytes,
    pc_ko_tai5msg: bytes,
    pc_dinput8: bytes,
    mapping_package_blob: bytes,
    font_part00_blob: bytes,
    repo_root: Path,
) -> OfflineIntegrationReport:
    mapping_codes, mapping_entries = _mapping_codes_from_pc_dinput8(pc_dinput8)
    tai5msg, tai_report = reconstruct_selective_tai5msg(
        stock_tai5msg,
        pc_ko_tai5msg,
        repo_root,
        mapping_codes,
        require_diagnostic_sha=True,
    )
    if len(tai5msg) != EXPECTED_FINAL_SIZE or _sha(tai5msg) != EXPECTED_DIAGNOSTIC_SHA256:
        _fail("TAI5MSG_OUTPUT_IDENTITY_MISMATCH", "current selective TAI5MSG output identity mismatch")

    ips, _flat = build_integrated_ips(main_blob, mapping_package_blob)
    font = recover_canonical_font(font_part00_blob)

    info = {
        "schema": "TAI5MSG_3179_SELECTIVE_PACKAGE_INTEGRATION_OFFLINE_V1",
        "delivery_profile": "EDEN_CLASSIC_IPS_ONLY",
        "title_id": TITLE_ID,
        "version": VERSION,
        "build_id": BUILD_ID_NAME,
        "files": {
            IPS_RELATIVE_PATH: {"bytes": len(ips), "sha256": _sha(ips)},
            TAI5MSG_RELATIVE_PATH: {"bytes": len(tai5msg), "sha256": _sha(tai5msg)},
            FONT_RELATIVE_PATH: {"bytes": len(font), "sha256": _sha(font)},
        },
        "tai5msg": tai_report.to_dict(),
        "published_package": False,
    }
    info_bytes = json.dumps(info, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")
    staged = {
        IPS_RELATIVE_PATH: ips,
        TAI5MSG_RELATIVE_PATH: tai5msg,
        FONT_RELATIVE_PATH: font,
        INFO_RELATIVE_PATH: info_bytes,
    }
    validate_package_allowlist(staged.keys())

    return OfflineIntegrationReport(
        main_sha256=_sha(main_blob),
        t5k_mapping_entries=mapping_entries,
        t5k_unique_game_codes=len(mapping_codes),
        tai5msg_sha256=_sha(tai5msg),
        tai5msg_size=len(tai5msg),
        tai5msg_selected_rows=tai_report.selected_rows,
        tai5msg_unselected_rows=tai_report.unselected_rows,
        font_sha256=_sha(font),
        font_size=len(font),
        mapping_ips_sha256=MAPPING_IPS_SHA256,
        integrated_ips_sha256=_sha(ips),
        integrated_ips_size=len(ips),
        integrated_ips_records=len(parse_ips(ips)),
        page_mapper_mapped_offset=PAGE_MAPPER_SITE,
        package_allowlist=tuple(sorted(PACKAGE_ALLOWLIST)),
        staged_file_count=len(staged),
        info_sha256=_sha(info_bytes),
        published_package=False,
    )


def main() -> int:
    ap = argparse.ArgumentParser(description="V310 selective package integration offline validator; publishes no package")
    ap.add_argument("--switch-main", required=True, type=Path)
    ap.add_argument("--stock-tai5msg", required=True, type=Path)
    ap.add_argument("--pc-ko-tai5msg", required=True, type=Path)
    ap.add_argument("--pc-dinput8", required=True, type=Path)
    ap.add_argument("--mapping-package", required=True, type=Path)
    ap.add_argument("--font-part00", required=True, type=Path)
    ap.add_argument("--repo-root", type=Path, default=Path(__file__).resolve().parents[1])
    args = ap.parse_args()
    report = offline_validate(
        main_blob=args.switch_main.read_bytes(),
        stock_tai5msg=args.stock_tai5msg.read_bytes(),
        pc_ko_tai5msg=args.pc_ko_tai5msg.read_bytes(),
        pc_dinput8=args.pc_dinput8.read_bytes(),
        mapping_package_blob=args.mapping_package.read_bytes(),
        font_part00_blob=args.font_part00.read_bytes(),
        repo_root=args.repo_root.resolve(),
    )
    print(json.dumps(report.to_dict(), ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
