# F1 Machine-Readable Accounting Pilot

Date: 2026-09-12
Base HEAD: `2ccb99141742804ed34289cd96102a3b69b3b9b3`
Status: PILOT PASS / SCHEMA NOT FROZEN

## 1. Scope

This stage implements only the agreed machine-accounting pilot:

- schema definition;
- F1 278-row source-state migration snapshot;
- 158 existing V094 actions and 158 source/action edges;
- V088-V095 atomic claim migration;
- F1 audit source-anchor coverage and exact textual round trip;
- isolated synthetic 1:N / N:1 / N:M validator fixture.

It does not migrate the full project corpus, analyze the remaining 797 residual rows, freeze the schema, edit the builder, emit IPS, or perform runtime/game-file work.

## 2. Pilot source-state result

The 278 historical F1 residual source rows reproduce the canonical disposition exactly:

```text
DIRECT_PORT authorized                 158
PADDING_RECONSTRUCTION_REQUIRED         75
SHARED_OWNER_BINDING_REQUIRED           25
TERMINATOR_CAPACITY_FAIL                 4
F1_RULE_REJECTED                        16
TOTAL                                  278
```

Machine-state axes:

```text
analysis_state
  RESOLVED                  262
  ANALYZED_UNRESOLVED        16

target_status
  RESOLVED                  262
  UNRESOLVED                 16

closure_state
  CLOSED                    158
  OPEN                      120

verified scope exclusions     0
applicable denominator       278
```

The 16 V088-rejected rows contain `candidate_target_identity` only. Their canonical `target_identity` is null, preserving the existing rule that their candidate relation was not proven false but was not promoted.

## 3. Write-authority responsibility

Write authority is family-scoped rather than measured as `158 / 262`:

```text
F1_LOCALIZATION_STATIC_DIRECT  158 / 158 authorized
F1_PADDING_RECONSTRUCTION        0 / 75  open
F1_STORAGE_RECONSTRUCTION        0 / 4   open
SHARED_OWNER_BINDING             0 / 25  open
```

The 25 shared-owner rows hand off to `SHARED_OWNER_BINDING`, not directly to I4. Current canonical evidence does not prove replacement conflict. Owner binding must determine whether I3 shared replacement or I4 redirection is appropriate.

Handoff does not exclude a source from total/applicable accounting.

## 4. Actions and edges

The pilot reuses the exact 158 V094 stable authorization action IDs.

```text
source revisions       278
Switch actions         158
source/action edges    158
```

Only the 158 closed `DIRECT_PORT` sources have actions/edges. The 75 padding, 25 shared-owner, 4 capacity, and 16 rule-rejected rows intentionally have zero placeholder actions.

The ordered authorized source-ID SHA-256 remains:

`87d5a7531b5e2b3841fe4ba093a87dd9da11e8c85b5d4184c6ae705436c1833e`

## 5. UNKNOWN debt

UNKNOWN is structured debt, not a skip state.

```text
target_identity   16
owner_binding     25
TOTAL             41 unknown items / 41 affected sources
```

Each item records `reason`, `resolution_requirement`, `blocks`, and evidence references. Every UNKNOWN item that blocks `WRITE_AUTHORIZATION` is verified to remain unauthorized.

## 6. Claim migration

V088-V095 were split into 42 atomic claims.

The pilot codifies these extraction rules:

- independently falsifiable/supersedable values split into separate claims;
- fact and interpretation are separate claims with explicit dependency;
- `not proven`, missing provenance, or unresolved ownership is an explicit `EVIDENCE_GAP`, not absence of a claim;
- verified zero results remain ordinary facts;
- downstream authorization boundaries are explicit `BOUNDARY` claims;
- claim IDs are immutable after issuance.

No V001-V087 claims were migrated in this stage.

## 7. Source-anchor coverage and round trip

`docs/F1_LOCALIZATION_SEQUENCE_AUDIT.md` was used as the source-coverage pilot document.

Its exact Git blob identity is:

`ba9c660cf6f229ec2b19f024b9bc2cef94d26a44`

Coverage result:

```text
source blocks                 61
assertion-bearing blocks      47
EXTRACTED blocks              47
NARRATIVE_ONLY blocks          2
NON_ASSERTION_METADATA        12
UNEXPLAINED blocks             0
```

All blocks are stored with path, source blob, heading, line range, block hash and coverage disposition. The exact source document can be reconstructed byte-for-byte from the coverage records; reconstructed SHA-256 equals the source SHA-256 `e0087ccbb3460df384469b8a91ab4b412dce3e8d4ebd5a5833aa25dc7e74e667`.

The V087 HEAD-impact section is outside the agreed V088-V095 atomic-claim pilot. It is not omitted: its blocks are explicitly covered by the legacy canonical evidence reference `V087`.

## 8. Cardinality fixture isolation

Synthetic 1:N, N:1 and N:M cases live only at:

`tests/fixtures/machine_accounting_cardinality.json`

All synthetic IDs use `FIXTURE-*`. The validator hard-fails if that prefix appears in project pilot state. Progress and UNKNOWN-debt data do not read fixture content.

The fixture validates schema capability only and contributes zero project facts or progress rows.

## 9. Seven pilot gates

All seven required gates pass:

```text
membership preservation                 PASS
provenance preservation                 PASS
blocker meaning preservation            PASS
source/action cardinality preservation  PASS
UNKNOWN silent-pass prevention          PASS
unexplained round-trip diff = 0         PASS
source-anchor unexplained blocks = 0    PASS
```

Validator result: `PASS`.

## 10. Storage and granularity rule

The historical `27,430` remains a valid mixed-granularity inventory-record count. Descriptor containers (`11`) are grouping rows, while descriptor subpatches (`14`) are leaf obligations.

For progress accounting:

- descriptor container = `GROUP`;
- descriptor subpatch = `OBLIGATION`;
- descriptor denominator = `14`;
- mixed-granularity `27,430` is not a universal progress denominator;
- removing the 11 grouping records yields a leaf-obligation record count of `27,419`, but that number also must not be treated as one universal project completion percentage.

## 11. Compact/sharded pilot storage

The pilot uses deterministic compact/sharded transport while preserving the normative schema semantics. This avoids duplicating the already-canonical V094 action payload and keeps reviewable datasets small.

Primary paths:

- `data/pilot/f1/source_state_compact/` — 278 revision-1 source seeds, losslessly expanded by the validator;
- `data/pilot/f1/action_table_binding.json` — binds the existing V094 158-action manifest as action authority;
- `data/pilot/f1/source_action_edges_compact/` — 158 source/action edges;
- `data/pilot/f1/validation_claims/` — 42 atomic claims in deterministic hash-indexed shards;
- `data/pilot/f1/migration_manifest/` — 697 grouped migrated entity IDs with common PASS status;
- `data/pilot/f1/source_anchor_coverage/` — 61 source blocks in deterministic hash-indexed shards without duplicating the original Markdown bytes;
- `generated/pilot/f1/` — progress, UNKNOWN debt, round-trip and validator summaries.

Every shard index records part hashes and a logical-content hash. The existing `docs/manifests/F1_STATIC_WRITE_AUTHORIZATION_MANIFEST.jsonl.gz` remains the action payload authority rather than being copied into a second pilot action table. Compact transport is a pilot implementation detail and is not frozen as the eventual full-corpus storage format.

Pilot shard boundaries are deterministic and transport-only: logical datasets are separated first; rows stay in canonical logical order; row caps are `40` for source state, `80` for source/action edges, `10` for validation claims, and `12` for source-anchor coverage; migration-manifest parts are grouped by entity type. Each dataset directory's `INDEX.json` is the authoritative ordered shard list and contains per-part hashes plus the logical-content hash. Validators must read that index and hard-fail on missing/unindexed/reordered/hash-mismatched parts. Shard boundaries carry no family or disposition semantics.

## 12. Boundary and next decision

The schema is deliberately **not frozen** by this pilot. Canonical Markdown remains authoritative. The machine pilot is a validated migration candidate and stress test.

A fresh execution signal is required before either:

1. freezing/amending the schema based on this pilot; or
2. authorizing any wider V001-V095 / source-corpus migration.

No 797-family analysis or builder/runtime work was performed.
