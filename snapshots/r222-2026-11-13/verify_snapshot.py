"""Offline integrity, count, membership and boundary checks for this snapshot.

This verifies aggregate artifacts, not personal signatures, source acquisition,
whole-review duplicate reading, clinical transitivity or submission authority.
"""
import hashlib,json,math,re
from collections import Counter
from pathlib import Path

HERE=Path(__file__).resolve().parent
checks=[]
def read(name):return json.loads((HERE/name).read_text())
def check(label,condition):
 checks.append({'check':label,'pass':bool(condition)})
 if not condition:raise AssertionError(label)
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()

manifest=read('PUBLIC_MANIFEST.json')
for row in manifest['files']:
 p=HERE/row['path'];check('hash:'+row['path'],p.is_file() and p.stat().st_size==row['bytes'] and sha(p)==row['sha256'])
files=[p for p in HERE.rglob('*') if p.is_file() and not p.name.startswith('._') and '__pycache__' not in p.parts]
check('exact snapshot allowlist',set(str(p.relative_to(HERE)) for p in files)==set(r['path'] for r in manifest['files'])|{'PUBLIC_MANIFEST.json'})
L=read('inputs/pool_sets39.json');pools=L['pools'];pm={p['pool_id']:p for p in pools}
check('39 distinct overlapping input sets',len(pools)==len(pm)==39)
check('three source locks with8/30/1sets',Counter(p['source_lock_id'] for p in pools)=={'r221-initial8':8,'r221-additional30':30,'r221-inclusive14':1})
catalog=read('inputs/source_assets.json')['source_carriers'];cm={r['source_id']:r for r in catalog}
for p in pools:
 rows=p['rows'];check('K-membership:'+p['pool_id'],p['K']==len(rows)==len(set(r['family_id'] for r in rows)) and p['member_input_ids']==[r['input_id'] for r in rows] and p['member_family_ids']==[r['family_id'] for r in rows])
 check('finite yi positive vi:'+p['pool_id'],all(math.isfinite(r['yi']) and math.isfinite(r['vi']) and r['vi']>0 for r in rows))
 check('licensed source hash links:'+p['pool_id'],all(r['source_assets'] and all(a['source_id'] in cm and a['sha256']==cm[a['source_id']]['sha256'] for a in r['source_assets']) for r in rows))
 for layer in ['n_analysis_source','N_randomized_family_source','N_randomized_selected_source']:
  n=p.get('N_layers',{}).get(layer)
  if n:
   vals=[r.get(layer) for r in rows if r.get(layer) is not None]
   check('N-layer:'+p['pool_id']+':'+layer,n['known_sum']==(sum(vals) if vals else None) and n['known_families']==len(vals) and n['model_families']==len(rows) and n['complete']==(len(vals)==len(rows)) and n['not_unique_whole_review_N'])
F=read('data/frequentist_results78.json')['rows'];B=read('data/bayesian_results54.json')['rows'];LOO=read('data/leave_one_family_out45.json')['rows']
check('78frequencyviews two per input set',len(F)==78 and Counter(r['pool_id'] for r in F)=={k:2 for k in pm})
for r in F+B:
 p=pm[r['pool_id']];check('result-members:'+r['pool_id']+':'+str(r.get('method')),r['K']==p['K'] and r['members']==p['member_input_ids'] and r['N_layers']==p['N_layers'])
plans=[(p['pool_id'],b['tau_half_normal_SD'],b['computation']) for p in pools for b in p['bayesian_replay_plan']]
check('54Bayesian51MCMC3deterministic',len(B)==54 and len(plans)==54 and sum(r[2]=='MCMC' for r in plans)==51 and sum(r[2]=='deterministic_marginal_tau_quadrature' for r in plans)==3)
check('Bayes priors match plans',Counter((b['pool_id'],b['tau_prior_half_normal_SD']) for b in B)==Counter((p,s) for p,s,_ in plans))
check('45LOO views',len(LOO)==45)
for r in LOO:
 p=pm[r['pool_id']];check('single family omission:'+r['pool_id']+':'+r['omitted_input'],r['K']==p['K']-1 and r['members']==[i for i in p['member_input_ids'] if i!=r['omitted_input']])
