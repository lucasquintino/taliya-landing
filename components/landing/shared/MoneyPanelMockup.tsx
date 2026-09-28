"use client";

import { useId, useState } from "react";
import { createPortal } from "react-dom";
import type { CalculatorDefaults, PricingPlan } from "@/data/landing/niches/types";
import type { MoneyCalculatorResult } from "@/lib/landing/money-calculator";
import { ESTIMATED_OPERATIONAL_HOUR_VALUE, formatCurrency } from "@/lib/landing/money-calculator";

export type MoneyControl = {
  key: keyof CalculatorDefaults;
  label: string;
  min: number;
  max: number;
  step: number;
  prefix?: string;
  suffix?: string;
  group?: string;
};

function MetricIcon({ type }: { type: "agenda" | "retencao" | "financeiro" | "vendas" | "tempo" | "info" }) {
  const common = {
    fill: "none",
    stroke: "currentColor",
    strokeLinecap: "round" as const,
    strokeLinejoin: "round" as const,
    strokeWidth: 2,
  };
  const paths = {
    agenda: (
      <>
        <path d="M8 3v3M16 3v3M4.5 9h15" {...common} />
        <rect height="15" rx="3" width="15" x="4.5" y="5.5" {...common} />
        <path d="m8.5 14 2 2 4.5-5" {...common} />
      </>
    ),
    retencao: <path d="M12 21s7-4.4 7-11a4 4 0 0 0-7-2.6A4 4 0 0 0 5 10c0 6.6 7 11 7 11Z" {...common} />,
    financeiro: (
      <>
        <path d="M4 7h16v10H4z" {...common} />
        <path d="M8 11h4M8 14h8" {...common} />
      </>
    ),
    vendas: (
      <>
        <path d="M5 19V5h14" {...common} />
        <path d="m8 16 3.5-3.5 2 2L19 9" {...common} />
      </>
    ),
    tempo: (
      <>
        <circle cx="12" cy="12" r="8" {...common} />
        <path d="M12 8v5l3 2" {...common} />
      </>
    ),
    info: (
      <>
        <circle cx="12" cy="12" r="8" {...common} />
        <path d="M12 11.5v4" {...common} />
        <path d="M12 8.5h.01" {...common} />
      </>
    ),
  };

  return (
    <span className="flex h-9 w-9 shrink-0 items-center justify-center rounded-2xl bg-[#7BE0C8]/12 text-[#7BE0C8]">
      <svg aria-hidden="true" className="h-5 w-5" viewBox="0 0 24 24">
        {paths[type]}
      </svg>
    </span>
  );
}

function InfoTooltip({ ariaLabel, text }: { ariaLabel: string; text: string }) {
  const tooltipId = useId();
  const [isVisible, setIsVisible] = useState(false);

  return (
    <>
      <span className="money-info ml-auto">
        <button
          aria-describedby={isVisible ? tooltipId : undefined}
          aria-label={ariaLabel}
          className="flex h-9 w-9 items-center justify-center rounded-full border border-white/10 bg-white/[0.055] text-white/58 transition hover:border-[#7BE0C8]/40 hover:text-[#7BE0C8] focus:outline-none focus:ring-2 focus:ring-[#7BE0C8]"
          onBlur={() => setIsVisible(false)}
          onFocus={() => setIsVisible(true)}
          onMouseEnter={() => setIsVisible(true)}
          onMouseLeave={() => setIsVisible(false)}
          type="button"
        >
          <svg aria-hidden="true" className="h-4 w-4" viewBox="0 0 24 24">
            <circle cx="12" cy="12" fill="none" r="8" stroke="currentColor" strokeWidth="2" />
            <path d="M12 11.5v4" fill="none" stroke="currentColor" strokeLinecap="round" strokeWidth="2" />
            <path d="M12 8.5h.01" fill="none" stroke="currentColor" strokeLinecap="round" strokeWidth="3" />
          </svg>
        </button>
      </span>
      {isVisible && typeof document !== "undefined"
        ? createPortal(
            <span className="money-info-tooltip is-visible" id={tooltipId} role="tooltip">
              {text}
            </span>,
            document.body,
          )
        : null}
    </>
  );
}

