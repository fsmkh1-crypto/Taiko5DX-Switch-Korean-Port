# KNOWN FAILURES AND DO-NOT-REPEAT PATHS

Date: 2026-09-19 (KST)
Status: CANONICAL SELECTIVE-KO FAILURE / REJECTION REGISTRY / V308 VALIDATION-BOUNDARY ADDED
Track: `SWITCH_SELECTIVE_KOREANIZATION`

This file preserves rejected, weakened, and failed paths so later chats, models, or automations do not repeat them. New operational incidents are appended; older technical failures must not be erased merely to add a newer failure record.

## 1. Dialogue malformed-ending family

Representative Switch symptoms observed during the full-port track:

- `조금 과음한 모양이이오군`
- `오늘은 이만 실례하하겠습니다`
- `야규님입니다인가`

Relevant findings already established:

- not a font/glyph cause;
- not a Mapping 10,036 cause;
- `0x6A` is a real speech-style selector, but inversion is not a fix;
- field64 is person/context identity-related, not a simple speech-style field;
- C8:87 PC/Switch predicate structure is closely corresponding;
- PC original vs PC Korean SNR relation-state tail used by C8:87 is preserved;
- PC Korean TAI5MSG and current Switch-reconstructed C73/C188/message objects can be byte-identical while Switch output remains malformed;
- PC Korean data itself can contain caller + formatter boundaries such as `실례하 + C188`, so stored-fragment visual inspection is insufficient to infer final composition semantics.

Selective-project disposition:

- do not treat this family as an R1-R3 blocker;
- affected rows are deferred under the common taxonomy (`DEFER_KO` when a concrete R4 revisit condition is recorded; otherwise unresolved evidence remains `UNRESOLVED`);
- historical `HOLD_DYNAMIC_DIALOGUE` wording is provenance only, not a new-row terminal disposition;
- reopen only under an explicit R4 formatter-family grammar scope.

## 2. Prohibited dialogue shortcuts

Do not use:

- sentence-by-sentence translation correction to hide a shared formatter failure;
- direct suffix deletion;
- global `하하 -> 하`;
- global `이이 -> 이`;
- longest-overlap/repeated-syllable dedup as a general runtime rule;
- forced C8:87 false;
- global `0x6A` inversion;
- Korean-source rewriting merely because Switch output is malformed;
- assuming every nested call is a pure append without proving the composition contract.

## 3. Name / yomi / CWTDAT boundary

Historical work established that visible names, yomi/readings, auxiliary-name rows, name composition, and platform-specific CWTDAT structure are distinct problem families.

Selective-project policy:

- person names remain Japanese in dedicated identity presentation fields;
- place names remain Japanese in dedicated identity presentation fields;
- yomi/reading/sort keys remain Japanese;
- Korean name input is excluded;
- CWTDAT Korean reconstruction is not required for R1-R3;
- Korean person/place spellings already authored inside selected PC Korean prose remain Korean under V294.

Do not import CWTDAT/name risk into description/event work unless a selected content item has a concrete dependency.

## 4. Runtime-byte normalization

Rejected:

- global Japanese halfwidth-normalization disable;
- patching the downstream decoder merely because compact Korean bytes can be altered upstream;
- mechanical PC x86 byte-validation-helper transplant;
- identifying a normalizer owner by caller-count coincidence alone.

Known Switch structure contains distinct direct-display, generic-parser, and auxiliary/yomi conversion routes. Future transport work remains route-aware.

## 5. Mapping 10,036

Do not reopen Mapping 10,036 because of unrelated renderer/font/dialogue symptoms. The tested Switch-native realization already demonstrated Korean forward/reverse round-trip on the tested route.

## 6. Static-write shortcuts

Do not revive:

- raw occurrence uniqueness as write authorization;
- equal replacement length as sufficient safety proof;
- PC padding as assumed Switch capacity;
- shared-object overwrite without all logical-owner obligations;
- source target resolution as automatic write safety.

Every included selective write still requires a proven Switch owner and appropriate guard/capacity semantics.

## 7. PC implementation trust boundary

Do not assume:

- every PC workaround is desirable on Switch;
- PC descriptor/helper cardinality equals Switch counterpart cardinality;
- PC runtime allocation/signature-search mechanics are portability requirements;
- historical PC patch versions are uniformly reliable;
- PC-original <-> PC-Korean file/message correspondence proves Switch-original correspondence.

