#!/usr/bin/env node

import fs from "node:fs";
import path from "node:path";
import process from "node:process";

const FEATURE = "011-taliya-commercial-agent-core-reset";
const REPORT_DIR = path.join("specs", FEATURE, "eval-reports");

function usage() {
  return [
    "Usage:",
    "  node scripts/eval-agent-runtime-spec011-golden-do-not-do.mjs",
    "    --fixture <runtime-fixture.json> --report <real-report.json> [--report <real-report.json> ...]",
    "    [--static-fixture <static-fixture.json> --static-report <static-audit-report.json>]",
    "    --name <output-name>",
  ].join("\n");
}

function parseArgs(argv) {
  const parsed = {
    fixture: null,
    reports: [],
    staticFixture: null,
    staticReport: null,
    name: null,
  };
  for (let index = 0; index < argv.length; index += 1) {
    const arg = argv[index];
    const value = argv[index + 1];
    if (arg === "--fixture" && value) {
      parsed.fixture = value;
      index += 1;
    } else if (arg === "--report" && value) {
      parsed.reports.push(value);
      index += 1;
    } else if (arg === "--static-fixture" && value) {
      parsed.staticFixture = value;
      index += 1;
    } else if (arg === "--static-report" && value) {
      parsed.staticReport = value;
      index += 1;
    } else if (arg === "--name" && value) {
      parsed.name = value;
      index += 1;
    } else {
      throw new Error(`Unknown or incomplete argument: ${arg}\n${usage()}`);
    }
  }
  if (!parsed.fixture || parsed.reports.length === 0 || !parsed.name) {
    throw new Error(usage());
  }
  if (Boolean(parsed.staticFixture) !== Boolean(parsed.staticReport)) {
    throw new Error("--static-fixture and --static-report must be provided together");
  }
  return parsed;
}

function readJson(filePath) {
  return JSON.parse(fs.readFileSync(filePath, "utf8"));
}

function canonical(value) {
  return String(value ?? "")
    .normalize("NFD")
    .replace(/\p{Diacritic}/gu, "")
    .toLowerCase();
}

function outputForTurn(turn) {
  const payload = turn?.payload ?? {};
  const output = payload.output ?? {};
  return typeof output === "object" && output ? output : {};
}

function allOutputs(scenario) {
  return (scenario.turns ?? []).map(outputForTurn).filter((output) => output);
}

function allRenderedText(scenario) {
  const texts = [];
  for (const output of allOutputs(scenario)) {
    for (const message of output.messages ?? []) {
      if (message?.text) {
        texts.push(String(message.text));
      }
    }
  }
  return texts.join("\n");
}

function lastOutput(scenario) {
  const outputs = allOutputs(scenario);
  return outputs.length > 0 ? outputs[outputs.length - 1] : {};
}

function lastDecision(scenario) {
  return lastOutput(scenario).decision ?? {};
}

function templateIds(output) {
  const ids = output?.decision?.template_ids ?? [];
  return Array.isArray(ids) ? ids : [];
}

function scenarioCost(scenario) {
  return (scenario.turns ?? []).reduce((total, turn) => {
    const usage = outputForTurn(turn).usage ?? {};
    return total + Number(usage.cost_usd ?? 0);
  }, 0);
}

function isSuppressedHumanHandoffTurn(turn) {
  const payload = turn?.payload ?? {};
  const output = payload.output ?? {};
  const messages = output.messages ?? [];
  const deliverySuppressed =
    payload.delivery_control?.delivery_suppressed === true ||
    (output.delivery_events ?? []).some(
      (event) => event?.metadata?.delivery_suppressed === true,
    );
  return payload.status === "human_paused" && messages.length === 0 && deliverySuppressed;
}

function selectScenarioEvidence(reports) {
  const candidates = new Map();
  const failed = new Map();
  for (const reportPath of reports) {
    const report = readJson(reportPath);
    for (const scenario of report.scenarios ?? []) {
      const record = {
        ...scenario,
        evidence_report: reportPath,
      };
      const ok =
        (scenario.failures ?? []).length === 0 &&
        scenario.budget_status !== "stopped_before_completion";
      if (ok) {
        const existing = candidates.get(scenario.id) ?? [];
        existing.push(record);
        candidates.set(scenario.id, existing);
      } else if (!ok && !failed.has(scenario.id)) {
        failed.set(scenario.id, record);
      }
    }
  }
  return { candidates, failed };
}

