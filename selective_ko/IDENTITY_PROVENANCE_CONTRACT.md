# IDENTITY AND PROVENANCE CONTRACT

Date: 2026-09-15 (KST)
Status: CANONICAL SELECTIVE-KO IDENTITY / PROVENANCE CONTRACT
Track: `SWITCH_SELECTIVE_KOREANIZATION`
Scope: `SELECTIVE_KO_IDENTITY_PROVENANCE_CONTRACT_MATERIALIZATION`

## 1. Purpose

This document defines the identity, provenance, freshness, supersession, evidence, and manual-review contract used by the selective Koreanization extraction pipeline.

It exists to prevent parser locators, generated adapter output, historical artifact layout, or source-row cardinality from becoming accidental permanent identity.

This contract does not create corpus candidates, adapter output, release actions, builder changes, IPS files, or runtime artifacts.

## 2. Normative basis

The contract inherits the following canonical rules without redesign:

- issued IDs are immutable and histories are append-only;
- corrections use explicit supersession rather than deletion or renumbering;
- facts and interpretations remain separate claims;
- generated artifacts are derived evidence, not source authority;
- PC Korean patch data supplies Korean content/source obligation while Switch original structure supplies structural authority;
- unresolved or stale evidence never authorizes inclusion or write.

## 3. ID issuance model

All persistent selective-pipeline IDs are **registry-issued opaque IDs**.

They are never deterministically recomputed from:

- PC RVA;
- resource offset;
- Switch file/virtual offset;
- block/message ordinal;
- EVENT section/operand ordinal;
- decoded text;
- source hash;
- parser output ordering;
- any other native locator.

A stable-looking native anchor may be stored as provenance, but it does not generate the permanent ID.

### 3.1 Canonical registry asset

The ID registry itself is a canonical project asset.

Issued IDs cannot be reconstructed reliably from locators after registry loss. Therefore:

- registry history is append-only;
- an issued ID is never reused;
- an issued ID is never renumbered;
- corrections create a new record and an explicit supersession edge;
- registry loss is a canonical-data-loss event, not a cache miss;
- generated adapter artifacts may reference registry IDs but never replace the registry.

The physical registry files are created in the later adapter-materialization scope. This document fixes their semantics before implementation.

### 3.2 ID namespaces

The registry must provide independent opaque namespaces for at least:

```text
entity_id
candidate_id
edge_id
artifact_id
manual_task_id
classification_id
```

Locator history records may additionally receive opaque record IDs when materialized, but native locators themselves are never permanent entity IDs.

Prefix or display formatting may identify the namespace only. It must not encode semantic role, file offset, parser ordinal, owner class, mechanism class, or disposition.

## 4. Identity layers

### 4.1 `entity_id`

Represents one persistent source/structural entity discovered by an adapter or canonical provenance source.

Examples include:

- one PC patch occurrence entity;
- one Switch physical owner entity;
- later, one TAI5MSG message entity;
- later, one EVENT instruction/text entity.

The `entity_id` survives locator correction.

If evidence proves that the semantic/structural entity itself was misidentified, do not mutate identity. Issue a new entity and connect the old record through `SUPERSEDED_BY`.

### 4.2 `candidate_id`

Represents a selective-Koreanization candidate only after Korean semantic obligation and Switch output responsibility are sufficiently bound under a separately authorized candidate-issuance rule.

Adapter rows do not automatically receive candidate IDs.

The following is a valid normal state:

```text
candidate_id = null
candidate_status = NOT_ISSUED
```

`NOT_ISSUED` is not an error, unresolved ID, or missing-data exception.

The PC source count and Switch owner count are not assumed to have 1:1 cardinality. No source-row-per-candidate rule is permitted.

The exact positive issuance gate for future `candidate_id` creation remains intentionally outside this contract and must be fixed before candidate materialization begins.

### 4.3 `edge_id`

Represents one persistent directed relationship between registry entities or other registry-addressable records.

Edges are stored independently. Do not store a cardinality enum such as `N:1` as the identity of the relationship.

Relationship cardinality is derived from graph degree over the applicable relation set.

This allows 1:1, 1:N, N:1, and N:M relationships to coexist without regenerating existing edge IDs when another edge is discovered.

### 4.4 `artifact_id`

Represents one generated adapter/extractor artifact instance.

Each new generation receives a new `artifact_id`. Regeneration never overwrites historical artifact identity.

Artifacts are derived evidence and never become structural/content authority merely because they are canonical project files.

### 4.5 `manual_task_id`

Represents one independently resolvable manual-review or tooling-debt task.

Multiple manual tasks may target the same entity/candidate/field simultaneously.

### 4.6 `classification_id`

Represents one historical classification decision snapshot when classification materialization begins.

A stale or corrected classification is superseded by a new classification record; it is not overwritten.

## 5. Native locator contract

A native locator answers **where/how the entity is found in one source representation**. It does not answer **what permanent entity ID it is**.

