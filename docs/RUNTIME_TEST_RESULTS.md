# RUNTIME TEST RESULTS

Observed Eden Android behavior for Taiko5DX Switch Korean-port development builds.

These observations are empirical evidence. They do not by themselves certify an inline candidate as SAFE.

## 2026-09-10

### Baseline / integrated tests

| Variant | Inline set | Other Korean-port components | Result |
|---|---:|---|---|
| Add-on disabled | 0 | none | Game boots/runs normally |
| v0.2a integrated | 5,519 selected patterns | 207 RomFS replacements + Korean font + IPS records emitted with the old offset convention | Freeze |
| v0.2b NO-INLINE | 0 | 207 RomFS replacements + Korean font + one page-mapper IPS record emitted with the old offset convention | Boots; Korean title `태합입지전 V DX` is displayed |
| v0.2c | 5,518 selected patterns | same old-offset IPS convention | Still fails/freezes |
| P0N v0.2f | 5,519 intended no-op records | same RomFS/font baseline + page mapper; **old IPS offsets** | Freeze |
| P0N2 v0.2g | 5,519 true no-op records | same RomFS/font baseline + corrected page mapper; **all IPS offsets mapped+0x100** | **Boots, reaches Korean title, accepts input, reaches next main menu** |
| M1A v0.2h | 1 real inline (`R489`) | same corrected RomFS/font/page-mapper baseline | **PASS — reaches scenario selection, scenario description, protagonist selection; remains responsive** |

### Address-ordered half split

The remaining 5,518 inline patterns were split by Switch offset order only for diagnosis. These builds also used the old IPS-offset convention and therefore cannot be used to infer candidate-level safety or multi-fault distribution.

| Group | Count | Approx. mapped Switch offset range | Result |
|---|---:|---|---|
| A | 2,759 | `0x682AE5..0x72028D` | Freeze |
| B | 2,759 | `0x72034F..0x783F9A` | Korean title appears; pressing a button causes forced exit/crash |

### Critical IPS-offset correction discovered after P0N failure

Inspection of Eden/Yuzu-derived NSO loading shows that ExeFS IPS patches are applied to an artificial patch image consisting of:

```text
0x000000..0x0000FF  NSOHeader (0x100 bytes)
0x000100..          decompressed mapped NSO image
```

Eden's NSO loader copies the decompressed `codeset.memory` after `sizeof(NSOHeader)`, and `NSOHeader` is statically `0x100` bytes. Therefore a mapped flat-image offset `X` must be emitted to classic IPS as **`X + 0x100`**.

All development IPS builds through P0N v0.2f emitted mapped offsets directly without the required `+0x100`. Consequently:

- the P0N records were **not true no-ops in Eden** even though they round-tripped against our flat-image model;
- a record intended for flat offset `X` actually overwrote flat offset `X - 0x100` in Eden;
- the page-mapper record intended for flat `0x44650C` was emitted at IPS `0x44650C`, which targets flat `0x44640C`; the correct Eden IPS offset is `0x44660C`;
- prior v0.2a/v0.2c/A/B crashes do **not** prove that the selected inline candidates themselves were wrong, because they were never applied at the intended addresses;
- v0.2b boot/Korean-title observation remains a real runtime fact, but it does **not** validate the intended page-mapper rewrite because that IPS record was also shifted by `-0x100` at application time.

This supersedes the earlier interpretation that the P0N failure demonstrated a large-record-count or semantic-inline failure.

### Corrected control: P0N2 v0.2g — PASSED

Artifact:

- filename: `P0N2_Taiko5DX_KR_DBG_NOOP5519_PLUS100_v0.2g.zip`
- SHA-256: `1ccb27e7f8836b8687ade7e147b0f549d49069dcecebaf808fa6eabd3277e8f6`
- IPS records: 5,520 total = corrected page mapper + 5,519 true no-op inline records
- emitted offset rule: `mapped flat offset + 0x100`
- page mapper: mapped `0x44650C` -> emitted IPS `0x44660C`
- static round-trip: VERIFIED; every 5,519 no-op payload equals the original bytes at `(IPS offset - 0x100)`
- runtime result: **PASS — boot, Korean title, button input, and next main menu all reached**

This establishes the following narrow conclusions:

1. Eden accepts the corrected classic-IPS coordinate convention used by P0N2.
2. A 5,520-record classic IPS is not intrinsically causing the observed freeze on this test path.
3. The old P0N freeze is explained by the `-0x100` misapplication and must not be used as a large-record-count failure result.
4. The corrected page-mapper record coexists with the baseline through the tested menu path, but this is still only path coverage, not exhaustive mapper proof.

### MVI content test M1A v0.2h — PASSED

Configuration:

- corrected page mapper;
- 207 RomFS replacements + Korean 64-page font;
- exactly one real inline replacement;
- T5K record ID `489`;
- Japanese: `シナリオを選んでください`;
- Korean: `시나리오를 선택하세요`;
- mapped Switch offset: `0x69B6A1`;
- emitted Eden IPS offset: `0x69B7A1`;
- all other historical inline candidates absent.

User runtime evidence on 2026-09-10 shows successful progression through the corrected build: title/main flow, scenario screen, scenario-description screen, and protagonist-selection screen all render and remain responsive. Screenshots also show extensive Korean text from the RomFS/font baseline. Those baseline Korean strings must not be misattributed to the single M1A inline record.

Narrow conclusion: **at least one corrected real inline record can coexist with the corrected page mapper/RomFS/font baseline without reproducing the former freeze on this route.** This weakens a blanket hypothesis that any real inline content necessarily causes immediate failure. It does not certify the historical 5,519 set or prove that every runtime descriptor is already unnecessary.

### Next MVI controls

Two additional independent one-record builds are prepared before scaling to 10 records:

- `M1B v0.2i`: T5K `R674`, mapped `0x682DA4` / IPS `0x682EA4`, `主人公選択` -> `주인공선택`.
- `M1C v0.2j`: T5K `R726`, mapped `0x684140` / IPS `0x684240`, `はじめから` -> `처음부터`.

Test each build independently with all other Korean diagnostic mods disabled. If both remain stable and the target label visibly changes, proceed to a corrected 10-record MVI build.

### Current interpretation

- The dominant confirmed implementation defect in all pre-P0N2 IPS builds was the missing `+0x100` Eden/NSO-header IPS offset shift.
- P0N2 proves the corrected large-record-count no-op path works through the main menu.
- M1A proves one corrected real inline replacement can survive substantially beyond the title on the tested route.
- Previous IPS-bearing runtime results remain useful historical observations but must not be used as candidate-safety evidence.
- Semantic inline validation is still required for release quality; P0N2/M1A do not make the old 5,519 selector safe by themselves.
- Future IPS generators must validate both mapped offsets and emitted Eden IPS offsets separately.
