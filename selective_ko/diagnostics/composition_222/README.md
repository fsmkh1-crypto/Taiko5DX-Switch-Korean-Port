# Composition diagnostic 222

This is a bounded expanded-profile experiment, not a release or V371 closure.
V369_UNCHANGED; V371_PARTIAL_BLOCKED. Runtime has not been run.

The exact diagnostic 218 baseline is required. Original source identities remain
14,832 records. Eighteen original message programs change: sixteen from the
preceding whole-message plan, plus aliases B21:131 and B21:133. Forty specialized
helper programs are appended at B0:471..510. All original 471 B0 programs remain
unchanged. The experimental total is 14,872; B0 has 511 records. This profile is
separate from the canonical fixed-count serializer, which remains unchanged.

The reviewed 36 CALL sites in five messages use dedicated helpers. Original
conditions, variable fields and words are preserved. Eight dynamic terminal
records retain their original suffix; one empty-local fallback also preserves
it. This is not general runtime particle handling or all-dialogue correction.

PC_PATCH_ORACLE_GATE=PASS for inherited exact stored-data evidence only. The
particle rule is a Switch-specific correction, not proof of PC runtime parity.
The lineage archive and frozen plan hashes are in CONTRACT.json.

## Reproduction

Python standard library only. MESSAGE_PLAN.json is an immutable exact-byte write
plan. CONTRACT.json binds the baseline, main, source preimages and clone sources.
The source receipt must identify the actual pre-build repository commit and the
five frozen files: build.py, readback.py, CONTRACT.json, MESSAGE_PLAN.json, README.md.

    python build.py --baseline DIAG218.zip --main SWITCH_113_main.nso --out OUT --check
    python build.py --baseline DIAG218.zip --main SWITCH_113_main.nso --out OUT --source-receipt SOURCE_RECEIPT.json --source-commit COMMIT

--check emits no game bytes. Generation requires the source freeze. The separate
readback module independently checks stored block extents, explicit counts,
offsets, all 14,872 payloads and the B32 omitted-tail contract. Negative probes
must reject header, count, original-payload and appended-helper corruption.

Only TAI5MSG_JP.DAT and package metadata change. The inherited thirteen EVENT
files, font and IPS remain byte-identical. ZIP names and contents are reread.
Installed game version/main identity and actual emulator loading remain unverified.

## Installation and observation

For the intended Switch 1.1.3 / TitleID 0100346017304000 diagnostic only.
Extract the single Taiko5DX_KR_DIAG_222_COMPOSITION mod folder into the title's
mod location. Disable prior Taiko Korean diagnostic mods before enabling this
one, to prevent overlapping romfs/exefs files. Keep a copy of the previously
used mod. This does not modify save data.

Record the exact ZIP/hash, installed game update and emulator version when
reporting a result. Revisit ordinary first meetings and the previously malformed
dialogues, but do not assume every such message is included in the eighteen
changed records. Include preceding/following text and actor identity in evidence.

Do not claim global coverage, semantic release admission, PC runtime parity or
V371 closure from packaging/readback tests. TE5, SNR, source identity holds,
inline 139, non-B24 reflow, B0:181/307 and suffix3/root obligations, EVENT-to-TAI
relations, legacy version/evidence gaps and circular readback concerns retain
their prior scope. The original 48/46/5 root denominators are not the forty new
experimental helpers.
