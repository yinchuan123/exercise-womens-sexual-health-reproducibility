from pathlib import Path
import json, hashlib, textwrap, datetime, shutil, sys
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch
from matplotlib.ticker import ScalarFormatter
import pypdfium2 as pdfium
from pypdf import PdfReader

ROOT=Path(__file__).resolve().parents[1]
MATRIX=ROOT/'inputs'
OUT=ROOT/'figures'; OUT.mkdir(parents=True,exist_ok=True)
INPUT=ROOT/'plot_data'; INPUT.mkdir(exist_ok=True)
QA=ROOT/'qa'; QA.mkdir(exist_ok=True)

def load(p): return json.loads(p.read_text())
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
Q=load(MATRIX/'quantitative_targets11.json')
A=load(MATRIX/'clinical_targets5.json')
COUNTS=load(MATRIX/'cutoff_counts.json')
QR={r['pool_id']:r for r in Q['adopted_rows11']}
AR={r['row_id']:r for r in A['rows']}

plt.rcParams.update({'font.family':'DejaVu Sans','font.size':8.4,
 'axes.labelsize':8.3,'xtick.labelsize':7.6,'ytick.labelsize':8.1,
 'axes.spines.top':False,'axes.spines.right':False,'axes.spines.left':False,
 'axes.linewidth':0.6,'pdf.fonttype':42,'ps.fonttype':42,'svg.fonttype':'none',
 'savefig.facecolor':'white','figure.facecolor':'white'})
BLUE='#15588a'; ORANGE='#b2601e'; INK='#1b2c3c'; GREY='#687987'; LIGHT='#d4dce4'
WRITTEN=[]; AXIS_ARTISTS=[]

def save(fig,stem,number,mode,source_ids,data):
    paths=[]
    for ext in ['pdf','svg','png']:
        p=OUT/f'{stem}.{ext}'
        fig.savefig(p,dpi=300)
        paths.append({'path':str(p.relative_to(ROOT)),'sha256':sha(p),'bytes':p.stat().st_size})
    plt.close(fig)
    p=INPUT/f'{stem}.json'
    payload={'figure':number,'production_mode':mode,'source_row_ids':source_ids,
       'data':data,'no_model_refit':True,'no_new_eligibility_or_GRADE':True,
       'source_files': [{'path':'inputs/quantitative_targets11.json','sha256':sha(MATRIX/'quantitative_targets11.json')},
                        {'path':'inputs/clinical_targets5.json','sha256':sha(MATRIX/'clinical_targets5.json')} ]}
    p.write_text(json.dumps(payload,ensure_ascii=False,indent=2)+'\n')
    WRITTEN.append({'figure':number,'stem':stem,'mode':mode,'outputs':paths,'plot_data':str(p.relative_to(ROOT)),'plot_data_sha256':sha(p),
                    'new_model_fits':0,'status':'NUMERIC_CHECKED_AWAITING_FINAL_RENDER_INSPECTION'})

def fmt(v): return f'{v:.2f}'
def interval(v,ci): return f'{fmt(v)} ({fmt(ci[0])} to {fmt(ci[1])})'
def plain_ax(ax):
    ax.set_axis_off();ax.set_xlim(0,1);ax.set_ylim(0,1)

