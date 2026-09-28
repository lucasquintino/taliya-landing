import type { ConversationMockup as ConversationMockupData } from "@/data/landing/niches/types";

const lineClasses = {
  student: "ml-auto bg-[#DDF7C8] text-[#123023] rounded-br-md",
  agent: "mr-auto bg-white text-[#17233C] rounded-bl-md border border-[#E6E1D8]",
  system: "mx-auto bg-[#FFF5D6] text-[#6C4B00] rounded-2xl border border-[#F4D47B] text-center",
  owner: "ml-auto bg-[#E9E5FF] text-[#241A5B] rounded-br-md",
};

export function WhatsAppConversationMockup({
  conversation,
  compact = false,
}: {
  conversation: ConversationMockupData;
  compact?: boolean;
}) {
  return (
    <div className="mockup-float overflow-hidden rounded-[2rem] border border-[#D9E1D8] bg-[#101B3A] shadow-[0_28px_80px_rgba(16,27,58,0.18)]">
      <div className="flex items-center gap-3 border-b border-white/10 bg-[#17254B] px-4 py-3 text-white">
        <div className="grid h-10 w-10 place-items-center rounded-full bg-[#0E8F7E] text-xs font-black shadow-[0_0_0_6px_rgba(14,143,126,0.14)]">IA</div>
        <div className="min-w-0 flex-1">
          <p className="truncate text-sm font-black">{conversation.title}</p>
          <p className="truncate text-xs text-[#7BE0C8]">{conversation.status}</p>
        </div>
        <span className="online-dot h-2.5 w-2.5 rounded-full bg-[#7BE0C8]" />
      </div>
      <div className={`relative space-y-3 bg-[radial-gradient(circle_at_20%_20%,rgba(255,255,255,0.08),transparent_26%),linear-gradient(135deg,#ECE6DA_0%,#DAD4C8_100%)] p-4 ${compact ? "min-h-[270px]" : "min-h-[390px] sm:p-5"}`}>
        <div className="mx-auto mb-2 w-fit rounded-full bg-white/70 px-3 py-1 text-[11px] font-bold text-[#667085]">Hoje</div>
        {conversation.lines.map((line, index) => (
          <div
            className={`chat-line max-w-[88%] break-words [overflow-wrap:anywhere] rounded-2xl px-4 py-3 text-sm font-semibold leading-6 shadow-sm ${lineClasses[line.from]}`}
            key={`${line.from}-${index}-${line.text}`}
            style={{ animationDelay: `${index * 140}ms` }}
          >
            {line.label ? (
              <p className="mb-1 text-[10px] font-black uppercase tracking-[0.16em] opacity-70">{line.label}</p>
            ) : null}
            {line.text}
            <p className="mt-1 text-right text-[10px] opacity-45">14:{32 + index}</p>
          </div>
        ))}
        <div className="typing-pill mr-auto inline-flex rounded-full bg-white/80 px-3 py-2 shadow-sm" aria-hidden="true">
          <span />
          <span />
          <span />
        </div>
        {conversation.quickReplies?.length ? (
          <div className="flex flex-wrap gap-2 pt-1">
            {conversation.quickReplies.map((reply) => (
              <span className="interactive-hit rounded-full border border-[#0E8F7E]/35 bg-white/85 px-3 py-1.5 text-xs font-black text-[#0E8F7E]" key={reply}>
                {reply}
              </span>
            ))}
          </div>
        ) : null}
      </div>
      <div className="flex items-center gap-3 bg-[#F8F5EF] px-4 py-3">
        <div className="min-h-11 flex-1 rounded-full bg-white px-4 py-3 text-sm font-semibold text-[#98A2B3] shadow-inner">Mensagem sugerida...</div>
        <div className="interactive-hit grid h-11 w-11 place-items-center rounded-full bg-[#101B3A] font-black text-white">→</div>
      </div>
      <div className="border-t border-[#E6E1D8] bg-white px-4 py-3 text-sm font-black text-[#0E8F7E]">
        {conversation.result}
      </div>
    </div>
  );
}

export function ConversationMockup(props: { conversation: ConversationMockupData; compact?: boolean }) {
  return <WhatsAppConversationMockup {...props} />;
}
