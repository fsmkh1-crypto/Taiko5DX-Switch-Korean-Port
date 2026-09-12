# PC Korean Patch Oracle Resolver V1 — read-only forward 986 routing

Date: 2026-09-13 (KST)  
Status: CANONICAL READ-ONLY ANALYSIS / NO SWITCH WRITE AUTHORIZATION

## 요약

The stable forward population remains exactly 986 rows. Instead of continuing semantic review family-by-family, this pass treats the actual PC Korean patch as an oracle and asks whether the patch already supplies enough occurrence, replacement, sequence, composite, table, formatter, or encoding evidence to resolve the Switch counterpart before any expensive semantic adjudication.

The two read-only oracle passes produce:

| Routing disposition | Count | Meaning |
|---|---:|---|
| `ORACLE_RESOLVED` | 656 | deterministic PC-patch evidence resolves the counterpart/composite/template counterpart |
| `ORACLE_REROUTED` | 7 | legacy PC broad-region obligations are superseded by the expanded Switch region table |
| `ORACLE_ASSISTED` | 297 | useful oracle evidence exists, but current hard gates do not prove one counterpart |
| `ASTRA_REQUIRED` | 10 | semantic/context adjudication remains useful |
| `TRACE_REQUIRED` | 16 | encoding/control/data-consumer structure is the blocker |
| **Total** | **986** | exact, disjoint, complete |

Machine-readable membership:
- `data/post_freeze/pc_patch_oracle_resolver_v1/MEMBERSHIP.json`
- semantic SHA-256 `4fc30336e34962439f2228442ee4d5331065fbe639141b17c550720acc412822`

Machine-readable index:
- `data/post_freeze/pc_patch_oracle_resolver_v1/INDEX.json`
- semantic SHA-256 `076aeaaf3fb5db065d5ec6d68961324b02669fee4863d67405b9d70be65cb7c3`

This artifact resolves target/counterpart routing only. `TARGET_RESOLVED` still does not imply `WRITE_SAFE`.

## 1. 확정된 사실

### 가. PC Korean patch must be used as an oracle before semantic escalation

The effective evidence order for the forward population is now:

1. actual PC occurrence and replacement;
2. exact/same-delta sequence correspondence;
3. full-object reverse lookup across all 17,103 PC inline records;
4. composite reconstruction from adjacent PC patch records;
5. table/template and cross-encoding correspondence;
6. semantic adjudication only when deterministic evidence stops;
7. consumer tracing only when the blocker is structural/encoding/consumer ownership.

The stable structural family remains routing metadata. It is not the end goal.

### 나. First deterministic oracle pass resolved 540 rows

The disjoint first-pass rule sets are:

| Rule | Count |
|---|---:|
| `EXACT_SEQUENCE_LOCK` | 474 |
| `COMPOSITE_PAIR_LOCK` | 29 |
| `REPLACEMENT_FULL_OBJECT_LOCK` | 26 |
| `T4_FORMAT_TEMPLATE_LOCK` | 10 |
| `CROSS_ENCODING_EXACT_TEXT_LOCK` | 1 |
| **Total** | **540** |

`EXACT_SEQUENCE_LOCK` requires one physical counterpart, same-original replacement agreement, object-level replacement agreement, no `%` formatter marker, and at least two same-delta ordered neighbors.

`COMPOSITE_PAIR_LOCK` reconstructs one Switch object from multiple adjacent PC patch records rather than assuming one PC record equals one Switch object.

`REPLACEMENT_FULL_OBJECT_LOCK` requires the current PC replacement to be materially contained in, or prefix-aligned with, the replacement of a PC occurrence whose full Japanese logical object equals the candidate Switch object. Replacement fragments shorter than four bytes are not accepted as hard evidence.

`T4_FORMAT_TEMPLATE_LOCK` resolves the ten CP932 UI-label rows as one coherent Switch formatter/template object rather than ten unrelated writes.

`R16466` is the accepted cross-encoding case: the PC source is UTF-16LE while the Switch counterpart is CP932, but the decoded Japanese text is exact.

### 다. Second reverse-oracle pass resolved 116 additional rows

