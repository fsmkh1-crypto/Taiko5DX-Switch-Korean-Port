# PC DLL PHASE 2 — T5K parser grammar and bounds

Date: 2026-09-11
Status: COMPLETE / STOP

## 1. Scope and evidence

This phase analyzes only the PC Korean patch T5K parser. It does not analyze mapping/pointer runtime meaning, helper machine-code semantics, runtime-descriptor semantics, or any Switch counterpart.

Fixed evidence:

- embedded `dinput8.dll` SHA-256 `ffe7e9da8e00c96bec631b45a3e9c4d3f314551623351f3e7024e0318913c6b7`
- `RT_RCDATA/101` SHA-256 `5c6f4eba8c6f0516365e4518f27e9d8c840aead463b5a2938dd1e08b99726d29`
- parser entry DLL RVA `0x2640`
- parser failure propagates to PHASE-1 init caller around `0x7A5E`; a malformed recipe does not continue to disk identity, staging, or commit.

Established V004/V005 counts are reused rather than re-counted as a new claim.

## 2. Exact 0x48-byte header

Wire layout:

```text
+0x00  char magic[8]          = "T5K121R\0"
+0x08  u32 version
+0x0C  u32 inline_count
+0x10  u32 pointer_count
+0x14  u32 descriptor_count
+0x18  u32 prefix_len
+0x1C  u32 helper_len
+0x20  u64 target_exe_size
+0x28  u8  target_exe_sha256[32]
+0x48  first payload byte
```

Parser `0x2640` hard-validates these structural denominators:

```text
version          = 1
inline_count     = 17,103
pointer_count    = 56
descriptor_count = 11
prefix_len       = 0x9F2A
helper_len       = 0x9E
```

The parser does **not** hard-code the target EXE size or hash. It preserves the header values; the later identity path established in PHASE 1 compares the actual EXE against them.

There is **no mapping_count header field**. The known 10,036 mapping count is independently established semantic knowledge about the prefix, not a field parsed by `0x2640`.

## 3. Exact top-level consumption

For the fixed resource, parser traversal is:

```text
0x00000..0x00047  header                 0x48
0x00048..0x09F71  prefix                 0x9F2A
0x09F72..0x0A00F  runtime helper blob    0x009E
0x0A010..0x951BF  inline records         17,103 variable records
0x951C0..0x9553F  pointer records        56 * 0x10
0x95540..0x95D34  runtime descriptors    11 variable descriptors
0x95D35            EOF
```

The parser requires exact consumption. After the eleventh descriptor the cursor must equal the resource end; trailing garbage is rejected.

Prefix/helper are represented as spans into the locked resource rather than being semantically split by the parser. The known prefix interpretation `10,036 x 4 mapping + pointer string pool` is a later semantic layer and is PHASE 3 territory.

## 4. Inline record wire grammar

Each inline record is:

```text
u32 pc_rva
u32 length
u8  original[length]
u8  replacement[length]
```

Parser-level rules:

- a fixed 8-byte header must fit;
- `length` must be non-zero;
- both original and replacement payloads of exactly `length` bytes must fit inside the resource;
- cursor advances by `8 + 2*length`;
- `pc_rva` target validity against the EXE is not established as a parser-level check here; later staging/preimage checks are a separate layer from PHASE 1.

The fixed resource's inline lengths span 1..445 bytes. That observed population is not a parser maximum.

## 5. Pointer record wire grammar

Each pointer record is exactly 16 bytes:

```text
+0x00 u32 pc_slot_rva
+0x04 u32 pc_original_target_rva
+0x08 u8  mode
+0x09 u8  reserved[3]
+0x0C u32 arg
```

Parser-level rules:

- all 16 bytes must fit;
- `mode <= 1` is enforced;
- the three reserved bytes are skipped; PHASE 2 did not find a zero-value validation on them;
- the runtime meaning of `mode` and `arg` is intentionally deferred to PHASE 3.

Current fixed resource population is 51 records with mode 1 and 5 records with mode 0. This is an observed resource distribution, not a parser denominator.

Important correction: treating the third field as a full `u32 mode` (as current `builder/t5k.py` effectively does with `<IIII`) is not the canonical PC wire grammar.

## 6. Runtime descriptor wire grammar

Each descriptor begins with four u32 values:

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

Parser structural constraints include:

- `signature_len` in `1..0x1000`;
- `patch_count > 0`;
- `name_len` in `1..0xFF`;
- every name/signature/mask/subpatch region must remain within the resource bounds.

The name is length-delimited, not a NUL-terminated scanner. Therefore descriptor discovery by arbitrary residual substring search is non-canonical.

### Subpatch wire grammar

A subpatch has a fixed `0x14`-byte header followed by variable data:

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

Parser-level constraints:

- `preimage_len != 0`;
- `offset + preimage_len` is overflow-protected and must fit inside the enclosing descriptor signature;
- `kind <= 3`;
- kind 0 requires `payload_len == preimage_len`;
- kinds 1, 2, 3 require `payload_len == 0`;
- every variable payload must fit resource bounds.

The fixed resource contains 14 total subpatches distributed as kinds 0/1/2/3 = 9/2/1/2. **Fourteen is not a parser-level hard denominator**; only the descriptor count 11 is fixed by the top-level parser.

The runtime meanings of kinds/arg are deferred to PHASE 4.

## 7. Parsed in-memory representation

`0x2640` does not copy the full resource into one new semantic blob. The observed parsed recipe object uses:

- a raw `0x48` header copy;
- zero-copy spans for prefix/helper and byte payloads;
- vectors for inline records, pointer records and descriptors;
- descriptor name as an MSVC `std::string`-like field;
- typed subpatch vector entries.

Observed layout anchors:

```text
Parsed recipe object ~0xB0 bytes
+0x00..+0x47 raw header copy
+0x48 prefix_ptr
+0x50 prefix_len
+0x58 helper_ptr
+0x60 helper_len
+0x68/+0x70/+0x78 inline vector begin/end/capacity
+0x80/+0x88/+0x90 pointer vector begin/end/capacity
+0x98/+0xA0/+0xA8 descriptor vector begin/end/capacity

parsed inline entry      0x28 bytes
parsed descriptor entry  0x60 bytes
parsed subpatch entry    0x30 bytes
```

These parsed-object sizes describe the DLL's in-memory representation, not additional wire fields.

## 8. Failure propagation

Explicit structural validation failure returns parser false. The PHASE-1 initialization caller then takes the common failure path before EXE identity, storage preparation, staging, and transaction commit.

Therefore the PC patch does not tolerate a malformed T5K record by merely skipping that record and continuing.

Allocator/CRT exceptional failures are governed by the broader PHASE-1 SEH/fatal framework; PHASE 2 makes no stronger cleanup guarantee.

## 9. Audit of current `builder/t5k.py`

`builder/t5k.py` remains useful for established fixed-blob analysis, but it must not be cited as the canonical PC wire-format implementation.

Differences from DLL parser `0x2640`:

1. reads target EXE size as u32; actual wire field is u64;
2. hard-checks the known target EXE size during parse, while the PC parser preserves header size/hash and later identity logic validates them;
3. does not enforce the exact prefix/helper denominators as the PC parser does;
4. parses pointer records as `<IIII>`, folding `u8 mode + reserved[3]` into a u32;
5. leaves runtime descriptors as a residual blob and searches substrings instead of parsing the length-delimited descriptor/subpatch structure;
6. consequently does not reproduce the PC parser's exact descriptor/subpatch bounds and trailing-byte checks.

The previously reported names `mapping_lookup_1A` and `mapping_lookup_2A` are substring false positives. Actual descriptor names are:

```text
mapping_lookup_1
mapping_lookup_2
```

The following signature's first byte is `0x41` (`'A'`), so a cross-boundary substring scan spuriously extends each real name by one character.

No builder source was modified in PHASE 2. Correcting the convenience parser is an implementation task and requires a separate user signal if/when needed.

## 10. Confirmed / deferred / rejected

### Confirmed

- exact 0x48 header widths and field roles;
- fixed structural denominators;
- prefix/helper zero-copy spans;
- inline/pointer/descriptor/subpatch wire grammars;
- bounds and payload rules;
- exact no-trailing-data requirement;
- parsed object/vector representation;
- parser false -> initialization failure propagation;
- differences between DLL parser and current builder convenience parser.

### Deferred to PHASE 3/4

- prefix mapping/string-pool runtime meaning;
- mapping 10,036 allocation/relocation/lookup application;
- pointer mode/arg runtime semantics and 56-record application engine;
- helper 158-byte machine-code semantics;
- descriptor kind/arg runtime meanings;
- signature/mask application behavior in staging beyond parser structure.

### Rejected interpretations

- mapping_count exists in the T5K header;
- parser hard-codes the target EXE size/hash as approval constants;
- pointer mode is a full u32 wire field;
- descriptor grammar is NUL-terminated or substring-based;
- trailing resource data is tolerated;
- total subpatch count 14 is a parser hard denominator.

## 11. PHASE 3 handoff

After a fresh execution signal, PHASE 3 should analyze only:

1. mapping 10,036 runtime storage and lookup relocation;
2. pointer 56 mode/arg application engine.

Do not enter helper 158-byte semantics or descriptor semantic interpretation; those remain PHASE 4. Do not inspect Switch counterparts, ARM64, IPS or builds during PHASE 3.

STOP.
