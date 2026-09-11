# PROJECT_STATE

Last updated: 2026-09-11 (KST)

## Active staged analysis — PC Runtime Canonical Closure complete / STOP

PC DLL PHASE 1–4 and the subsequent Canonical Closure are complete. The closed PC reference is `docs/PC_RUNTIME_DLL_SPEC.md`; integration/audit details are in `docs/PC_RUNTIME_CANONICAL_CLOSURE.md`.

Canonical closure results:

- PHASE 1–4 factual authority remains validation ledger V001–V061; closure adds no V062+ claims.
- the Windows runtime package is structurally closed through initialization, T5K parser, mapping 10,036, pointer 56, helper 2 entries, descriptor 11/subpatch 14, staging and transaction commit.
- canonical pointer grammar is `u32 slot, u32 original_target, u8 mode, reserved[3], u32 arg`; old `<IIII>` aggregate wording is superseded.
- prefix total `0x9F2A = 40,746` bytes = mapping `0x9CD0 = 40,144` bytes + pointer replacement pool `0x25A = 602` bytes.
- prefix/helper use one contiguous PC private allocation with page-aligned regions; older separate-allocation wording is superseded.
- `runtime_byte_validation` helper `+0x20` is a copy/control-flow trampoline; fallback resumes original processing at PC RVA `0x68328A`, not immediate rejection.
- `font_page_limit` raw confirmed behavior is threshold `0xFF -> 0xA0`, not a literal page-count assignment.
- PC descriptor unique-match + exact-anchor behavior is PC target-version application machinery, not a future Switch counterpart uniqueness gate.

Switch port status is intentionally separate from PC completion. Baseline matrix: `docs/PC_RUNTIME_SWITCH_COUNTERPART_MATRIX.md`.

Primary next-stage axes:

1. mapping 10,036 storage/references/counts;
2. pointer 56 and replacement-string ownership;
3. helper semantics (`runtime_page_mapper`, byte-validation/copy);
4. all 14 descriptor subpatch semantics;
5. inline 17,103 / repeated objects / fixed fields / data-selection coverage.

CWTDAT compatibility remains a separate data-port axis.

Current major placement risks are also split by axis:

- mapping: 2,542 Korean additions require representable capacity somewhere beyond the known original 7,494-entry behavior unless a complete equivalent table is later found elsewhere;
- pointer mode-1: the PC implementation uses a 602-byte pool, but Switch may or may not need comparable new storage depending on object reuse;
- helper: new executable storage is **not** assumed mandatory because equivalent behavior may be possible through existing ARM64 control-flow edits;
- literal descriptor counterparts may be in-place.

The compact `쓰` symptom remains unresolved across three independent paths: (a) duplicated fixed-field/active name-slot selection, (b) pointer/reference selection, and (c) byte-validation/copy behavior. Do not promote one to root cause without evidence.

PCREF1 emitted-IPS verification is not a prerequisite for static counterpart discovery, but must be closed before a new counterpart-derived runtime build result is interpreted causally. Survey and PCREF1 verification may therefore run in parallel, but implementation/runtime validation may not ignore the delivery uncertainty.

Next authorized stage only after a fresh user signal: **Switch Functional Counterpart Survey**, following `docs/SWITCH_COUNTERPART_SURVEY_RULES.md`. That survey must report and STOP before any implementation/build stage.

This is the canonical resume point. Before new Switch work, read it with `docs/VALIDATION_LEDGER.md`, `docs/PC_RUNTIME_DLL_SPEC.md`, `docs/PC_RUNTIME_CANONICAL_CLOSURE.md`, `docs/PC_RUNTIME_SWITCH_COUNTERPART_MATRIX.md`, `docs/SWITCH_COUNTERPART_SURVEY_RULES.md`, `PATCH_MAP.md`, `docs/INLINE_VALIDATION_POLICY.md`, `docs/RUNTIME_TEST_RESULTS.md`, and `docs/POST_D5519_ANALYSIS.md`.

## 1. Goal

Port `Taiko5DX_Korean_Patcher_v1.02` to Nintendo Switch **TAIKO RISHHIDEN V DX v1.1.3**, with Eden Android as the primary target. Final user-facing frontend remains an Android APK reusing the stabilized core builder.

## 2. Canonical Eden IPS coordinate rule

Eden/Yuzu NSO IPS patching operates on `0x100-byte NSOHeader + decompressed mapped NSO image`.

```text
emitted Eden IPS offset = mapped flat NSO offset + 0x100
```

Example: mapped page mapper `0x44650C` -> Eden IPS `0x44660C`.

All IPS-bearing builds through P0N v0.2f omitted this shift and patched `0x100` early. Their crashes remain historical observations but cannot establish candidate-level safety/failure.

## 3. Corrected runtime baseline

- **P0N2 v0.2g**: corrected mapper + 5,519 true no-op records -> PASS through title/input/main menu.
- **M1A v0.2h**: one corrected real inline `R489` -> PASS through scenario/protagonist flow.
- **D5519 v0.2k**: historical 5,519 real replacements with only the IPS coordinates corrected -> PASS through title, menu, scenario flow, protagonist selection, and normal early gameplay without freeze/forced exit.

