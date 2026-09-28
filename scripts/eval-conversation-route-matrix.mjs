#!/usr/bin/env node

import { readFileSync } from "node:fs";
import { resolve } from "node:path";

const fixturePath = resolve("specs/002-floating-ai-sales-agent/evals/conversation-route-matrix.md");
const targetArg = process.argv.find((arg) => arg.startsWith("--target="));
const target = targetArg?.slice("--target=".length) || process.env.AI_ATTENDANT_EVAL_TARGET;
const salesTokenArg = process.argv.find((arg) => arg.startsWith("--sales-token="));
const salesToken = salesTokenArg?.slice("--sales-token=".length) || process.env.INTERNAL_SALES_INBOX_TOKEN;
const caseArg = process.argv.find((arg) => arg.startsWith("--case="));
const caseFilter = caseArg
  ? new Set(caseArg.slice("--case=".length).split(",").map((item) => normalizeCaseId(item)).filter(Boolean))
  : undefined;
const runId = `run_${Date.now().toString(36)}_${Math.random().toString(36).slice(2, 8)}`;
const text = readFileSync(fixturePath, "utf8");
const cases = parseCases(text);

if (!cases.length) {
  console.error("No CASE-* fixtures found.");
  process.exit(1);
}

if (!target) {
  const missing = cases.filter((item) => !item.channel || !item.entryPath || !item.input.length);
  if (missing.length) {
    console.error(`Fixture validation failed: ${missing.length} cases are missing channel, entry path or input.`);
    for (const item of missing) console.error(`- ${item.id}: ${item.title}`);
    process.exit(1);
  }

  console.log(`Fixture validation passed: ${cases.length} route-matrix cases found.`);
  console.log("Run against a local app with: npm run eval:ai-routes -- --target=http://localhost:3000");
  process.exit(0);
}

const endpoint = new URL("/api/landing/ai-attendant", target).toString();
const salesInboxEndpoint = new URL("/api/internal/sales-inbox/leads", target).toString();
const runnable = cases.filter(
  (item) =>
    (!caseFilter || caseFilter.has(normalizeCaseId(item.id))) &&
    !item.input.some((line) => /system\/operator action|provider message id|existing lead/i.test(line)) &&
    !requiresUnavailableConfig(item),
);
const results = [];

for (const item of runnable) {
  const result = await runCase(endpoint, salesInboxEndpoint, item);
  results.push(result);
  const icon = result.ok ? "PASS" : "FAIL";
  console.log(`${icon} ${item.id}: ${item.title}${result.reason ? ` - ${result.reason}` : ""}`);
}

const failed = results.filter((item) => !item.ok);
console.log(`\nRoute-matrix evals: ${results.length - failed.length}/${results.length} passed (${cases.length - runnable.length} skipped).`);

if (failed.length) process.exit(1);

function normalizeCaseId(value) {
  if (!value) return "";
  const normalized = value.toUpperCase().replace(/^CASE-?/, "").replace(/^CRM-?/, "CRM-");
  return normalized.startsWith("CRM-") ? `CASE-${normalized}` : `CASE-${normalized}`;
}

