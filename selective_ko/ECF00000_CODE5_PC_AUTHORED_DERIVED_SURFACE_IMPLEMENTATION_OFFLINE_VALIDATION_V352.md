# ECF00000 code-5 PC-authored derived-surface implementation / offline validation — V352

Date: 2026-09-20 (KST)

```text
validation_id   V352
track           SWITCH_SELECTIVE_KOREANIZATION
scope_kind      IMPLEMENTATION_AND_OFFLINE_VALIDATION
parent          e31bed7a5d6a406a6e964c015c256a7d88218134 / V351
product bytes   DIAGNOSTIC ONLY / NOT PACKAGED
build/package   NONE
IPS             NONE
hardware        NOT RUN
```

## 1. Scope

V352 implements only the exact V351 61-row authority:

```text
COPULA_DERIVED_ONLY             59
MIXED_DIRECT_AND_DERIVED_RISK    2
----------------------------------
total                            61

derived occurrences             62
mixed direct edits                3
```

The three V346 `NON_PARTICLE_SUFFIX_ADJACENCY` rows remain outside this scope.

## 2. Implementation

New module:

`builder/selective_event_derived_surface.py`

New tests:

`tests/test_selective_event_derived_surface.py`

Implementation rules:

```text
pure 59
  exact V334-bound raw PC-KO command overlay
  preserve PC-authored derived surface verbatim

mixed 2
  exact raw PC-KO command overlay
  preserve derived surface verbatim
  apply only the exact V351 direct-particle edits
```

Mixed direct edits:

```text
row 12476   \%00    이 -> 가
row 13029   \#07F0  을 -> 를
row 13029   \E079   을 -> 를
```

No pronunciation inference, escape-identity morphology selection, or global allomorph rewrite is introduced.

## 3. Exact V334 binding provenance

V352 materializes:

`selective_ko/artifacts/ecf00000_v352_pc_authored_derived_surface_implementation_v1/BINDINGS_V334_HASHED.jsonl`

```text
rows                       61
EDITOR_TARGET_ORDINAL      58
EDITOR_TARGET_ALIGNMENT     3
REPLACE_FROM_PC_KO         61
```

The three alignment-mapped rows are:

```text
row 8389   partition 388   original 0x9784C
row 8403   partition 388   original 0x97C80
row 8406   partition 388   original 0x97D74
```

This is expected V334 provenance, not a mapping defect. The first local implementation draft incorrectly assumed all 61 rows used ordinal mapping; that assumption was rejected before product output and replaced with an exact allowed-method/count guard.

Bindings SHA-256:

`95f2b98120ddf20f287321393a9d2a52b6f7704d37786df0ef228ae50a47d15f`

Canonical V334 `ROWS.jsonl` source SHA-256 remains:

`aef17d206559ec548a5fb3c2414d8a1f17832f7e4c2df03b8468240926c11b65`

## 4. Payload result

Exact command totals:

```text
original bytes                3,132
raw PC-KO bytes               4,104
transformed bytes             4,104
payload growth                 +972
```

The three mixed direct-particle edits are all 2-byte -> 2-byte and therefore add no further length delta.

V350 baseline:

```text
size      1,108,384
sha256    bedd0cd3b367e3caed4f7d06adc6b3ecfb607d0152d8329f830eb6de98411ff2
```

V352 diagnostic:

```text
size      1,109,356
delta     +972
sha256    e61569508ffc9995f78df51f01b42be5402b79d5e26a8c8f3e71c0448d8eaaeb
```

Deterministic replay:

`PASS_BYTE_IDENTICAL`

## 5. Mutation accounting

Against canonical V350 diagnostic:

```text
changed grouped items                 142
target payload items                   61
target payloads byte-exact after repair 61
targets also structural owners          0
non-target changes                     81
generic relocation-owner changes       81
special-span owner changes              0
unexpected non-target changes           0
```

Therefore all non-target mutations are owned by the existing V337 generic relocation layer.

## 6. Inherited structural gates

```text
generic relocation plans       7,579 / PASS
special spans                      3 / PASS
false EVENT-02 nonowners           2 / PASS
5A mapping rows                1,088
5A translated                  1,074
5A name-only                      14
5A violations                      0
baseline walker errors             0
```

New module unit tests:

`PASS 6 / 6`

Local code-5 regression after staging the canonical V348 fixtures required by the older direct-particle tests:

`PASS 17 / 17`

The first local discovery run had two fixture-not-found errors because the temporary workspace did not contain the V348 ledger files. This was a test-workspace setup issue, not a code or product failure.

## 7. State-aware residual gate and V344 alias disappearance

V350 observed:

```text
candidate observations       3
unique logical residuals     2
inherited stock              1
source-proven V344 alias     1
novel                        0
```

V352 observes:

```text
candidate observations       1
unique logical residuals     1
inherited stock              1
source-proven alias          0
novel                        0
blocking                     false
```

