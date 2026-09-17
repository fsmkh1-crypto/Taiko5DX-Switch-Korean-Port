# SELECTIVE PROJECT STATE

Date: 2026-09-17 (KST)
Status: V293 NEXT_SCOPE AUTHORITY RECONCILED / TAI5MSG STRUCTURE MATERIALIZED / F1 STATIC 158 COMPLETE / NO CORPUS CLASSIFICATION / NO BUILD
Track: `SWITCH_SELECTIVE_KOREANIZATION`

## 1. Resume authority

Repository: `fsmkh1-crypto/Taiko5DX-Switch-Korean-Port`
Branch: `main`
Target: Nintendo Switch title `0100346017304000`, game v1.1.3.

This file is the sole executable next-scope authority for the `SWITCH_SELECTIVE_KOREANIZATION` product track.

The repository-root `PROJECT_STATE.md` is the repository-level resume authority and routes selective work here. Historical/design/reference documents may describe sequences or old next stages, but they do not override this file.

A new chat/model is not a reason to reopen VERIFIED or already-closed evidence.

Required reads for the next selective scope:

1. `../docs/SELECTIVE_KO_NEXT_SCOPE_AUTHORITY_RECONCILIATION_V293.md`
2. `KNOWN_FAILURES.md`
3. `ARCHITECTURE.md`
4. `CLASSIFICATION_SCHEMA.md`
5. `SCRIPT_TAXONOMY_AND_CROSSCUTTING_RULES.md`
6. `IDENTITY_PROVENANCE_CONTRACT.md`
7. `SWITCH_APPLICABILITY_REALIZATION_TAXONOMY.md`
8. `FIXED_PARTICLE_POLICY.md`
9. `PC_SOURCE_SWITCH_OWNER_ADAPTER_REPLAY_EXPANSION.md`
10. `registry/provenance_shards/INDEX.json`
11. `TAI5MSG_STRUCTURE_INDEX_MATERIALIZATION.md`
12. `artifacts/TAI5MSG_STRUCTURE_INDEX_MANIFEST.json`
13. `artifacts/tai5msg_structure_index_v1/INDEX.json`
14. this file

## 2. Product / authority boundary

The selective project is not a full clone of the PC Korean patch.

Priority Korean scope remains descriptions, event/system/context text, and structurally safe dialogue. Person/place identity, yomi/readings, calendar/name composition/input, and unresolved dynamic grammar remain Japanese or deferred unless separately promoted.

```text
translation_review_status = DEFER_TO_RUNTIME_QA
```

This translation-QA deferral does not apply to unresolved product-policy decisions such as identity tokens embedded inside Korean prose.

Authority remains:

```text
PC Korean content/terminology              -> SOURCE_AUTHORITY
PC mapping/font source obligation          -> SOURCE_AUTHORITY
verified Switch mapping realization        -> SWITCH_RUNTIME_AUTHORITY
Switch script/control/owner/runtime        -> STRUCTURAL_AUTHORITY
known-good PC visible Korean               -> SEMANTIC_ORACLE
PC runtime mechanics                       -> REFERENCE_OR_HINT
PC workaround/defect                       -> NON_AUTHORITATIVE_EVIDENCE
```

Conflict rule:

```text
structure = Switch
content/semantic obligation = PC source/oracle
implementation = Switch-native design
```

## 3. Product-route exclusions and retained evidence

The following historical full-port artifacts are excluded from the selective product baseline:

```text
V290 integrated full-port builder/build = EXCLUDE_FROM_SELECTIVE_PRODUCT
V291 package                            = EXCLUDE_FROM_SELECTIVE_PRODUCT
```

V291 is retained only as historical failure / narrow diagnostic evidence. It is not a payload source or starting point for a selective release.

Separately retained:

```text
V285-V288 grammar125 analysis/manifest = OPTIONAL_R4_GRAMMAR_EVIDENCE
V289 implementation technique          = REFERENCE_ONLY
```

Do not incrementally subtract problems from V291 to create a selective product.

## 4. Persistent registry state

Current totals remain:

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

Next sequences remain:

```text
entity_id          = 317
edge_id            = 159
artifact_id        = 6
candidate_id       = 1
manual_task_id     = 1
classification_id = 1
```

Existing seed/F1 identities remain immutable. `ART-00000005` is the TAI5MSG structure artifact. No TAI5MSG message entity IDs were issued.

## 5. F1 static source-owner layer

