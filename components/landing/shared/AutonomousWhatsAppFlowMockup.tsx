"use client";

import { useEffect, useMemo, useRef, useState } from "react";
import Image from "next/image";
import { BatteryFull, Camera, CheckCheck, ChevronLeft, Mic, Phone, Plus, Signal, Sticker, Video, Wifi } from "lucide-react";

import styles from "./IntentWhatsAppMockup.module.css";

import { agentVisualTokens } from "@/data/landing/agentVisuals";
import type { AutonomousFlowMockup, AutonomousFlowStep } from "@/data/landing/niches/types";

const STEP_REVEAL_INTERVAL_MS = 2000;

const stepBaseClass = styles.step;

function getStepClass(step: AutonomousFlowStep) {
  if (step.type === "process") {
    return "mx-auto flex max-w-[82%] items-center gap-2 rounded-full border border-[#E8D59D] bg-[#FFF8DF]/95 px-3 py-2 text-left text-[10px] font-black uppercase tracking-[0.10em] text-[#7A5600]";
  }

  if (step.type === "switch") {
    return "mx-auto max-w-[78%] rounded-full border border-white/70 bg-white/85 px-4 py-2 text-center text-[11px] font-black text-[#667085]";
  }

  if (step.type === "notification") {
    return "mx-auto max-w-[84%] rounded-2xl border border-[#CCE8DF] bg-[#ECFFF8]/95 px-4 py-3 text-xs font-bold leading-5 text-[#0B6F61]";
  }

  return `${styles.bubble} ${step.actor === "student" ? styles.incoming : styles.outgoing}`;
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
      {step.speaker ? <p className="sr-only">{step.speaker}</p> : null}
      {step.attachment ? (
        <div
          className={`mb-2 flex min-w-0 items-center gap-[0.7em] rounded-lg p-[0.7em] ${step.actor === "student" ? "bg-[#F0F2F3]" : "bg-[#C7EBC1]"}`}
          aria-label={`Arquivo anexado: ${step.attachment.name}, ${step.attachment.pages} ${step.attachment.pages === 1 ? "página" : "páginas"}, ${step.attachment.size}, ${step.attachment.format}`}
        >
          <span className="relative grid h-[3em] w-[2.25em] shrink-0 place-items-center rounded-sm border border-[#C9CDD0] bg-white" aria-hidden="true">
            <span className="absolute -right-px -top-px h-[0.75em] w-[0.75em] border-b border-l border-[#C9CDD0] bg-[#E4E7E9]" />
            <span className="relative mt-[1em] rounded-sm bg-[#E2574C] px-1 py-0.5 text-[0.65em] font-bold leading-none text-white">PDF</span>
          </span>
          <span className="min-w-0 flex-1">
            <span className="block break-words text-[1em] font-medium leading-tight text-[#111B21] [overflow-wrap:anywhere]">{step.attachment.name}</span>
            <span className="mt-1 block text-[0.8em] leading-tight text-[#667781]">
              {step.attachment.pages} {step.attachment.pages === 1 ? "página" : "páginas"} · {step.attachment.size} · {step.attachment.format}
            </span>
          </span>
          <span className="grid h-[2em] w-[2em] shrink-0 place-items-center rounded-full border border-[#8696A0] text-[#667781]" aria-hidden="true">
            <svg className="h-4 w-4" fill="none" stroke="currentColor" strokeLinecap="round" strokeLinejoin="round" strokeWidth="1.5" viewBox="0 0 24 24">
              <path d="M12 4v11m-4-4 4 4 4-4M5 17v3h14v-3" />
            </svg>
          </span>
        </div>
      ) : null}
      <WhatsAppFormattedText text={step.text} />
    </>
  );
}

