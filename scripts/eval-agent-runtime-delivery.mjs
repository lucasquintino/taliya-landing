import { assert, readJson, readText, writeReport } from "./eval-agent-runtime-utils.mjs";

const fixtures = readJson("scripts/fixtures/agent-runtime/handoff-whatsapp.json");
const whatsappRoute = readText("app/api/landing/ai-attendant/whatsapp/route.ts");
const whatsapp = readText("lib/landing/ai-attendant/whatsapp.ts");
const renderer = readText("services/taliya-agent-runtime/app/domains/taliya_commercial/renderer.py");
const templates = readText("services/taliya-agent-runtime/app/domains/taliya_commercial/templates.py");
const runtimeClient = readText("lib/landing/ai-attendant/runtime-client.ts");
const floatingPanel = readText("components/landing/shared/FloatingAiAttendantPanel.tsx");

const results = [
  assert(fixtures.some((item) => item.expectedResultStatus === "duplicate_ignored"), "duplicate webhook fixture is present"),
  assert(whatsappRoute.includes("registered.duplicate"), "WhatsApp route checks duplicate provider messages"),
  assert(whatsappRoute.includes("duplicate_ignored"), "WhatsApp route returns duplicate_ignored instead of replying twice"),
  assert(whatsappRoute.includes("createWhatsAppSemanticTurnIdempotencyKey"), "WhatsApp route creates a same-text/same-state semantic idempotency key"),
  assert(whatsappRoute.includes("whatsapp_semantic_turn"), "WhatsApp route reserves semantic turn idempotency before runtime execution"),
  assert(whatsappRoute.includes("semantic_duplicate_ignored"), "WhatsApp route skips delayed duplicate text in the same pending state"),
  assert(whatsappRoute.includes("enqueueWhatsAppTurn"), "WhatsApp route queues inbound turns before runtime processing"),
  assert(whatsappRoute.includes("acquireWhatsAppTurnLock"), "WhatsApp route serializes processing per WhatsApp conversation"),
  assert(whatsappRoute.includes("processPendingWhatsAppBatches"), "WhatsApp route drains pending split-message batches after delivery"),
  assert(whatsappRoute.includes("AI_ATTENDANT_WHATSAPP_INBOUND_DEBOUNCE_MS"), "WhatsApp route has an inbound debounce window for split user messages"),
  assert(whatsappRoute.includes("AI_ATTENDANT_WHATSAPP_POST_DELIVERY_DRAIN_MS"), "WhatsApp route has a post-delivery drain window for messages sent during chunks"),
  assert(
    whatsappRoute.includes('await waitForInboundBatchWindow("drain")') &&
      whatsappRoute.indexOf('await waitForInboundBatchWindow("drain")') < whatsappRoute.indexOf("const hasMore = await hasPendingWhatsAppTurns"),
    "WhatsApp route waits for the post-delivery drain window before releasing a conversation with no pending rows",
  ),
  assert(!whatsappRoute.includes("shouldIgnoreInterleavedWhatsAppSocialAck"), "WhatsApp route does not use text-specific social acknowledgement shortcuts"),
  assert(!whatsappRoute.includes("interleaved_social_ack_ignored"), "WhatsApp route does not silently ignore interleaved user replies by phrase"),
  assert(whatsapp.includes("ON CONFLICT (idempotency_key) DO NOTHING"), "WhatsApp outbox uses idempotency key conflict protection"),
  assert(whatsapp.includes("withMetaWhatsAppTypingKeepAlive"), "WhatsApp keep-alive helper is still available"),
  assert(
    whatsappRoute.includes("await sendMetaWhatsAppTypingIndicator") &&
      whatsappRoute.indexOf("await sendMetaWhatsAppTypingIndicator") < whatsappRoute.indexOf("response = await runAiAttendantTurn"),
    "WhatsApp webhook awaits the initial typing indicator before runtime work",
  ),
  assert(whatsappRoute.includes("startMetaWhatsAppTypingKeepAlive") && whatsappRoute.indexOf("startMetaWhatsAppTypingKeepAlive") < whatsappRoute.indexOf("runAiAttendantTurn"), "WhatsApp webhook starts typing before calling the runtime"),
  assert(whatsappRoute.includes("stopTyping()") && whatsappRoute.indexOf("sendMetaWhatsAppReplySequence") < whatsappRoute.lastIndexOf("stopTyping()"), "WhatsApp webhook keeps typing alive through chunk delivery"),
  assert(whatsapp.includes("startMetaWhatsAppTypingKeepAlive({ ...typing") === false, "WhatsApp chunk pacing uses delay instead of unsupported per-chunk typing"),
  assert(whatsapp.includes('process.env.META_WHATSAPP_GRAPH_VERSION || "v22.0"'), "WhatsApp Graph API defaults to a typing-indicator-compatible version"),
  assert(whatsapp.includes("[whatsapp-typing] failed"), "WhatsApp typing failures are logged for production debugging"),
  assert(whatsapp.includes("responseToWhatsAppTexts(response).slice") === false, "delivery slicing stays in responseToWhatsAppTexts helper"),
  assert(runtimeClient.includes("const messageLimit = stagedDiagnosticDelivery ? 12 : 3"), "runtime client preserves completed diagnostic closing chunks while capping normal turns"),
  assert(renderer.includes("render_template_plan"), "runtime renderer renders selected template plans"),
  assert(renderer.includes("channel == \"whatsapp\""), "renderer has WhatsApp-specific chunk cap"),
  assert(templates.includes("buttons_allowed"), "template registry records button/channel constraints"),
  assert(templates.includes("official_links_allowed"), "template registry records official link constraints"),
  assert(templates.includes("buttons_allowed=True"), "demo template is allowed to render as widget action"),
  assert(renderer.includes("kind = \"action\""), "renderer marks widget button-enabled links as action messages"),
  assert(runtimeClient.includes("createAssistantActionMessage"), "runtime client maps action messages to widget actions"),
  assert(
    runtimeClient.includes("spec011TransportMetadata(request.metadata)"),
    "runtime client forwards sanitized transport metadata to the LLM runtime",
  ),
  assert(
    runtimeClient.includes("delete transport.client_pending_context")
      && runtimeClient.includes("delete transport.commercial_route")
      && runtimeClient.includes("delete transport.template_id"),
    "runtime client strips legacy commercial hints from transport metadata",
  ),
  assert(floatingPanel.includes("message.action.href"), "floating panel renders assistant action hrefs"),
];

writeReport("agent-runtime-delivery", results, {
  fixtures: fixtures.map((fixture) => fixture.id),
});
