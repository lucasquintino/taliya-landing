import assert from "node:assert/strict";
import fs from "node:fs";
import Module from "node:module";
import path from "node:path";
import test from "node:test";
import vm from "node:vm";

import ts from "typescript";

const root = process.cwd();
const moduleCache = new Map();

function loadTsModule(relativePath) {
  const absolutePath = path.join(root, relativePath);
  const cached = moduleCache.get(absolutePath);
  if (cached) return cached.exports;

  const source = fs.readFileSync(absolutePath, "utf8");
  const transpiled = ts.transpileModule(source, {
    compilerOptions: {
      module: ts.ModuleKind.CommonJS,
      target: ts.ScriptTarget.ES2022,
      esModuleInterop: true,
      moduleResolution: ts.ModuleResolutionKind.Node10,
    },
    fileName: absolutePath,
  }).outputText;

  const loadedModule = { exports: {} };
  moduleCache.set(absolutePath, loadedModule);
  const localRequire = (specifier) => {
    if (specifier === "@/lib/landing/ai-attendant/schema") {
      return loadTsModule("lib/landing/ai-attendant/schema.ts");
    }
    if (specifier.startsWith("node:") || Module.builtinModules.includes(specifier)) {
      return Module.createRequire(import.meta.url)(specifier);
    }
    throw new Error(`Unsupported import in test loader: ${specifier}`);
  };
  const script = new vm.Script(
    `(function(exports, require, module, __filename, __dirname) { ${transpiled}\n})`,
    { filename: absolutePath },
  );
  script.runInThisContext()(
    loadedModule.exports,
    localRequire,
    loadedModule,
    absolutePath,
    path.dirname(absolutePath),
  );
  return loadedModule.exports;
}

function widgetRequest() {
  return {
    session: {
      sessionId: "widget_session_123",
      channelSessionId: "browser_session_123",
      leadId: "lead_widget_123",
      channel: "web",
      entryPath: "widget",
      sourceSection: "floating_agent",
      niche: "pilates",
      sourcePage: "/pilates",
      campaignStage: "commercial",
      publicOfferMode: "direct_saas_subscription",
      messages: [
        { id: "u1", role: "user", content: "quanto custa?" },
      ],
    },
    userMessage: "quanto custa?",
    metadata: { utm_source: "direct" },
  };
}

function widgetDiagnosticAcceptanceRequest() {
  return {
    session: {
      ...widgetRequest().session,
      sessionId: "widget_session_diagnostic_acceptance",
      channelSessionId: "browser_session_diagnostic_acceptance",
      leadId: "lead_widget_diagnostic_acceptance",
      messages: [
        {
          id: "a1",
          role: "assistant",
          content: "Oi. Estou aqui para te acompanhar e responder dúvidas sobre a Taliya.",
        },
        {
          id: "a2",
          role: "assistant",
          content: "Se fizer sentido para você, podemos fazer um diagnóstico gratuito do seu studio. O que você acha?",
        },
        { id: "u1", role: "user", content: "sim" },
      ],
    },
    userMessage: "sim",
  };
}

function whatsappRequest() {
  return {
    session: {
      sessionId: "whatsapp_session_123",
      channelSessionId: "wa_conv_5511999990000",
      leadId: "lead_whatsapp_123",
      channel: "whatsapp",
      entryPath: "whatsapp",
      sourceSection: "taliya_owned_whatsapp",
      niche: "pilates",
      sourcePage: "whatsapp:taliya",
      campaignStage: "commercial",
      publicOfferMode: "direct_saas_subscription",
      externalContact: {
        provider: "whatsapp",
        providerMessageId: "wamid.HBgMNTUxMTk5OTk5MDAwMA",
        phone: "+5511999990000",
        displayName: "Ana WhatsApp",
      },
      messages: [
        { id: "wa1", role: "user", content: "vi no whatsapp, serve pro meu studio?" },
      ],
    },
    userMessage: "vi no whatsapp, serve pro meu studio?",
    metadata: {
      utm_source: "whatsapp",
      client_pending_context: "legacy_hint_must_not_cross",
      commercial_route: "legacy_route_must_not_cross",
      template_id: "legacy.template_must_not_cross",
    },
  };
}

test("Spec 011 widget adapter resolves the new core endpoint", () => {
  const runtimeClient = loadTsModule("lib/landing/ai-attendant/runtime-client.ts");

  assert.equal(
    runtimeClient.resolveTaliyaCommercialRuntimeEndpointPath(widgetRequest()),
    "/v1/taliya-commercial/turn",
  );
});

