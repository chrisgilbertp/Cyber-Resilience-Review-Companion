"""Reproduce the five engineering figures.

Article  Quantum Computing and Artificial Intelligence in Learning and Device Engineering
Journal  Quantum Machine Intelligence
Authors  Chris Gilbert and Maxwell Dorgbefu Jnr
Chris Gilbert  Department of Computer Science and Engineering, William V. S. Tubman University, Harper, Liberia
Maxwell Dorgbefu Jnr  Department of Information Technology Education, University of Skills Training and Entrepreneurial Development (USTED), Kumasi, Ghana
Correspondence  Chris Gilbert  cabilimi@tubmanu.edu.lr

Run python build_figures.py in the extracted folder.
The script writes RGB PNG and vector EPS files to the figures directory.
Requires Python, NumPy, Matplotlib and Pillow.
OpenAI ChatGPT assisted with the plotting code.
"""
from io import BytesIO
from pathlib import Path
import csv
import math

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
from matplotlib.patches import FancyArrowPatch, FancyBboxPatch
from matplotlib.ticker import MultipleLocator
import numpy as np
from PIL import Image

ROOT = Path(__file__).resolve().parent
OUTPUT = ROOT / 'figures'
OUTPUT.mkdir(exist_ok=True)
DPI = 650
BLUE = "#1C5682"
ORANGE = "#A55318"
TEAL = "#20655B"
INK = "#202B35"
MUTED = "#4C5C67"
LIGHT = "#E9F1F7"
PALE = "#EEF5F3"
GRAY = "#D5DDE3"
WIDTH = 6.68
plt.rcParams.update({
    "font.family": "Liberation Sans", "font.size": 8.5,
    "axes.labelsize": 8.5, "axes.titlesize": 9,
    "axes.spines.top": False, "axes.spines.right": False,
    "axes.edgecolor": INK, "axes.labelcolor": INK, "text.color": INK,
    "xtick.labelsize": 8, "ytick.labelsize": 8,
    "legend.fontsize": 8, "legend.frameon": False,
    "pdf.fonttype": 42, "ps.fonttype": 42,
    "savefig.facecolor": "white",
})

def export(fig, number):
    fig.savefig(OUTPUT / f"Fig{number}.eps", format="eps")
    with BytesIO() as buffer:
        fig.savefig(buffer, format="png", dpi=DPI)
        buffer.seek(0)
        with Image.open(buffer) as image:
            image.convert("RGB").save(OUTPUT / f"Fig{number}.png", dpi=(DPI, DPI))
    plt.close(fig)

def canvas(height):
    fig = plt.figure(figsize=(WIDTH, height))
    ax = fig.add_axes([0, 0, 1, 1])
    ax.set(xlim=(0, 1), ylim=(0, 1))
    ax.axis("off")
    return fig, ax

def block(ax, x, y, w, h, title, lines, accent=BLUE, face=LIGHT):
    patch = FancyBboxPatch((x, y), w, h, boxstyle="round,pad=.004,rounding_size=.012",
                           edgecolor=accent, facecolor=face, linewidth=.9, zorder=3)
    ax.add_patch(patch)
    ax.text(x+w/2, y+h*.70, title, fontsize=8.7, fontweight="bold", color=accent,
            ha="center", va="center", zorder=4)
    ax.text(x+w/2, y+h*.30, lines, fontsize=8, ha="center", va="center",
            linespacing=1.13, color=MUTED, zorder=4)

def arrow(ax, start, end, color=MUTED, dashed=False, connection="arc3"):
    ax.add_patch(FancyArrowPatch(start, end, arrowstyle="-|>", mutation_scale=9,
                                 linewidth=1.05, linestyle="--" if dashed else "-",
                                 color=color, connectionstyle=connection, zorder=2))

def axes_grid(ax):
    ax.grid(axis="y", which="major", color=GRAY, linewidth=.6)
    ax.set_axisbelow(True)

def panel(ax, title):
    ax.set_title(title, loc="left", fontweight="bold", pad=8)
    axes_grid(ax)

def gram_shots(samples, shots_per_pair):
    return samples * (samples - 1) // 2 * shots_per_pair

