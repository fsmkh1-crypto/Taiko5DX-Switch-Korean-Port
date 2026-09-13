# PC Korean Patch Oracle Assisted 297 Follow-up V1

Date: 2026-09-13 (KST)  
Status: CANONICAL READ-ONLY FOLLOW-UP / NO SWITCH WRITE AUTHORIZATION  
Parent HEAD: `8999a65ec97b4a81391f7030d76d9d175aa5b816`

## 요약

This follow-up consumes the canonical `ORACLE_ASSISTED = 297` membership from PC Patch Oracle Resolver V1 without reopening the stable 986 structural partition or the already-canonical Oracle V1 routing.

The 297 rows were analyzed in three exact, disjoint 99-row batches. The taxonomy is normalized to the Batch-1 rule:

- `TARGET_RESOLVED`: independent Switch semantic/logical object counterpart is resolved.
- `COMPOSITE_OR_FORMATTER_RESOLVED`: the PC occurrence belongs to a longer Switch object, split/composite, unit/format string, or formatter/template counterpart.
- `NEED_TRACE`: semantic meaning is narrowed, but owner/consumer binding still requires structural trace.

Normalized result:

| Disposition | Batch 1 | Batch 2 | Batch 3 | Total |
|---|---:|---:|---:|---:|
| `TARGET_RESOLVED` | 6 | 13 | 46 | **65** |
| `COMPOSITE_OR_FORMATTER_RESOLVED` | 92 | 86 | 53 | **231** |
| `NEED_TRACE` | 1 | 0 | 0 | **1** |
| **Total** | **99** | **99** | **99** | **297** |

Semantic counterpart closure is therefore **296 / 297**. The only follow-up residual is `R19`, retained as `NEED_TRACE`.

Machine-readable artifacts:
- `data/post_freeze/pc_patch_oracle_assisted_297_followup_v1/MEMBERSHIP.json`
- semantic SHA-256 `506b10ce073ce0d87feabe4c031f1b16b6ea0267d177c99090d921b1a47f0848`
- `data/post_freeze/pc_patch_oracle_assisted_297_followup_v1/INDEX.json`
- semantic SHA-256 `2746d7b89f1c829855ba714a332f50b543f6956685d35b5a228bd1e76c9b9679`

This stage still creates **zero Switch write authorizations**. `TARGET_RESOLVED` and `COMPOSITE_OR_FORMATTER_RESOLVED` are counterpart-routing dispositions, not `WRITE_SAFE` outcomes.

## 1. 확정된 사실

### 가. Canonical 297 membership was consumed unchanged

The union of the three 99-row batches equals the canonical Oracle V1 `ORACLE_ASSISTED` membership exactly:

- population: `297`
- batch intersection: `0`
- normalized disposition intersection: `0`
- unclassified: `0`
- missing canonical assisted rows: `0`
- extra rows: `0`

Oracle V1 remains provenance and is not overwritten.

### 나. Batch 1 remains 6 / 92 / 1

Batch 1 is preserved unchanged:

- `TARGET_RESOLVED = 6`
- `COMPOSITE_OR_FORMATTER_RESOLVED = 92`
- `NEED_TRACE = 1`

The one residual is `R19`. Its meaning is not the blocker; the unresolved point is owner selection between competing PC occurrence/context candidates around the expanded Switch attack-selection structure.

### 다. Batch 2 recheck confirms 13 / 86 / 0

Batch 2 was rechecked under the same Batch-1 taxonomy and required **zero label changes**.

Representative distinctions:
- `R1580`, `R1582`, `R2285`, `R2286`, `R2311`, `R2323` are independent semantic/logical objects and remain `TARGET_RESOLVED`.
- `R1490`, `R1588`, `R1639`, `R1641`, `R1642`, `R2085`, `R2086`, `R2103`, `R2182`, `R2183`, `R2186`, `R2195`, `R2196` are longer-object fragments or formatter/unit objects and remain `COMPOSITE_OR_FORMATTER_RESOLVED`.

