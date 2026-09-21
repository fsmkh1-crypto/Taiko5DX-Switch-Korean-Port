# KNOWN FAILURES AND DO-NOT-REPEAT PATHS

Date: 2026-09-20 (KST)
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

## 23. V339 5A solve-before-branch-repair interaction

Scope:

`ECF00000_5A_BRANCH_AWARE_JP_IDENTITY_KO_DIALOGUE_COMPOSITE_IMPLEMENTATION_OFFLINE_VALIDATION`

A preimplementation 5A audit initially proved all 1,074 translated outer-5A rows against the current layout before final branch relocation. That was insufficient.

After V337 generic relocation was applied, exactly one previously passing row changed runtime behavior:

```text
partition        118
original 5A      0x3FE34
PC-KO 5A         0x504B8
following branch 0x04 @ original 0x3FE58
```

The relocated 0x04 field introduced a new NUL byte into data inspected by the preceding Switch 0x5A runtime-length calculation. The earlier assumption:

```text
solve all 5A
-> repair branch fields
-> 5A geometry remains valid
```

is therefore rejected.

Binding replacement:

```text
partition reverse-order 5A solve
-> evaluate every candidate against current V337 generic + V338 special repaired following bytes
-> final branch/special repair
-> reverify all 1,074 translated 5A rows
```

The affected row is resolved as the single `ZERO_NEXT_TERMINATOR` subtype using original JP names, PC-KO dialogue, and two trailing ASCII spaces in the second JP name field. This makes the 5A self-contained without translating identity.

Final V339 result:

```text
ORIGINAL_TARGET         1,058
CHOICE_NEXT_START          15
ZERO_NEXT_TERMINATOR        1
violations                  0
```

Do not repeat:

- validate 5A only before branch relocation;
- hard-code the 82 modified offsets instead of recomputing from the current layout;
- treat the partition-118 row as an ordinary dialogue-padding case;
- translate 5A names merely to inherit PC-KO byte geometry.

## 24. V340 absolute state-aware zero-error gate false blocker

Scope:

`ECF00000_PARTITION593_0E_RESIDUAL_RUNTIME_OVERRUN_ROOT_CAUSE_AND_VALIDATOR_GATE`

V339 retained one state-aware diagnostic overrun at partition 593 / original `0xBDD78` / opcode `0x0E`. Replaying the same diagnostic model on unmodified stock produces the same logical residual:

```text
partition        593
original anchor  0xBDD78
header           0E 02 D5 1F
decoded length   0x7F5408
```

V339 relocates the same original logical object to current `0xDDD84`; it does not create a new residual.

Bounded Switch-main disassembly confirms the 0x5A consumed-length formula and 0x0E parent-length formula, while also proving that the common interpreter loop carries control state beyond the conservative V333 `(context, physical_address, S, F)` model. Handler-returned length is not applied before mode/control/global-stop checks.

Rejected gate:

```text
state-aware residual count must equal zero
```

Binding replacement:

```text
compare candidate residuals to exact stock logical baseline
identity = kind + partition + original_offset + opcode + decoded_length

same stock residual, relocated current offset  -> NON_BLOCKING
stock residual disappears                     -> NON_BLOCKING
new/mutated logical residual                   -> BLOCKING
```

Do not:

- patch stock `0x0E` bytes merely to make a diagnostic count zero;
- force V339 5A geometry to PC-KO solely to suppress the stock residual;
- compare residual identity by current relocated offset;
- treat V333 MAY-reachable state union as exact gameplay-feasible execution.

## 25. V341 0x1E semantic-admission vs runtime-admission separation

Scope:

`ECF00000_1E_SEMANTIC_ADMISSION_LEDGER_MATERIALIZATION`

The full PC patch changes 388 of 461 editor-owned `0x1E` objects, but changed does not mean product-admissible.

Exact semantic partition:

```text
KEEP_JP_IDENTITY             344
PRESERVE_IDENTICAL            73
semantic PC-KO candidates     44
```

The 344 identity rows include 103 direct personal names, 24 clan/kabane identity composites, 216 dynamic name-slot fragments referenced through `\Z001`, and one named-person honorific. Do not translate them merely because PC-KO changed them.

The 44 non-identity semantic candidates must remain separated from runtime admission:

```text
INCLUDE_KO_READY             23
INCLUDE_KO_RUNTIME_PENDING   21
```

Do not repeat:

- copy all 461 PC-KO 1E objects;
- copy all 388 changed 1E objects;
- preserve only obvious full personal names while translating dynamic name fragments;
- classify `国 / 徳 / 愛 / 義 / 豪 / 初 / 早川 / 永 / 冬` as ordinary standalone vocabulary in this context;
- equate semantic translatability with runtime admission;
- promote the 21 pending rows without new runtime provenance;
- reopen V340's stock-preexisting 0x0E residual as evidence that 1E must be bulk-copied.

## 26. V343 PC-editor 0x3C over-group is not runtime ownership

Scope:

`ECF00000_3C_KEEP_JP_EXACT_LEDGER_CANONICALIZATION`

The PC editor groups 101 apparent `0x3C` objects. Runtime evidence proves that only 100 are normal four-field rename/identity commands.

The exceptional editor object:

```text
partition        283
original offset  0x7BFEC
PC-KO offset     0x9B038
editor length    36
runtime 3C len   20
PC-KO changed    NO
MAY-reachable    NO
```

is physically `EVENT 0x38 @ 0x7BFE8 + 4`. The apparent `0x3C` byte is inside another runtime command and must be preserved as `PRESERVE_STRUCTURAL_ALIAS`.

Binding V343 disposition:

```text
KEEP_JP_IDENTITY             100
PRESERVE_STRUCTURAL_ALIAS      1
PC-KO 3C mutation allowed      0
```

Do not repeat:

- treat every editor-grouped 0x3C as a standalone runtime rename owner;
- copy all 100 changed PC-KO rename objects merely because mapping is exact;
- translate only MAY-reachable identity rows while mutating non-MAY identity rows;
- build a 3C mutation serializer for the current KEEP_JP product;
- use final-Korean fresh grouping as runtime ownership authority.

## 27. V344 particle applicability is not the V335 single semantic-detail code

Scope:

`ECF00000_FIXED_SURFACE_PARTICLE_V1_PREIMPLEMENTATION_CLOSURE`

V335's single semantic-detail code is mutually exclusive. Choice rows are classified as `INCLUDE_KO_CHOICE` before the fixed-particle detail, so 25 choice rows containing exact dual-particle literals do not carry code 3.

Exact correction:

```text
code 3 fixed-particle rows       1,226 / 1,364 occurrences
choice-overlap particle rows        25 /    25 occurrences
exact applicability             1,251 / 1,389 occurrences
```

The historical total 1,389 occurrence census is retained. The rejected implementation interpretation is that all 1,389 occurrences are inside the 1,226 code-3 rows.

Do not repeat:

- use `semantic_detail == 3` as the complete FIXED_SURFACE_PARTICLE applicability gate;
- omit particle normalization from the 25 choice rows;
- convert semantic admission into a single-axis technical applicability model;
- globally rewrite standalone Korean particles rather than exact approved dual literals.

## 28. V344 layout-exposed embedded aliases require source proof, not one-off residual exceptions

The full particle read-only simulation exposes a new conservative state-aware logical residual at original `0xC3740`. It is `EVENT 0x0B @ 0xC373C + 4`, not a standalone product command.

The exact stock structural family contains 52 `0x0B +4 -> 0x0E` aliases:

```text
INHERITED_STOCK_RESIDUAL     1
NOVEL_ALIAS_ELIGIBLE        48
NOT_GATE_ELIGIBLE            3
```

No alias overlaps a TS5 entrypoint or V334 canonical text/choice target.

Binding V344 gate:

- inherited stock logical residuals remain non-blocking;
- a novel residual is non-blocking only if it matches an exact `NOVEL_ALIAS_ELIGIBLE` ledger row **and** current bytes prove the same parent header, parent length, +4 relation, alias header, alias decoded length, and partition containment;
- identical logical observations at the same current offset are collapsed across conservative S/F states;
- the same logical key at different current offsets is blocking ambiguity.

Do not repeat:

- add only `0xC3740` as a one-off exception;
- blanket-whitelist every `0x0B+4` command-looking byte;
- retain the earlier temporary count of 64 aliases; exact V344 runtime-length census is 52;
- reject legitimate duplicate S/F observations merely because they share one logical residual;
- accept a source alias without current-byte proof.

