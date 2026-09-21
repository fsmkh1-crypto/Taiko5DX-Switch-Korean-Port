# ECF00000 V363-added %12 Switch-main dispatch direct evidence — V364

Date: 2026-09-21 (KST)

```text
validation_id   V364
track           SWITCH_SELECTIVE_KOREANIZATION
scope_kind      READ_ONLY_DIRECT_BINARY_DISPATCH_EVIDENCE_CLOSURE
parent          8f0b49b7c0287406709edc5b45b3d053885cd0bb
implementation  NONE
product bytes   UNCHANGED
build/package   NONE
hardware        NOT RUN
```

## 1. Scope

This validation closes only the previously unresolved direct Switch ownership proof for the one
V363-added independent percent-macro occurrence:

```text
row 15277
partition 618
original offset 0xC77E0
PC-KO offset    0xF8860
macro           \%12
```

The broader V363 added-2,876 downstream policy/cross-carrier audit remains read-only and is not
implemented here.

## 2. Exact Switch source

The audited Nintendo Switch v1.1.3 NSO `main` is the existing Drive source:

```text
Drive project path  태합입지전 프로젝트/Switch/main
Drive file id       1rj18c0Py5jp1zCj4x78m7guGc10EUzUh
bytes               5,287,359
SHA-256             b366e692208f3c0cc18bc1884ef95689b6b11d722fa2d749b8500abccbc3109b
NSO magic           NSO0
```

This SHA is byte-exact with the required audit input.

## 3. RODATA integrity

NSO segment metadata and independent decompression give:

```text
RODATA file offset          0x343D31
RODATA compressed bytes     0x1C0BFF
RODATA memory base          0x58D000
RODATA decompressed bytes   0x432018
RODATA SHA-256              4dd81f6bb7c899375e428a881abf6d2ca561d074e7c9ca760ad001becd2ac00b
NSO header RODATA hash      SAME
hash validation             PASS
```

Therefore the dispatch bytes below come from an integrity-checked RODATA image of the exact main.

## 4. 52-entry percent dispatch table

Inherited V353 owner location:

```text
table VA            0x6AC004
entry count         52
entry width         4 bytes / little-endian uint32
RODATA-relative     0x11F004
table byte length   208
table SHA-256       f8a329319321f2b249422d8c6c7d88064376f1d7ff08c8f7de92a57f59711333
```

For `%12`, hexadecimal macro index `0x12` selects table entry 18:

```text
entry VA            0x6AC004 + (0x12 * 4)
                    = 0x6AC04C
raw bytes           B5 00 00 00
little-endian value 0x000000B5
decimal value       181
```

Direct binary result:

```text
%12 -> dispatch value 181
```

## 5. Cross-checks in the same raw table

The exact same 52-entry table reproduces already established neighboring / V353 bindings:

```text
%11 -> 174
%12 -> 181
%13 -> 188
%15 -> 209
%21 -> 349
%2A -> 395
```

Thus the earlier array/semantic inference for `%12` is superseded by direct Switch-main evidence.

## 6. TAI5MSG owner conclusion

V353 already established the Switch TAI5MSG getter at `0x43F2A4` and the message-ID split:

```text
block = message_id / 1000
local = message_id % 1000
```

V364 does not reopen that closed getter proof. Combining that inherited VERIFIED rule with the new
direct dispatch value gives:

```text
%12
 -> message_id 181
 -> TAI5MSG block 0
 -> local 181
 -> B0:181
```

Therefore:

```text
%12 -> B0:181 = DIRECTLY CLOSED
```

The corresponding PC-KO B0:181 payload remains the previously audited 339-byte negative-form
selector family; no TAI5MSG mutation is authorized by V364 itself.

## 7. Rejected / do-not-repeat

- treating `%12 -> 181` as only an interpolation from `%11` and `%13`;
- promoting the inference without the exact Switch binary;
- reopening the already VERIFIED V353 getter rule solely because this is a new validation;
- treating `%04/%20` argument-bearing EVENT references as independent B0 roots;
- mixing 5A/1E/3C, relocation replay, implementation, build, package, IPS, or hardware into this proof.

## 8. Product impact boundary

V364 changes no product bytes.

The V363-added independent-percent census can now treat its formerly uncovered single `%12`
occurrence as having exact runtime owner `TAI5MSG B0:181`. The V357 46-root implementation did
not contain this newly observed root, so downstream policy/capacity/relocation consequences remain
part of the broader V363 added-row audit and are not decided here.

## 9. Exact next scope

`ECF00000_V363_ADDED_2876_DOWNSTREAM_POLICY_AND_CROSS_CARRIER_IMPACT_AUDIT_READ_ONLY`

Continue the already-open V363 added-row audit with `%12 -> B0:181` treated as VERIFIED direct
binary ownership. No implementation, EVENT/TAI5MSG mutation, build/package/IPS, or hardware
without a fresh explicit user execution signal.
