#!/usr/bin/env node

import { createHmac } from "node:crypto";
import { mkdirSync, writeFileSync } from "node:fs";
import { dirname } from "node:path";

const targetArg = process.argv.find((arg) => arg.startsWith("--target="));
const target = targetArg?.slice("--target=".length) || process.env.AI_ATTENDANT_EVAL_TARGET;
const salesTokenArg = process.argv.find((arg) => arg.startsWith("--sales-token="));
const salesToken = salesTokenArg?.slice("--sales-token=".length) || process.env.INTERNAL_SALES_INBOX_TOKEN;
const reportArg = process.argv.find((arg) => arg.startsWith("--report="));
const reportPath = reportArg?.slice("--report=".length);
const caseArg = process.argv.find((arg) => arg.startsWith("--case="));
const caseFilter = caseArg ? new Set(caseArg.slice("--case=".length).split(",").map((item) => item.trim()).filter(Boolean)) : undefined;
const maxArg = process.argv.find((arg) => arg.startsWith("--max-cases="));
const maxCases = maxArg ? Number(maxArg.slice("--max-cases=".length)) : undefined;

const appSecret = process.env.META_WHATSAPP_APP_SECRET || "codex_meta_app_secret";
const phoneNumberId = process.env.META_WHATSAPP_PHONE_NUMBER_ID || "phone_number_test";

const shortCases = [
  shortCase("SHORT-PRICE", "Preco depois do nome", "Quanto custa?", {
    mustIncludeAny: ["planos", "base", "agente", "valores"],
    forbidden: ["checkout", "lista de espera"],
  }),
  shortCase("SHORT-DEMO", "Demo depois do nome", "Quero ver uma demo", {
    mustIncludeAny: ["demo", "visualizar", "funcionando"],
    forbidden: ["/pilates/demonstracao", "lista de espera"],
  }),
  shortCase("SHORT-KNOW", "Conhecer melhor", "Quero conhecer melhor", {
    mustIncludeAny: ["taliya", "studio", "rotina", "organiza"],
    forbidden: ["lista de espera", "checkout"],
  }),
  shortCase("SHORT-REPLACEMENTS", "Dor de reposicoes", "Tenho problema com reposicoes", {
    mustIncludeAny: ["reposicoes", "agenda", "faltas"],
    mustInclude: ["diagnostico"],
    forbidden: ["lista de espera", "checkout"],
  }),
  shortCase("SHORT-WHATSAPP", "WhatsApp baguncado", "Meu WhatsApp esta uma bagunca", {
    mustIncludeAny: ["whatsapp", "atendimento", "mensagens"],
    mustInclude: ["diagnostico"],
    forbidden: ["lista de espera", "checkout"],
  }),
  shortCase("SHORT-SALES", "Perdendo leads", "Estou perdendo leads", {
    mustIncludeAny: ["leads", "vendas", "interessados", "follow"],
    forbidden: ["checkout", "lista de espera"],
  }),
  shortCase("SHORT-FINANCE", "Financeiro dificil", "Financeiro esta dificil", {
    mustIncludeAny: ["financeiro", "cobranca", "mensalidade"],
    forbidden: ["nota fiscal automatica", "checkout", "lista de espera"],
  }),
  shortCase("SHORT-MANAGEMENT", "Sem visao do dia", "Nao vejo o que acontece no dia", {
    mustIncludeAny: ["rotina", "dia", "prioridades", "gestao"],
    forbidden: ["checkout", "lista de espera"],
  }),
  shortCase("SHORT-HIRE", "Quer contratar", "Quero contratar", {
    mustIncludeAny: ["entender", "cenario", "diagnostico", "studio"],
    forbidden: ["coloquei seu studio na lista", "checkout"],
  }),
  shortCase("SHORT-EXISTING-SYSTEM", "Ja tem sistema", "Ja tenho sistema", {
    mustIncludeAny: ["o que", "nao resolve", "sistema atual", "rotina"],
    forbidden: ["substitui tudo", "lista de espera"],
  }),
  shortCase("SHORT-RECEPTIONIST", "Substitui recepcionista", "Isso substitui recepcionista?", {
    mustIncludeAny: ["nao", "equipe", "repetitivas", "controle"],
    forbidden: ["substitui sua recepcionista", "lista de espera"],
  }),
  shortCase("SHORT-SMALL", "Studio pequeno", "Meu studio e pequeno", {
    mustIncludeAny: ["pequeno", "rotina", "repetitiva", "dor"],
    forbidden: ["nao serve", "lista de espera"],
  }),
  shortCase("SHORT-LARGE-MANUAL", "120 alunos e caderno", "Tenho 120 alunos e uso caderno", {
    mustIncludeAny: ["120", "caderno", "manual", "organizar"],
    mustInclude: ["diagnostico"],
    forbidden: ["lista de espera", "checkout"],
  }),
  shortCase("SHORT-RESEARCHING", "So pesquisando", "Estou so pesquisando", {
    mustIncludeAny: ["sem problema", "comparar", "pesquisando", "entender"],
    forbidden: ["checkout", "lista de espera"],
  }),
  shortCase("SHORT-INTEGRATION", "Integracao desconhecida", "Integra com Google Agenda?", {
    mustIncludeAny: ["nao", "confirmar", "fluxo", "integracao"],
    forbidden: ["sim, ja integra", "integracao pronta", "lista de espera"],
  }),
];