def figure1():
    c=COUNTS; r=c['record_identification']
    assert r['records_identified']==29491 and c['included_reports']==340
    assert c['reports_assessed']==c['total_reports_not_included_with_source_reasons']+c['awaiting_classification_at_cutoff_reports']+c['included_reports']
    fig=plt.figure(figsize=(175/25.4,255/25.4)); ax=fig.add_axes([0,0,1,1]);plain_ax(ax)
    boxes={}
    def box(key,x,y,w,h,lines,fs=8.0,boldfirst=True):
        rect=FancyBboxPatch((x,y),w,h,boxstyle='square,pad=0',linewidth=.7,edgecolor=GREY,facecolor='white')
        ax.add_patch(rect);boxes[key]=(x,y,w,h)
        txt=ax.text(x+.014,y+h-.014,lines,va='top',ha='left',fontsize=fs,color=INK,linespacing=1.34)
        AXIS_ARTISTS.append((fig,txt,rect,key))
    def arrow(s,t,kind='vertical'):
        x,y,w,h=boxes[s];a,b,cw,dh=boxes[t]
        if kind=='right': start=(x+w,y+h/2);end=(a,b+dh/2)
        else:start=(x+w/2,y);end=(a+cw/2,b+dh)
        ax.add_patch(FancyArrowPatch(start,end,arrowstyle='-|>',mutation_scale=8,linewidth=.7,color=GREY))
    source=(
      'Records identified (n = 29,491)\n'
      'Databases (n = 17,574)\n'
      '  PubMed / MEDLINE, 2,262\n  Embase.com bibliographic records, 6,433\n'
      '  Web of Science Core Collection, 4,420\n  Cochrane CENTRAL, 2,194\n'
      '  LILACS, 727\n  CINAHL Complete (EBSCOhost), 922\n'
      '  APA PsycInfo (EBSCOhost), 484\n  SPORTDiscus (EBSCOhost), 132\n'
      'Trial registers (n = 10,937)\n  Embase Registry, 683\n'
      '  ClinicalTrials.gov, 8,639\n  WHO ICTRP, 1,615\nOther identified sources (n = 980)')
    box('identified',.065,.704,.583,.282,source,fs=7.8)
    box('duplicates',.710,.827,.275,.085,'Duplicate representations\nremoved before screening\n(n = 7,566)',fs=7.9)
    box('screened',.065,.611,.583,.055,'Records screened (n = 21,925)',fs=8.6)
    box('record_excluded',.710,.611,.275,.055,'Records excluded\n(n = 18,827)',fs=8.1)
    box('sought',.065,.512,.583,.063,'Reports sought for retrieval (n = 3,088)\nLinked from 3,098 candidate records*',fs=8.4)
    box('not_retrieved',.710,.512,.275,.063,'Reports not retrieved\n(n = 499)',fs=8.2)
    box('assessed',.065,.414,.583,.063,'Reports assessed for eligibility\n(n = 2,589)',fs=8.6)
    reasons=('Reports not included\n(n = 2,209)\n'
      'Outside active-practice scope, 147\nNo eligible direct sexual result, 194\n'
      'Ineligible or mixed design, 81\nNot an original result report, 59\n'
      'Nonseparable population, 26\nRetracted report, 1\n'
      'Protocols and other noncontributing\nreport contexts, 1,701')
    box('report_excluded',.710,.316,.275,.161,reasons,fs=7.25)
    box('unclassified',.710,.222,.275,.065,'Reports awaiting classification\nat the evidence cutoff\n(n = 40)',fs=7.8)
    box('included',.065,.278,.583,.089,'Included reports (n = 340)\n199 principal result reports; 141 companion reports\nConservative reported-strategy groups (n = 194)',fs=8.4)
    box('quant',.065,.136,.583,.095,'Outcome-specific quantitative evidence\nS5: 39 overlapping input sets from 17 source groups\nS6: three retained restricted comparisons, K = 2 each\nCounts are specific to each synthesis, not additive.',fs=7.7)
    for s,t in [('identified','screened'),('screened','sought'),('sought','assessed'),('assessed','included'),('included','quant')]:arrow(s,t)
    for s,t in [('screened','record_excluded'),('sought','not_retrieved')]:arrow(s,t,'right')
    ax.add_patch(FancyArrowPatch((.648,.8695),(.710,.8695),arrowstyle='-|>',mutation_scale=8,linewidth=.7,color=GREY))
    ax.add_patch(FancyArrowPatch((.648,.4455),(.710,.4455),arrowstyle='-|>',mutation_scale=8,linewidth=.7,color=GREY))
    # A separate assessed-report branch; awaiting classification is not an exclusion.
    ax.plot([.681,.681],[.4455,.253],color=GREY,lw=.7)
    ax.add_patch(FancyArrowPatch((.681,.253),(.710,.253),arrowstyle='-|>',mutation_scale=8,linewidth=.7,color=GREY))
    for y0,y1,label in [(.697,.990,'Identification'),(.399,.680,'Screening and eligibility'),(.128,.379,'Included')]:
        ax.add_patch(FancyBboxPatch((.012,y0),.031,y1-y0,boxstyle='square,pad=0',facecolor='#eef3f6',edgecolor='none'))
        ax.text(.0275,(y0+y1)/2,label,rotation=90,ha='center',va='center',fontsize=8.3,color=INK)
    foot=[
      '* Record-to-report linkage: 3,098 - 1 proceedings container + 4 additional reports - 13 redundant representations = 3,088. The 13 comprise 10 alias nodes and three many-to-one merges. See S1.',
      'The 194 groups are conservative reported strategies, not a certified review-wide independent trial K. Splitting one or both suspected-dependency pairs gives 195 or 196 groups; unique female N remains unverified.',
      'Complete programmes and defined adaptive bodily-task offers are retained. No isolated exercise-component effect is identified. Adapted from PRISMA 2020.'
    ]
    y=.113
    for para in foot:
        lines=textwrap.wrap(para,width=113)
        ax.text(.065,y,'\n'.join(lines),ha='left',va='top',fontsize=6.6,color=GREY,linespacing=1.25)
        y-=len(lines)*.0113+.008
    fig.canvas.draw()
    renderer=fig.canvas.get_renderer()
    bcheck=[]
    for f,txt,rect,key in AXIS_ARTISTS:
        if f is fig:
            tb=txt.get_window_extent(renderer);bb=rect.get_window_extent(renderer)
            bcheck.append({'box':key,'text_fits':bool(tb.x0>=bb.x0 and tb.x1<=bb.x1-1 and tb.y0>=bb.y0+1 and tb.y1<=bb.y1)})
    (QA/'PRISMA_TEXT_BOXES.json').write_text(json.dumps(bcheck,indent=2))
    save(fig,'Figure_1_PRISMA',1,'Frozen count redrawing; current single consolidated report flow',[],{'counts':c,'quantitative_S5_source_groups':17,'quantitative_S5_overlapping_input_sets':39,'S6_restricted_comparisons':3,'S6_K_each':2})

