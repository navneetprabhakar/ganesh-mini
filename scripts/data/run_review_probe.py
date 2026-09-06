"""Run a pinned sandbox review probe against a frozen reference."""
import argparse
import copy
import hashlib
import json
from pathlib import Path

from scripts.data.admit_expansion import canonical_json, read_jsonl
from scripts.verify.sandbox import verify


def main():
    p = argparse.ArgumentParser()
    p.add_argument('--id', required=True)
    p.add_argument('--probe', type=Path, required=True)
    p.add_argument('--output', type=Path, required=True)
    args = p.parse_args()
    if args.output.exists():
        raise ValueError('preserve existing evidence')
    root = Path('datasets/cache/expansion-v1/cutoff-5885')
    sample = root / 'quality-sample.candidates.jsonl'
    digest = lambda data: hashlib.sha256(data).hexdigest()
    manifest = json.loads((root / 'manifest.json').read_text())
    if digest(sample.read_bytes()) != manifest['files'][sample.name]['sha256']:
        raise ValueError('sample hash mismatch')
    row = next(r for r in read_jsonl(sample) if r['id'] == args.id)
    if row['lane'] not in ('go', 'java', 'javascript', 'python'):
        raise ValueError('unsupported probe language')
    task = copy.deepcopy(row['verification_task'])
    task['surface'] = 'synthetic_harness'
    content = args.probe.read_text()
    probe_path = {'go': 'review_test.go', 'java': 'SolutionTest.java',
                  'javascript': 'solution.test.js', 'python': 'test_solution.py'}[row['lane']]
    # Use the pinned runtime test entry point. Preserve the original task in
    # the output and use a separate diagnostic test; never edit the candidate.
    if row['lane'] != 'go':
        task['files'] = [f for f in task['files'] if f['path'] != probe_path]
    task['files'].append({'path': probe_path, 'role': 'test',
                          'content': content, 'sha256': digest(content.encode())})
    runtime = Path('configs/eval/runtimes.json')
    result = verify(task, task['validation']['reference']['code'], runtime)
    args.output.write_text(json.dumps({'id': row['id'], 'sample_sha256': digest(sample.read_bytes()),
        'candidate_sha256': digest(canonical_json(row)), 'task': task,
        'original_task': row['verification_task'],
        'probe_mode': 'additive' if row['lane'] == 'go' else 'isolated-test',
        'runtime_config_sha256': digest(runtime.read_bytes()), 'result': result}, indent=2) + '\n')
    print(json.dumps(result))


if __name__ == '__main__':
    main()
