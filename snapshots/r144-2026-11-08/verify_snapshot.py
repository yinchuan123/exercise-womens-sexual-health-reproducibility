# SPDX-License-Identifier: MIT
from pathlib import Path
from hashlib import sha256
import json,csv,collections
P=Path(__file__).resolve().parent
for line in(P/'MANIFEST.sha256').read_text().splitlines():
 d,n=line.split('  ',1);p=P/n;assert p.resolve().is_relative_to(P) and not p.is_symlink();assert sha256(p.read_bytes()).hexdigest()==d,n
x=json.loads((P/'aggregate_summary.json').read_text());r=x['record_framework'];t=x['terminal_counts'];assert r['records_identified']-r['duplicates_removed']==r['records_screened']==21924
assert r['records_screened']==r['records_excluded_at_record_phase']+r['record_groups_advanced_to_report_or_resource_assessment']
assert x['reports_sought']==sum(t.values())==3099 and x['available_assessed']+t['not_retrieved']==3099
assert t['included_reports']==125+96 and x['actual_S27_cases']==41 and x['actual_S27_choice_cells']==123 and x['S27_pending']==0
with(P/'current_report_identity_and_stage3099.tsv').open()as f:rr=list(csv.DictReader(f,delimiter='\t'))
assert len(rr)==len({r['canonical_own_report_id']for r in rr})==3099
a=json.loads((P/'verified_same_own_record_and_report_aliases.json').read_text());assert len(a['record_alias_to_canonical'])==16 and len(a['own_report_alias_to_canonical'])==16
assert not x['new_clinical_candidates_or_independent_AI_recommendations_applied']and not x['submission_ready']and x['unique_adult_female_N']is None
print(json.dumps({'status':'PASS_VERIFIED_TECHNICAL_IDENTITIES_CURRENT_SOURCE_CUTOFF','reports':3099,'actual_S27_pending':0,'new_clinical_models':0,'whole_review_eligibility_final':False}))
