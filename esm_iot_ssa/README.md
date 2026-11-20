# Additional file 1

Evidence register and numerical checks for *Internet of Things deployment and learning evidence in sub-Saharan African higher education: a critical narrative review*.

## Contents

- `study_register.csv` records each publication’s country, study setting, primary design, application domain, DOI, consulted source, endpoint and interpretation limits. Kenya denotes the participating Kenyan institution in a multinational project. Each row contributes one count.
- `verification_queries.csv` records the DOI-centred source checks run on 20 November 2026. These searches verified selected publications during revision. The original discovery and screening records are incomplete.
- `revision_source_checks.csv` gives claim locations, source access and the results of the additional citation checks. The access checks in the manuscript apply to the simulation and the learning comparison based on rounded outcomes from an abstract. The `consulted_source` column records source access for every publication.
- `numerical_inputs.json` identifies the publicly reported aggregate values and the manuscript’s illustrative buffer assumptions. Kwateng and Leong’s inconsistent group sizes prevented numerical effect extraction. The six domain values from the Nigerian laboratory paper were unavailable for independent extraction.
- `reproduce.py` calculates the counts, two access sensitivity checks, descriptive contrasts and the outage example. It can also regenerate numerical counterparts to Figures 1 and 3.
- `results/checks.json` and the two PNGs are outputs from executing the script. Figure 2 in the manuscript is a conceptual diagram of the proposed gateway and evaluation workflow.

## Run the checks

Unzip this archive. In the directory containing `reproduce.py`, run `python3 reproduce.py` to regenerate the numerical results. For the plots, use `python3 reproduce.py --plots`. Plotting requires Matplotlib 3.8 or newer. The script uses the Python standard library for the tabular results.

The first sensitivity check removes the repository-only simulation. The second additionally removes the learning evaluation for which the publisher’s abstract supplied the means. The checks describe the selected publications and their accessible source material. All inputs are study-level or illustrative values.