def figure2():
    specs=[
     {'id':'MORIN_DIRECTION','title':'A  Intercourse pain in provoked vestibulodynia','compare':'Multimodal physiotherapy vs lidocaine; 10 weeks',
      'n':'Randomized N = 212; effective model n not reported','value':-1.8,'ci':[-2.3,-1.2],'measure':'MD','axis':'NRS 0-10 points; lower favours physiotherapy','lim':[-2.8,.1],'ticks':[-2.5,-2,-1.5,-1,-.5,0],'grade':'Moderate (direction)'},
     {'id':'MORIN_PGIC','title':'B  Clearly improved pain in the same Morin trial','compare':'Pain-focused patient global impression; 10 weeks',
      'n':'Observed N = 201; 78/99 vs 40/102 much / very much improved','value':2.01,'ci':[1.55,2.61],'measure':'RR','axis':'Risk ratio (log scale); higher favours physiotherapy','lim':[.9,3.0],'ticks':[1,1.5,2,3],'grade':'Moderate (direction)','log':True},
     {'id':'MYLOVIA_PRIMARY_FUNCTION','title':'C  Sexual function with the complete mylovia programme','compare':'Complete digital programme vs usual treatment plus information; 3 months',
      'n':'Randomized N = 252; observed / effective model n not verified','value':3.7,'ci':[1.7,5.6],'measure':'MD','axis':'FSFI points; higher favours the complete programme','lim':[-.2,6.2],'ticks':[0,1,2,3,4,5,6],'grade':'Moderate (mean direction)'},
     {'id':'ESENSE_DESIRE_R1','title':'D  Desire and arousal with the complete eSense mindfulness package','compare':'First-stage mindfulness package vs initial waiting condition',
      'n':'Selected-arm allocation N = 86; same initial trial family N = 129','value':7.334,'ci':[2.893,11.775],'measure':'Coefficient','axis':'SIDI-F points; higher favours the complete programme','lim':[-.4,12.5],'ticks':[0,3,6,9,12],'grade':'Moderate (exact target)'},
     {'id':'ESENSE_DISTRESS_R1','title':'E  Sexual distress in the same eSense comparison','compare':'First-stage mindfulness package vs initial waiting condition',
      'n':'Same selected-arm allocation N = 86; effective model n not reported','value':-8.903,'ci':[-13.147,-4.658],'measure':'Coefficient','axis':'FSDS-R points; lower favours the complete programme','lim':[-14.3,.5],'ticks':[-14,-12,-10,-8,-6,-4,-2,0],'grade':'Moderate (exact target)'}
    ]
    for s in specs:
        r=AR[s['id']]
        assert r['adoptedGRADEexactscope']['display_zh']=='中等'
        s['source_matrix_row']=r
    fig=plt.figure(figsize=(175/25.4,235/25.4))
    fig.text(.045,.984,'Selected outcome-specific estimates within the full clinical synthesis',ha='left',va='top',fontsize=8.5,fontweight='bold',color=INK)
    fig.text(.045,.959,'Different native scales and populations; no overall pooled effect or ranking',ha='left',va='top',fontsize=7.8,color=GREY)
    top=.913; step=.165
    for i,s in enumerate(specs):
        y=top-i*step
        fig.text(.045,y,s['title'],fontsize=8.5,fontweight='bold',ha='left',va='top',color=INK)
        fig.text(.045,y-.025,s['compare'],fontsize=7.45,ha='left',va='top',color=INK)
        fig.text(.045,y-.044,s['n'],fontsize=7.2,ha='left',va='top',color=GREY)
        ax=fig.add_axes([.075,y-.109,.555,.036])
        ax.set_xlim(*s['lim']);ax.set_ylim(-.5,.5);ax.set_yticks([])
        ax.spines['bottom'].set_color(GREY)
        if s.get('log'):
            ax.set_xscale('log');ax.xaxis.set_major_formatter(ScalarFormatter());ax.minorticks_off()
        ax.set_xticks(s['ticks']);ax.set_xticklabels([str(x).replace('.0','') for x in s['ticks']])
        ax.tick_params(axis='x',length=2,pad=1)
        ax.axvline(1 if s.get('log') else 0,color=GREY,linestyle='--',linewidth=.65)
        ax.errorbar(s['value'],0,xerr=[[s['value']-s['ci'][0]],[s['ci'][1]-s['value']]],fmt='s',color=BLUE,ecolor=BLUE,capsize=2.7,markersize=4.8,lw=1.25)
        ax.set_xlabel(s['axis'],fontsize=7.1,labelpad=2)
        fig.text(.665,y-.074,f"{s['measure']} {interval(s['value'],s['ci'])}",ha='left',va='center',fontsize=7.6,color=INK)
        fig.text(.665,y-.095,'GRADE: '+s['grade'],ha='left',va='center',fontsize=7.25,color=INK)
        if i<4:fig.add_artist(Line2D([.045,.97],[y-.143,y-.143],transform=fig.transFigure,color=LIGHT,lw=.5))
    footer=('Intervals are 95% CIs. B retains the frozen observed-case RR; C preserves the published bootstrap multiple-imputation interval. '
      'A/B and D/E share trial families; K = 1 for each source, not five independent trials. '
      'A has Low certainty for a mean advantage of at least the 1.5-point design anchor. '
      'eSense treatment completion and waiting use different source clocks. '
      'The full synthesis also retains active-comparator, null, uncertain and ungraded evidence (Table 3).')
    fig.text(.045,.069,'\n'.join(textwrap.wrap(footer,113)),fontsize=6.9,ha='left',va='top',color=GREY,linespacing=1.3)
    save(fig,'Figure_2',2,'Redrawing of already-adopted published and frozen aggregate effects; selected displays', [s['id'] for s in specs],specs)

