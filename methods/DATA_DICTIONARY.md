# Data dictionary

| File | Unit | Key and interpretation |
|---|---|---|
| `selection_accounting.json` | Counts across separate archive layers | Database export members, deduplicated record groups, report carriers, documented request IDs and study families use different units. Request and completeness subsets overlap. |
| `whole_review_flow_unknowns.tsv` | Whole-review stage field | `cell` identifies a requested count. An empty `value` represents a documented unknown. `status` and `reason` explain the absence. |
| `report_catalogue.csv` | Bounded catalogue report | `report_id` is a stable local study-report carrier identifier. `title` is bibliographic metadata. `catalogue_category` records the scoped report disposition. `linked_to_current_record_group` records an exact current link. `whole_review_eligibility` is empty throughout. |
| `bounded_families.csv` | Bounded study family | `bounded_family_id` links results to a source-supported family. `principal_report_ids` and `own_registry_aliases` can have pipe-delimited multiple entries. `denominator_evidence_layer` indicates the archive layer. Selected results can include descriptive or held records. |
| `source_result_ledger.jsonl` | Source result record | `result_id` identifies the result. `report_id` and `family_id` join to the corresponding public ledgers. Population, intervention, comparator, outcome, timepoint and estimator are retained as short source-linked labels. |
| `comparison_routes.csv` | Clinical comparison routing entry | `comparison_id` identifies a clinical question. `nonadditive_local_source_family_K` is scoped to that question. The source families can recur in other comparisons. No unrestricted primary pool is declared. |
| `certainty_and_models.json` | Scoped model and judgement records | `restricted_comparisons` names the three existing model comparison sets, fitted K, denominator evidence, and preserved certainty scope. `certainty_scope` gives route counts and distinguishes legacy targets from later actions. They cannot be added as independent evidence bodies. |
| `AGGREGATE_INPUTS_THREE_RESTRICTED_COMPARISONS.json` | Fitted study-level input | `yi` is the treatment-minus-control estimate on the specified scale. `vi` is its variance. When supplied, `mean_*`, `sd_*` and `n_*` are source arm summaries. `native_SE` is a source-reported standard error. |
| `EXPECTED_SIX_EXISTING_CLINICAL_FITS.json` | Existing model evaluation | Two inferential routes per comparison, with frozen estimate, 95% interval, standard error, and available heterogeneity statistics. |
| `figures/PRISMA_2020_FIGURE1_DATA.json` | Figure count cell | Shared counts and unresolved fields used by the diagram builder. |
| `methods/provenance.csv` | Public artifact binding | `source_snapshot` and its SHA-256 identify the underlying frozen private or public input. `transformation` describes how the shared artifact was derived. |

## Result fields

- `release_route` and `source_use` give the allowed interpretation of a record. Conditional, descriptive and held records stay visible without automatic model entry.
- `effect_measure`, `estimate`, `ci`, and `se` retain the documented estimate and precision. `publication_or` and `publication_or_ci` preserve source-native odds ratios when separately recorded.
- `model_n_as_source` and `observed_item_n_as_source` show only literal values from the identically named source fields when present. A blank or null can also reflect that the shared projection did not map other source-specific denominator fields. Consult the named report for exact denominators.
- `interval_origin` separates source and derived interval routes. Null means that the current projection contains no comparable interval-origin field.
- `risk_route` and `grade_route` describe how a result enters the existing assessment record. They are route labels, with no new ratings produced by the reproduction.
- Missing or held fields are retained as empty or null. They must never be counted as zero events or converted into eligibility, sample size or certainty.
