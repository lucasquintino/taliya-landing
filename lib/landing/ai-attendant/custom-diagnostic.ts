import type { CampaignStage, NicheLandingConfig, PublicOfferMode } from "@/data/landing/niches/types";
import { classifyInputGuardrail } from "./guardrails";
import { getNicheConfig } from "./context";
import type { AiAttendantRequest, ConversionPath, DiagnosticClassification, DiagnosticContextVariant, GuardrailDecision } from "./schema";
import { logAiUsageEvent } from "./usage";

export type CustomAgentDiagnosticRequest = {
  sessionId: string;
  niche: string;
  sourcePage: string;
  sourceSection: "custom_agent_diagnostic" | "final_diagnostic_cta";
  campaignStage: CampaignStage;
  publicOfferMode: PublicOfferMode;
  description: string;
  pageSignals?: {
    selectedPainId?: string;
    selectedAgentId?: string;
    calculatorEstimate?: number;
  };
};

export type CustomAgentDiagnosticResponse = {
  reportId: string;
  classification: DiagnosticClassification;
  diagnosticContextVariant: DiagnosticContextVariant;
  confidence: "high" | "medium" | "low";
  title: string;
  sections: Array<{
    id: "request_summary" | "studio_impact" | "taliya_fit" | "recommended_path" | "next_step";
    title: string;
    body: string;
  }>;
  mappedAgentIds: string[];
  customAgent?: {
    label: string;
    operationSummary: string;
    missingScopeQuestions: string[];
  };
  recommendedPlanId?: string;
  ctas: Array<{
    id: "talk_to_consultor" | "guided_demo" | "continue_whatsapp" | "request_custom_agent_proposal";
    label: string;
    destination: "open_consultor" | "configured_guided_demo" | "configured_whatsapp";
    contextVariant: DiagnosticContextVariant;
  }>;
  leadEffect: {
    shouldCreateOrUpdateLead: boolean;
    conversionPath: ConversionPath;
    priority: "alta" | "media" | "baixa";
    safeSummary: string;
  };
  guardrailDecision: GuardrailDecision;
};

const MAX_DESCRIPTION_LENGTH = 1200;

const CUSTOM_KEYWORDS = [
  "marketing",
  "instagram",
  "campanha",
  "campanhas",
  "anuncio",
  "anuncios",
  "trafego",
  "conteudo",
  "parceria",
  "parcerias",
  "estoque",
  "rh",
  "professor",
  "professores",
  "contratacao",
  "contratacao",
  "fora dos agentes",
  "sob medida",
];

export function parseCustomAgentDiagnosticRequest(input: unknown):
  | { ok: true; value: CustomAgentDiagnosticRequest }
  | { ok: false; error: string } {
  if (!isRecord(input)) return { ok: false, error: "Request body must be an object." };

  const description = typeof input.description === "string" ? input.description.trim() : "";
  if (description.length < 3) return { ok: false, error: "Description is required." };
  if (description.length > MAX_DESCRIPTION_LENGTH) return { ok: false, error: "Description is too long." };
  if (typeof input.sessionId !== "string" || !input.sessionId) return { ok: false, error: "Invalid session id." };
  if (typeof input.niche !== "string" || !input.niche) return { ok: false, error: "Invalid niche." };
  if (typeof input.sourcePage !== "string" || !input.sourcePage) return { ok: false, error: "Invalid source page." };

  return {
    ok: true,
    value: {
      sessionId: input.sessionId,
      niche: input.niche,
      sourcePage: input.sourcePage,
      sourceSection: input.sourceSection === "final_diagnostic_cta" ? "final_diagnostic_cta" : "custom_agent_diagnostic",
      campaignStage: input.campaignStage === "commercial" ? "commercial" : "commercial",
      publicOfferMode: input.publicOfferMode === "direct_saas_subscription" ? "direct_saas_subscription" : "direct_saas_subscription",
      description,
      pageSignals: parsePageSignals(input.pageSignals),
    },
  };
}

export async function runCustomAgentDiagnostic(request: CustomAgentDiagnosticRequest): Promise<CustomAgentDiagnosticResponse> {
  const config = getNicheConfig(request.niche);
  const pseudoRequest = toPseudoAiRequest(request);
  const guardrailDecision = classifyInputGuardrail(pseudoRequest);

  if (guardrailDecision.category !== "allowed") {
    await logAiUsageEvent({
      sessionId: request.sessionId,
      channel: "web",
      niche: config.niche,
      provider: "internal",
      status: "guardrail_blocked",
      fallbackOrGuardrailCategory: guardrailDecision.category,
    });
    return createGuardrailDiagnostic(request, config, guardrailDecision);
  }

  await logAiUsageEvent({
    sessionId: request.sessionId,
    channel: "web",
    niche: config.niche,
    provider: "internal",
    status: "success",
  });

  return createDeterministicDiagnostic(request, config, guardrailDecision);
}

