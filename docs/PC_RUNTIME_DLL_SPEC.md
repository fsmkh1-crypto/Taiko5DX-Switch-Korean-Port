# PC RUNTIME DLL SPEC — canonical closure edition

Date: 2026-09-11
Status: CLOSED PC REFERENCE / STOP

This is the authoritative closed specification of the Windows Korean patch `dinput8.dll` used by `Taiko5DX_Korean_Patcher_v1.02`. It incorporates PHASE 1–4 and supersedes stale pre-closure wording in older revisions of this file. Factual authority remains the validation ledger V001–V061 and the PHASE detail records.

This document describes the PC reference implementation. It does not authorize a Switch build and does not assert that Windows implementation mechanisms must be copied literally on Switch.

## 1. Fixed input identity

- PC patch ZIP SHA-256: `df1b62de95e992369e9686c9731d814e7a7e4634888f610430635429e24f7cec`
- embedded `dinput8.dll`: 836,096 bytes
- DLL SHA-256: `ffe7e9da8e00c96bec631b45a3e9c4d3f314551623351f3e7024e0318913c6b7`
- `RT_RCDATA/101` (`T5K121R`) SHA-256: `5c6f4eba8c6f0516365e4518f27e9d8c840aead463b5a2938dd1e08b99726d29`
- exact target EXE: Steam 1.2.1.0 build 9163702, 18,685,960 bytes, SHA-256 `10c69bab50d29baf6311360cafbf7383716a126a6484d209f5e299e12ab565a2`
- the supplied mismatched PC EXE is barred from target-RVA neighborhood/XREF claims.

## 2. Historical direct-copy control

A Stage-1 Eden control copied the PC data payload, including PC `CWTDAT_JP.TR5`, and placed the unmodified Windows `dinput8.dll` in the add-on. The game booted but Korean remained garbled/symbol-like and the Windows DLL produced no visible effect.

The only safe interpretation is that direct placement does not make the Windows proxy runtime execute under Switch/Eden. It does **not** prove PC/Switch CWTDAT structural compatibility and does not prove the DLL executed and failed internally.

## 3. Proxy initialization and failure model

The DLL is an AMD64 PE32+ `dinput8.dll` proxy.

- `DllMain` only stores module state / disables thread-library callbacks; it does not apply the Korean patch.
- Korean patch initialization occurs on `DirectInput8Create` through a proxy once guard and a separate patch once guard.
- a distinct patch-success flag must be true before the real `DirectInput8Create` is called.
- the other five exports do not initialize the Korean patch.
- normal patch failures are fail-closed: log, optional MessageBox unless `TAIKO5DX_KO_NOUI`, then process termination with `0xC1`.
- NOUI suppresses the dialog only; it does not bypass validation or termination.

## 4. T5K header and parser grammar

The resource header is exactly `0x48` bytes:

```text
+0x00 char magic[8]            = "T5K121R\0"
+0x08 u32 version              = 1
+0x0C u32 inline_count         = 17,103
+0x10 u32 pointer_count        = 56
+0x14 u32 descriptor_count     = 11
+0x18 u32 prefix_len           = 0x9F2A
+0x1C u32 helper_len           = 0x9E
+0x20 u64 target_exe_size
+0x28 u8 target_exe_sha256[32]
+0x48 payload
```

There is no mapping-count header field. Target EXE size/hash are preserved by the parser and validated later by the identity path rather than hard-coded as parser acceptance constants.

Top-level fixed-resource consumption:

```text
0x00000..0x00047  header
0x00048..0x09F71  prefix                0x9F2A
0x09F72..0x0A00F  helper                0x009E
0x0A010..0x951BF  inline records        17,103
0x951C0..0x9553F  pointer records       56 * 0x10
0x95540..0x95D34  descriptors           11
0x95D35            EOF
```

Trailing bytes are rejected.

### Inline record

```text
u32 pc_rva
u32 length
u8 original[length]
u8 replacement[length]
```

