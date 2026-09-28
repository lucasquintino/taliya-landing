import fs from "node:fs";
import path from "node:path";

export const root = process.cwd();
export const featureDir = path.join(root, "specs", "009-taliya-sales-agent-architecture");
export const reportDir = path.join(featureDir, "eval-reports");

export function ensureReportDir() {
  fs.mkdirSync(reportDir, { recursive: true });
}

export function readText(relativePath) {
  return fs.readFileSync(path.join(root, relativePath), "utf8");
}

export function readJson(relativePath) {
  return JSON.parse(readText(relativePath));
}

export function assert(condition, message, details = {}) {
  return condition ? pass(message, details) : fail(message, details);
}

export function pass(message, details = {}) {
  return { ok: true, message, details };
}

export function fail(message, details = {}) {
  return { ok: false, message, details };
}

export function createBudgetFromEnv() {
  return {
    dryRun: process.env.AGENT_V2_EVAL_DRY_RUN !== "false",
    maxScenarios: numberEnv("AGENT_V2_EVAL_MAX_SCENARIOS", 25),
    maxRealModelCalls: numberEnv("AGENT_V2_EVAL_MAX_REAL_MODEL_CALLS", 0),
    maxEstimatedCostUsd: numberEnv("AGENT_V2_EVAL_MAX_ESTIMATED_COST_USD", 0.25),
    realModelCallCount: 0,
    estimatedCostUsd: 0,
    skippedScenarios: [],
  };
}

export function canRunScenario(budget, scenarioId, estimatedCost = 0.003) {
  if (budget.skippedScenarios.length >= budget.maxScenarios) {
    budget.skippedScenarios.push({ scenarioId, reason: "max_scenarios" });
    return false;
  }
  if (budget.realModelCallCount >= budget.maxRealModelCalls && !budget.dryRun) {
    budget.skippedScenarios.push({ scenarioId, reason: "max_real_model_calls" });
    return false;
  }
  if (budget.estimatedCostUsd + estimatedCost > budget.maxEstimatedCostUsd) {
    budget.skippedScenarios.push({ scenarioId, reason: "max_estimated_cost" });
    return false;
  }
  budget.estimatedCostUsd += estimatedCost;
  if (!budget.dryRun) budget.realModelCallCount += 1;
  return true;
}

export function writeReport(name, results, extra = {}) {
  ensureReportDir();
  const summary = {
    total: results.length,
    passed: results.filter((result) => result.ok).length,
    failed: results.filter((result) => !result.ok).length,
  };
  const report = {
    runId: `${name}-${Date.now()}`,
    feature: "009-taliya-sales-agent-architecture",
    createdAt: new Date().toISOString(),
    summary,
    results,
    releaseGate: summary.failed === 0 ? "pass" : "fail",
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
  return report;
}

export function contains(relativePath, patterns) {
  const source = readText(relativePath);
  return patterns.map((pattern) => ({
    pattern: String(pattern),
    found: pattern instanceof RegExp ? pattern.test(source) : source.includes(pattern),
  }));
}

function numberEnv(key, fallback) {
  const value = Number(process.env[key]);
  return Number.isFinite(value) ? value : fallback;
}

