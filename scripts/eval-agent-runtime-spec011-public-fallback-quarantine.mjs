import fs from "node:fs";
import path from "node:path";

const root = process.cwd();
const reportDir = path.join(root, "specs", "011-taliya-commercial-agent-core-reset", "eval-reports");

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

function readText(relativePath) {
  return fs.readFileSync(path.join(root, relativePath), "utf8").replace(/^\uFEFF/, "");
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
  const edges = [];
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
      edges.push({ from: current.path, specifier, to: resolved });
      if (allowedLegacyOperationalModules.has(resolved)) continue;
      stack.push({ path: resolved, via: [...current.via, { from: current.path, to: resolved }] });
    }
  }

  return { entrypoint, visited: [...visited].sort(), edges, forbiddenHits };
}

function lineHits(relativePath, regex) {
  return readText(relativePath)
    .split(/\r?\n/)
    .flatMap((line, index) => (regex.test(line) ? [{ line: index + 1, text: line.trim() }] : []));
}

function result(ok, message, details = {}) {
  return { ok: Boolean(ok), message, details };
}

const reachability = publicEntrypoints.map(reachableFrom);
const forbiddenReachability = reachability.flatMap((entry) =>
  entry.forbiddenHits.map((hit) => ({ entrypoint: entry.entrypoint, ...hit })),
);
const runtimeClient = "lib/landing/ai-attendant/runtime-client.ts";
const runtimeLegacyPayloadHits = [
  ...lineHits(runtimeClient, /\bcreateRuntimeRequestBody\b/),
  ...lineHits(runtimeClient, /\binferClientPendingContext\b/),
  ...lineHits(runtimeClient, /\bclient_pending_context\s*:/),
  ...lineHits(runtimeClient, /\bcommercial_route\s*:/),
  ...lineHits(runtimeClient, /\btemplate_id\s*:/),
];
const runtimeStripHits = lineHits(runtimeClient, /client_pending_context|commercial_route|template_id/);

const results = [
  result(
    forbiddenReachability.length === 0,
    "public widget/WhatsApp paths cannot reach old TS v2 commercial fallback modules",
    { forbiddenReachability, allowedLegacyOperationalModules: [...allowedLegacyOperationalModules] },
  ),
  result(
    runtimeLegacyPayloadHits.length === 0,
    "runtime client public turn path has no legacy commercial payload builder or hints",
    { runtimeLegacyPayloadHits },
  ),
  result(
    runtimeStripHits.length > 0,
    "runtime client still strips legacy commercial hints from supplied metadata",
    { runtimeStripHits },
  ),
  result(
    readText(runtimeClient).includes('return "/v1/taliya-commercial/turn"'),
    "runtime client commercial turn endpoint is fixed to the Spec 011 API",
  ),
];

fs.mkdirSync(reportDir, { recursive: true });
const summary = {
  total: results.length,
  passed: results.filter((item) => item.ok).length,
  failed: results.filter((item) => !item.ok).length,
};
const report = {
  runId: `agent-runtime-spec011-public-fallback-quarantine-${Date.now()}`,
  feature: "011-taliya-commercial-agent-core-reset",
  task: "T011-092",
  createdAt: new Date().toISOString(),
  summary,
  releaseGate: summary.failed === 0 ? "pass" : "fail",
  publicEntrypoints,
  forbiddenPublicModules: [...forbiddenPublicModules].sort(),
  reachability,
  results,
};

const jsonPath = path.join(reportDir, "agent-runtime-spec011-public-fallback-quarantine.json");
const mdPath = path.join(reportDir, "agent-runtime-spec011-public-fallback-quarantine.md");
fs.writeFileSync(jsonPath, `${JSON.stringify(report, null, 2)}\n`);
fs.writeFileSync(
  mdPath,
  [
    "# agent-runtime-spec011-public-fallback-quarantine",
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
  console.error(`agent-runtime-spec011-public-fallback-quarantine: ${summary.failed} failure(s). Report: ${jsonPath}`);
  process.exitCode = 1;
} else {
  console.log(`agent-runtime-spec011-public-fallback-quarantine: ${summary.passed}/${summary.total} passed. Report: ${jsonPath}`);
}
