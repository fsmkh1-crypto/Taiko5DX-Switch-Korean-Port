# CHANGELOG

## 2026-09-11

### Compact Korean single-byte font path mapped; W0 prepared

- Traced the missing `츠` in `마츠다이라 모토야스` to a PC compact single-byte Korean mechanism rather than a translation omission.
- T5K R9751/R9752 encode `마츠다이라 모토야스` in a 16-byte fixed field using page-63 single-byte `B2/BD/AA = 마/츠/다`, then normal two-byte Korean for the remainder.
- Direct BC3 decode of the exact Korean G1T verifies valid source glyph artwork for compact `마/츠/다` and normal two-byte `케/자`; source-font corruption is ruled out for these glyphs.
- Decoded PC `font_page_limit` semantics: threshold `0xFF -> 0xA0`, making A1+ single-byte codes take the alternate/full-width path.
- Identified six Switch v1.1.3 semantic counterpart/inlined comparisons at mapped `0x445EAC`, `0x445FC8`, `0x446198`, `0x4472E8`, `0x447344`, `0x447C44`.
- Added `builder/build_w0_fontwidth.py`; W0 changes only these six `cmp w8,#0x100` instructions to `cmp w8,#0xA1` on top of D5519.
- Prepared `W0_Taiko5DX_KR_DBG_FONTWIDTH_A1_v0.2m.zip`, SHA-256 `e453d5958793748ebf841f295ef4005a9a612fdbe643439fe9c2a2c0183ea2ad`, 5,526 IPS records total. Runtime pending.
- A separate `cmp #0x100` in conversion logic around mapped `0x4304F8` is explicitly excluded from this patch family.

### Y0 runtime result: narrow suppression hypothesis incomplete

- User runtime-tested `Y0 v0.2l` in Eden Android.
- Y0 remained stable, but the garbled small reading rows in protagonist selection and dialogue nameplates **did not disappear**.
- The eight direct `mov w6,#1` call sites to shared routine `0x45B0F8` remain valid static mappings, but they do not control the observed two rows by themselves, or another wrapper/path renders/re-enables them.
- Do not repeat the eight-site-only suppression attempt. Internal Japanese yomi preservation remains the data policy while the actual visible-row path is deferred behind the higher-impact compact-name/font issue.

### D5519 corrected full-inline diagnostic passed

- User runtime-tested `D5519 v0.2k`, which reuses the historical v0.2a 5,519 real inline payload bytes but fixes every Eden IPS address to `mapped + 0x100`.
- D5519 reached title, menu, scenario selection/description, protagonist selection, and normal gameplay without freeze/forced exit on the tested route.
- This strongly shifts the old freeze diagnosis from "the 5,519 inline set is broadly unsafe" to "the pre-P0N2 builds were dominated by the missing +0x100 IPS coordinate bug". The 5,519 set is still not release-certified for all paths.
- Visible residual issues are now treated as UI/data-coverage problems: garbled auxiliary yomi line, repeated short Japanese UI tokens, repeated place-name fields, and compact/fixed-field Korean name rendering.

### Yomi strategy established

- Added `docs/POST_D5519_ANALYSIS.md`.
- Verified that 2,099 of D5519's 5,519 real inline records target halfwidth-kana/NUL fields; 3,420 historical non-yomi records remain after excluding them.
- Verified eight mapped call sites containing `mov w6,#1` immediately before/near calls to shared name/yomi routine `0x45B0F8`: `0x2A0ABC`, `0x2A565C`, `0x2A6F4C`, `0x2A7720`, `0x2A7FE4`, `0x2ADE5C`, `0x2BC1A0`, `0x2BD5C8`.
- Switch-port policy is: keep Korean main names, preserve original Japanese yomi internally for sort/comparison/input compatibility, and eventually suppress only the visible auxiliary yomi line through the actual rendering path.
- Added reproducible `builder/build_y0_noyomi.py`.
- `Y0_Taiko5DX_KR_DBG_NOYOMI_v0.2l.zip` SHA-256 `ae67b2bdece0e261239a3a505ad018761904c25124f0857cf0a917f9a4a6c869`.

### Repeated-object recovery evidence