function AutonomousWhatsAppFlowMockupContent({ flow }: { flow: AutonomousFlowMockup }) {
  const visual = agentVisualTokens[flow.agentId] ?? agentVisualTokens.atendimento;
  const phoneRef = useRef<HTMLDivElement>(null);
  const chatScrollRef = useRef<HTMLDivElement>(null);
  const [isVisible, setIsVisible] = useState(false);
  const [visibleSteps, setVisibleSteps] = useState(0);
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
    const phone = phoneRef.current;
    if (!phone) return;

    const observer = new IntersectionObserver(
      ([entry]) => setIsVisible(Boolean(entry?.isIntersecting && entry.intersectionRatio >= 0.15)),
      { rootMargin: "-80px 0px 0px 0px", threshold: 0.15 },
    );
    observer.observe(phone);
    return () => observer.disconnect();
  }, []);

  useEffect(() => {
    if (!isVisible || visibleSteps >= flow.steps.length) return;
    const prefersReducedMotion = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
    if (prefersReducedMotion) {
      const timeout = window.setTimeout(() => setVisibleSteps(flow.steps.length), 0);
      return () => window.clearTimeout(timeout);
    }
    const timeout = window.setTimeout(() => {
      setVisibleSteps((current) => Math.min(current + 1, flow.steps.length));
    }, visibleSteps === 0 ? 0 : STEP_REVEAL_INTERVAL_MS);

    return () => window.clearTimeout(timeout);
  }, [flow.steps.length, isVisible, visibleSteps]);

  useEffect(() => {
    if (!isVisible || visibleSteps === 0) return;
    const chatScroll = chatScrollRef.current;
    if (!chatScroll) return;
    const prefersReducedMotion = window.matchMedia("(prefers-reduced-motion: reduce)").matches;

    chatScroll.scrollTo({
      top: chatScroll.scrollHeight,
      behavior: prefersReducedMotion ? "auto" : "smooth",
    });
  }, [isVisible, visibleSteps, flow.title]);

  return (
    <div ref={phoneRef} className={styles.phone} aria-label="Demonstração de conversa no WhatsApp em um iPhone">
      <div className={styles.frame}>
        <div className={styles.screen}>
          <div className={styles.island} aria-hidden="true"><span /></div>
          <div className={styles.statusbar} aria-hidden="true">
            <span>9:41</span>
            <span className={styles.statusIcons}><Signal /><Wifi /><BatteryFull /></span>
          </div>

          <div className={styles.header}>
            <ChevronLeft className={styles.back} aria-hidden="true" />
            <div className={styles.avatar} style={{ color: visual.accent }}>
              {activeAvatar ? (
                <Image alt="" className="h-full w-full object-cover" height={40} src={activeAvatar} width={40} />
              ) : (
                contactInitials
              )}
            </div>
            <div className={styles.contact}>
              <p>{activeContactName}</p>
              <p>{flow.status}</p>
            </div>
            <Video className={styles.headerIcon} aria-hidden="true" />
            <Phone className={styles.headerIcon} aria-hidden="true" />
          </div>

          <div
            ref={chatScrollRef}
            className={styles.chat}
            key={flow.title}
            role="region"
            aria-label={`Conversa de ${flow.title}. Role para rever as mensagens.`}
            tabIndex={0}
          >
            <div className={styles.date}>Hoje</div>
            {visibleFlowSteps.map((step, index) => (
              <div
                className={`${stepBaseClass} ${getStepClass(step)}`}
                key={`${flow.title}-${index}-${step.type}`}
              >
                <StepContent step={step} />
                {step.type === "message" ? (
                  <div className={styles.messageMeta}>
                    <span>14:{String(31 + index).padStart(2, "0")}</span>
                    {step.actor === "agent" ? <CheckCheck aria-hidden="true" /> : null}
                  </div>
                ) : null}
              </div>
            ))}

            {isVisible && visibleSteps < flow.steps.length ? (
              <div className={`typing-pill ${styles.typing}`} aria-label="Preparando a próxima mensagem">
                <span /><span /><span />
              </div>
            ) : null}
          </div>

          <div className={styles.composer} aria-hidden="true">
            <Plus />
            <div className={styles.field}><span>Mensagem</span><Sticker /></div>
            <Camera /><Mic />
          </div>
          <div className={styles.homebar} aria-hidden="true"><span /></div>
        </div>
      </div>
    </div>
  );
}

export function AutonomousWhatsAppFlowMockup({ flow }: { flow: AutonomousFlowMockup }) {
  return <AutonomousWhatsAppFlowMockupContent key={flow.title} flow={flow} />;
}
