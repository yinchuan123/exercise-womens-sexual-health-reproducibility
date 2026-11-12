"""Verify executed cutoff dispositions without imputing missing source facts."""
from pathlib import Path
from collections import Counter
import csv,json
p=Path(__file__).resolve().parent
j=json.loads((p/"workflow_closure_metadata.json").read_text())
with (p/"FINAL_CUTOFF_DISPOSITIONS50.tsv").open(newline="") as f:r=list(csv.DictReader(f,delimiter="\t"))
c=Counter(x["task_type"] for x in r)
checks={
 "fifty_different_unit_tasks":len(r)==50 and c=={"qualification":40,"initial_female_N":8,"dependency_pair":2},
 "terminal_workflow_actions":all(x["workflow_state"]=="CLOSED_AT_FINAL_AVAILABLE_EVIDENCE_CUTOFF" for x in r),
 "no_active_resources":all(x["active_resource_request"]=="False" for x in r) and j["active_resource_requests"]==0,
 "no_new_signature_or_missing_fact_vote":all(x["new_scientific_human_judgment_needed"]=="False" and x["missing_fact_proved"]=="False" for x in r),
 "no_new_numerical_admission":all(x["entered_quantitative_input_by_this_closure"]=="False" for x in r),
 "retained_counts":(j["included_reports"],j["qualification_unascertainable_at_cutoff"],j["not_retrieved_at_cutoff"])==(340,40,499),
 "principal_companion":j["included_reports"]==j["principal"]+j["companion"],
 "group_layers_not_global_independent_K":j["conservative_strategy_groups"]==194 and j["dependency_split_scenarios"]==[195,196] and not j["whole_review_independent_K_certified"],
 "no_grand_unique_N":j["whole_review_unique_female_N"] is None and j["initial_female_N_gaps_retained"]==8,
 "comparison_K":j["existing_comparison_K"]==[2,2,2],
 "no_submission_or_preprint":not j["formal_submission_performed"] and not j["preprint_published"]}
print(json.dumps({"passed":sum(checks.values()),"total":len(checks),"checks":checks},indent=2))
if not all(checks.values()):raise SystemExit(1)
