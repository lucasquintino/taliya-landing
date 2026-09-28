import { execFileSync } from "node:child_process";

import { assert, readText, writeReport } from "./eval-agent-runtime-utils.mjs";

const usage = readText("services/taliya-agent-runtime/app/runtime/usage.py");
const runner = readText("services/taliya-agent-runtime/app/runtime/runner.py");
const store = readText("services/taliya-agent-runtime/app/shared/memory/postgres.py");

const results = [
  assert(usage.includes("ModelUsageRecord"), "usage.py defines model usage records"),
  assert(usage.includes("hard_cap_blocked"), "usage.py classifies hard cost cap"),
  assert(runner.includes("status=\"cost_capped\""), "runner returns cost_capped when budget is exhausted"),
  assert(runner.includes("human_follow_up_required"), "cost cap creates operator follow-up flag"),
  assert(store.includes("record_model_usage"), "memory store persists model usage summaries"),
];

try {
  execFileSync("python", ["-m", "pytest", "services/taliya-agent-runtime/tests/test_model_usage.py", "-q"], {
    cwd: process.cwd(),
    stdio: "pipe",
    encoding: "utf8",
  });
  results.push(assert(true, "model usage and cost cap tests pass"));
} catch (error) {
  results.push(
    assert(false, "model usage and cost cap tests pass", {
      stdout: error.stdout,
      stderr: error.stderr,
      status: error.status,
    }),
  );
}

writeReport("agent-runtime-cost", results);
