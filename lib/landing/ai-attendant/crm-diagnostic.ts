import type { NicheLandingConfig, PricingPlan } from "@/data/landing/niches/types";
import type { AiAttendantRequest, AiAttendantResponse, GuardrailDecision, QualificationDraft } from "./schema";
import { buildPlanPriceSummary } from "./commercial-pricing";
import { createAssistantMessage } from "./schema";
import { interpretCrmDiagnosticAnswer, type CrmDiagnosticInterpretation, type DiagnosticTurnIntent } from "./crm-diagnostic-interpreter";
import { generateFinalDiagnosticMessages } from "./crm-diagnostic-final";

type DiagnosticState = QualificationDraft & {
  diagnosticType?: "crm_agent_diagnostic";
};

type DiagnosticProfile = {
  painIds: string[];
  crmModules: string[];
  agentIds: string[];
  plan: PricingPlan | undefined;
  temperature: "hot" | "warm" | "cold";
  nextStep: string;
};

type DiagnosticField = keyof DiagnosticState;

const DIAGNOSTIC_TYPE = "crm_agent_diagnostic";

export function isCrmAgentDiagnosticRequest(request: AiAttendantRequest) {
  if (request.session.qualificationDraft?.diagnosticCompleted === "true") return false;
  if (request.session.qualificationDraft?.diagnosticCancelled === "true" && request.quickReplyId !== "start_crm_diagnostic") return false;
  return (
    request.quickReplyId === "start_crm_diagnostic" ||
    request.session.entryPath === "diagnostic_cta" ||
    request.session.qualificationDraft?.diagnosticType === DIAGNOSTIC_TYPE
  );
}

export async function createCrmAgentDiagnosticTurn(
  config: NicheLandingConfig,
  request: AiAttendantRequest,
  guardrailDecision: GuardrailDecision,
): Promise<AiAttendantResponse> {
  const current = (request.session.qualificationDraft ?? {}) as DiagnosticState;
  const currentField = lastAskedField(current);
  const deterministicRoute = currentField ? deterministicDiagnosticSideRoute(request.userMessage ?? "") : undefined;
  if (currentField && deterministicRoute) {
    return createDiagnosticRoutedTurn(config, request, current, guardrailDecision, deterministicRoute);
  }

  const deterministicPatch = extractDiagnosticPatch(request.userMessage ?? "", current);
  const aiInterpretation = shouldUseAiDiagnosticInterpretation(currentField, deterministicPatch, request.userMessage ?? "")
    ? await interpretCrmDiagnosticAnswer({
        userMessage: request.userMessage ?? "",
        currentField,
        currentQuestion: lastAskedQuestion(current),
        currentDraft: current,
      })
    : undefined;
  if (currentField && aiInterpretation && aiInterpretation.confidence >= 0.55 && aiInterpretation.intent !== "answer_current_question") {
    return createDiagnosticRoutedTurn(config, request, current, guardrailDecision, aiInterpretation);
  }

  const extracted = ensureDiagnosticProgress(
    mergeDiagnosticPatches(current, deterministicPatch, aiInterpretation?.patch),
    request.userMessage ?? "",
    lastAskedField(current),
  );
  const nextDraft: DiagnosticState = {
    ...current,
    ...extracted,
    diagnosticType: DIAGNOSTIC_TYPE,
  };

  const nextQuestion = chooseNextDiagnosticQuestion(nextDraft);
  const profile = buildDiagnosticProfile(config, nextDraft);
  const basePatch: QualificationDraft = {
    ...extracted,
    diagnosticType: DIAGNOSTIC_TYPE,
    diagnosticAskedFields: markAsked(current.diagnosticAskedFields, nextQuestion?.field),
    contactCaptureStatus: nextDraft.contactCaptureStatus ?? contactStatus(nextDraft),
  };

  if (nextQuestion) {
    const acknowledgement = buildAcknowledgement(current, extracted, nextDraft, aiInterpretation?.feedback, aiInterpretation?.sideAnswer);
    const assistantMessages = acknowledgement
      ? [
          createAssistantMessage(acknowledgement, "crm_agent_diagnostic"),
          createAssistantMessage(nextQuestion.message, "crm_agent_diagnostic"),
        ]
      : [createAssistantMessage(nextQuestion.message, "crm_agent_diagnostic")];

    return {
      assistantMessages,
      capturedPainIds: unique([...(request.session.selectedPainIds ?? []), ...profile.painIds]),
      recommendedAgentIds: unique([...(request.session.recommendedAgentIds ?? []), ...profile.agentIds]),
      nextQuestion: nextQuestion.message,
      shouldOfferDiagnostic: true,
      qualificationPatch: basePatch,
      guardrailDecision,
    };
  }

  const finalPatch: QualificationDraft = {
    ...basePatch,
    diagnosticCompleted: "true",
    diagnosticStatus: "completed",
    diagnosticCompletedAt: new Date().toISOString(),
    commercialStage: "recommendation_validation",
    waitlistStatus: "not_offered",
    operationalPains: nextDraft.operationalPains ?? profile.painIds.join(", "),
    primaryPainOrIntent: nextDraft.operationalPains ?? nextDraft.priorityGoal ?? profile.painIds.join(", "),
    crmPainAreas: profile.crmModules.join(", "),
    agentPainAreas: profile.agentIds.join(", "),
    leadTemperature: profile.temperature,
    recommendedCrmModules: profile.crmModules.join(", "),
    recommendedAgents: profile.agentIds.join(", "),
    recommendedPlan: profile.plan?.id ?? config.subscription.recommendedPlanId,
    diagnosticSummary: buildShortSummary(nextDraft, profile),
    diagnosticNextStep: "Validar se a recomendacao fez sentido antes de oferecer lista de espera ou demo.",
    nextAction: "Aguardar resposta do lead ao diagnostico antes de oferecer lista de espera.",
  };

  const fallbackMessages = buildFinalDiagnosticMessages(config, nextDraft, profile).map((message) => message.content);
  const finalMessages = hasNoOperationalPain(nextDraft)
    ? undefined
    : await generateFinalDiagnosticMessages({
        config,
        draft: nextDraft,
        painIds: profile.painIds,
        crmModules: profile.crmModules,
        agentIds: profile.agentIds,
        planName: profile.plan?.name ?? "Completo",
        fallbackMessages,
      });

  return {
    assistantMessages: [
      ...(finalMessages ?? fallbackMessages).map((content) => createAssistantMessage(content, "crm_agent_diagnostic")),
      createAssistantMessage("Isso faz sentido para o momento do seu studio?", "crm_agent_diagnostic"),
    ],
    capturedPainIds: hasNoOperationalPain(nextDraft) ? [] : unique([...(request.session.selectedPainIds ?? []), ...profile.painIds]),
    recommendedAgentIds: hasNoOperationalPain(nextDraft) ? [] : unique([...(request.session.recommendedAgentIds ?? []), ...profile.agentIds]),
    recommendations: buildRecommendations(config, profile.painIds),
    nextQuestion: "Isso faz sentido para o momento do seu studio?",
    conversionPath: "crm_agent_diagnostic",
    subscription: undefined,
    shouldOfferDiagnostic: false,
    qualificationPatch: finalPatch,
    guardrailDecision,
  };
}

