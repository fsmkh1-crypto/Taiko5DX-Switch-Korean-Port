# SELECTIVE PROJECT STATE

Date: 2026-09-18 (KST)
Status: V299 NUMERIC 53 CANDIDATE/CLASSIFICATION MATERIALIZED / R1 INCLUDE_KO 92 TOTAL / NO BUILD
Track: `SWITCH_SELECTIVE_KOREANIZATION`

## 1. Resume authority

Repository: `fsmkh1-crypto/Taiko5DX-Switch-Korean-Port`
Branch: `main`
Target: Nintendo Switch title `0100346017304000`, game v1.1.3.

This file is the sole executable next-scope authority for the selective product track. Repository-root `PROJECT_STATE.md` is the sole repository-level resume authority.

Required reads, in authority order:

1. `INLINE_R1_NUMERIC_53_CANDIDATE_CLASSIFICATION_V299.md`
2. `artifacts/inline_r1_numeric_53_candidate_classification_v1/INDEX.json`
3. `ENDING_HELP_39_CANDIDATE_CLASSIFICATION_V298.md`
4. `artifacts/ending_help_39_candidate_classification_v1/INDEX.json`
5. `INLINE_R1_LOGICAL_OBJECT_RECONSTRUCTION_AND_REUSABLE_RULES_V297.md`
6. `LEGACY_EVIDENCE_CLAIM_STRENGTH_POLICY_V296.md`
7. `CONTENT_CONTAINER_FIELD_AVAILABILITY_CORRECTION_V295.md`
8. `IDENTITY_IN_PROSE_POLICY.md`
9. `CLASSIFICATION_SCHEMA.md`
10. `SCRIPT_TAXONOMY_AND_CROSSCUTTING_RULES.md`
11. `KNOWN_FAILURES.md`
12. `SWITCH_ORIGINAL_SOURCE_INPUT_CONTRACT.md`
13. `ARCHITECTURE.md`
14. this file

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

After V299:

```text
candidate IDs             92
classification IDs        92
INCLUDE_KO rows           92
R1 materialized rows      92
```

Population:

```text
SEL-CAND/SEL-CLS-000001..000039  V298 ending-help STATIC_COMPLETE
SEL-CAND/SEL-CLS-000040..000092  V299 numeric VARIABLE_INSERT
```

Artifacts:

- `artifacts/ending_help_39_candidate_classification_v1/`
- `artifacts/inline_r1_numeric_53_candidate_classification_v1/`

No builder/build/IPS/runtime write exists.

## 4. V299 numeric population invariants

```text
usage_class                 UI_DESCRIPTION 53/53
mechanism_class             VARIABLE_INSERT 53/53
investigation_status        RESOLVED 53/53
derived_disposition         INCLUDE_KO 53/53
physical owners             53 unique
PC inline source records    60 unique
RELA consumer slots         54 unique
shared-consumer owners       1
token-sequence mismatches    0
particle-risk rows           0
dynamic-counter rows         0
capacity failures            0
risk-flagged rows            0
manual overrides             0
```

Format signatures:

```text
%d          33
%d + %d     10
%u + %d      7
%u           3
```

Capacity:

```text
KO payload incl NUL 15..39 bytes
proven capacity     18..45 bytes
minimum slack        0 bytes
maximum slack       13 bytes
```

## 5. Binding census correction

Canonical V299 corrections:

```text
numeric objects                         50 -> 53
%d occurrences                         57 -> 60
remaining ordinary inline R1 objects   99 -> 102
inline R1 source-role objects          138 -> 141
```

`%u = 10` is unchanged.

Do not reuse the superseded 50 / 57 / 99 / 138 intermediate counts.

## 6. Current inline R1 routing

```text
INLINE R1 source-role total             141

ending-help                              39  V298 INCLUDE_KO
ordinary inline                         102
  static-like                            49
    resolved/not materialized            47
    unresolved                            2  R2884 / R2885
  numeric VARIABLE_INSERT                53  V299 INCLUDE_KO
```

The currently materialized R1 release-classification population is 92, not 141.

`R2884` and `R2885` remain evidence waits. They are not rejected and must not be included by heuristic.

## 7. Reusable V299 discovery

For this ordinary-inline numeric family, direct code XREF absence does not imply absence of a consumer.

The verified route is:

```text
.rela.dyn R_AARCH64_RELATIVE (0x403)
 -> r_offset runtime source/consumer slot
 -> r_addend Switch physical text owner
```

Before declaring a similar ordinary-inline owner caller-unknown solely because direct ADR/ADRP string XREF is absent, inspect the RELA-slot route.

This is a reusable investigation rule, not blanket authorization for other families.

## 8. Identity policy

```text
identity presentation fields            -> KEEP_JP
authored Korean prose identity literals -> PRESERVE_AS_AUTHORED_KO
runtime-inserted identity                -> KEEP_JP
reverse substitution                     -> FORBIDDEN
```

## 9. Open work

Still open:

- materialize the 47 already-resolved static ordinary-inline R1 rows;
- retain R2884/R2885 as unresolved until consumer semantics are proven, possibly through later shared-route evidence;
- TAI5MSG selective classifications;
- EVENT/TS5 production parser/caller coverage;
- SNR field/record selective parsing;
- R2/R3 corpus;
- builder/serializer/build/IPS;
- runtime font/layout/translation QA.

## 10. Executable next scope — sole authority

After a fresh explicit user signal, resume:

```text
SELECTIVE_KO_REMAINING_STATIC_47_CANDIDATE_CLASSIFICATION_MATERIALIZATION
```

Scope constraints:

```text
include only the 47 static rows already resolved by selected-use audit
exclude R2884 and R2885
create actual per-row candidate/classification values
do not begin builder/build/IPS
```

After reporting that materialization, require another explicit user signal before any further scope.

## 11. Repository write boundary

Repository writes remain restricted to exactly:

```text
create_blob -> create_tree -> create_commit -> update_ref(force=false)
```

No Contents-API write, branch creation, issue/PR write, or force update is permitted.
