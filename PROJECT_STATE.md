# PROJECT_STATE

Last updated: 2026-09-10 (KST)

This file is the canonical resume point for the project. Read it together with `PATCH_MAP.md`, `docs/INLINE_VALIDATION_POLICY.md`, and `docs/RUNTIME_TEST_RESULTS.md` before touching inline mapping or runtime crash diagnosis.

## 1. Goal

Port the existing PC Korean patch `Taiko5DX_Korean_Patcher_v1.02` to Nintendo Switch **TAIKO RISHHIDEN V DX v1.1.3**, with Eden Android as the primary development/test target.

Primary development direction remains one integrated Eden mod, but inline patches now have a mandatory static validation gate before they can re-enter the integrated build.

## 2. Project-level inline premise

The old rule "exact original bytes occur uniquely in Switch `main` rodata, therefore patch them" is superseded.

`unique exact match` is **candidate-discovery evidence only**. It is not a safety criterion.

A releasable inline patch must be supported by all of the following:

1. valid game-code decoding/encoding;
2. PC-to-Switch structural homology, preferably piecewise-collinear/anchor-supported;
3. independently established Switch-side field/boundary structure;
4. no unresolved overlap or severe binary-structure risk;
5. simulated post-patch offline re-validation.

Runtime success is a final sanity check, not proof that a candidate is safe.

The normative details are in `docs/INLINE_VALIDATION_POLICY.md`.

## 3. Input assumption

Development assumes a **complete extracted Switch 1.1.3 dump is locally available**. The builder consumes the dump root directly.

Expected local source material:

- Switch 1.1.3 ExeFS including `main`;
- Switch 1.1.3 RomFS;
- `Taiko5DX_Korean_Patcher_v1.02.zip`;
- PC original `Taiko5DX.exe` when PC RVA/context comparison is required.

Large/binary source material stays outside this public repository.

## 4. Fixed target identity

- Title ID: `0100346017304000`
- Switch version: `1.1.3`
- `main` NSO Build ID: `D9120950C258610A746F4A31CE3A3B376DE393D9`
- compressed `main` observed size: 5,287,359 bytes
- mapped uncompressed end: `0xA20430`

NSO segments:

- text: mem `0x000000`, decompressed `0x58CE60`
- rodata: mem `0x58D000`, decompressed `0x432018`
- data: mem `0x9C0000`, decompressed `0x60430`

## 5. PC Korean patch structure

Embedded `patch_payload.zip` contains 209 items:

- 169 `EVENT/*.TS5`
- 28 G1T
- 10 TR5
- 1 `TAI5MSG_JP.DAT`
- 1 `dinput8.dll`

Therefore: 208 game-data replacements + `dinput8.dll`.

All 208 target relative paths exist in Switch 1.1.3 RomFS. The builder may reuse 207 directly; `CMENU/CWTDAT_JP.TR5` is the deliberate platform exception.

## 6. CWTDAT platform exception

`CMENU/CWTDAT_JP.TR5` is structurally different between PC and Switch.

- Switch JP size: 480,382 bytes
- PC original JP size: 548,530 bytes
- PC Korean patched size: 548,530 bytes

Never replace the Switch file wholesale with the PC file. Reconstruct only validated Korean changes onto the Switch-native structure.

## 7. Font and Korean encoding

Switch original `FONT/FONT_JPN.G1T` and Steam original font are byte-identical.

- original font: 13,108,628 bytes, 50 pages
- original SHA-256: `9c886848c31c31d09aeeed0ac5c44b909d561220110ca04da0f7fa32d3a0083e`
- Korean patched font: 16,779,036 bytes, 64 pages
- patched SHA-256: `c82d80dada61ce80db42f948eafd3eb5b8f3bed5725ceebbc1c0897246166932`

Pages 0~48 are unchanged. Korean pages 49~62 correspond to lead bytes `EB~F8`. Page 63 is the final single-byte/ASCII-ish page.

