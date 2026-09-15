# SWITCH APPLICABILITY, REALIZATION, RELEASE SCOPE, AND WORK-QUEUE TAXONOMY

Date: 2026-09-15 (KST)
Status: CANONICAL SELECTIVE-KO SWITCH APPLICABILITY / REALIZATION / RELEASE-SCOPE CONTRACT
Track: `SWITCH_SELECTIVE_KOREANIZATION`
Scope: `SELECTIVE_KO_SWITCH_APPLICABILITY_REALIZATION_TAXONOMY_MATERIALIZATION`

## 1. Purpose

This document defines the selective Koreanization planning layers that answer four different questions without collapsing them:

1. what the content is and how its visible output is generated;
2. whether an equivalent semantic owner/path exists on Switch;
3. how the obligation can technically be realized on Switch;
4. whether the current release has explicitly chosen to act on that obligation.

It also defines the derived work-queue contract used to turn those independent facts/decisions into actionable work without allowing unresolved rows to disappear.

This document is a **later narrow canonical correction** over older broad product-policy/default wording in `SCRIPT_TAXONOMY_AND_CROSSCUTTING_RULES.md` and `CLASSIFICATION_SCHEMA.md` only for:

- Switch applicability;
- Switch realization;
- release scope;
- derived disposition where release scope is relevant;
- derived work queues.

It does not redefine the existing mechanism, usage, investigation, caller, owner, risk, PC-source, translation, or identity/provenance semantics.

No corpus row is classified by this materialization scope.

## 2. Authority and non-collapse rule

Existing authority remains:

```text
PC Korean content/terminology             -> SOURCE_AUTHORITY
Switch original structure/owner/runtime   -> STRUCTURAL_AUTHORITY
verified Switch runtime realization       -> SWITCH_RUNTIME_AUTHORITY
known-good PC visible Korean result        -> SEMANTIC_ORACLE (observed context only)
PC runtime mechanism                       -> REFERENCE_OR_HINT
```

The following planning layers are independent inputs. One layer may constrain another, but no non-derived axis may be assigned solely because another axis has a particular value.

```text
CONTENT / GENERATION LAYER
  mechanism_class
  usage_class
  investigation_status

SWITCH APPLICABILITY LAYER
  switch_applicability

SWITCH REALIZATION LAYER
  switch_realization
  realization_constraints[]

RELEASE-SCOPE LAYER
  release_scope

DERIVED OUTPUTS
  derived_disposition
  work_queue
```

The first layer continues to use the existing three observed axes; this document does not merge them into one field.

## 3. Switch applicability

`switch_applicability` answers only:

> Does the Switch contain an existing semantic owner/path corresponding to this obligation, and if so, what is the structural relationship?

Allowed values:

```text
EXACT_COUNTERPART
EQUIVALENT_COUNTERPART
COMPOSITE_COUNTERPART
NO_SWITCH_COUNTERPART
COUNTERPART_UNKNOWN
```

### 3.1 `EXACT_COUNTERPART`

Verified evidence binds the obligation to an existing Switch semantic owner/path with materially equivalent semantic responsibility.

This does **not** imply `DIRECT_DATA` realization.

### 3.2 `EQUIVALENT_COUNTERPART`

The exact PC-side object/mechanism is not mirrored, but an existing Switch-native owner/path carries the equivalent semantic responsibility.

### 3.3 `COMPOSITE_COUNTERPART`

The obligation binds to multiple Switch entities/responsibilities or multiple source obligations jointly bind one or more Switch responsibilities such that a simple one-source/one-owner statement is insufficient.

This value describes counterpart topology, not implementation mechanism.

### 3.4 `NO_SWITCH_COUNTERPART`

Verified evidence establishes that no existing Switch semantic owner/path carries the equivalent obligation.

This is **not** equivalent to impossible, blocked, out of scope, or irrelevant.

The following combination is explicitly valid:

```text
switch_applicability = NO_SWITCH_COUNTERPART
switch_realization   = SWITCH_NATIVE_RUNTIME_EQUIVALENT
```

An existing counterpart may be absent while a new Switch-native realization remains technically possible.

### 3.5 `COUNTERPART_UNKNOWN`

