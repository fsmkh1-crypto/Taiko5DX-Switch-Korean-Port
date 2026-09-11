# PROJECT_STATE

Last updated: 2026-09-12 (KST)

## Current status

Repo: `fsmkh1-crypto/Taiko5DX-Switch-Korean-Port`
Branch: `main`

Stage 1 canonical inventory: COMPLETE.
Stage 2 affine structural targeting: COMPLETE.
F1 unique-anchor bounded localization sequence audit: COMPLETE.
No builder/IPS/runtime implementation is authorized by the F1 audit.

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

The `797` figure is the current conservative target-resolution working count after the F1 audit correction. It does not mean the remaining 451 resolved rows are all write-authorized.

## F1 audit snapshot

F1 residual population: 278.

```text
TARGET_RESOLVED_WRITE_SAFE_STATIC              158
TARGET_RESOLVED_CAPACITY_FAIL                    4
TARGET_RESOLVED_PADDING_RECONSTRUCTION_REQUIRED 75
TARGET_RESOLVED_OTHER_BLOCKER                   25
F1_RULE_REJECTED                                16
TOTAL                                           278
```

Important boundaries:

- accepted F1 residual targets: 262;
- 16 rows are returned to unresolved because the final unique-anchor-bounded interval is shorter than five rows;
- 158 rows satisfy the current static write-safety audit conditions but are not release/builder authorization;
- 4 full-window PASS rows consume the terminating NUL and fail actual object capacity;
- 75 accepted rows require storage reconstruction because PC padding is occupied by following JP objects on Switch;
- 25 accepted rows remain blocked on shared-physical-object owner obligation binding;
- no proven case currently requires conflicting replacement values simultaneously on one shared physical Switch object.

## Canonical safety rules added by F1

- full original-byte guard plus same replacement length is not sufficient for a string write;
- capacity includes the terminating NUL and is bounded by the actual Switch object boundary;
- PC NUL padding must not be assumed available on Switch;
- raw PC-length writes are forbidden for the F1 padding-mismatch family;
- shared physical object overwrite requires source obligation closure for all relevant logical owners;
- an F1 final anchor-bounded segment itself must satisfy the minimum five-row promotion gate.

## Canonical documents

- rules: `docs/PC_TO_SWITCH_PORTING_RULE_FRAMEWORK.md`
- invariants: `docs/PC_TO_SWITCH_ACCOUNTING_INVARIANTS.md`
- Stage 1: `docs/FULL_PORT_INVENTORY_STAGE1.md`
- Stage 2: `docs/STAGE2_AFFINE_STRUCTURAL_TARGETING.md`
- F1 audit: `docs/F1_LOCALIZATION_SEQUENCE_AUDIT.md`
- validation index: `docs/VALIDATION_LEDGER.md`

R0/R1/R1B/R1C, Stage 1, Stage 2, and F1 ledger facts remain canonical; do not revalidate them merely because a new chat/model is used.

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

Recommended next scope: F1 static-safe 158 rows only. Formalize row-level evidence and final write-authorization invariants without mixing in the 25 shared-owner rows, 4 terminator failures, 75 padding-reconstruction rows, yomi, F2-F5, bounded-gap candidates, CN sequence, UTF-16, builder/IPS, or runtime diagnostic work.
