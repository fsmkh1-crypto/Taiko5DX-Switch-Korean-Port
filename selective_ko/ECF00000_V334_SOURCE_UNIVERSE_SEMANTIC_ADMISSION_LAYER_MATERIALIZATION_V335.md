# ECF00000 V334 SOURCE-UNIVERSE SEMANTIC ADMISSION LAYER MATERIALIZATION — V335

Date: 2026-09-20 (KST)

```text
validation_id   V335
track           SWITCH_SELECTIVE_KOREANIZATION
scope_kind      SEMANTIC_ADMISSION_ARTIFACT_MATERIALIZATION
parent          3b627960c0960a8badb139d39420320958dcc00d / V334
product_bytes   UNCHANGED
serializer      NOT IMPLEMENTED
build/package   NONE
repository      DOCUMENTATION_AND_PROVENANCE_ARTIFACTS_ONLY
```

V335 binds the inherited V325/V326 semantic-admission rules to the exact V334 13,075-row source universe. It closes the last count-only semantic-membership gap before EVENT serializer design.

## 1. Provenance gate

The classifier was first replayed against the surviving 2,858-row V329/V330-era diagnostic population. Korean-bearing state, escape/control forms, explicit dual-particle detection/counts, particle detector and V326 disposition all matched.

```text
rows checked    2,858
exact matches   2,858
mismatches          0
status           PASS_EXACT_2858_OF_2858
```

Therefore this is a replay of the V325/V326 rule family, not a new semantic policy.

## 2. Exact V334-bound membership

```text
INCLUDE_KO_NO_ESCAPE                 8,155
INCLUDE_KO_CHOICE                      357
INCLUDE_KO_FIXED_SURFACE_PARTICLE    1,226
INCLUDE_KO_RUNTIME_EXPANSION         2,433
                                      ------
INCLUDE_KO                          12,171

UNRESOLVED_PARTICLE_RISK               426
NON_KOREAN_TARGET                      478
                                      ------
TOTAL                               13,075
```

Exact rowset SHA-256:

```text
INCLUDE_KO
714938521e9db784725b1de2bf2018114090a0aabc5759a29975caba092d1d10

UNRESOLVED
5e0fa8d144974082097974b33a119893e553e63ada1a28196c842fd7e3beaa90

NON_KOREAN_TARGET
ff5839e8c45aa07465dfcc7bbe497bfbc144a399dc4dbc1a0eaa3e703241e5f0
```

## 3. Rule contract

```text
korean_bearing=false
  -> NON_KOREAN_TARGET

Korean + opcode 0x15
  -> INCLUDE_KO_CHOICE

Korean message + no parsed runtime escape
  -> INCLUDE_KO_NO_ESCAPE

Korean escaped message + exact authorized dual-particle literal
  -> INCLUDE_KO_FIXED_SURFACE_PARTICLE

particle detector true + no exact dual-particle literal
  -> UNRESOLVED_PARTICLE_RISK

remaining Korean escaped message
  -> INCLUDE_KO_RUNTIME_EXPANSION
```

Do not treat the particle detector as proof of a grammatical particle.

## 4. Escape/particle population

```text
escape/control rows                    4,155
particle detector rows                   443
explicit dual-particle rows            1,226
detector + explicit-dual overlap          17
detector-only unresolved                 426
```

Explicit fixed-surface occurrences:

```text
은(는)   521
이(가)   395
을(를)   358
과(와)    41
와(과)    51
(으)로    23
----------------
total   1,389 occurrences / 1,226 rows
```

## 5. Exact Git membership encoding

V334 already canonically fixes the 13,075-row order. V335 therefore stores one semantic detail code per V334 row rather than duplicating offsets/opcodes.

```text
code 0  NON_KOREAN_TARGET
code 1  INCLUDE_KO_NO_ESCAPE
code 2  INCLUDE_KO_CHOICE
code 3  INCLUDE_KO_FIXED_SURFACE_PARTICLE
code 4  INCLUDE_KO_RUNTIME_EXPANSION
code 5  UNRESOLVED_PARTICLE_RISK
```

