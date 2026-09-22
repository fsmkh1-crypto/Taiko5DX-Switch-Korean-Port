"""Pinned V371 plan adapter. Compiles references; never reclassifies admission.

No pickle/exec/import of supplied audit or draft code. The operation plan's
protected-source snapshots remain evidence, not executable input to this tool.
"""
from __future__ import annotations

from collections import Counter
from dataclasses import dataclass
import json
from pathlib import Path
from typing import Any
import zipfile

from .selective_event_contracts import (
    ConsumerContract, ContractError, FieldContract, FieldState, OwnerContract,
    Proof, ProtectedRange, Route, Span, require, sha256,
)

CANONICAL_HEAD = 'fedf8f2dc7161f4aae145fa59fecfe47d0658389'
PLAN_SHA256 = '8ceb6fa9d0c0e8a0bf096f84fb95f42b4e9aabd235cba0940ab2b45290cfcdba'
OWNERS = 'OWNER_OPERATIONS_66987.jsonl'
FIELDS = 'FIELD_OPERATIONS_24305.jsonl'
EV = 'inherited/EVENT_PAYLOAD_ADJUDICATIONS_19.jsonl'
XB = 'inherited/EXTERNAL_BOUNDARY_ADJUDICATIONS_7.jsonl'
EP = 'inherited/inherited/ENDPOINT_PARENT_PATH_PROOFS_12.jsonl'
HOLDS = 'EXPLICIT_HOLDS.jsonl'
UNITS = 'UNIT_BINDINGS_80.jsonl'
MEMBERS = (OWNERS, FIELDS, EV, XB, EP, HOLDS, UNITS)


@dataclass
class ContractCatalog:
    owners: dict[str, OwnerContract]
    fields: dict[str, FieldContract]
    consumers: dict[str, ConsumerContract]
    input_receipts: list[dict[str, Any]]
    plan_sha256: str
    source_rows: dict[str, list[dict[str, Any]]]

    def summary(self) -> dict[str, Any]:
        return {
            'scope': 'IM01_TYPED_CATALOG_COMPILED_NOT_PRODUCT_ACCEPTANCE',
            'canonical_head': CANONICAL_HEAD,
            'plan_sha256': self.plan_sha256,
            'owner_count': len(self.owners), 'field_count': len(self.fields),
            'consumer_contract_count': len(self.consumers),
            'owner_routes': dict(sorted(Counter(o.route.value for o in self.owners.values()).items())),
            'field_states': dict(sorted(Counter(f.state.value for f in self.fields.values()).items())),
            'upstream_recipe_operations': sum(o.needs_upstream_recipe for o in self.owners.values()),
            'upstream_delegates_retained': sum(o.route == Route.DELEGATE for o in self.owners.values()),
            'selected_unknown_label_routes': dict(sorted(Counter(
                o.route.value for o in self.owners.values()
                if o.needs_upstream_recipe and 'UNRESOLVED_ROLE' in o.role_labels).items())),
            'local_holds': {k: [o.owner for o in self.owners.values() if k in o.holds] for k in ('H01',)},
            'H02_fields': [f.field for f in self.fields.values() if f.state == FieldState.DISPOSITION],
            'PC_PATCH_ORACLE_GATE': 'PASS_INHERITED_SAME_AUTHORED_DATA_AND_BINDING_FAMILY',
            'PC_interpreter_equivalence': 'UNKNOWN_NOT_ASSUMED',
            'final_effects_computed': False,
            'product_accepted': False,
            'product_outputs_emitted': 0,
            'semantic_admission_recomputed': False,
            'canonical_membership_changed': False,
        }


def _unique(rows: list[dict[str, Any]], key: str) -> dict[str, dict[str, Any]]:
    require(all(isinstance(r, dict) and isinstance(r.get(key), str) for r in rows), 'ROW_KEY_SCHEMA', key)
    out = {r[key]: r for r in rows}
    require(len(out) == len(rows), 'DUPLICATE_INPUT_KEY', key)
    return out


