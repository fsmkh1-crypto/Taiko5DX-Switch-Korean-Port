# VALIDATION LEDGER — R1B localization secondary indirection

Date: 2026-09-11  
Scope: analysis-only continuation of R1. No builder, patch, IPS, ZIP, runtime artifact, game file, or aggregate project document was modified.

Detailed report: `docs/R1B_LOCALIZATION_SECONDARY_INDIRECTION.md`

## V074 — pooled `拠点 @ 0x6A3D6B` feeds four distinct first-table localization IDs

**Claim:** The one pooled rodata object `拠点 @ 0x6A3D6B` is referenced by four distinct entries in the first 3,803-entry localization source table and must not be treated as one logical localization ID.

**Status:** `VERIFIED`

**Evidence:**

- entry 402: source `0x9C0C98`, destination `0xA21D70`;
- entry 1297: source `0x9C2890`, destination `0xA23968`;
- entry 1620: source `0x9C32A8`, destination `0xA24380`;
- entry 2633: source `0x9C5250`, destination `0xA26328`;
- all four first-table source slots are `R_AARCH64_RELATIVE`-materialized to the same rodata object `0x6A3D6B`;
- the four source-table neighborhoods are semantically distinct.

**Runtime anchor:** DCTRL7's retained basic-information screenshot visibly contains `拠点 岡崎城`. This proves the visible lexeme is consumed on that route, but it does not by itself identify which of the four localization IDs supplies that screen.

**Reuse rule:** Do not equate visible `拠点` with entry 2633 solely because entry 2633 is adjacent to `年/月/日`. Logical-ID binding must use downstream consumer evidence.

## V075 — entry 1297 participates in a four-entry secondary pointer-to-destination-cell table with a direct runtime-buffer reader

**Claim:** Localization entry 1297 (`拠点`) has a post-materialization indirection through a four-entry static table of pointers to runtime destination cells, and code directly indexes that table, dereferences the selected destination cell, and passes the resulting runtime string pointer to a consumer call.

**Status:** `VERIFIED`

**Evidence:**

Entry 1297 destination:

- destination cell `0xA23968`;
- ordinary GOT-style relocation `0xA00C28 -> 0xA23968`;
- additional relocation `0x9E9690 -> 0xA23968`.

Four-entry secondary table:

```text
0x9E9690 -> 0xA23968  entry 1297  拠点
0x9E9698 -> 0xA23AF8  entry 1347  国
0x9E96A0 -> 0xA21D60  entry 400   勢力
0x9E96A8 -> 0xA23B00  entry 1348  地方
```

Reader at `0x3DFA60..0x3DFA84`:

- bounds selector with `cmp w24,#3`;
- materializes table base `0x9E9690` at `0x3DFA68..0x3DFA6C`;
- `0x3DFA74` loads the selected pointer-to-destination-cell;
- `0x3DFA78` dereferences that cell into `x1`, yielding the runtime string-buffer pointer;
- `0x3DFA84` calls `0x25F754` with that string pointer.

Corroborating entry-1297 post-copy readers:

- `0x4B48CC..0x4B48E0` loads the entry-1297 runtime string through ordinary GOT slot `0xA00C28` and passes it as `x2` to `0x44758C`;
- `0x4B4D98..0x4B4DAC` repeats the same pattern;
- `0x44758C` forwards non-null `x2` as a string argument into `0x432760` after object setup.

**What is established:** the localization materialization layer can feed at least one additional pointer-to-cell selector/registry layer before a UI-side consumer receives the runtime string.

**Limits:**

- V075 does not prove entry 1297 is definitively the exact `拠点` ID used by the retained basic-information screenshot; its semantic neighborhood makes it the strongest current candidate.
- V075 does not prove entry 2630 `年` uses this same four-entry table mechanism.
- exact semantic naming of `0x25F754`, `0x44758C`, and their final UI widget/render role remains open.

**Next-use rule:** Future R1 continuation may search for an analogous secondary pointer-to-cell table or selector for entry 2630, but must not infer one merely from V075. A fresh execution signal is required before that work.
