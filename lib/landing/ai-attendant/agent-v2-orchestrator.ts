import type { AgentV2ConversationState, AgentV2Interpretation, AgentV2OrchestrationDecision } from "./agent-v2-types";
import type { ProductKnowledge } from "./product-knowledge-source";
import { hasEnoughForDiagnostic, nextDiagnosticQuestion } from "./agent-v2-diagnostic";

export function orchestrateAgentV2Turn({
  state,
  interpretation,
  product,
}: {
  state: AgentV2ConversationState;
  interpretation: AgentV2Interpretation;
  product: ProductKnowledge;
}): AgentV2OrchestrationDecision {
  if (state.humanStatus === "active" || state.macroState === "human_active") {
    return decision("pause_no_reply", "human_active", "IA pausada por humano.", [], "simple_answer");
  }

  if (state.substate.cost.capStatus === "hard_cap_blocked") {
    return decision("cost_cap_fallback", state.macroState, "Limite de custo atingido; preservar contexto e chamar humano.", [
      { toolName: "recordCostCap", payload: { reason: "hard_cap_blocked" } },
    ], "simple_answer");
  }

  if (interpretation.primaryIntent === "prompt_injection" || interpretation.primaryIntent === "abuse") {
    return decision("safe_refusal", state.macroState, "Recusar risco e voltar ao contexto da Taliya.", [], "simple_answer");
  }

  if (interpretation.primaryIntent === "media") {
    return decision("unsupported_media", state.macroState, "Pedir resumo em texto ou oferecer humano.", [
      { toolName: "recordMedia", payload: { riskFlags: interpretation.riskFlags } },
    ], "simple_answer");
  }

  if (interpretation.primaryIntent === "human_request" || interpretation.directQuestions.includes("human")) {
    return decision("handoff_human", "human_requested", "Confirmar handoff e pausar IA.", [
      { toolName: "pauseForHuman", payload: { reason: "lead_requested_human" } },
    ], "medium_qualified_lead");
  }

  if (state.macroState === "waitlist_joined") {
    return decision("answer_post_waitlist", "waitlist_joined", "Responder duvida preservando lista de espera.", [
      { toolName: "updateLeadFacts", payload: { facts: interpretation.factsExtracted } },
    ], "simple_answer");
  }

  if (state.macroState === "waitlist_pending_details") {
    return decision("collect_waitlist_details", "waitlist_pending_details", "Coletar dados faltantes da lista sem reiniciar fluxo.", [
      { toolName: "markWaitlist", payload: { status: "pending_details", facts: interpretation.factsExtracted } },
    ], "medium_qualified_lead");
  }

  if (state.macroState === "waitlist_offered") {
    if (interpretation.primaryIntent === "waitlist_decline") {
      return decision("answer_direct", "open_question", "Responder sem insistir na lista.", [
        { toolName: "markWaitlist", payload: { status: "declined" } },
      ], "simple_answer");
    }
    if (interpretation.primaryIntent === "waitlist_accept") {
      return decision("collect_waitlist_details", "waitlist_pending_details", "Registrar aceite e pedir dados faltantes.", [
        { toolName: "markWaitlist", payload: { status: "pending_details", facts: interpretation.factsExtracted } },
      ], "medium_qualified_lead");
    }
    if (hasWaitlistDetails(interpretation)) {
      return decision("collect_waitlist_details", "waitlist_pending_details", "Tratar dados enviados como aceite da lista e registrar.", [
        { toolName: "markWaitlist", payload: { status: "pending_details", facts: interpretation.factsExtracted } },
      ], "medium_qualified_lead");
    }
  }

  if (interpretation.directQuestions.length && !onlyBuyingIntent(interpretation)) {
    return decision("answer_direct", directState(interpretation), "Responder pergunta direta antes de qualquer steering.", [
      { toolName: "getProductKnowledge", payload: { version: product.version } },
      { toolName: "updateLeadFacts", payload: { facts: interpretation.factsExtracted } },
    ], interpretation.directQuestions.length > 1 ? "long_complex_lead" : "simple_answer", interpretation.needsEscalation, interpretation.escalationReason);
  }

  if (interpretation.primaryIntent === "buying_intent" || interpretation.directQuestions.includes("buy")) {
    return decision("offer_waitlist", "waitlist_offered", "Alta intencao: substituir checkout por lista de espera aprovada.", [
      { toolName: "markWaitlist", payload: { status: "offered" } },
    ], "medium_qualified_lead");
  }

  if (interpretation.primaryIntent === "greeting") {
    return decision("opening", "open_question", "Abertura natural sem capturar nome/telefone.", [
      { toolName: "updateLeadFacts", payload: { facts: interpretation.factsExtracted } },
    ], "simple_answer");
  }

  if (interpretation.primaryIntent === "diagnostic_accept") {
    return decision("continue_diagnostic", "diagnostic_in_progress", "Iniciar diagnostico com proxima pergunta necessaria.", [
      { toolName: "updateLeadFacts", payload: { facts: interpretation.factsExtracted } },
    ], "diagnostic_lead");
  }

  if (state.macroState === "diagnostic_in_progress" || interpretation.primaryIntent === "diagnostic_answer") {
    const facts = { ...state.substate.knownFacts, ...interpretation.factsExtracted };
    if (hasEnoughForDiagnostic(facts)) {
      return decision("deliver_diagnostic", "diagnostic_completed", "Entregar diagnostico especifico com evidencia e validacao.", [
        { toolName: "saveDiagnostic", payload: { facts } },
      ], "diagnostic_lead");
    }
    const next = nextDiagnosticQuestion({ ...state.substate, knownFacts: facts });
    return decision("continue_diagnostic", "diagnostic_in_progress", next?.question ?? "Completar diagnostico com uma pergunta util.", [
      { toolName: "updateLeadFacts", payload: { facts: interpretation.factsExtracted } },
    ], "diagnostic_lead");
  }

  if (state.macroState === "diagnostic_completed" && interpretation.primaryIntent !== "diagnostic_decline") {
    if (interpretation.primaryIntent === "waitlist_accept") {
      if (hasWaitlistDetails(interpretation)) {
        return decision("collect_waitlist_details", "waitlist_pending_details", "Lead enviou dados da lista depois do diagnostico; registrar.", [
          { toolName: "markWaitlist", payload: { status: "pending_details", facts: interpretation.factsExtracted } },
        ], "medium_qualified_lead");
      }
      return decision("offer_waitlist", "waitlist_offered", "Depois de validacao positiva, explicar lista antes de pedir dados.", [
        { toolName: "markWaitlist", payload: { status: "offered", facts: interpretation.factsExtracted } },
      ], "medium_qualified_lead");
    }
    return decision("offer_waitlist", "waitlist_offered", "Depois de validacao positiva, oferecer lista de espera.", [
      { toolName: "markWaitlist", payload: { status: "offered" } },
    ], "medium_qualified_lead");
  }

  if (interpretation.factsExtracted.personName && (state.macroState === "open_question" || state.macroState === "new_lead")) {
    return decision("capture_name", "open_question", "Capturar nome informado espontaneamente e continuar aberto.", [
      { toolName: "updateLeadFacts", payload: { facts: interpretation.factsExtracted } },
    ], "simple_answer");
  }

  if (interpretation.primaryIntent === "pain_or_fit" || interpretation.factsExtracted.mainPainOrIntent) {
    return decision("offer_diagnostic", "diagnostic_offered", "Oferecer diagnostico como mini-consultoria.", [
      { toolName: "updateLeadFacts", payload: { facts: interpretation.factsExtracted } },
    ], "medium_qualified_lead");
  }

  return decision("legacy_fallback", state.macroState, "Sem rota v2 confiante; usar legado com trace.", [
    { toolName: "updateLeadFacts", payload: { facts: interpretation.factsExtracted } },
  ], "simple_answer");
}

