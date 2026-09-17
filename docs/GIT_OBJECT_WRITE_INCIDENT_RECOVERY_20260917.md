# Git Object Write Incident Recovery — 2026-09-17

Status: CANONICAL OPERATIONAL INCIDENT RECORD
Related stage: `SELECTIVE_KO_DIRECTION_RECONCILIATION_V292_MATERIALIZATION`

## 1. Incident summary

During V292 materialization, the repository policy required Git-object-only writes:

```text
create_blob -> create_tree -> create_commit -> update_ref(force=false)
```

Nevertheless, forbidden Contents-API actions were selected on successive attempts. Because Contents-API writes mutate the branch directly, each successful forbidden call advanced `main` before the intended Git-object commit could be attached.

This was an operator/tool-selection failure, not a gameplay-data or Koreanization-design failure.

## 2. Accidental commit chain

Pre-incident canonical HEAD:

```text
2172e3b24bce5daf4e7cc1547d3b1d0f3c78e38a
```

Accidental branch history:

```text
06091bfeda6420e270f8cc82603e3c1536192a0b
  forbidden Contents-API write
  added root sentinel __NEVER__

e2a1e2ae0ad4b71687083a89c54958a5d36fa27c
  forbidden Contents-API write
  modified root sentinel __NEVER__

01028ecbfcd41fe799799d2d639151b46f542288
  forbidden Contents-API write
  added root sentinel __NEVER2__

a358c43b4fa43cff0f0ab8aff145205fcbf08366
  forbidden Contents-API write
  added root sentinel __SHOULD_NOT_BE_CALLED__
```

Read-only comparison from `2172e3b...` to `a358c43...` proved the net file delta was exactly:

```text
A  __NEVER__
A  __NEVER2__
A  __SHOULD_NOT_BE_CALLED__
```

No legitimate project/gameplay path differed from the pre-incident canonical tree.

## 3. Root cause

The repository policy existed only as an execution rule while the connected GitHub tool surface still exposed both permitted Git-object actions and forbidden convenience/Contents-API actions.

The failure was repeated because action availability was incorrectly treated as an invocation candidate set instead of enforcing the project allowlist before tool selection.

The correct invariant is stronger:

```text
exposed by connector != permitted by project
```

For repository mutation, action selection must be performed from this literal allowlist only:

```text
GitHub.create_blob
GitHub.create_tree
GitHub.create_commit
GitHub.update_ref(force=false)
```

All other write-capable actions are nonexistent for project execution purposes even if their schemas are visible.

## 4. Recovery method

History must not be reset, rewritten, or force-pushed.

Forward recovery starts from the latest accidental HEAD and creates a new tree that:

1. deletes exactly the three sentinel paths;
2. preserves every other path from the latest branch tree;
3. adds the intended V292 route-reconciliation documentation/state changes;
4. creates one child commit of the latest accidental HEAD;
5. moves `main` only with `update_ref(force=false)` after a final HEAD-drift check.

## 5. Strengthened pre-write gate

Immediately before every repository-writing stage, confirm all of the following:

```text
allowed write actions = create_blob, create_tree, create_commit, update_ref
update_ref.force = false
Contents API writes = forbidden
create_branch = forbidden
write target branch = main
base HEAD = freshly checked remote main HEAD
changed-file set = frozen before first blob
```

After the first `create_blob`, do not rediscover or switch write routes.

If any write action outside the four-action allowlist is selected or invoked, STOP immediately. A fresh explicit user execution signal is required before recovery.

## 6. Repetition prevention

Do not use sentinel/probe files to test write availability.

Do not call `create_file`, `update_file`, `delete_file`, or `create_branch` for convenience, recovery, documentation, or probing.

File addition, replacement, and deletion all use Git objects:

```text
add/replace: create_blob + create_tree entry
remove:       create_tree entry with deletion semantics
commit:       create_commit
canonicalize: update_ref(force=false)
```

This incident record exists so later chats/models/agents do not repeat the same Contents-API route.