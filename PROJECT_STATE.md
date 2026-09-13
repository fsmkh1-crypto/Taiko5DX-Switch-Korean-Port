# PROJECT_STATE

Last updated: 2026-09-13 (KST)

This file is the sole project-resume authority. Historical documents and ledgers preserve provenance but do not override this file.

<!-- PROJECT_RESUME_V2
{
  "schema": "PROJECT_RESUME_V2",
  "scope_id": "PORTABILITY_MATRIX_ACTION_LEDGER_DESIGN_MATERIALIZED",
  "scope_kind": "READ_ONLY_DESIGN",
  "status": "STOPPED_AWAITING_USER_SIGNAL",
  "last_closed_validation_id": "V158",
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
  "portability_action_ledger_design": "docs/PORTABILITY_MATRIX_AND_ACTION_LEDGER_DESIGN.md",
  "required_reads": [
    "data/pilot/f1_v1_candidate/schema_freeze_declaration.json",
    "data/pilot/f1_v1_candidate/bindings.json",
    "docs/MASTER_RULE_REGISTRY.md",
    "data/post_freeze/master_rule_registry_v1/INDEX.json",
    "docs/VALIDATION_LEDGER_MASTER_RULE_REGISTRY.txt",
    "docs/PORTABILITY_MATRIX_AND_ACTION_LEDGER_DESIGN.md",
    "docs/VALIDATION_LEDGER_PORTABILITY_ACTION_LEDGER_DESIGN.txt",
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
- FZ001 post-freeze rule compatibility audit: COMPLETE / NO SCHEMA REDESIGN REQUIRED
- Portability Matrix / Action Ledger design: COMPLETE / MATERIALIZED
- central validation index: CURRENT THROUGH V158
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

FZ001 is an immutable historical baseline. Later canonical overlays do not mutate these hashes; they refine current effective state only on the exact membership/axis proven by each overlay.

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

F1 write-safety authority remains unchanged:

```text
DIRECT_PORT static-write-authorized 158
PADDING_RECONSTRUCTION_REQUIRED      75
SHARED_OWNER_BINDING_REQUIRED        25
TERMINATOR_CAPACITY_FAIL              4
F1_RULE_REJECTED                     16
TOTAL                               278
```

The labels above preserve the historical F1 authorization partition. The 158 authorized rows are not implemented merely because they are authorized. No other F1 population is silently promoted.

### 4.1 Current effective F1 target-resolution overlay

The frozen FZ001 snapshot recorded 262 target-resolved and 16 F1-rule-rejected/analyzed-unresolved rows. Post-freeze target/counterpart evidence later resolved all 16 without changing their write authorization:

- 14 rows: deterministic Oracle V1 `ORACLE_RESOLVED`;
- `R3181`, `R3182`: Assisted follow-up `TARGET_RESOLVED`.

Current effective target-resolution accounting is therefore:

```text
F1 source population                278
current effective target resolved   278
static-write authorized             158
write/action closure still open     120
```

This is a target-resolution overlay only. It does not alter the FZ001 frozen hashes, the F1 historical partition, or the 158-row write-authorization boundary.

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

## 6. Portability / Action Ledger design authority

Current design contract:
- `docs/PORTABILITY_MATRIX_AND_ACTION_LEDGER_DESIGN.md`
- validation: `docs/VALIDATION_LEDGER_PORTABILITY_ACTION_LEDGER_DESIGN.txt`

Fixed design decisions:

- PC Korean semantic result remains the default Oracle.
- current planning input is the effective source-state view: frozen baseline + exact later canonical overlays, composed field-by-field within proven scope.
- portability P1-P4 and terminal disposition are independent axes.
- `NATIVE_EQUIVALENT_VERIFIED` has no forced portability class.
- `SUBSUMED` has no independent portability class and must reference a final non-SUBSUMED action.
- `PROVEN_IRRELEVANT` is the normal P4 terminal and requires verified exclusion evidence.
- Portability Matrix is a derived planning view; no new mandatory FZ001 semantic field is created.
- existing source/action/edge/claim schema is sufficient for this planning stage.
- capacity/storage blockers do not authorize automatic translation changes.
- future builder must be a semantic-free, fail-closed executor of a fully resolved Action Ledger.

## 7. Master rule authority

Central rule-discovery/precedence overlay:
- `docs/MASTER_RULE_REGISTRY.md`
- `data/post_freeze/master_rule_registry_v1/INDEX.json`
- `data/post_freeze/master_rule_registry_v1/RULES.json`
- validation: `docs/VALIDATION_LEDGER_MASTER_RULE_REGISTRY.txt`

Source canonical documents remain the technical evidence authority. The registry remains an overlay only and does not mutate FZ001.

## 8. Validation and governance

- `docs/VALIDATION_LEDGER.md` is the central validation index through V158 and also indexes post-freeze namespaced ledgers.
- existing document-governance and machine-accounting validation through V107 remain provenance; this design materialization does not alter FZ001 semantic pins.
- later narrow canonical corrections/overlays take precedence only within their proven scope.
- target/counterpart closure never implies write authorization.

## 9. Repository operating boundary

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

## 10. Current STOP boundary

Status: `STOPPED_AWAITING_USER_SIGNAL`.

Do not begin builder/IPS/runtime implementation, game-file modification, schema redesign, or diagnostic build without a fresh explicit user execution signal.

Next recommended scope: **`PORTABILITY_MATRIX_ACTION_LEDGER_POPULATION_READ_ONLY`**.

That scope may materialize a read-only current effective source-state input view, Portability Matrix proposal, Action Ledger proposal, and unresolved/conflict/write-safety queues. It must not implement the builder/runtime, emit IPS, or modify game files.
