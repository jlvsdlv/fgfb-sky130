import sys, json, numpy as np
from lib import run
from rate import rate_from
vq=float(sys.argv[1]); pts=[float(x) for x in sys.argv[2:]]
for iin in pts:
    T=max(80e-6, 80e-6*50e-9/iin)
    d=run(vq, 0.5, f"Vdrv vd 0 0\nIin vd vmem {iin}", T=T, maxstep=T/20000, ic=3.0, tag=f"IF_{vq}_{iin:g}")
    r,sw,a,b=rate_from(d); print(f"VQ={vq} Iin={iin*1e9:.0f} nA: {r/1e3:.1f} kHz swing {sw:.2f}", flush=True)