Available evidence is insufficient to choose any of the preceding states.

This state may not be silently dropped from accounting or treated as no counterpart.

## 4. Switch realization

`switch_realization` answers only:

> Given the semantic obligation and current Switch evidence, what technical realization family is required or already sufficient?

Allowed values:

```text
DIRECT_DATA
OBJECT_RECONSTRUCTION
REDIRECT_PORT
SWITCH_NATIVE_RUNTIME_EQUIVALENT
EXISTING_NATIVE_BEHAVIOR
REALIZATION_UNRESOLVED
```

`NO_REALIZATION_REQUIRED` is intentionally not used. It is a result-like phrase. Existing sufficient behavior is recorded as `EXISTING_NATIVE_BEHAVIOR`; the no-change work outcome is derived later.

### 4.1 `DIRECT_DATA`

The obligation can be realized within the proven current Switch data owner/storage model without unresolved blocking constraints and without reconstructing the object, redirecting ownership, or adding a runtime semantic family.

### 4.2 `OBJECT_RECONSTRUCTION`

Correct realization requires rebuilding/reconstructing the relevant object/storage/layout while preserving the proven Switch semantic responsibility.

### 4.3 `REDIRECT_PORT`

Correct realization requires redirecting the obligation/reference to different valid Switch storage/owner/path rather than using the current direct object as-is.

### 4.4 `SWITCH_NATIVE_RUNTIME_EQUIVALENT`

The semantic effect requires a Switch runtime behavior family or a Switch-native runtime semantic equivalent.

This does not authorize mechanical transplantation of PC Windows/x86 runtime mechanics.

### 4.5 `EXISTING_NATIVE_BEHAVIOR`

Verified Switch-native behavior already satisfies the semantic obligation. No new mutation is required for that obligation.

### 4.6 `REALIZATION_UNRESOLVED`

A counterpart/obligation may be known, but available technical evidence is insufficient to select a realization family.

This is distinct from `NO_SWITCH_COUNTERPART`.

## 5. Realization constraints

Technical reasons are represented by `realization_constraints[]`, not by overloading realization values.

Each constraint record contains at least:

```text
constraint_kind
constraint_code
field_evidence
provenance
status
```

Allowed `constraint_kind` values:

```text
BLOCKER
DIRECT_NOT_REQUIRED
```

Initial `BLOCKER` codes:

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

Initial `DIRECT_NOT_REQUIRED` code:

```text
NATIVE_BEHAVIOR_ALREADY_SATISFIES_OBLIGATION
```

Multiple constraints may coexist.

### 5.1 Realization/constraint invariants

```text
DIRECT_DATA
  -> unresolved BLOCKER count = 0

OBJECT_RECONSTRUCTION
  -> BLOCKER count >= 1

REDIRECT_PORT
  -> BLOCKER count >= 1

SWITCH_NATIVE_RUNTIME_EQUIVALENT
  -> BLOCKER count >= 1

EXISTING_NATIVE_BEHAVIOR
  -> DIRECT_NOT_REQUIRED count >= 1

REALIZATION_UNRESOLVED
  -> unresolved or UNKNOWN BLOCKER count >= 1
```

A realization value that fails its required constraint contract is invalid.

Blocker counts are intended to support tooling/work-priority analysis, such as measuring how many obligations could become direct candidates if one technical blocker family were closed.

## 6. Realization ownership/cardinality

Realization is not assumed to belong one-per-source-row.

Existing project evidence already permits:

```text
1:1
1:N
N:1
N:M
```

source/owner/action relationships.

Therefore:

- a source entity does not automatically receive one realization value;
- a composite counterpart may require more than one independently executable realization responsibility;
- different components of one semantic obligation may legitimately require different realization families;
- realization responsibility must attach to the actual realization/action unit once that unit is materialized, and must link to source/owner/candidate entities by graph edges.

Whether a dedicated `realization_unit_id` namespace is required remains intentionally unresolved until actual adapter/materialization data demonstrates the needed identity boundary.

Do not compress independently executable reconstruction/runtime/redirection responsibilities into one vague mixed realization merely to keep one value per source row.

## 7. Axis-evidence independence invariant

Every non-derived axis must carry its own field-level evidence.

