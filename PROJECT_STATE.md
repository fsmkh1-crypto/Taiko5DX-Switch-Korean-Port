# PROJECT_STATE

Last updated: 2026-09-11 (KST)

## Active staged analysis — R0 repeated-object normalization complete / STOP

PC DLL PHASE 1–4 and PC Runtime Canonical Closure remain complete. Historical PCREF1 remains `ARTIFACT_INSUFFICIENT` under V062 and must not be used as negative evidence against repeated/fixed-object mappings.

The current Switch feedback loop has now been restored by the fully provenance-bound DCTRL7 diagnostic and the subsequent R0 normalization pass.

Current canonical authority:

- V001–V061: established Switch baseline and closed PC runtime facts;
- V062: historical PCREF1 emitted-delivery provenance gap;
- V063–V069: DCTRL7 provenance/runtime result plus R0 RELA/place-table/formatter structure;
- detailed R0 report: `docs/R0_REPEATED_OBJECT_NORMALIZATION.md`;
- DCTRL7 runtime record: `docs/diagnostics/DCTRL7_RUNTIME_RESULT.md`;
- validation index: `docs/VALIDATION_LEDGER.md`.

### Current resume point

R0 is complete. No R1 analysis, code modification, builder modification, IPS generation or new diagnostic build has been authorized or started.

The next recommended stage after a fresh user execution signal is **R1 consumer binding only**:

`rodata object -> RELA .data slot -> code reader -> consumer -> runtime screen`

Preferred positive anchor: runtime-confirmed standalone `年 @ 0x69785A`.

R1 must report and STOP before any later DATE/PLACE implementation or diagnostic build.

## 1. Goal

Port `Taiko5DX_Korean_Patcher_v1.02` to Nintendo Switch **TAIKO RISHHIDEN V DX v1.1.3**, with Eden Android as the primary runtime target. Final user-facing frontend remains an Android APK reusing the stabilized core builder.

Fixed target:

- Title ID `0100346017304000`
- Switch version `1.1.3`
- Build ID `D9120950C258610A746F4A31CE3A3B376DE393D9`
- compressed `main` SHA-256 `b366e692208f3c0cc18bc1884ef95689b6b11d722fa2d749b8500abccbc3109b`
- mapped flat size `0xA20430`
- text `0x000000 + 0x58CE60`
- rodata `0x58D000 + 0x432018`
- data `0x9C0000 + 0x60430`

## 2. Canonical Eden IPS coordinate rule

Eden/Yuzu classic NSO IPS operates on `0x100-byte NSOHeader + decompressed mapped NSO image`.

```text
emitted IPS offset = mapped flat NSO offset + 0x100
```

Example: mapped page mapper `0x44650C` -> emitted `0x44660C`.

All IPS-bearing builds through P0N v0.2f omitted this shift; their crashes are historical observations only and cannot establish candidate-level failure.

## 3. Corrected runtime baseline

- **P0N2 v0.2g**: corrected mapper + 5,519 true no-op records -> PASS through title/input/main menu.
- **M1A v0.2h**: one real inline `R489` -> PASS through scenario/protagonist flow.
- **D5519 v0.2k**: historical 5,519 real replacements at corrected coordinates -> PASS into normal early gameplay.
- **Y0 v0.2l**: stable but eight-site yomi suppression did not remove observed garbled reading rows.
- **W0 v0.2m**: stable; `케/자` observation retained, direct A1+ causality not established.
- **W1 v0.2n**: tested Matsudaira `쓰` symptom unchanged; direct-cause hypothesis at `0x44D9D0` invalidated.
- **DCTRL7**: current delivery discriminator; scenario `1560年 -> 1560년`, tested `岡崎城` unchanged, in-game HUD date reported unchanged.

## 4. DCTRL7 provenance and runtime consequence

DCTRL7 artifact identity:

- builder source commit `ccb13b3e85b8a72339b628f57bf12dda789fffe3`
- 7 IPS records = page mapper prerequisite + V019 R489 positive control + five V024 repeated-object diagnostics
- guards `7 PASS / 0 FAIL / 0 SKIP`, no extras
- exact self-reparse / independent raw serialization / coordinate round-trip PASS
- IPS SHA-256 `2114f14ccc098103524b7cb4afaf416a8bc0185bc607dd198ce4f9511d2d6fab`
- package SHA-256 `c1092c6cb43da985a536c94dd01f132516540af35232f11d634e1afc0341fb33`
- Drive-retained package was redownloaded byte-identical before runtime use

Runtime on Eden Android v0.2.1:

- standalone `年 @ 0x69785A` visibly changed scenario `1560年` to `1560년`;
- therefore current ExeFS IPS delivery and Korean font/page-mapper rendering are proven for that record/route;
- global DCTRL7 delivery failure is rejected;
- standalone `城 @ 0x6A15DC` did not change the tested `拠点 岡崎城` screen, so that standalone object is not sufficient for that route;
- user reported in-game HUD `1560年 2月30日` remained Japanese; consumer binding is still required before promoting a specific composite source.

PCREF1 remains provenance-insufficient; DCTRL7 does not retroactively repair the lost PCREF1 artifact.

## 5. R0 repeated-object normalization

### 5.1 RELA-backed string materialization

Selected repeated/composite rodata strings are addends of `R_AARCH64_RELATIVE` relocations that materialize pointers into `.data`.

Examples:

```text
年 0x69785A
  -> 0x9C3558, 0x9C5238

%4d年%2d月%2d日 0x68DD49
  -> 0x9C1040, 0x9C2B58

%s城 0x68A1FB
  -> 0x9C09F0

standalone 城 0x6A15DC
  -> 0x9C05A0, 0x9C0EC8, 0x9C4580, 0x9C63B0
```

A narrow direct `ADR` / `ADRP+ADD` scan found no exact direct address materialization for those four rodata addresses. Therefore direct string-XREF absence is not non-use evidence.

Current proven mechanism stops at:

`rodata -> loader RELA -> .data pointer slot`

The downstream `.data slot -> reader -> UI consumer` chain is R1 work. Do not call this a game-code global-string initializer until that is independently established.

### 5.2 Place table layout corrected

Japanese place table base is:

`0x6ADA10`

not `0x6ADA11`.

Record structure:

```text
stride 0x18
+0x00  type/category byte
+0x01  name[11], NUL padded
+0x0C  yomi[12], NUL padded
```

There are three parallel 310-entry tables at:

```text
0x6AF720
0x6ADA10
0x6B1430
```

Each adjacent base differs by `0x1D10 = 310 * 0x18`. The exact semantic role/language of the two non-Japanese tables remains intentionally unnamed.

Accessor code around `0x1CC74C..0x1CCCC4` uses `index * 0x18`, reads record `+0`, forms name `+1`, and Japanese yomi `+0x0C`.

Rejected prior wording:

- `0x6ADA11` as record base;
- category/type at the record end.

### 5.3 Duplicate place family

Japanese table census:

- records 310
- unique names 277
- duplicated names 33
- duplicate slots 66
- type pairs `(0,3)=30`, `(0,5)=2`, `(3,0)=1`

Important examples:

```text
岡崎
  index 86  type 0  name 0x6AE221
  index 232 type 3  name 0x6AEFD1

清洲
  index 89  type 0  name 0x6AE269
  index 233 type 3  name 0x6AEFE9
```

All PC T5K records matching each of the 33 duplicated names agree on one replacement byte sequence. `江戸`, `鳥羽`, `洲本` each have three matching PC records, but their replacements also agree.

Internal yomi remains preserved and is not a translation target.

### 5.4 Place formatter family

PC T5K R2552–R2563 form a consecutive family:

`城 / 館 / の町 / の里 / の砦 / 寺 / じょう / やかた / のまち / のさと / のとりで / じ`

Switch has a corresponding consecutive RELA-backed formatter family:

`%s城 / %s館 / %sの町 / %sの里 / %sの砦 / %s寺 / %sじょう / %sやかた / %sのまち / %sのさと / %sのとりで / %sじ`

Pointer slots occupy `0x9C09F0..0x9C0A48` at 8-byte stride.

Static structural correspondence is VERIFIED. The tested `岡崎城` screen has not yet been directly consumer-bound to `%s城 @ 0x68A1FB`.

### 5.5 Date working set

PC T5K contains 19 isolated date-suffix records:

- `年`: 5
- `月`: 5
- `日`: 9

All replacements agree within each suffix family.

R0 correlates these with an 11-object Switch standalone/composite **working set**, including:

- standalone `年 @ 0x69785A`
- standalone `月 @ 0x68925A`
- standalone `日 @ 0x6A3CC6`
- `%4d年%2d月%2d日 @ 0x68DD49`
- other `%d年`, `% 2u月 % 2u日`, remaining-day and save-data composite objects

This is not a claim that Switch has exactly 11 date objects. `%4d年%2d月%2d日` is a strong candidate for the in-game HUD but remains unbound to that consumer.

## 6. PC patch remains semantic authority

PC patch source identity:

- patch ZIP SHA-256 `df1b62de95e992369e9686c9731d814e7a7e4634888f610430635429e24f7cec`
- `dinput8.dll` SHA-256 `ffe7e9da8e00c96bec631b45a3e9c4d3f314551623351f3e7024e0318913c6b7`
- T5K121R SHA-256 `5c6f4eba8c6f0516365e4518f27e9d8c840aead463b5a2938dd1e08b99726d29`
- T5K contains 10,036 mappings, 17,103 inline records, 56 pointer records, 11 runtime descriptors

Where PC and Switch storage differ, port PC actual replacement bytes/semantics into the Switch structure; do not invent translations or encodings.

The supplied Drive `PC_Original/Taiko5DX.exe` is not the exact target and remains barred from PC RVA-neighborhood evidence. Exact target: Steam build 9163702, size 18,685,960, SHA-256 `10c69bab50d29baf6311360cafbf7383716a126a6484d209f5e299e12ab565a2`.

## 7. Other unresolved families retained

- mapping expansion: Switch conversion loops still search 7,494 rather than 10,036 entries;
- pointer-56 correspondence remains pending;
- remaining runtime-descriptor/helper counterparts remain pending;
- visible yomi row path remains unresolved; do not repeat the eight-site-only Y0 attempt;
- compact `쓰` remains unresolved across active-name slot/data selection, pointer/reference selection, and byte-validation/copy behavior;
- currency `貫/文` remains a separate format-object family;
- CWTDAT release path remains Switch-native reconstruction, not blind wholesale PC replacement.

## 8. Mandatory rules for next work

- one execution signal authorizes only the agreed stage;
- analysis and modification remain separate;
- one diagnostic build = one root-cause family;
- survey all same-cause sites before patching;
- PC actual patch first;
- direct XREF absence cannot reject an indirectly referenced string;
- preserve Japanese internal yomi;
- no new build/runtime evidence without tracked builder, pre-test commit, guards, self-reparse, hashes and retained artifact identity.

## 9. Next stage

After a fresh user signal, perform **R1 consumer binding analysis only**.

Trace one complete positive path:

`年 @ 0x69785A -> RELA .data slot -> slot reader -> consumer -> scenario screen`

Use that mechanism to define how later DATE-COMPOSITE and PLACE-FORMATTER paths should be traced. Report:

`확정된 사실 / 유력한 가설 / 미확정 사항 / 기각된 가설 / 관련 영향 범위 / 수정 제안`

Then STOP. Do not build or modify code without another fresh signal.

## 10. Distribution

Development builds are installed through Eden per-game Add-ons import. Final frontend remains an Android APK using SAF, accepting the user's extracted Switch 1.1.3 dump plus PC patch ZIP and emitting an Eden-ready mod without embedding copyrighted game binaries/data, patch payloads/fonts, keys or dumps.
