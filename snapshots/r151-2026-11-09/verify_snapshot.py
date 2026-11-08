import csv,json,hashlib,collections
from pathlib import Path
S=Path(__file__).resolve().parent
manifest=json.loads((S/'MANIFEST_SHA256.json').read_text())
for f in manifest['files']:
 raw=(S/f['name']).read_bytes();assert len(raw)==f['bytes'];assert hashlib.sha256(raw).hexdigest()==f['sha256']
a=json.loads((S/'aggregate_counts.json').read_text())
def rows(p):
 with(S/p).open(newline='',encoding='utf-8')as f:return list(csv.DictReader(f,delimiter='\t'))
r=rows('report_dispositions3098.tsv');g=rows('source_families139.tsv');s=rows('actual_S32_source_actions17.tsv')
assert len(r)==len({x['own_report_id']for x in r})==3098
counts=dict(collections.Counter(x['terminal_partition']for x in r));assert counts==a['report_terminal_partition']
assert counts==dict(included=263,awaiting_classification=104,not_retrieved=725,excluded_own_source_use=356,protocol_or_associated_no_current_target_result_inventory=1650)
assert 3098==725+2373 and 2373==356+1650+104+263 and 3097+4-3==3098
z=a['record_identification'];assert 29490==17574+10937+979 and 29490-7566==21924==18827+3097
selected=[x for x in r if x['selected_result_source']=='True'];assert len(selected)==143 and 263-143==120
assert len(g)==len({x['counting_cluster_key']for x in g})==139
known=[int(x['source_N_subtotal_contribution'])for x in g if x['source_N_subtotal_contribution']!=''];assert len(known)==135 and sum(known)==15833
assert len(s)==17 and len(json.loads((S/'actual_S32_result_risk3.json').read_text())['rows'])==3
assert abs(a['source_disposition_percent']-2269/2373*100)<1e-10
assert not a['new_S33_adoption_assumed']and not a['submitted']and not a['authorizes_submission']
print('PASS R151:3098 reports;263included;104information-limited/pending;143sources/139families;reported source N15833;actual S32 20cases;S33 not adopted')
