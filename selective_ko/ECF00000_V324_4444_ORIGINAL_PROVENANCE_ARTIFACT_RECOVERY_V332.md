# ECF00000 V324 4,444 ORIGINAL PROVENANCE ARTIFACT RECOVERY — V332

Date: 2026-09-20 (KST)

```text
validation_id   V332
track           SWITCH_SELECTIVE_KOREANIZATION
scope_kind      READ_ONLY_PROVENANCE_RECOVERY_CHECKPOINT
parent          9214d1343babe9fc110ba35f804dd96fde073cae / V331
product_bytes   UNCHANGED
code            UNCHANGED
build/package   NONE
repository      DOCUMENTATION_ONLY
```

This checkpoint closes the bounded search for the original V324 exact 4,444-row census code or materialized row artifact. It does not declare the historical aggregate false. It records that the exact physical membership and generating code path are not recoverable from the currently preserved repository, project Drive, or Library/Project-file material and therefore cannot be used as serializer authority.

## 1. 확정된 사실

Repository state at analysis start:

```text
main HEAD  9214d1343babe9fc110ba35f804dd96fde073cae
drift      NONE
```

The V324 commit is:

```text
b9f40519a8f043bb8871c4e3ef328ed29809b0ff
docs: close V324 EVENT TS5 parity and census
```

V323 -> V324 is exactly one commit. The V324 commit persisted only these three files:

```text
PROJECT_STATE.md
selective_ko/DIALOGUE_EVENT_TS5_SWITCH_PARITY_AND_CENSUS_CHECKPOINT_V324.md
selective_ko/SELECTIVE_PROJECT_STATE.md
```

No census source code, Python script, notebook, JSON, CSV, exact physical-offset rowset, ledger, or parser artifact was committed with V324.

The V324 report preserves aggregate results including:

```text
target path occurrences     4,464
unique physical targets     4,444
messages                    4,193
choices                       251
choice strings                504
physical newline bytes      4,212
```

but does not preserve the exact 4,444 physical offsets.

Accessible project Drive searches for V324-era census/code/artifact terms did not recover an original V324/V325/V326 census artifact. The surviving 2026-09-19 EVENT diagnostic folders recovered in the project Drive are V327, V329, V330, and V331-era diagnostics.

Accessible Library/Project-file searches likewise did not recover the original V324 census code or exact 4,444-row materialization.

The currently preserved simple outer walker reproduces only the V327 diagnostic subset:

```text
physical targets  2,817
messages          2,569
choices             248
```

The V330/V331 EVENT<->BRANCH two-context replay reproduces:

```text
physical targets  2,863
messages          2,614
choices             249
Korean targets    2,656
INCLUDE_KO        2,542
UNRESOLVED          114
```

Neither is the historical exact 4,444 rowset.

## 2. 유력한 가설

The most likely provenance explanation is that the V324 aggregate was produced by temporary analysis code or an ephemeral execution environment and only the resulting aggregate counts were carried into documentation.

This is a provenance explanation, not proof that 4,444 is numerically false.

## 3. 미확정 사항

The original V324 generating path no longer establishes, with recoverable evidence:

- whether additional nested-command traversal beyond the later reconstructed rules was used;
- which branch/internal regions were included;
- whether command spans containing later entrypoints were traversed separately;
- whether deduplication identity was physical address only or context plus address;
- whether any PC-editor false-positive guards were mixed into the census;
- the exact ordered or unordered set of 4,444 physical offsets.

These remain unknown and must not be guessed.

## 4. 기각된 가설

Do not repeat:

- a pure `p += handler_length` outer walker as the source of 4,444;
- EVENT-only nested traversal as sufficient to reproduce 4,444;
- EVENT/BRANCH two-context recursion as sufficient to reproduce 4,444;
- PC editor v0.30 grouping as the direct source of the 4,444 runtime target population;
- raw scanning of `11/12/13/15` bytes as a substitute for structural parsing;
- filtering the PC editor's 15,945 target-looking items until the result numerically equals 4,444;
- tuning any new parser against 4,444 as a target value.

The historical count is evidence, not a fitting objective.

## 5. 관련 영향 범위

Unchanged and still authoritative:

- Switch/PC-original ECF00000 carrier byte parity;
- PC-Korean ECF00000 payload identity;
- Mapping 10,036;
- Korean font and glyph closure findings;
- PC editor v0.30 edit-time branch arithmetic and false-positive guards;
- Switch EVENT/BRANCH runtime descriptor and context findings;
- identity presentation policy;
- TAI5MSG/B24 results;
- all unrelated VERIFIED/CLOSED scopes.

Historical aggregate claims remain preserved:

```text
physical targets  4,444
messages          4,193
choices             251
Korean targets    4,238
INCLUDE_KO        4,123
UNRESOLVED          115
```

However, exact row membership for those aggregates is not available. Therefore they are not authorized as exact serializer membership.

Blocked until a new deterministic corpus definition is independently justified:

- EVENT exact selective serializer rowset;
- exact V326 4,123 INCLUDE_KO membership;
- exact V326 115 UNRESOLVED membership;
- semantic-adjacency closure that depends on those exact rows;
- EVENT payload implementation/build/package based on historical row membership.

## 6. 수정 제안

Close provenance recovery here rather than repeatedly searching for an artifact that is not present in the accessible preserved material.

The next analysis scope must define a deterministic EVENT physical-command corpus from two already established authorities:

```text
PC editor v0.30 source-proven edit/preservation rules
+
Switch EVENT/BRANCH runtime descriptor/handler rules
->
deterministic physical-command corpus contract
```

The new corpus design must define, before implementation:

- source-of-truth boundary between edit-time and runtime rules;
- physical-command identity;
- traversal-state identity;
- nested/branch inclusion rules;
- deduplication rules;
- false-positive handling;
- deterministic acceptance and replay gates;
- independence from the historical number 4,444.

If the future deterministic corpus count differs from 4,444, it must be judged by provenance and reproducibility rather than adjusted to match 4,444.

## 7. Exact next scope

After a fresh explicit user execution signal:

`ECF00000_DETERMINISTIC_PHYSICAL_COMMAND_CORPUS_DESIGN_READ_ONLY`

Authorized:

- READ ONLY design analysis;
- derive the corpus contract from V331 PC editor authority plus V330 Switch runtime authority;
- compare obligations against V324-V331 evidence;
- specify deterministic gates and rejected shortcuts.

Not authorized:

- parser implementation;
- serializer implementation;
- EVENT payload rewrite;
- build/package/IPS;
- tuning against 4,444;
- unrelated EVENT files;
- SNR.

No gameplay byte, builder, parser implementation, package, build, or IPS is changed by V332.
