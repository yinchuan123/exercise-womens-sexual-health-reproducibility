from pathlib import Path
import csv,json,hashlib
H=Path(__file__).resolve().parent
for line in (H/'MANIFEST.sha256').read_text().splitlines():
 s,n=line.split('  ',1);assert hashlib.sha256((H/n).read_bytes()).hexdigest()==s,n
a=json.loads((H/'aggregate_summary.json').read_text())
f=list(csv.DictReader((H/'source_family136_reported_N_replay.tsv').open(),delimiter='\t'))
r=list(csv.DictReader((H/'selected_report140_typed_N_projection.tsv').open(),delimiter='\t'))
assert 29490-7566==21924==18827+3097
assert 3097+3-2==3098==726+2372
assert 2372==213+1593+328+238 and 238==140+98
assert len(r)==140 and len(f)==136
known=[x for x in f if x['reported_source_N_contribution']]
assert len(known)==132 and sum(int(x['reported_source_N_contribution']) for x in known)==15619
by={}
for x in r:
 if x['reported_source_N_for_replay']:by.setdefault(x['source_dependency_group'],[]).append(int(x['reported_source_N_for_replay']))
assert len(by)==132 and sum(max(v) for v in by.values())==15619
assert a['unique_female_N'] is None and a['final_independent_whole_review_K'] is None
assert a['whole_work_completion_percent'] is None and not a['submission_ready']
assert abs(a['source_disposition_percent']-2044/2372*100)<1e-10
print('PASS exact-publication alias, current count equations and source-N replay; not whole-study completion')
