# DCTRL7 runtime result

Date: 2026-09-11  
Target: Nintendo Switch Taiko Risshiden V DX v1.1.3 / Build ID `D9120950C258610A746F4A31CE3A3B376DE393D9`  
Emulator: Eden Android v0.2.1

## Artifact identity

- test ID: `DCTRL7`
- builder source commit: `ccb13b3e85b8a72339b628f57bf12dda789fffe3`
- build report: `docs/diagnostics/DCTRL7_BUILD_REPORT.json`
- IPS SHA-256: `2114f14ccc098103524b7cb4afaf416a8bc0185bc607dd198ce4f9511d2d6fab`
- package: `DCTRL7_Taiko5DX_KR_EDEN.zip`
- package SHA-256: `c1092c6cb43da985a536c94dd01f132516540af35232f11d634e1afc0341fb33`
- Drive artifact ID: `1UTXpiOfju77_9yQT55dkhlTeB59jlwJ4`
- install method: Eden per-game Add-ons -> Mods and cheats; extracted mod root containing `exefs/` and `romfs/`
- user stated DCTRL7 was registered and active
- exact concurrent add-on list was not retained
- Eden's internal installed copy was not separately hashable

## Intended records

7 IPS records:

1. V006 page mapper prerequisite;
2. V019 R489 positive-control text;
3. `月 @ 0x68925A`;
4. `年 @ 0x69785A`;
5. `はい @ 0x6A15A5`;
6. `城 @ 0x6A15DC`;
7. `日 @ 0x6A3CC6`.

All seven preimage guards passed and the emitted IPS passed exact self-reparse, independent raw serialization and `mapped + 0x100` coordinate round-trip before runtime use.

## Runtime observations

### 1. Scenario-selection year — visible change

Observed:

`1560年 日輪の章` -> `1560년 日輪の章`

The only DCTRL7 diagnostic record capable of this exact `年` replacement is:

- mapped `0x69785A`
- emitted `0x69795A`
- `94 4E -> EC E0`

Interpretation:

- the current DCTRL7 ExeFS IPS path is active at least for this record/route;
- the Korean font/page-mapper path can render this replacement;
- global "DCTRL7 IPS was not delivered" is rejected.

Retained evidence:

- `DCTRL7_01_scenario_1560nyeon.jpg`
- Drive ID `17XlqbJWd5aaEAUtsV0QRedPRNkKcPctR`
- SHA-256 `5dc08060b4e0d18eecc962a7512347486b2253e20d2a1d9a5b361efa11e5f75f`

### 2. Protagonist basic-information `岡崎城` — unchanged

Observed:

`拠点 岡崎城` remained Japanese.

DCTRL7 did contain:

- mapped `0x6A15DC`
- emitted `0x6A16DC`
- `8F E9 -> F1 59`

Narrow interpretation:

- patching the standalone `城 @ 0x6A15DC` is insufficient to change this tested `岡崎城` display;
- do not yet claim `%s城` is the consumer until R1/R3 binds its RELA slot to the screen.

Retained evidence:

- `DCTRL7_02_basic_info_okazaki_castle_jp.jpg`
- Drive ID `1eY4pPcBP80HnDfkSfodPTX5oi_C7ppjj`
- SHA-256 `76a450b0770ab155c85f0e4272bc51bbe80daac78e5b764975f834dcd8bf25bb`

### 3. In-game HUD date — user-reported unchanged

The user reported that the in-game HUD still displayed:

`1560年 2月30日`

under DCTRL7.

No DCTRL7 HUD screenshot was retained in this R0 session, so preserve this as a runtime observation with narrower provenance than observations 1–2. It supports, but does not by itself prove, the separate-composite-date-source hypothesis.

## Not observed / not failed

The supplied DCTRL7 route did not directly expose:

- R489 `シナリオを選んでください`;
- standalone `月`;
- standalone `日`;
- `はい`.

Do not classify these as runtime failures.

## Canonical consequence

DCTRL7 restores a trustworthy feedback loop for the tested `年 @ 0x69785A` route: a fully provenance-bound artifact produced a visible, source-grounded change. PCREF1 remains artifact-insufficient and is not retroactively repaired by DCTRL7.

Follow-up static normalization is recorded in `docs/R0_REPEATED_OBJECT_NORMALIZATION.md`.
