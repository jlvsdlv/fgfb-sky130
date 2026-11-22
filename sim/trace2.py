import sys, numpy as np
from concurrent.futures import ThreadPoolExecutor
from lib import run
def j(i):
    d=run(0.40,0.4,f"Vdrv vd 0 0\nIin vd vmem {i}",srcA="1.8",T=1.5e-3,maxstep=20e-9,ic=3.0)
    np.save(f"TR_{i}.npy",d[::5]); return i
with ThreadPoolExecutor(2) as ex: print(list(ex.map(j,["8n","8.5n"])))
