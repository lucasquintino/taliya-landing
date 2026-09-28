import type { NicheLandingConfig } from "@/data/landing/niches/types";
import type { AiAttendantRequest, AiAttendantResponse } from "./schema";
import { buildPlanComparisonSummary, buildPlanPriceSummary } from "./commercial-pricing";
import { createAssistantMessage } from "./schema";

export function enforceConversionGates(
  response: AiAttendantResponse,
  request: AiAttendantRequest,
  config: NicheLandingConfig,
  options: { routeIntent?: string } = {},
): AiAttendantResponse {
  if (request.quickReplyId === "view_plans") {
    return createViewPlansResponse(response, config);
  }

  if (request.session.qualificationDraft?.diagnosticCancelled === "true" && hasContactInCurrentMessage(request)) {
    return createPostCancellationContactResponse(response);
  }

  if (options.routeIntent === "price_or_plan" && isCurrentPriceOrPlanQuestion(request) && !isBuyingText(request)) {
    return createPricePlanResponse(response, request, config);
  }

  if (isCheckoutAllowed(request)) {
    return {
      ...response,
      conversionPath: "checkout_intent",
      subscription: {
        planId: config.subscription.recommendedPlanId,
        ctaLabel: config.floatingAgent.conversionCtas.checkoutIntent.label,
      },
      shouldOfferDiagnostic: true,
    };
  }

  if (isDemoRequest(request) && !config.floatingAgent.guidedDemoReady) {
    return hasCompletedDiagnostic(request)
      ? ensureContactCapture(
          {
            ...response,
            assistantMessages: [
              createAssistantMessage(
                "A demonstracao real so deve abrir quando o ambiente da Taliya estiver pronto. Para nao te mostrar um prototipo que confunda sua decisao, posso te explicar o fluxo agora e encaminhar seu caso para continuarmos no WhatsApp com o contexto desta conversa.",
                "guided_demo",
              ),
            ],
            conversionPath: "human_whatsapp_assist",
            subscription: undefined,
            shouldOfferDiagnostic: true,
          },
          request,
          "human_whatsapp_handoff",
        )
      : {
          ...response,
          assistantMessages: [
            createAssistantMessage(
              "A demo real ainda nao esta disponivel agora, e eu nao quero te mostrar um prototipo que confunda sua decisao.",
              "answer_question",
            ),
            createAssistantMessage(
              "Posso te explicar o fluxo na pratica por aqui ou, se preferir, te ajudar a mapear qual parte do studio voce quer ver funcionando.",
              "answer_question",
            ),
          ],
          conversionPath: undefined,
          subscription: undefined,
          handoff: undefined,
          nextQuestion: "Voce quer entender o fluxo por aqui ou mapear uma parte especifica do studio?",
          shouldOfferDiagnostic: true,
        };
  }

  if (shouldStartDiagnosticBeforeConversion(response, request, options)) {
    return createDiagnosticFirstResponse(response, request, diagnosticGateReason(response, request));
  }

  if (!response.conversionPath) return response;

  if (isPostSubscriptionQuestion(request) && !isBuyingText(request)) {
    return {
      ...response,
      conversionPath: undefined,
      subscription: undefined,
      handoff: undefined,
      shouldOfferDiagnostic: false,
    };
  }

  if (response.conversionPath === "guided_demo" && !config.floatingAgent.guidedDemoReady) {
    return {
      ...response,
      assistantMessages: [
        createAssistantMessage(
          "A demonstracao guiada so deve abrir quando o ambiente real da Taliya estiver pronto. Posso te explicar o fluxo agora ou continuar com um consultor no WhatsApp usando o contexto desta conversa.",
          "guided_demo",
        ),
      ],
      conversionPath: "human_whatsapp_assist",
      subscription: undefined,
      shouldOfferDiagnostic: true,
    };
  }

  if (response.conversionPath === "plan_recommendation" && isCheckoutAllowed(request)) {
    return {
      ...response,
      conversionPath: "checkout_intent",
      subscription: response.subscription,
      shouldOfferDiagnostic: true,
    };
  }

  if (response.conversionPath === "checkout_intent" && !isCheckoutAllowed(request)) {
    if (!hasCompletedDiagnostic(request) && request.session.entryPath !== "plans_page") {
      return createDiagnosticFirstResponse(response, request, "checkout_intent");
    }

    return {
      ...response,
      assistantMessages: [
        createAssistantMessage(
          "Antes de te mandar para a assinatura, faz sentido confirmar o plano certo para o seu studio. Pelo que voce contou ate aqui, posso te mostrar o plano recomendado e o comparativo para voce decidir com seguranca.",
          "plan_recommendation",
        ),
      ],
      conversionPath: "plan_recommendation",
      subscription: {
        planId: config.subscription.recommendedPlanId,
        ctaLabel: config.floatingAgent.conversionCtas.viewPlans.label,
      },
      shouldOfferDiagnostic: true,
    };
  }

  if (response.conversionPath === "plan_recommendation" && isBuyingText(request) && !hasCompletedDiagnostic(request) && request.session.entryPath !== "plans_page") {
    return createDiagnosticFirstResponse(response, request, "plan_recommendation");
  }

  if (response.conversionPath === "plan_recommendation" && isPriceWithoutContext(request)) {
    return {
      ...response,
      conversionPath: undefined,
      subscription: undefined,
      handoff: undefined,
      shouldOfferDiagnostic: true,
    };
  }

  if (response.conversionPath === "view_plans" && isBuyingText(request)) {
    return {
      ...response,
      conversionPath: hasPlanConfirmation(request) ? "checkout_intent" : "plan_recommendation",
      subscription: hasPlanConfirmation(request) ? response.subscription : undefined,
    };
  }

  if (response.conversionPath === "custom_agent_diagnostic_unclear" && hasCustomAgentIntent(request)) {
    return ensureContactCapture(
      {
        ...response,
        conversionPath: "custom_agent_follow_up",
        subscription: undefined,
        shouldOfferDiagnostic: true,
      },
      request,
      "custom_agent_follow_up",
    );
  }

  if (response.conversionPath === "custom_agent_follow_up") {
    return ensureContactCapture(response, request, "custom_agent_follow_up");
  }

  if (response.conversionPath === "human_whatsapp_assist") {
    return ensureContactCapture(response, request, "human_whatsapp_handoff");
  }

  if ((response.conversionPath === "view_plans" || response.conversionPath === "plan_recommendation") && (isBroadRoutineOnly(request) || isBroadMultiAreaNeed(request)) && !hasPlanIntent(request)) {
    return {
      ...response,
      conversionPath: undefined,
      subscription: undefined,
      handoff: undefined,
      shouldOfferDiagnostic: true,
    };
  }

  if ((response.conversionPath === "view_plans" || response.conversionPath === "plan_recommendation") && isBasicProductQuestion(request) && !hasPlanIntent(request)) {
    return {
      ...response,
      conversionPath: undefined,
      subscription: undefined,
      handoff: undefined,
      shouldOfferDiagnostic: false,
    };
  }

  if (response.conversionPath === "view_plans" && isPriceObjection(request)) {
    return {
      ...response,
      conversionPath: "plan_recommendation",
      subscription: {
        planId: config.subscription.recommendedPlanId,
        ctaLabel: config.floatingAgent.conversionCtas.viewPlans.label,
      },
      shouldOfferDiagnostic: true,
    };
  }

  if (isCustomAgentConversion(response.conversionPath) && !hasCustomAgentIntent(request)) {
    return {
      ...response,
      conversionPath: undefined,
      subscription: undefined,
      handoff: undefined,
      shouldOfferDiagnostic: false,
    };
  }

  return response;
}

