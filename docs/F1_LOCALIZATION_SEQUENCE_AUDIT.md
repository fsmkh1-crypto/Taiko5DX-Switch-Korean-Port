# F1 LOCALIZATION SEQUENCE AUDIT

Date: 2026-09-12
Canonical base: `3d3bad07af347c2f6a22a0d77a90af67f1c21688`
Scope: independent audit of the F1 unique-anchor bounded localization sequence family only. No builder, IPS, runtime artifact, game-file modification, yomi implementation, or other residual-family analysis is included.

## 1. Summary

The earlier F1 residual set contained 278 rows. Under the stricter rule that the final anchor-bounded segment itself must contain at least five rows, 262 remain structurally target-resolved and 16 are returned to unresolved status.

Audit disposition:

| audit disposition | rows |
|---|---:|
| TARGET_RESOLVED_WRITE_SAFE_STATIC | 158 |
| TARGET_RESOLVED_CAPACITY_FAIL | 4 |
| TARGET_RESOLVED_PADDING_RECONSTRUCTION_REQUIRED | 75 |
| TARGET_RESOLVED_OTHER_BLOCKER | 25 |
| F1_RULE_REJECTED | 16 |
| total | 278 |

`WRITE_SAFE_STATIC` is an audit classification, not a release or builder authorization. No canonical source-ledger terminal disposition is changed by this report.

Because 16 earlier F1 mappings are no longer promoted, the conservative overall target-unresolved residual becomes `797`, not `781`.

## 2. HEAD impact audit

The earlier residual analysis used `317d3e3040fa02babbb6c9c09e20a418e10ea7e7`. Current canonical HEAD is `3d3bad07af347c2f6a22a0d77a90af67f1c21688`.

Result: `NO_IMPACT`.

The intervening commit changes only documentation/state accounting. Canonical source inputs, Stage-1 ledgers, Stage-2 structural blocks/deltas, and game/code data used by F1 are unchanged.

## 3. F1 rule correction

Earlier search procedure found 142 search segments / 1,402 mapped rows / 278 residual rows. The search segments were at least five rows before unique-anchor trimming.

For canonical promotion, the stricter boundary is adopted:

- the final interval between the first and last accepted unique anchors must itself contain at least five rows;
- the ID relation remains `Switch localization ID = PC record number + segment-specific constant` only inside that final bounded interval;
- constants never extend across a gap/reset or outside the anchor interval.

Under this rule:

- accepted final segments: 112;
- mapped rows: 1,311;
- accepted F1 residual rows: 262;
- rejected residual rows: 16.

The 16 rejected rows come from ten short post-trim intervals:

```text
R283-R286   -> ID1389-1392
R820-R822   -> ID2007-2009
R1274-R1275 -> ID2785-2786
R1984-R1987 -> ID3531-3534
R2014-R2015 -> ID3553-3554
R2160-R2163 -> ID3678-3681
R2252-R2254 -> ID3777-3779
R2424-R2427 -> ID178-181
R2479-R2480 -> ID240-241
R3181-R3182 -> ID993-994
```

This does not prove the ID calculations are wrong. It means those intervals do not satisfy the conservative family-promotion gate.

All accepted F1 targets remain `JP_ONLY`. No PC record receives conflicting ID formulas inside the accepted segments.

R549 remains bound by F1 context to localization ID1706; pooled `年` physical identity does not rebind it to ID2630.

## 4. Full-window PASS audit

The earlier F1 residual split was:

- 197 full PC original-window matches;
- 81 logical-object matches with full-window mismatch caused by PC padding.

For the 197 full-window rows, the mutually exclusive audit result is:

| result | rows |
|---|---:|
| static safety conditions satisfied | 158 |
| terminator/capacity fail | 4 |
| shared-object owner obligation unresolved | 25 |
| rejected by final-segment minimum-length rule | 10 |
| total | 197 |

All 197 have exact full original-window byte guards. None has a replacement longer than the PC original window. However, exact guard plus same-length replacement is not sufficient by itself: four replacements consume the existing terminating NUL.

### 4.1 Terminator/capacity failures

```text
R2674  PC 0xB29D14  JP ID452  Switch [0x6868D4,0x6868DB)  object bytes 7  required incl NUL 8
R2684  PC 0xB29DA8  JP ID462  Switch [0x6A8BD4,0x6A8BDD)  object bytes 9  required incl NUL 10
R2712  PC 0xB29ED4  JP ID491  Switch [0x693F83,0x693F86)  object bytes 3  required incl NUL 4
R3142  PC 0xB2BD90  JP ID938  Switch [0x6A5364,0x6A5371)  object bytes 13 required incl NUL 14
```

