import json, numpy as np, matplotlib
matplotlib.use("Agg"); import matplotlib.pyplot as plt
plt.rcParams.update({"font.size": 8, "font.family": "DejaVu Sans", "axes.linewidth": 0.6,
    "axes.spines.top": False, "axes.spines.right": False, "legend.frameon": False,
    "legend.fontsize": 7, "savefig.bbox": "tight", "savefig.pad_inches": 0.02})
C = ["#2a6fdb", "#e07b39", "#3a9e6b", "#8a5cc2"]
S = json.load(open("pois_stats.json")); W = json.load(open("wsum_stats.json"))
fig, ax = plt.subplots(1, 2, figsize=(7.2, 2.7))
a = ax[0]
for k, amp in enumerate([0.6, 1.2, 1.8]):
    pts = sorted([v for kk, v in S.items() if kk.startswith(f"{amp}_") and v["n"] >= 3], key=lambda v: v["rin"])
    x = [v["rin"]/1e3 for v in pts]; y = [v["rout"]/1e3 for v in pts]; e = [v["se"]/1e3 for v in pts]
    a.errorbar(x, y, yerr=e, fmt="-o", c=C[k], ms=4, lw=1.2, capsize=2, label=f"{amp} V pulses")
a.set_xlabel("Mean Poisson input rate on $V_A$ (kHz)"); a.set_ylabel("Mean output rate (kHz)")
a.set_xlim(0, 170); a.set_ylim(0, 20); a.legend(loc="upper left")
a.set_title("(a) Graded response, one input (no input: silent)", loc="left", fontsize=8)
a = ax[1]; w = W["w"]
mk = {"A": ("o", C[0], "input A only"), "B": ("s", C[1], "input B only ($2\\times C_{in}$)"), "AB": ("D", C[2], "A and B together")}
seen = set()
for r in W["rows"]:
    t = "A" if r["rB"] == 0 else ("B" if r["rA"] == 0 else "AB")
    m, c, l = mk[t]; x = (r["rA"] + w*r["rB"])/1e3
    a.errorbar(x, r["rout"]/1e3, yerr=r["se"]/1e3, fmt=m, c=c, ms=5, capsize=2, label=None if t in seen else l); seen.add(t)
xx = np.linspace(50, 195, 10); a.plot(xx, (W["slope"]*xx*1e3 + W["icpt"])/1e3, "--", c="#888", lw=0.8)
a.set_xlabel(f"Weighted input $r_A + {w:.1f}\\,r_B$ (kHz)"); a.set_ylabel("Mean output rate (kHz)")
a.set_xlim(50, 200); a.set_ylim(0, 16); a.legend(loc="upper left")
a.set_title("(b) Two inputs combine as a weighted sum", loc="left", fontsize=8)
fig.tight_layout(); fig.savefig("../figures/fig_poisson.pdf"); fig.savefig("fig_poisson.png", dpi=170)
