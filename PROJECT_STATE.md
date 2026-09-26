# PROJECT_STATE

Last updated: 2026-09-26 (KST)

This file is the sole repository-level project-resume authority.

## Active product

Status: `FINAL_PRODUCT_CANONICAL_REPRODUCTION_ADOPTED / USER_RUNTIME_OBSERVED_PASS`

Target:

- TitleID `0100346017304000`
- Nintendo Switch v1.1.3
- Build ID `D9120950C258610A746F4A31CE3A3B376DE393D9`

Canonical final payload identities:

```text
TAI5MSG_JP.DAT
  bytes   2,276,425
  records 16,153
  sha256  1b44170a817e047ba942ba10e46571049ff7405c7fac4278c3e1598089efd61e

BuildID IPS
  bytes   2,999
  records 18
  sha256  28c423a0a8e805308f8e935f2a3f5304fe12e3f948ca6468c46dd72a96cdcfae
```

The final builder reproduces those bytes from the Diagnostic218 TAI5MSG, inherited 5-record IPS, exact Switch v1.1.3 `main`, and frozen plans in `selective_ko/final_product_v1/`.

The user-observed runtime-pass reference ZIP is preserved as a large artifact:

- SHA-256 `cfd14031bab300929a9926bae9bb82bf28f21a9d417aee50ca527b88df873c91`
- Google Drive ID `1yCgjdWKQUTpwEfLll_Y29ztKG96EkXv2`

Implementation/proof archive:

- Google Drive ID `1jiFlitnhVpH0KOBcONfGG6zgcpaXsDme`
- source implementation evidence was verified before this Git adoption.

<!-- PROJECT_RESUME_V2
{"schema":"PROJECT_RESUME_V2","scope_id":"FINAL_PRODUCT_CANONICAL_REPRODUCTION_V1","scope_kind":"CANONICAL_PRODUCT","status":"ADOPTED_USER_RUNTIME_OBSERVED_PASS","repository_write_mode":"GIT_OBJECT_ONLY_WRITE_MODE","repository_write_allowed_actions":["create_blob","create_tree","create_commit","update_ref"],"repository_update_ref_force":false,"active_product_track":"SWITCH_SELECTIVE_KOREANIZATION","selective_subtree_resume_authority":"selective_ko/SELECTIVE_PROJECT_STATE.md","exact_next_scope_authority":"selective_ko/SELECTIVE_PROJECT_STATE.md","current_builder":"builder/final_product_candidate.py","current_plan_index":"selective_ko/final_product_v1/INDEX.json","current_verification":"selective_ko/final_product_v1/FINAL_PRODUCT_REPRO_VERIFICATION.json","current_failure_authority":"selective_ko/final_product_v1/KNOWN_FAILURES.json","runtime_reference_zip_sha256":"cfd14031bab300929a9926bae9bb82bf28f21a9d417aee50ca527b88df873c91","runtime_reference_drive_id":"1yCgjdWKQUTpwEfLll_Y29ztKG96EkXv2","rootcause223_tai_sha256":"8c9a70575258fad362c0197c8b59190fd332843195f35e185894ee34fe6547b1","final_tai_sha256":"1b44170a817e047ba942ba10e46571049ff7405c7fac4278c3e1598089efd61e","final_ips_sha256":"28c423a0a8e805308f8e935f2a3f5304fe12e3f948ca6468c46dd72a96cdcfae","defective_ips_do_not_use":"dadb49f92fd66313145620194b05c108373f780f566bd5ba433f045e8acef7ec","v371_event_disposition":"HISTORICAL_NOT_PROMOTED_SUPERSEDED_FOR_CURRENT_PRODUCT","priority_next_scope":"ADVANCED_POLISH_CONTINUE_FROM_ROADMAP","advanced_polish_roadmap":"selective_ko/advanced_polish/ADVANCED_POLISH_ROADMAP_20260926.md","font_a_diagnostic_runtime_status":"NOT_YET_CONFIRMED","optional_next_scope":"CANONICAL_RELEASE_METADATA_REFRESH_AND_RUNTIME_RETEST","required_reads":["selective_ko/SELECTIVE_PROJECT_STATE.md","selective_ko/advanced_polish/ADVANCED_POLISH_ROADMAP_20260926.md","selective_ko/final_product_v1/INDEX.json","selective_ko/final_product_v1/FINAL_PRODUCT_REPRO_VERIFICATION.json","selective_ko/final_product_v1/KNOWN_FAILURES.json"],"active_read_budget_max":8}
PROJECT_RESUME_V2 -->

## Provenance closure

Final RootCause223 lowering is fully accounted:

```text
196 layer       120 rewritten callers + 4 exact no-op sites + 628 helpers
699 layer       699/699 source preimages; 367 sites -> B18 views; 332 preserve original helper
B18             693/693 helpers reachable from 77 entry roots; orphan 0
combined        430 changed baseline caller messages / 1,321 appended helpers
unaccounted     0 callers / 0 helpers
```

B23 Switch reflow is a final independent TAI stage:

```text
B23 messages     617
reflowed         462
preserved        155
whitespace edits 1,844
non-whitespace   0
over-32 residual 0
```

## V371 disposition

The historical V371 EVENT replay remains technically partial (54/169 replayed, 115 unreplayed), but it is **not promoted into the current product** and is **not a blocker** for the current runtime-pass carrier.

Preserve V371 artifacts and history. Do not report V371 as 169/169 complete. Resume it only under a new explicit historical/research scope.

## Known failure boundaries

- `dadb49f9...` Buffer8 IPS is a confirmed startup-freeze artifact and is **DO NOT USE**.
- changing the proven top-level mod folder created a patch-loading failure during B23 packaging; do not repeat that packaging shortcut.
- the known-working runtime reference ZIP intentionally retains stale pre-B23 package-info metadata; do not rewrite it in place.

Detailed current authority: `selective_ko/final_product_v1/KNOWN_FAILURES.json`.

## Advanced polish track

The runtime-pass product above remains immutable. A separate quality-polish track is now active.

Roadmap authority:

`selective_ko/advanced_polish/ADVANCED_POLISH_ROADMAP_20260926.md`

Current exact continuation point:

`FONT_A_RUNTIME_VALIDATION_AWAIT_USER_OBSERVATION`

The Font A diagnostic changes only `FONT_JPN.G1T`; it is not yet promoted into the canonical product. After Font A runtime closure, the preferred low-risk order is dialogue-quality audit -> untranslated-text audit -> names/places excluding world map -> terminology -> speech-register polish -> world-map labels -> broad runtime QA.

## Other optional maintenance scope

`CANONICAL_RELEASE_METADATA_REFRESH_AND_RUNTIME_RETEST`

This maintenance scope is separate from quality polish and must not overwrite the immutable runtime-pass reference.

Git writes remain restricted to:

`create_blob -> create_tree -> create_commit -> update_ref(force=false)`.
