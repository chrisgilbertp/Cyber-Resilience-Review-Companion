#!/usr/bin/env python3
"""Reproduce numerical scenarios and figures for Online Resource 1."""

import argparse
import csv
from math import exp, isclose, log, pi
from pathlib import Path

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import FancyArrowPatch, Rectangle
from matplotlib.ticker import LogLocator, MultipleLocator


INITIAL_CAPABILITY = 1.0
RATE_CONSTANT = 1.0
BOLTZMANN_J_PER_K = 1.380649e-23
PLANCK_J_S = 6.62607015e-34
LIGHT_SPEED_M_PER_S = 299_792_458
TEMPERATURE_K = 300.0
POWERS_W = (20.0, 1_000.0, 1_000_000.0, 1_000_000_000.0)
MASS_KG = 1.0
DOUBLING_MONTHS = (24, 20, 6)
HORIZON_MONTHS = 144

INK = "#17202A"
STYLES = ("-", "--", "-.")


def normalized_capability(time, exponent):
    """Evaluate the solution on its positive-base domain."""
    if exponent == 1.0:
        return INITIAL_CAPABILITY * np.exp(RATE_CONSTANT * time)
    power = 1.0 - exponent
    base = INITIAL_CAPABILITY**power + power * RATE_CONSTANT * time
    return base ** (1.0 / power)


def singularity_time(exponent):
    return INITIAL_CAPABILITY ** (1.0 - exponent) / (RATE_CONSTANT * (exponent - 1.0))


def write_csv(path, header, records):
    with path.open("w", encoding="utf-8", newline="") as file:
        writer = csv.writer(file, lineterminator="\n")
        writer.writerow(header)
        writer.writerows(records)


def write_scenarios(output):
    exponential_growth = [2.0 ** (HORIZON_MONTHS / d) for d in DOUBLING_MONTHS]
    singularity_times = [singularity_time(a) for a in (1.25, 1.5, 2.0)]
    erasure_energy = BOLTZMANN_J_PER_K * TEMPERATURE_K * log(2.0)
    quantum_rate = 2.0 * MASS_KG * LIGHT_SPEED_M_PER_S**2 / (pi * (PLANCK_J_S / (2.0 * pi)))

    assert exponential_growth[0] == 64.0
    assert exponential_growth[2] / exponential_growth[0] == 262_144.0
    assert singularity_times == [4.0, 2.0, 1.0]
    assert isclose(float(normalized_capability(1.0, 1.0)), exp(1.0))
    assert isclose(erasure_energy, 2.870978885078724e-21)
    assert isclose(quantum_rate, 5.4255699586085285e50)

    write_csv(output / "compute_growth.csv",
              ["elapsed_months", "doubling_months", "growth_factor"],
              [(t, d, f"{2.0 ** (t / d):.12g}")
               for d in DOUBLING_MONTHS for t in range(HORIZON_MONTHS + 1)])
    write_csv(output / "feedback_sensitivity.csv",
              ["exponent", "initial_capability", "rate_constant", "divergence_time"],
              [(a, INITIAL_CAPABILITY, RATE_CONSTANT, t)
               for a, t in zip((1.25, 1.5, 2.0), singularity_times)])
    write_csv(output / "physical_bounds.csv",
              ["quantity", "temperature_K", "power_W", "mass_kg", "value", "unit"],
              [("Landauer minimum energy", TEMPERATURE_K, "", "",
                f"{erasure_energy:.12g}", "J per bit erasure")]
              + [("Ideal irreversible bit erasure rate", TEMPERATURE_K, p, "",
                  f"{p / erasure_energy:.12g}", "bit erasures per s") for p in POWERS_W]
              + [("Lloyd ideal quantum rate", "", "", MASS_KG, f"{quantum_rate:.12g}",
                  "state transformations per s")])


def save_figure(fig, output, number):
    fig.savefig(output / f"Fig{number}.eps", format="eps")
    fig.savefig(output / f"Fig{number}.png", dpi=1200, facecolor="white")
    plt.close(fig)


