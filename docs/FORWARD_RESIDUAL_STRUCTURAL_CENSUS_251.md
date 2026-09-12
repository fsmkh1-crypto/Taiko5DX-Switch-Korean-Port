# FORWARD RESIDUAL STRUCTURAL CENSUS 251

Date: 2026-09-13 (KST)
Canonical parent HEAD: `f666103776c64de0958ba97d398674e970c0e9d3`
Scope: read-only structural census of the exact 251 rows left under the legacy `216 residual-other + 35 formatter` labels after the CAP64 correction.
Status: COMPLETE / STRUCTURAL ONLY / NO SWITCH WRITE AUTHORIZATION

## 1. Summary

The legacy `216 residual-other + 35 formatter` split is not a stable structural taxonomy.

All 251 rows are now partitioned into 13 exact, disjoint structural families with zero remainder:

| family | rows |
|---|---:|
| E1_TERMINATED_LOGICAL_FULL_SINGLE | 67 |
| E2_TERMINATED_LOGICAL_FULL_SHARED | 6 |
| E3_TERMINATED_LOGICAL_PREFIX | 4 |
| E4A_EMBEDDED_SINGLE_NO_RAW_OCCURRENCE | 18 |
| E4B_EMBEDDED_SINGLE_RAW_MULTI_OCCURRENCE | 8 |
| E5_EMBEDDED_MULTI_PHYSICAL | 104 |
| E6_EMPTY_LOGICAL_WINDOW | 1 |
| E7_OPAQUE_FIXED_BLOCK_3244_3250 | 7 |
| G1_AFFINE_GAP_REGION_TABLE | 7 |
| G2_AFFINE_GAP_ROLE_TABLE | 13 |
| G3_AFFINE_GAP_ITEM_TABLE | 7 |
| G4_AFFINE_GAP_UI_HEADER_COMPOSITE | 1 |
| G5_AFFINE_GAP_UTF16_MIXED_BLOCK | 8 |
| total | 251 |

Population integrity:
- intersection count: 0
- unclassified count: 0
- duplicate R-number count: 0
- ordered source-ID SHA-256: `2158d76714750ef9dd3661e9fba5ac6e14ab65d327e70dcdd567eac16c2ae80f`
- ordered R-ID SHA-256: `891bda7b16bc8b3d59725c8a03f28ce3d04b9838b41611a1f7793c7e8a8090b4`

Machine-readable membership:
- `data/post_freeze/forward_residual_structural_census_251_v1/MEMBERSHIP.json`
- SHA-256 `c84f4fde42721c698ef1227836b67fb0eaaf005ee52a4ffbf46fcbbb98f480d9`

Index:
- `data/post_freeze/forward_residual_structural_census_251_v1/INDEX.json`
- SHA-256 `7091621b3a5e5eb3028907df182036780f28fcba34e51d7ecc2bf1578b26766a`

## 2. Corrected observation: 79 -> 78

The CAP64 follow-up precheck previously observed 79 additional JP logical relations inside the 251 population.

That count is corrected to 78.

`R1690` normalizes to an empty logical string because its PC original begins with NUL. Empty-string prefix matching is not valid positive evidence. `R1690` is therefore separated into `E6_EMPTY_LOGICAL_WINDOW`.

This correction does not change the 251-row parent population.

## 3. Structural conclusions

### 3.1 Terminated logical-window families

E1/E2/E3 show that the full PC raw window is not the correct comparison unit for every row. After NUL-aware logical normalization:

- 67 rows have one exact JP physical object / one logical owner;
- 6 rows have one exact JP physical object shared by multiple logical owners;
- 4 rows are strict logical prefixes of longer JP objects.

These are structural relations only. They do not imply semantic target approval or write safety.

### 3.2 Embedded-fragment families

E4A/E4B/E5 show that many PC inline records are fragments of larger Switch JP objects:

- E4A 18: embedded in exactly one JP physical object and the full PC raw window has no Switch occurrence;
- E4B 8: embedded in one JP physical object but raw bytes occur at multiple Switch locations;
- E5 104: embedded in multiple JP physical objects.

E5 is the largest ambiguity family and cannot be resolved by containment alone.

### 3.3 Non-ordinary text/data families

- E6 isolates the empty logical window `R1690`.
- E7 isolates `R3244-R3250` as an opaque/fixed block requiring encoding or data-structure analysis rather than ordinary CP932 string matching.

### 3.4 Affine-gap table families

Residual rows in Stage-2 gaps form coherent structural table families:

- G1: region table, 7 rows
- G2: role/status/profession table, 13 rows
- G3: item-category table, 7 rows
- G4: UI-header composite, 1 row
- G5: UTF-16/mixed block, 8 rows

The neighboring Stage-2 affine deltas were tested as a shortcut for these gaps and do not satisfy the exact original-byte guard. Affine deltas must not be extended across the gap without independent proof.

## 4. Legacy formatter label

The 35 legacy `FORMATTER_CANDIDATE` rows do not form an independent top-level structural family.

They distribute across the structural partition as:

- E1: 1
- E4B: 1
- E5: 33

Therefore formatter/control behavior should be treated as a semantic/mechanism overlay on structural families, not as the primary structural axis.

## 5. Why the next scope is the full 986

The corrected raw-start partition contains 735 rows. This census contains the remaining 251 historical residual-label rows.

However, coherent table/object structures cross the historical `735 / 251` boundary. Therefore:

`735 + 251 = 986`

must be synthesized into one stable forward structural partition before deep semantic auditing continues.

This is not a reopening of:
- Stage-2 affine target mappings;
- F1 accepted 262 membership;
- frozen F1 semantic identities.

## 6. Rejected shortcuts

The following are rejected:

- `216 residual-other + 35 formatter` is a final taxonomy.
- `%` presence defines a top-level structural family.
- every residual row requires immediate consumer tracing.
- JP substring containment alone selects a semantic target.
- an empty logical string can be used as positive prefix evidence.
- adjacent Stage-2 affine deltas can be extended through uncovered gaps without exact-byte proof.
- the historical 735/251 boundary is itself a true data-structure boundary.

## 7. Next scope

Recommended next scope after a fresh execution signal:

`FORWARD_986_STABLE_STRUCTURAL_PARTITION_SYNTHESIS`

Goal:
- combine the corrected 735 raw-start population with this exact 251 census;
- preserve exact membership provenance;
- merge/split only where coherent physical/table/storage structures justify it;
- produce a stable 986-row structural taxonomy before semantic/context approval.

No repository framework change, builder/IPS/runtime work, game-file modification, or Switch write authorization is included in this report.