D5519 strongly attributes the former immediate freezes to the missing `+0x100` build-layer defect. It does not certify every historical inline record for every late-game path.

## 4. Current visible issues

Current runtime screenshots establish several independent residual classes:

1. garbled auxiliary yomi/furigana rows on protagonist-selection and dialogue name UIs;
2. repeated short Japanese UI objects such as `はい`, date suffixes, `城`, and repeated `清洲` fields missed by unique-only matching;
3. the tested Matsudaira nameplate still appears without `쓰`, but this is no longer established as a compact-glyph rendering failure because the historical D5519 unique-only selector did not patch the duplicated `松平元康` fixed fields;
4. the earlier odd `케/자` shapes in `나야 스케자에몬` disappear in W0, but direct causality to the A1+ single-byte threshold family is not established because `케/자` are normal two-byte Korean codes;
5. currency format strings containing `貫/文`, which require format-object analysis rather than global replacement.

These are quality/coverage/runtime-behavior issues, not a recurrence of the old immediate freeze.

## 5. Yomi result

D5519 classification found 2,099 historical inline records whose original non-NUL bytes are entirely halfwidth kana `0xA1..0xDF`, leaving 3,420 non-yomi records.

Eight direct call sites set `mov w6,#1` before calls to shared name/yomi routine `0x45B0F8`:

```text
0x2A0ABC  0x2A565C  0x2A6F4C  0x2A7720
0x2A7FE4  0x2ADE5C  0x2BC1A0  0x2BD5C8
```

`Y0 v0.2l` restored the 2,099 internal yomi records to original Switch bytes and changed those eight enables to zero. Runtime remained stable, but the garbled small reading rows still appeared.

Therefore do not repeat the same eight-site-only suppression attempt. Preserve internal Japanese yomi for sort/comparison compatibility while the actual visible-row path is traced later.

## 6. Compact Korean mechanism — corrected transcription

PC T5K R9751/R9752 for `松平元康` use a 16-byte compact replacement:

```text
B2 BD AA F3 6B EE 93 20 EF 90 F5 E2 F2 7E F1 B8
```

Correct semantics:

```text
B2 = 마
BD = 쓰
AA = 다
F36B = 이
EE93 = 라
20   = space
EF90 F5E2 F27E F1B8 = 모토야스
```

The intended Korean display is **`마쓰다이라 모토야스`**. Earlier project text that called `BD` `츠` was a transcription error and is superseded.

Direct BC3 decoding of the exact Korean G1T confirms correct source glyph art for compact `마/쓰/다` and normal two-byte `케/자`. The source font is not the defect.

The PC runtime descriptor `font_page_limit` changes a threshold from `0xFF` to `0xA0`. Canonical closure keeps this as a raw compare-threshold fact only; do not describe it as a literal font-page-count assignment.

## 7. W0 result — observation retained, causality downgraded

W0 v0.2m adds six Switch equivalents of the PC A1+ half/fullwidth threshold:

```text
0x445EAC
0x445FC8
0x446198
0x4472E8
0x447344
0x447C44
```

Each changes:

```text
cmp w8,#0x100 -> cmp w8,#0xA1
```

Runtime on 2026-09-11:

- stable on the tested route;
- `나야 스케자에몬` renders `케/자` correctly in W0;
- the tested Matsudaira nameplate still lacks `쓰` visually.

These observations remain valid. However, do not claim that W0 directly fixed `케/자` through the A1+ single-byte threshold family, and do not use the Matsudaira result as proof that compact `BD=쓰` reached the renderer. The active-name data premise was not established.

## 8. W1 result — direct-cause hypothesis invalidated

Further disassembly found an additional text-render/layout gate at mapped `0x44D9D0`:

```text
and w8,w26,#0xffff
cmp w8,#0x100
b.hs 0x44D9E0
mov w19,#8
...
bl 0x44E400
```

W1 v0.2n changed only this compare on top of W0:

```text
mapped 0x44D9D0 : cmp w8,#0x100 -> cmp w8,#0xA1
Eden IPS 0x44DAD0
```

Artifact:

- `W1_Taiko5DX_KR_DBG_FONTWIDTH_RENDER_v0.2n.zip`
- SHA-256 `26fcd1434561b2e02d797079d6d996e5becfe66808e763d0b309ee1db10d44d1`
- W0 records 5,526 -> W1 5,527
- original-byte guard + IPS round-trip PASS.

Runtime on 2026-09-11: the tested Matsudaira nameplate still appears without `쓰`. Therefore the prior claim that `0x44D9D0` was the direct cause of the missing compact `쓰` is invalidated. The static width gate itself remains real, but its causal link to this symptom is not established.

