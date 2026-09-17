# INLINE R1 LOGICAL-OBJECT RECONSTRUCTION AND REUSABLE RULES — V297

Date: 2026-09-18 (KST)
Status: READ-ONLY ANALYSIS MATERIALIZED / NO CANDIDATE IDS / NO INCLUDE_KO ROWS / NO BUILD
Track: `SWITCH_SELECTIVE_KOREANIZATION`
Scope: `INLINE_R1_LOGICAL_OBJECT_RECONSTRUCTION_AND_REUSABLE_RULES_V297`

## 1. Purpose

This document materializes the read-only inline R1 logical-object reconstruction performed after V296 and records the reusable analysis rules learned from it.

It does not create candidate/classification IDs, authorize Switch writes, create `INCLUDE_KO` rows, modify gameplay data, build IPS, or start a builder.

V296 claim-strength rules remain binding:

```text
source fact != owner proof
owner proof != WRITE_SAFE
WRITE_SAFE != INCLUDE_KO
build/package PASS != gameplay PASS
```

## 2. Source reconstruction baseline

The PC Korean patch T5K inline layer was independently reproduced from the canonical patch source:

```text
inline raw records                         = 17,103
exact (original bytes, replacement bytes) = 8,751 semantic groups
external provisional triage               = YES 205 / UNCERTAIN 227 / NO-MEDIUM 5 / NO-HIGH 8,314
```

The external triage remains a semantic prefilter only. It is not a corpus authority.

One external-YES group, bundle row 2768, has an all-NUL replacement and is not Korean-bearing. Therefore:

```text
Korean-bearing external-positive groups      = 204
PC source occurrences represented by them    = 206
```

After logical normalization of the PC original component:

```text
single Switch location occurrences            = 191
those occurrences collapse to logical objects = 189
positive multi-match semantic groups           = 13
```

The earlier intermediate value `189 unique occurrences` is withdrawn. Correct wording is `191 single-location occurrences -> 189 distinct logical objects`.

## 3. External UNCERTAIN reconstruction findings

The 227 UNCERTAIN groups expand to 658 PC source occurrences.

Important results:

```text
UNCERTAIN groups with one Switch location = 125
UNCERTAIN fragments proven to attach to positive logical objects >= 28
zero raw-match groups = 11
```

The 11 zero-match groups are not evidence that Switch text is absent:

```text
8 = NUL/padding-only source fragments
3 = PC UTF-16LE wide-string duplicates / runtime UI strings
```

The PC wide-string examples include a UTF-16LE form of `ゲームを終了してよろしいですか？`; Switch contains the semantic UI in a different CP932 object.

Therefore `raw zero match -> missing Switch sentence` is rejected.

## 4. Ending-table structural closure

A repeated ending table was reconstructed in Switch `main` as a fixed-stride structure:

```text
record count  = 39
record stride = 0x3FF = 1023 bytes

per record:
  title       = 21 bytes
  help        = 501 bytes
  narration   = 501 bytes

offsets:
  title       = +0x000
  help        = +0x015
  narration   = +0x20A
```

This gives 117 Switch text objects in the table:

```text
39 title + 39 help + 39 narration
```

The whole ending-table region is covered by 208 PC inline patch records.

Correction of an earlier intermediate statement:

```text
208 = PC inline records across the whole 117-object ending table
102 = PC inline records belonging specifically to the 39 help fields
```

Do not repeat the superseded statement `39 ending-help objects = 208 PC records`.

## 5. Ending-help Korean payload reconstruction

All 39 help fields were reconstructed from the PC Korean patch at logical-object level.

Validation:

```text
help objects                            = 39/39
help-field PC records                   = 102
whole ending-table PC records assigned = 208/208
original-byte mismatch                 = 0
PC RVA <-> Switch object-relative affine violations = 0
Korean decode failures                 = 0
```

The completed Korean help payloads all fit the Switch fixed field:

```text
Switch help-field capacity = 501 bytes
longest Korean payload including NUL = 412 bytes
minimum remaining slack = 89 bytes
capacity PASS = 39/39
```

These are source/structure/capacity facts. No release row is created by this document.

## 6. Ending-help usage and mechanism evidence

The ending detail consumer indexes the repeated records by `index * 0x3FF` and consumes the help field at `+0x15`; narration is at `+0x20A`.

No same-sentence message-fragment append or grammar-producing formatter was found for the help field in the analyzed route.

The reconstructed help payloads contain no dynamic `%d` / `%s` insertion responsibility. A visible percentage such as `80%` is literal text, not a runtime format token.

Source-side/route classification supported by current evidence:

```text
usage_class      = UI_DESCRIPTION
mechanism_class  = STATIC_COMPLETE
append_after     = NO
investigation    = RESOLVED for the analyzed ending-help route
```

R1 product definition still requires derived `INCLUDE_KO`; this document does not materialize that disposition.

## 7. Multi-match prompt closure

Five UI-prompt-like positive multi-match cases were investigated. Four were the previously outstanding prompt-owner set after the already-closed attack-target prompt.

Exact results:

```text
Attack target prompt:
  canonical PC R645 / INLINE:00644
  F1 category DIRECT
  localization_id 1808
  logical_owner_count 1
  target_object 6938194

R2799 / INLINE:02798  -> DIRECT, owner_count 1, target_object 6862647
R2975 / INLINE:02974  -> DIRECT, owner_count 1, target_object 6957335
R3013 / INLINE:03012  -> DIRECT, owner_count 1, target_object 6921870
```

### R651 correction / closure

Historical L3 semantic review intentionally left canonical R651 unresolved and requested targeted consumer/XREF tracing.

Selected-use source-sequence analysis now resolves the target without requiring the unavailable exact PC executable:

```text
R649  `投資する`      -> unique Switch anchor at 0x6A7C18
R651  investment prompt candidate -> 0x6A7C21
R652  suffix fragment -> same object at 0x6A7C39
```

The same sequence reconstructs:

```text
いくら投資しますか？\n(1000～%d)
```

The alternate R651 raw candidate belongs to a different semantic object (`いくら献上しますか？...`) and does not satisfy the R649 -> R651 -> R652 source sequence.

Therefore for selected-use owner binding:

```text
R651 old state = UNRESOLVED in historical L3 overlay
R651 current evidence = TARGET_RESOLVED_BY_SELECTED_USE_SEQUENCE
Switch target = 0x6A7C21
```

The historical L3 artifact is retained as provenance; it is not silently rewritten.

## 8. Occurrence-conflict hazard retained

Two positive groups corresponding to historical sources around R3039/R3042 share the same Japanese original surface but carry substantively different PC Korean replacements (`더 낮출 수 없습니다` vs `더 줄일 수 없습니다`).

Treat this family as `PC_OCCURRENCE_CONFLICT` evidence until caller/owner context is applied. Do not globally collapse same-Japanese-original rows into one Korean replacement.

## 9. Reusable reconstruction rules

The following rules are reusable for other inline families and containers.

### 9.1 Diff-run is not a logical string

A PC inline patch record may:

- begin/end inside a logical string;
- contain an internal NUL and bytes belonging to another field/window;
- represent only changed bytes while unchanged bytes are absent from the record.

Therefore:

```text
patch record != logical object
semantic group != logical object
```

Reconstruct against Switch structural boundaries before semantic classification.

### 9.2 Replacement may consume source padding

A PC replacement can use bytes that were NUL padding in the original as continuation bytes for Korean text.

Therefore the first NUL in the Japanese source is not automatically the end of the Korean payload.

For a fixed field/table, use the proven field boundary/capacity, not the source text's first NUL, as the maximum structural boundary.

### 9.3 Object-first reconstruction

Preferred order:

```text
PC diff record
-> Switch physical/logical object boundary
-> recover unchanged bytes / relative placement
-> reconstruct complete PC Korean payload
-> classify usage/mechanism
-> owner/caller/risk/capacity
-> derived disposition
```

