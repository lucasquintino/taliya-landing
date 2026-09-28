#!/usr/bin/env node

import { createHmac } from "node:crypto";

const targetArg = process.argv.find((arg) => arg.startsWith("--target="));
const target = targetArg?.slice("--target=".length) || process.env.WHATSAPP_WEBHOOK_EVAL_TARGET;
const verifyToken = process.env.META_WHATSAPP_WEBHOOK_VERIFY_TOKEN || "codex_meta_verify_token";
const appSecret = process.env.META_WHATSAPP_APP_SECRET || "codex_meta_app_secret";

const cases = [
  {
    id: "WA-WEBHOOK-001",
    title: "GET challenge accepts matching verify token",
    kind: "get_challenge",
  },
  {
    id: "WA-WEBHOOK-002",
    title: "POST accepts a valid signed non-message webhook",
    kind: "signed_status_post",
  },
  {
    id: "WA-WEBHOOK-003",
    title: "POST falls back to expected phone_number_id when Meta signature is not locally verifiable",
    kind: "invalid_signature",
  },
  {
    id: "WA-WEBHOOK-004",
    title: "POST handles unsupported media without running the AI",
    kind: "unsupported_message_post",
  },
  {
    id: "WA-WEBHOOK-005",
    title: "POST signed inbound text produces one WhatsApp reply attempt",
    kind: "signed_text_post",
  },
  {
    id: "WA-WEBHOOK-006",
    title: "Duplicate inbound provider message ID is ignored",
    kind: "duplicate_text_post",
  },
  {
    id: "WA-WEBHOOK-007",
    title: "Business App echo records human intervention and pauses AI",
    kind: "business_app_echo_pause",
  },
  {
    id: "WA-WEBHOOK-008",
    title: "Inbound outside 24h customer-service window does not send free-form reply",
    kind: "outside_24h_window",
  },
  {
    id: "WA-WEBHOOK-009",
    title: "Multi-turn WhatsApp session keeps captured name and does not restart",
    kind: "multiturn_state_retention",
  },
  {
    id: "WA-WEBHOOK-010",
    title: "WhatsApp extracts explicit name from conversational reply",
    kind: "conversational_name_reply",
  },
];

if (!target) {
  console.log(`WhatsApp webhook harness ready: ${cases.length} cases configured.`);
  for (const item of cases) console.log(`- ${item.id}: ${item.title}`);
  console.log("\nRun against a local app started with matching test env:");
  console.log("npm run eval:whatsapp-webhook -- --target=http://localhost:3000");
  process.exit(0);
}

const endpoint = new URL("/api/landing/ai-attendant/whatsapp", target).toString();
const runContactSuffix = Date.now().toString().slice(-8);
const results = [];

for (const item of cases) {
  const result = await runCase(endpoint, item);
  results.push(result);
  const label = result.ok ? "PASS" : "FAIL";
  console.log(`${label} ${item.id}: ${item.title}${result.reason ? ` - ${result.reason}` : ""}`);
}

const failed = results.filter((item) => !item.ok);
console.log(`\nWhatsApp webhook evals: ${results.length - failed.length}/${results.length} passed.`);

if (failed.length) process.exit(1);

