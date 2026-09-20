# ECF00000 SELECTIVE EVENT SWITCH SPECIAL OWNER IMPLEMENTATION / OFFLINE VALIDATION — V338

Date: 2026-09-20 (KST)

```text
validation_id   V338
track           SWITCH_SELECTIVE_KOREANIZATION
scope_kind      IMPLEMENTATION_AND_OFFLINE_VALIDATION
parent          4e52488e495d5c136cf7f4aadc400e9c55f8020f / V337
stage           S3_SWITCH_SPECIAL_OWNER_ONLY
product_bytes   UNCHANGED
build/package   NONE
hardware        NOT RUN
```

V338 implements only the three Switch-specific dynamic-span owners already fixed by V333/V334 and locks the two false EVENT-`0x02` expression operands as non-owners. It does not apply any V334/V335 Korean payload.

## 1. Authority

The ordinary relocation engine remains V337/PC editor v0.30 authority. Switch runtime is authority only for these exceptional runtime owners.

PC editor source provenance remains:

```text
archive size       3,379,608
archive sha256     0f0df73e9d79355687e7a95c35b8bacb1fcdf1f83d0a80d5abeb105514bde903
Form1.vb size        296,505
Form1.vb sha256     dc41d778ab11268fc137d0b995bc5cff14d0fcec127e020803c6dc838523e14d
```

The editor remains authoritative for edit partition/grouping and ordinary branch preservation, not for these Switch runtime exceptions.

## 2. Exact special-owner anchors

Stock `ECF00000.TS5` was replayed from exact original bytes.

```text
owner       kind       partition  owner item  inner  original target  original span
0xCBBB0     EVENT_04      626          3        4      0xCBD78          456
0x65F40     EVENT_04      218         69        4      0x65F9C           92
0x7E1B0     BRANCH_09     290          1        0      0x7EBE4         2612
```

For both special EVENT `04` owners, PC editor grouping merges the preceding `17` and the real `04` into one 8-byte item. The actual runtime owner is therefore fixed as inner offset +4 of that original grouped item.

All three original targets are exact grouped-item boundaries.

For `0x7E1B0`, `0x7EBE4` is additionally the exact next physical raw `09` boundary, confirming the inherited Switch-runtime interpretation.

## 3. Implemented dynamic calculation

Updated module:

`builder/selective_event.py`

Added:

- `SwitchSpecialSpanPlan`;
- exact original owner/target anchor discovery;
- inner-item owner offset support for the two merged `17 + 04` cases;
- final span calculation from current grouped-item lengths without final-Korean reparsing;
- EVENT-`04` field rewrite as `span * 2`;
- BRANCH-`09` Switch-runtime rewrite preserving low 19 instruction bits and replacing only the high runtime span units;
- overflow and representability gates;
- exact-next-physical-`09` validation for `0x7E1B0`;
- `FalseEvent02NonOwner` validation for `0xAC470 / 0x980C0`.

For special BRANCH `09`:

```text
runtime span = (word >> 19) << 2
rewrite:
  preserve word & ((1 << 19) - 1)
  require span % 4 == 0
  replace high 13 bits with span / 4
```

This differs intentionally from the ordinary PC-editor `09` preservation arithmetic used in V337.

## 4. Stock unchanged replay

The three plans were analyzed from stock and reapplied with unchanged grouped-item lengths.

```text
0xCBBB0  span  456  04 01 90 03 -> 04 01 90 03
0x65F40  span   92  04 01 B8 00 -> 04 01 B8 00
0x7E1B0  span 2612  09 F0 6F 14 -> 09 F0 6F 14

special plans                3
changed headers              0
result             PASS_BYTE_EXACT
```

## 5. Controlled +4 length-change replay

For each special owner, the last grouped item before its frozen target boundary was increased by four bytes.

```text
0xCBBB0  456 -> 460   04 01 98 03
0x65F40   92 ->  96   04 01 C0 00
0x7E1B0 2612 -> 2616  09 F0 77 14

validated  3 / 3
failures   0
result     PASS
```

The `09` validation also confirms that the low 19 instruction bits remain unchanged.

## 6. Full-PC-KO diagnostic-vector regression

The encoder was checked against the already-canonical V333 full-PC-KO diagnostic spans without using those bytes as hardcoded output.

```text
owner       diagnostic span   expected diagnostic header
0xCBBB0          628           04 01 E8 04
0x65F40          128           04 01 00 01
0x7E1B0         3524           09 F0 8F 1B
```

