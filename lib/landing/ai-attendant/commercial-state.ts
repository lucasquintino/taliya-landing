import type { NicheLandingConfig } from "@/data/landing/niches/types";
import type { AiAttendantRequest, AiAttendantResponse, QualificationDraft, WaitlistStatus } from "./schema";
import { createPricePlanAnswer, isPriceOrPlanQuestion } from "./commercial-pricing";
import { createAssistantMessage } from "./schema";

type CommercialPatch = Pick<
  QualificationDraft,
  | "commercialStage"
  | "waitlistStatus"
  | "waitlistOfferedAt"
  | "waitlistJoinedAt"
  | "waitlistDeclinedAt"
  | "diagnosticStatus"
  | "diagnosticCompletedAt"
  | "demoStatus"
  | "demoOfferedAt"
  | "demoSeenAt"
  | "leadSourceChannel"
  | "leadSourceDetail"
  | "primaryPainOrIntent"
  | "nextAction"
  | "name"
  | "studioName"
  | "cityState"
  | "studioCity"
  | "whatsapp"
  | "contactPreference"
  | "customRoutine"
  | "missingWaitlistFields"
  | "humanActive"
  | "aiPaused"
  | "closureState"
>;

const WAITLIST_NARRATIVE =
  "Estamos trabalhando com um numero pequeno de studios agora.";

export function createHumanizedSalesTurn(
  request: AiAttendantRequest,
  config: NicheLandingConfig,
): AiAttendantResponse | undefined {
  if (request.quickReplyId && request.quickReplyId !== "start_conversation") return undefined;
  if (request.session.qualificationDraft?.diagnosticType === "crm_agent_diagnostic" && request.session.qualificationDraft.diagnosticCompleted !== "true") {
    return undefined;
  }

  const text = request.userMessage?.trim() ?? "";
  if (!text) return undefined;

  const draft = request.session.qualificationDraft ?? {};
  const basePatch = sourcePatch(request);
  const knownName = draft.name;
  const extractedName = !knownName ? extractName(text) : undefined;
  const currentPainOrIntent = extractPainOrIntent(text) ?? draft.primaryPainOrIntent ?? draft.operationalPains ?? draft.biggestPain;
  const current = normalize(text);

  if (draft.waitlistStatus === "joined") {
    const joinedWaitlistTurn = createWaitlistFollowUpTurn(request, config, basePatch);
    if (joinedWaitlistTurn) return joinedWaitlistTurn;
  }

  if (isPriceOrPlanQuestion(request) && !isBuyingIntent(current)) {
    return createPricePlanAnswer({ config, request, reason: "Humanized commercial price/plan answer before context capture." });
  }

  const customOpening = createCustomAgentOpeningTurn(current, basePatch);
  if (customOpening) return customOpening;

  const waitlistFollowUp = createWaitlistFollowUpTurn(request, config, basePatch);
  if (waitlistFollowUp) return waitlistFollowUp;

  const postDemo = createPostDemoTurn(request, basePatch);
  if (postDemo) return postDemo;

  const postDiagnostic = createPostDiagnosticValidationTurn(request, config, basePatch);
  if (postDiagnostic) return postDiagnostic;

  if (draft.diagnosticStatus === "offered" && draft.diagnosticCompleted !== "true" && isPositiveIntent(current)) {
    return undefined;
  }

  if (isHumanRequest(current)) {
    return createHumanHandoffTurn(request, basePatch);
  }

  if (!knownName) {
    return createNameCaptureTurn(request, text, extractedName, currentPainOrIntent, basePatch);
  }

  const contextualTurn = createKnownNameContextualTurn({
    request,
    config,
    text,
    normalized: current,
    knownName,
    currentPainOrIntent,
    basePatch,
  });
  if (contextualTurn) return contextualTurn;

  if (!hasPainOrIntent(draft) && currentPainOrIntent) {
    return createDiagnosticOfferTurn({
      name: knownName,
      painOrIntent: currentPainOrIntent,
      basePatch,
      extraPatch: {},
    });
  }

  if (draft.diagnosticStatus === "offered" && currentPainOrIntent && draft.diagnosticCompleted !== "true") {
    return createDiagnosticOfferTurn({
      name: knownName,
      painOrIntent: currentPainOrIntent,
      basePatch,
      extraPatch: {},
    });
  }

  if (!hasPainOrIntent(draft) && shouldAskPainAfterName(text)) {
    const nextQuestion = "Em que posso ajudar?";
    const opening = request.session.channel === "whatsapp" && isGreetingOnly(current) ? `Oi, ${firstName(knownName)}. Tudo bem?` : `Boa, ${firstName(knownName)}.`;
    return baseResponse({
      messages: [opening, nextQuestion],
      nextQuestion,
      patch: {
        ...basePatch,
        commercialStage: "awaiting_pain_or_intent",
        waitlistStatus: existingWaitlistStatus(draft),
        name: knownName,
        nextAction: "Descobrir dor ou intencao antes de oferecer diagnostico.",
      },
    });
  }

  if (isDemoRequest(text)) {
    return createDemoUnavailableOrOfferedTurn(config, basePatch);
  }

  return undefined;
}

function createKnownNameContextualTurn({
  request,
  config,
  text,
  normalized,
  knownName,
  currentPainOrIntent,
  basePatch,
}: {
  request: AiAttendantRequest;
  config: NicheLandingConfig;
  text: string;
  normalized: string;
  knownName: string;
  currentPainOrIntent: string | undefined;
  basePatch: CommercialPatch;
}): AiAttendantResponse | undefined {
  const draft = request.session.qualificationDraft ?? {};

  const objectionTurn = createCommercialObjectionTurn(normalized, knownName, basePatch);
  if (objectionTurn) return objectionTurn;

  if (isIntegrationQuestion(normalized)) {
    const painOrIntent = "integracao de agenda e rotina";
    const nextQuestion = "Quer que eu faca um diagnostico gratuito para entender esse fluxo antes de te dizer o caminho?";
    return baseResponse({
      messages: [
        "Boa pergunta. Eu nao vou te prometer isso sem confirmar o fluxo.",
        "Para agenda, o ponto e entender se hoje voces dependem do Google Agenda, de outro sistema ou de controle manual.",
        nextQuestion,
      ],
      nextQuestion,
      patch: {
        ...basePatch,
        primaryPainOrIntent: painOrIntent,
        commercialStage: "diagnostic_offered",
        waitlistStatus: "not_offered",
        diagnosticStatus: "offered",
        nextAction: "Validar fluxo de integracao antes de prometer suporte.",
      },
    });
  }

  if (isDemoRequest(text)) {
    return createDemoUnavailableOrOfferedTurn(config, basePatch);
  }

  if (isExistingSystemContext(normalized)) {
    const nextQuestion = "O que esse sistema atual ainda nao resolve bem na rotina?";
    return baseResponse({
      messages: [
        "Boa. Se voce ja tem sistema, a conversa muda um pouco.",
        "A Taliya so faz sentido se aliviar algo que o sistema atual ainda deixa manual, espalhado ou dependente da equipe lembrar.",
        nextQuestion,
      ],
      nextQuestion,
      patch: {
        ...basePatch,
        commercialStage: "awaiting_pain_or_intent",
        waitlistStatus: existingWaitlistStatus(draft),
        name: knownName,
        nextAction: "Entender lacuna do sistema atual antes de oferecer diagnostico.",
      },
    });
  }

  if (isResearchingContext(normalized)) {
    const nextQuestion = "Voce esta comparando mais por valor, funcionamento no WhatsApp, agenda ou controle da rotina?";
    return baseResponse({
      messages: [
        `Sem problema, ${knownName}. Da para olhar com calma.`,
        "O melhor caminho e comparar pelo que pesa na operacao, nao por uma lista generica de recursos.",
        nextQuestion,
      ],
      nextQuestion,
      patch: {
        ...basePatch,
        commercialStage: "awaiting_pain_or_intent",
        waitlistStatus: existingWaitlistStatus(draft),
        name: knownName,
        nextAction: "Entender criterio de pesquisa sem pressionar diagnostico ou lista de espera.",
      },
    });
  }

  if (isReceptionistOpening(normalized)) {
    const painOrIntent = "atendimento e tarefas repetitivas da equipe";
    const nextQuestion = "Quer que eu faca um diagnostico gratuito para ver onde a automacao ajudaria sem tirar o controle da equipe?";
    return baseResponse({
      messages: [
        "Nao. A ideia nao e substituir sua recepcionista.",
        "A Taliya ajuda a equipe com tarefas repetitivas, historico, lembretes e controle do que precisa de resposta.",
        nextQuestion,
      ],
      nextQuestion,
      patch: {
        ...basePatch,
        primaryPainOrIntent: painOrIntent,
        commercialStage: "diagnostic_offered",
        waitlistStatus: "not_offered",
        diagnosticStatus: "offered",
        nextAction: "Oferecer diagnostico depois de esclarecer papel da equipe.",
      },
    });
  }

  if (isQuantifiedManualContext(normalized)) {
    return createDiagnosticOfferTurn({
      name: knownName,
      painOrIntent: currentPainOrIntent ?? "rotina manual com muitos alunos",
      basePatch,
      extraPatch: {
        name: knownName,
      },
    });
  }

  return undefined;
}

