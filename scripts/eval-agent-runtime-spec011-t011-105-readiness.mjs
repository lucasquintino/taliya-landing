import { execFileSync } from "node:child_process";
import fs from "node:fs";
import path from "node:path";
import { buildSpec011T011105SourceFingerprint } from "./spec011-t011-105-source-fingerprint.mjs";

const root = process.cwd();
const feature = "011-taliya-commercial-agent-core-reset";
const task = "T011-105";
const reportDir = path.join(root, "specs", feature, "eval-reports");

const protectedPaths = [
  "app/pilates",
  "components/landing",
  "data/landing",
  "lib/landing/floating-agent.ts",
  "components/internal/SalesInboxClient.tsx",
];

const expectedGoldenMissing = ["final-pain-first", "step3g-long-conversation"];
const expectedDoNotDoMissing = [
  "do-not-do-client-studio-whatsapp-capture",
  "do-not-do-date-vip-discount",
  "do-not-do-early-phone-capture",
  "do-not-do-wrong-student-language",
];

const goldenReadinessName = "agent-runtime-spec011-t011-105-golden-readiness";
const doNotDoReadinessName = "agent-runtime-spec011-t011-105-do-not-do-readiness";
const knownValidatorRecoveryName = "agent-runtime-spec011-known-validator-recovery";
const safetyAuditName = "agent-runtime-spec011-t011-105-safety-audit";
const unitContractGateName = "agent-runtime-spec011-unit-contract";
const painDryRunName = "agent-runtime-spec011-t011-105-pain-first-plan";
const longDryRunName = "agent-runtime-spec011-t011-105-long-conversation-plan";
const doNotDoDryRunName = "agent-runtime-spec011-t011-105-do-not-do-missing-plan";
const readinessName = "agent-runtime-spec011-t011-105-readiness";

