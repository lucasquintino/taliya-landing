import { spawnSync } from "node:child_process";
import fs from "node:fs";
import path from "node:path";

const root = process.cwd();
const featureName = "011-taliya-commercial-agent-core-reset";
const reportDir = path.join(root, "specs", featureName, "eval-reports");
const fixturePath = path.join(root, "scripts", "fixtures", "agent-runtime", "spec-011-real-openai-p0.json");
const realReportName = process.env.SPEC011_REAL_MODEL_REPORT_NAME ?? "agent-runtime-spec011-p0-real-model";
const realReportPath = path.join(reportDir, `${realReportName}.json`);
const redBaselinePath = path.join(reportDir, "agent-runtime-spec011-p0-current-red-full.json");

const realModelCases = [
  "RC-011-001",
  "RC-011-002",
  "RC-011-003",
  "RC-011-004",
  "RC-011-005",
  "RC-011-006",
  "RC-011-007",
  "RC-011-008",
  "RC-011-009",
  "RC-011-012",
  "RC-011-013",
  "RC-011-014",
];

const supplementalCases = ["RC-011-010", "RC-011-011", "RC-011-014A"];
const allP0Cases = [...realModelCases, ...supplementalCases];

function result(ok, message, details = {}) {
  return { ok: Boolean(ok), message, details };
}

function rel(filePath) {
  return path.relative(root, filePath);
}

function runCommand(command, args) {
  const startedAt = new Date().toISOString();
  const run = spawnSync(command, args, {
    cwd: root,
    encoding: "utf8",
    shell: false,
  });
  return {
    command: [command, ...args].join(" "),
    startedAt,
    finishedAt: new Date().toISOString(),
    status: run.status,
    signal: run.signal,
    stdout: String(run.stdout || "").slice(-12000),
    stderr: String(run.stderr || "").slice(-12000),
    error: run.error ? String(run.error.message || run.error) : null,
  };
}

function readJson(filePath) {
  return JSON.parse(fs.readFileSync(filePath, "utf8"));
}

function writeReport(results, extra = {}) {
  fs.mkdirSync(reportDir, { recursive: true });
  const summary = {
    total: results.length,
    passed: results.filter((item) => item.ok).length,
    failed: results.filter((item) => !item.ok).length,
  };
  const report = {
    runId: `agent-runtime-spec011-p0-real-model-gate-${Date.now()}`,
    feature: featureName,
    createdAt: new Date().toISOString(),
    releaseGate: summary.failed === 0 ? "pass" : "fail",
    summary,
    results,
    ...extra,
  };
  const jsonPath = path.join(reportDir, "agent-runtime-spec011-p0-real-model-gate.json");
  fs.writeFileSync(jsonPath, `${JSON.stringify(report, null, 2)}\n`);

  const mdPath = path.join(reportDir, "agent-runtime-spec011-p0-real-model-gate.md");
  const lines = [
    "# agent-runtime-spec011-p0-real-model-gate",
    "",
    `Generated at: ${report.createdAt}`,
    `Release gate: ${report.releaseGate}`,
    `Passed: ${summary.passed}/${summary.total}`,
    "",
    ...results.flatMap((item) => [
      `## ${item.ok ? "PASS" : "FAIL"} ${item.message}`,
      "",
      "```json",
      JSON.stringify(item.details ?? {}, null, 2),
      "```",
      "",
    ]),
  ];
  fs.writeFileSync(mdPath, `${lines.join("\n").trim()}\n`);

  if (summary.failed > 0) {
    console.error(`agent-runtime-spec011-p0-real-model-gate: ${summary.failed} failure(s). Report: ${jsonPath}`);
    for (const item of results.filter((entry) => !entry.ok)) console.error(`- ${item.message}`);
    process.exitCode = 1;
  } else {
    console.log(`agent-runtime-spec011-p0-real-model-gate: ${summary.passed}/${summary.total} passed. Report: ${jsonPath}`);
  }
}

const results = [];

