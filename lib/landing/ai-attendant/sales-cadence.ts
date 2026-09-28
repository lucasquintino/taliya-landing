import type { NicheLandingConfig } from "@/data/landing/niches/types";
import type { AiAttendantRequest, AiAttendantResponse } from "./schema";
import { buildPlanComparisonSummary, buildPlanPriceSummary } from "./commercial-pricing";
import { createAssistantMessage } from "./schema";

export function enforceHumanSalesCadence(
  response: AiAttendantResponse,
  request: AiAttendantRequest,
  config: NicheLandingConfig,
): AiAttendantResponse {
  if (response.guardrailDecision.category !== "allowed") return response;

  if (isContactOnlyMessage(request)) {
    const qualificationPatch = extractContactPatch(request);

    return {
      ...response,
      assistantMessages: [
        createAssistantMessage("Perfeito, obrigado. Deixei esse contato salvo para continuar depois.", "qualification_started"),
        createAssistantMessage("Agora posso te ajudar sem pressa por aqui.", "answer_question"),
      ],
      nextQuestion: nextQuestionAfterContact(request),
      conversionPath: undefined,
      subscription: undefined,
      handoff: undefined,
      shouldOfferDiagnostic: true,
      qualificationPatch: {
        ...response.qualificationPatch,
        ...qualificationPatch,
      },
    };
  }

  if (
    response.qualificationPatch?.diagnosticType === "crm_agent_diagnostic" &&
    request.session.qualificationDraft?.diagnosticCompleted !== "true" &&
    !shouldAnswerCurrentQuestionBeforeDiagnostic(request)
  ) {
    return response;
  }

  if (isBareHowItWorksQuestion(request)) {
    return withEarlyContactCapture(
      {
        ...response,
        assistantMessages: [
          createAssistantMessage("Funciona assim: voce configura as regras do studio e a Taliya ajuda nas partes repetidas da rotina.", "answer_question"),
          createAssistantMessage("Eles podem ajudar no WhatsApp, agenda, vendas, cobranca e acompanhamento. Voce continua no controle.", "answer_question"),
        ],
        nextQuestion: recentlyExplainedHowItWorks(request)
          ? "Quer que eu foque em WhatsApp, agenda, vendas ou financeiro?"
          : "Qual parte voce quer entender primeiro: WhatsApp, agenda, vendas ou financeiro?",
        conversionPath: undefined,
        subscription: undefined,
        handoff: undefined,
        shouldOfferDiagnostic: false,
      },
      request,
    );
  }

  if (isSpecificPlanQuestion(request)) {
    return withEarlyContactCapture(
      {
        ...response,
        assistantMessages: [
          createAssistantMessage("O plano Essencial e para comecar por uma dor clara, sem tentar organizar tudo de uma vez.", "answer_question"),
          createAssistantMessage("Por exemplo: escolher Agenda para reposicoes e faltas, ou Atendimento para WhatsApp cheio.", "answer_question"),
        ],
        nextQuestion: "Qual rotina voce colocaria primeiro na Taliya?",
        conversionPath: undefined,
        subscription: undefined,
        handoff: undefined,
        shouldOfferDiagnostic: true,
      },
      request,
    );
  }

  if (isCustomMarketingRequest(request)) {
    return {
      ...response,
      assistantMessages: [
        createAssistantMessage("Isso parece uma rotina sob medida, separada dos planos publicos da Taliya.", "custom_agent_follow_up"),
        createAssistantMessage("Me conta o que essa rotina de marketing teria que fazer e qual WhatsApp ou email voce prefere deixar?", "custom_agent_follow_up"),
      ],
      nextQuestion: "Qual WhatsApp ou email voce prefere deixar?",
      conversionPath: "custom_agent_follow_up",
      subscription: undefined,
      handoff: response.handoff,
      shouldOfferDiagnostic: true,
    };
  }

  if (response.conversionPath === "custom_agent_follow_up" && isMappedOperationalContext(request) && !isCustomMarketingRequest(request)) {
    return withEarlyContactCapture(
      {
        ...response,
        conversionPath: undefined,
        subscription: undefined,
        handoff: undefined,
        diagnosticClassification: undefined,
        diagnosticContextVariant: undefined,
        shouldOfferDiagnostic: true,
      },
      request,
    );
  }

  if (response.conversionPath && isInChatOnlyRequest(request) && !hasPlanIntent(request) && !isBuyingText(request)) {
    return withEarlyContactCapture(
      {
        ...response,
        conversionPath: undefined,
        subscription: undefined,
        handoff: undefined,
      },
      request,
    );
  }

  if (isPostSubscriptionQuestion(request)) {
    return withEarlyContactCapture(
      {
        ...response,
        assistantMessages: [
          createAssistantMessage("Depois do pagamento, voce entra no sistema e configura seu studio.", "answer_question"),
          createAssistantMessage("A Taliya te guia nos primeiros passos e ajuda a ajustar as regras das rotinas escolhidas.", "answer_question"),
        ],
        nextQuestion: "Quer entender como fica essa configuracao na pratica?",
        conversionPath: undefined,
        subscription: undefined,
        handoff: undefined,
        shouldOfferDiagnostic: false,
      },
      request,
    );
  }

  if (response.conversionPath === "checkout_intent" && isPlansOnlyRequest(request)) {
    return softenPrematureConversion(
      response,
      "Eu te mostro os planos, sim. Antes de mandar link de assinatura, quero entender o que combina com seu studio.",
      "Quer comparar por tamanho do studio ou pela parte da rotina que mais pesa hoje?",
      true,
      config,
      request,
    );
  }

  if (response.conversionPath === "checkout_intent" && !hasCompletedDiagnostic(request)) {
    return softenPrematureConversion(
      response,
      "Da para seguir para contratacao, sim. Antes de mandar link de assinatura, prefiro fechar o diagnostico para confirmar o plano certo para o seu studio.",
      "Quer terminar o diagnostico comigo agora?",
      false,
      config,
      request,
    );
  }

  if (response.conversionPath === "checkout_intent" && !hasConfirmedPurchaseContext(request)) {
    return softenPrematureConversion(
      response,
      "Da para seguir para assinatura, sim. Antes disso, quero confirmar o plano certo para voce nao pagar por algo desalinhado.",
      "Hoje voce quer resolver uma dor especifica ou organizar o studio como um todo?",
      true,
      config,
      request,
    );
  }

  if (isBroadCompleteSystemNeed(request) && response.conversionPath !== "checkout_intent") {
    return withEarlyContactCapture(
      {
        ...response,
        assistantMessages: [
          createAssistantMessage("Pelo que voce descreveu, a bagunca esta em varias partes do studio.", "answer_question"),
          createAssistantMessage(
            "Antes de falar em plano, eu organizaria isso no diagnostico: quais rotinas pesam mais, onde a Taliya ajuda e so depois qual pacote comparar.",
            "answer_question",
          ),
        ],
        nextQuestion: "Qual dessas frentes pesa mais hoje: atendimento, agenda, vendas ou financeiro?",
        conversionPath: undefined,
        subscription: undefined,
        handoff: undefined,
        shouldOfferDiagnostic: true,
      },
      request,
    );
  }

  if (isKnownPainDiscovery(request) && hasPlanIntent(request) && response.conversionPath !== "checkout_intent") {
    const plan = config.subscription.plans.find((item) => item.id === "one_agent") ?? config.subscription.plans[0];

    return withEarlyContactCapture(
      {
        ...response,
        assistantMessages: [
          createAssistantMessage(`Para uma dor concentrada como reposicao, o ${plan.name} pode ser um caminho de comparacao depois do diagnostico.`, "answer_question"),
          createAssistantMessage(
            "Para nao cravar no escuro, eu olharia tamanho do studio, como a agenda funciona hoje e se isso tambem encosta em WhatsApp ou vendas.",
            "answer_question",
          ),
        ],
        nextQuestion: "Hoje reposicao vira mais troca de mensagem ou falta de horario livre?",
        conversionPath: undefined,
        subscription: undefined,
        handoff: undefined,
        shouldOfferDiagnostic: true,
      },
      request,
    );
  }

  if (isKnownPainDiscovery(request) && !hasPlanIntent(request)) {
    return withEarlyContactCapture(
      {
        ...response,
        assistantMessages: [
          createAssistantMessage(
            "Isso costuma tomar muito tempo mesmo. Reposicao baguncada vira mensagem indo e voltando, horario vazio e aluno esperando resposta.",
            "pain_detected",
          ),
          createAssistantMessage(
            "Aqui o caminho normalmente passa por Agenda e Atendimento: um ajuda com os horarios, o outro entende o pedido no WhatsApp.",
            "pain_detected",
          ),
        ],
        nextQuestion: "Hoje o maior problema e falta em cima da hora ou dificuldade de encaixar horario?",
        conversionPath: undefined,
        subscription: undefined,
        handoff: undefined,
        shouldOfferDiagnostic: true,
      },
      request,
    );
  }

  if (isUnknownIntegrationQuestion(request)) {
    return withEarlyContactCapture(
      {
        ...response,
        assistantMessages: [
          createAssistantMessage("Nao vou te prometer essa integracao sem confirmar antes.", "answer_question"),
          createAssistantMessage("Me diz qual sistema voce usa e o que precisaria conversar com a Taliya.", "answer_question"),
        ],
        nextQuestion: "Esse sistema e obrigatorio para voce comecar?",
        conversionPath: undefined,
        subscription: undefined,
        handoff: undefined,
        shouldOfferDiagnostic: true,
      },
      request,
    );
  }

  if (isColdDiscovery(request)) {
    return withEarlyContactCapture(
      {
        ...response,
        assistantMessages: [
          createAssistantMessage("Entendi. Antes de falar de plano, quero entender onde esta a maior bagunca hoje.", "answer_question"),
          createAssistantMessage("E no WhatsApp, na agenda, nas vendas ou na cobranca?", "answer_question"),
        ],
        nextQuestion: "E no WhatsApp, na agenda, nas vendas ou na cobranca?",
        conversionPath: undefined,
        subscription: undefined,
        handoff: undefined,
        shouldOfferDiagnostic: true,
      },
      request,
    );
  }

  if (response.conversionPath === "view_plans" && isSimplePriceQuestion(request)) {
    const planSummary = buildPlanPriceSummary(config);
    return withEarlyContactCapture(
      {
        ...response,
        assistantMessages: [
          createAssistantMessage(`Hoje temos estes planos: ${planSummary}.`, "answer_question"),
          createAssistantMessage(
            "Se voce quiser, posso recomendar um deles pelo diagnostico gratuito. Se preferir, tambem posso te mostrar o comparativo direto.",
            "answer_question",
          ),
        ],
        nextQuestion: "Qual caminho prefere agora: recomendacao por diagnostico ou comparativo direto?",
        conversionPath: undefined,
        subscription: undefined,
        handoff: undefined,
        shouldOfferDiagnostic: true,
      },
      request,
    );
  }

  if (response.conversionPath !== "checkout_intent" && isPlansOnlyRequest(request) && !hasCompletedDiagnostic(request)) {
    return withEarlyContactCapture(
      {
        ...response,
        assistantMessages: [
          createAssistantMessage(`Claro. Eu te ajudo a comparar os planos: ${buildPlanPriceSummary(config)}.`, "answer_question"),
          createAssistantMessage(buildPlanComparisonSummary(config), "answer_question"),
        ],
        nextQuestion: "Quer que eu abra a pagina de planos ou prefere uma recomendacao por diagnostico gratuito?",
        conversionPath: "view_plans",
        subscription: {
          planId: config.subscription.recommendedPlanId,
          ctaLabel: config.floatingAgent.conversionCtas.viewPlans.label,
        },
        handoff: undefined,
        shouldOfferDiagnostic: true,
      },
      request,
    );
  }

  if (isPriceObjection(request) && response.conversionPath !== "checkout_intent") {
    return withEarlyContactCapture(
      {
        ...response,
        assistantMessages: [
          createAssistantMessage(
            "Entendo. Antes de olhar so o valor, vale comparar com o que hoje se perde em tempo, interessados sem resposta e horarios vazios.",
            "answer_question",
          ),
          createAssistantMessage(
            "Os planos menores podem fazer sentido para uma dor estreita; pacote maior so deve entrar na conversa quando o diagnostico mostrar varias frentes conectadas.",
            "answer_question",
          ),
        ],
        nextQuestion: "Qual perda pesa mais hoje: tempo manual, interessado sem retorno ou horario vazio?",
        conversionPath: undefined,
        subscription: undefined,
        handoff: undefined,
        shouldOfferDiagnostic: true,
      },
      request,
    );
  }

  if (isBasicProductQuestion(request) && !hasPlanIntent(request)) {
    return withEarlyContactCapture(
      {
        ...response,
        assistantMessages: [
          createAssistantMessage("A Taliya e a IA do studio de Pilates: ela acompanha atendimento, agenda, vendas, cobranca e alunos que estao sumindo.", "answer_question"),
          createAssistantMessage("Ela ajuda com WhatsApp, agenda, vendas, cobranca e acompanhamento dos alunos.", "answer_question"),
        ],
        nextQuestion: "Voce quer entender o sistema ou olhar uma dor do seu studio?",
        conversionPath: undefined,
        subscription: undefined,
        handoff: undefined,
        shouldOfferDiagnostic: false,
      },
      request,
    );
  }

  if (isTrustObjection(request) && hasConfirmedPurchaseContext(request) && isBuyingText(request)) {
    return withEarlyContactCapture(
      {
        ...response,
        assistantMessages: [
          createAssistantMessage("Faz sentido tirar essa duvida antes de fechar.", "checkout_intent"),
          createAssistantMessage(
            "A Taliya usa regras do seu studio, respostas aprovadas e pode chamar uma pessoa quando precisar. Se o Completo for mesmo o caminho, a assinatura segue por link seguro de pagamento.",
            "checkout_intent",
          ),
        ],
        nextQuestion: undefined,
        conversionPath: "checkout_intent",
        subscription: {
          planId: config.subscription.recommendedPlanId,
          ctaLabel: config.floatingAgent.conversionCtas.checkoutIntent.label,
        },
        handoff: undefined,
        shouldOfferDiagnostic: true,
      },
      request,
    );
  }

  if (isTrustObjection(request)) {
    return withEarlyContactCapture(
      {
        ...response,
        assistantMessages: [
          createAssistantMessage("Justo. A IA nao pode sair respondendo qualquer coisa.", "answer_question"),
          createAssistantMessage(
            "Ela precisa seguir regras do seu studio, usar respostas aprovadas e chamar uma pessoa quando tiver duvida.",
            "answer_question",
          ),
        ],
        nextQuestion: "Seu maior medo e resposta errada no WhatsApp ou agenda baguncada?",
        conversionPath: undefined,
        subscription: undefined,
        handoff: undefined,
        shouldOfferDiagnostic: true,
      },
      request,
    );
  }

  if (isReceptionistObjection(request)) {
    return withEarlyContactCapture(
      {
        ...response,
        assistantMessages: [
          createAssistantMessage("Faz sentido ter recepcionista. A ideia nao e trocar sua equipe.", "answer_question"),
          createAssistantMessage(
            "A Taliya ajuda nas tarefas repetidas, como responder duvidas, lembrar aluno e organizar pedido de reposicao.",
            "answer_question",
          ),
        ],
        nextQuestion: "Hoje sua recepcao perde mais tempo com WhatsApp ou agenda?",
        conversionPath: undefined,
        subscription: undefined,
        handoff: undefined,
        shouldOfferDiagnostic: true,
      },
      request,
    );
  }

  if (response.conversionPath === "human_whatsapp_assist") {
    const isDemo = isDemoRequest(request);
    const canHandoffNow = hasCompletedDiagnostic(request) && hasContact(request);
    return withEarlyContactCapture(
      {
        ...response,
        assistantMessages: [
          createAssistantMessage(
            isDemo ? "A demonstracao real ainda nao esta pronta. Posso te explicar o fluxo pelo WhatsApp." : "Claro. Posso te encaminhar para continuar pelo WhatsApp.",
            "human_whatsapp_handoff",
          ),
          createAssistantMessage(
            canHandoffNow ? "Como ja tenho contexto do diagnostico, da para seguir com um resumo mais util." : "Antes disso, quero deixar um pouco de contexto para a pessoa nao entrar no escuro.",
            "human_whatsapp_handoff",
          ),
        ],
        nextQuestion: canHandoffNow ? "Quer que eu encaminhe pelo WhatsApp agora?" : "Qual WhatsApp ou email voce prefere deixar para continuar?",
        conversionPath: canHandoffNow ? "human_whatsapp_assist" : undefined,
        subscription: undefined,
        handoff: canHandoffNow ? response.handoff : undefined,
        shouldOfferDiagnostic: true,
      },
      request,
    );
  }

  if (response.conversionPath === "checkout_intent") {
    return withEarlyContactCapture(
      {
        ...response,
        assistantMessages: [
          createAssistantMessage("Perfeito. Vou seguir com o plano recomendado.", "checkout_intent"),
          createAssistantMessage("A assinatura segue por link seguro de pagamento. O plano so ativa depois da confirmacao.", "checkout_intent"),
        ],
        nextQuestion: undefined,
        conversionPath: "checkout_intent",
        subscription: response.subscription ?? {
          planId: config.subscription.recommendedPlanId,
          ctaLabel: config.floatingAgent.conversionCtas.checkoutIntent.label,
        },
        handoff: undefined,
        shouldOfferDiagnostic: true,
      },
      request,
    );
  }

  return withEarlyContactCapture(response, request);
}

