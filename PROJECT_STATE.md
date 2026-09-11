# PROJECT_STATE

Last updated: 2026-09-11 (KST)

## Current status

Repo: `fsmkh1-crypto/Taiko5DX-Switch-Korean-Port`
Branch: `main`

Stage 1 canonical inventory: COMPLETE.
Stage 2 affine structural targeting: COMPLETE.
No builder/IPS/runtime implementation is authorized by Stage 2.

Canonical target:
- Title ID `0100346017304000`
- Switch v1.1.3
- Build ID `D9120950C258610A746F4A31CE3A3B376DE393D9`
- `main` SHA-256 `b366e692208f3c0cc18bc1884ef95689b6b11d722fa2d749b8500abccbc3109b`

## Accounting snapshot

```text
source-ledger rows                 27,430
inline rows                        17,103
Stage-1 raw exceptions             11,050
Stage-2 affine target-resolved     13,771
Stage-1 exceptions target-resolved  9,802
residual exceptions                 1,248
```

Residual families:

```text
LOCALIZATION_CANDIDATE  886
  1 full JP candidate   608
  2+ candidates         189
  0 full JP candidate    89
UNCLASSIFIED_INLINE     327
FORMATTER_CANDIDATE      35
```

## Canonical documents

- rules: `docs/PC_TO_SWITCH_PORTING_RULE_FRAMEWORK.md`
- invariants: `docs/PC_TO_SWITCH_ACCOUNTING_INVARIANTS.md`
- Stage 1: `docs/FULL_PORT_INVENTORY_STAGE1.md`
- Stage 2: `docs/STAGE2_AFFINE_STRUCTURAL_TARGETING.md`
- validation index: `docs/VALIDATION_LEDGER.md`

R0/R1/R1B/R1C and PC runtime facts remain canonical; do not revalidate them merely because a new chat/model is used.

## Mandatory boundaries

- PC patch is semantic authority.
- raw uniqueness is not a safety rule.
- target resolution is not write authorization.
- preserve internal Japanese yomi until I7 is resolved.
- consumer tracing is an exception/family tool, not the default for structurally resolved rows.
- one diagnostic build = one root-cause family.
- no force-push and no silent source omission.

## Next stage

Fresh execution signal required.

Priority: residual localization family `886`, starting with the `608` single-full-JP-candidate rows and deriving corpus-wide context rules before individual consumer tracing.

After localization: unclassified `327`, formatter/composite `35`, yomi decision, then pointer/mapping/runtime/RomFS/cross-axis closure.

Do not modify builder or generate IPS/ZIP/runtime diagnostics without separate authorization.
