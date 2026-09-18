# TAI5MSG B24 V315 Eden Diagnostic Package Design — V316

Date: 2026-09-18 (KST)

Validation ID: `V316`

Parent canonical state:

`a9464048a20c56ccb5bfa32c7e28a672de5bea5c` — V315 B24 semantic/layout correction implementation + offline validation.

Status:

`CLOSED / DESIGN ONLY / PACKAGE NOT MATERIALIZED / HARDWARE NOT RUN`

## 1. Scope

V316 freezes the exact diagnostic-package contract for runtime validation of the V315 B24 correction.

V316 does not build a ZIP, does not emit or alter IPS bytes, does not execute Eden, and does not modify any product payload.

The next execution scope remains:

`TAI5MSG_B24_V315_EDEN_DIAGNOSTIC_PACKAGE_MATERIALIZATION`

## 2. Inherited V315 payload authority

The diagnostic package must consume the already-validated V315 TAI5MSG output exactly:

```text
bytes   1,840,073 / 0x1C13C9
sha256  b212da65010d3a2e7ff6f7b8e10ce57371cb67e3093f58a6ad16a085399a8d0d

B24 selected rows             124
B24 changed rows              109
layout reconstructed          108
semantic corrections            3  M227 / M228 / M229
untouched correct rows         15
maximum target line width      40 units
```

The package materialization step must fail closed if the reconstructed TAI5MSG does not reproduce the exact V315 size and SHA-256 above.

## 3. Diagnostic package tree

Package root remains:

`Taiko5DX_KR_SELECTIVE/`

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

No fifth file is permitted.

The materialization filename is frozen as:

`Taiko5DX_KR_SELECTIVE_V315_B24_EDEN_DIAG.zip`

V315 denotes the payload generation. V316 is the design checkpoint and is not encoded in the package filename.

## 4. Component identities

The package execution must independently validate:

```text
ExeFS integrated IPS
  expected bytes   2,742
  expected sha256  6d6989b4d22a12f0bc54e78a45a79944a9aaa0a6523d7d15fc5dc6d3620aaab4

V315 selective TAI5MSG
  required bytes   1,840,073
  required sha256  b212da65010d3a2e7ff6f7b8e10ce57371cb67e3093f58a6ad16a085399a8d0d

Korean FONT_JPN.G1T
  required bytes   16,779,036
  required sha256  c82d80dada61ce80db42f948eafd3eb5b8f3bed5725ceebbc1c0897246166932
```

The IPS and font identities are inherited expectations from the previously validated package route. They must still be rechecked during materialization; V316 does not claim a new byte-level revalidation of them.

## 5. Build isolation contract

This diagnostic package is a one-cause-family build.

Included:

- the existing Mapping 10,036 ExeFS route;
- the existing page mapper;
- the existing Korean font;
- the V315 3,179-row selective TAI5MSG, including the B24 109-row correction overlay.

Explicitly excluded:

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
- any unrelated translation cleanup.

No unrelated improvement may be folded into this diagnostic ZIP.

## 6. Deterministic ZIP contract

Reuse the V312 deterministic packaging rules:

- lexicographically stable entry order;
- fixed timestamp;
- fixed Unix mode `0644`;
- DEFLATE level 9;
- retained top-level package root;
- two independent builds must produce byte-identical ZIP size and SHA-256.

The execution report must record:

- package ZIP bytes and SHA-256;
- all four entry names;
- each entry size and SHA-256;
- package-info size and SHA-256;
- independent rebuild identity result.

## 7. Drive transport contract

Target path:

`Google Drive/GPT/태합입지전/V315_B24_EDEN_DIAG_PACKAGE/`

Upload:

- `Taiko5DX_KR_SELECTIVE_V315_B24_EDEN_DIAG.zip`
- materialization report JSON.

Then download both files back and verify byte-identical SHA-256.

A Drive upload without roundtrip verification is not closure.

## 8. Runtime validation checklist

After package materialization and a separate explicit execution signal for runtime testing, the minimum Eden checklist is:

1. game boot and title/menu reachability;
2. one previously known ordinary selected Korean screen to confirm the shared Mapping/page/font route remains alive;
3. B24:M227 — verify restored `인재 조사` semantics and sane section layout;
4. B24:M228 — verify `아시가루 대장의 주명` title slot;
5. B24:M229 — verify `군자금 조달` semantics, section structure and line wrapping;
6. one V315 layout-only B24 row whose semantic payload was preserved;
7. one untouched B24 row from the 15-row control set, preferably M232 or M341;
8. confirm no obvious stale JP control debris or duplicate later-slot body appears in the tested B24 screens.

The exact layout-only representative locator should be selected from the V315 correction artifact at materialization time and recorded in the package report. Do not invent a representative before reading the artifact.

## 9. Runtime PASS / FAIL contract

Runtime PASS requires all of the following:

```text
boot / title path                         PASS
selected Korean rendering route          PASS
M227 semantics/layout                    PASS
M228 title                               PASS
M229 semantics/layout                    PASS
layout-only representative               PASS
untouched B24 control representative      PASS
no observed stale duplicate body         PASS
```

Any crash, blank help body, wrong-slot text, section-control corruption, or repeatable rendering defect is a FAIL for the B24 cause-family and must be classified before any unrelated reflow work begins.

## 10. 확정된 사실

- V315 B24 correction is already implemented and offline byte-exact validated.
- V315 changes exactly 109 B24 selected messages.
- V315 output identity is fixed at 1,840,073 bytes / `b212da65...`.
- The V312 package is stale because it carries the pre-V315 TAI5MSG.
- The existing package route is a four-file Eden classic-IPS package.
- No V315 diagnostic package has yet been materialized.

## 11. 유력한 가설

The V315 correction should remove the common B24 flattened-layout / wrong-slot symptoms without requiring any additional ExeFS or font change.

This remains a runtime hypothesis until the bounded Eden checklist is executed.

## 12. 미확정 사항

- final deterministic ZIP bytes and SHA-256;
- new `SELECTIVE_PACKAGE_INFO.json` identity;
- Drive roundtrip identity for the V315 package;
- Eden runtime behavior of the V315 B24 targets;
- whether any B24 caller has an effective visual constraint stricter than the audited 40-unit width model.

## 13. 기각된 가설

- ordinary non-B24 584-row reflow should be mixed into the same diagnostic package — REJECTED;
- a new IPS or font change is required merely because B24 TAI5MSG changed — NOT SUPPORTED;
- V312 package may be reused as the V315 diagnostic package — REJECTED;
- runtime validation may be considered complete from offline serializer results alone — REJECTED.

## 14. 관련 영향 범위

V316 changes documentation/state only.

No builder, serializer, IPS, font, TAI5MSG payload, ZIP, Drive package or runtime state is modified by V316.

## 15. 수정 제안 / exact next scope

After a new explicit execution signal:

`TAI5MSG_B24_V315_EDEN_DIAGNOSTIC_PACKAGE_MATERIALIZATION`

That scope may:

1. rebuild V315 TAI5MSG through the canonical serializer;
2. revalidate the four package components;
3. materialize the deterministic diagnostic ZIP;
4. rebuild it independently;
5. upload ZIP/report to Drive and verify roundtrip identity;
6. stop before Eden runtime execution unless runtime testing is separately authorized.

## 16. Repository write boundary

Any repository write remains restricted to:

`create_blob -> create_tree -> create_commit -> update_ref(force=false)`
