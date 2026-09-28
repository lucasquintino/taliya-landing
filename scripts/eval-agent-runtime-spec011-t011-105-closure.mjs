import { execFileSync } from "node:child_process";
import fs from "node:fs";
import path from "node:path";
import { buildSpec011T011105SourceFingerprint } from "./spec011-t011-105-source-fingerprint.mjs";

const root = process.cwd();
const feature = "011-taliya-commercial-agent-core-reset";
const task = "T011-105";
const reportDir = path.join(root, "specs", feature, "eval-reports");
const closureName = "agent-runtime-spec011-t011-105-closure";
const approvalToken = "T011-105-US0.36";
const expectedBudgetUsd = 0.36;

const readinessName = "agent-runtime-spec011-t011-105-readiness";
const paidBatchName = "agent-runtime-spec011-t011-105-paid-batch";
const painFirstName = "agent-runtime-spec011-golden-pain-first-1";
const longConversationName = "agent-runtime-spec011-golden-long-conversation-17";
const doNotDoMissingName = "agent-runtime-spec011-do-not-do-missing-1";
const goldenAfterPaidName = "agent-runtime-spec011-t011-105-golden-after-paid-batch";
const doNotDoAfterPaidName =
  "agent-runtime-spec011-t011-105-do-not-do-after-paid-batch";

const protectedPaths = [
  "app/pilates",
  "components/landing",
  "data/landing",
  "lib/landing/floating-agent.ts",
  "components/internal/SalesInboxClient.tsx",
];

const expectedDoNotDoPaidScenarios = [
  "do-not-do-client-studio-whatsapp-capture",
  "do-not-do-date-vip-discount",
  "do-not-do-early-phone-capture",
  "do-not-do-wrong-student-language",
];

function runCommand(id, command, args) {
  try {
    const output = execFileSync(command, args, {
      cwd: root,
      encoding: "utf8",
      stdio: ["ignore", "pipe", "pipe"],
      maxBuffer: 1024 * 1024 * 10,
    });
    return {
      id,
      ok: true,
      exitCode: 0,
      command: [command, ...args].join(" "),
      output: output.trim(),
    };
  } catch (error) {
    return {
      id,
      ok: false,
      exitCode: typeof error.status === "number" ? error.status : null,
      command: [command, ...args].join(" "),
      output: String(error.stdout ?? "").trim(),
      error: String(error.stderr ?? error.message ?? error).trim(),
    };
  }
}

function protectedSourceDiff() {
  const command = runCommand("protected_source_diff", "git", [
    "-c",
    "safe.directory=C:/Users/lucas/agentes-landing-system",
    "diff",
    "--name-only",
    "--",
    ...protectedPaths,
  ]);
  return {
    ...command,
    files: command.output
      .split(/\r?\n/)
      .map((line) => line.trim())
      .filter(Boolean),
  };
}

function reportAbsolutePath(reportName) {
  return path.join(reportDir, `${reportName}.json`);
}

function reportRelativePath(reportName) {
  return path.join("specs", feature, "eval-reports", `${reportName}.json`);
}

function readReport(reportName) {
  const absolutePath = reportAbsolutePath(reportName);
  if (!fs.existsSync(absolutePath)) {
    return {
      exists: false,
      reportName,
      path: reportRelativePath(reportName),
      data: null,
    };
  }
  return {
    exists: true,
    reportName,
    path: reportRelativePath(reportName),
    data: JSON.parse(fs.readFileSync(absolutePath, "utf8")),
  };
}

function result(ok, message, details = {}) {
  return { ok: Boolean(ok), message, details };
}

function cost(report) {
  return Number(report?.data?.summary?.estimatedCostUsd ?? 0);
}

function sameList(left, right) {
  return (
    left.length === right.length &&
    left.every((item, index) => item === right[index])
  );
}

function selectedEvidenceFor(report, scenarioId) {
  return (report?.data?.results ?? []).find((item) => item.id === scenarioId);
}

