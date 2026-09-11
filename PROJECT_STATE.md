# PROJECT_STATE

Last updated: 2026-09-12 (KST)

## Current status

Repo: `fsmkh1-crypto/Taiko5DX-Switch-Korean-Port`
Branch: `main`

Stage 1 canonical inventory: COMPLETE.
Stage 2 affine structural targeting: COMPLETE.
F1 unique-anchor bounded localization sequence audit: COMPLETE.
F1 158-row static write authorization/provenance closure: COMPLETE.

The exact 158 F1 actions are now row-level `DIRECT_PORT` authorized for future static builder consumption, subject to their manifest guards. No builder, IPS, ZIP, runtime artifact, or game-file modification was performed in this authorization stage.

Canonical target:
- Title ID `0100346017304000`
- Switch v1.1.3
- Build ID `D9120950C258610A746F4A31CE3A3B376DE393D9`
- `main` SHA-256 `b366e692208f3c0cc18bc1884ef95689b6b11d722fa2d749b8500abccbc3109b`

## Accounting snapshot

```text
source-ledger rows                         27,430
inline rows                                17,103
Stage-1 raw exceptions                     11,050
Stage-2 affine target-resolved             13,771
Stage-1 exceptions target-resolved          9,802
Stage-2 residual                            1,248
post-Stage2 provisional target-resolved       467
F1 rows returned by stricter gate              16
conservative later target-resolved             451
conservative target-unresolved residual        797
```

The `797` target-unresolved working count is unchanged by static authorization of already target-resolved rows.

## F1 authorization snapshot

Historical F1 residual population: 278.

```text
F1_STATIC_WRITE_AUTHORIZED                    158
TARGET_RESOLVED_CAPACITY_FAIL                   4
TARGET_RESOLVED_PADDING_RECONSTRUCTION_REQUIRED 75
TARGET_RESOLVED_OTHER_BLOCKER                  25
F1_RULE_REJECTED                               16
TOTAL                                          278
```

Deterministic selector replay reproduced exactly:

```text
search segments            142
anchor-bounded mapped    1,402
residual in bounds          278
accepted segments           112
accepted mapped           1,311
accepted residual           262
rejected residual            16
```

Row-level artifacts:

- `tools/f1_static_authorization.py`
- `docs/F1_STATIC_WRITE_AUTHORIZATION.md`
- `docs/manifests/F1_STATIC_WRITE_AUTHORIZATION_MANIFEST.jsonl.gz`
- `docs/manifests/F1_STATIC_WRITE_AUTHORIZATION_SUMMARY.json`

Manifest content SHA-256: `c612bcf55d0c139d55dee42a6a6397f702ead0f1628b47b45c46512fd1b52bff`; canonical compressed file SHA-256: `8bbbeb03695b4bd06f028b9c9cfe0d367af170a012af56803f3a8553356a0b68`.

Important boundaries:

- the 158 authorized rows are 158 unique PC source rows -> 158 unique localization IDs -> 158 unique physical JP-only objects;
- every authorized action has an exact original-byte guard, 1:1 object cardinality, terminating-NUL proof, single logical owner, and zero overlap with the F1 full-window set and Stage-2 targets;
- 4 capacity failures, 75 padding-reconstruction rows, 25 shared-owner rows, and 16 F1-rule rejects remain excluded;
- no builder/IPS/runtime work is implied by authorization alone.

## Canonical safety rules added by F1

- full original-byte guard plus same replacement length is not sufficient for a string write;
- capacity includes the terminating NUL and is bounded by actual Switch storage;
- PC NUL padding must not be assumed available on Switch;
- raw PC-length writes are forbidden for the F1 padding-mismatch family;
- shared physical object overwrite requires source obligation closure for all relevant logical owners;
- an F1 final anchor-bounded segment itself must satisfy the minimum five-row promotion gate;
- the canonical F1 selector is now reproducible and must not be replaced by raw uniqueness or aggregate-count fitting.

## Canonical documents

- rules: `docs/PC_TO_SWITCH_PORTING_RULE_FRAMEWORK.md`
- invariants: `docs/PC_TO_SWITCH_ACCOUNTING_INVARIANTS.md`
- Stage 1: `docs/FULL_PORT_INVENTORY_STAGE1.md`
- Stage 2: `docs/STAGE2_AFFINE_STRUCTURAL_TARGETING.md`
- F1 audit: `docs/F1_LOCALIZATION_SEQUENCE_AUDIT.md`
- F1 static authorization: `docs/F1_STATIC_WRITE_AUTHORIZATION.md`
- validation index: `docs/VALIDATION_LEDGER.md`

R0/R1/R1B/R1C, Stage 1, Stage 2, F1 audit, and F1 authorization ledger facts remain canonical; do not revalidate them merely because a new chat/model is used.

## Mandatory boundaries

- PC patch is semantic authority.
- raw uniqueness is not a safety rule.
- target resolution is not write authorization.
- preserve internal Japanese yomi until its separate consumer/semantic gate is resolved.
- consumer tracing is an exception/family tool, not the default for structurally resolved rows.
- one diagnostic build = one root-cause family.
- no force-push and no silent source omission.

## Next stage

Fresh execution signal required.

If the next scope is implementation, consume exactly the 158 manifest actions as one F1 static-direct family with fail-closed canonical-input and per-row original-byte guards. Do not mix the 25 shared-owner rows, 4 capacity failures, 75 padding-reconstruction rows, yomi, F2-F5, bounded-gap candidates, CN sequence, UTF-16, or unrelated runtime work into that implementation step.