function createDiagnosticRoutedTurn(
  config: NicheLandingConfig,
  request: AiAttendantRequest,
  current: DiagnosticState,
  guardrailDecision: GuardrailDecision,
  route: DiagnosticTurnRouteLike,
): AiAttendantResponse {
  if (route.intent === "diagnostic_cancel") {
    return createDiagnosticCancellationTurn(config, request, guardrailDecision, route.sideAnswer);
  }

  if (route.intent === "custom_agent_request") {
    return createDiagnosticCustomAgentTurn(request, guardrailDecision, route.sideAnswer);
  }

  return createDiagnosticSideQuestionTurn(
    config,
    request,
    current,
    guardrailDecision,
    route.intent === "price_or_plan" ? undefined : route.sideAnswer,
    route.shouldContinueDiagnostic,
  );
}

type DiagnosticTurnRouteLike = Pick<CrmDiagnosticInterpretation, "intent" | "shouldContinueDiagnostic" | "confidence" | "sideAnswer" | "reason">;

function createDiagnosticCancellationTurn(
  config: NicheLandingConfig,
  request: AiAttendantRequest,
  guardrailDecision: GuardrailDecision,
  sideAnswer?: string,
): AiAttendantResponse {
  const planSummary = buildPlanPriceSummary(config);
  const nextQuestion = "Voce quer abrir o comparativo de planos ou prefere tirar alguma duvida antes?";

  return {
    assistantMessages: [
      createAssistantMessage(sideAnswer ?? "Tudo bem, deixo o diagnostico de lado.", "answer_question"),
      createAssistantMessage(`Hoje os planos sao: ${planSummary}.`, "answer_question"),
      createAssistantMessage(nextQuestion, "answer_question"),
    ],
    capturedPainIds: request.session.selectedPainIds ?? [],
    recommendedAgentIds: request.session.recommendedAgentIds ?? [],
    recommendations: undefined,
    nextQuestion,
    shouldOfferDiagnostic: false,
    qualificationPatch: {
      diagnosticCancelled: "true",
      contactCaptureStatus: request.session.qualificationDraft?.contactCaptureStatus ?? "pending",
    },
    guardrailDecision,
  };
}

function createDiagnosticCustomAgentTurn(
  request: AiAttendantRequest,
  guardrailDecision: GuardrailDecision,
  sideAnswer?: string,
): AiAttendantResponse {
  const message = request.userMessage?.trim() ?? "essa rotina";
  return {
    assistantMessages: [
      createAssistantMessage(
        sideAnswer ?? "Essa frente nao parece estar no time principal da Taliya hoje.",
        "custom_agent_follow_up",
      ),
      createAssistantMessage(
        "Isso entra melhor como Agente sob medida. Vou te levar para esse caminho para mapear a rotina, canal e objetivo sem forcar um diagnostico que nao combina com esse pedido.",
        "custom_agent_follow_up",
      ),
    ],
    capturedPainIds: request.session.selectedPainIds ?? [],
    recommendedAgentIds: request.session.recommendedAgentIds ?? [],
    recommendations: undefined,
    conversionPath: "custom_agent_follow_up",
    subscription: undefined,
    shouldOfferDiagnostic: true,
    qualificationPatch: {
      diagnosticCancelled: "true",
      customRoutine: message.slice(0, 180),
      preferredNextStep: "custom_agent_follow_up",
    },
    guardrailDecision,
  };
}

function createDiagnosticSideQuestionTurn(
  config: NicheLandingConfig,
  request: AiAttendantRequest,
  current: DiagnosticState,
  guardrailDecision: GuardrailDecision,
  sideAnswer?: string,
  shouldResumeDiagnostic = true,
): AiAttendantResponse {
  const currentQuestion = cleanDiagnosticQuestion(lastAskedQuestion(current) ?? chooseNextDiagnosticQuestion(current)?.message ?? "Quer continuar o diagnostico por aqui?");
  const planSummary = buildPlanPriceSummary(config);
  const profile = buildDiagnosticProfile(config, current);

  return {
    assistantMessages: shouldResumeDiagnostic
      ? [
          createAssistantMessage(sideAnswer ?? `Claro. Antes de seguir: hoje os planos sao ${planSummary}.`, "answer_question"),
          createAssistantMessage(
            `Se quiser continuar, sigo da pergunta em que eu estava: ${currentQuestion}`,
            "crm_agent_diagnostic",
          ),
        ]
      : [createAssistantMessage(sideAnswer ?? `Claro. Antes de seguir: hoje os planos sao ${planSummary}.`, "answer_question")],
    capturedPainIds: unique([...(request.session.selectedPainIds ?? []), ...profile.painIds]),
    recommendedAgentIds: unique([...(request.session.recommendedAgentIds ?? []), ...profile.agentIds]),
    nextQuestion: currentQuestion,
    shouldOfferDiagnostic: true,
    qualificationPatch: {
      diagnosticType: DIAGNOSTIC_TYPE,
      diagnosticAskedFields: current.diagnosticAskedFields,
      contactCaptureStatus: current.contactCaptureStatus ?? contactStatus(current),
    },
    guardrailDecision,
  };
}

function deterministicDiagnosticSideRoute(message: string): DiagnosticTurnRouteLike | undefined {
  const normalized = normalize(message);
  const route = deterministicDiagnosticSideIntent(normalized);
  if (!route) return undefined;

  return {
    intent: route,
    shouldContinueDiagnostic: route !== "custom_agent_request" && route !== "diagnostic_cancel",
    confidence: 1,
    reason: "deterministic diagnostic side route",
    sideAnswer: deterministicDiagnosticSideAnswer(route),
  };
}

function deterministicDiagnosticSideIntent(normalized: string): DiagnosticTurnIntent | undefined {
  if (/\b(nao quero|nao preciso|cancela|cancelar|deixa pra la|deixa de lado|sem diagnostico)\b/.test(normalized) && /\b(diagnostico|diagnositco|diagnosticar|raio[-\s]?x)\b/.test(normalized)) {
    return "diagnostic_cancel";
  }
  if (
    /\b(preco|precos|valor|valores|quanto custa|quanto e|quanto fica|assinatura)\b/.test(normalized) ||
    /\b(ver|mostrar|comparar|saber|quais|qual|me fala|me mostra|abrir)\b.{0,40}\bplanos?\b/.test(normalized) ||
    /\bplanos?\b.{0,40}\b(custa|custam|valor|valores|preco|precos)\b/.test(normalized)
  ) {
    return "price_or_plan";
  }
  if (/\b(marketing|instagram|campanha|campanhas|trafego|conteudo|post|posts|social media|midia social|anuncio|anuncios|parceria|estoque|rh)\b/.test(normalized)) {
    return "custom_agent_request";
  }
  if (/\b(humano|pessoa|consultor|vendedor|atendente|whatsapp humano|falar com alguem)\b/.test(normalized)) {
    return "human_request";
  }
  if (/\b(integra|integracao|conecta|conectar)\b/.test(normalized) && /\b(sistema|software|app|plataforma|agenda|crm)\b/.test(normalized)) {
    return "unsupported_integration";
  }
  return undefined;
}

