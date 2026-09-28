import { after } from "next/server";
import { randomUUID } from "crypto";
import { pilatesLanding } from "@/data/landing/niches/pilates";
import { buildAiAttendantContext } from "@/lib/landing/ai-attendant/context";
import { createConversionHandoff } from "@/lib/landing/ai-attendant/conversion";
import { normalizeWhatsAppTurnToRequest } from "@/lib/landing/ai-attendant/channels";
import type { WhatsAppInboundTurn } from "@/lib/landing/ai-attendant/channels";
import { isOptOutText } from "@/lib/landing/ai-attendant/guardrails";
import { completeAgentV2IdempotencyKey, reserveAgentV2IdempotencyKey } from "@/lib/landing/ai-attendant/agent-v2-idempotency";
import { createLeadRecord } from "@/lib/landing/ai-attendant/leads";
import { dispatchN8nEvent, salesInboxSyncStatusFromN8nResult } from "@/lib/landing/ai-attendant/n8n";
import { recordFunnelEvent } from "@/lib/landing/ai-attendant/funnel-events";
import {
  appendWhatsAppMessages,
  getOrCreateWhatsAppSession,
  markProviderMessageProcessed,
  markWhatsAppOptOut,
  recordProviderStatus,
  registerProviderMessage,
  updateWhatsAppSessionState,
} from "@/lib/landing/ai-attendant/session-store";
import { logAiUsageEvent } from "@/lib/landing/ai-attendant/usage";
import { appendSalesLeadMessage, appendSalesLeadMessages, applyOperatorAction, findSalesLeadForWhatsApp, updateSalesLeadSyncStatus, upsertSalesLead } from "@/lib/landing/ai-attendant/sales-inbox-store";
import { hasPostgresStorage, postgresQuery } from "@/lib/landing/ai-attendant/storage/postgres";
import { summarizeConversation } from "@/lib/landing/ai-attendant/summarize";
import {
  isWithinWhatsAppCustomerServiceWindow,
  parseMetaWhatsAppBusinessAppEchoes,
  parseMetaWhatsAppUnsupportedInbound,
  parseMetaWhatsAppInbound,
  parseMetaWhatsAppStatuses,
  recordWhatsAppOutboxProviderStatus,
  responseToWhatsAppTexts,
  sendMetaWhatsAppReply,
  sendMetaWhatsAppReplySequence,
  sendMetaWhatsAppTypingIndicator,
  startMetaWhatsAppTypingKeepAlive,
  verifyDualhookSharedSecret,
  verifyDualhookSignature,
  verifyExpectedWhatsAppPhoneNumber,
  verifyMetaSignature,
  verifyMetaWebhookChallenge,
} from "@/lib/landing/ai-attendant/whatsapp";
import { runTaliyaCommercialRuntimeTurn as runAiAttendantTurn } from "@/lib/landing/ai-attendant/runtime-client";
import type { QualificationDraft } from "@/lib/landing/ai-attendant/schema";

export const maxDuration = 60;

type QueuedWhatsAppTurn = WhatsAppInboundTurn & {
  queueId: string;
  batchId?: string;
};

export async function GET(request: Request) {
  const challenge = verifyMetaWebhookChallenge(request.url);
  if (!challenge) return new Response("Forbidden", { status: 403 });
  return new Response(challenge, { status: 200 });
}