function createNameCaptureTurn(
  request: AiAttendantRequest,
  text: string,
  extractedName: string | undefined,
  painOrIntent: string | undefined,
  basePatch: CommercialPatch,
): AiAttendantResponse | undefined {
  const draft = request.session.qualificationDraft ?? {};
  const normalized = normalize(text);

  if (isNameRefusal(normalized) && isDirectQuestion(normalized)) {
    const answer = directQuestionAnswer(normalized);
    const nextQuestion = "Se quiser depois, me fala seu nome que eu consigo deixar a conversa mais organizada.";
    return baseResponse({
      messages: [answer, nextQuestion],
      nextQuestion,
      patch: {
        ...basePatch,
        commercialStage: "awaiting_name",
        waitlistStatus: existingWaitlistStatus(draft),
        nextAction: "Responder duvida direta sem bloquear atendimento e sem oferecer lista de espera.",
      },
    });
  }

  if (isBuyingIntent(normalized)) {
    const nextQuestion = "Qual é o nome do studio e de qual cidade ele é?";
    return baseResponse({
      messages: [
        WAITLIST_NARRATIVE,
        "Se fizer sentido, posso colocar seu studio na lista de espera e chamar assim que abrir uma próxima janela.",
        nextQuestion,
      ],
      nextQuestion,
      patch: {
        ...basePatch,
        commercialStage: "waitlist_pending_details",
        waitlistStatus: "pending_details",
        nextAction: "Lead pediu contratacao; coletar studio e cidade para lista de espera.",
      },
    });
  }

  const webOpeningIntent = createWebOpeningIntentTurn(request, normalized, painOrIntent, basePatch);
  if (webOpeningIntent) return webOpeningIntent;

  const openingIntent = createWhatsAppOpeningIntentTurn(request, normalized, painOrIntent, basePatch);
  if (openingIntent) return openingIntent;

  if (extractedName && painOrIntent) {
    return createDiagnosticOfferTurn({
      name: extractedName,
      painOrIntent,
      basePatch,
      extraPatch: { name: extractedName },
    });
  }

  if (extractedName) {
    const nextQuestion = "Em que posso ajudar?";
    return baseResponse({
      messages: [`Prazer, ${extractedName}.`, nextQuestion],
      nextQuestion,
      patch: {
        ...basePatch,
        name: extractedName,
        commercialStage: "awaiting_pain_or_intent",
        waitlistStatus: existingWaitlistStatus(draft),
        nextAction: "Perguntar dor ou intencao antes do diagnostico.",
      },
    });
  }

  if (isGreetingOnly(normalized) || request.session.channel === "whatsapp") {
    const leadIn = isDirectQuestion(normalized) ? "Claro, te ajudo com isso." : "Oi! Tudo bem?";
    const nextQuestion = "Em que posso ajudar?";
    return baseResponse({
      messages: [leadIn, nextQuestion],
      nextQuestion,
      patch: {
        ...basePatch,
        commercialStage: "awaiting_pain_or_intent",
        waitlistStatus: existingWaitlistStatus(draft),
        nextAction: "Entender dor ou intencao sem capturar nome cedo.",
      },
    });
  }

  return undefined;
}

function createWebOpeningIntentTurn(
  request: AiAttendantRequest,
  normalized: string,
  painOrIntent: string | undefined,
  basePatch: CommercialPatch,
): AiAttendantResponse | undefined {
  if (request.session.channel !== "web") return undefined;
  if (request.session.qualificationDraft?.name) return undefined;
  if (isDemoRequest(normalized) || isDirectQuestion(normalized)) return undefined;
  if (!isLowContextExploration(normalized)) return undefined;

  const nextQuestion = "Qual seu nome?";
  return baseResponse({
    messages: [
      "Claro, te ajudo a entender como a Taliya ficaria no contexto do seu studio.",
      nextQuestion,
    ],
    nextQuestion,
    patch: {
      ...basePatch,
      primaryPainOrIntent: painOrIntent ?? "entender a Taliya no studio",
      commercialStage: "awaiting_name",
      waitlistStatus: existingWaitlistStatus(request.session.qualificationDraft ?? {}),
      nextAction: "Capturar nome antes de demo, recomendacao ou diagnostico para lead com interesse inicial.",
    },
  });
}