The remaining residual is the already-canonical V340 stock-preexisting logical residual:

```text
partition       593
original offset 0xBDD78
opcode          0x0E
decoded length  0x7F5408
```

The V344 source-proven alias at original `0xC3740` disappears from conservative state-aware reachability in V352. This is not caused by mutation of partition 604.

Partition 604 is byte-identical between V350 and V352:

```text
size             1,920 / 1,920
sha256 V350      1f3708a138b87704caa95482344c294ae216c239118efeec19c49a589dd5dc9b
sha256 V352      1f3708a138b87704caa95482344c294ae216c239118efeec19c49a589dd5dc9b
0xC373C parent   0bdc1700 / unchanged
0xC3740 alias    0e009d06 / unchanged
```

Isolation proves the observation loss comes from valid V351 payload growth in partition 593:

```text
V351 none                         3 observations
all V351 except partition 593     3 observations
partition 593 rows only           1 observation

row 11074 only                    3 observations
row 11082 only                    1 observation
row 11090 only                    1 observation
```

Partition-593 V351 rows are `11074`, `11082`, and `11090`, each +28 bytes. Rows 11082 or 11090 independently change the conservative MAY-walker path enough that the source-alias observation is no longer reached.

Binding conclusion:

```text
alias bytes mutated                         NO
new state-aware residual                    NO
canonical inherited stock residual          YES
source-proven alias still observed          NO
alias disappearance                         NON_BLOCKING
```

The initial V352 diagnostic harness assumption `candidate observations == 3` is rejected. Later valid payload growth must use the canonical V340/V344 provenance-based residual gate, not a fixed observation count.

## 8. 확정된 사실

- exact V351 61 rows are implemented;
- all 61 bind to canonical V334 original/PC-KO command hashes;
- V334 mapping methods are 58 ordinal + 3 alignment;
- pure 59 use exact raw PC-KO commands;
- mixed 2 preserve authored derived morphology and apply exactly three direct-particle normalizations;
- output growth is exactly +972 bytes vs V350;
- all 61 target payloads survive structural repair byte-exact;
- all 81 non-target changes are generic relocation owners;
- no unexpected non-target mutation exists;
- inherited 5A / special-owner / false-02 / baseline walker gates pass;
- state-aware novel residual count is zero;
- deterministic rebuild is byte-identical.

## 9. 유력한 가설

None remains inside the V351/V352 derived-surface cause family.

The state-aware alias disappearance is closed as a conservative diagnostic reachability change induced by legal partition-593 payload growth; it is not treated as a gameplay-semantic claim.

## 10. 미확정 사항

V352 does not address the three V346 `NON_PARTICLE_SUFFIX_ADJACENCY` rows.

V352 also does not establish hardware behavior because no package/IPS/hardware run is in scope.

## 11. 기각된 가설 / do-not-repeat

Reject:

- require every later diagnostic to preserve V344's exact three raw state observations;
- treat disappearance of the source-proven alias as corruption;
- patch partition 604 merely to restore a diagnostic alias observation;
- assume all V351 rows use `EDITOR_TARGET_ORDINAL` mapping;
- infer pronunciation or rewrite PC-authored derived allomorphs;
- raw-copy the two mixed rows without their three exact direct-particle normalizations;
- widen this implementation to the suffix-three family;
- build/package/IPS or claim hardware validation from V352.

## 12. Current disposition / next scope

```text
DIRECT_PARTICLE_ONLY                  350 IMPLEMENTED / OFFLINE PASS
LEXICAL_FALSE_POSITIVE_GAMUN           12 IMPLEMENTED / OFFLINE PASS
COPULA_DERIVED_ONLY                    59 IMPLEMENTED / OFFLINE PASS
MIXED_DIRECT_AND_DERIVED_RISK           2 IMPLEMENTED / OFFLINE PASS
--------------------------------------------------------------
code-5 admitted / implemented         423

NON_PARTICLE_SUFFIX_ADJACENCY           3 DEFER
```

Effective V334 product overlay remains:

```text
INCLUDE_KO             12,594
DEFER                        3
NON_KOREAN_TARGET          478
TOTAL                    13,075
```

Exact next scope after a fresh explicit user signal:

`ECF00000_CODE5_NON_PARTICLE_SUFFIX_ADJACENCY_RUNTIME_RESPONSIBILITY_READ_ONLY`

READ ONLY only. Investigate the exact three remaining V346 suffix-adjacency rows as one cause family against actual PC-patch bytes and Switch runtime/data ownership. Do not implement them, build/package/IPS, or run hardware without another fresh authorization.
## 13. Drive archive

Git remains canonical authority. Drive is an archive mirror.

```text
folder       10mulhDcpOT5c0n9MyWWazorHhkwkn47V
diagnostic   1mIkFwodiotxI6gV0iGGeuW33vC5vEq46
```

The same folder contains the final validation JSON, implementation module, tests, exact V334-hashed bindings, authority document, and INDEX by filename.

