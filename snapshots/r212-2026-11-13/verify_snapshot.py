from pathlib import Path
from collections import Counter
import hashlib,json
HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[1]
def rd(n):return json.loads((HERE/n).read_text())
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
checks=[]
def check(name,v):
    assert v,name
    checks.append(name)
m=rd('PUBLIC_MANIFEST.json')
for x in m['files']:
    p=HERE/x['path'];check('hash:'+x['path'],p.is_file() and sha(p)==x['sha256'] and p.stat().st_size==x['bytes'])
c=rd('aggregate_counts.json')
check('records',c['database_records']+c['trial_register_records']+c['other_source_records']==c['records_identified']==29491)
check('dedup',c['records_identified']-c['duplicate_representations_removed']==c['record_groups']==21925)
check('screen',c['record_groups_excluded']+c['record_groups_advanced']==c['record_groups'])
check('retrieval',c['distinct_reports_sought']==c['reports_not_retrieved']+c['reports_assessed']==3088)
check('assessment',c['reports_assessed']==c['reports_not_included_with_reasons']+c['reports_unclassifiable_at_cutoff']+c['included_reports']==2589)
check('reports',c['included_reports']==c['principal_reports']+c['companion_reports']==340)
check('no_global_K_N',c['whole_review_independent_K'] is None and c['whole_review_unique_female_N'] is None)
a=rd('author_adoption_summary.json')
check('three_actual_approvals',a['actual_author_count']==a['exact_bound_whole_manuscript_approvals']==3 and a['new_scientific_decisions_per_author']==6)
check('not_human_original_reading',a['these_returns_do_not_attest_independent_original_source_reading'])
r=rd('adopted_result_risk279.json');check('risk279',len(r['risk_targets'])==r['risk_target_count']==279)
current={x['risk_target_id']:x for x in r['risk_targets']}
for tid in r['current_changed_risk_target_IDs']:
    x=current[tid];check('High:'+tid,x['adopted_domains']['D4']==x['adopted_overall']=='High' and x['current_signalling_answers']['D4']['4.5']=='NI')
pg=current['R30-MORIN-PGIC'];check('PGIC_D2',pg['adopted_domains']['D2']=='Some concerns' and pg['current_signalling_answers']['D2']['2.6']=='PY' and pg['current_signalling_answers']['D2']['2.7']=='NA')
oc=Counter(x.get('adopted_overall') or 'UNRESOLVED_OR_NO_ADOPTED_OVERALL' for x in current.values())
check('overall_layers',dict(oc)==r['current_overall_counts'] and oc['High']==184 and oc['Some concerns']==70 and oc['UNRESOLVED_OR_NO_ADOPTED_OVERALL']==25)
bp=ROOT/r['previous_immutable_public_risk_view']
if bp.is_file():
    check('base_fingerprint',sha(bp)==r['previous_public_file_sha256'])
    old={x['risk_target_id']:x for x in json.loads(bp.read_text())['risk_targets']}
    changed=[k for k in old if old[k]!=current[k]]
    check('only_two_risk_rows_changed',set(changed)==set(r['current_changed_risk_target_IDs']))
g=rd('exact_grade_targets3.json');check('three_exact_targets_one_trial',len(g['current_targets'])==3 and g['independent_trial_family_count']==1)
check('exact_grades',[x['current_label'] for x in g['current_targets']]==['Moderate','Low','Moderate'])
for x in g['current_targets']:
    check('grade_levels:'+x['decision_id'],sum(d['downgrade_levels'] for d in x['GRADE_domains'].values())==x['total_downgrade_levels'])
w=rd('clinical_window194.json');check('mapping194',len(w['rows'])==len({x['group'] for x in w['rows']})==194)
check('timing_categories',dict(Counter(x['timing_class'] for x in w['rows']))==w['counts']['timing_categories'])
can=Counter('PLANNED' if x['has_scheduled_window_candidate'] is True else 'CONDITIONAL' if x['has_scheduled_window_candidate']=='CONDITIONAL' else 'NO_ESTABLISHED_TARGET' for x in w['rows'])
check('candidate_layers',dict(can)==w['counts']['candidate_certainty_layers'] and can['PLANNED']==100 and can['CONDITIONAL']==38)
me=rd('registered_to_actual_methods.json');check('method_deviation',not me['registered_Bayesian_plan_implemented_for_focused_report'] and not me['planned_human_original_source_work_completed_claimed'])
me=rd('snapshot_meta.json');check('no_new_models',me['new_effects_CIs_N_models_or_trials']==0 and me['six_clinical_fits_and_22_diagnostic_fits_remain_separate'])
check('not_submission',not me['formal_submission_authorized'] and not me['formal_submission_performed'] and not me['preprint_published'])
print(json.dumps({'status':'PASS','checks':len(checks),'risk_targets':279,'current_exact_grade_targets':3,'clinical_window_groups':194,'new_models':0,'global_K_N_certified':False,'formal_submission_performed':False}))
