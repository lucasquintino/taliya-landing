#!/usr/bin/env node

const targetArg = process.argv.find((arg) => arg.startsWith("--target="));
const target = targetArg?.slice("--target=".length) || process.env.AI_ATTENDANT_EVAL_TARGET;
const salesTokenArg = process.argv.find((arg) => arg.startsWith("--sales-token="));
const salesToken = salesTokenArg?.slice("--sales-token=".length) || process.env.INTERNAL_SALES_INBOX_TOKEN;
const caseArg = process.argv.find((arg) => arg.startsWith("--case="));
const caseFilter = caseArg ? new Set(caseArg.slice("--case=".length).split(",").map((item) => item.trim()).filter(Boolean)) : undefined;
const maxArg = process.argv.find((arg) => arg.startsWith("--max-cases="));
const maxCases = maxArg ? Number(maxArg.slice("--max-cases=".length)) : undefined;

const scenarios = [
  {
    id: "HUM-001",
    title: "Cold broad routine does not get pushed to plans",
    turns: ["Tenho um studio de pilates e gostaria de melhorar minha rotina."],
    expectedFinal: "none",
    forbiddenPaths: ["checkout_intent", "view_plans", "plan_recommendation"],
    requireQuestion: true,
    requireSimpleLanguage: true,
  },
  {
    id: "HUM-002",
    title: "Basic product question sounds consultative",
    turns: ["O que exatamente e a Taliya?"],
    expectedFinal: "none",
    mustMentionAny: ["studio", "pilates"],
    forbiddenText: ["so um chatbot", "apenas um chatbot"],
    requireQuestion: true,
    requireSimpleLanguage: true,
  },
  {
    id: "HUM-003",
    title: "Price first gets answered without checkout pressure",
    turns: ["Quanto custa?"],
    expectedFinal: "none",
    mustMentionAny: ["base", "agente", "plano"],
    forbiddenText: ["com quem eu falo", "demo fica melhor", "demo real ainda nao esta disponivel"],
    forbiddenPaths: ["checkout_intent"],
    requireQuestion: true,
    requireSimpleLanguage: true,
  },
  {
    id: "HUM-004",
    title: "Explicit plan comparison is answered without checkout pressure",
    turns: ["Quero ver os planos e comparar."],
    expectedFinal: "view_plans",
    mustMentionAny: ["base", "1", "3", "7"],
    forbiddenText: ["demo real ainda nao esta disponivel"],
    forbiddenPaths: ["checkout_intent"],
    requireSimpleLanguage: true,
  },
  {
    id: "HUM-013",
    title: "Cold plan question does not fall into demo fallback",
    turns: ["Quais planos vcs tem?"],
    expectedFinal: "none",
    mustMentionAny: ["base", "1 agente", "3 agentes", "7 agentes"],
    forbiddenText: ["demo real ainda nao esta disponivel", "com quem eu falo"],
    forbiddenPaths: ["checkout_intent", "guided_demo"],
    requireQuestion: true,
    requireSimpleLanguage: true,
  },
  {
    id: "HUM-014",
    title: "Name-only cold reply does not trigger plans or recommendations",
    turns: ["Lucas"],
    expectedFinal: "none",
    mustMentionAny: ["prazer", "diagnostico", "duvida"],
    forbiddenText: ["demo real ainda nao esta disponivel", "agentes indicados"],
    forbiddenPaths: ["checkout_intent", "view_plans", "plan_recommendation", "guided_demo"],
    forbidRecommendations: true,
    requireQuestion: true,
    requireSimpleLanguage: true,
  },
  {
    id: "HUM-015",
    title: "WhatsApp cold greeting asks name before any funnel",
    channel: "whatsapp",
    turns: ["ola"],
    expectedFinal: "none",
    mustMentionAny: ["qual seu nome"],
    forbiddenText: ["diagnostico gratuito", "lista de espera", "planos sao", "demo"],
    forbiddenPaths: ["checkout_intent", "view_plans", "plan_recommendation", "guided_demo", "waitlist_intent"],
    requireQuestion: true,
    requireSimpleLanguage: true,
  },
  {
    id: "HUM-016",
    title: "WhatsApp cold price question answers price before diagnostic option",
    channel: "whatsapp",
    turns: ["quais os valores?"],
    expectedFinal: "none",
    mustMentionAny: ["r$", "planos", "diagnostico"],
    forbiddenText: ["lista de espera", "assinar agora"],
    forbiddenPaths: ["checkout_intent", "view_plans", "plan_recommendation", "guided_demo", "waitlist_intent"],
    requireQuestion: true,
    requireSimpleLanguage: true,
  },
  {
    id: "HUM-017",
    title: "WhatsApp asks pain after name and offers diagnostic after pain",
    channel: "whatsapp",
    turns: ["Lucas", "agenda e reposicoes estao baguncadas"],
    expectedFinal: "none",
    mustMentionAny: ["diagnostico gratuito"],
    forbiddenText: ["lista de espera", "assinar agora"],
    forbiddenPaths: ["checkout_intent", "view_plans", "plan_recommendation", "guided_demo", "waitlist_intent"],
    requireQuestion: true,
    requireSimpleLanguage: true,
  },
  {
    id: "HUM-018",
    title: "Positive answer after diagnostic offers waitlist",
    turns: ["faz sentido, gostei"],
    initialQualificationDraft: {
      name: "Lucas",
      diagnosticCompleted: "true",
      diagnosticStatus: "completed",
      primaryPainOrIntent: "reposicoes e vendas",
      operationalPains: "reposicoes, vendas",
    },
    expectedFinal: "waitlist_intent",
    mustMentionAny: ["numero pequeno", "lista de espera"],
    forbiddenText: ["checkout", "assinar agora"],
    requireQuestion: true,
    expectedQualification: {
      waitlistStatus: "offered",
      commercialStage: "waitlist_offered",
    },
    expectedLeadFields: {
      waitlistStatus: "offered",
      commercialStage: "waitlist_offered",
      conversionPath: "waitlist_intent",
    },
    requireLead: true,
    requireSimpleLanguage: true,
  },
  {
    id: "HUM-019",
    title: "Waitlist acceptance with missing fields stays pending details",
    channel: "whatsapp",
    turns: ["pode colocar"],
    initialQualificationDraft: {
      name: "Lucas",
      primaryPainOrIntent: "reposicoes",
      waitlistStatus: "offered",
      commercialStage: "waitlist_offered",
      whatsapp: "27999999999",
    },
    expectedFinal: "waitlist_intent",
    mustMentionAny: ["studio", "cidade"],
    expectedQualification: {
      waitlistStatus: "pending_details",
      commercialStage: "waitlist_pending_details",
    },
    expectedLeadFields: {
      waitlistStatus: "pending_details",
      commercialStage: "waitlist_pending_details",
      conversionPath: "waitlist_intent",
    },
    requireLead: true,
    requireSimpleLanguage: true,
  },
  {
    id: "HUM-020",
    title: "Refused name with direct question still gets a useful answer",
    channel: "whatsapp",
    turns: ["prefiro nao falar meu nome, quanto custa?"],
    expectedFinal: "none",
    mustMentionAny: ["planos"],
    forbiddenText: ["lista de espera", "nao posso ajudar"],
    forbiddenPaths: ["waitlist_intent", "checkout_intent"],
    requireQuestion: true,
    requireSimpleLanguage: true,
  },
  {
    id: "HUM-025",
    title: "Waitlist details parse studio and city from one message",
    channel: "web",
    turns: ["studio do lucas, vila velha"],
    initialQualificationDraft: {
      name: "Lucas",
      whatsapp: "27996991427",
      primaryPainOrIntent: "reposicoes",
      waitlistStatus: "pending_details",
      commercialStage: "waitlist_pending_details",
    },
    expectedFinal: "waitlist_intent",
    mustMentionAny: ["completo", "lista de espera"],
    forbiddenText: ["diagnostico", "isso faz sentido para o momento"],
    expectedQualification: {
      waitlistStatus: "joined",
      commercialStage: "waitlist_joined",
    },
    requireLead: true,
    requireSimpleLanguage: true,
  },
  {
    id: "HUM-026",
    title: "Waitlist pending city-only reply completes instead of restarting diagnostic",
    channel: "web",
    turns: ["vila velha"],
    initialQualificationDraft: {
      name: "Lucas",
      whatsapp: "27996991427",
      studioName: "studio do lucas",
      primaryPainOrIntent: "reposicoes",
      diagnosticType: "crm_agent_diagnostic",
      diagnosticCompleted: "true",
      diagnosticStatus: "completed",
      waitlistStatus: "pending_details",
      commercialStage: "waitlist_pending_details",
    },
    expectedFinal: "waitlist_intent",
    mustMentionAny: ["lista de espera"],
    forbiddenText: ["Ok, ja tenho as informacoes necessarias", "isso faz sentido para o momento"],
    expectedQualification: {
      waitlistStatus: "joined",
      commercialStage: "waitlist_joined",
    },
    requireLead: true,
    requireSimpleLanguage: true,
  },
  {
    id: "HUM-027",
    title: "Waitlist details accept comma-separated studio and city even when studio matches name",
    channel: "web",
    turns: ["lucas, vitoria"],
    initialQualificationDraft: {
      name: "Lucas",
      whatsapp: "27996991427",
      primaryPainOrIntent: "vendas e interessados",
      diagnosticType: "crm_agent_diagnostic",
      diagnosticCompleted: "true",
      diagnosticStatus: "completed",
      waitlistStatus: "pending_details",
      commercialStage: "waitlist_pending_details",
    },
    expectedFinal: "waitlist_intent",
    mustMentionAny: ["lista de espera"],
    forbiddenText: ["Qual e o nome do studio", "De qual cidade", "Ok, ja tenho as informacoes necessarias"],
    expectedQualification: {
      waitlistStatus: "joined",
      commercialStage: "waitlist_joined",
      studioName: "lucas",
      cityState: "vitoria",
      studioCity: "vitoria",
    },
    requireLead: true,
    requireSimpleLanguage: true,
  },
  {
    id: "HUM-028",
    title: "Waitlist joined follow-up explains next steps instead of restarting diagnostic",
    channel: "web",
    turns: ["e agora?"],
    initialQualificationDraft: {
      name: "Lucas",
      whatsapp: "27996991427",
      studioName: "Studio do Lucas",
      cityState: "Vitoria",
      studioCity: "Vitoria",
      primaryPainOrIntent: "WhatsApp, vendas e agenda",
      diagnosticType: "crm_agent_diagnostic",
      diagnosticCompleted: "true",
      diagnosticStatus: "completed",
      waitlistStatus: "joined",
      commercialStage: "waitlist_joined",
    },
    expectedFinal: "waitlist_intent",
    mustMentionAny: ["lista de espera", "proxima janela", "contato"],
    forbiddenText: [
      "Ok, ja tenho as informacoes necessarias",
      "Pelo que voce contou",
      "Isso faz sentido para o momento",
      "Quer que eu coloque",
    ],
    expectedQualification: {
      waitlistStatus: "joined",
      commercialStage: "waitlist_joined",
    },
    expectedLeadFields: {
      waitlistStatus: "joined",
      commercialStage: "waitlist_joined",
      conversionPath: "waitlist_intent",
    },
    requireLead: true,
    requireQuestion: true,
    requireSimpleLanguage: true,
  },
  {
    id: "HUM-029",
    title: "Known-name Taliya fit exploration bridges naturally to diagnostic",
    channel: "web",
    turns: ["Lucas", "quero ver como Taliya ficaria no meu studio..."],
    expectedFinal: "none",
    mustMentionAny: ["rotina real", "diagnostico gratuito", "partes fariam sentido"],
    forbiddenText: ["ponto agora parece", "demo real ainda nao"],
    forbiddenPaths: ["checkout_intent", "view_plans", "plan_recommendation", "guided_demo", "waitlist_intent"],
    requireQuestion: true,
    requireSimpleLanguage: true,
  },
  {
    id: "HUM-030",
    title: "Waitlist joined timeline question stays in post-waitlist mode",
    channel: "web",
    turns: ["quando voces vao chamar?"],
    initialQualificationDraft: joinedWaitlistDraft(),
    expectedFinal: "waitlist_intent",
    mustMentionAny: ["proxima janela", "contato", "lista de espera"],
    forbiddenText: ["Ok, ja tenho as informacoes necessarias", "Pelo que voce contou", "diagnostico gratuito"],
    expectedQualification: {
      waitlistStatus: "joined",
      commercialStage: "waitlist_joined",
    },
    requireQuestion: true,
    requireLead: true,
    requireSimpleLanguage: true,
  },
  {
    id: "HUM-031",
    title: "Waitlist joined contact update changes contact without restarting diagnostic",
    channel: "web",
    turns: ["meu contato mudou, usa 27 98888-7777"],
    initialQualificationDraft: joinedWaitlistDraft(),
    expectedFinal: "waitlist_intent",
    mustMentionAny: ["contato", "atualizado", "lista de espera"],
    forbiddenText: ["Ok, ja tenho as informacoes necessarias", "Pelo que voce contou", "Qual WhatsApp usamos"],
    expectedQualification: {
      waitlistStatus: "joined",
      commercialStage: "waitlist_joined",
      whatsapp: "27 98888-7777",
    },
    requireLead: true,
    requireSimpleLanguage: true,
  },
  {
    id: "HUM-032",
    title: "Waitlist joined human request routes to human handoff",
    channel: "web",
    turns: ["quero falar com uma pessoa"],
    initialQualificationDraft: joinedWaitlistDraft(),
    expectedFinal: "human_whatsapp_assist",
    mustMentionAny: ["pessoa", "contexto"],
    forbiddenText: ["diagnostico gratuito", "Ok, ja tenho as informacoes necessarias", "Pelo que voce contou"],
    expectedQualification: {
      waitlistStatus: "joined",
      commercialStage: "human_handoff",
    },
    requireQuestion: true,
    requireLead: true,
    requireSimpleLanguage: true,
  },
  {
    id: "HUM-033",
    title: "Waitlist joined opt-out removes waitlist state without restarting diagnostic",
    channel: "web",
    turns: ["nao quero mais ficar na lista"],
    initialQualificationDraft: joinedWaitlistDraft(),
    expectedFinal: "waitlist_intent",
    mustMentionAny: ["sem problema", "retirei"],
    forbiddenText: ["diagnostico gratuito", "Ok, ja tenho as informacoes necessarias", "Pelo que voce contou"],
    expectedQualification: {
      waitlistStatus: "declined",
      commercialStage: "waitlist_declined",
    },
    requireLead: true,
    requireSimpleLanguage: true,
  },
  {
    id: "HUM-034",
    title: "Waitlist joined WhatsApp doubt gets answered without diagnostic restart",
    channel: "web",
    turns: ["como funciona o WhatsApp da Taliya?"],
    initialQualificationDraft: joinedWaitlistDraft(),
    expectedFinal: "waitlist_intent",
    mustMentionAny: ["WhatsApp", "equipe", "lista de espera"],
    forbiddenText: ["diagnostico gratuito", "Ok, ja tenho as informacoes necessarias", "Pelo que voce contou"],
    expectedQualification: {
      waitlistStatus: "joined",
      commercialStage: "waitlist_joined",
    },
    requireQuestion: true,
    requireLead: true,
    requireSimpleLanguage: true,
  },
  {
    id: "HUM-035",
    title: "Waitlist joined guarantee doubt gets answered directly",
    channel: "web",
    turns: ["tem garantia ou posso cancelar?"],
    initialQualificationDraft: joinedWaitlistDraft(),
    expectedFinal: "waitlist_intent",
    mustMentionAny: ["30 dias", "cancelar", "garantia"],
    forbiddenText: ["diagnostico gratuito", "Ok, ja tenho as informacoes necessarias", "Pelo que voce contou"],
    expectedQualification: {
      waitlistStatus: "joined",
      commercialStage: "waitlist_joined",
    },
    requireQuestion: true,
    requireLead: true,
    requireSimpleLanguage: true,
  },
  {
    id: "HUM-036",
    title: "Waitlist joined plan change doubt gets answered directly",
    channel: "web",
    turns: ["se eu comecar em um plano menor consigo trocar depois?"],
    initialQualificationDraft: joinedWaitlistDraft(),
    expectedFinal: "waitlist_intent",
    mustMentionAny: ["trocar", "ajustar", "comecar menor"],
    forbiddenText: ["diagnostico gratuito", "Ok, ja tenho as informacoes necessarias", "Pelo que voce contou"],
    expectedQualification: {
      waitlistStatus: "joined",
      commercialStage: "waitlist_joined",
    },
    requireQuestion: true,
    requireLead: true,
    requireSimpleLanguage: true,
  },
  {
    id: "HUM-037",
    title: "Waitlist joined setup doubt gets answered directly",
    channel: "web",
    turns: ["quem configura tudo no comeco?"],
    initialQualificationDraft: joinedWaitlistDraft(),
    expectedFinal: "waitlist_intent",
    mustMentionAny: ["configuracao", "setup", "regras do studio"],
    forbiddenText: ["diagnostico gratuito", "Ok, ja tenho as informacoes necessarias", "Pelo que voce contou"],
    expectedQualification: {
      waitlistStatus: "joined",
      commercialStage: "waitlist_joined",
    },
    requireQuestion: true,
    requireLead: true,
    requireSimpleLanguage: true,
  },
  {
    id: "HUM-038",
    title: "Waitlist joined price question answers values without offering diagnostic again",
    channel: "web",
    turns: ["quanto custa mesmo?"],
    initialQualificationDraft: joinedWaitlistDraft(),
    expectedFinal: "waitlist_intent",
    mustMentionAny: ["R$", "Base", "Completo"],
    forbiddenText: ["diagnostico gratuito", "Ok, ja tenho as informacoes necessarias", "Pelo que voce contou"],
    expectedQualification: {
      waitlistStatus: "joined",
      commercialStage: "waitlist_joined",
    },
    requireQuestion: true,
    requireLead: true,
    requireSimpleLanguage: true,
  },
  {
    id: "HUM-039",
    title: "Waitlist joined plan comparison can still route to plans",
    channel: "web",
    turns: ["quero ver o comparativo de planos"],
    initialQualificationDraft: joinedWaitlistDraft(),
    expectedFinal: "view_plans",
    mustMentionAny: ["Base", "Essencial", "Avance", "Completo"],
    forbiddenText: ["diagnostico gratuito", "Ok, ja tenho as informacoes necessarias", "Pelo que voce contou"],
    expectedQualification: {
      waitlistStatus: "joined",
      commercialStage: "waitlist_joined",
    },
    requireQuestion: true,
    requireLead: true,
    requireSimpleLanguage: true,
  },
  {
    id: "HUM-040",
    title: "Waitlist joined open product doubt is answered and stored without diagnostic restart",
    channel: "web",
    turns: ["como funciona a parte financeira?"],
    initialQualificationDraft: joinedWaitlistDraft(),
    expectedFinal: "waitlist_intent",
    mustMentionAny: ["financeiro", "cobranca"],
    forbiddenText: ["diagnostico gratuito", "Ok, ja tenho as informacoes necessarias", "Pelo que voce contou"],
    expectedQualification: {
      waitlistStatus: "joined",
      commercialStage: "waitlist_joined",
      diagnosticCompleted: "true",
    },
    requireQuestion: true,
    requireLead: true,
    requireSimpleLanguage: true,
  },
  {
    id: "HUM-021",
    title: "Negative answer after diagnostic does not offer waitlist",
    channel: "whatsapp",
    turns: ["nao sei se faz sentido pra mim"],
    initialQualificationDraft: {
      name: "Lucas",
      whatsapp: "5511999999999",
      studioName: "Studio Teste",
      cityState: "Vitoria/ES",
      diagnosticType: "crm_agent_diagnostic",
      diagnosticCompleted: "true",
      diagnosticStatus: "completed",
      primaryPainOrIntent: "Reposicoes e WhatsApp",
      waitlistStatus: "not_offered",
    },
    expectedFinal: "none",
    mustMentionAny: ["demo", "duvida", "explicar"],
    forbiddenText: ["lista de espera", "pode colocar seu studio"],
    forbiddenPaths: ["waitlist_intent", "checkout_intent"],
    requireQuestion: true,
    requireSimpleLanguage: true,
  },
  {
    id: "HUM-022",
    title: "Positive answer after demo offers waitlist",
    channel: "whatsapp",
    turns: ["gostei, quero seguir"],
    initialQualificationDraft: {
      name: "Lucas",
      whatsapp: "5511999999999",
      studioName: "Studio Teste",
      cityState: "Vitoria/ES",
      diagnosticStatus: "completed",
      primaryPainOrIntent: "Agenda e vendas",
      demoStatus: "viewed_discussed",
      waitlistStatus: "not_offered",
    },
    expectedFinal: "waitlist_intent",
    mustMentionAny: ["numero pequeno", "lista de espera"],
    expectedQualification: {
      waitlistStatus: "offered",
      commercialStage: "waitlist_offered",
    },
    expectedLeadFields: {
      waitlistStatus: "offered",
      commercialStage: "waitlist_offered",
      conversionPath: "waitlist_intent",
    },
    requireLead: true,
    requireQuestion: true,
    requireSimpleLanguage: true,
  },
  {
    id: "HUM-023",
    title: "Negative answer after demo does not offer waitlist",
    channel: "whatsapp",
    turns: ["nao era isso que eu esperava"],
    initialQualificationDraft: {
      name: "Lucas",
      whatsapp: "5511999999999",
      studioName: "Studio Teste",
      cityState: "Vitoria/ES",
      diagnosticStatus: "completed",
      primaryPainOrIntent: "WhatsApp e agenda",
      demoStatus: "viewed_discussed",
      waitlistStatus: "not_offered",
    },
    expectedFinal: "none",
    mustMentionAny: ["nao vou te colocar", "nao ficou claro", "valor", "funcionamento"],
    forbiddenText: ["quer que eu coloque o studio na lista"],
    forbiddenPaths: ["waitlist_intent", "checkout_intent"],
    expectedQualification: {
      waitlistStatus: "undecided",
      demoStatus: "negative",
    },
    requireQuestion: true,
    requireSimpleLanguage: true,
  },
  {
    id: "HUM-024",
    title: "Waitlist declined is stored without joined state",
    channel: "whatsapp",
    turns: ["nao agora"],
    initialQualificationDraft: {
      name: "Lucas",
      whatsapp: "5511999999999",
      studioName: "Studio Teste",
      cityState: "Vitoria/ES",
      diagnosticStatus: "completed",
      primaryPainOrIntent: "Vendas e WhatsApp",
      waitlistStatus: "offered",
    },
    expectedFinal: "waitlist_intent",
    mustMentionAny: ["nao vou te colocar", "sem problema"],
    expectedQualification: {
      waitlistStatus: "declined",
      commercialStage: "waitlist_declined",
    },
    expectedLeadFields: {
      waitlistStatus: "declined",
      commercialStage: "waitlist_declined",
      conversionPath: "waitlist_intent",
    },
    requireLead: true,
    requireQuestion: true,
    requireSimpleLanguage: true,
  },
  {
    id: "HUM-005",
    title: "Buy intent without diagnostic confirms plan before checkout",
    turns: ["Quero assinar agora."],
    allowedFinal: ["none", "plan_recommendation"],
    mustMentionAny: ["plano", "studio", "assinatura"],
    forbiddenPaths: ["checkout_intent"],
    requireQuestion: true,
    requireSimpleLanguage: true,
  },
  {
    id: "HUM-006",
    title: "Checkout intent keeps diagnostic-first gate when context is incomplete",
    turns: [
      "Tenho 120 alunos, muitas reposicoes e WhatsApp baguncado. Qual plano faz sentido?",
      "Lucas, meu WhatsApp e 11999999999.",
      "Minhas maiores dores sao reposicoes, faltas, vendas e financeiro.",
      "Hoje uso planilha e WhatsApp. Nao consigo ver facil o que resolver no dia.",
      "Reposicoes viram muita troca de mensagem.",
      "Interessados ficam sem retorno.",
      "Quero resolver agora.",
      "Quero fechar o plano recomendado, pode mandar o link.",
    ],
    expectedFinal: "none",
    mustMentionAny: ["diagnostico", "plano", "studio"],
    forbiddenText: ["cartao por aqui", "manda o cvv"],
    requireSimpleLanguage: true,
  },
  {
    id: "HUM-007",
    title: "Human/WhatsApp request creates explicit handoff without checkout",
    turns: ["Quero falar com uma pessoa antes de assinar."],
    expectedFinal: "human_whatsapp_assist",
    requireContactAsk: true,
    requireLead: true,
    forbiddenPaths: ["checkout_intent"],
    requireSimpleLanguage: true,
  },
  {
    id: "HUM-008",
    title: "Custom marketing request becomes custom agent follow-up",
    turns: ["Quero um agente de marketing para Instagram e campanhas."],
    expectedFinal: "custom_agent_follow_up",
    mustMentionAny: ["sob medida", "marketing"],
    requireContactAsk: true,
    requireLead: true,
    requireSimpleLanguage: true,
  },
  {
    id: "HUM-009",
    title: "Expensive objection is handled without discount",
    turns: [
      "Tenho 80 alunos e me perco em leads, reposicoes e cobrancas.",
      "Achei caro.",
    ],
    allowedFinal: ["none"],
    mustMentionAny: ["diagnostico", "com quem eu falo", "rotina"],
    forbiddenText: ["desconto", "resultado garantido"],
    forbiddenPaths: ["checkout_intent"],
    requireQuestion: true,
    requireContactAsk: true,
    requireSimpleLanguage: true,
  },
  {
    id: "HUM-010",
    title: "Receptionist objection positions leverage",
    turns: ["Ja tenho recepcionista. Por que eu precisaria disso?"],
    allowedFinal: ["none", "plan_recommendation"],
    mustMentionAny: ["tarefas repetidas", "duvidas", "lembrar aluno", "reposicao"],
    forbiddenText: ["substituir sua recepcionista", "demitir"],
    forbiddenPaths: ["checkout_intent"],
    requireQuestion: true,
    forbidContactAsk: true,
    requireSimpleLanguage: true,
  },
  {
    id: "HUM-011",
    title: "AI trust objection explains control",
    turns: ["Tenho medo da IA responder errado."],
    allowedFinal: ["none", "plan_recommendation"],
    mustMentionAny: ["regras", "respostas aprovadas", "chamar uma pessoa"],
    forbiddenText: ["nunca erra", "100% garantido"],
    forbiddenPaths: ["checkout_intent"],
    requireQuestion: true,
    forbidContactAsk: true,
    requireSimpleLanguage: true,
  },
  {
    id: "HUM-012",
    title: "Unsupported integration does not invent support",
    turns: ["Integra com o sistema X que eu uso no studio?"],
    expectedFinal: "none",
    mustMentionAny: ["nao", "confirmar", "sistema"],
    forbiddenText: ["sim, integra", "ja integra", "integracao pronta"],
    requireQuestion: true,
    forbidContactAsk: true,
    requireSimpleLanguage: true,
  },
];

