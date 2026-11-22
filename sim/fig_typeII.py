"""Type II excitability and input locking (PDK-only, extracted layout)."""
import json, numpy as np, matplotlib, matplotlib.ticker
matplotlib.use("Agg"); import matplotlib.pyplot as plt
plt.rcParams.update({"font.size": 8, "font.family": "DejaVu Sans", "axes.linewidth": 0.6,
    "axes.spines.top": False, "axes.spines.right": False, "legend.frameon": False,
    "legend.fontsize": 7, "savefig.bbox": "tight", "savefig.pad_inches": 0.02})
C = ["#2a6fdb", "#e07b39", "#3a9e6b"]
L = lambda f: json.load(open(f))
fi = {}
def add(vq, g, i, r, sw): fi.setdefault((vq, g), []).append((i*1e9, r/1e3, sw))
for r in L("onset1.json"):
    if r.get("ms", 2e-8) == 2e-8: add(r["vq"], 0.5, r["iin"], r["rate"], r["swing"])
for i, r, _ in L("band.json")["0.4"]:
    if i <= 5e-8: add(0.40, 0.5, i, r, 1.0 if r > 0 else 0)
for f in ["onset_vg2.json", "onset_vg2b.json"]:
    for r in L(f):
        if r["vg2"] == 0.4: add(r["vq"], 0.4, r["iin"], r["rate"], r["swing"])
fig, ax = plt.subplots(2, 2, figsize=(7.2, 4.6))
a = ax[0, 0]
for k, key in enumerate([(0.38, 0.5), (0.40, 0.5), (0.40, 0.4)]):
    p = sorted(fi[key]); i = np.array([q[0] for q in p]); r = np.array([q[1] for q in p])
    on = r > 0
    a.plot(i[on], r[on], "-o", c=C[k], ms=4, lw=1.2,
           label=f"$V_Q$={key[0]:.2f} V, $V_{{G2}}$={key[1]:.1f} V")
    a.plot(i[~on], r[~on], "o", mfc="white", c=C[k], ms=4)
    if on.any():
        j = np.argmax(on); a.plot([i[j-1], i[j]], [0, r[j]], ":", c=C[k], lw=1)
a.set_xlim(0, 52); a.set_ylim(-3, 95); a.set_xlabel("Input current $I_{in}$ (nA)")
a.set_ylabel("Firing rate (kHz)"); a.legend(loc="upper left")
a.set_title("(a) Discontinuous onset (open = silent)", loc="left", fontsize=8)
a = ax[0, 1]
for k, (f, lab) in enumerate([("TR_8n.npy", "8.0 nA"), ("TR_8.5n.npy", "8.5 nA")]):
    d = np.load(f); m = (d[:, 0] > 1.2e-3) & (d[:, 0] < 1.5e-3)
    a.plot((d[m, 0]-1.2e-3)*1e6, d[m, 1], c=C[k], lw=1, label=lab)
a.set_xlabel("Time (µs)"); a.set_ylabel("$V_{mem}$ (V)"); a.legend(loc="lower right", ncol=2)
a.set_title("(b) Hopf-like onset, $V_Q$=0.40 V, $V_{G2}$=0.4 V", loc="left", fontsize=8)
aw = L("amp_width.json")
a = ax[1, 0]
w = [(r["w"]*1e6, r["rate"]/1e3) for r in aw if r["amp"] == 1.8] + [(2.0, 25.0)]
w = sorted(w)
a.plot([q[0] for q in w], [q[1] for q in w], "-o", c=C[0], ms=4, lw=1.2)
a.text(0.55, 36.2, "amplitude 0.3 V (2 µs): 23.1 kHz\namplitude ≥0.6 V (2 µs): 25.0 kHz", fontsize=6.5, color="#444", va="top")
for n, lbl in [(4, "$f_{in}/4$"), (3, "$f_{in}/3$")]:
    a.axhline(100/n, c="#999", lw=0.6, ls="--"); a.text(8.3, 100/n+0.4, lbl, fontsize=7, color="#666", ha="right")
a.set_xscale("log"); a.set_xticks([0.5, 1, 2, 4, 8]); a.set_xticklabels(["0.5", "1", "2", "4", "8"])
a.set_xlabel("Pulse width (µs), amplitude 1.8 V"); a.xaxis.set_minor_formatter(matplotlib.ticker.NullFormatter()); a.set_ylabel("Output rate (kHz)"); a.set_ylim(15, 38)
a.set_title("(c) 100 kHz input below rheobase (20 nA)", loc="left", fontsize=8)
a = ax[1, 1]
fs = [0, 50, 100, 200]
for k, vq in enumerate([0.42, 0.45, 0.48]):
    rr = [0]*4
    for line in open("syn2.log"):
        if line.startswith("{"):
            r = json.loads(line)
            if abs(r["vq"]-vq) < 1e-6 and r["iin"] == 4e-8: rr[fs.index(int(r["f"]/1e3))] = r["rate"]/1e3
    a.plot(range(4), rr, "-o", c=C[k], ms=4, lw=1.2, label=f"$V_Q$={vq:.2f} V")
for y in [50, 66.67, 75]: a.axhline(y, c="#999", lw=0.6, ls="--")
a.text(3.1, 66.67, "$f_{in}/3$", fontsize=7, va="center", color="#666")
a.set_xticks(range(4)); a.set_xticklabels(["none", "50", "100", "200"]); a.set_xlim(-0.2, 3.5)
a.set_xlabel("Input pulse rate (kHz)"); a.set_ylabel("Output rate (kHz)"); a.legend(loc="lower right")
a.set_title("(d) Above rheobase (40 nA): mode locking", loc="left", fontsize=8)
fig.tight_layout(h_pad=1.2)
fig.savefig("../figures/fig_typeII.pdf"); fig.savefig("../figures/fig_typeII.png", dpi=170)
