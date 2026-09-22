"""Migrated V371 serializer caller: IM01 -> final shape/writers -> IM02.

The four old runtime_end uses are replaced on this active path. The old prototype
is preserved under evidence/, never imported or executed. Real recipes/actions
and any missing field/interior authority MUST be provisioned by reviewed adapters;
this module does not issue grammar permits or infer lengths from NULs. No product
file exporter, blanket role exemption, --force, or partial-product PASS exists.
"""
from __future__ import annotations
from collections import Counter, defaultdict
from dataclasses import dataclass, field
from types import MappingProxyType
from typing import Mapping, Iterable

from .selective_event_contracts import (
    ContractError, Proof, Span, Window, Route, Status, Result, RecipeContract,
    ReviewedInteriorRecipe, FieldState, FieldProposal, DependencyIdentity,
    FinalFieldAnchors, DispositionApproval,
    MappedWindow, require, sha256, blocked,
)
from .selective_event_contract_catalog import ContractCatalog, FIELDS, OWNERS, UNITS
from .selective_event_role_session import RoleContractSession
from .selective_event_obligation_catalog import canonical_json
from .selective_event_obligation_receipts import (
    Action, Candidate, EvidenceBundle, ObligationEngine, BatchReport, OwnerView,
    Placement, RecipeInput, OccurrenceSubmission, RootBinding, SupportSubmission,
    UnitRegion, WriterRange,
)
from .selective_event_final_layout import (
    SourceIdentity, Geometry, MapPoint, FieldSlot, PayloadEdit, FieldWrite,
    ResponsibilityRegion, FinalLayout, AssembledFile,
)

from .selective_event_relocation_adapter import ReviewedFieldRule
from .selective_event_field_policy import FieldPolicyCatalog

def required_failure(result: Result) -> bool:
    """Observation failures remain data; required-phase failures cannot pass."""
    return (not result.operation.startswith('OBSERVE:')
            and result.status in (Status.BLOCKED, Status.NOT_OBSERVED, Status.FAILED))


@dataclass(frozen=True)
class PreparedProjection:
    """Exact post-transform span relative to one composed owner, not global offsets."""
    prepared_span: Span
    relative_span: Span
    authority: Proof


@dataclass(frozen=True)
class PayloadDirective:
    owner: str
    prepared_sha256: str
    after: bytes
    authority: Proof
    points: tuple[MapPoint,...]=()
    slots: tuple[FieldSlot,...]=()
    projections: tuple[PreparedProjection,...]=()

    def __post_init__(self):
        for name in ('points','slots','projections'):
            object.__setattr__(self,name,tuple(getattr(self,name)))
        require(type(self.after) is bytes and len(self.after)>=4 and len(self.after)%4==0
                and isinstance(self.authority,Proof),'INVALID_PAYLOAD_DIRECTIVE',self.owner)
        require(len({(p.prepared_span.start,p.prepared_span.end) for p in self.projections})==len(self.projections),
                'DUPLICATE_PREPARED_PROJECTION',self.owner)

    def project(self, span:Span, prepared:bytes) -> Span:
        require(sha256(prepared)==self.prepared_sha256 and span.end<=len(prepared),
                'PREPARED_PROJECTION_PREIMAGE',self.owner)
        if self.after==prepared: return span
        found=[p for p in self.projections if p.prepared_span==span]
        require(len(found)==1,'MISSING_EXACT_POST_TRANSFORM_PROJECTION',(self.owner,span))
        r=found[0]
        require(isinstance(r.authority,Proof) and r.relative_span.end<=len(self.after),
                'POST_TRANSFORM_PROJECTION_RANGE',self.owner)
        return r.relative_span


@dataclass(frozen=True)
class OccurrenceAction:
    id: str
    action: Action
    rewrite_id: str|None=None
    preservation_permit: str|None=None


