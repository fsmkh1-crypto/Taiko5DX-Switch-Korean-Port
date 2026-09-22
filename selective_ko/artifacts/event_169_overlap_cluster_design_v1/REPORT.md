# EVENT 169 runtime-overlap serializer design

Date: 2026-09-22 (KST)
Status: CANONICAL DESIGN AUTHORITY / V369 / IMPLEMENTATION NOT STARTED
Parent: `756596e57353a0ed8f3538c22b4fbeac8f08a326` (V368)

This report promotes the completed local overlap analysis. It does not rerun that analysis or change V366 membership/binding, V367 runtime continuity, or V368 semantic admission. The original local report is identified by SHA-256 `4a67260d1aefbb3591010949062021c9510ddb0fe12b45d2a2264e4af9c75ccc`. This English revision preserves its findings and adopts the approved **80 final write-responsibility units**. No serializer, builder, EVENT, TAI5MSG, package, IPS, or hardware output is changed.

## Authority and evidence

The PC patch oracle gate is inherited PASS. V366 supplies exact PC v1.02 EVENT bindings and composite recipes; V337 supplies source branch ownership. V367 supplies runtime spans and continuity; V368 supplies closed semantic admission. Exact identities and source-ledger line numbers remain in `PROVENANCE.json` and `NODES.jsonl`.

V366 archive: 2,211,822 bytes, SHA-256 `430ab6394ade066c5314ac734819d68cd9f24554da2a5346bc23031019712b1c`. Its direct ledger is 34,971,518 bytes, SHA-256 `6e7ca36d05a1a79e4e0918645f27a72b05c05505f66ac33a683e745b03da3d60`. The completed analysis connected actual embedded PC EVENT bytes to the 169-file manifest without executing the patcher. Large source inputs are not copied here.

The original local analysis used the V367 local checkout plus pinned V368 remote references. Its verified graph came from frozen V366 bindings and the already validated runtime helper, not fresh PC grouping. V368's closed Korean-bearing subset selected the graph. V369 reuses those verified outputs byte-for-byte except the report, canonical index/validation metadata, and responsibility-unit status wording. No new semantic admission or graph discovery occurs during promotion.

## Frozen accounting

| Measure | Count |
|---|---:|
| Product-relevant INCLUDE_KO outer owners | 91 |
| Relations, direct/composite inner split | 130; 108 / 22 |
| Unique nodes, direct/composite split | 210; 188 / 22 |
| Unique inner nodes; outer/inner intersection | 123; 4 |
| Connected runtime-overlap clusters | 87 |
| Direct-only / composite-involved clusters | 65 / 22 |
| EVENT files | 33 |
| Same-partition / cross-partition clusters | 87 / 0 |
| Maximum actual containment depth | 2 edges / 3 owner layers |
| Atomic payload components / independent owner serialization approvals | 87 / 0 |
| Unclassified design models | 0 |
| Final write-responsibility units | 80 |
| Direct-only / composite-involved units | 60 / 20 |

`91 + 123 - 4 = 210`. The **87 components are not 87 independent serializer transactions**. Shared relocation joins seven component pairs into the 80 final responsibility units in `TRANSACTION_DOMAINS.jsonl`. These are design commitments, not implementation or hardware PASS claims.

| Shape | Clusters | Nodes per cluster | Relations per cluster | Containment depth |
|---|---:|---:|---:|---:|
| Direct pair | 47 | 2 | 1 | 1 |
| Direct outer plus composite inner | 22 | 2 | 1 | 1 |
| Outer plus two inners | 12 | 3 | 2 | 1 |
| Partially overlapping roots sharing inners | 3 | 5 | 6 | 1 |
| Three-layer containment | 1 | 3 | 3 | 2 |
| Outer plus eight inners | 2 | 9 | 8 | 1 |
| Total | 87 | 210 total | 130 total | |

## Graph and conflict types

A node key is `(EVENT filename, exact source owner offset)`. A directed relation places the inner start strictly inside the outer runtime span. This permits partial overlap; complete containment and containment depth are separately recorded. Ranges are half-open. Composite PC ranges are containing windows, not final command ownership or relocated output coordinates.

There are 88 shared-end suffix relations, 39 other strict containments, and 3 partial overlaps. Overlapping siblings sharing an immediate containing parent: 0. Composite outer to direct inner: 0; composite to composite: 0. Intercluster source-union and PC runtime/window-union collisions: 0. Identical full target ranges: 0. All 130 relations would permit overlapping writes if both complete owners were emitted independently; this is a design hazard, not an observed product write count.

| Cluster | File / partition | Root pair | Source overlap | PC overlap |
|---|---|---|---|---|
| C17 | ECF00000 / 187 | 507D0 / 507D8 | [507D8,50828) | [65048,650C4) |
| C19 | ECF00000 / 188 | 50C94 / 50C9C | [50C9C,50CEC) | [65668,656E4) |
| C21 | ECF00000 / 189 | 51158 / 51160 | [51160,511B0) | [65C88,65D04) |

These unions extend beyond the first root's end. The first root is not a container for the entire union. The actual three-layer containment is C59, `EFF1FA00 p78: 20A34 -> 20A48 -> 20A50`. A path through partial relations is not actual containment depth.

## Overlay and structural intersections

Exact owner intersections with existing direct-particle, derived, lexical, and suffix-three applicability are all 0. Fixed-particle intersections are 17 owners in 17 clusters. Composite intersections are 22 owners in 22 clusters. All 5 leading-control recovery owners are included. Existing 5A runtime ranges, 1E/3C grouped ranges, and the three known ECF special spans each have 0 intersections. Those zero counts do not prove the absence of additional special behavior across all 169 EVENT files.