const scenarios = readJson(fixturePath);
const fixtureCoverage = new Set(
  scenarios.flatMap((scenario) => scenario.regression_case_ids || []),
);
const missingRealCases = realModelCases.filter((caseId) => !fixtureCoverage.has(caseId));
results.push(
  result(missingRealCases.length === 0, "real-model fixture covers required P0 behavior cases", {
    fixture: rel(fixturePath),
    scenarioCount: scenarios.length,
    expected: realModelCases,
    covered: [...fixtureCoverage].sort(),
    missing: missingRealCases,
  }),
);

if (fs.existsSync(redBaselinePath)) {
  const redBaseline = readJson(redBaselinePath);
  results.push(
    result(
      redBaseline.releaseGate === "fail" && Number(redBaseline.summary?.failed || 0) > 0,
      "RC-011-014A known red baseline exists and actually failed",
      {
        report: rel(redBaselinePath),
        releaseGate: redBaseline.releaseGate,
        summary: redBaseline.summary,
      },
    ),
  );
  const redContractRun = runCommand("node", [
    "scripts/eval-agent-runtime-spec011-report-contract.mjs",
    rel(redBaselinePath),
  ]);
  results.push(
    result(redContractRun.status !== 0, "RC-011-014A report contract rejects incomplete red baseline evidence", redContractRun),
  );
} else {
  results.push(result(false, "RC-011-014A red baseline report is missing", { report: rel(redBaselinePath) }));
}

const realRun = runCommand("python", [
  "scripts/eval-agent-runtime-real-openai.py",
  "--fixture",
  rel(fixturePath),
  "--report-name",
  realReportName,
  "--max-scenarios",
  "0",
  "--max-model-calls",
  "11",
  "--max-cost-usd",
  "0.35",
]);
results.push(result(realRun.status === 0, "real OpenAI P0 fixture passes against Spec 011 endpoint", realRun));

if (fs.existsSync(realReportPath)) {
  const realReport = readJson(realReportPath);
  results.push(
    result(realReport.releaseGate === "pass", "real OpenAI P0 report has pass release gate", {
      report: rel(realReportPath),
      model: realReport.model,
      summary: realReport.summary,
      releaseGate: realReport.releaseGate,
    }),
  );
  const reportContractRun = runCommand("node", [
    "scripts/eval-agent-runtime-spec011-report-contract.mjs",
    rel(realReportPath),
  ]);
  results.push(result(reportContractRun.status === 0, "real OpenAI P0 report has mandatory trace artifacts", reportContractRun));
} else {
  results.push(result(false, "real OpenAI P0 report was not written", { report: rel(realReportPath) }));
}

const deliveryRun = runCommand("node", ["scripts/eval-agent-runtime-spec011-delivery-turn-gate.mjs"]);
results.push(
  result(deliveryRun.status === 0, "RC-011-010/011 delivery duplicate and interleaving gate passes", deliveryRun),
);

const provenCases = new Set([
  ...realModelCases.filter((caseId) => fixtureCoverage.has(caseId)),
  ...(deliveryRun.status === 0 ? ["RC-011-010", "RC-011-011"] : []),
  ...(fs.existsSync(redBaselinePath) ? ["RC-011-014A"] : []),
]);
const missingAllCases = allP0Cases.filter((caseId) => !provenCases.has(caseId));
results.push(
  result(missingAllCases.length === 0, "Spec 011 P0 gate has explicit evidence mapping for all required cases", {
    expected: allP0Cases,
    proven: [...provenCases].sort(),
    missing: missingAllCases,
    realModelReport: rel(realReportPath),
    deliveryReport: rel(path.join(reportDir, "agent-runtime-spec011-delivery-turn-gate.json")),
    redBaselineReport: rel(redBaselinePath),
  }),
);

writeReport(results, {
  realModelReport: rel(realReportPath),
  redBaselineReport: rel(redBaselinePath),
  coveredCases: allP0Cases,
  supplementalCases,
});