Subsequent static inspection also found two corresponding Switch `松平元康` fixed fields at mapped `0x729D4D` and `0x729D5E`. The historical D5519 unique-only selector patched neither because the original pattern occurs twice. Therefore the earlier premise that an active compact `BD=쓰` byte was reaching the tested renderer was not established.

Do not repeat W1 as a compact-`쓰` fix without first establishing the actual active name-slot/data-selection path.

## 9. Repeated short-object recovery already established

Use actual Switch string objects, not every raw substring occurrence.

High-confidence targets:

- `はい` -> `예`: standalone object `0x6A15A5`, pointer ref `0x58D0D0`;
- `年/月/日` -> `년/월/일`: pooled objects `0x69785A / 0x68925A / 0x6A3CC6`, with consecutive pointer-table registration around `0x59C730..0x59C768`;
- `城` -> `성`: pooled standalone object `0x6A15DC`;
- `清洲` -> `기요스`: two fixed-field objects `0x6AE269`, `0x6AEFE9` with matching PC replacements.

Currency `貫/文` remains separate because many uses occur inside longer format strings.

Reproducible analyzer: `builder/repeated_token_probe.py`.

## 10. Fixed target identity

- Title ID `0100346017304000`
- Switch version `1.1.3`
- `main` Build ID `D9120950C258610A746F4A31CE3A3B376DE393D9`
- compressed main SHA-256 `b366e692208f3c0cc18bc1884ef95689b6b11d722fa2d749b8500abccbc3109b`
- mapped flat size `10,617,904 / 0xA20430`
- text `0x000000 + 0x58CE60`
- rodata `0x58D000 + 0x432018`
- data `0x9C0000 + 0x60430`

## 11. PC patch source facts

PC patch ZIP SHA-256 `df1b62de95e992369e9686c9731d814e7a7e4634888f610430635429e24f7cec`.

T5K121R: 10,036 mapping entries; 7,494 originals; 2,542 Korean additions; 17,103 inline records; 56 pointer records; 11 runtime descriptors.

The Drive `PC_Original/Taiko5DX.exe` is not the exact T5K target and must not be used for PC binary-context evidence. Exact target is Steam build 9163702, size 18,685,960, SHA-256 `10c69bab50d29baf6311360cafbf7383716a126a6484d209f5e299e12ab565a2`.

## 12. Encoding/font/conversion status

- Switch original font == Steam original: 13,108,628 bytes / 50 pages / SHA-256 `9c886848...a0083e`.
- Korean font: 16,779,036 bytes / 64 pages / SHA-256 `c82d80da...66932`.
- Normal Korean uses the custom two-byte game code; lead bytes `EB~F8` map to pages 49~62.
- PC patch additionally repurposes page-63 single-byte codes above `0xA0` for compact Korean glyphs in tight fixed fields.

Switch functions include `0x430350` UTF-16->game code, `0x4305D0` game code->UTF-16, `0x445C60` per-character decode, `0x445DE0` width selection, `0x446310` segmentation/count, and `0x446420` GetFontTexIndex.

The per-character JP decode around `0x445C60` accepts `0xA1..0xDF` as single-byte values, so compact `BD=쓰` is not discarded at basic decode. Both conversion loops still search only 7,494 mapping entries; expansion remains needed for full input/conversion behavior.

## 13. Validator role after D5519

The full 17,103-record validator remains a release-audit/recovery mechanism, not the primary explanation for the old freeze. It must recover missed repeated/string-pool/fixed-field mappings safely and audit late-game structural risk.

## 14. Priority after Canonical Closure

A fresh execution signal should start **Switch Functional Counterpart Survey**, not a build.

Survey order is functional rather than symptom-local:

1. mapping storage + every table-base/count consumer;
2. all 56 pointer records and replacement-object ownership;
3. page-mapper and byte-validation/copy semantic paths;
4. all 14 descriptor subpatch semantic counterparts;
5. inline/repeated/fixed-field/data-selection coverage.

CWTDAT is a separate data-port compatibility track.

Rules:

- do not use unique match as a Switch coverage gate;
- PC one-site behavior may fan out to multiple Switch sites;
- `NATIVE_EQUIVALENT` requires concrete Switch evidence, otherwise keep `UNSURVEYED`/`PARTIAL_EVIDENCE`/`UNRESOLVED`;
- treat the compact `쓰` symptom as three unresolved paths: data selection, pointer/reference selection, byte-validation/copy;
- space/capacity must be reported separately for mapping, pointer strings and any helper code need;
- PCREF1 delivery verification may run in parallel with static survey but must close before a new counterpart-derived runtime build is interpreted.

No implementation/build is authorized by this state update; after survey report, STOP and obtain a fresh user signal.

## 15. Eden Android / final distribution

Development builds must be installed through Eden's per-game Add-ons importer; direct normal file-manager access to Eden internal storage is not assumed.

Final frontend remains an Android APK using SAF. It accepts the user's complete extracted Switch v1.1.3 dump and PC patch ZIP and emits an Eden-ready mod without embedding copyrighted game binaries, patch payloads/fonts, keys, or dumps.
