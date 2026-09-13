# PROJECT_STATE

Last updated: 2026-09-13 (KST)

This file is the sole project-resume authority. Historical documents and ledgers preserve provenance but do not override this file.

<!-- PROJECT_RESUME_V2
{
  "schema": "PROJECT_RESUME_V2",
  "scope_id": "MASTER_RULE_REGISTRY_MATERIALIZED",
  "scope_kind": "READ_ONLY",
  "status": "STOPPED_AWAITING_USER_SIGNAL",
  "last_closed_validation_id": "V151",
  "last_closed_stage_commit": "813441d170929717b4f4ea75a515b4a1fc3086e9",
  "last_closed_ci_run_id": 34691523117,
  "last_closed_ci_validation_id": "V107",
  "last_closed_ci_conclusion": "success",
  "repository_write_mode": "GIT_OBJECT_ONLY_WRITE_MODE",
  "repository_write_allowed_actions": [
    "create_blob",
    "create_tree",
    "create_commit",
    "update_ref"
  ],
  "schema_freeze_status": "FROZEN_FZ001",
  "schema_freeze_declaration_id": "FZ001",
  "schema_freeze_declaration": "data/pilot/f1_v1_candidate/schema_freeze_declaration.json",
  "schema_freeze_declaration_git_blob_sha": "6c726b7d004753e2f49f63640bd4f6df343dd736",
  "schema_freeze_basis_validation_id": "V107",
  "schema_freeze_basis_ci_run_id": 34691523117,
  "schema_freeze_basis_head": "ed0e4f2ffe8f9e1c646b96078a5c37ca57f8afea",
  "machine_fact_binding": "data/pilot/f1_v1_candidate/bindings.json",
  "master_rule_registry": "docs/MASTER_RULE_REGISTRY.md",
  "master_rule_registry_index": "data/post_freeze/master_rule_registry_v1/INDEX.json",
  "required_reads": [
    "data/pilot/f1_v1_candidate/schema_freeze_declaration.json",
    "data/pilot/f1_v1_candidate/bindings.json",
    "docs/MASTER_RULE_REGISTRY.md",
    "data/post_freeze/master_rule_registry_v1/INDEX.json",
    "docs/VALIDATION_LEDGER_MASTER_RULE_REGISTRY.txt",
    "docs/MACHINE_READABLE_ACCOUNTING_SCHEMA.md",
    "docs/CLAIM_EXTRACTION_RULES.md",
    "docs/VALIDATION_POLICY.md",
    "docs/GITHUB_AND_CI_POLICY.md",
    "docs/INLINE_VALIDATION_POLICY.md",
    "docs/PC_TO_SWITCH_PORTING_RULE_FRAMEWORK.md",
    "docs/PC_TO_SWITCH_ACCOUNTING_INVARIANTS.md",
    "docs/F1_STATIC_WRITE_AUTHORIZATION.md",
    "docs/PC_PATCH_ORACLE_TRACE_19_CLOSURE.md",
    "data/post_freeze/pc_patch_oracle_trace_19_closure_v1/INDEX.json"
  ],
  "forbidden_scope_expansion": [
    "FULL_MIGRATION",
    "BUILDER_IPS_RUNTIME",
    "GAME_FILE_MODIFICATION",
    "SCHEMA_REDESIGN"
  ]
}
PROJECT_RESUME_V2 -->

## 1. Current state

Repository: `fsmkh1-crypto/Taiko5DX-Switch-Korean-Port`  
Branch: `main`

Completed and inherited without revalidation:
- Stage 1 canonical inventory: COMPLETE
- Stage 2 affine structural targeting: COMPLETE
- F1 localization-sequence audit: COMPLETE
- schema v1 freeze: FROZEN — FZ001
- PC DLL/runtime reference analysis: COMPLETE
- CAP64 correction and stable forward-986 structural synthesis: COMPLETE
- PC Patch Oracle V1 and assisted/Astra follow-ups: COMPLETE
- TRACE 19 cause-group closure: COMPLETE / MATERIALIZED
- master rule integration audit and registry materialization: COMPLETE
- central document authority and validation indexes: CURRENT THROUGH V151
- unresolved counterpart-routing queue: 0
- TRACE remainder: 0

