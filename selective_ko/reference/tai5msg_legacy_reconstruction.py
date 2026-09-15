from __future__ import annotations

from collections import Counter
from dataclasses import asdict, dataclass
import hashlib
import struct

TAI5MSG_INPUT_SHA256 = "e3b4522a1047ff409e099b5ee197d7689279ea7472cb403d305b2507fec96090"
TAI5MSG_OUTPUT_SHA256 = "88181ec81a2062264a10a556e68f296acd6fbca5d84f81225ed9e8797afc7c38"
TAI5MSG_BLOCK_COUNT = 33
TAI5MSG_MESSAGE_COUNT = 14_832
TAI5MSG_EXPECTED_COMPACT_OCCURRENCES = 44
TAI5MSG_EXPECTED_CHANGED_MESSAGES = 33
TAI5MSG_EXPECTED_SIZE_GROWTH = 128
TAI5MSG_EXPECTED_AFFECTED_BLOCKS = {
    1: 4,
    2: 2,
    3: 2,
    4: 6,
    6: 1,
    8: 5,
    9: 8,
    10: 5,
    11: 1,
    13: 2,
    14: 1,
    15: 5,
    16: 2,
}
_BLOCK_ALIGNMENT = 0x40
_RAW_PRESERVE_ON = b"\x1b\x6b"
_RAW_PRESERVE_OFF = b"\x1b\x48"


@dataclass(frozen=True)
class Tai5MsgReconstructionReport:
    input_sha256: str
    output_sha256: str
    block_count: int
    message_count: int
    compact_occurrences: int
    changed_messages: int
    affected_blocks: int
    grown_blocks: int
    input_size: int
    output_size: int
    size_growth: int

    def to_dict(self) -> dict[str, int | str]:
        return asdict(self)


def _sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def _decrypt_block(data: bytes) -> bytes:
    return bytes((value + 0x5B) & 0xFF for value in data)


def _encrypt_block(data: bytes) -> bytes:
    return bytes((value - 0x5B) & 0xFF for value in data)


def _trailing_count(data: bytes, value: int) -> int:
    pos = len(data)
    while pos and data[pos - 1] == value:
        pos -= 1
    return len(data) - pos


def _is_game_two_byte_lead(value: int) -> bool:
    return 0x81 <= value <= 0x9F or 0xE0 <= value <= 0xFC


def _scan_compact_display_positions(message: bytes) -> list[tuple[int, str]]:
    positions: list[tuple[int, str]] = []
    state = "DEFAULT_OFF"
    pos = 0

    while pos < len(message):
        value = message[pos]

        if value == 0x02 and pos + 2 < len(message):
            pos += 3
            continue

        if value in (0x1A, 0x1B) and pos + 1 < len(message):
            sub = message[pos + 1]
            if value == 0x1B:
                if sub == 0x6B:
                    state = "ON"
                elif sub == 0x48:
                    state = "OFF_H"
                elif sub == 0x4B:
                    state = "OFF_K"
            if sub == 0x43 and pos + 2 < len(message):
                pos += 3
            else:
                pos += 2
            continue

        if value == 0x01 and pos + 1 < len(message):
            sub = message[pos + 1]
            if sub in (0x43, 0x4A) and pos + 3 < len(message):
                pos += 4
            else:
                pos += 2
            continue

        if (
            value == 0x05
            and pos + 2 < len(message)
            and message[pos + 1] == 0x05
            and 0x04 <= message[pos + 2] <= 0x09
        ):
            pos += 3
            continue

        if _is_game_two_byte_lead(value) and pos + 1 < len(message):
            pos += 2
            continue

        if 0xA6 <= value <= 0xDF:
            positions.append((pos, state))

        pos += 1

    return positions


def _parse_header(blob: bytes) -> list[tuple[int, int]]:
    if len(blob) < 0x140:
        raise RuntimeError("TAI5MSG is too short")
    pairs = [struct.unpack_from("<II", blob, index * 8) for index in range(TAI5MSG_BLOCK_COUNT)]
    if pairs[0][0] != 0x140:
        raise RuntimeError("TAI5MSG first block offset guard failed")
    for index in range(TAI5MSG_BLOCK_COUNT - 1):
        off, size = pairs[index]
        next_off = pairs[index + 1][0]
        if off % _BLOCK_ALIGNMENT or size % _BLOCK_ALIGNMENT:
            raise RuntimeError("TAI5MSG block alignment guard failed")
        if off + size != next_off:
            raise RuntimeError("TAI5MSG block contiguity guard failed")
    if pairs[-1][0] >= len(blob):
        raise RuntimeError("TAI5MSG final block offset guard failed")
    return pairs


