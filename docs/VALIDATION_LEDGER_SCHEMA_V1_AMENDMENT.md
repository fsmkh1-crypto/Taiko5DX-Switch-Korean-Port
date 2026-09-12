# VALIDATION LEDGER — Schema v1 amendment

Date: 2026-09-12  
Scope: machine-accounting schema v1 candidate amendment and F1 regression attempt only. No schema freeze, full-corpus migration, residual-family analysis, builder, IPS, runtime, or game-file work.

Detailed report: `docs/SCHEMA_V1_AMENDMENT.md`

## V099 — schema v1 candidate closes the freeze-review model gaps

**Status:** `VERIFIED AS CANDIDATE DESIGN / NOT FROZEN`

The v1 candidate adds or makes normative:

- independent semantic-schema and transport-format versioning;
- explicit `accounting_role = OBLIGATION | GROUP`;
- append-only source and action revision semantics;
- a normalized action schema bound to, rather than duplicating, the V094 action manifest;
- deterministic full edge materialization from the F1 compact edge seed;
- atomic `claim_refs[]` separated from `legacy_evidence_refs[]`;
- immutable historical claim IDs with explicit supersession and appended atomic replacements;
- variable-width claim-number syntax;
- `legacy_supersedes_refs[]` for pre-claim symbolic history;
- invariant definition/evaluation separation and dependency-fingerprint `PASS -> STALE` behavior;
- mixed migration-status semantics;
- assertion-bearing `SUPERSEDED_TEXT` handling with required supersession provenance;
- explicit target-resolution denominator triplet;
- materialization-contract binding and future materialized semantic-hash pinning;
- explicit fail-closed validation without relying on Python `assert`.

The original 42 pilot claims remain immutable historical rows. The candidate amendment declares 52 appended atomic claims, yielding 94 effective rows / 85 ACTIVE claims if the regression reaches full materialization.

V099 does not itself make machine data authoritative over canonical Markdown and does not freeze the schema.

## V100 — exact F1 source membership passes, but V094 action-table regression is blocked by a pre-existing truncated repository artifact

**Status:** `VERIFIED BLOCKER / REGRESSION INCOMPLETE`

Before the action-table gate, the v1 candidate validator reproduced:

```text
sources                       278
target resolved               262
analyzed unresolved            16
closed                        158
verified exclusions             0
```

It also passed exact DIRECT/PADDING/SHARED/CAPACITY/REJECT membership and the full ordered source-ID hash:

`ace2bc4d27ae97d6583cd5b9293b994cb6ab0faed7551a5f5eb123ed216f3624`

The bound repository artifact `docs/manifests/F1_STATIC_WRITE_AUTHORIZATION_MANIFEST.jsonl.gz` fails the V094 identity gate.

Canonical V094 identity:

```text
gzip SHA-256       8bbbeb03695b4bd06f028b9c9cfe0d367af170a012af56803f3a8553356a0b68
content SHA-256    c612bcf55d0c139d55dee42a6a6397f702ead0f1628b47b45c46512fd1b52bff
rows               158
```

GitHub Actions run `34663770280` measured:

```text
repository bytes            21,288
repository SHA-256          826c73a0f80ae645420a189a4dd7b1e3637afd0e514fbc4f00d84189595daf37
gzip EOF                    false
recovered bytes             314,998
recovered SHA-256           772ed05a0d3af9856eca3cf93165663b005d5ef9bbd06b228886c7f18ca51fc0
complete JSON rows          55 / 158
first malformed line        56
```

Therefore the stored file is not merely missing a gzip footer; its semantic JSONL payload is truncated.

Git history attributes the path introduction to commit `c6c7800177c46d320f3281ddd9fd9bf03b137726`; the same Git blob persists in later commits. The v1 amendment did not cause the corruption.

**Boundary:** this repository-artifact defect does not automatically invalidate the historical V094 authorization conclusion, whose original replay recorded 158 rows and pinned both hashes. It does make the current committed artifact unusable as the sole machine-consumable action payload until exact provenance restoration.

Consequences:

- do not infer or synthesize the missing 103 action rows;
- do not pin v1 action semantic hashes from partial data;
- do not freeze schema v1;
- do not re-run the whole F1 analysis merely because of this transport/provenance defect;
- repair/restore the exact V094 manifest in a separate stage under a fresh user signal, then rerun the candidate regression.

## V102 — V094 transport repair v2 restores complete machine-consumable action authority and exposes a separate atomic-claim blocker

**Status:** `VERIFIED TRANSPORT REPAIR / V094 BLOCKER CLOSED / SCHEMA STILL NOT FROZEN`

Repair commit:

`d25fd5be5c15aabd1483c0e8bf0ad4873974bb1b` — `repair: replace V094 failed transport with deterministic JSONL shards`

The failed binary/gzip repository transport was replaced by a deterministic plain-JSONL shard transport at:

`docs/manifests/F1_STATIC_WRITE_AUTHORIZATION_MANIFEST/`

Current transport identity:

```text
format                    PLAIN_JSONL_SHARDS
shard rule                preserve canonical V094 row order; contiguous groups of 8 rows
shards                    20
rows                      158
INDEX SHA-256             ce241ab9a3257e0cf858d4b016eebdcd3c564958e95cdaf23035c0f4dfdfd6d4
logical content SHA-256   c612bcf55d0c139d55dee42a6a6397f702ead0f1628b47b45c46512fd1b52bff
ordered source IDs SHA    87d5a7531b5e2b3841fe4ba093a87dd9da11e8c85b5d4184c6ae705436c1833e
```

All 20 shard uploads used small UTF-8 Git blobs and each GitHub-returned blob SHA matched the locally expected Git blob SHA before the repair tree was committed.

Historical transport provenance remains separate and unchanged:

```text
format                    deterministic gzip JSONL
historical gzip SHA-256   8bbbeb03695b4bd06f028b9c9cfe0d367af170a012af56803f3a8553356a0b68
```

The new transport diagnostic reconstructs the historical deterministic gzip from the shard-concatenated semantic byte stream and obtains the exact historical `8bbb...` hash. Both prior failed transports remain recorded in `INDEX.json` as `FAILED_TRANSPORT_NOT_CANONICAL` provenance rather than being erased.

GitHub Actions run `34677635822` independently checked the repair and passed the V094 transport gate:

```text
transport index SHA-256        ce241ab9a3257e0cf858d4b016eebdcd3c564958e95cdaf23035c0f4dfdfd6d4
shards                         20
rows                           158
logical content SHA-256        c612bcf55d0c139d55dee42a6a6397f702ead0f1628b47b45c46512fd1b52bff
ordered source IDs SHA-256     87d5a7531b5e2b3841fe4ba093a87dd9da11e8c85b5d4184c6ae705436c1833e
reconstructed gzip SHA-256     8bbbeb03695b4bd06f028b9c9cfe0d367af170a012af56803f3a8553356a0b68
failed transports recorded     2
```

The candidate validator then advanced beyond the former V094 blocker and passed action-table semantics, 158 actions, source/action edge agreement, exact F1 membership, and the pre-action source gates. It subsequently failed at:

`atomic_claim_policy: ['V089.C03']`

This is a separate schema-v1 claim-shape cause family, not a V094 transport failure. It was not modified in the V094 repair stage.

Consequences:

- the V094 repository transport blocker recorded by V100 is closed;
- V094 semantic identity and historical gzip provenance are unchanged;
- the current plain-shard transport is the machine-consumable V094 action authority;
- the schema-v1 candidate regression is still incomplete because of the separate `V089.C03` atomic-claim-policy blocker;
- materialized semantic hashes remain unpinned;
- schema v1 remains **NOT FROZEN**;
- no 797 residual, builder, IPS, runtime, mapping, or game-file work was performed.

## Stopping point

V094 transport repair v2 is complete.

The next separately authorized stage is analysis of the schema-v1 candidate `V089.C03` atomic-claim-policy blocker only. Do not treat that stage as schema-freeze authorization, and do not expand it into full migration, the 797 residual, builder, IPS, runtime, mapping, or game-file work.
