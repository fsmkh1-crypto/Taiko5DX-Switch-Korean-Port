"""Replay frozen V371 requests into memory and write diagnostic JSON only.

No EVENT binary export, Git mutation, TAI5MSG validation or product acceptance.
Missing physical requests remain explicitly NOT_OBSERVED.
"""
from __future__ import annotations
import argparse
from collections import Counter
from dataclasses import replace
import hashlib
import json
from pathlib import Path
import sys
import time
from unittest.mock import patch
import zipfile

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT / 'work'))
from builder.selective_event_contracts import require, Proof, sha256, Route
from builder.selective_event_contract_catalog import load_catalog
from builder.selective_event_recipe_catalog import load_existing_recipes
from builder.selective_event_obligation_catalog import load_obligations
from builder.selective_event_obligation_receipts import ObligationEngine
from builder.selective_event_field_policy import load_field_policy
from builder.selective_event_overlap import IntegratedSerializer
from tools.validate_event_overlap import ManifestInputs, read_requests
import builder.selective_event_final_layout as final_layout

BASE_HEAD = '736f8b56ae641e847315f8e3735ad958f9538870'

class PinnedInputStore(ManifestInputs):
    """Cache verified immutable proof identities, without weakening stock checks."""
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.identities = {}
    def proof(self, spec):
        key = spec['document']; doc = self.documents.get(key)
        require(doc is not None, 'PROOF_DOCUMENT_NOT_PROVISIONED', key)
        if key not in self.identities:
            p = self.path(doc['path'])
            if doc.get('member') is not None:
                with zipfile.ZipFile(p) as z:
                    require(len(z.namelist()) == len(set(z.namelist())), 'DUPLICATE_PROOF_ZIP_MEMBER', key)
                    info = z.getinfo(doc['member'])
                    require(info.file_size <= 128*1024*1024, 'PROOF_DOCUMENT_TOO_LARGE', key)
                    raw = z.read(info)
            else:
                raw = p.read_bytes()
            actual = sha256(raw); count = len(raw.splitlines())
            require(len(raw) == doc['bytes'] and actual == doc['sha256'], 'PROOF_DOCUMENT_IDENTITY', key)
            self.identities[key] = (actual, count)
            self.receipts.append({'kind':'PROOF_DOCUMENT','id':key,'bytes':len(raw),
                'sha256':actual,'rows':count,'claim_boundary':'IDENTITY_NOT_ARBITRARY_TRUTH'})
        actual, count = self.identities[key]
        require(spec['sha256'] == actual, 'PROOF_REFERENCE_HASH_MISMATCH', key)
        row = spec.get('row')
        require(row is None or type(row) is int and 1 <= row <= count, 'PROOF_ROW_BOUNDS', key)
        return Proof(key, actual, spec['claim'], row)


