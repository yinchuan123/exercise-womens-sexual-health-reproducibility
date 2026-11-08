# SPDX-License-Identifier: MIT
from pathlib import Path
from hashlib import sha256
import json
P=Path(__file__).resolve().parent
for line in(P/"MANIFEST.sha256").read_text().splitlines():
 digest,name=line.split("  ",1);p=P/name;assert p.resolve().is_relative_to(P)and not p.is_symlink();assert sha256(p.read_bytes()).hexdigest()==digest,name
d=json.loads((P/"aggregate_summary.json").read_text());r=d["record_framework"];a=d["dated_record_phases"];e=d["source_extent_flags_not_eligibility"];x=d["this_round"];l=d["limits"]
assert r["identified"]-r["duplicates"]==r["canonical_groups"]==sum(d["legacy_working_routes_before_stage_migration"].values())==21940
assert a["record_screen_excluded"]+a["record_groups_advanced_to_report_or_resource_assessment"]==21940
assert sum(e.values())==3113 and d["bounded_own_report_nodes"]==3114
assert x["new_only_human_cases"]*3==x["new_only_role_choice_cells"]==69
assert x["new_formal_human_receipts"]==x["new_models"]==x["new_effect_inputs"]==x["new_GRADE"]==0
assert l["whole_review_independent_K"]is None and l["whole_review_unique_N"]is None and l["all_reports_of_included_studies"]is None
assert not l["whole_review_final_PRISMA"]and not l["submission_ready"]
print(json.dumps({"status":"PASS_SOURCE_IDENTITY_AND_DATED_STAGE_AGGREGATES_ONLY","snapshot":d["snapshot_id"],"canonical_records":21940,"final_PRISMA":False},indent=2))
