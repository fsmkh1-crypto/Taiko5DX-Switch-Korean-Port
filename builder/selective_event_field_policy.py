"""V371 role-aware structural-field policy adapter.

This module consumes the reviewed 24,305-row field-policy ledger.  It does not
re-discover fields from final bytes, infer runtime roles from opcodes, or admit a
fallback rule.  Source ownership and stage-count semantics remain those frozen
by the retained IM01 catalog and the PC editor v0.30 source-plan oracle.

The ledger closes field writer admission only.  Loading it does not emit EVENT
files or assert VAL01/runtime acceptance.
"""
from __future__ import annotations

from collections import Counter
from dataclasses import dataclass
from enum import Enum
import json
from pathlib import Path
from types import MappingProxyType
from typing import Mapping

from .selective_event_contracts import (
    ContractError, DispositionApproval, FieldContract, FieldState, Proof, Result,
    Status, require, sha256,
)
from .selective_event_contract_catalog import ContractCatalog
from .selective_event_relocation_adapter import ReviewedFieldRule

POLICY_SCHEMA = 'V371_ROLE_AWARE_FIELD_POLICY_STATIC_CLOSURE_V1'
POLICY_ROWS = 24_305
POLICY_BYTES = 18_399_148
POLICY_SHA256 = '4cdf5df2c6b7264641374d459ef1dc7484749ea6adfb99b5646a6c40cfddfeff'
POLICY_DOCUMENT = 'V371_ROLE_AWARE_FIELD_POLICY_24305.jsonl'


class FieldPolicyCategory(str, Enum):
    GENERIC_IDENTITY = 'GENERIC_PC_EDITOR_IDENTITY_COALESCE'
    GENERIC_REENCODE = 'GENERIC_PC_EDITOR_SOURCE_PLAN_REENCODE'
    PAYLOAD_PRESERVE = 'PAYLOAD_PRESERVE_NO_FIELD_WRITER'
    SECONDARY_HEADER_PRESERVE = 'SECONDARY_HEADER_PRESERVE_NO_FIELD_WRITER'
    EXPRESSION_OPERAND_PRESERVE = 'EXPRESSION_OPERAND_PRESERVE_NO_FIELD_WRITER'
    SWITCH_SPECIAL = 'SWITCH_SPECIAL_SPAN_REENCODE'
    TYPED_EVENT04 = 'TYPED_EVENT04_REENCODE'
    DUAL_VIEW_SLOT = 'DUAL_VIEW_SUBORDINATE_FIELD_SLOT'


NO_FIELD_WRITER = frozenset({
    FieldPolicyCategory.PAYLOAD_PRESERVE,
    FieldPolicyCategory.SECONDARY_HEADER_PRESERVE,
    FieldPolicyCategory.EXPRESSION_OPERAND_PRESERVE,
})
WRITER_POLICIES = frozenset(set(FieldPolicyCategory) - set(NO_FIELD_WRITER))
EXPECTED_COUNTS = {
    FieldPolicyCategory.GENERIC_IDENTITY: 12_522,
    FieldPolicyCategory.GENERIC_REENCODE: 11_745,
    FieldPolicyCategory.PAYLOAD_PRESERVE: 19,
    FieldPolicyCategory.SECONDARY_HEADER_PRESERVE: 1,
    FieldPolicyCategory.EXPRESSION_OPERAND_PRESERVE: 1,
    FieldPolicyCategory.SWITCH_SPECIAL: 3,
    FieldPolicyCategory.TYPED_EVENT04: 6,
    FieldPolicyCategory.DUAL_VIEW_SLOT: 8,
}


def _field_key(row_id: str) -> str:
    require(isinstance(row_id, str) and row_id.startswith('F:'),
            'FIELD_POLICY_ROW_ID', row_id)
    return row_id[2:]


def _generic_intrusion(opcode: int, source_header: bytes) -> int:
    if opcode in (0x06, 0x07):
        return (int.from_bytes(source_header[1:4], 'little') * 2) % 4
    if opcode == 0x09:
        return int.from_bytes(source_header[2:4], 'little') % 4
    return 0


