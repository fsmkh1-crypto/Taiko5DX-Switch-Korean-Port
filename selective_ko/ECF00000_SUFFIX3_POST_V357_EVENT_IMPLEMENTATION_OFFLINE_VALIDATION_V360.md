# ECF00000 suffix-three post-V357 EVENT implementation / offline validation — V360

Date: 2026-09-21 (KST)

```text
validation_id   V360
track           SWITCH_SELECTIVE_KOREANIZATION
parent          21f3fa02568c4ea8ac10dfb44b3532b0ddbc217d / V359
scope_kind      IMPLEMENTATION_AND_OFFLINE_VALIDATION
implementation  IMPLEMENTED
package/IPS     NONE
runtime         NOT RUN
```

## 1. Scope

V360 implements only the exact V353 cross-carrier suffix-three EVENT rows after the V357 TAI5MSG
B0 dependency closure. It does not modify TAI5MSG, ordinary non-B24 584 reflow, inline 139, SNR,
font, IPS, or package contents.

Exact rows:

```text
4743   partition 208   original 0x60248   PC-KO 0x78624   \%21 -> B0:M349
5059   partition 215   original 0x64898   PC-KO 0x7DC28   \%15 -> B0:M209
11440  partition 604   original 0xC3988   PC-KO 0xF3C9C   \%2A -> B0:M395
```

## 2. Source authority

Canonical inputs:

```text
stock ECF00000.TS5
  931,936
  bbaaff8dc552da17a49ea2e6ce49a76da662541ee22fdec7dc7933046430bf09

PC-KO ECF00000.TS5
  1,156,480
  0899bf81789acfbd243d43be209a8a3960933fa090960ac8c753c63f95f07bbe

V352 diagnostic baseline
  1,109,356
  e61569508ffc9995f78df51f01b42be5402b79d5e26a8c8f3e71c0448d8eaaeb

required V357 TAI5MSG
  ad91776d47c3170573bed063dd6677716833e3a138be27474373ef5d2782e794
```

The PC-KO source was re-extracted from the actual v1.02 patcher:
outer ZIP `df1b62de...`, EXE `109dc729...`, embedded payload `eebc7aa1...`.
The extracted ECF00000 identity matches the canonical PC-patch authority exactly.

## 3. Exact applicability

`selective_ko/artifacts/ecf00000_v360_suffix3_post_v357_event_v1/APPLICABILITY.jsonl`

```text
rows      3
bytes     1,385
sha256    f92b9e8f2ad7ff5c904cbbbd3ca1932f70a85050ed93591ff718f597cd777b5b
```

Per-row exact command identities:

```text
row 4743
  source 72  / 51929405255cb459fce3919838062d8d16b5b445aef07dc7d3972901293c0172
  target 100 / 4135f259154a507d2576fe796f5a8e0309c504f5750ff5753e5ee52a29002964
  growth +28

row 5059
  source 56  / bdb8fe417a78e765858d69c51f81b40e178346aebec8344444c57e16f66eaf3a
  target 76  / 016a8dac91b0caf70f7ca7157c87817319e53a73d91d202297ff7e8ade8728b9
  growth +20

row 11440
  source 56  / c71384be023c392fb79201c29c7ae66b29343777367e345f2f80ab67ae00d494
  target 92  / a44fbb9b8ccc43e2f3cda7e4963e717319347fe0af30e53aa8b864cf9e1586ff
  growth +36
```

All three target rows are still exact stock bytes in V352 before V360 application.

Cross-carrier target hashes are bound to the already-closed V357 roots:

```text
B0:M209  05e3c0397482ce98b34f89de3e67cc32e1e070e05801ff72b2790ebcbf441267
B0:M349  706bfadf482b6848c058e242994288529380ad5b1113282987bde80987e4d98e
B0:M395  ad90e66db5e87b245a5ee6ad03243f7b6f4edac6dde2a33a59564f77e049c545
```

## 4. Implementation

New module:

`builder/selective_event_suffix3.py`

New test:

`tests/test_selective_event_suffix3.py`

The implementation:

1. consumes only the exact V360 three-row applicability;
2. requires exact original owner bytes and SHA;
3. slices exact same-locator PC-KO command bytes by canonical offset/length;
4. requires exact target SHA and one expected %xx macro occurrence;
5. binds each EVENT row to its exact V357 B0 target hash;
6. performs no particle heuristic, translation synthesis, or global search/replace.

Module report:

```text
rows                         3
source command bytes       184
target command bytes       268
payload growth             +84
opcode 0x11                  3
transformed corpus sha256   8ab2e7701676348e1434674135a97fa3140f8c17276ca7f88489155060e40bfe
```

Dedicated tests: `PASS_3_OF_3`.
Module py_compile: `PASS`.

## 5. Whole-context replay

V352 was parsed with the stock grouping contract. All 782 partitions retain exact grouped-item
cardinality relative to stock, permitting source-item ordinal binding without final-Korean ownership
rediscovery.

After exact three-row overlay, V337 generic relocation was recomputed from the frozen stock plans:

```text
generic plans             7,579
generic owner changes         4
special span plans            3
special owner changes         0
false EVENT-02 owners     2 / 2 unchanged
unexpected changes             0
```

The four changed generic owners are exact opcode-0x04 source owners:

```text
partition 208  original 0x601A4
partition 215  original 0x64884
partition 215  original 0x64894
partition 604  original 0xC3960
```

Mutation accounting versus V352:

```text
changed logical items      7
target payload items       3
generic relocation owners  4
special owners             0
unexpected                 0
```

All grouped opcode-0x5A items remain byte-identical to V352. The existing V339 semantic/runtime
5A state is therefore not reopened.

## 6. Residual / alias differential gate

The V340 inherited logical residual remains the same source object:

```text
partition         593
original anchor   0xBDD78
header            0E 02 D5 1F
decoded length    0x7F5408
V352 current      0xE3364
V360 current      0xE3394
shift             +0x30
```

The shift is exactly the +48 bytes introduced in partitions 208 and 215 before partition 593.
The logical residual key is unchanged.

The V344 source-alias bytes in partition 604 remain unchanged:

```text
original 0xC373C parent  0B DC 17 00
original 0xC3740 alias   0E 00 9D 06
```

The V360 target in partition 604 begins later at original 0xC3988, so it does not mutate the alias
owner bytes. The differential gate is therefore replayed at canonical logical-provenance level:
the inherited residual remains inherited, no residual-owner header is newly mutated, and the prior
alias bytes remain source-proven. The historical conservative MAY-walker executable itself is not
a repository production component and is not promoted as product authority.

## 7. Exact output identity

Two independent deterministic replays produce identical bytes:

```text
bytes      1,109,440
sha256     4b31d771c9bb3736d7cbc5fc95c1a4e4c54a55e43f38606227cca32ecb22045d
delta V352 +84
rerun      PASS_BYTE_IDENTICAL
```

Only partitions 208, 215 and 604 change in physical payload size:

```text
P208  +28
P215  +20
P604  +36
```

## 8. Drive archive

```text
folder  1Jf7p384tCyu6Ir_GmE9HqbYjxJ_cUgD6
EVENT   1W2OhLHRemlqwmuQLRDbjXKsOUGAnWsAY
report  1wgneAnFzSspztvs7lJl4u_JhrIgzPwlj
```

Downloaded roundtrip:

```text
EVENT   PASS_BYTE_IDENTICAL / 4b31d771c9bb3736d7cbc5fc95c1a4e4c54a55e43f38606227cca32ecb22045d
report  PASS_BYTE_IDENTICAL / ad1de5ec983c0c59f6e3d1c6ce09618ff1241692dfde8c7fdd334be360940761
```

## 9. 확정된 사실

- the exact three V353 EVENT rows are now implemented;
- the old V353 cross-carrier blocker is closed because V357 already supplies all three B0 roots;
- output growth is exactly +84 bytes;
- mutation accounting is 3 target + 4 generic owners, with zero unexpected changes;
- V337 generic / V338 special / false-02 / V339 5A invariants remain satisfied;
- deterministic output and Drive roundtrip are byte-identical;
- no package or runtime test is part of V360.

## 10. 유력한 가설

Combining this V360 EVENT with the exact V357 TAI5MSG in the already-verified IPS/font package route
should restore the ordinary EVENT dialogue family that was absent in V358.

This remains a runtime hypothesis.

## 11. 미확정 사항

- Eden runtime behavior of the integrated V360 EVENT + V357 TAI5MSG package;
- ordinary non-B24 584 reflow;
- inline 139 implementation;
- exact SNR ownership of the scenario synopsis screenshot.

## 12. 기각된 가설 / do-not-repeat

- package raw V352 as final EVENT — REJECTED;
- patch only TAI5MSG roots without the three dependent EVENT rows — REJECTED;
- treat suffix `는` as a noun particle — REJECTED;
- combine EVENT completion and 584 reflow in the same diagnostic build — REJECTED;
- reopen B24 108 native-wrap rows — REJECTED.

## 13. 관련 영향 범위

Changed:

- exact EVENT rows 4743 / 5059 / 11440;
- four source-proven generic relocation owners;
- resulting outer partition offsets;
- V360 builder/test/artifacts/state.

Unchanged:

- V357 TAI5MSG bytes;
- TAI5MSG non-B24 584 reflow;
- inline 139;
- SNR;
- Mapping/font;
- IPS;
- package/hardware.

## 14. 수정 제안 / exact next scope

`ECF00000_V360_EVENT_V357_TAI5MSG_EDEN_DIAGNOSTIC_PACKAGE_MATERIALIZATION`

Under a fresh explicit user signal, build an isolated package containing exactly:

```text
romfs/EVENT/ECF00000.TS5   V360 / 4b31d771...
romfs/TAI5MSG_JP.DAT       V357 / ad91776d...
existing verified FONT
existing verified IPS
```

Do not add the 584 reflow, inline 139, SNR, or unrelated translation work in that package.
