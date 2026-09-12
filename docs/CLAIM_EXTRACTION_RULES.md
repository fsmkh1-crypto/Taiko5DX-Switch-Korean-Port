# Claim Extraction Rules — v1 Frozen

Date: 2026-09-12  
Status: FROZEN — `FZ001`

<!-- MACHINE_FACTS_V1
{
  "schema": "MACHINE_FACTS_V1",
  "facts": {
    "source_anchor_gate_registry": [
      "anchor_blob_",
      "anchor_document_",
      "anchor_heading_",
      "anchor_present_",
      "anchor_text_hash_",
      "anchor_text_in_heading_"
    ],
    "structured_atomic_exception_count": 10,
    "structured_atomic_exception_ids": [
      "V088.C04",
      "V089.C03",
      "V090.C01",
      "V091.C02",
      "V091.C05",
      "V092.C02",
      "V093.C03",
      "V094.C01",
      "V094.C03",
      "V095.C01"
    ],
    "structured_atomic_registry_path": "data/pilot/f1_v1_candidate/claim_amendments.json"
  }
}
MACHINE_FACTS_V1 -->

## 1. Atomicity

A claim is the smallest assertion that can be independently falsified, corrected, superseded, invalidated or depended on.

If values in one statement can change independently, they are separate claims. A structured value may remain one claim only when it is one inseparable identity, one exhaustive set/map, one histogram treated as a single measurement, or one accounting equation whose meaning is defined only as a whole.

A structured exception must be explicitly declared in the frozen machine registry. The historical `f1_v1_candidate` path name is retained as a stable provenance identifier after freeze. A structured exception cannot be used merely to avoid issuing atomic IDs.

## 2. Facts and interpretations

Observed fact and interpretation are separate claims. Interpretations depend explicitly on the fact claims they use and do not silently inherit their verification state.

## 3. Negative knowledge

Absence of proof is explicit:

- `EVIDENCE_GAP` = not proven / provenance missing / ownership unresolved.
- `FACT` with zero/none = exhaustive method proved zero/none.

For the F1 shared-owner population, the canonical meaning is `replacement conflict not proven`, not `absence of conflict proven`.

## 4. Boundary claims

Authorization limits, scope limits and downstream-use prohibitions are `BOUNDARY` claims. They remain machine-visible because violating them changes allowed downstream behavior.

## 5. Immutable IDs and supersession

Issued claim IDs are permanent and are never renumbered, reused or deleted.

If an issued pilot claim is too composite:

1. retain the original ID;
2. mark it `SUPERSEDED`;
3. issue new atomic IDs;
4. record `superseded_by[]` / `supersedes[]`;
5. keep unaffected sibling claims ACTIVE.

Claim ID syntax allows variable-width claim numbers: `Vnnn.Cn+`.

`supersedes[]` contains claim IDs only. Pre-claim symbolic history belongs in `legacy_supersedes_refs[]`.

## 6. Evidence references

New machine entities use:

```text
claim_refs[]
legacy_evidence_refs[]
```

Atomic dependency and staleness logic use `claim_refs`. Legacy ledger IDs remain provenance, not a substitute for atomic dependency links.

## 7. Source anchors

Every migrated claim has a source anchor with:

```text
document_path
document_git_blob_sha
heading_path
anchor_text
anchor_text_sha256
```

The current validator exposes six independent source-anchor gate families:

- `anchor_present_` — the source-anchor object exists;
- `anchor_document_` — the bound document path exists;
- `anchor_blob_` — the bound document Git blob identity matches;
- `anchor_text_hash_` — the anchor-text SHA-256 matches;
- `anchor_heading_` — `heading_path` resolves uniquely in the bound Markdown document;
- `anchor_text_in_heading_` — the anchor occurs inside the resolved heading section.

A missing source-anchor object or bound document fails before the later identity/section checks can succeed. A heading that resolves to zero or multiple sections fails. Merely finding the anchor text somewhere else in the same document is insufficient.

Historical coverage may continue to point to a superseded claim because it records what text was originally extracted. New active decisions must resolve through the supersession graph to active claims.

## 8. v0.1 F1 claim amendment

The v0.1 claim rows remain immutable historical data.

The historically named v1 candidate amendment file, now part of the frozen `FZ001` snapshot, is:

`data/pilot/f1_v1_candidate/claim_amendments.json`

supersedes the identified composite claims and issues appended atomic IDs. It also replaces the legacy symbolic supersession inside `V092.C01` by a new correction claim whose `legacy_supersedes_refs` carries that historical symbol.

No technical byte fact is revalidated by this claim-shape amendment.

## 9. Structured atomic exceptions in the frozen F1 v1 snapshot

`data/pilot/f1_v1_candidate/claim_amendments.json` is the frozen structured-atomic exception registry for schema v1. The path name is retained for provenance stability. The registry contains exactly ten ACTIVE structured exceptions:

```text
V088.C04
V089.C03
V090.C01
V091.C02
V091.C05
V092.C02
V093.C03
V094.C01
V094.C03
V095.C01
```

These cover only reviewed inseparable/exhaustive structured claims such as exhaustive sets or maps, histogram/accounting structures, manifest identity, terminator partition and Build-ID identity. The registry entry's reason is authoritative for why a specific claim may remain structured.

Any later structured exception requires an explicit registry entry and review. Adding prose here without changing the machine registry does not authorize a new exception.
