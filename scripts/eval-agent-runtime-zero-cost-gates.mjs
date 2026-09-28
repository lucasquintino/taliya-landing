import { execFileSync } from "node:child_process";

import { assert, writeReport, writeTranscriptMarkdown } from "./eval-agent-runtime-utils.mjs";

const commands = [
  {
    id: "python-contract-tests",
    command: "python",
    args: [
      "-m",
      "pytest",
      "services/taliya-agent-runtime/tests/test_conversation_state_contract.py",
      "services/taliya-agent-runtime/tests/test_message_templates.py",
      "services/taliya-agent-runtime/tests/test_message_renderer.py",
      "services/taliya-agent-runtime/tests/test_runtime_behavior_regressions.py",
      "services/taliya-agent-runtime/tests/test_diagnostic_ledger.py",
      "services/taliya-agent-runtime/tests/test_waitlist_contract.py",
      "services/taliya-agent-runtime/tests/test_name_policy.py",
      "services/taliya-agent-runtime/tests/test_llm_output_repair.py",
      "services/taliya-agent-runtime/tests/test_idempotency_contract.py",
      "services/taliya-agent-runtime/tests/test_conversation_ordering.py",
      "services/taliya-agent-runtime/tests/test_widget_opening_policy.py",
      "services/taliya-agent-runtime/tests/test_settings.py",
      "services/taliya-agent-runtime/tests/test_agent_runs_api.py",
      "services/taliya-agent-runtime/tests/test_product_knowledge.py",
      "services/taliya-agent-runtime/tests/test_output_guardrails.py",
      "-q",
    ],
  },
  { id: "runtime-invariants", command: "node", args: ["scripts/eval-agent-runtime-invariants.mjs"] },
  { id: "runtime-delivery", command: "node", args: ["scripts/eval-agent-runtime-delivery.mjs"] },
  { id: "runtime-sales-inbox", command: "node", args: ["scripts/eval-agent-runtime-sales-inbox.mjs"] },
  {
    id: "runtime-completion-evidence",
    command: "node",
    args: ["scripts/eval-agent-runtime-completion-evidence.mjs"],
  },
  {
    id: "next-production-build",
    command: process.execPath,
    args: ["node_modules/next/dist/bin/next", "build"],
  },
];

const results = [];

for (const item of commands) {
  try {
    const output = execFileSync(item.command, item.args, {
      cwd: process.cwd(),
      encoding: "utf8",
      stdio: "pipe",
      env: {
        ...process.env,
        TALIYA_AGENT_PROVIDER: "mock",
      },
    });
    results.push(assert(true, `${item.id} passed`, { output: output.slice(-2000) }));
  } catch (error) {
    results.push(
      assert(false, `${item.id} passed`, {
        stdout: String(error.stdout ?? "").slice(-4000),
        stderr: String(error.stderr ?? "").slice(-4000),
        status: error.status,
      }),
    );
  }
}

writeReport("agent-runtime-zero-cost-gates-latest", results, {
  commands: commands.map((item) => `${item.command} ${item.args.join(" ")}`),
});

writeTranscriptMarkdown("agent-runtime-zero-cost-gates-latest", [
  {
    title: "Zero-Cost Gates",
    lines: results.map((result) => `- ${result.ok ? "PASS" : "FAIL"}: ${result.message}`),
  },
]);
