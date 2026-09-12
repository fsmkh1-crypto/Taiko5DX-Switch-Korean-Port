# PROJECT_STATE

Last updated: 2026-09-13 (KST)

This file is the sole project-resume authority. Historical documents and ledgers preserve provenance but do not override this file.

<!-- PROJECT_RESUME_V2
{
  "schema": "PROJECT_RESUME_V2",
  "scope_id": "FORWARD_986_SEMANTIC_FAMILY_AUDIT",
  "scope_kind": "READ_ONLY",
  "status": "STOPPED_AWAITING_USER_SIGNAL",
  "last_closed_validation_id": "V107",
  "last_closed_stage_commit": "ef494198345e01ea11c5b287dfb4d6e44081dde5",
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
- corrected raw-start partition v2: MATERIALIZED (`454 / 165 / 116 / 0 = 735`)
- historical 700-row v1 completeness claim: SUPERSEDED
- historical L4=R1291 claim: RETRACTED
- exact structural census of remaining 251 rows: COMPLETE / MATERIALIZED
- stable structural synthesis of full forward 986: COMPLETE / MATERIALIZED
- next scope: semantic-family audit on the stable 986 partition

## 2. Frozen semantic identities

FZ001 semantic bindings remain unchanged:

```text
source_state         91a54c8760f84f0e5b48e25dfda8adb9ae16ff32a83a4af86275fbc0c762322c
actions              a7c0f3ce3423b2a07797ef18e538c963140303751621a985dc6fe76c52bb8a4f
source_action_edges  1399fa309889399854d68f5d89f202df0f22f7be58ec2c85e3a02342987a4fe7
effective_claims     c29751ecca3233516fd9effc850e6e961d4418e3784266175df2af59798b6d35
```

Forward structural work does not reopen these frozen F1 semantic identities.

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

## 4. Historical forward artifacts retained as provenance

CAP64 correction:
- `data/post_freeze/forward_localization_raw_start_partition_v2/INDEX.json`
- raw-start relation count: 735
- L1/L2/L3/L4 = 454 / 165 / 116 / 0

Residual structural census:
- `data/post_freeze/forward_residual_structural_census_251_v1/INDEX.json`
- exact population count: 251
- 13 exact structural families within that historical population
- corrected provisional logical-relation observation: 79 -> 78

The historical `735 / 251` split is not a stable data-structure boundary.

## 5. Current structural authority — forward 986

Canonical document:
- `docs/FORWARD_986_STABLE_STRUCTURAL_PARTITION.md`
- SHA-256 `c4c59977ae8072162009c637f6e35716dfbce7e4926587be4dab0147ec5939b3`

Validation ledger:
- `docs/VALIDATION_LEDGER_FORWARD_986_STRUCTURAL.txt`
- SHA-256 `13cbfa16e31ebc553bc720fcc3e3f2dc8017a7599b309d639ed65d029a5171f9`

Machine-readable index:
- `data/post_freeze/forward_986_stable_structural_partition_v1/INDEX.json`
- SHA-256 `1aaa6355f5f7618f883eca217282dbae960fb6ef02e55c2d1e5be728b47bffe0`

Machine-readable membership:
- `data/post_freeze/forward_986_stable_structural_partition_v1/MEMBERSHIP.json`
- SHA-256 `487b287b6d2a0cb0ea23aa2ab66ab5189418c08ab916d0b8c539fca4a75a8e4c`

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
                                                    ---
                                                    986
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

Legacy formatter 35 remains an overlay: S1=1 / S4B=1 / S5=33.

## 6. Historical semantic overlay scope

- Historical L1 semantic overlays remain evidence for their original reviewed membership only; stable S1 is broader.
- Historical L3 88-row semantic/context review remains evidence for its original rows, but table-family rows now have stronger stable structural parents.
- The existing unresolved five `R651, R1062, R1277, R1283, R1284` remain in stable S3.
- `R2300` remains in S3 and retains its expanded-candidate-set re-review trigger.
- No row is newly Switch-write authorized by the stable structural synthesis.

## 7. Repository operating state

Permitted remote write actions are exactly:

```text
create_blob
create_tree
create_commit
update_ref(main, force=false)
```

Forbidden write actions include `update_file`, `create_file`, `delete_file`, `create_branch`, force-push, and history rewrite.

Historical write-rule violations from the prior 251 canonicalization attempt remain provenance only. The temporary files created by those noncanonical Contents-API commits were removed by canonical recovery commit `60ee3d8c9a63ae817a93e1996d0077e53c742e80`. They must not be repeated or used as precedent.

## 8. Authority and boundaries

- `PROJECT_STATE.md` is the sole resume authority.
- Verified F1 and Stage-2 affine facts are not reopened by forward structural synthesis.
- Historical artifacts remain provenance; supersession does not delete history.
- Stable structural family identity is distinct from semantic target disposition.
- `TARGET_RESOLVED` remains distinct from `WRITE_SAFE`.
- PC Korean patch behavior remains the reference before inventing Switch-specific mechanisms.
- No full migration, builder, IPS, runtime implementation, game-file modification, or new Switch write authorization is currently authorized.

## 9. Awaiting fresh signal

STOPPED_AWAITING_USER_SIGNAL.

Next recommended scope: `FORWARD_986_SEMANTIC_FAMILY_AUDIT`.

Recommended analysis order:
T1-T5 -> S1 additional/unreviewed scope -> S2 -> S3 -> S4A/S4B -> S5 -> S6/S7.

Do not begin semantic review, framework modification, builder/runtime work, or further repository writes without a fresh explicit signal.
