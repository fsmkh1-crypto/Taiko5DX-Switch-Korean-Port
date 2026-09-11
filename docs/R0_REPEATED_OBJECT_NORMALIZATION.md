# R0 repeated-object evidence normalization

Date: 2026-09-11  
Scope: analysis-only normalization after DCTRL7. No builder/patch/IPS/ZIP changes were made in R0.

## 1. Purpose

R0 separates newly observed runtime facts from hypotheses and verifies two new static leads before R1 consumer tracing:

1. repeated/date/place strings may be materialized through NSO RELA into `.data` pointer slots rather than referenced by direct `.text` address construction;
2. the place table record base/layout needed correction from the earlier `0x6ADA11` interpretation.

Canonical prior facts V001–V062 were reused rather than revalidated unless new DCTRL7 evidence or insufficient provenance required a narrow check.

## 2. Fixed input identities

- Switch v1.1.3 compressed `main`: 5,287,359 bytes, SHA-256 `b366e692208f3c0cc18bc1884ef95689b6b11d722fa2d749b8500abccbc3109b`
- Build ID: `D9120950C258610A746F4A31CE3A3B376DE393D9`
- mapped image size: `0xA20430`
- PC patch ZIP SHA-256: `df1b62de95e992369e9686c9731d814e7a7e4634888f610430635429e24f7cec`
- `dinput8.dll` SHA-256: `ffe7e9da8e00c96bec631b45a3e9c4d3f314551623351f3e7024e0318913c6b7`
- T5K121R SHA-256: `5c6f4eba8c6f0516365e4518f27e9d8c840aead463b5a2938dd1e08b99726d29`

## 3. DCTRL7 runtime evidence normalization

DCTRL7 package identity:

- builder source commit `ccb13b3e85b8a72339b628f57bf12dda789fffe3`
- IPS SHA-256 `2114f14ccc098103524b7cb4afaf416a8bc0185bc607dd198ce4f9511d2d6fab`
- ZIP SHA-256 `c1092c6cb43da985a536c94dd01f132516540af35232f11d634e1afc0341fb33`

Runtime observations on Eden v0.2.1:

- scenario selection shows `1560년 日輪の章`; DCTRL7 has one diagnostic write to standalone `年` at mapped `0x69785A`, so this establishes that this write was delivered and consumed on that route;
- protagonist basic-information screen still shows `拠点 岡崎城`; therefore the tested screen did not consume DCTRL7's standalone `城` object at `0x6A15DC`, or a later independent source overwrote/recomposed the suffix. Global delivery failure is not a viable explanation because the same artifact visibly delivered `年`;
- user separately reported that the in-game HUD remained `1560年 2月30日` under DCTRL7. No DCTRL7 HUD screenshot was retained in R0, so this is recorded as a runtime observation with narrower provenance than the two retained screenshots;
- R489 positive-control text itself, standalone `月`, standalone `日`, and `はい` were not observed in the supplied DCTRL7 route and are not classified as runtime fail.

Retained screenshots in Google Drive `Test_Results/`:

- `DCTRL7_01_scenario_1560nyeon.jpg`, Drive ID `17XlqbJWd5aaEAUtsV0QRedPRNkKcPctR`, SHA-256 `5dc08060b4e0d18eecc962a7512347486b2253e20d2a1d9a5b361efa11e5f75f`
- `DCTRL7_02_basic_info_okazaki_castle_jp.jpg`, Drive ID `1eY4pPcBP80HnDfkSfodPTX5oi_C7ppjj`, SHA-256 `76a450b0770ab155c85f0e4272bc51bbe80daac78e5b764975f834dcd8bf25bb`

The exact installed internal Eden copy was not separately hashable. The user stated that DCTRL7 was registered and active; the complete concurrent add-on list was not retained.

## 4. RELA materialization

MOD0/dynamic parsing of the exact mapped Switch image gives:

- MOD0 at `0x8`
- dynamic table at `0x9FD708`
- `DT_RELA = 0x58D078`
- `DT_RELASZ = 0xECC70`
- `DT_RELAENT = 0x18`
- 40,410 RELA entries total
- 40,023 entries are relocation type `1027` (`R_AARCH64_RELATIVE`)

Selected repeated/composite objects are present as RELA addends:

| rodata object | RELA `.data` slots |
|---|---|
| `年` `0x69785A` | `0x9C3558`, `0x9C5238` |
| `%4d年%2d月%2d日` `0x68DD49` | `0x9C1040`, `0x9C2B58` |
| `%s城` `0x68A1FB` | `0x9C09F0` |
| standalone `城` `0x6A15DC` | `0x9C05A0`, `0x9C0EC8`, `0x9C4580`, `0x9C63B0` |

A narrow `.text` scan decoded AArch64 `ADR` and `ADRP+ADD` materialization for these exact rodata addresses. It found zero direct materializations for all four. This does **not** prove there are no indirect users; the RELA slots are the positive pointer evidence.

Therefore the correct R0 wording is:

> NSO loader RELA materializes these rodata addresses into `.data` pointer slots. Direct string-address XREF absence must not be treated as non-use. The later slot-reader -> consumer chain remains R1 work.

The stronger phrase "a game-code global string initializer does this" is not established and is rejected for now.

## 5. Place-table layout correction

The Japanese place table begins at mapped `0x6ADA10`, not `0x6ADA11`.

Three parallel bases are RELA-bound:

- `[0xA1C420] -> 0x6AF720`
- `[0xA1C428] -> 0x6ADA10`
- `[0xA1C430] -> 0x6B1430`

The bases are separated by `0x1D10 = 7,440 = 310 * 0x18`.

For the Japanese table, 310 consecutive records parse as:

```text
record size 0x18
+0x00  type/category : 1 byte
+0x01  name          : 11 bytes, NUL-padded
+0x0C  yomi          : 12 bytes, NUL-padded
```

Accessor-cluster raw instruction evidence:

- `0x1CC74C`: loads table pointer from global slot, multiplies index by `0x18`, then `LDRB` from record `+0`;
- `0x1CC770`: loads the `0xA1C428`/`0xA1C430` table pointers, computes `index * 0x18`, selects a record and reads record `+0`;
- `0x1CC7CC`: same stride model then forms a record `+1` pointer;
- `0x1CCCB4`: loads Japanese table pointer from `0xA1C428`, computes `index * 0x18`, then forms record `+0x0C`.

This corrects the earlier description that put category/type at the end of a record.

The exact semantic role/language of the two non-Japanese parallel tables is intentionally not named in R0.

## 6. Duplicate place-name census

Japanese table census:

- records: 310
- unique names: 277
- names occurring twice: 33
- slots belonging to duplicated names: 66
- type-pair distribution: `(0,3)=30`, `(0,5)=2`, `(3,0)=1`

Important fixed fields:

- `岡崎`: record 86 type 0, name `0x6AE221`; record 232 type 3, name `0x6AEFD1`
- `清洲`: record 89 type 0, name `0x6AE269`; record 233 type 3, name `0x6AEFE9`

The old simplification "all duplicate pairs are type 0/3" is rejected.

PC T5K was checked for every one of the 33 duplicated names. All matching PC records for each name use one consistent replacement byte sequence. `江戸`, `鳥羽`, and `洲本` have three matching PC T5K records rather than two; their three replacements still agree.

Examples:

- `岡崎`: R3424/R3718, original `89AA8DE800000000`, replacement `F2BEF54AF379F5AE`
- `清洲`: R3430/R3720, original `90B48F460000`, replacement `EBE0F2E2F1B8`

### Full duplicated-name matrix

