import fs from "node:fs";
import path from "node:path";

const root = process.cwd();
const feature = "011-taliya-commercial-agent-core-reset";
const reportDir = path.join(root, "specs", feature, "eval-reports");
const reportName = "agent-runtime-spec011-t011-105-safety-audit";

const files = {
  paidBatch: path.join(root, "scripts", "eval-agent-runtime-spec011-t011-105-paid-batch.mjs"),
  closure: path.join(root, "scripts", "eval-agent-runtime-spec011-t011-105-closure.mjs"),
  goldenDoNotDo: path.join(root, "scripts", "eval-agent-runtime-spec011-golden-do-not-do.mjs"),
  knownValidatorRecovery: path.join(root, "scripts", "eval-agent-runtime-spec011-known-validator-recovery.mjs"),
  readiness: path.join(root, "scripts", "eval-agent-runtime-spec011-t011-105-readiness.mjs"),
};

function read(filePath) {
  return fs.readFileSync(filePath, "utf8");
}

function result(ok, message, details = {}) {
  return { ok: Boolean(ok), message, details };
}

function indexOf(text, pattern) {
  return text.indexOf(pattern);
}

function includesAll(text, patterns) {
  return patterns.every((pattern) => text.includes(pattern));
}

function countMatches(text, pattern) {
  return [...text.matchAll(pattern)].length;
}

const paidBatch = read(files.paidBatch);
const closure = read(files.closure);
const goldenDoNotDo = read(files.goldenDoNotDo);
const knownValidatorRecovery = read(files.knownValidatorRecovery);
const readiness = read(files.readiness);

const approvalIndex = indexOf(paidBatch, "assertPaidApproval(args);");
const firstCommandIndex = indexOf(paidBatch, "runCommand(\"readiness_gate_before_paid_batch\"");
const firstPaidCommandIndex = indexOf(paidBatch, "runCommand(\"paid_pain_first\"");

