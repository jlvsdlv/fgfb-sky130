import json
from concurrent.futures import ThreadPoolExecutor
from lib import run
from rate import rate_from
jobs=[(0.6,0.55),(0.7,0.55),(0.7,0.65),(0.6,0.65)]
def job(j):
    vg2,vq=j; d=run(vq,vg2,"Vdrv vd 0 0\nIin vd vmem 50n",T=80e-6,maxstep=4e-9,ic=3.0,corner="ss")
    r,sw,_,_=rate_from(d); return dict(label="ss",vg2=vg2,vq=vq,iin=50e-9,rate=r,swing=sw)
with ThreadPoolExecutor(2) as ex: out=list(ex.map(job,jobs))
for o in out: print(o)
json.dump(out,open("vg2_ss.json","w"))
