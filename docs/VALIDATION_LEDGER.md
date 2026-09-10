# VALIDATION_LEDGER

Canonical record of validated, runtime-validated, superseded, invalidated, and still-unresolved facts.

## Operating rule

Do not repeat a well-recorded validation. Revalidation is allowed only when:

1. input file/version/hash changes;
2. new static/runtime evidence directly contradicts the record;
3. provenance is insufficient for the current high-risk decision;
4. the prior validation method is shown to be unsound.

A new chat/model/agent is never by itself a revalidation trigger.

When revalidation is required, perform it once and record validation ID/date, exact claim, input identity/hash/version, method/script/parameters, offsets/ranges/count units, result/status, and a reproducible artifact/report/commit path.

## Status values

- `VERIFIED`: direct evidence sufficiently recorded for reuse.
- `VERIFIED-RUNTIME`: directly observed in Eden/runtime; keep safety claims narrow to the tested route.
- `VERIFIED-LEGACY`: likely valid, but provenance is insufficient for a current high-risk decision.
- `NEEDS-REVERIFY`: conflicting/incomplete/external result that must be reproduced before canonical use.
- `INVALIDATED`: previous conclusion disproved.
- `SUPERSEDED`: historical fact/interpretation replaced by stronger evidence or policy.

## Current ledger

