"use client";

import Link from "next/link";
import { useEffect, useMemo, useState, type CSSProperties } from "react";
import type { CalculatorDefaults, NicheLandingConfig, PricingPlan } from "@/data/landing/niches/types";
import { calculateMoneyOnTable } from "@/lib/landing/money-calculator";
import { trackLandingEvent } from "@/lib/landing/tracking";
import { FinalCTASection } from "./sections/FinalCTASection";
import { FooterSection } from "./sections/FooterSection";
import { MoneyCalculatorSection } from "./sections/MoneyCalculatorSection";
import { SectionShell } from "./shared/SectionShell";
import { FloatingAiAttendant } from "./shared/FloatingAiAttendant";
import { TaliyaLogo } from "./shared/TaliyaLogo";

type Props = {
  config: NicheLandingConfig;
  initialPlanId?: string;
};

type TouchState = {
  intent: "horizontal" | "pending" | "vertical";
  offsetX: number;
  startX: number;
  startY: number;
};

const SWIPE_INTENT_PX = 8;
const SWIPE_COMMIT_PX = 42;
const SWIPE_MAX_OFFSET_PX = 52;

const faqItems = [
  {
    question: "Qual plano eu deveria escolher?",
    answer: "Se você quer a Taliya cuidando da rotina completa do studio, o Completo é o caminho natural. Base organiza a casa; Essencial começa pelo atendimento; Avance conecta atendimento, agenda e vendas.",
  },
  {
    question: "O Base já age sozinho?",
    answer: "Não. Base organiza alunos, contatos, tarefas, histórico básico e rotina no sistema, mas sem agentes ativos acompanhando ou agindo. Ele existe para colocar a casa em ordem antes dos agentes entrarem na rotina.",
  },
  {
    question: "Preciso ter WhatsApp Business?",
    answer: "Sim, para agentes conversarem com alunos pelo número do studio. Se hoje o studio usa WhatsApp pessoal, o ideal é preparar ou migrar para WhatsApp Business antes de ativar os agentes.",
  },
  {
    question: "O WhatsApp usado é o meu?",
    answer: "Sim. Nos planos com agentes, as conversas com alunos acontecem no WhatsApp Business do próprio studio. O WhatsApp da Taliya fica separado e serve para venda, diagnóstico e suporte.",
  },
  {
    question: "Posso começar por um plano menor e mudar depois?",
    answer: "Sim. A página separa os planos por momento do studio: organizar primeiro, ativar uma frente, conectar três rotinas ou usar o time completo. Se fizer sentido, o diagnóstico ajuda a escolher sem travar a decisão.",
  },
  {
    question: "O que acontece depois de assinar?",
    answer: "A Taliya conduz o próximo passo de configuração: base do studio, regras, rotinas, acessos e, nos planos com agentes, preparação do WhatsApp Business e das mensagens aprovadas.",
  },
  {
    question: "Posso cancelar?",
    answer: "Sim. Os planos públicos têm 30 dias de garantia na primeira assinatura, com cancelamento e reembolso conforme os termos comerciais.",
  },
  {
    question: "Agente sob medida entra no plano?",
    answer: "Não. Agente sob medida é uma frente separada para operações fora do time principal, como marketing, parcerias ou rotinas internas muito específicas.",
  },
];

const planIntents: Record<string, string> = {
  base: "Base organizada",
  one_agent: "Primeira frente",
  three_agents: "Rotinas conectadas",
  seven_agents: "Time completo",
};

const planPresentation: Record<
  string,
  {
    name: string;
    pitch: string;
    proof: string;
  }
> = {
  base: {
    name: "Base",
    pitch: "Organize alunos, contatos e tarefas antes de ativar agentes.",
    proof: "Para studios que precisam enxergar a rotina com clareza.",
  },
  one_agent: {
    name: "Essencial",
    pitch: "Ative uma frente para a Taliya agir onde mais trava o dia.",
    proof: "Para provar valor em uma rotina antes de expandir.",
  },
  three_agents: {
    name: "Avance",
    pitch: "Conecte atendimento, agenda e vendas nas rotinas que mais pesam.",
    proof: "Para conectar conversa, agenda e matrícula no WhatsApp.",
  },
  seven_agents: {
    name: "Completo",
    pitch: "Coloque o time principal da Taliya cuidando das rotinas do studio.",
    proof: "Para vender, reter e reduzir trabalho repetitivo junto.",
  },
};

