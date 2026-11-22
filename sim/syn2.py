import sys, json, numpy as np
from concurrent.futures import ThreadPoolExecutor
from lib import run
T0, T = 0.2e-3, 1.0e-3
def rate_cross(d):
    t,v=d[:,0],d[:,1]; m=t>T0; tt,vv=t[m],v[m]
    sw=vv.max()-vv.min()
    if sw<0.4: return 0.0, sw
    mid=(vv.max()+vv.min())/2
    k=np.where((vv[:-1]<mid)&(vv[1:]>=mid))[0]
    if len(k)<3: return 0.0, sw
    tc=tt[k]+(mid-vv[k])/(vv[k+1]-vv[k])*(tt[k+1]-tt[k])
    return (len(tc)-1)/(tc[-1]-tc[0]), sw
def job(p):
    vq,iin,f,w=p["vq"],p["iin"],p["f"],p["w"]
    src="0" if f==0 else f"PULSE(1.8 0 {T0/2} 20n 20n {w} {1/f})"
    if f==0: src="1.8"
    d=run(vq,0.5,f"Vdrv vd 0 0\nIin vd vmem {iin}",srcA=src,T=T,maxstep=5e-9,ic=3.0)
    r,sw=rate_cross(d); return dict(p, rate=r, swing=sw)
if __name__=="__main__":
    jobs=json.loads(sys.argv[1])
    with ThreadPoolExecutor(2) as ex:
        for o in ex.map(job,jobs): print(json.dumps(o), flush=True)
