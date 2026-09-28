import { execFileSync } from "node:child_process";

import { assert, readJson, writeReport } from "./eval-agent-runtime-utils.mjs";

const fixtures = readJson("scripts/fixtures/agent-runtime/waitlist-timing.json");
const finalMatrix = readJson("scripts/fixtures/agent-runtime/final-behavior-matrix.json");
const results = [
  assert(fixtures.some((item) => item.expectWaitlist === false), "no-early-waitlist fixture is present"),
  assert(fixtures.some((item) => item.expectWaitlist === "joined"), "post-waitlist join fixture is present"),
  assert(
    finalMatrix.some(
      (item) =>
        item.id === "final-post-waitlist-product-question" &&
        item.checks?.includes("no_waitlist_status_repetition") &&
        item.checks?.includes("mentions_complete_price_only"),
    ),
    "post-waitlist product question must answer directly without repeating joined status",
  ),
];

try {
  execFileSync("python", ["-m", "pytest", "services/taliya-agent-runtime/tests/test_waitlist_tool.py", "-q"], {
    cwd: process.cwd(),
    stdio: "pipe",
    encoding: "utf8",
  });
  results.push(assert(true, "waitlist timing and idempotency tests pass"));
} catch (error) {
  results.push(
    assert(false, "waitlist timing and idempotency tests pass", {
      stdout: error.stdout,
      stderr: error.stderr,
      status: error.status,
    }),
  );
}

writeReport("agent-runtime-waitlist", results, {
  fixtures: fixtures.map((fixture) => fixture.id),
});
