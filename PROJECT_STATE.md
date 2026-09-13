# PROJECT_STATE

Last updated: 2026-09-13 (KST)

This file is the sole project-resume authority. Historical documents and ledgers preserve provenance but do not override this file.

<!-- PROJECT_RESUME_V2
{
  "schema": "PROJECT_RESUME_V2",
  "scope_id": "GAP_INTERNAL_24_EDGE_PROVENANCE_RECOVERY_MATERIALIZED",
  "scope_kind": "READ_ONLY_GAP_INTERNAL_24_EDGE_PROVENANCE_RECOVERY",
  "status": "STOPPED_AWAITING_USER_SIGNAL",
  "last_closed_validation_id": "V201",
  "last_closed_stage_commit": "9eeff6fbc819a868e065d08b26fea3e7816b2604",
  "last_closed_ci_run_id": 34691523117,
  "last_closed_ci_validation_id": "V107",
  "last_closed_ci_conclusion": "success",
  "repository_write_mode": "GIT_OBJECT_ONLY_WRITE_MODE",
  "repository_write_allowed_actions": ["create_blob","create_tree","create_commit","update_ref"],
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
  "inline_full_corpus_coverage_overlay": "docs/INLINE_FULL_CORPUS_COVERAGE_OVERLAY.md",
  "inline_full_corpus_coverage_index": "data/post_freeze/inline_full_corpus_coverage_overlay_v1/INDEX.json",
  "inline_full_corpus_semantic_owner_overlay": "docs/INLINE_FULL_CORPUS_SEMANTIC_OWNER_OVERLAY.md",
  "inline_full_corpus_semantic_owner_index": "data/post_freeze/inline_full_corpus_semantic_owner_overlay_v1/INDEX.json",
  "inline_full_corpus_action_collapse_overlay": "docs/INLINE_FULL_CORPUS_ACTION_COLLAPSE_OVERLAY.md",
  "inline_full_corpus_action_collapse_index": "data/post_freeze/inline_full_corpus_action_collapse_overlay_v1/INDEX.json",
  "inline_gap_internal_24_edge_recovery": "docs/INLINE_GAP_INTERNAL_24_EDGE_PROVENANCE_RECOVERY.md",
  "inline_gap_internal_24_edge_recovery_index": "data/post_freeze/inline_gap_internal_24_edge_provenance_recovery_v1/INDEX.json",
  "inline_f1_cross_boundary_action_collapse": "docs/INLINE_F1_CROSS_BOUNDARY_ACTION_COLLAPSE_CLOSURE.md",
  "inline_f1_cross_boundary_action_collapse_index": "data/post_freeze/inline_f1_cross_boundary_action_collapse_v1/INDEX.json",
  "inline_pre_stage2_to_stage2_cross_boundary_adjudication": "docs/INLINE_PRE_STAGE2_TO_STAGE2_CROSS_BOUNDARY_ADJUDICATION_CLOSURE.md",
  "inline_pre_stage2_to_stage2_cross_boundary_adjudication_index": "data/post_freeze/inline_pre_stage2_to_stage2_cross_boundary_adjudication_v1/INDEX.json",
  "required_reads": [
    "data/pilot/f1_v1_candidate/schema_freeze_declaration.json",
    "data/pilot/f1_v1_candidate/bindings.json",
    "docs/MASTER_RULE_REGISTRY.md",
    "data/post_freeze/master_rule_registry_v1/INDEX.json",
    "docs/PORTABILITY_MATRIX_AND_ACTION_LEDGER_DESIGN.md",
    "docs/INLINE_FULL_CORPUS_COVERAGE_OVERLAY.md",
    "data/post_freeze/inline_full_corpus_coverage_overlay_v1/INDEX.json",
    "docs/INLINE_FULL_CORPUS_SEMANTIC_OWNER_OVERLAY.md",
    "data/post_freeze/inline_full_corpus_semantic_owner_overlay_v1/INDEX.json",
    "docs/INLINE_FULL_CORPUS_ACTION_COLLAPSE_OVERLAY.md",
    "docs/VALIDATION_LEDGER_INLINE_FULL_CORPUS_ACTION_COLLAPSE_OVERLAY.txt",
    "data/post_freeze/inline_full_corpus_action_collapse_overlay_v1/INDEX.json",
    "docs/INLINE_GAP_INTERNAL_24_EDGE_PROVENANCE_RECOVERY.md",
    "docs/VALIDATION_LEDGER_INLINE_GAP_INTERNAL_24_EDGE_PROVENANCE_RECOVERY.txt",
    "data/post_freeze/inline_gap_internal_24_edge_provenance_recovery_v1/INDEX.json",
    "docs/INLINE_F1_CROSS_BOUNDARY_ACTION_COLLAPSE_CLOSURE.md",
    "docs/VALIDATION_LEDGER_INLINE_F1_CROSS_BOUNDARY_ACTION_COLLAPSE.txt",
    "data/post_freeze/inline_f1_cross_boundary_action_collapse_v1/INDEX.json",
    "docs/INLINE_PRE_STAGE2_TO_STAGE2_CROSS_BOUNDARY_ADJUDICATION_CLOSURE.md",
    "docs/VALIDATION_LEDGER_INLINE_PRE_STAGE2_TO_STAGE2_CROSS_BOUNDARY_ADJUDICATION.txt",
    "data/post_freeze/inline_pre_stage2_to_stage2_cross_boundary_adjudication_v1/INDEX.json",
    "docs/MACHINE_READABLE_ACCOUNTING_SCHEMA.md",
    "docs/CLAIM_EXTRACTION_RULES.md",
    "docs/VALIDATION_POLICY.md",
    "docs/GITHUB_AND_CI_POLICY.md",
    "docs/PC_TO_SWITCH_PORTING_RULE_FRAMEWORK.md",
    "docs/PC_TO_SWITCH_ACCOUNTING_INVARIANTS.md",
    "docs/F1_STATIC_WRITE_AUTHORIZATION.md",
    "docs/PC_PATCH_ORACLE_TRACE_19_CLOSURE.md"
  ],
  "forbidden_scope_expansion": ["FULL_MIGRATION","BUILDER_IPS_RUNTIME","GAME_FILE_MODIFICATION","SCHEMA_REDESIGN"]
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
- inline full-corpus coverage overlay: COMPLETE / MATERIALIZED
- inline full-corpus semantic-owner overlay: COMPLETE / MATERIALIZED
- partial gap/forward action-collapse overlay: COMPLETE / MATERIALIZED
- exact gap-internal 24-edge provenance recovery: COMPLETE / MATERIALIZED
- F1 cross-boundary action-collapse closure: COMPLETE / MATERIALIZED
- pre-Stage2 <-> Stage2 cross-boundary adjudication closure: COMPLETE / MATERIALIZED
- central validation index: CURRENT THROUGH V201
- unresolved counterpart-routing queue inside forward-986: 0
- TRACE remainder: 0
- semantic-owner remainder inside exact unique-only gap 1,035: 0
- F1 cross-boundary unresolved units: 0
- F1 cross-boundary conflict units: 0
- pre-Stage2 <-> Stage2 boundary unresolved units: 0
- pre-Stage2 <-> Stage2 boundary conflict units: 0

No builder, IPS, runtime, or game-file implementation is authorized by this state.

## 2. Frozen semantic identities

FZ001 remains unchanged:

```text
source_state         91a54c8760f84f0e5b48e25dfda8adb9ae16ff32a83a4af86275fbc0c762322c
actions              a7c0f3ce3423b2a07797ef18e538c963140303751621a985dc6fe76c52bb8a4f
source_action_edges  1399fa309889399854d68f5d89f202df0f22f7be58ec2c85e3a02342987a4fe7
effective_claims     c29751ecca3233516fd9effc850e6e961d4418e3784266175df2af59798b6d35
```

FZ001 is an immutable historical baseline. Later canonical overlays refine current effective state only on their exact proven axes/membership and do not mutate these hashes.

## 3. Canonical target and source populations

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

Full inline planning partition:

```text
Stage-2 affine verified        13,771
F1 accepted mapped              1,311
forward-986                       986
unique-only coverage gap        1,035
TOTAL                           17,103
```

The four full-inline coverage sets remain pairwise disjoint and source-complete.

## 4. F1 write-safety authority

Historical F1 authorization partition remains unchanged:

```text
DIRECT_PORT static-write-authorized 158
PADDING_RECONSTRUCTION_REQUIRED      75
SHARED_OWNER_BINDING_REQUIRED        25
TERMINATOR_CAPACITY_FAIL              4
F1_RULE_REJECTED                     16
TOTAL                               278
```

Post-freeze evidence resolves all 278 on the target/counterpart axis, but static-write authorization remains 158. Current effective F1 write/action closure still open: 120.

## 5. Effective forward-986 routing closure

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

Counterpart/routing closure does not imply WRITE_SAFE.

## 6. Gap semantic-owner closure

The exact unique-only gap remains 1,035 rows:
- early R1-R3250: 1,009
- late family holes: 26

Owner-axis accounting:

```text
OWNER_BOUND        1,035
OWNER_UNRESOLVED       0
TOTAL              1,035
```

Important retained conclusions:
- all 225 logical-prefix rows are owner-bound only after deterministic complete-object/composite evidence;
- all 130 formatter/longer-object interior fragments are owner-bound as components of larger Switch semantic objects;
- `R14708 旅人` is an independent T2 owner and is not subsumed into `漂泊の旅人`;
- broad `R14543 北陸` and `R14549 四国` bind to the expanded Switch region family;
- `R2047 真備` remains an N:1 agreement relation with promoted Stage2 owner `R15678`.

## 7. Action-collapse overlays

### 7.1 Gap-internal exact provenance recovery

Canonical count and exact membership are now both closed:

```text
gap source rows          1,035
gap owner-action units   1,011
reduction                   24
exact 2:1 pair units         24
```

Exact membership is materialized at:
- `data/post_freeze/inline_gap_internal_24_edge_provenance_recovery_v1/MEMBERSHIP.json`

Pair-list SHA-256: `133173ac874c64c9fda0fc40d020363e9fe2214ecba258e9602100f9432c3a5d`.

Exactly one recovered pair, `R1264 + R1266`, is already contained in the existing gap/forward strong-core unit `R1264 + R1265 + R1266`. Therefore only 23 recovered pairs are independent when composing with that already-materialized exact graph. This overlap accounting does not alter the canonical internal reduction of 24.

### 7.2 Exact gap <-> forward adjudication

Exact review units = 37:

```text
confirmed strong-core composite units   35
confirmed T4 formatter units              1
confirmed T1 region reroute units         1
false-positive units                      0
TOTAL                                    37
```

Direct merge: 82 source rows -> 36 action units, reduction 46. The T1 broad-region unit remains a reroute to the detailed Stage2 expanded-region family and is not counted as one physical direct-merge action.

### 7.3 Exact gap+forward <-> F1 closure

```text
review units        11
source rows          28
owner/action units   11
reduction            17
unresolved            0
conflict              0
```

Formal terminal `SUBSUMED` rows remain deferred until final Action Ledger IDs exist. No new WRITE_SAFE authorization is created.

### 7.4 Exact pre-Stage2 <-> Stage2 boundary closure

```text
candidate review units          3
confirmed units                 2
rejected false positives        1
unresolved                      0
conflict                        0
new WRITE_SAFE                  0
```

- `R2047 真備` -> Stage2 owner `R15678 真備`; no second independent action.
- `R2553 館` <-> `R3283 角館` is rejected as different semantic owners.
- broad `R14542-R14550` reroutes to Stage2 expanded-region family `R16428-R16446`.

Stage2-internal action cardinality is still not canonicalized by this repository state.

## 8. Portability / Action Ledger authority

Current design contract: `docs/PORTABILITY_MATRIX_AND_ACTION_LEDGER_DESIGN.md`.

Fixed boundaries:
- PC Korean semantic result remains the default Oracle.
- source -> PC semantic obligation -> Switch semantic owner -> Switch action remain separate layers.
- target resolution, semantic-owner closure, action closure, write safety, implementation, and release closure are separate axes.
- capacity/storage blockers do not authorize translation shortening.
- future builder must be semantic-free and fail-closed.

## 9. Validation and precedence

- `docs/VALIDATION_LEDGER.md` is current through V201.
- exact gap-internal 24-edge recovery supersedes only the earlier provenance limitation that the 24 exact pairs were unavailable; the historical `1,035 -> 1,011` result is preserved.
- pre-Stage2 <-> Stage2 closure remains authoritative on its exact three units.
- F1 cross-boundary closure remains authoritative on its exact 11 units.
- gap/forward action-collapse remains authoritative on its exact 37 review units.
- historical coverage, routing and owner memberships remain unchanged.
- no canonical fact is revalidated solely because chat/model changes.

## 10. Repository operating boundary

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
- Base64/Contents-API write transport

## 11. Current STOP boundary

Status: `STOPPED_AWAITING_USER_SIGNAL`.

No builder/IPS/runtime implementation, game-file modification, schema redesign, write-safety expansion, or diagnostic build is authorized.

Next recommended scope: **`STAGE2_INTERNAL_ACTION_COLLAPSE_RESULT_MATERIALIZATION`**.

That scope may materialize the already-completed Stage2-internal candidate/adjudication analysis, but must not silently redo prior verified analysis, expand WRITE_SAFE, or begin builder/runtime work. A fresh explicit user signal is required.
