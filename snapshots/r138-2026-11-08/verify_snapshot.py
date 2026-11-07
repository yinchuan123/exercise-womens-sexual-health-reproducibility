# SPDX-License-Identifier: MIT
"""Check only the public R138 aggregate snapshot; no source text or model fits."""
from pathlib import Path
from hashlib import sha256
import json
ROOT = Path(__file__).resolve().parent

def verify():
    checked = 0
    for line in (ROOT / "MANIFEST.sha256").read_text().splitlines():
        digest, rel = line.split("  ", 1)
        target = ROOT / rel
        if not target.resolve().is_relative_to(ROOT) or target.is_symlink():
            raise ValueError("Unsafe path in snapshot manifest")
        if sha256(target.read_bytes()).hexdigest() != digest:
            raise ValueError("Snapshot checksum mismatch: " + rel)
        checked += 1
    d = json.loads((ROOT / "aggregate_summary.json").read_text())
    f, w, delta = d["record_framework"], d["working_routes"], d["record_route_delta"]
    assert f["records_identified"] - f["duplicates_removed"] == f["current_record_groups"] == sum(w.values())
    assert delta["new_record_screen_dispositions"] - delta["prior_exclusion_reversed_by_actual_source_scope"] == delta["net_record_screen_exclusion_delta"]
    assert delta["previous_record_screen_excluded"] + delta["net_record_screen_exclusion_delta"] == w["RECORD_SCREEN_EXCLUDED"]
    assert delta["reused_specific_source_dispositions"] + delta["new153_source_dispositions"] == delta["new_record_screen_dispositions"]
    h, s, a, n, b = (d[k] for k in ["human_review_aggregate", "source_use_adoptions", "received_material_aggregate", "numeric_gate_aggregate", "remaining_boundaries"])
    assert h["actual_receipt_files"] * 9 == h["actual_top_level_choice_cells"] == h["actual_A_choices"]
    assert h["source_vector153_rows"] + h["new31_source_vector_rows"] == h["source_actions_per_role"]
    assert s["limited_whole_package_narrative_uses"] + s["nonrandom_or_mixed_design_limits"] + s["companion_or_protocol_uses"] + s["carrier_without_own_target_result"] == s["source_use_rows"]
    assert a["requested_targets_identity_matched"] + a["different_report_supplied"] == a["pdf_carriers"]
    assert a["requested_targets_identity_matched"] + a["requested_targets_unobtained_closed"] == 41
    assert n["new_numeric_inputs"] == n["new_model_fits"] == n["new_GRADE_admissions"] == 0
    assert b["final_PRISMA"] is False and b["whole_review_independent_K"] is None and b["whole_review_unique_N"] is None and b["submission_ready"] is False
    assert d["previously_adopted_anchor"]["is_final_whole_search_independent_census"] is False
    assert d["review_method_boundary"]["independent_duplicate_human_original_fulltext_reading_established_by_receipts"] is False
    return {"status":"PASS_AGGREGATE_PROCESS_ONLY", "snapshot_id":d["snapshot_id"], "manifest_files_checked":checked, "new_clinical_models":0, "final_PRISMA":False}

if __name__ == "__main__":
    print(json.dumps(verify(), indent=2))
