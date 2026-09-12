# Machine-Accounting Schema v1 Amendment

Date: 2026-09-12  
Base HEAD: `e2e70298466d44fc28d210e323f91d13e5561a38`  
Status: AMENDMENT IMPLEMENTED / REGRESSION BLOCKED / NOT FROZEN

## 1. Scope

This stage implements only the schema-v1 amendment authorized after the schema-freeze review. It does not perform full-corpus migration, analyze the 797 target-unresolved residual, modify builder/IPS/runtime/game data, or revalidate the already-canonical F1 byte-analysis conclusions.

The amendment preserves the v0.1 F1 pilot as historical evidence and adds a v1 candidate overlay.

## 2. v1 candidate changes

The candidate now separates semantic schema from transport format and defines normalized semantic rows for:

- source obligation/state revisions;
- action identity/revisions;
- source/action edges;
- validation claims;
- invariant definitions/evaluations;
- migration and coverage records.

Key amendments:

- `accounting_role = OBLIGATION | GROUP` is explicit;
- descriptor GROUP rows are auditable but are not leaf-obligation denominator rows;
- action semantics are normalized from the existing V094 manifest rather than copied into a second truth source;
- two-field F1 edge seeds materialize deterministically into full edge semantics;
- atomic and legacy provenance are separated as `claim_refs[]` and `legacy_evidence_refs[]`;
- structured UNKNOWN remains a hard authorization blocker;
- invariant dependency fingerprints implement `PASS -> STALE` without converting STALE to FAIL;
- assertion-bearing `SUPERSEDED_TEXT` is accepted only with explicit supersession provenance;
- target-resolution dashboards name the numerator axis and emit `resolved/applicable`, `resolved/total`, and `excluded/total` together;
- compact transport is bound to a versioned materialization contract and must later pin materialized semantic hashes;
- validators use explicit failures rather than Python `assert` as the release mechanism.

## 3. Claim amendment

The original 42 v0.1 claim IDs remain immutable historical IDs.

Nine composite/legacy-shape claims are represented as `SUPERSEDED` in the v1 effective view and 52 new atomic claims are appended. No existing claim ID is renumbered, reused or deleted.

Expected v1 candidate claim accounting:

```text
base historical claims      42
new atomic claims            52
effective claim rows         94
ACTIVE claims                85
```

The legacy symbolic supersession `PROVISIONAL_RESIDUAL_781` is retained only as legacy supersession provenance in the replacement correction claim; claim-to-claim supersession fields contain machine claim IDs only.

No technical byte fact is revalidated by this claim-shape migration.

## 4. F1 population pre-action regression

Before loading the V094 action payload, the v1 validator reproduced the F1 source population exactly:

```text
sources                         278
target RESOLVED                 262
analysis ANALYZED_UNRESOLVED     16
closure CLOSED                  158
verified exclusions               0
```

The validator also passed exact category membership checks for DIRECT, PADDING, SHARED, CAPACITY and REJECT, and the full ordered source-ID hash matched:

`ace2bc4d27ae97d6583cd5b9293b994cb6ab0faed7551a5f5eb123ed216f3624`

Therefore the amendment did not alter the canonical F1 278-row membership before the action-table gate.

## 5. Newly discovered V094 repository-artifact blocker

The v1 regression uncovered a pre-existing repository transport defect in:

`docs/manifests/F1_STATIC_WRITE_AUTHORIZATION_MANIFEST.jsonl.gz`

Canonical V094 provenance records:

```text
expected gzip SHA-256       8bbbeb03695b4bd06f028b9c9cfe0d367af170a012af56803f3a8553356a0b68
expected content SHA-256    c612bcf55d0c139d55dee42a6a6397f702ead0f1628b47b45c46512fd1b52bff
expected rows               158
```

GitHub Actions run `34663770280` measured the checked-out repository artifact as:

```text
repository bytes            21,288
repository SHA-256          826c73a0f80ae645420a189a4dd7b1e3637afd0e514fbc4f00d84189595daf37
gzip end-of-stream          false
recoverable payload bytes   314,998
recovered payload SHA-256   772ed05a0d3af9856eca3cf93165663b005d5ef9bbd06b228886c7f18ca51fc0
decoded line fragments      129
complete JSON action rows   55 / 158
first malformed line        56
payload ends with newline   false
```

This is not a missing gzip footer only. Semantic payload is truncated before the canonical 158-action table is complete.

Git history shows this path was introduced by commit `c6c7800177c46d320f3281ddd9fd9bf03b137726` (`docs: close F1 static write authorization`) and the same Git blob is present in later commits. The schema-v1 amendment did not introduce the truncation.

## 6. Authority interpretation

This defect does **not** by itself invalidate the historical V094 authorization conclusion. V094 records that the original local deterministic replay produced 158 actions and pins both the content and gzip hashes.

However, the repository copy currently cannot serve as the promised action-payload authority because 103 of 158 complete JSON action rows are unavailable from that file. Therefore:

- V094 historical authorization remains canonical evidence;
- the current repository artifact is provenance-incomplete for downstream machine consumption;
- the v1 candidate cannot normalize and hash all 158 actions;
- the full F1 278 regression cannot reach PREPIN/PASS;
- semantic hashes for action and edge/action consistency must not be invented or pinned;
- schema v1 must remain NOT FROZEN.

## 7. Rejected shortcuts

The following were explicitly rejected:

- accepting the partial 55-row payload as the action table;
- treating zlib partial recovery as canonical reconstruction;
- reconstructing the missing 103 rows from action IDs or summary counts;
- creating a second action truth source from the pilot edge table;
- re-running the F1 selector merely because the committed gzip is truncated;
- proceeding to schema freeze while the sole bound action payload is incomplete.

## 8. Required next stage

A fresh execution signal is required before repair.

The next stage should be **V094 manifest provenance/transport repair only**:

1. locate an exact copy whose gzip SHA-256 is `8bbb...`; or
2. if no exact artifact exists, reproduce the canonical manifest from the already-defined V093/V094 deterministic replay using the same canonical inputs, treating this as artifact restoration rather than new F1 analysis;
3. require content SHA-256 `c612...`, gzip SHA-256 `8bbb...`, 158 rows, stable action IDs and existing V094 source-ID hash;
4. replace only the corrupted repository artifact after exact identity proof;
5. rerun the v1 candidate regression;
6. only after that regression emits and pins all materialized semantic hashes may a later, separately authorized schema-freeze step be considered.

No full migration, residual analysis, builder, IPS or runtime work is part of that repair.
