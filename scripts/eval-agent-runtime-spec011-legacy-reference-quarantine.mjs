import fs from "node:fs";
import path from "node:path";

const root = process.cwd();
const reportDir = path.join(root, "specs", "011-taliya-commercial-agent-core-reset", "eval-reports");

function readText(relativePath) {
  return fs.readFileSync(path.join(root, relativePath), "utf8").replace(/^\uFEFF/, "");
}

function walkFiles(relativeDir, extensions = new Set([".py"])) {
  const absoluteDir = path.join(root, relativeDir);
  const files = [];
  for (const item of fs.readdirSync(absoluteDir, { withFileTypes: true })) {
    const absolutePath = path.join(absoluteDir, item.name);
    const relativePath = path.relative(root, absolutePath).replaceAll("\\", "/");
    if (item.isDirectory()) {
      files.push(...walkFiles(relativePath, extensions));
    } else if (extensions.has(path.extname(item.name))) {
      files.push(relativePath);
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

const pyprojectPath = "services/taliya-agent-runtime/pyproject.toml";
const readmePath = "services/taliya-agent-runtime/README.md";
const realOpenAiPath = "scripts/eval-agent-runtime-real-openai.py";
const legacyEvalPath = "scripts/eval-agent-runtime-legacy-behavior.py";
const testFiles = walkFiles("services/taliya-agent-runtime/tests");

const runnerImportTests = testFiles
  .filter((file) => readText(file).includes("app.runtime.runner"))
  .map((file) => ({
    file,
    marked: readText(file).includes("pytestmark = pytest.mark.legacy_runner_reference"),
  }));
const unmarkedRunnerImportTests = runnerImportTests.filter((item) => !item.marked);
const realOpenAiLegacyEndpointHits = lineHits(realOpenAiPath, /client\.post\("\/v1\/agent-runs"/);

const readmeText = readText(readmePath);
const realOpenAiText = readText(realOpenAiPath);
const legacyEvalText = readText(legacyEvalPath);
const pyprojectText = readText(pyprojectPath);

const results = [
  result(
    unmarkedRunnerImportTests.length === 0 && runnerImportTests.length > 0,
    "all tests importing the legacy runner are explicitly marked as legacy_runner_reference",
    { runnerImportTests, unmarkedRunnerImportTests },
  ),
  result(
    pyprojectText.includes("legacy_runner_reference:"),
    "pytest marker registry documents legacy runner reference tests",
    { markerPath: pyprojectPath },
  ),
  result(
    readmeText.includes("POST /v1/taliya-commercial/turn") &&
      readmeText.includes("legacy_commercial_runner_quarantined") &&
      readmeText.includes("not a production behavior or quality gate"),
    "runtime README names Spec 011 as active endpoint and quarantines /v1/agent-runs",
    { readmePath },
  ),
  result(
    realOpenAiText.includes('FEATURE_NAME = "011-taliya-commercial-agent-core-reset"') &&
      realOpenAiText.includes('"/v1/taliya-commercial/turn"') &&
      realOpenAiLegacyEndpointHits.length === 0,
    "real OpenAI production-path eval posts to the Spec 011 endpoint, not /v1/agent-runs",
    { realOpenAiLegacyEndpointHits },
  ),
  result(
    legacyEvalText.includes("LEGACY_RUNNER_REFERENCE_ONLY = True") &&
      legacyEvalText.includes("PRODUCTION_PATH_GATE = False") &&
      legacyEvalText.includes('"referenceOnly": LEGACY_RUNNER_REFERENCE_ONLY') &&
      legacyEvalText.includes("not active production-path release evidence"),
    "legacy behavior eval is labeled as reference-only and not production-path evidence",
    { legacyEvalPath },
  ),
];

fs.mkdirSync(reportDir, { recursive: true });
const summary = {
  total: results.length,
  passed: results.filter((item) => item.ok).length,
  failed: results.filter((item) => !item.ok).length,
};
const report = {
  runId: `agent-runtime-spec011-legacy-reference-quarantine-${Date.now()}`,
  feature: "011-taliya-commercial-agent-core-reset",
  task: "T011-094",
  createdAt: new Date().toISOString(),
  summary,
  releaseGate: summary.failed === 0 ? "pass" : "fail",
  results,
};

const jsonPath = path.join(reportDir, "agent-runtime-spec011-legacy-reference-quarantine.json");
const mdPath = path.join(reportDir, "agent-runtime-spec011-legacy-reference-quarantine.md");
fs.writeFileSync(jsonPath, `${JSON.stringify(report, null, 2)}\n`);
fs.writeFileSync(
  mdPath,
  [
    "# agent-runtime-spec011-legacy-reference-quarantine",
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
  console.error(`agent-runtime-spec011-legacy-reference-quarantine: ${summary.failed} failure(s). Report: ${jsonPath}`);
  process.exitCode = 1;
} else {
  console.log(`agent-runtime-spec011-legacy-reference-quarantine: ${summary.passed}/${summary.total} passed. Report: ${jsonPath}`);
}
