"use client";

import { useEffect, useMemo, useRef, useState } from "react";
import Image from "next/image";

import { agentVisualTokens } from "@/data/landing/agentVisuals";
import type { AutonomousFlowMockup, AutonomousFlowStep } from "@/data/landing/niches/types";

const STEP_REVEAL_INTERVAL_MS = 2000;

const stepBaseClass = "chat-line relative break-words [overflow-wrap:anywhere] shadow-sm";

function getStepClass(step: AutonomousFlowStep) {
  if (step.type === "process") {
    return "whatsapp-process-pill mx-auto flex max-w-[82%] items-center gap-2 rounded-full border border-[#E8D59D] bg-[#FFF8DF]/95 px-3 py-2 text-left text-[10px] font-black uppercase tracking-[0.10em] text-[#7A5600]";
  }

  if (step.type === "switch") {
    return "mx-auto max-w-[78%] rounded-full border border-white/70 bg-white/85 px-4 py-2 text-center text-[11px] font-black text-[#667085]";
  }

  if (step.type === "notification") {
    return "mx-auto max-w-[84%] rounded-2xl border border-[#CCE8DF] bg-[#ECFFF8]/95 px-4 py-3 text-xs font-bold leading-5 text-[#0B6F61]";
  }

  if (step.actor === "student") {
    return "whatsapp-bubble-agent mr-auto max-w-[82%] rounded-[1.05rem] rounded-bl-[0.28rem] bg-white px-3.5 py-2.5 text-[13px] font-medium leading-5 text-[#111B21]";
  }

  return "whatsapp-bubble-user ml-auto max-w-[82%] rounded-[1.05rem] rounded-br-[0.28rem] bg-[#D9FDD3] px-3.5 py-2.5 text-[13px] font-medium leading-5 text-[#111B21]";
}

function WhatsAppFormattedText({ text }: { text: string }) {
  return (
    <span className="whitespace-pre-line">
      {text.split(/(\*[^*\n]+\*)/g).map((part, index) => {
        const isBold = part.startsWith("*") && part.endsWith("*") && part.length > 2;
        return isBold ? <strong key={index}>{part.slice(1, -1)}</strong> : part;
      })}
    </span>
  );
}

function StepContent({ step }: { step: AutonomousFlowStep }) {
  if (step.type === "process") {
    return (
      <span className="flex min-w-0 items-center gap-2">
        <span className="grid h-6 w-7 shrink-0 place-items-center text-[#7A5600]">
          <svg aria-hidden="true" className="h-5 w-5" fill="currentColor" viewBox="0 0 24 24">
            <path d="M9.2 3.5c.2-.7 1.2-.7 1.4 0l1 3.3c.1.3.3.5.6.6l3.3 1c.7.2.7 1.2 0 1.4l-3.3 1c-.3.1-.5.3-.6.6l-1 3.3c-.2.7-1.2.7-1.4 0l-1-3.3c-.1-.3-.3-.5-.6-.6l-3.3-1c-.7-.2-.7-1.2 0-1.4l3.3-1c.3-.1.5-.3.6-.6l1-3.3Z" />
            <path d="M17.3 12.4c.2-.5.9-.5 1.1 0l.7 2.1c.1.2.2.4.4.4l2.1.7c.5.2.5.9 0 1.1l-2.1.7c-.2.1-.4.2-.4.4l-.7 2.1c-.2.5-.9.5-1.1 0l-.7-2.1c-.1-.2-.2-.4-.4-.4l-2.1-.7c-.5-.2-.5-.9 0-1.1l2.1-.7c.2-.1.4-.2.4-.4l.7-2.1Z" opacity="0.78" />
            <path d="M5.1 15.4c.1-.4.7-.4.8 0l.4 1.2c0 .2.2.3.3.3l1.2.4c.4.1.4.7 0 .8l-1.2.4c-.2 0-.3.2-.3.3L5.9 20c-.1.4-.7.4-.8 0l-.4-1.2c0-.2-.2-.3-.3-.3l-1.2-.4c-.4-.1-.4-.7 0-.8l1.2-.4c.2 0 .3-.2.3-.3l.4-1.2Z" opacity="0.55" />
          </svg>
        </span>
        <span className="min-w-0">{step.text}</span>
      </span>
    );
  }

  if (step.type === "switch") {
    return <span>{step.text}</span>;
  }

  if (step.type === "notification") {
    return (
      <>
        <p className="mb-1 text-[9px] font-black uppercase tracking-[0.14em] text-[#0E8F7E]">Responsável notificado</p>
        {step.text}
      </>
    );
  }

  return (
    <>
      {step.speaker ? <p className="mb-1 text-[10px] font-bold text-[#667781]">{step.speaker}</p> : null}
      <WhatsAppFormattedText text={step.text} />
    </>
  );
}