function PlansPriceDefensePanel({
  plans,
  result,
  values,
}: {
  plans: PricingPlan[];
  result: MoneyCalculatorResult;
  values: CalculatorDefaults;
}) {
  const monthlyFee = Math.max(values.averageMonthlyFee, 1);
  const classSpotValue = Math.max(values.averageMonthlyFee / 8, 1);
  const hourValue = ESTIMATED_OPERATIONAL_HOUR_VALUE;
  const leakSources = [
    {
      label: "Interessados que esfriam",
      value: result.metrics.trialOpportunitiesRecovered,
      unit: "retomadas/mês",
      detail: "pedem preço, horário ou experimental e ficam sem próximo passo",
    },
    {
      label: "Mensalidades sem acompanhamento",
      value: result.metrics.financeFollowUps,
      unit: "contatos/mês",
      detail: "vencimentos, atrasos e renovações que alguém precisa lembrar",
    },
    {
      label: "Alunos em risco",
      value: result.metrics.studentsReactivated,
      unit: "sinais/mês",
      detail: "somem, pausam ou faltam antes de cancelar",
    },
    {
      label: "Horários que viram buraco",
      value: result.metrics.absencesAvoided,
      unit: "horários/mês",
      detail: "faltas, reposições e confirmações perdidas",
    },
    {
      label: "Tempo preso da equipe",
      value: result.metrics.monthlyManualHours,
      unit: "horas/mês",
      detail: "conversa, planilha e agenda conferidas na mão",
    },
  ];
  const planPaybacks = plans.map((plan) => {
    const monthlyEquivalent = Math.max(1, Math.ceil(plan.monthlyPriceBRL / monthlyFee));
    const classSpotEquivalent = Math.max(1, Math.ceil(plan.monthlyPriceBRL / classSpotValue));
    const hourEquivalent = Math.max(1, Math.ceil(plan.monthlyPriceBRL / hourValue));
    const activeAgentsByPlan: Record<string, string[]> = {
      base: [],
      one_agent: ["Atendimento"],
      three_agents: ["Atendimento", "Agenda", "Vendas"],
      seven_agents: ["Atendimento", "Agenda", "Vendas", "Financeiro", "Retenção", "Gestão", "Histórico/Evolução"],
    };
    const activeAgents = activeAgentsByPlan[plan.id] ?? plan.includedAgents;
    const recoveryOptions = [
      { agents: [], label: monthlyEquivalent === 1 ? "mensalidade paga" : "mensalidades pagas", value: monthlyEquivalent },
      { agents: ["Atendimento", "Vendas"], label: monthlyEquivalent === 1 ? "interessado que se matricula" : "interessados que se matriculam", value: monthlyEquivalent },
      { agents: ["Retenção"], label: monthlyEquivalent === 1 ? "aluno em risco recuperado" : "alunos em risco recuperados", value: monthlyEquivalent },
      { agents: ["Agenda"], label: classSpotEquivalent === 1 ? "encaixe de horário" : "encaixes de horário", value: classSpotEquivalent },
      { agents: [], label: hourEquivalent === 1 ? "hora sua economizada" : "horas suas economizadas", value: hourEquivalent },
    ].filter((option) => !option.agents.length || option.agents.some((agent) => activeAgents.includes(agent)));

    return {
      classSpotEquivalent,
      hourEquivalent,
      isFeatured: plan.id === "seven_agents",
      monthlyEquivalent,
      plan,
      recoveryOptions,
    };
  });

  return (
    <div className="money-result-panel plans-price-defense-card flex h-full self-stretch overflow-hidden rounded-3xl border border-[#E5DED2] bg-[#101B3A] p-5 text-white shadow-[0_28px_80px_rgba(16,27,58,0.18)] sm:p-6 lg:p-5 xl:p-6">
      <div className="grid gap-5 xl:grid-cols-[0.98fr_1.02fr]">
        <section className="flex min-w-0 flex-col">
          <p className="text-[0.68rem] font-black uppercase tracking-[0.18em] text-[#7BE0C8]">Quantas recuperações pagam cada plano?</p>
          <div className="mt-4 grid gap-2">
            {planPaybacks.map(({ isFeatured, plan, recoveryOptions }) => (
              <div
                className={`grid gap-2.5 rounded-2xl border px-3 py-2.5 xl:grid-cols-[7rem_1fr] xl:items-start ${
                  isFeatured ? "border-[#FFB21A]/58 bg-[#FFB21A]/10" : "border-white/10 bg-white/[0.04]"
                }`}
                key={plan.id}
              >
                <div className="min-w-0">
                  <p className="text-base font-black leading-5 text-white">{plan.name}</p>
                  <span className={`mt-1 inline-flex rounded-full px-2 py-0.5 text-[10px] font-black ${isFeatured ? "bg-[#FFB21A] text-[#101B3A]" : "bg-white/10 text-white/70"}`}>
                    {plan.monthlyPriceLabel}
                  </span>
                </div>
                <ul className="grid content-start gap-0.5 text-xs font-bold leading-4 text-white/66">
                  {recoveryOptions.map((option, index) => (
                    <li className="flex items-baseline gap-2" key={option.label}>
                      <span className="mt-[0.38rem] h-1.5 w-1.5 shrink-0 rounded-full bg-[#7BE0C8]" />
                      <span>
                        <strong className="text-sm font-black text-white">{option.value}</strong> {option.label}
                        {index < recoveryOptions.length - 1 ? ", ou" : ""}
                      </span>
                    </li>
                  ))}
                </ul>
              </div>
            ))}
          </div>
        </section>

        <section className="flex min-w-0 flex-col border-t border-white/10 pt-4 xl:border-l xl:border-t-0 xl:pl-5 xl:pt-0">
          <p className="text-[0.68rem] font-black uppercase tracking-[0.18em] text-white/50">Onde o dinheiro costuma escapar?</p>
          <div className="mt-4 grid gap-2">
            {leakSources.map((item) => (
              <div className="rounded-2xl border border-white/10 bg-white/[0.035] p-3" key={item.label}>
                <div className="flex h-full items-start justify-between gap-3">
                  <div>
                    <p className="text-base font-black leading-5 text-white">{item.label}</p>
                    <p className="mt-1 text-xs font-bold leading-4 text-white/58">{item.detail}</p>
                  </div>
                  <div className="shrink-0 rounded-2xl bg-[#7BE0C8]/10 px-3 py-2 text-right">
                    <p className="text-2xl font-black leading-none text-[#7BE0C8]">{item.value}</p>
                    <p className="mt-1 text-[0.62rem] font-black uppercase tracking-[0.08em] text-white/48">{item.unit}</p>
                  </div>
                </div>
              </div>
            ))}
          </div>
        </section>
      </div>
    </div>
  );
}