The second pass starts only from the first-pass `ORACLE_ASSISTED` population. Accepted rule sets are:

| Rule | Count |
|---|---:|
| `SECOND_PASS_STRICT_REVERSE_CONTEXT_LOCK` | 85 |
| `SECOND_PASS_PAIR_LOCK` | 6 |
| `S3_PARTIAL_COMPOSITE_RECONSTRUCTION_LOCK` | 9 |
| `S3_FORMATTER_COMPOSITE_RECONSTRUCTION_LOCK` | 11 |
| `S4B_EMBEDDED_COMPOSITE_RECONSTRUCTION_LOCK` | 5 |
| **Total** | **116** |

The strict reverse-context rule requires:
- current and reverse-found PC logical values to have globally uniform replacements;
- exact Korean replacement equality for S1/S2;
- no `%` formatter marker;
- candidate Switch object to have replacement agreement;
- a full-object PC occurrence;
- at least two ordered PC/Switch neighborhood matches.

The accepted S1/S2 second-pass total is 91 rows: 85 strict reverse-context rows plus six separate pair-lock rows:
`R144, R539, R2035, R2036, R3018, R3019`.

The accepted S3 partial-composite rows are:
`R472, R1861, R1989, R2002, R2016, R2033, R2049, R2053, R2280`.

The accepted S3 formatter/composite rows are:
`R1047, R1123, R1189, R1192, R1194, R1295, R1383, R1492, R1495, R1498, R2863`.

The accepted S4B composite rows are:
`R1110, R1990, R2017, R2034, R2763`.

### 라. Final resolved distribution by stable structural family

| Stable family | Resolved |
|---|---:|
| S1 single physical / single owner | 443 |
| S2 single physical / shared owner | 122 |
| S3 prefix of longer JP object | 41 |
| S4A embedded single physical | 16 |
| S4B embedded single physical / raw multi | 5 |
| S5 embedded multi physical | 18 |
| T4 CP932 UI block | 10 |
| T5 UTF16/mixed block | 1 |
| **Total** | **656** |

No row in these 656 becomes Switch-write authorized merely by this result.

### 마. T1 seven-row broad-region family is rerouted, not directly ported

The seven T1 source rows are:
`R14542, R14544, R14545, R14546, R14547, R14548, R14550`.

The Switch contains a coherent 19-entry expanded region table beginning at raw object start `0x77FF71` and ending with the final object start at `0x780037`:

`北奥羽 / 南奥羽 / 北陸 / 北関東 / 南関東 / 甲信 / 駿遠三 / 濃尾勢 / 北近畿 / 南近畿 / 山陰 / 山陽 / 四国 / 北九州 / 南九州 / 朝鮮 / 明国 / 琉球 / 南蛮`

The PC Korean patch already contains these same detailed-region labels as `R16428-R16446`, with actual Korean replacement bytes.

Therefore the old T1 broad-region obligations are not forced into false one-to-one Switch matches. They are classified:

`ORACLE_REROUTED / SUPERSEDED_BY_EXPANDED_SWITCH_TABLE`

The future porting source for that Switch table is the PC patch's detailed-region occurrences `R16428-R16446`.

### 바. Exact final routing is complete and disjoint

Final family routing:

| Stable family | Resolved | Rerouted | Assisted | Astra | Trace |
|---|---:|---:|---:|---:|---:|
| S1 | 443 | 0 | 73 | 1 | 0 |
| S2 | 122 | 0 | 45 | 0 | 0 |
| S3 | 41 | 0 | 66 | 5 | 0 |
| S4A | 16 | 0 | 2 | 0 | 0 |
| S4B | 5 | 0 | 3 | 0 | 0 |
| S5 | 18 | 0 | 82 | 4 | 0 |
| S6 | 0 | 0 | 0 | 0 | 1 |
| S7 | 0 | 0 | 0 | 0 | 7 |
| T1 | 0 | 7 | 0 | 0 | 0 |
| T2 | 0 | 0 | 19 | 0 | 0 |
| T3 | 0 | 0 | 7 | 0 | 0 |
| T4 | 10 | 0 | 0 | 0 | 0 |
| T5 | 1 | 0 | 0 | 0 | 8 |
| **Total** | **656** | **7** | **297** | **10** | **16** |

