#!/usr/bin/env node

import { mkdirSync, writeFileSync } from "node:fs";
import { dirname } from "node:path";
import { createHmac } from "node:crypto";

const target = arg("target") || process.env.AI_ATTENDANT_EVAL_TARGET;
const reportPath = arg("report") || `reports/008-price-plan-commercial-matrix-${Date.now()}.md`;
const salesToken = arg("sales-token") || process.env.INTERNAL_SALES_INBOX_TOKEN;
const caseFilter = arg("case") ? new Set(arg("case").split(",").map((item) => item.trim()).filter(Boolean)) : undefined;
const maxCases = Number(arg("max-cases") || 0);

const expectedPlans = ["Base: R$ 197/mes", "Essencial: R$ 497/mes", "Avance: R$ 897/mes", "Completo: R$ 1.497/mes"];

const cases = [
  priceCase("PRICE-SOURCE-OF-TRUTH-MATCH", ["Quanto custa?"], { sourceOfTruth: true }),
  priceCase("PRICE-COLD-FIRST-MSG", ["Quanto custa?"]),
  priceCase("PRICE-AFTER-NAME", ["Lucas", "Qual valor?"]),
  priceCase("PRICE-AFTER-PAIN", ["Lucas", "reposicoes estao baguncadas", "E quanto custa?"]),
  priceCase("PRICE-DIAG-OFFERED", ["Lucas", "reposicoes estao baguncadas", "Antes, quanto custa?"]),
  priceCase("PRICE-IN-DIAGNOSTIC", ["Quero fazer diagnostico gratuito", "Lucas", "27 996991427", "Quero saber valores primeiro."]),
  priceCase("PRICE-AFTER-DIAG", diagnosticTurns("Quanto custa?"), { diagnosticDone: true }),
  priceCase("PRICE-AFTER-DEMO", ["Lucas", "Quero ver uma demo", "Quanto fica?"]),
  planCase("PLANS-COLD", ["Quais sao os planos?"]),
  planCase("PLANS-VIEW-DIRECT", ["Quero ver planos."]),
  planCase("PLANS-COMPARE", ["Quero comparar os planos."]),
  quickReplyCase("PLANS-QUICK-REPLY-NO-DIAG", "view_plans"),
  quickReplyCase("PLANS-QUICK-REPLY-WITH-DIAG", "view_plans", { initialQualificationDraft: { diagnosticCompleted: "true", diagnosticStatus: "completed" } }),
  planCase("PLANS-PAGE-ENTRY", ["Quero ver planos."], { entryPath: "plans_page", sourcePage: "/pilates/planos" }),
  recommendCase("PLAN-RECOMMEND-NO-DIAG", ["Qual plano faz sentido?"]),
  recommendCase("PLAN-RECOMMEND-WITH-PAIN-ONLY", ["Lucas", "agenda e reposicoes", "Qual plano faz sentido?"]),
  recommendCase("PLAN-RECOMMEND-WITH-DIAG", diagnosticTurns("Qual plano faz sentido?"), { diagnosticDone: true }),
  recommendCase("PLAN-RECOMMEND-AFTER-DEMO", ["Lucas", "Quero ver uma demo", "faz sentido", "Qual plano faz sentido?"], { forbidden: ["checkout"] }),
  buyCase("BUY-NO-DIAG", ["Quero contratar"]),
  buyCase("BUY-WITH-PAIN", ["Lucas", "tenho problema com reposicoes", "Quero contratar"]),
  buyCase("BUY-AFTER-DIAG-POSITIVE", [...diagnosticTurns("faz sentido"), "pode colocar"]),
  buyCase("BUY-AFTER-DEMO-POSITIVE", ["Lucas", "Quero ver uma demo", "faz sentido, gostei"]),
  buyCase("BUY-WAITLIST-CURRENT-REALITY", [...diagnosticTurns("faz sentido"), "pode colocar", "Studio Lucas, Vila Velha"]),
  {
    id: "DEMO-UNAVAILABLE-HONEST-ROUTE",
    title: "Demo indisponivel nao inventa tela pronta",
    channels: ["widget", "whatsapp"],
    turns: ["Lucas", "Quero ver uma demo"],
    mustIncludeAny: ["demo real ainda nao", "nao esta disponivel"],
    forbidden: ["clique na demo", "/pilates/demonstracao"],
  },
  objection("PRICE-EXPENSIVE", "Achei caro"),
  objection("PRICE-DISCOUNT", "Tem desconto?"),
  objection("PRICE-FREE", "Tem plano gratis?"),
  objection("PRICE-TRIAL", "Tem teste gratis?"),
  objection("PRICE-ROI", "Isso se paga como?"),
  objection("PRICE-SMALL-STUDIO", "Meu studio e pequeno, vale a pena?"),
  objection("PRICE-ONLY-ONE-PAIN", "So tenho problema com agenda, qual plano?"),
  objection("PRICE-MANY-PAINS", "Tenho problema com WhatsApp, agenda, vendas e financeiro"),
].filter((item) => !caseFilter || caseFilter.has(item.id)).slice(0, maxCases > 0 ? maxCases : undefined);

