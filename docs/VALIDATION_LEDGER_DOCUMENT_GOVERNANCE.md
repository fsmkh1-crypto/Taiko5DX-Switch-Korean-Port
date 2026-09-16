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

## V209 — Documentation-governance drift repair

Date: 2026-09-13  
Base HEAD: `51247b28ed77a7e8a39e33953cc78f66ff45159e`  
Status: **VERIFIED**

### Claim

The post-V101 governance drift is limited to metadata synchronization. Eight later canonical Markdown documents were materialized without corresponding entries in `docs/DOCUMENT_AUTHORITY_INDEX.json`, and `PROJECT_RESUME_V2.scope_kind` drifted from the canonical enum to a stage-specific label.

The affected canonical semantic documents themselves are not reopened or modified.

### Verified repair scope

- register exactly the eight Markdown paths reported by the failing `INV-DOC-05` machine gate;
- classify them as retained canonical evidence with `PROJECT_STATE.md` as plan/resume supersession authority;
- restore `PROJECT_RESUME_V2.scope_kind` to canonical `READ_ONLY`;
- keep `scope_id` as the descriptive stage identity;
- leave FZ001, Stage 1, Stage 2, F1, forward-986, Oracle/Assisted/Astra/TRACE, semantic-owner, action-collapse, write-authority, builder/runtime, and game-file state unchanged.

### Rejected repair paths

- weakening `INV-DOC-05` to ignore the missing documents;
- narrowing `markdown_scope` to hide materialized canonical documents;
- expanding the accepted `scope_kind` enum with stage-specific values;
- rewriting any of the eight semantic evidence documents merely to satisfy governance metadata.

### Boundary

V209 is a governance-only repair. It creates no new semantic conclusion, no new Switch write authorization, no builder/IPS/runtime work, and no game-file modification.

The final repository state must pass the existing unmodified `tools/validate_document_governance.py` machine gate.

## V271 — Documentation-governance recurrence repair

Date: 2026-09-16  
Base HEAD: `2e9760b561e421c8ee717410f54e2a484829d8d8`  
Implementation commit: `5e0cec7f233f85b0f5ec8b75fe3e6615930a1151`  
Status: **VERIFIED PENDING FINAL CI READBACK**

### Claim

The governance failure observed after TAI5MSG structure-index materialization is a recurrence of the V209 metadata-drift cause family, not a TAI5MSG artifact failure. The first failing invariant was `INV-DOC-05`; after accounting for that gate, the current resume header also carried two latent contract drifts: noncanonical `scope_kind=CANONICAL_STATE_OVERLAY` and missing frozen-FZ001 provenance bindings required by the unchanged validator.

### Repair scope

- register the eight existing Markdown paths reported by the failing `INV-DOC-05` gate without altering their semantic contents;
- restore `PROJECT_RESUME_V2.scope_kind` to canonical `READ_ONLY`, preserving the descriptive stage identity in `scope_id`;
- restore the previously VERIFIED FZ001 declaration path/blob and basis validation/run/head provenance values;
- retain `tools/validate_document_governance.py` byte-identically; V209's rejected enum-expansion/validator-weakening routes remain rejected;
- preserve the issue-C next priority `DIALOGUE_FORMATTER_PC_SWITCH_PREDICATE_STATE_PARITY_READ_ONLY`;
- create no new Switch write authorization and modify no game/runtime/TAI5MSG payload.

### Registered recurrence set

- `docs/CWTDAT_AUXILIARY_NAME_ROW_HOLD.md`
- `docs/DIALOGUE_FORMATTER_PC_ORIGINAL_TO_KOREAN_GRAPH_DIFF_CLOSURE_20260916.md`
- `docs/POINTER_56_CROSS_AXIS_ACTION_INTEGRATION.md`
- `docs/RUNTIME_BYTE_COPY_NORMALIZATION_GENERIC_PARSER_OWNER_CLOSURE_20260915.md`
- `docs/RUNTIME_BYTE_COPY_NORMALIZATION_LOWLEVEL_OWNER_CHECKPOINT_20260915.md`
- `docs/RUNTIME_BYTE_COPY_NORMALIZATION_ROUTE_BINDING_C2_TABLE_CLOSURE_20260915.md`
- `docs/RUNTIME_BYTE_COPY_NORMALIZATION_ROUTE_BINDING_PROGRESS_20260915.md`
- `docs/VALIDATION_LEDGER_POINTER_56_CROSS_AXIS_ACTION_INTEGRATION.md`

### Rejected/superseded repair paths

- treating the TAI5MSG materialization as the cause of the CI failure — REJECTED;
- weakening Markdown coverage or excluding the eight documents — REJECTED;
- adding a new `execution_mode` field and expanding validator semantics — REJECTED by the existing V209 contract;
- modifying frozen FZ001 evidence instead of restoring its resume provenance — REJECTED;
- force-moving or rewriting branch history — REJECTED.

### Boundary

V271 repairs repository governance metadata only. It does not change frozen evidence, localization semantics, runtime behavior, game files, the TAI5MSG 33-block/14,832-message artifact, or existing WRITE_SAFE cardinality.

Final status becomes fully VERIFIED only after the automatic `Document governance` workflow passes on the final fast-forward `main` commit.
