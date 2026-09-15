# PC SOURCE / SWITCH OWNER ADAPTER REPLAY EXPANSION

Date: 2026-09-15 (KST)
Status: CANONICAL PRODUCTION REGISTRY REPLAY EXPANSION / F1 STATIC 158-ROW DECLARED POPULATION COMPLETE / SHARDED PROVENANCE / NO CANDIDATE / NO CLASSIFICATION / NO BUILD
Track: `SWITCH_SELECTIVE_KOREANIZATION`
Scope: `PROVENANCE_SHARDED_REPLAY_MATERIALIZATION`

## 1. Purpose

This scope materializes the already-validated 158-row F1 static source/owner replay while preserving every previously issued registry ID and replacing the blocked monolithic provenance transport with an indexed append-only shard layout.

It does not rerun `dinput8.dll` analysis, F1 target discovery, semantic-owner discovery, write-safety analysis, candidate issuance, applicability/realization/release-scope classification, TAI5MSG/EVENT work, builder changes, IPS generation, or a runtime build.

## 2. Replay evidence basis and materialization parent

Replay evidence was produced against:

```text
commit = 3ee03c11b7b608b03e3094d70f4ae056d7490f2f
tree   = bc534e7664a716c0338826206bb5934859d3bcdc
```

After an unrelated Git forward-recovery, materialization starts from:

```text
parent commit = 7c722e65484193420ea0d4405c87c97350dc3624
parent tree   = bc534e7664a716c0338826206bb5934859d3bcdc
```

The trees are identical:

```text
TREE_EQUIVALENCE = PASS
```

Therefore the 158-row replay evidence and ID issuance are reused without recomputation or renumbering.

## 3. Replay result

```text
PC_SOURCE_INLINE        = 158
SWITCH_PHYSICAL_OWNER   = 158
entity IDs              = 316

BINDS_TO edges          = 158
edge IDs                = 158

artifact IDs            = 4
  seed                   = ART-00000001 .. ART-00000002
  replay expansion       = ART-00000003 .. ART-00000004

candidate IDs           = 0
manual task IDs         = 0
classification IDs      = 0
```

Existing IDs remain byte-for-byte replay-stable:

```text
ENT-00000001 .. ENT-00000016    unchanged
EDG-00000001 .. EDG-00000008    unchanged
```

New IDs are append-only:

```text
PC source entities      ENT-00000017 .. ENT-00000166
Switch owner entities   ENT-00000167 .. ENT-00000316
binding edges           EDG-00000009 .. EDG-00000158
```

## 4. Owner-dedup/cardinality result

Owner reuse was checked before issuance across `localization_id`, `target_object`, `runtime_destination_cell`, `write_start`, and `terminator_offset`.

```text
manifest rows       = 158
unique owners       = 158
shared owner count  = 0
cardinality         = 1:1 x 158
```

This population contains no new N:1 binding. The broader identity contract statement that N:1 is corpus-proven elsewhere remains unchanged.

## 5. Sharded provenance storage

Canonical storage schema:

```text
schema       = SELECTIVE_KO_PROVENANCE_SHARD_INDEX_V1
storage_mode = SHARDED_INDEXED_V1
```

The existing seed provenance file remains unchanged and acts as physical shard 1:

```text
selective_ko/registry/provenance.jsonl
records  = 8
Git blob = 6d1617072cb78fb2b1f3081aab5fa8562d9f59f8
```

New physical shards follow the source F1 shard boundaries exactly:

```text
selective_ko/registry/provenance_shards/F1_STATIC/part-02.jsonl
...
selective_ko/registry/provenance_shards/F1_STATIC/part-20.jsonl
```

The physical location authority is:

```text
selective_ko/registry/provenance_shards/INDEX.json
```

`provenance_ref` remains the stable logical reference. Consumers must use the index to resolve physical storage; they must not infer file paths by parsing a provenance-ref string.

The index records every shard's source-manifest identity, source line range, first/last provenance ref, row count, byte count, SHA-256, and Git blob.

Logical reconstruction over shard ordinal and file line order is byte-identical to the validated 158-line monolith:

```text
logical records        = 158
logical bytes          = 267054
logical SHA-256        = 7d5f753b4c1401cf89cf037d0eb3a3033573e50b47b3e90089c8a2516e38321a
virtual monolith OID   = 0033877e00f7f9eab163b5329531ac4587533bc0
physical shards        = 20
new physical shards    = 19
```

No new persistent shard-ID namespace is introduced. Shards are artifact storage components, not semantic entities.

