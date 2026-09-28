import { createHmac, randomUUID } from "crypto";

import { createAssistantActionMessage, createAssistantMessage } from "@/lib/landing/ai-attendant/schema";
import type {
  AiAttendantIntent,
  AiAttendantRequest,
  AiAttendantResponse,
  ConversionPath,
  QualificationDraft,
} from "@/lib/landing/ai-attendant/schema";

type RuntimeChannel = "widget" | "whatsapp";

type RuntimeAgentOutput = {
  decision?: {
    previous_state?: string;
    current_state?: string;
    next_state?: string;
    route?: string;
    detected_intents?: string[];
    template_ids?: string[];
    diagnostic_ledger_status?: string;
    diagnostic_action?: string;
    demo_status?: string;
    demo_next_step?: string;
    waitlist_allowed_now?: boolean;
    facts_used?: string[];
    facts_missing?: string[];
  };
  messages?: Array<{
    text?: string;
    channel_hint?: RuntimeChannel;
    kind?: string;
    template_id?: string | null;
    requires_product_source?: boolean;
  }>;
  lead_facts?: Array<{ key?: string; value?: string; confidence?: string; evidence?: string[] }>;
  diagnostic?: {
    status?: string;
    ledger?: Array<{
      question_key?: string;
      answer_value?: string | null;
      areas?: string[];
      status?: string;
      confidence?: string;
      evidence?: string[];
    }>;
    facts_used?: string[];
    main_bottleneck?: string | null;
    crm_base_recommendation?: string | null;
    indicated_agents?: Array<Record<string, unknown>>;
    plan_or_range_to_compare?: string | null;
    final_plan_line?: string | null;
    demo_status_at_delivery?: string | null;
    final_demo_line?: string | null;
    final_demo_next_step_question?: string | null;
    evidence?: string[];
    confidence?: string;
    next_question?: string | null;
  } | null;
  waitlist_action?: {
    status?: string;
    reason?: string | null;
    missing_fields?: string[];
  } | null;
  handoff?: {
    status?: string;
    reason?: string | null;
  } | null;
  sources?: Array<{ type?: string; version?: string; keys?: string[] }>;
  safety_flags?: string[];
  usage?: {
    model?: string | null;
    model_operations?: number;
    input_tokens?: number;
    cached_input_tokens?: number;
    cache_write_input_tokens?: number;
    output_tokens?: number;
    reasoning_tokens?: number;
    repairs?: number;
    latency_ms?: number;
    cost_usd?: number;
  };
  confidence?: string;
  sales_inbox_projection?: {
    conversation_id?: string;
    lead_id?: string | null;
    commercial_stage?: string;
    summary?: string;
    diagnostic_status?: string;
    waitlist_status?: string;
    handoff_status?: string;
    identity?: Array<{
      key?: string;
      value?: string;
      source?: string;
      verified?: boolean;
    }>;
    fields?: Record<string, unknown>;
  };
};

type RuntimeAgentRunResponse = {
  contract_version?: string;
  run_id?: string;
  conversation_id?: string;
  lead_id?: string | null;
  agent_key?: string;
  current_agent?: string;
  status?: "succeeded" | "failed" | "blocked" | "human_paused" | "cost_capped";
  output?: RuntimeAgentOutput;
  trace_id?: string;
  input_snapshot?: {
    contract_version?: string;
    channel?: RuntimeChannel;
    conversation_id?: string;
    lead_id?: string | null;
    message_id?: string;
  } | null;
};

const COMMERCIAL_OPS_CONTRACT_VERSION = "taliya-commercial-ops.v1";

export async function runTaliyaCommercialRuntimeTurn(request: AiAttendantRequest): Promise<AiAttendantResponse> {
  const localRuntime = process.env.NODE_ENV !== "production" ? "http://127.0.0.1:8088" : undefined;
  const url = (process.env.TALIYA_AGENT_RUNTIME_URL ?? localRuntime)?.replace(/\/+$/g, "");
  const secret = process.env.TALIYA_AGENT_RUNTIME_HMAC_SECRET ?? (process.env.NODE_ENV !== "production" ? "dev-secret" : undefined);
  if (!url || !secret) return createOperationalFallbackResponse("runtime_not_configured", request);

  const body = JSON.stringify(createSpec011RuntimeRequestBody(request));
  const timestamp = new Date().toISOString().replace(/\.\d{3}Z$/, "Z");
  const requestId = createRuntimeRequestId(request);
  const timeoutMs = Number(process.env.TALIYA_AGENT_RUNTIME_TIMEOUT_MS || 60000);
  const controller = new AbortController();
  const timeout = setTimeout(() => controller.abort(), Number.isFinite(timeoutMs) ? timeoutMs : 60000);

  try {
    const response = await fetch(`${url}${resolveTaliyaCommercialRuntimeEndpointPath(request)}`, {
      method: "POST",
      headers: {
        "content-type": "application/json",
        "x-taliya-agent-timestamp": timestamp,
        "x-taliya-agent-request-id": requestId,
        "x-taliya-agent-signature": signRuntimeRequest(secret, timestamp, body),
      },
      body,
      signal: controller.signal,
    });
    const payload = (await response.json().catch(() => null)) as unknown;
    if (!response.ok) {
      const errorCode = getRuntimeErrorCode(payload, `http_${response.status}`);
      return createOperationalFallbackResponse(errorCode, request);
    }
    const runtime = parseRuntimeAgentRunResponse(payload);
    if (!runtime) return createOperationalFallbackResponse("runtime_invalid_contract", request);
    return mapRuntimeResponseToAiAttendantResponse(runtime, request);
  } catch (error) {
    return createOperationalFallbackResponse(error instanceof Error ? error.name : "runtime_fetch_failed", request);
  } finally {
    clearTimeout(timeout);
  }
}

