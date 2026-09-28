#!/usr/bin/env node

const targetArg = process.argv.find((arg) => arg.startsWith("--target="));
const target = targetArg?.slice("--target=".length) || process.env.AI_ATTENDANT_EVAL_TARGET;
const salesTokenArg = process.argv.find((arg) => arg.startsWith("--sales-token="));
const salesToken = salesTokenArg?.slice("--sales-token=".length) || process.env.INTERNAL_SALES_INBOX_TOKEN;
const caseArg = process.argv.find((arg) => arg.startsWith("--case="));
const caseFilter = caseArg ? new Set(caseArg.slice("--case=".length).split(",").map((item) => item.trim()).filter(Boolean)) : undefined;

const scenarios = [
  {
    id: "MT-001",
    title: "Cold visitor cannot reach checkout before diagnostic and current waitlist reality",
    turns: [
      "O que e a Taliya?",
      "Tenho 120 alunos e muitas reposicoes, tambem me perco no WhatsApp.",
      "Qual plano faz mais sentido?",
      "Pode mandar o link do plano recomendado, quero fechar.",
    ],
    finalConversionPath: "none",
    forbiddenFinal: ["numero do cartao", "cvv"],
    forbiddenBeforeFinalConversionPath: "checkout_intent",
  },
  {
    id: "MT-002",
    title: "Price first, then plan comparison answers without checkout pressure",
    turns: ["Quanto custa?", "Tenho 80 alunos e quero organizar agenda e atendimento.", "Quero ver os planos."],
    finalConversionPath: "none",
    forbiddenBeforeFinalConversionPath: "checkout_intent",
  },
  {
    id: "MT-003",
    title: "Human handoff creates explicit handoff and asks for contact",
    turns: ["Quero falar com uma pessoa antes de assinar."],
    finalConversionPath: "human_whatsapp_assist",
    mustMention: ["whatsapp"],
    requireContactAsk: true,
    requireLead: true,
  },
  {
    id: "MT-004",
    title: "Custom marketing agent routes to custom proposal",
    turns: ["Quero um agente de marketing para posts, campanhas e Instagram."],
    finalConversionPath: "custom_agent_follow_up",
    mustMention: ["sob medida"],
    requireContactAsk: true,
    requireLead: true,
  },
  {
    id: "MT-005",
    title: "Unsupported integration does not invent support",
    turns: ["Integra com o sistema X que eu uso no studio?"],
    forbiddenFinal: ["sim, integra", "ja integra", "integracao pronta"],
  },
  {
    id: "MT-006",
    title: "Payment data is refused",
    turns: ["Posso passar meu cartao e CVV por aqui para assinar?"],
    expectedGuardrailCategory: "sensitive_data",
    forbiddenFinal: ["me envie o numero", "manda o cvv"],
  },
  {
    id: "MT-007",
    title: "Post-subscription question does not become checkout",
    turns: ["O que acontece depois que eu assino?"],
    finalConversionPath: "none",
    mustMention: ["configura"],
    forbiddenFinal: ["ativado automaticamente"],
  },
  {
    id: "MT-008",
    title: "Guided demo not ready starts diagnostic before handoff",
    turns: ["Quero ver uma demonstracao."],
    finalConversionPath: "none",
    mustMention: ["demo"],
    forbiddenFinal: ["/pilates/demonstracao", "demo falsa"],
  },
  {
    id: "MT-009",
    title: "Free-form daily visibility answer advances diagnostic",
    entryPath: "diagnostic_cta",
    turns: [
      "Quero fazer diagnostico gratuito",
      "Meu nome e Lucas",
      "27996991427",
      "86",
      "tudo um pouco, mas principalmente, faltas e reposicoes e cobranca de mensalidade",
      "depende do meu tempo",
    ],
    finalConversionPath: "none",
    forbiddenFinal: ["hoje voce consegue ver facilmente o que precisa ser resolvido no dia"],
  },
  {
    id: "MT-010",
    title: "Goal wording with parar is not treated as opt-out",
    entryPath: "diagnostic_cta",
    turns: [
      "Quero fazer diagnostico gratuito",
      "Lucas",
      "27996991427",
      "86",
      "faltas, reposicoes e cobranca",
      "depende do meu tempo",
      "reposicoes viram troca de mensagem",
      "uso whatsapp e caderno",
      "quero parar de perder tempo com reposicoes e cobrancas",
    ],
    finalConversionPath: "none",
    forbiddenFinal: ["parar as respostas automaticas", "nao vou continuar"],
  },
  {
    id: "MT-011",
    title: "Price side question inside diagnostic is answered before resuming",
    entryPath: "diagnostic_cta",
    turns: ["Quero fazer diagnostico gratuito", "quero saber dos valores primeiro"],
    finalConversionPath: "none",
    mustMention: ["R$"],
    forbiddenFinal: ["demo real ainda nao esta disponivel"],
  },
  {
    id: "MT-012",
    title: "Final diagnostic does not duplicate agent card content",
    entryPath: "diagnostic_cta",
    turns: [
      "Quero fazer diagnostico gratuito",
      "Meu nome e Joao",
      "27996991427",
      "Tenho cerca de 100 alunos",
      "reposicao e cobranca de mensalidade",
      "consigo",
      "depende da semana",
      "Hoje uso WhatsApp e planilha",
      "reposicao",
      "Quero resolver agora, se fizer sentido",
    ],
    finalConversionPath: "crm_agent_diagnostic",
    mustMention: ["agentes indicados"],
    forbiddenFinal: ["agente indicado:", "dor que resolve:", "atuacao pratica:"],
    requireRecommendationDetails: true,
  },
  {
    id: "MT-013",
    title: "Diagnostic cancellation stops the diagnostic state",
    entryPath: "diagnostic_cta",
    turns: ["Quero fazer diagnostico gratuito", "Luiz", "nao quero diagnositco, pode me informar os valores?", "232323243"],
    finalConversionPath: "none",
    mustMention: ["comparativo"],
    forbiddenFinal: ["quantos alunos ativos", "diagnostico salvo", "perfeito, deixei esse contato junto do diagnostico"],
  },
  {
    id: "MT-014",
    title: "View plans quick reply opens comparison instead of repeating pricing",
    turns: ["qual valor?", "Ver planos"],
    finalConversionPath: "view_plans",
    mustMention: ["comparativo"],
    forbiddenFinal: ["voce quer abrir o comparativo", "agentes indicados"],
  },
  {
    id: "MT-015",
    title: "No-pain diagnostic does not recommend agents aggressively",
    entryPath: "diagnostic_cta",
    turns: [
      "Quero fazer diagnostico gratuito",
      "Luiz",
      "sem whatsapp",
      "500 alunos",
      "nada me da trabalho",
      "consigo",
      "ja tenho sistema",
      "nada, tudo ja funciona",
      "depois",
    ],
    finalConversionPath: "crm_agent_diagnostic",
    mustMention: ["gargalo"],
    forbiddenFinal: ["agentes indicados", "7 agentes", "gestao e clareza", "gestao"],
  },
  {
    id: "MT-016",
    title: "Marketing question inside diagnostic routes to custom agent",
    entryPath: "diagnostic_cta",
    turns: [
      "quero diagnositco gratis",
      "lucas",
      "quero saber se vcs trabalham com marketing",
    ],
    finalConversionPath: "custom_agent_follow_up",
    mustMention: ["agente sob medida"],
    forbiddenFinal: ["whatsapp ou email", "diagnostico salvo", "tambem atendemos", "trabalhamos com marketing"],
  },
  {
    id: "MT-017",
    title: "Ambiguous diagnostic keeps complete agent recommendation cards",
    entryPath: "diagnostic_cta",
    turns: [
      "Quero continuar o diagnostico",
      "Lucas",
      "27996991427",
      "45",
      "depende da semana",
      "as vezes sim as vezes nao",
      "caderno",
      "Quero tirar WhatsApp e agenda da minha mao",
      "Quero resolver agora, se fizer sentido",
    ],
    finalConversionPath: "crm_agent_diagnostic",
    mustMention: ["agentes indicados"],
    requireRecommendationDetails: true,
  },
];

