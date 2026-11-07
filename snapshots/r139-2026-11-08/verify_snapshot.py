# SPDX-License-Identifier: MIT
from pathlib import Path
from hashlib import sha256
import json
P=Path(__file__).resolve().parent
def verify():
    for line in (P/"MANIFEST.sha256").read_text().splitlines():
        digest,name=line.split("  ",1);f=P/name
        assert f.resolve().is_relative_to(P) and not f.is_symlink()
        assert sha256(f.read_bytes()).hexdigest()==digest,name
    d=json.loads((P/"aggregate_summary.json").read_text());s=json.loads((P/"schema.json").read_text())
    assert set(d)==set(s["required"])
    assert {k:type(v).__name__ for k,v in d.items()}==s["top_level_types"]
    f=d["record_framework"];r=d["this_round"];lim=d["limits"]
    assert f["identified"]-f["duplicates"]==f["canonical_groups"]==sum(d["current_working_routes"].values())
    assert 7497+r["same_published_report_aliases"]==f["duplicates"]
    assert 21993-r["same_published_report_aliases"]==f["canonical_groups"]
    assert r["source_qualification_rows"]==1277 and r["old_specific_author_fact_own_source_actions"]==499
    assert r["unadopted_proposal_rows_before_alias"]==417 and r["canonical_unadopted_sources"]==415
    assert r["new_human_signatures"]==r["new_model_inputs"]==r["new_models"]==r["new_GRADE"]==0
    assert lim["final_PRISMA"]is False and lim["submission_ready"]is False
    assert lim["whole_review_independent_K"]is None and lim["whole_review_unique_N"]is None
    assert d["previously_adopted_anchor"]["whole_search_final"]is False
    return {"status":"PASS_DERIVED_PROCESS_ONLY","snapshot":d["snapshot_id"],"canonical_groups":f["canonical_groups"],"new_clinical_models":0,"final_PRISMA":False}
if __name__=="__main__":print(json.dumps(verify(),indent=2))