function joinedWaitlistDraft() {
  return {
    name: "Lucas",
    whatsapp: "27996991427",
    studioName: "Studio do Lucas",
    cityState: "Vitoria",
    studioCity: "Vitoria",
    primaryPainOrIntent: "WhatsApp, vendas e agenda",
    diagnosticType: "crm_agent_diagnostic",
    diagnosticCompleted: "true",
    diagnosticStatus: "completed",
    waitlistStatus: "joined",
    commercialStage: "waitlist_joined",
  };
}

if (!target) {
  console.log(`AI sales humanization eval harness ready: ${scenarios.length} realistic scenarios configured.`);
  for (const scenario of scenarios) console.log(`- ${scenario.id}: ${scenario.title}`);
  console.log("\nRun with: npm run eval:ai-sales-humanization -- --target=http://localhost:3000");
  process.exit(0);
}

const endpoint = new URL("/api/landing/ai-attendant", target).toString();
const salesInboxEndpoint = new URL("/api/internal/sales-inbox/leads", target).toString();
const runnable = scenarios
  .filter((scenario) => !caseFilter || caseFilter.has(scenario.id))
  .slice(0, Number.isFinite(maxCases) ? maxCases : undefined);
const results = [];

for (const scenario of runnable) {
  const result = await runScenario(endpoint, salesInboxEndpoint, scenario);
  results.push(result);
  const label = result.ok ? "PASS" : "FAIL";
  console.log(`${label} ${scenario.id}: ${scenario.title}${result.reason ? ` - ${result.reason}` : ""}`);
  if (result.costTokens) console.log(`  tokens input=${result.costTokens.inputTokens ?? "?"} output=${result.costTokens.outputTokens ?? "?"}`);
}

