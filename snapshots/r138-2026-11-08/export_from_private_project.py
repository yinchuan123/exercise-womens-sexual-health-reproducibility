# SPDX-License-Identifier: MIT
"""Regenerate the aggregate-only R138 process snapshot from a private project.
The private source archive and signed receipts are not distributed. This script
projects named numerical fields; it never copies whole source JSON objects.
"""
from argparse import ArgumentParser
from pathlib import Path
import json

def project(root):
    base = Path(root) / "outputs/bmj_r138_s24_intake_20261108"
    def read(path):
        return json.loads(Path(path).read_text(encoding="utf-8"))
    r = read(base / "R138_RECORD_RECONCILIATION.json")
    v = read(base / "actual_intake/RECEIPT_VERIFICATION.json")
    u = read(base / "new_source_admission/APPLIED_SOURCE_USES.json")
    q = read(base / "analysis/NEW_SIGNED_SOURCES_NUMERIC_GATE_QA.json")
    a = read(Path(root) / "outputs/bmj_r137_final_flow_reconstruction_20261108/new_fulltexts_31/CURRENT_ACQUISITION_OVERLAY.json")
    c = v["counts"]
    def integers(d, names):
        return {k: int(d[k]) for k in names}
    return {
        "schema_version": "1.0",
        "snapshot_id": "r138-2026-11-08",
        "status": "AGGREGATE_PROCESS_SNAPSHOT_NOT_FINAL_SELECTION_OR_NEW_CLINICAL_ANALYSIS",
        "record_framework": integers(r, ["records_identified", "duplicates_removed", "current_record_groups"]),
        "working_routes": integers(r["current_working_routes"], ["RECORD_SCREEN_EXCLUDED", "RETAIN_OR_LINK_AUTHOR_ADOPTED", "FORMAL_HOLD", "RETAIN_OR_LINK_TECHNICAL_EXISTING_POLICY"]),
        "record_route_delta": {
            "previous_record_screen_excluded": int(r["previous_working_routes"]["RECORD_SCREEN_EXCLUDED"]),
            "new_record_screen_dispositions": int(r["new_record_screen_dispositions"]),
            "prior_exclusion_reversed_by_actual_source_scope": int(r["prior_record_exclusions_superseded_by_new_actual_full_source_scope"]),
            "net_record_screen_exclusion_delta": int(r["new_record_screen_dispositions"]) - int(r["prior_record_exclusions_superseded_by_new_actual_full_source_scope"]),
            "reused_specific_source_dispositions": int(r["reused_old_specific_source_dispositions"]),
            "new153_source_dispositions": int(r["new153_source_dispositions"]),
            "parent_trials_excluded_by_source_role_projection": int(r["new_false_parent_trial_exclusions"]),
        },
        "human_review_aggregate": integers(c, ["actual_receipt_files", "actual_top_level_choice_cells", "actual_A_choices", "source_actions_per_role", "clinical_source_cases", "source_vector153_rows", "new31_source_vector_rows", "two_reviewer_unresolved_source_actions_adjudicated", "Yin_dissents_to_agreed_two_reviewer_actions_retained"]),
        "review_method_boundary": {
            "two_reviewers_agreement_then_actual_adjudicator_for_their_unresolved_difference": True,
            "third_author_dissent_to_agreed_reviewers_preserved": True,
            "majority_voting": False,
            "independent_duplicate_human_original_fulltext_reading_established_by_receipts": False,
            "actual_work": "Author adoption of independently generated AI role recommendations; planned independent human original reading is not inferred.",
        },
        "source_use_adoptions": {
            "source_use_rows": int(r["all_current_source_use_rows"]),
            "limited_whole_package_narrative_uses": int(r["additional_author_adopted_narrative_source_uses"]),
            "nonrandom_or_mixed_design_limits": int(u["counts"]["categories"]["NONRANDOM_OR_MIXED_DESIGN_LIMIT"]),
            "companion_or_protocol_uses": int(u["counts"]["categories"]["COMPANION_OR_PROTOCOL"]),
            "carrier_without_own_target_result": int(u["counts"]["categories"]["NO_OWN_TARGET_RESULT"]),
            "not_18_additional_independent_trials": True,
        },
        "received_material_aggregate": {
            "pdf_carriers": int(a["actual_files"]),
            "workbooks": 1,
            "requested_targets_identity_matched": int(a["actual_requested_targets_matched"]),
            "requested_targets_unobtained_closed": int(a["requested_targets_unobtained_closed"]),
            "different_report_supplied": 1,
            "receipt_is_not_scientific_admission": True,
        },
        "previously_adopted_anchor": {
            "result_reports": int(r["current_positive_anchor_reports"]),
            "source_supported_family_groups": int(r["current_positive_anchor_source_family_groups"]),
            "principal_reports": 85,
            "principal_family_groups": 84,
            "is_final_whole_search_independent_census": False,
        },
        "numeric_gate_aggregate": {
            "source_carriers_checked": int(q["actual_signed_scope_carriers"]),
            "source_endpoint_objects": int(q["source_endpoint_objects"]),
            "technical_source_component_candidates": int(q["technical_ready_source_component_candidates"]),
            "direct_reported_coefficient_SE_candidates": int(q["direct_reported_coefficient_SE_candidates"]),
            "new_numeric_inputs": int(r["new_numeric_model_or_GRADE_inputs"]),
            "new_model_fits": int(v["new_models"]),
            "new_GRADE_admissions": int(v["new_GRADE"]),
            "source_components_not_new_effects_or_studies": True,
        },
        "remaining_boundaries": {
            "final_PRISMA": bool(r["final_PRISMA"]),
            "whole_review_independent_K": r["whole_review_independent_K"],
            "whole_review_unique_N": r["whole_review_unique_N"],
            "submission_ready": bool(r["submission_ready"]),
            "working_routes_not_sequential_PRISMA_stages": True,
            "no_missing_result_is_automatic_trial_exclusion": True,
            "new_scope_adoption_not_effect_admission": True,
            "previous_scoped_GRADE_differences_preserved": int(r["old_GRADE_differences_retained"]),
        },
        "historical_reproduction_snapshot": {
            "git_commit": "1f4131d50445727c44c3e1210bf78e45ed7121fc",
            "tag": "v0.1.0",
            "model_reproduction_command": "python3 analysis/reproduce.py --output out",
            "historical_numerical_inputs_not_replaced_by_this_process_snapshot": True,
        },
    }

if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument("--project", required=True, type=Path)
    parser.add_argument("--output", required=True, type=Path)
    args = parser.parse_args()
    payload = project(args.project)
    args.output.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