Generic relocation spans intersect 65 clusters through 136 unique plans and 148 dependencies. There are 39 internal generic `04` fields, covered by 43 INCLUDE runtime views. Four fields have two covering views (C17/C19/C21/C59). C29/C65 also contain frozen `1D / 21` structural items. Other nonmember grouped fragments remain preserved without declaring every first byte a runtime control opcode.

Existing overlay wrappers replace whole source grouped items. Of 91 outer owners, 90 have different grouped-item and runtime lengths. C66's outer has equal lengths, but its runtime-only inner `EKF00800:F60` is inside that item and cannot be found by the wrapper's grouped lookup. Existing wrappers are therefore not independently approved runtime-owner writers.

## Composite and C31 ordering

All 22 graph composites are direct-outer to composite-inner relations. Each PC containing window's first four bytes differ from the corresponding Switch header. Preserve source structural ownership and the V366 recipe; do not copy the PC window as a complete Switch owner.

The nine composites outside this graph remain authoritative: `ECF00000:7F428,96E40`; `EFF06E00:60C0,63DC,669C,69B8`; `EFF07700:CE44`; `EFF21800:1AD8`; `EPF32000:E44`.

**C31 ordering is mandatory: canonical composite reconstruction first, then the approved particle transform.** `ECF00000:C22BC` is the unique composite/fixed-particle intersection. The previous fixed-particle PC window at `F20F0` has 48 bytes; the V366 reconstructed owner has 52 bytes, including the Switch header and restored leading literal `5C`. Bind the two approved particle occurrences to the reconstructed surface. Do not reuse the old fixed-particle result hash as the final composite hash or invent a new recipe.

## Shared relocation and final responsibility

| Joined clusters | EVENT | Shared branch owner offsets |
|---|---|---|
| C04 + C05 | ECF00000 | CCB0 |
| C06 + C07 | ECF00000 | F4E0, F424 |
| C17 + C18 | ECF00000 | 50758, 507EC |
| C19 + C20 | ECF00000 | 50C1C, 50CB0 |
| C21 + C22 | ECF00000 | 510E0, 51174 |
| C33 + C34 | ECF00000 | D6BC4, D7310 |
| C45 + C46 | EFF0C300 | 93B0 |

Seven pairs share 12 fields: `87 - 7 = 80`. Joining responsibility does not authorize overwriting unrelated gaps. Preserve disjoint payload regions while solving shared field layout dependencies together. The file offset table still needs a final file-layout owner.

## Preservation boundaries

The five connected NON_KOREAN_TARGET owners stay outside the 210-node INCLUDE graph and remain in `SUPPORT_OWNERS.jsonl`: internal `EFF2D200:5CE8`, `EKF00800:1764`, `EP111700:1358`; preceding partial-header boundaries `EFF07700:5FE8`, `EFF20600:7914`. Preserve unrelated payload bytes and separately constrain approved structural relocation edits. The graph also retains duplicate-KO override `EP111700:1364 -> 1794`.

All 2,327 observed mapped Korean code pairs in the 91 outer target views lie inside inner target/window ranges; outer-exclusive observations are 0. These are occurrence observations, not unique glyphs or new admissions. They support one-time inner payload materialization while preserving outer runtime views, but do not authorize dropping ASCII, escapes, headers, control, padding, or terminators.

## Design contract and remaining gates

Resolve frozen source anchors, assign disjoint writers, materialize direct payloads or canonical composite recipes, apply approved occurrence transforms once, connect runtime views and anchors, calculate each shared relocation field once from final layout, emit each payload region once within its final responsibility unit, then calculate partition/file offsets and validate.

| Responsibility | Authority |
|---|---|
| Semantic payload | V366 direct binding or canonical composite recipe |
| Structural header | Exact Switch source owner |
| Runtime span | Each runtime view; no independent payload writer |
| Branch/control | Frozen source control owner |
| Relocation | One writer per field within T01-T80 |
| Final emission | Coordinated by T01-T80, then final file-layout ownership |

C17/C19/C21 require interval-union handling, C66 requires a runtime-only inner anchor, and C31 requires recipe-before-particle ordering. Implementation-facing modules affected are `selective_event.py`, `selective_event_particle.py`, existing whole-item overlay wrappers, and the 5A structure-repair path. Candidate-time repair calculations and final field commits must have distinct responsibilities.

Future implementation gates: unchanged 66,987 source owners and 66,956/31 binding split; direct target uniqueness and recipe/override identity; exact 91 outer/130 relations and overlap types; one writer per output byte/relocation field; runtime event_len continuity; partition containment; branch/control ownership; all 80 responsibility units; deterministic rebuild; zero unrelated payload mutation; exact composite 31, leading-control 5, fixed-particle 17 and NON_KOREAN boundary 5 preservation. No final-output gate or hardware test is claimed here. Additional future payload changes may require additional dependency joins.

Rejected approaches remain rejected: independent full-owner patches, treating all relations as containment, treating 87 clusters as relocation-independent transactions, bulk PC outer copying, assuming all overlay intersections are zero, grouped lookup for every runtime owner, treating the old C22BC result as the final composite, conflating PC windows with relocated runtime spans, raw 89/128 counts, semantic fallback, fresh target grouping as source authority, and the rejected event_len mismatch hypothesis and its historical counts.

Historical input-access failures (restricted Python download and opening the entire patcher EXE as ZIP) did not supply authority. Verified cached archives and the manifest-sized embedded ZIP supplied the completed analysis. V369 does not repeat those analyses.

Canonicalization ends here. Serializer implementation requires a fresh explicit user instruction.