export function MoneyPanelMockup({
  context = "landing",
  result,
  ctaHref,
  onCta,
  plans,
  values,
}: {
  context?: "landing" | "plans";
  result: MoneyCalculatorResult;
  ctaHref: string;
  onCta: () => void;
  plans?: PricingPlan[];
  values: CalculatorDefaults;
}) {
  const recoveredMetrics = [
    {
      agent: "Agenda",
      detail: "Confirma presença, identifica quem não vai e ajuda a ocupar o horário antes da vaga ser perdida.",
      formula: `${result.metrics.absencesAvoided} por mês, cerca de ${Math.max(1, Math.round(result.metrics.absencesAvoided / 4))} por semana.`,
      icon: "agenda" as const,
      label: "faltas evitadas por mês",
      tooltip:
        "Todo mês tem aluno que esquece, falta em cima da hora, pede para remarcar ou deixa um horário vazio. A Taliya confirma presença, descobre quem não vai e tenta salvar o horário antes que ele vire buraco na agenda.",
      value: result.metrics.absencesAvoided,
    },
    {
      agent: "Retenção",
      detail: "Percebe aluno sumido, traz o contexto recente e chama a equipe antes da pausa virar cancelamento.",
      formula: `${result.metrics.studentsReactivated} por mês que recebem contato antes de esfriar.`,
      icon: "retencao" as const,
      label: "alunos em risco por mês",
      tooltip:
        "Nem todo aluno cancela de uma vez. Antes disso ele some, responde menos, pausa, falta mais ou demonstra insatisfação. A Taliya percebe esses sinais e leva o caso para a equipe com contexto.",
      value: result.metrics.studentsReactivated,
    },
    {
      agent: "Financeiro",
      detail: "Acompanha vencimentos, atrasos e renovações para reduzir pagamento esquecido.",
      formula: `${result.metrics.financeFollowUps} por mês entre vencimentos, atrasos e renovações.`,
      icon: "financeiro" as const,
      label: "cobranças por mês",
      tooltip:
        "Mesmo em um studio organizado existem vencimentos, atrasos, renovações, links de pagamento e combinados para acompanhar. A Taliya organiza lembretes e reduz cobrança esquecida.",
      value: result.metrics.financeFollowUps,
    },
    {
      agent: "Vendas",
      detail: "Retoma interessados, lembra aula experimental e mantem o próximo passo claro.",
      formula: `${result.metrics.trialOpportunitiesRecovered} por mês que poderiam esfriar sem retorno rápido.`,
      icon: "vendas" as const,
      label: "oportunidades por mês",
      tooltip:
        "Interessado esfria rápido. As vezes pediu horário, marcou experimental, perguntou preco ou veio por indicação. A Taliya retoma no momento certo e mantem o próximo passo vivo.",
      value: result.metrics.trialOpportunitiesRecovered,
    },
    {
      agent: "Gestão + Histórico",
      detail: "Mostram prioridades, histórico do aluno e pendências do dia para reduzir WhatsApp, planilha e conferências manuais.",
      formula: `${result.metrics.monthlyManualHours}h por mês, cerca de ${Math.max(1, Math.round(result.metrics.monthlyManualHours / 4))}h por semana.`,
      icon: "tempo" as const,
      label: "horas economizadas por mês",
      tooltip:
        "A maior economia vem de parar de procurar contexto, revisar conversa antiga, conferir agenda, lembrar combinado e atualizar planilha. Estimamos esse tempo escondido que o studio gasta todos os dias.",
      value: result.metrics.monthlyManualHours,
    },
    {
      agent: "Total",
      detail: "O valor combina receita preservada e tempo que volta para a equipe.",
      formula: `Calculado com mensalidade média de ${formatCurrency(values.averageMonthlyFee)} e valor estimado das horas poupadas.`,
      icon: "tempo" as const,
      label: "em dinheiro na mesa",
      tooltip:
        "Esse número junta dinheiro e tempo que escapam aos poucos: horário vazio, aluno que some, pagamento sem acompanhamento, interessado que esfria e horas da equipe presas em conferência.",
      value: formatCurrency(result.total),
    },
  ];
  const isPlansContext = context === "plans";
  const displayedMetrics = isPlansContext
    ? recoveredMetrics
        .filter((item) => item.agent === "Agenda" || item.agent === "Retenção" || item.agent === "Financeiro" || item.agent === "Vendas")
        .map((item) => {
          if (item.agent === "Agenda") {
            return {
              ...item,
              detail: "Horários que podem virar buraco na agenda quando falta, reposição ou confirmação escapam.",
              label: "horários protegidos",
            };
          }
          if (item.agent === "Retenção") {
            return {
              ...item,
              detail: "Alunos que já dão sinais de pausa, sumiço ou cancelamento antes da receita desaparecer.",
              label: "alunos em risco",
            };
          }
          if (item.agent === "Financeiro") {
            return {
              ...item,
              detail: "Vencimentos, atrasos e renovações que precisam de acompanhamento para não ficar para depois.",
              label: "mensalidades acompanhadas",
            };
          }
          if (item.agent === "Vendas") {
            return {
              ...item,
              detail: "Interessados e aulas experimentais que precisam de retomada antes de esfriarem.",
              label: "interessados retomados",
            };
          }
          return item;
        })
    : recoveredMetrics;

  if (isPlansContext && plans?.length) {
    return <PlansPriceDefensePanel plans={plans} result={result} values={values} />;
  }

  return (
    <div className="money-result-panel flex h-full min-h-[35rem] flex-col overflow-hidden rounded-3xl border border-[#E5DED2] bg-[#101B3A] p-5 text-white shadow-[0_28px_80px_rgba(16,27,58,0.18)] sm:p-6 lg:p-5 xl:p-6">
      <div className="money-result-header grid gap-4 border-b border-white/12 pb-4 lg:grid-cols-[0.82fr_1.18fr] lg:items-end">
        <div>
          <p className="text-xs font-black uppercase tracking-[0.28em] text-[#7BE0C8]">
            {isPlansContext ? "Quanto pode estar escapando" : "Dinheiro na mesa estimado"}
          </p>
          <p className="money-result-total money-result-total-value mt-3 text-[clamp(2.65rem,5vw,4.6rem)] font-black leading-none tracking-[-0.08em]" key={`total-${result.total}`}>{formatCurrency(result.total)}</p>
        </div>
        <p className="money-result-summary max-w-xl text-sm font-bold leading-6 text-white/72 xl:text-base xl:leading-7">
          {isPlansContext
            ? `Estimativa conservadora do que pode escapar por mês em interessados sem retorno, horários vazios, mensalidades sem acompanhamento e alunos que somem. Mensalidade média: ${formatCurrency(values.averageMonthlyFee)}.`
            : `Soma receita que deixa de escapar e horas operacionais que voltam para a equipe, usando mensalidade média de ${formatCurrency(values.averageMonthlyFee)}.`}
        </p>
      </div>

      <p className="mt-3 text-[0.68rem] font-black uppercase tracking-[0.16em] text-white/50">
        {isPlansContext ? "De onde vem esse custo" : "Toque no ícone para ver o cálculo"}
      </p>

      <div className={`money-metric-grid mt-4 grid content-start gap-2 ${isPlansContext ? "lg:grid-cols-4" : "flex-1 lg:grid-cols-3"}`}>
        {displayedMetrics.map((item) => {
          const infoLabel = item.agent === "Total" ? "Ver cálculo do total" : `Ver cálculo de ${item.agent}`;
          return (
            <div className="money-metric-card rounded-2xl border border-white/10 bg-white/[0.055] px-3 py-2.5" key={item.label}>
              <div className="flex items-start gap-2.5">
                <MetricIcon type={item.icon} />
                <div className="min-w-0">
                  <p className="text-[0.65rem] font-black uppercase tracking-[0.16em] text-[#7BE0C8]">{item.agent}</p>
                  <p className="money-metric-value mt-1 text-sm font-black leading-5 xl:text-base" key={`${item.label}-${item.value}`}>
                    {item.value} {item.label}
                  </p>
                </div>
                <InfoTooltip ariaLabel={infoLabel} text={item.tooltip} />
              </div>
              <p className="money-metric-detail mt-1.5 text-xs font-bold leading-4 text-white/66 xl:text-sm xl:leading-5">{item.detail}</p>
              {!isPlansContext ? <p className="money-metric-formula mt-1 text-[0.7rem] font-black leading-4 text-white/58 xl:text-xs">{item.formula}</p> : null}
            </div>
          );
        })}
      </div>
      <a
        className="money-result-cta mt-auto inline-flex w-full items-center justify-center rounded-full bg-[#7BE0C8] px-5 py-3.5 text-sm font-black text-[#101B3A] transition hover:bg-[#92EBD7] focus:outline-none focus:ring-2 focus:ring-white"
        href={ctaHref}
        onClick={onCta}
      >
        Ver como recuperar esse valor <span aria-hidden="true" className="ml-2">→</span>
      </a>
    </div>
  );
}
