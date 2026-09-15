# SELECTIVE PROJECT STATE

Date: 2026-09-15 (KST)
Status: PC_SOURCE_SWITCH_OWNER_PRODUCTION_REGISTRY_SEED_MATERIALIZED / FIXED_PARTICLE_POLICY_MATERIALIZED / SWITCH_APPLICABILITY_REALIZATION_TAXONOMY_MATERIALIZED / IDENTITY_PROVENANCE_CONTRACT_MATERIALIZED / NO CANDIDATE / NO CORPUS CLASSIFICATION / NO BUILD
Track: `SWITCH_SELECTIVE_KOREANIZATION`

## 1. Resume authority

Repository: `fsmkh1-crypto/Taiko5DX-Switch-Korean-Port`
Branch: `main`
Target: Nintendo Switch title `0100346017304000`, game v1.1.3.

This file is the resume authority for the `selective_ko/` subtree. The repository-root `PROJECT_STATE.md` remains authority for the historical full-port track.

A new chat/model is not a reason to reopen VERIFIED or already-closed evidence.

Required reads for the next selective scope:

1. `IDENTITY_PROVENANCE_CONTRACT.md`
2. `SWITCH_APPLICABILITY_REALIZATION_TAXONOMY.md`
3. `FIXED_PARTICLE_POLICY.md`
4. `SCRIPT_TAXONOMY_AND_CROSSCUTTING_RULES.md`
5. `PC_SOURCE_SWITCH_OWNER_ADAPTER_MATERIALIZATION.md`
6. this file

## 2. Product target

The selective product target is not a complete clone of the PC Korean patch.

Priority Korean scope remains:

- character/person descriptions;
- region/location descriptions while place names may remain Japanese;
- tools/items descriptions;
- techniques/skills descriptions;
- event narration/body/system/context text;
- static or otherwise proven-safe dialogue where practical.

Identity/yomi/calendar/name-composition/input and unresolved dynamic grammar may be excluded or deferred, but that remains a product decision until explicit `release_scope` materialization.

Translation quality review remains:

```text
translation_review_status = DEFER_TO_RUNTIME_QA
```

## 3. Authority model

```text
PC Korean content/terminology             -> SOURCE_AUTHORITY
PC mapping/font source obligation         -> SOURCE_AUTHORITY
verified Switch mapping realization       -> SWITCH_RUNTIME_AUTHORITY
Switch script/control/owner/runtime       -> STRUCTURAL_AUTHORITY
known-good PC visible Korean              -> SEMANTIC_ORACLE (observed context only)
PC runtime mechanics                      -> REFERENCE_OR_HINT
PC workaround/defect                      -> NON_AUTHORITATIVE_EVIDENCE
```

Conflict rule:

```text
structure = Switch
content/semantic obligation = PC source/oracle
implementation = Switch-native design
```

Existing full-port WRITE_SAFE or historical action labels do not automatically authorize selective output.

## 4. Canonical contracts

- `SCRIPT_TAXONOMY_AND_CROSSCUTTING_RULES.md`
  - mechanism/usage/investigation taxonomy;
  - caller/owner/risk/mechanism-decision rules.
- `IDENTITY_PROVENANCE_CONTRACT.md`
  - registry-issued opaque IDs;
  - native-locator separation;
  - append-only supersession;
  - edge graph/cardinality;
  - artifact freshness;
  - manual tasks;
  - field evidence.
- `SWITCH_APPLICABILITY_REALIZATION_TAXONOMY.md`
  - applicability;
  - realization/constraints;
  - explicit release scope;
  - derived disposition bridge;
  - total work-queue accounting.
- `FIXED_PARTICLE_POLICY.md`
  - `FIXED_SURFACE_PARTICLE_V1`;
  - approved fixed allomorph forms;
  - narrow investigation-relief boundary;
  - TAI5MSG shrink-only byte-impact contract;
  - EVENT/TS5 no-rewrite boundary.
- `EVENT_EXTRACTION_SCHEMA.md`
  - event-specific structural metadata only.