```text
AXIS_EVIDENCE_INDEPENDENCE = PASS required
```

For `switch_applicability` and `switch_realization`, `field_evidence` must identify structural/technical evidence sufficient for that field's claim. Merely citing a different axis value is not evidence for the new axis.

A validator must fail the record when the evidence chain contains only the shortcut itself and no independent evidence for the target axis.

### 7.1 Mandatory negative shortcut tests

The following shortcuts are explicitly invalid and must be treated as validator test cases, not merely prose examples:

```text
STATIC_COMPLETE       -> DIRECT_DATA
EXACT_COUNTERPART     -> DIRECT_DATA
OUT_OF_SCOPE          -> NO_SWITCH_COUNTERPART
DEFERRED_TO_LATER     -> REALIZATION_UNRESOLVED
NO_SWITCH_COUNTERPART -> BLOCKED
```

Validation rule:

```text
if target_axis.field_evidence
   cites only another axis value/policy decision
   and contains no independent structural/technical evidence
then
   AXIS_EVIDENCE_INDEPENDENCE = FAIL
```

Examples of why the shortcuts are invalid:

- an exact counterpart may still require object reconstruction due to capacity/terminator/storage constraints;
- static complete content may still live behind a non-direct owner/storage path;
- an out-of-scope product choice says nothing about whether a Switch counterpart exists;
- deferral says nothing about whether realization is technically unresolved;
- absence of an existing counterpart does not prove that a Switch-native equivalent cannot be built.

## 8. Release scope

`release_scope` is a product/release-decision axis, not a technical evidence axis.

Allowed values:

```text
NOT_DECIDED
IN_SCOPE
OUT_OF_SCOPE
DEFERRED_TO_LATER
```

### 8.1 Default

The only default is:

```text
release_scope = NOT_DECIDED
```

No technical or semantic class automatically changes this default.

In particular:

```text
IDENTITY / NAME_COMPOSED       != automatic OUT_OF_SCOPE
STATIC_COMPLETE                != automatic IN_SCOPE
GRAMMAR_FORMATTER              != automatic DEFERRED_TO_LATER
```

Existing first-release policy descriptions are planning intent until converted into an explicit release-scope decision under this contract.

### 8.2 Explicit decision requirement

`IN_SCOPE`, `OUT_OF_SCOPE`, and `DEFERRED_TO_LATER` require an explicit decision record containing at least:

```text
decided_by
rationale
decision_provenance
policy_version
```

Materialized decision history must additionally preserve ordering/time and supersession provenance.

Release-scope decisions are append-only historical decisions. A later decision supersedes an earlier one; it does not erase it.

### 8.3 Human/product decision asymmetry

Technical axes change because evidence changes or is superseded.

`release_scope` may change solely because the product/release decision changes.

Therefore a future release may move:

```text
DEFERRED_TO_LATER -> IN_SCOPE
```

without any change to mechanism, applicability, realization, or structural evidence.

Conversely, changing `release_scope` must never mutate technical axes.

### 8.4 Batch scope policy

Explicit scope decisions may be applied by an approved policy to a well-defined set rather than requiring manual per-row clicking.

A batch policy must preserve at least:

```text
policy_version
decided_by
rationale
membership rule or exact membership provenance
supersession history
```

A batch decision is still an explicit product decision; it is not a default inference.

The physical storage schema for batch policies remains deferred until actual materialization.

## 9. Derived disposition bridge

The existing values remain:

```text
INCLUDE_KO
DEFER_KO
KEEP_JP
BLOCKED
UNRESOLVED
```

But for new selective corpus materialization, `derived_disposition` must include `release_scope` as an input. It is not independently stored policy truth.

Minimum bridge:

```text
release_scope = NOT_DECIDED
  -> UNRESOLVED

release_scope = OUT_OF_SCOPE
  -> KEEP_JP

release_scope = DEFERRED_TO_LATER
  -> DEFER_KO

release_scope = IN_SCOPE + required technical/evidence state unresolved
  -> UNRESOLVED

release_scope = IN_SCOPE + all inclusion gates pass
  -> INCLUDE_KO

release_scope = IN_SCOPE + evidence proves no approved realization path remains
  -> BLOCKED
```

