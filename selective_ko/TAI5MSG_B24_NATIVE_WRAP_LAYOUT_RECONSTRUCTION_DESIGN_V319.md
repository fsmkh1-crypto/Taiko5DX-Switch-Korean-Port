# TAI5MSG B24 Native-Wrap Layout Reconstruction Design — V319

Date: 2026-09-18 (KST)

Validation ID: `V319`

Parent canonical state:

`98da5742d6f4ab5bb0994d093797f1710c5176d2` — V318 B24 V317 Eden runtime root-cause closure.

Status:

`CLOSED / DESIGN ONLY / B24 BODY 108-ROW NATIVE-WRAP CONTRACT FROZEN / NO PRODUCT BYTES CHANGED`

## 1. Scope

V319 freezes the body-only reconstruction contract for the 108 B24 rows whose V315 layout reconstruction used the now-superseded 40-unit hard-wrap model.

V319 does not modify TAI5MSG, serializer code, correction artifacts, IPS, font, package ZIP, or runtime state.

The B24 help-header/title family remains explicitly out of scope.

## 2. Inherited facts

V318 established:

- the V315 B24 40-unit correctness model is invalid for this caller;
- Switch B24 uses native renderer wrapping;
- B24 long-body overflow is caused by excessive sentence-internal hard newlines from V315;
- M227/M228/M229 semantic corrections remain valid;
- help-header wrapping is a separate cause-family.

The V315 109-row correction artifact remains historical provenance and semantic authority where V318 did not supersede it.

## 3. Exact B24 native width

Read-only Switch renderer analysis binds the body width to exact pixel geometry.

```text
B24 body geometry width       788 px
font-index-4 two-byte advance  30 px
font-index-4 one-byte advance  15 px

52 half-width units = 780 px   FIT
53 half-width units = 795 px   WRAP
```

Therefore:

`B24_NATIVE_LINE_WIDTH = 52 half-width units`

This is not an inferred convenience threshold. It is the caller-specific width bound derived from Switch geometry and renderer advance.

## 4. Official-language corroboration

The audited official B24 M221..M344 source families remain consistent with the 52-unit caller model:

```text
                 max authored lines   max authored width
JP                       12                  52
SC                       12                  52
TW                       12                  52
```

Official B24 data contains many authored lines wider than 40 units, so the former 40-unit B24 model remains superseded.

## 5. Reconstruction population

Exact body-layout population:

`108 rows`

These are the V315 rows classified as body/control-layout reconstruction cases.

The following are preserved:

- M227 semantic recovery;
- M228 semantic/title payload recovery;
- M229 군자금 조달 semantic recovery;
- semantic text token order;
- control/style order required by the localized payload;
- terminal `05 05 05`;
- candidate/classification membership.

The 15 untouched B24 rows remain untouched.

## 6. Binding reconstruction algorithm

For every one of the 108 rows:

1. use the V315 corrected semantic/control payload as the starting semantic authority;
2. preserve section starts and semantic structure;
3. join sentence-internal continuation lines introduced only by the V315 40-unit hard-wrap;
4. retain hard boundaries for:
   - `●` section starts;
   - `◆` section starts;
   - `※` note starts;
   - deliberate semantic blank-section boundaries;
   - required style/control boundaries;
5. reflow ordinary paragraph text at `52 half-width units`;
6. select the last legal whitespace boundary that keeps the line at or below 52 units;
7. never split inside a Korean whitespace-delimited token when a prior legal boundary exists;
8. preserve the existing full-width paragraph indent convention on wrapped continuation content where required by the B24 body grammar;
9. treat Switch native auto-wrap as a safety net rather than the primary Korean word-break mechanism;
10. require final simulated visible line count `<= 12`.

No translation shortening is permitted merely to satisfy layout.

## 7. Decorative-blank exception rule

A full 108-row dry-run showed:

```text
105 rows  <= 12 visual rows directly
3 rows    = 13 rows before decorative-blank normalization
```

The three rows are:

`B24:M221 / B24:M257 / B24:M320`

All three share the same long 修業 / 수업-family structure and contain a decorative blank line between the preamble and the first `●` section.

For these rows, and only when the generic post-reflow result exceeds the 12-row envelope, the following normalization is allowed:

`remove one purely decorative blank line between preamble and first ● section`

After this normalization:

```text
M221   13 -> 12
M257   13 -> 12
M320   13 -> 12
```

No semantic text, punctuation, section title, control, or terminator is removed.

This is one shared structural rule, not three locator-specific translation edits.

## 8. Full-population dry-run result

The V319 design dry-run over all 108 target rows produced:

```text
layout population                         108 / 108
semantic byte/token order preserved       PASS 108 / 108
required control order preserved          PASS 108 / 108
terminal 05 05 05 preserved               PASS 108 / 108
line width > 52                              0
forced Korean token split                    0
predicted extra native auto-wrap              0
final simulated visual rows > 12              0
```

This closes the design requirement for a single common-cause body-layout rule.