export function resolveTaliyaCommercialRuntimeEndpointPath(request: AiAttendantRequest) {
  void request;
  return "/v1/taliya-commercial/turn";
}

export async function syncTaliyaCommercialRuntimeHandoffState({
  actorUserId,
  lead,
  mode,
  reason,
}: {
  actorUserId: string;
  lead: {
    leadId: string;
    sessionId: string;
    channel: "web" | "whatsapp";
    channelSessionId?: string;
    contact?: { providerContactId?: string; normalizedWhatsapp?: string; whatsapp?: string };
  };
  mode: "pause" | "resume";
  reason: string;
}): Promise<{ ok: true; status?: string; traceId?: string } | { ok: false; reason: string }> {
  const url = process.env.TALIYA_AGENT_RUNTIME_URL?.replace(/\/+$/g, "");
  const localRuntime = process.env.NODE_ENV !== "production" ? "http://127.0.0.1:8088" : undefined;
  const resolvedUrl = (url ?? localRuntime)?.replace(/\/+$/g, "");
  const secret = process.env.TALIYA_AGENT_RUNTIME_HMAC_SECRET ?? (process.env.NODE_ENV !== "production" ? "dev-secret" : undefined);
  if (!resolvedUrl || !secret) return { ok: false, reason: "runtime_not_configured" };

  const channel = mapRuntimeChannel(lead.channel);
  const body = JSON.stringify({
    agent_key: process.env.TALIYA_AGENT_RUNTIME_AGENT_KEY || "taliya_commercial",
    channel,
    conversation: {
      conversation_id: lead.channelSessionId || lead.sessionId || lead.leadId,
      lead_id: lead.leadId,
      channel_conversation_id: lead.channelSessionId,
      source: channel === "whatsapp" ? "sales_inbox_whatsapp_control" : "sales_inbox_widget_control",
      entry_intent: "operator_handoff_control",
    },
    message: {
      idempotency_key: `runtime-control:${lead.leadId}:${mode}:${Date.now()}`,
      type: "text",
      text: mode === "resume" ? "operator resumed automation" : "operator paused automation",
      timestamp: new Date().toISOString(),
    },
    sender: {
      whatsapp_phone: lead.contact?.normalizedWhatsapp ?? lead.contact?.whatsapp,
    },
    metadata: {
      runtime_control: {
        action: mode === "resume" ? "resume_human" : "pause_human",
        reason,
        actor_user_id: actorUserId,
      },
    },
  });
  const timestamp = new Date().toISOString().replace(/\.\d{3}Z$/, "Z");
  const requestId = `runtime-control:${lead.leadId}:${mode}:${hashShort(`${reason}:${timestamp}`)}`;

  try {
    const response = await fetch(`${resolvedUrl}/v1/agent-runs`, {
      method: "POST",
      headers: {
        "content-type": "application/json",
        "x-taliya-agent-timestamp": timestamp,
        "x-taliya-agent-request-id": requestId,
        "x-taliya-agent-signature": signRuntimeRequest(secret, timestamp, body),
      },
      body,
    });
    const payload = (await response.json().catch(() => null)) as unknown;
    if (!response.ok) {
      const code = getRuntimeErrorCode(payload, `http_${response.status}`);
      return { ok: false, reason: code };
    }
    const runtime = payload as RuntimeAgentRunResponse;
    return { ok: true, status: runtime.status, traceId: runtime.trace_id };
  } catch (error) {
    return { ok: false, reason: error instanceof Error ? error.message : "runtime_control_failed" };
  }
}

export function signRuntimeRequest(secret: string, timestamp: string, body: string) {
  return createHmac("sha256", secret).update(`${timestamp}.${body}`).digest("hex");
}

export function createSpec011RuntimeRequestBody(request: AiAttendantRequest) {
  const channel = mapRuntimeChannel(request.session.channel);
  const safeMetadata = spec011TransportMetadata(request.metadata);
  const runtimeEntryIntent = request.pageSignals?.aiRouteIntent || request.quickReplyId || request.session.entryPath;
  const runtimeMessageText = request.userMessage || lastUserMessageText(request) || request.quickReplyId || "";
  const recentClientMessages = request.session.messages.slice(-8).map((message) => ({
    role: message.role,
    content: message.content,
    intent: message.intent,
  }));

  return {
    contract_version: COMMERCIAL_OPS_CONTRACT_VERSION,
    agent_key: process.env.TALIYA_AGENT_RUNTIME_AGENT_KEY || "taliya_commercial",
    channel,
    conversation: {
      conversation_id: request.session.channelSessionId || request.session.sessionId,
      lead_id: request.session.leadId ?? null,
      channel_conversation_id: request.session.channelSessionId,
      source: request.session.channel === "whatsapp" ? "taliya_whatsapp" : "pilates_landing",
      entry_intent: runtimeEntryIntent,
    },
    message: {
      idempotency_key: createRuntimeRequestId(request),
      channel_message_id: request.session.externalContact?.providerMessageId,
      type: "text",
      text: runtimeMessageText,
      timestamp: new Date().toISOString(),
    },
    sender: {
      name: request.session.qualificationDraft?.name,
      whatsapp_phone: request.session.externalContact?.phone,
      email: request.session.qualificationDraft?.email,
    },
    metadata: {
      ...safeMetadata,
      spec011_core_contract: "taliya_commercial_core_reset_v1",
      page_path: request.session.sourcePage,
      source_section: request.session.sourceSection,
      provider: channel,
      campaign_stage: request.session.campaignStage,
      public_offer_mode: request.session.publicOfferMode,
      selected_pain_ids: request.session.selectedPainIds ?? [],
      recommended_agent_ids: request.session.recommendedAgentIds ?? [],
      qualification: request.session.qualificationDraft ?? {},
      quick_reply_id: request.quickReplyId,
      page_signals: request.pageSignals ?? {},
      client_has_prior_assistant_messages: recentClientMessages.some(
        (message) => message.role === "assistant",
      ),
      recent_client_messages: recentClientMessages,
    },
  };
}