function deterministicDiagnosticSideAnswer(intent: DiagnosticTurnIntent) {
  if (intent === "custom_agent_request") {
    return "Essa frente nao parece estar no time principal da Taliya hoje.";
  }
  if (intent === "human_request") {
    return "Claro, posso te encaminhar para uma conversa humana. Para nao chegar no escuro, eu estava deixando um pouco de contexto organizado.";
  }
  if (intent === "unsupported_integration") {
    return "Sobre integracao com sistema externo, eu prefiro confirmar caso a caso para nao te prometer algo errado.";
  }
  if (intent === "product_question") {
    return "Claro. Te respondo isso sem problema e depois retomo a pergunta do diagnostico.";
  }
  return undefined;
}

function shouldUseAiDiagnosticInterpretation(
  currentField: DiagnosticField | undefined,
  deterministicPatch: Partial<DiagnosticState>,
  message: string,
) {
  if (!currentField) return false;
  if (message.trim().length < 2) return false;
  if (!Object.keys(deterministicPatch).length) return true;

  const answeredByField: Partial<Record<DiagnosticField, keyof DiagnosticState>> = {
    name: "name",
    contactCaptureStatus: "contactCaptureStatus",
    activeStudentsRange: "activeStudentsRange",
    operationalPains: "operationalPains",
    dailyVisibility: "dailyVisibility",
    replacementComplexity: "replacementComplexity",
    salesFollowupMaturity: "salesFollowupMaturity",
    currentSystem: "currentSystem",
    priorityGoal: "priorityGoal",
    buyingTiming: "buyingTiming",
  };
  const expectedKey = answeredByField[currentField];
  return !expectedKey || !deterministicPatch[expectedKey];
}

function extractDiagnosticPatch(message: string, current: DiagnosticState): Partial<DiagnosticState> {
  const normalized = normalize(message);
  const patch: Partial<DiagnosticState> = {};
  const diagnosticRequest = isDiagnosticRequest(message);
  const currentField = lastAskedField(current);
  const contact = extractContact(message, currentField);
  const size = extractStudioSize(normalized, currentField);
  const pains = shouldExtractPains(normalized, currentField, diagnosticRequest) ? extractPains(normalized) : [];
  const currentSystem = currentField === "currentSystem" ? extractCurrentSystem(normalized) : undefined;
  const timing = currentField === "buyingTiming" ? extractBuyingTiming(normalized) : undefined;

  if (contact.name && !current.name) patch.name = contact.name;
  if (contact.email) patch.email = contact.email;
  if (contact.whatsapp) patch.whatsapp = contact.whatsapp;
  if (contact.refused) patch.contactCaptureStatus = "refused";
  if (contact.email || contact.whatsapp) patch.contactCaptureStatus = "captured";
  if (size) patch.activeStudentsRange = size;
  if (size) patch.studioSizeRange = size;
  if (pains.length) patch.operationalPains = mergeCsv(current.operationalPains, pains);
  if (currentSystem) patch.currentSystem = currentSystem;
  if (timing) patch.buyingTiming = timing;

  if (currentField === "contactCaptureStatus" && isContinueWithoutContact(normalized)) patch.contactCaptureStatus = "refused";
  if (!patch.dailyVisibility && currentField === "dailyVisibility" && isAffirmative(normalized) && /caderno|planilha|papel|whatsapp|manual|anotacao|anotacoes/.test(normalized)) {
    patch.dailyVisibility = "visao_manual";
  }
  if (!patch.dailyVisibility && currentField === "dailyVisibility" && isAffirmative(normalized) && !/caderno|planilha|papel|whatsapp|bagunca|baguncado|perdido|manual|anotacao|anotacoes/.test(normalized)) {
    patch.dailyVisibility = "tem_visao";
  }
  if (!patch.dailyVisibility && currentField === "dailyVisibility" && (isNegative(normalized) || (!isAffirmative(normalized) && /caderno|planilha|papel|whatsapp|bagunca|baguncado|perdido|manual/.test(normalized)))) {
    patch.dailyVisibility = "sem_visao";
  }
  if (!patch.dailyVisibility && currentField === "dailyVisibility" && /(consigo|conseguimos|sim).*(ver|enxergar|saber).*(dia|hoje|prioridade)/.test(normalized)) patch.dailyVisibility = "tem_visao";
  if (currentField === "dailyVisibility" && /(nao|não|n|difícil|dificil|bagunca|bagunça|perdido|planilha|caderno).*(ver|enxergar|saber|dia|hoje|prioridade)/.test(normalized)) {
    patch.dailyVisibility = "sem_visao";
  }
  if (currentField === "replacementComplexity" && (/mensagem|troca|caos|bagunca|baguncado|trabalho|dificil|demora/.test(normalized) || isNegative(normalized))) {
    patch.replacementComplexity = "alta";
  }
  if (currentField === "replacementComplexity" && (/ok|tranquilo|facil|organizado|sim/.test(normalized) && !/nao|não|n /.test(normalized))) {
    patch.replacementComplexity = "baixa";
  }
  if (/(reposicao|reposicoes|repor|remarcar).*(bagunca|bagunça|dificil|difícil|mensagem|caos|trabalho)/.test(normalized)) {
    patch.replacementComplexity = "alta";
  }
  if (/(reposicao|reposicoes|repor|remarcar).*(ok|tranquilo|facil|fácil|organizado)/.test(normalized)) {
    patch.replacementComplexity = "baixa";
  }
  if (currentField === "salesFollowupMaturity" && (isNegative(normalized) || /perco|perde|demora|esfria|sem retorno|nao acompanha|não acompanha|n consigo|nao consigo/.test(normalized))) {
    patch.salesFollowupMaturity = "fraco";
  }
  if (currentField === "salesFollowupMaturity" && /toma tempo|demora|trabalho|manual|na mao|na unha|cansativo/.test(normalized)) {
    patch.salesFollowupMaturity = "manual";
  }
  if (currentField === "salesFollowupMaturity" && (isAffirmative(normalized) || /acompanho|organizado|crm|sistema/.test(normalized)) && !patch.salesFollowupMaturity) {
    patch.salesFollowupMaturity = "organizado";
  }
  if (
    currentField === "salesFollowupMaturity" &&
    (/(lead|interessado|interessados|venda|vendas|vender|experimental|matricula|matrícula).*(perde|demora|sem retorno|sem follow|nao acompanha|não acompanha|nao consigo|não consigo|n consigo|esfria)/.test(normalized) ||
      /(sem follow|sem retorno|perco interessados|perde interessados|nao consigo vender|não consigo vender|n consigo vender|vender bem)/.test(normalized))
  ) {
    patch.salesFollowupMaturity = "fraco";
  }
  if (currentField === "salesFollowupMaturity" && /(lead|interessado|interessados|venda|vendas|vender|experimental|matricula|matrícula).*(acompanha|organizado|crm|sistema)/.test(normalized)) {
    patch.salesFollowupMaturity = "organizado";
  }
  if (!diagnosticRequest && !current.priorityGoal && message.trim().length > 10 && currentField === "priorityGoal") {
    patch.priorityGoal = message.trim().slice(0, 180);
  }

  return patch;
}

function shouldExtractPains(normalized: string, currentField: DiagnosticField | undefined, diagnosticRequest: boolean) {
  if (diagnosticRequest) return false;
  if (currentField === "operationalPains") return true;
  if (currentField) return false;
  return !/(whatsapp|zap|telefone|celular|email|e-mail)\s*(e|eh|:)?\s*(?:\+?55\s*)?(?:\(?\d{2}\)?\s*)?\d{4,5}[-\s]?\d{4}/.test(normalized);
}

