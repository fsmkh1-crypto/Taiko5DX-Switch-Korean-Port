# ECF00000 percent-macro TAI5MSG V357 Eden diagnostic package materialization — V358

Date: 2026-09-21 (KST)

```text
validation_id   V358
track           SWITCH_SELECTIVE_KOREANIZATION
parent          29cdc5f452630dba03c93cf1230da918d6d515c0 / V357
scope_kind      DIAGNOSTIC_PACKAGE_MATERIALIZATION
package         MATERIALIZED
drive_roundtrip PASS_BYTE_IDENTICAL
Eden/runtime    NOT RUN
hardware        NOT RUN
```

## 1. Scope

V358 materializes the existing four-file Eden classic-IPS diagnostic package route with the exact
V357 TAI5MSG payload. It does not alter IPS bytes, font bytes, EVENT payloads, Mapping, serializer
logic, or any unrelated content family.

This stage stops before Eden or physical Switch execution.

## 2. Package tree

Artifact:

`Taiko5DX_KR_SELECTIVE_V357_PERCENT_MACRO_EDEN_DIAG.zip`

Exact allowlist:

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

Strict allowlist: `PASS / 4 of 4 exact / no extra file`.

## 3. Component identities

```text
SELECTIVE_PACKAGE_INFO.json
  bytes   1,549
  sha256  6d134ff829fb577c95bb08b3c60f8b2a18afac2a75bb3bdf2ab2c0568b0d10f3

ExeFS integrated IPS
  bytes   2,742
  sha256  6d6989b4d22a12f0bc54e78a45a79944a9aaa0a6523d7d15fc5dc6d3620aaab4

Korean FONT_JPN.G1T
  bytes   16,779,036
  sha256  c82d80dada61ce80db42f948eafd3eb5b8f3bed5725ceebbc1c0897246166932

V357 selective TAI5MSG
  bytes   1,840,329 / 0x1C14C9
  sha256  ad91776d47c3170573bed063dd6677716833e3a138be27474373ef5d2782e794
```

The IPS and font identities are byte-identical to the verified V321 package route. The only product
payload change relative to V321 is the V357 TAI5MSG, which includes the exact 46-root B0 program
overlay on top of the inherited V320 TAI5MSG baseline.

## 4. Deterministic ZIP

```text
filename  Taiko5DX_KR_SELECTIVE_V357_PERCENT_MACRO_EDEN_DIAG.zip
bytes     3,208,934
sha256    04e5c57a889908d0e7059e44cbb14b62e95b45e019063fbfaba2e7acde5500a1
entries   4
```

Two independent builds used the inherited V321 deterministic packaging contract:

- lexicographically stable entry order;
- fixed timestamp `2026-09-18 00:00:00`;
- Unix mode `0644`;
- DEFLATE level 9;
- retained top-level package root.

Result: `DETERMINISTIC_REBUILD = PASS_BYTE_IDENTICAL`.

## 5. Drive transport

```text
path       Google Drive/GPT/태합입지전/V357_PERCENT_MACRO_EDEN_DIAG_PACKAGE/
folder ID  16v--Z_fPBBimKDWdO7X3RTexOWI6gCfv
ZIP ID     1-FVMaQLJ7biHzSsHFHy5WnwQaXjImbKE
report ID  1NW4v1nwr5zSsw6SjHjJt_z2-A2kw61Nd
```

ZIP roundtrip:

```text
local       3,208,934 / 04e5c57a889908d0e7059e44cbb14b62e95b45e019063fbfaba2e7acde5500a1
Drive back  3,208,934 / 04e5c57a889908d0e7059e44cbb14b62e95b45e019063fbfaba2e7acde5500a1
identity    PASS_BYTE_IDENTICAL
```

Report roundtrip:

```text
bytes    2,871
sha256   932cacef3f2a50291893a27cb035914541395e053ffc204579d0879a5cfe4ba0
identity PASS_BYTE_IDENTICAL
```

Git authority remains canonical. Drive stores the large package and its transport report.

## 6. Runtime representatives frozen for the next scope

The three original cross-carrier blockers are mandatory representatives:

```text
EVENT row 4743    %21 -> TAI5MSG B0:M349
EVENT row 5059    %15 -> TAI5MSG B0:M209
EVENT row 11440   %2A -> TAI5MSG B0:M395
```

A broader representative sample across the 46-root family must be selected from the existing V355
role ledger when the runtime scope starts; do not invent additional representatives in V358.

## 7. Isolation boundary

Included:

- existing Mapping 10,036 ExeFS route;
- existing page mapper and Korean font;
- inherited V320 TAI5MSG baseline;
- exact V357 B0 46-root percent-macro overlay.

Explicitly excluded:

- new IPS changes;
- new font changes;
- ordinary non-B24 584 reflow;
- inline 139;
- TAI5MSG external-caller wait 191;
- unrelated EVENT/SNR/CWTDAT/name/yomi/pointer work;
- any new translation cleanup.

## 8. 확정된 사실

1. The exact V357 TAI5MSG is packaged with the already-verified V321 IPS/font route.
2. Package allowlist is exactly four files.
3. IPS and font bytes are unchanged from V321.
4. Two independent ZIP builds are byte-identical.
5. ZIP Drive roundtrip and report Drive roundtrip are both byte-identical.
6. Eden and physical Switch runtime execution were not performed.

## 9. 유력한 가설

This package should expose the V357 Korean percent-macro root outputs at runtime while preserving
the inherited V320 package behavior.

This is a runtime hypothesis, not a V358 PASS condition.

## 10. 미확정 사항

- Eden boot/title and general selected-Korean route under this exact ZIP;
- runtime output for EVENT rows 4743, 5059 and 11440;
- broader representative behavior across the 46-root selector/direct-literal families;
- physical Switch / Atmosphere behavior.

## 11. 기각된 가설 / do-not-repeat

- modify IPS or font merely because the B0 roots changed — REJECTED;
- mix unrelated EVENT/reflow work into this diagnostic ZIP — REJECTED;
- reuse the stale V320 ZIP as the V357 diagnostic package — REJECTED;
- treat deterministic package/Drive PASS as runtime PASS — REJECTED.

## 12. 관련 영향 범위

Changed:

- diagnostic package ZIP;
- `SELECTIVE_PACKAGE_INFO.json` inside the ZIP;
- Drive package/report artifacts;
- V358 documentation/state.

Unchanged:

- serializer code after V357;
- V303 membership and V304/V315/V320 correction ownership;
- ExeFS IPS bytes;
- Korean font bytes;
- EVENT data;
- runtime/hardware state.

## 13. 수정 제안 / exact next scope

`ECF00000_PERCENT_MACRO_TAI5MSG_V357_EDEN_RUNTIME_VALIDATION`

The next scope must use this exact ZIP identity:

`04e5c57a889908d0e7059e44cbb14b62e95b45e019063fbfaba2e7acde5500a1`

and must not introduce unrelated changes. Runtime execution requires a fresh explicit user signal.
