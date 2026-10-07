import type { PainOption } from "@/data/landing/niches/types";
import { agentVisualTokens } from "@/data/landing/agentVisuals";
import { SectionShell } from "../shared/SectionShell";
import { AutonomousWhatsAppFlowMockup } from "../shared/AutonomousWhatsAppFlowMockup";

export function IntentSelectorSection({
  pains,
  selectedPain,
  onSelectPain,
}: {
  pains: PainOption[];
  selectedPain: PainOption;
  onSelectPain: (painId: string) => void;
}) {
  const visiblePains = pains.filter((pain) => pain.autonomousFlow);
  const painPersonaMeta: Record<string, { agent: keyof typeof agentVisualTokens; icon: string; label: string }> = {
    resumos: { agent: "gestao", label: "Dia, semana e serviço", icon: "M4 18h16M7 15v-4M12 15V7M17 15v-6" },
    servicos: { agent: "atendimento", label: "Pacotes e sessões", icon: "M4 7h16v13H4zM7 4h10v3M8 11h8M8 15h5" },
    agenda: { agent: "agenda", label: "Marcar, remarcar e cancelar", icon: "M7 3v3M17 3v3M4.5 8h15M6 5h12a2 2 0 0 1 2 2v11a2 2 0 0 1-2 2H6a2 2 0 0 1-2-2V7a2 2 0 0 1 2-2ZM8.5 14l2 2 5-5" },
    listagens: { agent: "retencao", label: "Clientes e registros", icon: "M5 5h14v14H5zM8 9h8M8 13h8M8 17h5" },
    recebimentos: { agent: "financeiro", label: "Pagamentos e saldos", icon: "M7 8h10M7 12h10M9 16h6M5 5h14v14H5z" },
    documentos: { agent: "historico", label: "Documentos e materiais de trabalho", icon: "M7 3h7l5 5v13H7zM14 3v5h5M10 13h6M10 17h6" },
  };
  const selectedPersona = painPersonaMeta[selectedPain.id];
  const selectedVisual = selectedPersona ? agentVisualTokens[selectedPersona.agent] : agentVisualTokens.agenda;
  const selectedAccent = selectedVisual.accent;
  const selectedFlow = selectedPain.autonomousFlow ?? visiblePains[0]?.autonomousFlow;
  const statusDotColor = "#AEB7C2";

  return (
    <SectionShell id="intencoes" tone="white" className="landing-take-section intent-selector-section">
      <div className="intent-demo-card reveal-step w-full overflow-hidden rounded-[2.5rem] border border-[#E2DED5] bg-white shadow-[0_34px_90px_rgba(16,27,58,0.12)] lg:min-h-[82.5svh]">
        <div className="intent-demo-grid grid min-w-0 lg:min-h-[82.5svh] lg:grid-cols-[minmax(0,0.42fr)_minmax(0,0.58fr)]">
          <div className="flex min-w-0 flex-col border-b border-[#E9E4DA] p-5 sm:p-8 lg:border-b-0 lg:border-r">
            <div className="reveal-step reveal-delay-1 relative z-30 block">
              <p className="text-xl font-medium text-[#101B3A]" id="intent-pain-label">Quero que a Taliya cuide de</p>
              <details
                className="group relative z-30 mt-3 border-b-2 pb-2 open:z-50"
                style={{ borderColor: selectedAccent }}
              >
                <summary
                  aria-labelledby="intent-pain-label"
                  className="intent-selected-summary flex cursor-pointer list-none items-center justify-between gap-3 text-[clamp(1.55rem,7vw,3rem)] font-black leading-tight tracking-[-0.045em] outline-none marker:hidden focus:opacity-80 sm:gap-4 sm:leading-none sm:tracking-[-0.055em]"
                  style={{ color: selectedAccent }}
                >
                  <span className="intent-selected-label min-w-0 whitespace-nowrap">{selectedPain.chip}</span>
                  <span
                    aria-hidden="true"
                    className="mr-3 h-4 w-4 shrink-0 rotate-45 border-b-[3px] border-r-[3px] transition group-open:rotate-[225deg] sm:mr-5"
                    style={{ borderColor: selectedAccent }}
                  />
                </summary>
                <div className="absolute left-0 right-0 top-full z-50 mt-0 overflow-hidden border-x border-b border-[#ECE7DE] bg-white px-3 py-5 shadow-[0_14px_26px_rgba(16,27,58,0.12)]">
                  {visiblePains.map((pain) => {
                    const persona = painPersonaMeta[pain.id] ?? { agent: "agenda" as const, icon: "" };
                    const visual = agentVisualTokens[persona.agent];
                    return (
                      <button
                        className="flex w-full items-center justify-between gap-4 py-3 text-left text-[clamp(1.45rem,6.4vw,2.55rem)] font-black leading-tight tracking-[-0.045em] transition hover:translate-x-1 focus:outline-none focus:ring-4 focus:ring-[#FFB21A]/20 sm:gap-5 sm:leading-none sm:tracking-[-0.06em]"
                        key={pain.id}
                        onClick={(event) => {
                          onSelectPain(pain.id);
                          event.currentTarget.closest("details")?.removeAttribute("open");
                        }}
                        style={{ color: visual.accent }}
                        type="button"
                      >
                          <span className="min-w-0 break-words [overflow-wrap:anywhere]">{pain.chip}</span>
                      </button>
                    );
                  })}
                </div>
              </details>
              <p className="mt-2 text-[0.66rem] font-black uppercase tracking-[0.16em] text-[#98A2B3]">Toque para trocar</p>
            </div>
            <div className="reveal-step reveal-delay-3 relative z-0 mt-4 hidden flex-1 flex-col justify-between gap-3 lg:flex">
              {visiblePains.map((pain) => {
                const selected = pain.id === selectedPain.id;
                const persona = painPersonaMeta[pain.id] ?? {
                    agent: "agenda",
                    icon: "M12 5v14M5 12h14",
                    label: "Rotina",
                };
                const visual = agentVisualTokens[persona.agent];
                return (
                  <button
                    className={`intent-pain-option group flex min-h-[4.85rem] w-full flex-1 items-center gap-4 rounded-[1.2rem] border px-5 py-3 text-left transition duration-200 focus:outline-none focus:ring-4 focus:ring-[#FFB21A]/20 ${
                      selected ? "is-active" : "border-transparent bg-white hover:bg-[#FBF8F2]"
                    }`}
                    key={pain.id}
                    onClick={() => onSelectPain(pain.id)}
                    style={{
                      backgroundColor: selected ? visual.activeBg : undefined,
                      borderColor: selected ? visual.accent : "transparent",
                      boxShadow: selected ? `0 8px 18px ${visual.accent}26` : undefined,
                    }}
                    type="button"
                  >
                    <span
                      className="grid h-12 w-12 shrink-0 place-items-center rounded-full transition group-hover:scale-105"
                      style={{ backgroundColor: visual.soft, color: visual.accent }}
                    >
                      <svg aria-hidden="true" className="h-6 w-6" fill="none" stroke="currentColor" strokeLinecap="round" strokeLinejoin="round" strokeWidth="2.15" viewBox="0 0 24 24">
                        <path d={persona.icon} />
                      </svg>
                    </span>
                    <span className="min-w-0 flex-1">
                      <span className="flex flex-wrap items-center gap-2">
                        <span className="block text-lg font-black tracking-[-0.03em] text-[#101B3A]">{pain.chip}</span>
                        <span
                          className="rounded-full px-3 py-1 text-xs font-semibold leading-none"
                          style={{ backgroundColor: visual.soft, color: visual.accent }}
                        >
                          {persona.label}
                        </span>
                      </span>
                      {selected ? <span className="mt-1 block text-sm leading-5 text-[#8A90A6]">{pain.result}</span> : null}
                    </span>
                    <span
                      className="h-5 w-5 shrink-0 rounded-full"
                      style={{
                        backgroundColor: selected ? visual.accent : statusDotColor,
                        opacity: selected ? 1 : 0.62,
                      }}
                    />
                  </button>
                );
              })}
            </div>
          </div>
          <div className="intent-phone-stage reveal-step reveal-delay-4 flex min-w-0 items-center justify-center overflow-hidden bg-[#F4F0FF] p-5 sm:p-8">
            <div className="intent-mockup-panel flex w-full min-w-0 justify-center" key={selectedPain.id}>
              {selectedFlow ? <AutonomousWhatsAppFlowMockup flow={selectedFlow} /> : null}
            </div>
          </div>
        </div>
      </div>
    </SectionShell>
  );
}