inc=pm['BROAD_INCLUSIVE14_ORDINARY_CI_WITH_BASGOL'];base=pm['BROAD_COMPLETE_STRATEGY13_ORDINARY_CI_EQUIVALENTS']
check('inclusive14 preserves13 and addsBasgolonce',inc['rows'][:13]==base['rows'] and len(inc['rows'])==14 and sum('Basgol' in r['input_id'] for r in inc['rows'])==1)
D=read('qa/mcmc_diagnostics51.json')['rows'];check('51diagnostics',len(D)==51)
for d in D:
 check('convergence:'+d['pool_id']+':'+str(d['tau_prior_SD']),d['pass'] and d['chains']==4 and d['iterations_per_chain']==10000 and d['warmup_per_chain']==2500 and d['divergences']==0 and d['treedepth_hits']==0 and min(d['E_BFMI'])>.3 and all(z['Rhat']<=1.01 and z['ESS_bulk']>=1000 and z['ESS_tail']>=1000 and z['MCSE_mean']/z['SD']<.05 for z in d['parameters']))
G=read('data/new_certainty_targets11.json')['targets'];check('11new exact grades8Low3Verylow',len(G)==11 and Counter(g['grade'] for g in G)=={'Low':8,'Very low':3})
for g in G:check('exactgrade:'+g['target_id'],g['author_agreement_count']==g['author_count']==3 and g['all_three_agree'] and len(g['five_domains'])==5 and sum(d['downgrade_levels'] for d in g['five_domains'])==(2 if g['grade']=='Low' else 3))
net=read('inputs/conditional_pain_network.json');nr=read('data/conditional_pain_network_results.json');top=nr['topology']
check('network three families four nodes no residual or loop',len({r['family_id'] for r in net['trials']})==3 and top['nodes']==4 and top['edges']==3 and top['rank_X']==3 and top['residual_degrees_of_freedom']==0 and top['independent_closed_loops']==0)
check('conditionalnetwork four tau views six pairs',len(nr['rows'])==4 and all(len(r['pairs'])==6 and r['no_MCMC_or_convergence_claim'] and all(p['pair_CrI_direct_mixture_not_subtracted_marginal_CrI'] for p in r['pairs']) for r in nr['rows']))
A=read('data/author_adoption_aggregate.json');cut=A['factual_cutoff_preserved'];check('aggregate adoption not submission',A['actual_author_count']==3 and A['new_question_count']==16 and A['unanimous_questions']==15 and not A['new_whole_manuscript_approval'] and not A['formal_submission_authorized'] and not A['formal_submission_performed'] and A['new_original_readings_attested']==0)
check('anonymous display disagreement retained',A['retained_presentation_difference']['anonymous_votes']=={'A':1,'B':2} and A['retained_presentation_difference']['majority_not_automatic_formal_adjudication'])
check('fixedcutoff not globalKN',cut=={'included_reports':340,'conservative_strategy_groups_not_global_independent_K':194,'eligibility_unascertainable':40,'unretrieved':499,'initial_female_N_gaps':8,'dependency_pairs':2,'whole_review_unique_female_N':None,'whole_review_independent_K':None})
check('eightdose maps no optimized dose fit',read('data/dose_prescription_map8.json')['count']==8 and read('data/dose_prescription_map8.json')['no_common_dose_response_fitted'])
for p in files:
 text=p.read_text();private_prefixes=['/'+x+'/' for x in ['Users','Volumes','var/folders']];check('no local private path:'+str(p.relative_to(HERE)),not any(x in text for x in private_prefixes))
 check('safe public filetype:'+str(p.relative_to(HERE)),p.suffix in {'.json','.md','.txt','.py','.R','.stan'})
print(json.dumps({'status':'PASS','checks_passed':len(checks),'snapshot_file_count':len(files),'frequency_views':78,'Bayesian_views':54,'MCMC_views':51,'deterministic_views':3,'input_sets':39,'conditional_network_only':True,'signature_or_whole_review_reading_verification':False},indent=2))
