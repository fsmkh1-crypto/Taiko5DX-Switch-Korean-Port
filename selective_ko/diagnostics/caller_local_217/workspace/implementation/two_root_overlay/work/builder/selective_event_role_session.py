"""One IM01 caller interface for the four formerly conflated NUL-view phases.

This is an isolated front end, NOT a replacement final serializer. Existing
protected prototype callers are unchanged and must not be treated as migrated.
"""
from __future__ import annotations
from dataclasses import dataclass, field
from typing import Iterable
from .selective_event_contract_catalog import ContractCatalog
from .selective_event_contracts import (
    ContractError, FieldProposal, MappedWindow, Observation, PreparedRecipe,
    RecipeContract, ReviewedInteriorRecipe, Result, Status, Window, blocked, check_field_proposal,
    emit_product, observe_nul_view, prepare_recipe, require_all_view_results,
    validate_consumer_view, validate_prepared_payload,
)


@dataclass
class RoleContractSession:
    catalog: ContractCatalog
    recipes: dict[str, RecipeContract]
    attempts: list[Result] = field(default_factory=list)
    prepared: dict[str, PreparedRecipe] = field(default_factory=dict)

    def _owner(self, owner: str):
        if owner not in self.catalog.owners:
            self.attempts.append(blocked('LOOKUP:'+owner, 'UNKNOWN_RETAINED_OWNER'))
            raise ContractError('UNKNOWN_RETAINED_OWNER', owner)
        return self.catalog.owners[owner]

    def _record(self, result: Result) -> Result:
        self.attempts.append(result)
        return result

    def observe_source(self, owner: str, file_bytes: bytes | None, partition_end: int) -> Observation:
        o = self._owner(owner)
        observation = observe_nul_view(file_bytes, o.observed_span.start, partition_end,
                                       operation='OBSERVE:'+owner)
        self._record(observation.result)
        # The measurement is deliberately NOT inserted into recipes.
        return observation

    def prepare_owner(self, owner: str, source: Window | None, pc: Window | None = None,
                      interior: ReviewedInteriorRecipe | None = None) -> PreparedRecipe:
        o = self._owner(owner)
        prepared = prepare_recipe(o, self.recipes.get(owner), source, pc, interior)
        self._record(prepared.result)
        self.prepared[owner] = prepared
        return prepared

    def check_pretransform_payload(self, owner: str, payload: bytes) -> Result:
        o = self._owner(owner)
        prepared = self.prepared.get(owner)
        if prepared is None:
            return self._record(blocked('PAYLOAD:'+owner, 'RECIPE_NOT_PREPARED'))
        return self._record(validate_prepared_payload(o, prepared, payload))

    def check_established_views(self, owner: str,
                                samples: dict[str, Iterable[MappedWindow]]) -> Result:
        self._owner(owner)
        contracts = {c.id: c for c in self.catalog.consumers.values() if c.owner == owner}
        if set(samples) != set(contracts):
            return self._record(blocked('JOINT_VIEWS:'+owner, 'MISSING_OR_EXTRA_ESTABLISHED_VIEW'))
        individual = [self._record(validate_consumer_view(c, samples[key])) for key,c in contracts.items()]
        return self._record(require_all_view_results(contracts, individual))

    def check_field(self, proposal: FieldProposal) -> Result:
        contract = self.catalog.fields.get(proposal.field)
        if contract is None:
            return self._record(blocked('FIELD:'+proposal.field, 'UNKNOWN_RETAINED_FIELD'))
        return self._record(check_field_proposal(contract, proposal))

    def emit(self, **kwargs) -> None:
        self._record(blocked('EMIT', 'PRODUCT_EMISSION_DISABLED_IM01'))
        emit_product(**kwargs)