function softenPrematureConversion(
  response: AiAttendantResponse,
  content: string,
  nextQuestion: string,
  keepPlanComparison: boolean,
  config: NicheLandingConfig,
  request: AiAttendantRequest,
): AiAttendantResponse {
  return withEarlyContactCapture(
    {
      ...response,
      assistantMessages: [createAssistantMessage(content, keepPlanComparison ? "plan_recommendation" : "answer_question")],
      nextQuestion,
      conversionPath: keepPlanComparison ? "plan_recommendation" : undefined,
      subscription: keepPlanComparison
        ? {
            planId: config.subscription.recommendedPlanId,
            ctaLabel: config.floatingAgent.conversionCtas.viewPlans.label,
          }
        : undefined,
      handoff: undefined,
      shouldOfferDiagnostic: true,
    },
    request,
  );
}

function withEarlyContactCapture(response: AiAttendantResponse, request: AiAttendantRequest): AiAttendantResponse {
  if (!shouldAskContactNow(request, response) || hasContact(request) || asksForContact(response)) return response;

  const assistantMessages = [...response.assistantMessages];
  const contactPrompt = contactPromptFor(request, response);
  assistantMessages.push(createAssistantMessage(contactPrompt, "qualification_started"));

  return {
    ...response,
    assistantMessages,
    nextQuestion: response.nextQuestion ?? "Qual WhatsApp ou email voce prefere deixar?",
  };
}

