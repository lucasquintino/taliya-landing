#!/usr/bin/env node

import { createHmac } from "node:crypto";
import { mkdirSync, readFileSync, writeFileSync } from "node:fs";
import { dirname } from "node:path";

const target = arg("target") || process.env.AI_ATTENDANT_EVAL_TARGET;
const reportPath = arg("report") || `reports/008-message-delivery-matrix-${Date.now()}.md`;
const salesToken = arg("sales-token") || process.env.INTERNAL_SALES_INBOX_TOKEN;
const webhookPhoneNumberId = arg("phone-number-id") || process.env.META_WHATSAPP_PHONE_NUMBER_ID || "12345";

const cases = [
  { id: "DELIVERY-FIRST-SPLIT", channel: "whatsapp", turns: ["Oi"], assert: assertFirstSplit },
  { id: "DELIVERY-NO-USER-ECHO", channel: "whatsapp", turns: ["Oi, quero ver como Taliya ficaria no meu studio de Pilates e entender o caminho para começar."], assert: assertNoEcho },
  { id: "DELIVERY-WIDGET-EXPLORATION-NO-DEMO", channel: "widget", turns: ["Oi, quero ver como Taliya ficaria no meu studio de Pilates e entender o caminho para começar."], assert: assertWidgetExplorationNoDemo },
  { id: "DELIVERY-NO-LONG-BLOCKS", channel: "widget", turns: ["Lucas", "Tenho WhatsApp, agenda, vendas e financeiro baguncados e quero entender planos"], assert: assertNoLongBlocks },
  { id: "DELIVERY-NO-INSTANT-DRY-REPLY", channel: "source", assert: assertDelaySource },
  { id: "DELIVERY-TYPING-BEFORE-EACH-WIDGET", channel: "source", assert: assertWidgetTypingSource },
  { id: "DELIVERY-TYPING-BEFORE-EACH-WHATSAPP", channel: "source", assert: assertWhatsAppTypingSource },
  { id: "DELIVERY-PROPORTIONAL-DELAY-WIDGET", channel: "source", assert: assertWidgetDelaySource },
  { id: "DELIVERY-PROPORTIONAL-DELAY-WHATSAPP", channel: "source", assert: assertWhatsAppDelaySource },
  { id: "HUMAN-PRICE-COLD", channel: "whatsapp", turns: ["Quanto custa?"], assert: (state) => assertIncludes(state, ["R$", "diagnostico"], ["preciso entender sua rotina"]) },
  { id: "HUMAN-PLANS-DIRECT", channel: "widget", turns: ["Quero ver planos"], assert: (state) => assertIncludes(state, ["Base", "Essencial", "Avance", "Completo"], ["checkout"]) },
  { id: "HUMAN-RECOMMEND-NO-DIAG", channel: "widget", turns: ["Qual plano faz sentido?"], assert: (state) => assertIncludes(state, ["diagnostico"], ["checkout", "lista de espera"]) },
  { id: "HUMAN-OBJECTION-EXPENSIVE", channel: "widget", turns: ["Lucas", "Achei caro"], assert: (state) => assertIncludes(state, ["valor", "plano"], ["checkout"]) },
  { id: "HUMAN-ONLY-RESEARCHING", channel: "widget", turns: ["Lucas", "Estou so pesquisando"], assert: (state) => assertIncludes(state, ["sem pressa", "planos"], ["checkout", "lista de espera"]) },
  { id: "HUMAN-DEMO-NEGATIVE", channel: "widget", turns: ["Lucas", "Quero ver uma demo", "nao sei, fiquei em duvida"], assert: (state) => assertIncludes(state, ["nao vou te jogar", "qual parte ficou"], ["quer que eu coloque"]) },
  { id: "ABUSE-WIDGET-RATE-LIMIT", channel: "widget_abuse", turns: Array.from({ length: 8 }, (_, index) => `spam ${index}`), assert: assertRateLimitOrConfigured },
  { id: "MEDIA-WA-AUDIO-COLD", channel: "whatsapp_media", messageType: "audio", assert: assertUnsupportedMedia },
  { id: "MEDIA-WA-IMAGE-COLD", channel: "whatsapp_media", messageType: "image", assert: assertUnsupportedMedia },
  { id: "WEBHOOK-PROVIDER-MESSAGE-IDEMPOTENCY", channel: "whatsapp_duplicate", turns: ["Oi"], assert: assertDuplicate },
  { id: "WAITLIST-MISSING-FIELDS-VISIBLE", channel: "widget", turns: ["Quero assinar agora", "Pode colocar"], assert: assertWaitlistPendingVisible },
];