`BLOCKED` continues to require exhaustion of currently authorized technical escalation paths; capacity failure or no existing counterpart alone is insufficient.

### 9.1 Narrow correction to older default wording

For new materialized rows:

- `usage_class=IDENTITY` does not itself derive `KEEP_JP`;
- `mechanism_class=NAME_COMPOSED` does not itself derive `KEEP_JP`;
- a grammar/fragment mechanism does not itself create `DEFERRED_TO_LATER` release scope;
- earlier first-release defaults become explicit release-scope policy inputs only after a recorded decision.

This section supersedes older broader wording that could be read as mechanism/usage automatically deciding product scope.

## 10. Work queue is derived, not canonical row state

`work_queue` is derived from current inputs and a versioned queue rule.

It is not a canonical mutable field on a source/candidate row.

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

Queue rules are versioned contracts.

If the queue rule changes, any cached/generated queue artifact based on the prior contract becomes `STALE_CONTRACT` under `IDENTITY_PROVENANCE_CONTRACT.md`.

## 11. Queue totality and precedence

Queue derivation must consume every in-accounting work item.

Hard invariant:

```text
QUEUE_UNASSIGNED = 0
```

Minimum primary queue precedence:

| Condition | Derived primary queue |
|---|---|
| `release_scope=NOT_DECIDED` | `SCOPE_DECISION_QUEUE` |
| `release_scope=OUT_OF_SCOPE` | `OUT_OF_SCOPE_HOLD_QUEUE` |
| `release_scope=DEFERRED_TO_LATER` | `DEFERRED_LATER_QUEUE` |
| `IN_SCOPE` + required technical/evidence state unresolved | `INVESTIGATION_QUEUE` |
| `IN_SCOPE` + `EXISTING_NATIVE_BEHAVIOR` | `NO_CHANGE_REQUIRED` |
| `IN_SCOPE` + `DIRECT_DATA` | `DIRECT_DATA_QUEUE` |
| `IN_SCOPE` + `OBJECT_RECONSTRUCTION` | `OBJECT_RECONSTRUCTION_QUEUE` |
| `IN_SCOPE` + `REDIRECT_PORT` | `REDIRECT_QUEUE` |
| `IN_SCOPE` + `SWITCH_NATIVE_RUNTIME_EQUIVALENT` | `RUNTIME_EQUIVALENT_QUEUE` |
| no defined rule matches | `INVESTIGATION_QUEUE` + `QUEUE_RULE_GAP` |

Example:

```text
release_scope        = IN_SCOPE
switch_applicability = COUNTERPART_UNKNOWN
switch_realization   = REALIZATION_UNRESOLVED
```

must enter `INVESTIGATION_QUEUE`; it may never disappear as skipped/unassigned.

If the same technical state has `release_scope=NOT_DECIDED`, it enters `SCOPE_DECISION_QUEUE` first because whether the current release should spend investigation effort has not yet been decided.

## 12. `QUEUE_RULE_GAP` is a rule defect, not a row defect

`QUEUE_RULE_GAP` is raised only when an in-accounting state combination is not handled by the current versioned queue rule.

The affected row/work item is still routed to `INVESTIGATION_QUEUE` so `QUEUE_UNASSIGNED=0` remains true.

However:

```text
QUEUE_RULE_GAP > 0
  -> queue_rule_version revision candidate
```

A queue-rule gap must be counted separately from semantic/structural investigation backlog.

It must not be hidden as:

- `COUNTERPART_UNKNOWN`;
- `REALIZATION_UNRESOLVED`;
- `EXTRACTOR_GAP`;
- `SEMANTIC_JUDGMENT`;
- ordinary `INVESTIGATION_QUEUE` workload.

This distinction allows the project to tell whether work is blocked by the game/data or by an incomplete routing rule.

The target steady-state invariant is:

```text
QUEUE_UNASSIGNED = 0
QUEUE_RULE_GAP   = 0
```

`QUEUE_UNASSIGNED=0` is mandatory at all times; `QUEUE_RULE_GAP=0` is required before treating the queue rule version as closed for broad production use.

## 13. Historical full-port provenance bridge

