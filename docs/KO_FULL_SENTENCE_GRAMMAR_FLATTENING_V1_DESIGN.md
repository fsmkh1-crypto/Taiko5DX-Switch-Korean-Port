# KO Full-Sentence Grammar Flattening V1 Design

Date: 2026-09-16 (KST)
Status: CANONICAL READ-ONLY DESIGN DIRECTION — ADVERSARIAL REVIEW INCORPORATED
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

The adversarial review narrows the authority of this reference:

- SC/TW proves an engine-compatible structural flattening model;
- SC/TW does not decide how much Korean speech register or character tone may be
  collapsed;
- Korean tone/register disposition must be made from JP meaning, actual PC Korean text,
  caller control flow, and the Korean sentence itself.

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
changes semantic content or required speaker register rather than only redundant
segmentation, that distinction must be retained in caller control flow, another dynamic
value, or an explicit exception.

### 5.4 Full-sentence does not mean fully static

A flattened Korean sentence may still contain dynamic semantic calls inside it.

Desired model:

```text
localized Korean sentence structure
  + dynamic name/address/value insertion where semantically required
  + caller-local style/control branches where already present
  - inherited Japanese inflection-only formatter dependency
```

This is the central difference between full-sentence grammar flattening and global
removal of all block-0 calls.

## 6. Migration safety rules

No formatter family may be globally blanked or disabled first.

Required order for each grammar family/caller population:

```text
1. census every external caller
2. classify each caller by semantic responsibility
3. classify formatter branches as style-only vs semantic/tone-bearing
4. preserve the caller's existing control/branch skeleton
5. preserve required dynamic semantic calls and their order
6. design branch-local natural Korean full-sentence wording
7. explicitly adjudicate any nested register/tone that would disappear
8. migrate only the complete proven caller set
9. enumerate residual callers explicitly
10. only when residual obligations are zero or documented exceptions remain,
    consider retiring/emptying the now-unused grammar literal family
11. run structural/locator/capacity/provenance gates before any build
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
4. preservation of caller-owned speech-style/control branches;
5. explicit review before any nested formatter register/tone is collapsed.

All 42 grammar families observed in the completed census carry multiple Korean output
variants rather than one fixed output. Family output multiplicity is approximately
2–9 variants; representative families include:

```text
C73   입니다 / 이오 / 이다 / 이네 / 이옵니다 ...
C188  하겠습니다 / 하겠다 / 합니다 / 한다 / 하오 ...
C209  없습니다 / 없소 / 없네 / 없다 / 없사옵니다 / 없어요 ...
```

`0x6A` remains a real speech-style selector. Global inversion remains rejected.

SC/TW may collapse substantial inherited Japanese grammar variation, but Korean does
not copy that collapse mechanically. Important characters/events may require
`TONE_CRITICAL_EXCEPTION` handling when nested formatter register carries a distinction
that caller-local control does not already preserve.

## 8. Prohibited repair paths

Do not use any of the following as the design:

- sentence-by-sentence patching only where a malformed screenshot was observed;
- global `하하 -> 하`;
- global `이이 -> 이`;
- repeated-syllable or longest-overlap deduplication;
- direct suffix deletion;
- fixed left/right boundary trimming based only on identical Hangul syllables;
- forced C8:87 result;
- global `0x6A` inversion;
- removing the first Korean syllable from C73/C188 as a universal fix;
- globally blanking C73/C188 or the C65..C358 grammar cluster before every caller is
  migrated/accounted;
- preserving Japanese segmentation merely because PC Korean v1.02 preserved it;
- treating official SC/TW as a Korean tone/register oracle;
- treating the former 913 structurally-direct callers as automatic migration authority;
- requiring recovery of the unavailable exact PC v1.02 target EXE before Korean design
  can proceed.

## 9. Completed whole-family classification

The externally used block-0 entry population is now closed at read-only census level:

```text
external entry families             73
GRAMMAR_FLATTEN families             42 / 2,364 KO external calls
DYNAMIC_MEANING_RETAIN families      31 / 4,254 KO external calls
MIXED_SPLIT_REQUIRED families         0
UNRESOLVED families                   0
TOTAL external calls              6,618
```

The recursive internal block-0 graph reachable from the 42 grammar entry families
covers exactly `C65..C358`, 294 nodes. No internal edge crosses from that grammar
cluster into the retained dynamic-semantic clusters around `C12..C64` and `C403+`.

The 2,364 grammar calls occur in exactly 1,013 non-block-0 caller messages. Of those,
386 callers also contain dynamic-semantic calls. Family-level separation is therefore
clean, while caller-level semantic preservation remains mandatory.

## 10. Caller migration matrix — structural census

The first migration-matrix census produced:

| class | callers | grammar edges | disposition |
|---|---:|---:|---|
| `DIRECT_STATIC_FLATTEN` | 591 | 1,252 | structural reference only; automatic authority superseded |
| `DIRECT_DYNAMIC_PRESERVE` | 322 | 835 | structural reference only; automatic authority superseded |
| `CN_SEMANTIC_DIVERGENCE_REVIEW` | 42 | 168 | explicit semantic review |
| `GRAMMAR_RESIDUAL_EXCEPTION_REVIEW` | 58 | 109 | explicit residual review |
| **TOTAL** | **1,013** | **2,364** | |

For the former 913 structurally-direct callers, SC and TW both remove grammar calls and
preserve Korean dynamic-meaning call ID/order where such calls exist.

Across all 1,013 callers, the compared JP/KO/SC/TW branch-marker sequence remains
structurally identical. This establishes the migration invariant:

`preserve existing caller control/branch skeleton`

Within the 58 residual-exception callers, 22 are C314-only structural/no-op-like
residuals and 36 remain true branch-level exception cases.

The words `DIRECT_STATIC_FLATTEN` and `DIRECT_DYNAMIC_PRESERVE` no longer imply direct
automatic migration. They describe only the initial structural reference relation to
SC/TW and are superseded for execution ordering by the adversarial review below.

## 11. Adversarial review — speech-style ownership correction

The 1,013 grammar callers divide by direct caller-level `0x6A` style/control presence:

```text
caller has direct 0x6A style branch       601 / 1,494 grammar edges
caller has no direct 0x6A style branch    412 /   870 grammar edges
```

Within the former 913 structurally-direct callers:

```text
CALLER_STYLE_BRANCH_AVAILABLE             567 / 1,356 grammar edges
STYLE_COLLAPSE_REVIEW                     346 /   731 grammar edges
TOTAL                                     913 / 2,087 grammar edges
```

The earlier idea that all 913 could move directly to automatic flattening is rejected.

`CALLER_STYLE_BRANCH_AVAILABLE` means only that the caller already has explicit
style/control branching that can serve as the first detailed migration-design tranche.
It does not itself authorize text mutation. Each existing branch must remain, and each
branch must receive a natural Korean full-sentence design while required dynamic values
remain dynamic.

`STYLE_COLLAPSE_REVIEW` means nested formatter register/tone could disappear because the
caller does not directly expose the same style branch. Those 346 callers must not be
auto-flattened. Shared-message ownership, speaker use, relationship/register meaning and
possible `TONE_CRITICAL_EXCEPTION` disposition must be reviewed first.

## 12. Adversarial review — composition and morphology boundary

A simple adjacency census across the 2,364 grammar edges found:

```text
left-side stored overlap present        604 edges
right-side Hangul continuation present  728 edges

