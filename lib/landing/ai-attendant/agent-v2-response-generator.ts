import type { AiAttendantRequest, AiAttendantResponse, QualificationDraft } from "./schema";
import { createAssistantMessage } from "./schema";
import type { AgentV2ConversationState, AgentV2Interpretation, AgentV2OrchestrationDecision } from "./agent-v2-types";
import type { ProductKnowledge } from "./product-knowledge-source";
import { buildDiagnosticOutput, nextDiagnosticQuestion } from "./agent-v2-diagnostic";
import { hardCapFallbackText } from "./agent-v2-cost-policy";
import { firstName } from "./agent-v2-identity";

export function generateAgentV2Response({
  request,
  state,
  interpretation,
  decision,
  product,
}: {
  request: AiAttendantRequest;
  state: AgentV2ConversationState;
  interpretation: AgentV2Interpretation;
  decision: AgentV2OrchestrationDecision;
  product: ProductKnowledge;
}): AiAttendantResponse | null {
  const facts = mergeKnownFactsForTurn(state, interpretation, request);
  Object.assign(facts, inferWaitlistDetailsFromCurrentMessage(request, facts));
  const basePatch: QualificationDraft = {
    commercialStage: mapMacroToCommercialStage(decision.stateTransition),
    waitlistStatus: mapWaitlistStatus(decision.stateTransition, request.session.qualificationDraft?.waitlistStatus),
    whatsapp: request.session.externalContact?.phone ?? facts.whatsappPhone,
    email: facts.email,
    contactPreference: request.session.externalContact?.phone ?? facts.whatsappPhone ?? facts.email,
    name: facts.personName,
    primaryPainOrIntent: facts.mainPainOrIntent,
    biggestPain: facts.mainPainOrIntent,
    operationalPains: facts.mainPainOrIntent,
    currentSystem: facts.currentWorkflowOrTool,
    studioName: facts.studioName,
    cityState: facts.cityState,
    studioCity: facts.cityState,
    studioSizeRange: facts.activeStudents,
    activeStudentsRange: facts.activeStudents,
    priorityGoal: facts.priorityToMakeLighter,
    buyingTiming: facts.urgency,
    agentV2ProductSourceVersion: product.version,
  };

  if (decision.selectedAction === "opening") {
    return response({
      messages: openingMessages(request, facts.personName),
      nextQuestion: "Em que posso te ajudar?",
      patch: { ...basePatch, nextAction: "Entender dor, dúvida ou intenção antes de oferecer diagnóstico." },
    });
  }

  if (decision.selectedAction === "answer_direct") {
    return response({
      messages: withFirstTurnGreeting(
        request,
        facts.personName,
        answerDirectQuestions(interpretation, product, Boolean(request.session.qualificationDraft?.diagnosticCompleted === "true"), state),
      ),
      nextQuestion: nextAfterDirectQuestion(interpretation, request),
      patch: {
        ...basePatch,
        diagnosticStatus: request.session.qualificationDraft?.diagnosticStatus ?? "not_started",
        nextAction: "Pergunta direta respondida; seguir pelo caminho escolhido pelo lead.",
      },
      conversionPath: interpretation.directQuestions.includes("plans") && !interpretation.directQuestions.includes("plan_recommendation") ? "view_plans" : undefined,
    });
  }

  if (decision.selectedAction === "offer_diagnostic") {
    return response({
      messages: withFirstTurnGreeting(request, facts.personName, [
        "Claro, posso te ajudar com isso sim.",
        "A melhor forma de entender como a Taliya ficaria no seu studio é fazer um diagnóstico rápido da rotina.",
        "Eu te faço algumas perguntas simples e, no final, te devolvo um caminho claro.",
        "Pode ser?",
      ]),
      nextQuestion: "Pode ser?",
      patch: {
        ...basePatch,
        diagnosticStatus: "offered",
        nextAction: "Aguardar aceite para iniciar diagnóstico gratuito.",
      },
    });
  }

  if (decision.selectedAction === "continue_diagnostic") {
    const next = nextDiagnosticQuestion({ ...state.substate, knownFacts: facts });
    if (!next) return null;
    return response({
      messages: [acknowledgeFact(interpretation), next.question].filter(Boolean),
      nextQuestion: next.question,
      patch: {
        ...basePatch,
        commercialStage: "diagnostic_in_progress",
        diagnosticStatus: "in_progress",
        diagnosticType: "crm_agent_diagnostic",
        diagnosticAskedFields: addAskedField(request.session.qualificationDraft?.diagnosticAskedFields, next.step),
        nextAction: "Continuar diagnóstico com perguntas necessárias, sem repetir fatos conhecidos.",
      },
    });
  }

  if (decision.selectedAction === "deliver_diagnostic") {
    const diagnostic = buildDiagnosticOutput(facts);
    return response({
      messages: [
        "Perfeito, já consigo te devolver uma leitura inicial.",
        diagnostic.mainBottleneck,
        diagnostic.likelyOperationalCause,
        diagnostic.operationalImpact,
        diagnostic.firstOrganizationStep,
        ...diagnostic.indicatedAgents.map((agent, index) => explainAgent(agent, facts.mainPainOrIntent, facts.priorityToMakeLighter, index)),
        diagnostic.validationQuestion,
      ],
      nextQuestion: diagnostic.validationQuestion,
      patch: {
        ...basePatch,
        commercialStage: "diagnostic_completed",
        diagnosticStatus: "completed",
        diagnosticCompleted: "true",
        diagnosticCompletedAt: new Date().toISOString(),
        diagnosticSummary: diagnostic.mainBottleneck,
        recommendedAgents: diagnostic.indicatedAgents.join(", "),
        recommendedPlan: diagnostic.planOrPlanRangeToCompare,
        diagnosticNextStep: diagnostic.validationQuestion,
        nextAction: "Aguardar validação positiva antes de oferecer lista de espera.",
      },
      conversionPath: "crm_agent_diagnostic",
    });
  }

  if (decision.selectedAction === "offer_waitlist") {
    return response({
      messages: [
        `Boa${facts.personName ? `, ${firstName(facts.personName)}` : ""}. Faz sentido começar por aí mesmo.`,
        ...product.availability.waitlistCopy.split("\n\n"),
        "Quer que eu deixe registrado?",
      ],
      nextQuestion: "Quer que eu deixe registrado?",
      patch: {
        ...basePatch,
        commercialStage: "waitlist_offered",
        waitlistStatus: "offered",
        waitlistOfferedAt: new Date().toISOString(),
        nextAction: "Aguardar aceite explicito para lista de espera.",
      },
      conversionPath: "waitlist_intent",
    });
  }

  if (decision.selectedAction === "collect_waitlist_details") {
    const missing = missingWaitlistFields(request, facts);
    if (missing.length === 0) {
      return response({
        messages: [
          "Perfeito, deixei seu studio na lista.",
          "Quando abrir uma próxima janela, chamamos por esse contato.",
          "Ficou alguma dúvida, pode ficar à vontade pra perguntar.",
        ],
        patch: {
          ...basePatch,
          commercialStage: "waitlist_joined",
          waitlistStatus: "joined",
          waitlistJoinedAt: new Date().toISOString(),
          missingWaitlistFields: "",
          closureState: "waitlist_joined",
          nextAction: "Studio na lista de espera; responder dúvidas sem reiniciar fluxo.",
        },
        conversionPath: "waitlist_intent",
      });
    }
    const question = waitlistQuestion(missing, request.session.channel === "whatsapp");
    const sideAnswer = waitlistPendingSideAnswer(request, interpretation, product);
    return response({
      messages: [
        ...sideAnswer,
        sideAnswer.length ? "Para deixar registrado certinho, ainda falta um detalhe." : "Perfeito. Para registrar certinho, só falta um detalhe.",
        question,
      ],
      nextQuestion: question,
      patch: {
        ...basePatch,
        commercialStage: "waitlist_pending_details",
        waitlistStatus: "pending_details",
        missingWaitlistFields: missing.join(","),
        nextAction: "Coletar dados faltantes para tornar a lista de espera acionável.",
      },
      conversionPath: "waitlist_intent",
    });
  }

  if (decision.selectedAction === "answer_post_waitlist") {
    return response({
      messages: answerPostWaitlist(request, interpretation, product),
      nextQuestion: "Quer tirar mais alguma dúvida enquanto seu studio fica na lista?",
      patch: {
        ...basePatch,
        commercialStage: "waitlist_joined",
        waitlistStatus: "joined",
        closureState: "waiting_user",
        nextAction: "Responder dúvidas pós-lista sem reiniciar diagnóstico ou lista.",
      },
      conversionPath: "waitlist_intent",
    });
  }

  if (decision.selectedAction === "capture_name") {
    return response({
      messages: [`Prazer, ${firstName(facts.personName ?? "")}.`, "Em que posso te ajudar?"],
      nextQuestion: "Em que posso te ajudar?",
      patch: {
        ...basePatch,
        commercialStage: "awaiting_pain_or_intent",
        nextAction: "Nome capturado; aguardar dor, dúvida ou intenção do lead.",
      },
    });
  }

  if (decision.selectedAction === "handoff_human") {
    return response({
      messages: ["Claro. Vou deixar uma pessoa assumir daqui.", "Também deixo o contexto salvo para você não precisar repetir tudo."],
      patch: {
        ...basePatch,
        commercialStage: "human_handoff",
        humanActive: "requested",
        aiPaused: "true",
        closureState: "human_active",
        nextAction: "Lead pediu humano; IA pausada até retomada explícita.",
      },
      conversionPath: "human_whatsapp_assist",
    });
  }

  if (decision.selectedAction === "cost_cap_fallback") {
    return response({
      messages: hardCapFallbackText().split("\n\n"),
      patch: {
        ...basePatch,
        aiPaused: "true",
        humanActive: "requested",
        closureState: "error_needs_attention",
        nextAction: "Limite de custo atingido; operador deve retornar assim que possível.",
      },
    });
  }

  if (decision.selectedAction === "unsupported_media") {
    return response({
      messages: [
        "Recebi o arquivo, mas por aqui preciso que você me mande o ponto principal em texto para eu não interpretar errado.",
        "Se preferir, também posso deixar para uma pessoa olhar.",
      ],
      patch: { ...basePatch, nextAction: "Aguardar resumo em texto ou handoff humano para mídia." },
    });
  }

  if (decision.selectedAction === "safe_refusal") {
    return response({
      messages: ["Não consigo ajudar com isso.", "Posso seguir com dúvidas sobre a Taliya, planos, diagnóstico ou funcionamento no WhatsApp."],
      patch: { ...basePatch, nextAction: "Risco recusado; voltar para contexto Taliya." },
    });
  }

  if (decision.selectedAction === "legacy_fallback") {
    const demoFollowUp = demoFollowUpResponse(request.userMessage, state);
    if (demoFollowUp.length) {
      return response({
        messages: demoFollowUp,
        nextQuestion: demoFollowUp[demoFollowUp.length - 1],
        patch: {
          ...basePatch,
          commercialStage: "demo_seen",
          nextAction: "Responder dúvida sobre demo sem empurrar lista ou reiniciar diagnóstico.",
        },
      });
    }

    const researching = researchingResponse(request.userMessage);
    if (researching.length) {
      return response({
        messages: researching,
        nextQuestion: researching[researching.length - 1],
        patch: {
          ...basePatch,
          commercialStage: "awaiting_pain_or_intent",
          nextAction: "Lead pesquisando; responder com calma e abrir caminhos sem pressão.",
        },
      });
    }

    const objection = objectionResponse(request.userMessage);
    if (objection.length) {
      return response({
        messages: objection,
        nextQuestion: objection[objection.length - 1],
        patch: {
          ...basePatch,
          commercialStage: "awaiting_pain_or_intent",
          nextAction: "Objeção respondida; seguir para contexto da rotina sem reiniciar fluxo.",
        },
      });
    }

    const standaloneName = standaloneNameFromCurrentMessage(request.userMessage, state);
    if (standaloneName) {
      return response({
        messages: [`Prazer, ${firstName(standaloneName)}.`, "Em que posso te ajudar?"],
        nextQuestion: "Em que posso te ajudar?",
        patch: {
          ...basePatch,
          name: standaloneName,
          commercialStage: "awaiting_pain_or_intent",
          nextAction: "Nome capturado; aguardar dor, dúvida ou intenção do lead.",
        },
      });
    }
    if (interpretation.factsExtracted.personName && !state.substate.knownFacts.mainPainOrIntent) {
      return response({
        messages: [`Prazer, ${firstName(interpretation.factsExtracted.personName)}.`, "Em que posso te ajudar?"],
        nextQuestion: "Em que posso te ajudar?",
        patch: {
          ...basePatch,
          commercialStage: "awaiting_pain_or_intent",
          nextAction: "Nome capturado; aguardar dor, dúvida ou intenção do lead.",
        },
      });
    }
    return response({
      messages: [
        "Entendi.",
        "Me conta um pouco mais sobre o que você quer resolver no studio: atendimento, agenda, vendas, financeiro ou organização da rotina?",
      ],
      nextQuestion: "Qual parte da rotina você quer entender melhor?",
      patch: {
        ...basePatch,
        nextAction: "Fallback v2: pedir contexto sem acionar agente legado.",
      },
    });
  }

  return null;
}

