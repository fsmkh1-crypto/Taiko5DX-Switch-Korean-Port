# Machine-Readable Accounting Schema — v1 Candidate

Date: 2026-09-12  
Status: CANDIDATE / NOT FROZEN  
Supersedes for review purposes: Pilot v0.1 schema design. The v0.1 F1 pilot artifacts remain immutable historical evidence.

## 1. Scope and authority

This schema defines the machine-accounting semantic model only. It does not authorize full-corpus migration, residual-family analysis, builder/IPS/runtime work, or game-file modification.

Until an explicit later freeze step, canonical Markdown remains authoritative. The v1 candidate must reproduce the already-verified F1 population and V094 action authority without revalidating the underlying byte analysis.

Semantic schema and transport format are independent:

- `semantic_schema_version` governs entity meaning, lifecycle, referential integrity and progress semantics.
- `transport_format_version` governs sharding, compact encoding and connector-size workarounds.
- A transport change must never silently change semantic rows.
- A semantic change requires a semantic-schema version change even if transport bytes stay identical.

## 2. Canonical entity model

The v1 semantic model contains these linked entity classes:

1. source obligation identity;
2. append-only source-state revision;
3. action identity and append-only action revision;
4. source/action edge;
5. validation claim;
6. invariant definition;
7. invariant evaluation;
8. migration/coverage record.

Stable IDs are never renumbered, reused or recycled.

### 2.1 Source obligation vs source-state revision

A source obligation is the immutable PC-side accounting identity. State changes are append-only revisions.

Migration begins at revision `1` from the canonical current state. Historical Stage1 -> Stage2 -> F1 revisions are not retroactively invented.

Minimum source-state fields:

```text
source_id
revision
source_family
accounting_role
analysis_state
applicability_state
exclusion_claim_id
target_status
target_identity
candidate_target_identity
language_domain
storage_class
window_object_cardinality
logical_owner_count
write_authority
write_authority_family
handoff_family
closure_state
terminal_disposition
blocker
unknown_fields[]
claim_refs[]
legacy_evidence_refs[]
changed_by
supersedes_revision
```

`accounting_role` is:

```text
OBLIGATION
GROUP
```

Descriptor containers are `GROUP`; descriptor subpatches are `OBLIGATION`. GROUP records stay auditable but do not enter the leaf-obligation progress denominator. This is not a scope exclusion and does not use `exclusion_claim_id`.

### 2.2 Analysis, applicability, target and closure are independent axes

`analysis_state`:

```text
NOT_YET_ANALYZED
ANALYZED_UNRESOLVED
RESOLVED
```

`closure_state`:

```text
OPEN
CLOSED
```

`closure_state` is never inferred from `terminal_disposition`.

A source leaves the applicable denominator only through a verified scope-exclusion claim recorded in `exclusion_claim_id`. BLOCKED, UNKNOWN, NOT_YET_ANALYZED and ANALYZED_UNRESOLVED remain in scope. `NATIVE_EQUIVALENT_VERIFIED` is applicable-and-closed. `PROVEN_IRRELEVANT` is excluded only after a verified exclusion claim proves the canonical obligation itself is outside Switch scope.

## 3. Target identity and UNKNOWN

Only canonically promoted targets populate `target_identity`. Hypotheses populate `candidate_target_identity`.

UNKNOWN is structured:

```json
{
  "field": "owner_binding",
  "reason": "...",
  "resolution_requirement": "...",
  "blocks": ["WRITE_AUTHORIZATION", "CLOSURE"],
  "claim_refs": ["V089.C07"],
  "legacy_evidence_refs": ["V089"]
}
```

An UNKNOWN used by an authorization gate is a hard blocker. UNKNOWN is never a silent skip.

The 25 F1 shared-owner rows remain `SHARED_OWNER_BINDING`. Current evidence means replacement conflict is **not proven**; it does not prove absence of conflict. Only owner binding may later branch to I3 agreement or I4 conflict/redirection.