| name | Switch `index:type:name_offset` | PC records | replacement | agree |
|---|---|---|---|---|
| 仙台 | 12:0:0x6ADB31; 211:3:0x6AEDD9 | R3275@0xB513C1; R3676@0xB52669 | `f15ded78f36b` | yes |
| 厩橋 | 36:0:0x6ADD71; 217:3:0x6AEE69 | R3324@0xB51601; R3688@0xB526F9 | `f2eaef55f27eefd7f1c1` | yes |
| 佐倉 | 43:0:0x6ADE19; 219:3:0x6AEE99 | R3338@0xB516A9; R3692@0xB52729 | `f0e5f58dee93` | yes |
| 江戸 | 45:0:0x6ADE49; 220:3:0x6AEEB1 | R3342@0xB516D9; R3694@0xB52741; R16394@0xC57C7A | `f29fedb3` | yes |
| 小田原 | 50:0:0x6ADEC1; 221:3:0x6AEEC9 | R3352@0xB51751; R3696@0xB52759 | `f2beed78f2cbee93` | yes |
| 富山 | 57:0:0x6ADF69; 223:3:0x6AEEF9 | R3366@0xB517F9; R3700@0xB52789 | `edb3f27eef55` | yes |
| 金沢 | 61:0:0x6ADFC9; 225:3:0x6AEF29 | R3374@0xB51859; R3704@0xB527B9 | `eb40eca8f379f2cb` | yes |
| 敦賀 | 67:0:0x6AE059; 226:3:0x6AEF41 | R3386@0xB518E9; R3706@0xB527D1 | `f251eee5eb40` | yes |
| 小諸 | 72:0:0x6AE0D1; 227:3:0x6AEF59 | R3396@0xB51961; R3708@0xB527E9 | `eb8def90eecc` | yes |
| 甲府 | 77:0:0x6AE149; 229:3:0x6AEF89 | R3406@0xB519D9; R3712@0xB52819 | `eb8df763` | yes |
| 駿府 | 80:0:0x6AE191; 230:3:0x6AEFA1 | R3412@0xB51A21; R3714@0xB52831 | `f1baf6a8` | yes |
| 浜松 | 83:0:0x6AE1D9; 231:3:0x6AEFB9 | R3418@0xB51A69; R3716@0xB52849 | `f6cdef55ef55f251` | yes |
| 岡崎 | 86:0:0x6AE221; 232:3:0x6AEFD1 | R3424@0xB51AB1; R3718@0xB52861 | `f2bef54af379f5ae` | yes |
| 清洲 | 89:0:0x6AE269; 233:3:0x6AEFE9 | R3430@0xB51AF9; R3720@0xB52879 | `ebe0f2e2f1b8` | yes |
| 岐阜 | 95:0:0x6AE2F9; 235:3:0x6AF019 | R3442@0xB51B89; R3724@0xB528A9 | `ebe0f763` | yes |
| 松倉 | 100:0:0x6AE371; 236:3:0x6AF031 | R3452@0xB51C01; R3726@0xB528C1 | `ef55f251f58dee93` | yes |
| 飛騨高山 | 101:0:0x6AE389; 237:3:0x6AF049 | R3454@0xB51C19; R3728@0xB528D9 | `f797aaf5b6d5f27eef55` | yes |
| 鳥羽 | 105:0:0x6AE3E9; 298:5:0x6AF601 | R3463@0xB51C79; R3852@0xB52E91; R16410@0xC57D0A | `edb3efd7` | yes |
| 今浜 | 108:0:0x6AE431; 239:3:0x6AF079 | R3469@0xB51CC1; R3733@0xB52909 | `f36bef55f6cdef55` | yes |
| 長浜 | 109:0:0x6AE449; 240:3:0x6AF091 | R3471@0xB51CD9; R3735@0xB52921 | `eca8eb40f6cdef55` | yes |
| 安土 | 111:0:0x6AE479; 242:3:0x6AF0C1 | R3475@0xB51D09; R3739@0xB52951 | `f265f3ecf540` | yes |
| 大坂 | 129:0:0x6AE629; 249:3:0x6AF169 | R3511@0xB51EB9; R3753@0xB529F9 | `f2bef0e5f54a` | yes |
| 雑賀 | 135:0:0x6AE6B9; 250:3:0x6AF181 | R3523@0xB51F49; R3755@0xB52A11 | `f0e5f36bf54a` | yes |
| 鳥取 | 137:0:0x6AE6E9; 251:3:0x6AF199 | R3527@0xB51F79; R3757@0xB52A29 | `edbcf5e2ef4d` | yes |
| 出石 | 138:0:0x6AE701; 252:3:0x6AF1B1 | R3529@0xB51F91; R3759@0xB52A41 | `f36bf3ecf1c1` | yes |
| 姫路 | 146:0:0x6AE7C1; 255:3:0x6AF1F9 | R3545@0xB52051; R3765@0xB52A89 | `f797ef7df3f4` | yes |
| 洲本 | 173:0:0x6AEA49; 299:5:0x6AF619 | R3600@0xB522D9; R3854@0xB52EA9; R16412@0xC57D1C | `f1b8ef90f5e2` | yes |
| 柳川 | 182:0:0x6AEB21; 267:3:0x6AF319 | R3618@0xB523B1; R3790@0xB52BA9 | `f27eeca8eb40f2cb` | yes |
| 平戸 | 187:0:0x6AEB99; 268:3:0x6AF331 | R3628@0xB52429; R3792@0xB52BC1 | `f797ee93edb3` | yes |
| 八代 | 193:0:0x6AEC29; 269:3:0x6AF349 | R3640@0xB524B9; R3794@0xB52BD9 | `f27ef251f1c1eecc` | yes |
| 小倉 | 197:0:0x6AEC89; 270:3:0x6AF361 | R3648@0xB52519; R3796@0xB52BF1 | `eb8df58dee93` | yes |
| 府内 | 198:0:0x6AECA1; 271:3:0x6AF379 | R3650@0xB52531; R3798@0xB52C09 | `f763eca8f36b` | yes |
| 津山 | 256:3:0x6AF211; 309:0:0x6AF709 | R3767@0xB52AA1; R3874@0xB52F99 | `f251f27eef55` | yes |

