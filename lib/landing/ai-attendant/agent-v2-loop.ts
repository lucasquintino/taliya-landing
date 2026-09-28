// Quarantined legacy runtime.
// The official production path for Taliya commercial turns is now
// `lib/landing/ai-attendant/runtime-client.ts` -> `services/taliya-agent-runtime`.
// This module remains only as historical/rollback reference and must not be imported
// from the widget or WhatsApp production routes.
import type { AiAttendantResponse } from "./schema";
import type { AgentV2ConversationState, AgentV2LoopInput } from "./agent-v2-types";
import { getAgentV2Config, isAgentV2CaptureOnly, shouldAgentV2ReplyAutomatically } from "./agent-v2-flags";
import { buildChannelDeliveryPlan, normalizeAgentV2Input } from "./agent-v2-channel-adapter";
import { createInboundIdempotencyKey, completeAgentV2IdempotencyKey, reserveAgentV2IdempotencyKey } from "./agent-v2-idempotency";
import { buildInitialV2State, serializeV2State } from "./agent-v2-state-compat";
import { loadAgentV2State, saveAgentV2State } from "./agent-v2-state-store";
import { getProductKnowledge } from "./product-knowledge-source";
import { interpretLeadMessage } from "./agent-v2-semantic-interpreter";
import { orchestrateAgentV2Turn } from "./agent-v2-orchestrator";
import { executeAgentV2Tools } from "./agent-v2-tools";
import { generateAgentV2Response } from "./agent-v2-response-generator";
import { validateAgentV2Response, validateToolPlan } from "./agent-v2-guardrails";
import { estimateTurnUsage, getCostCapStatus, shouldBlockForCost } from "./agent-v2-cost-policy";
import { createTraceId, recordAgentV2Trace } from "./agent-v2-trace-store";
import { attachWidgetActions } from "./agent-v2-widget-delivery";
import { planWhatsAppChunks } from "./agent-v2-whatsapp-delivery";