export function PlansPage({ config, initialPlanId }: Props) {
  const plans = config.subscription.plans;
  const fallbackPlan = plans[0];
  const [calculatorValues, setCalculatorValues] = useState(config.calculator.defaults);
  const initialSelectedPlanId =
    initialPlanId && plans.some((plan) => plan.id === initialPlanId)
      ? initialPlanId
      : config.subscription.recommendedPlanId;
  const [selectedPlanId, setSelectedPlanId] = useState(initialSelectedPlanId);
  const recommendedPlan = useMemo(
    () =>
      plans.find((plan) => plan.id === config.subscription.recommendedPlanId) ??
      plans.find((plan) => plan.recommended) ??
      fallbackPlan,
    [config.subscription.recommendedPlanId, fallbackPlan, plans],
  );
  const selectedPlan = plans.find((plan) => plan.id === selectedPlanId) ?? recommendedPlan;
  const comparisonSections = comparisonGroups(plans, config.agents);
  const money = useMemo(() => calculateMoneyOnTable(calculatorValues), [calculatorValues]);
  const plansCalculatorConfig = useMemo(
    () => ({
      ...config,
      calculator: {
        ...config.calculator,
        eyebrow: "Conta rápida do preço",
        title: "Quanto a Taliya precisa recuperar?",
        subtitle:
          "Ajuste alunos ativos e mensalidade média. A conta mostra quanto pode estar escapando e quantas recuperações pagam cada plano.",
        cta: { label: "Voltar para os planos", href: "#planos" },
      },
    }),
    [config],
  );

  useEffect(() => {
    trackLandingEvent(config.tracking, "plans_page_viewed", {
      sourcePage: "/pilates/planos",
      recommendedPlanId: config.subscription.recommendedPlanId,
      planFromUrl: initialPlanId,
    });
  }, [config.subscription.recommendedPlanId, config.tracking, initialPlanId]);

  function openConsultor(plan: PricingPlan, sourceSection: string) {
    setSelectedPlanId(plan.id);
    trackLandingEvent(config.tracking, "human_whatsapp_clicked", {
      sourcePage: "/pilates/planos",
      sourceSection,
      planId: plan.id,
      destinationKind: "floating_agent",
    });
    window.dispatchEvent(
      new CustomEvent("landing:open-sales-agent", {
        detail: {
          sourceSection,
          message: `Estou comparando os planos e quero confirmar se ${plan.name} e o melhor para meu studio antes de assinar.`,
        },
      }),
    );
  }

  function requestCheckout(plan: PricingPlan, sourceSection: string) {
    setSelectedPlanId(plan.id);
    trackLandingEvent(config.tracking, "plan_cta_clicked", {
      sourcePage: "/pilates/planos",
      sourceSection,
      planId: plan.id,
      billingPeriod: plan.billingPeriod,
      checkoutGate: "billing_not_implemented",
      nextStep: "checkout_or_consultor_confirmation",
    });
    window.dispatchEvent(
      new CustomEvent("landing:open-sales-agent", {
        detail: {
          sourceSection,
          message: `Quero assinar o plano ${plan.name}. Me conduza pelo checkout seguro assim que estiver tudo confirmado.`,
        },
      }),
    );
  }

  function requestDemo(plan: PricingPlan, sourceSection: string) {
    setSelectedPlanId(plan.id);
    trackLandingEvent(config.tracking, "floating_agent_guided_demo_cta", {
      sourcePage: "/pilates/planos",
      sourceSection,
      planId: plan.id,
      guidedDemoReady: config.floatingAgent.guidedDemoReady,
    });

    if (config.floatingAgent.guidedDemoReady) {
      window.location.href = config.floatingAgent.guidedDemoDestination.href;
      return;
    }

    window.dispatchEvent(
      new CustomEvent("landing:open-sales-agent", {
        detail: {
          sourceSection,
          message: `Quero ver uma demo antes de assinar o plano ${plan.name}. Me mostre o melhor caminho.`,
        },
      }),
    );
  }

  function trackDiagnosticInterest(sourceSection: string) {
    trackLandingEvent(config.tracking, "cta_click", {
      sourcePage: "/pilates/planos",
      sourceSection,
      intent: "plan_recommendation_diagnostic",
    });
  }

  function trackPlansCustomAgentCta(label: string, href: string) {
    trackLandingEvent(config.tracking, "cta_click", {
      sourcePage: "/pilates/planos",
      sourceSection: "plans_custom_agent",
      label,
      href,
    });
  }

  function updateCalculatorValue(key: keyof CalculatorDefaults, value: number) {
    setCalculatorValues((current) => ({ ...current, [key]: value }));
  }

  return (
    <main className="min-h-screen overflow-x-clip bg-[#FFFDF8] text-[#101B3A]">
      <header className="sticky top-0 z-40 border-b border-[#E9E4DA]/80 bg-[#FFFDF8]/92 px-4 py-3 backdrop-blur-xl sm:px-8 lg:px-12">
        <div className="mx-auto flex max-w-[1520px] items-center justify-between gap-3 lg:w-[80vw]">
          <div className="flex min-w-0 items-center gap-3">
            <Link
              aria-label="Voltar para Taliya Pilates"
              className="interactive-hit inline-flex h-11 w-11 shrink-0 items-center justify-center rounded-full border border-[#E2DED5] bg-white text-[#080A0F] shadow-[0_10px_24px_rgba(16,27,58,0.06)] transition hover:border-[#101B3A] focus:outline-none focus:ring-2 focus:ring-[#0E8F7E] focus:ring-offset-2"
              href="/pilates"
            >
              <BackArrowIcon />
            </Link>
            <Link className="interactive-hit flex min-w-0 shrink-0 items-center text-[#101B3A]" href="/pilates">
              <TaliyaLogo label={config.brand} />
            </Link>
          </div>
          <nav className="hidden items-center gap-1 text-sm font-bold text-[#667085] lg:flex">
            <a className="interactive-hit rounded-full px-3 py-2 hover:bg-[#F5F0E8] hover:text-[#101B3A]" href="#planos">
              Planos
            </a>
            <a className="interactive-hit rounded-full px-3 py-2 hover:bg-[#F5F0E8] hover:text-[#101B3A]" href="#dinheiro-na-mesa">
              Preço
            </a>
            <a className="interactive-hit rounded-full px-3 py-2 hover:bg-[#F5F0E8] hover:text-[#101B3A]" href="#comparativo-alternativas">
              Alternativas
            </a>
            <a className="interactive-hit rounded-full px-3 py-2 hover:bg-[#F5F0E8] hover:text-[#101B3A]" href="#comparativo">
              Comparativo
            </a>
            <a className="interactive-hit rounded-full px-3 py-2 hover:bg-[#F5F0E8] hover:text-[#101B3A]" href="#faq-planos">
              Dúvidas
            </a>
          </nav>
          <button
            className="interactive-hit inline-flex min-h-11 shrink-0 items-center justify-center rounded-full bg-[#101B3A] px-4 text-xs font-black text-white shadow-[0_18px_45px_rgba(16,27,58,0.18)] transition hover:bg-[#17254B] focus:outline-none focus:ring-2 focus:ring-[#0E8F7E] focus:ring-offset-2 sm:text-sm"
            onClick={() => openConsultor(selectedPlan, "plans_header")}
            type="button"
          >
            Consultor
          </button>
        </div>
      </header>

      <section className="relative isolate overflow-hidden px-4 py-12 sm:px-8 sm:py-16 lg:px-12 lg:py-20">
        <div className="absolute inset-x-0 top-0 -z-10 h-[560px] bg-[radial-gradient(circle_at_22%_12%,rgba(255,178,26,0.14),transparent_27%),radial-gradient(circle_at_78%_8%,rgba(99,91,255,0.12),transparent_26%),linear-gradient(180deg,#FFFFFF_0%,#FFFDF8_62%,#FAF7F1_100%)]" />
        <div className="mx-auto w-[95vw] max-w-[1520px] lg:w-[80vw]">
          <div className="mx-auto grid max-w-[1360px] justify-items-center gap-6 text-center">
            <h1 className="w-full text-[clamp(2.55rem,6.4vw,5.75rem)] font-black leading-[1.02] tracking-[-0.055em] text-[#101B3A] [text-wrap:balance] sm:leading-[0.94] sm:tracking-[-0.075em]">
              Planos Taliya para studios de Pilates
            </h1>

            <p className="mx-auto max-w-5xl text-base font-bold leading-7 text-[#667085] sm:text-lg lg:text-xl lg:leading-8">
              Escolha entre organizar a casa, recuperar interessados, preencher horários, acompanhar mensalidades ou colocar a Taliya para cuidar da rotina completa.
            </p>

            <div className="flex w-full flex-col items-center justify-center gap-3 sm:w-auto sm:flex-row">
              <a
                className="interactive-hit inline-flex min-h-13 items-center justify-center rounded-full bg-[#101B3A] px-6 text-sm font-black text-white shadow-[0_18px_42px_rgba(16,27,58,0.18)] transition hover:bg-[#17254B] focus:outline-none focus:ring-2 focus:ring-[#0E8F7E] focus:ring-offset-2"
                href="#diagnostico"
                onClick={() => trackDiagnosticInterest("plans_hero_diagnostic")}
              >
                Fazer diagnóstico gratuito
              </a>
              <button
                className="interactive-hit inline-flex min-h-13 items-center justify-center rounded-full border border-[#E2DED5] bg-white px-6 text-sm font-black text-[#101B3A] shadow-[0_14px_32px_rgba(16,27,58,0.07)] transition hover:border-[#0E8F7E] focus:outline-none focus:ring-2 focus:ring-[#0E8F7E] focus:ring-offset-2"
                onClick={() => requestDemo(recommendedPlan, "plans_hero_demo")}
                type="button"
              >
                Ver demo
              </button>
            </div>
          </div>
        </div>
      </section>

      <section className="px-4 pb-8 sm:px-8 sm:pb-10 lg:px-12" id="planos">
        <div className="mx-auto max-w-[1520px] lg:w-[80vw]">
          <div className="grid gap-4 lg:grid-cols-4">
            {plans.map((plan) => {
              const featured = plan.id === recommendedPlan.id;

              return (
                <article
                  className={`flex min-h-[27rem] flex-col rounded-[22px] border p-5 shadow-[0_18px_45px_rgba(16,27,58,0.07)] transition ${
                    featured
                      ? "border-[#101B3A] bg-[#101B3A] text-white shadow-[0_24px_58px_rgba(16,27,58,0.22)] ring-4 ring-[#101B3A]/12"
                      : plan.id === selectedPlanId
                        ? "border-[#101B3A] bg-white ring-4 ring-[#101B3A]/10"
                        : plan.recommended
                          ? "border-[#0E8F7E] bg-white ring-4 ring-[#0E8F7E]/10"
                          : "border-[#E2DED5] bg-white"
                  }`}
                  id={plan.id}
                  key={plan.id}
                >
                  <div className="flex min-h-[11.5rem] flex-col">
                    <div className="flex min-h-[3.75rem] items-start justify-between gap-3">
                      <div>
                      <p className={`text-xs font-black uppercase tracking-[0.16em] ${featured ? "text-[#FFB21A]" : "text-[#0E8F7E]"}`}>
                        {planIntents[plan.id] ?? plan.name}
                      </p>
                      <h2 className={`mt-2 text-2xl font-black tracking-[-0.04em] ${featured ? "text-white" : "text-[#101B3A]"}`}>
                        {commercialPlanName(plan)}
                      </h2>
                      </div>
                      {plan.recommended ? (
                        <span className={`rounded-full px-3 py-1 text-[11px] font-black ${featured ? "bg-[#FFB21A] text-[#101B3A]" : "bg-[#0E8F7E] text-white"}`}>
                          Melhor
                        </span>
                      ) : null}
                    </div>
                    <p className={`mt-6 text-4xl font-black tracking-[-0.055em] ${featured ? "text-white" : "text-[#101B3A]"}`}>{plan.monthlyPriceLabel}</p>
                    <p className={`mt-3 min-h-[4.5rem] text-sm font-bold leading-6 ${featured ? "text-white/72" : "text-[#667085]"}`}>
                      {planPresentation[plan.id]?.pitch ?? shortPositioning(plan)}
                    </p>
                  </div>
                  <div className={`mt-5 grid gap-2.5 border-t pt-5 ${featured ? "border-white/12" : "border-[#EEE7DA]"}`}>
                    {planCardFeatures(plan).map((feature) => (
                      <PlanFeatureRow feature={feature} featured={featured} key={feature.label} />
                    ))}
                  </div>
                  <p className={`mt-4 flex min-h-[4.5rem] items-center rounded-2xl p-3 text-xs font-black leading-5 ${featured ? "bg-white/10 text-white/78 ring-1 ring-white/12" : "bg-[#FBF8F2] text-[#667085]"}`}>
                    {planPresentation[plan.id]?.proof ?? plan.bestFor}
                  </p>
                  <div className="mt-auto grid gap-2 pt-6">
                    <button
                      className={`interactive-hit inline-flex min-h-12 items-center justify-center rounded-full px-5 text-sm font-black transition focus:outline-none focus:ring-2 focus:ring-[#0E8F7E] focus:ring-offset-2 ${
                        featured
                          ? "bg-[#FFB21A] text-[#101B3A] hover:bg-[#F8A800] focus:ring-offset-[#101B3A]"
                          : "bg-[#101B3A] text-white hover:bg-[#17254B]"
                      }`}
                      onClick={() => requestCheckout(plan, "plans_card_checkout")}
                      type="button"
                    >
                      Assinar
                    </button>
                    <button
                      className={`interactive-hit inline-flex min-h-12 items-center justify-center rounded-full border px-5 text-sm font-black transition focus:outline-none focus:ring-2 focus:ring-[#0E8F7E] focus:ring-offset-2 ${
                        featured
                          ? "border-white/24 bg-white/8 text-white hover:bg-white/14 focus:ring-offset-[#101B3A]"
                          : "border-[#E2DED5] bg-white text-[#101B3A] hover:border-[#0E8F7E]"
                      }`}
                      onClick={() => requestDemo(plan, "plans_card_demo")}
                      type="button"
                    >
                      Ver demo
                    </button>
                  </div>
                </article>
              );
            })}
          </div>
        </div>
      </section>

      <MoneyCalculatorSection
        config={plansCalculatorConfig}
        context="plans"
        onChange={updateCalculatorValue}
        onCta={(label, href) =>
          trackLandingEvent(config.tracking, "cta_click", {
            sourcePage: "/pilates/planos",
            sourceSection: "plans_money_calculator",
            label,
            href,
          })
        }
        plans={plans}
        result={money}
        values={calculatorValues}
      />

      <SimpleSystemComparisonSection />

      <section className="px-4 py-8 sm:px-8 sm:py-10 lg:px-12" id="comparativo">
        <div className="mx-auto max-w-[1520px] lg:w-[80vw]">
          <div className="mb-8 text-center">
            <h2 className="text-4xl font-black leading-none tracking-[-0.055em] text-[#101B3A] sm:text-5xl">
              Compare todos os planos
            </h2>
          </div>
          <MobileComparison
            groups={comparisonSections}
            onCheckout={(plan) => requestCheckout(plan, "plans_mobile_comparison_checkout")}
            onPlanSelect={setSelectedPlanId}
            plans={plans}
            recommendedPlanId={recommendedPlan.id}
            selectedPlanId={selectedPlanId}
          />
          <div className="hidden overflow-x-auto bg-[#FFFDF8] lg:block lg:overflow-visible">
            <table className="w-full min-w-[1060px] border-collapse text-sm">
              <thead>
                <tr>
                  <th className="sticky top-[4.5rem] z-30 w-[25%] bg-[#FFFDF8] px-3 py-4 shadow-[0_1px_0_#DDD7CD]">
                    <span className="sr-only">Recursos</span>
                  </th>
                  {plans.map((plan) => (
                    <th
                      className="sticky top-[4.5rem] z-30 min-w-[12.5rem] bg-[#FFFDF8] px-5 py-4 text-center align-bottom shadow-[0_1px_0_#DDD7CD]"
                      key={plan.id}
                    >
                      <span className="block text-lg font-black text-[#080A0F]">{commercialPlanName(plan)}</span>
                      <button
                        className={`interactive-hit mt-4 inline-flex min-h-12 w-full max-w-[15rem] items-center justify-center rounded-[8px] px-5 text-sm font-black uppercase tracking-[0.04em] transition focus:outline-none focus:ring-2 focus:ring-[#0E8F7E] focus:ring-offset-2 ${
                          plan.id === recommendedPlan.id
                            ? "bg-[#101B3A] text-white hover:bg-[#17254B]"
                            : "bg-[#0E8F7E] text-white hover:bg-[#0A7B6D]"
                        }`}
                        onClick={() => requestCheckout(plan, "plans_comparison_checkout")}
                        type="button"
                      >
                        Assinar
                      </button>
                    </th>
                  ))}
                </tr>
              </thead>
              <tbody>
                {comparisonSections.map((group) => (
                  <ComparisonGroupRows columns={plans} group={group} highlightedColumnId={recommendedPlan.id} key={group.title} />
                ))}
              </tbody>
            </table>
          </div>
        </div>
      </section>

      <PlansSalesCtaSection config={config} />

      <section className="px-4 py-14 sm:px-8 sm:py-16 lg:px-12 lg:py-20" id="faq-planos">
        <div className="mx-auto max-w-4xl">
          <h2 className="text-center text-4xl font-black leading-none tracking-[-0.055em] text-[#101B3A] sm:text-5xl lg:whitespace-nowrap">
            Dúvidas rápidas antes de assinar
          </h2>
          <div className="mt-7 grid gap-3">
            {faqItems.map((item) => (
              <details
                className="group rounded-2xl border border-[#E2DED5] bg-white p-4 shadow-[0_10px_28px_rgba(16,27,58,0.05)] sm:p-5"
                key={item.question}
                onToggle={(event) =>
                  event.currentTarget.open &&
                  trackLandingEvent(config.tracking, "faq_item_opened", {
                    sourcePage: "/pilates/planos",
                    question: item.question,
                  })
                }
              >
                <summary className="cursor-pointer list-none text-base font-black text-[#101B3A] sm:text-lg">
                  {item.question}
                  <span className="float-right text-[#0E8F7E] transition group-open:rotate-45">+</span>
                </summary>
                <p className="mt-3 text-sm font-bold leading-6 text-[#667085]">{item.answer}</p>
              </details>
            ))}
          </div>
        </div>
      </section>

      <div className="py-6 sm:py-8 lg:py-10">
        <FinalCTASection config={config} onCta={trackPlansCustomAgentCta} />
      </div>

      <section className="flex min-h-[38rem] items-center bg-[#FFFDF8] py-14 sm:min-h-[40rem] sm:py-16 lg:min-h-[42.5rem] lg:py-20">
        <div className="flex min-h-[26rem] w-full flex-col items-center justify-center gap-7 bg-[#101B3A] px-5 py-16 text-center text-white sm:py-20 lg:py-24">
          <p className="text-[clamp(2.75rem,6vw,5.6rem)] font-black leading-[0.94] tracking-[-0.07em]">
            Pronto para começar?
          </p>
          <div className="grid w-full gap-3 sm:flex sm:w-auto sm:items-center sm:justify-center">
            <button
              className="interactive-hit inline-flex min-h-14 items-center justify-center rounded-[8px] bg-[#FFB21A] px-8 text-sm font-black text-[#101B3A] shadow-[0_18px_38px_rgba(0,0,0,0.16)] transition hover:bg-[#F8A800] focus:outline-none focus:ring-2 focus:ring-white focus:ring-offset-2 focus:ring-offset-[#101B3A]"
              onClick={() => requestCheckout(recommendedPlan, "plans_final_checkout")}
              type="button"
            >
              Assinar {recommendedPlan.name}
            </button>
            <button
              className="interactive-hit inline-flex min-h-14 items-center justify-center rounded-[8px] border border-white/50 bg-transparent px-8 text-sm font-black text-white transition hover:bg-white/10 focus:outline-none focus:ring-2 focus:ring-white focus:ring-offset-2 focus:ring-offset-[#101B3A]"
              onClick={() => requestDemo(recommendedPlan, "plans_final_demo")}
              type="button"
            >
              Ver demo
            </button>
          </div>
        </div>
      </section>

      <FooterSection config={config} />

      <FloatingAiAttendant
        config={config}
        pageSignals={{
          selectedPainId: undefined,
          selectedAgentId: undefined,
        }}
      />
    </main>
  );
}

