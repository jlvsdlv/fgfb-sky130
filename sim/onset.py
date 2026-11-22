import sys, json, numpy as np, time
from concurrent.futures import ThreadPoolExecutor
from lib import run
def rate(d, t0):
    t,v=d[:,0],d[:,1]; m=t>t0; tt,vv=t[m],v[m]; sw=vv.max()-vv.min()
    if sw<0.4: return 0.0, sw
    mid=(vv.max()+vv.min())/2; k=np.where((vv[:-1]<mid)&(vv[1:]>=mid))[0]
    if len(k)<3: return 0.0, sw
    tc=tt[k]+(mid-vv[k])/(vv[k+1]-vv[k])*(tt[k+1]-tt[k]); return (len(tc)-1)/(tc[-1]-tc[0]), sw
def job(p):
    t0=time.time(); T=p.get("T",2e-3); ms=p.get("ms",20e-9)
    src=p.get("src","1.8")
    d=run(p["vq"],p.get("vg2",0.5),f"Vdrv vd 0 0\nIin vd vmem {p['iin']}",srcA=src,T=T,maxstep=ms,ic=3.0)
    r,sw=rate(d,T*0.25); return dict({k:v for k,v in p.items() if k!="src"}, rate=r, swing=sw, sec=round(time.time()-t0))
if __name__=="__main__":
    jobs=json.loads(open(sys.argv[1]).read())
    with ThreadPoolExecutor(2) as ex:
        out=[]
        for o in ex.map(job,jobs): print(json.dumps(o), flush=True); out.append(o)
    json.dump(out,open(sys.argv[2],"w"))
