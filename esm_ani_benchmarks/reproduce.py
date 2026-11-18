"""Reproduce Table 2 and Figs. 1–3 for the ANI review.

Evaluating artificial narrow intelligence from benchmarks to deployment
Artificial Intelligence Review
Chris Gilbert, Duah Jeremiah Leakpor, Kwitee D. Gaylah, John K. Constance,
Maxwell Dorgbefu Jnr and Mercy A. Gilbert
Correspondence: Chris Gilbert, William V. S. Tubman University, Liberia
cabilimi@tubmanu.edu.lr
"""

from argparse import ArgumentParser
import csv
import math
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
from matplotlib import pyplot as plt
from matplotlib.lines import Line2D
from matplotlib.patches import FancyArrowPatch, Rectangle
from matplotlib.ticker import PercentFormatter


TRUE_POSITIVE_RATE = 0.99
FALSE_POSITIVE_RATES = (1e-2, 1e-3, 1e-4)
FALSE_MATCH_PROBABILITIES = (1e-4, 1e-6, 1e-8)
PREVALENCE_DENOMINATORS = (10, 100, 1_000, 10_000, 100_000)
GALLERY_SIZES = sorted({round(10 ** (6 * i / 350)) for i in range(351)})
PREVALENCES = [10 ** (-6 + 5 * i / 350) for i in range(351)]
LINE_STYLES = ("-", "--", "-.")

plt.rcParams.update({
    "axes.spines.right": False,
    "axes.spines.top": False,
    "font.family": "DejaVu Sans",
    "font.size": 9.5,
    "mathtext.fontset": "dejavusans",
    "ps.fonttype": 42,
    "pdf.fonttype": 42,
})


def gallery_probability(size, comparison_probability):
    """Exact probability for independent comparisons, evaluated stably."""
    return -math.expm1(size * math.log1p(-comparison_probability))


def score_alerts(prevalence, true_positive_rate, false_positive_rate, event_count):
    """Calculate alert precision and the expected counts at a fixed threshold."""
    positive_alerts = event_count * prevalence * true_positive_rate
    negative_alerts = event_count * (1 - prevalence) * false_positive_rate
    total_alerts = positive_alerts + negative_alerts
    return positive_alerts / total_alerts, positive_alerts, negative_alerts, total_alerts


def write_csv(output, stem, headers, rows):
    with (output / f"{stem}.csv").open("w", newline="", encoding="utf-8") as handle:
        writer = csv.writer(handle, lineterminator="\n")
        writer.writerow(headers)
        writer.writerows(rows)


def format_plot(ax, xlabel, ylabel, legend_title, legend_location):
    ax.set(xscale="log", xlabel=xlabel, ylabel=ylabel, ylim=(0, 1.01))
    ax.yaxis.set_major_formatter(PercentFormatter(xmax=1, decimals=0))
    ax.grid(axis="y", color="0.82", linewidth=0.55)
    ax.legend(title=legend_title, frameon=True, facecolor="white",
              edgecolor="0.8", framealpha=1, loc=legend_location, handlelength=2.6)


def save_figure(figure, output, stem):
    figure.savefig(output / f"{stem}.eps")
    figure.savefig(output / f"{stem}.png", dpi=1200, facecolor="white")
    plt.close(figure)


def draw_gallery(output):
    rows = []
    fig, ax = plt.subplots(figsize=(6.65, 3.05), layout="constrained")
    for probability, style in zip(FALSE_MATCH_PROBABILITIES, LINE_STYLES):
        values = [gallery_probability(size, probability) for size in GALLERY_SIZES]
        ax.plot(GALLERY_SIZES, values, style, color="0.15", linewidth=1.35)
        rows.extend((size, f"{probability:.0e}", f"{value:.12g}")
                    for size, value in zip(GALLERY_SIZES, values))
    format_plot(ax, "Gallery size", "Probability of at least one false candidate",
                "False match probability", "upper left")
    save_figure(fig, output, "Fig1")
    write_csv(output, "gallery_curve", ["gallery_size", "false_match_probability", "prob_at_least_one"], rows)


