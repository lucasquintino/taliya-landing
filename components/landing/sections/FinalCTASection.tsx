"use client";

import { useEffect, useId, useRef, useState } from "react";
import type { NicheLandingConfig } from "@/data/landing/niches/types";
import type { CustomAgentDiagnosticResponse } from "@/lib/landing/ai-attendant/custom-diagnostic";
import { trackLandingEvent } from "@/lib/landing/tracking";
import { SectionShell } from "../shared/SectionShell";

export function FinalCTASection({
  config,
  onCta,
}: {
  config: NicheLandingConfig;
  onCta: (label: string, href: string) => void;
}) {
  const isPlansPage = config.floatingAgent.label === "Consultor";
  const reactId = useId();
  const [description, setDescription] = useState("");
  const [report, setReport] = useState<CustomAgentDiagnosticResponse | null>(null);
  const [pending, setPending] = useState(false);
  const [error, setError] = useState("");
  const startedTrackedRef = useRef(false);
  const [sessionId] = useState(() => `diag_${reactId.replaceAll(":", "")}_${Date.now().toString(36)}`);
  const diagnosticComingSoon = true;

  function trackStarted() {
    if (startedTrackedRef.current) return;
    startedTrackedRef.current = true;
    trackLandingEvent(config.tracking, "custom_agent_diagnostic_started", {
      sourceSection: "final_diagnostic_cta",
    });
  }

  async function submitDiagnostic() {
    const cleanDescription = description.trim();
    onCta("Gerar diagnóstico", config.finalCta.cta.href);

    if (cleanDescription.length < 3) {
      openConsultor("diagnostic_unclear", "Quero falar com a equipe para entender o melhor caminho para meu negócio.");
      return;
    }

    setPending(true);
    setError("");
    trackLandingEvent(config.tracking, "custom_agent_diagnostic_submitted", {
      sourceSection: "final_diagnostic_cta",
      descriptionLength: cleanDescription.length,
    });

    try {
      const response = await fetch("/api/landing/custom-agent-diagnostic", {
        method: "POST",
        headers: { "content-type": "application/json" },
        body: JSON.stringify({
          sessionId,
          niche: config.niche,
          sourcePage: typeof window !== "undefined" ? window.location.pathname : config.route,
          sourceSection: "final_diagnostic_cta",
          campaignStage: config.tracking.campaignStage,
          publicOfferMode: config.tracking.publicOfferMode,
          description: cleanDescription,
        }),
      });
      const payload = (await response.json()) as CustomAgentDiagnosticResponse | { error?: string };
      if (!response.ok || "error" in payload) throw new Error("error" in payload ? payload.error : "Diagnostic request failed.");
      const diagnosticReport = payload as CustomAgentDiagnosticResponse;

      setReport(diagnosticReport);
      trackLandingEvent(config.tracking, "custom_agent_diagnostic_generated", {
        sourceSection: "final_diagnostic_cta",
        reportId: diagnosticReport.reportId,
        classification: diagnosticReport.classification,
        contextVariant: diagnosticReport.diagnosticContextVariant,
        conversionPath: diagnosticReport.leadEffect.conversionPath,
        mappedAgentIds: diagnosticReport.mappedAgentIds,
        recommendedPlanId: diagnosticReport.recommendedPlanId,
        safeSummary: diagnosticReport.leadEffect.safeSummary,
      });
    } catch {
      setError(isPlansPage
        ? "Não consegui gerar o diagnóstico agora. Posso abrir o consultor com seu contexto."
        : "Não consegui preparar uma sugestão agora. Posso continuar a conversa com a Taliya usando esse contexto.");
      trackLandingEvent(config.tracking, "custom_agent_diagnostic_failed", {
        sourceSection: "final_diagnostic_cta",
      });
    } finally {
      setPending(false);
    }
  }

  function handleReportCta(cta: CustomAgentDiagnosticResponse["ctas"][number]) {
    if (!report) return;
    trackLandingEvent(config.tracking, "custom_agent_diagnostic_cta_clicked", {
      sourceSection: "final_diagnostic_cta",
      reportId: report.reportId,
      classification: report.classification,
      contextVariant: cta.contextVariant,
      destination: cta.destination,
      conversionPath: report.leadEffect.conversionPath,
      safeSummary: report.leadEffect.safeSummary,
    });
    void fetch("/api/landing/custom-agent-diagnostic/cta", {
      method: "POST",
      headers: { "content-type": "application/json" },
      body: JSON.stringify({
        sessionId,
        niche: config.niche,
        sourcePage: typeof window !== "undefined" ? window.location.pathname : config.route,
        reportId: report.reportId,
        selectedCtaId: cta.id,
        classification: report.classification,
        contextVariant: cta.contextVariant,
        conversionPath: report.leadEffect.conversionPath,
        safeSummary: report.leadEffect.safeSummary,
        mappedAgentIds: report.mappedAgentIds,
        customAgent: report.customAgent,
      }),
    });

    if (cta.destination === "configured_whatsapp") {
      window.open(withWhatsAppMessage(config.assistedConversion.humanWhatsAppDestination.href, messageForVariant(cta.contextVariant, report)), "_blank", "noreferrer");
      return;
    }

    if (cta.destination === "configured_guided_demo") {
      window.location.href = config.floatingAgent.guidedDemoDestination.href;
      return;
    }

    openConsultor(cta.contextVariant, messageForVariant(cta.contextVariant, report));
  }

  function openConsultor(contextVariant: string, message: string) {
    window.dispatchEvent(
      new CustomEvent("landing:open-sales-agent", {
        detail: {
          sourceSection: contextVariant.includes("diagnostic") ? "custom_agent_diagnostic" : "final_diagnostic_cta",
          message,
        },
      }),
    );
  }

  return (
    <SectionShell id="cta-final" tone="warm" className="is-visible min-h-0" contentClassName="py-10 sm:py-14">
      <div className="custom-diagnostic mx-auto max-w-7xl text-center">
        <h2 className="custom-diagnostic-title mx-auto max-w-6xl text-[clamp(2.35rem,8vw,5.1rem)] font-black leading-[0.95] text-[#080A0F] sm:leading-[0.92]">
          {config.finalCta.title}
        </h2>
        <p className="custom-diagnostic-copy mx-auto mt-4 max-w-3xl text-base font-semibold leading-7 text-[#667085] sm:text-lg">
          {config.finalCta.description}
        </p>

        <DiagnosticComposer
          description={description}
          onChange={(value) => {
            trackStarted();
            setDescription(value);
          }}
          onSubmit={() => void submitDiagnostic()}
          pending={pending}
          placeholder={config.finalCta.promptPlaceholder}
          submitDisabled={diagnosticComingSoon}
          submitLabel="Em breve"
        />

        {error ? (
          <div className="mx-auto mt-5 grid max-w-xl justify-items-center gap-3 rounded-[18px] border border-[#F2D6A2] bg-[#FFF8EA] px-4 py-4">
            <p className="text-sm font-bold leading-6 text-[#8A5A00]">{error}</p>
            <button
              className="interactive-hit inline-flex min-h-12 items-center justify-center rounded-full bg-[#101B3A] px-5 text-sm font-black text-white"
              onClick={() => openConsultor("diagnostic_unclear", description || "Quero falar com a equipe sobre meu negócio.")}
              type="button"
            >
              {isPlansPage ? "Abrir consultor" : "Continuar com a Taliya"}
            </button>
          </div>
        ) : null}

        {report ? <DiagnosticReport report={report} onCta={handleReportCta} /> : null}
      </div>
    </SectionShell>
  );
}

