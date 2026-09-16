# KO Full-Sentence Grammar Flattening V1 Design

Date: 2026-09-16 (KST)
Status: CANONICAL READ-ONLY DESIGN DIRECTION
Scope ID: `KO_FULL_SENTENCE_GRAMMAR_FLATTENING_V1`
Implementation authorization: NONE
Build authorization: NONE
New WRITE_SAFE authorization: 0

## 1. Purpose

This document fixes the current Korean dialogue-formatter design direction after the
issue-C investigation exposed a structural responsibility collision between Korean
caller text and the inherited Japanese dynamic grammar formatter families.

The goal is not to hide malformed outputs one sentence at a time. The goal is to
define a Korean localization model that keeps genuinely dynamic semantic values while
removing Japanese-language grammar segmentation where that segmentation conflicts with
natural Korean sentence construction.

The design name is:

`KO_FULL_SENTENCE_GRAMMAR_FLATTENING_V1`

Core rule:

`preserve dynamic meaning / flatten inherited Japanese dynamic grammar`

This document is a design authority only. It does not authorize TAI5MSG rewriting,
builder implementation, IPS generation, runtime hooks, translation changes, or a
build.

## 2. Evidence and provenance boundary

### 2.1 TAI5MSG source identities

The comparison basis is the actual game/localization data:

```text
JP original TAI5MSG_JP.DAT
  size    1,810,889
  sha256  aae037dd5948f79b9fc2e5affcb1e60e08efca39f897123045fe685786be978f

PC Korean v1.02 TAI5MSG_JP.DAT
  size    2,134,366
  sha256  e3b4522a1047ff409e099b5ee197d7689279ea7472cb403d305b2507fec96090

Official SC TAI5MSG_SC.DAT
  size    1,918,773
  sha256  04ff8afe290b12f2f7b93e174952f5c7550acff1ef0fe17b96d889170e0a706e

Official TW TAI5MSG_TW.DAT
  size    1,944,333
  sha256  bf165a3f30b72045ea5f92e5acca45a950be4d94294cc10e82576f3fffcb0294
```

The earlier PC-original -> PC-Korean graph-diff closure remains valid: all 471
block-0 formatter messages preserve the control/graph skeleton while Korean literal
fragments replace Japanese output fragments.

### 2.2 Exact PC v1.02 runtime limitation

The exact PC executable required by Korean patch v1.02 is not available in the project
corpus and must not be searched for again merely to continue this design.

The v1.02 patch requires:

```text
expected EXE size    18,685,960
expected EXE sha256  10C69BAB50D29BAF6311360CAFBF7383716A126A6484D209F5E299E12AB565A2
```

The Drive `Taiko5DX.exe` previously inspected during the formatter investigation is a
different build of size 18,479,304 bytes. Therefore any conclusion that used that
binary to assert exact v1.02 PC `0x43/0x4A` cursor/return parity is not canonical
runtime proof.

Disposition:

- the wrong-build disassembly may remain structural background only;
- exact v1.02 PC runtime cursor/return parity is `UNAVAILABLE / UNPROVEN`;
- do not revive a search for the missing target EXE;
- this limitation does not block a Switch-native Korean data design based on verified
  TAI5MSG semantics and official JP/SC/TW localization structures.

## 3. Problem definition

Representative malformed Switch outputs include:

```text
조금 과음한 모양이이오군
오늘은 이만 실례하하겠습니다
야규님입니다인가
```

The first two demonstrate the responsibility collision directly.

Actual PC Korean v1.02 data contains caller/formatter boundaries equivalent to:

```text
caller:    조금 과음한 모양이
formatter: C73 family -> 이오 (through the relevant nested branch)
suffix:    군
result under direct composition: 모양이 + 이오 + 군

caller:    오늘은 이만 실례하
formatter: C188 family -> 하겠습니다 (through the relevant nested branch)
result under direct composition: 실례하 + 하겠습니다
```

The Korean formatter fragments are not isolated anomalies. Representative block-0
families already contain complete Korean inflectional forms:

```text
C73 family   입니다 / 이다 / 이옵니다 / 이오 / 이네 ...
C188 family  합니다 / 한다 / 하오 / 하겠습니다 ...
C209 family  없습니다 / 없다 / 없사옵니다 / 없어요 ...
C125 family  주십시오 / 주게 / 주세요 ...
C272 family  왔습니다 / 왔소 / 왔다 / 왔어요 ...
C244 family  이었습니다 / 이었다 / 이었사옵니다 / 이었어요 ...
C202 family  있습니다 / 있다 / 있사옵니다 / 있어요 ...
```

At the same time, Korean caller text may already own the copular or verbal stem.
Corpus evidence includes:

```text
C73 calls with immediate caller code for `이` before the call    97
C188 calls with immediate caller code for `하` before the call   66
```

These counts are risk/shape evidence, not automatic rewrite counts. They prove that
caller/formatter responsibility overlap is a family-level design issue rather than a
single `이이` or `하하` typo.

## 4. Official SC/TW structural reference

Official simplified/traditional Chinese data provides a same-engine localization
reference. It is not treated as a Korean translation oracle; it is used to understand
which inherited formatter responsibilities can be flattened safely at the data-model
level.

External calls from blocks other than block 0 to block-0 targets show:

```text
JP original   6,618
PC Korean     6,618
Official SC   4,233
Official TW   4,263
```

Selected family counts:

| target | JP | KO | SC | TW | current interpretation |
|---|---:|---:|---:|---:|---|
| C73  | 660 | 660 | 13 | 21 | grammar / copula-register family |
| C188 | 155 | 155 | 1 | 1 | grammar / `하다`-register family |
| C342 | 154 | 154 | 0 | 0 | grammar / copula family |
| C209 | 264 | 264 | 1 | 3 | grammar / `없다` family |
| C125 | 192 | 192 | 1 | 1 | grammar / command/register family |
| C272 | 84 | 84 | 0 | 0 | grammar / `오다` inflection family |
| C244 | 76 | 76 | 1 | 1 | grammar / past-copula family |
| C202 | 73 | 73 | 2 | 4 | grammar / `있다` family |
| C51 | 1,278 | 1,278 | 1,255 | 1,255 | predominantly dynamic address/relationship value |
| C27 | 1,217 | 1,217 | 1,196 | 1,205 | predominantly dynamic pronoun/address value |
| C16 | 1,001 | 1,001 | 966 | 970 | predominantly dynamic first-person value |
| C58 | 317 | 317 | 317 | 317 | retained dynamic semantic value family |

The pattern is structural and strong: SC/TW removes most calls to inflectional grammar
families while retaining most dynamic semantic-value families.

For the representative grammar nodes, official SC/TW also empties the variable grammar
literal outputs themselves: for example C68 retains only control structure and C184 is
only the control/end sequence. The corresponding localized caller messages absorb the
sentence wording instead of reproducing Japanese-style grammar fragments.

Therefore official SC/TW demonstrates that the game format supports a localization
strategy in which Japanese grammar-generator dependencies are largely flattened into
localized caller sentences while dynamic semantic inserts remain dynamic.

## 5. Korean responsibility model

### 5.1 Single-owner rule

A Korean grammatical unit must have one owner.

Do not allow both caller and formatter to own the same copula, verbal stem, tense,
politeness ending, or final ending boundary.

Examples of invalid overlapping ownership:

```text
caller owns 이 + formatter owns 이오
caller owns 하 + formatter owns 하겠습니다
```

### 5.2 Dynamic meaning stays dynamic

Keep calls whose runtime result changes the semantic referent/value of the sentence,
for example names, relationship/address forms, pronouns, person-dependent values,
numbers, and other context values that cannot be replaced by one fixed Korean literal
without changing meaning.

The retained/flattened decision is made by semantic responsibility, not by block-0 ID
alone.

### 5.3 Japanese grammar generators are flattening candidates

A formatter whose principal responsibility is Japanese-language inflection/register
realization is a candidate for removal from Korean caller composition.

The caller is then translated/reconstructed as a natural Korean sentence with the
necessary grammatical material owned locally by that caller.

