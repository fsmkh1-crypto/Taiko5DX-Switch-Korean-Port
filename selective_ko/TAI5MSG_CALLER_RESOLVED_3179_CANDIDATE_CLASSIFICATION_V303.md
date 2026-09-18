# TAI5MSG CALLER-RESOLVED 3179 CANDIDATE / CLASSIFICATION MATERIALIZATION — V303

Date: 2026-09-18 (KST)
Status: CANONICAL MATERIALIZATION / 3,179 INCLUDE_KO / NO BUILDER / NO BUILD
Track: `SWITCH_SELECTIVE_KOREANIZATION`
Validation ID: `V303`
Parent: `ce0e7f2ed5d23849499ba8a3e35e8978aff0787c` / V302 state + PC-patch residual-QA documentation

## 1. Purpose

V303 materializes exactly the TAI5MSG caller-resolved release-admitted population closed by V301 caller/mechanism evidence, V302 block-growth acceptance, and the subsequent read-only release-admission/provenance reconstruction.

It does not implement a serializer, rebuild TAI5MSG, generate IPS, build a package, or claim hardware/gameplay PASS.

## 2. Canonical source identity

```text
PC original TAI5MSG
size    1,810,889
sha256  aae037dd5948f79b9fc2e5affcb1e60e08efca39f897123045fe685786be978f

PC Korean v1.02 TAI5MSG
size    2,134,366
sha256  e3b4522a1047ff409e099b5ee197d7689279ea7472cb403d305b2507fec96090

Switch original TAI5MSG
status  HISTORICALLY_VERIFIED_BYTE_IDENTICAL_TO_PC_JP
```

Payload provenance is `canonical file SHA-256 + exact (block, local)` locator. Full payload bytes are not duplicated into every classification row.

## 3. Exact selected source floor

R1 UI_DESCRIPTION:

```text
B17  0..199, 202..258                         257
B18  0..199, 204..215                         212
B19  0..199, 202..290                         289
B20  0..199, 202..268                         267
B21  44..58                                    15
B22  0..354, 363..533                         526
B23  0..616                                   617
B24  221..344                                 124
B28  0..199                                   200
B29  0..199                                   200
B30  0..199                                   200
B31  0..199                                   200
B32  0..160,162..176,178..240,242            240
------------------------------------------------
TOTAL                                        3,347
```

R2 NARRATION_SYSTEM:

```text
B0   10..11                                     2
B21  39..40, 63..76, 78..82                   21
------------------------------------------------
TOTAL                                           23
```

Selected total = `3,370`.

## 4. Exact 191 caller-wait exclusion

```text
B23:0..93                          94
B23:616                             1
B21:44..58                         15
B21:39..40                          2
B32:160                             1
B32:162..176                       15
B32:178..240                       63
-------------------------------------
TOTAL                             191
```

These rows remain evidence waits and are not promoted by V303.

## 5. Materialized caller-resolved population

```text
R1 caller-resolved       3,158
R2 caller-resolved          21
------------------------------
TOTAL                     3,179
```

By block:

```text
B0       2
B17    257
B18    212
B19    289
B20    267
B21     19
B22    526
B23    522
B24    124
B28    200
B29    200
B30    200
B31    200
B32    161
----------------
TOTAL 3,179
```

ID allocation:

```text
candidate IDs       SEL-CAND-000140..SEL-CAND-003318
classification IDs  SEL-CLS-000140..SEL-CLS-003318
derived disposition INCLUDE_KO 3,179 / 3,179
```

## 6. Row-level artifact

Canonical artifact:

`selective_ko/artifacts/tai5msg_caller_resolved_3179_candidate_classification_v1/INDEX.json`

Eight UTF-8 JSONL shards contain all 3,179 actual row records. Every row stores candidate/classification ID, exact block/local locator and runtime message ID, usage class, STATIC_COMPLETE mechanism, RESOLVED investigation status, resolved caller family, current-envelope or V302 block-growth realization, and terminal `INCLUDE_KO` disposition.

The V301 aggregate-only row-artifact deficiency is therefore closed for this population.

## 7. V301 / V302 invariant replay

```text
R1 selected                    3,347
R2 selected                       23
selected total                 3,370
R1 resolved                    3,158
R2 resolved                       21
resolved total                 3,179
caller wait                      191
resolved current-envelope      1,175
resolved growth-cleared        2,004
```

Block growth remains:

```text
B17  +0x0340
B19  +0x0A80
B20  +0x06C0
B21  +0x0400
B22  +0x4340
B23  +0x1280
B24  +0x0E40
TOTAL +0x7C80
```

No closed V301/V302 runtime-structure fact is reopened.

## 8. Classification and identity policy

All V303 rows:

```text
mechanism_class       STATIC_COMPLETE
investigation_status  RESOLVED
append_after          NO
cross-message compose ABSENT
derived_disposition   INCLUDE_KO
```

Usage:

```text
UI_DESCRIPTION     3,158
NARRATION_SYSTEM      21
```

Identity remains:

```text
dedicated person/place identity presentation = KEEP_JP
authored Korean identity literals in prose    = PRESERVE_AS_AUTHORED_KO
runtime-inserted identity                     = KEEP_JP
reverse substitution                          = FORBIDDEN
```

## 9. Cumulative selective corpus

After V303:

```text
candidate IDs              3,318
classification IDs         3,318
INCLUDE_KO rows            3,318
R1 materialized            3,297
R2 materialized               21
```

The prior 139 inline R1 rows remain unchanged.

## 10. Claim boundary

```text
release candidate/classification materialized = YES
builder implemented                           = NO
serializer implemented                        = NO
TAI5MSG rebuilt                               = NO
IPS/build/package                             = NONE
hardware execution                            = NOT PERFORMED
layout/translation/help completeness QA       = NOT CLOSED
```

The PC-patch residual QA hazards in `selective_ko/KNOWN_FAILURES.md` section 14 remain binding.

## 11. Next scope

After a fresh explicit user signal:

`TAI5MSG_3179_SELECTIVE_BUILDER_SERIALIZER_DESIGN_READ_ONLY`

Design may consume this exact row artifact and canonical payload source and specify fail-closed guards, mapping/font coverage gates, deterministic block reconstruction and output validation. It must not implement, build, or generate IPS until that design is reported and a further explicit signal is received.

## 12. Repository write boundary

`create_blob -> create_tree -> create_commit -> update_ref(force=false)`

No Contents-API write, branch creation, issue/PR write, or force update is permitted.
