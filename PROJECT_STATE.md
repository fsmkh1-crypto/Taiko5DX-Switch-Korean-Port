# PROJECT_STATE

Last updated: 2026-09-13 (KST)

This file is the sole project-resume authority. Historical documents and ledgers preserve provenance but do not override this file.

<!-- PROJECT_RESUME_V2
{
  "schema": "PROJECT_RESUME_V2",
  "scope_id": "PC_PATCH_ORACLE_ASSISTED_297_FOLLOWUP",
  "scope_kind": "READ_ONLY",
  "status": "STOPPED_AWAITING_USER_SIGNAL",
  "last_closed_validation_id": "V118",
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
    "docs/PC_PATCH_ORACLE_RESOLVER_V1.md",
    "docs/VALIDATION_LEDGER_PC_PATCH_ORACLE_V1.txt",
    "data/post_freeze/pc_patch_oracle_resolver_v1/INDEX.json",
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
- PC Korean Patch Oracle Resolver V1: COMPLETE / MATERIALIZED
- next scope: read-only follow-up on the remaining 297 oracle-assisted rows

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

## 4. Historical forward artifacts retained as provenance

CAP64 correction:
- `data/post_freeze/forward_localization_raw_start_partition_v2/INDEX.json`
- raw-start relation count: 735
- L1/L2/L3/L4 = 454 / 165 / 116 / 0

Residual structural census:
- `data/post_freeze/forward_residual_structural_census_251_v1/INDEX.json`
- exact population count: 251
- corrected provisional logical-relation observation: 79 -> 78

The historical `735 / 251` split is provenance, not a stable data-structure boundary.

## 5. Current structural authority — forward 986

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
                                                    ---
                                                    986
intersection                                          0
unclassified                                          0
```

Population ordered source-ID SHA-256: `52d71e85ff11b7327a563623ba00ea99dd7e7fdb733724b17b0a598e2579b370`  
Population ordered R-ID SHA-256: `76ec677dd6cc9b97f82828925f32296328cef6d7a3140b0d75a2a1c60f0af776`

Structural precedence remains:
1. coherent table/storage/encoding family;
2. NUL-aware logical full match;
3. shared-owner cardinality;
4. logical prefix;
5. embedded containment;
6. opaque/unknown structure.

## 6. Current semantic/target-routing authority — PC Patch Oracle V1

Canonical report:
- `docs/PC_PATCH_ORACLE_RESOLVER_V1.md`
- semantic SHA-256 `74a7b4a28266cc2cb7ae396d81d5815e0b4ee9fb7e80e719f1a93cde71df91d9`

Validation ledger:
- `docs/VALIDATION_LEDGER_PC_PATCH_ORACLE_V1.txt`
- semantic SHA-256 `f0bdc90e68c4466ce62038053e1eb0a069f6ade2072ef6abed55d613e90cce8f`

Machine-readable artifacts:
- `data/post_freeze/pc_patch_oracle_resolver_v1/INDEX.json`
- semantic SHA-256 `076aeaaf3fb5db065d5ec6d68961324b02669fee4863d67405b9d70be65cb7c3`
- `data/post_freeze/pc_patch_oracle_resolver_v1/MEMBERSHIP.json`
- semantic SHA-256 `4fc30336e34962439f2228442ee4d5331065fbe639141b17c550720acc412822`

Exact routing:

```text
ORACLE_RESOLVED      656
ORACLE_REROUTED        7
ORACLE_ASSISTED       297
ASTRA_REQUIRED         10
TRACE_REQUIRED         16
                    ----
TOTAL                 986
intersection            0
unclassified            0
```

`ORACLE_RESOLVED` family distribution:

```text
S1 443
S2 122
S3  41
S4A 16
S4B  5
S5  18
T4  10
T5   1
TOTAL 656
```

`ORACLE_ASSISTED` remainder:

```text
S5  82
S1  73
S3  66
S2  45
T2  19
T3   7
S4B  3
S4A  2
TOTAL 297
```

Current Astra queue:
- historical semantic holdouts: `R651, R1062, R1277, R1283, R1284, R2572`
- no-useful-oracle-signal S5: `R75, R1583, R1591, R1631`

Current trace queue:
- `R16458-R16465`
- `R1690`
- `R3244-R3250`

T1 reroute:
- broad-region source rows `R14542, R14544, R14545, R14546, R14547, R14548, R14550`
- Switch expanded 19-entry region table uses PC patch detailed-region oracle rows `R16428-R16446`

Important boundary:
- `ORACLE_RESOLVED` means deterministic counterpart/target routing only.
- `ORACLE_REROUTED` means the old source obligation is superseded by a stronger Switch structure and a different PC-patch occurrence family supplies the translation oracle.
- neither disposition implies `WRITE_SAFE`;
- Switch write-authorized rows created by this oracle stage = 0.

## 7. Preserved semantic overlays and rejected shortcuts

Historical semantic overlays remain evidence and are not recomputed merely because the stable family name changed.

Preserved unresolved five from historical L3:
`R651, R1062, R1277, R1283, R1284`.

`R2300` remains in S3 with its expanded-candidate re-review trigger.

Rejected oracle shortcuts:
- unique physical target + replacement agreement alone;
- full Switch object appearing elsewhere in PC patch alone;
- loose reverse-context matching;
- two-byte Korean replacement containment as hard evidence;
- sparse adjacency alone;
- direct one-to-one forcing of T1 broad-region labels;
- structural family identity as a substitute for actual counterpart resolution;
- sending all 986 or all 297 rows directly to Astra;
- consumer tracing before exhausting PC-patch oracle evidence.

## 8. Repository operating state

Permitted remote write actions are exactly:

```text
create_blob
create_tree
create_commit
update_ref(main, force=false)
```

Forbidden write actions include `update_file`, `create_file`, `delete_file`, `create_branch`, force-push, and history rewrite.

Historical write-rule violations from the prior 251 canonicalization attempt remain provenance only. The temporary files created by those noncanonical Contents-API commits were removed by canonical recovery commit `60ee3d8c9a63ae817a93e1996d0077e53c742e80`. They must not be repeated or used as precedent.

## 9. Authority and boundaries

- `PROJECT_STATE.md` is the sole resume authority.
- Verified F1 and Stage-2 affine facts are not reopened.
- Stable 986 structural membership is not reopened by the oracle overlay.
- PC Korean patch behavior is the reference before inventing Switch-specific mechanisms.
- `TARGET_RESOLVED` remains distinct from `WRITE_SAFE`.
- Framework is unchanged.
- No builder, IPS, runtime implementation, game-file modification, or new Switch write authorization is authorized.
- The exact target PC EXE remains unavailable; no new target-build PC XREF/preimage ownership claim is made.

## 10. Awaiting fresh signal

STOPPED_AWAITING_USER_SIGNAL.

Next recommended scope: `PC_PATCH_ORACLE_ASSISTED_297_FOLLOWUP` (READ_ONLY).

Recommended order:
1. S1/S2 remaining reverse-oracle closure;
2. S3 existing semantic-overlay reuse + full-object/composite evidence;
3. S5 replacement/full-object/composite narrowing;
4. T2/T3 storage/consumer ownership;
5. S4A/S4B remainder;
6. Astra only for genuinely semantic residuals;
7. consumer tracing only for structural/encoding blockers.

Do not begin the 297 follow-up, Astra work, consumer tracing, framework modification, builder/runtime work, or further repository writes without a fresh explicit signal.
