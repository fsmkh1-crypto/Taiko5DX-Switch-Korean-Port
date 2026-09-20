# ECF00000 SELECTIVE EVENT GENERIC RELOCATION ENGINE IMPLEMENTATION / OFFLINE VALIDATION — V337

Date: 2026-09-20 (KST)

```text
validation_id   V337
track           SWITCH_SELECTIVE_KOREANIZATION
scope_kind      IMPLEMENTATION_AND_OFFLINE_VALIDATION
parent          1efe2a9d820e231d871e5caeba2c91421aad5ccd / V336
stage           S2_GENERIC_RELOCATION_ONLY
product_bytes   UNCHANGED
build/package   NONE
hardware        NOT RUN
```

V337 implements only the ordinary PC-editor relocation cause-family for `02/04/06/07/08/09`. It preserves V336 original edit-partition/grouping authority and freezes branch ownership from original grouped items before any length-changing payload is introduced.

## 1. Actual PC editor source authority

The original user-supplied archive was re-opened and `Form1.vb` was directly extracted for this stage.

```text
archive size       3,379,608
archive sha256     0f0df73e9d79355687e7a95c35b8bacb1fcdf1f83d0a80d5abeb105514bde903
Form1.vb size        296,505
Form1.vb sha256     dc41d778ab11268fc137d0b995bc5cff14d0fcec127e020803c6dc838523e14d
```

The exact source functions used are the six 저장/자동갱신 pairs for:

```text
02 -> 순환_02패턴_단계수저장 / 자동갱신
04 -> 조건분기_04패턴_단계수저장 / 자동갱신
06 -> 조건분기_06패턴_단계수저장 / 자동갱신
07 -> 조건분기_07패턴_단계수저장 / 자동갱신
08 -> 조건분기_08패턴_단계수저장 / 자동갱신
09 -> 조건분기_09패턴_단계수저장 / 자동갱신
```

Source behavior confirmed for all six families:

1. scan original grouped ListBox items;
2. decode the original branch byte distance;
3. starting at the branch item itself, find the exact number of grouped items whose byte counts equal that distance;
4. store that stage count;
5. after text length changes, sum the same number of current grouped items;
6. rewrite the field in family order `02 -> 04 -> 06 -> 07 -> 08 -> 09`;
7. preserve the original modulo-4 intrusion for `06/07/09`.

V337 therefore does not rediscover branch ownership from final Korean bytes.

## 2. Implemented generic engine

Updated module:

`builder/selective_event.py`

Added:

- `BranchRepairPlan`;
- exact PC-editor branch candidate recognition;
- exact original stage-count freezing with the source 2,000-item bound;
- `02/04/06/07/08/09` decode arithmetic;
- `06/07/09` intrusion preservation;
- deterministic repair in the source family order;
- field overflow guards;
- representability guards for division-based encodings;
- original-grouped-item-count/order guard;
- generic-pass exclusion contract for the five already-canonical special original starts.

The five excluded original starts are:

```text
Switch dynamic span:
  0xCBBB0 EVENT 0x04
  0x65F40 EVENT 0x04
  0x7E1B0 BRANCH 0x09

false EVENT-0x02 expression operands:
  0xAC470
  0x980C0
```

S2 does not implement the three dynamic-span recalculations. Exclusion only prevents the generic pass from claiming those special cases.

## 3. Stock full-corpus generic-plan census

Against exact stock `ECF00000.TS5`:

```text
stock size        931,936
stock sha256      bbaaff8dc552da17a49ea2e6ce49a76da662541ee22fdec7dc7933046430bf09

family   source candidates   exact stage plans
02                1,497               179
04                6,784             6,612
06                  111                62
07                  411               410
08                   40                39
09                  280               277
TOTAL                                 7,579
```

Candidates without an exact stage match remain ignored exactly as the editor does; V337 does not invent ownership for them.

Intrusion census among accepted plans:

```text
06: intrusion 0 = 1,  intrusion 2 = 61
07: intrusion 0 = 53, intrusion 2 = 357
09: intrusion 0 = 44, intrusion 1 = 59,
    intrusion 2 = 127, intrusion 3 = 47
```

All five canonical special starts are absent from the accepted generic stock plans under the original editor grouping; the explicit exclusion set remains a safety invariant for later selective layouts.