No builder, IPS, runtime, or game-file implementation is authorized by this state.

## 2. Frozen semantic identities

FZ001 remains unchanged:

```text
source_state         91a54c8760f84f0e5b48e25dfda8adb9ae16ff32a83a4af86275fbc0c762322c
actions              a7c0f3ce3423b2a07797ef18e538c963140303751621a985dc6fe76c52bb8a4f
source_action_edges  1399fa309889399854d68f5d89f202df0f22f7be58ec2c85e3a02342987a4fe7
effective_claims     c29751ecca3233516fd9effc850e6e961d4418e3784266175df2af59798b6d35
```

The master rule registry is an overlay only. It does not mutate FZ001 or its frozen bindings.

## 3. Canonical target and population

Target:
- Title ID `0100346017304000`
- Switch v1.1.3
- Build ID `D9120950C258610A746F4A31CE3A3B376DE393D9`
- Switch `main` SHA-256 `b366e692208f3c0cc18bc1884ef95689b6b11d722fa2d749b8500abccbc3109b`

Stable source accounting:

```text
inline rows                         17,103
Stage-1 raw exceptions              11,050
Stage-2 residual                     1,248
F1 accepted excluded                   262
forward-analysis population            986
```

## 4. F1 write-safety authority

F1 remains unchanged:

```text
DIRECT_PORT static-write-authorized 158
PADDING_RECONSTRUCTION_REQUIRED      75
SHARED_OWNER_BINDING_REQUIRED        25
TERMINATOR_CAPACITY_FAIL              4
F1_RULE_REJECTED                     16
TOTAL                               278
```

The 158 authorized rows are not implemented merely because they are authorized. No other F1 population is silently promoted.

## 5. Effective forward-986 routing closure

Current consolidated counterpart/routing classes:

```text
base deterministic Oracle resolved      656
target resolved                           73
composite/formatter resolved             242
rerouted                                  15
trace                                      0
TOTAL                                    986
```

Remainders:
- ORACLE_ASSISTED: 0
- ASTRA_REQUIRED: 0
- TRACE: 0

This is counterpart/routing closure only. It creates no new `WRITE_SAFE` authorization.

## 6. Master rule authority

Central rule-discovery/precedence overlay:
- `docs/MASTER_RULE_REGISTRY.md`
- `data/post_freeze/master_rule_registry_v1/INDEX.json`
- `data/post_freeze/master_rule_registry_v1/RULES.json`
- validation: `docs/VALIDATION_LEDGER_MASTER_RULE_REGISTRY.txt`

The registry contains 78 operative, boundary, promoted, rejected, or superseded rules covering:
- operating/governance
- authority/provenance
- accounting schema
- PC runtime reference
- structural targeting
- write safety
- semantic Oracle rules
- reroute/subsume rules
- rejected/superseded shortcuts

Source canonical documents remain the technical evidence authority. The registry exists to make current rules, precedence, and negative knowledge discoverable without rewriting historical evidence.

## 7. Validation and governance

- `docs/VALIDATION_LEDGER.md` is the central validation index through V151 and also indexes post-freeze namespaced ledgers.
- `docs/DOCUMENT_AUTHORITY_INDEX.json` covers current Markdown authority through 2026-09-13.
- document-governance validation now checks the current central validation closure and the master registry identity/coverage boundary.
- the most recent previously recorded successful machine-accounting CI remains V107; later documentation/governance CI does not alter FZ001 semantic pins.

## 8. Repository operating boundary

Permitted remote write actions remain exactly:

```text
create_blob
create_tree
create_commit
update_ref(main, force=false)
```

Forbidden:
- `update_file`
- `create_file`
- `delete_file`
- `create_branch`
- force push
- history rewrite

## 9. Current STOP boundary

Status: `STOPPED_AWAITING_USER_SIGNAL`.

Do not begin write-safety/action-ledger planning, builder/IPS/runtime implementation, game-file modification, or schema redesign without a fresh explicit user execution signal.

Next recommended scope: **write-safety and action-ledger planning for the already resolved/rerouted obligations**, still separated from implementation.
