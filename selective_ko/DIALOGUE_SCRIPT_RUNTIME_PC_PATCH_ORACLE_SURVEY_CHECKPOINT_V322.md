# DIALOGUE SCRIPT / RUNTIME PC PATCH ORACLE SURVEY CHECKPOINT — V322

Date: 2026-09-19 (KST)

Validation ID: `V322`

Parent canonical state:

`11dc8fac971d7f1a79496891d8c90663e0898b43` — V321 V320 body-only Eden diagnostic package materialization.

Status:

`CHECKPOINT CLOSED / READ ONLY / PARTIAL SURVEY / NO PRODUCT BYTES CHANGED / BROAD CALL-GRAPH TRAVERSAL STOPPED`

## 1. Purpose

V322 pivots the active investigation from B24-only layout work to the larger dialogue/script and shared text-presentation surface.

The checkpoint preserves all bounded evidence obtained before the user-requested STOP and explicitly prevents repeating the unbounded caller-graph traversal that stalled for more than one hour.

V322 does not implement, patch, build, serialize, package, or modify any game payload.

## 2. Investigation boundary

Investigated read-only:

- canonical PC Korean patcher v1.02 payload manifest and embedded payloads;
- EVENT / TS5 population and growth behavior;
- SNR0..SNR8 JP population and replacement-size behavior;
- Switch v1.1.3 `main` resource-name/resource-ID evidence;
- bounded EVENT and SNR resource-loader/consumer anchors;
- inherited TAI5MSG dialogue-formatter graph evidence;
- relationship to the open PC `description_font_* / ui_width_*` counterpart family.

Not completed:

- full EVENT/TS5 text-field grammar;
- full SNR field/record parser;
- complete EVENT caller graph;
- actual dialogue-window renderer caller binding;
- Switch-original RomFS EVENT/SNR byte-for-byte structure comparison.

## 3. PC_PATCH_ORACLE_GATE

`PASS`

Exact reconstructed PC Korean patcher v1.02 identity used in V322:

```text
bytes    177,267,850
sha256   109dc729e66df8cd0a47c5f6c24719260eb03a89890a0c69d3ba739145dcfb23
```

This identity was reconstructed from the canonical Drive split parts and matched `PATCHER_SHA256.txt`.

The embedded manifest exposed the same canonical data population already associated with V295:

```text
RomFS/data payload entries    208
EVENT/*.TS5                    169
SNR*_JP.TR5                      9
```

## 4. EVENT / TS5 actual PC patch behavior

Manifest-wide EVENT results:

```text
EVENT TS5 files                         169
patched size > original size         169 / 169
aggregate original bytes          3,347,984
aggregate patched bytes           4,085,204
aggregate growth                   +737,220
median per-file growth               +24.30%
```

Therefore PC EVENT localization is not a fixed-length replacement family.

Representative common-event manifest record:

```text
data/EVENT/ECF00000.TS5
original bytes    931,936
patched bytes   1,156,480
growth           +224,544
original sha256 bbaaff8dc552da17a49ea2e6ce49a76da662541ee22fdec7dc7933046430bf09
patched sha256  0899bf81789acfbd243d43be209a8a3960933fa090960ac8c753c63f95f07bbe
```

The patched `ECF00000.TS5` payload was successfully extracted from the exact v1.02 patcher during the V322 read-only survey.

The exact PC-original ECF00000 bytes are not currently materialized in the Drive PC_Original bundle; the original size/SHA above are manifest provenance and must not be represented as a separately inspected original file.

## 5. SNR actual PC patch behavior

The Drive PC_Original corpus contains JP/SC/TW SNR0..SNR8 files.

For the JP family, patcher manifest comparison established:

```text
SNR0_JP.TR5   174,788 -> 174,788
SNR1_JP.TR5   174,812 -> 174,812
SNR2_JP.TR5   174,797 -> 174,797
SNR3_JP.TR5   174,662 -> 174,662
SNR4_JP.TR5   174,575 -> 174,575
SNR5_JP.TR5   174,797 -> 174,797
SNR6_JP.TR5   174,464 -> 174,464
SNR7_JP.TR5   174,161 -> 174,161
SNR8_JP.TR5   174,599 -> 174,599
```

