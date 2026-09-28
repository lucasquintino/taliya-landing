import fs from "node:fs";
import path from "node:path";
import { spawnSync } from "node:child_process";

import { assert, reportDir, writeReport, writeTranscriptMarkdown } from "./eval-agent-runtime-utils.mjs";

const APP_URL = process.env.AGENT_AUTONOMOUS_APP_URL || "http://127.0.0.1:3999";
const DEMO_URL = "https://www.taliya.com.br/pilates/planos/demonstracao";
const REPORT_NAME = "autonomous-widget-sales-cost-tone-latest";
const ASSET_DIR = path.join(reportDir, "assets", REPORT_NAME);

loadEnvLocal();
fs.mkdirSync(ASSET_DIR, { recursive: true });

const salesToken = process.env.INTERNAL_SALES_INBOX_TOKEN;
const startedAt = new Date().toISOString();

const visual = await runVisualValidation();
const sales = await runConversationScenario({
  id: `autoval-sales-${Date.now()}`,
  title: "Widget -> Sales Inbox complete flow",
  messages: [
    "quanto custa?",
    "quero fazer diagnostico gratuito",
    "tenho 120 alunos, perco interessados no WhatsApp, hoje respondo manualmente, prioridade vendas, urgente agora, quero comparar plano",
    "quero contratar, pode me colocar na lista de espera",
    "pode colocar o Studio Viva em Vitoria ES",
    "quanto custa o Completo?",
    "quero falar com humano",
  ],
});
const salesInbox = await fetchSalesInboxEvidence(sales.leadId);

const costScenarios = [];
for (const scenario of [
  {
    id: `autoval-price-${Date.now()}`,
    title: "Price short lead",
    messages: ["quanto custa?"],
  },
  {
    id: `autoval-demo-${Date.now()}`,
    title: "Demo lead",
    messages: ["quero ver uma demonstracao"],
  },
  {
    id: `autoval-pain-${Date.now()}`,
    title: "Pain-first lead",
    messages: ["perco interessados no WhatsApp porque a equipe demora para responder"],
  },
  {
    id: `autoval-plan-${Date.now()}`,
    title: "Plan fit lead",
    messages: ["qual plano voce recomenda pra mim?"],
  },
  {
    id: `autoval-human-${Date.now()}`,
    title: "Human handoff lead",
    messages: ["quero falar com uma pessoa"],
  },
  {
    id: `autoval-long-${Date.now()}`,
    title: "Long mixed lead",
    messages: [
      "vim pelo instagram e queria entender melhor",
      "tenho agenda meio baguncada e algumas reposicoes se perdem",
      "quanto custa?",
      "pode fazer diagnostico gratuito",
      "tenho 90 alunos, hoje controlo em planilha, prioridade e agenda, urgente agora",
      "quero ver uma demonstracao",
      "qual plano faria mais sentido?",
      "quero contratar quando abrir vaga",
      "pode colocar o Studio Movimento em Campinas SP",
    ],
  },
]) {
  costScenarios.push(await runConversationScenario(scenario));
}

const allConversationScenarios = [sales, ...costScenarios];
const toneReviews = allConversationScenarios.map(reviewTone);
const behaviorReview = reviewMappedBehavior(allConversationScenarios);
const costSummary = summarizeCost(allConversationScenarios);
const results = buildResults({ visual, sales, salesInbox, allConversationScenarios, toneReviews, behaviorReview, costSummary });
const finishedAt = new Date().toISOString();

writeReport(REPORT_NAME, results, {
  startedAt,
  finishedAt,
  appUrl: APP_URL,
  demoUrl: DEMO_URL,
  visual,
  salesInbox,
  costSummary,
  toneReviews,
  behaviorReview,
  scenarios: allConversationScenarios,
});

writeTranscriptMarkdown(REPORT_NAME, buildMarkdownSections({
  visual,
  sales,
  salesInbox,
  costScenarios,
  costSummary,
  toneReviews,
  behaviorReview,
  startedAt,
  finishedAt,
}));

