# STAGE 2 — affine structural targeting

Date: 2026-09-11
Scope: Stage-1 inline exception reduction by corpus-wide structural targeting. Documentation only. No builder, IPS, runtime artifact, game file, or validator code modification is included in this stage.

## 1. Confirmed facts

A fixed-delta structural sweep over the PC inline source corpus identifies 22 exact affine blocks. Every row in each block satisfies:

`Switch target = PC RVA + block delta`

and the original PC byte sequence matches exactly at the computed Switch target.

Aggregate result:

- inline source rows: 17,103
- structurally targeted rows: 13,771 (80.518%)
- mapped replacement bytes: 184,142
- exact original-byte guards: 13,771 / 13,771 PASS
- mapped-target overlaps: 0
- Stage-1 exceptions inside these blocks: 9,802
- Stage-1 total inline exceptions: 11,050
- residual exceptions after structural target resolution: 1,248

This resolves target-location ambiguity for 88.706% of the Stage-1 exception population. It does not by itself authorize every write semantically.

## 2. Exact affine blocks

| block | PC rows | delta | rows | prior exceptions | storage |
|---:|---|---:|---:|---:|---|
| 1 | R3251-R3875 | -0x4A3890 | 625 | 243 | RODATA |
| 2 | R3876-R3996 | -0x476E80 | 121 | 11 | RODATA |
| 3 | R3997-R4188 | -0x476700 | 192 | 21 | RODATA |
| 4 | R4189-R4417 | -0x4769E0 | 229 | 52 | RODATA |
| 5 | R4418-R4569 | -0x477074 | 152 | 15 | RODATA |
| 6 | R4570-R14429 | -0x4AE480 | 9,860 | 8,884 | RODATA |
| 7 | R14430-R14541 | -0x4A4EAC | 112 | 16 | RODATA |
| 8 | R14551-R14683 | -0x4C3A6E | 133 | 55 | RODATA |
| 9 | R14737-R15462 | -0x4C6E50 | 726 | 61 | RODATA |
| 10 | R15463-R15613 | -0x4C8A34 | 151 | 110 | RODATA |
| 11 | R15614-R15619 | -0x4C9584 | 6 | 4 | RODATA |
| 12 | R15620-R15679 | -0x4C8DD7 | 60 | 28 | RODATA |
| 13 | R15680-R15719 | -0x4C909A | 40 | 0 | RODATA |
| 14 | R15720-R15927 | -0x4B5869 | 208 | 48 | RODATA |
| 15 | R15928-R16229 | -0x4CF306 | 302 | 17 | RODATA |
| 16 | R16230-R16284 | -0x4D8311 | 55 | 40 | RODATA |
| 17 | R16285-R16367 | -0x4D84D4 | 83 | 35 | RODATA |
| 18 | R16368-R16427 | -0x4D878C | 60 | 48 | RODATA |
| 19 | R16428-R16446 | -0x4D87CF | 19 | 5 | RODATA |
| 20 | R16467-R16872 | -0x67C7CC | 406 | 47 | DATA |
| 21 | R16873-R16902 | -0x6804B8 | 30 | 5 | DATA |
| 22 | R16903-R17103 | -0x680238 | 201 | 57 | DATA |

The three DATA blocks contain 637 rows and none of their mapped write ranges overlap any RELA target of any relocation type. They are therefore not relocation pointer cells.

## 3. Exception effect

Stage-1 exception rows inside the 22 blocks:

- E_MULTI_CANDIDATE: 9,744
- E_REPLACEMENT_CONFLICT: 58
- E_OBJECT_UNKNOWN: 0

The 58 replacement-conflict rows are positional/contextual conflicts created by grouping identical original bytes across different PC RVAs. The affine mapping assigns each source record to a distinct Switch position, so raw-value conflict is not sufficient reason to reject these rows.

Residual exception population outside the affine blocks:

- total: 1,248
- E_MULTI_CANDIDATE: 1,003
- E_OBJECT_UNKNOWN: 187
- E_REPLACEMENT_CONFLICT: 58

By semantic family:

- LOCALIZATION_CANDIDATE: 886
- UNCLASSIFIED_INLINE: 327
- FORMATTER_CANDIDATE: 35

## 4. Place-table structural result

The PC place-table base is structurally aligned at `0xB512A0` to the Switch Japanese place table at `0x6ADA10` using delta `-0x4A3890`.

For all 310 records:

- name field start: `record + 0x01`
- yomi field start: `record + 0x0C`
- all 620 field-start source records align and match exact bytes

Five additional PC patch records begin inside those fixed fields rather than at field start, producing 625 total records in the affine place-table range. All five also match by exact relative offset.

This proves structural target identity. It does not change the existing rule that yomi is not automatically a translation/write target; visible display semantics and internal sort/input semantics remain separate gates.

## 5. Residual localization result

Among the 886 residual localization exceptions, comparison against the complete 3,803-entry JP logical source table gives:

- exactly one full logical-entry candidate: 608
- two or more full logical-entry candidates: 189
- no full logical object: 89

A global order comparison also shows strong sequence correspondence between the early PC inline corpus and the Switch JP logical table, but this stage does not promote sequence coincidence alone to a terminal port rule.

The next localization stage should therefore apply logical-entry/table-context rules before any per-string consumer tracing. Common short strings and composite suffixes must not be resolved by value equality alone.

## 6. Rejected shortcuts

The following approaches are rejected for future work:

1. Treating every raw multi-candidate row as requiring individual consumer tracing. At least 9,744 such exceptions are structurally target-resolved by affine blocks.
2. Treating same original bytes with different PC replacements as a global semantic conflict. At least 58 such rows are positionally disambiguated by affine structure.
3. Treating every DATA match as a possible relocation pointer cell. The 637 rows in the three exact DATA blocks have zero overlap with all RELA targets.
4. Treating pooled rodata identity or raw uniqueness as logical-text identity. R1-R1C already disproved that shortcut for localization objects.

## 7. Rule boundary

Proposed structural rule:

`AFFINE_STATIC_BLOCK_PORT`

Target-resolution semantics:

`PC source record -> exact block membership -> target = PC RVA + block delta -> exact original-byte guard`

This stage verifies target resolution only. Final write disposition still requires the applicable semantic/storage-family gate, especially for yomi, localization composites, and formatter behavior.

## 8. Next stage

Stage 2 is complete and stops here.

Recommended next analysis scope after a fresh user execution signal:

- residual localization family only: 886 rows
- prioritize the 608 rows with exactly one full JP logical-entry candidate
- derive source-context-to-logical-entry rules corpus-wide before consumer tracing
- keep date suffix/composite and place formatter families grouped rather than tracing individual visible words

Do not modify builder, emit IPS, or create a runtime diagnostic artifact without a new explicit execution signal.