Internal yomi remains outside the proposed translation target.

## 7. PC place-fragment -> Switch formatter structural family

PC T5K R2552-R2563 are a consecutive 12-record place-suffix family. Switch has a consecutive 12-slot RELA-backed `%s...` formatter family at `.data 0x9C09F0..0x9C0A48`.

| PC | PC visible fragment | PC replacement | Switch formatter | Switch offset | RELA slot |
|---|---|---|---|---|---|
| R2552 | `城` | `f159` | `%s城` | `0x68A1FB` | `0x9C09F0` |
| R2553 | `館` | `f39af5c1` | `%s館` | `0x68DD09` | `0x9C09F8` |
| R2554 | `の町` | `ef55f35a` | `%sの町` | `0x69B4BF` | `0x9C0A00` |
| R2555 | `の里` | `ef55f35a` | `%sの里` | `0x68B6E8` | `0x9C0A08` |
| R2556 | `の砦` | `f2e2f0f3` | `%sの砦` | `0x691852` | `0x9C0A10` |
| R2557 | `寺` | `f3f4` | `%s寺` | `0x683EDB` | `0x9C0A18` |
| R2558 | `じょう` | `f15900000000` | `%sじょう` | `0x683EE0` | `0x9C0A20` |
| R2559 | `やかた` | `f39af5c10000` | `%sやかた` | `0x6A3D56` | `0x9C0A28` |
| R2560 | `のまち` | `ef55f35a0000` | `%sのまち` | `0x6A51EB` | `0x9C0A30` |
| R2561 | `のさと` | `ef55f35a0000` | `%sのさと` | `0x68DD0E` | `0x9C0A38` |
| R2562 | `のとりで` | `f2e2f0f300000000` | `%sのとりで` | `0x68A200` | `0x9C0A40` |
| R2563 | `じ` | `f3f4` | `%sじ` | `0x68DD17` | `0x9C0A48` |

