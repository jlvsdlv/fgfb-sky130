import sys, json, time, numpy as np
from concurrent.futures import ProcessPoolExecutor
from lib import run
def spikes(d,t0):
    t,v=d[:,0],d[:,1]; m=t>t0; t,v=t[m],v[m]
    if v.max()-v.min()<0.4: return np.array([])
    mid=(v.max()+v.min())/2; k=np.where((v[:-1]>mid)&(v[1:]<=mid))[0]
    return t[k]+(mid-v[k])/(v[k+1]-v[k])*(t[k+1]-t[k])
def job(p):
    t0=time.time(); f=p["f"]; per=1/f if f>0 else 1; T=p.get("T",1e-3)
    src=f"PULSE(1.8 {1.8-p.get('amp',1.8):.3f} {p.get('dly',20e-6)} 20n 20n {p['w']} {per})" if f>0 else "1.8"
    d=run(p["vq"],p.get("vg2",0.5),f"Vdrv vd 0 0\nIin vd vmem {p['iin']}",srcA=src,T=T,maxstep=p.get("ms",20e-9),ic=p.get("ic",3.0),extra=p.get("extra",""))
    ts=spikes(d,T*0.4); r=(len(ts)-1)/(ts[-1]-ts[0]) if len(ts)>2 else 0
    out=dict(p,rate=r,n=len(ts),sec=round(time.time()-t0))
    if f>0 and len(ts)>2:
        ph=((ts-p.get('dly',20e-6))%(2*per))/(2*per)   # phase within two reference periods
        z=np.exp(2j*np.pi*ph); out["phase"]=float(np.angle(z.mean())/(2*np.pi)%1); out["R"]=float(abs(z.mean()))
    if p.get("save"): np.save(p["save"],d[::4])
    return out
if __name__=="__main__":
    J=json.load(open(sys.argv[1])); out=[]
    with ProcessPoolExecutor(2) as ex:
        for o in ex.map(job,J): print(json.dumps(o),flush=True); out.append(o)
    json.dump(out,open(sys.argv[2],"w"))