const failed = results.filter((result) => !result.ok);
console.log(`\nAI sales humanization evals: ${results.length - failed.length}/${results.length} passed.`);
if (failed.length) process.exit(1);

async function runScenario(endpointUrl, salesInboxUrl, scenario) {
  const sessionId = `eval_human_${scenario.id.toLowerCase()}_${Date.now()}`;
  const messages = [];
  const qualificationDraft = { ...(scenario.initialQualificationDraft ?? {}) };
  const channel = scenario.channel ?? "web";
  let finalPayload;

  for (let index = 0; index < scenario.turns.length; index += 1) {
    const userMessage = scenario.turns[index];
    messages.push({
      id: `user_${index}`,
      role: "user",
      content: userMessage,
    });

    const response = await fetch(endpointUrl, {
      method: "POST",
      headers: { "content-type": "application/json" },
      body: JSON.stringify({
        session: {
          sessionId,
          channel,
          channelSessionId: channel === "whatsapp" ? `${sessionId}_contact` : undefined,
          entryPath: channel === "whatsapp" ? "whatsapp_cta" : index === 0 ? "widget" : "consultor_cta",
          niche: "pilates",
          sourcePage: channel === "whatsapp" ? "whatsapp" : "/pilates",
          campaignStage: "commercial",
          publicOfferMode: "direct_saas_subscription",
          messages: messages.slice(0, -1),
          qualificationDraft,
          externalContact:
            channel === "whatsapp"
              ? {
                  type: "whatsapp",
                  phone: "5511999999999",
                  providerContactId: `${sessionId}_contact`,
                  phoneNumberId: "phone_number_test",
                }
              : undefined,
        },
        userMessage,
        pageSignals: {},
      }),
    });

    if (!response.ok) return { ok: false, reason: `HTTP ${response.status} on turn ${index + 1}` };

    const payload = await response.json();
    finalPayload = payload;
    Object.assign(qualificationDraft, payload.qualificationPatch ?? {});
    for (const assistantMessage of payload.assistantMessages ?? []) {
      messages.push({
        id: assistantMessage.id ?? `assistant_${index}`,
        role: "assistant",
        content: assistantMessage.content ?? "",
        intent: assistantMessage.intent,
      });
    }

    if ((scenario.forbiddenPaths ?? []).includes(payload.conversionPath)) {
      return { ok: false, reason: `forbidden conversionPath ${payload.conversionPath} on turn ${index + 1}` };
    }
  }

  if (!finalPayload) return { ok: false, reason: "no payload returned" };

  const finalPath = finalPayload.conversionPath ?? "none";
  const answer = normalizeText((finalPayload.assistantMessages ?? []).map((message) => message.content ?? "").join("\n"));
  const rawAnswer = (finalPayload.assistantMessages ?? []).map((message) => message.content ?? "").join("\n");

  if (scenario.expectedFinal && finalPath !== scenario.expectedFinal) {
    return { ok: false, reason: `expected final conversionPath ${scenario.expectedFinal}, got ${finalPath}` };
  }
  if (scenario.allowedFinal && !scenario.allowedFinal.includes(finalPath)) {
    return { ok: false, reason: `expected final conversionPath ${scenario.allowedFinal.join("|")}, got ${finalPath}` };
  }
  for (const path of scenario.forbiddenPaths ?? []) {
    if (finalPath === path) return { ok: false, reason: `forbidden final conversionPath ${path}` };
  }
  for (const text of scenario.forbiddenText ?? []) {
    if (answer.includes(normalizeText(text))) return { ok: false, reason: `included forbidden text: ${text}` };
  }
  if (scenario.mustMentionAny?.length && !scenario.mustMentionAny.some((text) => answer.includes(normalizeText(text)))) {
    return { ok: false, reason: `missing one of: ${scenario.mustMentionAny.join(", ")}` };
  }
  if (scenario.requireQuestion && !hasQuestion(finalPayload, rawAnswer)) {
    return { ok: false, reason: "expected a natural next question" };
  }
  if (scenario.forbidContactAsk && asksForContact(answer)) {
    return { ok: false, reason: "asked for contact too early" };
  }
  if (scenario.requireContactAsk && !asksForContact(answer)) {
    return { ok: false, reason: "expected contact capture question" };
  }
  if (scenario.expectedQualification) {
    for (const [key, value] of Object.entries(scenario.expectedQualification)) {
      if (finalPayload.qualificationPatch?.[key] !== value) {
        return { ok: false, reason: `expected qualificationPatch.${key}=${value}, got ${finalPayload.qualificationPatch?.[key]}` };
      }
    }
  }
  if (scenario.forbidRecommendations && ((finalPayload.recommendedAgentIds ?? []).length || (finalPayload.recommendations ?? []).length)) {
    return { ok: false, reason: "included recommendations too early" };
  }
  if (scenario.requireSimpleLanguage) {
    const languageResult = assertSimpleLanguage(finalPayload, answer);
    if (!languageResult.ok) return languageResult;
  }
  if (isAggressive(answer)) {
    return { ok: false, reason: "answer sounded too aggressive or robotic by blocked phrase check" };
  }
  if (scenario.requireLead && salesToken) {
    const leadResult = await assertSalesInboxLead(salesInboxUrl, sessionId, finalPath, scenario.expectedLeadFields);
    if (!leadResult.ok) return leadResult;
  }

  return { ok: true };
}