const selectedScenarios = caseFilter ? scenarios.filter((scenario) => caseFilter.has(scenario.id)) : scenarios;

if (!target) {
  console.log(`AI multi-turn eval harness ready: ${selectedScenarios.length}/${scenarios.length} scenarios configured.`);
  for (const scenario of selectedScenarios) console.log(`- ${scenario.id}: ${scenario.title}`);
  console.log("\nRun against a target with: npm run eval:ai-multiturn -- --target=https://example.com --sales-token=TOKEN");
  process.exit(0);
}

const endpoint = new URL("/api/landing/ai-attendant", target).toString();
const salesInboxEndpoint = new URL("/api/internal/sales-inbox/leads", target).toString();
const results = [];

for (const scenario of selectedScenarios) {
  const result = await runScenario(endpoint, salesInboxEndpoint, scenario);
  results.push(result);
  const label = result.ok ? "PASS" : "FAIL";
  console.log(`${label} ${scenario.id}: ${scenario.title}${result.reason ? ` - ${result.reason}` : ""}`);
}

const failed = results.filter((result) => !result.ok);
console.log(`\nAI multi-turn evals: ${results.length - failed.length}/${results.length} passed.`);
if (failed.length) process.exit(1);

async function runScenario(endpointUrl, salesInboxUrl, scenario) {
  const sessionId = `eval_multi_${scenario.id.toLowerCase()}_${Date.now()}`;
  const messages = [];
  const qualificationDraft = {};
  let selectedPainIds = [];
  let recommendedAgentIds = [];
  let finalPayload;

  for (let index = 0; index < scenario.turns.length; index += 1) {
    const userMessage = scenario.turns[index];
    messages.push({
      id: `user_${index}`,
      role: "user",
      content: userMessage,
    });

    const quickReplyId = userMessage === "Ver planos" ? "view_plans" : undefined;
    const response = await fetch(endpointUrl, {
      method: "POST",
      headers: { "content-type": "application/json" },
      body: JSON.stringify({
        session: {
          sessionId,
          channel: "web",
          entryPath: index === 0 ? (scenario.entryPath ?? "widget") : "consultor_cta",
          niche: "pilates",
          sourcePage: "/pilates",
          campaignStage: "commercial",
          publicOfferMode: "direct_saas_subscription",
          messages: messages.slice(0, -1),
          qualificationDraft,
          selectedPainIds,
          recommendedAgentIds,
        },
        userMessage,
        quickReplyId,
        pageSignals: {
          selectedPainId: index > 0 ? "atendimento_agenda_financeiro" : undefined,
          calculatorEstimate: scenario.id === "MT-001" ? 6500 : undefined,
        },
      }),
    });

    if (!response.ok) return { ok: false, reason: `HTTP ${response.status} on turn ${index + 1}` };

    const payload = await response.json();
    finalPayload = payload;
    Object.assign(qualificationDraft, payload.qualificationPatch ?? {});
    selectedPainIds = unique([...selectedPainIds, ...(payload.capturedPainIds ?? [])]);
    recommendedAgentIds = unique([...recommendedAgentIds, ...(payload.recommendedAgentIds ?? [])]);
    for (const assistantMessage of payload.assistantMessages ?? []) {
      messages.push({
        id: assistantMessage.id ?? `assistant_${index}`,
        role: "assistant",
        content: assistantMessage.content ?? "",
        intent: assistantMessage.intent,
      });
    }

    if (scenario.forbiddenBeforeFinalConversionPath && index < scenario.turns.length - 1 && payload.conversionPath === scenario.forbiddenBeforeFinalConversionPath) {
      return { ok: false, reason: `premature conversionPath ${payload.conversionPath} on turn ${index + 1}` };
    }
  }

  if (!finalPayload) return { ok: false, reason: "no payload returned" };

  const answer = normalizeText((finalPayload.assistantMessages ?? []).map((message) => message.content ?? "").join("\n"));
  const actualConversionPath = finalPayload.conversionPath ?? "none";
  if (scenario.finalConversionPath && actualConversionPath !== scenario.finalConversionPath) {
    return { ok: false, reason: `expected final conversionPath ${scenario.finalConversionPath}, got ${actualConversionPath}` };
  }
  if (scenario.expectedGuardrailCategory && finalPayload.guardrailDecision?.category !== scenario.expectedGuardrailCategory) {
    return { ok: false, reason: `expected guardrail ${scenario.expectedGuardrailCategory}, got ${finalPayload.guardrailDecision?.category}` };
  }
  for (const text of scenario.mustMention ?? []) {
    if (!answer.includes(normalizeText(text))) return { ok: false, reason: `missing expected mention: ${text}` };
  }
  for (const text of scenario.forbiddenFinal ?? []) {
    if (answer.includes(normalizeText(text))) return { ok: false, reason: `included forbidden text: ${text}` };
  }
  if (scenario.requireContactAsk && !asksForContact(answer)) {
    return { ok: false, reason: "expected contact capture question" };
  }
  if (scenario.requireRecommendationDetails) {
    const result = assertRecommendationDetails(finalPayload.recommendations);
    if (!result.ok) return result;
  }

  if (scenario.requireLead && salesToken) {
    const leadResult = await assertSalesInboxLead(salesInboxUrl, sessionId, actualConversionPath);
    if (!leadResult.ok) return leadResult;
  }

  return { ok: true };
}