def _codec(category: FieldPolicyCategory, opcode: int, mechanism: str) -> str | None:
    if category in NO_FIELD_WRITER:
        return None
    if category == FieldPolicyCategory.TYPED_EVENT04:
        require(opcode == 0x04, 'TYPED_EVENT04_POLICY_OPCODE', opcode)
        return 'EVENT04_BITS19'
    if category == FieldPolicyCategory.SWITCH_SPECIAL:
        if mechanism == 'EVENT_04':
            require(opcode == 0x04, 'SPECIAL04_POLICY_OPCODE', opcode)
            return 'SPECIAL04'
        require(mechanism == 'BRANCH_09' and opcode == 0x09,
                'SWITCH09_POLICY_MECHANISM', (mechanism, opcode))
        return 'SWITCH09_BITS19'
    require(opcode in (0x02, 0x04, 0x06, 0x07, 0x08, 0x09),
            'GENERIC_POLICY_UNSUPPORTED_OPCODE', opcode)
    return f'PC_EDITOR{opcode:02}'


@dataclass(frozen=True)
class FieldPolicyEntry:
    field: str
    file: str
    field_start: int
    source_header: bytes
    opcode: int
    source_span: int
    partition: int
    unit: str | None
    category: FieldPolicyCategory
    mechanism: str
    geometry_changed: bool
    final_field_oracle: int
    final_target_oracle: int
    final_span_oracle: int
    output_header_oracle: bytes
    final_writer: str
    writer_order: str
    authority_label: str
    contact_dispositions: tuple[str, ...]
    proof: Proof

    def __post_init__(self) -> None:
        require(self.field == f'{self.file}:{self.field_start:X}',
                'FIELD_POLICY_KEY_MISMATCH', self.field)
        require(type(self.source_header) is bytes and len(self.source_header) == 4
                and self.source_header[0] == self.opcode,
                'FIELD_POLICY_SOURCE_HEADER', self.field)
        require(type(self.source_span) is int and self.source_span >= 4
                and self.source_span % 4 == 0,
                'FIELD_POLICY_SOURCE_SPAN', self.field)
        require(type(self.final_span_oracle) is int and self.final_span_oracle >= 4
                and self.final_span_oracle % 4 == 0
                and self.final_target_oracle - self.final_field_oracle == self.final_span_oracle,
                'FIELD_POLICY_FINAL_ORACLE', self.field)
        require(type(self.output_header_oracle) is bytes and len(self.output_header_oracle) == 4,
                'FIELD_POLICY_OUTPUT_HEADER', self.field)
        require(self.category in FieldPolicyCategory and bool(self.mechanism)
                and bool(self.final_writer) and bool(self.writer_order)
                and bool(self.authority_label) and isinstance(self.proof, Proof),
                'FIELD_POLICY_REQUIRED_METADATA', self.field)

    @property
    def has_field_writer(self) -> bool:
        return self.category in WRITER_POLICIES

    @property
    def codec(self) -> str | None:
        return _codec(self.category, self.opcode, self.mechanism)

    @property
    def intrusion(self) -> int:
        return 0 if self.codec in ('EVENT04_BITS19', 'SWITCH09_BITS19', 'SPECIAL04') else _generic_intrusion(self.opcode, self.source_header)

    def reviewed_rule(self, contract: FieldContract) -> ReviewedFieldRule:
        require(self.has_field_writer and self.codec is not None,
                'NO_FIELD_WRITER_POLICY_CANNOT_CREATE_RULE', self.field)
        require(contract.field == self.field and contract.source_header == self.source_header
                and contract.source_span.start == self.field_start
                and contract.source_target - contract.source_span.start == self.source_span
                and contract.partition == self.partition and contract.unit == self.unit,
                'FIELD_POLICY_CONTRACT_SCOPE', self.field)
        return ReviewedFieldRule(
            self.field, self.codec, sha256(self.source_header), contract.source_target,
            self.partition, self.unit, self.intrusion, self.proof,
        )

    def validate_oracles(self, contract: FieldContract) -> None:
        require(contract.field == self.field and contract.source_header == self.source_header
                and contract.source_span.start == self.field_start
                and contract.source_target - contract.source_span.start == self.source_span
                and contract.partition == self.partition and contract.unit == self.unit,
                'FIELD_POLICY_CATALOG_JOIN', self.field)
        if self.has_field_writer:
            rule = self.reviewed_rule(contract)
            require(rule.encode(self.source_header, self.source_span) == self.source_header,
                    'FIELD_POLICY_SOURCE_DECODE', self.field)
            require(rule.encode(self.source_header, self.final_span_oracle) == self.output_header_oracle,
                    'FIELD_POLICY_OUTPUT_ORACLE', self.field)
        else:
            require(self.output_header_oracle == self.source_header,
                    'NO_WRITER_POLICY_OUTPUT_MUST_PRESERVE_SOURCE', self.field)

    def check_no_writer(self, contract: FieldContract, layout, final_bytes: bytes,
                        approval: DispositionApproval | None = None) -> Result:
        require(not self.has_field_writer and contract.field == self.field,
                'FIELD_POLICY_NO_WRITER_SCOPE', self.field)
        if self.category == FieldPolicyCategory.SECONDARY_HEADER_PRESERVE:
            require(contract.state == FieldState.DISPOSITION and approval is not None
                    and approval.field == contract.field and approval.unit == contract.unit
                    and approval.disposition == 'PRESERVE_SECONDARY_HEADER'
                    and approval.expected_word_sha256 == sha256(contract.source_header),
                    'H02_EXPLICIT_CANONICAL_PLAN_DISPOSITION_REQUIRED', self.field)
        elif self.category == FieldPolicyCategory.PAYLOAD_PRESERVE:
            require(contract.state == FieldState.PAYLOAD,
                    'PAYLOAD_PRESERVE_POLICY_STATE', self.field)
        elif self.category == FieldPolicyCategory.EXPRESSION_OPERAND_PRESERVE:
            require(contract.state in (FieldState.CONTEXT, FieldState.UNKNOWN),
                    'EXPRESSION_PRESERVE_POLICY_STATE', self.field)
        try:
            final_span = layout.project(contract.source_span)
        except ContractError as ex:
            raise ContractError('NO_WRITER_POLICY_REQUIRES_EXACT_PARENT_MAP',
                                f'{self.field}; {ex.code}') from ex
        require(final_span.size == 4 and final_span.start % 4 == 0,
                'NO_WRITER_FINAL_STORAGE_ENVELOPE', self.field)
        require(final_bytes[final_span.start:final_span.end] == contract.source_header,
                'NO_WRITER_POLICY_BYTES_CHANGED', self.field)
        # Existing protected consumer-view validation still runs separately.
        return Result(
            'FIELD:' + self.field, Status.PRESERVED,
            evidence=(contract.proof, self.proof, layout.mapping_proof),
            details={
                'policy_category': self.category.value,
                'writer': self.final_writer,
                'final_span': [final_span.start, final_span.end],
                'no_structural_field_writer': True,
                'partition_table_still_final_writer': True,
                'product_accepted': False,
            },
        )


