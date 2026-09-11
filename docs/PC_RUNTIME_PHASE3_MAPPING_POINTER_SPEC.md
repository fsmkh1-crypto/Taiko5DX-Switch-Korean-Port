# PC DLL PHASE 3 — mapping and pointer runtime semantics

Date: 2026-09-11
Status: COMPLETE / STOP

## 1. Scope and authority

This phase analyzes only the PC Korean patch runtime behavior for:

1. the 10,036-entry mapping storage and lookup relocation; and
2. the 56 pointer records and their mode/arg application engine.

It does not analyze the 158-byte helper instruction semantics, generic runtime-descriptor kind semantics, Switch counterparts, ARM64, IPS, or builds.

Canonical prior facts from PHASE 1 and PHASE 2 are reused without revalidation. In particular, the pointer wire record remains:

```text
u32 pc_slot_rva
u32 pc_original_target_rva
u8  mode
u8  reserved[3]
u32 arg
```

The older convenience interpretation of the third field as a full u32 `mode` is not canonical.

Fixed inputs:

- embedded `dinput8.dll` SHA-256 `ffe7e9da8e00c96bec631b45a3e9c4d3f314551623351f3e7024e0318913c6b7`
- `RT_RCDATA/101` SHA-256 `5c6f4eba8c6f0516365e4518f27e9d8c840aead463b5a2938dd1e08b99726d29`
- exact target PC EXE identity remains Steam 1.2.1.0 build 9163702, 18,685,960 bytes, SHA-256 `10c69bab50d29baf6311360cafbf7383716a126a6484d209f5e299e12ab565a2`
- that exact EXE was not available for whole-program XREF/call-site naming in this phase

## 2. Prefix runtime layout

The T5K prefix is `0x9F2A` bytes and is copied into the PC patch's private runtime allocation before patch commit.

Its established semantic split is:

```text
prefix + 0x0000 .. +0x9CCF   mapping table   10,036 * 4 = 0x9CD0 bytes
prefix + 0x9CD0 .. +0x9F29   pointer pool    0x25A = 602 bytes
```

Equivalent fixed-resource coordinates are:

```text
RCDATA 0x00048 .. 0x09D17   mapping table
RCDATA 0x09D18 .. 0x09F71   pointer replacement pool
```

Therefore the 10,036-entry mapping is not builder-only metadata. It is copied into runtime storage used by the patched PC process.

The 10,036 entries consist of the established 7,494 original mappings plus 2,542 Korean additions. PHASE 3 does not alter those already-verified counts.

## 3. Mapping lookup relocation/application

Two mapping-lookup patch paths together alter five mapping-related operands:

- three address/table-base operands are redirected to the relocated private mapping storage;
- two mapping-count limits are changed from 7,494 (`0x1D46`) to 10,036 (`0x2734`).

This establishes that the PC patch does not merely change a loop bound. It relocates the expanded mapping table and changes the lookup paths so they use the relocated storage and the expanded count.

The three address changes comprise the mapping-table reference family; the two count changes are the corresponding search/iteration limits. The exact whole-program call graph and human-readable game function names remain unassigned without the exact target EXE.

The mapping relocation path is separate from the 56 pointer-record engine. The pointer records do not themselves relocate the 10,036-entry mapping table.

## 4. Pointer-record application engine

All 56 pointer records were surveyed as one mechanism before assigning mode semantics.

Population:

```text
mode 0 = 5 records
mode 1 = 51 records
```

For each record, the engine stages an 8-byte absolute pointer write to the slot identified by `pc_slot_rva`.

The destination calculation is mode-dependent:

```text
mode 0: destination = EXE/module base + arg
mode 1: destination = private prefix base + arg
```

Thus `arg` is not one universal semantic field independent of mode. It is interpreted against a different base according to `mode`.

`pc_slot_rva` identifies the target pointer slot in the PC module. `pc_original_target_rva` identifies the record's original PC target relationship and belongs to the original/preimage side of the pointer patch rather than the replacement-address calculation above.

The staged pointer write enters the PHASE-1 transaction as the pointer patch class, whose commit priority is 1.

## 5. Mode 0 — five records

All five mode-0 records resolve the replacement destination inside the existing PC module:

```text
destination = EXE/module base + arg
```

The five records point to only two underlying targets. Those two targets are themselves translated by the inline patch layer before final commit.

