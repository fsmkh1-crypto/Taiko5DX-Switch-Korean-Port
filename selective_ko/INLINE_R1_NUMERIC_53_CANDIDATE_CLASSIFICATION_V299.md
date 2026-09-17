# INLINE R1 NUMERIC 53 CANDIDATE / CLASSIFICATION — V299

Date: 2026-09-18 (KST)
Status: CANONICAL CANDIDATE/CLASSIFICATION MATERIALIZATION / R1 VARIABLE_INSERT 53 / NO BUILD
Track: `SWITCH_SELECTIVE_KOREANIZATION`
Validation ID: `V299`
Parent: `f9bf016e647c62644a96d088d0dd10c904cbb3a5` / V298

## 1. Scope

This validation materializes the ordinary-inline R1 numeric UI family only.

It does not implement a builder, modify Switch game bytes, create IPS output, or claim runtime/layout/hardware PASS.

Canonical row artifact:

`selective_ko/artifacts/inline_r1_numeric_53_candidate_classification_v1/INDEX.json`

## 2. Census correction

The prior read-only intermediate census undercounted three independent physical objects while collapsing multi-match/source-equivalent groups.

Superseded intermediate values:

```text
numeric objects                         50
%d occurrences                         57
remaining ordinary inline R1 objects   99
inline R1 source-role objects          138
```

Canonical V299 values:

```text
numeric objects                         53
%d occurrences                         60
%u occurrences                         10
remaining ordinary inline R1 objects  102
inline R1 source-role objects          141
```

The three restored independent physical owners are:

```text
0x6A7C21  いくら投資しますか？\n(1000～%d)
0x68F1DC  いくつ買いますか？\n(1～%d)
0x683FC4  賄賂をいくら渡しますか？\n(1～%d)
```

They are not new translations. They were independent Switch logical objects incorrectly collapsed out of the earlier intermediate count.

## 3. Materialized population

V299 adds:

```text
candidate IDs             53
classification IDs        53
INCLUDE_KO rows           53
```

ID ranges:

```text
SEL-CAND-000040 .. SEL-CAND-000092
SEL-CLS-000040  .. SEL-CLS-000092
```

Cumulative selective corpus after V299:

```text
candidate IDs             92
classification IDs        92
INCLUDE_KO rows           92
R1 materialized rows      92
```

The previous 39 V298 ending-help rows remain unchanged.

## 4. Per-row evidence

Every V299 row contains actual individual values for:

- contributing PC inline source IDs / RNUMs / RVAs;
- complete Switch Japanese logical object;
- complete reconstructed PC-Korean logical payload;
- exact Switch physical-owner offset;
- exhaustive `R_AARCH64_RELATIVE (0x403)` consumer-slot membership for that owner;
- format-token signature and insertion-following literals;
- Korean payload length including NUL;
- current proven storage capacity and slack;
- mechanism / usage / investigation status;
- caller/consumer compatibility;
- evidence/provenance and derived disposition.

No family placeholder row is used.

Population evidence:

```text
physical objects              53 unique
PC inline source records      60 unique
RELA consumer slots           54 unique
single-slot owners            52
two-slot owners                1
original-guard failures        0
format-token mismatches        0
capacity failures              0
manual overrides               0
risk-flagged rows              0
```

## 5. Generation mechanism

Format signatures:

```text
%d          33 objects
%d + %d     10 objects
%u + %d      7 objects
%u           3 objects
```

The Japanese and PC-Korean payloads preserve token type and order for all 53 objects.

Observed insertion followers contain fixed literals such as punctuation, range separators, and literal units (`貫`, `文字`, `人`, `石`). No selected slot is followed by a Japanese particle requiring Korean allomorph selection.

Therefore the 53 rows are classified:

```text
mechanism_class          VARIABLE_INSERT
variable_source_kind     RUNTIME_DATA
jp_particle_adjacency    NO
dynamic_counter_decision NO
```

They are not `NUMERIC_COUNTER_FORMAT`; there is no proven runtime unit/counter/morphology selection. This applies the canonical rule that a numeric slot followed by a fixed literal unit remains ordinary `VARIABLE_INSERT`.

## 6. Owner / consumer topology

All 53 Switch physical strings occur as addends in `.rela.dyn` `R_AARCH64_RELATIVE (0x403)` records whose `r_offset` entries provide runtime source/consumer slots.

This explains why direct ADR/ADRP string-address XREF scans do not enumerate their consumers.

Topology:

```text
53 physical owners
54 RELA consumer slots
52 owners -> 1 slot
 1 owner  -> 2 slots
```

The shared owner is:

```text
owner 0x68F1DC
JP    いくつ買いますか？\n(1～%d)
KO    몇 개 살까요?\n(1~%d)
slots 0x9C1D60, 0x9C1E08
```

Both slots belong to compatible purchase-quantity contexts and use the same one-`%d` visible-output responsibility. No caller-specific Korean surface conflict was found.

Reusable rule:

> For this Switch inline family, absence of direct string-address code XREF is not absence of consumers. Check `.rela.dyn R_AARCH64_RELATIVE -> r_offset slot -> physical owner` before declaring caller/consumer evidence unavailable.

This rule may be useful when revisiting other indirect inline owners, including currently deferred consumer questions, but V299 does not automatically resolve those other rows.

## 7. Capacity

Current storage realization is sufficient for all 53 rows:

```text
KO payload incl NUL   15..39 bytes
proven capacity       18..45 bytes
minimum slack          0 bytes
maximum slack         13 bytes
exact-fit rows          3
capacity failures       0
```

All resulting payloads terminate before the next nonzero logical object. No redirect or alternate storage is required by this family at classification time.

Capacity PASS is not runtime/layout PASS.

## 8. Classification result

All 53 rows satisfy the current R1 classification gates:

```text
usage_class             UI_DESCRIPTION
mechanism_class         VARIABLE_INSERT
investigation_status    RESOLVED
physical owner          RESOLVED
consumer-slot topology  RESOLVED
particle risk           NONE
dynamic counter         NO
cross-message consumer  NONE
PC logical conflict     NONE
capacity                PASS
manual override         NO
derived_disposition     INCLUDE_KO
```

`INCLUDE_KO` is a product/classification disposition only.

It does not imply:

```text
implementation WRITE_SAFE
builder PASS
IPS PASS
runtime formatting PASS
font/render PASS
layout PASS
hardware/gameplay PASS
```

## 9. Remaining ordinary-inline R1 state

After V299, the canonical source-role census is:

```text
INLINE R1 source-role total             141

V298 ending-help                         39  materialized INCLUDE_KO
ordinary inline                         102
  static-like                            49
    selected-use structurally resolved  47  not yet row-materialized
    consumer unresolved                  2  R2884 / R2885
  numeric VARIABLE_INSERT               53  V299 materialized INCLUDE_KO
```

Thus:

```text
materialized R1 INCLUDE_KO = 92
structurally resolved but not materialized static = 47
remaining source-role unresolved = 2
```

The two unresolved static rows remain deferred evidence waits, not rejected rows. They are not included in V299.

## 10. Do-not-repeat / superseded interpretations

Do not repeat:

- `numeric R1 = 50`;
- `%d count = 57`;
- `remaining ordinary inline R1 = 99`;
- `inline R1 source-role = 138`;
- `direct string XREF = 0` means the object has no consumer;
- any `%d/%u` string is automatically `NUMERIC_COUNTER_FORMAT`;
- raw textual equality authorizes collapsing separate physical objects.

## 11. No implementation authority

V299 performs no builder, Switch write, build, IPS generation, runtime test, or hardware test.

Repository write scope for V299 is documentation/corpus materialization only.
