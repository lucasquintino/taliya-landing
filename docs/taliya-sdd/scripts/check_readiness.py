#!/usr/bin/env python3
"""Read-only preparation check. Never executes tasks or authorizes remote work."""
import argparse
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]


def read(root, name):
    return json.loads((root / name).read_text())


def inspect(root=ROOT, selected=None):
    repo = root.parents[1]
    data = read(root, 'planning/execution.json')
    stages = {s['id']: s for s in read(root, 'planning/program.json')['stages']}
    tasks = {t['id']: t for t in read(root, 'planning/tasks.json')}
    reqs = {r['id']: r for r in read(root, 'planning/requirements.json')}
    status = read(root, 'STATUS.json')
    states = {s['id']: s['status'] for s in status['specs']}
    cards = {t['id']: t for t in data['tasks']}
    errors = []
    def check(ok, message):
        if not ok:
            errors.append(message)
    def local_file(path):
        return isinstance(path, str) and not Path(path).is_absolute() and '..' not in Path(path).parts and (repo / path).is_file()

    check(len(cards) == len(data['tasks']), 'duplicate preparation task')
    check(set(cards) == set(tasks), 'preparation/task coverage mismatch')
    check(set(data['profiles']) == set(stages), 'preparation/spec coverage mismatch')
    check(selected is None or selected in stages, 'unknown selected spec')
    for sid, profile in data['profiles'].items():
        check(bool(profile.get('interface')) and bool(profile.get('data_and_failure_plan')),
              'missing technical slice ' + sid)
        for path in profile['existing_paths']:
            check(path in data['source_hashes'] or any(p.startswith(path.rstrip('/') + '/') for p in data['source_hashes']),
                  'source not inspected ' + path)
        for path in profile['proposed_paths']:
            check(not Path(path).is_absolute() and '..' not in Path(path).parts and '://' not in path,
                  'invalid proposed local path ' + path)
    for key, blocker in data['blockers'].items():
        check(blocker['state'] in {'open', 'resolved'}, 'invalid blocker state ' + key)
        check(bool(blocker.get('owner')) and bool(blocker.get('resolution')), 'incomplete blocker ' + key)
        if blocker['state'] == 'resolved':
            evidence = blocker.get('evidence', [])
            check(bool(evidence) and all(local_file(x) for x in evidence), 'resolved blocker without evidence ' + key)
    visited, visiting = set(), set()
    def visit(tid):
        if tid in visiting:
            errors.append('cyclic task dependency ' + tid)
            return
        if tid in visited:
            return
        visiting.add(tid)
        for dep in cards[tid]['depends_on_tasks']:
            check(dep in cards, 'unknown task dependency ' + dep)
            if dep in cards:
                visit(dep)
        visiting.remove(tid)
        visited.add(tid)
    for tid, card in cards.items():
        visit(tid)
        if tid not in tasks:
            continue
        task = tasks[tid]
        check(card['spec'] == task['spec'], 'task spec mismatch ' + tid)
        check(card['requirement_ids'] == task['requirement_ids'], 'requirement mismatch ' + tid)
        expected = {c for r in task['requirement_ids'] for c in reqs[r]['test_ids']}
        check(set(card['case_ids']) == expected, 'case coverage mismatch ' + tid)
        check(set(card['blocker_ids']) <= data['blockers'].keys(), 'unknown blocker ' + tid)
        check(card['mode'] in {'local_after_dependencies', 'authorized_environment'}, 'invalid execution mode ' + tid)
        if card['spec'] in stages:
            path = repo / 'specs' / stages[card['spec']]['directory'] / 'execution.md'
            doc = path.read_text() if path.is_file() else ''
            check('### ' + tid in doc and card['deliverable'] in doc and card['test_oracle'] in doc,
                  'missing or stale task card ' + tid)
        check(local_file(card['evidence_target']), 'missing verification target ' + tid)
    # Report current impediments without treating human authorization as a JSON toggle.
    rows = []
    for tid, card in cards.items():
        if tid not in tasks or (selected and card['spec'] != selected):
            continue
        sid = card['spec']
        if sid not in stages:
            continue
        reasons = []
        if tasks[tid]['status'] != 'completed':
            if status.get('active_spec') != sid:
                reasons.append('spec_not_active')
            reasons += ['spec:' + dep for dep in stages[sid]['deps'] if states.get(dep) != 'completed']
            reasons += ['task:' + dep for dep in card['depends_on_tasks'] if tasks.get(dep, {}).get('status') != 'completed']
            reasons += [b for b in card['blocker_ids'] if data['blockers'].get(b, {}).get('state') != 'resolved']
            if card['mode'] == 'authorized_environment':
                reasons.append('specific_environment_authorization_must_be_verified')
            if tasks[tid]['status'] == 'blocked':
                reasons.append('task_marked_blocked_in_canonical_status')
        rows.append({'task': tid, 'execution_status': tasks[tid]['status'], 'impediments': reasons})
    return {'scope': 'preparation_consistency_only', 'passed': not errors, 'errors': errors,
            'active_spec': status.get('active_spec'), 'prepared_tasks': len(cards),
            'execution_unblocked': bool(rows) and not errors and all(not r['impediments'] for r in rows),
            'tasks': rows}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--spec', choices=[f'{i:03}' for i in range(13, 26)])
    parser.add_argument('--require-unblocked', action='store_true')
    args = parser.parse_args()
    try:
        report = inspect(selected=args.spec)
    except (KeyError, ValueError, TypeError, OSError) as exc:
        report = {'passed': False, 'errors': [str(exc)], 'execution_unblocked': False}
    print(json.dumps(report, ensure_ascii=False, indent=2))
    return 1 if not report['passed'] else 2 if args.require_unblocked and not report['execution_unblocked'] else 0


if __name__ == '__main__':
    sys.exit(main())
