"""Portable replay of the actual conditional pain-network calculation.
No transitivity certification, treatment ranking, new GRADE or new source acquisition.
"""
import json,math,argparse
from pathlib import Path
import numpy as np
from scipy.integrate import quad,cumulative_trapezoid
from scipy.optimize import minimize_scalar,brentq
from scipy.special import ndtr
from scipy.stats import norm
ap=argparse.ArgumentParser();ap.add_argument('--output',default='out-r222');args=ap.parse_args()
HERE=Path(__file__).resolve().parents[1];OUT=Path(args.output);OUT.mkdir(parents=True,exist_ok=True)
L=json.loads((HERE/'inputs/conditional_pain_network.json').read_text())
expected=json.loads((HERE/'data/conditional_pain_network_results.json').read_text())['rows']
X=np.array(L['design_matrix_X'],float);y=np.array([r['y'] for r in L['trials']]);v=np.array([r['vi'] for r in L['trials']]);prior=25*np.eye(3);priorprec=np.eye(3)/25
pairdefs=[('PT','LIDO',[1,0,0]),('CBCT','LIDO',[0,1,0]),('ICBT','LIDO',[0,0,1]),('PT','CBCT',[1,-1,0]),('PT','ICBT',[1,0,-1]),('CBCT','ICBT',[0,1,-1])]
issues=[]
def test(label,a,b,atol=3e-5,rtol=1e-7):
 ok=bool(np.allclose(a,b,atol=atol,rtol=rtol))
 if not ok:issues.append({'check':label,'primary':np.asarray(a).tolist(),'independent':np.asarray(b).tolist(),'atol':atol,'rtol':rtol})
 return ok
def cond(t):
 t=np.asarray(t);w=1/(v+t[...,None]**2);A=np.einsum('ai,...a,aj->...ij',X,w,X)+priorprec;cov=np.linalg.inv(A);bb=np.einsum('ai,...a,a->...i',X,w,y);mean=np.einsum('...ij,...j->...i',cov,bb);return mean,cov,A,bb
def altcond(t):
 R=prior @ X.T @ np.linalg.inv(X @ prior @ X.T+np.diag(v+t*t));m=R @ y;cov=prior-R @ X @ prior;return m,cov
def logprimary(t,sd):
 t=np.asarray(t);m,S,A,b=cond(t);sg,ld=np.linalg.slogdet(25*A);assert np.all(sg>0)
 return -.5*(np.sum(np.log(v+t[...,None]**2),axis=-1)+np.sum(y*y/(v+t[...,None]**2),axis=-1)-np.sum(b*m,axis=-1)+ld)-.5*(t/sd)**2
def logalternate(t,sd):
 t=np.asarray(t);base=X @ prior @ X.T;C=np.broadcast_to(base,t.shape+(3,3)).copy();idx=np.arange(3);C[...,idx,idx]+=v+t[...,None]**2;sg,ld=np.linalg.slogdet(C);yy=np.broadcast_to(y,t.shape+(3,));sol=np.linalg.solve(C,yy[...,None])[...,0]
 return -.5*(ld+np.sum(yy*sol,axis=-1))-.5*(t/sd)**2
for tau in [0,.1,.5,1,2,5,10]:
 m,c,_,_=cond(tau);am,ac=altcond(tau);test('conditionalmeanparameterisationtau'+str(tau),m,am,1e-11,1e-11);test('conditionalcovparameterisationtau'+str(tau),c,ac,1e-11,1e-11)