def _parse_block(
    blob: bytes,
    pairs: list[tuple[int, int]],
    block_index: int,
) -> tuple[bytes, int, list[int], list[bytes], int]:
    off, declared_size = pairs[block_index]
    physical_end = pairs[block_index + 1][0] if block_index + 1 < len(pairs) else len(blob)
    raw = blob[off:physical_end]
    decoded = _decrypt_block(raw)
    if len(decoded) < 2:
        raise RuntimeError(f"TAI5MSG block {block_index} is truncated")

    message_count = struct.unpack_from("<H", decoded, 0)[0]
    table_end = 2 + 4 * message_count
    if table_end > len(decoded):
        raise RuntimeError(f"TAI5MSG block {block_index} offset table is truncated")

    offsets = [
        struct.unpack_from("<I", decoded, 2 + 4 * index)[0]
        for index in range(message_count)
    ]
    if not offsets or offsets[0] != table_end or offsets != sorted(offsets):
        raise RuntimeError(f"TAI5MSG block {block_index} message offsets are invalid")

    trailing = _trailing_count(decoded, 0x5B)
    core_end = len(decoded) - trailing
    if offsets[-1] >= core_end:
        raise RuntimeError(f"TAI5MSG block {block_index} final message offset is invalid")

    messages = []
    for index, start in enumerate(offsets):
        end = offsets[index + 1] if index + 1 < message_count else core_end
        if not start < end <= core_end:
            raise RuntimeError(f"TAI5MSG block {block_index} message boundary is invalid")
        messages.append(decoded[start:end])

    return raw, declared_size, offsets, messages, trailing


