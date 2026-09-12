from __future__ import annotations
import hashlib,json
from collections import Counter,defaultdict
from pathlib import Path

def sha256(b:bytes)->str:return hashlib.sha256(b).hexdigest()
def git_blob_sha1(b:bytes)->str:return hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()
def load_sharded(d:Path):
 idx=json.loads((d/'INDEX.json').read_text());rows=[];raw=b''
 for q in idx['parts']:
  b=(d/q['file']).read_bytes();assert sha256(b)==q['sha256'];lines=b.decode().splitlines(True);assert len(lines)==q['rows'];raw+=b;rows.extend(json.loads(x) for x in lines if x.strip())
 assert len(rows)==idx['total_rows'] and sha256(raw)==idx['logical_content_sha256'];return rows,idx
def load_migration(d:Path):
 idx=json.loads((d/'INDEX.json').read_text());groups={};n=0
 for q in idx['parts']:
  b=(d/q['file']).read_bytes();assert sha256(b)==q['sha256'];o=json.loads(b);assert o['entity_type']==q['entity_type'] and len(o['entity_ids'])==q['rows'];groups[o['entity_type']]=o['entity_ids'];n+=len(o['entity_ids'])
 assert n==idx['total_entries'];return groups,idx
def expand_state(r):
 c={'source_id':r['source_id'],'pc_record':r['pc_record'],'revision':1,'source_family':'inline','applicability_state':'APPLICABLE','exclusion_claim_id':None,'changed_by':{'type':'MIGRATION','refs':['MIGRATION-F1-PILOT-2026-09-12']},'supersedes_revision':None};i={'family':'F1_LOCALIZATION_SEQUENCE','localization_id':r['localization_id'],'target_object':r['target_object'],'segment_delta':r['segment_delta']};cat=r['category']
 if cat=='DIRECT':return {**c,'analysis_state':'RESOLVED','target_status':'RESOLVED','target_identity':i,'candidate_target_identity':None,'language_domain':'JP_ONLY','storage_class':'STATIC_RODATA','window_object_cardinality':'1:1','logical_owner_count':r['logical_owner_count'],'write_authority':'AUTHORIZED','write_authority_family':'F1_LOCALIZATION_STATIC_DIRECT','handoff_family':None,'closure_state':'CLOSED','terminal_disposition':'DIRECT_PORT','blocker':None,'unknown_fields':[],'evidence_refs':['V088','V089','V093','V094']}
 if cat=='PADDING':return {**c,'analysis_state':'RESOLVED','target_status':'RESOLVED','target_identity':i,'candidate_target_identity':None,'language_domain':'JP_ONLY','storage_class':'STATIC_RODATA','window_object_cardinality':'1:1','logical_owner_count':r['logical_owner_count'],'write_authority':'NOT_AUTHORIZED','write_authority_family':'F1_PADDING_RECONSTRUCTION','handoff_family':'F1_PADDING_RECONSTRUCTION','closure_state':'OPEN','terminal_disposition':'UNRESOLVED','blocker':'PADDING_RECONSTRUCTION_REQUIRED','unknown_fields':[],'evidence_refs':['V088','V091']}
 if cat=='CAPACITY':return {**c,'analysis_state':'RESOLVED','target_status':'RESOLVED','target_identity':i,'candidate_target_identity':None,'language_domain':'JP_ONLY','storage_class':'STATIC_RODATA','window_object_cardinality':'1:1','logical_owner_count':r['logical_owner_count'],'write_authority':'NOT_AUTHORIZED','write_authority_family':'F1_STORAGE_RECONSTRUCTION','handoff_family':'F1_STORAGE_RECONSTRUCTION','closure_state':'OPEN','terminal_disposition':'UNRESOLVED','blocker':'TERMINATOR_CAPACITY_FAIL','unknown_fields':[],'evidence_refs':['V088','V090']}
 if cat=='SHARED':
  u={'field':'owner_binding','reason':'Physical target has multiple logical localization owners and not every relevant PC obligation is bound.','resolution_requirement':'Bind every relevant logical owner to its PC obligation and prove replacement agreement or conflict before choosing I3 shared overwrite or I4 redirection.','blocks':['WRITE_AUTHORIZATION','CLOSURE'],'evidence_refs':['V089']};return {**c,'analysis_state':'RESOLVED','target_status':'RESOLVED','target_identity':i,'candidate_target_identity':None,'language_domain':'JP_ONLY','storage_class':'STATIC_RODATA','window_object_cardinality':'1:1','logical_owner_count':r['logical_owner_count'],'write_authority':'NOT_AUTHORIZED','write_authority_family':'SHARED_OWNER_BINDING','handoff_family':'SHARED_OWNER_BINDING','closure_state':'OPEN','terminal_disposition':'UNRESOLVED','blocker':'SHARED_OWNER_BINDING_REQUIRED','unknown_fields':[u],'evidence_refs':['V088','V089']}
 if cat=='REJECT':
  u={'field':'target_identity','reason':'F1 candidate relation was not canonically promoted by V088; it is not proven false but remains unresolved.','resolution_requirement':'Resolve this source under another verified target-resolution family or independently promote the candidate with new evidence.','blocks':['WRITE_AUTHORIZATION','CLOSURE'],'evidence_refs':['V088','V092']};return {**c,'analysis_state':'ANALYZED_UNRESOLVED','target_status':'UNRESOLVED','target_identity':None,'candidate_target_identity':{**i,'promotion_status':'F1_UNPROMOTED'},'language_domain':None,'storage_class':None,'window_object_cardinality':None,'logical_owner_count':None,'write_authority':'NOT_AUTHORIZED','write_authority_family':None,'handoff_family':'RESIDUAL_FAMILY_UNASSIGNED','closure_state':'OPEN','terminal_disposition':'UNRESOLVED','blocker':'F1_RULE_REJECTED_MIN_FINAL_INTERVAL','unknown_fields':[u],'evidence_refs':['V088','V092']}
 raise AssertionError(cat)
def classify_fixture(f):
 incoming=Counter(e['action_id'] for e in f['edges']);by=defaultdict(list)
 for e in f['edges']:by[e['source_id']].append(e['action_id'])
 out={}
 for s in f['sources']:
  a=by[s];n=len(a);m=max([incoming[x] for x in a],default=0);out[s]='N:M' if n>1 and m>1 else '1:N' if n>1 else 'N:1' if n==1 and m>1 else '1:1' if n==1 else '0:?'
 return out