## 29. V345 final-PC-KO fresh grouping is not payload-owner authority

Scope:

`ECF00000_FIXED_SURFACE_PARTICLE_V1_IMPLEMENTATION_OFFLINE_VALIDATION`

The first V345 particle-module integration attempt tried to locate each Korean particle owner by freshly grouping the final PC-KO TS5 and indexing grouped items by the canonical `ko_offset`.

It failed at canonical row 556 / KO offset `0x16828`.

This is not a bad V344 ledger row. V334 already records final-Korean fresh-reparse drift and exact special original->KO bindings. Final-Korean fresh grouping is explicitly not ownership authority.

Binding implementation:

```text
exact V344/V334 ko_offset + ko_length
-> raw slice from exact canonical PC-KO blob
-> opcode/length guard
-> transform approved message/choice string ranges
```

Do not repeat:

- reparse/group final Korean bytes to rediscover a canonical KO owner;
- reject V334 special bindings because the final-Korean editor grouping does not start at the bound offset;
- replace exact raw ledger slicing with ordinal lookup against a fresh final-Korean parse.

## 30. V346 code-5 particle-risk detector conflates four semantic cause families

Scope:

`ECF00000_V335_CODE5_426_SEMANTIC_ADJACENCY_LEDGER_CANONICALIZATION`

V335 code-5 / `UNRESOLVED_PARTICLE_RISK` is a conservative detector bucket, not one implementation family.

Exact V346 partition:

```text
DIRECT_PARTICLE_ONLY              350
COPULA_DERIVED_ONLY                59
MIXED_DIRECT_AND_DERIVED_RISK       2
LEXICAL_FALSE_POSITIVE_GAMUN       12
NON_PARTICLE_SUFFIX_ADJACENCY       3
```

The 12 lexical false positives are exact `escape + 가문...` cases. Here `가` is the first syllable of the noun `가문`, not a subject particle. They are promoted to semantic `INCLUDE_KO` but are not implemented in V346.

The three non-particle suffix rows are:

```text
row 4743   \%21 + 는 것도 ...
row 5059   없\%15 + 는데 ...
row 11440  보\%2A + 는 건 ...
```

Their detected `는` belongs to verbal/ending morphology rather than a noun-particle attached to a runtime value.

Binding disposition:

```text
INCLUDE_KO   12
DEFER       414
```

Do not repeat:

- treat all 426 rows as one fixed-particle transform family;
- treat every escape-adjacent `가` as a subject particle;
- keep the 12 `가문` rows unresolved;
- route copula/derived forms through V345 FIXED_SURFACE_PARTICLE_V1;
- treat rows 4743/5059/11440 as noun-particle adjacency;
- promote the remaining 414 merely because V345 fixed-particle validation passed.

The exact direct-particle hit total remains 389. V346 corrects the prior conversational per-particle transcription to:

```text
가 104 / 는 81 / 은 50 / 를 47 / 이 46 / 와 27 / 을 15 / 로 10 / 과 9
```


## 31. V347 do not invent a hidden runtime Korean-particle selector

Scope:

`ECF00000_CODE5_DIRECT_PARTICLE_RUNTIME_RESPONSIBILITY_READ_ONLY`

The V346 direct-particle family preserves its runtime escape sequence between original-PC and
PC-KO for all 352 target rows and all 389 direct occurrences. Switch EVENT runtime expands the
escape value/control token and then resumes ordinary literal scanning; the following Korean
particle is authored EVENT data.

PC patch code-layer audit gives no Korean josa selector:

```text
T5K inline records                  17,103
inline targets inside target .text      0
runtime descriptors                    11
helper bytes                           158
```

Established descriptor/helper responsibilities cover mapping, byte handling, page mapping,
font/page threshold, UI width and description-font behavior, not Hangul final-consonant or
particle-allomorph selection.

Do not repeat:

- assume an EVENT escape dynamically chooses Korean particles;
- search for a missing Switch josa hook before respecting the actual PC patch mechanism;
- interpret the 17,103 inline replacements as executable particle-selection code;
- assign one Korean particle to an escape family merely from escape identity;
- silently fold the V346 direct rows into V345's exact 1,251-row fixed-surface ledger.

The next question is product-policy applicability, not runtime mechanism reconstruction.

