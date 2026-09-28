import type { AiAttendantRequest, QualificationDraft } from "./schema";
import type { AgentV2ConversationState, AgentV2OrchestrationDecision, AgentV2ToolRecord } from "./agent-v2-types";
import { createToolIdempotencyKey } from "./agent-v2-idempotency";
import { saveAgentV2State } from "./agent-v2-state-store";

export async function executeAgentV2Tools({
  request,
  state,
  decision,
  turnId,
}: {
  request: AiAttendantRequest;
  state: AgentV2ConversationState;
  decision: AgentV2OrchestrationDecision;
  turnId: string;
}) {
  const records: AgentV2ToolRecord[] = [];
  let patch: QualificationDraft = {};
  let nextState = { ...state, macroState: decision.stateTransition, updatedAt: new Date().toISOString() };

  for (const action of decision.toolActions) {
    const idempotencyKey = createToolIdempotencyKey({
      conversationId: state.conversationId,
      turnId,
      toolName: action.toolName,
    });

    try {
      const result = applyTool(action.toolName, action.payload, request, nextState);
      patch = { ...patch, ...result.patch };
      nextState = result.state;
      records.push({ toolName: action.toolName, idempotencyKey, status: "succeeded", output: result.output });
    } catch (error) {
      records.push({
        toolName: action.toolName,
        idempotencyKey,
        status: "failed",
        failureReason: error instanceof Error ? error.message : "tool_failed",
      });
    }
  }

  await saveAgentV2State(nextState);
  return { records, patch, state: nextState };
}

function applyTool(
  toolName: string,
  payload: Record<string, unknown>,
  request: AiAttendantRequest,
  state: AgentV2ConversationState,
): {
  state: AgentV2ConversationState;
  patch: QualificationDraft;
  output: Record<string, unknown>;
} {
  if (toolName === "updateLeadFacts") {
    const facts = isRecord(payload.facts) ? payload.facts : {};
    const nextFacts = mergeToolFacts(state.substate.knownFacts, facts, request.userMessage);
    return {
      state: {
        ...state,
        substate: {
          ...state.substate,
          knownFacts: nextFacts,
          lastTopic: typeof nextFacts.mainPainOrIntent === "string" ? nextFacts.mainPainOrIntent : state.substate.lastTopic,
        },
      },
      patch: qualificationPatchFromFacts(nextFacts, request),
      output: { updatedFactKeys: Object.keys(facts) },
    };
  }

  if (toolName === "markWaitlist") {
    const status = typeof payload.status === "string" ? payload.status : "offered";
    return {
      state: {
        ...state,
        macroState: status === "pending_details" ? "waitlist_pending_details" : status === "joined" ? "waitlist_joined" : "waitlist_offered",
        priority: "waitlist_ready",
      },
      patch: {
        waitlistStatus: status === "pending_details" ? "pending_details" : status === "joined" ? "joined" : status === "declined" ? "declined" : "offered",
        waitlistOfferedAt: status === "offered" ? new Date().toISOString() : request.session.qualificationDraft?.waitlistOfferedAt,
        waitlistJoinedAt: status === "joined" ? new Date().toISOString() : request.session.qualificationDraft?.waitlistJoinedAt,
      },
      output: { waitlistStatus: status },
    };
  }

  if (toolName === "pauseForHuman") {
    return {
      state: {
        ...state,
        macroState: "human_active",
        humanStatus: "active",
        priority: "human_needed",
        substate: {
          ...state.substate,
          queuedResponseStatus: "suppressed",
        },
      },
      patch: {
        humanActive: "requested",
        aiPaused: "true",
        closureState: "human_active",
      },
      output: { paused: true },
    };
  }

  if (toolName === "recordCostCap") {
    return {
      state: {
        ...state,
        humanStatus: "requested",
        priority: "human_needed",
        substate: {
          ...state.substate,
          queuedResponseStatus: "suppressed",
          cost: {
            ...state.substate.cost,
            capStatus: "hard_cap_blocked",
          },
        },
      },
      patch: {
        aiPaused: "true",
        humanActive: "requested",
        closureState: "error_needs_attention",
      },
      output: { capStatus: "hard_cap_blocked" },
    };
  }

  if (toolName === "saveDiagnostic") {
    return {
      state: {
        ...state,
        macroState: "diagnostic_completed",
      },
      patch: {
        diagnosticStatus: "completed",
        diagnosticCompleted: "true",
        diagnosticCompletedAt: new Date().toISOString(),
      },
      output: { saved: true },
    };
  }

  return { state, patch: {}, output: { skipped: true } };
}

function mergeToolFacts(
  knownFacts: AgentV2ConversationState["substate"]["knownFacts"],
  incomingFacts: Record<string, unknown>,
  userMessage?: string,
) {
  const nextFacts = {
    ...knownFacts,
    ...incomingFacts,
  };
  const incomingPain = typeof incomingFacts.mainPainOrIntent === "string" ? incomingFacts.mainPainOrIntent : undefined;
  if (knownFacts.mainPainOrIntent && incomingPain) {
    nextFacts.mainPainOrIntent = knownFacts.mainPainOrIntent;
    if (!nextFacts.priorityToMakeLighter && /\b(aliviar|leve|primeiro|prioridade|complicado|resolver)\b/i.test(userMessage ?? "")) {
      nextFacts.priorityToMakeLighter = incomingPain;
    }
  }
  return nextFacts;
}

function qualificationPatchFromFacts(facts: Record<string, unknown>, request: AiAttendantRequest): QualificationDraft {
  return {
    name: asString(facts.personName) ?? request.session.qualificationDraft?.name,
    whatsapp: request.session.externalContact?.phone ?? asString(facts.whatsappPhone),
    email: asString(facts.email),
    studioName: asString(facts.studioName),
    cityState: asString(facts.cityState),
    studioCity: asString(facts.cityState),
    studioSizeRange: asString(facts.activeStudents),
    activeStudentsRange: asString(facts.activeStudents),
    primaryPainOrIntent: asString(facts.mainPainOrIntent),
    biggestPain: asString(facts.mainPainOrIntent),
    currentSystem: asString(facts.currentWorkflowOrTool),
    priorityGoal: asString(facts.priorityToMakeLighter),
    buyingTiming: asString(facts.urgency),
  };
}

function asString(value: unknown) {
  return typeof value === "string" && value.trim() ? value.trim() : undefined;
}

function isRecord(input: unknown): input is Record<string, unknown> {
  return typeof input === "object" && input !== null;
}
