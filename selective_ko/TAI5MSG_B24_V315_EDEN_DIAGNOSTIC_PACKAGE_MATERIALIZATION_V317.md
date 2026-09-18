# TAI5MSG B24 V315 Eden Diagnostic Package Materialization — V317

Date: 2026-09-18 (KST)

Validation ID: `V317`

Parent canonical state:

`17a4dae83db97e8dfb6fefd6a9df9e525886b311` — V316 B24 V315 Eden diagnostic package design.

Status:

`CLOSED / DETERMINISTIC PACKAGE MATERIALIZED / DRIVE ROUNDTRIP VERIFIED / HARDWARE NOT RUN`

## 1. Scope

V317 materializes exactly the V316 one-cause-family diagnostic package for runtime validation of the V315 B24 correction.

No ordinary non-B24 reflow, inline 139, or unrelated content family is added.

No Eden or hardware execution is performed in V317.

## 2. V315 TAI5MSG materialization guard

The package TAI5MSG is required to be:

```text
bytes   1,840,073 / 0x1C13C9
sha256  b212da65010d3a2e7ff6f7b8e10ce57371cb67e3093f58a6ad16a085399a8d0d
```

Before packaging, V317 independently replayed the V315 delta against the exact V312 pre-V315 selective TAI5MSG:

```text
V312 source sha256                 dfcb928f694117bdd51e69d25daf337c14e30c3a7078da3961dc3a570ffe44f9
V315 overlay rows                  109
source guards                      PASS 109 / 109
actual changed locators            B24 only / 109
replayed output sha256             b212da65010d3a2e7ff6f7b8e10ce57371cb67e3093f58a6ad16a085399a8d0d
byte-identical to stored V315 DAT  PASS
```

This is an independent delta replay of the already-closed V315 correction, not a new semantic/layout transformation.

## 3. Package tree

Artifact:

`Taiko5DX_KR_SELECTIVE_V315_B24_EDEN_DIAG.zip`

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
  bytes   1,601
  sha256  6de45c52475ccba2c5b42a32a6e52a7c36fc3458b836f78c682c3971f9c28f62

ExeFS integrated IPS
  bytes   2,742
  sha256  6d6989b4d22a12f0bc54e78a45a79944a9aaa0a6523d7d15fc5dc6d3620aaab4

Korean FONT_JPN.G1T
  bytes   16,779,036
  sha256  c82d80dada61ce80db42f948eafd3eb5b8f3bed5725ceebbc1c0897246166932

V315 selective TAI5MSG
  bytes   1,840,073
  sha256  b212da65010d3a2e7ff6f7b8e10ce57371cb67e3093f58a6ad16a085399a8d0d
```

The IPS and font bytes are the previously validated V312 route and were re-hashed during V317 materialization.

## 5. Deterministic ZIP

```text
filename  Taiko5DX_KR_SELECTIVE_V315_B24_EDEN_DIAG.zip
bytes     3,208,715
sha256    aded0ebc67a1ac8bfc57351c418e7d447188cfce2e7f36b9d8b234f40979d614
entries   4
```

Two independent builds used the frozen V316 deterministic ZIP rules and produced byte-identical output.

Result:

`DETERMINISTIC_REBUILD = PASS`

## 6. Drive transport

Path:

`Google Drive/GPT/태합입지전/V315_B24_EDEN_DIAG_PACKAGE/`

Folder ID:

`1OkWLL79YXd7PcU8TDyvR04cpjFaQdoo3`

Uploaded ZIP ID:

`1429gxzGOw8ap9iPdjcdf-uGXhFGsUtVM`

Materialization report ID:

`1o7DgwxpB1SQ45WaX6woL9mVobTwL2l-n`

ZIP roundtrip:

```text
local       3,208,715 / aded0ebc67a1ac8bfc57351c418e7d447188cfce2e7f36b9d8b234f40979d614
Drive back  3,208,715 / aded0ebc67a1ac8bfc57351c418e7d447188cfce2e7f36b9d8b234f40979d614
identity    PASS_BYTE_IDENTICAL
```

Report roundtrip:

```text
bytes   2,521
sha256  27954591daa6e1828b3c79231554f2e1f336ed295c2c2ca3fca79cd9bbf96c1e
identity PASS_BYTE_IDENTICAL
```

## 7. Runtime representatives frozen for next scope

The V315 correction artifact was read at materialization time.

Runtime representatives are:

```text
semantic correction   B24:M227
semantic correction   B24:M228
semantic correction   B24:M229
layout-only            B24:M221
untouched control      B24:M232
```

M221 is an actual `SEMANTIC_PRESERVED_LAYOUT_RECONSTRUCTION` row from the V315 correction artifact.

M232 is one of the 15 untouched B24 control rows.

## 8. Isolation boundary

Explicitly absent from this package:

- ordinary non-B24 overflow/reflow 584 rows;
- B0/B21 width investigation;
- inline 139;
- R2884 / R2885;
- TAI5MSG external-caller waits 191;
- EVENT / TS5;
- SNR;
- CWTDAT;
- names / yomi;
- pointer-56 expansion;
- unrelated translation cleanup.

## 9. Closure

```text
V315 TAI5MSG identity                   PASS
V315 independent delta replay           PASS_BYTE_IDENTICAL
strict package allowlist                PASS
IPS identity                            PASS
font identity                           PASS
deterministic ZIP rebuild               PASS_BYTE_IDENTICAL
Drive ZIP roundtrip                     PASS_BYTE_IDENTICAL
Drive report roundtrip                  PASS_BYTE_IDENTICAL
hardware / Eden runtime                 NOT RUN
```

## 10. 확정된 사실

- The V315 B24 diagnostic package now exists and is transport-verified.
- The package carries exactly the V315 B24 correction and no non-B24 584-row reflow.
- The runtime test representatives are fixed to M227, M228, M229, M221 and M232.
- V312 package remains historical/stale for B24 diagnosis.

## 11. 유력한 가설

The V315 B24 common-cause correction should remove the flattened-layout / wrong-slot symptoms while preserving the existing Mapping 10,036, page mapper and font route.

This remains a runtime hypothesis.

## 12. 미확정 사항

- Eden boot/runtime behavior of this exact V317 package;
- visual section/layout behavior for M221/M227/M229;
- whether the effective runtime viewport imposes a stricter constraint than the audited 40-unit model.

## 13. 기각된 가설

- non-B24 584-row reflow must be mixed into this diagnostic build — REJECTED;
- V312 ZIP can stand in for V317 — REJECTED;
- Drive upload alone is sufficient without roundtrip — REJECTED;
- offline materialization alone proves runtime success — REJECTED.

## 14. 관련 영향 범위

V317 changes package artifacts and documentation/state only.

No new translation, serializer behavior, ExeFS action, font bytes, or non-B24 payload is introduced.

## 15. Exact next scope

After a new explicit execution signal:

`TAI5MSG_B24_V315_EDEN_RUNTIME_VALIDATION`

The runtime validation must use the exact ZIP SHA-256:

`aded0ebc67a1ac8bfc57351c418e7d447188cfce2e7f36b9d8b234f40979d614`

and must not introduce any unrelated content change.

## 16. Repository write boundary

Any repository write remains restricted to:

`create_blob -> create_tree -> create_commit -> update_ref(force=false)`
