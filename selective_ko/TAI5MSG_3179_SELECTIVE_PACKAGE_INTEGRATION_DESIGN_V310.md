# TAI5MSG 3,179 Selective Package Integration Design — V310

Date: 2026-09-18 (KST)

Design ID: `V310`

Parent canonical state:

`5b757ec0230834d7ba1c36433afd48bd424b2c59` — V309 byte-exact offline replay closure.

## 1. Scope and authorization boundary

V310 defines the package-integration contract for the already verified TAI5MSG 3,179 selective payload.

This is a design/materialization stage only.

It creates no selective package builder, gameplay output, IPS, package ZIP, runtime package or hardware state.

The first integration target is Eden classic IPS delivery only. Physical Nintendo Switch / Atmosphere delivery remains a separate future transport scope because the verified Eden coordinate contract is `mapped + 0x100` and must not be generalized to another loader without evidence.

## 2. PC patch oracle gate

`PC_PATCH_ORACLE_GATE=PASS`

The relevant PC Korean patch evidence is already exact and must be reused rather than guessed:

- actual `dinput8.dll` `T5K121R` resource;
- Mapping 10,036 = original 7,494 + Korean 2,542;
- canonical Korean `FONT_JPN.G1T`;
- PC runtime-page-mapper semantics;
- actual PC-Korean TAI5MSG payload.

No Switch-specific replacement data may be invented where the PC patch already supplies the corresponding source authority.

## 3. Legacy integrated builder is not the selective package path

Existing `builder/build.py` is rejected as the selective package integration layer.

It currently combines unrelated historical/full-port behavior including:

- bulk PC `data/` import;
- 207 direct RomFS payload replacements;
- historical 5,519 unique-rodata inline replacements;
- legacy `builder/tai5msg.py` reconstruction;
- one historical page-mapper patch.

Those behaviors exceed the bounded V310 TAI5MSG selective slice and would violate the current `SWITCH_SELECTIVE_KOREANIZATION` product boundary.

Therefore:

```text
builder/build.py                 historical/reference only
builder/tai5msg.py               historical/reference only
builder/selective_tai5msg.py     authoritative TAI5MSG serializer
builder/selective_package.py     suggested new integration module
```

The selective package module must consume explicit approved components. It must not discover scope by importing everything present in the PC patch.

## 4. Authoritative input identities

### 4.1 Switch v1.1.3 main

```text
title id    0100346017304000
version     1.1.3
Build ID    D9120950C258610A746F4A31CE3A3B376DE393D9
main sha256 b366e692208f3c0cc18bc1884ef95689b6b11d722fa2d749b8500abccbc3109b
```

The main identity is required before any ExeFS action is emitted.

### 4.2 Stock TAI5MSG

```text
size    1,810,889
sha256  aae037dd5948f79b9fc2e5affcb1e60e08efca39f897123045fe685786be978f
```

### 4.3 PC Korean TAI5MSG

```text
size    2,134,366
sha256  e3b4522a1047ff409e099b5ee197d7689279ea7472cb403d305b2507fec96090
```

For the current transport, this exact member is recoverable from the existing split Korean patch `part02`; the 170 MB outer patch ZIP is not required.

### 4.4 V303 / V304 authority

The package integration must consume the same canonical V303 3,179-row membership and V304 two-row payload correction already enforced by `builder/selective_tai5msg.py`.

No package layer may add, remove or reinterpret TAI5MSG membership.

### 4.5 Canonical Korean font

```text
path    romfs/FONT/FONT_JPN.G1T
size    16,779,036
pages   64
sha256  c82d80dada61ce80db42f948eafd3eb5b8f3bed5725ceebbc1c0897246166932
```

The canonical Switch original font remains:

```text
size    13,108,628
pages   50
sha256  9c886848c31c31d09aeeed0ac5c44b909d561220110ca04da0f7fa32d3a0083e
```

V306 already established that pages 0..48 of the Korean font preserve the Switch-original texture bytes and that the effective TAI5MSG 992 Hangul codes have 992/992 non-empty glyph cells.

## 5. Korean font recovery route

The exact Korean font can be recovered without reassembling the 383 MB V291 package and without using the 170 MB PC patch ZIP.

Authoritative existing transport source:

```text
Drive folder  V291_HWTEST_PARTS
part          Taiko5DX_KR_V291_GRAMMAR125_HWTEST.zip.part00
part00 bytes  50,331,648
part00 sha256 04db6aea9dd18b686be4f500473493fbdaddcca0a6126f09ca48f227341053c9
```

The ZIP member is wholly contained in `part00`:

```text
member      Taiko5DX_KR_V291_GRAMMAR125_HWTEST/romfs/FONT/FONT_JPN.G1T
local hdr   27,513,210
data start  27,513,298
method      STORE / 0
stored size 16,779,036
sha256      c82d80dada61ce80db42f948eafd3eb5b8f3bed5725ceebbc1c0897246166932
```

