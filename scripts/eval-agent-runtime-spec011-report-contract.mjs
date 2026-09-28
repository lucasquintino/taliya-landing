import fs from "node:fs";
import path from "node:path";

const root = process.cwd();
const featureName = "011-taliya-commercial-agent-core-reset";
const reportDir = path.join(root, "specs", featureName, "eval-reports");
const defaultInput = path.join(reportDir, "agent-runtime-spec011-p0-current-red.json");

function result(ok, message, details = {}) {
  return { ok: Boolean(ok), message, details };
}

function writeReport(name, results, extra = {}) {
  fs.mkdirSync(reportDir, { recursive: true });
  const summary = {
    total: results.length,
    passed: results.filter((item) => item.ok).length,
    failed: results.filter((item) => !item.ok).length,
  };
  const report = {
    runId: `${name}-${Date.now()}`,
    feature: featureName,
    createdAt: new Date().toISOString(),
    summary,
    results,
    releaseGate: summary.failed === 0 ? "pass" : "fail",
    ...extra,
  };
  const jsonPath = path.join(reportDir, `${name}.json`);
  fs.writeFileSync(jsonPath, `${JSON.stringify(report, null, 2)}\n`);

  const mdPath = path.join(reportDir, `${name}.md`);
  const lines = [
    `# ${name}`,
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
    console.error(`${name}: ${summary.failed} failure(s). Report: ${jsonPath}`);
    for (const item of results.filter((entry) => !entry.ok)) console.error(`- ${item.message}`);
    process.exitCode = 1;
  } else {
    console.log(`${name}: ${summary.passed}/${summary.total} passed. Report: ${jsonPath}`);
  }
}

function hasObject(value) {
  return Boolean(value && typeof value === "object" && !Array.isArray(value));
}

function hasArray(value) {
  return Boolean(Array.isArray(value));
}

function isSuppressedHumanHandoffTurn(turn) {
  const payload = hasObject(turn.payload) ? turn.payload : {};
  const output = hasObject(payload.output) ? payload.output : {};
  const usage = hasObject(output.usage) ? output.usage : {};
  const handoff = hasObject(output.handoff) ? output.handoff : {};
  const messages = Array.isArray(output.messages) ? output.messages : [];
  const safetyFlags = Array.isArray(output.safety_flags) ? output.safety_flags : [];
  const deliveryEvents = Array.isArray(output.delivery_events) ? output.delivery_events : [];
  const deliverySuppressed = deliveryEvents.some(
    (event) =>
      event?.event === "delivery_suppressed" &&
      event?.status === "suppressed" &&
      event?.metadata?.reason === "human_handoff_active",
  );

  return (
    payload.status === "human_paused" &&
    handoff.status === "active" &&
    messages.length === 0 &&
    safetyFlags.includes("ai_reply_suppressed") &&
    deliverySuppressed &&
    usage.model == null &&
    Number(usage.input_tokens || 0) === 0 &&
    Number(usage.output_tokens || 0) === 0 &&
    Number(usage.cost_usd || 0) === 0
  );
}

function requiredTurnArtifacts(turn) {
  const payload = hasObject(turn.payload) ? turn.payload : {};
  const output = hasObject(payload.output) ? payload.output : {};
  const usage = hasObject(output.usage) ? output.usage : {};
  const suppressedHumanHandoff = isSuppressedHumanHandoffTurn(turn);
  return {
    trace_id: typeof payload.trace_id === "string" && payload.trace_id.length > 0,
    context_snapshot: hasObject(output.context_snapshot),
    conductor_json: hasObject(output.conductor_json),
    decision_json: hasObject(output.decision),
    rendered_messages:
      (hasArray(output.messages) && output.messages.length > 0) || suppressedHumanHandoff,
    validator_results: hasArray(output.validator_results),
    repair_attempts: hasArray(output.repair_attempts),
    model_usage:
      (typeof usage.model === "string" &&
        Number.isFinite(Number(usage.input_tokens)) &&
        Number(usage.input_tokens) > 0) ||
      suppressedHumanHandoff,
    runtime_state: hasObject(output.runtime_state),
    sales_inbox_projection: hasObject(output.sales_inbox_projection),
    delivery_events: hasArray(output.delivery_events),
    trace_complete: output.trace_complete === true,
  };
}

function main() {
  const reportPath = process.argv[2] ? path.resolve(process.argv[2]) : defaultInput;
  if (!fs.existsSync(reportPath)) {
    throw new Error(`Report not found: ${reportPath}`);
  }
  const report = JSON.parse(fs.readFileSync(reportPath, "utf8"));
  const scenarios = Array.isArray(report.scenarios) ? report.scenarios : [];

  const results = [
    result(report.feature === featureName, "report belongs to Spec 011", {
      expected: featureName,
      actual: report.feature,
    }),
    result(report.releaseGate === "fail" || report.releaseGate === "pass", "report has explicit release gate", {
      releaseGate: report.releaseGate,
    }),
    result(scenarios.length > 0, "report includes scenarios", {
      scenarioCount: scenarios.length,
    }),
  ];

  for (const scenario of scenarios) {
    const turns = Array.isArray(scenario.turns) ? scenario.turns : [];
    results.push(
      result(Boolean(scenario.id && scenario.title), `scenario ${scenario.id ?? "unknown"} has identity`, {
        id: scenario.id,
        title: scenario.title,
      }),
    );
    results.push(
      result(Array.isArray(scenario.checks) && scenario.checks.length > 0, `scenario ${scenario.id} lists checks`, {
        checks: scenario.checks,
      }),
    );
    results.push(
      result(Array.isArray(scenario.failures), `scenario ${scenario.id} records failures array`, {
        failures: scenario.failures,
      }),
    );

    turns.forEach((turn, index) => {
      const artifacts = requiredTurnArtifacts(turn);
      const missing = Object.entries(artifacts)
        .filter(([, ok]) => !ok)
        .map(([key]) => key);
      results.push(
        result(
          missing.length === 0,
          `scenario ${scenario.id} turn ${index + 1} has mandatory Spec 011 artifacts`,
          { missing, artifacts },
        ),
      );
    });
  }

  writeReport("agent-runtime-spec011-report-contract", results, {
    checkedReport: path.relative(root, reportPath),
    requiredTurnArtifacts: [
      "trace_id",
      "context_snapshot",
      "conductor_json",
      "decision_json",
      "rendered_messages",
      "validator_results",
      "repair_attempts",
      "model_usage",
      "runtime_state",
      "sales_inbox_projection",
      "delivery_events",
      "trace_complete",
    ],
  });
}

main();