All nine preserve whole-file size.

Read-only diff inspection is consistent with the prior V295 correction: SNR is a mixed container containing narrative/scenario text and identity-related content. It must not receive one file-level selective disposition.

This checkpoint does not yet canonicalize a complete SNR field/record grammar.

## 6. EVENT and SNR are separate storage/consumer families

The PC evidence establishes materially different localization strategies:

```text
EVENT/TS5    variable-size script payload; all 169 patched files grow
SNR          fixed-whole-file-size mixed record container
```

Therefore:

- no common fixed-length replacement policy may be assigned to both;
- no common line-wrap rule may be assigned solely from container naming;
- SNR whole-file Korean import remains incompatible with the selective identity policy;
- EVENT capacity/layout work must allow for payload growth if Switch structure permits it.

## 7. Switch v1.1.3 resource evidence

Exact Switch `main` identity used:

```text
compressed NSO bytes   5,287,359
sha256                 b366e692208f3c0cc18bc1884ef95689b6b11d722fa2d749b8500abccbc3109b
```

Read-only resource-table analysis established the relevant JP resource IDs:

```text
SNR0_JP .. SNR8_JP     resource IDs 46 .. 54
ECF00000.TE5            resource ID 76
ECF00000.TS5            resource ID 77
```

EVENT TE5/TS5 resources are registered as a paired family.

The already-established common resource getter at `0x440A80` participates in both higher-level systems.

## 8. Bounded EVENT / SNR loader binding

The V322 bounded Switch analysis established:

### EVENT

A function in the `0x158A58` family searches the finite EVENT-key population and selects the language-specific TE5/TS5 resource pair.

For the JP common event, the TS5 side resolves to resource ID 77 and is loaded through `0x440A80`.

The TS5 consumer uses the file's leading count/offset-table structure before later event processing.

### SNR

A separate SNR consumer in the `0x287AB4` family selects JP resource IDs 46..54 by scenario and obtains the resource through the same `0x440A80` getter.

Disposition:

```text
common resource system     YES
same higher-level consumer NO / separate subsystems observed
```

This is sufficient to reject treating EVENT and SNR as one runtime carrier family.

## 9. Inherited TAI5MSG dialogue-formatter fact

The canonical PC original -> PC Korean block-0 formatter comparison remains binding:

```text
block-0 messages                         471
graph/control skeleton preserved     471 / 471
graph/control skeleton changed         0 / 471
content/output fragments changed         366
```

Therefore the PC Korean patch does not solve Korean dialogue by installing a new formatter graph for this family.

The missing-Switch-formatter-graph hypothesis remains rejected.

## 10. Relationship to current UI overflow evidence

User-supplied Eden screenshots after the B24 work show similar bottom overflow in non-B24 description panels, including 名所 and 称号 card descriptions.

This evidence is chat/runtime evidence only; the screenshots are not committed repository artifacts in V322.

Consequence:

- V315's excessive B24 hard-wrap was a real B24 data-layer defect;
- V320 remains a valid B24 data correction;
- B24 hard-wrap cannot explain all observed Korean text overflow;
- a broader runtime presentation family involving font/width/height/line-spacing remains open.

PC runtime descriptor evidence remains:

```text
ui_width_1            170 -> 200
ui_width_2            170 -> 200
ui_width_3            170 -> 200
ui_width_4            150 -> 200
description_font_1      5 -> 4
description_font_2      5 -> 4
```

The complete Switch semantic counterparts are not yet established.

## 11. 확정된 사실

1. The exact PC v1.02 patcher was reconstructed and SHA-guarded.
2. The PC patch contains 169 EVENT/TS5 payloads.
3. All 169 patched EVENT/TS5 files are larger than their original manifest sizes.
4. ECF00000.TS5 grows by 224,544 bytes in the PC patch.
5. SNR0..SNR8 JP all preserve whole-file size.
6. SNR remains a mixed narrative + identity-related container, not identity-only.
7. EVENT and SNR use different PC storage/localization strategies.
8. Switch resource IDs 46..54 bind SNR0..8 JP; IDs 76/77 bind ECF00000 TE5/TS5.
9. EVENT and SNR share the resource getter family but have separate higher-level consumers.
10. TAI5MSG block-0 Koreanization preserves the original formatter graph.
11. B24 hard-wrap does not explain all currently observed overflow symptoms.
12. No product bytes, code, builder, IPS, package, or runtime artifact were changed in V322.

