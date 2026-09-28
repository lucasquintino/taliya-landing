import { assert, contains, readJson, writeReport } from "./eval-agent-v2-utils.mjs";

const offers = readJson("scripts/fixtures/agent-v2/diagnostic-offers.json");
const states = readJson("scripts/fixtures/agent-v2/diagnostic-state.json");
const checks = [
  ...contains("lib/landing/ai-attendant/agent-v2-diagnostic.ts", ["getMissingDiagnosticSteps", "hasEnoughForDiagnostic", "buildDiagnosticOutput"]),
  ...contains("lib/landing/ai-attendant/agent-v2-response-generator.ts", ["diagnóstico rápido da rotina", "validationQuestion"]),
];

writeReport("agent-v2-diagnostic", [
  assert(offers.length >= 3, "diagnostic offer fixtures exist"),
  assert(states.some((item) => item.expectComplete), "diagnostic completion fixture exists"),
  ...checks.map((check) => assert(check.found, `diagnostic implementation contains ${check.pattern}`)),
]);
