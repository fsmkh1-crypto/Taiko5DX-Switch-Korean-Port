"""Active IM03 manifest caller, replacing the old NUL-slicing runner.

Loads only JSON, fixed canonical catalogs and local bytes; no exec/import of
handoff code. Writes diagnostics/receipts only. No EVENT/IPS/package exporter.
Exit 0 = locally complete IM03 pipeline, 2 = blocked/incomplete, 3 = invalid input.
None of these exit codes asserts V371 or runtime acceptance.
"""
from __future__ import annotations
import argparse,json,sys,zipfile
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))
from builder.selective_event_contracts import (
 ContractError,Proof,Span,RecipeContract,RecipeKind,RegionAuthority,
 InteriorFieldBinding,ReviewedInteriorRecipe,require,sha256,
)
from builder.selective_event_contract_catalog import load_catalog,OWNERS
from builder.selective_event_recipe_catalog import load_existing_recipes
from builder.selective_event_obligation_catalog import load_obligations
from builder.selective_event_obligation_receipts import (
 Action,RewriteRegistry,PreservationPermit,ExactRewrite,ObligationEngine,
)
from builder.selective_event_final_layout import SourceIdentity,MapPoint,FieldSlot
from builder.selective_event_relocation_adapter import ReviewedFieldRule
from builder.selective_event_field_policy import load_field_policy
from builder.selective_event_overlap import (
 IntegratedSerializer,FileRequest,PayloadDirective,PreparedProjection,OccurrenceAction,
 RootInput,reviewed_secondary_header_disposition,
)


class ManifestInputs:
    def __init__(self,root:Path,documents:dict):
        self.root=root.resolve();self.documents=documents;self.cache={};self.receipts=[]

    def path(self,name:str) -> Path:
        require(type(name) is str and bool(name),'INVALID_INPUT_PATH',name)
        p=(self.root/name).resolve()
        require(p.is_relative_to(self.root) and p.is_file(),'INPUT_PATH_OUTSIDE_ROOT_OR_MISSING',name)
        return p

    def proof(self,spec:dict) -> Proof:
        key=spec['document'];doc=self.documents.get(key)
        require(doc is not None,'PROOF_DOCUMENT_NOT_PROVISIONED',key)
        if key not in self.cache:
            p=self.path(doc['path'])
            if doc.get('member') is not None:
                with zipfile.ZipFile(p) as z:
                    require(len(z.namelist())==len(set(z.namelist())),'DUPLICATE_PROOF_ZIP_MEMBER',key)
                    info=z.getinfo(doc['member']);require(info.file_size<=128*1024*1024,'PROOF_DOCUMENT_TOO_LARGE',key)
                    raw=z.read(info)
            else:raw=p.read_bytes()
            require(len(raw)==doc['bytes'] and sha256(raw)==doc['sha256'],'PROOF_DOCUMENT_IDENTITY',key)
            self.cache[key]=raw
            self.receipts.append({'kind':'PROOF_DOCUMENT','id':key,'bytes':len(raw),'sha256':sha256(raw),
                                  'claim_boundary':'IDENTITY_CHECK_NOT_PROOF_OF_ARBITRARY_DOCUMENT_TRUTH'})
        raw=self.cache[key]
        require(spec['sha256']==sha256(raw),'PROOF_REFERENCE_HASH_MISMATCH',key)
        row=spec.get('row')
        require(row is None or type(row) is int and 1<=row<=len(raw.splitlines()),'PROOF_ROW_BOUNDS',key)
        return Proof(key,spec['sha256'],spec['claim'],row)

    def asset(self,spec:dict,asset:str) -> tuple[bytes,SourceIdentity]:
        proof=self.proof(spec['proof']);p=self.path(spec['path']);b=p.read_bytes()
        ident=SourceIdentity(asset,spec['bytes'],spec['sha256'],proof);ident.verify(asset,b)
        self.receipts.append({'kind':'BYTE_INPUT','asset':asset,'bytes':len(b),'sha256':ident.sha256,'authority':proof.document})
        return b,ident