Use PC content as source authority where appropriate and Switch structure as implementation authority.

## 8. Git write invariant

The only permitted repository write chain is:

```text
create_blob -> create_tree -> create_commit -> update_ref(force=false)
```

Forbidden even if exposed by tools:

```text
create_file
update_file
delete_file
create_branch
force push
```

Forbidden actions are excluded at action-selection time, not merely rejected after selection.

### 8.1 TAI5MSG structure resume contents-API incidents

Scope: `TAI5MSG_STRUCTURE_INDEX_MATERIALIZATION_RESUME`

First transient chain:

```text
859d291add8912c37c3902bd919fabb1b7dbbf3a
3bd83d87ff592da97a97b8e1337d69683da44111
f6fcc8a599eb5f658701ff289a30092c55bcadc2
8b7944c9c2bf248001dfd01c88f144e75479f597
```

First forward recovery:

```text
commit = bc40ad12dd62fc3600438555b32ce1266ba92a7d
tree   = c5b8416ef5764d67d3c11e48b338254b6cacac5d
TREE_EQUIVALENCE = PASS
```

Follow-on transient chain:

```text
34e9e4eee662fe228e1dad4a80d939064c58b1a0
c43b6a8778df5e84916d8f887498023fda858fbb
c5be2ac723037f341e50d8892a59cdf6669e6579
fbee1bc539b206cfa334f354f410d5572905044f
3c64901b49fec130e93aa7cebd9f1069b8d70c3e
032f766d8cb47036e2a696a72f08165166b29527
cac238c0aaabab561996a22fd52c47ce6be09bda
b690ca4522da6a1484460e6466c6419c414a9d1b
2484c57a9c75dc05a28fa148b119264cad6df6ed
```

Final forward recovery:

```text
commit = a683289dc520a90f3e3c132e8cf10b9e6e1a137d
tree   = c5b8416ef5764d67d3c11e48b338254b6cacac5d
TREE_EQUIVALENCE = PASS
```

The transient commits remain history-only provenance. No force rewrite was used.

### 8.2 Overnight incident-documentation regression

Commit `cd5566c31bb302cfcdb6deb3286bfad34673033e` correctly canonicalized the Git incident but replaced rather than appended the pre-existing technical failure sections in this file. It changed only `selective_ko/KNOWN_FAILURES.md`; gameplay data, registries, and artifact payloads were unaffected.

This materialization corrects the documentation regression by preserving the historical technical failures and appending the Git incident record.

### 8.3 2026-09-16 repeated contents-route incident and recovery

During a subsequent manual materialization attempt, the same forbidden contents-API route was selected again. The transient commits were:

```text
578cd45217c5f234067dace74aa25255ffa3cd79
05cf84312abf6c3bca9e84c506516a5edf43af19
518674a0ae16ecc4c1fe142776087cb0cb2d1f59
```

Forward recovery restored the exact pre-incident documented tree:

```text
commit = ce77b50e289755540e43fad9a78385d888c564e7
tree   = a8c29bf77ddfec362b29456363d30ee69001e143
reference pre-incident commit = cd5566c31bb302cfcdb6deb3286bfad34673033e
reference pre-incident tree   = a8c29bf77ddfec362b29456363d30ee69001e143
TREE_EQUIVALENCE = PASS
changed files relative to cd5566c31bb302cfcdb6deb3286bfad34673033e = 0
```

The accidental paths are absent from the recovered canonical tree. No force update/history rewrite was used.

Operational conclusion: a verbal or prompt-level ban is insufficient by itself. Repository writes must invoke the exact allowlisted Git-object action by name; if the requested tool surface cannot guarantee that, the write scope must stop before mutation.

### 8.4 2026-09-16 pre-materialization sentinel-file drift and forward recovery

After the valid dialogue formatter graph-diff closure at:

```text
commit = 12e0708e1ab601385e2a653a5c6cb31af479b16a
tree   = 9e46f426ffd36179407602b251af25a05ad5bde2
```

two accidental follow-on commits advanced `main`:

```text
f2936af5215c8e37d9995a8622f1eac46b91e20e
6173bc4609525516c02b398636b9b80876851c67
```

The effective delta from the valid closure to the drift head was exactly two added root paths:

```text
__NEVER__
__SHOULD_NOT_BE_CALLED__
```