Korean text uses the game's custom 1/2-byte code system, not generic UTF-8/UTF-16 and not a generic Shift-JIS decoder. Confirmed examples include `EBE0=기`, `ECE9=노`, `F5B6=타`.

## 8. Switch text/font functions

- `0x430350`: UTF-16 -> game code
- `0x4305D0`: game code -> UTF-16
- `0x446310`: 1/2-byte segmentation/count
- `0x446420`: `GetFontTexIndex`

Existing segmentation accepts `0x81~0x9F` and `0xE0~0xFC` as two-byte leads, so Korean `EB~F8` already segments correctly.

## 9. T5K121R resource

`dinput8.dll` SHA-256: `ffe7e9da8e00c96bec631b45a3e9c4d3f314551623351f3e7024e0318913c6b7`.

The builder extracts `RT_RCDATA/101` and parses `T5K121R` directly.

Canonical layout:

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

Header values:

- version 1
- inline records 17,103
- pointer records 56
- runtime descriptors 11
- target PC EXE size 18,685,960

## 10. Page mapper

Implemented Switch ARM64 in-place rewrite at `0x44650C..0x446534`:

- preserves existing Japanese mapping;
- adds `EB~F8 -> font pages 49~62`;
- no code cave required.

Original 44 bytes:

`690a4011293d00123ffd2b7168010054093940510ae09b1208010a0b3f01007108b1891a087d0813007d0011`

Replacement 44 bytes:

`693e08532a8103515f610071680100545f29007168000054407d00110400001440990011020000141f2003d5`

## 11. Mapping expansion

Canonical counts:

- original mapping: 7,494 (`0x1D46`)
- Korean additions: 2,542
- total: 10,036 (`0x2734`)

Any contrary count such as 7,334 is unverified and must not replace the confirmed 7,494 baseline without a reproducible measurement explaining the discrepancy.

Switch `0x430350` / `0x4305D0` still use the original 7,494-entry mapping. Full Unicode/input conversion support still requires safe table expansion/relocation plus reference/count patches.

## 12. Inline corpus and superseded selector

Canonical corpus:

```text
PC records total                 17,103
unique original patterns          8,713
no Switch match                     186
multiple Switch matches            2,476
unique match outside rodata          528
candidate rodata patterns           5,523
overlap-skipped                         4
old selected unique patterns       5,519
PC records covered by old set       5,521
```

The old 5,519-set was selected by exact-unique rodata matching and non-overlap. **It is no longer considered pre-approved or safe.** It is retained only as a regression/reference set.

The new validator target is the full **17,103-record corpus** so it can both reject false positives and recover valid repeated/ambiguous mappings using structural evidence.

Counts must always distinguish records, unique patterns, and candidate locations.

## 13. Measured/externally reviewed structural evidence

Review measurements indicate large order-preserving PC-RVA -> Switch-offset runs, suggesting substantial block-level collinearity between PC `.rdata` and Switch `.rodata`.

This is treated as a hypothesis/evidence source to reproduce in our own validator, not as an unquestioned imported result. The implementation must use **piecewise monotonic blocks/anchors**, not assume one global ordering across the entire binary.

Similarly, reports that many PC replacements consume NUL/padding are treated as a major risk signal. They do not automatically prove run-on on Switch: Switch-side field type/width must be established independently.

## 14. Current Eden Android runtime evidence

Empirical results are recorded in `docs/RUNTIME_TEST_RESULTS.md`.

Established results:

- add-on OFF: normal boot/run;
- `v0.2b NO-INLINE` = 207 RomFS replacements + Korean font + page mapper, zero inline: boots and renders Korean title `태합입지전 V DX`;
- integrated inline set: freezes;
- v0.2c with one suspicious record removed: still fails;
- address-ordered half A: freezes;
- address-ordered half B: reaches title, then pressing a button causes forced exit/crash.

Therefore inline patches are the current differentiating failure source and more than one unsafe mapping may exist. A passing split can never be treated as globally safe.

## 15. Inline validation architecture

Mandatory pipeline, summarized from `docs/INLINE_VALIDATION_POLICY.md`:

1. normalize all 17,103 records with stable record/pattern IDs;
2. validate original and replacement using the game's real mapping rules;
3. enumerate all Switch candidate positions instead of forcing uniqueness;
4. exclude ordinary `.text` mapping and keep `.data` out of auto-SAFE;
5. derive piecewise PC↔Switch collinearity blocks;
6. establish strong ANCHOR records;
7. resolve repeat/multi-match candidates inside reliable anchor blocks;
8. infer Switch field type/width independently from PC record length;
9. verify NUL/boundary/stride preservation;
10. flag integer/float/pointer/offset/table/padding/non-text risks;
11. use XREF/use-site evidence where feasible;
12. audit overlap and pattern-inclusion conflicts;
13. simulate applying the candidate set to the flat Switch image;
14. re-decode and re-check all patched fields offline;
15. classify ANCHOR / SAFE-A / SAFE-B / PROBABLE / HOLD / REJECT.

Do not automatically shorten translations to satisfy a guessed field width. If the original PC translation cannot be proven safe on Switch, HOLD it until a separate translation decision is made.

Do not hard-code arbitrary minimum lengths before corpus measurements. Use effective `info_len` distributions and structural evidence to determine thresholds.

## 16. Pointer records and remaining runtime work

The exact 56 pointer records are parsed and retained, but Switch correspondence is not yet emitted.

Remaining major items after/alongside inline validation:

- 7,494 -> 10,036 mapping relocation/reference/count patches;
- 56 pointer-record Switch mapping;
- `runtime_byte_validation` counterpart if required;
- font threshold behavior if required;
- `description_font_1~2`;
- `ui_width_1~4`;
- Switch-native `CWTDAT_JP.TR5` reconstruction.

## 17. Eden Android installation constraint

Do **not** assume normal Android file-manager access to Eden's internal folder.

Development ZIP flow:

1. extract into an ordinary accessible location such as `Download`;
2. Eden target-game Add-ons;
3. `+ Install` -> `Mods and cheats`;
4. select the extracted mod root containing `exefs/` and/or `romfs/` directly beneath it;
5. enable only the intended test build.

See `docs/EDEN_ANDROID_TEST_GUIDE.md`.

## 18. Final distribution target

Primary end-user frontend: **Android APK**.

The APK is a separate patch-generation app, not an Eden plugin. It will:

1. accept a user-selected complete extracted Switch 1.1.3 dump;
2. accept `Taiko5DX_Korean_Patcher_v1.02.zip`;
3. validate Build ID/source layout;
4. reuse the same core patch engine;
5. emit an Eden-ready `exefs/` + `romfs/` mod;
6. use Android SAF/user-granted locations.

It must not embed or redistribute game binaries, translated payloads/fonts, the PC patch archive, keys, XCI/NSP/NCA, or full dumps.

## 19. Work priority from here

1. Treat `docs/INLINE_VALIDATION_POLICY.md` as the mandatory premise for all inline work.
2. Build the full-corpus 17,103-record correspondence/validation pipeline when the user explicitly authorizes implementation.
3. Reproduce and measure collinearity, field structure, NUL/boundary behavior, `info_len` distributions, and conflict/risk classes.
4. Produce auditable machine-readable output plus a human-review summary.
5. Create ANCHOR-only, then SAFE-A, then SAFE-A+SAFE-B runtime builds only after offline gates pass.
6. Use delta debugging only if a statically validated set still produces a reproducible runtime failure.
7. Continue mapping expansion, pointer records, runtime/UI counterparts, and CWTDAT after the core text-safety architecture is stable enough to avoid reintroducing unsafe inline patches.
8. Wrap the stabilized core builder in the Android APK frontend last.

## 20. Anti-loop and execution rules

Do not revalidate established facts without new contradictory evidence. Prefer forward progress, but do not bypass the mandatory inline safety gates.

Do not begin implementation merely because design discussion is ongoing. Follow the explicit user-start rule in `AGENTS.md`.
