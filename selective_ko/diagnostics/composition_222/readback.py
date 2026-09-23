"""Independent byte-indexed storage reader; does not import the writer or canonical parser."""
import hashlib

def decode(blob,counts,last_lengths):
    if len(counts)!=33 or len(last_lengths)!=33:raise ValueError('reader profile')
    pairs=[]
    for b in range(33):
        h=8*b;off=int.from_bytes(blob[h:h+4],'little');size=int.from_bytes(blob[h+4:h+8],'little')
        if off%64 or size%64 or size>131072:raise ValueError('header alignment/capacity')
        pairs.append((off,size))
    if pairs[0][0]!=320:raise ValueError('header extent')
    out=[];meta=[]
    for b,(off,size) in enumerate(pairs):
        end=pairs[b+1][0] if b<32 else len(blob)
        if b<32 and off+size!=end:raise ValueError('noncontiguous block')
        if not off<end<=off+size:raise ValueError('physical extent')
        # Translation table is independent of the writer's per-byte arithmetic.
        plain=blob[off:end].translate(bytes(list(range(91,256))+list(range(91))))
        n=int.from_bytes(plain[:2],'little')
        if n!=counts[b]:raise ValueError('message count')
        starts=[int.from_bytes(plain[2+4*i:6+4*i],'little') for i in range(n)]
        if not starts or starts[0]!=2+4*n:raise ValueError('first message offset')
        if any(a>=c for a,c in zip(starts,starts[1:])):raise ValueError('nonmonotonic offsets')
        used=starts[-1]+last_lengths[b]
        if used>len(plain) or used<=starts[-1]:raise ValueError('final extent')
        if any(c!=91 for c in plain[used:]):raise ValueError('unexpected padding')
        stops=starts[1:]+[used]
        if any(not 2+4*n<=a<c<=used for a,c in zip(starts,stops)):raise ValueError('message extent')
        rows=[plain[a:c] for a,c in zip(starts,stops)];out.append(rows)
        meta.append({'block':b,'offset':off,'declared':size,'physical':end-off,'messages':n,'used':used,'omitted':size-(end-off)})
    return out,meta

def verify(baseline,candidate,contract,plan):
    original,_=decode(baseline,contract['baseline_counts'],contract['base_last_lengths'])
    counts=list(contract['baseline_counts']);counts[0]=511
    last=list(contract['base_last_lengths']);last[0]=len(bytes.fromhex(plan['B0:510']))
    actual,meta=decode(candidate,counts,last)
    if candidate[264:320]!=baseline[264:320]:raise ValueError('reserved header changed')
    changed=preserved=added=0;ledger=[]
    for b,rows in enumerate(actual):
        for m,value in enumerate(rows):
            key=f'B{b}:{m}'
            expected=bytes.fromhex(plan[key]) if key in plan else original[b][m]
            if value!=expected:raise ValueError('payload mismatch '+key)
            if m>=len(original[b]):added+=1;role='ADDED_HELPER'
            elif value!=original[b][m]:changed+=1;role='CHANGED_ORIGINAL'
            else:preserved+=1;role='PRESERVED_ORIGINAL'
            ledger.append({'locator':key,'role':role,'size':len(value),'sha256':hashlib.sha256(value).hexdigest()})
    if (changed,added,preserved)!=(18,40,14814):raise ValueError('accounting')
    if actual[0][:471]!=original[0]:raise ValueError('original B0 change')
    if meta[32]['omitted']!=55:raise ValueError('B32 physical contract')
    return {'checked_records':len(ledger),'changed_original':changed,'preserved_original':preserved,'appended_helpers':added,'blocks':meta,'ledger':ledger}