function contactPromptFor(request: AiAttendantRequest, response: AiAttendantResponse) {
  if (request.session.entryPath === "whatsapp_cta" || response.conversionPath === "human_whatsapp_assist") {
    return "Se quiser continuar por la, qual WhatsApp voce prefere usar?";
  }

  if (response.conversionPath === "custom_agent_follow_up") {
    return "Para eu encaminhar essa proposta com contexto, qual WhatsApp ou email voce prefere deixar?";
  }

  return "Se quiser que eu deixe esse contexto salvo para continuar depois, qual WhatsApp ou email voce prefere deixar?";
}

function isColdDiscovery(request: AiAttendantRequest) {
  const text = currentNormalizedText(request);
  const hasHistory = request.session.messages.some((message) => message.role === "assistant" || message.role === "user");
  const hasContext =
    Boolean(request.pageSignals?.selectedPainId) ||
    Boolean(request.pageSignals?.selectedAgentId) ||
    Boolean(request.pageSignals?.calculatorEstimate) ||
    Boolean(request.session.selectedPainIds?.length) ||
    Boolean(request.session.recommendedAgentIds?.length);
  const broad = /\b(rotina|melhorar|organizar|studio|estudio|pilates|comecar|entender|explicar|sistema)\b/i.test(text);
  const specific = /\b(whatsapp|agenda|reposicao|reposicoes|faltas|vendas|financeiro|cobranca|renovacao|marketing|instagram|alunos|120|80|50)\b/i.test(text);

  return broad && !specific && !hasContext && !hasHistory && !hasPlanIntent(request) && !isBuyingText(request);
}

