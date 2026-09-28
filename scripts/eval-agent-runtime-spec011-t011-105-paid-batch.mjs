import { execFileSync } from "node:child_process";
import fs from "node:fs";
import path from "node:path";
import process from "node:process";
import { buildSpec011T011105SourceFingerprint } from "./spec011-t011-105-source-fingerprint.mjs";

const root = process.cwd();
const feature = "011-taliya-commercial-agent-core-reset";
const reportDir = path.join(root, "specs", feature, "eval-reports");
const readinessName = "agent-runtime-spec011-t011-105-readiness";
const readinessPath = path.join(reportDir, `${readinessName}.json`);
const approvalToken = "T011-105-US0.36";
const expectedBudgetUsd = 0.36;

function usage() {
  return [
    "Usage:",
    "  node scripts/eval-agent-runtime-spec011-t011-105-paid-batch.mjs --approval-token T011-105-US0.36 --approved-budget-usd 0.36",
    "",
    "Safety:",
    "  This script refuses to run paid OpenAI evals unless the exact approval token",
    "  and budget are provided as command-line arguments. It reruns readiness first",
    "  and always stops after the first paid failure to avoid unnecessary spend.",
  ].join("\n");
}

function parseArgs(argv) {
  const parsed = {
    approvalToken: null,
    approvedBudgetUsd: null,
  };
  for (let index = 0; index < argv.length; index += 1) {
    const arg = argv[index];
    const value = argv[index + 1];
    if (arg === "--approval-token" && value) {
      parsed.approvalToken = value;
      index += 1;
    } else if (arg === "--approved-budget-usd" && value) {
      parsed.approvedBudgetUsd = value;
      index += 1;
    } else if (arg === "--continue-on-failure") {
      throw new Error(
        [
          "Refusing --continue-on-failure for the T011-105 paid batch.",
          "This batch must stop after the first paid failure to avoid unnecessary spend.",
          "No paid commands were started.",
        ].join("\n"),
      );
    } else if (arg === "--help" || arg === "-h") {
      console.log(usage());
      process.exit(0);
    } else {
      throw new Error(`Unknown or incomplete argument: ${arg}\n${usage()}`);
    }
  }
  return parsed;
}

function assertPaidApproval(args) {
  const budget = Number(args.approvedBudgetUsd);
  if (args.approvalToken !== approvalToken || budget !== expectedBudgetUsd) {
    throw new Error(
      [
        "Refusing paid OpenAI T011-105 batch without exact approval.",
        `Required: --approval-token ${approvalToken} --approved-budget-usd ${expectedBudgetUsd}`,
        "No paid commands were started.",
      ].join("\n"),
    );
  }
}

