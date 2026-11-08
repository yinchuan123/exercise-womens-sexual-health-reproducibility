from pathlib import Path
from hashlib import sha256
import json
H=Path(__file__).resolve().parent
for line in (H/'MANIFEST.sha256').read_text().splitlines():
    s,n=line.split('  ',1);assert sha256((H/n).read_bytes()).hexdigest()==s,n
a=json.loads((H/'aggregate_summary.json').read_text())
assert a['actual_S30_author_approvals']==3 and a['current_full_manuscript_author_approval']
assert not a['submission_authorized'] and not a['preprint_authorized'] and not a['submitted']
assert a['new_scientific_changes_after_S30']==0 and a['new_pooled_fits']==0
assert a['certified_whole_review_independent_K'] is None and a['unique_adult_female_N'] is None
assert a['whole_review_scientific_completeness_percent'] is None and not a['whole_review_complete']
assert a['identified']-a['duplicates']==a['screened_records']==21924
assert 3099==727+2372 and 2372==213+1593+328+238 and 238==140+98
print('PASS author-approved derived status and explicit scientific limits; no external release authorized')