def read_requests(manifest:dict,store:ManifestInputs,im,recipes:dict):
    require(manifest.get('schema')=='V371_IM03_REQUEST_V1','REQUEST_SCHEMA','')
    source_rows={r['owner']:r for r in im.source_rows.get(OWNERS,())}
    # Optional exact direct extent contracts may be supplied by a reviewed
    # adapter. Never derive them from current bytes, role labels or a NUL scan.
    extensions=manifest.get('exact_direct_recipes',[])
    seen=set()
    for x in extensions:
        key=x['owner'];require(key in im.owners and key not in recipes and key not in seen,
                              'RECIPE_EXTENSION_CANNOT_OVERRIDE_CANONICAL',key);seen.add(key)
        o=im.owners[key];row=source_rows[key];p=store.proof(x['boundary_proof'])
        require(o.needs_upstream_recipe and x['recipe_id']==o.recipe_id and
                x['source_span'][0]==o.observed_span.start and
                row['binding']['member']=='DIRECT_HEADER_PRESERVED.jsonl' and
                x['pc_span'][0]==row['recipe']['pc_offset'], 'EXACT_DIRECT_BINDING_SCOPE',key)
        recipes[key]=RecipeContract(key,o.recipe_id,RecipeKind.DIRECT,'stock:'+o.file,
             RegionAuthority(Span(*x['source_span']),x['source_sha256'],p),p,o.source_header,
             'pc:'+o.file,RegionAuthority(Span(*x['pc_span']),x['pc_sha256'],p),o.source_header,
             transform_obligations=tuple(x.get('transform_obligations',())))
    interiors={}
    for x in manifest.get('reviewed_interior_recipes',[]):
        key=x['owner'];require(key in im.owners and key in recipes and key not in interiors,
                              'REVIEWED_INTERIOR_RECIPE_SCOPE',key)
        p=store.proof(x['authority'])
        slots=tuple(InteriorFieldBinding(s['field'],Span(*s['source_span']),s['relative'],
                    s['source_word_sha256'],s['source_target'],s['codec'],s['partition'],s.get('unit'))
                    for s in x['slots'])
        interiors[key]=ReviewedInteriorRecipe(key,x['recipe_id'],Span(*x['source_span']),x['source_sha256'],
                    Span(*x['pc_span']),x['pc_sha256'],x['payload_sha256'],x['identity_map'],slots,p)
    requests=[]
    used_interiors=set()
    for x in manifest.get('files',[]):
        file=x['file'];s,identity=store.asset(x['source'],file)
        pcs={}
        for a in x.get('pc_assets',[]):
            require(a['asset'] not in pcs,'DUPLICATE_PC_ASSET',a['asset'])
            pcs[a['asset']]=store.asset(a,a['asset'])[0]
        ds=[]
        for d in x.get('payloads',[]):
            ds.append(PayloadDirective(d['owner'],d['prepared_sha256'],bytes.fromhex(d['after_hex']),store.proof(d['authority']),
                tuple(MapPoint(p['source'],p['relative'],store.proof(p['authority'])) for p in d.get('points',[])),
                tuple(FieldSlot(p['field'],Span(*p['source_span']),p['relative'],store.proof(p['authority'])) for p in d.get('slots',[])),
                tuple(PreparedProjection(Span(*p['prepared_span']),Span(*p['relative_span']),store.proof(p['authority']))
                      for p in d.get('projections',[]))))
        acts=tuple(OccurrenceAction(a['id'],Action(a['action']),a.get('rewrite_id'),a.get('preservation_permit'))
                   for a in x.get('occurrence_actions',[]))
        use=x.get('use_reviewed_t01_preservation',False)
        require(type(use) is bool,'T01_DISPOSITION_SWITCH_TYPE',file)
        require(not use or file=='ECF00000.TS5','T01_DISPOSITION_FILE_SCOPE',file)
        dispositions=(reviewed_secondary_header_disposition(im),) if use else ()
        rules=tuple(ReviewedFieldRule(r['field'],r['codec'],r['source_word_sha256'],r['source_target'],r['partition'],
                       r.get('unit'),r.get('intrusion',0),store.proof(r['authority'])) for r in x.get('field_rules',[]))
        file_interiors=tuple(ic for owner,ic in interiors.items() if im.owners[owner].file==file)
        used_interiors.update(ic.owner for ic in file_interiors)
        requests.append(FileRequest(file,s,identity,pcs,tuple(ds),acts,dispositions,rules,file_interiors))
    require(used_interiors==set(interiors),'UNUSED_REVIEWED_INTERIOR_RECIPE',sorted(set(interiors)-used_interiors))
    rewrites=[];permits=[]
    for r in manifest.get('rewrites',[]):
        rewrites.append(ExactRewrite(r['id'],r['occurrence'],r['recipe_id'],bytes.fromhex(r['before_hex']),
                      bytes.fromhex(r['after_hex']),r['prepared_sha256'],store.proof(r['authority'])))
    for r in manifest.get('preservation_permits',[]):
        permits.append(PreservationPermit(r['id'],r['occurrence'],r['recipe_id'],r['before_sha256'],store.proof(r['authority'])))
    roots=[]
    for r in manifest.get('roots',[]):
        b,i=store.asset(r,'TAI5MSG:FINAL')
        loc=tuple((a['id'],a['block'],a['local'],Span(*a['span']),a.get('partition',0),store.proof(a['proof']))
                  for a in r.get('locators',[]))
        roots.append(RootInput('TAI5MSG:FINAL',b,i,loc))
    return tuple(requests),RewriteRegistry(rewrites,permits),tuple(roots)