const mediumCases = [
  mediumCase("MID-AGENDA", "Diagnostico medio de agenda", "agenda e reposicoes estao baguncadas"),
  mediumCase("MID-WHATSAPP", "Diagnostico medio de WhatsApp", "meu WhatsApp esta uma bagunca"),
  mediumCase("MID-SALES", "Diagnostico medio de vendas", "perco muitos leads e interessados"),
  mediumCase("MID-FINANCE", "Diagnostico medio de financeiro", "cobranca e mensalidade estao confusas"),
  mediumCase("MID-BROAD", "Diagnostico medio de dor ampla", "tudo um pouco, depende do dia"),
];

const longCases = [
  {
    id: "LONG-WA-WAITLIST",
    title: "WhatsApp ideal ate lista de espera",
    channels: ["whatsapp"],
    turns: [
      "Oi",
      "Lucas",
      "reposicoes e agenda estao me dando trabalho",
      "quero fazer o diagnostico gratuito",
      "100 alunos",
      "tudo um pouco, depende do dia",
      "consigo quando tudo esta em ordem",
      "caderno",
      "reposicao",
      "agora",
      "faz sentido",
      "pode ser",
      "studio do lucas, vila velha",
    ],
    expectedLead: {
      conversionPath: "waitlist_intent",
      waitlistStatus: "joined",
      commercialStage: "waitlist_joined",
    },
    mustInclude: ["coloquei", "lista de espera"],
  },
  {
    id: "LONG-WIDGET-WAITLIST",
    title: "Widget ideal ate lista de espera",
    channels: ["widget"],
    turns: [
      "Quero fazer diagnostico gratuito",
      "Lucas",
      "27 996991427",
      "100",
      "tudo um pouco, depende do dia",
      "consigo qd tudo esta em ordem",
      "caderno",
      "reposicao",
      "agora",
      "faz sentido",
      "pode ser",
      "studio do lucas, vila velha",
    ],
    expectedLead: {
      conversionPath: "waitlist_intent",
      waitlistStatus: "joined",
      commercialStage: "waitlist_joined",
    },
    mustInclude: ["coloquei", "lista de espera"],
  },
  {
    id: "LONG-DIAG-NEGATIVE",
    title: "Resposta negativa apos diagnostico nao oferece lista",
    channels: ["widget", "whatsapp"],
    turns: [
      "Quero fazer diagnostico gratuito",
      "Lucas",
      "27 996991427",
      "100",
      "reposicoes e agenda",
      "consigo quando tudo esta em ordem",
      "caderno",
      "caderno",
      "reposicao",
      "agora",
      "nao sei, ainda nao faz sentido",
    ],
    whatsappTurns: [
      "Oi",
      "Lucas",
      "reposicoes e agenda estao me dando trabalho",
      "quero fazer o diagnostico gratuito",
      "100 alunos",
      "reposicoes e agenda",
      "consigo quando tudo esta em ordem",
      "caderno",
      "caderno",
      "reposicao",
      "agora",
      "nao sei, ainda nao faz sentido",
    ],
    mustIncludeAny: ["nao colocaria", "nao vou te colocar", "sem problema"],
    forbidden: ["quer que eu coloque", "lista de espera?"],
  },
  {
    id: "LONG-DEMO-POSITIVE",
    title: "Resposta positiva apos demo oferece lista",
    channels: ["widget", "whatsapp"],
    turns: ["Lucas", "Quero ver uma demo", "faz sentido, gostei"],
    mustInclude: ["lista de espera"],
    expectedLead: {
      conversionPath: "waitlist_intent",
      waitlistStatus: "offered",
      commercialStage: "waitlist_offered",
    },
  },
  {
    id: "LONG-DEMO-NEGATIVE",
    title: "Resposta negativa apos demo nao forca lista",
    channels: ["widget", "whatsapp"],
    turns: ["Lucas", "Quero ver uma demo", "nao sei, ainda fiquei em duvida"],
    mustIncludeAny: ["nao vou te colocar", "nao ficou claro", "sem problema"],
    forbidden: ["quer que eu coloque", "lista de espera?"],
  },
];