export async function POST(request: Request) {
  const rawBody = await request.text();
  const workerResponse = handleInternalWhatsAppWorkerRequest(request, rawBody);
  if (workerResponse) return workerResponse;

  const signature = verifyWebhookSignature(rawBody, request);

  if (!signature.ok) {
    return Response.json({ error: signature.reason }, { status: 401 });
  }

  const turns = parseMetaWhatsAppInbound(rawBody);
  const unsupportedTurns = parseMetaWhatsAppUnsupportedInbound(rawBody);
  const businessAppEchoes = parseMetaWhatsAppBusinessAppEchoes(rawBody);
  const statuses = parseMetaWhatsAppStatuses(rawBody);
  if (!turns.length && !unsupportedTurns.length && !businessAppEchoes.length && !statuses.length) {
    return Response.json({ status: "ignored", reason: "No supported inbound text message." });
  }

  const results = [];

  for (const status of statuses) {
    await recordProviderStatus({
      providerMessageId: status.providerMessageId,
      providerStatus: status.providerStatus,
      errorCode: status.errorCode,
    });
    await recordWhatsAppOutboxProviderStatus({
      providerMessageId: status.providerMessageId,
      providerStatus: status.providerStatus,
      errorCode: status.errorCode,
    });
    results.push({
      providerMessageId: status.providerMessageId,
      status: "provider_status_recorded",
      providerStatus: status.providerStatus,
      phoneNumberId: status.phoneNumberId,
      errorCode: status.errorCode,
    });
  }

  for (const echo of businessAppEchoes) {
    const registered = await registerProviderMessage({
      providerContactId: echo.providerContactId,
      providerMessageId: echo.providerMessageId,
      phone: echo.toPhone,
      phoneNumberId: echo.phoneNumberId,
      displayPhoneNumber: echo.displayPhoneNumber,
    });

    if (!registered.ok) {
      results.push({ providerMessageId: echo.providerMessageId, status: "failed", reason: registered.reason });
      continue;
    }

    if (registered.duplicate) {
      results.push({ providerMessageId: echo.providerMessageId, status: "duplicate_ignored" });
      continue;
    }

    const content = echo.text ?? `[business_app_message:${echo.messageType}]`;
    await appendWhatsAppMessages(echo.providerContactId, [{ id: echo.providerMessageId, role: "assistant", content }]);
    await updateWhatsAppSessionState(echo.providerContactId, { status: "humanActive" });

    const salesLead = await findSalesLeadForWhatsApp({
      providerContactId: echo.providerContactId,
      phone: echo.toPhone,
    });

    if (salesLead) {
      await appendSalesLeadMessage(salesLead.leadId, {
        id: echo.providerMessageId,
        role: "assistant",
        content,
        createdAt: echo.occurredAt,
      });

      if (!salesLead.aiPaused && salesLead.status !== "human_active" && salesLead.status !== "do_not_contact") {
        await applyOperatorAction({
          action: "take_over",
          actorUserId: "system:whatsapp_business_app_echo",
          leadId: salesLead.leadId,
          payload: {
            providerContactId: echo.providerContactId,
            phoneNumberId: echo.phoneNumberId,
            reason: "business_app_manual_reply",
          },
        });
      }
    }

    await logAiUsageEvent({
      sessionId: registered.session.channelSessionId,
      channel: "whatsapp",
      niche: pilatesLanding.niche,
      provider: "meta_whatsapp_cloud_api",
      status: "skipped",
      idempotencyKey: echo.providerMessageId,
    });
    await markProviderMessageProcessed(echo.providerMessageId, "processed");

    results.push({
      providerMessageId: echo.providerMessageId,
      status: "business_app_echo_recorded_ai_paused",
      leadId: salesLead?.leadId,
      phoneNumberId: echo.phoneNumberId,
      messageType: echo.messageType,
    });
  }

  for (const turn of unsupportedTurns) {
    const registered = await registerProviderMessage({
      providerContactId: turn.providerContactId,
      providerMessageId: turn.providerMessageId,
      phone: turn.fromPhone,
      phoneNumberId: turn.phoneNumberId,
      displayPhoneNumber: turn.displayPhoneNumber,
    });

    if (!registered.ok) {
      results.push({ providerMessageId: turn.providerMessageId, status: "failed", reason: registered.reason });
      continue;
    }

    if (registered.duplicate) {
      results.push({ providerMessageId: turn.providerMessageId, status: "duplicate_ignored" });
      continue;
    }

    const safeUserMessage = `[unsupported_whatsapp_message:${turn.messageType}]`;
    await appendWhatsAppMessages(turn.providerContactId, [{ id: turn.providerMessageId, role: "user", content: safeUserMessage }]);

    if (registered.session.status === "optedOut") {
      await markProviderMessageProcessed(turn.providerMessageId, "processed");
      results.push({ providerMessageId: turn.providerMessageId, status: "opted_out", messageType: turn.messageType });
      continue;
    }

    const salesLead = await findSalesLeadForWhatsApp({
      providerContactId: turn.providerContactId,
      phone: turn.fromPhone,
    });

    if (registered.session.status === "humanActive" || salesLead?.aiPaused || salesLead?.status === "human_active" || salesLead?.status === "do_not_contact") {
      await markProviderMessageProcessed(turn.providerMessageId, "processed");
      results.push({
        providerMessageId: turn.providerMessageId,
        status: salesLead?.status === "do_not_contact" ? "do_not_contact" : "ai_paused_human_active",
        leadId: salesLead?.leadId,
        messageType: turn.messageType,
      });
      continue;
    }

    if (!isWithinWhatsAppCustomerServiceWindow(turn.occurredAt)) {
      await markProviderMessageProcessed(turn.providerMessageId, "processed");
      results.push({ providerMessageId: turn.providerMessageId, status: "outside_customer_service_window", messageType: turn.messageType });
      continue;
    }

    const content = unsupportedWhatsAppMessageReply(turn.messageType);
    const sendResult = await sendMetaWhatsAppReply({
      content,
      replyToProviderMessageId: turn.providerMessageId,
      to: turn.fromPhone ?? turn.providerContactId,
      phoneNumberId: turn.phoneNumberId,
      idempotencyKey: `unsupported_reply:${turn.providerMessageId}`,
      channelSessionId: registered.session.channelSessionId,
      providerContactId: turn.providerContactId,
    });

    await appendWhatsAppMessages(turn.providerContactId, [
      {
        id: sendResult.ok && sendResult.providerMessageId ? sendResult.providerMessageId : `unsupported_reply_${turn.providerMessageId}`,
        role: "assistant",
        content,
      },
    ]);

    await logAiUsageEvent({
      sessionId: `wa_${turn.providerContactId}`,
      channel: "whatsapp",
      niche: pilatesLanding.niche,
      provider: "meta_whatsapp_cloud_api",
      status: sendResult.ok ? (sendResult.status === "sent" ? "success" : "skipped") : "provider_error",
      idempotencyKey: turn.providerMessageId,
    });
    await markProviderMessageProcessed(turn.providerMessageId, sendResult.ok ? "replied" : "failed", sendResult.ok ? undefined : sendResult.reason);

    results.push({
      providerMessageId: turn.providerMessageId,
      status: sendResult.ok ? "unsupported_message_safe_reply" : "reply_failed",
      providerReplyId: sendResult.ok ? sendResult.providerMessageId : undefined,
      reason: sendResult.ok ? undefined : sendResult.reason,
      phoneNumberId: turn.phoneNumberId,
      messageType: turn.messageType,
    });
  }

  for (const turn of turns) {
    const turnStartedAt = Date.now();
    const registered = await registerProviderMessage({
      providerContactId: turn.providerContactId,
      providerMessageId: turn.providerMessageId,
      phone: turn.fromPhone,
      phoneNumberId: turn.phoneNumberId,
      displayPhoneNumber: turn.displayPhoneNumber,
    });

    if (!registered.ok) {
      results.push({ providerMessageId: turn.providerMessageId, status: "failed", reason: registered.reason });
      continue;
    }

    if (registered.duplicate) {
      results.push({ providerMessageId: turn.providerMessageId, status: "duplicate_ignored" });
      continue;
    }

    if (registered.session.status === "optedOut") {
      await markProviderMessageProcessed(turn.providerMessageId, "processed");
      results.push({ providerMessageId: turn.providerMessageId, status: "opted_out" });
      continue;
    }

    const salesLead = await findSalesLeadForWhatsApp({
      providerContactId: turn.providerContactId,
      phone: turn.fromPhone,
    });

    if (registered.session.status === "humanActive" || salesLead?.aiPaused || salesLead?.status === "human_active" || salesLead?.status === "do_not_contact") {
      await appendWhatsAppMessages(turn.providerContactId, [{ id: turn.providerMessageId, role: "user", content: turn.text }]);
      await markProviderMessageProcessed(turn.providerMessageId, "processed");
      results.push({
        providerMessageId: turn.providerMessageId,
        status: salesLead?.status === "do_not_contact" ? "do_not_contact" : "ai_paused_human_active",
        leadId: salesLead?.leadId,
      });
      continue;
    }

    if (!isWithinWhatsAppCustomerServiceWindow(turn.occurredAt)) {
      await appendWhatsAppMessages(turn.providerContactId, [{ id: turn.providerMessageId, role: "user", content: turn.text }]);
      await logAiUsageEvent({
        sessionId: registered.session.channelSessionId,
        channel: "whatsapp",
        niche: pilatesLanding.niche,
        provider: "meta_whatsapp_cloud_api",
        status: "skipped",
        idempotencyKey: turn.providerMessageId,
      });
      await markProviderMessageProcessed(turn.providerMessageId, "processed");
      results.push({
        providerMessageId: turn.providerMessageId,
        status: "outside_customer_service_window",
        reason: "Free-form WhatsApp replies are limited to the 24h customer service window.",
      });
      continue;
    }

    if (!hasPostgresStorage()) {
      const result = await processQueuedWhatsAppBatch({
        batchTurns: [
          {
            ...turn,
            queueId: `wa_memory_${turn.providerMessageId}`,
            batchId: `wa_memory_batch_${turn.providerMessageId}`,
          },
        ],
        turnStartedAt,
      });
      results.push(result);
      continue;
    }

    const queued = await enqueueWhatsAppTurn(turn, registered.session.channelSessionId);
    if (isExternalWhatsAppWorkerConfigured()) {
      afterResponse("trigger_whatsapp_queue_worker", () => triggerWhatsAppQueueWorker({
        channelSessionId: registered.session.channelSessionId,
        providerContactId: turn.providerContactId,
      }));
      results.push({
        providerMessageId: turn.providerMessageId,
        status: queued.inserted ? "queued_for_worker" : "queued_duplicate",
        reason: "WhatsApp turn queued for the Railway worker.",
        phoneNumberId: turn.phoneNumberId,
        leadId: salesLead?.leadId,
      });
      continue;
    }

    const lockOwnerId = `whatsapp_lock_${randomUUID()}`;
    const lock = await acquireWhatsAppTurnLock(registered.session.channelSessionId, lockOwnerId);
    if (!lock.acquired) {
      afterResponse("drain_queued_whatsapp_turn", () => drainQueuedWhatsAppTurnsLater({
        channelSessionId: registered.session.channelSessionId,
        providerContactId: turn.providerContactId,
      }));
      results.push({
        providerMessageId: turn.providerMessageId,
        status: queued.inserted ? "queued" : "queued_duplicate",
        reason: "Another WhatsApp turn is already processing for this conversation.",
        phoneNumberId: turn.phoneNumberId,
        leadId: salesLead?.leadId,
      });
      continue;
    }

    try {
      const batchResults = await processPendingWhatsAppBatches({
        channelSessionId: registered.session.channelSessionId,
        providerContactId: turn.providerContactId,
        lockOwnerId,
        turnStartedAt,
      });
      results.push(...batchResults);
    } finally {
      await releaseWhatsAppTurnLock(registered.session.channelSessionId, lockOwnerId);
    }
  }

  return Response.json({ status: "processed", results });
}

