import type { NicheLandingConfig } from "@/data/landing/niches/types";
import type { AiAttendantRequest, AiAttendantResponse, GuardrailDecision } from "./schema";
import { createAssistantMessage } from "./schema";

export function createFallbackResponse(config: NicheLandingConfig, decision: GuardrailDecision, request?: AiAttendantRequest): AiAttendantResponse {
  const fallbackMessages = config.floatingAgent.fallbackMessages;
  const content =
    decision.visibleMessage ??
    (decision.category === "prompt_injection"
      ? fallbackMessages.promptInjection
      : decision.category === "sensitive_data"
        ? fallbackMessages.sensitiveData
        : decision.category === "off_topic"
        ? fallbackMessages.offTopic
        : decision.category === "rate_limited"
          ? createRateLimitedMessage(request, fallbackMessages.rateLimited)
          : fallbackMessages.providerFailure);

  return {
    assistantMessages: [createAssistantMessage(content, decision.action === "respond" ? "answer_question" : "fallback")],
    capturedPainIds: [],
    recommendedAgentIds: [],
    shouldOfferDiagnostic: false,
    guardrailDecision: {
      ...decision,
      action: decision.action === "respond" ? "respond" : "fallback",
    },
  };
}

function createRateLimitedMessage(request: AiAttendantRequest | undefined, fallback: string) {
  if (!request) return fallback;

  const previousMessages = request.session.messages ?? [];
  const assistantTurns = previousMessages.filter((message) => message.role === "assistant").length;
  const userTurns = previousMessages.filter((message) => message.role === "user").length + (request.userMessage ? 1 : 0);
  const draft = request.session.qualificationDraft ?? {};
  const hasUsefulContext = Boolean(
    draft.name ||
      draft.primaryPainOrIntent ||
      draft.operationalPains ||
      draft.diagnosticStatus ||
      request.session.selectedPainIds?.length ||
      request.session.recommendedAgentIds?.length,
  );

  if (assistantTurns === 0 && userTurns <= 1 && !hasUsefulContext) {
    return "Estou com uma fila alta por aqui agora. Deixa sua mensagem que eu retorno assim que possivel.";
  }

  return "A conversa ficou salva. Preciso pausar por alguns minutos para nao responder pela metade, mas retorno assim que possivel por aqui.";
}

export function createGuidedOpeningResponse(config: NicheLandingConfig): AiAttendantResponse {
  return {
    assistantMessages: [createAssistantMessage(config.floatingAgent.greeting, "answer_question")],
    capturedPainIds: [],
    recommendedAgentIds: [],
    shouldOfferDiagnostic: false,
    guardrailDecision: {
      category: "allowed",
      action: "respond",
      reason: "Opening greeting.",
    },
  };
}