left only                                458
right only                               582
both                                     146
neither                                1,178
```

Thus at least 1,186 grammar edges across 601 callers show direct visible composition
coupling. These counts are lower-bound risk/shape evidence, not a rewrite classifier.

Korean morphology makes simple overlap detection insufficient. For example, C109 can
produce forms such as:

```text
했습니다 / 했다 / 했사옵니다 / 했어요
```

while callers can already contain forms/stems such as:

```text
기다리셨 + C109
기다렸 + C109
실패했 + C109
```

The grammatical responsibility overlaps even when adjacent stored syllables are not
identical. Therefore deduplication, prefix stripping, suffix stripping, or a fixed
byte/syllable boundary rule cannot close the family safely.

## 13. Revised migration contract and current STOP boundary

The core design remains unchanged:

`preserve dynamic meaning / flatten inherited Japanese dynamic grammar`

The reviewed execution contract is now:

```text
preserve caller control/branch skeleton
preserve required dynamic semantic call IDs/order
flatten inherited Japanese grammar segmentation into branch-local natural Korean
never collapse nested formatter register/tone implicitly
explicitly classify STYLE_COLLAPSE_REVIEW / TONE_CRITICAL_EXCEPTION where required
use SC/TW as structural evidence only, not Korean wording/tone authority
```

The preferred first detailed matrix is the 567 callers already carrying caller-level
style/control branching:

`KO_GRAMMAR_FLATTEN_CALLER_STYLE_BRANCH_AVAILABLE_567_MATRIX_READ_ONLY`

That next scope may enumerate each caller, grammar-edge occurrence, branch ownership,
dynamic-semantic obligations, speaker/tone obligations, and post-migration invariants.

It may not rewrite Korean text, mutate TAI5MSG, modify the builder, generate IPS, create
a diagnostic build, patch runtime code, or add WRITE_SAFE authority.

A fresh explicit user execution signal is required before beginning the 567-caller
matrix.

## 14. V282-V284 narrowing and Korean V1 tone policy

Later read-only closures narrow the execution interpretation of sections 11-13 without
changing the core design.

V282 partitions the 567 caller-style population into:

```text
ROOT_STYLE_ONLY                         253 callers / 406 grammar edges
ROOT_STYLE_PLUS_SECONDARY               207 callers / 657 grammar edges
NESTED_STYLE_BEFORE_ALL_GRAMMAR          64 callers / 166 grammar edges
PRE_STYLE_GRAMMAR_MIXED                  43 callers / 127 grammar edges
TOTAL                                   567 callers / 1,356 grammar edges
```

V283 proves that preserving caller `0x6A` does not reproduce all nested formatter tone
conditions. Across the 460 root-style-owner callers, complete caller coverage of nested
formatter relation/register conditions is 0/460. Therefore all 460 require explicit
tone-collapse adjudication before text migration.

V284 establishes the first reusable Korean tone policy from the least noisy 253
`ROOT_STYLE_ONLY` callers:

```text
callers                                  253
grammar edges                            406
dynamic callers                           91
dynamic-semantic edges                   226
simple two-arm 0x6A callers              250
of those, one arm already grammar-free   210
grammar edges in opposite arms           290
```

The 210/250 corpus pattern is direct PC Korean evidence that branch-local complete
Korean wording is already used inside the same caller structures.

All 34 grammar entry families used by this tranche are assigned to four policy classes:

```text
REGISTER_NORMALIZE_CANDIDATE
  C73 C82 C100 C109 C118 C195 C202 C209 C244 C272 C279 C286 C300 C328 C335

LEXICAL_MOOD_REWRITE_REQUIRED
  C125 C132 C146 C160 C174 C181 C188 C216 C223 C230 C237 C251 C265

ZERO_OUTPUT_STRUCTURAL_EXCEPTION
  C91 C342

HONORIFIC_ROLE_TONE_CRITICAL
  C167 C258 C349 C356
```

Edge/caller coverage in the 253 population:

```text
REGISTER_NORMALIZE_CANDIDATE       241 edges / 174 callers
LEXICAL_MOOD_REWRITE_REQUIRED      109 edges /  92 callers
ZERO_OUTPUT_STRUCTURAL_EXCEPTION    42 edges /  37 callers
HONORIFIC_ROLE_TONE_CRITICAL        14 edges /   9 callers
```

Because callers can use more than one class, highest-risk caller assignment is used for
execution ordering:

```text
pure REGISTER_NORMALIZE_CANDIDATE   125 callers
LEXICAL_MOOD_REWRITE_REQUIRED        86 callers
ZERO_OUTPUT_STRUCTURAL_EXCEPTION     33 callers
HONORIFIC_ROLE_TONE_CRITICAL          9 callers
TOTAL                                253 callers
```

Korean V1 tone policy is now:

1. preserve caller-owned `0x6A` and all caller-local control branches;
2. preserve required dynamic-semantic call IDs/order;
3. normalize formatter-only simple register variation into natural branch-local Korean;
4. do not mechanically rewrite request/intention/proposal or lexical-mood families;
5. isolate C91/C342 empty/non-empty output behavior as structural exceptions;
6. preserve/review `-시-`, `말씀-`, `드리-` and similar honorific-role distinctions as
   `TONE_CRITICAL_EXCEPTION` obligations;
7. never assign a global Korean tone meaning to `0x6A=0` or `0x6A=1`; caller wording is
   the local tone authority;
8. use SC/TW only as structural evidence, not Korean wording/tone authority.

V284 does not authorize text mutation. The exact next read-only scope is:

`KO_GRAMMAR_REGISTER_NORMALIZE_CANDIDATE_125_BRANCH_WORDING_READ_ONLY`

Only after that wording-responsibility design is reviewed may any implementation or
write-safety stage be proposed, and such a stage requires a fresh explicit signal.