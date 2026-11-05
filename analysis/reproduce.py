"""Verify the shared evidence projection and rerun the six frozen fits."""
from argparse import ArgumentParser
from collections import Counter
from csv import DictReader
from hashlib import sha256
from pathlib import Path
import json
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]

def read_json(relative):
    return json.loads((ROOT / relative).read_text(encoding='utf-8'))

def rows(relative, delimiter=','):
    with (ROOT / relative).open(encoding='utf-8-sig', newline='') as f:
        return list(DictReader(f, delimiter=delimiter))

def tally(items, key):
    return Counter(item[key] for item in items)

def verify_manifest():
    manifest = ROOT / 'MANIFEST.sha256'
    checked = 0
    for line in manifest.read_text().splitlines():
        digest, relative = line.split('  ', 1)
        location = ROOT / relative
        if not location.resolve().is_relative_to(ROOT) or location.is_symlink():
            raise ValueError(f'Unexpected manifest path {relative}')
        if sha256(location.read_bytes()).hexdigest() != digest:
            raise ValueError(f'Checksum mismatch for {relative}')
        checked += 1
    return checked

def verify_data():
    selection = read_json('data/selection_accounting.json')
    record = selection['record_accounting']
    report = selection['report_catalogue']
    request = selection['bounded_request_evidence']
    held = selection['retained_awaiting_report_evidence']
    summary = selection['bounded_synthesis_counts']
    historical = selection['historical_event_subflow']
    unknowns = selection['whole_review_cells']

    streams = record['source_members_by_stream']
    assert sum(streams.values()) == record['focused_native_export_members']
    focused = record['focused_native_export_members'] - record['focused_duplicate_representations']
    assert focused == record['canonical_focused_record_groups']
    archive = (record['archive_representations']
               - record['archive_within_archive_duplicate_representations']
               - record['archive_focused_overlap'])
    assert archive == record['net_additional_archival_record_groups']
    assert focused + archive == record['canonical_total_record_groups'] == 21866
    assert sum(record['source_group_routes'].values()) == focused + archive
    focused_routes = record['source_group_routes_by_origin']['focused']
    archive_routes = record['source_group_routes_by_origin']['prior_archive_only']
    assert sum(focused_routes.values()) == focused
    assert sum(archive_routes.values()) == archive
    assert Counter(focused_routes) + Counter(archive_routes) == Counter(record['source_group_routes'])

    catalogue = rows('data/report_catalogue.csv')
    by_category = {row['category']: row['reports'] for row in report['by_category']}
    assert len(catalogue) == report['reports'] == 392
    assert len({row['report_id'] for row in catalogue}) == len(catalogue)
    assert tally(catalogue, 'catalogue_category') == by_category
    assert sum(row['linked_to_current_record_group'] == 'True' for row in catalogue) == report['reports_with_exact_current_record_anchor']
    assert all(not row['whole_review_eligibility'] for row in catalogue)
    assert sum(report['exact_edge_record_routes'].values()) == report['carrier_to_report_edges']
    assert request['with_exact_current_anchor'] + request['with_positive_complete_own_body_evidence'] - request['with_both_exact_anchor_and_complete_body_evidence'] + request['with_neither_confirmed_anchor_nor_positive_complete_body'] == request['unique_catalogue_ids']
    assert request['unique_catalogue_ids'] + request['catalogue_ids_outside_request_archive'] == report['reports']
    assert historical['complete_body_at_event'] + historical['not_retrieved_at_event'] == historical['documented_request_targets']
    assert sum(held['complete_own_body_evidence_tiers'].values()) == held['reports'] == by_category['AWAITING_CLASSIFICATION'] == 114
    unresolved = rows('data/whole_review_flow_unknowns.tsv', '\t')
    assert len(unresolved) == len(unknowns) == 8
    assert {row['cell'] for row in unresolved} == set(unknowns)
    assert all(not row['value'] and unknowns[row['cell']]['value'] is None for row in unresolved)
    assert selection['final_PRISMA'] is False
    diagram = read_json('figures/PRISMA_2020_FIGURE1_DATA.json')
    chart = diagram['counts']
    assert diagram['unresolved_whole_review_fields'] == unknowns
    assert chart['focused_export_members'] == record['focused_native_export_members']
    assert chart['focused_duplicates'] == record['focused_duplicate_representations']
    assert chart['focused_unique'] == focused and chart['archive_net'] == archive
    assert chart['screening_frame'] == focused + archive
    assert chart['awaiting_catalogue_reports'] == held['reports']
    route_keys = {
        'excluded': 'RECORD_SCREEN_EXCLUDED',
        'author_retained': 'RETAIN_OR_LINK_AUTHOR_ADOPTED',
        'technical_retained': 'RETAIN_OR_LINK_TECHNICAL_EXISTING_POLICY',
        'hold': 'FORMAL_HOLD',
    }
    assert all(chart['record_routes'][figure_key] == record['source_group_routes'][archive_key]
               for figure_key, archive_key in route_keys.items())

    families = rows('data/bounded_families.csv')
    ids = {row['bounded_family_id'] for row in families}
    principal = {row['report_id'] for row in catalogue if row['catalogue_category'] == 'QUALIFIED_PRINCIPAL_SOURCE'}
    family_reports = [report_id for row in families for report_id in row['principal_report_ids'].split('|')]
    assert len(ids) == len(families) == summary['source_supported_families'] == 84
    assert len(principal) == chart['principal_reports'] == summary['principal_report_carriers'] == 85
    assert chart['study_families'] == len(families)
    assert len(family_reports) == len(principal) and set(family_reports) == principal
    assert all(not row['whole_review_independent_participant_N'] for row in families)

    result_path = ROOT / 'data/source_result_ledger.jsonl'
    result = [json.loads(line) for line in result_path.read_text(encoding='utf-8').splitlines()]
    certainty = read_json('data/certainty_and_models.json')
    scope = certainty['bounded_set']
    assert len({row['result_id'] for row in result}) == len(result) == summary['typed_numerical_or_descriptive_records'] == 152
    assert chart['result_records'] == len(result)
    assert {row['family_id'] for row in result} <= ids
    assert {row['report_id'] for row in result} <= principal
    assert tally(result, 'release_route') == scope['result_use_counts']
    assert tally(result, 'risk_route') == certainty['certainty_scope']['result_RoB2_layer_counts']
    assert tally(result, 'grade_route') == certainty['certainty_scope']['result_grade_route_counts']
    comparisons = rows('data/comparison_routes.csv')
    assert len({row['comparison_id'] for row in comparisons}) == len(comparisons) == 26
    assert all(not row['unrestricted_primary_pool_K'] for row in comparisons)
    assert all(certainty['full_search'][k] is None for k in ('K', 'N', 'GRADE'))

    inputs = read_json('analysis/AGGREGATE_INPUTS_THREE_RESTRICTED_COMPARISONS.json')
    targets = certainty['restricted_comparisons']
    assert len(inputs['cases']) == len(targets) == 3
    assert [x['id'] for x in inputs['cases']] == [x['id'] for x in targets]
    for case, target in zip(inputs['cases'], targets):
        assert len({row['candidate_family_id'] for row in case['source_rows']}) == target['model_entry_K'] == 2
        assert case['pooled_effective_N'] is target['certified_effective_pooled_N'] is None
    return {
        'status': 'PASS_SHARED_AGGREGATE_SCOPE_CHECKS',
        'canonical_record_groups': focused + archive, 'report_catalogue_rows': len(catalogue),
        'retained_awaiting_reports': held['reports'], 'unknown_whole_review_flow_fields': len(unresolved),
        'bounded_study_families': len(families), 'principal_report_carriers': len(principal),
        'source_result_ledger_rows': len(result), 'nonadditive_clinical_comparison_rows': len(comparisons),
        'whole_review_K': None, 'whole_review_N': None, 'whole_review_GRADE': None,
    }