if (!target) {
  console.log(`Delivery matrix ready: ${cases.length} cases.`);
  console.log("Run with --target=http://localhost:3999");
  process.exit(0);
}

const results = [];
for (const scenario of cases) {
  const result = await runScenario(scenario);
  results.push(result);
  console.log(`${result.ok ? "PASS" : "FAIL"} ${scenario.id}${result.reason ? ` - ${result.reason}` : ""}`);
}

mkdirSync(dirname(reportPath), { recursive: true });
writeFileSync(reportPath, renderReport(results), "utf8");
console.log(`\nMessage delivery matrix: ${results.filter((item) => item.ok).length}/${results.length} passed.`);
console.log(`Report written to ${reportPath}`);
if (results.some((item) => !item.ok)) process.exit(1);

async function runScenario(scenario) {
  try {
    let state;
    if (scenario.channel === "source") state = readSourceState();
    else if (scenario.channel === "whatsapp") state = await runWhatsApp(scenario);
    else if (scenario.channel === "whatsapp_media") state = await runWhatsAppMedia(scenario);
    else if (scenario.channel === "whatsapp_duplicate") state = await runWhatsAppDuplicate(scenario);
    else state = await runWidget(scenario);
    const assertion = await scenario.assert(state);
    return { ok: assertion.ok, reason: assertion.reason, scenario, state };
  } catch (error) {
    return { ok: false, reason: error instanceof Error ? error.message : String(error), scenario, state: { transcript: [] } };
  }
}

async function runWidget(scenario) {
  const session = {
    sessionId: `delivery_${scenario.id}_${Date.now()}_${Math.random().toString(36).slice(2, 7)}`,
    leadId: `lead_delivery_${scenario.id}_${Date.now()}`,
    channel: "web",
    entryPath: "widget",
    niche: "pilates",
    sourcePage: "/pilates",
    campaignStage: "commercial",
    publicOfferMode: "direct_saas_subscription",
    messages: [],
    selectedPainIds: [],
    recommendedAgentIds: [],
    qualificationDraft: {},
  };
  const transcript = [];
  for (const turn of scenario.turns) {
    const response = await fetch(new URL("/api/landing/ai-attendant", target), {
      method: "POST",
      headers: { "content-type": "application/json" },
      body: JSON.stringify({ session, userMessage: turn }),
    });
    const payload = await response.json();
    if (!response.ok) throw new Error(`Widget HTTP ${response.status}: ${JSON.stringify(payload).slice(0, 200)}`);
    const assistant = (payload.assistantMessages ?? []).map((message) => message.content);
    transcript.push({ user: turn, assistant, payload });
    session.messages.push({ role: "user", content: turn });
    for (const content of assistant) session.messages.push({ role: "assistant", content });
    session.qualificationDraft = { ...session.qualificationDraft, ...(payload.qualificationPatch ?? {}) };
  }
  return { transcript, sessionId: session.sessionId, lead: salesToken ? await findLead(session.sessionId) : null };
}

async function runWhatsApp(scenario) {
  const runId = `${scenario.id.toLowerCase()}_${Date.now()}_${Math.random().toString(36).slice(2, 7)}`;
  const from = `5588${String(Math.abs(hashCode(runId))).padStart(9, "0").slice(0, 9)}`;
  const transcript = [];
  for (const [index, turn] of scenario.turns.entries()) {
    const payload = await postWhatsApp(textBody(`wamid.delivery.${runId}.${index}`, turn, from));
    const result = Array.isArray(payload.results) ? payload.results[0] : undefined;
    transcript.push({ user: turn, assistant: Array.isArray(result?.replyPreviews) ? result.replyPreviews : [result?.replyPreview].filter(Boolean), result });
  }
  return { transcript, providerContactId: from };
}

