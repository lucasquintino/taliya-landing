import type { NicheLandingConfig, PricingPlan } from "@/data/landing/niches/types";
import type { AiAttendantRequest, AiAttendantResponse } from "./schema";
import { createAssistantMessage } from "./schema";

export function buildPlanPriceSummary(config: NicheLandingConfig) {
  return config.subscription.plans.map((plan) => `${plan.name}: ${plan.monthlyPriceLabel}`).join("; ");
}

export function buildPlanComparisonSummary(config: NicheLandingConfig) {
  return config.subscription.plans.map(planComparisonLine).join(" ");
}

export function createPricePlanAnswer({
  config,
  request,
  reason = "price_or_plan",
}: {
  config: NicheLandingConfig;
  request: AiAttendantRequest;
  reason?: string;
}): AiAttendantResponse {
  const hasDiagnostic = request.session.qualificationDraft?.diagnosticCompleted === "true";
  const asksRecommendation = isPlanRecommendationRequest(request);
  const asksDirectComparison = isDirectPlanComparisonRequest(request);
  const planSummary = buildPlanPriceSummary(config);
  const comparison = buildPlanComparisonSummary(config);
  const isFirstMessage = !request.session.messages.some((message) => message.role === "user" || message.role === "assistant");
  const greeting = firstMessageGreeting(request);
  const nextQuestion = hasDiagnostic
    ? "Quer que eu abra o comparativo de planos?"
    : "Quer que eu recomende um plano pelo diagnostico gratuito, ou prefere ver o comparativo direto?";
  const middleMessage =
    asksRecommendation && !hasDiagnostic
      ? "Eu nao vou cravar um plano sem entender seu studio, mas nao preciso esconder os valores para isso."
      : asksDirectComparison
        ? comparison
        : "A diferenca principal e a quantidade de rotinas que voce quer organizar com IA ativa.";
  const messages =
    isFirstMessage && greeting
      ? [greeting, `Hoje os planos sao: ${planSummary}. ${middleMessage}`, nextQuestion]
      : [`Hoje os planos sao: ${planSummary}.`, middleMessage, nextQuestion];

  return {
    assistantMessages: messages.map((message, index) =>
      createAssistantMessage(message, index === messages.length - 1 && (hasDiagnostic || asksDirectComparison) ? "view_plans" : "answer_question"),
    ),
    capturedPainIds: [],
    recommendedAgentIds: [],
    recommendations: undefined,
    nextQuestion,
    conversionPath: asksDirectComparison ? "view_plans" : undefined,
    subscription: asksDirectComparison
      ? {
          planId: config.subscription.recommendedPlanId,
          ctaLabel: config.floatingAgent.conversionCtas.viewPlans.label,
        }
      : undefined,
    shouldOfferDiagnostic: !hasDiagnostic,
    qualificationPatch: {
      commercialStage: hasDiagnostic ? "recommendation_validation" : "diagnostic_offered",
      diagnosticStatus: hasDiagnostic ? "completed" : "offered",
      waitlistStatus: request.session.qualificationDraft?.waitlistStatus ?? "not_offered",
      nextAction: hasDiagnostic
        ? "Responder planos e abrir comparativo se o lead quiser."
        : "Responder preco sem bloquear e oferecer diagnostico gratuito como opcao de recomendacao.",
    },
    guardrailDecision: {
      category: "allowed",
      action: "respond",
      reason,
    },
  };
}

function firstMessageGreeting(request: AiAttendantRequest) {
  const name = request.session.qualificationDraft?.name?.trim().split(/\s+/)[0];
  if (request.session.channel === "whatsapp" && name) return `Oi, ${name}. Tudo bem?`;
  if (request.session.channel === "whatsapp") return "Oi! Tudo bem?";
  if (request.session.channel === "web") return "Oi! Tudo bem?";
  return undefined;
}

export function isPriceOrPlanQuestion(request: AiAttendantRequest) {
  if (request.quickReplyId === "view_plans" || request.quickReplyId === "ask_price") return true;
  const text = normalizeText([request.userMessage, request.quickReplyId].filter(Boolean).join(" "));
  return (
    /\b(preco|precos|valor|valores|quanto custa|quanto e|quanto fica|mensalidade|assinatura)\b/.test(text) ||
    /\b(quais|qual|ver|mostrar|abrir|comparar|comparativo|saber|me fala|me mostra)\b.{0,50}\bplanos?\b/.test(text) ||
    /\bplanos?\b.{0,50}\b(custa|custam|valor|valores|preco|precos|comparar|comparativo)\b/.test(text)
  );
}

export function isDirectPlanComparisonRequest(request: AiAttendantRequest) {
  if (request.quickReplyId === "view_plans") return true;
  const text = normalizeText(request.userMessage ?? "");
  return /\b(ver|mostrar|abrir|comparar|comparativo)\b.{0,50}\bplanos?\b/.test(text);
}

function isPlanRecommendationRequest(request: AiAttendantRequest) {
  const text = normalizeText(request.userMessage ?? "");
  return /\b(qual plano|plano faz sentido|plano recomenda|recomenda.*plano|melhor plano|indica.*plano)\b/.test(text);
}

function planComparisonLine(plan: PricingPlan) {
  if (plan.id === "base") return `${plan.name} organiza a base, sem IA ativa no WhatsApp.`;
  if (plan.id === "one_agent") return `${plan.name} ativa 1 agente para uma dor principal.`;
  if (plan.id === "three_agents") return `${plan.name} ativa 3 agentes para rotinas prioritarias.`;
  if (plan.id === "seven_agents") return `${plan.name} cobre as 7 rotinas principais do studio.`;
  if (plan.includedAgents.length === 0) return `${plan.name} organiza a base, sem IA ativa no WhatsApp.`;
  return `${plan.name} segue a configuracao comercial atual da Taliya.`;
}

function normalizeText(value: string) {
  return value
    .toLowerCase()
    .normalize("NFD")
    .replace(/\p{Diacritic}/gu, "");
}