function DiagnosticComposer({
  description,
  onChange,
  onSubmit,
  pending,
  placeholder,
  submitDisabled,
  submitLabel,
}: {
  description: string;
  onChange: (value: string) => void;
  onSubmit: () => void;
  pending: boolean;
  placeholder: string;
  submitDisabled?: boolean;
  submitLabel?: string;
}) {
  const loadingSteps = [
    "Interpretando o contexto do seu negócio...",
    "Separando o que a Taliya já cobre...",
    "Mapeando se existe rotina sob medida...",
    "Preparando o melhor próximo passo...",
  ];

  return (
    <div className="mx-auto mt-8 max-w-5xl sm:mt-10">
      <form
        className="custom-diagnostic-form rounded-[26px] bg-[linear-gradient(90deg,#2F91F5,#D95AD9,#FF8A3D)] p-[3px] text-left shadow-[0_22px_55px_rgba(16,27,58,0.14)]"
        onSubmit={(event) => {
          event.preventDefault();
          if (!pending && !submitDisabled) onSubmit();
        }}
      >
        <div className="flex min-h-[96px] flex-col gap-4 rounded-[23px] bg-[#FFFDF8]/96 px-4 py-4 backdrop-blur-xl sm:min-h-[104px] sm:flex-row sm:items-center sm:px-7 lg:px-8">
          <textarea
            aria-label="Conte a rotina que você precisa organizar"
            className="custom-diagnostic-textarea min-h-[5.5rem] min-w-0 flex-1 resize-none bg-transparent text-left text-lg font-semibold leading-7 text-[#344054] outline-none placeholder:text-[#9BA3AF] sm:min-h-[4.25rem] sm:text-xl lg:text-2xl"
            disabled={pending}
            onChange={(event) => onChange(event.target.value)}
            placeholder={placeholder}
            value={description}
          />

          {pending ? (
            <button
              className="interactive-hit inline-flex min-h-[3.25rem] w-full shrink-0 items-center justify-center gap-2 rounded-full border border-[#FFB8B8] bg-[#FFF5F5] px-6 text-base font-black text-[#D92D20] shadow-[0_12px_32px_rgba(217,45,32,0.08)] transition hover:bg-white focus:outline-none focus:ring-2 focus:ring-[#D92D20]/30 focus:ring-offset-2 sm:min-h-14 sm:w-auto sm:px-8 sm:text-lg"
              onClick={() => window.location.reload()}
              type="button"
            >
              <span className="grid h-5 w-5 place-items-center rounded-full border-2 border-current text-[10px]">□</span>
              Parar
            </button>
          ) : (
            <button
              className="interactive-hit custom-diagnostic-submit inline-flex min-h-[3.25rem] w-full shrink-0 items-center justify-center rounded-full border border-[#E7E2D9] bg-white px-6 text-base font-black text-[#101B3A] shadow-[0_12px_32px_rgba(16,27,58,0.08)] transition hover:border-[#0E8F7E]/30 hover:bg-[#FFFDF8] focus:outline-none focus:ring-2 focus:ring-[#0E8F7E] focus:ring-offset-2 disabled:cursor-not-allowed disabled:border-[#E2DED5] disabled:bg-[#F5F0E8] disabled:text-[#858B98] disabled:shadow-none disabled:hover:border-[#E2DED5] disabled:hover:bg-[#F5F0E8] sm:min-h-14 sm:w-auto sm:px-8 sm:text-lg"
              disabled={submitDisabled}
              type="submit"
            >
              <span>{submitLabel ?? "Gerar diagnóstico"}</span>
              {submitDisabled ? null : <ArrowIcon className="ml-2 h-4 w-4" />}
            </button>
          )}
        </div>
      </form>

      {pending ? (
        <div className="custom-diagnostic-loading mt-6 rounded-[24px] border border-[#F0D7B4] bg-white p-5 text-left shadow-[0_18px_48px_rgba(16,27,58,0.10)] sm:mt-7 sm:p-7">
          <div className="custom-diagnostic-loading-bar" />
          <div className="flex items-start justify-between gap-4">
            <div className="flex min-w-0 items-center gap-3">
              <span className="custom-diagnostic-spinner h-9 w-9 shrink-0 rounded-full border border-[#EEF1F5]" />
              <p className="custom-diagnostic-loading-title text-base font-black leading-6 sm:text-2xl">{loadingSteps[0]}</p>
            </div>
            <span className="custom-diagnostic-loading-percent text-sm font-black text-[#101B3A]">24%</span>
          </div>
          <div className="mt-7 grid gap-3 sm:gap-4">
            {loadingSteps.map((step, index) => (
              <div className="custom-diagnostic-skeleton" key={step} style={{ animationDelay: `${index * 120}ms`, width: `${92 - index * 8}%` }} />
            ))}
            <div className="custom-diagnostic-skeleton w-[58%]" />
          </div>
        </div>
      ) : null}
    </div>
  );
}

