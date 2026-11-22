import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt, matplotlib.image as mpimg
plt.rcParams.update({"font.size": 8, "font.family": "DejaVu Sans"})
img = mpimg.imread("../layout/original/layout_paper.png")
H, W = img.shape[:2]
x0, x1, y0, y1 = -15.5, 22.7, -5.5, 24.5
fig, ax = plt.subplots(figsize=(6.0, 6.0 * H / W))
ax.imshow(img, extent=[x0, x1, y0, y1]); ax.set_xlim(x0, x1); ax.set_ylim(y0, y1)
ax.set_xlabel("x (µm)"); ax.set_ylabel("y (µm)")
for s in ["top", "right"]: ax.spines[s].set_visible(False)
def note(x, y, t, tx, ty):
    ax.annotate(t, xy=(x, y), xytext=(tx, ty), fontsize=7, ha="center",
                arrowprops=dict(arrowstyle="-", lw=0.5, color="#333333"),
                bbox=dict(boxstyle="round,pad=0.2", fc="white", ec="#888888", lw=0.4))
note(-9, 16, "$C_{fix}$ (MIM, 192 fF)", -9, 23.2)
note(16, 18, "$C_{mem}$ (MIM, 208 fF)", 9.5, 23.2)
note(2.5, 11.5, "$C_A$", 2.0, 15.0)
note(7.5, 11.5, "$C_B$", 8.0, 15.0)
note(-4, 8.25, "FG bus (metal 4)", -9.5, 6.5)
note(10, 5.2, "$V_{mem}$ (metal 2)", 10.5, 8.0)
note(0, 0, "$M_1$ in deep n-well", -9.5, 0.5)
note(9, 0, "$M_2$ (bulk control)", 15.5, 1.5)
note(4.5, -0.6, "body (metal 1)", 6, -4.2)
fig.tight_layout(); fig.savefig("../figures/fig_layout.pdf", dpi=300)
