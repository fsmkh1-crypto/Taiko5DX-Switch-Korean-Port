# VALIDATION LEDGER — Documentation Governance v2

Date: 2026-09-12
Base HEAD: `b58402a6713800ea32f6151ca26ab0e84c6ad568`
Scope: documentation authority/governance only. No V094 artifact repair, schema freeze, 797 residual analysis, builder/IPS/runtime work, or game-file modification.

## V101 — Documentation authority and transport-governance closure

Status: **VERIFIED**

### Claim

The repository now separates current resume authority, operating/domain rules, canonical evidence, technical maps, historical plans, archive material, and chronology through a central machine-readable registry without rewriting anchored evidence documents.

### Verified governance invariants

- `INV-DOC-01`: `PROJECT_STATE.md` is the only `PROJECT_RESUME` document with `current_authority=true`.
- `INV-DOC-02`: non-current documents containing plan/next-step wording carry machine-readable supersession metadata pointing to `PROJECT_STATE.md`.
- `INV-DOC-03`: source-anchor-protected evidence is blob-identity locked unless an explicit anchor migration is separately authorized.
- `INV-DOC-04`: default read chain is exactly `AGENTS.md -> PROJECT_STATE.md -> PROJECT_STATE.required_reads`; open-ended conditional pre-reading is prohibited.
- `INV-DOC-05`: every Markdown document in governance scope is indexed exactly once; indexed paths exist; `DOCUMENT_AUTHORITY_INDEX.json` self-registers.

Anchor-protected documents retained byte-identically from base HEAD:

- `docs/VALIDATION_LEDGER_F1.md` — Git blob `058b9f87e99d7b3e6b9a12c4878740545cc98c74`
- `docs/VALIDATION_LEDGER_F1_AUTH.md` — Git blob `4d53132f1281758490b5bb310427e91939362927`
- `docs/F1_LOCALIZATION_SEQUENCE_AUDIT.md` — Git blob `ba9c660cf6f229ec2b19f024b9bc2cef94d26a44`

### V094 transport status normalized for resume purposes

Historical V094 semantics remain unchanged: 158 actions, logical-content SHA-256 `c612bcf55d0c139d55dee42a6a6397f702ead0f1628b47b45c46512fd1b52bff`. Historical canonical gzip transport SHA-256 `8bbbeb03695b4bd06f028b9c9cfe0d367af170a012af56803f3a8553356a0b68` remains provenance.

The file currently present on base `main` is explicitly classified as failed transport, not canonical action payload:

- path `docs/manifests/F1_STATIC_WRITE_AUTHORIZATION_MANIFEST.jsonl.gz`
- bytes `12,071`
- Git blob `9a3bc50b18a51582b2031611a2f46fe1c069a862`
- status `FAILED_TRANSPORT_NOT_CANONICAL`

The earlier V100 21,288-byte truncation remains historical evidence and is not overwritten by this current-state classification.

### Rejected workflow

The attempted connector route of progressively shrinking binary/base64 fragments and assembling many Git blobs/trees is rejected as a normal repair workflow. A credible transport failure must trigger a route redesign rather than further fragmentation of the same transport mechanism. Unreferenced staging Git objects/temporary branches do not become authority.

### Boundary

V101 changes documentation governance only. It does not repair V094, pin schema-v1 semantic hashes, freeze schema v1, migrate the full corpus, analyze the 797 residual, or authorize builder/runtime/game changes.

Next stage remains **V094 transport repair v2 only**, and requires a fresh user execution signal.
