# Full-port inventory/accounting validator — Stage 1

Date: 2026-09-11  
Status: IMPLEMENTED / CI VERIFIED / CANONICAL DATA RUN BLOCKED BY EXECUTION BACKEND

## 1. Scope

This stage implements the first read-only validator required by:

- `docs/PC_TO_SWITCH_PORTING_RULE_FRAMEWORK.md`
- `docs/PC_TO_SWITCH_ACCOUNTING_INVARIANTS.md`

No builder transformation, IPS generation, ZIP generation, game-file edit, or runtime diagnostic build was authorized or performed.

The implementation is:

- `tools/full_port_inventory.py`

CI definition:

- `.github/workflows/inventory-validator-ci.yml`

## 2. Intended inputs

Canonical inputs selected for the first run:

### Switch `main`

Google Drive source:

- file ID: `1nfnXSCmSHp0rP_bbDNSyhKCroKSTtTPQ`
- streamed file name: `main.bin`
- provider size: 5,287,359 bytes

Canonical expected identity already established by project records:

- SHA-256 `b366e692208f3c0cc18bc1884ef95689b6b11d722fa2d749b8500abccbc3109b`
- Build ID `D9120950C258610A746F4A31CE3A3B376DE393D9`

### PC Korean patch package

Google Drive source:

- file ID: `1dYepodubrgFKIVByUtITkpclRJSGKbDE`
- file name: `Taiko5DX_Korean_Patcher_v1.02.zip`
- provider size: 170,498,865 bytes

Canonical expected identity already established by project records:

- patch ZIP SHA-256 `df1b62de95e992369e9686c9731d814e7a7e4634888f610430635429e24f7cec`
- embedded `dinput8.dll` SHA-256 `ffe7e9da8e00c96bec631b45a3e9c4d3f314551623351f3e7024e0318913c6b7`
- T5K121R SHA-256 `5c6f4eba8c6f0516365e4518f27e9d8c840aead463b5a2938dd1e08b99726d29`

The validator fails closed if these input identities do not match.

## 3. Implemented Stage-1 behavior

The validator is read-only with respect to game inputs and performs these operations:

1. verifies canonical Switch main / Build ID / PC patch ZIP / DLL / T5K identities;
2. decompresses Switch NSO into the canonical mapped-flat coordinate system;
3. parses the canonical RELA table;
4. inventories the three 3,803-entry localization source tables;
5. derives localization object language-domain ownership from RELA addends;
6. parses all PC source denominators:
   - 17,103 inline records;
   - 56 pointer records;
   - 10,036 mapping entries;
   - 11 descriptor containers;
   - 14 descriptor subpatches;
   - 2 helper semantic entries;
   - 208 RomFS package data items;
7. creates stable source IDs and a source ledger;
8. records raw Switch candidate occurrences without treating uniqueness as a safety proof;
9. records candidate segment/storage and exact localization-start language-domain information;
10. recognizes the already-VERIFIED Japanese place-table name/yomi field starts as structural candidates;
11. creates an exception queue rather than silently dropping nonmatches/multiples/conflicts;
12. emits a preliminary invariant ledger.

Stage 1 deliberately does **not** promote raw unique matches to terminal `DIRECT_PORT`. The tool records discovery evidence only until independent object/structure rules authorize a terminal action.

## 4. Output contract

A successful canonical run emits only reports under `--out-dir`:

```text
SUMMARY.json
source_ledger.jsonl
switch_inventory.json
switch_action_proposals.jsonl
invariants.json
localization_language_inventory.json
exceptions.jsonl
evidence_fanout.json
OUTPUT_HASHES.json
```

Expected Stage-1 mutation state:

```text
input game-file mutations = 0
IPS emitted               = 0
game files emitted        = 0
```

## 5. CI verification

GitHub Actions workflow `Inventory validator CI` run `34603558396`, job `103276457698`, completed successfully.

Verified steps:

- dependency install PASS;
- `python -m py_compile tools/full_port_inventory.py builder/build.py builder/t5k.py` PASS;
- `python tools/full_port_inventory.py --help` PASS.

Therefore the committed Stage-1 validator is syntactically valid under Python 3.12 and its CLI/import path initializes successfully in the repository CI environment.

## 6. Canonical data-run blockage

The actual canonical-input run was attempted in the active ChatGPT execution environment after both Drive inputs had been streamed into the session.

The execution backend failed independently of validator logic:

- `container.exec` timed out even for a trivial `echo` / `/bin/true` command;
- private Python execution timed out even for `print("ok")`;
- user-visible Python execution likewise timed out before reading the inputs.

The error class reported by the execution backend was `TransportTimeoutError`.

Because the failure occurs on commands that do not touch the validator or binaries, this stage does **not** classify it as a validator/data failure.

Status:

```text
validator syntax/CLI        PASS
canonical inputs identified PASS
canonical data execution    BLOCKED_EXECUTION_BACKEND
accounting measurements     NOT PRODUCED
new numeric corpus claims   NONE
```

No externally reported measurement such as PC `.data` counts or NUL-window counts was promoted to canonical fact.

## 7. Exact resume command

When an execution environment capable of reading the canonical files is available, the next operation is only:

```bash
python tools/full_port_inventory.py \
  --main <canonical Switch v1.1.3 main> \
  --pc-patcher <Taiko5DX_Korean_Patcher_v1.02.zip> \
  --out-dir <read-only report directory>
```

The first successful run must then be checked for:

1. all input-identity gates PASS;
2. all source denominator checks PASS;
3. 3,803 × 3 localization source-table inventory completeness;
4. RELA totals matching canonical R0 facts;
5. RomFS data-file denominator = 208;
6. deterministic report hashes on a repeat run;
7. no input mutations / no IPS / no game-file outputs.

Only after that report is recorded should the project begin promoting reusable structural classification rules from the exception/candidate populations.

## 8. Stop boundary

This stage stops here because the remaining first-run work is blocked by the external execution backend, not by an unresolved project hypothesis.

No patch implementation or runtime build follows from this report without a fresh user execution signal.