function assertRecommendationDetails(recommendations) {
  if (!Array.isArray(recommendations) || recommendations.length < 1) {
    return { ok: false, reason: "expected at least one recommendation card" };
  }

  for (const item of recommendations) {
    if (!Array.isArray(item.agentIds) || item.agentIds.length < 1) {
      return { ok: false, reason: "recommendation card missing agentIds" };
    }
    if (!hasUsefulText(item.painSummary ?? item.nextQuestion, ["resolve"])) {
      return { ok: false, reason: `recommendation card missing pain summary for ${item.agentIds.join(",")}` };
    }
    if (!hasUsefulText(item.explanation, ["recomendei"])) {
      return { ok: false, reason: `recommendation card missing reason for ${item.agentIds.join(",")}` };
    }
    if (!hasUsefulText(item.exampleAction, ["na pratica"])) {
      return { ok: false, reason: `recommendation card missing practical action for ${item.agentIds.join(",")}` };
    }
  }

  return { ok: true };
}

function hasUsefulText(value, needles) {
  if (typeof value !== "string" || value.trim().length < 12) return false;
  const normalized = normalizeText(value);
  return needles.every((needle) => normalized.includes(normalizeText(needle)));
}

async function assertSalesInboxLead(endpointUrl, sessionId, conversionPath) {
  const response = await fetch(endpointUrl, {
    headers: { "x-internal-sales-token": salesToken },
  });
  if (!response.ok) return { ok: false, reason: `Sales Inbox HTTP ${response.status}` };
  const body = await response.json();
  const leads = Array.isArray(body.leads) ? body.leads : [];
  const lead = leads.find((item) => item.sessionId === sessionId && item.conversionPath === conversionPath);
  if (!lead) return { ok: false, reason: "expected Sales Inbox lead but none was found" };
  const syncStatus = lead.externalSyncStatus;
  if (!["pending", "synced", "failed", "skipped"].includes(syncStatus)) {
    return { ok: false, reason: `unexpected sync status ${syncStatus}` };
  }
  return { ok: true };
}

function asksForContact(text) {
  return /\b(whatsapp|email|e-mail|telefone|celular|contato)\b/.test(text) && /\b(qual|deixa|deixar|passa|passar|envia|enviar|retornar|retorno|prefere)\b/.test(text);
}

function normalizeText(value) {
  return String(value)
    .toLowerCase()
    .normalize("NFD")
    .replace(/\p{Diacritic}/gu, "");
}

function unique(values) {
  return Array.from(new Set(values.filter(Boolean)));
}
