# TAI5MSG B24 SEMANTIC/LAYOUT CORRECTION IMPLEMENTATION + OFFLINE VALIDATION — V315

Date: 2026-09-18 (KST)  
Status: CLOSED / IMPLEMENTED / OFFLINE BYTE-EXACT VALIDATED / NO PACKAGE / NO HARDWARE  
Track: `SWITCH_SELECTIVE_KOREANIZATION`  
Validation ID: `V315`  
Parent canonical HEAD: `087bf9382438c78d4f60bc01be3ad4eec4cfb72d` / V314

## 1. Scope

V315 implements the common-cause B24 repair authorized after the exhaustive B24 audit.

The affected family is the selected B24 range `M221..M344`.

```text
selected B24 rows                       124
CORRECT_PAYLOAD + LAYOUT_COLLAPSED     106
WRONG_SLOT_DUPLICATE + LAYOUT_COLLAPSED  3  M227/M228/M229 family
CORRECT_PAYLOAD, no layout repair       15
actual changed rows                     109
```

No package, IPS, Eden package, physical Switch build, or hardware execution is performed in V315.

## 2. Source/provenance

Canonical sources remain:

```text
PC JP TAI5MSG
size    1,810,889
sha256  aae037dd5948f79b9fc2e5affcb1e60e08efca39f897123045fe685786be978f

PC Korean v1.02 TAI5MSG
size    2,134,366
sha256  e3b4522a1047ff409e099b5ee197d7689279ea7472cb403d305b2507fec96090

PC dinput8 Mapping
entries 10,036
```

V315 consumes the V314 cache instead of reconstructing the PC patcher.

## 3. Correction artifact

Artifact:

`selective_ko/artifacts/tai5msg_b24_semantic_layout_correction_v1/INDEX.json`

Rows:

`selective_ko/artifacts/tai5msg_b24_semantic_layout_correction_v1/ROWS.jsonl`

Every changed row uses `EXACT_REPLACE_MESSAGE` with exact source length/SHA/bytes and exact target length/SHA/bytes.

The source identity is the canonical PC-KO TAI5MSG. Application is fail-closed through `builder/tai5msg_corrections.py`.

## 4. Layout reconstruction contract

For the 108 body/control-separated rows:

1. consume only the Korean semantic body before the stale skeleton tail;
2. preserve the existing Korean wording for the 106 semantically correct rows;
3. rebuild `●` headings with `1B4331 ... 1B4330`;
4. rebuild `◆` headings with `1B4333 ... 1B4330`;
5. place body lines under the heading with the original B24 full-width indent `0x8140`;
6. insert a blank line before a later `●` mission section;
7. wrap only at whitespace boundaries so every visible line is `<= 40` half-width units;
8. preserve the standard `05 05 05` terminal.

The stale tail contains `1B4B/1B48` only where JP source uses half-width-katakana fragments such as `ﾚﾍﾞﾙ` and `ﾐﾆｹﾞｰﾑ`. The Korean semantic prefix itself does not contain those controls. V315 therefore does not transplant those stale JP inline controls into the Hangul target.

Observed removed stale-control counts in the 109 source rows:

```text
1B4B   55
1B48  143
```

Rebuilt semantic section controls:

```text
1B4331  122
1B4333  216
1B4330  338
```

## 5. Semantic corrections

### M227

PC-KO same-slot payload is displaced/wrong.

V315 uses the already recoverable PC-KO `인재 조사` body:

```text
●인재 조사
아직 만나지 못한 낭인을 찾습니다.

◆달성 방법
마을의 민가 등을 찾아가 안면이 없는 낭인을 찾습니다.
발견한 낭인이 많을수록 높은 평가를 받습니다.
```

The final byte payload is reflowed to the 40-unit B24 layout contract.

### M228

Exact replacement:

```text
아시가루 대장의 주명
```

No B24 body layout reconstruction is needed for this title-only slot.

### M229

Historical PC Korean body is not recoverable and the v1.02 same-slot payload is the wrong `교역품 수송` body.

New translation is based on the exact JP M229 source while following the existing PC Korean terminology/style:

```text
신분이 아시가루 대장일 때 받을 수 있는 주명입니다.
아시가루 조두의 주명도 받을 수 있습니다.

●군자금 조달
맡은 돈을 최대한 많이 늘립니다.

◆달성 방법
맡은 돈으로 마을의 좌에서 교역품을 사고팔아 돈을 늘립니다.

◆유효 기능 등
산술, 변설.
```

