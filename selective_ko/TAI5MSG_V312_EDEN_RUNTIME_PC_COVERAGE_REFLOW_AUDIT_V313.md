# TAI5MSG V312 EDEN RUNTIME / PC COVERAGE / REFLOW AUDIT — V313

Date: 2026-09-18 (KST)
Status: CLOSED / EDEN ANDROID RUNTIME PASS FOR SELECTED TAI5MSG / PC COVERAGE AUDITED / HARD-OVERFLOW PARTITIONED / B24 SEMANTIC-LAYOUT HOLD
Track: `SWITCH_SELECTIVE_KOREANIZATION`
Validation ID: `V313`
Parent canonical HEAD: `2856aef8f5dd8a5987a86ecaf69e80ea87788a2b` — V312 package materialization

## 1. Purpose

This checkpoint consolidates the V312 Eden runtime observations and the subsequent read-only PC-Korean TAI5MSG coverage / line-reflow audit.

It does not modify translations, TAI5MSG bytes, the serializer, ExeFS IPS, font, package contents, inline 139, EVENT/TS5, SNR, CWTDAT, names/yomi, or any gameplay asset.

The next executable cause-family is isolated to B24 selected messages:

`TAI5MSG_B24_124_PC_KO_SEMANTIC_ALIGNMENT_AND_LAYOUT_AUDIT_READ_ONLY`

## 2. Runtime evidence

User-supplied Eden Android runtime evidence established all of the following for the exact V312 package family.

Log evidence:

- title/program ID `0100346017304000` was executed;
- `HasNSOPatch` queried build ID `D9120950C258610A746F4A31CE3A3B376DE393D9`;
- Eden logged `Applying IPS patch from mod "Taiko5DX_KR_SELECTIVE"`;
- Eden logged successful RomFS update application followed by `LayeredFS patches applied successfully`.

Visible runtime evidence:

- card/person description for `九鬼嘉隆` displayed Korean prose while the dedicated identity remained Japanese;
- title/card description for `剣聖` displayed Korean prose while the dedicated title remained Japanese;
- Korean glyph rendering was legible;
- the visible result therefore demonstrates effective TAI5MSG Korean payload consumption together with Mapping/page/font realization on this route.

Current runtime dispositions:

```text
ExeFS IPS / exact main Build ID              PASS
LayeredFS title-level application             PASS
TAI5MSG selected Korean visible in game       PASS
Korean Mapping realization                    PASS on observed route
runtime page mapper                           PASS on observed route
FONT_JPN.G1T Korean glyph rendering           PASS on observed route
identity presentation KEEP_JP                 PASS on observed examples
physical Nintendo Switch / Atmosphere         NOT TESTED
```

Do not reopen “V312 is not loaded”, “TAI5MSG override is globally absent”, “font is globally absent”, or “Mapping is globally absent” without new contradictory evidence.

## 3. PC source identities used by the coverage audit

```text
PC original TAI5MSG
size    1,810,889
sha256  aae037dd5948f79b9fc2e5affcb1e60e08efca39f897123045fe685786be978f

PC Korean v1.02 TAI5MSG
size    2,134,366
sha256  e3b4522a1047ff409e099b5ee197d7689279ea7472cb403d305b2507fec96090

PC Korean patch dinput8.dll
size    836,096
sha256  ffe7e9da8e00c96bec631b45a3e9c4d3f314551623351f3e7024e0318913c6b7

T5K mapping entries          10,036
unique game codes            10,035
```

The audit uses actual game-code bytes, not guessed Unicode width.

## 4. PC TAI5MSG coverage census

Across all 14,832 TAI5MSG logical slots:

```text
all messages                         14,832
PC-KO messages with Korean codes     13,591
messages with no Korean code          1,241
byte-identical to JP among those      1,233
different from JP but no Korean           8
```

The 13,591 count is a Korean-bearing byte census, not a claim that every such slot is semantically correct or final-QA complete.

For the V303/V312 selected population:

```text
selected rows                         3,179
selected rows containing Korean       3,179 / 3,179
selected rows byte-identical to JP        0
PC Korean-bearing rows outside V312  10,412
  caller-wait rows                       191
  outside current selected source floor 10,221
```

Therefore random Japanese description screens are not sufficient evidence of package failure. Some low-priority/person/shop-owner descriptions may remain Japanese in the PC patch or may belong to another non-selected container/slot. Exact PC payload existence and selected membership must be checked before classifying such a screen as a defect.

## 5. Message-window width model and observed reflow defect

Inherited reported PC-patch authoring constraint:

```text
20 full-width units per line
40 half-width units per line
2 half-width = 1 full-width
```

The V313 byte-width audit uses:

```text
single-byte printable / space   1 unit
valid two-byte mapped glyph     2 units
0x1B control sequence           0 width
terminator                      0 width
newline                         reset line width
```

The observed `剣聖` card is a direct runtime corroboration.

Exact selected anchor:

```text
B23:M094
SEL-CAND-001712
runtime_message_id 23094
caller B23_DESCRIPTION
```

PC-KO prose includes:

```text
검술 계열 칭호.
자신을 천지와 하나로 만들고 흐르는 맑은 물과
같은 검을 휘두르는 궁극의 검사에게만
주어지는 칭호.
도장을 열 수 있다.
```

Measured line widths:

```text
15 / 44 / 36 / 14 / 18
```

The 44-unit line visibly forced an undesirable syllable-level wrap in Eden. This supports the conclusion that at least part of the visible wrapping defect is inherited from incomplete PC manual reflow rather than a Mapping/font failure.

## 6. Hard-overflow census

Within the selected 3,179 messages:

```text
all lines <= 40 units                 2,482 messages
at least one line > 40 units            697 messages
over-40 lines total                    1,535 lines

overflow rows with existing PC newline   639
overflow rows with no PC newline           58
```

Per block:

```text
B0      2
B17    40
B18    12
B19    62
B20    42
B21     2
B22   308
B23   120
B24   109
------------
total 697
```

Per resolved caller family:

```text
B0_SYSTEM                  2
HELP_RENDERER_0x220E60   265
B21_SYSTEM_PROGRESSION     2
B22_DESCRIPTION          308
B23_DESCRIPTION          120
```

Usage:

```text
UI_DESCRIPTION       693
NARRATION_SYSTEM       4
```

Realization:

```text
REBUILT_BLOCK_GROWTH     683
CURRENT_BLOCK_ENVELOPE    14
```

No whitespace-delimited token in the 697-row population exceeds 40 units. Thus ordinary overflow rows can, in principle, be wrapped at existing word boundaries without forced Korean syllable splitting.

## 7. Reflow partition discovered during design audit

The 697 rows are not one homogeneous cause-family.

```text
ordinary text                                     382
control sequences integrated normally in body     207
body/control skeleton separated                    108
------------------------------------------------------
total                                              697
```

The 108 body/control-skeleton-separated rows are in B24.

Safe ordinary reflow population currently identified:

```text
B17..B20 HELP_RENDERER   156
B22_DESCRIPTION          308
B23_DESCRIPTION          120
----------------------------
subtotal                 584
```

B0/B21 four rows remain width-model/caller-specific evidence waits.

B24 must be audited separately before any reflow implementation.

## 8. B24 semantic-alignment defect family

B24 selected population is:

```text
B24 selected rows      124  (M221..M344)
B24 hard-overflow      109
B24 separated control skeleton pattern 108
```

A semantic slot-misalignment / duplicate-payload family was discovered.

Representative proven examples:

```text
B24:M227  JP source role begins ●人材調査
           PC-KO payload instead corresponds closely to the later 米買占め/借金取立 family

B24:M228  JP source role 足軽大将ﾉ主命
           PC-KO payload instead corresponds closely to the later 特産品調査/人材調査 family

B24:M229  JP source role is an 足軽大将 mission-description slot
           PC-KO payload instead corresponds closely to the later 交易品輸送 family
```

The misplaced Korean bodies have near-duplicate counterparts later in the same PC-KO B24 region:

```text
M227 ~ M327 KO body   approximately 97.5% similar
M228 ~ M328 KO body   approximately 89.2% similar
M229 ~ M329 KO body   approximately 94.9% similar
```

These are not treated as mere wording differences. They are evidence that Korean-bearing presence alone does not prove correct JP-slot semantic correspondence.

A second B24 property is layout collapse:

- many PC-KO messages contain a flattened Korean body;
- original-style control/newline skeleton bytes remain later in the message;
- therefore B24 cannot be repaired safely by whitespace-only wrapping before semantic/control alignment is audited.

Do not patch only M227..M229. The whole B24 selected 124-row family must be inspected because the same authoring/export mechanism may affect adjacent rows.

## 9. Proposed safe reflow contract for non-B24 ordinary rows

When separately authorized after B24 closure, ordinary reflow should be byte-conservative.

Allowed mutation class:

```text
0x20 SPACE <-> 0x0A NEWLINE
```

Preserve exactly:

- all Korean and Japanese game-code bytes;
- digits and punctuation;
- all `0x1B` control sequences and their parameters;
- message terminal bytes;
- candidate membership and locator;
- text token order.

Width selection rule:

- never split inside a Korean whitespace-delimited token when a prior boundary exists;
- choose the last legal token boundary that keeps the line at or below 40 units;
- preserve explicit structural section starts such as `●`, `◆`, `※`, deliberate empty lines, and style-control boundaries as hard boundaries unless a caller-specific audit proves otherwise;
- treat ordinary sentence-internal PC newlines as soft candidates, not absolute authority;
- compute width from game-code bytes, not Unicode string length.

A desirable implementation property is length preservation by exchanging space and newline bytes only. This avoids changing message/block offsets for the ordinary reflow family.

This is a design proposal only; it is not implementation authority yet.

## 10. 확정된 사실

1. V312 selected TAI5MSG Korean text is visibly consumed in Eden Android.
2. V312 Mapping/page/font path is functional on observed selected-card routes.
3. Dedicated identity/title fields remained Japanese while Korean prose rendered, matching selective identity policy.
4. All 3,179 selected TAI5MSG rows contain Korean codes in canonical PC-KO source.
5. PC-KO TAI5MSG contains 13,591 Korean-bearing messages, leaving 10,412 Korean-bearing rows outside current V312.
6. 697 selected messages contain at least one line over the 40-half-width-unit model.
7. B23:M094 / SEL-CAND-001712 is a visible runtime example whose 44-unit PC-KO line reproduces the observed bad wrap.
8. The 697 rows split into ordinary/control-integrated and B24 body/control-separated families.
9. B24 has 124 selected rows, 109 hard-overflow rows and 108 body/control-skeleton separation cases.
10. B24:M227..M229 provide concrete semantic slot-misalignment evidence with near-duplicate later PC-KO payloads.

## 11. 유력한 가설

The B24 defect family most likely reflects an incomplete/incorrect PC patch authoring or export/reconstruction process in which Korean bodies were flattened and, for some slots, displaced or duplicated while original control/newline skeleton data remained.

The exact historical editor/export step is not established and must not be invented.

## 12. 미확정 사항

- semantic correctness of all 124 selected B24 rows;
- exact count of B24 rows requiring payload reassignment versus only layout reconstruction;
- whether B0/B21 system callers use the same 40-unit visible width;
- exact provenance of low-priority/shop-owner untranslated descriptions seen during random gameplay;
- physical Nintendo Switch/Atmosphere behavior.

## 13. 기각된 가설

Rejected or materially weakened:

- V312 is globally not loaded by Eden;
- TAI5MSG LayeredFS override is globally absent;
- Korean font/Mapping/page mapper is globally nonfunctional;
- all 697 overflow rows are one uniform whitespace-only reflow family;
- Korean-bearing presence proves correct semantic JP-slot alignment;
- preserving all PC-KO manual line breaks is sufficient final layout QA;
- B24 M227..M229 may be patched locally without auditing the common B24 cause-family.

## 14. 관련 영향 범위

Immediate future work is partitioned:

```text
B24 selected 124
 -> semantic alignment + control/layout audit FIRST

ordinary non-B24 overflow 584
 -> whitespace-only reflow candidate AFTER B24 cause-family separation

B0/B21 overflow 4
 -> caller-specific width validation

PC Korean-bearing outside current V312 10,412
 -> future coverage expansion only after role/caller/mechanism admission
```

No bulk PC TAI5MSG import is authorized.

## 15. 수정 제안 / next scope

Next executable scope:

`TAI5MSG_B24_124_PC_KO_SEMANTIC_ALIGNMENT_AND_LAYOUT_AUDIT_READ_ONLY`

Required work:

1. enumerate all B24 selected locators M221..M344;
2. compare JP slot meaning/structure with exact PC-KO same-slot payload;
3. detect duplicate/displaced Korean bodies against neighboring/later B24 slots;
4. inventory control/newline skeleton position and body/control separation;
5. classify each row as one of:
   - `CORRECT_PAYLOAD`
   - `WRONG_SLOT_DUPLICATE`
   - `PC_UNTRANSLATED`
   - `PC_MISSING`
   - `LAYOUT_COLLAPSED`
   - compound classification where evidence supports it;
6. report the complete common-cause impact range before proposing any repair.

No implementation, TAI5MSG mutation, build, package, or repository write is authorized by that audit itself.

## 16. Repository write boundary

Any later repository materialization remains restricted to:

`create_blob -> create_tree -> create_commit -> update_ref(force=false)`

