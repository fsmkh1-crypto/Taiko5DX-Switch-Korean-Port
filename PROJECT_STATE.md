# PROJECT_STATE

Last updated: 2026-09-12 (KST)

This file is the **sole project-resume authority**. Historical documents may contain valid evidence and old “next step” language, but they do not override this file.

<!-- PROJECT_RESUME_V2
{
  "schema": "PROJECT_RESUME_V2",
  "scope_id": "SCHEMA_FREEZE_DECLARATION",
  "scope_kind": "REPOSITORY_WRITE",
  "status": "STOPPED_AWAITING_USER_SIGNAL",
  "last_closed_validation_id": "V107",
  "last_closed_stage_commit": "ed0e4f2ffe8f9e1c646b96078a5c37ca57f8afea",
  "last_closed_ci_run_id": 34691523117,
  "last_closed_ci_validation_id": "V107",
  "last_closed_ci_conclusion": "success",
  "remote_io_metrics_location": "Google Drive / GPT / 태합입지전 프로젝트 / REMOTE_IO_METRICS.jsonl",
  "ruleset_rebase_status": "COMPLETE",
  "repository_write_mode": "GIT_OBJECT_ONLY_WRITE_MODE",
  "repository_write_allowed_actions": [
    "create_blob",
    "create_tree",
    "create_commit",
    "update_ref"
  ],
  "authority_freshness_status": "COMPLETE",
  "rules_workflow_cleanup_status": "COMPLETE",
  "pre_freeze_governance_cleanup_status": "COMPLETE_V106",
  "pre_freeze_hash_pin_status": "COMPLETE_V107_CORRECTED",
  "machine_fact_binding": "data/pilot/f1_v1_candidate/bindings.json",
  "required_reads": [
    "docs/MACHINE_READABLE_ACCOUNTING_SCHEMA.md",
    "docs/VALIDATION_POLICY.md",
    "docs/GITHUB_AND_CI_POLICY.md",
    "docs/ARTIFACT_AND_PROVENANCE_RULES.md",
    "data/pilot/f1_v1_candidate/bindings.json",
    "tools/validate_machine_accounting_schema_v1_candidate.py",
    ".github/workflows/machine-accounting-schema-v1-candidate.yml"
  ],
  "forbidden_scope_expansion": [
    "FULL_MIGRATION",
    "797_RESIDUAL_ANALYSIS",
    "BUILDER_IPS_RUNTIME",
    "GAME_FILE_MODIFICATION"
  ]
}
PROJECT_RESUME_V2 -->

## Current repository state

Repository: `fsmkh1-crypto/Taiko5DX-Switch-Korean-Port`  
Branch: `main`

Documentation Governance v2: **COMPLETE** after V101.  
V094 transport repair v2: **COMPLETE** after V102.  
Structured atomic-claim cause family: **COMPLETE** after V103.  
Source-anchor/provenance cause family: **COMPLETE** after V104.  
Schema-v1 validation-pipeline cause family: **COMPLETE** after V105.  
Pre-freeze governance cleanup: **COMPLETE** after V106.  
Pre-freeze semantic-hash pinning: **COMPLETE after corrected V107 forward recovery**.  
Ruleset rebase: **COMPLETE**.  
Repository write mode: **GIT_OBJECT_ONLY_WRITE_MODE**.  
Authority-freshness/change-detection cleanup: **COMPLETE**.  
Schema v1: **CANDIDATE / NOT FROZEN**.  
Candidate machine-accounting state: **PASS / FOUR SEMANTIC HASHES PINNED / NOT FROZEN**.

Canonical target:

- Title ID `0100346017304000`
- Switch v1.1.3
- Build ID `D9120950C258610A746F4A31CE3A3B376DE393D9`
- canonical game `main` SHA-256 `b366e692208f3c0cc18bc1884ef95689b6b11d722fa2d749b8500abccbc3109b`

## Canonical completed work

