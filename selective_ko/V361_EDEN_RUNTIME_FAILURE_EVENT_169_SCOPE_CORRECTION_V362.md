# V361 Eden runtime failure / EVENT 169-file scope correction — V362

Date: 2026-09-21 (KST)

```text
validation_id   V362
track           SWITCH_SELECTIVE_KOREANIZATION
scope_kind      RUNTIME_EVIDENCE_AND_SCOPE_CORRECTION_CHECKPOINT
parent          f64a63bdfad3b7b8b886ae882e3e7b315e5b1351 / V361
product_bytes   UNCHANGED
code            UNCHANGED
build/package   NONE
repository      DOCUMENTATION_ONLY
```

This checkpoint records the user-supplied Eden runtime evidence for the exact V361 package and corrects the EVENT ownership scope that had been narrowed too aggressively to `ECF00000.TS5`.

All earlier VERIFIED/CLOSED facts remain inherited unless explicitly superseded here.

## 1. V361 runtime evidence

The user ran the V361 diagnostic package and revisited ordinary dialogue screens that had remained Japanese under V358.

Observed result:

```text
boot / scene progression             PASS
Korean TAI5MSG/description route     still observable
ordinary dialogue body               JAPANESE
V361 expectation "EVENT dialogue KO" NOT MET
runtime verdict                      FAIL_EXPECTATION
```

Representative observed Japanese surfaces include:

```text
大殿を助け
相良家の力を強めていかねばならぬ…
ふぅ……
美味い
```

This is sufficient to close the V361 ordinary-dialogue expectation as failed. Repeating the same V361 package is not required.

## 2. EVENT family census correction

Direct inspection of the PC Korean patch v1.02 embedded replacement manifest established:

```text
PC Korean patch EVENT .TS5 replacements   169
all replacement originals differ          169 / 169
embedded replacement payload identity      169 / 169
```

The Switch v1.1.3 decompressed `main` contains resource-path literals for the same EVENT family:

```text
EVENT\\*.TS5 path members   169
EVENT\\*.TE5 path members   169
```

The exact 169 Switch TS5 filename set and the exact 169 PC-patch replacement TS5 filename set are equal:

```text
Switch-only names    0
PC-patch-only names  0
set equality         PASS_169_OF_169
```

Family breakdown of the 169 TS5 names:

```text
EC500000-family     1
ECF-family          1
EF5-family          2
EFF-family         71
EKF-family          3
EP non-EPF         13
EPF-family         78
---------------------
TOTAL              169
```

Therefore `ECF00000.TS5` is one member of a 169-file EVENT TS5 family, not the complete ordinary-dialogue carrier universe.

## 3. Path correction

The Switch v1.1.3 `main` directly contains the resource path:

```text
EVENT\\ECF00000.TS5
```

and corresponding paths for the other EVENT members.

Therefore the V361 LayeredFS placement:

```text
romfs/EVENT/ECF00000.TS5
```

is structurally consistent with the actual Switch resource path.

The post-V361 working hypothesis that the Japanese-dialogue result was caused by an incorrectly guessed `romfs/EVENT/` path is rejected.

## 4. Screenshot dialogue ownership consequence

The representative Japanese surfaces above were searched against the currently available original carrier sources using the established original game-code mapping representation.

No matching encoded surface was found in the currently available:

```text
ECF00000.TS5
TAI5MSG_JP.DAT
SNR0_JP.TR5 .. SNR8_JP.TR5
CWTDAT_JP.TR5
Switch main
```

This is consistent with ownership by another EVENT TS5 member, but the exact filename is not yet closed because the full Switch v1.1.3 `romfs/EVENT/` subtree is not yet available as extracted files.

Do not infer an exact EFF/EP/EPF owner until the raw Switch EVENT family is supplied and searched.

## 5. Source requirement now active

The next bounded source requirement is no longer the whole RomFS.

Required exact Switch v1.1.3 subtree:

```text
romfs/EVENT/
  169 x *.TS5
  169 x paired *.TE5
```

Preserve exact extracted relative paths and raw bytes.

The 3.88 GB combined XCI is present in project storage, but the current Drive connector cannot download a single file above its 256 MiB transfer limit. This transport limitation does not authorize substituting PC originals for Switch originals.

A user-side extraction of only the exact `romfs/EVENT/` subtree is sufficient for the next scope.

## 6. 확정된 사실

- V361 ordinary dialogue remained Japanese in user-run Eden runtime.
- V361's expected ordinary EVENT Korean output did not occur.
- The V361 `romfs/EVENT/ECF00000.TS5` relative path is supported by the Switch v1.1.3 `main` resource-path table.
- The PC Korean patch replaces 169 EVENT TS5 files, not only `ECF00000.TS5`.
- The Switch v1.1.3 `main` names 169 EVENT TS5 and 169 paired TE5 resources.
- Switch TS5 names and PC-patch EVENT replacement TS5 names match 169/169.
- `ECF00000.TS5` is 1/169 of the EVENT TS5 family.
- No new product byte, code, IPS, package, or translation was changed by V362.

## 7. 유력한 가설

The dominant explanation for the still-Japanese ordinary dialogue is that the tested dialogue is owned by one of the other 168 EVENT TS5 members that V361 did not replace.

This hypothesis is stronger than the rejected wrong-path hypothesis and is directly consistent with the PC patch's 169-file replacement model.

## 8. 미확정 사항

- exact TS5 owner of each captured Japanese dialogue surface;
- byte parity of all 169 Switch TS5 files against the corresponding PC originals;
- whether all 169 files share the same serializer/interpreter compatibility already proven for `ECF00000.TS5`;
- exact PC-KO selective-admission policy needed outside `ECF00000.TS5`;
- paired TE5 relevance outside the already-closed `ECF00000` case;
- EVENT-family layout/reflow burden outside the current ECF audit.

## 9. 기각된 가설 / do-not-repeat

- `romfs/EVENT/ECF00000.TS5` is a guessed or incorrect Switch resource path — REJECTED by Switch `main` resource-path evidence.
- `ECF00000.TS5` alone is the complete ordinary-dialogue EVENT carrier — REJECTED by the exact 169-file PC-patch replacement family and matching Switch filename set.
- V361 Japanese ordinary dialogue proves font or Mapping failure — REJECTED; Korean TAI5MSG/description output remains observable.
- Repeat V361 unchanged to obtain the same ordinary-dialogue answer — NOT REQUIRED.
- Guess the screenshot's exact EFF/EP/EPF owner without the Switch EVENT subtree — FORBIDDEN.

## 10. 관련 영향 범위

The active EVENT scope expands from one ECF carrier to the full 169-member Switch/PC-corresponding TS5 family.

This does not reopen already-closed ECF00000 structural work, Mapping 10,036, font closure, TAI5MSG V357, or the known non-B24 reflow family.

SNR, inline 139, and ordinary non-B24 reflow remain separate cause families and must not be mixed into the next EVENT parity audit.

## 11. 수정 제안 / exact next scope

`SWITCH_V113_EVENT_169_SOURCE_PARITY_AND_PC_PATCH_PORTABILITY_AUDIT_READ_ONLY`

READ ONLY.

Required bounded work after a fresh explicit user execution signal:

1. obtain the exact Switch v1.1.3 `romfs/EVENT/` subtree preserving raw names and bytes;
2. census all 169 TS5 + 169 TE5 Switch members;
3. compare each Switch TS5 to its same-name PC original and PC-KO replacement;
4. locate the captured Japanese runtime surfaces to exact Switch EVENT owners;
5. classify structural parity families before proposing any serializer or product mutation;
6. inspect paired TE5 only by evidence, not by filename assumption;
7. do not modify/build/package/translate during this scope.