async function assertSalesInboxLead(endpointUrl, sessionId, conversionPath, expectedFields) {
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
  for (const [key, value] of Object.entries(expectedFields ?? {})) {
    if (lead[key] !== value) return { ok: false, reason: `expected Sales Inbox lead.${key}=${value}, got ${lead[key]}` };
  }
  return { ok: true };
}

function hasQuestion(payload, rawAnswer) {
  return Boolean(payload.nextQuestion) || /\?/.test(rawAnswer);
}

function asksForContact(text) {
  if (/\bcom quem eu falo\b/.test(text)) return true;
  const asksEmailOrPhone =
    /\b(email|e-mail|telefone|celular|contato)\b/.test(text) &&
    /\b(qual|deixa|deixar|passa|passar|envia|enviar|usar|retornar|retorno|prefere|podemos usar)\b/.test(text);
  const asksWhatsapp =
    /\bwhatsapp\b/.test(text) &&
    /\b(qual whatsapp|deixa|deixar|passa|passar|envia|enviar|usar para|retornar|retorno|prefere|podemos usar)\b/.test(text);

  return asksEmailOrPhone || asksWhatsapp;
}

function isAggressive(text) {
  return [
    "compre agora",
    "assine agora",
    "ultima chance",
    "nao perca tempo",
    "plano mais forte",
    "voce precisa assinar",
    "sem pensar",
  ].some((phrase) => text.includes(phrase));
}

function assertSimpleLanguage(payload, normalizedAnswer) {
  const blockedTerms = [
    "cadencia",
    "escopo",
    "onboarding",
    "conversao",
    "integracao oficial",
    "checkout",
    "destino seguro",
  ];
  const blocked = blockedTerms.find((term) => normalizedAnswer.includes(term));
  if (blocked) return { ok: false, reason: `used non-simple term: ${blocked}` };

  const messages = payload.assistantMessages ?? [];
  const longMessage = messages.find((message) => String(message.content ?? "").length > 240);
  if (longMessage) return { ok: false, reason: "assistant message is too long for chat" };

  return { ok: true };
}

function normalizeText(value) {
  return String(value)
    .toLowerCase()
    .normalize("NFD")
    .replace(/\p{Diacritic}/gu, "");
}
