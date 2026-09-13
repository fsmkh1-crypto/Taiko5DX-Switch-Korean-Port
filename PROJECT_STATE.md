# PROJECT_STATE

Last updated: 2026-09-13 (KST)

This file is the sole project-resume authority. Historical documents and ledgers preserve provenance but do not override this file.

<!-- PROJECT_RESUME_V2
{
  "schema": "PROJECT_RESUME_V2",
  "scope_id": "PC_PATCH_ORACLE_TRACE_19_CLOSURE_MATERIALIZED",
  "scope_kind": "READ_ONLY",
  "status": "STOPPED_AWAITING_USER_SIGNAL",
  "last_closed_validation_id": "V143",
  "last_closed_stage_commit": "0710e36077dd5184974701da67c4b019fa751851",
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
  "machine_fact_binding": "data/pilot/f1_v1_candidate/bindings.json",
  "required_reads": [
    "data/pilot/f1_v1_candidate/schema_freeze_declaration.json",
    "docs/MACHINE_READABLE_ACCOUNTING_SCHEMA.md",
    "docs/CLAIM_EXTRACTION_RULES.md",
    "docs/VALIDATION_POLICY.md",
    "docs/PC_TO_SWITCH_PORTING_RULE_FRAMEWORK.md",
    "docs/PC_TO_SWITCH_ACCOUNTING_INVARIANTS.md",
    "docs/STAGE2_AFFINE_STRUCTURAL_TARGETING.md",
    "docs/CAP64_FORWARD_CORRECTION.md",
    "docs/VALIDATION_LEDGER_CAP64_CORRECTION.txt",
    "data/post_freeze/forward_localization_raw_start_partition_v2/INDEX.json",
    "docs/FORWARD_RESIDUAL_STRUCTURAL_CENSUS_251.md",
    "docs/VALIDATION_LEDGER_FORWARD_STRUCTURAL_CENSUS_251.txt",
    "data/post_freeze/forward_residual_structural_census_251_v1/INDEX.json",
    "docs/FORWARD_986_STABLE_STRUCTURAL_PARTITION.md",
    "docs/VALIDATION_LEDGER_FORWARD_986_STRUCTURAL.txt",
    "data/post_freeze/forward_986_stable_structural_partition_v1/INDEX.json",
    "docs/L3_SEMANTIC_PC_MECHANISM_ANALYSIS.md",
    "data/post_freeze/l3_semantic_pc_mechanism_v1/INDEX.json",
    "docs/PC_PATCH_ORACLE_RESOLVER_V1.md",
    "docs/VALIDATION_LEDGER_PC_PATCH_ORACLE_V1.txt",
    "data/post_freeze/pc_patch_oracle_resolver_v1/INDEX.json",
    "docs/PC_PATCH_ORACLE_ASSISTED_297_FOLLOWUP.md",
    "docs/VALIDATION_LEDGER_PC_PATCH_ORACLE_ASSISTED_297_FOLLOWUP.txt",
    "data/post_freeze/pc_patch_oracle_assisted_297_followup_v1/INDEX.json",
    "docs/PC_PATCH_ORACLE_ASTRA_10_FOLLOWUP.md",
    "docs/VALIDATION_LEDGER_PC_PATCH_ORACLE_ASTRA_10_FOLLOWUP.txt",
    "data/post_freeze/pc_patch_oracle_astra_10_followup_v1/INDEX.json",
    "docs/PC_PATCH_ORACLE_TRACE_19_CLOSURE.md",
    "docs/VALIDATION_LEDGER_PC_PATCH_ORACLE_TRACE_19_CLOSURE.txt",
    "data/post_freeze/pc_patch_oracle_trace_19_closure_v1/INDEX.json",
    "data/pilot/f1_v1_candidate/bindings.json"
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

Inherited without revalidation:
- Stage 1 canonical inventory: COMPLETE
- Stage 2 affine structural targeting: COMPLETE
- F1 localization-sequence audit: COMPLETE
- F1 accepted residual membership: 262
- F1 action split: 158 / 75 / 25 / 4, with 16 F1-rule rejects
- schema-v1 freeze declaration: FROZEN — FZ001
- PC DLL/runtime mechanics: inherited from canonical runtime documents

Post-freeze forward work:
- CAP64 root-cause audit: COMPLETE
- stable structural synthesis of full forward 986: COMPLETE / MATERIALIZED
- PC Korean Patch Oracle Resolver V1: COMPLETE / MATERIALIZED
- Oracle-assisted 297 follow-up: COMPLETE / MATERIALIZED
- Astra-required 10 follow-up: COMPLETE / MATERIALIZED
- TRACE 19 cause-group closure: COMPLETE / MATERIALIZED
- ORACLE_ASSISTED remainder: 0
- ASTRA_REQUIRED remainder: 0
- TRACE remainder: 0
- current unresolved counterpart-routing queue: 0
- next scope requires a fresh explicit user signal

## 2. Frozen semantic identities

FZ001 semantic bindings remain unchanged:

```text
source_state         91a54c8760f84f0e5b48e25dfda8adb9ae16ff32a83a4af86275fbc0c762322c
actions              a7c0f3ce3423b2a07797ef18e538c963140303751621a985dc6fe76c52bb8a4f
source_action_edges  1399fa309889399854d68f5d89f202df0f22f7be58ec2c85e3a02342987a4fe7
effective_claims     c29751ecca3233516fd9effc850e6e961d4418e3784266175df2af59798b6d35
```

Forward oracle work does not reopen these frozen F1 semantic identities.

## 3. Canonical target and stable accounting

Target:
- Title ID `0100346017304000`
- Switch v1.1.3
- Build ID `D9120950C258610A746F4A31CE3A3B376DE393D9`
- Switch `main` SHA-256 `b366e692208f3c0cc18bc1884ef95689b6b11d722fa2d749b8500abccbc3109b`

Stable accounting:

```text
inline rows                         17,103
Stage-1 raw exceptions              11,050
Stage-2 residual                     1,248
F1 accepted excluded                   262
forward-analysis population            986
```

F1 remains:

```text
DIRECT_PORT authorized               158
PADDING_RECONSTRUCTION_REQUIRED       75
SHARED_OWNER_BINDING_REQUIRED         25
TERMINATOR_CAPACITY_FAIL               4
F1_RULE_REJECTED                      16
TOTAL                                278
```

## 4. Current structural authority — forward 986

Canonical structural artifacts:
- `docs/FORWARD_986_STABLE_STRUCTURAL_PARTITION.md`
- `docs/VALIDATION_LEDGER_FORWARD_986_STRUCTURAL.txt`
- `data/post_freeze/forward_986_stable_structural_partition_v1/INDEX.json`
- `data/post_freeze/forward_986_stable_structural_partition_v1/MEMBERSHIP.json`

Stable partition:

```text
S1 LOGICAL_FULL_SINGLE_PHYSICAL_SINGLE_OWNER      517
S2 LOGICAL_FULL_SINGLE_PHYSICAL_SHARED_OWNER      167
S3 LOGICAL_PREFIX_OF_LONGER_JP_OBJECT             112
S4A EMBEDDED_SINGLE_PHYSICAL_NO_RAW_OCCURRENCE     18
S4B EMBEDDED_SINGLE_PHYSICAL_RAW_MULTI_OCCURRENCE   8
S5 EMBEDDED_MULTI_PHYSICAL                         104
S6 EMPTY_LOGICAL_WINDOW                              1
S7 OPAQUE_FIXED_BLOCK_3244_3250                     7
T1 REGION_TABLE                                      7
T2 ROLE_STATUS_PROFESSION_TABLE                     19
T3 ITEM_CATEGORY_TABLE                               7
T4 CP932_UI_LABEL_BLOCK                             10
T5 UTF16_MIXED_UI_BLOCK                              9
TOTAL                                               986
intersection                                          0
unclassified                                          0
```

Population ordered source-ID SHA-256: `52d71e85ff11b7327a563623ba00ea99dd7e7fdb733724b17b0a598e2579b370`  
Population ordered R-ID SHA-256: `76ec677dd6cc9b97f82828925f32296328cef6d7a3140b0d75a2a1c60f0af776`

Structural precedence:
1. coherent table/storage/encoding family;
2. NUL-aware logical full match;
3. shared-owner cardinality;
4. logical prefix;
5. embedded containment;
6. opaque/unknown structure.

## 5. Historical authority — PC Patch Oracle V1

Canonical report:
- `docs/PC_PATCH_ORACLE_RESOLVER_V1.md`
- semantic SHA-256 `74a7b4a28266cc2cb7ae396d81d5815e0b4ee9fb7e80e719f1a93cde71df91d9`

Validation ledger:
- `docs/VALIDATION_LEDGER_PC_PATCH_ORACLE_V1.txt`
- semantic SHA-256 `f0bdc90e68c4466ce62038053e1eb0a069f6ade2072ef6abed55d613e90cce8f`

Machine-readable:
- `data/post_freeze/pc_patch_oracle_resolver_v1/INDEX.json`
- semantic SHA-256 `076aeaaf3fb5db065d5ec6d68961324b02669fee4863d67405b9d70be65cb7c3`
- `data/post_freeze/pc_patch_oracle_resolver_v1/MEMBERSHIP.json`
- semantic SHA-256 `4fc30336e34962439f2228442ee4d5331065fbe639141b17c550720acc412822`

Historical routing remains provenance:

```text
ORACLE_RESOLVED      656
ORACLE_REROUTED        7
ORACLE_ASSISTED       297
ASTRA_REQUIRED         10
TRACE_REQUIRED         16
TOTAL                 986
```

## 6. Current authority — assisted 297 follow-up

Canonical report:
- `docs/PC_PATCH_ORACLE_ASSISTED_297_FOLLOWUP.md`
- semantic SHA-256 `9cd19de89cfbd08e2492c1a97a5b388cbbabf6be54174bbc1d805f3d2c07f898`

Validation ledger:
- `docs/VALIDATION_LEDGER_PC_PATCH_ORACLE_ASSISTED_297_FOLLOWUP.txt`
- semantic SHA-256 `2e2e14b7c580de42452456f2f37b568afb96d9ba55817ad3148cee73f8b2ff1b`

Machine-readable:
- `data/post_freeze/pc_patch_oracle_assisted_297_followup_v1/INDEX.json`
- semantic SHA-256 `2746d7b89f1c829855ba714a332f50b543f6956685d35b5a228bd1e76c9b9679`
- `data/post_freeze/pc_patch_oracle_assisted_297_followup_v1/MEMBERSHIP.json`
- semantic SHA-256 `506b10ce073ce0d87feabe4c031f1b16b6ea0267d177c99090d921b1a47f0848`

Normalized 297:

```text
TARGET_RESOLVED                         65
COMPOSITE_OR_FORMATTER_RESOLVED        231
NEED_TRACE                               1  (R19)
TOTAL                                  297
intersection                             0
unclassified                             0
```

The rejected noncanonical `93 / 203 / 1` taxonomy must not be reused.

## 7. Current authority — Astra 10 follow-up

Canonical report:
- `docs/PC_PATCH_ORACLE_ASTRA_10_FOLLOWUP.md`
- semantic SHA-256 `c0ba5ca6ba229bdfe4bca20053e8ace32767fc132afc6bc4039becc18c6036f7`

Validation ledger:
- `docs/VALIDATION_LEDGER_PC_PATCH_ORACLE_ASTRA_10_FOLLOWUP.txt`
- semantic SHA-256 `19abaa08e0f2c473f28dfe8659d054b1497575586a28b801f245cae727adc4d6`

Machine-readable:
- `data/post_freeze/pc_patch_oracle_astra_10_followup_v1/INDEX.json`
- semantic SHA-256 `e4f563ad35f16cbac77704227af44496e680f342c1f337b2eebc7dbc270a728c`
- `data/post_freeze/pc_patch_oracle_astra_10_followup_v1/MEMBERSHIP.json`
- semantic SHA-256 `a5d86347752d2dee56490d7d6c7716af3e79a6daa3cb787c2b32bb177a543cb1`

Astra 10 partition:

```text
TARGET_RESOLVED                          0
COMPOSITE_OR_FORMATTER_RESOLVED          8
NEED_TRACE                               2
TOTAL                                   10
intersection                             0
unclassified                             0
ASTRA_REQUIRED_REMAINDER                 0
```

Resolved composite:
`R75, R651, R1062, R1277, R1583, R1591, R1631, R2572`

Historical Astra trace:
`R1283, R1284`

The TRACE-closure overlay below supersedes only the current effective disposition of those two rows; the Astra artifact remains provenance.

## 8. Current authority — TRACE 19 closure

Canonical report:
- `docs/PC_PATCH_ORACLE_TRACE_19_CLOSURE.md`
- semantic SHA-256 `bd3ded42d5b6c9fe8475811983bddeef1850f1fd9a4e636d8bc7b2d16353a23d`

Validation ledger:
- `docs/VALIDATION_LEDGER_PC_PATCH_ORACLE_TRACE_19_CLOSURE.txt`
- semantic SHA-256 `32a2141d1d7a4fa0f608a638091c5ad89b8500911bd3808902919b1d37becc7b`

Machine-readable:
- `data/post_freeze/pc_patch_oracle_trace_19_closure_v1/INDEX.json`
- semantic SHA-256 `606d5c198bab86e4763481d945eef6e532898b463f9c95dc0cf74ef447692bbd`
- `data/post_freeze/pc_patch_oracle_trace_19_closure_v1/MEMBERSHIP.json`
- semantic SHA-256 `080cbddce6c01793d158660eb2fd9bec365cd6801fcf6858eaa812211228e3f5`

Exact TRACE-closure partition:

```text
TARGET_RESOLVED                          8
COMPOSITE_OR_FORMATTER_RESOLVED          3
ORACLE_REROUTED                          8
NEED_TRACE                               0
TOTAL                                   19
intersection                             0
unclassified                             0
TRACE_REMAINDER                          0
```

Cause groups and final routing:
- `R19`: target resolved / owner bound / JP ID 1088; merged-consumer presentation conflict remains an implementation policy issue.
- `R1283`: composite/formatter resolved / opening owner JP ID 2795.
- `R1284`: composite/formatter resolved / closing owner JP ID 2796.
- `R1690`: composite/formatter resolved / padding-extension component owned by `R1689 -> JP ID 3245`.
- `R3244-R3250`: target resolved / GBK CN exact counterparts at localization IDs 1099-1105; language-table routing/presentation remains separate.
- `R16458-R16465`: rerouted / one PC UTF-16 display-resolution warning subsumed by Switch JP localization ID 1480.

No row remains in TRACE.

## 9. Effective forward routing

After Oracle V1 + assisted-297 + Astra-10 + TRACE-19 closure:

```text
BASE_ORACLE_RESOLVED                         656
BASE_ORACLE_REROUTED                           7
ASSISTED_FOLLOWUP_TARGET_RESOLVED             65
ASSISTED_FOLLOWUP_COMPOSITE_RESOLVED         231
ASTRA_FOLLOWUP_COMPOSITE_RESOLVED              8
TRACE_CLOSURE_TARGET_RESOLVED                   8
TRACE_CLOSURE_COMPOSITE_RESOLVED                3
TRACE_CLOSURE_REROUTED                          8
TRACE_REQUIRED                                  0
                                             ---
TOTAL                                        986
ORACLE_ASSISTED_REMAINDER                      0
ASTRA_REQUIRED_REMAINDER                       0
TRACE_REMAINDER                                0
```

Consolidated current counterpart classes:
- base deterministic Oracle resolved: 656
- target resolved: 73
- composite/formatter resolved: 242
- rerouted: 15
- trace: 0
- total: 986

This is counterpart/routing closure only. It creates no new `WRITE_SAFE` authorization.

## 10. Preserved rejected shortcuts

Do not reintroduce:
- unique physical target + replacement agreement alone;
- full Switch object elsewhere in PC patch alone;
- loose reverse-context alone;
- two-byte Korean replacement containment alone;
- sparse adjacency alone;
- structural family as semantic target;
- same Korean replacement as proof of same target;
- occurrence order/NUL padding alone to bind R1283/R1284;
- empty-string prefix matching as positive evidence;
- CP932 decode failure as proof of non-text;
- CN exact counterpart as automatic CN write authorization;
- absent exact PC-specific object as permission for silent omission;
- target/counterpart/routing resolution = WRITE_SAFE;
- consumer trace before exhausting PC patch oracle evidence;
- nonmatching PC EXE as global canonical target-build XREF proof.

## 11. Repository operating state

Permitted remote write actions are exactly:

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
- force-push
- history rewrite

## 12. Authority and boundaries

- `PROJECT_STATE.md` is the sole resume authority.
- FZ001, F1, Stage-2, and stable 986 structural membership are not reopened.
- Oracle V1 and earlier overlays remain provenance where superseded.
- PC Korean patch behavior remains the reference before inventing Switch-specific mechanisms.
- counterpart/routing closure remains distinct from `WRITE_SAFE`.
- no builder/IPS/runtime implementation, game-file modification, or new Switch write authorization is created.
- exact target PC EXE remains unavailable; no new global target-build XREF/preimage ownership claim is made.

## 13. Awaiting fresh signal

STOPPED_AWAITING_USER_SIGNAL.

The forward-986 counterpart/routing problem is now closed with TRACE remainder `0`.

Next recommended scope: write-safety/action-ledger planning for the resolved/rerouted forward obligations, still separated from builder/runtime implementation.

Do not begin action-ledger redesign, write-safety implementation, builder/runtime work, game-file modification, or further repository writes without a fresh explicit signal.
