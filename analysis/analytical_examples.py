"""Reproduce the analytical scenarios and the engineering figures."""
from pathlib import Path
from fractions import Fraction
import csv
import math
import platform

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch, FancyBboxPatch
import numpy as np

ROOT = Path(__file__).resolve().parent
POPULATION = 1_000_000
PREVALENCE = Fraction(1, 1_000)
RECALL = Fraction(9, 10)
BUDGET = 2_000
RECORDS = 1_000_000
REPLICAS = 7
DIGEST_BYTES = 32
ED25519 = 64
MLDSA65 = 3309
BATCH_SIZE = 4096
KEM_KEY = 1184
KEM_CIPHERTEXT = 1088
X25519_SHARE = 32
INK = "#172a38"
MUTED = "#415966"
BLUE = "#18557d"
TEAL = "#20695e"
ORANGE = "#9c481b"
LIGHT = "#e9f3f7"

plt.rcParams.update({"font.family": "DejaVu Sans", "font.size": 8.8,
                     "text.color": INK, "axes.labelcolor": INK,
                     "axes.spines.top": False, "axes.spines.right": False,
                     "axes.edgecolor": MUTED, "axes.linewidth": .8,
                     "pdf.fonttype": 42, "svg.fonttype": "none"})

def write_csv(name, fields, rows):
    with (ROOT / name).open("w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(fields)
        writer.writerows(rows)

def alert_counts(population, prevalence, recall, fpr):
    tp = population * prevalence * recall
    fp = population * (1 - prevalence) * fpr
    return tp, fp, tp / (tp + fp)

def signature_bytes(records, batch_size, signature_size, replicas=1):
    return ((records + batch_size - 1) // batch_size) * signature_size * replicas

def export(fig, number):
    for ext in ("pdf", "svg", "png"):
        fig.savefig(ROOT / f"Figure_{number}.{ext}", dpi=360, facecolor="white")
    plt.close(fig)

def box(ax, x, y, title, subtitle):
    w, h = .258, .205
    patch = FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.012,rounding_size=0.018",
                           edgecolor=BLUE, facecolor=LIGHT, linewidth=1.0)
    ax.add_patch(patch)
    ax.text(x+w/2, y+.132, title, ha="center", va="center", fontweight="bold", fontsize=8.7)
    ax.text(x+w/2, y+.057, subtitle, ha="center", va="center", color=MUTED, fontsize=8.0)

def arrow(ax, a, b, color=TEAL, dashed=False):
    p = FancyArrowPatch(a, b, arrowstyle="-|>", mutation_scale=11,
                        linewidth=1.2, color=color, linestyle="--" if dashed else "-",
                        shrinkA=0, shrinkB=0)
    ax.add_patch(p)

def draw_architecture():
    fig, ax = plt.subplots(figsize=(7.05, 3.14))
    fig.subplots_adjust(left=.025, right=.975, bottom=.025, top=.975)
    ax.set(xlim=(0, 1), ylim=(0, 1))
    ax.axis("off")
    ax.text(.023, .925, "EVIDENCE PLANE", fontsize=8.6, fontweight="bold", color=TEAL)
    ax.text(.023, .475, "RESPONSE PLANE", fontsize=8.6, fontweight="bold", color=TEAL)
    xs = [.024, .371, .718]
    top = [("Sources and collectors", "Identity, timestamp and\nsigned event envelope"),
           ("Encrypted evidence store", "Payloads, access policy\nand retention"),
           ("Witnessed log or ledger", "Signed batch roots\nand continuity proofs")]
    lower = [("Isolated AI analysis", "Verified read-only copies\nand versioned scores"),
             ("Policy and approval", "Validate authority, scope\nand response conditions"),
             ("Action and recovery", "Bounded execution, receipt\nand rollback verification")]
    for entries, y in ((top, .64), (lower, .184)):
        for x, (title, subtitle) in zip(xs, entries):
            box(ax, x, y, title, subtitle)
        for i in range(2):
            arrow(ax, (xs[i]+.274,y+.102), (xs[i+1]-.016,y+.102))
    arrow(ax, (.405,.62), (.268,.405))
    ax.text(.423, .531, "Verified copy", ha="left", va="center", fontsize=8, color=MUTED)
    arrow(ax, (.85,.405), (.85,.62), color=ORANGE, dashed=True)
    ax.text(.826, .514, "Receipt", ha="right", va="center", fontsize=8, color=MUTED)
    ax.text(.023, .065, "Independent keys and authorisation policies separate evidence, scoring and action.",
            fontsize=8.0, color=MUTED)
    export(fig, 1)

def draw_alerts():
    fig, ax = plt.subplots(figsize=(7.05, 3.55))
    fig.subplots_adjust(left=.11, right=.97, bottom=.16, top=.94)
    x = np.geomspace(.00001, .10, 240)
    for p, color, style in ((.0001, MUTED, ":"), (.001, BLUE, "-"), (.01, TEAL, "--")):
        ppv = p * float(RECALL) / (p * float(RECALL) + (1-p) * x)
        ax.semilogx(100*x, 100*ppv, lw=2, ls=style, color=color, label=f"Prevalence {100*p:g}%")
    for fpr in (.0001, .001, .01):
        _, _, ppv = alert_counts(POPULATION, PREVALENCE, RECALL, Fraction(str(fpr)))
        ax.scatter(100*fpr, 100*float(ppv), color=ORANGE, s=22, zorder=4)
    ax.set(xlabel="False-positive rate among benign events (%)", ylabel="Precision among alerts (%)",
           ylim=(-1, 101), xlim=(.001, 10))
    ax.grid(axis="y", color="#d6e0e5", lw=.65)
    ax.legend(loc="upper right", frameon=False, fontsize=8.5)
    export(fig, 2)

def draw_storage():
    fig, ax = plt.subplots(figsize=(7.05, 3.40))
    fig.subplots_adjust(left=.13, right=.97, bottom=.19, top=.90)
    batches = np.array([2**i for i in range(17)])
    for size, color, style, label in ((ED25519, MUTED, "--", "Ed25519"), (MLDSA65, BLUE, "-", "ML-DSA-65")):
        vals = [signature_bytes(RECORDS, int(b), size, REPLICAS)/1e6 for b in batches]
        ax.loglog(batches, vals, color=color, linestyle=style, lw=2, label=label)
    ax.axvline(BATCH_SIZE, color=TEAL, linestyle=":", lw=1.35)
    ax.annotate("4,096 records per root", xy=(BATCH_SIZE, .24),
                xytext=(430, .028), fontsize=8, color=TEAL,
                arrowprops={"arrowstyle":"-", "color":TEAL})
    ax.set(xlabel="Records per signed root", ylabel="Signature-only storage (MB)")
    ax.grid(axis="y", color="#d6e0e5", lw=.65)
    ax.legend(frameon=False, loc="upper right", fontsize=8.5)
    export(fig, 3)

def main():
    alert_rows = []
    for denominator in (100, 1_000, 10_000):
        p = Fraction(1, denominator)
        for f_den in (100, 1_000, 10_000):
            f = Fraction(1, f_den)
            tp, fp, ppv = alert_counts(POPULATION, p, RECALL, f)
            alert_rows.append((POPULATION, float(p), float(RECALL), float(f),
                               float(tp), float(fp), float(tp+fp), float(ppv)))
    write_csv("alert_scenarios.csv",
              ["events","prevalence","recall","false_positive_rate","expected_true_alerts",
               "expected_false_alerts","expected_alerts","precision"], alert_rows)
    storage_rows = []
    for b in (1, 16, 256, 4096, 65_536):
        for label, size in (("Ed25519", ED25519), ("ML-DSA-65", MLDSA65)):
            n = math.ceil(RECORDS / b)
            storage_rows.append((RECORDS, b, label, n, size, REPLICAS,
                                 signature_bytes(RECORDS, b, size),
                                 signature_bytes(RECORDS, b, size, REPLICAS)))
    write_csv("signature_scenarios.csv",
              ["records","batch_size","signature","signed_objects","bytes_per_signature","replicas",
               "signature_bytes_per_replica","signature_bytes_all_replicas"], storage_rows)

    first = alert_counts(POPULATION, PREVALENCE, RECALL, Fraction(1, 100))
    second = alert_counts(POPULATION, PREVALENCE, RECALL, Fraction(1, 1_000))
    third = alert_counts(POPULATION, PREVALENCE, RECALL, Fraction(1, 10_000))
    max_fpr = (Fraction(BUDGET, POPULATION) - PREVALENCE*RECALL) / (1-PREVALENCE)
    total_hybrid = KEM_KEY + KEM_CIPHERTEXT + 2*X25519_SHARE
    difference = signature_bytes(RECORDS, 1, MLDSA65-ED25519, REPLICAS)
    batch_mldsa = signature_bytes(RECORDS, BATCH_SIZE, MLDSA65)
    proof_bytes = int(math.log2(BATCH_SIZE)) * DIGEST_BYTES
    assert first == (900, 9990, Fraction(10, 121))
    assert second[:2] == (900, 999) and third[:2] == (900, Fraction(999, 10))
    assert max_fpr == Fraction(11, 9990)
    assert total_hybrid == 2336 and difference == 22_715_000_000
    assert batch_mldsa == 810705 and proof_bytes == 384
    lines = [
        f"Python {platform.python_version()}, Matplotlib {matplotlib.__version__}, NumPy {np.__version__}",
        "Deterministic calculations. No training or experimental observations.",
        f"Precision at 1%, 0.1%, 0.01% FPR and 0.1% prevalence: "
        f"{100*float(first[2]):.4f}%, {100*float(second[2]):.4f}%, {100*float(third[2]):.4f}%.",
        f"FPR ceiling for a {BUDGET:,}-alert budget: {100*float(max_fpr):.6f}%.",
        f"X25519MLKEM768 raw client and server key-share bytes together: {total_hybrid:,}.",
        f"Additional unbatched signature bytes across seven replicas: {difference:,}.",
        f"ML-DSA-65 signature bytes per replica with 4,096-record batches: {batch_mldsa:,}.",
        f"Full 4,096-leaf binary tree sibling-hash payload: {proof_bytes} bytes.",
    ]
    (ROOT / "validation.txt").write_text("\n".join(lines)+"\n", encoding="utf-8")
    draw_architecture()
    draw_alerts()
    draw_storage()
    print("\n".join(lines))

if __name__ == "__main__":
    main()
