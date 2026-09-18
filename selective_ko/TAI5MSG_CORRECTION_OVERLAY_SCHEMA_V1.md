# TAI5MSG MESSAGE CORRECTION OVERLAY V1

Date: 2026-09-18 (KST)  
Status: CANONICAL SCHEMA / UTILITY AVAILABLE / EXISTING V304 PATH NOT MIGRATED

## 1. Purpose

This schema prevents future PC-source payload defects from requiring one-off serializer code for every defect family.

It does **not** change V303 membership, classification, or `INCLUDE_KO` counts. It only describes exact replacement payloads for rows that are already admitted.

Existing V304 behavior remains unchanged in V314. The generic loader in `builder/tai5msg_corrections.py` is prepared for later overlays and for an explicitly authorized V304 migration.

## 2. Index contract

```json
{
  "schema": "TAI5MSG_MESSAGE_CORRECTION_OVERLAY_V1",
  "source_identity": {"size": 0, "sha256": "..."},
  "rows": {
    "path": "ROWS.jsonl",
    "bytes": 0,
    "sha256": "...",
    "row_count": 0
  }
}
```

The row transport is UTF-8 JSONL. Row order is deterministic and the index guards exact byte size, SHA-256, and row count.

## 3. Row contract

Every row carries:

```text
candidate_id
classification_id
block
local
operation
source_message_length
source_message_sha256
source_message_hex
target_message_length
target_message_sha256
target_message_hex
optional edit metadata
```

The source file identity belongs in the index. Source-message identity and full source bytes belong in each row. Application is fail-closed.

## 4. Supported operations

### `EXACT_REPLACE_MESSAGE`

Use when the canonical PC payload is semantically wrong, displaced, missing, or must be replaced by an independently proven exact target message.

The operation performs no transformation heuristic. After source guards pass, the exact recorded target bytes are returned.

### `DELETE_EXACT_BYTE`

Compatibility operation for V304-style defects. Required edit fields are:

```text
byte_offset_zero_based
expected_byte_hex
optional expected_following_hex
```

The loader proves that deleting exactly that byte produces the recorded target bytes.

## 5. Safety invariants

A consumer must:

1. guard the source TAI5MSG file identity before resolving rows;
2. guard exact source-message length, SHA-256 and bytes;
3. reject unknown operations;
4. prove operation-specific edit semantics;
5. guard exact target-message length, SHA-256 and bytes;
6. reject duplicate locators;
7. abort on any mismatch rather than guessing or silently skipping.

Overlay application does not itself authorize reflow, membership changes, new translations, package building, or runtime delivery.

## 6. V314 implementation boundary

`builder/tai5msg_corrections.py` implements schema parsing and per-message fail-closed application.

V314 intentionally does **not** replace the currently verified V304 path in `builder/selective_tai5msg.py`. That migration would touch the production serializer and therefore remains a separate explicitly authorized implementation scope.
