import fs from "node:fs";
import path from "node:path";

const root = process.cwd();
const reportDir = path.join(root, "specs", "011-taliya-commercial-agent-core-reset", "eval-reports");

function readText(relativePath) {
  return fs.readFileSync(path.join(root, relativePath), "utf8").replace(/^\uFEFF/, "");
}

function walkFiles(relativeDir, extensions = new Set([".py"])) {
  const dir = path.join(root, relativeDir);
  const files = [];
  for (const item of fs.readdirSync(dir, { withFileTypes: true })) {
    const absolute = path.join(dir, item.name);
    const relative = path.relative(root, absolute).replaceAll("\\", "/");
    if (item.isDirectory()) {
      files.push(...walkFiles(relative, extensions));
    } else if (extensions.has(path.extname(item.name))) {
      files.push(relative);
    }
  }
  return files;
}

function lineHits(relativePath, regex) {
  return readText(relativePath)
    .split(/\r?\n/)
    .flatMap((line, index) => (regex.test(line) ? [{ path: relativePath, line: index + 1, text: line.trim() }] : []));
}

function result(ok, message, details = {}) {
  return { ok: Boolean(ok), message, details };
}

const mainPath = "services/taliya-agent-runtime/app/main.py";
const runtimeClientPath = "lib/landing/ai-attendant/runtime-client.ts";
const coreFiles = walkFiles("services/taliya-agent-runtime/app/core/taliya_commercial");
const mainText = readText(mainPath);
const runtimeClientText = readText(runtimeClientPath);

const mainRunnerImportHits = [
  ...lineHits(mainPath, /\bfrom app\.runtime\.runner import\b/),
  ...lineHits(mainPath, /\brun_agent_turn\b/),
];
const coreRunnerImportHits = coreFiles.flatMap((file) =>
  lineHits(file, /\bfrom app\.runtime\.runner import\b|\bapp\.runtime\.runner\b|\brun_agent_turn\b/),
);
const legacyEndpointQuarantineHits = [
  ...lineHits(mainPath, /legacy_commercial_runner_quarantined/),
  ...lineHits(mainPath, /Taliya commercial turns must use \/v1\/taliya-commercial\/turn/),
];
const operationalControlHits = [
  ...lineHits(mainPath, /runtime_control/),
  ...lineHits(mainPath, /pause_human/),
  ...lineHits(mainPath, /resume_human/),
  ...lineHits(mainPath, /input_tokens=0/),
];
const runtimeClientLegacyTurnHits = lineHits(runtimeClientPath, /fetch\(`\$\{url\}\/v1\/agent-runs`/);

const results = [
  result(
    mainRunnerImportHits.length === 0,
    "runtime API shell does not import or call runtime/runner.py",
    { mainRunnerImportHits },
  ),
  result(
    coreRunnerImportHits.length === 0,
    "Spec 011 core package does not import or call runtime/runner.py",
    { coreRunnerImportHits },
  ),
  result(
    legacyEndpointQuarantineHits.length >= 2,
    "legacy /v1/agent-runs rejects Taliya commercial turns instead of calling the old runner",
    { legacyEndpointQuarantineHits },
  ),
  result(
    operationalControlHits.length >= 4,
    "legacy /v1/agent-runs keeps only zero-token runtime_control handoff operations",
    { operationalControlHits },
  ),
  result(
    runtimeClientText.includes('return "/v1/taliya-commercial/turn"') && runtimeClientLegacyTurnHits.length === 0,
    "public commercial runtime client does not post turns to /v1/agent-runs",
    { runtimeClientLegacyTurnHits },
  ),
];

fs.mkdirSync(reportDir, { recursive: true });
const summary = {
  total: results.length,
  passed: results.filter((item) => item.ok).length,
  failed: results.filter((item) => !item.ok).length,
};
const report = {
  runId: `agent-runtime-spec011-runner-quarantine-${Date.now()}`,
  feature: "011-taliya-commercial-agent-core-reset",
  task: "T011-093",
  createdAt: new Date().toISOString(),
  summary,
  releaseGate: summary.failed === 0 ? "pass" : "fail",
  checkedFiles: {
    runtimeApi: mainPath,
    runtimeClient: runtimeClientPath,
    coreFiles,
  },
  results,
};

const jsonPath = path.join(reportDir, "agent-runtime-spec011-runner-quarantine.json");
const mdPath = path.join(reportDir, "agent-runtime-spec011-runner-quarantine.md");
fs.writeFileSync(jsonPath, `${JSON.stringify(report, null, 2)}\n`);
fs.writeFileSync(
  mdPath,
  [
    "# agent-runtime-spec011-runner-quarantine",
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
  ].join("\n").trim() + "\n",
);

if (summary.failed > 0) {
  console.error(`agent-runtime-spec011-runner-quarantine: ${summary.failed} failure(s). Report: ${jsonPath}`);
  process.exitCode = 1;
} else {
  console.log(`agent-runtime-spec011-runner-quarantine: ${summary.passed}/${summary.total} passed. Report: ${jsonPath}`);
}