A future implementation must verify the recovered font SHA before staging it.

The V291 package is used only as a byte-transport source for the already verified font asset. No V291 TAI5MSG, IPS, bulk RomFS content, grammar125 payload or historical full-port state may be inherited from that package.

## 6. Mapping 10,036 integration

The Mapping semantic authority remains the actual PC `T5K121R` 10,036-entry table.

For Switch runtime realization, reuse the already verified four-action family. Do not redesign it because V310 is a new integration stage.

```text
MAP10036_FWD_MISS_HOOK_V1
  mapped       0x4304E0
  size         4
  guard sha    98813cf6edbe59d962385f8bf0f1badd2557cf12ef0c35bc588aa9104f21d45b
  payload sha  2df5115d570e7775ce72bee4b267ffdc1f771f4e4feafcee253c72745f997d2d

MAP10036_REV_MISS_HOOK_V1
  mapped       0x430798
  size         4
  guard sha    196b4f3803e4f689fd5a889e142a35311b7bc5fcccabc1b700c39ebf406a1561
  payload sha  c92c275afc2d98a43dc2a0f7008bcd62bd4dda07fe4e540e45d33b5c7a80df7d

MAP10036_HELPER_TEXT_V2
  mapped       0x58CE60
  size         308
  guard sha    9575b2125169377b2ade7b401ea36c81228331d971f49664d9648d4f255d4868
  payload sha  f472326cab461ac8258282d5795031c33bcc52c9d2f1cd821b8eb6c94352f493

MAP10036_DELTA_RODATA_V1
  mapped       0x9BF018
  size         2,349
  guard sha    9bff4e0fc43a214b9efe2fddbcd29b1d1d61d2d278f89d34f9cd8b9c0f11516a
  payload sha  ddedc507fa892a5b5be6f35ab24f0a0e5fac0d71e633134712b33bd4c6a2088f
```

The four-action family already passed Eden runtime forward/reverse round-trip observation. V310 does not reopen that closed fact.

## 7. Page mapper integration

The deployed Korean page-mapper realization is required by the effective TAI5MSG population.

Mapped target:

`0x44650C`

Eden classic-IPS emitted offset:

`0x44660C`

Length:

`44 bytes`

Original:

```text
690a4011293d00123ffd2b7168010054093940510ae09b1208010a0b3f01007108b1891a087d0813007d0011
```

Original SHA-256:

`7fbdbe36095e02fd55ffd69dd671250c369be1e3b4cce68e576cab98082ade3b`

Replacement:

```text
693e08532a8103515f610071680100545f29007168000054407d00110400001440990011020000141f2003d5
```

Replacement SHA-256:

`f548a5c3ce313c1b578fe4867045c96abfae8b41ea76df09732baafb2fdbe050`

Semantic result:

```text
E0..EA -> pages 31..41
EB..F8 -> pages 49..62
F9     -> fallback
FA..FC -> existing pages 46..48 logic
```

The effective TAI5MSG uses Korean lead pages `EB..F7`, wholly inside this realization.

## 8. Dependency separation

The current TAI5MSG 3,179 output already contains game-code bytes.

Therefore its direct visible-render dependency is:

```text
selective TAI5MSG
 -> Korean page mapper
 -> Korean font
```

Mapping 10,036 is a separate Korean code-space / Unicode-conversion foundation and is still a package prerequisite under V307/V310.

Do not conflate these obligations into one causal claim.

V306 population facts remain binding:

```text
effective Korean Hangul codes    992
compact A1..DF Korean usage        0
PUA usage                           0
effective missing glyph cells      0
```

Consequently, W0/W1 compact A1..DF width changes are not required for this TAI5MSG population and are excluded from this integration stage.

## 9. Exact ExeFS action set

For the first Eden TAI5MSG integration slice, the ExeFS action set is exactly:

```text
4 Mapping 10,036 actions
1 page-mapper action
-------------------------
5 total IPS records
```

The action intervals do not overlap.

Eden classic-IPS serialization remains:

`emitted offset = mapped offset + 0x100`

No RLE records are authorized.

Given the already verified four-action Mapping IPS size of 2,693 bytes, adding the 44-byte page mapper as one non-RLE record gives the deterministic expected postcondition:

```text
record count  5
IPS size      2,742 bytes
```

These values are postconditions. An implementation must construct records from guarded actions and verify the result rather than hard-code bytes merely to reach the expected size.

## 10. Exact package allowlist

The bounded package root is:

`Taiko5DX_KR_SELECTIVE/`

Its allowed file set for this stage is exactly:

```text
Taiko5DX_KR_SELECTIVE/
├─ exefs/
│  └─ D9120950C258610A746F4A31CE3A3B376DE393D9.ips
├─ romfs/
│  ├─ TAI5MSG_JP.DAT
│  └─ FONT/
│     └─ FONT_JPN.G1T
└─ SELECTIVE_PACKAGE_INFO.json
```