export async function runAiAttendantTurnV2({ request, legacyTurn }: AgentV2LoopInput): Promise<AiAttendantResponse> {
  const config = getAgentV2Config();
  const normalizedInput = normalizeAgentV2Input(request);
  const turnId = normalizedInput.externalMessageId ?? `${Date.now()}_${Math.random().toString(36).slice(2, 8)}`;
  const idempotencyKey = createInboundIdempotencyKey({
    channel: normalizedInput.channel,
    conversationId: normalizedInput.conversationId,
    externalMessageId: normalizedInput.externalMessageId,
    text: `${request.session.messages.length}:${normalizedInput.text ?? ""}`,
  });
  const stateFromRequest = buildInitialV2State(request);
  const persistedState = await loadAgentV2State(stateFromRequest.conversationId);
  const stateBefore = persistedState ?? stateFromRequest;
  const product = getProductKnowledge();
  const traceId = createTraceId();

  const duplicate = await reserveAgentV2IdempotencyKey(idempotencyKey, "agent_v2_inbound");
  if (duplicate.duplicate) {
    await recordAgentV2Trace({
      id: traceId,
      leadId: request.session.leadId,
      conversationId: normalizedInput.conversationId,
      turnId,
      channel: request.session.channel,
      normalizedInput,
      stateBefore,
      productSourceVersion: product.version,
      toolActions: [],
      guardrailResult: { status: "blocked", reasons: ["duplicate_inbound"] },
      modelUsage: [],
      costEstimateUsd: 0,
      fallbackReason: "duplicate_inbound",
      createdAt: new Date().toISOString(),
    });
    return {
      assistantMessages: [],
      capturedPainIds: [],
      recommendedAgentIds: [],
      shouldOfferDiagnostic: false,
      guardrailDecision: {
        category: "allowed",
        action: "respond",
        reason: "Mensagem duplicada ignorada por idempotencia.",
      },
      qualificationPatch: {
        agentV2TraceId: traceId,
        agentV2CostEstimateUsd: "0",
        agentV2ProductSourceVersion: product.version,
        agentV2Priority: stateBefore.priority,
      },
    };
  }

  const interpretation = interpretLeadMessage(normalizedInput, stateBefore);
  const projectedUsage = estimateTurnUsage({
    input: `${normalizedInput.text ?? ""}\n${JSON.stringify(stateBefore.substate.knownFacts)}`,
    category: "simple_answer",
    operation: "interpretation",
    model: config.defaultModel,
  });

  const costBlockedState = shouldBlockForCost(stateBefore.substate, projectedUsage.estimatedCostUsd)
    ? {
        ...stateBefore,
        substate: {
          ...stateBefore.substate,
          cost: {
            ...stateBefore.substate.cost,
            capStatus: "hard_cap_blocked" as const,
          },
        },
      }
    : stateBefore;

  const decision = orchestrateAgentV2Turn({
    state: costBlockedState,
    interpretation,
    product,
  });
  const toolPlanGuardrail = validateToolPlan(decision);
  const toolResult = toolPlanGuardrail.ok
    ? await executeAgentV2Tools({ request, state: costBlockedState, decision, turnId })
    : { records: [], patch: {}, state: costBlockedState };

  let response =
    shouldAgentV2ReplyAutomatically()
      ? generateAgentV2Response({ request, state: toolResult.state, interpretation, decision, product })
      : null;

  if (!response && isAgentV2CaptureOnly()) {
    response = config.enableLegacyFallback ? await legacyTurn(request) : noReplyResponse();
  }

  if (!response) {
    response = generateAgentV2Response({
      request,
      state: toolResult.state,
      interpretation,
      decision: {
        ...decision,
        selectedAction: "legacy_fallback",
        responseObjective: "Responder com fallback seguro do v2 sem acionar o agente legado.",
      },
      product,
    });
  }

  if (!response) {
    throw new Error("Agent v2 failed to generate a response");
  }

  const widgetMapped = request.session.channel === "web" ? attachWidgetActions(response, product) : response;
  const guardrail = validateAgentV2Response({ request, response: widgetMapped, decision });
  const validatedResponse = guardrail.response;
  const responseText = validatedResponse.assistantMessages.map((message) => message.content).join("\n\n");
  const usage = estimateTurnUsage({
    input: normalizedInput.text ?? "",
    output: responseText,
    category: decision.costBudgetCategory,
    operation: decision.selectedAction === "legacy_fallback" ? "recovery" : "generation",
    model: decision.modelClass === "stronger" ? config.strongerModel : config.defaultModel,
    escalationReason: decision.escalationReason,
  });
  const costAfter = Number((toolResult.state.substate.cost.estimatedConversationCostUsd + projectedUsage.estimatedCostUsd + usage.estimatedCostUsd).toFixed(6));
  const responsePatch = validatedResponse.qualificationPatch ?? {};
  const askedQuestions = responsePatch.diagnosticAskedFields
    ? parseCsv(responsePatch.diagnosticAskedFields)
    : toolResult.state.substate.askedQuestions;
  const isDiagnosticInProgress = responsePatch.diagnosticStatus === "in_progress" || decision.selectedAction === "continue_diagnostic";
  const isDiagnosticFinished = responsePatch.diagnosticStatus === "completed" || decision.selectedAction === "deliver_diagnostic";
  const missingFields =
    typeof responsePatch.missingWaitlistFields === "string"
      ? parseCsv(responsePatch.missingWaitlistFields)
      : decision.selectedAction === "collect_waitlist_details"
        ? toolResult.state.substate.missingFields
        : decision.stateTransition === "waitlist_joined"
          ? []
          : toolResult.state.substate.missingFields;
  const finalMacroState =
    responsePatch.waitlistStatus === "joined"
      ? "waitlist_joined"
      : responsePatch.waitlistStatus === "pending_details"
        ? "waitlist_pending_details"
        : decision.stateTransition;
  const stateAfter: AgentV2ConversationState = {
    ...toolResult.state,
    macroState: finalMacroState,
    productSourceVersion: product.version,
    substate: {
      ...toolResult.state.substate,
      knownFacts: mergeTurnFacts(toolResult.state.substate.knownFacts, interpretation.factsExtracted, request.userMessage),
      askedQuestions,
      diagnosticStep: isDiagnosticFinished ? null : isDiagnosticInProgress ? (askedQuestions.at(-1) ?? toolResult.state.substate.diagnosticStep) : toolResult.state.substate.diagnosticStep,
      pendingQuestion: validatedResponse.nextQuestion ?? null,
      missingFields,
      lastAnsweredDirectQuestion: interpretation.directQuestions[0] ?? toolResult.state.substate.lastAnsweredDirectQuestion,
      sentiment: interpretation.sentiment,
      confidence: interpretation.confidence,
      cost: {
        estimatedConversationCostUsd: costAfter,
        capStatus: getCostCapStatus(costAfter),
      },
    },
    updatedAt: new Date().toISOString(),
  };
  await saveAgentV2State(stateAfter);

  const deliveryResult =
    normalizedInput.channel === "whatsapp"
      ? { chunks: planWhatsAppChunks(validatedResponse.assistantMessages.map((message) => message.content)) }
      : buildChannelDeliveryPlan(validatedResponse.assistantMessages.map((message) => message.content), stateAfter);

  await recordAgentV2Trace({
    id: traceId,
    leadId: request.session.leadId,
    conversationId: normalizedInput.conversationId,
    turnId,
    channel: request.session.channel,
    normalizedInput,
    stateBefore,
    productSourceVersion: product.version,
    semanticInterpretation: interpretation,
    orchestrationDecision: decision,
    toolActions: toolResult.records,
    guardrailResult: {
      status: guardrail.status,
      reasons: [...guardrail.reasons, ...toolPlanGuardrail.reasons],
    },
    responseDraft: response,
    validatedResponse,
    stateAfter,
    deliveryResult,
    modelUsage: [projectedUsage, usage],
    costEstimateUsd: costAfter,
    fallbackReason: decision.selectedAction === "legacy_fallback" ? "legacy_fallback" : undefined,
    createdAt: new Date().toISOString(),
  });

  await completeAgentV2IdempotencyKey(idempotencyKey, "processed");

  return {
    ...validatedResponse,
    qualificationPatch: {
      ...toolResult.patch,
      ...validatedResponse.qualificationPatch,
      agentV2State: serializeV2State(stateAfter),
      agentV2TraceId: traceId,
      agentV2CostEstimateUsd: String(costAfter),
      agentV2ProductSourceVersion: product.version,
      agentV2Priority: stateAfter.priority,
    },
  };
}