function reportPassed(report, expectedTotal, expectedPassed) {
  return (
    report.exists &&
    report.data?.releaseGate === "pass" &&
    report.data?.summary?.total === expectedTotal &&
    report.data?.summary?.passed === expectedPassed &&
    report.data?.summary?.failed === 0
  );
}

function reportTimestamp(report) {
  return report?.data?.startedAt ?? report?.data?.generatedAt ?? null;
}

function reportTimestampAtOrAfter(report, isoTimestamp) {
  const reportTime = Date.parse(reportTimestamp(report));
  const referenceTime = Date.parse(isoTimestamp);
  return (
    Number.isFinite(reportTime) &&
    Number.isFinite(referenceTime) &&
    reportTime >= referenceTime
  );
}

const reports = {
  readiness: readReport(readinessName),
  paidBatch: readReport(paidBatchName),
  painFirst: readReport(painFirstName),
  longConversation: readReport(longConversationName),
  doNotDoMissing: readReport(doNotDoMissingName),
  goldenAfterPaid: readReport(goldenAfterPaidName),
  doNotDoAfterPaid: readReport(doNotDoAfterPaidName),
};

const protectedDiff = protectedSourceDiff();
const currentSourceFingerprint = buildSpec011T011105SourceFingerprint(root);
const paidBatchStartedAt = reports.paidBatch.data?.startedAt ?? null;
const goldenPainEvidence = selectedEvidenceFor(
  reports.goldenAfterPaid,
  "final-pain-first",
);
const goldenLongEvidence = selectedEvidenceFor(
  reports.goldenAfterPaid,
  "step3g-long-conversation",
);
const doNotDoPaidEvidence = expectedDoNotDoPaidScenarios.map((scenarioId) =>
  selectedEvidenceFor(reports.doNotDoAfterPaid, scenarioId),
);
const scenarioCostTotal =
  cost(reports.painFirst) +
  cost(reports.longConversation) +
  cost(reports.doNotDoMissing);
const paidBatchCost = cost(reports.paidBatch);

