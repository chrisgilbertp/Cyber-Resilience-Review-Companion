# Online Resource 1

**Evaluating artificial narrow intelligence from benchmarks to deployment**  
*Artificial Intelligence Review*

Chris Gilbert, Duah Jeremiah Leakpor, Kwitee D. Gaylah, John K. Constance, Maxwell Dorgbefu Jnr and Mercy A. Gilbert

**Corresponding author**  
Chris Gilbert  
Department of Computer Science and Engineering  
College of Engineering and Technology, William V. S. Tubman University  
Harper, Maryland County, Liberia  
cabilimi@tubmanu.edu.lr

## Purpose

This archive reproduces the hypothetical values in Table 2 and the quantitative plots from Eqs. (2), (4) and (5). It also provides the source for the deployment lifecycle diagram. The calculations use no operational data.

## Reproduce

Requires Python 3.10 or newer and Matplotlib (tested with 3.10.8).

```bash
python -m pip install "matplotlib>=3.7"
python reproduce.py --out results
```

The script defines the input grids at its beginning. Its outputs are fractions unless specified below. CSV files use one header row.

- `gallery_curve.csv` — Gallery sizes, comparison probabilities and probability of one or more false candidates
- `alert_curve.csv` — Prevalences, conditional rates and alert PPV
- `alert_grid.csv` — Values shown as percentages in Table 2
- `scenario_checks.csv` — Point values for the examples in the article
- Fig1–Fig3 (EPS and 1200 dpi PNG)

The gallery model assumes a nonmated probe, one template per identity, and independent comparisons with a common false match probability. Alert PPV and workload use rates for a single event definition, before alert grouping. The negative sample size example assumes independent, representative trials.

ChatGPT (OpenAI) assisted with preparing the code and Matplotlib figures.