def paired_summary(ids,labels,stem,number,domain=False):
    rows=[QR[x] for x in ids]
    height=175 if domain else 175
    fig=plt.figure(figsize=(175/25.4,height/25.4))
    ytop=len(rows)-1
    # Fixed columns retain a full, unclipped interval axis and native text columns.
    labelax=fig.add_axes([.02,.245,.34,.625]);plain_ax(labelax)
    ax=fig.add_axes([.36,.245,.31,.625]);ax.set_ylim(-.65,len(rows)-.35)
    valax=fig.add_axes([.69,.245,.245,.625]);plain_ax(valax)
    gax=fig.add_axes([.94,.245,.058,.625]);plain_ax(gax)
    for a in [labelax,valax,gax]: a.set_ylim(-.65,len(rows)-.35)
    ax.set_yticks([])
    ax.spines['bottom'].set_color(GREY);ax.axvline(0,color=GREY,lw=.65,ls='--')
    ax.set_xlim((-.9,1.6) if domain else (-.3,8.9))
    ax.set_xticks([-.5,0,.5,1,1.5] if domain else [0,2,4,6,8])
    ax.set_xlabel('Mean difference in FSFI domain points' if domain else 'Mean difference in FSFI total points',fontsize=7.7,labelpad=7)
    for i,(r,label) in enumerate(zip(rows,labels)):
        y=ytop-i
        labelax.text(0,y+.19,label,ha='left',va='center',fontsize=8.0,fontweight='bold',color=INK,linespacing=1.2)
        cov=r['n_source_coverage']
        # Display labels consume the already-saved coverage, not an imputed denominator.
        total=r['K']; ns=r['n_source_sum']; have=next((int(v) for k,v in cov.items() if 'with' in k.lower() and 'N' in k),None) if isinstance(cov,dict) else None
        # A separate saved string carries exact source coverage in Chinese; the English display count is explicit below.
        coverage={'MENOPAUSE_RAW_ENDPOINT4':'4/4','MENOPAUSE_ALL6_WITH_WALD_EQUIV':'5/6','BROAD_RAW_ENDPOINT10_PRINTED_OUTCOME_N':'10/10','BROAD_ENDPOINT11_ADD_BASGOL':'11/11','BROAD_INCLUSIVE14_ORDINARY_CI_WITH_BASGOL':'12/14'}
        cv='3/3' if domain else coverage[r['pool_id']]
        labelax.text(0,y-.15,f'K = {total}; source n = {ns} ({cv} sources)',ha='left',va='center',fontsize=7.1,color=GREY)
        for dy,mean,ci,marker,col in [(+.11,r['MD'],r['CI95'],'s',BLUE),(-.11,r['Bayesian_primary_mean'],r['Bayesian_primary_95CrI'],'o',ORANGE)]:
            assert ci[0]<=mean<=ci[1]
            ax.errorbar(mean,y+dy,xerr=[[mean-ci[0]],[ci[1]-mean]],fmt=marker,color=col,ecolor=col,markersize=3.8,lw=1.1,capsize=2.1)
            valax.text(0,y+dy,interval(mean,ci),fontsize=7.25,color=col,va='center',ha='left')
        grade='Very\nlow' if r['GRADE']=='Very low' else r['GRADE']
        gax.text(0,y,grade,ha='left',va='center',fontsize=7.1,color=INK,linespacing=1.15)
    fig.text(.02,.93,'Exploratory domain syntheses in the same three families' if domain else 'Exploratory total-score syntheses in five overlapping sets',fontsize=9,fontweight='bold',ha='left',va='top',color=INK)
    fig.text(.69,.895,'MD (95% CI or CrI)',fontsize=7.4,ha='left',color=INK)
    fig.text(.94,.895,'GRADE',fontsize=7.0,ha='left',color=INK)
    legend=[Line2D([0],[0],marker='s',color=BLUE,lw=1.1,markersize=4,label='REML modified HK: 95% CI'),Line2D([0],[0],marker='o',color=ORANGE,lw=1.1,markersize=4,label='Bayesian primary prior: 95% CrI')]
    fig.legend(handles=legend,loc='lower left',bbox_to_anchor=(.02,.115),frameon=False,ncol=2,fontsize=7.1,handlelength=1.5,columnspacing=1.0)
    footer=('All six domains reuse Franco, Khosravi and Elgayar; K and source n are not added across rows. '
        'Higher scores indicate fewer problems, including the pain domain. The wider-prior arousal CrI is -0.16 to 1.37. '
        'No between-domain interaction was tested; domain means are not recovery probabilities.' if domain else
        'Post hoc, overlapping sets. Source n sums printed denominators with coverage; it is not unique review-wide N or a certified effective model n. '
        'Six- and 14-family expansions include source-CI-equivalent precision. All source restrictions, priors and prediction intervals are retained in S5.')
    fig.text(.02,.108,'\n'.join(textwrap.wrap(footer,119)),fontsize=6.7,color=GREY,ha='left',va='top',linespacing=1.3)
    save(fig,stem,number,'Redrawing of frozen mKH and primary-prior Bayesian estimates; no refit',ids,rows)