const scenarios = [...shortCases, ...mediumCases, ...longCases]
  .filter((scenario) => !caseFilter || caseFilter.has(scenario.id))
  .slice(0, Number.isFinite(maxCases) && maxCases > 0 ? maxCases : undefined);

if (!target || !salesToken) {
  console.error("Usage: npm run eval:commercial-conversation-matrix -- --target=http://localhost:3000 --sales-token=TOKEN [--report=path]");
  process.exit(1);
}

const results = [];
for (const scenario of scenarios) {
  for (const channel of scenario.channels) {
    const result = await runScenario(scenario, channel);
    results.push(result);
    const label = result.ok ? "PASS" : "FAIL";
    console.log(`${label} ${scenario.id}/${channel}: ${scenario.title}${result.reason ? ` - ${result.reason}` : ""}`);
  }
}

const failed = results.filter((result) => !result.ok);
console.log(`\nCommercial conversation matrix: ${results.length - failed.length}/${results.length} passed.`);
if (reportPath) {
  mkdirSync(dirname(reportPath), { recursive: true });
  writeFileSync(reportPath, renderReport(results), "utf8");
  console.log(`Report written to ${reportPath}`);
}
if (failed.length) process.exit(1);

function shortCase(id, title, userSignal, expectations) {
  return {
    id,
    title,
    channels: ["widget", "whatsapp"],
    turns: ["Lucas", userSignal],
    ...expectations,
    forbidden: [...(expectations.forbidden ?? []), "quer que eu coloque o studio na lista de espera"],
  };
}

function mediumCase(id, title, pain) {
  return {
    id,
    title,
    channels: ["widget", "whatsapp"],
    turns: ["Lucas", pain, "quero fazer o diagnostico gratuito", "100 alunos", "uso caderno e WhatsApp"],
    widgetTurns: ["Lucas", pain, "quero fazer o diagnostico gratuito", "27 996991427", "100 alunos", "uso caderno e WhatsApp"],
    mustIncludeAny: ["quais partes", "hoje voce consegue", "sistema", "caderno", "whatsapp"],
    forbidden: ["lista de espera", "checkout"],
    expectedLeadPartial: {
      waitlistStatus: "not_offered",
    },
  };
}

function turnsForChannel(scenario, channel) {
  if (channel === "widget" && Array.isArray(scenario.widgetTurns)) return scenario.widgetTurns;
  if (channel === "whatsapp" && Array.isArray(scenario.whatsappTurns)) return scenario.whatsappTurns;
  return scenario.turns;
}

async function runScenario(scenario, channel) {
  const runId = `${scenario.id.toLowerCase()}_${channel}_${Date.now()}_${Math.random().toString(36).slice(2, 7)}`;
  const runner = channel === "whatsapp" ? runWhatsAppScenario : runWidgetScenario;
  try {
    const state = await runner(scenario, runId);
    const assertions = assertScenario(scenario, state);
    return {
      ok: assertions.ok,
      reason: assertions.reason,
      scenario,
      channel,
      state,
    };
  } catch (error) {
    return {
      ok: false,
      reason: error instanceof Error ? error.message : "Scenario failed.",
      scenario,
      channel,
      state: { transcript: [] },
    };
  }
}