function DiagnosticReport({
  onCta,
  report,
}: {
  onCta: (cta: CustomAgentDiagnosticResponse["ctas"][number]) => void;
  report: CustomAgentDiagnosticResponse;
}) {
  const primaryCta = report.ctas[0];
  const secondaryCtas = report.ctas.slice(1, 3);
  const [visibleStep, setVisibleStep] = useState(0);
  const reportSections = report.sections.slice(0, 3);
  const ctasVisible = visibleStep > reportSections.length;

  return (
    <div className="custom-diagnostic-report mx-auto mt-6 max-w-5xl rounded-[26px] border border-[#F0D7B4] bg-white p-5 text-left shadow-[0_20px_52px_rgba(16,27,58,0.10)] sm:p-7">
      <div className="custom-diagnostic-report-accent" />
      <div className="flex items-start gap-3 sm:gap-4">
        <span className="mt-1 grid h-9 w-9 shrink-0 place-items-center rounded-full bg-[#F0F3DF] text-xs font-black text-[#6E7F2C] sm:h-10 sm:w-10">T</span>
        <div className="min-w-0 flex-1 text-base font-semibold leading-7 text-[#101B3A] sm:text-xl sm:leading-9">
          <TypewriterText
            onDone={() => setVisibleStep((current) => Math.max(current, 1))}
            text={`${classificationLabel(report.classification)}. ${report.title}`}
          />
        </div>
      </div>

      <div className="mt-7 grid gap-6 sm:mt-8 sm:gap-7">
        {reportSections.map((section, index) =>
          visibleStep > index ? (
            <article className="custom-diagnostic-written-block flex items-start gap-3 sm:gap-4" key={section.id}>
              <span className="mt-1 grid h-9 w-9 shrink-0 place-items-center rounded-full bg-[#FBF8F2] text-sm font-black text-[#101B3A] ring-1 ring-[#EFE8DC] sm:h-10 sm:w-10">
                {index + 1}
              </span>
              <div className="min-w-0">
                <h4 className="text-base font-black leading-7 text-[#101B3A] sm:text-lg">{section.title}</h4>
                <p className="mt-2 text-sm font-semibold leading-7 text-[#101B3A] sm:mt-3 sm:text-lg sm:leading-8">
                  <TypewriterText
                    onDone={() => setVisibleStep((current) => Math.max(current, index + 2))}
                    speedMs={9}
                    text={section.body}
                  />
                </p>
              </div>
            </article>
          ) : null,
        )}
      </div>

      {ctasVisible ? (
        <div className="custom-diagnostic-ctas mt-8 flex flex-col gap-2 sm:flex-row">
          {primaryCta ? (
            <button
              className="interactive-hit inline-flex min-h-12 flex-[1.3] items-center justify-center rounded-full bg-[#101B3A] px-5 text-sm font-black text-white transition hover:bg-[#18264F] focus:outline-none focus:ring-4 focus:ring-[#FFB21A]/20"
              onClick={() => onCta(primaryCta)}
              type="button"
            >
              {primaryCta.label}
              <ArrowIcon className="ml-2 h-4 w-4" />
            </button>
          ) : null}
          {secondaryCtas.map((cta) => (
            <button
              className="interactive-hit inline-flex min-h-12 flex-1 items-center justify-center rounded-full border border-[#E7E2D9] bg-white px-4 text-sm font-black text-[#101B3A] transition hover:border-[#6E7F2C]/35 hover:bg-[#FFFDF8] focus:outline-none focus:ring-4 focus:ring-[#FFB21A]/20"
              key={`${cta.id}-${cta.contextVariant}`}
              onClick={() => onCta(cta)}
              type="button"
            >
              {cta.label}
            </button>
          ))}
        </div>
      ) : null}
    </div>
  );
}

