import sys, json
from lib import run, ramp_drive, loop
vq=float(sys.argv[1]); out=[]
for vg2 in [0.3, 0.4, 0.5, 0.6]:
    tr=2e-3
    d=run(vq, vg2, ramp_drive(tr), T=2*tr, maxstep=tr/2000)
    L=loop(d,tr); L.update(vq=vq, vg2=vg2); out.append(L)
    print(f"VQ={vq} VG2={vg2}: area {L['area']*1e6:.3f} uA*V, max ratio {L['ratio']:.1f} at {L['at']:.2f} V (low {L['ilow']*1e6:.3f}, high {L['ihigh']*1e6:.3f} uA), trig {L['vtrig']:.2f} rel {L['vrel']:.2f}", flush=True)
json.dump(out, open(f"map_{vq}.json","w"))
