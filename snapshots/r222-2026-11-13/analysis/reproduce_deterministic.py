import json,math,argparse
from pathlib import Path
import numpy as np
from scipy.integrate import quad,cumulative_trapezoid
from scipy.optimize import minimize_scalar,brentq
from scipy.special import ndtr
from scipy.stats import norm

# Portable parameterized derivation of actual independent R221 integration.
class Mixture:
 def __init__(self,y,v,sd,mu_sd=10):
  self.mu_sd=float(mu_sd);self.prec0=1/self.mu_sd**2;self.y=np.array(y,dtype=float);self.v=np.array(v,dtype=float);self.sd=float(sd);self.upper=max(40.,12*self.sd)
  tt=np.linspace(0,self.upper,1001);i=int(np.argmax(self.logtau(tt)));lo=tt[max(0,i-1)];hi=tt[min(1000,i+1)];opt=minimize_scalar(lambda z:-float(self.logtau(z)),bounds=(lo,hi),method='bounded',options={'xatol':1e-12});self.shift=max(float(self.logtau(0)),float(self.logtau(opt.x)))
  self.Z,self.Zerr=quad(self.density,0,np.inf,epsabs=2e-11,epsrel=2e-11,limit=300)
  self.mean=self.integrate(lambda x:self.cm(x)[0]);self.tau_mean=self.integrate(lambda x:x)
  self.sd_mu=math.sqrt(max(0,self.integrate(lambda x:self.cm(x)[1]+self.cm(x)[0]**2)-self.mean**2))
  self.sd_theta=math.sqrt(max(0,self.integrate(lambda x:self.cm(x)[1]+x*x+self.cm(x)[0]**2)-self.mean**2))
 def cm(self,x):
  z=np.asarray(x);w=1/(self.v+z[...,None]**2);A=self.prec0+np.sum(w,axis=-1);V=1/A;m=V*np.sum(w*self.y,axis=-1);return m,V
 def logtau(self,x):
  z=np.asarray(x);s=self.v+z[...,None]**2;w=1/s;A=self.prec0+np.sum(w,axis=-1);B=np.sum(w*self.y,axis=-1);C=np.sum(w*self.y**2,axis=-1)
  return -.5*(np.sum(np.log(s),axis=-1)+C-B*B/A+np.log(self.mu_sd**2*A))-.5*(z/self.sd)**2
 def density(self,x):return np.exp(self.logtau(x)-self.shift)
 def integrate(self,f):return quad(lambda x:float(self.density(x)*f(x)),0,np.inf,epsabs=2e-10,epsrel=2e-10,limit=300)[0]/self.Z
 def cdf(self,x,kind):
  if kind=='tau':return 0. if x<=0 else quad(self.density,0,x,epsabs=2e-10,epsrel=2e-10,limit=200)[0]/self.Z
  return self.integrate(lambda z:ndtr((x-self.cm(z)[0])/np.sqrt(self.cm(z)[1]+(z*z if kind=='theta_new' else 0))))
 def pdf(self,x,kind):
  if kind=='tau':return float(self.density(x)/self.Z) if x>=0 else 0.
  return self.integrate(lambda z:norm.pdf(x,loc=self.cm(z)[0],scale=np.sqrt(self.cm(z)[1]+(z*z if kind=='theta_new' else 0))))
 def quantiles(self,kind):
  low,high=(0.,self.upper) if kind=='tau' else (-200.,200.)
  return [float(brentq(lambda x:self.cdf(x,kind)-p,low,high,xtol=2e-9,rtol=1e-12)) for p in [.025,.5,.975]]
 def grid(self,n):
  x=np.linspace(0,self.upper,n);f=self.density(x);Z=np.trapezoid(f,x);w=f/Z;m,V=self.cm(x)
  def integ(z):return float(np.trapezoid(w*z,x))
  tauCDF=cumulative_trapezoid(w,x,initial=0)
  def cdf(z,kind):return float(np.interp(z,x,tauCDF)) if kind=='tau' else integ(ndtr((z-m)/np.sqrt(V+(x*x if kind=='theta_new' else 0))))
  def qs(kind):return [float(brentq(lambda z:cdf(z,kind)-p,0 if kind=='tau' else -200,self.upper if kind=='tau' else 200,xtol=1e-9)) for p in [.025,.5,.975]]
  return {'points':n,'upper_tau':self.upper,'normalising_integral':float(Z),'mu_mean':integ(m),'mu_025_50_975':qs('mu'),'tau_mean':integ(x),'tau_025_50_975':qs('tau'),'theta_new_025_50_975':qs('theta_new'),'Pr_mu_gt0':integ(ndtr(m/np.sqrt(V))),'Pr_theta_new_gt0':integ(ndtr(m/np.sqrt(V+x*x)))}

