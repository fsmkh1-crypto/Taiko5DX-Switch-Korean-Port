# GitHub and CI Policy

Date: 2026-09-12  
Status: CANONICAL REPOSITORY OPERATING POLICY

## 1. Stage start

Before a repository-writing stage:

1. read `PROJECT_STATE.md`;
2. verify remote `main` HEAD;
3. use the legitimate newer HEAD if it advanced;
4. never reset/revert legitimate newer work merely to match an older handoff SHA.

## 2. REMOTE_IO_FAST_PATH

Default execution path:

```text
resolve scope and required reads
-> reuse same-HEAD cached reads
-> generate/validate locally
-> freeze changed-file set
-> skip no-op files
-> create required blobs
-> create one tree
-> create one logical commit
-> one HEAD-drift check
-> non-force update_ref(main)
-> verify remote HEAD/tree once
-> observe one automatic CI run when required
-> STOP
```

The purpose is to reduce both latency and tool-selection risk by finishing decisions before remote writes begin.

## 3. Same-HEAD read cache

For the same canonical HEAD, do not refetch the same path unless:

- the path itself changed;
- a previously unread range is specifically needed;
- a concrete provenance/identity question cannot be answered from the cached read.

Tool-schema rediscovery for an already-used action is operational waste. Avoid it unless the available schema is genuinely unavailable or ambiguous.

## 4. Freeze the write plan before writing

Before the first remote write, determine:

- base HEAD/tree;
- exact changed-file set;
- which files are true no-ops;
- required new blob identities;
- expected tree/commit/ref operations;
- whether CI is required.

Do not discover new unrelated changes during the write phase.

For a planned Git-object stage, the operational write checklist is:

```text
create_blob
create_tree
create_commit
update_ref(main, force=false)
```

This checklist is an operator discipline, not a repository-enforced sandbox. If a different write route is intentionally required, authorize it as a new scope/transport decision first.

## 5. Canonical mutation boundary

Dangling blobs, trees, and commits are not project authority.

For the Git-object route, canonical state changes only when the intended branch ref is moved. Before `update_ref(main)`, temporary objects may physically exist but do not change the project resume authority.

Contents-API writes are different because they directly mutate a branch; do not mix them into an allowlisted Git-object closure stage.

## 6. No-op and original-boundary rules

Do not write a file whose resulting content/blob identity is unchanged.

Preserve original file boundaries unless there is a proven transport reason to change them. Do not pad, combine, or shard small files merely to reach a probe size.

The successful ~37.5 KiB validator blob is evidence that this size can travel intact through the tested Git-object route. It is not a universal size limit or minimum.

## 7. Transport failures

Do not repeatedly create progressively smaller blobs/shards after a credible integrity failure.

If the same transport route fails twice for the same cause family, do not make a third attempt. STOP and redesign the route.

Fragment count is itself remote-I/O cost. When sharding is required, use the fewest deterministic parts compatible with the proven safe transport and semantic ordering rules.

## 8. Commit discipline

Group one logical stage into one commit when practical.

Do not create a chain of tiny branch mutations merely because an API exposes per-file writes.

Force-push is forbidden. Preserve accidental or failed history that already reached `main`; recover forward and record provenance.

## 9. Remote verification

After the ref move, verify only what proves the intended canonical mutation:

- remote `main` HEAD;
- intended tree/path identity where necessary;
- required hash/count/validator result.

Do not re-prove the same identity through several remote APIs.

## 10. CI

CI is for independent regression, release/merge gates, full-corpus validation, and builds that require CI infrastructure.

A completed logical change should normally trigger one automatic final CI run. If that run succeeds, do not manually dispatch, rerun, or create a second equivalent CI check.

If a workflow did not trigger because its path filters are incomplete, treat that as a change-detection defect to fix; do not normalize manual dispatch as the permanent solution.

## 11. Metrics

When repository I/O performance matters, record only measured values:

- read calls;
- blob/tree/commit/ref writes;
- CI runs;
- measured call/run durations when available.

Do not invent timings. Separate Git object latency from orchestration, schema discovery, repeated reads, and failure-recovery overhead.

## 12. Stop condition

STOP rather than improvising when:

- the exact-byte write route is not safe;
- the write plan must expand into a different cause family;
- the same route has failed twice;
- an unexpected branch mutation or disallowed write path occurs;
- remote HEAD advanced and invalidates the prepared parent/tree assumptions.

Redesign under a fresh explicit scope before resuming.
