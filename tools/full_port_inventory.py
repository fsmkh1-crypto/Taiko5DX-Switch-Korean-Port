#!/usr/bin/env python3
"""Read-only full PC->Switch inventory/accounting validator.

This tool NEVER emits IPS, mutates game files, or modifies input binaries.
It consumes the canonical PC patch ZIP and Switch v1.1.3 ExeFS/main, then
writes accounting/inventory reports only under --out-dir.

The first-stage policy is deliberately conservative: discovery evidence is
recorded, but raw/unique matches are not promoted to terminal DIRECT_PORT
outcomes without an independently established object/structure rule.
"""
from __future__ import annotations

import argparse
from collections import Counter, defaultdict
import hashlib
import json
from pathlib import Path
import struct
import sys
from typing import Any, Iterable

REPO_ROOT = Path(__file__).resolve().parents[1]
BUILDER_DIR = REPO_ROOT / "builder"
if str(BUILDER_DIR) not in sys.path:
    sys.path.insert(0, str(BUILDER_DIR))

from build import (  # noqa: E402
    BUILD_ID_FULL,
    BUILD_ID_NAME,
    DATA_MEM_OFF,
    DATA_SIZE,
    RODATA_MEM_OFF,
    RODATA_SIZE,
    TEXT_MEM_OFF,
    TEXT_SIZE,
    decompress_nso,
    open_payload,
)
from t5k import (  # noqa: E402
    extract_t5k_rcdata,
    find_pattern_occurrences,
    parse_t5k_resource,
)

CANONICAL_MAIN_SHA256 = "b366e692208f3c0cc18bc1884ef95689b6b11d722fa2d749b8500abccbc3109b"
CANONICAL_PATCHER_SHA256 = "df1b62de95e992369e9686c9731d814e7a7e4634888f610430635429e24f7cec"
CANONICAL_DINPUT_SHA256 = "ffe7e9da8e00c96bec631b45a3e9c4d3f314551623351f3e7024e0318913c6b7"
CANONICAL_T5K_SHA256 = "5c6f4eba8c6f0516365e4518f27e9d8c840aead463b5a2938dd1e08b99726d29"
CANONICAL_ROMFS_ITEMS = 208

# R0/R1 verified Switch structural facts.
RELA_START = 0x58D078
RELA_SIZE = 0xECC70
RELA_ENT = 0x18
R_AARCH64_RELATIVE = 1027
LOCALIZATION_COUNT = 3803
LOCALIZATION_TABLES = {
    "JP": 0x9C0008,
    "CN": 0x9C76E0,
    "TW": 0x9CEDB8,
}
LOCALIZATION_DEST_BASE = 0xA210E0
PLACE_TABLE_BASE_JP = 0x6ADA10
PLACE_TABLE_COUNT = 310
PLACE_TABLE_STRIDE = 0x18
PLACE_NAME_OFF = 0x01
PLACE_NAME_SIZE = 11
PLACE_YOMI_OFF = 0x0C
PLACE_YOMI_SIZE = 12


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for block in iter(lambda: f.read(1024 * 1024), b""):
            h.update(block)
    return h.hexdigest()