test("Spec 011 widget adapter preserves ids/channel/source without commercial pending-context hints", () => {
  const runtimeClient = loadTsModule("lib/landing/ai-attendant/runtime-client.ts");
  const body = runtimeClient.createSpec011RuntimeRequestBody(widgetRequest());

  assert.equal(body.agent_key, "taliya_commercial");
  assert.equal(body.channel, "widget");
  assert.equal(body.conversation.conversation_id, "browser_session_123");
  assert.equal(body.conversation.lead_id, "lead_widget_123");
  assert.equal(body.conversation.channel_conversation_id, "browser_session_123");
  assert.equal(body.conversation.source, "pilates_landing");
  assert.equal(body.message.type, "text");
  assert.equal(body.message.text, "quanto custa?");
  assert.match(body.message.idempotency_key, /^widget:/);
  assert.equal(body.metadata.page_path, "/pilates");
  assert.equal(body.metadata.source_section, "floating_agent");
  assert.equal(body.metadata.spec011_core_contract, "taliya_commercial_core_reset_v1");
  assert.ok(Array.isArray(body.metadata.recent_client_messages));
  assert.equal(body.metadata.client_has_prior_assistant_messages, false);
  assert.equal("client_pending_context" in body.metadata, false);
});

test("Spec 011 widget adapter marks prior assistant messages for runtime context", () => {
  const runtimeClient = loadTsModule("lib/landing/ai-attendant/runtime-client.ts");
  const body = runtimeClient.createSpec011RuntimeRequestBody(
    widgetDiagnosticAcceptanceRequest(),
  );

  assert.equal(body.channel, "widget");
  assert.equal(body.message.text, "sim");
  assert.equal(body.metadata.client_has_prior_assistant_messages, true);
  assert.equal(body.metadata.recent_client_messages.length, 3);
});

test("Spec 011 WhatsApp adapter resolves the same new core endpoint", () => {
  const runtimeClient = loadTsModule("lib/landing/ai-attendant/runtime-client.ts");

  assert.equal(
    runtimeClient.resolveTaliyaCommercialRuntimeEndpointPath(whatsappRequest()),
    "/v1/taliya-commercial/turn",
  );
});

test("Spec 011 WhatsApp adapter preserves provider ids/source without commercial hints", () => {
  const runtimeClient = loadTsModule("lib/landing/ai-attendant/runtime-client.ts");
  const body = runtimeClient.createSpec011RuntimeRequestBody(whatsappRequest());

  assert.equal(body.agent_key, "taliya_commercial");
  assert.equal(body.channel, "whatsapp");
  assert.equal(body.conversation.conversation_id, "wa_conv_5511999990000");
  assert.equal(body.conversation.lead_id, "lead_whatsapp_123");
  assert.equal(body.conversation.channel_conversation_id, "wa_conv_5511999990000");
  assert.equal(body.conversation.source, "taliya_whatsapp");
  assert.equal(body.message.type, "text");
  assert.equal(body.message.text, "vi no whatsapp, serve pro meu studio?");
  assert.equal(body.message.channel_message_id, "wamid.HBgMNTUxMTk5OTk5MDAwMA");
  assert.equal(body.message.idempotency_key, "whatsapp:wamid.HBgMNTUxMTk5OTk5MDAwMA");
  assert.equal(body.sender.whatsapp_phone, "+5511999990000");
  assert.equal(body.metadata.page_path, "whatsapp:taliya");
  assert.equal(body.metadata.source_section, "taliya_owned_whatsapp");
  assert.equal(body.metadata.provider, "whatsapp");
  assert.equal(body.metadata.spec011_core_contract, "taliya_commercial_core_reset_v1");
  assert.equal("client_pending_context" in body.metadata, false);
  assert.equal("commercial_route" in body.metadata, false);
  assert.equal("template_id" in body.metadata, false);
});

test("Spec 012 adapter returns an operational reply for an empty blocked widget turn", async () => {
  const runtimeClient = loadTsModule("lib/landing/ai-attendant/runtime-client.ts");
  const previousFetch = globalThis.fetch;
  globalThis.fetch = async () => ({
    ok: true,
    json: async () => ({ status: "blocked", output: { messages: [] } }),
  });

  try {
    const response = await runtimeClient.runTaliyaCommercialRuntimeTurn(widgetRequest());

    assert.equal(response.guardrailDecision.category, "provider_failure");
    assert.equal(response.guardrailDecision.action, "fallback");
    assert.equal(response.guardrailDecision.reason, "runtime_blocked");
    assert.equal(response.shouldOfferDiagnostic, false);
    assert.equal(response.conversionPath, undefined);
    assert.equal(response.qualificationPatch.closureState, "error_needs_attention");
    assert.match(response.assistantMessages[0].content, /instabilidade|registrada/i);
    assert.doesNotMatch(response.assistantMessages[0].content, /preco|preço|plano|demo|diagnostico|diagnóstico|lista de espera/i);
  } finally {
    globalThis.fetch = previousFetch;
  }
});

