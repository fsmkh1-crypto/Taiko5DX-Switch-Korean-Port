# PC DLL PHASE 4 — original handoff provenance closure

Date: 2026-09-11 (KST)
Status: PROVENANCE GAP CLOSED / NO NEW RUNTIME CLAIM

## 1. Purpose

This record closes the transfer/provenance gap that existed when PHASE 4 was first canonicalized. The original Astra PHASE 4 auxiliary artifacts were later supplied by the user and compared against the existing canonical PHASE 4 findings.

This step does not reopen PHASE 4 analysis, does not add Switch counterpart work, and does not create a new runtime-validation claim. V052–V061 remain the PHASE 4 factual validation IDs.

## 2. Supplied artifacts and identity

User-supplied files:

- `PC_RUNTIME_PHASE4_VERIFICATION.json`
  - SHA-256 `68abae6d9299ae698a9e4bfcb37a8807ac5e92a31a53f9bda6be0a83415ee612`
  - 1,371 bytes
- `pc_phase4_probe.py`
  - SHA-256 `bf613c1ac3cfa9d402aec3bb2fd12fc2445f4b3f1357fc8c652637d4a6856a23`
  - 9,467 bytes
- `PHASE4_HELPER_DESCRIPTOR_HANDOFF(1).zip`
  - SHA-256 `3cd2fd7919b67237558bc65dccc25a45900d36541b460903ae64f63f5c6fdaea`
  - 65,347 bytes

The detached JSON and probe script are byte-for-byte identical to the corresponding files inside the ZIP.

The ZIP's own `MANIFEST.json` pins the handoff to starting remote `main`:

`06177d3e67717a890ef8364b8110499c1f4f7b78`

and records the original PHASE 4 report hash:

`docs/PC_RUNTIME_PHASE4_HELPER_DESCRIPTOR_SPEC.md`
SHA-256 `b948a412c3589e399727c6f4dc4dcc992fc8493a849ee71fc1cbc65bc051d0ff`

and original PHASE 4 ledger hash:

`docs/VALIDATION_LEDGER_PHASE4.md`
SHA-256 `fbedbd9b7e2fc99e27a4c248d8fdeb1f763618de0b886e662bd2d38bc6afe381`

## 3. Comparison result against canonical PHASE 4

No incompatible PHASE 4 mechanism claim was found.

The original handoff confirms the canonical facts already carried by V052–V061, including:

- helper length `0x9E`, two descriptor-referenced entries `+0x00` / `+0x20`;
- 42 reachable instruction boundaries;
- unreachable padding `+0x1C..+0x1F` (4 bytes);
- exact helper external rel32 operand offsets `+0x18`, `+0x86`, `+0x90`, `+0x9A`;
- corresponding EXE RVAs `0x6933D5`, `0x6832BC`, `0x6832BC`, `0x68328A`;
- full-.text descriptor search with unique match plus exact-anchor equality;
- nonzero descriptor mask byte means full-byte equality, not bitwise masking;
- kind formulas 0/1/2/3 and kind population `9/2/1/2`;
- 11 descriptors / 14 subpatches;
- application-stage total-14 check separate from parser grammar;
- raw `font_page_limit` threshold change `0xFF -> 0xA0`;
- `runtime_byte_validation` as a copy/control-flow hook with original-path fallback, not a Boolean validator.

The original report is more detailed than the first canonical import because it retains full signature/mask/preimage/payload tables and helper boundary listings.

## 4. Verification artifact result

The supplied verification JSON records:

- mapper inputs: 65,536;
- upper-ECX mapper cases: 256;
- byte-validator lead/trail pairs: 65,536;
- outcomes:
  - one-byte: 16,128;
  - two-byte: 11,280;
  - fallback: 38,128;
- all 42 helper instruction boundaries reached;
- descriptor count 11;
- subpatch count 14;
- kind counts 9/2/1/2;
- six synthetic resolver cases;
- six rel32 boundary cases;
- status: `PASS (bounded static/synthetic verification only)`.

The probe source imports and compiles successfully under Python syntax checking in this provenance session. The JSON was parsed and its key counts/status fields matched the handoff manifest/report.

No T5K resource was re-executed through the probe in this provenance session. Therefore this step verifies artifact identity, internal consistency, and transfer provenance; it does not claim a fresh independent native or game-runtime reproduction.

## 5. Scope limit

The probe itself states its limit: it is a narrow raw-byte interpreter/specification model, not native DLL/EXE execution and not complete x86 fault/EFLAGS emulation.

The original handoff likewise states that it performed no Switch counterpart analysis, ARM64 edit, cave selection, IPS generation, build, or Eden runtime test.

## 6. Canonical effect

The earlier PHASE 4 transfer note saying the auxiliary files were unavailable remains historically true for the first canonical-import moment, but the artifact-availability gap is now closed.

Canonical use after this record:

1. V052–V061 remain unchanged.
2. `docs/PC_RUNTIME_PHASE4_VERIFICATION.json` and `tools/pc_phase4_probe.py` are now preserved in the repository.
3. The original handoff and manifest are preserved under `docs/phase4_handoff/`; the manifest records the original detailed report/ledger hashes and sizes.
4. The existing canonical PHASE 4 report/ledger remain the repository authority; the newly preserved handoff artifacts close the transfer gap without overwriting later closure corrections.
5. Later closure corrections still govern semantic wording where they intentionally narrowed older labels; importing original evidence does not roll those corrections back.
6. No new PHASE or Switch implementation is authorized by this provenance import.
