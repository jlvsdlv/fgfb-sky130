import sys
from lib import run, ramp_drive, loop
which=sys.argv[1]
if which=="rate":
    for tr in [200e-6, 20e-3]:
        d=run(0.5, 0.5, ramp_drive(tr), T=2*tr, maxstep=tr/2000, tag=f"L_rate_{tr:g}")
        L=loop(d,tr); print(f"ramp {tr*1e6:.0f} us: area {L['area']*1e6:.3f}, trig {L['vtrig']:.2f}, rel {L['vrel']:.2f}", flush=True)
else:
    for vq in [float(x) for x in sys.argv[2:]]:
        d=run(vq, 0.5, ramp_drive(2e-3), T=4e-3, maxstep=1e-6, tag=f"L_vq_{vq}")
        L=loop(d,2e-3); print(f"VQ {vq}: trig {L['vtrig']:.2f} rel {L['vrel']:.2f} ratio {L['ratio']:.1f}", flush=True)