`length` is nonzero; both payloads must fit; fixed-resource observed lengths are 1..445, not a parser maximum.

### Pointer record — canonical wire grammar

```text
u32 pc_slot_rva
u32 pc_original_target_rva
u8  mode
u8  reserved[3]
u32 arg
```

Parser enforces `mode <= 1`. The three reserved bytes are skipped; no zero-value validation was established.

**Superseded:** older revisions of this file represented the record as four u32 fields and named the last field `string_offset_or_target`. That is not canonical.

### Descriptor

```text
u32 anchor_rva
u32 signature_len
u32 patch_count
u32 name_len
u8  name[name_len]
u8  signature[signature_len]
u8  mask[signature_len]
subpatch subpatches[patch_count]
```

### Subpatch

```text
u32 offset
u32 preimage_len
u8  kind
u8  reserved[3]
u32 arg
u32 payload_len
u8  preimage[preimage_len]
u8  payload[payload_len]
```

Parser rules include `kind <= 3`, nonzero preimage, in-signature bounds, kind-0 `payload_len == preimage_len`, and kinds 1–3 `payload_len == 0`.

The fixed resource contains 14 total subpatches with kind distribution `9/2/1/2`. Fourteen is not a parser hard denominator; PHASE 4 established a separate staging-time fixed-package total check.

## 5. Private storage preparation — corrected

After T5K parse and target identity/profile validation, the DLL prepares **one contiguous private allocation**. Prefix and helper sizes are separately page-rounded and combined into one allocation. They are not two independent mandatory `VirtualAlloc` operations.

The resource prefix and helper are copied into their respective regions. Helper control-transfer operands are fixed up before staging completes. On successful staging, the prefix region is made read-only and helper region execute-read before commit.

Successful runtime storage remains allocated because patched game code/pointers refer to it.

## 6. Runtime prefix layout

The semantic prefix is:

```text
prefix +0x0000..+0x9CCF   mapping table   10,036 * 4 = 0x9CD0 = 40,144 bytes
prefix +0x9CD0..+0x9F29   pointer pool                  0x25A =    602 bytes
prefix total                                               0x9F2A = 40,746 bytes
```

Do not call the 40,746-byte prefix a 40,746-byte mapping table. Mapping alone is 40,144 bytes.

The mapping consists of:

- original mappings: 7,494 (`0x1D46`)
- Korean additions: 2,542
- total: 10,036 (`0x2734`)

## 7. Mapping relocation semantics

The PC patch does not merely increase a count. It copies the full 10,036-entry mapping to private runtime storage and modifies two lookup paths.

Across those paths it changes:

- three table/address operands -> relocated mapping storage;
- two count operands `7,494 -> 10,036`.

`mapping_lookup_1` contains one relocated reference + one count change.

`mapping_lookup_2` contains two relocated references + one count change.

Mapping relocation and pointer application are separate engines sharing the same prefix allocation.

## 8. Pointer 56 application engine

Every pointer record stages an 8-byte absolute pointer write to the slot identified by `pc_slot_rva`.

Runtime replacement-address calculation is mode-dependent:

```text
mode 0: destination = EXE/module base + arg
mode 1: destination = private prefix base + arg
```

Observed population:

- mode 0: 5 records
- mode 1: 51 records

Mode 0's five records converge on two module-resident targets that are also translated by the inline layer.

Mode 1's 51 records reference 47 distinct replacement strings in the private prefix pool.

`pc_original_target_rva` belongs to the original/preimage relationship; it is not part of the replacement-address formula above.

## 9. Descriptor search/application engine

For each descriptor the PC engine searches the target EXE `.text` region using the signature and mask.

Mask semantics:

```text
mask[i] == 0x00  -> ignore byte i
mask[i] != 0x00  -> compare full signature byte i
```

Success requires:

1. exactly one masked match in `.text`; and
2. that match to equal the descriptor's declared anchor expectation.

Zero matches, multiple matches, or a unique match at a different address fail the descriptor/application path.