function AutonomousWhatsAppFlowMockupContent({ flow }: { flow: AutonomousFlowMockup }) {
  const visual = agentVisualTokens[flow.agentId] ?? agentVisualTokens.atendimento;
  const chatScrollRef = useRef<HTMLDivElement>(null);
  const [visibleSteps, setVisibleSteps] = useState(1);
  const visibleFlowSteps = useMemo(() => flow.steps.slice(0, visibleSteps), [flow.steps, visibleSteps]);
  const activeContactName = useMemo(() => {
    const latestSwitch = visibleFlowSteps.findLast((step) => step.type === "switch");
    if (!latestSwitch) return flow.contactName;
    const match = latestSwitch.text.match(/com\s+(.+)$/i);
    return match?.[1] ?? flow.contactName;
  }, [flow.contactName, visibleFlowSteps]);
  const contactInitials = activeContactName
    .split(" ")
    .filter(Boolean)
    .slice(0, 2)
    .map((part) => part[0]?.toUpperCase())
    .join("");
  const activeAvatar = flow.contactAvatars?.[activeContactName];

  useEffect(() => {
    const prefersReducedMotion = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
    if (prefersReducedMotion) {
      const timeout = window.setTimeout(() => setVisibleSteps(flow.steps.length), 0);
      return () => window.clearTimeout(timeout);
    }
    if (visibleSteps >= flow.steps.length) return;

    const timeout = window.setTimeout(() => {
      setVisibleSteps((current) => Math.min(current + 1, flow.steps.length));
    }, STEP_REVEAL_INTERVAL_MS);

    return () => window.clearTimeout(timeout);
  }, [flow.steps.length, visibleSteps]);

  useEffect(() => {
    const chatScroll = chatScrollRef.current;
    if (!chatScroll) return;
    const prefersReducedMotion = window.matchMedia("(prefers-reduced-motion: reduce)").matches;

    chatScroll.scrollTo({
      top: chatScroll.scrollHeight,
      behavior: prefersReducedMotion ? "auto" : "smooth",
    });
  }, [visibleSteps, flow.title]);

  return (
    <div className="autonomous-phone-mockup mockup-float relative mx-auto w-full max-w-[min(100%,390px)]">
      <div className="absolute -inset-8 rounded-[4rem] bg-[radial-gradient(circle_at_50%_12%,rgba(255,255,255,0.96),rgba(255,255,255,0)_58%)] blur-2xl" />
      <div className="autonomous-phone-frame relative rounded-[3.1rem] border border-black/20 bg-[#222] p-2 shadow-[0_34px_80px_rgba(16,27,58,0.28),0_8px_18px_rgba(16,27,58,0.16)]">
        <div className="autonomous-phone-screen relative overflow-hidden rounded-[2.55rem] border border-white/10 bg-[#0B141A]">
          <div className="autonomous-phone-notch absolute left-1/2 top-2 z-30 h-7 w-28 -translate-x-1/2 rounded-full bg-[#1D1F22] shadow-inner" />
          <div className="autonomous-phone-statusbar flex h-11 items-center justify-between bg-[#0B141A] px-7 pt-2 text-[11px] font-black text-white">
            <span>12:30</span>
            <span className="flex items-center gap-1.5">
              <span className="h-2 w-3 rounded-sm border border-white/70" />
              <span className="h-2 w-3 rounded-sm border border-white/70 bg-white/80" />
            </span>
          </div>

          <div className="autonomous-phone-header flex items-center gap-2 bg-[#075E54] px-3 py-2 text-white">
            <span className="autonomous-phone-back text-xl leading-none">&lt;</span>
            <div className="autonomous-phone-avatar grid h-9 w-9 shrink-0 place-items-center overflow-hidden rounded-full bg-white/95 text-[11px] font-black ring-2 ring-white/70" style={{ color: visual.accent }}>
              {activeAvatar ? (
                <Image alt="" className="h-full w-full object-cover" height={36} src={activeAvatar} width={36} />
              ) : (
                contactInitials
              )}
            </div>
            <div className="autonomous-phone-contact min-w-0 flex-1">
              <p className="truncate text-[13px] font-black">{activeContactName}</p>
              <p className="truncate text-[10px] text-white/75">{flow.status} via {flow.title}</p>
            </div>
            <span className="h-2 w-2 rounded-full bg-white/80" />
            <span className="h-2 w-2 rounded-full bg-white/80" />
          </div>

          <div
            ref={chatScrollRef}
            className="whatsapp-chat-bg relative h-[500px] space-y-2.5 overflow-y-auto p-3 scroll-smooth sm:h-[540px] lg:h-[430px] xl:h-[500px]"
            key={flow.title}
          >
            <div className="sticky top-0 z-10 mx-auto mb-2 w-fit rounded-full bg-[#D9EAF4]/90 px-3 py-1 text-[10px] font-bold text-[#5B6B73] backdrop-blur">HOJE</div>
            {visibleFlowSteps.map((step, index) => (
              <div
                className={`${stepBaseClass} ${getStepClass(step)}`}
                key={`${flow.title}-${index}-${step.type}`}
              >
                <StepContent step={step} />
                {step.type === "message" ? <p className="mt-1 text-right text-[10px] leading-none text-[#667781]">14:{String(31 + index).padStart(2, "0")}</p> : null}
              </div>
            ))}

            {visibleSteps < flow.steps.length ? (
              <div className="typing-pill mr-auto flex w-fit items-center rounded-[1.05rem] rounded-bl-[0.28rem] bg-white px-3.5 py-3 shadow-sm">
                <span />
                <span />
                <span />
              </div>
            ) : null}
          </div>

          <div className="autonomous-phone-input flex items-center gap-2 bg-[#F0E9DF] px-2.5 py-2.5">
            <div className="autonomous-phone-emoji grid h-8 w-8 place-items-center rounded-full bg-white text-xs font-black text-[#667781]">:)</div>
            <div className="autonomous-phone-field flex min-h-9 flex-1 items-center rounded-full bg-white px-3 text-[12px] font-semibold text-[#8696A0] shadow-inner">Mensagem</div>
            <div className="autonomous-phone-send grid h-9 w-9 place-items-center rounded-full text-white" style={{ backgroundColor: visual.accent }}>
              <span className="text-lg leading-none">&gt;</span>
            </div>
          </div>

          <div className="autonomous-phone-homebar flex h-6 items-center justify-center bg-[#F0E9DF]">
            <div className="h-1 w-28 rounded-full bg-black/80" />
          </div>
        </div>
      </div>
    </div>
  );
}

export function AutonomousWhatsAppFlowMockup({ flow }: { flow: AutonomousFlowMockup }) {
  return <AutonomousWhatsAppFlowMockupContent key={flow.title} flow={flow} />;
}
