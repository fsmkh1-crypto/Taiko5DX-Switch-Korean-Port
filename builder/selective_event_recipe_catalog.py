"""Consume existing V366 composites / V369 precise intervals as recipe inputs.

No grouping, new translation, NUL-derived boundary, or family-label selector.
Other direct bindings stay references until their required extent authority is
provided. This is input recipe preparation, NOT the IM02 obligation checker.
"""
from __future__ import annotations

import json
from pathlib import Path
import zipfile
from .selective_event_contracts import (
    Proof, RecipeContract, RecipeKind, RegionAuthority, Span, require, sha256,
)
from .selective_event_contract_catalog import ContractCatalog, OWNERS

V366_SHA256 = '430ab6394ade066c5314ac734819d68cd9f24554da2a5346bc23031019712b1c'
V369_SHA256 = '4e8b5dc2899789541e010ec16adcf1921b05673913e6840c3b2e8eb0cfa07189'
APP_SHA256 = 'b9c421d18e7ce0a5d7603d7d3e764ad102bf791d965d7216edac85682a838c43'


def _member(archive: Path, expected: str, member: str) -> bytes:
    require(sha256(archive.read_bytes()) == expected, 'RECIPE_ARCHIVE_IDENTITY', archive.name)
    with zipfile.ZipFile(archive) as z:
        require(len(z.namelist()) == len(set(z.namelist())), 'RECIPE_DUPLICATE_ZIP_MEMBER', archive.name)
        return z.read(member)


def load_existing_recipes(catalog: ContractCatalog, v366: Path, v369: Path) -> tuple[dict[str, RecipeContract], dict]:
    apps_raw = _member(v369, V369_SHA256, 'APPLICABILITY.jsonl')
    require(sha256(apps_raw) == APP_SHA256, 'EXACT_APPLICABILITY_LEDGER_IDENTITY', '')
    comp_raw = _member(v366, V366_SHA256, 'OVERLAP_COMPOSITE_31.jsonl')
    comp_sha = sha256(comp_raw)
    owner_rows = {r['owner']: r for r in catalog.source_rows[OWNERS]}
    out: dict[str, RecipeContract] = {}
    for line, raw in enumerate(apps_raw.splitlines(), 1):
        r = json.loads(raw)
        key = f"{r['file']}:{r['source_owner_offset']:X}"
        require(key in catalog.owners and key not in out, 'RECIPE_OWNER_KEY', key)
        o = catalog.owners[key]
        reference = owner_rows[key]['recipe']
        require(o.needs_upstream_recipe and reference['kind'] == 'FROZEN_V369_EXACT_INTERVAL_REFERENCE',
                'RECIPE_REFERENCE_ROUTE_MISMATCH', key)
        binding = owner_rows[key]['binding']
        require(binding['member'] == r['binding_provenance']['member']
                and binding['line'] == r['binding_provenance']['line_1based'], 'RECIPE_BINDING_ROW_MISMATCH', key)
        require(reference['source_span'] == r['source_runtime_span']
                and reference['pc_span'] == r['pc_ko_runtime_span']
                and reference['source_sha256'] == r['source_runtime_bytes_sha256']
                and reference['pc_span_sha256'] == r['pc_ko_runtime_bytes_sha256'],
                'RECIPE_PLAN_INTERVAL_REFERENCE_MISMATCH', key)
        p = Proof('V369_V368_EXACT_APPLICABILITY_2438.zip::APPLICABILITY.jsonl', APP_SHA256,
                  'EXISTING_PRECISE_AUTHORED_INTERVAL_NOT_NEW_ROLE_CLASSIFICATION', line)
        header = bytes.fromhex(r['runtime_control_provenance']['header_hex'])
        require(header == o.source_header, 'RECIPE_CANONICAL_HEADER_MISMATCH', key)
        out[key] = RecipeContract(key, o.recipe_id, RecipeKind.DIRECT,
            'stock:'+r['file'], RegionAuthority(Span(*r['source_runtime_span']), r['source_runtime_bytes_sha256'], p),
            p, header, 'pc:'+r['file'], RegionAuthority(Span(*r['pc_ko_runtime_span']), r['pc_ko_runtime_bytes_sha256'], p),
            header, transform_obligations=(owner_rows[key]['applicability_obligation'],))
    app_count = len(out)
    for line, raw in enumerate(comp_raw.splitlines(), 1):
        r = json.loads(raw)
        key = f"{r['file']}:{r['source_offset']:X}"
        require(key in catalog.owners and key not in out, 'RECIPE_OWNER_KEY', key)
        o = catalog.owners[key]
        reference = owner_rows[key]['recipe']
        require(o.needs_upstream_recipe and reference['kind'] == 'FROZEN_EXACT_COMPOSITE',
                'RECIPE_REFERENCE_ROUTE_MISMATCH', key)
        require(owner_rows[key]['binding'] == {'member': 'OVERLAP_COMPOSITE_31.jsonl', 'line': line},
                'COMPOSITE_BINDING_LINE', key)
        p = Proof('V366_EVENT_169_EXACT_LEDGER_RECONSTRUCTION_LARGE_ARTIFACTS.zip::OVERLAP_COMPOSITE_31.jsonl',
                  comp_sha, 'EXISTING_CANONICAL_COMPOSITE_BEFORE_APPROVED_TRANSFORMS', line)
        literal = bytes.fromhex(r['final_selective_owner_hex'])
        require(len(literal) == r['final_selective_owner_len']
                and sha256(literal) == r['final_selective_owner_sha256'] == reference['sha256'],
                'COMPOSITE_LITERAL_IDENTITY', key)
        header = bytes.fromhex(r['source_header_hex'])
        require(header == o.source_header and literal[:4] == header, 'COMPOSITE_HEADER', key)
        source = RegionAuthority(Span(r['source_offset'], r['source_offset']+r['source_owner_len']),
                                 r['source_owner_sha256'], p)
        out[key] = RecipeContract(key, o.recipe_id, RecipeKind.COMPOSITE, 'stock:'+r['file'], source,
             p, header, canonical_literal=literal, canonical_literal_sha256=r['final_selective_owner_sha256'],
             transform_obligations=('IM02_APPROVED_OWNER_TRANSFORMS:'+key,))
    require(app_count == 2438 and len(out)-app_count == 31, 'EXISTING_RECIPE_CONSUMPTION_COUNT', len(out))
    return out, {'precise_interval_references_consumed': app_count, 'composite_recipes_consumed': len(out)-app_count,
                 'other_direct_references_not_defaulted_to_nul': sum(o.needs_upstream_recipe and o.owner not in out
                                                                   for o in catalog.owners.values()),
                 'new_boundary_proofs_created': 0, 'product_accepted': False,
                 'scope': 'PINNED_RECIPE_INPUT_ADAPTER; NOT_CANONICAL_OBLIGATION_DISCHARGE'}
