# NAME DATA INVESTIGATION PLAN

Canonical scope-control plan for the post-W1 person-name investigation.

## Purpose

The W1 runtime result invalidated the narrow hypothesis that mapped `0x44D9D0` directly caused the missing `쓰` in the tested Matsudaira nameplate. Static inspection then established that the corresponding Switch `松平元康` fixed fields are duplicated and were both skipped by the historical D5519 unique-only selector.

The remaining person-name problem must therefore be investigated as one root-cause family without turning into an unbounded scan of every untranslated string.

## Scope split

The person-name root-cause family is split into five investigation groups. Only one group is executed per user authorization unless the user explicitly expands the scope.

### A — duplicated original-name fixed slots

Find person-name fixed fields whose original Japanese byte pattern occurs more than once on Switch and was therefore excluded by historical unique-only matching. Establish counts, locations, field structure, and whether each repeated occurrence is a true name object rather than an incidental substring.

Do not patch them in this group.

### E — PC Korean-patch correspondence

For candidates established in A, verify the actual PC T5K replacement bytes and whether repeated PC records agree. Use the PC patch as ground truth for spelling, compact glyph codes, field length, and replacement semantics.

Do not infer Korean names from romanization or screen appearance.

### B — renaming / historical-name chains

Investigate person records that change names over time, such as childhood/adult/historical names, and determine how multiple name slots are associated with one person identity.

### C — aliases / common names / alternate display names

Investigate aliases, common names, titles, and alternate names that may be selected differently by events, lists, dialogue, biographies, or other UI contexts.

### D — nameplate-specific selection/render path

Trace event/person ID -> active current-name/alias slot -> any copy/cache/temporary buffer -> rendered name object. Determine whether a nameplate uses the canonical person record directly or a separately selected/cached display field.

## Investigation order

Default order:

```text
A -> E -> B -> C -> D
```

Rationale: first establish the duplicated-data population, then attach exact PC replacement evidence before tracing more complex rename/alias/runtime selection behavior.

## Execution gate

- One group is investigated at a time.
- After each group, report `confirmed facts / likely hypotheses / unresolved items / invalidated hypotheses / affected scope / proposed next step`.
- That report does not authorize the next group.
- No patch, diagnostic build, or builder integration is authorized merely by completing an investigation group.
- A new explicit user execution signal is required before entering the next investigation group or creating a patch/build.

## Current authorized group

As of 2026-09-11, user authorization covers **Group A only** after recording this plan.