## 4. Stock no-change relocation replay

All 7,579 accepted plans were recalculated from unchanged grouped-item lengths.

```text
generic plans                  7,579
changed branch headers             0
partition byte mismatches           0
result                     PASS_BYTE_EXACT
```

Thus the generic engine reproduces every source-recognized stock branch field without changing stock bytes.

## 5. Controlled length-change replay

For every accepted stock plan with at least one owned item after the owner, the final owned item was increased by exactly four bytes and the branch field was recalculated.

```text
eligible plans                 7,578
validated                      7,578
failures                           0
result                       PASS
```

The sole stage-count-1 plan is:

```text
original start  0xD228C
family          0x06
stage count     1
original span   4
```

It is not a failure; there is simply no child item inside its frozen stage on which to perform the +4 controlled-growth experiment. Its unchanged replay passes.

Representative real-stock +4 results:

```text
02 @ 0x103C  span 3216 -> 3220  header 02 25 03 00
04 @ 0x0C50  span   20 ->   24  header 04 01 30 00
06 @ 0x34D4  span 2720 -> 2724  intrusion 2  header 06 53 05 00
07 @ 0x34DC  span 1600 -> 1604  intrusion 2  header 07 23 03 00
08 @ 0x0D50  span  900 ->  904  header 08 00 E2 00
09 @ 0x0D54  span   20 ->   24  intrusion 0  header 09 C3 30 00
```

## 6. Unit validation

`tests/test_selective_event.py` retains all V336 tests and adds S2 tests for:

- all six relocation families;
- `06/07/09` intrusion preservation;
- actual PC-editor `04` store guards;
- special-owner generic exclusion;
- rejection of an unrepresentable divided span.

Expected repository unit total after V337:

```text
V336 tests  8
V337 added  4
total      12
```

The S2 algorithm was independently exercised locally before repository mutation; all added controlled tests passed.

## 7. Safety tightening vs editor UI behavior

The VB editor uses integer division when writing `02/06/07/08`. A malformed edited length could therefore be silently truncated by the UI implementation.

The Switch serializer does not copy that failure mode. V337 uses the same source formula but rejects a length that cannot be represented exactly by the corresponding field.

This is a validation guard, not a different ownership or distance formula.

## 8. Scope boundary

V337 closes only the generic relocation cause-family.

Not implemented:

- Switch dynamic-span recalculation at `0xCBBB0 / 0x65F40 / 0x7E1B0`;
- any special rewrite at the two false EVENT-0x02 expression operands;
- V334/V335 12,171 Korean replacements;
- `FIXED_SURFACE_PARTICLE_V1`;
- EVENT reflow;
- TS5 product build/package/IPS;
- hardware execution;
- other EVENT files;
- SNR.

## 9. Rejected / do-not-repeat

Do not:

- recalculate branches from final-Korean fresh grouping;
- convert source stage count into guessed runtime ownership;
- promote candidates without an exact original grouped-byte match;
- silently truncate an unrepresentable divided span;
- let the generic pass claim any of the five canonical special starts;
- treat V337 as proof of the three Switch dynamic-span formulas;
- apply the 12,171 Korean payloads before S3 is closed.

## 10. Current disposition

```text
S1 no-op serializer core             CLOSED_V336
S2 generic relocation engine         IMPLEMENTED
generic source plans                 7,579
stock unchanged relocation replay    PASS_BYTE_EXACT
controlled +4 replay                 PASS_7578_OF_7578
Switch dynamic-span exceptions       NOT IMPLEMENTED
V334/V335 selective replacement      NOT IMPLEMENTED
product bytes / build / package      NONE
```

## 11. Exact next scope

After a fresh explicit user execution signal:

`ECF00000_SELECTIVE_EVENT_SWITCH_SPECIAL_OWNER_IMPLEMENTATION_OFFLINE_VALIDATION`

S3 only:

- implement actual selective-layout recalculation for the two EVENT `0x04` dynamic spans and one BRANCH `0x09` runtime span;
- lock the two false EVENT-`0x02` expression operands as non-owners;
- validate these special cases independently from the generic engine;
- no V334/V335 Korean replacement;
- no build/package/IPS/hardware.
