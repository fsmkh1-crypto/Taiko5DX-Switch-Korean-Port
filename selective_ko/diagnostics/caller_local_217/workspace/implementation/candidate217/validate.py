"""Bounded in-memory integration: existing root chain plus five audit consumers."""
from pathlib import Path
import sys,json,hashlib,collections
from dataclasses import replace
BASE=Path(__file__).resolve().parents[2]; OUT=Path(__file__).parent/'results'
OUT.mkdir(exist_ok=True)
WORK=BASE/'implementation/two_root_overlay/work'
sys.path.insert(0,str(WORK))
from builder.selective_event_contracts import Proof,Span,sha256
from builder.selective_event_contract_catalog import load_catalog
from builder.selective_event_recipe_catalog import load_existing_recipes
from builder.selective_event_obligation_catalog import load_obligations
from builder.selective_event_obligation_receipts import ObligationEngine
from builder.selective_event_field_policy import load_field_policy
from builder.selective_event_overlap import IntegratedSerializer,RootInput
from builder.selective_event_final_layout import SourceIdentity
from builder.selective_event_root_values import SerializedRootValues
from builder.selective_tai5msg_additional_roots import reconstruct_with_additional_roots,PROFILE
from tools.validate_event_overlap import read_requests
# Reuse only the inherited, hash-checking proof cache; no replay main is invoked.
R=BASE/'evidence/backup/work/resume'
sys.path.append(str(R))
from replay import PinnedInputStore
def save(name,obj):
    (OUT/name).write_text(json.dumps(obj,ensure_ascii=False,indent=2)+'\n')
raw=BASE/'evidence/raw_inputs'
codes={x[0] for x in json.loads((raw/'MAPPING_10036_CACHE.json').read_text())['entries']}
data,report=reconstruct_with_additional_roots((raw/'PC_ORIGINAL_TAI5MSG.DAT').read_bytes(),(raw/'PC_KO_TAI5MSG.DAT').read_bytes(),WORK,codes,profile=PROFILE)
assert sha256(data)=='eddf9cf57332f090fde2c6b9ed707342fc57c1ed6a366de89c553b707953ba1c'
save('TAI5MSG_RECONSTRUCTION.json',report)
proof=Proof('TAI5MSG_RECONSTRUCTION',sha256((OUT/'TAI5MSG_RECONSTRUCTION.json').read_bytes()),'ACTUAL_SERIALIZED_PROFILE_AND_DERIVED_LOCATORS_NOT_PRODUCT_ACCEPTANCE')
au=R/'authorities';plan=au/'v371_operation_obligation_plan_20260922.zip'
im=load_catalog(plan);oc=load_obligations(plan,au/'V369_V368_EXACT_APPLICABILITY_2438.zip')
policy=load_field_policy(au/'ROLE_AWARE_FIELD_POLICY_24305.jsonl',im)
recipes,_=load_existing_recipes(im,au/'V366_EVENT_169_EXACT_LEDGER_RECONSTRUCTION_LARGE_ARTIFACTS.zip',au/'V369_V368_EXACT_APPLICABILITY_2438.zip')
sys.path.insert(0,str(BASE/'implementation/caller_local_redesign'))
from caller_local import Redesign,Rejected
sys.path.insert(0,str(BASE/'implementation/caller_local_integration'))
from compose import compose
sys.path.insert(0,str(BASE/'implementation/residual75_integration'))
from residual import Residual
D=BASE/'analysis/redesign_remaining_10'
ledger=(D/'REDESIGN_DECISIONS_143.json').read_bytes();mapping=(raw/'MAPPING_10036_CACHE.json').read_bytes()
redesign=Redesign(ledger,mapping,sha256(ledger),sha256(mapping))
selected_owners={k for k,rs in redesign.rows.items() if all(r['design_status']=='BOUNDARY_DESIGN_DECIDED' for r in rs)}
residual_bytes=(BASE/'analysis/residual75_design/DECISIONS_75.json').read_bytes()
residual=Residual(residual_bytes,sha256(residual_bytes),redesign.encode)
selected_files={k.split(':')[0] for k in selected_owners}
selected_owners={k for k in selected_owners if k.split(':')[0] in selected_files}
m=json.loads((R/'active_inputs/ACTIVE_REQUEST_ALL_LEGACY_169.json').read_text())
m['files']=[r for r in m['files'] if r['file'] in selected_files]
m['reviewed_interior_recipes']=[r for r in m.get('reviewed_interior_recipes',[]) if r['owner'].split(':')[0] in selected_files]
store=PinnedInputStore(R/'active_inputs',m['proof_documents'])
requests,registry,roots=read_requests(m,store,im,recipes);assert not roots
reader=SerializedRootValues(data); locators=[]
for rid,row in oc.roots.items():
    p=row['proof'];block=reader.parsed.blocks[p['block']];local=p['local']
    span=Span(block.file_offset+block.offsets[local],block.file_offset+block.offsets[local+1])
    locators.append((rid,p['block'],local,span,p['block'],proof))
