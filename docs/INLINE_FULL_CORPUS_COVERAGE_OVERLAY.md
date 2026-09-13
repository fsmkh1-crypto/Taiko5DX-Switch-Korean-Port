# INLINE FULL-CORPUS COVERAGE OVERLAY

Date: 2026-09-13 (KST)  
Status: CANONICAL POST-FREEZE READ-ONLY COVERAGE OVERLAY / NO SWITCH WRITE AUTHORIZATION  
Basis HEAD: `fabac86f8f4c442b8436f8f2feee99e1819c572f`  
Scope: `INLINE_FULL_CORPUS_COVERAGE_OVERLAY_MATERIALIZATION`

## 요약

This overlay closes a coverage-accounting gap discovered while populating the Portability Matrix / Action Ledger.

It does not invalidate Stage 1, Stage 2, F1, the stable forward-986 partition, Oracle/Assisted/Astra/TRACE closure, FZ001, or the existing 158 F1 static-write authorizations.

The canonical F1 selector was deterministically replayed only to recover its already-verified full `accepted mapped = 1,311` membership. No F1 semantic rule was changed or re-adjudicated.

The complete inline population now partitions exactly as:

| Coverage class | Rows |
|---|---:|
| Stage-2 affine verified | 13,771 |
| F1 accepted mapped | 1,311 |
| forward-986 | 986 |
| unique-only coverage gap | 1,035 |
| **Total** | **17,103** |

The four sets are pairwise disjoint and their union is the complete 17,103 inline source population.

The 1,035-row gap is not a translation-failure population. It is the remainder of Stage-1 unique raw candidates that were outside Stage-2 affine coverage and outside the accepted F1 sequence family. Stage-1 and the Master Rule Registry already prohibit promoting raw uniqueness alone to target identity or a port action.

Machine-readable exact membership:
- `data/post_freeze/inline_full_corpus_coverage_overlay_v1/MEMBERSHIP.json`
- semantic SHA-256 `12cf73cc0962b18ac629922a095d9148fb194352e0e48df667a1073f4de8c367`

## 1. 확정된 사실

### 가. F1 full accepted membership is 1,311

Deterministic replay of the existing canonical selector reproduced all canonical counts without semantic re-adjudication:

```text
search segments             142
trimmed mapped rows       1,402
accepted segments           112
accepted mapped rows      1,311
accepted Stage-2 residual   262
F1 rule rejected             16
```

The exact 1,311-row membership is materialized in the overlay artifact. This replay is provenance recovery, not revalidation of the already-verified F1 rule.

### 나. Exact coverage gap is 1,035

Stage 1 recorded 6,053 inline rows with exactly one stored raw Switch candidate. Of those:

```text
covered by Stage 2 affine structure     3,969
covered by accepted F1 sequence         1,049
remaining exact unique-only gap         1,035
                                      -------
Stage-1 unique-only population          6,053
```

The exact 1,035 rows are now materialized.

Split:

```text
R1-R3250 early gap      1,009
later gap                  26
TOTAL                   1,035
```

### 다. Early 1,009 structural census

The early gap is not one homogeneous action class.

| Structural shape | Rows |
|---|---:|
| JP logical full object / single owner | 622 |
| JP logical full object / shared owner | 31 |
| JP logical prefix / single owner | 224 |
| JP logical prefix / shared owner | 1 |
| formatter interior fragment | 45 |
| other longer-object interior fragment | 85 |
| independent raw object start | 1 |
| **Total** | **1,009** |

These are structural observations only. They do not grant terminal disposition or write authority.

### 라. Late 26 are exception-centric family holes

Exact membership:

- T1 broad-region holes: `R14543, R14549`
- T2 role/status/profession holes: `R14684, R14685, R14686, R14688, R14691, R14692, R14698, R14701, R14705, R14707, R14708, R14709, R14713, R14714`
- T3 item-area holes: `R14719, R14725-R14732`
- T4 CP932 UI/formatter hole: `R16450`

Source-complete views relevant to later Action Ledger work are therefore:

```text
T1 broad-region PC block       R14542-R14550   9 source rows
T1 detailed-region oracle      R16428-R16446  19 source rows
region accounting total                         28 source obligations -> 19 Switch semantic owners

T2 role/status/profession      R14684-R14716  33 source rows
T3 item source block           R14717-R14736  20 source rows
T4 CP932 UI source block       R16447-R16457  11 source rows
```

