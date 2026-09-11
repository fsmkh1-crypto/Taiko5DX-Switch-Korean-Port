# R1B localization secondary indirection trace

Date: 2026-09-11  
Scope: analysis-only continuation of R1. No builder, patch, IPS, ZIP, runtime artifact, game file, or aggregate project document was modified.

## 1. Goal and stopping rule

R1B was intentionally limited to one question:

> after localization materialization, is there an additional indirection / registry / accessor layer before a UI-side consumer receives the runtime string?

The DCTRL7 basic-information screenshot visibly contains the label `拠点` in `拠点 岡崎城`. R1B therefore used pooled rodata object `拠点 @ 0x6A3D6B` as the visible anchor instead of widening into DATE-COMPOSITE or PLACE-FORMATTER families.

The stopping rule was to stop immediately once one post-materialization indirection structure was directly established.

## 2. Fixed input

- Switch v1.1.3 Build ID `D9120950C258610A746F4A31CE3A3B376DE393D9`
- compressed `main` SHA-256 `b366e692208f3c0cc18bc1884ef95689b6b11d722fa2d749b8500abccbc3109b`
- mapped flat image size `0xA20430`
- canonical R1 localization table base `0x9C0008`
- canonical runtime destination-cell base `0xA210E0`

R1 facts V070-V073 were reused and not revalidated.

## 3. `拠点` is pooled across four localization IDs

The first localization source table has four entries whose RELA addend is the same rodata object `拠点 @ 0x6A3D6B`:

| localization ID | source slot | destination cell | semantic neighborhood |
|---:|---:|---:|---|
| 402 | `0x9C0C98` | `0xA21D70` | `人物一覧・配下武将 / 主人公 / 人物 / 勢力 / 勢力図 / 拠点 / 所持品 / 相場 / 札 / 販路 / その他` |
| 1297 | `0x9C2890` | `0xA23968` | `能力 / 面会 / 出陣 / 官位 / 自勢 / 拠点 / 収入 / 紹介状 / 親密 / 面識 / 茶会` |
| 1620 | `0x9C32A8` | `0xA24380` | `主人公を選んでください / シナリオを選んでください / 顔 / 名前 / 性別 / 拠点 / 生年 / 寿命 / 死因 / 出自 / 父親` |
| 2633 | `0x9C5250` | `0xA26328` | `状況:: / シナリオ / 年 / 月 / 日 / 拠点 / 場面 / 空き大名家数 / 天気 / イベント主命 / 評定期限` |

Therefore the visible word `拠点` cannot be assigned to localization ID 2633 merely because that ID is adjacent to the R1 `年/月/日` cluster.

For the tested protagonist basic-information screen, ID 1297 is the strongest semantic candidate because its neighborhood is character-status/action data. This screen binding remains a hypothesis, not a VERIFIED edge.

## 4. Entry 1297 has an additional pointer-to-cell indirection

Entry 1297 differs from the R1 entry-2630 pattern in a critical way.

Its destination cell is:

`0xA23968`

There are two `R_AARCH64_RELATIVE` relocations whose addend is that destination cell:

- ordinary GOT-style slot `0xA00C28 -> 0xA23968`
- additional static slot `0x9E9690 -> 0xA23968`

The second slot is not isolated. It begins a four-entry table:

```text
0x9E9690 -> 0xA23968  localization 1297  拠点
0x9E9698 -> 0xA23AF8  localization 1347  国
0x9E96A0 -> 0xA21D60  localization 400   勢力
0x9E96A8 -> 0xA23B00  localization 1348  地方
```

The next slot is not a fifth member of this destination-cell table, and the code reader independently bounds the selector to four elements.

## 5. Exact secondary-table reader

Mapped code at `0x3DFA60..0x3DFA84` directly reads the four-entry table:

```text
0x3DFA60  cmp  w24,#3
0x3DFA64  b.hi ...
0x3DFA68  adrp x8,0x9E9000
0x3DFA6C  add  x8,x8,#0x690        ; table base 0x9E9690
0x3DFA74  ldr  x8,[x8,w24,sxtw #3] ; selected pointer-to-destination-cell
0x3DFA78  ldr  x1,[x8]              ; runtime string-buffer pointer
0x3DFA7C  ldr  x0,[...]
0x3DFA80  mov  w2,wzr
0x3DFA84  bl   0x25F754
```

This directly establishes the missing post-materialization layer:

```text
localization destination cell
-> secondary pointer-to-cell table
-> selected destination cell
-> runtime string buffer
-> consumer handoff
```

For selector `w24 = 0`, the chain is specifically:

```text
entry 1297 source slot 0x9C2890
-> destination cell 0xA23968
-> secondary table slot 0x9E9690
-> reader 0x3DFA68..0x3DFA78
-> runtime buffer in x1
-> call 0x25F754
```

R1B does not assign a final UI-widget name to `0x25F754`. Static inspection shows that it accepts the string pointer path and tail-calls an imported helper after preparing an internal subobject; exact widget/render semantics are left for a later stage.

## 6. Direct UI-side string handoff also exists for entry 1297

The ordinary destination GOT slot `0xA00C28 -> 0xA23968` has post-copy readers in addition to allocation/clear/language-copy lifecycle uses.

Two notable call sites are:

```text
0x4B48CC  adrp/ldr -> 0xA00C28
0x4B48D4  ldr x2,[x8]       ; runtime string pointer
0x4B48E0  bl  0x44758C

0x4B4D98  adrp/ldr -> 0xA00C28
0x4B4DA0  ldr x2,[x8]       ; runtime string pointer
0x4B4DAC  bl  0x44758C
```

At `0x44758C`, a non-null `x2` string argument is forwarded as `x1` into `0x432760` after object-state setup. R1B records this only as corroborating string-consumer behavior; it does not attempt to finish the screen/widget identification because the secondary-indirection stopping rule has already been satisfied.

## 7. What this changes from R1

R1 V073 remains correct for entry 2630: direct following of its exact destination GOT slot exposes only allocation/clear/copy lifecycle.

R1B adds a narrower fact:

> other localization IDs can have additional static pointer-to-destination-cell tables and UI-side consumers beyond the lifecycle-only pattern seen for entry 2630.

Therefore absence of a direct post-copy reader for one destination GOT slot does not imply that the localization system has no higher-level registry/selector layer.

It also reinforces the R1 rule that pooled rodata identity is not localization-ID identity. `拠点` has four logical IDs, not one.

## 8. Unresolved edge

R1B does **not** prove either of the following:

- entry 1297 is definitively the exact source of the tested `拠点 岡崎城` basic-information label;
- entry 2630 `年` is reachable through the same four-entry table mechanism.

Those edges require separate work and were intentionally not pursued in this stage.

## 9. Stopping point

The R1B stopping condition is met because one concrete post-materialization indirection structure is directly established.

No DATE-COMPOSITE survey, PLACE-FORMATTER survey, builder work, patch generation, or runtime build was started.

Next work requires a fresh user execution signal.
