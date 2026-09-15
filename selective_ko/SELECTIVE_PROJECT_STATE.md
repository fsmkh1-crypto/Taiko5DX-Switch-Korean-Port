# SELECTIVE PROJECT STATE

Date: 2026-09-15 (KST)
Status: PC_SOURCE_SWITCH_OWNER_REPLAY_EXPANSION_MATERIALIZED / F1_STATIC_158_COMPLETE / SHARDED_PROVENANCE_MATERIALIZED / FIXED_PARTICLE_POLICY_MATERIALIZED / SWITCH_APPLICABILITY_REALIZATION_TAXONOMY_MATERIALIZED / IDENTITY_PROVENANCE_CONTRACT_MATERIALIZED / NO CANDIDATE / NO CORPUS CLASSIFICATION / NO BUILD
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
6. `PC_SOURCE_SWITCH_OWNER_ADAPTER_REPLAY_EXPANSION.md`
7. `registry/provenance_shards/INDEX.json`
8. this file

## 2. Product and authority boundary

The selective project is not a full clone of the PC Korean patch.

Priority Korean scope remains descriptions, event/system/context text, and proven-safe dialogue where practical. Identity/yomi/calendar/name-composition/input and unresolved dynamic grammar may be excluded or deferred only through explicit release-scope decisions.

Translation review remains:

```text
translation_review_status = DEFER_TO_RUNTIME_QA
```

Authority model:

```text
PC Korean content/terminology             -> SOURCE_AUTHORITY
PC mapping/font source obligation         -> SOURCE_AUTHORITY
verified Switch mapping realization       -> SWITCH_RUNTIME_AUTHORITY
Switch script/control/owner/runtime       -> STRUCTURAL_AUTHORITY
known-good PC visible Korean              -> SEMANTIC_ORACLE
PC runtime mechanics                      -> REFERENCE_OR_HINT
PC workaround/defect                      -> NON_AUTHORITATIVE_EVIDENCE
```

Conflict rule:

```text
structure = Switch
content/semantic obligation = PC source/oracle
implementation = Switch-native design
```

Historical full-port WRITE_SAFE/action labels remain provenance only and do not automatically authorize selective output.

## 3. Canonical contracts

- `IDENTITY_PROVENANCE_CONTRACT.md`: opaque registry IDs, locator separation, append-only history, graph/cardinality, freshness, manual tasks, field evidence.
- `SWITCH_APPLICABILITY_REALIZATION_TAXONOMY.md`: applicability, realization/constraints, explicit release scope, derived disposition, queue accounting.
- `FIXED_PARTICLE_POLICY.md`: `FIXED_SURFACE_PARTICLE_V1`; no automatic mechanism reclassification or rewrite authority.
- `SCRIPT_TAXONOMY_AND_CROSSCUTTING_RULES.md`: mechanism/usage/investigation and caller/owner risk rules.
- `registry/provenance_shards/INDEX.json`: physical provenance-shard resolution authority for the current expanded registry.

Valid adapter state remains:

```text
candidate_id = null
candidate_status = NOT_ISSUED
```

## 4. Registry history

Initial production seed:

```text
scope  = PC_SOURCE_SWITCH_OWNER_ADAPTER_MATERIALIZATION
commit = 3ee03c11b7b608b03e3094d70f4ae056d7490f2f

PC_SOURCE_INLINE        = 8
SWITCH_PHYSICAL_OWNER   = 8
BINDS_TO                = 8
artifact IDs            = 2
candidate/manual/class  = 0
```

Seed IDs remain immutable:

```text
ENT-00000001 .. ENT-00000016
EDG-00000001 .. EDG-00000008
ART-00000001 .. ART-00000002
```

The seed entities, edges, and provenance were byte-exactly replayed before expansion.

## 5. Current F1 static replay population

Completed scopes:

```text
PC_SOURCE_SWITCH_OWNER_ADAPTER_REPLAY_EXPANSION
PROVENANCE_SHARDED_REPLAY_MATERIALIZATION
```

Declared canonical F1 input:

```text
rows                       = 158
source shards              = 20
INDEX blob                 = 479b21c8bcbaa09aaf845906179411c3cec6dafb
logical-content SHA-256    = c612bcf55d0c139d55dee42a6a6397f702ead0f1628b47b45c46512fd1b52bff
ordered-source-IDs SHA-256 = 87d5a7531b5e2b3841fe4ba093a87dd9da11e8c85b5d4184c6ae705436c1833e
```

Current registry totals:

```text
PC_SOURCE_INLINE        = 158
SWITCH_PHYSICAL_OWNER   = 158
entity IDs              = 316
BINDS_TO edges          = 158
edge IDs                = 158
artifact IDs            = 4

candidate IDs           = 0
manual task IDs         = 0
classification IDs      = 0
```

Next sequences:

```text
entity_id          = 317
edge_id            = 159
artifact_id        = 5
candidate_id       = 1
manual_task_id     = 1
classification_id = 1
```

New expansion IDs:

```text
PC source: ENT-00000017 .. ENT-00000166
Switch owner: ENT-00000167 .. ENT-00000316
edges: EDG-00000009 .. EDG-00000158
artifacts: ART-00000003 .. ART-00000004
```

## 6. Replay/cardinality result

Owner reuse is checked before new owner issuance.

Across all 158 F1 static rows, `localization_id`, `target_object`, `runtime_destination_cell`, `write_start`, and `terminator_offset` are each unique.

Therefore:

```text
shared owner count = 0
derived graph cardinality in F1-static-158 = 1:1 x 158
```

This does not change the broader contract fact that N:1 relationships are corpus-proven elsewhere.

## 7. Provenance storage

Canonical physical storage:

```text
schema       = SELECTIVE_KO_PROVENANCE_SHARD_INDEX_V1
storage_mode = SHARDED_INDEXED_V1
index        = selective_ko/registry/provenance_shards/INDEX.json
```

The original seed file remains unchanged and serves as physical shard 1:

```text
selective_ko/registry/provenance.jsonl
records = 8
Git blob = 6d1617072cb78fb2b1f3081aab5fa8562d9f59f8
```

New physical shards:

```text
selective_ko/registry/provenance_shards/F1_STATIC/part-02.jsonl
...
selective_ko/registry/provenance_shards/F1_STATIC/part-20.jsonl
```

Logical reconstruction:

```text
records              = 158
bytes                = 267054
aggregate SHA-256    = 7d5f753b4c1401cf89cf037d0eb3a3033573e50b47b3e90089c8a2516e38321a
virtual monolith OID = 0033877e00f7f9eab163b5329531ac4587533bc0
physical shards      = 20
```

`provenance_ref` is stable logical identity. Physical path resolution comes from `INDEX.json`, never from parsing the ref string.

## 8. Provenance basis and recovery equivalence

Seed provenance rows retain:

```text
commit = 2d78b64ab3a13c98e6faaf86f69ec35698be7682
tree   = a56e71f5eeef7ceb3468c397d4a28f275ac8d363
```

Expansion rows retain replay evidence basis:

```text
commit = 3ee03c11b7b608b03e3094d70f4ae056d7490f2f
tree   = bc534e7664a716c0338826206bb5934859d3bcdc
```

Actual materialization parent after Git recovery:

```text
commit = 7c722e65484193420ea0d4405c87c97350dc3624
tree   = bc534e7664a716c0338826206bb5934859d3bcdc
TREE_EQUIVALENCE = PASS
```

Recovery history does not rewrite provenance semantics.

## 9. Canonical expanded artifact identities

