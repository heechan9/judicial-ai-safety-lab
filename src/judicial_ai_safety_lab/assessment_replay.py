"""Compare frozen assessment runs without asserting legal correctness.

The v13 hash covers cohort/input fingerprints, not system outputs. Recompute
that contract, then separately compare all per-case outputs and source inputs.
No legal text or reviewer identity is copied into the resulting report.
"""
import hashlib
import json
import re

INPUT_FIELDS = ('raw_response_hash', 'normalized_hash', 'normalized_case')
OUTPUT_FIELDS = ('verification_status', 'title_equivalence', 'verification_tasks',
                 'system_output', 'human_review_required')
IDENTITY_FIELDS = ('source_id', 'prec_seq', 'domain')


def _hash(value):
    return hashlib.sha256(json.dumps(value, ensure_ascii=False, sort_keys=True,
        separators=(',', ':'), allow_nan=False).encode()).hexdigest()


def _hex(value, length):
    return isinstance(value, str) and re.fullmatch('[0-9a-f]{%d}' % length, value)


def _validate(run):
    if not isinstance(run, dict) or run.get('schema') != 'jaisl.real-assessment.v1':
        raise ValueError('unsupported assessment schema')
    if run.get('frozen') is not True or not _hex(run.get('target_commit'), 40):
        raise ValueError('frozen assessment with full target_commit required')
    rows = run.get('cases')
    if not isinstance(rows, list) or not rows:
        raise ValueError('non-empty cases required')
    if type(run.get('case_count')) is not int or run['case_count'] != len(rows):
        raise ValueError('case_count does not match cases')
    indexed = {}
    sources = set()
    for row in rows:
        if not isinstance(row, dict):
            raise ValueError('case must be an object')
        for key in ('case_id',) + IDENTITY_FIELDS:
            if not isinstance(row.get(key), str) or not row[key].strip():
                raise ValueError('non-empty case identity required: ' + key)
        if row['case_id'] in indexed or row['source_id'] in sources:
            raise ValueError('duplicate case or source identity')
        for key in INPUT_FIELDS + OUTPUT_FIELDS:
            if key not in row:
                raise ValueError('missing case field: ' + key)
        if not all(_hex(row[k], 64) for k in INPUT_FIELDS[:2]):
            raise ValueError('invalid input hash')
        if not isinstance(row['normalized_case'], dict) or not row['normalized_case']:
            raise ValueError('normalized_case must be a non-empty object')
        if _hash(row['normalized_case']) != row['normalized_hash']:
            raise ValueError('normalized_hash does not match normalized_case')
        for key in ('case_id',) + IDENTITY_FIELDS:
            if row['normalized_case'].get(key) != row[key]:
                raise ValueError('normalized case identity mismatch: ' + key)
        if not isinstance(row['verification_tasks'], list) or not row['verification_tasks']:
            raise ValueError('verification_tasks must be a non-empty list')
        if not isinstance(row['system_output'], str) or not row['system_output'].strip():
            raise ValueError('system_output must be non-empty')
        if type(row['human_review_required']) is not bool:
            raise ValueError('human_review_required must be boolean')
        if row['verification_status'] != 'VERIFIED_DETAIL_READY':
            raise ValueError('frozen assessment requires verified cases')
        indexed[row['case_id']] = row
        sources.add(row['source_id'])
    if type(run.get('verified_count')) is not int or run['verified_count'] != len(rows):
        raise ValueError('verified_count does not match verified cases')
    payload = {'target_commit': run['target_commit'], 'case_count': len(rows),
        'case_ids': [r['case_id'] for r in rows],
        'raw_hashes': [r['raw_response_hash'] for r in rows],
        'normalized_hashes': [r['normalized_hash'] for r in rows]}
    if run.get('assessment_hash') != _hash(payload):
        raise ValueError('assessment_hash does not match frozen inputs')
    _hash(run)  # Reject non-finite/non-JSON payloads even in unexamined fields.
    return indexed


def compare_assessment_runs(reference, candidate):
    """Return a descriptive, fail-closed comparison; never a release approval."""
    before, after = _validate(reference), _validate(candidate)
    missing = sorted(before.keys() - after.keys())
    added = sorted(after.keys() - before.keys())
    cases = []
    for case_id in sorted(before.keys() & after.keys()):
        a, b = before[case_id], after[case_id]
        identity = [f for f in IDENTITY_FIELDS if a[f] != b[f]]
        inputs = [f for f in INPUT_FIELDS if a[f] != b[f]]
        outputs = [f for f in OUTPUT_FIELDS if a[f] != b[f]]
        state = ('IDENTITY_CHANGED' if identity else 'INPUT_CHANGED' if inputs
                 else 'OUTPUT_CHANGED' if outputs else 'MATCH')
        cases.append({'case_id': case_id, 'status': state,
            'identity_changes': identity, 'input_changes': inputs,
            'output_changes': outputs})
    comparable = not (missing or added or any(
        c['identity_changes'] or c['input_changes'] for c in cases))
    changed = [c['case_id'] for c in cases if c['status'] != 'MATCH']
    status = ('NOT_COMPARABLE' if not comparable else
              'OUTPUT_CHANGED' if changed else 'MATCH')
    return {'schema': 'jaisl.assessment-replay.v1', 'status': status,
        'same_inputs': comparable, 'missing_case_ids': missing,
        'added_case_ids': added, 'cases': cases,
        'retest_case_ids': sorted(set(changed + missing + added)),
        'reference_commit': reference['target_commit'],
        'candidate_commit': candidate['target_commit'],
        'same_commit': reference['target_commit'] == candidate['target_commit'],
        'reference_artifact_hash': _hash(reference),
        'candidate_artifact_hash': _hash(candidate),
        'human_review_required': True,
        'legal_correctness_verified': False,
        'independent_rerun_verified': False,
        'limitations': ['Artifact comparison only; execution and operator independence are not verified.',
            'MATCH does not establish legal correctness or expert-review completion.',
            'Input changes require separate source review before output comparisons.']}
