import { execFileSync } from "node:child_process";

import { applyEvalBudget, assert, readJson, writeReport, writeTranscriptMarkdown } from "./eval-agent-runtime-utils.mjs";

const openings = readJson("scripts/fixtures/agent-runtime/free-form-openings.json");
const mixed = readJson("scripts/fixtures/agent-runtime/mixed-messages.json");
const budgeted = applyEvalBudget([...openings, ...mixed]);
const results = [];

results.push(assert(openings.length >= 3, "free-form opening fixtures are present"));
results.push(assert(mixed.length >= 3, "mixed-message fixtures are present"));
results.push(assert(budgeted.skipped.every((item) => item.reason), "skipped scenarios are labeled when eval budget trims cases"));

try {
  execFileSync("python", ["-m", "pytest", "services/taliya-agent-runtime/tests/test_agent_runs_api.py", "services/taliya-agent-runtime/tests/test_runner_events.py", "-q"], {
    cwd: process.cwd(),
    stdio: "pipe",
    encoding: "utf8",
  });
  results.push(assert(true, "runtime API and runner conversation contracts pass"));
} catch (error) {
  results.push(
    assert(false, "runtime API and runner conversation contracts pass", {
      stdout: error.stdout,
      stderr: error.stderr,
      status: error.status,
    }),
  );
}

writeReport("agent-runtime-conversations", results, {
  fixtureCounts: {
    openings: openings.length,
    mixed: mixed.length,
  },
  selectedScenarios: budgeted.selected.map((scenario) => scenario.id),
  skippedScenarios: budgeted.skipped,
});

writeTranscriptMarkdown("agent-runtime-transcripts-latest", [
  {
    title: "Conversation Fixture Summary",
    lines: budgeted.selected.map((scenario) => `- ${scenario.id}: ${scenario.message ?? (scenario.messages ?? []).join(" | ")}`),
  },
  {
    title: "Budget",
    lines: [
      `- maxScenarios: ${budgeted.budget.maxScenarios}`,
      `- maxModelCalls: ${budgeted.budget.maxModelCalls}`,
      `- maxCostUsd: ${budgeted.budget.maxCostUsd}`,
      `- skipped: ${budgeted.skipped.length}`,
    ],
  },
]);