export function toPseudoAiRequest(request: CustomAgentDiagnosticRequest): AiAttendantRequest {
  return {
    session: {
      sessionId: request.sessionId,
      channel: "web",
      entryPath: "custom_agent_diagnostic",
      sourceSection: request.sourceSection,
      niche: request.niche,
      sourcePage: request.sourcePage,
      campaignStage: request.campaignStage,
      publicOfferMode: request.publicOfferMode,
      messages: [
        {
          id: "diagnostic_user_description",
          role: "user",
          content: request.description,
          intent: "custom_agent_diagnostic_request",
        },
      ],
    },
    userMessage: request.description,
    pageSignals: request.pageSignals,
  };
}

function createDeterministicDiagnostic(
  request: CustomAgentDiagnosticRequest,
  config: NicheLandingConfig,
  guardrailDecision: GuardrailDecision,
): CustomAgentDiagnosticResponse {
  const reportId = createReportId(request);
  const mappedAgentIds = findMappedAgents(request.description, config);
  const hasCustomSignal = CUSTOM_KEYWORDS.some((keyword) => normalized(request.description).includes(normalized(keyword)));
  const classification = classifyDiagnostic(request.description, mappedAgentIds, hasCustomSignal);
  const contextVariant = contextVariantFor(classification);
  const customOperation = hasCustomSignal ? summarizeCustomOperation(request.description) : undefined;
  const recommendedPlanId = classification === "custom_agent" || classification === "unclear" ? undefined : config.subscription.recommendedPlanId;
  const safeSummary = buildSafeSummary(classification, mappedAgentIds, customOperation);

  return {
    reportId,
    classification,
    diagnosticContextVariant: contextVariant,
    confidence: classification === "unclear" ? "low" : mappedAgentIds.length || hasCustomSignal ? "high" : "medium",
    title: titleFor(classification),
    sections: buildSections({
      classification,
      config,
      customOperation,
      description: request.description,
      mappedAgentIds,
      recommendedPlanId,
    }),
    mappedAgentIds,
    customAgent:
      classification === "custom_agent" || classification === "mixed_solution"
        ? {
            label: customOperation?.label ?? "Agente sob medida",
            operationSummary: customOperation?.summary ?? "Operação fora do time principal da Taliya.",
            missingScopeQuestions: [
              "O agente deve apenas sugerir ações ou também executar alguma etapa?",
              "Em quais canais ou ferramentas essa rotina acontece hoje?",
              "Quem aprova as ações antes de irem para alunos, equipe ou parceiros?",
            ],
          }
        : undefined,
    recommendedPlanId,
    ctas: ctasFor(classification, contextVariant, config),
    leadEffect: {
      shouldCreateOrUpdateLead: classification !== "unclear",
      conversionPath: conversionPathFor(classification),
      priority: classification === "mixed_solution" ? "alta" : classification === "unclear" ? "baixa" : "media",
      safeSummary,
    },
    guardrailDecision,
  };
}

function createGuardrailDiagnostic(
  request: CustomAgentDiagnosticRequest,
  config: NicheLandingConfig,
  guardrailDecision: GuardrailDecision,
): CustomAgentDiagnosticResponse {
  return {
    reportId: createReportId(request),
    classification: "unclear",
    diagnosticContextVariant: "diagnostic_unclear",
    confidence: "low",
    title: "Não consegui gerar esse diagnóstico",
    sections: [
      {
        id: "request_summary",
        title: "O que aconteceu",
        body: guardrailDecision.visibleMessage ?? "Não preciso de dados sensíveis para orientar seu studio. Descreva a rotina de forma geral.",
      },
      {
        id: "next_step",
        title: "Próximo passo",
        body: "Explique a operação sem dados de pagamento, prontuários ou informações privadas de alunos.",
      },
    ],
    mappedAgentIds: [],
    ctas: ctasFor("unclear", "diagnostic_unclear", config),
    leadEffect: {
      shouldCreateOrUpdateLead: false,
      conversionPath: "custom_agent_diagnostic_unclear",
      priority: "baixa",
      safeSummary: "Diagnostic blocked by guardrail.",
    },
    guardrailDecision,
  };
}

function classifyDiagnostic(description: string, mappedAgentIds: string[], hasCustomSignal: boolean): DiagnosticClassification {
  if (hasCustomSignal && mappedAgentIds.length) return "mixed_solution";
  if (hasCustomSignal) return "custom_agent";
  if (mappedAgentIds.length) return "mapped_solution";
  if (normalized(description).split(/\s+/).length < 4) return "unclear";
  return "unclear";
}

