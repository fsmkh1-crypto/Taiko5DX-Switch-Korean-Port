# SELECTIVE PROJECT STATE

Date: 2026-09-18 (KST)
Status: V312 SELECTIVE TAI5MSG EDEN TEST PACKAGE MATERIALIZED / DRIVE ROUNDTRIP VERIFIED / NO HARDWARE
Track: `SWITCH_SELECTIVE_KOREANIZATION`

## 1. Resume authority

Repository: `fsmkh1-crypto/Taiko5DX-Switch-Korean-Port`
Branch: `main`
Target: Nintendo Switch title `0100346017304000`, game v1.1.3.

This file is the sole executable next-scope authority for the selective product track. Repository-root `PROJECT_STATE.md` is the sole repository-level resume authority.

Required reads, in authority order:

1. `TAI5MSG_3179_SELECTIVE_EDEN_TEST_PACKAGE_MATERIALIZATION_V312.md`
2. `TAI5MSG_3179_SELECTIVE_PACKAGE_INTEGRATION_IMPLEMENTATION_OFFLINE_VALIDATION_V311.md`
3. `TAI5MSG_3179_SELECTIVE_PACKAGE_INTEGRATION_DESIGN_V310.md`
4. `TAI5MSG_3179_SELECTIVE_SERIALIZER_BYTE_EXACT_OFFLINE_REPLAY_CLOSURE_V309.md`
5. `TAI5MSG_3179_SELECTIVE_SERIALIZER_IMPLEMENTATION_OFFLINE_VALIDATION_V308.md`
6. `TAI5MSG_3179_SELECTIVE_BUILDER_SERIALIZER_DESIGN_V307.md`
7. `TAI5MSG_PREIMPLEMENTATION_GATE_1_5_CLOSURE_V306.md`
8. `TAI5MSG_EXTERNAL_DESIGN_AUDIT_CONSOLIDATION_V305.md`
9. `TAI5MSG_V303_PC_PAYLOAD_DEFECT_CORRECTION_2_V304.md`
10. `artifacts/tai5msg_v303_pc_payload_defect_correction_2_v1/INDEX.json`
11. `TAI5MSG_CALLER_RESOLVED_3179_CANDIDATE_CLASSIFICATION_V303.md`
12. `artifacts/tai5msg_caller_resolved_3179_candidate_classification_v1/INDEX.json`
13. `TAI5MSG_SELECTED_BLOCK_GROWTH_RUNTIME_ACCEPTANCE_V302.md`
14. `artifacts/tai5msg_block_growth_runtime_acceptance_v1/INDEX.json`
15. `TAI5MSG_SELECTED_3370_CALLER_CAPACITY_CHECKPOINT_V301.md`
16. `artifacts/tai5msg_selected_3370_checkpoint_v1/INDEX.json`
17. `INLINE_R1_STATIC_47_CANDIDATE_CLASSIFICATION_V300.md`
18. `artifacts/inline_r1_static_47_candidate_classification_v1/INDEX.json`
19. `INLINE_R1_NUMERIC_53_CANDIDATE_CLASSIFICATION_V299.md`
20. `artifacts/inline_r1_numeric_53_candidate_classification_v1/INDEX.json`
21. `ENDING_HELP_39_CANDIDATE_CLASSIFICATION_V298.md`
22. `artifacts/ending_help_39_candidate_classification_v1/INDEX.json`
23. `INLINE_R1_LOGICAL_OBJECT_RECONSTRUCTION_AND_REUSABLE_RULES_V297.md`
24. `LEGACY_EVIDENCE_CLAIM_STRENGTH_POLICY_V296.md`
25. `CONTENT_CONTAINER_FIELD_AVAILABILITY_CORRECTION_V295.md`
26. `IDENTITY_IN_PROSE_POLICY.md`
27. `CLASSIFICATION_SCHEMA.md`
28. `SCRIPT_TAXONOMY_AND_CROSSCUTTING_RULES.md`
29. `KNOWN_FAILURES.md`
30. `SWITCH_ORIGINAL_SOURCE_INPUT_CONTRACT.md`
31. `ARCHITECTURE.md`
32. `this file`

## 2. Product boundary

The product remains selective Koreanization, not a full clone of the PC patch.

Authority remains:

```text
PC Korean content/terminology        -> SOURCE_AUTHORITY
Switch structure/owner/caller        -> STRUCTURAL_AUTHORITY
verified Switch mapping realization  -> SWITCH_RUNTIME_AUTHORITY
known-good PC visible result         -> SEMANTIC_ORACLE
PC runtime mechanism                 -> REFERENCE_OR_HINT
```

Dedicated identity/yomi/date/name-entry and unresolved dynamic grammar remain Japanese/deferred unless separately promoted.

## 3. Current materialized selective corpus

After V303:

```text
candidate IDs             3,318
classification IDs        3,318
INCLUDE_KO rows           3,318
R1 materialized rows      3,297
R2 materialized rows         21
```

Population:

```text
SEL-CAND/SEL-CLS-000001..000039  V298 ending-help STATIC_COMPLETE
SEL-CAND/SEL-CLS-000040..000092  V299 numeric VARIABLE_INSERT
SEL-CAND/SEL-CLS-000093..000139  V300 ordinary-inline STATIC_COMPLETE
SEL-CAND/SEL-CLS-000140..003318  V303 TAI5MSG caller-resolved STATIC_COMPLETE
```

Artifacts:

- `artifacts/ending_help_39_candidate_classification_v1/`
- `artifacts/inline_r1_numeric_53_candidate_classification_v1/`
- `artifacts/inline_r1_static_47_candidate_classification_v1/`
- `artifacts/tai5msg_caller_resolved_3179_candidate_classification_v1/`

The selective serializer source exists and is byte-exact verified by V309. No package/build/IPS/runtime output exists.

## 4. Inline R1 source-role state

```text
INLINE R1 source-role total             141

ending-help                              39  V298 INCLUDE_KO
ordinary inline                         102
  static-like                            49
    V300 resolved/materialized           47
    unresolved                            2  R2884 / R2885
  V299 numeric VARIABLE_INSERT           53
```

The currently materialized inline R1 release-classification population is 139.

`R2884` and `R2885` remain evidence waits. They are not rejected and must not be included by heuristic.

## 5. V300 static population invariants

```text
usage_class                 UI_DESCRIPTION 47/47
mechanism_class             STATIC_COMPLETE 47/47
investigation_status        RESOLVED 47/47
derived_disposition         INCLUDE_KO 47/47

physical owners             47 unique
PC inline source records    49 unique
RELA consumer slots         47 unique
shared-consumer owners       0
original-guard failures      0
terminator failures          0
capacity failures            0
risk-flagged rows            0
manual overrides             0
```

Capacity:

```text
KO payload incl NUL 10..38 bytes
proven capacity     13..41 bytes
minimum slack        0 bytes
maximum slack       10 bytes
exact-fit rows        2
```

Special reconstruction cases:

```text
R234         fixed-prefix owner
R235         fixed-prefix owner
R485+R486   split PC diff -> one complete Switch object
R642+R643   split PC diff -> one complete Switch object
```

## 6. Reusable ordinary-inline consumer discovery

Verified route:

```text
.rela.dyn R_AARCH64_RELATIVE (0x403)
 -> r_offset runtime source/consumer slot
 -> r_addend Switch physical text owner
```

V300 has one such slot for every included static owner.

This rule is investigation methodology, not blanket authorization for other containers or unresolved rows.

## 7. Binding V299 census correction

Canonical values remain:

```text
numeric objects                         53
%d occurrences                         60
%u occurrences                         10
remaining ordinary inline R1 objects  102
inline R1 source-role objects          141
```

Do not reuse the superseded 50 / 57 / 99 / 138 intermediate counts.

## 8. Identity policy

```text
identity presentation fields            -> KEEP_JP
authored Korean prose identity literals -> PRESERVE_AS_AUTHORED_KO
runtime-inserted identity                -> KEEP_JP
reverse substitution                     -> FORBIDDEN
```

## 9. TAI5MSG V301 checkpoint

Canonical authority:

`TAI5MSG_SELECTED_3370_CALLER_CAPACITY_CHECKPOINT_V301.md`

Machine-readable checkpoint:

`artifacts/tai5msg_selected_3370_checkpoint_v1/INDEX.json`

```text
selected total                              3,370
R1 UI_DESCRIPTION                          3,347
R2 NARRATION_SYSTEM                           23
external caller resolved                   3,179
external caller evidence wait                191
current block envelope fit                  1,254
block growth required                       2,116
caller resolved + current envelope fit      1,175
caller resolved + block-growth gate         2,004
```