This establishes the **static family correspondence**. It does not yet establish that the protagonist basic-information `岡崎城` screen consumes `%s城 @ 0x68A1FB`; that is reserved for consumer binding.

## 8. Date working set

PC T5K isolated suffix records:

- `年`: 5 records, all replacement `ECE0`
- `月`: 5 records, all replacement `F2F7`
- `日`: 9 records, all replacement `F36E`

The current Switch structural working set contains the following 11 standalone/composite candidates correlated with those PC contexts:

| Switch offset | object | RELA slots |
|---|---|---|
| `0x6A7BF9` | `%d年` | `0x9C3538` |
| `0x69785A` | `年` | `0x9C3558, 0x9C5238` |
| `0x68925A` | `月` | `0x9C5240` |
| `0x6A8ECD` | `% 2u月 % 2u日` | `0x9C61F0` |
| `0x695162` | `残%y日` | `0x9C2B40` |
| `0x69DD7B` | `残り%d日` | `0x9C2BB8` |
| `0x694360` | `60日` | `0x9C74E0` |
| `0x68A69B` | `20日` | `0x9C74E8` |
| `0x6A3CC6` | `日` | `0x9C0258, 0x9C5248` |
| `0x68DD49` | `%4d年%2d月%2d日` | `0x9C1040, 0x9C2B58` |
| `0x783F8A` | `%s %d年%d月%d日\n総時間：%d時間%02d分\n主人公：%s%s\n%s：%s\n%s\n%d年%d月%d日\n%s\n%s\n%d` | `none found` |

This list is **not** a verified claim that Switch has exactly 11 date objects, nor that every PC suffix record is already consumer-bound to one listed object. It is the R1/R2 working set.

`0x68DD49 = %4d年%2d月%2d日` is a strong candidate for the in-game HUD because its output form matches the observed `1560年 2月30日` and it is RELA-registered twice, but HUD consumer binding is not yet proven.

## 9. R0 conclusions

### Confirmed

- DCTRL7 delivered at least `年 @ 0x69785A` through the current Eden path and the Korean font rendered the replacement correctly.
- The tested basic-information `岡崎城` route does not use standalone `城 @ 0x6A15DC` as its sole effective suffix source.
- selected strings are materialized into `.data` through RELA; direct string-address XREF absence is not rejection evidence.
- Japanese place table base/layout is `0x6ADA10`, stride `0x18`, `type +0`, `name +1`, `yomi +0x0C`, 310 entries.
- 33 duplicated place names occupy 66 slots; type pairs are not uniformly 0/3.
- all PC replacements for each of the 33 duplicate names agree.
- PC R2552-R2563 and the Switch 12 `%s...` formatters form a strong static structural family.

### Likely, not yet consumer-bound

- in-game HUD date uses the `%4d年%2d月%2d日` family;
- basic-information `岡崎城` uses the `%s城` family;
- table type/category participates in runtime slot selection.

### Rejected/overstated

- `0x6ADA11` is a record base;
- category/type is at the end of the place record;
- all duplicate names are type 0/3 pairs;
- no direct `.text` XREF means a string is unused;
- standalone `年` or standalone `城` is a universal source for every screen;
- "game-code global initialization" has been established beyond loader RELA materialization.

## 10. Next authorized analysis

R1 should trace one complete positive path:

`rodata object -> RELA .data slot -> code reader -> consumer -> runtime screen`

The preferred anchor is runtime-confirmed standalone `年 @ 0x69785A`. R1 is not authorized by this R0 documentation update and requires a fresh user execution signal.