function runCommand(id, command, args, options = {}) {
  const allowedExitCodes = options.allowedExitCodes ?? [0];
  try {
    const output = execFileSync(command, args, {
      cwd: root,
      encoding: "utf8",
      env: { ...process.env, ...(options.env ?? {}) },
      stdio: ["ignore", "pipe", "pipe"],
      maxBuffer: 1024 * 1024 * 30,
    });
    return {
      id,
      ok: true,
      allowed: true,
      exitCode: 0,
      command: [command, ...args].join(" "),
      output: output.trim(),
    };
  } catch (error) {
    const exitCode = typeof error.status === "number" ? error.status : null;
    const allowed = allowedExitCodes.includes(exitCode);
    return {
      id,
      ok: false,
      allowed,
      exitCode,
      command: [command, ...args].join(" "),
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
  );
  return {
    ...command,
    files: command.output
      .split(/\r?\n/)
      .map((line) => line.trim())
      .filter(Boolean),
  };
}

function readJson(relativePath) {
  return JSON.parse(fs.readFileSync(path.join(root, relativePath), "utf8"));
}

function reportPath(name) {
  return path.join("specs", feature, "eval-reports", `${name}.json`);
}

function dryRunReportPath(name) {
  return path.join("specs", feature, "eval-reports", `${name}-dry-run.json`);
}

function failedResultIds(report) {
  return (report.results ?? [])
    .filter((result) => result.status !== "PASS")
    .map((result) => result.id)
    .sort();
}

function sameList(left, right) {
  return (
    left.length === right.length &&
    left.every((item, index) => item === right[index])
  );
}

function result(ok, message, details = {}) {
  return { ok: Boolean(ok), message, details };
}

const commands = [
  runCommand(
    "node_check_golden_do_not_do",
    "node",
    ["--check", "scripts\\eval-agent-runtime-spec011-golden-do-not-do.mjs"],
  ),
  runCommand(
    "node_check_paid_batch_runner",
    "node",
    ["--check", "scripts\\eval-agent-runtime-spec011-t011-105-paid-batch.mjs"],
  ),
  runCommand(
    "node_check_t011_105_safety_audit",
    "node",
    ["--check", "scripts\\eval-agent-runtime-spec011-t011-105-safety-audit.mjs"],
  ),
  runCommand(
    "node_check_known_validator_recovery",
    "node",
    ["--check", "scripts\\eval-agent-runtime-spec011-known-validator-recovery.mjs"],
  ),
  runCommand(
    "fixture_inventory_gate",
    "node",
    ["scripts\\eval-agent-runtime-spec011-fixture-inventory.mjs"],
  ),
  runCommand(
    "known_validator_recovery_gate",
    "node",
    ["scripts\\eval-agent-runtime-spec011-known-validator-recovery.mjs"],
  ),
  runCommand(
    "t011_105_safety_audit",
    "node",
    ["scripts\\eval-agent-runtime-spec011-t011-105-safety-audit.mjs"],
  ),
  runCommand(
    "unit_contract_gate",
    "node",
    ["scripts\\eval-agent-runtime-spec011-unit-contract.mjs"],
  ),
  runCommand(
    "action_coverage_contract_gate",
    "python",
    [
      "-m",
      "pytest",
      "services\\taliya-agent-runtime\\tests\\test_spec011_action_coverage_contract.py",
      "-q",
    ],
  ),
  runCommand(
    "paid_batch_refuses_without_approval",
    "node",
    ["scripts\\eval-agent-runtime-spec011-t011-105-paid-batch.mjs"],
    { allowedExitCodes: [1] },
  ),
  runCommand(
    "paid_batch_refuses_wrong_budget",
    "node",
    [
      "scripts\\eval-agent-runtime-spec011-t011-105-paid-batch.mjs",
      "--approval-token",
      "T011-105-US0.36",
      "--approved-budget-usd",
      "0.35",
    ],
    { allowedExitCodes: [1] },
  ),
  runCommand(
    "paid_batch_refuses_env_only_approval",
    "node",
    ["scripts\\eval-agent-runtime-spec011-t011-105-paid-batch.mjs"],
    {
      allowedExitCodes: [1],
      env: {
        TALIYA_SPEC011_T011_105_APPROVAL_TOKEN: "T011-105-US0.36",
        TALIYA_SPEC011_T011_105_APPROVED_BUDGET_USD: "0.36",
      },
    },
  ),
  runCommand(
    "paid_batch_refuses_continue_on_failure",
    "node",
    [
      "scripts\\eval-agent-runtime-spec011-t011-105-paid-batch.mjs",
      "--approval-token",
      "T011-105-US0.36",
      "--approved-budget-usd",
      "0.36",
      "--continue-on-failure",
    ],
    { allowedExitCodes: [1] },
  ),
  runCommand(
    "focused_t011_105_preflight_pytest",
    "python",
    [
      "-m",
      "pytest",
      "services\\taliya-agent-runtime\\tests\\test_spec011_mocked_conductor_fixtures.py::test_t011_105_missing_do_not_do_cases_have_local_preflight",
      "services\\taliya-agent-runtime\\tests\\test_spec011_widget_runtime_adapter.py::test_runtime_adapter_repairs_pain_first_product_route_without_paid_repair",
      "services\\taliya-agent-runtime\\tests\\test_spec011_widget_runtime_adapter.py::test_runtime_adapter_long_conversation_preflight_covers_last_real_gate_failures",
      "-q",
    ],
  ),
  runCommand(
    "mocked_conductor_gate",
    "node",
    ["scripts\\eval-agent-runtime-spec011-mocked-conductor.mjs"],
  ),
  runCommand(
    "golden_existing_evidence",
    "node",
    [
      "scripts\\eval-agent-runtime-spec011-golden-do-not-do.mjs",
      "--fixture",
      "scripts\\fixtures\\agent-runtime\\spec-011-golden-transcripts.json",
      "--report",
      "specs\\011-taliya-commercial-agent-core-reset\\eval-reports\\agent-runtime-spec011-full-required-final-matrix-budgeted-1.json",
      "--report",
      "specs\\011-taliya-commercial-agent-core-reset\\eval-reports\\agent-runtime-spec011-full-required-remaining-budgeted-1.json",
      "--report",
      "specs\\011-taliya-commercial-agent-core-reset\\eval-reports\\agent-runtime-spec011-golden-demo-direct-fixed-1.json",
      "--report",
      "specs\\011-taliya-commercial-agent-core-reset\\eval-reports\\agent-runtime-spec011-golden-long-conversation-16.json",
      "--name",
      goldenReadinessName,
    ],
    { allowedExitCodes: [0, 1] },
  ),
  runCommand(
    "do_not_do_existing_evidence",
    "node",
    [
      "scripts\\eval-agent-runtime-spec011-golden-do-not-do.mjs",
      "--fixture",
      "scripts\\fixtures\\agent-runtime\\spec-011-do-not-do-runtime.json",
      "--report",
      "specs\\011-taliya-commercial-agent-core-reset\\eval-reports\\agent-runtime-spec011-full-required-final-matrix-budgeted-1.json",
      "--report",
      "specs\\011-taliya-commercial-agent-core-reset\\eval-reports\\agent-runtime-spec011-full-required-remaining-budgeted-1.json",
      "--report",
      "specs\\011-taliya-commercial-agent-core-reset\\eval-reports\\agent-runtime-spec011-full-required-product-delta-budgeted-1.json",
      "--report",
      "specs\\011-taliya-commercial-agent-core-reset\\eval-reports\\agent-runtime-spec011-full-required-product-delta-integration-fixed-1.json",
      "--report",
      "specs\\011-taliya-commercial-agent-core-reset\\eval-reports\\agent-runtime-spec011-full-required-product-delta-remaining-budgeted-1.json",
      "--report",
      "specs\\011-taliya-commercial-agent-core-reset\\eval-reports\\agent-runtime-spec011-full-required-product-delta-diagnostic-refusal-fixed-1.json",
      "--report",
      "specs\\011-taliya-commercial-agent-core-reset\\eval-reports\\agent-runtime-spec011-p0-real-model.json",
      "--static-fixture",
      "scripts\\fixtures\\agent-runtime\\spec-011-do-not-do-runtime.json",
      "--static-report",
      "specs\\011-taliya-commercial-agent-core-reset\\eval-reports\\agent-runtime-spec011-static-audit.json",
      "--name",
      doNotDoReadinessName,
    ],
    { allowedExitCodes: [0, 1] },
  ),
  runCommand(
    "pain_first_paid_plan_dry_run",
    "python",
    [
      "scripts\\eval-agent-runtime-spec011.py",
      "--fixture",
      "scripts\\fixtures\\agent-runtime\\spec-011-golden-transcripts.json",
      "--scenario-id",
      "final-pain-first",
      "--max-scenarios",
      "1",
      "--max-model-calls",
      "1",
      "--max-cost-usd",
      "0.03",
      "--dry-run",
      "--report-name",
      painDryRunName,
    ],
  ),
  runCommand(
    "long_conversation_paid_plan_dry_run",
    "python",
    [
      "scripts\\eval-agent-runtime-spec011.py",
      "--fixture",
      "scripts\\fixtures\\agent-runtime\\spec-011-golden-transcripts.json",
      "--scenario-id",
      "step3g-long-conversation",
      "--max-scenarios",
      "1",
      "--max-model-calls",
      "14",
      "--max-cost-usd",
      "0.25",
      "--dry-run",
      "--report-name",
      longDryRunName,
    ],
  ),
  runCommand(
    "do_not_do_paid_plan_dry_run",
    "python",
    [
      "scripts\\eval-agent-runtime-spec011.py",
      "--fixture",
      "scripts\\fixtures\\agent-runtime\\spec-011-do-not-do-runtime.json",
      "--scenario-id",
      "do-not-do-early-phone-capture",
      "--scenario-id",
      "do-not-do-date-vip-discount",
      "--scenario-id",
      "do-not-do-client-studio-whatsapp-capture",
      "--scenario-id",
      "do-not-do-wrong-student-language",
      "--max-scenarios",
      "4",
      "--max-model-calls",
      "4",
      "--max-cost-usd",
      "0.08",
      "--dry-run",
      "--report-name",
      doNotDoDryRunName,
    ],
  ),
];

const protectedDiff = protectedSourceDiff();
const knownValidatorRecoveryReport = readJson(reportPath(knownValidatorRecoveryName));
const safetyAuditReport = readJson(reportPath(safetyAuditName));
const unitContractGateReport = readJson(reportPath(unitContractGateName));
const goldenReport = readJson(reportPath(goldenReadinessName));
const doNotDoReport = readJson(reportPath(doNotDoReadinessName));
const painDryRun = readJson(dryRunReportPath(painDryRunName));
const longDryRun = readJson(dryRunReportPath(longDryRunName));
const doNotDoDryRun = readJson(dryRunReportPath(doNotDoDryRunName));
const goldenFailures = failedResultIds(goldenReport);
const doNotDoFailures = failedResultIds(doNotDoReport);
const totalCapUsd =
  Number(painDryRun.maxCostUsd ?? 0) +
  Number(longDryRun.maxCostUsd ?? 0) + Number(doNotDoDryRun.maxCostUsd ?? 0);
const totalEstimatedModelCalls =
  Number(painDryRun.estimatedModelCalls ?? 0) +
  Number(longDryRun.estimatedModelCalls ?? 0) +
  Number(doNotDoDryRun.estimatedModelCalls ?? 0);
const paidBatchRefusalCommands = commands.filter((command) =>
  command.id.startsWith("paid_batch_refuses_"),
);
const sourceFingerprint = buildSpec011T011105SourceFingerprint(root);

const results = [
  result(
    sourceFingerprint.algorithm === "sha256" && sourceFingerprint.fileCount > 0,
    "readiness records a source fingerprint for paid evidence freshness",
    { sourceFingerprint },
  ),
  result(
    commands.every((command) => command.ok || command.allowed),
    "all readiness commands completed with expected exit status",
    { commands },
  ),
  result(
    paidBatchRefusalCommands.length === 4 &&
      paidBatchRefusalCommands.every(
        (command) =>
          command.exitCode === 1 &&
          command.error.includes("No paid commands were started."),
      ),
    "paid batch runner refuses missing or wrong approval before any paid command can start",
    { paidBatchRefusalCommands },
  ),
  result(
    knownValidatorRecoveryReport.releaseGate === "pass" &&
      knownValidatorRecoveryReport.summary?.total === 9 &&
      knownValidatorRecoveryReport.summary?.passed === 9 &&
      knownValidatorRecoveryReport.summary?.failed === 0,
    "known critical validator errors have no-500 recovery proof before paid rerun",
    {
      summary: knownValidatorRecoveryReport.summary,
      releaseGate: knownValidatorRecoveryReport.releaseGate,
      report: reportPath(knownValidatorRecoveryName),
    },
  ),
  result(
    safetyAuditReport.releaseGate === "pass" &&
      safetyAuditReport.summary?.total === 12 &&
      safetyAuditReport.summary?.passed === 12 &&
      safetyAuditReport.summary?.failed === 0,
    "T011-105 paid-batch safety audit passed all no-cost guard checks",
    {
      summary: safetyAuditReport.summary,
      releaseGate: safetyAuditReport.releaseGate,
      report: reportPath(safetyAuditName),
    },
  ),
  result(
    unitContractGateReport.releaseGate === "pass" &&
      unitContractGateReport.summary?.total === 7 &&
      unitContractGateReport.summary?.passed === 7 &&
      unitContractGateReport.summary?.failed === 0,
    "full local unit/contract gate passed before paid evidence can be accepted",
    {
      summary: unitContractGateReport.summary,
      releaseGate: unitContractGateReport.releaseGate,
      report: reportPath(unitContractGateName),
    },
  ),
  result(
    goldenReport.summary?.total === 9 &&
      goldenReport.summary?.passed === 7 &&
      goldenReport.summary?.failed === 2 &&
      sameList(goldenFailures, expectedGoldenMissing),
    "golden existing evidence has exactly the expected paid-evidence gaps",
    {
      summary: goldenReport.summary,
      failures: goldenFailures,
      expectedGoldenMissing,
      report: reportPath(goldenReadinessName),
    },
  ),
  result(
    doNotDoReport.summary?.total === 8 &&
      doNotDoReport.summary?.passed === 4 &&
      doNotDoReport.summary?.failed === 4 &&
      sameList(doNotDoFailures, expectedDoNotDoMissing),
    "do-not-do existing evidence has exactly the expected four paid-evidence gaps",
    {
      summary: doNotDoReport.summary,
      failures: doNotDoFailures,
      expectedDoNotDoMissing,
      report: reportPath(doNotDoReadinessName),
    },
  ),
  result(
    painDryRun.dryRun === true &&
      painDryRun.selectedScenarioCount === 1 &&
      painDryRun.estimatedModelCalls === 1 &&
      painDryRun.maxModelCalls === 1 &&
      Number(painDryRun.maxCostUsd) === 0.03 &&
      sameList(painDryRun.scenarioIds ?? [], ["final-pain-first"]),
    "pain-first paid rerun plan is capped and targets only the missing golden pain-first scenario",
    { dryRun: painDryRun, report: dryRunReportPath(painDryRunName) },
  ),
  result(
    longDryRun.dryRun === true &&
      longDryRun.selectedScenarioCount === 1 &&
      longDryRun.estimatedModelCalls === 14 &&
      longDryRun.maxModelCalls === 14 &&
      Number(longDryRun.maxCostUsd) === 0.25 &&
      sameList(longDryRun.scenarioIds ?? [], ["step3g-long-conversation"]),
    "long-conversation paid rerun plan is capped and targets only the missing golden scenario",
    { dryRun: longDryRun, report: dryRunReportPath(longDryRunName) },
  ),
  result(
    doNotDoDryRun.dryRun === true &&
      doNotDoDryRun.selectedScenarioCount === 4 &&
      doNotDoDryRun.estimatedModelCalls === 4 &&
      doNotDoDryRun.maxModelCalls === 4 &&
      Number(doNotDoDryRun.maxCostUsd) === 0.08 &&
      sameList([...(doNotDoDryRun.scenarioIds ?? [])].sort(), expectedDoNotDoMissing),
    "do-not-do paid rerun plan is capped and targets only the missing forbidden-behavior scenarios",
    { dryRun: doNotDoDryRun, report: dryRunReportPath(doNotDoDryRunName) },
  ),
  result(
    Number(totalCapUsd.toFixed(2)) === 0.36 && totalEstimatedModelCalls === 19,
    "combined paid batch stays within the approved-request ceiling",
    { totalCapUsd: Number(totalCapUsd.toFixed(2)), totalEstimatedModelCalls },
  ),
  result(
    protectedDiff.ok && protectedDiff.files.length === 0,
    "readiness gate produced no protected /pilates, landing visual, floating-agent, or Sales Inbox UI source diff",
    { protectedDiff },
  ),
];

const failedResults = results.filter((item) => !item.ok);
const releaseGate = failedResults.length === 0 ? "ready_for_paid_batch" : "fail";
const report = {
  feature,
  task,
  name: readinessName,
  releaseGate,
  paidOpenAiSpend: 0,
  paidBatchRequiresExplicitUserApproval: true,
  sourceFingerprint,
  expectedPaidBatch: {
    maxCostUsd: Number(totalCapUsd.toFixed(2)),
    maxModelCalls: totalEstimatedModelCalls,
    commands: [
      "python scripts\\eval-agent-runtime-spec011.py --fixture scripts\\fixtures\\agent-runtime\\spec-011-golden-transcripts.json --scenario-id final-pain-first --max-scenarios 1 --max-model-calls 1 --max-cost-usd 0.03 --report-name agent-runtime-spec011-golden-pain-first-1",
      "python scripts\\eval-agent-runtime-spec011.py --fixture scripts\\fixtures\\agent-runtime\\spec-011-golden-transcripts.json --scenario-id step3g-long-conversation --max-scenarios 1 --max-model-calls 14 --max-cost-usd 0.25 --report-name agent-runtime-spec011-golden-long-conversation-17",
      "python scripts\\eval-agent-runtime-spec011.py --fixture scripts\\fixtures\\agent-runtime\\spec-011-do-not-do-runtime.json --scenario-id do-not-do-early-phone-capture --scenario-id do-not-do-date-vip-discount --scenario-id do-not-do-client-studio-whatsapp-capture --scenario-id do-not-do-wrong-student-language --max-scenarios 4 --max-model-calls 4 --max-cost-usd 0.08 --report-name agent-runtime-spec011-do-not-do-missing-1",
    ],
  },
  summary: {
    total: results.length,
    passed: results.length - failedResults.length,
    failed: failedResults.length,
    goldenExistingEvidence: goldenReport.summary,
    doNotDoExistingEvidence: doNotDoReport.summary,
    safetyAudit: safetyAuditReport.summary,
    unitContractGate: unitContractGateReport.summary,
  },
  results,
};

fs.mkdirSync(reportDir, { recursive: true });
const jsonPath = path.join(reportDir, `${readinessName}.json`);
fs.writeFileSync(jsonPath, `${JSON.stringify(report, null, 2)}\n`);

const lines = [
  `# ${readinessName}`,
  "",
  `Release gate: ${releaseGate}`,
  "Paid OpenAI spend: US$0",
  `Paid batch cap: US$${report.expectedPaidBatch.maxCostUsd}`,
  `Paid batch model-call cap: ${report.expectedPaidBatch.maxModelCalls}`,
  "",
  "## Expected Paid Batch",
  "",
  ...report.expectedPaidBatch.commands.map((command) => `- \`${command}\``),
  "",
];
for (const item of results) {
  lines.push(`## ${item.ok ? "PASS" : "FAIL"} ${item.message}`, "");
  lines.push("```json");
  lines.push(JSON.stringify(item.details, null, 2));
  lines.push("```", "");
}
const mdPath = path.join(reportDir, `${readinessName}.md`);
fs.writeFileSync(mdPath, `${lines.join("\n").trim()}\n`);

console.log(
  `agent-runtime-spec011-t011-105-readiness: ${report.summary.passed}/${report.summary.total} passed`,
);
console.log(`Release gate: ${releaseGate}`);
console.log(`Report JSON: ${jsonPath}`);
console.log(`Report MD: ${mdPath}`);

if (releaseGate === "fail") {
  process.exitCode = 1;
}