function createWhatsAppOpeningIntentTurn(
  request: AiAttendantRequest,
  normalized: string,
  painOrIntent: string | undefined,
  basePatch: CommercialPatch,
): AiAttendantResponse | undefined {
  if (request.session.channel !== "whatsapp") return undefined;
  if (request.session.qualificationDraft?.name) return undefined;

  const draft = request.session.qualificationDraft ?? {};

  if (isHumanRequest(normalized)) {
    return baseResponse({
      messages: [
        "Claro. Vou deixar uma pessoa assumir daqui.",
        "Também deixo o contexto salvo para você não precisar repetir tudo.",
      ],
      conversionPath: "human_whatsapp_assist",
      patch: {
        ...basePatch,
        commercialStage: "human_handoff",
        waitlistStatus: existingWaitlistStatus(draft),
        humanActive: "requested",
        aiPaused: "true",
        closureState: "human_active",
        nextAction: "Lead pediu humano; IA pausada e operador deve assumir.",
      },
    });
  }

  if (mentionsAudioOrMedia(normalized)) {
    return baseResponse({
      messages: [
        "Recebi o contexto, mas por aqui eu consigo seguir melhor por texto.",
        painOrIntent ? `Pelo que voce contou, o ponto parece ser ${painOrIntent}.` : "Me resume em uma frase o que voce quer resolver no studio.",
      ],
      patch: {
        ...basePatch,
        primaryPainOrIntent: painOrIntent,
        commercialStage: "awaiting_pain_or_intent",
        waitlistStatus: existingWaitlistStatus(draft),
        nextAction: "Continuar por texto depois de mencao a audio ou midia.",
      },
    });
  }

  if (isReceptionistOpening(normalized)) {
    return baseResponse({
      messages: [
        "Faz sentido ter recepcionista. A ideia nao e trocar sua equipe.",
        "A Taliya ajuda nas tarefas repetidas e deixa o contexto organizado.",
        "Em que parte da rotina isso pesa mais hoje?",
      ],
      nextQuestion: "Em que parte da rotina isso pesa mais hoje?",
      patch: {
        ...basePatch,
        commercialStage: "awaiting_pain_or_intent",
        waitlistStatus: existingWaitlistStatus(draft),
        nextAction: "Entender dor depois de responder objecao inicial sobre recepcionista.",
      },
    });
  }

  if (isDiagnosticAdOpening(normalized)) {
    const nextQuestion = "Pode ser?";
    return baseResponse({
      messages: [
        "Oi! Claro, dá para fazer por aqui.",
        "O diagnóstico é rápido: eu faço algumas perguntas sobre a rotina do studio e depois te devolvo um caminho mais claro.",
        nextQuestion,
      ],
      nextQuestion,
      patch: {
        ...basePatch,
        primaryPainOrIntent: painOrIntent ?? "diagnostico gratuito pelo anuncio",
        commercialStage: "diagnostic_offered",
        waitlistStatus: existingWaitlistStatus(draft),
        diagnosticStatus: "offered",
        nextAction: "Aguardar confirmacao para iniciar diagnostico vindo de anuncio.",
      },
    });
  }

  if (isOriginOrLowContextIntent(normalized)) {
    const nextQuestion = "Você quer entender a ideia geral primeiro ou tem alguma parte do studio que está pesando mais hoje?";
    return baseResponse({
      messages: [
        "Oi! Claro, te explico.",
        "A Taliya é um CRM para studios de Pilates, com IA para ajudar em atendimento, agenda, vendas e organização da rotina.",
        nextQuestion,
      ],
      nextQuestion,
      patch: {
        ...basePatch,
        commercialStage: "awaiting_pain_or_intent",
        waitlistStatus: existingWaitlistStatus(draft),
        nextAction: "Explicar origem/site/social e entender contexto sem capturar nome cedo.",
      },
    });
  }

  return undefined;
}

function createDiagnosticOfferTurn({
  name,
  painOrIntent,
  basePatch,
  extraPatch,
}: {
  name: string;
  painOrIntent: string;
  basePatch: CommercialPatch;
  extraPatch: Partial<QualificationDraft>;
}) {
  const isFitExploration = isTaliyaFitExploration(painOrIntent);
  const nextQuestion = isFitExploration
    ? "Quer que eu faca esse diagnostico gratuito rapido?"
    : "Quer que eu faca um diagnostico gratuito para entender esse cenario antes de falar de plano ou demo?";
  const messages = isFitExploration
    ? [
        `Boa, ${name}. Para entender como a Taliya ficaria no seu studio, eu preciso olhar a rotina real, nao te jogar uma demo generica.`,
        "Posso fazer um diagnostico gratuito com poucas perguntas e te dizer quais partes fariam sentido primeiro.",
        nextQuestion,
      ]
    : [
        painBridge(name, painOrIntent),
        "Posso fazer um diagnostico gratuito com poucas perguntas e te dizer o caminho mais coerente para o studio.",
        nextQuestion,
      ];

  return baseResponse({
    messages,
    nextQuestion,
    patch: {
      ...basePatch,
      ...extraPatch,
      primaryPainOrIntent: painOrIntent,
      commercialStage: "diagnostic_offered",
      waitlistStatus: "not_offered",
      diagnosticStatus: "offered",
      nextAction: "Aguardar aceite do diagnostico gratuito.",
    },
  });
}

function createPostDiagnosticValidationTurn(
  request: AiAttendantRequest,
  config: NicheLandingConfig,
  basePatch: CommercialPatch,
): AiAttendantResponse | undefined {
  const draft = request.session.qualificationDraft ?? {};
  if (draft.diagnosticCompleted !== "true") return undefined;
  if (draft.waitlistStatus === "offered" || draft.waitlistStatus === "pending_details" || draft.waitlistStatus === "joined") return undefined;

  const text = normalize(currentConversationText(request));
  const current = normalize(request.userMessage ?? "");

  if (isNegativeOrUncertain(current)) {
    return createDiagnosticNegativeTurn(config, basePatch);
  }

  if (isPositiveIntent(current) || isPositiveAfterRecommendation(text)) {
    return createWaitlistOfferTurn(basePatch, "diagnostic_positive");
  }

  return undefined;
}

function createPostDemoTurn(request: AiAttendantRequest, basePatch: CommercialPatch): AiAttendantResponse | undefined {
  const draft = request.session.qualificationDraft ?? {};
  if (draft.waitlistStatus === "offered" || draft.waitlistStatus === "pending_details" || draft.waitlistStatus === "joined") return undefined;
  if (!["offered", "unavailable", "viewed_discussed", "positive"].includes(draft.demoStatus ?? "")) return undefined;

  const current = normalize(request.userMessage ?? "");
  if (isNegativeOrUncertain(current)) {
    const nextQuestion = "O que ainda nao ficou claro para voce: valor, funcionamento no WhatsApp, configuracao ou controle humano?";
    return baseResponse({
      messages: ["Tudo bem. Entao eu nao vou te colocar em lista agora.", nextQuestion],
      nextQuestion,
      patch: {
        ...basePatch,
        commercialStage: "demo_seen",
        demoStatus: "negative",
        waitlistStatus: "undecided",
        nextAction: "Entender objecao depois da demo antes de oferecer lista de espera.",
      },
    });
  }

  if (isPositiveIntent(current)) {
    return createWaitlistOfferTurn(
      {
        ...basePatch,
        demoStatus: "positive",
      },
      "demo_positive",
    );
  }

  return undefined;
}

