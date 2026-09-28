import { after } from "next/server";
import { runTaliyaCommercialRuntimeTurn as runAiAttendantTurn } from "@/lib/landing/ai-attendant/runtime-client";
import { buildAiAttendantContext } from "@/lib/landing/ai-attendant/context";
import { createConversionHandoff } from "@/lib/landing/ai-attendant/conversion";
import { createLeadRecord } from "@/lib/landing/ai-attendant/leads";
import { dispatchN8nEvent } from "@/lib/landing/ai-attendant/n8n";
import { parseAiAttendantRequest } from "@/lib/landing/ai-attendant/schema";
import { recordFunnelEvent } from "@/lib/landing/ai-attendant/funnel-events";
import { appendSalesLeadMessages, findSalesLeadForSession, getSalesLead, updateSalesLeadSyncStatus, upsertSalesLead } from "@/lib/landing/ai-attendant/sales-inbox-store";
import { summarizeConversation } from "@/lib/landing/ai-attendant/summarize";

export async function POST(request: Request) {
  let body: unknown;

  try {
    body = await request.json();
  } catch {
    return Response.json({ error: "Invalid JSON body." }, { status: 400 });
  }

  const parsed = parseAiAttendantRequest(body);
  if (!parsed.ok) {
    return Response.json({ error: parsed.error }, { status: 400 });
  }

  const response = await runAiAttendantTurn(parsed.value);
  const context = buildAiAttendantContext(parsed.value);
  const userMessageCount = parsed.value.session.messages.filter((message) => message.role === "user").length;
  if (userMessageCount === 1) {
    afterResponse("record_widget_first_message", () => recordFunnelEvent({
      eventName: "first_message",
      request: parsed.value,
      response,
      leadId: parsed.value.session.leadId,
    }));
  }
  afterResponse("record_widget_funnel_event", () => recordFunnelEvent({
    eventName: funnelEventName(response),
    request: parsed.value,
    response,
  }));

  if (response.conversionPath) {
    const conversionEventName =
      response.conversionPath === "human_whatsapp_assist"
        ? "floating_agent_human_whatsapp_handoff"
        : response.conversionPath === "waitlist_intent"
          ? "floating_agent_waitlist_intent"
          : response.conversionPath === "analysis_request"
            ? "floating_agent_analysis_handoff"
            : response.conversionPath === "crm_agent_diagnostic"
              ? "floating_agent_crm_diagnostic_completed"
            : response.conversionPath === "view_plans"
            ? "floating_agent_view_plans_cta"
            : response.conversionPath === "guided_demo"
              ? "floating_agent_guided_demo_cta"
              : response.conversionPath === "plan_recommendation"
                ? "floating_agent_plan_recommendation_cta"
                : "floating_agent_checkout_cta";
    const handoff = createConversionHandoff({
      config: context.nicheConfig,
      conversionPath: response.conversionPath,
      request: parsed.value,
      selectedPlanId: response.subscription?.planId,
      summary: summarizeConversation(parsed.value),
    });
    handoff.qualification = {
      ...handoff.qualification,
      ...response.qualificationPatch,
    };
    handoff.selectedPainIds = Array.from(new Set([...handoff.selectedPainIds, ...response.capturedPainIds]));
    handoff.recommendedAgentIds = Array.from(new Set([...handoff.recommendedAgentIds, ...response.recommendedAgentIds]));
    response.handoff = handoff;
    const lead = createLeadRecord({
      config: context.nicheConfig,
      eventName: conversionEventName,
      handoff,
      request: parsed.value,
      response,
    });
    const existingSessionLead = await findSalesLeadForSession(parsed.value.session.sessionId);
    const leadToStore = promoteExistingSessionLead(lead, existingSessionLead);
    const salesLead = await upsertSalesLead(leadToStore);
    afterResponse("record_widget_lead_created", () => recordFunnelEvent({
      eventName: "lead_created",
      request: parsed.value,
      response,
      leadId: salesLead.leadId,
    }));
    afterResponse("record_widget_conversion_event", () => recordFunnelEvent({
      eventName: conversionEventName,
      request: parsed.value,
      response,
      leadId: salesLead.leadId,
    }));
    await appendSalesLeadTurn(salesLead.leadId, parsed.value, response);

    afterResponse("dispatch_widget_conversion_event", () => dispatchN8nEvent(response.conversionPath === "analysis_request" ? "landing_ai_attendant_analysis_handoff" : "landing_ai_attendant_high_intent", {
      eventName: conversionEventName,
      occurredAt: new Date().toISOString(),
      lead: leadToStore,
      salesLeadId: salesLead.leadId,
      ...handoff,
    }));
    afterResponse("update_widget_conversion_sync_status", () => updateSalesLeadSyncStatus(salesLead.leadId, "skipped", {
      eventName: "lead_stored_locally",
      reason: "Lead stored in Sales Inbox/Postgres. External CRM lead sync is disabled.",
    }));
    if (shouldNotifyOperator(leadToStore.priority, leadToStore.conversionPath)) {
      afterResponse("dispatch_widget_operator_alert", () => dispatchN8nEvent("landing_ai_attendant_lead_alert", {
        eventName: "sales_lead_urgent_alert",
        occurredAt: new Date().toISOString(),
        lead: {
          leadId: leadToStore.leadId,
          priority: leadToStore.priority,
          readiness: leadToStore.readiness,
          channel: leadToStore.channel,
          conversionPath: leadToStore.conversionPath,
          selectedPlanId: leadToStore.selectedPlanId,
          nextAction: leadToStore.nextAction,
          summary: leadToStore.summary,
        },
      }));
    }
  }

  if (!response.conversionPath && shouldPersistColdLead(parsed.value, response)) {
    const handoff = createConversionHandoff({
      config: context.nicheConfig,
      conversionPath: "cold_lead",
      request: parsed.value,
      summary: summarizeColdLead(parsed.value, response),
    });
    handoff.qualification = {
      ...handoff.qualification,
      ...response.qualificationPatch,
    };
    handoff.selectedPainIds = Array.from(new Set([...handoff.selectedPainIds, ...response.capturedPainIds]));
    handoff.recommendedAgentIds = Array.from(new Set([...handoff.recommendedAgentIds, ...response.recommendedAgentIds]));

    const lead = createLeadRecord({
      config: context.nicheConfig,
      eventName: "floating_agent_cold_lead",
      handoff,
      request: parsed.value,
      response,
    });
    const existingLead = (await getSalesLead(lead.leadId)) ?? (await findSalesLeadForSession(parsed.value.session.sessionId));
    if (existingLead && existingLead.conversionPath !== "cold_lead") {
      await appendSalesLeadTurn(existingLead.leadId, parsed.value, response);
    } else {
      const salesLead = await upsertSalesLead(promoteExistingSessionLead(lead, existingLead));
      afterResponse("record_widget_lead_created", () => recordFunnelEvent({
        eventName: "lead_created",
        request: parsed.value,
        response,
        leadId: salesLead.leadId,
      }));
      afterResponse("record_widget_cold_lead_event", () => recordFunnelEvent({
        eventName: "floating_agent_cold_lead_recorded",
        request: parsed.value,
        response,
        leadId: salesLead.leadId,
      }));
      await appendSalesLeadTurn(salesLead.leadId, parsed.value, response);
      afterResponse("update_widget_cold_lead_sync_status", () => updateSalesLeadSyncStatus(salesLead.leadId, "skipped", {
        eventName: "cold_lead_recorded",
        reason: "Cold lead stored in Sales Inbox without external lead sync.",
      }));
    }
  }

  if (response.guardrailDecision.category !== "allowed") {
    afterResponse("dispatch_widget_safety_event", () => dispatchN8nEvent("landing_ai_attendant_safety_event", {
      eventName: "floating_agent_fallback",
      occurredAt: new Date().toISOString(),
      niche: context.nicheConfig.niche,
      sourcePage: parsed.value.session.sourcePage,
      campaignStage: context.nicheConfig.tracking.campaignStage,
      publicOfferMode: context.nicheConfig.tracking.publicOfferMode,
      sessionId: parsed.value.session.sessionId,
      channel: parsed.value.session.channel,
      guardrailDecision: response.guardrailDecision,
      safeSummary: "Guardrail or fallback response emitted.",
    }));
  }

  return Response.json(response);
}