if (!target) {
  console.log(`Price/plan matrix ready: ${cases.length} cases.`);
  console.log("Run with --target=http://localhost:3999");
  process.exit(0);
}

const results = [];
for (const scenario of cases) {
  for (const channel of scenario.channels) {
    const result = await runScenario(scenario, channel);
    results.push(result);
    console.log(`${result.ok ? "PASS" : "FAIL"} ${scenario.id}/${channel}${result.reason ? ` - ${result.reason}` : ""}`);
  }
}

mkdirSync(dirname(reportPath), { recursive: true });
writeFileSync(reportPath, renderReport(results), "utf8");
console.log(`\nPrice/plan matrix: ${results.filter((item) => item.ok).length}/${results.length} passed.`);
console.log(`Report written to ${reportPath}`);
if (results.some((item) => !item.ok)) process.exit(1);

function priceCase(id, turns, extra = {}) {
  return {
    id,
    title: id,
    channels: ["widget", "whatsapp"],
    turns,
    mustIncludeAny: ["planos", "Base", "Essencial", "Avance", "Completo"],
    mustInclude: ["R$"],
    forbidden: ["preciso entender sua rotina", "checkout", "lista de espera"],
    ...extra,
  };
}

function planCase(id, turns, extra = {}) {
  return {
    ...priceCase(id, turns, extra),
    mustIncludeAny: ["comparativo", "Base", "Essencial", "Avance", "Completo"],
    forbidden: ["preciso entender sua rotina", "checkout", "lista de espera"],
  };
}

function quickReplyCase(id, quickReplyId, extra = {}) {
  return {
    ...planCase(id, [], extra),
    quickReplyId,
  };
}

function recommendCase(id, turns, extra = {}) {
  return {
    ...priceCase(id, turns, extra),
    forbidden: extra.forbidden ?? ["checkout", "quer que eu coloque o studio na lista de espera"],
  };
}

function buyCase(id, turns, extra = {}) {
  return {
    id,
    title: id,
    channels: ["widget", "whatsapp"],
    turns,
    mustIncludeAny: ["diagnostico", "lista de espera", "planos", "studio"],
    forbidden: ["checkout seguro", "link de pagamento"],
    ...extra,
  };
}

function objection(id, message) {
  return {
    id,
    title: id,
    channels: ["widget", "whatsapp"],
    turns: ["Lucas", message],
    mustIncludeAny: ["Taliya", "diagnostico", "plano", "valor", "studio", "rotina"],
    forbidden: ["checkout", "lista de espera"],
  };
}

function diagnosticTurns(finalTurn) {
  return [
    "Quero fazer diagnostico gratuito",
    "Lucas",
    "27 996991427",
    "100 alunos",
    "reposicoes e agenda",
    "consigo quando tudo esta em ordem",
    "caderno",
    "reposicao",
    "agora",
    finalTurn,
  ];
}

async function runScenario(scenario, channel) {
  const runId = `${scenario.id.toLowerCase()}_${channel}_${Date.now()}_${Math.random().toString(36).slice(2, 7)}`;
  try {
    const state = channel === "whatsapp" ? await runWhatsApp(scenario, runId) : await runWidget(scenario, runId);
    const assertion = assertScenario(scenario, state);
    return { ok: assertion.ok, reason: assertion.reason, scenario, channel, state };
  } catch (error) {
    return { ok: false, reason: error instanceof Error ? error.message : String(error), scenario, channel, state: { transcript: [] } };
  }
}

async function runWidget(scenario, runId) {
  const session = {
    sessionId: `price_${runId}`,
    leadId: `lead_price_${runId}`,
    channel: "web",
    entryPath: scenario.entryPath ?? "widget",
    niche: "pilates",
    sourcePage: scenario.sourcePage ?? "/pilates",
    campaignStage: "commercial",
    publicOfferMode: "direct_saas_subscription",
    messages: [],
    selectedPainIds: [],
    recommendedAgentIds: [],
    qualificationDraft: scenario.initialQualificationDraft ?? {},
  };
  const transcript = [];
  if (scenario.quickReplyId) {
    await sendWidgetTurn(session, "", scenario.quickReplyId, transcript);
  }
  for (const turn of scenario.turns) await sendWidgetTurn(session, turn, undefined, transcript);
  return { transcript, sessionId: session.sessionId, lead: salesToken ? await findLead(session.sessionId) : null };
}

async function sendWidgetTurn(session, userMessage, quickReplyId, transcript) {
  const response = await fetch(new URL("/api/landing/ai-attendant", target), {
    method: "POST",
    headers: { "content-type": "application/json" },
    body: JSON.stringify({ session, userMessage: userMessage || undefined, quickReplyId }),
  });
  const payload = await response.json();
  if (!response.ok) throw new Error(`Widget HTTP ${response.status}: ${JSON.stringify(payload).slice(0, 200)}`);
  const assistant = (payload.assistantMessages ?? []).map((message) => message.content);
  transcript.push({ user: userMessage || `[quick:${quickReplyId}]`, assistant });
  if (userMessage) session.messages.push({ role: "user", content: userMessage });
  for (const content of assistant) session.messages.push({ role: "assistant", content });
  session.qualificationDraft = { ...session.qualificationDraft, ...(payload.qualificationPatch ?? {}) };
}

