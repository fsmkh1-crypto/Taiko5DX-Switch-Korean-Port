# VALIDATION LEDGER — R0 repeated-object normalization

Date: 2026-09-11  
Scope: DCTRL7 runtime normalization plus R0 static RELA/place-table/formatter evidence. No patch/build modification is part of V063-V069.

Detailed report: `docs/R0_REPEATED_OBJECT_NORMALIZATION.md`

## V063 — DCTRL7 diagnostic artifact has a complete pre-runtime provenance chain

**Claim:** `DCTRL7_Taiko5DX_KR_EDEN.zip` is a reproducible seven-record diagnostic generated from a builder committed before build/runtime use, with exact emitted-IPS verification and retained package identity.

**Status:** `VERIFIED`

**Evidence:**

- builder source commit `ccb13b3e85b8a72339b628f57bf12dda789fffe3`;
- 7 records = 1 page-mapper prerequisite + 1 V019 R489 positive control + 5 V024 repeated-object diagnostics;
- guards `7 PASS / 0 FAIL / 0 SKIP`, no extra records;
- exact self-reparse, independent raw serialization check and `mapped + 0x100` coordinate round-trip pass;
- IPS SHA-256 `2114f14ccc098103524b7cb4afaf416a8bc0185bc607dd198ce4f9511d2d6fab`;
- ZIP SHA-256 `c1092c6cb43da985a536c94dd01f132516540af35232f11d634e1afc0341fb33`;
- Drive-retained package was redownloaded and byte-identical to the built ZIP.

**Reuse rule:** This validates the DCTRL7 artifact/build pipeline only. It does not retroactively establish historical PCREF1 emitted contents.

## V064 — DCTRL7 visibly delivers standalone `年 @ 0x69785A` on the scenario route

**Claim:** Under DCTRL7 in Eden v0.2.1, the scenario-selection display changed `1560年` to `1560년`, establishing runtime delivery and consumption of the standalone `年` replacement at mapped `0x69785A` on that route.

**Status:** `VERIFIED-RUNTIME`

**Evidence:**

- DCTRL7 record: mapped `0x69785A`, emitted `0x69795A`, original `94 4E`, replacement `EC E0`;
- retained screenshot `DCTRL7_01_scenario_1560nyeon.jpg`, Drive ID `17XlqbJWd5aaEAUtsV0QRedPRNkKcPctR`, SHA-256 `5dc08060b4e0d18eecc962a7512347486b2253e20d2a1d9a5b361efa11e5f75f`;
- the same artifact also includes the Korean font/page-mapper prerequisite.

**Limit:** This proves delivery/consumption for this record and route. It is not proof that every DCTRL7 record or every text path is delivered/consumed.

**Additional observation:** The user reported the in-game HUD still showed `1560年 2月30日` under DCTRL7. No DCTRL7 HUD screenshot was retained in R0, so that HUD result is observation-only pending consumer binding.

## V065 — Patching standalone `城 @ 0x6A15DC` is insufficient to change tested `岡崎城`

**Claim:** On the tested protagonist basic-information screen, DCTRL7 left `拠点 岡崎城` in Japanese even though the artifact contains the guarded standalone `城 @ 0x6A15DC -> 성` record. Therefore the standalone object is not sufficient to control that visible suffix on this route.

**Status:** `VERIFIED-RUNTIME`

**Evidence:**

- DCTRL7 record: mapped `0x6A15DC`, emitted `0x6A16DC`, original `8F E9`, replacement `F1 59`;
- retained screenshot `DCTRL7_02_basic_info_okazaki_castle_jp.jpg`, Drive ID `1eY4pPcBP80HnDfkSfodPTX5oi_C7ppjj`, SHA-256 `76a450b0770ab155c85f0e4272bc51bbe80daac78e5b764975f834dcd8bf25bb`;
- V064 proves the same DCTRL7 artifact was active and visibly delivered at least one diagnostic text record.

**Reuse rule:** Do not conclude the screen consumes `%s城` until its reader/consumer chain is traced. The only runtime conclusion here is that the standalone `城` patch alone is insufficient for this screen.

## V066 — Selected repeated/composite strings are RELA-materialized into `.data` pointer slots

**Claim:** In the exact Switch v1.1.3 mapped NSO, selected repeated/composite rodata objects are addends of `R_AARCH64_RELATIVE` relocations that materialize their addresses into `.data`; direct string-address XREF absence is therefore not evidence of non-use.

**Status:** `VERIFIED`

**Evidence:**