type PlanCardFeature = {
  detail?: string;
  included: boolean;
  label: string;
  tooltip: string;
};

function PlanFeatureRow({ feature, featured }: { feature: PlanCardFeature; featured: boolean }) {
  const labelClass = feature.included
    ? featured
      ? "text-white"
      : "text-[#101B3A]"
    : featured
      ? "text-white/42"
      : "text-[#A0A6B2]";
  const detailClass = feature.included
    ? featured
      ? "text-white/64"
      : "text-[#667085]"
    : featured
      ? "text-white/34"
      : "text-[#B4BAC5]";

  return (
    <div className="flex min-h-7 items-start gap-2.5 text-sm font-bold leading-5">
      <span
        aria-hidden="true"
        className={`mt-0.5 inline-flex h-5 w-5 shrink-0 items-center justify-center ${
          feature.included ? (featured ? "text-[#FFB21A]" : "text-[#0E8F7E]") : featured ? "text-white/30" : "text-[#B8B1A6]"
        }`}
      >
        {feature.included ? (
          <svg className="h-5 w-5" fill="none" viewBox="0 0 16 16">
            <path d="m3.5 8.2 2.7 2.7 6.3-6.8" stroke="currentColor" strokeLinecap="round" strokeLinejoin="round" strokeWidth="2.2" />
          </svg>
        ) : (
          <span className="text-xl leading-none">-</span>
        )}
      </span>
      <span className="min-w-0 flex-1">
        <span className={`block ${labelClass}`}>{feature.label}</span>
        {feature.detail ? <span className={`mt-0.5 block text-xs leading-4 ${detailClass}`}>{feature.detail}</span> : null}
      </span>
      <span className={featured && !feature.included ? "opacity-60" : ""}>
        <Tooltip text={feature.tooltip} />
      </span>
    </div>
  );
}

function planCardFeatures(plan: PricingPlan): PlanCardFeature[] {
  return [
    {
      label: "Painel Taliya + app",
      included: true,
      tooltip: "Tela central para ver alunos, tarefas e prioridades.",
    },
    {
      label: "Sistema do studio",
      included: true,
      tooltip: "Base onde ficam contatos, histórico e rotina do studio.",
    },
    {
      label: "WhatsApp Business",
      included: plan.id !== "base",
      tooltip: "Nos planos com agentes, usa o WhatsApp Business do studio.",
    },
    ...comparisonAgents.map((agent) => ({
      label: agent,
      included: planHasComparisonAgent(plan, agent),
      tooltip: agentTooltipCopy(agent),
    })),
    {
      label: "Mensagens dos agentes",
      detail: shortUsageCopy(plan),
      included: plan.id !== "base",
      tooltip: "Quantidade mensal usada nas conversas feitas pelos agentes.",
    },
  ];
}

function BackArrowIcon() {
  return (
    <svg aria-hidden="true" className="h-5 w-5" fill="none" viewBox="0 0 24 24">
      <path d="M15 6l-6 6 6 6" stroke="currentColor" strokeLinecap="round" strokeLinejoin="round" strokeWidth="2.4" />
    </svg>
  );
}

const alternativeComparisonColumns = [
  { id: "simple_system", name: "Sistema simples", role: "Registra" },
  { id: "common_chatbot", name: "Chatbot comum", role: "Responde" },
  { id: "taliya", name: "Taliya", role: "Trabalha" },
] as const;

function coverageValues(
  items: {
    label: string;
    simple: boolean;
    chatbot: boolean;
    simpleLabel?: string;
    chatbotLabel?: string;
    taliyaLabel?: string;
    simpleModes?: ("Manual" | "Automático")[];
    chatbotModes?: ("Manual" | "Automático")[];
    taliyaModes?: ("Manual" | "Automático")[];
  }[],
): ComparisonCell[] {
  const actionablePattern =
    /^(abre|acompanha|agenda|agrupa|ajuda|atualiza|avisa|busca|calcula|chama|coleta|confere|confirma|conduz|conecta|conversa|cria|cruza|deixa|destaca|detecta|direciona|distribui|entende|entrega|envia|evita|identifica|leva|mantem|mantém|marca|oferece|ordena|organiza|pausa|pede|permite|prepara|prioriza|propõe|puxa|reaproveita|recomenda|registra|renova|reserva|retoma|responde|separa|sugere|usa|vincula)(?:\b|\s|$)/i;
  const isActionable = (text: string) => actionablePattern.test(text);

  return [
    {
      kind: "coverage",
      items: items.map((item) => ({
        included: item.simple,
        label: item.simpleLabel ?? item.label,
        modes: item.simple ? (item.simpleModes ?? (isActionable(item.simpleLabel ?? item.label) ? ["Manual"] : undefined)) : undefined,
      })),
    },
    {
      kind: "coverage",
      items: items.map((item) => ({
        included: item.chatbot,
        label: item.chatbotLabel ?? item.label,
        modes: item.chatbot ? (item.chatbotModes ?? (isActionable(item.chatbotLabel ?? item.label) ? ["Automático"] : undefined)) : undefined,
      })),
    },
    {
      kind: "coverage",
      items: items.map((item) => ({
        included: true,
        label: item.taliyaLabel ?? item.label,
        modes: item.taliyaModes ?? (isActionable(item.taliyaLabel ?? item.label) ? ["Manual", "Automático"] : undefined),
      })),
    },
  ];
}

