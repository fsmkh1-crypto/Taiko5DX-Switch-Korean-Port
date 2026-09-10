# AGENTS.md

Operating rules for ChatGPT, Claude, or any other coding/research agent working on this repository.

1. Read `PROJECT_STATE.md` and `PATCH_MAP.md` before starting work.
2. Treat facts marked confirmed there as established unless a new implementation result directly contradicts them.
3. Optimize for an integrated working Eden mod, not endless isolated validation phases.
4. When debugging, use internal feature switches or binary search to isolate failures, but keep the user-facing development build unified.
5. Assume a complete extracted Switch v1.1.3 dump is available locally. Do not redesign the workflow around manually supplying one file at a time.
6. Do not commit XCI/NSP/NCA, Switch executables, PC executables, the PC patch archive/payload, fonts, translated game data, keys, dumps, or generated full mod packages.
7. It is acceptable to commit hashes, sizes, Build IDs, offsets, patch bytes, scripts, manifests, and analysis needed to reproduce the port from locally supplied source material.
8. Never replace Switch `CMENU/CWTDAT_JP.TR5` wholesale with the PC version. Reconstruct only validated changes onto the Switch-native base.
9. Do not treat the 17,103 PC EXE replacement records as a single string blob. They are primarily same-length in-place records and must be mapped to Switch homologous locations.
10. At the end of any meaningful work session, update `PROJECT_STATE.md`, `PATCH_MAP.md` when relevant, and `CHANGELOG.md`.
11. Record failed approaches briefly so later agents do not repeat them.
12. Prefer implementation plus real Eden testing over speculative micro-analysis when both are possible.
13. Final end-user frontend is Android APK first. The APK is a separate patch-generation app that accepts the user's extracted Switch 1.1.3 dump and PC Korean patch archive, then emits an Eden-ready mod using user-granted Android Storage Access Framework locations.
14. Do not create a second independent patch engine for Android. Finish and stabilize the core builder first, then make the APK a frontend/wrapper around the same patch-generation logic.
15. A Windows CLI/EXE may be added later only as a secondary frontend sharing the same core logic.