function spec011TransportMetadata(metadata?: Record<string, unknown>) {
  if (!metadata) return {};
  const transport = { ...metadata };
  delete transport.client_pending_context;
  delete transport.commercial_route;
  delete transport.template_id;
  return transport;
}

function lastUserMessageText(request: AiAttendantRequest) {
  return [...request.session.messages].reverse().find((message) => message.role === "user")?.content?.trim();
}

export function mapRuntimeResponseToAiAttendantResponse(
  runtime: RuntimeAgentRunResponse,
  request: AiAttendantRequest,
): AiAttendantResponse {
  const output = runtime.output ?? {};
  const stagedDiagnosticDelivery = output.decision?.template_ids?.some((templateId) => templateId.startsWith("diagnostic.deliver_")) ?? false;
  const messageLimit = stagedDiagnosticDelivery ? 12 : 3;
  const assistantMessages = (output.messages ?? [])
    .map((message, index) => mapRuntimeMessageToAssistantMessage(message, runtime, request, index))
    .filter((message): message is NonNullable<typeof message> => Boolean(message))
    .slice(0, messageLimit);

  if (runtime.status === "failed" || runtime.status === "cost_capped") {
    return createOperationalFallbackResponse(`runtime_${runtime.status}`, request);
  }
  if (!runtime.status || !["succeeded", "blocked", "human_paused"].includes(runtime.status)) {
    return createOperationalFallbackResponse("runtime_invalid_status", request);
  }
  if (runtime.status !== "human_paused" && assistantMessages.length === 0) {
    return createOperationalFallbackResponse(
      runtime.status === "blocked" ? "runtime_blocked" : "runtime_empty_response",
      request,
    );
  }

  return {
    assistantMessages,
    capturedPainIds: painIdsFromRuntimeOutput(output),
    recommendedAgentIds: agentIdsFromDiagnostic(output.diagnostic),
    recommendations: undefined,
    nextQuestion: output.diagnostic?.next_question ?? undefined,
    conversionPath: conversionPathFromRuntime(runtime),
    shouldOfferDiagnostic: output.diagnostic?.status === "offered" || output.diagnostic?.status === "in_progress",
    qualificationPatch: createRuntimeQualificationPatch(runtime, request),
    guardrailDecision: guardrailDecisionFromRuntime(runtime),
  };
}

function guardrailDecisionFromRuntime(runtime: RuntimeAgentRunResponse) {
  const output = runtime.output;
  const detectedIntents = new Set(output?.decision?.detected_intents ?? []);
  if (detectedIntents.has("prompt_injection")) {
    return {
      category: "prompt_injection" as const,
      action: "refuse" as const,
      reason: "agent_runtime:prompt_injection",
    };
  }
  if (detectedIntents.has("sensitive_data")) {
    return {
      category: "sensitive_data" as const,
      action: "refuse" as const,
      reason: "agent_runtime:sensitive_data",
    };
  }
  if (runtime.status === "blocked" || runtime.status === "failed") {
    return {
      category: "provider_failure" as const,
      action: "fallback" as const,
      reason: `agent_runtime:${runtime.status ?? "unknown"}`,
    };
  }
  return {
    category: "allowed" as const,
    action: runtime.status === "human_paused" ? ("handoff" as const) : ("respond" as const),
    reason: `agent_runtime:${runtime.status ?? "unknown"}`,
  };
}

function mapRuntimeMessageToAssistantMessage(
  message: NonNullable<RuntimeAgentOutput["messages"]>[number],
  runtime: RuntimeAgentRunResponse,
  request: AiAttendantRequest,
  index: number,
) {
  const text = typeof message.text === "string" ? message.text.trim().slice(0, 900) : "";
  if (!text) return null;
  const intent = intentFromRuntimeOutput(runtime);
  const action = request.session.channel === "web" && message.kind === "action" ? actionFromRuntimeText(text) : undefined;
  const id = createRuntimeAssistantMessageId(runtime, request, index);
  if (action) {
    return { ...createAssistantActionMessage(action.label, intent, action), id };
  }
  return { ...createAssistantMessage(text, intent), id };
}

function createRuntimeAssistantMessageId(
  runtime: RuntimeAgentRunResponse,
  request: AiAttendantRequest,
  index: number,
) {
  const runIdentity = runtime.run_id || runtime.trace_id || runtime.conversation_id || request.session.sessionId;
  return `assistant_runtime_${hashShort(`${runIdentity}:${index}`)}`;
}

