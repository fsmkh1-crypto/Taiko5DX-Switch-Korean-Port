# SELECTIVE PROJECT STATE

Date: 2026-09-15 (KST)
Status: SWITCH_APPLICABILITY_REALIZATION_TAXONOMY_MATERIALIZED / IDENTITY_PROVENANCE_CONTRACT_MATERIALIZED / CONTRACT_PILOT_7_OF_7_PASS / NO PRODUCTION_REGISTRY / NO CORPUS MATERIALIZATION / NO BUILD
Track: `SWITCH_SELECTIVE_KOREANIZATION`

## 1. Base identity

Repository: `fsmkh1-crypto/Taiko5DX-Switch-Korean-Port`
Umbrella branch: `main`
Initialization base HEAD: `f652333af41271b32bafb2054a1a1c3c853f1105`
Selective-project initialization commit: `2fb74c1e53030750012bcf7f13cf2ad8ebe43b2d`
Nintendo Switch title ID: `0100346017304000`
Target game version: `1.1.3`

This file is the resume authority for the `selective_ko/` subtree only. The repository-root `PROJECT_STATE.md` remains authoritative for the historical full-port track.

## 2. Product target

The selective product target is not a complete clone of the PC Korean patch.

Priority Korean scope:

- character/person descriptions;
- region/location descriptions, while place names themselves may remain Japanese;
- tools/items descriptions;
- techniques/skills descriptions;
- event narration/body/system/context text;
- static or otherwise proven-safe dialogue when practical.

Likely first-release exclusions/deferments include person/place identity, yomi, calendar formatting, name composition/input, and unresolved dynamic grammar, but **these are product-policy intentions only until an explicit `release_scope` decision is materialized** under `SWITCH_APPLICABILITY_REALIZATION_TAXONOMY.md`.

Translation quality review remains:

```text
translation_review_status = DEFER_TO_RUNTIME_QA
```

## 3. Inherited VERIFIED assets

Inherited without revalidation unless identity changes or contradictory evidence appears:

- Switch v1.1.3 `main` identity and Build ID;
- Stage1/Stage2/F1/FZ001 structural discoveries as provenance sources;
- L1/L2/L3 physical/semantic owner findings where applicable;
- Mapping 10,036 semantic obligation and verified Switch realization family;
- Mapping forward/reverse/round-trip PASS on the tested Eden Android route;
- Switch decoder evidence for compact Korean bytes when they reach the decoder;
- Switch Japanese halfwidth normalization ownership/route findings;
- PC Korean translation corpus, terminology, mapping/font assets as source evidence;
- TAI5MSG container/message parser knowledge;
- existing EVENT/TS5 structural observations;
- known failure/rejected-hypothesis history;
- full-port portability/action/owner evidence as provenance only for selective adjudication.

Existing full-port WRITE_SAFE does not automatically authorize selective-project output.

## 4. PC patch authority model

```text
PC Korean translation/content/terminology     -> SOURCE_AUTHORITY
PC mapping/font source obligation             -> SOURCE_AUTHORITY
verified Switch mapping/font realization      -> SWITCH_RUNTIME_AUTHORITY
Switch script/control/owner/runtime structure -> STRUCTURAL_AUTHORITY
known-good PC Korean visible result           -> SEMANTIC_ORACLE (observed context only)
PC runtime mechanism                          -> REFERENCE_OR_HINT
PC workaround/known defect                    -> NON_AUTHORITATIVE_EVIDENCE
```

Conflict rule:

```text
structure = Switch
content/semantic obligation = PC source/oracle
implementation = Switch-native design
```

## 5. Current repository assets

Direct-reuse family:

- `reuse/mapping10036/build_mapping10036_diag.py`
- `reuse/mapping10036/mapping10036_helper_v2.s`
- `reuse/mapping10036/mapping10036_helper_v2.ld`

Reference-only family:

- `reference/tai5msg_legacy_reconstruction.py`
- `reference/t5k_pc_patch_parser.py`

Reference-only code must not become release behavior without separate review against the selective scope.

## 6. Canonical design documents and precedence

Current selective design baseline includes:

- `ARCHITECTURE.md`
- `SCRIPT_TAXONOMY_AND_CROSSCUTTING_RULES.md`
- `IDENTITY_PROVENANCE_CONTRACT.md`
- `SWITCH_APPLICABILITY_REALIZATION_TAXONOMY.md`
- `CLASSIFICATION_SCHEMA.md`
- `EVENT_EXTRACTION_SCHEMA.md`
- `KNOWN_FAILURES.md`
- `MIGRATION_MANIFEST.json`

Authority by question:

1. `SCRIPT_TAXONOMY_AND_CROSSCUTTING_RULES.md`
   - mechanism/usage/investigation taxonomy;
   - caller/owner/risk/mechanism-decision rules;
   - source authority and safe-dialogue structural rules.
2. `IDENTITY_PROVENANCE_CONTRACT.md`
   - registry-issued opaque IDs;
   - native locator separation;
   - edge graph/cardinality derivation;
   - artifact freshness;
   - manual-task and field-evidence rules.
3. `SWITCH_APPLICABILITY_REALIZATION_TAXONOMY.md`
   - Switch applicability;
   - Switch realization and constraints;
   - release scope;
   - derived disposition bridge where release scope is relevant;
   - versioned work-queue derivation and queue accounting.
4. `CLASSIFICATION_SCHEMA.md`
   - selective-product presentation bridge, except where its older broad product-default wording is narrowly superseded by item 3.
5. container-specific schemas such as `EVENT_EXTRACTION_SCHEMA.md`
   - additional source-specific metadata only.

`SWITCH_APPLICABILITY_REALIZATION_TAXONOMY.md` is a later narrow correction. It does not erase older provenance; it supersedes only older wording that could be read as mechanism/usage automatically deciding release scope, realization, or final work queue.

## 7. Common content/generation taxonomy

Existing observed/classified fields remain independent:

```text
mechanism_class
usage_class
investigation_status
```

Mechanism classes:

```text
STATIC_COMPLETE
BRANCH_COMPLETE
VARIABLE_INSERT
PARTICLE_SENSITIVE_INSERT
NUMERIC_COUNTER_FORMAT
FRAGMENT_COMPOSED
GRAMMAR_FORMATTER
NAME_COMPOSED
MECHANISM_MIXED
```

Usage classes:

```text
UI_DESCRIPTION
NARRATION_SYSTEM
DIALOGUE
IDENTITY
OTHER
```

Investigation status:

```text
RESOLVED
CALLER_UNKNOWN
NOT_INVESTIGATED
```

Existing mechanism-decision inputs and risks remain in force, including `append_after`, variable-source provenance, particle adjacency, dynamic-counter evidence, shared-owner risk, cross-message composition, PC occurrence conflict, and capacity risk.

## 8. Identity/provenance contract

Persistent pipeline IDs are registry-issued opaque IDs and are not generated from RVA, offsets, parser ordinals, text, or hashes.

Minimum namespaces already fixed by contract:

```text
entity_id
candidate_id
edge_id
artifact_id
manual_task_id
classification_id
```

The registry itself is canonical append-only project data.

Native locators are versioned provenance. Locator correction does not change entity identity when the entity remains the same.

Valid normal state:

```text
candidate_id = null
candidate_status = NOT_ISSUED
```

Candidate issuance remains intentionally later than adapter-row creation.

Edge cardinality is derived from graph degree, not stored as immutable edge identity.

Contract-pilot evidence boundary remains:

```text
N:1 = CORPUS_PROVEN
1:N = FIXTURE_EXPRESSION_PROVEN / CORPUS_EXISTENCE_NOT_CLAIMED
N:M = FIXTURE_EXPRESSION_PROVEN / CORPUS_EXISTENCE_NOT_CLAIMED
```

Artifact freshness is recomputed:

```text
FRESH
STALE_INPUT
STALE_DEPENDENCY
STALE_CONTRACT
INVALID
```

Manual tasks remain separate entities with reasons:

```text
STRUCTURE_INSUFFICIENT
EXTRACTOR_GAP
SEMANTIC_JUDGMENT
```

Historical exact-edge recovery state remains:

```text
RECOVERABLE_FROM_SOURCE
STRUCTURE_INSUFFICIENT
NOT_YET_ASSESSED
```

The known 24 internal-collapse edges whose exact machine-readable membership was not preserved remain `NOT_YET_ASSESSED` until actual adapter provenance is inspected.

## 9. Switch applicability layer

Canonical values:

```text
EXACT_COUNTERPART
EQUIVALENT_COUNTERPART
COMPOSITE_COUNTERPART
NO_SWITCH_COUNTERPART
COUNTERPART_UNKNOWN
```

Important boundary:

```text
NO_SWITCH_COUNTERPART != impossible
NO_SWITCH_COUNTERPART != OUT_OF_SCOPE
NO_SWITCH_COUNTERPART != BLOCKED
```

The following combination is explicitly valid when supported by independent evidence:

```text
NO_SWITCH_COUNTERPART
+ SWITCH_NATIVE_RUNTIME_EQUIVALENT
```

## 10. Switch realization layer

Canonical values:

```text
DIRECT_DATA
OBJECT_RECONSTRUCTION
REDIRECT_PORT
SWITCH_NATIVE_RUNTIME_EQUIVALENT
EXISTING_NATIVE_BEHAVIOR
REALIZATION_UNRESOLVED
```

