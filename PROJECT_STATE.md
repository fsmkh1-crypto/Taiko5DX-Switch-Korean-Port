# PROJECT_STATE

Last updated: 2026-09-13 (KST)

This file is the sole project-resume authority. Historical documents and ledgers preserve provenance but do not override this file.

<!-- PROJECT_RESUME_V2
{
  "schema": "PROJECT_RESUME_V2",
  "scope_id": "FORWARD_986_STABLE_STRUCTURAL_PARTITION_SYNTHESIS",
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
- exact structural census of remaining legacy 251 rows: COMPLETE / MATERIALIZED
- next scope: stable structural synthesis across the full forward 986

## 2. Frozen semantic identities

FZ001 semantic bindings remain unchanged:

```text
source_state         91a54c8760f84f0e5b48e25dfda8adb9ae16ff32a83a4af86275fbc0c762322c
actions              a7c0f3ce3423b2a07797ef18e538c963140303751621a985dc6fe76c52bb8a4f
source_action_edges  1399fa309889399854d68f5d89f202df0f22f7be58ec2c85e3a02342987a4fe7
effective_claims     c29751ecca3233516fd9effc850e6e961d4418e3784266175df2af59798b6d35
```

CAP64 correction and the 251 census do not reopen these frozen F1 semantic identities.

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

## 4. CAP64 corrected raw-start authority

Canonical corrected raw-start artifact:

- `data/post_freeze/forward_localization_raw_start_partition_v2/INDEX.json`
- SHA-256 `7134f9df08d6541d099bf0bf6dd305fc6232967910ef5ecb2818923da46ae4fc`

Current raw-start relation:

```text
L1 UNIQUE_FULL_JP_SINGLE_OWNER       454
L2 SHARED_PHYSICAL_JP_ALIAS          165
L3 JP_PREFIX_OF_LONGER_OBJECT        116
L4 NON_JP_LOCALIZATION_START           0
                                      ---
                                      735
```

The historical `forward_localization_family_partition_v1/` remains provenance only for its old 700-row completeness claim.

CAP rule remains:

- a stored raw candidate count of 64 is censored and means actual count `>= 64`;
- capped lists cannot prove absence, uniqueness/cardinality, complete language domain, or complete storage mutability.

Existing L1 semantic overlays remain scoped to their original 448 rows.
Existing L3 semantic overlay remains scoped to its original 88 rows.
R2300 retains an expanded-candidate re-review trigger.
No CAP64 correction row is Switch-write authorized by this correction.

## 5. Exact structural census of the remaining 251

Canonical report:

- `docs/FORWARD_RESIDUAL_STRUCTURAL_CENSUS_251.md`
- SHA-256 `e4c860cb3dbd38bce6d7881aafca73688cb10f042ef441f1072cb372a45da483`

Validation ledger:

- `docs/VALIDATION_LEDGER_FORWARD_STRUCTURAL_CENSUS_251.txt`
- SHA-256 `23b1b72270c06d7b65a5d2b066cd32eda630c7372929d1f2f0492d50abf5c2b9`

Machine-readable artifacts:

- `data/post_freeze/forward_residual_structural_census_251_v1/INDEX.json`
  - SHA-256 `7091621b3a5e5eb3028907df182036780f28fcba34e51d7ecc2bf1578b26766a`
- `data/post_freeze/forward_residual_structural_census_251_v1/MEMBERSHIP.json`
  - SHA-256 `c84f4fde42721c698ef1227836b67fb0eaaf005ee52a4ffbf46fcbbb98f480d9`

Exact structural partition:

```text
E1 TERMINATED_LOGICAL_FULL_SINGLE              67
E2 TERMINATED_LOGICAL_FULL_SHARED               6
E3 TERMINATED_LOGICAL_PREFIX                    4
E4A EMBEDDED_SINGLE_NO_RAW_OCCURRENCE          18
E4B EMBEDDED_SINGLE_RAW_MULTI_OCCURRENCE        8
E5 EMBEDDED_MULTI_PHYSICAL                    104
E6 EMPTY_LOGICAL_WINDOW                         1
E7 OPAQUE_FIXED_BLOCK_3244_3250                 7
G1 AFFINE_GAP_REGION_TABLE                      7
G2 AFFINE_GAP_ROLE_TABLE                       13
G3 AFFINE_GAP_ITEM_TABLE                        7
G4 AFFINE_GAP_UI_HEADER_COMPOSITE               1
G5 AFFINE_GAP_UTF16_MIXED_BLOCK                 8
                                                ---
                                                251
```

Integrity:

```text
family sum            251
intersection            0
unclassified            0
duplicate R-number      0
ordered source-ID SHA  2158d76714750ef9dd3661e9fba5ac6e14ab65d327e70dcdd567eac16c2ae80f
ordered R-ID SHA       891bda7b16bc8b3d59725c8a03f28ce3d04b9838b41611a1f7793c7e8a8090b4
```

The earlier provisional count of 79 additional JP logical relations is superseded by 78. `R1690` normalizes to an empty logical string and is isolated as E6; empty-string prefix matching is invalid evidence.

The legacy 35 formatter rows are not a top-level structural family. They distribute as E1=1, E4B=1, E5=33 and remain an overlay.

## 6. Current structural boundary

The 735 raw-start relation and the exact 251 census are both valid within their historical parent populations, but the boundary between them is not guaranteed to be a true data-structure boundary.

Coherent table/object structures cross the historical split. Therefore the next task is not semantic review of one family in isolation.

Next required analytical scope:

`FORWARD_986_STABLE_STRUCTURAL_PARTITION_SYNTHESIS`

Goals:

1. combine all 986 forward rows;
2. preserve exact membership/provenance from both current artifacts;
3. merge or split families only when physical object, table, storage, encoding, or occurrence structure justifies it;
4. produce one stable 986-row structural taxonomy;
5. defer semantic target approval until that taxonomy is stable;
6. keep consumer tracing as last resort.

This does not reopen F1 accepted 262 or Stage-2 affine target mappings.

## 7. Repository operating state

Repository writes use `GIT_OBJECT_ONLY_WRITE_MODE`.

Permitted remote write actions are exactly:

```text
create_blob
create_tree
create_commit
update_ref(main, force=false)
```

Forbidden write actions include `update_file`, `create_file`, `delete_file`, `create_branch`, force-push, and history rewrite.

## 8. Authority and boundaries

- `PROJECT_STATE.md` is the sole resume authority.
- Historical documents remain provenance and are not silently deleted.
- Verified F1 and Stage-2 affine facts are not reopened without a legitimate trigger.
- Structural membership is not semantic target approval.
- `TARGET_RESOLVED` remains distinct from `WRITE_SAFE`.
- PC Korean patch behavior remains the reference before inventing Switch-specific mechanisms.
- Accidental noncanonical commits `6aabde5e77a58e51fbe125101ae1b3f1309b4887`, `0c99cec726b7b1d0a0acefafb7d9ee30ebab6fdd`, `e19810b00258f726feb4edb0b398bc2f70b0127c`, `f3534d8d8b25c0dacd74e60652fa74bb148eb819` (temporary test files created by forbidden Contents-API writes) are historical provenance only. The canonical recovery commit removes all temporary files through Git-tree construction; no force-push/history rewrite is used.
- `docs/PC_TO_SWITCH_PORTING_RULE_FRAMEWORK.md` is unchanged.
- No builder/IPS/runtime implementation, game-file modification, full migration, or Switch write authorization is currently authorized.

## 9. Awaiting fresh signal

STOPPED_AWAITING_USER_SIGNAL.

Next recommended scope: read-only `FORWARD_986_STABLE_STRUCTURAL_PARTITION_SYNTHESIS`.

Do not begin semantic family audit, framework modification, builder/runtime work, or repository writes without a fresh explicit signal.
