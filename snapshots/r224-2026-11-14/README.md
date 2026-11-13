# R224 presentation and input-scope snapshot

This additive snapshot reproduces four figures from already adopted numerical inputs. It does not publish or approve a manuscript, preprint or journal submission. It contains no new model fit, source-eligibility decision or GRADE judgement. Earlier snapshots are unchanged.

## Rebuild in an independent directory

Use Python 3.12 with the tested versions in `requirements.txt`:

```sh
python -m pip install -r requirements.txt
python scripts/build_figures.py
python scripts/verify_rebuild.py
```

Outputs are written locally to `figures/`, `plot_data/` and `qa/`. They are generated results, not required source inputs. The code uses only this directory's `inputs/`; it does not require the authors' project tree, licensed full texts, manuscripts or external drives. Normalise expected PDF text for line-ending differences; exact text and parsed plot-input values are checked. PDF binary metadata can differ between runs and is not claimed byte-identical.

## Evidence hierarchy

The main clinical synthesis distinguishes the woman's condition, complete assigned strategy, actual comparator, outcome and source assessment clock. No unrestricted confirmatory primary meta-analysis was established. Figure 2 shows five selected adopted source-level outcomes, not an exhaustive set of primary eligible outcomes or five independent trials. Correlated Morin and eSense outcomes retain their shared family; native scales are not merged into a common effect. Active-comparator, null and uncertain findings remain in the full clinical map and journal material; selected displays do not establish programme superiority across populations.

All additional total-score and domain meta-analyses are result-informed and exploratory. Figure 3 has five overlapping sets. Figure 4 reuses the same three families for all six domains. Source-denominator sums are not certified effective model N or unique review-wide female N. GRADE applies to exact adopted targets; it is not a studywide label and is not transferred to other sensitivity views. Existing numerical models, priors and diagnostics remain in `../r222-2026-11-13/`.

The conditional pain network is an assumption stress test, not a validated treatment ranking. The eight-source prescription map does not establish a common dose-response efficacy curve or optimal dose. Neither is refitted here.

## Count and membership boundaries

At the fixed evidence cutoff: 340 included reports describe194 conservatively grouped reported strategies;40 reports have unascertainable eligibility and499 were not retrieved at the required extent. Eight groups have initial-female-denominator gaps and two pairs have suspected cohort dependency. The review-wide independent trial K and unique female N remain uncertified. Alternative grouping scenarios are not independent-trial certifications.

`inputs/current_input_scope_bridge.json` publishes only exact identifier-intersection counts and the actual numerical-input family IDs. The50terminal questions did not supply newly resolved source facts. Empty current-ID intersections do not prove absence of biological or historical overlap. The bridge does not fill missing ages, Ns, eligibility, variances or participant identities and is not a new human-reading record.

## Files and provenance

- `inputs/quantitative_targets11.json`: minimal actual fields used by the score figures, projected from adopted matrices.
- `inputs/clinical_targets5.json`: exact adopted grade-display links; published/frozen effect constants stay unchanged in the figure code.
- `inputs/cutoff_counts.json`: scientific count fields projected unchanged from the approved S1count snapshot.
- `inputs/source_attribution.json`: original source hashes, publication identifiers and interpretation boundaries, without private local paths.
- `inputs/current_input_scope_bridge.json`: current input families and intersection counts only.
- `expected/*_PDF_TEXT.txt`: text extracted from the source figure PDFs for portable verification.
- `verification/PORTABLE_REBUILD_QA.json`: actual independent-directory rebuild result; no statistical refit.
- `PUBLIC_MANIFEST.json`: hashes of this public source snapshot.

No unapproved manuscript, submission letter, author receipt, signature, correspondence, licensed full text or proprietary database export is included. AI-assisted presentation and source accounting do not attest independent duplicate human reading or author approval. This process release is not preprint publication or formal journal submission.