const alternativeComparisonGroups: ComparisonGroup[] = [
  {
    title: "Atendimento e base do studio",
    description: "Rotinas cobertas: nova conversa, dúvidas permitidas e aluno existente.",
    rows: [
      {
        feature: "Nova conversa",
        description: "Primeiro contato no WhatsApp, origem do interessado e intenção inicial.",
        tooltip: "A entrada precisa virar contexto aproveitável, não só uma mensagem respondida.",
        values: coverageValues([
          { label: "Registra no sistema nome, telefone e origem.", simple: true, chatbot: false },
          { label: "Entende se é aluno ou interessado.", simple: false, chatbot: true },
          {
            label: "Cria próximo passo no sistema.",
            simple: false,
            chatbot: false,
            simpleLabel: "Depende da equipe cadastrar depois.",
            chatbotLabel: "Responde, mas não cria rotina no sistema.",
          },
          {
            label: "Mantém contexto para a equipe.",
            simple: false,
            chatbot: false,
            simpleLabel: "Não nasce com contexto de conversa.",
            chatbotLabel: "Não leva o caso para a equipe.",
          },
        ]),
      },
      {
        feature: "Dúvidas permitidas",
        description: "Endereço, funcionamento, regras, primeira aula, planos e informações aprovadas.",
        tooltip: "Responder rápido ajuda, mas responder com regra aprovada e registrar lacuna ajuda mais.",
        values: coverageValues([
          {
            label: "Usa informações aprovadas do studio.",
            simple: true,
            chatbot: true,
            simpleLabel: "Guarda informações aprovadas.",
            chatbotLabel: "Usa respostas configuradas.",
          },
          { label: "Responde dúvidas frequentes.", simple: false, chatbot: true },
          {
            label: "Evita responder o que não está configurado.",
            simple: false,
            chatbot: false,
            simpleLabel: "Depende da equipe conferir a regra.",
            chatbotLabel: "Não valida regra publicada do studio.",
          },
          {
            label: "Cria tarefa quando falta dado na base.",
            simple: false,
            chatbot: false,
            simpleLabel: "Não aponta lacuna sozinho.",
            chatbotLabel: "Não organiza pendência para a equipe.",
          },
        ]),
      },
      {
        feature: "Aluno existente",
        description: "Mensagem de aluno sobre aula, reposição, pagamento, plano ou retorno.",
        tooltip: "O ganho está em reconhecer o aluno e cair na rotina certa desde a primeira resposta.",
        values: coverageValues([
          { label: "Guarda cadastro e histórico do aluno.", simple: true, chatbot: false },
          {
            label: "Identifica a rotina correta da mensagem.",
            simple: false,
            chatbot: false,
            simpleLabel: "Depende da equipe triar.",
            chatbotLabel: "Responde a conversa, mas não leva para a rotina certa.",
          },
          {
            label: "Pede esclarecimento curto quando está ambíguo.",
            simple: false,
            chatbot: true,
            simpleLabel: "Não conversa com o aluno sozinho.",
          },
          {
            label: "Direciona para agenda, financeiro, retenção ou vendas.",
            simple: false,
            chatbot: false,
            simpleLabel: "Não encaminha a rotina sozinho.",
            chatbotLabel: "Não conecta com as rotinas internas.",
          },
        ]),
      },
    ],
  },
  {
    title: "Agenda, turmas e ocupação",
    description: "Rotinas cobertas: confirmação de presença, falta com aviso, reposição/remarcação e vaga aberta.",
    rows: [
      {
        feature: "Confirmação de presença",
        description: "Lembretes, confirmação de alunos, presença esperada e casos que precisam revisão.",
        tooltip: "Confirmar presença é simples, mas precisa ficar refletido na agenda.",
        values: coverageValues([
          { label: "Mostra horários, turma e lista de alunos.", simple: true, chatbot: false },
          { label: "Envia lembrete de presença.", simple: false, chatbot: true },
          {
            label: "Registra confirmação na aula.",
            simple: true,
            chatbot: false,
            simpleLabel: "Permite registrar confirmação na aula.",
            chatbotLabel: "Não atualiza a agenda do studio.",
            taliyaLabel: "Registra confirmação na aula.",
          },
          {
            label: "Mostra exceção para a equipe.",
            simple: false,
            chatbot: false,
            simpleLabel: "Depende da equipe perceber.",
            chatbotLabel: "Não separa exceção para a equipe.",
          },
        ]),
      },
      {
        feature: "Falta com aviso",
        description: "Aluno avisa que não vai, regra precisa ser conferida e a vaga pode ser liberada.",
        tooltip: "A diferença é a falta virar vaga recuperável antes do horário passar.",
        values: coverageValues([
          {
            label: "Registra a ausência.",
            simple: true,
            chatbot: false,
            simpleLabel: "Permite registrar ausência.",
            taliyaLabel: "Registra ausência.",
          },
          {
            label: "Confere regra de reposição.",
            simple: true,
            chatbot: false,
            simpleLabel: "Permite conferir regra de reposição.",
            chatbotLabel: "Não consulta regra do aluno.",
            taliyaLabel: "Confere regra antes de agir.",
          },
          {
            label: "Cria crédito quando permitido.",
            simple: true,
            chatbot: false,
            simpleLabel: "Permite criar crédito quando permitido.",
            chatbotLabel: "Não cria crédito no sistema.",
            taliyaLabel: "Cria crédito quando permitido.",
          },
          {
            label: "Abre vaga para outro aluno.",
            simple: false,
            chatbot: false,
            simpleLabel: "Não abre vaga sozinho.",
            chatbotLabel: "Não atua na ocupação da agenda.",
          },
        ]),
      },
      {
        feature: "Reposição e remarcação",
        description: "Aluno pede para remarcar ou usar reposição, com crédito e horários compatíveis.",
        tooltip: "O sistema mostra possibilidades; a Taliya reduz as trocas repetitivas.",
        values: coverageValues([
          { label: "Mostra agenda e horários possíveis.", simple: true, chatbot: false },
          {
            label: "Confere crédito de reposição.",
            simple: true,
            chatbot: false,
            simpleLabel: "Permite conferir crédito de reposição.",
            chatbotLabel: "Não consulta crédito no sistema.",
            taliyaLabel: "Confere crédito antes de oferecer horário.",
          },
          { label: "Oferece poucas opções compatíveis.", simple: false, chatbot: false },
          {
            label: "Confirma a opção escolhida na agenda.",
            simple: true,
            chatbot: false,
            simpleLabel: "Permite confirmar a opção escolhida.",
            chatbotLabel: "Não confirma aula no sistema.",
            taliyaLabel: "Confirma a opção escolhida na agenda.",
          },
        ]),
      },
      {
        feature: "Recuperar vaga aberta",
        description: "Vaga abre por falta, cancelamento ou baixa ocupação e pode ser preenchida.",
        tooltip: "Aqui está um dos pontos mais diretos de defesa do preço.",
        values: coverageValues([
          { label: "Mostra vaga aberta na agenda.", simple: true, chatbot: false },
          {
            label: "Busca alunos com reposição pendente.",
            simple: true,
            chatbot: false,
            simpleLabel: "Permite buscar alunos com reposição.",
            chatbotLabel: "Não consulta lista de reposição.",
            taliyaLabel: "Busca candidatos com reposição pendente.",
          },
          {
            label: "Cruza preferência de horário.",
            simple: false,
            chatbot: false,
            simpleLabel: "Não cruza preferência sozinho.",
            chatbotLabel: "Não cruza lista, horário e preferência.",
          },
          { label: "Chama a melhor pessoa para ocupar.", simple: false, chatbot: false },
        ]),
      },
    ],
  },
  {
    title: "Vendas e aulas experimentais",
    description: "Rotinas cobertas: valores e planos, aula experimental, pós-aula experimental e pré-matrícula.",
    rows: [
      {
        feature: "Valores e planos",
        description: "Interessado pergunta preço, plano, disponibilidade ou como começar.",
        tooltip: "Responder preço é só uma parte; venda boa puxa o próximo passo.",
        values: coverageValues([
          { label: "Guarda planos e valores.", simple: true, chatbot: false },
          { label: "Responde preço e regras.", simple: false, chatbot: true },
          {
            label: "Confere horário disponível antes de prometer.",
            simple: true,
            chatbot: false,
            simpleLabel: "Permite conferir horário disponível.",
            chatbotLabel: "Não cruza agenda real antes de prometer.",
          },
          {
            label: "Puxa para experimental ou matrícula.",
            simple: false,
            chatbot: false,
            simpleLabel: "Não conduz próximo passo sozinho.",
            chatbotLabel: "Responde, mas não conduz a venda inteira.",
          },
        ]),
      },
      {
        feature: "Aula experimental",
        description: "Agendamento, confirmação, preparação e presença na primeira aula.",
        tooltip: "A experimental só vira receita se o próximo passo não esfriar.",
        values: coverageValues([
          { label: "Guarda interessado e origem.", simple: true, chatbot: false },
          { label: "Responde dúvidas da primeira aula.", simple: false, chatbot: true },
          {
            label: "Agenda experimental.",
            simple: true,
            chatbot: false,
            simpleLabel: "Permite agendar experimental.",
            chatbotLabel: "Não reserva horário na agenda.",
            taliyaLabel: "Agenda experimental.",
          },
          {
            label: "Confirma presença e prepara chegada.",
            simple: true,
            chatbot: false,
            simpleLabel: "Permite confirmar presença e preparar chegada.",
            chatbotLabel: "Não acompanha agenda e presença.",
            taliyaLabel: "Confirma presença e prepara chegada com contexto.",
          },
        ]),
      },
      {
        feature: "Pós-aula experimental",
        description: "Contato depois da aula, objeções, horário fixo e continuidade.",
        tooltip: "Esse é o momento em que muitos interessados bons esfriam.",
        values: coverageValues([
          { label: "Registra que a aula aconteceu.", simple: true, chatbot: false },
          { label: "Guarda observação comercial.", simple: true, chatbot: false },
          {
            label: "Retoma no timing certo.",
            simple: false,
            chatbot: false,
            simpleLabel: "Não retoma sozinho.",
            chatbotLabel: "Não sabe que a aula terminou.",
          },
          {
            label: "Sugere horário fixo e próximo plano.",
            simple: false,
            chatbot: false,
            simpleLabel: "Exige ação comercial da equipe.",
            chatbotLabel: "Não cruza interesse, agenda e plano.",
          },
        ]),
      },
      {
        feature: "Pré-matrícula",
        description: "Dados básicos, escolha de plano, horário fixo e encaminhamento para pagamento.",
        tooltip: "Pré-matrícula boa tira atrito da decisão e deixa a equipe no controle.",
        values: coverageValues([
          { label: "Guarda dados do interessado.", simple: true, chatbot: false },
          {
            label: "Coleta dados básicos na conversa.",
            simple: false,
            chatbot: true,
            simpleLabel: "Depende da equipe coletar.",
            chatbotLabel: "Coleta dados básicos na conversa.",
          },
          {
            label: "Organiza dados no sistema sem perder contexto.",
            simple: true,
            chatbot: false,
            simpleLabel: "Permite organizar dados no sistema.",
            chatbotLabel: "Não organiza tudo no sistema.",
            taliyaLabel: "Organiza dados no sistema sem perder contexto.",
          },
          {
            label: "Vincula plano e horário.",
            simple: true,
            chatbot: false,
            simpleLabel: "Permite vincular plano e horário.",
            chatbotLabel: "Não vincula plano e agenda.",
            taliyaLabel: "Vincula plano e horário.",
          },
          {
            label: "Deixa próximo passo claro para pagamento.",
            simple: false,
            chatbot: false,
            simpleLabel: "Depende da equipe conduzir.",
            chatbotLabel: "Não conecta venda e financeiro.",
          },
        ]),
      },
    ],
  },
  {
    title: "Financeiro e renovações",
    description: "Rotinas cobertas: lembrete de vencimento, Pix/link, confirmação de pagamento e renovação de plano.",
    rows: [
      {
        feature: "Lembrete de vencimento",
        description: "Plano perto de vencer, mensagem cordial e continuidade do aluno.",
        tooltip: "Cobrança boa começa antes de virar atraso.",
        values: coverageValues([
          { label: "Mostra planos vencendo.", simple: true, chatbot: false },
          { label: "Envia lembrete aprovado.", simple: false, chatbot: true },
          {
            label: "Confere contexto antes de falar.",
            simple: true,
            chatbot: false,
            simpleLabel: "Permite conferir contexto.",
            chatbotLabel: "Não cruza frequência, plano e histórico.",
            taliyaLabel: "Confere contexto antes de falar.",
          },
          {
            label: "Acompanha resposta e próximo passo.",
            simple: false,
            chatbot: false,
            simpleLabel: "Não acompanha sozinho.",
            chatbotLabel: "Não registra andamento financeiro.",
          },
        ]),
      },
      {
        feature: "Pix ou link",
        description: "Envio de instrução de pagamento conforme regra do studio.",
        tooltip: "Enviar link sem controle vira conversa solta; enviar com rotina vira cobrança acompanhada.",
        values: coverageValues([
          { label: "Guarda forma de pagamento.", simple: true, chatbot: false },
          { label: "Envia Pix ou link aprovado.", simple: false, chatbot: true },
          {
            label: "Registra que a instrução foi enviada.",
            simple: true,
            chatbot: false,
            simpleLabel: "Permite registrar instrução enviada.",
            chatbotLabel: "Não registra no financeiro.",
            taliyaLabel: "Registra instrução enviada.",
          },
          {
            label: "Pausa se faltar permissão ou dado.",
            simple: false,
            chatbot: false,
            simpleLabel: "Depende da equipe perceber.",
            chatbotLabel: "Não garante controle depois do envio.",
          },
        ]),
      },
      {
        feature: "Confirmação de pagamento",
        description: "Comprovante, baixa, pendência resolvida e continuidade do plano.",
        tooltip: "O problema não é só cobrar; é saber se resolveu.",
        values: coverageValues([
          { label: "Recebe ou guarda comprovante.", simple: true, chatbot: true },
          {
            label: "Confirma pagamento no financeiro.",
            simple: true,
            chatbot: false,
            simpleLabel: "Permite confirmar pagamento.",
            chatbotLabel: "Não dá baixa confiável no sistema.",
            taliyaLabel: "Confirma pagamento no financeiro.",
          },
          {
            label: "Atualiza status do aluno ou plano.",
            simple: true,
            chatbot: false,
            simpleLabel: "Permite atualizar status.",
            chatbotLabel: "Não atualiza cadastro financeiro.",
            taliyaLabel: "Atualiza status do aluno ou plano.",
          },
          {
            label: "Chama humano quando houver divergência.",
            simple: false,
            chatbot: false,
            simpleLabel: "Depende da equipe identificar divergência.",
            chatbotLabel: "Não audita regra e status.",
          },
        ]),
      },
      {
        feature: "Renovação de plano",
        description: "Plano vencendo, manutenção de horário, confirmação e continuidade.",
        tooltip: "Renovação esquecida vira receita atrasada e agenda instável.",
        values: coverageValues([
          { label: "Mostra plano vencendo.", simple: true, chatbot: false },
          {
            label: "Confere horários atuais.",
            simple: true,
            chatbot: false,
            simpleLabel: "Permite conferir horários atuais.",
            chatbotLabel: "Não consulta agenda atual.",
            taliyaLabel: "Confere horários antes de propor renovação.",
          },
          { label: "Envia mensagem de renovação aprovada.", simple: false, chatbot: true },
          {
            label: "Renova plano e mantém horários.",
            simple: true,
            chatbot: false,
            simpleLabel: "Permite renovar plano e manter horários.",
            chatbotLabel: "Não renova no sistema.",
            taliyaLabel: "Renova plano e mantém horários.",
          },
        ]),
      },
    ],
  },
  {
    title: "Retenção e risco de cancelamento",
    description: "Rotinas cobertas: queda de frequência, aluno inativo, retorno e risco de cancelamento.",
    rows: [
      {
        feature: "Queda de frequência",
        description: "Aluno reduz presença antes de pedir pausa ou cancelar.",
        tooltip: "Retenção começa quando o sinal aparece, não quando o cancelamento chega.",
        values: coverageValues([
          { label: "Mostra presença e ausência.", simple: true, chatbot: false },
          {
            label: "Detecta queda de frequência.",
            simple: true,
            chatbot: false,
            simpleLabel: "Permite perceber queda no relatório.",
            chatbotLabel: "Não acompanha frequência.",
            taliyaLabel: "Acompanha queda de frequência.",
          },
          {
            label: "Sugere abordagem de cuidado.",
            simple: false,
            chatbot: false,
            simpleLabel: "Não prepara abordagem sozinho.",
            chatbotLabel: "Não vê histórico e presença.",
          },
          {
            label: "Cria prioridade antes do cancelamento.",
            simple: false,
            chatbot: false,
            simpleLabel: "Depende da equipe cruzar sinais.",
            chatbotLabel: "Não monitora aluno em silêncio.",
          },
        ]),
      },
      {
        feature: "Aluno inativo",
        description: "Aluno sem aula há dias, fora da rotina ou sem próximo horário claro.",
        tooltip: "Aluno inativo precisa de cuidado, não só mensagem pronta.",
        values: coverageValues([
          { label: "Mostra alunos sem presença recente.", simple: true, chatbot: false },
          {
            label: "Separa quem precisa de reativação.",
            simple: true,
            chatbot: false,
            simpleLabel: "Permite filtrar inativos.",
            chatbotLabel: "Não vê frequência.",
            taliyaLabel: "Separa inativos para reativação.",
          },
          {
            label: "Chama com contexto e cuidado.",
            simple: false,
            chatbot: false,
            simpleLabel: "Depende da equipe escrever e lembrar.",
            chatbotLabel: "Não sabe o histórico do aluno.",
          },
          {
            label: "Propõe horário de retorno compatível.",
            simple: false,
            chatbot: false,
            simpleLabel: "Exige busca na agenda.",
            chatbotLabel: "Não cruza retorno com agenda.",
          },
        ]),
      },
      {
        feature: "Retorno",
        description: "Aluno aceita voltar e precisa de horário, cuidado e continuidade.",
        tooltip: "O retorno precisa virar presença real, não só conversa simpática.",
        values: coverageValues([
          { label: "Mostra agenda para retorno.", simple: true, chatbot: false },
          { label: "Conversa com aluno sobre voltar.", simple: false, chatbot: true },
          {
            label: "Reserva horário de retorno.",
            simple: true,
            chatbot: false,
            simpleLabel: "Permite reservar retorno.",
            chatbotLabel: "Não reserva na agenda.",
            taliyaLabel: "Reserva horário de retorno.",
          },
          {
            label: "Avisa equipe com contexto recente.",
            simple: false,
            chatbot: false,
            simpleLabel: "Depende da equipe avisar.",
            chatbotLabel: "Não leva contexto para a equipe.",
          },
        ]),
      },
      {
        feature: "Risco de cancelamento",
        description: "Sinais de pausa, dor, insatisfação, queda de frequência ou mensagem sensível.",
        tooltip: "Aqui a Taliya deve ajudar sem tirar o controle humano.",
        values: coverageValues([
          { label: "Mostra histórico e frequência.", simple: true, chatbot: false },
          {
            label: "Detecta sinais de risco.",
            simple: false,
            chatbot: false,
            simpleLabel: "Depende da equipe interpretar.",
            chatbotLabel: "Não vê sinais da rotina.",
          },
          {
            label: "Pausa o atendimento em caso sensível.",
            simple: false,
            chatbot: false,
            simpleLabel: "Não tem atendimento ativo para pausar.",
            chatbotLabel: "Não escala com contexto suficiente.",
          },
          {
            label: "Agrupa contexto para contato humano.",
            simple: false,
            chatbot: false,
            simpleLabel: "Exige busca em telas.",
            chatbotLabel: "Não conecta histórico e rotina.",
          },
        ]),
      },
    ],
  },
  {
    title: "Gestão e prioridades",
    description: "Rotinas cobertas: prioridades do dia, dinheiro na mesa, fila humana e resumo semanal.",
    rows: [
      {
        feature: "Prioridades do dia",
        description: "Lista do que precisa de ação hoje por impacto, urgência e dinheiro recuperável.",
        tooltip: "Sem prioridade, a rotina vira WhatsApp, planilha, agenda e memória da equipe.",
        values: coverageValues([
          { label: "Mostra relatórios e filtros.", simple: true, chatbot: false },
          { label: "Responde perguntas sob demanda.", simple: false, chatbot: true },
          { label: "Ordena vagas, atrasos, riscos e interessados.", simple: false, chatbot: false },
          { label: "Entrega a próxima ação do dia.", simple: false, chatbot: false },
        ]),
      },
      {
        feature: "Dinheiro na mesa",
        description: "Receita recuperável em vagas, mensalidades, interessados e alunos em risco.",
        tooltip: "Ajuda o dono a comparar dinheiro escapando com custo do plano.",
        values: coverageValues([
          { label: "Mostra dados para análise.", simple: true, chatbot: false },
          {
            label: "Calcula impacto provável.",
            simple: false,
            chatbot: false,
            simpleLabel: "Exige conta da equipe.",
            chatbotLabel: "Não tem dados operacionais confiáveis.",
          },
          {
            label: "Mostra onde agir primeiro.",
            simple: false,
            chatbot: false,
            simpleLabel: "Não prioriza impacto sozinho.",
            chatbotLabel: "Não cruza receita, agenda e retenção.",
          },
          {
            label: "Conecta oportunidade com agente responsável.",
            simple: false,
            chatbot: false,
            simpleLabel: "Depende do dono distribuir.",
            chatbotLabel: "Não opera a rotina depois da resposta.",
          },
        ]),
      },
      {
        feature: "Fila humana",
        description: "Casos que precisam revisão, aprovação ou cuidado de uma pessoa.",
        tooltip: "Rotina boa não some com o humano; ela separa o que realmente precisa dele.",
        values: coverageValues([
          { label: "Permite criar tarefas.", simple: true, chatbot: false, taliyaLabel: "Cria tarefas para a equipe." },
          { label: "Chama humano quando configurado.", simple: false, chatbot: true },
          {
            label: "Mostra motivo, regra e impacto.",
            simple: false,
            chatbot: false,
            simpleLabel: "Não explica impacto sozinho.",
            chatbotLabel: "Encaminha sem contexto da rotina.",
          },
          {
            label: "Distribui para o responsável certo.",
            simple: false,
            chatbot: false,
            simpleLabel: "Depende da equipe distribuir.",
            chatbotLabel: "Não sabe dono da rotina.",
          },
        ]),
      },
      {
        feature: "Resumo semanal",
        description: "O que aconteceu, o que escapou e onde o studio deve ajustar a rotina.",
        tooltip: "Resumo bom não é relatório bonito; é decisão para a próxima semana.",
        values: coverageValues([
          { label: "Tem relatórios para consultar.", simple: true, chatbot: false },
          { label: "Responde perguntas sobre dados informados.", simple: false, chatbot: true },
          {
            label: "Agrupa sinais da semana.",
            simple: false,
            chatbot: false,
            simpleLabel: "Exige análise da equipe.",
            chatbotLabel: "Não acompanha a rotina completa.",
          },
          {
            label: "Recomenda ajustes de rotina.",
            simple: false,
            chatbot: false,
            simpleLabel: "Não recomenda próximo ajuste sozinho.",
            chatbotLabel: "Não conhece regras, agenda e histórico.",
          },
        ]),
      },
    ],
  },
  {
    title: "Histórico, cuidado e evolução",
    description: "Rotinas cobertas: contexto antes da aula, observação pós-aula, restrição/cuidado e objetivo/evolução.",
    rows: [
      {
        feature: "Contexto antes da aula",
        description: "Ficha, objetivo, restrição, observação recente e histórico útil antes do atendimento.",
        tooltip: "Histórico bom evita tratar aluno antigo como se fosse novo.",
        values: coverageValues([
          { label: "Guarda ficha e observações.", simple: true, chatbot: false },
          { label: "Mostra restrições e histórico recente.", simple: true, chatbot: false },
          {
            label: "Leva contexto para conversa ou aula.",
            simple: false,
            chatbot: false,
            simpleLabel: "Depende da equipe abrir a ficha.",
            chatbotLabel: "Não acessa a rotina completa do aluno.",
          },
          {
            label: "Ajuda equipe a não recomeçar do zero.",
            simple: false,
            chatbot: false,
            simpleLabel: "Não entrega contexto proativamente.",
            chatbotLabel: "Não conecta ficha, presença e histórico.",
          },
        ]),
      },
      {
        feature: "Observação pós-aula",
        description: "Nota da aula, evolução percebida, cuidado para a próxima visita e histórico atualizado.",
        tooltip: "A observação só tem valor se voltar para a rotina na hora certa.",
        values: coverageValues([
          { label: "Permite registrar observação.", simple: true, chatbot: false, taliyaLabel: "Registra observação no histórico." },
          {
            label: "Pede ou sugere nota pós-aula.",
            simple: false,
            chatbot: false,
            simpleLabel: "Não lembra professor sozinho.",
            chatbotLabel: "Não sabe que a aula terminou.",
          },
          {
            label: "Atualiza linha do tempo do aluno.",
            simple: true,
            chatbot: false,
            simpleLabel: "Permite atualizar linha do tempo.",
            chatbotLabel: "Não atualiza histórico.",
            taliyaLabel: "Atualiza linha do tempo do aluno.",
          },
          {
            label: "Reaproveita nota no próximo atendimento.",
            simple: false,
            chatbot: false,
            simpleLabel: "Depende da equipe procurar.",
            chatbotLabel: "Não vê histórico do aluno.",
          },
        ]),
      },
      {
        feature: "Restrição e cuidado",
        description: "Dores, limitações, restrições, alerta para professores e resposta cuidadosa.",
        tooltip: "Assunto sensível precisa de contexto e controle humano.",
        values: coverageValues([
          { label: "Guarda restrições importantes.", simple: true, chatbot: false },
          {
            label: "Destaca cuidado antes da aula.",
            simple: false,
            chatbot: false,
            simpleLabel: "Depende da equipe procurar.",
            chatbotLabel: "Não vê ficha e agenda juntas.",
          },
          {
            label: "Pausa o atendimento se parecer sensível.",
            simple: false,
            chatbot: false,
            simpleLabel: "Não tem atendimento ativo para pausar.",
            chatbotLabel: "Não escala com contexto completo.",
          },
          {
            label: "Agrupa histórico para contato humano.",
            simple: false,
            chatbot: false,
            simpleLabel: "Exige busca da equipe.",
            chatbotLabel: "Não conecta histórico, cuidado e rotina.",
          },
        ]),
      },
      {
        feature: "Objetivo e evolução",
        description: "Objetivo do aluno, evolução, preferências e acompanhamento do progresso.",
        tooltip: "Evolução vira retenção quando aparece no atendimento e na conversa certa.",
        values: coverageValues([
          { label: "Guarda objetivo e evolução.", simple: true, chatbot: false },
          { label: "Mostra histórico de notas.", simple: true, chatbot: false },
          {
            label: "Sugere cuidado ou próximo foco.",
            simple: false,
            chatbot: false,
            simpleLabel: "Não sugere foco sozinho.",
            chatbotLabel: "Não vê histórico de evolução.",
          },
          {
            label: "Usa evolução para reter e personalizar contato.",
            simple: false,
            chatbot: false,
            simpleLabel: "Depende da equipe conectar os pontos.",
            chatbotLabel: "Não conecta evolução com retenção.",
          },
        ]),
      },
    ],
  },
];

