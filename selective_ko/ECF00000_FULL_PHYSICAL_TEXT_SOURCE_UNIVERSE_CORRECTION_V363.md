# ECF00000 FULL PHYSICAL TEXT SOURCE-UNIVERSE CORRECTION / STABLE LEDGER MATERIALIZATION — V363

Date: 2026-09-21 (KST)

~~~text
validation_id   V363
track           SWITCH_SELECTIVE_KOREANIZATION
scope_kind      SOURCE_UNIVERSE_COMPLETENESS_CORRECTION_AND_PROVENANCE_MATERIALIZATION
parent          0416e80f3937864f30e944b28f10a6ac3e5991f2 / V362
product_bytes   UNCHANGED
serializer      UNCHANGED
build/package   NONE
repository      DOCUMENTATION_AND_PROVENANCE_ARTIFACTS_ONLY
~~~

V363 corrects one bounded cause family exposed by the V361 Eden runtime screenshot: V334's deterministic MAY-reachable membership is a valid 13,075-row subset, but it is not a complete EVENT text-owner universe.

## 1. Trigger and exact runtime counterexample

The first captured Japanese ordinary-dialogue lines are owned by `ECF00000.TS5`, not by another EVENT file.

~~~text
PC/Switch original offset   0x4748
PC-KO offset                0x4ED4
opcode                      0x12
V334 membership             ABSENT
V361 diagnostic payload     ORIGINAL COMMAND PRESENT
V363 stable row id          13223
V363 semantic detail        INCLUDE_KO_FIXED_SURFACE_PARTICLE
V363 product disposition    INCLUDE_KO
~~~

Original source contains runtime placeholders rather than the final rendered names, which is why literal search for the complete screenshot text failed. V362's other-EVENT-owner inference is superseded for this exact dialogue.

## 2. Correct structural authority

V333/V334 used runtime-MAY reachability as the localization membership gate. The screen counterexample proves that model is not complete enough for source-universe admission.

~~~text
source membership authority
  = PC-original editor physical text ownership for opcodes 11/12/13/15

counterpart authority
  = exact PC-original -> PC-KO binding

semantic authority
  = inherited V325/V326/V335 classifier family

NOT source membership authority
  = V334 runtime-MAY reachability
  = fresh parse of final PC-KO bytes
~~~

Existing V334 rows remain valid. Their mapping and V335 semantic classification replay exactly and retain stable row IDs.

## 3. Exact full physical source universe

Canonical inputs:

~~~text
PC/Switch original ECF00000.TS5
size     931,936
sha256   bbaaff8dc552da17a49ea2e6ce49a76da662541ee22fdec7dc7933046430bf09

PC-KO ECF00000.TS5
size     1,156,480
sha256   0899bf81789acfbd243d43be209a8a3960933fa090960ac8c753c63f95f07bbe
~~~

Result:

~~~text
PC-original editor text owners       15,951
PC-KO fresh-reparse target-like      15,945
exact original->KO bindings          15,946
binding DEFER                             5
KO-only fresh-reparse unbound             1
~~~

The authoritative source-universe size is 15,951, not the KO fresh-reparse count 15,945.

## 4. Stable-row compatibility

~~~text
legacy V334 rows preserved        13,075 / 13,075
legacy row IDs preserved          1..13,075
mapping/semantic mismatches       0
new rows appended                 2,876
new row IDs                       13,076..15,951
clean replay                      PASS_EXACT_13075_OF_13075
~~~

This preserves all downstream ledgers that bind to legacy V334 row IDs.

## 5. Newly recovered 2,876 rows

~~~text
new rows                          2,876
exact PC-KO binding               2,871
binding DEFER                         5

among 2,871 mapped:
REPLACE_FROM_PC_KO                1,678
PRESERVE_ORIGINAL                 1,193
Korean-bearing                    1,678
~~~

Inherited V335 semantic rules classify the mapped additions as:

~~~text
INCLUDE_KO_NO_ESCAPE                982
INCLUDE_KO_RUNTIME_EXPANSION        375
INCLUDE_KO_FIXED_SURFACE_PARTICLE   232
INCLUDE_KO_CHOICE                    45
UNRESOLVED_PARTICLE_RISK             44
NON_KOREAN_TARGET                 1,193
~~~

Product disposition of the additions:

~~~text
INCLUDE_KO        1,634
UNRESOLVED           44
NON_KOREAN_TARGET 1,193
BINDING_DEFER         5
~~~

## 6. Full V363 ECF admission state

~~~text
INCLUDE_KO          13,805
UNRESOLVED             470
NON_KOREAN_TARGET     1,671
BINDING_DEFER             5
TOTAL                15,951
~~~

These are census/admission results only. They do not authorize payload mutation of newly added rows before downstream V339-V360 policy/dependency impact is audited.