No legitimate C-closure content was discarded. Forward recovery was prepared from drift head `6173bc4609525516c02b398636b9b80876851c67` using only the allowed Git-object route and produced:

```text
commit = ef1a3dbe9872f9b29ec1b39a426f847c7139c5b8
tree   = 9e46f426ffd36179407602b251af25a05ad5bde2
TREE_EQUIVALENCE_TO_12e0708 = PASS
```

This recovery removes only the two accidental sentinel paths. History is preserved and no force update is used. The recovery commit is the materialization parent for `ART-00000005`.

## 9. Transport / repair shortcuts

- Do not retry the rejected monolithic provenance transport.
- Base64 remains prohibited unless the user explicitly changes that policy.
- Do not use contents-API writes as probes or convenience writes.
- Do not repair accidental commits via force push; use forward canonical-tree recovery.
- Do not treat orphan Git blobs as canonical artifacts until a verified tree/commit/ref materializes them.

## 10. Exact PC v1.02 formatter-runtime provenance correction

During the 2026-09-16 dialogue-formatter investigation, an exploratory PC disassembly used a Drive `Taiko5DX.exe` of size 18,479,304 bytes. That executable is not the exact target required by Korean patch v1.02.

Exact v1.02 patch target identity:

```text
size    18,685,960
sha256  10C69BAB50D29BAF6311360CAFBF7383716A126A6484D209F5E299E12AB565A2
```

The exact target executable is unavailable and its recovery had already been abandoned before this correction.

Therefore the earlier exploratory conclusion that exact PC v1.02 and Switch `0x43/0x4A` cursor/return semantics were proven equal is withdrawn from canonical status. The 18,479,304-byte wrong-build disassembly may be used only as structural background, not exact-target runtime provenance.

Do not repeat either of these paths:

- do not cite the wrong-build disassembly as proof of exact v1.02 runtime parity;
- do not restart the abandoned search for the missing exact v1.02 target EXE merely to continue Korean grammar-flattening design.

The correction does not invalidate exact PC Korean TAI5MSG data provenance or the official JP/SC/TW structural-localization evidence used by `KO_FULL_SENTENCE_GRAMMAR_FLATTENING_V1`.

Canonical correction authority also exists in:

```text
docs/KO_FULL_SENTENCE_GRAMMAR_FLATTENING_V1_DESIGN.md
docs/VALIDATION_LEDGER_KO_FULL_SENTENCE_GRAMMAR_FLATTENING_V1_DESIGN.txt
PROJECT_STATE.md
```

## 11. 2026-09-16 prohibited write-action selection incidents during correction materialization

Two prohibited Contents-API write actions were selected during the correction/materialization sequence despite the repository's Git-object-only rule.

### 11.1 Failed `create_file` selection

A forbidden `create_file` action was selected and returned HTTP 404. It did not advance project `main` and did not create a project-repository object.

Even though the call failed, selecting a forbidden write action is itself a stage failure under repository policy. The stage stopped and required a fresh explicit execution signal.

### 11.2 `update_file` selection that created root path `x`

A later forbidden `update_file` selection did mutate `main` and produced:

```text
commit = f831055b0b69523f6c2f73dc9cb1dca927cdec52
tree   = 8653ffd0d9970ee925522903873e4c5024105aa2
parent = 8e297ffcc8987143eb0afacea582d489a5ba159f
```

Its entire repository delta was one accidental root file:

```text
path     x
content  x
```

No legitimate project file was modified by that commit. This history is preserved rather than force-rewritten.

The canonical forward recovery is the Git-object-only commit that adds this incident record and removes root path `x` in the same final tree. Its commit identity is the direct successor of `f831055b0b69523f6c2f73dc9cb1dca927cdec52` in repository history.

Operational rule reinforced by both incidents:

- tool exposure is not permission;
- `create_file`, `update_file`, `delete_file`, and `create_branch` are excluded before action selection;
- the only repository write actions are `create_blob`, `create_tree`, `create_commit`, and `update_ref(force=false)`;
- any future forbidden-action selection, including a failed 404 call, is an immediate STOP boundary.

## 12. Full-port container/file-level assembly-order failure — V295

The old full-port product path moved too quickly from verified low-level evidence to bulk/file-level payload assembly.

The failure was not that every underlying binary fact was wrong. Mapping, F1 owner evidence, TAI5MSG structure, font/code-space work, and other closed facts remain usable where their original scope applies.

