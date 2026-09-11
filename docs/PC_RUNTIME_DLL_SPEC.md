# PC RUNTIME DLL SPEC

Canonical static-analysis record for the Windows Korean patch `dinput8.dll` used by `Taiko5DX_Korean_Patcher_v1.02`.

This document describes what the PC patch actually does at runtime. It is a reference specification for later Switch-equivalent work. It does not authorize or contain a Switch build.

## 1. Fixed input identity

- PC patch ZIP SHA-256: `df1b62de95e992369e9686c9731d814e7a7e4634888f610430635429e24f7cec`
- embedded `dinput8.dll`: 836,096 bytes
- `dinput8.dll` SHA-256: `ffe7e9da8e00c96bec631b45a3e9c4d3f314551623351f3e7024e0318913c6b7`
- `RT_RCDATA/101` (`T5K121R`) SHA-256: `5c6f4eba8c6f0516365e4518f27e9d8c840aead463b5a2938dd1e08b99726d29`
- exact T5K target PC EXE: Steam 1.2.1.0 build 9163702, 18,685,960 bytes, SHA-256 `10c69bab50d29baf6311360cafbf7383716a126a6484d209f5e299e12ab565a2`
- the currently supplied Drive PC EXE is not the exact target and remains barred from PC-RVA neighborhood/XREF claims.

## 2. Stage-1 direct-copy runtime result

A pure PC-payload control was runtime-tested in Eden:

- all 208 embedded `data/` files copied byte-for-byte to Switch `romfs/`;
- PC `CWTDAT_JP.TR5` included wholesale;
- original PC `dinput8.dll` included byte-for-byte at add-on root;
- no Switch `exefs` patch, no ARM64 patch, no IPS.

Result: game boots and proceeds, but Korean text renders as the same garbled/symbol-like output observed with the data-only control. Adding the unmodified Windows `dinput8.dll` produced no visible runtime effect.

Interpretation: direct file placement does not cause the Windows proxy DLL runtime to execute under Switch/Eden. Do not describe this as proof that the DLL executed and failed internally.

## 3. Proxy-DLL initialization model

The DLL is a Windows `dinput8.dll` proxy. `DllMain` does not apply the Korean patch. It stores module state / disables thread-library callbacks; the patch initialization is reached through the proxy export path, centered on `DirectInput8Create`.

Logical flow:

```text
DirectInput8Create
  -> load/resolve original Windows dinput8 exports
  -> initialize Korean runtime patch
  -> call real DirectInput8Create only after patch initialization succeeds
```

The patching path is fail-closed: validation/patch failures lead to an error path rather than silently running a partial patch.

## 4. Runtime application sequence

Static control-flow reconstruction establishes the following integrated operation family:

1. load `RT_RCDATA/101` and validate `T5K121R` structure;
2. validate target EXE identity/profile;
3. allocate runtime storage for the expanded mapping table plus pointer replacement string pool;
4. copy the T5K prefix into that runtime storage;
5. allocate/install the 158-byte runtime helper and fix helper-relative control transfers;
6. stage all 17,103 inline replacements;
7. stage all 56 pointer records;
8. parse/apply 11 runtime descriptors containing 14 actual code sub-patches;
9. assign final memory protection for mapping/helper regions;
10. commit the patch transaction, flush instruction cache, and restore protections.

The important architectural conclusion is that the PC patch treats inline, pointer, mapping, helper and runtime-descriptor work as one integrated runtime patch, not as optional independent layers.

## 5. `T5K121R` layout

```text
resource size                  613,685 (0x95D35)
header                         0x0000..0x0047
mapping table                  0x0048..0x9D17   (10,036 x 4)
pointer replacement strings    0x9D18..0x9F71   (602 bytes)
runtime helper blob            0x9F72..0xA00F   (158 bytes)
inline patch records            0xA010..0x951BF  (17,103)
pointer patch records           0x951C0..0x9553F (56 x 16)
runtime descriptors             0x95540..end      (11)
```