## 12. 유력한 가설

- EVENT/TS5 is likely the major authored dialogue/event carrier for later selective Koreanization work, but exact field grammar and Switch-original structural parity remain open.
- Korean description/dialogue layout may require both source-data reflow and caller/runtime presentation corrections depending on UI family.
- PC `description_font_*` and `ui_width_*` patches may cover more than the B24 header family, but their exact Switch screen/caller mapping is not yet proven.
- The safest next dialogue investigation is to bind one already-known EVENT anchor to its immediate consumer/render path rather than enumerate the entire game's call graph.

## 13. 미확정 사항

- Switch-original EVENT/TS5 and SNR RomFS byte structures; the original RomFS bundle is not yet supplied.
- complete TS5 opcode/control/text-field parser;
- exact newline/page-break/choice semantics in ECF00000;
- complete SNR field and record schema;
- exact event-script -> visible dialogue-window call path;
- dialogue body pixel width, font selector, row height and page capacity;
- whether dialogue, B24 help, 名所 and 称号 descriptions share a common presentation descriptor family;
- exact Switch counterparts for the six PC `ui_width/description_font` descriptor edits.

## 14. 기각된 가설 / do-not-repeat

Rejected or superseded:

- `B24 hard-wrap = root cause of all Korean overflow`;
- `40 half-width units applies globally to every text caller`;
- `SNR is identity-only`;
- `EVENT/TS5 contains control only and no direct visible Korean payload`;
- `EVENT and SNR can use one storage/replacement strategy`;
- `find two Switch call sites using numeric font selector 5 and declare them description_font counterparts`;
- `PC Korean installs a redesigned TAI5MSG block-0 formatter graph`.

Operationally rejected:

- unbounded whole-subsystem caller/call-graph traversal.

The final broad EVENT caller search expanded beyond the intended anchors and remained without completion for more than one hour. No error code conclusively identified the internal cause, so this is recorded as an analysis-path failure/hang, not as a proven tool defect.

## 15. 관련 영향 범위

V322 changes only project knowledge/state documentation.

Unchanged:

- V320 TAI5MSG output and overlay;
- V321 diagnostic ZIP;
- Mapping 10,036;
- font and page mapper;
- EVENT/TS5 payloads;
- SNR payloads;
- ExeFS runtime code;
- non-B24 584 family;
- B24 header/title family.

V321 Eden runtime validation remains available but is no longer the active investigation priority.

## 16. 수정 제안 / exact next scope

After a new explicit execution signal:

`DIALOGUE_EVENT_TS5_ANCHOR_BOUNDED_CALLER_BINDING_READ_ONLY`

Binding limits:

1. start only from already-established EVENT anchors around `0x158A58`, resource getter `0x440A80`, and JP `ECF00000.TS5` resource ID 77;
2. trace at most one or two direct call levels per anchor before reporting;
3. enumerate finite direct callers/callees rather than recursively expanding the whole graph;
4. stop and report if the trace leaves the EVENT/text subsystem or exceeds the declared bounded node set;
5. do not analyze SNR in the same pass except as a comparison baseline;
6. do not modify code, payloads, builders, IPS, or packages;
7. do not start a diagnostic build.

Separate queued cause families remain:

- `B24_HELP_HEADER_PC_DESCRIPTOR_SWITCH_COUNTERPART_SURVEY_READ_ONLY`;
- non-B24 584 reflow;
- V321 V320 Eden runtime validation.

## 17. STOP boundary

V322 ends at this checkpoint.

The interrupted broad call-graph search is not to be resumed.

Any further caller binding, parser work, implementation, diagnostic build, or repository content change requires a fresh explicit user execution signal.
