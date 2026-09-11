# PCREF1 delivery verification

Date: 2026-09-11
Status: ARTIFACT_INSUFFICIENT / STOP

## 1. Scope

This stage verifies only whether the historical `PCREF1` diagnostic can be trusted as an emitted-IPS delivery test. It does not create or modify any IPS, builder, ARM64 code, Switch counterpart, or runtime diagnostic.

The question is deliberately narrow:

> Did the historical PCREF1 artifact actually contain the intended inline/repeated-object writes at the correct Eden IPS coordinates with the intended payload bytes?

## 2. Historical PCREF1 reconstruction

The only surviving description of PCREF1 is a conversation-level reconstruction, not a retained build artifact.

PCREF1 was described as a clean PC-reference-derived **inline-only** build rather than a cumulative W1 build. Its intended scope was approximately 14,544 PC inline instances and explicitly included objects that the historical unique-only selector had skipped, including:

- duplicated `松平元康` fixed fields at mapped `0x729D4D` and `0x729D5E`;
- `年/月/日`;
- `はい`;
- `城`;
- repeated `清洲` objects.

It did **not** include the PC pointer-56 layer, 10,036 mapping relocation, or 11-descriptor runtime code layer. The reported runtime observation was no visible screen change.

This description is useful for intent only. It is not sufficient to prove what the emitted IPS actually contained.

## 3. Retained evidence that still exists

Independent static evidence predating PCREF1 remains canonical:

- V014: Eden/Yuzu classic IPS uses `emitted offset = mapped offset + 0x100`.
- V024: repeated short objects are structurally identified, including `はい` at mapped `0x6A15A5`, `年/月/日` at `0x69785A / 0x68925A / 0x6A3CC6`, and `城` at `0x6A15DC`.
- V025: two padded `清洲` fixed fields are established at mapped `0x6AE269` and `0x6AEFE9`.
- V033: duplicated `松平元康` fixed fields exist at mapped `0x729D4D` and `0x729D5E`; D5519 did not patch them because the historical selector required uniqueness.

These facts identify intended Switch objects. They do not prove PCREF1 emitted records for them.

## 4. Artifact search result

The actual PCREF1 ZIP/IPS could not be recovered from the canonical sources available to this verification session.

Checked sources:

1. repository `fsmkh1-crypto/Taiko5DX-Switch-Korean-Port` current source/history/search context: no retained PCREF1 build artifact, manifest, SHA record, or reproducible PCREF1 builder was found;
2. Google Drive project folder `태합입지전 포팅`:
   - `Eden_Builds/` is empty;
   - `Test_Results/` is empty;
   - no file named `PCREF1`/`PCREF` was returned by Drive search;
3. ChatGPT File Library search for `PCREF1`, `PC-reference clean`, `14544`, W1/DIRECT1-related terms: no PCREF1 artifact was found.

The absence claim is limited to the sources accessible in this session. It does not claim that no copy exists on the user's local device or another external location.

## 5. Missing provenance

The following required evidence is not retained:

- PCREF1 ZIP;
- emitted `.ips` file;
- artifact SHA-256;
- final IPS record count;
- build manifest / intended-record list;
- original-byte guard PASS/SKIP counts;
- per-record mapped and emitted coordinates;
- emitted payload bytes;
- IPS round-trip report;
- EOF-collision handling result;
- exact builder source/commit that produced PCREF1.

Therefore the requested reverse parse cannot be performed on the historical artifact.

## 6. Checks that cannot be completed

Without the emitted IPS, this stage cannot establish:

- whether the intended object records were present at all;
- whether mapped offsets were serialized as `mapped + 0x100`;
- whether any original-byte guard skipped the intended records;
- whether the actual payload matched the PC Korean replacements;
- whether the two `松平元康` fields were both emitted;
- whether `はい`, `年/月/日`, `城`, and both `清洲` objects were emitted;
- whether an offset/serialization/EOF issue truncated or redirected records;
- whether the package tested at runtime was the package described as PCREF1.

## 7. Final verdict

**PCREF1 delivery status: ARTIFACT_INSUFFICIENT.**

The historical runtime observation "PCREF1 produced no visible change" is retained only as an observation. It is **not valid negative evidence** against V024/V025 object correspondence or against the duplicated fixed-field findings, because the prerequisite fact "the intended bytes were actually present in the tested emitted IPS" is not established.

Accordingly, PCREF1 must not be used to conclude that:

- the game does not read the established repeated objects;
- the repeated/fixed-object family is semantically irrelevant;
- the mapped object locations are wrong;
- the PC replacements are ineffective on Switch.

Those conclusions remain unresolved until a reproducible delivery-controlled diagnostic is separately authorized and tested.

## 8. Feedback-loop consequence

The feedback loop is **not yet restored** by this verification. The correct next runtime gate, if later authorized, is a fresh reproducible delivery-control diagnostic with:

- one root-cause family only;
- explicit intended-record manifest;
- original-byte guard report;
- emitted IPS reparse/round-trip;
- `mapped -> emitted (+0x100)` table;
- artifact SHA-256 and record count;
- retained downloadable artifact or reproducible builder output.

A future new artifact would validate the current pipeline; it would not retroactively prove what the lost PCREF1 artifact contained.

## 9. Work explicitly not performed

This stage did not:

- reconstruct PCREF1 by guesswork;
- create a replacement PCREF1 build;
- modify builder logic;
- patch repeated objects;
- investigate `쓰` further;
- begin the five-axis Switch counterpart survey;
- create IPS/build files;
- perform Eden runtime testing.

STOP.