def write_json(path:Path,value):path.write_text(json.dumps(value,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    for name in ('plan','v366','v369','field-policy','manifest','input-root','out'):parser.add_argument('--'+name,type=Path,required=True)
    a=parser.parse_args()
    require(not a.out.exists(),'OUTPUT_DIRECTORY_MUST_BE_NEW',a.out)
    a.out.mkdir(parents=True)
    try:
        raw=a.manifest.read_bytes();manifest=json.loads(raw)
        im=load_catalog(a.plan);policy=load_field_policy(a.field_policy,im)
        oc=load_obligations(a.plan,a.v369);recipes,recipe_summary=load_existing_recipes(im,a.v366,a.v369)
        inputs=ManifestInputs(a.input_root,manifest.get('proof_documents',{}))
        requests,registry,roots=read_requests(manifest,inputs,im,recipes)
        engine=ObligationEngine(oc,im,recipes,registry);co=IntegratedSerializer(im,engine,policy)
        run=co.run(requests,run_id=str(manifest.get('run_id','IM03'))+':'+sha256(raw),roots=roots)
        summary=run.summary();summary['manifest_sha256']=sha256(raw);summary['canonical_recipe_adapter']=recipe_summary
        summary['role_aware_field_policy']=policy.summary()
        write_json(a.out/'SUMMARY.json',summary);write_json(a.out/'INPUT_RECEIPTS.json',inputs.receipts)
        with (a.out/'OBLIGATION_RECEIPTS.jsonl').open('w',encoding='utf-8') as f:
            for r in run.obligations.receipts:f.write(json.dumps(r.to_dict(),sort_keys=True,ensure_ascii=False)+'\n')
        # Diagnostics only; never write the assembled EVENT buffers to disk.
        for fr in run.files:
            write_json(a.out/(fr.file+'.attempts.json'),[
                {'operation':r.operation,'status':r.status.value,'reasons':list(r.reasons),'details':r.details}
                for r in fr.attempts])
            if fr.assembled is not None:
                write_json(a.out/(fr.file+'.writer_journal.json'),[j.to_dict() for j in fr.assembled.journal])
        print(json.dumps({'file_runs':len(run.files),'complete_local_pipeline':run.complete_local_pipeline,
                          'product_accepted':False,'V371_closed':False,'diagnostics':str(a.out)}))
        return 0 if run.complete_local_pipeline else 2
    except (ContractError,KeyError,TypeError,ValueError,OSError,zipfile.BadZipFile) as ex:
        write_json(a.out/'INPUT_ERROR.json',{'code':getattr(ex,'code',type(ex).__name__),'detail':str(ex),
                                           'product_accepted':False,'V371_closed':False})
        print(str(ex),file=sys.stderr);return 3

if __name__=='__main__':raise SystemExit(main())
