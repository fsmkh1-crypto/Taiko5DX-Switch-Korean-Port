# PC Patch Oracle TRACE 19 Closure — canonical read-only routing closure

Date: 2026-09-13 (KST)  
Status: CANONICAL READ-ONLY TRACE CLOSURE / NO SWITCH WRITE AUTHORIZATION  
Parent HEAD: `0710e36077dd5184974701da67c4b019fa751851`

## 요약

The exact canonical TRACE queue of 19 rows has now been analyzed by cause group without framework, builder, IPS, runtime, game-file, or Switch-write modification.

Final TRACE-closure overlay:

| Disposition | Count | Exact membership |
|---|---:|---|
| `TARGET_RESOLVED` | 8 | `R19, R3244-R3250` |
| `COMPOSITE_OR_FORMATTER_RESOLVED` | 3 | `R1283, R1284, R1690` |
| `ORACLE_REROUTED` | 8 | `R16458-R16465` |
| `NEED_TRACE` | 0 | none |
| **Total** | **19** | exact / disjoint / complete |

Effective forward routing after this overlay:

```text
BASE_ORACLE_RESOLVED                         656
BASE_ORACLE_REROUTED                           7
ASSISTED_FOLLOWUP_TARGET_RESOLVED             65
ASSISTED_FOLLOWUP_COMPOSITE_RESOLVED         231
ASTRA_FOLLOWUP_COMPOSITE_RESOLVED              8
TRACE_CLOSURE_TARGET_RESOLVED                   8
TRACE_CLOSURE_COMPOSITE_RESOLVED                3
TRACE_CLOSURE_REROUTED                          8
TRACE_REQUIRED                                  0
                                             ---
TOTAL                                        986
ORACLE_ASSISTED_REMAINDER                      0
ASTRA_REQUIRED_REMAINDER                       0
TRACE_REMAINDER                                0
```

Consolidated current counterpart classes:

- base deterministic Oracle resolved: 656
- target resolved: 73
- composite/formatter resolved: 242
- rerouted: 15
- trace: 0
- total: 986

Counterpart/routing closure still does **not** imply `WRITE_SAFE`.

## 1. 확정된 사실

### 가. R19 — owner binding resolved

`R19` has one Switch target object and the unresolved question was which competing PC occurrence should own the Korean oracle.

The long command-family lineage on Switch preserves the first PC command-sequence occurrence far more strongly than the later vocabulary/menu-style occurrence. The Switch localization entry is reused by multiple consumers, so the remaining issue is presentation policy rather than target discovery.

Disposition:

`R19 = TARGET_RESOLVED / OWNER_BOUND`

Annotation:

`MERGED_CONSUMER_PRESENTATION_CONFLICT`

Switch localization owner:

`JP ID 1088`

No Switch write is authorized.

### 나. R1283 / R1284 — opening and closing owners resolved

The available PC EXE is not the exact global T5K target build and remains barred from whole-program target-build XREF claims.

However, the local region covering `R1276-R1290` preserves all 15 canonical T5K preimages at the same local positions. Within that preserved block, the two `発生条件` occurrences are directly separated into opening-side and closing-side objects, and the Switch localization block preserves the same longer structured sequence.

Resolved owners:

- `R1283 -> JP ID 2795` opening-side object
- `R1284 -> JP ID 2796` closing-side object

Dispositions:

- `R1283 = COMPOSITE_OR_FORMATTER_RESOLVED / OPENING_OWNER_BOUND`
- `R1284 = COMPOSITE_OR_FORMATTER_RESOLVED / CLOSING_OWNER_BOUND`

Occurrence order or NUL padding alone remains rejected; the closure is based on full local object structure and long-block correspondence.

### 다. R1690 — padding-extension component resolved

`R1690` is not an independent semantic string.

It is a one-byte extension component of the preceding `R1689` translated object. The Korean replacement consumes one byte of the original trailing layout, and `R1690` restores the required trailing-space structure.

Switch ownership is therefore inherited from the complete `R1689` counterpart:

`R1689 -> JP ID 3245`

Disposition:

`R1690 = COMPOSITE_OR_FORMATTER_RESOLVED / PADDING_EXTENSION_COMPONENT`

No standalone `R1690` Switch action should be created.

### 라. R3244-R3250 — language-table encoding blocker resolved

The seven records are not opaque binary data.

Their PC originals are Simplified-Chinese localization strings encoded in GBK. The exact same Chinese logical strings exist in the Switch CN localization table as one consecutive run, and the same localization IDs in the JP table contain the corresponding Japanese command concepts.

Exact target identities:

| Row | Switch localization ID | Routing note |
|---|---:|---|
| `R3244` | 1099 | CN exact counterpart; same-ID JP semantic counterpart |
| `R3245` | 1100 | CN exact counterpart; same-ID JP semantic counterpart |
| `R3246` | 1101 | CN exact counterpart; same-ID JP semantic counterpart |
| `R3247` | 1102 | CN exact counterpart; same-ID JP semantic counterpart |
| `R3248` | 1103 | CN exact counterpart; same-ID JP semantic counterpart |
| `R3249` | 1104 | CN exact counterpart; same-ID JP semantic counterpart |
| `R3250` | 1105 | CN exact counterpart; same-ID JP semantic counterpart |

