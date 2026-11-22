import sys, json, time, numpy as np
from concurrent.futures import ProcessPoolExecutor
import lib
from lock import spikes
def pwl(rate, amp, w, T, seed, tr=20e-9, dead=None):
    r=np.random.default_rng(seed); t=5e-6; pts=[(0,1.8)]; dead=dead or (w+0.2e-6)
    lo=1.8-amp
    while True:
        t+=dead+r.exponential(1/rate)
        if t+w>T: break
        pts+= [(t,1.8),(t+tr,lo),(t+tr+w,lo),(t+2*tr+w,1.8)]
    s="PWL("+" ".join(f"{a:.9g} {b:.4g}" for a,b in pts)+")"
    # wrap long line
    out=[];line=""
    for tok in s.split(" "):
        if len(line)>200: out.append(line); line="+ "
        line+=tok+" "
    out.append(line); return "\n".join(out), (len(pts)-1)//4
def job(p):
    t0=time.time(); T=p.get("T",1e-3)
    if p.get("lib")=="c": lib.HDR=lib.HDR.replace("pex_flat.spice","pexc_flat.spice"); lib.FGIC=True
    if p.get("net"): lib.HDR=lib.HDR.replace("pex_flat.spice",p["net"]); lib.FGIC=True
    src,n=pwl(p["rate"],p["amp"],p["w"],T,p["seed"]) if p["rate"]>0 else ("1.8",0)
    rb=p.get("rateB",0)
    srcB,nb=pwl(rb,p.get("ampB",p["amp"]),p["w"],T,p["seed"]+1000) if rb>0 else ("1.8",0)
    d=lib.run(p["vq"],p.get("vg2",0.5),f"Vdrv vd 0 0\nIin vd vmem {p['iin']}",srcA=src,srcB=srcB,T=T,maxstep=p.get("ms",20e-9),ic=p.get("ic",3.0))
    ts=spikes(d,0.1e-3)
    return dict(p,nin=n,rin=n/T,ninB=nb,rinB=nb/T,nout=len(ts),rout=len(ts)/(T-0.1e-3),sec=round(time.time()-t0))
if __name__=="__main__":
    J=json.load(open(sys.argv[1])); out=[]
    with ProcessPoolExecutor(2) as ex:
        for o in ex.map(job,J): print(json.dumps(o),flush=True); out.append(o)
    json.dump(out,open(sys.argv[2],"w"))
