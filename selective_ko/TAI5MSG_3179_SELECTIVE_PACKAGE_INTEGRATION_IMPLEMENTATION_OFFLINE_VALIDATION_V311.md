# TAI5MSG 3,179 Selective Package Integration Implementation / Offline Validation — V311

Date: 2026-09-18 (KST)

Validation ID: `V311`

Parent canonical state:

`9c78151aa6aa8250fe5a4aea0866df13b69b1c36` — V310 package-integration design.

Status:

`CLOSED / IMPLEMENTED / OFFLINE INTEGRATION PASS / NO PACKAGE PUBLISHED`

## 1. Scope

V311 implements and validates the isolated TAI5MSG package-integration layer defined by V310.

Created repository files:

```text
builder/selective_package.py
  Git blob 393e80004ec7b3c840457efb616e664a190965ac

tests/test_selective_package.py
  Git blob 5b6cc0caec02600727532788ad3c66c6cbff9d34
```

Existing `builder/selective_tai5msg.py`, `builder/t5k.py`, V303/V304 artifacts and historical builders are unchanged.

No release/test ZIP, mod directory, gameplay package or hardware execution is published by V311.

## 2. PC patch oracle gate

`PC_PATCH_ORACLE_GATE=PASS`

V311 consumes the actual PC patch evidence rather than reconstructing Korean data heuristically:

```text
PC dinput8.dll from canonical part02
  size    836,096
  sha256  ffe7e9da8e00c96bec631b45a3e9c4d3f314551623351f3e7024e0318913c6b7

T5K121R Mapping entries
  entries            10,036
  unique game codes  10,035
```

The 10,035 unique-code count is the inherited duplicate-code property of Mapping 10,036 and is not a new mapping defect.

## 3. Canonical offline inputs

Actual bytes used for the clean integration replay:

```text
Switch v1.1.3 main
  5,287,359 bytes
  b366e692208f3c0cc18bc1884ef95689b6b11d722fa2d749b8500abccbc3109b

stock TAI5MSG
  1,810,889 bytes
  aae037dd5948f79b9fc2e5affcb1e60e08efca39f897123045fe685786be978f

PC-KO TAI5MSG from canonical part02
  2,134,366 bytes
  e3b4522a1047ff409e099b5ee197d7689279ea7472cb403d305b2507fec96090

verified Mapping-only Eden package
  package sha256 e4810b8186bab484fc076419c1a882b7deb9031b09560d47a8eace00b5f49cca
  inner IPS sha256 6ff4b07db9b83b22197009206e21b5023ad02e62458e8597bac219a3c0faa120

V291 part00 font transport
  50,331,648 bytes
  04db6aea9dd18b686be4f500473493fbdaddcca0a6126f09ca48f227341053c9
```

The V309 clean workspace/artifacts were reused byte-for-byte instead of regenerating V303/V304 evidence.

## 4. Implementation boundary

`builder/selective_package.py` is intentionally an offline integration validator, not a package publisher.

It performs:

- exact Switch main SHA / Build-ID / segment-layout validation;
- actual PC `T5K121R` Mapping-source validation;
- V309 TAI5MSG reconstruction through `builder/selective_tai5msg.py`;
- exact verified four-record Mapping IPS consumption;
- all four Mapping preimage and payload guards;
- exact 44-byte page-mapper preimage/payload guards;
- action interval non-overlap validation;
- deterministic five-record Eden classic-IPS serialization and reparse;
- canonical Korean-font recovery from V291 part00 with part/member/SHA guards;
- exact four-path in-memory staging allowlist;
- deterministic `SELECTIVE_PACKAGE_INFO.json` bytes in memory only.

It does not:

- write a mod directory;
- write a final IPS to disk as a package artifact;
- write the reconstructed TAI5MSG/font into a package tree;
- create a ZIP;
- add inline 139;
- add historical 5,519;
- add W0/W1, CWTDAT, EVENT/SNR, name/yomi or pointer-56;
- perform hardware execution.

## 5. Unit/regression validation

Executed in the clean V309-derived workspace:

```text
existing selective_tai5msg tests   7 PASS
new selective_package tests        6 PASS
total                              13 / 13 PASS
```

New focused tests cover:

- page-mapper exact byte identities;
- five-record / 2,742-byte classic-IPS framing;
- RLE rejection;
- ExeFS overlap rejection;
- stored ZIP-member extraction;
- strict package allowlist / extra-file rejection.

## 6. Full canonical offline integration replay

Result:

```text
Switch main guard                 PASS
PC T5K Mapping source             PASS
Mapping entries                   10,036
unique Mapping game codes         10,035

TAI5MSG selected                  3,179
TAI5MSG unselected JP            11,653
TAI5MSG output bytes              1,841,481
TAI5MSG output sha256             dfcb928f694117bdd51e69d25daf337c14e30c3a7078da3961dc3a570ffe44f9

Korean font bytes                 16,779,036
Korean font sha256                c82d80dada61ce80db42f948eafd3eb5b8f3bed5725ceebbc1c0897246166932

Mapping-only IPS sha256           6ff4b07db9b83b22197009206e21b5023ad02e62458e8597bac219a3c0faa120
integrated IPS records            5
integrated IPS bytes              2,742
integrated IPS sha256             6d6989b4d22a12f0bc54e78a45a79944a9aaa0a6523d7d15fc5dc6d3620aaab4
page mapper mapped offset         0x44650C

in-memory staged file count       4
offline info sha256               90a7b81727c92525684b58d5187c794aec43eb36d6890177c32f13477f65ced6
published package                 false
```

The V310 predicted record count and IPS size are therefore reproduced by actual canonical bytes, not merely by arithmetic.

## 7. In-memory staged allowlist

The validated staged key set is exactly:

```text
SELECTIVE_PACKAGE_INFO.json
exefs/D9120950C258610A746F4A31CE3A3B376DE393D9.ips
romfs/FONT/FONT_JPN.G1T
romfs/TAI5MSG_JP.DAT
```

No extra asset is admitted.

This remains the bounded TAI5MSG integration slice. The separately approved inline 139 population is not silently merged into V311.

## 8. Rejected / preserved boundaries

Still rejected:

- legacy `builder/build.py` as selective package policy engine;
- bulk PC RomFS import;
- historical 5,519 inline import;
- V291 IPS inheritance;
- W0/W1 inclusion for this TAI5MSG population;
- generalizing Eden `mapped + 0x100` to physical Switch.

Preserved as open:

- inline 139 package integration as a separate carrier family;
- R2884/R2885;
- TAI5MSG 191 external-caller waits;
- EVENT/TS5 / SNR;
- layout/reflow and translation/content QA;
- physical Nintendo Switch delivery/validation.

## 9. Closure

```text
V310 package design                CLOSED
V311 integration implementation    PASS
V311 unit/regression tests         PASS 13/13
V311 canonical offline replay      PASS
V311 deterministic 5-record IPS    PASS
V311 font recovery                 PASS
V311 strict in-memory allowlist     PASS
published Eden package             NONE
hardware execution                 NONE
```

## 10. Next scope

After a fresh explicit user signal:

`TAI5MSG_3179_SELECTIVE_EDEN_TEST_PACKAGE_MATERIALIZATION`

That next scope may materialize exactly the V311-validated four-file Eden test-package tree and deterministic ZIP/manifest, place the large artifact in Google Drive, verify its identities, and stop.

It must not add inline 139 or any unrelated family and must not perform hardware execution.
