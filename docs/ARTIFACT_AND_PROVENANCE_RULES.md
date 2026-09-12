# Artifact and Provenance Rules

Date: 2026-09-12  
Status: CANONICAL MACHINE-ARTIFACT POLICY

## 1. Scope

This policy governs canonical machine artifacts, generated state, JSON/JSONL storage direction, serialization, sharding, hashes, and repository transport.

Build/runtime artifact provenance remains separately governed by `docs/PROVENANCE_POLICY.md`.

## 2. Semantic identity and transport identity are separate

Every canonical machine artifact distinguishes logical content from the bytes used to store or transport it.

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

Changing transport must not silently change semantic rows. Changing semantic content requires a semantic revision/version even if transport bytes happen to remain unchanged.

## 3. Structured canonical-state direction

The machine-accounting model keeps entity classes separate because their cardinality and lifecycle differ.

The target canonical structure after an explicitly authorized schema freeze/migration is conceptually:

```text
validation claims
append-only source-state history
actions
source/action edges
migration manifest
```

Current snapshots, progress summaries, unknown-debt summaries, and invariant-status summaries are derived views unless explicitly promoted with provenance and identity.

Do not collapse these entity classes into one generic facts file merely for storage convenience.

Until the explicit freeze/migration stage occurs, existing canonical Markdown evidence and the current F1 candidate bindings retain their present authority. This section states direction; it does not perform migration or authority transfer.

## 4. Historical transport provenance

If a transport hash has already been used as validation provenance, changing storage format does not erase it.

Retain historical transport identity with its format and provenance reference. A new transport is additional provenance, not a rewrite of history.

## 5. Failed transport is first-class provenance

A failed/truncated repository object is not canonical merely because it exists or once existed on `main`.

Record enough identity to prevent rediscovery:

```text
commit/ref
path
byte size
Git blob identity and/or sha256 when available
failure mode
canonical semantic identity it failed to carry
```

Failed transport must never be consumed as semantic action/state authority.

## 6. Canonical vs generated

Use this decision rule:

> Has another canonical decision, validation, migration, or release gate cited this artifact as an authority dependency?

If yes, preserve it as canonical evidence/authority under its declared schema.

If no, and it is deterministically reproducible from stronger canonical sources, it remains generated.

Generated output is not a second truth source. Promotion to canonical requires explicit provenance, source identities, and identity binding.

Human-readable Markdown may be generated from stronger machine state in later migration stages, but historical/anchor-protected Markdown evidence remains evidence and is not retroactively rewritten.

## 7. Serialization rules

Every logical dataset defines a deterministic serialization contract.

For JSONL-like datasets the contract states:

- UTF-8 encoding;
- exact row order;
- JSON serialization rule;
- line ending;
- whether the final row ends with LF.

Existing canonical semantic hashes retain the serialization contract under which they were issued. Do not normalize old canonical bytes and silently reuse the old semantic identity.

## 8. Sharding rules

Sharding is transport only. Shard boundaries do not define semantic families.

For an existing ordered canonical payload:

```text
preserve canonical row order
split only by a deterministic boundary rule
minimize shard count within the proven-safe transport route
```

The dataset index records:

- shard rule;
- authoritative shard order;
- row/range boundary metadata;
- per-shard row counts and hashes;
- total rows;
- logical-content hash;
- exact concatenation/line-ending normalization contract.

Reassembly in index order must reproduce the declared logical byte stream exactly.

A historical 32 KiB probe is not a minimum legitimate file or shard size. Do not pad/combine ordinary files to satisfy it.

## 9. Connector transport rule

Do not use long manual binary/base64 arguments as the normal connector write path.

Do not answer truncation by repeatedly slicing the same payload into progressively smaller Git blobs and manually assembling more fragments.

After a credible transport-integrity failure, change route/design. After the same route fails twice for the same cause, STOP rather than making a third attempt.

Preferred order:

1. ordinary UTF-8 repository files preserving natural boundaries;
2. deterministic text shards when actually required;
3. native file-reference/repository-native generation;
4. another explicitly supported exact-byte route.

## 10. Verification split

Use each mechanism for its role:

- row count: omission/truncation;
- SHA-256: exact identity;
- validator: structural/semantic invariants;
- Git diff: intentional semantic review.

Once the identity required by the stage matches, stop re-proving it through unrelated tools.

## 11. V094 precedent

V094 demonstrates the separation:

```text
semantic identity:
  rows    = 158
  sha256  = c612bcf55d0c139d55dee42a6a6397f702ead0f1628b47b45c46512fd1b52bff

historical canonical transport:
  format  = deterministic gzip JSONL
  sha256  = 8bbbeb03695b4bd06f028b9c9cfe0d367af170a012af56803f3a8553356a0b68

failed transports:
  21,288-byte object = FAILED_TRANSPORT_NOT_CANONICAL
  12,071-byte object = FAILED_TRANSPORT_NOT_CANONICAL

current repository transport:
  path      = docs/manifests/F1_STATIC_WRITE_AUTHORIZATION_MANIFEST/
  format    = PLAIN_JSONL_SHARDS
  shards    = 20
  rows      = 158
  INDEX SHA = ce241ab9a3257e0cf858d4b016eebdcd3c564958e95cdaf23035c0f4dfdfd6d4
```

The current transport preserves the same V094 semantic identity and historical gzip provenance.

The 20-shard layout is a historical implementation produced under the transport constraints proven at that time. It is **not** a future sharding precedent, default shard count, safe-size threshold, or recommendation for larger migrations. Future sharding must follow §8 and §9 and use the fewest deterministic parts compatible with the transport route actually proven safe for that stage.

`docs/manifests/F1_STATIC_WRITE_AUTHORIZATION_SUMMARY.json` is a historical/reporting view, not canonical action authority. Its semantic payload identity and transport identity must be explicitly named and must not reuse a generic hash field for different transport generations. The canonical current action authority remains the indexed shard transport above; the historical deterministic gzip identity remains provenance only.