Selected internal composition closure:

```text
outgoing C/J edges              0
incoming C/J edges              0
semantic 0x02 insertions        0
```

Growth blocks: `B17 B19 B20 B21 B22 B23 B24`.

V301 issues no new candidate/classification rows.

## 10. V302 block-growth runtime acceptance

Canonical authority:

`TAI5MSG_SELECTED_BLOCK_GROWTH_RUNTIME_ACCEPTANCE_V302.md`

Machine-readable checkpoint:

`artifacts/tai5msg_block_growth_runtime_acceptance_v1/INDEX.json`

```text
runtime structural acceptance     PASS
growth gate cleared rows          2,004
current-fit caller-resolved       1,175
next release-admission population 3,179
external caller wait                191
per-block runtime capacity        0x20000
largest selected rebuilt block    0x12B00
selected total growth             0x7C80
hardware execution                NOT PERFORMED
```

No candidate/classification/INCLUDE_KO rows are issued by V302.

## 11. V303 TAI5MSG 3,179 candidate/classification materialization

Canonical authority:

`TAI5MSG_CALLER_RESOLVED_3179_CANDIDATE_CLASSIFICATION_V303.md`

Machine-readable row artifact:

`artifacts/tai5msg_caller_resolved_3179_candidate_classification_v1/INDEX.json`

```text
new candidate IDs             3,179
new classification IDs        3,179
new INCLUDE_KO rows           3,179
R1 UI_DESCRIPTION             3,158
R2 NARRATION_SYSTEM              21
current-envelope realization  1,175
growth-gate-cleared           2,004
external-caller waits excluded  191
ID range                      000140..003318
```

Cumulative selective corpus is 3,318 candidate/classification/INCLUDE_KO rows.

V303 stores all 3,179 exact row locators in eight UTF-8 JSONL shards. Payload provenance is canonical PC-Korean TAI5MSG SHA-256 plus exact block/local locator.

Builder, serializer, build, IPS and hardware execution remain absent.

## 12. V304 TAI5MSG PC payload-defect correction overlay

Canonical authority:

`TAI5MSG_V303_PC_PAYLOAD_DEFECT_CORRECTION_2_V304.md`

Machine-readable correction artifact:

`artifacts/tai5msg_v303_pc_payload_defect_correction_2_v1/INDEX.json`

```text
correction rows                 2
affected candidates             000669 / 002816
affected locators               B19:58 / B30:58
verdict                         PAYLOAD_DEFECT
V303 membership                 unchanged 3,179
candidate/classification count  unchanged 3,318 cumulative
INCLUDE_KO count                unchanged 3,318 cumulative
builder/build/IPS               NONE
```

A future builder must apply V304 only after an exact canonical PC-KO file guard and exact per-message source hash guard. Any mismatch aborts.

For all other 3,177 V303 TAI5MSG rows, exact canonical PC-KO locator payload remains the target.

## 13. V305 external text-only design audit consolidation

Canonical authority:

`TAI5MSG_EXTERNAL_DESIGN_AUDIT_CONSOLIDATION_V305.md`

Evidence class: four user-supplied external text-only red-team reviews; advisory claim-strength/invariant review; no new binary fact promoted solely from external opinion.

Carrier separation:

global selective INCLUDE_KO 3,318 = inline/Switch main 139 + TAI5MSG/RomFS 3,179.

Accepted gates:

- DETERMINISTIC_PADDING_GATE
- ZERO_REPLACEMENT_IDENTITY_REBUILD_GATE
- CONTROL_AND_CODE_VALIDATION_GATE
- STRONG_REPARSE_OFFSET_GATE
- MAPPING_TO_GLYPH_CLOSURE_GATE

Repeated unsupported external hypotheses are recorded in KNOWN_FAILURES.md section 15.

No candidate/classification counts, gameplay data, builder, build or IPS change in V305.

## 14. V306 preimplementation gate closure

Canonical authority:

`TAI5MSG_PREIMPLEMENTATION_GATE_1_5_CLOSURE_V306.md`

