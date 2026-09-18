# TAI5MSG 3,179 Selective Eden Test Package Materialization — V312

Date: 2026-09-18 (KST)

Validation ID: `V312`

Parent canonical state:

`a3c98b7f2a46fdffa5bfed5567e58e452cd72ca0` — V311 package-integration implementation / offline validation.

Status:

`CLOSED / DETERMINISTIC EDEN TEST PACKAGE MATERIALIZED / DRIVE ROUNDTRIP VERIFIED / NO HARDWARE EXECUTION`

## 1. Scope

V312 materializes exactly the four-file V311 TAI5MSG integration slice into a deterministic Eden test package.

No new content family is added.

Excluded from this package remain:

- inline 139;
- R2884 / R2885;
- TAI5MSG external-caller waits 191;
- EVENT / TS5;
- SNR;
- CWTDAT;
- name / yomi;
- W0 / W1;
- pointer-56;
- historical 5,519 inline and bulk full-port payloads.

No gameplay/hardware execution is performed in V312.

## 2. Package tree

Package root:

`Taiko5DX_KR_SELECTIVE/`

Exact file set:

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

Strict allowlist audit:

`PASS / 4 of 4 exact / no extra file`

## 3. Materialized component identities

```text
ExeFS integrated IPS
  bytes   2,742
  sha256  6d6989b4d22a12f0bc54e78a45a79944a9aaa0a6523d7d15fc5dc6d3620aaab4

selective TAI5MSG
  bytes   1,841,481
  sha256  dfcb928f694117bdd51e69d25daf337c14e30c3a7078da3961dc3a570ffe44f9

Korean FONT_JPN.G1T
  bytes   16,779,036
  sha256  c82d80dada61ce80db42f948eafd3eb5b8f3bed5725ceebbc1c0897246166932

SELECTIVE_PACKAGE_INFO.json
  bytes   1,555
  sha256  1181f4ad0e97a51c957445dcd80cf13028c7821b67d29cc2a9f2004889cacba6
```

The three gameplay/runtime component identities are identical to the V311 validated values.

The package-info document is a V312 publication manifest and is therefore intentionally distinct from the V311 in-memory unpublished-info bytes.

## 4. Deterministic ZIP

Artifact:

`Taiko5DX_KR_SELECTIVE_V312_EDEN_TEST.zip`

```text
bytes   3,320,602
sha256  cb5fcece2dd793e5de573c7a4380c95f0135eafe41248157da90b80f88036c5e
entries 4
```

ZIP construction uses:

- lexicographically stable entry order;
- fixed timestamp `2026-09-18 00:00:00`;
- fixed Unix mode `0644`;
- DEFLATE level 9;
- top-level package root retained.

An independent second rebuild produced the exact same byte length and SHA-256.

Result:

`DETERMINISTIC_REBUILD = PASS`

## 5. Drive transport

Project artifact path:

`Google Drive/GPT/태합입지전/V312_EDEN_TEST_PACKAGE/`

Uploaded files:

```text
Taiko5DX_KR_SELECTIVE_V312_EDEN_TEST.zip
V312_PACKAGE_REPORT.json
```

The uploaded ZIP was downloaded back from Drive and independently hashed.

Roundtrip result:

```text
local ZIP
  3,320,602 bytes
  cb5fcece2dd793e5de573c7a4380c95f0135eafe41248157da90b80f88036c5e

Drive roundtrip ZIP
  3,320,602 bytes
  cb5fcece2dd793e5de573c7a4380c95f0135eafe41248157da90b80f88036c5e

transport identity  PASS
```

The package report also roundtripped byte-identically:

`7b9a3f6d0b7458872e2d40f864b30e1b3f967c70ef9274081c03d39ccd2570be`

## 6. Package metadata boundary

`SELECTIVE_PACKAGE_INFO.json` records:

- schema `TAI5MSG_3179_SELECTIVE_EDEN_TEST_PACKAGE_V1`;
- V311 as the validation source;
- Eden classic-IPS as the only delivery profile;
- exact title/version/Build ID;
- exact V311 component identities;
- TAI5MSG selected population 3,179;
- `inline_139_included = false`;
- no unrelated content family;
- `hardware_validation = NOT_PERFORMED`.

V312 does not claim a complete selective release.

Global materialized selective INCLUDE_KO remains 3,318 = inline 139 + TAI5MSG 3,179, but this test package intentionally carries only the TAI5MSG 3,179 family.

## 7. Closure

```text
V311 component identities        PASS
strict package allowlist         PASS
deterministic package tree       PASS
deterministic ZIP rebuild        PASS
Drive upload                     PASS
Drive download roundtrip         PASS
ZIP transport identity           PASS
hardware execution               NONE
inline 139 integration           NONE
```

## 8. Next scope

After a fresh explicit user signal:

`TAI5MSG_3179_SELECTIVE_EDEN_RUNTIME_VALIDATION`

That scope may define and execute the bounded Eden runtime validation checklist for this exact V312 package, collect device/emulator observations, classify failures by cause-family and stop.

It must not add inline 139 or any other content family while validating the V312 package.
