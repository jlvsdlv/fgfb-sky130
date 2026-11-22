"""Pazos-style pulsed synaptic test on the extracted cell: potentiation pulses on the drain
(membrane node) with low-voltage reads in between, then a long read to watch the decay."""
import sys, json, numpy as np, lib
from concurrent.futures import ProcessPoolExecutor
def wave(vpot, tp, tr, npot, Vr, tail, gaps=None, ef=20e-9):
    t=0; pts=[(0,Vr)]; marks=[]; e=20e-9
    t=20e-6; marks.append(("read0",t-10e-6,t-1e-6))
    gaps=gaps or [tr]*npot
    for k in range(npot):
        pts+=[(t,Vr),(t+e,vpot),(t+e+tp,vpot),(t+e+tp+ef,Vr)]; t+=e+tp+ef
        marks.append((f"r{k+1}",t+gaps[k]*0.3,t+gaps[k]*0.9)); t+=gaps[k]
    t_end=t+tail; pts.append((t_end,Vr))
    return "PWL("+" ".join(f"{a:.9g} {b}" for a,b in pts)+")", marks, t_end
def job(p):
    src,marks,T=wave(p["vpot"],p["tp"],p["tr"],p["npot"],p["vr"],p["tail"],p.get("gaps"),p.get("ef",20e-9))
    d=lib.run(p["vq"],p["vg2"],f"Vdrv vmem 0 {src}",srcA="1.8",T=T,maxstep=p.get("ms",10e-9),ic=p["vr"])
    t,I,vb=d[:,0],-d[:,2],d[:,4]
    reads={n:float(np.mean(I[(t>a)&(t<b)])) for n,a,b in marks}
    tail_t=t[t>marks[-1][2]]-marks[-1][2]; tail_I=I[t>marks[-1][2]]
    dec={f"{x*1e6:.0f}us":float(np.interp(x,tail_t,tail_I)) for x in [1e-6,10e-6,50e-6,200e-6,500e-6] if x<tail_t[-1]}
    np.save(f"STP_{p['tag']}.npy",d[::5])
    return dict(p,reads=reads,decay=dec,vbmax=float(vb.max()))
if __name__=="__main__":
    J=json.load(open(sys.argv[1])); out=[]
    with ProcessPoolExecutor(2) as ex:
        for o in ex.map(job,J): print(json.dumps(o),flush=True); out.append(o)
    json.dump(out,open(sys.argv[2],"w"))