Raw code vector:

```text
records       13,075
bytes         13,075
sha256        a698b788787c0006e98b62029e9145f56f33270e363ca31c389ede0442001b12
```

Git stores the zlib-compressed vector:

```text
file          SEMANTIC_DETAIL_CODES_BY_V334_ROW.bin.zlib
bytes         2,680
sha256        dea9a6b76619f03ec698b8d60c700680a55c422a6ee0ae3ffe794cace27213dd
```

Joining this code vector to the canonical V334 row order reconstructs the three product rowsets byte-for-byte and reproduces all three SHA-256 values in section 2.

## 6. Non-Korean population

```text
NON_KOREAN_TARGET                   478
PC-original == PC-KO               476
PC-original != PC-KO                 2
```

Two changed non-Korean rows:

```text
row 1576  KO 0x2D600  original 0x248A4  opcode 0x11  escape \%03
row 5712  KO 0x89274  original 0x6DAC4  opcode 0x11  escape \#0CB8
```

They remain outside INCLUDE_KO. Porting them is a separate non-blocking policy queue.

## 7. Drive artifact and clean replay

Complete verbose artifact:

```text
Google Drive/GPT/태합입지전/ECF00000_V335_SEMANTIC_ADMISSION_LAYER/
folder id  1eXSc0ml_bO89XIpRdG3BOSnh8GaRti-s
file id    13ffnjrOgfDv3MtveBg-ktOmd_waJMWHw
file       ECF00000_V335_SEMANTIC_ADMISSION_CANONICAL.zip
size       360,776
sha256     9e1f7cb880235323aadd3aa2e47d94e1775d25b2375201e60ca7eafd9a097a7e
roundtrip  PASS_BYTE_IDENTICAL
```

Verbose semantic JSONL SHA-256:

`d449b9b30938ec46b3ef40a5fb69f695efdb82cbc05aa0f8f070134e897d235e`

Clean replay:

```text
legacy regression       PASS_EXACT_2858_OF_2858
expected aggregate      PASS
INCLUDE_KO              12,171
UNRESOLVED                 426
NON_KOREAN                 478
result                    PASS
```

## 8. Rejected / do-not-repeat

Rejected:

- all escapes are unresolved;
- all 443 detector hits are true particle risks;
- the 17 detector/explicit-dual overlaps are unresolved;
- historical V324 4,444 membership is semantic authority;
- semantic classification without V334 exact row binding;
- aggregate 12,171/426 counts without exact membership;
- silently admitting the two non-Korean changed rows;
- re-deriving V325/V326 rules from guesses in a new chat/model.

V326's 4,123/115 counts remain historical for its old 4,238-row population. V335 applies the same proven rule family to the exact V334 source universe.

## 9. Current disposition

```text
V334 structural source universe            CLOSED
V334 original->KO binding                  CLOSED
V335 exact semantic admission membership   CLOSED
V335 clean replay                          PASS
V335 Drive roundtrip                       PASS_BYTE_IDENTICAL
EVENT serializer design                    NEXT
EVENT serializer implementation            NOT AUTHORIZED BY V335
product bytes / build / package / IPS      NONE
```

## 10. Exact next scope

After a fresh explicit user execution signal:

`ECF00000_SELECTIVE_EVENT_SERIALIZER_DESIGN_READ_ONLY`

Authorized next: design only.

- reconstruction ownership from PC-original edit partitions;
- INCLUDE_KO replacement vs UNRESOLVED/NON_KOREAN preservation;
- FIXED_SURFACE_PARTICLE_V1 transformation timing;
- Switch dynamic-span recalculation at `0xFDC04 / 0x7F7A8 / 0x9DAE4`;
- preserve `0xD7008 / 0xBDC58` as EVENT 0x0A expression data;
- offset-table rebuild and deterministic validation gates.

Not authorized:

- serializer implementation;
- payload mutation;
- build/package/IPS;
- resolving 426 semantic rows inside the design scope;
- porting the two non-Korean changes without separate policy;
- unrelated EVENT files or SNR.