function mergeDiagnosticPatches(
  current: DiagnosticState,
  deterministicPatch: Partial<DiagnosticState>,
  aiPatch: Partial<QualificationDraft> | undefined,
): Partial<DiagnosticState> {
  if (!aiPatch || !Object.keys(aiPatch).length) return deterministicPatch;

  const semanticPatch = aiPatch as Partial<DiagnosticState>;
  const merged: Partial<DiagnosticState> = {
    ...deterministicPatch,
    ...semanticPatch,
  };

  if (deterministicPatch.whatsapp) merged.whatsapp = deterministicPatch.whatsapp;
  if (deterministicPatch.email) merged.email = deterministicPatch.email;
  if (deterministicPatch.activeStudentsRange) merged.activeStudentsRange = deterministicPatch.activeStudentsRange;
  if (deterministicPatch.studioSizeRange) merged.studioSizeRange = deterministicPatch.studioSizeRange;
  if (deterministicPatch.contactCaptureStatus === "captured") merged.contactCaptureStatus = "captured";

  const painValues = [deterministicPatch.operationalPains, aiPatch.operationalPains].filter(Boolean) as string[];
  if (painValues.length) merged.operationalPains = mergeCsv(current.operationalPains, painValues.flatMap((item) => item.split(",").map((value) => value.trim())));

  return merged;
}

function ensureDiagnosticProgress(
  patch: Partial<DiagnosticState>,
  message: string,
  currentField: DiagnosticField | undefined,
): Partial<DiagnosticState> {
  const clean = message.trim();
  if (!currentField || clean.length < 2 || isDiagnosticRequest(clean)) return patch;

  if (currentField === "operationalPains" && !patch.operationalPains) {
    return { ...patch, operationalPains: clean.slice(0, 180) };
  }
  if (currentField === "dailyVisibility" && !patch.dailyVisibility) {
    return { ...patch, dailyVisibility: "resposta_livre" };
  }
  if (currentField === "replacementComplexity" && !patch.replacementComplexity) {
    return { ...patch, replacementComplexity: "resposta_livre" };
  }
  if (currentField === "salesFollowupMaturity" && !patch.salesFollowupMaturity) {
    return { ...patch, salesFollowupMaturity: "resposta_livre" };
  }
  if (currentField === "currentSystem" && !patch.currentSystem) {
    return { ...patch, currentSystem: clean.slice(0, 120) };
  }
  if (currentField === "priorityGoal" && !patch.priorityGoal) {
    return { ...patch, priorityGoal: clean.slice(0, 180) };
  }
  if (currentField === "buyingTiming" && !patch.buyingTiming) {
    return { ...patch, buyingTiming: clean.slice(0, 80) };
  }

  return patch;
}

function chooseNextDiagnosticQuestion(draft: DiagnosticState): { field: keyof DiagnosticState; message: string } | null {
  const asked = csvSet(draft.diagnosticAskedFields);
  if (!draft.name) {
    return { field: "name", message: "Boa. Antes de eu montar o diagnóstico: com quem eu falo?" };
  }
  if (!draft.whatsapp && !draft.email && draft.contactCaptureStatus !== "refused") {
    return {
      field: "contactCaptureStatus",
      message: `Pra deixar esse diagnóstico salvo para você, ${draft.name}, me passa um WhatsApp ou email? Se preferir, eu continuo mesmo assim, tudo bem?`,
    };
  }
  if (!draft.activeStudentsRange) {
    return { field: "activeStudentsRange", message: "Hoje seu studio tem mais ou menos quantos alunos ativos?" };
  }
  if (!draft.operationalPains) {
    return {
      field: "operationalPains",
      message: "Quais partes mais dão trabalho hoje: WhatsApp, agenda/reposições, vendas, financeiro ou acompanhamento dos alunos?",
    };
  }
  if (!draft.dailyVisibility) {
    return { field: "dailyVisibility", message: "Hoje você consegue ver facilmente o que precisa ser resolvido no dia?" };
  }
  if (hasPain(draft, ["reposicoes", "faltas"]) && !draft.replacementComplexity && !asked.has("replacementComplexity")) {
    return { field: "replacementComplexity", message: "E reposições hoje são fáceis de organizar ou viram troca de mensagem?" };
  }
  if (hasPain(draft, ["vendas"]) && !draft.salesFollowupMaturity && !asked.has("salesFollowupMaturity")) {
    return { field: "salesFollowupMaturity", message: "Quando alguém chama querendo conhecer o studio, vocês conseguem acompanhar até virar aluno?" };
  }
  if (!draft.currentSystem && !asked.has("currentSystem")) {
    const manualHint = draft.dailyVisibility === "visao_manual";
    return {
      field: "currentSystem",
      message: manualHint
        ? "Além dessas anotações, hoje isso fica em algum sistema ou mais em WhatsApp, planilha e caderno?"
        : "Hoje isso fica em algum sistema ou mais em WhatsApp, planilha e caderno?",
    };
  }
  if (!draft.priorityGoal && !asked.has("priorityGoal")) {
    return { field: "priorityGoal", message: "Pensando na rotina do studio, qual tarefa você mais gostaria de deixar mais leve primeiro?" };
  }
  if (!draft.buyingTiming && !asked.has("buyingTiming")) {
    return { field: "buyingTiming", message: "Vocês estão buscando resolver isso agora ou só pesquisando por enquanto?" };
  }
  return null;
}

function buildDiagnosticProfile(config: NicheLandingConfig, draft: DiagnosticState): DiagnosticProfile {
  const painIds = derivePainIds(draft);
  const agentIds = deriveAgentIds(painIds);
  const crmModules = deriveCrmModules(draft, painIds);
  const plan = recommendPlan(config, draft, agentIds, crmModules);
  const temperature = deriveTemperature(draft);
  const nextStep =
    hasNoOperationalPain(draft)
      ? "Quer abrir o comparativo de planos só para conhecer as opções, sem recomendação agressiva?"
      : temperature === "hot"
      ? "Quer que eu te mostre os planos já com essa recomendação?"
      : config.floatingAgent.guidedDemoReady
        ? "Quer ver uma demo guiada ou comparar os planos com essa recomendação?"
        : "Quer comparar os planos com essa recomendação ou continuar pelo WhatsApp?";

  return { painIds, agentIds, crmModules, plan, temperature, nextStep };
}

