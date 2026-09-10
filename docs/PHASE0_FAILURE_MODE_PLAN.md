# PHASE 0 FAILURE-MODE PLAN

This document defines the mandatory diagnosis that precedes implementation of the full 17,103-record inline validator.

## 1. Why Phase 0 exists

The observed Eden failures are compatible with at least two broad fault classes:

1. **candidate faults** — some PC inline records are mapped to the wrong Switch objects or violate Switch field structure;
2. **systemic faults** — the patch/build/runtime path has a prerequisite that fails whenever enough or certain Korean inline data is present, independent of whether a particular candidate is semantically correct.

The validator is designed to solve class (1). Before investing in the full validator, Phase 0 must test whether class (2) is independently present.

Do not state that "any inline set fails". The actually observed facts are narrower: the old 5,519 set failed, v0.2c still failed, A failed, and B reached title then failed after input.

## 2. Phase 0 order

### P0-A — source identity and reproducible measurements

Run `builder/phase0_probe.py` against the exact Switch `main` and PC patch ZIP. Record input hashes and count units.

If a PC original executable is supplied, it must be checked against the T5K target size/hash before it can be used for PC-RVA neighborhood/homology analysis.

### P0-B — IPS/build-layer control

Use a diagnostic build containing the known-good NO-INLINE baseline plus **5,519 no-op inline IPS records** at the historical selected offsets. Each no-op record writes the exact original Switch bytes back to itself. The page mapper remains the only intentional code change.

Interpretation:

- **boots like NO-INLINE**: record count/classic-IPS packaging/application is not the current failure cause; proceed to content MVI tests;
- **fails**: stop semantic-validator work and investigate IPS generation/loading/application first.

The generated test identifier is `P0N`. Test artifact binaries are not committed to this public repository.

### P0-C — Minimal Viable Inline (MVI)

Only after P0N passes, test a small number of independently selected, very-high-confidence real inline replacements.

Do not infer a systemic fault from one failing record. Use several independent candidates from different structural/text blocks.

Recommended progression:

1. multiple independent 1-record builds;
2. 10-record high-confidence build;
3. 100-record high-confidence build.

Interpretation must remain conditional:

- one candidate fails while others pass -> candidate-specific evidence;
- several structurally independent high-confidence candidates fail on the same transition -> systemic-prerequisite evidence strengthens;
- 1-record tests pass but a larger set fails -> cumulative/build-path or shared runtime-path hypothesis strengthens;
- 100 high-confidence records pass -> proceed with full validator implementation; this still does not prove every candidate safe.

### P0-D — runtime prerequisite analysis

Before attributing failures solely to bad candidate mappings, inspect the PC runtime descriptors and Switch counterparts, prioritizing:

1. `mapping_lookup_1A` / `mapping_lookup_2A`;
2. `runtime_byte_validation`;
3. `font_page_limit`;
4. then `ui_width_1~4` and `description_font_1~2` as symptom/reachability requires.

The remaining descriptors are not automatically prerequisites to beginning the validator; their actual semantics and reachability decide priority.

## 3. Confirmed mapping-loop observation

For fixed Switch v1.1.3 `main`, both known conversion loops still contain the original mapping-count limit `0x1D46 = 7,494`:

- `0x430350` UTF-16 -> game-code path: count load at `0x4303AC`;
- `0x4305D0` game-code -> UTF-16 path: count load at `0x430624`.

Manual ARM64 disassembly of the fixed flat image also establishes that a table miss has a defined fallback rather than an immediately undefined return:

- UTF-16 -> game-code miss falls back to bytes corresponding to `0x81A1` in the observed routine;
- game-code -> UTF-16 miss falls back to `U+25A0`.

Therefore the missing 10,036-entry expansion is a real functional gap, but **it is not presently proven to be the direct freeze mechanism**. It can still break search/sort/compare/save/conversion semantics and must be ported safely; do not use it as a crash conclusion without runtime/use-site evidence.

## 4. Build-layer checks

Classic IPS remains viable for the fixed flat image because mapped end `0xA20430` is below the 24-bit IPS offset ceiling `0xFFFFFF`.

Every diagnostic/release IPS generator must:

- reject offsets above `0xFFFFFF`;
- reject a record beginning at `0x454F46` (`EOF`) unless format handling explicitly changes;
- reparse the finished IPS;
- reconstruct the simulated patched image from the emitted IPS and compare it against the intended image/patch plan;
- distinguish flat NSO mapped offsets from compressed NSO file offsets.

P0N tests the loader/large-record-count path at runtime without introducing any inline content change.

## 5. Transition to the full validator

If P0N passes and MVI evidence does not reveal a general prerequisite failure, proceed to the full validator under `docs/INLINE_VALIDATION_POLICY.md`.

The validator must then add the review-derived structural axes:

- relocation/reference evidence as strong positive evidence, not an absolute requirement;
- `.data` excluded from auto-patching but retained as an evidence source;
- rodata-wide tail-merge/subsequence detection;
- local/piecewise block homology using order **and distance consistency**;
- multi-match recovery only when ambiguity is actually resolved;
- independent control-code whitelist frozen before classification;
- a negative/shuffled control group when choosing `info_len` thresholds;
- set-level post-patch invariants and nearby-patch interaction checks;
- final IPS reparse/diff against the intended simulated image.

Collinearity is not a universal mandatory gate. Strong independent structural evidence can support a candidate in a reordered block; conversely, collinearity alone cannot make a candidate safe.

## 6. Runtime testing rule

Phase 0 runtime tests answer narrow questions only. Record each result in `docs/RUNTIME_TEST_RESULTS.md` and the validation ledger.

A successful diagnostic run means only that the specific tested hypothesis did not fail on that path. It never promotes an unvalidated candidate to SAFE.