function SimpleSystemComparisonSection() {
  return (
    <section className="scroll-mt-24 px-4 py-8 sm:px-8 sm:py-10 lg:px-12" id="comparativo-alternativas">
      <div className="mx-auto max-w-[1520px] lg:w-[80vw]">
        <div className="mb-6 text-center sm:mb-8">
          <h2 className="mx-auto max-w-4xl text-[2rem] font-black leading-[0.98] tracking-[-0.045em] text-[#101B3A] sm:text-5xl sm:leading-none sm:tracking-[-0.055em]">
            Por que Taliya não é só sistema nem só chatbot?
          </h2>
        </div>
        <AlternativeMobileComparison groups={alternativeComparisonGroups} />
        <div className="hidden overflow-x-auto bg-[#FFFDF8] lg:block lg:overflow-visible">
          <table className="w-full min-w-[960px] border-collapse text-sm">
            <thead>
              <tr>
                <th className="sticky top-[4.5rem] z-30 w-[25%] bg-[#FFFDF8] px-3 py-4 shadow-[0_1px_0_#DDD7CD]">
                  <span className="sr-only">Situações</span>
                </th>
                {alternativeComparisonColumns.map((column) => (
                  <th
                    className="sticky top-[4.5rem] z-30 min-w-[13.5rem] bg-[#FFFDF8] px-5 py-4 text-center align-bottom shadow-[0_1px_0_#DDD7CD]"
                    key={column.id}
                  >
                    <span className="block text-lg font-black text-[#080A0F]">{column.name}</span>
                    <span
                      className={`mt-4 inline-flex min-h-10 w-full max-w-[15rem] items-center justify-center rounded-[8px] px-5 text-sm font-black uppercase tracking-[0.04em] ${
                        column.id === "taliya" ? "bg-[#101B3A] text-white" : "bg-[#F1ECE3] text-[#667085]"
                      }`}
                    >
                      {column.role}
                    </span>
                  </th>
                ))}
              </tr>
            </thead>
            <tbody>
              {alternativeComparisonGroups.map((group) => (
                <ComparisonGroupRows
                  columns={alternativeComparisonColumns}
                  group={group}
                  highlightedColumnClassName="bg-[#F5FBF8] border-x border-[#CDEFE4]"
                  highlightedColumnId="taliya"
                  key={group.title}
                />
              ))}
            </tbody>
          </table>
        </div>
      </div>
    </section>
  );
}

