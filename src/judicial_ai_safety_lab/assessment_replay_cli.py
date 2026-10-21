"""Compare two frozen assessments; preserve inputs and refuse output overwrite."""
import argparse
import json
from pathlib import Path
from .assessment_replay import compare_assessment_runs
from .artifact_integrity import _unique_pairs, _reject_constant


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--reference', type=Path, required=True)
    parser.add_argument('--candidate', type=Path, required=True)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args(argv)
    try:
        runs = [json.loads(p.read_text(encoding='utf-8'),
            object_pairs_hook=_unique_pairs, parse_constant=_reject_constant)
            for p in (args.reference, args.candidate)]
        report = compare_assessment_runs(*runs)
        args.output.parent.mkdir(parents=True, exist_ok=True)
        with args.output.open('x', encoding='utf-8') as stream:
            json.dump(report, stream, ensure_ascii=False, indent=2, allow_nan=False)
    except (ValueError, TypeError, OSError) as error:
        parser.exit(2, f'assessment comparison rejected: {error}\n')
    print(json.dumps({'status': report['status'],
        'retest_case_ids': report['retest_case_ids']}, ensure_ascii=False))
    return 0 if report['status'] == 'MATCH' else 1


if __name__ == '__main__':
    raise SystemExit(main())
