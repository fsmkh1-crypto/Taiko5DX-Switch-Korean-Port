# AGENTS.md

Operating rules for ChatGPT, Claude, or any other coding/research agent working on this repository.

1. **Mandatory pre-read:** before any analysis, implementation, validation, IPS generation, or crash diagnosis, read `PROJECT_STATE.md`, `docs/VALIDATION_LEDGER.md`, `PATCH_MAP.md`, `docs/INLINE_VALIDATION_POLICY.md`, and `docs/RUNTIME_TEST_RESULTS.md` as applicable. For any question of whether a fact must be checked again, `docs/VALIDATION_LEDGER.md` is the first authority.
2. **No redundant revalidation:** before repeating any previously performed check, consult `docs/VALIDATION_LEDGER.md`. A recorded `VERIFIED` or `VERIFIED-RUNTIME` result must be reused unless an allowed revalidation trigger exists: changed input/version/hash, contradictory new evidence, inadequate provenance for the current high-risk decision, or proof that the old method was unsound. A new chat, new agent, or new model is never by itself a reason to revalidate.
3. When revalidation is legitimately required because an old result is ambiguous or poorly documented, perform it once and record enough provenance to prevent future repetition: validation ID/date, exact claim, input identity/hash/version, method/script and parameters, offsets/ranges/count units, observed result, final status, and reproducible artifact/report/commit path.
4. Treat facts marked confirmed in the canonical documents as established unless a new implementation result directly contradicts them or the ledger explicitly marks them `VERIFIED-LEGACY` / `NEEDS-REVERIFY` for the decision at hand.
5. Optimize for an integrated working Eden mod, not endless isolated validation phases.
6. When debugging, use internal feature switches or delta debugging only to isolate a reproducible failure; never infer that a passing split is globally safe.
7. Assume a complete extracted Switch v1.1.3 dump is available locally. Do not redesign the workflow around manually supplying one file at a time.
8. Do not commit XCI/NSP/NCA, Switch executables, PC executables, the PC patch archive/payload, fonts, translated game data, keys, dumps, or generated full mod packages.
9. It is acceptable to commit hashes, sizes, Build IDs, offsets, patch bytes, scripts, manifests, and analysis needed to reproduce the port from locally supplied source material.
10. Never replace Switch `CMENU/CWTDAT_JP.TR5` wholesale with the PC version. Reconstruct only validated changes onto the Switch-native base.
11. Do not treat the 17,103 PC EXE replacement records as a single string blob. They are primarily same-length in-place records and must be mapped to Switch homologous locations.
12. At the end of any meaningful work session, update `docs/VALIDATION_LEDGER.md` for new/revalidated/invalidated facts, plus `PROJECT_STATE.md`, `PATCH_MAP.md` when relevant, and `CHANGELOG.md`.
13. Record failed approaches briefly so later agents do not repeat them.
14. Prefer implementation plus real Eden testing over speculative micro-analysis when both are possible, but do not bypass mandatory static safety gates for inline patches.
15. Final end-user frontend is Android APK first. The APK is a separate patch-generation app that accepts the user's extracted Switch 1.1.3 dump and PC Korean patch archive, then emits an Eden-ready mod using user-granted Android Storage Access Framework locations.
16. Do not create a second independent patch engine for Android. Finish and stabilize the core builder first, then make the APK a frontend/wrapper around the same patch-generation logic.
17. A Windows CLI/EXE may be added later only as a secondary frontend sharing the same core logic.
18. **Do not assume direct filesystem access to Eden's internal Android folder.** In the actual target environment the user could not access the Eden folder directly. Development-build instructions must use Eden's own per-game Add-ons installer (`+ Install` -> `Mods and cheats`) with an extracted mod root containing `exefs/` and/or `romfs/`.
19. Keep `docs/EDEN_ANDROID_TEST_GUIDE.md` aligned with every development build when installation or required test observations change.
20. **Inline-validation invariant:** `unique exact match` is candidate-discovery evidence only, never a release-safety criterion. Final inclusion must follow `docs/INLINE_VALIDATION_POLICY.md`.
21. **Full-corpus target:** the validator must be designed for all 17,103 T5K inline records. The old 5,519 exact-unique rodata subset is only a regression/reference set and must not be treated as pre-approved.
22. **Release gate for inline patches:** valid game encoding, PC↔Switch structural homology, independently established Switch field/boundary structure, no unresolved conflicts/severe binary risk, and simulated post-patch offline validation are mandatory. Runtime success alone cannot promote a candidate to SAFE.
23. **User start gate:** when the user is discussing, reviewing, or planning work, do not create builds, modify code, or commit implementation changes until the user gives an explicit execution signal such as `시작`, `해`, or `진행`. A direct request to save/update documentation counts only for that requested documentation action, not as authorization to begin unrelated implementation work.
