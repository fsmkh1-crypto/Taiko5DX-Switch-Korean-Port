# Artifact and Provenance Rules

Date: 2026-09-12  
Status: CANONICAL MACHINE-ARTIFACT POLICY

## 1. Scope

This policy governs canonical machine artifacts, generated state, storage format, sharding, hashes, and connector/repository transport.

Build/runtime artifact provenance remains separately governed by `docs/PROVENANCE_POLICY.md`.

## 2. Semantic identity and transport identity are separate

Every canonical machine artifact should distinguish the logical content from the bytes used to transport/store it.

Semantic identity contains, as applicable:

```text
logical_content_sha256
row_count
canonical_order_rule
serialization_rule
schema/semantic version
```

Transport identity contains, as applicable:

```text
format
transport version
shard rule
shard count
per-shard sha256
optional whole-transport sha256
```

Changing transport must not silently change semantic rows.

Changing semantic content requires a semantic revision/version even if transport bytes happen to remain unchanged.

## 3. Historical transport provenance

If a transport hash has already been used as validation provenance, changing storage format does not erase it.

Retain it as `historical_transport` with its format, identity, and provenance reference.

A new transport is additional provenance, not a rewrite of history.

## 4. Failed transport is a first-class state

A repository object produced by a failed or truncated upload is not canonical merely because it exists on `main`.

Record it explicitly as a failed transport with enough identity to prevent later rediscovery/re-investigation:

```text
commit/ref
path
byte size
Git blob identity and/or sha256 when available
failure mode
canonical semantic identity it failed to carry
```

Failed transport must never be consumed as the semantic action/state authority.

## 5. Canonical vs generated

Use this decision rule:

> Has another canonical decision, validation, migration, or release gate cited this artifact?

If yes, preserve it as canonical evidence.

If no, and the artifact is deterministically reproducible from stronger canonical sources, it may remain generated.

Promotion from generated to canonical requires provenance and identity binding.

## 6. Serialization rules

Every logical dataset defines a deterministic serialization contract.

For JSONL-like datasets the contract must state:

- UTF-8 encoding;
- exact row order;
- JSON serialization rule;
- line ending;
- whether the final row ends with LF.

Existing canonical semantic hashes retain the serialization contract under which they were issued. Do not “normalize” an old canonical payload into a new byte representation and then call the new hash the same semantic identity.

## 7. Sharding rules

Sharding is transport only.

For an existing ordered canonical payload:

```text
preserve canonical row order
split only into deterministic contiguous groups
```

Shard boundaries do not define semantic families.

The dataset index records:

- shard rule;
- authoritative shard order;
- rows per shard or deterministic boundary rule;
- per-shard row counts and hashes;
- total rows;
- logical-content hash of raw shard concatenation.

Reassembling shards in index order under the declared serialization contract must reproduce the logical semantic byte stream exactly.

## 8. Connector transport rule

Do not make long manual binary/base64 strings a normal connector write path.

Do not respond to a truncation by repeatedly slicing the same payload into progressively smaller Git blobs and manually assembling trees.

After one credible transport-integrity failure, change the transport route/design.

Preferred order:

1. small ordinary UTF-8 repository files;
2. deterministic text shards when semantically appropriate;
3. native file-reference transfer or repository-native generation;
4. a different supported transport path.

If no safe exact-byte path exists, STOP and report the transport blocker instead of manufacturing a complicated partial repository state.

## 9. Verification split

Use each mechanism for its proper role:

- row count: omission/truncation;
- SHA-256: exact identity;
- validator: structural/semantic invariants;
- Git diff: review of intentional semantic change.

Once the canonical identity required by the current stage matches, stop re-proving the same fact through unrelated tools.

## 10. V094 precedent

V094 currently demonstrates the required separation:

```text
semantic identity:
  rows    = 158
  sha256  = c612bcf55d0c139d55dee42a6a6397f702ead0f1628b47b45c46512fd1b52bff

historical canonical transport:
  format  = deterministic gzip JSONL
  sha256  = 8bbbeb03695b4bd06f028b9c9cfe0d367af170a012af56803f3a8553356a0b68

failed current transport on main b58402a...:
  path     = docs/manifests/F1_STATIC_WRITE_AUTHORIZATION_MANIFEST.jsonl.gz
  bytes    = 12071
  git_blob = 9a3bc50b18a51582b2031611a2f46fe1c069a862
  status   = FAILED_TRANSPORT_NOT_CANONICAL
```

This policy does not itself repair V094 or choose its replacement current transport.
