import sys, json, time, numpy as np, lib
from concurrent.futures import ThreadPoolExecutor
from onset import rate
S={150:8.49,100:6.93,60:5.37,40:4.38,20:3.09}
base=open("pex_flat.spice").read()
for c,s in S.items():
    open(f"pex_cm{c}.spice","w").write(base.replace("sky130_fd_pr__cap_mim_m3_1 l=10 w=10",f"sky130_fd_pr__cap_mim_m3_1 l={s} w={s}"))
H0=lib.HDR
def job(p):
    t0=time.time(); c=p["c"]
    # thread-safe: pass header via replace inside run
    hdr=H0.replace("pex_flat.spice",f"pex_cm{c}.spice")
    lib.HDR=hdr
    d=lib.run(p["vq"],p.get("vg2",0.5),f"Vdrv vd 0 0\nIin vd vmem {p['iin']}",srcA="1.8",T=p["T"],maxstep=p["ms"],ic=3.0,tag=f"CM_{c}_{p['iin']}")
    r,sw=rate(d,p["T"]*0.3); m=d[:,0]>p["T"]*0.3
    return dict(p,rate=r,swing=sw,vmin=float(d[m,1].min()),vmax=float(d[m,1].max()),sec=round(time.time()-t0))
if __name__=="__main__":
    J=json.load(open(sys.argv[1])); out=[]
    with ThreadPoolExecutor(1) as ex:
        for o in ex.map(job,J): print(json.dumps(o),flush=True); out.append(o)
    json.dump(out,open(sys.argv[2],"w"))