def dump(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2)+'\n', encoding='utf-8')


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--input-root', type=Path, default=ROOT/'active_inputs')
    ap.add_argument('--authority-root', type=Path, default=ROOT/'authorities')
    ap.add_argument('--output', type=Path, required=True)
    ap.add_argument('--late-failure-probes', action='store_true')
    a = ap.parse_args(); inp = a.input_root.resolve(); au = a.authority_root.resolve(); out = a.output.resolve()
    require(not out.exists(), 'FRESH_DIAGNOSTIC_DIRECTORY_REQUIRED', str(out))
    out.mkdir(parents=True)
    t = time.monotonic()
    m = json.loads((inp/'ACTIVE_REQUEST_FIXED_CONNECTED_169.json').read_text(encoding='utf-8'))
    declared = m['files']; names = [r['file'] for r in declared]
    require(len(names) == 169 and len(set(names)) == 169, 'EXACT_169_REQUEST_MEMBERSHIP', '')
    missing = sorted(r['file'] for r in declared if not (inp/r['source']['path']).is_file())
    m['files'] = [r for r in declared if r['file'] not in missing]
    plan = au/'v371_operation_obligation_plan_20260922.zip'
    v366 = au/'V366_EVENT_169_EXACT_LEDGER_RECONSTRUCTION_LARGE_ARTIFACTS.zip'
    v369 = au/'V369_V368_EXACT_APPLICABILITY_2438.zip'
    im = load_catalog(plan)
    policy = load_field_policy(au/'ROLE_AWARE_FIELD_POLICY_24305.jsonl', im)
    obligations = load_obligations(plan, v369)
    recipes, _ = load_existing_recipes(im, v366, v369)
    store = PinnedInputStore(inp, m['proof_documents'])
    requests, registry, roots = read_requests(m, store, im, recipes)
    require(not roots, 'TAI5MSG_IS_A_SEPARATE_STAGE', '')
    require((len(im.owners),len(recipes),len(policy.entries)) == (66987,52491,24305), 'FROZEN_CATALOG_COUNTS', '')
    engine = IntegratedSerializer(im, ObligationEngine(obligations, im, recipes, registry), policy)
    class Traced(type(engine)):
        def run_file(self, q):
            run = super().run_file(q)
            dump(out/(q.file+'.summary.json'), run.summary())
            with (out/(q.file+'.attempts.jsonl')).open('w',encoding='utf-8') as f:
                for r in run.attempts:
                    f.write(json.dumps({'operation':r.operation,'status':r.status.value,'reasons':list(r.reasons),'details':r.details},ensure_ascii=False)+'\n')
            if run.assembled is not None:
                dump(out/(q.file+'.writer_journal.json'),[r.to_dict() for r in run.assembled.journal])
            print(q.file, 'PASS' if run.local_complete else 'BLOCKED', flush=True)
            return run
    traced = Traced(im, engine.engine, policy)
    result = traced.run(requests, run_id='V371_ACTIVE_REQUEST_PARTIAL_FIXED1251_'+BASE_HEAD[:8])
    dump(out/'SUMMARY.json', result.summary())
    with (out/'OBLIGATION_RECEIPTS.jsonl').open('w',encoding='utf-8') as f:
        for r in result.obligations.receipts: f.write(json.dumps(r.to_dict(),ensure_ascii=False)+'\n')
    actual = {}; extents = []; units = []; journals = []
    fixed = json.loads((ROOT/'EXISTING_FIXED_PARTICLE_CONNECTION.json').read_text(encoding='utf-8'))['rows']
    fixed_map = {r['owner']:r for r in fixed}; readbacks = []
    for run in result.files:
        built = run.assembled
        actual[run.file] = {'file':run.file,'local_complete':run.local_complete,'source_sha256':sha256(run.request.source),
            'owner_identities':len(run.owner_identity_spans),'recipe_views':len(run.owner_recipe_spans),'relation_views':len(run.owner_relation_spans),
            'assembled_size':None if built is None else len(built.data),'assembled_sha256':None if built is None else sha256(built.data),
            'last_writer':None if built is None else built.journal[-1].writer}
        for key, span in run.owner_identity_spans.items():
            rr = run.owner_recipe_spans.get(key); rv = run.owner_relation_spans.get(key)
            extents.append({'owner':key,'identity':[span.start,span.end],
                'recipe':None if rr is None else [rr.start,rr.end], 'relation':None if rv is None else [rv.start,rv.end]})
        if built is None: continue
        byid = {s.id:(i,s) for i,s in enumerate(built.journal)}
        slots = []
        for i,s in enumerate(built.journal):
            if s.kind != 'FIELD_SLOT': continue
            require(len(s.supersedes) == 1, 'SLOT_EXACT_PARENT', s.id)
            pi, parent = byid[s.supersedes[0]]
            ok = pi < i < len(built.journal)-1 and parent.kind == 'PREPARED_PAYLOAD' and parent.writer == s.writer
            require(ok, 'PARENT_SLOT_FINAL_TABLE_ORDER', s.id)
            slots.append({'field':s.id,'parent':parent.id,'parent_index':pi,'slot_index':i,'table_index':len(built.journal)-1,'pass':ok})
        require(built.journal[-1].kind == 'FINAL_TABLE', 'FINAL_TABLE_LAST', run.file)
        journals.append({'file':run.file,'field_slots':slots,'last_writer':'FINAL_TABLE','layout_audit':built.audit.to_dict()})
        for uid in run.summary()['retained_units']:
            u = obligations.units[uid]; claims = [r for r in built.ownership if r.unit == uid]
            require(bool(claims), 'UNIT_FINAL_RESPONSIBILITY_NOT_OBSERVED', uid)
            delegates = [key for key in u['owner_ids'] if im.owners[key].route == Route.DELEGATE]
            independent = [e.owner for e in built.layout.edits if e.owner in delegates]
            require(not independent,'DELEGATE_HAS_INDEPENDENT_PAYLOAD_WRITE',uid)
            units.append({'unit':uid,'file':run.file,'owner_ids':list(u['owner_ids']),
                'final_responsibility_spans':len(claims),'final_responsibility_bytes':sum(c.final_span.size for c in claims),
                'independent_delegate_writes':independent,'last_writer':'FINAL_TABLE',
                'claim_boundary':'Final unit accounting and delegation; not an independent full-product scheduler acceptance.'})
        for key, span in run.owner_recipe_spans.items():
            if key not in fixed_map:continue
            expected=bytes.fromhex(fixed_map[key]['after_hex']);observed=built.data[span.start:span.end]
            readbacks.append({'owner':key,'span':[span.start,span.end],'sha256':sha256(observed),'pass':expected==observed})
    with (out/'OWNER_EXTENT_RECEIPTS.jsonl').open('w',encoding='utf-8') as f:
        for r in extents:f.write(json.dumps(r,ensure_ascii=False)+'\n')
    dump(out/'UNIT_FINAL_RESPONSIBILITY_80.json',units)
    dump(out/'JOURNAL_ORDER_AND_LAYOUT.json',journals)
    dump(out/'FIXED_PARTICLE_READBACK.json',{'expected':1251,'observed':len(readbacks),'passed':sum(r['pass'] for r in readbacks),'rows':readbacks})
    dump(out/'INPUT_CONNECTION.json',{'expected_files':169,'actual_files':len(requests),'missing_files':missing,'receipts':store.receipts})
    dump(out/'RESULTS.json',{'base_head':BASE_HEAD,'actual_files':len(requests),'passed':sum(r.local_complete for r in result.files),
        'files':list(actual.values()),'missing_files':missing,'bridge_errors':list(result.bridge_errors),
        'obligations':result.obligations.summary(),'units_observed':len(units),'candidate_files_emitted':0,
        'product_accepted':False,'legacy_overlay_completion':False,'runtime_tested':False,'TAI5MSG_read':False,
        'elapsed_seconds':time.monotonic()-t})
    if a.late_failure_probes:
        original = final_layout.audit_output; probes=[]; byfile = {r.file:r for r in requests}
        for uid,u in obligations.units.items():
            if u['file'] not in byfile:
                probes.append({'unit':uid,'status':'NOT_OBSERVED'});continue
            q=byfile[u['file']]; before=sha256(q.source); pc={k:sha256(v) for k,v in q.pc_assets.items()}; evidence={}
            def injected(data,journal,ownership,offsets,prefix,regions=()):
                indexes=[i for i,c in enumerate(ownership) if c.unit==uid]
                require(bool(indexes),'FAULT_TARGET_UNIT_NOT_PRESENT',uid)
                index=indexes[0]; changed=list(ownership)
                changed[index]=replace(changed[index],unit='INVALID_TEST_ONLY_UNIT')
                audited=original(data,journal,tuple(changed),offsets,prefix,regions)
                evidence.update(target_step=ownership[index].step,
                    audit_detected=any('FINAL_RESPONSIBILITY_UNIT_MISMATCH' in x for x in audited.errors),
                    final_table_staged=journal[-1].writer=='FINAL_TABLE',audit_errors=list(audited.errors))
                return audited
            with patch.object(final_layout,'audit_output',injected): failed=engine.run_file(q)
            ok=evidence.get('audit_detected') and evidence.get('final_table_staged') and failed.assembled is None and not failed.local_complete and before==sha256(q.source) and pc=={k:sha256(v) for k,v in q.pc_assets.items()} and final_layout.audit_output is original
            probes.append({'unit':uid,'file':q.file,'pass':bool(ok),'partial_assembled_object_returned':failed.assembled is not None,**evidence})
        dump(out/'LATE_FAILURE_DISCARD_PROBES.json',{'rows':probes,'passed':sum(bool(r.get('pass')) for r in probes),
            'boundary':'Late-final ownership metadata fault only, not all fault classes or full-product acceptance.'})
    print('COMPLETE DIAGNOSTIC; product_accepted=False; candidate_files_emitted=0',flush=True)
    return 0

if __name__ == '__main__':
    raise SystemExit(main())