function compareTextExpectation(expected, actualText, diffs) {
  const normalized = canonical(actualText);
  const mustInclude = expected.rendered_text_must_include ?? [];
  for (const phrase of mustInclude) {
    if (!normalized.includes(canonical(phrase))) {
      diffs.rendered_message_diff.push(`missing required rendered text: ${phrase}`);
    }
  }

  const includeAny = expected.rendered_text_must_include_any ?? [];
  if (
    includeAny.length > 0 &&
    !includeAny.some((phrase) => normalized.includes(canonical(phrase)))
  ) {
    diffs.rendered_message_diff.push(
      `missing one of required rendered text options: ${includeAny.join(" | ")}`,
    );
  }

  const mustNotInclude = expected.rendered_text_must_not_include ?? [];
  for (const phrase of mustNotInclude) {
    if (normalized.includes(canonical(phrase))) {
      diffs.rendered_message_diff.push(`forbidden rendered text present: ${phrase}`);
    }
  }
}

function compareDecisionExpectation(expected, scenario, diffs) {
  const decision = lastDecision(scenario);
  const output = lastOutput(scenario);
  const expectedDecision = expected.decision ?? {};
  if (expectedDecision.route && decision.route !== expectedDecision.route) {
    diffs.conductor_json_diff.push(
      `route expected ${expectedDecision.route}, got ${decision.route}`,
    );
  }
  if (
    typeof expectedDecision.direct_question_answered_first === "boolean" &&
    decision.direct_question_answered_first !==
      expectedDecision.direct_question_answered_first
  ) {
    diffs.conductor_json_diff.push(
      `direct_question_answered_first expected ${expectedDecision.direct_question_answered_first}, got ${decision.direct_question_answered_first}`,
    );
  }
  if (expectedDecision.handoff_status) {
    const handoffStatus = output.handoff?.status ?? decision.handoff_status;
    if (handoffStatus !== expectedDecision.handoff_status) {
      diffs.conductor_json_diff.push(
        `handoff status expected ${expectedDecision.handoff_status}, got ${handoffStatus}`,
      );
    }
  }
  for (const expectedTemplateId of expectedDecision.template_ids ?? []) {
    if (!templateIds(output).includes(expectedTemplateId)) {
      diffs.conductor_json_diff.push(
        `template id missing from final decision: ${expectedTemplateId}`,
      );
    }
  }
  if (expected.waitlist_status) {
    const waitlistStatus = output.waitlist_action?.status;
    if (waitlistStatus !== expected.waitlist_status) {
      diffs.conductor_json_diff.push(
        `waitlist status expected ${expected.waitlist_status}, got ${waitlistStatus}`,
      );
    }
  }
}

function compareValidatorUsageProjection(scenario, expected, diffs) {
  for (const [index, turn] of (scenario.turns ?? []).entries()) {
    if (isSuppressedHumanHandoffTurn(turn)) {
      continue;
    }
    const output = outputForTurn(turn);
    const messages = output.messages ?? [];
    const validatorResults = output.validator_results ?? [];
    if (!Array.isArray(validatorResults) || validatorResults.length === 0) {
      diffs.validator_diff.push(`turn ${index + 1} missing validator_results`);
    } else {
      const bad = validatorResults.filter((result) => result.status !== "passed");
      if (bad.length > 0) {
        diffs.validator_diff.push(
          `turn ${index + 1} validator not passed: ${bad
            .map((result) => result.status)
            .join(", ")}`,
        );
      }
    }

    if (messages.length > 0) {
      const usage = output.usage ?? {};
      if (!usage.model || Number(usage.input_tokens ?? 0) <= 0) {
        diffs.usage_diff.push(`turn ${index + 1} missing model usage`);
      }
    }

    const projection = output.sales_inbox_projection;
    if (!projection || typeof projection !== "object") {
      diffs.sales_inbox_projection_diff.push(
        `turn ${index + 1} missing Sales Inbox projection`,
      );
    } else if (expected.sales_inbox?.validator_status) {
      const status = projection.fields?.validator_status;
      if (status !== expected.sales_inbox.validator_status) {
        diffs.sales_inbox_projection_diff.push(
          `turn ${index + 1} projection validator_status expected ${expected.sales_inbox.validator_status}, got ${status}`,
        );
      }
    }
  }
}

