# VALIDATION LEDGER — Stage 2 affine structural targeting

Date: 2026-09-11
Scope: Stage-1 inline target-resolution reduction. Documentation-only validation record; no builder/IPS/runtime modification.

Detailed report: `docs/STAGE2_AFFINE_STRUCTURAL_TARGETING.md`

## V078 — 22 exact affine blocks cover 13,771 inline source rows

**Claim:** The PC inline source corpus contains 22 contiguous fixed-delta blocks in which every row maps to a Switch target by `target = PC RVA + block delta` and every mapped target contains the exact expected original PC bytes.

**Status:** `VERIFIED`

**Evidence:**

- covered inline rows: 13,771 / 17,103 (80.518%);
- exact source-byte guards: 13,771 / 13,771 PASS;
- mapped replacement bytes: 184,142;
- mapped target interval overlaps: 0;
- blocks and deltas are enumerated in the detailed Stage 2 report.

**Boundary:** This proves structural target identity, not unconditional write authorization. Semantic/storage-family gates remain required.

## V079 — affine targeting resolves the location ambiguity of 9,802 Stage-1 exception rows

**Claim:** Of the 11,050 Stage-1 inline exceptions, 9,802 lie inside verified affine blocks and therefore no longer require raw-string occurrence selection to identify their Switch target.

**Status:** `VERIFIED`

**Evidence:**

Inside the 22 blocks:

- E_MULTI_CANDIDATE: 9,744
- E_REPLACEMENT_CONFLICT: 58
- E_OBJECT_UNKNOWN: 0

Residual after target-resolution:

- total: 1,248
- E_MULTI_CANDIDATE: 1,003
- E_OBJECT_UNKNOWN: 187
- E_REPLACEMENT_CONFLICT: 58

This removes target-location ambiguity from 88.706% of the Stage-1 exception population.

**Reuse rule:** Do not send affine-covered multi-candidate rows to per-string consumer tracing merely because Stage 1 marked them `E_MULTI_CANDIDATE`.

## V080 — three affine DATA blocks are not RELA pointer-cell writes

**Claim:** The three verified DATA affine blocks R16467-R17103 contain 637 rows whose mapped write ranges overlap no RELA target of any relocation type.

**Status:** `VERIFIED`

**Evidence:**

- R16467-R16872: 406 rows
- R16873-R16902: 30 rows
- R16903-R17103: 201 rows
- total: 637 rows
- mapped-write/RELA-target overlaps: 0

**Consequence:** A generic `DATA match => possible relocation pointer cell` rejection is invalid for these exact ranges.

## V081 — PC and Switch Japanese place tables are positionally aligned across the complete 310-record structure

**Claim:** PC place-table base `0xB512A0` aligns to Switch Japanese place-table base `0x6ADA10` under affine delta `-0x4A3890`, preserving the complete 310-record, stride-0x18 field layout.

**Status:** `VERIFIED`

**Evidence:**

- 310 name field starts at record `+0x01` align and match;
- 310 yomi field starts at record `+0x0C` align and match;
- five additional PC patch records that begin inside those fields also align and match;
- total place-range source records covered by the affine block: 625.

**Boundary:** Structural identity of yomi fields does not authorize yomi translation. Existing visible-vs-internal semantic gates remain in force.

## V082 — residual localization exceptions are substantially reducible by logical-entry context before consumer tracing

**Claim:** Among the 886 residual localization exceptions, full logical-object comparison against the complete 3,803-entry JP source table yields 608 rows with exactly one full JP logical-entry candidate, 189 with multiple candidates, and 89 with no full JP logical object.

**Status:** `VERIFIED`

**Evidence:**

```text
1 full JP logical-entry candidate : 608
2+ candidates                     : 189
0 candidates                      :  89
                                  ----
total                             : 886
```

**Boundary:** A unique full logical-entry candidate is not yet a terminal semantic/write disposition. Source-context-to-logical-entry correspondence must be established as a family rule, especially for short/common strings and composite suffixes.

**Next-use rule:** Analyze these 886 as a localization family. Do not consumer-trace all 886 individually and do not close them by raw value equality alone.

## Rejected hypotheses retained

- Raw `E_MULTI_CANDIDATE` necessarily implies an individual consumer-trace problem: rejected by V078/V079.
- Same original bytes with differing PC replacements necessarily form a global semantic conflict: rejected for at least the 58 affine-covered conflict rows.
- DATA candidates in the three verified affine ranges may be relocation pointer cells merely because they reside in DATA: rejected by V080.
- Pooled rodata identity or raw uniqueness can stand in for logical localization identity: remains rejected by R1-R1C and is not reopened here.

Stage 2 stops at structural target resolution and residual-family classification. A fresh user execution signal is required for the next localization-family analysis or any implementation/build work.
