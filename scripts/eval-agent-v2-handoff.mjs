import { assert, contains, readJson, writeReport } from "./eval-agent-v2-utils.mjs";

const fixtures = readJson("scripts/fixtures/agent-v2/handoff.json");
const checks = [
  ...contains("lib/landing/ai-attendant/agent-v2-tools.ts", ["pauseForHuman", "human_active", "queuedResponseStatus"]),
  ...contains("app/api/internal/sales-inbox/[leadId]/handoff/route.ts", ["take_over", "resume_ai"]),
];

writeReport("agent-v2-handoff", [
  assert(fixtures.length >= 3, "handoff fixtures exist"),
  ...checks.map((check) => assert(check.found, `handoff path contains ${check.pattern}`)),
]);

