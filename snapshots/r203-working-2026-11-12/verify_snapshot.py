from pathlib import Path
from collections import Counter
import csv,json,hashlib
R=Path(__file__).resolve().parent
manifest=json.loads((R/'MANIFEST_SHA256.json').read_text())
for f in manifest['files']:
 p=R/f['path'];assert p.is_file() and hashlib.sha256(p.read_bytes()).hexdigest()==f['sha256'],f['path']
c=json.loads((R/'aggregate_counts.json').read_text())
with (R/'report_dispositions3088.tsv').open(newline='') as h:rows=list(csv.DictReader(h,delimiter='\t'))
assert len(rows)==3088
d=Counter(x['disposition'] for x in rows)
assert d['INCLUDED_PRINCIPAL_RESULT_REPORT']==199
assert d['INCLUDED_COMPANION_REPORT_NO_ADDITIONAL_TRIAL']==141
assert d['AWAITING_CLASSIFICATION_AT_FINAL_EVIDENCE_CUTOFF']==40
assert d['NOT_RETRIEVED_AT_FIXED_CUTOFF']==499
assert d['EXCLUDED_WITH_EXISTING_SOURCE_REASON']==508
assert d['PROTOCOL_OR_OTHER_NONCONTRIBUTING_REPORT_CONTEXT']==1701
assert 29491==17574+10937+980 and 29491-7566==21925 and 21925-18827==3098
assert 3098-1+4-13==3088 and 3088==499+2589 and 2589==2209+40+340 and 340==199+141
groups={x['conservative_reported_event_group'] for x in rows if x['disposition']=='INCLUDED_PRINCIPAL_RESULT_REPORT'}
assert len(groups)==194
with (R/'reported_event_groups194.tsv').open(newline='') as h:group_rows=list(csv.DictReader(h,delimiter='\t'))
principal_ids=[p for x in group_rows for p in json.loads(x['principal_report_ids'])]
companion_ids=[p for x in group_rows for p in json.loads(x['companion_report_ids'])]
assert len(group_rows)==194 and len(principal_ids)==len(set(principal_ids))==199
assert len(companion_ids)==len(set(companion_ids))==141
assert set(companion_ids)=={x['report_id'] for x in rows if x['disposition']=='INCLUDED_COMPANION_REPORT_NO_ADDITIONAL_TRIAL'}
assert set(principal_ids)=={x['report_id'] for x in rows if x['disposition']=='INCLUDED_PRINCIPAL_RESULT_REPORT'}
with (R/'source_result_routes126.tsv').open(newline='') as h:routes=list(csv.DictReader(h,delimiter='\t'))
assert len(routes)==len({x['group'] for x in routes})==126
assert Counter(x['route'] for x in routes)=={'EXACT_RESULT_TARGET_READY':93,'RESULT_PRESENT_TARGET_UNRESOLVED':27,'SOURCE_DESCRIPTION_ONLY_OR_PRIOR_FACT_ONLY':6}
r=json.loads((R/'adopted_result_risk168.json').read_text())
assert len(r['risk_targets'])==168 and r['current_groups_with_at_least_one_target']==68
assert len(groups)==68+126
v=json.loads((R/'analysis/VERIFICATION_SIX_EXISTING_CLINICAL_FITS.json').read_text())
assert v['check_count']==74 and all(x['pass'] for x in v['checks']) and v['new_scientific_fits']==0
print(json.dumps({'status':'PASS_CURRENT_WORKING_SNAPSHOT','distinct_reports':3088,'included_reports':340,'conservative_groups':194,'awaiting':40,'risk_targets':168,'source_inventory':126,'verification_checks':74,'new_scientific_models':0}))
