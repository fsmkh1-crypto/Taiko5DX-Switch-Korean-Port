# ECF00000 PC EDITOR V0.30 PARSER PROVENANCE AND V324 4,444 CONFLICT — V331

Date: 2026-09-19 (KST)

```text
validation_id   V331
track           SWITCH_SELECTIVE_KOREANIZATION
scope_kind      READ_ONLY_PROVENANCE_CHECKPOINT
parent          d9e6605022d9febdeffdd7e9384b0060327eb32e / V330
product_bytes   UNCHANGED
code            UNCHANGED
build/package   NONE
repository      DOCUMENTATION_ONLY
```

This checkpoint records the exact PC editor v0.30 source behavior, the failed V330 two-context full replay, and the resulting provenance conflict around the historical V324 4,444-target aggregate.

## 1. Source identity

User-supplied original archive:

```text
file      taikou5_dx_msg v0.30.7z
size      3,379,608 bytes
SHA-256   0f0df73e9d79355687e7a95c35b8bacb1fcdf1f83d0a80d5abeb105514bde903
Drive id  1OkLoJPQRYKYC-isox4P4WzXqYhpYFehh
```

The archive contains the full Visual Basic project, not only an executable.

```text
UI version       v0.30
target framework .NET Framework 4.5.1
core source      Form1.vb
Form1.vb size    296,505 bytes
Form1.vb SHA-256 dc41d778ab11268fc137d0b995bc5cff14d0fcec127e020803c6dc838523e14d
```

This source is the PC editor authority for edit-time EVENT grouping, branch arithmetic, false-positive guards, and TS5 rebuilding behavior.

## 2. PC editor load model

The v0.30 editor does not emulate the Switch runtime entrypoint interpreter.

For editing, it treats the TS5 offset table as non-overlapping edit partitions:

```text
partition i = offset[i] .. offset[i+1]
last partition = offset[last] .. EOF
```

Within each partition it:

```text
forces all bytes to control-code form
-> splits into 4-byte chunks
-> CombineDialogueBytes()
-> analyzes branch families in order:
   02 -> 04 -> 06 -> 07 -> 08 -> 09
```

This is an editor-preservation model. It does not supersede the Switch runtime fact that offset[i+1] is not the runtime interpreter end of entrypoint i.

## 3. Exact edit-time branch arithmetic

The source establishes these branch-length formulas:

```text
02   LE16(bytes1..2) * 4
04   LE16(bytes2..3) / 2
     odd values are rejected as branch recognition candidates
06   LE24(bytes1..3) * 2
     modulo-4 intrusion bytes preserved separately
07   LE24(bytes1..3) * 2
     modulo-4 intrusion bytes preserved separately
08   LE16(bytes2..3) * 4
09   (LE16(bytes2..3) - modulo4 intrusion) / 2
     intrusion preserved separately
```

When edited text changes byte lengths, the editor recalculates these branch families in the same order and then rebuilds TS5 partition lengths and the global offset table.

Therefore the actual PC-patch preservation behavior is:

```text
text length change
-> branch-distance recalculation inside affected partition
-> partition-length recalculation
-> global TS5 offset-table rebuild
```

This must be consulted before designing a Switch EVENT serializer.

## 4. CombineDialogueBytes trap / false-positive guards

The PC source explicitly contains guards against command-looking bytes inside text or structural payloads.

For text-like `11/12/13/1E`, merging stops before a following chunk that begins with:

```text
11 / 12 / 13 / 1E / 15
04 / 06 / 07 / 08 / 09
3C
```

Choice `15` has a disguised-`15` guard:

```text
current 15 header fourth byte == 0x03
-> do not merge as ordinary choice payload
```

The source includes the ECF00000 example:

```text
15 09 F8 03 0A 80 1C 00
```

Additional false-`04` guards:

```text
16/17/18 + following 04
-> merge to prevent false 04 recognition

0B xx 17 00 + following 04 00
-> merge

04 00 xx 0E + following 04 00 yy 0E
-> merge
```

These are source-proven PC editor rules and must not be replaced by raw opcode scanning.

## 5. Developer experiment note

The archive includes an ECF00000 development/test note documenting empirical work on conditional `04` branches.

The developer identifies `04 xx yy zz` as a conditional branch whose false path advances by the byte-flipped `yy zz / 2` distance. Correcting the relevant TS5 `04` fields restored the female custom-character dialogue in the recorded test.

The same note considers TE5 involvement, but the successful correction is the TS5 `04` jump-field change. This does not support treating TE5 as the hidden target-row index.

## 6. Exact editor-grouping replay on PC-KO ECF00000

The source-level `CombineDialogueBytes()` behavior was reproduced byte-for-byte at the grouping-rule level over all 782 PC-Korean edit partitions.

```text
partition errors               0
grouped items             70,819
target-looking items      15,945

0x11                      12,088
0x12                       1,425
0x13                       1,981
0x15                         451

messages                  15,494
choices                      451
```

Observed trap diagnostics:

```text
dialogue trap before branch      236
16/17/18 + 04 trap               837
dialogue trap before target      356
04 00 xx 0E pair trap             38
0B xx 17 00 + 04 00 trap          32
disguised 15                      65
dialogue trap before 3C            1
```

Therefore the PC editor's editable/grouped surface is not the V324 4,444 target population.

## 7. V330 two-context full replay result

After V330, the full 782-entrypoint reconstruction was rerun with traversal state `(context, physical address)` and the EVENT/BRANCH transition rules.

Result:

```text
                         historical gate   two-context replay
physical targets               4,444             2,863
messages                       4,193             2,614
choices                          251               249
choice strings                   504               500
Korean targets                 4,238             2,656
INCLUDE_KO                     4,123             2,542
UNRESOLVED                       115               114

entrypoint errors                                  0
recursive edges                                  340
max recursion depth                                4
```

The V330 context fix is valid because it removes the prior wrong-context overrun, but the two-context model still does not reconstruct the historical 4,444 population.

The two-context full replay is diagnostic only and is forbidden as serializer row membership.

## 8. V324 provenance conflict

The same PC-Korean ECF00000 identity remains:

```text
size      1,156,480 bytes
SHA-256   0899bf81789acfbd243d43be209a8a3960933fa090960ac8c753c63f95f07bbe
count     782
offsets   783
```

A finite outer walker using the currently preserved V324 structural length rules reproduces the V327 subset:

```text
target path occurrences   2,825
physical targets          2,817
0x11                      2,050
0x12                         94
0x13                        425
0x15                        248
```

It also closely reproduces the historical V324 structural-containment fingerprint while not reproducing the 4,444 target population.

Therefore the V324 statement that a simple finite Switch-interpreter walker alone produced exactly 4,444 targets is now provenance-conflicted.

This does **not** by itself prove that the historical aggregate 4,444 is false. It proves that the exact rowset and the original code/artifact that produced it are not currently materialized or reproducible from the documented simple-walker method.

Canonical status:

```text
V324 aggregate 4,444             HISTORICAL CLAIM PRESERVED
exact 4,444 physical rowset      UNRESOLVED / NOT MATERIALIZED
simple finite-walker explanation PROVENANCE CONFLICT
serializer use of 4,444 rowset   BLOCKED
```

The same provenance limitation propagates to historical aggregate derivatives:

```text
4,238 Korean
4,123 INCLUDE_KO
115 UNRESOLVED
```

These are preserved as historical aggregate claims, not as an exact currently reconstructed serializer rowset.

## 9. Authority split after V331

### PC editor v0.30 authority

Use as authority for:

- edit-partition handling;
- 4-byte grouping;
- `02/04/06/07/08/09` branch arithmetic;
- false-`04` and disguised-`15` guards;
- edit-time branch-distance repair;
- partition-size and TS5 offset-table rebuilding.

### Switch runtime authority

Use as authority for:

- runtime descriptor/context behavior;
- actual command execution semantics;
- EVENT vs BRANCH context transitions;
- runtime rendering/caller behavior.

### Not established by either source

Neither currently materializes the historical V324 exact 4,444-row target set.

## 10. Rejected / do-not-repeat

Rejected:

- PC editor v0.30 directly generates the V324 4,444 target census;
- editor offset partitions are runtime interpreter boundaries;
- the 15,945 editor target-looking grouped items are the 4,444 runtime target corpus;
- raw `11/12/13/15` scanning can substitute for structural parsing;
- all apparent `04` or `15` chunks are genuine commands;
- EVENT+BRANCH two-context recursion is sufficient to reconstruct 4,444;
- TE5 is established as the hidden ECF00000 TS5 target index;
- forcing filters until the editor's 15,945 rows numerically equal 4,444 is acceptable;
- using historical 4,444 aggregate counts as serializer exact row membership without provenance materialization.

Do not rerun another full 782-entrypoint walker merely with another guessed recursive rule before provenance recovery.

## 11. Artifact preservation

Original source archive remains in the project Drive root:

```text
taikou5_dx_msg v0.30.7z
Drive file id 1OkLoJPQRYKYC-isox4P4WzXqYhpYFehh
SHA-256      0f0df73e9d79355687e7a95c35b8bacb1fcdf1f83d0a80d5abeb105514bde903
```

V331 diagnostic folder:

```text
Google Drive/GPT/태합입지전/ECF00000_V331_PC_EDITOR_PROVENANCE/
folder id 1bF5qbJhSq-4sy5mnrlZb8zxuujSHPUHw
```

PC editor provenance artifact:

```text
ecf_pc_editor_v030_parser_provenance.json
Drive file id 1g6Zp4GrHu2FyZHoSbSPAQp5qhtgSDZ1i
SHA-256 37f8ee6a4f011fde9154f4f462d0a860d2f71c0cefd33c238644a2e072459b52
```

Two-context failed full replay:

```text
ecf_v330_two_context_full_ledger.json
Drive file id 14YJR7FjLAleqN0ECYNiPbyJUNoYAbyel
SHA-256 de6ccff2139c9f36cdadd650d7cfcaa368e7e8ca0b013528cc09809b9795e36a
```

## 12. Impact boundary

Unchanged:

- Mapping 10,036;
- Korean font and page mapper;
- TAI5MSG/B24;
- identity presentation policy;
- FIXED_SURFACE_PARTICLE_V1;
- Switch/PC-original carrier parity;
- product bytes.

Blocked:

- exact EVENT selective serializer rowset;
- exact 115-row semantic-adjacency closure based on V326 membership;
- EVENT payload implementation/build/package.

## 13. Exact next scope

After a fresh explicit execution signal:

`ECF00000_V324_4444_ORIGINAL_PROVENANCE_ARTIFACT_RECOVERY_READ_ONLY`

Search order:

1. repository history/current tree for the original V324 census code or materialized row artifact;
2. project Drive for V324-era diagnostics, scripts, notebooks, JSON/CSV/index artifacts;
3. surviving current-session analysis artifacts/code only where provenance can be established;
4. recover exact physical offsets and the code path that generated them before any new census design.

Do not:

- create another guessed walker;
- tune filters to hit 4,444;
- implement serializer/payload changes;
- build/package/IPS;
- broaden to other EVENT files or SNR.

No product bytes, builder code, package, build or IPS are changed by V331.