function shouldAnswerCurrentQuestionBeforeDiagnostic(request: AiAttendantRequest) {
  return (
    isBareHowItWorksQuestion(request) ||
    isSpecificPlanQuestion(request) ||
    isUnknownIntegrationQuestion(request) ||
    isPostSubscriptionQuestion(request) ||
    isSimplePriceQuestion(request) ||
    isPlansOnlyRequest(request) ||
    isPriceObjection(request) ||
    isBasicProductQuestion(request) ||
    isTrustObjection(request) ||
    isReceptionistObjection(request) ||
    isDemoRequest(request) ||
    isCustomMarketingRequest(request)
  );
}

function isSimplePriceQuestion(request: AiAttendantRequest) {
  const text = currentText(request);
  const asksPrice = /\b(quanto custa|pre.o|valor|mensalidade)\b/i.test(text);
  return asksPrice && !/\b(ver|mostrar|abrir|comparar|comparativo|planos)\b/i.test(text) && !isBuyingText(request);
}

function isPriceObjection(request: AiAttendantRequest) {
  const text = currentText(request);
  return /\b(achei caro|esta caro|ta caro|muito caro|caro demais|nao cabe|n.o cabe|sem orcamento|sem or.amento|preco alto|pre.o alto)\b/i.test(text);
}