The runtime prefix copied to newly allocated memory is `0x9F2A` bytes = 40,746 bytes: 40,144 bytes of mapping entries plus the 602-byte pointer string pool.

## 6. Mapping expansion semantics

PC mapping content:

- original mappings: 7,494 (`0x1D46`)
- Korean additions: 2,542
- expanded total: 10,036 (`0x2734`)

The PC patch does not merely alter a loop count. It relocates the full 10,036-entry mapping into runtime storage and redirects lookup code to the relocated table.

`mapping_lookup_1` performs two sub-patches:

- replace a RIP-relative mapping-table reference with the relocated table;
- replace `0x1D46` with `0x2734`.

`mapping_lookup_2` performs three sub-patches:

- replace another RIP-relative mapping-table reference;
- replace `0x1D46` with `0x2734`;
- replace an additional module-base-relative table reference.

Therefore any Switch equivalent must survey table-base references as well as the two known loop counts; changing only `0x4303AC` and `0x430624` is not established as sufficient.

## 7. Pointer-record engine

56 pointer records use the established format:

```text
u32 pc_slot_rva
u32 pc_original_target_rva
u32 mode
u32 string_offset_or_target
```

Observed mode population:

- mode 1: 51 records
- mode 0: 5 records

Mode 1 redirects a PC pointer slot from its original EXE string to a Korean replacement string inside the newly allocated T5K prefix/string-pool block.

Mode 0 redirects to another existing target rather than to the replacement string pool.

The 56 records are a first-class patch layer for strings/references that cannot be represented solely as same-length inline replacements.

## 8. Runtime descriptor binary layout

Each descriptor is:

```text
u32 anchor_rva
u32 signature_len
u32 patch_count
u32 name_len
name[name_len]
signature[signature_len]
mask[signature_len]
patch[patch_count]
```

Each sub-patch is:

```text
u32 offset
u32 preimage_len
u8  kind
u8  reserved[3]
u32 arg
u32 payload_len
preimage[preimage_len]
payload[payload_len]
```

Patch kinds:

- kind 0: literal byte replacement;
- kind 1: RIP-relative displacement targeting relocated mapping storage;
- kind 2: module-base-relative mapping-table displacement;
- kind 3: five-byte relative JMP to the runtime helper.

The 11 descriptors contain exactly 14 sub-patches in total.

## 9. Correct descriptor names and sub-patches

The actual descriptor names are `mapping_lookup_1` and `mapping_lookup_2`, not `mapping_lookup_1A` / `mapping_lookup_2A`. The prior parser accepted the latter only because byte `0x41` immediately following the name produced a cross-boundary substring false positive. Future parsers must validate descriptor names structurally.

| Descriptor | PC anchor RVA | Sub-patches | Confirmed PC behavior |
|---|---:|---:|---|
| `ui_width_1` | `0x137A5B` | 1 | immediate `0xAA -> 0xC8` (170 -> 200) |
| `ui_width_2` | `0x137CDB` | 1 | immediate `0xAA -> 0xC8` |
| `ui_width_3` | `0x137EAE` | 1 | immediate `0xAA -> 0xC8` |
| `ui_width_4` | `0x13CBDC` | 1 | immediate `0x96 -> 0xC8` (150 -> 200) |
| `description_font_1` | `0x3EE12F` | 1 | immediate `0x05 -> 0x04` |
| `description_font_2` | `0x3EE196` | 1 | immediate `0x05 -> 0x04` |
| `mapping_lookup_1` | `0x662963` | 2 | relocated table reference + 7,494 -> 10,036 |
| `mapping_lookup_2` | `0x662B60` | 3 | relocated table refs + 7,494 -> 10,036 |
| `runtime_byte_validation` | `0x68327A` | 1 | JMP to helper entry `+0x20` |
| `font_page_limit` | `0x693136` | 1 | immediate `0xFF -> 0xA0` |
| `runtime_page_mapper` | `0x6933D0` | 1 | JMP to helper entry `+0x00` |

