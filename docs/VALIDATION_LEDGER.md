# VALIDATION_LEDGER

Canonical record of what has actually been validated, what still needs revalidation, and what has been invalidated or superseded.

## Operating rule

The project must not repeatedly re-check an already well-recorded fact. However, a prior conclusion whose evidence/provenance is incomplete may be revalidated **once when the result materially matters to current work**. After that revalidation, the result must be recorded here with enough detail that another agent can reproduce or trust it without starting over.

A validation may be repeated only when at least one of the following is true:

1. an input file/version/hash changed;
2. a new runtime or static-analysis result directly contradicts the recorded conclusion;
3. the original record lacks enough provenance to support a current implementation decision;
4. the validation method itself is later shown to be unsound.

Do not revalidate merely because a new chat, agent, or model is starting.

## Required evidence for new validations

Every meaningful validation entry should record, where applicable:

- validation ID and date;
- exact claim being tested;
- input identity: filename/role, version, size, hash, Build ID as available;
- method/tool/script and relevant parameters;
- exact offsets/ranges/count units when relevant;
- observed result;
- final status;
- artifact/report/script path or commit that can reproduce the result;
- reason for any later revalidation, invalidation, or supersession.

Counts must state their unit explicitly, e.g. `records`, `unique patterns`, or `candidate locations`.

## Status values

- `VERIFIED`: direct evidence is sufficiently recorded for reuse.
- `VERIFIED-RUNTIME`: directly observed in the target runtime; keep static-safety claims separate.
- `VERIFIED-LEGACY`: likely valid prior result, but provenance is not yet sufficient for a high-risk implementation decision. Revalidate once if that decision depends on it.
- `NEEDS-REVERIFY`: conflicting, incomplete, or externally reported result that must be reproduced before becoming canonical.
- `INVALIDATED`: a previous conclusion was disproved.
- `SUPERSEDED`: still historically true, but replaced by a stronger/newer rule or result.

## Current ledger