function AlternativeMobileComparison({ groups }: { groups: ComparisonGroup[] }) {
  const [selectedGroupIndex, setSelectedGroupIndex] = useState(0);
  const [transitionDirection, setTransitionDirection] = useState<1 | -1>(1);
  const [touchState, setTouchState] = useState<TouchState | null>(null);
  const selectedGroup = groups[selectedGroupIndex] ?? groups[0];
  const dragOffset = touchState?.intent === "horizontal" ? touchState.offsetX : 0;

  function selectGroup(nextIndex: number, direction?: 1 | -1) {
    const normalizedIndex = (nextIndex + groups.length) % groups.length;
    setTransitionDirection(direction ?? (normalizedIndex >= selectedGroupIndex ? 1 : -1));
    setSelectedGroupIndex(normalizedIndex);
  }

  function moveGroup(direction: 1 | -1) {
    selectGroup(selectedGroupIndex + direction, direction);
  }

  function handleTouchStart(touch: { clientX: number; clientY: number }) {
    setTouchState({ startX: touch.clientX, startY: touch.clientY, offsetX: 0, intent: "pending" });
  }

  function handleTouchMove(touch: { clientX: number; clientY: number }) {
    setTouchState((current) => {
      if (!current || current.intent === "vertical") return current;

      const deltaX = touch.clientX - current.startX;
      const deltaY = touch.clientY - current.startY;
      const absX = Math.abs(deltaX);
      const absY = Math.abs(deltaY);

      if (current.intent === "pending" && absY > SWIPE_INTENT_PX && absY > absX * 1.15) {
        return { ...current, intent: "vertical", offsetX: 0 };
      }

      if (current.intent === "pending" && (absX < SWIPE_INTENT_PX || absX < absY * 1.25)) {
        return current;
      }

      return {
        ...current,
        intent: "horizontal",
        offsetX: Math.max(-SWIPE_MAX_OFFSET_PX, Math.min(SWIPE_MAX_OFFSET_PX, deltaX)),
      };
    });
  }

  function handleTouchEnd() {
    if (!touchState || touchState.intent !== "horizontal") {
      setTouchState(null);
      return;
    }

    const delta = touchState.offsetX;
    setTouchState(null);
    if (Math.abs(delta) < SWIPE_COMMIT_PX) return;
    moveGroup(delta < 0 ? 1 : -1);
  }

  return (
    <div
      className="lg:hidden"
      onTouchCancel={() => setTouchState(null)}
      onTouchEnd={handleTouchEnd}
      onTouchMove={(event) => {
        const touch = event.touches[0];
        if (touch) handleTouchMove(touch);
      }}
      onTouchStart={(event) => {
        const touch = event.touches[0];
        if (touch) handleTouchStart(touch);
      }}
    >
      <div className="sticky top-[4.5rem] z-30 -mx-4 mb-4 flex items-center justify-between gap-3 border-y border-[#E2DED5]/80 bg-[#FFFDF8]/95 px-4 py-3 shadow-[0_10px_28px_rgba(16,27,58,0.08)] backdrop-blur-xl sm:-mx-8 sm:px-8">
        <button
          aria-label="Ver tópico anterior"
          className="interactive-hit grid h-11 w-11 shrink-0 place-items-center rounded-full border border-[#E2DED5] bg-white text-[#101B3A] shadow-[0_8px_20px_rgba(16,27,58,0.08)] focus:outline-none focus:ring-2 focus:ring-[#0E8F7E]"
          onClick={() => moveGroup(-1)}
          type="button"
        >
          &lt;
        </button>
        <div className="min-w-0 text-center">
          <p className="text-xs font-black uppercase tracking-[0.16em] text-[#0E8F7E]">
            {selectedGroupIndex + 1}/{groups.length}
          </p>
          <p className="mt-1 text-lg font-black leading-5 tracking-[-0.035em] text-[#101B3A] [text-wrap:balance]">{selectedGroup.title}</p>
        </div>
        <button
          aria-label="Ver próximo tópico"
          className="interactive-hit grid h-11 w-11 shrink-0 place-items-center rounded-full border border-[#E2DED5] bg-white text-[#101B3A] shadow-[0_8px_20px_rgba(16,27,58,0.08)] focus:outline-none focus:ring-2 focus:ring-[#0E8F7E]"
          onClick={() => moveGroup(1)}
          type="button"
        >
          &gt;
        </button>
      </div>

      <article
        className={`topic-carousel-slide mobile-swipe-slide overflow-hidden rounded-[22px] border border-[#E2DED5] bg-white shadow-[0_12px_34px_rgba(16,27,58,0.06)] ${touchState?.intent === "horizontal" ? "is-dragging" : ""}`}
        data-direction={transitionDirection}
        key={selectedGroup.title}
        style={{ "--carousel-drag-x": `${dragOffset}px` } as CSSProperties}
      >
        <div className="border-b border-[#E2DED5] bg-[#FBF8F2] p-4">
          <p className="text-sm font-bold leading-6 text-[#667085]">{selectedGroup.description}</p>
        </div>
        <div className="divide-y divide-[#E2DED5]">
          {selectedGroup.rows.map((row) => (
            <div className="p-4" key={`${selectedGroup.title}-${row.feature}`}>
              <FeatureLabel description={row.description} title={row.feature} tooltip={row.tooltip} />
              <div className="mt-4 grid gap-3">
                {row.values.map((cell, index) => {
                  const column = alternativeComparisonColumns[index];
                  const featured = column.id === "taliya";

                  return (
                    <div
                      className={`rounded-[16px] border p-4 ${
                        featured ? "border-[#0E8F7E]/32 bg-[#F4FBF8]" : "border-[#E2DED5] bg-[#FFFDF8]"
                      }`}
                      key={`${row.feature}-${column.id}`}
                    >
                      <p className={`text-xs font-black uppercase tracking-[0.16em] ${featured ? "text-[#0E8F7E]" : "text-[#98A2B3]"}`}>
                        {column.name}
                      </p>
                      <div className="mt-3">
                        <ComparisonCellView cell={cell} featured={featured} />
                      </div>
                    </div>
                  );
                })}
              </div>
            </div>
          ))}
        </div>
      </article>

      <div className="mt-4 flex items-center justify-center gap-1.5">
        {groups.map((group, index) => (
          <button
            aria-label={`Ver tópico ${group.title}`}
            className="interactive-hit grid h-8 w-8 place-items-center rounded-full focus:outline-none focus:ring-2 focus:ring-[#0E8F7E]"
            key={group.title}
            onClick={() => selectGroup(index)}
            type="button"
          >
            <span className={`h-2.5 rounded-full transition-all ${index === selectedGroupIndex ? "w-8 bg-[#101B3A]" : "w-2.5 bg-[#D8D2C8]"}`} />
          </button>
        ))}
      </div>
    </div>
  );
}

function PlansSalesCtaSection({ config }: { config: NicheLandingConfig }) {
  const whatsappHref = withWhatsAppMessage(config.assistedConversion.humanWhatsAppDestination.href, config.salesCta.whatsappMessage);

  function openDiagnostic() {
    trackLandingEvent(config.tracking, "cta_click", {
      sourcePage: "/pilates/planos",
      label: config.salesCta.primaryCta,
      href: "#floating-agent",
      sourceSection: "studio_diagnostic",
      entryPath: "diagnostic_cta",
    });
    window.dispatchEvent(
      new CustomEvent("landing:open-sales-agent", {
        detail: {
          sourceSection: "studio_diagnostic",
          message: "Quero fazer diagnóstico gratuito",
        },
      }),
    );
  }

  function trackWhatsApp() {
    const destination = config.assistedConversion.humanWhatsAppDestination;
    trackLandingEvent(config.tracking, "human_whatsapp_clicked", {
      sourcePage: "/pilates/planos",
      sourceSection: "studio_diagnostic_whatsapp",
      destinationLabel: destination.label,
      destinationKind: destination.kind,
      destinationHref: destination.href,
      conversionPurpose: config.assistedConversion.conversionPurpose,
    });
  }

  return (
    <SectionShell id="diagnostico" tone="plain" className="!min-h-0 !py-14 sm:!py-16 lg:!items-center lg:!py-20" contentClassName="py-0">
      <div className="mx-auto max-w-6xl text-center">
        <h2 className="mx-auto max-w-5xl text-[clamp(3rem,6vw,6rem)] font-black leading-[0.92] tracking-[-0.075em] text-[#080A0F]">
          {config.salesCta.title}
        </h2>
        <p className="mx-auto mt-5 max-w-3xl text-lg font-bold leading-8 text-[#667085]">{config.salesCta.subtitle}</p>

        <div className="mt-10 flex flex-col items-center justify-center gap-3 sm:flex-row">
          <button
            className="interactive-hit inline-flex min-h-16 w-full items-center justify-center gap-2 rounded-full bg-[#101B3A] px-8 text-base font-black leading-5 text-white shadow-[0_18px_42px_rgba(16,27,58,0.20)] transition hover:bg-[#17254B] focus:outline-none focus:ring-2 focus:ring-[#0E8F7E] focus:ring-offset-2 sm:w-auto sm:min-w-[18rem] lg:min-w-[21rem] lg:px-10 lg:text-lg"
            onClick={openDiagnostic}
            type="button"
          >
            <span>{config.salesCta.primaryCta}</span>
            <span aria-hidden="true" className="shrink-0">→</span>
          </button>
          <a
            className="interactive-hit inline-flex min-h-16 w-full items-center justify-center gap-2 rounded-full border border-[#E2DED5] bg-white px-8 text-base font-black leading-5 text-[#101B3A] shadow-[0_14px_32px_rgba(16,27,58,0.08)] transition hover:border-[#0E8F7E]/40 focus:outline-none focus:ring-2 focus:ring-[#0E8F7E] focus:ring-offset-2 sm:w-auto sm:min-w-[18rem] lg:min-w-[21rem] lg:px-10 lg:text-lg"
            href={whatsappHref}
            onClick={trackWhatsApp}
            rel="noreferrer"
            target="_blank"
          >
            <span>{config.salesCta.secondaryCta}</span>
            <span aria-hidden="true" className="shrink-0">→</span>
          </a>
        </div>

        <p className="mx-auto mt-5 max-w-2xl text-sm font-bold leading-6 text-[#667085]">{config.salesCta.microcopy}</p>
      </div>
    </SectionShell>
  );
}

type ComparisonTone = "green" | "blue" | "yellow" | "gray" | "dark";

type ComparisonCell =
  | {
      kind: "check";
      label?: string;
      detail?: string;
      tone?: ComparisonTone;
    }
  | {
      kind: "dash";
      label?: string;
      detail?: string;
    }
  | {
      kind: "x";
      label?: string;
      detail?: string;
    }
  | {
      kind: "pill";
      label: string;
      detail?: string;
      tone?: ComparisonTone;
    }
  | {
      kind: "text";
      label: string;
      detail?: string;
    }
  | {
      kind: "coverage";
      items: {
        included: boolean;
        label: string;
        modes?: ("Manual" | "Automático")[];
      }[];
    }
  | {
      kind: "verdict";
      verdict: "check" | "x";
      label: string;
      bullets: string[];
    }
  | {
      kind: "status";
      label: string;
      detail?: string;
      tone: ComparisonTone;
      icon?: "check";
    };

type ComparisonRow = {
  feature: string;
  description: string;
  tooltip?: string;
  values: ComparisonCell[];
};

type ComparisonGroup = {
  title: string;
  description: string;
  rows: ComparisonRow[];
};

type ComparisonColumn = {
  id: string;
  name: string;
};

type LandingAgent = NicheLandingConfig["agents"][number];

function ComparisonGroupRows({
  columns,
  group,
  highlightedColumnClassName = "",
  highlightedColumnId,
}: {
  columns: readonly ComparisonColumn[];
  group: ComparisonGroup;
  highlightedColumnClassName?: string;
  highlightedColumnId: string;
}) {
  return (
    <>
      <tr>
        <th className="border-b border-[#DDD7CD] px-3 pb-4 pt-8 text-left" colSpan={columns.length + 1}>
          <span className="block text-2xl font-black tracking-[-0.04em] text-[#080A0F]">{group.title}</span>
          <span className="sr-only">{group.description}</span>
        </th>
      </tr>
      {group.rows.map((row) => (
        <tr key={`${group.title}-${row.feature}`}>
          <th className="border-b border-[#E2DED5] px-3 py-4 align-middle text-left">
            <FeatureLabel description={row.description} title={row.feature} tooltip={row.tooltip} />
          </th>
          {row.values.map((cell, index) => {
            const column = columns[index];
            const featured = column.id === highlightedColumnId;

            return (
              <td
                className={`border-b border-[#E2DED5] px-5 py-4 text-center align-middle ${featured ? highlightedColumnClassName : ""}`}
                key={`${row.feature}-${column.id}`}
              >
                <ComparisonCellView cell={cell} featured={featured} />
              </td>
            );
          })}
        </tr>
      ))}
    </>
  );
}

function FeatureLabel({ description, title, tooltip }: { description: string; title: string; tooltip?: string }) {
  return (
    <div className="flex items-center justify-between gap-3">
      <div>
        <span className="block text-base font-black text-[#080A0F]">{title}</span>
        <span className="sr-only">{description}</span>
      </div>
      <span className="shrink-0">
        {tooltip ? <Tooltip text={tooltip} /> : null}
      </span>
    </div>
  );
}

function Tooltip({ text }: { text: string }) {
  return (
    <span className="group relative inline-flex">
      <button
        aria-label={`Explicacao: ${text}`}
        className="inline-flex h-5 w-5 items-center justify-center rounded-full border border-[#858B98] bg-transparent text-[11px] font-black text-[#667085] transition hover:border-[#0E8F7E] hover:text-[#101B3A] focus:outline-none focus:ring-2 focus:ring-[#0E8F7E]"
        type="button"
      >
        ?
      </button>
      <span className="pointer-events-none absolute bottom-8 right-0 z-50 w-[min(16rem,calc(100vw-2rem))] rounded-2xl bg-[#101B3A] p-3 text-left text-xs font-bold leading-5 text-white opacity-0 shadow-[0_18px_44px_rgba(16,27,58,0.2)] transition group-focus-within:opacity-100 group-hover:opacity-100 sm:left-1/2 sm:right-auto sm:-translate-x-1/2">
        {text}
      </span>
    </span>
  );
}

