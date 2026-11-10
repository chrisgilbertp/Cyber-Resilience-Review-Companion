# Companion materials for Post-quantum migration, verifiable ledgers and AI-assisted cyber defense

The review by Chris Gilbert and Maxwell Dorgbefu Jnr uses the files in this package to document the migration example, the engineering schematic and the editorial checks.

## Reproduce Table 6

Run `python analysis/migration_order.py` from the extracted package. The script uses the Python standard library and was executed with Python 3.12.14. It generates `analysis/migration_scenarios.csv` and `analysis/validation.txt`. The scenario inputs are defined in the script. The horizons, lifetimes and lead times are in years. Lead times are estimates for the entire transition from the common planning date, including prerequisites. A blank own margin denotes a supporting task.

The checks cover priority inheritance, dependency precedence, reproducibility under reversed input order, and rejection of invalid input and cycles. The example evaluates the ordering rule on a hypothetical inventory. Applying it to an organization requires a validated inventory and schedule.

## Figure 1

`figures/Figure_1.pdf` contains the vector schematic. Regenerate it with `dot -Tpdf figures/Figure_1.dot -o figures/Figure_1.pdf` using Graphviz. The manuscript caption discloses assistance in preparing the Graphviz source.

## Editorial materials

`editorial/review_and_readiness.md` records the substantive revisions and the remaining author checks. `editorial/citation_register.tsv` maps all numbered references to their stable identifiers and citation counts. `editorial/Highlights.txt` and `editorial/Cover_Letter_Draft.txt` are drafts for the corresponding author.
