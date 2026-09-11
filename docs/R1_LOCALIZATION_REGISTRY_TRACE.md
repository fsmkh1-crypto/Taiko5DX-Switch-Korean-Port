# R1 localization registry / consumer trace

Date: 2026-09-11  
Scope: analysis-only trace of the DCTRL7-verified standalone `年 @ 0x69785A`. No builder, patch, IPS, ZIP, runtime artifact, or aggregate project document was modified in R1.

## 1. Goal and stopping rule

R1 started from the verified DCTRL7 observation that standalone `年 @ 0x69785A` renders as Korean `년` on the scenario route. The intended trace was:

`rodata object -> RELA-backed source slot -> runtime materialization -> downstream reader/consumer -> scenario screen`

R1 establishes the chain through the runtime materialization layer and separates two independent localization IDs that share the same rodata object. A direct post-materialization UI reader for the tested scenario screen was not statically bound. That gap is preserved rather than inferred away.

Canonical R0 facts V063-V069 were reused, not revalidated from scratch.

## 2. Fixed input

- Switch v1.1.3 Build ID `D9120950C258610A746F4A31CE3A3B376DE393D9`
- compressed `main` SHA-256 `b366e692208f3c0cc18bc1884ef95689b6b11d722fa2d749b8500abccbc3109b`
- mapped flat image size `0xA20430`
- DCTRL7 standalone `年` target `0x69785A`, replacement `94 4E -> EC E0`
- DCTRL7 runtime provenance/result: V063-V065

Static inspection used the exact decompressed `main` plus AArch64 disassembly. No source bytes were changed.

## 3. Localization source-table architecture

R0 already established that `年 @ 0x69785A` is the addend of two `R_AARCH64_RELATIVE` entries:

- `.data 0x9C3558 -> rodata 0x69785A`
- `.data 0x9C5238 -> rodata 0x69785A`

R1 found that these belong to a much larger fixed-index localization source layout.

### 3.1 Three contiguous 3,803-entry source pointer tables

The first source pointer table begins at `0x9C0008`. Two same-size parallel source tables begin at:

- `0x9C0008`
- `0x9C76E0`
- `0x9CEDB8`

The spacing is exactly:

`0x76D8 = 30,424 = 3,803 * 8`

`0x9C0000` itself is not entry zero. It is used separately as a module/DSO-style handle in destructor-registration paths. Therefore localization index zero begins at `0x9C0008`.

For the first source table:

`index = (source_slot - 0x9C0008) / 8`

The exact semantic language labels of the second and third source tables are intentionally not assigned in R1; only their parallel structural role is established.

### 3.2 Parallel runtime destination cells

A contiguous run of 3,803 eight-byte destination pointer cells exists at:

`0xA210E0 .. 0xA287B0`

with the same index relation:

`destination_cell(index) = 0xA210E0 + index * 8`

Each destination cell receives an allocated byte buffer, is cleared, and is populated from one of the parallel source tables by large generated copy routines.

## 4. `年` is one rodata object but two localization IDs

Because the same pooled rodata object `0x69785A` is referenced by two distinct first-table source slots, it represents at least two independent localization entries.

### 4.1 Entry 1706 — character-creation / birth-year cluster

Source slot:

`0x9C3558`

Index:

`(0x9C3558 - 0x9C0008) / 8 = 1706 = 0x6AA`

Destination cell:

`0xA210E0 + 1706*8 = 0xA24630`

The source-slot neighborhood is:

```text
0x9C3520  新規作成
0x9C3528  内容変更
0x9C3530  武将削除
0x9C3538  %d年
0x9C3540  %d歳
0x9C3548  父親武将一覧
0x9C3550  名前を入力してください
0x9C3558  年
0x9C3560  生年を入力してください
0x9C3568  歳
```

This establishes a character-creation/birth-year semantic cluster for localization entry 1706.

### 4.2 Entry 2630 — scenario/status/date cluster

Source slot:

`0x9C5238`

Index:

`(0x9C5238 - 0x9C0008) / 8 = 2630 = 0xA46`

Destination cell:

`0xA210E0 + 2630*8 = 0xA26310`

The source-slot neighborhood is:

```text
0x9C5220  セーブナンバー::%d
0x9C5228  状況::
0x9C5230  シナリオ
0x9C5238  年
0x9C5240  月
0x9C5248  日
0x9C5250  拠点
0x9C5258  場面
0x9C5260  空き大名家数
0x9C5268  天気
0x9C5270  イベント主命
0x9C5278  評定期限
```

This strongly distinguishes entry 2630 from entry 1706. It is the structurally relevant standalone `年` entry for scenario/status/date semantics.

This is stronger than treating `0x69785A` itself as one global semantic token: one pooled byte object feeds more than one logical localization ID.

## 5. Exact materialization chain for scenario/status `年` entry 2630

R1 traces entry 2630 through two relocation levels and the runtime copy layer.

### 5.1 Source side

- `0x9C5238` is RELA-materialized to point to rodata `0x69785A`.
- `0xA0ACC0` is separately RELA-materialized to point to source slot `0x9C5238`.

The JP-source copy block at mapped `0x427EC` performs:

```text
0x427E0  ADRP/LDR -> GOT-like destination reference
0x427E8  LDR x0,[x8]              ; destination byte-buffer pointer
0x427EC  ADRP x8,...
0x427F0  LDR  x8,[...,#0xCC0]     ; 0xA0ACC0 -> 0x9C5238
0x427F4  LDR  x1,[x8]             ; source char* -> 0x69785A
0x427F8  BL   0x454850
```

### 5.2 Destination side

