# PROJECT_STATE

Last updated: 2026-09-12 (KST)

This file is the **sole project-resume authority**. Historical documents may contain valid evidence and old “next step” language, but they do not override this file.

<!-- PROJECT_RESUME_V2
{
  "schema": "PROJECT_RESUME_V2",
  "scope_id": "AUTHORITY_FRESHNESS_AND_CHANGE_DETECTION",
  "status": "STOPPED_AWAITING_USER_SIGNAL",
  "last_closed_validation_id": "V105",
  "last_closed_stage_commit": "3d7e640af4528b674229dddb707eea2a89b8c952",
  "last_closed_ci_run_id": 34685595581,
  "last_closed_ci_conclusion": "success",
  "ruleset_rebase_status": "COMPLETE",
  "ruleset_rebase_base_commit": "d272bb1a8feef2a53144c5a04489b4b080d0179f",
  "required_reads": [
    "docs/MACHINE_READABLE_ACCOUNTING_SCHEMA.md",
    "docs/CLAIM_EXTRACTION_RULES.md",
    "docs/DOCUMENT_AUTHORITY_INDEX.json",
    "tools/validate_document_governance.py",
    ".github/workflows/document-governance.yml",
    ".github/workflows/machine-accounting-schema-v1-candidate.yml",
    "data/pilot/f1_v1_candidate/bindings.json",
    "generated/pilot/f1_v1_candidate/validation_status.json"
  ],
  "forbidden_scope_expansion": [
    "SEMANTIC_HASH_PINNING",
    "SCHEMA_FREEZE_DECLARATION",
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
Ruleset rebase: **COMPLETE** after the current policy-only stage.  
Schema v1: **CANDIDATE / NOT FROZEN**.  
Candidate regression status: **PREPIN_PASS**.

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
- schema-v1 candidate regression: PREPIN_PASS after V104; semantic hashes observed but not pinned
- schema-v1 validation pipeline: consolidated and verified after V105; release fail-fast and collect-all machine-gate diagnostic both PASS

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

`V089.C03` remains one explicit exhaustive structured partition (`197 + 81 = 278`). `V094.C04` is SUPERSEDED and replaced by `V094.C23`, `V094.C24`, and `V094.C25`.

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

The candidate validator checks all 97 effective claims for bound document Git blob identity, anchor-text SHA-256, unique Markdown `heading_path` resolution, and anchor occurrence inside the claimed heading section.

GitHub Actions run `34680748843` completed successfully with `PREPIN_PASS`.

Observed materialized semantic hashes remain:

```text
source_state         91a54c8760f84f0e5b48e25dfda8adb9ae16ff32a83a4af86275fbc0c762322c
actions              a7c0f3ce3423b2a07797ef18e538c963140303751621a985dc6fe76c52bb8a4f
source_action_edges  1399fa309889399854d68f5d89f202df0f22f7be58ec2c85e3a02342987a4fe7
effective_claims     2cb8459c95ec53e0f61fd72dd80de45148a1091b637bebaa50ef4d3607c50676
```

These hashes are not pinned and do not authorize schema freeze.

## V105 schema-v1 validation-pipeline closure

Implementation commit:

`3d7e640af4528b674229dddb707eea2a89b8c952` — `fix: recover noop history and consolidate schema validation pipeline`

Canonical tree:

`baa95192cdc3401a0c7cda63c9b336b467b789ba`

The current candidate pipeline now has two explicit roles:

- release validation remains fail-fast;
- non-release diagnostics run the current machine gates in collect-all mode without replaying historical technical byte analysis.

The former compatibility behavior is consolidated into the canonical candidate validation path. The collect-all entry point delegates to the same validator semantics rather than maintaining a second patched truth path.

Automatic GitHub Actions run `34685595581` (`push`, attempt 1) completed successfully for head `3d7e640af4528b674229dddb707eea2a89b8c952`. The `validate` job passed all four relevant steps:

1. Compile validators
2. Diagnose bound V094 transport
3. Release fail-fast validation
4. Collect-all machine-gate diagnostic

No manual rerun or second CI validation was used.

Two accidental commits remain in main history as provenance and were corrected by the forward recovery commit; no force-push or history rewrite occurred:

- `8665bb191d81853400cb93c437fcabbb300d2b68` — accidental `noop`, introduced empty `NONEXISTENT` in its tree;
- `5de2805df71090e879a979b044f2bda4d43e0afb` — second `noop`, tree-wise no-op relative to its parent.

The final V105 tree removes the accidental file and contains the intended validation-pipeline files. These historical commits do not change current technical conclusions.

V105 does **not** pin the four semantic hashes and does **not** freeze schema v1.

## Current boundaries

- schema v1 remains NOT FROZEN;
- materialized semantic hashes remain unpinned;
- `PREPIN_PASS` means no known current machine-gate blocker under the present candidate inputs/validator definition, not permanent proof against later evidence or rule changes;
- PC patch remains semantic authority;
- raw uniqueness is not a safety rule;
- target resolution is not write authorization;
- no silent UNKNOWN authorization or source omission;
- no force-push;
- no synthesis of canonical rows from counts/IDs/edges;
- no governance edit to anchor-protected evidence without explicit anchor migration;
- do not reopen V094, V103, V104, or V105 without a legitimate revalidation trigger.

## Ruleset rebase

The operating policies now define, without changing any technical fact:

- verified-fact reuse and dependency-scoped revalidation;
- `COLLECT_ALL` as current machine-gate evaluation rather than historical technical replay;
- `REMOTE_IO_FAST_PATH` as the default repository execution path;
- semantic identity as separate from transport identity;
- structured JSON/JSONL machine-state direction, with generated current views separated from canonical evidence/authority.

This policy stage does not pin hashes, freeze the schema, migrate the full corpus, modify machine-accounting artifacts, or change game data.

## Next authorized scope after a fresh signal

**Close authority freshness and change-detection gaps only (`AUTHORITY_FRESHNESS_AND_CHANGE_DETECTION`).**

That stage may synchronize the current machine-accounting authority documents with already-canonical machine artifacts and add mechanical checks that prevent the same drift from recurring. It may also close workflow trigger gaps required for those checks and remove stale generated status authority.

Do not combine that stage with semantic-hash pinning, schema freeze, full migration, the 797 residual, builder, IPS, runtime, mapping, or game-file work.
