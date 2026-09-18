# TAI5MSG B24 Native-Wrap Layout Reconstruction Implementation / Offline Validation — V320

Date: 2026-09-18 (KST)

Validation ID: `V320`

Parent canonical state:

`8b8940ce13f90099730fbef106c44a07d0a2d531` — V319 B24 native-wrap layout reconstruction design.

Status:

`CLOSED / IMPLEMENTED / OFFLINE BYTE-EXACT VALIDATED / DRIVE ROUNDTRIP VERIFIED / NO PACKAGE / NO EDEN RUNTIME`

## 1. Scope

V320 implements the V319 body-only contract for the full 108-row B24 layout population.

Explicitly excluded:

- B24 help-header/title runtime descriptor changes;
- non-B24 584-row reflow;
- IPS modification;
- package/ZIP materialization;
- Eden/runtime execution;
- unrelated translation cleanup.

## 2. Overlay architecture

V315 remains immutable historical/semantic authority.

V320 is a chained overlay:

```text
canonical PC-KO TAI5MSG
  -> V315 109-row correction
  -> V320 108-row native-wrap body correction
```

V320 source identity:

```text
V315 intermediate bytes   1,840,073
V315 intermediate sha256  b212da65010d3a2e7ff6f7b8e10ce57371cb67e3093f58a6ad16a085399a8d0d
```

V320 excludes M228 because M228 is V315 semantic/title-only and is not one of the 108 layout-collapsed rows.

## 3. Machine-readable artifact

`selective_ko/artifacts/tai5msg_b24_native_wrap_layout_correction_v1/INDEX.json`

`selective_ko/artifacts/tai5msg_b24_native_wrap_layout_correction_v1/ROWS.jsonl`

Transport identity:

```text
rows      108
bytes     195,031
sha256    f23ece9f76b992abeba57f613975bcc6161c2bb6a46de7f8b9fc5c0887930abe
```

All rows use `EXACT_REPLACE_MESSAGE`.

## 4. Binding runtime-layout guards encoded in builder

The production serializer now fails closed unless every V320 row satisfies:

- exact V315 intermediate source-message bytes and SHA;
- locator set equals V315 layout population exactly;
- no M228 V320 row;
- semantic/control non-layout signature preserved;
- terminal `05 05 05` preserved;
- every authored line <= 52 half-width units;
- every message <= 12 authored/visible rows under the V319 simulation contract.

V320 does not execute a heuristic reflow at runtime/build time. The exact reflowed target bytes are stored in the overlay.

## 5. Offline output identity

The V319 prospective output identity was reproduced exactly.

```text
output bytes    1,839,753 / 0x1C1289
output sha256   fd4c8b9f527f67f667d5fded6bdb4703607b70e8b6addf1f41c5d11ebf93e85c
growth          0x70C0
B24 used_end    0xEB7C
B24 declared    0xEB80
B24 growth      0x0780
B32 offset      0x1B4840
B32 used_end    0xB8D5
```

Therefore the former V319 SHA is promoted from design projection to the V320 canonical offline output identity.

## 6. Full-population validation

Independent byte-level validation established:

```text
blocks                         33
messages                       14,832
changed from V315             108
changed outside B24              0
M228 changed from V315           0
15 untouched B24 rows changed    0
max line width                 52
max visual rows                12
rows > 52                       0
rows > 12                       0
semantic non-layout drift       0
runtime block capacity        PASS
```

The three shared decorative-blank normalizations are exactly:

`M221 / M257 / M320`

## 7. Mapping/code census

The body reflow changes only layout whitespace/newline placement.

Expected selected-population census after V320:

```text
unique two-byte codes          1,011
two-byte occurrences         225,719
unique Korean-added codes        992
Korean-added occurrences     219,210
```

Hangul occurrence count is unchanged from V315.

The reduction in total two-byte occurrences is caused by removal of redundant full-width indentation/layout spaces, not semantic glyph loss.

## 8. Generic-overlay replay

The V320 artifact was independently loaded through the repository's existing generic correction utility and applied to the exact V315 intermediate messages.

Result:

`PASS_BYTE_IDENTICAL`

The generic-utility replay produced the same final SHA-256:

`fd4c8b9f527f67f667d5fded6bdb4703607b70e8b6addf1f41c5d11ebf93e85c`

## 9. Drive validation artifacts

Path:

`Google Drive/GPT/태합입지전/V320_B24_NATIVE_WRAP_VALIDATION/`

Folder ID:

`1O5lG7P8rcSDo7OfUKrZBx3E1p9Heiji3`

Files:

```text
TAI5MSG_V320_B24_NATIVE_WRAP.DAT
  id      1Q6hfQ7HNKBrziaWIER_PtlmFz0JvVKrV
  bytes   1,839,753
  sha256  fd4c8b9f527f67f667d5fded6bdb4703607b70e8b6addf1f41c5d11ebf93e85c

V320_B24_NATIVE_WRAP_VALIDATION.json
  id      1f2nqDwMHcQ46q6t4-SAoKNQ2eBurAzJL
  bytes   16,678
  sha256  8ce6b03176067c5c35d9ca75328be8dfde0e1fea3dad9c4451ce7a369edf818a

INDEX.json
  id      1T39agvzHcOrxim6jZddYfP5P32TSohJq
  bytes   1,087
  sha256  9b5f897eca2937b7ddb6f5640ede2f0cb36d2caa5989a625cee436a8efd09132

ROWS.jsonl
  id      1TCMgGoELjhCM0LNnY-mfGivTVnT1Q4GP
  bytes   195,031
  sha256  f23ece9f76b992abeba57f613975bcc6161c2bb6a46de7f8b9fc5c0887930abe
```

All four files were downloaded back from Drive and matched their pre-upload SHA-256 exactly.

## 10. 확정된 사실

1. V319's prospective SHA and all projected structural values were reproduced exactly.
2. V320 changes exactly 108 B24 layout messages relative to V315.
3. M228 remains byte-identical to the V315 semantic/title correction.
4. M227 and M229 semantic corrections remain present while their body layout is reflowed.
5. All 15 untouched B24 control rows remain byte-identical to V315.
6. All non-B24 messages remain byte-identical to V315.
7. All V320 rows satisfy <=52 units and <=12 rows.
8. Generic correction utility replay is byte-identical to the independently generated V320 DAT.
9. No IPS, package, ZIP or runtime change is part of V320.

## 11. 유력한 가설

The V320 body-only TAI5MSG should remove the V317 long-body overflow in Eden without requiring renderer/font/Mapping changes.

This remains a runtime hypothesis until an isolated V320 diagnostic package is executed.

## 12. 미확정 사항

- Eden visual result for V320 long-body representatives;
- physical Nintendo Switch / Atmosphere behavior;
- independent B24 help-header/title counterpart fix.

## 13. 기각된 가설

V320 retains the V318/V319 rejections:

- 40-unit B24 hard-wrap;
- patching only visibly overflowing rows;
- translation shortening;
- mixing the header/title runtime family into the body fix.

## 14. 관련 영향 범위

Changed production path:

- V320 exact correction artifact;
- selective TAI5MSG serializer overlay chain;
- serializer postconditions/tests.

Unchanged:

- V303 membership 3,179;
- V304 corrections;
- V315 historical artifact;
- Mapping 10,036;
- page mapper;
- font;
- ExeFS IPS;
- non-B24 584;
- B24 help-header runtime code.

The V317 package is stale after V320 because it contains the V315 TAI5MSG.

## 15. 수정 제안 / exact next scope

After a fresh explicit execution signal:

`TAI5MSG_B24_V320_EDEN_DIAGNOSTIC_PACKAGE_MATERIALIZATION`

That scope may materialize only the V320 body-layout TAI5MSG into the existing four-file Eden diagnostic package route, perform deterministic rebuild and Drive roundtrip, then stop before runtime execution.

The queued independent header scope remains:

`B24_HELP_HEADER_PC_DESCRIPTOR_SWITCH_COUNTERPART_SURVEY_READ_ONLY`

Do not combine the header fix with the V320 body diagnostic package.

## 16. Repository write boundary

Any repository write remains restricted to:

`create_blob -> create_tree -> create_commit -> update_ref(force=false)`
