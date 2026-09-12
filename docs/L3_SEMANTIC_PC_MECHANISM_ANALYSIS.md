# L3 semantic/context and PC-mechanism analysis

Date: 2026-09-13  
Status: SEMANTIC REVIEW COMPLETE / MATERIALIZED OVERLAY / NO SWITCH WRITE AUTHORIZATION

## 1. Summary

This analysis consumes the already-canonical L3 population and does not re-partition forward localization.

Parent family:

```text
L3_JP_PREFIX_OF_LONGER_OBJECT = 88
```

Canonical parent identity:

```text
ordered source-ID SHA-256  b4c9af9ba3640634121c757c5585ece80d4e230533b24f6b2d81f4aebff714b2
ordered R-ID SHA-256       36d433243692ef53f8f36c27145a9f5d58b14c2d030e871d888bb5dc363e2434
```

The 88 rows close into five mutually-exclusive semantic/context dispositions:

| disposition | rows |
|---|---:|
| `PARTIAL_COMPOSITE_WINDOW` | 31 |
| `FORMATTER_CONTROL_PREFIX` | 22 |
| `CONTEXT_DIVERGENT_FALSE_PREFIX` | 17 |
| `STANDALONE_MEANINGFUL_PREFIX` | 13 |
| `UNRESOLVED` | 5 |
| **total** | **88** |

No Switch write is authorized by this analysis. The first four sets are semantic-review dispositions, not terminal port actions. The remaining five rows are the only L3 rows that still require targeted consumer/XREF tracing after this review.

Machine-readable overlay:

- `data/post_freeze/l3_semantic_pc_mechanism_v1/INDEX.json`
- `data/post_freeze/l3_semantic_pc_mechanism_v1/DISPOSITIONS.json`
- `data/post_freeze/l3_semantic_pc_mechanism_v1/MECHANISMS.json`
- INDEX SHA-256: `dd2ad754732d16dc05263a674c8b76d494f98baf09d71dd3c1ae2f3b1d56a33e`

## 2. Fixed evidence and method

The analysis reuses the canonical L3 membership and fixed evidence identities. No L1/L2 structural question was reopened.

Primary evidence:

- forward-localization partition INDEX SHA-256 `6d79c648b4ee671aa4c0592467b89101de76456a5493ffaadb743014a74fdc76`
- Stage-1 report ZIP SHA-256 `0643bf1aed4cc014c980255caa58535ef5f06ecb4979549fdd6d77f40a84c463`
- Stage-1 source ledger SHA-256 `0ef81c629adb2e348a72922efcb030908c76fb3cff964804948bf84cd7fd1570`
- PC patcher ZIP SHA-256 `df1b62de95e992369e9686c9731d814e7a7e4634888f610430635429e24f7cec`
- embedded `dinput8.dll` SHA-256 `ffe7e9da8e00c96bec631b45a3e9c4d3f314551623351f3e7024e0318913c6b7`
- `T5K121R` SHA-256 `5c6f4eba8c6f0516365e4518f27e9d8c840aead463b5a2938dd1e08b99726d29`
- Switch `main` SHA-256 `b366e692208f3c0cc18bc1884ef95689b6b11d722fa2d749b8500abccbc3109b`

Evidence order used:

```text
Switch structure
-> actual PC occurrence mechanism
-> PC replacement/context
-> Switch JP neighborhood
-> linguistic/semantic role
-> consumer tracing only when ambiguity remains
```

This is the same working order previously used on L1. L3 is an independent structural family and therefore serves as a counterexample test of methodology reuse.

## 3. Exact semantic/context dispositions

### 3.1 `PARTIAL_COMPOSITE_WINDOW` — 31

These rows are best explained as PC occurrence windows that intentionally cover only part of a larger displayed/logical object, including name/yomi fragments and other composite rewrites.

```text
R472, R1744, R1840, R1861, R1871, R1953, R1956, R1957,
R1960, R1989, R1992, R1998, R2000, R2002, R2005, R2016,
R2023, R2028, R2033, R2037, R2039, R2041, R2049, R2053,
R2057, R2061, R2071, R2073, R2280, R2745, R3101
```

