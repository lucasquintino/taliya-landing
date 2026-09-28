import { execFileSync } from "node:child_process";
import fs from "node:fs";
import path from "node:path";

const root = process.cwd();
const feature = "011-taliya-commercial-agent-core-reset";
const task = "T011-101";
const reportDir = path.join(root, "specs", feature, "eval-reports");
const runtimeDir = path.join(root, "services", "taliya-agent-runtime");

const requiredSpec011TestFiles = [
  "services/taliya-agent-runtime/tests/test_spec011_core_schemas.py",
  "services/taliya-agent-runtime/tests/test_spec011_contract_schema_map.py",
  "services/taliya-agent-runtime/tests/test_spec011_context_builder.py",
  "services/taliya-agent-runtime/tests/test_spec011_product_knowledge_context.py",
  "services/taliya-agent-runtime/tests/test_spec011_conductor_boundary.py",
  "services/taliya-agent-runtime/tests/test_spec011_conductor_usage.py",
  "services/taliya-agent-runtime/tests/test_spec011_validators_core.py",
  "services/taliya-agent-runtime/tests/test_spec011_validators_diagnostic.py",
  "services/taliya-agent-runtime/tests/test_spec011_validators_product_claims.py",
  "services/taliya-agent-runtime/tests/test_spec011_repair_loop.py",
  "services/taliya-agent-runtime/tests/test_spec011_failed_path_guards.py",
  "services/taliya-agent-runtime/tests/test_spec011_renderer_validated_plan.py",
  "services/taliya-agent-runtime/tests/test_spec011_renderer_no_semantic_defaults.py",
  "services/taliya-agent-runtime/tests/test_spec011_trace_store.py",
  "services/taliya-agent-runtime/tests/test_spec011_trace_export.py",
  "services/taliya-agent-runtime/tests/test_spec011_runtime_state_diff.py",
  "services/taliya-agent-runtime/tests/test_spec011_sales_inbox_projection_builder.py",
  "services/taliya-agent-runtime/tests/test_spec011_feedback_loop_prevention.py",
  "services/taliya-agent-runtime/tests/test_spec011_turn_gate_idempotency.py",
  "services/taliya-agent-runtime/tests/test_spec011_turn_gate_lock.py",
  "services/taliya-agent-runtime/tests/test_spec011_turn_gate_outbox.py",
  "services/taliya-agent-runtime/tests/test_spec011_turn_gate_delivery_regressions.py",
  "services/taliya-agent-runtime/tests/test_spec011_widget_runtime_adapter.py",
  "services/taliya-agent-runtime/tests/test_spec011_shadow_mode.py",
  "services/taliya-agent-runtime/tests/test_agent_runs_api.py",
  "services/taliya-agent-runtime/tests/test_settings.py",
];

const protectedPaths = [
  "app/pilates",
  "components/landing",
  "data/landing",
  "lib/landing/floating-agent.ts",
  "components/internal/SalesInboxClient.tsx",
];

