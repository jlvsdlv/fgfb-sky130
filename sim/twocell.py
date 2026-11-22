from lib import PDK_LIB
import sys, json, time, subprocess, uuid, os, numpy as np
from concurrent.futures import ProcessPoolExecutor
from lock import spikes
def job(p):
    t0=time.time(); tag="tc_"+uuid.uuid4().hex[:6]; f=p["f"]; per=1/f; T=p.get("T",0.6e-3); dly=20e-6
    ref=f"PULSE(1.8 0 {dly} 20n 20n {p['w']} {per})"
    cc=p["cc"]; sign=p.get("sign","dir")
    if cc==0: coup=""
    elif sign=="dir":   # vmem_j -> fg_i through a capacitor
        coup=f"Cc12 vmem1 fg2 {cc}\nCc21 vmem2 fg1 {cc}\n"
    else:               # through an ideal inverting unity buffer (test-bench only)
        coup=f"E1 vm1n 0 vmem1 0 -1\nE2 vm2n 0 vmem2 0 -1\nCc12 vm1n fg2 {cc}\nCc21 vm2n fg1 {cc}\n"
    net=f""".lib {PDK_LIB} tt
.param mc_mm_switch=0 mc_pr_switch=0
.include pex_cell.spice
Vvddh vddh 0 5
Vz z 0 0
Vg2 g2 0 0.5
X1 vddh vmem1 fg1 b1 ina1 inb1 g2 z z z z z fgfbcell
X2 vddh vmem2 fg2 b2 ina2 inb2 g2 z z z z z fgfbcell
VQ1 q1 0 {p['vq1']}
Rq1 fg1 q1 1e18
VQ2 q2 0 {p['vq2']}
Rq2 fg2 q2 1e18
VA1 ina1 0 {ref if f>0 else 1.8}
VA2 ina2 0 {ref if f>0 else 1.8}
VB1 inb1 0 1.8
VB2 inb2 0 1.8
I1 0 vmem1 {p['iin']}
I2 0 vmem2 PWL(0 0 {p['ts']} 0 {p['ts']+10e-9} {p['iin']})
{coup}
.ic v(vmem1)=3.0 v(vmem2)=3.0
.control
set wr_singlescale
tran 20n {T} 0 20n
wrdata {tag}.out v(vmem1) v(vmem2)
.endc
.end
"""
    open(tag+".sp","w").write(net)
    subprocess.run(["ngspice","-b",tag+".sp"],capture_output=True,timeout=3000)
    d=np.loadtxt(tag+".out"); os.remove(tag+".sp"); os.remove(tag+".out")
    out=dict(p,sec=round(time.time()-t0))
    for k,col in [(1,1),(2,2)]:
        ts=spikes(d[:,[0,col]],T*0.5); out[f"rate{k}"]=(len(ts)-1)/(ts[-1]-ts[0]) if len(ts)>2 else 0
        if f>0 and len(ts)>2:
            z=np.exp(2j*np.pi*((ts-dly)%(2*per))/(2*per)).mean(); out[f"ph{k}"]=float(np.angle(z)/(2*np.pi)%1); out[f"R{k}"]=float(abs(z))
    if "ph1" in out and "ph2" in out: out["dph"]=round((out["ph2"]-out["ph1"])%1,3)
    if p.get("save"): np.save(p["save"],d[::2])
    return out
if __name__=="__main__":
    J=json.load(open(sys.argv[1])); out=[]
    with ProcessPoolExecutor(2) as ex:
        for o in ex.map(job,J):
            print(json.dumps({k:(round(v,4) if isinstance(v,float) else v) for k,v in o.items()}),flush=True); out.append(o)
    json.dump(out,open(sys.argv[2],"w"))