function loadEnvLocal() {
  const envPath = path.join(process.cwd(), ".env.local");
  if (!fs.existsSync(envPath)) return;
  for (const rawLine of fs.readFileSync(envPath, "utf8").split(/\r?\n/)) {
    const line = rawLine.trim();
    if (!line || line.startsWith("#") || !line.includes("=")) continue;
    const [key, ...rest] = line.split("=");
    if (!key || process.env[key]) continue;
    process.env[key] = rest.join("=").trim().replace(/^['"]|['"]$/g, "");
  }
}

async function runVisualValidation() {
  const specPath = path.join(process.cwd(), "scripts", "generated", "autonomous-widget-visual.spec.js");
  const desktopPath = path.join(ASSET_DIR, "widget-demo-desktop.png");
  const mobilePath = path.join(ASSET_DIR, "widget-demo-mobile.png");
  fs.mkdirSync(path.dirname(specPath), { recursive: true });
  fs.writeFileSync(
    specPath,
    `
import { test, expect } from '@playwright/test';

const appUrl = ${JSON.stringify(APP_URL)};
const demoUrl = ${JSON.stringify(DEMO_URL)};
const desktopPath = ${JSON.stringify(desktopPath.replaceAll("\\", "/"))};
const mobilePath = ${JSON.stringify(mobilePath.replaceAll("\\", "/"))};

async function exerciseWidget(page, screenshotPath) {
  await page.goto(appUrl + '/pilates', { waitUntil: 'networkidle' });
  await expect(page.getByLabel('Abrir atendimento')).toBeVisible({ timeout: 20000 });
  await page.getByLabel('Abrir atendimento').click();
  await page.getByPlaceholder('Pergunte sobre planos ou rotina...').fill('quero ver uma demonstracao');
  await page.getByLabel('Enviar mensagem').click();
  const demoAction = page.locator('a[href="' + demoUrl + '"]').first();
  await expect(demoAction).toBeVisible({ timeout: 60000 });
  await page.screenshot({ path: screenshotPath, fullPage: true });
  await expect(demoAction).toContainText(/^Ver demonstra/i);
}

test('desktop widget demo CTA renders', async ({ page }) => {
  await page.setViewportSize({ width: 1365, height: 900 });
  await exerciseWidget(page, desktopPath);
});

test('mobile widget demo CTA renders', async ({ page }) => {
  await page.setViewportSize({ width: 390, height: 844 });
  await exerciseWidget(page, mobilePath);
});
`,
    "utf8",
  );

  const started = Date.now();
  const playwrightSpecPath =
    process.platform === "win32" ? path.relative(process.cwd(), specPath).replaceAll("\\", "/") : specPath.replaceAll("\\", "/");
  const result =
    process.platform === "win32"
      ? spawnSync(
          "powershell.exe",
          ["-NoProfile", "-Command", `npx playwright test '${playwrightSpecPath}' --reporter=json --timeout=120000`],
          { cwd: process.cwd(), encoding: "utf8", timeout: 300000 },
        )
      : spawnSync(
          "npx",
          ["playwright", "test", playwrightSpecPath, "--reporter=json", "--timeout=120000"],
          { cwd: process.cwd(), encoding: "utf8", timeout: 300000 },
        );
  const latencyMs = Date.now() - started;
  const stdout = result.stdout || "";
  let parsed = null;
  try {
    parsed = JSON.parse(stdout.slice(stdout.indexOf("{")));
  } catch {
    parsed = null;
  }
  const failures = [];
  if (result.status !== 0) failures.push("Playwright visual test failed");
  for (const screenshot of [desktopPath, mobilePath]) {
    if (!fs.existsSync(screenshot) || fs.statSync(screenshot).size < 1000) {
      failures.push(`Missing screenshot: ${screenshot}`);
    }
  }
  return {
    ok: failures.length === 0,
    latencyMs,
    failures,
    screenshots: {
      desktop: path.relative(process.cwd(), desktopPath),
      mobile: path.relative(process.cwd(), mobilePath),
    },
    playwright: {
      status: result.status,
      error: result.error?.message,
      stderr: result.stderr,
      stdout: stdout.slice(0, 2000),
      suites: parsed?.suites?.length ?? null,
    },
  };
}

async function runConversationScenario({ id, title, messages }) {
  const sessionId = id;
  const leadId = `lead-${id}`;
  const history = [];
  const turns = [];
  let qualificationDraft = {
    name: "Ana Paula",
    whatsapp: "+5511999999999",
    email: `${id}@example.com`,
  };
  for (let index = 0; index < messages.length; index += 1) {
    const userText = messages[index];
    const userMessage = {
      id: `user-${id}-${index + 1}`,
      role: "user",
      content: userText,
    };
    const body = {
      session: {
        sessionId,
        leadId,
        channel: "web",
        niche: "pilates",
        entryPath: "widget",
        sourceSection: "autonomous_validation",
        sourcePage: "/pilates",
        campaignStage: "commercial",
        publicOfferMode: "direct_saas_subscription",
        messages: [...history, userMessage],
        selectedPainIds: [],
        recommendedAgentIds: [],
        qualificationDraft,
      },
      userMessage: userText,
      pageSignals: {},
    };
    const started = Date.now();
    const response = await fetch(`${APP_URL}/api/landing/ai-attendant`, {
      method: "POST",
      headers: { "content-type": "application/json" },
      body: JSON.stringify(body),
    });
    const latencyMs = Date.now() - started;
    const payload = await response.json().catch(() => ({ error: "invalid_json" }));
    const assistantMessages = Array.isArray(payload.assistantMessages) ? payload.assistantMessages : [];
    history.push(userMessage, ...assistantMessages.map((message, assistantIndex) => ({
      id: message.id || `assistant-${id}-${index + 1}-${assistantIndex + 1}`,
      role: "assistant",
      content: message.content || "",
      intent: message.intent,
      action: message.action,
    })));
    qualificationDraft = {
      ...qualificationDraft,
      ...(payload.qualificationPatch || {}),
    };
    turns.push({
      index: index + 1,
      user: userText,
      httpStatus: response.status,
      latencyMs,
      assistantMessages,
      conversionPath: payload.conversionPath,
      shouldOfferDiagnostic: payload.shouldOfferDiagnostic,
      qualificationPatch: payload.qualificationPatch,
      guardrailDecision: payload.guardrailDecision,
      costUsd: Number(payload.qualificationPatch?.agentRuntimeCostEstimateUsd || 0),
      traceId: payload.qualificationPatch?.agentRuntimeTraceId,
      runId: payload.qualificationPatch?.agentRuntimeRunId,
      currentAgent: payload.qualificationPatch?.agentRuntimeCurrentAgent,
      route: payload.qualificationPatch?.agentRuntimeRoute,
      templateIds: payload.qualificationPatch?.agentRuntimeTemplateIds,
    });
  }
  return {
    id,
    title,
    sessionId,
    leadId,
    turns,
    totals: {
      turns: turns.length,
      costUsd: roundMoney(turns.reduce((sum, turn) => sum + turn.costUsd, 0)),
      latencyMs: turns.reduce((sum, turn) => sum + turn.latencyMs, 0),
      avgLatencyMs: Math.round(turns.reduce((sum, turn) => sum + turn.latencyMs, 0) / Math.max(turns.length, 1)),
      maxLatencyMs: Math.max(...turns.map((turn) => turn.latencyMs)),
    },
  };
}

async function fetchSalesInboxEvidence(leadId) {
  if (!salesToken) {
    return { ok: false, error: "INTERNAL_SALES_INBOX_TOKEN missing in local environment", leadId };
  }
  const headers = { authorization: `Bearer ${salesToken}` };
  const listResponse = await fetch(`${APP_URL}/api/internal/sales-inbox/leads`, { headers });
  const listPayload = await listResponse.json().catch(() => ({}));
  const detailResponse = await fetch(`${APP_URL}/api/internal/sales-inbox/leads/${encodeURIComponent(leadId)}`, { headers });
  const detailPayload = await detailResponse.json().catch(() => ({}));
  const lead = detailPayload.lead;
  return {
    ok: listResponse.ok && detailResponse.ok && Boolean(lead),
    leadId,
    listStatus: listResponse.status,
    detailStatus: detailResponse.status,
    listCount: Array.isArray(listPayload.leads) ? listPayload.leads.length : null,
    lead: lead
      ? {
          leadId: lead.leadId,
          status: lead.status,
          priority: lead.priority,
          channel: lead.channel,
          conversionPath: lead.conversionPath,
          waitlistStatus: lead.waitlistStatus,
          diagnosticStatus: lead.diagnosticStatus,
          commercialStage: lead.commercialStage,
          closureState: lead.closureState,
          humanActive: lead.humanActive,
          aiPaused: lead.aiPaused,
          externalSyncStatus: lead.externalSyncStatus,
          recentMessages: lead.recentMessages || [],
          agentRuntime: lead.agentRuntime,
          contact: lead.contact,
          summary: lead.summary,
          nextAction: lead.nextAction,
        }
      : null,
    auditCount: Array.isArray(detailPayload.audit) ? detailPayload.audit.length : null,
    error: detailPayload.error,
  };
}

function summarizeCost(scenarios) {
  const turns = scenarios.flatMap((scenario) => scenario.turns.map((turn) => ({ ...turn, scenarioId: scenario.id })));
  const totalCostUsd = roundMoney(turns.reduce((sum, turn) => sum + turn.costUsd, 0));
  const latencies = turns.map((turn) => turn.latencyMs).sort((a, b) => a - b);
  const p95LatencyMs = latencies.length ? latencies[Math.min(latencies.length - 1, Math.ceil(latencies.length * 0.95) - 1)] : 0;
  return {
    scenarioCount: scenarios.length,
    turnCount: turns.length,
    totalCostUsd,
    avgCostPerTurnUsd: roundMoney(totalCostUsd / Math.max(turns.length, 1)),
    avgCostPerLeadUsd: roundMoney(totalCostUsd / Math.max(scenarios.length, 1)),
    maxTurnCostUsd: roundMoney(Math.max(...turns.map((turn) => turn.costUsd))),
    totalLatencyMs: turns.reduce((sum, turn) => sum + turn.latencyMs, 0),
    avgLatencyMs: Math.round(turns.reduce((sum, turn) => sum + turn.latencyMs, 0) / Math.max(turns.length, 1)),
    p95LatencyMs,
    maxLatencyMs: Math.max(...turns.map((turn) => turn.latencyMs)),
    mostExpensiveTurn: turns.reduce((max, turn) => (turn.costUsd > max.costUsd ? turn : max), turns[0] || { costUsd: 0 }),
  };
}

function reviewTone(scenario) {
  const text = scenario.turns
    .flatMap((turn) => turn.assistantMessages.map((message) => message.content || ""))
    .join("\n");
  const lowered = text.toLowerCase();
  const failures = [];
  if (!/^oi, [^,\n]+, tudo bem\?|^oi, tudo bem\?/i.test(scenario.turns[0]?.assistantMessages?.[0]?.content || "")) {
    failures.push("first assistant message lacks approved greeting");
  }
  if (text.includes("Pelo que você contou") || text.includes("Pelo que voce contou")) failures.push("uses banned fake-evidence phrasing");
  if (/\b(voce|voces|mes|tambem|nao|prioritaria)\b/i.test(text)) failures.push("assistant copy has unaccented pt-BR words");
  if (/\.\./.test(text)) failures.push("assistant copy has doubled punctuation");
  if (/Eu compararia ainda não dá|Eu compararia ainda nao da|com calma, validando/i.test(text)) {
    failures.push("assistant copy has malformed plan comparison sentence");
  }
  if (/\b(lead reports|lead says|prospects|slow to reply|slow to respond)\b/i.test(text)) {
    failures.push("assistant copy leaked English/internal lead fact phrasing");
  }
  if (/checkout|pagamento/.test(lowered) && !/checkout indispon|não libera|nao libera|sem checkout|não tem checkout|nao tem checkout/.test(lowered)) {
    failures.push("unsafe checkout/payment wording");
  }
  if (scenario.turns.some((turn) => turn.assistantMessages.some((message) => (message.content || "").length > 360))) {
    failures.push("message longer than 360 chars");
  }
  if ((lowered.match(/posso fazer um diagnóstico gratuito|posso fazer um diagnostico gratuito/g) || []).length > 2) {
    failures.push("diagnostic offer repeated too often");
  }
  if (!/[.!?]/.test(text)) failures.push("missing visible punctuation");
  const score = Math.max(1, 5 - failures.length);
  return {
    scenarioId: scenario.id,
    title: scenario.title,
    score,
    ok: failures.length === 0,
    failures,
    notes: failures.length ? "Needs copy/behavior review." : "Tone is concise, punctuated, and commercially aligned.",
  };
}

function reviewMappedBehavior(scenarios) {
  const failures = [];
  const findScenario = (title) => scenarios.find((scenario) => scenario.title === title);
  const textFor = (scenario, turnIndex) =>
    scenario?.turns?.[turnIndex - 1]?.assistantMessages?.map((message) => message.content || "").join("\n") || "";
  const turnFor = (scenario, turnIndex) => scenario?.turns?.[turnIndex - 1];

  const salesScenario = findScenario("Widget -> Sales Inbox complete flow");
  const salesTurn3 = textFor(salesScenario, 3);
  if (!/interessados|WhatsApp|vendas|retorno/i.test(salesTurn3) || /ponto mais crítico|primeira rotina crítica/i.test(salesTurn3)) {
    failures.push({
      scenario: salesScenario?.title,
      turn: 3,
      issue: "diagnostic delivery did not use the lead facts with enough specificity",
      observed: salesTurn3,
    });
  }

  const salesTurn4 = textFor(salesScenario, 4);
  if (!/lista de espera|vaga|dados|studio/i.test(salesTurn4) || turnFor(salesScenario, 4)?.templateIds === "diagnostic.deliver") {
    failures.push({
      scenario: salesScenario?.title,
      turn: 4,
      issue: "clear buy/waitlist intent should move to waitlist copy instead of repeating diagnostic",
      observed: salesTurn4,
    });
  }

  const salesTurn5 = textFor(salesScenario, 5);
  if (!/lista de espera|registrad|anotad|entr(o|ou)/i.test(salesTurn5) || turnFor(salesScenario, 5)?.templateIds === "diagnostic.deliver") {
    failures.push({
      scenario: salesScenario?.title,
      turn: 5,
      issue: "waitlist join should confirm the saved waitlist entry",
      observed: salesTurn5,
    });
  }

  const salesTurn6 = textFor(salesScenario, 6);
  if (!/Completo|1\.497|R\$ ?1\.497/i.test(salesTurn6)) {
    failures.push({
      scenario: salesScenario?.title,
      turn: 6,
      issue: "post-waitlist product question should answer the product fact directly",
      observed: salesTurn6,
    });
  }

  const salesTurn7 = textFor(salesScenario, 7);
  if (!/humano|pessoa|equipe|assumir/i.test(salesTurn7) || turnFor(salesScenario, 7)?.templateIds === "diagnostic.deliver") {
    failures.push({
      scenario: salesScenario?.title,
      turn: 7,
      issue: "handoff request should acknowledge human takeover instead of repeating diagnostic",
      observed: salesTurn7,
    });
  }

  const longScenario = findScenario("Long mixed lead");
  const longTurn5 = textFor(longScenario, 5);
  if (/Posso fazer um diagnóstico gratuito|Posso fazer um diagnostico gratuito/i.test(longTurn5)) {
    failures.push({
      scenario: longScenario?.title,
      turn: 5,
      issue: "diagnostic already in progress should not re-offer the diagnostic",
      observed: longTurn5,
    });
  }

  const longTurn6 = textFor(longScenario, 6);
  if (!/demonstração|demonstracao|link|ver na prática|ver na pratica/i.test(longTurn6)) {
    failures.push({
      scenario: longScenario?.title,
      turn: 6,
      issue: "demo request during a mixed flow should still be acknowledged as a demo request",
      observed: longTurn6,
    });
  }

  for (const scenario of scenarios) {
    for (const turn of scenario.turns) {
      const text = turn.assistantMessages.map((message) => message.content || "").join("\n");
      if (/\b(voce|voces|mes|tambem|nao|prioritaria)\b/i.test(text)) {
        failures.push({ scenario: scenario.title, turn: turn.index, issue: "assistant copy has unaccented pt-BR words", observed: text });
      }
      if (/\.\./.test(text)) {
        failures.push({ scenario: scenario.title, turn: turn.index, issue: "assistant copy has doubled punctuation", observed: text });
      }
      if (/Eu compararia ainda não dá|Eu compararia ainda nao da|com calma, validando/i.test(text)) {
        failures.push({ scenario: scenario.title, turn: turn.index, issue: "assistant copy has malformed plan comparison sentence", observed: text });
      }
      if (/\b(lead reports|lead says|prospects|slow to reply|slow to respond)\b/i.test(text)) {
        failures.push({ scenario: scenario.title, turn: turn.index, issue: "assistant copy leaked English/internal lead fact phrasing", observed: text });
      }
    }
  }

  return {
    ok: failures.length === 0,
    failures,
  };
}

function buildResults({ visual, sales, salesInbox, allConversationScenarios, toneReviews, behaviorReview, costSummary }) {
  return [
    assert(visual.ok, "Visual widget CTA renders in desktop and mobile screenshots", visual),
    assert(
      sales.turns.every((turn) => turn.httpStatus === 200),
      "Widget API complete Sales Inbox flow returned HTTP 200 for every turn",
      { statuses: sales.turns.map((turn) => turn.httpStatus) },
    ),
    assert(salesInbox.ok, "Sales Inbox detail endpoint returned persisted lead", salesInbox),
    assert((salesInbox.lead?.recentMessages?.length || 0) >= 10, "Sales Inbox persisted full conversation messages", {
      messageCount: salesInbox.lead?.recentMessages?.length || 0,
    }),
    assert(salesInbox.lead?.waitlistStatus === "joined", "Sales Inbox persisted joined waitlist", {
      waitlistStatus: salesInbox.lead?.waitlistStatus,
    }),
    assert(salesInbox.lead?.humanActive === true || salesInbox.lead?.aiPaused === true, "Sales Inbox persisted handoff/human pause", {
      humanActive: salesInbox.lead?.humanActive,
      aiPaused: salesInbox.lead?.aiPaused,
    }),
    assert(costSummary.totalCostUsd > 0, "OpenAI real usage cost was recorded", costSummary),
    assert(costSummary.totalCostUsd <= 1.0, "Autonomous validation stayed under US$1.00 cost budget", costSummary),
    assert(costSummary.p95LatencyMs <= 45000, "P95 latency stayed below 45s", costSummary),
    assert(behaviorReview.ok, "Mapped behavior QA passed for waitlist, handoff, product, diagnostic, and pt-BR copy", behaviorReview),
    assert(toneReviews.every((review) => review.ok), "Tone rubric passed for every autonomous transcript", toneReviews),
    assert(
      allConversationScenarios.every((scenario) => scenario.turns.every((turn) => turn.assistantMessages.length <= 3)),
      "All widget responses used at most three chunks",
    ),
  ];
}

function buildMarkdownSections({ visual, sales, salesInbox, costScenarios, costSummary, toneReviews, behaviorReview, startedAt, finishedAt }) {
  return [
    {
      title: "Executive Summary",
      lines: [
        `- Started: ${startedAt}`,
        `- Finished: ${finishedAt}`,
        `- App URL: ${APP_URL}`,
        `- Visual widget: ${visual.ok ? "PASS" : "FAIL"}`,
        `- Sales Inbox: ${salesInbox.ok ? "PASS" : "FAIL"}`,
        `- Mapped behavior QA: ${behaviorReview.ok ? "PASS" : "FAIL"} (${behaviorReview.failures.length} issue(s))`,
        `- Total OpenAI cost observed: US$${costSummary.totalCostUsd}`,
        `- Average cost per lead: US$${costSummary.avgCostPerLeadUsd}`,
        `- Average latency: ${costSummary.avgLatencyMs}ms`,
        `- P95 latency: ${costSummary.p95LatencyMs}ms`,
      ],
    },
    {
      title: "Visual Widget Evidence",
      lines: [
        `- Status: ${visual.ok ? "PASS" : "FAIL"}`,
        `- Desktop screenshot: ${visual.screenshots.desktop}`,
        `- Mobile screenshot: ${visual.screenshots.mobile}`,
        `- Failures: ${visual.failures.length ? visual.failures.join("; ") : "none"}`,
      ],
    },
    scenarioSection(sales, "Sales Inbox Flow Transcript"),
    {
      title: "Sales Inbox Evidence",
      lines: [
        `- Lead ID: ${salesInbox.leadId}`,
        `- API status: list=${salesInbox.listStatus}, detail=${salesInbox.detailStatus}`,
        `- Lead status: ${salesInbox.lead?.status}`,
        `- Conversion path: ${salesInbox.lead?.conversionPath}`,
        `- Waitlist status: ${salesInbox.lead?.waitlistStatus}`,
        `- Diagnostic status: ${salesInbox.lead?.diagnosticStatus}`,
        `- Human active: ${salesInbox.lead?.humanActive}`,
        `- AI paused: ${salesInbox.lead?.aiPaused}`,
        `- Messages saved: ${salesInbox.lead?.recentMessages?.length ?? 0}`,
        `- Runtime trace: ${salesInbox.lead?.agentRuntime?.traceId ?? "missing"}`,
        `- Runtime cost: ${salesInbox.lead?.agentRuntime?.estimatedCostUsd ?? "missing"}`,
        "",
        ...(salesInbox.lead?.recentMessages || []).map((message) => `- ${message.role}: ${message.content}`),
      ],
    },
    {
      title: "Cost And Latency",
      lines: [
        `- Scenarios: ${costSummary.scenarioCount}`,
        `- Turns: ${costSummary.turnCount}`,
        `- Total cost: US$${costSummary.totalCostUsd}`,
        `- Average cost per turn: US$${costSummary.avgCostPerTurnUsd}`,
        `- Average cost per lead: US$${costSummary.avgCostPerLeadUsd}`,
        `- Max turn cost: US$${costSummary.maxTurnCostUsd}`,
        `- Average latency: ${costSummary.avgLatencyMs}ms`,
        `- P95 latency: ${costSummary.p95LatencyMs}ms`,
        `- Max latency: ${costSummary.maxLatencyMs}ms`,
        `- Most expensive turn: ${costSummary.mostExpensiveTurn?.scenarioId} turn ${costSummary.mostExpensiveTurn?.index}, US$${costSummary.mostExpensiveTurn?.costUsd}`,
      ],
    },
    ...costScenarios.map((scenario) => scenarioSection(scenario, `Transcript: ${scenario.title}`)),
    {
      title: "Mapped Behavior QA",
      lines: behaviorReview.failures.length
        ? behaviorReview.failures.flatMap((failure) => [
            `- FAIL ${failure.scenario} turn ${failure.turn}: ${failure.issue}`,
            `  - Observed: ${failure.observed}`,
          ])
        : ["- PASS: mapped behavior checks found no issues."],
    },
    {
      title: "Tone Review",
      lines: toneReviews.flatMap((review) => [
        `- ${review.ok ? "PASS" : "FAIL"} ${review.title}: ${review.score}/5`,
        `  - Notes: ${review.notes}`,
        `  - Issues: ${review.failures.length ? review.failures.join("; ") : "none"}`,
      ]),
    },
  ];
}

function scenarioSection(scenario, title) {
  return {
    title,
    lines: [
      `- Scenario ID: ${scenario.id}`,
      `- Lead ID: ${scenario.leadId}`,
      `- Turns: ${scenario.totals.turns}`,
      `- Cost: US$${scenario.totals.costUsd}`,
      `- Average latency: ${scenario.totals.avgLatencyMs}ms`,
      "",
      ...scenario.turns.flatMap((turn) => [
        `Lead ${turn.index}: ${turn.user}`,
        ...turn.assistantMessages.map((message, index) => {
          const action = message.action ? ` [action: ${message.action.label} -> ${message.action.href}]` : "";
          return `Taliya ${turn.index}.${index + 1}: ${message.content}${action}`;
        }),
        `Runtime ${turn.index}: http=${turn.httpStatus}; latency=${turn.latencyMs}ms; cost=US$${turn.costUsd}; route=${turn.route}; agent=${turn.currentAgent}; templates=${turn.templateIds}`,
        "",
      ]),
    ],
  };
}

function roundMoney(value) {
  return Number((Number.isFinite(value) ? value : 0).toFixed(6));
}