def gradient_shots(parameters, batch, groups, shots_per_setting):
    return 2 * parameters * batch * groups * shots_per_setting

def raw_array_bytes(qubits, density=False):
    return 16 * (4 if density else 2)**qubits

# Figure 1. Hybrid QML workflow and location of the quantum contribution.
fig, ax = canvas(2.65)
ax.text(.024, .927, "Classical input", fontweight="bold", color=MUTED)
ax.text(.498, .927, "Quantum circuit", fontweight="bold", color=TEAL, ha="center")
ax.text(.805, .927, "Classical output", fontweight="bold", color=MUTED)
stages = [
    ("Prepare", "Split, fit and\ntransform"),
    ("Encode", "Map inputs to\nquantum states"),
    ("Process", "Kernel or\ntrainable circuit"),
    ("Measure", "Sample outcomes\nwith fixed shots"),
    ("Evaluate", "Training loss or\nheld-out score"),
]
for i, (title, lines) in enumerate(stages):
    x = .023 + .194*i
    quantum = i in {1, 2, 3}
    block(ax, x, .51, .174, .31, title, lines, TEAL if quantum else BLUE,
          PALE if quantum else LIGHT)
    if i:
        arrow(ax, (x-.016, .662), (x-.003, .662))
block(ax, .403, .087, .370, .248, "Training feedback",
      "Optimiser updates circuit parameters")
arrow(ax, (.888, .503), (.777, .212), BLUE, dashed=True, connection="arc3,rad=-.13")
arrow(ax, (.496, .339), (.497, .502), BLUE, dashed=True)
ax.text(.023, .185, "Solid  data path\nDashed  training only", fontsize=8, color=MUTED,
        va="center", linespacing=1.35)
export(fig, 1)

# Figure 2. Finite-shot precision and direct Gram acquisition.
fig, (a, b) = plt.subplots(1, 2, figsize=(WIDTH, 3.10))
fig.subplots_adjust(left=.115, right=.978, bottom=.20, top=.855, wspace=.42)
shots = np.logspace(1, 6, 121)
panel(a, "(a)")
a.loglog(shots, 1/np.sqrt(shots), color=BLUE, lw=1.5, label="Pauli ±1")
a.loglog(shots, .5/np.sqrt(shots), color=ORANGE, lw=1.5, ls="--", label="Binary 0/1")
a.set_xlabel("Independent shots per estimate")
a.set_ylabel("Maximum standard error")
a.legend(loc="upper right")
panel(b, "(b)")
samples = np.unique(np.geomspace(8, 4096, 100).astype(int))
for budget, color, ls in [(128, TEAL, ":"), (1024, BLUE, "-"), (8192, ORANGE, "--")]:
    b.loglog(samples, gram_shots(samples, budget), label=f"{budget:,} shots/pair",
             color=color, ls=ls, lw=1.5)
b.set_xlabel("Training samples")
b.set_ylabel("Total circuit shots")
b.legend(loc="upper left")
export(fig, 2)

# Figure 3. Explicit storage and gradient resource models.
fig, (a, b) = plt.subplots(1, 2, figsize=(WIDTH, 3.14))
fig.subplots_adjust(left=.111, right=.978, bottom=.203, top=.85, wspace=.43)
panel(a, "(a)")
for density, c, style, name in [(False, BLUE, "-", "Statevector"), (True, ORANGE, "--", "Density matrix")]:
    qubits = np.arange(4, 33 if not density else 17)
    gib = [raw_array_bytes(int(n), density)/2**30 for n in qubits]
    a.semilogy(qubits, gib, c=c, ls=style, lw=1.5, label=name)
a.axhline(16, c=MUTED, lw=.8, ls=":", label="16 GiB")
a.set_xlabel("Qubits")
a.set_ylabel("Memory (GiB, complex128)")
a.set_xlim(4, 33)
a.legend(loc="lower right")
panel(b, "(b)")
params = np.arange(8, 513)
for s, color, ls in [(128, TEAL, ":"), (1024, BLUE, "-"), (8192, ORANGE, "--")]:
    b.semilogy(params, gradient_shots(params, 32, 4, s), color=color, ls=ls, lw=1.5,
               label=f"{s:,} shots/setting")
