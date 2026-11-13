from pathlib import Path
import json, hashlib
from pypdf import PdfReader
from PIL import Image

ROOT=Path(__file__).resolve().parents[1]
def load(p): return json.loads(p.read_text())
def normalise(s): return s.replace('\r\n','\n').replace('\r','\n').strip()
checks=[]
def check(name, passed): checks.append({'name':name,'pass':bool(passed)})
frozen=load(ROOT/'expected/PLOT_VALUE_AND_PIXEL_CHECKS.json')
for stem in ['Figure_1_PRISMA','Figure_2','Figure_3','Figure_4']:
    p=ROOT/'figures'/f'{stem}.pdf';pdf=PdfReader(p)
    check(stem+'_one_pdf_page',len(pdf.pages)==1)
    check(stem+'_exact_pdf_text',normalise(pdf.pages[0].extract_text())==normalise((ROOT/'expected'/f'{stem}_PDF_TEXT.txt').read_text()))
    image=Image.open(ROOT/'qa'/f'{stem}_PDF_RENDER.png').convert('RGB')
    old=frozen['pdf_render_pixels'][stem]
    check(stem+'_exact_rendered_pixels',list(image.size)==old['size'] and hashlib.sha256(image.tobytes()).hexdigest()==old['RGB_pixels_sha256'])
q=load(ROOT/'inputs/quantitative_targets11.json')['adopted_rows11']
qr={r['pool_id']:r for r in q}
check('eleven_exact_target_inputs',len(q)==11 and len(qr)==11)
for stem in ['Figure_3','Figure_4']:
    rows=load(ROOT/'plot_data'/f'{stem}.json')['data']
    for r in rows: check(stem+'_'+r['pool_id']+'_exact_minimal_input',r==qr[r['pool_id']])
actual=load(ROOT/'plot_data/Figure_2.json')['data']
for r,old in zip(actual,frozen['clinical_specs']):
    check(r['id']+'_fixed_clinical_spec_unchanged',{k:r[k] for k in old}==old)
check('five_selected_clinical_panels',len(actual)==5)
c=load(ROOT/'inputs/cutoff_counts.json')
check('PRISMA_report_equation',c['reports_assessed']==c['total_reports_not_included_with_source_reasons']+c['awaiting_classification_at_cutoff_reports']+c['included_reports'])
check('counts_40_499_8_2_and_no_unique_N',c['awaiting_classification_at_cutoff_reports']==40 and c['not_retrieved_fixed']==499 and c['initial_female_N_gap_groups']==8 and c['possible_dependency_pairs']==2 and c['initial_unique_female_N'] is None)
b=load(ROOT/'inputs/current_input_scope_bridge.json')['bridge']
check('S5_family_count17',len(b['S5_distinct_actual_source_families'])==17)
check('current_ID_intersections_empty_not_certified_cohort_independence',all(v==0 for k,v in b.items() if 'intersection' in k))
result={'schema':'R224_PORTABLE_READONLY_FIGURE_CHECK_V1','status':'PASS' if all(r['pass'] for r in checks) else 'FAIL','checks_passed':sum(r['pass'] for r in checks),'checks_total':len(checks),'checks':checks,'no_model_refit':True,'no_new_eligibility_or_GRADE':True,'binary_PDF_hash_identity_claimed':False}
(ROOT/'qa/PORTABLE_REBUILD_CHECK.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result))
assert result['status']=='PASS'