This is Windows target-version guard machinery. It must not be copied as a Switch `unique match` discovery rule.

## 10. Subpatch generation formulas

Let:

```text
M = EXE/module base
P = private prefix base
H = helper base
W = actual write address
```

Canonical generation:

```text
kind 0: replacement = payload
kind 1: replacement = i32(P - W - 4)
kind 2: replacement = i32(P - M)
kind 3: replacement = E9 || i32(H + arg - W - 5)
```

Kinds 1 and 2 do not use `arg`. Kind 3 uses `arg` as helper-entry offset.

## 11. Descriptor census

| Descriptor | Anchor RVA | Subpatches | Confirmed raw behavior |
|---|---:|---:|---|
| `ui_width_1` | `0x137A5B` | 1 | immediate `170 -> 200` |
| `ui_width_2` | `0x137CDB` | 1 | immediate `170 -> 200` |
| `ui_width_3` | `0x137EAE` | 1 | immediate `170 -> 200` |
| `ui_width_4` | `0x13CBDC` | 1 | immediate `150 -> 200` |
| `description_font_1` | `0x3EE12F` | 1 | stack argument `5 -> 4` |
| `description_font_2` | `0x3EE196` | 1 | stack argument `5 -> 4` |
| `mapping_lookup_1` | `0x662963` | 2 | relocated table reference + `7,494 -> 10,036` |
| `mapping_lookup_2` | `0x662B60` | 3 | two relocated table references + `7,494 -> 10,036` |
| `runtime_byte_validation` | `0x68327A` | 1 | helper `+0x20` JMP |
| `font_page_limit` | `0x693136` | 1 | compare threshold `0xFF -> 0xA0` |
| `runtime_page_mapper` | `0x6933D0` | 1 | helper `+0x00` JMP |

Successful write RVAs and kind assignments are recorded in `docs/PC_RUNTIME_PHASE4_HELPER_DESCRIPTOR_SPEC.md`.

The exact screen/unit/font meanings of `ui_width_*` and `description_font_*` remain inferential without the exact target PC EXE. The raw changes above are the canonical facts.

The actual descriptor names are `mapping_lookup_1` / `mapping_lookup_2`; `mapping_lookup_1A/2A` were cross-boundary substring false positives from an older convenience parser.

## 12. Runtime helper

The helper is 158 bytes (`0x9E`) with two descriptor-used logical entries. PHASE 4 counted 42 reachable instructions plus 4 bytes of unreachable alignment/padding and four control-transfer targets fixed up after allocation.

### `helper +0x00` — page mapper

For Korean lead bytes `0xEB..0xF8`, it produces page indices `49..62` in `EAX` and returns. Otherwise it reproduces displaced original behavior and resumes target EXE flow at RVA `0x6933D5`.

Conceptually:

```text
if 0xEB <= lead <= 0xF8:
    EAX = (lead - 0xEB) + 49
    RET
else:
    displaced original operation
    JMP 0x6933D5
```

### `helper +0x20` — byte-validation/copy control-flow hook

Inputs reported by PHASE 4 include current byte in `CL`, next-input location through `RBX`, and output destination through `RDI`.

It directly handles accepted one-byte and valid two-byte forms, copies/emits them, and continues at EXE RVA `0x6832BC`.

Accepted direct ranges include:

```text
single byte: 0xA1..0xDF
lead:        0x81..0x9F or 0xE0..0xFC
trail:       0x40..0x7E or 0x80..0xFC
```

Other inputs do **not** immediately fail. The helper reproduces displaced original `LEA/CMP` behavior and resumes original processing at EXE RVA `0x68328A`.

Therefore:

- it is not a Boolean validator API;
- fallback is not equivalent to immediate invalid-input rejection;
- the old phrase `continue_original_invalid_path` is superseded as a semantic conclusion.

## 13. Staging / commit / rollback

The PC patch stages all writes before commit. Common staging requires exact preimage equality and equal nonzero write lengths; overlap is rejected. It does not silently skip mismatched records.