async function runWhatsApp(scenario, runId) {
  const providerContactId = `5599${String(Math.abs(hashCode(runId))).padStart(9, "0").slice(0, 9)}`;
  const transcript = [];
  const turns = scenario.quickReplyId ? ["Quero ver planos"] : scenario.turns;
  for (const [index, turn] of turns.entries()) {
    const rawBody = JSON.stringify(textBody(`wamid.price.${runId}.${index}`, turn, providerContactId));
    const response = await fetch(new URL("/api/landing/ai-attendant/whatsapp", target), {
      method: "POST",
      headers: { "content-type": "application/json", "x-hub-signature-256": sign(rawBody) },
      body: rawBody,
    });
    const payload = await response.json();
    if (!response.ok) throw new Error(`WhatsApp HTTP ${response.status}: ${JSON.stringify(payload).slice(0, 200)}`);
    const result = Array.isArray(payload.results) ? payload.results[0] : undefined;
    transcript.push({ user: turn, assistant: Array.isArray(result?.replyPreviews) ? result.replyPreviews : [result?.replyPreview].filter(Boolean) });
  }
  return { transcript, providerContactId, lead: salesToken ? await findLeadByProvider(providerContactId) : null };
}

function assertScenario(scenario, state) {
  const allText = normalize(state.transcript.flatMap((turn) => turn.assistant ?? []).join("\n"));
  if (!allText) return fail("empty assistant transcript");
  if (scenario.sourceOfTruth) {
    for (const plan of expectedPlans) {
      if (!allText.includes(normalize(plan))) return fail(`missing source-of-truth plan ${plan}`);
    }
  }
  for (const required of scenario.mustInclude ?? []) {
    if (!allText.includes(normalize(required))) return fail(`missing required text: ${required}`);
  }
  if (scenario.mustIncludeAny?.length && !scenario.mustIncludeAny.some((item) => allText.includes(normalize(item)))) {
    return fail(`missing any of ${scenario.mustIncludeAny.join(", ")}`);
  }
  for (const forbidden of scenario.forbidden ?? []) {
    if (allText.includes(normalize(forbidden))) return fail(`forbidden text: ${forbidden}`);
  }
  return { ok: true };
}

async function findLead(sessionId) {
  const leads = await listLeads();
  return leads.find((lead) => lead.sessionId === sessionId) ?? null;
}

async function findLeadByProvider(providerContactId) {
  const leads = await listLeads();
  return leads.find((lead) => lead.contact?.providerContactId === providerContactId) ?? null;
}

async function listLeads() {
  if (!salesToken) return [];
  const response = await fetch(new URL("/api/internal/sales-inbox/leads", target), { headers: { "x-internal-sales-token": salesToken } });
  if (!response.ok) return [];
  const payload = await response.json();
  return Array.isArray(payload.leads) ? payload.leads : [];
}

function textBody(providerMessageId, text, from) {
  return {
    object: "whatsapp_business_account",
    entry: [{ id: "waba_test", changes: [{ field: "messages", value: { messaging_product: "whatsapp", metadata: { display_phone_number: "5527920015824", phone_number_id: process.env.META_WHATSAPP_PHONE_NUMBER_ID || "phone_number_test" }, contacts: [{ wa_id: from, profile: { name: "Lead Matriz" } }], messages: [{ from, id: providerMessageId, timestamp: Math.floor(Date.now() / 1000).toString(), type: "text", text: { body: text } }] } }] }],
  };
}

function sign(rawBody) {
  const secret = process.env.META_WHATSAPP_APP_SECRET || "codex_meta_app_secret";
  return `sha256=${createHmac("sha256", secret).update(rawBody).digest("hex")}`;
}

function arg(name) {
  return process.argv.find((item) => item.startsWith(`--${name}=`))?.slice(name.length + 3);
}

function normalize(value) {
  return String(value ?? "").toLowerCase().normalize("NFD").replace(/\p{Diacritic}/gu, "");
}

function fail(reason) {
  return { ok: false, reason };
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
  const lines = ["# Price/Plan Commercial Matrix", "", `Generated: ${new Date().toISOString()}`, "", `Summary: ${results.filter((item) => item.ok).length}/${results.length} passed.`, ""];
  for (const result of results) {
    lines.push(`## ${result.ok ? "PASS" : "FAIL"} ${result.scenario.id}/${result.channel}`, "");
    if (result.reason) lines.push(`Failure: ${result.reason}`, "");
    for (const turn of result.state.transcript ?? []) {
      lines.push(`- Lead: ${turn.user}`);
      for (const assistant of turn.assistant ?? []) lines.push(`- Taliya: ${assistant}`);
    }
    if (result.state.lead) {
      lines.push("", `Lead: ${result.state.lead.leadId} / ${result.state.lead.priority} / ${result.state.lead.conversionPath}`);
    }
    lines.push("");
  }
  return `${lines.join("\n")}\n`;
}