## 7. Structural-drift DEFER set

Five PC-original owners have Korean text present in the PC-KO raw region, but final-Korean editor grouping does not expose a safe ordinary target boundary:

~~~text
0x7F428
0x96E40
0x96E6C
0x96E7C
0xB0E44
~~~

They remain explicit `BINDING_DEFER`; do not guess a raw-copy owner. The observed cause family is branch/control bytes interacting with translated text under final-Korean fresh reparse.

One KO fresh-reparse target-like item has no original editor-owner binding:

~~~text
KO 0x8E010
~~~

It is recorded only as `KO_ONLY_FRESH_REPARSE_UNBOUND_TARGET_LIKE` and is not promoted.

## 8. Mapping provenance

~~~text
EDITOR_TARGET_ORDINAL                    15,106
EDITOR_TARGET_ALIGNMENT                     838
V333_5A_FRESH_REPARSE_DRIFT_BINDING            2
PC_KO_BINDING_STRUCTURAL_DRIFT_UNRESOLVED       5
~~~

Verified V333 drift bindings remain:

~~~text
KO 0x16828 -> original 0x12C40
KO 0x168E0 -> original 0x12C90
~~~

## 9. Canonical artifact

Large verbose artifacts are stored in Google Drive:

~~~text
folder id   1Ab2FIt97Mf_S45Ny0m1NjHkH8_8vXtym
file        ECF00000_V363_FULL_PHYSICAL_TEXT_SOURCE_UNIVERSE_CANONICAL.zip
file id     1afc-b8Zh39RQq2XGO7DAVNXlq1ir70_0
size        1,984,864 bytes
sha256      2ac7c048150887e7b47196f8d784c813d2a33dc8c6e4d5582e19d6f95b1952dc
roundtrip   PASS_BYTE_IDENTICAL
~~~

Key rowset identities:

~~~text
FULL_ROWS.jsonl
d3092d1a3d621b746cd80321a52f047e38e7c1033439010dc861c1342d945aa4

ADDED_ROWS.jsonl
7e4f4533add1966aa5a29536f97279b69b976b0dca8726820647733d66249fa4

FULL_ROWSET_ORIGINAL_OFFSET_OPCODE.bin
934fd1c95c52fb72f3af721e5c2f65d811a8259f438498157bf8fdc94af08e87

MAPPED_PAIR_ROWSET.bin
1d55d9124cdf02b09f7290709c886ff543202e28d4e775c4a5a7f928d9e89180

STABLE_LEDGER_COMPACT.bin
7588a165b179884c23e175e4059a4a8ebf5ad11f8c9159decff88f774fea4a0e
~~~

Two independent output directories reproduced all 11 archived files byte-for-byte before Drive upload.

## 10. Supersession boundary

Superseded:

- V333/V334 claim that 13,075 is a complete conservative localization source universe.
- V362 other-EVENT-owner inference for the exact first captured dialogue at original 0x4748.

Still valid:

- exact correctness and IDs of the existing V334 13,075 rows;
- their original->KO bindings and V335 classifications;
- V336-V360 results for their exact previously authorized memberships;
- Mapping 10,036, font/glyph, TAI5MSG, generic relocation arithmetic, and closed 5A/1E/3C facts unless separately contradicted.

Do not repeat:

- use runtime-MAY reachability as EVENT text admission-completeness authority;
- use final PC-KO fresh grouping as owner authority;
- renumber legacy 13,075 rows;
- bulk-replace all 15,951 physical owners;
- guess the five structural-drift bindings;
- promote KO-only 0x8E010 without original ownership.

## 11. Current disposition

~~~text
V363 full physical source universe       MATERIALIZED / CLEAN REPLAY PASS
V334 legacy compatibility                PASS_EXACT_13075_OF_13075
new exact mapped rows                    2,871
new binding-defer rows                       5
product bytes                            UNCHANGED
serializer/runtime code                  UNCHANGED
build/package/IPS                        NONE
~~~

## 12. Exact next scope

After a fresh explicit user execution signal:

`ECF00000_V363_ADDED_2876_DOWNSTREAM_POLICY_AND_CROSS_CARRIER_IMPACT_AUDIT_READ_ONLY`

READ ONLY only. Audit the exact 2,876 appended rows, including the five binding-DEFER rows, against post-V335 EVENT policy/dependency layers: 5A/1E/3C ownership interactions, fixed/direct/derived particle handling, `%xx` -> TAI5MSG cross-carrier roots, generic/special relocation ownership, and row-ID-bound V344-V360 applicability. Preserve all legacy V334 row IDs and closed results. Do not implement new rows, mutate EVENT/TAI5MSG, build/package/IPS, or run hardware.