function MobileComparison({
  groups,
  onCheckout,
  onPlanSelect,
  plans,
  recommendedPlanId,
  selectedPlanId,
}: {
  groups: ComparisonGroup[];
  onCheckout: (plan: PricingPlan) => void;
  onPlanSelect: (planId: string) => void;
  plans: PricingPlan[];
  recommendedPlanId: string;
  selectedPlanId: string;
}) {
  const [transitionDirection, setTransitionDirection] = useState<1 | -1>(1);
  const [touchState, setTouchState] = useState<TouchState | null>(null);
  const selectedIndex = Math.max(
    0,
    plans.findIndex((plan) => plan.id === selectedPlanId),
  );
  const selectedPlan = plans[selectedIndex] ?? plans[0];
  const dragOffset = touchState?.intent === "horizontal" ? touchState.offsetX : 0;

  function selectPlan(nextIndex: number, direction?: 1 | -1) {
    const normalizedIndex = (nextIndex + plans.length) % plans.length;
    setTransitionDirection(direction ?? (normalizedIndex >= selectedIndex ? 1 : -1));
    onPlanSelect(plans[normalizedIndex]?.id ?? plans[0]?.id ?? selectedPlanId);
  }

  function movePlan(direction: 1 | -1) {
    selectPlan(selectedIndex + direction, direction);
  }

  function handleTouchStart(touch: { clientX: number; clientY: number }) {
    setTouchState({ startX: touch.clientX, startY: touch.clientY, offsetX: 0, intent: "pending" });
  }

  function handleTouchMove(touch: { clientX: number; clientY: number }) {
    setTouchState((current) => {
      if (!current || current.intent === "vertical") return current;

      const deltaX = touch.clientX - current.startX;
      const deltaY = touch.clientY - current.startY;
      const absX = Math.abs(deltaX);
      const absY = Math.abs(deltaY);

      if (current.intent === "pending" && absY > SWIPE_INTENT_PX && absY > absX * 1.15) {
        return { ...current, intent: "vertical", offsetX: 0 };
      }

      if (current.intent === "pending" && (absX < SWIPE_INTENT_PX || absX < absY * 1.25)) {
        return current;
      }

      return {
        ...current,
        intent: "horizontal",
        offsetX: Math.max(-SWIPE_MAX_OFFSET_PX, Math.min(SWIPE_MAX_OFFSET_PX, deltaX)),
      };
    });
  }

  function handleTouchEnd() {
    if (!touchState || touchState.intent !== "horizontal") {
      setTouchState(null);
      return;
    }

    const delta = touchState.offsetX;
    setTouchState(null);
    if (Math.abs(delta) < SWIPE_COMMIT_PX) return;
    movePlan(delta < 0 ? 1 : -1);
  }

  return (
    <div
      className="lg:hidden"
      onTouchCancel={() => setTouchState(null)}
      onTouchEnd={handleTouchEnd}
      onTouchMove={(event) => {
        const touch = event.touches[0];
        if (touch) handleTouchMove(touch);
      }}
      onTouchStart={(event) => {
        const touch = event.touches[0];
        if (touch) handleTouchStart(touch);
      }}
    >
      <div className="sticky top-[4.5rem] z-30 -mx-4 mb-4 flex items-center justify-between gap-3 border-y border-[#E2DED5]/80 bg-[#FFFDF8]/95 px-4 py-3 shadow-[0_10px_28px_rgba(16,27,58,0.08)] backdrop-blur-xl sm:-mx-8 sm:px-8">
        <button
          aria-label="Ver plano anterior"
          className="interactive-hit grid h-11 w-11 shrink-0 place-items-center rounded-full border border-[#E2DED5] bg-white text-[#101B3A] shadow-[0_8px_20px_rgba(16,27,58,0.08)] focus:outline-none focus:ring-2 focus:ring-[#0E8F7E]"
          onClick={() => movePlan(-1)}
          type="button"
        >
          &lt;
        </button>
        <div className="min-w-0 text-center">
          <p className="text-xs font-black uppercase tracking-[0.16em] text-[#0E8F7E]">
            {selectedIndex + 1}/{plans.length}
          </p>
          <p className="mt-1 text-xl font-black tracking-[-0.04em] text-[#101B3A]">{commercialPlanName(selectedPlan)}</p>
          <p className="text-sm font-bold text-[#667085]">{selectedPlan.monthlyPriceLabel}</p>
        </div>
        <button
          aria-label="Ver próximo plano"
          className="interactive-hit grid h-11 w-11 shrink-0 place-items-center rounded-full border border-[#E2DED5] bg-white text-[#101B3A] shadow-[0_8px_20px_rgba(16,27,58,0.08)] focus:outline-none focus:ring-2 focus:ring-[#0E8F7E]"
          onClick={() => movePlan(1)}
          type="button"
        >
          &gt;
        </button>
      </div>

      <div
        className={`topic-carousel-slide mobile-swipe-slide overflow-hidden rounded-[22px] border border-[#E2DED5] bg-white shadow-[0_12px_34px_rgba(16,27,58,0.07)] ${touchState?.intent === "horizontal" ? "is-dragging" : ""}`}
        data-direction={transitionDirection}
        key={selectedPlan.id}
        style={{ "--carousel-drag-x": `${dragOffset}px` } as CSSProperties}
      >
        <div className="flex items-center justify-between gap-3 border-b border-[#E2DED5] bg-[#FFFDF8] p-4">
          <div className="min-w-0">
            <p className="text-lg font-black text-[#101B3A]">{commercialPlanName(selectedPlan)}</p>
            <p className="text-sm font-bold text-[#667085]">{selectedPlan.monthlyPriceLabel}</p>
          </div>
          {selectedPlan.id === recommendedPlanId ? (
            <span className="rounded-full bg-[#FFB21A] px-3 py-1 text-[11px] font-black text-[#101B3A]">Melhor</span>
          ) : null}
        </div>
        <table className="w-full border-collapse text-sm">
          <tbody>
            {groups.map((group) => (
              <MobileComparisonGroupRows group={group} key={group.title} planIndex={selectedIndex} />
            ))}
          </tbody>
        </table>
        <div className="border-t border-[#E2DED5] bg-[#FFFDF8] p-4">
          <button
            className="interactive-hit inline-flex min-h-12 w-full items-center justify-center rounded-full bg-[#101B3A] px-5 text-sm font-black text-white transition hover:bg-[#17254B] focus:outline-none focus:ring-2 focus:ring-[#0E8F7E] focus:ring-offset-2"
            onClick={() => onCheckout(selectedPlan)}
            type="button"
          >
            Assinar {commercialPlanName(selectedPlan)}
          </button>
        </div>
      </div>

      <div className="mt-4 flex items-center justify-center gap-1.5">
        {plans.map((plan, index) => (
          <button
            aria-label={`Ver plano ${commercialPlanName(plan)}`}
            className="interactive-hit grid h-8 w-8 place-items-center rounded-full focus:outline-none focus:ring-2 focus:ring-[#0E8F7E]"
            key={plan.id}
            onClick={() => selectPlan(index)}
            type="button"
          >
            <span className={`h-2.5 rounded-full transition-all ${index === selectedIndex ? "w-8 bg-[#101B3A]" : "w-2.5 bg-[#D8D2C8]"}`} />
          </button>
        ))}
      </div>
    </div>
  );
}

function MobileComparisonGroupRows({ group, planIndex }: { group: ComparisonGroup; planIndex: number }) {
  return (
    <>
      <tr>
        <th className="border-b border-[#DDD7CD] bg-[#FBF8F2] px-4 py-4 text-left" colSpan={2}>
          <span className="block text-base font-black tracking-[-0.03em] text-[#080A0F]">{group.title}</span>
          <span className="sr-only">{group.description}</span>
        </th>
      </tr>
      {group.rows.map((row) => (
        <tr key={`${group.title}-${row.feature}`}>
          <th className="w-[58%] border-b border-[#E2DED5] px-4 py-4 align-middle text-left">
            <FeatureLabel description={row.description} title={row.feature} tooltip={row.tooltip} />
          </th>
          <td className="w-[42%] border-b border-[#E2DED5] px-3 py-4 text-center align-middle">
            <ComparisonCellView cell={row.values[planIndex] ?? row.values[0]} featured={false} />
          </td>
        </tr>
      ))}
    </>
  );
}

function ComparisonCellView({ cell, featured }: { cell: ComparisonCell; featured: boolean }) {
  if (cell.kind === "coverage") {
    return (
      <div className="mx-auto max-w-[18rem] text-left">
        <ul className="grid gap-2">
          {cell.items.map((item) => (
            <li className="flex items-start gap-2.5" key={item.label}>
              <CoverageIcon included={item.included} />
              <span
                className={`text-xs font-bold leading-5 ${
                  item.included ? (featured ? "text-[#101B3A]" : "text-[#344054]") : "text-[#667085]"
                }`}
              >
                {item.label}
                {item.modes?.length ? (
                  <span className="ml-1.5 inline-flex translate-y-[-1px] gap-1">
                    {item.modes.map((mode) => (
                      <span
                        className={`rounded-full px-1.5 py-0.5 text-[0.55rem] font-black uppercase leading-none tracking-[0.04em] ${
                          mode === "Manual" ? "bg-[#F1ECE3] text-[#667085]" : "bg-[#DDF8EA] text-[#08715E]"
                        }`}
                        key={mode}
                      >
                        {mode}
                      </span>
                    ))}
                  </span>
                ) : null}
              </span>
            </li>
          ))}
        </ul>
      </div>
    );
  }

  if (cell.kind === "verdict") {
    return (
      <div className="mx-auto max-w-[18rem] text-left">
        <div className="flex items-start gap-2.5">
          <StatusIcon kind={cell.verdict} />
          <div className="min-w-0">
            <p className={`text-base font-black leading-5 ${featured ? "text-[#101B3A]" : "text-[#344054]"}`}>{cell.label}</p>
            <ul className="mt-2 grid gap-1.5">
              {cell.bullets.map((bullet) => (
                <li className="flex gap-2 text-xs font-bold leading-5 text-[#667085]" key={bullet}>
                  <span className={`mt-2 h-1.5 w-1.5 shrink-0 rounded-full ${cell.verdict === "check" ? "bg-[#0E8F7E]" : "bg-[#A44A3F]"}`} />
                  <span>{bullet}</span>
                </li>
              ))}
            </ul>
          </div>
        </div>
      </div>
    );
  }

  if (cell.kind === "check") {
    return (
      <div className="flex items-center justify-center gap-2">
        <StatusIcon kind="check" />
        {cell.label && cell.label !== "Incluído" ? <CellText detail={cell.detail} featured={featured} label={cell.label} /> : null}
      </div>
    );
  }

  if (cell.kind === "dash") {
    return (
      <div className="flex items-center justify-center gap-2">
        <StatusIcon kind="dash" />
        {cell.label && cell.label !== "Não incluído" ? <CellText detail={cell.detail} featured={featured} label={cell.label} /> : null}
      </div>
    );
  }

  if (cell.kind === "x") {
    return (
      <div className="flex items-center justify-center gap-2">
        <StatusIcon kind="x" />
        {cell.label ? <CellText detail={cell.detail} featured={featured} label={cell.label} /> : null}
      </div>
    );
  }

  if (cell.kind === "pill") {
    return (
      <div className="text-center">
        <span className={`inline-flex rounded-full px-3 py-1 text-xs font-black ${pillToneClass(cell.tone ?? "gray", featured)}`}>{cell.label}</span>
        {cell.detail ? <p className={`mt-2 text-xs font-bold leading-5 ${featured ? "text-white/72" : "text-[#667085]"}`}>{cell.detail}</p> : null}
      </div>
    );
  }

  if (cell.kind === "status") {
    return (
      <div className="text-center">
        <span className={`inline-flex items-center gap-1.5 rounded-full px-3 py-1 text-xs font-black ${pillToneClass(cell.tone, featured)}`}>
          {cell.icon === "check" ? (
            <svg aria-hidden="true" className="h-3.5 w-3.5" fill="none" viewBox="0 0 16 16">
              <path d="m3.5 8.2 2.7 2.7 6.3-6.8" stroke="currentColor" strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" />
            </svg>
          ) : null}
          {cell.label}
        </span>
        {cell.detail ? <p className={`mt-2 text-xs font-bold leading-5 ${featured ? "text-white/72" : "text-[#667085]"}`}>{cell.detail}</p> : null}
      </div>
    );
  }

  return <CellText detail={cell.detail} featured={featured} label={cell.label} />;
}