async function processQueuedWhatsAppBatch({
  batchTurns,
  turnStartedAt,
}: {
  batchTurns: QueuedWhatsAppTurn[];
  turnStartedAt: number;
}) {
  const turn = composeWhatsAppBatchTurn(batchTurns);
  const session = await getOrCreateWhatsAppSession({
    providerContactId: turn.providerContactId,
    phone: turn.fromPhone,
    phoneNumberId: turn.phoneNumberId,
    displayPhoneNumber: turn.displayPhoneNumber,
  });
  const salesLead = await findSalesLeadForWhatsApp({
    providerContactId: turn.providerContactId,
    phone: turn.fromPhone,
  });
  const requestedOptOut = isOptOutText(turn.text);

  const requestPayload = normalizeWhatsAppTurnToRequest({
    baseRequest: {
      campaignStage: pilatesLanding.tracking.campaignStage,
      publicOfferMode: pilatesLanding.tracking.publicOfferMode,
    },
    turn,
    messages: session.messages,
    qualificationDraft: session.qualification,
    selectedPainIds: session.selectedPainIds,
    recommendedAgentIds: session.recommendedAgentIds,
    optedOut: false,
  });
  requestPayload.metadata = {
    ...requestPayload.metadata,
    batchedWhatsappMessages: batchTurns.length > 1,
    batchedMessageCount: batchTurns.length,
    batchedProviderMessageIds: batchTurns.map((item) => item.providerMessageId),
  };
  if (salesLead) {
    requestPayload.session.leadId = salesLead.leadId;
  }
  const deliveryDrainBatch = batchTurns.some((item) => item.batchId?.includes(":drain:"));

  const semanticTurnIdempotencyKey = createWhatsAppSemanticTurnIdempotencyKey({
    providerContactId: turn.providerContactId,
    text: turn.text,
    qualification: session.qualification,
  });
  const semanticTurnReservation = await reserveAgentV2IdempotencyKey(semanticTurnIdempotencyKey, "whatsapp_semantic_turn");
  if (semanticTurnReservation.duplicate) {
    await logAiUsageEvent({
      sessionId: session.channelSessionId,
      channel: "whatsapp",
      niche: pilatesLanding.niche,
      provider: "meta_whatsapp_cloud_api",
      status: "skipped",
      idempotencyKey: semanticTurnIdempotencyKey,
    });
    await markBatchProviderMessagesProcessed(batchTurns, "processed", "semantic_duplicate");
    return {
      providerMessageId: turn.providerMessageId,
      providerMessageIds: batchTurns.map((item) => item.providerMessageId),
      status: "semantic_duplicate_ignored",
      reason: "Same text received again in the same pending conversation state.",
      phoneNumberId: turn.phoneNumberId,
      leadId: salesLead?.leadId,
    };
  }

  const runtimeStartedAt = Date.now();
  let stopTyping = () => {};
  if (!deliveryDrainBatch) {
    await sendMetaWhatsAppTypingIndicator({
      messageId: turn.replyToProviderMessageId,
      phoneNumberId: turn.phoneNumberId,
    });
    stopTyping = startMetaWhatsAppTypingKeepAlive({
      messageId: turn.replyToProviderMessageId,
      phoneNumberId: turn.phoneNumberId,
      intervalMs: 3000,
      initialDelayMs: 3500,
    });
  }
  let response: Awaited<ReturnType<typeof runAiAttendantTurn>>;
  try {
    response = await runAiAttendantTurn(requestPayload);
  } catch (error) {
    stopTyping();
    await completeAgentV2IdempotencyKey(semanticTurnIdempotencyKey, "failed");
    throw error;
  }
  const runtimeFinishedAt = Date.now();
  afterResponse("record_whatsapp_turn_event", () => recordFunnelEvent({
    eventName: funnelEventName(response),
    request: requestPayload,
    response,
    leadId: salesLead?.leadId,
  }));
  await appendWhatsAppMessages(turn.providerContactId, [
    ...batchTurns.map((item) => ({ id: item.providerMessageId, role: "user" as const, content: item.text })),
    ...response.assistantMessages,
  ]);
  await updateWhatsAppSessionState(turn.providerContactId, {
    selectedPainIds: response.capturedPainIds.length ? response.capturedPainIds : session.selectedPainIds,
    recommendedAgentIds: response.recommendedAgentIds.length ? response.recommendedAgentIds : session.recommendedAgentIds,
    qualification: {
      ...session.qualification,
      ...response.qualificationPatch,
    },
  });

  if (requestedOptOut || response.guardrailDecision.reason.toLowerCase().includes("opt-out") || response.guardrailDecision.visibleMessage?.toLowerCase().includes("parar")) {
    await markWhatsAppOptOut(turn.providerContactId);
    if (salesLead) {
      const optOutAction = await applyOperatorAction({
        action: "mark_do_not_contact",
        actorUserId: "system:whatsapp_opt_out",
        leadId: salesLead.leadId,
        payload: {
          providerContactId: turn.providerContactId,
          reason: "whatsapp_opt_out",
        },
      });
      if (optOutAction.ok) {
        afterResponse("dispatch_whatsapp_opt_out_operator_action", async () => {
          const syncResult = await dispatchN8nEvent("landing_ai_attendant_operator_action", {
            eventName: "sales_inbox_operator_action",
            occurredAt: new Date().toISOString(),
            lead: {
              leadId: optOutAction.lead.leadId,
              status: optOutAction.lead.status,
              priority: optOutAction.lead.priority,
              readiness: optOutAction.lead.readiness,
              channel: optOutAction.lead.channel,
              conversionPath: optOutAction.lead.conversionPath,
              selectedPlanId: optOutAction.lead.selectedPlanId,
              nextAction: optOutAction.lead.nextAction,
              summary: optOutAction.lead.summary,
            },
            action: optOutAction.action,
          });
          await updateSalesLeadSyncStatus(optOutAction.lead.leadId, salesInboxSyncStatusFromN8nResult(syncResult), {
            eventName: "sales_inbox_operator_action",
            n8nStatus: syncResult.status,
            n8nReason: "reason" in syncResult ? syncResult.reason : undefined,
            n8nStatusCode: "statusCode" in syncResult ? syncResult.statusCode : undefined,
          });
        });
      }
    }
  }

  const replyTexts = responseToWhatsAppTexts(response);
  const replyText = replyTexts.join("\n\n");
  if (deliveryDrainBatch && replyTexts.length) {
    await sendMetaWhatsAppTypingIndicator({
      messageId: turn.replyToProviderMessageId,
      phoneNumberId: turn.phoneNumberId,
    });
    stopTyping = startMetaWhatsAppTypingKeepAlive({
      messageId: turn.replyToProviderMessageId,
      phoneNumberId: turn.phoneNumberId,
      intervalMs: 3000,
      initialDelayMs: 3500,
    });
  }
  const leadStorage = await ensureSalesLeadBeforeWhatsAppSend({
    existingLead: salesLead,
    request: requestPayload,
    response,
  });
  const activeSalesLead = leadStorage.salesLead ?? salesLead;
  const sendStartedAt = Date.now();
  const sendResult = await sendMetaWhatsAppReplySequence({
    contents: replyTexts,
    replyToProviderMessageId: turn.replyToProviderMessageId,
    to: turn.fromPhone ?? turn.providerContactId,
    phoneNumberId: turn.phoneNumberId,
    idempotencyKey: `ai_reply_batch:${turn.providerMessageId}`,
    leadId: activeSalesLead?.leadId,
    channelSessionId: session.channelSessionId,
    providerContactId: turn.providerContactId,
  });
  const sendFinishedAt = Date.now();
  stopTyping();
  logWhatsAppLatency({
    providerMessageId: turn.providerMessageId,
    leadId: activeSalesLead?.leadId,
    runtimeMs: runtimeFinishedAt - runtimeStartedAt,
    sendMs: sendFinishedAt - sendStartedAt,
    totalMs: sendFinishedAt - turnStartedAt,
    chunks: replyTexts.length,
    status: sendResult.ok ? sendResult.status : sendResult.status,
  });

  afterResponse("log_whatsapp_usage_event", () => logAiUsageEvent({
    sessionId: requestPayload.session.sessionId,
    channel: "whatsapp",
    niche: pilatesLanding.niche,
    provider: "meta_whatsapp_cloud_api",
    status: sendResult.ok ? "success" : "provider_error",
    latencyMs: sendFinishedAt - turnStartedAt,
    idempotencyKey: turn.providerMessageId,
  }));
  await markBatchProviderMessagesProcessed(batchTurns, sendResult.ok ? "replied" : "failed", sendResult.ok ? undefined : sendResult.reason);
  await completeAgentV2IdempotencyKey(semanticTurnIdempotencyKey, sendResult.ok ? "processed" : "failed");

  if (!sendResult.ok) {
    response.qualificationPatch = {
      ...response.qualificationPatch,
      closureState: "error_needs_attention",
      humanActive: "requested",
      aiPaused: "true",
      nextAction: `Falha ao enviar resposta pelo WhatsApp; operador deve assumir. Motivo: ${sendResult.reason.slice(0, 180)}`,
    };
    if (activeSalesLead) {
      await applyOperatorAction({
        action: "take_over",
        actorUserId: "system:whatsapp_send_failure",
        leadId: activeSalesLead.leadId,
        payload: {
          providerContactId: turn.providerContactId,
          phoneNumberId: turn.phoneNumberId,
          reason: "whatsapp_send_failure",
          error: sendResult.reason,
        },
      });
    }
  }

  if (response.conversionPath || response.guardrailDecision.category !== "allowed") {
    const storedLead = activeSalesLead;
    if (storedLead) {
      afterResponse("record_whatsapp_conversion_event", () => recordFunnelEvent({
        eventName: response.conversionPath ? `floating_agent_${response.conversionPath}` : "floating_agent_fallback",
        request: requestPayload,
        response,
        leadId: storedLead.leadId,
      }));
    }

    afterResponse("dispatch_whatsapp_conversion_event", () => dispatchN8nEvent(response.guardrailDecision.category !== "allowed" ? "landing_ai_attendant_safety_event" : "landing_ai_attendant_high_intent", {
      eventName: response.conversionPath ? `floating_agent_${response.conversionPath}` : "floating_agent_fallback",
      occurredAt: new Date().toISOString(),
      niche: pilatesLanding.niche,
      sourcePage: "whatsapp",
      campaignStage: pilatesLanding.tracking.campaignStage,
      publicOfferMode: pilatesLanding.tracking.publicOfferMode,
      sessionId: requestPayload.session.sessionId,
      channel: "whatsapp",
      conversionPath: response.conversionPath,
      lead: leadStorage.leadRecord,
      selectedPainIds: response.capturedPainIds,
      recommendedAgentIds: response.recommendedAgentIds,
      safeSummary: response.assistantMessages.map((message) => message.intent).join(", "),
      guardrailDecision: response.guardrailDecision,
    }));
    if (storedLead) {
      afterResponse("update_whatsapp_conversion_sync_status", () => updateSalesLeadSyncStatus(storedLead.leadId, "skipped", {
        eventName: "lead_stored_locally",
        reason: "Lead stored in Sales Inbox/Postgres. External CRM lead sync is disabled.",
      }));
    }
    const leadToNotify = leadStorage.leadRecord;
    if (leadToNotify && shouldNotifyOperator(leadToNotify.priority, leadToNotify.conversionPath)) {
      afterResponse("dispatch_whatsapp_operator_alert", () => dispatchN8nEvent("landing_ai_attendant_lead_alert", {
        eventName: "sales_lead_urgent_alert",
        occurredAt: new Date().toISOString(),
        lead: {
          leadId: leadToNotify.leadId,
          priority: leadToNotify.priority,
          readiness: leadToNotify.readiness,
          channel: leadToNotify.channel,
          conversionPath: leadToNotify.conversionPath,
          selectedPlanId: leadToNotify.selectedPlanId,
          nextAction: leadToNotify.nextAction,
          summary: leadToNotify.summary,
        },
      }));
    }
  }

  if (leadStorage.kind === "cold_lead" && activeSalesLead) {
    afterResponse("record_whatsapp_cold_lead_event", () => recordFunnelEvent({
      eventName: "floating_agent_cold_lead_recorded",
      request: requestPayload,
      response,
      leadId: activeSalesLead.leadId,
    }));
    afterResponse("update_whatsapp_cold_lead_sync_status", () => updateSalesLeadSyncStatus(activeSalesLead.leadId, "skipped", {
      eventName: "cold_lead_recorded",
      reason: "Cold lead stored in Sales Inbox without external lead sync.",
    }));
  }

  if (activeSalesLead) {
    await appendWhatsAppSalesLeadTurn(
      activeSalesLead.leadId,
      requestPayload,
      response,
      batchTurns,
      sendResult.ok ? "delivered" : "failed",
    );
  }

  return {
    providerMessageId: turn.providerMessageId,
    providerMessageIds: batchTurns.map((item) => item.providerMessageId),
    status: sendResult.ok ? sendResult.status : "reply_failed",
    providerReplyId: sendResult.ok ? sendResult.providerMessageId : undefined,
    providerReplyIds: sendResult.ok ? sendResult.providerMessageIds : sendResult.providerMessageIds,
    replyPreview: replyText.slice(0, 500),
    replyPreviews: replyTexts.map((text) => text.slice(0, 500)),
    reason: sendResult.ok ? undefined : sendResult.reason,
    phoneNumberId: turn.phoneNumberId,
    leadId: activeSalesLead?.leadId,
    latencyMs: sendFinishedAt - turnStartedAt,
    batchedMessageCount: batchTurns.length,
  };
}