if __name__=='__main__':
 ap=argparse.ArgumentParser();ap.add_argument('--output',default='out-r222');ap.add_argument('--only-pool');args=ap.parse_args();HERE=Path(__file__).resolve().parents[1];OUT=Path(args.output);OUT.mkdir(parents=True,exist_ok=True)
 pools=json.loads((HERE/'inputs/pool_sets39.json').read_text())['pools'];expected=json.loads((HERE/'data/bayesian_results54.json').read_text())['rows'];diags=json.loads((HERE/'qa/mcmc_diagnostics51.json').read_text())['rows'];dm={(d['pool_id'],d['tau_prior_SD']):d for d in diags};results=[];checks=[]
 for p in pools:
  if args.only_pool and p['pool_id']!=args.only_pool:continue
  y=[r['yi'] for r in p['rows']];v=[r['vi'] for r in p['rows']]
  for plan in p['bayesian_replay_plan']:
   sd=plan['tau_half_normal_SD'];m=Mixture(y,v,sd,plan['mu_normal_SD']);r={'pool_id':p['pool_id'],'K':p['K'],'tau_prior_half_normal_SD':sd,'mu_prior_normal_SD':plan['mu_normal_SD'],'posterior_mean':m.mean,'posterior_mu_025_50_975':m.quantiles('mu'),'posterior_tau_mean':m.tau_mean,'posterior_tau_025_50_975':m.quantiles('tau'),'new_setting_true_effect_025_50_975':m.quantiles('theta_new'),'Pr_mean_MD_gt0':1-m.cdf(0,'mu'),'Pr_new_setting_true_MD_gt0':1-m.cdf(0,'theta_new'),'method':'DETERMINISTIC_REPLAY_SAME_DECLARED_MODEL_NOT_MCMC','Rhat':None,'ESS':None};results.append(r)
   e=next(e for e in expected if e['pool_id']==p['pool_id'] and e['tau_prior_half_normal_SD']==sd)
   if plan['computation']=='MCMC':
    d=dm[(p['pool_id'],sd)];mu=next(z for z in d['parameters'] if z['parameter']=='mu');tol=max(.01,5*mu['MCSE_mean']);ok=abs(e['posterior_mean']-r['posterior_mean'])<=tol;basis='5recordedMCMC_meanMCSE_or0.01floor;notbyteidentity'
   else:
    tol=1e-6;ok=np.allclose(e['posterior_mu_025_50_975'],r['posterior_mu_025_50_975'],atol=tol,rtol=1e-7) and abs(e['posterior_mean']-r['posterior_mean'])<tol;basis='Deterministicquadraturetolerance'
   checks.append({'pool_id':p['pool_id'],'tau_prior_SD':sd,'pass':bool(ok),'mean_absolute_difference':abs(e['posterior_mean']-r['posterior_mean']),'tolerance':tol,'basis':basis});print(p['pool_id'],sd,'PASS' if ok else 'FAIL',flush=True)
 assert all(c['pass'] for c in checks)
 if not args.only_pool:assert len(results)==54
 (OUT/'deterministic_Bayesian_replay.json').write_text(json.dumps({'rows':results,'checks':checks,'status':'PASS','quantity_note':'Probabilitiesreferaveragetreatmentdifferences,notindividualresponse;integrationhasnoRhat/ESS.'},ensure_ascii=False,indent=2)+'\n')