function mergeKnownFactsForTurn(
  state: AgentV2ConversationState,
  interpretation: AgentV2Interpretation,
  request: AiAttendantRequest,
) {
  const known = state.substate.knownFacts;
  const extracted = interpretation.factsExtracted;
  const facts = {
    ...known,
    ...extracted,
  };

  if (known.mainPainOrIntent && extracted.mainPainOrIntent) {
    facts.mainPainOrIntent = known.mainPainOrIntent;
    const text = normalize(request.userMessage ?? "");
    if (!facts.priorityToMakeLighter && /\b(aliviar|leve|primeiro|prioridade|complicado|resolver)\b/.test(text)) {
      facts.priorityToMakeLighter = extracted.mainPainOrIntent;
    }
  }

  return facts;
}

function response({
  messages,
  nextQuestion,
  patch,
  conversionPath,
}: {
  messages: string[];
  nextQuestion?: string;
  patch: QualificationDraft;
  conversionPath?: AiAttendantResponse["conversionPath"];
}): AiAttendantResponse {
  return {
    assistantMessages: messages.map((message) => createAssistantMessage(message, conversionPath === "waitlist_intent" ? "waitlist_intent" : "answer_question")),
    capturedPainIds: [],
    recommendedAgentIds: parseAgents(patch.recommendedAgents),
    recommendations: undefined,
    nextQuestion,
    conversionPath,
    shouldOfferDiagnostic: patch.diagnosticStatus !== "completed",
    qualificationPatch: patch,
    guardrailDecision: {
      category: "allowed",
      action: "respond",
      reason: "Agent v2 layered response.",
    },
  };
}

