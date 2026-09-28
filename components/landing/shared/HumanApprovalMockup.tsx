import type { HumanControlMode } from "@/data/landing/niches/types";
import { WhatsAppConversationMockup } from "./WhatsAppConversationMockup";

export function HumanApprovalMockup({ mode }: { mode: HumanControlMode }) {
  return (
    <div className="grid gap-5 lg:grid-cols-[1fr_0.85fr] lg:items-center">
      <WhatsAppConversationMockup conversation={mode.conversation} />
      <div className="rounded-[2rem] border border-[#E2DED5] bg-white p-5 shadow-[0_24px_70px_rgba(16,27,58,0.10)]">
        <p className="text-xs font-black uppercase tracking-[0.22em] text-[#D96B5F]">{mode.label}</p>
        <h3 className="mt-3 text-3xl font-black tracking-[-0.05em] text-[#101B3A]">{mode.title}</h3>
        <p className="mt-3 text-sm leading-6 text-[#667085]">{mode.description}</p>
        <div className="mt-5 grid gap-3">
          {mode.actions.map((item) => (
            <button className="interactive-hit rounded-2xl border border-[#E2DED5] bg-[#FBF8F2] px-4 py-4 text-left text-sm font-black text-[#344054] focus:outline-none focus:ring-4 focus:ring-[#0E8F7E]/15" key={item} type="button">
              {item}
            </button>
          ))}
        </div>
      </div>
    </div>
  );
}