function parseCases(markdown) {
  const chunks = markdown.split(/^## CASE-/m).slice(1);
  return chunks.map((chunk) => {
    const [heading, ...rest] = chunk.split("\n");
    const [idPart, ...titleParts] = heading.split(":");
    const body = rest.join("\n");
    return {
      id: `CASE-${idPart.trim()}`,
      title: titleParts.join(":").trim(),
      body,
      channel: field(body, "Channel")?.replaceAll("`", "").trim(),
      entryPath: field(body, "Entry Path")?.replaceAll("`", "").trim(),
      input: listAfter(body, "Input"),
      mustInclude: listAfter(body, "Must Include"),
      expectedConversionPaths: expectedPaths(body, "Expected Conversion Path"),
      expectedCta: field(body, "Expected CTA/Handoff")?.replaceAll("`", "").trim(),
      expectedLeadEffect: field(body, "Expected Status/Lead Effect")?.replaceAll("`", "").trim(),
      nextQuestionPolicy: expectedNextQuestionPolicy(body),
      contactCapturePolicy: expectedContactCapturePolicy(body),
      expectedGuardrail: expectedGuardrail(body),
      mustNotInclude: listAfter(body, "Must Not Include"),
      requiresGuidedDemoReady: /guidedDemoReady:\s*true/i.test(body),
    };
  });
}

function field(body, label) {
  const match = body.match(new RegExp(`^\\s*- ${escapeRegExp(label)}: (.+)$`, "m"));
  return match?.[1];
}

function listAfter(body, label) {
  const lines = body.split("\n");
  const start = lines.findIndex((line) => line.trim() === `- ${label}:`);
  if (start === -1) return [];
  const values = [];
  for (let index = start + 1; index < lines.length; index += 1) {
    const line = lines[index].trimEnd();
    if (/^- [A-Z]/.test(line)) break;
    const value = line.match(/^\s+- (.+)$/)?.[1]?.trim();
    if (value) values.push(value.replace(/^"|"$/g, ""));
  }
  return values;
}

function expectedPaths(body, label) {
  const value = field(body, label);
  if (!value) return [];
  const paths = [...value.matchAll(/`([^`]+)`/g)].map((match) => match[1]);
  if (/\bnone\b/i.test(value)) paths.push("none");
  if (/\bonly if\b|\botherwise\b|\bunless\b/i.test(value)) paths.push("none");
  return paths;
}

function expectedGuardrail(body) {
  const value = field(body, "Expected Guardrail Decision");
  if (!value) return undefined;
  if (/refuse|redirect|stop|guardrail|minimize|unsafe/i.test(value)) return "not_allowed";
  return undefined;
}

function expectedNextQuestionPolicy(body) {
  const value = `${field(body, "Expected CTA/Handoff") ?? ""} ${field(body, "Expected Status/Lead Effect") ?? ""}`.toLowerCase();
  if (/terminal|opt-out|stop automation|no automated reply|checkout only|none/.test(value)) return "optional";
  return "required";
}

function expectedContactCapturePolicy(body) {
  const combined = `${field(body, "Expected CTA/Handoff") ?? ""}\n${field(body, "Expected Status/Lead Effect") ?? ""}\n${listAfter(body, "Must Include").join("\n")}\n${listAfter(body, "Must Not Include").join("\n")}`.toLowerCase();
  if (/must not include:\s*contact capture|contact capture|no lead until/.test(combined) && /must not include/i.test(body)) return "forbidden";
  if (/ask whatsapp|ask.*email|whatsapp\/email|email or whatsapp|contact if missing|contact\/high intent|contact exists|contact capture/.test(combined)) return "required";
  return "optional";
}

async function runCase(endpoint, salesInboxEndpoint, item) {
  const userMessage = firstVisitorMessage(item.input);
  const quickReplyId = userMessage ? undefined : "start_conversation";
  const sessionId = `eval_${runId}_${item.id.toLowerCase().replaceAll("-", "_")}`;

  const response = await fetch(endpoint, {
    method: "POST",
    headers: { "content-type": "application/json" },
    body: JSON.stringify({
      session: {
        sessionId,
        channel: item.channel === "whatsapp" ? "whatsapp" : "web",
        entryPath: normalizeEntryPath(item.entryPath),
        niche: "pilates",
        sourcePage: item.channel === "whatsapp" ? "whatsapp" : "/pilates",
        campaignStage: "commercial",
        publicOfferMode: "direct_saas_subscription",
        messages: [],
      },
      userMessage,
      quickReplyId,
      pageSignals: pageSignals(item.body),
    }),
  });

  if (!response.ok) return { ok: false, reason: `HTTP ${response.status}` };
  const payload = await response.json();
  const answerText = Array.isArray(payload.assistantMessages)
    ? payload.assistantMessages.map((message) => message.content || "").join("\n").toLowerCase()
    : "";
  const normalizedAnswer = normalizeText(answerText);

  for (const prohibited of item.mustNotInclude) {
    const probe = normalizeText(prohibited.replaceAll("`", ""));
    if (probe && normalizedAnswer.includes(probe)) return { ok: false, reason: `included prohibited text: ${prohibited}` };
    if (/checkout cta|immediate checkout|cold.*checkout|route.*checkout/.test(probe) && payload.conversionPath === "checkout_intent") {
      return { ok: false, reason: `showed checkout path despite prohibition: ${prohibited}` };
    }
    if (/model-generated arbitrary checkout url/.test(probe) && payload.subscription?.checkoutUrl && !isTrustedRelativeUrl(payload.subscription.checkoutUrl)) {
      return { ok: false, reason: `checkout URL is not a trusted relative/configured URL: ${payload.subscription.checkoutUrl}` };
    }
    if (/route directly|diretamente/.test(probe) && payload.conversionPath) {
      return { ok: false, reason: `routed directly despite prohibition: ${prohibited}` };
    }
    if (/contact capture|ask.*whatsapp|ask.*email|pede.*contato/.test(probe) && asksForContact(normalizedAnswer)) {
      return { ok: false, reason: `asked for contact despite prohibition: ${prohibited}` };
    }
  }

  if (item.expectedGuardrail === "not_allowed" && payload.guardrailDecision?.category === "allowed") {
    return { ok: false, reason: "expected guardrail/non-allowed decision" };
  }

  if (item.expectedConversionPaths.length) {
    const actual = payload.conversionPath ?? "none";
    if (!item.expectedConversionPaths.includes(actual)) {
      return { ok: false, reason: `expected conversionPath ${item.expectedConversionPaths.join("|")}, got ${actual}` };
    }
  }

  if (item.nextQuestionPolicy === "required" && payload.guardrailDecision?.category === "allowed" && !isTerminalConversion(payload.conversionPath)) {
    if (!payload.nextQuestion && !/\?/.test(answerText)) {
      return { ok: false, reason: "expected a nextQuestion or a clear question in the assistant answer" };
    }
  }

  const ctaResult = assertCtaPolicy(item, payload);
  if (!ctaResult.ok) return ctaResult;

  if (item.contactCapturePolicy === "required" && !asksForContact(normalizedAnswer)) {
    return { ok: false, reason: "expected contact capture or contact question" };
  }

  const leadResult = salesToken ? await assertSalesInboxEffect(salesInboxEndpoint, item, payload, sessionId) : { ok: true };
  if (!leadResult.ok) return leadResult;

  return { ok: true };
}