All three are reproduced exactly by the dynamic encoder.

This is a regression oracle only. Final selective output must use its actual rebuilt layout.

## 7. False EVENT-02 non-owner lock

The two original-side expression operands are:

```text
0xAC470
0x980C0
```

Validation requires:

- raw byte at the anchor is `0x02`;
- the enclosing expression begins with raw EVENT `0x0A` eight bytes earlier;
- the anchor is not a TS5 entrypoint;
- the grouped item starts at the exact anchor;
- V337 generic branch analysis does not promote it.

Both anchors pass and remain mutation-free expression data.

## 8. V337 repository test-fixture correction

Pre-main V338 validation exposed a repository-test defect inherited from V337.

The V337-added unit fixtures contained doubled Python byte escapes such as:

```text
b"\\\\x02\\\\x03..."
```

instead of executable byte literals:

```text
b"\\x02\\x03..."
```

Impact audit:

```text
builder/selective_event.py doubled-escape hits   0
V337 test lines affected                         14
V338 draft test lines additionally affected       5
production EVENT bytes                            0
main V338 publication                              none before correction
```

The cause is test-source string escaping during repository materialization, not the S2 relocation arithmetic itself.

V338 corrects the entire affected test-literal family before publication and revalidates S2 with both corrected unit fixtures and the exact stock full-corpus gates:

```text
S2 corrected unit tests                PASS_4_OF_4
S2 generic plans                       7,579
S2 stock unchanged replay              PASS_BYTE_EXACT
S2 controlled +4 replay                PASS_7578_OF_7578
```

Do not use test-method count as evidence of execution. Future checkpoints must distinguish source presence from actual test execution.

## 9. Unit/offline validation

Repository test file now contains the V336/V337 tests plus four S3 tests:

- merged-item EVENT-`04` inner-owner anchor;
- BRANCH-`09` runtime bitfield preservation;
- BRANCH-`09` non-multiple-of-four rejection;
- false-`02` non-owner exclusion invariant.

Corrected repository test-method total:

```text
V336  8
V337  4
V338  4
total 16
```

Corrected EVENT unit suite: `PASS_16_OF_16`.

Exact stock offline gates:

```text
special-plan discovery        PASS_3_OF_3
stock special replay          PASS_BYTE_EXACT
controlled +4 replay          PASS_3_OF_3
full-KO diagnostic vectors    PASS_3_OF_3
false EVENT-02 nonowners      PASS_2_OF_2
```

## 10. Scope boundary

V338 closes the S3 special-owner cause-family only.

Still not implemented:

- V334/V335 selective replacement application;
- `FIXED_SURFACE_PARTICLE_V1`;
- EVENT reflow;
- final TS5 output;
- package/build/IPS;
- hardware execution;
- other EVENT files;
- SNR.

## 11. Rejected / do-not-repeat

Do not:

- run the two special `04` owners through ordinary PC-editor grouped-owner discovery;
- calculate the special `09` using ordinary PC-editor `09` arithmetic;
- hardcode the full-PC-KO diagnostic headers;
- find targets by fresh-parsing final Korean bytes;
- treat `0xAC470 / 0x980C0` as branches because their first byte is `02`;
- interpret V338 as authorization to apply Korean payloads.

## 12. Current disposition

```text
S1 no-op serializer core             CLOSED_V336
S2 generic relocation engine         CLOSED_V337
S3 Switch special owners             IMPLEMENTED
special dynamic plans                3
stock special replay                 PASS_BYTE_EXACT
controlled +4 replay                 PASS_3_OF_3
diagnostic-vector regression         PASS_3_OF_3
false EVENT-02 nonowners             PASS_2_OF_2
V334/V335 selective replacement      NOT IMPLEMENTED
product bytes / build / package      NONE
```

## 13. Exact next scope

After a fresh explicit user execution signal:

`ECF00000_SELECTIVE_EVENT_V334_V335_REPLACEMENT_APPLICATION_IMPLEMENTATION_OFFLINE_VALIDATION`

S4 only:

- consume the exact V334 original->KO mapping and V335 semantic code vector;
- apply only admitted Korean payloads while preserving 426 UNRESOLVED and 478 NON_KOREAN rows;
- run V337 generic relocation and V338 special-span repair on the resulting current item layout;
- do not yet implement `FIXED_SURFACE_PARTICLE_V1` code-3 transformation unless its canonical literal transform definition is first recovered and explicitly included in a later stage;
- no build/package/IPS/hardware.