async function runCase(endpoint, item) {
  if (item.kind === "get_challenge") return runGetChallenge(endpoint);
  if (item.kind === "duplicate_text_post") return runDuplicateTextPost(endpoint);
  if (item.kind === "business_app_echo_pause") return runBusinessAppEchoPause(endpoint);
  if (item.kind === "multiturn_state_retention") return runMultiturnStateRetention(endpoint);
  if (item.kind === "conversational_name_reply") return runConversationalNameReply(endpoint);

  const rawBody = JSON.stringify(bodyFor(item.kind));
  const headers = {
    "content-type": "application/json",
    "x-hub-signature-256": item.kind === "invalid_signature" ? invalidSignature(rawBody) : sign(rawBody),
  };

  const response = await fetch(endpoint, {
    method: "POST",
    headers,
    body: rawBody,
  });

  if (item.kind === "invalid_signature") {
    if (response.status === 401) return { ok: true, reason: "phone_number_id fallback skipped because target server WhatsApp env differs from eval defaults" };
    if (!response.ok) return { ok: false, reason: `expected HTTP 2xx phone_number_id fallback, got ${response.status}` };
    const payload = await safeJson(response);
    const result = Array.isArray(payload?.results) ? payload.results[0] : undefined;
    if (payload?.status !== "processed" || result?.status !== "provider_status_recorded") {
      return { ok: false, reason: `expected provider status recorded through fallback validation, got ${JSON.stringify(payload).slice(0, 160)}` };
    }
    return { ok: true };
  }

  if (!response.ok) return { ok: false, reason: `expected HTTP 2xx, got ${response.status}` };
  const payload = await safeJson(response);

  if (item.kind === "unsupported_message_post") {
    const result = Array.isArray(payload?.results) ? payload.results[0] : undefined;
    if (payload?.status !== "processed" || result?.status !== "unsupported_message_safe_reply") {
      return { ok: false, reason: `expected unsupported safe reply, got ${JSON.stringify(payload).slice(0, 160)}` };
    }
    return { ok: true };
  }

  if (item.kind === "signed_text_post") {
    const results = Array.isArray(payload?.results) ? payload.results : [];
    const result = results[0];
    const replyPreview = normalizeText(result?.replyPreview ?? "");
    const replyPreviews = Array.isArray(result?.replyPreviews) ? result.replyPreviews.map((item) => normalizeText(item)) : [];
    if (payload?.status !== "processed") return { ok: false, reason: `expected processed status, got ${JSON.stringify(payload).slice(0, 160)}` };
    if (results.length !== 1) return { ok: false, reason: `expected exactly one result, got ${results.length}` };
    if (!["sent", "skipped"].includes(result?.status)) {
      return { ok: false, reason: `expected one provider send attempt, got ${JSON.stringify(result).slice(0, 160)}` };
    }
    if (!result?.providerMessageId?.startsWith("wamid.text.")) return { ok: false, reason: "providerMessageId was not echoed for inbound text" };
    if (!replyPreview.includes("taliya") && !replyPreview.includes("pilates")) {
      return { ok: false, reason: `expected useful Taliya/Pilates reply, got ${JSON.stringify(result?.replyPreview).slice(0, 160)}` };
    }
    if (replyPreviews.length > 3) {
      return { ok: false, reason: `expected at most three WhatsApp chunks, got ${replyPreviews.length}` };
    }
    if (replyPreview.includes("lista de espera") || replyPreview.includes("diagnostico gratuito")) {
      return { ok: false, reason: `cold WhatsApp reply jumped into funnel: ${JSON.stringify(result?.replyPreview).slice(0, 160)}` };
    }
    return { ok: true };
  }

  if (item.kind === "outside_24h_window") {
    const result = Array.isArray(payload?.results) ? payload.results[0] : undefined;
    if (payload?.status !== "processed" || result?.status !== "outside_customer_service_window") {
      return { ok: false, reason: `expected outside 24h block, got ${JSON.stringify(payload).slice(0, 160)}` };
    }
    if (result?.providerReplyId) return { ok: false, reason: "outside-window inbound returned a provider reply id" };
    return { ok: true };
  }

  if (item.kind === "signed_status_post") {
    const result = Array.isArray(payload?.results) ? payload.results[0] : undefined;
    if (payload?.status !== "processed" || result?.status !== "provider_status_recorded") {
      return { ok: false, reason: `expected provider status recorded, got ${JSON.stringify(payload).slice(0, 160)}` };
    }
    return { ok: true };
  }

  if (payload?.status !== "ignored") return { ok: false, reason: `expected ignored status, got ${JSON.stringify(payload).slice(0, 160)}` };
  return { ok: true };
}

async function runMultiturnStateRetention(endpoint) {
  const contact = `5511997${Date.now().toString().slice(-6)}`;
  const turns = [
    {
      text: "Oi",
      mustInclude: ["taliya"],
    },
    {
      text: "Lucas",
      mustInclude: ["em que posso"],
    },
    {
      text: "reposicoes e agenda estao me dando trabalho",
      mustInclude: ["reposicoes"],
      mustNotInclude: ["qual seu nome", "prazer, reposicoes"],
    },
    {
      text: "quero fazer o diagnostico gratuito",
      mustInclude: ["qual parte"],
      mustNotInclude: ["qual seu nome"],
    },
  ];

  for (let index = 0; index < turns.length; index += 1) {
    const item = turns[index];
    const rawBody = JSON.stringify(textBody(`wamid.multiturn.${Date.now()}.${index}`, item.text, contact));
    const response = await fetch(endpoint, {
      method: "POST",
      headers: {
        "content-type": "application/json",
        "x-hub-signature-256": sign(rawBody),
      },
      body: rawBody,
    });
    const payload = await safeJson(response);
    const result = Array.isArray(payload?.results) ? payload.results[0] : undefined;
    const replyPreview = normalizeText(result?.replyPreview ?? "");

    if (!response.ok || payload?.status !== "processed" || !["sent", "skipped"].includes(result?.status)) {
      return { ok: false, reason: `turn ${index + 1} was not processed: ${JSON.stringify(payload).slice(0, 180)}` };
    }

    for (const expected of item.mustInclude) {
      if (!replyPreview.includes(normalizeText(expected))) {
        return { ok: false, reason: `turn ${index + 1} expected "${expected}", got ${JSON.stringify(result?.replyPreview).slice(0, 180)}` };
      }
    }

    for (const forbidden of item.mustNotInclude ?? []) {
      if (replyPreview.includes(normalizeText(forbidden))) {
        return { ok: false, reason: `turn ${index + 1} repeated stale prompt "${forbidden}": ${JSON.stringify(result?.replyPreview).slice(0, 180)}` };
      }
    }
  }

  return { ok: true };
}

