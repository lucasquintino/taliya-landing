"use client";

import { useState } from "react";
import type { BillingPeriod, NicheLandingConfig } from "@/data/landing/niches/types";
import { SectionShell } from "../shared/SectionShell";

export function PlanOfferSection({
  config,
  onStartSubscription,
}: {
  config: NicheLandingConfig;
  onStartSubscription: (billingPeriod: BillingPeriod) => void;
}) {
  const [billingPeriod, setBillingPeriod] = useState<BillingPeriod>("annual");
  const offer = config.launchOffer;
  const billingOption = billingPeriod === "annual" ? offer.annual : offer.monthly;
  const priceLabel = billingPeriod === "annual"
    ? new Intl.NumberFormat("pt-BR", { style: "currency", currency: "BRL" }).format(offer.annual.priceBRL / 12)
    : billingOption.price;
  const periodLabel = billingPeriod === "annual" ? "por mês" : billingOption.period;

  return (
    <SectionShell id="planos" tone="warm" className="is-visible !min-h-0 !py-12 sm:!py-14 lg:!py-16" contentClassName="py-0">
      <div className="mx-auto max-w-7xl">
        <header className="mx-auto max-w-7xl text-center">
          <p className="text-xs font-black uppercase tracking-[0.24em] text-[#0E8F7E]">Plano Taliya</p>
          <h2 className="mt-4 text-balance text-[clamp(2rem,3.7vw,3.75rem)] font-black leading-[0.96] tracking-[-0.06em] text-[#101B3A] lg:whitespace-nowrap">
            {offer.title}
          </h2>
          <p className="mx-auto mt-5 max-w-none text-[clamp(1rem,1.25vw,1.125rem)] font-medium leading-7 text-[#667085] lg:whitespace-nowrap">
            {offer.body}
          </p>
        </header>

        <article className="mx-auto mt-10 grid max-w-6xl overflow-hidden rounded-[30px] border border-[#E2DED5] bg-white shadow-[0_28px_80px_rgba(16,27,58,0.10)] lg:grid-cols-[0.9fr_1.1fr]">
          <div className="flex flex-col bg-[#101B3A] p-6 text-white sm:p-9 lg:p-10">
            <p className="text-xs font-black uppercase tracking-[0.22em] text-[#76DDD0]">{offer.name}</p>
            <p className="mt-5 text-sm font-bold text-white/75">{offer.toggleLabel}</p>
            <div aria-label={offer.toggleLabel} className="mt-3 grid grid-cols-2 rounded-full border border-white/15 bg-white/10 p-1" role="group">
              {(["monthly", "annual"] as const).map((period) => {
                const option = period === "annual" ? offer.annual : offer.monthly;
                const selected = billingPeriod === period;

                return (
                  <button
                    aria-pressed={selected}
                    className={`interactive-hit min-h-11 rounded-full px-4 text-sm font-black transition ${
                      selected ? "bg-white text-[#101B3A] shadow-sm" : "text-white/80 hover:text-white"
                    }`}
                    key={period}
                    onClick={() => setBillingPeriod(period)}
                    type="button"
                  >
                    {option.label}
                  </button>
                );
              })}
            </div>

            <div aria-live="polite" className="mt-8">
              <div className="flex flex-wrap items-baseline gap-x-3 gap-y-1">
                <p className="text-[clamp(2.7rem,6vw,4.5rem)] font-black leading-none tracking-[-0.06em]">{priceLabel}</p>
                <span className="text-base font-bold text-white/75">{periodLabel}</span>
              </div>
              <p className="mt-3 text-sm font-medium leading-6 text-white/75">{billingOption.renewal}</p>
            </div>

            <div className="mt-7 rounded-2xl border border-white/10 bg-white/10 px-4 py-3 text-sm font-black leading-6 text-white">
              {offer.trial}
            </div>

            <div className="mt-auto pt-6">
              <button
                className="interactive-hit inline-flex min-h-14 w-full items-center justify-center gap-2 rounded-full bg-[#76DDD0] px-6 text-base font-black text-[#101B3A] shadow-[0_14px_36px_rgba(0,0,0,0.18)] transition hover:bg-[#98E8DE] focus:outline-none focus:ring-2 focus:ring-white focus:ring-offset-2 focus:ring-offset-[#101B3A]"
                onClick={() => onStartSubscription(billingPeriod)}
                type="button"
              >
                <span>{offer.cta}</span>
                <span aria-hidden="true">→</span>
              </button>

              {offer.smallPrint ? <p className="mt-4 text-xs font-medium leading-5 text-white/65">{offer.smallPrint}</p> : null}
            </div>
          </div>

          <div className="flex flex-col p-6 sm:p-9 lg:p-10">
            <ul className="grid gap-4 sm:gap-5">
              {offer.benefits.map((benefit) => (
                <li className="flex items-start gap-3" key={benefit.title}>
                  <span aria-hidden="true" className="mt-0.5 grid h-6 w-6 shrink-0 place-items-center rounded-full bg-[#E7F7F3] text-sm font-black text-[#0E8F7E]">✓</span>
                  <span>
                    <span className="block text-sm font-black leading-6 text-[#101B3A] sm:text-base">{benefit.title}</span>
                    <span className="mt-0.5 block text-sm font-medium leading-6 text-[#667085]">{benefit.description}</span>
                  </span>
                </li>
              ))}
            </ul>
          </div>
        </article>
      </div>
    </SectionShell>
  );
}