| ID | Claim | Status | Recorded evidence / reuse rule |
|---|---|---|---|
| V001 | Fixed Switch target is v1.1.3, Title ID `0100346017304000`, `main` Build ID `D9120950C258610A746F4A31CE3A3B376DE393D9`. | VERIFIED | Recorded in `PROJECT_STATE.md`; builder hard-guards the Build ID. Recheck only if target version/dump changes. |
| V002 | Switch NSO mapped layout is text `0x000000+0x58CE60`, rodata `0x58D000+0x432018`, data `0x9C0000+0x60430`. | VERIFIED | Recorded in `PROJECT_STATE.md`; builder hard-guards the exact segment layout. Recheck only if `main` changes. |
| V003 | Switch original `FONT_JPN.G1T` matches Steam original; original SHA-256 `9c886848...a0083e`; PC Korean font SHA-256 `c82d80da...66932`; 50 -> 64 pages. | VERIFIED | Recorded in `PROJECT_STATE.md`; original/patched font hash guards exist in builder. Recheck only if source patch/dump changes. |
| V004 | T5K121R contains 10,036 mappings, 17,103 inline records, 56 pointer records, 11 runtime descriptors. | VERIFIED | Parsed directly from `RT_RCDATA/101`; layout and counts recorded in `PROJECT_STATE.md`/`PATCH_MAP.md` and parser path. Do not recount unless PC patch archive changes. |
| V005 | Original mapping count is 7,494 (`0x1D46`), Korean additions 2,542, total 10,036 (`0x2734`). | VERIFIED | Recorded consistently in `PROJECT_STATE.md` and `PATCH_MAP.md`. Any conflicting `7,334` claim is non-canonical until reproduced and explained. |
| V006 | The page-mapper rewrite bytes are correct for mapped flat offset `0x44650C` and logically add `EB~F8 -> pages 49~62` while preserving existing ranges. | VERIFIED | Static byte/disassembly evidence remains valid. **Previous Eden runtime evidence does not validate this rewrite**, because all earlier IPS generators omitted the required `+0x100` NSO-header shift; the old IPS record targeted flat `0x44640C`, not `0x44650C`. Correct Eden IPS offset is `0x44660C`. |
| V007 | Historical exact-unique scan: 17,103 records -> 8,713 unique original patterns; 5,523 candidate rodata patterns; 4 overlap-skipped; 5,519 selected patterns covering 5,521 PC records. | VERIFIED | Reproduced again on 2026-09-10 by `builder/phase0_probe.py`/historical selector against Switch `main` SHA-256 `b366e692...3109b` and PC patch ZIP SHA-256 `df1b62de...f7cec`. These are regression counts only; they are not a release-safety proof. |
| V008 | `unique exact match in rodata` by itself is sufficient to classify an inline patch as safe. | SUPERSEDED | The project policy rejects this as an insufficient methodology because it proves location uniqueness, not field semantics/structure. **Do not cite old v0.2a/A/B failures as proof of this claim's failure**, because those IPS records were all applied `0x100` early. `docs/INLINE_VALIDATION_POLICY.md` remains normative. |
| V009 | v0.2b NO-INLINE boots and reaches Korean title in Eden Android. | VERIFIED-RUNTIME | The observed boot/title is valid. However, the build's page-mapper IPS record used the wrong no-shift convention, so this result proves only that the RomFS/font baseline plus that misapplied 44-byte write reaches title. It does **not** prove the intended page mapper at flat `0x44650C` works at runtime. |
| V010 | A half of the old inline set freezes; B half reaches title then exits after button input. | VERIFIED-RUNTIME | The observations are real historical results, but their prior semantic interpretation is SUPERSEDED: both builds used IPS offsets `0x100` too low, so they cannot establish multiple candidate faults or candidate safety. Retain only as history. |
| V011A | Record-level unique-match PC-RVA/Switch-offset data has strong global monotonic structure: 6,053 record pairs, LIS 3,524, 2,529 outside the LIS; top adjacent monotonic runs 1,844 / 1,074 / 978 / 78. | VERIFIED | Reproduced on 2026-09-10 with `builder/phase0_probe.py` using fixed input hashes below. Pattern-level equivalent is 6,051 unique pairs, LIS 3,522. Global LIS is evidence/reference only, not a release hard gate. |
| V011B | 12,347 / 17,103 inline records contain at least one NUL in the original and no NUL in the replacement; 4,747 originals contain no NUL. | VERIFIED | Reproduced on 2026-09-10 by direct T5K record scan in `builder/phase0_probe.py`. This is a risk statistic, not proof of Switch run-on because Switch field type must be established independently. |
| V011C | External claim that `430` cases are structurally confirmed termination/run-on failures. | NEEDS-REVERIFY | The claim is not reproducible under the clearest unique-match definition. Our fixed-input probe gives 98 **records** where a unique match is followed by a non-zero byte after the full record, 266 records where any capped candidate has that property, and 439 capped candidate instances. The external `430` likely used a different unit/selection rule. Do not use `430` as a hard gate until its exact definition is reproduced. |
| V011D | External claim that patterns occurring `>=5` times correspond to `8,981 records / 1,242 patterns`. | NEEDS-REVERIFY | Fixed-input whole-flat scan capped at 5 gives `9,557 records / 1,539 unique patterns` with `>=5` observed occurrences. The discrepancy is material and likely reflects a different scope/filter. Do not use the external values canonically until scope is identified. |
| V012 | The currently supplied Drive `PC_Original/Taiko5DX.exe` is **not** the exact T5K target executable and must not be used for PC-RVA neighborhood/homology evidence. | VERIFIED | Supplied file: size `18,479,304`, SHA-256 `22e1cd1afbd7d87a58b3560e7549f7e0fb462c723b4db9e1b1e747babb765ef6`, version resource `1.2.1.0`. T5K/README target: size `18,685,960`, SHA-256 `10c69bab50d29baf6311360cafbf7383716a126a6484d209f5e299e12ab565a2`, Steam build 9163702. File-version equality is insufficient. Exact target EXE is optional for Switch-side work but required before PC-binary-context claims. |
| V013 | Both fixed Switch conversion routines still use mapping-count `0x1D46 = 7,494`; table misses have defined fallback behavior rather than an immediately uninitialized/undefined return. | VERIFIED | Fixed flat `main` derived from SHA-256 `b366e692...3109b`. ARM64 disassembly: `0x4303AC` loads 7,494 in UTF-16->game-code loop; `0x430624` loads 7,494 in game-code->UTF-16 loop. Miss paths observed at `0x4304E0` -> fallback `0x81A1` bytes and `0x430798` -> `U+25A0`. This confirms the 10,036 expansion is functionally needed but does **not** prove it is the direct freeze cause. |
| V014 | Eden/Yuzu-style classic IPS offsets for NSO patches include a `0x100` NSO-header prefix: mapped flat offset `X` must be emitted as IPS offset `X + 0x100`. | VERIFIED | Source-level proof: Eden NSO loader builds `pi_header = sizeof(NSOHeader) + decompressed patchable_section`, copies `codeset.memory` at `+sizeof(NSOHeader)`, then passes that image to `PatchNSO`; `sizeof(NSOHeader)==0x100`. Confirmed in Eden mirror commit `5f142c7926d0c7fcbbd0ce30794d72f638a43b2a` and the emuall Eden code path. This directly invalidates the builder's former no-shift emitter. |
| V015 | P0N v0.2f with 5,519 intended no-op records freezes in Eden Android. | VERIFIED-RUNTIME | User-observed on 2026-09-10. Because v0.2f emitted mapped offsets without `+0x100`, the records were **not true no-ops in Eden**. The result must not be interpreted as evidence that 5,519 IPS records or no-op writes themselves cause the freeze. |
| V016 | The statement "P0N v0.2f is a true no-op control in Eden" is valid. | INVALIDATED | Local round-trip checked the wrong coordinate system. Eden applies IPS to a 0x100-byte NSOHeader-prefixed decompressed image, so each intended no-op at mapped `X` actually overwrote mapped `X-0x100`. Corrected control is `P0N2 v0.2g` with all emitted offsets shifted `+0x100`. |

## Reproducible Phase-0 input identity

The 2026-09-10 Phase-0 probe used:

- Switch compressed `main` SHA-256: `b366e692208f3c0cc18bc1884ef95689b6b11d722fa2d749b8500abccbc3109b`;
- Switch mapped flat size: `10,617,904 (0xA20430)`;
- PC patch ZIP SHA-256: `df1b62de95e992369e9686c9731d814e7a7e4634888f610430635429e24f7cec`;
- embedded `dinput8.dll` SHA-256: `ffe7e9da8e00c96bec631b45a3e9c4d3f314551623351f3e7024e0318913c6b7`;
- `RT_RCDATA/101` SHA-256: `5c6f4eba8c6f0516365e4518f27e9d8c840aead463b5a2938dd1e08b99726d29`.

Reproduce these measurements with `builder/phase0_probe.py`; do not hand-recount them in later chats.

## Inline-validation precedence

For inline mapping, `docs/INLINE_VALIDATION_POLICY.md` is the normative safety policy. `docs/PHASE0_FAILURE_MODE_PLAN.md` is the mandatory prerequisite diagnosis before the full validator. This ledger answers a different question: **which underlying measurements and facts are already sufficiently proven, and which must be revalidated before use?**

When a new validation changes a canonical fact, update this ledger first or in the same commit as `PROJECT_STATE.md` / `PATCH_MAP.md` / `CHANGELOG.md`.