function createPostCancellationContactResponse(response: AiAttendantResponse): AiAttendantResponse {
  const nextQuestion = "Quer abrir o comparativo de planos ou prefere tirar alguma duvida antes?";
  return {
    ...response,
    assistantMessages: [
      createAssistantMessage("Perfeito, deixei esse contato salvo.", "answer_question"),
      createAssistantMessage(nextQuestion, "answer_question"),
    ],
    recommendations: undefined,
    capturedPainIds: [],
    recommendedAgentIds: [],
    conversionPath: undefined,
    subscription: undefined,
    handoff: undefined,
    nextQuestion,
    shouldOfferDiagnostic: false,
    qualificationPatch: {
      ...response.qualificationPatch,
      diagnosticCancelled: "true",
    },
  };
}

function createViewPlansResponse(response: AiAttendantResponse, config: NicheLandingConfig): AiAttendantResponse {
  const planSummary = buildPlanPriceSummary(config);
  const comparison = buildPlanComparisonSummary(config);
  return {
    ...response,
    assistantMessages: [
      createAssistantMessage(`Claro. Hoje os planos sao: ${planSummary}.`, "view_plans"),
      createAssistantMessage(comparison, "view_plans"),
    ],
    recommendations: undefined,
    capturedPainIds: [],
    recommendedAgentIds: [],
    conversionPath: "view_plans",
    subscription: {
      planId: config.subscription.recommendedPlanId,
      ctaLabel: config.floatingAgent.conversionCtas.viewPlans.label,
    },
    handoff: undefined,
    nextQuestion: undefined,
    shouldOfferDiagnostic: true,
  };
}

