# KO Grammar Register Normalize 125 Hardware Validation Package — V291

Date: 2026-09-17 (KST)
Status: PASS / PACKAGE READY / HARDWARE NOT YET EXECUTED
Validation ID: `V291`
Scope: `KO_GRAMMAR_REGISTER_NORMALIZE_125_HARDWARE_VALIDATION_PACKAGE`
New gameplay fix: 0
New WRITE_SAFE authorization: 0

## 1. Inherited authority

V291 inherits V290 without reopening V288/V289/V290.

```text
canonical main before V291 = d78af420d83516adcdae607e3dadf2d7d01c8f6e
V290 TAI5MSG sha256        = 993d3fc29cabe002d4a2071fe4b0c39fb9c3799dd9e33a7bd68349c7f8ef4b06
V290 FONT sha256           = c82d80dada61ce80db42f948eafd3eb5b8f3bed5725ceebbc1c0897246166932
V290 IPS sha256            = ea6bd258e459e913356be68a177efdb48e33eb103cb0c10e378d88133b57408d
```

No builder, manifest, wording, gameplay data, IPS logic, or other cause family was modified.

## 2. Shortest-path artifact recovery

The already existing local V291 candidate ZIP was inspected directly; no rebuild or builder execution was performed in V291.

The ZIP was extracted and its three authoritative V290 identities were checked byte-for-byte by SHA-256:

```text
romfs/TAI5MSG_JP.DAT
  sha256 = 993d3fc29cabe002d4a2071fe4b0c39fb9c3799dd9e33a7bd68349c7f8ef4b06
  result = MATCH V290

romfs/FONT/FONT_JPN.G1T
  sha256 = c82d80dada61ce80db42f948eafd3eb5b8f3bed5725ceebbc1c0897246166932
  result = MATCH V290

exefs/D9120950C258610A746F4A31CE3A3B376DE393D9.ips
  sha256 = ea6bd258e459e913356be68a177efdb48e33eb103cb0c10e378d88133b57408d
  result = MATCH V290
```

Therefore the package is a byte-identical transport of the V290 validated payload for these authoritative components.

## 3. Package identity

```text
package = Taiko5DX_KR_V291_GRAMMAR125_HWTEST.zip
bytes   = 382,935,991
sha256  = c5a560a2fe4fdcec3c0ec5b6b2ac90efb2c3e57db211f65c2e6729ec38faba3d
```

The package contains the V290 mod payload and `V291_PACKAGE_INFO.json`. CWTDAT remains excluded according to the canonical builder policy; no name/yomi/CWTDAT change is included.

## 4. Google Drive transport

The single 383 MB ZIP could not be sent through the available direct Drive upload route. Transport was therefore split without recompression or content change into eight ordered binary parts.

Drive folder:

```text
/Google Drive/GPT/태합입지전/V291_HWTEST_PARTS
folder id = 1TZSn4_87QyQQhxf8CJ9beCAY9vQ5qCOq
```

Parts:

```text
part00  50,331,648  04db6aea9dd18b686be4f500473493fbdaddcca0a6126f09ca48f227341053c9
part01  50,331,648  7c6846ad80870b4b3558f43a83aee78df67fc4a29484b98919cfe7da9bd1102e
part02  50,331,648  411beddffc92159a5a61bb4c9b3fdf1c0d4284bd72abdfe5e15aced6b1075282
part03  50,331,648  4d6a2fe5e3ce5a9d02010cf3674ea2805c7aa81a78096dcb52e8299fd0f98be0
part04  50,331,648  5b742287bbfdebb40e1a2d6bc9753a2e2af7e0e2cc1049db9369fb206aca7bbd
part05  50,331,648  46902e398a97b501721f20f4e00243d0ded2c1cde842934df6168152739c6040
part06  50,331,648  b3c09266b5dce16d317a9529c899519f89d6511b825c053d6aed5f30c56843d3
part07  30,614,455  fca0d7a5c154f986971e42225dc22045b38b30f0bd3b8208ac32b1cb4d35404e
```

Concatenating `part00` through `part07` in lexical order was locally replayed and reproduced the exact full-package SHA-256 `c5a560a2fe4fdcec3c0ec5b6b2ac90efb2c3e57db211f65c2e6729ec38faba3d`.

`V291_HWTEST_PACKAGE_MANIFEST.json` is stored in the same Drive folder.

## 5. Authorization boundary

V291 closes packaging/transport only.

```text
V288 static-write authorization  CLOSED
V289 builder implementation      CLOSED
V290 integrated build validation CLOSED
V291 hardware package            READY
hardware execution               NOT YET PERFORMED
```

WRITE_SAFE remains exactly 287. No unrelated F1, Mapping, CWTDAT, name/yomi, pointer, or formatter/runtime queue is changed by V291.

## 6. Next scope / STOP

The next eligible scope under a fresh explicit execution signal is:

`KO_GRAMMAR_REGISTER_NORMALIZE_125_HARDWARE_EXECUTION_VALIDATION`

That scope must use the V291 package unchanged and record only the observed hardware/runtime result for this grammar125 cause family. New fixes must not be mixed into that validation run.
