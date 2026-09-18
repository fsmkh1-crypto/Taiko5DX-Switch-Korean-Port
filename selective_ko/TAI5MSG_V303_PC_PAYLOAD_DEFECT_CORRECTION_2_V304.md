# TAI5MSG V303 PC PAYLOAD DEFECT CORRECTION 2 — V304

Date: 2026-09-18 (KST)
Status: CANONICAL CORRECTION OVERLAY MATERIALIZED / 2 ROWS / NO NEW IDs / NO BUILDER / NO BUILD
Track: `SWITCH_SELECTIVE_KOREANIZATION`
Validation ID: `V304`
Parent: `b999fea1ba121f91200efd4ac4e483cc1b3a13a0`

## 1. Purpose

V304 materializes the two source-payload corrections proven by the bounded read-only scope `TAI5MSG_V303_FB05_CONTROL_TOKEN_PROVENANCE_READ_ONLY`.

It does not rewrite the historical V303 row artifact. V303 membership, candidate IDs, classification IDs and `INCLUDE_KO` dispositions remain immutable.

Instead V304 is an exact target-payload override layer for only:

```text
SEL-CAND/SEL-CLS-000669  TAI5MSG:B19:M058
SEL-CAND/SEL-CLS-002816  TAI5MSG:B30:M058
```

## 2. 확정된 사실

Canonical PC Korean v1.02 TAI5MSG:

```text
size    2,134,366
sha256  e3b4522a1047ff409e099b5ee197d7689279ea7472cb403d305b2507fec96090
```

The two selected messages end with the malformed byte sequence:

```text
... 2E FB 05 05 05
       ^^
```

The corresponding JP/SC/TW slots do not end in `FB 05 05 05`.

Normal JP `FB A7` is a valid mapped two-byte game code and maps to `U+8ABE`. This does not authorize `FB 05`.

The verified PC runtime byte-processing rule treats `FB` as an eligible two-byte lead because it lies in `E0..FC`, but `05` is not a valid trail because valid trails are `40..7E` or `80..FC`. Therefore `FB 05` is not a normal handled two-byte character and falls back to the original path.

Mapping 10,036 contains no `FB05` entry.

The exact corrections are:

```text
B19:58
source length  207
source sha256  3ff24bb71b0b2754a7404a00189bd8d5b328de540a29356c36dca076cc361c01
delete          byte 0xFB at zero-based message offset 203
target length  206
target sha256  779701b92009fae908d94f4ec5a5239c1cc78101db80e3e0ea76a1e8172d827f

B30:58
source length  209
source sha256  cfcc3a761137f3251bd190366299e49ab5498cd48eeb3fe53e6b4c3c8171c085
delete          byte 0xFB at zero-based message offset 205
target length  208
target sha256  6baf9274bcb4cf2d7b7102e79a17d5e18988d3032bbf84d11781eddd01f642c5
```

The complete source and corrected target message bytes are materialized in:

`selective_ko/artifacts/tai5msg_v303_pc_payload_defect_correction_2_v1/ROWS.jsonl`

## 3. 유력한 가설

The two slots are duplicate/parallel biography payloads and share the same Korean body ending. A translation/export or source-reconstruction defect likely left one original lead byte `FB` immediately before the normal `05 05 05` message-ending sequence.

The exact historical authoring/tool cause is not required for the payload-defect verdict.

## 4. 미확정 사항

The exact editor/export step that introduced the stray `FB` remains unknown.

The full PC Korean TAI5MSG contains additional `... FB 05 05 05` occurrences outside the V303 release population. V304 does not classify, correct or authorize changes to those out-of-scope rows.

## 5. 기각된 가설

```text
FB is a standalone Korean control token                    REJECTED
FB05 is a valid Mapping 10,036 Korean character            REJECTED
the normal JP FBA7 character authorizes KO FB05            REJECTED
05 05 05 are proven FB parameters                          REJECTED
the defect requires changing V303 membership/disposition   REJECTED
```

## 6. 관련 영향 범위

V303 membership remains exactly:

```text
TAI5MSG release rows       3,179
R1                         3,158
R2                            21
candidate/classification   unchanged
INCLUDE_KO                 unchanged
```

Project cumulative counts remain:

```text
candidate IDs       3,318
classification IDs  3,318
INCLUDE_KO rows     3,318
```

Only the target payload for two already-approved rows changes.

The correction removes one byte in B19 and one byte in B30. It does not create a new block-capacity problem and does not authorize any new row.

## 7. 수정 제안 — materialized correction contract

A future selective builder must process these two rows fail-closed:

```text
1. resolve the V303 target by exact locator;
2. require the full canonical PC-KO file SHA-256;
3. require the exact V304 source message length and SHA-256;
4. require byte FB at the exact recorded offset;
5. require following bytes 05 05 05;
6. apply exactly one-byte deletion;
7. require exact corrected target length and SHA-256;
8. on any mismatch: ABORT, never guess or silently skip.
```

For the other 3,177 V303 TAI5MSG rows, V304 grants no payload transformation.

Effective future build rule:

```text
3,177 rows  -> exact canonical PC-KO locator payload
2 rows      -> exact V304 corrected payload
-----------------------------------------------
3,179 rows  -> V303 release membership unchanged
```

## 8. Artifact

Machine-readable authority:

`selective_ko/artifacts/tai5msg_v303_pc_payload_defect_correction_2_v1/INDEX.json`

Exact row payloads:

`selective_ko/artifacts/tai5msg_v303_pc_payload_defect_correction_2_v1/ROWS.jsonl`

```text
row count   2
ROWS bytes  4,582
ROWS sha256 17714de6f54c6e8eeab85166845394344bbb283392d7ec19d24b294e7869ac52
```

## 9. Claim boundary

V304 authorizes only the two correction payload definitions as canonical data.

It does not implement:

- the selective TAI5MSG serializer;
- Mapping 10,036 integration;
- font/runtime integration;
- RomFS output;
- IPS/build/package;
- hardware execution.

## 10. Next scope

The canonical next implementation-oriented analysis remains:

`TAI5MSG_3179_SELECTIVE_BUILDER_SERIALIZER_DESIGN_READ_ONLY`

V304 must be treated as an input overlay in that design.

A fresh explicit user signal remains required for any implementation or further repository materialization.

## 11. Repository write boundary

`create_blob -> create_tree -> create_commit -> update_ref(force=false)`

No Contents-API write, branch creation, issue/PR write, or force update is permitted.
