import { execFileSync } from "node:child_process";
import fs from "node:fs";
import Module from "node:module";
import path from "node:path";

const root = process.cwd();
const feature = "011-taliya-commercial-agent-core-reset";
const task = "T011-098";
const reportDir = path.join(root, "specs", feature, "eval-reports");

const publicEntrypoints = [
  "app/api/landing/ai-attendant/route.ts",
  "app/api/landing/ai-attendant/whatsapp/route.ts",
  "lib/landing/floating-agent.ts",
  "lib/landing/ai-attendant/runtime-client.ts",
];

const forbiddenPublicModules = new Set([
  "lib/landing/ai-attendant/agent-v2-loop.ts",
  "lib/landing/ai-attendant/agent-v2-response-generator.ts",
  "lib/landing/ai-attendant/agent-v2-semantic-interpreter.ts",
  "lib/landing/ai-attendant/agent-v2-orchestrator.ts",
  "lib/landing/ai-attendant/agent-v2-tools.ts",
  "lib/landing/ai-attendant/provider.ts",
  "lib/landing/ai-attendant/fallback.ts",
]);

const allowedLegacyOperationalModules = new Set([
  "lib/landing/ai-attendant/agent-v2-idempotency.ts",
]);

const protectedPaths = [
  "app/pilates",
  "components/landing",
  "data/landing",
  "lib/landing/floating-agent.ts",
  "components/internal/SalesInboxClient.tsx",
];

function readText(relativePath) {
  return fs.readFileSync(path.join(root, relativePath), "utf8").replace(/^\uFEFF/, "");
}

function walkFiles(relativeDir, extensions = new Set([".py"])) {
  const dir = path.join(root, relativeDir);
  const files = [];
  for (const item of fs.readdirSync(dir, { withFileTypes: true })) {
    const absolute = path.join(dir, item.name);
    const relative = path.relative(root, absolute).replaceAll("\\", "/");
    if (item.isDirectory()) {
      files.push(...walkFiles(relative, extensions));
    } else if (extensions.has(path.extname(item.name))) {
      files.push(relative);
    }
  }
  return files;
}

function lineHits(relativePath, regex) {
  return readText(relativePath)
    .split(/\r?\n/)
    .flatMap((line, index) => (regex.test(line) ? [{ path: relativePath, line: index + 1, text: line.trim() }] : []));
}