function buildFinalDiagnosticMessages(config: NicheLandingConfig, draft: DiagnosticState, profile: DiagnosticProfile) {
  const planName = profile.plan?.name ?? "Completo";
  if (hasNoOperationalPain(draft)) {
    return [
      createAssistantMessage("Ok, já tenho as informações necessárias e vou montar o diagnóstico.", "crm_agent_diagnostic"),
      createAssistantMessage(
        "Pelo que você contou, não apareceu um gargalo urgente agora: a rotina está funcionando, vocês já têm sistema e a busca é mais para conhecer opções.",
        "crm_agent_diagnostic",
      ),
      createAssistantMessage(
        `Nesse cenário, eu não começaria por agentes. Se fizer sentido comparar a Taliya, olharia primeiro o plano ${planName} como ponto de comparação e deixaria automações para quando surgir uma dor clara.`,
        "crm_agent_diagnostic",
      ),
      createAssistantMessage(profile.nextStep, "crm_agent_diagnostic"),
    ];
  }

  const painText = profile.painIds.length ? labelList(profile.painIds.map(labelPain)) : "organização da rotina";
  const moduleText = labelList(profile.crmModules);
  const agentText = labelList(profile.agentIds.map(labelAgent));
  const recommendation = buildPlanRecommendationText(planName, profile);
  const baseReason = buildCrmBaseReason(draft, profile);
  const agentIntro = profile.agentIds.length
    ? `Em cima disso, os agentes indicados seriam ${agentText}. Eles aparecem abaixo, um por vez, para ficar claro o papel de cada um.`
    : "Como a dor ainda ficou mais geral, eu começaria organizando a base da rotina antes de ativar agentes.";

  return [
    createAssistantMessage("Ok, já tenho as informações necessárias para montar seu diagnóstico. Já te retorno.", "crm_agent_diagnostic"),
    createAssistantMessage(
      `Pelo que você contou, o gargalo principal está em ${painText}. Antes de pensar em agente, a Taliya precisa organizar a base da rotina: alunos, conversas, agenda, financeiro e prioridades do dia no mesmo lugar.`,
      "crm_agent_diagnostic",
    ),
    createAssistantMessage(`Minha recomendação é organizar primeiro a base que sustenta esses gargalos: ${moduleText}. ${baseReason} ${recommendation}`, "crm_agent_diagnostic"),
    createAssistantMessage(`${agentIntro} ${profile.nextStep}`, "crm_agent_diagnostic"),
  ];
}

function buildRecommendations(config: NicheLandingConfig, painIds: string[]) {
  const agentIds = deriveAgentIds(painIds);
  return agentIds.map((agentId) => {
    const detail = agentRecommendationDetail(agentId, painIds);
    return {
      painId: `${agentId}_diagnostic`,
      agentIds: [agentId],
      painSummary: detail.reason,
      explanation: detail.explanation,
      exampleAction: detail.exampleAction,
    };
  });
}

function derivePainIds(draft: DiagnosticState) {
  const source = normalize([draft.operationalPains, draft.biggestPain, draft.priorityGoal].filter(Boolean).join(" "));
  if (hasNoOperationalPain(draft)) return [];
  const painIds = new Set<string>();
  if (/whatsapp|mensagem|atendimento|duvida|dúvida/.test(source)) painIds.add("whatsapp_baguncado");
  if (/reposicao|reposicoes|remarcar|remarcacao|agenda|horario|vaga|falta|faltas/.test(source)) {
    painIds.add("reposicoes");
    painIds.add("faltas");
  }
  if (/venda|vendas|vender|interessado|interessados|experimental|matricula|matrícula|lead/.test(source)) painIds.add("interessados");
  if (/financeiro|mensalidade|cobranca|cobrança|pagamento|renovacao|renovação|vencendo/.test(source)) {
    painIds.add("mensalidades_atrasadas");
    painIds.add("planos_vencendo");
  }
  if (/inativo|sumiu|retencao|retenção|abandono|voltar/.test(source)) painIds.add("alunos_inativos");
  if (/gestao|gestão|prioridade|dia|relatorio|relatório|dinheiro|indicador/.test(source) || draft.dailyVisibility === "sem_visao" || draft.dailyVisibility === "visao_manual") painIds.add("gestao_clareza");
  if (/historico|histórico|evolucao|evolução|restricao|restrição|avaliacao|avaliação/.test(source)) painIds.add("historico_evolucao");
  if (draft.dailyVisibility === "visao_condicional") painIds.add("gestao_clareza");
  return Array.from(painIds);
}

function deriveAgentIds(painIds: string[]) {
  const agentIds = new Set<string>();
  if (painIds.includes("whatsapp_baguncado")) agentIds.add("atendimento");
  if (painIds.includes("reposicoes") || painIds.includes("faltas")) agentIds.add("agenda");
  if (painIds.includes("interessados")) agentIds.add("vendas");
  if (painIds.includes("mensalidades_atrasadas") || painIds.includes("planos_vencendo")) agentIds.add("financeiro");
  if (painIds.includes("alunos_inativos")) agentIds.add("retencao");
  if (painIds.includes("gestao_clareza")) agentIds.add("gestao");
  if (painIds.includes("historico_evolucao")) agentIds.add("historico-evolucao");
  return Array.from(agentIds);
}

function deriveCrmModules(draft: DiagnosticState, painIds: string[]) {
  if (hasNoOperationalPain(draft)) return ["cadastro de alunos", "histórico de conversas", "painel do dia"];
  const modules = new Set<string>(["cadastro de alunos", "histórico de conversas"]);
  if (painIds.some((id) => ["reposicoes", "faltas"].includes(id))) modules.add("agenda e presença");
  if (painIds.includes("interessados")) modules.add("pipeline de interessados");
  if (painIds.some((id) => ["mensalidades_atrasadas", "planos_vencendo"].includes(id))) modules.add("financeiro e renovações");
  if (painIds.includes("alunos_inativos")) modules.add("retenção");
  if (painIds.includes("gestao_clareza") || draft.dailyVisibility === "sem_visao" || draft.dailyVisibility === "visao_manual") modules.add("painel do dia");
  if (painIds.includes("historico_evolucao")) modules.add("histórico e evolução");
  if (draft.dailyVisibility === "visao_condicional") modules.add("painel do dia");
  return Array.from(modules);
}

function recommendPlan(config: NicheLandingConfig, draft: DiagnosticState, agentIds: string[], crmModules: string[]) {
  const crmOnlyIntent = normalize([draft.operationalPains, draft.priorityGoal, draft.biggestPain].filter(Boolean).join(" "));
  if (hasNoOperationalPain(draft)) return config.subscription.plans.find((plan) => plan.id === "base");
  if (/crm|organizar alunos|sem ia|sem agente|sem automacao|sem automação/.test(crmOnlyIntent)) {
    return config.subscription.plans.find((plan) => plan.id === "base");
  }
  if (!agentIds.length) return config.subscription.plans.find((plan) => plan.id === "base");
  const activeStudents = estimateActiveStudents(draft.activeStudentsRange);
  if (agentIds.length >= 5 || activeStudents >= 100 || crmModules.length >= 5) return findPlan(config, "seven_agents");
  if (agentIds.length >= 3 || activeStudents >= 60) return findPlan(config, "three_agents");
  return findPlan(config, "one_agent");
}

function estimateActiveStudents(range: string | undefined) {
  if (range === "ate_30") return 20;
  if (range === "30_a_79") return 60;
  if (range === "80_a_149") return 110;
  if (range === "150_mais") return 150;
  return Number(range?.match(/\d+/)?.[0] ?? 0);
}

function deriveTemperature(draft: DiagnosticState): DiagnosticProfile["temperature"] {
  const timing = normalize(draft.buyingTiming ?? "");
  if (/agora|urgente|este mes|esse mes|comprar|assinar|implantar|resolver/.test(timing)) return "hot";
  if (/pesquisando|vendo|olhando|futuro|depois/.test(timing)) return "cold";
  if (draft.whatsapp || draft.email) return "warm";
  return "cold";
}

