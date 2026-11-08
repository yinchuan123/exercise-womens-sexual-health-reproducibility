from pathlib import Path
from hashlib import sha256
from collections import Counter
import json,csv
H=Path(__file__).resolve().parent
for line in(H/'MANIFEST.sha256').read_text().splitlines():
 s,n=line.split('  ',1);assert sha256((H/n).read_bytes()).hexdigest()==s,n
a=json.loads((H/'aggregate_summary.json').read_text());r=list(csv.DictReader((H/'current_report_identity_and_stage3099.tsv').open(),delimiter='\t'));c=list(csv.DictReader((H/'selected_result_to_source_group140.tsv').open(),delimiter='\t'));u=list(csv.DictReader((H/'actual_S28_source_use49.tsv').open(),delimiter='\t'))
assert len(r)==len({v['own_report_id']for v in r})==3099
assert 29490-7566==21924==18827+3097 and 3099==727+2372 and 2372==213+1593+328+238
assert len(c)==140 and len({v['current_report_counting_cluster_key']for v in c})==136 and len(u)==49 and Counter(v['action']for v in u)==Counter({'A':15,'B':21,'C':13})
assert a['certified_whole_review_independent_K']is None and a['unique_adult_female_N']is None
assert a['new_pooled_fits']==0 and a['new_certainty_targets_pending_actual_author_adoption']==4
print('PASS currentfinitecountflow/140sources/49actualsourceuses/unknownKandNpreserved;notclinicalvalidationorsubmission')