The rejected product sequence was:

```text
bulk/file-level PC payload import
-> run on Switch
-> observe broken names/grammar/transport
-> diagnose symptoms individually
```

Cross-container inspection later established that this sequencing assumption is too coarse:

- TAI5MSG is not dialogue-only;
- verified EVENT/TS5 samples directly contain narration/dialogue payloads;
- SNR contains both scenario/narrative and identity-related data;
- static inline Korean text spans multiple usage roles;
- container/file names do not determine release phase or safety.

Do not repeat these shortcuts:

```text
container == usage_class
container == release phase
long Korean string == UI_DESCRIPTION
F1 static 158 == R1 158
PC original <-> PC Korean structure == Switch structure
raw binary Korean-looking byte scan == verified text-field census
Drive search miss == proof of file absence
bulk PC data/ import == selective release baseline
```

Current required sequence:

```text
identify exact field/message/object
-> classify source-side role/mechanism evidence
-> bind Switch-original structure/owner/callers when required
-> close risk/capacity/provenance
-> authorize only selected Korean realization
```

Canonical correction authority:

`CONTENT_CONTAINER_FIELD_AVAILABILITY_CORRECTION_V295.md`

Switch-original sources may be supplied later under:

`SWITCH_ORIGINAL_SOURCE_INPUT_CONTRACT.md`

Do not repeatedly request XCI extraction before an actual Switch-structure scope requires it.


## 13. V302 SELECTIVE_PROJECT_STATE regex truncation and forward recovery

During V302 checkpoint materialization, the Git-object write route itself was correct, but an in-memory regular-expression replacement used to renumber the required-read list was overly broad because dot matched newlines. The resulting commit:

```text
9779bd0a5888fe278bc0553c7dfff911a4fdde93
```

correctly materialized the V302 authority document, machine-readable checkpoint, and root `PROJECT_STATE.md`, but truncated `selective_ko/SELECTIVE_PROJECT_STATE.md` immediately after the required-read list.

No gameplay data, builder, IPS, candidate/classification artifact, or other project file was damaged.

Recovery rule:

- rebuild the selective state from the exact pre-V302 canonical blob at `7940685f56d51ad1cc260d66e5c7d01a69ae861d`;
- apply V302 edits only through explicit marker-bounded replacements;
- forward-recover with the allowed Git-object route;
- do not force-rewrite history.

Do not repeat a multiline greedy regex for whole-state section replacement. Use explicit start/end markers or exact section replacement and verify required downstream headings before commit/ref update.

## 14. PC Korean patch historical residual QA hazards

Source status:

- The following items are preserved as user-supplied historical information about issues the PC Korean patch author reportedly stated remained even in an improved release.
- They are QA/provenance hazards, not independently verified root-cause conclusions.
- They do not reopen already closed Switch structural facts and do not change the current selective product boundary.

Reported residual issues:

1. Remaining mistranslations still existed.
2. Manual line-break work remained incomplete in text inside the common event file `ECF00000.TS5` and message files.
   - Reported message-window width rule: approximately 20 full-width characters or 40 half-width characters per line.
   - Reported width relation: 2 half-width characters = 1 full-width character.
   - The author reportedly intended to insert line breaks before forced wrapping but stopped part-way because of the time required.
3. Some in-game help text remained untranslated, and some deleted/omitted message-file data still required restoration and translation.
4. Unknown runtime bugs could remain, with forced-minigame events and scenes containing three or more choices specifically mentioned as areas of concern.

### 14.1 Selective-project implications

Do not treat the PC Korean patch payload as a proof of final QA completeness.

Keep these layers separate:

```text
structural release admission
-> content completeness / mistranslation audit
-> layout / reflow QA
-> runtime event-flow QA
```

Required future checks when those scopes are opened:

- audit selected PC Korean text for untranslated, deleted, empty, or suspiciously shortened payloads against the corresponding JP slot;
- treat help-text completeness as its own audit rather than assuming the PC Korean message file is complete;
- implement/review line wrapping using the actual target UI width model rather than blindly preserving all PC line breaks;
- include `ECF00000.TS5` and selected TAI5MSG text in line-break QA;
- include forced-minigame events and scenes with three or more choices in runtime regression coverage;
- preserve the distinction `build/package PASS != gameplay PASS`.

### 14.2 Historical long place-name / history-screen crash

