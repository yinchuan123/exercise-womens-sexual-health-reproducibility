# R139 source qualification process snapshot

8 November 2026. This snapshot records derived process counts. It does not
publish a manuscript, preprint, final PRISMA, independent whole-review census,
new clinical analysis or new author signatures.

## Current accounting

The combined frame contains 29,490 identified representations. An additional
38 same-published-report bibliographic aliases bring duplicates to 7,535,
leaving 21,955 canonical record groups. Conference/journal reports and
thesis/journal reports remain distinct documents when they are not the same
published report. Asset versions and original native fields remain preserved.

The current qualification assessed 1,277 previously retained source groups.
It reuses 499 specific source facts already adopted by authors to implement
current own-source screening routes. These actions do not exclude the parent
trial or assert historical retrieval dates. The 417 new source proposals map
to 415 canonical sources after identity reconciliation. They are not adopted
human judgments at this snapshot. They include proposed uses of existing
original reports, source-role corrections and protected scope differences.

Current working routes are 18,456 own-record exclusions, 2,866 author-retained
routes, 345 technical identity/source routes and 288 explicit HOLD routes.
These sum to 21,955. They are not finalized sequential PRISMA stage totals;
HOLD is not an inventory of all remaining scientific or resource limitations.
The previously adopted 99-report/98-source-family anchor is not the final
whole-search independent trial count. No new effect inputs, models or GRADE
ratings are released. Previous certainty disagreements remain preserved.

## Reproduce the process checks

Run `python3 snapshots/r139-2026-11-08/verify_snapshot.py` from the repository.
The script validates hashes, field types, count arithmetic and release limits.
It cannot reproduce private source reading or author-signature verification.
Authorized private-project users can regenerate the aggregate JSON using
`export_from_private_project.py --project /path/to/project --output /tmp/r139.json`.

The historical `v0.1.0` analysis inputs and six evaluations remain unchanged.
Their command is `python3 analysis/reproduce.py --output out`. The 22 diagnostic
fits remain separate. No raw source texts, licensed PDFs, database exports,
correspondence, signed receipts or unapproved manuscript are included here.
Code is MIT; external materials retain their original rights.