The exact semantic UI meaning of the `ui_width_*` and `description_font_*` call sites still benefits from the exact target PC EXE; the immediate changes themselves are directly established from the DLL/T5K resource.

## 10. Runtime helper: 158-byte executable code

The helper blob is executable x86-64 code and contains at least two logical entries used by descriptors.

### Entry `+0x00`: Korean font-page mapper

Logical behavior:

```c
lead = code >> 8;
if (lead >= 0xEB && lead <= 0xF8)
    return (lead - 0xEB) + 49;
else
    continue_original_path;
```

Thus normal Korean two-byte lead bytes `EB..F8` map to font pages 49..62. This agrees with the already-established Switch page-mapper requirement.

### Entry `+0x20`: byte-validation hook

Logical behavior:

```c
if (0xA1 <= ch && ch <= 0xDF) {
    emit_one_byte(ch);
    success;
}

if ((0x81 <= ch && ch <= 0x9F) || (0xE0 <= ch && ch <= 0xFC)) {
    trail = next_byte;
    if ((0x40 <= trail && trail <= 0x7E) ||
        (0x80 <= trail && trail <= 0xFC)) {
        emit_two_bytes(ch, trail);
        success;
    }
}

continue_original_invalid_path;
```

This proves that the PC patch explicitly hooks a validation/copy path so `A1..DF` is accepted as a valid one-byte game-code range in addition to the normal two-byte ranges.

## 11. Relation to established Switch observations

- Switch `GetFontTexIndex` page-mapper work around mapped `0x44650C` is semantically consistent with the PC `runtime_page_mapper` helper.
- Switch per-character decoding around `0x445C60` already accepts `A1..DF` as one-byte values, but the PC DLL shows that a separate byte-validation path also required hooking on Windows. Therefore per-character decode alone is insufficient evidence that all Switch paths already implement the PC byte-validation semantics.
- The existing W0/W1 width experiments are not a full equivalent of the PC integrated runtime package.
- Mapping relocation/reference handling and all 56 pointer records remain mandatory comparison targets before claiming a PC-equivalent clean port.

## 12. Exact PC EXE requirement — corrected interpretation

The exact Steam build 9163702 EXE remains highly valuable for PC neighborhood/function semantics and especially for identifying the exact UI roles of width/description-font descriptors.

However, it is not an absolute blocker for reconstructing the core runtime patch engine: the DLL/T5K resource directly exposes descriptor signatures, preimages, replacements, helper code, mapping relocation semantics, pointer modes and patch-application logic.

Do not use the mismatched supplied PC EXE for target-RVA neighborhood evidence.

## 13. Porting rule derived from this analysis

The PC runtime patch is now the reference implementation. A Switch clean-port design must compare/reproduce the meaning of the complete family:

- 10,036 mapping storage and all lookup/table references;
- 56 pointer redirects;
- `runtime_byte_validation`;
- `font_page_limit`;
- `runtime_page_mapper`;
- four `ui_width_*` adjustments;
- two `description_font_*` adjustments;
- 17,103 inline records, using actual Switch object correspondence rather than PC addresses.

Do not reduce this family to the historical 5,519 unique subset or to W0/W1 unless a later Switch-side analysis proves a PC behavior is already native/equivalent and therefore needs no patch.

## 14. Unresolved items

- exact Switch counterpart set for all 14 runtime sub-patches;
- full Switch reference set for relocated 10,036 mapping storage;
- per-record Switch counterpart/necessity classification for all 56 pointer records;
- exact UI role of `ui_width_1..4` and `description_font_1..2` without the exact PC EXE;
- whether any PC runtime behavior is already natively equivalent in Switch and requires no edit.

These are the next static-analysis stage. No Switch code or build is authorized by this document alone.