```text
GATE-1 DETERMINISTIC_PADDING_GATE        PASS
GATE-2 ZERO_REPLACEMENT_IDENTITY_REBUILD PASS
GATE-3 CONTROL_AND_CODE_VALIDATION_GATE   PASS
GATE-4 STRONG_REPARSE_OFFSET_GATE         PASS
GATE-5 MAPPING_TO_GLYPH_CLOSURE_GATE      PASS_FOR_EFFECTIVE_TAI5MSG_3179
```

Effective release postconditions:

```text
TAI5MSG rows          3,179
growth                +0x7780
final physical size   0x1C1949
B32 used-end          0xB8D5
B32 physical          0xCA49
B32 declared          0xCA80
B32 omitted tail      55 bytes
effective KO codes    992 Hangul
effective PUA usage   0
```

B32's stock zero-replacement relation `physical EOF == used-end` must not be generalized to the shrinking effective release. Preserve the current effective physical extent `0xCA49`, fill the new physical slack deterministically with canonical on-disk `0x00`, and keep the final 55 bytes omitted.

GATE-5 is population-scoped. It closes Mapping/page/font availability for the 992 Hangul codes actually emitted by the 3,179-row TAI5MSG population; it does not claim visible-glyph closure for all 2,542 Korean-added Mapping entries.

No builder, serializer, release TAI5MSG, IPS, build or hardware execution exists.

## 15. V307 selective serializer design

Canonical authority:

`TAI5MSG_3179_SELECTIVE_BUILDER_SERIALIZER_DESIGN_V307.md`

Binding design summary:

```text
source lattice          canonical stock JP 14,832
selected replacement    exact V303 3,179
correction overlay      exact V304 2 rows
unselected preservation 11,653 byte-exact JP

B0..B31 declared        max(stock_declared, align_up(used,0x40))
B32 current declared    0xCA80
B32 current physical    0xCA49
B32 current omitted     0x37
canonical growth        +0x7780
canonical final size    0x1C1949
naive shrink growth     +0x58C0 REJECTED
```

The growth/final-size values are postconditions and must not drive layout calculation.

Existing `builder/tai5msg.py` remains legacy/reference for the historical V288/V289/V290 path. The selective implementation should be isolated, suggested as `builder/selective_tai5msg.py`.

No implementation or gameplay output exists in V307.

## 16. V308 serializer implementation / metadata offline validation

Canonical authority:

`TAI5MSG_3179_SELECTIVE_SERIALIZER_IMPLEMENTATION_OFFLINE_VALIDATION_V308.md`

```text
selective serializer module      IMPLEMENTED
unit/regression test source      IMPLEMENTED
V303 shard replay                PASS
V304 exact correction replay     PASS
structure-length layout replay   PASS
byte-exact new-module execution  PENDING
package/build/IPS/runtime        NONE
```

Do not promote metadata replay into byte-exact output validation. That pending state is closed only by V309.

## 17. V309 byte-exact offline replay closure

Canonical authority:

`TAI5MSG_3179_SELECTIVE_SERIALIZER_BYTE_EXACT_OFFLINE_REPLAY_CLOSURE_V309.md`

```text
runtime                   Python 3.13.5 clean directory
stock identity            PASS
PC-KO identity            PASS
V303/V304 canonical data  PASS
Mapping 10,036 source     PC patch T5K121R actual table
zero-replacement identity PASS
effective reconstruction  PASS
selected                  3,179
unselected                11,653
messages                  14,832
growth                    +0x7780
final size                0x1C1949
B32                        off 0x1B4F00 / used 0xB8D5 / declared 0xCA80 / physical 0xCA49 / omitted 0x37
output SHA-256            dfcb928f694117bdd51e69d25daf337c14e30c3a7078da3961dc3a570ffe44f9
tests                     7/7 PASS
```

Status: `CLOSED / CLEAN_RUNTIME_VERIFIED / BYTE_EXACT_REPLAY_VERIFIED`.

No package/build/IPS/runtime package/hardware execution occurred.

## 18. Open work

Still open:

- `R2884/R2885` unresolved consumer semantics;
- TAI5MSG 191 external-caller waits;
- Eden runtime validation for the exact V312 TAI5MSG package;
- EVENT/TS5 and SNR work;
- remaining R2/R3 corpus;
- layout/reflow, mistranslation, help/content-completeness QA;
- forced-minigame and 3+-choice runtime QA;
- physical Nintendo Switch validation.

## 19. V310 package-integration design

Canonical authority:

`TAI5MSG_3179_SELECTIVE_PACKAGE_INTEGRATION_DESIGN_V310.md`

Binding conclusions:

```text
legacy builder/build.py          REJECTED_FOR_SELECTIVE_PACKAGE
new package integration          ISOLATED_SELECTIVE_BUILDER
suggested module                 builder/selective_package.py
first delivery profile           EDEN_CLASSIC_IPS_ONLY
Mapping actions                  4
page-mapper actions              1
expected ExeFS IPS records       5
expected classic IPS size        2,742
TAI5MSG SHA-256                  dfcb928f694117bdd51e69d25daf337c14e30c3a7078da3961dc3a570ffe44f9
Korean font SHA-256              c82d80dada61ce80db42f948eafd3eb5b8f3bed5725ceebbc1c0897246166932
bulk PC RomFS import             FORBIDDEN
historical inline 5,519          FORBIDDEN
W0/W1 compact-width family       NOT_REQUIRED_FOR_CURRENT_TAI5MSG
physical Switch delivery         NOT_YET_DESIGNED
```

Exact package allowlist for this bounded TAI5MSG integration slice:

```text
exefs/D9120950C258610A746F4A31CE3A3B376DE393D9.ips
romfs/TAI5MSG_JP.DAT
romfs/FONT/FONT_JPN.G1T
SELECTIVE_PACKAGE_INFO.json
```

This is not the complete future selective release; the already materialized inline 139 population and other content families remain outside this TAI5MSG-only integration stage.

## 20. V311 package-integration implementation / offline validation

Canonical authority:

`TAI5MSG_3179_SELECTIVE_PACKAGE_INTEGRATION_IMPLEMENTATION_OFFLINE_VALIDATION_V311.md`

```text
implementation              builder/selective_package.py
tests                       tests/test_selective_package.py
combined tests              13/13 PASS
TAI5MSG                     1,841,481 / dfcb928f694117bdd51e69d25daf337c14e30c3a7078da3961dc3a570ffe44f9
font                        16,779,036 / c82d80dada61ce80db42f948eafd3eb5b8f3bed5725ceebbc1c0897246166932
integrated Eden IPS         5 records / 2,742 bytes
integrated IPS SHA-256      6d6989b4d22a12f0bc54e78a45a79944a9aaa0a6523d7d15fc5dc6d3620aaab4
staged allowlist            4/4 exact
published package           NONE
hardware                    NONE
```

The module validates and stages components in memory only. It does not publish a package tree or ZIP.

Inline 139 remains an approved but separate Switch-main carrier family and is not part of the V311 TAI5MSG package slice.

## 21. V312 Eden test-package materialization

Canonical authority:

`TAI5MSG_3179_SELECTIVE_EDEN_TEST_PACKAGE_MATERIALIZATION_V312.md`

```text
artifact                    Taiko5DX_KR_SELECTIVE_V312_EDEN_TEST.zip
bytes                       3,320,602
SHA-256                     cb5fcece2dd793e5de573c7a4380c95f0135eafe41248157da90b80f88036c5e
entries                     4/4 exact allowlist
deterministic rebuild       PASS
Drive upload/download       PASS byte-identical
Drive path                  Google Drive/GPT/태합입지전/V312_EDEN_TEST_PACKAGE
inline 139                  NOT INCLUDED
hardware                    NOT PERFORMED
```

The package is an intentionally bounded TAI5MSG 3,179 runtime-test carrier, not the complete 3,318-row selective release.

## 22. Executable next scope — sole authority

After a fresh explicit user signal, resume:

`TAI5MSG_3179_SELECTIVE_EDEN_RUNTIME_VALIDATION`

Authorized:

- use exactly the V312 package identity;
- define the smallest runtime observation checklist needed to validate TAI5MSG loading/rendering, Mapping/page/font integration and representative selected/unselected behavior;
- collect Eden observations supplied or produced during the test;
- classify failures by one cause-family at a time;
- report and stop.

Not authorized:

- changing package contents while validation is in progress;
- adding inline 139;
- EVENT/SNR/CWTDAT/name/yomi/W0/W1/pointer-56 or unrelated content;
- physical Switch/Atmosphere delivery unless separately authorized.

## 23. Repository write boundary

```text
create_blob -> create_tree -> create_commit -> update_ref(force=false)
```