function actionFromRuntimeText(text: string): { label: string; href: string } | undefined {
  const match = text.match(/^([^:]{2,80}):\s*(https?:\/\/\S+)$/);
  const label = match?.[1]?.trim();
  const href = match?.[2]?.trim();
  if (!label || !href) return undefined;
  return { label, href };
}

function createRuntimeQualificationPatch(runtime: RuntimeAgentRunResponse, request: AiAttendantRequest): QualificationDraft {
  const output = runtime.output ?? {};
  const productSources = output.sources?.filter((source) => source.type === "product_knowledge") ?? [];
  const sourceVersion = productSources.find((source) => source.version)?.version;
  const productSourceKeys = unique(productSources.flatMap((source) => source.keys ?? []));
  const productFollowupIntent = latestProductFollowupIntent(output.decision?.detected_intents);
  const postDiagnosticContextUsed = usesPostDiagnosticContext(output);
  const unsupportedFactRequested = summarizeUnsupportedFactRequest(output);
  const humanConfirmationOffered = didOfferHumanConfirmation(output);
  const diagnosticRefusalRespected = wasDiagnosticRefusalRespected(output);
  const inferredQualification = qualificationFromStructuredRuntime(
    output,
    inferOperationalContactFromUserText(request.userMessage, request.session.qualificationDraft),
  );
  const diagnosticStatus = output.diagnostic?.status
    ? output.diagnostic.status === "insufficient_evidence"
      ? "in_progress"
      : mapDiagnosticStatus(output.diagnostic.status)
    : undefined;
  const hasCompletedDiagnostic = diagnosticStatus === "completed";
  const completedAgentRecommendations = hasCompletedDiagnostic ? serializeAgentRecommendations(output.diagnostic?.indicated_agents) : undefined;
  const runtimePainSummary = painSummaryFromRuntimeOutput(output);
  const runtimeCurrentProcess = diagnosticAnswerValue(output, "current_process");
  const runtimePriorityGoal = diagnosticAnswerValue(output, "priority");
  const runtimeBuyingTiming = diagnosticAnswerValue(output, "urgency");
  const patch: QualificationDraft = {
    ...inferredQualification,
    primaryPainOrIntent: runtimePainSummary ?? inferredQualification.primaryPainOrIntent,
    operationalPains: runtimePainSummary ?? inferredQualification.operationalPains,
    currentSystem: runtimeCurrentProcess ?? inferredQualification.currentSystem,
    priorityGoal: runtimePriorityGoal ?? inferredQualification.priorityGoal,
    buyingTiming: runtimeBuyingTiming ?? inferredQualification.buyingTiming,
    leadSourceChannel: request.session.channel === "whatsapp" ? "whatsapp" : "widget",
    agentRuntimeRunId: runtime.run_id,
    agentRuntimeContractVersion: runtime.contract_version,
    agentRuntimeTraceId: runtime.trace_id,
    agentRuntimeCurrentAgent: runtime.current_agent,
    agentRuntimePreviousState: output.decision?.previous_state,
    agentRuntimeCurrentState: output.decision?.current_state,
    agentRuntimeNextState: output.decision?.next_state,
    agentRuntimeRoute: output.decision?.route,
    agentRuntimeDetectedIntents: output.decision?.detected_intents?.join(", "),
    agentRuntimeTemplateIds: output.decision?.template_ids?.join(", ") || output.messages?.map((message) => message.template_id).filter(Boolean).join(", "),
    agentRuntimeDiagnosticLedgerStatus: output.decision?.diagnostic_ledger_status,
    agentRuntimeDemoStatus: output.decision?.demo_status || output.diagnostic?.demo_status_at_delivery || undefined,
    agentRuntimeDemoNextStep: output.decision?.demo_next_step,
    agentRuntimeFinalPlanLine: hasCompletedDiagnostic ? output.diagnostic?.final_plan_line || undefined : undefined,
    agentRuntimeFinalDemoLine: hasCompletedDiagnostic ? output.diagnostic?.final_demo_line || output.diagnostic?.final_demo_next_step_question || undefined : undefined,
    agentRuntimeCrmBaseRecommendation: hasCompletedDiagnostic ? output.diagnostic?.crm_base_recommendation || undefined : undefined,
    agentRuntimeAgentRecommendations: completedAgentRecommendations,
    agentRuntimeGuardrailFlags: output.safety_flags?.join(", "),
    agentRuntimeWaitlistIntentEvidence:
      output.decision?.waitlist_allowed_now && output.decision?.facts_used?.length
        ? output.decision.facts_used.join(" | ")
        : undefined,
    agentRuntimeProductSourceKeys: productSourceKeys.join(", ") || undefined,
    agentRuntimeLatestProductFollowupIntent: productFollowupIntent,
    agentRuntimePostDiagnosticContextUsed: typeof postDiagnosticContextUsed === "boolean" ? String(postDiagnosticContextUsed) : undefined,
    agentRuntimeUnsupportedFactRequested: unsupportedFactRequested,
    agentRuntimeHumanConfirmationOffered: typeof humanConfirmationOffered === "boolean" ? String(humanConfirmationOffered) : undefined,
    agentRuntimeDiagnosticRefusalRespected: typeof diagnosticRefusalRespected === "boolean" ? String(diagnosticRefusalRespected) : undefined,
    agentRuntimeCostEstimateUsd: typeof output.usage?.cost_usd === "number" ? String(output.usage.cost_usd) : undefined,
    agentRuntimeProductSourceVersion: sourceVersion,
  };

  if (output.waitlist_action?.status) {
    patch.waitlistStatus = mapWaitlistStatus(output.waitlist_action.status);
    patch.missingWaitlistFields = output.waitlist_action.missing_fields?.join(", ");
    if (patch.waitlistStatus === "joined") {
      patch.waitlistJoinedAt = new Date().toISOString();
      patch.commercialStage = "waitlist_joined";
      patch.closureState = "waitlist_joined";
    }
  }

  if (output.diagnostic?.status) {
    const waitlistStatus = output.waitlist_action?.status;
    const hasWaitlistAction = Boolean(waitlistStatus && waitlistStatus !== "none");
    patch.diagnosticStatus = diagnosticStatus;
    patch.diagnosticNextStep = output.diagnostic.next_question || output.diagnostic.final_demo_next_step_question || output.diagnostic.final_demo_line || undefined;
    if (hasCompletedDiagnostic) {
      patch.diagnosticSummary = output.diagnostic.main_bottleneck || undefined;
      patch.recommendedAgents = completedAgentRecommendations || patch.recommendedAgents;
      patch.recommendedPlan = output.diagnostic.plan_or_range_to_compare || output.diagnostic.final_plan_line || patch.recommendedPlan;
      patch.diagnosticCompletedAt = new Date().toISOString();
      patch.commercialStage = "diagnostic_completed";
      if (!hasWaitlistAction) {
        patch.nextAction = "Diagnóstico entregue; acompanhar resposta sobre demonstrações, plano ou lista de espera.";
      }
    } else if (diagnosticStatus === "in_progress") {
      patch.commercialStage = "diagnostic_in_progress";
      patch.nextAction = output.diagnostic.next_question
        ? `Diagnóstico em andamento; aguardando resposta: ${output.diagnostic.next_question}`
        : "Diagnóstico em andamento; continuar pela próxima pergunta necessária.";
    } else if (diagnosticStatus === "offered") {
      patch.commercialStage = "diagnostic_offered";
      patch.nextAction = "Diagnóstico gratuito oferecido; aguardar aceite ou dúvida do lead.";
    } else {
      patch.recommendedPlan = undefined;
    }
    if (!hasCompletedDiagnostic) {
      patch.diagnosticSummary = undefined;
      patch.recommendedAgents = undefined;
      patch.recommendedPlan = undefined;
      patch.agentRuntimeFinalPlanLine = undefined;
      patch.agentRuntimeFinalDemoLine = undefined;
      patch.agentRuntimeCrmBaseRecommendation = undefined;
      patch.agentRuntimeAgentRecommendations = undefined;
    }
  }

  const demoStatus = mapRuntimeDemoStatus(output.decision?.demo_status || output.diagnostic?.demo_status_at_delivery);
  const completedDiagnosticOfferedDemo = hasCompletedDiagnostic && didCompletedDiagnosticOfferDemo(output);
  if (demoStatus) {
    patch.demoStatus = demoStatus === "not_offered" && completedDiagnosticOfferedDemo ? "offered" : demoStatus;
    if (patch.demoStatus === "offered" && !patch.demoOfferedAt) patch.demoOfferedAt = new Date().toISOString();
    if (demoStatus === "viewed_discussed" && !patch.demoSeenAt) patch.demoSeenAt = new Date().toISOString();
  }
  if (completedDiagnosticOfferedDemo && !patch.demoOfferedAt) {
    patch.demoStatus = patch.demoStatus === "viewed_discussed" || patch.demoStatus === "positive" ? patch.demoStatus : "offered";
    patch.demoOfferedAt = new Date().toISOString();
  }

  if (runtime.status === "human_paused" || output.handoff?.status === "requested" || output.handoff?.status === "active") {
    patch.humanActive = "requested";
    patch.aiPaused = "true";
    patch.commercialStage = "human_handoff";
    patch.closureState = "human_active";
    patch.nextAction = "Humano deve assumir a conversa; automacao pausada.";
  }

  return patch;
}

