"""Verify source-specific N arithmetic and the retained report-flow boundary."""
from pathlib import Path
import csv
import json

base = Path(__file__).resolve().parent
state = json.loads((base / "current_state_after_source_intake.json").read_text())
with (base / "Zhang_candidate_source_N_correction.tsv").open(newline="") as f:
    rows = {r["arm"]: r for r in csv.DictReader(f, delimiter="\t")}
with (base / "final_three_source_intake.tsv").open(newline="") as f:
    intake = list(csv.DictReader(f, delimiter="\t"))
checks = {}
checks["three_received_files_two_matching_originals_one_background"] = len(intake) == 3 and state["matching_original_clinical_reports"] == 2 and state["background_only_files"] == 1
checks["source_screening_arithmetic"] = 20198 - 13858 == 6340 and 6340 - 3640 == 2700
checks["four_initial_arms"] = sum(int(rows[a]["initial_randomized_N"]) for a in rows if a != "ALL") == 2700
checks["six_week_evaluated"] = sum(int(rows[a]["six_week_evaluated_N"]) for a in rows if a != "ALL") == 2403
checks["losses"] = sum(int(rows[a]["lost_N"]) for a in rows if a != "ALL") == 297 and 2700 - 297 == 2403
checks["each_arm_flow"] = all(int(r["initial_randomized_N"]) == int(r["six_week_evaluated_N"]) + int(r["lost_N"]) for r in rows.values())
checks["report_retrieval_arithmetic"] = state["reports_sought"] == state["not_retrieved"] + state["reports_assessed"]
checks["report_disposition_arithmetic"] = state["reports_assessed"] == state["not_included"] + state["qualification_unascertainable"] + state["included"]
checks["principal_companion_arithmetic"] = state["included"] == state["principal"] + state["companion"]
checks["strict_gaps_retained"] = (state["qualification_unascertainable"],state["initial_female_N_gap_groups"],state["unresolved_dependency_pairs"],state["not_retrieved"]) == (40,8,2,499)
checks["no_candidate_admission_or_new_model"] = state["new_effect_inputs"] == 0 and state["new_fits_or_RoB2_or_GRADE"] == 0 and state["whole_review_unique_female_N"] is None and not state["whole_review_independent_K_certified"]
checks["no_new_author_or_resource_request"] = state["new_human_judgments"] == 0 and state["active_resource_requests"] == 0 and state["external_messages_sent"] == 0
print(json.dumps({"checks":checks,"passed":sum(checks.values()),"total":len(checks)},indent=2))
if not all(checks.values()):
    raise SystemExit(1)