This does not rewrite the stable forward structural partition. It establishes that forward-family membership was complete only for the forward-986 denominator and must not be treated as source-complete Action Ledger membership.

### 마. Promoted-target collision census has three exact pairs

Cross-checking the 1,035 unique-only candidate targets against already promoted Stage-2/F1 targets produced exactly three same-physical-target pairs:

| Gap source | Promoted source | Logical text | Replacement relation |
|---|---|---|---|
| `R14543` | `R16430` | `北陸` | **DIFFERENT** |
| `R14549` | `R16440` | `四国` | AGREEMENT |
| `R2047` | `R15678` | `真備` | AGREEMENT |

`四国` and `真備` are N:1 agreement candidates, not replacement conflicts.

`北陸` is the only currently demonstrated same-target / same-logical-text / differing-PC-replacement collision in this coverage overlay.

The root cause of the `北陸` difference is **not yet established**. A semantic-role/consumer distinction is a plausible hypothesis only. No translation is selected or discarded by this document.

## 2. 유력한 가설

The principal workflow cause is `EXCEPTION_CENTRIC_SCOPE_GAP`.

After Stage 1, later work progressively used Stage-1 exception, Stage-2 residual, F1 residual, and forward-986 denominators. Rows that were unique raw candidates at Stage 1 therefore did not automatically re-enter later source-family promotion work unless another family such as F1 independently covered them.

This explains why 1,035 rows remained outside the effective full-corpus planning population even though no existing canonical stage was itself incorrect.

For the early 1,009, most rows are likely reusable through the already-established logical-object/composite/shared-owner rules, but they must be promoted under full-corpus evidence rather than by raw uniqueness.

For `北陸`, different PC semantic roles/consumers are a plausible cause of the differing replacements, but this remains unverified until PC occurrence context and Switch owner/consumer binding are compared.

## 3. 미확정 사항

This overlay does not establish:

- final terminal disposition for the 1,035 rows;
- final source-to-action collapse cardinality;
- write authority for any newly covered row;
- whether the early 878 logical-object-shaped rows become P1/P3 or another disposition;
- final shared-owner agreement for the 31 early shared-owner rows;
- final reconstruction grouping for the 130 formatter/longer-object fragments;
- final action-family grouping for T2/T3/T4 source-complete blocks;
- the semantic-role/consumer cause of the `北陸` collision;
- the final resolution of the `北陸` collision;
- any new builder/runtime/IPS/game-file action.

## 4. 기각된 가설

The following are rejected:

1. Stage-1 raw uniqueness is equivalent to verified target identity.
2. The forward-986 structural partition is a source-complete partition of all 17,103 inline rows.
3. F1 covered only its 262 residual rows; its verified accepted mapped population is 1,311.
4. The 1,035 gap consists only of independent raw strings.
5. Late 26 rows form unrelated new families; they are holes inside source-complete T1/T2/T3/T4 regions.
6. Every same-target collision is a replacement conflict; two of the three exact collisions have replacement agreement.
7. The `北陸` collision may be solved by arbitrarily choosing one PC replacement.
8. Astra is required for the current coverage-accounting problem.

## 5. 관련 영향 범위

Unchanged and preserved:

- Stage-1 canonical inventory;
- Stage-2 affine 13,771 membership and target evidence;
- F1 accepted sequence evidence;
- F1 158 static-write authorization;
- FZ001 frozen semantic identities;
- stable forward-986 membership;
- Oracle/Assisted/Astra/TRACE provenance and routing closure;
- builder/runtime/IPS/game files;
- INV-1 through INV-11.

New planning consequence:

The effective inline planning denominator must be source-complete. The Action Ledger must not use the forward-986 family partition as though it were the full 17,103 source-family partition.

## 6. 수정 제안

No implementation modification is authorized by this overlay.

Next recommended read-only scope:

`INLINE_FULL_CORPUS_SEMANTIC_OWNER_ACTION_POPULATION_READ_ONLY`

Recommended order:

1. consume the exact full-corpus coverage partition from this overlay;
2. bind semantic owners for the 1,035 gap using existing PC Oracle and structural rules;
3. analyze each cause family corpus-wide, not row-by-row patches;
4. resolve the `北陸` semantic-role/consumer question as its own owner-binding cause group;
5. construct proposed source/action relations and final action families;
6. keep portability and write authority independent;
7. use Astra only if deterministic evidence is genuinely exhausted.

No builder/runtime/IPS/game-file implementation is part of that scope.