def captions():
    caps={
     'Figure 1 Study selection':
       'One consolidated PRISMA 2020 flow distinguishes records, distinct reports and conservative reported-strategy groups at the fixed evidence cutoff. The 3,088 distinct reports comprise 499 not retrieved and 2,589 assessed; assessed reports comprise 2,209 not included with reasons, 40 awaiting classification and 340 included reports (199 principal result and 141 companion reports). The 194 conservative strategy groups are not a certified review-wide independent trial K; splitting one or both suspected-dependency pairs gives 195 or 196 groups. The source-to-report reconciliation and individual source reasons are in S1. The S5 input-set count and S6 retained restricted comparisons are distinct, overlapping analysis layers, not additive independent trials. No participant total is inferred by summing source denominators.',
     'Figure 2 Selected source-specific clinical outcomes in native measures':
       'Selected outcome-specific estimates are displayed within the full clinical synthesis, not as an exhaustive set of primary eligible outcomes or a new pooled treatment comparison. Panels retain distinct populations, complete programmes, native outcome units and source assessment clocks. A and B are correlated outcomes from one vestibulodynia trial: the NRS difference concerns average intercourse pain, while the project’s frozen observed-case patient-global-improvement RR uses 78/99 versus 40/102 respondents. Moderate certainty applies to favourable direction; the separate claim of a mean pain advantage of at least the 1.5-point trial-design anchor has Low certainty. Panel C retains the published bootstrap multiple-imputation interval. D and E share the initial eSense trial family and the same first-stage 43/43 selected-arm allocation; the initial three-arm family has 129 participants, and treatment completion is not a common randomization-relative assessment clock. Each displayed source has K=1; the five panels do not add five independent trials or unique patient counts. Exact adopted certainty scopes are retained, not transferred to recovery or isolated exercise. Active-comparator, null, uncertain and ungraded clinical evidence remains in Table 3 and S3; these selected panels do not establish programme superiority across populations.',
     'Figure 3 Exploratory FSFI total-score syntheses':
       'Five post hoc overlapping sets are displayed: the four-family menopause raw-endpoint set, its six-family expansion, the broad 10-family raw-endpoint set without Basgol, the inclusive 11-family raw-endpoint set with Basgol, and the inclusive 14-family precision expansion. Squares show REML mean differences with modified Hartung-Knapp 95% confidence intervals; circles show Bayesian means with 95% credible intervals under the primary priors. Source n sums printed denominators with explicit source coverage; it is not unique review-wide N or a certified effective model denominator. Six- and 14-family expansions include labelled source-CI-equivalent precision. The 11- and 14-family scopes have Very low certainty; the other three displayed total-score targets have Low certainty. Grades apply to the exact adopted target, not to an important individual response or recovery. All 39 input sets, without-Basgol sensitivity views, priors and prediction intervals are retained in S5.',
     'Figure 4 Exploratory FSFI domains in the same three source families':
       'All six core domains reuse Franco, Khosravi and Elgayar; source K=3 and source n=225 are repeated, not added across outcomes. Squares show REML modified Hartung-Knapp confidence intervals and circles show primary-prior Bayesian credible intervals. Higher scores indicate fewer problems, including in the FSFI pain domain. Mean-score intervals are not individual response or recovery probabilities. Desire has Very low certainty and the other five exact domain targets have Low certainty. Under the wider domain heterogeneity prior, the arousal 95% credible interval was -0.16 to 1.37. No between-domain interaction was tested. Separately labelled Qigong and linearly weighted TLM extensions in S5 do not add families to the core estimates.'}
    (ROOT/'FIGURE_CAPTIONS_EN.json').write_text(json.dumps(caps,ensure_ascii=False,indent=2)+'\n')
    (ROOT/'FIGURE_CAPTIONS_EN.md').write_text('\n\n'.join(k+'\n\n'+v for k,v in caps.items())+'\n')
    return caps

