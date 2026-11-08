"""Recompute one trial's seven early complete-case contrasts; no pooled model.
Requires Python3 and scipy. Run --input with the derived JSON from supplementS8.
All rows use seven observed women per arm; allocated12/14 is not variance N.
"""
from pathlib import Path
import argparse,json,math,sys
import scipy
from scipy.stats import t
p=argparse.ArgumentParser();p.add_argument('--input',type=Path,default=Path(__file__).with_name('S8_SOURCE039_DERIVED_COMPLETECASE_EFFECTS7.json'));args=p.parse_args();data=json.loads(args.input.read_text());rows=data['rows'];assert len(rows)==7;checked=[]
for r in rows:
 mi,mc=r['source_arm_change_means'];si,sc=r['source_arm_change_SDs'];ni,nc=r['observed_complete_case_arm_N'];assert(ni,nc)==(7,7)
 vi,vc=si*si/ni,sc*sc/nc;v=vi+vc;se=math.sqrt(v);df=v*v/(vi*vi/(ni-1)+vc*vc/(nc-1));md=mi-mc;lo,hi=md-t.ppf(.975,df)*se,md+t.ppf(.975,df)*se
 differences=[abs(md-r['estimate']),abs(v-r['sampling_variance']),abs(se-r['standard_error']),abs(df-r['Welch_df']),abs(lo-r['CI95_Welch'][0]),abs(hi-r['CI95_Welch'][1])];assert max(differences)<1e-10
 checked.append({'endpoint_id':r['endpoint_id'],'construct':r['construct'],'estimate':md,'variance':v,'CI95_Welch':[lo,hi],'max_absolute_difference':max(differences)})
print(json.dumps({'status':'PASS_SEVEN_OBSERVED_COMPLETECASE_CONTRASTS','Python':sys.version.split()[0],'scipy':scipy.__version__,'K':1,'observed_N_per_endpoint':14,'new_pooled_fits':0,'six_week_outside_primary_window':True,'results':checked},ensure_ascii=False,indent=2))
