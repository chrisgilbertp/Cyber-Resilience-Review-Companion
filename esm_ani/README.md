# Online Resource: Artificial Narrow Intelligence Review

Reproducibility materials for the narrative review:

**Artificial narrow intelligence in practice: a review of methods, applications, engineering limits and governance**

Authors: Chris Gilbert, Duah Jeremiah Leakpor, Kwitee D. Gaylah, John K. Constance, Maxwell Dorgbefu Jnr, Mercy A. Gilbert

## Contents

- `reproduce.py` — Regenerates the base-rate (Bayes) results and the false-match probability curves described in Section 4.
- `results/` — Output CSV files produced by the script (created on first run).

## Reproduce

Requires Python 3.8+ with NumPy and Matplotlib.

```bash
python -m pip install numpy matplotlib
python reproduce.py
```

The script writes CSV files to `results/` and prints the key numerical values reported in the manuscript. No external data are required. All calculations use the exact formulas and parameters given in Section 4 of the paper.

## Notes

- The base-rate example uses a true positive rate of 0.99, false positive rate of 0.001, and prevalence of 1/10,000.
- The false-match curves use the formula \(1 - (1 - \text{FMR})^N\) for gallery sizes up to 1,000,000 and the three false-match rates stated in the paper.
- Figures in the manuscript were generated from these calculations (and Graphviz for the task-family diagram).

Generated values are analytical scenarios; no observed operational data are included.
