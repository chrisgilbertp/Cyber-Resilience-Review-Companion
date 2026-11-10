# Companion materials for Quantum Computing, Blockchain, and Artificial Intelligence for Cyber Resilience

The editable manuscript contains 122 numbered references, including six works identified on Chris Gilbert’s ResearchGate profile. These materials document the targeted review searches, connect the principal technical claims to source records, and reproduce the figures and analytical scenarios.

## Evidence and use

- `records/source_register.tsv` maps each reference number to bibliographic details, a stable record, the evidence type, and its locations in the manuscript.
- `records/search_record.txt` records the query families, discovery services, search date, and scope.
- `records/claim_checks.tsv` records checks for the central technical claims and numerical inputs.
- `records/unicode_inspection.json` records inspection of the manuscript source text. The document check covered the text in the Word package and preserved meaningful punctuation, names, and mathematical characters.
- `analysis/validation.txt` reports the executed numerical checks and runtime versions.
- `figures/` contains the three vector PDF figures.

The corpus includes primary studies, syntheses, technical reports, final specifications, and explicitly labelled preprints. The critical integrative design compares evidence and assumptions across these categories. Coverage reflects targeted selection and accessible source records. The claim checks distinguish standard sizes and analytical results from prospective deployment tests. The profile papers provide application context in quantum cryptography, blockchain, IoT detection, graph-based detection, and homomorphic encryption.

## Reproduce the analysis

Run `python analytical_examples.py` from the `analysis` folder. The recorded execution used Python 3.12.14, NumPy 2.3.5, and Matplotlib 3.10.8. The program regenerates the two CSV files, the validation output, and the three figures in PNG, PDF, and SVG. It uses exact rational arithmetic for the alert examples, integer counts for signature storage, and a deterministic grid for plotted sensitivities.

| Scenario | Inputs | Output and scope |
|---|---|---|
| Alert precision | 1,000,000 events, 90% recall, assumed prevalences of 0.01%, 0.1%, and 1%. The table uses false-positive rates of 0.01%, 0.1%, and 1%. | `alert_scenarios.csv` gives expected true alerts, false alerts, total alerts, and precision. Input rates and precision are fractions. The 2,000-alert budget assumes the same volume and 0.1% prevalence. |
| Signature storage | 1,000,000 records, 7 complete replicas, 64-byte Ed25519 signatures, 3,309-byte ML-DSA-65 signatures, and one signature per record or batch. | `signature_scenarios.csv` gives signature counts and bytes per replica and across all replicas. MB and GB are decimal. Payloads, proofs, certificates, metadata, traffic, and runtime are separate costs. |
| Merkle proof size | Full binary tree with 4,096 leaves and 32-byte digests. | The 384-byte result counts 12 sibling hashes. A partial batch or a different tree encoding can change the path. |
| Hybrid TLS key-share sizes | RFC 10024 X25519MLKEM768 client and server key shares. | The 2,336-byte result covers the two raw key-share values. |

All examples are calculated from the stated inputs. Their relevance to a particular deployment depends on measuring the actual workload, implementation, and threat conditions.

## Submission status

The manuscript is ready for author review. Confirm the byline, affiliations, corresponding author, contributions, funding, competing interests, and journal-specific AI disclosure before submission. The current document uses numbered references and a general engineering review format.

*Computer Science Review* is a scope candidate because its publisher describes a remit for research surveys and expository reviews in computer science. Its print ISSN is 1574-0137. Confirm current indexing, metric category and quartile with the relevant issuer, and check the venue’s current author instructions and publication route before formatting for submission. Scope was checked on 10 November 2026. [Publisher record](https://shop.elsevier.com/journals/computer-science-review/1574-0137)