function createWaitlistFollowUpTurn(
  request: AiAttendantRequest,
  config: NicheLandingConfig,
  basePatch: CommercialPatch,
): AiAttendantResponse | undefined {
  const draft = request.session.qualificationDraft ?? {};
  const current = normalize(request.userMessage ?? "");
  const status = draft.waitlistStatus;

  if (status === "joined") {
    return createJoinedWaitlistTurn(request, config, basePatch, current);
  }

  if (status !== "offered" && status !== "pending_details") return undefined;

  if (isNegativeOrUncertain(current)) {
    const nextQuestion = "Sem problema. Quer que eu tire alguma duvida ou prefere ver uma explicacao mais pratica antes?";
    return baseResponse({
      messages: ["Tudo bem, nao vou te colocar na lista sem certeza.", nextQuestion],
      nextQuestion,
      conversionPath: "waitlist_intent",
      patch: {
        ...basePatch,
        commercialStage: "waitlist_declined",
        waitlistStatus: "declined",
        waitlistDeclinedAt: new Date().toISOString(),
        nextAction: "Tratar duvidas sem insistir na lista de espera.",
      },
    });
  }

  if (isPositiveIntent(current) || /\b(pode colocar|coloca|me coloca|quero entrar|entrar na lista|lista de espera)\b/.test(current)) {
    const details = extractWaitlistDetails(request.userMessage ?? "", draft);
    const missing = missingWaitlistFields(request, details);
    if (missing.length) {
      const nextQuestion = missingQuestion(missing);
      return baseResponse({
        messages: ["Perfeito. Para deixar isso organizado, so falta um detalhe.", nextQuestion],
        nextQuestion,
        conversionPath: "waitlist_intent",
        patch: {
          ...basePatch,
          ...details,
          commercialStage: "waitlist_pending_details",
          waitlistStatus: "pending_details",
          missingWaitlistFields: missing.join(","),
          nextAction: `Coletar dados pendentes da lista de espera: ${missing.join(", ")}.`,
        },
      });
    }

    return baseResponse({
      messages: ["Perfeito. Coloquei seu studio na lista de espera. Assim que abrirmos uma proxima janela, chamamos pelo canal combinado."],
      conversionPath: "waitlist_intent",
      patch: {
        ...basePatch,
        commercialStage: "waitlist_joined",
        waitlistStatus: "joined",
        waitlistJoinedAt: new Date().toISOString(),
        missingWaitlistFields: "",
        nextAction: "Studio entrou na lista de espera; avisar quando houver proxima janela.",
      },
    });
  }

  const details = extractWaitlistDetails(request.userMessage ?? "", draft);
  if (status === "pending_details") {
    const mergedRequest: AiAttendantRequest = {
      ...request,
      session: {
        ...request.session,
        qualificationDraft: {
          ...request.session.qualificationDraft,
          ...details,
        },
      },
    };
    const missing = missingWaitlistFields(mergedRequest, details);
    if (!missing.length) {
      return baseResponse({
        messages: ["Perfeito. Agora ficou completo. Coloquei seu studio na lista de espera e chamamos assim que possivel."],
        conversionPath: "waitlist_intent",
        patch: {
          ...basePatch,
          ...details,
          commercialStage: "waitlist_joined",
          waitlistStatus: "joined",
          waitlistJoinedAt: new Date().toISOString(),
          missingWaitlistFields: "",
          nextAction: "Studio entrou na lista de espera; avisar quando houver proxima janela.",
        },
      });
    }

    const nextQuestion = missingQuestion(missing);
    return baseResponse({
      messages: [Object.keys(details).length ? nextQuestion : `Ainda falta esse ponto para eu confirmar a lista: ${nextQuestion}`],
      nextQuestion,
      conversionPath: "waitlist_intent",
      patch: {
        ...basePatch,
        ...details,
        commercialStage: "waitlist_pending_details",
        waitlistStatus: "pending_details",
        missingWaitlistFields: missing.join(","),
        nextAction: `Coletar dados pendentes da lista de espera: ${missing.join(", ")}.`,
      },
    });
  }

  return undefined;
}

function createDiagnosticNegativeTurn(config: NicheLandingConfig, basePatch: CommercialPatch): AiAttendantResponse {
  if (!config.floatingAgent.guidedDemoReady) {
    const nextQuestion = "Qual parte voce gostaria de ver melhor: WhatsApp, agenda, vendas ou financeiro?";
    return baseResponse({
      messages: [
        "Sem problema. Entao eu nao colocaria seu studio em lista agora.",
        "A demo real ainda nao esta aberta, mas posso te explicar um fluxo pratico para voce visualizar melhor.",
        nextQuestion,
      ],
      nextQuestion,
      patch: {
        ...basePatch,
        commercialStage: "demo_offered",
        demoStatus: "unavailable",
        demoOfferedAt: new Date().toISOString(),
        waitlistStatus: "undecided",
        nextAction: "Oferecer explicacao/demo quando resposta ao diagnostico for negativa ou incerta.",
      },
    });
  }

  const nextQuestion = "Quer ver uma demo desse fluxo antes de decidir?";
  return baseResponse({
    messages: ["Sem problema. Entao eu nao colocaria seu studio em lista agora.", nextQuestion],
    nextQuestion,
    conversionPath: "guided_demo",
    patch: {
      ...basePatch,
      commercialStage: "demo_offered",
      demoStatus: "offered",
      demoOfferedAt: new Date().toISOString(),
      waitlistStatus: "undecided",
      nextAction: "Mostrar demo antes de retomar lista de espera.",
    },
  });
}

function createDemoUnavailableOrOfferedTurn(config: NicheLandingConfig, basePatch: CommercialPatch): AiAttendantResponse {
  if (!config.floatingAgent.guidedDemoReady) {
    const nextQuestion = "Qual parte da rotina voce queria enxergar primeiro?";
    return baseResponse({
      messages: [
        "A demo real ainda nao esta disponivel. Prefiro nao te mostrar algo que pareca pronto antes da hora.",
        "Mas posso te explicar um fluxo pratico com base no seu studio.",
        nextQuestion,
      ],
      nextQuestion,
      patch: {
        ...basePatch,
        commercialStage: "demo_offered",
        demoStatus: "unavailable",
        demoOfferedAt: new Date().toISOString(),
        waitlistStatus: "not_offered",
        nextAction: "Explicar demo em texto enquanto demo real nao estiver disponivel.",
      },
    });
  }

  return baseResponse({
    messages: ["Sim, posso te mostrar a demo.", "Depois que voce ver, se fizer sentido, a gente fala sobre lista de espera."],
    conversionPath: "guided_demo",
    patch: {
      ...basePatch,
      commercialStage: "demo_offered",
      demoStatus: "offered",
      demoOfferedAt: new Date().toISOString(),
      nextAction: "Levar para demo e validar interesse depois.",
    },
  });
}

function createWaitlistOfferTurn(basePatch: CommercialPatch, reason: "diagnostic_positive" | "demo_positive"): AiAttendantResponse {
  const nextQuestion = "Quer que eu coloque o studio na lista de espera?";
  return baseResponse({
    messages: [WAITLIST_NARRATIVE, "Se fizer sentido para voce, posso colocar seu studio na lista de espera e chamar assim que abrir uma proxima janela.", nextQuestion],
    nextQuestion,
    conversionPath: "waitlist_intent",
    patch: {
      ...basePatch,
      commercialStage: "waitlist_offered",
      waitlistStatus: "offered",
      waitlistOfferedAt: new Date().toISOString(),
      nextAction:
        reason === "diagnostic_positive"
          ? "Aguardar aceite explicito para entrar na lista apos diagnostico positivo."
          : "Aguardar aceite explicito para entrar na lista apos demo positiva.",
    },
  });
}

function createCustomAgentOpeningTurn(normalized: string, basePatch: CommercialPatch): AiAttendantResponse | undefined {
  if (!/\b(agente|automacao|automatizar)\b/.test(normalized) || !/\b(marketing|instagram|campanha|posts?|conteudo)\b/.test(normalized)) {
    return undefined;
  }

  const nextQuestion = "Qual WhatsApp ou email voce prefere deixar para continuarmos com esse contexto?";
  return baseResponse({
    messages: [
      "Isso parece uma rotina sob medida, separada dos planos publicos da Taliya.",
      "Antes de prometer marketing dentro dos 7 agentes, eu mapearia objetivo, canal, processo atual e resultado esperado.",
      nextQuestion,
    ],
    nextQuestion,
    conversionPath: "custom_agent_follow_up",
    patch: {
      ...basePatch,
      commercialStage: "human_handoff",
      waitlistStatus: "not_offered",
      customRoutine: "agente sob medida de marketing",
      nextAction: "Mapear agente sob medida de marketing sem vender como agente publico.",
    },
  });
}

