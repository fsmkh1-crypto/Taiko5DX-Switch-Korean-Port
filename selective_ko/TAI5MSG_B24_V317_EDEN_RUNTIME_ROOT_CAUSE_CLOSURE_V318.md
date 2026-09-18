# TAI5MSG B24 V317 Eden Runtime Root-Cause Closure — V318

Date: 2026-09-18 (KST)

Validation ID: `V318`

Parent canonical state:

`c14f7f05995ad25cf7781240d31164bfe74bf9e8` — V317 B24 V315 Eden diagnostic package materialization.

Status:

`CLOSED / RUNTIME EVIDENCE INTEGRATED / V315 B24 40-UNIT HARD-WRAP MODEL SUPERSEDED / NO PRODUCT BYTES CHANGED`

## 1. Scope

V318 records the Eden Android runtime evidence supplied by the user for the exact V317 diagnostic package and closes the immediate B24 runtime root-cause analysis.

V318 is documentation only.

It does not modify:

- TAI5MSG bytes;
- the V315 correction artifact;
- the serializer;
- ExeFS IPS;
- font data;
- the V317 ZIP;
- any runtime binary;
- any translation payload.

The V317 package identity remains historical evidence:

```text
Taiko5DX_KR_SELECTIVE_V315_B24_EDEN_DIAG.zip
bytes   3,208,715
sha256  aded0ebc67a1ac8bfc57351c418e7d447188cfce2e7f36b9d8b234f40979d614
```

## 2. Runtime evidence class

Evidence source:

`USER_SUPPLIED_EDEN_ANDROID_SCREENSHOTS / CHAT EVIDENCE / NOT REPOSITORY-ARCHIVED IN V318`

Observed screens include:

- 足軽組頭の主命;
- 武士の主命 menu;
- B24 `인재 조사`;
- 성주/국주 mission help;
- 부장 mission help;
- 아시가루 대장 mission help;
- B24 `군자금 조달`;
- additional long B24 help bodies.

The screenshots establish visible runtime behavior but V318 does not invent image hashes or repository provenance that were not materialized.

## 3. Runtime dispositions

### Semantic correction results

```text
B24:M227  인재 조사             PASS_SEMANTIC / PASS_VISIBLE_LAYOUT
B24:M228  아시가루 대장의 주명   PASS_SEMANTIC / FAIL_HEADER_WRAP
B24:M229  군자금 조달            PASS_SEMANTIC / PASS_VISIBLE_LAYOUT
```

M227 no longer displays the displaced later-slot payload.

M229 displays the newly authored 군자금 조달 content with the intended section order and readable Korean glyphs.

Therefore the V315 semantic repairs for M227/M228/M229 are not rejected by the runtime evidence.

### Long-body runtime defect

Multiple longer B24 help messages visibly render lines below the white help-body panel.

Representative visible behavior:

- short bodies such as M227 and M229 remain inside the panel;
- longer bodies exceed the panel height;
- the overflow is correlated with the number of authored hard-newline rows produced by V315.

This is a B24 body-layout failure, not a global Mapping/font/TAI5MSG-delivery failure.

## 4. B24 official-language structural comparison

Read-only comparison of official B24 M221..M344 JP/SC/TW source families established:

```text
                  maximum authored lines   maximum authored line width
JP                         12                         52 units
SC                         12                         52 units
TW                         12                         52 units

official lines > 40 units
JP                         71
SC                         48
TW                         48
```

Therefore `line width > 40` is not itself an invalid B24 condition.

The B24 caller must not inherit the V313 ordinary-message 40-unit reflow model without caller-specific proof.

## 5. V315 layout-model correction

V315 reconstructed 108 B24 layout rows using a hard-wrap contract that forced each produced line to at most 40 units.

Runtime evidence invalidates that contract for B24.

V315 remains authoritative for:

- the M227 semantic recovery;
- the M228 semantic/title recovery;
- the M229 군자금 조달 semantic recovery;
- removal of stale flattened PC-KO body/control separation;
- exact source-guard provenance of the 109 correction rows.

V315 is superseded for:

`B24 40-unit hard-wrap / max-line-width-as-layout-correctness model`

This supersession is B24-specific.

It does **not** automatically invalidate the separately isolated ordinary non-B24 584-row reflow candidate family. That family still requires its own caller-specific design/validation.

## 6. Switch B24 text-render behavior

Read-only Switch main analysis established a native line-wrap path at:

`mapped 0x44714C`

The text renderer advances to a new line when the current glyph would exceed the right-side extent.

Explicit newline `0x0A` also advances to a new line.

Therefore B24 does not require sentence text to be pre-wrapped every 40 units in TAI5MSG.

The safer B24 direction is:

- preserve semantic text;
- preserve semantic section boundaries such as `●`, `◆`, `※`;
- preserve required style/control boundaries;
- avoid unnecessary sentence-internal hard newlines;
- let the native renderer perform ordinary visual wrapping;
- validate the resulting authored-line/visible-line height against the B24 fixed help panel.

## 7. Scrollbar / viewport finding

Read-only analysis of the B24 path around `0x220E60` / `0x220B18` shows the visible right-side scrollbar belongs to help-entry/list position handling rather than an established per-message text-body scroll mechanism.

The runtime overflow must therefore not be papered over by assuming that a long individual message can be scrolled internally.

Current evidence supports a fixed-height help-body contract.

## 8. 0x1B48 / 0x1B4B disposition

Restoring JP-only `0x1B48 / 0x1B4B` control bytes is not supported as the root fix for the long-body defect.