export function createGuidedFallbackTurn(config: NicheLandingConfig, request: AiAttendantRequest, decision: GuardrailDecision): AiAttendantResponse {
  const text = `${request.userMessage ?? ""} ${request.quickReplyId ?? ""}`.toLowerCase();
  const checkoutIntent = /(quero assinar|quero comprar|quero contratar|posso assinar|assinar agora|comprar agora|fechar agora|quero fechar|me manda.*link|link.*pag|quase fechando|fechando o|comecar agora|começar agora)/i.test(text) || request.quickReplyId === "checkout_intent";
  const planComparison = /(quanto custa|preco|preço|valor|planos|comparar|plano)/i.test(text) || request.quickReplyId === "view_plans" || request.quickReplyId === "ask_price";
  const explicitPlanComparison = /(quero ver.*plano|ver os planos|ver planos|comparar|comparativo|pagina de planos|página de planos)/i.test(text) || request.quickReplyId === "view_plans";
  const priceObjection = /(achei caro|esta caro|tá caro|ta caro|muito caro|caro demais|nao cabe|não cabe|sem orcamento|sem orçamento|preco alto|preço alto)/i.test(text);
  const guidedDemo = /(demo|demonstracao|demonstração|ver funcionando|funcionando|como funciona na pratica|como funciona na prática|mostrar funcionando|antes de falar de plano)/i.test(text) || request.quickReplyId === "guided_demo";
  const human = /(humano|pessoa|whatsapp|atendente)/i.test(text) || request.quickReplyId === "human_whatsapp_assist";
  const whatsappSetupQuestion = /(whatsapp business|whatsapp pessoal|whatsapp normal|n.mero pessoal|mesmo n.mero|n.mero do studio|conectar whatsapp|preciso.*whatsapp|exige.*whatsapp|business app)/i.test(text);
  const analysis = /(analise|analise|diagnostico|diagnóstico|raio-x|dinheiro na mesa)/i.test(text) || request.quickReplyId === "analysis_request";
  const customAgent = /(marketing|agente sob medida|campanha|fora dos agentes)/i.test(text) || request.quickReplyId === "custom_agent_interest";
  const productQuestion = /(o que|como funciona|sistema|chatbot|crm)/i.test(text) || request.quickReplyId === "ask_product";
  const afterSubscribing = /(depois que eu assino|apos assinar|após assinar|depois da assinatura|quando eu assinar|quando assino)/i.test(text);
  const unknownIntegration = /(integra|integracao|integração|sistema de gestao|sistema de gestão|sistema x|meu sistema)/i.test(text);
  const completeSystemNeed = /(sistema completo|todos os agentes|7 agentes|sete agentes|tudo funcionando|atendimento.*agenda.*financeiro|agenda.*vendas.*financeiro|varias rotinas|várias dores)/i.test(text);
  const trialQuestion = /(teste gratis|teste grátis|trial|testar gratis|testar grátis|periodo gratis|período grátis)/i.test(text);
  const planFitQuestion = /(qual plano|plano faz sentido|plano indicado|plano recomendado|recomenda.*plano|comecar com qual|começar com qual)/i.test(text);
  const explicitPlanMention = /(7 agentes|sete agentes|3 agentes|tres agentes|três agentes|1 agente|um agente|base|plano recomendado|plano indicado|esse plano)/i.test(text);
  const broadRoutineQuestion = /\b(rotina|organizar|melhorar|studio|estudio|pilates|processo|operacao|bagunca|baguncado)\b/i.test(text);
  const receptionistObjection = /\b(recepcionista|secretaria|atendente|equipe)\b/i.test(text) && /\b(ja tenho|tenho|precisaria|por que|porque)\b/i.test(text);
  const trustObjection = /\b(medo|nao confio|n.o confio|responder errado|resposta errada|controle|assumir|aprovar)\b/i.test(text);
  const detectedPain = config.floatingAgent.painOptions.find((pain) => pain.keywords.some((keyword) => text.includes(keyword.toLowerCase())));
  const mapping = detectedPain ? config.floatingAgent.painToAgents.find((item) => item.painId === detectedPain.id) : undefined;

  if (checkoutIntent) {
    const plan = config.subscription.plans.find((item) => item.id === config.subscription.recommendedPlanId) ?? config.subscription.plans[0];

    if (explicitPlanMention && /(link|quero fechar|fechar|plano recomendado|plano indicado|esse plano)/i.test(text)) {
      return {
        assistantMessages: [
          createAssistantMessage(
            `Perfeito. Vou considerar o ${plan.name} como plano recomendado. A assinatura deve acontecer em checkout seguro, fora do chat, e o plano so ativa depois da confirmacao de pagamento. Eu nao coleto dados de cartao por aqui.`,
            "checkout_intent",
          ),
        ],
        capturedPainIds: request.session.selectedPainIds ?? [],
        recommendedAgentIds: request.session.recommendedAgentIds ?? [],
        conversionPath: "checkout_intent",
        subscription: {
          planId: plan.id,
          ctaLabel: config.floatingAgent.conversionCtas.checkoutIntent.label,
        },
        shouldOfferDiagnostic: false,
        guardrailDecision: decision,
      };
    }

    if (explicitPlanMention && /(medo|configurar errado|ia responder errado|quase fechando|fechando o)/i.test(text)) {
      return {
        assistantMessages: [
          createAssistantMessage(
            `Faz sentido tirar essa duvida antes de fechar. O ${plan.name} tem setup self-guided em poucos minutos com suporte 24/7 pelo consultor, usa limites configurados por studio e humanos continuam podendo controlar ou assumir quando necessario. A assinatura segue por checkout seguro fora do chat; aqui eu nao peco dados de pagamento.`,
            "checkout_intent",
          ),
        ],
        capturedPainIds: request.session.selectedPainIds ?? [],
        recommendedAgentIds: request.session.recommendedAgentIds ?? [],
        conversionPath: "checkout_intent",
        subscription: {
          planId: plan.id,
          ctaLabel: config.floatingAgent.conversionCtas.checkoutIntent.label,
        },
        shouldOfferDiagnostic: false,
        guardrailDecision: decision,
      };
    }

    return {
      assistantMessages: [
        createAssistantMessage(
            `Da para seguir para assinatura, sim. Antes disso, eu confirmaria se o ${plan.name} e mesmo o melhor encaixe para o seu studio. A assinatura acontece fora do chat, em um destino seguro, sem dados de cartao aqui. Quer que eu compare o plano recomendado com os outros antes de avancar?`,
          "plan_recommendation",
        ),
      ],
      capturedPainIds: request.session.selectedPainIds ?? [],
      recommendedAgentIds: request.session.recommendedAgentIds ?? [],
      conversionPath: "plan_recommendation",
      subscription: {
        planId: plan.id,
        ctaLabel: config.floatingAgent.conversionCtas.viewPlans.label,
      },
      shouldOfferDiagnostic: true,
      guardrailDecision: decision,
    };
  }

  if (afterSubscribing) {
    return {
      assistantMessages: [
        createAssistantMessage(
          "Depois da assinatura, o plano so ativa com pagamento confirmado. Em seguida voce recebe o caminho de onboarding para criar a conta, cadastrar o studio e configurar os agentes com suporte 24/7. Antes disso, o ideal e escolher o plano com calma para nao pagar por algo desalinhado.",
          "answer_question",
        ),
      ],
      capturedPainIds: request.session.selectedPainIds ?? [],
      recommendedAgentIds: request.session.recommendedAgentIds ?? [],
      nextQuestion: "Quer que eu te ajude a escolher o plano pela sua rotina?",
      shouldOfferDiagnostic: false,
      guardrailDecision: decision,
    };
  }

  if (trialQuestion) {
    const canHandoffNow = canHandoffFromFallback(request);
    return {
      assistantMessages: [
        createAssistantMessage(
          config.floatingAgent.guidedDemoReady
            ? "Hoje nao vamos trabalhar com trial publico gratuito. Para reduzir risco, existe garantia de 14 dias quando configurada e a demonstracao guiada real mostra a Taliya funcionando antes de voce decidir."
            : "Hoje nao vamos trabalhar com trial publico gratuito. Para reduzir risco, existe garantia de 14 dias quando configurada; enquanto a demo real nao esta ativa, posso te explicar o fluxo ou continuar pelo WhatsApp com contexto.",
          "guided_demo",
        ),
      ],
      capturedPainIds: request.session.selectedPainIds ?? [],
      recommendedAgentIds: request.session.recommendedAgentIds ?? [],
      conversionPath: config.floatingAgent.guidedDemoReady && hasCompletedDiagnostic(request) ? "guided_demo" : canHandoffNow ? "human_whatsapp_assist" : undefined,
      shouldOfferDiagnostic: !config.floatingAgent.guidedDemoReady,
      guardrailDecision: decision,
    };
  }

  if (guidedDemo) {
    const canHandoffNow = canHandoffFromFallback(request);
    return {
      assistantMessages: [
        createAssistantMessage(
          config.floatingAgent.guidedDemoReady
            ? "Posso abrir uma demonstracao guiada da Taliya com um fluxo real de studio. Ela mostra configuracao, agente atuando, registro no sistema e onde voce continua para escolher o plano."
            : "A demonstracao guiada entra quando o ambiente real da Taliya estiver pronto para mostrar esse fluxo sem simular produto. Por enquanto posso explicar o funcionamento ou continuar pelo WhatsApp com contexto.",
          "guided_demo",
        ),
      ],
      capturedPainIds: request.session.selectedPainIds ?? [],
      recommendedAgentIds: request.session.recommendedAgentIds ?? [],
      conversionPath: config.floatingAgent.guidedDemoReady && hasCompletedDiagnostic(request) ? "guided_demo" : canHandoffNow ? "human_whatsapp_assist" : undefined,
      shouldOfferDiagnostic: !config.floatingAgent.guidedDemoReady,
      guardrailDecision: decision,
    };
  }

  if (whatsappSetupQuestion) {
    return {
      assistantMessages: [
        createAssistantMessage(
          "Para usar os agentes no WhatsApp do studio, o numero precisa estar no WhatsApp Business. Se hoje ele esta no WhatsApp pessoal, o caminho seguro e migrar para Business ou separar um numero do studio antes de ativar mensagens. Se esse numero mistura vida pessoal e alunos, eu recomendaria nao conectar ainda para evitar conversas pessoais no painel, equipe, logs ou automacoes.",
          "answer_question",
        ),
      ],
      capturedPainIds: request.session.selectedPainIds ?? [],
      recommendedAgentIds: request.session.recommendedAgentIds ?? [],
      nextQuestion: "Hoje o WhatsApp que os alunos usam ja e um numero separado do studio?",
      shouldOfferDiagnostic: true,
      guardrailDecision: decision,
    };
  }

  if (human) {
    const canHandoffNow = canHandoffFromFallback(request);
    return {
      assistantMessages: [
        createAssistantMessage(
          canHandoffNow
            ? "Posso te encaminhar para um humano no WhatsApp com um resumo seguro do que voce contou."
            : "Posso te encaminhar para um humano no WhatsApp, mas para nao chegar sem contexto eu preciso deixar um diagnostico curto ou um contato salvo primeiro.",
          "human_whatsapp_handoff",
        ),
      ],
      capturedPainIds: request.session.selectedPainIds ?? [],
      recommendedAgentIds: request.session.recommendedAgentIds ?? [],
      conversionPath: canHandoffNow ? "human_whatsapp_assist" : undefined,
      nextQuestion: canHandoffNow ? undefined : "Qual WhatsApp ou email voce prefere deixar para a equipe continuar?",
      shouldOfferDiagnostic: true,
      guardrailDecision: decision,
    };
  }

  if (unknownIntegration) {
    return {
      assistantMessages: [
        createAssistantMessage("Eu nao vou te prometer essa integracao sem confirmar antes.", "answer_question"),
        createAssistantMessage(
          "O que posso confirmar agora e o fluxo principal da Taliya: atendimento, agenda, vendas, financeiro, retencao, gestao e historico.",
          "answer_question",
        ),
        createAssistantMessage("Se essa integracao for decisiva, vale mapear com um consultor antes.", "answer_question"),
        createAssistantMessage("Essa integracao e obrigatoria para comecar ou voce quer primeiro ver o fluxo principal da Taliya?", "answer_question"),
      ],
      capturedPainIds: request.session.selectedPainIds ?? [],
      recommendedAgentIds: request.session.recommendedAgentIds ?? [],
      nextQuestion: "Essa integracao e obrigatoria para comecar ou voce quer primeiro ver o fluxo principal da Taliya?",
      shouldOfferDiagnostic: true,
      guardrailDecision: decision,
    };
  }

  if (customAgent) {
    return {
      assistantMessages: [
        createAssistantMessage("Marketing fica fora do time principal desta landing, entao entra como Agente sob medida.", "custom_agent_follow_up"),
        createAssistantMessage(
          "Para eu entender se vale proposta sob medida, me conta qual rotina de marketing voce quer automatizar: posts, campanhas, DMs, comentarios ou outra coisa?",
          "custom_agent_follow_up",
        ),
      ],
      capturedPainIds: ["agente_sob_medida"],
      recommendedAgentIds: [],
      conversionPath: "custom_agent_follow_up",
      nextQuestion: "Qual rotina de marketing voce quer automatizar primeiro?",
      shouldOfferDiagnostic: true,
      guardrailDecision: decision,
    };
  }

  if (analysis) {
    return {
      assistantMessages: [
        createAssistantMessage(
          "A analise da operacao ajuda a entender quais agentes fazem mais sentido antes de assinar. Posso te mandar para esse caminho com o contexto da conversa.",
          "analysis_handoff",
        ),
      ],
      capturedPainIds: request.session.selectedPainIds ?? [],
      recommendedAgentIds: request.session.recommendedAgentIds ?? [],
      conversionPath: "analysis_request",
      shouldOfferDiagnostic: true,
      guardrailDecision: decision,
    };
  }

  if (completeSystemNeed) {
    return {
      assistantMessages: [
        createAssistantMessage(
          "Pelo que voce descreveu, tem varias frentes conectadas: atendimento, agenda, vendas ou financeiro. Antes de indicar plano, eu faria um diagnostico curto para separar o que a Taliya precisa organizar primeiro e quais agentes realmente ajudam.",
          "answer_question",
        ),
      ],
      capturedPainIds: request.session.selectedPainIds ?? [],
      recommendedAgentIds: request.session.recommendedAgentIds ?? [],
      nextQuestion: "Hoje onde a bagunca pesa mais: atendimento, agenda, vendas ou financeiro?",
      shouldOfferDiagnostic: true,
      guardrailDecision: decision,
    };
  }

  if (trustObjection) {
    return {
      assistantMessages: [
        createAssistantMessage("Justo. A IA nao pode sair respondendo qualquer coisa.", "answer_question"),
        createAssistantMessage("A Taliya trabalha com regras do studio, respostas aprovadas e pode chamar uma pessoa quando tiver duvida.", "answer_question"),
        createAssistantMessage("Seu maior medo e resposta errada no WhatsApp ou agenda baguncada?", "answer_question"),
      ],
      capturedPainIds: request.session.selectedPainIds ?? [],
      recommendedAgentIds: request.session.recommendedAgentIds ?? [],
      nextQuestion: "Seu maior medo e resposta errada no WhatsApp ou agenda baguncada?",
      shouldOfferDiagnostic: true,
      guardrailDecision: decision,
    };
  }

  if (receptionistObjection) {
    return {
      assistantMessages: [
        createAssistantMessage("Faz sentido ter recepcionista. A ideia nao e trocar sua equipe.", "answer_question"),
        createAssistantMessage("A Taliya ajuda nas tarefas repetidas, como responder duvidas, lembrar aluno e organizar pedido de reposicao.", "answer_question"),
        createAssistantMessage("Hoje sua recepcao perde mais tempo com WhatsApp ou agenda?", "answer_question"),
      ],
      capturedPainIds: request.session.selectedPainIds ?? [],
      recommendedAgentIds: request.session.recommendedAgentIds ?? [],
      nextQuestion: "Hoje sua recepcao perde mais tempo com WhatsApp ou agenda?",
      shouldOfferDiagnostic: true,
      guardrailDecision: decision,
    };
  }

  if (priceObjection) {
    return {
      assistantMessages: [
        createAssistantMessage(
          "Entendo. Eu nao tentaria justificar pelo preco isolado.",
          "answer_question",
        ),
        createAssistantMessage("O ponto e olhar a rotina: horarios vazios, interessados sem retorno, cobrancas e trabalho manual.", "answer_question"),
        createAssistantMessage("Se quiser continuar com calma, qual WhatsApp ou email voce prefere deixar?", "answer_question"),
      ],
      capturedPainIds: request.session.selectedPainIds ?? [],
      recommendedAgentIds: request.session.recommendedAgentIds ?? [],
      nextQuestion: "Se quiser continuar com calma, qual WhatsApp ou email voce prefere deixar?",
      shouldOfferDiagnostic: true,
      guardrailDecision: decision,
    };
  }

  if (planFitQuestion && detectedPain && mapping) {
    const plan =
      config.subscription.plans.find((item) => item.id === (mapping.agentIds.length <= 2 ? "one_agent" : "three_agents")) ??
      config.subscription.plans.find((item) => item.id === config.subscription.recommendedPlanId) ??
      config.subscription.plans[0];

    return {
      assistantMessages: [
        createAssistantMessage(
          `Para ${detectedPain.label.toLowerCase()}, o ${plan.name} pode entrar como comparacao depois do diagnostico, porque e uma dor mais concentrada. Antes de indicar plano, preciso entender tamanho do studio e como essa rotina acontece hoje.`,
          "answer_question",
        ),
      ],
      capturedPainIds: [detectedPain.id],
      recommendedAgentIds: mapping.agentIds,
      recommendations: [mapping],
      nextQuestion: mapping.nextQuestion,
      shouldOfferDiagnostic: true,
      guardrailDecision: decision,
    };
  }

  if (planComparison) {
    const planList = config.subscription.plans.map((plan) => `${plan.name}: ${plan.monthlyPriceLabel}`).join("; ");
    const recommendedPlan = config.subscription.plans.find((plan) => plan.id === config.subscription.recommendedPlanId);
    if (!explicitPlanComparison) {
      return {
        assistantMessages: [
          createAssistantMessage(
          `Hoje os planos configurados sao ${planList}. Eu consigo te passar isso, mas prefiro nao recomendar nada no escuro: voce quer resolver uma dor especifica ou organizar atendimento, agenda, vendas e financeiro juntos?`,
            "answer_question",
          ),
        ],
        capturedPainIds: request.session.selectedPainIds ?? [],
        recommendedAgentIds: request.session.recommendedAgentIds ?? [],
        nextQuestion: "Voce quer resolver uma dor especifica ou organizar atendimento, agenda, vendas e financeiro juntos?",
        shouldOfferDiagnostic: true,
        guardrailDecision: decision,
      };
    }
    if (hasCompletedDiagnostic(request)) {
      return {
        assistantMessages: [
          createAssistantMessage(
            `Claro. Com o diagnostico feito, posso abrir o comparativo com Base, Essencial, Avance e Completo. Pelo que ja apareceu, use essa recomendacao como filtro para comparar sem pular direto para assinatura.`,
            "view_plans",
          ),
        ],
        capturedPainIds: request.session.selectedPainIds ?? [],
        recommendedAgentIds: request.session.recommendedAgentIds ?? [],
        conversionPath: "view_plans",
        subscription: {
          planId: request.session.qualificationDraft?.recommendedPlan ?? recommendedPlan?.id ?? config.subscription.recommendedPlanId,
          ctaLabel: config.floatingAgent.conversionCtas.viewPlans.label,
        },
        shouldOfferDiagnostic: false,
        guardrailDecision: decision,
      };
    }
    return {
      assistantMessages: [
        createAssistantMessage(
          `Claro. Hoje os planos configurados sao ${planList}. Para escolher sem chute, eu prefiro fazer um diagnostico curto antes de recomendar ${recommendedPlan?.name ?? "um plano"} ou um plano menor.`,
          "answer_question",
        ),
      ],
      capturedPainIds: request.session.selectedPainIds ?? [],
      recommendedAgentIds: request.session.recommendedAgentIds ?? [],
      nextQuestion: "Voce quer resolver uma dor especifica ou organizar atendimento, agenda, vendas e financeiro juntos?",
      shouldOfferDiagnostic: true,
      guardrailDecision: decision,
    };
  }

  if (productQuestion) {
    return {
      assistantMessages: [
        createAssistantMessage(
          "Taliya e a IA do seu studio de Pilates. Ela organiza alunos, conversas, agenda, financeiro, interessados e historico em um so lugar, responde quando faz sentido e ajuda a equipe a enxergar as proximas acoes.",
          "answer_question",
        ),
      ],
      capturedPainIds: request.session.selectedPainIds ?? [],
      recommendedAgentIds: request.session.recommendedAgentIds ?? [],
      nextQuestion: "Hoje voce quer entender o sistema ou quer olhar uma dor especifica da sua rotina?",
      shouldOfferDiagnostic: false,
      guardrailDecision: decision,
    };
  }

  if (broadRoutineQuestion) {
    return {
      assistantMessages: [
        createAssistantMessage(
          "Entendi. Para melhorar a rotina do studio, eu preciso descobrir onde o peso esta maior antes de te empurrar plano. Hoje o que mais trava: atendimento no WhatsApp, agenda/reposicoes, vendas ou financeiro?",
          "answer_question",
        ),
      ],
      capturedPainIds: request.session.selectedPainIds ?? [],
      recommendedAgentIds: request.session.recommendedAgentIds ?? [],
      nextQuestion: "Hoje o que mais trava: atendimento no WhatsApp, agenda/reposicoes, vendas ou financeiro?",
      shouldOfferDiagnostic: true,
      guardrailDecision: decision,
    };
  }

  if (detectedPain && mapping) {
    return {
      assistantMessages: [
        createAssistantMessage(
          `${detectedPain.label} costuma envolver ${mapping.agentIds.join(" + ")}. ${mapping.explanation}${mapping.nextQuestion ? ` ${mapping.nextQuestion}` : ""}`,
          "pain_detected",
        ),
      ],
      capturedPainIds: [detectedPain.id],
      recommendedAgentIds: mapping.agentIds,
      recommendations: [mapping],
      nextQuestion: mapping.nextQuestion,
      shouldOfferDiagnostic: false,
      guardrailDecision: decision,
    };
  }

  return createFallbackResponse(config, decision);
}

function hasCompletedDiagnostic(request: AiAttendantRequest) {
  return request.session.qualificationDraft?.diagnosticCompleted === "true";
}

function canHandoffFromFallback(request: AiAttendantRequest) {
  return hasCompletedDiagnostic(request) && Boolean(request.session.qualificationDraft?.whatsapp || request.session.qualificationDraft?.email || request.session.externalContact?.phone);
}