function compareSecondTurnSilence(expected, scenario, diffs) {
  if (!expected.second_turn_must_be_silent) {
    return;
  }
  const second = scenario.turns?.[1];
  if (!second) {
    diffs.transcript_diff.push("expected a second turn for silence check");
    return;
  }
  const messages = outputForTurn(second).messages ?? [];
  if (messages.length > 0) {
    diffs.rendered_message_diff.push(
      `second turn expected silent, got ${messages.length} message(s)`,
    );
  }
}

function compareRuntimeScenario(fixtureScenario, scenario) {
  const expected = fixtureScenario.expected ?? {};
  const diffs = {
    transcript_diff: [],
    conductor_json_diff: [],
    rendered_message_diff: [],
    validator_diff: [],
    usage_diff: [],
    sales_inbox_projection_diff: [],
  };
  const actualLeadTurns = (scenario.turns ?? []).map((turn) => turn.lead);
  const expectedLeadTurns = (fixtureScenario.messages ?? []).map((turn) =>
    typeof turn === "object" ? turn.text ?? `[${turn.type ?? "text"}]` : String(turn),
  );
  if (actualLeadTurns.length !== expectedLeadTurns.length) {
    diffs.transcript_diff.push(
      `lead turn count expected ${expectedLeadTurns.length}, got ${actualLeadTurns.length}`,
    );
  }
  for (const [index, expectedLead] of expectedLeadTurns.entries()) {
    if (canonical(actualLeadTurns[index]) !== canonical(expectedLead)) {
      diffs.transcript_diff.push(
        `lead turn ${index + 1} expected ${expectedLead}, got ${actualLeadTurns[index]}`,
      );
    }
  }

  if ((scenario.failures ?? []).length > 0) {
    diffs.transcript_diff.push(
      `underlying real-model checks failed: ${scenario.failures.join("; ")}`,
    );
  }
  if (scenario.budget_status === "stopped_before_completion") {
    diffs.usage_diff.push("scenario stopped before completion due to budget");
  }

  compareTextExpectation(expected, allRenderedText(scenario), diffs);
  compareDecisionExpectation(expected, scenario, diffs);
  compareValidatorUsageProjection(scenario, expected, diffs);
  compareSecondTurnSilence(expected, scenario, diffs);

  const failures = Object.values(diffs).flat();
  return {
    id: fixtureScenario.id,
    title: fixtureScenario.title,
    case_ids: fixtureScenario.golden_case_ids ?? fixtureScenario.do_not_do_case_ids ?? [],
    evidence_report: scenario.evidence_report,
    status: failures.length === 0 ? "PASS" : "FAIL",
    failures,
    cost_usd: Number(scenarioCost(scenario).toFixed(6)),
    diffs,
    observed: {
      rendered_messages: allOutputs(scenario).flatMap((output) =>
        (output.messages ?? []).map((message) => ({
          template_id: message.template_id ?? null,
          text: message.text ?? "",
        })),
      ),
      final_decision: lastDecision(scenario),
      final_waitlist: lastOutput(scenario).waitlist_action ?? null,
      final_handoff: lastOutput(scenario).handoff ?? null,
    },
  };
}

function missingRuntimeEvidenceResult(fixtureScenario, failedEvidence) {
  return {
    id: fixtureScenario.id,
    title: fixtureScenario.title,
    case_ids: fixtureScenario.golden_case_ids ?? fixtureScenario.do_not_do_case_ids ?? [],
    evidence_report: failedEvidence?.evidence_report ?? null,
    status: "FAIL",
    failures: failedEvidence
      ? [`no passing evidence report; failures: ${(failedEvidence.failures ?? []).join("; ")}`]
      : ["missing scenario evidence report"],
    cost_usd: failedEvidence ? Number(scenarioCost(failedEvidence).toFixed(6)) : 0,
    diffs: {
      transcript_diff: ["missing passing scenario evidence"],
    },
  };
}

function selectRuntimeFixtureResult(fixtureScenario, evidenceCandidates, failedEvidence) {
  if (!evidenceCandidates.length) {
    return missingRuntimeEvidenceResult(fixtureScenario, failedEvidence);
  }

  const compared = evidenceCandidates.map((evidence) =>
    compareRuntimeScenario(fixtureScenario, evidence),
  );
  const passing = compared.find((result) => result.status === "PASS");
  if (passing) {
    return {
      ...passing,
      evaluated_evidence_count: compared.length,
      rejected_evidence: compared
        .filter((result) => result.status !== "PASS")
        .map((result) => ({
          evidence_report: result.evidence_report,
          failures: result.failures,
        })),
    };
  }

  const firstResult = compared[0];
  return {
    ...firstResult,
    failures: [
      `no candidate evidence satisfied fixture expectations across ${compared.length} passing runtime report(s)`,
      ...firstResult.failures,
    ],
    candidate_failures: compared.map((result) => ({
      evidence_report: result.evidence_report,
      failures: result.failures,
    })),
  };
}