## 4. Evidence references

Machine entities separate atomic and legacy provenance:

```text
claim_refs[]            active or historical machine claim IDs
legacy_evidence_refs[]  canonical pre-migration ledger IDs / legacy evidence IDs
```

New machine decisions must depend on `claim_refs`. Legacy refs remain available for provenance and round-trip reconstruction but do not substitute for atomic dependency edges when atomic claims exist.

## 5. Validation claims

Canonical claim fields:

```text
claim_id
ledger_id
claim_type
lifecycle_state
verification_state
subject
predicate
value
depends_on_claims[]
depends_on_families[]
supersedes[]
superseded_by[]
legacy_supersedes_refs[]
source_anchor
method
notes
```

Allowed claim types:

```text
FACT
INVARIANT
CORRECTION
INTERPRETATION
EVIDENCE_GAP
BOUNDARY
```

Allowed lifecycle states:

```text
ACTIVE
SUPERSEDED
INVALIDATED
STALE
```

`STALE != FAILED`.

Claim IDs are permanent after issuance. If a pilot claim was too composite, it is retained and marked `SUPERSEDED`; new atomic claims receive new IDs. Claim-number width is variable: `Vnnn.Cn+`. Existing IDs are never renumbered to make room.

`supersedes[]` and `superseded_by[]` contain claim IDs only. Pre-claim symbolic references belong in `legacy_supersedes_refs[]`.

## 6. Switch actions

The canonical action representation must preserve the existing three-ledger contract. Minimum normalized fields:

```text
action_id
revision
lifecycle_state
action_family
storage_class
language_domain
switch_object_or_code_sites
input_source_ids[]
replacement_or_behavior
guards[]
apply_priority
capacity_requirement
conflict_state
runtime_test_family
runtime_validation_required
status
claim_refs[]
legacy_evidence_refs[]
changed_by
supersedes_revision
```

Action history is append-only. A material semantic change creates a new revision under the same action identity only when the logical action identity remains the same; otherwise a new action ID is issued and linkage/supersession is explicit.

For the F1 candidate, `docs/manifests/F1_STATIC_WRITE_AUTHORIZATION_MANIFEST.jsonl.gz` remains the only V094 action payload authority. No second action truth source is created. The v1 validator normalizes each manifest row into the action shape above and binds both compressed-file and uncompressed-content hashes.

## 7. Source/action edges

Normalized edge fields:

```text
source_id
action_id
role
source_byte_range
target_byte_range
claim_refs[]
legacy_evidence_refs[]
```

`role`:

```text
PRIMARY
SHARED_OWNER
FRAGMENT
GUARD
SUBSUMED_BY
```

Byte ranges may be null when the edge covers the whole referenced action and the action record owns the authoritative target range.

The table must support 1:1, 1:N, N:1 and N:M. Unresolved/no-edit sources may have zero actions. Placeholder/no-op actions are forbidden.

## 8. Write-authority responsibility

Authorization progress is family-scoped:

```text
authorized / sources for which that family owns authorization responsibility
```

`handoff_family` is mandatory when responsibility moves. Handoff does not reduce total/applicable project accounting.

## 9. Invariants

Invariant definitions and evaluations are separate.

Definition:

```text
invariant_id
scope
depends_on_namespaces[]
method
expected_condition
```

Evaluation:

```text
invariant_id
evaluation_revision
result_state
last_evaluated_against
evidence_refs
```

`result_state`:

```text
PASS
FAIL
NOT_RUN
UNKNOWN
NOT_APPLICABLE_WITH_EVIDENCE
STALE
```

`last_evaluated_against` stores dependency namespace fingerprints/versions. If any dependency fingerprint changes, a prior PASS becomes STALE until reevaluated. STALE is not FAIL but cannot satisfy a release gate.

## 10. Migration and coverage

A normalized migration row records:

```text
migration_id
entity_type
entity_id
source_provenance
target_revision_or_id
migration_status
roundtrip_status
diff_disposition
```

