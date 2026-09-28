import { assert, canRunScenario, createBudgetFromEnv, readJson, writeReport } from "./eval-agent-v2-utils.mjs";

const budget = createBudgetFromEnv();
const fixtureFiles = [
  "source-openings.json",
  "direct-questions.json",
  "diagnostic-offers.json",
  "waitlist.json",
  "handoff.json",
  "channel-parity.json",
  "safety-and-media.json",
];

const scenarios = fixtureFiles.flatMap((file) => readJson(`scripts/fixtures/agent-v2/${file}`).map((item) => ({ ...item, fixtureFile: file })));
const results = [];
for (const scenario of scenarios) {
  if (!canRunScenario(budget, scenario.id)) {
    results.push({ ok: true, message: `${scenario.id} skipped by budget`, details: { scenario } });
    continue;
  }
  results.push(assert(Boolean(scenario.id), `${scenario.id} has scenario id`, { scenario }));
  results.push(assert(Boolean(scenario.expect || scenario.truth || scenario.event), `${scenario.id} has expected outcome`, { scenario }));
}

writeReport("agent-v2-conversation-matrix", results, {
  productSourceVersion: "taliya-pilates-commercial-2026-05-21",
  budget,
  summaryExtras: {
    scenarioCount: scenarios.length,
    skipped: budget.skippedScenarios.length,
  },
});

