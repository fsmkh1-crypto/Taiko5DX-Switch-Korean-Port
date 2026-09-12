# Machine-Readable Accounting Schema — Pilot v0.1

Date: 2026-09-12
Status: PILOT / NOT FROZEN
Scope: schema definition and F1 278-row pilot only. This does not migrate the full canonical corpus and does not authorize builder, IPS, runtime, mapping, or new residual-family work.

## 1. Design goals

The machine layer records current project state without revalidating already canonical evidence. Markdown remains authoritative during the pilot. A generated Markdown view may replace hand-maintained ledgers only after the pilot passes and a later schema-freeze step is explicitly authorized.

The schema separates five concerns with different cardinality and lifetimes:

1. validation claims — mostly stable evidence claims with explicit supersession;
2. source-state revisions — append-only history of each source obligation;
3. Switch actions — actual mutation/no-mutation execution units;
4. source/action edges — explicit N:M relation between obligations and actions;
5. migration/coverage records — provenance and round-trip accounting for the conversion itself.

## 2. Stable identity rules

### 2.1 Claim IDs

`claim_id` is immutable after issuance. Renumbering, reuse, recycling, and deletion are forbidden.

If a claim was split incorrectly, the old claim remains with lifecycle `INVALIDATED` or `SUPERSEDED` and new claim IDs are issued. A claim discovered later is appended with a new ID even if document order no longer matches numeric order.

Claim extraction is therefore a permanent-ID issuance operation.

### 2.2 Source IDs and action IDs

Existing canonical source IDs are reused unchanged. Existing stable F1 action IDs are reused unchanged.

Synthetic test IDs use the reserved prefix `FIXTURE-`. `FIXTURE-*` IDs are forbidden under `data/state/` and `data/pilot/`; the validator must hard-fail if they occur there.

## 3. Validation claims

Canonical shape:

```json
{
  "claim_id": "V094.C01",
  "ledger_id": "V094",
  "claim_type": "FACT | INVARIANT | CORRECTION | INTERPRETATION | EVIDENCE_GAP | BOUNDARY",
  "lifecycle_state": "ACTIVE | SUPERSEDED | INVALIDATED | STALE",
  "verification_state": "VERIFIED | UNVERIFIED | FAILED | NOT_APPLICABLE_WITH_EVIDENCE",
  "subject": "...",
  "predicate": "...",
  "value": {},
  "depends_on_claims": [],
  "depends_on_families": [],
  "supersedes": [],
  "superseded_by": [],
  "source_anchor": {},
  "method": "...",
  "notes": "..."
}
```

`STALE` is not `FAILED`. An invariant becomes `STALE` when a dependency family or relevant canonical input changes. It cannot satisfy a release gate again until reevaluated.

Invariant claims additionally carry `result_state = PASS | FAIL | NOT_RUN | UNKNOWN | NOT_APPLICABLE_WITH_EVIDENCE` and `last_evaluated_against`.

## 4. Source-state history

Source state is append-only. Migration creates revision `1` from the current canonical state; historical Stage1 -> Stage2 -> F1 states are not reconstructed retroactively.

Minimum pilot fields:

```text
source_id
revision
source_family
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
evidence_refs[]
changed_by
supersedes_revision
```

### 4.1 Analysis state

```text
NOT_YET_ANALYZED
ANALYZED_UNRESOLVED
RESOLVED
```

This is independent from `target_status`. An F1-rejected row is `ANALYZED_UNRESOLVED`; an untouched row is `NOT_YET_ANALYZED`.

### 4.2 Applicability and denominators

`total_denominator` for a family is fixed by canonical inventory identity. Progress must never improve merely by silently shrinking scope.

A source can leave `applicable_denominator` only through a verified scope-exclusion claim and must carry `exclusion_claim_id`.

`BLOCKED`, `UNKNOWN`, `NOT_YET_ANALYZED`, `ANALYZED_UNRESOLVED`, and `NATIVE_EQUIVALENT_VERIFIED` remain in the total denominator. `NATIVE_EQUIVALENT_VERIFIED` is applicable-and-closed, not scope-excluded.

Dashboards must report together:

```text
resolved / applicable
resolved / total
excluded / total
```

An increasing exclusion ratio is independently visible and reviewable.

