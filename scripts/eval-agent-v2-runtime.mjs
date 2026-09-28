import { assert, writeReport } from "./eval-agent-v2-utils.mjs";

const baseUrl = process.env.AGENT_V2_EVAL_TARGET ?? "http://localhost:3999";
const now = () => Date.now().toString(36);

const scenarios = [
  {
    id: "runtime-widget-price-before-diagnostic",
    channel: "web",
    inputs: ["oi", "Lucas", "Quero ver planos", "pode recomendar sim"],
    expect: [
      ["Oi! Tudo bem?", "Em que posso te ajudar?"],
      ["Prazer, Lucas", "Em que posso te ajudar?"],
      ["Hoje a Taliya tem quatro faixas", "comparativo"],
      ["Hoje seu studio tem mais ou menos quantos alunos ativos?"],
    ],
  },
  {
    id: "runtime-widget-ideal-diagnostic-waitlist",
    channel: "web",
    inputs: [
      "oi",
      "Quero fazer diagnostico gratuito",
      "96",
      "Vendas e interessados",
      "Hoje uso WhatsApp e planilha",
      "Perco interessados por demora no retorno",
      "Quero aliviar WhatsApp e agenda primeiro",
      "Quero resolver agora, se fizer sentido",
      "faz sentido",
      "pode ser",
      "Studio do Lucas, Vitoria",
      "27996991427",
      "quanto custa depois?",
    ],
    expect: [
      ["Oi! Tudo bem?", "Em que posso te ajudar?"],
      ["Hoje seu studio tem mais ou menos quantos alunos ativos?"],
      ["Qual parte mais pesa hoje"],
      ["Hoje isso fica em algum sistema"],
      ["Quando alguém chama querendo conhecer"],
      ["qual tarefa você mais gostaria"],
      ["buscando resolver isso agora"],
      ["problema não está em uma rotina só", "agente de Atendimento", "agente de Vendas", "isso conversa com o que você precisa resolver agora"],
      ["número pequeno de studios", "lista de espera"],
      ["Qual é o nome do studio"],
      ["Qual WhatsApp ou email"],
      ["Perfeito, deixei seu studio na lista", "Quando abrir uma próxima janela"],
      ["Hoje a Taliya tem quatro faixas", "comparativo"],
    ],
    forbid: {
      8: ["compararia", "Plano para comparar"],
    },
  },
  {
    id: "runtime-whatsapp-user-reported-flow",
    channel: "whatsapp",
    profileName: "Lucas Quintino",
    inputs: [
      "Oi, quero ver como Taliya ficaria no meu studio de Pilates e entender o caminho para começar.",
      "Pode ser",
      "100",
      "Reposição é o mais complicado",
      "Caderno",
      "Consigo as vezes depende do dia",
      "Quero aliviar reposição primeiro",
      "Faz sentido",
      "Pode colocar",
      "Studio do Lucas, Vila Velha",
      "Quanto tempo leva até eu receber o chamado?",
    ],
    expect: [
      ["Oi, Lucas. Tudo bem?", "diagnóstico rápido da rotina"],
      ["Hoje seu studio tem mais ou menos quantos alunos ativos?"],
      ["Qual parte mais pesa hoje"],
      ["Hoje isso fica em algum sistema"],
      ["reposições ficam claras"],
      ["buscando resolver isso agora"],
      ["problema não é só reposição", "o de Agenda", "isso conversa com o que você precisa resolver agora"],
      ["número pequeno de studios", "lista de espera"],
      ["Qual é o nome do studio"],
      ["Perfeito, deixei seu studio na lista", "Quando abrir uma próxima janela"],
      ["Ainda não tenho uma data fechada", "Quando chegar a vez"],
    ],
    forbid: {
      8: ["compararia", "Plano para comparar", "Essencial"],
    },
  },
  {
    id: "runtime-whatsapp-first-direct-with-name",
    channel: "whatsapp",
    profileName: "Lucas Quintino",
    inputs: ["Quanto custa a Taliya?"],
    expect: [["Oi, Lucas. Tudo bem?", "Hoje a Taliya tem quatro faixas"]],
  },
  {
    id: "runtime-widget-human-handoff",
    channel: "web",
    inputs: ["quero falar com uma pessoa"],
    expect: [["Vou deixar uma pessoa assumir", "contexto salvo"]],
  },
  {
    id: "runtime-widget-demo-explain",
    channel: "web",
    inputs: ["Quero ver uma demo da Taliya", "Prefiro você me explicar o fluxo por aqui"],
    expect: [
      ["demonstração oficial", "/pilates/planos/demonstracao"],
      ["Na prática", "agentes entram em rotinas específicas"],
    ],
  },
  {
    id: "runtime-widget-price-demo-mixed",
    channel: "web",
    inputs: ["Vocês tem demo? E quanto custa mais ou menos?"],
    expect: [["Hoje a Taliya tem quatro faixas", "demonstração oficial"]],
  },
  {
    id: "runtime-widget-price-objection-small-studio",
    channel: "web",
    inputs: ["Achei caro, meu studio e pequeno"],
    expect: [["Faz sentido olhar o valor com cuidado", "diagn"]],
  },
  {
    id: "runtime-widget-existing-system-objection",
    channel: "web",
    inputs: ["Ja uso Tecnofit, por que eu usaria Taliya?"],
    expect: [["ferramenta solta", "Qual parte ainda pesa"]],
  },
  {
    id: "runtime-widget-mixed-sales-agenda-diagnostic",
    channel: "web",
    inputs: [
      "Perco interessados por demora no retorno e minha agenda fica baguncada",
      "Pode fazer",
      "96",
      "WhatsApp e planilha",
      "Nao vejo facil o que precisa resolver no dia",
      "Quero aliviar WhatsApp e agenda primeiro",
      "Quero resolver agora",
    ],
    expect: [
      ["diagnóstico rápido da rotina"],
      ["Hoje seu studio tem mais ou menos quantos alunos ativos?"],
      ["Hoje isso fica em algum sistema"],
      ["Quando alguém chama querendo conhecer"],
      ["qual tarefa você mais gostaria"],
      ["buscando resolver isso agora"],
      ["problema não está em uma rotina só", "agente de Vendas", "agente de Atendimento", "agente de Agenda"],
    ],
  },
  {
    id: "runtime-widget-diagnostic-cta-entry",
    channel: "web",
    entryPath: "diagnostic_cta",
    sourceSection: "studio_diagnostic",
    quickReplyId: "start_crm_diagnostic",
    inputs: ["Quero fazer diagnostico gratuito"],
    expect: [["Hoje seu studio tem mais ou menos quantos alunos ativos?"]],
  },
  {
    id: "runtime-widget-waitlist-pending-question",
    channel: "web",
    inputs: ["Quero assinar agora", "Pode colocar", "Studio Plano, Vila Velha", "Quanto tempo leva para chamar?"],
    expect: [
      ["número pequeno de studios", "lista de espera"],
      ["Qual é o nome do studio"],
      ["Qual WhatsApp ou email"],
      ["Ainda não tenho uma data fechada", "Qual WhatsApp ou email"],
    ],
  },
];