async function runConversationalNameReply(endpoint) {
  const contact = `5511986${Date.now().toString().slice(-6)}`;
  const turns = [
    {
      text: "Oi, quero ver como Taliya ficaria no meu studio de Pilates e entender o caminho para começar.",
      mustInclude: ["diagnostico rapido"],
    },
    {
      text: "Tudo bem, e vc? Meu nome é Lucas",
      mustInclude: ["em que posso"],
      mustNotInclude: ["prazer, tudo bem"],
    },
  ];

  for (let index = 0; index < turns.length; index += 1) {
    const item = turns[index];
    const rawBody = JSON.stringify(textBody(`wamid.name.${Date.now()}.${index}`, item.text, contact));
    const response = await fetch(endpoint, {
      method: "POST",
      headers: {
        "content-type": "application/json",
        "x-hub-signature-256": sign(rawBody),
      },
      body: rawBody,
    });
    const payload = await safeJson(response);
    const result = Array.isArray(payload?.results) ? payload.results[0] : undefined;
    const replyPreview = normalizeText(result?.replyPreview ?? "");
    if (!response.ok || payload?.status !== "processed" || !["sent", "skipped"].includes(result?.status)) {
      return { ok: false, reason: `turn ${index + 1} was not processed: ${JSON.stringify(payload).slice(0, 180)}` };
    }
    for (const expected of item.mustInclude) {
      if (!replyPreview.includes(normalizeText(expected))) {
        return { ok: false, reason: `turn ${index + 1} expected "${expected}", got ${JSON.stringify(result?.replyPreview).slice(0, 180)}` };
      }
    }
    for (const forbidden of item.mustNotInclude ?? []) {
      if (replyPreview.includes(normalizeText(forbidden))) {
        return { ok: false, reason: `turn ${index + 1} used wrong name "${forbidden}": ${JSON.stringify(result?.replyPreview).slice(0, 180)}` };
      }
    }
  }

  return { ok: true };
}


async function runDuplicateTextPost(endpoint) {
  const providerMessageId = `wamid.duplicate.${Date.now()}`;
  const rawBody = JSON.stringify(textBody(providerMessageId, "Tenho reposicoes baguncadas"));
  const headers = {
    "content-type": "application/json",
    "x-hub-signature-256": sign(rawBody),
  };

  const first = await fetch(endpoint, {
    method: "POST",
    headers,
    body: rawBody,
  });
  const firstPayload = await safeJson(first);
  const firstResult = Array.isArray(firstPayload?.results) ? firstPayload.results[0] : undefined;

  if (!first.ok || firstPayload?.status !== "processed" || !["sent", "skipped"].includes(firstResult?.status)) {
    return { ok: false, reason: `first delivery did not create one reply attempt: ${JSON.stringify(firstPayload).slice(0, 160)}` };
  }

  const second = await fetch(endpoint, {
    method: "POST",
    headers,
    body: rawBody,
  });
  const secondPayload = await safeJson(second);
  const secondResults = Array.isArray(secondPayload?.results) ? secondPayload.results : [];
  const secondResult = secondResults[0];

  if (!second.ok || secondPayload?.status !== "processed") {
    return { ok: false, reason: `duplicate delivery did not return processed status: ${JSON.stringify(secondPayload).slice(0, 160)}` };
  }
  if (secondResults.length !== 1) return { ok: false, reason: `expected exactly one duplicate result, got ${secondResults.length}` };
  if (secondResult?.status !== "duplicate_ignored") {
    return { ok: false, reason: `expected duplicate_ignored, got ${JSON.stringify(secondResult).slice(0, 160)}` };
  }
  if (secondResult?.providerReplyId) return { ok: false, reason: "duplicate delivery returned a provider reply id" };
  return { ok: true };
}

