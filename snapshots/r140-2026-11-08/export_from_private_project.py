# SPDX-License-Identifier: MIT
"""Export whitelisted R140 process aggregates; never author receipts or source text."""
from pathlib import Path
import json,argparse
def project(project):
    b=Path(project)/"outputs/bmj_r140_s25_actual_intake_20261108"
    r=json.loads((b/"R140_RECORD_RECONCILIATION.json").read_text())
    c=json.loads((b/"actual_intake/RECEIPT_VERIFICATION.json").read_text())["counts"]
    return {
      "snapshot_id":"r140-2026-11-08","status":"ACTUAL_SOURCE_ADOPTION_PROCESS_AGGREGATES_NOT_FINAL_PRISMA_OR_NEW_ANALYSIS",
      "record_framework":{"identified":int(r["records_identified"]),"duplicates":int(r["duplicates_removed"]),"canonical_groups":int(r["current_record_groups"])},
      "current_working_routes":{k:int(v)for k,v in r["current_working_routes"].items()},
      "actual_author_review":{"receipt_files":int(c["actual_receipt_files"]),"top_level_choice_cells":int(c["actual_top_level_choices"]),"source_actions_per_role":int(c["source_actions_per_role"]),"actual_source_action_cells":int(c["total_actual_source_action_cells"]),"two_reviewer_differences_using_actual_adjudicator":int(c["two_reviewer_differences_using_actual_Yin"]),"adjudicator_dissent_to_agreed_reviewers_retained":int(c["Yin_dissents_to_agreed_reviewers_retained"]),"source_action_differences_preserved":int(c["three_role_action_differences"]),"AI_adoption_not_planned_independent_duplicate_human_original_reading":True,"discussion_not_inferred":True},
      "applied_source_actions":{k:int(v)for k,v in c["applied_action_counts"].items()},
      "this_round":{"own_record_screen_closures":int(r["new_record_screen_dispositions"]),"additional_same_report_merges":0,"parent_trial_exclusions":0,"new_model_inputs":0,"new_models":0,"new_GRADE":0,"pending_new_author_cases":0},
      "previously_adopted_anchor":{"reports":99,"source_family_groups":98,"whole_search_final":False},
      "limits":{"final_PRISMA":False,"whole_review_independent_K":None,"whole_review_unique_N":None,"submission_ready":False,"other_clinical_registry_and_resource_gates_remain":True,"source_roles_not_independent_studies":True,"previous_eight_GRADE_differences_preserved":True},
      "historical_analysis":{"unchanged_commit":"1f4131d50445727c44c3e1210bf78e45ed7121fc","tag":"v0.1.0","comparisons":3,"fits":6,"diagnostic_fits_separate":22}
    }
if __name__=="__main__":
    p=argparse.ArgumentParser();p.add_argument("--project",required=True,type=Path);p.add_argument("--output",required=True,type=Path);a=p.parse_args();a.output.write_text(json.dumps(project(a.project),indent=2)+"\n")