@dataclass(frozen=True)
class FieldPolicyCatalog:
    entries: Mapping[str, FieldPolicyEntry]
    ledger_sha256: str
    ledger_bytes: int
    source: str

    def __post_init__(self) -> None:
        object.__setattr__(self, 'entries', MappingProxyType(dict(self.entries)))
        require(len(self.entries) == len(set(self.entries)),
                'DUPLICATE_FIELD_POLICY_ENTRY', self.source)

    def entry(self, field: str) -> FieldPolicyEntry:
        require(field in self.entries, 'MISSING_ROLE_AWARE_FIELD_POLICY', field)
        return self.entries[field]

    def validate_catalog(self, catalog: ContractCatalog) -> None:
        require(set(self.entries) == set(catalog.fields),
                'ROLE_AWARE_FIELD_POLICY_COVERAGE', {
                    'missing': sorted(set(catalog.fields) - set(self.entries))[:10],
                    'extra': sorted(set(self.entries) - set(catalog.fields))[:10],
                })
        for key, entry in self.entries.items():
            contract = catalog.fields[key]
            entry.validate_oracles(contract)
            allowed = {
                FieldPolicyCategory.GENERIC_IDENTITY: (FieldState.CONTEXT, FieldState.UNKNOWN),
                FieldPolicyCategory.GENERIC_REENCODE: (FieldState.CONTEXT, FieldState.UNKNOWN),
                FieldPolicyCategory.PAYLOAD_PRESERVE: (FieldState.PAYLOAD,),
                FieldPolicyCategory.SECONDARY_HEADER_PRESERVE: (FieldState.DISPOSITION,),
                FieldPolicyCategory.EXPRESSION_OPERAND_PRESERVE: (FieldState.CONTEXT, FieldState.UNKNOWN),
                FieldPolicyCategory.SWITCH_SPECIAL: (FieldState.SPECIAL,),
                FieldPolicyCategory.TYPED_EVENT04: (FieldState.BRANCH04,),
                FieldPolicyCategory.DUAL_VIEW_SLOT: (FieldState.CONTEXT, FieldState.UNKNOWN),
            }[entry.category]
            require(contract.state in allowed,
                    'FIELD_POLICY_STATE_CATEGORY_MISMATCH', (key, contract.state.value, entry.category.value))
            if contract.interior_recipe_ids:
                require(entry.category == FieldPolicyCategory.DUAL_VIEW_SLOT,
                        'INTERIOR_FIELD_MUST_BE_DUAL_VIEW_POLICY', key)
        counts = Counter(e.category for e in self.entries.values())
        if len(self.entries) == POLICY_ROWS:
            require(dict(counts) == EXPECTED_COUNTS,
                    'FIELD_POLICY_CATEGORY_COUNTS', dict(counts))

    def summary(self) -> dict:
        counts = Counter(e.category.value for e in self.entries.values())
        return {
            'schema': 'V371_ROLE_AWARE_FIELD_POLICY_ADAPTER_V1',
            'source': self.source,
            'ledger_bytes': self.ledger_bytes,
            'ledger_sha256': self.ledger_sha256,
            'rows': len(self.entries),
            'policy_counts': dict(sorted(counts.items())),
            'field_writer_rows': sum(e.has_field_writer for e in self.entries.values()),
            'no_field_writer_rows': sum(not e.has_field_writer for e in self.entries.values()),
            'product_accepted': False,
        }


