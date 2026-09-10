# AGENTS.md

Operating rules for ChatGPT, Claude, or any other coding/research agent working on this repository.

1. Read `PROJECT_STATE.md`, `PATCH_MAP.md`, and `docs/INLINE_VALIDATION_POLICY.md` before starting work that touches inline mapping, text validation, IPS generation, or crash diagnosis.
2. Treat facts marked confirmed there as established unless a new implementation result directly contradicts them.
3. Optimize for an integrated working Eden mod, not endless isolated validation phases.
4. When debugging, use internal feature switches or delta debugging only to isolate a reproducible failure; never infer that a passing split is globally safe.
5. Assume a complete extracted Switch v1.1.3 dump is available locally. Do not redesign the workflow around manually supplying one file at a time.
6. Do not commit XCI/NSP/NCA, Switch executables, PC executables, the PC patch archive/payload, fonts, translated game data, keys, dumps, or generated full mod packages.
7. It is acceptable to commit hashes, sizes, Build IDs, offsets, patch bytes, scripts, manifests, and analysis needed to reproduce the port from locally supplied source material.
8. Never replace Switch `CMENU/CWTDAT_JP.TR5` wholesale with the PC version. Reconstruct only validated changes onto the Switch-native base.
9. Do not treat the 17,103 PC EXE replacement records as a single string blob. They are primarily same-length in-place records and must be mapped to Switch homologous locations.
10. At the end of any meaningful work session, update `PROJECT_STATE.md`, `PATCH_MAP.md` when relevant, and `CHANGELOG.md`.
11. Record failed approaches briefly so later agents do not repeat them.
12. Prefer implementation plus real Eden testing over speculative micro-analysis when both are possible, but do not bypass mandatory static safety gates for inline patches.
13. Final end-user frontend is Android APK first. The APK is a separate patch-generation app that accepts the user's extracted Switch 1.1.3 dump and PC Korean patch archive, then emits an Eden-ready mod using user-granted Android Storage Access Framework locations.
14. Do not create a second independent patch engine for Android. Finish and stabilize the core builder first, then make the APK a frontend/wrapper around the same patch-generation logic.
15. A Windows CLI/EXE may be added later only as a secondary frontend sharing the same core logic.
16. **Do not assume direct filesystem access to Eden's internal Android folder.** In the actual target environment the user could not access the Eden folder directly. Development-build instructions must use Eden's own per-game Add-ons installer (`+ Install` -> `Mods and cheats`) with an extracted mod root containing `exefs/` and/or `romfs/`.
17. Keep `docs/EDEN_ANDROID_TEST_GUIDE.md` aligned with every development build when installation or required test observations change.
18. **Inline-validation invariant:** `unique exact match` is candidate-discovery evidence only, never a release-safety criterion. Final inclusion must follow `docs/INLINE_VALIDATION_POLICY.md`.
19. **Full-corpus target:** the validator must be designed for all 17,103 T5K inline records. The old 5,519 exact-unique rodata subset is only a regression/reference set and must not be treated as pre-approved.
20. **Release gate for inline patches:** valid game encoding, PC↔Switch structural homology, independently established Switch field/boundary structure, no unresolved conflicts/severe binary risk, and simulated post-patch offline validation are mandatory. Runtime success alone cannot promote a candidate to SAFE.
21. **User start gate:** when the user is discussing, reviewing, or planning work, do not create builds, modify code, or commit implementation changes until the user gives an explicit execution signal such as `시작`, `해`, or `진행`. A direct request to save/update documentation counts only for that requested documentation action, not as authorization to begin unrelated implementation work.
