# SWITCH ORIGINAL SOURCE INPUT CONTRACT

Date: 2026-09-17 (KST)
Status: CANONICAL EXTERNAL-INPUT CONTRACT / SOURCE NOT YET REQUIRED
Track: `SWITCH_SELECTIVE_KOREANIZATION`

## 1. Purpose

This document defines where and how future Nintendo Switch original sources should be supplied when a later read-only structural scope needs XCI-derived RomFS/ExeFS authority.

The user does **not** need to provide these files now.

When they become necessary, the user may extract them from the XCI and place them under the layout below. Extraction procedure can be provided at that time.

## 2. Google Drive storage location

Use the existing project Drive area and create/use this relative layout:

```text
태합입지전 프로젝트/
└─ Switch/
   └─ Original_v1.1.3/
      ├─ exefs/
      │  └─ main
      └─ romfs/
         └─ <preserve the XCI-extracted relative RomFS tree exactly>
```

Do not flatten the extracted RomFS tree.

Do not rename files merely to match PC patch paths.

Do not mix PC-original or PC-Korean-patch files into this directory.

The directory is an external source bundle, not a repository payload.

## 3. Preferred supply form

Preferred:

- exact Switch v1.1.3 `exefs/main`;
- extracted `romfs/` tree preserving original directory/file names and relative paths.

A full RomFS tree is preferred because future container ownership may cross file families and because preselecting only guessed EVENT/SNR/TAI5MSG paths can accidentally omit structural dependencies.

If storage size later makes a full RomFS upload impractical, first provide a file listing from the extracted RomFS. The required subtrees can then be selected from their **actual Switch paths**, not guessed from PC filenames.

## 4. Source families expected to matter later

Current analysis indicates that later structural scopes may need original Switch counterparts for families including:

- TAI5MSG;
- EVENT/TS5;
- SNR/scenario data;
- UI/description/static tables where identified;
- other referenced data discovered by owner/caller analysis.

This list is a planning hint only. It does not declare exact Switch paths or assert PC/Switch path equality.

## 5. Integrity procedure after the files are supplied

After upload, before using any source as structural authority:

1. record exact relative path;
2. record file size;
3. record SHA-256;
4. bind source identity to Switch v1.1.3 / title `0100346017304000`;
5. preserve the raw file unchanged;
6. perform analysis on copies or read-only access;
7. never substitute a PC file merely because its filename is similar.

`exefs/main` retains the already-known Switch build identity guard and should be checked against the canonical v1.1.3 target before any structural conclusion is extended to newly supplied RomFS data.

## 6. Current status

```text
source_bundle_status = NOT_YET_SUPPLIED
supply_timing        = WHEN_A_LATER_SCOPE_REQUIRES_SWITCH_ORIGINAL_STRUCTURE
current_blocker      = false
```

The absence of this bundle does not block V295 documentation correction and does not authorize guessing Switch structure.

## 7. User handoff

When the project reaches a scope that needs these files, tell the user:

1. which exact source family is now required;
2. whether a full RomFS tree or a smaller exact subtree is sufficient;
3. the XCI extraction method appropriate at that time;
4. the Drive destination above.

Until then, do not repeatedly request the XCI extraction.
