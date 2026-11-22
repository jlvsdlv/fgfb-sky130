import sys, json, numpy as np
from concurrent.futures import ThreadPoolExecutor
from lib import run
def spikes(d, drop=0.4):
    t,v=d[:,0],d[:,1]; k=[]; j=0
    for i in range(1,len(t)):
        while t[i]-t[j]>1.5e-6: j+=1
        if v[j:i+1].max()-v[i]>drop and (not k or t[i]-k[-1]>3e-6): k.append(t[i])
    return np.array(k)
def job(p):
    vq,iin,amp,w,per,T=p["vq"],p["iin"],p["amp"],p["w"],p["per"],p.get("T",200e-6)
    if amp>0: src=f"PULSE(0 {amp} 30u 20n 20n {w} {per})"
    elif amp<0: src=f"PULSE({-amp} 0 30u 20n 20n {w} {per})"
    else: src="0"
    d=run(vq,0.5,f"Vdrv vd 0 0\nIin vd vmem {iin}",srcA=src,T=T,maxstep=4e-9,ic=3.0,tag=p.get("tag"))
    st=spikes(d); st=st[st>30e-6]
    return dict(p, n=int(len(st)), rate=len(st)/(T-30e-6), vmin=float(d[d[:,0]>30e-6,1].min()), vmax=float(d[:,1].max()))
if __name__=="__main__":
    jobs=json.loads(sys.argv[1]); 
    with ThreadPoolExecutor(2) as ex: out=list(ex.map(job,jobs))
    for o in out: print(json.dumps({k:(float("%.4g"%v) if isinstance(v,float) else v) for k,v in o.items() if k!='tag'}), flush=True)
    if len(sys.argv)>2: json.dump(out,open(sys.argv[2],"w"))
