# R138 aggregate process snapshot — 8 November 2026

This is a process update, not a manuscript, preprint, final PRISMA flow,
new set of independent trials, or new clinical analysis. The summary contains
only review-derived aggregate counts and explicit limitations. It does not
contain source abstracts, database exports, licensed PDFs, correspondence,
individual author choices, signatures or review receipts.

## What changed

The source framework contains 29,490 identified representations. Removing
7,497 duplicates leaves 21,993 current record groups. There were 2,117 new
record-screen dispositions, comprising 2,007 reused specific source dispositions
and 110 new source-role projections. One prior exclusion was superseded by an
actual source-scope decision, so the net increase in that working exclusion
route was 2,116. These are technical record routes, not finalized sequential
PRISMA stages or exclusions of 2,117 independent trials.

Three actual author receipts contain 27 top-level choices. Their embedded
153-row and 18-row vectors are source actions, not additional independent
human original-report readings. The applied procedure retains two-reviewer
agreement and uses the named adjudicator's actual source-specific action only
for their unresolved differences. Dissent remains visible in the private audit.
No discussion record or independent duplicate human original reading is inferred.

Twenty-five source-use actions comprise 18 limited whole-package narrative
uses, four nonrandom or mixed-assignment restrictions, two companion/protocol
uses, and one carrier without its own target sexual result. The 18 uses do not
establish 18 new independent studies. The previously adopted anchor remains
99 result reports in 98 source-supported family groups; this is not the final
whole-search independent census. New source components and native precision
candidates have not been released as model inputs or certainty ratings.

## Reproduce the public checks

Use Python 3.10 or later; this snapshot needs only the standard library.

```sh
python3 snapshots/r138-2026-11-08/verify_snapshot.py
```

This validates local file hashes and arithmetic/boundary relationships. It does
not reproduce screening from licensed databases, independently verify private
signatures, or refit models. To regenerate the same whitelisted fields from the
private project, where authorized access to those files exists:

```sh
python3 snapshots/r138-2026-11-08/export_from_private_project.py --project /path/to/private/project --output /tmp/r138_aggregate_summary.json
```

The original v0.1.0 model inputs and six historical evaluations remain unchanged.
Their separate entry point is `python3 analysis/reproduce.py --output out`.
Do not relabel those frozen numerical checks as an R138 primary analysis.

## Fields and rights

`schema.json` defines the aggregate fields. `null` for whole-review K/N means
not established, not zero. A working HOLD count does not include every report-
identity, extractability or independence limitation. A retained record is not
an included efficacy report; a registry without grouped results is not an
excluded trial. No unresolved values have been filled from recruitment N.

The original code in this snapshot is provided under the repository MIT
license. External study materials retain their original rights and are absent
from this export. No new whole-review GRADE, manuscript publication, preprint,
or journal submission is claimed.