- MOD0 `0x8`; dynamic table `0x9FD708`;
- `DT_RELA=0x58D078`, `DT_RELASZ=0xECC70`, `DT_RELAENT=0x18`;
- 40,410 RELA entries; 40,023 type 1027;
- `年 0x69785A -> 0x9C3558, 0x9C5238`;
- `%4d年%2d月%2d日 0x68DD49 -> 0x9C1040, 0x9C2B58`;
- `%s城 0x68A1FB -> 0x9C09F0`;
- standalone `城 0x6A15DC -> 0x9C05A0, 0x9C0EC8, 0x9C4580, 0x9C63B0`;
- a narrow `.text` decode of exact `ADR` and `ADRP+ADD` materialization found zero direct references to those four exact rodata addresses.

**Reuse rule:** R1 must follow `rodata -> RELA data slot -> slot reader -> consumer`. Do not call this a game-code initializer; R0 establishes loader relocation/materialization, not yet the downstream reader.

## V067 — Japanese place table base/layout is `0x6ADA10`, stride `0x18`

**Claim:** The Japanese place table is a 310-entry fixed-stride array beginning at mapped `0x6ADA10`; `0x6ADA11` is the first record's name field, not the record base.

**Status:** `VERIFIED`

**Evidence:**

- parallel bases `0x6AF720 / 0x6ADA10 / 0x6B1430`, each separated by `0x1D10 = 310 * 0x18`;
- RELA global slots `[0xA1C420] -> 0x6AF720`, `[0xA1C428] -> 0x6ADA10`, `[0xA1C430] -> 0x6B1430`;
- record layout:
  - `+0x00` type/category byte;
  - `+0x01` 11-byte NUL-padded name field;
  - `+0x0C` 12-byte NUL-padded yomi field;
- accessor cluster around `0x1CC74C..0x1CCCC4` uses multiply/add by 24, reads record `+0`, forms record `+1`, and forms Japanese record `+0x0C`.

**Rejected prior wording:** `0x6ADA11` as record base and category/type at the record end.

## V068 — Place-table duplicate family is 33 names / 66 slots and PC replacements agree

**Claim:** The 310-entry Japanese place table contains 277 unique names; exactly 33 names occur twice, occupying 66 slots. All PC T5K records matching each duplicated name agree on one replacement byte sequence.

**Status:** `VERIFIED`

**Evidence:**

- duplicate type-pair distribution: `(0,3)=30`, `(0,5)=2`, `(3,0)=1`;
- `岡崎`: name fields `0x6AE221` (index 86/type 0) and `0x6AEFD1` (index 232/type 3); PC R3424/R3718 replacement `F2BEF54AF379F5AE`;
- `清洲`: name fields `0x6AE269` (index 89/type 0) and `0x6AEFE9` (index 233/type 3); PC R3430/R3720 replacement `EBE0F2E2F1B8`;
- `江戸`, `鳥羽`, `洲本` each have three matching PC T5K records rather than two, but all three replacements still agree;
- full 33-name matrix is in the R0 report.

**Reuse rule:** Preserve yomi. Duplicate-name translation may use source-grounded PC bytes only after the runtime table/type selection path is understood. Do not assume all duplicate pairs are 0/3.

## V069 — PC R2552-R2563 correspond structurally to a 12-slot Switch `%s...` formatter family

**Claim:** PC T5K R2552-R2563 form a consecutive place suffix/reading family that corresponds in order to 12 consecutive RELA-backed Switch formatter slots.

**Status:** `VERIFIED`

**Evidence:**

PC visible sequence:
`城 / 館 / の町 / の里 / の砦 / 寺 / じょう / やかた / のまち / のさと / のとりで / じ`

Switch sequence:
`%s城 / %s館 / %sの町 / %sの里 / %sの砦 / %s寺 / %sじょう / %sやかた / %sのまち / %sのさと / %sのとりで / %sじ`

The Switch formatter pointers occupy consecutive `.data` slots `0x9C09F0..0x9C0A48` at 8-byte stride.

**Limit:** This is static family correspondence only. R0 does not prove that the tested basic-information `岡崎城` screen consumes `%s城 @ 0x68A1FB`.

## Working hypothesis intentionally not promoted to a validation ID

PC T5K contains 19 isolated `年/月/日` suffix records (`5/5/9`), all replacement-consistent. R0 records an 11-object Switch standalone/composite working set, including `%4d年%2d月%2d日 @ 0x68DD49`. This is a structural candidate set for R1/R2, **not** a claim that Switch has exactly 11 date objects or that the HUD consumer is already bound.
