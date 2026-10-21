import copy
import json
import pytest
from test_v130 import _ready_inputs
from judicial_ai_safety_lab.real_case_assessment import build_real_case_assessment
from judicial_ai_safety_lab.assessment_replay import compare_assessment_runs, _hash
from judicial_ai_safety_lab.assessment_replay_cli import main


def freeze(run):
    rows = run['cases']
    run['case_count'] = run['verified_count'] = len(rows)
    run['assessment_hash'] = _hash({'target_commit': run['target_commit'],
        'case_count': len(rows), 'case_ids': [r['case_id'] for r in rows],
        'raw_hashes': [r['raw_response_hash'] for r in rows],
        'normalized_hashes': [r['normalized_hash'] for r in rows]})
    return run


@pytest.fixture
def runs():
    d, e, p = _ready_inputs()
    a = build_real_case_assessment(d, e, p, target_commit='a'*40)
    return a, copy.deepcopy(a)


def test_matching_artifacts_do_not_imply_expert_validation(runs):
    result = compare_assessment_runs(*runs)
    assert result['status'] == 'MATCH'
    assert result['human_review_required']
    assert not result['independent_rerun_verified']
    assert not result['legal_correctness_verified']


def test_output_tampering_not_covered_by_v13_hash_is_detected(runs):
    a, b = runs
    b['cases'][0]['system_output'] = 'changed output'
    assert a['assessment_hash'] == b['assessment_hash']
    result = compare_assessment_runs(a, b)
    assert result['status'] == 'OUTPUT_CHANGED'
    assert result['retest_case_ids'] == [b['cases'][0]['case_id']]
    assert 'changed output' not in json.dumps(result)


def test_source_changes_are_not_scored_as_output_regression(runs):
    a, b = runs
    b['cases'][0]['raw_response_hash'] = 'b'*64
    result = compare_assessment_runs(a, freeze(b))
    assert result['status'] == 'NOT_COMPARABLE'
    assert result['cases'][0]['status'] == 'INPUT_CHANGED'


def test_changed_commit_can_compare_same_input(runs):
    a, b = runs
    b['target_commit'] = 'b'*40
    result = compare_assessment_runs(a, freeze(b))
    assert result['status'] == 'MATCH' and not result['same_commit']


def test_reordering_is_not_a_regression(runs):
    a, b = runs
    b['cases'].reverse()
    assert compare_assessment_runs(a, freeze(b))['status'] == 'MATCH'


def test_missing_cases_block_comparison(runs):
    a, b = runs
    removed = b['cases'].pop()['case_id']
    result = compare_assessment_runs(a, freeze(b))
    assert result['status'] == 'NOT_COMPARABLE'
    assert result['missing_case_ids'] == [removed]


@pytest.mark.parametrize('mutation', ['duplicate', 'hash', 'count', 'boolean', 'missing', 'nan'])
def test_malformed_artifacts_are_rejected(runs, mutation):
    a, b = runs
    if mutation == 'duplicate': b['cases'][1] = copy.deepcopy(b['cases'][0])
    if mutation == 'hash': b['assessment_hash'] = '0'*64
    if mutation == 'count': b['case_count'] = True
    if mutation == 'boolean': b['cases'][0]['human_review_required'] = 'false'
    if mutation == 'missing': del b['cases'][0]['verification_tasks']
    if mutation == 'nan': b['extra'] = float('nan')
    with pytest.raises(ValueError): compare_assessment_runs(a, b)


def test_cli_exit_codes_and_no_overwrite(runs, tmp_path):
    a, b = runs
    ref, new, out = [tmp_path/x for x in ('ref.json', 'new.json', 'out.json')]
    ref.write_text(json.dumps(a))
    b['cases'][0]['human_review_required'] = not b['cases'][0]['human_review_required']
    new.write_text(json.dumps(b))
    args = ['--reference', str(ref), '--candidate', str(new), '--output', str(out)]
    assert main(args) == 1
    original = out.read_bytes()
    with pytest.raises(SystemExit) as error: main(args)
    assert error.value.code == 2 and out.read_bytes() == original


def test_cli_rejects_duplicate_keys(tmp_path):
    ref = tmp_path/'bad.json'
    ref.write_text('{"schema":1,"schema":2}')
    with pytest.raises(SystemExit) as error:
        main(['--reference', str(ref), '--candidate', str(ref), '--output', str(tmp_path/'out')])
    assert error.value.code == 2