function summarizeColdWhatsAppLead(request: Parameters<typeof summarizeConversation>[0], response: Awaited<ReturnType<typeof runAiAttendantTurn>>) {
  const current = request.userMessage?.trim();
  const base = summarizeConversation(request);
  const next = response.nextQuestion ? ` Próxima pergunta: ${response.nextQuestion}` : "";
  return `${base}${current ? ` Mensagem atual: ${current.slice(0, 240)}.` : ""}${next}`.slice(0, 900);
}

async function ensureSalesLeadBeforeWhatsAppSend({
  existingLead,
  request,
  response,
}: {
  existingLead: Awaited<ReturnType<typeof findSalesLeadForWhatsApp>>;
  request: Parameters<typeof summarizeConversation>[0];
  response: Awaited<ReturnType<typeof runAiAttendantTurn>>;
}) {
  if (response.conversionPath) {
    const context = buildAiAttendantContext(request);
    const handoff = response.conversionPath
      ? createConversionHandoff({
          config: context.nicheConfig,
          conversionPath: response.conversionPath,
          request,
          selectedPlanId: response.subscription?.planId,
          summary: summarizeConversation(request),
        })
      : undefined;
    if (!handoff) return { kind: "none" as const, salesLead: existingLead, leadRecord: undefined };
    handoff.qualification = {
      ...handoff.qualification,
      ...response.qualificationPatch,
    };
    handoff.selectedPainIds = Array.from(new Set([...handoff.selectedPainIds, ...response.capturedPainIds]));
    handoff.recommendedAgentIds = Array.from(new Set([...handoff.recommendedAgentIds, ...response.recommendedAgentIds]));
    const leadRecord = createLeadRecord({
      config: context.nicheConfig,
      eventName: `floating_agent_${response.conversionPath}`,
      handoff,
      request,
      response,
    });
    const salesLead = await upsertSalesLead(leadRecord);
    return { kind: "conversion" as const, salesLead, leadRecord };
  }

  if (!response.conversionPath && (!existingLead || existingLead.conversionPath === "cold_lead")) {
    const context = buildAiAttendantContext(request);
    const handoff = createConversionHandoff({
      config: context.nicheConfig,
      conversionPath: "cold_lead",
      request,
      summary: summarizeColdWhatsAppLead(request, response),
    });
    handoff.qualification = {
      ...handoff.qualification,
      ...response.qualificationPatch,
    };
    handoff.selectedPainIds = Array.from(new Set([...handoff.selectedPainIds, ...response.capturedPainIds]));
    handoff.recommendedAgentIds = Array.from(new Set([...handoff.recommendedAgentIds, ...response.recommendedAgentIds]));

    const leadRecord = createLeadRecord({
      config: context.nicheConfig,
      eventName: "floating_agent_cold_lead",
      handoff,
      request,
      response,
    });
    const salesLead = await upsertSalesLead(leadRecord);
    return { kind: "cold_lead" as const, salesLead, leadRecord };
  }

  return { kind: "existing" as const, salesLead: existingLead, leadRecord: existingLead ?? undefined };
}