const results = [
  result(
    includesAll(paidBatch, [
      "const approvalToken = \"T011-105-US0.36\";",
      "const expectedBudgetUsd = 0.36;",
      "assertPaidApproval(args);",
      "args.approvalToken !== approvalToken",
      "budget !== expectedBudgetUsd",
      "No paid commands were started.",
    ]),
    "paid batch requires exact CLI approval token and budget before paid work",
    {
      approvalIndex,
      firstCommandIndex,
      firstPaidCommandIndex,
      approvalBeforeCommands:
        approvalIndex >= 0 &&
        firstCommandIndex >= 0 &&
        firstPaidCommandIndex >= 0 &&
        approvalIndex < firstCommandIndex &&
        approvalIndex < firstPaidCommandIndex,
    },
  ),
  result(
    approvalIndex >= 0 &&
      firstCommandIndex >= 0 &&
      firstPaidCommandIndex >= 0 &&
      approvalIndex < firstCommandIndex &&
      approvalIndex < firstPaidCommandIndex &&
      !paidBatch.includes("process.env"),
    "paid batch cannot use environment-only approval and validates before any command starts",
    {
      approvalIndex,
      firstCommandIndex,
      firstPaidCommandIndex,
      processEnvHits: countMatches(paidBatch, /process\.env/g),
    },
  ),
  result(
    includesAll(paidBatch, [
      "Refusing --continue-on-failure for the T011-105 paid batch.",
      "fail_stopped_after_pain_first",
      "fail_stopped_after_long_conversation",
      "fail_stopped_after_do_not_do_missing",
    ]),
    "paid batch refuses continue-on-failure and has explicit stop gates after each paid block",
    {
      paidCommandIds: [
        "paid_pain_first",
        "paid_long_conversation",
        "paid_do_not_do_missing",
      ].filter((id) => paidBatch.includes(`runCommand(\"${id}\"`)),
    },
  ),
  result(
    countMatches(paidBatch, /runCommand\("paid_/g) === 3 &&
      includesAll(paidBatch, [
        "--max-model-calls",
        "1",
        "0.03",
        "14",
        "0.25",
        "4",
        "0.08",
      ]),
    "paid batch has exactly three paid commands with per-scenario caps",
    {
      paidCommandCount: countMatches(paidBatch, /runCommand\("paid_/g),
      requiredScenarioIds: [
        "final-pain-first",
        "step3g-long-conversation",
        "do-not-do-early-phone-capture",
        "do-not-do-date-vip-discount",
        "do-not-do-client-studio-whatsapp-capture",
        "do-not-do-wrong-student-language",
      ].filter((id) => paidBatch.includes(id)),
    },
  ),
  result(
    includesAll(paidBatch, [
      "appendFreshnessCheck",
      "fresh_paid_pain_first_report",
      "fresh_paid_long_conversation_report",
      "fresh_golden_aggregation_report",
      "fresh_paid_do_not_do_report",
      "fresh_do_not_do_aggregation_report",
      "Report was missing or stale relative to this approved paid batch.",
    ]),
    "paid batch rejects stale scenario and aggregation reports during the batch",
    {
      freshnessCheckCount: countMatches(paidBatch, /appendFreshnessCheck/g),
    },
  ),
  result(
    includesAll(paidBatch, [
      "appendSourceStabilityCheck",
      "source_stable_after_readiness",
      "source_stable_after_pain_first",
      "source_stable_after_long_conversation",
      "source_stable_after_golden_aggregation",
      "source_stable_after_do_not_do_missing",
      "source_stable_after_do_not_do_aggregation",
      "No additional paid commands should run on mixed source/gate state.",
    ]),
    "paid batch rejects source/gate drift before continuing across paid phases",
    {
      sourceStabilityCheckCount: countMatches(
        paidBatch,
        /appendSourceStabilityCheck/g,
      ),
    },
  ),
  result(
    includesAll(paidBatch, [
      "commands.every((command) => command.ok)",
      "paidStarted === 3",
      "estimatedCostUsd > 0",
      "estimatedCostUsd <= expectedBudgetUsd",
    ]),
    "paid batch can only pass with all commands green, three paid commands, and cost within budget",
    {
      passGateExcerptPresent: true,
    },
  ),
  result(
    includesAll(closure, [
      "reportTimestampAtOrAfter",
      "paid and aggregation evidence is fresh relative to the approved paid batch start",
      "paid batch cost equals the sum of fresh paid scenario reports and stays within budget",
      "Math.abs(paidBatchCost - scenarioCostTotal) <= 0.000001",
      "expectedBudgetUsd = 0.36",
      "maxModelCalls === 19",
    ]),
    "closure requires fresh evidence, matching batch/scenario cost, and approved budget/model-call envelope",
    {
      closureFreshnessChecks: countMatches(closure, /reportTimestampAtOrAfter/g),
      closureCostChecks: countMatches(closure, /scenarioCostTotal/g),
    },
  ),
  result(
    includesAll(closure, [
      "app/pilates",
      "components/landing",
      "data/landing",
      "lib/landing/floating-agent.ts",
      "components/internal/SalesInboxClient.tsx",
      "protected_source_diff",
    ]),
    "closure preserves protected /pilates, floating-agent, and Sales Inbox UI source diff gate",
    {
      protectedPathCount: countMatches(closure, /app\/pilates|components\/landing|data\/landing|floating-agent|SalesInboxClient/g),
    },
  ),
  result(
    goldenDoNotDo.includes("generatedAt: new Date().toISOString()"),
    "golden/do-not-do aggregation reports carry generatedAt timestamps for freshness checks",
    {
      generatedAtHits: countMatches(goldenDoNotDo, /generatedAt/g),
    },
  ),
  result(
    includesAll(knownValidatorRecovery, [
      "pain_first_must_offer_diagnostic",
      "diagnostic_urgency_answer_not_captured",
      "diagnostic_next_question_invalid",
      "diagnostic_next_question_not_missing",
      "diagnostic_final_demo_stage_missing",
      "diagnostic_final_staged_order_invalid",
      "price_question_missing_price_answer",
      "price_question_missing_diagnostic_hook",
      "price_question_missing_diagnostic_offer",
      "demo_direct_question_flags_missing",
      "sales_inbox_diagnostic_status_mismatch",
      "Paid OpenAI spend: US$0",
    ]) &&
      readiness.includes("known_validator_recovery_gate") &&
      readiness.includes("known critical validator errors have no-500 recovery proof"),
    "readiness requires known critical validator recovery before paid reruns",
    {
      coveredValidatorCodeHits: [
        "pain_first_must_offer_diagnostic",
        "diagnostic_urgency_answer_not_captured",
        "diagnostic_next_question_invalid",
        "diagnostic_next_question_not_missing",
        "diagnostic_final_demo_stage_missing",
        "diagnostic_final_staged_order_invalid",
        "price_question_missing_price_answer",
        "price_question_missing_diagnostic_hook",
        "price_question_missing_diagnostic_offer",
        "demo_direct_question_flags_missing",
        "sales_inbox_diagnostic_status_mismatch",
      ].filter((code) => knownValidatorRecovery.includes(code)),
      readinessGatePresent: readiness.includes("known_validator_recovery_gate"),
    },
  ),
  result(
      readiness.includes("paid_batch_refuses_env_only_approval") &&
      readiness.includes("paid_batch_refuses_continue_on_failure") &&
      readiness.includes("0.36") &&
      readiness.includes("totalEstimatedModelCalls === 19"),
    "readiness proves no-cost approval refusals and the US$0.36 / 19-call paid ceiling",
    {
      refusalChecks: [
        "paid_batch_refuses_without_approval",
        "paid_batch_refuses_wrong_budget",
        "paid_batch_refuses_env_only_approval",
        "paid_batch_refuses_continue_on_failure",
      ].filter((id) => readiness.includes(id)),
    },
  ),
];

const failed = results.filter((item) => !item.ok);
const report = {
  feature,
  name: reportName,
  releaseGate: failed.length === 0 ? "pass" : "fail",
  paidOpenAiSpend: 0,
  summary: {
    total: results.length,
    passed: results.length - failed.length,
    failed: failed.length,
  },
  results,
};

fs.mkdirSync(reportDir, { recursive: true });
const jsonPath = path.join(reportDir, `${reportName}.json`);
fs.writeFileSync(jsonPath, `${JSON.stringify(report, null, 2)}\n`);

const lines = [
  `# ${reportName}`,
  "",
  `Release gate: ${report.releaseGate}`,
  "Paid OpenAI spend: US$0",
  `Passed: ${report.summary.passed}/${report.summary.total}`,
  "",
];
for (const item of results) {
  lines.push(`## ${item.ok ? "PASS" : "FAIL"} ${item.message}`, "");
  lines.push("```json");
  lines.push(JSON.stringify(item.details, null, 2));
  lines.push("```", "");
}
const mdPath = path.join(reportDir, `${reportName}.md`);
fs.writeFileSync(mdPath, `${lines.join("\n").trim()}\n`);

console.log(
  `agent-runtime-spec011-t011-105-safety-audit: ${report.summary.passed}/${report.summary.total} passed`,
);
console.log(`Release gate: ${report.releaseGate}`);
console.log(`Report JSON: ${jsonPath}`);
console.log(`Report MD: ${mdPath}`);

if (report.releaseGate !== "pass") {
  process.exitCode = 1;
}
