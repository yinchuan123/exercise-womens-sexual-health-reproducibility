from pathlib import Path
from hashlib import sha256
import json
H=Path(__file__).resolve().parent
for line in (H/'MANIFEST.sha256').read_text().splitlines():
    s,n=line.split('  ',1); assert sha256((H/n).read_bytes()).hexdigest()==s,n
a=json.loads((H/'aggregate_summary.json').read_text());g=json.loads((H/'actual_S29_target_assessments4.json').read_text())
assert a['identified']-a['duplicates']==a['screened_records']==21924
assert 21924==18827+3097 and 3099==727+2372 and 2372==213+1593+328+238
assert a['actual_S29_author_choice_cells']==12 and a['new_certainty_targets_pending_actual_author_adoption']==0
assert a['certified_whole_review_independent_K'] is None and a['unique_adult_female_N'] is None
assert len(g['rows'])==4 and g['new_pooled_fits']==0
r={v['source_id']:v for v in g['rows']}
assert r['FULL136-030']['source_parameter_certainty']=='Moderate'
assert r['FULL136-039']['source_parameter_certainty']=='Very low'
assert r['FULL136-069']['source_parameter_certainty']=='Low'
assert r['FULL136-107']['source_parameter_certainty']=='NOT_RATEABLE'
assert not a['current_full_manuscript_author_approval'] and not a['submission_authorized']
print('PASS four scoped certainty cases, finite counts and explicit K/N limits; not clinical validation or submission')