function decision(
  selectedAction: AgentV2OrchestrationDecision["selectedAction"],
  stateTransition: AgentV2OrchestrationDecision["stateTransition"],
  responseObjective: string,
  toolActions: AgentV2OrchestrationDecision["toolActions"],
  costBudgetCategory: AgentV2OrchestrationDecision["costBudgetCategory"],
  needsEscalation = false,
  escalationReason?: string,
): AgentV2OrchestrationDecision {
  return {
    selectedAction,
    stateTransition,
    responseObjective,
    toolActions,
    modelClass: needsEscalation ? "stronger" : "default",
    escalationReason,
    costBudgetCategory,
  };
}

function directState(interpretation: AgentV2Interpretation) {
  if (interpretation.directQuestions.includes("price") || interpretation.directQuestions.includes("plans") || interpretation.directQuestions.includes("plan_recommendation")) return "price_or_plan" as const;
  if (interpretation.directQuestions.includes("demo")) return "demo_interest" as const;
  return "product_question" as const;
}

function onlyBuyingIntent(interpretation: AgentV2Interpretation) {
  return interpretation.directQuestions.length === 1 && interpretation.directQuestions[0] === "buy";
}

function hasWaitlistDetails(interpretation: AgentV2Interpretation) {
  return Boolean(interpretation.factsExtracted.studioName || interpretation.factsExtracted.cityState || interpretation.factsExtracted.email || interpretation.factsExtracted.whatsappPhone);
}