function runCommand(id, command, args, options = {}) {
  const allowedExitCodes = options.allowedExitCodes ?? [0];
  try {
    const output = execFileSync(command, args, {
      cwd: root,
      encoding: "utf8",
      stdio: ["ignore", "pipe", "pipe"],
      maxBuffer: 1024 * 1024 * 50,
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
    return {
      id,
      ok: false,
      allowed: allowedExitCodes.includes(exitCode),
      exitCode,
      command: [command, ...args].join(" "),
      output: String(error.stdout ?? "").trim(),
      error: String(error.stderr ?? error.message ?? error).trim(),
    };
  }
}

function readJson(absolutePath) {
  return JSON.parse(fs.readFileSync(absolutePath, "utf8"));
}

function reportPath(reportName) {
  return path.join(reportDir, `${reportName}.json`);
}

function reportRelative(reportName) {
  return path.join("specs", feature, "eval-reports", `${reportName}.json`);
}

function scenarioCost(reportName) {
  const report = readJson(reportPath(reportName));
  return Number(report.summary?.estimatedCostUsd ?? 0);
}

function reportTimestamp(reportName) {
  const report = readJson(reportPath(reportName));
  return report.startedAt ?? report.generatedAt ?? null;
}

function reportIsFresh(reportName, isoTimestamp) {
  const reportTime = Date.parse(reportTimestamp(reportName));
  const referenceTime = Date.parse(isoTimestamp);
  return (
    Number.isFinite(reportTime) &&
    Number.isFinite(referenceTime) &&
    reportTime >= referenceTime
  );
}

function freshnessFailure(id, reportName, batchStartedAt) {
  const reportExists = fs.existsSync(reportPath(reportName));
  return {
    id,
    ok: false,
    allowed: false,
    exitCode: null,
    command: `freshness check for ${reportRelative(reportName)}`,
    output: "",
    error: [
      "Report was missing or stale relative to this approved paid batch.",
      `Report: ${reportRelative(reportName)}`,
      `Report timestamp: ${reportExists ? reportTimestamp(reportName) : null}`,
      `Batch startedAt: ${batchStartedAt}`,
    ].join("\n"),
  };
}

function appendFreshnessCheck(commands, id, reportName, batchStartedAt) {
  const reportExists = fs.existsSync(reportPath(reportName));
  if (!reportExists || !reportIsFresh(reportName, batchStartedAt)) {
    commands.push(freshnessFailure(id, reportName, batchStartedAt));
    return false;
  }
  return true;
}

function sourceStabilityFailure(id, expectedFingerprint) {
  const currentFingerprint = buildSpec011T011105SourceFingerprint(root);
  return {
    id,
    ok: false,
    allowed: false,
    exitCode: null,
    command: "source fingerprint stability check",
    output: "",
    error: [
      "T011-105 source fingerprint changed during the approved paid batch.",
      `Expected digest: ${expectedFingerprint.digest}`,
      `Current digest: ${currentFingerprint.digest}`,
      "No additional paid commands should run on mixed source/gate state.",
    ].join("\n"),
    expectedFingerprint,
    currentFingerprint,
  };
}

function appendSourceStabilityCheck(commands, id, expectedFingerprint) {
  const currentFingerprint = buildSpec011T011105SourceFingerprint(root);
  if (currentFingerprint.digest !== expectedFingerprint.digest) {
    commands.push(sourceStabilityFailure(id, expectedFingerprint));
    return false;
  }
  commands.push({
    id,
    ok: true,
    allowed: true,
    exitCode: 0,
    command: "source fingerprint stability check",
    output: `Source fingerprint stable: ${currentFingerprint.digest}`,
  });
  return true;
}

function paidCommandsStarted(commands) {
  return commands.filter((command) => command.id.startsWith("paid_")).length;
}

function writeReport(payload) {
  fs.mkdirSync(reportDir, { recursive: true });
  const jsonPath = path.join(reportDir, "agent-runtime-spec011-t011-105-paid-batch.json");
  fs.writeFileSync(jsonPath, `${JSON.stringify(payload, null, 2)}\n`);

  const lines = [
    "# agent-runtime-spec011-t011-105-paid-batch",
    "",
    `Release gate: ${payload.releaseGate}`,
    `Estimated paid cost: US$${payload.summary.estimatedCostUsd}`,
    `Paid commands started: ${payload.summary.paidCommandsStarted}`,
    `Source fingerprint: ${payload.sourceFingerprint?.digest ?? "missing"}`,
    "",
  ];
  for (const command of payload.commands) {
    lines.push(`## ${command.ok ? "PASS" : "FAIL"} ${command.id}`, "");
    lines.push("```text");
    lines.push(command.command);
    lines.push("```");
    if (command.output) {
      lines.push("", "Output:", "```text", command.output, "```");
    }
    if (command.error) {
      lines.push("", "Error:", "```text", command.error, "```");
    }
    lines.push("");
  }
  const mdPath = path.join(reportDir, "agent-runtime-spec011-t011-105-paid-batch.md");
  fs.writeFileSync(mdPath, `${lines.join("\n").trim()}\n`);
  return { jsonPath, mdPath };
}

function aggregateGolden(painReportName, longReportName) {
  return runCommand(
    "aggregate_golden_after_paid_batch",
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
      reportRelative(painReportName),
      "--report",
      reportRelative(longReportName),
      "--name",
      "agent-runtime-spec011-t011-105-golden-after-paid-batch",
    ],
  );
}

function aggregateDoNotDo(doNotDoReportName) {
  return runCommand(
    "aggregate_do_not_do_after_paid_batch",
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
      "--report",
      reportRelative(doNotDoReportName),
      "--static-fixture",
      "scripts\\fixtures\\agent-runtime\\spec-011-do-not-do-runtime.json",
      "--static-report",
      "specs\\011-taliya-commercial-agent-core-reset\\eval-reports\\agent-runtime-spec011-static-audit.json",
      "--name",
      "agent-runtime-spec011-t011-105-do-not-do-after-paid-batch",
    ],
  );
}

