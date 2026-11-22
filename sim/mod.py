import numpy as np
from lib import run
from rate import rate_from
A="PULSE(0 1.8 60u 0.2u 0.2u 50u 1)"; B="PULSE(1.8 0 140u 0.2u 0.2u 50u 1)"
d=run(0.45, 0.5, "Vdrv vd 0 0\nIin vd vmem 50n", srcA=A, srcB=B, T=200e-6, maxstep=10e-9, ic=3.0, tag="MOD")
t=d[:,0]
for a,b,lab in [(20e-6,60e-6,"base"),(60e-6,110e-6,"A +1.8"),(110e-6,140e-6,"base"),(140e-6,190e-6,"B -1.8")]:
    m=(t>a+5e-6)&(t<b); r,sw,_,_=rate_from(d[m],frac=0.0); print(lab, f"{r/1e3:.1f} kHz swing {sw:.2f}", flush=True)
