# SPDX-License-Identifier: MIT
"""Export only named derived R139 counts, never source text or author receipts."""
from pathlib import Path
import json,argparse
def project(project):
    base=Path(project)/"outputs/bmj_r139_remaining_source_qualification_20261108"
    r=json.loads((base/"R139_RECORD_RECONCILIATION.json").read_text())
    return {
      "snapshot_id":"r139-2026-11-08",
      "status":"DERIVED_PROCESS_AGGREGATES_NOT_FINAL_SELECTION_OR_CLINICAL_ANALYSIS",
      "record_framework":{"identified":int(r["identified_records"]),"duplicates":int(r["duplicate_records"]),"canonical_groups":int(r["current_canonical_record_groups"])},
      "current_working_routes":{k:int(v)for k,v in r["current_working_routes"].items()},
      "this_round":{"same_published_report_aliases":int(r["additional_same_report_aliases"]),"old_specific_author_fact_own_source_actions":int(r["own_source_record_screen_actions"]),"source_qualification_rows":int(r["source_qualification_rows"]),"unadopted_proposal_rows_before_alias":int(r["new_unadopted_source_rows"]),"canonical_unadopted_sources":int(r["canonical_new_question_sources"]),"new_human_signatures":0,"new_model_inputs":0,"new_models":0,"new_GRADE":0},
      "previously_adopted_anchor":{"reports":99,"source_supported_family_groups":98,"whole_search_final":False},
      "limits":{"final_PRISMA":False,"whole_review_independent_K":None,"whole_review_unique_N":None,"submission_ready":False,"other_clinical_and_registry_gates_remain":True,"missing_source_not_clinical_exclusion":True,"same_report_merge_not_trial_merge":True,"raw_and_versioned_carriers_retained_privately":True,"planned_duplicate_human_original_reading_not_established_by_AI_adoption":True,"previous_eight_GRADE_differences_preserved":True},
      "historical_analysis":{"unchanged_commit":"1f4131d50445727c44c3e1210bf78e45ed7121fc","tag":"v0.1.0","comparisons":3,"fits":6,"diagnostic_fits_separate":22}
    }
if __name__=="__main__":
    a=argparse.ArgumentParser();a.add_argument("--project",required=True,type=Path);a.add_argument("--output",required=True,type=Path);p=a.parse_args();p.output.write_text(json.dumps(project(p.project),indent=2)+"\n")
