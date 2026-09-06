"""Check archived test-author evidence; this does not perform semantic review."""
import argparse
import hashlib
import json
from collections import Counter
from pathlib import Path

from scripts.data.admit_expansion import canonical_json, read_jsonl
from scripts.data.generate_expansion_qualification import test_prompt, critic_test_prompt, parse_events


def digest(data):
    return hashlib.sha256(data).hexdigest()


def check_run(run, *, critic=False):
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
    marker = 'Items: ' if critic else 'Tasks: '
    visible, _ = json.JSONDecoder().raw_decode(run['prompt'].split(marker, 1)[1])
    expected_fields = {'id', 'problem', 'test_code'} if critic else {'id', 'problem'}
    if any(set(item) != expected_fields for item in visible):
        raise ValueError('unexpected test-author input')
    expected_prompt = (critic_test_prompt(run['lane'], visible, visible) if critic
                       else test_prompt(run['lane'], visible))
    if expected_prompt != run['prompt']:
        raise ValueError('prompt differs from specification-only template')
    return {item['id']: item for item in visible}


def normalized_test(code):
    code = code.strip()
    if code.startswith('```'):
        lines = code.splitlines()[1:]
        if lines and lines[-1].strip() == '```':
            lines.pop()
        code = '\n'.join(lines).strip()
    return code + '\n'


def load_evidence(path):
    evidence = json.loads(path.read_text())
    seal = evidence.pop('evidence_sha256')
    if digest(canonical_json(evidence)) != seal:
        raise ValueError('teacher evidence seal mismatch')
    return evidence


def audit(row, origin):
    path = Path(origin['path'])
    if digest(path.read_bytes()) != origin['file_sha256']:
        raise ValueError('origin file hash mismatch')
    if digest(canonical_json(row)) != origin['candidate_sha256']:
        raise ValueError('candidate hash mismatch')
    evidence_path = path.parent / 'teacher-evidence.json'
    repair_path = path.parent / 'repair.teacher-evidence.json'
    initial_path = path.parent / 'candidates.jsonl'
    repaired_path = path.parent / 'repaired.candidates.jsonl'
    if path.name.startswith('source-pilot-') and path.name.endswith('-lineage.candidates.jsonl'):
        prefix = path.name.removesuffix('-lineage.candidates.jsonl')
        evidence_path = path.parent / (prefix + '.teacher-evidence.json')
        repair_path = path.parent / (prefix + '-repair.teacher-evidence.json')
        initial_path = path.parent / (prefix + '.candidates.jsonl')
        repaired_path = path.parent / (prefix + '-repaired.candidates.jsonl')
    evidence = load_evidence(evidence_path)
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
        code = normalized_test(outputs[row['id']])
        tests = [f for f in row['verification_task']['files'] if f['role'] == 'test']
        if len(tests) != 1:
            raise ValueError('expected exactly one final test file')
        status = 'original-specification-only-tests-verified'
        chain = []
        if tests[0]['content'] != code:
            repair = load_evidence(repair_path)
            if digest(initial_path.read_bytes()) != repair['input_sha256']:
                raise ValueError('critic input file hash mismatch')
            if digest(repaired_path.read_bytes()) != repair['output_sha256']:
                raise ValueError('critic output file hash mismatch')
            for corrected in repair['runs']:
                if corrected['run_kind'] != 'rejection-test-critic':
                    continue
                proposed = check_run(corrected, critic=True)
                if row['id'] not in proposed:
                    continue
                item = proposed[row['id']]
                if item['problem'].strip() != problem or normalized_test(item['test_code']) != code:
                    raise ValueError('critic input does not match original independent tests')
                final = {x['id']: x['test_code'] for x in json.loads(corrected['final_output'])['items']}
                if normalized_test(final[row['id']]) != tests[0]['content']:
                    raise ValueError('critic output does not match final tests')
                chain.append({'teacher_path': str(repair_path),
                              'teacher_file_sha256': digest(repair_path.read_bytes()),
                              'prompt_sha256': corrected['prompt_sha256'],
                              'input_sha256': repair['input_sha256'],
                              'output_sha256': repair['output_sha256']})
            if len(chain) != 1:
                raise ValueError('expected one matching independent critic run')
            status = 'specification-only-test-critic-chain-verified'
        return {'id': row['id'], 'status': status, 'critic_chain': chain,
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
