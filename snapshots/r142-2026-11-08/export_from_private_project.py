# SPDX-License-Identifier: MIT
"""Whitelist export of derived counts and report/trial linkage, without source text."""
from pathlib import Path
import json,csv,argparse

def project(project):
 h=Path(project)/"outputs/bmj_r142_s26_intake_and_final_flow_20261108"
 rd=lambda p:json.loads(p.read_text())
 f=rd(h/"report_flow/R142_REPORT_FLOW_COUNTS.json")
 c=rd(h/"census/CURRENT_ACTUALLY_ADOPTED_SELECTED_RESULT_REPORTS125.json")["summary"]
 a=rd(h/"actual_intake/APPLIED_S26_AUTHOR_DECISIONS.json")["counts"]
 return {"snapshot_id":"r142-2026-11-08","status":"AVAILABLE_EVIDENCE_CUTOFF_COUNTS_LOCKED_NOT_WHOLE_REVIEW_FINAL_ELIGIBILITY_OR_SUBMISSION", "record_framework":f["record_identification"],"report_inventory":{"reports_sought":f["own_report_nodes_sought_or_assessed"],"terminal_counts":f["report_terminal_counts"],"available_source_assessed":f["reports_currently_classified_or_assessed_from_available_sources"],"record_to_report_transfer":f["report_transfer_mapping"]["equation"],"selected_results":125,"available_exact_parent_companions":80,"required_extent_not_retrieved_split":{"indexed_abstract_only_required_body_missing":531,"no_own_text":198}},"selected_source_counting_policy":{"reports":125,"possible_dependency_clusters_primary":121,"separate_Yun_sensitivity":122,"Yun_proven_same_RCT":False,"new_LILA_Due_reports_do_not_add_K_or_N":True,"DMT110_added_once":True},"female_source_N_layers":{"female_allocation_or_prerandomization_indexwoman_subtotal":14156,"known_source_family_groups":118,"parallel_stricter_first_allocation_excluding_LookAHEAD_index375":13781,"parallel_stricter_known_family_groups":117,"initial_female_allocation_unknown_families":3,"unknown_families":["MSIR","CAT_DM","Brasil_Teles_RF"],"individual_level_unique_adult_female_N":None,"sexual_endpoint_N":None,"not_whole_review_participant_total":True,"baseline107groups_12109_inherited_not_all_reread":True},"actual_author_intake_aggregate":{"receipt_files":3,"choices":69,"source_and_policy_questions":23,"two_reviewer_agreements":21,"actual_third_author_adjudications":2,"preserved_Wen_dissents":2,"scope":"new source uses and dependency policy only; not numerical or whole-manuscript approval"},"new_only_author_review":{"packet":"S27","current_posted_registry_module_source_use_cases":41,"pending_actual_role_choices":123,"previous_S26_not_repeated":True,"remaining18_of59_current_source_checks_reused_or_specific_body_or_reporting_gates_retained_without_resign":18,"clinical_parent_trial_exclusions_added":0},"analysis":{"existing_restricted_comparisons":3,"existing_fits":6,"diagnostic_fits_separate":22,"new_effect_inputs":0,"new_fits":0,"new_RoB2_or_GRADE":0,"old_eight_GRADE_differences_retained":True,"historical_tag":"v0.1.0","historical_commit":"1f4131d50445727c44c3e1210bf78e45ed7121fc"},"limits":{"counts_locked_at_available_cutoff":True,"whole_review_final_eligibility_complete":False,"whole_review_final_K":None,"whole_review_unique_N":None,"all_current_sources_are_full_journal_papers":False,"protocol_and_awaiting_carriers_not_parent_trial_exclusions":True,"original_independent_dual_human_fulltext_reading_claimed":False,"current_full_manuscript_author_approval_obtained":False,"submission_ready":False,"submitted":False}}

def export(project_dir,output):
 h=Path(project_dir)/"outputs/bmj_r142_s26_intake_and_final_flow_20261108";output=Path(output);output.mkdir(parents=True,exist_ok=True)
 (output/"aggregate_summary.json").write_text(json.dumps(project(project_dir),indent=2)+"\n")
 rd=lambda p:json.loads(p.read_text())
 fields=["own_report_id","record_groups","title","own_PMIDs","own_DOIs","own_registry_primary_ids","confirmed_adopted_mother_family_ids","current_report_stage","formal_current_flow","coarse_actual_source_extent","source_report_role"]
 rows=rd(h/"report_flow/R142_REPORT_FLOW_CURRENT.json")["rows"]
 with(output/"current_report_identity_and_stage3114.tsv").open("w",newline="")as f:
  w=csv.DictWriter(f,fields,delimiter="\t",lineterminator="\n");w.writeheader()
  for r in rows:w.writerow({k:json.dumps(r.get(k),ensure_ascii=False,separators=(",",":"))if isinstance(r.get(k),(dict,list))else r.get(k,"")for k in fields})
 fields=["census_report_id","source_use_id","stratum","own_title","own_report_identity_key","own_DOIs","own_PMIDs","source_family_identity_key","current_report_counting_cluster_key"]
 rows=rd(h/"census/CURRENT_ACTUALLY_ADOPTED_SELECTED_RESULT_REPORTS125.json")["rows"]
 with(output/"selected_result_to_source_cluster125.tsv").open("w",newline="")as f:
  w=csv.DictWriter(f,fields,delimiter="\t",lineterminator="\n");w.writeheader()
  for r in rows:w.writerow({k:json.dumps(r.get(k),ensure_ascii=False,separators=(",",":"))if isinstance(r.get(k),(dict,list))else r.get(k,"")for k in fields})

if __name__=="__main__":
 p=argparse.ArgumentParser();p.add_argument("--project",type=Path,required=True);p.add_argument("--output",type=Path,required=True);a=p.parse_args();export(a.project,a.output)
