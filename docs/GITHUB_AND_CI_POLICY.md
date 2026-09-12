# GitHub and CI Policy

Date: 2026-09-12  
Status: CANONICAL REPOSITORY OPERATING POLICY

## 1. Stage start

Before a repository-writing stage:

1. read `PROJECT_STATE.md`;
2. verify remote `main` HEAD;
3. use the legitimate newer HEAD if it advanced;
4. never reset/revert legitimate newer work merely to match an older handoff SHA.

## 2. Preferred work path

```text
confirm input identity
-> generate locally or in one exact supported environment
-> local validator
-> count/hash checks
-> one logical Git change set
-> non-force push/fast-forward
-> remote HEAD/tree/identity verification
-> CI once when required
-> ledger/state update
-> STOP
```

## 3. Commit discipline

Group one logical stage into one commit when practical.

Do not create a sequence of tiny repository commits merely because a connector exposes one-file write operations.

Temporary Git objects are not project authority until referenced by the intended tree/commit/ref.

Temporary branches are not canonical state unless explicitly promoted.

## 4. Binary and large-payload transport

Do not use manual long binary/base64 tool arguments as the default path.

Do not repeatedly create progressively smaller Git blobs to work around truncation.

If one credible payload-integrity failure occurs, stop that route and select a transport method that can preserve exact bytes.

Small UTF-8 text files are preferred when the data model permits them.

For large files, use a native file-reference path or Google Drive rather than manually embedding bytes in connector calls.

## 5. Remote verification

After a write, verify only what is needed to prove the commit carried the intended change:

- remote `main` HEAD;
- affected path/tree identity;
- required row count/hash/validator result.

Do not repeat the same verification through several APIs once identity is established.

## 6. CI

CI is for:

- independent regression;
- release/merge gates;
- full-corpus validation;
- builds that actually require CI infrastructure.

Do not use Actions repeatedly for simple file inspection or to compensate for an unverified connector upload path.

A stage should normally need at most one final CI validation of the completed logical change.

## 7. Force and history

Force-push is forbidden.

Preserve historical failed commits/transport states when they already exist; correct them with a forward commit and explicit provenance.

## 8. Stop condition

If the available connector cannot perform a required exact-byte write safely, do not build a complicated chain of fragments/trees as a workaround.

STOP, record the transport limitation, and redesign the path before resuming the artifact repair.