Reported older-PC-patch symptom:

- before a later improvement, sufficiently long Korean base/place names could crash when opening/calling history information;
- the exact historical threshold is not considered proven here and was remembered as around 7-8 Korean characters;
- the concrete example supplied is `히다다카야마마을` (8 Hangul syllables).

Treat this as:

```text
PLACE_NAME_LONG_LENGTH_HISTORY_CRASH
status = HISTORICAL_REPORTED_HAZARD
exact_threshold = UNCONFIRMED
representative_example = 히다다카야마마을
```

Do not infer the cause solely from character count. Plausible cause families to investigate only when the identity/name scope is explicitly reopened include:

- fixed-size temporary/history UI buffers;
- byte-count vs character-count assumptions;
- descriptor length limits;
- copy/termination boundaries;
- secondary consumers of place-name identity data.

Because a later PC patch reportedly improved this issue, future identity/name work must inspect the actual pre-fix vs post-fix PC patch replacement bytes, descriptors, pointers, and runtime handling before designing a Switch-side solution.

Current first-release policy remains unchanged:

```text
dedicated person/place identity presentation = KEEP_JP
yomi/reading/sort keys                       = KEEP_JP
authored Korean identity literals in prose   = PRESERVE_AS_AUTHORED_KO
```

Therefore this historical long-name crash is not a blocker for the current selective R1/R2 TAI5MSG prose track. It becomes a mandatory regression/provenance item only if dedicated Korean identity/place-name presentation is explicitly reopened.

## 15. External text-only audit recurring false blockers and adopted gates — V305

Four user-supplied external text-only red-team reviews were consolidated by TAI5MSG_EXTERNAL_DESIGN_AUDIT_CONSOLIDATION_V305.md.

External reviews do not supersede verified binary evidence.

Rejected without new binary evidence:
- global selective 3,318 must all be TAI5MSG;
- inline 139 must be added to TAI5MSG block growth;
- V304 payload lengths prove a per-message length prefix;
- TAI5MSG has a movable offset-table pointer that must be rewritten;
- TAI5MSG checksum/CRC/HMAC must exist because other formats may contain one;
- V304 necessarily changes +0x7780 physical release growth;
- reverse mapping conflicts with reverse-substitution policy;
- post-V304 05 05 05 is a newly introduced unknown Switch sequence.

Binding carrier separation: global selective INCLUDE_KO 3,318 = inline/main 139 + TAI5MSG/RomFS 3,179.

Adopted gates:
- DETERMINISTIC_PADDING_GATE
- ZERO_REPLACEMENT_IDENTITY_REBUILD_GATE
- CONTROL_AND_CODE_VALIDATION_GATE
- STRONG_REPARSE_OFFSET_GATE
- MAPPING_TO_GLYPH_CLOSURE_GATE

The first four constrain the TAI5MSG serializer path. Mapping-to-glyph closure is a release/package integration gate.

Next bounded read-only scope: TAI5MSG_SELECTIVE_SERIALIZER_IDENTITY_REBUILD_AND_PADDING_PROVENANCE_READ_ONLY.

Do not implement the serializer merely because V305 records these gates.


## 16. V306 preimplementation closure — do-not-overgeneralize boundaries

Canonical authority: `TAI5MSG_PREIMPLEMENTATION_GATE_1_5_CLOSURE_V306.md`.

Do not repeat these overgeneralizations:

- do not infer `B32 physical EOF = rebuilt used-end` from the zero-replacement stock identity case;
- do not shrink B32 declared size merely because the selected payload becomes shorter;
- do not emit the final stock 55-byte B32 declared-minus-physical tail as writable filler;
- do not treat `+0x7780` or `0x1C1949` as hard-coded serializer inputs; they are expected recomputed postconditions for the current 3,179-row corpus;
- do not claim V303 raw payload is control-safe without applying the exact V304 two-row correction overlay;
- do not treat arbitrary `00` as an allowed TAI5MSG token because the canonical final B32:M242 structural terminator is `...05 05 05 00`;
- do not import the W0/W1 compact A1..DF font-width family into this TAI5MSG release population; effective compact-Korean usage is zero;
- do not claim all 2,542 Korean-added Mapping entries have visible glyph closure. V306 GATE-5 is limited to the 992 Hangul codes actually emitted by the effective 3,179 TAI5MSG rows;
- do not reopen GATE-1..5 without new contradictory binary/runtime evidence.

