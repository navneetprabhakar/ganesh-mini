"""Check archived test-author evidence; this does not perform semantic review."""
import argparse
import hashlib
import json
from collections import Counter
from pathlib import Path

from scripts.data.admit_expansion import canonical_json, read_jsonl
from scripts.data.generate_expansion_qualification import test_prompt, parse_events


def digest(data):
    return hashlib.sha256(data).hexdigest()


def check_run(run):
    for field, hash_field in [('prompt', 'prompt_sha256'), ('final_output', 'final_output_sha256'),
                              ('stdout_jsonl', 'stdout_sha256'), ('stderr', 'stderr_sha256')]:
        if digest(run[field].encode()) != run[hash_field]:
            raise ValueError(f'{field} hash mismatch')
    events, usage, disallowed = parse_events(run['stdout_jsonl'])
    if events != run['events'] or not usage or disallowed or run['returncode'] != 0:
        raise ValueError('invalid execution events')
    command = run['command_identity']
    if not all(flag in command for flag in ['--ephemeral', '--ignore-user-config', '--ignore-rules', '-C']):
        raise ValueError('missing isolation flags')
    if command[command.index('--sandbox') + 1] != 'read-only':
        raise ValueError('wrong sandbox')
    visible, _ = json.JSONDecoder().raw_decode(run['prompt'].split('Tasks: ', 1)[1])
    if any(set(item) != {'id', 'problem'} for item in visible):
        raise ValueError('unexpected test-author input')
    if test_prompt(run['lane'], visible) != run['prompt']:
        raise ValueError('prompt differs from specification-only template')
    return {item['id']: item for item in visible}


def audit(row, origin):
    path = Path(origin['path'])
    if digest(path.read_bytes()) != origin['file_sha256']:
        raise ValueError('origin file hash mismatch')
    if digest(canonical_json(row)) != origin['candidate_sha256']:
        raise ValueError('candidate hash mismatch')
    evidence_path = path.parent / 'teacher-evidence.json'
    evidence = json.loads(evidence_path.read_text())
    seal = evidence.pop('evidence_sha256')
    if digest(canonical_json(evidence)) != seal:
        raise ValueError('teacher evidence seal mismatch')
    for run in evidence['runs']:
        if run['run_kind'] != 'source-test-author':
            continue
        visible = check_run(run)
        if row['id'] not in visible:
            continue
        problem = visible[row['id']]['problem'].strip()
        suffix = '\n\nReturn only the complete source file; do not include Markdown fences or prose.'
        if problem + suffix != row['messages'][0]['content']:
            raise ValueError('final specification differs from original test input')
        outputs = {x['id']: x['test_code'] for x in json.loads(run['final_output'])['items']}
        code = outputs[row['id']].strip()
        if code.startswith('```'):
            lines = code.splitlines()[1:]
            if lines and lines[-1].strip() == '```':
                lines.pop()
            code = '\n'.join(lines).strip()
        tests = [f for f in row['verification_task']['files'] if f['role'] == 'test']
        if len(tests) != 1 or tests[0]['content'] != code + '\n':
            raise ValueError('final tests changed; requires critic-chain audit')
        return {'id': row['id'], 'status': 'original-specification-only-tests-verified',
                'candidate_sha256': origin['candidate_sha256'], 'teacher_path': str(evidence_path),
                'teacher_file_sha256': digest(evidence_path.read_bytes()),
                'prompt_sha256': run['prompt_sha256'], 'test_sha256': tests[0]['sha256'],
                'limitation': 'Evidence trace, not semantic sign-off or proof of hidden provider isolation.'}
    raise ValueError('no matching original test-author run')


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--count', type=int, required=True)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    if args.output.exists():
        raise ValueError('preserve existing audit')
    root = Path('datasets/cache/expansion-v1/cutoff-5885')
    sample = root / 'quality-sample.candidates.jsonl'
    manifest = json.loads((root / 'manifest.json').read_text())
    if digest(sample.read_bytes()) != manifest['files'][sample.name]['sha256']:
        raise ValueError('sample hash mismatch')
    origins = {x['id']: x for x in manifest['candidate_origins']}
    rows = read_jsonl(sample)
    if not 0 < args.count <= len(rows):
        raise ValueError('invalid count')
    findings = []
    for row in rows[:args.count]:
        try:
            findings.append(audit(row, origins[row['id']]))
        except (ValueError, KeyError, OSError) as exc:
            findings.append({'id': row['id'], 'status': 'unresolved', 'reason': str(exc)})
    result = {'sample_sha256': digest(sample.read_bytes()), 'records': findings,
              'scope': 'Archived test origin only; semantic quality review is separate.'}
    args.output.write_text(json.dumps(result, indent=2) + '\n')
    print(json.dumps(dict(Counter(row['status'] for row in findings)), sort_keys=True))


if __name__ == '__main__':
    main()
