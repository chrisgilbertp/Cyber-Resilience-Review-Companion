#!/usr/bin/env python3
"""Reproduce analytical results for the ANI review manuscript (Section 4)."""

import csv
from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt

# Parameters from the manuscript
TPR = 0.99          # true positive rate
FPR = 0.001         # false positive rate
PREVALENCE = 1 / 10_000  # one attack in 10,000 events

# False match rates for gallery analysis
FMRS = [1e-4, 1e-6, 1e-8]  # one in 10k, 1M, 100M
GALLERY_SIZES = np.array([100, 1_000, 10_000, 100_000, 1_000_000])


def positive_predictive_value(tpr, fpr, prevalence):
    """Bayes' rule for PPV (precision) at a given prevalence."""
    numerator = tpr * prevalence
    denominator = numerator + fpr * (1 - prevalence)
    return numerator / denominator


def false_match_probability(fmr, n):
    """Probability of at least one false match in a gallery of size n."""
    return 1.0 - (1.0 - fmr) ** n


def main():
    out_dir = Path("results")
    out_dir.mkdir(exist_ok=True)

    # --- Base-rate calculation ---
    ppv = positive_predictive_value(TPR, FPR, PREVALENCE)
    print(f"Base-rate example (Section 4):")
    print(f"  TPR = {TPR}, FPR = {FPR}, prevalence = {PREVALENCE:.0e}")
    print(f"  Positive predictive value ≈ {ppv:.4f}  ({ppv*100:.1f}%)")
    print(f"  → About {ppv*100:.0f}% of alarms are true positives under these assumptions.\n")

    with open(out_dir / "base_rate.csv", "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["tpr", "fpr", "prevalence", "ppv", "ppv_percent"])
        writer.writerow([TPR, FPR, PREVALENCE, f"{ppv:.6f}", f"{ppv*100:.2f}"])

    # --- False-match probability curves ---
    print("False-match probability by gallery size (Eq. 3):")
    print(f"{'Gallery N':>12} | " + " | ".join(f"FMR={fmr:.0e}" for fmr in FMRS))
    print("-" * 60)

    rows = []
    for n in GALLERY_SIZES:
        probs = [false_match_probability(fmr, n) for fmr in FMRS]
        print(f"{n:>12,} | " + " | ".join(f"{p:8.4f}" for p in probs))
        for fmr, p in zip(FMRS, probs):
            rows.append([n, fmr, f"{p:.6f}"])

    with open(out_dir / "false_match_probabilities.csv", "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["gallery_size", "false_match_rate", "prob_at_least_one_false_match"])
        writer.writerows(rows)

    # Optional: quick plot of the curves (not required for manuscript values)
    plt.figure(figsize=(6.5, 4))
    for fmr in FMRS:
        probs = [false_match_probability(fmr, n) for n in GALLERY_SIZES]
        plt.plot(GALLERY_SIZES, probs, marker="o", label=f"FMR = {fmr:.0e}")
    plt.xscale("log")
    plt.xlabel("Gallery size N")
    plt.ylabel("P(at least one false match)")
    plt.legend()
    plt.grid(True, which="both", alpha=0.3)
    plt.tight_layout()
    plt.savefig(out_dir / "false_match_curves.png", dpi=300)
    plt.close()

    print(f"\nResults written to: {out_dir.resolve()}")
    print("Run complete. All values are direct evaluations of the formulas in Section 4.")


if __name__ == "__main__":
    main()