Persistent IDs are registry-issued opaque IDs. Registry loss is canonical-data loss.

Valid normal adapter state:

```text
candidate_id = null
candidate_status = NOT_ISSUED
```

## 5. Current production registry seed

Completed materialization scope:

```text
PC_SOURCE_SWITCH_OWNER_ADAPTER_MATERIALIZATION
```

Canonical files:

```text
registry/REGISTRY_STATE.json
registry/entities.jsonl
registry/edges.jsonl
registry/provenance.jsonl
artifacts/PC_SOURCE_SWITCH_OWNER_ADAPTER_MANIFEST.json
PC_SOURCE_SWITCH_OWNER_ADAPTER_MATERIALIZATION.md
```

Initial issued IDs:

```text
entity_id         16
  PC_SOURCE_INLINE        8
  SWITCH_PHYSICAL_OWNER   8

edge_id            8
  BINDS_TO                8

artifact_id        2
  PC_SOURCE_ADAPTER       1
  SWITCH_OWNER_ADAPTER    1

candidate_id       0
manual_task_id     0
classification_id  0
```

Seed cohort is exactly the first canonical F1 static-authorization shard:

```text
R36
R103
R128
R136
R137
R138
R139
R140
```

It is intentionally non-exhaustive.

All row facts are consumed from the already-canonical F1 manifest. No `dinput8.dll`, F1 selector, Switch target discovery, semantic-owner analysis, or write-safety analysis was rerun.

Candidates, mechanism/usage classifications, applicability, realization, release-scope decisions, derived dispositions, work queues, and particle-policy classifications emitted by this materialization: **0**.

## 6. Production artifact identity and freshness

Materialization run provenance before commit:

```text
basis commit = 2d78b64ab3a13c98e6faaf86f69ec35698be7682
basis tree   = a56e71f5eeef7ceb3468c397d4a28f275ac8d363
```

Direct immutable adapter inputs:

```text
F1 index blob
479b21c8bcbaa09aaf845906179411c3cec6dafb

F1 seed shard blob
235ca401ca313369b90b76e710fcc0329312a716

F1 seed shard semantic SHA-256
0c57bf4da934b20fe93ccf39aed0fb0aba6d6d6b9c7ab82dbff778d84e33776b

identity/provenance contract blob
da67fff27e6845bb29e728c41ebb763553512bac
```

Context-only canonical policy identities:

```text
applicability/realization taxonomy blob
9813ea91ff5bb8e331b5da721219e15713480fe8

fixed-particle policy blob
36d6a1530bc96b40a00b96d64dd6173aab834ef5
```

Freshness is recomputed; stored creation-time `FRESH` is not authority.

Current output SHA-256:

```text
REGISTRY_STATE.json
ce29f06b99f6de6a2fcfd8d560a28f1e2616c630316371e2aea3936048620496

entities.jsonl
90fd30dfe2b9d14e8caecc0f6f9b65c2281a91bca48db219f11e78221c73aab9

edges.jsonl
0b792990e5cc0dc62c0daebeb63d9774729001ca747220042792ba72f5b055b6

provenance.jsonl
36ff55b27497618b632ec914d99fff9607cfcb903264dd84510f42b1403c14c2

PC_SOURCE_SWITCH_OWNER_ADAPTER_MANIFEST.json
b2cca41f1efed7399709e08dc953059660df123ccc1c6e9ccf3bdf4eadaf9844
```

## 7. Historical 24-edge provenance correction

The old identity-contract placeholder for the known gap-internal 24 exact memberships is superseded on the provenance axis by canonical recovery evidence.

Canonical recovery:

```text
docs/INLINE_GAP_INTERNAL_24_EDGE_PROVENANCE_RECOVERY.md
blob = 12fd5f8db9df8d96ad9599f619771fb711a1623a

data/post_freeze/inline_gap_internal_24_edge_provenance_recovery_v1/MEMBERSHIP.json
blob = 5223f3eb6659a05d67230e5ce621d5a0beb0f025

pair-list SHA-256
133173ac874c64c9fda0fc40d020363e9fe2214ecba258e9602100f9432c3a5d
```

