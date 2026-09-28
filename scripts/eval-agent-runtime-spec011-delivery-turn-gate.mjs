import fs from "node:fs";
import path from "node:path";

const root = process.cwd();
const featureName = "011-taliya-commercial-agent-core-reset";
const reportDir = path.join(root, "specs", featureName, "eval-reports");

function readText(relativePath) {
  return fs.readFileSync(path.join(root, relativePath), "utf8").replace(/^\uFEFF/, "");
}

function result(ok, message, details = {}) {
  return { ok: Boolean(ok), message, details };
}

function lineHits(text, regex, { max = 30 } = {}) {
  const hits = [];
  text.split(/\r?\n/).forEach((line, index) => {
    if (regex.test(line)) {
      hits.push({ line: index + 1, text: line.trim().slice(0, 220) });
    }
  });
  return hits.slice(0, max);
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

const routePath = "app/api/landing/ai-attendant/whatsapp/route.ts";
const whatsappPath = "lib/landing/ai-attendant/whatsapp.ts";
const runtimeMainPath = "services/taliya-agent-runtime/app/main.py";
const runtimeClientPath = "lib/landing/ai-attendant/runtime-client.ts";

const route = readText(routePath);
const whatsapp = readText(whatsappPath);
const runtimeMain = readText(runtimeMainPath);
const runtimeClient = readText(runtimeClientPath);

const enqueueIndex = route.indexOf("await enqueueWhatsAppTurn");
const lockIndex = route.indexOf("await acquireWhatsAppTurnLock");
const queuedReturnIndex = route.indexOf('status: queued.inserted ? "queued" : "queued_duplicate"');
const deferredDrainIndex = route.indexOf('afterResponse("drain_queued_whatsapp_turn"');
const sendIndex = route.indexOf("const sendResult = await sendMetaWhatsAppReplySequence");
const markProcessedIndex = route.indexOf("await markBatchProviderMessagesProcessed(batchTurns, sendResult.ok");

const routeDeliveryMetadataHits = lineHits(
  route,
  /batchedDuringAssistantDelivery|batched_during_assistant_delivery/i,
);
const routeSemanticAckHits = lineHits(route, /shouldIgnoreInterleaved|social_ack|interleaved_social|tudo bem/i);
const activeRunnerQuarantineEvidence = {
  runtimeClientUsesSpec011Endpoint: runtimeClient.includes('return "/v1/taliya-commercial/turn"'),
  runtimeClientLegacyTurnHits: lineHits(runtimeClient, /fetch\(`\$\{url\}\/v1\/agent-runs`/),
  runtimeApiLegacyQuarantineHits: lineHits(runtimeMain, /legacy_commercial_runner_quarantined/),
  runtimeApiRunnerImportHits: lineHits(runtimeMain, /\bfrom app\.runtime\.runner import\b|\brun_agent_turn\b/),
};

const results = [
  result(
    route.includes("registered.duplicate") &&
      route.includes("duplicate_ignored") &&
      route.includes("semantic_duplicate_ignored"),
    "RC-011-010 duplicate inbound/provider messages are ignored before runtime execution",
    {
      hasProviderDuplicate: route.includes("registered.duplicate"),
      hasDuplicateStatus: route.includes("duplicate_ignored"),
      hasSemanticDuplicateStatus: route.includes("semantic_duplicate_ignored"),
    },
  ),
  result(
    whatsapp.includes("ON CONFLICT (idempotency_key) DO NOTHING") &&
      route.includes('idempotencyKey: `ai_reply_batch:${turn.providerMessageId}`'),
    "RC-011-010 outbound chunk delivery uses idempotency reservation",
    {
      hasOutboxConflictProtection: whatsapp.includes("ON CONFLICT (idempotency_key) DO NOTHING"),
      hasBatchIdempotencyKey: route.includes('idempotencyKey: `ai_reply_batch:${turn.providerMessageId}`'),
    },
  ),
  result(
    enqueueIndex >= 0 && lockIndex > enqueueIndex && queuedReturnIndex > lockIndex && deferredDrainIndex > lockIndex,
    "RC-011-011 inbound during an active turn is queued/deferred instead of processed in parallel",
    { enqueueIndex, lockIndex, queuedReturnIndex, deferredDrainIndex },
  ),
  result(
    sendIndex >= 0 && markProcessedIndex > sendIndex,
    "RC-011-011 current outbound delivery is marked after send sequence finishes",
    { sendIndex, markProcessedIndex },
  ),
  result(
    routeDeliveryMetadataHits.length === 0,
    "RC-011-011 deferred inbound must be processed as the next clean turn without delivery-interleaving semantic metadata",
    { routeDeliveryMetadataHits },
  ),
  result(
    activeRunnerQuarantineEvidence.runtimeClientUsesSpec011Endpoint &&
      activeRunnerQuarantineEvidence.runtimeClientLegacyTurnHits.length === 0 &&
      activeRunnerQuarantineEvidence.runtimeApiLegacyQuarantineHits.length > 0 &&
      activeRunnerQuarantineEvidence.runtimeApiRunnerImportHits.length === 0,
    "RC-011-011 active Taliya commercial path is quarantined from legacy runner interleaving classifiers",
    activeRunnerQuarantineEvidence,
  ),
  result(
    routeSemanticAckHits.length === 0,
    "RC-011-011 delivery layer must not use text-specific social acknowledgement shortcuts",
    { routeSemanticAckHits },
  ),
];

writeReport("agent-runtime-spec011-delivery-turn-gate", results, {
  regressionCases: ["RC-011-010", "RC-011-011"],
  auditedFiles: [routePath, whatsappPath, runtimeMainPath, runtimeClientPath],
});