### 4.3 Descriptor granularity

Descriptor containers are grouping records, not progress obligations.

```text
11 descriptor containers -> accounting_role = GROUP
14 descriptor subpatches -> accounting_role = OBLIGATION
```

A container-level conclusion fans out to every covered subpatch, with each leaf subpatch recording the same evidence reference. Descriptor progress denominator is 14, not 11. Historical `27,430` remains a mixed-granularity inventory-record count; the corresponding leaf-obligation record count is `27,419`, but neither number is a universal single progress percentage.

### 4.4 Target identity vs candidate identity

Only canonically promoted targets populate `target_identity`.

Unpromoted but useful hypotheses populate `candidate_target_identity` with their promotion status. A rejected F1 relation is not silently counted as target-resolved merely because its candidate formula remains plausible.

### 4.5 Closure state

`closure_state = OPEN | CLOSED` is separate from `terminal_disposition` so accounting does not infer closure from strings such as `UNRESOLVED` or `CONFLICT`.

`NATIVE_EQUIVALENT_VERIFIED` and `PROVEN_IRRELEVANT` may both have zero actions, but differ in applicability: native-equivalent remains applicable and closed; proven-irrelevant is scope-excluded only with a verified exclusion claim.

### 4.6 Write authority responsibility

Write-authority progress is family-scoped:

```text
authorized / sources for which that family owns authorization responsibility
```

When responsibility moves to another family, `handoff_family` is mandatory. Handoff is not exclusion; the source remains in total/applicable accounting.

## 5. Structured UNKNOWN debt

`unknown_fields` is an array of objects, not field names:

```json
{
  "field": "owner_binding",
  "reason": "...",
  "resolution_requirement": "...",
  "blocks": ["WRITE_AUTHORIZATION", "CLOSURE"],
  "evidence_refs": ["V089"]
}
```

Any UNKNOWN used by an authorization gate blocks authorization. `unknown_debt.json` reports both field-level counts and `resolution_requirement` counts so shared investigations can be prioritized by likely fan-out.

UNKNOWN is never a silent skip state.

## 6. Change provenance

Every source revision carries one change event:

```text
CLAIM
RULE
RECLASSIFICATION
MIGRATION
BULK_RECOMPUTE
MANUAL_CORRECTION
```

`changed_by.refs` identifies the claim/rule/migration event. Initial machine snapshots use `MIGRATION`; they must not masquerade as historical analysis revisions.

## 7. Switch actions and source/action edges

Actions are stored independently from sources. Source rows never contain the authoritative relationship itself.

Edge shape:

```json
{
  "source_id": "...",
  "action_id": "...",
  "role": "PRIMARY | SHARED_OWNER | FRAGMENT | GUARD | SUBSUMED_BY",
  "source_byte_range": null,
  "target_byte_range": [0, 1],
  "evidence_refs": []
}
```

The edge table must represent `1:1`, `1:N`, `N:1`, and `N:M`. A terminal source is allowed to have zero actions where semantics require no mutation. Placeholder/no-op actions are forbidden for unresolved reconstruction work.

## 8. Invariant staleness

Invariant claims carry dependency namespaces such as:

```text
family:mapping
family:romfs
family:font
action_family:F1_LOCALIZATION_STATIC_DIRECT
```

Creating, deleting, or materially changing an action/state in a dependency family marks the invariant `STALE`. A stale invariant cannot satisfy release closure until reevaluated.

## 9. Migration manifest and round-trip gates

Migration is itself accounted work. Every migrated entity records source provenance, migration status, target revision/ID, round-trip state, and diff disposition.

Migration statuses:

```text
PENDING
MIGRATED
ROUNDTRIP_PASS
ROUNDTRIP_EXPLAINED
BLOCKED
```

Markdown conversion uses two gates:

1. exact/semantic round trip for material that was extracted;
2. source-anchor coverage for material that could otherwise be silently omitted.

Every source block receives:

```text
EXTRACTED
NARRATIVE_ONLY
SUPERSEDED_TEXT
NON_ASSERTION_METADATA
UNEXPLAINED
```

Release of a migration stage requires:

```text
unexplained round-trip differences = 0
assertion-bearing UNEXPLAINED source blocks = 0
```

A nonzero explained diff is allowed only with an explicit disposition.


