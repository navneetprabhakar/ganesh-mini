"""Inventory frozen quality follow-up scope without executing candidate code.

Heuristic hits are review candidates, never inferred failures or approvals.
Systematic groups are explicit reviewer decisions supported by inspected IDs.
"""
import argparse
import hashlib
import json
import re
from collections import Counter
from pathlib import Path

from scripts.data.admit_expansion import canonical_json


ROOT = Path('datasets/cache/expansion-v1/cutoff-5885')
KEYS = ('lane', 'source', 'task_type', 'rejection_history')
GROUPS = {
    'go_elementary_training_targets': [
        'exp-v1-go-generation-0137', 'exp-v1-go-generation-0416',
        'exp-v1-go-repair-0025', 'exp-v1-go-repair-0034',
        'exp-v1-go-repair-0097', 'exp-v1-go-repair-0099',
        'exp-v1-go-repair-0143', 'exp-v1-go-repair-0259'],
    'sparse_element_validation': [
        'exp-v1-javascript-generation-0233', 'exp-v1-javascript-generation-0173',
        'exp-v1-javascript-generation-0206', 'exp-v1-javascript-generation-0319',
        'exp-v1-javascript-repair-0111', 'exp-v1-javascript-repair-0132',
        'exp-v1-javascript-repair-0240', 'exp-v1-typescript-generation-0273'],
    'subscription_registration_identity': [
        'exp-v1-typescript-generation-0382', 'exp-v1-typescript-generation-0281',
        'exp-v1-typescript-repair-0174'],
    'reference_accommodates_incorrect_test_or_api': [
        'exp-v1-rust-generation-0192', 'exp-v1-typescript-generation-0382',
        'exp-v1-typescript-repair-0208'],
    'incomplete_rust_generation_api': [
        'exp-v1-rust-generation-0279', 'exp-v1-rust-generation-0291',
        'exp-v1-rust-generation-0345', 'exp-v1-rust-generation-0466',
        'exp-v1-rust-generation-0568'],
    'python_mapping_contract': [
        'exp-v1-python-generation-0259', 'exp-v1-python-generation-0368'],
    'python_invalid_enum_exception': [
        'exp-v1-python-generation-0152', 'exp-v1-python-generation-0588'],
}


def stratum(row):
    return (row['lane'], row['source']['dataset'], row['task_type'],
            'corrected' if 'corrected against independent tests' in
            row['source'].get('transformation', '') else 'first_pass')


def hits(row):
    code = row['verification_task']['validation']['reference']['code']
    found = []
    if row['lane'] in ('javascript', 'typescript'):
        if re.search(r'\.(every|some|map|filter|reduce)\s*\(', code):
            found.append('js_array_callbacks_require_sparse_scope_review')
        if re.search(r'indexOf\s*\(\s*listener\s*\)', code):
            found.append('listener_function_index_not_registration_identity')
        if re.search(r'owner\s*[:?=]|\.owner', code) and 'subscri' in code.lower():
            found.append('subscription_owner_grouping')
        if re.search(r'^\s*find\([^\n]+\)\s*:\s*[^\n;]+;', code, re.M):
            found.append('public_find_overload_check_nullability')
    if row['lane'] == 'rust' and '"data"' in code and '"x:y"' in code:
        found.append('specific_data_x_y_exception')
    return found


