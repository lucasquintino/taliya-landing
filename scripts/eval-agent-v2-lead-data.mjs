import { assert, contains, readJson, writeReport } from "./eval-agent-v2-utils.mjs";

const fixtures = readJson("scripts/fixtures/agent-v2/lead-data-after-value.json");
const checks = contains("lib/landing/ai-attendant/agent-v2-response-generator.ts", ["missingWaitlistFields", "request.session.channel !== \"whatsapp\"", "WhatsApp ou email"]);

writeReport("agent-v2-lead-data", [
  assert(fixtures.length >= 2, "lead data fixtures cover WhatsApp and widget"),
  ...checks.map((check) => assert(check.found, `lead data policy contains ${check.pattern}`)),
]);

