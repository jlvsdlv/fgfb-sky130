import sys, json, time, numpy as np
from lib import run
vq=float(sys.argv[1]); out=[]
def spikes(t, v, T):
    pk=np.where((v[1:-1]>=v[:-2])&(v[1:-1]>v[2:]))[0]+1
    return np.array([t[i] for i in pk if v[i]-v[i:min(len(v),i+400)].min()>0.25])
for iin in [10e-9, 25e-9, 50e-9, 100e-9, 150e-9]:
    T=max(80e-6, 80e-6*50e-9/iin)
    t0=time.time()
    d=run(vq, 0.5, f"Vdrv vd 0 0\nIin vd vmem {iin}", T=T, maxstep=T/20000, ic=3.0, tag=f"IF_{vq}_{iin:g}")
    t,v=d[:,0],d[:,1]; sp=spikes(t,v,T); s2=sp[sp>T*0.3]; m=t>T*0.3
    r=float(1/np.median(np.diff(s2))) if len(s2)>2 else 0.0
    o=dict(vq=vq,iin=iin,rate=r,vmax=float(v[m].max()),vmin=float(v[m].min()))
    out.append(o); print(o, f"{time.time()-t0:.0f}s", flush=True)
json.dump(out, open(f"if_{vq}.json","w"))
