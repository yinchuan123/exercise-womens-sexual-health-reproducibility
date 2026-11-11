from pathlib import Path
from collections import Counter
import hashlib,csv,json
S=Path(__file__).resolve().parent
m=json.loads((S/'MANIFEST_SHA256.json').read_text())
for x in m['files']:
 b=(S/x['name']).read_bytes();assert len(b)==x['bytes'] and hashlib.sha256(b).hexdigest()==x['sha256'],x['name']
def tab(n):
 with(S/n).open(encoding='utf-8-sig',newline='')as f:return list(csv.DictReader(f,delimiter='\t'))
a=json.loads((S/'aggregate_counts.json').read_text());r=tab('report_dispositions3087.tsv');g=tab('principal_report_groups191.tsv');q=tab('aliases_or_containers11.tsv');w=tab('awaiting_classification48.tsv')
assert len(r)==len({x['report_id']for x in r})==3087
assert len(q)==11 and not(set(x['report_id']for x in q)&set(x['report_id']for x in r))
c=Counter(x['cutoff_disposition']for x in r)
assert c==dict(INCLUDED_PRINCIPAL_RESULT_REPORT=191,INCLUDED_COMPANION_REPORT_NO_ADDITIONAL_TRIAL=139,AWAITING_CLASSIFICATION_AT_FINAL_EVIDENCE_CUTOFF=48,NOT_RETRIEVED_AT_FIXED_CUTOFF=499,PROTOCOL_OR_OTHER_NONCONTRIBUTING_REPORT_CONTEXT=1701,EXCLUDED_WITH_EXISTING_SOURCE_REASON=509)
assert 3087==499+2588 and 2588==509+1701+48+330 and 330==191+139
assert 29490-7566==21924==18827+3097 and 3097-1+4-13==3087
assert len(g)==191 and len({x['conservative_trial_group']for x in g})==187
assert set(x['report_id']for x in g)==set(x['report_id']for x in r if x['cutoff_disposition']=='INCLUDED_PRINCIPAL_RESULT_REPORT')
G=set(x['conservative_trial_group']for x in g)
assert all(x['conservative_trial_group']in G for x in r if x['cutoff_disposition']=='INCLUDED_COMPANION_REPORT_NO_ADDITIONAL_TRIAL')
assert len(w)==48 and set(x['report_id']for x in w)==set(x['report_id']for x in r if x['cutoff_disposition']=='AWAITING_CLASSIFICATION_AT_FINAL_EVIDENCE_CUTOFF')
L=tab('record_report_links.tsv');b=json.loads((S/'record_report_identity_bridge.json').read_text());assert len({x['record_group']for x in L})+b['bibliographic_container_without_distinct_sought_report']==3097;assert len(L)==3100 and len({x['canonical_own_report']for x in L})==3087
assert a['actual_final_choice_cells']==15 and a['initial_unique_female_N']is None and not a['all_source_eligibility_gaps_resolved']
k=json.loads((S/'result_risk_and_certainty.json').read_text());assert len(k['risk_targets'])==166 and len(k['certainty_record_views'])==91 and len(k['existing_disagreements'])==8
assert len(json.loads((S/'result_risk_signals166.json').read_text())['targets'])==166
assert not k['all187_groups_all_outcome_coverage'] and not a['formal_submission_performed'] and not a['preprint_published']
print('PASS R193 current cutoff:3087 distinct reports;330 included;48 awaiting;499 not retrieved;187 conservative strategy groups;unique female N not asserted;existing scoped risk/certainty retained')
