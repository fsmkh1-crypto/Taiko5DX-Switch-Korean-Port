from pathlib import Path
import struct
import unittest

from builder.selective_event import SelectiveEventError, parse_event_ts5
from builder.selective_event_particle import (
    PARTICLE_LEDGER_RECORD_COUNT,
    PARTICLE_OCCURRENCES,
    PARTICLE_AGGREGATE_SHRINK,
    PARTICLE_TRANSFORMED_CORPUS_SHA256,
    SEMANTIC_INCLUDE_KO_CHOICE,
    SEMANTIC_INCLUDE_KO_FIXED_SURFACE_PARTICLE,
    ParticleLedgerRecord,
    apply_fixed_surface_particles,
    load_particle_ledger,
    transform_particle_command,
)

ARTIFACT = (
    Path(__file__).resolve().parents[1]
    / 'selective_ko' / 'artifacts' / 'ecf00000_v344_particle_preimplementation_v1'
    / 'PARTICLE_APPLICABILITY_COMPACT.bin'
)


def field(value: bytes) -> bytes:
    raw = value + b'\0'
    return raw + b'\0' * ((-len(raw)) % 4)


def message(opcode: int, value: bytes) -> bytes:
    return bytes((opcode, 0, 0, 0)) + field(value)


def choice(*values: bytes) -> bytes:
    return bytes((0x15, len(values), 0, 0)) + b''.join(field(value) for value in values)


def ts5(part: bytes) -> bytes:
    first = 16
    return b'HEAD' + struct.pack('<I', 1) + struct.pack('<II', first, first + len(part)) + part


class ParticleUnitTests(unittest.TestCase):
    def test_canonical_ledger(self):
        rows = load_particle_ledger(ARTIFACT.read_bytes())
        self.assertEqual(len(rows), PARTICLE_LEDGER_RECORD_COUNT)
        self.assertEqual(sum(r.occurrence_count for r in rows), PARTICLE_OCCURRENCES)
        self.assertEqual(sum(r.ko_length - r.transformed_length for r in rows), PARTICLE_AGGREGATE_SHRINK)

    def test_bad_ledger_sha_rejected(self):
        blob = bytearray(ARTIFACT.read_bytes())
        blob[-1] ^= 1
        with self.assertRaises(SelectiveEventError) as cm:
            load_particle_ledger(bytes(blob))
        self.assertEqual(cm.exception.code, 'PARTICLE_LEDGER_SHA_FAIL')

    def test_all_six_surfaces_transform_only_inside_message(self):
        surfaces = [
            (bytes.fromhex('f35928ed6129'), bytes.fromhex('ed61')),
            (bytes.fromhex('f36b28eb4029'), bytes.fromhex('eb40')),
            (bytes.fromhex('f35a28ef4529'), bytes.fromhex('ef45')),
            (bytes.fromhex('eb9a28f2cb29'), bytes.fromhex('f2cb')),
            (bytes.fromhex('f2cb28eb9a29'), bytes.fromhex('f2cb')),
            (bytes.fromhex('28f35729eecc'), bytes.fromhex('eecc')),
        ]
        for source, target in surfaces:
            cmd = message(0x11, b'X' + source + b'Y')
            out, counts = transform_particle_command(cmd)
            self.assertEqual(sum(counts.values()), 1)
            self.assertIn(target, out)
            self.assertNotIn(source, out)
            self.assertEqual(len(cmd) - len(out), 4)
            self.assertEqual(cmd[:4], out[:4])

    def test_choice_preserves_choice_count_and_handles_multiple_fields(self):
        p1 = bytes.fromhex('f35a28ef4529')
        p2 = bytes.fromhex('f35928ed6129')
        cmd = choice(b'A' + p1, b'B' + p2)
        out, counts = transform_particle_command(cmd)
        self.assertEqual(out[1], 2)
        self.assertEqual(sum(counts.values()), 2)
        self.assertEqual(len(cmd) - len(out), 8)

    def test_apply_accepts_code3_original_and_choice_raw_ko(self):
        jp0 = message(0x11, b'JP')
        ko0 = message(0x11, b'K' + bytes.fromhex('f35928ed6129'))
        jp1 = choice(b'JP')
        ko1 = choice(b'K' + bytes.fromhex('f35a28ef4529'))
        original = parse_event_ts5(ts5(jp0 + jp1))
        korean_blob = ts5(ko0 + ko1)
        r0 = ParticleLedgerRecord(1, 0, 16, 16, 0x11, SEMANTIC_INCLUDE_KO_FIXED_SURFACE_PARTICLE, 1, 0, len(ko0), len(ko0)-4)
        r1 = ParticleLedgerRecord(2, 0, 16+len(jp0), 16+len(ko0), 0x15, SEMANTIC_INCLUDE_KO_CHOICE, 1, 1, len(ko1), len(ko1)-4)
        current = [[item.data for item in original.partitions[0].grouped_items]]
        current[0][1] = ko1
        solved, report = apply_fixed_surface_particles(original, korean_blob, current, (r0, r1), require_canonical=False)
        self.assertEqual(report.rows, 2)
        self.assertEqual(report.occurrences, 2)
        self.assertEqual(report.aggregate_shrink_bytes, 8)
        self.assertNotEqual(solved[0][0], jp0)
        self.assertNotEqual(solved[0][1], ko1)

    def test_wrong_preexisting_state_is_rejected(self):
        jp = message(0x11, b'JP')
        ko = message(0x11, b'K' + bytes.fromhex('f35928ed6129'))
        original = parse_event_ts5(ts5(jp))
        korean_blob = ts5(ko)
        rec = ParticleLedgerRecord(1, 0, 16, 16, 0x11, SEMANTIC_INCLUDE_KO_FIXED_SURFACE_PARTICLE, 1, 0, len(ko), len(ko)-4)
        current = [[item.data for item in original.partitions[0].grouped_items]]
        current[0][0] = b'\x11\x00\x00\x00' + field(b'OTHER')
        with self.assertRaises(SelectiveEventError) as cm:
            apply_fixed_surface_particles(original, korean_blob, current, (rec,), require_canonical=False)
        self.assertEqual(cm.exception.code, 'PARTICLE_CODE3_BASELINE_FAIL')


if __name__ == '__main__':
    unittest.main()
