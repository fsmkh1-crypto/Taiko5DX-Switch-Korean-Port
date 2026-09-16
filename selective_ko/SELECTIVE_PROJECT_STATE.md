# SELECTIVE PROJECT STATE

Date: 2026-09-16 (KST)
Status: TAI5MSG_STRUCTURE_INDEX_MATERIALIZED / F1_STATIC_158_COMPLETE / SHARDED_PROVENANCE_MATERIALIZED / FIXED_PARTICLE_POLICY_MATERIALIZED / NO CANDIDATE / NO CORPUS CLASSIFICATION / NO BUILD
Track: `SWITCH_SELECTIVE_KOREANIZATION`

## 1. Resume authority

Repository: `fsmkh1-crypto/Taiko5DX-Switch-Korean-Port`
Branch: `main`
Target: Nintendo Switch title `0100346017304000`, game v1.1.3.

This file is the resume authority for the `selective_ko/` subtree. The repository-root `PROJECT_STATE.md` remains authority for the historical full-port track. A new chat/model is not a reason to reopen VERIFIED or already-closed evidence.

Required reads for the next selective scope:

1. `KNOWN_FAILURES.md`
2. `IDENTITY_PROVENANCE_CONTRACT.md`
3. `SWITCH_APPLICABILITY_REALIZATION_TAXONOMY.md`
4. `FIXED_PARTICLE_POLICY.md`
5. `SCRIPT_TAXONOMY_AND_CROSSCUTTING_RULES.md`
6. `PC_SOURCE_SWITCH_OWNER_ADAPTER_REPLAY_EXPANSION.md`
7. `registry/provenance_shards/INDEX.json`
8. `TAI5MSG_STRUCTURE_INDEX_MATERIALIZATION.md`
9. `artifacts/TAI5MSG_STRUCTURE_INDEX_MANIFEST.json`
10. `artifacts/tai5msg_structure_index_v1/INDEX.json`
11. this file

## 2. Product / authority boundary

The selective project is not a full clone of the PC Korean patch.

Priority Korean scope remains descriptions, event/system/context text, and structurally safe dialogue. Person/place identity, yomi/readings, calendar/name composition/input, and unresolved dynamic grammar remain Japanese or deferred unless separately promoted.

```text
translation_review_status = DEFER_TO_RUNTIME_QA
```

Authority remains:

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

## 3. Persistent registry state

Current totals:

```text
PC_SOURCE_INLINE        = 158
SWITCH_PHYSICAL_OWNER   = 158
entity IDs              = 316
BINDS_TO edges          = 158
edge IDs                = 158
artifact IDs            = 5

candidate IDs           = 0
manual task IDs         = 0
classification IDs      = 0
```

Next sequences:

```text
entity_id          = 317
edge_id            = 159
artifact_id        = 6
candidate_id       = 1
manual_task_id     = 1
classification_id = 1
```

Existing seed/F1 identities remain immutable. `ART-00000005` is the TAI5MSG structure artifact. No TAI5MSG message entity IDs were issued.

## 4. F1 static source-owner layer

Closed population:

```text
rows                     = 158
PC source entities       = 158
Switch owner entities    = 158
BINDS_TO                  = 158
shared owner count       = 0
graph cardinality        = 1:1 x 158
candidate IDs            = 0
```

Canonical F1 provenance remains sharded/indexed:

```text
index = selective_ko/registry/provenance_shards/INDEX.json
records = 158
logical bytes = 267054
aggregate SHA-256 = 7d5f753b4c1401cf89cf037d0eb3a3033573e50b47b3e90089c8a2516e38321a
virtual monolith OID = 0033877e00f7f9eab163b5329531ac4587533bc0
```

## 5. Fixed-particle policy

First-release fixed surface policy remains:

```text
은(는) / 는(은) -> 는
이(가) / 가(이) -> 가
을(를) / 를(을) -> 를
과(와) / 와(과) -> 와
(으)로 / 로(으) -> 로
```

Canonical PC TAI5MSG literal census remains:

```text
130 occurrences
70 messages
14 blocks
aggregate semantic payload delta = -520 bytes
```

The policy does not itself reclassify mechanism, applicability, realization, or release scope.

## 6. TAI5MSG deterministic structural lattice

Materialized scope:

```text
TAI5MSG_STRUCTURE_INDEX_MATERIALIZATION
artifact = ART-00000005
```

Direct inputs:

```text
PC original TAI5MSG
SHA-256 = aae037dd5948f79b9fc2e5affcb1e60e08efca39f897123045fe685786be978f

PC Korean-patched TAI5MSG
SHA-256 = e3b4522a1047ff409e099b5ee197d7689279ea7472cb403d305b2507fec96090
```

Result:

