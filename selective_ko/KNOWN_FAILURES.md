# KNOWN FAILURES

Date: 2026-09-15 (KST)
Track: `SWITCH_SELECTIVE_KOREANIZATION`

This file records rejected/failed operational paths so later chats, models, or automations do not repeat them.

## Git write invariant

Only the following repository write chain is permitted:

```text
create_blob -> create_tree -> create_commit -> update_ref(force=false)
```

Forbidden even if exposed by the tool list:

```text
create_file
update_file
delete_file
create_branch
force push
```

## 2026-09-15 TAI5MSG structure resume incident

Scope: `TAI5MSG_STRUCTURE_INDEX_MATERIALIZATION_RESUME`

A forbidden contents-API `create_file` action was invoked repeatedly and created transient files `x`, `y`, `z`, and `q` through these commits:

```text
859d291add8912c37c3902bd919fabb1b7dbbf3a
3bd83d87ff592da97a97b8e1337d69683da44111
f6fcc8a599eb5f658701ff289a30092c55bcadc2
8b7944c9c2bf248001dfd01c88f144e75479f597
```

Pre-incident canonical state:

```text
commit = 1800177201731178b64bc8b9515bdd3fdd86e579
tree   = c5b8416ef5764d67d3c11e48b338254b6cacac5d
```

Forward recovery used only permitted Git-object actions and produced:

```text
commit = bc40ad12dd62fc3600438555b32ce1266ba92a7d
tree   = c5b8416ef5764d67d3c11e48b338254b6cacac5d
TREE_EQUIVALENCE = PASS
```

The recovered tree is byte-identical to the pre-incident canonical tree. No force update/history rewrite was used. The accidental files are absent from the recovered canonical tree.

Root cause: forbidden contents-API actions remained visible in the discovered tool surface and were incorrectly selected despite the project policy.

Prevention rule: forbidden actions are excluded at action-selection time, not merely checked after selection. Before every Git write, re-assert the four-action allowlist and `force=false`.

## Rejected transport/repair shortcuts

- Do not retry monolithic provenance transport that was already rejected.
- Do not use Base64 unless the user explicitly changes the current restriction.
- Do not use contents-API writes as probes or convenience writes.
- Do not repair accidental commits with force push; use forward recovery via canonical tree reproduction.

### Follow-on tool-routing incident and final recovery

After the first recovery, the same forbidden contents-API route was selected again during manual resume. Additional transient commits were:

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

Final forward recovery checkpoint:

```text
commit = a683289dc520a90f3e3c132e8cf10b9e6e1a137d
tree   = c5b8416ef5764d67d3c11e48b338254b6cacac5d
TREE_EQUIVALENCE = PASS
```

This tree is again byte-identical to the pre-incident canonical tree. These commits are history-only incident provenance and confer no content authority.

Hard prevention: discover/call only the four allowlisted Git-object actions for writes. If a forbidden contents action is selected, stop the scope immediately and perform forward recovery only.