Ordered source-ID SHA-256: `2a9df9c57d066e808d7cf4a7ac52479554fc5d2378c95e7d71a20a91d287501b`  
Ordered R-ID SHA-256: `261959556a24dbc8aec570c84fe0fd23727806097574baef51a8991e92918272`

### 3.2 `FORMATTER_CONTROL_PREFIX` — 22

These rows behave as formatter/control/debug prefixes or structured label components. Their prefix relation is useful context evidence but is not a direct target-selection rule.

```text
R67, R802, R968, R1047, R1049, R1087, R1096, R1123,
R1156, R1189, R1192, R1194, R1295, R1383, R1492, R1495,
R1498, R1504, R1516, R1519, R2087, R2863
```

Ordered source-ID SHA-256: `159be03c38b0ed492634566b79024783480977b2843ce92d76cbf211255b977f`  
Ordered R-ID SHA-256: `371189a674a6f62cf191cf7a09fc6c77d0feefeec7f933059c8c2c9c0e47fe4a`

### 3.3 `CONTEXT_DIVERGENT_FALSE_PREFIX` — 17

The byte-prefix relation is real, but PC occurrence context shows a different semantic use. These rows are counterexamples to value/prefix-only target binding.

```text
R55, R214, R281, R486, R643, R1996, R2114, R2292,
R2300, R2301, R2302, R2303, R2558, R2563, R2769, R2770,
R16452
```

Ordered source-ID SHA-256: `33a36fa8e83579c252f4dfd53e4b046be3dd7dd022afb2387701032e413d047f`  
Ordered R-ID SHA-256: `702c245e0b9bc1e734cd4f12fafc9d281e67269d53c98bf7e59f8aff0c1c61a5`

### 3.4 `STANDALONE_MEANINGFUL_PREFIX` — 13

The PC occurrence is independently meaningful, while Switch localization exposes longer objects beginning with the same text. The shared prefix therefore does not by itself establish owner binding.

```text
R79, R1593, R2124, R14690, R14700, R14702, R14704,
R14706, R14711, R14733, R14734, R14735, R14736
```

Ordered source-ID SHA-256: `42b8c28029c92e0c93f4f739c4e77b46c4a8b3cc1c7824926b699edea78a180b`  
Ordered R-ID SHA-256: `3129e2d111b9abc025af2bac239e012b71c4ee6e116a8fcb1f4b02ee0079d13f`

### 3.5 `UNRESOLVED` — 5

Current Switch structure, PC occurrence mechanism, PC replacement/context, and Switch neighborhood do not close these rows. Targeted consumer/XREF tracing is justified for these five only.

```text
R651, R1062, R1277, R1283, R1284
```

Ordered source-ID SHA-256: `960e87c362400ab1da36036327c26cca4f26781dfaf15de754edcf9db717c38a`  
Ordered R-ID SHA-256: `0236907c9c3867ee6284aacafbcd958f0e57c3921cb74d4f9680c505c0c986d1`

## 4. PC mechanism observations

All 88 L3 rows are represented by the PC inline layer. Cross-check against the inherited exhaustive 56-record pointer population found zero L3 pointer-linked rows.

```text
L3 inline rows                         88
pointer-linked L3 rows                  0
PC pointer population checked          56
inherited pointer modes       mode0=5 / mode1=51
```

This is a PC mechanism observation only. It does not authorize in-place Switch writes.

### 4.1 Inline windows can split a CP932 multibyte character

Seven PC originals terminate inside a multibyte CP932 character:

```text
R472   96bc914f82
R1156  8ee596bd82
R1383  835283938365836983
R1744  82e682ed82d982
R1861  82ad82eb82
R2745  82b182cc835a815b83758366815b835e82
R3101  906591
```

Therefore a PC inline-record boundary is not necessarily a character boundary, C-string boundary, or semantic-object boundary. This directly rejects any rule that treats every inline record as one complete text object.

### 4.2 Full-zero suppression occurs inside composite rewrites

```text
R486  original 82b382a2 -> replacement 00000000
R643  original 82b382a2 -> replacement 00000000
```

Both are `さい` occurrences reviewed in a larger `ください`-type composite context. Zero replacement here is evidence of occurrence-specific composition, not automatic deletion semantics for standalone `さい`.

### 4.3 Translation plus trailing zero padding

