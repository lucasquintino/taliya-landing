import { assert, contains, readJson, writeReport } from "./eval-agent-v2-utils.mjs";

const fixtures = readJson("scripts/fixtures/agent-v2/source-openings.json");
const sourceChecks = contains("lib/landing/ai-attendant/agent-v2-response-generator.ts", ["Em que posso te ajudar?", "Oi,"]);
const identityChecks = contains("lib/landing/ai-attendant/agent-v2-identity.ts", ["studio", "pilates", "firstName"]);

writeReport("agent-v2-openings", [
  assert(fixtures.length >= 7, "opening fixtures cover SRC-001..SRC-007"),
  ...sourceChecks.map((check) => assert(check.found, `opening generator contains ${check.pattern}`)),
  ...identityChecks.map((check) => assert(check.found, `identity classifier contains ${check.pattern}`)),
]);

