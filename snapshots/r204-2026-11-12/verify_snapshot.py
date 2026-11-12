from pathlib import Path
from collections import Counter
import json,csv,hashlib
R=Path(__file__).resolve().parent
for x in json.loads((R/'MANIFEST_SHA256.json').read_text())['files']:
 assert hashlib.sha256((R/x['path']).read_bytes()).hexdigest()==x['sha256'],x['path']
read=lambda n:json.loads((R/n).read_text())
tsv=lambda n:list(csv.DictReader((R/n).open(newline=''),delimiter='\t'))
rows=tsv('report_dispositions3088.tsv');groups=tsv('reported_event_groups194.tsv')
assert len(rows)==3088 and len(groups)==194
d=Counter(x['disposition'] for x in rows)
assert d['INCLUDED_PRINCIPAL_RESULT_REPORT']==199 and d['INCLUDED_COMPANION_REPORT_NO_ADDITIONAL_TRIAL']==141
assert d['AWAITING_CLASSIFICATION_AT_FINAL_EVIDENCE_CUTOFF']==40 and d['NOT_RETRIEVED_AT_FIXED_CUTOFF']==499
p=[z for x in groups for z in json.loads(x['principal_report_ids'])];c=[z for x in groups for z in json.loads(x['companion_report_ids'])]
assert len(p)==len(set(p))==199 and len(c)==len(set(c))==141
assert set(c)=={x['report_id'] for x in rows if x['disposition']=='INCLUDED_COMPANION_REPORT_NO_ADDITIONAL_TRIAL'}
assert 29491==17574+10937+980 and 29491-7566==21925 and 21925-18827==3098
assert 3098-1+4-13==3088 and 3088==499+2589 and 2589==2209+40+340 and 340==199+141
r=read('adopted_result_risk279.json')['risk_targets'];assert len(r)==len({x['risk_target_id'] for x in r})==279
assert len({x['family'] for x in r})==159
h=read('actual_tool_HOLDs2.json')['rows'];assert len(h)==2 and not ({x['target_id'] for x in h}&{x['risk_target_id'] for x in r})
for role in 'ABC':
 v=read('new111_signal_positions_role_'+role+'.json')['rows'];assert len(v)==111
 assert Counter(x['tool'] for x in v)=={'parallel2019':108,'cluster2021':2,'crossover2021':1}
 assert sum(len(x['answers']) for x in v)==2458
 assert all(x['answers'].get('3.2') in ['Y','PY','N','PN','NA'] for x in v)
q=read('retained_certainty91_views.json');assert len(q['certainty_record_views'])==91 and q['existing_disagreement_count']==8
assert len(tsv('qualification40_retained.tsv'))==40 and len(tsv('initial_female_N8_retained.tsv'))==8 and len(tsv('dependency_pairs2_retained.tsv'))==2
v=read('analysis/VERIFICATION_SIX_EXISTING_CLINICAL_FITS.json');assert v['check_count']==74 and all(x['pass'] for x in v['checks']) and v['new_scientific_fits']==0
print(json.dumps({'status':'PASS_R204_ACTUAL_ADOPTIONS_AND_RETAINED_CUTOFF_GAPS','reports':3088,'included_reports':340,'groups':194,'risk_targets':279,'groups_with_risk_target':159,'tool_HOLDs':2,'new_GRADE':0,'verification_checks':74,'reply_facts_used':0}))