function openingMessages(request: AiAttendantRequest, knownName?: string) {
  if (request.session.channel === "whatsapp" && knownName) return [`Oi, ${firstName(knownName)}. Tudo bem?`, "Em que posso te ajudar?"];
  return ["Oi! Tudo bem?", "Em que posso te ajudar?"];
}

function withFirstTurnGreeting(request: AiAttendantRequest, knownName: string | undefined, messages: string[]) {
  if (request.session.messages.length > 0) return messages;
  return [...openingMessages(request, knownName).slice(0, 1), ...messages];
}

function answerDirectQuestions(
  interpretation: AgentV2Interpretation,
  product: ProductKnowledge,
  hasDiagnostic: boolean,
  state: AgentV2ConversationState,
) {
  const messages: string[] = [];
  if (interpretation.directQuestions.includes("price") || interpretation.directQuestions.includes("plans") || interpretation.directQuestions.includes("plan_recommendation")) {
    const planList = product.plans.map((plan) => `${plan.name}: ${formatPrice(plan.priceMonthlyBrl)}/mês`).join("; ");
    messages.push("Hoje a Taliya tem quatro faixas de plano, começando em R$ 197/mês.");
    messages.push("A diferença principal é o quanto você quer automatizar agora: só organizar a base, começar com 1 agente, conectar 3 rotinas ou usar o sistema completo.");
    messages.push(`Os valores são: ${planList}.`);
    if (interpretation.directQuestions.includes("plan_recommendation") && !hasDiagnostic) {
      messages.push("Para recomendar com segurança, eu prefiro entender um pouco da rotina antes. Se fizer sentido, posso recomendar pelo diagnóstico gratuito.");
    } else {
      if (!hasDiagnostic) messages.push("Se quiser uma recomendação, eu faço pelo diagnóstico gratuito para entender a rotina antes.");
      messages.push(`Se preferir ver direto, o comparativo fica aqui: ${product.links.plans}`);
    }
  }
  if (interpretation.directQuestions.includes("demo")) {
    if (state.substate.lastAnsweredDirectQuestion === "demo") {
      messages.push("Na prática, a Taliya começa organizando a base do studio: alunos, agenda, conversas e pendências em um só lugar.");
      messages.push("Depois disso, os agentes entram em rotinas específicas, como atendimento, reposições, vendas ou financeiro, sempre com a equipe no controle.");
      messages.push("Se quiser, faço um diagnóstico rápido para te mostrar qual parte faria mais sentido ver primeiro.");
    } else {
      messages.push(`A demonstração oficial fica aqui: ${product.links.demonstration}.`);
      messages.push("Se preferir, também posso te explicar o fluxo por aqui antes de você abrir a página.");
    }
  }
  if (interpretation.directQuestions.includes("product")) {
    messages.push("A Taliya é um CRM para studios de Pilates, com IA para ajudar em atendimento, agenda, vendas, financeiro e acompanhamento dos alunos.");
  }
  if (interpretation.directQuestions.includes("whatsapp")) {
    messages.push("No WhatsApp, a ideia é a equipe continuar no controle, com a Taliya organizando contexto, histórico e respostas da rotina.");
  }
  if (interpretation.directQuestions.includes("guarantee")) {
    messages.push(product.commercialPolicies.guaranteeCancellation ?? "Ainda não tenho uma regra comercial confirmada para garantia/cancelamento. Posso deixar para uma pessoa confirmar.");
  }
  if (interpretation.directQuestions.includes("privacy")) {
    messages.push(`A Taliya deve guardar apenas dados necessários para operar a rotina e atendimento. Política de privacidade: ${product.links.privacy}`);
  }
  if (interpretation.directQuestions.includes("uncertainty")) {
    messages.push("Quando a IA não tiver segurança, ela não deve inventar. O certo é pedir contexto ou passar para a equipe.");
  }
  if (!messages.length) messages.push("Claro, te ajudo com isso.");
  return compactDirectMessages(messages, interpretation);
}

