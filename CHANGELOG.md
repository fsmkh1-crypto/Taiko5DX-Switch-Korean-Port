# CHANGELOG

## 2026-09-11

### PCREF1 delivery verification — artifact insufficient

- Added `docs/PCREF1_DELIVERY_VERIFICATION.md` and `docs/VALIDATION_LEDGER_PCREF1.md`.
- Added V062 as `NEEDS-REVERIFY`: historical PCREF1 emitted-delivery integrity is not established because the actual ZIP/IPS, SHA-256, record count, guard report, manifest, round-trip report, EOF handling result, and reproducible builder were not retained.
- Confirmed the accessible Google Drive `Eden_Builds/` and `Test_Results/` folders are empty; repository/File Library searches did not recover a PCREF1 artifact in the available sources.
- Preserved V014/V024/V025/V033: the `mapped + 0x100` coordinate rule and repeated/fixed-object locations remain independently established.
- Downgraded PCREF1's historical no-visible-change runtime result to observation-only. It must not invalidate `はい`, `年/月/日`, `城`, `清洲`, or duplicated `松平元康` object/fixed-field evidence because emitted delivery was never proven.
- Feedback loop remains un-restored. Before interpreting any new runtime no-change result causally, a fresh reproducible one-family delivery-control diagnostic must preserve manifest, original-byte guards, mapped/emitted coordinates, IPS round-trip, final record count, and SHA-256.
- Updated `PROJECT_STATE.md` so the recommended next stage after a fresh signal is delivery-control diagnostic design only; implementation/build still requires a later separate signal.
- No builder logic, Switch binary, ARM64, IPS, build, or runtime test was created or modified in this verification stage.

### PC Runtime Canonical Closure complete

- Added `docs/PC_RUNTIME_CANONICAL_CLOSURE.md`, `docs/PC_RUNTIME_SWITCH_COUNTERPART_MATRIX.md`, and `docs/SWITCH_COUNTERPART_SURVEY_RULES.md`.
- Rewrote `docs/PC_RUNTIME_DLL_SPEC.md` as the closed PHASE 1–4 PC reference and removed stale aggregate wording that conflicted with later validated phases.
- Corrected pointer grammar to `u32 slot / u32 original_target / u8 mode / reserved[3] / u32 arg`; mode 0 resolves `EXE base + arg`, mode 1 resolves `prefix base + arg`.
- Corrected size terminology: mapping = 40,144 bytes (`0x9CD0`), pointer pool = 602 bytes (`0x25A`), prefix total = 40,746 bytes (`0x9F2A`).
- Corrected allocation wording: PHASE 1 establishes one contiguous private allocation containing page-aligned prefix/helper regions, not two mandatory independent allocations.
- Preserved PHASE 4 control-flow corrections: byte-validation helper fallback resumes original processing at `0x68328A`; `font_page_limit` remains raw threshold `0xFF -> 0xA0` only.
- Separated PC specification completion from Switch port status; closure adds no V062+ facts and V001–V061 remain factual authority.
- Added five-axis Switch survey baseline: mapping, pointer 56, helper semantics, descriptor 14 semantics, inline/data-selection coverage; CWTDAT remains separate.
- Added evidence requirement for any `NATIVE_EQUIVALENT` classification and banned Switch unique-match as a coverage gate.
- Split storage risk by axis: mapping additional capacity, pointer replacement strings, optional helper executable space, and in-place descriptor/inline possibilities.
- Recorded compact `쓰` as a three-path unresolved problem: data selection, pointer/reference selection, byte-validation/copy.
- Recorded PCREF1 delivery verification as parallel to static survey but mandatory before interpreting a new counterpart-derived runtime result.
- No new Switch disassembly, ARM64 edit, IPS, build, or runtime test was performed. Next stage is Switch Functional Counterpart Survey after a fresh user signal.

### PC DLL PHASE 4 complete — helper and descriptor runtime semantics

