import { execFileSync } from "node:child_process";
import fs from "node:fs";
import path from "node:path";

const root = process.cwd();
const feature = "011-taliya-commercial-agent-core-reset";
const task = "T011-099";
const specDir = path.join(root, "specs", feature);
const reportDir = path.join(specDir, "eval-reports");
const planJsonPath = path.join(specDir, "production-cutover-watch-plan.json");
const planMdPath = path.join(specDir, "production-cutover-watch-plan.md");

const requiredMonitorIds = [
  "trace_quality",
  "handoff_behavior",
  "sales_inbox_completeness",
  "model_usage",
  "cost",
  "fallback_error_rate",
  "duplicate_interleaved_delivery",
  "p0_behavior",
  "rollback_readiness",
];

const requiredWatchFields = [
  "channel",
  "conversation_id",
  "lead_id",
  "request_id",
  "idempotency_key",
  "trace_id",
  "turn_id",
  "conductor_schema_version",
  "selected_template_ids",
  "validator_status",
  "repair_status",
  "rendered_message_count",
  "delivery_control",
  "delivery_events",
  "model_usage",
  "cost_usd",
  "runtime_state_diff",
  "sales_inbox_projection",
  "handoff_status",
  "fallback_reason",
  "error_code",
];

const requiredP0AbortIds = [
  "internal_text_leak",
  "wrong_product_fact",
  "wrong_numeric_grounding",
  "diagnostic_required_question_skipped",
  "duplicate_or_interleaved_delivery",
  "human_pause_violation",
  "sales_inbox_missing_or_wrong",
  "false_pass_eval_or_trace_gap",
];

const requiredEvidenceIds = [
  "shadow_mode",
  "shadow_compare",
  "rollback",
  "runner_quarantine",
  "public_fallback_quarantine",
  "pilates_no_drift",
];

const protectedPaths = [
  "app/pilates",
  "components/landing",
  "data/landing",
  "lib/landing/floating-agent.ts",
  "components/internal/SalesInboxClient.tsx",
];

function readTextIfExists(absolutePath) {
  if (!fs.existsSync(absolutePath)) return null;
  return fs.readFileSync(absolutePath, "utf8").replace(/^\uFEFF/, "");
}

function readJsonIfExists(absolutePath) {
  const text = readTextIfExists(absolutePath);
  if (text === null) return null;
  return JSON.parse(text);
}

function result(ok, message, details = {}) {
  return { ok: Boolean(ok), message, details };
}

function unique(values) {
  return [...new Set(values)];
}

function missingValues(required, actual) {
  const actualSet = new Set(Array.isArray(actual) ? actual : []);
  return required.filter((item) => !actualSet.has(item));
}

function protectedSourceDiff() {
  try {
    const output = execFileSync(
      "git",
      [
        "-c",
        "safe.directory=C:/Users/lucas/agentes-landing-system",
        "diff",
        "--name-only",
        "--",
        ...protectedPaths,
      ],
      { cwd: root, encoding: "utf8" },
    );
    return output.split(/\r?\n/).map((line) => line.trim()).filter(Boolean);
  } catch (error) {
    return [`git_diff_failed:${error instanceof Error ? error.message : String(error)}`];
  }
}

function evidenceGateOk(item) {
  const reportJson = item?.reportJson;
  if (!reportJson) return { ok: false, reason: "missing_report_path" };
  const absolutePath = path.join(root, reportJson);
  const report = readJsonIfExists(absolutePath);
  if (!report) return { ok: false, reason: "missing_report_json", reportJson };
  const allowedReleaseGates = Array.isArray(item.allowedReleaseGates)
    ? item.allowedReleaseGates
    : ["pass"];
  const releaseGate = report.releaseGate ?? report.release_gate;
  const summary = report.summary ?? {};
  const ok =
    allowedReleaseGates.includes(releaseGate) &&
    Number(summary.failed ?? 1) === 0;
  return {
    ok,
    reason: ok ? "pass" : "bad_gate_or_failures",
    reportJson,
    releaseGate,
    summary,
    allowedReleaseGates,
  };
}

function validateMonitor(monitor) {
  const missing = [];
  if (!monitor || typeof monitor !== "object") return ["missing_monitor"];
  for (const key of [
    "id",
    "title",
    "source",
    "requiredFields",
    "healthyCriteria",
    "abortCriteria",
    "operatorAction",
    "evidenceOwner",
    "checkCadenceMinutes",
  ]) {
    if (monitor[key] === undefined || monitor[key] === null) missing.push(key);
  }
  if (!Array.isArray(monitor.requiredFields) || monitor.requiredFields.length === 0) {
    missing.push("requiredFields_non_empty");
  }
  if (!Array.isArray(monitor.healthyCriteria) || monitor.healthyCriteria.length === 0) {
    missing.push("healthyCriteria_non_empty");
  }
  if (!Array.isArray(monitor.abortCriteria) || monitor.abortCriteria.length === 0) {
    missing.push("abortCriteria_non_empty");
  }
  if (!Number.isFinite(Number(monitor.checkCadenceMinutes)) || Number(monitor.checkCadenceMinutes) <= 0) {
    missing.push("positive_checkCadenceMinutes");
  }
  return unique(missing);
}

const plan = readJsonIfExists(planJsonPath);
const planMarkdown = readTextIfExists(planMdPath);
const protectedDiff = protectedSourceDiff();
const monitors = Array.isArray(plan?.monitors) ? plan.monitors : [];
const monitorIds = monitors.map((monitor) => monitor.id);
const monitorProblems = monitors
  .map((monitor) => ({ id: monitor.id, missing: validateMonitor(monitor) }))
  .filter((item) => item.missing.length > 0);
