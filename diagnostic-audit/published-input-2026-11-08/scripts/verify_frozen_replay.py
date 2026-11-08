# coding: utf-8
from pathlib import Path
import json,math,hashlib
O=Path(__file__).resolve().parent.parent
J=lambda p:json.loads(p.read_text());H=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();F=J(O/'data/FROZEN_PUBLISHED_INPUT_IMPACT_AUDIT.json');R=J(O/'replay/PUBLISHED_INPUT_IMPACT_AUDIT.json');P=J(O/'data/IMPACT_AUDIT_PLAN.json');I=J(O/'data/SCENARIO_INPUTS11.json')['scenario_inputs'];Q=J(O/'replay/INDEPENDENT_IMPACT_CHECK.json')
assert set(F['results'])==set(R['results'])==set(I)=={x['id']for x in P['scenarios']};checks=[]
def compare(a,b,path=''):
 out=[]
 if isinstance(a,dict):
  assert set(a)==set(b),(path,'keys')
  for k in a:out+=compare(a[k],b[k],path+'/'+k)
 elif isinstance(a,list):
  assert len(a)==len(b),(path,'list-length')
  for i,(x,y)in enumerate(zip(a,b)):out+=compare(x,y,path+'/'+str(i))
 elif isinstance(a,(float,int))and not isinstance(a,bool):
  assert isinstance(b,(float,int))and math.isfinite(a)and math.isfinite(b),(path,'finite-number')
  delta=abs(a-b);tol=1e-10*max(1.,abs(a));assert delta<=tol,(path,delta,tol);out.append({'path':path,'frozen':a,'replayed':b,'absolute_difference':delta,'tolerance':tol})
 else:assert a==b,(path,a,b)
 return out
inputchecks=compare(I,R['scenario_inputs'],'/scenario_inputs')
for sid,f in F['results'].items():
 assert f['independent_trial_k']is None and f['valid_clinical_pool']is False and f['project_primary_model']is False
 for model in ['fixed','random_REML_modified_HK']:
  d=compare(f[model],R['results'][sid][model],f'/results/{sid}/{model}');checks.append({'fit_id':sid+':'+('IV_FIXED'if model=='fixed'else'REML_MHK'),'numeric_fields_checked':len(d),'max_absolute_difference':max(x['absolute_difference']for x in d),'fields':d,'pass':True})
assert len(checks)==22 and Q['checked_scenario_count']==11 and all(x['pass']for x in Q['scenario_checks'])and not Q['errors_found']
z={'status':'PASS_ENGINEERING_REPLAY_OF_SAME22_HISTORICAL_FITS','scope':'Existing diagnostic scenario-model runs only;0newunique scientific models; separate current clinical6unchanged.','model_fit_summaries_replayed':22,'scenarios':11,'numeric_output_fields_checked':sum(x['numeric_fields_checked']for x in checks),'per_scenario_input_numeric_fields_checked':len(inputchecks),'maximum_saved_output_absolute_difference':max(x['max_absolute_difference']for x in checks),'independent_scalar_REML_QA_pass_for11':True,'independent_max_tau2_absolute_difference':max(x['tau2_abs_difference_from_metafor']for x in Q['scenario_checks']),'independent_max_mu_SE_CI_PI_absolute_difference':max(x['max_mu_SE_CI_PI_abs_difference_from_metafor']for x in Q['scenario_checks']),'frozen_output_sha256':H(O/'data/FROZEN_PUBLISHED_INPUT_IMPACT_AUDIT.json'),'replay_output_sha256':H(O/'replay/PUBLISHED_INPUT_IMPACT_AUDIT.json'),'replay_QA_sha256':H(O/'replay/INDEPENDENT_IMPACT_CHECK.json'),'models':checks,'no_new_clinical_eligibility_or_effect_admission_or_GRADE':True}
(O/'replay/FROZEN_REPLAY_VERIFICATION.json').write_text(json.dumps(z,ensure_ascii=False,indent=2)+'\n');print({k:v for k,v in z.items()if k not in ['models']})