function createPricePlanResponse(
  response: AiAttendantResponse,
  request: AiAttendantRequest,
  config: NicheLandingConfig,
): AiAttendantResponse {
  const planSummary = buildPlanPriceSummary(config);
  const question = currentMessageText(request);
  const askedPlans = /\b(planos?|assinatura|pacotes?|opcoes?)\b/i.test(normalizeText(question));
  const secondMessage = askedPlans
    ? buildPlanComparisonSummary(config)
    : "Sem diagnostico, eu te mostro os valores. Para recomendar um plano, prefiro fazer um diagnostico gratuito e nao chutar.";
  const nextQuestion = "Quer abrir o comparativo de planos ou prefere fazer o diagnostico gratuito para eu recomendar com contexto?";

  return {
    ...response,
    assistantMessages: [
      createAssistantMessage(`Hoje os planos sao: ${planSummary}.`, "answer_question"),
      createAssistantMessage(secondMessage, "answer_question"),
      createAssistantMessage(nextQuestion, "answer_question"),
    ],
    conversionPath: undefined,
    subscription: undefined,
    handoff: undefined,
    nextQuestion,
    shouldOfferDiagnostic: true,
  };
}

export function isCheckoutAllowed(request: AiAttendantRequest) {
  if (!isBuyingText(request) && request.quickReplyId !== "checkout_intent") return false;
  if (request.session.entryPath === "plans_page") return true;
  if (!hasCompletedDiagnostic(request)) return false;
  return hasPlanConfirmation(request);
}

function hasPlanConfirmation(request: AiAttendantRequest) {
  const text = conversationText(request);
  const previousPlanRecommendation = request.session.messages.some(
    (message) => message.intent === "plan_recommendation" || message.intent === "checkout_intent",
  );
  const explicitPlanMention = /\b(7 agentes|sete agentes|3 agentes|tres agentes|tr[eê]s agentes|1 agente|um agente|base|plano recomendado|plano indicado|esse plano)\b/i.test(text);

  return previousPlanRecommendation || explicitPlanMention;
}

function isBuyingText(request: AiAttendantRequest) {
  const text = conversationText(request);
  return /(quero assinar|quero comprar|quero contratar|posso assinar|assinar agora|comprar agora|fechar agora|quase fechando|fechando o|quero fechar|me manda.*link|link.*pag|pagar|pagamento|comecar agora|começar agora|seguir para assinatura)/i.test(text);
}

function hasPlanIntent(request: AiAttendantRequest) {
  if (request.quickReplyId === "view_plans" || request.quickReplyId === "checkout_intent") return true;
  if (request.session.entryPath === "plans_page") return true;

  const text = conversationText(request);
  return /(plano|planos|preco|preço|valor|quanto custa|assinatura|assinar|comparar|comparativo)/i.test(text);
}

function isCurrentPriceOrPlanQuestion(request: AiAttendantRequest) {
  const text = normalizeText(currentMessageText(request));
  return /\b(preco|precos|valor|valores|quanto custa|quanto e|quanto fica|planos?|pacotes?|assinatura)\b/i.test(text);
}

function isBasicProductQuestion(request: AiAttendantRequest) {
  const text = conversationText(request);
  return /(o que .*taliya|que .*taliya|como funciona .*taliya|o que .*sistema|que sistema|me explica .*taliya|me explique .*taliya)/i.test(text);
}