function findMappedAgents(description: string, config: NicheLandingConfig) {
  const text = normalized(description);
  const agentIds = new Set<string>();

  for (const pain of config.floatingAgent.painOptions) {
    const matchesPain = pain.keywords.some((keyword) => text.includes(normalized(keyword)));
    if (!matchesPain || pain.id === "agente_sob_medida") continue;
    const mapping = config.floatingAgent.painToAgents.find((item) => item.painId === pain.id);
    mapping?.agentIds.forEach((agentId) => agentIds.add(agentId));
  }

  if (/whatsapp|mensagem|atendimento|duvida/.test(text)) agentIds.add("atendimento");
  if (/agenda|reposi|horario|turma|vaga/.test(text)) agentIds.add("agenda");
  if (/venda|lead|interessad|experimental|assinar/.test(text)) agentIds.add("vendas");
  if (/mensalidade|cobranc|financeiro|pagamento|pix/.test(text)) agentIds.add("financeiro");
  if (/inativo|falt|retenc|renova/.test(text)) agentIds.add("retencao");
  if (/gestao|prioridade|relatorio|indicador|dinheiro/.test(text)) agentIds.add("gestao");
  if (/historico|evolu|restri|observacao|ficha/.test(text)) agentIds.add("historico-evolucao");

  return Array.from(agentIds);
}

function buildSections({
  classification,
  config,
  customOperation,
  description,
  mappedAgentIds,
  recommendedPlanId,
}: {
  classification: DiagnosticClassification;
  config: NicheLandingConfig;
  customOperation?: { label: string; summary: string };
  description: string;
  mappedAgentIds: string[];
  recommendedPlanId?: string;
}): CustomAgentDiagnosticResponse["sections"] {
  const agentNames = mappedAgentIds.length ? mappedAgentIds.map((agentId) => agentName(agentId, config)).join(", ") : "nenhum agente principal";
  const plan = config.subscription.plans.find((item) => item.id === recommendedPlanId);

  if (classification === "custom_agent") {
    return [
      { id: "request_summary", title: "O que você quer automatizar", body: customOperation?.summary ?? safeSlice(description, 220) },
      {
        id: "taliya_fit",
        title: "Isso entra nos planos atuais?",
        body: "Esse pedido parece ficar fora do time principal da Taliya. Portanto entra como Agente sob medida, separado dos planos públicos.",
      },
      {
        id: "recommended_path",
        title: "Caminho recomendado",
        body: "O melhor próximo passo é mapear escopo, canais, aprovações e contato para preparar uma proposta sob medida.",
      },
    ];
  }

  if (classification === "mixed_solution") {
    return [
      { id: "request_summary", title: "O que você descreveu", body: safeSlice(description, 260) },
      {
        id: "taliya_fit",
        title: "Parte já coberta pela Taliya",
        body: `A parte operacional já conversa com ${agentNames}. A parte de ${customOperation?.label ?? "agente sob medida"} precisa ser tratada como proposta separada.`,
      },
      {
        id: "recommended_path",
        title: "Caminho recomendado",
        body: `Eu começaria pelo caminho Taliya com ${plan?.name ?? "o plano recomendado"} e mapearia a expansão sob medida em paralelo.`,
      },
    ];
  }

  if (classification === "mapped_solution") {
    return [
      { id: "request_summary", title: "O que você quer resolver", body: safeSlice(description, 240) },
      {
        id: "taliya_fit",
        title: "Isso já está no mapa da Taliya",
        body: `Esse pedido já é atendido pelo caminho dos agentes ${agentNames}. Não precisa virar agente sob medida como primeira opção.`,
      },
      {
        id: "recommended_path",
        title: "Caminho recomendado",
        body: `O próximo passo é conversar com o consultor, ver a demo guiada quando disponível e chegar no plano certo. Para operação completa, a referência comercial é ${plan?.name ?? "o plano recomendado"}.`,
      },
    ];
  }

  return [
    { id: "request_summary", title: "Ainda falta contexto", body: "A descrição está ampla demais para separar com segurança entre plano atual e agente sob medida." },
    {
      id: "next_step",
      title: "O que explicar agora",
      body: "Diga qual rotina você quer automatizar, em qual canal ela acontece e qual resultado espera no dia a dia do studio.",
    },
  ];
}