Closed population remains:

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

These 158 bindings may be reused where the same selected source is consumed. They are not evidence of owner closure for the broader selective corpus.

## 6. Fixed-particle policy

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

These counts and byte-impact facts are TAI5MSG-specific evidence. They do not establish an equivalent census or byte contract for R1 description/UI containers, EVENT/TS5, or other containers.

The policy does not itself reclassify mechanism, applicability, realization, or release scope.

## 7. TAI5MSG deterministic structural lattice

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

Message-shard aggregate remains:

```text
shards           = 33
message records  = 14,832
bytes            = 105,711
SHA-256          = bee9ef962bc5ebbba9c8d738238b63975e371ad415dd93a9aafb5c4a87a388e1
```

Structure index remains:

```text
SHA-256 = 63b2c12c5c101b1333833992d0c4665aae2e5d6b8ba98d59fa8aeda5c7d8639c
Git blob = f4d7f6db22938639c645e02461a96011c467de9f
```

`block_index/local_message_index` are artifact-local locators only and do not generate permanent IDs.

Final block rule remains:

```text
blocks 0..31 -> physical padding through declared size
block 32     -> EOF padding omitted
original declared-physical gap = 55
Korean declared-physical gap   = 34
writable capacity inference    = FORBIDDEN
```

### V293 authority clarification

`ART-00000005` is a PC-original <-> PC-Korean locator/length structure lattice.

It does not by itself contain or prove:

- decoded payload semantics;
- opcode/call structure;
- append/formatter responsibility;
- Switch physical-owner mapping;
- Switch caller topology;
- release disposition.

Its 1:1 x 14,832 correspondence must not be described as a proven complete PC-to-Switch mapping.

## 8. Axis boundary

Current materialized layers still emit zero:

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

Source/mechanism inventory may proceed where evidence exists, but release inclusion remains unresolved until required owner/caller/applicability/capacity gates close.

## 9. Open product-policy / dependency constraints

### 9.1 Identity-in-prose

Identity fields remain Japanese by default, but Korean explanatory/narrative source may contain Korean person/place names as prose literals.

Current status:

```text
identity_in_prose_policy = UNRESOLVED_PRODUCT_DECISION
```

This must be decided before R1 release materialization depends on affected prose. It is not ordinary translation polish and must not be deferred only to runtime QA.

### 9.2 Mixed-script route safety

Historical runtime evidence shows at least one route can render Japanese and Korean together. This does not prove all selective routes safe.

For any selected family emitting mixed Japanese/Korean text, mapping/font/transport behavior must preserve both scripts on that actual route.

### 9.3 Container/adapter availability

Still not materialized:

- a cross-container inventory of which files/source families own R1/R2/R3 content;
- broader source-owner coverage outside F1-static-158;
- pointer/runtime T5K selective entities;
- TAI5MSG selective corpus classifications;
- permanent TAI5MSG message `ENT-*` identities;
- EVENT/TS5 production structure adapter;
- R1 description/UI structure adapters where needed;
- rewritten TAI5MSG/EVENT/UI payloads;
- selective serializers/builders;
- IPS/build;
- translation QA.

## 10. Executable next scope — sole authority

The exact next selective scope is:

```text
SELECTIVE_KO_CONTENT_CONTAINER_AND_FIELD_AVAILABILITY_READ_ONLY
```

Purpose:

1. identify the source families/containers that actually own R1 descriptions/UI, R2 event/system context, and R3 dialogue candidates;
2. record per family/container which common classification fields are machine-extractable, manually decidable, or currently unavailable;
3. record current Switch owner/caller coverage per family;
4. bind reusable parsers, structure indices, and owner ledgers;
5. sample/measure identity-in-prose exposure sufficiently to support the later product-policy decision;
6. identify whether TAI5MSG, EVENT/TS5, UI/description tables, or other containers are required for each release phase.

This scope is READ ONLY inventory/availability analysis.

It must not:

- create broad corpus classification rows;
- issue candidate/classification IDs;
- assign corpus dispositions;
- decide the final identity-in-prose policy;
- mutate gameplay data;
- implement serializers/builders;
- create IPS/build/runtime artifacts.

A fresh explicit user execution signal is required before this scope begins.

## 11. Repository write boundary

Repository writes remain restricted to:

```text
create_blob -> create_tree -> create_commit -> update_ref(force=false)
```

No Contents-API writes, branch creation, or force update are permitted.
