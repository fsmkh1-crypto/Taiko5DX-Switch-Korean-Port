# Inline Pre-Stage2 <-> Stage2 Cross-Boundary Adjudication Closure

Date: 2026-09-13 (KST)  
Status: CANONICAL POST-FREEZE READ-ONLY PRE-STAGE2/ STAGE2 CROSS-BOUNDARY ADJUDICATION CLOSURE / NO SWITCH WRITE AUTHORIZATION  
Basis HEAD: `d865d85579f7ff2f1bd409aa3908aade5086e812`

## 요약

The bounded candidate-generation pass produced exactly three strong pre-Stage2 <-> Stage2 review units. This closure adjudicates those three units only. It does not reopen Stage2 affine targeting, F1, forward-986 routing, gap semantic-owner closure, gap/forward action-collapse, or F1 cross-boundary action-collapse.

Final adjudication result:

- candidate review units: 3
- candidate pre-Stage2 source rows: 11
- candidate Stage2 source rows: 21
- total candidate source rows: 32
- confirmed units: 2
- rejected false-positive units: 1
- unresolved units: 0
- conflict units: 0
- new Switch write authorization: 0

The two confirmed units are `S2X-C01` (`R2047` -> Stage2 `R15678`) and `S2X-C03` (the nine broad-region obligations -> the canonical Stage2 expanded-region owner family). `S2X-C02` (`R2553 館` <-> `R3283 角館`) is rejected because the canonical owner of `R2553` is the `%s館` place-suffix formatter, not the `角館` place-name fixed field.

This closure proves only owner/action relation on these exact boundary units. It does not calculate Stage2-internal action collapse or final full-inline action cardinality.

## 1. 확정된 사실

### 가. Exact adjudication queue is three units

| Unit | Pre-Stage2 side | Stage2 side | Verdict |
|---|---|---|---|
| `S2X-C01` | `R2047 真備` | `R15678 真備` | `CONFIRMED_N1_TO_STAGE2_OWNER` |
| `S2X-C02` | `R2553 館` | `R3283 角館` | `REJECTED_FALSE_POSITIVE` |
| `S2X-C03` | `R14542-R14550` broad-region family | `R16428-R16446` expanded-region family | `CONFIRMED_EXPANDED_REGION_OWNER_REROUTE` |

No fourth candidate is added during adjudication. Same Japanese text, prefix, substring, replacement equality, or incidental containment alone remain insufficient evidence.

### 나. S2X-C01 closes as an N:1 relation to the Stage2 owner

`R2047 真備` and `R15678 真備` already had:

- the same physical Switch target/window in the canonical coverage collision census;
- agreeing PC Korean replacement bytes;
- a canonical semantic-owner conclusion that `R2047` is an N:1 agreement relation with its promoted owner.

The promoted owner is the Stage2 source `R15678`. Therefore `R2047` does not require a second independent Switch action.

The formal terminal `SUBSUMED` disposition is not instantiated here because the final Action Ledger action ID does not yet exist. When final action IDs are materialized, the source must link directly to the final non-`SUBSUMED` action under the canonical Action Ledger contract.

### 다. S2X-C02 is a false positive caused by raw containment

`R2553 館` already has a canonical Switch counterpart in the place-suffix formatter family:

- PC source: `R2553 館`
- Switch semantic owner: `%s館`

This relation is structurally established together with the full `R2552-R2563` suffix/formatter family.

`R3283 角館` is a complete place-name fixed-field object. The fact that the final character of `角館` is `館` does not make the place-name field the semantic owner of the `館` suffix obligation.

Therefore the candidate-generation overlap observation does not survive owner adjudication.

Final verdict:

`S2X-C02 = REJECTED_FALSE_POSITIVE / DIFFERENT_SEMANTIC_OWNERS`

This rejection corrects only the preliminary non-canonical candidate queue. No prior canonical owner/action claim is invalidated.

### 라. S2X-C03 closes the broad-region boundary against the Stage2 expanded-region family

The nine broad-region source obligations are already canonically rerouted away from direct one-to-one legacy targets and toward the Switch expanded 19-entry region owner family. The PC Korean patch contains the corresponding detailed-region Oracle as `R16428-R16446`.

The exact broad -> Stage2 detailed-owner linkage is:

| Broad source | Broad JP | Stage2 detailed owner source(s) |
|---|---|---|
| `R14542` | `東北` | `R16428 北奥羽`, `R16429 南奥羽` |
| `R14543` | `北陸` | `R16430 北陸` |
| `R14544` | `甲信` | `R16433 甲信` |
| `R14545` | `関東` | `R16431 北関東`, `R16432 南関東` |
| `R14546` | `東海` | `R16434 駿遠三`, `R16435 濃尾勢` |
| `R14547` | `近畿` | `R16436 北近畿`, `R16437 南近畿` |
| `R14548` | `中国` | `R16438 山陰`, `R16439 山陽` |
| `R14549` | `四国` | `R16440 四国` |
| `R14550` | `九州` | `R16441 北九州`, `R16442 南九州` |

Thus the nine broad obligations are bound to 15 domestic detailed Stage2 owner sources inside the 19-entry expanded family.

`R16443-R16446` (`朝鮮 / 明国 / 琉球 / 南蛮`) remain members of the same canonical expanded Stage2 region family but have no corresponding source among the legacy nine broad obligations. They are family context, not additional broad-source links.

The earlier coverage ledger records raw replacement-byte disagreement for `R14543/R16430` and agreement for `R14549/R16440`. That raw-byte difference remains source-level provenance; it is not a competing final owner/action conflict. The canonical Oracle rule already establishes `R16428-R16446` as the porting source for the expanded Switch region table.

Final verdict:

`S2X-C03 = CONFIRMED_EXPANDED_REGION_OWNER_REROUTE`

This closure does not yet assign final Action Ledger IDs or calculate how many physical actions the Stage2 region family will require.

### 마. Exact closure state

The exact boundary closure is:

- review units: 3
- confirmed: 2
- rejected false positives: 1
- unresolved: 0
- conflict: 0

Candidate source membership remains 32 rows for provenance:

- confirmed-unit source rows: 30
- rejected-unit source rows: 2

No new `WRITE_SAFE` authorization is created.

## 2. 유력한 가설

No hypothesis remains necessary to close these three pre-Stage2 <-> Stage2 boundary units on the owner/action-relation axis.

Stage2-internal action grouping remains a separate later scope and must not be inferred from this boundary closure.

## 3. 미확정 사항

This closure does not establish:

- Stage2-internal action-collapse candidate membership;
- final Stage2 action cardinality;
- final full-inline 17,103-source action cardinality;
- final Action Ledger action IDs;
- formal `SUBSUMED_BY` edges to final actions;
- physical write sites;
- capacity/terminator/storage safety;
- shared-owner mutation safety;
- overlap/application priority;
- portability P1/P2/P3/P4;
- builder/IPS/runtime/game-file implementation.

The existing F1 static-write authorization remains 158. New Switch write authorization from this closure is 0.

## 4. 기각된 가설

The following are rejected:

1. `R2553 館` should collapse into `R3283 角館` because the character `館` is physically contained in the place name.
2. Same Japanese text alone proves a pre-Stage2 <-> Stage2 owner relation.
3. Prefix or substring containment alone creates an action-collapse relation.
4. Replacement equality alone creates owner identity.
5. The raw replacement-byte disagreement between broad and detailed `北陸` requires two competing Switch actions.
6. The legacy nine broad-region rows should each be forced into direct old-style one-to-one Switch writes.
7. Cross-boundary owner closure implies write safety.

## 5. 관련 영향 범위

Unchanged:

- FZ001 frozen identities/hashes;
- Stage1 canonical inventory;
- Stage2 affine verified membership 13,771;
- F1 accepted mapped membership 1,311;
- F1 historical authorization partition and 158 static-write-authorized boundary;
- forward-986 membership and routing closure;
- unique-only gap 1,035 and semantic-owner closure;
- gap/forward 37-unit action-collapse overlay;
- F1 cross-boundary 11-unit closure;
- Oracle / Assisted / Astra / TRACE provenance;
- builder/runtime/game files.

This closure supersedes only the preliminary three-unit Stage2-boundary candidate queue on its exact adjudicated relation axis.

New Switch write authorization: 0.

## 6. 수정 제안

No implementation modification is authorized by this materialization.

Next recommended read-only scope:

`STAGE2_INTERNAL_ACTION_COLLAPSE_CANDIDATE_GENERATION_READ_ONLY`

That scope should inspect only the already-verified Stage2 13,771 population for strong internal same-owner/action candidates, inherit all existing affine mappings without revalidation, exclude text/prefix/substring-only matches, and STOP before adjudication.

It must not expand write safety, calculate final full-corpus cardinality prematurely, or start builder/runtime/game-file work.
