# VALIDATION LEDGER — R1 localization registry trace

Date: 2026-09-11  
Scope: localization source-table/materialization architecture for standalone `年 @ 0x69785A`. No patch/build modification is part of V070-V073.

Detailed report: `docs/R1_LOCALIZATION_REGISTRY_TRACE.md`

## V070 — localized text uses three parallel 3,803-entry source pointer tables and indexed runtime destination cells

**Claim:** The exact Switch v1.1.3 `main` contains three structurally parallel 3,803-entry source pointer tables beginning at `0x9C0008`, `0x9C76E0`, and `0x9CEDB8`, plus a same-index run of runtime destination pointer cells beginning at `0xA210E0`.

**Status:** `VERIFIED`

**Evidence:**

- source-table spacing `0x76D8 = 3,803 * 8`;
- first-table index formula `(source_slot - 0x9C0008)/8`;
- destination formula `0xA210E0 + index*8`;
- generated allocation/clear/copy blocks preserve the same per-entry correspondence;
- `0x9C0000` is used separately by module/DSO-style registration paths and is not localization entry zero.

**Limit:** R1 does not assign semantic language names to the second/third parallel source tables.

## V071 — pooled `年 @ 0x69785A` feeds two distinct localization IDs with different semantic neighborhoods

**Claim:** The one pooled rodata object `年 @ 0x69785A` is referenced by two distinct first-source-table entries and therefore must not be treated as one global logical text ID.

**Status:** `VERIFIED`

**Evidence:**

- `0x9C3558 -> 0x69785A`, index 1706 (`0x6AA`), destination cell `0xA24630`;
- neighborhood contains `新規作成 / 内容変更 / 武将削除 / %d年 / %d歳 / 父親武将一覧 / 名前を入力してください / 年 / 生年を入力してください / 歳`, establishing character-creation/birth-year semantics;
- `0x9C5238 -> 0x69785A`, index 2630 (`0xA46`), destination cell `0xA26310`;
- neighborhood contains `セーブナンバー::%d / 状況:: / シナリオ / 年 / 月 / 日 / 拠点 / 場面 / 空き大名家数 / 天気 / イベント主命 / 評定期限`, establishing scenario/status/date semantics.

**Reuse rule:** Future repeated-object recovery must distinguish logical localization entries from pooled rodata byte identity.

## V072 — scenario/status `年` entry 2630 has an exact RELA/GOT/copy materialization chain

**Claim:** Localization entry 2630 for the scenario/status/date `年` is directly traceable from pooled rodata through the first source slot into an allocated runtime byte buffer.

**Status:** `VERIFIED`

**Evidence:**

- rodata `0x69785A -> source slot 0x9C5238` by `R_AARCH64_RELATIVE`;
- relocation slot `0xA0ACC0 -> 0x9C5238`;
- copy block `0x427EC..0x427F8` loads the source char pointer and calls `0x454850`;
- destination GOT/relocation `0xA035E8 -> destination pointer cell 0xA26310`;
- allocation/store at `0x8B844..0x8B84C` and clear at `0x219E8..`;
- parallel source-table copies occur around `0x5C7E0` and `0x767E0` into the same destination buffer;
- `0x454850` is directly disassembled as a NUL-terminated byte-string copy loop.

**Limit:** A direct post-copy UI reader connecting `0xA26310` to the tested scenario card was not found in R1. Do not promote `entry 2630 -> tested scenario screen` to VERIFIED yet. DCTRL7 V064 remains the independent runtime observation that the pooled `年` replacement is consumed on the scenario route.

## V073 — direct destination-GOT following is insufficient to identify the UI consumer for entry 2630

**Claim:** For the exact scenario/status `年` destination cell, direct references to its GOT/relocation slot account for allocation, clear, and three parallel source-copy operations but not a post-copy UI/read consumer; therefore the R1 consumer search cannot be completed by direct destination-GOT XREF following alone.

**Status:** `VERIFIED`

**Evidence:**

Direct functional references to `0xA035E8 -> 0xA26310` are limited to:

- allocation/store at `0x8B844`;
- clear at `0x219E8`;
- first-table copy at `0x427E0`;
- second-table copy at `0x5C7E0`;
- third-table copy at `0x767E0`.

The same lifecycle-dominated pattern is present for the independent `年` entry 1706 and for canonical R489's corresponding runtime destination.

**Rejected shortcut:** Numeric immediate equality is not localization-ID evidence. `0xA46` at `0x4963A4` feeds non-localization helper `0x454FA4`, and `0x650` at `0x4E5060` is used in a separate object/resource path. Do not search raw integer IDs and infer a consumer from value equality.

**Next-use rule:** Consumer tracing must identify the additional indirection/model/access mechanism after localization materialization before DATE-COMPOSITE or PLACE-FORMATTER screen binding is called complete.
