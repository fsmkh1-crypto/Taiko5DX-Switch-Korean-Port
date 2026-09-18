# SELECTIVE PROJECT STATE

Date: 2026-09-18 (KST)
Status: V302 TAI5MSG BLOCK-GROWTH RUNTIME ACCEPTANCE PASS / NEXT 3179 RELEASE-ADMISSION READ-ONLY / NO NEW CANDIDATES / NO BUILD
Track: `SWITCH_SELECTIVE_KOREANIZATION`

## 1. Resume authority

Repository: `fsmkh1-crypto/Taiko5DX-Switch-Korean-Port`
Branch: `main`
Target: Nintendo Switch title `0100346017304000`, game v1.1.3.

This file is the sole executable next-scope authority for the selective product track. Repository-root `PROJECT_STATE.md` is the sole repository-level resume authority.

Required reads, in authority order:

1. `TAI5MSG_SELECTED_BLOCK_GROWTH_RUNTIME_ACCEPTANCE_V302.md`
2. `artifacts/tai5msg_block_growth_runtime_acceptance_v1/INDEX.json`
3. `TAI5MSG_SELECTED_3370_CALLER_CAPACITY_CHECKPOINT_V301.md`
4. `artifacts/tai5msg_selected_3370_checkpoint_v1/INDEX.json`
5. `INLINE_R1_STATIC_47_CANDIDATE_CLASSIFICATION_V300.md`
6. `artifacts/inline_r1_static_47_candidate_classification_v1/INDEX.json`
7. `INLINE_R1_NUMERIC_53_CANDIDATE_CLASSIFICATION_V299.md`
8. `artifacts/inline_r1_numeric_53_candidate_classification_v1/INDEX.json`
9. `ENDING_HELP_39_CANDIDATE_CLASSIFICATION_V298.md`
10. `artifacts/ending_help_39_candidate_classification_v1/INDEX.json`
11. `INLINE_R1_LOGICAL_OBJECT_RECONSTRUCTION_AND_REUSABLE_RULES_V297.md`
12. `LEGACY_EVIDENCE_CLAIM_STRENGTH_POLICY_V296.md`
13. `CONTENT_CONTAINER_FIELD_AVAILABILITY_CORRECTION_V295.md`
14. `IDENTITY_IN_PROSE_POLICY.md`
15. `CLASSIFICATION_SCHEMA.md`
16. `SCRIPT_TAXONOMY_AND_CROSSCUTTING_RULES.md`
17. `KNOWN_FAILURES.md`
18. `SWITCH_ORIGINAL_SOURCE_INPUT_CONTRACT.md`
19. `ARCHITECTURE.md`
20. `this file`

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

After V300:

```text
candidate IDs             139
classification IDs        139
INCLUDE_KO rows           139
R1 materialized rows      139
```

Population:

```text
SEL-CAND/SEL-CLS-000001..000039  V298 ending-help STATIC_COMPLETE
SEL-CAND/SEL-CLS-000040..000092  V299 numeric VARIABLE_INSERT
SEL-CAND/SEL-CLS-000093..000139  V300 ordinary-inline STATIC_COMPLETE
```

Artifacts:

- `artifacts/ending_help_39_candidate_classification_v1/`
- `artifacts/inline_r1_numeric_53_candidate_classification_v1/`
- `artifacts/inline_r1_static_47_candidate_classification_v1/`

No builder/build/IPS/runtime write exists.

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

## 11. Open work

Still open:

- retain `R2884/R2885` as unresolved until consumer semantics are proven, potentially by later shared-route evidence;
- TAI5MSG caller-resolved 3,179-row release-admission audit after V302 growth closure;
- TAI5MSG 191 external-caller evidence waits;
- EVENT/TS5 production parser/caller coverage;
- SNR field/record selective parsing;
- R2/R3 corpus;
- builder/serializer/build/IPS;
- runtime font/layout/translation QA.

Do not re-audit the 139 materialized inline rows because work moves to another container.

## 12. Executable next scope — sole authority

After a fresh explicit user signal, resume:

```text
TAI5MSG_CALLER_RESOLVED_3179_RELEASE_ADMISSION_READ_ONLY
```

Scope population:

```text
R1 caller-resolved  3,158
R2 caller-resolved     21
total                3,179
```

Scope intent:

```text
reuse V301 source-role/mechanism/caller closure
reuse V302 block-growth/capacity structural acceptance
audit remaining common release gates for exactly the 3,179 caller-resolved rows
check provenance / PC occurrence conflict / risk flags / transport requirements / identity-policy applicability
derive terminal release dispositions without issuing candidate/classification IDs
keep the 191 external-caller waits outside this cause-family
do not begin builder, serializer, build, or IPS
keep R2884/R2885 as separate evidence waits
```

After reporting that read-only analysis, require another explicit user signal before candidate/classification materialization or implementation.

## 13. Repository write boundary

Repository writes remain restricted to exactly:

```text
create_blob -> create_tree -> create_commit -> update_ref(force=false)
```

No Contents-API write, branch creation, issue/PR write, or force update is permitted.
