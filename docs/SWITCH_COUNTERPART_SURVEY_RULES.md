# Switch Functional Counterpart Survey Rules

Date: 2026-09-11
Status: INPUT CONTRACT FOR NEXT STAGE / NOT YET AUTHORIZED

## 1. Purpose

This document defines how the next Switch counterpart survey must be conducted after PC Runtime Canonical Closure. It does not itself start that survey and does not authorize ARM64 edits, IPS, builds, or runtime tests.

The survey input authority is:

- `docs/PC_RUNTIME_DLL_SPEC.md`
- `docs/PC_RUNTIME_CANONICAL_CLOSURE.md`
- `docs/PC_RUNTIME_SWITCH_COUNTERPART_MATRIX.md`
- validation ledger V001–V061
- existing Switch runtime/static evidence already recorded in `PROJECT_STATE.md`, `docs/RUNTIME_TEST_RESULTS.md`, `docs/POST_D5519_ANALYSIS.md`, `PATCH_MAP.md` and related validated records.

## 2. Survey objective

For every closed PC semantic family, determine the complete Switch counterpart set and classify each item as:

- counterpart required;
- counterpart found;
- concrete native-equivalent candidate;
- native-equivalent verified within stated scope;
- unresolved / not found.

Do not design or implement the final patch during the survey.

## 3. Required functional axes

The survey must cover at least these five primary axes independently:

1. mapping 10,036 storage / references / counts;
2. pointer 56, including mode-0 and mode-1 semantics and replacement-string ownership;
3. helper semantic entries: page mapper and byte-validation/copy path;
4. all 14 descriptor subpatch semantics, including width/font/threshold/mapping/helper families;
5. inline 17,103 / repeated objects / fixed fields / data-selection coverage.

CWTDAT compatibility is a separate data-port axis and must not be silently folded into the runtime counterpart result.

## 4. No uniqueness gate

PC descriptor search requires a unique x86 signature at an exact PC anchor. That is a Windows target-version validation mechanism, **not** a Switch counterpart discovery rule.

Switch survey rules:

- never require one unique byte match as proof of one counterpart;
- PC one-site behavior may correspond to multiple ARM64 sites;
- enumerate all sites with the same semantic role;
- distinguish code/data objects from raw substring matches;
- if one semantic family occurs at six sites, all six belong to the family unless evidence excludes one;
- if a candidate is ambiguous, keep it unresolved instead of selecting a convenient unique match.

This explicitly avoids repeating the historical unique-only shrinkage that missed repeated/fixed objects.

## 5. PC -> Switch evidence hierarchy

For each counterpart claim prefer, in order:

1. same data/control-flow purpose established by Switch disassembly or object structure;
2. callers/callees/data references supporting the same semantic role;
3. value/range behavior matching the PC requirement;
4. actual PC replacement bytes/meaning as reference;
5. runtime behavior only as a later corroborating signal, not the primary locator.

Do not search for x86 signatures in ARM64 code. Do not infer a counterpart merely because constants look similar.

## 6. `NATIVE_EQUIVALENT` evidence rule

No row may be labeled `NATIVE_EQUIVALENT_CANDIDATE` solely because:

- the game currently boots;
- one screen renders correctly;
- no visible bug has been observed;
- a nearby function accepts one relevant byte range;
- a patch experiment had no effect.

A candidate requires concrete Switch code/data evidence implementing the same semantic obligation. `NATIVE_EQUIVALENT_VERIFIED` requires the scope and evidence to be recorded explicitly. Otherwise the item stays `UNSURVEYED`, `PARTIAL_EVIDENCE`, or `UNRESOLVED`.

## 7. Mapping survey requirements

The mapping family must be surveyed as one root-cause family, not two count literals in isolation.

Required outputs:

- physical location and footprint of the Switch 7,494-entry mapping data;
- every lookup/conversion path that references the table or its count;
- all table-base/reference sites semantically corresponding to the PC three-address family;
- all count/limit sites semantically corresponding to the PC two-count family;
- whether any complete 10,036-equivalent mapping already exists elsewhere;
- exact additional-capacity requirement if not;
- placement constraints, without yet selecting or patching a cave.

The survey must not conclude that editing only `0x4303AC` / `0x430624` is sufficient unless the full reference family has first been enumerated.

## 8. Pointer 56 survey requirements

Treat pointer records as a separate first-class family.

For all 56 PC records record:

- PC index / mode / `arg` / original relationship;
- semantic target object/string;
- Switch corresponding object(s) or pointer/reference(s);
- whether the replacement already exists in Switch data;
- whether new string storage is required;
- sharing relationships for the 47 distinct mode-1 pool strings;
- mode-0 relation to the two inline-translated module targets;
- status: found / native-equivalent / unresolved.

Do not reduce the task to searching for 56 PC pointer-slot addresses.

## 9. Helper semantic survey requirements

### Page mapping

Survey every Switch path relevant to converting Korean lead bytes `EB..F8` to font pages `49..62`. Existing evidence around mapped `0x44650C` is input evidence, not automatic completeness proof.

### Byte-validation/copy

Survey the full byte-copy/validation family. Existing evidence that mapped `0x445C60` accepts `A1..DF` is not enough to prove every path is equivalent to PC helper `+0x20`.

Required result:

- enumerate all relevant copy/decode/validation paths;
- determine which path feeds compact fixed-field rendering;
- determine whether accepted single-byte compact data is preserved, transformed, or dropped;
- decide whether equivalent behavior can be achieved in existing ARM64 flow or would require added helper code.

No code is written in the survey.

## 10. Descriptor semantic survey requirements

For each of the 14 PC subpatches, map semantic behavior rather than x86 bytes:

- four `170/150 -> 200` width-related changes;
- two `5 -> 4` argument changes;
- three mapping-address changes;
- two mapping-count changes;
- one `0xFF -> 0xA0` threshold change;
- page-mapper hook semantics;
- byte-validation/copy hook semantics.

PC one-to-one cardinality must not be assumed. W0 already demonstrates that one PC semantic concept may fan out to multiple Switch sites.

## 11. Inline/data-selection survey requirements

The 17,103 PC inline records are the semantic source, but Switch object correspondence is authoritative for placement.

Rules:

- actual PC Korean replacement data is ground truth for text/glyph spelling;
- repeated objects must be handled as objects, not substring matches;
- duplicated fixed fields must not be excluded merely because they are non-unique;
- person name / alias / active-slot selection must be traced before using screen symptoms to infer renderer defects;
- yomi/internal reading data remains separate from visible-row suppression;
- currency format objects remain a structural family, not global single-character replacement.

## 12. Compact `쓰` three-path requirement

Do not start by assuming one cause. Explicitly keep these paths independent until evidence converges:

1. duplicated fixed-field / active name-slot selection;
2. pointer/reference selection;
3. byte-validation/copy path.

For each new finding, state which of the three paths it supports or excludes. Do not use W1 again as a direct `쓰` fix without first establishing that the active source bytes reach the tested render path.

## 13. Space/capacity survey

Space analysis is required as a dedicated output of counterpart survey, separated by axis:

- mapping additional capacity;
- pointer replacement-string capacity;
- helper executable capacity, if any;
- literal in-place descriptor edits;
- inline/fixed-object capacity constraints.

Do not begin by assuming a classic code/data cave is mandatory for every family. Conversely, do not hide the mapping-capacity requirement inside descriptor analysis. State exact bytes/alignment/range constraints after the actual Switch layout is surveyed.

## 14. PCREF1 delivery verification gate

PCREF1 emitted-IPS verification may run in parallel with this static survey. It need not finish before counterpart locations are discovered.

However, before generating/interpreting the first new counterpart-derived runtime diagnostic, PCREF1 delivery uncertainty must be closed. Required verification should include the previously identified emitted coordinates/guard behavior and EOF-collision question recorded by the project.

This prevents a later no-change runtime result from being ambiguous between:

- wrong semantic counterpart; and
- correct counterpart but failed/misdirected IPS delivery.

## 15. Diagnostic-build rule after survey

This survey does not authorize builds. When a later user signal authorizes diagnostics:

- one root-cause family per diagnostic build;
- all proven sites of that same family should be changed together;
- do not mix unrelated hypotheses;
- original-byte guards and emitted-IPS round-trip checks are required;
- actual runtime result must be recorded narrowly to the tested route.

## 16. Required survey deliverables

At survey completion produce:

1. full PC-family -> Switch-site matrix;
2. unresolved/missing counterpart list;
3. native-equivalent claims with concrete evidence;
4. per-axis storage/capacity requirements;
5. rejected hypotheses / negative findings;
6. implementation candidates, clearly marked as proposals only;
7. updated resume gate.

Report the result and STOP. Implementation requires a fresh execution signal.