## 10. Pilot storage encoding

The normative shapes above are the semantic schema. The F1 pilot stores large repetitive tables in a deterministic compact/sharded transport representation so the pilot does not duplicate already-canonical V094 action payloads or turn the repository into opaque large artifacts.

- `source_state_compact/` stores the per-source varying identity/category fields; the validator losslessly materializes the §4 revision-1 semantics from the category contract.
- the existing canonical `docs/manifests/F1_STATIC_WRITE_AUTHORIZATION_MANIFEST.jsonl.gz` is reused as the 158-action table authority; `action_table_binding.json` pins its hashes.
- `source_action_edges_compact/` stores the 158 source/action relationships.
- `validation_claims/` and `source_anchor_coverage/` use deterministic hash-indexed JSONL shards. Coverage stores hashes/line ranges rather than duplicating source Markdown bytes; the validator reconstructs each block from the canonical document and checks the exact Git blob/SHA-256.
- `migration_manifest/` stores grouped migrated entity identities with one common PASS status in hash-indexed JSON parts.

This compact encoding is **pilot transport only**, not a schema-freeze decision. A later freeze may choose expanded append-only JSONL, a normalized database, or the compact encoding, but must preserve the same semantic rows and invariants.

### 10.1 Deterministic shard boundary contract

Sharding is a transport/storage concern, never a semantic classification. The pilot applies the following deterministic rules so connector/request-size limits cannot recreate undocumented document fragmentation:

1. **Separate logical datasets first.** Source state, source/action edges, validation claims, source-anchor coverage, and migration entities never share one shard namespace. A shard boundary does not define a semantic family.
2. **Stable logical order before splitting.** Rows are emitted in the validator-defined canonical order for that dataset; consumers concatenate parts strictly in `INDEX.json` order. Filesystem enumeration order is never authoritative.
3. **Pilot row caps are fixed per dataset:** `source_state_compact=40`, `source_action_edges_compact=80`, `validation_claims=10`, `source_anchor_coverage=12`. `migration_manifest/` is grouped by `entity_type` because it is a migration checklist rather than one homogeneous row table. These caps exist only to keep connector requests small; they carry no semantic meaning.
4. **Index location is fixed.** Every sharded logical dataset has an `INDEX.json` in that dataset directory. It is the sole shard-list authority and records ordered part names, per-part row counts/hashes, total rows, and the logical concatenated-content hash.
5. **No silent repartitioning.** Changing the row cap, ordering rule, or grouping rule requires a transport-format/schema-version bump and regeneration of the index/hashes. It does not change the migrated semantic state unless logical-content hashes change.
6. **Validators consume the index, not guessed filenames.** Missing, duplicate, reordered, hash-mismatched, or unindexed parts are hard failures.

Future full-corpus migration may adopt different deterministic row caps or a byte-threshold policy, but that choice must be versioned and documented before the first wider migration. Semantic family boundaries must never be inferred from physical shard boundaries.

## 11. Synthetic-fixture isolation

Cardinality capability tests live only under `tests/fixtures/` and use `FIXTURE-*` IDs. State/progress generators never read fixture paths. State validators hard-fail on a fixture-prefixed ID in project state.

## 12. F1 pilot expected state

The 278-row pilot intentionally contains both success and failure states:

```text
158 target-resolved / authorized / CLOSED / DIRECT_PORT / action present
 75 target-resolved / padding reconstruction blocked / OPEN / action absent
 25 target-resolved / shared-owner binding blocked / OPEN / action absent
  4 target-resolved / capacity blocked / OPEN / action absent
 16 ANALYZED_UNRESOLVED / F1 rule rejected / candidate only / action absent
```

The 25 shared-owner rows hand off to `SHARED_OWNER_BINDING`, not directly to I4: current evidence does not prove replacement conflict. Owner binding must first determine whether I3 shared replacement or I4 redirection is warranted.

## 13. Pilot pass gate

All must pass before schema freeze or full migration:

1. membership preservation;
2. provenance preservation;
3. blocker-meaning preservation;
4. source/action cardinality preservation;
5. no silent UNKNOWN pass;
6. unexplained round-trip diff = 0;
7. unexplained source-anchor coverage blocks = 0.

The pilot may change this schema. Schema freeze is a later, separately authorized step.
