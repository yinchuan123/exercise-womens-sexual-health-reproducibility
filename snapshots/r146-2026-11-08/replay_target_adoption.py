"""Replay target-specific application of recorded author positions.

This applies saved decisions; it does not perform GRADE, verify source facts,
recover private signatures, or identify a causal effect from selected outcomes.
"""
from pathlib import Path
import json

def replay(row):
    p=row['recorded_author_positions']
    q,w,y=(p[n]for n in ['Linwen Qiu','Kaiting Wen','Chuan Yin'])
    grade=lambda x:x['normalized_certainty']
    domains=lambda x:x['normalized_domain_deductions']
    code=row['case_id'].split('-')[2]
    if code=='030':
        assert grade(q)==grade(y)=='Moderate'and grade(w)=='NOT_RATEABLE'
        return {'source_parameter_certainty':grade(y),'domain_deductions_for_applied_target':domains(y),'complete_randomized_strategy_causal_grade':'NOT_EXTRAPOLATED_BEYOND_THE_REPORTED_NARROW_PARAMETER'}
    if code=='039':
        assert grade(q)==grade(w)=='Very low'and domains(q)==domains(w)
        assert grade(y)=='NOT_RATEABLE'
        # Q/W concern the restricted completer parameter; Y concerns assignment
        # in all randomized women. These are distinct target views, not votes
        # on an identical estimand and not extra independent trials.
        return {'source_parameter_certainty':'Very low','domain_deductions_for_applied_target':domains(q),'complete_randomized_strategy_causal_grade':'NOT_RATEABLE'}
    if code=='069':
        assert grade(q)==grade(w)==grade(y)=='Low'
        assert domains(q)==domains(w)==domains(y)
        return {'source_parameter_certainty':'Low','domain_deductions_for_applied_target':domains(q),'complete_randomized_strategy_causal_grade':'LIMITED_LOW_CERTAINTY_INTERPRETATION_NOT_RECOVERED_FULL_ITT_ESTIMATE'}
    assert code=='107'and grade(q)==grade(w)==grade(y)=='NOT_RATEABLE'
    # Wen's provisional annotations remain in the input and are not added to
    # an unidentified whole-strategy causal grade.
    return {'source_parameter_certainty':'NOT_RATEABLE','domain_deductions_for_applied_target':{k:None for k in domains(y)},'complete_randomized_strategy_causal_grade':'NOT_RATEABLE'}

if __name__=='__main__':
    h=Path(__file__).resolve().parent
    rows=json.loads((h/'actual_S29_target_assessments4.json').read_text())['rows']
    out=[]
    for r in rows:
        applied=replay(r)
        for k,v in applied.items():assert r[k]==v,(r['case_id'],k)
        out.append({'case_id':r['case_id'],**applied})
    assert len(out)==4
    print(json.dumps({'status':'PASS_SAVED_TARGET_SPECIFIC_ADOPTION_REPLAY_NOT_INDEPENDENT_CLINICAL_GRADING','rows':out},indent=2))