const results = [];
const transcripts = [];

for (const scenario of scenarios) {
  const session = createSession(scenario);
  const transcript = [];
  for (const [index, input] of scenario.inputs.entries()) {
    const response = await postJson(`${baseUrl}/api/landing/ai-attendant`, {
      session,
      userMessage: input,
      quickReplyId: index === 0 ? scenario.quickReplyId : undefined,
    });
    if (!response.ok) {
      results.push(assert(false, `${scenario.id} turn ${index + 1} HTTP ${response.status}`, { body: response.body }));
      break;
    }
    const payload = response.body;
    const assistantTexts = Array.isArray(payload.assistantMessages)
      ? payload.assistantMessages.map((message) => message.content).filter(Boolean)
      : [];
    transcript.push({ user: input, assistant: assistantTexts });
    session.messages.push({ id: `user_${index}`, role: "user", content: input });
    for (const message of payload.assistantMessages ?? []) session.messages.push(message);
    session.qualificationDraft = {
      ...(session.qualificationDraft ?? {}),
      ...(payload.qualificationPatch ?? {}),
    };
    session.selectedPainIds = payload.capturedPainIds?.length ? payload.capturedPainIds : session.selectedPainIds;
    session.recommendedAgentIds = payload.recommendedAgentIds?.length ? payload.recommendedAgentIds : session.recommendedAgentIds;

    const expected = scenario.expect[index] ?? [];
    const joined = assistantTexts.join("\n");
    for (const snippet of expected) {
      results.push(assert(joined.includes(snippet), `${scenario.id} turn ${index + 1} contains "${snippet}"`, { input, assistantTexts }));
    }
    for (const snippet of scenario.forbid?.[index + 1] ?? []) {
      results.push(assert(!joined.includes(snippet), `${scenario.id} turn ${index + 1} does not contain "${snippet}"`, { input, assistantTexts }));
    }
  }
  transcripts.push({ id: scenario.id, transcript });
}

