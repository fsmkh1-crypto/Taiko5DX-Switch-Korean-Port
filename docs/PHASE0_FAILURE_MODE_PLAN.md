# PHASE 0 FAILURE-MODE PLAN

This document defines the mandatory diagnosis that precedes implementation of the full 17,103-record inline validator.

## 1. Why Phase 0 exists

The observed Eden failures are compatible with several fault classes:

1. **build/application faults** — generated IPS coordinates or serialization do not match Eden's NSO patch coordinate system;
2. **candidate faults** — PC inline records are mapped to the wrong Switch objects or violate Switch field structure;
3. **runtime-prerequisite faults** — semantically correct Korean inline data reaches an unported conversion/validation/runtime path.

Phase 0 must separate class (1) before drawing conclusions about classes (2) or (3).

## 2. Critical Eden IPS coordinate rule

Source inspection after the first P0N runtime failure established a previously missing `+0x100` rule.

Eden/Yuzu's NSO loader decompresses the NSO into `codeset.memory`, then constructs a patch image as:

```text
0x000000..0x0000FF  NSOHeader (0x100 bytes)
0x000100..          decompressed mapped NSO image
```

Classic IPS is applied to that header-prefixed patch image. Therefore:

```text
emitted IPS offset = mapped flat NSO offset + 0x100
```

Example:

- intended mapped page-mapper offset: `0x44650C`
- correct Eden IPS offset: `0x44660C`

All test builds through `P0N v0.2f` omitted this shift. Those tests remain historical runtime observations but cannot be used to infer candidate-level safety.

## 3. Phase 0 order

### P0-A — source identity and reproducible measurements

Run `builder/phase0_probe.py` against the exact Switch `main` and PC patch ZIP. Record input hashes and count units.

If a PC original executable is supplied, check it against the T5K target size/hash before using it for PC-RVA neighborhood/homology analysis.

### P0-B — corrected IPS/build-layer control

The original `P0N v0.2f` attempted 5,519 no-op records but was **not a true no-op at runtime** because every mapped offset was emitted without the required `+0x100`. It froze and thereby exposed the coordinate error.

The corrected control is **`P0N2 v0.2g`**:

- 207 RomFS replacements + Korean font;
- corrected page-mapper IPS record at `0x44660C` for mapped target `0x44650C`;
- 5,519 historical inline locations, each writing the original Switch bytes back to itself;
- every emitted inline IPS offset is mapped offset `+0x100`;
- 5,520 IPS records total.

Interpretation:

- **P0N2 boots**: corrected classic-IPS large-record path is viable; old P0N freeze is explained by the coordinate bug. Proceed to corrected semantic/MVI testing.
- **P0N2 fails**: isolate corrected page mapper from corrected 5,519 no-op records before any semantic-validator work.

Do not rerun old `P0N v0.2f`; its hypothesis was invalidated.

### P0-C — Minimal Viable Inline (MVI)

Only after P0N2 passes, test independently selected, very-high-confidence real inline replacements using the corrected `+0x100` emitter.

Do not infer a systemic fault from one failing record. Use several independent candidates from different structural/text blocks.

Recommended progression:

1. multiple independent 1-record builds;
2. 10-record high-confidence build;
3. 100-record high-confidence build.

Interpretation remains conditional:

- one candidate fails while others pass -> candidate-specific evidence;
- several independent high-confidence candidates fail on the same transition -> runtime-prerequisite evidence strengthens;
- 1-record tests pass but a larger set fails -> cumulative/shared runtime-path hypothesis strengthens;
- 100 high-confidence records pass -> proceed with full validator implementation; this still does not prove every candidate safe.

### P0-D — runtime prerequisite analysis

Before attributing corrected-offset failures solely to candidate mappings, inspect PC runtime descriptors and Switch counterparts, prioritizing:

1. `mapping_lookup_1A` / `mapping_lookup_2A`;
2. `runtime_byte_validation`;
3. `font_page_limit`;
4. then `ui_width_1~4` and `description_font_1~2` as symptom/reachability requires.

## 4. Confirmed mapping-loop observation

For fixed Switch v1.1.3 `main`, both conversion loops still contain the original mapping-count limit `0x1D46 = 7,494`:

- `0x430350` UTF-16 -> game-code path: count load at `0x4303AC`;
- `0x4305D0` game-code -> UTF-16 path: count load at `0x430624`.

Manual ARM64 disassembly shows defined miss fallbacks:

- UTF-16 -> game-code miss -> `0x81A1` bytes;
- game-code -> UTF-16 miss -> `U+25A0`.

The missing 10,036-entry expansion is therefore a real functional gap, but is not yet proven to be a freeze mechanism.

## 5. Build-layer checks

Classic IPS remains viable because mapped end `0xA20430` plus the `0x100` header prefix remains below `0xFFFFFF`.

Every diagnostic/release IPS generator must:

- keep analysis/PatchPlan offsets in mapped flat-image coordinates;
- add exactly `0x100` when serializing Eden/Yuzu classic IPS;
- reject emitted offsets above `0xFFFFFF`;
- reject emitted record start `0x454F46` (`EOF`) unless the format changes;
- reparse the final IPS;
- subtract `0x100` when validating emitted records against the mapped flat image;
- compare reconstructed post-patch bytes against the intended patch plan;
- never confuse compressed NSO file offsets, mapped flat offsets, and emitted IPS offsets.

## 6. Transition to the full validator

If P0N2 passes and corrected-offset MVI evidence does not expose a general runtime prerequisite failure, proceed to the full validator under `docs/INLINE_VALIDATION_POLICY.md`.

The validator retains the review-derived structural axes: relocation/reference evidence, `.data` as evidence but not auto-patch target, rodata-wide tail-merge/subsequence checks, local/piecewise homology using order and distance consistency, independent control-code whitelist, shuffled negative controls for `info_len`, set-level invariants, and final emitted-IPS reparse/diff.

Collinearity is strong evidence but not a universal mandatory gate.

## 7. Runtime testing rule

Record every Phase-0 runtime result in `docs/RUNTIME_TEST_RESULTS.md` and `docs/VALIDATION_LEDGER.md`.

A successful diagnostic run answers only its narrow hypothesis. It never promotes an unvalidated candidate to SAFE.
