# SELECTIVE PROJECT STATE

Date: 2026-09-18 (KST)
Status: V297 INLINE R1 LOGICAL-OBJECT RECONSTRUCTION MATERIALIZED / ENDING-HELP 39 CANDIDATE STAGE NOT STARTED / NO BUILD
Track: `SWITCH_SELECTIVE_KOREANIZATION`

## 1. Resume authority

Repository: `fsmkh1-crypto/Taiko5DX-Switch-Korean-Port`
Branch: `main`
Target: Nintendo Switch title `0100346017304000`, game v1.1.3.

This file is the sole executable next-scope authority for the selective product track.

The repository-root `PROJECT_STATE.md` is the sole repository-level resume authority and routes selective work here.

All earlier VERIFIED/CLOSED facts are inherited unless explicitly corrected by V295, narrowed by V296, or superseded by the V297 inline logical-object overlay.

Required reads, in authority order:

1. `INLINE_R1_LOGICAL_OBJECT_RECONSTRUCTION_AND_REUSABLE_RULES_V297.md`
2. `LEGACY_EVIDENCE_CLAIM_STRENGTH_POLICY_V296.md`
3. `CONTENT_CONTAINER_FIELD_AVAILABILITY_CORRECTION_V295.md`
4. `IDENTITY_IN_PROSE_POLICY.md`
5. `CLASSIFICATION_SCHEMA.md`
6. `SCRIPT_TAXONOMY_AND_CROSSCUTTING_RULES.md`
7. `KNOWN_FAILURES.md`
8. `SWITCH_ORIGINAL_SOURCE_INPUT_CONTRACT.md`
9. `ARCHITECTURE.md`
10. this file

## 2. Product / authority boundary

The product remains selective Koreanization, not a full clone of the PC patch.

Priority release scope:

- UI/help/descriptive text;
- structurally safe narration/system/event text;
- structurally safe dialogue.

First-release Japanese/deferred scope remains:

- dedicated person/place identity fields;
- yomi/readings/sort keys;
- surname/given-name composition;
- date/calendar identity presentation;
- Korean name entry;
- unresolved dynamic grammar/formatter dialogue.

Authority remains:

```text
PC Korean content/terminology        -> SOURCE_AUTHORITY
Switch structure/owner/caller        -> STRUCTURAL_AUTHORITY
verified Switch mapping realization  -> SWITCH_RUNTIME_AUTHORITY
known-good PC visible result         -> SEMANTIC_ORACLE
PC runtime mechanism                 -> REFERENCE_OR_HINT
```

## 3. Identity policy remains closed

```text
identity presentation fields          -> KEEP_JP
PC Korean prose identity literals      -> PRESERVE_AS_AUTHORED_KO
runtime-inserted person/place identity -> KEEP_JP
reverse-substituting prose names       -> FORBIDDEN
```

## 4. V297 inline logical-object result

Canonical overlay:

`INLINE_R1_LOGICAL_OBJECT_RECONSTRUCTION_AND_REUSABLE_RULES_V297.md`

Current counts:

```text
PC inline raw records                       17,103
exact source/replacement groups             8,751
external provisional YES                    205
external provisional UNCERTAIN              227
Korean-bearing positive groups              204
positive source occurrences                 206
single Switch-location occurrences          191
those collapse to logical objects           189
positive multi-match groups                 13
```

External semantic triage is a prefilter only and must not be used directly as R1 corpus authority.

## 5. Ending-table / ending-help result

Switch ending table:

```text
39 records
stride       = 0x3FF / 1023 bytes
help offset  = +0x15
narration    = +0x20A
field sizes  = title 21 / help 501 / narration 501
```

The table contains 117 text fields.

PC patch coverage:

```text
full ending-table inline records = 208
help-field inline records         = 102
original-byte mismatches          = 0
affine relative-offset violations = 0
```

All 39 help fields have complete Korean payload reconstruction and current source/route classification:

```text
usage_class      = UI_DESCRIPTION
mechanism_class  = STATIC_COMPLETE
append_after     = NO
investigation    = RESOLVED
capacity         = 501 bytes
max Korean incl NUL = 412 bytes
minimum slack    = 89 bytes
capacity PASS    = 39/39
```

These are not yet candidate/classification rows and do not yet constitute materialized `INCLUDE_KO`.

## 6. Prompt-owner closure

Exact inherited/selected-use owner facts:

```text
R645  / INLINE:00644 -> target 6938194 / DIRECT / owner_count 1
R2799 / INLINE:02798 -> target 6862647 / DIRECT / owner_count 1
R2975 / INLINE:02974 -> target 6957335 / DIRECT / owner_count 1
R3013 / INLINE:03012 -> target 6921870 / DIRECT / owner_count 1
```

R651 historical L3 state was `UNRESOLVED`. V297 selected-use source sequence resolves it to:

```text
R649 anchor   -> 0x6A7C18
R651 prompt   -> 0x6A7C21
R652 suffix   -> same object at 0x6A7C39
```

Historical L3 artifacts remain unchanged as provenance; V297 supersedes only the selected-use target-resolution conclusion.

## 7. Reusable method rules

The selective project must reuse the following V297 method rules rather than rediscover them:

- diff-run/group is not a logical string;
- Korean replacement may extend through original NUL padding;
- reconstruct against Switch object/field boundaries first;
- use original-byte guards plus family-bounded affine relative-offset validation;
- use adjacent source sequence/containment to disambiguate repeated raw strings;
- use repeated stride/internal offsets/caller arithmetic to recognize fixed record tables;
- decode PC inline payload as compact Hangul -> Korean-added two-byte mapping -> CP932;
- do not naively invert all Mapping 10,036 codes;
- treat UTF-16/mixed UI as a separate encoding/storage family.

## 8. Superseded intermediate values

Do not reuse:

```text
189 unique positive occurrences
39 ending-help = 208 PC records
UNC zero-match padding/NUL = 7
R651 requires exact PC EXE for target closure
```

Use V297 corrected values instead.

## 9. Other container boundaries remain open

V297 does not close the broader inventory:

- TAI5MSG: 33 blocks / 14,832 logical slots structure retained; selective message classification still open.
- EVENT/TS5: 169-file denominator retained; whole-family production parser/caller inventory still open.
- SNR: mixed-container conclusion retained; field/record selective parser still open.
- Switch original RomFS bundle remains `NOT_YET_SUPPLIED` and is not a current blocker until a scope needs it.

## 10. Current materialized product counts

```text
candidate IDs               = 0
classification IDs          = 0
selective INCLUDE_KO rows   = 0
selective builder           = NOT IMPLEMENTED
selective build             = NONE
IPS/runtime artifact        = NONE
```

## 11. Executable next scope — sole authority

After a fresh explicit user execution signal, the exact next scope is:

```text
SELECTIVE_KO_ENDING_HELP_39_CANDIDATE_CLASSIFICATION_MATERIALIZATION
```

This next scope may:

- create the 39 ending-help candidate/classification records;
- carry forward exact source/object provenance;
- encode `UI_DESCRIPTION + STATIC_COMPLETE + RESOLVED` evidence;
- represent 39/39 capacity PASS;
- record R651 selected-use target-resolution provenance where relevant;
- derive terminal disposition only according to the common schema/risk gates.

It must not mix in:

- builder implementation;
- IPS generation;
- gameplay data modification;
- broad TAI5MSG/EVENT/SNR classification;
- grammar125/R4 work.

After this stage, the broader `SELECTIVE_KO_CONTENT_CONTAINER_AND_FIELD_AVAILABILITY_READ_ONLY` work remains open for non-inline containers.

## 12. Repository write boundary

Repository writes remain restricted to exactly:

```text
create_blob -> create_tree -> create_commit -> update_ref(force=false)
```

No Contents-API write, branch creation, issue/PR write, or force update is permitted.

After V297 materialization is reported, another fresh explicit user execution signal is required before beginning the next scope.