function isPostSubscriptionQuestion(request: AiAttendantRequest) {
  const text = currentNormalizedText(request);
  return /\b(depois que eu assino|apos assinar|quando eu assinar|depois da assinatura|pos pagamento|depois que pagar)\b/i.test(text);
}

function isDemoRequest(request: AiAttendantRequest) {
  const text = currentText(request);
  return /\b(demo|demonstracao|ver funcionando|ver o sistema funcionando|mostrar funcionando)\b/i.test(text);
}

function isPlansOnlyRequest(request: AiAttendantRequest) {
  const text = currentText(request);
  return /\b(ver|mostrar|abrir|comparar|comparativo)\b.*\b(plano|planos)\b/i.test(text) && !isBuyingText(request);
}

function isKnownPainDiscovery(request: AiAttendantRequest) {
  const text = currentNormalizedText(request);
  return /\b(agenda|agendamento|reposicao|reposicoes|reposi..es|faltas|faltam|horario vazio|horarios vazios|encaixe|remarcar)\b/i.test(text);
}

function isMappedOperationalContext(request: AiAttendantRequest) {
  const text = normalizeText(conversationText(request));
  return /\b(agenda|agendamento|reposicao|reposicoes|faltas|faltam|horario|horarios|encaixe|remarcar|whatsapp|atendimento|financeiro|cobranca|vendas|leads|renovacao|retencao|historico)\b/i.test(text);
}