def plot_scenarios(output):
    fig, (feedback, compute) = plt.subplots(1, 2, figsize=(6.65, 2.9),
                                            layout="constrained", facecolor="white")
    for exponent, style in zip((0.5, 1.0, 1.5), STYLES):
        end = 1.98 if exponent > 1.0 else 2.15
        time = np.linspace(0, end, 400)
        feedback.plot(time, normalized_capability(time, exponent),
                      style, linewidth=1.35, color=INK, label=fr"α = {exponent:g}")
    feedback.axvline(2.0, color="#606060", linestyle=":", linewidth=1.1,
                    label=r"$t^* = 2$")
    feedback.set(yscale="log", xlim=(0, 2.15), ylim=(0.9, 2e4),
                 xlabel="Normalized time", ylabel="Normalized capability")
    feedback.xaxis.set_major_locator(MultipleLocator(0.5))
    feedback.yaxis.set_major_locator(LogLocator(base=10, numticks=6))
    feedback.legend(loc="upper left", edgecolor="#8A8A8A", framealpha=1.0)

    months = np.linspace(0, HORIZON_MONTHS, HORIZON_MONTHS + 1)
    for doubling, style, marker in zip(DOUBLING_MONTHS, STYLES, ("o", "s", "^")):
        compute.plot(months / 12.0, 2.0 ** (months / doubling), style, color=INK,
                     linewidth=1.35, marker=marker, markersize=3.2,
                     markerfacecolor="white", markevery=36, label=f"{doubling} months")
    compute.set(yscale="log", xlim=(0, 12.35), ylim=(0.7, 5e7),
                xlabel="Elapsed years", ylabel="Growth factor (unitless)")
    compute.xaxis.set_major_locator(MultipleLocator(3))
    compute.yaxis.set_major_locator(LogLocator(base=10, numticks=6))
    compute.legend(loc="upper left", edgecolor="#8A8A8A", framealpha=1.0)

    for panel, letter in zip((feedback, compute), ("a", "b")):
        panel.yaxis.grid(True, which="major", color="#D3D3D3", linewidth=0.55)
        panel.set_axisbelow(True)
        panel.spines[["right", "top"]].set_visible(False)
        panel.tick_params(axis="y", which="minor", length=2)
        panel.text(0.01, 1.02, letter, transform=panel.transAxes,
                   ha="left", va="bottom", fontsize=10, weight="bold")
    save_figure(fig, output, 1)


def draw_controls(output):
    fig = plt.figure(figsize=(6.65, 3.46), facecolor="white")
    axes = fig.add_axes([0.02, 0.01, 0.96, 0.97])
    axes.set_xlim(0, 100)
    axes.set_ylim(0, 100)
    axes.axis("off")

    stages = [
        (87, "1  Specification", "Intended use and permitted access"),
        (63, "2  Training and design", "Documented controls and versions"),
        (39, "3  Evaluation", "Independent findings and criteria"),
        (15, "4  Deployment", "Authorization, monitoring, rollback"),
    ]
    for y, label, detail in stages:
        axes.add_patch(Rectangle((4, y - 9), 53, 18, facecolor="white",
                                 edgecolor=INK, linewidth=1.05))
        axes.text(7, y + 2.0, label, fontsize=10.4, weight="bold", va="center")
        axes.text(7, y - 4.0, detail, fontsize=9.3, va="center")

    def arrow(start, end, style="-|>", line="-", connection="arc3,rad=0"):
        axes.add_patch(FancyArrowPatch(start, end, arrowstyle=style, linewidth=1.1,
                                       connectionstyle=connection, linestyle=line,
                                       mutation_scale=8, color=INK, shrinkA=0, shrinkB=0))

    for upper, lower in zip(stages, stages[1:]):
        arrow((30.5, upper[0] - 9), (30.5, lower[0] + 9))

    axes.add_patch(Rectangle((67, 6), 30, 90, facecolor="#F2F2F2",
                             edgecolor=INK, linewidth=1.05))
    axes.text(82, 64, "5  Institutional\noversight", fontsize=10.25,
              weight="bold", ha="center", va="center", linespacing=1.2)
    axes.text(82, 42, "Independent sign-off\nEvidence records\nAppeal and redress",
              fontsize=9.3, ha="center", va="center", linespacing=1.45)
    for y, _, _ in stages:
        arrow((57, y), (67, y), style="<->")
    axes.plot([4, 0.8, 0.8], [15, 15, 39], color=INK, linestyle="--", linewidth=1.1)
    arrow((0.8, 39), (4, 39), line="--")
    save_figure(fig, output, 2)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, default=Path.cwd() / "reproduced")
    output = parser.parse_args().output
    output.mkdir(parents=True, exist_ok=True)
    plt.rcParams.update({
        "font.family": "Liberation Sans",
        "mathtext.fontset": "dejavusans",
        "font.size": 9.5,
        "axes.labelsize": 9.4,
        "legend.fontsize": 8.5,
        "xtick.labelsize": 8.8,
        "ytick.labelsize": 8.8,
        "text.color": INK,
        "ps.fonttype": 42,
        "ps.useafm": False,
    })
    write_scenarios(output)
    plot_scenarios(output)
    draw_controls(output)


if __name__ == "__main__":
    main()