Final Batch 2 counts:
- `TARGET_RESOLVED = 13`
- `COMPOSITE_OR_FORMATTER_RESOLVED = 86`
- residual = `0`

### 라. Batch 3 normalizes to 46 / 53 / 0

Batch 3 resolves all 99 rows. T2/T3 rows confirm that the PC patch's contiguous role/item tables are not preserved as one identical contiguous table on Switch; the relevant Japanese labels are redistributed among Switch raw string pools.

This is a layout/ownership migration, not a new translation problem.

Examples:
- T2 labels such as `家老`, `国主`, `水夫`, `職人`, `医師`, `賊` have Switch counterparts.
- T3 labels `具足`, `名馬`, `屏風`, `茶釜`, `茶壺`, `香炉`, `兵法書` have Switch counterparts.
- `R14687` is a composite window for `侍大将`, not an independent one-character target.

Final Batch 3 counts:
- `TARGET_RESOLVED = 46`
- `COMPOSITE_OR_FORMATTER_RESOLVED = 53`
- residual = `0`

### 마. The prior count-only 93 / 203 / 1 summary is rejected

A prior noncanonical automation summary implied:

- `TARGET_RESOLVED = 93`
- `COMPOSITE_OR_FORMATTER_RESOLVED = 203`
- `NEED_TRACE = 1`

That count-only taxonomy is inconsistent with the Batch-1 definition and is not canonical evidence.

Applying one taxonomy consistently across all three batches yields:

```text
TARGET_RESOLVED                         65
COMPOSITE_OR_FORMATTER_RESOLVED        231
NEED_TRACE                               1
                                      ---
TOTAL                                  297
```

### 바. Effective forward routing after this overlay

Oracle V1 remains the historical routing artifact. This follow-up refines only its `ORACLE_ASSISTED 297` branch.

Effective forward state:

```text
BASE_ORACLE_RESOLVED                    656
BASE_ORACLE_REROUTED                      7
FOLLOWUP_TARGET_RESOLVED                 65
FOLLOWUP_COMPOSITE_OR_FORMATTER_RESOLVED 231
ASTRA_REQUIRED                           10
TRACE_REQUIRED                           17
                                        ---
TOTAL                                   986
ORACLE_ASSISTED_REMAINDER                 0
```

The trace queue grows from 16 to 17 only because `R19` moves from the assisted follow-up population to trace-required ownership analysis.

Existing `ASTRA_REQUIRED 10` remains unchanged.

## 2. 유력한 가설

The principal cause of the original 297 assisted population was not broad translation ambiguity. It was mostly granularity mismatch between PC patch occurrences and Switch logical objects:

- split names or labels;
- prefix/suffix windows;
- formatter/unit fragments;
- composite strings;
- PC contiguous tables redistributed into Switch pools.

`R19` is likewise more likely an owner/consumer binding problem than a semantic-language problem.

## 3. 미확정 사항

This follow-up does not establish:

- write capacity;
- terminator placement;
- overlap safety;
- shared-owner mutation safety;
- formatter argument preservation at runtime;
- consumer-pointer/action construction;
- Switch replacement payload design.

The exact target PC EXE remains unavailable, so no new target-build XREF/preimage ownership claim is made.

The existing ten Astra rows and original sixteen trace rows are not reanalyzed here.

## 4. 기각된 가설

The following are rejected:

1. The prior count-only `93 / 203 / 1` taxonomy is canonical.
2. Any standalone same-text Switch occurrence is automatically the semantic owner.
3. A full logical object containing format syntax should automatically be labeled `TARGET_RESOLVED`.
4. Short unit/label fragments may be classified without PC/Switch sequence context.
5. NUL suppression in the PC patch is automatically a Switch write instruction.
6. Counterpart resolution implies `WRITE_SAFE`.