function TypewriterText({
  onDone,
  speedMs = 7,
  text,
}: {
  onDone: () => void;
  speedMs?: number;
  text: string;
}) {
  const [visibleChars, setVisibleChars] = useState(0);
  const doneRef = useRef(false);

  useEffect(() => {
    if (visibleChars >= text.length) {
      if (!doneRef.current) {
        doneRef.current = true;
        window.setTimeout(onDone, 180);
      }
      return;
    }

    const timer = window.setTimeout(() => {
      setVisibleChars((current) => Math.min(text.length, current + 3));
    }, speedMs);

    return () => window.clearTimeout(timer);
  }, [onDone, speedMs, text, visibleChars]);

  return (
    <>
      {text.slice(0, visibleChars)}
      {visibleChars < text.length ? <span className="custom-diagnostic-cursor" aria-hidden="true" /> : null}
    </>
  );
}

function ArrowIcon({ className = "" }: { className?: string }) {
  return (
    <svg aria-hidden="true" className={className} fill="none" viewBox="0 0 20 20">
      <path d="M4 10h12M11 5l5 5-5 5" stroke="currentColor" strokeLinecap="round" strokeLinejoin="round" strokeWidth="2.2" />
    </svg>
  );
}

function classificationLabel(classification: CustomAgentDiagnosticResponse["classification"]) {
  if (classification === "custom_agent") return "Rotina sob medida";
  if (classification === "mixed_solution") return "Taliya + sob medida";
  if (classification === "unclear") return "Precisa de contexto";
  return "Taliya já atende";
}

function messageForVariant(contextVariant: string, report: CustomAgentDiagnosticResponse) {
  if (contextVariant === "diagnostic_custom_agent") {
    return `Vi meu diagnóstico (${report.reportId}) e quero explicar melhor a operação para uma proposta de rotina sob medida.`;
  }
  if (contextVariant === "diagnostic_mixed_solution") {
    return `Vi meu diagnóstico (${report.reportId}). Quero entender o plano Taliya e a parte sob medida.`;
  }
  if (contextVariant === "diagnostic_existing_solution") {
    return `Vi meu diagnóstico (${report.reportId}) e parece que a Taliya já cobre esse caminho. Quero entender o melhor plano.`;
  }
  return `Vi meu diagnóstico (${report.reportId}) e quero explicar melhor minha operação.`;
}

function withWhatsAppMessage(href: string, message: string) {
  if (!href.includes("wa.me")) return href;

  const [base] = href.split("?");
  return `${base}?text=${encodeURIComponent(message)}`;
}