Official localized SC/TW B24 material can represent corresponding help content without requiring those JP control bytes.

Therefore:

`MISSING_1B48_1B4B_CAUSES_B24_BODY_OVERFLOW = REJECTED`

## 9. Header/title is a separate cause-family

The runtime screenshot for `아시가루 대장의 주명` shows the top-left help title wrapping into two lines.

This is not classified as the same defect as the body overflow.

Switch B24 title-object construction evidence:

```text
mapped 0x21F1B8   title rect setup
  x      16
  y      46
  width  306
  height 34

mapped 0x21F1D4
  w6 = 5

mapped 0x21F1E8
  text-object constructor
```

Switch B24 body-object construction differs:

```text
mapped 0x21F63C
  geometry argument = 788

mapped 0x21F650
  w6 = 4

mapped 0x21F658
  text-object constructor
```

The PC Korean patch has separate runtime descriptors:

```text
description_font_1   5 -> 4
description_font_2   5 -> 4

ui_width_1           170 -> 200
ui_width_2           170 -> 200
ui_width_3           170 -> 200
ui_width_4           150 -> 200
```

The B24 title `w6 = 5` is a strong semantic counterpart candidate for the PC description-font family, but the exact complete Switch counterpart set is not yet closed.

Do not patch `0x21F1D4` alone from numeric coincidence.

## 10. 확정된 사실

1. The exact V317 package reaches Eden and displays the V315 B24 payload.
2. M227 semantic repair is visibly correct.
3. M228 semantic/title text is visibly correct, but its help header wraps incorrectly.
4. M229 군자금 조달 semantic repair is visibly correct.
5. Long B24 bodies can render below the fixed white help panel.
6. V315's B24 40-unit hard-wrap model produces excessive authored line counts for this caller.
7. Official JP/SC/TW B24 families allow authored lines wider than 40 units and cap at 12 authored lines in the audited M221..M344 range.
8. Switch has native renderer wrapping; B24 does not require 40-unit pre-wrap.
9. The right-side B24 scrollbar is not established as an intra-message long-text scroll mechanism.
10. B24 body layout and help-header width/font are separate cause-families.
11. PC patch runtime descriptors include four UI-width changes and two description-font 5->4 changes that are relevant reference evidence for the header family.

## 11. 유력한 가설

### Body family

The B24 long-body runtime failure is caused by V315 introducing too many sentence-internal hard newlines under an incorrect 40-unit caller model.

A reconstruction that keeps semantic/section boundaries while relying on native auto-wrap is the leading repair design.

### Header family

The B24 title-wrap failure most likely belongs to a Switch counterpart of the PC `description_font_1/2` and/or `ui_width_1..4` descriptor families.

The exact Switch counterpart set is not yet established.

## 12. 미확정 사항

- the exact B24 native-wrap reconstruction contract for all 108 V315 layout rows;
- final visual-line count for every reconstructed B24 message;
- whether a caller-specific safety margin below the observed 12 authored-line source maximum is required;
- the exact complete Switch counterpart set for PC `description_font_1/2`;
- the exact complete Switch counterpart set for PC `ui_width_1..4`;
- whether title correction needs font-selector, width, or both;
- physical Nintendo Switch / Atmosphere behavior.

## 13. 기각된 가설

Rejected for the B24 runtime symptom:

- B24 viewport/clipping failure is the primary cause;
- the right-side scrollbar should scroll an overlong individual message body;
- every B24 authored line must be <= 40 units;
- restoring JP `0x1B48 / 0x1B4B` is the body-overflow fix;
- M227/M229 semantics caused the runtime overflow;
- patching only the visibly overflowing subset is sufficient;
- patching B24 title `w6=5 -> 4` immediately from numeric coincidence is safe.

## 14. 관련 영향 범위

Two cause-families are now isolated.

### A. B24 body-layout family

Population:

`the 108 V315 layout-reconstructed B24 rows`

Semantic payload corrections for M227/M228/M229 remain preserved.

Required next work:

- design a native-wrap reconstruction rule;
- regenerate the full 108-row common-cause family together;
- evaluate authored and simulated visible line counts;
- do not mix header/runtime-descriptor edits into the same diagnostic build.

### B. B24 help-header family

Current evidence:

- long Korean help title visibly wraps;
- B24 title object uses `w6=5`;
- B24 body object uses `w6=4`;
- PC patch has `description_font 5->4` and UI-width descriptor families.

Required later work:

- enumerate all same-semantic Switch counterparts;
- establish preimages/call ownership;
- only then design a separate header diagnostic patch.

## 15. 수정 제안 / next scopes

Priority next executable scope:

`TAI5MSG_B24_NATIVE_WRAP_LAYOUT_RECONSTRUCTION_DESIGN_READ_ONLY`

That scope is body-only and must not patch or build.

Queued separate cause-family:

`B24_HELP_HEADER_PC_DESCRIPTOR_SWITCH_COUNTERPART_SURVEY_READ_ONLY`

Do not combine the body and header families into one diagnostic build.

Ordinary non-B24 584-row reflow remains deferred and is not authorized by V318.

## 16. Historical authority correction

For B24 only, this V318 document takes precedence over the following earlier claims where they conflict:

- V315: `all corrected lines <= 40 units` as a correctness criterion;
- V316/V317: any runtime expectation derived from that B24 40-unit criterion.

The exact V315/V317 byte identities remain valid historical artifact identities.

## 17. Repository write boundary

Any later repository write remains restricted to:

`create_blob -> create_tree -> create_commit -> update_ref(force=false)`