function extractContact(message: string, currentField?: DiagnosticField) {
  const email = message.match(/[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}/i)?.[0];
  const phone = message.match(/(?:\+?55\s*)?(?:\(?\d{2}\)?\s*)?\d{4,5}[-\s]?\d{4}/)?.[0];
  const clean = message.trim();
  const diagnosticRequest = isDiagnosticRequest(clean);
  const shouldReadName = currentField === "name" || (!currentField && !email && !phone);
  const contactName = diagnosticRequest || !shouldReadName ? undefined : extractContactName(clean, { email, phone });
  const refused = /\b(prefiro nao|prefiro não|nao quero passar|não quero passar|sem contato|passo depois|depois eu passo)\b/i.test(clean) && clean.length < 100;
  const name =
    !diagnosticRequest && shouldReadName && !email && !phone && looksLikePersonName(clean)
      ? clean
      : undefined;
  return { email, whatsapp: phone, name: contactName ?? name, refused };
}

function isDiagnosticRequest(message: string) {
  const normalized = normalize(message);
  return /\b(diagnostico|diagnositco|raio[-\s]?x|mapear|diagnosticar)\b/.test(normalized);
}

function cleanDiagnosticQuestion(question: string) {
  return question.replace(/^boa\.\s*/i, "").trim();
}

function extractContactName(clean: string, contact: { email?: string; phone?: string }) {
  const explicit =
    clean.match(/\b(?:sou|me chamo|meu nome (?:e|é|eh|Ã©|ÃƒÂ©)|aqui (?:e|é|eh|Ã©|ÃƒÂ©))\s+(\p{L}{2,}(?:\s+\p{L}{2,}){0,2})/iu)?.[1] ??
    clean.match(/\bnome\s*(?:e|é|eh|:)\s*(\p{L}{2,}(?:\s+\p{L}{2,}){0,2})/iu)?.[1] ??
    clean.match(/\bmeu nome\s+\S+\s+(\p{L}{2,}(?:\s+\p{L}{2,}){0,2})/iu)?.[1];
  const leading = clean.match(/^(\p{L}{2,}(?:\s+\p{L}{2,}){0,2})\s*[,;-]/u)?.[1];
  if (explicit && looksLikePersonName(explicit)) return explicit;
  if (leading && looksLikePersonName(leading)) return leading;

  const withoutContact = clean
    .replace(contact.email ?? "", "")
    .replace(contact.phone ?? "", "")
    .replace(/(?:meu\s+)?(?:whatsapp|zap|telefone|celular|email|e-mail)\s*(?:e|é|eh|:)?/gi, "")
    .replace(/\b(meu|minha|nome|e|é|eh|contato|numero|número|para|pra|diagnostico|diagnóstico)\b/gi, " ")
    .replace(/[,:;.\-()]/g, " ")
    .replace(/\s+/g, " ")
    .trim();

  return looksLikePersonName(withoutContact) ? withoutContact : undefined;
}

function looksLikePersonName(value: string) {
  const clean = value.trim();
  const normalized = normalize(clean);
  if (clean.length < 2 || clean.length > 40) return false;
  if (!/^[\p{L}\s]+$/u.test(clean)) return false;
  if (clean.split(/\s+/).length > 3) return false;
  return !/\b(consigo|conseguimos|quero|preciso|vender|vendas|whatsapp|agenda|financeiro|caderno|sistema|studio|estudio|resolver|melhorar|organizar)\b/.test(normalized);
}

function extractStudioSize(normalized: string, currentField?: DiagnosticField) {
  const match =
    normalized.match(/(\d{1,4})\s*(alunos|aluno|clientes|cliente|pessoas|ativos|ativas)\b/) ??
    (currentField === "activeStudentsRange" ? normalized.match(/\b(\d{1,4})\b/) : null);
  if (!match) return undefined;
  const total = Number(match[1]);
  if (!Number.isFinite(total)) return undefined;
  if (total < 30) return "ate_30";
  if (total < 80) return "30_a_79";
  if (total < 150) return "80_a_149";
  return "150_mais";
}

function extractPains(normalized: string) {
  const pains: string[] = [];
  if (/whatsapp|mensagem|atendimento|duvida|dúvida/.test(normalized)) pains.push("whatsapp");
  if (/reposicao|reposicoes|remarcar|agenda|horario|falta|faltas/.test(normalized)) pains.push("agenda/reposições");
  if (/venda|vendas|vender|comercial|interessado|interessados|experimental|matricula|lead|leads|orcamento|orçamento/.test(normalized)) pains.push("vendas");
  if (/financeiro|mensalidade|cobranca|pagamento|renovacao/.test(normalized)) pains.push("financeiro");
  if (/gestao|prioridade|dia|relatorio|dinheiro/.test(normalized)) pains.push("gestão");
  if (/historico|evolucao|restricao|avaliacao/.test(normalized)) pains.push("histórico/evolução");
  return pains;
}

function extractCurrentSystem(normalized: string) {
  const mentionsSystemContext = /(hoje fica|fica em|uso|usamos|estou usando|sistema|planilha|excel|caderno|papel|manual|crm|software|\bapp\b)/.test(normalized);
  if (!mentionsSystemContext) return undefined;
  if (/planilha|excel|google sheets/.test(normalized)) return "planilha";
  if (/whatsapp|zap/.test(normalized) && /caderno|papel|manual/.test(normalized)) return "whatsapp_e_manual";
  if (/whatsapp|zap/.test(normalized)) return "whatsapp";
  if (/caderno|papel|manual/.test(normalized)) return "manual";
  if (/sistema|crm|software|app/.test(normalized)) return "sistema";
  return undefined;
}

function extractBuyingTiming(normalized: string) {
  if (/agora|urgente|este mes|esse mes|ja|já|comprar|assinar|implantar/.test(normalized)) return "agora";
  if (/pesquisando|vendo|olhando|comparando|futuro|depois/.test(normalized)) return "pesquisando";
  return undefined;
}

function hasPain(draft: DiagnosticState, needles: string[]) {
  const text = normalize([draft.operationalPains, draft.biggestPain, draft.priorityGoal].filter(Boolean).join(" "));
  return needles.some((needle) => text.includes(needle));
}

function hasNoOperationalPain(draft: DiagnosticState) {
  return hasNoPainText([draft.operationalPains, draft.biggestPain, draft.priorityGoal].filter(Boolean).join(" "));
}

function hasNoPainText(value: string | undefined) {
  if (!value) return false;
  const normalized = normalize(value);
  return /\b(nada|nenhuma|nenhum|sem dor|sem problema|sem problemas|tudo funciona|tudo ja funciona|tudo certo|nao tenho dor|nao pesa|nada me da trabalho)\b/.test(normalized);
}

function contactStatus(draft: DiagnosticState) {
  if (draft.whatsapp || draft.email) return "captured";
  if (draft.contactCaptureStatus === "refused") return "refused";
  return "pending";
}

function buildShortSummary(draft: DiagnosticState, profile: DiagnosticProfile) {
  return `Diagnóstico ${draft.activeStudentsRange ?? "sem tamanho"}: dores ${profile.painIds.join(", ")}; CRM ${profile.crmModules.join(", ")}; agentes ${profile.agentIds.join(", ")}; plano ${profile.plan?.id ?? "indefinido"}.`;
}

function findPlan(config: NicheLandingConfig, id: string) {
  return config.subscription.plans.find((plan) => plan.id === id) ?? config.subscription.plans.find((plan) => plan.id === config.subscription.recommendedPlanId);
}

function mergeCsv(current: string | undefined, values: string[]) {
  return unique([...(current ? current.split(",").map((item) => item.trim()) : []), ...values]).join(", ");
}