## 6. Provenance-history rule

The original first eight records retain their seed materialization basis:

```text
commit = 2d78b64ab3a13c98e6faaf86f69ec35698be7682
tree   = a56e71f5eeef7ceb3468c397d4a28f275ac8d363
```

Rows 9..158 retain the replay evidence basis:

```text
commit = 3ee03c11b7b608b03e3094d70f4ae056d7490f2f
tree   = bc534e7664a716c0338826206bb5934859d3bcdc
```

Forward-recovery history does not rewrite earlier provenance.

## 7. Freshness and validity

Creation-time `FRESH` is not authority.

A consumer recomputes against:

- the F1 INDEX identity;
- all 20 canonical F1 shard identities;
- registry history;
- the identity/provenance contract;
- `provenance_shards/INDEX.json`;
- every shard hash declared by that index.

The sharded provenance artifact is `INVALID` if any shard is missing, any shard hash mismatches, any provenance ref is missing/duplicated, the index is inconsistent, or logical reconstruction does not match the aggregate hash.

## 8. Validation gates

```text
F1 rows replayed                         158 PASS
F1 source shards                          20 PASS
provenance physical shards                20 PASS
new provenance shards                     19 PASS
logical provenance refs                  158 PASS
logical aggregate reconstruction              PASS

entity IDs unique                    316/316 PASS
edge IDs unique                      158/158 PASS
all edge endpoints exist                  PASS
source BINDS_TO degree            1 x 158 PASS
owner BINDS_TO degree             1 x 158 PASS

seed entity prefix byte-identical          PASS
seed edge prefix byte-identical            PASS
seed provenance physical shard unchanged   PASS
issued IDs renumbered                         0 PASS

candidate IDs issued                          0 PASS
manual task IDs issued                        0 PASS
classification IDs issued                     0 PASS
applicability rows emitted                    0 PASS
realization rows emitted                      0 PASS
release-scope decisions emitted               0 PASS
work-queue rows emitted                       0 PASS

TAI5MSG adapter started                   false PASS
EVENT/TS5 adapter started                 false PASS
builder modified                          false PASS
build produced                            false PASS
```

## 9. Canonical output identities

```text
REGISTRY_STATE.json
SHA-256 = 96d02fdfbd4f2422f5c2828118274facb22356a37c5d8dd708e9acd39c32d31f
Git blob = 3bfc9f21cfab01a0ab009e60868ff240626efcbb

entities.jsonl
SHA-256 = 35c986d5c9563e3b9c2df3c4d444c661034680e9359619cf4986dce01697efdf
Git blob = fc43b543850b7ced40fada89945aa89f6af5e5cf

edges.jsonl
SHA-256 = d333f1369e3915e55fda212d2dc9bfc0f39f9f41283e42ff91002fb061727210
Git blob = 780410d2ed8771042a6b024647f710ffddeeba4a

provenance_shards/INDEX.json
SHA-256 = 1726f00b327546096f11c3c480feafde5e3224a7a2403a85cb8dec42d2ae7845
Git blob = 261077ea6e25632ca167cf299fc1221a281cc24f

PC_SOURCE_SWITCH_OWNER_ADAPTER_REPLAY_EXPANSION_MANIFEST.json
SHA-256 = 4d5e915ced4bc597c55ffd18a594c230f0220234ab31bff5a038c6112a797116
Git blob = a1bc5a49eb939b0abc31d864ed7c54c5ff586315
```

Individual provenance-shard identities are authoritative in `provenance_shards/INDEX.json`.

## 10. Rejected shortcuts

Rejected:

1. retry the 267 KB monolithic transport;
2. require Base64 to move provenance;
3. move or rewrite the existing seed `provenance.jsonl`;
4. renumber existing entity/edge IDs;
5. derive physical shard path from `provenance_ref`;
6. create a persistent shard-ID namespace;
7. treat historical `DIRECT_PORT` as selective `DIRECT_DATA`;
8. issue candidates from source-owner binding alone;
9. infer applicability, realization, or release scope from F1 static authorization;
10. mix TAI5MSG/EVENT/build work into this materialization.

## 11. Boundary

This closes source/owner registry materialization for the declared canonical F1 static 158-row population with indexed sharded provenance.

Broader inline/Stage2/forward/gap/pointer/runtime-T5K source families remain outside this closure.

The next planned selective structural layer remains `TAI5MSG_STRUCTURE_ADAPTER`, subject to a fresh explicit user execution signal.