Binding effective B32 release state:

```text
used-end       0xB8D5
physical       0xCA49
declared       0xCA80
physical filler 0x1174 bytes
omitted tail      0x37 bytes
```

Binding current release postconditions:

```text
growth      +0x7780
final size  0x1C1949
```


## 17. V307 serializer-design rejected shortcuts

Canonical authority: `TAI5MSG_3179_SELECTIVE_BUILDER_SERIALIZER_DESIGN_V307.md`.

Do not repeat:

- do not rebuild every B0..B31 declared extent as only `align_up(used,0x40)`; this naive shrink strategy yields aggregate `+0x58C0` for the current corpus instead of canonical `+0x7780`;
- do not shrink a block below its stock declared envelope merely because Korean target payload is shorter;
- do not treat B32 like B0..B31; current B32 preserves declared `0xCA80`, physical `0xCA49`, and omits the final `0x37`;
- do not calculate layout from expected `+0x7780`, `0x1C1949`, `0x1B4F00` or the V306 diagnostic hash; compute layout from inputs and use those only as postconditions;
- do not begin from full PC-Korean TAI5MSG and restore excluded rows; begin from stock JP and replace exactly V303 membership;
- do not make `builder/tai5msg.py` the selective policy engine; it remains legacy/reference for the V288/V289/V290 path;
- do not let the serializer discover, translate, promote, skip, or repair rows beyond V303 membership and exact V304 authority;
- do not publish a partial output after a guard failure;
- do not couple the pure TAI5MSG serializer to Mapping/font/ExeFS mutation.

Binding B0..B31 policy:

```text
required = align_up(effective_used,0x40)
declared = max(stock_declared, required)
physical = declared
```

Binding current B32 policy:

```text
used-end  0xB8D5
physical  0xCA49
declared  0xCA80
omitted   0x37
```


## 18. V308 metadata-PASS is not byte-output PASS

Canonical authority: `TAI5MSG_3179_SELECTIVE_SERIALIZER_IMPLEMENTATION_OFFLINE_VALIDATION_V308.md`.

The V308 repository-only metadata replay independently passes V303 shard integrity, V304 exact deletion semantics and V307 block arithmetic.

Do not overclaim it as execution of the new Python serializer.

Current limitation:

```text
new module byte-exact execution = PENDING
reason = current container/Python file-mount transport timeout after large PC-patcher attachment
```

Do not proceed to package/build integration until the bounded byte-exact offline replay executes:

- zero-replacement identity;
- actual canonical 3,179 serialization;
- independent reparse;
- V306 diagnostic SHA comparison.


## 19. V313 runtime / reflow audit — do-not-repeat conclusions

Canonical authority:

`selective_ko/TAI5MSG_V312_EDEN_RUNTIME_PC_COVERAGE_REFLOW_AUDIT_V313.md`

Runtime evidence closes the following false blockers for the observed V312 Eden route:

- V312 globally not loaded;
- TAI5MSG LayeredFS globally absent;
- Korean Mapping/page mapper/font globally nonfunctional.

Content/layout audit adds these prohibitions:

- do not interpret any random Japanese description screen as patch failure without first proving PC-KO payload existence and selected membership;
- do not infer semantic correctness merely because a PC-KO slot contains Korean codes;
- do not apply one uniform whitespace-only reflow to all 697 over-width selected messages;
- do not patch only B24:M227..M229. They are representatives of a common B24 cause-family and require full B24 M221..M344 audit first;
- do not preserve all PC manual newlines as final layout authority;
- do not split Korean tokens mechanically at the 40-unit boundary when a legal prior word boundary exists.

Binding V313 partition:

```text
hard-overflow selected rows              697
ordinary non-B24 reflow candidates       584
B0/B21 caller-width waits                  4
B24 selected rows                         124
B24 hard-overflow                         109
B24 body/control skeleton separated       108
known B24 semantic misalignment      M227 M228 M229
```

Next cause-family is read-only B24 semantic alignment/control-layout audit.

## 20. V322 broad EVENT caller-graph traversal hang

Scope:

`DIALOGUE_SCRIPT_RUNTIME_PC_PATCH_ORACLE_SURVEY_READ_ONLY`

During V322, the investigation reached already-useful bounded EVENT/SNR resource-loader anchors and then expanded into a broad EVENT-subsystem caller/call-flow traversal.