async function runWidgetScenario(scenario, runId) {
  const sessionId = `matrix_${runId}`;
  const session = {
    sessionId,
    channel: "web",
    entryPath: scenario.entryPath ?? "widget",
    niche: "pilates",
    sourcePage: "/pilates",
    campaignStage: "commercial",
    publicOfferMode: "direct_saas_subscription",
    messages: [],
    selectedPainIds: [],
    recommendedAgentIds: [],
    qualificationDraft: { ...(scenario.initialQualificationDraft ?? {}) },
  };
  const transcript = [];
  let finalResponse;

  for (const userMessage of turnsForChannel(scenario, "widget")) {
    const response = await fetch(new URL("/api/landing/ai-attendant", target), {
      method: "POST",
      headers: { "content-type": "application/json" },
      body: JSON.stringify({
        session,
        userMessage,
        pageSignals: scenario.pageSignals ?? {},
      }),
    });
    const payload = await response.json();
    if (!response.ok) throw new Error(`Widget HTTP ${response.status}: ${JSON.stringify(payload).slice(0, 180)}`);
    const assistant = (payload.assistantMessages ?? []).map((message) => message.content);
    transcript.push({ user: userMessage, assistant, conversionPath: payload.conversionPath ?? "none" });
    session.messages.push({ role: "user", content: userMessage });
    for (const content of assistant) session.messages.push({ role: "assistant", content });
    session.qualificationDraft = { ...session.qualificationDraft, ...(payload.qualificationPatch ?? {}) };
    session.selectedPainIds = unique([...(session.selectedPainIds ?? []), ...(payload.capturedPainIds ?? [])]);
    session.recommendedAgentIds = unique([...(session.recommendedAgentIds ?? []), ...(payload.recommendedAgentIds ?? [])]);
    if (payload.handoff?.leadId) session.leadId = payload.handoff.leadId;
    finalResponse = payload;
  }

  const lead = await findLead((item) => item.sessionId === sessionId);
  return { transcript, finalResponse, lead, sessionId };
}

async function runWhatsAppScenario(scenario, runId) {
  const providerContactId = `5511${String(Math.abs(hashCode(runId))).padStart(9, "0").slice(0, 9)}`;
  const transcript = [];
  let finalPayload;

  for (const [index, userMessage] of turnsForChannel(scenario, "whatsapp").entries()) {
    const rawBody = JSON.stringify(textBody(`wamid.matrix.${runId}.${index}`, userMessage, providerContactId));
    const response = await fetch(new URL("/api/landing/ai-attendant/whatsapp", target), {
      method: "POST",
      headers: {
        "content-type": "application/json",
        "x-hub-signature-256": sign(rawBody),
      },
      body: rawBody,
    });
    const payload = await response.json();
    if (!response.ok) throw new Error(`WhatsApp HTTP ${response.status}: ${JSON.stringify(payload).slice(0, 180)}`);
    const result = Array.isArray(payload.results) ? payload.results[0] : undefined;
    transcript.push({
      user: userMessage,
      assistant: Array.isArray(result?.replyPreviews) ? result.replyPreviews : result?.replyPreview ? [result.replyPreview] : [],
      providerStatus: result?.status,
      conversionPath: result?.status ?? "processed",
    });
    finalPayload = payload;
  }

  const lead = await findLead((item) => item.sessionId === `wa_${providerContactId}` || item.contact?.providerContactId === providerContactId);
  return { transcript, finalResponse: finalPayload, lead, providerContactId };
}

function assertScenario(scenario, state) {
  const finalText = normalize(lastAssistantText(state));
  const allText = normalize(fullAssistantText(state));

  for (const expected of scenario.mustInclude ?? []) {
    if (!allText.includes(normalize(expected))) return fail(`expected text containing "${expected}"`);
  }

  if (scenario.mustIncludeAny?.length && !scenario.mustIncludeAny.some((item) => allText.includes(normalize(item)))) {
    return fail(`expected any of: ${scenario.mustIncludeAny.join(", ")}`);
  }

  for (const forbidden of scenario.forbidden ?? []) {
    if (allText.includes(normalize(forbidden))) return fail(`forbidden text found: "${forbidden}"`);
  }

  if (scenario.expectedLead) {
    if (!state.lead) return fail("expected Sales Inbox lead");
    for (const [key, value] of Object.entries(scenario.expectedLead)) {
      if (state.lead[key] !== value) return fail(`expected lead.${key}=${value}, got ${state.lead[key]}`);
    }
  }

  if (scenario.expectedLeadPartial && state.lead) {
    for (const [key, value] of Object.entries(scenario.expectedLeadPartial)) {
      if (state.lead[key] !== value) return fail(`expected lead.${key}=${value}, got ${state.lead[key]}`);
    }
  }

  if (!state.transcript.length || !finalText) return fail("empty transcript");
  return { ok: true };
}