function nextAfterDirectQuestion(interpretation: AgentV2Interpretation, request: AiAttendantRequest) {
  if (request.session.qualificationDraft?.diagnosticCompleted === "true") return "Quer que eu abra o comparativo de planos?";
  if (interpretation.directQuestions.includes("plan_recommendation")) return "Quer fazer esse diagnóstico gratuito para eu recomendar com mais segurança?";
  if (interpretation.directQuestions.includes("price") || interpretation.directQuestions.includes("plans")) return "Quer ver o comparativo direto ou prefere que eu recomende pelo diagnóstico gratuito?";
  if (interpretation.directQuestions.includes("demo")) return "Quer que eu explique por aqui ou prefere abrir a demonstração?";
  return "Isso responde sua dúvida ou tem alguma parte da rotina que você quer entender melhor?";
}

function compactDirectMessages(messages: string[], interpretation: AgentV2Interpretation) {
  if (interpretation.directQuestions.length <= 1) return messages.slice(0, 5);
  const compacted: string[] = [];
  for (const message of messages) {
    if (message.includes("A diferença principal") && interpretation.directQuestions.includes("demo")) continue;
    compacted.push(message);
  }
  return compacted.slice(0, 5);
}

function bridgePain(pain?: string) {
  if (!pain) return "Certo.";
  if (/vendas|interessados/i.test(pain)) return "Certo. Quando interessados ficam soltos, muita oportunidade esfria antes de virar aluno.";
  if (/whatsapp/i.test(pain) && /agenda|repos/i.test(pain)) return "Boa. Atendimento e agenda costumam destravar bastante coisa quando passam a trabalhar juntos.";
  if (/agenda|repos/i.test(pain)) return "Faz sentido. Reposição e agenda costumam pesar quando tudo depende de conversa e memória da equipe.";
  if (/whatsapp/i.test(pain)) return "Boa. Quando o WhatsApp concentra tudo, fica fácil perder contexto e próximo passo.";
  return "Certo. Dá para olhar isso com calma.";
}

