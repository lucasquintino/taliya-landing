import { execFileSync } from "node:child_process";

import { assert, readJson, writeReport } from "./eval-agent-runtime-utils.mjs";

const rich = readJson("scripts/fixtures/agent-runtime/diagnostic-rich-context.json");
const thin = readJson("scripts/fixtures/agent-runtime/diagnostic-thin-context.json");
const results = [
  assert(rich.length >= 2, "rich diagnostic fixtures are present"),
  assert(thin.length >= 2, "thin diagnostic fixtures are present"),
];

try {
  execFileSync("python", ["-m", "pytest", "services/taliya-agent-runtime/tests/test_diagnostic.py", "services/taliya-agent-runtime/tests/test_structured_output.py", "-q"], {
    cwd: process.cwd(),
    stdio: "pipe",
    encoding: "utf8",
  });
  results.push(assert(true, "diagnostic runtime and fake-certainty tests pass"));
} catch (error) {
  results.push(
    assert(false, "diagnostic runtime and fake-certainty tests pass", {
      stdout: error.stdout,
      stderr: error.stderr,
      status: error.status,
    }),
  );
}

writeReport("agent-runtime-diagnostic", results, {
  fixtureCounts: { rich: rich.length, thin: thin.length },
});