function logWhatsAppLatency({
  providerMessageId,
  leadId,
  runtimeMs,
  sendMs,
  totalMs,
  chunks,
  status,
}: {
  providerMessageId: string;
  leadId?: string;
  runtimeMs: number;
  sendMs: number;
  totalMs: number;
  chunks: number;
  status: string;
}) {
  console.info("[whatsapp-latency]", {
    providerMessageId,
    leadId,
    runtimeMs,
    sendMs,
    totalMs,
    chunks,
    status,
  });
}

function handleInternalWhatsAppWorkerRequest(request: Request, rawBody: string) {
  if (!request.headers.has("x-taliya-whatsapp-worker-secret")) return null;

  const secret = process.env.TALIYA_WHATSAPP_WORKER_SECRET;
  if (!secret || request.headers.get("x-taliya-whatsapp-worker-secret") !== secret) {
    return Response.json({ error: "unauthorized_worker_request" }, { status: 401 });
  }

  const payload = parseWorkerPayload(rawBody);
  if (!payload) {
    return Response.json({ error: "invalid_worker_payload" }, { status: 400 });
  }

  afterResponse("process_whatsapp_queue_worker", async () => {
    await drainQueuedWhatsAppTurnsLater({
      channelSessionId: payload.channelSessionId,
      providerContactId: payload.providerContactId,
    });
    if (await hasPendingWhatsAppTurns(payload.channelSessionId, payload.providerContactId)) {
      await triggerWhatsAppQueueWorker(payload);
    }
  });

  return Response.json({
    status: "accepted",
    channelSessionId: payload.channelSessionId,
    providerContactId: payload.providerContactId,
  });
}