def draw_alerts(output):
    rows = []
    fig, ax = plt.subplots(figsize=(6.65, 3.05), layout="constrained")
    for rate, style in zip(FALSE_POSITIVE_RATES, LINE_STYLES):
        values = [score_alerts(prevalence, TRUE_POSITIVE_RATE, rate, 1)[0] for prevalence in PREVALENCES]
        ax.plot(PREVALENCES, values, style, color="0.15", linewidth=1.35)
        rows.extend((f"{prevalence:.12g}", f"{rate:.0e}", f"{value:.12g}")
                    for prevalence, value in zip(PREVALENCES, values))
    format_plot(ax, "Event prevalence", "Alert positive predictive value",
                "False positive rate", "lower right")
    save_figure(fig, output, "Fig2")
    write_csv(output, "alert_curve", ["prevalence", "false_positive_rate", "ppv"], rows)


def write_grid_and_checks(output):
    grid_rows = []
    for denominator in PREVALENCE_DENOMINATORS:
        prevalence = 1 / denominator
        for rate in FALSE_POSITIVE_RATES:
            ppv, _, _, _ = score_alerts(prevalence, TRUE_POSITIVE_RATE, rate, 1)
            grid_rows.append([denominator, f"{rate:.0e}", f"{ppv * 100:.1f}"])
    write_csv(output, "alert_grid", ["prevalence_denominator", "false_positive_rate", "ppv_percent"], grid_rows)

    checks = [
        ["Gallery N=10000, q=1e-6", f"{gallery_probability(10000, 1e-6):.6f}", "Eq. (2)"],
        ["Gallery N=1000000, q=1e-6", f"{gallery_probability(1000000, 1e-6):.6f}", "Eq. (2)"],
        ["Alert PPV prevalence 1/10000, TPR 0.99, FPR 0.001", f"{score_alerts(1/10000, 0.99, 0.001, 1)[0]:.6f}", "Eq. (4)/(5)"],
    ]
    write_csv(output, "scenario_checks", ["quantity", "value", "equation"], checks)


def draw_lifecycle(output):
    fig = plt.figure(figsize=(6.65, 3.4), facecolor="white")
    ax = fig.add_axes([0.02, 0.02, 0.96, 0.96])
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 100)
    ax.axis("off")
    stages = [
        (12, 72, "1  Specify decision\nand operating limits"),
        (38, 72, "2  Select evaluation\nunit and threshold"),
        (64, 72, "3  Estimate operating\nconditions"),
        (12, 28, "4  Monitor and\nreassess"),
        (38, 28, "5  Document changes\nin use"),
        (64, 28, "6  Update evidence\nor restrict use"),
    ]
    for x, y, text in stages:
        ax.add_patch(Rectangle((x, y), 22, 18, facecolor="white", edgecolor="0.15", linewidth=1.0))
        ax.text(x + 11, y + 9, text, ha="center", va="center", fontsize=8.5, linespacing=1.25)
    for (x1, y1, _), (x2, y2, _) in zip(stages, stages[1:]):
        if y1 == y2:
            ax.add_patch(FancyArrowPatch((x1 + 22, y1 + 9), (x2, y2 + 9), arrowstyle="-|>", mutation_scale=8, color="0.15", linewidth=1.0))
        else:
            ax.add_patch(FancyArrowPatch((x1 + 11, y1), (x2 + 11, y2 + 18), arrowstyle="-|>", mutation_scale=8, color="0.15", linewidth=1.0))
    save_figure(fig, output, "Fig3")


def main():
    parser = ArgumentParser(description=__doc__)
    parser.add_argument("--out", type=Path, default=Path("results"))
    output = parser.parse_args().out
    output.mkdir(parents=True, exist_ok=True)
    draw_gallery(output)
    draw_alerts(output)
    write_grid_and_checks(output)
    draw_lifecycle(output)
    print(f"Wrote results to {output.resolve()}")


if __name__ == "__main__":
    main()
