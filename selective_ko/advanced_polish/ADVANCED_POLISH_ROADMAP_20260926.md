# TAIKO5DX ADVANCED POLISH ROADMAP

Date: 2026-09-26 (KST)
Status: `ACTIVE_QUALITY_POLISH_TRACK / CANONICAL_RUNTIME_PRODUCT_IMMUTABLE`
Repository baseline at roadmap creation: `bc0582a3053b647ce009e8a1cfeed1f192473f72`

## 1. Immutable baseline

The current runtime-pass product is the fixed regression baseline. Quality work must never overwrite or silently replace it.

- active product: `ROOTCAUSE223_B23_REFLOW_V1`
- final TAI5MSG SHA-256: `1b44170a817e047ba942ba10e46571049ff7405c7fac4278c3e1598089efd61e`
- final IPS SHA-256: `28c423a0a8e805308f8e935f2a3f5304fe12e3f948ca6468c46dd72a96cdcfae`
- immutable runtime reference ZIP SHA-256: `cfd14031bab300929a9926bae9bb82bf28f21a9d417aee50ca527b88df873c91`
- runtime reference Drive ID: `1yCgjdWKQUTpwEfLll_Y29ztKG96EkXv2`
- runtime reference status: `USER RUNTIME OBSERVED PASS`

RootCause223, Buffer8, B23 and the superseded historical V371 partial track are not reopened merely for polish work.

## 2. Font A diagnostic — current state

User-selected visual direction:

- family: `Noto Serif CJK KR Bold`
- style goal: serif / myeongjo-like, not thin
- cell: `32x32`
- first raster candidate: `24 px`, glyph bottom around y=30
- proven Korean syllable oracle: PC patch `dinput8.dll` mapping, 2,350 Hangul syllables
- normal Hangul replacement pages: 49-61
- PUA 192 entries: preserve
- pages 0-48 and 62-63: preserve in first diagnostic

Diagnostic artifacts already produced outside Git:

- diagnostic ZIP: `TAIKO5DX_KR_ROOTCAUSE223_FONT_A_DIAGNOSTIC_20260926.zip`
- diagnostic ZIP SHA-256: `b29128b65337dd2d0aed3f58665598ebf006c2a1cf89904c0f09f291e8d8d63d`
- candidate FONT_JPN.G1T SHA-256: `c622ab750f3f539277488fd7c1a6e0288e345002c1a54fb7ad516b765bb4614e`
- scope: font file only; TAI5MSG / IPS / EVENT unchanged
- runtime status: `NOT YET CONFIRMED`

Next font action: user runtime check. If visually and functionally normal, record `FONT_A USER_RUNTIME_OBSERVED_PASS` before promoting it into a future polished product.

## 3. Remaining polish tasks — recommended execution order

The ordering below favors lower-risk / higher-clarity work first. Do not combine unrelated cause groups into one diagnostic build.

### P0 — Font A runtime closure

Goal:
- boot/load check
- dialogue readability
- small UI readability
- clipping / vertical alignment / excessive weight check

Implementation rule:
- no further font mutation until the current font-only diagnostic is observed on runtime.

### P1 — Awkward dialogue audit and correction

Known symptom class:
- obvious malformed Korean such as `나은`
- direct-translation residue
- awkward sentence endings
- honorific / archaic-style mismatch that is not a RootCause223 structural duplication bug

Required analysis before edits:
- scan the final product corpus rather than fixing screenshot sentences one by one
- classify by root cause: typo/lexical error, translation literalism, grammatical defect, register mismatch, runtime composition residue
- compare against actual PC Korean patch text first when available
- keep RootCause223 caller/helper structure intact unless direct evidence contradicts it

Preferred outcome:
- corpus-level correction ledger with common-rule groups plus a bounded manual-review residue.

### P2 — Untranslated Japanese / missing Korean audit

Observed surfaces include:
- fixed menu labels
- character/status UI
- tavern menu
- card/category/list UI
- scenario title/description
- names and place labels

Required classification:
- executable/static UI strings
- TAI5MSG messages
- EVENT text
- TR5 / G1T or other data carriers
- names/places handled by the separate name/place track