const webhookResult = await runWhatsAppWebhookProbe();
results.push(...webhookResult.results);
transcripts.push(webhookResult.transcript);

writeReport("agent-v2-runtime", results, {
  target: baseUrl,
  transcripts,
});

function createSession(scenario) {
  const id = `${scenario.id}_${now()}`;
  const qualificationDraft = {};
  if (scenario.profileName) qualificationDraft.name = scenario.profileName;
  return {
    sessionId: id,
    channel: scenario.channel,
    channelSessionId: scenario.channel === "whatsapp" ? `wa_${id}` : undefined,
    entryPath: scenario.entryPath ?? (scenario.channel === "whatsapp" ? "whatsapp_cta" : "widget"),
    sourceSection: scenario.sourceSection ?? (scenario.channel === "whatsapp" ? "whatsapp" : "widget"),
    niche: "pilates",
    sourcePage: scenario.channel === "whatsapp" ? "whatsapp" : "/pilates",
    campaignStage: "commercial",
    publicOfferMode: "direct_saas_subscription",
    messages: [],
    selectedPainIds: [],
    recommendedAgentIds: [],
    qualificationDraft,
    externalContact:
      scenario.channel === "whatsapp"
        ? {
            type: "whatsapp",
            phone: "+5527999990000",
            providerContactId: `5527999990000_${id}`,
            phoneNumberId: "12345",
            displayPhoneNumber: "+55 27 92001-5824",
          }
        : undefined,
  };
}

async function runWhatsAppWebhookProbe() {
  const providerMessageId = `wamid.${now()}`;
  const waId = `552799${Math.floor(100000 + Math.random() * 899999)}`;
  const body = {
    object: "whatsapp_business_account",
    entry: [
      {
        id: "waba_test",
        changes: [
          {
            field: "messages",
            value: {
              messaging_product: "whatsapp",
              metadata: {
                display_phone_number: "5527920015824",
                phone_number_id: "12345",
              },
              contacts: [
                {
                  profile: { name: "Lucas Quintino" },
                  wa_id: waId,
                },
              ],
              messages: [
                {
                  from: waId,
                  id: providerMessageId,
                  timestamp: String(Math.floor(Date.now() / 1000)),
                  text: { body: "Oi, quero entender os planos" },
                  type: "text",
                },
              ],
            },
          },
        ],
      },
    ],
  };
  const response = await postJson(`${baseUrl}/api/landing/ai-attendant/whatsapp`, body);
  const resultBody = response.body;
  const previews = resultBody?.results?.[0]?.replyPreviews ?? [];
  return {
    transcript: {
      id: "runtime-whatsapp-webhook-probe",
      transcript: [{ user: "Oi, quero entender os planos", assistant: previews }],
    },
    results: [
      assert(response.ok, "WhatsApp webhook probe returns HTTP 200", { status: response.status, body: resultBody }),
      assert(resultBody?.status === "processed", "WhatsApp webhook probe processed", { body: resultBody }),
      assert(previews.length >= 2, "WhatsApp webhook probe sends separated messages", { previews }),
      assert(previews.join("\n").includes("Hoje a Taliya tem quatro faixas"), "WhatsApp webhook probe answers plans", { previews }),
    ],
  };
}

async function postJson(url, body) {
  const response = await fetch(url, {
    method: "POST",
    headers: { "content-type": "application/json" },
    body: JSON.stringify(body),
  });
  let parsed;
  try {
    parsed = await response.json();
  } catch {
    parsed = await response.text();
  }
  return { ok: response.ok, status: response.status, body: parsed };
}