| ID | Claim | Status | Evidence / reuse rule |
|---|---|---|---|
| V001 | Fixed target is Switch v1.1.3, Title ID `0100346017304000`, main Build ID `D9120950C258610A746F4A31CE3A3B376DE393D9`. | VERIFIED | Builder hard-guards Build ID. Recheck only if target dump/version changes. |
| V002 | Mapped NSO layout is text `0x000000+0x58CE60`, rodata `0x58D000+0x432018`, data `0x9C0000+0x60430`. | VERIFIED | Builder hard-guards segment layout. |
| V003 | Switch original `FONT_JPN.G1T` equals Steam original; original SHA-256 `9c886848...a0083e`; Korean font SHA-256 `c82d80da...66932`; 50 -> 64 pages. | VERIFIED | Hash-guarded in builder. |
| V004 | T5K121R contains 10,036 mappings, 17,103 inline records, 56 pointer records, 11 runtime descriptors. | VERIFIED | Direct parse of `RT_RCDATA/101`; parser is `builder/t5k.py`. |
| V005 | Mapping counts are 7,494 original (`0x1D46`) + 2,542 Korean = 10,036 (`0x2734`). | VERIFIED | Direct T5K parse. Conflicting 7,334 claim is non-canonical. |
| V006 | Page-mapper rewrite at mapped `0x44650C` adds `EB~F8 -> pages 49~62`; correct Eden emitted offset is `0x44660C`. | VERIFIED | Static bytes/logic plus canonical IPS coordinate rule. |
| V007 | Historical selector: 17,103 records -> 8,713 unique original patterns -> 5,523 unique-rodata candidates -> 4 overlap skips -> 5,519 selected patterns covering 5,521 PC records. | VERIFIED | Reproduced with `builder/phase0_probe.py`; regression/reference only. |
| V008 | `unique exact match in rodata` alone is sufficient to classify a release-safe inline patch. | SUPERSEDED | Policy now requires structural/object evidence and offline validation. |
| V009 | Old v0.2b NO-INLINE booted and showed Korean title. | VERIFIED-RUNTIME | Observation is real but page-mapper IPS was `0x100` early, so do not use it to validate intended mapper execution. |
| V010 | Old A freezes; old B reaches title then crashes after input. | VERIFIED-RUNTIME | Historical observations only. Both used wrong IPS coordinates and cannot prove multi-fault/candidate safety. |
| V011A | Unique-match record pairs show strong monotonic structure: 6,053 pairs, global LIS 3,524, 2,529 outside; top runs 1,844/1,074/978/78. | VERIFIED | `builder/phase0_probe.py`; global LIS is evidence/reference, not hard gate. |
| V011B | 12,347/17,103 records have NUL in original and none in replacement; 4,747 originals have no NUL. | VERIFIED | Direct T5K scan; risk statistic only, not automatic run-on verdict. |
| V011C | External `430` cases are structurally confirmed termination failures. | NEEDS-REVERIFY | Fixed-input probe did not reproduce the stated unit/definition. Do not use 430 as a hard gate. |
| V011D | External `8,981 records / 1,242 patterns` are >=5-match counts. | NEEDS-REVERIFY | Fixed-input whole-flat probe gives different counts under the clearest definition. |
| V012 | Drive `PC_Original/Taiko5DX.exe` is not exact T5K target and cannot support PC-RVA neighborhood/XREF claims. | VERIFIED | Supplied: 18,479,304 bytes, SHA-256 `22e1cd1a...65ef6`; target: Steam build 9163702, 18,685,960 bytes, SHA-256 `10c69bab...65a2`. |
| V013 | Switch conversion functions still use mapping count 7,494 and have defined misses (`0x81A1`, `U+25A0`). | VERIFIED | Mapped main disassembly at `0x4303AC`, `0x430624` and miss paths. Expansion remains functionally needed, but not proven freeze cause. |
| V014 | Eden/Yuzu classic IPS for NSO uses a `0x100` NSOHeader prefix: emitted offset = mapped offset + `0x100`. | VERIFIED | Eden/Yuzu loader source path plus successful P0N2 control. |
| V015 | P0N v0.2f freezes. | VERIFIED-RUNTIME | User observed. It was not a true no-op because offsets were `0x100` early. |
| V016 | P0N v0.2f is a true no-op control in Eden. | INVALIDATED | Wrong coordinate model; P0N wrote bytes from `X` to mapped `X-0x100`. |
| V017 | P0N2 v0.2g is a true 5,519-record no-op control with corrected mapper/offsets. | VERIFIED | Artifact SHA-256 `1ccb27e7...7e8f6`; emitted IPS reparsed and mapped back successfully. |
| V018 | P0N2 boots, reaches Korean title, accepts input, reaches main menu. | VERIFIED-RUNTIME | User screenshot/runtime evidence. Proves large corrected classic-IPS/no-op path works on tested route. |
| V019 | M1A v0.2h real inline `R489` remains stable through scenario/protagonist flow. | VERIFIED-RUNTIME | `シナリオを選んでください` -> `시나리오를 선택하세요`, mapped `0x69B6A1`, emitted `0x69B7A1`. |
| V020 | D5519 v0.2k applies the historical 5,519 real replacements at corrected `+0x100` offsets and reaches normal early gameplay without freeze/forced exit. | VERIFIED-RUNTIME | User tested title -> menu -> scenario -> protagonist selection -> normal gameplay with screenshots. Artifact SHA-256 `46017206ed2679a645b1e0121aff6b7742fcbec94f41197e5f5681f517c9fae2`. This strongly attributes pre-P0N2 immediate freezes to the coordinate bug, but does not certify all late-game paths. |
| V021 | Of D5519's 5,519 real inline records, 2,099 target fields whose original non-NUL bytes are entirely halfwidth-kana `0xA1..0xDF`; 3,420 are non-yomi historical records. | VERIFIED | Reproduced against fixed mapped main by classifying each D5519 mapped record using original bytes. Reproducible builder: `builder/build_y0_noyomi.py`; analysis documented in `docs/POST_D5519_ANALYSIS.md`. |
| V022 | Eight direct call sites explicitly enable the auxiliary name-reading line with `mov w6,#1` before a `BL` to shared mapped routine `0x45B0F8`. | VERIFIED | Call-site offsets: `0x2A0ABC`, `0x2A565C`, `0x2A6F4C`, `0x2A7720`, `0x2A7FE4`, `0x2ADE5C`, `0x2BC1A0`, `0x2BD5C8`. Original bytes at all sites are `26 00 80 52`; nearby BL targets resolve to `0x45B0F8`. |
| V023 | D5519 garbled small name-reading line is consistent with translated halfwidth-yomi fields entering a Switch auxiliary-render path; Korean main names themselves render correctly. | VERIFIED-RUNTIME | User screenshots show the main Korean name readable while only the small auxiliary line is garbled. Internal-yomi preservation remains the preferred data policy. |
| V024 | Repeated short strings can be safely distinguished from substring collisions using object-boundary/pointer evidence. | VERIFIED | `builder/repeated_token_probe.py` and `docs/POST_D5519_ANALYSIS.md`: `はい` has 7 raw rodata matches but one standalone NUL object at `0x6A15A5`, pointer-ref `0x58D0D0`; pooled `年/月/日` objects are `0x69785A/0x68925A/0x6A3CC6`; pooled standalone `城` is `0x6A15DC`; PC replacements agree. |
| V025 | `清洲` repeated recovery has strong fixed-field evidence. | VERIFIED | T5K contains two `清洲\0\0` records with identical Korean replacement `기요스`; Switch has exactly two corresponding padded occurrences at mapped `0x6AE269` and `0x6AEFE9`, both in fixed-stride place-name/yomi tables. |
| V026 | Y0 v0.2l does **not** suppress the garbled auxiliary reading rows visible in protagonist selection and dialogue nameplates. | VERIFIED-RUNTIME | User tested Y0 alone on 2026-09-11 and supplied screenshots. The rows remain visible/garbled. V022's eight direct call-site mappings remain valid static facts, but the inference that those eight sites control the observed two screens is invalid/incomplete. Do not repeat the same eight-site-only suppression attempt. |
| V027 | PC T5K uses repurposed single-byte codes in the `0xA1..0xFF` range as compact Korean glyphs when a fixed field cannot fit the normal two-byte Korean spelling. | VERIFIED | T5K R9751/R9752 for `松平元康` use replacement bytes `B2 BD AA F3 6B EE 93 20 EF 90 F5 E2 F2 7E F1 B8`, where page-63 glyph cells `B2/BD/AA` are `마/쓰/다`, followed by normal two-byte `이라 모토야스`. The intended Korean display is `마쓰다이라 모토야스`. This explains how the 16-byte fixed record fits. |
| V028 | The source Korean G1T atlas contains correct glyph shapes for compact `B2=마`, `BD=쓰`, `AA=다` and normal two-byte `F568=케`, `F379=자`; the observed missing/odd characters are not caused by corrupt source glyph art. | VERIFIED | Direct BC3 G1T page/cell decode of the exact Korean font SHA-256 `c82d80da...66932`. Page 63 contains the compact single-byte glyphs; Korean lead pages contain `케/자` at the expected trail-index cells. |
| V029 | PC runtime descriptor `font_page_limit` changes a single-byte classification threshold from `0xFF` to `0xA0`, making codes above `0xA0` use the alternate/full-width path. | VERIFIED | Direct T5K runtime-descriptor byte semantics: PC code compares against `0xFF`; descriptor changes the immediate to `0xA0`. This is a halfwidth/fullwidth behavior patch, not a literal font-page-count patch. |
| V030 | Switch v1.1.3 has six semantically corresponding width/layout comparisons using `cmp w8,#0x100`; W0 changes them to `cmp w8,#0xA1` as a partial Switch equivalent of V029. | VERIFIED | Mapped sites `0x445EAC`, `0x445FC8`, `0x446198`, `0x4472E8`, `0x447344`, `0x447C44`; all original bytes `1F 01 04 71`, replacement `1F 85 02 71`. A separate `cmp #0x100` in conversion logic around `0x4304F8` is explicitly excluded. Reproducible builder `builder/build_w0_fontwidth.py`. Runtime observation is V031; do not infer compact-name causality from W0 alone. |
| V031 | W0 v0.2m is stable on the tested early-game route; `나야 스케자에몬` renders `케/자` normally, while the tested Matsudaira nameplate still visually lacks `쓰`. | VERIFIED-RUNTIME | User tested W0 alone on 2026-09-11 and supplied screenshots. The observations are retained. The earlier inference that W0 directly fixed `케/자` through the A1+ single-byte threshold family is downgraded: `케/자` are normal two-byte Korean codes and are not themselves direct A1+ single-byte targets. Likewise the Matsudaira observation does not by itself prove compact `BD=쓰` was present in the active source string. |
| V032 | A seventh text-render/layout decision exists at mapped `0x44D9D0`: codes `<0x100` take a width-8 path immediately before glyph construction/draw; W1 changes only this compare to `cmp w8,#0xA1` on top of W0. | VERIFIED | Disassembly around `0x44D9C4..0x44DA30`: `and w8,w26,#0xffff; cmp w8,#0x100; b.hs 0x44D9E0; mov w19,#8`, followed by the alternate table-width path and `bl 0x44E400`. This static control-flow fact remains valid. The prior causal claim that this gate was the direct cause of the missing compact `쓰` is invalidated by V033. |
| V033 | W1 v0.2n does **not** restore `마쓰다이라 모토야스` on the tested nameplate; the name still appears without `쓰`. Therefore mapped `0x44D9D0` is not the direct cause established by that symptom, and the W1 causal hypothesis is invalidated. | VERIFIED-RUNTIME | User runtime-tested W1 on 2026-09-11 and observed no restoration of `쓰`. Artifact identity remains `W1_Taiko5DX_KR_DBG_FONTWIDTH_RENDER_v0.2n.zip`, SHA-256 `26fcd1434561b2e02d797079d6d996e5becfe66808e763d0b309ee1db10d44d1`. Static inspection performed before this record also found two corresponding Switch `松平元康` fixed fields at mapped `0x729D4D` and `0x729D5E`; the historical D5519 unique-only selector patched neither because the original pattern is duplicated. Thus the earlier premise that an active compact `BD=쓰` byte was reaching this renderer was not established. Do not repeat W1 as a compact-`쓰` fix without first establishing the actual active name-slot selection/data path. |

