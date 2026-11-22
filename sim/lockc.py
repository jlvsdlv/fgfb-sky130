import sys, json, lib
lib.HDR=lib.HDR.replace("pex_flat.spice","pexc_flat.spice"); lib.FGIC=True
import lock
from concurrent.futures import ProcessPoolExecutor
if __name__=="__main__":
    J=json.load(open(sys.argv[1])); out=[]
    with ProcessPoolExecutor(2) as ex:
        for o in ex.map(lock.job,J): print(json.dumps(o),flush=True); out.append(o)
    json.dump(out,open(sys.argv[2],"w"))
