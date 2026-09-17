# Selective-KO Direction Reconciliation — V292

Date: 2026-09-17 (KST)
Status: CANONICAL PRODUCT-ROUTE RECONCILIATION / DOCUMENTATION ONLY
Validation ID: `V292`
Scope: `SELECTIVE_KO_DIRECTION_RECONCILIATION_MATERIALIZATION`
Implementation authorization: NONE
Build authorization: NONE
New WRITE_SAFE authorization: 0

## 1. Authority and inherited state

Pre-incident canonical product state:

```text
main HEAD = 2172e3b24bce5daf4e7cc1547d3b1d0f3c78e38a
tree      = a222a8a1b72f28ccd732f4b5e3d3ede8cea65e04
last closed validation = V291
```

All previously VERIFIED/CLOSED technical evidence remains inherited without revalidation, including FZ001, Stage1/Stage2/F1 provenance, Mapping 10,036, Pointer-56 analysis, TAI5MSG 33 blocks / 14,832 logical slots, V272-V291, and the exact V288 grammar125 manifest.

This reconciliation changes project routing and product-boundary interpretation only. It does not revoke historical evidence and does not mutate gameplay data.

## 2. Confirmed route divergence

The repository contains two distinct tracks:

```text
historical full-port track
  repository-root PROJECT_STATE.md history through V291

Switch selective Koreanization track
  subtree authority: selective_ko/SELECTIVE_PROJECT_STATE.md
  product: SWITCH_SELECTIVE_KOREANIZATION
```

The selective product was created to stop treating the whole PC Korean patch payload as a Switch release obligation. Its canonical product boundary keeps person/place identity, yomi/readings, calendar/name composition/input, and unresolved dynamic grammar Japanese or deferred unless separately promoted.

The selective migration manifest explicitly classifies legacy `builder/tai5msg.py` as `REFERENCE_ONLY`: its parser/container knowledge is reusable, while its full-file Korean reconstruction policy is not.

V289-V291 nevertheless used the historical integrated builder. V290 records that this builder copied 207 PC payload data files, skipped only PC CWTDAT, reconstructed the entire PC Korean TAI5MSG input, and applied the historical inline-selection path. Therefore V290/V291 remain valid historical/full-port diagnostic artifacts but are not a selective-release baseline.

## 3. Canonical product route restored

Effective after V292:

```text
active product track = SWITCH_SELECTIVE_KOREANIZATION
historical full-port status = FROZEN_DIAGNOSTIC_REFERENCE
V291 package role = HISTORICAL_GRAMMAR125_HARDWARE_DIAGNOSTIC
V291 selective-release baseline = NO
selective builder = NOT IMPLEMENTED
selective corpus classification = NOT YET MATERIALIZED
```

New work must route through `selective_ko/SELECTIVE_PROJECT_STATE.md` and its required reads.

The historical full-port track remains available as evidence/reference and must not be deleted, rewritten, or revalidated merely because the active product route changed.

## 4. Reuse / defer boundary

### Directly reusable foundation

- verified Switch-native Mapping 10,036 realization and assets;
- Korean font/code-space evidence required by selected Korean corpus;
- TAI5MSG parser/container knowledge;
- deterministic TAI5MSG structure lattice: 33 blocks / 14,832 1:1 logical slots;
- F1 source-owner provenance and other verified owner evidence when the same selected source is reused;
- PC Korean content/terminology as source authority and known-good visible Korean as semantic oracle where actually observed.

### Reference / optional later reuse

- V285-V288 grammar125 caller analysis and exact 125-row manifest;
- V289 grammar125 reconstruction implementation technique;
- V290/V291 integrated full-port build/package identities;
- PC runtime descriptors/helpers and legacy full-port action accounting.

The grammar125 corpus is retained as `OPTIONAL_R4_GRAMMAR_EVIDENCE`. It is not a prerequisite for R1-R3 selective release work.

### Excluded from the initial selective product path