const results = [
  result(
    reports.readiness.data?.sourceFingerprint?.digest === currentSourceFingerprint.digest &&
      reports.paidBatch.data?.sourceFingerprint?.digest === currentSourceFingerprint.digest,
    "readiness and paid batch evidence match the current source fingerprint",
    {
      currentSourceFingerprint,
      readinessSourceFingerprint:
        reports.readiness.data?.sourceFingerprint ?? null,
      paidBatchSourceFingerprint:
        reports.paidBatch.data?.sourceFingerprint ?? null,
    },
  ),
  result(
    reports.readiness.exists &&
      reports.readiness.data?.releaseGate === "ready_for_paid_batch" &&
      reports.readiness.data?.paidOpenAiSpend === 0 &&
      reports.readiness.data?.expectedPaidBatch?.maxCostUsd === expectedBudgetUsd &&
      reports.readiness.data?.expectedPaidBatch?.maxModelCalls === 19,
    "pre-paid readiness report is still the approved no-cost starting point",
    {
      report: reports.readiness.path,
      exists: reports.readiness.exists,
      releaseGate: reports.readiness.data?.releaseGate ?? null,
      expectedPaidBatch: reports.readiness.data?.expectedPaidBatch ?? null,
    },
  ),
  result(
    reports.paidBatch.exists &&
      reports.paidBatch.data?.releaseGate === "pass" &&
      reports.paidBatch.data?.approvalToken === approvalToken &&
      reports.paidBatch.data?.approvedBudgetUsd === expectedBudgetUsd &&
      reports.paidBatch.data?.summary?.paidCommandsStarted === 3 &&
      cost(reports.paidBatch) > 0 &&
      cost(reports.paidBatch) <= expectedBudgetUsd &&
      (reports.paidBatch.data?.commands ?? []).every((command) => command.ok),
    "paid batch report passed with the exact approved token, budget, command count, and cost ceiling",
    {
      report: reports.paidBatch.path,
      exists: reports.paidBatch.exists,
      releaseGate: reports.paidBatch.data?.releaseGate ?? null,
      approvalToken: reports.paidBatch.data?.approvalToken ?? null,
      approvedBudgetUsd: reports.paidBatch.data?.approvedBudgetUsd ?? null,
      summary: reports.paidBatch.data?.summary ?? null,
    },
  ),
  result(
    Boolean(paidBatchStartedAt) &&
      [
        reports.painFirst,
        reports.longConversation,
        reports.doNotDoMissing,
        reports.goldenAfterPaid,
        reports.doNotDoAfterPaid,
      ].every((report) => report.exists && reportTimestampAtOrAfter(report, paidBatchStartedAt)),
    "paid and aggregation evidence is fresh relative to the approved paid batch start",
    {
      paidBatchStartedAt,
      evidenceReports: [
        reports.painFirst,
        reports.longConversation,
        reports.doNotDoMissing,
        reports.goldenAfterPaid,
        reports.doNotDoAfterPaid,
      ].map((report) => ({
        report: report.path,
        exists: report.exists,
        timestamp: reportTimestamp(report),
        fresh:
          Boolean(paidBatchStartedAt) &&
          report.exists &&
          reportTimestampAtOrAfter(report, paidBatchStartedAt),
      })),
    },
  ),
  result(
    reports.paidBatch.exists &&
      paidBatchCost > 0 &&
      paidBatchCost <= expectedBudgetUsd &&
      scenarioCostTotal > 0 &&
      Math.abs(paidBatchCost - scenarioCostTotal) <= 0.000001,
    "paid batch cost equals the sum of fresh paid scenario reports and stays within budget",
    {
      paidBatchReport: reports.paidBatch.path,
      paidBatchCost: Number(paidBatchCost.toFixed(6)),
      scenarioCostTotal: Number(scenarioCostTotal.toFixed(6)),
      expectedBudgetUsd,
      scenarioCosts: {
        painFirst: Number(cost(reports.painFirst).toFixed(6)),
        longConversation: Number(cost(reports.longConversation).toFixed(6)),
        doNotDoMissing: Number(cost(reports.doNotDoMissing).toFixed(6)),
      },
    },
  ),
  result(
    reportPassed(reports.painFirst, 1, 1) &&
      cost(reports.painFirst) > 0 &&
      cost(reports.painFirst) <= 0.03 &&
      reports.painFirst.data?.scenarios?.[0]?.id === "final-pain-first",
    "paid pain-first report passed only the missing golden pain-first scenario under the US$0.03 cap",
    {
      report: reports.painFirst.path,
      exists: reports.painFirst.exists,
      releaseGate: reports.painFirst.data?.releaseGate ?? null,
      summary: reports.painFirst.data?.summary ?? null,
      scenarioIds:
        reports.painFirst.data?.scenarios?.map((scenario) => scenario.id) ?? [],
    },
  ),
  result(
    reportPassed(reports.longConversation, 1, 1) &&
      cost(reports.longConversation) > 0 &&
      cost(reports.longConversation) <= 0.25 &&
      reports.longConversation.data?.scenarios?.[0]?.id ===
        "step3g-long-conversation",
    "paid long-conversation report passed only the missing golden scenario under the US$0.25 cap",
    {
      report: reports.longConversation.path,
      exists: reports.longConversation.exists,
      releaseGate: reports.longConversation.data?.releaseGate ?? null,
      summary: reports.longConversation.data?.summary ?? null,
      scenarioIds:
        reports.longConversation.data?.scenarios?.map((scenario) => scenario.id) ??
        [],
    },
  ),
  result(
    reportPassed(reports.doNotDoMissing, 4, 4) &&
      cost(reports.doNotDoMissing) > 0 &&
      cost(reports.doNotDoMissing) <= 0.08 &&
      sameList(
        [
          ...(reports.doNotDoMissing.data?.scenarios?.map(
            (scenario) => scenario.id,
          ) ?? []),
        ].sort(),
        expectedDoNotDoPaidScenarios,
      ),
    "paid do-not-do report passed only the four missing forbidden-behavior scenarios under the US$0.08 cap",
    {
      report: reports.doNotDoMissing.path,
      exists: reports.doNotDoMissing.exists,
      releaseGate: reports.doNotDoMissing.data?.releaseGate ?? null,
      summary: reports.doNotDoMissing.data?.summary ?? null,
      scenarioIds:
        reports.doNotDoMissing.data?.scenarios?.map((scenario) => scenario.id) ??
        [],
    },
  ),
  result(
    reportPassed(reports.goldenAfterPaid, 9, 9) &&
      goldenPainEvidence?.status === "PASS" &&
      goldenPainEvidence?.evidence_report === reportRelativePath(painFirstName) &&
      goldenLongEvidence?.status === "PASS" &&
      goldenLongEvidence?.evidence_report ===
        reportRelativePath(longConversationName),
    "golden aggregation passed 9/9 and selected the new paid pain-first and long-conversation evidence",
    {
      report: reports.goldenAfterPaid.path,
      exists: reports.goldenAfterPaid.exists,
      releaseGate: reports.goldenAfterPaid.data?.releaseGate ?? null,
      summary: reports.goldenAfterPaid.data?.summary ?? null,
      painFirstEvidence: goldenPainEvidence ?? null,
      longConversationEvidence: goldenLongEvidence ?? null,
    },
  ),
  result(
    reportPassed(reports.doNotDoAfterPaid, 8, 8) &&
      doNotDoPaidEvidence.every(
        (item) =>
          item?.status === "PASS" &&
          item?.evidence_report === reportRelativePath(doNotDoMissingName),
      ),
    "do-not-do aggregation passed 8/8 and selected the new paid evidence for all four missing forbidden behaviors",
    {
      report: reports.doNotDoAfterPaid.path,
      exists: reports.doNotDoAfterPaid.exists,
      releaseGate: reports.doNotDoAfterPaid.data?.releaseGate ?? null,
      summary: reports.doNotDoAfterPaid.data?.summary ?? null,
      expectedDoNotDoPaidScenarios,
      selectedEvidence: doNotDoPaidEvidence,
    },
  ),
  result(
    protectedDiff.ok && protectedDiff.files.length === 0,
    "closure produced no protected /pilates, landing visual, floating-agent, or Sales Inbox UI source diff",
    { protectedDiff },
  ),
];

