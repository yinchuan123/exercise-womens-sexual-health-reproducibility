# SPDX-License-Identifier: MIT
from pathlib import Path
from hashlib import sha256
import json,csv,collections
P=Path(__file__).resolve().parent
for line in(P/"MANIFEST.sha256").read_text().splitlines():
 digest,name=line.split("  ",1);p=P/name;assert p.resolve().is_relative_to(P)and not p.is_symlink();assert sha256(p.read_bytes()).hexdigest()==digest,name
d=json.loads((P/"aggregate_summary.json").read_text());r=d["record_framework"];f=d["report_inventory"];n=f["terminal_counts"]
assert r["records_identified"]-r["duplicates_removed"]==r["records_screened"]==21940
assert r["records_excluded_at_record_phase"]+r["record_groups_advanced_to_report_or_resource_assessment"]==21940
assert f["reports_sought"]==sum(n.values())==3114 and n["reports_excluded_with_actual_source_reasons"]==179
assert f["available_source_assessed"]+n["not_retrieved"]==3114
assert f["selected_results"]+f["available_exact_parent_companions"]==n["included_reports"]
a=d["actual_S27_author_intake_aggregate"];assert a["receipt_files"]==3 and a["source_use_questions"]==41 and a["actual_author_cells"]==123 and a["two_named_reviewer_agreements"]==41 and a["actual_third_author_arbitrations"]==0
assert sum(a["current_own_module_actions"].values())==41 and a["new_parent_clinical_exclusions"]==0
with(P/"current_report_identity_and_stage3114.tsv").open()as f:rows=list(csv.DictReader(f,delimiter="\t"))
assert len(rows)==len({r["own_report_id"]for r in rows})==3114
with(P/"selected_result_to_source_cluster125.tsv").open()as f:rows=list(csv.DictReader(f,delimiter="\t"))
assert len(rows)==125 and len({r["current_report_counting_cluster_key"]for r in rows})==121
with(P/"actual_S27_own_module_use41.tsv").open()as f:rows=list(csv.DictReader(f,delimiter="\t"))
assert len(rows)==41 and len({r["case_id"]for r in rows})==41
assert not d["limits"]["whole_review_final_eligibility_complete"] and not d["limits"]["submission_ready"] and d["limits"]["whole_review_unique_N"]is None
print(json.dumps({"status":"PASS_ACTUAL_S27_AND_CURRENT_AVAILABLE_CUTOFF_COUNTS_ONLY","reports":3114,"selected_results":125,"primary_clusters":121,"S27_pending_cases":0,"whole_review_final_eligibility":False},indent=2))
