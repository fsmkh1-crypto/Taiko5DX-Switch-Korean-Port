# PROJECT_STATE

Last updated: 2026-09-12 (KST)

This file is the **sole project-resume authority**. Historical documents may contain valid evidence and old “next step” language, but they do not override this file.

<!-- PROJECT_RESUME_V2
{
  "schema": "PROJECT_RESUME_V2",
  "scope_id": "SOURCE_ANCHOR_PROVENANCE_CLOSURE",
  "status": "IN_PROGRESS",
  "required_reads": [
    "docs/VALIDATION_POLICY.md",
    "docs/MACHINE_READABLE_ACCOUNTING_SCHEMA.md",
    "docs/CLAIM_EXTRACTION_RULES.md",
    "docs/VALIDATION_LEDGER_SCHEMA_V1_AMENDMENT.md"
  ],
  "forbidden_scope_expansion": [
    "SCHEMA_FREEZE_DECLARATION",
    "FULL_MIGRATION",
    "797_RESIDUAL_ANALYSIS",
    "BUILDER_IPS_RUNTIME",
    "GAME_FILE_MODIFICATION"
  ]
}
PROJECT_RESUME_V2 -->

## Current repository state

Repository: `fsmkh1-crypto/Taiko5DX-Switch-Korean-Port`  
Branch: `main`

Documentation Governance v2: **COMPLETE** after V101.  
V094 transport repair v2: **COMPLETE** after V102.  
Structured atomic-claim cause family: **COMPLETE** after V103.  
Schema v1: **CANDIDATE / NOT FROZEN**.  
Current authorized work: **source-anchor/provenance closure only**.

Canonical target:

- Title ID `0100346017304000`
- Switch v1.1.3
- Build ID `D9120950C258610A746F4A31CE3A3B376DE393D9`
- canonical game `main` SHA-256 `b366e692208f3c0cc18bc1884ef95689b6b11d722fa2d749b8500abccbc3109b`

## Canonical completed work

- Stage 1 canonical inventory: COMPLETE
- Stage 2 affine structural targeting: COMPLETE
- F1 unique-anchor bounded localization sequence audit: COMPLETE
- F1 historical V094 static-write authorization: COMPLETE as semantic/provenance evidence
- V094 machine-consumable repository transport: COMPLETE as deterministic plain JSONL shards
- machine-readable accounting v0.1 F1 pilot: PASS
- schema-v1 amendment: candidate only; regression passed V094 transport and V103 structured-claim gates and is now in source-anchor/provenance closure

Current accounting facts remain:

```text
historical mixed-granularity inventory records  27,430
leaf-obligation records after descriptor groups 27,419
inline rows                                      17,103
Stage-1 raw exceptions                           11,050
Stage-2 residual                                  1,248
conservative later target-resolved                  451
conservative target-unresolved residual              797
```

F1 population remains:

```text
DIRECT_PORT authorized                    158
PADDING_RECONSTRUCTION_REQUIRED            75
SHARED_OWNER_BINDING_REQUIRED              25
TERMINATOR_CAPACITY_FAIL                    4
F1_RULE_REJECTED                           16
TOTAL                                     278
```

The 25 shared-owner rows remain `SHARED_OWNER_BINDING`; replacement conflict is not proven.

## V094 semantic and transport state

Semantic identity is unchanged:

```text
rows                    158
logical content SHA-256 c612bcf55d0c139d55dee42a6a6397f702ead0f1628b47b45c46512fd1b52bff
ordered source IDs SHA  87d5a7531b5e2b3841fe4ba093a87dd9da11e8c85b5d4184c6ae705436c1833e
```

Historical gzip provenance remains `8bbbeb03695b4bd06f028b9c9cfe0d367af170a012af56803f3a8553356a0b68`.

Current repository transport:

```text
path       docs/manifests/F1_STATIC_WRITE_AUTHORIZATION_MANIFEST/
format     PLAIN_JSONL_SHARDS
shards     20
rows       158
INDEX SHA  ce241ab9a3257e0cf858d4b016eebdcd3c564958e95cdaf23035c0f4dfdfd6d4
repair     d25fd5be5c15aabd1483c0e8bf0ad4873974bb1b
```

## V103 atomic-claim closure

Commit:

`9df784890b9f21f79187ed67825919fedf4d77f7` — `fix: close structured atomic-claim classification gaps`

The effective F1 candidate now has:

```text
base claims       42
new claims        55
effective claims  97
ACTIVE claims     87
```

All ACTIVE structured claim values must be explicitly registered as `structured_atomic_exceptions`; the V094 transport-aware validator hard-fails on any unregistered structured ACTIVE claim, any registry entry that is no longer ACTIVE/structured, duplicate registry IDs, or a claim classified as both split and structured-atomic.

`V089.C03` is retained as one exhaustive historical 278-row storage partition (`197 full-window + 81 padding-mismatch`) because V093 exact replay reproduces that same split.

`V094.C04` is SUPERSEDED and split into:

- `V094.C23` — terminal disposition overlay
- `V094.C24` — action family
- `V094.C25` — action status

Materialization claim references were updated accordingly; edge provenance now uses `V094.C14` for the unique action-ID assertion.

## Current source-anchor/provenance closure

Known current blocker before this stage:

`anchor_text_present_V092.C04: None`

Diagnosis established that V092.C04 stores an anchor phrase from `docs/F1_LOCALIZATION_SEQUENCE_AUDIT.md` while binding it to `docs/VALIDATION_LEDGER_F1.md`. Existing source coverage already binds the same V092 assertion family to the audit document's `8. Accounting correction` section.

This stage may correct claim source-anchor metadata and strengthen anchor validation. It must not edit anchor-protected canonical evidence documents or change underlying V092/F1 technical semantics.

## Current boundaries

- schema v1 remains NOT FROZEN;
- materialized semantic hashes remain unpinned;
- PC patch remains semantic authority;
- raw uniqueness is not a safety rule;
- target resolution is not write authorization;
- no silent UNKNOWN authorization or source omission;
- no force-push;
- no synthesis of canonical rows from counts/IDs/edges;
- no governance edit to anchor-protected evidence without explicit anchor migration;
- do not reopen V094 transport or the V103 atomic cause family without a legitimate revalidation trigger.

## Current authorized scope

**Close the source-anchor/provenance cause family only.**

- correct V092.C04 source binding without changing canonical evidence text;
- audit base and appended claim provenance locators;
- verify `heading_path` exists and `anchor_text` occurs within the claimed heading section, not merely somewhere in the document;
- support explicit source-anchor overrides for appended claims when inherited provenance would be too coarse;
- run one candidate regression and record the next first blocker, if any.

Do not combine this with authority-freshness cleanup, CI trigger cleanup, generated-status cleanup, schema freeze, full migration, the 797 residual, builder, IPS, runtime, mapping, or game-file work.
