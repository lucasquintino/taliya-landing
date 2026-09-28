import { execFileSync } from "node:child_process";

import { assert, readJson, readText, writeReport } from "./eval-agent-runtime-utils.mjs";

const fixtures = readJson("scripts/fixtures/agent-runtime/handoff-whatsapp.json");
const runner = readText("services/taliya-agent-runtime/app/runtime/runner.py");
const route = readText("app/api/internal/sales-inbox/[leadId]/handoff/route.ts");
const actionsRoute = readText("app/api/internal/sales-inbox/leads/[leadId]/actions/route.ts");
const whatsappRoute = readText("app/api/landing/ai-attendant/whatsapp/route.ts");

const results = [
  assert(fixtures.some((item) => item.expectedStatus === "human_paused"), "human pause fixture is present"),
  assert(runner.includes('previous_state.human_status == "active"'), "runtime suppresses replies while human is active"),
  assert(runner.includes("runtime_control"), "runtime accepts operator pause/resume control"),
  assert(route.includes("syncTaliyaCommercialRuntimeHandoffState"), "handoff route syncs runtime state"),
  assert(actionsRoute.includes("syncTaliyaCommercialRuntimeHandoffState"), "Sales Inbox actions sync pause/resume runtime state"),
  assert(whatsappRoute.includes("business_app_manual_reply"), "WhatsApp Business App echo still pauses Sales Inbox"),
];

try {
  execFileSync("python", ["-m", "pytest", "services/taliya-agent-runtime/tests/test_human_handoff.py", "-q"], {
    cwd: process.cwd(),
    stdio: "pipe",
    encoding: "utf8",
  });
  results.push(assert(true, "human handoff runtime tests pass"));
} catch (error) {
  results.push(
    assert(false, "human handoff runtime tests pass", {
      stdout: error.stdout,
      stderr: error.stderr,
      status: error.status,
    }),
  );
}

writeReport("agent-runtime-handoff", results, {
  fixtures: fixtures.map((fixture) => fixture.id),
});
