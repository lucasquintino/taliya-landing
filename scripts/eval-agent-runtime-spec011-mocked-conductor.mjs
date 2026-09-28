import { execFileSync } from "node:child_process";
import fs from "node:fs";
import path from "node:path";

const root = process.cwd();
const feature = "011-taliya-commercial-agent-core-reset";
const task = "T011-102";
const reportDir = path.join(root, "specs", feature, "eval-reports");
const runtimeDir = path.join(root, "services", "taliya-agent-runtime");

const protectedPaths = [
  "app/pilates",
  "components/landing",
  "data/landing",
  "lib/landing/floating-agent.ts",
  "components/internal/SalesInboxClient.tsx",
];

const requiredFixtureFiles = [
  "services/taliya-agent-runtime/tests/test_spec011_mocked_conductor_fixtures.py",
  "services/taliya-agent-runtime/tests/test_spec011_conductor_template_plan.py",
  "services/taliya-agent-runtime/tests/test_spec011_repair_loop.py",
  "services/taliya-agent-runtime/tests/test_spec011_safe_fallback.py",
  "services/taliya-agent-runtime/tests/test_spec011_widget_runtime_adapter.py",
  "services/taliya-agent-runtime/tests/test_spec011_shadow_mode.py",
];

const fixtureMatrix = [
  {
    id: "valid_adapter",
    proof: "mocked valid conductor decision renders, persists live state, records model usage, and exposes shadow trace/projection evidence",
  },
  {
    id: "repairable_adapter",
    proof: "mocked repairable JSON decision reaches validator, sends precise errors to one repair call, then renders and persists the repaired decision",
  },
  {
    id: "repaired_trace_projection",
    proof: "mocked repaired decision builds rendered messages, runtime-state diff, Sales Inbox projection, and mandatory trace with repair metadata",
  },
  {
    id: "invalid_provider_output",
    proof: "free-form/non-JSON provider output fails with the conductor error and maps only to approved safe fallback disposition",
  },
  {
    id: "blocked_validator",
    proof: "blocked validator result skips repair and maps to handoff disposition without commercial copy",
  },
  {
    id: "failed_repair",
    proof: "failed repair maps to handoff disposition without deterministic commercial answer",
  },
  {
    id: "t011_105_missing_do_not_do_preflight",
    proof: "the four do-not-do scenarios still missing real-model evidence have local structured-JSON preflight coverage for validators, renderer, model usage, and Sales Inbox projection",
  },
];

function runCommand(id, command, args, cwd) {
  try {
    const output = execFileSync(command, args, {
      cwd,
      encoding: "utf8",
      stdio: ["ignore", "pipe", "pipe"],
      maxBuffer: 1024 * 1024 * 20,
    });
    return {
      id,
      ok: true,
      command: [command, ...args].join(" "),
      cwd: path.relative(root, cwd) || ".",
      output: output.trim(),
    };
  } catch (error) {
    return {
      id,
      ok: false,
      command: [command, ...args].join(" "),
      cwd: path.relative(root, cwd) || ".",
      exitCode: typeof error.status === "number" ? error.status : null,
      output: String(error.stdout ?? "").trim(),
      error: String(error.stderr ?? error.message ?? error).trim(),
    };
  }
}

function protectedSourceDiff() {
  const command = runCommand(
    "protected_source_diff",
    "git",
    [
      "-c",
      "safe.directory=C:/Users/lucas/agentes-landing-system",
      "diff",
      "--name-only",
      "--",
      ...protectedPaths,
    ],
    root,
  );
  const files = command.output
    .split(/\r?\n/)
    .map((line) => line.trim())
    .filter(Boolean);
  return { ...command, files };
}

function result(ok, message, details = {}) {
  return { ok: Boolean(ok), message, details };
}

function extractPassedCount(output) {
  const matches = [...String(output).matchAll(/(\d+)\s+passed/g)];
  if (!matches.length) return 0;
  return matches.reduce((total, match) => total + Number(match[1] || 0), 0);
}

const missingFixtureFiles = requiredFixtureFiles.filter(
  (relativePath) => !fs.existsSync(path.join(root, relativePath)),
);