function acknowledgeFact(interpretation: AgentV2Interpretation) {
  if (interpretation.factsExtracted.activeStudents) return "Boa, isso já me dá uma noção do tamanho da operação.";
  if (interpretation.factsExtracted.currentWorkflowOrTool) return "Certo, então hoje isso ainda fica nesse controle.";
  if (interpretation.factsExtracted.mainPainOrIntent) return bridgePain(interpretation.factsExtracted.mainPainOrIntent);
  if (interpretation.factsExtracted.painSpecificDetail) return "Ok, isso mostra onde a rotina ainda fica vulnerável.";
  if (interpretation.factsExtracted.priorityToMakeLighter) return bridgePain(interpretation.factsExtracted.priorityToMakeLighter);
  if (interpretation.factsExtracted.urgency) return "Perfeito, isso ajuda a entender o momento.";
  if (interpretation.primaryIntent === "diagnostic_accept") return "Perfeito. Vou começar pelo tamanho do studio.";
  return "";
}

function explainAgent(agent: string, pain?: string, priority?: string, index = 0) {
  const context = `${pain ?? ""} ${priority ?? ""}`;
  const normalizedAgent = normalize(agent);
  if (normalizedAgent.includes("agenda")) {
    return [
      index === 0 ? "O primeiro agente que faz sentido aqui é o de Agenda." : "Também olharia o agente de Agenda.",
      "Ele organiza faltas, reposições e horários disponíveis para a equipe não depender de caderno, memória ou conversa antiga.",
      "Na prática, fica mais claro quem precisa repor, quando pode repor e o que ainda está pendente.",
    ].join(" ");
  }
  if (normalizedAgent.includes("vendas")) {
    return [
      "Também olharia o agente de Vendas.",
      "Ele entra quando interessados esfriam por demora no retorno ou falta de acompanhamento.",
      "A ideia é cada interessado ter um próximo passo claro, em vez de ficar perdido entre mensagens, planilha e memória da equipe.",
    ].join(" ");
  }
  if (normalizedAgent.includes("atendimento")) {
    return [
      "Também faz sentido olhar o agente de Atendimento.",
      "Ele ajuda quando o WhatsApp concentra dúvidas, pedidos repetidos e retornos que a equipe precisa lembrar de fazer.",
      "Na prática, organiza o contexto da conversa e ajuda a não deixar pedido importante passar batido.",
    ].join(" ");
  }
  if (normalizedAgent.includes("financeiro")) {
    return [
      "Para a parte financeira, o agente de Financeiro pode entrar como apoio.",
      "Ele faz sentido quando cobranças, mensalidades, atrasos ou renovações começam a consumir tempo da equipe.",
      "Na prática, a rotina fica menos dependente de conferência manual e mais fácil de acompanhar.",
    ].join(" ");
  }
  if (normalizedAgent.includes("gestao")) {
    return [
      "Eu também colocaria Gestão como apoio.",
      "Ele transforma a rotina do dia em prioridades visíveis, principalmente quando várias frentes dependem da memória da equipe.",
      "Na prática, fica mais claro o que precisa de atenção primeiro e o que pode esperar.",
    ].join(" ");
  }
  return [
    `Também olharia o agente de ${agent}.`,
    context.trim()
      ? "Ele entra para organizar uma parte específica da rotina que apareceu no diagnóstico."
      : "Ele entra para organizar uma parte específica da rotina do studio.",
    "A ideia é reduzir trabalho manual e deixar próximo passo mais claro para a equipe.",
  ].join(" ");
}

