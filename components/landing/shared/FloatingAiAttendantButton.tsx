import Image from "next/image";
import type { FloatingAgentConfig } from "@/data/landing/niches/types";

export function FloatingAiAttendantButton({
  config,
  attention = false,
  mobileOnly = false,
  mode = "idle",
  settled = true,
  onClick,
}: {
  attention?: boolean;
  compact?: boolean;
  config: FloatingAgentConfig;
  mobileOnly?: boolean;
  mode?: "idle" | "attention" | "active";
  settled?: boolean;
  onClick: () => void;
}) {
  const isActive = mode === "active";
  const isAttention = mode === "attention" || attention;
  const showBadge = isAttention;
  const headline = isActive ? "Continuar atendimento" : "Falar com consultor";
  const subline = isActive ? "Sua conversa está salva" : "Tire dúvidas sobre a Taliya";

  return (
    <button
      aria-label="Abrir atendimento"
      className={`floating-ai-attendant-button interactive-hit group fixed z-50 flex cursor-pointer items-center overflow-hidden rounded-full border border-[#E5DED2] bg-white/95 text-left text-[#101B3A] shadow-[0_22px_60px_rgba(16,27,58,0.16)] backdrop-blur transition hover:-translate-y-0.5 hover:border-[#6E7F2C]/55 hover:shadow-[0_26px_72px_rgba(16,27,58,0.20)] focus:outline-none focus:ring-4 focus:ring-[#FFB21A]/25 ${
        mobileOnly
          ? "bottom-4 right-4 h-[4.25rem] w-[4.25rem] justify-center gap-0 overflow-visible p-1.5"
          : "bottom-6 right-6 h-[4.625rem] w-[21.75rem] max-w-[calc(100vw-2rem)] gap-3 rounded-[1.7rem] py-2 pl-2 pr-3"
      }`}
      data-attention={attention ? "true" : "false"}
      data-mobile-only={mobileOnly ? "true" : "false"}
      data-mode={mode}
      data-settled={settled ? "true" : "false"}
      onClick={onClick}
      type="button"
    >
      {mobileOnly ? (
        <MessageIcon className="floating-ai-attendant-mobile-icon h-6 w-6" />
      ) : (
        <>
          <span className="floating-ai-attendant-avatar relative grid h-14 w-14 shrink-0 place-items-center">
            <span className="floating-ai-attendant-avatar-frame relative block h-full w-full overflow-hidden rounded-full bg-[#F0F3DF] ring-2 ring-[#6E7F2C]/18">
              <Image alt={config.avatar.alt} className="h-full w-full object-cover" height={56} priority sizes="56px" src={config.avatar.src} unoptimized width={56} />
            </span>
            <span aria-hidden="true" className="floating-ai-attendant-online absolute bottom-1 right-1 z-10 h-3.5 w-3.5 rounded-full border-2 border-white bg-[#6E7F2C] shadow-[0_2px_6px_rgba(16,27,58,0.18)]" />
            {isAttention ? <span className="floating-ai-attendant-pulse absolute inset-0 rounded-full ring-2 ring-[#FFB21A]/45" /> : null}
          </span>
          <span className="floating-ai-attendant-copy min-w-[196px] pr-1">
            <span className="block whitespace-nowrap text-base font-black leading-5">{headline}</span>
            <span className="mt-0.5 block text-sm font-bold leading-4 text-[#667085]">
              <span className="truncate">{subline}</span>
            </span>
          </span>
          <span aria-hidden="true" className="floating-ai-attendant-action relative grid h-14 w-14 shrink-0 place-items-center overflow-hidden rounded-full bg-[#101B3A] text-white shadow-[0_10px_22px_rgba(16,27,58,0.18)] transition group-hover:scale-105">
            {isAttention ? <span className="floating-ai-attendant-ripple absolute inset-0 rounded-full" /> : null}
            <MessageIcon className="h-5 w-5" />
          </span>
        </>
      )}
      {showBadge ? (
        <span
          aria-hidden="true"
          className={`floating-ai-attendant-badge absolute grid h-6 min-w-6 place-items-center rounded-full bg-[#FFB21A] px-1.5 text-[11px] font-black text-[#101B3A] shadow-[0_8px_18px_rgba(16,27,58,0.18)] ${mobileOnly ? "-right-1 -top-1" : "right-1.5 top-1.5"}`}
        >
          1
        </span>
      ) : null}
    </button>
  );
}

function MessageIcon({ className = "" }: { className?: string }) {
  return (
    <svg aria-hidden="true" className={className} fill="none" viewBox="0 0 24 24">
      <path d="M5 6.5h14v8.8H9.4L5 18.5v-12Z" stroke="currentColor" strokeLinejoin="round" strokeWidth="2" />
    </svg>
  );
}