function isPriceObjection(request: AiAttendantRequest) {
  const text = conversationText(request);
  return /(achei caro|esta caro|t[aá] caro|muito caro|caro demais|nao cabe|não cabe|sem orcamento|sem orçamento|preco alto|preço alto)/i.test(text);
}

function isPriceWithoutContext(request: AiAttendantRequest) {
  const text = normalizedConversationText(request);
  const asksPricingOrPlan = /(quanto custa|preco|valor|qual plano|plano recomenda|plano voce recomenda)/i.test(text);
  const hasKnownContext =
    Boolean(request.pageSignals?.selectedPainId) ||
    Boolean(request.pageSignals?.selectedAgentId) ||
    Boolean(request.pageSignals?.calculatorEstimate) ||
    Boolean(request.session.selectedPainIds?.length) ||
    Boolean(request.session.recommendedAgentIds?.length) ||
    /(reposicao|reposicoes|agenda|whatsapp|financeiro|vendas|faltas|renovacao|retencao|historico|gestao|120 alunos|alunos)/i.test(text);

  return asksPricingOrPlan && !hasKnownContext && !isBuyingText(request);
}

function isPostSubscriptionQuestion(request: AiAttendantRequest) {
  const text = normalizedConversationText(request);
  return /(depois que eu assino|apos assinar|quando eu assinar|depois da assinatura|pos pagamento|depois que pagar)/i.test(text);
}

function shouldStartDiagnosticBeforeConversion(
  response: AiAttendantResponse,
  request: AiAttendantRequest,
  options: { routeIntent?: string },
) {
  if (hasCompletedDiagnostic(request)) return false;
  if (request.session.entryPath === "plans_page") return false;
  if (request.session.qualificationDraft?.diagnosticType === "crm_agent_diagnostic") return false;
  if (response.qualificationPatch?.diagnosticType === "crm_agent_diagnostic") return false;
  if (isPostSubscriptionQuestion(request)) return false;
  if (response.guardrailDecision.category !== "allowed") return false;

  if (options.routeIntent !== "diagnostic_request" && options.routeIntent !== "diagnostic_continue") return false;

  const commercialPath =
    response.conversionPath === "view_plans" ||
    response.conversionPath === "guided_demo" ||
    response.conversionPath === "plan_recommendation" ||
    response.conversionPath === "checkout_intent" ||
    response.conversionPath === "human_whatsapp_assist" ||
    response.conversionPath === "analysis_request";

  if (commercialPath) return true;
  if (isCustomAgentConversion(response.conversionPath)) return false;

  return false;
}

function hasCompletedDiagnostic(request: AiAttendantRequest) {
  return request.session.qualificationDraft?.diagnosticCompleted === "true";
}

function createDiagnosticFirstResponse(
  response: AiAttendantResponse,
  request: AiAttendantRequest,
  reason: NonNullable<AiAttendantResponse["conversionPath"]> | "checkout" | "demo" | "interest",
): AiAttendantResponse {
  const prompt = nextDiagnosticPrompt(request);
  const bridge = diagnosticBridgeMessage(reason);
  const assistantMessage =
    prompt.field === "name"
      ? `${bridge} Antes de eu montar isso direito: com quem eu falo?`
      : `${bridge} ${prompt.message}`;
  const baseMessages =
    reason === "interest" && !response.conversionPath && response.assistantMessages.length
      ? [...response.assistantMessages, createAssistantMessage(prompt.message, "crm_agent_diagnostic")]
      : [createAssistantMessage(assistantMessage, "crm_agent_diagnostic")];

  return {
    ...response,
    assistantMessages: baseMessages,
    conversionPath: undefined,
    subscription: undefined,
    handoff: undefined,
    nextQuestion: prompt.message,
    shouldOfferDiagnostic: true,
    qualificationPatch: {
      ...response.qualificationPatch,
      diagnosticType: "crm_agent_diagnostic",
      diagnosticAskedFields: mergeCsv(response.qualificationPatch?.diagnosticAskedFields ?? request.session.qualificationDraft?.diagnosticAskedFields, [prompt.field]),
      contactCaptureStatus: request.session.qualificationDraft?.contactCaptureStatus ?? response.qualificationPatch?.contactCaptureStatus ?? "pending",
    },
  };
}

