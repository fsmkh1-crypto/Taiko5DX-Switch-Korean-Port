# PC Runtime Canonical Closure

Date: 2026-09-11
Status: COMPLETE / STOP

## 1. Purpose

This closure does not introduce a new reverse-engineering phase and does not create new validation IDs. It integrates the already-validated PC runtime findings V001–V061 into one authoritative reference boundary for later Nintendo Switch counterpart work.

Authority order after this closure:

1. `docs/VALIDATION_LEDGER.md` and its phase parts;
2. `docs/PC_RUNTIME_DLL_SPEC.md` as the closed PC runtime specification;
3. PHASE 1–4 detail records for provenance;
4. `docs/PC_RUNTIME_SWITCH_COUNTERPART_MATRIX.md` for Switch-side status only;
5. `docs/SWITCH_COUNTERPART_SURVEY_RULES.md` for the next-stage operating contract;
6. `PROJECT_STATE.md` for the resume gate.

No Switch disassembly, ARM64 implementation, code/data-cave search, IPS generation, diagnostic build, or runtime test was performed in this closure.

## 2. Closure result

The Windows Korean patch runtime is structurally closed at the following layers:

- proxy loading / `DirectInput8Create` initialization and fail-closed transaction framework;
- exact T5K parser grammar and fixed-package bounds;
- 17,103 inline records;
- 10,036-entry mapping storage and five mapping-related code operands;
- 56 pointer records and their mode/arg application engine;
- 158-byte helper with two descriptor-used entries;
- descriptor search/application engine;
- 11 descriptors / 14 subpatches and kind 0–3 generation formulas;
- commit ordering, protections, cache flush and best-effort rollback.

This means the PC reference implementation is closed enough to define what a Switch clean port must compare semantically. It does **not** mean Switch feasibility, address coverage, storage placement, or runtime equivalence is already established.

## 3. Canonical runtime model

The PC patch uses one integrated runtime package.

```text
DirectInput8Create
  -> proxy once
  -> patch once
  -> parse T5K
  -> disk EXE identity
  -> in-memory PE profile
  -> one contiguous private allocation
       ├─ page-aligned prefix region
       │    ├─ mapping 10,036 * 4 = 40,144 bytes (0x9CD0)
       │    └─ pointer replacement pool = 602 bytes (0x25A)
       └─ page-aligned helper region containing 158-byte helper
  -> stage inline records (priority 0)
  -> stage pointer records (priority 1)
  -> stage descriptor-generated code patches (priority 2)
  -> prefix R / helper RX
  -> commit / flush / restore protections
  -> call real DirectInput8Create only if patch-success flag is true
```

The prefix total is `0x9F2A = 40,746` bytes. The mapping table alone is `0x9CD0 = 40,144` bytes. These sizes must not be conflated.

## 4. T5K grammar closure

Canonical pointer wire grammar is:

```text
u32 pc_slot_rva
u32 pc_original_target_rva
u8  mode
u8  reserved[3]
u32 arg
```

The old `<IIII>` / `u32 mode` representation is non-canonical.

Runtime interpretation:

```text
mode 0: replacement destination = EXE/module base + arg
mode 1: replacement destination = private prefix base + arg
```

Observed fixed-resource population:

```text
mode 0 = 5
mode 1 = 51
```

The 51 mode-1 records reference 47 distinct strings in the replacement pool. The five mode-0 records converge on two module-resident targets translated by the inline layer.

## 5. Mapping closure

The PC reference mapping family is not merely a count edit.

```text
original mapping count = 7,494 (0x1D46)
Korean additions       = 2,542
expanded count         = 10,036 (0x2734)
```

The full 10,036-entry table is copied to private runtime storage. Two lookup paths collectively patch:

- three address/table-base operands to the relocated mapping storage; and
- two count operands from 7,494 to 10,036.

Mapping relocation and pointer-record application are separate engines even though both use the same private prefix allocation.

## 6. Descriptor/helper closure

Descriptor search is PC-version-specific machinery: it scans target `.text`, applies a byte-select mask (`0` ignore / nonzero full-byte compare), requires exactly one match, and also requires exact declared-anchor agreement.

This strict PC search policy is **not** a rule that Switch counterpart discovery must also require uniqueness. It is part of the Windows patcher's target-version guard.

Subpatch formulas are canonical:

```text
M = target EXE/module base
P = relocated private prefix base
H = helper base
W = actual write address

kind 0: payload
kind 1: i32(P - W - 4)
kind 2: i32(P - M)
kind 3: E9 || i32(H + arg - W - 5)
```

Kinds 1/2 do not use `arg`; kind 3 uses `arg` as helper-entry offset.

Helper entries:

- `+0x00`: Korean page mapping `EB..F8 -> pages 49..62`; nonmatching input resumes original PC flow at RVA `0x6933D5`.
- `+0x20`: accepted one/two-byte forms are copied/handled directly and continue at RVA `0x6832BC`; other input resumes the original PC path at RVA `0x68328A`. It is not a Boolean validator and fallback is not immediate rejection.

Raw `font_page_limit` behavior is only the compare-threshold change `0xFF -> 0xA0`. A literal font-page-count interpretation is rejected.

## 7. 11 descriptors / 14 subpatches

The fixed resource contains:

```text
descriptors = 11
subpatches  = 14
kind 0/1/2/3 = 9/2/1/2
```

The raw functional groups are:

- `ui_width_1..4`: four literal immediates `170/150 -> 200`;
- `description_font_1..2`: two stack-argument changes `5 -> 4`;
- `mapping_lookup_1/2`: three relocated-table address operands + two `7,494 -> 10,036` counts;
- `runtime_byte_validation`: helper `+0x20` branch;
- `font_page_limit`: threshold `0xFF -> 0xA0`;
- `runtime_page_mapper`: helper `+0x00` branch.

The descriptor names are useful labels. Exact screen/unit/font meanings of `ui_width_*` and `description_font_*` remain contextual gaps without the exact target PC EXE.

## 8. PC implementation machinery vs portable semantic requirements

| PC mechanism | PC implementation detail | Portable semantic requirement |
|---|---|---|
| proxy init | `dinput8.dll`, once guards, Windows APIs | none as a literal mechanism; Switch only needs equivalent game behavior |
| identity guard | EXE basename/size/SHA + PE profile | target-version guarding should exist in the eventual builder, not necessarily in-game |
| private allocation | Windows `VirtualAlloc`, one contiguous allocation | enough storage/addressability for whatever Switch representation is chosen |
| mapping | relocated 10,036-entry table + 3 references + 2 counts | all relevant conversion/lookup paths must access the Korean-complete mapping |
| pointer pool | 602-byte pool plus 51 mode-1 pointer redirects | referenced Korean replacement strings must exist and all required references must target them |
| mode-0 pointers | 5 redirects to 2 existing module targets | equivalent object/reference relationships must be preserved |
| helper `+0x00` | x86-64 trampoline | `EB..F8` Korean leads must resolve to pages 49..62 on every relevant Switch path |
| helper `+0x20` | x86-64 copy/control-flow trampoline | relevant byte-copy/validation paths must preserve the single-byte compact range and valid two-byte behavior |
| descriptor search | x86 signature/mask + exact anchor | not portable; Switch counterparts must be found semantically |
| literal descriptor patches | x86 immediates/stack args | reproduce only where Switch behavior is not already equivalent |
| inline layer | PC RVAs + equal-length preimage/replacement | use actual Switch object correspondence, not PC addresses or uniqueness as a release gate |

## 9. Storage/placement risk — separated by functional axis

The closure does not assert that a code/data cave is the only possible solution. It does establish which families may require new capacity.

### Mapping

To represent the PC-equivalent 10,036-entry mapping, the 2,542 Korean additions must exist somewhere beyond the original 7,494-entry content unless the Switch binary already contains an equivalent complete mapping elsewhere. Existing Switch evidence still shows conversion loops using 7,494 entries. Therefore **mapping-capacity placement is the primary storage risk**, but the exact solution is not selected here.

### Pointer replacement pool

The PC implementation uses 602 bytes of private pool storage. A Switch port may need comparable new storage, or may be able to reuse existing rodata objects / other proven unused storage. Per-record survey is required before deciding.

### Helper code

No conclusion is made that a new ARM64 helper blob is mandatory. One or both PC helper semantics may be reproducible by in-place edits to existing Switch control flow. Extra executable storage is therefore unresolved, not assumed.

### Literal descriptor equivalents