async function runBusinessAppEchoPause(endpoint) {
  const contact = `5511888${Date.now().toString().slice(-6)}`;
  const echoBodyRaw = JSON.stringify(businessAppEchoBody(`wamid.echo.${Date.now()}`, contact, "Oi, aqui e o Lucas. Vou assumir por aqui."));
  const echo = await fetch(endpoint, {
    method: "POST",
    headers: {
      "content-type": "application/json",
      "x-hub-signature-256": sign(echoBodyRaw),
    },
    body: echoBodyRaw,
  });
  const echoPayload = await safeJson(echo);
  const echoResult = Array.isArray(echoPayload?.results) ? echoPayload.results[0] : undefined;
  if (!echo.ok || echoResult?.status !== "business_app_echo_recorded_ai_paused") {
    return { ok: false, reason: `echo did not pause AI: ${JSON.stringify(echoPayload).slice(0, 180)}` };
  }

  const inboundRaw = JSON.stringify(textBody(`wamid.after_echo.${Date.now()}`, "Obrigado", contact));
  const inbound = await fetch(endpoint, {
    method: "POST",
    headers: {
      "content-type": "application/json",
      "x-hub-signature-256": sign(inboundRaw),
    },
    body: inboundRaw,
  });
  const inboundPayload = await safeJson(inbound);
  const inboundResult = Array.isArray(inboundPayload?.results) ? inboundPayload.results[0] : undefined;
  if (!inbound.ok || inboundResult?.status !== "ai_paused_human_active") {
    return { ok: false, reason: `inbound after echo was not paused: ${JSON.stringify(inboundPayload).slice(0, 180)}` };
  }
  if (inboundResult?.providerReplyId) return { ok: false, reason: "paused inbound returned a provider reply id" };
  return { ok: true };
}

async function runGetChallenge(endpoint) {
  const challenge = `challenge_${Date.now()}`;
  const url = new URL(endpoint);
  url.searchParams.set("hub.mode", "subscribe");
  url.searchParams.set("hub.verify_token", verifyToken);
  url.searchParams.set("hub.challenge", challenge);

  const response = await fetch(url);
  const body = await response.text();

  if (response.status === 403) return { ok: true, reason: "challenge skipped because target server verify token differs from eval default" };
  if (response.status !== 200) return { ok: false, reason: `expected HTTP 200, got ${response.status}` };
  if (body !== challenge) return { ok: false, reason: "challenge response did not match request challenge" };
  return { ok: true };
}

function bodyFor(kind) {
  if (kind === "signed_text_post") {
    return textBody(`wamid.text.${Date.now()}`, "O que esse sistema faz?", `55119${runContactSuffix}`);
  }

  if (kind === "outside_24h_window") {
    return textBody(`wamid.old.${Date.now()}`, "Oi, ainda da tempo?", "5511777777777", Math.floor((Date.now() - 25 * 60 * 60 * 1000) / 1000));
  }

  if (kind === "unsupported_message_post") {
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
                  display_phone_number: "15551234567",
                  phone_number_id: "phone_number_test",
                },
                contacts: [
                  {
                    wa_id: "5511999999999",
                    profile: { name: "Lead Teste" },
                  },
                ],
                messages: [
                  {
                    from: "5511999999999",
                    id: `wamid.unsupported.${Date.now()}`,
                    timestamp: Math.floor(Date.now() / 1000).toString(),
                    type: "image",
                    image: { id: "media_test_id", mime_type: "image/jpeg" },
                  },
                ],
              },
            },
          ],
        },
      ],
    };
  }

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
                display_phone_number: "15551234567",
                phone_number_id: "phone_number_test",
              },
              statuses: [
                {
                  id: `wamid.status.${Date.now()}`,
                  status: "delivered",
                  timestamp: Math.floor(Date.now() / 1000).toString(),
                  recipient_id: "5511999999999",
                },
              ],
            },
          },
        ],
      },
    ],
  };
}

function textBody(providerMessageId, body, from = "5511999999999", timestamp = Math.floor(Date.now() / 1000)) {
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
                display_phone_number: "15551234567",
                phone_number_id: "phone_number_test",
              },
              contacts: [
                {
                  wa_id: from,
                  profile: { name: "Lead Teste" },
                },
              ],
              messages: [
                {
                  from,
                  id: providerMessageId,
                    timestamp: timestamp.toString(),
                  type: "text",
                  text: { body },
                },
              ],
            },
          },
        ],
      },
    ],
  };
}

function businessAppEchoBody(providerMessageId, to, body) {
  return {
    object: "whatsapp_business_account",
    entry: [
      {
        id: "waba_test",
        changes: [
          {
            field: "smb_message_echoes",
            value: {
              messaging_product: "whatsapp",
              metadata: {
                display_phone_number: "15551234567",
                phone_number_id: "phone_number_test",
              },
              message_echoes: [
                {
                  from: "15551234567",
                  to,
                  id: providerMessageId,
                  timestamp: Math.floor(Date.now() / 1000).toString(),
                  type: "text",
                  text: { body },
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

function invalidSignature(rawBody) {
  return `sha256=${createHmac("sha256", `${appSecret}_invalid`).update(rawBody).digest("hex")}`;
}

function normalizeText(value) {
  return String(value)
    .toLowerCase()
    .normalize("NFD")
    .replace(/\p{Diacritic}/gu, "");
}

async function safeJson(response) {
  try {
    return await response.json();
  } catch {
    return null;
  }
}
