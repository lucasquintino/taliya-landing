import { BrowserFrame } from "./SaasPanelMockup";

export function StudentHistoryMockup() {
  return (
    <BrowserFrame title="Histórico do aluno">
      <div className="bg-[#FBF8F2] p-5 sm:p-6">
        <div className="rounded-[1.5rem] bg-white p-5 shadow-sm">
          <div className="flex items-center gap-4">
            <div className="grid h-14 w-14 place-items-center rounded-full bg-[#E9E5FF] text-lg font-black text-[#4937A8]">RL</div>
            <div>
              <h3 className="text-xl font-black text-[#101B3A]">Roberta Lima</h3>
              <p className="text-sm text-[#667085]">Aluno desde mar/2023</p>
            </div>
          </div>
          <div className="mt-5 grid gap-3 sm:grid-cols-3">
            <div className="rounded-2xl bg-[#FFF3E0] p-4"><p className="text-xs font-black text-[#B54708]">Restricao</p><p className="mt-2 font-bold text-[#101B3A]">Lombar sensível</p></div>
            <div className="rounded-2xl bg-[#E7F8F1] p-4"><p className="text-xs font-black text-[#087A61]">Objetivo</p><p className="mt-2 font-bold text-[#101B3A]">Mobilidade</p></div>
            <div className="rounded-2xl bg-[#EBE7FF] p-4"><p className="text-xs font-black text-[#4937A8]">Evolução</p><p className="mt-2 font-bold text-[#101B3A]">Mais constância</p></div>
          </div>
        </div>
      </div>
    </BrowserFrame>
  );
}