## 32. Unbounded resume-state fetch creates context I/O bottleneck

Scope:

`PROJECT_RESUME / SELECTIVE_TRACK_OPERATIONS`

On 2026-09-20, a resume attempt fetched accumulated `PROJECT_STATE.md`,
`SELECTIVE_PROJECT_STATE.md`, and `KNOWN_FAILURES.md` too broadly. The returned material was
large enough to be truncated and created avoidable context-processing latency before the V345
implementation itself had begun.

Impact:

```text
technical analysis lost       NO
product bytes changed         NO
repository write              NO
implementation begun          NO
root cause                    over-broad resume reads / context I/O
```

Binding replacement authority:

`selective_ko/BOUNDED_RESUME_READ_POLICY.md`

Do not repeat:

- dump the full accumulated PROJECT_STATE history into active context on every resume;
- read every `required_reads` entry merely because it is listed;
- dump all KNOWN_FAILURES when only one current cause-family is relevant;
- re-read CLOSED/VERIFIED authorities without a demonstrated provenance need.

Required resume pattern:

```text
remote HEAD
-> bounded PROJECT_RESUME_V2/current overlay
-> bounded SELECTIVE current status/next scope
-> current authority + INDEX
-> exact-scope code/data only
```

The `required_reads` array is provenance ordering, not a mandatory read-all checklist.

## 33. V346 human-ledger surface metadata can misbind repeated identical escapes

Scope:

`ECF00000 / V346-V348 DIRECT_ESCAPE_PARTICLE`

V348 found exactly two direct-hit records in V346 `LEDGER.jsonl` where the auxiliary
`surface` field disagrees with the actual decoded source adjacency and `detector_head`:

```text
row 4094   \%00   detector_head 를   surface 는
row 7233   \%01   detector_head 를   surface 가
```

Both rows contain the same escape multiple times with different following particles. An
occurrence-binding mistake in the diagnostic `surface` metadata is the leading explanation,
but the original generating-code cause was not recovered and must remain INFERRED.

Impact is bounded:

```text
V346 compact membership             unchanged
V346 DIRECT_PARTICLE_ONLY rowset    unchanged
direct occurrence total             unchanged
preferred/opposite totals           unchanged
V347 runtime responsibility         unchanged
V348 applicability result           unchanged
```

Do not repeat:

- use `surface` as authoritative direct-particle content;
- identify an occurrence only by `(row_id, escape)`;
- collapse repeated identical escapes inside one message;
- regenerate the V346 350-row membership because of these two metadata records.

V348 occurrence authority instead binds row + field + decoded position + exact escape + expected
source particle, and future raw-byte implementation must reverify against the canonical PC-KO
`ko_offset/ko_length` slice before mutation.

## 34. V352 do not hard-code state-aware residual observation counts across legal payload growth

Scope:

`ECF00000 / V340 / V344 / V352 state-aware validation`

The first V352 integration harness incorrectly asserted that every later valid EVENT diagnostic
must preserve V344's exact three raw state-aware observations.

V350 had:

```text
observations          3
logical residuals     2
inherited stock       1
source-proven alias   1
```

V352 valid payload growth changed conservative MAY-walker reachability and produced:

```text
observations          1
logical residuals     1
inherited stock       1
source-proven alias   0
novel                 0
blocking              false
```

Isolation proved the disappearance is caused by valid V351 payload growth in partition 593.
Applying all V351 rows except partition 593 retains the three observations; applying only the
three partition-593 rows reduces them to one. Row 11082 or row 11090 individually is sufficient.

The V344 alias source bytes are not modified. Partition 604 is byte-identical between V350 and
V352, including parent 0xC373C and alias 0xC3740.

Do not repeat:

- assert an exact raw observation count from an earlier diagnostic;
- treat disappearance of an inherited/source-proven diagnostic residual as corruption;
- patch unchanged source bytes merely to restore a conservative MAY-model observation;
- replace the V340/V344 provenance-based residual-delta gate with absolute-count validation.

Canonical rule remains: known residuals may disappear; exact inherited or source-proven
residuals may remain; genuinely novel residuals are blocking.
## 35. V353 do not treat percent macros as ordinary value-only EVENT escapes

Scope: `ECF00000 / %xx / TAI5MSG block-0 cross-carrier runtime grammar`