def write_json(path: Path, obj: Any) -> None:
    path.write_text(json.dumps(obj, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def write_jsonl(path: Path, rows: Iterable[dict[str, Any]]) -> None:
    with path.open("w", encoding="utf-8") as f:
        for row in rows:
            f.write(json.dumps(row, ensure_ascii=False, sort_keys=True) + "\n")


def segment_class(off: int, length: int = 1) -> str:
    end = off + length
    if TEXT_MEM_OFF <= off and end <= TEXT_MEM_OFF + TEXT_SIZE:
        return "CODE"
    if RODATA_MEM_OFF <= off and end <= RODATA_MEM_OFF + RODATA_SIZE:
        return "STATIC_RODATA"
    if DATA_MEM_OFF <= off and end <= DATA_MEM_OFF + DATA_SIZE:
        return "STATIC_DATA_OR_RELA_SLOT"
    return "OUTSIDE_FILE_SEGMENTS"


def parse_rela(flat: bytes) -> list[dict[str, int]]:
    if RELA_SIZE % RELA_ENT:
        raise RuntimeError("canonical RELA size is not entry-aligned")
    end = RELA_START + RELA_SIZE
    if end > len(flat):
        raise RuntimeError("canonical RELA range exceeds mapped image")
    rows = []
    for off in range(RELA_START, end, RELA_ENT):
        r_offset, r_info, r_addend = struct.unpack_from("<QQq", flat, off)
        rows.append({
            "entry_offset": off,
            "r_offset": r_offset,
            "r_info": r_info,
            "type": r_info & 0xFFFFFFFF,
            "symbol": r_info >> 32,
            "addend": r_addend,
        })
    return rows


def build_localization_inventory(rela_rows: list[dict[str, int]]) -> dict[str, Any]:
    relative_by_target: dict[int, list[dict[str, int]]] = defaultdict(list)
    for row in rela_rows:
        if row["type"] == R_AARCH64_RELATIVE:
            relative_by_target[row["r_offset"]].append(row)

    table_entries: dict[str, list[dict[str, Any]]] = {}
    object_domains: dict[int, set[str]] = defaultdict(set)
    missing: list[dict[str, Any]] = []
    duplicate_target_rela: list[dict[str, Any]] = []

    for domain, base in LOCALIZATION_TABLES.items():
        entries = []
        for index in range(LOCALIZATION_COUNT):
            slot = base + index * 8
            matches = relative_by_target.get(slot, [])
            if len(matches) != 1:
                missing.append({"domain": domain, "index": index, "slot": slot, "relative_rela_count": len(matches)})
                if len(matches) > 1:
                    duplicate_target_rela.append({"domain": domain, "index": index, "slot": slot})
                entries.append({"index": index, "slot": slot, "object": None})
                continue
            obj = matches[0]["addend"]
            object_domains[obj].add(domain)
            entries.append({"index": index, "slot": slot, "object": obj})
        table_entries[domain] = entries

    domain_class_by_object: dict[int, str] = {}
    combination_hist = Counter()
    for obj, domains in object_domains.items():
        key = "+".join(sorted(domains))
        combination_hist[key] += 1
        if len(domains) == 1:
            domain_class_by_object[obj] = f"{next(iter(domains))}_ONLY"
        else:
            domain_class_by_object[obj] = "SHARED_LANGUAGE"

    return {
        "table_entries": table_entries,
        "object_domains": {f"0x{k:X}": sorted(v) for k, v in sorted(object_domains.items())},
        "domain_class_by_object": {f"0x{k:X}": v for k, v in sorted(domain_class_by_object.items())},
        "domain_combination_histogram": dict(sorted(combination_hist.items())),
        "missing_or_nonrelative_slots": missing,
        "duplicate_target_relative_rela": duplicate_target_rela,
    }


def language_domain_at(offset: int, loc: dict[str, Any]) -> str:
    key = f"0x{offset:X}"
    return loc["domain_class_by_object"].get(key, "UNKNOWN")


def known_structural_class(off: int) -> tuple[str, str]:
    delta = off - PLACE_TABLE_BASE_JP
    if 0 <= delta < PLACE_TABLE_COUNT * PLACE_TABLE_STRIDE:
        index, within = divmod(delta, PLACE_TABLE_STRIDE)
        if within == PLACE_NAME_OFF:
            return "PLACE_TABLE_NAME", f"place:{index}:name"
        if within == PLACE_YOMI_OFF:
            return "PLACE_TABLE_YOMI", f"place:{index}:yomi"
    return "UNKNOWN", ""


def parse_descriptors(blob: bytes) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    containers: list[dict[str, Any]] = []
    subpatches: list[dict[str, Any]] = []
    cursor = 0
    for index in range(11):
        if cursor + 16 > len(blob):
            raise RuntimeError("truncated descriptor header")
        start = cursor
        anchor, sig_len, patch_count, name_len = struct.unpack_from("<4I", blob, cursor)
        cursor += 16
        name = blob[cursor:cursor + name_len].decode("ascii")
        cursor += name_len
        sig = blob[cursor:cursor + sig_len]
        cursor += sig_len
        mask = blob[cursor:cursor + sig_len]
        cursor += sig_len
        container_id = f"DESC:{index:02d}:{name}"
        row = {
            "source_family": "descriptor_container",
            "source_id": container_id,
            "resource_offset": start,
            "name": name,
            "anchor_rva": anchor,
            "signature_len": sig_len,
            "patch_count": patch_count,
            "signature_sha256": sha256_bytes(sig),
            "mask_sha256": sha256_bytes(mask),
        }
        containers.append(row)
        for subindex in range(patch_count):
            if cursor + 20 > len(blob):
                raise RuntimeError("truncated descriptor subpatch")
            sub_start = cursor
            delta, pre_len, kind, arg, payload_len = struct.unpack_from("<IIB3xII", blob, cursor)
            cursor += 20
            pre = blob[cursor:cursor + pre_len]
            cursor += pre_len
            payload = blob[cursor:cursor + payload_len]
            cursor += payload_len
            subpatches.append({
                "source_family": "descriptor_subpatch",
                "source_id": f"SUBPATCH:{index:02d}:{subindex:02d}:{name}",
                "container_id": container_id,
                "resource_offset": sub_start,
                "name": name,
                "index": subindex,
                "offset": delta,
                "successful_write_rva": anchor + delta,
                "preimage_len": pre_len,
                "preimage": pre.hex(),
                "kind": kind,
                "arg": arg,
                "payload_len": payload_len,
                "payload": payload.hex(),
            })
    if cursor != len(blob):
        raise RuntimeError(f"descriptor parse did not consume blob: 0x{cursor:X}/0x{len(blob):X}")
    return containers, subpatches


def source_base(source_family: str, source_id: str) -> dict[str, Any]:
    return {
        "source_family": source_family,
        "source_id": source_id,
        "semantic_family_id": "",
        "language_domain": "UNKNOWN",
        "storage_mutability": "UNKNOWN",
        "window_object_cardinality": "UNKNOWN",
        "terminal_disposition": "UNRESOLVED",
        "switch_action_ids": [],
        "evidence_ids": [],
        "evidence_scope": "",
        "falsification_condition": "",
        "runtime_validation_required": False,
        "notes": [],
    }


def build_source_ledger(t5k: Any, payload_names: list[str], flat: bytes, loc: dict[str, Any]) -> tuple[list[dict[str, Any]], list[dict[str, Any]], dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    exceptions: list[dict[str, Any]] = []

    groups: dict[bytes, list[tuple[int, Any]]] = defaultdict(list)
    for i, rec in enumerate(t5k.inline_records):
        groups[rec.original].append((i, rec))
    patterns = list(groups)
    occurrences = find_pattern_occurrences(flat, patterns, cap=64)
    locs_by_pattern = dict(zip(patterns, occurrences))
    replacement_sets = {p: {rec.replacement for _, rec in recs} for p, recs in groups.items()}

    candidate_hist = Counter()
    inline_domain_hist = Counter()
    inline_segment_hist = Counter()
    inline_struct_hist = Counter()

    for index, rec in enumerate(t5k.inline_records):
        sid = f"INLINE:{index:05d}"
        row = source_base("inline", sid)
        locs = locs_by_pattern[rec.original]
        candidate_hist["64+" if len(locs) >= 64 else str(len(locs))] += 1
        candidate_rows = []
        for off in locs:
            seg = segment_class(off, rec.length)
            domain = language_domain_at(off, loc)
            structural_class, structural_id = known_structural_class(off)
            candidate_rows.append({
                "offset": off,
                "offset_hex": f"0x{off:X}",
                "segment": seg,
                "language_domain": domain,
                "structural_class": structural_class,
                "structural_id": structural_id,
            })
            inline_domain_hist[domain] += 1
            inline_segment_hist[seg] += 1
            inline_struct_hist[structural_class] += 1

        exact_localization_starts = [c for c in candidate_rows if c["language_domain"] != "UNKNOWN"]
        structural = [c for c in candidate_rows if c["structural_class"] != "UNKNOWN"]
        replacement_agreement = len(replacement_sets[rec.original]) == 1

        if exact_localization_starts:
            row["semantic_family_id"] = "LOCALIZATION_CANDIDATE"
        elif structural:
            row["semantic_family_id"] = structural[0]["structural_class"]
        elif b"%" in rec.original:
            row["semantic_family_id"] = "FORMATTER_CANDIDATE"
        else:
            row["semantic_family_id"] = "UNCLASSIFIED_INLINE"

        domains = {c["language_domain"] for c in candidate_rows if c["language_domain"] != "UNKNOWN"}
        if len(domains) == 1:
            row["language_domain"] = next(iter(domains))
        elif len(domains) > 1:
            row["language_domain"] = "MULTI_CANDIDATE_DOMAIN"

        segs = {c["segment"] for c in candidate_rows}
        if len(segs) == 1:
            row["storage_mutability"] = next(iter(segs))
        elif len(segs) > 1:
            row["storage_mutability"] = "MULTI_CANDIDATE_STORAGE"

        # Stage-1 does not promote candidate cardinality to object cardinality.
        row.update({
            "pc_location_or_index": rec.pc_rva,
            "pc_location_hex": f"0x{rec.pc_rva:X}",
            "length": rec.length,
            "original": rec.original.hex(),
            "replacement": rec.replacement.hex(),
            "original_sha256": sha256_bytes(rec.original),
            "replacement_sha256": sha256_bytes(rec.replacement),
            "pc_same_original_record_count": len(groups[rec.original]),
            "pc_same_original_replacement_agreement": replacement_agreement,
            "switch_raw_candidate_count_capped_64": len(locs),
            "switch_raw_candidates": candidate_rows,
        })
        if not locs:
            exceptions.append({"source_id": sid, "reason": "E_OBJECT_UNKNOWN", "detail": "no raw Switch candidate; structural/semantic recovery required"})
        elif not replacement_agreement:
            exceptions.append({"source_id": sid, "reason": "E_REPLACEMENT_CONFLICT", "detail": "same PC original has multiple Korean replacements"})
        elif len(locs) > 1:
            exceptions.append({"source_id": sid, "reason": "E_MULTI_CANDIDATE", "detail": "raw occurrence multiplicity requires structural classification"})
        rows.append(row)

    for index, rec in enumerate(t5k.pointer_records):
        row = source_base("pointer", f"POINTER:{index:03d}")
        row.update({
            "pc_location_or_index": rec.pc_slot_rva,
            "pc_location_hex": f"0x{rec.pc_slot_rva:X}",
            "pc_original_target_rva": rec.pc_original_target_rva,
            "mode": rec.mode,
            "arg": rec.string_offset,
            "semantic_family_id": "POINTER_MODE_0" if rec.mode == 0 else "POINTER_MODE_1" if rec.mode == 1 else "POINTER_INVALID_MODE",
        })
        if rec.mode not in (0, 1):
            exceptions.append({"source_id": row["source_id"], "reason": "E_POINTER_OWNER_UNKNOWN", "detail": f"unexpected pointer mode {rec.mode}"})
        rows.append(row)

    for index, (a, b) in enumerate(t5k.mapping_entries):
        row = source_base("mapping", f"MAPPING:{index:05d}")
        row.update({
            "pc_location_or_index": index,
            "semantic_family_id": "MAPPING_ORIGINAL" if index < 7494 else "MAPPING_KOREAN_ADDITION",
            "mapping_left": a,
            "mapping_right": b,
        })
        rows.append(row)

    containers, subpatches = parse_descriptors(t5k.runtime_descriptor_blob)
    for item in containers:
        row = source_base("descriptor_container", item["source_id"])
        row.update(item)
        row["semantic_family_id"] = item["name"]
        rows.append(row)
    for item in subpatches:
        row = source_base("descriptor_subpatch", item["source_id"])
        row.update(item)
        row["semantic_family_id"] = item["name"]
        rows.append(row)

    helper_entries = [
        ("HELPER:PAGE_MAPPER", "runtime_page_mapper", 0x00),
        ("HELPER:BYTE_VALIDATION_COPY", "runtime_byte_validation_copy", 0x20),
    ]
    for sid, family, entry in helper_entries:
        row = source_base("helper_semantic_entry", sid)
        row.update({"pc_location_or_index": entry, "semantic_family_id": family})
        rows.append(row)

    data_files = sorted(n for n in payload_names if n.startswith("data/") and not n.endswith("/"))
    for index, name in enumerate(data_files):
        rel = name[5:]
        row = source_base("romfs", f"ROMFS:{index:03d}:{rel}")
        row.update({
            "pc_location_or_index": rel,
            "semantic_family_id": "CWTDAT_SWITCH_NATIVE_RECONSTRUCTION" if rel == "CMENU/CWTDAT_JP.TR5" else "ROMFS_FILE",
        })
        rows.append(row)

    metrics = {
        "inline_raw_candidate_histogram": dict(sorted(candidate_hist.items(), key=lambda kv: (kv[0] == "64+", int(kv[0]) if kv[0].isdigit() else 999))),
        "inline_candidate_language_domain_histogram": dict(sorted(inline_domain_hist.items())),
        "inline_candidate_segment_histogram": dict(sorted(inline_segment_hist.items())),
        "inline_candidate_structural_histogram": dict(sorted(inline_struct_hist.items())),
        "romfs_data_file_count": len(data_files),
        "descriptor_container_count": len(containers),
        "descriptor_subpatch_count": len(subpatches),
    }
    return rows, exceptions, metrics


def build_switch_inventory(build_id: bytes, flat: bytes, rela_rows: list[dict[str, int]], loc: dict[str, Any]) -> dict[str, Any]:
    rela_type_hist = Counter(row["type"] for row in rela_rows)
    table_summary = {}
    for domain, entries in loc["table_entries"].items():
        present = sum(1 for e in entries if e["object"] is not None)
        unique_objects = len({e["object"] for e in entries if e["object"] is not None})
        table_summary[domain] = {"entry_count": len(entries), "relative_rela_present": present, "unique_source_objects": unique_objects}
    return {
        "build_id_hex": build_id.hex().upper(),
        "mapped_flat_size": len(flat),
        "segments": {
            "text": {"start": TEXT_MEM_OFF, "size": TEXT_SIZE},
            "rodata": {"start": RODATA_MEM_OFF, "size": RODATA_SIZE},
            "data": {"start": DATA_MEM_OFF, "size": DATA_SIZE},
        },
        "rela": {
            "start": RELA_START,
            "size": RELA_SIZE,
            "entry_size": RELA_ENT,
            "entry_count": len(rela_rows),
            "type_histogram": {str(k): v for k, v in sorted(rela_type_hist.items())},
            "relative_count": rela_type_hist[R_AARCH64_RELATIVE],
        },
        "localization": {
            "entries_per_table": LOCALIZATION_COUNT,
            "source_tables": LOCALIZATION_TABLES,
            "destination_base": LOCALIZATION_DEST_BASE,
            "table_summary": table_summary,
            "language_object_combinations": loc["domain_combination_histogram"],
            "missing_or_nonrelative_slot_count": len(loc["missing_or_nonrelative_slots"]),
        },
        "place_table": {
            "jp_base": PLACE_TABLE_BASE_JP,
            "record_count": PLACE_TABLE_COUNT,
            "stride": PLACE_TABLE_STRIDE,
            "name_field": {"offset": PLACE_NAME_OFF, "size": PLACE_NAME_SIZE},
            "yomi_field": {"offset": PLACE_YOMI_OFF, "size": PLACE_YOMI_SIZE},
        },
    }


def source_counts(rows: list[dict[str, Any]]) -> dict[str, int]:
    return dict(sorted(Counter(r["source_family"] for r in rows).items()))


def make_invariants(identity: dict[str, Any], source_summary: dict[str, Any], switch_inventory: dict[str, Any]) -> list[dict[str, Any]]:
    rows = []
    def inv(i: int, scope: str, status: str, evidence: Any, note: str) -> None:
        rows.append({
            "invariant_id": f"INV-{i}",
            "scope": scope,
            "status": status,
            "evidence_or_output": evidence,
            "falsification_condition": "Recorded condition or canonical identity no longer holds.",
            "notes": note,
        })

    inv(1, "final code-space / glyph closure", "NOT_RUN", {}, "Requires final replacement/action set and final font/mapping runtime model.")
    inv(2, "language-domain isolation", "NOT_RUN", {"language_inventory_built": True}, "Domain ownership inventory is built; mutation isolation requires an action set.")
    inv(3, "storage ownership / relocation integrity", "NOT_RUN", {"rela_inventory_built": True}, "RELA inventory is built; action ownership validation requires resolved actions.")
    inv(4, "source/action cardinality integrity", "NOT_RUN", {}, "Stage-1 raw occurrence counts are not object cardinality proof.")
    inv(5, "overlap and application-order consistency", "NOT_RUN", {}, "No mutation action set exists in read-only Stage-1.")
    inv(6, "mapping consumer algorithm consistency", "UNKNOWN", {}, "Mapping lookup algorithms and full consumer family are not yet closed.")
    inv(7, "code-site authorization and containment", "NOT_RUN", {}, "No code mutation plan exists in read-only Stage-1.")

    id_ok = all(identity[k]["match"] for k in ("switch_main", "pc_patcher_zip", "dinput8", "t5k_rcdata")) and identity["switch_build_id"]["match"]
    inv(8, "guard / target-identity closure", "PASS" if id_ok else "FAIL", identity, "Canonical input identity gate is executable in Stage-1.")
    inv(9, "final semantic decode / round-trip consistency", "NOT_RUN", {}, "Requires final encoded replacements and mapping/runtime decisions.")
    inv(10, "deterministic build and emitted-patch reproducibility", "NOT_RUN", {}, "No build is authorized in this stage; report hashes are recorded separately.")
    inv(11, "evidence closure for no-edit dispositions", "NOT_RUN", {"terminal_no_edit_rows": 0}, "Stage-1 intentionally creates no terminal no-edit dispositions.")
    return rows


def main() -> None:
    ap = argparse.ArgumentParser(description="Read-only full PC->Switch accounting inventory validator")
    ap.add_argument("--main", required=True, type=Path, help="Canonical Switch v1.1.3 compressed ExeFS/main")
    ap.add_argument("--pc-patcher", required=True, type=Path, help="Canonical Taiko5DX_Korean_Patcher_v1.02.zip")
    ap.add_argument("--out-dir", required=True, type=Path, help="Report output directory only")
    args = ap.parse_args()

    main_hash = sha256_file(args.main)
    patcher_hash = sha256_file(args.pc_patcher)
    build_id, flat = decompress_nso(args.main)
    payload = open_payload(args.pc_patcher)
    payload_names = payload.namelist()
    dll = payload.read("dinput8.dll")
    t5k_blob = extract_t5k_rcdata(dll)
    t5k = parse_t5k_resource(t5k_blob)

    identity = {
        "switch_main": {"actual": main_hash, "expected": CANONICAL_MAIN_SHA256, "match": main_hash == CANONICAL_MAIN_SHA256},
        "switch_build_id": {"actual": build_id.hex().upper(), "expected": BUILD_ID_FULL.hex().upper(), "name": BUILD_ID_NAME, "match": build_id == BUILD_ID_FULL},
        "pc_patcher_zip": {"actual": patcher_hash, "expected": CANONICAL_PATCHER_SHA256, "match": patcher_hash == CANONICAL_PATCHER_SHA256},
        "dinput8": {"actual": sha256_bytes(dll), "expected": CANONICAL_DINPUT_SHA256, "match": sha256_bytes(dll) == CANONICAL_DINPUT_SHA256},
        "t5k_rcdata": {"actual": sha256_bytes(t5k_blob), "expected": CANONICAL_T5K_SHA256, "match": sha256_bytes(t5k_blob) == CANONICAL_T5K_SHA256},
    }
    if not all(v["match"] for v in identity.values()):
        raise SystemExit("canonical input identity check failed; no accounting report emitted")

    rela_rows = parse_rela(flat)
    loc = build_localization_inventory(rela_rows)
    switch_inventory = build_switch_inventory(build_id, flat, rela_rows, loc)
    source_rows, exceptions, discovery_metrics = build_source_ledger(t5k, payload_names, flat, loc)
    counts = source_counts(source_rows)

    expected_counts = {
        "inline": 17103,
        "pointer": 56,
        "mapping": 10036,
        "descriptor_container": 11,
        "descriptor_subpatch": 14,
        "helper_semantic_entry": 2,
        "romfs": CANONICAL_ROMFS_ITEMS,
    }
    denominator_checks = {k: {"actual": counts.get(k, 0), "expected": v, "match": counts.get(k, 0) == v} for k, v in expected_counts.items()}
    if not all(v["match"] for v in denominator_checks.values()):
        raise SystemExit("source denominator check failed; no accounting report emitted")

    source_summary = {
        "counts": counts,
        "denominator_checks": denominator_checks,
        "terminal_dispositions": dict(sorted(Counter(r["terminal_disposition"] for r in source_rows).items())),
        "discovery_metrics": discovery_metrics,
        "exception_count": len(exceptions),
        "policy": "Stage-1 is discovery/accounting only; raw uniqueness never becomes terminal DIRECT_PORT without independent structural evidence.",
    }

    invariants = make_invariants(identity, source_summary, switch_inventory)
    invariant_summary = dict(sorted(Counter(r["status"] for r in invariants).items()))

    out = args.out_dir
    out.mkdir(parents=True, exist_ok=True)
    write_jsonl(out / "source_ledger.jsonl", source_rows)
    write_json(out / "switch_inventory.json", switch_inventory)
    write_jsonl(out / "exceptions.jsonl", exceptions)
    write_json(out / "invariants.json", invariants)
    write_json(out / "localization_language_inventory.json", loc)

    # No terminal action proposals are created in Stage-1. This empty ledger is
    # intentional and prevents discovery evidence from masquerading as approval.
    write_jsonl(out / "switch_action_proposals.jsonl", [])
    write_json(out / "evidence_fanout.json", {"status": "NOT_APPLICABLE_STAGE1", "reason": "no terminal no-edit dispositions or approved actions"})

    summary = {
        "status": "ok_read_only_inventory",
        "input_identity": identity,
        "source_summary": source_summary,
        "switch_inventory_summary": {
            "mapped_flat_size": switch_inventory["mapped_flat_size"],
            "rela_entry_count": switch_inventory["rela"]["entry_count"],
            "rela_relative_count": switch_inventory["rela"]["relative_count"],
            "localization_table_summary": switch_inventory["localization"]["table_summary"],
            "localization_language_object_combinations": switch_inventory["localization"]["language_object_combinations"],
            "localization_missing_or_nonrelative_slot_count": switch_inventory["localization"]["missing_or_nonrelative_slot_count"],
        },
        "invariant_status_summary": invariant_summary,
        "mutated_input_files": 0,
        "ips_emitted": 0,
        "game_files_emitted": 0,
    }
    write_json(out / "SUMMARY.json", summary)

    output_hashes = {}
    for p in sorted(out.iterdir()):
        if p.is_file() and p.name != "OUTPUT_HASHES.json":
            output_hashes[p.name] = sha256_file(p)
    write_json(out / "OUTPUT_HASHES.json", output_hashes)

    print(json.dumps(summary, ensure_ascii=False, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