Effective state:

```text
historical_artifact_edge_recovery = RECOVERABLE_FROM_SOURCE
exact membership recovered canonically = YES
selective-registry import in current seed = NO
```

The recovered set contains 24 pair units. One pair overlaps the historical exact cross-boundary graph, so the recovery evidence records 23 additional reductions when composed with that graph.

No write authority changes.

## 8. Fixed-particle release policy

Canonical policy:

```text
particle_release_policy = FIXED_SURFACE_PARTICLE
particle_release_policy_version = FIXED_SURFACE_PARTICLE_V1
```

Approved first-release forms:

```text
은(는) / 는(은) -> 는
이(가) / 가(이) -> 가
을(를) / 를(을) -> 를
과(와) / 와(과) -> 와
(으)로 / 로(으) -> 로
```

Applicability is limited to explicit dual-form literals or separately proven particle-only selector leaves. Ordinary Korean particles are never globally substituted.

The structural `PARTICLE_SENSITIVE_INSERT` mechanism and `PARTICLE_RISK` provenance remain intact.

This policy does not automatically determine:

- owner/caller topology;
- Switch applicability;
- Switch realization;
- release scope;
- capacity/terminator safety;
- copula/ending/register/interrogative formatters;
- numeric-counter morphology;
- cross-message composition.

Canonical PC TAI5MSG read-only census remains:

```text
130 occurrences
70 messages
14 blocks
6 bytes -> 2 bytes
-4 bytes / occurrence
aggregate semantic payload delta = -520 bytes
```

TAI5MSG rewrite and EVENT/TS5 rewrite remain unimplemented and unauthorized in the current registry seed.

## 9. Applicability / realization / release-scope boundary

Applicability values:

```text
EXACT_COUNTERPART
EQUIVALENT_COUNTERPART
COMPOSITE_COUNTERPART
NO_SWITCH_COUNTERPART
COUNTERPART_UNKNOWN
```

Realization values:

```text
DIRECT_DATA
OBJECT_RECONSTRUCTION
REDIRECT_PORT
SWITCH_NATIVE_RUNTIME_EQUIVALENT
EXISTING_NATIVE_BEHAVIOR
REALIZATION_UNRESOLVED
```

Hard rule:

```text
AXIS_EVIDENCE_INDEPENDENCE = PASS required
```

Historical full-port action labels are evidence only and never direct selective values.

Release-scope default:

```text
release_scope = NOT_DECIDED
```

Other values require explicit decision provenance.

Work queue is derived and must satisfy:

```text
QUEUE_UNASSIGNED = 0
```

`QUEUE_RULE_GAP` is a routing-rule defect tracked separately from ordinary investigation backlog.

## 10. Current exclusions and remaining coverage

Still not materialized:

- remaining 150 F1 static rows;
- broader F1/Stage2/forward/gap PC-source and Switch-owner registry coverage;
- pointer/runtime T5K source entities;
- candidate IDs;
- broad mechanism/usage classifications;
- applicability/realization rows;
- release-scope decisions;
- work-queue artifacts;
- fixed-particle corpus classifications;
- TAI5MSG structure adapter;
- EVENT/TS5 structure adapter;
- TAI5MSG or EVENT rewritten payloads;
- selective builder/IPS/build;
- translation QA.

Mapping 10,036 and other inherited VERIFIED full-port facts remain closed and are not reopened by this state.

## 11. Next scope

Recommended next scope:

```text
PC_SOURCE_SWITCH_OWNER_ADAPTER_REPLAY_EXPANSION
```

Purpose:

1. read the current registry as an input;
2. consume remaining READY canonical PC-source/Switch-owner evidence;
3. append IDs/edges without renumbering any issued ID;
4. validate append-only replay and freshness;
5. keep `candidate_id` unissued by default;
6. do not broadly classify mechanism/applicability/realization/release scope;
7. do not start TAI5MSG/EVENT/build work in the same scope.

After that scope report: STOP and require a fresh explicit user execution signal.
