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

The original 42 pilot claims remain immutable historical rows. The candidate amendment initially declared 52 appended atomic claims, yielding 94 effective rows / 85 ACTIVE claims before the later V103 structured-claim closure.

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

The bound repository artifact `docs/manifests/F1_STATIC_WRITE_AUTHORIZATION_MANIFEST.jsonl.gz` failed the V094 identity gate.

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

Therefore the stored file was not merely missing a gzip footer; its semantic JSONL payload was truncated.

Git history attributes the path introduction to commit `c6c7800177c46d320f3281ddd9fd9bf03b137726`; the v1 amendment did not cause the corruption.

**Boundary:** this repository-artifact defect did not invalidate the historical V094 authorization conclusion. It blocked current machine consumption until exact provenance restoration.

## V102 — V094 transport repair v2 restores complete machine-consumable action authority and exposes a separate atomic-claim blocker

**Status:** `VERIFIED TRANSPORT REPAIR / V094 BLOCKER CLOSED / SCHEMA STILL NOT FROZEN`

Repair commit:

`d25fd5be5c15aabd1483c0e8bf0ad4873974bb1b` — `repair: replace V094 failed transport with deterministic JSONL shards`

The failed binary/gzip repository transport was replaced by deterministic plain-JSONL shards at:

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

Historical transport provenance remains separate and unchanged:

```text
format                    deterministic gzip JSONL
historical gzip SHA-256   8bbbeb03695b4bd06f028b9c9cfe0d367af170a012af56803f3a8553356a0b68
```

GitHub Actions run `34677635822` independently passed the V094 transport gate and reconstructed the exact historical gzip identity. The candidate then advanced beyond the V094 blocker and first failed at:

`atomic_claim_policy: ['V089.C03']`

This was classified as a separate schema-v1 claim-shape cause family.

## V103 — structured atomic-claim cause family is closed and the regression advances to V092.C04 anchor provenance

**Status:** `VERIFIED ATOMIC-CLAIM CLOSURE / REGRESSION ADVANCED / SCHEMA STILL NOT FROZEN`

Fix commit:

`9df784890b9f21f79187ed67825919fedf4d77f7` — `fix: close structured atomic-claim classification gaps`

The cause-family audit classified every ACTIVE structured claim value instead of relying only on predicate-name heuristics.

`V089.C03` remains ACTIVE as an explicit structured-atomic exception because it is one exhaustive historical storage partition of the same 278 F1 residual population:

```text
full-window       197
padding-mismatch   81
TOTAL             278
```

V093 deterministic replay independently reproduces that same historical split.

`V094.C04` is not treated as an inseparable tuple. It is retained historically as SUPERSEDED and replaced by three appended atomic claims:

```text
V094.C23  terminal_disposition_overlay = DIRECT_PORT
V094.C24  action_family                = F1_LOCALIZATION_STATIC_DIRECT
V094.C25  action_status                = STATIC_WRITE_AUTHORIZED_NOT_IMPLEMENTED
```

The materialization contract was rebound accordingly:

- DIRECT source-state provenance references C23/C24/C25;
- normalized action provenance references C24/C25;
- source/action edge provenance uses `V094.C14` for the unique-action-ID assertion;
- the action materialization source path now points to the current plain-shard V094 transport.

The candidate counts are now:

```text
base claims                 42
new appended claims         55
effective claims            97
ACTIVE claims               87
candidate migration entries 752
```

The transport-aware validator additionally requires the explicit structured-claim registry to equal the set of all ACTIVE dict/list-valued claims exactly. It rejects:

- an ACTIVE structured claim omitted from the registry;
- a registry entry that is no longer ACTIVE or structured;
- duplicate registry IDs;
- a claim classified as both split and structured-atomic.

GitHub Actions run `34679464287` passed:

- V094 transport identity;
- amendment and contract hashes;
- exact F1 source/category membership;
- 158 actions and 158 source/action edges;
- action/source/edge active-claim referential integrity;
- split-source supersession;
- effective/ACTIVE claim counts;
- `atomic_claim_policy`;
- the new structured-claim registry preflight.

The first subsequent failure is:

`anchor_text_present_V092.C04: None`

Therefore the V089.C03/structured-atomic cause family is closed. The new failure is a separate source-anchor/provenance cause family and is not evidence against V092, F1, or V094 technical facts.

Consequences:

- do not reopen the V103 atomic-claim classification without a legitimate revalidation trigger;
- do not alter V092 technical semantics merely to satisfy the anchor gate;
- materialized semantic hashes remain unpinned;
- schema v1 remains **NOT FROZEN**;
- no 797 residual, builder, IPS, runtime, mapping, or game-file work was performed.

## V104 — source-anchor provenance closure reaches PREPIN_PASS

**Status:** `VERIFIED PROVENANCE CLOSURE / PREPIN_PASS / SCHEMA STILL NOT FROZEN`

Fix commit:

`cb21ce200a89457b77072b56f2f48a5d43d1bac0` — `fix: close source-anchor provenance gaps`

The pilot base-claim dataset remains byte-immutable. A candidate overlay now carries explicit source-anchor corrections instead of rewriting historical claim rows:

`data/pilot/f1_v1_candidate/source_anchor_overrides.json`

Seven weak or malformed locators were corrected as one provenance cause family:

- `V088.C06` — direct `JP_ONLY` statement;
- `V088.C07` — direct R549 -> localization ID1706 statement;
- `V089.C01` — complete 278-row disposition partition;
- `V089.C03` — complete 197/81 historical storage partition;
- `V091.C02` — exact padding histogram;
- `V091.C05` — exact nine overlap pairs;
- `V092.C04` — direct evidence-gap statement that the 16 candidate mappings remain useful but are not promoted.

All seven bind to the already-canonical `docs/F1_LOCALIZATION_SEQUENCE_AUDIT.md` Git blob `ba9c660cf6f229ec2b19f024b9bc2cef94d26a44`. No anchor-protected canonical evidence document was edited.

The validator now audits **all 97 effective claims**, including appended split claims, and requires for each claim:

- the bound document Git blob identity matches;
- `anchor_text_sha256` matches the stored text;
- `heading_path` resolves to exactly one Markdown section;
- the anchor text occurs inside that claimed heading section rather than merely somewhere in the document.

Source-anchor override IDs are unique, bound by canonical JSON hash, must resolve to an effective claim ID, and may be used for future appended claims when inherited provenance is too coarse.

GitHub Actions run `34680748843` completed successfully and returned:

`PREPIN_PASS`

No further candidate validation blocker was exposed. The materialized semantic hashes produced by that run are:

```text
source_state         91a54c8760f84f0e5b48e25dfda8adb9ae16ff32a83a4af86275fbc0c762322c
actions              a7c0f3ce3423b2a07797ef18e538c963140303751621a985dc6fe76c52bb8a4f
source_action_edges  1399fa309889399854d68f5d89f202df0f22f7be58ec2c85e3a02342987a4fe7
effective_claims     2cb8459c95ec53e0f61fd72dd80de45148a1091b637bebaa50ef4d3607c50676
```

These hashes are **observed candidate outputs only**. They are not yet pinned in bindings and V104 does not authorize schema freeze.

## Stopping point

The source-anchor/provenance cause family is closed. The candidate currently reaches `PREPIN_PASS` with no later blocker exposed by the existing fail-fast pipeline.

The next separately authorized stage should address the validation-pipeline cause family identified during the V104 audit: diagnostic collect-all visibility and consolidation of the transport/provenance compatibility wrapper into the candidate validation path. Authority-freshness cleanup, CI-trigger/generated-status cleanup, semantic-hash pinning, and schema-freeze judgment remain separate later scopes.

No full migration, 797 residual analysis, builder, IPS, runtime, mapping, or game-file work is authorized by V104.