- Added `docs/PC_RUNTIME_PHASE4_HELPER_DESCRIPTOR_SPEC.md` and `docs/VALIDATION_LEDGER_PHASE4.md`; advanced canonical resume state to PHASE 4 complete / STOP.
- Confirmed the 158-byte helper has two descriptor-used logical entries (`+0x00`, `+0x20`), with the PHASE 4 handoff reporting 42 reachable instructions, 4 bytes of unreachable padding/alignment, and four runtime-fixed control-transfer targets.
- Confirmed descriptor search scans target `.text`; mask byte zero ignores a position while nonzero compares the full byte. Success requires exactly one match and exact declared-anchor agreement, so a unique relocated signature is not accepted.
- Confirmed the fixed package's 14-subpatch total is separately checked during staging even though 14 is not a parser hard denominator.
- Canonicalized subpatch formulas: kind0=`payload`; kind1=`i32(P-W-4)`; kind2=`i32(P-M)`; kind3=`E9 || i32(H+arg-W-5)`. Kinds 1/2 do not use `arg`; kind3 uses it as the helper-entry offset.
- Confirmed `runtime_page_mapper` -> helper `+0x00`: `EB..F8` maps to pages 49..62; nonmatching input resumes original PC flow at RVA `0x6933D5`.
- Corrected `runtime_byte_validation` semantics: helper `+0x20` directly handles accepted one/two-byte forms and jumps to `0x6832BC`; fallback resumes the original processing path at `0x68328A`. It is not a Boolean-return validator.
- Accounted for all 11 descriptors / 14 subpatches with fixed-resource kind population 9/2/1/2 and successful write RVAs recorded in the PHASE 4 detail document.
- Corrected `font_page_limit` wording: raw confirmed behavior is compare threshold `0xFF -> 0xA0`, not a directly proven literal font-page-count assignment.
- The original PHASE 4 handoff listed a verification JSON, probe script, and raw-evidence ZIP. Those auxiliary files were not available during canonical import and were not fabricated; the transfer limitation is recorded in the PHASE 4 detail/ledger.
- No Switch counterpart research, ARM64, IPS, build, or runtime test was performed. Next stage is PC Runtime Canonical Closure only after a fresh user signal.

### PC DLL PHASE 3 complete — mapping relocation and pointer engine

- Added `docs/PC_RUNTIME_PHASE3_MAPPING_POINTER_SPEC.md` and a PHASE 3 validation-ledger part.
- Confirmed the `0x9F2A` private runtime prefix contains the 10,036 x 4-byte mapping table (`0x9CD0`) followed by the 602-byte pointer replacement pool (`0x25A`); the mapping table is runtime data, not builder-only metadata.
- Confirmed two mapping lookup paths collectively relocate three table/address operands and expand two count limits from 7,494 (`0x1D46`) to 10,036 (`0x2734`).
- Surveyed all 56 pointer records using PHASE-2's canonical `u8 mode + reserved[3] + u32 arg` grammar. Every record stages an 8-byte absolute pointer write.
- Confirmed mode 0 (5 records) computes `EXE/module base + arg`; the five records converge on two module-resident targets translated by inline patches.
- Confirmed mode 1 (51 records) computes `private prefix base + arg`; the 51 records reference 47 distinct replacement strings.
- Confirmed mapping relocation and pointer-record application are separate engines sharing the private prefix allocation; pointer records do not themselves relocate the mapping table.
- Exact target PC EXE absence leaves complete XREF/table/UI naming unresolved only; helper and runtime-descriptor semantics remain deferred to PHASE 4.
- No Switch counterpart research, ARM64, IPS, build, or runtime test was performed.

### PC DLL PHASE 2 complete — T5K parser grammar and bounds

