# ECF00000 PC-KO SWITCH CODE / GLYPH / PRODUCT ADMISSION AUDIT — V325

Date: 2026-09-19 (KST)

```text
validation_id   V325
track           SWITCH_SELECTIVE_KOREANIZATION
scope_kind      READ_ONLY_ANALYSIS_CHECKPOINT
parent          b9f40519a8f043bb8871c4e3ef328ed29809b0ff / V324
product_bytes   UNCHANGED
code            UNCHANGED
build/package   NONE
repository      DOCUMENTATION_ONLY
```

This checkpoint closes the exact PC-Korean ECF00000.TS5 code/glyph infrastructure audit and narrows product admission. V324 structural parity and entrypoint-graph facts remain inherited.

## 1. Source / carrier state inherited

```text
Switch v1.1.3 ECF00000.TS5
size    931,936
sha256  bbaaff8dc552da17a49ea2e6ce49a76da662541ee22fdec7dc7933046430bf09
identity vs PC original  BYTE_EXACT

PC Korean ECF00000.TS5
size    1,156,480
sha256  0899bf81789acfbd243d43be209a8a3960933fa090960ac8c753c63f95f07bbe

entrypoints                782
Switch-interpreter walk    PASS 782/782
unique target commands     4,444
```

The carrier/loader/entrypoint compatibility problem is not the active blocker.

## 2. Visible-string population

The V324 walker was reused. Counts are physical, not duplicated entrypoint-path visits, unless explicitly stated.

```text
message commands 0x11/0x12/0x13       4,193
choice commands 0x15                     251
physical choice strings                    504
non-empty visible strings                4,691
Hangul-bearing visible strings           4,491
Hangul-bearing messages                  3,987
Hangul-bearing choices                 504/504
non-Korean message commands                206
```

Choice commands are structurally simple for this audit: all 504 physical choice strings are Korean-bearing and no choice string contains the inline escape/control population described below.

## 3. Exact Korean game-code closure

For Hangul-bearing visible EVENT payloads:

```text
unique Hangul game codes      907
Hangul code occurrences    83,933
present in Mapping 10,036     907 / 907
missing from Mapping             0
PUA usage                        0
lead pages                   EB..F7
deployed page-mapper domain  EB..F8
```

V306 already established direct non-empty glyph-cell closure for all 2,350 Mapping Hangul codes in the canonical Korean FONT_JPN.G1T. The EVENT population is a strict subset:

```text
EVENT Hangul codes          907
non-empty font glyph cells  907 / 907
missing glyph cells           0
```

Therefore ECF00000 does not require:

- Mapping 10,036 expansion;
- another Korean font page;
- PUA realization;
- a new EVENT-specific text-code mapping mechanism.

The existing canonical Korean font and page mapper are sufficient for this exact Hangul population.

## 4. Escape/control-bearing message population

PC-Korean EVENT visible message payloads contain backslash-prefixed runtime escape/control forms.

```text
escape/control occurrences             1,745
strings containing >=1 escape/control  1,108
unique escape/control surface forms      278
Hangul message strings with escape     1,096
Hangul message strings without escape  2,891
choice strings with escape                 0
```

Observed prefix families include `\#`, `\%`, `\A`, `\B`, `\C`, `\D`, `\E`, `\G`, `\M`, numeric forms, `\&`, `\>`, and `\=`.

These prefixes must not be globally interpreted as one semantic class such as person-name insertion. The actual runtime responsibility varies and requires bounded classification.

The product-admission consequence is:

```text
no-escape Hangul messages      2,891  primary static-candidate population
Hangul choice commands           251  / 504 strings
escape/control Hangul messages 1,096  dynamic/control classification required
```

Presence of an escape/control token alone is not a proof of unsafe Korean grammar. Absence of one is also not by itself a complete caller/owner safety proof.

## 5. Fixed-surface-particle population

Canonical policy authority remains `FIXED_PARTICLE_POLICY.md` / `FIXED_SURFACE_PARTICLE_V1`.

Exact explicit dual-form literals in PC-Korean ECF00000:

```text
은(는)    136
이(가)     75
을(를)     43
과(와)     14
와(과)     15
(으)로      4
----------------
total      287 occurrences
strings    243
```

Canonical first-release surfaces remain:

```text
은(는) / 는(은) -> 는
이(가) / 가(이) -> 가
을(를) / 를(을) -> 를
과(와) / 와(과) -> 와
(으)로 / 로(으) -> 로
```

For these explicit EVENT literals the encoded payload relation is also `6 bytes -> 2 bytes`, so the direct semantic-payload shrink is:

```text
287 * -4 = -1,148 bytes
```

This is not authorization for raw byte deletion. EVENT entrypoint offsets and enclosing length-bearing command structure must be regenerated/revalidated by an EVENT-aware serializer before any implementation.

An additional detector identified 118 strings where an escape/control token is immediately adjacent to a standalone-looking Korean particle-family surface. This is only a PARTICLE_RISK candidate set. It must not be globally rewritten because cases such as a following Korean lexical word can superficially match the detector.