Allowed migration states include:

```text
PENDING
MIGRATED
ROUNDTRIP_PASS
ROUNDTRIP_EXPLAINED
BLOCKED
```

The compact v0.1 F1 grouped migration manifest remains a historical transport input. v1 normalization expands the common defaults into per-entity semantic rows. Full migration must support mixed statuses in one dataset.

Coverage dispositions:

```text
EXTRACTED
NARRATIVE_ONLY
SUPERSEDED_TEXT
NON_ASSERTION_METADATA
UNEXPLAINED
```

Assertion-bearing text is allowed to be `SUPERSEDED_TEXT` only when explicit supersession provenance is present.

Migration release gates remain:

```text
unexplained round-trip differences = 0
assertion-bearing UNEXPLAINED source blocks = 0
```

## 11. Progress and denominators

No universal project percentage is derived from historical `27,430` or leaf-obligation `27,419`.

Every dashboard must name the numerator axis. For target resolution it must show all three:

```text
target_resolved / applicable
target_resolved / total
excluded / total
```

Closure is reported separately, e.g.:

```text
closed / applicable
closed / total
```

GROUP records are excluded from leaf-obligation denominators by accounting role, not by applicability exclusion.

## 12. Transport and materialization integrity

Compact/sharded storage is transport only.

Requirements:

- every logical dataset has one `INDEX.json`;
- INDEX order is authoritative but must follow the declared deterministic ordering rule;
- duplicate, missing, reordered, hash-mismatched or unindexed parts hard-fail;
- logical-content hashes bind compact input;
- semantic materialization is governed by a versioned materialization contract;
- candidate/frozen bindings pin the canonical-json hash of that contract;
- before freeze, the validator emits semantic hashes for fully materialized source state, actions, edges and effective claims;
- freeze must pin those emitted semantic hashes.

Shard boundaries never define semantic families.

## 13. Synthetic fixtures

Synthetic IDs use `FIXTURE-*` and live only under `tests/fixtures/`. Project state must hard-fail if fixture IDs appear in canonical state.

Fixtures validate:

- 1:N / N:1 / N:M edge capability;
- invariant PASS -> STALE dependency behavior;
- mixed migration statuses;
- `SUPERSEDED_TEXT` coverage handling.

Fixtures contribute zero project facts or progress.

## 14. F1 v1-candidate migration rule

The v1 candidate reuses, without technical revalidation:

- 278 F1 source seeds;
- V094 158-action manifest;
- 158 source/action edge seeds;
- 42 v0.1 pilot claims as immutable historical claims;
- 61 source-coverage blocks;
- 697 v0.1 migration entities.

Composite v0.1 claims identified by the schema-freeze review are superseded through `data/pilot/f1_v1_candidate/claim_amendments.json`. New claim IDs are appended; no existing claim ID is renumbered or deleted.

The candidate must preserve:

```text
sources                     278
target resolved             262
analyzed unresolved          16
closed                      158
open                        120
actions                     158
edges                       158
verified exclusions           0
```

The candidate does not authorize builder/runtime work and is not itself a schema freeze.

## 15. Candidate freeze gates

Before explicit v1 freeze authorization, all must pass:

1. exact full F1 membership hash and category membership;
2. V094 manifest binding and normalized action semantics;
3. full edge materialization and cardinality integrity;
4. atomic-claim amendment and supersession referential integrity;
5. source/action/UNKNOWN claim refs resolve to ACTIVE claims;
6. claim source-anchor blob/hash/text integrity;
7. no silent UNKNOWN authorization;
8. exact F1 source-document round trip and coverage closure;
9. invariant staleness fixture;
10. mixed migration-status fixture;
11. unindexed/reordered/missing/hash-mismatched shard hard-fail behavior;
12. explicit target-resolution progress triplet;
13. semantic hashes emitted and pinned.

Passing this candidate review still does not freeze v1. Freeze remains a separately authorized step.
