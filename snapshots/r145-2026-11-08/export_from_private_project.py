"""Export derived aggregate data only. No licensed original text or author receipts.
Usage: python export_from_private_project.py --project PROJECT_ROOT --output OUT
"""
from pathlib import Path
from hashlib import sha256
import argparse,csv,json
p=argparse.ArgumentParser();p.add_argument('--project',type=Path,required=True);p.add_argument('--output',type=Path,required=True);a=p.parse_args();H=a.project/'outputs/bmj_r145_s28_actual_adoption_and_analysis_20261108';D=a.output;D.mkdir(parents=True,exist_ok=True);rd=lambda p:json.loads(p.read_text())
def put(n,v):(D/n).write_text(json.dumps(v,ensure_ascii=False,indent=2)+'\n')
def tab(n,rs):
 with(D/n).open('w',newline='')as f:
  w=csv.DictWriter(f,fieldnames=list(rs[0]),delimiter='\t',lineterminator='\n');w.writeheader();w.writerows({k:json.dumps(v,ensure_ascii=False)if isinstance(v,(list,dict))else v for k,v in r.items()}for r in rs)
F=rd(H/'report_flow/R145_REPORT_FLOW_CURRENT.json');C=rd(H/'census/CURRENT_ACTUALLY_ADOPTED_SELECTED_RESULT_REPORTS140.json');records=[];actions=[]
for r in F['rows']:
 records.append({'own_report_id':r['canonical_own_report_id'],'record_groups':r['record_groups'],'title':r['title'],'flow_stage':r['formal_current_flow'],'available_extent':r['coarse_actual_source_extent'],'selected_result_slot':r.get('selected_source_slot'),'linked_source_families':r.get('confirmed_adopted_mother_family_ids',[]),'current_own_scope_reason':r.get('R145_primary_source_reason_code'),'parent_trial_excluded':False})
 if r.get('R145_actual_source_case'):actions.append({'case_id':r['R145_actual_source_case'],'own_report_id':r['canonical_own_report_id'],'action':r['R145_actual_source_use_choice'],'current_flow_stage':r['formal_current_flow'],'own_scope_reason':r.get('R145_primary_source_reason_code'),'parent_trial_excluded':False})
tab('current_report_identity_and_stage3099.tsv',records);tab('actual_S28_source_use49.tsv',actions)
tab('selected_result_to_source_group140.tsv',[{k:r.get(k)for k in ['census_report_id','source_use_id','own_title','own_report_identity_key','current_report_counting_cluster_key','report_randomized_N','N_count_status']}for r in C['rows']])
e=rd(H/'analysis/SOURCE039_DERIVED_COMPLETECASE_EFFECTS7.json');keys=['endpoint_id','construct','assigned_arm_N','observed_complete_case_arm_N','analysis_N','source_arm_change_means','source_arm_change_SDs','estimate','sampling_variance','standard_error','Welch_df','CI95_Welch','status','not_full_randomized_population_effect'];put('S8_SOURCE039_DERIVED_COMPLETECASE_EFFECTS7.json',{'status':'ONE_EARLY_COMPLETER_TRIAL_RELATED_RESULTS_NOT_POOLED','independent_trial_K':1,'analysis_N_per_endpoint':14,'rows':[{k:r[k]for k in keys}for r in e['rows']]})
c=F['summary'];put('aggregate_summary.json',{'snapshot':'R145availableevidencecutoff8November2026','identified':29490,'duplicates':7566,'screened_records':21924,'record_exclusions':18827,'record_groups_advanced':3097,'distinct_reports':3099,'reports_not_retrieved_at_required_extent':727,'assessed_or_classified_from_available_sources':2372,'report_terminal_counts':c['report_terminal_counts'],'selected_result_source_objects':140,'available_companions':98,'source_identity_dependency_policy_groups':136,'split_Yun_sensitivity_groups':137,'certified_whole_review_independent_K':None,'unique_adult_female_N':None,'source_enrolment_allocation_index_subtotal':15619,'known_N_source_groups':132,'source_N_is_not_unique_women_or_model_N':True,'actual_S28_cases':61,'actual_S28_author_choice_cells':183,'new_source_use_actions':49,'new_direct_result_sources':15,'new_own_source_scope_closures':34,'new_exact_companions':2,'new_source039_expressions':7,'source039_trial_K':1,'source039_complete_case_N':14,'new_pooled_fits':0,'clinical_model_fits_unchanged':6,'separate_historical_diagnostic_fits':22,'new_certainty_targets_pending_actual_author_adoption':4,'old8GRADE_differences_retained':True,'raw_papers_licensed_exports_private_receipts_or_ICMJE_uploaded':False,'submitted':False})
for f in D.iterdir():
 if f.is_file():f.write_text(f.read_text().replace('\r\n','\n').replace('\r','\n'))
print('Exported5derivedaggregatefiles;nooriginalpapertext/receipts')
