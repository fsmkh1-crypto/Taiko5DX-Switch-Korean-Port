# SELECTIVE PROJECT STATE

Date: 2026-09-18 (KST)
Status: V300 STATIC 47 CANDIDATE/CLASSIFICATION MATERIALIZED / INLINE R1 INCLUDE_KO 139 OF 141 / NO BUILD
Track: `SWITCH_SELECTIVE_KOREANIZATION`

## 1. Resume authority

Repository: `fsmkh1-crypto/Taiko5DX-Switch-Korean-Port`
Branch: `main`
Target: Nintendo Switch title `0100346017304000`, game v1.1.3.

This file is the sole executable next-scope authority for the selective product track. Repository-root `PROJECT_STATE.md` is the sole repository-level resume authority.

Required reads, in authority order:

1. `INLINE_R1_STATIC_47_CANDIDATE_CLASSIFICATION_V300.md`
2. `artifacts/inline_r1_static_47_candidate_classification_v1/INDEX.json`
3. `INLINE_R1_NUMERIC_53_CANDIDATE_CLASSIFICATION_V299.md`
4. `artifacts/inline_r1_numeric_53_candidate_classification_v1/INDEX.json`
5. `ENDING_HELP_39_CANDIDATE_CLASSIFICATION_V298.md`
6. `artifacts/ending_help_39_candidate_classification_v1/INDEX.json`
7. `INLINE_R1_LOGICAL_OBJECT_RECONSTRUCTION_AND_REUSABLE_RULES_V297.md`
8. `LEGACY_EVIDENCE_CLAIM_STRENGTH_POLICY_V296.md`
9. `CONTENT_CONTAINER_FIELD_AVAILABILITY_CORRECTION_V295.md`
10. `IDENTITY_IN_PROSE_POLICY.md`
11. `CLASSIFICATION_SCHEMA.md`
12. `SCRIPT_TAXONOMY_AND_CROSSCUTTING_RULES.md`
13. `KNOWN_FAILURES.md`
14. `SWITCH_ORIGINAL_SOURCE_INPUT_CONTRACT.md`
15. `ARCHITECTURE.md`
16. this file

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

## 9. Open work

Still open:

- retain `R2884/R2885` as unresolved until consumer semantics are proven, potentially by later shared-route evidence;
- TAI5MSG selective message classification;
- EVENT/TS5 production parser/caller coverage;
- SNR field/record selective parsing;
- R2/R3 corpus;
- builder/serializer/build/IPS;
- runtime font/layout/translation QA.

Do not re-audit the 139 materialized inline rows because work moves to another container.

## 10. Executable next scope — sole authority

After a fresh explicit user signal, resume:

```text
SELECTIVE_KO_TAI5MSG_SELECTIVE_MESSAGE_CLASSIFICATION_READ_ONLY
```

Scope intent:

```text
reuse the verified 33-block / 14,832-slot TAI5MSG structural lattice
classify selected messages by usage/mechanism/owner evidence
do not treat TAI5MSG as dialogue-only
do not bulk-import the PC Korean file
do not begin builder/build/IPS
keep R2884/R2885 as evidence waits unless independently resolved by new shared-route evidence
```

After reporting that read-only analysis, require another explicit user signal before materialization or implementation.

## 11. Repository write boundary

Repository writes remain restricted to exactly:

```text
create_blob -> create_tree -> create_commit -> update_ref(force=false)
```

No Contents-API write, branch creation, issue/PR write, or force update is permitted.