def load_catalog(path: Path) -> ContractCatalog:
    """Verify only consumed input members; reuse closed interpretations verbatim."""
    digest = sha256(path.read_bytes())
    require(digest == PLAN_SHA256, 'PLAN_ARCHIVE_IDENTITY_MISMATCH', digest)
    receipts = []
    rows: dict[str, list[dict[str, Any]]] = {}
    with zipfile.ZipFile(path) as z:
        names = z.namelist()
        require(len(names) == len(set(names)), 'DUPLICATE_ZIP_MEMBER', path.name)
        index = json.loads(z.read('INDEX.json'))
        require(index['canonical_head'] == CANONICAL_HEAD, 'PLAN_HEAD_MISMATCH', index['canonical_head'])
        require(index['schema'] == 'V371_NONCANONICAL_OPERATION_OBLIGATION_PLAN_INDEX_V1',
                'UNKNOWN_PLAN_SCHEMA', index['schema'])
        for member in MEMBERS:
            info = index['files'][member]
            raw = z.read(member)
            require(len(raw) == info['bytes'] and sha256(raw) == info['sha256'], 'PLAN_MEMBER_IDENTITY', member)
            require(raw.endswith(b'\n'), 'PLAN_MEMBER_FINAL_LF', member)
            decoded = [json.loads(line) for line in raw.splitlines()]
            require(len(decoded) == info['rows'], 'PLAN_MEMBER_ROW_COUNT', member)
            rows[member] = decoded
            receipts.append({'member': member, 'bytes': len(raw), 'sha256': sha256(raw),
                             'rows': len(decoded), 'purpose': 'INPUT_CONSUMPTION_NOT_TECHNICAL_REVALIDATION'})
    metadata = {r['member']: r for r in receipts}
    def proof(member: str, line: int, claim: str) -> Proof:
        return Proof('v371_operation_obligation_plan_20260922.zip::' + member,
                     metadata[member]['sha256'], claim, line)

    owner_rows = _unique(rows[OWNERS], 'owner')
    field_rows = _unique(rows[FIELDS], 'field')
    unit_rows = _unique(rows[UNITS], 'id')
    require(len(owner_rows) == 66987 and len(field_rows) == 24305 and len(unit_rows) == 80,
            'INPUT_POPULATION_MISMATCH', (len(owner_rows), len(field_rows), len(unit_rows)))
    hold_owners = {r['id']: tuple(r.get('owners', ())) for r in rows[HOLDS]}
    owners = {}
    for line, r in enumerate(rows[OWNERS], 1):
        kind = r['recipe']['kind']
        require(kind in ('FROZEN_DIRECT_BINDING_BOUNDARY_CONTRACT_TO_CONSUME',
                         'FROZEN_V369_EXACT_INTERVAL_REFERENCE', 'FROZEN_EXACT_COMPOSITE'),
                'UNKNOWN_RECIPE_REFERENCE_KIND', kind)
        binding = r['binding']
        require(binding['member'] in ('DIRECT_HEADER_PRESERVED.jsonl', 'OVERLAP_COMPOSITE_31.jsonl')
                and type(binding['line']) is int and binding['line'] > 0,
                'INVALID_CANONICAL_BINDING_REFERENCE', r['owner'])
        owners[r['owner']] = OwnerContract(
            r['owner'], r['file'], r['partition'], Span(*r['observed_physical_view']),
            bytes.fromhex(r['source_header_hex']), Route(r['draft_route']),
            proof(OWNERS, line, f"FROZEN_BINDING_REFERENCE:{binding['member']}:{binding['line']}; NOT_NEW_ADMISSION"),
            kind, (r['recipe_id'] if r['draft_route'] != Route.PRESERVE.value else None), r['unit'], tuple(r['inherited_role_labels']),
            tuple(k for k, keys in hold_owners.items() if r['owner'] in keys))
    require(all(o.unit is None or o.unit in unit_rows for o in owners.values()), 'OWNER_UNKNOWN_UNIT', '')

    consumers = {}
    fields_proofs: dict[str, Proof] = {}
    field_protections: dict[str, tuple[ProtectedRange, ...]] = {}
    field_views: dict[str, tuple[str, ...]] = {}
    def add_consumer(c: ConsumerContract) -> None:
        require(c.id not in consumers and c.owner in owners, 'CONSUMER_KEY_OR_OWNER', c.id)
        consumers[c.id] = c

    for line, r in enumerate(rows[EV], 1):
        p = proof(EV, line, 'INHERITED_PATH_BOUNDED_EVENT_PAYLOAD_PRESERVATION')
        span = Span(*r['source_view'])
        raw = bytes.fromhex(r['pc_window'])
        require(len(raw) == span.size and raw[:4] == owners[r['owner']].source_header,
                'EV_WINDOW_OR_HEADER_IDENTITY', r['id'])
        if r.get('new_raw_source_window_hex') is not None:
            require(bytes.fromhex(r['new_raw_source_window_hex']) == raw, 'EV_SOURCE_PC_WINDOW_MISMATCH', r['id'])
        payload = Span(*r['payload_preserve_range'])
        require(payload == Span(span.start+4, span.end), 'EV_PAYLOAD_RANGE', r['id'])
        protections = (
            ProtectedRange(r['id']+':HEADER', Span(span.start, span.start+4), raw[:4], p),
            ProtectedRange(r['id']+':PAYLOAD', payload, raw[4:], p),
        )
        add_consumer(ConsumerContract(r['id'], r['owner'], 'CONDITIONAL_EVENT_PAYLOAD',
                                     r['consumer_entry_condition'], protections, p))
        fields_proofs[r['field']] = p
        field_protections[r['field']] = protections
        field_views[r['field']] = (r['id'],)

    for line, r in enumerate(rows[XB], 1):
        p = proof(XB, line, 'INHERITED_PATH_BOUNDED_EXTERNAL_BOUNDARY_CONTRACT')
        raw = bytes.fromhex(r['input_window_receipt']['hex'])
        base = r['input_window_receipt']['source_range'][0]
        require(sha256(raw) == r['input_window_receipt']['sha256'], 'XB_WINDOW_HASH', r['id'])
        scalar = Span(*r['owner_effective_consumed_range'])
        data = raw[scalar.start-base:scalar.end-base]
        require(scalar.size == 4 and data == owners[r['owner']].source_header, 'XB_SCALAR_WINDOW', r['id'])
        scalar_protection = ProtectedRange(r['id']+':VALUE', scalar, data, p)
        view_id = r['id']+':VALUE'
        add_consumer(ConsumerContract(view_id, r['owner'], 'CONDITIONAL_VALUE_OPERAND',
                                     r['parent_entry_condition'], (scalar_protection,), p))
        ranges = (scalar_protection,)
        views = (view_id,)
        if r['id'] == 'XB01':
            # Keep both EVENT16 header words. Do not reinterpret the upper halfword.
            second = Span(*r['record16_second_word_range'])
            first = Span(second.start-4, second.start)
            ranges = ranges + (
                ProtectedRange('XB01:EVENT16_HEADER', first, bytes.fromhex(r['record16_header_hex']), p),
                ProtectedRange('XB01:SECONDARY_WORD', second, bytes.fromhex(r['protected_field_hex']), p))
            add_consumer(ConsumerContract('XB01:EVENT16', r['owner'], 'CONDITIONAL_EVENT16_HEADER',
                                         r['parent_entry_condition'], ranges[1:], p))
            views += ('XB01:EVENT16',)
        fields_proofs[r['field']] = p
        field_protections[r['field']] = ranges
        field_views[r['field']] = views

    for line, r in enumerate(rows[EP], 1):
        p = proof(EP, line, 'INHERITED_ENDPOINT_PARENT_PATH_ONLY_NO_GLOBAL_EXEMPTION')
        raw = bytes.fromhex(r['source_parent_hex'])
        require(sha256(raw) == r['parent_source_window_sha256'], 'ENDPOINT_WINDOW_HASH', r['owner'])
        start = r['source_owner']
        delta = start-r['source_parent_start']
        value = raw[delta:delta+4]
        require(value == owners[r['owner']].source_header, 'ENDPOINT_SCALAR_IDENTITY', r['owner'])
        # The existing proof retains the nested guard. Never flatten it to another operator.
        condition = r['entry_condition'] + ' | ' + r.get('interpretation', '')
        if 'NESTED' in r['proof_id']:
            condition += ' | NESTED_CHILD_READ_GUARD_MUST_ADMIT; NO_CONSUMPTION_CLAIM_ON_SKIPPED_PATH'
        vid = 'EP:' + r['owner']
        add_consumer(ConsumerContract(vid, r['owner'], 'CONDITIONAL_VALUE_OPERAND', condition,
                     (ProtectedRange(vid+':VALUE', Span(start, start+4), value, p),), p))

    fields = {}
    for line, r in enumerate(rows[FIELDS], 1):
        key = r['field']
        require(r['candidate_retained'] is True and r['emitted'] is False, 'FIELD_PLAN_STATE', key)
        state = FieldState(r['plan_state'])
        if state in (FieldState.PAYLOAD, FieldState.BRANCH04, FieldState.DISPOSITION):
            require(key in fields_proofs, 'MISSING_INHERITED_FIELD_CONTRACT', key)
        dependencies = tuple(dict.fromkeys(tuple(r['anchors']) + tuple('CONTACT:'+o for o in r['contact_owner_ids']) + ('ROLE_POLICY:'+key,)))
        fields[key] = FieldContract(key, Span(*r['physical_write_envelope']),
             bytes.fromhex(r['source_header_hex']), r['source_target'], r['partition'], r['unit'], state,
             fields_proofs[key] if key in fields_proofs else proof(FIELDS, line, 'CANDIDATE_REFERENCE_NOT_REWRITE_PERMISSION'),
             dependencies, field_protections.get(key, ()), field_views.get(key, ()),
             tuple(sorted({'R:'+d['containing_replacement'] for d in r['interior_recipe_dependencies']})))
        for cid in r['contact_owner_ids']:
            require(cid.removeprefix('O:') in owners, 'UNKNOWN_CONTACT_OWNER', cid)
    require(all(f.unit is None or f.unit in unit_rows for f in fields.values()), 'FIELD_UNKNOWN_UNIT', '')
    require(set(fields_proofs) <= set(fields), 'ORPHAN_FIELD_PROOF', '')
    return ContractCatalog(owners, fields, consumers, receipts, digest, rows)