Therefore mode 0 is not a pointer into the private replacement-string pool. It is a redirection to an existing module-resident target whose contents are handled by the normal inline layer.

This also demonstrates an explicit cross-layer relationship: a pointer record may redirect a slot to data whose translation is supplied by an inline record.

## 6. Mode 1 — 51 records

All 51 mode-1 records resolve into the copied T5K prefix:

```text
destination = private prefix base + arg
```

Their targets lie in the prefix's replacement/pool area rather than being calculated from the PC EXE base.

The 51 mode-1 records reference 47 distinct replacement strings, so several records intentionally share pool targets.

This is a first-class runtime string/reference layer: it handles references that are not represented solely as same-length in-place inline replacements.

## 7. Mapping/pointer relationship

The PHASE 3 data flow is:

```text
T5K prefix
  ├─ mapping[10,036]               +0x0000 .. +0x9CCF
  └─ pointer replacement pool      +0x9CD0 .. +0x9F29
          │
          ▼
private runtime prefix allocation
  ├─ mapping base
  └─ pool base
          │
          ├──────── mapping lookup relocation
          │           ├─ 3 table/address operands -> relocated mapping
          │           └─ 2 count operands 7,494 -> 10,036
          │
          └──────── pointer engine
                      ├─ mode 0 (5): EXE base + arg
                      └─ mode 1 (51): prefix base + arg
                                  │
                                  ▼
                             8-byte pointer slots
```

The mechanisms share the same private prefix allocation but are not the same application engine. In particular, the 56 pointer records do not perform the mapping-table relocation.

## 8. Confirmed facts

- The full 10,036 mapping table is runtime data copied into private storage.
- The semantic prefix split is 40,144-byte mapping table + 602-byte pointer pool.
- Mapping lookup relocation changes three table/address operands and two count limits.
- Both count limits expand 7,494 to 10,036.
- All 56 pointer records were included in the mode analysis.
- Mode 0 has 5 records and computes `EXE base + arg`.
- Mode 1 has 51 records and computes `prefix base + arg`.
- Pointer writes are 8-byte absolute addresses.
- The five mode-0 records converge on two module-resident targets that are also translated by inline patches.
- The 51 mode-1 records share 47 distinct private-prefix replacement strings.
- Pointer-record application and mapping-table relocation are separate runtime mechanisms.

## 9. Likely but not fully named

The pointer slots span multiple string/reference tables or related registration structures, but exact table/function names and their complete callers are not assigned without the exact target EXE.

This limitation does not weaken the established address-calculation and mode semantics above.

## 10. Unresolved

Without the exact target PC EXE, this phase does not claim:

- a complete whole-program XREF graph for every mapping reference;
- exact runtime virtual addresses after ASLR;
- human-readable UI/screen role for every one of the 56 pointer slots;
- exact names of all containing PC functions/tables.

Those are context/naming gaps, not gaps in the mode/base calculation established by the DLL/T5K application logic.

## 11. Rejected/corrected interpretations

- Rejected: the 10,036 mapping entries are builder-only conversion metadata.
- Rejected: the 56 pointer records directly perform mapping-table relocation.
- Rejected: a search/signature anchor can be treated as the actual runtime EXE address without the target context and relocation/application step.
- Corrected: pointer runtime semantics must be applied to the PHASE-2 canonical wire grammar (`u8 mode + reserved[3] + u32 arg`), not the older `<IIII>` convenience interpretation.

## 12. Impact surface

PHASE 3 establishes one connected PC runtime family spanning:

- relocated 10,036-entry mapping storage;
- three mapping-table/address references;
- two expanded mapping-count limits;
- the 602-byte pointer replacement pool;
- all 56 target pointer slots;
- two module-resident mode-0 targets tied to inline translation;
- 47 distinct mode-1 replacement strings shared by 51 pointer records.

A later clean-port comparison must therefore account for mapping storage/reference behavior and pointer redirection behavior separately; neither may be silently collapsed into the 158-byte helper.

## 13. PHASE 4 handoff

PHASE 4 remains limited to the deferred PC runtime code layer, including the 158-byte helper and runtime-descriptor/subpatch semantics.

This PHASE 3 record does not authorize or begin PHASE 4, Switch counterpart work, ARM64, IPS, code-cave design, or builds.

STOP.
