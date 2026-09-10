# CHANGELOG

## 2026-09-10

### Repository initialization

- Established Nintendo Switch v1.1.3 / Title ID / NSO Build ID as the fixed development target.
- Adopted full extracted Switch 1.1.3 dump as the standard local development input.
- Documented the existing PC Korean patch as the source implementation to port rather than rebuilding translation assets from scratch.
- Recorded confirmed PC payload composition: 208 game-data replacements plus `dinput8.dll`.
- Recorded the Switch CWTDAT structural exception.
- Recorded the confirmed 64-page Korean font layout and custom Korean byte-code range.
- Recorded Switch text/font functions at `0x430350`, `0x4305D0`, `0x446310`, and `0x446420`.
- Recorded and implemented the first ARM64 page-mapper rewrite adding `EB~F8 -> pages 49~62`.
- Recorded exact mapping counts: 7,494 original + 2,542 Korean = 10,036.
- Corrected previous misunderstanding of 17,103 PC EXE records: they are primarily same-length in-place replacement records, not a monolithic injected text blob.
- Established integrated-build-first workflow and Eden Android as the primary test target.

### Existing local proof-of-concept

A local P0 Eden mod was produced containing:

- Build-ID IPS with the page-mapper patch
- PC Korean-patched `FONT_JPN.G1T`
- one translated EVENT TS5 smoke-test file

This P0 is a development artifact only and is not stored in this public repository.