- Stage 1 canonical inventory: COMPLETE
- Stage 2 affine structural targeting: COMPLETE
- F1 unique-anchor bounded localization sequence audit: COMPLETE
- F1 historical V094 static-write authorization: COMPLETE as semantic/provenance evidence
- V094 machine-consumable repository transport: COMPLETE as deterministic plain JSONL shards
- machine-readable accounting v0.1 F1 pilot: PASS
- schema-v1 candidate regression: PASS; four materialized semantic hashes pinned and verified after corrected V107 recovery
- schema-v1 validation pipeline: consolidated and verified after V105; release fail-fast and collect-all share one current validator path
- pre-freeze governance cleanup: V106 closes ambiguous transport hash naming, orphan operating authority, write-scope read-chain enforcement, external remote-I/O telemetry design, candidate PASS/FROZEN language, generated-roundtrip trust, and anchor-workflow change detection
- pre-freeze semantic hash pinning: the initial V107 attempt reused the V104 historical `effective_claims` hash; forward recovery `ed0e4f2ffe8f9e1c646b96078a5c37ca57f8afea` corrected that pin to the V105+ current materialization hash and passed current release plus collect-all validation
- repository-writing stages: `GIT_OBJECT_ONLY_WRITE_MODE` is the default; allowed remote write actions are exactly `create_blob`, `create_tree`, `create_commit`, and `update_ref(main, force=false)` unless a fresh explicit scope authorizes another route
- current machine-accounting authority documents: mechanically bound to actual repository artifacts/implementation by document-governance checks
- generated artifacts remain derived views and are not candidate gate authority
- source-anchor gate registry documentation: synchronized with all six source-anchor gate families

Current accounting facts remain:

```text
historical mixed-granularity inventory records  27,430
leaf-obligation records after descriptor groups 27,419
inline rows                                      17,103
Stage-1 raw exceptions                           11,050
Stage-2 residual                                  1,248
conservative later target-resolved                  451
conservative target-unresolved residual              797
```

F1 population remains:

```text
DIRECT_PORT authorized                    158
PADDING_RECONSTRUCTION_REQUIRED            75
SHARED_OWNER_BINDING_REQUIRED              25
TERMINATOR_CAPACITY_FAIL                    4
F1_RULE_REJECTED                           16
TOTAL                                     278
```

The 25 shared-owner rows remain `SHARED_OWNER_BINDING`; replacement conflict is not proven.

## V094 semantic and transport state

Semantic identity is unchanged:

```text
rows                    158
logical content SHA-256 c612bcf55d0c139d55dee42a6a6397f702ead0f1628b47b45c46512fd1b52bff
ordered source IDs SHA  87d5a7531b5e2b3841fe4ba093a87dd9da11e8c85b5d4184c6ae705436c1833e
```

Historical gzip provenance remains `8bbbeb03695b4bd06f028b9c9cfe0d367af170a012af56803f3a8553356a0b68`.

Current repository transport:

```text
path       docs/manifests/F1_STATIC_WRITE_AUTHORIZATION_MANIFEST/
format     PLAIN_JSONL_SHARDS
shards     20
rows       158
INDEX SHA  ce241ab9a3257e0cf858d4b016eebdcd3c564958e95cdaf23035c0f4dfdfd6d4
repair     d25fd5be5c15aabd1483c0e8bf0ad4873974bb1b
```

The 20-shard layout is historical transport provenance, **not** a future sharding precedent or safe-size threshold.

`docs/manifests/F1_STATIC_WRITE_AUTHORIZATION_SUMMARY.json` is a historical/reporting view, not canonical action authority. Current action transport identity and historical gzip provenance are explicitly separated.

## V103 atomic-claim closure

Commit:

`9df784890b9f21f79187ed67825919fedf4d77f7` — `fix: close structured atomic-claim classification gaps`

Effective claim accounting:

```text
base claims                 42
new appended claims         55
effective claims            97
ACTIVE claims               87
candidate migration entries 752
```

The current structured-atomic exception registry is `data/pilot/f1_v1_candidate/claim_amendments.json` and contains 10 reviewed entries. `V089.C03` remains one explicit exhaustive structured partition (`197 + 81 = 278`). `V094.C04` is SUPERSEDED and replaced by `V094.C23`, `V094.C24`, and `V094.C25`.

## V104 source-anchor/provenance closure

Fix commit:

`cb21ce200a89457b77072b56f2f48a5d43d1bac0` — `fix: close source-anchor provenance gaps`

Seven weak/malformed source locators are corrected through candidate overlay metadata without modifying immutable v0.1 claim rows or anchor-protected canonical evidence:

```text
V088.C06
V088.C07
V089.C01
V089.C03
V091.C02
V091.C05
V092.C04
```

All bind to canonical `docs/F1_LOCALIZATION_SEQUENCE_AUDIT.md` blob:

`ba9c660cf6f229ec2b19f024b9bc2cef94d26a44`

The current candidate validator exposes six source-anchor gate families:

1. `anchor_present_` — source-anchor object exists;
2. `anchor_document_` — bound document path exists;
3. `anchor_blob_` — bound document Git blob identity matches;
4. `anchor_text_hash_` — anchor-text SHA-256 matches;
5. `anchor_heading_` — Markdown `heading_path` resolves uniquely;
6. `anchor_text_in_heading_` — anchor occurs inside the resolved heading section.

V104 historically observed these candidate outputs:

```text
source_state         91a54c8760f84f0e5b48e25dfda8adb9ae16ff32a83a4af86275fbc0c762322c
actions              a7c0f3ce3423b2a07797ef18e538c963140303751621a985dc6fe76c52bb8a4f
source_action_edges  1399fa309889399854d68f5d89f202df0f22f7be58ec2c85e3a02342987a4fe7
effective_claims     2cb8459c95ec53e0f61fd72dd80de45148a1091b637bebaa50ef4d3607c50676
```

The first three remain current. The V104 `effective_claims` value is retained as historical provenance only: V105 consolidated the current validator so `source_anchor_overrides` are applied to fully materialized effective claims before semantic hashing. Under the current V105+ materialization semantics, the effective-claims hash is `c29751ecca3233516fd9effc850e6e961d4418e3784266175df2af59798b6d35`.

## V105 schema-v1 validation-pipeline closure

Implementation commit:

`3d7e640af4528b674229dddb707eea2a89b8c952` — `fix: recover noop history and consolidate schema validation pipeline`

Canonical tree:

`baa95192cdc3401a0c7cda63c9b336b467b789ba`

The candidate pipeline has two explicit roles:

- release validation remains fail-fast;
- non-release diagnostics run current machine gates in collect-all mode without replaying historical technical byte analysis.

Automatic GitHub Actions run `34685595581` (`push`, attempt 1) completed successfully for head `3d7e640af4528b674229dddb707eea2a89b8c952`.

Two accidental commits remain in main history as provenance and were corrected by forward recovery; no force-push or history rewrite occurred:

- `8665bb191d81853400cb93c437fcabbb300d2b68` — accidental `noop`, introduced empty `NONEXISTENT` in its tree;
- `5de2805df71090e879a979b044f2bda4d43e0afb` — second `noop`, tree-wise no-op relative to its parent.

They do not change current technical conclusions.

## V106 pre-freeze governance cleanup

Implementation commit:

`50d41c1e036fa336d7605cfd0ae7f317e1b1422b` — `fix: close pre-freeze governance audit gaps`

V106 changes governance and machine-gate plumbing only. It does not change historical F1 technical facts or populate any semantic pin.

### Transport identity

- candidate binding uses explicit `current_transport_index_sha256` rather than a generic file-hash alias;
- current INDEX, semantic logical-content SHA, and historical gzip provenance remain separate identities;
- `action_canonical_gzip_hash` is renamed to `action_current_transport_index_hash`;
- the historical SUMMARY and its regeneration path use explicit reporting/transport semantics and cannot silently recreate the ambiguous generic field.

### Read chain and authority

- `PROJECT_RESUME_V2.scope_kind` is explicit;
- a `REPOSITORY_WRITE` scope must include `docs/GITHUB_AND_CI_POLICY.md` in `required_reads` or documentation governance fails;
- `docs/PROJECT_OPERATING_RULES.md` is retained only as a consolidated reference, not a current orphan authority;
- remote-I/O metrics are non-authoritative external telemetry at the location declared in `remote_io_metrics_location`, avoiding a second Git mutation after final CI values become known.

### Roundtrip root cause

The candidate validator no longer trusts `generated/pilot/f1/roundtrip_result.json`. It reconstructs the source document directly from canonical coverage and verifies block order, gap-free line coverage from line 1, bounds, every block SHA, document blob/SHA, EOF coverage, exact rebuilt bytes, and `UNEXPLAINED=0`.

The 61 canonical coverage blocks span the complete 187-line F1 audit. The machine-accounting workflow now triggers on the three canonical source-anchor evidence documents used by current gates. `generated/**` is intentionally not added to that workflow because generated roundtrip status is not authority.

## V107 pre-freeze semantic hash pinning — corrected closure

Initial implementation commit:

`1a4e2e39d5ce179724d32f465ee6ee2ecfef9dbb` — `chore: pin schema-v1 candidate semantic hashes`

The first V107 attempt pinned the four hashes as observed by V104. That was correct historical provenance for V104, but it was stale for one current semantic identity after V105 consolidated the validator path. Specifically, V105+ applies `source_anchor_overrides` to the effective claims before `semantic_rows_hash(ctx["claims"])`. Therefore the current effective-claims semantic identity is `c29751ecca3233516fd9effc850e6e961d4418e3784266175df2af59798b6d35`, not the historical V104 value `2cb8459c...`.

The first final-current validation correctly rejected the stale pin. No source/action/edge membership, claim count, transport identity, or historical F1 technical conclusion changed.

During recovery, accidental commit `92c924aaa971a748349a2b9c9946f58cd7b9d6cc` (`x`) added a root `DUMMY` file through a forbidden Contents-API write. History was not rewritten. Forward recovery commit:

`ed0e4f2ffe8f9e1c646b96078a5c37ca57f8afea` — `fix: recover V107 pin after accidental write`

uses the intended pre-accident tree as its base, removes `DUMMY` from canonical main state, and binds the current effective-claims semantic hash. The current four pins are:

```text
source_state         91a54c8760f84f0e5b48e25dfda8adb9ae16ff32a83a4af86275fbc0c762322c
actions              a7c0f3ce3423b2a07797ef18e538c963140303751621a985dc6fe76c52bb8a4f
source_action_edges  1399fa309889399854d68f5d89f202df0f22f7be58ec2c85e3a02342987a4fe7
effective_claims     c29751ecca3233516fd9effc850e6e961d4418e3784266175df2af59798b6d35
```

Automatic GitHub Actions run `34691523117` on recovery head `ed0e4f2f...` completed successfully. Its `validate` job passed both `Release fail-fast validation` and `Collect-all machine-gate diagnostic`. Document-governance run `34691523090` also completed successfully.

An accidentally created branch named `__INVALID_DO_NOT_CREATE__` still points to the old accidental commit `92c924aa...`. It is **non-authoritative**, is not referenced by `main`, and does not affect project state. The current repository write allowlist does not permit branch deletion, so it is retained as an external/noncanonical artifact rather than removed through an unauthorized write route. Several additional dangling commit objects created while preparing recovery are likewise non-authoritative and are not project state.

V107 is therefore **PASS / NOT FROZEN** after forward recovery. No schema freeze, 797 residual analysis, builder, IPS, runtime, mapping, or game-file work was performed.

## Authority freshness and change detection

Current authority is protected by mechanical checks rather than generation labels alone:

- `MACHINE_READABLE_ACCOUNTING_SCHEMA.md` declares a machine-readable fact block bound to the actual V094 `INDEX.json` and action binding;
- `CLAIM_EXTRACTION_RULES.md` declares a machine-readable fact block bound to the actual structured-exception registry and all six source-anchor gate families exposed by the validator implementation;
- document governance checks those current-authority facts against repository artifacts/implementation;
- document governance verifies `last_closed_validation_id` against the schema-v1 amendment ledger and verifies `last_closed_stage_commit` is an ancestor of current HEAD;
- document governance enforces `scope_kind` and the write-scope GitHub-policy required-read invariant;
- `generated/` artifacts cannot become `PROJECT_STATE.required_reads` or current document authority, and generated JSON carrying next-stage/resume authority keys is rejected;
- machine-accounting roundtrip is recalculated from canonical source coverage, not generated status;
- machine-accounting workflow triggers include the canonical evidence documents consumed by source-anchor gates.

Anchor-protected evidence remains unchanged by corrected V107 recovery.

## Repository write mode

All repository-writing stages default to `GIT_OBJECT_ONLY_WRITE_MODE`.

Before the first remote write, freeze the base HEAD/tree, changed paths, deleted paths, no-op decisions, expected blob/tree/commit/ref counts, and CI expectation. After the first remote write, do not rediscover write schemas or switch routes unless a previously loaded tool schema is genuinely unavailable in the active tool context.

Permitted remote write actions are exactly:

```text
create_blob
create_tree
create_commit
update_ref(main, force=false)
```

Any invocation of another remote write action is a stage failure even if it produces no canonical mutation. STOP and require a fresh explicit signal. Repository deletions are expressed through the intended tree rather than Contents-API deletion.

This is an operator-enforced mode, not a connector-level capability sandbox; other tools may remain visible but must not be used.

## Current boundaries

- schema v1 remains NOT FROZEN;
- all four current materialized semantic hashes are pinned in the candidate bindings;
- candidate `PASS` means current candidate gates pass and all four required semantic pins match; it still does not mean schema freeze;
- `FROZEN` requires a separate explicitly authorized schema-freeze declaration;
- `COLLECT_ALL` means current machine-gate evaluation, not replay of historical technical analysis;
- PC patch remains semantic authority for equivalent functionality;
- raw uniqueness is not a safety rule;
- target resolution is not write authorization;
- no silent UNKNOWN authorization or source omission;
- no force-push;
- no synthesis of canonical rows from counts/IDs/edges;
- no governance edit to anchor-protected evidence without explicit anchor migration;
- do not reopen V094, V103, V104, V105, V106, or corrected V107 without a legitimate revalidation trigger.

## Next authorized scope after a fresh signal

**`SCHEMA_FREEZE_DECLARATION`**

A fresh explicit user signal is required before any schema-freeze declaration or authority transition. Candidate `PASS` is a prerequisite, not permission to freeze automatically.

That future stage must remain separate from full migration, the 797 residual, builder, IPS, runtime, mapping, and game-file work.