- relocation/GOT slot `0xA035E8 -> BSS destination pointer cell 0xA26310`;
- `0x8B844..0x8B84C` stores the result of allocator `0x58B9F0` into `0xA26310`;
- `0x219E8..` loads the allocated pointer and clears a `0x90`-byte region;
- `0x427E0..0x427F8` copies from the first source table;
- corresponding generated copy blocks around `0x5C7E0` and `0x767E0` copy the same localization index from the second and third parallel source tables into the same destination buffer.

### 5.3 Copy helper semantics

Mapped `0x454850` is a NUL-terminated byte-string copy routine:

```text
454850  ldrb w8,[x1]
454854  mov  x9,x0
454858  cbz  w8,454870
45485c  add  x10,x1,#1
454860  mov  x9,x0
454864  strb w8,[x9],#1
454868  ldrb w8,[x10],#1
45486c  cbnz w8,454864
454870  strb wzr,[x9]
454874  ret
```

So the chain through runtime materialization is directly established:

`0x69785A -> 0x9C5238 -> 0xA0ACC0 -> copy@0x427EC -> allocated buffer referenced by 0xA26310`

## 6. Entry 1706 uses the same machinery independently

The other `年` source slot `0x9C3558` uses the same mechanism but a different localization ID and destination:

- source `0x9C3558`, index 1706;
- second-level relocation slot `0xA08FE0 -> 0x9C3558`;
- source load at `0x3C2DC..0x3C2E4`;
- destination relocation/GOT `0xA01908 -> 0xA24630`;
- call to the same copy helper `0x454850` at `0x3C2E8`.

Thus pooled rodata identity is not equivalent to localization-ID identity.

## 7. R489 is a structural positive-control for the same source/copy system

Canonical R489 (`シナリオを選んでください`) is at rodata `0x69B6A1` and first source slot `0x9C3288`.

Its source-table index is:

`(0x9C3288 - 0x9C0008) / 8 = 1616 = 0x650`

Its corresponding destination pointer cell is:

`0xA210E0 + 1616*8 = 0xA24360`

R489 is copied through the same generated localization machinery and the same `0x454850` byte-copy helper. This independently shows that the `年` chain is part of the normal localized-text materialization system rather than an isolated data accident.

R1 does not reclassify DCTRL7's R489 runtime observation; the exact R489 phrase was not visible in the retained DCTRL7 screenshots.

## 8. Downstream-consumer search and the remaining gap

The specific destination pointer cell for scenario/status `年`, `0xA26310`, is reached via relocation/GOT slot `0xA035E8`.

A direct code-reference census for that exact GOT slot found only five functional uses:

1. allocation/store of the destination buffer pointer (`0x8B844`);
2. zero/clear of the destination buffer (`0x219E8`);
3. first source-table copy (`0x427E0`);
4. second source-table copy (`0x5C7E0`);
5. third source-table copy (`0x767E0`).

No direct post-copy UI/read use of that exact destination GOT slot was found in `main`.

The same pattern holds for the entry-1706 destination cell and for R489's corresponding destination cell: their direct references are dominated by allocation/clear/language-copy lifecycle code.

Therefore the initial R1 assumption that one could simply continue `destination GOT -> reader -> screen` by following direct references is incomplete. The actual UI may consume the localization entry through an additional indirection, a higher-level object/model, a pool/index accessor not encoded as the numeric localization index, or another data path. R1 does not choose among those without evidence.

## 9. Scenario-name side evidence does not close the `年` consumer gap

A separate static scenario-name array exists at `0x9E9F28`, with the Japanese sequence including:

`乱麻の章 / 日輪の章 / 昇龍の章 / 覇道の章 / 転変の章 / 太平の章 / ...`

A selector around `0x3FDAF0` indexes parallel scenario-name pointer arrays using a scenario index and is called at `0x401164`.

This confirms that scenario chapter names have their own indexed data path. It does **not** prove that the tested `年` suffix is read from entry 2630 at the same call site. The chapter-name path and standalone `年` path must not be conflated merely because both are visible on the same scenario card.

## 10. Rejected numeric-index shortcut

The equality between a localization index and an immediate constant in unrelated code is not consumer evidence.

Examples investigated:

- `0x650` (= R489 source-table index 1616) appears as an argument to `0x4F6CC4` at `0x4E5060`;
- calls to `0x4F6CC4` also use unrelated fixed/dynamic sizes such as `0x68`, `0x70`, `0x108`, `0x110`, `0x2038`, and computed values;
- the only direct `0xA46` (= scenario/status `年` index 2630) immediate found at `0x4963A4` feeds `0x454FA4`, which simply stores four integer fields (`stp w1,w2` / `stp w3,w4`) and is not a localization lookup.

Therefore searching for raw integer `2630` or `1616` in code cannot establish a localization consumer.

## 11. R1 conclusion

R1 establishes a real localization materialization architecture and a critical semantic split:

- one pooled `年` rodata object feeds at least two independent localization IDs;
- entry 1706 belongs to character-creation/birth-year semantics;
- entry 2630 belongs to scenario/status/date semantics;
- entry 2630 is copied through an exact RELA/GOT/buffer chain;
- the final UI consumer after materialization is not yet directly bound.

The DCTRL7 runtime observation remains the runtime fact that some scenario-route consumer reaches the patched pooled `年`. The static evidence makes entry 2630 the strongest source-slot candidate for that route, but the final `entry 2630 -> tested scenario card` edge remains a hypothesis until a downstream reader/model path is proven.

## 12. Next-stage recommendation

Do not build or patch anything from R1 alone.

The next analysis should stay within the same consumer-resolution problem and determine how a materialized localization string leaves the allocation/copy layer. The preferred method is to identify one downstream access mechanism using a known UI-visible localized object, then reuse that mechanism for entry 2630 and later DATE-COMPOSITE / PLACE-FORMATTER families.

Do not return to raw immediate-value searches and do not equate pooled rodata address identity with one logical text ID.