def reconstruct_tai5msg_switch_native(
    blob: bytes,
) -> tuple[bytes, Tai5MsgReconstructionReport]:
    input_sha = _sha256(blob)
    if input_sha != TAI5MSG_INPUT_SHA256:
        raise RuntimeError(
            "TAI5MSG input hash guard failed; only the canonical PC patch v1.02 payload is supported"
        )

    pairs = _parse_header(blob)
    parsed = []
    message_total = 0
    targets: dict[tuple[int, int], list[int]] = {}
    affected_histogram: Counter[int] = Counter()

    for block_index in range(TAI5MSG_BLOCK_COUNT):
        raw, declared_size, offsets, messages, trailing = _parse_block(blob, pairs, block_index)
        parsed.append((raw, declared_size, offsets, messages, trailing))
        message_total += len(messages)
        for local_index, message in enumerate(messages):
            scanned = _scan_compact_display_positions(message)
            unsafe_states = [state for _pos, state in scanned if state not in ("DEFAULT_OFF", "OFF_H")]
            if unsafe_states:
                raise RuntimeError(
                    "TAI5MSG canonical input contains a susceptible compact byte in an unexpected preservation state"
                )
            positions = [pos for pos, _state in scanned]
            if positions:
                targets[(block_index, local_index)] = positions
                affected_histogram[block_index] += len(positions)

    if message_total != TAI5MSG_MESSAGE_COUNT:
        raise RuntimeError("TAI5MSG message-count guard failed")
    if sum(len(positions) for positions in targets.values()) != TAI5MSG_EXPECTED_COMPACT_OCCURRENCES:
        raise RuntimeError("TAI5MSG compact-byte occurrence guard failed")
    if len(targets) != TAI5MSG_EXPECTED_CHANGED_MESSAGES:
        raise RuntimeError("TAI5MSG changed-message guard failed")
    if dict(sorted(affected_histogram.items())) != TAI5MSG_EXPECTED_AFFECTED_BLOCKS:
        raise RuntimeError("TAI5MSG affected-block census guard failed")

    rebuilt_blocks: list[bytes] = []
    new_sizes: list[int] = []
    grown_blocks = 0

    for block_index, (raw, declared_size, offsets, messages, trailing) in enumerate(parsed):
        if block_index not in affected_histogram:
            rebuilt_blocks.append(raw)
            new_sizes.append(declared_size)
            continue

        count = len(messages)
        table_end = 2 + 4 * count
        updated_messages: list[bytes] = []
        for local_index, message in enumerate(messages):
            positions = targets.get((block_index, local_index), [])
            updated = message
            for position in sorted(positions, reverse=True):
                updated = (
                    updated[:position]
                    + _RAW_PRESERVE_ON
                    + updated[position:position + 1]
                    + _RAW_PRESERVE_OFF
                    + updated[position + 1:]
                )
            updated_messages.append(updated)

        used = table_end + sum(len(message) for message in updated_messages)
        new_size = declared_size
        while used > new_size:
            new_size += _BLOCK_ALIGNMENT
        if new_size != declared_size:
            grown_blocks += 1

        new_offsets = []
        cursor = table_end
        for message in updated_messages:
            new_offsets.append(cursor)
            cursor += len(message)
        if cursor != used:
            raise RuntimeError("TAI5MSG reconstruction cursor mismatch")

        decoded = bytearray()
        decoded += struct.pack("<H", count)
        for offset in new_offsets:
            decoded += struct.pack("<I", offset)
        for message in updated_messages:
            decoded += message
        decoded += bytes([0x5B]) * (new_size - len(decoded))
        if len(decoded) != new_size:
            raise RuntimeError("TAI5MSG rebuilt block size mismatch")

        rebuilt_blocks.append(_encrypt_block(bytes(decoded)))
        new_sizes.append(new_size)

    new_offsets = [pairs[0][0]]
    for index in range(1, TAI5MSG_BLOCK_COUNT):
        new_offsets.append(new_offsets[-1] + new_sizes[index - 1])

    header = bytearray(blob[:pairs[0][0]])
    for index in range(TAI5MSG_BLOCK_COUNT):
        struct.pack_into("<II", header, index * 8, new_offsets[index], new_sizes[index])

    rebuilt = bytes(header) + b"".join(rebuilt_blocks)

    output_sha = _sha256(rebuilt)
    size_growth = len(rebuilt) - len(blob)
    if size_growth != TAI5MSG_EXPECTED_SIZE_GROWTH:
        raise RuntimeError("TAI5MSG output-size guard failed")
    if grown_blocks != 2:
        raise RuntimeError("TAI5MSG grown-block count guard failed")
    if output_sha != TAI5MSG_OUTPUT_SHA256:
        raise RuntimeError("TAI5MSG deterministic output hash guard failed")

    new_pairs = _parse_header(rebuilt)
    new_message_total = 0
    for block_index in range(TAI5MSG_BLOCK_COUNT):
        _raw, _declared, _offsets, messages, _trailing = _parse_block(
            rebuilt, new_pairs, block_index
        )
        new_message_total += len(messages)
    if new_message_total != TAI5MSG_MESSAGE_COUNT:
        raise RuntimeError("TAI5MSG post-reconstruction parse guard failed")

    protected_after = 0
    unprotected_after = 0
    for block_index in range(TAI5MSG_BLOCK_COUNT):
        _raw, _declared, _offsets, messages, _trailing = _parse_block(
            rebuilt, new_pairs, block_index
        )
        for message in messages:
            for _pos, state in _scan_compact_display_positions(message):
                if state == "ON":
                    protected_after += 1
                else:
                    unprotected_after += 1
    if protected_after != TAI5MSG_EXPECTED_COMPACT_OCCURRENCES or unprotected_after != 0:
        raise RuntimeError("TAI5MSG post-reconstruction preservation-state guard failed")

    report = Tai5MsgReconstructionReport(
        input_sha256=input_sha,
        output_sha256=output_sha,
        block_count=TAI5MSG_BLOCK_COUNT,
        message_count=TAI5MSG_MESSAGE_COUNT,
        compact_occurrences=TAI5MSG_EXPECTED_COMPACT_OCCURRENCES,
        changed_messages=TAI5MSG_EXPECTED_CHANGED_MESSAGES,
        affected_blocks=len(affected_histogram),
        grown_blocks=grown_blocks,
        input_size=len(blob),
        output_size=len(rebuilt),
        size_growth=size_growth,
    )
    return rebuilt, report