function diagnosticGateReason(
  response: AiAttendantResponse,
  request: AiAttendantRequest,
): NonNullable<AiAttendantResponse["conversionPath"]> | "checkout" | "demo" | "interest" {
  if (response.conversionPath) return response.conversionPath;
  const text = normalizedConversationText(request);
  if (/(quanto custa|preco|valor|planos|plano|assinatura)/i.test(text)) return "view_plans";
  if (/(demo|demonstracao|ver funcionando|funcionando)/i.test(text)) return "demo";
  if (/(humano|pessoa|whatsapp|atendente)/i.test(text)) return "human_whatsapp_assist";
  if (/(assinar|comprar|contratar|fechar|pagar|pagamento)/i.test(text)) return "checkout";
  if (/(analise|diagnostico|raio-x|raio x)/i.test(text)) return "analysis_request";
  return "interest";
}

function diagnosticBridgeMessage(reason: NonNullable<AiAttendantResponse["conversionPath"]> | "checkout" | "demo" | "interest") {
  if (reason === "view_plans") {
    return "Posso te mostrar planos e valores agora. Se voce quiser uma recomendacao, ela fica melhor com um diagnostico gratuito rapido.";
  }
  if (reason === "plan_recommendation") {
    return "Da para recomendar um plano, mas eu prefiro fazer isso com contexto do seu studio para nao indicar no escuro.";
  }
  if (reason === "checkout" || reason === "checkout_intent") {
    return "Da para chegar na assinatura, mas antes vale confirmar se o plano esta certo para o seu studio.";
  }
  if (reason === "guided_demo" || reason === "demo") {
    return "A demo fica melhor quando eu sei qual parte da rotina voce quer enxergar funcionando.";
  }
  if (reason === "human_whatsapp_assist") {
    return "Claro, posso encaminhar para continuarmos pelo WhatsApp. Para ir com contexto, vou deixar um diagnostico curto salvo antes.";
  }
  if (reason === "analysis_request") {
    return "Esse diagnostico e exatamente o melhor caminho para mapear sua operacao sem pular direto para plano.";
  }
  return "Posso te ajudar com isso pelo diagnostico gratuito.";
}

function nextDiagnosticPrompt(request: AiAttendantRequest): { field: string; message: string } {
  const draft = request.session.qualificationDraft;
  if (!draft?.name) return { field: "name", message: "Antes de eu montar isso direito: com quem eu falo?" };
  if (!draft.whatsapp && !draft.email && draft.contactCaptureStatus !== "refused") {
    return { field: "contactCaptureStatus", message: `Para deixar esse diagnostico salvo para voce, ${draft.name}, me passa um WhatsApp ou email?` };
  }
  if (!draft.activeStudentsRange) return { field: "activeStudentsRange", message: "Hoje seu studio tem mais ou menos quantos alunos ativos?" };
  if (!draft.operationalPains) {
    return { field: "operationalPains", message: "Quais partes mais dao trabalho hoje: WhatsApp, agenda/reposicoes, vendas, financeiro ou acompanhamento dos alunos?" };
  }
  return { field: "dailyVisibility", message: "Hoje voce consegue ver facilmente o que precisa ser resolvido no dia?" };
}

function isDemoRequest(request: AiAttendantRequest) {
  const text = normalizedConversationText(request);
  return /(demo|demonstracao|ver funcionando|ver o sistema funcionando|mostrar funcionando)/i.test(text);
}

function isBroadRoutineOnly(request: AiAttendantRequest) {
  const text = conversationText(request)
    .normalize("NFD")
    .replace(/\p{Diacritic}/gu, "");
  const broad = /\b(rotina|organizar|melhorar|studio|estudio|pilates|processo|operacao|bagunca|baguncado)\b/i.test(text);
  const specific = /\b(whatsapp|agenda|agendamento|reposicao|reposicoes|falta|faltas|aluno|alunos|venda|vendas|lead|leads|financeiro|cobranca|cobrancas|renovacao|renovacoes|marketing|instagram)\b/i.test(text);

  return broad && !specific;
}

