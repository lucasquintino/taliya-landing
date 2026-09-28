import type { CalculatorDefaults, NicheLandingConfig } from "@/data/landing/niches/types";
import type { MoneyCalculatorResult } from "@/lib/landing/money-calculator";
import type { PricingPlan } from "@/data/landing/niches/types";
import { MoneyPanelMockup, type MoneyControl } from "../shared/MoneyPanelMockup";
import { SectionShell } from "../shared/SectionShell";
import { SectionIntro } from "../shared/SectionIntro";

const controls: MoneyControl[] = [
  { key: "activeStudents", label: "Alunos ativos no studio", min: 10, max: 400, step: 5, group: "Tamanho do studio" },
  { key: "averageMonthlyFee", label: "Mensalidade média por aluno", min: 80, max: 900, step: 10, prefix: "R$ ", group: "Valor médio" },
];
const revealDelayClasses = ["reveal-delay-1", "reveal-delay-2", "reveal-delay-3", "reveal-delay-4", "reveal-delay-5", "reveal-delay-6"];

function CalculatorControl({
  control,
  onChange,
  rangeFill,
  value,
  visualDelay,
}: {
  control: MoneyControl;
  onChange: (key: keyof CalculatorDefaults, value: number) => void;
  rangeFill: { background: string };
  value: number;
  visualDelay: string;
}) {
  return (
    <label className={`reveal-step grid gap-2 rounded-2xl border border-[#EFE7DA] bg-[#FFFDF8] p-3.5 ${visualDelay}`}>
      <span className="flex items-start justify-between gap-3">
        <span className="min-w-0">
          <span className="block text-[0.63rem] font-black uppercase tracking-[0.16em] text-[#98A2B3]">{control.group}</span>
          <span className="mt-1 block text-sm font-black leading-tight text-[#101B3A]">{control.label}</span>
        </span>
        <span className="shrink-0 text-xl font-black tracking-[-0.04em] text-[#0E8F7E]">
          {control.prefix}{value}{control.suffix}
        </span>
      </span>
      <input
        aria-label={control.label}
        className="money-range h-2 w-full"
        max={control.max}
        min={control.min}
        onChange={(event) => onChange(control.key, Number(event.target.value))}
        step={control.step}
        style={rangeFill}
        type="range"
        value={value}
      />
      <span className="flex justify-between text-[0.7rem] font-bold text-[#667085]">
        <span>{control.prefix}{control.min}{control.suffix}</span>
        <span>{control.prefix}{control.max}+{control.suffix}</span>
      </span>
    </label>
  );
}

export function MoneyCalculatorSection({
  config,
  context = "landing",
  plans,
  values,
  result,
  onChange,
  onCta,
}: {
  config: NicheLandingConfig;
  context?: "landing" | "plans";
  plans?: PricingPlan[];
  values: CalculatorDefaults;
  result: MoneyCalculatorResult;
  onChange: (key: keyof CalculatorDefaults, value: number) => void;
  onCta: (label: string, href: string) => void;
}) {
  function rangeFill(control: MoneyControl) {
    const value = values[control.key];
    const percentage = ((value - control.min) / (control.max - control.min)) * 100;
    return {
      background: `linear-gradient(90deg, #0E8F7E 0%, #0E8F7E ${percentage}%, #DED8CE ${percentage}%, #DED8CE 100%)`,
    };
  }

  return (
    <SectionShell id="dinheiro-na-mesa" tone="plain" className="scroll-mt-24 landing-take-section landing-roomy-section money-calculator-section">
      <div className="reveal-step money-calculator-title mb-10 lg:mb-16">
        <SectionIntro align="center" eyebrow={config.calculator.eyebrow} title={config.calculator.title} subtitle={config.calculator.subtitle} />
      </div>
      <div className="money-calculator-layout mx-auto grid gap-6 lg:items-stretch">
        <div className="reveal-step reveal-delay-1 flex h-full flex-col rounded-3xl border border-[#E2DED5] bg-white/88 p-5 shadow-[0_18px_48px_rgba(16,27,58,0.06)] sm:p-6">
          <div className="money-control-piece mb-6 border-b border-[#ECE6DB] pb-4">
            <p className="text-[10px] font-black uppercase tracking-[0.22em] text-[#98A2B3]">Dados do studio</p>
          </div>
          <div className="money-controls-stack grid gap-4 sm:gap-5 lg:gap-5 xl:gap-6">
            {controls.map((control, index) => (
              <CalculatorControl control={control} key={control.key} onChange={onChange} rangeFill={rangeFill(control)} value={values[control.key]} visualDelay={revealDelayClasses[index] ?? "reveal-delay-6"} />
            ))}
          </div>
          <div className="money-control-note money-control-piece mt-auto rounded-2xl bg-[#F5F0E8] px-4 py-4">
            <div>
              <p className="text-[0.68rem] font-black uppercase tracking-[0.18em] text-[#98A2B3]">O que entra na conta</p>
              <p className="mt-1 text-sm font-bold leading-5 text-[#475467]">A conta considera cinco vazamentos comuns.</p>
            </div>
            <div className="mt-3 grid gap-1.5">
              {[
                "Interessados sem próximo passo.",
                "Mensalidades, atrasos e renovações.",
                "Alunos sumindo antes de cancelar.",
                "Faltas, reposições e horários vazios.",
                "Tempo da equipe preso em mensagens e conferências.",
              ].map((item) => (
                <p className="flex gap-2 text-xs font-black leading-4 text-[#667085]" key={item}>
                  <span className="mt-1 h-1.5 w-1.5 shrink-0 rounded-full bg-[#0E8F7E]" />
                  <span>{item}</span>
                </p>
              ))}
            </div>
          </div>
        </div>
        <div className="reveal-step reveal-delay-3 h-full min-w-0">
          <MoneyPanelMockup
            context={context}
            ctaHref={config.calculator.cta.href}
            onCta={() => onCta(config.calculator.cta.label, config.calculator.cta.href)}
            plans={plans}
            result={result}
            values={values}
          />
        </div>
      </div>
    </SectionShell>
  );
}
