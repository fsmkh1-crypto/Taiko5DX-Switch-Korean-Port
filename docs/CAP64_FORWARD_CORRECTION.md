# CAP64 FORWARD CORRECTION

Date: 2026-09-13
Status: CANONICAL CORRECTION / NO SWITCH WRITE AUTHORIZATION

## 1. Root cause

Stage-1 raw Switch occurrence discovery used `find_pattern_occurrences(..., cap=64)`.
The resulting `switch_raw_candidate_count_capped_64` and `switch_raw_candidates` fields are censored when the stored count is 64. Later forward-family work incorrectly consumed some capped absences/cardinalities as complete structural evidence.

Canonical rule from this correction:

- stored count `< 64`: the stored list may be used as the complete Stage-1 raw occurrence list;
- stored count `== 64`: interpret as `actual count >= 64`, not exact count 64;
- a capped list must not prove absence, uniqueness, complete language-domain ownership, or complete storage-mutability ownership.

## 2. Impact census

Across all 17,103 inline rows:

- rows hitting the cap: 386;
- distinct capped raw patterns: 131;
- rows whose actual occurrence count is greater than 64: 377;
- rows whose complete storage-mutability set expands beyond the capped view: 211;
- rows whose complete language-domain evidence changes beyond the capped view: 106.

The Stage-2 affine target mapping itself is unaffected. F1 target membership is also unaffected because the F1 procedure compares the complete 3,803-entry JP logical table directly rather than relying on the capped Stage-1 raw-candidate list.

## 3. Forward-population correction

Forward population remains 986 (`Stage-2 residual 1,248 - F1 accepted 262`).

The old current-state census:

- raw-start localization relation: 700;
- legacy unclassified label: 251;
- legacy formatter label: 35.

After uncapped correction of this root cause:

- raw-start localization relation: 735;
- legacy residual-other label: 216;
- legacy formatter label: 35.

The 216 and 35 labels are not final structural families. They form one 251-row next-scope census population.

Thirty-five forward rows move from the legacy unclassified label into the raw-start localization relation:

- L1 additions: R390, R685, R2256, R2349, R2929, R16454;
- L2 additions: R2433, R2488;
- L3 additions: R80, R82, R1035, R1088, R1155, R1163, R1168, R1171, R1191, R1452, R1454, R1456, R1458, R1460, R1526, R1528, R1695, R1697, R1699, R1715, R1717, R1719, R1819, R1995, R2054, R2853, R16461.

R1291 moves from old L4 into corrected L3. Its old L4 classification was produced by capped JP-start absence and is retracted.

Corrected raw-start partition:

- L1 = 454;
- L2 = 165;
- L3 = 116;
- L4 = 0;
- total = 735.

The exact corrected memberships are materialized in `data/post_freeze/forward_localization_raw_start_partition_v2/`.

## 4. Prior-artifact status

`data/post_freeze/forward_localization_family_partition_v1/` remains historical provenance. Its exact 700-row memberships are not deleted, but its claim of complete/current forward-localization coverage is superseded.

`data/post_freeze/l3_semantic_pc_mechanism_v1/` remains valid as a semantic/mechanism review of its original 88-row parent population only. It is not a complete review of corrected L3=116. R2300 has a legitimate re-review trigger because its uncapped JP-prefix candidate set expanded.

No existing L1 semantic overlay is extended automatically to the six new L1 rows.

## 5. Additional census trigger

A read-only precheck of the remaining 251 legacy residual labels found 79 rows with additional JP logical relations after logical-window normalization, all involving PC originals with NUL + zero padding. This observation is a next-scope trigger only: its exact membership is not materialized by this correction and it is not a final family claim.

Therefore the next analysis must census all 251 rows jointly before further semantic auditing.

## 6. Safety consequences

Rejected shortcuts:

- `count == 64` means exactly 64 candidates;
- no JP start in a capped list proves no JP start exists;
- the old 700/251/35 split is complete/current;
- the old L4=1 is a valid current family;
- 216 and 35 are already final structural families.

This correction does not authorize builder, IPS, runtime, game-file modification, or Switch writes.