function main() {
  const args = parseArgs(process.argv.slice(2));
  assertPaidApproval(args);
  const batchStartedAt = new Date().toISOString();
  const sourceFingerprint = buildSpec011T011105SourceFingerprint(root);

  if (!fs.existsSync(readinessPath)) {
    throw new Error(`Missing readiness report: ${readinessPath}`);
  }

  const commands = [];
  commands.push(
    runCommand("readiness_gate_before_paid_batch", "node", [
      "scripts\\eval-agent-runtime-spec011-t011-105-readiness.mjs",
    ]),
  );
  const readinessReport = readJson(readinessPath);
  if (
    !commands.at(-1).ok ||
    readinessReport.releaseGate !== "ready_for_paid_batch" ||
    readinessReport.expectedPaidBatch?.maxCostUsd !== expectedBudgetUsd ||
    readinessReport.sourceFingerprint?.digest !== sourceFingerprint.digest
  ) {
    throw new Error("Readiness gate is not green for the approved paid batch.");
  }

  if (!appendSourceStabilityCheck(commands, "source_stable_after_readiness", sourceFingerprint)) {
    const payload = {
      feature,
      task: "T011-105",
      startedAt: batchStartedAt,
      releaseGate: "fail_source_changed_before_paid_commands",
      approvalToken,
      approvedBudgetUsd: expectedBudgetUsd,
      sourceFingerprint,
      summary: {
        paidCommandsStarted: paidCommandsStarted(commands),
        estimatedCostUsd: 0,
      },
      commands,
    };
    const { jsonPath, mdPath } = writeReport(payload);
    console.log(`Stopped before paid commands. Report JSON: ${jsonPath}`);
    console.log(`Report MD: ${mdPath}`);
    process.exit(1);
  }

  const painReportName = "agent-runtime-spec011-golden-pain-first-1";
  commands.push(
    runCommand("paid_pain_first", "python", [
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
      "--report-name",
      painReportName,
    ]),
  );

  const painCommand = commands.at(-1);
  const painFresh = appendFreshnessCheck(
    commands,
    "fresh_paid_pain_first_report",
    painReportName,
    batchStartedAt,
  );
  const sourceStableAfterPain = appendSourceStabilityCheck(
    commands,
    "source_stable_after_pain_first",
    sourceFingerprint,
  );
  let estimatedCostUsd = painFresh ? scenarioCost(painReportName) : 0;
  if (!painCommand.ok || !painFresh || !sourceStableAfterPain) {
    const payload = {
      feature,
      task: "T011-105",
      startedAt: batchStartedAt,
      releaseGate: "fail_stopped_after_pain_first",
      approvalToken,
      approvedBudgetUsd: expectedBudgetUsd,
      sourceFingerprint,
      summary: {
        paidCommandsStarted: paidCommandsStarted(commands),
        estimatedCostUsd: Number(estimatedCostUsd.toFixed(6)),
      },
      commands,
    };
    const { jsonPath, mdPath } = writeReport(payload);
    console.log(`Stopped after first paid failure. Report JSON: ${jsonPath}`);
    console.log(`Report MD: ${mdPath}`);
    process.exit(1);
  }

  const longReportName = "agent-runtime-spec011-golden-long-conversation-17";
  commands.push(
    runCommand("paid_long_conversation", "python", [
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
      "--report-name",
      longReportName,
    ]),
  );

  const longCommand = commands.at(-1);
  const longFresh = appendFreshnessCheck(
    commands,
    "fresh_paid_long_conversation_report",
    longReportName,
    batchStartedAt,
  );
  const sourceStableAfterLong = appendSourceStabilityCheck(
    commands,
    "source_stable_after_long_conversation",
    sourceFingerprint,
  );
  if (longFresh) {
    estimatedCostUsd += scenarioCost(longReportName);
  }
  if (!longCommand.ok || !longFresh || !sourceStableAfterLong) {
    const payload = {
      feature,
      task: "T011-105",
      startedAt: batchStartedAt,
      releaseGate: "fail_stopped_after_long_conversation",
      approvalToken,
      approvedBudgetUsd: expectedBudgetUsd,
      sourceFingerprint,
      summary: {
        paidCommandsStarted: paidCommandsStarted(commands),
        estimatedCostUsd: Number(estimatedCostUsd.toFixed(6)),
      },
      commands,
    };
    const { jsonPath, mdPath } = writeReport(payload);
    console.log(`Stopped after first paid failure. Report JSON: ${jsonPath}`);
    console.log(`Report MD: ${mdPath}`);
    process.exit(1);
  }

  commands.push(aggregateGolden(painReportName, longReportName));
  const goldenAggregateName = "agent-runtime-spec011-t011-105-golden-after-paid-batch";
  const goldenFresh = commands.at(-1).ok
    ? appendFreshnessCheck(
        commands,
        "fresh_golden_aggregation_report",
        goldenAggregateName,
        batchStartedAt,
      )
    : false;
  const sourceStableAfterGolden = appendSourceStabilityCheck(
    commands,
    "source_stable_after_golden_aggregation",
    sourceFingerprint,
  );
  if (!commands.at(-1).ok || !goldenFresh || !sourceStableAfterGolden) {
    const payload = {
      feature,
      task: "T011-105",
      startedAt: batchStartedAt,
      releaseGate: "fail_stopped_after_golden_aggregation",
      approvalToken,
      approvedBudgetUsd: expectedBudgetUsd,
      sourceFingerprint,
      summary: {
        paidCommandsStarted: paidCommandsStarted(commands),
        estimatedCostUsd: Number(estimatedCostUsd.toFixed(6)),
      },
      commands,
    };
    const { jsonPath, mdPath } = writeReport(payload);
    console.log(`Stopped after golden aggregation failure. Report JSON: ${jsonPath}`);
    console.log(`Report MD: ${mdPath}`);
    process.exit(1);
  }

  const doNotDoReportName = "agent-runtime-spec011-do-not-do-missing-1";
  commands.push(
    runCommand("paid_do_not_do_missing", "python", [
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
      "--report-name",
      doNotDoReportName,
    ]),
  );
  const doNotDoCommand = commands.at(-1);
  const doNotDoFresh = appendFreshnessCheck(
    commands,
    "fresh_paid_do_not_do_report",
    doNotDoReportName,
    batchStartedAt,
  );
  const sourceStableAfterDoNotDo = appendSourceStabilityCheck(
    commands,
    "source_stable_after_do_not_do_missing",
    sourceFingerprint,
  );
  if (doNotDoFresh) {
    estimatedCostUsd += scenarioCost(doNotDoReportName);
  }
  if (!doNotDoCommand.ok || !doNotDoFresh || !sourceStableAfterDoNotDo) {
    const payload = {
      feature,
      task: "T011-105",
      startedAt: batchStartedAt,
      releaseGate: "fail_stopped_after_do_not_do_missing",
      approvalToken,
      approvedBudgetUsd: expectedBudgetUsd,
      sourceFingerprint,
      summary: {
        paidCommandsStarted: paidCommandsStarted(commands),
        estimatedCostUsd: Number(estimatedCostUsd.toFixed(6)),
      },
      commands,
    };
    const { jsonPath, mdPath } = writeReport(payload);
    console.log(`Stopped after first paid failure. Report JSON: ${jsonPath}`);
    console.log(`Report MD: ${mdPath}`);
    process.exit(1);
  }

  commands.push(aggregateDoNotDo(doNotDoReportName));
  const doNotDoAggregateName =
    "agent-runtime-spec011-t011-105-do-not-do-after-paid-batch";
  if (commands.at(-1).ok) {
    appendFreshnessCheck(
      commands,
      "fresh_do_not_do_aggregation_report",
      doNotDoAggregateName,
      batchStartedAt,
    );
  }
  appendSourceStabilityCheck(
    commands,
    "source_stable_after_do_not_do_aggregation",
    sourceFingerprint,
  );
  const paidStarted = paidCommandsStarted(commands);
  const releaseGate =
    commands.every((command) => command.ok) &&
    paidStarted === 3 &&
    estimatedCostUsd > 0 &&
    estimatedCostUsd <= expectedBudgetUsd
      ? "pass"
      : "fail";
  const payload = {
    feature,
    task: "T011-105",
    startedAt: batchStartedAt,
    releaseGate,
    approvalToken,
    approvedBudgetUsd: expectedBudgetUsd,
    sourceFingerprint,
    summary: {
      paidCommandsStarted: paidStarted,
      estimatedCostUsd: Number(estimatedCostUsd.toFixed(6)),
    },
    commands,
  };
  const { jsonPath, mdPath } = writeReport(payload);
  console.log(
    `agent-runtime-spec011-t011-105-paid-batch: releaseGate=${releaseGate} cost=US$${payload.summary.estimatedCostUsd}`,
  );
  console.log(`Report JSON: ${jsonPath}`);
  console.log(`Report MD: ${mdPath}`);
  if (releaseGate !== "pass") {
    process.exit(1);
  }
}

try {
  main();
} catch (error) {
  console.error(error.message);
  process.exit(1);
}