root=RootInput('TAI5MSG:FINAL',data,SourceIdentity('TAI5MSG:FINAL',len(data),sha256(data),proof),tuple(locators))
engine=ObligationEngine(oc,im,recipes,registry)
from builder.selective_event_overlap import PayloadDirective,PreparedProjection
from builder.selective_event_final_layout import MapPoint,FieldSlot
coordinator=IntegratedSerializer(im,engine,policy)
authority=Proof('CALLER_LOCAL_142_PLUS_RESIDUAL75',sha256(ledger+residual_bytes),'USER_AUTHORIZED_SUPPLEMENTAL_INTEGRATION_NOT_CANONICAL_PROMOTION')
from builder.selective_event_obligation_receipts import ExactRewrite,RewriteRegistry,Action
from builder.selective_event_overlap import OccurrenceAction
spec_bytes=(BASE/'implementation/residual75_integration/rewrite_specs.json').read_bytes();specs=json.loads(spec_bytes)
rewrite_authority=Proof('RESIDUAL75_EXACT_OCCURRENCE_REWRITES',sha256(spec_bytes),'EXACT_FOUR_REWRITES_DERIVED_FROM_USER_AUTHORIZED_RESIDUAL75_DESIGN_NOT_CANONICAL_POLICY_CHANGE')
new_rules=[];rewritten=[]
new_requests=[];connections=[];conflicts=[];removed=[]
for q in requests:
 baseline=coordinator.run_file(q)
 assert baseline.local_complete, (q.file,baseline.summary())
 payloads={d.owner:d for d in q.payloads}
 for owner in sorted(selected_owners):
  if owner.split(':')[0]!=q.file:continue
  recipe=recipes[owner];pc=q.pc_assets[recipe.pc_asset][recipe.pc.span.start:recipe.pc.span.end];source=q.source[recipe.source.span.start:recipe.source.span.end]
  prepared=baseline.prepared[owner].data;old=baseline.directives[owner]
  try:
   changed=redesign.apply(owner,source,pc,prepared)
   changed,inherited_edits=compose(changed,old)
   if owner in residual.rows:changed=residual.apply(owner,changed)
   points=tuple(MapPoint(p.source,changed.project(p.relative,p.relative+1)[0],p.authority) for p in old.points)
   slots=tuple(FieldSlot(s.field,s.source_span,changed.project(s.relative,s.relative+s.source_span.size)[0],s.authority) for s in old.slots)
   projections=[]
   for oid,row in oc.occurrences.items():
    if row['owner']!=owner:continue
    x=row['exact_occurrence'];a=x['escape_start']-recipe.pc.span.start;z=x['literal_end']-recipe.pc.span.start
    try:dst=changed.project(a,z)
    except Rejected as ex:
     if oid not in specs:
      removed.append({'owner':owner,'occurrence':oid,'relative_span':[a,z],'reason':str(ex)});continue
     spec=specs[oid];assert spec['owner']==owner and spec['source_relative_span']==[a,z]
     assert spec['decision'] in [r['id'] for r in residual.rows[owner]]
     before=redesign.encode(spec['before']);after=redesign.encode(spec['after']);dst=tuple(spec['final_relative_span'])
     assert prepared[a:z]==before and changed.after[dst[0]:dst[1]]==after and dst[1]-dst[0]==len(after)
     ruleid='RESIDUAL75:'+oid
     new_rules.append(ExactRewrite(ruleid,oid,recipe.recipe_id,before,after,sha256(prepared),rewrite_authority))
     rewritten.append({'occurrence':oid,'owner':owner,'decision':spec['decision'],'source_relative_span':[a,z],'final_relative_span':list(dst),'before_sha256':sha256(before),'after_sha256':sha256(after),'rule_id':ruleid})
    projections.append(PreparedProjection(Span(a,z),Span(*dst),authority))
   # Deduplicate exact requested source spans without inferring deleted references.
   projections=tuple({(p.prepared_span.start,p.prepared_span.end):p for p in projections}.values())
   payloads[owner]=PayloadDirective(owner,sha256(prepared),changed.after,authority,points,slots,projections)
   connections.append({'owner':owner,'audit_ids':[r['audit_id'] for r in redesign.rows[owner]],'before_sha256':sha256(prepared),'after_sha256':sha256(changed.after),'bytes_before':len(prepared),'bytes_after':len(changed.after),'residual_ids':[r['id'] for r in residual.rows.get(owner,[])],'inherited_edits':len(inherited_edits),'existing_points':len(points),'existing_slots':len(slots),'preserved_occurrence_projections':len(projections)})
  except (Rejected,AttributeError) as ex:conflicts.append({'owner':owner,'reason':str(ex)})
 actions={a.id:a for a in q.occurrence_actions}
 for r in new_rules:
  if specs[r.occurrence]['owner'].split(':')[0]==q.file:
   assert r.occurrence in actions
   actions[r.occurrence]=OccurrenceAction(r.occurrence,Action.TRANSFORM,r.id,None)
 new_requests.append(replace(q,payloads=tuple(payloads.values()),occurrence_actions=tuple(actions.values())))
 print('CONNECTED',q.file,flush=True)