Exact membership is stored in the machine-readable artifact.

## 2. 유력한 가설

### 가. The remaining 297 should not be sent directly to Astra

The 297 assisted rows are:

| Family | Count |
|---|---:|
| S5 | 82 |
| S1 | 73 |
| S3 | 66 |
| S2 | 45 |
| T2 | 19 |
| T3 | 7 |
| S4B | 3 |
| S4A | 2 |
| **Total** | **297** |

Most still possess one or more oracle signals. The next efficient step is another deterministic/reverse-oracle pass, not broad semantic review.

### 나. T2/T3 are more likely storage/consumer-layout migrations than translation problems

For T2, 18/19 source values have standalone Switch raw C-string occurrences; T3 has standalone occurrences for all 7. However they are not preserved as the same contiguous PC table. This supports treating them as layout/consumer-routing questions first.

### 다. Astra should remain a narrow adjudicator

Current Astra queue is only ten rows:

- historical semantic holdouts: `R651, R1062, R1277, R1283, R1284, R2572`;
- S5 rows with no useful current oracle signal: `R75, R1583, R1591, R1631`.

This queue may change only if later deterministic analysis produces new evidence. It is not an authorization to start Astra work.

## 3. 미확정 사항

- The 297 assisted rows do not yet have deterministic single-counterpart closure.
- T2/T3 standalone raw occurrences do not yet establish the relevant Switch consumer/table owner.
- The 16 trace rows still require data-structure/encoding/consumer work:
  - T5 mixed/UTF16 residual: `R16458-R16465`;
  - empty logical window: `R1690`;
  - opaque fixed block: `R3244-R3250`.
- The exact target PC EXE remains unavailable; therefore PC target-build XREF/preimage ownership is not newly claimed.
- No write-safety/capacity/overlap authorization is created by this oracle routing.

## 4. 기각된 가설

The following approaches are rejected and must not be reintroduced under another name:

1. `unique physical target + replacement agreement` is enough for semantic binding — REJECTED.
2. A Switch full object appearing elsewhere in the PC patch is by itself enough to select the target — REJECTED.
3. Loose reverse-context matching is a hard resolver — REJECTED. It re-captured known counterexamples including `R19`, `R64`, `R666`, `R1634`, and `R2157`.
4. Short two-byte Korean replacement containment is hard evidence — REJECTED; the accepted full-object replacement rule requires a meaningful replacement length of at least four bytes.
5. Sparse adjacency alone proves a composite — REJECTED.
6. T1 broad PC regions must each receive a direct one-to-one Switch target — REJECTED; the Switch uses an expanded 19-entry region table already represented in the PC patch elsewhere.
7. Structural-family membership itself is the objective — REJECTED. Structural families route the oracle strategy; the objective is actual counterpart resolution.
8. All 986 rows should be sent to Astra — REJECTED.
9. All ambiguous rows require consumer tracing before using PC-patch evidence — REJECTED.

## 5. 관련 영향 범위

This analysis changes the forward-work routing only.

It does not change:
- FZ001 schema freeze;
- F1 accepted 262;
- F1 static write-authorized 158;
- Stage-2 affine mappings;
- stable forward 986 structural membership;
- PC runtime/DLL facts;
- the porting framework;
- builder/IPS/runtime implementation;
- any game file.

The oracle artifact is an overlay on the stable 986 partition.

## 6. 수정 제안

No implementation modification is proposed at this stage.

The next recommended read-only scope, after a fresh explicit user signal, is:

`PC_PATCH_ORACLE_ASSISTED_297_FOLLOWUP`

Recommended order:
1. S1/S2 remaining reverse-oracle closure;
2. S3 reuse of existing semantic overlays plus full-object/composite evidence;
3. S5 replacement/full-object/composite narrowing;
4. T2/T3 storage/consumer ownership;
5. S4A/S4B remainder;
6. Astra only for the genuinely semantic remainder;
7. consumer tracing only for the 16 structural/encoding blockers or newly proven equivalents.

Repository write, framework modification, builder/runtime work, and Switch write authorization require separate explicit authorization.