function inferOperationalContactFromUserText(text?: string, existing: QualificationDraft = {}): QualificationDraft {
  const clean = text?.trim();
  if (!clean) return {};
  const patch: QualificationDraft = {};
  if (!existing.whatsapp) {
    const phone = inferBrazilianPhone(clean);
    if (phone) patch.whatsapp = phone;
  }

  if (!existing.email) {
    const email = clean.match(/[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}/i)?.[0];
    if (email) patch.email = email.toLowerCase();
  }

  if (!existing.studioName) {
    const studioName = inferStudioName(clean);
    if (studioName) patch.studioName = studioName;
  }

  if (!existing.cityState) {
    const cityState = inferCityState(clean);
    if (cityState) patch.cityState = cityState;
  }

  return patch;
}

function qualificationFromStructuredRuntime(
  output: RuntimeAgentOutput,
  existing: QualificationDraft,
): QualificationDraft {
  const patch: QualificationDraft = { ...existing };
  for (const identity of output.sales_inbox_projection?.identity ?? []) {
    if (!identity.verified || !identity.key || !identity.value?.trim()) continue;
    const value = identity.value.trim();
    if (["name", "first_name", "lead_name", "person_name", "profile_name"].includes(identity.key)) {
      patch.name = patch.name ?? value;
    } else if (identity.key === "studio_name") {
      patch.studioName = patch.studioName ?? value;
    } else if (identity.key === "email") {
      patch.email = patch.email ?? value;
    } else if (["phone", "whatsapp_phone"].includes(identity.key)) {
      patch.whatsapp = patch.whatsapp ?? value;
    }
  }
  return patch;
}