save('CONNECTIONS.json',connections);save('CONFLICTS.json',conflicts);save('CHANGED_OCCURRENCES.json',removed)
assert len(new_rules)==4 and len({r.occurrence for r in new_rules})==4
save('EXACT_REWRITES_4.json',rewritten)
registry=RewriteRegistry((*registry.rules.values(),*new_rules),registry.permits.values())
engine=ObligationEngine(oc,im,recipes,registry)
class Traced(IntegratedSerializer):
 def run_file(self,q):
  r=super().run_file(q);save(q.file+'.summary.json',r.summary());print('REPLAY',q.file,r.local_complete,flush=True);return r
result=Traced(im,engine,policy).run(new_requests,run_id='CALLER_LOCAL_142_PLUS_RESIDUAL75_AFFECTED_FILES',roots=(root,))
save('RUN_SUMMARY.json',result.summary());save('INPUT_RECEIPTS.json',store.receipts)
save('OBLIGATION_RECEIPTS.json',[r.to_dict() for r in result.obligations.receipts])
readbacks=[]
for run in result.files:
 if run.assembled is None:continue
 for row in connections:
  if row['owner'].split(':')[0]!=run.file:continue
  owner=row['owner'];s=run.owner_recipe_spans[owner];actual=run.assembled.data[s.start:s.end];expected=run.directives[owner].after
  assert actual==expected
  readbacks.append({'owner':owner,'span':[s.start,s.end],'sha256':sha256(actual),'matches_directive':True})
save('FINAL_READBACKS.json',readbacks)
summary={'exact_occurrence_rewrites_connected':len(new_rules),'new_residual_boundaries':sum(len(r['residual_ids']) for r in connections),'new_residual_owners':sum(bool(r['residual_ids']) for r in connections),'selected_owners':len(selected_owners),'selected_files':len(selected_files),'connected_owners':len(connections),'connected_boundaries':sum(len(r['audit_ids']) for r in connections),'connection_conflicts':len(conflicts),'changed_occurrences_requiring_new_authority':len(removed),'files_local_complete':sum(r.local_complete for r in result.files),'files_replayed':len(result.files),'bridge_errors':list(result.bridge_errors),'final_owner_readbacks':len(readbacks),'obligations':result.obligations.summary(),'V369':'UNCHANGED','V371':'PARTIAL_BLOCKED','product_accepted':False,'game_files_written':0}
save('SUMMARY.json',summary);print(json.dumps(summary,indent=2),flush=True)

# Candidate-level verification; no installable artifact is emitted here.
from package_builder import prerequisites,BUILD,sha
ips,font,prereq=prerequisites(raw/'V361_DIAG.zip')
save('PREREQUISITES.json',prereq)
assert len(result.files)==13 and all(r.local_complete for r in result.files) and not result.bridge_errors and not conflicts
prior={r['owner']:r for r in json.loads((BASE/'implementation/residual75_integration/COMBINED_OWNER_RECEIPTS_139.json').read_text())}
assert len(readbacks)==139
for r in readbacks:assert r['sha256']==prior[r['owner']]['sha256']
records=[r.to_dict() for r in result.obligations.receipts]
for oid in specs:assert next(r for r in records if r['obligation']==oid)['state']=='SATISFIED_LOCAL_OBLIGATION'
assert not any(r['state']=='BLOCKED' for r in records)
members={'exefs/'+BUILD+'.ips':ips,'romfs/FONT/FONT_JPN.G1T':font,'romfs/TAI5MSG_JP.DAT':data}
for run in result.files:members['romfs/EVENT/'+run.file]=run.assembled.data
save('CANDIDATE_MEMBER_PLAN.json',{'title_id':'0100346017304000','version':'1.1.3','build_id':BUILD,'event_files':13,'payload_members':[{'path':k,'bytes':len(v),'sha256':sha(v)} for k,v in sorted(members.items())],'builder_source_commit':None,'source_freeze_required':True,'game_files_written':0,'installable_zip_written':False,'runtime_PASS':False})
# Pin actually imported workspace source, plus this runner and the packager.
codefiles={Path(__file__).resolve(),(Path(__file__).parent/'package_builder.py').resolve()}
for mod in sys.modules.values():
 f=getattr(mod,'__file__',None)
 if f and f.endswith('.py') and str(Path(f).resolve()).startswith(str(BASE)+'/'):codefiles.add(Path(f).resolve())
save('SOURCE_FREEZE_REQUIRED.json',[{'local_path':str(p),'workspace_relative_path':str(p.relative_to(BASE)),'sha256':sha(p.read_bytes())} for p in sorted(codefiles)])
print('CANDIDATE13 verified; package withheld pending exact Git source freeze',flush=True)