function isTrustedRelativeUrl(value) {
  return typeof value === "string" && value.startsWith("/");
}

function assertCtaPolicy(item, payload) {
  const expected = normalizeText(item.expectedCta ?? "");
  const actual = payload.conversionPath ?? "none";
  const hasPlansExpectation = /planos|plans|comparativo|\/pilates\/planos/.test(expected);
  const hasCheckoutExpectation = /checkout|assinatura/.test(expected);
  const hasHumanExpectation = /whatsapp|humano|human/.test(expected);
  const checkoutIsGated = /only after|not|nao|nÃ£o|gate|before|after|confirm|recommended|recomend/.test(expected);
  const plansAreGated = /only if|not|nao|nÃ£o|gate|before|after|confirm|unless/.test(expected);

  if (/none/.test(expected) && actual !== "none") {
    return { ok: false, reason: `expected no CTA/conversion, got ${actual}` };
  }
  if (hasPlansExpectation && !plansAreGated && !["view_plans", "plan_recommendation", "custom_agent_diagnostic_mapped"].includes(actual)) {
    return { ok: false, reason: `expected plans/comparison CTA, got ${actual}` };
  }
  if (hasCheckoutExpectation && !checkoutIsGated && actual !== "checkout_intent" && payload.guardrailDecision?.category === "allowed") {
    return { ok: false, reason: `expected checkout CTA, got ${actual}` };
  }
  if (hasHumanExpectation && !hasPlansExpectation && !hasCheckoutExpectation && !["human_whatsapp_assist", "custom_agent_follow_up", "mixed_subscription_plus_custom"].includes(actual) && actual !== "none") {
    return { ok: false, reason: `expected WhatsApp/human/custom handoff policy, got ${actual}` };
  }

  return { ok: true };
}