function isBroadMultiAreaNeed(request: AiAttendantRequest) {
  const text = conversationText(request)
    .normalize("NFD")
    .replace(/\p{Diacritic}/gu, "");
  const areaPatterns = [
    /\b(whatsapp|atendimento|mensagem|mensagens)\b/i,
    /\b(agenda|agendamento|reposicao|reposicoes|falta|faltas)\b/i,
    /\b(venda|vendas|lead|leads|interessado|interessados)\b/i,
    /\b(financeiro|cobranca|cobrancas|mensalidade|renovacao|renovacoes)\b/i,
  ];
  const matchedAreas = areaPatterns.filter((pattern) => pattern.test(text)).length;
  return matchedAreas >= 3 && /\b(organizar tudo|tudo|baguncad|completo|operacao toda|studio todo)\b/i.test(text);
}

function isCustomAgentConversion(conversionPath: AiAttendantResponse["conversionPath"]) {
  return (
    conversionPath === "custom_agent_follow_up" ||
    conversionPath === "mixed_subscription_plus_custom" ||
    conversionPath === "custom_agent_diagnostic_mapped" ||
    conversionPath === "custom_agent_diagnostic_unclear"
  );
}

function hasCustomAgentIntent(request: AiAttendantRequest) {
  if (request.quickReplyId === "custom_agent_interest") return true;
  if (request.session.entryPath === "custom_agent_diagnostic") return true;

  const text = conversationText(request);
  return /(agente sob medida|sob medida|marketing|instagram|campanha|campanhas|anuncio|anuncios|trafego|conteudo|parceria|parcerias|estoque|rh|contratacao|fora dos agentes|nao existe|não existe|novo agente)/i.test(text);
}

function conversationText(request: AiAttendantRequest) {
  return [
    request.userMessage,
    request.quickReplyId,
    ...request.session.messages.slice(-4).map((message) => message.content),
  ]
    .filter(Boolean)
    .join(" ")
    .toLowerCase();
}

function normalizedConversationText(request: AiAttendantRequest) {
  return conversationText(request)
    .normalize("NFD")
    .replace(/\p{Diacritic}/gu, "");
}

function currentMessageText(request: AiAttendantRequest) {
  return [request.userMessage, request.quickReplyId].filter(Boolean).join(" ");
}

function hasContactInCurrentMessage(request: AiAttendantRequest) {
  const text = currentMessageText(request);
  return /[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}/i.test(text) || /(?:\+?55\s*)?(?:\(?\d{2}\)?\s*)?\d{4,5}[-\s]?\d{4}/.test(text);
}

function normalizeText(value: string) {
  return value
    .toLowerCase()
    .normalize("NFD")
    .replace(/\p{Diacritic}/gu, "");
}

function ensureContactCapture(
  response: AiAttendantResponse,
  request: AiAttendantRequest,
  intent: "human_whatsapp_handoff" | "custom_agent_follow_up",
) {
  if (hasContact(request) || asksForContact(response)) return response;

  const prompt =
    intent === "custom_agent_follow_up"
      ? "Para transformar isso em proposta, qual WhatsApp ou email voce prefere deixar?"
      : "Para eu encaminhar com o contexto certo, qual WhatsApp ou email voce prefere deixar?";

  const assistantMessages = [...response.assistantMessages, createAssistantMessage(prompt, intent)];

  return {
    ...response,
    assistantMessages,
    nextQuestion: response.nextQuestion ?? prompt,
  };
}

function hasContact(request: AiAttendantRequest) {
  return Boolean(
    request.session.externalContact?.phone ||
      request.session.qualificationDraft?.whatsapp ||
      request.session.qualificationDraft?.email,
  );
}

function asksForContact(response: AiAttendantResponse) {
  const text = response.assistantMessages.map((message) => message.content).join(" ").toLowerCase();
  const asksEmailOrPhone =
    /\b(email|e-mail|telefone|celular)\b/.test(text) &&
    /\b(qual|deixa|deixar|passa|passar|envia|enviar|usar|retornar|retorno|prefere)\b/.test(text);
  const asksWhatsapp =
    /\bwhatsapp\b/.test(text) &&
    /\b(qual whatsapp|deixa|deixar|passa|passar|envia|enviar|usar para|retornar|retorno|prefere)\b/.test(text);

  return asksEmailOrPhone || asksWhatsapp;
}

function mergeCsv(current: string | undefined, values: string[]) {
  return Array.from(new Set([...(current ? current.split(",").map((item) => item.trim()) : []), ...values].filter(Boolean))).join(", ");
}
