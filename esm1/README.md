# Online Resource 1
## Quantum Computing and Artificial Intelligence in Learning and Device Engineering

**Journal:** Quantum Machine Intelligence  
**Authors:** Chris Gilbert and Maxwell Dorgbefu Jnr  

### Files
- `build_figures.py` generates the five figures.
- `alphaqubit_sycamore.csv` records the ten decoder estimates, the uncertainties in percentage points and the source panels. The CSV starts with article metadata in lines beginning with #.

### Reproduce the figures
Extract the archive and run the following commands from that folder. Install Liberation Sans to reproduce the lettering.

```bash
python -m pip install numpy matplotlib pillow
python build_figures.py
```

The script writes 650 dpi RGB PNG and vector EPS files to `figures/`. The manuscript exports were generated with Python 3.12.14, NumPy 2.3.5, Matplotlib 3.10.8 and Pillow 13.0.0.

### Figure provenance
Figures 1 and 4 show engineering workflows. Figures 2 and 3 plot the stated analytical models. The script checks selected values for kernel acquisition, raw memory and gradient workloads.

Figure 5 uses values replotted from Bausch et al. (2024), Nature 635, 834–840, Fig. 3a and b. The source article is licensed under CC BY 4.0. https://doi.org/10.1038/s41586-024-08148-8

OpenAI ChatGPT assisted with the figure-generation code. The script and input table make the figure outputs reproducible.