@dataclass(frozen=True)
class FileRequest:
    file: str
    source: bytes
    source_identity: SourceIdentity
    pc_assets: Mapping[str,bytes]=field(default_factory=dict)
    payloads: tuple[PayloadDirective,...]=()
    occurrence_actions: tuple[OccurrenceAction,...]=()
    dispositions: tuple[DispositionApproval,...]=()
    field_rules: tuple[ReviewedFieldRule,...]=()
    interior_contracts: tuple[ReviewedInteriorRecipe,...]=()

    def __post_init__(self):
        require(all(type(k) is str and type(v) is bytes for k,v in self.pc_assets.items()),
                'IMMUTABLE_PC_ASSETS_REQUIRED',self.file)
        object.__setattr__(self,'pc_assets',MappingProxyType(dict(self.pc_assets)))
        for name in ('payloads','occurrence_actions','dispositions','field_rules','interior_contracts'):
            object.__setattr__(self,name,tuple(getattr(self,name)))


@dataclass(frozen=True)
class RootInput:
    artifact: str
    data: bytes
    identity: SourceIdentity
    # (ROOT:id, block, local, byte span, partition, reviewed locator authority)
    locators: tuple[tuple[str,int,int,Span,int,Proof],...]

    def __post_init__(self):
        object.__setattr__(self,'locators',tuple(tuple(x) for x in self.locators))
        require(type(self.data) is bytes and isinstance(self.identity,SourceIdentity),
                'ROOT_IMMUTABLE_INPUT_REQUIRED',self.artifact)
        for x in self.locators:
            require(len(x)==6 and isinstance(x[0],str) and bool(x[0])
                    and all(type(x[i]) is int and x[i]>=0 for i in (1,2,4))
                    and isinstance(x[3],Span) and x[3].end<=len(self.data)
                    and isinstance(x[5],Proof),'INVALID_ROOT_LOCATOR',self.artifact)
        require(len({x[0] for x in self.locators})==len(self.locators),'DUPLICATE_ROOT_LOCATOR',self.artifact)


@dataclass(frozen=True)
class FileRun:
    file: str
    request: FileRequest
    assembled: AssembledFile|None
    attempts: tuple[Result,...]
    owner_spans: Mapping[str,Span]
    prepared: Mapping
    directives: Mapping[str,PayloadDirective]
    recipe_inputs: tuple[RecipeInput,...]
    consumer_results: tuple[Result,...]
    retained_units: tuple[str,...]

    @property
    def local_complete(self):
        return self.assembled is not None and self.assembled.audit.local_complete and not any(required_failure(r) for r in self.attempts)

    def summary(self):
        return {'file':self.file,'local_complete':self.local_complete,
                'assembled_in_memory':self.assembled is not None,'product_accepted':False,
                'states':dict(Counter(r.status.value for r in self.attempts)),
                'blocking_operations':[{'operation':r.operation,'reasons':list(r.reasons)} for r in self.attempts
                                       if required_failure(r)],
                'physical_observations_not_normative':sum(r.operation.startswith('OBSERVE:') for r in self.attempts),
                'retained_units':list(self.retained_units),
                'layout':None if self.assembled is None else self.assembled.audit.to_dict()}


@dataclass(frozen=True)
class IntegratedRun:
    files: tuple[FileRun,...]
    evidence: EvidenceBundle|None
    obligations: BatchReport
    bridge_errors: tuple[str,...]
    expected_files: frozenset[str]
    product_accepted: bool=field(default=False,init=False)

    @property
    def complete_local_pipeline(self):
        return ({f.file for f in self.files}==self.expected_files and len(self.files)==len(self.expected_files)
                and all(f.local_complete for f in self.files) and not self.bridge_errors and self.obligations.local_complete)

    def summary(self):
        return {'scope':'IM03_IN_MEMORY_INTEGRATION_NOT_VAL01','file_runs':len(self.files),
                'expected_files':len(self.expected_files),'missing_files':sorted(self.expected_files-{r.file for r in self.files}),
                'file_summaries':[f.summary() for f in self.files],
                'bridge_errors':list(self.bridge_errors),'obligations':self.obligations.summary(),
                'complete_local_pipeline':self.complete_local_pipeline,
                'product_accepted':False,'V371_closed':False,'product_files_exported':0,
                'pending':['VAL01_FULL_CORPUS_OUTPUT_ACCEPTANCE','RUNTIME_SAFETY_NOT_CLAIMED']}

    def __bool__(self): raise TypeError('A local integrated run is not V371 PASS.')
    def emit_product(self,*args,**kwargs):
        raise ContractError('PRODUCT_EXPORT_REQUIRES_VAL01','IM03 has no game-file exporter.')