const failedResults = results.filter((item) => !item.ok);
const releaseGate =
  failedResults.length === 0 ? "pass" : "fail_missing_or_failed_paid_evidence";
const report = {
  feature,
  task,
  name: closureName,
  releaseGate,
  paidOpenAiSpend: 0,
  paidBatchClosureRequiresExistingPaidEvidence: true,
  currentSourceFingerprint,
  requiredPaidBatchCommand:
    "node scripts\\eval-agent-runtime-spec011-t011-105-paid-batch.mjs --approval-token T011-105-US0.36 --approved-budget-usd 0.36",
  summary: {
    total: results.length,
    passed: results.length - failedResults.length,
    failed: failedResults.length,
  },
  results,
};

fs.mkdirSync(reportDir, { recursive: true });
const jsonPath = path.join(reportDir, `${closureName}.json`);
fs.writeFileSync(jsonPath, `${JSON.stringify(report, null, 2)}\n`);

const lines = [
  `# ${closureName}`,
  "",
  `Release gate: ${releaseGate}`,
  "Paid OpenAI spend by this closure gate: US$0",
  "",
  "Required paid batch command before this gate can pass:",
  "",
  `\`${report.requiredPaidBatchCommand}\``,
  "",
];
for (const item of results) {
  lines.push(`## ${item.ok ? "PASS" : "FAIL"} ${item.message}`, "");
  lines.push("```json");
  lines.push(JSON.stringify(item.details, null, 2));
  lines.push("```", "");
}
const mdPath = path.join(reportDir, `${closureName}.md`);
fs.writeFileSync(mdPath, `${lines.join("\n").trim()}\n`);

console.log(
  `agent-runtime-spec011-t011-105-closure: ${report.summary.passed}/${report.summary.total} passed`,
);
console.log(`Release gate: ${releaseGate}`);
console.log(`Report JSON: ${jsonPath}`);
console.log(`Report MD: ${mdPath}`);

if (releaseGate !== "pass") {
  process.exitCode = 1;
}