def main():
    parser = ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path, default=ROOT / 'out')
    parser.add_argument('--data-only', action='store_true', help='Skip the R verification.')
    parser.add_argument('--figure', action='store_true', help='Rebuild Figure 1 with Matplotlib.')
    args = parser.parse_args()
    summary = verify_data()
    summary['manifest_files_checked'] = verify_manifest()
    args.output.mkdir(parents=True, exist_ok=True)
    if not args.data_only:
        subprocess.run(
            ['Rscript', str(ROOT / 'analysis/verify_existing_six_clinical_fits.R'), str(args.output.resolve())],
            check=True,
        )
        verification = json.loads((args.output / 'VERIFICATION_SIX_EXISTING_CLINICAL_FITS.json').read_bytes())
        assert verification['verification_model_evaluations'] == 6
        assert verification['new_scientific_fits'] == 0
        assert verification['check_count'] == len(verification['checks']) == 74
        assert all(check['pass'] for check in verification['checks'])
        assert all(model['model_entry_K'] == 2 and model['effective_pooled_N'] is None
                   for item in verification['results'] for model in item['models'])
        summary['existing_model_evaluations'] = 6
        summary['model_checks'] = 74
        summary['new_scientific_models'] = 0
    if args.figure:
        figure_out = args.output.resolve() / 'figures'
        subprocess.run(
            [sys.executable, str(ROOT / 'figures/build_prisma_figure.py'), '--output', str(figure_out)],
            check=True,
        )
        for ext in ('pdf', 'svg', 'png'):
            assert (figure_out / f'Figure_1_PRISMA_2020.{ext}').stat().st_size > 0
        summary['figure_1_rebuilt'] = True
    (args.output / 'run_summary.json').write_text(json.dumps(summary, indent=2) + '\n')
    print(json.dumps(summary, sort_keys=True))

if __name__ == '__main__':
    main()
