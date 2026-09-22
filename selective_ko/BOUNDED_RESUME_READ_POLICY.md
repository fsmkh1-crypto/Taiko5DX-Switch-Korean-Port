# BOUNDED RESUME READ POLICY

Date: 2026-09-22 (KST)

Status: CANONICAL OPERATING POLICY

## 1. Purpose

This policy prevents repository resume from turning accumulated project history into an active context/I/O bottleneck.

It changes only how canonical state is routed and read. It does not change product scope, validation membership, implementation authority, Git history, or any CLOSED/VERIFIED technical fact.

## 2. Binding resume sequence

On every selective-track resume:

1. verify remote `main` HEAD against the expected canonical HEAD;
2. stop and report repository drift before any analysis or write if HEAD differs;
3. read `AGENTS.md`;
4. read the compact root `PROJECT_STATE.md`;
5. read only the active paths in `PROJECT_RESUME_V2.required_reads`;
6. read the current checkpoint/INDEX before opening historical provenance;
7. load exact-scope code or row-level artifacts only when the authorized task actually consumes them;
8. expand historical provenance only for a concrete unresolved provenance question.

## 3. Active required_reads semantics

`PROJECT_RESUME_V2.required_reads` is the active bounded bootstrap set.

It is not a historical provenance superset.

Rules:

- keep the list finite and deduplicated;
- include routing/decision authorities needed to understand the current authorized boundary;
- do not place large row-level execution inputs in this list merely because an implementation consumes them;
- do not place the historical dependency catalog itself in the bootstrap set;
- repository-writing scopes must include `docs/GITHUB_AND_CI_POLICY.md`;
- the current state may declare an `active_read_budget_max`; exceeding it is a governance failure unless that budget is deliberately revised by an authorized migration.

## 4. Dependency classes

Resume dependencies are separated into four classes:

```text
routing dependency
  read during bootstrap

decision dependency
  read when resolving the authorized scope

execution input
  load programmatically when the authorized work consumes its bytes

historical provenance
  retrieve only for a specific provenance question
```

A serializer needing a complete ledger does not imply that every ledger row belongs in conversational bootstrap context.

## 5. Historical discovery

Historical dependency discovery is routed through:

`selective_ko/RESUME_HISTORY_INDEX.json`

The catalog points to pinned historical state snapshots and authority locations. Historical evidence remains canonical for its declared scope even when it is no longer active resume input.

Do not rewrite an old checkpoint merely to mark it inactive.

## 6. Long-file handling

Do not bulk-dump accumulated long files into model context merely to resume.

In particular:

- do not bulk-dump historical versions of `PROJECT_STATE.md`;
- do not bulk-dump historical versions of `selective_ko/SELECTIVE_PROJECT_STATE.md`;
- do not bulk-dump all of `selective_ko/KNOWN_FAILURES.md`;
- use compact indexes, targeted headings, exact locators, or bounded excerpts;
- filter connector/API results before emitting them when the tool supports it.

Use `selective_ko/KNOWN_FAILURES_INDEX.json` to locate the relevant detailed failure section.

## 7. CLOSED/VERIFIED preservation

A new chat, model, or resume is not a reason to re-read or re-prove CLOSED/VERIFIED facts.

Historical authority is reopened only when:

- a current canonical authority identifies a concrete unresolved provenance gap;
- new contradictory evidence is supplied;
- exact implementation/validation requires bytes or fields not preserved by the active authority;
- a demonstrated flaw in the prior method invalidates the relevant claim.

## 8. Large-artifact retrieval

Large canonical artifacts remain outside Git when their active access pattern does not justify Git residency.

Default retrieval order:

```text
resolve pinned INDEX
-> reuse verified local cache if available
-> otherwise retrieve pinned external artifact
-> verify transport/member identity
-> load/filter required records programmatically
-> expose only relevant excerpts
```

Sharding is transport only and must never redefine semantic membership or serializer transaction boundaries.

## 9. Write boundary

This read policy does not authorize implementation, build, package, IPS, hardware testing, or repository writes by itself.

All explicit-signal scope rules and Git object-only write restrictions remain binding.

## 10. Origin and supersession

This policy supersedes the earlier interpretation in which `required_reads` remained a provenance-ordered historical superset.

Historical dependency paths remain preserved through the pinned V369 state snapshot and `RESUME_HISTORY_INDEX.json`.

Binding replacement:

```text
HEAD
-> AGENTS.md
-> compact PROJECT_STATE
-> active required_reads
-> exact-scope execution inputs
-> lazy historical provenance only when demonstrated necessary
```