## Reproducible fixed input identity

- Switch compressed `main` SHA-256: `b366e692208f3c0cc18bc1884ef95689b6b11d722fa2d749b8500abccbc3109b`;
- mapped flat size: `10,617,904 (0xA20430)`;
- PC patch ZIP SHA-256: `df1b62de95e992369e9686c9731d814e7a7e4634888f610430635429e24f7cec`;
- embedded `dinput8.dll` SHA-256: `ffe7e9da8e00c96bec631b45a3e9c4d3f314551623351f3e7024e0318913c6b7`;
- `RT_RCDATA/101` SHA-256: `5c6f4eba8c6f0516365e4518f27e9d8c840aead463b5a2938dd1e08b99726d29`.

Do not hand-recount established Phase-0 figures in later chats. Use `builder/phase0_probe.py`, `builder/repeated_token_probe.py`, and the ledger.

## Current precedence

- release inline safety policy: `docs/INLINE_VALIDATION_POLICY.md`;
- validated fact/revalidation authority: this ledger;
- corrected-runtime observations: `docs/RUNTIME_TEST_RESULTS.md`;
- D5519/yomi/repeated-object/font-width analysis: `docs/POST_D5519_ANALYSIS.md`;
- current resume point: `PROJECT_STATE.md`.

When a new result changes a canonical fact, update this ledger in the same work session as the affected state/runtime/changelog documents.