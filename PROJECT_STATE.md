# PROJECT_STATE

Last updated: 2026-09-12 (KST)

This file is the **sole project-resume authority**. Historical documents may contain valid evidence and old “next step” language, but they do not override this file.

<!-- PROJECT_RESUME_V2
{
  "schema": "PROJECT_RESUME_V2",
  "scope_id": "SCHEMA_V1_V092_C04_SOURCE_ANCHOR_BLOCKER",
  "status": "STOPPED_AWAITING_USER_SIGNAL",
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
Current schema-v1 regression blocker: **`V092.C04` source-anchor text presence**.

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
- schema-v1 amendment: candidate only; regression now passes the structured atomic-claim gate and is blocked by `V092.C04` anchor provenance

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

All ACTIVE structured claim values must be explicitly registered as `structured_atomic_exceptions`; the V094 transport-aware validator now hard-fails on any unregistered structured ACTIVE claim, any registry entry that is no longer ACTIVE/structured, duplicate registry IDs, or a claim classified as both split and structured-atomic.

`V089.C03` is retained as one exhaustive historical 278-row storage partition (`197 full-window + 81 padding-mismatch`) because V093 exact replay reproduces that same split.

`V094.C04` is SUPERSEDED and split into:

- `V094.C23` — terminal disposition overlay
- `V094.C24` — action family
- `V094.C25` — action status

Materialization claim references were updated accordingly; edge provenance now uses `V094.C14` for the unique action-ID assertion.

GitHub Actions run `34679464287` passed the structured-claim gate and then first failed at:

`anchor_text_present_V092.C04: None`

This is a separate source-anchor/provenance cause family. It is not an atomic-claim failure and is not evidence against V094/F1 technical facts.

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

## Next authorized scope after a fresh signal

**Analyze the schema-v1 candidate `V092.C04` source-anchor text-presence blocker only.**

Determine whether the stored `anchor_text`, bound document identity, coverage extraction, or supersession/migration metadata is stale or malformed. Do not alter the underlying V092/F1 technical fact merely to satisfy the anchor gate.

After that analysis, report and STOP. Any fix and any schema-freeze decision require separate fresh execution signals.

Do not combine this analysis with full migration, the 797 residual, builder, IPS, runtime, mapping, or game-file work.
