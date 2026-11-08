# SPDX-License-Identifier: MIT
from pathlib import Path
from hashlib import sha256
import json
P=Path(__file__).resolve().parent
def verify():
    for line in (P/"MANIFEST.sha256").read_text().splitlines():
        digest,name=line.split("  ",1);f=P/name
        assert f.resolve().is_relative_to(P)and not f.is_symlink()
        assert sha256(f.read_bytes()).hexdigest()==digest,name
    d=json.loads((P/"aggregate_summary.json").read_text());s=json.loads((P/"schema.json").read_text())
    assert set(d)==set(s["required"])
    assert {k:type(v).__name__ for k,v in d.items()}==s["top_level_types"]
    f=d["record_framework"];a=d["actual_author_review"];acts=d["applied_source_actions"];r=d["this_round"];b=d["limits"]
    assert f["identified"]-f["duplicates"]==f["canonical_groups"]==sum(d["current_working_routes"].values())==21955
    assert a["receipt_files"]==3 and a["top_level_choice_cells"]==18
    assert a["source_actions_per_role"]==sum(acts.values())==415
    assert a["actual_source_action_cells"]==a["receipt_files"]*a["source_actions_per_role"]==1245
    assert a["two_reviewer_differences_using_actual_adjudicator"]==22
    assert a["adjudicator_dissent_to_agreed_reviewers_retained"]==27
    assert a["source_action_differences_preserved"]==49
    assert acts["CLOSE_OWN_NONRESULT_OR_NONRANDOM_SOURCE_KEEP_PARENT"]+acts["CLOSE_OWN_OUTSIDE_ADULT_FEMALE_OR_ACTIVE_TASK_SCOPE_KEEP_PARENT"]==r["own_record_screen_closures"]==379
    assert 18456+r["own_record_screen_closures"]==d["current_working_routes"]["RECORD_SCREEN_EXCLUDED"]
    assert r["new_model_inputs"]==r["new_models"]==r["new_GRADE"]==r["parent_trial_exclusions"]==0
    assert b["whole_review_independent_K"]is None and b["whole_review_unique_N"]is None
    assert b["final_PRISMA"]is False and b["submission_ready"]is False
    return {"status":"PASS_ACTUAL_SOURCE_ADOPTION_AGGREGATES_ONLY","snapshot":d["snapshot_id"],"receipt_files":3,"source_actions_per_role":415,"new_models":0,"final_PRISMA":False}
if __name__=="__main__":print(json.dumps(verify(),indent=2))