- bulk import of the PC patch `data/` payload;
- treating the entire PC Korean `TAI5MSG_JP.DAT` as the product payload;
- heuristic inclusion of historical 17,103 inline records;
- Korean person-name replacement;
- Korean place-name replacement;
- yomi/reading conversion;
- calendar/name-composition/name-entry Koreanization;
- unresolved dynamic grammar formatter families.

## 5. Product inclusion rule

The selective release starts from canonical Switch v1.1.3 structure and applies only explicitly classified and authorized Korean content.

First-release priority remains:

```text
R1  descriptions / explanatory UI
R2  event narration / event-system context
R3  structurally safe dialogue
R4  optional dynamic Korean grammar
```

Identity content such as person names, place names, yomi/readings, name composition, and date identity remains `KEEP_JP` by default.

R3 safe dialogue requires a resolved Switch physical owner/caller set and a complete Korean surface under `STATIC_COMPLETE`, `BRANCH_COMPLETE`, or proven-safe `VARIABLE_INSERT`. `FRAGMENT_COMPOSED` and `GRAMMAR_FORMATTER` remain deferred until their complete composition contract is proven.

## 6. Historical WRITE_SAFE interpretation

Historical explicit WRITE_SAFE authority remains preserved exactly as provenance:

```text
F1 DIRECT_PORT        158
Mapping                 4
grammar125            125
TOTAL                  287
```

V292 adds zero WRITE_SAFE rows and revokes none.

These rows do not automatically mean `INCLUDE_KO` for the selective product. Selective release inclusion additionally requires selective classification, owner/applicability, product disposition, and capacity gates.

Current selective corpus/release state remains:

```text
candidate IDs                 0
TAI5MSG classification rows   0
selective INCLUDE_KO rows     0
selective build               NONE
```

## 7. Rejected / do-not-repeat route

Do not resume the selective product by incrementally subtracting problems from V291.

Rejected as the selective product baseline:

```text
PC payload bulk copy
+ whole-PC-Korean-TAI5MSG reconstruction
+ historical inline heuristic selection
+ local symptom fixes
```

Do not delete V288-V291 or rewrite history. Preserve them as historical diagnostic/evidence artifacts.

## 8. 2026-09-17 Git write incident and recovery boundary

During V292 materialization, forbidden Contents-API actions were selected despite the Git-object-only rule. The accidental history advanced `main` through four commits after `2172e3b...` and introduced only three root sentinel paths relative to that pre-incident state:

```text
__NEVER__
__NEVER2__
__SHOULD_NOT_BE_CALLED__
```

The final pre-recovery incident HEAD was:

```text
a358c43b4fa43cff0f0ab8aff145205fcbf08366
```

Comparison against `2172e3b...` proved that the effective repository delta was limited to those three sentinel paths. No legitimate gameplay/project file changed in the accidental chain.

The V292 forward recovery therefore removes exactly those three paths while preserving history and materializes only the intended V292 documentation/state-routing changes. Force update/history rewrite is forbidden.

Detailed incident provenance and the strengthened invocation rule are recorded in:

`docs/GIT_OBJECT_WRITE_INCIDENT_RECOVERY_20260917.md`

## 9. Next scope / STOP

The next eligible scope, under a fresh explicit user execution signal, is exactly:

`TAI5MSG_SELECTIVE_MESSAGE_CLASSIFICATION_READ_ONLY`

That scope consumes the existing `ART-00000005` TAI5MSG structure lattice and performs classification only.

First partition remains:

```text
simple 1:1 / static-variable population
vs
cross-message / nested grammar-formatter population
```

It must not implement a builder, generate a build, mutate TAI5MSG, auto-issue inclusion authorization, or reopen already VERIFIED structural evidence.

V292 ends here.

## 10. Repository write boundary

Repository mutation is permitted only through the exact action sequence:

```text
create_blob -> create_tree -> create_commit -> update_ref(force=false)
```

`create_file`, `update_file`, `delete_file`, `create_branch`, and any force update are excluded from action selection.