if __name__=='__main__':
    figure1();figure2()
    paired_summary(['MENOPAUSE_RAW_ENDPOINT4','MENOPAUSE_ALL6_WITH_WALD_EQUIV','BROAD_RAW_ENDPOINT10_PRINTED_OUTCOME_N','BROAD_ENDPOINT11_ADD_BASGOL','BROAD_INCLUSIVE14_ORDINARY_CI_WITH_BASGOL'],
       ['Menopause: raw endpoints','Menopause: expanded','Broad: raw endpoints\nwithout Basgol','Broad: inclusive endpoints\nwith Basgol','Broad: inclusive expansion\nwith Basgol'],'Figure_3',3)
    paired_summary(['DOMAIN_'+d+'_CORE3' for d in ['Desire','Arousal','Lubrication','Orgasm','Satisfaction','Pain']],
       ['Desire','Arousal','Lubrication','Orgasm','Satisfaction','Pain domain'],'Figure_4',4,True)
    captions()
    # Independent actual-PDF renders are the basis of visual inspection.
    for f in WRITTEN:
        p=OUT/(f['stem']+'.pdf');doc=pdfium.PdfDocument(p)
        assert len(doc)==1
        image=doc[0].render(scale=2).to_pil();image.save(QA/(f['stem']+'_PDF_RENDER.png'))
        extracted=PdfReader(p).pages[0].extract_text()
        (QA/(f['stem']+'_PDF_TEXT.txt')).write_text(extracted)
        f['pdf_pages']=1;f['pdf_contains_native_text']=bool(extracted.strip())
        resources=PdfReader(p).pages[0].get('/Resources').get_object()
        f['pdf_image_xobjects']=len([k for k,v in resources.get('/XObject',{}).get_object().items() if v.get_object().get('/Subtype')=='/Image']) if resources.get('/XObject') else 0
        f['render_preview']=str((QA/(f['stem']+'_PDF_RENDER.png')).relative_to(ROOT))
    manifest={'schema':'BMJ_R224_FIGURES_FROZEN_DATA_REDRAW_V1','created_UTC':datetime.datetime.now(datetime.timezone.utc).isoformat(),
        'figures':WRITTEN,'no_model_refit_or_GRADE_change':True,'original_signed_files_modified':False,
        'dependency_resolution':'requirements.txt; no project-private runtime required',
        'python_runtime':Path(sys.executable).name,'versions':{'matplotlib':matplotlib.__version__},
        'render_inspection':'PENDING','readable_font_default_points':8.4,'vector_width_mm':175}
    (ROOT/'FIGURE_MANIFEST_QA.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps({'figures':len(WRITTEN),'main_output':str(OUT),'manifest':str(ROOT/'FIGURE_MANIFEST_QA.json')},ensure_ascii=False))
