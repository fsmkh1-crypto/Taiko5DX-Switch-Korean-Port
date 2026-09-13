# PROJECT_STATE

Last updated: 2026-09-13 (KST)

This file is the sole project-resume authority. Historical documents and ledgers preserve provenance but do not override this file.

<!-- PROJECT_RESUME_V2
{
  "schema": "PROJECT_RESUME_V2",
  "scope_id": "INLINE_FULL_CORPUS_ACTION_COLLAPSE_OVERLAY_MATERIALIZED",
  "scope_kind": "READ_ONLY_ACTION_COLLAPSE_OVERLAY",
  "status": "STOPPED_AWAITING_USER_SIGNAL",
  "last_closed_validation_id": "V181",
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
  "inline_full_corpus_coverage_overlay": "docs/INLINE_FULL_CORPUS_COVERAGE_OVERLAY.md",
  "inline_full_corpus_coverage_index": "data/post_freeze/inline_full_corpus_coverage_overlay_v1/INDEX.json",
  "inline_full_corpus_semantic_owner_overlay": "docs/INLINE_FULL_CORPUS_SEMANTIC_OWNER_OVERLAY.md",
  "inline_full_corpus_semantic_owner_index": "data/post_freeze/inline_full_corpus_semantic_owner_overlay_v1/INDEX.json",
  "inline_full_corpus_action_collapse_overlay": "docs/INLINE_FULL_CORPUS_ACTION_COLLAPSE_OVERLAY.md",
  "inline_full_corpus_action_collapse_index": "data/post_freeze/inline_full_corpus_action_collapse_overlay_v1/INDEX.json",
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
    "docs/MACHINE_READABLE_ACCOUNTING_SCHEMA.md",
    "docs/CLAIM_EXTRACTION_RULES.md",
    "docs/VALIDATION_POLICY.md",
    "docs/GITHUB_AND_CI_POLICY.md",
    "docs/PC_TO_SWITCH_PORTING_RULE_FRAMEWORK.md",
    "docs/PC_TO_SWITCH_ACCOUNTING_INVARIANTS.md",
    "docs/F1_STATIC_WRITE_AUTHORIZATION.md",
    "docs/PC_PATCH_ORACLE_TRACE_19_CLOSURE.md"
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
- inline full-corpus coverage overlay: COMPLETE / MATERIALIZED
- inline full-corpus semantic-owner overlay: COMPLETE / MATERIALIZED
- partial inline action-collapse overlay: COMPLETE / MATERIALIZED
- central validation index: CURRENT THROUGH V181
- unresolved counterpart-routing queue inside forward-986: 0
- TRACE remainder: 0
- semantic-owner remainder inside exact unique-only gap 1,035: 0

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

Current consolidated counterpart/routing classes remain:

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

## 6. Inline full-corpus coverage

Canonical source-complete planning partition:

```text
Stage-2 affine verified        13,771
F1 accepted mapped              1,311
forward-986                       986
unique-only coverage gap        1,035
TOTAL                           17,103
```

The 1,035 gap remains exact membership inherited from:
- `data/post_freeze/inline_full_corpus_coverage_overlay_v1/MEMBERSHIP.json#gap_ranges`

Gap split remains:
- early R1-R3250: 1,009
- late family holes: 26

## 7. Semantic-owner overlay for gap 1,035

Canonical owner-axis accounting remains:

```text
OWNER_BOUND        1,035
OWNER_UNRESOLVED       0
TOTAL              1,035
```

Important owner conclusions remain:
- all 225 logical-prefix rows are owner-bound only after deterministic complete-object/composite evidence;
- all 130 formatter/longer-object interior fragments are owner-bound as components of larger Switch semantic objects;
- `R14708 旅人` has an independent T2 role/status/profession semantic owner and is not subsumed into `漂泊の旅人`;
- broad-region `R14543 北陸` and `R14549 四国` bind to the expanded Switch region semantic-owner family;
- `R2047 真備` remains an N:1 agreement relation with its promoted owner.

No new Switch write authorization is created by semantic-owner closure.

## 8. Partial action-collapse overlay

Canonical overlay:
- `docs/INLINE_FULL_CORPUS_ACTION_COLLAPSE_OVERLAY.md`
- `data/post_freeze/inline_full_corpus_action_collapse_overlay_v1/INDEX.json`
- `data/post_freeze/inline_full_corpus_action_collapse_overlay_v1/MEMBERSHIP.json`
- validation: `docs/VALIDATION_LEDGER_INLINE_FULL_CORPUS_ACTION_COLLAPSE_OVERLAY.txt`

### 8.1 Gap-internal count-level result

Verified planning count:

```text
gap source rows          1,035
gap owner-action units   1,011
reduction                   24
```

Provenance limit: the exact 24 internal source/action edge memberships were not preserved in a machine-readable analysis artifact. The count is canonical planning state, but those edges must not be guessed or instantiated until exact membership is separately recovered/proven.

### 8.2 Exact gap <-> forward adjudication

Exact review units = 37:

```text
confirmed strong-core composite units   35
confirmed T4 formatter units              1
confirmed T1 region reroute units         1
false-positive units                      0
TOTAL                                    37
```

Direct-merge accounting:

```text
source rows       82
action units      36
direct reduction  46
```

The T1 region unit is not included in the direct reduction. The nine broad-region source obligations reroute to the detailed 19-entry expanded region owner family; final region action identities/cardinality remain deferred to Stage2 region-owner integration.

This action-cardinality closure creates no new `WRITE_SAFE` authorization.

## 9. Portability / Action Ledger design authority

Current design contract remains:
- `docs/PORTABILITY_MATRIX_AND_ACTION_LEDGER_DESIGN.md`

Fixed boundaries:
- PC Korean semantic result remains the default Oracle.
- source -> PC semantic obligation -> Switch semantic owner -> Switch action remain separate layers.
- target resolution, semantic-owner closure, action closure, write safety, implementation, and release closure are separate axes.
- capacity/storage blockers do not authorize translation shortening.
- future builder must be semantic-free and fail-closed.

## 10. Validation and precedence

- `docs/VALIDATION_LEDGER.md` is current through V181.
- latest action-collapse overlay takes precedence only on the exact action-cardinality relations it proves.
- the count-level gap-internal result does not silently manufacture row-level edges.
- historical coverage and owner memberships remain unchanged.
- no canonical fact is revalidated solely because chat/model changes.

## 11. Repository operating boundary

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

## 12. Current STOP boundary

Status: `STOPPED_AWAITING_USER_SIGNAL`.

Do not begin F1-boundary adjudication, Stage2-boundary integration, write-safety expansion, builder/IPS/runtime implementation, game-file modification, schema redesign, or diagnostic build without a fresh explicit user execution signal.

Next recommended scope: **`GAP_FORWARD_TO_F1_CROSS_BOUNDARY_CANDIDATE_GENERATION_READ_ONLY`**.

That scope may generate the exact candidate list between the current gap+forward action view and F1 1,311 only. It must STOP before candidate adjudication and must not touch Stage2 or write safety.