function compareStaticCases(staticFixturePath, staticReportPath) {
  if (!staticFixturePath || !staticReportPath) {
    return [];
  }
  const fixture = readJson(staticFixturePath);
  const report = readJson(staticReportPath);
  return (fixture.cases ?? []).map((staticCase) => {
    const matching = (report.results ?? []).find(
      (result) =>
        result.ok === true &&
        canonical(result.message).includes(
          canonical(staticCase.static_report_required_message),
        ),
    );
    const failures = [];
    if (report.releaseGate !== "pass") {
      failures.push(`static report releaseGate expected pass, got ${report.releaseGate}`);
    }
    if (!matching) {
      failures.push(
        `static report missing passed result containing: ${staticCase.static_report_required_message}`,
      );
    }
    return {
      id: staticCase.id,
      title: staticCase.title,
      case_ids: staticCase.do_not_do_case_ids ?? [],
      evidence_report: staticReportPath,
      status: failures.length === 0 ? "PASS" : "FAIL",
      failures,
      diffs: {
        static_report_diff: failures,
      },
    };
  });
}

function writeReport(name, payload) {
  fs.mkdirSync(REPORT_DIR, { recursive: true });
  const jsonPath = path.join(REPORT_DIR, `${name}.json`);
  fs.writeFileSync(jsonPath, `${JSON.stringify(payload, null, 2)}\n`);

  const lines = [
    `# ${name}`,
    "",
    `Release gate: ${payload.releaseGate}`,
    `Passed: ${payload.summary.passed}/${payload.summary.total}`,
    `Runtime evidence cost: US$${payload.summary.estimatedCostUsd}`,
    "",
  ];
  for (const result of payload.results) {
    lines.push(`## ${result.status} ${result.id}`, "");
    lines.push(`Cases: ${(result.case_ids ?? []).join(", ") || "n/a"}`);
    lines.push(`Evidence: ${result.evidence_report}`);
    if (result.failures?.length) {
      lines.push("Failures:");
      for (const failure of result.failures) {
        lines.push(`- ${failure}`);
      }
    }
    lines.push("");
  }
  const mdPath = path.join(REPORT_DIR, `${name}.md`);
  fs.writeFileSync(mdPath, `${lines.join("\n").trim()}\n`);
  return { jsonPath, mdPath };
}

function main() {
  const args = parseArgs(process.argv.slice(2));
  const fixture = readJson(args.fixture);
  const { candidates, failed } = selectScenarioEvidence(args.reports);
  const runtimeResults = [];

  for (const scenario of fixture) {
    runtimeResults.push(
      selectRuntimeFixtureResult(
        scenario,
        candidates.get(scenario.id) ?? [],
        failed.get(scenario.id),
      ),
    );
  }

  const staticResults = compareStaticCases(args.staticFixture, args.staticReport);
  const results = [...runtimeResults, ...staticResults];
  const failedResults = results.filter((result) => result.status !== "PASS");
  const estimatedCostUsd = runtimeResults.reduce(
    (total, result) => total + Number(result.cost_usd ?? 0),
    0,
  );
  const payload = {
    feature: FEATURE,
    name: args.name,
    generatedAt: new Date().toISOString(),
    fixture: args.fixture,
    reports: args.reports,
    staticFixture: args.staticFixture,
    staticReport: args.staticReport,
    summary: {
      total: results.length,
      passed: results.length - failedResults.length,
      failed: failedResults.length,
      runtimeCases: runtimeResults.length,
      staticCases: staticResults.length,
      estimatedCostUsd: Number(estimatedCostUsd.toFixed(6)),
    },
    releaseGate: failedResults.length === 0 ? "pass" : "fail",
    results,
  };
  const { jsonPath, mdPath } = writeReport(args.name, payload);
  console.log(
    `agent-runtime-spec011-golden-do-not-do: ${payload.summary.passed}/${payload.summary.total} passed`,
  );
  console.log(`Report JSON: ${path.resolve(jsonPath)}`);
  console.log(`Report MD: ${path.resolve(mdPath)}`);
  if (payload.releaseGate !== "pass") {
    process.exitCode = 1;
  }
}

try {
  main();
} catch (error) {
  console.error(error.message);
  process.exit(1);
}
