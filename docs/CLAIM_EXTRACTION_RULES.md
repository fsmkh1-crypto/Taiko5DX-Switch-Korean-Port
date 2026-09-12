# Claim Extraction Rules — v1 Candidate

Date: 2026-09-12  
Status: CANDIDATE / NOT FROZEN

## 1. Atomicity

A claim is the smallest assertion that can be independently falsified, corrected, superseded, invalidated or depended on.

If values in one statement can change independently, they are separate claims. A structured value may remain one claim only when it is one inseparable identity, one exhaustive set/map, one histogram treated as a single measurement, or one accounting equation whose meaning is defined only as a whole.

A structured exception must be explicitly declared. It cannot be used merely to avoid issuing atomic IDs.

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

The validator checks:

- document Git blob identity;
- anchor-text SHA-256;
- anchor text occurs in the bound document.

Historical coverage may continue to point to a superseded claim because it records what text was originally extracted. New active decisions must resolve through the supersession graph to active claims.

## 8. v0.1 F1 claim amendment

The v0.1 claim rows remain immutable historical data.

The v1 candidate amendment file:

`data/pilot/f1_v1_candidate/claim_amendments.json`

supersedes the identified composite claims and issues appended atomic IDs. It also replaces the legacy symbolic supersession inside `V092.C01` by a new correction claim whose `legacy_supersedes_refs` carries that historical symbol.

No technical byte fact is revalidated by this claim-shape amendment.

## 9. Structured atomic exceptions in the F1 candidate

Only explicitly declared exceptions may remain structured. Current candidate exceptions cover:

- one exhaustive histogram measurement;
- one accounting equation;
- one canonical manifest identity tuple;
- one exhaustive terminator-mode partition;
- one Build-ID representation identity tuple.

Any later structured exception requires an explicit reason and review.