Simple counterpart instruction edits may be in-place and need no new data/code storage. This must be decided per semantic family.

### Inline data

The PC inline wire format is equal-length replacement and does not inherently require a new pool. Switch object correspondence, repeated objects, fixed fields and pointer-owned objects remain separate coverage concerns.

## 10. Switch status must be kept separate from PC completion

PC specification completion and Switch-port completion are different dimensions. `docs/PC_RUNTIME_SWITCH_COUNTERPART_MATRIX.md` therefore tracks them separately.

`NATIVE POSSIBLE` or any equivalent "patch may be unnecessary" status is forbidden without concrete Switch-side code/data evidence. If no evidence exists, the status stays `UNSURVEYED`. Existing partial evidence is labeled `PARTIAL_EVIDENCE`, not treated as native equivalence.

## 11. Compact `쓰` symptom — unresolved three-path model

The missing `쓰` observation must not be assigned to one cause during closure. Three paths remain unresolved and may interact:

1. **data selection** — duplicated fixed fields / actual active name or alias slot selection;
2. **pointer/reference selection** — whether the rendered object/reference follows a pointer path not covered by historical selection;
3. **byte-validation/copy path** — whether a Switch path distinct from the already-observed per-character decoder drops or transforms compact single-byte data.

W1 invalidated the direct claim that mapped `0x44D9D0` alone causes the missing `쓰`. The historical unique-only selector also missed duplicated `松平元康` fields. No single remaining path is promoted to root cause by this closure.

## 12. PCREF1 and CWTDAT separation

PCREF1 emitted-IPS verification is logically independent of counterpart discovery. It may run in parallel with the later survey, but it must be closed **before a new counterpart-derived build is interpreted at runtime**, so a no-change result is not ambiguously attributed to either wrong counterpart selection or patch-delivery failure.

CWTDAT compatibility is also a separate data-port axis. Stage-1 direct copy proves that the Windows DLL did not execute under Eden; it does not prove PC/Switch CWTDAT structural equivalence. Do not infer compatibility from that control alone.

## 13. Audit of pre-closure `PC_RUNTIME_DLL_SPEC.md`

The pre-closure SPEC was systematically compared against PHASE 1–4 authority. Key corrections incorporated into the closed SPEC are:

- **CORRECTED:** pointer wire record is `u8 mode + reserved[3] + u32 arg`, not four u32 fields.
- **CORRECTED:** `arg` is mode-dependent; `string_offset_or_target` is not a canonical universal field name.
- **CORRECTED:** prefix/helper are prepared inside one contiguous private allocation, not two independent VirtualAlloc operations.
- **CORRECTED:** helper `+0x20` fallback resumes original processing at `0x68328A`; it is not `continue_original_invalid_path` as a semantic conclusion.
- **CORRECTED:** `font_page_limit` is raw threshold `0xFF -> 0xA0`, not a proven literal page-count edit.
- **CONFIRMED:** prefix split is 40,144-byte mapping + 602-byte pool = 40,746 bytes total.
- **CONFIRMED:** mapping relocation modifies three address operands plus two counts.
- **CONFIRMED:** 56 pointer records are a distinct first-class layer.
- **CONFIRMED:** descriptor kinds 0–3 and helper entry offsets.
- **CONFIRMED:** exact PC EXE is not required to close the DLL-generated mechanics, but remains required for whole-program caller/UI naming and target-process runtime confirmation.

No contradictory PHASE 1–4 canonical fact remains intentionally preserved in the closed `PC_RUNTIME_DLL_SPEC.md`.

## 14. Validation accounting

Closure adds no new factual validation claim and therefore assigns no V062+ IDs. The factual authority remains V001–V061. This document is an integration/audit product whose claims must trace to those existing ledger entries and phase records.

The PHASE 4 auxiliary JSON/probe/raw-evidence ZIP were not available at canonical-import time. Their absence remains a provenance limitation for exact raw helper-fixup offsets/signature bytes not reproduced in the imported PHASE 4 record. Do not fabricate them.

## 15. Next stage

After a fresh user execution signal, the next stage is **Switch Functional Counterpart Survey**.

It must use the closed PC semantic families as the checklist, enumerate all Switch locations with equivalent meaning, never use uniqueness as a coverage gate, and leave unfound items explicitly unresolved. No implementation/build authorization is implied by this closure.

STOP.