function parseWorkerPayload(rawBody: string): { channelSessionId: string; providerContactId: string } | null {
  try {
    const payload = JSON.parse(rawBody) as Record<string, unknown>;
    const channelSessionId = typeof payload.channelSessionId === "string" ? payload.channelSessionId.trim() : "";
    const providerContactId = typeof payload.providerContactId === "string" ? payload.providerContactId.trim() : "";
    if (!channelSessionId || !providerContactId) return null;
    return { channelSessionId, providerContactId };
  } catch {
    return null;
  }
}

function isExternalWhatsAppWorkerConfigured() {
  return Boolean(process.env.TALIYA_WHATSAPP_WORKER_URL && process.env.TALIYA_WHATSAPP_WORKER_SECRET);
}

async function triggerWhatsAppQueueWorker({
  channelSessionId,
  providerContactId,
}: {
  channelSessionId: string;
  providerContactId: string;
}) {
  const url = process.env.TALIYA_WHATSAPP_WORKER_URL?.replace(/\/+$/g, "");
  const secret = process.env.TALIYA_WHATSAPP_WORKER_SECRET;
  if (!url || !secret) return;

  const controller = new AbortController();
  const timeout = setTimeout(() => controller.abort(), positiveNumberFromEnv("TALIYA_WHATSAPP_WORKER_TRIGGER_TIMEOUT_MS", 5000));
  try {
    const response = await fetch(`${url}/api/landing/ai-attendant/whatsapp`, {
      method: "POST",
      headers: {
        "content-type": "application/json",
        "x-taliya-whatsapp-worker-secret": secret,
      },
      body: JSON.stringify({ channelSessionId, providerContactId }),
      signal: controller.signal,
    });
    if (!response.ok) {
      console.error("[whatsapp-worker-trigger]", {
        status: response.status,
        channelSessionId,
        providerContactId,
      });
    }
  } catch (error) {
    console.error("[whatsapp-worker-trigger]", {
      reason: error instanceof Error ? error.message : "worker trigger failed",
      channelSessionId,
      providerContactId,
    });
  } finally {
    clearTimeout(timeout);
  }
}

function createWhatsAppSemanticTurnIdempotencyKey({
  providerContactId,
  qualification,
  text,
}: {
  providerContactId: string;
  qualification: QualificationDraft;
  text: string;
}) {
  const normalizedText = normalizeSemanticTurnText(text);
  const pendingContext = [
    qualification.commercialStage,
    qualification.diagnosticStatus,
    qualification.diagnosticNextStep,
    qualification.diagnosticCompleted,
    qualification.waitlistStatus,
    qualification.demoStatus,
  ]
    .filter(Boolean)
    .join("|");
  const windowMs = positiveNumberFromEnv("AI_ATTENDANT_WHATSAPP_SEMANTIC_DEDUPE_WINDOW_MS", 120_000);
  const bucket = Math.floor(Date.now() / windowMs);
  return [
    "whatsapp",
    "semantic_turn",
    providerContactId,
    bucket,
    stableHash(normalizedText),
    stableHash(pendingContext || "no_pending_context"),
  ].join(":");
}

async function enqueueWhatsAppTurn(turn: WhatsAppInboundTurn, channelSessionId: string) {
  if (!hasPostgresStorage()) return { inserted: true };
  const queueId = `wa_queue_${randomUUID()}`;
  const inserted = await postgresQuery<{ queue_id: string }>(
    `INSERT INTO whatsapp_turn_queue (
       queue_id, channel_session_id, provider_contact_id, provider_message_id,
       phone_number_id, display_phone_number, from_phone, profile_name, text, occurred_at, status,
       created_at, updated_at
     ) VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9, $10::timestamptz, 'pending', now(), now())
     ON CONFLICT (provider_message_id) DO NOTHING
     RETURNING queue_id`,
    [
      queueId,
      channelSessionId,
      turn.providerContactId,
      turn.providerMessageId,
      turn.phoneNumberId,
      turn.displayPhoneNumber,
      turn.fromPhone,
      turn.profileName,
      turn.text,
      turn.occurredAt,
    ],
  );
  return { inserted: Boolean(inserted.rows.length) };
}

async function acquireWhatsAppTurnLock(channelSessionId: string, ownerId: string) {
  if (!hasPostgresStorage()) return { acquired: true };
  const ttlMs = positiveNumberFromEnv("AI_ATTENDANT_WHATSAPP_TURN_LOCK_TTL_MS", 90_000);
  const lockedUntil = new Date(Date.now() + ttlMs).toISOString();
  const result = await postgresQuery<{ owner_id: string }>(
    `INSERT INTO whatsapp_turn_locks (channel_session_id, owner_id, locked_until, created_at, updated_at)
     VALUES ($1, $2, $3::timestamptz, now(), now())
     ON CONFLICT (channel_session_id) DO UPDATE
       SET owner_id = EXCLUDED.owner_id,
           locked_until = EXCLUDED.locked_until,
           updated_at = now()
       WHERE whatsapp_turn_locks.locked_until < now()
     RETURNING owner_id`,
    [channelSessionId, ownerId, lockedUntil],
  );
  return { acquired: result.rows[0]?.owner_id === ownerId };
}

async function releaseWhatsAppTurnLock(channelSessionId: string, ownerId: string) {
  if (!hasPostgresStorage()) return;
  await postgresQuery(
    "DELETE FROM whatsapp_turn_locks WHERE channel_session_id = $1 AND owner_id = $2",
    [channelSessionId, ownerId],
  );
}

async function processPendingWhatsAppBatches({
  channelSessionId,
  providerContactId,
  lockOwnerId,
  turnStartedAt,
}: {
  channelSessionId: string;
  providerContactId: string;
  lockOwnerId: string;
  turnStartedAt: number;
}) {
  const results = [];
  const maxBatches = positiveNumberFromEnv("AI_ATTENDANT_WHATSAPP_MAX_BATCHES_PER_LOCK", 1);
  for (let index = 0; index < maxBatches; index += 1) {
    await waitForInboundBatchWindow(index === 0 ? "initial" : "drain");
    await extendWhatsAppTurnLock(channelSessionId, lockOwnerId);
    const batchId = `wa_batch_${randomUUID()}${index === 0 ? ":initial" : ":drain:" + index}`;
    const batchTurns = await claimPendingWhatsAppTurns(channelSessionId, batchId);
    if (!batchTurns.length) break;
    try {
      const result = await processQueuedWhatsAppBatch({
        batchTurns,
        turnStartedAt: index === 0 ? turnStartedAt : Date.now(),
      });
      await markWhatsAppTurnBatch(batchTurns, "processed");
      results.push(result);
    } catch (error) {
      await markWhatsAppTurnBatch(batchTurns, "failed", error instanceof Error ? error.message : "batch failed");
      throw error;
    }
    if (index < maxBatches - 1) {
      await waitForInboundBatchWindow("drain");
      await extendWhatsAppTurnLock(channelSessionId, lockOwnerId);
    }
    const hasMore = await hasPendingWhatsAppTurns(channelSessionId, providerContactId);
    if (!hasMore) break;
  }
  return results;
}