function ctasFor(
  classification: DiagnosticClassification,
  contextVariant: DiagnosticContextVariant,
  config: NicheLandingConfig,
): CustomAgentDiagnosticResponse["ctas"] {
  if (classification === "custom_agent") {
    return [
      { id: "request_custom_agent_proposal", label: "Solicitar proposta de agente sob medida", destination: "open_consultor", contextVariant },
      { id: "continue_whatsapp", label: "Continuar pelo WhatsApp", destination: "configured_whatsapp", contextVariant },
    ];
  }

  const base: CustomAgentDiagnosticResponse["ctas"] = [
    { id: "talk_to_consultor", label: "Falar com consultor", destination: "open_consultor", contextVariant },
  ];
  if (classification !== "unclear" && config.floatingAgent.guidedDemoReady) {
    base.push({ id: "guided_demo", label: "Demo guiada", destination: "configured_guided_demo", contextVariant });
  }
  if (classification === "mixed_solution") {
    base.push({ id: "request_custom_agent_proposal", label: "Solicitar proposta de agente sob medida", destination: "open_consultor", contextVariant });
  }
  base.push({ id: "continue_whatsapp", label: "Continuar pelo WhatsApp", destination: "configured_whatsapp", contextVariant });
  return base;
}

function contextVariantFor(classification: DiagnosticClassification): DiagnosticContextVariant {
  if (classification === "custom_agent") return "diagnostic_custom_agent";
  if (classification === "mixed_solution") return "diagnostic_mixed_solution";
  if (classification === "unclear") return "diagnostic_unclear";
  return "diagnostic_existing_solution";
}

function conversionPathFor(classification: DiagnosticClassification): ConversionPath {
  if (classification === "custom_agent") return "custom_agent_follow_up";
  if (classification === "mixed_solution") return "mixed_subscription_plus_custom";
  if (classification === "unclear") return "custom_agent_diagnostic_unclear";
  return "custom_agent_diagnostic_mapped";
}

function titleFor(classification: DiagnosticClassification) {
  if (classification === "custom_agent") return "Diagnóstico: proposta de agente sob medida";
  if (classification === "mixed_solution") return "Diagnóstico: plano Taliya + agente sob medida";
  if (classification === "unclear") return "Diagnóstico: preciso de mais detalhes";
  return "Diagnóstico: Taliya já cobre esse caminho";
}

function summarizeCustomOperation(description: string) {
  const text = normalized(description);
  if (/marketing|instagram|campanha|anuncio|trafego|conteudo/.test(text)) {
    return { label: "Agente de Marketing", summary: "Operação de marketing, campanhas, conteúdo ou comunicação fora do time principal da Taliya." };
  }
  if (/parceria/.test(text)) return { label: "Agente de Parcerias", summary: "Operação de parcerias e relacionamento externo do studio." };
  if (/estoque/.test(text)) return { label: "Agente de Estoque", summary: "Operação de estoque ou controle interno fora do escopo principal." };
  if (/rh|professor|contratacao/.test(text)) return { label: "Agente de RH", summary: "Operação interna de equipe, professores ou contratações." };
  return { label: "Agente sob medida", summary: safeSlice(description, 260) };
}

function buildSafeSummary(classification: DiagnosticClassification, mappedAgentIds: string[], customOperation?: { label: string; summary: string }) {
  if (classification === "custom_agent") return `Pedido classificado como Agente sob medida: ${customOperation?.label ?? "operação personalizada"}.`;
  if (classification === "mixed_solution") return `Pedido misto: Taliya cobre ${mappedAgentIds.join(", ")} e há interesse em ${customOperation?.label ?? "agente sob medida"}.`;
  if (classification === "mapped_solution") return `Pedido já coberto por Taliya com agentes ${mappedAgentIds.join(", ")}.`;
  return "Pedido ainda vago; precisa de contexto antes de recomendar.";
}

function agentName(agentId: string, config: NicheLandingConfig) {
  return config.agents.find((agent) => agent.id === agentId)?.name ?? agentId;
}

function createReportId(request: CustomAgentDiagnosticRequest) {
  return `diag_${Math.abs(hashString(`${request.sessionId}:${request.description.slice(0, 120)}`)).toString(36)}`;
}

function safeSlice(value: string, maxLength: number) {
  return value.replace(/\s+/g, " ").trim().slice(0, maxLength);
}

function normalized(value: string) {
  return value
    .toLowerCase()
    .normalize("NFD")
    .replace(/[\u0300-\u036f]/g, "");
}

function parsePageSignals(input: unknown): CustomAgentDiagnosticRequest["pageSignals"] {
  if (!isRecord(input)) return undefined;
  return {
    selectedPainId: typeof input.selectedPainId === "string" ? input.selectedPainId : undefined,
    selectedAgentId: typeof input.selectedAgentId === "string" ? input.selectedAgentId : undefined,
    calculatorEstimate: typeof input.calculatorEstimate === "number" ? input.calculatorEstimate : undefined,
  };
}

function isRecord(input: unknown): input is Record<string, unknown> {
  return typeof input === "object" && input !== null;
}

function hashString(value: string) {
  let hash = 0;
  for (let index = 0; index < value.length; index += 1) {
    hash = (hash << 5) - hash + value.charCodeAt(index);
    hash |= 0;
  }
  return hash;
}
