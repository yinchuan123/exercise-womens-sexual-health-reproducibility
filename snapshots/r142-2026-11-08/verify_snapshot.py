# SPDX-License-Identifier: MIT
from pathlib import Path
from hashlib import sha256
import json,csv,collections
P=Path(__file__).resolve().parent
for line in(P/"MANIFEST.sha256").read_text().splitlines():
 digest,name=line.split("  ",1);p=P/name;assert p.resolve().is_relative_to(P)and not p.is_symlink();assert sha256(p.read_bytes()).hexdigest()==digest,name
d=json.loads((P/"aggregate_summary.json").read_text());r=d["record_framework"];x=d["report_inventory"];t=x["terminal_counts"]
assert r["records_identified"]-r["duplicates_removed"]==r["records_screened"]==21940
assert r["records_excluded_at_record_phase"]+r["record_groups_advanced_to_report_or_resource_assessment"]==21940
assert x["reports_sought"]==3114 and x["available_source_assessed"]==2385
assert sum(t.values())==3114 and t["not_retrieved"]==729 and t["included_reports"]==205
assert sum(x["required_extent_not_retrieved_split"].values())==729
assert 125+80==205 and 14156-375==13781
q=d["actual_author_intake_aggregate"];assert q["receipt_files"]==3 and q["choices"]==69 and q["two_reviewer_agreements"]+q["actual_third_author_adjudications"]==23
assert d["new_only_author_review"]["current_posted_registry_module_source_use_cases"]*3==123
with(P/"current_report_identity_and_stage3114.tsv").open()as f:rows=list(csv.DictReader(f,delimiter="\t"))
assert len(rows)==len({r["own_report_id"]for r in rows})==3114
with(P/"selected_result_to_source_cluster125.tsv").open()as f:rows=list(csv.DictReader(f,delimiter="\t"))
assert len(rows)==125 and len({r["current_report_counting_cluster_key"]for r in rows})==121
l=d["limits"];assert l["counts_locked_at_available_cutoff"] and not l["whole_review_final_eligibility_complete"] and not l["submission_ready"] and l["whole_review_unique_N"]is None
assert d["analysis"]["new_effect_inputs"]==d["analysis"]["new_fits"]==d["analysis"]["new_RoB2_or_GRADE"]==0
print(json.dumps({"status":"PASS_FINITE_AVAILABLE_CUTOFF_COUNTS_AND_DERIVED_LINKAGE_ONLY","reports":3114,"selected_results":125,"primary_clusters":121,"whole_review_final_eligibility":False},indent=2))
