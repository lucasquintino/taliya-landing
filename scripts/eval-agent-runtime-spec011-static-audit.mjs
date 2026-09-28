import { execFileSync } from "node:child_process";
import fs from "node:fs";
import path from "node:path";

const root = process.cwd();
const featureName = "011-taliya-commercial-agent-core-reset";
const task = "T011-100";
const reportDir = path.join(root, "specs", featureName, "eval-reports");

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

const activePythonCoreDir = "services/taliya-agent-runtime/app/core/taliya_commercial";
const activePythonPaths = [
  "services/taliya-agent-runtime/app/main.py",
  "services/taliya-agent-runtime/app/settings.py",
  "services/taliya-agent-runtime/app/runtime/schemas.py",
  ...walkFiles(activePythonCoreDir, new Set([".py"])),
];

const activeTsPaths = unique([
  ...publicEntrypoints,
  "lib/landing/ai-attendant/runtime-client.ts",
]);

const activeProductFactSurfaces = [
  "services/taliya-agent-runtime/app/core/taliya_commercial/conductor.py",
  "services/taliya-agent-runtime/app/core/taliya_commercial/conductor_policy.py",
  "services/taliya-agent-runtime/app/core/taliya_commercial/context_builder.py",
  "services/taliya-agent-runtime/app/core/taliya_commercial/fallback.py",
  "services/taliya-agent-runtime/app/core/taliya_commercial/renderer.py",
  "services/taliya-agent-runtime/app/core/taliya_commercial/repair.py",
  "services/taliya-agent-runtime/app/core/taliya_commercial/runtime_adapter.py",
  "services/taliya-agent-runtime/app/core/taliya_commercial/runtime_state.py",
  "services/taliya-agent-runtime/app/core/taliya_commercial/sales_inbox_projection.py",
  "services/taliya-agent-runtime/app/core/taliya_commercial/template_registry.py",
  "lib/landing/ai-attendant/runtime-client.ts",
];

const legacyReferencePaths = existingFiles([
  "services/taliya-agent-runtime/app/runtime/runner.py",
  "services/taliya-agent-runtime/app/domains/taliya_commercial/templates.py",
  "services/taliya-agent-runtime/app/domains/taliya_commercial/prompts.py",
  "services/taliya-agent-runtime/app/domains/taliya_commercial/behavior_policy.py",
  "services/taliya-agent-runtime/app/domains/taliya_commercial/renderer.py",
  "lib/landing/ai-attendant/agent-v2-response-generator.ts",
  "lib/landing/ai-attendant/agent-v2-loop.ts",
]);

const commercialBranchRegex =
  /\b(if|elif|case)\b.{0,140}(pre[cç]o|quanto custa|plano|demo|demonstra[cç][aã]o|diagn[oó]stic|waitlist|lista de espera|instagram|dor|pain|como funciona|alunos|students|whatsapp|obje[cç][aã]o|objection)/i;
const productFactRegex =
  /(R\$\s*(197|497|897|1\.497)|checkout seguro|link de pagamento|checkout para (assinar|fechar|comprar)|integra[cç][aã]o garantida|certifica[cç][aã]o|criptografia garantida|desconto garantido|vip garantido)/i;
const genericWholeResponseRegex = /\b(message_text|freeform_response|assistant_reply)\b/i;

function readText(relativePath) {
  return fs.readFileSync(path.join(root, relativePath), "utf8").replace(/^\uFEFF/, "");
}

function existingFiles(paths) {
  return paths.filter((relativePath) => fs.existsSync(path.join(root, relativePath)));
}

function walkFiles(relativeDir, extensions) {
  const dir = path.join(root, relativeDir);
  if (!fs.existsSync(dir)) return [];
  const files = [];
  for (const item of fs.readdirSync(dir, { withFileTypes: true })) {
    const absolute = path.join(dir, item.name);
    const relative = path.relative(root, absolute).replaceAll("\\", "/");
    if (item.isDirectory()) {
      if (item.name === "__pycache__") continue;
      files.push(...walkFiles(relative, extensions));
    } else if (extensions.has(path.extname(item.name))) {
      files.push(relative);
    }
  }
  return files.sort();
}