function fail(reason) {
  return { ok: false, reason };
}

async function findLead(predicate) {
  for (let attempt = 0; attempt < 8; attempt += 1) {
    await wait(attempt === 0 ? 250 : 500);
    const response = await fetch(new URL("/api/internal/sales-inbox/leads", target), {
      headers: { "x-internal-sales-token": salesToken },
    });
    if (!response.ok) return null;
    const body = await response.json();
    const leads = Array.isArray(body.leads) ? body.leads : [];
    const lead = leads.find(predicate);
    if (lead) return lead;
  }
  return null;
}

function textBody(providerMessageId, text, from) {
  return {
    object: "whatsapp_business_account",
    entry: [
      {
        id: "waba_test",
        changes: [
          {
            field: "messages",
            value: {
              messaging_product: "whatsapp",
              metadata: {
                display_phone_number: "5527920015824",
                phone_number_id: phoneNumberId,
              },
              contacts: [
                {
                  wa_id: from,
                  profile: { name: "Lead Matriz" },
                },
              ],
              messages: [
                {
                  from,
                  id: providerMessageId,
                  timestamp: Math.floor(Date.now() / 1000).toString(),
                  type: "text",
                  text: { body: text },
                },
              ],
            },
          },
        ],
      },
    ],
  };
}

function sign(rawBody) {
  return `sha256=${createHmac("sha256", appSecret).update(rawBody).digest("hex")}`;
}

function normalize(value) {
  return String(value ?? "")
    .toLowerCase()
    .normalize("NFD")
    .replace(/\p{Diacritic}/gu, "");
}

function lastAssistantText(state) {
  const last = state.transcript[state.transcript.length - 1];
  return (last?.assistant ?? []).join("\n");
}

function fullAssistantText(state) {
  return state.transcript.flatMap((turn) => turn.assistant ?? []).join("\n");
}

function unique(items) {
  return Array.from(new Set(items.filter(Boolean)));
}

function wait(ms) {
  return new Promise((resolve) => setTimeout(resolve, ms));
}

function hashCode(value) {
  let hash = 0;
  for (let index = 0; index < value.length; index += 1) {
    hash = (hash << 5) - hash + value.charCodeAt(index);
    hash |= 0;
  }
  return hash;
}

function renderReport(results) {
  const lines = [
    "# Commercial Conversation Matrix Report",
    "",
    `Generated: ${new Date().toISOString()}`,
    "",
    `Summary: ${results.filter((result) => result.ok).length}/${results.length} passed.`,
    "",
  ];

  for (const result of results) {
    lines.push(`## ${result.ok ? "PASS" : "FAIL"} ${result.scenario.id}/${result.channel}`);
    lines.push("");
    lines.push(`Title: ${result.scenario.title}`);
    if (result.reason) lines.push(`Failure: ${result.reason}`);
    lines.push("");
    lines.push("Transcript:");
    lines.push("");
    for (const turn of result.state.transcript ?? []) {
      lines.push(`- Lead: ${turn.user}`);
      for (const assistant of turn.assistant ?? []) lines.push(`- Taliya: ${assistant}`);
    }
    lines.push("");
    if (result.state.lead) {
      lines.push("Lead state:");
      lines.push("");
      lines.push(`- leadId: ${result.state.lead.leadId}`);
      lines.push(`- status: ${result.state.lead.status}`);
      lines.push(`- priority: ${result.state.lead.priority}`);
      lines.push(`- conversionPath: ${result.state.lead.conversionPath}`);
      lines.push(`- commercialStage: ${result.state.lead.commercialStage}`);
      lines.push(`- waitlistStatus: ${result.state.lead.waitlistStatus}`);
      lines.push(`- diagnosticStatus: ${result.state.lead.diagnosticStatus}`);
      lines.push("");
    }
  }

  return `${lines.join("\n")}\n`;
}
