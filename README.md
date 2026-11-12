# Exercise interventions and women's sexual health

This repository documents the search, study-selection accounting, extraction
scope, certainty assessment, and aggregate statistical verification for a
focused review of exercise and exercise-containing interventions. The
[registered protocol](https://www.crd.york.ac.uk/PROSPERO/view/CRD420261549870)
covers a broader intervention question. The focused manuscript scope was
selected after some results had been seen. The dated decisions and evidence
limits are documented in [Scope changes](methods/scope_changes.txt).

## Final available-evidence report workflow

The [R209 closure](snapshots/r209-2026-11-12/README.md) executes existing actual author policies and ends acquisition/reply waiting.50cutoff dispositions have been processed; the40unclassifiable reports,8strict initial-N gaps and2suspected cohort relations remain disclosed facts, not continuing work queues. No new clinical data, effect, fit, risk/GRADE or main-manuscript approval is created. The final private report archive is prepared, while global independentK, unique femaleN, journal acceptance and compliance with every planned conduct step are not certified. No submission or preprint posting has been performed.

```sh
python3 snapshots/r209-2026-11-12/verify_final_cutoff.py
```

## Latest source-intake update

The [R208 final-source update](snapshots/r208-2026-11-12/README.md) archives three final obtainable user-supplied files privately and publishes only source facts and process metadata. Two requested original conference reports were obtained; the radiofrequency PDF is a three-page background article rather than the requested dissertation. Zhang2016 now has source-confirmed initial randomization2,700(four arms675each), compared with2,403evaluated after6weeks and297lost. Its adult eligibility and endpoint precision remain unreported. Iervolino2017 originalS37–S38 also lacks the adult age boundary and numerical FSFI precision. No new report, independent K, grand female N, quantitative input, RoB2 or GRADE is adopted. The R206 author-adopted state and R204 data remain operative. No further acquisition or reply waiting is active under the final user cutoff.

```sh
python3 snapshots/r208-2026-11-12/verify_source_intake.py
```

## Latest actual author-adopted process snapshot

The [R206 update](snapshots/r206-2026-11-12/README.md) applies three actual R205 returns for the single new Obler report-disposition question. The final author-adjudicated choice is B: retain eligibility-unascertainable at cutoff, outside the evidence core and quantitative inputs. The disclosed author adjudicator's explicit returned choice resolved the disagreement; this was not a majority-vote or AI-consensus decision. The 40 qualification, eight initial-female-N and two suspected-dependency tasks received targeted original-source reassessment, with no newly established complete eligibility, initial-N or overlap fact. The 50 targeted native-source checks were performed by AI agents, not independent duplicate human full-text readings; author returns cover the disclosed new disposition only. There are no new author questions pending in this update.

The report flow remains 3,088 sought = 499 not retrieved + 2,589 assessed, comprising 340 included (199 principal + 141 companion), 40 awaiting and 2,209 not included. There are 194 conservative reported-event groups, or 195/196 under dependency-split scenarios; each of three existing comparisons retains independent K=2. No whole-review unique female N or certified global independent K is asserted. The 499 cutoff was not reopened and no unreceived reply was used.

The [R204 data and actual result-risk snapshot](snapshots/r204-2026-11-12/README.md) remains unchanged: 279 adopted result-risk targets in 159 groups, two tool HOLDs, 70 new domain differences retained, 91 prior certainty record views and eight old GRADE differences. No clinical input, fit, effect, risk/GRADE judgment or approved manuscript was changed. The existing six-fit replay has 74 passing checks; this update does not call them a new model run. The 22 published-input diagnostic fits below remain separate.

```sh
python3 snapshots/r206-2026-11-12/verify_snapshot.py
python3 snapshots/r204-2026-11-12/verify_snapshot.py
Rscript snapshots/r204-2026-11-12/analysis/verify_existing_six_clinical_fits.R
```

[Current metadata](CURRENT_SNAPSHOT.json), [R206 review scope](snapshots/r206-2026-11-12/snapshot_meta.json), [risk positions](snapshots/r204-2026-11-12/adopted_result_risk279.json), [report dispositions](snapshots/r204-2026-11-12/report_dispositions3088.tsv), [PRISMA](snapshots/r204-2026-11-12/figures/Figure_1_PRISMA.pdf), [41-record quantitative admission audit](snapshots/r204-2026-11-12/quantitative_admission_limits41.tsv) and [cutoff limit dispositions](snapshots/r204-2026-11-12/available_evidence_limit_dispositions.tsv) are available. Earlier snapshots remain historical and immutable. The unpublished manuscript, licensed original full texts, investigator contacts, raw mail and signed author files are excluded. No journal submission or preprint has been made.

## Separate published-input diagnostic audit

The [portable diagnostic package](diagnostic-audit/published-input-2026-11-08/README.txt) preserves 11 conditional published-input scenarios and their 22 historical summaries. The 8 November engineering replay matched all 176 output fields exactly, with the independent 11-scenario numerical check also passing. This is separate from the six clinical fits: it adds no clinical trials, eligible effects, K/N or certainty ratings. Conditional source-N/dispersion alternatives remain assumptions rather than validated corrections.

## Run the historical v0.1.0 checks

Use Python 3.10 or later and R with `jsonlite` and `metafor`. The verified
environment used R 4.6.1, jsonlite 2.0.0, and metafor 5.0-1. Install the two
R packages in an appropriate local library before running.

```sh
python3 analysis/reproduce.py --output out
```

The script validates the file manifest, reproduces the available-source
accounting, and reruns six model evaluations for three comparisons. It writes
the numerical checks, result summaries and R session information under
`out/`. It should report 74 passing model checks and zero new scientific
models. For data checks without R, append `--data-only`. Add `--figure` to
rebuild the [PRISMA 2020 diagram](figures/Figure_1_PRISMA_2020.pdf) from the
same shared counts. The figure build was verified with Matplotlib 3.9.4 and
DejaVu Sans.

## Inspect the historical v0.1.0 process

1. Read the [registered scope](methods/registration.json) and
   [as-run database strategies](methods/as_run_search_strategies.txt).
2. Inspect [search and selection accounting](data/selection_accounting.json)
   and [unknown whole-review fields](data/whole_review_flow_unknowns.tsv).
   The [figure data](figures/PRISMA_2020_FIGURE1_DATA.json) record the template
   attribution and distinguish verified routes from unresolved stages.
3. Follow principal reports to [bounded family identities](data/bounded_families.csv)
   and [source result records](data/source_result_ledger.jsonl). The
   [report catalogue](data/report_catalogue.csv) records bounded dispositions.
4. Read the [clinical comparison routes](data/comparison_routes.csv) and
   [outcome-specific certainty and model scope](data/certainty_and_models.json).
5. Reproduce the aggregate analysis using [model inputs](analysis/AGGREGATE_INPUTS_THREE_RESTRICTED_COMPARISONS.json)
   and [frozen numerical targets](analysis/EXPECTED_SIX_EXISTING_CLINICAL_FITS.json).
   [Data dictionary](methods/DATA_DICTIONARY.md) and [source snapshots](methods/provenance.csv)
   document the fields and projection.

The frozen v0.1.0/R82 accounting snapshot identifies 21,866 record groups and a separate 392-report
catalogue. The bounded synthesis uses 85 principal reports from 84 families
and records 152 results, including non-causal descriptions and held values.
Its 114 awaiting-classification labels describe that historical snapshot. Later
source dispositions are documented separately in the R138 and R139 process updates. The report
catalogue does not establish a complete chronological selection sequence.
Eight whole-review flow/count fields remain unknown. Each of the three
restricted comparisons has two fitted families. None has a verified pooled
effective participant denominator. The OAB comparison is exploratory.
The existing outcome-specific GRADE entries remain scoped to their targets.

The run starts from published aggregate or review-derived data in this
repository. Recreating the original database result sets requires applicable
subscriptions and their original indexing snapshots. The code does not redo
licensed source screening, regenerate author decisions, reconstruct trial IPD,
or produce a new whole-review pooled effect. See [rights and scope](methods/RIGHTS.md)
and [provenance](methods/provenance.csv).

The [R140 source-adoption snapshot](snapshots/r140-2026-11-08/README.md) remains immutable.

The [R141 dated-source audit](snapshots/r141-2026-11-08/README.md) remains immutable.

The [R142 S26 cutoff snapshot](snapshots/r142-2026-11-08/README.md) remains immutable.

The [R143 actualS27 intake and extent snapshot](snapshots/r143-2026-11-08/README.md) is retained unchanged.

The [R144 technical snapshot](snapshots/r144-2026-11-08/README.md) remains immutable.