function parseRuntimeAgentRunResponse(payload: unknown): RuntimeAgentRunResponse | null {
  if (!payload || typeof payload !== "object" || Array.isArray(payload)) return null;
  const runtime = payload as RuntimeAgentRunResponse;
  if (runtime.contract_version !== COMMERCIAL_OPS_CONTRACT_VERSION) return null;
  if (!runtime.run_id || !runtime.conversation_id || !runtime.agent_key || !runtime.trace_id) return null;
  if (!runtime.output || typeof runtime.output !== "object") return null;
  return runtime;
}

function inferBrazilianPhone(clean: string) {
  const phoneMatch = clean.match(/(?:\+?55\s*)?(?:\(?\d{2}\)?\s*)?\d{4,5}[-\s]?\d{4}/);
  return phoneMatch?.[0]?.replace(/[^\d+]/g, "");
}

function inferStudioName(clean: string) {
  const match =
    clean.match(/\b(?:meu\s+)?studio\s+(?:e|é|eh|se chama|chama)\s+([^,.]+?)(?=\s+(?:em|fica|de)\s+|[,.]|$)/i) ??
    clean.match(/\b(?:studio|estudio)\s+([^,.]+?)(?=\s+(?:em|fica|de)\s+|[,.]|$)/i);
  return cleanStudioNameCandidate(match?.[1]);
}

function cleanStudioNameCandidate(candidate?: string) {
  const clean = candidate?.trim().replace(/\s+/g, " ").slice(0, 80);
  if (!clean) return undefined;
  const normalized = normalizeRuntimeText(clean);
  if (/^(de\s+)?pilates$/.test(normalized)) return undefined;
  if (/^(de|do|da|dos|das|para|pra|no|na|em)\b/.test(normalized)) return undefined;
  if (/\b(rotina|agenda|reposicao|reposicoes|cobranca|gestao|atendimento|acompanhamento|whatsapp|alunos?)\b/.test(normalized)) {
    return undefined;
  }
  return clean;
}