Do not treat all remaining Japanese as one carrier.

### P3 — Person and place names in Hangul, excluding world-map layout

Policy direction:
- preserve existing yomi/readings where the UI has a separate yomi field
- convert visible person/place names to Korean based on actual source readings/data, not guessed Sino-Korean readings
- do not infer names when PC patch or game data provides the reading

Required analysis:
- enumerate all display carriers and duplicated representations
- determine per-field byte/character capacity
- identify where the same entity appears in status UI, dialogue, lists, cards, locations and events

World-map labels are excluded from this phase.

### P4 — Terminology and notation normalization

Scope:
- ranks/titles
- skills/cards
- facility/location terminology
- recurring system vocabulary
- punctuation and spacing conventions
- person/place transcription policy

Rule:
- establish a glossary/normalization ledger before mass replacement.
- PC patch text is evidence, not an automatic quality authority when it is itself unnatural or inconsistent.

### P5 — Speech-register / character-voice polish

Goal:
- consistent polite/plain/archaic style according to role, relationship and scene
- eliminate mixed endings and unnatural register transitions

Required method:
- define reusable register classes and evidence from actual speaker/context
- avoid sentence-by-sentence arbitrary rewriting
- keep this separate from simple typo/direct-translation cleanup where possible

### P6 — World-map place-name Hangul and long-yomi layout

This is the highest-layout-risk localization task.

First questions to close:
- exact carrier/source for map labels
- renderer and width rule
- fixed coordinates / collision behavior
- truncation, scale or wrapping support
- whether different UI surfaces can safely use different display forms

Problem:
- yomi-based Korean labels can be substantially longer than 2-4 kanji labels.

Do not invent abbreviations before the actual map renderer and overlap constraints are measured.
A map-specific short display policy is allowed only if the technical need is proven and the full place name remains available elsewhere.

### P7 — Special/runtime QA

After text/data polish:
- minigames
- multi-choice branches
- rare events
- long descriptions
- list/table screens
- cards
- map labels
- special glyphs/PUA
- uncommon dialogue compositions

Diagnostics should isolate one cause group at a time.

## 4. Separate technical research item

### FONT page 63 / description-font path

Confirmed:
- page 63 contains Korean-looking glyph content.
- it is not part of the directly proven normal 2,350-syllable EB-F8 mapping used for Font A replacement.

Unresolved:
- exact runtime reachability
- relation to historical PC `description_font_1 / description_font_2` behavior

Rule:
- preserve page 63 until runtime/source evidence identifies its role.
- do not block P1-P5 on this research unless a symptom points to it.

## 5. Priority and dependency summary

```text
CURRENT
  P0 Font A runtime check

THEN, LOW-RISK FIRST
  P1 awkward dialogue audit
  P2 untranslated-text audit
  P3 names/places except world map
  P4 terminology normalization
  P5 speech-register polish

LATER / HIGHER LAYOUT RISK
  P6 world-map place names and long-yomi layout

FINAL BROAD VALIDATION
  P7 special/runtime QA

PARALLEL RESEARCH WHEN RELEVANT
  FONT page 63 / description-font path
```

## 6. Regression and implementation rules

Every future change must:
- use the immutable runtime-pass product as before/after baseline
- preserve exact provenance for changed bytes
- keep unrelated carriers byte-exact
- separate analysis from implementation
- investigate the whole cause group before patching individual symptoms
- make one diagnostic build per cause group
- record rejected/failed hypotheses
- consult the actual PC patch first where it contains equivalent behavior/data
- never overwrite the known-good runtime reference ZIP

Git write remains restricted to:
`create_blob -> create_tree -> create_commit -> update_ref(force=false)`.

## 7. Resume instruction

On a new chat/session:
1. read root `PROJECT_STATE.md`
2. read `selective_ko/SELECTIVE_PROJECT_STATE.md`
3. read this roadmap
4. do not reopen already closed RootCause223 / Buffer8 / B23 findings
5. continue only the user-authorized polish scope

Exact current continuation point:
`FONT_A_RUNTIME_VALIDATION_AWAIT_USER_OBSERVATION`
