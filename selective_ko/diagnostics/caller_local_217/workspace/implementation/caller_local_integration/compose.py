"""Compose new edits with an exact, already-authorized existing directive."""
from caller_local import Result,Rejected,require
from builder.selective_event_particle import PARTICLE_REPLACEMENTS,transform_particle_command,_message_ranges

def compose(changed,old):
    before=changed.before
    if old.after==before:return changed,[]
    require(not old.points and not old.slots,'EXISTING_POSITIONAL_CONTRACT_REQUIRES_EXPLICIT_COMPOSITION')
    edits=[]
    if old.authority.document=='V344_FIXED_SURFACE_PARTICLE':
        expected,_=transform_particle_command(before)
        require(expected==old.after,'CANONICAL_PARTICLE_OUTPUT_MISMATCH')
        for pattern,replacement,name in PARTICLE_REPLACEMENTS:
            for start,end in _message_ranges(before):
                pos=start
                while True:
                    a=before.find(pattern,pos,end)
                    if a<0:break
                    edits.append((a,a+len(pattern),replacement));pos=a+1
    elif old.authority.document=='LEGACY_OVERLAY_CONNECTION':
        require(len(before)==len(old.after),'UNSUPPORTED_LENGTH_CHANGING_LEGACY_COMPOSITION')
        # Coordinates are identical by this explicitly restricted same-length case.
        # Copy existing authorized differences verbatim; do not infer a new transformation.
        pos=0
        while pos<len(before):
            if before[pos]==old.after[pos]:pos+=1;continue
            start=pos
            while pos<len(before) and before[pos]!=old.after[pos]:pos+=1
            edits.append((start,pos,old.after[start:pos]))
    else:raise Rejected('UNSUPPORTED_EXISTING_TRANSFORM')
    edits.sort();require(all(4<=a<z<changed.content_end for a,z,_ in edits),'EXISTING_EDIT_OUTSIDE_TEXT')
    def splice(es,align):
        chunks=[];last=0
        for a,z,new in es:chunks.extend((before[last:a],new));last=z
        chunks.append(before[last:changed.content_end] if align else before[last:])
        data=b''.join(chunks)
        return data+b'\0'*((-len(data))%4) if align else data
    require(splice(edits,False)==old.after,'EXISTING_EDIT_RECONSTRUCTION')
    combined=sorted((*edits,*changed.edits))
    require(all(combined[i][1]<=combined[i+1][0] for i in range(len(combined)-1)),'EXISTING_AND_NEW_EDIT_OVERLAP')
    final=splice(combined,True)
    return Result(changed.owner,before,final,tuple(combined),changed.content_end),edits