- Extended `docs/PC_RUNTIME_REVERSE_ENGINEERING.md` with an address-grounded reconstruction of parser `0x2640` only; no mapping/pointer/helper/descriptor runtime semantics or Switch counterpart work was performed.
- Confirmed the exact `0x48` T5K header grammar, including `u64` target EXE size and 32-byte target SHA-256, plus fixed parser denominators for version/counts/prefix/helper lengths.
- Confirmed top-level exact consumption: prefix `0x9F2A`, helper `0x9E`, 17,103 variable inline records, 56 fixed 16-byte pointer records, 11 variable descriptors, then mandatory zero trailing bytes.
- Reconstructed inline, pointer, descriptor and subpatch binary layouts and parser-level bounds/payload rules. Pointer `mode` is a single byte with three skipped reserved bytes; subpatch kinds are structurally limited to 0..3.
- Confirmed parser `0x2640` does not hard-code the target EXE size/hash and does not parse a mapping-count header field; those interpretations are rejected.
- Audited `builder/t5k.py` as a convenience parser rather than a canonical wire-format implementation: current fixed blob still parses for existing uses, but EXE-size width, pointer grammar, exact prefix/helper denominators and runtime descriptor structure differ from the PC parser. `mapping_lookup_1A/2A` are cross-boundary substring false positives.
- Added PHASE 2 validation ledger entries and advanced the canonical resume gate to PHASE 3 pending fresh user authorization.
- Documentation-only change. No builder/source modification, ARM64, IPS, mod build or runtime test was performed.

### PC DLL PHASE 1 complete — loading, initialization and transaction only

- Added cumulative `docs/PC_RUNTIME_REVERSE_ENGINEERING.md` with exact DLL RVA evidence for PE/proxy/once initialization, resource acquisition, target identity, staging, commit, rollback and fatal errors.
- Reused fixed input identities and existing PC runtime facts; no mapping/pointer/descriptor/helper semantic reanalysis or Switch counterpart work in this phase.
- Clarified one contiguous private allocation, inline/pointer/code write priorities, and best-effort rollback limits (unchecked rollback API returns and no atomicity guarantee).
- Added V034–V039 and an active PHASE 1 complete / STOP resume gate.
- Documentation-only change. No executable, builder, patch, IPS, build or test automation changed.

### W1 runtime result: direct compact-`쓰` cause hypothesis invalidated

- User runtime-tested `W1 v0.2n`; the tested Matsudaira nameplate still appears without `쓰`.
- The static render-width gate at mapped `0x44D9D0` remains a verified control-flow fact, but the hypothesis that it directly caused the missing compact `쓰` symptom is invalidated.
- Static inspection found two corresponding Switch `松平元康` fixed fields at mapped `0x729D4D` and `0x729D5E`; the historical D5519 unique-only selector patched neither because the original pattern occurs twice. The preceding `松平竹千代` occurrence was unique and therefore selected.
- Therefore the prior premise that an active compact `BD=쓰` byte was reaching the tested nameplate renderer was not established. W1 must not be repeated as a compact-`쓰` fix without first tracing the actual event/person -> current name/alias slot -> rendered-name path.
- W0 observations are retained, but the claim that W0 directly fixed `케/자` through the A1+ single-byte threshold family is downgraded because `케/자` are normal two-byte Korean codes.
- Updated canonical state/ledger/runtime/analysis/mapping documents only. No new code patch or diagnostic build was created.

### Project operating rules strengthened

- Strengthened `AGENTS.md` so a single observed symptom must not be patched in isolation once a common mechanism is suspected. Agents must first survey the full root-cause family: affected data classes, code paths, call sites, runtime descriptors, and analogous visible symptoms.
- Added a PC-patch-first rule: when the Windows Korean patch already implements equivalent behavior, inspect its actual replacement bytes, font strategy, runtime descriptors, pointer handling, and related implementation before inventing a Switch-only workaround.
- Split analysis and implementation into explicit phases. After an analysis result is reported, a fresh user execution signal is required before code edits, build generation, or commits for the next stage.
- Clarified that one execution signal authorizes only the scope agreed at that moment; it does not carry forward automatically into later stages.
- Added diagnostic-build discipline: one root-cause family per diagnostic artifact, while all proven instances of that same mechanism should be tested together rather than patched one-by-one.
- Added explicit hypothesis-invalidation recording so failed local approaches are not repeated under new names.
- Added source-grounded naming/encoding rule: when Korean spelling, compact glyph codes, or replacements are directly available from the PC patch/font/canonical data, verify them from source instead of guessing from romanization or screen appearance.

### W0 partial pass; W1 render-width diagnostic prepared