Examples:

```text
PC: pc_rva + resource_offset
Switch: file/virtual offset + owner/table identity
TAI5MSG: block + message_id (+ raw boundary where available)
EVENT: future validated raw structural locator
```

Rules:

1. locators include the exact input identity against which they are valid;
2. locator correction does not change `entity_id` when entity identity itself remains the same;
3. locator history is append-only;
4. old locator records remain as provenance and point to the current locator through explicit supersession;
5. a locator must never be used to recreate a lost registry ID.

EVENT permanent entity issuance is additionally blocked until a future `locator_determinism = PASS` gate proves that the chosen locator can be replayed deterministically from the same canonical input.

Section/operand ordinals alone are not approved permanent EVENT locators.

## 6. Supersession contract

Supersession is explicit and append-only.

At minimum the graph must support:

```text
SUPERSEDED_BY
DERIVED_FROM
BINDS_TO
DEPENDS_ON
```

A correction never deletes the old record merely because the new record is better.

Examples:

```text
locator_v1 -> SUPERSEDED_BY -> locator_v2
entity_old -> SUPERSEDED_BY -> entity_new
classification_v1 -> SUPERSEDED_BY -> classification_v2
```

Historical records remain inspectable and must not silently regain active authority after supersession.

## 7. Edge graph contract

Edges store the smallest independently persistent relationship fact.

Minimum fields when materialized:

```text
edge_id
relation_type
source_id
target_id
field_evidence
provenance
status
```

Cardinality is calculated from the graph, not frozen into edge identity.

### 7.1 Pilot evidence boundary

The contract pilot passed the edge-expression gate, but evidence strength differs by relationship shape:

```text
GATE_3_EDGE_CARDINALITY_EXPRESSION = PASS

1:1
  status = STRUCTURALLY_SUPPORTED
  corpus examples = available

N:1
  status = CORPUS_PROVEN
  evidence = existing F1/cross-boundary/action-collapse corpus

1:N
  status = FIXTURE_EXPRESSION_PROVEN
  corpus_existence = NOT_CLAIMED

N:M
  status = FIXTURE_EXPRESSION_PROVEN
  corpus_existence = NOT_CLAIMED
```

`PASS` must never be summarized as proof that 1:N or N:M relationships have been observed in the game corpus.

Existing corpus evidence includes multiple PC source rows collapsing to one Switch owner/action responsibility, including 2-to-1 groups, larger complete-object collapses, and an 11-source formatter collapse. This proves the need for N:1 graph representation only.

## 8. Artifact manifest and freshness

Every future adapter artifact must contain enough identity to recompute freshness from current canonical inputs.

Minimum artifact manifest fields:

```text
artifact_id
adapter_name
adapter_contract_version
extractor_version
input_manifest
depends_on
output_schema_version
output_hash
```

`input_manifest` records each authoritative/canonical input with its role and exact identity, such as content hash, Git blob/commit identity, or other approved immutable source identity.

### 8.1 Freshness is computed, not trusted

A stored `freshness_status` is never authoritative.

The consumer recomputes freshness against current canonical inputs and contracts.

Allowed computed states:

```text
FRESH
STALE_INPUT
STALE_DEPENDENCY
STALE_CONTRACT
INVALID
```

Meaning:

- `FRESH`: declared inputs, dependencies, and contract identities match current canonical values;
- `STALE_INPUT`: one or more direct source identities changed;
- `STALE_DEPENDENCY`: a canonical dependency changed/superseded;
- `STALE_CONTRACT`: adapter or output contract changed such that the artifact cannot be assumed current;
- `INVALID`: required manifest/provenance data is missing or internally inconsistent.

Only `FRESH` artifacts may act as current derived evidence for downstream gates.

### 8.2 Staleness does not rewrite history

Discovering that an artifact or classification is stale does not mutate its historical result.

A later result receives a new ID and supersedes the prior result.

## 9. Manual task entities

Manual work is represented by independent task entities rather than one row-level boolean.

Minimum fields when materialized:

```text
manual_task_id
target_id
blocked_field
manual_reason
resolution_requirement
status
provenance
```

Required `manual_reason` values:

```text
STRUCTURE_INSUFFICIENT
EXTRACTOR_GAP
SEMANTIC_JUDGMENT
```

Interpretation:

- `STRUCTURE_INSUFFICIENT`: the available canonical structure cannot currently establish the required fact;
- `EXTRACTOR_GAP`: the fact is expected to be machine-extractable, but current tooling does not materialize it;
- `SEMANTIC_JUDGMENT`: Korean meaning/grammar/context requires explicit semantic judgment even after structural facts are available.

One target may have multiple simultaneous tasks. Resolving an `EXTRACTOR_GAP` must not automatically resolve a remaining `SEMANTIC_JUDGMENT` task.

`EXTRACTOR_GAP` counts are a tooling-priority metric: they allow ranking extractor improvements by the number of manual tasks they can eliminate.

