# PROJECT_STATE

Last updated: 2026-09-13 (KST)

This file is the sole project-resume authority. Historical documents/ledgers preserve provenance but do not override this file.

<!-- PROJECT_RESUME_V2
{
  "schema": "PROJECT_RESUME_V2",
  "scope_id": "POST_FREEZE_FORWARD_STRUCTURAL_CENSUS_251",
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
    "docs/POST_FREEZE_FORWARD_RESIDUAL_ANALYSIS.txt",
    "docs/VALIDATION_LEDGER_POST_FREEZE_RESIDUAL.txt",
    "docs/CAP64_FORWARD_CORRECTION.md",
    "docs/VALIDATION_LEDGER_CAP64_CORRECTION.txt",
    "data/post_freeze/forward_localization_raw_start_partition_v2/INDEX.json",
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
- PC DLL/runtime mechanics already closed in canonical runtime documents
- historical forward-localization partition v1 and L3 88-row review remain provenance

Current correction:

- CAP64 root-cause audit: COMPLETE
- corrected raw-start partition v2: MATERIALIZED
- historical v1 completeness claim: SUPERSEDED
- historical L4=R1291 claim: RETRACTED
- next scope: joint structural census of the remaining 251 legacy residual labels

## 2. Frozen semantic identities

FZ001 semantic bindings remain unchanged:

```text
source_state         91a54c8760f84f0e5b48e25dfda8adb9ae16ff32a83a4af86275fbc0c762322c
actions              a7c0f3ce3423b2a07797ef18e538c963140303751621a985dc6fe76c52bb8a4f
source_action_edges  1399fa309889399854d68f5d89f202df0f22f7be58ec2c85e3a02342987a4fe7
effective_claims     c29751ecca3233516fd9effc850e6e961d4418e3784266175df2af59798b6d35
```

CAP64 correction does not reopen these frozen F1 semantic identities.

## 3. Canonical target and accounting

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

## 4. CAP64 correction — current authority

Canonical correction document:

- `docs/CAP64_FORWARD_CORRECTION.md`
- SHA-256 `71b122a2f9b3ca83c76a1f8e7a3eaf59e60234a10d14e4b1d6a1c272641d2c0d`

Correction ledger:

- `docs/VALIDATION_LEDGER_CAP64_CORRECTION.txt`
- SHA-256 `053b6d3405d8cd89649ea9b8fde10ec26b41e60536bca99892886350cc609147`

Machine-readable corrected raw-start artifact:

- `data/post_freeze/forward_localization_raw_start_partition_v2/INDEX.json`
- SHA-256 `7134f9df08d6541d099bf0bf6dd305fc6232967910ef5ecb2818923da46ae4fc`

The historical artifact `data/post_freeze/forward_localization_family_partition_v1/` is retained unchanged for provenance, but its claim of complete/current 700-row coverage is superseded.

### 4.1 Censorship rule

`switch_raw_candidate_count_capped_64 == 64` means `actual candidate count >= 64`; it is not an exact count.

A capped candidate list must not be used to prove:

- absence beyond the stored candidates;
- uniqueness/cardinality;
- complete language-domain coverage;
- complete storage-mutability coverage.

### 4.2 Corrected raw-start census

The corrected raw-start relation is:

```text
L1 UNIQUE_FULL_JP_SINGLE_OWNER       454
L2 SHARED_PHYSICAL_JP_ALIAS          165
L3 JP_PREFIX_OF_LONGER_OBJECT        116
L4 NON_JP_LOCALIZATION_START           0
                                      ---
                                      735
```

Legacy forward labels after this one root-cause correction:

```text
raw-start localization relation      735
legacy residual-other                216
legacy formatter                      35
                                      ---
                                      986
```

The 216 and 35 are NOT final structural families. The next analysis population is their joint 251 rows.

Thirty-five exact forward rows move from the legacy unclassified bucket into the corrected raw-start relation. R1291 moves from historical L4 into corrected L3.

### 4.3 Historical semantic overlays after correction

- Existing L1 overlays remain scoped to the original L1 448 only. The six added L1 rows have not received semantic/context review.
- `data/post_freeze/l3_semantic_pc_mechanism_v1/` remains a valid review of its original 88-row parent only.
- Corrected L3 parent count is 116, so the old 88-row review is incomplete for the current parent.
- R2300 has a legitimate re-review trigger because its uncapped JP-prefix candidate set expanded.
- The prior five L3 unresolved rows remain unresolved within the original 88-row review.
- No CAP64 correction row is Switch-write authorized by this correction.

## 5. Next-scope trigger: residual 251

A read-only precheck observed 79 additional JP logical relations inside the remaining 251 legacy residual labels after logical-window normalization, all involving PC originals with NUL + zero padding.

This 79-row observation is PROVISIONAL only. Its exact membership is intentionally not canonicalized yet.

Therefore the next authorized analytical scope is:

**`POST_FREEZE_FORWARD_STRUCTURAL_CENSUS_251`**

Required order:

1. treat all 251 rows as one census population;
2. do not preserve `216 unclassified` and `35 formatter` as final families;
3. test logical full match, shared owner, prefix/composite, padding/boundary, containment/adjacency, table/storage structure;
4. form stable structural families first;
5. perform semantic/context auditing only after the population is structurally stable;
6. consumer tracing remains last resort.

## 6. Repository operating state

Repository writes use `GIT_OBJECT_ONLY_WRITE_MODE`.

Permitted remote write actions are exactly:

```text
create_blob
create_tree
create_commit
update_ref(main, force=false)
```

Forbidden write actions include `update_file`, `create_file`, `delete_file`, `create_branch`, force-push, and history rewrite.

## 7. Authority and boundaries

- `PROJECT_STATE.md` is the sole resume authority.
- Verified F1 and Stage-2 affine facts are not reopened by CAP64 correction.
- Historical artifacts remain provenance; supersession does not delete history.
- The corrected 735 is a raw-start relation partition, not the final forward localization taxonomy.
- The 251 residual rows must be structurally censused before further deep semantic auditing.
- `TARGET_RESOLVED` remains distinct from `WRITE_SAFE`.
- PC Korean patch behavior remains the reference before inventing Switch-specific mechanisms.
- No full migration, builder, IPS, runtime implementation, game-file modification, or Switch write authorization is currently authorized.

## 8. Awaiting fresh signal

STOPPED_AWAITING_USER_SIGNAL.

Next recommended scope: read-only structural census of the exact 251-row legacy residual-label population.

Do not begin semantic review, framework modification, builder/runtime work, or repository writes without a fresh explicit signal.