def _unique(seq,key,label):
    out={getattr(x,key):x for x in seq}
    require(len(out)==len(seq),'DUPLICATE_'+label,'')
    return out


def reviewed_secondary_header_disposition(catalog:ContractCatalog) -> DispositionApproval:
    """Explicit local plan disposition implementing the reviewed XB01 decision.

    Keeps the original field and T01. This is preservation, never a relocation
    PASS or a change to the V369 ledger. No fixture authority is involved.
    """
    f=catalog.fields.get('ECF00000.TS5:2DFC')
    require(f is not None and f.unit=='T01' and f.state==FieldState.DISPOSITION
            and f.source_header==bytes.fromhex('0400f03a')
            and 'XB01:EVENT16' in f.required_view_ids,
            'T01_REVIEWED_DISPOSITION_SCOPE','')
    require(any(p.expected==f.source_header and p.source_span==f.source_span for p in f.protected_ranges),
            'T01_SECONDARY_HEADER_PROTECTION_MISSING','')
    return DispositionApproval(f.field,'T01',sha256(f.source_header),'PRESERVE_SECONDARY_HEADER',f.proof)


class IntegratedSerializer:
    """Concrete active caller of IM01 preparation/views and IM02 receipts.

    Generic field execution labels do not provision nonidentity relocation rules.
    The six existing typed EVENT04 contracts can calculate their own final bits.
    Other necessary nonidentity operations remain explicit, named proof holds.
    """
    def __init__(self,im01:ContractCatalog,engine:ObligationEngine,
                 field_policy:FieldPolicyCatalog|None=None):
        require(engine.im01 is im01,'INTEGRATION_CATALOG_OBJECT_MISMATCH','')
        if field_policy is not None:
            field_policy.validate_catalog(im01)
        self.catalog=im01;self.engine=engine;self.field_policy=field_policy
        self.owners_by_file=defaultdict(dict);self.fields_by_file=defaultdict(dict)
        self.consumers_by_owner=defaultdict(list)
        for k,o in im01.owners.items():self.owners_by_file[o.file][k]=o
        for k,f in im01.fields.items():self.fields_by_file[k.rsplit(':',1)[0]][k]=f
        for c in im01.consumers.values():self.consumers_by_owner[c.owner].append(c)
        self.units_by_file=defaultdict(list)
        for k,u in engine.catalog.units.items():self.units_by_file[u['file']].append(k)
        self.expected_files=frozenset(self.owners_by_file)
        self.cluster_members=defaultdict(set);self.cluster_units={}
        for r in engine.catalog.relations.values():
            e=r['canonical_edge'];cid=e['cluster_id']
            self.cluster_members[cid].update((e['outer_owner'],e['inner_owner']))
            require(cid not in self.cluster_units or self.cluster_units[cid]==r['unit'],'CLUSTER_UNIT_CONFLICT',cid)
            self.cluster_units[cid]=r['unit']

    def _regions(self,filename):
        result=[]
        for cid,members in sorted(self.cluster_members.items()):
            os=[self.catalog.owners[k] for k in members]
            if os[0].file!=filename:continue
            require(all(o.file==filename and o.partition==os[0].partition and o.unit==self.cluster_units[cid] for o in os),
                    'FROZEN_CLUSTER_MEMBERSHIP_MISMATCH',cid)
            span=Span(min(o.observed_span.start for o in os),max(o.observed_span.end for o in os))
            # The exact frozen cluster/edge keys authorize the union; this is
            # consuming topology, not discovering owners or generating a graph.
            p=Proof('IM03_FROZEN_CLUSTER_UNION:'+cid,sha256(canonical_json(sorted(members))),
                    'UNION_OF_RETAINED_SOURCE_VIEWS; FROZEN_UNIT='+self.cluster_units[cid])
            result.append(ResponsibilityRegion(cid,self.cluster_units[cid],span,os[0].partition,p))
        return tuple(result)

    def _dependencies(self,f,layout,final_bytes):
        """Derive identity witnesses from actual final effects, not booleans.

        Absolute whole-file motion is normalized to the field origin. For a
        proved payload/secondary header the obsolete *branch-candidate* target
        is not a runtime dependency; the retained typed protection is instead.
        Unknown/contact views remain conservative when no typed view is known.
        """
        out=[];typed_preserve=f.state in (FieldState.PAYLOAD,FieldState.DISPOSITION)
        for key in f.dependency_ids:
            if key.startswith('A:'):
                x=int(key.rsplit(':',1)[1],16)
                if typed_preserve:
                    a=b={'retained_candidate_anchor':key,'semantic_use':'NOT_A_BRANCH_TARGET',
                         'typed_authority':f.proof.sha256}
                else:
                    a={'relative_anchor':x-f.source_span.start,'partition':f.partition}
                    b={'relative_anchor':layout.anchor(x)-layout.anchor(f.source_span.start),'partition':f.partition}
            elif key.startswith('CONTACT:'):
                owner=key[len('CONTACT:'):].removeprefix('O:')
                require(owner in self.catalog.owners,'UNKNOWN_CONTACT_OWNER_DEPENDENCY',owner)
                o=self.catalog.owners[owner]
                views=self.consumers_by_owner.get(owner,())
                spans=[p.source_span for c in views for p in c.ranges] or [o.observed_span]
                before=[];after=[]
                for s in spans:
                    t=layout.project(s)
                    before.append((s.start-f.source_span.start,s.size,sha256(layout.source[s.start:s.end])))
                    after.append((t.start-layout.anchor(f.source_span.start),t.size,sha256(final_bytes[t.start:t.end])))
                a={'owner':owner,'views':before};b={'owner':owner,'views':after}
            elif key.startswith('ROLE_POLICY:'):
                a=b={'field':f.field,'state':f.state.value,'authority':f.proof.sha256}
            else:raise ContractError('UNIMPLEMENTED_DEPENDENCY_KIND',key)
            out.append(DependencyIdentity(key,sha256(canonical_json(a)),sha256(canonical_json(b)),layout.mapping_proof))
        return tuple(out)

    def run_file(self,request:FileRequest) -> FileRun:
        file=request.file; require(file in self.expected_files,'UNKNOWN_EVENT_FILE',file)
        cat=self.catalog;owners=self.owners_by_file[file];fields=self.fields_by_file[file]
        session=RoleContractSession(cat,dict(self.engine.recipes));extra=[];ris=[];directives={};spans={};assembled=None;view_results=[]
        units=tuple(sorted(self.units_by_file[file]))
        def capture(op,ex):extra.append(blocked(op,ex.code,detail=str(ex)))
        def finish():
            return FileRun(file,request,assembled,tuple(session.attempts+extra),MappingProxyType(dict(spans)),
                           MappingProxyType(dict(session.prepared)),MappingProxyType(dict(directives)),
                           tuple(ris),tuple(view_results),units)
        try:
            request.source_identity.verify(file,request.source);g=Geometry.read(request.source)
            payloads=_unique(request.payloads,'owner','PAYLOAD_DIRECTIVE')
            actions=_unique(request.occurrence_actions,'id','OCCURRENCE_ACTION')
            approvals=_unique(request.dispositions,'field','FIELD_DISPOSITION')
            rules=_unique(request.field_rules,'field','REVIEWED_FIELD_RULE')
            interiors=_unique(request.interior_contracts,'owner','REVIEWED_INTERIOR_CONTRACT')
            if self.field_policy is not None:
                require(not rules,'ROLE_AWARE_FIELD_POLICY_FORBIDS_MANIFEST_FIELD_RULE_OVERRIDE',file)
            require(set(payloads)<=set(owners),'EXTRA_OR_CROSS_FILE_PAYLOAD_DIRECTIVE',file)
            allowed_occ={k for k,r in self.engine.catalog.occurrences.items() if r['owner'] in owners}
            require(set(actions)<=allowed_occ,'EXTRA_OR_CROSS_FILE_OCCURRENCE_ACTION',file)
            require(set(approvals)<=set(fields),'EXTRA_OR_CROSS_FILE_DISPOSITION',file)
            require(set(rules)<=set(fields),'EXTRA_OR_CROSS_FILE_FIELD_RULE',file)
            require(set(interiors)<=set(owners),'EXTRA_OR_CROSS_FILE_INTERIOR_CONTRACT',file)
            for key,ic in interiors.items():
                o=owners[key]
                require('H01' in o.holds and ic.recipe_id==o.recipe_id,
                        'REVIEWED_INTERIOR_CONTRACT_NOT_H01_OWNER',key)
                expected={f.field for f in fields.values() if ic.recipe_id in f.interior_recipe_ids}
                require(expected=={s.field for s in ic.slots} and bool(expected),
                        'H01_EXACT_FIELD_SET_MISMATCH',key)
        except ContractError as ex:capture('INPUT:'+file,ex);return finish()
        edits=[]
        for key,o in sorted(owners.items(),key=lambda kv:kv[1].observed_span.start):
            try:
                require(g.contains(o.partition,Span(o.observed_span.start,o.observed_span.start+4)),
                        'SOURCE_OWNER_PARTITION',key)
                require(request.source[o.observed_span.start:o.observed_span.start+4]==o.source_header,
                        'SOURCE_OWNER_HEADER',key)
                session.observe_source(key,request.source,g.offsets[o.partition+1])
                if not o.needs_upstream_recipe:
                    require(key not in payloads,'PRESERVATION_OWNER_CANNOT_ACCEPT_KO_PAYLOAD',key)
                    continue
                r=self.engine.recipes.get(key);sw=pw=None
                if r is not None:
                    require(r.source_asset=='stock:'+file,'RECIPE_SOURCE_ASSET_SCOPE',key)
                    require(r.source.span.end<=len(request.source),'RECIPE_SOURCE_RANGE',key)
                    sw=Window(r.source_asset,r.source.span,request.source[r.source.span.start:r.source.span.end])
                    if r.pc is not None and r.pc_asset in request.pc_assets:
                        raw=request.pc_assets[r.pc_asset]
                        require(r.pc.span.end<=len(raw),'RECIPE_PC_RANGE',key)
                        pw=Window(r.pc_asset,r.pc.span,raw[r.pc.span.start:r.pc.span.end])
                p=session.prepare_owner(key,sw,pw,interiors.get(key));ris.append(RecipeInput(key,sw,pw))
                if p.result.status!=Status.PREPARED:continue
                check=session.check_pretransform_payload(key,p.data)
                if check.status!=Status.SATISFIED:continue
                require(g.contains(o.partition,p.source_span),'EXACT_RECIPE_CROSSES_PARTITION',key)
                d=payloads.get(key,PayloadDirective(key,p.data_sha256,p.data,r.boundary_proof))
                require(d.prepared_sha256==p.data_sha256 and d.after[:4]==o.source_header,
                        'FINAL_PAYLOAD_PREIMAGE_OR_HEADER',key)
                # Changed payload bytes must come from an explicitly provisioned
                # reviewed materialization, not a guessed grammar transformation.
                for projection in d.projections:
                    require(isinstance(projection.authority,Proof) and projection.prepared_span.end<=len(p.data)
                            and projection.relative_span.end<=len(d.after),'PAYLOAD_PROJECTION_RANGE',key)
                directives[key]=d
                if key in interiors:
                    interiors[key].validate_directive(d.after,d.slots)
                    require(not d.points and not d.projections,
                            'H01_IDENTITY_PARENT_CANNOT_DECLARE_REMAP_OR_PROJECTION',key)
                if o.route==Route.DELEGATE:
                    require(not d.slots,'DELEGATE_CANNOT_OWN_FIELD_SLOT',key)
                    require(not d.points,'DELEGATE_CANNOT_DECLARE_UNUSED_SOURCE_MAP',key)
                    continue
                edits.append(PayloadEdit(key,p.source_span,d.after,o.partition,o.unit or key,o.unit,
                                         sha256(sw.data),d.authority,d.points,d.slots))
            except ContractError as ex:capture('OWNER:'+key,ex)
        if any(required_failure(r) for r in session.attempts+extra):
            for key in fields:extra.append(Result('FIELD:'+key,Status.NOT_OBSERVED,('SHAPE_BLOCKED_BY_REQUIRED_INPUT',)))
            return finish()
        try:layout=FinalLayout(file,request.source,request.source_identity,edits,self._regions(file))
        except ContractError as ex:capture('SHAPE:'+file,ex);return finish()
        # All field values are proposed before any dependency-identity result is
        # evaluated.  With the role-aware catalog, every retained field has
        # exactly one reviewed policy; final bytes are never reparsed to discover
        # a writer.
        writes=[];anchors={};policy_rules={};no_writer_entries={}
        for key,f in sorted(fields.items(),key=lambda kv:kv[1].source_span.start):
            try:
                interior=None
                if f.interior_recipe_ids:
                    matches=[ic for ic in interiors.values() if ic.recipe_id in f.interior_recipe_ids]
                    require(len(matches)==1,'H01_INTERIOR_ROLE_CONTRACT_NOT_DISCHARGED',key)
                    interior=matches[0]
                if self.field_policy is not None:
                    entry=self.field_policy.entry(key)
                    if not entry.has_field_writer:
                        require(interior is None,'NO_WRITER_POLICY_CANNOT_OWN_INTERIOR_SLOT',key)
                        no_writer_entries[key]=entry
                        continue
                    target=layout.anchor(f.source_target);start=layout.anchor(f.source_span.start)
                    g.locate(f.source_target,boundary_partition=f.partition)
                    anchors[key]=FinalFieldAnchors(key,f.source_span.start,f.source_target,start,target,start+4,
                                f.partition,f.partition,f.partition,f.unit,layout.mapping_proof)
                    rule=entry.reviewed_rule(f)
                    word=rule.propose(f,anchors[key],interior);mask=rule.mask();policy_rules[key]=rule
                    writes.append(FieldWrite(key,f.source_span,f.source_header,word,f.partition,f.unit,
                                  entry.proof,mask,entry.category.value))
                    continue

                # Compatibility path for the previous isolated IM03 fixtures.
                if f.interior_recipe_ids:
                    require(key in rules,'H01_REVIEWED_FIELD_RULE_REQUIRED',key)
                word=f.source_header;mask=0
                if f.state==FieldState.BRANCH04 or key in rules:
                    target=layout.anchor(f.source_target);start=layout.anchor(f.source_span.start)
                    g.locate(f.source_target,boundary_partition=f.partition)
                    span=target-start
                    anchors[key]=FinalFieldAnchors(key,f.source_span.start,f.source_target,start,target,start+4,
                                f.partition,f.partition,f.partition,f.unit,layout.mapping_proof)
                    if key in rules:
                        word=rules[key].propose(f,anchors[key],interior);mask=rules[key].mask()
                    else:
                        require(span%4==0 and 4<=span<=32764,'EVENT04_SPAN_UNREPRESENTABLE',key)
                        word=((int.from_bytes(word,'little')&0x0007ffff)|((span//4)<<19)).to_bytes(4,'little')
                        mask=0xfff80000
                writes.append(FieldWrite(key,f.source_span,f.source_header,word,f.partition,f.unit,f.proof,mask,
                              'TYPED_EVENT04_PROPOSAL' if f.state==FieldState.BRANCH04 else 'PRESERVATION_PROPOSAL'))
            except ContractError as ex:capture('FIELD:'+key,ex)
        if extra:return finish()
        try:trial=layout.assemble(writes)
        except ContractError as ex:capture('ASSEMBLY:'+file,ex);return finish()
        for w in writes:
            try:
                f=fields[w.field];deps=self._dependencies(f,layout,trial.data)
                proposal=FieldProposal(w.field,w.before,w.after,deps,anchors.get(w.field),approvals.get(w.field))
                if self.field_policy is not None:
                    matches=[ic for ic in interiors.values() if ic.recipe_id in f.interior_recipe_ids]
                    interior=matches[0] if len(matches)==1 else None
                    session.attempts.append(policy_rules[w.field].check(f,proposal,interior))
                elif w.field in rules:
                    matches=[ic for ic in interiors.values() if ic.recipe_id in f.interior_recipe_ids]
                    interior=matches[0] if len(matches)==1 else None
                    session.attempts.append(rules[w.field].check(f,proposal,interior))
                else:session.check_field(proposal)
            except ContractError as ex:capture('FIELD:'+w.field,ex)
        for key,entry in sorted(no_writer_entries.items(),key=lambda kv:fields[kv[0]].source_span.start):
            try:
                session.attempts.append(entry.check_no_writer(fields[key],layout,trial.data,approvals.get(key)))
            except ContractError as ex:capture('FIELD:'+key,ex)
        # Preserve every known view jointly. No alternate-view absence is inferred.
        for key,o in sorted(owners.items()):
            try:
                s=layout.placements.get(key)
                if s is None:s=layout.project(o.observed_span)
                require(layout.final_offsets[o.partition]<=s.start<s.end<=layout.final_offsets[o.partition+1],
                        'FINAL_OWNER_PARTITION',key)
                require(trial.data[s.start:s.start+4]==o.source_header,'FINAL_OWNER_HEADER',key)
                spans[key]=s
                contracts=self.consumers_by_owner.get(key,())
                if contracts:
                    samples={c.id:tuple(MappedWindow(r.id,r.source_span,layout.project(r.source_span),
                        trial.data[layout.anchor(r.source_span.start):layout.anchor(r.source_span.end)],layout.mapping_proof)
                        for r in c.ranges) for c in contracts}
                    view_results.append(session.check_established_views(key,samples))
                else:
                    extra.append(Result('VIEW_SCOPE:'+key,Status.SATISFIED,evidence=(o.binding,),
                        details={'claim':'FROZEN_RECIPE_OR_PRESERVATION_AND_HEADER_ONLY',
                                 'no_new_runtime_role_or_absence_claim':True}))
            except ContractError as ex:capture('FINAL_OWNER:'+key,ex)
        if any(required_failure(r) for r in session.attempts+extra):return finish()
        assembled=trial
        return finish()

    def run(self,requests:Iterable[FileRequest],*,run_id:str,roots:Iterable[RootInput]=()) -> IntegratedRun:
        requests=tuple(requests);roots=tuple(roots)
        require(len({r.file for r in requests})==len(requests),'DUPLICATE_FILE_REQUEST','')
        results=tuple(self.run_file(r) for r in requests)
        successful={r.file:r for r in results if r.local_complete}
        buffers={};errors=[]
        for file,r in successful.items():
            buffers['EVENT:'+file]=r.assembled.data;buffers['STOCK:'+file]=r.request.source
        root_inputs={}
        for r in roots:
            try:
                require(r.artifact=='TAI5MSG:FINAL' and r.artifact not in root_inputs,'ROOT_ARTIFACT_SCOPE_OR_DUPLICATE',r.artifact)
                r.identity.verify(r.artifact,r.data);buffers[r.artifact]=r.data;root_inputs[r.artifact]=r
            except ContractError as ex:errors.append(ex.code+':'+str(ex))
        if not buffers:
            return IntegratedRun(results,None,self.engine.verify(),tuple(errors),self.expected_files)
        candidate=Candidate(run_id,self.engine.catalog.fingerprint,buffers)
        def place(file,span,partition,unit,proof):
            art='EVENT:'+file
            return Placement(art,candidate.hashes[art],candidate.fingerprint,span,partition,unit,proof)
        views=[];inputs=[];occs=[];supp=[];regions=[];writers=[];rbs=[]
        for file,r in successful.items():
            a=r.assembled;l=a.layout;inputs.extend(r.recipe_inputs)
            for key,s in r.owner_spans.items():
                o=self.catalog.owners[key]
                mode={Route.DIRECT:'MEMBER_VIEW',Route.DELEGATE:'DELEGATED_VIEW',Route.PRESERVE:'PRESERVED_VIEW'}[o.route]
                views.append(OwnerView(key,place(file,s,o.partition,o.unit,l.mapping_proof),mode))
            for rr,s in l.final_regions:regions.append(UnitRegion(rr.unit,rr.cluster,place(file,s,rr.partition,rr.unit,l.mapping_proof)))
            for w in a.ownership:
                writers.append(WriterRange('EVENT:'+file,w.final_span,w.writer,w.unit,candidate.fingerprint))
            actions={x.id:x for x in r.request.occurrence_actions}
            cache={}
            def occurrence(oid,visiting=frozenset()):
                if oid in cache:return cache[oid]
                require(oid not in visiting,'BRIDGE_DELEGATION_CYCLE',oid)
                row=self.engine.catalog.occurrences[oid];key=row['owner'];o=self.catalog.owners[key]
                x=row['exact_occurrence'];pcspan=Span(x['escape_start'],x['literal_end'])
                child=self.engine.catalog.delegate_occurrences.get(oid)
                if child is not None:
                    require(oid not in actions,'DELEGATE_MUST_USE_FROZEN_CHILD_NOT_ACTION',oid)
                    sub=occurrence(child,visiting|{oid})
                    require(sub is not None,'DELEGATE_CHILD_NOT_PROVISIONED',oid)
                    p=sub.placement;action=Action.DELEGATE;rewrite=permit=None
                else:
                    actiondef=actions.get(oid)
                    if actiondef is None:return None
                    require(actiondef.action!=Action.DELEGATE,'UNAUTHORIZED_BRIDGE_DELEGATION',oid)
                    prepared=r.prepared[key];recipe=self.engine.recipes[key]
                    require(recipe.pc is not None,'OCCURRENCE_PC_RECIPE_REQUIRED',oid)
                    rel=Span(pcspan.start-recipe.pc.span.start,pcspan.end-recipe.pc.span.start)
                    proj=r.directives[key].project(rel,prepared.data)
                    owner_span=r.owner_spans[key]
                    target=Span(owner_span.start+proj.start,owner_span.start+proj.end)
                    require(target.end<=owner_span.end,'BRIDGE_OCCURRENCE_OUTSIDE_OWNER',oid)
                    p=place(file,target,o.partition,o.unit,l.mapping_proof)
                    action=actiondef.action;rewrite=actiondef.rewrite_id;permit=actiondef.preservation_permit
                sub=OccurrenceSubmission(oid,key,pcspan,p,action,rewrite,child,permit);cache[oid]=sub;return sub
            for oid,row in self.engine.catalog.occurrences.items():
                if self.catalog.owners[row['owner']].file!=file:continue
                try:occurrence(oid)
                except ContractError as ex:errors.append('OCC:'+oid+':'+ex.code)
            occs.extend(cache.values())
            for sid,row in self.engine.catalog.supports.items():
                srow=row['canonical_support'];key=srow['node_id'];o=self.catalog.owners[key]
                if o.file!=file:continue
                try:
                    src=Span(*srow['source_runtime_span']);s=l.project(src)
                    supp.append(SupportSubmission(sid,key,src,place(file,s,o.partition,row['unit'],l.mapping_proof)))
                except ContractError as ex:errors.append('SUP:'+sid+':'+ex.code)
        for art,r in root_inputs.items():
            for rid,b,local,s,p,proof in r.locators:
                rbs.append(RootBinding(rid,b,local,Placement(art,candidate.hashes[art],candidate.fingerprint,s,p,None,proof),proof))
        evidence=EvidenceBundle(candidate,tuple(views),tuple(inputs),tuple(occs),tuple(rbs),tuple(supp),tuple(regions),tuple(writers))
        return IntegratedRun(results,evidence,self.engine.verify(evidence),tuple(errors),self.expected_files)


def serialize_file(request:FileRequest,coordinator:IntegratedSerializer) -> FileRun:
    """Active replacement for the unsafe legacy (filename,source,owners,graph) API."""
    require(isinstance(request,FileRequest) and isinstance(coordinator,IntegratedSerializer),
            'TYPED_INTEGRATION_REQUEST_REQUIRED','Old NUL-based owner payloads are not accepted.')
    return coordinator.run_file(request)
