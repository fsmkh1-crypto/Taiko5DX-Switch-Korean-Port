# BOUNDED RESUME READ POLICY

Date: 2026-09-20 (KST)

Status: CANONICAL OPERATING POLICY

## 1. Purpose

This policy prevents repository-resume work from creating a context/I/O bottleneck by dumping
the accumulated full history of long authority files into the active model context.

It changes only how canonical state is read. It does not change product scope, validation
membership, implementation authority, Git history, or any CLOSED/VERIFIED technical fact.

## 2. Binding resume sequence

On every selective-track resume:

1. verify remote `main` HEAD against the expected canonical HEAD;
2. stop and report repository drift before any analysis or write if HEAD differs;
3. read only the root `PROJECT_STATE.md` current overlay and `PROJECT_RESUME_V2` fields needed
   for the current scope;
4. read only the top/current-scope portion of `selective_ko/SELECTIVE_PROJECT_STATE.md`,
   including status, current authority, current artifact and exact next scope;
5. read the latest current-scope authority and artifact INDEX first;
6. read only code/data paths directly required by that scope;
7. expand into an older authority only when the current authority explicitly requires that
   provenance to answer an unresolved question.

## 3. required_reads semantics

`PROJECT_RESUME_V2.required_reads` is a provenance-ordered superset.

It is **not** an instruction to fetch every listed document on every resume.

The current authority/INDEX and this policy are the default bounded resume set. Older entries
are consulted lazily and only when materially required.

## 4. Long-file handling

Do not emit the full contents of accumulated long files into model context merely to resume.

In particular:

- do not bulk-dump all of `PROJECT_STATE.md`;
- do not bulk-dump all of `selective_ko/SELECTIVE_PROJECT_STATE.md`;
- do not bulk-dump all of `selective_ko/KNOWN_FAILURES.md`;
- use targeted sections, parsed resume JSON fields, exact headings, or bounded excerpts;
- if a connector/API returns a whole long file, filter/parse it inside the tool call and emit
  only the bounded fields needed by the current scope.

For `KNOWN_FAILURES.md`, search by current validation ID, cause-family, or exact failure name
and read only the matching section unless a broader audit is explicitly required.

## 5. CLOSED/VERIFIED preservation

A new chat, model, or resume is not a reason to re-read or re-prove CLOSED/VERIFIED facts.

Historical authority is reopened only when:

- a current canonical authority explicitly identifies an unresolved provenance gap;
- new contradictory evidence is supplied;
- exact implementation/validation requires bytes or fields not already preserved.

## 6. Write boundary

This read policy never authorizes implementation, build, package, IPS, hardware testing, or a
repository write by itself.

All existing explicit-signal scope rules and Git object-only write restrictions remain binding.

## 7. Origin / failure prevention

The policy canonicalizes the 2026-09-20 resume bottleneck correction: fetching accumulated
`PROJECT_STATE.md`, `SELECTIVE_PROJECT_STATE.md`, and `KNOWN_FAILURES.md` wholesale produced
large/truncated tool output and avoidable context processing before any V345 implementation work
began.

Binding replacement:

```text
HEAD
-> bounded current resume fields
-> current authority + INDEX
-> exact scope code/data only
-> expand history only on demonstrated need
```