function createCommercialObjectionTurn(
  normalized: string,
  knownName: string,
  basePatch: CommercialPatch,
): AiAttendantResponse | undefined {
  const nextQuestion = "Quer que eu faca um diagnostico gratuito para comparar isso com a rotina do seu studio?";

  if (/\b(achei caro|esta caro|ta caro|muito caro|caro demais|preco alto|nao cabe|sem orcamento)\b/.test(normalized)) {
    return baseResponse({
      messages: [
        `Entendo, ${knownName}. Olhar so o valor pode parecer pesado se a dor do studio ainda nao estiver clara.`,
        "O diagnostico gratuito ajuda a comparar plano, rotina e perda real de tempo antes de qualquer decisao.",
        nextQuestion,
      ],
      nextQuestion,
      patch: {
        ...basePatch,
        commercialStage: "diagnostic_offered",
        diagnosticStatus: "offered",
        waitlistStatus: "not_offered",
        nextAction: "Tratar objecao de preco com diagnostico gratuito, sem checkout.",
      },
    });
  }

  if (/\b(desconto|promocao|cupom|negociar)\b/.test(normalized)) {
    return baseResponse({
      messages: [
        "Hoje eu prefiro ser transparente com os planos configurados em vez de inventar desconto em conversa.",
        "Se o valor estiver no limite, o diagnostico gratuito ajuda a ver se faz sentido comecar menor ou esperar.",
        nextQuestion,
      ],
      nextQuestion,
      patch: {
        ...basePatch,
        commercialStage: "diagnostic_offered",
        diagnosticStatus: "offered",
        waitlistStatus: "not_offered",
        nextAction: "Responder desconto sem promessa comercial nao aprovada.",
      },
    });
  }

  if (/\b(teste gratis|teste gratuito|trial|plano gratis|plano gratuito|gratis para testar)\b/.test(normalized)) {
    return baseResponse({
      messages: [
        "Hoje nao temos trial publico gratuito para sair ativando sem contexto.",
        "Para reduzir risco, o caminho mais honesto e diagnosticar o studio e mostrar se existe plano que faca sentido.",
        nextQuestion,
      ],
      nextQuestion,
      patch: {
        ...basePatch,
        commercialStage: "diagnostic_offered",
        diagnosticStatus: "offered",
        waitlistStatus: "not_offered",
        nextAction: "Responder trial/gratuidade sem prometer acesso gratuito.",
      },
    });
  }

  if (/\b(se paga|roi|retorno|vale a pena|compensa)\b/.test(normalized)) {
    return baseResponse({
      messages: [
        "Depende de onde o studio perde mais hoje: horario vazio, interessado sem retorno, retrabalho de agenda ou cobranca manual.",
        "O diagnostico gratuito serve justamente para ligar plano e valor a uma perda real da rotina.",
        nextQuestion,
      ],
      nextQuestion,
      patch: {
        ...basePatch,
        commercialStage: "diagnostic_offered",
        diagnosticStatus: "offered",
        waitlistStatus: "not_offered",
        nextAction: "Tratar ROI com dor operacional antes de recomendar plano.",
      },
    });
  }

  return undefined;
}

function createJoinedWaitlistTurn(
  request: AiAttendantRequest,
  config: NicheLandingConfig,
  basePatch: CommercialPatch,
  current: string,
): AiAttendantResponse | undefined {
  const draft = request.session.qualificationDraft ?? {};

  if (isHumanRequest(current)) {
    return createHumanHandoffTurn(request, basePatch);
  }

  if (isPriceOrPlanQuestion(request) && !isBuyingIntent(current)) {
    const response = createPricePlanAnswer({
      config,
      request,
      reason: "Post-waitlist price/plan answer without restarting diagnostic.",
    });

    return {
      ...response,
      conversionPath: response.conversionPath ?? "waitlist_intent",
      qualificationPatch: {
        ...response.qualificationPatch,
        commercialStage: "waitlist_joined",
        waitlistStatus: "joined",
        diagnosticStatus: draft.diagnosticStatus,
        closureState: "waiting_user",
        nextAction:
          response.conversionPath === "view_plans"
            ? "Abrir comparativo de planos mantendo lead na lista de espera."
            : "Responder preco ou planos mantendo lead na lista de espera.",
      },
    };
  }

  if (isWaitlistRemovalRequest(current)) {
    return baseResponse({
      messages: [
        "Sem problema. Retirei seu studio da lista de espera por aqui.",
        "Se quiser retomar depois, e so me chamar com o contexto do studio.",
      ],
      conversionPath: "waitlist_intent",
      patch: {
        ...basePatch,
        commercialStage: "waitlist_declined",
        waitlistStatus: "declined",
        waitlistDeclinedAt: new Date().toISOString(),
        diagnosticStatus: draft.diagnosticStatus,
        closureState: "waitlist_declined",
        nextAction: "Lead pediu para sair da lista de espera; nao insistir.",
      },
    });
  }

  const details = extractWaitlistDetails(request.userMessage ?? "", draft);
  if (details.whatsapp || details.contactPreference || details.studioName || details.cityState || details.studioCity) {
    const nextQuestion = "Quer ajustar mais algum dado ou tirar alguma duvida enquanto isso?";
    return baseResponse({
      messages: [
        "Perfeito, atualizei esse dado junto da lista de espera.",
        "Quando abrir uma proxima janela, usamos o contato mais recente para chamar.",
        nextQuestion,
      ],
      nextQuestion,
      conversionPath: "waitlist_intent",
      patch: {
        ...basePatch,
        ...details,
        commercialStage: "waitlist_joined",
        waitlistStatus: "joined",
        diagnosticStatus: draft.diagnosticStatus,
        closureState: "waiting_user",
        nextAction: "Lead atualizou dados depois de entrar na lista de espera.",
      },
    });
  }

  if (isTimelineQuestion(current)) {
    const nextQuestion = "Enquanto isso, quer tirar alguma duvida sobre planos, WhatsApp ou funcionamento?";
    return baseResponse({
      messages: [
        "Ainda nao tenho uma data cravada para a proxima janela.",
        "Seu studio ja esta na lista de espera e a gente chama pelo contato salvo quando abrir vaga.",
        nextQuestion,
      ],
      nextQuestion,
      conversionPath: "waitlist_intent",
      patch: joinedWaitlistPatch(basePatch, draft, "Responder prazo da lista sem prometer data."),
    });
  }

  if (isDemoRequest(request.userMessage ?? "")) {
    const nextQuestion = "Qual parte voce quer visualizar melhor: atendimento, agenda, vendas ou financeiro?";
    return baseResponse({
      messages: [
        "A demo real ainda nao esta aberta para todo mundo.",
        "Mas como seu studio ja esta na lista de espera, posso te explicar o fluxo mais importante por aqui.",
        nextQuestion,
      ],
      nextQuestion,
      conversionPath: "waitlist_intent",
      patch: joinedWaitlistPatch(basePatch, draft, "Explicar demo/fluxo para lead que ja esta na lista."),
    });
  }

  if (isWhatsAppDoubt(current)) {
    const nextQuestion = "Quer que eu explique tambem como fica a parte de agenda ou planos?";
    return baseResponse({
      messages: [
        "No WhatsApp, a ideia e a equipe continuar no controle, com a Taliya organizando contexto e ajudando nas respostas da rotina.",
        "Como seu studio ja esta na lista de espera, esse ponto fica registrado para a proxima janela.",
        nextQuestion,
      ],
      nextQuestion,
      conversionPath: "waitlist_intent",
      patch: joinedWaitlistPatch(basePatch, draft, "Responder duvida sobre WhatsApp depois da lista de espera."),
    });
  }

  const directAnswer = postWaitlistDirectAnswer(current);
  if (directAnswer) {
    const nextQuestion = "Quer tirar mais alguma duvida enquanto seu studio fica na lista?";
    return baseResponse({
      messages: [...directAnswer, nextQuestion],
      nextQuestion,
      conversionPath: "waitlist_intent",
      patch: joinedWaitlistPatch(basePatch, draft, "Responder duvida comercial depois da lista de espera."),
    });
  }

  if (isThanksOrClosure(current)) {
    return baseResponse({
      messages: [
        "Fechado. Seu studio segue na lista de espera.",
        "Quando abrir uma proxima janela, chamamos pelo contato salvo.",
      ],
      conversionPath: "waitlist_intent",
      patch: joinedWaitlistPatch(basePatch, draft, "Encerrar conversa mantendo lead na lista de espera."),
    });
  }

  return undefined;
}