test("Spec 012 adapter returns an operational reply for an invalid WhatsApp runtime status", async () => {
  const runtimeClient = loadTsModule("lib/landing/ai-attendant/runtime-client.ts");
  const previousFetch = globalThis.fetch;
  globalThis.fetch = async () => ({
    ok: true,
    json: async () => ({ status: "unknown", output: { messages: [] } }),
  });

  try {
    const response = await runtimeClient.runTaliyaCommercialRuntimeTurn(whatsappRequest());

    assert.equal(response.guardrailDecision.category, "provider_failure");
    assert.equal(response.guardrailDecision.action, "fallback");
    assert.equal(response.guardrailDecision.reason, "runtime_invalid_status");
    assert.equal(response.shouldOfferDiagnostic, false);
    assert.equal(response.conversionPath, undefined);
    assert.equal(response.qualificationPatch.leadSourceChannel, "whatsapp");
    assert.match(response.assistantMessages[0].content, /instabilidade|registrada/i);
    assert.doesNotMatch(response.assistantMessages[0].content, /preco|preço|plano|demo|diagnostico|diagnóstico|lista de espera/i);
  } finally {
    globalThis.fetch = previousFetch;
  }
});

test("Spec 012 adapter returns an operational reply for a failed HTTP 200 runtime turn", async () => {
  const runtimeClient = loadTsModule("lib/landing/ai-attendant/runtime-client.ts");
  const previousFetch = globalThis.fetch;
  globalThis.fetch = async () => ({
    ok: true,
    json: async () => ({
      run_id: "run_failed_200",
      status: "failed",
      trace_id: "trace_failed_200",
      output: { messages: [] },
    }),
  });

  try {
    const response = await runtimeClient.runTaliyaCommercialRuntimeTurn(widgetRequest());

    assert.equal(response.guardrailDecision.category, "provider_failure");
    assert.equal(response.guardrailDecision.action, "fallback");
    assert.equal(response.guardrailDecision.reason, "runtime_failed");
    assert.equal(response.qualificationPatch.closureState, "error_needs_attention");
    assert.equal(response.assistantMessages.length, 1);
    assert.match(response.assistantMessages[0].content, /seguran\u00e7a/i);
  } finally {
    globalThis.fetch = previousFetch;
  }
});

test("Spec 012 adapter returns an operational reply when a successful turn has no messages", async () => {
  const runtimeClient = loadTsModule("lib/landing/ai-attendant/runtime-client.ts");
  const previousFetch = globalThis.fetch;
  globalThis.fetch = async () => ({
    ok: true,
    json: async () => ({
      run_id: "run_empty_success",
      status: "succeeded",
      trace_id: "trace_empty_success",
      output: { messages: [] },
    }),
  });

  try {
    const response = await runtimeClient.runTaliyaCommercialRuntimeTurn(widgetRequest());

    assert.equal(response.guardrailDecision.category, "provider_failure");
    assert.equal(response.guardrailDecision.action, "fallback");
    assert.equal(response.guardrailDecision.reason, "runtime_empty_response");
    assert.equal(response.qualificationPatch.closureState, "error_needs_attention");
    assert.equal(response.assistantMessages.length, 1);
  } finally {
    globalThis.fetch = previousFetch;
  }
});

test("Spec 012 adapter returns an operational reply when the runtime cost cap is reached", () => {
  const runtimeClient = loadTsModule("lib/landing/ai-attendant/runtime-client.ts");
  const response = runtimeClient.mapRuntimeResponseToAiAttendantResponse(
    {
      run_id: "run_cost_capped",
      status: "cost_capped",
      trace_id: "trace_cost_capped",
      output: { messages: [] },
    },
    whatsappRequest(),
  );

  assert.equal(response.guardrailDecision.category, "provider_failure");
  assert.equal(response.guardrailDecision.action, "fallback");
  assert.equal(response.guardrailDecision.reason, "runtime_cost_capped");
  assert.equal(response.qualificationPatch.leadSourceChannel, "whatsapp");
  assert.equal(response.qualificationPatch.closureState, "error_needs_attention");
  assert.equal(response.assistantMessages.length, 1);
  assert.match(response.assistantMessages[0].content, /seguran\u00e7a/i);
});

test("Spec 012 adapter keeps runtime assistant ids stable across idempotent replays", () => {
  const runtimeClient = loadTsModule("lib/landing/ai-attendant/runtime-client.ts");
  const runtime = {
    run_id: "run_stable_widget_reply",
    conversation_id: "browser_session_123",
    status: "succeeded",
    trace_id: "trace_stable_widget_reply",
    current_agent: "taliya_product_agent",
    output: {
      messages: [
        { kind: "text", text: "Oi, tudo bem?" },
        { kind: "text", text: "Resposta oficial sobre o WhatsApp." },
      ],
    },
  };

  const first = runtimeClient.mapRuntimeResponseToAiAttendantResponse(runtime, widgetRequest());
  const replay = runtimeClient.mapRuntimeResponseToAiAttendantResponse(runtime, widgetRequest());

  assert.deepEqual(
    first.assistantMessages.map((message) => message.id),
    replay.assistantMessages.map((message) => message.id),
  );
  assert.equal(new Set(first.assistantMessages.map((message) => message.id)).size, 2);
  assert.ok(first.assistantMessages.every((message) => message.id.startsWith("assistant_runtime_")));
});
