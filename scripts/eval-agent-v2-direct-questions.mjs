import { assert, contains, readJson, writeReport } from "./eval-agent-v2-utils.mjs";

const fixtures = readJson("scripts/fixtures/agent-v2/direct-questions.json");
const semantic = contains("lib/landing/ai-attendant/agent-v2-semantic-interpreter.ts", ["price", "plans", "demo", "whatsapp", "privacy", "guarantee"]);
const response = contains("lib/landing/ai-attendant/agent-v2-response-generator.ts", ["Hoje a Taliya tem quatro faixas", "comparativo", "product.links"]);

writeReport("agent-v2-direct-questions", [
  assert(fixtures.length >= 10, "direct question fixtures cover DIR-001..DIR-010"),
  ...semantic.map((check) => assert(check.found, `semantic detects ${check.pattern}`)),
  ...response.map((check) => assert(check.found, `direct response uses ${check.pattern}`)),
]);