- Added `builder/repeated_token_probe.py` to distinguish actual Switch string objects from raw substring collisions.
- `はい`: 7 raw rodata matches but exactly one standalone NUL object at `0x6A15A5`, pointer-ref `0x58D0D0`; adjacent pointer-table object is `いいえ` at `0x6A65B2`.
- Pooled date suffix objects identified: `年 0x69785A`, `月 0x68925A`, `日 0x6A3CC6`; pointer table `0x59C730..0x59C768` references them consecutively. Multiple PC records all agree on `년/월/일`.
- Pooled standalone `城` object identified at `0x6A15DC`, with multiple pointer refs; PC replacements agree on `성`.
- `清洲`: two T5K padded records with identical replacement `기요스`; Switch has exactly two corresponding fixed-field objects at `0x6AE269` and `0x6AEFE9`.
- New rule: recover repeated **objects**, not every raw byte match. Require replacement agreement and independent boundary/pointer/stride evidence.
- Currency `貫/文` remains a separate structural pass because many visible uses are embedded in longer format strings.

### Canonical documentation advanced

- Updated `PROJECT_STATE.md`, `PATCH_MAP.md`, `docs/RUNTIME_TEST_RESULTS.md`, `docs/VALIDATION_LEDGER.md`, and `docs/POST_D5519_ANALYSIS.md` so W0 is the current runtime diagnostic and the Y0 result is not repeated as an unresolved test.

## 2026-09-10

### Corrected Eden IPS coordinate bug

- Confirmed Eden/Yuzu NSO classic IPS operates on `0x100-byte NSOHeader + decompressed mapped image`.
- Canonical rule: `emitted IPS offset = mapped flat NSO offset + 0x100`.
- Corrected `builder/build.py` and diagnostic builders to preserve mapped offsets internally and add `+0x100` only during IPS serialization.
- Pre-P0N2 IPS-bearing builds patched `0x100` bytes early; their crashes cannot be used as candidate-safety evidence.

### P0N2 passed

- `P0N2 v0.2g`: corrected page mapper + 5,519 true no-op records.
- Runtime PASS through Korean title, input, and main menu.
- This disproved the hypothesis that 5,520 classic-IPS records themselves caused the old freeze.

### M1A passed

- `M1A v0.2h`: one real inline `R489`, `シナリオを選んでください` -> `시나리오를 선택하세요`, mapped `0x69B6A1`, emitted `0x69B7A1`.
- Runtime PASS through scenario/protagonist-selection flow.

### Phase-0 evidence/provenance

- Added `docs/PHASE0_FAILURE_MODE_PLAN.md`, `builder/phase0_probe.py`, and corrected diagnostic builders.
- Reverified historical selector counts: 17,103 records; 8,713 unique originals; 5,523 unique-rodata candidates; 4 overlap skips; 5,519 selected patterns covering 5,521 PC records.
- Reproduced collinearity: 6,053 record-level unique pairs; LIS 3,524; 2,529 outside; top runs 1,844/1,074/978/78.
- Reproduced NUL statistic: 12,347 records contain NUL in original and none in replacement; 4,747 originals contain no NUL.
- External `430` termination and `8,981/1,242` >=5-match figures remain non-canonical because the fixed-input probe did not reproduce their stated definitions.
- Confirmed Switch conversion loops still use 7,494 entries and have defined misses (`0x81A1`, `U+25A0`).
- Confirmed supplied Drive `PC_Original/Taiko5DX.exe` is not the exact Steam build-9163702 T5K target and barred it from PC binary-context evidence.

### Validation policy/ledger

- Added `docs/INLINE_VALIDATION_POLICY.md` and `docs/RUNTIME_TEST_RESULTS.md`.
- Promoted `docs/VALIDATION_LEDGER.md` to mandatory pre-read and no-redundant-revalidation authority.
- `unique exact match` is candidate discovery only; runtime pass is sanity evidence only.
- Full release validator target remains all 17,103 T5K inline records.

### Distribution/target workflow

- Fixed Eden Android as primary runtime target and Android APK as final frontend.
- APK will accept user-supplied complete Switch v1.1.3 dump + PC patch ZIP and emit an Eden-ready mod via SAF/user-granted locations.
- Direct normal file-manager access to Eden internal Android storage is not assumed; use Eden Add-ons import during development.
- Repository must never contain game executables/data, patch payloads/fonts, keys, dumps, or generated full mod packages.