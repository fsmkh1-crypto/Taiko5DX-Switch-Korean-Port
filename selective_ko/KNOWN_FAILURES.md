# KNOWN FAILURES AND DO-NOT-REPEAT PATHS

Date: 2026-09-16 (KST)
Status: CANONICAL SELECTIVE-KO FAILURE / REJECTION REGISTRY
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
- affected lines default to `HOLD_DYNAMIC_DIALOGUE`;
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

- person names remain Japanese;
- place names remain Japanese;
- yomi/reading/sort keys remain Japanese;
- Korean name input is excluded;
- CWTDAT Korean reconstruction is not required for R1-R3.

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
- historical PC patch versions are uniformly reliable.

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