The package layer must fail if any unapproved extra file exists.

Specifically forbidden:

- PC patch bulk `data/` import;
- historical 207 RomFS direct replacements;
- historical 5,519 inline patches;
- legacy grammar125 TAI5MSG output;
- V291 IPS or unrelated V291 RomFS payload;
- CWTDAT;
- EVENT/TS5;
- SNR;
- name/yomi/date-field Koreanization;
- W0/W1 compact-width changes;
- pointer-56;
- unrelated runtime descriptors.

The global selective corpus remains 3,318 rows, including 139 inline rows. Those 139 inline rows are not part of this bounded TAI5MSG package integration slice and must not be silently imported.

## 11. TAI5MSG output requirement

The package layer must invoke or consume the authoritative selective serializer result without altering it.

Required output identity:

```text
size    1,841,481 / 0x1C1949
sha256  dfcb928f694117bdd51e69d25daf337c14e30c3a7078da3961dc3a570ffe44f9
```

Required semantic postconditions remain:

```text
selected rows       3,179
unselected JP      11,653
messages           14,832
growth             +0x7780
B32 offset         0x1B4F00
B32 used-end       0xB8D5
B32 declared       0xCA80
B32 physical       0xCA49
B32 omitted        0x37
```

The package layer may not reserialize TAI5MSG with a separate algorithm.

## 12. Fail-closed validation order

A future implementation must be transactional and follow this logical order:

1. verify Switch main identity and Build ID;
2. verify stock / PC-KO TAI5MSG identities;
3. validate V303 / V304 artifacts through `builder/selective_tai5msg.py`;
4. construct the selective TAI5MSG in temporary storage;
5. require the V309 output identity and code-usage postconditions;
6. construct/reuse the exact four Mapping actions and verify every preimage/payload guard;
7. verify page-mapper original bytes and replacement identity;
8. reject any ExeFS interval overlap;
9. serialize exactly five Eden classic-IPS records;
10. independently reparse and require exact record identity, no RLE and no extra record;
11. recover the Korean font and require exact font identity;
12. stage only the four allowlisted package files;
13. audit the staged tree for unapproved extras;
14. emit `SELECTIVE_PACKAGE_INFO.json` only after every guard passes;
15. publish nothing if any check fails.

Minimum distinct error classes should include:

```text
SWITCH_MAIN_IDENTITY_MISMATCH
TAI5MSG_OUTPUT_IDENTITY_MISMATCH
MAPPING_ACTION_GUARD_FAIL
MAPPING_ACTION_PAYLOAD_FAIL
PAGE_MAPPER_GUARD_FAIL
PAGE_MAPPER_PAYLOAD_FAIL
FONT_IDENTITY_MISMATCH
EXEFS_ACTION_OVERLAP
IPS_RECORD_SET_MISMATCH
IPS_REPARSE_FAIL
PACKAGE_ALLOWLIST_FAIL
UNAUTHORIZED_ASSET_PRESENT
DELIVERY_PROFILE_MISMATCH
```

## 13. Delivery boundary

V310 authorizes design for the Eden classic-IPS profile only.

It does not assert that a physical Nintendo Switch / Atmosphere loader uses the same coordinate convention or package layout.

Physical Switch delivery requires a later, separately authorized transport analysis using the actual target loader/patch convention.

Do not reuse `mapped + 0x100` merely because it is correct for Eden.

## 14. Rejected package strategies

Rejected:

- extend `builder/build.py` into the selective package policy engine;
- copy all PC RomFS files and then remove unwanted ones;
- begin from V291 package and replace only TAI5MSG;
- inherit V291 IPS;
- mix historical 5,519 inline records into this TAI5MSG integration;
- add W0/W1 because they are font-related;
- treat Mapping 10,036 as the direct reason TAI5MSG glyphs render;
- omit Mapping because TAI5MSG itself already stores game codes;
- consume an unguarded Korean font file merely because the filename matches;
- package first and audit extras afterward;
- generalize the Eden IPS coordinate rule to physical Switch.

## 15. Next implementation scope

After a fresh explicit user signal, the next bounded scope is:

`TAI5MSG_3179_SELECTIVE_PACKAGE_INTEGRATION_IMPLEMENTATION_OFFLINE_VALIDATION`

That scope may:

- create `builder/selective_package.py`;
- add focused unit/regression tests;
- reuse the verified Mapping four-action implementation without reopening closed runtime evidence;
- integrate the exact V310 page-mapper/font guards;
- perform temporary/offline deterministic serialization needed to prove the implementation contract;
- verify strict package allowlisting.

It must still exclude:

- publishing a release package ZIP;
- user hardware package delivery;
- physical Switch/Atmosphere packaging;
- hardware execution;
- EVENT/SNR/CWTDAT/name/yomi/W0/W1/pointer-56 work;
- historical bulk/full-port payload import.

After the implementation/offline-validation report, another explicit user signal is required before creating a distributable Eden test package.