function joinedWaitlistPatch(basePatch: CommercialPatch, draft: QualificationDraft, nextAction: string): QualificationDraft {
  return {
    ...basePatch,
    commercialStage: "waitlist_joined",
    waitlistStatus: "joined",
    diagnosticStatus: draft.diagnosticStatus,
    closureState: "waiting_user",
    nextAction,
  };
}

function postWaitlistDirectAnswer(normalized: string): string[] | undefined {
  if (/\b(garantia|reembolso|cancelar|cancelamento|cancelo|contrato|fidelidade)\b/.test(normalized)) {
    return [
      "Sim. A regra comercial atual dos planos publicos considera 30 dias de garantia na primeira assinatura.",
      "Depois desse periodo, o plano mensal pode ser cancelado sem multa, mas reembolso nao e automatico.",
    ];
  }

  if (/\b(trocar|mudar|upgrade|downgrade|subir|descer|plano menor|plano maior)\b/.test(normalized)) {
    return [
      "Sim, a ideia e permitir ajustar o plano conforme a rotina do studio evolui.",
      "Da para comecar menor quando fizer sentido e depois trocar para cobrir mais agentes.",
    ];
  }

  if (/\b(configura|configuracao|setup|implantar|implantacao|comeco|instalar|treinar)\b/.test(normalized)) {
    return [
      "No comeco, a configuracao precisa mapear regras do studio, agenda, alunos, mensagens e limites de cada agente.",
      "A equipe continua no controle; a Taliya organiza a base e deixa as rotinas prontas para operar com seguranca.",
    ];
  }

  if (/\b(privacidade|dados|lgpd|seguranca|seguro)\b/.test(normalized)) {
    return [
      "A Taliya deve guardar apenas os dados necessarios para operar a rotina e atender o lead ou studio.",
      "Dados sensiveis e pagamento nao devem ser tratados pelo chat; isso fica em fluxo seguro e separado.",
    ];
  }

  if (/\b(integra|integracao|google agenda|agenda do google|sistema externo)\b/.test(normalized)) {
    return [
      "Eu nao vou prometer integracao especifica sem confirmar o sistema e o fluxo.",
      "O caminho seguro e validar se isso entra na configuracao atual ou se precisa de ajuste sob medida.",
    ];
  }

  return undefined;
}

function createHumanHandoffTurn(request: AiAttendantRequest, basePatch: CommercialPatch): AiAttendantResponse {
  const draft = request.session.qualificationDraft ?? {};
  const nextQuestion =
    request.session.channel === "web"
      ? "Qual WhatsApp ou email voce prefere usar para a pessoa continuar?"
      : draft.name
        ? "Quer que eu deixe um resumo para a pessoa continuar daqui?"
        : undefined;
  return baseResponse({
    messages: [
      "Claro. Posso deixar uma pessoa assumir daqui.",
      "Vou manter o contexto organizado para voce nao precisar repetir tudo.",
      ...(nextQuestion ? [nextQuestion] : []),
    ],
    nextQuestion,
    conversionPath: "human_whatsapp_assist",
    patch: {
      ...basePatch,
      commercialStage: "human_handoff",
      waitlistStatus: existingWaitlistStatus(draft),
      humanActive: "requested",
      aiPaused: "true",
      closureState: "human_active",
      nextAction: "Lead pediu humano; operador deve assumir ou confirmar retomada da IA.",
    },
  });
}

function baseResponse({
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
    assistantMessages: messages.map((message) =>
      createAssistantMessage(message, conversionPath === "waitlist_intent" ? "waitlist_intent" : "answer_question"),
    ),
    capturedPainIds: [],
    recommendedAgentIds: [],
    recommendations: undefined,
    nextQuestion,
    conversionPath,
    subscription: undefined,
    shouldOfferDiagnostic: patch.diagnosticStatus !== "completed",
    qualificationPatch: patch,
    guardrailDecision: {
      category: "allowed",
      action: "respond",
      reason: "Deterministic humanized sales flow.",
    },
  };
}

function sourcePatch(request: AiAttendantRequest): CommercialPatch {
  return {
    leadSourceChannel: request.session.channel === "whatsapp" ? "whatsapp" : "widget",
    leadSourceDetail: [request.session.entryPath, request.session.sourceSection, request.session.sourcePage].filter(Boolean).join(":").slice(0, 180),
    whatsapp: request.session.externalContact?.phone,
    contactPreference: request.session.externalContact?.phone,
  };
}

function hasPainOrIntent(draft: QualificationDraft) {
  return Boolean(draft.primaryPainOrIntent || draft.operationalPains || draft.biggestPain || draft.priorityGoal);
}

function shouldAskPainAfterName(text: string) {
  const normalized = normalize(text);
  return isGreetingOnly(normalized) || looksLikeName(text) || /\b(ok|sim|claro|boa|vamos)\b/.test(normalized);
}

function existingWaitlistStatus(draft: QualificationDraft): WaitlistStatus {
  return draft.waitlistStatus ?? "not_offered";
}

function extractName(text: string) {
  const clean = text.trim();
  const explicit =
    clean.match(/\b(?:sou|me chamo|meu nome e|meu nome eh|meu nome é|aqui e|aqui eh|aqui é)\s+(\p{L}{2,}(?:\s+\p{L}{2,}){0,2})/iu)?.[1] ??
    clean.match(/\bnome\s*(?:e|é|eh|:)\s*(\p{L}{2,}(?:\s+\p{L}{2,}){0,2})/iu)?.[1] ??
    clean.match(/^(\p{L}{2,}(?:\s+\p{L}{2,}){0,2})\s*[,;-]/u)?.[1];
  if (explicit && looksLikeName(explicit)) return titleName(explicit);
  if (looksLikeName(clean)) return titleName(clean);
  return undefined;
}

