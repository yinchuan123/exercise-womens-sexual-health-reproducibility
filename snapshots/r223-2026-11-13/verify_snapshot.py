#!/usr/bin/env python3
"""Public snapshot integrity only; no external sources or network access."""
from pathlib import Path
import hashlib,json,re
P=Path(__file__).resolve().parent
m=json.loads((P/'PUBLIC_MANIFEST.json').read_text())
expected={'README.md','approval_aggregate.json','snapshot_meta.json','verify_snapshot.py'}
assert {r['path'] for r in m['files']}==expected
for r in m['files']:
 p=P/r['path'];assert p.is_file() and hashlib.sha256(p.read_bytes()).hexdigest()==r['sha256'],r['path']
a=json.loads((P/'approval_aggregate.json').read_text());s=json.loads((P/'snapshot_meta.json').read_text())
assert a['anonymous_author_count']==3 and a['all_three_approved_bound_version']
assert a['bound_scientific_asset_count']==117 and a['ordered_asset_row_comparisons']==351
assert a['returned_version_options']==dict(A_approve_bound_version=3,B_request_revision=0,C_do_not_approve_yet=0)
assert s['frozen_evidence_boundaries']['whole_review_independent_K'] is None
assert s['frozen_evidence_boundaries']['whole_review_unique_female_N'] is None
for d in (a,s):
 for k in ('formal_submission_authorized','formal_submission_performed','preprint_authorized','preprint_published','scientific_fact_closure_certified','bmj_readiness_certified'):assert d[k] is False,k
text='\n'.join((P/n).read_text() for n in expected)
assert re.search(r'/(?:Users|Volumes)/',text) is None
assert re.search(r'[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}',text) is None
print(json.dumps(dict(status='PASS_SNAPSHOT_INTEGRITY_ONLY',files_checked=4,new_science_verified=False,submission_authorized=False)))