function csvSet(value: string | undefined) {
  return new Set((value ?? "").split(",").map((item) => item.trim()).filter(Boolean));
}

function markAsked(current: string | undefined, field: string | undefined) {
  if (!field) return current;
  return mergeCsv(current, [field]);
}

function lastAskedField(current: DiagnosticState): DiagnosticField | undefined {
  const fields = (current.diagnosticAskedFields ?? "")
    .split(",")
    .map((item) => item.trim())
    .filter(Boolean) as DiagnosticField[];
  return fields.at(-1);
}

function lastAskedQuestion(current: DiagnosticState) {
  const field = lastAskedField(current);
  if (!field) return undefined;
  return diagnosticQuestionText(field, current);
}

function diagnosticQuestionText(field: DiagnosticField, draft: DiagnosticState) {
  const questions: Partial<Record<DiagnosticField, string>> = {
    name: "Boa. Antes de eu montar o diagnostico: com quem eu falo?",
    contactCaptureStatus: `Pra deixar esse diagnostico salvo para voce, ${draft.name ?? ""}, me passa um WhatsApp ou email? Se preferir, eu continuo mesmo assim, tudo bem?`,
    activeStudentsRange: "Hoje seu studio tem mais ou menos quantos alunos ativos?",
    operationalPains: "Quais partes mais dao trabalho hoje: WhatsApp, agenda/reposicoes, vendas, financeiro ou acompanhamento dos alunos?",
    dailyVisibility: "Hoje voce consegue ver facilmente o que precisa ser resolvido no dia?",
    replacementComplexity: "E reposicoes hoje sao faceis de organizar ou viram troca de mensagem?",
    salesFollowupMaturity: "Quando alguem chama querendo conhecer o studio, voces conseguem acompanhar ate virar aluno?",
    currentSystem: "Hoje isso fica em algum sistema ou mais em WhatsApp, planilha e caderno?",
    priorityGoal: "Pensando na rotina do studio, qual tarefa voce mais gostaria de deixar mais leve primeiro?",
    buyingTiming: "Voces estao buscando resolver isso agora ou so pesquisando por enquanto?",
  };
  return questions[field];
}

function buildAcknowledgement(
  current: DiagnosticState,
  extracted: Partial<DiagnosticState>,
  nextDraft: DiagnosticState,
  aiFeedback?: string,
  sideAnswer?: string,
) {
  const answeredField = lastAskedField(current);
  if (!answeredField) return undefined;
  if (!Object.keys(extracted).length && sideAnswer) return sideAnswer;
  if (!Object.keys(extracted).length) return undefined;
  if (sideAnswer && aiFeedback) return `${sideAnswer} ${aiFeedback}`;
  if (sideAnswer) return sideAnswer;
  if (aiFeedback) return aiFeedback;

  if (answeredField === "name" && extracted.name) return `Prazer, ${extracted.name}. Vou conduzir isso em poucos passos.`;
  if (answeredField === "contactCaptureStatus") {
    if (extracted.whatsapp || extracted.email) return "Perfeito, deixei esse contato junto do diagnóstico.";
    if (extracted.contactCaptureStatus === "refused") return "Tudo bem, sigo por aqui e você deixa contato depois se quiser.";
  }
  if (answeredField === "activeStudentsRange" && extracted.activeStudentsRange) return "Boa, isso já me dá uma noção do tamanho da operação.";
  if (answeredField === "operationalPains" && extracted.operationalPains) return painAcknowledgement(nextDraft);
  if (answeredField === "dailyVisibility" && extracted.dailyVisibility) {
    if (extracted.dailyVisibility === "visao_manual") {
      return "Boa, então você até consegue enxergar o dia. O ponto é que, quando isso depende do caderno, a prioridade ainda fica muito presa na memória e na disciplina de atualizar tudo.";
    }
    if (extracted.dailyVisibility === "visao_condicional") {
      return "Entendi. Se depende do seu tempo, entao a visao do dia existe, mas ainda nao esta facil o suficiente para confiar nela na rotina.";
    }
    if (extracted.dailyVisibility === "resposta_livre") {
      return "Entendi. Vou considerar essa resposta como contexto da sua visao do dia.";
    }
    return extracted.dailyVisibility === "sem_visao"
      ? "Entendi. Quando a visão do dia fica espalhada, muita coisa importante depende da memória."
      : "Ótimo. Se vocês já enxergam o dia, o próximo ponto é ver onde ainda há trabalho manual demais.";
  }
  if (answeredField === "replacementComplexity" && extracted.replacementComplexity) {
    if (extracted.replacementComplexity === "resposta_livre") {
      return "Entendi. Vou levar esse contexto em conta para avaliar agenda, faltas e reposicoes.";
    }
    return extracted.replacementComplexity === "alta"
      ? "Faz sentido. Reposição que vira troca de mensagem costuma consumir energia e ainda deixar vaga vazia."
      : "Bom sinal. Então reposição talvez não seja o maior gargalo agora.";
  }
  if (answeredField === "salesFollowupMaturity" && extracted.salesFollowupMaturity) {
    if (extracted.salesFollowupMaturity === "resposta_livre") {
      return "Entendi. Vou considerar esse ponto para avaliar o acompanhamento de interessados.";
    }
    if (extracted.salesFollowupMaturity === "manual") {
      return "Entendi. Vocês até acompanham, mas se isso toma tempo, o gargalo está no próximo passo ficar organizado sem roubar a rotina.";
    }
    return extracted.salesFollowupMaturity === "fraco"
      ? "Entendi. Quando a venda fica solta, muita gente interessada esfria antes de marcar ou fechar."
      : "Ótimo. Se o acompanhamento comercial já existe, dá para conectar isso melhor com a operação.";
  }
  if (answeredField === "currentSystem" && extracted.currentSystem) {
    if (extracted.currentSystem === "manual" || extracted.currentSystem === "whatsapp_e_manual") {
      return "Entendi. Isso ajuda a não perder tudo, mas ainda deixa a rotina dependente de quem anotou, respondeu ou lembrou de conferir.";
    }
    return "Entendi onde isso está registrado hoje.";
  }
  if (answeredField === "priorityGoal" && extracted.priorityGoal) {
    return hasNoPainText(extracted.priorityGoal)
      ? "Entendi, então hoje não tem uma tarefa urgente pedindo automação."
      : "Boa escolha. Vou usar isso como prioridade do diagnóstico.";
  }
  if (answeredField === "buyingTiming" && extracted.buyingTiming) {
    return extracted.buyingTiming === "agora" ? "Perfeito. Vou considerar que você quer um caminho mais prático." : "Sem problema. Vou deixar a recomendação leve para pesquisa e comparação.";
  }

  return undefined;
}

function painAcknowledgement(draft: DiagnosticState) {
  const pains = derivePainIds(draft);
  if (pains.includes("interessados")) return "Entendi. Quando a venda fica solta, muita gente interessada acaba esfriando antes de marcar uma aula.";
  if (pains.includes("reposicoes") || pains.includes("faltas")) return "Entendi. Faltas e reposições costumam virar um nó porque misturam agenda, WhatsApp e regra do studio.";
  if (pains.includes("whatsapp_baguncado")) return "Entendi. WhatsApp cheio costuma esconder o que é urgente e o que pode esperar.";
  if (pains.includes("mensalidades_atrasadas") || pains.includes("planos_vencendo")) return "Entendi. Financeiro solto pesa porque cobrança e renovação entram no meio da rotina.";
  return "Entendi. Vou conectar essa dor com o que a Taliya precisa organizar primeiro.";
}