- User runtime-tested `W0 v0.2m` in Eden Android. The build remained stable on the tested route.
- W0 corrected the previously odd `케/자` rendering in `나야 스케자에몬` as an observed runtime change; direct causality to the A1+ single-byte threshold family is now downgraded by the later W1/name-slot findings.
- The compact single-byte second glyph in the PC `松平元康` replacement is correctly transcribed as **`쓰`**: page-63 `B2/BD/AA = 마/쓰/다`; earlier project text saying `마츠다이라` / `BD=츠` was a transcription error and has been corrected in canonical docs.
- Switch disassembly established that JP per-character decode around `0x445C60` already accepts `0xA1..0xDF` as one-byte values, so any `BD=쓰` that reaches that path is not dropped at basic byte decoding.
- Found a text-render/layout compare at mapped `0x44D9D0`: codes `<0x100` are forced to width 8 immediately before the alternate width path and glyph draw/construction call.
- Prepared `W1_Taiko5DX_KR_DBG_FONTWIDTH_RENDER_v0.2n.zip`, SHA-256 `26fcd1434561b2e02d797079d6d996e5becfe66808e763d0b309ee1db10d44d1`.
- W1 is W0 plus exactly one edit: mapped `0x44D9D0` / Eden IPS `0x44DAD0`, `cmp w8,#0x100 -> cmp w8,#0xA1`. Static original-byte guard and IPS round-trip pass. Later runtime result is recorded above and invalidates the direct-cause hypothesis.

### Y0 runtime result: narrow suppression hypothesis incomplete

- User runtime-tested `Y0 v0.2l` in Eden Android.
- Y0 remained stable, but the garbled small reading rows in protagonist selection and dialogue nameplates did not disappear.
- The eight direct `mov w6,#1` call sites to shared routine `0x45B0F8` remain valid static mappings, but they do not control the observed two rows by themselves, or another wrapper/path renders/re-enables them.
- Do not repeat the eight-site-only suppression attempt. Internal Japanese yomi preservation remains the data policy while the actual visible-row path is deferred behind higher-priority name-data analysis.

### D5519 corrected full-inline diagnostic passed

- User runtime-tested `D5519 v0.2k`, which reuses the historical v0.2a 5,519 real inline payload bytes but fixes every Eden IPS address to `mapped + 0x100`.
- D5519 reached title, menu, scenario selection/description, protagonist selection, and normal gameplay without freeze/forced exit on the tested route.
- This strongly shifts the old freeze diagnosis from "the 5,519 inline set is broadly unsafe" to "the pre-P0N2 builds were dominated by the missing +0x100 IPS coordinate bug". The 5,519 set is still not release-certified for all paths.
- Visible residual issues are now treated as UI/data-coverage problems: garbled auxiliary yomi line, repeated short Japanese UI tokens, repeated place-name fields, and person-name/fixed-slot coverage/selection issues.

### Yomi strategy established

- Added `docs/POST_D5519_ANALYSIS.md`.
- Verified that 2,099 of D5519's 5,519 real inline records target halfwidth-kana/NUL fields; 3,420 historical non-yomi records remain after excluding them.
- Verified eight mapped call sites containing `mov w6,#1` immediately before/near calls to shared name/yomi routine `0x45B0F8`: `0x2A0ABC`, `0x2A565C`, `0x2A6F4C`, `0x2A7720`, `0x2A7FE4`, `0x2ADE5C`, `0x2BC1A0`, `0x2BD5C8`.
- Switch-port policy is: keep Korean main names, preserve original Japanese yomi internally for sort/comparison/input compatibility, and eventually suppress only the visible auxiliary yomi line through the actual rendering path.
- Added reproducible `builder/build_y0_noyomi.py`.
- `Y0_Taiko5DX_KR_DBG_NOYOMI_v0.2l.zip` SHA-256 `ae67b2bdece0e261239a3a505ad018761904c25124f0857cf0a917f9a4a6c869`.

### Repeated-object recovery evidence