Commit priorities:

```text
inline   = 0
pointer  = 1
code     = 2
```

Commit makes touched pages writable, applies records in priority order, flushes instruction cache, and restores protections.

Rollback exists for failures but is best-effort. Some rollback API return values are not checked, so this is not a guarantee of fully atomic restoration.

## 14. Integrated PC operation family

The PC runtime reference comprises all of these layers:

1. parser / target identity / profile validation;
2. one contiguous private prefix+helper allocation;
3. mapping storage and lookup relocation;
4. pointer 56 redirection;
5. inline 17,103 replacement layer;
6. descriptor/helper code layer;
7. guarded transaction commit.

None of mapping, pointer, helper or descriptor layers should be silently collapsed into the historical 5,519 unique inline subset.

## 15. PC implementation vs Switch semantic obligation

The Switch clean port is required to reproduce **meaning**, not Windows mechanics.

Examples:

- Windows `VirtualAlloc` is not portable; Switch only needs a safe representation with enough addressability/capacity.
- x86 descriptor signature search is not portable; Switch counterparts must be found by semantic code/data analysis.
- the 158-byte x86 helper need not become a 158-byte ARM64 helper if existing Switch functions can be edited in place to provide equivalent behavior.
- the mapping requirement is the complete 10,036-entry behavior and all relevant consumers, not a literal copy of the PC allocation routine.
- pointer mode-1 semantics require replacement strings/references to exist; they do not mandate a 602-byte contiguous Switch pool if another proven-safe representation is equivalent.

## 16. Existing Switch evidence boundary

Pre-closure evidence already shows:

- Switch conversion loops still use 7,494 mapping entries, so full mapping expansion remains required unless later survey finds another complete native table/path.
- mapped `0x44650C` has an established page-mapper relation compatible with the PC `+0x00` semantic family.
- mapped `0x445C60` accepts `0xA1..0xDF` in one per-character path, but that is not proof that all byte-copy/validation paths are natively equivalent to helper `+0x20`.
- W0/W1 experiments are partial threshold/width evidence, not a complete descriptor counterpart mapping.
- duplicated `松平元康` fixed fields were missed by the historical unique-only selector, so missing `쓰` is not established as a renderer-only defect.

These are starting facts for the next survey, not new closure findings.

## 17. Compact `쓰` unresolved model

Keep three paths separate until evidence converges:

1. data selection / duplicated fixed field / active alias-name slot;
2. pointer/reference selection;
3. byte-validation/copy path.

No single path is the canonical root cause yet. W1 only invalidated the direct `0x44D9D0`-alone hypothesis.

## 18. Exact PC EXE limits

The exact target EXE is not required to close the DLL-generated mechanics above. It remains useful/required for:

- complete PC whole-program XREF/caller graph;
- exact containing-function names and C++ semantics;
- exact screen/UI role of width/font descriptors;
- actual target-process runtime execution confirmation.

Do not use the mismatched supplied EXE for those claims.

## 19. Closure audit / superseded wording

This closure specifically corrects the following older SPEC wording:

- four-u32 pointer grammar -> canonical `u8 mode + reserved[3] + u32 arg`;
- universal `string_offset_or_target` -> mode-dependent `arg`;
- separate helper allocation wording -> one contiguous prefix/helper allocation;
- `continue_original_invalid_path` -> original-processing continuation at `0x68328A`;
- `font_page_limit` as page-count concept -> raw compare threshold only;
- PC descriptor uniqueness/anchor rule -> Windows validation machinery, not Switch discovery policy.

## 20. Next-stage contract

Use:

- `docs/PC_RUNTIME_CANONICAL_CLOSURE.md`
- `docs/PC_RUNTIME_SWITCH_COUNTERPART_MATRIX.md`
- `docs/SWITCH_COUNTERPART_SURVEY_RULES.md`

for the next authorized Switch Functional Counterpart Survey.

No Switch survey, ARM64 edit, IPS, build or runtime test is authorized by this file itself.