def build(rows, review, followup_groups=None):
    by_id = {r['id']: r for r in rows}
    if len(by_id) != len(rows):
        raise ValueError('duplicate candidate IDs')
    sampled = {r['id']: r for r in review['records']}
    population = Counter(stratum(row) for row in rows)
    groups = []
    reopened = set()
    for name, ids in GROUPS.items():
        scopes = set()
        for identifier in ids:
            if identifier not in sampled or identifier not in by_id:
                raise ValueError('systematic finding must bind to frozen sample: ' + identifier)
            key = stratum(by_id[identifier])
            if key != tuple(sampled[identifier][k] for k in KEYS):
                raise ValueError('sample stratum mismatch: ' + identifier)
            scopes.add(key)
        reopened.update(scopes)
        groups.append({'group': name, 'inspected_evidence_ids': ids,
                       'status': 'affected-strata-reopened',
                       'strata': [dict(zip(KEYS, key), population=population[key])
                                  for key in sorted(scopes)]})
    # Explicit reviewer decisions outside the original sample can extend scope,
    # but only with candidate-bound executed diagnostics. They never enlarge
    # the frozen sample or turn heuristic matches into semantic labels.
    for name, evidence in (followup_groups or {}).items():
        if name in GROUPS or not evidence:
            raise ValueError('follow-up group must be new and nonempty')
        scopes = set()
        for item in evidence:
            identifier = item['id']
            row = by_id.get(identifier)
            if row is None or item['candidate_sha256'] != hashlib.sha256(canonical_json(row)).hexdigest():
                raise ValueError('follow-up candidate hash mismatch: ' + identifier)
            scopes.add(stratum(row))
        reopened.update(scopes)
        groups.append({'group': name,
                       'inspected_evidence_ids': [item['id'] for item in evidence],
                       'bound_followup_evidence': evidence,
                       'status': 'affected-strata-reopened',
                       'strata': [dict(zip(KEYS, key), population=population[key])
                                  for key in sorted(scopes)]})
    inventory = []
    for index, row in enumerate(rows, 1):
        tags = hits(row)
        if tags or stratum(row) in reopened:
            inventory.append({'id': row['id'], 'candidate_line': index,
                              'candidate_sha256': hashlib.sha256(canonical_json(row)).hexdigest(),
                              'stratum': dict(zip(KEYS, stratum(row))),
                              'heuristic_tags': tags,
                              'in_reopened_stratum': stratum(row) in reopened,
                              'semantically_inspected_in_frozen_sample': row['id'] in sampled})
    return {'status': 'requires-stratum-resolution-not-training-ready',
            'population': len(rows), 'sample_inspected': len(sampled),
            'policy': 'Scope inventory only. Pattern matches are not defects; absence is not clearance. Original corpus and reports remain immutable.',
            'systematic_groups': groups,
            'reopened_strata_count': len(reopened),
            'reopened_population': sum(population[k] for k in reopened),
            'heuristic_counts': dict(Counter(tag for r in inventory for tag in r['heuristic_tags'])),
            'records': inventory}


def load_followup_groups(path, rows):
    """Validate declared diagnostics; failure classification remains a reviewer decision."""
    by_id = {row['id']: row for row in rows}
    config = json.loads(path.read_text())
    groups = {}
    for name, items in config['groups'].items():
        bound = []
        for item in items:
            evidence_path = Path(item['evidence'])
            payload = evidence_path.read_bytes()
            report = json.loads(payload)
            row = by_id[item['id']]
            if (report['id'] != item['id'] or
                    report['candidate_sha256'] != hashlib.sha256(canonical_json(row)).hexdigest() or
                    report['original_task'] != row['verification_task']):
                raise ValueError('follow-up diagnostic candidate mismatch')
            result = report['result']
            codes = result.get('exit_codes', [])
            if result.get('timed_out') is not False or not codes or codes[-1] != 1 or any(c != 0 for c in codes[:-1]):
                raise ValueError('follow-up requires completed behavioral failure')
            bound.append({**item, 'candidate_sha256': report['candidate_sha256'],
                          'evidence_sha256': hashlib.sha256(payload).hexdigest()})
        groups[name] = bound
    return groups


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--output', type=Path, required=True)
    parser.add_argument('--followup-groups', type=Path)
    args = parser.parse_args()
    if args.output.exists():
        raise ValueError('preserve existing audit')
    manifest = json.loads((ROOT / 'manifest.json').read_text())
    bound = {}
    for name in ('final.candidates.jsonl', 'quality-review.json'):
        payload = (ROOT / name).read_bytes()
        sha = hashlib.sha256(payload).hexdigest()
        if sha != manifest['files'][name]['sha256']:
            raise ValueError('frozen input hash mismatch: ' + name)
        bound[name] = {'sha256': sha, 'bytes': len(payload)}
    rows = [json.loads(line) for line in (ROOT / 'final.candidates.jsonl').read_text().splitlines()]
    followup = load_followup_groups(args.followup_groups, rows) if args.followup_groups else None
    report = build(rows, json.loads((ROOT / 'quality-review.json').read_text()), followup)
    if args.followup_groups:
        report['followup_decisions'] = {'path': str(args.followup_groups),
            'sha256': hashlib.sha256(args.followup_groups.read_bytes()).hexdigest()}
    report['frozen_inputs'] = bound
    report['report_sha256'] = hashlib.sha256(canonical_json(report)).hexdigest()
    args.output.write_text(json.dumps(report, indent=2) + '\n')
    print(json.dumps({k: v for k, v in report.items() if k not in ('records', 'systematic_groups')}))


if __name__ == '__main__':
    main()
