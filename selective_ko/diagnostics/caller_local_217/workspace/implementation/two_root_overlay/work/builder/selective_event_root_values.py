"""Derive ROOT evidence from serialized TAI5MSG, never caller-decoded buffers.

Read-only structural/value evidence. Admission and cross-carrier acceptance stay
with the frozen catalog and the existing obligation engine, respectively.
"""
from pathlib import Path

from . import selective_tai5msg as codec
from .selective_event_contracts import ContractError, Span, require, sha256


class SerializedRootValues:
    """Evaluation-local cache over one immutable serialized candidate artifact."""

    def __init__(self, data: bytes):
        require(type(data) is bytes, 'ROOT_SERIALIZED_BYTES_REQUIRED', '')
        self.data = data
        try:
            self.parsed = codec.parse_tai5msg(data)
        except codec.SelectiveTai5MsgError as ex:
            raise ContractError('ROOT_SERIALIZED_STRUCTURE_INVALID', str(ex)) from ex
        self.artifact_sha256 = sha256(data)
        self.parser_sha256 = sha256(Path(codec.__file__).read_bytes())
        self.receipt_code_sha256 = sha256(Path(__file__).read_bytes())

    def value(self, block: int, local: int, physical_span: Span):
        require(type(block) is int and type(local) is int and
                0 <= block < len(self.parsed.blocks), 'ROOT_STRUCTURAL_INDEX', (block, local))
        b = self.parsed.blocks[block]
        require(0 <= local < b.message_count, 'ROOT_STRUCTURAL_INDEX', (block, local))
        start = b.offsets[local]
        end = b.offsets[local + 1] if local + 1 < b.message_count else b.used_end
        derived = Span(b.file_offset + start, b.file_offset + end)
        require(physical_span == derived, 'ROOT_STRUCTURAL_LOCATOR_MISMATCH', (block, local))
        decoded = b.messages[local]
        encoded_block = self.data[b.file_offset:b.file_offset + b.physical_size]
        decoded_block = codec._decrypt(encoded_block)
        return decoded, {
            'schema': 'SERIALIZED_ROOT_VALUE_RECEIPT_V1',
            'serialized_artifact_sha256': self.artifact_sha256,
            'serialized_artifact_bytes': len(self.data),
            'parser_source_sha256': self.parser_sha256,
            'receipt_source_sha256': self.receipt_code_sha256,
            'decoder': 'BYTE_ADD_0X5B_MOD_256',
            'block': block, 'local': local,
            'block_table_entry_range': [block * 8, block * 8 + 8],
            'block_table_sha256': sha256(self.parsed.header),
            'block_physical_range': [b.file_offset, b.file_offset + b.physical_size],
            'block_declared_bytes': b.declared_size,
            'block_encoded_sha256': sha256(encoded_block),
            'block_decoded_sha256': sha256(decoded_block),
            'message_count': b.message_count,
            'decoded_offset_entry_range': [2 + 4 * local, 6 + 4 * local],
            'decoded_offset_entry_value': start,
            'decoded_end_basis': 'NEXT_LOCAL_OFFSET' if local + 1 < b.message_count else 'PARSED_USED_END',
            'decoded_message_range': [start, end],
            'physical_encoded_range': [derived.start, derived.end],
            'encoded_value_sha256': sha256(self.data[derived.start:derived.end]),
            'decoded_value_sha256': sha256(decoded),
            'decoded_value_bytes': len(decoded),
            'block_used_end': b.used_end,
            'block_physical_filler_bytes': b.physical_filler_bytes,
            'block_declared_minus_physical': b.declared_minus_physical,
        }
