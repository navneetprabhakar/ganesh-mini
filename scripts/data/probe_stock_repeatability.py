"""Run an evidence-preserving, sandboxed quality-review diagnostic."""
import copy
import argparse
import hashlib
import json
from pathlib import Path

from scripts.data.admit_expansion import canonical_json, read_jsonl
from scripts.verify.sandbox import verify


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    root = Path('measurement/data/expansion-v1/cutoff-5885-review')
    output = args.output
    if output.exists():
        raise ValueError('preserve existing diagnostic evidence')
    sample = Path('datasets/cache/expansion-v1/cutoff-5885/quality-sample.candidates.jsonl')
    row = next(r for r in read_jsonl(sample) if r['id'] == 'exp-v1-go-generation-0058')
    task = copy.deepcopy(row['verification_task'])
    task['surface'] = 'synthetic_harness'
    probe = (root / 'stock_repeatability_test.go').read_text()
    task['files'].append({'path': 'review_test.go', 'role': 'test',
                          'content': probe, 'sha256': hashlib.sha256(probe.encode()).hexdigest()})
    runtime = Path('configs/eval/runtimes.json')
    result = {'id': row['id'], 'candidate_sha256': hashlib.sha256(canonical_json(row)).hexdigest(),
              'sample_sha256': hashlib.sha256(sample.read_bytes()).hexdigest(),
              'runtime_config_sha256': hashlib.sha256(runtime.read_bytes()).hexdigest(),
              'task': task, 'interpretation': 'Outer diagnostic deliberately exits nonzero to expose counts; child original-suite counts control interpretation.'}
    for label, code in [('reference', task['validation']['reference']['code']),
                        ('known_bad', task['validation']['known_bad'][0]['code'])]:
        result[label] = verify(task, code, runtime)
        print(label, json.dumps(result[label]), flush=True)
    output.write_text(json.dumps(result, indent=2) + '\n')


if __name__ == '__main__':
    main()