async function drainQueuedWhatsAppTurnsLater({
  channelSessionId,
  providerContactId,
}: {
  channelSessionId: string;
  providerContactId: string;
}) {
  const startedAt = Date.now();
  const retryBudgetMs = Math.min(55_000, positiveNumberFromEnv("AI_ATTENDANT_WHATSAPP_DEFERRED_DRAIN_RETRY_MS", 45_000));
  while (Date.now() - startedAt < retryBudgetMs) {
    await waitForInboundBatchWindow("drain");
    if (!(await hasPendingWhatsAppTurns(channelSessionId, providerContactId))) return;
    const lockOwnerId = `whatsapp_deferred_lock_${randomUUID()}`;
    const lock = await acquireWhatsAppTurnLock(channelSessionId, lockOwnerId);
    if (!lock.acquired) {
      await sleep(Math.min(2500, positiveNumberFromEnv("AI_ATTENDANT_WHATSAPP_DEFERRED_DRAIN_RETRY_DELAY_MS", 1500)));
      continue;
    }
    try {
      await processPendingWhatsAppBatches({
        channelSessionId,
        providerContactId,
        lockOwnerId,
        turnStartedAt: Date.now(),
      });
      return;
    } finally {
      await releaseWhatsAppTurnLock(channelSessionId, lockOwnerId);
    }
  }
}

async function extendWhatsAppTurnLock(channelSessionId: string, ownerId: string) {
  if (!hasPostgresStorage()) return;
  const ttlMs = positiveNumberFromEnv("AI_ATTENDANT_WHATSAPP_TURN_LOCK_TTL_MS", 90_000);
  await postgresQuery(
    `UPDATE whatsapp_turn_locks
     SET locked_until = $3::timestamptz, updated_at = now()
     WHERE channel_session_id = $1 AND owner_id = $2`,
    [channelSessionId, ownerId, new Date(Date.now() + ttlMs).toISOString()],
  );
}

async function waitForInboundBatchWindow(kind: "initial" | "drain") {
  const fallback = kind === "initial" ? 2500 : 2000;
  const envKey = kind === "initial" ? "AI_ATTENDANT_WHATSAPP_INBOUND_DEBOUNCE_MS" : "AI_ATTENDANT_WHATSAPP_POST_DELIVERY_DRAIN_MS";
  const delayMs = Math.min(8000, positiveNumberFromEnv(envKey, fallback));
  if (process.env.NODE_ENV === "test") return;
  await new Promise((resolve) => setTimeout(resolve, delayMs));
}

async function sleep(delayMs: number) {
  if (process.env.NODE_ENV === "test") return;
  await new Promise((resolve) => setTimeout(resolve, delayMs));
}

async function claimPendingWhatsAppTurns(channelSessionId: string, batchId: string): Promise<QueuedWhatsAppTurn[]> {
  if (!hasPostgresStorage()) return [];
  await recoverStaleProcessingWhatsAppTurns(channelSessionId);
  const result = await postgresQuery<WhatsAppTurnQueueRow>(
    `WITH claimed AS (
       SELECT queue_id
       FROM whatsapp_turn_queue
       WHERE channel_session_id = $1 AND status = 'pending'
       ORDER BY occurred_at ASC, created_at ASC
       LIMIT 12
       FOR UPDATE SKIP LOCKED
     )
     UPDATE whatsapp_turn_queue q
     SET status = 'processing', batch_id = $2, updated_at = now()
     FROM claimed
     WHERE q.queue_id = claimed.queue_id
     RETURNING q.*`,
    [channelSessionId, batchId],
  );
  return result.rows.map((row) => rowToQueuedWhatsAppTurn(row));
}

async function hasPendingWhatsAppTurns(channelSessionId: string, providerContactId: string) {
  if (!hasPostgresStorage()) return false;
  await recoverStaleProcessingWhatsAppTurns(channelSessionId, providerContactId);
  const result = await postgresQuery<{ has_pending: boolean }>(
    `SELECT EXISTS (
       SELECT 1 FROM whatsapp_turn_queue
       WHERE (channel_session_id = $1 OR provider_contact_id = $2)
         AND status = 'pending'
     ) AS has_pending`,
    [channelSessionId, providerContactId],
  );
  return Boolean(result.rows[0]?.has_pending);
}

async function recoverStaleProcessingWhatsAppTurns(channelSessionId: string, providerContactId?: string) {
  if (!hasPostgresStorage()) return;
  const staleMs = positiveNumberFromEnv("AI_ATTENDANT_WHATSAPP_PROCESSING_STALE_MS", 95_000);
  await postgresQuery(
    `UPDATE whatsapp_turn_queue q
     SET status = 'pending',
         batch_id = NULL,
         last_error = 'recovered_stale_processing_after_lock_expiry',
         updated_at = now()
     WHERE q.status = 'processing'
       AND (q.channel_session_id = $1 OR q.provider_contact_id = COALESCE($2, q.provider_contact_id))
       AND q.updated_at < $3::timestamptz
       AND NOT EXISTS (
         SELECT 1
         FROM whatsapp_turn_locks l
         WHERE l.channel_session_id = q.channel_session_id
           AND l.locked_until > now()
       )`,
    [channelSessionId, providerContactId ?? null, new Date(Date.now() - staleMs).toISOString()],
  );
}

async function markWhatsAppTurnBatch(batchTurns: QueuedWhatsAppTurn[], status: "processed" | "failed", reason?: string) {
  if (!hasPostgresStorage() || !batchTurns.length) return;
  await postgresQuery(
    `UPDATE whatsapp_turn_queue
     SET status = $2, last_error = $3, updated_at = now()
     WHERE queue_id = ANY($1::text[])`,
    [batchTurns.map((turn) => turn.queueId), status, reason?.slice(0, 500)],
  );
}

async function markBatchProviderMessagesProcessed(batchTurns: QueuedWhatsAppTurn[], status: "processed" | "replied" | "failed", errorCode?: string) {
  for (const turn of batchTurns) {
    await markProviderMessageProcessed(turn.providerMessageId, status, errorCode);
  }
}

function composeWhatsAppBatchTurn(batchTurns: QueuedWhatsAppTurn[]): WhatsAppInboundTurn & { replyToProviderMessageId: string } {
  const first = batchTurns[0];
  return {
    provider: "meta_whatsapp_cloud_api",
    providerMessageId: first.batchId || first.providerMessageId,
    providerContactId: first.providerContactId,
    fromPhone: first.fromPhone,
    profileName: first.profileName,
    phoneNumberId: first.phoneNumberId,
    displayPhoneNumber: first.displayPhoneNumber,
    text: batchTurns.map((turn) => turn.text.trim()).filter(Boolean).join("\n"),
    occurredAt: first.occurredAt,
    rawSignatureVerified: batchTurns.every((turn) => turn.rawSignatureVerified),
    replyToProviderMessageId: first.providerMessageId,
  };
}

