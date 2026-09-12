# PROJECT_STATE

Last updated: 2026-09-12 (KST)

## Current status

Repo: `fsmkh1-crypto/Taiko5DX-Switch-Korean-Port`
Branch: `main`

Stage 1 canonical inventory: COMPLETE.
Stage 2 affine structural targeting: COMPLETE.
F1 unique-anchor bounded localization sequence audit: COMPLETE.
F1 158-row static write authorization/provenance closure: COMPLETE.
Machine-readable accounting schema + F1 278-row pilot: COMPLETE / PASS / NOT FROZEN.

The exact 158 F1 actions remain row-level `DIRECT_PORT` authorized for future static builder consumption, subject to their existing V094 manifest guards. The machine-accounting pilot does not reauthorize them and does not modify builder/IPS/runtime/game data.

Canonical target:
- Title ID `0100346017304000`
- Switch v1.1.3
- Build ID `D9120950C258610A746F4A31CE3A3B376DE393D9` (canonical 20-byte identity; NSO header field `0x40:0x60` contains this value plus 12 zero padding bytes)
- `main` SHA-256 `b366e692208f3c0cc18bc1884ef95689b6b11d722fa2d749b8500abccbc3109b`

## Accounting snapshot

```text
historical mixed-granularity inventory records  27,430
leaf-obligation records after descriptor groups 27,419
inline rows                                      17,103
Stage-1 raw exceptions                           11,050
Stage-2 affine target-resolved                   13,771
Stage-1 exceptions target-resolved                9,802
Stage-2 residual                                  1,248
post-Stage2 provisional target-resolved             467
F1 rows returned by stricter gate                    16
conservative later target-resolved                   451
conservative target-unresolved residual              797
```

`27,430` and `27,419` are not universal progress percentages. Progress is tracked by family/axis with fixed denominators.

## F1 machine-accounting pilot snapshot

```text
pilot sources                     278
analysis RESOLVED                 262
analysis ANALYZED_UNRESOLVED       16
target RESOLVED                   262
closure CLOSED                    158
closure OPEN                      120
verified exclusions                0
actions                           158
source/action edges               158
atomic validation claims           42
source-coverage blocks              61
unexplained coverage blocks          0
migration-manifest entities        697
```

Blocker split remains canonical:

```text
DIRECT_PORT authorized                    158
PADDING_RECONSTRUCTION_REQUIRED            75
SHARED_OWNER_BINDING_REQUIRED              25
TERMINATOR_CAPACITY_FAIL                    4
F1_RULE_REJECTED                           16
TOTAL                                     278
```

Write-authority responsibility is family-scoped:

```text
F1_LOCALIZATION_STATIC_DIRECT  158 / 158
F1_PADDING_RECONSTRUCTION        0 / 75
F1_STORAGE_RECONSTRUCTION        0 / 4
SHARED_OWNER_BINDING             0 / 25
```

UNKNOWN debt in the pilot is explicit:

```text
target_identity   16
owner_binding     25
```

All seven pilot gates pass, including exact F1 audit textual round trip and source-anchor `UNEXPLAINED=0`.

## Pilot artifacts

- schema: `docs/MACHINE_READABLE_ACCOUNTING_SCHEMA.md`
- claim rules: `docs/CLAIM_EXTRACTION_RULES.md`
- report: `docs/F1_MACHINE_ACCOUNTING_PILOT.md`
- validation ledger: `docs/VALIDATION_LEDGER_MACHINE_ACCOUNTING_PILOT.md`
- machine pilot data: `data/pilot/f1/`
- generated pilot summaries: `generated/pilot/f1/`
- isolated cardinality fixture: `tests/fixtures/machine_accounting_cardinality.json`
- validator: `tools/validate_machine_accounting_pilot.py`

Large JSONL tables are deterministically sharded and indexed. `FIXTURE-*` IDs are forbidden from project state and contribute zero project facts/progress.

## Authority boundary

The schema is **not frozen**. Existing canonical Markdown remains authoritative during the pilot. The machine layer is a validated candidate representation, not yet a replacement for V001–V095 Markdown ledgers.

No full V001–V095 migration, no full 27,430/27,419 source migration, no new 797 residual-family analysis, and no builder/IPS/runtime work was performed.

R0/R1/R1B/R1C, Stage 1, Stage 2, F1 audit, F1 authorization, V095 cleanup, and V096–V098 pilot facts remain canonical; do not revalidate them merely because a new chat/model is used.

## Mandatory boundaries

- PC patch is semantic authority.
- raw uniqueness is not a safety rule.
- target resolution is not write authorization.
- preserve internal Japanese yomi until its separate consumer/semantic gate is resolved.
- consumer tracing is an exception/family tool, not the default for structurally resolved rows.
- one diagnostic build = one root-cause family.
- no force-push and no silent source omission.
- no silent UNKNOWN authorization.
- no denominator exclusion without a verified exclusion claim.
- machine claim IDs are immutable after issuance.

## Next stage

Fresh execution signal required.

Recommended next step is **schema-freeze review only**: inspect V096–V098 pilot outputs, decide whether any schema amendment is required, then freeze v1 if accepted. Do not combine schema freeze with the full corpus migration, 797 analysis, builder implementation, mapping/runtime work, or game-file modifications.