The UI remained on the call-flow/subsequent-code analysis step for more than one hour without completion.

No conclusive internal error code was returned, so the incident is recorded as:

```text
analysis_path_status = FAILED_BY_UNBOUNDED_EXPANSION_OR_HANG
tool_defect          = NOT_PROVEN
repository_write     = NONE
product_bytes        = NONE
build/package        = NONE
```

Do not repeat:

- whole-subsystem recursive caller expansion;
- unconstrained call-graph traversal from a broad EVENT subsystem root;
- waiting indefinitely merely because no explicit error banner is shown.

Required replacement method:

```text
known anchor
-> finite direct caller/callee census
-> maximum 1-2 direct call levels
-> report / checkpoint
-> fresh authorization before deeper trace
```

Current allowed next analysis anchor set is bounded to the already-established EVENT path around:

- `0x158A58`;
- resource getter `0x440A80`;
- JP `ECF00000.TS5` resource ID 77.

If bounded traversal leaves the declared subsystem or grows beyond the finite planned node set, stop and report rather than recursively expanding it.


## 21. V323 PC ECF00000 exact-census preparation stall

Scope:

`DIALOGUE_EVENT_TS5_PC_PATCH_TEXT_LAYOUT_ORACLE_READ_ONLY`

The exact PC v1.02 patcher and patched `ECF00000.TS5` were already known from V322, but two follow-up attempts spent excessive time in repeated input identification/parser preparation before producing the requested finite 782-script command census. One attempt remained active for more than 30 minutes without a completed census.

```text
analysis_path_status  FAILED_TO_REACH_BOUNDED_CENSUS_IN_TIME
tool_defect           NOT_PROVEN
pc_patcher_identity   RECONFIRMED_BYTE_EXACT
pc_ecf_payload        RECONFIRMED_BYTE_EXACT
exact_command_census  NOT_COMPLETED
repository_product    UNCHANGED
build/package         NONE
```

Do not repeat:

- re-search or reconstruct the PC patcher when the exact input already matches SHA-256 `109dc729e66df8cd0a47c5f6c24719260eb03a89890a0c69d3ba739145dcfb23`;
- re-extract/re-identify `ECF00000.TS5` when it already matches SHA-256 `0899bf81789acfbd243d43be209a8a3960933fa090960ac8c753c63f95f07bbe`;
- search indefinitely for a pre-existing TS5 parser before attempting the finite corpus walk;
- reverse-engineer all 96 opcode semantics before counting the known message/choice family;
- use raw byte scans as an opcode census.

Required replacement:

```text
verified 782-script offset table
-> finite command-boundary walker
-> resolve only lengths needed for safe stepping
-> count 0x11 / 0x12 / 0x13 / 0x15 and message 0x0A / 0x1B
-> stop on first unknown boundary with exact script+offset
-> report before broader grammar work
```

This failure does not invalidate the bounded Switch interpreter findings recorded by V323.

## 22. V337 EVENT unit-fixture byte escape defect

Scope:

`ECF00000_SELECTIVE_EVENT_GENERIC_RELOCATION_ENGINE_IMPLEMENTATION_OFFLINE_VALIDATION`

During V338 pre-publication validation, the four unit-test methods added in V337 were inspected at the actual repository blob level. Fourteen source lines contained doubled byte escapes such as `b"\\\\x02..."` instead of raw-byte Python literals `b"\\x02..."`.

Impact:

```text
production builder affected             NO
EVENT product bytes affected            NO
V337 stock full-corpus arithmetic       NOT INVALIDATED
V337 repository new unit fixtures       INVALID UNTIL V338 CORRECTION
V338 publication with bad fixtures      PREVENTED BEFORE main UPDATE
```

The S2 arithmetic had also been exercised independently against the exact stock corpus, but the repository unit fixtures themselves were not valid evidence until corrected.

V338 correction requirements:

- fix the complete doubled-escape cause-family in `tests/test_selective_event.py`;
- rerun the four corrected S2 tests;
- rerun exact stock S2 gates (7,579 plans / unchanged byte-exact / 7,578 controlled growth);
- run the S3 tests and special-owner stock gates before moving `main`.

Do not repeat:

- counting test methods as proof that tests executed;
- validating generated Python byte fixtures without inspecting the materialized source;
- correcting only one visible escaped literal while leaving the same generation defect elsewhere in the file.
