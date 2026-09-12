# PROJECT_STATE

Last updated: 2026-09-12 (KST)

This file is the **sole project-resume authority**. Historical documents may contain valid evidence and old “next step” language, but they do not override this file.

<!-- PROJECT_RESUME_V2
{
  "schema": "PROJECT_RESUME_V2",
  "scope_id": "SCHEMA_V1_V089_C03_ATOMIC_CLAIM_BLOCKER",
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
Schema v1: **CANDIDATE / NOT FROZEN**.  
Current schema-v1 regression blocker: **`V089.C03` atomic-claim policy**.

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
- schema-v1 amendment: implemented as candidate; regression advanced past V094 and is now blocked by `V089.C03`

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

Semantic identity remains unchanged:

```text
rows                    158
logical content SHA-256 c612bcf55d0c139d55dee42a6a6397f702ead0f1628b47b45c46512fd1b52bff
ordered source IDs SHA  87d5a7531b5e2b3841fe4ba093a87dd9da11e8c85b5d4184c6ae705436c1833e
```

Historical canonical transport provenance remains unchanged:

```text
format      deterministic gzip JSONL
gzip SHA    8bbbeb03695b4bd06f028b9c9cfe0d367af170a012af56803f3a8553356a0b68
```

Current repository transport:

```text
path       docs/manifests/F1_STATIC_WRITE_AUTHORIZATION_MANIFEST/
format     PLAIN_JSONL_SHARDS
rule       preserve canonical V094 order; contiguous groups of 8 rows
shards     20
rows       158
INDEX SHA  ce241ab9a3257e0cf858d4b016eebdcd3c564958e95cdaf23035c0f4dfdfd6d4
repair     d25fd5be5c15aabd1483c0e8bf0ad4873974bb1b
```

The old 21,288-byte and 12,071-byte gzip repository objects remain historical failed transports only. They are recorded in the current transport `INDEX.json` as `FAILED_TRANSPORT_NOT_CANONICAL`; neither is current action authority.

GitHub Actions run `34677635822` independently verified:

```text
shards                         20
rows                           158
logical content SHA-256        c612bcf55d0c139d55dee42a6a6397f702ead0f1628b47b45c46512fd1b52bff
ordered source IDs SHA-256     87d5a7531b5e2b3841fe4ba093a87dd9da11e8c85b5d4184c6ae705436c1833e
reconstructed gzip SHA-256     8bbbeb03695b4bd06f028b9c9cfe0d367af170a012af56803f3a8553356a0b68
```

Therefore the V100 transport blocker is closed.

## Current schema-v1 blocker

The same CI run advanced through the repaired V094 action-table gate and passed the 158-action/action-edge consistency checks. It then failed at:

`atomic_claim_policy: ['V089.C03']`

This is a separate schema-v1 claim-shape cause family. It is not evidence against V094, and it was not modified during the transport repair.

Until that blocker is analyzed and resolved under a fresh execution signal:

- schema v1 remains NOT FROZEN;
- materialized semantic hashes remain unpinned;
- schema-freeze declaration is not authorized.

## Document authority

Default read chain:

```text
AGENTS.md
-> PROJECT_STATE.md
-> PROJECT_STATE.required_reads
```

Document roles, historical-plan supersession, and anchor-protected files are registered in:

`docs/DOCUMENT_AUTHORITY_INDEX.json`

Technical maps, stage reports, handoffs, and historical plans may remain valid evidence without being current resume instructions.

## Current boundaries

- PC patch remains semantic authority.
- raw uniqueness is not a safety rule.
- target resolution is not write authorization.
- no silent UNKNOWN authorization or source omission.
- no force-push.
- no synthesis of missing canonical payload rows from counts/IDs/edges.
- no governance edit to anchor-protected evidence without explicit anchor migration.
- semantic identity and transport identity are separate.
- V094 failed binary/base64 transport routes remain rejected; do not resurrect them.
- do not fix a different schema blocker under the completed V094 repair scope.

## Next authorized scope after a fresh signal

**Analyze the schema-v1 candidate `V089.C03` atomic-claim-policy blocker only.**

Determine whether `V089.C03` should be an explicitly allowed structured atomic exception, superseded/split into appended atomic claims, or whether the current atomicity validator is over-broad. Use the existing immutable-claim/supersession rules and do not change the underlying F1 byte-analysis facts.

After that analysis, report and STOP. A subsequent modification/fix and any schema-freeze decision require separate fresh execution signals.

Do not combine this analysis with full migration, the 797 residual, builder, IPS, runtime, mapping, or game-file work.