type WhatsAppTurnQueueRow = {
  queue_id: string;
  channel_session_id: string;
  provider_contact_id: string;
  provider_message_id: string;
  phone_number_id?: string | null;
  display_phone_number?: string | null;
  from_phone?: string | null;
  profile_name?: string | null;
  text: string;
  occurred_at: string | Date;
  batch_id?: string | null;
};

function rowToQueuedWhatsAppTurn(row: WhatsAppTurnQueueRow): QueuedWhatsAppTurn {
  return {
    queueId: row.queue_id,
    batchId: row.batch_id ?? undefined,
    provider: "meta_whatsapp_cloud_api",
    providerMessageId: row.provider_message_id,
    providerContactId: row.provider_contact_id,
    fromPhone: row.from_phone ?? undefined,
    profileName: row.profile_name ?? undefined,
    phoneNumberId: row.phone_number_id ?? undefined,
    displayPhoneNumber: row.display_phone_number ?? undefined,
    text: row.text,
    occurredAt: row.occurred_at instanceof Date ? row.occurred_at.toISOString() : row.occurred_at,
    rawSignatureVerified: true,
  };
}

function normalizeSemanticTurnText(text: string) {
  return text
    .normalize("NFD")
    .replace(/[\u0300-\u036f]/g, "")
    .toLowerCase()
    .replace(/\s+/g, " ")
    .trim();
}

function positiveNumberFromEnv(key: string, fallback: number) {
  const value = Number(process.env[key]);
  return Number.isFinite(value) && value > 0 ? value : fallback;
}

function stableHash(value: string) {
  let output = 0;
  for (let index = 0; index < value.length; index += 1) {
    output = (output << 5) - output + value.charCodeAt(index);
    output |= 0;
  }
  return Math.abs(output).toString(36);
}

function afterResponse(label: string, task: () => Promise<unknown>) {
  after(async () => {
    try {
      await task();
    } catch (error) {
      console.error(`[whatsapp-after:${label}]`, error);
    }
  });
}

async function appendWhatsAppSalesLeadTurn(
  leadId: string,
  request: Parameters<typeof summarizeConversation>[0],
  response: Awaited<ReturnType<typeof runAiAttendantTurn>>,
  turns: WhatsAppInboundTurn[],
  deliveryStatus: "delivered" | "failed",
) {
  const runtimeRunId = response.qualificationPatch?.agentRuntimeRunId;
  const runtimeTraceId = response.qualificationPatch?.agentRuntimeTraceId;
  const conversationId = request.session.channelSessionId || request.session.sessionId;
  const safetyFlags = response.qualificationPatch?.agentRuntimeGuardrailFlags
    ?.split(",")
    .map((flag) => flag.trim())
    .filter(Boolean) ?? [];
  const messages: Array<Parameters<typeof appendSalesLeadMessages>[1][number]> = [];

  for (const message of request.session.messages.slice(-36)) {
    messages.push({
      id: message.id,
      role: message.role,
      content: message.content,
      conversationId,
      channelSessionId: request.session.channelSessionId,
      channel: "whatsapp",
    });
  }

  for (const turn of turns) {
    messages.push({
      id: turn.providerMessageId,
      role: "user",
      content: turn.text,
      createdAt: turn.occurredAt,
      conversationId,
      channelSessionId: request.session.channelSessionId,
      providerMessageId: turn.providerMessageId,
      channel: "whatsapp",
      direction: "inbound",
      deliveryStatus: "received",
      runId: runtimeRunId,
      traceId: runtimeTraceId,
      safetyFlags,
      isSensitive: response.guardrailDecision.category === "sensitive_data",
      isProblematic: response.guardrailDecision.category !== "allowed",
    });
  }
  for (const message of response.assistantMessages) {
    messages.push({
      id: message.id,
      role: "assistant",
      content: message.content,
      conversationId,
      channelSessionId: request.session.channelSessionId,
      channel: "whatsapp",
      direction: "outbound",
      deliveryStatus,
      runId: runtimeRunId,
      traceId: runtimeTraceId,
      safetyFlags,
      isProblematic: deliveryStatus === "failed" || response.guardrailDecision.category !== "allowed",
    });
  }
  await appendSalesLeadMessages(leadId, messages);
}

function verifyWebhookSignature(rawBody: string, request: Request) {
  const metaSignature = verifyMetaSignature(rawBody, request.headers.get("x-hub-signature-256"));
  if (metaSignature.ok) return metaSignature;

  const dualhookSignatureHeader = request.headers.get("x-dualhook-signature");
  if (dualhookSignatureHeader) {
    return verifyDualhookSignature(rawBody, dualhookSignatureHeader);
  }

  if (hasDualhookSharedSecret(request)) {
    return verifyDualhookSharedSecret(request.url, request.headers.get("x-dualhook-webhook-secret") || request.headers.get("x-webhook-secret"));
  }

  return verifyExpectedWhatsAppPhoneNumber(rawBody);
}

function hasDualhookSharedSecret(request: Request) {
  const url = new URL(request.url);
  return Boolean(
    request.headers.get("x-dualhook-webhook-secret") ||
      request.headers.get("x-webhook-secret") ||
      url.searchParams.has("dualhook_secret") ||
      url.searchParams.has("webhook_secret"),
  );
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

function unsupportedWhatsAppMessageReply(messageType: string) {
  const readableType = messageType === "unknown" ? "esse tipo de mensagem" : `mensagem do tipo ${messageType}`;
  return `Recebi ${readableType}, mas por aqui consigo continuar melhor por texto. Me descreva em uma mensagem o que voce quer mostrar, que eu sigo te ajudando.`;
}

function funnelEventName(response: Awaited<ReturnType<typeof runAiAttendantTurn>>) {
  if (response.guardrailDecision.category === "rate_limited") return "rate_limit";
  if (response.guardrailDecision.category !== "allowed") return "guardrail";
  if (response.qualificationPatch?.closureState === "error_needs_attention") return "send_error";
  if (response.qualificationPatch?.waitlistStatus === "joined") return "waitlist_joined";
  if (response.qualificationPatch?.waitlistStatus === "offered") return "waitlist_offered";
  if (response.qualificationPatch?.diagnosticStatus === "offered") return "diagnostic_offered";
  if (response.qualificationPatch?.diagnosticStatus === "completed" || response.conversionPath === "crm_agent_diagnostic") return "diagnostic_completed";
  if (response.conversionPath === "view_plans") return "plans_viewed";
  if (response.conversionPath === "human_whatsapp_assist") return "human_handoff";
  return "assistant_turn";
}