This does not mean that all branches may be discarded blindly. If a formatter branch
changes semantic content rather than only register/style, that semantic distinction
must be retained either in caller control flow, another dynamic value, or an explicit
exception.

### 5.4 Full-sentence does not mean fully static

A flattened Korean sentence may still contain dynamic semantic calls inside it.

Desired model:

```text
localized Korean sentence structure
  + dynamic name/address/value insertion where semantically required
  - inherited Japanese inflection-only formatter dependency
```

This is the central difference between full-sentence grammar flattening and global
removal of all block-0 calls.

## 6. Migration safety rules

No formatter family may be globally blanked or disabled first.

Required order for each grammar family:

```text
1. census every external caller
2. classify each caller by semantic responsibility
3. classify formatter branches as style-only vs semantic-bearing
4. design the natural Korean caller/full-sentence form
5. preserve any required dynamic semantic inserts
6. migrate the complete proven caller set
7. enumerate residual callers explicitly
8. only when residual obligations are zero or documented exceptions remain,
   consider retiring/emptying the now-unused grammar literal family
9. run structural/locator/capacity/provenance gates before any build
```

Shared physical messages, aliases, storage capacity, offsets, block growth and builder
reconstruction remain subject to the existing write-safety and provenance rules.
Target resolution or linguistic correctness alone is not WRITE_SAFE authority.

## 7. Speech-style policy

Japanese block-0 grammar families encode extensive register/speech-style variation.
Korean V1 prioritizes:

1. grammatical correctness;
2. natural Korean full-sentence construction;
3. preservation of semantic content and dynamic referents;
4. speaker tone where it can be retained without reintroducing unstable Japanese-style
   segmentation.

SC/TW is evidence that official localization may collapse substantial inherited
Japanese grammar variation. Korean does not have to copy that collapse mechanically,
but preserving every Japanese formatter branch is not a requirement if doing so
recreates structurally invalid Korean segmentation.

Important characters/events may later receive caller-level tone refinement after the
flattening model is structurally stable.

## 8. Prohibited repair paths

Do not use any of the following as the design:

- sentence-by-sentence patching only where a malformed screenshot was observed;
- global `하하 -> 하`;
- global `이이 -> 이`;
- repeated-syllable or longest-overlap deduplication;
- direct suffix deletion;
- forced C8:87 result;
- global `0x6A` inversion;
- removing the first Korean syllable from C73/C188 as a universal fix;
- globally blanking C73/C188 before every caller is migrated/accounted;
- preserving Japanese segmentation merely because PC Korean v1.02 preserved it;
- requiring recovery of the unavailable exact PC v1.02 target EXE before Korean design
  can proceed.

## 9. Family classification model for the next stage

Every externally used block-0 family must be classified into one of these buckets:

```text
GRAMMAR_FLATTEN
  Japanese inflection/register responsibility should move into Korean caller text.

DYNAMIC_MEANING_RETAIN
  result carries a runtime semantic referent/value and remains dynamic.

MIXED_SPLIT_REQUIRED
  family contains both semantic and grammar responsibilities and requires subfamily or
  branch-level separation before migration.

UNRESOLVED
  insufficient evidence; no rewrite authority.
```

Classification is whole-population analysis. A few representative callsites are not
sufficient to authorize a family rewrite.

## 10. Next scope and STOP boundary

Next read-only scope:

`DIALOGUE_FORMATTER_GRAMMAR_GENERATOR_FAMILY_CENSUS_AND_CLASSIFICATION_READ_ONLY`

That scope must:

- enumerate the externally used block-0 family population;
- bind caller counts and representative semantics;
- classify `GRAMMAR_FLATTEN / DYNAMIC_MEANING_RETAIN / MIXED_SPLIT_REQUIRED / UNRESOLVED`;
- identify the full caller population for each grammar candidate;
- record exceptions and semantic-bearing branches;
- produce no TAI5MSG rewrite, builder change, build, IPS, translation mutation, or new
  WRITE_SAFE authorization.

A fresh explicit user execution signal is required before beginning that census.