function missingWaitlistFields(request: AiAttendantRequest, facts: Record<string, unknown>) {
  const missing: string[] = [];
  if (!facts.studioName && !request.session.qualificationDraft?.studioName) missing.push("studio");
  if (!facts.cityState && !request.session.qualificationDraft?.cityState && !request.session.qualificationDraft?.studioCity) missing.push("cidade");
  if (request.session.channel !== "whatsapp" && !facts.whatsappPhone && !facts.email && !request.session.qualificationDraft?.whatsapp && !request.session.qualificationDraft?.email) {
    missing.push("contato");
  }
  return missing;
}

function inferWaitlistDetailsFromCurrentMessage(request: AiAttendantRequest, facts: Record<string, unknown>) {
  const draft = request.session.qualificationDraft;
  const isWaitlistCollection =
    draft?.waitlistStatus === "pending_details" ||
    draft?.commercialStage === "waitlist_pending_details" ||
    draft?.waitlistStatus === "offered";
  if (!isWaitlistCollection) return {};

  const text = (request.userMessage ?? "").trim();
  if (!text) return {};

  const inferred: { studioName?: string; cityState?: string } = {};
  const missingStudio = !facts.studioName && !draft?.studioName;
  const missingCity = !facts.cityState && !draft?.cityState && !draft?.studioCity;
  const commaParts = text.split(",").map((part) => cleanWaitlistPart(part)).filter(Boolean);

  if (missingStudio && missingCity && commaParts.length >= 2) {
    inferred.studioName = normalizeStudioName(commaParts[0]);
    inferred.cityState = commaParts.slice(1).join(", ");
    return inferred;
  }

  const placeMatch = text.match(/^\s*(.+?)\s+(?:em|de)\s+([\p{L}\s.'-]{2,60})\s*$/iu);
  if (missingStudio && missingCity && placeMatch) {
    inferred.studioName = normalizeStudioName(placeMatch[1]);
    inferred.cityState = cleanWaitlistPart(placeMatch[2]);
    return inferred;
  }

  if (missingCity && !missingStudio && text.length <= 80) inferred.cityState = cleanWaitlistPart(text);
  if (missingStudio && !missingCity && text.length <= 80) inferred.studioName = normalizeStudioName(text);
  return inferred;
}

function cleanWaitlistPart(value: string) {
  return value.trim().replace(/\s+/g, " ").replace(/[.。]+$/g, "");
}

function normalizeStudioName(value: string) {
  return cleanWaitlistPart(value).replace(/^(?:o\s+|a\s+)?(?:studio|estudio|stúdio)\s+(?:do|da|de)?\s*/i, "");
}

function waitlistQuestion(missing: string[], isWhatsApp: boolean) {
  if (missing.includes("studio") && missing.includes("cidade")) return "Qual é o nome do studio e de qual cidade ele é?";
  if (missing.includes("studio")) return "Qual é o nome do studio?";
  if (missing.includes("cidade")) return "De qual cidade é o studio?";
  if (missing.includes("contato") && !isWhatsApp) return "Qual WhatsApp ou email você prefere deixar para chamarmos?";
  return "Qual detalhe falta para eu deixar registrado certinho?";
}

function answerPostWaitlist(request: AiAttendantRequest, interpretation: AgentV2Interpretation, product: ProductKnowledge) {
  const text = normalize(request.userMessage ?? "");
  if (/\b(obrigad|valeu|perfeito|show|beleza)\b/.test(text)) {
    return ["Imagina. Ficou alguma dúvida? Pode ficar à vontade, estou à disposição por aqui."];
  }
  if (/\b(quando|quanto tempo|prazo|chama|chamado|proxima janela|próxima janela)\b/.test(text)) {
    return [
      "Ainda não tenho uma data fechada para chamar todos os studios.",
      "A ideia é abrir novas janelas aos poucos, para conseguir acompanhar bem cada implantação.",
      "Quando chegar a vez do seu studio, chamamos por aqui.",
    ];
  }
  const direct = answerDirectQuestions(interpretation, product, true, {
    version: "agent-v2",
    conversationId: request.session.sessionId,
    channel: request.session.channel === "whatsapp" ? "whatsapp" : "widget",
    macroState: "waitlist_joined",
    priority: "waitlist_ready",
    humanStatus: "none",
    updatedAt: new Date().toISOString(),
    substate: {
      askedQuestions: [],
      knownFacts: {},
      pendingQuestion: null,
      diagnosticStep: null,
      missingFields: [],
      lastTopic: null,
      lastAnsweredDirectQuestion: null,
      sentiment: "neutral",
      confidence: "medium",
      lastSummary: null,
      queuedResponseStatus: "none",
      cost: { estimatedConversationCostUsd: 0, capStatus: "ok" },
    },
  });
  if (direct.length && direct[0] !== "Claro, te ajudo com isso.") {
    return direct.slice(0, 4);
  }
  return ["Claro. Me manda sua dúvida que eu te respondo por aqui."];
}

function waitlistPendingSideAnswer(request: AiAttendantRequest, interpretation: AgentV2Interpretation, product: ProductKnowledge) {
  const text = normalize(request.userMessage ?? "");
  if (looksLikeWaitlistDetailMessage(request.userMessage)) return [];
  if (/\b(quando|quanto tempo|prazo|chama|chamado|proxima janela|proxima janela)\b/.test(text)) {
    return [
      "Ainda não tenho uma data fechada para chamar todos os studios.",
      "A ideia é abrir novas janelas aos poucos, para conseguir acompanhar bem cada implantação.",
    ];
  }
  if (interpretation.directQuestions.length) {
    return answerDirectQuestions(interpretation, product, true, {
      version: "agent-v2",
      conversationId: request.session.sessionId,
      channel: request.session.channel === "whatsapp" ? "whatsapp" : "widget",
      macroState: "waitlist_pending_details",
      priority: "waitlist_ready",
      humanStatus: "none",
      updatedAt: new Date().toISOString(),
      substate: {
        askedQuestions: [],
        knownFacts: {},
        pendingQuestion: null,
        diagnosticStep: null,
        missingFields: [],
        lastTopic: null,
        lastAnsweredDirectQuestion: null,
        sentiment: "neutral",
        confidence: "medium",
        lastSummary: null,
        queuedResponseStatus: "none",
        cost: { estimatedConversationCostUsd: 0, capStatus: "ok" },
      },
    }).slice(0, 4);
  }
  return [];
}

function mapMacroToCommercialStage(macro: AgentV2OrchestrationDecision["stateTransition"]): QualificationDraft["commercialStage"] {
  if (macro === "diagnostic_offered") return "diagnostic_offered";
  if (macro === "diagnostic_in_progress") return "diagnostic_in_progress";
  if (macro === "diagnostic_completed") return "diagnostic_completed";
  if (macro === "waitlist_offered") return "waitlist_offered";
  if (macro === "waitlist_pending_details") return "waitlist_pending_details";
  if (macro === "waitlist_joined") return "waitlist_joined";
  if (macro === "human_requested" || macro === "human_active") return "human_handoff";
  return "awaiting_pain_or_intent";
}

function mapWaitlistStatus(macro: AgentV2OrchestrationDecision["stateTransition"], current?: QualificationDraft["waitlistStatus"]): QualificationDraft["waitlistStatus"] {
  if (macro === "waitlist_offered") return "offered";
  if (macro === "waitlist_pending_details") return "pending_details";
  if (macro === "waitlist_joined") return "joined";
  return current ?? "not_offered";
}

function addAskedField(existing: string | undefined, field: string) {
  return Array.from(new Set([...(existing ? existing.split(",") : []), field].map((item) => item.trim()).filter(Boolean))).join(",");
}

function parseAgents(value?: string) {
  return value ? value.split(",").map((item) => item.trim().toLowerCase()).filter(Boolean) : [];
}

function formatPrice(value: number) {
  return `R$ ${value.toLocaleString("pt-BR")}`;
}

function normalize(value: string) {
  return value
    .toLowerCase()
    .normalize("NFD")
    .replace(/\p{Diacritic}/gu, "");
}

function looksLikeWaitlistDetailMessage(message: string | undefined) {
  const text = message?.trim();
  if (!text) return false;
  const normalized = normalize(text);
  return (
    /\b(studio|estudio|stúdio)\b/.test(normalized) ||
    text.includes(",") ||
    /\b(vitoria|vila velha|serra|cariacica|sao paulo|rio de janeiro|belo horizonte)\b/.test(normalized)
  );
}

function objectionResponse(message: string | undefined) {
  const text = normalize(message ?? "");
  if (/\b(caro|valor alto|muito caro|studio pequeno|estudio pequeno|pequeno)\b/.test(text)) {
    return [
      "Faz sentido olhar o valor com cuidado.",
      "Para um studio menor, não precisa começar pelo sistema completo. O ponto é entender se existe uma dor clara que já justifica organizar melhor a rotina.",
      "Se quiser, faço um diagnóstico rápido para ver se faz sentido agora ou se é melhor esperar.",
    ];
  }
  if (/\b(tecnofit|nextfit|sistema|ja uso|já uso)\b/.test(text) && /\b(por que|porque|pra que|para que|usaria|trocar|diferenca|diferença)\b/.test(text)) {
    return [
      "Se você já usa um sistema, a Taliya não precisa entrar como mais uma ferramenta solta.",
      "A pergunta principal é onde ainda sobra trabalho manual: WhatsApp, reposições, interessados, financeiro ou prioridades do dia.",
      "Qual parte ainda pesa mesmo com o sistema atual?",
    ];
  }
  return [];
}

function researchingResponse(message: string | undefined) {
  const text = normalize(message ?? "");
  if (!/\b(pesquisando|so pesquisando|só pesquisando|vendo ainda|entendendo ainda|sem pressa)\b/.test(text)) return [];
  return [
    "Sem pressa.",
    "Posso te responder direto sobre planos, demo ou funcionamento da Taliya.",
    "Se quiser uma leitura mais útil, também posso fazer um diagnóstico rápido só para entender se faz sentido agora.",
  ];
}

function demoFollowUpResponse(message: string | undefined, state: AgentV2ConversationState) {
  if (state.substate.lastAnsweredDirectQuestion !== "demo") return [];
  const text = normalize(message ?? "");
  if (!/\b(duvida|duvidas|nao sei|fiquei em duvida|nao entendi|confuso|confusa|nao ficou claro)\b/.test(text)) return [];
  return [
    "Tranquilo, não vou te jogar para lista nem plano sem isso ficar claro.",
    "A demo serve para mostrar a rotina funcionando: base do studio, agenda, conversas e próximos passos.",
    "Qual parte ficou mais em dúvida: atendimento, agenda, vendas ou implantação?",
  ];
}

function standaloneNameFromCurrentMessage(message: string | undefined, state: AgentV2ConversationState) {
  const text = message?.trim();
  if (!text) return undefined;
  if (state.macroState === "diagnostic_in_progress" || state.macroState === "diagnostic_completed" || state.macroState.startsWith("waitlist") || state.macroState.startsWith("human")) return undefined;
  if (!/^[\p{L}][\p{L}\s.'-]{1,48}$/u.test(text)) return undefined;
  const normalized = normalize(text);
  if (/\b(oi|ola|olá|opa|bom dia|boa tarde|boa noite|agenda|reposicao|reposicoes|whatsapp|planos?|preco|valor|demo|diagnostico|vendas|financeiro|studio|pilates|alunos?|caderno|planilha|sim|nao|ok|pode|quero|preciso)\b/.test(normalized)) return undefined;
  return text.split(/\s+/).length <= 3 ? text : undefined;
}