async function assertSalesInboxEffect(endpoint, item, payload, sessionId) {
  const expected = normalizeText(item.expectedLeadEffect ?? "");
  const actualConversionPath = payload.conversionPath;
  const shouldHaveLead = Boolean(actualConversionPath) && !/no lead until|safety event|avoid raw|none/.test(expected);

  if (!shouldHaveLead) return { ok: true };

  const response = await fetch(endpoint, {
    headers: {
      "x-internal-sales-token": salesToken,
    },
  });

  if (!response.ok) return { ok: false, reason: `Sales Inbox check failed with HTTP ${response.status}` };
  const body = await response.json();
  const leads = Array.isArray(body.leads) ? body.leads : [];
  const lead = leads.find((item) => item.sessionId === sessionId && item.conversionPath === actualConversionPath);

  if (!lead) return { ok: false, reason: "expected Sales Inbox lead for conversion path but none was found" };
  const syncStatus = lead.externalSyncStatus;
  if (!["pending", "synced", "failed", "skipped"].includes(syncStatus)) {
    return { ok: false, reason: `unexpected Sales Inbox sync status: ${syncStatus}` };
  }

  return { ok: true };
}

function requiresUnavailableConfig(item) {
  return item.requiresGuidedDemoReady;
}

function isTerminalConversion(conversionPath) {
  return conversionPath === "checkout_intent" || conversionPath === "human_whatsapp_assist" || conversionPath === "guided_demo";
}

function asksForContact(text) {
  return /\b(whatsapp|email|e-mail|telefone|celular|contato)\b/.test(text) && /\b(qual|deixar|passar|usar|continuar|retornar|retorno)\b/.test(text);
}

function normalizeText(value) {
  return value
    .toLowerCase()
    .normalize("NFD")
    .replace(/\p{Diacritic}/gu, "");
}

function firstVisitorMessage(inputLines) {
  const quoted = inputLines.find((line) => /^".+"$/.test(line));
  if (quoted) return quoted.slice(1, -1);
  const plain = inputLines.find((line) => !/^visitor opens|visitor clicks|system condition/i.test(line));
  return plain?.replace(/^Visitor sends: /i, "").replace(/^"|"$/g, "");
}

function normalizeEntryPath(entryPath) {
  if (["widget", "consultor_cta", "whatsapp_cta", "guided_demo", "plans_page"].includes(entryPath)) return entryPath;
  return "widget";
}

function pageSignals(body) {
  const signals = {};
  const selectedPainId = field(body, "selectedPainId");
  const selectedAgentId = field(body, "selectedAgentId");
  const calculatorEstimate = field(body, "calculatorEstimate");
  if (selectedPainId && selectedPainId !== "none") signals.selectedPainId = selectedPainId.replaceAll("`", "").trim();
  if (selectedAgentId && selectedAgentId !== "none") signals.selectedAgentId = selectedAgentId.replaceAll("`", "").trim();
  if (calculatorEstimate && Number.isFinite(Number(calculatorEstimate))) signals.calculatorEstimate = Number(calculatorEstimate);
  return signals;
}

function escapeRegExp(value) {
  return value.replace(/[.*+?^${}()|[\]\\]/g, "\\$&");
}