function promoteExistingSessionLead<T extends { leadId: string }>(
  lead: T,
  existingLead: { leadId: string; conversionPath: string } | null,
) {
  if (!existingLead) return lead;
  return {
    ...lead,
    leadId: existingLead.leadId,
  };
}

function afterResponse(label: string, task: () => Promise<unknown>) {
  after(async () => {
    try {
      await task();
    } catch (error) {
      console.error(`[ai-attendant-after:${label}]`, error);
    }
  });
}

function shouldPersistColdLead(request: Parameters<typeof summarizeConversation>[0], response: Awaited<ReturnType<typeof runAiAttendantTurn>>) {
  void response;
  return Boolean(request.userMessage?.trim());
}

function summarizeColdLead(request: Parameters<typeof summarizeConversation>[0], response: Awaited<ReturnType<typeof runAiAttendantTurn>>) {
  const current = request.userMessage?.trim();
  const base = summarizeConversation(request);
  const next = response.nextQuestion ? ` Próxima pergunta: ${response.nextQuestion}` : "";
  return `${base}${current ? ` Mensagem atual: ${current.slice(0, 240)}.` : ""}${next}`.slice(0, 900);
}

async function appendSalesLeadTurn(leadId: string, request: Parameters<typeof summarizeConversation>[0], response: Awaited<ReturnType<typeof runAiAttendantTurn>>) {
  const turnIndex = request.session.messages.length;
  const runtimeRunId = response.qualificationPatch?.agentRuntimeRunId;
  const runtimeTraceId = response.qualificationPatch?.agentRuntimeTraceId;
  const conversationId = request.session.channelSessionId || request.session.sessionId;
  const safetyFlags = response.qualificationPatch?.agentRuntimeGuardrailFlags
    ?.split(",")
    .map((flag) => flag.trim())
    .filter(Boolean) ?? [];
  const messages: Array<Parameters<typeof appendSalesLeadMessages>[1][number]> = request.session.messages.slice(-36).map((message) => ({
    id: salesInboxMessageId(leadId, request.session.sessionId, message.id),
    role: message.role,
    content: message.content,
    conversationId,
    channelSessionId: request.session.channelSessionId,
    channel: request.session.channel,
  }));
  const currentUserAlreadyInSession = request.session.messages
    .slice(-36)
    .some((message) => message.role === "user" && message.content.trim() === request.userMessage?.trim());

  if (request.userMessage?.trim() && !currentUserAlreadyInSession) {
    messages.push({
      id: salesInboxMessageId(leadId, request.session.sessionId, `web_${turnIndex}_user`),
      role: "user",
      content: request.userMessage,
      conversationId,
      channelSessionId: request.session.channelSessionId,
      providerMessageId: request.session.externalContact?.providerMessageId,
      channel: request.session.channel,
      direction: "inbound",
      runId: runtimeRunId,
      traceId: runtimeTraceId,
      safetyFlags,
      isSensitive: response.guardrailDecision.category === "sensitive_data",
      unsupportedMedia: false,
      isProblematic: response.guardrailDecision.category !== "allowed",
    });
  }

  messages.push(
    ...response.assistantMessages.map((message) => ({
      id: salesInboxMessageId(leadId, request.session.sessionId, message.id),
      role: "assistant" as const,
      content: message.content,
      conversationId,
      channelSessionId: request.session.channelSessionId,
      channel: request.session.channel,
      direction: "outbound" as const,
      deliveryStatus: "delivered",
      runId: runtimeRunId,
      traceId: runtimeTraceId,
      safetyFlags,
      isProblematic: response.guardrailDecision.category !== "allowed",
    })),
  );

  await appendSalesLeadMessages(leadId, messages);
}