```text
registry/REGISTRY_STATE.json
SHA-256 = 96d02fdfbd4f2422f5c2828118274facb22356a37c5d8dd708e9acd39c32d31f
Git blob = 3bfc9f21cfab01a0ab009e60868ff240626efcbb

registry/entities.jsonl
SHA-256 = 35c986d5c9563e3b9c2df3c4d444c661034680e9359619cf4986dce01697efdf
Git blob = fc43b543850b7ced40fada89945aa89f6af5e5cf

registry/edges.jsonl
SHA-256 = d333f1369e3915e55fda212d2dc9bfc0f39f9f41283e42ff91002fb061727210
Git blob = 780410d2ed8771042a6b024647f710ffddeeba4a

registry/provenance_shards/INDEX.json
SHA-256 = 1726f00b327546096f11c3c480feafde5e3224a7a2403a85cb8dec42d2ae7845
Git blob = 261077ea6e25632ca167cf299fc1221a281cc24f

artifacts/PC_SOURCE_SWITCH_OWNER_ADAPTER_REPLAY_EXPANSION_MANIFEST.json
SHA-256 = 4d5e915ced4bc597c55ffd18a594c230f0220234ab31bff5a038c6112a797116
Git blob = a1bc5a49eb939b0abc31d864ed7c54c5ff586315

PC_SOURCE_SWITCH_OWNER_ADAPTER_REPLAY_EXPANSION.md
SHA-256 = 144a5e932924dc71e383920d8f619ca7c8af439257758a1cbaffa69649da4fa5
Git blob = 252106d1fccc72b6e50715bdafef43b67088db85
```

Individual provenance-shard identities are recorded in the shard index.

Freshness is computed, not trusted. Missing/mismatched shard/index/ref coverage or aggregate mismatch is `INVALID`.

## 10. Historical 24-edge recovery

Effective historical state remains:

```text
historical_artifact_edge_recovery = RECOVERABLE_FROM_SOURCE
exact membership recovered canonically = YES
```

Canonical evidence:

```text
recovery document blob = 12fd5f8db9df8d96ad9599f619771fb711a1623a
membership blob        = 5223f3eb6659a05d67230e5ce621d5a0beb0f025
pair-list SHA-256      = 133173ac874c64c9fda0fc40d020363e9fe2214ecba258e9602100f9432c3a5d
```

Those 24 pairs are outside this F1-static-158 population and are not auto-imported.

## 11. Fixed-particle policy

Canonical first-release surface policy remains:

```text
은(는) / 는(은) -> 는
이(가) / 가(이) -> 가
을(를) / 를(을) -> 를
과(와) / 와(과) -> 와
(으)로 / 로(으) -> 로
```

The structural `PARTICLE_SENSITIVE_INSERT` / `PARTICLE_RISK` provenance remains intact.

Canonical PC TAI5MSG read-only census remains:

```text
130 occurrences
70 messages
14 blocks
6 bytes -> 2 bytes
-4 bytes / occurrence
aggregate semantic payload delta = -520 bytes
```

No particle corpus rewrite was performed by this adapter materialization.

## 12. Applicability / realization / release-scope boundary

Current adapter registry emits zero applicability, realization, release-scope, derived-disposition, work-queue, and particle-policy classification rows.

Hard rule remains:

```text
AXIS_EVIDENCE_INDEPENDENCE = PASS required
release_scope = NOT_DECIDED
```

## 13. Current exclusions

Still not materialized:

- broader inline/Stage2/forward/gap source-owner coverage outside F1-static-158;
- pointer/runtime T5K selective entities;
- candidate IDs;
- broad mechanism/usage classifications;
- applicability/realization rows;
- release-scope decisions;
- work-queue artifacts;
- fixed-particle corpus classifications;
- TAI5MSG structure adapter;
- EVENT/TS5 structure adapter;
- rewritten TAI5MSG/EVENT payloads;
- selective builder/IPS/build;
- translation QA.

Mapping 10,036 and other inherited VERIFIED full-port facts remain closed.

## 14. Next planned structural scope

The declared F1 static source-owner registry population and its physical provenance storage are closed.

Next planned structural layer:

```text
TAI5MSG_STRUCTURE_ADAPTER
```

Future boundary:

1. consume existing canonical TAI5MSG parser/container facts rather than reopen PC runtime analysis;
2. materialize deterministic TAI5MSG message/structure identities under the registry contract;
3. keep EVENT/TS5 separate until its locator-determinism gate;
4. do not emit game rewrite/build output merely by creating structure identities;
5. use fixed-particle policy only as context until separately authorized rewrite/serializer work.

A fresh explicit user execution signal is required.