const commands = [
  runCommand(
    "mocked_conductor_fixture_pytest",
    "python",
    [
      "-m",
      "pytest",
      "tests\\test_spec011_mocked_conductor_fixtures.py",
      "tests\\test_spec011_conductor_template_plan.py",
      "tests\\test_spec011_repair_loop.py",
      "tests\\test_spec011_safe_fallback.py",
      "-q",
    ],
    runtimeDir,
  ),
  runCommand(
    "adapter_shadow_fixture_pytest",
    "python",
    [
      "-m",
      "pytest",
      "tests\\test_spec011_widget_runtime_adapter.py",
      "tests\\test_spec011_shadow_mode.py",
      "-q",
    ],
    runtimeDir,
  ),
  runCommand(
    "mocked_conductor_ruff",
    "python",
    [
      "-m",
      "ruff",
      "check",
      "app/core/taliya_commercial/conductor.py",
      "tests/test_spec011_mocked_conductor_fixtures.py",
      "tests/test_spec011_conductor_template_plan.py",
    ],
    runtimeDir,
  ),
  runCommand("static_audit", "node", ["scripts\\eval-agent-runtime-spec011-static-audit.mjs"], root),
  runCommand("runner_quarantine", "node", ["scripts\\eval-agent-runtime-spec011-runner-quarantine.mjs"], root),
  runCommand("public_fallback_quarantine", "node", ["scripts\\eval-agent-runtime-spec011-public-fallback-quarantine.mjs"], root),
];

const protectedDiff = protectedSourceDiff();
const fixturePassedCount = extractPassedCount(
  commands.find((item) => item.id === "mocked_conductor_fixture_pytest")?.output,
);
const adapterShadowPassedCount = extractPassedCount(
  commands.find((item) => item.id === "adapter_shadow_fixture_pytest")?.output,
);

const results = [
  result(
    missingFixtureFiles.length === 0,
    "required mocked conductor fixture files exist",
    { missingFixtureFiles, requiredFixtureFiles },
  ),
  result(
    commands.find((item) => item.id === "mocked_conductor_fixture_pytest")?.ok === true &&
      fixturePassedCount >= 24,
    "mocked conductor fixture matrix passes",
    {
      passedCount: fixturePassedCount,
      command: commands.find((item) => item.id === "mocked_conductor_fixture_pytest"),
      fixtureMatrix,
    },
  ),
  result(
    commands.find((item) => item.id === "adapter_shadow_fixture_pytest")?.ok === true &&
      adapterShadowPassedCount >= 8,
    "adapter and shadow mocked fixture boundaries pass",
    {
      passedCount: adapterShadowPassedCount,
      command: commands.find((item) => item.id === "adapter_shadow_fixture_pytest"),
    },
  ),
  result(
    commands.find((item) => item.id === "mocked_conductor_ruff")?.ok === true,
    "mocked conductor fixture code passes ruff",
    { command: commands.find((item) => item.id === "mocked_conductor_ruff") },
  ),
  result(
    commands
      .filter((item) => [
        "static_audit",
        "runner_quarantine",
        "public_fallback_quarantine",
      ].includes(item.id))
      .every((item) => item.ok),
    "LLM-first static, runner quarantine, and public fallback guards pass",
    {
      commands: commands.filter((item) => [
        "static_audit",
        "runner_quarantine",
        "public_fallback_quarantine",
      ].includes(item.id)),
    },
  ),
  result(
    protectedDiff.ok && protectedDiff.files.length === 0,
    "mocked conductor gate produced no protected /pilates, landing visual, floating-agent, or Sales Inbox UI source diff",
    { protectedDiff, protectedPaths },
  ),
];

fs.mkdirSync(reportDir, { recursive: true });
const summary = {
  total: results.length,
  passed: results.filter((item) => item.ok).length,
  failed: results.filter((item) => !item.ok).length,
};
const report = {
  runId: `agent-runtime-spec011-mocked-conductor-${Date.now()}`,
  feature,
  task,
  createdAt: new Date().toISOString(),
  summary,
  releaseGate: summary.failed === 0 ? "pass" : "fail",
  fixtureMatrix,
  commands,
  protectedDiff,
  results,
};

const jsonPath = path.join(reportDir, "agent-runtime-spec011-mocked-conductor.json");
const mdPath = path.join(reportDir, "agent-runtime-spec011-mocked-conductor.md");
fs.writeFileSync(jsonPath, `${JSON.stringify(report, null, 2)}\n`);
fs.writeFileSync(
  mdPath,
  [
    "# agent-runtime-spec011-mocked-conductor",
    "",
    `Generated at: ${report.createdAt}`,
    `Release gate: ${report.releaseGate}`,
    `Passed: ${summary.passed}/${summary.total}`,
    "",
    "## Fixture Matrix",
    "",
    ...fixtureMatrix.map((item) => `- ${item.id}: ${item.proof}`),
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
  console.error(`agent-runtime-spec011-mocked-conductor: ${summary.failed} failure(s). Report: ${jsonPath}`);
  process.exitCode = 1;
} else {
  console.log(`agent-runtime-spec011-mocked-conductor: ${summary.passed}/${summary.total} passed. Report: ${jsonPath}`);
}
