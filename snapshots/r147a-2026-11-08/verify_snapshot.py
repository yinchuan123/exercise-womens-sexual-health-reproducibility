from pathlib import Path
from hashlib import sha256
import json
H=Path(__file__).resolve().parent
for line in (H/'MANIFEST.sha256').read_text().splitlines():
 s,n=line.split('  ',1);assert sha256((H/n).read_bytes()).hexdigest()==s,n
a=json.loads((H/'aggregate_summary.json').read_text())
assert a['actual_S30_author_approvals']==3 and a['current_full_manuscript_author_approval']
assert a['administrative_Authors_status_paragraph_changes']==1
assert not a['main_Word_PDF_bytes_identical_to_preapproval_snapshot']
assert a['all_other_main_paragraphs_and87references_literal_unchanged']and a['new_scientific_changes_after_S30']==0
assert a['certified_whole_review_independent_K']is None and a['unique_adult_female_N']is None
assert not a['whole_review_complete']and not a['submission_authorized']and not a['preprint_authorized']and not a['submitted']
assert 3099==727+2372 and 2372==213+1593+328+238 and 238==140+98
print('PASS administrative approval statement only; scientific content and source-fact limits unchanged; no external release')
