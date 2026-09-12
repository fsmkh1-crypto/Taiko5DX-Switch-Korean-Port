# Validation Policy

Date: 2026-09-12  
Status: CANONICAL VALIDATION OPERATING POLICY

## 1. Reuse verified facts

A VERIFIED or VERIFIED-RUNTIME fact is reused unless a legitimate trigger exists:

- canonical input identity/version/hash changed;
- new evidence directly contradicts it;
- provenance is insufficient for the present decision;
- the prior method is demonstrated unsound.

A new chat, model, tool, or agent is never a revalidation trigger.

## 2. Dependency-scoped revalidation

A new hypothesis or code change does not automatically require broad revalidation.

Revalidation follows dependency impact:

- no relevant dependency identity change -> no revalidation;
- one dependency namespace changes -> only gates depending on that namespace become `STALE`;
- validator semantics change -> reevaluate the gate family owned by that validator rule;
- canonical input identity changes -> stale only the downstream dependencies that consume it.

Do not replay historical technical byte analysis when a current machine gate can be reevaluated from already-verified canonical evidence.

## 3. Status meanings

Keep these states distinct:

```text
PASS      condition evaluated and satisfied
FAIL      condition evaluated and violated
STALE     prior result no longer matches dependency identity
BLOCKED   evaluation cannot complete because required evidence/input is unavailable
UNKNOWN   unresolved semantic/evidence state
```

`STALE != FAIL`. `BLOCKED` is not technical disproof. `UNKNOWN` may not silently authorize a write or remove a source from accounting.

## 4. Fail-fast vs collect-all

Release validation remains fail-fast.

`COLLECT_ALL` is a non-release diagnostic mode that evaluates all currently reachable machine gates and reports `PASS / FAIL / BLOCKED / STALE` without weakening release semantics.

`COLLECT_ALL` is **not**:

- a replay of all historical reverse engineering;
- a reason to re-prove VERIFIED byte facts;
- permission to synthesize missing evidence.

Immediately before an explicitly authorized schema freeze, run one full current machine-gate collect-all after all intended candidate identities are fixed. This is gate reevaluation, not historical technical reanalysis.

## 5. Minimal proof path

Use the shortest evidence path sufficient for the current decision.

Do not prove the same identity independently through GitHub, Drive, CI, and local tooling unless the gate requires independent paths.

When the canonical hash/count/membership gate matches, stop checking that same fact and move to the next gate.

## 6. Revalidation record

When revalidation is legitimately required, record:

- validation ID/date;
- exact claim;
- dependency/input identity, hash, or version;
- method/script/parameters;
- offsets/ranges/count units when applicable;
- result/status;
- reproducible report/artifact/commit.

## 7. Provenance failure vs semantic failure

A corrupt, missing, or failed transport may block downstream machine consumption without disproving the historical semantic conclusion.

Do not reopen technical byte analysis merely because transport failed when deterministic provenance already establishes the semantic result.

Conversely, do not fabricate missing payload rows from counts, IDs, summaries, edges, or downstream materialization.

## 8. Local-first validation

Prefer deterministic local validation when complete inputs are available.

CI is an independent/final gate, not a repeated exploratory debugger. A logical change should normally produce one automatic final CI run. Do not manually rerun a successful final gate merely for reassurance.

## 9. Cause-family validation

One diagnostic build tests one root-cause family.

All confirmed same-mechanism sites may be tested together. Different hypotheses must not be mixed merely to save runs.

A passing subset is not proof that every member is safe.

## 10. Rejected hypotheses

Rejected or weakened hypotheses remain documented. Do not remove them merely because a later explanation supersedes them.

## 11. Candidate-state language

`PREPIN_PASS` means no known blocker remains under the current candidate inputs and validator definition while one or more required materialized semantic hashes remain unpinned.

It does not mean:

- semantic hashes are pinned;
- schema is frozen;
- future evidence cannot invalidate a dependency;
- all unresolved technical work is solved.

For the schema-v1 candidate, top-level validator `PASS` means:

```text
all current reachable candidate gates pass
AND
all four required materialized semantic hashes are pinned
AND
each pinned hash matches current materialization
```

Candidate `PASS` still does **not** mean the schema is frozen and does not authorize migration, residual-family analysis, builder/runtime work, or game-file modification.

`FROZEN` may be used only after a separately authorized schema-freeze declaration is completed and recorded. No validator transition from `PREPIN_PASS` to `PASS` may implicitly create `FROZEN` state.

## 12. Documentation governance

`tools/validate_document_governance.py` enforces the document authority invariants defined by `docs/DOCUMENT_AUTHORITY_INDEX.json`.

Governance validation must not mutate anchor-protected canonical evidence merely to make metadata easier to validate.
