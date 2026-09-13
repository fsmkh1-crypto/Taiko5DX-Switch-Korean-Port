# Inline Full-Corpus Action-Collapse Overlay

Date: 2026-09-13 (KST)  
Status: CANONICAL POST-FREEZE READ-ONLY ACTION-COLLAPSE OVERLAY / NO SWITCH WRITE AUTHORIZATION  
Basis HEAD: `9b85bde1e0d6952611f2dc69d9459683529e7844`

## 요약

This overlay records the action-collapse results proven after semantic-owner closure and before F1/Stage2 cross-boundary population.

It deliberately separates two provenance strengths:

1. **gap-internal count-level closure**: `1,035 source rows -> 1,011 owner-action units`, reduction `24`; exact 24 internal edge memberships were not materialized in the analysis artifact and are therefore not promoted here as exact row-level edges.
2. **gap <-> forward exact cross-boundary adjudication**: 37 exact review units were materialized; 35 direct composite units and one formatter unit are confirmed merges, one region unit is a confirmed reroute relation, and false-positive count is zero.

No new `WRITE_SAFE` authorization is created.

## 1. 확정된 사실

### 가. Gap-internal action-collapse count is closed at count level

The exact gap source population remains `1,035` and remains owner-bound `1,035 / 1,035`.

Read-only action-collapse analysis established:

```text
gap source rows                 1,035
gap owner-action units          1,011
internal action reduction          24
```

The reduction consists of 24 internal 2:1 collapse relations. This is a count-level verified result only in this overlay because the exact 24 edge memberships were not preserved as a machine-readable list during the analysis pass.

Therefore:

- the count `1,011` is retained as verified planning state;
- it is **not** yet sufficient to instantiate all final source/action edges;
- no missing exact edge is guessed or reconstructed during this materialization scope.

### 나. Exact gap <-> forward review population is 37 units

The cross-boundary candidate pass reduced the gap/forward boundary to exactly:

- 35 same-object strong-core review units;
- 1 T4 formatter-family unit;
- 1 T1 broad-region reroute unit;
- total 37 units.

No candidate outside those 37 units is promoted by this overlay.

### 다. All 35 strong-core units are confirmed composite N:1 relations

The 35 exact groups are materialized in the accompanying `MEMBERSHIP.json`.

Composition:

- 34 groups are 2 source -> 1 action;
- 1 group (`R1264 + R1265 + R1266`) is 3 source -> 1 action.

Accounting:

```text
source rows       71
action units      35
action reduction  36
false positives    0
```

These relations are closed on the action-cardinality axis only. They do not imply write safety.

### 라. T4 source-complete formatter family is one action unit

The T4 source-complete block is `R16447-R16457`, 11 source rows total.

- gap contribution: `R16450`
- forward contribution: the other 10 rows
- final relation on this axis: `CONFIRMED_FORMATTER_N1`

Accounting:

```text
source rows       11
action units       1
action reduction  10
```

### 마. Direct gap <-> forward merge total is 82 source -> 36 action

Combining the 35 strong-core units and T4 formatter unit:

```text
source rows       82
action units      36
direct reduction  46
```

This `46` reduction is exact for the adjudicated direct-merge population.

### 바. T1 broad-region unit is rerouted, not collapsed into one physical action

The broad-region source block is `R14542-R14550`, nine source rows.

- gap rows: `R14543`, `R14549`
- forward rows: the other seven

Verdict:

`CONFIRMED_REROUTE_TO_EXPANDED_REGION_OWNER_FAMILY`

The nine broad-region source obligations are not represented as one independent physical action. Their final action ownership belongs to the detailed 19-entry expanded region owner family already established by the Oracle evidence.

Therefore the T1 review unit is **not** included in the direct `82 -> 36` reduction. Final action IDs/cardinality for the region family remain deferred until the Stage2 detailed-region owners are combined.

## 2. 유력한 가설

None is required for the 36 confirmed direct-merge units or the region reroute classification.

The remaining uncertainty belongs to later cross-boundary graph completion, primarily F1 and then Stage2.

## 3. 미확정 사항

This overlay does not establish:

- exact row-level membership of the 24 gap-internal 2:1 collapses;
- final gap+forward total action cardinality across every owner family;
- gap+forward <-> F1 cross-boundary relations;
- gap+forward+F1 <-> Stage2 cross-boundary relations;
- final region 28-source -> 19-owner action IDs;
- final full-inline `17,103 source -> N actions` cardinality;
- write-safety expansion;
- portability P1/P2/P3/P4 totals;
- builder/runtime implementation.

## 4. 기각된 가설

The following are rejected:

1. `1,035 gap sources = 1,035 actions`.
2. The 35 strong-core cross-boundary units contain false positives.
3. T4 requires 11 independent Switch actions.
4. The nine broad-region sources should collapse into one physical Switch action.
5. Same text alone is sufficient for action collapse.
6. Action-collapse closure implies `WRITE_SAFE`.
7. F1 or Stage2 must be reopened or semantically revalidated to preserve these results.
8. Missing exact gap-internal edge membership may be guessed during materialization.

## 5. 관련 영향 범위

Unchanged:

- FZ001 frozen identities/hashes;
- Stage2 membership;
- F1 historical partition and 158 static-write-authorized boundary;
- forward-986 membership and routing closure;
- gap semantic-owner closure `1,035 / 1,035`;
- Oracle / Assisted / Astra / TRACE provenance;
- builder/runtime/game files.

New Switch write authorization from this overlay: **0**.

## 6. 수정 제안

No implementation modification is authorized here.

Next recommended read-only scope:

`GAP_FORWARD_TO_F1_CROSS_BOUNDARY_CANDIDATE_GENERATION_READ_ONLY`

That scope should only generate the exact F1 boundary candidate list and STOP. Candidate adjudication must be a later separately authorized scope. Stage2 remains deferred until the F1 boundary is closed.
