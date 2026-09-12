# PROJECT_STATE

Last updated: 2026-09-13 (KST)

This file is the **sole project-resume authority**. Historical documents and ledgers preserve detailed provenance but do not override this file.

<!-- PROJECT_RESUME_V2
{
  "schema": "PROJECT_RESUME_V2",
  "scope_id": "POST_FREEZE_L3_UNRESOLVED_CONSUMER_TRACING",
  "scope_kind": "READ_ONLY",
  "status": "STOPPED_AWAITING_USER_SIGNAL",
  "last_closed_validation_id": "V107",
  "last_closed_stage_commit": "ef494198345e01ea11c5b287dfb4d6e44081dde5",
  "last_closed_ci_run_id": 34691523117,
  "last_closed_ci_validation_id": "V107",
  "last_closed_ci_conclusion": "success",
  "remote_io_metrics_location": "Google Drive / GPT / 태합입지전 프로젝트 / REMOTE_IO_METRICS.jsonl",
  "ruleset_rebase_status": "COMPLETE",
  "repository_write_mode": "GIT_OBJECT_ONLY_WRITE_MODE",
  "repository_write_allowed_actions": [
    "create_blob",
    "create_tree",
    "create_commit",
    "update_ref"
  ],
  "authority_freshness_status": "COMPLETE",
  "rules_workflow_cleanup_status": "COMPLETE",
  "pre_freeze_governance_cleanup_status": "COMPLETE_V106",
  "pre_freeze_hash_pin_status": "COMPLETE_V107_CORRECTED",
  "schema_freeze_status": "FROZEN_FZ001",
  "schema_freeze_declaration_id": "FZ001",
  "schema_freeze_declaration": "data/pilot/f1_v1_candidate/schema_freeze_declaration.json",
  "schema_freeze_declaration_git_blob_sha": "6c726b7d004753e2f49f63640bd4f6df343dd736",
  "schema_freeze_basis_validation_id": "V107",
  "schema_freeze_basis_ci_run_id": 34691523117,
  "schema_freeze_basis_head": "ed0e4f2ffe8f9e1c646b96078a5c37ca57f8afea",
  "schema_freeze_implementation_commit": "ef494198345e01ea11c5b287dfb4d6e44081dde5",
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
    "data/post_freeze/forward_localization_family_partition_v1/INDEX.json",
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

## Current state

Repository: `fsmkh1-crypto/Taiko5DX-Switch-Korean-Port`  
Branch: `main`

Completed and inherited without revalidation:

- Stage 1 canonical inventory: COMPLETE
- Stage 2 affine structural targeting: COMPLETE
- F1 localization-sequence audit and V094 authorization: COMPLETE
- V094 machine-consumable transport repair: COMPLETE
- V103 structured atomic-claim closure: COMPLETE
- V104 source-anchor/provenance closure: COMPLETE
- V105 schema-v1 validation pipeline: COMPLETE
- V106 pre-freeze governance cleanup: COMPLETE
- corrected V107 four-pin semantic hash pinning: PASS
- schema-v1 freeze declaration: **FROZEN — FZ001**
- forward localization 700 exact family partition: **MATERIALIZED** (`L1=448 / L2=163 / L3=88 / L4=1`)
- L3 88 semantic/context + PC-mechanism review: **COMPLETE / MATERIALIZED** (`31 / 22 / 17 / 13 / 5`)

`FZ001` freezes the exact semantic snapshot that passed corrected V107. It is an authority-state transition only: it does not rename historical `*_candidate` paths, does not change semantic rows, and does not freeze transport evolution.

## Frozen semantic identities

Bindings: `data/pilot/f1_v1_candidate/bindings.json`  
Bindings Git blob: `20c38cbe29b5ec77848b8257ee0f4e9ae7ea5dd5`

```text
source_state         91a54c8760f84f0e5b48e25dfda8adb9ae16ff32a83a4af86275fbc0c762322c
actions              a7c0f3ce3423b2a07797ef18e538c963140303751621a985dc6fe76c52bb8a4f
source_action_edges  1399fa309889399854d68f5d89f202df0f22f7be58ec2c85e3a02342987a4fe7
effective_claims     c29751ecca3233516fd9effc850e6e961d4418e3784266175df2af59798b6d35
```

Historical V104 `effective_claims = 2cb8459c...` remains provenance only. V105+ materialization applies source-anchor overrides before effective-claim hashing, producing the frozen `c29751ec...` identity.

Freeze declaration: `data/pilot/f1_v1_candidate/schema_freeze_declaration.json`  
Freeze declaration Git blob: `6c726b7d004753e2f49f63640bd4f6df343dd736`

Freeze basis:

- machine validation: V107 / head `ed0e4f2ffe8f9e1c646b96078a5c37ca57f8afea` / run `34691523117` / release fail-fast PASS / COLLECT_ALL PASS
- pre-freeze document governance: head `3d0c02ce59cf6412085c7188df78008ba96a2442` / run `34693640232` / PASS
- freeze implementation commit: `ef494198345e01ea11c5b287dfb4d6e44081dde5`

## Canonical target and accounting

Target:

- Title ID `0100346017304000`
- Switch v1.1.3
- Build ID `D9120950C258610A746F4A31CE3A3B376DE393D9`
- canonical game `main` SHA-256 `b366e692208f3c0cc18bc1884ef95689b6b11d722fa2d749b8500abccbc3109b`

Accounting facts:

```text
historical mixed-granularity inventory records  27,430
leaf-obligation records after descriptor groups 27,419
inline rows                                      17,103
Stage-1 raw exceptions                           11,050
Stage-2 residual                                  1,248
conservative later target-resolved                  451
conservative target-unresolved residual              797
```

F1 population:

```text
DIRECT_PORT authorized                    158
PADDING_RECONSTRUCTION_REQUIRED            75
SHARED_OWNER_BINDING_REQUIRED              25
TERMINATOR_CAPACITY_FAIL                    4
F1_RULE_REJECTED                           16
TOTAL                                     278
```

The 25 shared-owner rows remain `SHARED_OWNER_BINDING`; replacement conflict is not proven.

## V094 semantic and transport identity

```text
semantic rows              158
semantic SHA-256           c612bcf55d0c139d55dee42a6a6397f702ead0f1628b47b45c46512fd1b52bff
ordered source IDs SHA     87d5a7531b5e2b3841fe4ba093a87dd9da11e8c85b5d4184c6ae705436c1833e
historical gzip SHA-256    8bbbeb03695b4bd06f028b9c9cfe0d367af170a012af56803f3a8553356a0b68
current transport          PLAIN_JSONL_SHARDS
current INDEX SHA-256      ce241ab9a3257e0cf858d4b016eebdcd3c564958e95cdaf23035c0f4dfdfd6d4
```

The historical 20-shard transport is provenance, not a future sharding precedent.

## Post-freeze forward residual records

Method baseline and status-separated claims:

- `docs/POST_FREEZE_FORWARD_RESIDUAL_ANALYSIS.txt`
- `docs/VALIDATION_LEDGER_POST_FREEZE_RESIDUAL.txt`

Canonical forward-localization family membership:

- index: `data/post_freeze/forward_localization_family_partition_v1/INDEX.json`
- index SHA-256: `6d79c648b4ee671aa4c0592467b89101de76456a5493ffaadb743014a74fdc76`
- family membership files: `L1.json`, `L2.json`, `L3.json`, `L4.json`
- inherited L1 subpartition/semantic overlay memberships: `L1_OVERLAYS.json`

Exact partition:

```text
L1 UNIQUE_FULL_JP_SINGLE_OWNER       448
L2 SHARED_PHYSICAL_JP_ALIAS          163
L3 JP_PREFIX_OF_LONGER_OBJECT         88
L4 NON_JP_LOCALIZATION_START           1
                                      ---
                                      700
intersection                           0
unclassified                           0
duplicate R-number                     0
duplicate source ID                    0
```

L1 and L2 structural results are inherited and must not be reopened merely because work moves to a new chat/model. L1 exact 399/49 mechanical subpartition and exact memberships of the reviewed 395/3/1 and 30/16/3 overlays are preserved; those semantic judgments remain PROVISIONAL and are not write authorization.

The older `docs/POST_FREEZE_FORWARD_RESIDUAL_ANALYSIS.txt` is the pre-L3 methodology/family baseline. Any statement there that L3 analysis has not started is superseded by the dedicated L3 record below and by this file.

## L3 semantic/context + PC-mechanism review

Dedicated analysis:

- `docs/L3_SEMANTIC_PC_MECHANISM_ANALYSIS.md`
- analysis document SHA-256: `59a394c6fb790d7f2a62b8e78b5fa3b30d9ea04188baff2f532667de3f0f2428`

Machine-readable overlay:

- `data/post_freeze/l3_semantic_pc_mechanism_v1/INDEX.json`
- INDEX SHA-256: `dd2ad754732d16dc05263a674c8b76d494f98baf09d71dd3c1ae2f3b1d56a33e`
- `DISPOSITIONS.json` SHA-256: `432f80f1134b24ae72df580e727acbd9c739832f9285687582f20f7af745fcbf`
- `MECHANISMS.json` SHA-256: `d35e9e4dcdf4f459bf2d9ecedabf0a4c32a95d8ee437ccee79162ed100e2e7dd`

Exact L3 review partition:

```text
PARTIAL_COMPOSITE_WINDOW          31
FORMATTER_CONTROL_PREFIX          22
CONTEXT_DIVERGENT_FALSE_PREFIX    17
STANDALONE_MEANINGFUL_PREFIX      13
UNRESOLVED                         5
                                  --
                                  88
intersection                       0
unclassified                       0
Switch write-authorized rows       0
```

Mechanism observations:

```text
PC inline L3 rows                         88
pointer-linked L3 rows                     0
multibyte-boundary split rows              7
full-zero suppression rows                 2
translated-prefix + trailing-zero rows     3
same-original/nonuniform replacement rows  4 (2 Japanese values)
```

Only `R651, R1062, R1277, R1283, R1284` remain targeted consumer/XREF tracing candidates. The other 83 have coarse semantic/context review dispositions only; they are not Switch-write authorized.

The working evidence order has now survived L1 and an independent L3 family. This supports a future framework-promotion review, but `docs/PC_TO_SWITCH_PORTING_RULE_FRAMEWORK.md` has not been modified.

These records do not reconstruct historical 467/451/797 membership.

## Repository operating state

Repository writes default to `GIT_OBJECT_ONLY_WRITE_MODE`. Permitted remote write actions are exactly:

```text
create_blob
create_tree
create_commit
update_ref(main, force=false)
```

Text blobs (`.md`, `.json`, `.jsonl`, `.yml`, `.yaml`, `.txt`, source code) are passed as original UTF-8 text. The agent must not manually generate, split, or reassemble Base64 for text. Binary payloads such as gzip require STOP and explicit route approval before any manual Base64 handling.

The accidental/non-canonical commits `84b1f6740132d0288549815c9cc1bf1769595ff0` (`__INVALID_SHOULD_NOT_USE__`), `0f2873539e54035ae45a2c5ea769de657cf56c65` (`__SHOULD_NOT_USE_AGAIN__`), and `33f4199c46917bd871baee8b1929add22f07e2fd` (`foo`) remain historical provenance only. The canonical recovery path contains none of those files. No force-push or history rewrite is used.

## Authority and boundaries

- `PROJECT_STATE.md` is the sole project-resume authority.
- Detailed validation provenance remains in canonical validation ledgers; VERIFIED facts are not reopened without a legitimate revalidation trigger.
- Frozen schema authority does not authorize full migration, builder/IPS/runtime work, mapping, or game-file modification.
- Transport remains independently versioned and may change only while preserving frozen semantic identities.
- No silent UNKNOWN authorization, source omission, or synthetic reconstruction of missing canonical rows is allowed.
- PC Korean patch behavior remains the reference for equivalent functionality before inventing Switch-specific mechanisms.
- Force-push is forbidden.

## Awaiting fresh signal

The next recommended read-only scope is **`POST_FREEZE_L3_UNRESOLVED_CONSUMER_TRACING`**, limited to the five exact rows:

```text
R651, R1062, R1277, R1283, R1284
```

A fresh explicit user signal is required before starting that scope. Alternatively, a separately authorized framework-promotion review may evaluate whether the L1+L3 evidence order should be promoted into `docs/PC_TO_SWITCH_PORTING_RULE_FRAMEWORK.md`.

Full migration, builder, IPS, runtime implementation, game-file modification, and Switch write authorization remain outside the next scope.