Disposition for all seven:

`TARGET_RESOLVED / CN_LANGUAGE_TABLE_EXACT_COUNTERPART`

Annotation:

`LANGUAGE_TABLE_REROUTE_REQUIRED`

The PC patch uses different Korean presentation in some JP/CN occurrences for IDs 1101-1105. That is a later presentation-policy question, not target ambiguity.

### 마. R16458-R16465 — one PC UTF-16 warning rerouted to Switch-native localization owner

The eight rows are eight inline windows inside one PC UTF-16LE startup/display-resolution warning. They are not eight separate strings.

The exact PC wide-string object does not exist on Switch. The same semantic obligation is represented by the Switch localization system at:

`JP ID 1480`

The PC Korean patch also contains a separate ordinary localization-side Korean oracle for the generalized display-capability message corresponding to that Switch object.

Therefore the eight PC UTF-16 windows must not be forced into a nonexistent Switch UTF-16 object.

Disposition for all eight:

`ORACLE_REROUTED / PC_WIDE_RESOLUTION_DIALOG_SUBSUMED_BY_SWITCH_LOCALIZATION_1480`

At final source/action accounting, these rows may be `SUBSUMED` only after an explicit non-`SUBSUMED` Switch action for localization ID 1480 is linked.

They are not `PROVEN_IRRELEVANT`.

### 바. TRACE partition is exact

The original exact queue was:

`R19, R1283, R1284, R1690, R3244-R3250, R16458-R16465`

The final partition is disjoint and complete:

- target resolved: 8
- composite/formatter resolved: 3
- rerouted: 8
- trace remainder: 0
- intersection: 0
- unclassified: 0

## 2. 유력한 가설

No target/owner/encoding hypothesis remains necessary to route any of the 19 TRACE rows.

Implementation-stage hypotheses remain deliberately unpromoted:

- R19 may be representable by one common Korean rendering across merged consumers;
- R1283/R1284 may be writable as two complete localization objects without any consumer-specific hook;
- R1690 should be absorbed into the complete JP3245 replacement rather than emitted separately;
- R3244-R3250 should normally collapse to the same logical Korean localization IDs rather than create duplicate CN writes;
- R16458-R16465 should collapse into the Switch ID1480 action rather than recreate the PC wide dialog.

These are implementation directions, not `WRITE_SAFE` claims.

## 3. 미확정 사항

The following remain outside TRACE closure:

- final Korean presentation policy for R19 merged consumers;
- final JP/CN wording choice for localization IDs 1101-1105;
- storage capacity and terminator safety for all eventual Switch writes;
- formatter/control preservation;
- shared-owner effects;
- runtime reachability where required;
- exact source-to-action ledger linkage for rerouted/subsumed obligations;
- final `WRITE_SAFE` authorization;
- builder/IPS/runtime implementation.

The exact canonical PC target EXE remains unavailable. The nonmatching PC EXE may support locally verified preimage structure only where explicitly stated; it does not authorize global target-build XREF conclusions.

## 4. 기각된 가설

The following remain rejected:

1. same Japanese source text alone proves the correct PC owner;
2. occurrence order or NUL padding alone binds R1283/R1284;
3. an empty logical window should be matched as an empty-string prefix;
4. R1690 needs an independent Switch text target;
5. CP932 decode failure means R3244-R3250 are non-text binary data;
6. a CN counterpart automatically authorizes a CN-table Switch write;
7. R16458-R16465 are eight independent Switch UI targets;
8. Switch must recreate the PC UTF-16 display dialog;
9. an absent exact PC-specific object may be silently omitted;
10. target/counterpart/routing closure is equivalent to `WRITE_SAFE`;
11. the nonmatching PC EXE may be used as global canonical target-build XREF proof;
12. already-verified FZ001, F1, Stage-2, stable-986, Oracle V1, assisted, or Astra results should be reopened because this overlay exists.

## 5. 관련 영향 범위

This overlay changes only the effective disposition of the canonical TRACE 19 queue.

Unchanged:

- FZ001 semantic bindings;
- F1 accepted 262 and F1 action split;
- Stage-2 mappings;
- stable forward-986 structural membership;
- Oracle V1 provenance;
- assisted-297 provenance;
- Astra-10 provenance;
- framework/schema;
- builder/IPS/runtime;
- game files;
- Switch write authorization.

Historical TRACE counts remain provenance in older artifacts. Current effective TRACE remainder becomes `0` only through this overlay.

## 6. 수정 제안

Materialize this closure as a read-only canonical overlay only.

Create:

- this report;
- a dedicated validation ledger;
- machine-readable `INDEX.json`;
- machine-readable `MEMBERSHIP.json`;
- an updated `PROJECT_STATE.md` pointing to the new authority.

Do not start any builder/runtime implementation in the same step.

After materialization, the next project phase should be separately authorized and should focus on write-safety/action-ledger planning for the now fully routed forward-986 population.

Repository write mechanism for this materialization is restricted to:

`create_blob -> create_tree -> create_commit -> update_ref(main, force=false)`

No other write action is authorized.
