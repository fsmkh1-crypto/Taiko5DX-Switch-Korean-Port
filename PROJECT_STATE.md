# PROJECT_STATE

Last updated: 2026-09-12 (KST)

This file is the **sole project-resume authority**. Historical documents may contain valid evidence and old “next step” language, but they do not override this file.

<!-- PROJECT_RESUME_V2
{
  "schema": "PROJECT_RESUME_V2",
  "scope_id": "V094_TRANSPORT_REPAIR_V2",
  "status": "STOPPED_AWAITING_USER_SIGNAL",
  "required_reads": [
    "docs/ARTIFACT_AND_PROVENANCE_RULES.md",
    "docs/GITHUB_AND_CI_POLICY.md",
    "docs/SCHEMA_V1_AMENDMENT.md",
    "docs/MACHINE_READABLE_ACCOUNTING_SCHEMA.md"
  ],
  "forbidden_scope_expansion": [
    "SCHEMA_FREEZE",
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
Schema v1: **CANDIDATE / NOT FROZEN**.  
V094 repair: **NOT COMPLETE**.

Canonical target:

- Title ID `0100346017304000`
- Switch v1.1.3
- Build ID `D9120950C258610A746F4A31CE3A3B376DE393D9`
- canonical `main` SHA-256 `b366e692208f3c0cc18bc1884ef95689b6b11d722fa2d749b8500abccbc3109b`

## Canonical completed work

- Stage 1 canonical inventory: COMPLETE
- Stage 2 affine structural targeting: COMPLETE
- F1 unique-anchor bounded localization sequence audit: COMPLETE
- F1 historical V094 static-write authorization: COMPLETE as semantic/provenance evidence
- machine-readable accounting v0.1 F1 pilot: PASS
- schema-v1 amendment: implemented as candidate; regression blocked by V094 transport

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

Historical canonical transport provenance remains:

```text
format      deterministic gzip JSONL
gzip SHA    8bbbeb03695b4bd06f028b9c9cfe0d367af170a012af56803f3a8553356a0b68
```

V100 also records the original committed truncation discovered by schema-v1 review:

```text
bytes          21,288
file SHA256    826c73a0f80ae645420a189a4dd7b1e3637afd0e514fbc4f00d84189595daf37
complete rows  55 / 158
```

The current `main` at base commit `b58402a6713800ea32f6151ca26ab0e84c6ad568` contains a later **failed transport artifact**, not a canonical replacement:

```text
path      docs/manifests/F1_STATIC_WRITE_AUTHORIZATION_MANIFEST.jsonl.gz
bytes     12,071
Git blob  9a3bc50b18a51582b2031611a2f46fe1c069a862
status    FAILED_TRANSPORT_NOT_CANONICAL
```

Do not consume that 12,071-byte file as the V094 action table.

A later attempted manual fragmented Git-object route is also rejected as the normal repair method. Do not resume the old “upload progressively smaller blobs and assemble trees” approach merely because partial staging objects exist.

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
- no synthesis of missing V094 actions from counts/IDs/edges.
- no governance edit to anchor-protected evidence without explicit anchor migration.
- semantic identity and transport identity are separate.
- one credible connector transport failure means change the route, not progressively fragment the same payload.

## Next authorized scope after a fresh signal

**V094 transport repair v2 only.**

The next repair must choose a safe exact-byte transport path under the new artifact/GitHub policies, preserve V094 semantic identity and historical gzip provenance, validate the resulting current transport, update bindings/validator only as required by that transport, run the candidate regression, record the result, and STOP.

Schema freeze remains a later separately authorized stage.
