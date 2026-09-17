# KNOWN FAILURES AND DO-NOT-REPEAT PATHS

Date: 2026-09-17 (KST)
Status: CANONICAL SELECTIVE-KO FAILURE / REJECTION REGISTRY / V295 CONTAINER FAILURE ADDED
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
