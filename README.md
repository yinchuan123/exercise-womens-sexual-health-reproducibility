# Exercise interventions and women's sexual health

This repository documents the search, study-selection accounting, extraction
scope, certainty assessment, and aggregate statistical verification for a
focused review of exercise and exercise-containing interventions. The
[registered protocol](https://www.crd.york.ac.uk/PROSPERO/view/CRD420261549870)
covers a broader intervention question. The focused manuscript scope was
selected after some results had been seen. The dated decisions and evidence
limits are documented in [Scope changes](methods/scope_changes.txt).

## Latest aggregate process update

The [R147 author-approved status snapshot](snapshots/r147-2026-11-08/README.md) records that three actual final-manuscript approvals have been verified. Scientific files are unchanged; only administrative delivery-status notes were refreshed. This is not complete whole-review eligibility, certified independent K/unique female N, or authorization for preprint publication or journal submission. The bounded delivery checklist is complete and all disclosed source limits remain.

```sh
python3 snapshots/r147-2026-11-08/verify_snapshot.py
```

The [R146 scoped certainty snapshot](snapshots/r146-2026-11-08/README.md) and its saved-decision replay remain immutable. Its then-pending full-manuscript approval status is superseded only by this new snapshot; its scientific data are unchanged.

Earlier snapshots remain available: [R138](snapshots/r138-2026-11-08/README.md) and [R139](snapshots/r139-2026-11-08/README.md).

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

## Follow the process

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
