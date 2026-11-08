from pathlib import Path
import csv,json,hashlib
H=Path(__file__).resolve().parent
for line in(H/'MANIFEST.sha256').read_text().splitlines():
 s,n=line.split('  ',1);assert hashlib.sha256((H/n).read_bytes()).hexdigest()==s,n
a=json.loads((H/'aggregate_summary.json').read_text());r=list(csv.DictReader((H/'existing_source_roles27.tsv').open(),delimiter='\t'))
assert len(r)==len({x['own_report_id']for x in r})==27
assert sum(x['reused_role']=='SAME_ADOPTED_MOTHER_DISTINCT_COMPANION'for x in r)==11
assert sum(x['reused_role']=='EXISTING_SIGNED_NO_RANDOMIZED_SELF_RESULT_ROLE'for x in r)==16
assert 29490-7566==21924==18827+3097
assert 3098==726+2372 and 2372==1593+301+229+249 and 249==140+109
assert a['source_disposition_numerator']==2372-301==2071
assert abs(a['source_disposition_percent']-2071/2372*100)<1e-10
assert a['whole_review_independent_K']is None and a['unique_female_N']is None and a['whole_work_completion_percent']is None
assert a['new_author_scientific_votes']==0 and a['new_source_effects_models_RoB2_or_GRADE']==0 and not a['submitted']
print('PASS reused27 current source roles and count equations; no new human decisions or whole-study completion claim')
