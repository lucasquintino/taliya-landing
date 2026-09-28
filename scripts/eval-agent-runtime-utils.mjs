import fs from "node:fs";
import path from "node:path";

export const root = process.cwd();
export const featureDir = path.join(root, "specs", "010-openai-cs-agents-adaptation-for-taliya-commercial");
export const reportDir = path.join(featureDir, "eval-reports");

export function readText(relativePath) {
  return fs.readFileSync(path.join(root, relativePath), "utf8").replace(/^\uFEFF/, "");
}

export function readJson(relativePath) {
  return JSON.parse(readText(relativePath));
}

export function assert(condition, message, details = {}) {
  return { ok: Boolean(condition), message, details };
}

export function getEvalBudget() {
  return {
    maxScenarios: Number(process.env.AGENT_RUNTIME_EVAL_MAX_SCENARIOS || 50),
    maxModelCalls: Number(process.env.AGENT_RUNTIME_EVAL_MAX_MODEL_CALLS || 0),
    maxCostUsd: Number(process.env.AGENT_RUNTIME_EVAL_MAX_COST_USD || 0),
  };
}

export function applyEvalBudget(scenarios, { estimatedModelCalls = 0, estimatedCostUsd = 0 } = {}) {
  const budget = getEvalBudget();
  const selected = scenarios.slice(0, Number.isFinite(budget.maxScenarios) && budget.maxScenarios > 0 ? budget.maxScenarios : scenarios.length);
  const skipped = scenarios.slice(selected.length).map((scenario) => ({
    id: scenario.id ?? scenario.scenarioId ?? "unnamed",
    reason: "max_scenarios_budget",
  }));
  if (budget.maxModelCalls > 0 && estimatedModelCalls > budget.maxModelCalls) {
    return {
      selected: [],
      skipped: scenarios.map((scenario) => ({
        id: scenario.id ?? scenario.scenarioId ?? "unnamed",
        reason: "max_model_calls_budget",
      })),
      budget,
    };
  }
  if (budget.maxCostUsd > 0 && estimatedCostUsd > budget.maxCostUsd) {
    return {
      selected: [],
      skipped: scenarios.map((scenario) => ({
        id: scenario.id ?? scenario.scenarioId ?? "unnamed",
        reason: "max_cost_budget",
      })),
      budget,
    };
  }
  return { selected, skipped, budget };
}

export function writeReport(name, results, extra = {}) {
  fs.mkdirSync(reportDir, { recursive: true });
  const summary = {
    total: results.length,
    passed: results.filter((result) => result.ok).length,
    failed: results.filter((result) => !result.ok).length,
  };
  const report = {
    runId: `${name}-${Date.now()}`,
    feature: "010-openai-cs-agents-adaptation-for-taliya-commercial",
    createdAt: new Date().toISOString(),
    summary,
    results,
    releaseGate: summary.failed === 0 ? "pass" : "fail",
    budget: getEvalBudget(),
    ...extra,
  };
  const file = path.join(reportDir, `${name}.json`);
  fs.writeFileSync(file, `${JSON.stringify(report, null, 2)}\n`);
  if (summary.failed > 0) {
    console.error(`${name}: ${summary.failed} failure(s). Report: ${file}`);
    for (const result of results.filter((item) => !item.ok)) console.error(`- ${result.message}`);
    process.exitCode = 1;
  } else {
    console.log(`${name}: ${summary.passed}/${summary.total} passed. Report: ${file}`);
  }
}

export function writeTranscriptMarkdown(name, sections) {
  fs.mkdirSync(reportDir, { recursive: true });
  const file = path.join(reportDir, `${name}.md`);
  const lines = [
    `# ${name}`,
    "",
    `Generated at: ${new Date().toISOString()}`,
    "",
    ...sections.flatMap((section) => [
      `## ${section.title}`,
      "",
      ...(section.lines ?? []),
      "",
    ]),
  ];
  fs.writeFileSync(file, `${lines.join("\n").trim()}\n`);
  return file;
}