function looksLikeName(text: string) {
  const clean = text.trim();
  const normalized = normalize(clean);
  if (clean.length < 2 || clean.length > 40) return false;
  if (!/^[\p{L}\s]+$/u.test(clean)) return false;
  if (clean.split(/\s+/).length > 3) return false;
  if (isOriginOrLowContextIntent(normalized) || isHumanRequest(normalized) || mentionsAudioOrMedia(normalized) || isReceptionistOpening(normalized)) return false;
  return !/\b(ola|oi|opa|bom dia|boa tarde|boa noite|quero|preciso|valor|preco|plano|diagnostico|whatsapp|agenda|venda|vendas|lead|leads|financeiro|sistema|studio|pilates|sim|nao|ok|duvida|pesquisando|pesquisar|caderno|planilha|alunos|recepcionista|integra|integracao|google)\b/.test(normalized);
}

function titleName(name: string) {
  return name.replace(/\s+/g, " ").trim();
}

function firstName(name: string) {
  return name.trim().split(/\s+/)[0] || name;
}

function extractPainOrIntent(text: string) {
  const normalized = normalize(text);
  const direct = normalized.match(/\b(?:quero|preciso|busco|tenho problema com|minha dor e|minha dor eh|me ajuda com)\s+(.{4,120})/)?.[1];
  if (direct) return cleanPain(direct);
  if (/\b(reposicao|reposicoes|faltas|agenda|horario|encaixe)\b/.test(normalized)) return "agenda, faltas e reposicoes";
  if (/\b(whatsapp|mensagem|atendimento|responder)\b/.test(normalized)) return "atendimento no WhatsApp";
  if (/\b(vendas|interessados|lead|leads|aula experimental|matricula|follow)\b/.test(normalized)) return "vendas e interessados";
  if (/\b(financeiro|cobranca|mensalidade|renovacao)\b/.test(normalized)) return "financeiro e renovacoes";
  if (/\b(nao vejo|nao enxergo|visao do dia|acontece no dia|prioridade|prioridades)\b/.test(normalized)) return "visao do dia e prioridades";
  if (/\b(caderno|planilha|manual|papel)\b/.test(normalized)) return "rotina manual em caderno ou planilha";
  if (/\b(gestao|organizar|rotina|studio|operacao)\b/.test(normalized)) return "organizacao da rotina do studio";
  return undefined;
}

function painBridge(name: string, painOrIntent: string) {
  const normalized = normalize(painOrIntent);
  if (isTaliyaFitExploration(normalized)) {
    return `Boa, ${name}. Para entender como a Taliya ficaria no seu studio, eu preciso olhar a rotina real, nao te jogar uma demo generica.`;
  }
  if (/\b(leads|vendas|interessados)\b/.test(normalized)) {
    return `Entendi, ${name}. Quando leads comecam a escapar, normalmente o problema nao e so responder rapido; e nao perder origem, retorno e proxima acao.`;
  }
  if (/\b(caderno|manual|planilha)\b/.test(normalized)) {
    return `Entendi, ${name}. Com essa operacao no manual, a rotina fica dependente de quem anotou, lembrou ou conferiu.`;
  }
  if (/\b(visao|prioridades|dia|gestao)\b/.test(normalized)) {
    return `Entendi, ${name}. Entao o ponto e ganhar visao do dia e clareza do que precisa de atencao primeiro.`;
  }
  if (/\b(reposicao|agenda|faltas)\b/.test(normalized)) {
    return `Entendi, ${name}. Reposicao e agenda costumam virar gargalo quando a informacao fica espalhada entre conversa, anotacao e memoria da equipe.`;
  }
  return `Entendi, ${name}. Entao o ponto agora parece ser ${painOrIntent}.`;
}

function isTaliyaFitExploration(value: string) {
  const normalized = normalize(value);
  return /\btaliya\b/.test(normalized) && /\b(ficaria|funcionaria|ajudaria|entraria|studio|estudio)\b/.test(normalized);
}

function cleanPain(value: string) {
  return value.replace(/[?.!]+$/g, "").trim().slice(0, 140);
}

function isGreetingOnly(normalized: string) {
  return /^(oi|ola|ol[aá]|opa|bom dia|boa tarde|boa noite|e ai|ei|hey)[\s!.?]*$/.test(normalized.trim());
}

function isNameRefusal(normalized: string) {
  return /\b(prefiro nao|nao quero falar|nao vou falar|sem nome|nome nao|nao precisa do meu nome)\b/.test(normalized);
}

function isDirectQuestion(normalized: string) {
  return /\b(preco|valor|quanto custa|planos?|demo|demonstracao|como funciona|o que e|o que eh|whatsapp|integra)\b/.test(normalized);
}

function isIntegrationQuestion(normalized: string) {
  return /\b(integra|integracao|google agenda|agenda do google|calendar)\b/.test(normalized);
}

function isExistingSystemContext(normalized: string) {
  return /\b(ja tenho sistema|uso sistema|tenho um sistema|sistema atual|ja uso)\b/.test(normalized);
}

function isResearchingContext(normalized: string) {
  return /\b(so pesquisando|s[oó] pesquisando|pesquisando|estou vendo|estou comparando|quero comparar)\b/.test(normalized);
}

function isQuantifiedManualContext(normalized: string) {
  return /\b\d{2,4}\b/.test(normalized) && /\b(alunos?|clientes?|caderno|planilha|manual|papel)\b/.test(normalized);
}

function directQuestionAnswer(normalized: string) {
  if (/\b(preco|valor|quanto custa|planos?)\b/.test(normalized)) {
    return "Os planos sao por quantidade de agentes: Base, 1 Agente, 3 Agentes e 7 Agentes. Eu consigo te orientar melhor depois de entender a rotina.";
  }
  if (/\b(demo|demonstracao)\b/.test(normalized)) {
    return "A demo serve para visualizar a rotina na pratica. Se a demo real ainda nao estiver aberta, eu explico o fluxo por aqui sem inventar tela pronta.";
  }
  if (/\b(como funciona|o que e|o que eh)\b/.test(normalized)) {
    return "A Taliya organiza a rotina do studio e ajuda a equipe a acompanhar WhatsApp, agenda, vendas, financeiro e alunos que estao sumindo.";
  }
  return "Te respondo de forma objetiva: a Taliya ajuda o studio a organizar a rotina e decidir o proximo passo sem jogar tudo para a equipe lembrar.";
}

function isPositiveIntent(normalized: string) {
  return /\b(sim|faz sentido|gostei|boa|perfeito|quero|pode|vamos|tenho interesse|interesse total|curti|legal|avancar|avancar|seguir|coloca|pode colocar)\b/.test(normalized);
}

function isBuyingIntent(normalized: string) {
  return /\b(quero assinar|quero comprar|quero contratar|assinar agora|comprar agora|fechar agora|quero fechar|me manda.*link|link.*pag|pagamento|pagar)\b/.test(normalized);
}

function isPositiveAfterRecommendation(text: string) {
  return isPositiveIntent(text) && /\b(diagnostico|recomendacao|recomendado|plano|faz sentido|agentes|taliya)\b/.test(text);
}

function isNegativeOrUncertain(normalized: string) {
  return /\b(nao|nao sei|talvez|duvida|nao faz sentido|nao gostei|achei ruim|ainda nao|vou pensar|preciso pensar|caro|confuso|incerto)\b/.test(normalized);
}

function isDemoRequest(text: string) {
  return /\b(demo|demonstracao|ver funcionando|ver o sistema|mostrar funcionando)\b/i.test(normalize(text));
}

