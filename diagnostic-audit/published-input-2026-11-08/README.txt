Historical published-input diagnostic audit

This package contains 11 named scenarios, two algorithms per scenario, and 22 frozen numeric fit summaries from the 29 October 2026 audit. Every historical fit summary has been located and bound to its actual source artifact. The 8 November 2026 portable engineering replay ran the same 22 scenario-model combinations: all 176 numerical output fields matched the frozen summaries exactly, and the 2,431 numerical input fields reconciled. The independent scalar-REML check also passed all 11 scenarios under its original tolerances. This replay adds zero unique scientific models.

These calculations diagnose sensitivity of a published figure's aggregate arithmetic. They are not the current review clinical dataset, 22 trials, or 22 independent clinical syntheses. Shared controls, overlapping reports, incompatible scoring, displayed dispersion and time-clock problems remain. Removing a row in a diagnostic calculation does not exclude its trial clinically. The first seven scenarios and four later post hoc source-followup scenarios retain their original disclosure. Their N/SD alternatives are conditional assumptions, not validated final corrections. No clinical eligibility, independent K/N, effect-input admission, RoB2, GRADE or author signature follows. The three restricted clinical questions and their six clinical fits are a separate package and remain unchanged. The source19 archive's 48 Bayesian sampler-diagnostic objects are also separate and have not been renamed as these 22 runs.

Included files
- data/PUBLISHED_FIGURE_ROWS_REUSED.json: 18 transcribed aggregate rows, expressly not validated trial inputs.
- data/IMPACT_AUDIT_PLAN.json: the 11 scenario definitions, changes and limits.
- data/FROZEN_PUBLISHED_INPUT_IMPACT_AUDIT.json: the 22 historically saved numeric summaries, unchanged.
- data/SCENARIO_INPUTS11.json: actual per-scenario numeric inputs.
- data/INDEPENDENT_TRANSCRIBED_REFERENCE_ROWS.json: the separate legacy figure transcription for the independent numerical check.
- scripts/run_impact_audit.R: the original R/metafor estimation loop, with filesystem-only portability edits.
- scripts/independent_impact_check.py: the original independent arithmetic and scalar-REML check, with filesystem-only portability edits.
- scripts/verify_frozen_replay.py: comparison of the frozen and replayed summaries.
- qa/: safe archived independent check, original session, and mathematical-block preservation check.
- replay/: this actual engineering replay and verification outputs; frozen historical outputs are not overwritten.

To replay using existing software (R, metafor and jsonlite; Python 3 standard library), run from this package directory:
  Rscript scripts/run_impact_audit.R .
  python3 scripts/independent_impact_check.py
  python3 scripts/verify_frozen_replay.py
No software installation or network access is performed. Numerical solver differences on another software version are assessed using the explicit verifier tolerances; a prepared script alone is not evidence of successful execution.

No licensed full text, source figure image, abstract/registry prose, manuscript, email/correspondence, author receipt or private absolute user path is distributed here. The manifest and SHA256SUMS bind this safe process snapshot. Current author-review and submission approval remain separate.
