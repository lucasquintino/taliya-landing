"""Temporary fixture copies only. No API, browser, application DB or secrets."""
import importlib.util
import json
from pathlib import Path
import shutil
import tempfile
import unittest

SOURCE = Path(__file__).resolve().parents[1]
REPO = SOURCE.parents[1]
module = importlib.util.spec_from_file_location("progress", SOURCE / "scripts/validate_progress.py")
progress = importlib.util.module_from_spec(module)
module.loader.exec_module(progress)

class ProgressGateTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.repo = Path(self.tmp.name)
        self.root = self.repo / "docs/taliya-sdd"
        shutil.copytree(SOURCE, self.root, ignore=shutil.ignore_patterns("*.png", "*.zip", "__pycache__"))
        for path in REPO.glob("specs/0[12][0-9]-*"):
            if int(path.name[:3]) >= 13:
                shutil.copytree(path, self.repo / "specs" / path.name)
        (self.repo / ".specify").mkdir()
        shutil.copyfile(REPO / ".specify/feature.json", self.repo / ".specify/feature.json")

    def mutate(self, name, fn):
        p = self.root / name
        data = json.loads(p.read_text())
        fn(data)
        p.write_text(json.dumps(data))

    def test_partial_execution_is_legitimate(self):
        self.assertEqual(progress.validate(self.root), [])

    def test_unfinished_spec_cannot_be_completed(self):
        self.mutate("STATUS.json", lambda x: x["specs"][0].update(status="completed"))
        self.assertTrue(any("unfinished tasks" in e for e in progress.validate(self.root)))

    def test_dependent_spec_cannot_start(self):
        self.mutate("STATUS.json", lambda x: x["specs"][1].update(status="in_progress"))
        self.assertTrue(any("unfinished dependency" in e for e in progress.validate(self.root)))

    def test_pass_requires_existing_evidence(self):
        self.mutate("evals/acceptance-cases.json", lambda x: x[1].update(evidence=["missing.md"]))
        self.assertTrue(any("missing case evidence" in e for e in progress.validate(self.root)))

    def test_checkbox_cannot_hide_unfinished_task(self):
        p = self.repo / "specs/013-fundacao-e-contratos/tasks.md"
        p.write_text(p.read_text().replace("- [ ] **T013-01**", "- [x] **T013-01**"))
        self.assertTrue(any("checkbox disagrees" in e for e in progress.validate(self.root)))

    def test_requirement_needs_passed_case(self):
        self.mutate("planning/requirements.json", lambda x: x[0].update(status="verified"))
        self.assertTrue(any("verified without passed case" in e for e in progress.validate(self.root)))

    def test_matrix_must_follow_execution(self):
        p = self.root / "05_MATRIZ_DE_COBERTURA.md"
        p.write_text(p.read_text().replace("| PARCIAL |", "| VERIFICADO |"))
        self.assertTrue(any("matrix disagreement" in e for e in progress.validate(self.root)))

    def test_model_effort_cannot_silently_change(self):
        self.mutate("agent/config.intent.json", lambda x: x.update(reasoning_effort="low"))
        self.assertIn("model or effort changed", progress.validate(self.root))

    def test_no_extra_tool(self):
        self.mutate("contracts/tools.json", lambda x: x.append({"name":"sql"}))
        self.assertIn("five tools changed", progress.validate(self.root))

    def test_pointer_must_select_active_spec(self):
        p = self.repo / ".specify/feature.json"
        p.write_text(json.dumps({"feature_directory":"specs/taliya-migration/001-fundacao-migracao"}))
        self.assertIn("active pointer mismatch", progress.validate(self.root))

    def test_evidence_cannot_escape_repo(self):
        self.mutate("evals/acceptance-cases.json", lambda x: x[1].update(evidence=["../../etc/passwd"]))
        self.assertTrue(any("missing case evidence" in e for e in progress.validate(self.root)))

    def test_cycles_are_rejected(self):
        self.mutate("planning/program.json", lambda x: x["stages"][0].update(deps=["014"]))
        self.assertIn("cyclic dependency", progress.validate(self.root))

if __name__ == "__main__":
    unittest.main()
