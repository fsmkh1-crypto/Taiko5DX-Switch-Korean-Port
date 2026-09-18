# TAI5MSG 3,179 Selective Serializer Byte-Exact Offline Replay Closure — V309

Date: 2026-09-18 (KST)

Validation ID: `V309`

Parent implementation commit:

`3481b83b915af98ad00452a2af9b5c55277b43e6` — `feat: implement selective TAI5MSG serializer V308`

## 1. Scope

This validation closes the byte-exact offline replay that remained pending after V308.

It validates the existing V308 implementation only.

No serializer code, candidate/classification membership, translation payload, package, IPS, build, runtime package, or hardware target is modified by this validation.

## 2. Repository / runtime identity

Remote `main` was checked before execution and matched the V308 parent commit exactly.

Clean execution runtime:

`Python 3.13.5`

Canonical source/module and V303/V304 artifacts were transferred from the repository and checked against their Git blob identities before execution.

## 3. Canonical binary inputs

Stock JP TAI5MSG:

```text
size    1,810,889 bytes
sha256  aae037dd5948f79b9fc2e5affcb1e60e08efca39f897123045fe685786be978f
```

PC Korean TAI5MSG:

```text
size    2,134,366 bytes
sha256  e3b4522a1047ff409e099b5ee197d7689279ea7472cb403d305b2507fec96090
```

The PC-KO TAI5MSG was extracted directly from `Taiko5DX_Korean_Patcher.exe.part02`; the larger 170 MB patch ZIP was not used.

The Mapping game-code set was derived from the actual PC patch `dinput8.dll` `T5K121R` resource, preserving the verified Mapping 10,036 table as the source.

## 4. Canonical artifact integrity

Before execution:

- V303 index/shards matched canonical repository identities;
- all eight V303 row shards reconstructed the canonical 3,179-row set;
- V303 aggregate rowset integrity passed;
- V304 two-row correction index/rows matched canonical repository identities;
- builder and test source matched canonical Git blob identities.

No row was synthesized or rewritten for the validation.

## 5. Clean-runtime execution result

The V308 selective serializer executed against the exact canonical stock / PC-KO inputs.

```text
selected rows       3,179
unselected JP rows 11,653
message count      14,832
growth             +0x7780
final size         0x1C1949 / 1,841,481
B32 offset         0x1B4F00
B32 used-end       0xB8D5
B32 declared       0xCA80
B32 physical       0xCA49
B32 omitted        0x37
```

Output SHA-256:

`dfcb928f694117bdd51e69d25daf337c14e30c3a7078da3961dc3a570ffe44f9`

This matches the V306/V307 diagnostic byte-output identity.

The implementation also performs and passes the zero-replacement byte-identical stock rebuild before applying the effective replacements.

## 6. Tests

`tests/test_selective_tai5msg.py`

Result:

```text
Ran 7 tests
OK
```

Status: `PASS_7_OF_7`.

## 7. Resolved environment issue

A direct repository clone/download path was unavailable because the execution container could not resolve external GitHub network/DNS access.

This was an environment transport limitation, not a serializer defect.

The validation therefore used connector-delivered canonical repository bytes with Git blob identity checks. A temporary Drive transfer document used only as a byte-transport bridge was deleted after verification.

## 8. Closure

```text
V308 implementation             VERIFIED
clean-runtime execution          PASS
zero-replacement identity        PASS
effective 3,179 reconstruction   PASS
diagnostic output SHA            PASS
unit/regression tests            PASS 7/7
package / IPS / build            NONE
hardware execution               NOT PERFORMED
```

Final status:

`CLOSED / CLEAN_RUNTIME_VERIFIED / BYTE_EXACT_REPLAY_VERIFIED`

## 9. Next scope boundary

The next executable scope is:

`TAI5MSG_3179_SELECTIVE_PACKAGE_INTEGRATION_DESIGN`

That scope is design-only unless separately authorized later.

It must not generate a package, IPS/build/runtime output, gameplay binary write, or hardware execution.
