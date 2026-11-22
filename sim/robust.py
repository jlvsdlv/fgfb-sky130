import sys, json, itertools, numpy as np
from concurrent.futures import ThreadPoolExecutor
from lib import run
from rate import rate_from
T=80e-6
def job(kw):
    ms=kw.pop("ms", T/20000)
    d=run(kw.pop("vq"), 0.5, "Vdrv vd 0 0\nIin vd vmem 50n", T=T, maxstep=ms, ic=3.0, **kw)
    r,sw,a,b=rate_from(d)
    t=d[:,0]; m=t>T*0.3
    vavg=float(d[m,1].mean())
    return r, sw, vavg
which=sys.argv[1]; jobs=[]
VQS=[0.35,0.40,0.45,0.50,0.55]
if which=="ts":
    for ms in [T/10000, T/20000, T/40000]: jobs.append(dict(vq=0.45, ms=ms, tag=None))
elif which=="corner":
    for c in ["tt","ff","ss","fs","sf"]:
        for vq in VQS: jobs.append(dict(vq=vq, corner=c))
elif which=="temp":
    for tp in [-40, 85]:
        for vq in VQS: jobs.append(dict(vq=vq, temp=tp))
elif which=="mc":
    s0,s1=int(sys.argv[2]),int(sys.argv[3])
    for seed in range(s0,s1):
        for vq in VQS: jobs.append(dict(vq=vq, mc=1, seed=seed))
keys=[{k:v for k,v in j.items() if k!="tag"} for j in jobs]
for j in jobs: j.pop("tag",None)
with ThreadPoolExecutor(2) as ex: res=list(ex.map(job, [dict(j) for j in jobs]))
out=[]
for k,(r,sw,va) in zip(keys,res):
    k=dict(k); k.update(rate=r, swing=sw, vavg=va); out.append(k); print(k, flush=True)
json.dump(out, open(f"rob_{which}{'_'+sys.argv[2] if which=='mc' else ''}.json","w"))
