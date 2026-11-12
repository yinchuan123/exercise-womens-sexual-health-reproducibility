from pathlib import Path
import json,csv,hashlib
R=Path(__file__).resolve().parent
d=json.loads((R/'snapshot_meta.json').read_text());m=json.loads((R/'MANIFEST_SHA256.json').read_text())
for x in m['files']:
 b=(R/x['path']).read_bytes();assert len(b)==x['bytes'] and hashlib.sha256(b).hexdigest()==x['sha256'],x['path']
assert d['actual_new_disposition']=='B' and d['new_author_questions_remaining']==0
assert d['new_positive_eligibility_N_or_overlap_facts']==0
assert d['reports_sought']==d['not_retrieved']+d['assessed']==3088
assert d['assessed']==d['not_included']+d['awaiting_qualification']+d['included']==2589
assert d['included']==d['principal']+d['companion']==340
assert d['conservative_reported_event_groups']==194 and d['dependency_split_scenarios']==[195,196]
assert d['initial_female_N_gaps']==8 and d['suspected_dependency_pairs']==2
assert d['global_unique_female_N'] is None and not d['global_independent_K_certified']
assert d['existing_comparison_independent_K']==[2,2,2] and d['new_clinical_model_inputs_or_fits']==0
assert not d['all_missing_facts_resolved'] and not d['formal_submission_performed'] and not d['preprint_published']
q=list(csv.DictReader((R/'qualification40_reassessment.tsv').open(),delimiter='\t'))
n=list(csv.DictReader((R/'initialN8_dependency2_reassessment.tsv').open(),delimiter='\t'))
assert len(q)==40 and len(n)==10 and len({x['report_id'] for x in q})==40
assert sum(x['report_id']=='doi:10.1016/0005-7916(73)90051-7' for x in q)==1
prior=R.parent/'r204-2026-11-12'
if prior.is_dir():
 p=json.loads((prior/'snapshot_meta.json').read_text());risk=json.loads((prior/'adopted_result_risk279.json').read_text())
 assert p['included_reports']==d['included'] and p['qualification_unascertainable']==d['awaiting_qualification']
 assert risk['risk_target_count']==279 and len(risk['risk_targets'])==279
print(json.dumps({'status':'PASS_ACTUAL_FINAL_B_NO_NEW_FACTS_OR_INPUTS','reports':3088,'included':340,'awaiting':40,'groups':194,'new_author_questions':0,'new_model_fits':0}))
