"""Offline mutations prove that preparation cannot silently release dependencies."""
import importlib.util
import json
from pathlib import Path
import shutil
import tempfile
import unittest

SOURCE = Path(__file__).resolve().parents[1]
REPO = SOURCE.parents[1]
spec = importlib.util.spec_from_file_location('readiness', SOURCE / 'scripts/check_readiness.py')
readiness = importlib.util.module_from_spec(spec)
spec.loader.exec_module(readiness)


class ReadinessTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.repo = Path(self.tmp.name)
        self.root = self.repo / 'docs/taliya-sdd'
        shutil.copytree(SOURCE, self.root, ignore=shutil.ignore_patterns('*.png', '*.zip', '__pycache__'))
        for stage in json.loads((SOURCE / 'planning/program.json').read_text())['stages']:
            shutil.copytree(REPO / 'specs' / stage['directory'], self.repo / 'specs' / stage['directory'])

    def mutate(self, fn):
        path = self.root / 'planning/execution.json'
        data = json.loads(path.read_text())
        fn(data)
        path.write_text(json.dumps(data))

    def test_documented_does_not_mean_unblocked(self):
        report = readiness.inspect(self.root, '014')
        self.assertTrue(report['passed'])
        self.assertFalse(report['execution_unblocked'])
        self.assertIn('spec:013', report['tasks'][0]['impediments'])

    def test_missing_task_is_rejected(self):
        self.mutate(lambda d: d['tasks'].pop())
        self.assertIn('preparation/task coverage mismatch', readiness.inspect(self.root)['errors'])

    def test_cycle_is_rejected(self):
        self.mutate(lambda d: d['tasks'][0].update(depends_on_tasks=['T013-06']))
        self.assertTrue(any('cyclic task dependency' in e for e in readiness.inspect(self.root)['errors']))

    def test_unknown_blocker_is_rejected(self):
        self.mutate(lambda d: d['tasks'][0].update(blocker_ids=['B999']))
        self.assertIn('unknown blocker T013-01', readiness.inspect(self.root)['errors'])

    def test_cannot_resolve_blocker_without_evidence(self):
        self.mutate(lambda d: d['blockers']['B013-02'].update(state='resolved'))
        self.assertIn('resolved blocker without evidence B013-02', readiness.inspect(self.root)['errors'])

    def test_cannot_hide_acceptance_case(self):
        self.mutate(lambda d: d['tasks'][0].update(case_ids=[]))
        self.assertIn('case coverage mismatch T013-01', readiness.inspect(self.root)['errors'])

    def test_unknown_spec_is_not_unblocked(self):
        report = readiness.inspect(self.root, '999')
        self.assertFalse(report['passed'])
        self.assertFalse(report['execution_unblocked'])

    def test_uninspected_source_is_rejected(self):
        self.mutate(lambda d: d['profiles']['015']['existing_paths'].append('fake/billing.ts'))
        self.assertIn('source not inspected fake/billing.ts', readiness.inspect(self.root)['errors'])

    def test_environment_work_requires_specific_authorization(self):
        report = readiness.inspect(self.root, '016')
        smoke = next(t for t in report['tasks'] if t['task'] == 'T016-02')
        self.assertIn('specific_environment_authorization_must_be_verified', smoke['impediments'])

    def test_stale_markdown_is_rejected(self):
        path = self.repo / 'specs/016-runtime-agents-api-luna/execution.md'
        path.write_text('Task cards removed')
        self.assertTrue(any('missing or stale task card T016-' in e for e in readiness.inspect(self.root)['errors']))

    def test_check_does_not_mutate_progress(self):
        paths = ['STATUS.json', 'planning/tasks.json', 'planning/execution.json']
        before = {p: (self.root / p).read_bytes() for p in paths}
        readiness.inspect(self.root)
        self.assertEqual(before, {p: (self.root / p).read_bytes() for p in paths})


if __name__ == '__main__':
    unittest.main()
