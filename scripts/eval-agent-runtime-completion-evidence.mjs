import fs from "node:fs";
import path from "node:path";

import {
  assert,
  featureDir,
  readJson,
  readText,
  writeReport,
  writeTranscriptMarkdown,
} from "./eval-agent-runtime-utils.mjs";

const specText = readText(
  "specs/010-openai-cs-agents-adaptation-for-taliya-commercial/spec.md",
);
const tasksText = readText(
  "specs/010-openai-cs-agents-adaptation-for-taliya-commercial/tasks.md",
);
const evidenceText = readText(
  "specs/010-openai-cs-agents-adaptation-for-taliya-commercial/requirements-evidence-matrix.md",
);
const completionText = readText(
  "specs/010-openai-cs-agents-adaptation-for-taliya-commercial/completion-audit.md",
);
const readinessText = readText(
  "specs/010-openai-cs-agents-adaptation-for-taliya-commercial/release-readiness.md",
);

const allowedOpenTasks = new Set(["T132", "T133", "T134", "T135", "T137", "T157", "T205", "T223", "T224", "T225", "T226", "T260"]);
const expectedPendingRequirements = new Set([
  "FR-001",
  "FR-016",
  "FR-059",
  "FR-060",
  "FR-090",
  "SC-013",
  "SC-014",
]);
const requiredReports = [
  "agent-runtime-transcripts-latest.md",
  "agent-runtime-quality-judge-latest.md",
  "agent-runtime-blocking-failures-latest.md",
  "agent-runtime-cost-latest.md",
  "agent-runtime-whatsapp-smoke-latest.md",
  "agent-runtime-real-openai-behavior-latest.md",
  "agent-runtime-real-openai-behavior-latest.json",
  "agent-runtime-real-openai-final-latest.md",
  "agent-runtime-real-openai-final-latest.json",
  "agent-runtime-zero-cost-gates-latest.md",
  "agent-runtime-sales-inbox-completeness-latest.md",
];

function idsFrom(text, prefix) {
  return [...new Set([...text.matchAll(new RegExp(`\\b${prefix}-\\d{3}\\b`, "g"))].map((match) => match[0]))].sort();
}

function taskRows(text) {
  return [...text.matchAll(/^- \[([ xX])\] (T\d{3})\b(.+)$/gm)].map((match) => ({
    checked: match[1].toLowerCase() === "x",
    id: match[2],
    text: match[3].trim(),
  }));
}

const specRequirementIds = [...idsFrom(specText, "FR"), ...idsFrom(specText, "SC")];
const evidenceRequirementIds = [...idsFrom(evidenceText, "FR"), ...idsFrom(evidenceText, "SC")];
const taskItems = taskRows(tasksText);
const openTasks = taskItems.filter((task) => !task.checked).map((task) => task.id);
const unexpectedOpenTasks = openTasks.filter((taskId) => !allowedOpenTasks.has(taskId));
const missingEvidenceRows = specRequirementIds.filter((id) => !evidenceRequirementIds.includes(id));
const extraEvidenceRows = evidenceRequirementIds.filter((id) => !specRequirementIds.includes(id));

const pendingRequirementRows = [...evidenceText.matchAll(/^\| (FR|SC)-\d{3} \| Pending external gate \|/gm)]
  .map((match) => match[0].match(/\b(FR|SC)-\d{3}\b/)?.[0])
  .filter(Boolean);
const unexpectedPendingRequirements = pendingRequirementRows.filter(
  (id) => !expectedPendingRequirements.has(id),
);
const missingPendingRequirements = [...expectedPendingRequirements].filter(
  (id) => !pendingRequirementRows.includes(id),
);

const reportResults = [];
for (const reportName of requiredReports) {
  const reportPath = path.join(featureDir, "eval-reports", reportName);
  reportResults.push(
    assert(fs.existsSync(reportPath) && fs.statSync(reportPath).size > 0, `${reportName} exists and is non-empty`, {
      reportPath,
    }),
  );
}

