"""Combined figure for the AICSP letter: hysteresis vs V_Q, spiking waveform, firing bands."""
import glob, numpy as np, matplotlib
matplotlib.use("Agg"); import matplotlib.pyplot as plt
from rate import rate_from
plt.rcParams.update({"font.size": 8, "font.family": "DejaVu Sans", "axes.linewidth": 0.6,
    "lines.linewidth": 1.1, "axes.grid": True, "grid.color": "#dddddd", "grid.linewidth": 0.4,
    "axes.spines.top": False, "axes.spines.right": False, "legend.frameon": False,
    "legend.fontsize": 6.5, "savefig.bbox": "tight", "savefig.pad_inches": 0.02})
SEQ = {0.40: "#9ecae1", 0.45: "#4292c6", 0.50: "#2171b5", 0.55: "#08306b"}
ACC, RED = "#1f5fbf", "#c0392b"
def lab(ax, s): ax.text(-0.2, 1.03, s, transform=ax.transAxes, fontweight="bold", fontsize=9, va="bottom")
fig, axs = plt.subplots(1, 3, figsize=(7.2, 2.3), gridspec_kw={"width_ratios": [1.15, 1.1, 1]})
ax = axs[0]
for vq in [0.40, 0.45, 0.50, 0.55]:
    d = np.loadtxt(f"L_vq_{vq}.out"); ax.semilogy(d[:, 1], np.maximum(-d[:, 2]*1e6, 1e-5), color=SEQ[vq], label=f"{vq:.2f} V")
ax.set_xlim(2.5, 6); ax.set_ylim(1e-3, 30); ax.set_xlabel("$V_{mem}$ (V)"); ax.set_ylabel("$I_D$ (µA)")
ax.legend(loc="upper left", title="$V_Q$", title_fontsize=6.5, ncol=2); lab(ax, "(a)")
ax = axs[1]
d = np.loadtxt("IF_0.45_5e-08.out"); t = d[:, 0]*1e6; m = (t > 30) & (t < 70)
ax.plot(t[m]-30, d[m, 1], color=ACC); ax.set_xlabel("time (µs)"); ax.set_ylabel("$V_{mem}$ (V)", color=ACC)
axb = ax.twinx(); axb.grid(False); axb.spines["right"].set_visible(True)
axb.plot(t[m]-30, d[m, 4], color=RED, lw=0.8); axb.set_ylabel("$V_{body}$ (V)", color=RED); lab(ax, "(b)")
ax = axs[2]
for vq in [0.40, 0.45, 0.50, 0.55]:
    pts = []
    for f in glob.glob(f"IF_{vq}_*.out"):
        iin = float(f.split("_")[2][:-4]); r = rate_from(np.loadtxt(f))[0]; pts.append((iin, r))
    pts.sort(); x = np.array([p[0] for p in pts])*1e9; y = np.array([p[1] for p in pts])/1e3; on = y > 0
    ax.plot(x[on], y[on], "o-", color=SEQ[vq], ms=3, label=f"{vq:.2f} V"); ax.plot(x[~on], y[~on], "x", color=SEQ[vq], ms=3.5)
ax.set_xscale("log"); ax.set_xlabel("$I_{in}$ (nA)"); ax.set_ylabel("firing rate (kHz)")
ax.legend(loc="upper left", title="$V_Q$", title_fontsize=6.5); lab(ax, "(c)")
fig.tight_layout(w_pad=1.0); fig.savefig("../figures/fig_neuron3.pdf"); fig.savefig("../figures/fig_neuron3.png", dpi=150)
