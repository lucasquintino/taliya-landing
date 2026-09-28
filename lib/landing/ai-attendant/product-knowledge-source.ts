import { pilatesLanding } from "@/data/landing/niches/pilates";
import type { NicheLandingConfig } from "@/data/landing/niches/types";

export type ProductKnowledge = ReturnType<typeof buildProductKnowledge>;

export function getProductKnowledge(config: NicheLandingConfig = pilatesLanding) {
  return buildProductKnowledge(config);
}

function buildProductKnowledge(config: NicheLandingConfig) {
  return {
    version: `taliya-pilates-commercial-${config.subscription.recommendedPlanId}-2026-05-21`,
    updatedAt: "2026-05-21T00:00:00.000Z",
    brand: {
      name: "Taliya" as const,
      category: "CRM SaaS para studios de Pilates" as const,
    },
    plans: config.subscription.plans.map((plan) => ({
      id: plan.id,
      name: plan.name,
      priceMonthlyBrl: parseMonthlyPrice(plan.monthlyPriceLabel),
      priceLabel: plan.monthlyPriceLabel,
      summary: plan.positioning || plan.bestFor,
      includedRoutines: plan.includedAgents,
      limitations: plan.id === "base" ? ["Sem IA ativa no WhatsApp."] : undefined,
    })),
    routines: [
      {
        id: "attendance",
        name: "Atendimento",
        painSignals: ["whatsapp", "mensagens", "duvidas", "respostas"],
        practicalRole: "organiza mensagens, pedidos comuns e pendencias de resposta.",
      },
      {
        id: "schedule",
        name: "Agenda",
        painSignals: ["agenda", "faltas", "reposicoes", "horarios"],
        practicalRole: "ajuda a organizar faltas, reposicoes, vagas e encaixes.",
      },
      {
        id: "sales",
        name: "Vendas",
        painSignals: ["interessados", "aula experimental", "vendas", "matriculas"],
        practicalRole: "mantem interessados com proximo passo visivel.",
      },
      {
        id: "finance",
        name: "Financeiro",
        painSignals: ["mensalidades", "cobranca", "renovacao", "atrasos"],
        practicalRole: "ajuda a acompanhar mensalidades, vencimentos e renovacoes.",
      },
      {
        id: "management",
        name: "Gestao",
        painSignals: ["prioridade", "painel", "visao do dia", "gestao"],
        practicalRole: "mostra prioridades e pontos que precisam de ação.",
      },
    ],
    links: {
      landing: "https://www.taliya.com.br/",
      plans: "https://www.taliya.com.br/#planos",
      demonstration: "https://www.taliya.com.br/#como-funciona",
      privacy: "https://www.taliya.com.br/privacidade",
    },
    demo: {
      status: "available" as const,
      message: "A demonstração oficial pode ser acessada pela rota de demonstração da landing.",
    },
    availability: {
      status: "limited_studios_waitlist" as const,
      waitlistCopy:
        "Pelo que você contou, faz sentido deixar seu studio no radar.\n\nHoje estamos trabalhando com um número pequeno de studios, para acompanhar de perto cada implantação.\n\nCaso tenha interesse, posso colocar seu studio na lista de espera e te chamar quando abrir uma próxima janela.",
    },
    commercialPolicies: {
      guaranteeCancellation: "30 dias de garantia na primeira assinatura. Cancelamento mensal sem multa apos esse periodo, conforme politica vigente.",
      unsupportedClaims: [
        "ROI garantido",
        "integração específica sem confirmação",
        "data exata de abertura",
        "checkout enquanto disponibilidade ampla esta fechada",
      ],
      noCheckoutWhileClosed: true as const,
    },
  };
}

function parseMonthlyPrice(label: string) {
  const digits = label.replace(/\D/g, "");
  return Number(digits) || 0;
}
