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

## Stopping point

The schema-v1 amendment is implemented as a candidate, but the agreed F1 regression cannot complete because the pre-existing V094 repository payload is incomplete.

Schema remains **NOT FROZEN**.

Fresh user execution signal is required for V094 manifest provenance/transport repair. Full migration, the 797 residual, builder, IPS and runtime work remain out of scope.