function isInChatOnlyRequest(request: AiAttendantRequest) {
  const text = currentNormalizedText(request);
  return (
    text.includes("sem me mandar") ||
    text.includes("nao me manda") ||
    text.includes("nao quero ir") ||
    text.includes("aqui mesmo") ||
    text.includes("por aqui") ||
    text.includes("me explica aqui") ||
    text.includes("continua aqui")
  );
}

function isCustomMarketingRequest(request: AiAttendantRequest) {
  const text = currentText(request);
  return /\b(agente|automacao|automatizar)\b/i.test(text) && /\b(marketing|instagram|campanha|campanhas|posts|conteudo)\b/i.test(text);
}

function isBroadCompleteSystemNeed(request: AiAttendantRequest) {
  const text = currentText(request);
  const signals = [
    /\batendimento|whatsapp\b/i,
    /\bagenda|reposi..o|reposicoes|faltas\b/i,
    /\bfinanceiro|cobranca|cobran.as|renovacao|renovacoes\b/i,
    /\bvendas|leads|interessados|matriculas\b/i,
  ];
  const matched = signals.filter((pattern) => pattern.test(text)).length;
  return matched >= 3 && /\b(organizar tudo|tudo|baguncad|completo|studio todo|operacao toda)\b/i.test(text);
}

