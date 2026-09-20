# ECF00000 percent-macro ↔ TAI5MSG B0 46-root replacement implementation / offline validation — V357

Date: 2026-09-21 (KST)

```text
validation_id   V357
track           SWITCH_SELECTIVE_KOREANIZATION
parent          7c7bf970809e2204c67e83317c51bc459230ad7b / V356
scope_kind      IMPLEMENTATION_OFFLINE_VALIDATION
implementation  IMPLEMENTED
package/IPS     NONE
hardware        NOT RUN
```

## 1. Scope

V357 implements exactly the V356-admitted 46 B0 percent-macro program roots. It does not change
V303 membership, EVENT payloads, Mapping/font assets, ExeFS IPS, package contents, or hardware state.

The root family remains separate from the V303 prose validator. Exact source/target message identity
is the binding guard.

## 2. Implementation

New module:

`builder/tai5msg_percent_macro_roots.py`

The module loads the canonical V356 INDEX / ADMISSION / ADMISSION_ROWS authorities, validates the
exact 46-row transport and census, then resolves each locator against canonical stock and PC-KO
TAI5MSG source/target SHA-256 guards.

`builder/selective_tai5msg.py` now:

- keeps V303 3,179 prose rows unchanged;
- loads 46 disjoint B0 program roots independently;
- rejects overlap with V303/V304/V315/V320 owners;
- applies exact same-locator PC-KO payloads only after existing V303 prose/code validation;
- validates B0 `used_end=0xE9FC`, `declared=0xEA00`;
- validates 3,179 prose + 46 program roots + 11,607 untouched rows after reparse;
- promotes the deterministic diagnostic identity to the V357 output below.

## 3. Exact output

Independent byte-exact replay was performed twice from the canonical inputs. A second reconstruction
using the stock serializer block-size policy and the exact V320 target-message matrix produced the
same byte stream as direct V320-baseline overlay replay.

```text
output size                    1,840,329 / 0x1C14C9
output sha256                  ad91776d47c3170573bed063dd6677716833e3a138be27474373ef5d2782e794
growth vs stock                  29,440 / 0x7300
growth vs V320                      576 / 0x0240

B0 used_end                      59,900 / 0xE9FC
B0 declared                      59,904 / 0xEA00
B0 filler                             4

B32 offset                    1,788,544 / 0x1B4A80
B32 used_end                     47,317 / 0xB8D5
B32 declared                     51,840 / 0xCA80
B32 physical                     51,785 / 0xCA49
```

Growth blocks under the stock serializer policy:

```text
B0  +0x0240
B17 +0x0340
B19 +0x0A80
B20 +0x06C0
B21 +0x01C0
B22 +0x4340
B23 +0x0FC0
B24 +0x0780
```

This reproduces the V356 capacity projection exactly.

## 4. Regression result

```text
V356 exact roots                              46 / 46 target match
non-root messages vs V320                14,786 / 14,786 byte-identical
raw B1..B32 blocks vs V320                    32 / 32 byte-identical
stock-base vs V320-base serializer replay     PASS_BYTE_IDENTICAL
deterministic repeated output                 PASS_BYTE_IDENTICAL
dedicated root manifest/guard tests           PASS_2_OF_2
new root module py_compile                    PASS
```

The existing repository-wide TAI5MSG unit module was not rerun in this container because the complete
Git repository artifact tree is not locally materialized and direct GitHub network/DNS is unavailable.
This is recorded as an environment execution limitation, not silently promoted to PASS. The V320
baseline itself remains previously VERIFIED/CLOSED; V357 independently proves the exact new delta and
the stock-policy final byte stream.

## 5. 확정된 사실

1. The 46-root family is implemented as an independent B0 program overlay, not as V303 prose membership.
2. All 46 targets are exact same-locator PC-KO payloads guarded by V356 source/target hashes.
3. V356's `0xEA00 / 0x7300 / 0x1C14C9 / B32 0x1B4A80` projection is reproduced exactly.
4. All 14,786 non-root messages remain byte-identical to V320.
5. B1..B32 raw block bytes remain byte-identical; only their absolute offsets move by B0 growth.
6. No package, IPS or hardware operation is part of V357.

## 6. 유력한 가설

A diagnostic package containing the V357 TAI5MSG should replace the Japanese percent-macro output
surfaces for the V354 2,440 admitted occurrences while preserving the already verified V320 behavior.

This remains a runtime hypothesis until Eden/hardware execution.

## 7. 미확정 사항

- Eden visual/runtime result for representative percent-macro callers;
- physical Switch / Atmosphere behavior;
- a rerun of the complete historical TAI5MSG unit suite in a fully materialized repository runtime.

## 8. 기각된 가설 / do-not-repeat

- add the 46 roots to V303 prose membership: REJECTED;
- run the 46 roots through `_validate_selected_message`: REJECTED;
- patch only %15/%21/%2A: REJECTED;
- globally replace B0: REJECTED;
- treat raw +578 payload delta as +578 file growth: REJECTED.

## 9. 관련 영향 범위

Changed:

- `builder/tai5msg_percent_macro_roots.py`;
- `builder/selective_tai5msg.py`;
- TAI5MSG B0 exact 46-root payload family;
- serializer constants/postconditions/tests.

Unchanged:

- V303 3,179 membership;
- V304/V315/V320 correction membership;
- Mapping/font assets;
- EVENT V349/V350/V352 outputs;
- ExeFS IPS;
- package/ZIP;
- runtime/hardware.

## 10. 수정 제안 / exact next scope

`ECF00000_PERCENT_MACRO_TAI5MSG_V357_EDEN_DIAGNOSTIC_PACKAGE_MATERIALIZATION`

Under a fresh explicit user execution signal, materialize only the V357 TAI5MSG into the existing
diagnostic package route, verify deterministic package rebuild / roundtrip, then stop before Eden or
physical Switch runtime execution.