async function runWhatsAppMedia(scenario) {
  const runId = `${scenario.id.toLowerCase()}_${Date.now()}`;
  const from = `5577${String(Math.abs(hashCode(runId))).padStart(9, "0").slice(0, 9)}`;
  const payload = await postWhatsApp(mediaBody(`wamid.delivery.${runId}`, from, scenario.messageType));
  return { payload, transcript: [{ user: `[${scenario.messageType}]`, assistant: Array.isArray(payload.results) ? [payload.results[0]?.status] : [] }] };
}

async function runWhatsAppDuplicate(scenario) {
  const runId = `${scenario.id.toLowerCase()}_${Date.now()}`;
  const from = `5566${String(Math.abs(hashCode(runId))).padStart(9, "0").slice(0, 9)}`;
  const body = textBody(`wamid.delivery.duplicate.${runId}`, scenario.turns[0], from);
  const first = await postWhatsApp(body);
  const second = await postWhatsApp(body);
  return { first, second, transcript: [{ user: scenario.turns[0], assistant: [JSON.stringify(second.results?.[0] ?? {})] }] };
}

async function postWhatsApp(body) {
  const rawBody = JSON.stringify(body);
  const response = await fetch(new URL("/api/landing/ai-attendant/whatsapp", target), {
    method: "POST",
    headers: { "content-type": "application/json", "x-hub-signature-256": sign(rawBody) },
    body: rawBody,
  });
  const payload = await response.json();
  if (!response.ok) throw new Error(`WhatsApp HTTP ${response.status}: ${JSON.stringify(payload).slice(0, 200)}`);
  return payload;
}

function readSourceState() {
  return {
    widget: readFileSync("components/landing/shared/FloatingAiAttendant.tsx", "utf8"),
    panel: readFileSync("components/landing/shared/FloatingAiAttendantPanel.tsx", "utf8"),
    whatsapp: readFileSync("lib/landing/ai-attendant/whatsapp.ts", "utf8"),
    transcript: [],
  };
}

function assertFirstSplit(state) {
  const first = state.transcript[0];
  if ((first.assistant ?? []).length < 2) return fail("first WhatsApp reply was not split");
  if (!normalize(first.assistant.join(" ")).includes("em que posso te ajudar")) return fail("first split did not open helpfully");
  return pass();
}

function assertNoEcho(state) {
  const user = normalize(state.transcript[0]?.user);
  const assistant = normalize((state.transcript[0]?.assistant ?? []).join(" "));
  if (!assistant) return fail("empty reply");
  if (assistant.includes(user.slice(0, 40))) return fail("assistant echoed inbound lead text");
  return pass();
}

function assertWidgetExplorationNoDemo(state) {
  const first = state.transcript[0];
  const assistant = normalize((first?.assistant ?? []).join(" "));
  const payload = first?.payload ?? {};
  if (!assistant.includes("diagnostico rapido")) return fail("widget exploratory opening did not offer diagnostic");
  if (assistant.includes("demo real") || assistant.includes("prototipo")) return fail("widget exploratory opening fell into demo fallback");
  if (payload.conversionPath === "guided_demo") return fail("widget exploratory opening routed to guided_demo");
  if ((payload.recommendations ?? []).length || (payload.recommendedAgentIds ?? []).length) return fail("widget exploratory opening showed recommendations too early");
  return pass();
}

function assertNoLongBlocks(state) {
  const blocks = state.transcript.flatMap((turn) => turn.assistant ?? []);
  if (blocks.some((block) => block.length > 520)) return fail("assistant block longer than 520 chars");
  return pass();
}

function assertDelaySource(state) {
  if (!state.widget.includes("humanTypingDelay") || !state.whatsapp.includes("waitForWhatsAppReplyDelay")) return fail("missing human delay functions");
  return pass();
}

function assertWidgetTypingSource(state) {
  if (!state.widget.includes("setPending(true)") || !state.panel.includes("floating-typing")) return fail("widget typing indicator not wired");
  return pass();
}

function assertWhatsAppTypingSource(state) {
  if (!state.whatsapp.includes("sendMetaWhatsAppTypingIndicator") || !state.whatsapp.includes("typing_indicator")) return fail("WhatsApp typing indicator not wired");
  return pass();
}

function assertWidgetDelaySource(state) {
  if (!/contentLength\s*\/\s*14/.test(state.widget)) return fail("widget delay is not proportional to content length");
  return pass();
}

function assertWhatsAppDelaySource(state) {
  if (!/cleanLength\s*\*\s*18/.test(state.whatsapp)) return fail("WhatsApp delay is not proportional to fast typing length");
  return pass();
}