function hasConfirmedPurchaseContext(request: AiAttendantRequest) {
  const text = conversationText(request);
  const previousPlan = request.session.messages.some(
    (message) => message.intent === "plan_recommendation" || message.intent === "checkout_intent",
  );
  const explicitPlan = /\b(7 agentes|sete agentes|3 agentes|tres agentes|1 agente|um agente|base|plano recomendado|plano indicado|esse plano)\b/i.test(text);

  return previousPlan || explicitPlan;
}

function hasCompletedDiagnostic(request: AiAttendantRequest) {
  return request.session.qualificationDraft?.diagnosticCompleted === "true";
}

function hasPlanIntent(request: AiAttendantRequest) {
  if (request.quickReplyId === "view_plans" || request.quickReplyId === "checkout_intent") return true;
  const text = currentText(request);
  return /\b(plano|planos|pre.o|valor|quanto custa|assinatura|assinar|comparar|comparativo)\b/i.test(text);
}

function isBasicProductQuestion(request: AiAttendantRequest) {
  const text = currentText(request);
  return /\b(o que.*taliya|que (e|eh).*taliya|como funciona.*taliya|o que.*sistema|me explica.*taliya|me explique.*taliya)\b/i.test(text);
}

function isSpecificPlanQuestion(request: AiAttendantRequest) {
  const text = currentNormalizedText(request);
  return /\b(1 agente|um agente|3 agentes|tres agentes|7 agentes|sete agentes|base)\b/.test(text) && /\b(explica|entender|como funciona|melhor|inclui|serve|vale)\b/.test(text);
}

function isUnknownIntegrationQuestion(request: AiAttendantRequest) {
  const text = currentText(request);
  return /\b(integra|integracao|integra..o|sistema x|meu sistema|software que uso|sistema de gestao|sistema de gest.o)\b/i.test(text);
}

function isTrustObjection(request: AiAttendantRequest) {
  const text = currentText(request);
  return /\b(medo|nao confio|n.o confio|responder errado|resposta errada|controle|assumir|aprovar)\b/i.test(text);
}

function isReceptionistObjection(request: AiAttendantRequest) {
  const text = currentText(request);
  return /\b(recepcionista|secretaria|atendente|equipe)\b/i.test(text) && /\b(ja tenho|tenho|precisaria|por que|porque)\b/i.test(text);
}

function isBuyingText(request: AiAttendantRequest) {
  const text = currentText(request);
  return /\b(quero assinar|quero comprar|quero contratar|assinar agora|comprar agora|fechar agora|quase fechando|fechando o|quero fechar|manda.*link|me manda.*link|pagar|pagamento|seguir para assinatura)\b/i.test(text);
}

function shouldAskContactNow(request: AiAttendantRequest, response: AiAttendantResponse) {
  if (hasContact(request)) return false;
  if (!hasUserInterest(request)) return false;
  if (request.session.entryPath === "widget" && !currentText(request)) return false;
  if (request.session.channel === "whatsapp") return true;
  if (request.session.entryPath === "consultor_cta" || request.session.entryPath === "whatsapp_cta") return true;
  if (request.session.entryPath === "plans_page" || request.session.entryPath === "guided_demo" || request.session.entryPath === "custom_agent_diagnostic") return true;
  if (response.conversionPath) return true;
  return false;
}

function hasUserInterest(request: AiAttendantRequest) {
  const text = currentText(request);
  return Boolean(text.trim()) || request.quickReplyId !== undefined;
}

function asksForContact(response: AiAttendantResponse) {
  const text = response.assistantMessages.map((message) => message.content).join(" ").toLowerCase();
  const asksEmailOrPhone =
    /\b(email|e-mail|telefone|celular|contato)\b/.test(text) &&
    /\b(qual|deixa|deixar|passa|passar|envia|enviar|usar|retornar|retorno|prefere|podemos usar)\b/.test(text);
  const asksWhatsapp =
    /\bwhatsapp\b/.test(text) &&
    /\b(qual whatsapp|deixa|deixar|passa|passar|envia|enviar|usar para|prefere|podemos usar)\b/.test(text);

  return asksEmailOrPhone || asksWhatsapp;
}

function hasContact(request: AiAttendantRequest) {
  return Boolean(
    request.session.externalContact?.phone ||
      request.session.qualificationDraft?.whatsapp ||
      request.session.qualificationDraft?.email ||
      request.session.qualificationDraft?.contactPreference ||
      extractContactPatch(request).whatsapp ||
      extractContactPatch(request).email,
  );
}

