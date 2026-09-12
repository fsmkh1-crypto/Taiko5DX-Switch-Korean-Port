# Claim Extraction Rules — Pilot v0.1

Date: 2026-09-12
Status: PILOT OUTPUT / NOT FROZEN

## 1. Atomicity rule

A claim is the smallest assertion that can be independently falsified, superseded, invalidated, or depended on.

Multiple values in one sentence become separate claims when they can change independently. Values remain one structured claim only when together they form one inseparable identity or one accounting equation whose meaning would be lost by splitting.

Example: `base 0x6ADA10, stride 0x18, 33 duplicates / 66 slots` normally becomes separate atomic claims for base, stride, duplicate count, and slot count because each is independently testable and independently correctable.

## 2. Fact plus interpretation

`X is observed; therefore Y means ...` becomes at least two claims:

- a `FACT` claim for X;
- an `INTERPRETATION` or rule/correction claim for Y with `depends_on_claims` pointing to X.

Interpretation never silently inherits the verification status of the underlying byte fact.

## 3. Negative knowledge

Absence of proof is represented explicitly; it is never encoded by omitting a claim.

- `EVIDENCE_GAP`: a proposition is not proven, provenance is missing, or a consumer/owner relation remains unbound.
- `FACT` with zero/none value: an explicit exhaustive method proved that no instances exist.

Example: `no conflicting replacement is proven for the shared object` is an `EVIDENCE_GAP` unless the method exhaustively proves zero conflicts. `unintended overlaps = 0` after exhaustive interval comparison is a verified `FACT`.

## 4. Boundary claims

Statements such as `this is audit evidence, not builder authorization` are `BOUNDARY` claims because they constrain allowed downstream behavior even though they are not byte facts.

## 5. Supersession

Claim IDs are immutable. Narrow corrections supersede only the affected atomic claims. Unaffected sibling claims under the same ledger ID remain active.

A later-discovered claim is appended with a new claim ID; existing IDs are never renumbered.

## 6. Source-anchor rule

Every migrated claim carries a stable source anchor. During the pilot, anchors use document path, Git blob SHA where available, heading path, and an exact anchor-text hash. Full-document migration additionally covers every source block with an explicit coverage disposition.

## 7. F1 pilot consequences

The F1 pilot specifically preserves:

- the distinction between promoted `target_identity` and unpromoted `candidate_target_identity`;
- `not proven false` as explicit epistemic state rather than target promotion;
- audit-only classifications as boundary claims;
- verified zero-overlap results as facts rather than evidence gaps;
- shared-owner uncertainty as structured UNKNOWN debt.