function parseCsv(value?: string) {
  return value ? value.split(",").map((item) => item.trim()).filter(Boolean) : [];
}

function mergeTurnFacts(
  knownFacts: AgentV2ConversationState["substate"]["knownFacts"],
  incomingFacts: Partial<AgentV2ConversationState["substate"]["knownFacts"]>,
  userMessage?: string,
) {
  const nextFacts = {
    ...knownFacts,
    ...incomingFacts,
  };
  if (knownFacts.mainPainOrIntent && incomingFacts.mainPainOrIntent) {
    nextFacts.mainPainOrIntent = knownFacts.mainPainOrIntent;
    if (!nextFacts.priorityToMakeLighter && /\b(aliviar|leve|primeiro|prioridade|complicado|resolver)\b/i.test(userMessage ?? "")) {
      nextFacts.priorityToMakeLighter = incomingFacts.mainPainOrIntent;
    }
  }
  return nextFacts;
}

function noReplyResponse(): AiAttendantResponse {
  return {
    assistantMessages: [],
    capturedPainIds: [],
    recommendedAgentIds: [],
    shouldOfferDiagnostic: false,
    guardrailDecision: {
      category: "allowed",
      action: "fallback",
      reason: "Agent v2 capture-only/kill-switch mode; no automatic reply sent.",
    },
  };
}
