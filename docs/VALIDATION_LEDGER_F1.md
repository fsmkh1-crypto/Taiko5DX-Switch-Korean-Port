# VALIDATION LEDGER — F1 localization sequence audit

Date: 2026-09-12
Scope: F1 unique-anchor bounded localization sequence audit only. No builder/IPS/runtime/game-file modification.

Detailed report: `docs/F1_LOCALIZATION_SEQUENCE_AUDIT.md`

## V087 — HEAD drift from 317d3e30 to 3d3bad07 has no F1 data impact

**Status:** `VERIFIED`

The earlier residual analysis used `317d3e3040fa02babbb6c9c09e20a418e10ea7e7`; current canonical HEAD is `3d3bad07af347c2f6a22a0d77a90af67f1c21688`.

The intervening commit changes documentation/state accounting only. Canonical source inputs, Stage-1 source/exception ledgers, Stage-2 affine blocks/deltas, and game/code data used by F1 are unchanged.

Disposition: `NO_IMPACT`.

## V088 — canonical F1 promotion requires the final anchor-bounded interval itself to contain at least five rows

**Status:** `VERIFIED`

Under the stricter promotion gate:

- accepted final F1 segments: 112;
- mapped rows in those segments: 1,311;
- accepted F1 residual rows: 262;
- residual rows rejected by the F1 family gate: 16.

The rejected 16 occur in ten final anchor-bounded intervals of only 2-4 rows. Their candidate ID relations are not asserted false; they are simply not promoted under the canonical F1 family rule.

Reuse rule: do not infer F1 membership from a pre-trim search run of five or more rows unless the final unique-anchor-bounded interval also satisfies the minimum-length gate.

## V089 — 158 F1 residual rows satisfy the current static write-safety audit conditions

**Status:** `VERIFIED AS STATIC AUDIT`

Of the 197 F1 residual rows with exact full PC original-window matches:

```text
static safety conditions satisfied     158
terminator/capacity fail                 4
shared-owner obligation unresolved      25
short final segment / F1 gate rejected  10
TOTAL                                   197
```

The 158 rows satisfy the audited conditions for exact guard, object boundary, terminating NUL preservation, no unintended overlap with other audited F1 rows, no overlap with Stage-2 affine targets, JP ownership, and absence of the shared-owner blocker used by this audit.

Boundary: this is not release authorization, builder authorization, or a canonical source-ledger terminal disposition. `WRITE_SAFE_STATIC` remains an audit classification.

## V090 — exact original guard plus same-length replacement does not guarantee string capacity

**Status:** `VERIFIED`

Four full-window PASS rows consume the existing terminating NUL and require one additional byte beyond the Switch object boundary:

```text
R2674 / JP ID452
R2684 / JP ID462
R2712 / JP ID491
R3142 / JP ID938
```

In all four cases another JP object begins immediately after the current object. A static overwrite cannot safely append a new NUL.

Reuse rule: string write authorization must check payload plus terminating-NUL capacity against the actual Switch object boundary; same-length PC original/replacement comparison is insufficient.

## V091 — all 81 F1 padding mismatches are one storage-layout root-cause family

**Status:** `VERIFIED`

For all 81 rows:

- the PC original extends beyond the first logical NUL into zero padding;
- the Switch logical object ends at its NUL;
- the corresponding PC padding area is occupied by the next JP object on Switch;
- the PC replacement uses bytes in that padding area;
- replacement payload plus terminating NUL cannot fit inside the existing Switch object.

Six of the 81 fail V088's minimum-segment gate first. The remaining 75 are retained as `TARGET_RESOLVED_PADDING_RECONSTRUCTION_REQUIRED`.

Reuse rule: raw PC-length overwrite is prohibited for this family. A future storage/reconstruction design requires separate authorization.

## V092 — F1 audit corrects conservative target-unresolved residual from 781 to 797

**Status:** `VERIFIED ACCOUNTING`

The earlier provisional accounting treated all 278 F1 residual rows as target-resolved. V088 returns 16 to unresolved status.

Therefore:

```text
Stage-2 residual                         1,248
provisional later target-resolved          467
F1 returned to unresolved                  16
conservative target-resolved total         451
conservative target-unresolved residual    797
```

This correction does not alter Stage-2 V082-V086 facts. It supersedes only the later provisional `781` residual count.

## Shared-object boundary retained

Among the 197 full-window rows, 27 targets are shared physical objects. After excluding one capacity-fail row and one V088-rejected row, 25 remain target-resolved but blocked because the PC obligation of every relevant logical owner is not yet bound.

The audit proves no case in which different replacements are simultaneously required for the same physical Switch object. Do not promote those 25 to a global replacement conflict, and do not authorize a global physical overwrite until owner obligations are closed.

## Rejected shortcuts retained

- full guard + same replacement length implies safe string overwrite;
- PC padding can be reused unchanged on Switch;
- replacement length <= PC original length is a sufficient capacity rule;
- different PC replacement values for one raw original imply a global physical conflict;
- pre-trim run length alone is sufficient for F1 promotion;
- padding-window cross-object overlap may be assumed intentional.

F1 audit stops here. Fresh user execution signal is required for implementation, row-level authorization work, yomi analysis, another residual family, or any builder/IPS/runtime work.