The exact V346 suffix-three rows prove that bounded `%xx` macros can emit language-bearing TAI5MSG block-0 formatter fragments.

```text
\%15 -> 209 -> TAI5MSG 0:209
\%21 -> 349 -> TAI5MSG 0:349
\%2A -> 395 -> TAI5MSG 0:395
```

Switch table: `RODATA 0x6AC004 / 52 entries`
TAI5MSG getter: `0x43F2A4`

Current selective TAI5MSG B0 Korean locals are only 10 and 11, so the three required roots remain JP in the current product.

Do not repeat:
- classify all `%xx` macros as value/control-only escapes;
- patch the three suffix EVENT rows without their TAI5MSG dependency;
- treat the suffix `는` as an ordinary particle;
- infer `%xx` owner from the hexadecimal token value itself;
- return to CWTDAT as grammar owner without contradictory byte evidence;
- enable all 52 B0 roots blindly;
- invalidate V349/V352 structural serializer/relocation PASS merely because the runtime-language dependency layer was previously incomplete.

Canonical rule: `EVENT byte validity/relocation PASS != percent-macro runtime-language integration PASS`.

Run the bounded product-admitted `%xx` -> B0 dependency census before any implementation.
## 36. V354 do not infer percent-macro coverage from aggregate TAI5MSG selection

Scope: `ECF00000 %xx -> TAI5MSG block-0 direct-root coverage`

The selective TAI5MSG product contains 3,179 Korean messages overall, but its B0 Korean membership is exactly locals 10 and 11. The 46 B0 roots directly used by product-admitted `%xx` macros are all different from 10/11.

```text
product-used %xx roots   46
current KO roots          0
current JP roots         46
```

Do not repeat:
- infer `%xx` Korean runtime coverage from the aggregate 3,179 selected-message count;
- treat B0 10/11 as common support for the 46 direct roots;
- conclude all 2,440 occurrences are visible defects before role classification;
- globally replace all 46 roots solely because they are JP;
- re-scan all 14,832 TAI5MSG messages or all V288 grammar rows before inspecting the exact 46 roots.

Canonical next step is exact 46-root PC-original vs PC-Korean role/language-output classification only.


## V362 — V361 Japanese dialogue / EVENT-family scope correction

- **Wrong-path hypothesis rejected:** Switch v1.1.3 `main` directly names `EVENT\\ECF00000.TS5`; V361's `romfs/EVENT/ECF00000.TS5` placement is not the established cause of the Japanese dialogue result.
- **ECF00000-only carrier model rejected:** the PC Korean patch replaces 169 EVENT TS5 files and the Switch `main` names the same 169 TS5 members. Do not treat ECF00000 as the complete ordinary-dialogue universe.
- **V361 unchanged retest is unnecessary:** user Eden runtime already showed ordinary dialogue remained Japanese while the Korean TAI5MSG/description route remained observable.
- **Do not guess the screenshot owner:** exact EFF/EP/EPF ownership requires the extracted Switch v1.1.3 `romfs/EVENT/` subtree.
- Next cause-family: `SWITCH_V113_EVENT_169_SOURCE_PARITY_AND_PC_PATCH_PORTABILITY_AUDIT_READ_ONLY` (READ ONLY).


## 37. V363 runtime-MAY source universe is not a completeness gate

Scope: `ECF00000 / V333-V363 source-universe completeness`

V361 hardware-visible dialogue at original ECF offset `0x4748` is absent from V334's 13,075-row deterministic MAY-reachable universe but is a real PC-original editor text owner and has exact PC-KO counterpart `0x4ED4`. The V361 payload kept the original command, proving a coverage omission rather than a wrong RomFS path or another-file owner for that exact dialogue.

V363 full original-owner census:

```text
PC-original text owners        15,951
V334 stable subset             13,075
new rows                        2,876
exact new mappings              2,871
binding DEFER                       5
```

Do not repeat:

- use runtime-MAY reachability as a source-universe completeness gate;
- infer owner from final rendered screenshot literals when runtime placeholders exist in source;
- use final PC-KO fresh grouping as owner authority;
- renumber legacy V334 rows when extending coverage;
- guess five structural-drift bindings or promote KO-only `0x8E010` without original ownership.

V334's existing 13,075 rows remain valid and stable; only its completeness claim is superseded.
