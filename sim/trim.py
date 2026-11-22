import json, numpy as np
from concurrent.futures import ThreadPoolExecutor
from lib import run
from rate import rate_from
T=80e-6
grid={"ff":[0.25,0.30,0.33,0.37],"sf":[0.15,0.20,0.25,0.30],"ss":[0.60,0.65,0.70,0.75],"fs":[0.60,0.65,0.70,0.75]}
jobs=[(c,q) for c,qs in grid.items() for q in qs]
def job(cq):
    c,q=cq; d=run(q,0.5,"Vdrv vd 0 0\nIin vd vmem 50n",T=T,maxstep=T/20000,ic=3.0,corner=c)
    r,sw,_,_=rate_from(d); return dict(corner=c,vq=q,rate=r,swing=sw)
with ThreadPoolExecutor(2) as ex: out=list(ex.map(job,jobs))
for o in out: print(o, flush=True)
json.dump(out,open("trim_corner.json","w"))