Do not classify fragment-level AI output directly as release corpus rows.

### 9.4 Relative-offset affine validation

When a family appears table-like or contiguous, validate every contributing record with:

```text
PC_RVA - Switch_target_offset = constant delta within the proven family
```

Together with original-byte guards, zero affine violations provide stronger family binding than raw-text equality alone.

Do not generalize the affine relation outside the proven family/bounds.

### 9.5 Source-sequence disambiguation

When one raw Japanese fragment has multiple Switch candidates, use adjacent PC source obligations and containment to disambiguate:

```text
previous anchored source
-> ambiguous source fragment
-> following source fragment
-> same Switch logical object / expected adjacency
```

This method resolved R651 where raw prefix matching alone could not.

Raw uniqueness or raw multiplicity by itself remains non-authoritative.

### 9.6 Repeated-stride table discovery

For repeated data structures, search for stable:

- record stride;
- repeated internal field offsets;
- caller indexing arithmetic;
- record-relative references.

A stable `index * stride + field_offset` consumer can establish field ownership/capacity more strongly than NUL scanning alone.

The ending table is the current proof example (`0x3FF`, `+0x15`, `+0x20A`).

### 9.7 Decoder precedence

Do not use the entire Mapping 10,036 table as a naive inverse decoder for PC replacement bytes because source code values can collide/alias with ordinary CP932 values.

For PC inline Korean payload decoding use the proven source layers in precedence order:

```text
1. compact one-byte Hangul 0xA1..0xDF (63 glyph map)
2. Korean-added two-byte mapping domain (2,542 additions)
3. ordinary CP932 for Japanese/ASCII/punctuation bytes
```

This prevents duplicate-code artifacts such as mis-decoding ordinary full-width/CP932 characters through a broad inverse map.

### 9.8 UTF-16/mixed UI is a separate family

PC UTF-16LE runtime/UI strings must not be treated as failed CP932 inline matches. Identify encoding/storage family before declaring a Switch miss.

## 10. Superseded intermediate claims

The following intermediate statements are explicitly superseded by this document:

```text
`189 unique positive occurrences`       -> use `191 single-location occurrences -> 189 objects`
`39 ending-help = 208 PC records`       -> use `39 help = 102 records; whole ending table = 208`
`UNC zero-match NUL/padding = 7`         -> correct count = 8; plus 3 UTF-16LE groups
`R651 can only be closed with exact PC EXE` -> rejected for selected-use target binding
```

## 11. Remaining boundaries / unresolved work

Still not materialized:

```text
selective candidate IDs       = 0
classification IDs            = 0
selective INCLUDE_KO rows     = 0
selective builder             = NOT IMPLEMENTED
selective build / IPS         = NONE
```

The 39 ending-help objects have enough current evidence to enter a dedicated candidate/classification materialization audit, but that is a separate stage and requires a fresh user execution signal.

Runtime QA remains necessary after any later build for font rendering, line wrapping, on-screen overflow, correct ending-index selection, and actual hardware behavior.

The exact target PC v1.2.1.0 build-9163702 EXE remains unavailable; exact whole-program PC XREF/runtime-equivalence claims that depend on it remain blocked/HINT. This does not reopen the ending-help or R651 closures above because those closures use Switch structure plus exact PC patch bytes/source sequence rather than guessed PC runtime parity.

## 12. Next scope

Recommended next scope after a fresh explicit user signal:

```text
SELECTIVE_KO_ENDING_HELP_39_CANDIDATE_CLASSIFICATION_MATERIALIZATION
```

Purpose:

- materialize 39 ending-help candidates with exact source/object provenance;
- record `UI_DESCRIPTION + STATIC_COMPLETE + RESOLVED` evidence;
- derive disposition only after confirming required common metadata/risk gates;
- materialize the R651 selected-use target-resolution correction as provenance;
- do not start builder/build/IPS in the same stage.