function importSpecifiers(source) {
  const specs = [];
  const importRegex = /\bimport\s+(?:type\s+)?(?:[^'"]+?\s+from\s+)?["']([^"']+)["']/g;
  let match;
  while ((match = importRegex.exec(source))) {
    specs.push(match[1]);
  }
  return specs;
}

function resolveImport(fromPath, specifier) {
  if (specifier.startsWith("@/")) {
    return resolveExisting(specifier.slice(2));
  }
  if (!specifier.startsWith(".")) return null;
  const base = path.posix.join(path.posix.dirname(fromPath.replaceAll("\\", "/")), specifier);
  return resolveExisting(base);
}

function resolveExisting(base) {
  const normalizedBase = base.replaceAll("\\", "/").replace(/^\.\//, "");
  const candidates = [
    normalizedBase,
    `${normalizedBase}.ts`,
    `${normalizedBase}.tsx`,
    `${normalizedBase}.mjs`,
    path.posix.join(normalizedBase, "index.ts"),
    path.posix.join(normalizedBase, "index.tsx"),
  ];
  return candidates.find((candidate) => fs.existsSync(path.join(root, candidate))) ?? null;
}

function reachableFrom(entrypoint) {
  const visited = new Set();
  const stack = [{ path: entrypoint, via: [] }];
  const forbiddenHits = [];

  while (stack.length) {
    const current = stack.pop();
    if (!current || visited.has(current.path)) continue;
    visited.add(current.path);

    if (forbiddenPublicModules.has(current.path)) {
      forbiddenHits.push({ path: current.path, via: current.via });
      continue;
    }

    const source = readText(current.path);
    for (const specifier of importSpecifiers(source)) {
      const resolved = resolveImport(current.path, specifier);
      if (!resolved) continue;
      if (allowedLegacyOperationalModules.has(resolved)) continue;
      stack.push({ path: resolved, via: [...current.via, { from: current.path, to: resolved }] });
    }
  }

  return { entrypoint, visited: [...visited].sort(), forbiddenHits };
}

function protectedSourceDiff() {
  try {
    const output = execFileSync(
      "git",
      [
        "-c",
        "safe.directory=C:/Users/lucas/agentes-landing-system",
        "diff",
        "--name-only",
        "--",
        ...protectedPaths,
      ],
      { cwd: root, encoding: "utf8" },
    );
    return output.split(/\r?\n/).map((line) => line.trim()).filter(Boolean);
  } catch (error) {
    return [`git_diff_failed:${error instanceof Error ? error.message : String(error)}`];
  }
}

function result(ok, message, details = {}) {
  return { ok: Boolean(ok), message, details };
}

const settingsPath = "services/taliya-agent-runtime/app/settings.py";
const mainPath = "services/taliya-agent-runtime/app/main.py";
const runtimeClientPath = "lib/landing/ai-attendant/runtime-client.ts";
const testSettingsPath = "services/taliya-agent-runtime/tests/test_settings.py";
const testApiPath = "services/taliya-agent-runtime/tests/test_agent_runs_api.py";
const widgetAdapterTestPath = "scripts/eval-agent-runtime-spec011-widget-adapter.mjs";

const settingsText = readText(settingsPath);
const mainText = readText(mainPath);
const runtimeClientText = readText(runtimeClientPath);
const testSettingsText = readText(testSettingsPath);
const testApiText = readText(testApiPath);
const widgetAdapterTestText = readText(widgetAdapterTestPath);
const coreFiles = walkFiles("services/taliya-agent-runtime/app/core/taliya_commercial");

const runCoreIndex = mainText.indexOf("result = await run_spec011_agent_turn(");
const disabledCheckIndex = mainText.indexOf("if not current.spec011_commercial_core_enabled:");
const fetchIndex = runtimeClientText.indexOf("await fetch(");
const clientDisabledCheckIndex = runtimeClientText.indexOf("if (!isSpec011CommercialCoreEnabled())");

const mainRunnerHits = [
  ...lineHits(mainPath, /\bfrom app\.runtime\.runner import\b/),
  ...lineHits(mainPath, /\brun_agent_turn\b/),
];
const coreRunnerHits = coreFiles.flatMap((file) =>
  lineHits(file, /\bfrom app\.runtime\.runner import\b|\bapp\.runtime\.runner\b|\brun_agent_turn\b/),
);
const reachability = publicEntrypoints.map(reachableFrom);
const forbiddenReachability = reachability.flatMap((entry) =>
  entry.forbiddenHits.map((hit) => ({ entrypoint: entry.entrypoint, ...hit })),
);
const protectedDiff = protectedSourceDiff();

const results = [
  result(
    settingsText.includes("spec011_commercial_core_enabled") &&
      settingsText.includes('alias="TALIYA_SPEC011_COMMERCIAL_CORE_ENABLED"'),
    "runtime settings expose an explicit Spec 011 commercial core rollback flag",
    { settingsPath },
  ),
  result(
    disabledCheckIndex >= 0 &&
      runCoreIndex >= 0 &&
      disabledCheckIndex < runCoreIndex &&
      mainText.includes('"spec011_core_disabled"') &&
      mainText.includes("retryable=True"),
    "runtime API returns controlled operational error before running the core when flag is disabled",
    { mainPath, disabledCheckIndex, runCoreIndex },
  ),
  result(
    clientDisabledCheckIndex >= 0 &&
      fetchIndex >= 0 &&
      clientDisabledCheckIndex < fetchIndex &&
      runtimeClientText.includes('createOperationalFallbackResponse("spec011_core_disabled", request)'),
    "public runtime client short-circuits to operational fallback before fetch when flag is disabled",
    { runtimeClientPath, clientDisabledCheckIndex, fetchIndex },
  ),
  result(
    mainRunnerHits.length === 0 && coreRunnerHits.length === 0,
    "rollback path does not import or call the old Python runner",
    { mainRunnerHits, coreRunnerHits },
  ),
  result(
    forbiddenReachability.length === 0,
    "public widget/WhatsApp paths still cannot reach old TS v2 commercial modules",
    { forbiddenReachability, allowedLegacyOperationalModules: [...allowedLegacyOperationalModules] },
  ),
  result(
    testSettingsText.includes("test_spec011_commercial_core_can_be_disabled_by_explicit_rollback_flag") &&
      testApiText.includes("test_spec011_core_disabled_returns_operational_error_without_running_core") &&
      testApiText.includes("test_agent_run_keeps_legacy_endpoint_quarantined_when_spec011_core_disabled") &&
      widgetAdapterTestText.includes("rollback flag returns operational fallback without fetching widget runtime") &&
      widgetAdapterTestText.includes("rollback flag returns operational fallback without fetching WhatsApp runtime"),
    "rollback behavior is covered by settings, runtime API, widget, and WhatsApp tests",
    { testSettingsPath, testApiPath, widgetAdapterTestPath },
  ),
  result(
    protectedDiff.length === 0,
    "rollback implementation produced no protected /pilates, landing visual, floating-agent, or Sales Inbox UI source diff",
    { protectedDiff, protectedPaths },
  ),
];

fs.mkdirSync(reportDir, { recursive: true });
const summary = {
  total: results.length,
  passed: results.filter((item) => item.ok).length,
  failed: results.filter((item) => !item.ok).length,
};
const report = {
  runId: `agent-runtime-spec011-rollback-${Date.now()}`,
  feature,
  task,
  createdAt: new Date().toISOString(),
  summary,
  releaseGate: summary.failed === 0 ? "pass" : "fail",
  checkedFiles: [
    settingsPath,
    mainPath,
    runtimeClientPath,
    testSettingsPath,
    testApiPath,
    widgetAdapterTestPath,
  ],
  publicEntrypoints,
  forbiddenPublicModules: [...forbiddenPublicModules].sort(),
  reachability,
  results,
};

const jsonPath = path.join(reportDir, "agent-runtime-spec011-rollback.json");
const mdPath = path.join(reportDir, "agent-runtime-spec011-rollback.md");
fs.writeFileSync(jsonPath, `${JSON.stringify(report, null, 2)}\n`);
fs.writeFileSync(
  mdPath,
  [
    "# agent-runtime-spec011-rollback",
    "",
    `Generated at: ${report.createdAt}`,
    `Release gate: ${report.releaseGate}`,
    `Passed: ${summary.passed}/${summary.total}`,
    "",
    ...results.flatMap((item) => [
      `## ${item.ok ? "PASS" : "FAIL"} ${item.message}`,
      "",
      "```json",
      JSON.stringify(item.details ?? {}, null, 2),
      "```",
      "",
    ]),
  ].join("\n").trim() + "\n",
);

if (summary.failed > 0) {
  console.error(`agent-runtime-spec011-rollback: ${summary.failed} failure(s). Report: ${jsonPath}`);
  process.exitCode = 1;
} else {
  console.log(`agent-runtime-spec011-rollback: ${summary.passed}/${summary.total} passed. Report: ${jsonPath}`);
}