function CellText({ detail, featured, label }: { detail?: string; featured: boolean; label: string }) {
  return (
    <div>
      <p className={`text-base font-bold leading-5 ${featured ? "text-[#101B3A]" : "text-[#344054]"}`}>{label}</p>
      {detail ? <p className="mt-1 text-xs font-bold leading-5 text-[#667085]">{detail}</p> : null}
    </div>
  );
}

function CoverageIcon({ included }: { included: boolean }) {
  if (!included) {
    return (
      <span className="mt-0.5 inline-flex h-4 w-4 shrink-0 items-center justify-center text-[#A44A3F]">
        <svg aria-hidden="true" className="h-3.5 w-3.5" fill="none" viewBox="0 0 16 16">
          <path d="M4.25 4.25 11.75 11.75M11.75 4.25 4.25 11.75" stroke="currentColor" strokeLinecap="round" strokeWidth="2.2" />
        </svg>
      </span>
    );
  }

  return (
    <span className="mt-0.5 inline-flex h-4 w-4 shrink-0 items-center justify-center text-[#0E8F7E]">
      <svg aria-hidden="true" className="h-4 w-4" fill="none" viewBox="0 0 16 16">
        <path d="m3.5 8.2 2.7 2.7 6.3-6.8" stroke="currentColor" strokeLinecap="round" strokeLinejoin="round" strokeWidth="2.2" />
      </svg>
    </span>
  );
}

function StatusIcon({ kind }: { kind: "check" | "dash" | "x" }) {
  if (kind === "x") {
    return <span className="inline-flex h-6 w-6 shrink-0 items-center justify-center text-2xl font-black leading-none text-[#A44A3F]">×</span>;
  }

  if (kind === "dash") {
    return <span className="inline-flex h-6 w-6 shrink-0 items-center justify-center text-3xl font-bold leading-none text-[#7D828C]">-</span>;
  }

  return (
    <span className="inline-flex h-6 w-6 shrink-0 items-center justify-center text-[#0E8F7E]">
      <svg aria-hidden="true" className="h-6 w-6" fill="none" viewBox="0 0 16 16">
        <path d="m3.5 8.2 2.7 2.7 6.3-6.8" stroke="currentColor" strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" />
      </svg>
    </span>
  );
}

function pillToneClass(tone: ComparisonTone, featured: boolean) {
  if (featured && tone === "dark") return "bg-[#101B3A] text-white";
  if (tone === "green") return "bg-[#DDF8EA] text-[#08715E]";
  if (tone === "blue") return "bg-[#E6EEFF] text-[#2437A8]";
  if (tone === "yellow") return "bg-[#FFF0C2] text-[#835400]";
  if (tone === "dark") return "bg-[#101B3A] text-white";
  return "bg-[#F1ECE3] text-[#667085]";
}

const comparisonAgents = [
  "Atendimento",
  "Agenda",
  "Vendas",
  "Financeiro",
  "Retenção",
  "Gestão",
  "Histórico/Evolução",
] as const;

function planHasComparisonAgent(plan: PricingPlan, agent: (typeof comparisonAgents)[number]) {
  if (plan.id === "seven_agents") return true;
  if (plan.id === "three_agents") return agent === "Atendimento" || agent === "Agenda" || agent === "Vendas";
  if (plan.id === "one_agent") return agent === "Atendimento";
  return false;
}

function agentComparisonCell(plan: PricingPlan, agent: (typeof comparisonAgents)[number]): ComparisonCell {
  return planHasComparisonAgent(plan, agent) ? { kind: "check" } : { kind: "x" };
}

function agentFlowCell(plan: PricingPlan, agent: (typeof comparisonAgents)[number]): ComparisonCell {
  if (planHasComparisonAgent(plan, agent)) {
    return {
      kind: "status",
      label: "Taliya trabalha",
      tone: "green",
      icon: "check",
    };
  }

  return {
    kind: "status",
    label: "Organizado",
    tone: "gray",
  };
}

function agentFlowTooltip(trigger: string, action: string) {
  return `Organizado: a equipe acompanha no sistema. Com Taliya: ela percebe o caso e ajuda no próximo passo. Quando acontece: ${trigger}. O que a Taliya faz: ${action}.`;
}

function agentFlowGroups(plans: PricingPlan[], agents: LandingAgent[]): ComparisonGroup[] {
  return comparisonAgents.map((agentName) => {
    const agent = agents.find((item) => item.name === agentName || (agentName === "Histórico/Evolução" && item.id === "historico-evolucao"));
    const flows = agent?.operationalFlows?.slice(0, 4) ?? [];

    return {
      title: agentName,
      description: agent?.role ?? agentRoleCopy(agentName),
      rows: flows.map((flow) => ({
        feature: flow.title,
        description: flow.result,
        tooltip: agentFlowTooltip(flow.trigger, flow.action),
        values: plans.map((plan) => agentFlowCell(plan, agentName)),
      })),
    };
  });
}

function comparisonGroups(plans: PricingPlan[], agents: LandingAgent[]): ComparisonGroup[] {
  return [
    {
      title: "Indicação",
      description: "O jeito mais rápido de entender qual plano combina com o momento do studio.",
      rows: [
        {
          feature: "Momento do studio",
          description: "Resumo rápido do encaixe de cada plano.",
          tooltip: "Mostra quando cada plano costuma fazer sentido.",
          values: plans.map((plan) => ({ kind: "text", label: planMomentCopy(plan) })),
        },
        {
          feature: "Foco principal",
          description: "O que o plano resolve primeiro.",
          tooltip: "Resume a primeira entrega prática de cada plano.",
          values: plans.map((plan) => ({ kind: "text", label: planFocusCopy(plan) })),
        },
        {
          feature: "Melhor para",
          description: "Perfil de studio que tende a aproveitar melhor cada plano.",
          tooltip: "Ajuda a comparar o plano com o momento do studio.",
          values: plans.map((plan) => ({ kind: "text", label: plan.bestFor })),
        },
      ],
    },
    {
      title: "Base do sistema",
      description: "A fundação da Taliya para organizar alunos, contatos, tarefas e rotina.",
      rows: [
        {
          feature: "Painel Taliya",
          description: "Tela central para acompanhar alunos, tarefas e prioridades.",
          tooltip: "Tela central para ver rotina, alunos e tarefas.",
          values: plans.map(() => ({ kind: "check" })),
        },
        {
          feature: "Taliya App",
          description: "Acesso ao sistema para operar a rotina do studio.",
          tooltip: "Acesso ao sistema para operar a rotina.",
          values: plans.map(() => ({ kind: "check" })),
        },
        {
          feature: "Alunos e contatos",
          description: "Base para organizar alunos, interessados e responsáveis.",
          tooltip: "Base única para alunos, interessados e contatos.",
          values: plans.map(() => ({ kind: "check" })),
        },
        {
          feature: "Tarefas e prioridades",
          description: "Lista do que precisa de atenção no dia.",
          tooltip: "Mostra pendências e próximos passos da equipe.",
          values: plans.map(() => ({ kind: "check" })),
        },
        {
          feature: "Histórico básico",
          description: "Registro inicial de aluno, contato e rotina.",
          tooltip: "Organiza contexto básico. O agente completo entra no Completo.",
          values: plans.map(() => ({ kind: "check" })),
        },
      ],
    },
    {
      title: "Agentes da Taliya",
      description: "O que muda quando a Taliya deixa de só organizar e começa a acompanhar a rotina.",
      rows: comparisonAgents.map((agent) => ({
        feature: agent,
        description: agentRoleCopy(agent),
        tooltip: agentTooltipCopy(agent),
        values: plans.map((plan) => agentComparisonCell(plan, agent)),
      })),
    },
    ...agentFlowGroups(plans, agents),
    {
      title: "Começo e decisão",
      description: "O que ajuda o studio a escolher com segurança e começar sem confusão.",
      rows: [
        {
          feature: "Diagnóstico",
          description: "Ajuda para confirmar o plano antes de decidir.",
          tooltip: "Ajuda a escolher o plano antes de assinar.",
          values: plans.map((plan) => ({ kind: "text", label: diagnosticFitCopy(plan) })),
        },
        {
          feature: "Configuração",
          description: "Como a Taliya começa a ser configurada depois da escolha.",
          tooltip: "Configuração inicial de regras, rotinas e acesso.",
          values: plans.map((plan) => ({ kind: "text", label: plan.setupExpectation })),
        },
      ],
    },
  ];
}

function commercialPlanName(plan: PricingPlan) {
  return planPresentation[plan.id]?.name ?? plan.name;
}

function shortPositioning(plan: PricingPlan) {
  if (plan.id === "base") return "Base para organizar contatos, alunos e rotina antes dos agentes entrarem.";
  if (plan.id === "one_agent") return "Um agente para atacar a dor mais urgente do studio.";
  if (plan.id === "three_agents") return "Tres agentes para conectar atendimento, agenda e vendas.";
  if (plan.id === "seven_agents") return "Time principal trabalhando junto na rotina completa.";
  return plan.positioning;
}

function planMomentCopy(plan: PricingPlan) {
  if (plan.id === "base") return "Organizar a casa";
  if (plan.id === "one_agent") return "Começar pelo atendimento";
  if (plan.id === "three_agents") return "Conectar atendimento, agenda e vendas";
  if (plan.id === "seven_agents") return "Rotina completa";
  return plan.bestFor;
}

function planFocusCopy(plan: PricingPlan) {
  if (plan.id === "base") return "Base do sistema, sem agentes ativos.";
  if (plan.id === "one_agent") return "Responder melhor e não perder interessados.";
  if (plan.id === "three_agents") return "Organizar entrada, agenda e conversão.";
  if (plan.id === "seven_agents") return "Acompanhar agenda, vendas, financeiro, retenção, gestão e evolução.";
  return plan.positioning;
}

function diagnosticFitCopy(plan: PricingPlan) {
  if (plan.id === "base") return "Opcional, para confirmar se vale começar sem agentes.";
  if (plan.id === "one_agent") return "Recomendado para escolher a primeira dor certa.";
  if (plan.id === "three_agents") return "Recomendado para priorizar as três rotinas.";
  if (plan.id === "seven_agents") return "Recomendado para validar o caminho completo.";
  return "Recomendado antes de decidir.";
}

function shortUsageCopy(plan: PricingPlan) {
  if (plan.id === "base") return "Sem mensagens dos agentes";
  const match = plan.usageBoundary.match(/([\d.]+)\s+mensagens/i);
  return match ? `${match[1]} mensagens/mês` : plan.usageBoundary;
}

function agentRoleCopy(agent: string) {
  if (agent === "Atendimento") return "Responde interessados e alunos.";
  if (agent === "Agenda") return "Organiza faltas e reposições.";
  if (agent === "Vendas") return "Conduz experimental e matrícula.";
  if (agent === "Financeiro") return "Acompanha cobranças e renovações.";
  if (agent === "Retencao" || agent === "Retenção") return "Puxa alunos em risco de sumir.";
  if (agent === "Gestao" || agent === "Gestão") return "Mostra prioridades do dia.";
  return "Guarda contexto e evolução.";
}

function agentTooltipCopy(agent: string) {
  if (agent === "Atendimento") return "Responde dúvidas e chama humano quando precisa.";
  if (agent === "Agenda") return "Acompanha faltas, cancelamentos e reposições.";
  if (agent === "Vendas") return "Ajuda em experimental, retorno e matrícula.";
  if (agent === "Financeiro") return "Acompanha cobranças, vencimentos e lembretes.";
  if (agent === "Retenção") return "Identifica alunos sumindo e ajuda a reativar.";
  if (agent === "Gestão") return "Mostra prioridades e pontos de atenção do dia.";
  return "Guarda histórico, restrições e evolução do aluno.";
}

function withWhatsAppMessage(href: string, message: string) {
  if (!href.includes("wa.me")) return href;

  const [base] = href.split("?");
  return `${base}?text=${encodeURIComponent(message)}`;
}