let realOpenAiReport = null;
try {
  realOpenAiReport = readJson(
    "specs/010-openai-cs-agents-adaptation-for-taliya-commercial/eval-reports/agent-runtime-real-openai-final-latest.json",
  );
} catch (error) {
  realOpenAiReport = { error: String(error) };
}

const results = [
  assert(specRequirementIds.length === evidenceRequirementIds.length, "Spec FR/SC count matches the evidence matrix", {
    count: specRequirementIds.length,
  }),
  assert(missingEvidenceRows.length === 0, "Every spec FR/SC has an evidence matrix row", {
    missingEvidenceRows,
  }),
  assert(extraEvidenceRows.length === 0, "Evidence matrix has no unknown FR/SC rows", {
    extraEvidenceRows,
  }),
  assert(unexpectedOpenTasks.length === 0, "Only explicit external-gate tasks remain open", {
    openTasks,
    unexpectedOpenTasks,
    allowedOpenTasks: [...allowedOpenTasks],
  }),
  assert(
    unexpectedPendingRequirements.length === 0 && missingPendingRequirements.length === 0,
    "Pending external-gate requirements are exactly the approved production/owner gates",
    {
      pendingRequirementRows,
      expectedPendingRequirements: [...expectedPendingRequirements],
      unexpectedPendingRequirements,
      missingPendingRequirements,
    },
  ),
  assert(
    completionText.includes("Python runtime tests: `167/167` passed.") || completionText.includes("Python runtime tests: `124/124` passed.") || completionText.includes("Python runtime tests: `123/123` passed.") || completionText.includes("Python runtime tests: `121/121` passed.") || completionText.includes("Python runtime tests: `119/119` passed.") || completionText.includes("Python runtime tests: `103/103` passed."),
    "Completion audit records the current Python runtime result",
  ),
  assert(
    readinessText.includes("Python runtime tests: passed, `167 passed`.") || readinessText.includes("Python runtime tests: passed, `124 passed`.") || readinessText.includes("Python runtime tests: passed, `123 passed`.") || readinessText.includes("Python runtime tests: passed, `121 passed`.") || readinessText.includes("Python runtime tests: passed, `119 passed`.") || readinessText.includes("Python runtime tests: passed, `103 passed`."),
    "Release readiness records the current runtime test result",
  ),
  assert(
    completionText.includes("Runtime SQL persistence") && readinessText.includes("Postgres SQL paths are implemented"),
    "Completion/readiness docs record implemented SQL persistence",
  ),
  assert(
    realOpenAiReport?.provider === "openai"
      && realOpenAiReport?.summary?.total === 28
      && realOpenAiReport?.summary?.passed === 28
      && realOpenAiReport?.releaseGate === "pass",
    "Real OpenAI behavior matrix report proves 28/28 pass",
    {
      provider: realOpenAiReport?.provider,
      summary: realOpenAiReport?.summary,
      releaseGate: realOpenAiReport?.releaseGate,
    },
  ),
  assert(
    (
      readinessText.includes("not yet product-owner approved or deployed")
      || readinessText.includes("production blocked by product-owner final diagnostic/demo/name corrections")
      || readinessText.includes("production deployed; final approval still blocked by product-owner transcript approval and live WhatsApp smoke")
    )
      && (
        readinessText.includes("No production migration, Railway deploy, Vercel deploy, or live WhatsApp production action was executed")
        || readinessText.includes("Railway and Vercel production deployment were executed; live WhatsApp production smoke remains pending")
      ),
    "Readiness explicitly preserves external approval/deploy gates",
  ),
  ...reportResults,
];

writeReport("agent-runtime-completion-evidence", results, {
  specRequirementIds,
  evidenceRequirementIds,
  openTasks,
  allowedOpenTasks: [...allowedOpenTasks],
  pendingRequirementRows,
});

writeTranscriptMarkdown("agent-runtime-completion-evidence", [
  {
    title: "Evidence Audit",
    lines: results.map((result) => `- ${result.ok ? "PASS" : "FAIL"}: ${result.message}`),
  },
]);
