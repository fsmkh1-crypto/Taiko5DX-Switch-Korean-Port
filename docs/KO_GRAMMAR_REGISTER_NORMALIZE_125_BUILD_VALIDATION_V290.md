# KO Grammar Register Normalize 125 Build Validation — V290

Date: 2026-09-17 (KST)
Status: PASS / CLOSED BUILD VALIDATION
Validation ID: `V290`
Scope: `KO_GRAMMAR_REGISTER_NORMALIZE_125_BUILD_VALIDATION`
New WRITE_SAFE authorization: 0
Hardware validation: NOT PERFORMED

## 1. Authority and inherited state

V290 inherits the canonical state at:

```text
main HEAD = f556429814f72565bcb0a6cb5485f8ebed934951
last closed validation = V289
V289 implementation commit = 13a7fae6ce2737a7bd3e5f22d1e306a906168673
```

V272-V289, FZ001, `PC_PATCH_ORACLE_GATE=PASS`, existing WRITE_SAFE authority,
rejected hypotheses, and unrelated project queues remain inherited unchanged.

The only newly validated cause-family delta in this build is the already-authorized
V288 grammar125 implementation introduced by V289.

## 2. Exact canonical builder identity

The authoritative build was executed with repository files byte-identical to V289 HEAD.

```text
builder/build.py
  Git blob = 6e9a98e46f96533eaee1a229201f8828bfa2ea39
  bytes    = 14,479
  sha256   = 8cd087a204ca0e6d0292f5bfd4c1338fad3812a0bae458a8339c283ff323698b

builder/t5k.py
  Git blob = fb0c2966bc61ecaa1dfcbb0447341f53dd923ac5
  bytes    = 12,446
  sha256   = 7557686824d7c5805a3ad5f75382a1b371648c4ca8c749c316c77065eca57028

builder/tai5msg.py
  Git blob = a1400db06828174fb6193eccb447bc16d7c2749e
  bytes    = 15,336
  sha256   = 7398b48626dc641fc995ee1c7e1215d37d0bfb901d6496056a36324ada1f7a62
```

The V288 manifest index and ordered shards were the canonical artifacts already
materialized under:

`selective_ko/artifacts/ko_grammar_register_normalize_125_static_write_v1/`

No manifest row or wording target was regenerated or re-adjudicated for V290.

## 3. Build input provenance

The build used the actual Switch v1.1.3 reference files from the project Drive and the
actual PC Korean v1.02 patcher EXE.

```text
Switch main
  bytes  = 5,287,359
  sha256 = b366e692208f3c0cc18bc1884ef95689b6b11d722fa2d749b8500abccbc3109b
  Build ID = d9120950c258610a746f4a31ce3a3b376de393d9000000000000000000000000

Switch FONT_JPN.G1T
  bytes  = 13,108,628
  sha256 = 9c886848c31c31d09aeeed0ac5c44b909d561220110ca04da0f7fa32d3a0083e

Switch CWTDAT_JP.TR5
  bytes  = 480,382
  sha256 = 8e03d5fd4630895b4a2763589aaa90f99bb9c37a4abbedb74e6078156c9c3290

PC Korean v1.02 patcher EXE
  bytes  = 177,267,850
  sha256 = 109dc729e66df8cd0a47c5f6c24719260eb03a89890a0c69d3ba739145dcfb23
```

The current builder interface accepts a ZIP containing the patcher EXE. A local transport
wrapper ZIP was therefore created around that exact EXE only. Its container identity is
not project authority; the inner EXE SHA-256 above is the authoritative PC-patch input.

## 4. Authoritative build result

The canonical V289 builder completed successfully.

```text
status                         ok
PC payload data files copied   207
PC CWTDAT skipped              CMENU/CWTDAT_JP.TR5
TAI5MSG reconstructed          yes
IPS records                    5,520
mapped inline patterns         5,519
mapped PC inline records       5,521 / 17,103
IPS payload bytes              75,739
```

T5K resource census remained:

```text
mapping entries                 10,036
original mapping entries         7,494
Korean additions                 2,542
inline records                  17,103
pointer records                     56
runtime descriptors                 11
pointer string pool bytes          602
runtime helper blob bytes          158
```

## 5. TAI5MSG build-level closure

The emitted `romfs/TAI5MSG_JP.DAT` exactly reproduced the V288/V289 authorized identity.

```text
input sha256       e3b4522a1047ff409e099b5ee197d7689279ea7472cb403d305b2507fec96090
output sha256      993d3fc29cabe002d4a2071fe4b0c39fb9c3799dd9e33a7bd68349c7f8ef4b06
input bytes        2,134,366
output bytes       2,134,366
size growth        0
blocks             33
messages           14,832
changed messages   158
affected blocks    17
grown blocks       0
compact occurrences 44
```

Therefore the V289 builder implementation reproduces the exact V288 deterministic
whole-file identity through the full integrated builder path.

## 6. Other emitted identities

```text
patched FONT_JPN.G1T
  bytes  = 16,779,036
  sha256 = c82d80dada61ce80db42f948eafd3eb5b8f3bed5725ceebbc1c0897246166932

Eden classic IPS
  bytes  = 103,347
  sha256 = ea6bd258e459e913356be68a177efdb48e33eb103cb0c10e378d88133b57408d

BUILD_REPORT.json
  bytes  = 2,797
  sha256 = f826622c02c8941551a3c268364ab08e98d31a5c9028b98c5814269a28adf13f
```

`romfs/CMENU/CWTDAT_JP.TR5` is absent from the emitted mod by design. The canonical
builder explicitly skips PC CWTDAT until the separate Switch-native CWTDAT queue is closed.

## 7. Closure / authorization boundary

V290 closes grammar125 at build level:

```text
V288 static-write authorization     PASS / CLOSED
V289 builder implementation         PASS / CLOSED
V290 integrated build validation    PASS / CLOSED
```

WRITE_SAFE remains exactly 287:

```text
F1 DIRECT_PORT        158
Mapping                 4
grammar125            125
TOTAL                  287
```

V290 does not validate hardware/runtime behavior and does not close unrelated F1,
Mapping, CWTDAT, name/yomi, pointer, or formatter/runtime queues.

No new code/gameplay mutation was introduced during V290.

## 8. Next scope / STOP

The next eligible grammar125 scope under a fresh explicit execution signal is:

`KO_GRAMMAR_REGISTER_NORMALIZE_125_HARDWARE_VALIDATION_PACKAGE`

That scope may package the already validated V290 build output and place the large test
artifact in the project Google Drive with its exact package hash. It must not add new
cause-family fixes.

Actual hardware validation remains a subsequent separate scope after the package is
available to the user.
