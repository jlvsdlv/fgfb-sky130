"""Publication figures (PDF) for the AEU manuscript, from the PDK-only post-layout data."""
import glob, json, numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from rate import rate_from
from lib import loop

OUT = "../figures/"
import os; os.makedirs(OUT, exist_ok=True)
plt.rcParams.update({"font.size": 8, "font.family": "DejaVu Sans", "axes.linewidth": 0.6,
                     "lines.linewidth": 1.1, "axes.grid": True, "grid.color": "#dddddd",
                     "grid.linewidth": 0.4, "axes.spines.top": False, "axes.spines.right": False,
                     "legend.frameon": False, "legend.fontsize": 7, "xtick.major.width": 0.6,
                     "ytick.major.width": 0.6, "savefig.bbox": "tight", "savefig.pad_inches": 0.02})
SEQ = {0.40: "#9ecae1", 0.45: "#4292c6", 0.50: "#2171b5", 0.55: "#08306b"}
GREY, ACC, RED = "#7f7f7f", "#1f5fbf", "#c0392b"


def lab(ax, s):
    ax.text(-0.16, 1.04, s, transform=ax.transAxes, fontweight="bold", fontsize=9, va="bottom")


# ---------- Fig. 3: static hysteresis ----------
fig, axs = plt.subplots(1, 2, figsize=(7.2, 2.5), gridspec_kw={"width_ratios": [1.6, 1]})
ax = axs[0]
for vq in [0.40, 0.45, 0.50, 0.55]:
    d = np.loadtxt(f"L_vq_{vq}.out"); v, i = d[:, 1], -d[:, 2] * 1e6
    ax.semilogy(v, np.maximum(i, 1e-5), color=SEQ[vq], label=f"$V_Q$ = {vq:.2f} V")
ax.set_xlim(2.5, 6); ax.set_ylim(1e-3, 30)
ax.set_xlabel("$V_{mem}$ (V)"); ax.set_ylabel("$I_D$ (µA)")
ax.legend(loc="upper left", ncol=2); lab(ax, "(a)")
ax = axs[1]
for f, c, l in [("L_rate_0.0002.out", GREY, "200 µs ramp"), ("L_rate_0.02.out", ACC, "20 ms ramp")]:
    d = np.loadtxt(f); ax.semilogy(d[:, 1], np.maximum(-d[:, 2] * 1e6, 1e-5), color=c, label=l)
ax.set_xlim(3, 5.5); ax.set_ylim(1e-3, 10)
ax.set_xlabel("$V_{mem}$ (V)"); ax.set_ylabel("$I_D$ (µA)")
ax.legend(loc="lower right"); lab(ax, "(b)")
fig.tight_layout(); fig.savefig(OUT + "fig_hysteresis.pdf"); plt.close(fig)

# ---------- Fig. 4: neuron operation ----------
fig, axs = plt.subplots(1, 2, figsize=(7.2, 2.5), gridspec_kw={"width_ratios": [1.5, 1]})
ax = axs[0]
d = np.loadtxt("IF_0.45_5e-08.out"); t = d[:, 0] * 1e6; m = (t > 30) & (t < 80)
ax.plot(t[m] - 30, d[m, 1], color=ACC)
ax.set_xlabel("time (µs)"); ax.set_ylabel("$V_{mem}$ (V)", color=ACC)
axb = ax.twinx(); axb.grid(False); axb.spines["right"].set_visible(True)
axb.plot(t[m] - 30, d[m, 4], color=RED, lw=0.9)
axb.set_ylabel("$V_{body}$ (V)", color=RED); lab(ax, "(a)")
ax = axs[1]
band = {}
for vq in [0.40, 0.45, 0.50, 0.55]:
    pts = []
    for f in glob.glob(f"IF_{vq}_*.out"):
        iin = float(f.split("_")[2][:-4]); dd = np.loadtxt(f); r, sw, _, _ = rate_from(dd)
        mm = dd[:, 0] > dd[-1, 0] * 0.3
        pts.append((iin, r, float(dd[mm, 1].mean())))
    pts.sort(); band[vq] = pts
    x = np.array([p[0] for p in pts]) * 1e9; y = np.array([p[1] for p in pts]) / 1e3
    on = y > 0
    ax.plot(x[on], y[on], "o-", color=SEQ[vq], ms=3, label=f"$V_Q$ = {vq:.2f} V")
    ax.plot(x[~on], y[~on], "x", color=SEQ[vq], ms=3.5)
ax.set_xscale("log"); ax.set_xlabel("$I_{in}$ (nA)"); ax.set_ylabel("firing rate (kHz)")
ax.legend(loc="upper left"); lab(ax, "(b)")
fig.tight_layout(); fig.savefig(OUT + "fig_neuron.pdf"); plt.close(fig)
json.dump({str(k): v for k, v in band.items()}, open("band.json", "w"), indent=1)

# ---------- Fig. 5: control-gate modulation ----------
fig, ax = plt.subplots(figsize=(7.2, 2.0))
d = np.loadtxt("MOD.out"); t = d[:, 0] * 1e6
ax.axvspan(60, 110, color="#d9ead3", lw=0); ax.axvspan(140, 190, color="#f4cccc", lw=0)
ax.plot(t, d[:, 1], color=ACC, lw=0.9)
ax.text(85, 5.65, "$V_A$: 0 → 1.8 V", ha="center", fontsize=7)
ax.text(165, 5.65, "$V_B$: 1.8 → 0 V", ha="center", fontsize=7)
ax.set_xlim(20, 200); ax.set_ylim(2.8, 5.95)
ax.set_xlabel("time (µs)"); ax.set_ylabel("$V_{mem}$ (V)")
fig.tight_layout(); fig.savefig(OUT + "fig_modulation.pdf"); plt.close(fig)

# energy per spike for every firing point
E = []
for vq, pts in band.items():
    for iin, r, vav in pts:
        if r > 0: E.append((vq, iin, r, iin * vav / r))
json.dump(E, open("energy.json", "w"), indent=1)
for e in E: print("VQ %.2f Iin %5.1f nA  f %6.1f kHz  E %.2f pJ" % (e[0], e[1] * 1e9, e[2] / 1e3, e[3] * 1e12))