function buildCrmBaseReason(draft: DiagnosticState, profile: DiagnosticProfile) {
  if (draft.dailyVisibility === "visao_manual") {
    return "Como você já se apoia em anotações, o ganho não é trocar o caderno por telas: é fazer essas prioridades aparecerem sozinhas, com contexto de aluno, conversa e agenda.";
  }
  if (draft.dailyVisibility === "visao_condicional") {
    return "Como a visao do dia ainda depende do seu tempo, o ganho e fazer as prioridades aparecerem com contexto, sem precisar parar para reconstruir tudo manualmente.";
  }
  if (profile.painIds.includes("interessados")) {
    return "Assim cada interessado ganha próximo passo visível, em vez de depender de lembrar quem respondeu, quem esfriou e quem precisa de retorno.";
  }
  if (profile.painIds.includes("reposicoes") || profile.painIds.includes("faltas")) {
    return "Assim faltas, reposições e horários vagos deixam de ficar espalhados entre conversa, agenda e memória da equipe.";
  }
  if (profile.painIds.includes("mensalidades_atrasadas") || profile.painIds.includes("planos_vencendo")) {
    return "Assim cobrança, renovação e pendências financeiras aparecem antes de virarem atraso acumulado.";
  }
  return "Assim a rotina deixa de depender de memória e vira uma fila clara do que precisa ser resolvido primeiro.";
}

function buildPlanRecommendationText(planName: string, profile: DiagnosticProfile) {
  if (profile.plan?.id === "base") {
    return `Por isso eu compararia o ${planName} primeiro: organizar a operação antes de colocar agente para agir.`;
  }

  if (profile.plan?.id === "one_agent") {
    return `Como apareceu uma dor principal, eu compararia o ${planName}. É um começo enxuto para atacar o ponto mais caro da rotina sem pular direto para uma estrutura maior.`;
  }

  if (profile.plan?.id === "three_agents") {
    return `Como apareceram algumas frentes conectadas, eu compararia o ${planName}. Ele cobre as prioridades com a base da Taliya e agentes sem necessariamente ir para o pacote completo.`;
  }

  return `Como a dor encosta em várias áreas do studio, eu compararia o ${planName} com calma. Ele faz sentido quando atendimento, agenda, vendas, financeiro e gestão precisam trabalhar juntos.`;
}

function agentRecommendationDetail(agentId: string, painIds: string[]) {
  const details: Record<string, { reason: string; explanation: string; exampleAction: string }> = {
    atendimento: {
      reason: "Resolve WhatsApp bagunçado e dúvidas repetidas.",
      explanation: painIds.includes("whatsapp_baguncado")
        ? "Recomendei porque seu atendimento aparece como ponto de perda ou atraso no diagnóstico."
        : "Recomendei para organizar a entrada das conversas antes de passar para agenda, vendas ou financeiro.",
      exampleAction: "Na prática, classifica mensagens, separa aluno de interessado e deixa a equipe ver o que precisa de resposta.",
    },
    agenda: {
      reason: "Resolve reposições, faltas, encaixes e horários vazios.",
      explanation: "Recomendei porque faltas e reposições dependem de regra, vaga e resposta rápida.",
      exampleAction: "Na prática, aponta quem faltou, quem pode repor e quais horários podem ser recuperados.",
    },
    vendas: {
      reason: "Resolve perda de interessados e acompanhamento fraco.",
      explanation: "Recomendei porque a venda precisa de próximo passo claro depois do primeiro contato ou da aula experimental.",
      exampleAction: "Na prática, mostra interessados parados, lembra próximos contatos e ajuda a não deixar a conversa esfriar.",
    },
    financeiro: {
      reason: "Resolve mensalidades, cobranças e renovações esquecidas.",
      explanation: "Recomendei porque financeiro precisa aparecer antes de virar atraso ou plano vencido.",
      exampleAction: "Na prática, prioriza pagamentos pendentes, planos vencendo e mensagens aprovadas para cobrança.",
    },
    retencao: {
      reason: "Resolve alunos sumindo, baixa frequência e risco de cancelamento.",
      explanation: "Recomendei porque presença caindo precisa aparecer cedo, não só quando o aluno já desistiu.",
      exampleAction: "Na prática, cria uma fila de alunos em risco e sugere uma abordagem cuidadosa.",
    },
    gestao: {
      reason: "Resolve falta de clareza do que precisa ser feito no dia.",
      explanation: "Recomendei porque seu diagnóstico mostra necessidade de priorizar pendências espalhadas.",
      exampleAction: "Na prática, transforma faltas, cobranças, interessados e handoffs em uma lista de prioridades.",
    },
    "historico-evolucao": {
      reason: "Resolve contexto de aluno espalhado entre equipe, aula e conversa.",
      explanation: "Recomendei porque histórico ajuda outros agentes e humanos a responderem com memória.",
      exampleAction: "Na prática, organiza observações, restrições e combinados para a pessoa certa ver na hora certa.",
    },
  };

  return details[agentId] ?? {
    reason: "Resolve uma dor identificada no diagnóstico.",
    explanation: "Recomendei porque esse agente atua sobre a rotina que apareceu como prioridade.",
    exampleAction: "Na prática, transforma a pendência em uma próxima ação clara para a equipe.",
  };
}

function isContinueWithoutContact(normalized: string) {
  return /\b(prefiro nao|nao quero passar|sem contato|passo depois|depois eu passo|continua|pode continuar|segue|sem whatsapp|sem email)\b/.test(normalized);
}

function isAffirmative(normalized: string) {
  return /^(sim|s|consigo|conseguimos|tenho|temos|ok|claro|consigo sim)\b/.test(normalized.trim());
}

function isNegative(normalized: string) {
  return /^(nao|não|n|nao consigo|não consigo|n consigo|nem|dificil)\b/.test(normalized.trim());
}

function labelList(values: string[]) {
  if (!values.length) return "";
  if (values.length === 1) return values[0];
  return `${values.slice(0, -1).join(", ")} e ${values[values.length - 1]}`;
}

function labelPain(id: string) {
  const labels: Record<string, string> = {
    whatsapp_baguncado: "WhatsApp",
    reposicoes: "reposições",
    faltas: "faltas",
    interessados: "vendas/interessados",
    mensalidades_atrasadas: "mensalidades",
    planos_vencendo: "renovações",
    alunos_inativos: "alunos inativos",
    gestao_clareza: "gestão do dia",
    historico_evolucao: "histórico dos alunos",
  };
  return labels[id] ?? id;
}

function labelAgent(id: string) {
  const labels: Record<string, string> = {
    atendimento: "Atendimento",
    agenda: "Agenda",
    vendas: "Vendas",
    financeiro: "Financeiro",
    retencao: "Retenção",
    gestao: "Gestão",
    "historico-evolucao": "Histórico/Evolução",
  };
  return labels[id] ?? id;
}

function unique(values: string[]) {
  return Array.from(new Set(values.filter(Boolean)));
}

function normalize(value: string) {
  return value
    .toLowerCase()
    .normalize("NFD")
    .replace(/\p{Diacritic}/gu, "");
}
