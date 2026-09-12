# Project Operating Rules — v3

Date: 2026-09-12  
Status: CANONICAL OPERATING POLICY

## 1. Purpose and authority

This document contains project-wide operating rules that are too detailed for `AGENTS.md`.

Authority chain:

```text
AGENTS.md
  -> PROJECT_STATE.md
  -> PROJECT_STATE.required_reads
```

`PROJECT_STATE.md` is the sole project-resume authority. Domain specifications, machine bindings and canonical evidence retain only their narrower registered authority.

## 2. Execution and scope gates

- No analysis/tool work, modification, build, migration, or commit before an explicit user signal such as `시작`, `해`, `진행`, or `ㄱㄱ`.
- One signal applies only to the scope agreed at that moment.
- Analysis and modification are separate stages.
- After analysis, report `확정된 사실 / 유력한 가설 / 미확정 사항 / 기각된 가설 / 관련 영향 범위 / 수정 제안` and STOP.
- A result report never authorizes the next stage.
- Scope discipline outranks remote-I/O convenience. Do not combine separately forbidden cause families merely to save a ref update or CI run.

## 3. Read discipline

Stop broad discovery once `PROJECT_STATE.md` supplies the current scope and required reads.

Under the same canonical HEAD:

- do not fetch the same path twice unless a specific new need exists;
- reuse already-read canonical content;
- read historical/detail documents only for a concrete provenance claim, contradiction, or dependency.

A new chat, model, tool, or agent is never by itself a reason to reread or revalidate canonical material.

## 4. Analysis before modification

Once a common mechanism is identified, survey its reasonable impact surface before proposing a fix:

- data classes;
- code paths;
- callers/consumers;
- runtime descriptors/helpers;
- storage/ownership layers;
- analogous symptoms.

One diagnostic build tests one cause family. Proven same-mechanism sites may be tested together; unrelated hypotheses must not be mixed.

## 5. PC Korean patch precedence

If the PC Korean patch implements the same semantic feature, it is the first reference for:

- replacement bytes;
- names and translations;
- mapping;
- pointer behavior;
- font/glyph strategy;
- helper/runtime descriptors;
- storage/data structures.

Port actual PC behavior when Switch structure permits it. Diverge only for a concrete Switch architectural or UX reason.

## 6. Evidence and failed hypotheses

Already VERIFIED facts are inherited according to `docs/VALIDATION_POLICY.md`.

Failed, falsified, or materially weakened hypotheses remain recorded so later work does not repeat them under a new name.

If source data and runtime display disagree, treat the disagreement as a port/rendering/data-selection clue. Do not silently rewrite intended translations or proper names.

## 7. Document and machine-state roles

`docs/DOCUMENT_AUTHORITY_INDEX.json` classifies document authority.

Keep these roles distinct:

```text
PROJECT_STATE         current resume authority
operating/domain MD   current policy/specification
historical MD         evidence/provenance, not current plan
canonical machine data structured state/evidence under its declared schema
generated outputs     reproducible views/status, not authority unless explicitly promoted
```

The project direction is to move mutable accounting state into structured JSON/JSONL canonical stores after an explicit schema freeze and migration stage. Markdown does not become obsolete: anchor-protected and historical Markdown remains canonical evidence, while human-readable current summaries may later be generated from stronger machine state.

Do not silently promote generated output into authority.

## 8. Anchor-protected evidence

If a machine claim/source anchor binds a document Git blob identity, governance cleanup must not edit or move that document without an explicitly authorized anchor migration.

Authority metadata belongs in the central registry rather than being inserted into anchor-protected evidence.

## 9. Repository and artifact boundaries

Do not commit commercial game files, Switch/PC executables, patch archives/payloads, fonts, keys, dumps, or generated full mod packages.

Hashes, offsets, Build IDs, patch bytes, scripts, manifests, analysis, and reproducibility metadata may be committed.

Large generated artifacts belong in Google Drive and are bound to Git records by stable identity and hash.

Repository execution follows `docs/GITHUB_AND_CI_POLICY.md`; artifact identity and transport follow `docs/ARTIFACT_AND_PROVENANCE_RULES.md`.

## 10. Stage close

Meaningful work closes by:

- updating `PROJECT_STATE.md`;
- updating the relevant ledger/index when the stage creates or changes validation/provenance facts;
- recording rejected/failed approaches where relevant;
- verifying the remote repository state;
- observing only the required final CI;
- reporting the authorized scope;
- STOP.

A later stage requires a fresh user signal.