function salesInboxMessageId(leadId: string, sessionId: string, messageId: string) {
  const scopedId = `${leadId}:${sessionId}:${messageId}`;
  return scopedId.length <= 240 ? scopedId : `${leadId}:${hashMessageId(scopedId)}`;
}

function hashMessageId(input: string) {
  let hash = 2166136261;
  for (let index = 0; index < input.length; index += 1) {
    hash ^= input.charCodeAt(index);
    hash = Math.imul(hash, 16777619);
  }
  return (hash >>> 0).toString(36);
}

function shouldNotifyOperator(priority: string, conversionPath?: string) {
  return (
    priority === "hot" ||
    conversionPath === "checkout_intent" ||
    conversionPath === "subscription_intent" ||
    conversionPath === "human_whatsapp_assist" ||
    conversionPath === "waitlist_intent" ||
    conversionPath === "crm_agent_diagnostic" ||
    conversionPath === "custom_agent_follow_up"
  );
}

function funnelEventName(response: Awaited<ReturnType<typeof runAiAttendantTurn>>) {
  if (response.guardrailDecision.category === "rate_limited") return "rate_limit";
  if (response.guardrailDecision.category !== "allowed") return "guardrail";
  if (response.qualificationPatch?.waitlistStatus === "joined") return "waitlist_joined";
  if (response.qualificationPatch?.waitlistStatus === "offered") return "waitlist_offered";
  if (response.qualificationPatch?.diagnosticStatus === "offered") return "diagnostic_offered";
  if (response.qualificationPatch?.diagnosticStatus === "completed" || response.conversionPath === "crm_agent_diagnostic") return "diagnostic_completed";
  if (response.conversionPath === "view_plans") return "plans_viewed";
  if (response.conversionPath === "guided_demo") return "demo_requested";
  return "assistant_turn";
}
