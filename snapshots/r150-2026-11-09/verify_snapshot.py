from pathlib import Path
import csv,json,hashlib,collections
H=Path(__file__).resolve().parent
m=json.loads((H/'MANIFEST_SHA256.json').read_text(encoding='utf-8'))
assert len(m['files'])==6
for x in m['files']:
 p=H/x['name'];raw=p.read_bytes()
 assert p.parent==H and p.is_file()
 assert hashlib.sha256(raw).hexdigest()==x['sha256'],x['name']
 assert len(raw)==x['bytes'],x['name']
a=json.loads((H/'aggregate_counts.json').read_text(encoding='utf-8'))
def tsv(name):
 with(H/name).open(encoding='utf-8',newline='')as f:return list(csv.DictReader(f,delimiter='\t'))
r=tsv('report_dispositions3099.tsv');g=tsv('source_families139.tsv');s=tsv('actual_S31_scope_actions164.tsv')
def partition(stage):
 if stage.startswith('INCLUDED'):return 'included'
 if 'AWAITING'in stage:return 'awaiting_classification'
 if stage.startswith('REPORT_NOT_RETRIEVED'):return 'not_retrieved'
 if stage=='OWN_PROTOCOL_OR_NO_POSTED_RESULT_INVENTORY_PARENT_ELIGIBILITY_NOT_DENIED':return 'protocol_or_associated_no_current_target_result_inventory'
 if 'EXCLUDED'in stage or stage.startswith('REPORT_SOURCE_OUTSIDE_SCOPE'):return 'excluded_own_source_use'
 raise AssertionError(stage)
assert len(r)==len({x['own_report_id']for x in r})==3099
for x in r:assert partition(x['formal_current_flow'])==x['terminal_partition']
counts=dict(collections.Counter(x['terminal_partition']for x in r))
assert counts==a['report_terminal_partition']
assert counts=={'protocol_or_associated_no_current_target_result_inventory':1650,'not_retrieved':725,'awaiting_classification':126,'excluded_own_source_use':339,'included':259}
assert len(r)==725+2374 and 2374==1650+126+339+259
selected=[x for x in r if x['selected_result_source']=='true']
assert len(selected)==len({x['selected_result_source_id']for x in selected})==143
assert all(x['terminal_partition']=='included'for x in selected)
assert 259-143==a['included_companion_reports']==116
assert len(g)==len({x['counting_cluster_key']for x in g})==139
report_ids=[];known=[];unknown=[]
for x in g:
 ids=json.loads(x['selected_result_source_ids']);values=json.loads(x['reported_source_N_values'])
 assert len(ids)==int(x['selected_result_report_count'])
 report_ids.extend(ids);values=[v for v in values if v is not None]
 if x['source_N_subtotal_contribution']=='':
  assert not values;unknown.append(x['counting_cluster_key'])
 else:
  value=int(x['source_N_subtotal_contribution']);assert value>0 and value==max(values)
  known.append(value)
 assert x['not_unique_or_effective_model_N']=='true' and x['not_proof_of_no_individual_overlap']=='true'
assert len(report_ids)==len(set(report_ids))==143
assert set(report_ids)=={x['selected_result_source_id']for x in selected}
assert {x['selected_source_counting_cluster']for x in selected}=={x['counting_cluster_key']for x in g}
assert len(known)==135 and sum(known)==a['reported_source_female_allocation_or_index_N_subtotal']==15833
assert sorted(unknown)==sorted(a['source_N_unknown_groups']) and len(unknown)==4
assert 15833-375==a['subtotal_excluding_LookAHEAD_index375']==15458
assert 15833-375-14==a['subtotal_also_excluding_Gouveia14_methods_vs32_abstract_conflict']==15444
assert len(s)==len({x['case_id']for x in s})==len({x['source_id']for x in s})==164
byid={x['own_report_id']:x for x in r}
for x in s:
 assert x['scope']=='SOURCE_SCOPE_ONLY'
 assert x['new_numeric_RoB_GRADE_or_independent_K_N_release']=='false'
 assert byid[x['source_id']]['formal_current_flow']==x['current_stage']
assert sum(x['source_action'].startswith('INCLUDE_')for x in s)==3
assert sum(x['source_action'].startswith('EXCLUDE_')for x in s)==110
assert sum(x['source_action'].startswith('CLASSIFY_')for x in s)==50
assert sum(x['source_action'].startswith('LINK_')for x in s)==1
z=a['record_identification']
assert z['records_identified']==z['database_export_records']+z['trial_register_export_records']+z['other_source_records']==29490
assert 29490-7566==21924==18827+3097
assert 3097+3+1-1-1==len(r)
assert a['source_disposition_closed']==2374-126==2248
assert abs(a['source_disposition_percent']-2248/2374*100)<1e-10
assert a['whole_review_independent_trial_K']is None and a['whole_review_unique_female_N']is None and a['whole_work_completion_percent']is None
assert a['S32_new_scientific_judgments_pending']==20==a['S32_pending_source_use_judgments']+a['S32_pending_result_specific_RoB2_plans']
assert not a['S32_author_adoption_assumed']and a['old8_GRADE_disagreements_retained']
assert a['clinical_model_fits']==6 and a['bounded_clinical_comparisons']==3 and a['clinical_pool_trial_K_per_comparison']==2 and a['historical_diagnostic_fits_separate']==22
assert not a['whole_review_final_PRISMA']and not a['whole_review_final_GRADE']and not a['submission_ready']and not a['submitted']
print('PASS: 3099 report dispositions; 143 selected sources in 139 source groups; reported source N 15833 across 135 known groups; S31 actions164; pending S32 20; no whole-study completion claim')
