# TAI5MSG B24 V320 Eden Diagnostic Package Materialization — V321

Date: 2026-09-19 (KST)

Validation ID: `V321`

Parent canonical state:

`4a7c3a6d2f1fd83bd31b699c0f6184b0bed790b2` — V320 B24 native-wrap implementation / offline validation.

Status:

`CLOSED / DETERMINISTIC PACKAGE MATERIALIZED / DRIVE ROUNDTRIP VERIFIED / EDEN RUNTIME NOT RUN`

## 1. Scope

V321 materializes the isolated body-only Eden diagnostic package for V320.

Included:

- existing Mapping 10,036 ExeFS route;
- existing page mapper;
- existing Korean font;
- exact V320 selective TAI5MSG.

Explicitly excluded:

- B24 help-header/title runtime descriptor changes;
- ordinary non-B24 584-row reflow;
- inline 139;
- R2884 / R2885;
- TAI5MSG external-caller wait 191;
- EVENT / TS5;
- SNR;
- CWTDAT;
- names / yomi;
- pointer-56 expansion;
- unrelated translation cleanup.

No Eden/runtime execution occurs in V321.

## 2. V320 TAI5MSG authority

Required package payload:

```text
bytes   1,839,753 / 0x1C1289
sha256  fd4c8b9f527f67f667d5fded6bdb4703607b70e8b6addf1f41c5d11ebf93e85c
```

The V320 output is the already-closed canonical offline result from V320.

V321 re-hashed the exact Drive-cached V320 DAT before packaging and required this identity.

## 3. Package tree

Artifact:

`Taiko5DX_KR_SELECTIVE_V320_B24_EDEN_DIAG.zip`

Exact package tree:

```text
Taiko5DX_KR_SELECTIVE/
├─ SELECTIVE_PACKAGE_INFO.json
├─ exefs/
│  └─ D9120950C258610A746F4A31CE3A3B376DE393D9.ips
└─ romfs/
   ├─ TAI5MSG_JP.DAT
   └─ FONT/
      └─ FONT_JPN.G1T
```

Strict allowlist:

`PASS / 4 of 4 exact / no extra file`

## 4. Component identities

```text
SELECTIVE_PACKAGE_INFO.json
  bytes   1,667
  sha256  b6656120f868c52cc4aae5b8991300df0db57d60e608bd020119538958d18c19

ExeFS integrated IPS
  bytes   2,742
  sha256  6d6989b4d22a12f0bc54e78a45a79944a9aaa0a6523d7d15fc5dc6d3620aaab4

Korean FONT_JPN.G1T
  bytes   16,779,036
  sha256  c82d80dada61ce80db42f948eafd3eb5b8f3bed5725ceebbc1c0897246166932

V320 selective TAI5MSG
  bytes   1,839,753
  sha256  fd4c8b9f527f67f667d5fded6bdb4703607b70e8b6addf1f41c5d11ebf93e85c
```

The IPS and font bytes were recovered from the previously verified V317 package route and re-hashed during V321 materialization.

No new ExeFS action is introduced.

## 5. Deterministic ZIP

```text
filename  Taiko5DX_KR_SELECTIVE_V320_B24_EDEN_DIAG.zip
bytes     3,208,547
sha256    9520057a628b36149ea2ba1a24e3bcc236758d2629ca8b1de0b7e85cd94bcf29
entries   4
```

Two independent local builds used:

- stable lexicographic entry order;
- fixed timestamp `2026-09-18 00:00:00`;
- Unix mode `0644`;
- DEFLATE level 9;
- retained top-level package root.

Result:

`DETERMINISTIC_REBUILD = PASS_BYTE_IDENTICAL`

## 6. Drive transport

Path:

`Google Drive/GPT/태합입지전/V320_B24_EDEN_DIAG_PACKAGE/`

Folder ID:

`1hn7F59mAXQYADcm4KGRPg029u6sq1joG`

ZIP ID:

`1Rx-GwWZ6V_xgfEcCgZ912wrNZCCUk1-m`

Materialization report ID:

`1GIkCsftV5DW88xtgpUSKnPe27wxPtRGy`

ZIP roundtrip:

```text
local       3,208,547 / 9520057a628b36149ea2ba1a24e3bcc236758d2629ca8b1de0b7e85cd94bcf29
Drive back  3,208,547 / 9520057a628b36149ea2ba1a24e3bcc236758d2629ca8b1de0b7e85cd94bcf29
identity    PASS_BYTE_IDENTICAL
```

Report roundtrip:

```text
bytes    3,526
sha256   281392ca6990513322ca8cd7879b2346295905a899bec113f6f717a6ba289920
identity PASS_BYTE_IDENTICAL
```

## 7. Runtime representatives frozen for next scope

The V320 body-only runtime validation should prioritize:

```text
long-body regression        B24:M221
12-row boundary             B24:M242
12-row boundary             B24:M255
semantic preservation       B24:M227
semantic preservation       B24:M229
untouched control           B24:M232
known separate header issue B24:M228
```

M228 is included only as a known separate header/title observation.

The existing M228 header wrap must **not** be counted as V320 body-layout failure unless the body itself regresses.

## 8. Isolation boundary

This package contains the exact V320 body-layout TAI5MSG but **no B24 header/title runtime patch**.

Therefore the package tests one cause-family only:

`B24 body native-wrap reconstruction`

The following remain absent:

- PC `description_font` counterpart changes;
- PC `ui_width` counterpart changes;
- non-B24 584 reflow;
- all unrelated content/runtime families.

## 9. Closure

```text
V320 TAI5MSG identity             PASS
strict package allowlist          PASS
IPS identity                      PASS
font identity                     PASS
deterministic ZIP rebuild         PASS_BYTE_IDENTICAL
Drive ZIP roundtrip               PASS_BYTE_IDENTICAL
Drive report roundtrip            PASS_BYTE_IDENTICAL
header/title runtime patch        NOT INCLUDED
Eden/runtime execution            NOT RUN
```

## 10. 확정된 사실

- The V320 body-only Eden diagnostic package now exists.
- It contains the exact V320 canonical TAI5MSG.
- The ExeFS IPS and font are unchanged from the previously verified route.
- No non-B24 584-row reflow is included.
- No B24 help-header/title patch is included.
- ZIP and report both passed Drive roundtrip byte-identity checks.

## 11. 유력한 가설

The V320 package should remove the previously observed long B24 body overflow while leaving the known M228 help-header wrap unchanged.

This remains a runtime hypothesis.

## 12. 미확정 사항

- Eden visual result of M221/M242/M255 under the V320 package;
- physical Nintendo Switch / Atmosphere behavior;
- the separate B24 help-header/title fix.

## 13. 기각된 가설

- the V320 body diagnostic requires a header/title patch in the same package — REJECTED;
- non-B24 584 rows should be mixed into this diagnostic ZIP — REJECTED;
- the V317 ZIP can stand in for the V320 body diagnostic — REJECTED.

## 14. 관련 영향 범위

V321 changes package artifacts and documentation/state only.

No serializer logic, TAI5MSG content, ExeFS action, Mapping, page mapper, font byte, or translation content changes in V321.

## 15. Exact next scope

After a fresh explicit execution signal:

`TAI5MSG_B24_V320_EDEN_RUNTIME_VALIDATION`

Runtime validation must use the exact V321 ZIP identity:

`9520057a628b36149ea2ba1a24e3bcc236758d2629ca8b1de0b7e85cd94bcf29`

and must not introduce any unrelated change.

## 16. Repository write boundary

Any repository write remains restricted to:

`create_blob -> create_tree -> create_commit -> update_ref(force=false)`