Historical full-port decisions are evidence/provenance only for this selective taxonomy.

Historical values such as:

```text
DIRECT_PORT
STRUCTURAL_PORT
REDIRECT_PORT
RUNTIME_PORT
RUNTIME_PORT_REQUIRED_CANDIDATE
NATIVE_EQUIVALENT_VERIFIED
SUBSUMED
PROVEN_IRRELEVANT
```

must **not** be copied directly into `switch_realization` or `release_scope`.

They may support new field evidence, for example:

```text
historical DIRECT_PORT evidence
  -> may support DIRECT_DATA after selective re-evaluation

historical reconstruction evidence
  -> may support OBJECT_RECONSTRUCTION

historical REDIRECT_PORT evidence
  -> may support REDIRECT_PORT

historical runtime evidence
  -> may support SWITCH_NATIVE_RUNTIME_EQUIVALENT

historical NATIVE_EQUIVALENT_VERIFIED evidence
  -> may support EXISTING_NATIVE_BEHAVIOR

historical SUBSUMED/action-collapse evidence
  -> may support owner/edge/realization-unit topology
```

The final selective value must be newly adjudicated in the selective context because the historical full-port track targeted the full obligation set while the selective product has explicit release-scope decisions.

A historical full-port action may therefore remain technically relevant even when the selective release later chooses `OUT_OF_SCOPE` or `DEFERRED_TO_LATER`.

## 14. Relationship to existing risk/capacity rules

This contract does not weaken existing requirements:

- exact target/owner proof remains separate from write safety;
- capacity and terminator proof remain independent requirements;
- shared-owner obligations remain explicit;
- PC padding is not Switch capacity;
- source/action cardinality is not assumed 1:1;
- `COUNTERPART_UNKNOWN`, `REALIZATION_UNRESOLVED`, stale evidence, and unresolved investigation never authorize implementation;
- automatic truncation or translation shortening remains forbidden.

The canonical capacity escalation order remains:

```text
current storage
-> alternate existing storage
-> object/data reconstruction
-> redirect/relocation realization
-> Switch-native runtime semantic equivalent
-> only after technical routes are exhausted: human translation adjustment review
```

## 15. Materialization-time validation requirements

Future production materialization must be able to validate at least:

```text
AXIS_EVIDENCE_INDEPENDENCE
REALIZATION_CONSTRAINT_CONTRACT
RELEASE_SCOPE_EXPLICIT_DECISION
QUEUE_UNASSIGNED_ZERO
QUEUE_RULE_GAP_ACCOUNTING
ARTIFACT_FRESHNESS
FIELD_EVIDENCE_PROVENANCE
```

A broad corpus population must fail closed when a required validator cannot distinguish a technical fact from an inferred shortcut.

The mandatory negative shortcut test set from section 7.1 must be present in the future validator test contract.

## 16. Intentionally unresolved implementation details

This design does not guess the following before real materialization data requires them:

1. exact `queue_rule_version` V1 selector serialization;
2. whether a dedicated `realization_unit_id` registry namespace is necessary;
3. physical storage schema for batch release-scope policy records.

These are implementation-schema decisions, not reasons to weaken the semantic contract above.

## 17. Materialization boundary

This scope materializes taxonomy/contract only.

It creates no:

- production source/owner entity rows;
- candidate IDs;
- classification rows;
- applicability classifications;
- realization classifications;
- release-scope decisions;
- work-queue rows;
- realization units/actions;
- builder changes;
- IPS/build/runtime artifacts.

No existing corpus row is retroactively reclassified by this document alone.

## 18. Next scope

After this contract is canonical, the next planned scope remains:

```text
PC_SOURCE_SWITCH_OWNER_ADAPTER_MATERIALIZATION
```

That stage may materialize the READY PC-source and Switch-owner identity/provenance adapters and the evidence needed by later classifications, but it must not silently populate broad applicability/realization/release-scope decisions merely because this taxonomy exists.

Later planned order remains:

```text
PC_SOURCE_SWITCH_OWNER_ADAPTER_MATERIALIZATION
-> TAI5MSG_STRUCTURE_ADAPTER
-> EVENT_TS5_STRUCTURE_ADAPTER (after locator_determinism PASS)
```
