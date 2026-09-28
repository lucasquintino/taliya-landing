from __future__ import annotations

import importlib.util
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
BASE_EVAL = ROOT / "scripts" / "eval-agent-runtime-real-openai.py"

spec = importlib.util.spec_from_file_location("agent_runtime_real_openai_eval", BASE_EVAL)
if spec is None or spec.loader is None:
    raise SystemExit(f"Unable to load base eval script: {BASE_EVAL}")

module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)

module.FEATURE_DIR = ROOT / "specs" / "011-taliya-commercial-agent-core-reset"
module.FEATURE_NAME = "011-taliya-commercial-agent-core-reset"
module.REPORT_DIR = module.FEATURE_DIR / "eval-reports"
module.FIXTURE_FILE = ROOT / "scripts" / "fixtures" / "agent-runtime" / "spec-011-real-openai-p0.json"
module.DEFAULT_REPORT_NAME = "agent-runtime-spec011-real-openai-p0-latest"


if __name__ == "__main__":
    raise SystemExit(module.main())
