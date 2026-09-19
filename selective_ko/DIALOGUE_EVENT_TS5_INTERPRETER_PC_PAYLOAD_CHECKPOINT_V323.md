# DIALOGUE EVENT TS5 INTERPRETER / PC PAYLOAD CHECKPOINT V323

Date: 2026-09-19 (KST)

```text
checkpoint_id   V323
track           SWITCH_SELECTIVE_KOREANIZATION
scope_kind      READ_ONLY_ANALYSIS_CHECKPOINT
product_bytes   UNCHANGED
code            UNCHANGED
build/package   NONE
repository      DOCUMENTATION_ONLY
```

This checkpoint records the bounded Switch EVENT interpreter findings completed after V322, the exact PC Korean-patch `ECF00000.TS5` payload identity re-confirmed in the current session, the availability of the Switch v1.1.3 source package outside the repository, and the explicit stop boundary before the unfinished exact command census.

All earlier VERIFIED/CLOSED facts remain inherited unless explicitly superseded here.

## 1. Switch EVENT bounded caller binding

The bounded trace established:

```text
0x159CA0
  -> 0x1599FC
     -> 0x158A58
        -> 0x440A80
```

Direct-call facts:

- `0x158A58` has one direct BL caller in text: `0x159A24`, inside the function beginning at `0x1599FC`.
- `0x1599FC` has one direct caller: `0x159DE0`, inside the function beginning at `0x159CA0`.
- The direct BL calls in `0x159CA0..0x159E54` are `0x159D9C -> 0x1676C4`, `0x159DC8 -> 0x15F400`, and `0x159DE0 -> 0x1599FC`.
- The scope stopped at this level. No recursive expansion above `0x159CA0` is implied.

At `0x158A58`, the EVENT resource loader obtains the resource through `0x440A80`, reads the first 8 bytes, interprets the upper 32 bits as a count, copies `count + 1` 32-bit offsets from `base + 8`, then indexes that table with the selected event/script index.

The common resource getter `0x440A80` has six direct BL callers:

```text
0x158B90  EVENT
0x18F9C4  separate resource subsystem
0x23A448  separate table-driven resource subsystem
0x2875B4  locale-selected resource family
0x287CE8  SNR-related resource family
0x43F558  TAI5MSG resource family
```

Common resource infrastructure does not imply a common higher-level renderer.

## 2. Switch EVENT interpreter / text opcode findings

The bounded interpreter survey established that `0x15F2C0` participates in the EVENT stream execution loop and that the immediate opcode-dispatch layer around `0x15F44C` dispatches command values in the 1..0x60 range.

Confirmed message-family paths:

```text
0x11 -> handler 0x160334 -> parsed string -> message-text path
0x12 -> handler 0x16049C -> parsed string -> message-text path
0x13 -> handler 0x1605AC -> parsed string -> message-text path
0x15 -> multiple NUL-terminated strings -> list/choice-style UI path
```

For `0x11/0x12/0x13`, string parser `0x157C30` feeds message body engine `0x4BBA24`.

Within `0x4BBA24`:

```text
0x00  string terminator
0x0A  explicit newline
0x1B  inline control escape
other payload  consumed as 1-byte / 2-byte glyph data
```

The engine measures glyph advance rather than using a fixed character counter. The observed general wrap threshold is `0x2CA = 714` pixels, with additional punctuation-related limits including `0x286` and `0x2A8`. Explicit newline and automatic wrap converge on the same line-advance family. The observed page/window progression uses three visual lines, with a `0x30 = 48` pixel line-pitch family.

Therefore the historical “about 20 full-width / 40 half-width characters” statement may be an authoring approximation for this dialogue family, but it is not the Switch runtime algorithm. B24's 52-unit / 788-pixel body rule must not be reused for EVENT dialogue.

Additional bounded findings:

- `0x14` belongs to a message-window termination/state-transition family, but its exact game-semantic label remains unresolved.
- `0x15` is a strong choice/list command candidate because it parses multiple NUL-terminated strings and passes them as a list/array to UI state.
- `0x1E` parses a string into numbered storage slots and is not a direct speaker-text output command.
- Exact game-semantic labels for the distinctions among `0x11/0x12/0x13` remain partially unresolved.

## 3. Exact PC Korean-patch payload identity

The exact PC Korean patch v1.02 executable identity remains:

```text
size    177,267,850
sha256  109dc729e66df8cd0a47c5f6c24719260eb03a89890a0c69d3ba739145dcfb23
```

Do not repeat patcher discovery/reconstruction merely because the chat changes.

The embedded patched payload `data/EVENT/ECF00000.TS5` was re-extracted and matched V322:

```text
size    1,156,480
sha256  0899bf81789acfbd243d43be209a8a3960933fa090960ac8c753c63f95f07bbe
```

Container-header inspection establishes:

```text
script count        782
offset entries      783 (= count + 1)
first script offset 0xC44
header/table size   8 + 783*4 = 0xC44
```

The PC patched `ECF00000.TS5` is therefore ready for a finite command-boundary census.

## 4. Switch original source availability

A combined Switch v1.1.3 XCI is available in the user's Drive/work area, and a user-supplied `prod.keys` is also available outside the repository. The key contents are sensitive and are not copied into Git or recorded here.

```text
Switch v1.1.3 source package  AVAILABLE
prod.keys                     AVAILABLE_OUTSIDE_REPOSITORY
Switch EVENT/SNR RomFS        EXTRACTION_PENDING
```

This supersedes the older wording `NOT_YET_SUPPLIED`. The source package exists; the target EVENT/SNR files have not yet been extracted and canonicalized.

## 5. Incomplete exact census

The intended PC-payload exact census was NOT completed in this chat.

Not yet established:

- exact counts of `0x11/0x12/0x13/0x15` across all 782 scripts;
- exact `0x0A` newline distribution;
- exact `0x1B` inline-control distribution;
- exact choice-list population;
- exact long-line/manual-break statistics.

Two attempts spent excessive time in input re-identification/parser preparation before producing the finite census. No product bytes, code, build, package, or repository state were changed by those attempts.

Do not report any of these census values as known until the finite parser completes.

## 6. Exact next scope

After a fresh explicit user execution signal:

`DIALOGUE_EVENT_TS5_PC_PATCH_EXACT_COMMAND_CENSUS_READ_ONLY`

Boundaries:

1. Reuse the exact PC `ECF00000.TS5` identity above. Do not reconstruct/re-identify the patcher unless bytes contradict the recorded SHA.
2. Walk exactly 782 script ranges from the verified offset table.
3. Follow actual command boundaries. Do not raw-scan payload bytes for opcode values.
4. Resolve only command-length rules required to walk the corpus and count `0x11/0x12/0x13/0x15`, `0x0A`, and `0x1B`.
5. If an unknown command prevents safe stepping, stop at the first exact script/offset/opcode and report it rather than expanding into a full 96-opcode semantic reverse engineering.
6. No Switch RomFS comparison, translation change, reflow implementation, build/package, or repository write inside that analysis scope.

The subsequent source-comparison stage waits for Switch v1.1.3 EVENT/SNR extraction.
