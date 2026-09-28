import fs from "node:fs";
import path from "node:path";

const root = process.cwd();
const feature = "011-taliya-commercial-agent-core-reset";
const reportDir = path.join(root, "specs", feature, "eval-reports");
const reportName = "agent-runtime-spec011-fixture-inventory";

const goldenFixturePath = path.join(
  root,
  "scripts",
  "fixtures",
  "agent-runtime",
  "spec-011-golden-transcripts.json",
);
const doNotDoFixturePath = path.join(
  root,
  "scripts",
  "fixtures",
  "agent-runtime",
  "spec-011-do-not-do-runtime.json",
);
const regressionCasesPath = path.join(
  root,
  "specs",
  feature,
  "regression-cases.md",
);

const requiredGolden = [
  ["price", "final-price-first"],
  ["price_plus_pain", "final-price-plus-pain"],
  ["pain_first", "final-pain-first"],
  ["instagram_source", "final-instagram-interest"],
  ["whatsapp_product", "final-whatsapp-question"],
  ["diagnostic_and_long_conversation", "step3g-long-conversation"],
  ["waitlist", "final-waitlist-joined"],
  ["human_handoff", "final-human-request-silent-after"],
  ["product_demo", "final-demo-request"],
];

const requiredDoNotDo = [
  ["early_phone_capture", "do-not-do-early-phone-capture"],
  ["invented_checkout", "final-checkout-buy-intent"],
  ["invented_date_vip_discount", "do-not-do-date-vip-discount"],
  ["invented_integrations", "product-delta-integration-scope"],
  ["invented_certifications_security", "product-delta-security-data"],
  ["client_studio_whatsapp_capture", "do-not-do-client-studio-whatsapp-capture"],
  ["wrong_student_language", "do-not-do-wrong-student-language"],
  ["price_497_not_student_count", "spec011-rc003-price-497-not-student-count"],
];

function readJson(filePath) {
  return JSON.parse(fs.readFileSync(filePath, "utf8"));
}

function readText(filePath) {
  return fs.readFileSync(filePath, "utf8");
}

function result(ok, message, details = {}) {
  return { ok: Boolean(ok), message, details };
}

function fixtureIds(fixture) {
  return new Set(fixture.map((item) => item.id));
}

function duplicateIds(fixture) {
  const seen = new Set();
  const duplicates = new Set();
  for (const item of fixture) {
    if (seen.has(item.id)) {
      duplicates.add(item.id);
    }
    seen.add(item.id);
  }
  return [...duplicates].sort();
}

function missingRequired(required, ids) {
  return required
    .filter(([, id]) => !ids.has(id))
    .map(([category, id]) => ({ category, id }));
}

function schemaVersions(fixture) {
  return [...new Set(fixture.map((item) => item.fixture_schema_version))].sort();
}

function regressionCaseIds(markdown) {
  const ids = [];
  const pattern = /\|\s*(RC-011-[0-9]{3}[A-Z]?)\s*\|/g;
  let match = pattern.exec(markdown);
  while (match) {
    ids.push(match[1]);
    match = pattern.exec(markdown);
  }
  return ids;
}

function duplicateValues(values) {
  const seen = new Set();
  const duplicates = new Set();
  for (const value of values) {
    if (seen.has(value)) {
      duplicates.add(value);
    }
    seen.add(value);
  }
  return [...duplicates].sort();
}

function fixtureCaseIds(fixture, field) {
  return [
    ...new Set(
      fixture.flatMap((item) => item[field] ?? []).map((item) => String(item)),
    ),
  ].sort();
}

const golden = readJson(goldenFixturePath);
const doNotDo = readJson(doNotDoFixturePath);
const regressionCases = readText(regressionCasesPath);
const goldenIds = fixtureIds(golden);
const doNotDoIds = fixtureIds(doNotDo);
const regressionIds = regressionCaseIds(regressionCases);
const regressionIdSet = new Set(regressionIds);
const referencedCaseIds = [
  ...new Set([
    ...fixtureCaseIds(golden, "golden_case_ids"),
    ...fixtureCaseIds(doNotDo, "do_not_do_case_ids"),
  ]),
].sort();
const painFirst = golden.find((item) => item.id === "final-pain-first");
const painFirstMustNot =
  painFirst?.expected?.rendered_text_must_not_include?.map((item) =>
    String(item).toLowerCase(),
  ) ?? [];

const results = [
  result(
    duplicateIds(golden).length === 0 && duplicateIds(doNotDo).length === 0,
    "fixtures have unique scenario ids",
    {
      goldenDuplicates: duplicateIds(golden),
      doNotDoDuplicates: duplicateIds(doNotDo),
    },
  ),
  result(
    schemaVersions(golden).length === 1 &&
      schemaVersions(golden)[0] === "011.golden_transcript.v1",
    "golden fixtures use the expected versioned schema",
    { schemaVersions: schemaVersions(golden) },
  ),
  result(
    schemaVersions(doNotDo).length === 1 &&
      schemaVersions(doNotDo)[0] === "011.do_not_do_runtime.v1",
    "do-not-do fixtures use the expected versioned schema",
    { schemaVersions: schemaVersions(doNotDo) },
  ),
  result(
    duplicateValues(regressionIds).length === 0,
    "regression-case IDs are unique",
    {
      duplicateRegressionCaseIds: duplicateValues(regressionIds),
      count: regressionIds.length,
    },
  ),
  result(
    referencedCaseIds.every((id) => regressionIdSet.has(id)),
    "fixture case references exist in regression-cases.md",
    {
      referencedCaseIds,
      missing: referencedCaseIds.filter((id) => !regressionIdSet.has(id)),
    },
  ),
  result(
    missingRequired(requiredGolden, goldenIds).length === 0,
    "golden fixture covers all required T011-019 flow categories",
    {
      requiredGolden,
      missing: missingRequired(requiredGolden, goldenIds),
      count: golden.length,
    },
  ),
  result(
    missingRequired(requiredDoNotDo, doNotDoIds).length === 0,
    "do-not-do fixture covers all required T011-019A forbidden-behavior categories",
    {
      requiredDoNotDo,
      missing: missingRequired(requiredDoNotDo, doNotDoIds),
      count: doNotDo.length,
    },
  ),
  result(
    ["lead loses", "interested leads", "team takes too long"].every((phrase) =>
      painFirstMustNot.includes(phrase),
    ),
    "pain-first golden explicitly blocks translated English feedback leaks",
    { painFirstMustNot },
  ),
];

const failed = results.filter((item) => !item.ok);
const report = {
  feature,
  name: reportName,
  releaseGate: failed.length === 0 ? "pass" : "fail",
  paidOpenAiSpend: 0,
  summary: {
    total: results.length,
    passed: results.length - failed.length,
    failed: failed.length,
    goldenCount: golden.length,
    doNotDoCount: doNotDo.length,
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
];
for (const item of results) {
  lines.push(`## ${item.ok ? "PASS" : "FAIL"} ${item.message}`, "");
  lines.push("```json");
  lines.push(JSON.stringify(item.details, null, 2));
  lines.push("```", "");
}
const mdPath = path.join(reportDir, `${reportName}.md`);
fs.writeFileSync(mdPath, `${lines.join("\n").trim()}\n`);

console.log(
  `agent-runtime-spec011-fixture-inventory: ${report.summary.passed}/${report.summary.total} passed`,
);
console.log(`Release gate: ${report.releaseGate}`);
console.log(`Report JSON: ${jsonPath}`);
console.log(`Report MD: ${mdPath}`);

if (report.releaseGate !== "pass") {
  process.exitCode = 1;
}
