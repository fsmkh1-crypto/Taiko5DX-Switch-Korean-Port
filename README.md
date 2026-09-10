# Taiko5DX Switch Korean Port

Nintendo Switch porting workspace for the Korean patch of **TAIKO RISHHIDEN V DX / 太閤立志伝V DX**.

## Target

- Nintendo Switch version: **1.1.3**
- Title ID: `0100346017304000`
- NSO Build ID: `D9120950C258610A746F4A31CE3A3B376DE393D9`
- PC source patch: `Taiko5DX_Korean_Patcher_v1.02`
- Primary test target: **Eden Android**

## Project policy

This repository contains only porting code, patch metadata, hashes, offsets, analysis notes, and build logic. It does **not** contain commercial game files, Nintendo content, the original PC executable, the Korean patch payload, fonts, translated game data, or generated full mod packages.

The current development assumption is that the developer has a complete extracted **Switch 1.1.3 dump** available locally, including ExeFS `main` and RomFS. The builder may use that dump directly instead of asking end users to manually supply individual files one by one.

Read `PROJECT_STATE.md` and `PATCH_MAP.md` before continuing any porting work.