b.set_xlabel("Trainable parameters")
b.set_ylabel("Circuit shots per full gradient")
b.legend(loc="lower right")
export(fig, 3)

# Figure 4. Online error-correction stream, separate offline learning loop.
fig, ax = canvas(2.86)
nodes = [
    ("Syndrome extraction", "Repeated checks\non quantum hardware"),
    ("Stream and buffer", "Timestamp and\nroute events"),
    ("Decoder inference", "Estimate logical\nframe change"),
    ("Apply or track", "Consume output by\nfeedback deadline"),
]
for i, (title, lines) in enumerate(nodes):
    x = .024 + .245*i
    block(ax, x, .54, .219, .30, title, lines, TEAL if i==2 else BLUE,
          PALE if i==2 else LIGHT)
    if i:
        arrow(ax, (x-.022, .69), (x-.003, .69))
block(ax, .498, .09, .233, .245, "Offline training", "Simulated and\ncalibration data")
arrow(ax, (.612, .339), (.612, .532), BLUE, dashed=True)
ax.text(.025, .264, "Throughput", fontsize=8.7, fontweight="bold", color=BLUE)
ax.text(.025, .167, "Rounds processed per second", fontsize=8, color=MUTED)
ax.text(.025, .100, "Check backlog under sustained load", fontsize=8, color=MUTED)
ax.text(.760, .264, "Feedback latency", fontsize=8.7, fontweight="bold", color=BLUE)
ax.text(.760, .167, "Detection to usable result", fontsize=8, color=MUTED)
ax.text(.760, .100, "Tail latency and misses", fontsize=8, color=MUTED)
export(fig, 4)

# Figure 5. Replot of published estimates in Bausch et al. (2024), Fig. 3a,b.
with (ROOT / "alphaqubit_sycamore.csv").open(newline="", encoding="utf-8") as f:
    rows = list(csv.DictReader(line for line in f if not line.startswith('#')))
order = ["AlphaQubit (fine-tuned)", "Tensor network", "MWPM-BP", "MWPM-Corr", "PyMatching"]
assert len(rows) == 2*len(order)
results = {(int(r["distance"]), r["decoder"]): (float(r["logical_error_pct_per_round"]),
            float(r["reported_uncertainty_percentage_points"])) for r in rows}
assert len(results) == len(rows)
fig, ax = plt.subplots(figsize=(WIDTH, 3.12))
fig.subplots_adjust(left=.285, right=.971, bottom=.195, top=.82)
positions = np.arange(len(order))
for d, marker, color, offset in [(3, "o", BLUE, -.13), (5, "s", ORANGE, .13)]:
    rates, uncertainties = np.array([results[d, name] for name in order]).T
    ax.errorbar(rates, positions+offset, xerr=uncertainties, fmt=marker,
                color=color, markersize=4.8, capsize=2.4, elinewidth=.9,
                markerfacecolor="white" if d==3 else color, label=f"Distance {d}")
ax.set_yticks(positions, order)
ax.invert_yaxis()
ax.set_xlim(2.60, 4.52)
ax.xaxis.set_major_locator(MultipleLocator(.25))
ax.set_xlabel("Logical error per error-correction round (%)")
ax.grid(axis="x", color=GRAY, linewidth=.6)
ax.set_axisbelow(True)
ax.legend(loc="lower center", bbox_to_anchor=(.5, 1.02), ncol=2)
export(fig, 5)

assert gram_shots(1024, 1024) == 536_346_624
assert gradient_shots(100, 32, 4, 1024) == 26_214_400
assert raw_array_bytes(30)/2**30 == raw_array_bytes(15, True)/2**30 == 16
assert math.isclose(.5/math.sqrt(1024), .015625)
d3 = 100*(1-results[3, order[0]][0]/results[3, order[1]][0])
d5 = 100*(1-results[5, order[0]][0]/results[5, order[1]][0])
print(f"Relative LER reduction vs tensor network: distance 3 {d3:.2f}%, distance 5 {d5:.2f}%")
print(f"NumPy {np.__version__}; Matplotlib {matplotlib.__version__}")