## 9. Representative M221 design result

The resulting structure for M221 is conceptually:

```text
신분이 아시가루 조두일 때 받을 수 있는 주명입니다.
●수업
 수업을 통해 주인공의 기능 수준을 높입니다.
◆달성 방법
 기능을 가르칠 수 있는 인물이 있는 시설을 찾아가
 사사받습니다. 기능을 많이 올릴수록 평가도
 높아집니다. 사사받을 시설은 기능마다 다릅니다.
 아시가루, 궁술, 군학, 건축, 광산, 변설은 무가
 저택이나 민가, 기마는 마구간, 철포는 대장간,
 수군은 요새 수련장, 무예는 도장, 인술은 닌자 마을
 수련장, 개간은 남만사, 산술은 상가, 예법은 절,
 다도는 다인 저택, 의술은 의사 저택입니다.
```

This is a design rendering, not a new committed payload.

## 10. Prospective serializer postconditions

Applying the V319 design to the current V315 body-layout population produced the following dry-run projections:

```text
B24 used_end       0xECA5 -> 0xEB7C
B24 declared       0xECC0 -> 0xEB80
B24 growth         0x08C0 -> 0x0780

whole-file size    0x1C13C9 -> 0x1C1289
whole-file growth  0x7200   -> 0x70C0
B32 offset         0x1B4980 -> 0x1B4840
```

Prospective dry-run SHA-256:

`fd4c8b9f527f67f667d5fded6bdb4703607b70e8b6addf1f41c5d11ebf93e85c`

These values are **design projections only**.

They are not canonical output identities until an independently guarded implementation/materialization run reproduces them.

## 11. Header/title isolation

V319 does not alter the help-header/title family.

The separate queued scope remains:

`B24_HELP_HEADER_PC_DESCRIPTOR_SWITCH_COUNTERPART_SURVEY_READ_ONLY`

Do not combine:

- body-layout TAI5MSG changes; and
- description-font/UI-width runtime descriptor changes

in the same diagnostic build.

## 12. Non-B24 isolation

The ordinary non-B24 584-row reflow family remains unchanged and deferred.

V319 does not authorize using the B24 52-unit width for B17..B23 callers.

Every caller family requires its own bound.

## 13. 확정된 사실

1. B24 body width is 788 px.
2. Font-index-4 advance is 30 px for two-byte glyphs and 15 px for one-byte glyphs.
3. The exact B24 half-width-unit bound is 52.
4. Switch native wrapping is active for the B24 body route.
5. A 52-unit word-boundary reconstruction covers all 108 V315 layout rows.
6. 105/108 fit the 12-row envelope directly.
7. M221/M257/M320 fit after the same decorative-blank normalization rule.
8. No translation shortening is required.
9. No Korean token must be split.
10. M227/M228/M229 semantic corrections remain preserved.

## 14. 유력한 가설

A V319-conformant implementation should eliminate the V317 long-body overflow without changing renderer code, font bytes, Mapping 10,036, or B24 semantic content.

This remains a runtime hypothesis until an implementation and isolated Eden diagnostic build are executed.

## 15. 미확정 사항

- byte-exact implemented output identity;
- whether implementation reproduces the prospective SHA exactly;
- Eden visual confirmation for long representative rows after V319 implementation;
- physical Switch/Atmosphere behavior;
- independent help-header/title fix.

## 16. 기각된 가설

Rejected:

- B24 should use the ordinary 40-unit model;
- renderer-only wrapping with arbitrary Korean syllable breaks is the preferred design;
- only the 20 currently overflowing rows should be patched;
- 108 rows require manual one-by-one edits;
- Korean prose must be shortened to fit;
- M221/M257/M320 need locator-specific translation exceptions;
- header/title runtime edits should be mixed into the body diagnostic build.

## 17. 관련 영향 범위

Authorized future implementation population:

`B24 body layout 108 rows only`

Preserve:

- M227/M228/M229 semantics;
- 15 untouched B24 controls;
- all non-B24 selected rows;
- Mapping/font/page-mapper route;
- ExeFS runtime code for the body-only diagnostic.

## 18. 수정 제안 / exact next scope

After a new explicit execution signal:

`TAI5MSG_B24_NATIVE_WRAP_LAYOUT_RECONSTRUCTION_IMPLEMENTATION_OFFLINE_VALIDATION`

That scope may:

1. materialize a new guarded correction overlay for the 108 B24 body rows;
2. update the selective serializer and bounded tests;
3. reparse all 14,832 messages;
4. verify only the intended 108 body-layout locators differ from the current semantic authority, except the already-existing semantic corrections that must be preserved;
5. validate 52-unit / 12-row invariants;
6. establish canonical byte-exact output identity;
7. stop before package/IPS/Eden runtime materialization.

The help-header/title family remains excluded.

## 19. Repository write boundary

Any repository write remains restricted to:

`create_blob -> create_tree -> create_commit -> update_ref(force=false)`
