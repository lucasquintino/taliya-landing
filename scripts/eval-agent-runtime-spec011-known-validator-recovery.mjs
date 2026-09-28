import { execFileSync } from "node:child_process";
import fs from "node:fs";
import path from "node:path";

const root = process.cwd();
const feature = "011-taliya-commercial-agent-core-reset";
const reportName = "agent-runtime-spec011-known-validator-recovery";
const reportDir = path.join(root, "specs", feature, "eval-reports");

const cases = [
  {
    id: "pain_first_question_only_no_500",
    validatorCodes: ["pain_first_must_offer_diagnostic"],
    recovery: "structural_repair",
    command: [
      "python",
      [
        "-m",
        "pytest",
        "services\\taliya-agent-runtime\\tests\\test_spec011_widget_runtime_adapter.py::test_runtime_adapter_repairs_pain_first_question_only_without_500",
        "-q",
      ],
    ],
  },
  {
    id: "pain_first_schema_alias_no_500",
    validatorCodes: [
      "unsupported_schema_version",
      "diagnostic_start_must_ask_active_students",
    ],
    recovery: "structural_repair",
    command: [
      "python",
      [
        "-m",
        "pytest",
        "services\\taliya-agent-runtime\\tests\\test_spec011_widget_runtime_adapter.py::test_runtime_adapter_repairs_known_schema_alias_on_pain_first_without_500",
        "-q",
      ],
    ],
  },
  {
    id: "pain_first_product_route_no_500",
    validatorCodes: [
      "pain_first_diagnostic_offer_must_use_diagnostic_route",
      "diagnostic_start_must_ask_active_students",
    ],
    recovery: "structural_repair",
    command: [
      "python",
      [
        "-m",
        "pytest",
        "services\\taliya-agent-runtime\\tests\\test_spec011_widget_runtime_adapter.py::test_runtime_adapter_repairs_pain_first_product_route_without_paid_repair",
        "-q",
      ],
    ],
  },
  {
    id: "pending_urgency_answer_llm_repair",
    validatorCodes: ["diagnostic_urgency_answer_not_captured"],
    recovery: "one_call_llm_repair",
    command: [
      "python",
      [
        "-m",
        "pytest",
        "services\\taliya-agent-runtime\\tests\\test_spec011_repair_loop.py::test_repair_loop_sends_pending_urgency_answer_to_llm_repair",
        "-q",
      ],
    ],
  },
  {
    id: "invalid_diagnostic_next_question_llm_repair",
    validatorCodes: ["diagnostic_next_question_invalid"],
    recovery: "one_call_llm_repair",
    command: [
      "python",
      [
        "-m",
        "pytest",
        "services\\taliya-agent-runtime\\tests\\test_spec011_repair_loop.py::test_repair_loop_sends_invalid_diagnostic_next_question_to_llm_repair",
        "-q",
      ],
    ],
  },
  {
    id: "long_conversation_stale_state_no_500",
    validatorCodes: [
      "stale_demo_direct_without_current_request",
      "sales_inbox_diagnostic_status_mismatch",
    ],
    recovery: "state_projection_repair",
    command: [
      "python",
      [
        "-m",
        "pytest",
        "services\\taliya-agent-runtime\\tests\\test_spec011_widget_runtime_adapter.py::test_runtime_adapter_long_conversation_preflight_covers_last_real_gate_failures",
        "-q",
      ],
    ],
  },
  {
    id: "final_diagnostic_last_pending_answer_no_500",
    validatorCodes: [
      "diagnostic_next_question_not_missing",
      "diagnostic_final_demo_stage_missing",
      "diagnostic_final_staged_order_invalid",
    ],
    recovery: "structural_final_diagnostic_repair",
    command: [
      "python",
      [
        "-m",
        "pytest",
        "services\\taliya-agent-runtime\\tests\\test_spec011_repair_loop.py::test_repair_loop_completes_final_diagnostic_when_last_pending_answer_captured",
        "-q",
      ],
    ],
  },
  {
    id: "current_demo_request_stale_price_intent_no_500",
    validatorCodes: [
      "price_question_missing_price_answer",
      "price_question_missing_diagnostic_hook",
      "price_question_missing_diagnostic_offer",
      "demo_direct_question_flags_missing",
    ],
    recovery: "structural_demo_direct_repair",
    command: [
      "python",
      [
        "-m",
        "pytest",
        "services\\taliya-agent-runtime\\tests\\test_spec011_repair_loop.py::test_repair_loop_clears_stale_price_intent_for_current_demo_request",
        "-q",
      ],
    ],
  },
  {
    id: "long_conversation_latest_paid_500s_adapter_no_500",
    validatorCodes: [
      "diagnostic_next_question_not_missing",
      "diagnostic_final_demo_stage_missing",
      "diagnostic_final_staged_order_invalid",
      "price_question_missing_price_answer",
      "demo_direct_question_flags_missing",
    ],
    recovery: "adapter_sequential_structural_repair",
    command: [
      "python",
      [
        "-m",
        "pytest",
        "services\\taliya-agent-runtime\\tests\\test_spec011_widget_runtime_adapter.py::test_runtime_adapter_long_conversation_preflight_covers_latest_paid_500s",
        "-q",
      ],
    ],
  },
];

