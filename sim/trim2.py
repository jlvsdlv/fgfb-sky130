import json, numpy as np
from concurrent.futures import ThreadPoolExecutor
from lib import run
from rate import rate_from
jobs=[]
for c in ["ss","fs"]:
    for q in [0.55,0.65,0.75]:
        for i in [20e-9,100e-9,200e-9]: jobs.append(dict(corner=c,vq=q,iin=i))
for q in [0.60,0.65,0.70]: jobs.append(dict(temp=-40,vq=q,iin=50e-9))
for q in [0.25,0.30]: jobs.append(dict(temp=85,vq=q,iin=50e-9))
def job(j):
    j=dict(j); iin=j.pop("iin"); q=j.pop("vq"); T=max(80e-6,80e-6*50e-9/iin)
    d=run(q,0.5,f"Vdrv vd 0 0\nIin vd vmem {iin}",T=T,maxstep=T/20000,ic=3.0,**j)
    r,sw,_,_=rate_from(d); return r,sw
with ThreadPoolExecutor(2) as ex: res=list(ex.map(job,jobs))
out=[]
for j,(r,sw) in zip(jobs,res):
    j=dict(j); j.update(rate=r,swing=sw); out.append(j); print(j, flush=True)
json.dump(out,open("trim2.json","w"))
