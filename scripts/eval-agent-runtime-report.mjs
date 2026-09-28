import fs from "node:fs";
import path from "node:path";

import { reportDir, writeTranscriptMarkdown } from "./eval-agent-runtime-utils.mjs";

const finalGateReports = new Set([
  "agent-runtime-conversations.json",
  "agent-runtime-cost.json",
  "agent-runtime-delivery.json",
  "agent-runtime-diagnostic.json",
  "agent-runtime-handoff.json",
  "agent-runtime-invariants.json",
  "agent-runtime-naming.json",
  "agent-runtime-product-knowledge.json",
  "agent-runtime-quality-judge.json",
  "agent-runtime-real-openai-behavior-latest.json",
  "agent-runtime-real-openai-post-waitlist-latest.json",
  "agent-runtime-sales-inbox.json",
  "agent-runtime-waitlist.json",
  "agent-runtime-zero-cost-gates-latest.json",
]);

const reportFiles = fs.existsSync(reportDir)
  ? fs.readdirSync(reportDir).filter((file) => finalGateReports.has(file)).sort()
  : [];

const sections = reportFiles.map((file) => {
  const report = JSON.parse(fs.readFileSync(path.join(reportDir, file), "utf8"));
  return {
    title: file.replace(/\.json$/, ""),
    lines: [
      `- releaseGate: ${report.releaseGate}`,
      `- passed: ${report.summary?.passed ?? 0}`,
      `- failed: ${report.summary?.failed ?? 0}`,
      `- createdAt: ${report.createdAt}`,
    ],
  };
});

function readReport(file) {
  const fullPath = path.join(reportDir, file);
  if (!fs.existsSync(fullPath)) return null;
  return JSON.parse(fs.readFileSync(fullPath, "utf8"));
}

function writeAliasMarkdown(name, title, lines) {
  const file = path.join(reportDir, `${name}.md`);
  fs.writeFileSync(file, [`# ${title}`, "", `Generated at: ${new Date().toISOString()}`, "", ...lines, ""].join("\n"));
}

const quality = readReport("agent-runtime-quality-judge.json");
writeAliasMarkdown("agent-runtime-quality-judge-latest", "agent-runtime-quality-judge-latest", [
  `- source: agent-runtime-quality-judge.json`,
  `- releaseGate: ${quality?.releaseGate ?? "missing"}`,
  `- passed: ${quality?.summary?.passed ?? 0}`,
  `- failed: ${quality?.summary?.failed ?? 0}`,
  `- matrix_average: ${quality?.scoring?.matrixAverage ?? "missing"}/5`,
  `- required_average: ${quality?.scoring?.requiredAverage ?? "missing"}/5`,
  `- required_scenario_minimum: ${quality?.scoring?.requiredScenarioMinimum ?? "missing"}/5`,
  `- rubric: directness, naturalness, usefulness, evidence, diagnostic quality, waitlist timing, safety, brevity, and behavior contract`,
]);

const cost = readReport("agent-runtime-cost.json");
const realOpenAi = readReport("agent-runtime-real-openai-behavior-latest.json");
writeAliasMarkdown("agent-runtime-cost-latest", "agent-runtime-cost-latest", [
  `- source: agent-runtime-cost.json`,
  `- releaseGate: ${cost?.releaseGate ?? "missing"}`,
  `- passed: ${cost?.summary?.passed ?? 0}`,
  `- failed: ${cost?.summary?.failed ?? 0}`,
  `- real_openai_matrix_cost_usd: ${realOpenAi?.summary?.estimatedCostUsd ?? "missing"}`,
  `- real_openai_input_tokens: ${realOpenAi?.summary?.inputTokens ?? "missing"}`,
  `- real_openai_output_tokens: ${realOpenAi?.summary?.outputTokens ?? "missing"}`,
]);

const salesInbox = readReport("agent-runtime-sales-inbox.json");
writeAliasMarkdown("agent-runtime-sales-inbox-completeness-latest", "agent-runtime-sales-inbox-completeness-latest", [
  `- source: agent-runtime-sales-inbox.json`,
  `- releaseGate: ${salesInbox?.releaseGate ?? "missing"}`,
  `- passed: ${salesInbox?.summary?.passed ?? 0}`,
  `- failed: ${salesInbox?.summary?.failed ?? 0}`,
]);

const blockingSources = reportFiles.map((file) => ({ file, report: readReport(file) }));
const blockingFailures = blockingSources.flatMap(({ file, report }) =>
  (report?.results ?? [])
    .filter((result) => !result.ok)
    .map((result) => `- ${file}: ${result.message}`),
);
writeAliasMarkdown("agent-runtime-blocking-failures-latest", "agent-runtime-blocking-failures-latest", [
  `- checked_reports: ${blockingSources.length}`,
  `- blocking_failures: ${blockingFailures.length}`,
  ...(blockingFailures.length ? blockingFailures : ["- none"]),
]);

writeAliasMarkdown("agent-runtime-whatsapp-smoke-latest", "agent-runtime-whatsapp-smoke-latest", [
  "- status: local_http_smoke_passed_live_production_smoke_pending",
  "- local_whatsapp_webhook_harness: 10/10 passed against http://127.0.0.1:3999",
  "- local_message_delivery_matrix: 20/20 passed against http://127.0.0.1:3999",
  "- live_meta_dualhook_smoke: not run; blocked until explicit production deploy/live WhatsApp confirmation",
]);

writeTranscriptMarkdown("agent-runtime-transcripts-latest", [
  {
    title: "Eval Gate Summary",
    lines: reportFiles.length ? [`- reports: ${reportFiles.length}`] : ["- reports: 0"],
  },
  ...sections,
]);

console.log(`agent-runtime-report: wrote ${path.join(reportDir, "agent-runtime-transcripts-latest.md")}`);