`NO_REALIZATION_REQUIRED` is not used. Existing sufficient behavior is represented by `EXISTING_NATIVE_BEHAVIOR`; no-change work is derived later.

Realization is not assumed one-per-source-row. It belongs to actual realization/action responsibility once that unit is materialized, and source/owner/candidate relationships remain graph-based.

Whether a dedicated `realization_unit_id` namespace is needed remains intentionally unresolved until real materialization demonstrates the identity boundary.

## 11. Realization constraints

Use:

```text
realization_constraints[]
constraint_kind = BLOCKER | DIRECT_NOT_REQUIRED
```

Initial BLOCKER codes:

```text
CAPACITY
TERMINATOR
SHARED_OWNER
STORAGE_MUTABILITY
LANGUAGE_DOMAIN
STRUCTURE_MISMATCH
CONTROL_DEPENDENCY
RUNTIME_SEMANTICS
NO_EXISTING_COUNTERPART
UNKNOWN
```

Initial DIRECT_NOT_REQUIRED code:

```text
NATIVE_BEHAVIOR_ALREADY_SATISFIES_OBLIGATION
```

Hard invariants:

```text
DIRECT_DATA
  -> unresolved BLOCKER count = 0

OBJECT_RECONSTRUCTION / REDIRECT_PORT / SWITCH_NATIVE_RUNTIME_EQUIVALENT
  -> BLOCKER count >= 1

EXISTING_NATIVE_BEHAVIOR
  -> DIRECT_NOT_REQUIRED count >= 1

REALIZATION_UNRESOLVED
  -> unresolved or UNKNOWN BLOCKER count >= 1
```

## 12. Axis-evidence independence

Hard gate:

```text
AXIS_EVIDENCE_INDEPENDENCE = PASS required
```

Every non-derived axis requires its own `field_evidence`. A target-axis value may not be assigned merely because another axis or product decision has a particular value.

Mandatory negative validator cases:

```text
STATIC_COMPLETE       -> DIRECT_DATA
EXACT_COUNTERPART     -> DIRECT_DATA
OUT_OF_SCOPE          -> NO_SWITCH_COUNTERPART
DEFERRED_TO_LATER     -> REALIZATION_UNRESOLVED
NO_SWITCH_COUNTERPART -> BLOCKED
```

If target-axis evidence cites only the shortcut source value and no independent structural/technical evidence, validation must FAIL.

## 13. Release scope

Canonical values:

```text
NOT_DECIDED
IN_SCOPE
OUT_OF_SCOPE
DEFERRED_TO_LATER
```

Only default:

```text
release_scope = NOT_DECIDED
```

`IN_SCOPE`, `OUT_OF_SCOPE`, and `DEFERRED_TO_LATER` require an explicit decision with at least:

```text
decided_by
rationale
decision_provenance
policy_version
```

Release scope is intentionally asymmetric with technical axes:

- technical axes change because evidence changes/supersedes;
- release scope may change because a product/release decision changes;
- release-scope change must not mutate technical axes.

Batch release-scope decisions are allowed only as explicit versioned policies with decision provenance and exact/rule-based membership provenance. Batch policy storage format remains deferred until actual materialization.

## 14. Derived disposition bridge

Allowed values remain:

```text
INCLUDE_KO
DEFER_KO
KEEP_JP
BLOCKED
UNRESOLVED
```

For new materialization, `release_scope` is an explicit input:

```text
NOT_DECIDED                     -> UNRESOLVED
OUT_OF_SCOPE                    -> KEEP_JP
DEFERRED_TO_LATER               -> DEFER_KO
IN_SCOPE + required state open  -> UNRESOLVED
IN_SCOPE + all inclusion gates  -> INCLUDE_KO
IN_SCOPE + no approved path     -> BLOCKED
```

Therefore `usage_class=IDENTITY` or `mechanism_class=NAME_COMPOSED` does not automatically derive `KEEP_JP`; an explicit scope decision must exist first.

`BLOCKED` still requires evidence that currently authorized escalation paths are exhausted. Capacity failure or no existing counterpart alone is insufficient.

## 15. Work-queue contract

Work queue is derived, not canonical row state.

Conceptually:

```text
work_queue = f(
  content/generation taxonomy,
  switch_applicability,
  switch_realization,
  release_scope,
  realization_constraints,
  risk/evidence/freshness,
  queue_rule_version
)
```

Queue rules are versioned. Changing them makes prior cached/generated queue artifacts `STALE_CONTRACT`.

Minimum primary queue precedence:

| Condition | Queue |
|---|---|
| `NOT_DECIDED` | `SCOPE_DECISION_QUEUE` |
| `OUT_OF_SCOPE` | `OUT_OF_SCOPE_HOLD_QUEUE` |
| `DEFERRED_TO_LATER` | `DEFERRED_LATER_QUEUE` |
| `IN_SCOPE` + technical/evidence unresolved | `INVESTIGATION_QUEUE` |
| `IN_SCOPE` + `EXISTING_NATIVE_BEHAVIOR` | `NO_CHANGE_REQUIRED` |
| `IN_SCOPE` + `DIRECT_DATA` | `DIRECT_DATA_QUEUE` |
| `IN_SCOPE` + `OBJECT_RECONSTRUCTION` | `OBJECT_RECONSTRUCTION_QUEUE` |
| `IN_SCOPE` + `REDIRECT_PORT` | `REDIRECT_QUEUE` |
| `IN_SCOPE` + `SWITCH_NATIVE_RUNTIME_EQUIVALENT` | `RUNTIME_EQUIVALENT_QUEUE` |
| no defined rule matches | `INVESTIGATION_QUEUE + QUEUE_RULE_GAP` |

Hard accounting invariant:

```text
QUEUE_UNASSIGNED = 0
```

Unknown/unresolved technical states never disappear from accounting.

## 16. Queue-rule defect accounting

`QUEUE_RULE_GAP` is a queue-rule defect, not a semantic row defect.

Affected work still enters `INVESTIGATION_QUEUE`, preserving `QUEUE_UNASSIGNED=0`.

But:

```text
QUEUE_RULE_GAP > 0
  -> queue_rule_version revision candidate
```

Queue-rule-gap counts must be separate from ordinary investigation/manual/extractor backlog.

Target closed state for broad production use:

```text
QUEUE_UNASSIGNED = 0
QUEUE_RULE_GAP   = 0
```

## 17. Full-port provenance bridge

Historical full-port values such as `DIRECT_PORT`, `STRUCTURAL_PORT`, `REDIRECT_PORT`, `RUNTIME_PORT`, `NATIVE_EQUIVALENT_VERIFIED`, `SUBSUMED`, and related action families are **evidence/provenance only**.

They are not imported directly into selective `switch_realization`, `release_scope`, or `derived_disposition`.

Selective values must be newly adjudicated under the selective product contract because the historical track targeted the full obligation set while the selective project has explicit release-scope decisions.

## 18. Event/TAI5MSG and translation boundaries

EVENT membership alone never implies safety or scope.

EVENT/TS5 remains blocked from production identity materialization until its future `locator_determinism = PASS` gate.

TAI5MSG remains PARTIAL/strong-foundation and is not part of the next READY-two-adapter materialization.

Translation quality review remains deferred to runtime QA and does not replace structural/applicability/realization evidence.

## 19. Current materialization boundary

Materialized in this state:

- common script taxonomy;
- identity/provenance contract;
- 7/7 identity/provenance contract pilot result;
- Switch applicability/realization/release-scope/work-queue taxonomy contract.

Still **not** materialized:

- production identity registry files;
- production PC-source/Switch-owner entity rows;
- production edges/artifact manifests;
- candidates;
- classification rows;
- applicability/realization classifications;
- release-scope decisions;
- work-queue artifacts;
- realization units/actions;
- selective builder changes;
- IPS/build/runtime release artifact.

No existing corpus row is reclassified merely by materializing the new taxonomy.

## 20. Next scope

Next planned scope:

```text
PC_SOURCE_SWITCH_OWNER_ADAPTER_MATERIALIZATION
```

Boundary for that scope:

1. materialize only `PC_SOURCE_ADAPTER` and `SWITCH_OWNER_ADAPTER` under the identity/provenance contract;
2. create first production registry/entity/edge/artifact-manifest records using actual canonical inputs;
3. recompute freshness rather than trust stored labels;
4. preserve field-level evidence and separate manual-task entities;
5. leave `candidate_id` unissued by default;
6. assess historical edge recoverability only where actual inputs/provenance require it;
7. do not broadly populate applicability/realization/release-scope values merely because the taxonomy exists;
8. do not implement `TAI5MSG_STRUCTURE_ADAPTER` yet;
9. do not implement `EVENT_TS5_STRUCTURE_ADAPTER` yet;
10. do not modify the selective builder or produce a build.

Later planned order:

```text
PC_SOURCE_SWITCH_OWNER_ADAPTER_MATERIALIZATION
-> TAI5MSG_STRUCTURE_ADAPTER
-> EVENT_TS5_STRUCTURE_ADAPTER (after locator_determinism PASS)
```

After the next stage report: STOP and require a fresh explicit user execution signal.
