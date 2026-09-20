from pathlib import Path
import struct
import unittest

from builder.selective_event import parse_event_ts5, SelectiveEventError
from builder.selective_event_1e import (
    INCLUDE_KO_READY,
    KEEP_JP_IDENTITY,
    ONEE_LEDGER_RECORD_COUNT,
    ONEE_READY_ROWSET_SHA256,
    OneELedgerRecord,
    apply_onee_ready,
    load_onee_ledger,
)

ARTIFACT = (
    Path(__file__).resolve().parents[1]
    / "selective_ko" / "artifacts" / "ecf00000_v341_1e_semantic_admission_v1" / "LEDGER_COMPACT.bin"
)


def field(value: bytes) -> bytes:
    raw = value + b"\x00"
    return raw + b"\x00" * ((-len(raw)) % 4)


def onee(slot: int, value: bytes) -> bytes:
    return bytes((0x1E, slot, 0, 0)) + field(value)


def synthetic_ts5(part: bytes) -> bytes:
    first = 16
    return b"HEAD" + struct.pack("<I", 1) + struct.pack("<II", first, first + len(part)) + part


class OneEUnitTests(unittest.TestCase):
    def test_canonical_compact_ledger(self):
        rows = load_onee_ledger(ARTIFACT.read_bytes())
        self.assertEqual(len(rows), ONEE_LEDGER_RECORD_COUNT)
        ready = [row for row in rows if row.disposition == INCLUDE_KO_READY]
        self.assertEqual(len(ready), 23)

    def test_bad_ledger_sha_rejected(self):
        blob = bytearray(ARTIFACT.read_bytes())
        blob[-1] ^= 1
        with self.assertRaises(SelectiveEventError) as cm:
            load_onee_ledger(bytes(blob))
        self.assertEqual(cm.exception.code, "ONEE_LEDGER_SHA_FAIL")

    def test_synthetic_ready_replaces_pc_ko_payload(self):
        original_item = onee(2, b"JP")
        ko_item = onee(2, b"KOREAN")
        original = parse_event_ts5(synthetic_ts5(original_item + b"\x00\x00\x00\x00"))
        ko = parse_event_ts5(synthetic_ts5(ko_item + b"\x00\x00\x00\x00"))
        rec = OneELedgerRecord(0, 0, 16, 16, len(original_item), len(ko_item), INCLUDE_KO_READY, 1)
        current = [[item.data for item in original.partitions[0].grouped_items]]
        solved, report = apply_onee_ready(original, ko, current, (rec,), require_canonical=False)
        self.assertEqual(solved[0][0], ko_item)
        self.assertEqual(report.ready_rows, 1)
        self.assertEqual(report.growth_bytes, len(ko_item) - len(original_item))

    def test_nonready_row_remains_original(self):
        original_item = onee(1, b"NAME")
        ko_item = onee(1, b"IREUM")
        original = parse_event_ts5(synthetic_ts5(original_item + b"\x00\x00\x00\x00"))
        ko = parse_event_ts5(synthetic_ts5(ko_item + b"\x00\x00\x00\x00"))
        rec = OneELedgerRecord(0, 0, 16, 16, len(original_item), len(ko_item), KEEP_JP_IDENTITY, 3)
        current = [[item.data for item in original.partitions[0].grouped_items]]
        solved, report = apply_onee_ready(original, ko, current, (rec,), require_canonical=False)
        self.assertEqual(solved[0][0], original_item)
        self.assertEqual(report.ready_rows, 0)
        self.assertEqual(report.keep_jp_identity_rows, 1)

    def test_nonready_preexisting_mutation_is_rejected(self):
        original_item = onee(1, b"NAME")
        ko_item = onee(1, b"IREUM")
        original = parse_event_ts5(synthetic_ts5(original_item + b"\x00\x00\x00\x00"))
        ko = parse_event_ts5(synthetic_ts5(ko_item + b"\x00\x00\x00\x00"))
        rec = OneELedgerRecord(0, 0, 16, 16, len(original_item), len(ko_item), KEEP_JP_IDENTITY, 3)
        current = [[item.data for item in original.partitions[0].grouped_items]]
        current[0][0] = ko_item
        with self.assertRaises(SelectiveEventError) as cm:
            apply_onee_ready(original, ko, current, (rec,), require_canonical=False)
        self.assertEqual(cm.exception.code, "ONEE_UNAUTHORIZED_PREEXISTING_MUTATION")


if __name__ == "__main__":
    unittest.main()
