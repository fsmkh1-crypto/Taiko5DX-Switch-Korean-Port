"""IM02: consume the frozen obligation plan; never infer a transformation.

The plan archive is NONCANONICAL but byte-pinned. Its projections are checked
against the canonical V369 applicability bytes. Relation/support/unit rows are
consumed from that pinned projection, not re-derived or promoted to new authority.
The compiler checks transport, keys and joins, not the closed technical findings.
"""
from __future__ import annotations
from collections import Counter
from dataclasses import dataclass
import json
from pathlib import Path
from types import MappingProxyType
from typing import Any, Mapping
import zipfile
from .selective_event_contracts import Proof, Span, require, sha256
from .selective_event_contract_catalog import CANONICAL_HEAD, PLAN_SHA256
from .selective_event_recipe_catalog import V369_SHA256, APP_SHA256

PLAN_MEMBERS = (
    'APPLICABILITY_PLAN_2438.jsonl', 'OCCURRENCE_PLAN_2671.jsonl',
    'RELATION_PLAN_130.jsonl', 'SUPPORT_PLAN_5.jsonl',
    'ROOT_REFERENCE_PLAN_19.jsonl', 'ROOT_VALUE_REQUIREMENTS_5.jsonl',
    'UNIT_BINDINGS_80.jsonl', 'OWNER_OPERATIONS_66987.jsonl',
)


def freeze(x: Any) -> Any:
    if isinstance(x, dict):
        return MappingProxyType({k: freeze(v) for k, v in x.items()})
    if isinstance(x, list):
        return tuple(freeze(v) for v in x)
    return x


def thaw(x: Any) -> Any:
    if isinstance(x, Mapping):
        return {k: thaw(v) for k, v in x.items()}
    if isinstance(x, (tuple, list)):
        return [thaw(v) for v in x]
    return x


def canonical_json(x: Any) -> bytes:
    return json.dumps(thaw(x), sort_keys=True, ensure_ascii=False,
                      separators=(',', ':'), allow_nan=False).encode('utf-8')


def unique(rows: list[dict], key: str) -> dict[str, dict]:
    require(all(isinstance(r, dict) and isinstance(r.get(key), str) for r in rows),
            'OBLIGATION_KEY_SCHEMA', key)
    d = {r[key]: r for r in rows}
    require(len(d) == len(rows), 'DUPLICATE_OBLIGATION_KEY', key)
    return d


@dataclass(frozen=True)
class ObligationCatalog:
    apps: Mapping[str, Any]
    occurrences: Mapping[str, Any]
    relations: Mapping[str, Any]
    supports: Mapping[str, Any]
    root_refs: Mapping[str, Any]
    roots: Mapping[str, Any]
    units: Mapping[str, Any]
    owners: Mapping[str, Any]
    delegate_occurrences: Mapping[str, str]
    input_receipts: tuple[Any, ...]
    fingerprint: str
    plan_sha256: str = PLAN_SHA256

    @property
    def groups(self) -> Mapping[str, Mapping[str, Any]]:
        return MappingProxyType({'APP': self.apps, 'OCC': self.occurrences,
            'REL': self.relations, 'SUP': self.supports, 'ROOTREF': self.root_refs, 'ROOT': self.roots})

    @property
    def ids(self) -> frozenset[str]:
        return frozenset(k for group in self.groups.values() for k in group)

    def summary(self) -> dict:
        return {'scope': 'IM02_INPUT_CONSUMPTION_NOT_PRODUCT_ACCEPTANCE',
                'canonical_head': CANONICAL_HEAD, 'plan_sha256': self.plan_sha256,
                'catalog_fingerprint': self.fingerprint,
                'counts': {k: len(v) for k, v in self.groups.items()},
                'obligation_total': len(self.ids), 'retained_units': len(self.units),
                'retained_owners': len(self.owners),
                'exact_delegated_occurrences': len(self.delegate_occurrences),
                'support_forms': dict(Counter(r['canonical_support']['role'] for r in self.supports.values())),
                'PC_PATCH_ORACLE_GATE': 'PASS_INHERITED_SAME_AUTHORED_DATA_BINDING_FAMILY',
                'product_accepted': False, 'product_outputs': 0}


