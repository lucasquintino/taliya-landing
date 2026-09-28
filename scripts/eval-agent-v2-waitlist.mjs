import { assert, contains, readJson, writeReport } from "./eval-agent-v2-utils.mjs";

const fixtures = readJson("scripts/fixtures/agent-v2/waitlist.json");
const checks = [
  ...contains("lib/landing/ai-attendant/product-knowledge-source.ts", ["estamos trabalhando com um número pequeno de studios"]),
  ...contains("lib/landing/ai-attendant/agent-v2-response-generator.ts", ["answerPostWaitlist", "waitlist_joined", "sem reiniciar"]),
  ...contains("lib/landing/ai-attendant/agent-v2-guardrails.ts", ["no_checkout_while_waitlist_closed"]),
];

writeReport("agent-v2-waitlist", [
  assert(fixtures.length >= 3, "waitlist fixtures exist"),
  ...checks.map((check) => assert(check.found, `waitlist implementation contains ${check.pattern}`)),
]);
