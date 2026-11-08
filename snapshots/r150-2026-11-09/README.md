# R150: actual S31 source dispositions and current source accounting

This snapshot applies 164 actual S31 source-use decisions after three saved
receipts were checked against the frozen question/source packet. Only aggregate
receipt validation is disclosed here. It does not publish individual signatures,
notes, correspondence, or private disclosures. No author decision is inferred
from an AI recommendation.

The source actions concern 161 own-report roles and three qualified clinical
sources: Bergman (PFMT versus surgical repair of a poorly healed perineal tear),
Reese (a complete couples programme for localized breast-cancer survivors), and
SHIFT (the complete app strategy plus common clinical care). They do not release
new clinical numbers, risk ratings, certainty grades, or pooled models. A separate
Reese journal report was linked to an existing registry record, and an existing
protocol was obtained; neither event creates a historical database hit. Eleven
additional narrow roles and report links reuse existing decisions or document
current source type without another author signature.

## Reproducible count layers

* 29,490 identified records comprise 17,574 database, 10,937 trial-register and
  979 other-source records. Removing 7,566 duplicate representations leaves
  21,924 screened record groups: 18,827 record exclusions and 3,097 advanced
  groups. The distinct report accounting is 3,097 + 3 already-held reports + 1
  newly linked distinct journal report - 2 same-publication aliases = 3,099.
* Of 3,099 report nodes, required material is not retrieved for 725. The 2,374
  available reports partition into 339 own-source exclusions, 1,650 protocol or
  associated carriers without current target results, 126 awaiting classification,
  and 259 included reports (143 selected result sources plus 116 companions).
* 143 selected result sources map to 139 conservative source-identity/dependency
  groups. Splitting the two potentially overlapping Yun reports would give 140
  groups. These are source-accounting groups, not clinical pooled K.
* Reported female allocation or index-cohort N contributes 15,833 across 135
  source groups; four initial source counts remain unknown. This subtotal is not
  deduplicated women, sexual-outcome observed N or an effective analysis N.
  Excluding the 375-woman Look AHEAD index cohort gives 15,458. Also excluding
  Gouveia's conflicted 14-methods versus 32-abstract count gives 15,444.
* Available-source disposition closure is 2,248/2,374 = 94.6925%. This measures
  one workflow. It is not the completion percentage of the whole study.

`report_dispositions3099.tsv` publishes a whitelist of bibliographic metadata,
current source stages and family identifiers. Report-level exclusion does not
exclude the mother trial or imply that a sexual outcome was never measured.
`source_families139.tsv` retains the source N types and conservative within-family
counting policy. Companion reports do not create independent trials or new N.
`actual_S31_scope_actions164.tsv` records source identifiers/actions/stages only,
without individual author selections or notes.

## Work not approved or completed by this snapshot

Twenty new S32 scientific judgments remain pending: 17 own-report source-use
questions and three result-specific RoB2 plans. They have not been applied.
The previous eight GRADE disagreements remain visible in the private scientific
work. Six clinical model fits across three bounded comparisons (K=2 each) are
unchanged. Twenty-two historical diagnostic fits remain a separate audit and
are not additional clinical comparisons. No network, dose-response or large-K
claim is created by the source census. Whole-review independent K, unique female
N, final PRISMA and final GRADE are not certified; the manuscript is not
submission ready and has not been submitted.

Run `python3 snapshots/r150-2026-11-09/verify_snapshot.py` from the repository root,
or execute the verifier from any directory. It checks the manifest and recomputes
these partitions and the reported source-N sum entirely from this snapshot. Its
pass demonstrates finite arithmetic/file integrity, not clinical validity or
completion of independent human screening.

The earlier [R149 snapshot](../r149-2026-11-09/README.md) remains unchanged.
Licensed full texts, exported or verbatim abstracts, raw database exports,
individual author receipts, private ICMJE disclosures and the unpublished
manuscript are not included. This local payload does not itself publish to GitHub.