## 10. Field-level evidence

Evidence grade is stored at the individual fact/field claim level.

One row may legitimately contain, for example:

```text
PC source identity       = VERIFIED
Switch physical owner    = VERIFIED
usage interpretation     = INFERRED
```

A row-level summary grade, if retained for convenience, never replaces the field-level evidence used by gates.

Each materialized `field_evidence` record must identify at least:

```text
field_name
claim_value
evidence_grade
claim_kind
provenance
```

`claim_kind` distinguishes direct structural/observed fact from interpretation where applicable.

Evidence grades continue to use the canonical set:

```text
VERIFIED
OBSERVED
INFERRED
HINT
REJECTED
```

## 11. Historical artifact edge-recovery state

Historical artifacts may contain a proven count/cardinality result without retaining exact machine-readable edge membership.

The contract represents recovery status without guessing the result:

```text
historical_artifact_edge_recovery =
  RECOVERABLE_FROM_SOURCE
  STRUCTURE_INSUFFICIENT
  NOT_YET_ASSESSED
```

This contract does not adjudicate historical artifacts individually.

The previously known 24 internal-collapse edges whose exact machine-readable membership was not retained remain:

```text
NOT_YET_ASSESSED
```

until the adapter-materialization scope inspects their actual provenance/source recoverability.

Do not pre-classify them as `EXTRACTOR_GAP`, `STRUCTURE_INSUFFICIENT`, recoverable, or unrecoverable merely from the historical summary.

## 12. Contract pilot gates

Scope tested:

```text
SELECTIVE_KO_PC_SOURCE_SWITCH_OWNER_CONTRACT_PILOT
```

The pilot validated identity/provenance contract behavior only. It did not create production registry IDs, production adapter artifacts, candidates, classifications, release actions, or builds.

### Gate 1 — immutable entity identity

```text
same canonical identity on replay -> entity identity remains stable
RESULT = PASS
```

This proves contract behavior, not a production ID algorithm instance.

### Gate 2 — locator correction independence

```text
native locator correction/supersession -> entity_id unchanged
RESULT = PASS
```

When entity identity itself is wrong, a new entity is issued and linked by `SUPERSEDED_BY`.

### Gate 3 — graph cardinality expression

```text
1:1 / 1:N / N:1 / N:M expression -> supported
RESULT = PASS
```

Evidence boundary is mandatory:

- N:1 = corpus-proven;
- 1:N = fixture-expression proven only, corpus existence not claimed;
- N:M = fixture-expression proven only, corpus existence not claimed.

### Gate 4 — freshness recomputation

```text
current identities        -> FRESH
changed direct input      -> STALE_INPUT
changed dependency        -> STALE_DEPENDENCY
changed contract          -> STALE_CONTRACT
missing/inconsistent data -> INVALID
RESULT = PASS
```

### Gate 5 — manual-task reason separation

One target can independently retain `EXTRACTOR_GAP` and later/parallel `SEMANTIC_JUDGMENT` without collapsing the tasks.

```text
RESULT = PASS
```

### Gate 6 — field-level evidence separation

Different fields in one logical row can retain different evidence grades without row-wide promotion.

```text
RESULT = PASS
```

### Gate 7 — candidate not issued

```text
candidate_id = null
candidate_status = NOT_ISSUED
RESULT = PASS
```

The pilot can pass with zero candidate IDs issued. This is the expected state for this stage.

### 12.1 Pilot verdict

```text
PASS = 7 / 7
production registry IDs issued = 0
production adapter artifacts emitted = 0
candidate IDs issued = 0
classification rows emitted = 0
Switch write authorization added = 0
```

## 13. Adapter boundary after this contract

Next adapter materialization is limited to the two READY/near-READY layers:

```text
PC_SOURCE_ADAPTER
SWITCH_OWNER_ADAPTER
```

Its purpose is to create the first production registry/entities/edges/artifact manifests under this contract and validate them on actual canonical inputs.

It must not simultaneously implement:

- `TAI5MSG_STRUCTURE_ADAPTER`;
- `EVENT_TS5_STRUCTURE_ADAPTER`;
- broad mechanism/usage/disposition classification;
- candidate issuance by default;
- selective builder behavior;
- IPS/build/runtime output.

Later order remains:

```text
PC_SOURCE_SWITCH_OWNER_ADAPTER_MATERIALIZATION
-> TAI5MSG_STRUCTURE_ADAPTER
-> EVENT_TS5_STRUCTURE_ADAPTER (only after locator_determinism PASS)
```

## 14. Current boundary

This document materializes a contract only.

No registry data file, entity row, edge row, artifact manifest, manual task, candidate, classification, builder modification, patch, or build is created by this scope.

Next authorized-on-fresh-signal scope:

`PC_SOURCE_SWITCH_OWNER_ADAPTER_MATERIALIZATION`