function currentText(request: AiAttendantRequest) {
  return [request.userMessage, request.quickReplyId].filter(Boolean).join(" ").toLowerCase();
}

function conversationText(request: AiAttendantRequest) {
  return [request.userMessage, request.quickReplyId, ...request.session.messages.slice(-6).map((message) => message.content)]
    .filter(Boolean)
    .join(" ")
    .toLowerCase();
}

function isBareHowItWorksQuestion(request: AiAttendantRequest) {
  const text = normalizeText(currentText(request));
  return /\b(como funciona|como que funciona|me explica|me explique)\b/.test(text) && !hasPlanIntent(request) && !isSpecificPlanQuestion(request) && !isPostSubscriptionQuestion(request);
}

function recentlyExplainedHowItWorks(request: AiAttendantRequest) {
  const recentAssistantText = normalizeText(
    request.session.messages
      .slice(-6)
      .filter((message) => message.role === "assistant")
      .map((message) => message.content)
      .join(" "),
  );

  return /\b(funciona assim|sistema para studios|agentes que ajudam|whatsapp, agenda|agenda, vendas)\b/.test(recentAssistantText);
}

function isContactOnlyMessage(request: AiAttendantRequest) {
  const patch = extractContactPatch(request);
  if (!patch.whatsapp && !patch.email) return false;

  const text = normalizeText(request.userMessage ?? "");
  const withoutContact = text
    .replace(/[a-z0-9._%+-]+@[a-z0-9.-]+\.[a-z]{2,}/gi, "")
    .replace(/\+?\d[\d\s().-]{7,}\d/g, "")
    .replace(/\b(meu|minha|contato|whatsapp|zap|numero|telefone|celular|email|e-mail|e|eh|e:|é|é:|pode chamar|pode mandar|chama nesse|manda nesse)\b/g, "")
    .replace(/[^a-z0-9]/g, "")
    .trim();

  return withoutContact.length <= 10;
}

function extractContactPatch(request: AiAttendantRequest) {
  const text = request.userMessage ?? "";
  const email = text.match(/[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}/i)?.[0];
  const phone = text.match(/(?:\+?55\s?)?(?:\(?\d{2}\)?\s?)?(?:9\s?)?\d{4}[-.\s]?\d{4}/)?.[0];

  return {
    ...(phone ? { whatsapp: phone.trim(), contactPreference: phone.trim() } : {}),
    ...(email ? { email: email.trim().toLowerCase(), contactPreference: email.trim().toLowerCase() } : {}),
  };
}

function nextQuestionAfterContact(request: AiAttendantRequest) {
  const recentText = recentUserTextBeforeCurrent(request);

  if (/\b(preco|valor|quanto custa|plano|planos|assinar|assinatura|comprar|contratar)\b/.test(recentText)) {
    return "Quer que eu te ajude a escolher um plano ou prefere tirar uma duvida antes?";
  }

  if (/\b(reposicao|reposicoes|falta|faltas|agenda|horario|encaixar)\b/.test(recentText)) {
    return "Hoje o mais dificil e encaixar horario ou controlar quem ainda tem direito a reposicao?";
  }

  if (/\b(whatsapp|atendimento|mensagem|responder)\b/.test(recentText)) {
    return "Hoje o WhatsApp pesa mais em responder interessados ou em atender alunos atuais?";
  }

  if (/\b(marketing|instagram|campanha|conteudo)\b/.test(recentText)) {
    return "Essa rotina de marketing cuidaria mais de conteudo, mensagens ou campanhas?";
  }

  return "Quer que eu entenda sua rotina ou explique uma parte especifica do sistema?";
}

function normalizeText(value: string) {
  return value
    .toLowerCase()
    .normalize("NFD")
    .replace(/\p{Diacritic}/gu, "");
}

function currentNormalizedText(request: AiAttendantRequest) {
  return normalizeText(currentText(request));
}

function recentUserTextBeforeCurrent(request: AiAttendantRequest) {
  return normalizeText(
    request.session.messages
      .slice(-8)
      .filter((message) => message.role === "user")
      .map((message) => message.content)
      .join(" "),
  );
}
