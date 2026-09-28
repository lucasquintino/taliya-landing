#!/usr/bin/env node

import fs from "node:fs";
import path from "node:path";
import process from "node:process";

const FEATURE = "011-taliya-commercial-agent-core-reset";
const REPORT_DIR = path.join("specs", FEATURE, "eval-reports");

function usage() {
  return [
    "Usage:",
    "  node scripts/eval-agent-runtime-spec011-coverage-gate.mjs",
    "    --fixture <fixture.json> --report <report.json> [--report <report.json> ...]",
    "    --name <output-name>",
  ].join("\n");
}

function parseArgs(argv) {
  const parsed = { fixture: null, reports: [], name: null };
  for (let index = 0; index < argv.length; index += 1) {
    const arg = argv[index];
    const value = argv[index + 1];
    if (arg === "--fixture" && value) {
      parsed.fixture = value;
      index += 1;
    } else if (arg === "--report" && value) {
      parsed.reports.push(value);
      index += 1;
    } else if (arg === "--name" && value) {
      parsed.name = value;
      index += 1;
    } else {
      throw new Error(`Unknown or incomplete argument: ${arg}\n${usage()}`);
    }
  }
  if (!parsed.fixture || parsed.reports.length === 0 || !parsed.name) {
    throw new Error(usage());
  }
  return parsed;
}

function readJson(filePath) {
  return JSON.parse(fs.readFileSync(filePath, "utf8"));
}

function scenarioCost(scenario) {
  return (scenario.turns ?? []).reduce((total, turn) => {
    const usage = turn?.payload?.output?.usage ?? {};
    return total + Number(usage.cost_usd ?? 0);
  }, 0);
}

function isScenarioPass(scenario) {
  const failures = scenario.failures ?? [];
  const budgetStatus = scenario.budget_status ?? "within_budget";
  return failures.length === 0 && budgetStatus !== "stopped_before_completion";
}

function collectCoverage(expectedIds, reportPaths) {
  const passingById = new Map();
  const failedById = new Map();

  for (const reportPath of reportPaths) {
    const report = readJson(reportPath);
    for (const scenario of report.scenarios ?? []) {
      if (!expectedIds.has(scenario.id)) {
        continue;
      }
      const record = {
        id: scenario.id,
        report: reportPath,
        failures: scenario.failures ?? [],
        budget_status: scenario.budget_status ?? "within_budget",
        cost_usd: scenarioCost(scenario),
      };
      if (isScenarioPass(scenario)) {
        if (!passingById.has(scenario.id)) {
          passingById.set(scenario.id, record);
        }
      } else if (!failedById.has(scenario.id)) {
        failedById.set(scenario.id, record);
      }
    }
  }

  const passed = [...passingById.keys()].sort();
  const missing = [...expectedIds].filter((id) => !passingById.has(id)).sort();
  const failed = [...failedById.values()]
    .filter((record) => !passingById.has(record.id))
    .sort((left, right) => left.id.localeCompare(right.id));
  const selected = [...passingById.values()].sort((left, right) =>
    left.id.localeCompare(right.id),
  );

  return { passed, missing, failed, selected };
}

function writeReport(name, payload) {
  fs.mkdirSync(REPORT_DIR, { recursive: true });
  const outputPath = path.join(REPORT_DIR, `${name}.json`);
  fs.writeFileSync(outputPath, `${JSON.stringify(payload, null, 2)}\n`);
  return outputPath;
}

function main() {
  const args = parseArgs(process.argv.slice(2));
  const fixture = readJson(args.fixture);
  const expectedIds = new Set(fixture.map((scenario) => scenario.id));
  const coverage = collectCoverage(expectedIds, args.reports);
  const estimatedCostUsd = coverage.selected.reduce(
    (total, scenario) => total + scenario.cost_usd,
    0,
  );
  const releaseGate =
    coverage.missing.length === 0 && coverage.failed.length === 0 ? "pass" : "fail";
  const report = {
    feature: FEATURE,
    name: args.name,
    fixture: args.fixture,
    reports: args.reports,
    summary: {
      total: expectedIds.size,
      passed: coverage.passed.length,
      missing: coverage.missing.length,
      failed: coverage.failed.length,
      estimatedCostUsd: Number(estimatedCostUsd.toFixed(6)),
    },
    releaseGate,
    passedScenarioIds: coverage.passed,
    missingScenarioIds: coverage.missing,
    failedScenarios: coverage.failed,
    selectedEvidence: coverage.selected,
  };

  const outputPath = writeReport(args.name, report);
  console.log(
    `agent-runtime-spec011-coverage-gate: ${coverage.passed.length}/${expectedIds.size} passed`,
  );
  console.log(`Report: ${path.resolve(outputPath)}`);
  if (releaseGate !== "pass") {
    process.exitCode = 1;
  }
}

try {
  main();
} catch (error) {
  console.error(error.message);
  process.exit(1);
}