function lineHits(relativePath, regex, { max = 50 } = {}) {
  if (!fs.existsSync(path.join(root, relativePath))) return [];
  const hits = [];
  const lines = readText(relativePath).split(/\r?\n/);
  lines.forEach((line, index) => {
    regex.lastIndex = 0;
    if (regex.test(line)) {
      hits.push({
        path: relativePath,
        line: index + 1,
        text: line.trim().slice(0, 240),
      });
    }
  });
  return hits.slice(0, max);
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

function sliceFunction(source, functionName) {
  const start = source.indexOf(`function ${functionName}`);
  if (start < 0) return "";
  const nextFunction = source.indexOf("\nfunction ", start + 10);
  return source.slice(start, nextFunction < 0 ? undefined : nextFunction);
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

function unique(values) {
  return [...new Set(values)].sort();
}

function result(ok, message, details = {}) {
  return { ok: Boolean(ok), message, details };
}

function writeReport(name, results, extra = {}) {
  fs.mkdirSync(reportDir, { recursive: true });
  const summary = {
    total: results.length,
    passed: results.filter((item) => item.ok).length,
    failed: results.filter((item) => !item.ok).length,
  };
  const report = {
    runId: `${name}-${Date.now()}`,
    feature: featureName,
    task,
    createdAt: new Date().toISOString(),
    summary,
    results,
    releaseGate: summary.failed === 0 ? "pass" : "fail",
    ...extra,
  };
  const jsonPath = path.join(reportDir, `${name}.json`);
  fs.writeFileSync(jsonPath, `${JSON.stringify(report, null, 2)}\n`);

  const mdPath = path.join(reportDir, `${name}.md`);
  const lines = [
    `# ${name}`,
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
  ];
  fs.writeFileSync(mdPath, `${lines.join("\n").trim()}\n`);

  if (summary.failed > 0) {
    console.error(`${name}: ${summary.failed} failure(s). Report: ${jsonPath}`);
    for (const item of results.filter((entry) => !entry.ok)) {
      console.error(`- ${item.message}`);
    }
    process.exitCode = 1;
  } else {
    console.log(`${name}: ${summary.passed}/${summary.total} passed. Report: ${jsonPath}`);
  }
}

const reachability = publicEntrypoints.map(reachableFrom);
const forbiddenReachability = reachability.flatMap((entry) =>
  entry.forbiddenHits.map((hit) => ({ entrypoint: entry.entrypoint, ...hit })),
);

const mainText = readText("services/taliya-agent-runtime/app/main.py");
const runtimeAdapterText = readText("services/taliya-agent-runtime/app/core/taliya_commercial/runtime_adapter.py");
const runtimeClientText = readText("lib/landing/ai-attendant/runtime-client.ts");
const conversionPathFunction = sliceFunction(runtimeClientText, "conversionPathFromRuntime");
const endpointFunction = sliceFunction(runtimeClientText, "resolveTaliyaCommercialRuntimeEndpointPath");
const requestBodyFunction = sliceFunction(runtimeClientText, "buildSpec011RuntimeRequestBody");

const activeRunnerHits = [
  ...lineHits("services/taliya-agent-runtime/app/main.py", /\bfrom app\.runtime\.runner import\b|\bapp\.runtime\.runner\b|\brun_agent_turn\b/),
  ...walkFiles(activePythonCoreDir, new Set([".py"])).flatMap((file) =>
    lineHits(file, /\bfrom app\.runtime\.runner import\b|\bapp\.runtime\.runner\b|\brun_agent_turn\b/),
  ),
];

const runtimeClientLegacyHintHits = [
  ...lineHits("lib/landing/ai-attendant/runtime-client.ts", /\bcreateRuntimeRequestBody\b|\binferClientPendingContext\b|\bclient_pending_context\s*:|\bcommercial_route\s*:|\btemplate_id\s*:/),
].filter((hit) => !hit.text.includes("delete cleanMetadata.client_pending_context"));

const activeProductFactHits = existingFiles(activeProductFactSurfaces).flatMap((relativePath) =>
  lineHits(relativePath, productFactRegex).map((hit) => ({
    ...hit,
    classification: "active_surface",
  })),
);

const legacyReferenceProductFactHits = legacyReferencePaths.flatMap((relativePath) =>
  lineHits(relativePath, productFactRegex, { max: 20 }).map((hit) => ({
    ...hit,
    classification: "legacy_reference_not_active_path",
  })),
);

const genericWholeResponseActiveHits = [
  ...lineHits("services/taliya-agent-runtime/app/core/taliya_commercial/template_registry.py", genericWholeResponseRegex),
  ...lineHits("services/taliya-agent-runtime/app/core/taliya_commercial/renderer.py", genericWholeResponseRegex),
  ...lineHits("services/taliya-agent-runtime/app/core/taliya_commercial/runtime_adapter.py", genericWholeResponseRegex),
];

const genericWholeResponseGuardHits = [
  ...lineHits("services/taliya-agent-runtime/app/core/taliya_commercial/schemas.py", genericWholeResponseRegex),
  ...lineHits("services/taliya-agent-runtime/app/core/taliya_commercial/conductor.py", genericWholeResponseRegex),
  ...lineHits("services/taliya-agent-runtime/app/core/taliya_commercial/failed_path_guards.py", genericWholeResponseRegex),
];

const rendererDefaultHits = [
  ...lineHits(
    "services/taliya-agent-runtime/app/core/taliya_commercial/renderer.py",
    /(pain_context_human|first_recommended_step|plan_or_range_to_compare).{0,120}(\bor\b|default|fallback|or\s+["'])/i,
  ),
  ...lineHits(
    "services/taliya-agent-runtime/app/core/taliya_commercial/template_registry.py",
    /(pain_context_human|first_recommended_step|plan_or_range_to_compare).{0,120}(\bor\b|default|fallback|or\s+["'])/i,
  ),
];

const conductIndex = runtimeAdapterText.indexOf("conductor_result = await conduct_turn(");
const validateIndex = runtimeAdapterText.indexOf("validator_result = validate_conductor_result(");
const renderIndex = runtimeAdapterText.indexOf("rendered_messages = render_validated_template_plan(");
const stateDiffIndex = runtimeAdapterText.indexOf("runtime_state_diff = build_runtime_state_diff(");
const preConductRuntimeAdapter = runtimeAdapterText.slice(0, Math.max(conductIndex, 0));
const runtimeAdapterCommercialBranchHits = preConductRuntimeAdapter
  .split(/\r?\n/)
  .flatMap((line, index) => {
    commercialBranchRegex.lastIndex = 0;
    return commercialBranchRegex.test(line)
      ? [
          {
            path: "services/taliya-agent-runtime/app/core/taliya_commercial/runtime_adapter.py",
            line: index + 1,
            text: line.trim().slice(0, 240),
          },
        ]
      : [];
  });
const persistStartIndex = runtimeAdapterText.indexOf("async def _persist_turn");
const persistStartLine =
  persistStartIndex >= 0 ? runtimeAdapterText.slice(0, persistStartIndex).split(/\r?\n/).length : Number.MAX_SAFE_INTEGER;
const runtimeAdapterMessageTextHits = lineHits(
  "services/taliya-agent-runtime/app/core/taliya_commercial/runtime_adapter.py",
  /request\.message\.text/,
).filter((hit) => hit.line < persistStartLine);

const conversionPathTextParsingHits = /\brequest\b|userMessage|lastUserMessage|normalizeRuntimeText|\.test\(|\.match\(/.test(
  conversionPathFunction,
)
  ? [{ function: "conversionPathFromRuntime", body: conversionPathFunction.slice(0, 800) }]
  : [];

const endpointOk = endpointFunction.includes('return "/v1/taliya-commercial/turn"');

const requestBodyLegacyHints =
  /client_pending_context|commercial_route\s*:|template_id\s*:/.test(requestBodyFunction)
    ? [{ function: "buildSpec011RuntimeRequestBody", body: requestBodyFunction.slice(0, 1200) }]
    : [];

const protectedDiff = protectedSourceDiff();

const results = [
  result(
    activeRunnerHits.length === 0 &&
      mainText.includes("legacy_commercial_runner_quarantined") &&
      mainText.includes('"/v1/taliya-commercial/turn"'),
    "active runtime API and Spec 011 core do not import/call runtime/runner.py for commercial answering",
    { activeRunnerHits },
  ),
  result(
    forbiddenReachability.length === 0 &&
      endpointOk &&
      runtimeClientLegacyHintHits.length === 0 &&
      requestBodyLegacyHints.length === 0,
    "public widget/WhatsApp entrypoints use Spec 011 endpoint and cannot reach old TS v2 commercial fallback",
    {
      forbiddenReachability,
      endpointOk,
      runtimeClientLegacyHintHits,
      requestBodyLegacyHints,
      allowedLegacyOperationalModules: [...allowedLegacyOperationalModules],
    },
  ),
  result(
    conductIndex >= 0 &&
      validateIndex > conductIndex &&
      renderIndex > validateIndex &&
      stateDiffIndex > validateIndex &&
      runtimeAdapterCommercialBranchHits.length === 0 &&
      runtimeAdapterMessageTextHits.length === 0,
    "runtime adapter keeps commercial understanding inside conduct_turn before validation/render/state updates",
    {
      conductIndex,
      validateIndex,
      renderIndex,
      stateDiffIndex,
      runtimeAdapterCommercialBranchHits,
      runtimeAdapterMessageTextHits,
    },
  ),
  result(
    conversionPathTextParsingHits.length === 0,
    "public conversion path is derived from runtime structured output, not user-text regex routing",
    { conversionPathTextParsingHits },
  ),
  result(
    activeProductFactHits.length === 0,
    "active production-path prompts/templates/fallbacks do not hardcode product facts outside official product knowledge or Spec 006",
    { activeProductFactHits, legacyReferenceProductFactHits },
  ),
  result(
    genericWholeResponseActiveHits.length === 0 &&
      genericWholeResponseGuardHits.length > 0,
    "generic whole-response fields are blocked by guards and absent from active renderer/template/runtime output surfaces",
    { genericWholeResponseActiveHits, genericWholeResponseGuardHits },
  ),
  result(
    rendererDefaultHits.length === 0,
    "active renderer/template registry do not invent semantic defaults for missing commercial variables",
    { rendererDefaultHits },
  ),
  result(
    protectedDiff.length === 0,
    "static audit work produced no protected /pilates, landing visual, floating-agent, or Sales Inbox UI source diff",
    { protectedDiff, protectedPaths },
  ),
];

writeReport("agent-runtime-spec011-static-audit", results, {
  auditedFiles: {
    activePythonPaths: existingFiles(activePythonPaths),
    activeTsPaths: existingFiles(activeTsPaths),
    activeProductFactSurfaces: existingFiles(activeProductFactSurfaces),
    legacyReferencePaths,
  },
  publicEntrypoints,
  forbiddenPublicModules: [...forbiddenPublicModules].sort(),
  reachability,
  legacyReferenceFindings: {
    productFactHits: legacyReferenceProductFactHits,
    note:
      "Legacy runner/domain/TS v2 findings remain visible but are not active release-path evidence when runner/public fallback quarantine reports pass.",
  },
});
