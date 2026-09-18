from __future__ import annotations

import hashlib
import struct
import unittest

from builder.selective_package import (
    EXPECTED_IPS_SIZE,
    FONT_RELATIVE_PATH,
    INFO_RELATIVE_PATH,
    IPS_RELATIVE_PATH,
    IPS_SHIFT,
    PAGE_MAPPER_ORIGINAL,
    PAGE_MAPPER_ORIGINAL_SHA256,
    PAGE_MAPPER_REPLACEMENT,
    PAGE_MAPPER_REPLACEMENT_SHA256,
    PACKAGE_ALLOWLIST,
    SelectivePackageError,
    TAI5MSG_RELATIVE_PATH,
    _assert_nonoverlap,
    _extract_stored_local_member,
    parse_ips,
    serialize_mapped_ips,
    validate_package_allowlist,
)


class SelectivePackageUnitTests(unittest.TestCase):
    def test_page_mapper_identities(self) -> None:
        self.assertEqual(len(PAGE_MAPPER_ORIGINAL), 44)
        self.assertEqual(len(PAGE_MAPPER_REPLACEMENT), 44)
        self.assertEqual(hashlib.sha256(PAGE_MAPPER_ORIGINAL).hexdigest(), PAGE_MAPPER_ORIGINAL_SHA256)
        self.assertEqual(hashlib.sha256(PAGE_MAPPER_REPLACEMENT).hexdigest(), PAGE_MAPPER_REPLACEMENT_SHA256)

    def test_five_record_ips_size_contract(self) -> None:
        records = [
            (0x1000, b"A" * 4),
            (0x2000, b"B" * 4),
            (0x3000, b"C" * 44),
            (0x4000, b"D" * 308),
            (0x5000, b"E" * 2349),
        ]
        ips = serialize_mapped_ips(records)
        self.assertEqual(len(ips), EXPECTED_IPS_SIZE)
        self.assertEqual(parse_ips(ips), [(off + IPS_SHIFT, data) for off, data in records])

    def test_rle_is_rejected(self) -> None:
        blob = b"PATCH" + (0x100).to_bytes(3, "big") + b"\x00\x00" + b"\x00\x04X" + b"EOF"
        with self.assertRaises(SelectivePackageError) as cm:
            parse_ips(blob)
        self.assertEqual(cm.exception.code, "IPS_RECORD_SET_MISMATCH")

    def test_overlap_is_rejected(self) -> None:
        with self.assertRaises(SelectivePackageError) as cm:
            _assert_nonoverlap([(0x1000, b"A" * 8), (0x1004, b"B" * 4)])
        self.assertEqual(cm.exception.code, "EXEFS_ACTION_OVERLAP")

    def test_stored_local_member_extraction(self) -> None:
        name = "x/font.bin"
        data = b"font-bytes"
        header = struct.pack(
            "<IHHHHHIIIHH",
            0x04034B50, 20, 0, 0, 0, 0, 0, len(data), len(data), len(name), 0,
        )
        blob = b"ZZ" + header + name.encode() + data + b"TAIL"
        got = _extract_stored_local_member(blob, 2, name, len(data), hashlib.sha256(data).hexdigest())
        self.assertEqual(got, data)

    def test_allowlist_exact(self) -> None:
        validate_package_allowlist(PACKAGE_ALLOWLIST)
        self.assertEqual(PACKAGE_ALLOWLIST, frozenset({IPS_RELATIVE_PATH, TAI5MSG_RELATIVE_PATH, FONT_RELATIVE_PATH, INFO_RELATIVE_PATH}))
        with self.assertRaises(SelectivePackageError) as cm:
            validate_package_allowlist(set(PACKAGE_ALLOWLIST) | {"romfs/UNAUTHORIZED.BIN"})
        self.assertEqual(cm.exception.code, "PACKAGE_ALLOWLIST_FAIL")


if __name__ == "__main__":
    unittest.main()