- Added `builder/repeated_token_probe.py` to distinguish actual Switch string objects from raw substring collisions.
- `はい`: 7 raw rodata matches but exactly one standalone NUL object at `0x6A15A5`, pointer-ref `0x58D0D0`; adjacent pointer-table object is `いいえ` at `0x6A65B2`.
- Pooled date suffix objects identified: `年 0x69785A`, `月 0x68925A`, `日 0x6A3CC6`; pointer table `0x59C730..0x59C768` references them consecutively. Multiple PC records all agree on `년/월/일`.
- Pooled standalone `城` object identified at `0x6A15DC`, with multiple pointer refs; PC replacements agree on `성`.
- `清洲`: two T5K padded records with identical replacement `기요스`; Switch has exactly two corresponding fixed-field objects at `0x6AE269` and `0x6AEFE9`.
- New rule: recover repeated objects, not every raw byte match. Require replacement agreement and independent boundary/pointer/stride evidence.
- Currency `貫/文` remains a separate structural pass because many visible uses are embedded in longer format strings.

### Canonical documentation advanced

- Updated `PROJECT_STATE.md`, `PATCH_MAP.md`, `docs/RUNTIME_TEST_RESULTS.md`, `docs/VALIDATION_LEDGER.md`, and `docs/POST_D5519_ANALYSIS.md` to record W1's failed direct-cause test and remove the stale runtime-pending state.

## 2026-09-10

### Corrected Eden IPS coordinate bug

- Confirmed Eden/Yuzu NSO classic IPS operates on `0x100-byte NSOHeader + decompressed mapped image`.
- Canonical rule: `emitted IPS offset = mapped flat offset + 0x100`.
- Corrected `builder/build.py` and diagnostic builders to preserve mapped offsets internally and add `+0x100` only during IPS serialization.
- Pre-P0N2 IPS-bearing builds patched `0x100` bytes early; their crashes cannot be used as candidate-safety evidence.

### P0N2 passed

- `P0N2 v0.2g`: corrected mapper + 5,519 true no-op records.
- Runtime PASS through Korean title, input, and main menu.
- This disproved the hypothesis that 5,520 classic-IPS records themselves caused the old freeze.

### M1A passed

- `M1A v0.2h`: one real inline `R489`, `シナリオを選んでください` -> `시나리오를 선택하세요`, mapped `0x69B6A1`, emitted `0x69B7A1`.
- Runtime PASS through scenario/protagonist-selection flow.

### Phase-0 evidence/provenance

- Added `docs/PHASE0_FAILURE_MODE_PLAN.md`, `builder/phase0_probe.py`, and corrected diagnostic builders.
- Reverified historical selector counts: 17,103 records; 8,713 unique originals; 5,523 unique-rodata candidates; 4 overlap skips; 5,519 selected patterns covering 5,521 PC records.
- Reproduced collinearity: 6,053 record-level unique pairs; LIS 3,524; 2,529 outside; top runs 1,844/1,074/978/78.
- Reproduced NUL statistic: 12,347 records contain NUL in original and none in replacement; 4,747 originals contain no NUL.
- External `430` termination and `8,981/1,242` >=5-match figures remain non-canonical because the fixed-input probe did not reproduce their stated definitions.
- Confirmed Switch conversion loops still use 7,494 entries and have defined misses (`0x81A1`, `U+25A0`).
- Confirmed supplied Drive `PC_Original/Taiko5DX.exe` is not the exact Steam build-9163702 T5K target and barred it from PC binary-context evidence.

### Validation policy/ledger

- Added `docs/INLINE_VALIDATION_POLICY.md` and `docs/RUNTIME_TEST_RESULTS.md`.
- Promoted `docs/VALIDATION_LEDGER.md` to mandatory pre-read and no-redundant-revalidation authority.
- `unique exact match` is candidate discovery only; runtime pass is sanity evidence only.
- Full release validator target remains all 17,103 T5K inline records.

### Distribution/target workflow

- Fixed Eden Android as primary runtime target and Android APK as final frontend.
- APK will accept user-supplied complete Switch v1.1.3 dump + PC patch ZIP and emit an Eden-ready mod via SAF/user-granted locations.
- Direct normal file-manager access to Eden internal Android storage is not assumed; use Eden Add-ons import during development.
- Repository must never contain game executables/data, patch payloads/fonts, keys, dumps, or generated full mod packages.
