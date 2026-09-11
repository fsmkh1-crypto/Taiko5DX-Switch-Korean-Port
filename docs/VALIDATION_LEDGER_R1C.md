# VALIDATION LEDGER — R1C localization secondary-reference census

Date: 2026-09-11  
Scope: exhaustive static census of secondary references to all 3,803 localization runtime destination cells. Analysis only; no builder/patch/runtime artifact changes.

Detailed report: `docs/R1C_LOCALIZATION_SECONDARY_REFERENCE_CENSUS.md`

## V076 — secondary pointer-to-destination-cell references are sparse: exactly 7 of 3,803 localization IDs

**Claim:** Across the complete runtime destination-cell range `0xA210E0..0xA287B0`, exactly seven localization IDs have a second `R_AARCH64_RELATIVE` relocation pointing to their destination cell; the remaining 3,796 have exactly one inbound RELA reference.

**Status:** `VERIFIED`

**Evidence:**

Inbound-reference distribution:

```text
1 reference  : 3,796 cells
2 references :     7 cells
>2           :     0 cells
```

Seven double-referenced IDs:

```text
1314 武士勲功  secondary 0x9DF3A0
1315 商人勲功  secondary 0x9DF3A8
1316 忍者勲功  secondary 0x9DF3B0
1297 拠点      secondary 0x9E9690
1347 国        secondary 0x9E9698
400  勢力      secondary 0x9E96A0
1348 地方      secondary 0x9E96A8
```

The secondary references form exactly two contiguous static tables, of three and four entries respectively.

A `.text` scan for exact destination-cell materialization using direct `ADRP+ADD` and `ADRP+unsigned-load/store` forms found no exact materialization of any of the 3,803 cell addresses. This does not exclude runtime-computed access or pointer propagation.

**Consequence:** V075's four-entry structure is not a global second localization registry. It belongs to a sparse consumer-side selection family.

## V077 — both secondary tables are bounded selector tables; entry 2630 is outside this mechanism

**Claim:** The two secondary pointer-to-cell tables are directly code-indexed bounded selectors for small semantic label families. Entry 2630 (`年`, destination `0xA26310`) is not a member of either table and has no second static pointer-to-cell relocation.

**Status:** `VERIFIED`

**Evidence — 3-entry merit table:**

`0x9DF3A0..0x9DF3B0` contains:

```text
1314 武士勲功
1315 商人勲功
1316 忍者勲功
```

Reader `0x209C90..0x209CB0` bounds `w0 <= 2`, indexes `0x9DF3A0`, then dereferences the selected destination cell. The fallback path uses primary slot `0xA00CE0 -> destination 0xA23A08`, localization ID 1317 `海賊勲功`.

**Evidence — 4-entry category table:**

R1B V075 established `0x9E9690..0x9E96A8` as a bounded four-way selector for:

```text
1297 拠点
1347 国
400  勢力
1348 地方
```

**Entry 2630:**

- destination cell `0xA26310`;
- exactly one inbound RELA reference: primary/GOT-style slot `0xA035E8`;
- no membership in either secondary table.

**Reuse rule:** Do not continue searching for an R1B-style static secondary selector table for entry 2630. Its remaining consumer edge, if pursued later, must be sought through another mechanism such as primary-slot use, runtime pointer propagation/model storage, or computed access. This does not imply that entry 2630 lacks a consumer.
