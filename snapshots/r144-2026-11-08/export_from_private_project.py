# SPDX-License-Identifier: MIT
"""Export derived stage/identity data from the closed local project; no source prose or receipt files."""
from pathlib import Path
import json,csv,argparse

def export(project,output):
 root=Path(project)/'outputs';h=root/'bmj_r144_source_identity_and_final_clinical_review_20261108';out=Path(output);out.mkdir(parents=True,exist_ok=True)
 flow=json.loads((h/'report_flow_current/R144_REPORT_FLOW_CURRENT.json').read_text());rows=flow['rows'];summary=flow['summary'];r=summary['record_identification'];t=summary['report_terminal_counts']
 assert r['records_identified']-r['duplicates_removed']==r['records_screened']==21924
 assert summary['own_report_nodes_sought_or_assessed']==len(rows)==3099 and sum(t.values())==3099
 fields=['canonical_own_report_id','record_groups','title','own_DOIs','own_PMIDs','own_registry_primary_ids','formal_current_flow','coarse_actual_source_extent','source_report_role','selected_source_slot','confirmed_adopted_mother_family_ids']
 with(out/'current_report_identity_and_stage3099.tsv').open('w',encoding='utf-8',newline='')as f:
  w=csv.DictWriter(f,fieldnames=fields,delimiter='\t',lineterminator='\n');w.writeheader();w.writerows({k:json.dumps(a.get(k),ensure_ascii=False,separators=(',',':'))if isinstance(a.get(k),(dict,list))else a.get(k,'')for k in fields}for a in rows)
 p=out/'current_report_identity_and_stage3099.tsv';p.write_text(p.read_text())
 m=json.loads((h/'report_flow/CANONICAL_RECORD_AND_OWN_REPORT_MAP.json').read_text());x={'record_alias_to_canonical':m['record_alias_to_canonical'],'own_report_alias_to_canonical':m['own_report_alias_to_canonical'],'same_parent_edges_are_not_own_report_aliases':True,'new_clinical_adoption':False};(out/'verified_same_own_record_and_report_aliases.json').write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n')
 # Aggregate policy/status constants are the frozen public declaration, not a reconstruction of individual patients or votes.
 baseline=json.loads((Path(__file__).parent/'aggregate_summary.json').read_text());assert baseline['record_framework']==r and baseline['terminal_counts']==t
 a=json.loads((root/'bmj_r143_s27_actual_intake_20261108/actual_intake/APPLIED_S27_AUTHOR_DECISIONS.json').read_text())['counts'];assert a['actual_case_count']==41 and a['actual_author_cells']==123 and a['two_named_reviewers_actual_agreements']==41
 (out/'aggregate_summary.json').write_text(json.dumps(baseline,ensure_ascii=False,indent=2)+'\n')
 print('Derived3file export complete; original evidence, correspondence and actual author files excluded.')
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--project',required=True,type=Path);p.add_argument('--output',required=True,type=Path);a=p.parse_args();export(a.project,a.output)
