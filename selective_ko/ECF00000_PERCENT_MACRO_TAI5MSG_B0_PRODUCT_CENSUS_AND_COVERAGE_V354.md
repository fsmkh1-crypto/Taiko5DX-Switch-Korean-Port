# ECF00000 percent-macro ↔ TAI5MSG B0 product census and current coverage — V354

Date: 2026-09-20 (KST)

```text
validation_id   V354
track           SWITCH_SELECTIVE_KOREANIZATION
scope_kind      READ_ONLY_ANALYSIS_CLOSURE
parent          0737bd6b69cddfdb8d93f9ea90e75decf02ff5f3 / V353
implementation  NONE
product bytes   UNCHANGED
build/package   NONE
hardware        NOT RUN
```

## 1. Scope

V354 closes the bounded product-admitted `%xx` census and the direct-root current selective-TAI5MSG coverage check. It intentionally does not perform nested dependency traversal or root-role classification.

```text
product-admitted EVENT rows        12,594
rows containing used %xx            1,760
%xx occurrences                     2,440
used %xx tokens                        46 / 52
unused %xx tokens                       6 / 52
```

Unused exact token set: `%04 / %0C / %12 / %1F / %20 / %33`.

## 2. Exact root mapping result

V353 Switch authority remains binding: `%xx` dispatch table `RODATA 0x6AC004`, 52 entries, TAI5MSG getter `0x43F2A4`.

```text
used tokens           46
unique B0 roots       46
root collisions        0
all roots in B0       PASS
```

V353 anchors replay exactly: `%15 -> 0:209`, `%21 -> 0:349`, `%2A -> 0:395`.

Machine-readable exact mapping: `selective_ko/artifacts/ecf00000_v354_percent_macro_tai5msg_b0_product_census_v1/USED_PERCENT_MACRO_ROOTS.jsonl`.

## 3. Current selective TAI5MSG coverage

V303/V308/V309 authority: 14,832 total messages, 3,179 selected PC-KO, 11,653 unselected JP, and only B0 locals 10/11 selected. V309 byte-exact replay proves unselected messages remain JP bytes.

None of the 46 product-used percent-macro B0 roots is local 10 or 11.

```text
used B0 roots current KO       0 / 46
used B0 roots current JP      46 / 46
direct-root KO coverage        0.0%
direct-root JP preserved     100.0%
```

This is a systematic direct-root coverage gap, not only a suffix-three exception.

## 4. Interpretation boundary

The 2,440 percent-macro occurrences must not all be labeled runtime-visible Japanese defects yet. V354 establishes direct-root byte state only. Per-root language role, caller-local flattening, nested dependencies, and any language-neutral exceptions remain unclassified.

`JP root state != automatically authorized global root replacement`

## 5. Inherited validations

```text
V309 selective TAI5MSG serializer       PASS preserved
V349 EVENT serializer/relocation        PASS preserved
V352 EVENT serializer/relocation        PASS preserved
%xx runtime-language integration        OPEN
```

## 6. Rejected / do-not-repeat

- assume current selective TAI5MSG already covers a substantial subset of used `%xx` roots;
- assume B0 locals 10/11 are common support roots for `%xx`;
- inspect all 14,832 TAI5MSG messages before classifying the exact 46 roots;
- traverse all V288 grammar families before root-role classification;
- treat all 46 JP roots as automatically eligible for global PC-KO replacement;
- reopen the V353 52-entry dispatch mapping.

## 7. Exact next scope

`ECF00000_PERCENT_MACRO_TAI5MSG_B0_ROOT_ROLE_LANGUAGE_OUTPUT_CLASSIFICATION_READ_ONLY`

Inspect only the exact 46 roots, compare PC-original and PC-Korean content at the same locator, classify root role/language output, and identify only the subset needing nested-dependency analysis. Preserve caller-local responsibility policy. No EVENT/TAI5MSG mutation, full V288/TAI5MSG scan, build/package/IPS, or hardware.
