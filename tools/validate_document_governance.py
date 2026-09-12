#!/usr/bin/env python3
from __future__ import annotations
import argparse, hashlib, json, re, sys
from pathlib import Path

PLAN_TERMS=("next stage","next step","current plan","recommended next","현재 계획","다음 단계","다음 작업")

def git_blob_sha1(data:bytes)->str:
    return hashlib.sha1(b"blob "+str(len(data)).encode()+b"\0"+data).hexdigest()

def fail(msg):
    raise RuntimeError(msg)

def main():
    ap=argparse.ArgumentParser(); ap.add_argument('--repo-root',type=Path,default=Path('.')); a=ap.parse_args(); root=a.repo_root.resolve()
    idxp=root/'docs/DOCUMENT_AUTHORITY_INDEX.json'; idx=json.loads(idxp.read_text(encoding='utf-8'))
    entries=idx.get('documents',[]); paths=[x['path'] for x in entries]
    if len(paths)!=len(set(paths)): fail('INV-DOC-05 duplicate registry path')
    if paths.count('docs/DOCUMENT_AUTHORITY_INDEX.json')!=1: fail('INV-DOC-05 registry must self-register exactly once')
    missing=[p for p in paths if not (root/p).is_file()]
    if missing: fail(f'INV-DOC-05 indexed nonexistent paths: {missing}')
    actual=set()
    actual.update(str(p.relative_to(root)).replace('\\','/') for p in root.glob('*.md') if p.is_file())
    actual.update(str(p.relative_to(root)).replace('\\','/') for p in (root/'docs').rglob('*.md') if p.is_file())
    br=root/'builder/README.md'
    if br.is_file(): actual.add('builder/README.md')
    indexed_md={p for p in paths if p.endswith('.md')}
    if actual!=indexed_md:
        fail(f'INV-DOC-05 markdown coverage mismatch missing_from_index={sorted(actual-indexed_md)} nonexistent_indexed={sorted(indexed_md-actual)}')
    resume=[x['path'] for x in entries if x['authority_scope']=='PROJECT_RESUME' and x['current_authority']]
    if resume!=['PROJECT_STATE.md']: fail(f'INV-DOC-01 project resume authority: {resume}')
    for e in entries:
        p=e['path']
        if not p.endswith('.md') or e['current_authority']: continue
        text=(root/p).read_text(encoding='utf-8',errors='replace').lower()
        if any(term in text for term in PLAN_TERMS):
            sup=e.get('superseded_as_plan_by')
            if not sup or not (root/sup).is_file(): fail(f'INV-DOC-02 stale plan language lacks supersession metadata: {p}')
    for e in entries:
        if not e.get('anchor_protected'): continue
        data=(root/e['path']).read_bytes(); got=git_blob_sha1(data)
        if got!=e.get('registered_blob_sha'): fail(f'INV-DOC-03 anchor-protected blob changed: {e["path"]} {got}')
    agents=(root/'AGENTS.md').read_text(encoding='utf-8')
    if 'AGENTS.md -> PROJECT_STATE.md -> PROJECT_STATE.required_reads' not in agents: fail('INV-DOC-04 fixed read chain missing')
    if 'as applicable' in agents.lower(): fail('INV-DOC-04 open-ended pre-read wording reintroduced')
    state=(root/'PROJECT_STATE.md').read_text(encoding='utf-8')
    m=re.search(r'<!-- PROJECT_RESUME_V2\s*(\{.*?\})\s*PROJECT_RESUME_V2 -->',state,re.S)
    if not m: fail('INV-DOC-04 PROJECT_RESUME_V2 marker missing')
    resume_obj=json.loads(m.group(1))
    for p in resume_obj.get('required_reads',[]):
        if not (root/p).is_file(): fail(f'INV-DOC-04 required read missing: {p}')
    out={'schema':'DOCUMENT_GOVERNANCE_VALIDATION_V1','result':'PASS','invariants':['INV-DOC-01','INV-DOC-02','INV-DOC-03','INV-DOC-04','INV-DOC-05'],'registered_documents':len(entries),'registered_markdown':len(indexed_md),'project_resume_authority':'PROJECT_STATE.md','required_reads':resume_obj.get('required_reads',[])}
    print(json.dumps(out,ensure_ascii=False,indent=2,sort_keys=True)); return 0

if __name__=='__main__':
    try: raise SystemExit(main())
    except Exception as exc:
        print(json.dumps({'schema':'DOCUMENT_GOVERNANCE_VALIDATION_V1','result':'FAIL','error':str(exc)},ensure_ascii=False,indent=2),file=sys.stderr); raise SystemExit(1)
