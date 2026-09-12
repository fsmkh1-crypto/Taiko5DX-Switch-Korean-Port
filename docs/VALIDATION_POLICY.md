# Validation Policy

Date: 2026-09-12  
Status: CANONICAL VALIDATION OPERATING POLICY

## 1. Reuse verified facts

A VERIFIED or VERIFIED-RUNTIME fact is reused unless one of these triggers exists:

- input identity/version/hash changed;
- new evidence directly contradicts it;
- provenance is insufficient for the present decision;
- the prior method is demonstrated unsound.

A new chat, model, tool, or agent is never a revalidation trigger.

## 2. Minimal proof path

Use the shortest evidence path that is sufficient for the current decision.

Do not prove the same identity independently through GitHub, Drive, CI, and local tooling unless the current gate actually requires independent paths.

When a canonical hash/count/membership gate matches, stop checking that same fact and move to the next gate.

## 3. Revalidation record

When revalidation is legitimately required, record:

- validation ID/date;
- exact claim;
- input identity/hash/version;
- method/script/parameters;
- offsets/ranges/count units;
- result/status;
- reproducible report/artifact/commit.

## 4. Failure of provenance is not automatic failure of semantics

A corrupt, missing, or failed transport can block downstream machine consumption without disproving the historical semantic conclusion.

Do not reopen technical byte analysis merely because a transport artifact is unavailable if deterministic provenance already establishes the semantic result.

Conversely, do not fabricate missing payload rows from counts, IDs, summaries, or edges.

## 5. Status meanings

Keep these states distinct:

```text
PASS      condition evaluated and satisfied
FAIL      condition evaluated and violated
STALE     prior result no longer matches dependency identity
BLOCKED   evaluation/consumption cannot complete because required evidence/input is unavailable
UNKNOWN   unresolved semantic/evidence state
```

STALE is not FAIL. BLOCKED is not technical disproof.

## 6. Local-first validation

Prefer local deterministic validation before CI when the environment has the complete inputs.

CI is used as an independent/final gate, not as a repeated exploratory debugger.

If the current environment cannot safely materialize the exact repository/input tree, record that limitation and use one final repository CI gate rather than many speculative runs.

## 7. Cause-family validation

One diagnostic build tests one root-cause family.

All confirmed same-mechanism sites may be tested together. Different hypotheses must not be mixed merely to save runs.

A passing split is not proof that every member is safe.

## 8. Rejected hypotheses

Rejected or weakened hypotheses remain documented. Do not remove them merely because a later explanation supersedes them.

## 9. Documentation governance

`tools/validate_document_governance.py` enforces the document authority invariants defined by `docs/DOCUMENT_AUTHORITY_INDEX.json`.

Governance validation must not mutate anchor-protected canonical evidence just to add role metadata.
