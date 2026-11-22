"""Robustness figure: firing window vs stored charge across corners/temperature; Monte Carlo."""
import json, glob, numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.colors import Normalize
from matplotlib import cm
plt.rcParams.update({"font.size": 8, "font.family": "DejaVu Sans", "axes.linewidth": 0.6,
                     "axes.spines.top": False, "axes.spines.right": False, "legend.frameon": False,
                     "legend.fontsize": 7, "savefig.bbox": "tight", "savefig.pad_inches": 0.02})

# ---- collect corner / temperature points at 50 nA (rate in kHz, 0 = no firing)
pts = {}   # label -> list of (vq, rate)
def add(lbl, vq, r): pts.setdefault(lbl, []).append((vq, r / 1e3))
for r in json.load(open("rob_corner.json")): add(r["corner"], r["vq"], r["rate"])
for r in json.load(open("trim_corner.json")): add(r["corner"], r["vq"], r["rate"])
for r in json.load(open("rob_temp.json")): add(f"{r['temp']} °C", r["vq"], r["rate"])
extra = []   # points at other currents, marked separately
for r in json.load(open("trim2.json")):
    if "temp" in r: add(f"{r['temp']} °C", r["vq"], r["rate"])
    elif r["iin"] == 50e-9: add(r["corner"], r["vq"], r["rate"])
    else: extra.append((r["corner"], r["vq"], r["iin"], r["rate"] / 1e3, 0.5))
for f in glob.glob("vg2_*.json"):          # V_G2 retrim results
    for r in json.load(open(f)): extra.append((r["label"], r["vq"], r["iin"], r["rate"] / 1e3, r["vg2"]))
for q, r in [(v, r) for v, r in pts["tt"]]: add("27 °C", q, r * 1e3)

rows = ["tt", "ff", "ss", "fs", "sf", "-40 °C", "27 °C", "85 °C"]
norm = Normalize(60, 120); cmap = cm.Blues

fig, axs = plt.subplots(1, 2, figsize=(7.2, 2.7), gridspec_kw={"width_ratios": [1.45, 1]})
ax = axs[0]
for k, lbl in enumerate(rows):
    y = len(rows) - 1 - k
    for vq, r in pts.get(lbl, []):
        if r > 0:
            ax.scatter(vq, y, s=34, c=[cmap(norm(r))], edgecolors="#1f3b73", linewidths=0.4, zorder=3)
        else:
            ax.scatter(vq, y, s=10, marker="x", c="#9a9a9a", linewidths=0.6, zorder=2)
    for c, vq, iin, r, g in extra:
        if c == lbl and r > 0 and abs(iin - 50e-9) < 1e-12:
            ax.scatter(vq, y, s=40, marker="D", facecolors="none", edgecolors="#c0392b", linewidths=0.8, zorder=4)
ax.axvline(0.45, color="#555555", lw=0.6, ls="--")
ax.text(0.452, len(rows) - 0.55, "nominal $V_Q$", fontsize=6.5, color="#555555")
ax.scatter([], [], s=34, c=[cmap(norm(90))], edgecolors="#1f3b73", linewidths=0.4, label="fires, $V_{G2}$ = 0.5 V")
ax.scatter([], [], s=40, marker="D", facecolors="none", edgecolors="#c0392b", linewidths=0.8, label="fires after $V_{G2}$ retrim")
ax.scatter([], [], s=10, marker="x", c="#9a9a9a", linewidths=0.6, label="no firing")
ax.legend(loc="upper center", bbox_to_anchor=(0.5, -0.2), ncol=3, fontsize=6.5, handletextpad=0.2, columnspacing=0.8)
ax.set_yticks(range(len(rows)), rows[::-1]); ax.set_ylim(-0.6, len(rows) - 0.3)
ax.axhline(2.5, color="#cccccc", lw=0.5)
ax.set_xlabel("stored charge $V_Q$ (V)"); ax.grid(axis="x", color="#e5e5e5", lw=0.4)
sm = cm.ScalarMappable(norm=norm, cmap=cmap); sm.set_array([])
cb = fig.colorbar(sm, ax=ax, pad=0.01, fraction=0.04); cb.set_label("rate (kHz)", fontsize=7); cb.ax.tick_params(labelsize=6.5)
ax.text(-0.13, 1.03, "(a)", transform=ax.transAxes, fontweight="bold", fontsize=9)

# ---- Monte Carlo
mc = []
for f in sorted(glob.glob("rob_mc_*.json")): mc += json.load(open(f))
seeds = sorted({r["seed"] for r in mc}); vqs = sorted({r["vq"] for r in mc})
M = np.zeros((len(seeds), len(vqs)))
for r in mc: M[seeds.index(r["seed"]), vqs.index(r["vq"])] = r["rate"] / 1e3
ax = axs[1]
for i, s in enumerate(seeds):
    for j, q in enumerate(vqs):
        if M[i, j] > 0: ax.scatter(q, i + 1, s=12, c=[cmap(norm(M[i, j]))], edgecolors="#1f3b73", linewidths=0.3)
        else: ax.scatter(q, i + 1, s=5, marker="x", c="#bbbbbb", linewidths=0.5)
ax.axvline(0.45, color="#555555", lw=0.6, ls="--")
ax.set_xlabel("stored charge $V_Q$ (V)"); ax.set_ylabel("Monte Carlo sample")
ax.set_xticks(vqs); ax.set_ylim(0, len(seeds) + 1)
ax.text(-0.2, 1.03, "(b)", transform=ax.transAxes, fontweight="bold", fontsize=9)
fig.tight_layout(); fig.savefig("../figures/fig_robust.pdf")

# ---- summary numbers
j45 = vqs.index(0.45)
fire45 = int((M[:, j45] > 0).sum()); anyfire = int((M.max(axis=1) > 0).sum())
r45 = M[M[:, j45] > 0, j45]
print(f"MC: N={len(seeds)}, fire@0.45={fire45}, fire with trim={anyfire}, rate@0.45 mean {r45.mean():.1f} sd {r45.std():.1f} min {r45.min():.1f} max {r45.max():.1f} kHz")
w = [(M[i] > 0) for i in range(len(seeds))]
print("MC window width (grid points) per sample:", [int(x.sum()) for x in w])
for lbl in rows:
    on = sorted(q for q, r in pts.get(lbl, []) if r > 0)
    print(lbl, "fires at", on, "rates", [round(r, 1) for q, r in sorted(pts.get(lbl, [])) if r > 0])
print("extra (other I_in / V_G2):", [e for e in extra if e[3] > 0])
