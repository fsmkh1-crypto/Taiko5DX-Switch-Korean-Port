# PC Patch Oracle Astra 10 Follow-up — read-only semantic/context adjudication

Date: 2026-09-13 (KST)  
Status: CANONICAL READ-ONLY FOLLOW-UP / NO SWITCH WRITE AUTHORIZATION  
Parent HEAD: `16729c4a1fc5afd9c01f6cf9ef52ab7f6e0469d5`

## 요약

The canonical `ASTRA_REQUIRED` queue of 10 rows was adjudicated without repository, framework, builder, IPS, runtime, or game-file modification.

Result:

| Disposition | Count | Exact membership |
|---|---:|---|
| `TARGET_RESOLVED` | 0 | none |
| `COMPOSITE_OR_FORMATTER_RESOLVED` | 8 | `R75, R651, R1062, R1277, R1583, R1591, R1631, R2572` |
| `NEED_TRACE` | 2 | `R1283, R1284` |
| other dispositions | 0 | none |
| **Total** | **10** | exact / disjoint / complete |

`ASTRA_REQUIRED` remainder is now `0`.

The two remaining rows are not unresolved translation judgments. `R1283` and `R1284` both patch `発生条件` with different replacements and require occurrence-owner/consumer binding.

Effective forward routing after this overlay:

```text
BASE_ORACLE_RESOLVED                         656
BASE_ORACLE_REROUTED                           7
ASSISTED_FOLLOWUP_TARGET_RESOLVED             65
ASSISTED_FOLLOWUP_COMPOSITE_RESOLVED         231
ASTRA_FOLLOWUP_COMPOSITE_RESOLVED              8
TRACE_REQUIRED                                19
                                             ---
TOTAL                                        986
ASTRA_REQUIRED_REMAINDER                       0
ORACLE_ASSISTED_REMAINDER                      0
```

Consolidated current counterpart classes:
- target resolved: 65
- composite/formatter resolved: 239
- rerouted: 7
- base oracle resolved: 656
- trace: 19

Counterpart resolution still does not imply `WRITE_SAFE`.

## 1. 확정된 사실

### 가. Exact 10-row partition

`COMPOSITE_OR_FORMATTER_RESOLVED`:
`R75, R651, R1062, R1277, R1583, R1591, R1631, R2572`

`NEED_TRACE`:
`R1283, R1284`

No row remains in `ASTRA_REQUIRED`.

### 나. Row-level semantic/context evidence

| R | PC source | Actual PC replacement | Switch counterpart / candidate | Disposition | Basis |
|---|---|---|---|---|---|
| R75 | `上昇` | `상승` | JP 1146 `%s%d上昇` | COMPOSITE | PC sequence `が上昇 → 上昇 → 千石上昇 → 人増加` aligns with Switch formatter sequence; current row is the formatter tail. |
| R651 | `いくら投資しますか？\n(1` | `얼마를 투자합니까?\n(100` | JP 1814 `いくら投資しますか？\n(1000～%d)` | COMPOSITE | R651 and R652 windows fit the same full object at preserved relative positions; nearby investment/interference context agrees. |
| R1062 | `ＯＲ調査` | `OR조사(` plus the leading byte of the following incomplete glyph | JP 2261 `}:ＯＲ調査（結果 %d）` | COMPOSITE | R1062/R1063 windows map inside the result formatter and distinguish it from the open/skip objects. |
| R1277 | `スクリプト` | `스크립트` + NUL×2 | JP 2790 `} //スクリプト` | COMPOSITE | R1276 owns the opening object; R1277 belongs to the closing suffix, followed by the chapter-freeze block. |
| R1283 | `発生条件` | `발생조건` | JP 2795 `発生条件:{` / JP 2796 `}//発生条件` | NEED_TRACE | Opening-side binding is likely, but both candidate objects contain the source window and current bytes do not prove owner assignment. |
| R1284 | `発生条件` | `발생식` + NUL×2 | same two candidates | NEED_TRACE | Closing-side binding is likely, but occurrence order and NUL replacement alone are insufficient to prove owner assignment. |
| R1583 | `ターン` | `턴` + NUL×4 | JP 3137 `%uターン` | COMPOSITE | Remaining-days/list-selection neighborhood disambiguates this formatter from other `ターン` occurrences. |
| R1591 | `ターン` | `턴` + NUL×4 | JP 3145 `%s:%uターン` | COMPOSITE | Collapse/full-preparation/type-display neighborhood identifies a distinct formatter. |
| R1631 | `ターン` | `턴` + NUL×4 | JP 3192 `%dターン` | COMPOSITE | Combat-power/training-unit/retreat neighborhood identifies the owner formatter. |
| R2572 | `国` | `국` | JP 337 `%s国` | COMPOSITE | `石山町衆 → %s国 → %sのくに` and subsequent military/plot context align; the row is a name suffix. |

### 다. Historical semantic holdouts refined

The historical unresolved set `R651, R1062, R1277, R1283, R1284` remains provenance only.

Current status after this follow-up:
- resolved composite: `R651, R1062, R1277`
- owner/consumer trace: `R1283, R1284`

`R2572`, previously a semantic holdout, is also closed as the `%s国` suffix rather than the unrelated standalone `国` occurrence.

## 2. 유력한 가설

- `R1283` most likely belongs to the opening `発生条件:{` object.
- `R1284` most likely belongs to the closing `}//発生条件` object.

These are not promoted to resolved because the recorded PC source windows do not contain the opening/closing syntax needed to prove occurrence ownership.

## 3. 미확정 사항

- Exact owner/consumer binding for `R1283` and `R1284`.
- Replacement payload construction on Switch.
- Storage capacity, terminator behavior, formatter argument preservation, shared-owner effects, and runtime write safety.
- Exact PC target-build preimage/XREF ownership remains unavailable.

The R651/R652 and R1062/R1063 patch windows contain one-byte gaps not represented by the recorded patch originals. The full-object projections are internally consistent, but they are not claimed as exact PC EXE preimages.

## 4. 기각된 가설

The following shortcuts are rejected:

- infer R651 minimum investment from the visible replacement ending `(100`;
- map R1062 to the OR-investigation open/skip objects;
- map R1277 to the opening `スクリプト:{` object;
- merge all three `ターン` rows because their Korean replacements are equal;
- map R2572 to the unrelated standalone `国` occurrence;
- bind R1283/R1284 solely from occurrence order or NUL padding;
- treat semantic counterpart resolution as `WRITE_SAFE`.

## 5. 관련 영향 범위

This overlay changes only the effective disposition of the canonical ten-row Astra queue.

Unchanged:
- FZ001;
- F1 accepted 262 and F1 actions;
- Stage-2 mappings;
- stable forward 986 structural membership;
- Oracle V1 provenance;
- assisted-297 follow-up membership;
- framework;
- builder/IPS/runtime/game files;
- Switch write authorization.

## 6. 수정 제안

No implementation change is authorized.

Next recommended read-only scope is the exact 19-row trace queue:

`R19, R1283, R1284, R1690, R3244-R3250, R16458-R16465`

Analyze that queue as structural/encoding/owner problems, not as another semantic batch.

Repository writes for this materialization use only:
`create_blob → create_tree → create_commit → update_ref(force=false)`.
