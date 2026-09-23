from __future__ import annotations

from dataclasses import dataclass
import hashlib
import json
from pathlib import Path
from typing import Mapping

SUPPORTED_OPERATIONS = frozenset({'EXACT_REPLACE_MESSAGE', 'DELETE_EXACT_BYTE'})


class CorrectionOverlayError(RuntimeError):
    pass


@dataclass(frozen=True)
class MessageCorrection:
    candidate_id: str
    classification_id: str
    block: int
    local: int
    operation: str
    source_bytes: bytes
    source_sha256: str
    target_bytes: bytes
    target_sha256: str
    edit: Mapping[str, object] | None

    @property
    def locator(self) -> tuple[int, int]:
        return self.block, self.local


def _sha(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def _fail(message: str) -> None:
    raise CorrectionOverlayError(message)


def _guard_bytes(label: str, data: bytes, length: int, sha256: str) -> None:
    if len(data) != length or _sha(data) != sha256:
        _fail(f'{label} identity mismatch')


def _validate_operation(operation: str, source: bytes, target: bytes, edit: Mapping[str, object] | None) -> None:
    if operation == 'EXACT_REPLACE_MESSAGE':
        if edit not in (None, {}):
            _fail('EXACT_REPLACE_MESSAGE must not carry edit instructions')
        return
    if operation == 'DELETE_EXACT_BYTE':
        if not isinstance(edit, Mapping):
            _fail('DELETE_EXACT_BYTE requires edit metadata')
        offset = int(edit.get('byte_offset_zero_based', -1))
        expected = bytes.fromhex(str(edit.get('expected_byte_hex', '')))
        if len(expected) != 1 or offset < 0 or offset >= len(source):
            _fail('DELETE_EXACT_BYTE edit bounds/byte invalid')
        if source[offset:offset + 1] != expected:
            _fail('DELETE_EXACT_BYTE expected byte mismatch')
        following_hex = str(edit.get('expected_following_hex', ''))
        if following_hex:
            following = bytes.fromhex(following_hex)
            if source[offset + 1:offset + 1 + len(following)] != following:
                _fail('DELETE_EXACT_BYTE following guard mismatch')
        if source[:offset] + source[offset + 1:] != target:
            _fail('DELETE_EXACT_BYTE target mismatch')
        return
    _fail(f'unsupported correction operation: {operation}')


def load_overlay(index_path: Path, expected_source_identity: Mapping[str, object] | None = None) -> dict[tuple[int, int], MessageCorrection]:
    index = json.loads(index_path.read_text(encoding='utf-8'))
    if index.get('schema') != 'TAI5MSG_MESSAGE_CORRECTION_OVERLAY_V1':
        _fail('unexpected correction overlay schema')
    source_identity = index.get('source_identity')
    if expected_source_identity is not None and source_identity != dict(expected_source_identity):
        _fail('correction overlay source identity mismatch')
    meta = index.get('rows', {})
    rows_path = index_path.parent / str(meta.get('path', ''))
    payload = rows_path.read_bytes()
    _guard_bytes('correction rows transport', payload, int(meta.get('bytes', -1)), str(meta.get('sha256', '')))
    rows = [json.loads(line) for line in payload.decode('utf-8').splitlines() if line]
    if len(rows) != int(meta.get('row_count', -1)):
        _fail('correction row count mismatch')

    out: dict[tuple[int, int], MessageCorrection] = {}
    for row in rows:
        operation = str(row['operation'])
        if operation not in SUPPORTED_OPERATIONS:
            _fail(f'unsupported correction operation: {operation}')
        source = bytes.fromhex(row['source_message_hex'])
        target = bytes.fromhex(row['target_message_hex'])
        _guard_bytes('source message', source, int(row['source_message_length']), str(row['source_message_sha256']))
        _guard_bytes('target message', target, int(row['target_message_length']), str(row['target_message_sha256']))
        edit = row.get('edit')
        _validate_operation(operation, source, target, edit)
        correction = MessageCorrection(
            candidate_id=str(row['candidate_id']),
            classification_id=str(row['classification_id']),
            block=int(row['block']),
            local=int(row['local']),
            operation=operation,
            source_bytes=source,
            source_sha256=str(row['source_message_sha256']),
            target_bytes=target,
            target_sha256=str(row['target_message_sha256']),
            edit=edit,
        )
        if correction.locator in out:
            _fail(f'duplicate correction locator: {correction.locator}')
        out[correction.locator] = correction
    return out


def apply_correction(source: bytes, correction: MessageCorrection) -> bytes:
    if source != correction.source_bytes or _sha(source) != correction.source_sha256:
        _fail(f'correction source guard failed at {correction.locator}')
    _validate_operation(correction.operation, source, correction.target_bytes, correction.edit)
    return correction.target_bytes
