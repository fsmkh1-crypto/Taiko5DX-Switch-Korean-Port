# TAI5MSG STRUCTURE INDEX MATERIALIZATION

Date: 2026-09-16 (KST)
Status: CANONICAL MATERIALIZATION PAYLOAD
Scope: `TAI5MSG_STRUCTURE_INDEX_MATERIALIZATION`
Artifact ID: `ART-00000005`

## PC_PATCH_ORACLE_GATE

`PASS`

This scope consumes already-verified PC TAI5MSG/parser/container evidence. It does not reopen `dinput8.dll` or PC runtime reverse engineering.

Direct inputs:

```text
PC original TAI5MSG
SHA-256 = aae037dd5948f79b9fc2e5affcb1e60e08efca39f897123045fe685786be978f
size    = 1,810,889

PC Korean-patched TAI5MSG
SHA-256 = e3b4522a1047ff409e099b5ee197d7689279ea7472cb403d305b2507fec96090
size    = 2,134,366
```

Analysis basis and recovery:

```text
analysis commit = 1800177201731178b64bc8b9515bdd3fdd86e579
analysis tree   = c5b8416ef5764d67d3c11e48b338254b6cacac5d

baseline recovery commit = a683289dc520a90f3e3c132e8cf10b9e6e1a137d
baseline recovery tree   = c5b8416ef5764d67d3c11e48b338254b6cacac5d
TREE_EQUIVALENCE_TO_ANALYSIS = PASS

incident documentation commit = cd5566c31bb302cfcdb6deb3286bfad34673033e
incident documentation tree   = a8c29bf77ddfec362b29456363d30ee69001e143
delta from baseline recovery   = selective_ko/KNOWN_FAILURES.md only

latest contents-incident recovery commit = ce77b50e289755540e43fad9a78385d888c564e7
latest contents-incident recovery tree   = a8c29bf77ddfec362b29456363d30ee69001e143
TREE_EQUIVALENCE_TO_DOCUMENTATION_COMMIT = PASS

materialization parent commit = ef1a3dbe9872f9b29ec1b39a426f847c7139c5b8
materialization parent tree   = 9e46f426ffd36179407602b251af25a05ad5bde2
```

## 확정된 사실

```text
blocks                       = 33
messages                     = 14,832
logical slot correspondence  = 1:1 x 14,832
insertions                    = 0
deletions                     = 0
reorders                      = 0
locator_determinism           = PASS
```

`block_index + local_message_index` is an artifact-local locator only. No permanent message `ENT-*`, edge, candidate, classification, manual-task, applicability, realization, or release-scope rows are created here.

Canonical physical representation:

```text
selective_ko/artifacts/TAI5MSG_STRUCTURE_INDEX_MANIFEST.json
selective_ko/artifacts/tai5msg_structure_index_v1/INDEX.json
selective_ko/artifacts/tai5msg_structure_index_v1/BLOCKS.jsonl
selective_ko/artifacts/tai5msg_structure_index_v1/messages/block-00.json
...
selective_ko/artifacts/tai5msg_structure_index_v1/messages/block-32.json
```

Each message shard stores `message_count`, `table_end`, and ordered original/Korean message-length arrays. Exact message boundary `m` is reconstructed by prefix sum from `table_end`.

Storage identities:

```text
message shards        = 33
message records       = 14,832
aggregate bytes       = 105,711
aggregate SHA-256     = bee9ef962bc5ebbba9c8d738238b63975e371ad415dd93a9aafb5c4a87a388e1

BLOCKS SHA-256        = 347368773a54321654c4ccc7892c5896bd6cb5071282d87c280f8405add593f6
BLOCKS Git blob       = 47d9ace6323a511da8700fcf664d1b0c7233a6dc

INDEX SHA-256         = 63b2c12c5c101b1333833992d0c4665aae2e5d6b8ba98d59fa8aeda5c7d8639c
INDEX Git blob        = f4d7f6db22938639c645e02461a96011c467de9f

manifest SHA-256      = a434ba5ca5e4cf37ca400de81c1b5d53aa1bd5eac2d9925c0d7e24ec65aaa655
manifest Git blob       = 932047a3a9e0a1d562d86d8d767b7a3a0b52d39d
```

All 14,832 original/Korean slots replay-validate against the canonical input hashes.

Final-block behavior is explicit: blocks 0..31 are physically padded through declared size; block 32 omits EOF padding in both canonical inputs while header declared size remains 0x40-aligned.

```text
original block 32 declared - physical = 55 bytes
Korean block 32 declared - physical   = 34 bytes
```

Those EOF-omitted bytes are not approved writable capacity.

## 유력한 가설

A future serializer should preserve the observed final-block EOF omission. Serializer authorization remains separate.

## 미확정 사항

This artifact does not establish semantic VM call-ID equivalence, caller graph, nested formatter edges, mechanism class, usage class, applicability, realization, release scope, or build authorization.

## 기각된 가설

- absolute file offsets as permanent TAI5MSG identity;
- payload hashes as permanent identity;
- 14,832 PC/Switch entity pairs plus 14,832 `BINDS_TO` edges at this structural stage;
- blocks as semantic registry entities;
- `local_message_index` as proven semantic VM call ID;
- final-block declared-minus-physical bytes as writable capacity;
- legacy full-file reconstruction as selective serializer authority;
- treating a structure artifact as automatic candidate/release inclusion.

## 관련 영향 범위

```text
new artifact ID          = ART-00000005
artifact IDs total       = 5
next artifact sequence   = 6
new entity IDs           = 0
new edge IDs             = 0
new candidate IDs        = 0
new classifications      = 0
TAI5MSG payload rewrite  = 0
builder/build/IPS        = 0
```

## Git incident / failure provenance

The contents-API incident chains and forward recoveries through `ce77b50e...` are preserved in `selective_ko/KNOWN_FAILURES.md`.

The later sentinel-file drift (`f2936af5...` -> `6173bc46...`) is also preserved there. Forward recovery `ef1a3dbe...` removes only `__NEVER__` and `__SHOULD_NOT_BE_CALLED__`, reproducing the valid `12e0708e...` tree exactly.

The overnight documentation commit `cd5566c3...` correctly added incident provenance but replaced older technical failure sections instead of appending them. This materialization restores those prior sections, retains all incident records, and records that `ce77b50e...` reproduces the `cd5566c3...` tree exactly. No gameplay data was affected by either documentation or transport incidents.

Earlier unattached prototype blobs remain noncanonical.

## 수정 제안

After remote readback closes this artifact, proceed to:

```text
TAI5MSG_SELECTIVE_MESSAGE_CLASSIFICATION_READ_ONLY
```

The first partition should separate structurally simple 1:1/static-variable message populations from cross-message/nested grammar-formatter populations. Person/place/yomi identity remains Japanese for the initial selective release.