function runCase(testCase) {
  const [command, args] = testCase.command;
  try {
    const output = execFileSync(command, args, {
      cwd: root,
      encoding: "utf8",
      stdio: ["ignore", "pipe", "pipe"],
      maxBuffer: 1024 * 1024 * 10,
    });
    return {
      ...testCase,
      ok: true,
      paidOpenAiSpend: 0,
      command: [command, ...args].join(" "),
      output: output.trim(),
    };
  } catch (error) {
    return {
      ...testCase,
      ok: false,
      paidOpenAiSpend: 0,
      command: [command, ...args].join(" "),
      exitCode: typeof error.status === "number" ? error.status : null,
      output: String(error.stdout ?? "").trim(),
      error: String(error.stderr ?? error.message ?? error).trim(),
    };
  }
}

const results = cases.map(runCase);
const failed = results.filter((item) => !item.ok);
const coveredValidatorCodes = [
  ...new Set(results.flatMap((item) => item.validatorCodes)),
].sort();
const report = {
  feature,
  name: reportName,
  releaseGate: failed.length === 0 ? "pass" : "fail",
  paidOpenAiSpend: 0,
  purpose:
    "Block paid T011-105 reruns unless known critical validator errors have explicit no-500 recovery proof.",
  summary: {
    total: results.length,
    passed: results.length - failed.length,
    failed: failed.length,
    coveredValidatorCodes,
  },
  results,
};

fs.mkdirSync(reportDir, { recursive: true });
const jsonPath = path.join(reportDir, `${reportName}.json`);
fs.writeFileSync(jsonPath, `${JSON.stringify(report, null, 2)}\n`);

const lines = [
  `# ${reportName}`,
  "",
  `Release gate: ${report.releaseGate}`,
  "Paid OpenAI spend: US$0",
  `Passed: ${report.summary.passed}/${report.summary.total}`,
  "",
  "## Covered Validator Codes",
  "",
  ...coveredValidatorCodes.map((code) => `- \`${code}\``),
  "",
];
for (const item of results) {
  lines.push(`## ${item.ok ? "PASS" : "FAIL"} ${item.id}`, "");
  lines.push("```json");
  lines.push(
    JSON.stringify(
      {
        validatorCodes: item.validatorCodes,
        recovery: item.recovery,
        command: item.command,
        output: item.output,
        error: item.error,
      },
      null,
      2,
    ),
  );
  lines.push("```", "");
}
const mdPath = path.join(reportDir, `${reportName}.md`);
fs.writeFileSync(mdPath, `${lines.join("\n").trim()}\n`);

console.log(
  `${reportName}: ${report.summary.passed}/${report.summary.total} passed`,
);
console.log(`Release gate: ${report.releaseGate}`);
console.log(`Report JSON: ${jsonPath}`);
console.log(`Report MD: ${mdPath}`);

if (report.releaseGate !== "pass") {
  process.exitCode = 1;
}
