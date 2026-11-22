import numpy as np, json
from concurrent.futures import ThreadPoolExecutor
from lib import run
from syn import spikes
def job(vq):
    # 10 active-low presynaptic pulses (1 us, 100 kHz) between 30 and 130 us, then silence
    src="PWL(0 1.8 " + " ".join(f"{30e-6+k*10e-6:.9g} 1.8 {30e-6+k*10e-6+20e-9:.9g} 0 {31e-6+k*10e-6:.9g} 0 {31e-6+k*10e-6+20e-9:.9g} 1.8" for k in range(10)) + ")"
    d=run(vq,0.5,"Vdrv vd 0 0\nIin vd vmem 20n",srcA=src,T=330e-6,maxstep=4e-9,ic=3.0,tag=f"burst_{vq}")
    st=spikes(d)
    return vq, [round(x*1e6,1) for x in st]
with ThreadPoolExecutor(2) as ex:
    for vq,st in ex.map(job,[0.450,0.454]): print(vq, "spike times (us):", st, flush=True)
