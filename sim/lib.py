"""PDK-only simulations of the extracted FGFB layout (stock sky130 models, no macromodel)."""
from lib import PDK_LIB
import subprocess, uuid, os, numpy as np
PDK_LIB = os.path.join(os.environ.get("PDK_ROOT", "/usr/local/share/pdk"), os.environ.get("PDK", "sky130A"), "libs.tech/ngspice/sky130.lib.spice")
RQ = "1e18"
FGIC = False
HDR = f""".lib {PDK_LIB} tt
.param mc_mm_switch=0 mc_pr_switch=0
.include pex_flat.spice
Vvddh vddh 0 5
Vg1 gnd1 0 0
Vg2b gnd2 0 0
Vg3 gnd3 0 0
Vg4 gnd4 0 0
Vsub VSUBS 0 0
"""
def run(vq, vg2, drive, srcA="0", srcB="0", T=1e-3, maxstep=None, extra="", tag=None, ic=None, corner="tt", temp=27, mc=0, seed=1):
    tag = tag or "r_" + uuid.uuid4().hex[:6]
    hdr = HDR.replace(" tt\n", f" {corner}\n").replace("mc_mm_switch=0", f"mc_mm_switch={mc}")
    net = hdr + f""".temp {temp}
.options seed={seed}
VQ vq 0 {vq}
Rq fg vq {RQ}
VinA ina 0 {srcA}
VinB inb 0 {srcB}
VG2 g2 0 {vg2}
{drive}
{extra}
"""
    if ic is not None: net += f".ic v(vmem)={ic}" + (f" v(fg)={vq}" if FGIC else "") + "\n"
    ms = f" 0 {maxstep}" if maxstep else ""
    net += f""".control
set wr_singlescale
set rndseed={seed}
tran {maxstep or 20e-9} {T}{ms}
wrdata {tag}.out v(vmem) i(Vdrv) v(fg) v(body)
.endc
.end
"""
    open(f"{tag}.sp", "w").write(net)
    p = subprocess.run(["ngspice", "-b", f"{tag}.sp"], capture_output=True, text=True, timeout=1500)
    if not os.path.exists(f"{tag}.out"): raise RuntimeError(p.stdout[-3000:])
    d = np.loadtxt(f"{tag}.out")
    if tag.startswith("r_"): os.remove(f"{tag}.sp"); os.remove(f"{tag}.out")
    return d

def ramp_drive(tr, vmax=6.0):
    return f"Vdrv vmem 0 PWL(0 0.05 {tr} {vmax} {2*tr} 0.05)"

def loop(d, tr):
    t, v, i = d[:,0], d[:,1], -d[:,2]
    up = t <= tr; dn = t > tr
    g = np.linspace(0.2, 5.9, 1141)
    iu = np.interp(g, v[up], i[up]); o = np.argsort(v[dn]); idn = np.interp(g, v[dn][o], i[dn][o])
    r = (idn + 1e-12) / (iu + 1e-12)
    area = np.trapezoid(np.abs(idn - iu), g)
    k = np.argmax(r)
    # trigger (up jump) and release (down jump) voltages: largest log-slope points
    lu = np.log10(np.maximum(iu, 1e-13)); ld = np.log10(np.maximum(idn, 1e-13))
    vt = g[np.argmax(np.diff(lu))]; vr = g[np.argmax(np.diff(ld))]
    return dict(area=area, ratio=r[k], at=g[k], ilow=iu[k], ihigh=idn[k], vtrig=vt, vrel=vr)