In all four cases another JP object begins immediately after the existing object boundary. Appending a NUL byte is therefore not a safe static write.

### 4.2 Overlap

- full-window 197 rows against each other: 0 unintended overlaps;
- full-window 197 against Stage-2 affine targets: 0;
- all residual F1 hypothetical PC-length windows against Stage-2 affine targets: 0.

Padding-mismatch rows must not be written as PC-length windows. Doing so creates nine cross-object overlap pairs:

`R555/R567`, `R884/R908`, `R885/R891`, `R893/R902`, `R913/R946`, `R1986/R1987`, `R2722/R2725`, `R2933/R2941`, `R3072/R3078`.

## 5. Padding mismatch root cause

All 81 logical-object/full-window mismatches belong to one storage-layout root-cause family:

- PC original extends past the first logical NUL into zero padding;
- Switch object ends at its logical NUL;
- the corresponding PC padding position is occupied by the next JP object on Switch;
- PC replacement uses bytes that occupy the PC padding area;
- replacement payload plus a terminating NUL cannot fit in the existing Switch object capacity.

No alternative cause is required for these 81 rows.

Additional space required for replacement payload plus terminating NUL:

```text
+2 bytes: 23
+3 bytes: 33
+4 bytes:  8
+5 bytes: 11
+6 bytes:  3
+7 bytes:  2
+9 bytes:  1
TOTAL:    81
```

Six of these 81 are removed first by the stricter F1 segment-length gate, leaving 75 canonical F1 target-resolved rows requiring storage reconstruction.

Raw PC-length overwrite is forbidden for this family.

## 6. Shared physical objects

Among the 197 full-window rows, 27 targets are physical objects referenced by multiple localization IDs. After removing one capacity-fail row and one short-segment rejected row, 25 remain blocked on owner/source obligation binding.

Known PC replacements agree for many shared-value contexts, and differing replacement values often belong to separately mapped PC contexts. The audit found zero cases where different replacements are proven to be simultaneously required for the same physical Switch object.

Therefore these 25 rows are not classified as proven replacement conflicts. They remain `TARGET_RESOLVED_OTHER_BLOCKER` until the PC obligation for every relevant logical owner is bound.

Static overwrite of a shared physical object must not be authorized merely because the F1-selected logical ID has a known replacement.

## 7. Canonical safety consequences

The following shortcuts are rejected for future work:

1. `full original guard PASS + same replacement length => safe static write` — rejected by four terminator failures.
2. PC padding can be reused on Switch — rejected for all 81 padding mismatches because the space is occupied by following JP objects.
3. replacement length not exceeding PC original length is a complete capacity check — rejected; terminating NUL capacity is mandatory.
4. differing PC replacements for the same raw original imply a global physical conflict — rejected without source-context-to-owner binding.
5. a pre-trim search segment of five or more rows automatically makes every final anchor-bounded interval promotable — rejected; ten final intervals are only 2-4 rows.
6. padding-window overlap can be treated as intended reconstruction — rejected for the nine identified cross-object pairs.

## 8. Accounting correction

Before this audit, residual accounting treated all 278 F1 rows as target-resolved and produced a provisional overall residual of 781.

The stricter F1 rule rejects 16 rows. Therefore:

```text
Stage-2 residual                         1,248
later structural target-resolved          467   (provisional)
F1 rows returned to unresolved              16
conservative target-resolved total         451
conservative target-unresolved residual    797
```

This is a safety correction, not a regression in evidence. The 16 rows retain useful candidate mappings but are not promoted under the canonical F1 family rule.

## 9. Next scope

Recommended next work, only after a fresh user execution signal:

- formalize row-level evidence for the 158 `WRITE_SAFE_STATIC` audit candidates;
- keep the 25 shared-owner rows separate;
- keep the 4 terminator failures and 75 padding-reconstruction rows out of static overwrite implementation;
- do not mix yomi, F2-F5, bounded-gap candidates, CN sequence, UTF-16, builder/IPS, or runtime diagnostic work into that stage.

No repository/game-file/builder/IPS/runtime modification was performed by the audit itself. This document records and freezes the audit result only.