for sd in [.5,1,2]:test('marginaltau_primary_v_marginalMVN_SD'+str(sd),logprimary(np.array([0,.1,.5,1,2,5,10]),sd),logalternate(np.array([0,.1,.5,1,2,5,10]),sd),1e-11,1e-11)
result=[];gridqa=[]
for sd in [1,.5,2,0]:
 fixed=sd==0;U=max(24.,12*sd);shift=0.;Z=1.;err=0.
 if not fixed:
  xx=np.linspace(0,U,1001);ii=int(np.argmax(logprimary(xx,sd)));opt=minimize_scalar(lambda z:-float(logprimary(z,sd)),bounds=(xx[max(0,ii-1)],xx[min(1000,ii+1)]),method='bounded');shift=max(float(logprimary(0,sd)),float(logprimary(opt.x,sd)))
  dens=lambda t:float(np.exp(logprimary(t,sd)-shift));Z,err=quad(dens,0,np.inf,epsabs=2e-11,epsrel=2e-11,limit=250)
 def integrate(f):return float(f(0)) if fixed else quad(lambda t:dens(t)*float(f(t)),0,np.inf,epsabs=1e-10,epsrel=1e-10,limit=250)[0]/Z
 means=np.array([integrate(lambda t,i=i:cond(t)[0][i]) for i in range(3)]);second=np.array([[integrate(lambda t,i=i,j=j:cond(t)[1][i,j]+cond(t)[0][i]*cond(t)[0][j]) for j in range(3)] for i in range(3)]);marginalcov=second-np.outer(means,means)
 pairs=[]
 for first,second,c in pairdefs:
  c=np.array(c,float)
  def at(t):
   mm,SS,_,_=cond(t);return float(c @ mm),float(c @ SS @ c)
  mean=float(c @ means)
  def cdf(z):return integrate(lambda t:ndtr((z-at(t)[0])/math.sqrt(at(t)[1])))
  qs=[float(brentq(lambda z:cdf(z)-p,-100,100,xtol=2e-9)) for p in [.025,.5,.975]]
  prob=integrate(lambda t:ndtr(-at(t)[0]/math.sqrt(at(t)[1])))
  pairs.append({'first':first,'second':second,'difference_definition':first+'minus'+second+';negativefavoursthefirst','posterior_mean':mean,'CrI025_50_975':qs,'Pr_first_has_lower_mean_pain':prob,'probability_not_individual_response':True,'posterior_variance_using_full_basic_effect_covariance':float(c @ marginalcov @ c),'pair_CrI_direct_mixture_not_subtracted_marginal_CrI':True})
 tau_mean=integrate(lambda t:t)
 if fixed:tqs=[0.,0.,0.]
 else:
  def tcdf(z):return quad(dens,0,z,epsabs=1e-11,limit=250)[0]/Z
  tqs=[float(brentq(lambda z:tcdf(z)-p,0,U,xtol=1e-9)) for p in [.025,.5,.975]]
 # Independent numericalmethod:directmarginalN(y;0,XpriorX'+diagS)and dense trapezoidal grids.
 gg=[]
 for ngrid in ([1] if fixed else [16385,32769]):
  tt=np.array([0.]) if fixed else np.linspace(0,U,ngrid);mm,SS,_,_=cond(tt)
  assert np.all(np.isfinite(mm)) and np.all(np.isfinite(SS))
  if fixed:ww=np.ones(1)
  else:
   logg=logalternate(tt,sd);raw=np.exp(logg-np.max(logg));ww=raw/np.trapezoid(raw,tt)
  def gi(z):return float(z[0]) if fixed else float(np.trapezoid(ww*z,tt))
  gpairs=[]
  for i,(first,second,cc) in enumerate(pairdefs):
   c=np.array(cc,float);cm=np.einsum('ni,i->n',mm,c);cv=np.einsum('i,nij,j->n',c,SS,c)
   assert np.all(np.isfinite(cm)) and np.all(np.isfinite(cv)) and np.all(cv>0)
   gmean=gi(cm);gprob=gi(ndtr(-cm/np.sqrt(cv)))
   gqs=[float(brentq(lambda z:gi(ndtr((z-cm)/np.sqrt(cv)))-p,-100,100,xtol=1e-9)) for p in [.025,.5,.975]]
   test('NMApairgridmeanSD'+str(sd)+str(i)+str(ngrid),gmean,pairs[i]['posterior_mean']);test('NMApairgridCrISD'+str(sd)+str(i)+str(ngrid),gqs,pairs[i]['CrI025_50_975']);test('NMApairgridPrSD'+str(sd)+str(i)+str(ngrid),gprob,pairs[i]['Pr_first_has_lower_mean_pain'])
   gpairs.append({'first':first,'second':second,'mean':gmean,'CrI025_50_975':gqs,'Pr_lower':gprob})
  gg.append({'points':ngrid,'tau_upper':0 if fixed else U,'pairs':gpairs})
 if fixed:
  # GLS/conjugate Gaussian sanity checkandpair covariance identity.
  fm,fc,_,_=cond(0)
  for i,(_,_,cc) in enumerate(pairdefs):
   c=np.array(cc,float);qnormal=float(c @ fm)+norm.ppf([.025,.5,.975])*math.sqrt(float(c @ fc @ c));test('tau0normalpairCrI'+str(i),pairs[i]['CrI025_50_975'],qnormal,1e-9,1e-9)
 rr={'tau_prior_half_normal_SD':None if fixed else sd,'fixed_tau':0 if fixed else None,'primary_tau_prior':sd==1,'method':'Analyticmultivariatenormald|tau plus1Dadaptivequadrature;independentMVNmarginal-gridcheck','basic_effect_order':['PT','CBCT','ICBT'],'posterior_basic_means':means.tolist(),'posterior_basic_covariance':marginalcov.tolist(),'posterior_tau_mean':tau_mean,'posterior_tau_025_50_975':tqs,'pairs':pairs,'grid_checks':gg,'quad_normalisation':Z,'quad_normalisation_absolute_error':err,'Rhat':None,'MCMC_ESS':None,'no_MCMC_or_convergence_claim':True,'clinical_status':'Conditionalstressdemonstration;notprimaryNMA;notGRADEassessed;nosuitablerankingrecommendation'}
 result.append(rr);print('NMA','fixedtau0' if fixed else 'tauSD'+str(sd),[(p['first']+'-'+p['second'],round(p['posterior_mean'],4),[round(p['CrI025_50_975'][j],4) for j in [0,2]]) for p in pairs],flush=True)

for r,e in zip(result,expected):
 assert r['tau_prior_half_normal_SD']==e['tau_prior_half_normal_SD'] and r['fixed_tau']==e['fixed_tau']
 for p,q in zip(r['pairs'],e['pairs']):
  assert (p['first'],p['second'])==(q['first'],q['second'])
  for key in ['posterior_mean','CrI025_50_975','Pr_first_has_lower_mean_pain','posterior_variance_using_full_basic_effect_covariance']:
   test('published_replay_'+str(r['tau_prior_half_normal_SD'])+'_'+p['first']+'_'+p['second']+'_'+key,p[key],q[key],1e-7,1e-7)
assert len(result)==4 and not issues,issues
(OUT/'conditional_pain_network_replayed.json').write_text(json.dumps({'status':'PASS','rows':result,'issues':issues,'four_tau_views':4,'pairs_per_view':6,'conditions':L['assumptions_not_empirical_certifications'],'clinical_status':'CONDITIONAL_STRESS_TEST_ONLY_NOT_PRIMARY_CLINICAL_NMA_NO_RANKING_NO_GRADE'},ensure_ascii=False,indent=2)+'\n')
print('PASS: four conditional tau views, six covariance-aware pairs each; no clinical ranking.')
