import { execFileSync } from "node:child_process";

import { assert, readJson, readText, writeReport } from "./eval-agent-runtime-utils.mjs";

const fixtures = readJson("scripts/fixtures/agent-runtime/product-questions.json");
const source = readText("services/taliya-agent-runtime/app/shared/product_knowledge/source.py");
const results = [
  assert(fixtures.length >= 3, "product question fixtures are present"),
  assert(source.includes("version: str = \"taliya-commercial-2026-05-22\""), "product source has explicit version"),
  assert(
    source.includes("\"https://www.taliya.com.br/pilates/planos/demonstracao\""),
    "product source uses official demo/commercial link",
  ),
  assert(source.includes("checkout_status: str = \"unavailable\""), "checkout is explicitly unavailable"),
];

try {
  execFileSync("python", ["-m", "pytest", "services/taliya-agent-runtime/tests/test_product_knowledge.py", "services/taliya-agent-runtime/tests/test_structured_output.py", "-q"], {
    cwd: process.cwd(),
    stdio: "pipe",
    encoding: "utf8",
  });
  results.push(assert(true, "product knowledge contract tests pass"));
} catch (error) {
  results.push(
    assert(false, "product knowledge contract tests pass", {
      stdout: error.stdout,
      stderr: error.stderr,
      status: error.status,
    }),
  );
}

writeReport("agent-runtime-product-knowledge", results, {
  fixtures: fixtures.map((fixture) => fixture.id),
});
