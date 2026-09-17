# SELECTIVE PROJECT STATE

Date: 2026-09-18 (KST)
Status: V298 ENDING-HELP 39 CANDIDATE/CLASSIFICATION MATERIALIZED / R1 INCLUDE_KO 39 / NO BUILD
Track: `SWITCH_SELECTIVE_KOREANIZATION`

## 1. Resume authority

Repository: `fsmkh1-crypto/Taiko5DX-Switch-Korean-Port`
Branch: `main`
Target: Nintendo Switch title `0100346017304000`, game v1.1.3.

This file is the sole executable next-scope authority for the selective product track. Repository-root `PROJECT_STATE.md` is the sole repository-level resume authority.

Required reads, in authority order:

1. `ENDING_HELP_39_CANDIDATE_CLASSIFICATION_V298.md`
2. `artifacts/ending_help_39_candidate_classification_v1/INDEX.json`
3. `INLINE_R1_LOGICAL_OBJECT_RECONSTRUCTION_AND_REUSABLE_RULES_V297.md`
4. `LEGACY_EVIDENCE_CLAIM_STRENGTH_POLICY_V296.md`
5. `CONTENT_CONTAINER_FIELD_AVAILABILITY_CORRECTION_V295.md`
6. `IDENTITY_IN_PROSE_POLICY.md`
7. `CLASSIFICATION_SCHEMA.md`
8. `SCRIPT_TAXONOMY_AND_CROSSCUTTING_RULES.md`
9. `KNOWN_FAILURES.md`
10. `SWITCH_ORIGINAL_SOURCE_INPUT_CONTRACT.md`
11. `ARCHITECTURE.md`
12. this file

## 2. Product boundary

The product remains selective Koreanization, not a full clone of the PC patch.

Priority scope remains explanatory/UI content, structurally safe narration/system/event text, and proven-safe dialogue. Dedicated person/place identity, yomi, name composition, date/calendar identity presentation, Korean name entry, and unresolved dynamic grammar remain Japanese/deferred unless separately promoted.

Authority remains:

```text
PC Korean content/terminology        -> SOURCE_AUTHORITY
Switch structure/owner/caller        -> STRUCTURAL_AUTHORITY
verified Switch mapping realization  -> SWITCH_RUNTIME_AUTHORITY
known-good PC visible result         -> SEMANTIC_ORACLE
PC runtime mechanism                 -> REFERENCE_OR_HINT
```

## 3. Current materialized selective corpus

V298 is the first actual selective candidate/classification population:

```text
candidate IDs             39
classification IDs        39
INCLUDE_KO rows           39
R1 materialized rows      39
```

IDs:

```text
SEL-CAND-000001 .. SEL-CAND-000039
SEL-CLS-000001  .. SEL-CLS-000039
```

All 39 are ending-help fixed-field objects and are stored in:

`artifacts/ending_help_39_candidate_classification_v1/`

Each row is individual and contains actual source records, JP/KO payload, Switch owner, byte length/capacity, classification fields, risk/evidence, and provenance.

These 39 are not the final R1 corpus total.

## 4. V298 population invariants

```text
usage_class               UI_DESCRIPTION 39/39
mechanism_class           STATIC_COMPLETE 39/39
investigation_status      RESOLVED 39/39
derived_disposition       INCLUDE_KO 39/39
manual overrides          0
risk-flagged rows          0
capacity failures          0
PC conflict rows           0
```

Structure/capacity:

```text
ending records             39
record stride              0x3FF / 1023
help offset                +0x15
help capacity              501 bytes
help PC inline records     102 unique
KO payload incl NUL        48..412 bytes
minimum slack              89 bytes
```

`INCLUDE_KO` is a content/classification disposition only. No builder, IPS, game-file write, layout PASS, or hardware PASS is implied.

## 5. V297 inherited facts

Retain without re-analysis:

```text
PC inline raw records                      17,103
exact source/replacement groups            8,751
external provisional YES                   205
external provisional UNCERTAIN             227
Korean-bearing positive groups             204
positive source occurrences                206
single Switch-location occurrences         191
those collapse to logical objects          189
positive multi-match groups                13
```

External AI triage is a prefilter only.

V297 corrections remain binding:

- `189 unique positive occurrences` is superseded by `191 occurrences -> 189 objects`;
- ending-help 39 uses 102 PC records; 208 belongs to the whole 117-field ending table;
- UNC zero-match = 8 padding/NUL + 3 UTF-16LE;
- R651 selected-use owner is resolved to Switch `0x6A7C21`.

Reusable V297 rules (diff-run != string, object-first reconstruction, source-sequence disambiguation, fixed-stride discovery, NUL-padding continuation, decoder precedence) must be reused.

## 6. Identity policy

```text
identity presentation fields           -> KEEP_JP
authored Korean prose identity literals -> PRESERVE_AS_AUTHORED_KO
runtime-inserted identity               -> KEEP_JP
reverse substitution                    -> FORBIDDEN
```

## 7. Open work

Still open:

- remaining inline R1 logical objects outside ending-help 39;
- full cross-container field availability inventory;
- TAI5MSG selective classifications;
- EVENT/TS5 production parser/caller coverage;
- SNR field/record selective parsing;
- R2/R3 corpus;
- builder/serializer/build/IPS;
- runtime font/layout/translation QA.

## 8. Executable next scope — sole authority

After a fresh explicit user signal, resume:

```text
SELECTIVE_KO_CONTENT_CONTAINER_AND_FIELD_AVAILABILITY_READ_ONLY
```

First focus:

```text
remaining inline R1 logical-object census outside the materialized ending-help 39
```

Do not begin builder/build/IPS in that scope.

## 9. Repository write boundary

Repository writes remain restricted to exactly:

```text
create_blob -> create_tree -> create_commit -> update_ref(force=false)
```

No Contents-API write, branch creation, issue/PR write, or force update is permitted.