def load_field_policy(path: Path, catalog: ContractCatalog) -> FieldPolicyCatalog:
    raw = path.read_bytes()
    require(len(raw) == POLICY_BYTES and sha256(raw) == POLICY_SHA256,
            'FIELD_POLICY_LEDGER_IDENTITY', {'bytes': len(raw), 'sha256': sha256(raw)})
    require(raw.endswith(b'\n'), 'FIELD_POLICY_LEDGER_FINAL_LF', path.name)
    rows = raw.splitlines()
    require(len(rows) == POLICY_ROWS, 'FIELD_POLICY_LEDGER_ROW_COUNT', len(rows))
    entries: dict[str, FieldPolicyEntry] = {}
    for line_number, raw_line in enumerate(rows, 1):
        row = json.loads(raw_line)
        key = _field_key(row['id'])
        require(key not in entries and row['hold'] is False
                and row['runtime_hook_required'] is False,
                'FIELD_POLICY_ROW_STATUS', key)
        category = FieldPolicyCategory(row['policy_category'])
        proof = Proof(POLICY_DOCUMENT, POLICY_SHA256,
                      f"{row['authority']}; POLICY={category.value}; WRITER={row['final_writer']}",
                      line_number)
        entry = FieldPolicyEntry(
            key, row['file'], row['field_start'], bytes.fromhex(row['source_header_hex']),
            row['opcode'], row['source_span'], row['partition'], row.get('unit'),
            category, row['mechanism'], row['geometry_changed'], row['final_field'],
            row['final_target'], row['final_span'], bytes.fromhex(row['output_header_hex']),
            row['final_writer'], row['writer_order'], row['authority'],
            tuple(row.get('contact_dispositions', ())), proof,
        )
        entries[key] = entry
    result = FieldPolicyCatalog(entries, POLICY_SHA256, POLICY_BYTES, str(path))
    result.validate_catalog(catalog)
    return result