def load_obligations(plan: Path, applicability: Path) -> ObligationCatalog:
    """Byte identity and exact joins only. No archive-supplied code is executed."""
    require(sha256(plan.read_bytes()) == PLAN_SHA256, 'IM02_PLAN_ARCHIVE_IDENTITY', plan.name)
    require(sha256(applicability.read_bytes()) == V369_SHA256, 'IM02_APP_ARCHIVE_IDENTITY', applicability.name)
    rows: dict[str, list[dict]] = {}
    receipts = []
    with zipfile.ZipFile(plan) as z:
        require(len(z.namelist()) == len(set(z.namelist())), 'DUPLICATE_ZIP_MEMBER', plan.name)
        idx = json.loads(z.read('INDEX.json'))
        require(idx['canonical_head'] == CANONICAL_HEAD, 'IM02_CANONICAL_HEAD', '')
        for name in PLAN_MEMBERS:
            raw = z.read(name); m = idx['files'][name]
            require(len(raw) == m['bytes'] and sha256(raw) == m['sha256'], 'IM02_PLAN_MEMBER_IDENTITY', name)
            require(raw.endswith(b'\n'), 'IM02_TERMINAL_LF', name)
            rr = [json.loads(l) for l in raw.splitlines()]
            require(len(rr) == m['rows'], 'IM02_PLAN_MEMBER_COUNT', name)
            rows[name] = rr
            receipts.append({'member': name, **m, 'purpose': 'CONSUME_PINNED_INPUT'})
    with zipfile.ZipFile(applicability) as z:
        require(len(z.namelist()) == len(set(z.namelist())), 'DUPLICATE_ZIP_MEMBER', applicability.name)
        raw = z.read('APPLICABILITY.jsonl')
        require(sha256(raw) == APP_SHA256 and len(raw) == 4498481, 'IM02_CANONICAL_APP_IDENTITY', '')
        actual_apps = [json.loads(l) for l in raw.splitlines()]
    require(len(actual_apps) == 2438, 'IM02_CANONICAL_APP_COUNT', '')
    receipts.append({'member': 'V369::APPLICABILITY.jsonl', 'bytes': len(raw),
                     'sha256': APP_SHA256, 'rows': len(actual_apps), 'purpose': 'CONSUME_CANONICAL_ROWS'})
    apps = unique(rows[PLAN_MEMBERS[0]], 'id')
    occs = unique(rows[PLAN_MEMBERS[1]], 'id')
    rels = unique(rows[PLAN_MEMBERS[2]], 'id')
    sups = unique(rows[PLAN_MEMBERS[3]], 'id')
    refs = unique(rows[PLAN_MEMBERS[4]], 'id')
    roots = unique(rows[PLAN_MEMBERS[5]], 'id')
    units = unique(rows[PLAN_MEMBERS[6]], 'id')
    owners = unique(rows[PLAN_MEMBERS[7]], 'owner')
    require(tuple(map(len, (apps, occs, rels, sups, refs, roots, units, owners))) ==
            (2438, 2671, 130, 5, 19, 5, 80, 66987), 'IM02_INPUT_POPULATIONS', '')
    require(set(units) == {f'T{i:02}' for i in range(1, 81)}, 'IM02_UNIT_MEMBERSHIP', '')
    cluster_units = {}
    for uid, u in units.items():
        for c in u['cluster_ids']:
            require(c not in cluster_units, 'IM02_DUPLICATE_CLUSTER_RESPONSIBILITY', c)
            cluster_units[c] = uid
        for o in u['owner_ids']:
            require(o in owners and owners[o]['unit'] == uid, 'IM02_UNIT_OWNER_JOIN', o)
    require(len(cluster_units) == 87, 'IM02_CLUSTER_COUNT', '')
    app_by_owner = {}
    seen_occ = set()
    for line, actual in enumerate(actual_apps, 1):
        aid = f'APP:{line}'; a = apps[aid]; key = f"{actual['file']}:{actual['source_owner_offset']:X}"
        require(a['owner'] == key and a['source_line'] == line and a['source_ledger_sha256'] == APP_SHA256,
                'IM02_APP_SOURCE_JOIN', aid)
        require(key in owners and key not in app_by_owner, 'IM02_APP_OWNER_JOIN', key)
        app_by_owner[key] = aid
        binding = actual['binding_provenance']
        require(owners[key]['binding'] == {'member': binding['member'], 'line': binding['line_1based']},
                'IM02_APP_BINDING_JOIN', aid)
        require(actual['final_disposition'] == a['canonical_disposition'] == 'INCLUDE_KO',
                'IM02_ADMISSION_NOT_INFERRED', aid)
        require(a['unit'] == owners[key]['unit'], 'IM02_APP_UNIT_JOIN', aid)
        require(a['occurrence_ids'] == [f'OCC:{line}:{i}' for i in range(len(actual['exact_occurrences']))],
                'IM02_APP_OCCURRENCE_MEMBERSHIP', aid)
        a['canonical_row'] = actual
        for i, o in enumerate(actual['exact_occurrences']):
            oid = f'OCC:{line}:{i}'; p = occs[oid]
            require(p['app_id'] == aid and p['owner'] == key and p['exact_occurrence'] == o and
                    p['source'] == {'member': 'APPLICABILITY.jsonl', 'line': line, 'occurrence_index': i},
                    'IM02_EXACT_OCCURRENCE_JOIN', oid)
            literal = bytes.fromhex(o['literal_hex']); escape = o['escape'].encode('ascii')
            require(len(literal) == o['literal_end']-o['literal_start'] and sha256(literal) == o['literal_sha256'],
                    'IM02_LITERAL_REFERENCE_IDENTITY', oid)
            require(o['escape_end'] == o['literal_start'] and len(escape) == o['escape_end']-o['escape_start'],
                    'IM02_OCCURRENCE_REFERENCE_GEOMETRY', oid)
            require(actual['pc_ko_runtime_span'][0]+4 <= o['escape_start'] < o['literal_end'] <= actual['pc_ko_runtime_span'][1],
                    'IM02_OCCURRENCE_OUTSIDE_BOUND_PC_OWNER', oid)
            seen_occ.add(oid)
        require(a['required_root_refs'] == actual['required_tai5msg_roots'],
                'IM02_APP_ROOT_JOIN', aid)
    require(seen_occ == set(occs), 'IM02_ORPHAN_OCCURRENCE', '')
    # Delegation preserves absolute PC coordinates AND literal identity, not equal text.
    # Source-origin annotations are owner-relative: APP1714:0 and APP1715:0
    # intentionally differ there. Both unmodified provenance rows are retained.
    delegates = {}
    for aid, a in apps.items():
        cr = a['canonical_row']; d = cr.get('nested_occurrence_delegation')
        expected = [] if d is None else [f"{cr['file']}:{d['inner_source_owner']:X}"]
        require(a['direct_delegation_children'] == expected, 'IM02_DELEGATION_OWNER_JOIN', aid)
        if d is None:
            continue
        require(d['identical_absolute_occurrences'] and d['outer_exclusive_occurrences'] == 0 and
                d['inner_disposition'] == 'INCLUDE_KO', 'IM02_DELEGATION_AUTHORITY', aid)
        child = apps[app_by_owner[expected[0]]]
        for oid in a['occurrence_ids']:
            matches = [cid for cid in child['occurrence_ids'] if
                       all(occs[cid]['exact_occurrence'].get(k) == occs[oid]['exact_occurrence'].get(k) for k in ('escape_start','escape_end','escape','literal_start','literal_end','literal_hex','literal_sha256','surface_hex','required_root'))]
            require(len(matches) == 1, 'IM02_DELEGATION_EXACT_OCCURRENCE', oid)
            delegates[oid] = matches[0]
    for rid, r in rels.items():
        e = r['canonical_edge']; uid = r['unit']
        require(rid == 'REL:'+e['edge_id'] and cluster_units[e['cluster_id']] == uid,
                'IM02_RELATION_UNIT_JOIN', rid)
        require(all(owners[o]['unit'] == uid and o in units[uid]['owner_ids'] for o in (e['inner_owner'], e['outer_owner'])),
                'IM02_RELATION_OWNER_JOIN', rid)
    for sid, s in sups.items():
        c = s['canonical_support']; o = c['node_id']
        require(o in owners and c['semantic_disposition'] == 'NON_KOREAN_TARGET' and
                owners[o]['draft_route'] == 'PRESERVATION_CANDIDATE', 'IM02_SUPPORT_NOT_ADMISSION', sid)
        require(cluster_units[c['cluster_id']] == s['unit'], 'IM02_SUPPORT_UNIT_JOIN', sid)
        require(c['role'] in ('NON_KOREAN_EXTERNAL_HEADER_OVERLAP', 'NON_KOREAN_INSIDE_UNION'),
                'IM02_SUPPORT_SCHEMA', sid)
        require(('overlapped_node' in c) == (c['role'] == 'NON_KOREAN_EXTERNAL_HEADER_OVERLAP'),
                'IM02_SUPPORT_TWO_FORMS', sid)
    for refid, r in refs.items():
        root = roots['ROOT:'+r['root']]
        require(r['proof'] == root['proof'] and r['owner'] == apps[r['app_id']]['owner'] and
                any(o.get('required_root') == r['proof'] for o in apps[r['app_id']]['canonical_row']['exact_occurrences']),
                'IM02_ROOT_REFERENCE_JOIN', refid)
        require(refid == f"ROOTREF:{apps[r['app_id']]['source_line']}:{r['root']}", 'IM02_ROOT_REFERENCE_KEY', refid)
    for aid, a in apps.items():
        require(set(a['required_root_refs']) == {r['root'] for r in refs.values() if r['app_id'] == aid},
                'IM02_EXACT_ROOT_REFERENCE_SET', aid)
    tables = (apps, occs, rels, sups, refs, roots, units, owners)
    fp = sha256(canonical_json({'plan': PLAN_SHA256, 'inputs': receipts, 'delegates': delegates}))
    return ObligationCatalog(*(freeze(t) for t in tables), freeze(delegates),
                              tuple(freeze(r) for r in receipts), fp)