## 6. Control/binary records inside message opcodes

Not every 0x11/0x12/0x13 physical record is ordinary visible prose.

```text
non-Hangul control-only / binary-style records   144
```

Those 144 command bytes are also present byte-exact in the PC original. Apparent Mapping misses observed when naively decoding certain sequences as text, including representatives such as `8017`, `8617`, `E61F` and trailing-high cases, are therefore not Korean-patch glyph defects.

Binding rule:

- do not force every 0x11/0x12/0x13 payload through a plain text-code decoder;
- preserve proven control/binary leaves structurally;
- Mapping/glyph closure applies to the actual Hangul visible-text population, not arbitrary VM bytes.

## 7. Identity policy interaction

Canonical `IDENTITY_IN_PROSE_V1` remains unchanged:

```text
dedicated identity presentation fields  KEEP_JP
runtime-inserted identity                KEEP_JP
authored Korean prose identity literals PRESERVE_AS_AUTHORED_KO
reverse substitution                     FORBIDDEN
```

Mixed Japanese runtime identity + Korean surrounding prose is an accepted first-release presentation tradeoff. It is not by itself a product-admission blocker.

Runtime insertion can still create particle/morphology responsibility. Such rows must use the existing EVENT taxonomy and fixed-particle applicability gate rather than pronunciation guessing.

## 8. Known malformed grammar strings

The exact static PC-Korean ECF00000 payload contains zero literal occurrences of the previously known malformed surfaces:

```text
모양이이오군       0
실례하하겠습니다   0
입니다인가         0
```

This only proves absence of those literal malformed surfaces in the static payload. It does not prove every runtime composition path grammatically safe.

## 9. Shared physical target impact

From V324, 20 target physical commands are revisited through shared entrypoint paths.

Current audit overlay:

```text
shared physical target commands   20
Hangul-bearing                    20
escape/control-bearing             2
explicit dual-particle-bearing     1
```

Shared physical ownership still requires compatible caller/surface responsibility before unconditional Korean admission. One safe caller is not global proof.

## 10. Product-admission verdict

Infrastructure:

```text
Switch/PC-original carrier parity        PASS
Switch interpreter structural walk       PASS 782/782
Mapping 10,036 closure                   PASS 907/907
page-mapper domain                       PASS
canonical Korean font glyph closure      PASS 907/907
PUA dependency                           NONE
```

Whole-file product admission:

```text
PC-KO ECF00000 exact whole-file AS-IS    DEFER
```

Reason: the remaining blocker is not transport, file size, mapping, or glyph availability. It is product classification of dynamic/control-bearing message responsibilities, shared physical targets, explicit fixed-particle normalization, and later layout QA.

The correct product route is selective EVENT reconstruction using PC-Korean content as source authority and the Switch VM/container as structural authority.

## 11. Rejected / do-not-repeat

Rejected for this ECF00000 population:

- EVENT requires Mapping expansion;
- EVENT requires additional Korean font pages;
- EVENT requires PUA support;
- apparent binary/control bytes that do not map as characters prove a PC-Korean payload defect;
- every 0x11/0x12/0x13 record is plain visible text;
- Japanese runtime identity insertion is automatically a product-policy violation;
- whole-file admission is blocked by Switch carrier/file-size/font infrastructure;
- all 118 escape-adjacent particle detector hits are automatically grammar defects;
- known malformed formatter strings being absent statically proves all dynamic grammar safe.

Do not reopen V324 entrypoint-partition hypotheses.

## 12. Related impact boundary

Unchanged:

- V320 B24;
- V321 package;
- TAI5MSG 3,179 product population;
- Mapping 10,036;
- Korean FONT_JPN.G1T;
- page mapper;
- SNR;
- identity/yomi KEEP_JP policy.

Newly narrowed EVENT work:

- 2,891 Hangul no-escape messages;
- 251 Hangul choice commands / 504 strings;
- 1,096 Hangul escape/control messages;
- 20 shared physical target commands;
- 243 explicit-dual-particle strings / 287 normalization occurrences;
- 144 control/binary-style message records that must not be treated as ordinary text.

Layout/reflow remains a separate QA cause-family. V324's manual-newline facts remain inherited.

## 13. Exact next scope

After a fresh explicit execution signal:

`ECF00000_SELECTIVE_COMMAND_ADMISSION_CLASSIFICATION_READ_ONLY`

Required bounded work:

1. classify the 2,891 Hangul no-escape messages;
2. classify the 251 choice commands / 504 strings;
3. classify the 1,096 Hangul escape/control messages by actual runtime responsibility;
4. carry shared-physical-owner constraints for the 20 shared targets;
5. identify exact `FIXED_SURFACE_PARTICLE_V1` eligible rows separately from broader particle-risk detectors;
6. derive only the canonical dispositions `INCLUDE_KO / DEFER_KO / KEEP_JP / UNRESOLVED / BLOCKED`;
7. do not implement an EVENT serializer, modify payloads, build/package, or perform unrelated EVENT/SNR work.

No gameplay bytes, builder, IPS, package, or runtime artifact is changed by V325.
