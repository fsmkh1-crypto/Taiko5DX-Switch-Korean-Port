# Project Operating Rules — v2

Date: 2026-09-12  
Status: CANONICAL OPERATING POLICY

## 1. Purpose

This document contains project-wide operating rules that are too detailed for `AGENTS.md` but apply across analysis, documentation, implementation, diagnostics, and migration work.

`AGENTS.md` is the entry point. `PROJECT_STATE.md` is the sole project-resume authority.

## 2. Mandatory read chain

The default read chain is exactly:

```text
AGENTS.md
  -> PROJECT_STATE.md
  -> PROJECT_STATE.required_reads
```

Stop pre-reading once `PROJECT_STATE.md` supplies the current scope and required reads.

Do not use an open-ended “as applicable” judgment to read every historical document. Historical/detail documents are read only when a specific claim, provenance edge, or contradiction requires them.

## 3. Execution and scope gates

- No actual analysis/tool work, modification, build, migration, or commit before a clear user execution signal.
- One signal applies only to the scope agreed at that moment.
- A completed scope returns to STOP.
- A result report never authorizes the next stage.
- A direct documentation request authorizes only that documentation action unless the user explicitly broadens scope.

## 4. Analysis before modification

Analysis and implementation are separate stages.

At the end of analysis, report:

1. 확정된 사실
2. 유력한 가설
3. 미확정 사항
4. 기각된 가설
5. 관련 영향 범위
6. 수정 제안

Then STOP.

## 5. Root-cause-family handling

Do not repair one visible symptom as soon as one cause is found.

First establish the reasonable impact surface of the same mechanism across:

- data classes;
- code paths;
- callers/consumers;
- runtime descriptors/helpers;
- storage/ownership layers;
- analogous symptoms.

One diagnostic build tests one cause family. Proven same-family sites may be tested together.

## 6. PC Korean patch precedence

If the PC Korean patch implements the same semantic feature, it is the first reference for:

- replacement bytes;
- names and translations;
- mapping;
- pointer behavior;
- font/glyph strategy;
- helper/runtime descriptors;
- storage/data structures.

Port actual PC behavior when Switch structure permits it. Diverge only for a concrete Switch architectural or UX reason.

## 7. Evidence and failed hypotheses

Already VERIFIED facts are inherited. Do not repeat them because of a new session/model.

Failed, falsified, or materially weakened hypotheses remain recorded so later work does not repeat them under a new name.

If source data and runtime display disagree, treat that disagreement as a port/rendering/data-selection clue. Do not silently rewrite the intended translation.

## 8. Document authority model

Document roles and authority scopes are machine-readable in `docs/DOCUMENT_AUTHORITY_INDEX.json`.

Important distinction:

```text
evidence_still_valid = true
current_authority     = false
```

means the document remains valid provenance/evidence but its historical planning language is not a current instruction.

`PROJECT_STATE.md` is the only `PROJECT_RESUME` document with `current_authority=true`.

## 9. Anchor-protected evidence

If a machine claim/source anchor binds a document Git blob identity, governance cleanup must not edit or move that document without an explicitly authorized anchor migration.

Authority metadata belongs in the central registry rather than being inserted as front matter into anchor-protected evidence.

## 10. Storage and repository boundaries

Do not commit commercial game files, Switch/PC executables, patch archives/payloads, fonts, keys, dumps, or generated full mod packages.

Hashes, offsets, Build IDs, patch bytes, scripts, manifests, analysis, and reproducibility metadata may be committed.

Large generated artifacts belong in Google Drive and are bound to Git records by stable identity and hash.

## 11. Stage close

Meaningful work closes by:

- updating `PROJECT_STATE.md`;
- updating the relevant validation ledger/index;
- recording rejected/failed approaches where relevant;
- verifying repository state;
- reporting the authorized scope;
- STOP.
