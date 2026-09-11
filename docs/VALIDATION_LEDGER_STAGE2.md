# VALIDATION LEDGER — Stage 2 affine structural targeting

Date: 2026-09-11
Scope: Stage-1 inline target-resolution reduction. Documentation-only validation record; no builder/IPS/runtime modification.

Detailed report: `docs/STAGE2_AFFINE_STRUCTURAL_TARGETING.md`

## V082 — 22 exact affine blocks cover 13,771 inline source rows

**Status:** `VERIFIED`

The PC inline corpus contains 22 contiguous fixed-delta blocks satisfying `target = PC RVA + block delta`.

Evidence:
- covered rows: 13,771 / 17,103;
- exact source-byte guards: 13,771 / 13,771 PASS;
- mapped target overlaps: 0;
- detailed block table is in the Stage 2 report.

Boundary: target identity is verified; unconditional write authorization is not.

## V083 — affine targeting resolves 9,802 Stage-1 exception rows at the target-location layer

**Status:** `VERIFIED`

Inside the 22 blocks:
- `E_MULTI_CANDIDATE`: 9,744;
- `E_REPLACEMENT_CONFLICT`: 58;
- `E_OBJECT_UNKNOWN`: 0.

Residual after target resolution:
- total: 1,248;
- `E_MULTI_CANDIDATE`: 1,003;
- `E_OBJECT_UNKNOWN`: 187;
- `E_REPLACEMENT_CONFLICT`: 58.

Reuse rule: do not send affine-covered rows to per-string consumer tracing merely because Stage 1 marked them ambiguous.

## V084 — the three affine DATA blocks are not RELA pointer-cell writes

**Status:** `VERIFIED`

R16467-R17103 contain 637 mapped rows. Their mapped write ranges overlap no RELA target of any relocation type.

Consequence: `DATA => possible relocation pointer cell` is invalid for these exact ranges.

## V085 — PC and Switch Japanese place tables are positionally aligned across all 310 records

**Status:** `VERIFIED`

PC base `0xB512A0` aligns to Switch JP base `0x6ADA10` with delta `-0x4A3890`.

- 310 name starts at `+0x01` align and match;
- 310 yomi starts at `+0x0C` align and match;
- five additional in-field PC records also align and match;
- total place-range rows: 625.

Boundary: yomi structural identity does not authorize yomi translation; I7 remains in force.

## V086 — residual localization exceptions are reducible by logical-entry context before consumer tracing

**Status:** `VERIFIED`

Among 886 residual localization exceptions, full logical-object comparison against the complete 3,803-entry JP source table yields:

```text
1 full JP logical-entry candidate : 608
2+ candidates                     : 189
0 candidates                      :  89
                                  ----
total                             : 886
```

Boundary: one full logical-entry candidate is not a terminal write disposition. Source-context-to-logical-entry correspondence still requires a family rule.

Next-use rule: analyze the 886 as a localization family rather than tracing all 886 individually.

## Rejected hypotheses retained

- raw multi-candidate necessarily implies an individual consumer-trace problem: rejected by V082/V083;
- same original bytes with differing replacements necessarily form a global semantic conflict: rejected for the 58 affine-covered rows;
- DATA rows in the three verified affine ranges may be RELA pointer cells merely because they are in DATA: rejected by V084;
- pooled rodata identity or raw uniqueness can stand in for logical localization identity: remains rejected by R1-R1C.

Stage 2 stops here. Fresh execution signal required for the next family analysis or implementation/build work.
