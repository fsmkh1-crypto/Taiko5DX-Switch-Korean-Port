from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import zipfile

IPS_SHIFT = 0x100

# Switch v1.1.3 sites that implement/in-line the same single-byte
# halfwidth/fullwidth threshold behavior addressed by the PC font_page_limit
# runtime descriptor.  Do not add other cmp #0x100 sites without independent
# semantic proof; e.g. the conversion-path compare around 0x4304F8 is unrelated.
FONT_WIDTH_MAPPED_OFFSETS = (
    0x445EAC,
    0x445FC8,
    0x446198,
    0x4472E8,
    0x447344,
    0x447C44,
)

OLD_CMP_100 = bytes.fromhex("1f010471")  # cmp w8, #0x100
NEW_CMP_A1 = bytes.fromhex("1f850271")   # cmp w8, #0xA1


def parse_ips(blob: bytes) -> list[tuple[int, bytes]]:
    if not blob.startswith(b"PATCH") or not blob.endswith(b"EOF"):
        raise RuntimeError("invalid classic IPS")
    pos = 5
    records: list[tuple[int, bytes]] = []
    while blob[pos:pos + 3] != b"EOF":
        if pos + 5 > len(blob):
            raise RuntimeError("truncated IPS record")
        off = int.from_bytes(blob[pos:pos + 3], "big")
        size = int.from_bytes(blob[pos + 3:pos + 5], "big")
        pos += 5
        if size == 0:
            if pos + 3 > len(blob):
                raise RuntimeError("truncated IPS RLE record")
            rle_size = int.from_bytes(blob[pos:pos + 2], "big")
            value = blob[pos + 2]
            pos += 3
            data = bytes([value]) * rle_size
        else:
            data = blob[pos:pos + size]
            if len(data) != size:
                raise RuntimeError("truncated IPS payload")
            pos += size
        records.append((off, data))
    return records


def build_ips(records: list[tuple[int, bytes]]) -> bytes:
    out = bytearray(b"PATCH")
    for off, data in sorted(records, key=lambda item: item[0]):
        if off > 0xFFFFFF:
            raise RuntimeError(f"classic IPS offset overflow: 0x{off:X}")
        if off == 0x454F46:
            raise RuntimeError("classic IPS record offset collides with EOF")
        if not data or len(data) > 0xFFFF:
            raise RuntimeError("invalid classic IPS record length")
        out += off.to_bytes(3, "big")
        out += len(data).to_bytes(2, "big")
        out += data
    out += b"EOF"
    return bytes(out)


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Build W0: D5519-derived diagnostic with the PC-style A1+ fullwidth threshold ported to Switch."
    )
    parser.add_argument("--base-mod", type=Path, required=True, help="D5519-style corrected Eden mod ZIP")
    parser.add_argument("--flat-main", type=Path, required=True, help="decompressed/mapped Switch v1.1.3 main image")
    parser.add_argument("--output", type=Path, required=True, help="output W0 ZIP")
    parser.add_argument("--root", default="Taiko5DX_KR_DBG_W0", help="output mod root directory")
    args = parser.parse_args()

    flat = args.flat_main.read_bytes()
    for mapped in FONT_WIDTH_MAPPED_OFFSETS:
        got = flat[mapped:mapped + 4]
        if got != OLD_CMP_100:
            raise RuntimeError(
                f"font-width guard failed at mapped 0x{mapped:X}: "
                f"expected {OLD_CMP_100.hex()}, got {got.hex()}"
            )

    with zipfile.ZipFile(args.base_mod, "r") as zin:
        ips_names = [name for name in zin.namelist() if name.lower().endswith(".ips")]
        if len(ips_names) != 1:
            raise RuntimeError(f"expected exactly one IPS file, got {ips_names}")
        ips_name = ips_names[0]
        old_root = ips_name.split("/exefs/")[0] + "/"
        base_records = parse_ips(zin.read(ips_name))
        occupied = {off for off, _ in base_records}

        additions: list[tuple[int, bytes]] = []
        for mapped in FONT_WIDTH_MAPPED_OFFSETS:
            emitted = mapped + IPS_SHIFT
            if emitted in occupied:
                raise RuntimeError(f"W0 collision at emitted IPS 0x{emitted:X}")
            additions.append((emitted, NEW_CMP_A1))

        final_records = base_records + additions
        new_ips = build_ips(final_records)
        reparsed = parse_ips(new_ips)
        expected = sorted(final_records, key=lambda item: item[0])
        if reparsed != expected:
            raise RuntimeError("W0 emitted IPS failed exact round-trip verification")

        root = args.root.rstrip("/") + "/"
        args.output.parent.mkdir(parents=True, exist_ok=True)
        with zipfile.ZipFile(args.output, "w", compression=zipfile.ZIP_DEFLATED) as zout:
            for info in zin.infolist():
                if info.filename.endswith("D5519_TEST_README.json"):
                    continue
                data = zin.read(info.filename)
                new_name = root + info.filename[len(old_root):] if info.filename.startswith(old_root) else info.filename
                if info.filename == ips_name:
                    data = new_ips
                zout.writestr(new_name, data)

            report = {
                "test_id": "W0",
                "purpose": "Port PC font_page_limit single-byte A1+ fullwidth behavior to Switch v1.1.3.",
                "basis": args.base_mod.name,
                "mapped_offsets": [f"0x{x:X}" for x in FONT_WIDTH_MAPPED_OFFSETS],
                "eden_ips_offsets": [f"0x{x + IPS_SHIFT:X}" for x in FONT_WIDTH_MAPPED_OFFSETS],
                "instruction_before": {"asm": "cmp w8, #0x100", "bytes": OLD_CMP_100.hex()},
                "instruction_after": {"asm": "cmp w8, #0xA1", "bytes": NEW_CMP_A1.hex()},
                "base_record_count": len(base_records),
                "added_record_count": len(additions),
                "final_record_count": len(reparsed),
                "static_guards_passed": True,
            }
            zout.writestr("W0_BUILD_REPORT.json", json.dumps(report, ensure_ascii=False, indent=2).encode("utf-8"))

    digest = hashlib.sha256(args.output.read_bytes()).hexdigest()
    print(args.output)
    print(f"sha256={digest}")
    print(f"base_records={len(base_records)} added={len(additions)} final={len(reparsed)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
