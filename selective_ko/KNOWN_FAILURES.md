# KNOWN FAILURES AND DO-NOT-REPEAT PATHS

Date: 2026-09-15
Status: INITIAL MIGRATION RECORD

This file preserves important rejected or weakened approaches from the historical full-port track so the selective project does not repeat them.

## 1. Dialogue malformed-ending family

Representative Switch symptoms observed during the full-port track:

- `조금 과음한 모양이이오군`
- `오늘은 이만 실례하하겠습니다`
- `야규님입니다인가`

Relevant findings already established:

- not a font/glyph cause;
- not a Mapping 10,036 cause;
- `0x6A` is a real speech-style selector, but inversion is not a fix;
- field64 is person/context identity-related, not a simple speech-style field;
- C8:87 PC/Switch predicate structure is closely corresponding;
- PC original vs PC Korean SNR relation-state tail used by C8:87 is preserved;
- PC Korean TAI5MSG and current Switch-reconstructed C73/C188/message objects can be byte-identical while Switch output remains malformed;
- PC Korean data itself can contain caller + formatter boundaries such as `실례하 + C188`, so naive visual inspection of stored fragments is not enough to infer final PC composition semantics.

Selective-project disposition:

- do not treat this family as an R1-R3 blocker;
- affected lines default to `HOLD_DYNAMIC_DIALOGUE`;
- reopen only under an explicit R4 formatter-family grammar scope.

## 2. Prohibited dialogue shortcuts

Do not use:

- sentence-by-sentence translation correction to hide a shared formatter failure;
- direct deletion of suffixes;
- global `하하 -> 하` replacement;
- global `이이 -> 이` replacement;
- longest-overlap or repeated-syllable deduplication as a general runtime rule;
- forcing C8:87 false;
- global `0x6A` inversion;
- rewriting PC Korean source merely because Switch output is malformed;
- assuming every nested call is a pure string append without proving the exact composition contract.

## 3. Name/yomi/CWTDAT scope

Historical work showed that name display, yomi, auxiliary-name rows and platform-specific CWTDAT structure are separate problem families.

Selective-project policy:

- person names remain Japanese;
- place names remain Japanese;
- yomi/reading/sort keys remain Japanese;
- Korean name input is excluded;
- CWTDAT Korean reconstruction is not required for R1-R3.

Do not import the historical CWTDAT problem into description/event work unless a selected content item has a concrete dependency.

## 4. Runtime-byte normalization

Already rejected:

- globally disable Japanese halfwidth normalization;
- patch the downstream decoder merely because compact Korean bytes can be altered upstream;
- mechanically transplant the PC x86 byte-validation helper;
- identify a normalizer by caller-count coincidence alone.

Known Switch structure contains distinct direct-display, generic-parser and auxiliary/yomi conversion routes. Any future transport fix must remain route-aware.

## 5. Mapping

Do not reopen Mapping 10,036 because of unrelated renderer/font/dialogue symptoms.

The tested Switch-native four-action Mapping realization already demonstrated Korean forward/reverse round-trip on the tested Eden route.

## 6. Static-write shortcuts

Do not revive:

- raw occurrence uniqueness as write authorization;
- equal replacement length as sufficient safety proof;
- PC padding as assumed Switch capacity;
- shared-object overwrite without all logical-owner obligations;
- source target resolution as automatic write safety.

The selective scope reduces the source set, but every included write still needs a proven Switch owner and appropriate guard/capacity semantics.

## 7. PC implementation trust boundary

Do not assume:

- every PC workaround is desirable on Switch;
- PC descriptor/helper cardinality equals Switch counterpart cardinality;
- PC runtime allocation/signature-search mechanics are portability requirements;
- historical PC patch versions are uniformly reliable.

Use PC content as source evidence and PC visible behavior as semantic reference where relevant. Switch implementation must be chosen from Switch-native ownership and the selective product goal.
