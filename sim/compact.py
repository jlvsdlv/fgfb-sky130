import sys, json, time, numpy as np, lib
from concurrent.futures import ProcessPoolExecutor
from onset import rate
lib.HDR=lib.HDR.replace("pex_flat.spice","pexc_flat.spice"); lib.FGIC=True
def job(p):
    t0=time.time()
    d=lib.run(p["vq"],p.get("vg2",0.5),f"Vdrv vd 0 0\nIin vd vmem {p['iin']}",srcA="1.8",T=p["T"],maxstep=p["ms"],ic=p.get("ic",3.0))
    r,sw=rate(d,p["T"]*0.3); m=d[:,0]>p["T"]*0.3
    return dict(p,rate=r,swing=sw,vmin=float(d[m,1].min()),vmax=float(d[m,1].max()),sec=round(time.time()-t0))
if __name__=="__main__":
    J=json.load(open(sys.argv[1])); out=[]
    with ProcessPoolExecutor(2) as ex:
        for o in ex.map(job,J): print(json.dumps(o),flush=True); out.append(o)
    json.dump(out,open(sys.argv[2],"w"))