## 5. 관련 영향 범위

This overlay changes only the effective routing of Oracle V1's 297 assisted rows.

Unchanged:
- FZ001;
- F1 accepted 262;
- F1 static write-authorized 158;
- Stage-2 affine mappings;
- stable forward 986 structural membership;
- PC DLL/runtime canonical facts;
- porting framework;
- builder/IPS/runtime implementation;
- game files.

Framework change: `false`  
Builder/runtime change: `false`  
New Switch write authorization: `0`

## 6. 수정 제안

No implementation modification is proposed by this documentation stage.

Next recommended read-only scope:

`PC_PATCH_ORACLE_RESIDUAL_27_TRIAGE`

Effective residual queues:
- `ASTRA_REQUIRED = 10`
- `TRACE_REQUIRED = 17` including new `R19`

Semantic adjudication and structural/consumer tracing should remain separate bounded scopes.

## 7. Exact normalized membership

### TARGET_RESOLVED — 65

R90, R463, R464, R467, R468, R1051, R1344, R1347, R1348, R1580, R1582, R2025, R2030, R2056, R2075, R2285
R2286, R2311, R2323, R2373, R2392, R2420, R2432, R2487, R2489, R2609, R2705, R2821, R2826, R2874, R2913, R3021
R3022, R3047, R3099, R3100, R3161, R3181, R3182, R14689, R14690, R14693, R14694, R14695, R14696, R14697, R14699, R14700
R14702, R14703, R14704, R14706, R14710, R14711, R14712, R14715, R14716, R14717, R14718, R14720, R14721, R14722, R14723, R14724
R14736

### COMPOSITE_OR_FORMATTER_RESOLVED — 231

R10, R29, R46, R54, R55, R56, R60, R61, R64, R67, R69, R70, R78, R79, R80, R81
R82, R83, R210, R211, R213, R214, R265, R266, R267, R269, R270, R271, R273, R277, R280, R281
R282, R288, R292, R297, R302, R304, R306, R320, R344, R374, R459, R473, R483, R486, R571, R592
R643, R652, R660, R666, R678, R774, R777, R802, R824, R960, R968, R1033, R1034, R1035, R1057, R1066
R1067, R1068, R1070, R1071, R1072, R1088, R1091, R1097, R1106, R1113, R1122, R1129, R1132, R1135, R1137, R1139
R1141, R1143, R1148, R1152, R1155, R1163, R1168, R1171, R1191, R1195, R1265, R1279, R1289, R1291, R1452, R1454
R1456, R1458, R1460, R1490, R1504, R1507, R1516, R1519, R1526, R1528, R1588, R1593, R1594, R1633, R1634, R1639
R1641, R1642, R1695, R1697, R1699, R1715, R1717, R1719, R1744, R1745, R1819, R1840, R1871, R1953, R1956, R1957
R1960, R1995, R1996, R2050, R2054, R2055, R2085, R2086, R2087, R2099, R2103, R2114, R2118, R2124, R2128, R2157
R2159, R2166, R2182, R2183, R2186, R2195, R2196, R2255, R2281, R2283, R2284, R2291, R2292, R2294, R2295, R2296
R2297, R2298, R2299, R2300, R2301, R2302, R2303, R2306, R2307, R2308, R2309, R2310, R2312, R2313, R2318, R2319
R2322, R2324, R2325, R2326, R2350, R2380, R2383, R2447, R2552, R2554, R2555, R2556, R2557, R2558, R2559, R2563
R2655, R2656, R2691, R2753, R2754, R2755, R2757, R2758, R2766, R2769, R2770, R2775, R2778, R2806, R2807, R2808
R2829, R2840, R2853, R2864, R2873, R2899, R2900, R2912, R2916, R2937, R3003, R3043, R3061, R3065, R3074, R3101
R3114, R3116, R3117, R3119, R3120, R3163, R14687

### NEED_TRACE — 1

R19