Relevant PC style evidence inside the same B24 family uses `맡은 돈`, `좌`, `교역품`, and `산술, 변설`.

## 6. Untouched B24 rows

These 15 selected B24 rows remain byte-identical to V312 because their payload and layout were already correct:

```text
M232 M238 M249 M252 M256
M270 M279 M285 M287 M300
M307 M317 M319 M335 M341
```

## 7. Offline byte-exact validation

The existing V312 selective TAI5MSG was used only as an independently verified selected-message oracle. The final file was reserialized using the canonical stock block contracts.

```text
total messages                       14,832
selected rows                         3,179
unselected rows                      11,653
changed messages                        109
changed messages outside B24              0
untouched B24 15 mutation count           0
max corrected visible line width         40
```

Serializer structural results:

```text
output size       1,840,073 / 0x1C13C9
output sha256     b212da65010d3a2e7ff6f7b8e10ce57371cb67e3093f58a6ad16a085399a8d0d
growth            0x7200

B24 declared      0xECC0
B24 used_end      0xECA5
B24 growth        0x08C0
runtime capacity  0x20000  PASS

B32 offset        0x1B4980
B32 used_end      0xB8D5
B32 declared      0xCA80
B32 physical      0xCA49
B32 omitted       0x37

largest declared  0x12B00 < 0x20000
```

The changed B24 message payload total shrinks from `30,279` to `28,850` bytes, a semantic-message delta of `-1,429` bytes. Block alignment makes the final file `1,408` bytes smaller than V312.

Mapping/control validation:

```text
unique two-byte codes          1,011
two-byte occurrences         225,866
unique Korean-added codes        992
Korean-added occurrences     219,210
unknown control                 NONE
mapping-domain miss             NONE
```

Determinism/invariants:

```text
zero-replacement stock rebuild        PASS_BYTE_IDENTICAL
V315 deterministic rebuild            PASS_BYTE_IDENTICAL
14,832 message reparse                PASS
3,179 selected exact-target check     PASS
11,653 unselected JP preservation     PASS
B24 changed-locator set = 109         PASS
all corrected lines <= 40 units       PASS
runtime block capacity                PASS
```

## 8. 확정된 사실

1. The B24 common-cause family is repairable without touching game logic, ExeFS, font, Mapping, caller resolution, or selection membership.
2. Exactly 109 B24 messages change.
3. The 106 semantically correct collapsed rows preserve their Korean wording and receive layout reconstruction only.
4. M227/M228/M229 receive semantic correction; only M229 requires a newly authored Korean translation.
5. The rebuilt file remains comfortably below the verified `0x20000` per-block runtime capacity.
6. The resulting TAI5MSG is deterministic and preserves every unselected message byte-for-byte.

## 9. 유력한 가설

The corrected B24 payload should render materially better than V312 because the flattened Korean body and stale skeleton tail are removed and all reconstructed visible lines obey the 40-unit model.

This remains a runtime expectation until a diagnostic package is executed in Eden or on physical Switch.

## 10. 미확정 사항

- Actual Eden rendering of representative corrected B24 rows.
- Physical Nintendo Switch/Atmosphere behavior.
- Whether any B24 caller has a display constraint stricter than the audited 40-unit model.

## 11. 기각된 가설

```text
Only M227..M229 need B24 repair                         REJECTED
All 124 B24 rows need a new translation                REJECTED
The stale JP 1B4B/1B48 tail must be copied into Hangul REJECTED
B24 correction requires game-logic/ExeFS changes       REJECTED
B24 correction approaches runtime block capacity        REJECTED
```

## 12. 관련 영향 범위

Changed:

```text
B24 selected M221..M344: 109 exact message replacements
builder selective TAI5MSG correction application
metadata/output postconditions
offline regression tests
```

Unchanged:

```text
V303 membership 3,179
V304 two legacy exact-byte corrections
Mapping 10,036
FONT_JPN.G1T
ExeFS IPS
identity KEEP_JP policy
package integration layer
all non-B24 selected payloads
all 11,653 unselected JP payloads
```

## 13. Next scope

The next step is intentionally separated from V315:

`TAI5MSG_B24_V315_EDEN_DIAGNOSTIC_PACKAGE_MATERIALIZATION`

That later scope should build one diagnostic package from the V315 serializer output and validate representative B24 rows in runtime. It must not simultaneously begin the ordinary non-B24 584-row reflow family.

## 14. Repository write boundary

Any V315 materialization remains restricted to:

`create_blob -> create_tree -> create_commit -> update_ref(force=false)`