```text
R1277  replacement f1b8f5a7ef52f64d0000
R1284  replacement efddf0fbf1c20000
R2558  replacement f15900000000
```

Same-length PC inline records can therefore encode translated prefix bytes followed by zero padding.

### 4.4 Same original, different replacement

Four L3 rows form two same-original/nonuniform-replacement groups:

```text
登録武将: R802 / R2087
発生条件: R1283 / R1284
```

`R802` and `R2087` are especially useful because PC occurrence neighborhood and Switch localization neighborhood distinguish the two uses even though the Japanese original is identical. This independently confirms the L1 finding that Japanese value equality is not a semantic owner key.

`R1283` and `R1284` remain unresolved because the exact target PC EXE is unavailable for whole-program XREF/call-site naming and the two occurrences carry intentionally different replacements.

## 5. Representative semantic counterexamples

### 5.1 `R214 前`

The PC occurrence is part of a composite `名前` rewrite rather than the semantic object represented by Switch strings beginning with standalone `前`. Therefore a mechanically correct strict prefix can still be a false semantic binding.

### 5.2 `R486 / R643 さい`

Both occurrences are fully zeroed as components of a larger PC rewrite, while Switch strict-prefix candidates include unrelated longer yomi strings. This rejects `strict prefix -> same object` and `zero replacement -> delete this semantic word` shortcuts simultaneously.

### 5.3 `R802 / R2087 登録武将`

The two PC occurrences have different Korean replacements and different source neighborhoods. Their corresponding Switch neighborhoods also separate two longer formatter objects. Occurrence context can therefore resolve a replacement-conflict pair without treating the Japanese value globally.

### 5.4 standalone-prefix group

Rows such as `国主`, `頭領`, `武家`, `職人`, `医師`, and `風邪薬` are meaningful PC strings in their own right, while Switch localization contains longer strings beginning with those bytes. Linguistic plausibility of the prefix is not sufficient owner evidence.

## 6. Unresolved rows and next justified tracing scope

Only five L3 rows remain unresolved after structural/context review:

- `R651`: PC composite/range formatting does not map cleanly to one longer Switch formatter object; version/object variation remains plausible.
- `R1062`: PC `ＯＲ調査` occurrence appears formatter-like, but available Switch strict-prefix objects do not establish one owner.
- `R1277`: `スクリプト` has multiple longer Switch objects and PC context does not uniquely select one.
- `R1283`, `R1284`: same original `発生条件` has two deliberately different PC replacements; exact target-build XREF/caller evidence is unavailable.

Consumer tracing is therefore narrowed from 88 rows to these five. Any future tracing scope should remain read-only unless separately authorized.

## 7. Rejected hypotheses

L3 independently rejects the following shortcuts:

1. `strict prefix -> same semantic object`.
2. `one PC inline record -> one complete character/string/semantic object`.
3. `replacement conflict -> target cannot be distinguished`.
4. `zero replacement -> semantic deletion of that standalone text`.
5. `all L3 rows require consumer-by-consumer tracing`.
6. `PC inline mechanism match -> equivalent Switch write is authorized`.

The inherited rejections from L1 remain in force: language alone, raw value equality, replacement agreement, or unique value matching cannot independently authorize a Switch target/write.

## 8. Methodology result

The working evidence order survived a second independent residual family. It reduced 88 L3 rows to 83 reviewed coarse dispositions plus five true tracing candidates without starting consumer tracing from every row.

This materially supports reusability of:

```text
Switch structure
-> PC actual occurrence/mechanism
-> PC replacement/context
-> Switch logical neighborhood
-> semantic role
-> consumer tracing only when needed
```

This is sufficient evidence to consider a future framework-promotion review, but this analysis does not modify `docs/PC_TO_SWITCH_PORTING_RULE_FRAMEWORK.md`. Framework promotion requires a fresh user signal and a separate review scope.

## 9. Boundary

This record does not:

- authorize any of the 88 rows for Switch write;
- modify the builder, IPS, runtime, or game files;
- reconstruct historical 467/451/797 membership;
- reopen L1/L2 structural results;
- claim exact target-PC whole-program XREFs without the Steam 1.2.1.0 build 9163702 EXE.

The analysis scope ends here.
