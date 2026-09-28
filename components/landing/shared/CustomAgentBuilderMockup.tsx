import { BrowserFrame } from "./SaasPanelMockup";

export function CustomAgentBuilderMockup({ examples }: { examples: string[] }) {
  return (
    <BrowserFrame title="Rotina sob medida">
      <div className="bg-[#FBF8F2] p-5 sm:p-6">
        <div className="grid gap-4 lg:grid-cols-[0.8fr_1.2fr]">
          <div className="rounded-[1.5rem] bg-[#101B3A] p-5 text-white">
            <p className="text-xs font-black uppercase tracking-[0.2em] text-[#FFB21A]">Builder</p>
            <h3 className="mt-3 text-2xl font-black tracking-[-0.04em]">Descreva a rotina</h3>
            <div className="mt-5 rounded-2xl bg-white/10 p-4 text-sm text-white/72">Quando um aluno pos-cirurgico faltar, revisar restricoes, professor e retorno seguro.</div>
          </div>
          <div className="grid gap-3 sm:grid-cols-2">
            {examples.slice(0, 6).map((example) => (
              <div className="rounded-2xl border border-[#E2DED5] bg-white p-4 text-sm font-black text-[#344054]" key={example}>{example}</div>
            ))}
          </div>
        </div>
      </div>
    </BrowserFrame>
  );
}
