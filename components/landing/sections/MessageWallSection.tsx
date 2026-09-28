"use client";

import messageWall from "@/data/landing/message-wall.json";
import { SectionIntro } from "../shared/SectionIntro";
import { SectionShell } from "../shared/SectionShell";

const agentIdByCategory: Record<string, string> = {
  CL: "atendimento",
  SV: "vendas",
  AG: "agenda",
  OR: "vendas",
  RC: "financeiro",
  LE: "retencao",
  AR: "historico-evolucao",
};

const categoryLabel: Record<string, string> = {
  CL: "clientes",
  SV: "serviços",
  AG: "agenda",
  OR: "orçamentos",
  RC: "recebimentos",
  LE: "lembretes",
  AR: "documentos",
};

const messageById = new Map(messageWall.messages.map((message) => [message.id, message] as const));
const initialMessages = messageWall.initialIds.flatMap((id) => {
  const message = messageById.get(id);
  return message ? [message] : [];
});
const messagesPerTrack = 8;
const messageTracks = Array.from(
  { length: Math.ceil(initialMessages.length / messagesPerTrack) },
  (_, index) => initialMessages.slice(index * messagesPerTrack, (index + 1) * messagesPerTrack),
);

export function MessageWallSection({
  onSelectAgent,
}: {
  onSelectAgent: (agentId: string) => void;
}) {
  return (
    <SectionShell id="fale-do-seu-jeito" tone="white" className="landing-take-section" contentClassName="py-2">
      <div className="grid gap-7 lg:gap-9">
        <div className="landing-one-line-title reveal-step mx-auto max-w-4xl">
          <SectionIntro
            align="center"
            eyebrow="Exemplos do dia a dia"
            title={messageWall.title}
            subtitle=""
          />
        </div>

        <div className="message-wall grid gap-3" aria-label="Exemplos de mensagens para a Taliya" role="group">
          {messageTracks.map((track, trackIndex) => (
            <div className="message-wall-row overflow-hidden py-1" key={`track-${trackIndex}`}>
              <div className={`message-wall-track flex w-max ${trackIndex % 2 === 1 ? "message-wall-track--reverse" : ""}`}>
                <div className="flex shrink-0 gap-3 pr-3">
                  {track.map((message) => {
                    const label = categoryLabel[message.category] ?? "rotina";
                    const agentId = agentIdByCategory[message.category] ?? "atendimento";

                    return (
                      <a
                        aria-label={`Ver ${label}: ${message.text}`}
                        className="whatsapp-bubble-user relative flex min-h-12 w-max flex-none items-center whitespace-nowrap rounded-[1rem] rounded-br-[0.25rem] border border-[#C2E6B9] bg-[#D9FDD3] px-4 py-2 text-left text-xs font-semibold leading-5 text-[#111B21] shadow-sm transition-colors hover:bg-[#CFF4C7] focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-[#0E8F7E]"
                        data-target-subtype={message.targetSubtype}
                        href="#agentes"
                        key={message.id}
                        onClick={() => onSelectAgent(agentId)}
                      >
                        {message.text}
                      </a>
                    );
                  })}
                </div>

                <div aria-hidden="true" className="flex shrink-0 gap-3 pr-3">
                  {track.map((message) => (
                    <a
                      aria-label={`Ver ${categoryLabel[message.category] ?? "rotina"}: ${message.text}`}
                      className="whatsapp-bubble-user relative flex min-h-12 w-max flex-none items-center whitespace-nowrap rounded-[1rem] rounded-br-[0.25rem] border border-[#C2E6B9] bg-[#D9FDD3] px-4 py-2 text-left text-xs font-semibold leading-5 text-[#111B21] shadow-sm transition-colors hover:bg-[#CFF4C7]"
                      data-target-subtype={message.targetSubtype}
                      href="#agentes"
                      key={message.id}
                      onClick={() => onSelectAgent(agentIdByCategory[message.category] ?? "atendimento")}
                      tabIndex={-1}
                    >
                      {message.text}
                    </a>
                  ))}
                </div>
              </div>
            </div>
          ))}
        </div>
      </div>
    </SectionShell>
  );
}
