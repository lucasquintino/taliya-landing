import type { NicheLandingConfig, PricingPlan, TrustedDestination } from "@/data/landing/niches/types";
import { FormField } from "../shared/FormField";
import { SectionShell } from "../shared/SectionShell";

export function EarlyAccessSection({
  config,
  onAssistedClick,
  onFocus,
  onHumanWhatsApp,
  onPlanCta,
  onSubmit,
}: {
  config: NicheLandingConfig;
  onAssistedClick: () => void;
  onFocus: () => void;
  onHumanWhatsApp: (destination: TrustedDestination, sourceSection: string, plan?: PricingPlan) => void;
  onPlanCta: (plan: PricingPlan, destination: TrustedDestination, sourceSection: string) => void;
  onSubmit: (event: React.FormEvent<HTMLFormElement>) => void;
}) {
  const { assistedConversion, subscription } = config;

  return (
    <SectionShell id="planos" tone="white" contentClassName="py-10 sm:py-14">
      <span aria-hidden="true" className="sr-only" id="acesso-antecipado" />
      <div className="grid gap-10">
        <div className="grid gap-6 lg:grid-cols-[0.9fr_1.1fr] lg:items-end">
          <div className="max-w-3xl">
            <p className="text-xs font-black uppercase tracking-[0.24em] text-[#0E8F7E]">Planos Taliya</p>
            <h2 className="mt-4 text-[clamp(2.25rem,4.6vw,4.5rem)] font-black leading-none text-[#101B3A]">
              {config.earlyAccess.title}
            </h2>
            <p className="mt-5 text-lg leading-8 text-[#667085]">{config.earlyAccess.description}</p>
          </div>
          <div className="grid gap-3 sm:grid-cols-2">
            {config.earlyAccess.offerItems.slice(0, 4).map((item) => (
              <div className="rounded-2xl border border-[#E2DED5] bg-[#FBF8F2] p-4 text-sm font-black text-[#344054]" key={item}>
                {item}
              </div>
            ))}
          </div>
        </div>

        <div className="grid gap-4 lg:grid-cols-3">
          {subscription.plans.map((plan) => (
            <article
              className={`flex min-h-[520px] flex-col rounded-[28px] border bg-white p-5 shadow-[0_24px_60px_rgba(16,27,58,0.08)] ${
                plan.recommended ? "border-[#0E8F7E] ring-4 ring-[#0E8F7E]/10" : "border-[#E2DED5]"
              }`}
              key={plan.id}
            >
              <div className="flex items-start justify-between gap-4">
                <div>
                  <p className="text-sm font-black text-[#0E8F7E]">{plan.bestFor}</p>
                  <h3 className="mt-2 text-3xl font-black text-[#101B3A]">{plan.name}</h3>
                </div>
                {plan.recommended ? (
                  <span className="rounded-full bg-[#0E8F7E] px-3 py-1 text-xs font-black text-white">Mais escolhido</span>
                ) : null}
              </div>

              <p className="mt-5 text-4xl font-black text-[#101B3A]">{plan.monthlyPriceLabel}</p>
              <p className="mt-2 min-h-12 text-sm leading-6 text-[#667085]">{plan.positioning}</p>
              <div className="mt-4 grid gap-2 rounded-2xl bg-[#FBF8F2] p-4 text-xs font-bold leading-5 text-[#667085]">
                <p>{plan.whatsappAvailability}</p>
                <p>{plan.usageBoundary}</p>
              </div>

              <div className="mt-5 grid gap-2">
                {plan.includedAgents.slice(0, 6).map((agent) => (
                  <div className="flex gap-2 text-sm font-bold text-[#344054]" key={agent}>
                    <span className="mt-1 h-2 w-2 shrink-0 rounded-full bg-[#FFB21A]" />
                    <span>{agent}</span>
                  </div>
                ))}
              </div>

              <div className="mt-auto grid gap-3 pt-6">
                <a
                  className="interactive-hit inline-flex min-h-12 items-center justify-center rounded-full bg-[#101B3A] px-5 text-sm font-black text-white transition hover:bg-[#18264F] focus:outline-none focus:ring-2 focus:ring-[#0E8F7E] focus:ring-offset-2"
                  href={plan.primaryCta.href}
                  onClick={() => onPlanCta(plan, plan.primaryCta, "plans")}
                >
                  {plan.primaryCta.label}
                </a>
                <a
                  className="interactive-hit inline-flex min-h-12 items-center justify-center rounded-full border border-[#E2DED5] bg-white px-5 text-sm font-black text-[#101B3A] transition hover:border-[#0E8F7E] focus:outline-none focus:ring-2 focus:ring-[#0E8F7E] focus:ring-offset-2"
                  href={plan.secondaryHumanCta.href}
                  onClick={() => onHumanWhatsApp(plan.secondaryHumanCta, "plans", plan)}
                >
                  {plan.secondaryHumanCta.label}
                </a>
                <p className="text-xs leading-5 text-[#667085]">{plan.setupExpectation}</p>
              </div>
            </article>
          ))}
        </div>

        <div className="grid gap-6 lg:grid-cols-[0.9fr_1.1fr] lg:items-start">
          <div className="rounded-[28px] border border-[#E2DED5] bg-[#FBF8F2] p-6 sm:p-8">
            <p className="text-xs font-black uppercase tracking-[0.22em] text-[#0E8F7E]">Atendimento assistido</p>
            <h3 className="mt-3 text-3xl font-black text-[#101B3A]">{assistedConversion.title}</h3>
            <p className="mt-3 text-sm leading-6 text-[#667085]">{assistedConversion.subtitle}</p>
            <a
              className="interactive-hit mt-5 inline-flex min-h-12 items-center justify-center rounded-full border border-[#0E8F7E]/30 bg-white px-5 text-sm font-black text-[#0E8F7E] transition hover:border-[#0E8F7E] focus:outline-none focus:ring-2 focus:ring-[#0E8F7E] focus:ring-offset-2"
              href={assistedConversion.humanWhatsAppDestination.href}
              onClick={() => onHumanWhatsApp(assistedConversion.humanWhatsAppDestination, "assisted_conversion")}
            >
              {assistedConversion.humanWhatsAppDestination.label}
            </a>
            <p className="mt-3 text-xs leading-5 text-[#667085]">{assistedConversion.whatsappConsentText}</p>
          </div>

          <form className="rounded-[28px] border border-[#E2DED5] bg-white p-5 shadow-[0_24px_60px_rgba(16,27,58,0.08)] sm:p-6" onFocus={onFocus} onSubmit={onSubmit}>
            <p className="text-xs font-black uppercase tracking-[0.22em] text-[#FFB21A]">Ajuda para escolher</p>
            <h3 className="mt-3 text-3xl font-black text-[#101B3A]">{config.form.title}</h3>
            <p className="mt-3 text-sm leading-6 text-[#667085]">{config.form.subtitle}</p>
            <div className="mt-5 grid gap-4 sm:grid-cols-2">
              <FormField label="Seu nome" name="name" required />
              <FormField label="WhatsApp" name="whatsapp" required type="tel" />
              <FormField label="Nome do studio" name="studioName" />
              <FormField label="Cidade/estado" name="cityState" />
              <FormField label="Alunos ativos" name="activeStudents" type="number" />
              <label className="grid gap-2 sm:col-span-2">
                <span className="text-sm font-black text-[#344054]">Maior dor hoje</span>
                <select className="min-h-12 rounded-2xl border border-[#DDD8CF] bg-[#FBF8F2] px-4 py-3 text-[#101B3A] outline-none transition focus:border-[#0E8F7E] focus:ring-4 focus:ring-[#0E8F7E]/15" name="biggestPain">
                  {config.form.painOptions.map((option) => (
                    <option key={option}>{option}</option>
                  ))}
                </select>
              </label>
              <label className="grid gap-2 sm:col-span-2">
                <span className="text-sm font-black text-[#344054]">Sistema atual</span>
                <select className="min-h-12 rounded-2xl border border-[#DDD8CF] bg-[#FBF8F2] px-4 py-3 text-[#101B3A] outline-none transition focus:border-[#0E8F7E] focus:ring-4 focus:ring-[#0E8F7E]/15" name="currentSystem">
                  {config.form.systemOptions.map((option) => (
                    <option key={option}>{option}</option>
                  ))}
                </select>
              </label>
              <label className="grid gap-2 sm:col-span-2">
                <span className="text-sm font-black text-[#344054]">Rotina que você queria</span>
                <textarea className="min-h-28 rounded-2xl border border-[#DDD8CF] bg-[#FBF8F2] px-4 py-3 text-[#101B3A] outline-none transition focus:border-[#0E8F7E] focus:ring-4 focus:ring-[#0E8F7E]/15" name="customRoutine" />
              </label>
              <label className="grid gap-2 sm:col-span-2">
                <span className="text-sm font-black text-[#344054]">Próximo passo preferido</span>
                <select className="min-h-12 rounded-2xl border border-[#DDD8CF] bg-[#FBF8F2] px-4 py-3 text-[#101B3A] outline-none transition focus:border-[#0E8F7E] focus:ring-4 focus:ring-[#0E8F7E]/15" name="preferredNextStep">
                  {config.form.accessOptions.map((option) => (
                    <option key={option}>{option}</option>
                  ))}
                </select>
              </label>
              <label className="flex gap-3 text-xs leading-5 text-[#667085] sm:col-span-2">
                <input className="mt-1 h-4 w-4 shrink-0 accent-[#0E8F7E]" name="lgpdConsent" required type="checkbox" value="accepted" />
                <span>
                  {assistedConversion.consentText}{" "}
                  <a className="font-black text-[#0E8F7E] underline-offset-4 hover:underline" href={assistedConversion.privacyNotice.href}>
                    {assistedConversion.privacyNotice.label}
                  </a>
                  .
                </span>
              </label>
              <input name="niche" readOnly type="hidden" value={config.niche} />
              <input name="publicOfferMode" readOnly type="hidden" value={config.tracking.publicOfferMode} />
              <input name="conversionPurpose" readOnly type="hidden" value={assistedConversion.conversionPurpose} />
            </div>
            <button
              className="interactive-hit mt-5 inline-flex w-full min-h-12 items-center justify-center rounded-full bg-[#FFB21A] px-6 py-4 text-sm font-black text-[#101B3A] transition hover:bg-[#F8A800] focus:outline-none focus:ring-2 focus:ring-[#101B3A]"
              onClick={onAssistedClick}
              type="submit"
            >
              {config.earlyAccess.cta} <span aria-hidden="true" className="ml-2">→</span>
            </button>
          </form>
        </div>
      </div>
    </SectionShell>
  );
}
