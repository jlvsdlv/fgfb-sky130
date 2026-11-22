import json
from concurrent.futures import ThreadPoolExecutor
from lib import run
from rate import rate_from
jobs=[]
for lbl,kw in [("fs",dict(corner="fs")),("-40 °C",dict(temp=-40))]:
    for vg2 in [0.6,0.7]:
        for vq in [0.45,0.55]:
            for iin in [20e-9,50e-9]: jobs.append((lbl,kw,vg2,vq,iin))
def job(j):
    lbl,kw,vg2,vq,iin=j; T=max(80e-6,80e-6*50e-9/iin)
    d=run(vq,vg2,f"Vdrv vd 0 0\nIin vd vmem {iin}",T=T,maxstep=T/20000,ic=3.0,**kw)
    r,sw,_,_=rate_from(d); return dict(label=lbl,vg2=vg2,vq=vq,iin=iin,rate=r,swing=sw)
with ThreadPoolExecutor(2) as ex: out=list(ex.map(job,jobs))
for o in out: print(o)
json.dump(out,open("vg2_trim.json","w"))