function runCommand(id, command, args, cwd) {
  const executable = process.platform === "win32" && command === "npx" ? "npx.cmd" : command;
  try {
    const output = execFileSync(executable, args, {
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
  const files = command.output.split(/\r?\n/).map((line) => line.trim()).filter(Boolean);
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

const missingRequiredSpec011Tests = requiredSpec011TestFiles.filter(
  (relativePath) => !fs.existsSync(path.join(root, relativePath)),
);

const commands = [
  runCommand("full_runtime_pytest", "python", ["-m", "pytest", "tests", "-q"], runtimeDir),
  runCommand(
    "focused_api_adapter_shadow_pytest",
    "python",
    [
      "-m",
      "pytest",
      "tests\\test_settings.py",
      "tests\\test_agent_runs_api.py",
      "tests\\test_spec011_widget_runtime_adapter.py",
      "tests\\test_spec011_shadow_mode.py",
      "-q",
    ],
    runtimeDir,
  ),
  runCommand(
    "widget_whatsapp_adapter_node",
    "node",
    ["--test", "scripts\\eval-agent-runtime-spec011-widget-adapter.mjs"],
    root,
  ),
  runCommand("typescript_contract", "node", ["node_modules\\typescript\\bin\\tsc", "--noEmit", "--pretty", "false"], root),
  runCommand("static_audit", "node", ["scripts\\eval-agent-runtime-spec011-static-audit.mjs"], root),
  runCommand("runner_quarantine", "node", ["scripts\\eval-agent-runtime-spec011-runner-quarantine.mjs"], root),
  runCommand("public_fallback_quarantine", "node", ["scripts\\eval-agent-runtime-spec011-public-fallback-quarantine.mjs"], root),
  runCommand("rollback_contract", "node", ["scripts\\eval-agent-runtime-spec011-rollback.mjs"], root),
];
const protectedDiff = protectedSourceDiff();

const fullRuntimePassedCount = extractPassedCount(commands.find((item) => item.id === "full_runtime_pytest")?.output);
const focusedPassedCount = extractPassedCount(commands.find((item) => item.id === "focused_api_adapter_shadow_pytest")?.output);

const results = [
  result(
    missingRequiredSpec011Tests.length === 0,
    "required Spec 011 unit and contract test files exist",
    { missingRequiredSpec011Tests, requiredSpec011TestFiles },
  ),
  result(
    commands.find((item) => item.id === "full_runtime_pytest")?.ok === true &&
      fullRuntimePassedCount >= 500,
    "full runtime pytest suite passes",
    {
      passedCount: fullRuntimePassedCount,
      command: commands.find((item) => item.id === "full_runtime_pytest"),
    },
  ),
  result(
    commands.find((item) => item.id === "focused_api_adapter_shadow_pytest")?.ok === true &&
      focusedPassedCount >= 20,
    "focused API/settings/widget/shadow contract suite passes",
    {
      passedCount: focusedPassedCount,
      command: commands.find((item) => item.id === "focused_api_adapter_shadow_pytest"),
    },
  ),
  result(
    commands.find((item) => item.id === "widget_whatsapp_adapter_node")?.ok === true,
    "widget and Taliya-owned WhatsApp Node adapter contract tests pass",
    { command: commands.find((item) => item.id === "widget_whatsapp_adapter_node") },
  ),
  result(
    commands.find((item) => item.id === "typescript_contract")?.ok === true,
    "TypeScript contract check passes",
    { command: commands.find((item) => item.id === "typescript_contract") },
  ),
  result(
    commands
      .filter((item) => [
        "static_audit",
        "runner_quarantine",
        "public_fallback_quarantine",
        "rollback_contract",
      ].includes(item.id))
      .every((item) => item.ok),
    "static, runner, public fallback, and rollback contract guards pass",
    {
      commands: commands.filter((item) => [
        "static_audit",
        "runner_quarantine",
        "public_fallback_quarantine",
        "rollback_contract",
      ].includes(item.id)),
    },
  ),
  result(
    protectedDiff.ok && protectedDiff.files.length === 0,
    "unit/contract gate produced no protected /pilates, landing visual, floating-agent, or Sales Inbox UI source diff",
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
  runId: `agent-runtime-spec011-unit-contract-${Date.now()}`,
  feature,
  task,
  createdAt: new Date().toISOString(),
  summary,
  releaseGate: summary.failed === 0 ? "pass" : "fail",
  commands,
  protectedDiff,
  results,
};

const jsonPath = path.join(reportDir, "agent-runtime-spec011-unit-contract.json");
const mdPath = path.join(reportDir, "agent-runtime-spec011-unit-contract.md");
fs.writeFileSync(jsonPath, `${JSON.stringify(report, null, 2)}\n`);
fs.writeFileSync(
  mdPath,
  [
    "# agent-runtime-spec011-unit-contract",
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
  console.error(`agent-runtime-spec011-unit-contract: ${summary.failed} failure(s). Report: ${jsonPath}`);
  process.exitCode = 1;
} else {
  console.log(`agent-runtime-spec011-unit-contract: ${summary.passed}/${summary.total} passed. Report: ${jsonPath}`);
}
