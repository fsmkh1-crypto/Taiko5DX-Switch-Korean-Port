# FORWARD 986 STABLE STRUCTURAL PARTITION SYNTHESIS

Date: 2026-09-13 (KST)
Canonical parent HEAD: `60ee3d8c9a63ae817a93e1996d0077e53c742e80`
Scope: read-only synthesis of the complete forward-analysis population after CAP64 correction and the exact 251-row residual structural census.
Status: COMPLETE / STRUCTURAL ONLY / NO SWITCH WRITE AUTHORIZATION

## 1. 요약

The historical `735 raw-start + 251 residual` split is provenance, not a stable structural boundary.

The full forward population of 986 rows is now partitioned into 13 exact, disjoint structural families:

| family | rows |
|---|---:|
| S1_LOGICAL_FULL_SINGLE_PHYSICAL_SINGLE_OWNER | 517 |
| S2_LOGICAL_FULL_SINGLE_PHYSICAL_SHARED_OWNER | 167 |
| S3_LOGICAL_PREFIX_OF_LONGER_JP_OBJECT | 112 |
| S4A_EMBEDDED_SINGLE_PHYSICAL_NO_RAW_OCCURRENCE | 18 |
| S4B_EMBEDDED_SINGLE_PHYSICAL_RAW_MULTI_OCCURRENCE | 8 |
| S5_EMBEDDED_MULTI_PHYSICAL | 104 |
| S6_EMPTY_LOGICAL_WINDOW | 1 |
| S7_OPAQUE_FIXED_BLOCK_3244_3250 | 7 |
| T1_REGION_TABLE | 7 |
| T2_ROLE_STATUS_PROFESSION_TABLE | 19 |
| T3_ITEM_CATEGORY_TABLE | 7 |
| T4_CP932_UI_LABEL_BLOCK | 10 |
| T5_UTF16_MIXED_UI_BLOCK | 9 |
| total | 986 |

Integrity: intersection 0 / unclassified 0 / duplicate R-number 0.

Machine-readable membership:
- `data/post_freeze/forward_986_stable_structural_partition_v1/MEMBERSHIP.json`
- SHA-256 `487b287b6d2a0cb0ea23aa2ab66ab5189418c08ab916d0b8c539fca4a75a8e4c`

Index:
- `data/post_freeze/forward_986_stable_structural_partition_v1/INDEX.json`
- SHA-256 `1aaa6355f5f7618f883eca217282dbae960fb6ef02e55c2d1e5be728b47bffe0`

Population ordered source-ID SHA-256: `52d71e85ff11b7327a563623ba00ea99dd7e7fdb733724b17b0a598e2579b370`
Population ordered R-ID SHA-256: `76ec677dd6cc9b97f82828925f32296328cef6d7a3140b0d75a2a1c60f0af776`

## 2. 확정된 사실

### 2.1 Raw-start and terminated logical families unify

Raw-start L1 and terminated-logical E1 express the same stable target-cardinality structure after NUL-aware normalization. Four L1 rows are moved to the stronger T4 UI block, yielding S1 = 517.

Raw-start L2 and terminated-logical E2 similarly unify. Four L2 rows are moved to T4, yielding S2 = 167.

Raw-start L3 and terminated-logical E3 unify only after stronger table/storage overrides are removed. Six role-table rows move to T2, R16452 moves to T4, and R16461 moves to T5, yielding S3 = 112.

### 2.2 Stronger table/storage evidence overrides generic prefix classification

T2 expands from the 13-row residual role/status/profession table with six raw-start L3 rows:
`R14690, R14700, R14702, R14704, R14706, R14711`.

T4 combines:
- raw-start L1: `R16448, R16451, R16454, R16456`
- raw-start L2: `R16447, R16449, R16455, R16457`
- raw-start L3: `R16452`
- residual G4: `R16453`

This forms one 10-row CP932 UI-label block.

T5 combines residual G5 with raw-start `R16461`, yielding a 9-row UTF-16/mixed UI block. The raw byte value at R16461 must not be treated as ordinary CP932 prefix evidence.

### 2.3 Formatter remains an overlay

The 35 historical formatter-labeled rows distribute as:
- S1: 1
- S4B: 1
- S5: 33

Formatter/control behavior is therefore not a top-level structural axis.

## 3. 유력한 가설

The stable structural precedence supported by the 986-row synthesis is:

1. coherent table/storage/encoding structure;
2. NUL-aware logical full match;
3. shared-owner cardinality;
4. logical prefix;
5. embedded containment;
6. opaque/unknown data structure.

This ordering should be used for subsequent semantic-family review unless contradicted by stronger occurrence-level evidence.

## 4. 미확정 사항

Structural membership is closed, but semantic target resolution is not.

Key future obligations include:
- S2 shared-owner obligation binding;
- S3 semantic/context review, including the existing unresolved five and R2300 re-review trigger;
- S4B occurrence binding;
- S5 multi-physical target reduction;
- S7 encoding/data-structure analysis;
- T1-T5 table-level semantic and replacement/action analysis.

No row is newly Switch-write authorized by this synthesis.

## 5. 기각된 가설

The following shortcuts are rejected:

- `735 / 251` is a true data-structure boundary.
- Raw-start and terminated-logical full matches must remain separate semantic-target families.
- Every L3/E3 prefix relation outranks coherent table/storage evidence.
- Short byte prefix matches inside UTF-16/mixed blocks are ordinary CP932 localization evidence.
- Formatter presence defines a top-level structural family.
- Structural target resolution automatically implies write safety.

## 6. 관련 영향 범위

Historical artifacts remain provenance:
- `forward_localization_raw_start_partition_v2`
- `forward_residual_structural_census_251_v1`
- historical L1/L3 semantic overlays

The new 986 partition supersedes their historical boundary only for current structural/semantic forward work. It does not reopen F1 accepted 262 membership, Stage-2 affine target mappings, FZ001 frozen semantic identities, or PC DLL/runtime conclusions.

## 7. 수정 제안

Next recommended scope is `FORWARD_986_SEMANTIC_FAMILY_AUDIT`.

Recommended order:
T1-T5 -> S1 additional/unreviewed scope -> S2 -> S3 -> S4A/S4B -> S5 -> S6/S7.

Semantic target disposition and write-safety/action classification must remain separate stages.

No framework modification, builder/IPS/runtime work, game-file modification, or Switch write authorization is included in this synthesis.
