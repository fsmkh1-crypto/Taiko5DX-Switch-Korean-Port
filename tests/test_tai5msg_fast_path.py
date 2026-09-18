from __future__ import annotations

import hashlib
import json
from pathlib import Path
import tempfile
import unittest

from builder.tai5msg_corrections import CorrectionOverlayError, apply_correction, load_overlay
from tools.tai5msg_inspect import load_cache


def _sha(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


class Tai5MsgFastPathTests(unittest.TestCase):
    def test_git_anchor_cache_integrity_and_m229(self) -> None:
        repo_root = Path(__file__).resolve().parents[1]
        index = repo_root / 'selective_ko/artifacts/tai5msg_fast_source_cache_v1/INDEX.json'
        meta, rows, kind = load_cache(index)
        self.assertEqual(kind, 'GIT_ANCHOR_CACHE')
        self.assertEqual(len(rows), 3)
        self.assertEqual(meta['git_anchor_cache']['locators'], [
            'TAI5MSG:B24:M227', 'TAI5MSG:B24:M228', 'TAI5MSG:B24:M229'
        ])
        m229 = next(row for row in rows if row['local'] == 229)
        self.assertIn('軍資金調達', m229['jp']['decoded'])
        self.assertIn('교역품 수송', m229['pc_ko']['decoded'])
        self.assertEqual(m229['jp']['sha256'], 'd2c98a7fc6db1d87f2e173c75abd71155ec39d1259841754adf3fe9aa0943661')

    def _overlay(self, operation: str, source: bytes, target: bytes, edit: dict | None = None):
        td = tempfile.TemporaryDirectory()
        root = Path(td.name)
        row = {
            'candidate_id': 'SEL-CAND-TEST',
            'classification_id': 'SEL-CLS-TEST',
            'block': 24,
            'local': 229,
            'operation': operation,
            'source_message_length': len(source),
            'source_message_sha256': _sha(source),
            'source_message_hex': source.hex(),
            'target_message_length': len(target),
            'target_message_sha256': _sha(target),
            'target_message_hex': target.hex(),
        }
        if edit is not None:
            row['edit'] = edit
        payload = (json.dumps(row, separators=(',', ':')) + '\n').encode()
        (root / 'ROWS.jsonl').write_bytes(payload)
        index = {
            'schema': 'TAI5MSG_MESSAGE_CORRECTION_OVERLAY_V1',
            'source_identity': {'size': 1, 'sha256': 'test'},
            'rows': {
                'path': 'ROWS.jsonl',
                'bytes': len(payload),
                'sha256': _sha(payload),
                'row_count': 1,
            },
        }
        (root / 'INDEX.json').write_text(json.dumps(index), encoding='utf-8')
        return td, root

    def test_exact_replace_message(self) -> None:
        td, root = self._overlay('EXACT_REPLACE_MESSAGE', b'abc', b'xyz')
        with td:
            correction = load_overlay(root / 'INDEX.json')[(24, 229)]
            self.assertEqual(apply_correction(b'abc', correction), b'xyz')

    def test_delete_exact_byte(self) -> None:
        source = b'abXc'
        target = b'abc'
        edit = {'byte_offset_zero_based': 2, 'expected_byte_hex': '58', 'expected_following_hex': '63'}
        td, root = self._overlay('DELETE_EXACT_BYTE', source, target, edit)
        with td:
            correction = load_overlay(root / 'INDEX.json')[(24, 229)]
            self.assertEqual(apply_correction(source, correction), target)

    def test_source_guard_fails(self) -> None:
        td, root = self._overlay('EXACT_REPLACE_MESSAGE', b'abc', b'xyz')
        with td:
            correction = load_overlay(root / 'INDEX.json')[(24, 229)]
            with self.assertRaises(CorrectionOverlayError):
                apply_correction(b'abd', correction)


if __name__ == '__main__':
    unittest.main()
