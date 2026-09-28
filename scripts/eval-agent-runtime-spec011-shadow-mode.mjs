import fs from "node:fs";
import path from "node:path";

const root = process.cwd();
const feature = "011-taliya-commercial-agent-core-reset";
const task = "T011-096";
const reportDir = path.join(root, "specs", feature, "eval-reports");

function readText(relativePath) {
  return fs.readFileSync(path.join(root, relativePath), "utf8").replace(/^\uFEFF/, "");
}

function result(ok, message, details = {}) {
  return { ok: Boolean(ok), message, details };
}

function lineHits(relativePath, patterns) {
  const lines = readText(relativePath).split(/\r?\n/);
  return lines.flatMap((line, index) => {
    const hits = patterns.filter((pattern) => pattern.test(line));
    return hits.length ? [{ path: relativePath, line: index + 1, text: line.trim() }] : [];
  });
}

const runtimeAdapterPath = "services/taliya-agent-runtime/app/core/taliya_commercial/runtime_adapter.py";
const runtimeSchemasPath = "services/taliya-agent-runtime/app/runtime/schemas.py";
const shadowTestPath = "services/taliya-agent-runtime/tests/test_spec011_shadow_mode.py";
const mainPath = "services/taliya-agent-runtime/app/main.py";
const runtimeAdapter = readText(runtimeAdapterPath);
const runtimeSchemas = readText(runtimeSchemasPath);
const shadowTests = readText(shadowTestPath);
const shadowControlBody = runtimeAdapter.slice(runtimeAdapter.indexOf("def _shadow_mode_control"));

const runnerHits = [
  ...lineHits(runtimeAdapterPath, [/app\.runtime\.runner/, /run_agent_turn/]),
  ...lineHits(mainPath, [/from app\.runtime\.runner import/, /run_agent_turn/]),
];

const results = [
  result(
    runtimeSchemas.includes("class DeliveryControl") &&
      runtimeSchemas.includes("shadow_mode: bool = False") &&
      runtimeSchemas.includes("delivery_suppressed: bool = False") &&
      runtimeSchemas.includes("suppression_reason: str | None = None") &&
      runtimeSchemas.includes("delivery_control: DeliveryControl"),
    "runtime response has an explicit delivery_control envelope",
    { runtimeSchemasPath },
  ),
  result(
    runtimeAdapter.includes('request.metadata.get("spec011_shadow_mode")') &&
      runtimeAdapter.includes("raw.get(\"enabled\") is not True") &&
      !shadowControlBody.includes("request.message.text") &&
      runtimeAdapter.includes("ShadowModeControl"),
    "shadow mode is explicit metadata control, not inferred from commercial text",
    { runtimeAdapterPath },
  ),
  result(
    runtimeAdapter.includes('event="delivery_suppressed" if shadow_control.enabled else "rendered"') &&
      runtimeAdapter.includes('status="suppressed" if shadow_control.enabled else "planned"') &&
      runtimeAdapter.includes("response_messages = [] if shadow_control.enabled else rendered_messages") &&
      runtimeAdapter.includes('safety_flags = ["shadow_mode", "delivery_suppressed"]'),
    "shadow mode suppresses public delivery while preserving rendered trace material",
    { runtimeAdapterPath },
  ),
  result(
    runtimeAdapter.includes("async def _persist_shadow_turn") &&
      runtimeAdapter.includes("record_model_usage") &&
      runtimeAdapter.includes('content="spec011_shadow_turn_completed"') &&
      runtimeAdapter.includes('"trace": trace.model_dump(mode="json")') &&
      runtimeAdapter.includes('"sales_inbox_projection": trace.sales_inbox_projection.model_dump(mode="json")'),
    "shadow mode records model usage, trace, runtime diff, and Sales Inbox projection as evidence",
    { runtimeAdapterPath },
  ),
  result(
    !runtimeAdapter.slice(runtimeAdapter.indexOf("async def _persist_shadow_turn")).includes("save_state("),
    "shadow persistence does not mutate live runtime state",
    { runtimeAdapterPath },
  ),
  result(
    runnerHits.length === 0,
    "shadow mode does not call the old Python runner",
    { runnerHits },
  ),
  result(
    shadowTests.includes("test_shadow_mode_runs_core_trace_and_projection_without_public_reply") &&
      shadowTests.includes("test_shadow_mode_uses_same_core_boundary_for_taliya_whatsapp") &&
      shadowTests.includes("test_shadow_mode_api_envelope_is_explicit_for_widget") &&
      shadowTests.includes("test_normal_mode_still_returns_messages_and_persists_live_state"),
    "shadow mode has widget, WhatsApp, API envelope, and normal-mode separation tests",
    { shadowTestPath },
  ),
];

fs.mkdirSync(reportDir, { recursive: true });
const summary = {
  total: results.length,
  passed: results.filter((item) => item.ok).length,
  failed: results.filter((item) => !item.ok).length,
};
const report = {
  runId: `agent-runtime-spec011-shadow-mode-${Date.now()}`,
  feature,
  task,
  createdAt: new Date().toISOString(),
  summary,
  releaseGate: summary.failed === 0 ? "pass" : "fail",
  checkedFiles: [runtimeAdapterPath, runtimeSchemasPath, shadowTestPath, mainPath],
  results,
};

const jsonPath = path.join(reportDir, "agent-runtime-spec011-shadow-mode.json");
const mdPath = path.join(reportDir, "agent-runtime-spec011-shadow-mode.md");
fs.writeFileSync(jsonPath, `${JSON.stringify(report, null, 2)}\n`);
fs.writeFileSync(
  mdPath,
  [
    "# agent-runtime-spec011-shadow-mode",
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
  console.error(`agent-runtime-spec011-shadow-mode: ${summary.failed} failure(s). Report: ${jsonPath}`);
  process.exitCode = 1;
} else {
  console.log(`agent-runtime-spec011-shadow-mode: ${summary.passed}/${summary.total} passed. Report: ${jsonPath}`);
}
