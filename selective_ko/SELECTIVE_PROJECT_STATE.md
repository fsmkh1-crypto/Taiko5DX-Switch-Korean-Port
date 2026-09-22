# SELECTIVE PROJECT STATE

Date: 2026-09-23 (KST)
Status: V371 ROLE-AWARE FIELD-POLICY ADAPTER IMPLEMENTED / BOUNDED VALIDATION PASS / PRODUCT CANDIDATE NOT EMITTED
Track: `SWITCH_SELECTIVE_KOREANIZATION`

## 1. Resume authority

Repository: `fsmkh1-crypto/Taiko5DX-Switch-Korean-Port`  
Branch: `main`  
Target: Nintendo Switch title `0100346017304000`, game v1.1.3.

Repository-level authority: `../PROJECT_STATE.md`.

Current checkpoint:
`EVENT_169_ROLE_AWARE_FIELD_POLICY_ADAPTER_IMPLEMENTATION_V371.md`

Current artifact index:
`artifacts/event_169_role_aware_field_policy_adapter_v1/INDEX.json`

Current validation index:
`VALIDATION_INDEX.json`

Current product authority remains:
`EVENT_169_APPLICABILITY_AND_OVERLAP_CANONICALIZATION_V369.md`

## 2. Frozen product and implemented adapter state

```text
source-owner universe                    66,987
INCLUDE_KO recipe coverage               52,491
NON_KOREAN_TARGET                        14,496
UNRESOLVED                                    0

role-aware structural fields             24,305
  generic identity                       12,522
  generic re-encode                      11,745
  payload preserve                           19
  secondary-header preserve                   1
  expression-operand preserve                 1
  Switch special                              3
  typed EVENT04                               6
  dual-view subordinate slots                 8

field writer rows                        24,284
no-field-writer rows                         21
final write-responsibility units             80
```

Implementation commit: `4c5d2c4e010bf9c760337d39c0a64b6a82314918`.

## 3. Implemented rules

- Generic fields consume retained source-plan owner/stage-count authority.
- Final output bytes are not reparsed to invent structural fields.
- `CONTACT:<owner>` and `CONTACT:O:<owner>` are normalized to the same retained owner key.
- No-writer policies preserve exact bytes through parent mapping and protected views.
- H01 remains fail-closed except the exact `ECF00000:E29F4` parent/slot contract.
- Dual-view ordering is parent payload, subordinate field slot, then final partition table.
- Request manifests cannot override the canonical policy with ad hoc field rules.

## 4. Bounded validation

```text
IM01                     150 / 150 PASS
IM02                     363 / 363 PASS
IM03                     196 / 196 PASS
H01                        7 /   7 PASS
role-aware adapter        11 /  11 PASS
canonical compact          4 /   4 PASS
TOTAL                     731 / 731 PASS

full policy source oracle 24,305 / 24,305 PASS
full policy output oracle 24,305 / 24,305 PASS
candidate EVENT output    0
```

These are implementation/regression results only. They are not 169-file output acceptance.

## 5. Rejected paths

- no per-row exception treatment for 11,764 geometry changes;
- no assumption that 700 contact fields require runtime hooks;
- no revival of the rejected `EC500000:1DC` hard-NUL-conflict hypothesis;
- no final-byte opcode scan as field authority;
- no request-manifest field-rule override;
- no independent writer for subordinate dual-view slots;
- no runtime hook unless static full replay later proves a true irreducible conflict.

## 6. Remaining product work

- materialize the actual 169-file requests;
- connect all 52,491 recipe inputs and 24,305 field policies;
- resolve 60 source-identity authorities;
- execute and validate 80 atomic transaction units;
- verify all 66,987 owners and final writer responsibilities;
- verify TAI5MSG 5 roots / 19 references;
- VAL01, IPS/package, Eden, and Switch validation.

## 7. Exact next scope

A fresh explicit user execution signal may authorize:

`V371_ACTIVE_REQUEST_CONNECTION_AND_169_FILE_CANDIDATE_OFFLINE_VALIDATION`

That scope must use the current adapter and frozen V366-V369 authorities. It must not begin another role/rule census.