function isTimelineQuestion(normalized: string) {
  return /\b(quando|prazo|data|previsao|previsao|proxima janela|chamar|chamam|retorno|voltam|abrir vaga|abre vaga|e agora|proximo passo|agora o que|o que acontece)\b/.test(normalized);
}

function isWaitlistRemovalRequest(normalized: string) {
  return (
    /\b(tirar da lista|sair da lista|remove da lista|remover da lista|me tira da lista|me remove da lista)\b/.test(normalized) ||
    /\b(nao quero mais|nao tenho mais interesse|desistir|desisti)\b.{0,60}\b(lista|espera|taliya)\b/.test(normalized) ||
    /\b(lista|espera|taliya)\b.{0,60}\b(nao quero mais|nao tenho mais interesse|desistir|desisti)\b/.test(normalized)
  );
}

function isWhatsAppDoubt(normalized: string) {
  return /\b(whatsapp|numero|business|app|mensagem|responder|atendimento)\b/.test(normalized);
}

function isThanksOrClosure(normalized: string) {
  return /^(ok|obrigado|obrigada|valeu|perfeito|beleza|ta bom|t[aá] bom|fechado)[\s!.?]*$/.test(normalized.trim());
}

function isOriginOrLowContextIntent(normalized: string) {
  return (
    /\b(queria saber mais|quero saber mais|saber mais|me explica|explica melhor|fiquei curioso|tenho interesse|vim pelo site|vim pelo instagram|vim pelo facebook|vim pelo anuncio|vi no instagram|vi no facebook|vi no anuncio|sou do anuncio|e sobre ia|eh sobre ia)\b/.test(normalized) ||
    /^(interesse|tenho interesse|quero saber|queria entender|me explica melhor)[\s!.?]*$/.test(normalized)
  );
}

function isDiagnosticAdOpening(normalized: string) {
  return (
    /\b(vim pelo anuncio|vi no anuncio|sou do anuncio)\b/.test(normalized) &&
    /\b(diagnostico|diagnostico gratuito|organizar primeiro)\b/.test(normalized)
  ) || /\bdiagnostico gratuito\b.{0,120}\borganizar primeiro\b/.test(normalized);
}

function isLowContextExploration(normalized: string) {
  return (
    isOriginOrLowContextIntent(normalized) ||
    /\b(quero|queria|preciso|gostaria)\b.{0,80}\b(ver|entender|saber)\b.{0,80}\b(taliya|sistema|studio|estudio|pilates|como ficaria|caminho para comecar)\b/.test(normalized) ||
    /\b(como|qual)\b.{0,80}\b(taliya|sistema)\b.{0,80}\b(ficaria|funcionaria|entraria|ajudaria)\b/.test(normalized)
  );
}

function isHumanRequest(normalized: string) {
  return /\b(falar com alguem|falar com uma pessoa|falar com humano|atendente|consultor|pessoa real|alguem da equipe)\b/.test(normalized);
}

function mentionsAudioOrMedia(normalized: string) {
  return /\b(audio|áudio|imagem|foto|documento|print|video|enviei|mandei)\b/.test(normalized);
}

function isReceptionistOpening(normalized: string) {
  return /\b(recepcionista|secretaria|atendente|equipe)\b/.test(normalized);
}

function missingWaitlistFields(request: AiAttendantRequest, details: Partial<QualificationDraft> = extractWaitlistDetails(request.userMessage ?? "", request.session.qualificationDraft)) {
  const draft = {
    ...(request.session.qualificationDraft ?? {}),
    ...details,
  };
  const missing: string[] = [];
  if (request.session.channel !== "whatsapp" && !draft.name) missing.push("nome");
  if (!draft.studioName) missing.push("studio");
  if (!draft.cityState && !draft.studioCity) missing.push("cidade");
  if (request.session.channel !== "whatsapp" && !draft.whatsapp && !request.session.externalContact?.phone) missing.push("whatsapp");
  if (!draft.primaryPainOrIntent && !draft.operationalPains && !draft.biggestPain && !draft.diagnosticSummary) missing.push("dor");
  return missing;
}

function missingQuestion(missing: string[]) {
  if (missing.includes("studio") && missing.includes("cidade")) return "Qual e o nome do studio e de qual cidade ele e?";
  if (missing.includes("studio")) return "Qual e o nome do studio?";
  if (missing.includes("cidade")) return "De qual cidade e o studio?";
  if (missing.includes("whatsapp")) return "Qual WhatsApp usamos para te chamar?";
  if (missing.includes("nome")) return "Com quem eu falo?";
  return "Qual dor principal devo deixar registrada junto da lista?";
}

function extractWaitlistDetails(text: string, draft: QualificationDraft | undefined = {}): Partial<QualificationDraft> {
  const patch: Partial<QualificationDraft> = {};
  const cleanText = text.trim();
  const commaParts = cleanText.split(",").map((part) => part.trim()).filter(Boolean);
  const studio = cleanText.match(/\b((?:studio|estudio)\s+[\p{L}\d\s.'-]{2,50})(?:$|[,.;])/iu)?.[1];
  const studioFromComma =
    !draft.studioName && commaParts.length >= 2 && looksLikeWaitlistStudioName(commaParts.slice(0, -1).join(", "))
      ? commaParts.slice(0, -1).join(", ")
      : undefined;
  const city =
    cleanText.match(/\b(?:cidade|em|de)\s+([\p{L}\s.'-]{2,40})(?:$|[,.;])/iu)?.[1] ??
    (commaParts.length >= 2 ? commaParts[commaParts.length - 1] : undefined) ??
    (!draft.cityState && !draft.studioCity && looksLikeStandaloneCity(cleanText) ? cleanText : undefined);
  const phone = text.match(/(?:\+?55\s*)?(?:\(?\d{2}\)?\s*)?\d{4,5}[-\s]?\d{4}/)?.[0];
  if (studio || studioFromComma) patch.studioName = (studio ?? studioFromComma)?.trim();
  if (city) {
    patch.cityState = city.trim();
    patch.studioCity = city.trim();
  }
  if (phone) {
    patch.whatsapp = phone.trim();
    patch.contactPreference = phone.trim();
  }
  return patch;
}

function looksLikeStandaloneCity(text: string) {
  const clean = text.trim();
  const normalized = normalize(clean);
  if (clean.length < 3 || clean.length > 40) return false;
  if (!/^[\p{L}\s.'-]+$/u.test(clean)) return false;
  if (/\b(sim|nao|ok|pode|coloca|lista|studio|estudio|whatsapp|email|reposicao|agenda|financeiro|vendas?)\b/.test(normalized)) return false;
  return clean.split(/\s+/).length <= 4;
}

function looksLikeWaitlistStudioName(text: string) {
  const clean = text.trim();
  const normalized = normalize(clean);
  if (clean.length < 2 || clean.length > 60) return false;
  if (!/^[\p{L}\d\s.'-]+$/u.test(clean)) return false;
  if (/\b(sim|nao|ok|pode|coloca|lista|whatsapp|email|reposicao|agenda|financeiro|vendas?)\b/.test(normalized)) return false;
  return true;
}

function currentConversationText(request: AiAttendantRequest) {
  return [request.userMessage, ...request.session.messages.slice(-4).map((message) => message.content)].filter(Boolean).join(" ");
}

function normalize(value: string) {
  return value
    .toLowerCase()
    .normalize("NFD")
    .replace(/\p{Diacritic}/gu, "");
}
