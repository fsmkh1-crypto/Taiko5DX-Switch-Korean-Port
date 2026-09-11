# PHASE 4 repository handoff

starting remote main SHA: `06177d3e67717a890ef8364b8110499c1f4f7b78`
PHASE 4 analysis: COMPLETE (static DLL/T5K scope)
documentation: COMPLETE
local commit: NOT ATTEMPTED / not required
Git authentication / push / remote write: NOT ATTEMPTED (explicitly out of scope)

## Files to integrate

Created:

- `docs/PC_RUNTIME_PHASE4_HELPER_DESCRIPTOR_SPEC.md`
- `docs/VALIDATION_LEDGER_PHASE4.md`
- `docs/PC_RUNTIME_PHASE4_VERIFICATION.json`
- `tools/pc_phase4_probe.py`

Modified locally from the pinned remote version:

- `docs/PC_RUNTIME_REVERSE_ENGINEERING.md`
- `docs/VALIDATION_LEDGER.md`
- `PROJECT_STATE.md`
- `CHANGELOG.md`

new validation IDs: V052–V061
PROJECT_STATE new resume status: PC DLL PHASE 4 complete / handoff / STOP;
PC Runtime Canonical Closure is pending a separate explicit user execution signal.

recommended commit message:

`docs: complete PC DLL phase 4 helper and descriptor runtime analysis`

## What the receiving agent must preserve

The bundle contains full replacements for only the four modified files and four new
files, plus a textual unified diff and a SHA-256 manifest. `baseline_sha256` in the
manifest identifies the exact pinned remote bytes of each modified file. Check against
the current canonical version before integration; merge legitimate newer changes rather
than overwriting them. Do not reset/revert history or force-push. This package does not
grant a new remote-publication permission or authorize the next analysis phase.

The remote PHASE3 ledger ends at V051. An earlier unpushed local PHASE3 draft used
different V052/V053 numbering. Do not import that old draft over this canonical lineage.
All prior PHASE1–3 records, AGENTS and PC_RUNTIME_DLL_SPEC are unchanged in this handoff.

## Findings requiring careful closure wording

1. The descriptor resolver requires full-.text uniqueness AND exact declared-anchor
   equality. A unique signature match elsewhere is rejected. Actual live success was
   not observed; under success, W=M+anchor+subpatch_offset.
2. Four helper fixups use fixed EXE RVAs. Helper+0 has a fast RET and a replayed-prologue
   fallback. Helper+20 is a copy/native-continuation hook, not a Boolean validator.
3. Mask bytes select complete-byte equality when nonzero; they are not bitmasks.
4. Kinds0–2 ignore arg; kind3 uses it as a byte offset into H and writes E9 rel32.
5. 14 is an application-stage code-subpatch count requirement, while PHASE2 correctly
   says it is not a parser hard denominator. These are compatible facts.
6. UI/font/threshold raw operand changes are specified separately from unconfirmed
   screen/callee/result-unit interpretations. Preserve prior V029 provenance.
7. Static helper-local and DLL generation contracts are complete. Whole native EXE
   continuations, exact symbols/callers/UI meaning and live success remain unverified.

## Validation and limits

The reproducer accepts only the known T5K resource hash and does not use the builder,
an EXE, network access or executable output. It includes a narrow raw-byte helper
interpreter plus specification-model search/formula checks. All 42 reachable boundaries,
65,536 mapper inputs, 256 upper-ECX cases and 65,536 lead/trail pairs were checked.
The model is not a general x86/fault/EFLAGS emulator or a native runtime test.
11 descriptors / 14 subpatches / kind population9,2,1,2 and25 required answers are present.

No input DLL/T5K/EXE, fonts, game data, keys or generated mod package is included.
The ZIP is a documentation/source handoff only. No closure, PHASE5, Switch counterpart,
ARM64, cave, IPS, build or Eden testing has been performed. STOP.
