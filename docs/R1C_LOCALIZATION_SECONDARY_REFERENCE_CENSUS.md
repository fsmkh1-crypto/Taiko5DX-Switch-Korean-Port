# R1C localization secondary-reference census

Date: 2026-09-11  
Scope: analysis-only follow-up to R1B. No builder, patch, IPS, ZIP, runtime artifact, game file, or aggregate project document was modified.

## 1. Goal

R1B proved one concrete post-materialization pointer-to-destination-cell selector at `0x9E9690`. R1C tests whether that mechanism is a one-off, a broad localization registry, or a small repeated structural family.

The analysis therefore surveys the complete 3,803-entry runtime destination-cell range rather than tracing one visible string at a time.

## 2. Fixed input

- Switch v1.1.3 Build ID `D9120950C258610A746F4A31CE3A3B376DE393D9`
- compressed `main` SHA-256 `b366e692208f3c0cc18bc1884ef95689b6b11d722fa2d749b8500abccbc3109b`
- destination-cell range: `0xA210E0 .. 0xA287B0`, 3,803 entries at 8-byte stride
- RELA: `0x58D078`, size `0xECC70`, entry size `0x18`

R1/R1B facts V070-V075 were reused rather than revalidated.

## 3. Exhaustive inbound-RELA census

Every one of the 3,803 destination cells has at least one `R_AARCH64_RELATIVE` relocation whose addend is that exact cell address.

Inbound-reference count distribution:

```text
1 RELA reference : 3,796 destination cells
2 RELA references:     7 destination cells
>2 references     :     0 destination cells
```

Therefore the R1B secondary pointer-to-cell pattern is not a second global registry covering all localization entries. It is sparse.

The seven double-referenced IDs are exactly:

```text
ID 1314  武士勲功   dest 0xA239F0   secondary 0x9DF3A0
ID 1315  商人勲功   dest 0xA239F8   secondary 0x9DF3A8
ID 1316  忍者勲功   dest 0xA23A00   secondary 0x9DF3B0

ID 1297  拠点       dest 0xA23968   secondary 0x9E9690
ID 1347  国         dest 0xA23AF8   secondary 0x9E9698
ID 400   勢力       dest 0xA21D60   secondary 0x9E96A0
ID 1348  地方       dest 0xA23B00   secondary 0x9E96A8
```

The secondary references form exactly two contiguous static tables: one 3-entry table and one 4-entry table.

## 4. The 3-entry table is also a real selector

The table at `0x9DF3A0` is directly consumed by code at `0x209C90..0x209CB0`.

Relevant instructions:

```text
0x209C90  cmp  w0,#2
0x209C94  b.hi 0x209CA8
0x209C98  adrp x8,0x9DF000
0x209C9C  add  x8,x8,#0x3A0
0x209CA0  ldr  x8,[x8,w0,sxtw #3]
0x209CA4  b    0x209CB0
0x209CA8  adrp x8,0xA00000
0x209CAC  ldr  x8,[x8,#0xCE0]
0x209CB0  ldr  x0,[x8]
```

Table members:

```text
selector 0 -> ID 1314 武士勲功
selector 1 -> ID 1315 商人勲功
selector 2 -> ID 1316 忍者勲功
```

The out-of-range/fallback slot `0xA00CE0` points to destination cell `0xA23A08`, which is localization ID 1317 `海賊勲功`.

Thus the four merit labels form one runtime selection family, implemented as three secondary table entries plus one fallback primary slot.

## 5. The 4-entry R1B table is a second selector family

R1B already established code at `0x3DFA60..0x3DFA84` selecting among:

```text
ID 1297  拠点
ID 1347  国
ID 400   勢力
ID 1348  地方
```

The new census shows these are not four arbitrary examples from a larger secondary registry. They are the complete second contiguous secondary table.

## 6. Direct-code materialization check

A `.text` scan for exact PC-relative materialization of any destination-cell address in the 3,803-entry range using direct `ADRP+ADD` and `ADRP+unsigned-load/store` forms found zero exact destination-cell materializations.

This does not rule out runtime-computed indexing or pointer propagation, but it rules out the obvious alternative that the 3,796 single-RELA entries are broadly bypassed by direct exact cell-address references in ordinary AArch64 address materialization.

## 7. Consequence for entry 2630 `年`

Entry 2630 destination cell `0xA26310` has exactly one inbound RELA reference, the already-known primary/GOT-style slot `0xA035E8`.

It is not a member of either secondary selector table and has no second static pointer-to-cell relocation.

Therefore the exact R1B mechanism:

```text
destination cell
-> small static pointer-to-cell selector table
-> destination cell dereference
-> runtime buffer
```

is not the static structure used by entry 2630.

This does **not** mean entry 2630 lacks a consumer. It means further work should stop looking for another copy of the R1B four-entry-table mechanism and instead investigate a different post-materialization path: direct use through its primary slot, pointer propagation into another runtime object/model, or runtime-computed access.

## 8. Structural interpretation

The secondary pointer-to-cell mechanism is best classified as a sparse enum/category selection optimization rather than a general localization registry.

Observed families:

1. merit-role labels: `武士勲功 / 商人勲功 / 忍者勲功 / 海賊勲功`;
2. category/location labels: `拠点 / 国 / 勢力 / 地方`.

This changes the next search strategy. The localization architecture still has a general 3,803-entry source/destination materialization layer, but the R1B secondary table is a special consumer-side selection pattern used only by a small subset.

## 9. Stopping point

R1C has answered the family-scope question:

- the R1B structure is repeated, not unique;
- it is sparse, not global;
- exactly two static secondary pointer-to-cell selector tables cover seven of 3,803 destination IDs;
- entry 2630 is outside that family.

No DATE-COMPOSITE, PLACE-FORMATTER, builder, patch, or runtime-build work was started.