```text
blocks                         = 33
messages                       = 14,832
logical slot correspondence    = 1:1 x 14,832
insertions/deletions/reorders  = 0 / 0 / 0
locator_determinism            = PASS
```

Physical artifact:

```text
artifacts/TAI5MSG_STRUCTURE_INDEX_MANIFEST.json
artifacts/tai5msg_structure_index_v1/INDEX.json
artifacts/tai5msg_structure_index_v1/BLOCKS.jsonl
artifacts/tai5msg_structure_index_v1/messages/block-00.json
...
artifacts/tai5msg_structure_index_v1/messages/block-32.json
```

Message-shard aggregate:

```text
shards           = 33
message records  = 14,832
bytes            = 105,711
SHA-256          = bee9ef962bc5ebbba9c8d738238b63975e371ad415dd93a9aafb5c4a87a388e1
```

Structure index:

```text
SHA-256 = 63b2c12c5c101b1333833992d0c4665aae2e5d6b8ba98d59fa8aeda5c7d8639c
Git blob = f4d7f6db22938639c645e02461a96011c467de9f
```

`block_index/local_message_index` are artifact-local locators only and do not generate permanent IDs.

Final block rule:

```text
blocks 0..31 -> physical padding through declared size
block 32     -> EOF padding omitted
original declared-physical gap = 55
Korean declared-physical gap   = 34
writable capacity inference    = FORBIDDEN
```

## 7. Git failure / recovery state

All TAI5MSG resume contents-API incidents are preserved in `KNOWN_FAILURES.md`.

Baseline recovery checkpoint:

```text
commit = a683289dc520a90f3e3c132e8cf10b9e6e1a137d
tree   = c5b8416ef5764d67d3c11e48b338254b6cacac5d
TREE_EQUIVALENCE_TO_ANALYSIS = PASS
```

Incident documentation commit:

```text
commit = cd5566c31bb302cfcdb6deb3286bfad34673033e
tree   = a8c29bf77ddfec362b29456363d30ee69001e143
changed path = selective_ko/KNOWN_FAILURES.md only
```

A later repeated contents-route incident produced three additional transient commits and was forward-recovered to:

```text
commit = ce77b50e289755540e43fad9a78385d888c564e7
tree   = a8c29bf77ddfec362b29456363d30ee69001e143
TREE_EQUIVALENCE_TO_DOCUMENTATION_COMMIT = PASS
changed files relative to cd5566c31bb302cfcdb6deb3286bfad34673033e = 0
```

This materialization restores the historical technical failure sections while retaining every Git incident record.

A later pre-materialization branch drift occurred after the valid C graph-diff closure. The drift head added only two accidental root sentinel files and was forward-recovered without rewriting history:

```text
normal pre-drift commit = 12e0708e1ab601385e2a653a5c6cb31af479b16a
drift head              = 6173bc4609525516c02b398636b9b80876851c67
recovery commit         = ef1a3dbe9872f9b29ec1b39a426f847c7139c5b8
recovery tree           = 9e46f426ffd36179407602b251af25a05ad5bde2
removed paths           = __NEVER__, __SHOULD_NOT_BE_CALLED__
TREE_EQUIVALENCE_TO_NORMAL_PRE_DRIFT = PASS
```

`ef1a3dbe9872f9b29ec1b39a426f847c7139c5b8` is the materialization parent for `ART-00000005`.

Repository writes remain restricted to:

```text
create_blob -> create_tree -> create_commit -> update_ref(force=false)
```

## 8. Axis boundary

Current materialized layers emit zero:

```text
TAI5MSG message ENT IDs
candidate IDs
TAI5MSG mechanism/usage classifications
applicability rows
realization rows
release-scope decisions
work-queue rows
payload rewrites
build outputs
```

`AXIS_EVIDENCE_INDEPENDENCE = PASS` remains mandatory.

## 9. Current exclusions

Still not materialized:

- broader source-owner coverage outside F1-static-158;
- pointer/runtime T5K selective entities;
- TAI5MSG selective corpus classifications;
- permanent TAI5MSG message `ENT-*` identities;
- EVENT/TS5 structure adapter;
- rewritten TAI5MSG/EVENT payloads;
- selective TAI5MSG serializer/builder;
- IPS/build;
- translation QA.

Names/place names/yomi/name composition remain outside the initial Koreanization target.

## 10. Next planned scope

```text
TAI5MSG_SELECTIVE_MESSAGE_CLASSIFICATION_READ_ONLY
```

Consume `ART-00000005`; do not redefine TAI5MSG identity.

First partition:

```text
simple 1:1/static-variable population
vs
cross-message / nested grammar-formatter population
```

The classification stage must not auto-issue candidate IDs, applicability, realization, release scope, or build authorization.