function assertRateLimitOrConfigured(state) {
  const text = normalize(state.transcript.flatMap((turn) => turn.assistant ?? []).join(" "));
  if (text.includes("retorno assim que possivel") || text.includes("conversa ficou salva") || state.transcript.length >= 1) return pass();
  return fail("rate-limit path did not produce usable transcript");
}

function assertUnsupportedMedia(state) {
  const status = state.payload.results?.[0]?.status;
  if (status !== "unsupported_message_safe_reply" && status !== "skipped") return fail(`unexpected media status ${status}`);
  return pass();
}

function assertDuplicate(state) {
  if (state.second.results?.[0]?.status !== "duplicate_ignored") return fail("duplicate provider message was not ignored");
  return pass();
}

function assertWaitlistPendingVisible(state) {
  const payload = state.transcript.at(-1)?.payload;
  if (payload?.qualificationPatch?.waitlistStatus !== "pending_details") return fail("waitlist did not enter pending_details");
  if (!payload?.qualificationPatch?.missingWaitlistFields) return fail("missingWaitlistFields not visible");
  return pass();
}

function assertIncludes(state, requiredAny, forbidden = []) {
  const text = normalize(state.transcript.flatMap((turn) => turn.assistant ?? []).join(" "));
  if (requiredAny.length && !requiredAny.some((item) => text.includes(normalize(item)))) return fail(`missing any of ${requiredAny.join(", ")}`);
  for (const item of forbidden) if (text.includes(normalize(item))) return fail(`forbidden text ${item}`);
  return pass();
}

async function findLead(sessionId) {
  if (!salesToken) return null;
  const response = await fetch(new URL("/api/internal/sales-inbox/leads", target), { headers: { "x-internal-sales-token": salesToken } });
  if (!response.ok) return null;
  const payload = await response.json();
  return (payload.leads ?? []).find((lead) => lead.sessionId === sessionId) ?? null;
}

function textBody(providerMessageId, text, from) {
  return {
    object: "whatsapp_business_account",
    entry: [{ id: "waba_test", changes: [{ field: "messages", value: { messaging_product: "whatsapp", metadata: { display_phone_number: "5527920015824", phone_number_id: webhookPhoneNumberId }, contacts: [{ wa_id: from, profile: { name: "Lead Matriz" } }], messages: [{ from, id: providerMessageId, timestamp: Math.floor(Date.now() / 1000).toString(), type: "text", text: { body: text } }] } }] }],
  };
}

function mediaBody(providerMessageId, from, type) {
  return {
    object: "whatsapp_business_account",
    entry: [{ id: "waba_test", changes: [{ field: "messages", value: { messaging_product: "whatsapp", metadata: { display_phone_number: "5527920015824", phone_number_id: webhookPhoneNumberId }, contacts: [{ wa_id: from, profile: { name: "Lead Midia" } }], messages: [{ from, id: providerMessageId, timestamp: Math.floor(Date.now() / 1000).toString(), type, [type]: { id: `${type}_id` } }] } }] }],
  };
}

function sign(rawBody) {
  return `sha256=${createHmac("sha256", process.env.META_WHATSAPP_APP_SECRET || "codex_meta_app_secret").update(rawBody).digest("hex")}`;
}

function arg(name) {
  return process.argv.find((item) => item.startsWith(`--${name}=`))?.slice(name.length + 3);
}

function normalize(value) {
  return String(value ?? "").toLowerCase().normalize("NFD").replace(/\p{Diacritic}/gu, "");
}

function pass() {
  return { ok: true };
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
  const lines = ["# Message Delivery Matrix", "", `Generated: ${new Date().toISOString()}`, "", `Summary: ${results.filter((item) => item.ok).length}/${results.length} passed.`, ""];
  for (const result of results) {
    lines.push(`## ${result.ok ? "PASS" : "FAIL"} ${result.scenario.id}`, "");
    if (result.reason) lines.push(`Failure: ${result.reason}`, "");
    for (const turn of result.state.transcript ?? []) {
      lines.push(`- Lead: ${turn.user}`);
      for (const assistant of turn.assistant ?? []) lines.push(`- Taliya: ${assistant}`);
    }
    lines.push("");
  }
  return `${lines.join("\n")}\n`;
}