const evidence = Array.isArray(plan?.requiredEvidence) ? plan.requiredEvidence : [];
const evidenceIds = evidence.map((item) => item.id);
const evidenceResults = evidence.map((item) => ({ id: item.id, ...evidenceGateOk(item) }));
const badEvidence = evidenceResults.filter((item) => !item.ok);

const results = [
  result(
    Boolean(plan) &&
      plan.schema === "011.production_watch.v1" &&
      plan.task === task,
    "machine-readable production watch plan exists with the expected schema and task",
    {
      planJson: path.relative(root, planJsonPath),
      schema: plan?.schema,
      task: plan?.task,
    },
  ),
  result(
    plan?.rollout?.mode === "one_hundred_percent" &&
      plan?.rollout?.canaryEnabled === false &&
      plan?.rollout?.requiresPhase10ApprovalBeforeActivation === true &&
      plan?.rollout?.finalProductionActivationApproved === false,
    "rollout is explicitly 100 percent, not canary, while final activation remains blocked until Phase 10 approval",
    { rollout: plan?.rollout },
  ),
  result(
    plan?.rollout?.featureFlag?.env === "TALIYA_SPEC011_COMMERCIAL_CORE_ENABLED" &&
      plan?.rollout?.featureFlag?.rollbackValue === "false" &&
      String(plan?.rollout?.featureFlag?.rollbackExpectedDisposition ?? "").includes("operational"),
    "rollback switch is explicit and points to the proven Spec 011 operational fallback path",
    { featureFlag: plan?.rollout?.featureFlag },
  ),
  result(
    Number(plan?.watchWindow?.durationMinutes) >= 120 &&
      Number(plan?.watchWindow?.firstCheckWithinMinutes) <= 5 &&
      Array.isArray(plan?.watchWindow?.channels) &&
      plan.watchWindow.channels.includes("widget") &&
      plan.watchWindow.channels.includes("taliya_whatsapp"),
    "first-hours watch window covers widget and Taliya-owned WhatsApp with an immediate first check",
    { watchWindow: plan?.watchWindow },
  ),
  result(
    missingValues(requiredMonitorIds, monitorIds).length === 0 &&
      monitorProblems.length === 0,
    "all required monitors define source, fields, healthy criteria, abort criteria, owner, cadence, and operator action",
    {
      missingMonitorIds: missingValues(requiredMonitorIds, monitorIds),
      monitorProblems,
    },
  ),
  result(
    missingValues(requiredWatchFields, plan?.watchFields).length === 0,
    "watch plan names every required runtime, trace, delivery, cost, fallback, and Sales Inbox field",
    { missingWatchFields: missingValues(requiredWatchFields, plan?.watchFields) },
  ),
  result(
    missingValues(requiredP0AbortIds, (plan?.p0AbortCriteria ?? []).map((item) => item.id)).length === 0,
    "P0 abort criteria cover internal leaks, product facts, numeric grounding, diagnostics, delivery, handoff, Sales Inbox, and false PASS risk",
    {
      missingP0AbortIds: missingValues(
        requiredP0AbortIds,
        (plan?.p0AbortCriteria ?? []).map((item) => item.id),
      ),
    },
  ),
  result(
    missingValues(requiredEvidenceIds, evidenceIds).length === 0 &&
      badEvidence.length === 0,
    "watch readiness links to passing shadow, rollback, quarantine, and no-drift evidence",
    {
      missingEvidenceIds: missingValues(requiredEvidenceIds, evidenceIds),
      badEvidence,
    },
  ),
  result(
    Boolean(planMarkdown) &&
      planMarkdown.includes("100 percent production cutover") &&
      planMarkdown.includes("Abort criteria") &&
      planMarkdown.includes("Do not activate without Phase 10 approval"),
    "human-readable watch runbook exists and keeps activation blocked without Phase 10 approval",
    { planMarkdown: path.relative(root, planMdPath) },
  ),
  result(
    protectedDiff.length === 0,
    "production watch work produced no protected /pilates, landing visual, floating-agent, or Sales Inbox UI source diff",
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
  runId: `agent-runtime-spec011-production-watch-${Date.now()}`,
  feature,
  task,
  createdAt: new Date().toISOString(),
  summary,
  releaseGate: summary.failed === 0 ? "pass_watch_ready_no_production_activation" : "fail",
  checkedFiles: [
    path.relative(root, planJsonPath),
    path.relative(root, planMdPath),
  ],
  requiredMonitorIds,
  requiredWatchFields,
  requiredP0AbortIds,
  requiredEvidenceIds,
  evidenceResults,
  results,
};

const jsonPath = path.join(reportDir, "agent-runtime-spec011-production-watch.json");
const mdPath = path.join(reportDir, "agent-runtime-spec011-production-watch.md");
fs.writeFileSync(jsonPath, `${JSON.stringify(report, null, 2)}\n`);
fs.writeFileSync(
  mdPath,
  [
    "# agent-runtime-spec011-production-watch",
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
  console.error(`agent-runtime-spec011-production-watch: ${summary.failed} failure(s). Report: ${jsonPath}`);
  process.exitCode = 1;
} else {
  console.log(`agent-runtime-spec011-production-watch: ${summary.passed}/${summary.total} passed. Report: ${jsonPath}`);
}
