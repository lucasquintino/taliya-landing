import { assert, contains, readJson, writeReport } from "./eval-agent-v2-utils.mjs";

const fixtures = readJson("scripts/fixtures/agent-v2/sales-inbox.json");
const checks = [
  ...contains("lib/landing/ai-attendant/leads.ts", ["agentV2", "estimatedCostUsd"]),
  ...contains("components/internal/SalesInboxClient.tsx", ["Agente v2", "traceId"]),
  ...contains("app/api/internal/sales-inbox/leads/route.ts", ["agentV2"]),
];

writeReport("agent-v2-sales-inbox", [
  assert(fixtures.length >= 2, "sales inbox fixtures exist"),
  ...checks.map((check) => assert(check.found, `Sales Inbox contains ${check.pattern}`)),
]);