function inferCityState(clean: string) {
  const commaParts = clean.split(",").map((part) => part.trim()).filter(Boolean);
  if (commaParts.length >= 2 && /\bstudio|estudio\b/i.test(commaParts[0])) {
    const locationFromComma = cleanCityStateCandidate(commaParts.slice(1).join(", "));
    if (locationFromComma) return locationFromComma;
  }

  const candidates = [
    clean.match(/,\s*em\s+([A-Za-zÀ-ÖØ-öø-ÿ' -]{3,80})(?=[,.]|$)/i)?.[1],
    clean.match(/\b(?:fica em|sou de)\s+([A-Za-zÀ-ÖØ-öø-ÿ' -]{3,80})(?=[,.]|$)/i)?.[1],
    clean.match(/\bcidade\s*:?\s*([A-Za-zÀ-ÖØ-öø-ÿ' -]{3,80})(?=[,.]|$)/i)?.[1],
  ];
  return candidates
    .map(cleanCityStateCandidate)
    .find((candidate) => Boolean(candidate));
}

function cleanCityStateCandidate(candidate?: string) {
  const clean = candidate?.trim().replace(/\s+/g, " ").slice(0, 80);
  if (!clean) return undefined;
  const normalized = normalizeRuntimeText(clean);
  if (/^(espera|lista de espera)$/i.test(clean)) return undefined;
  if (/\b(planilha|caderno|sistema|whatsapp|agenda|reposicao|reposicoes|rotina|controle|manual)\b/.test(normalized)) {
    return undefined;
  }
  return clean;
}

function normalizeRuntimeText(value: string) {
  return value
    .toLowerCase()
    .normalize("NFD")
    .replace(/\p{Diacritic}/gu, "");
}

function createOperationalFallbackResponse(reason: string, request: AiAttendantRequest): AiAttendantResponse {
  const channel = request.session.channel;
  const content =
    channel === "whatsapp"
      ? "Estou com uma instabilidade aqui. Vou deixar sua mensagem registrada para a equipe da Taliya continuar com segurança."
      : "Estou com uma instabilidade no atendimento agora. Sua mensagem ficou registrada para a equipe da Taliya continuar com segurança.";
  return {
    assistantMessages: [createAssistantMessage(content, "fallback")],
    capturedPainIds: [],
    recommendedAgentIds: [],
    shouldOfferDiagnostic: false,
    qualificationPatch: {
      leadSourceChannel: channel === "whatsapp" ? "whatsapp" : "widget",
      closureState: "error_needs_attention",
      nextAction: `Runtime indisponivel: ${reason}. Operador deve revisar.`,
    },
    guardrailDecision: {
      category: "provider_failure",
      action: "fallback",
      reason,
    },
  };
}

function createRuntimeRequestId(request: AiAttendantRequest) {
  const externalId = request.session.externalContact?.providerMessageId;
  if (externalId) return `${mapRuntimeChannel(request.session.channel)}:${externalId}`;
  const content = request.userMessage || request.quickReplyId || "empty";
  return `${mapRuntimeChannel(request.session.channel)}:${request.session.sessionId}:${request.session.messages.length}:${hashShort(content)}`;
}

function hashShort(value: string) {
  return createHmac("sha256", "taliya-runtime-request-id").update(value).digest("hex").slice(0, 16);
}

function mapRuntimeChannel(channel: AiAttendantRequest["session"]["channel"]): RuntimeChannel {
  return channel === "whatsapp" ? "whatsapp" : "widget";
}

function unique(values: string[]) {
  return Array.from(new Set(values.filter(Boolean)));
}

function intentFromRuntimeOutput(runtime: RuntimeAgentRunResponse): AiAttendantIntent {
  const output = runtime.output;
  if (runtime.status === "human_paused" || output?.handoff?.status === "requested" || output?.handoff?.status === "active") return "human_whatsapp_handoff";
  if (output?.waitlist_action?.status && output.waitlist_action.status !== "none") return "waitlist_intent";
  if (output?.diagnostic?.status === "completed") return "crm_agent_diagnostic";
  if (runtime.current_agent?.includes("pricing")) return "view_plans";
  return "answer_question";
}

function conversionPathFromRuntime(runtime: RuntimeAgentRunResponse): ConversionPath | undefined {
  const output = runtime.output;
  if (runtime.status === "human_paused" || output?.handoff?.status === "requested" || output?.handoff?.status === "active") return "human_whatsapp_assist";
  if (output?.waitlist_action?.status === "offered" || output?.waitlist_action?.status === "pending_details" || output?.waitlist_action?.status === "joined") return "waitlist_intent";
  if (output?.diagnostic?.status === "completed") return "crm_agent_diagnostic";
  return undefined;
}

function mapWaitlistStatus(status: string): QualificationDraft["waitlistStatus"] {
  if (status === "offered") return "offered";
  if (status === "pending_details") return "pending_details";
  if (status === "joined") return "joined";
  if (status === "declined") return "declined";
  return "not_offered";
}

function mapDiagnosticStatus(status: string): QualificationDraft["diagnosticStatus"] {
  if (status === "offered") return "offered";
  if (status === "in_progress") return "in_progress";
  if (status === "completed") return "completed";
  return "not_started";
}

function mapRuntimeDemoStatus(status?: string | null): QualificationDraft["demoStatus"] | undefined {
  if (status === "offered") return "offered";
  if (status === "viewed_or_asked") return "viewed_discussed";
  if (status === "reacted_positive") return "positive";
  if (status === "not_offered") return "not_offered";
  return undefined;
}

function didCompletedDiagnosticOfferDemo(output: RuntimeAgentOutput) {
  const templateIds = output.decision?.template_ids ?? [];
  return Boolean(
    output.diagnostic?.final_demo_line ||
      output.diagnostic?.final_demo_next_step_question ||
      templateIds.includes("diagnostic.deliver_demo_not_offered") ||
      templateIds.includes("diagnostic.deliver_demo_already_offered"),
  );
}

function serializeAgentRecommendations(agents?: Array<Record<string, unknown>> | null): string | undefined {
  if (!agents?.length) return undefined;
  return agents
    .map((agent) => {
      const name = typeof agent.name === "string" ? agent.name : undefined;
      const agentName = typeof agent.agent_name === "string" ? agent.agent_name : undefined;
      const displayName = name ?? agentName;
      const pain = typeof agent.agent_pain_resolved === "string" ? agent.agent_pain_resolved : undefined;
      const action = typeof agent.agent_practical_action === "string" ? agent.agent_practical_action : undefined;
      return [displayName, pain, action].filter(Boolean).join(": ");
    })
    .filter(Boolean)
    .join(" | ");
}

const PRODUCT_FOLLOWUP_INTENTS = new Set([
  "product_how_it_works",
  "comparison_current_tool",
  "integration_scope_question",
  "trust_security_question",
  "lgpd_question",
  "data_sharing_question",
  "out_of_profile",
  "conversation_resume",
  "general_objection",
  "diagnostic_refusal",
]);

function latestProductFollowupIntent(intents?: string[]) {
  return intents?.find((intent) => PRODUCT_FOLLOWUP_INTENTS.has(intent));
}

function usesPostDiagnosticContext(output: RuntimeAgentOutput) {
  const stateBlob = [output.decision?.previous_state, output.decision?.current_state, output.decision?.next_state]
    .filter(Boolean)
    .join(" ");
  if (!stateBlob) return undefined;
  if (output.diagnostic?.status === "completed") return false;
  return /\b(diagnostic_completed|recommendation_validation)\b/.test(stateBlob);
}

function summarizeUnsupportedFactRequest(output: RuntimeAgentOutput) {
  const factsMissing = output.decision?.facts_missing?.filter(Boolean) ?? [];
  if (factsMissing.length) return factsMissing.join(" | ").slice(0, 600);
  return undefined;
}

function didOfferHumanConfirmation(output: RuntimeAgentOutput) {
  const text = (output.messages ?? []).map((message) => message.text ?? "").join(" ");
  if (!text.trim()) return undefined;
  return /\b(confirmar|validar|alguem|algu[eé]m|equipe|humano)\b/i.test(text);
}

function wasDiagnosticRefusalRespected(output: RuntimeAgentOutput) {
  const intents = new Set(output.decision?.detected_intents ?? []);
  if (!intents.has("diagnostic_refusal")) return undefined;
  const templateIds = output.decision?.template_ids ?? [];
  const diagnosticAction = output.decision?.diagnostic_action;
  const respectedAction = !diagnosticAction || diagnosticAction === "none" || diagnosticAction === "insufficient_evidence";
  const noDiagnosticTemplate = !templateIds.some((templateId) => templateId.startsWith("diagnostic."));
  return respectedAction && noDiagnosticTemplate;
}

function painIdsFromRuntimeOutput(output: RuntimeAgentOutput): string[] {
  const ids = new Set<string>();
  for (const area of output.diagnostic?.ledger?.flatMap((item) => item.areas ?? []) ?? []) {
    const mapped = painIdFromRuntimeArea(area);
    if (mapped) ids.add(mapped);
  }
  if (ids.size) return Array.from(ids);
  for (const fact of output.lead_facts ?? []) {
    if (fact.key === "main_pain" || fact.key === "pain" || fact.key === "studio_pains") {
      for (const mapped of painIdsFromText(fact.value ?? "")) ids.add(mapped);
    }
  }
  for (const value of output.diagnostic?.facts_used ?? []) {
    for (const mapped of painIdsFromText(value)) ids.add(mapped);
  }
  return Array.from(ids);
}

function painSummaryFromRuntimeOutput(output: RuntimeAgentOutput) {
  return (
    diagnosticAnswerValue(output, "main_pain") ??
    output.lead_facts?.find((fact) => fact.key === "studio_pains" || fact.key === "main_pain" || fact.key === "pain")?.value ??
    undefined
  );
}

function diagnosticAnswerValue(output: RuntimeAgentOutput, questionKey: string) {
  const item = output.diagnostic?.ledger?.find(
    (entry) =>
      entry.question_key === questionKey &&
      typeof entry.answer_value === "string" &&
      entry.answer_value.trim() &&
      (entry.status === "answered" || entry.status === "inferred_from_prior_message"),
  );
  return item?.answer_value?.trim();
}

function painIdFromRuntimeArea(area: string) {
  const normalized = normalizeRuntimeText(area);
  if (normalized === "atendimento") return "atendimento";
  if (normalized === "vendas") return "vendas";
  if (normalized === "financeiro" || normalized === "cobrancas") return "financeiro";
  if (normalized === "agenda_reposicoes" || normalized === "reposicoes" || normalized === "reposicao") return "agenda_reposicoes";
  if (normalized === "acompanhamento") return "acompanhamento";
  if (normalized === "gestao") return "gestao";
  return undefined;
}

function painIdsFromText(value: string) {
  const normalized = normalizeRuntimeText(value);
  const ids = new Set<string>();
  if (/\b(whatsapp|atendimento|mensagem|responder|retorno)\b/.test(normalized)) ids.add("atendimento");
  if (/\b(venda|vendas|interessado|interessados|lead|leads|follow)\b/.test(normalized)) ids.add("vendas");
  if (/\b(financeiro|pagamento|pagamentos|mensalidade|cobranca|cobrancas)\b/.test(normalized)) ids.add("financeiro");
  if (/\b(agenda|reposicao|reposicoes|falta|faltas|encaixe|encaixes)\b/.test(normalized)) ids.add("agenda_reposicoes");
  if (/\b(acompanhamento|aluno|alunos|retencao|inativo|inativos)\b/.test(normalized)) ids.add("acompanhamento");
  if (/\b(gestao|visao|pendente|pendentes|rotina|controle)\b/.test(normalized)) ids.add("gestao");
  return Array.from(ids);
}

function agentIdsFromDiagnostic(diagnostic: RuntimeAgentOutput["diagnostic"]): string[] {
  if (diagnostic?.status !== "completed") return [];
  const joined = [...(diagnostic?.facts_used ?? []), diagnostic?.main_bottleneck ?? ""].join(" ").toLowerCase();
  const ids = new Set<string>();
  if (joined.includes("agenda") || joined.includes("reposi")) ids.add("agenda");
  if (joined.includes("venda") || joined.includes("interess")) ids.add("vendas");
  if (joined.includes("finance") || joined.includes("mensal")) ids.add("financeiro");
  if (joined.includes("retenc") || joined.includes("inativo")) ids.add("retencao");
  if (joined.includes("atendimento") || joined.includes("whatsapp")) ids.add("atendimento");
  return Array.from(ids);
}

function isRecord(input: unknown): input is Record<string, unknown> {
  return typeof input === "object" && input !== null;
}

function getRuntimeErrorCode(payload: unknown, fallback: string): string {
  if (!isRecord(payload) || !isRecord(payload.error)) return fallback;
  return typeof payload.error.code === "string" ? payload.error.code : fallback;
}

export function createRuntimeMockResponse(overrides: Partial<RuntimeAgentRunResponse> = {}): RuntimeAgentRunResponse {
  return {
    run_id: `run_${randomUUID()}`,
    conversation_id: "conv_mock",
    agent_key: "taliya_commercial",
    current_agent: "taliya_commercial_triage_agent",
    status: "succeeded",
    trace_id: `trace_${randomUUID()}`,
    output: {
      messages: [{ text: "Oi. Posso te ajudar com a Taliya.", channel_hint: "widget", kind: "text" }],
      usage: { model: "gpt-5.2", input_tokens: 1, output_tokens: 1, cost_usd: 0.0001 },
    },
    ...overrides,
  };
}
