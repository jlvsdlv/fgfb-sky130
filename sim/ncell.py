from lib import PDK_LIB
import sys, json, time, subprocess, uuid, os, itertools, numpy as np
from concurrent.futures import ProcessPoolExecutor
from lock import spikes
def maxcut(n,E):
    best=0
    for s in itertools.product([0,1],repeat=n):
        best=max(best,sum(s[a]!=s[b] for a,b in E))
    return best
def job(p):
    t0=time.time(); tag="nc_"+uuid.uuid4().hex[:6]; n=p["n"]; E=p["E"]; f=p["f"]; per=1/f; T=p["T"]; dly=20e-6
    ref=f"PULSE(1.8 0 {dly} 20n 20n {p['w']} {per})"
    L=[f""".lib {PDK_LIB} tt
.param mc_mm_switch=0 mc_pr_switch=0
.include {p.get("cell","pex_cell.spice")}
Vvddh vddh 0 5
Vz z 0 0
Vg2 g2 0 0.5
VA ina 0 {ref}
VB inb 0 1.8"""]
    for i in range(n):
        ts=p["ts"][i]
        L.append(f"X{i} vddh vmem{i} fg{i} b{i} ina inb g2 z z z z z fgfbcell\nVQ{i} q{i} 0 {p['vq'][i]}\nRq{i} fg{i} q{i} 1e18\nI{i} 0 vmem{i} PWL(0 0 {ts} 0 {ts+10e-9} {p['iin']})")
    for k,(a,b) in enumerate(E):
        L.append(f"Cab{k} vmem{a} fg{b} {p['cc']}\nCba{k} vmem{b} fg{a} {p['cc']}")
    L.append(".ic "+" ".join(f"v(vmem{i})={p.get('ic',3.0)}" for i in range(n))+("".join(f" v(fg{i})={p['vq'][i]}" for i in range(n)) if p.get("fgic") else ""))
    L.append(f".control\nset wr_singlescale\ntran {p.get("ms",20e-9)} {T} 0 {p.get("ms",20e-9)}\nwrdata {tag}.out "+" ".join(f"v(vmem{i})" for i in range(n))+"\n.endc\n.end\n")
    open(tag+".sp","w").write("\n".join(L))
    subprocess.run(["ngspice","-b",tag+".sp"],capture_output=True,timeout=7000)
    d=np.loadtxt(tag+".out"); os.remove(tag+".sp"); os.remove(tag+".out")
    if p.get("save"): np.save(p["save"],d[::4])
    ph=[];R=[]
    for i in range(n):
        ts=spikes(d[:,[0,1+i]],T*0.6)
        if len(ts)<3: ph.append(float('nan')); R.append(0.0); continue
        z=np.exp(2j*np.pi*((ts-dly)%(2*per))/(2*per)).mean()
        ph.append(float(np.angle(z)/(2*np.pi)%1)); R.append(float(abs(z)))
    if any(np.isnan(ph)): return dict(name=p["name"],seed=p["seed"],cc=p["cc"],ph=ph,R=R,silent=[i for i in range(n) if np.isnan(ph[i])],sec=round(time.time()-t0))
    ref0=ph[0]; spin=[int(round(((x-ref0)%1)*2))%2 for x in ph]
    cut=sum(spin[a]!=spin[b] for a,b in E)
    return dict(name=p["name"],seed=p["seed"],cc=p["cc"],ph=[round(x,3) for x in ph],R=[round(x,3) for x in R],spin=spin,cut=cut,maxcut=maxcut(n,E),sec=round(time.time()-t0))
if __name__=="__main__":
    J=json.load(open(sys.argv[1])); out=[]
    with ProcessPoolExecutor(2) as ex:
        for o in ex.map(job,J): print(json.dumps(o),flush=True); out.append(o)
    json.dump(out,open(sys.argv[2],"w"))
