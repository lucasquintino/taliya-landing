"use client";

import Image from "next/image";
import { useEffect, useRef } from "react";
import type { FloatingAgentConfig, PricingPlan, TrustedDestination } from "@/data/landing/niches/types";
import type { AiAttendantMessage, AiAttendantResponse } from "@/lib/landing/ai-attendant/schema";

export function FloatingAiAttendantPanel({
  config,
  input,
  messages,
  onClose,
  onInputChange,
  onQuickReply,
  onSuggestedInput,
  onSend,
  openingPending,
  pending,
  response,
  analysisDestination,
  humanWhatsAppDestination,
  subscriptionPlan,
}: {
  config: FloatingAgentConfig;
  input: string;
  messages: AiAttendantMessage[];
  onClose: () => void;
  onInputChange: (value: string) => void;
  onQuickReply: (quickReplyId: string, label: string) => void;
  onSuggestedInput: (value: string) => void;
  onSend: () => void;
  openingPending?: boolean;
  pending: boolean;
  response?: AiAttendantResponse;
  analysisDestination: TrustedDestination;
  humanWhatsAppDestination: TrustedDestination;
  subscriptionPlan?: PricingPlan;
}) {
  const isThinking = pending || Boolean(openingPending);
  const hasFallback = messages.some((message) => message.intent === "fallback");
  const panelTitle = config.label.includes("Taliya") ? config.label : `${config.label} Taliya`;
  const transcriptRef = useRef<HTMLDivElement | null>(null);
  const inputRef = useRef<HTMLTextAreaElement | null>(null);

  useEffect(() => {
    const isCoarsePointer = window.matchMedia("(pointer: coarse)").matches;
    if (isCoarsePointer) return;

    window.setTimeout(() => inputRef.current?.focus(), 120);
  }, []);

  useEffect(() => {
    const handleKeyDown = (event: KeyboardEvent) => {
      if (event.key === "Escape") onClose();
    };

    window.addEventListener("keydown", handleKeyDown);
    return () => window.removeEventListener("keydown", handleKeyDown);
  }, [onClose]);

  useEffect(() => {
    if (messages.length <= 1 && !isThinking && !response) return;

    const scrollToEnd = (behavior: ScrollBehavior) => {
      const transcript = transcriptRef.current;
      if (!transcript) return;
      transcript.scrollTo({
        top: transcript.scrollHeight,
        behavior,
      });
    };

    scrollToEnd("smooth");
    const frame = window.requestAnimationFrame(() => scrollToEnd("smooth"));
    const settleTimer = window.setTimeout(() => scrollToEnd("auto"), 220);

    return () => {
      window.cancelAnimationFrame(frame);
      window.clearTimeout(settleTimer);
    };
  }, [messages, isThinking, response]);

  useEffect(() => {
    const root = document.documentElement;
    const body = document.body;
    const visualViewport = window.visualViewport;
    let viewportFrame = 0;
    let restoreTimer = 0;
    const previousBodyOverflow = body.style.overflow;
    const previousBodyOverscrollBehavior = body.style.overscrollBehavior;

    root.setAttribute("data-floating-chat-open", "true");
    body.style.overflow = "hidden";
    body.style.overscrollBehavior = "none";

    const clearViewportVars = () => {
      root.style.removeProperty("--floating-chat-visual-height");
      root.style.removeProperty("--floating-chat-visual-offset-top");
      root.style.removeProperty("--floating-chat-keyboard-bottom");
      root.removeAttribute("data-floating-chat-keyboard");
    };

    const updateViewportVars = () => {
      if (!visualViewport || window.innerWidth >= 640) {
        clearViewportVars();
        return;
      }

      const layoutHeight = document.documentElement.clientHeight || window.innerHeight;
      const keyboardBottom = Math.max(0, window.innerHeight - visualViewport.height - visualViewport.offsetTop);
      const keyboardActive = keyboardBottom > 80 || visualViewport.height < layoutHeight - 90;

      if (!keyboardActive) {
        clearViewportVars();
        return;
      }

      root.style.setProperty("--floating-chat-visual-height", `${Math.round(visualViewport.height)}px`);
      root.style.setProperty("--floating-chat-visual-offset-top", `${Math.max(0, Math.round(visualViewport.offsetTop))}px`);
      root.style.setProperty("--floating-chat-keyboard-bottom", `${Math.round(keyboardBottom)}px`);

      root.setAttribute("data-floating-chat-keyboard", "true");
    };

    const scheduleViewportUpdate = () => {
      window.cancelAnimationFrame(viewportFrame);
      viewportFrame = window.requestAnimationFrame(updateViewportVars);
    };

    const scheduleRestoreCheck = () => {
      window.clearTimeout(restoreTimer);
      restoreTimer = window.setTimeout(scheduleViewportUpdate, 220);
    };

    updateViewportVars();
    window.addEventListener("resize", scheduleViewportUpdate);
    window.addEventListener("orientationchange", scheduleViewportUpdate);
    window.addEventListener("focusout", scheduleRestoreCheck);
    window.addEventListener("visibilitychange", scheduleRestoreCheck);
    visualViewport?.addEventListener("resize", scheduleViewportUpdate);
    visualViewport?.addEventListener("scroll", scheduleViewportUpdate);

    return () => {
      window.removeEventListener("resize", scheduleViewportUpdate);
      window.removeEventListener("orientationchange", scheduleViewportUpdate);
      window.removeEventListener("focusout", scheduleRestoreCheck);
      window.removeEventListener("visibilitychange", scheduleRestoreCheck);
      visualViewport?.removeEventListener("resize", scheduleViewportUpdate);
      visualViewport?.removeEventListener("scroll", scheduleViewportUpdate);
      window.cancelAnimationFrame(viewportFrame);
      window.clearTimeout(restoreTimer);
      clearViewportVars();
      root.removeAttribute("data-floating-chat-open");
      body.style.overflow = previousBodyOverflow;
      body.style.overscrollBehavior = previousBodyOverscrollBehavior;
    };
  }, []);

  function handleInputFocus() {
    window.setTimeout(() => {
      transcriptRef.current?.scrollTo({
        top: transcriptRef.current.scrollHeight,
        behavior: "smooth",
      });
    }, 180);
  }

  return (
    <section
      aria-label="Chat de atendimento"
      aria-modal="false"
      className="floating-chat-panel fixed inset-x-3 bottom-3 top-3 z-[80] flex flex-col overflow-hidden rounded-[2rem] border border-[#E5DED2] bg-white text-[#101B3A] shadow-[0_34px_90px_rgba(16,27,58,0.18)] sm:inset-x-auto sm:bottom-6 sm:right-6 sm:top-[4.3125rem] sm:w-[438px] sm:rounded-[2.35rem]"
      data-mode={isThinking ? "typing_loading" : hasFallback ? "error_fallback" : response?.conversionPath ? "handoff_cta" : "open"}
      role="dialog"
    >
      <header className="floating-chat-header relative overflow-hidden border-b border-[#E9E4DA] bg-[#FFFDF8] px-4 py-4 pr-20">
        <div className="flex items-center gap-3">
          <span className="relative grid h-14 w-14 shrink-0 place-items-center">
            <span className="relative block h-full w-full overflow-hidden rounded-full bg-[#F0F3DF] ring-2 ring-[#6E7F2C]/18">
              <Image alt={config.avatar.alt} className="h-full w-full object-cover" height={56} priority sizes="56px" src={config.avatar.src} unoptimized width={56} />
            </span>
            <span aria-hidden="true" className="absolute bottom-1 right-1 h-3.5 w-3.5 rounded-full border-2 border-[#FFFDF8] bg-[#6E7F2C] shadow-[0_2px_6px_rgba(16,27,58,0.18)]" />
          </span>
          <div className="min-w-0 flex-1">
            <div className="flex items-center gap-2">
              <h2 className="truncate text-base font-black leading-5 tracking-[-0.03em] text-[#101B3A]">{panelTitle}</h2>
              <span className="floating-online-badge rounded-full bg-[#F0F3DF] px-2.5 py-1 text-[10px] font-black uppercase tracking-[0.16em] text-[#6E7F2C]">
                ativo
              </span>
            </div>
            <p className="mt-1 truncate text-sm font-bold leading-4 text-[#667085]">
              {isThinking ? "Respondendo sua dúvida" : hasFallback ? "Conversa preservada" : config.availability}
            </p>
          </div>
          <button
            aria-label="Fechar chat"
            className="floating-chat-close interactive-hit absolute right-4 top-4 z-20 grid h-12 w-12 shrink-0 place-items-center rounded-full border border-[#E2DED5] bg-white text-[#101B3A] shadow-[0_8px_18px_rgba(16,27,58,0.08)] transition hover:bg-[#FBF8F2] focus:outline-none focus:ring-4 focus:ring-[#FFB21A]/20"
            onClick={onClose}
            type="button"
          >
            <CloseIcon className="h-5 w-5" />
          </button>
        </div>
      </header>

      <div aria-live="polite" className="floating-chat-transcript min-h-0 flex-1 overflow-y-auto bg-[#FBF8F2] px-4 py-4 overscroll-contain" ref={transcriptRef}>
        <div className="grid gap-3">
          {messages.map((message, index) => (
            <MessageBubble index={index} key={message.id} message={message} />
          ))}

          {isThinking ? (
            <div className="floating-typing mr-auto flex max-w-[86%] items-center gap-2 rounded-[1.35rem] border border-[#E5DED2] bg-white px-4 py-3 text-sm font-black text-[#667085] shadow-[0_10px_22px_rgba(16,27,58,0.06)]">
              <span className="floating-typing-dots flex gap-1" aria-hidden="true">
                <span className="h-1.5 w-1.5 rounded-full bg-[#6E7F2C]" />
                <span className="h-1.5 w-1.5 rounded-full bg-[#FFB21A]" />
                <span className="h-1.5 w-1.5 rounded-full bg-[#101B3A]" />
              </span>
              Digitando
            </div>
          ) : null}
        </div>

        {response?.recommendations?.length ? (
          <div className="floating-response-card mt-4 grid gap-3 rounded-[1.55rem] border border-[#E5DED2] bg-white p-4 shadow-[0_12px_30px_rgba(16,27,58,0.06)]">
            <p className="text-[11px] font-black uppercase tracking-[0.22em] text-[#6E7F2C]">Rotinas indicadas</p>
            {response.recommendations.map((recommendation) => (
              <div className="rounded-[1.2rem] bg-[#FBF8F2] p-3 text-sm leading-6 text-[#344054]" key={recommendation.painId}>
                <strong className="block text-[#101B3A]">{formatAgentNames(recommendation.agentIds, config.label === "Consultor")}</strong>
                <AgentRecommendationLine label="Dor" text={recommendation.painSummary ?? recommendation.nextQuestion} tone="pain" />
                <AgentRecommendationLine label="Por que" text={recommendation.explanation} />
                <AgentRecommendationLine label="Na prática" text={recommendation.exampleAction} muted />
              </div>
            ))}
          </div>
        ) : null}

        {hasFallback && !isThinking ? <FallbackActions config={config} onQuickReply={onQuickReply} /> : null}

        {response?.conversionPath ? (
          <ConversionActions
            analysisDestination={analysisDestination}
            config={config}
            humanWhatsAppDestination={humanWhatsAppDestination}
            response={response}
            subscriptionPlan={subscriptionPlan}
          />
        ) : null}

        {!response?.conversionPath && !isThinking ? (
          <NextBestAction config={config} messages={messages} onQuickReply={onQuickReply} onSuggestedInput={onSuggestedInput} response={response} />
        ) : null}
      </div>

      <form
        autoComplete="off"
        className="floating-chat-form border-t border-[#E9E4DA] bg-white p-3 text-[#101B3A] pb-[max(0.75rem,env(safe-area-inset-bottom))]"
        data-1p-ignore="true"
        data-bwignore="true"
        data-form-type="other"
        data-lpignore="true"
        onSubmit={(event) => {
          event.preventDefault();
          onSend();
        }}
      >
        <div className="floating-input-shell flex items-end gap-2 rounded-[1.45rem] border border-[#E5DED2] bg-[#FFFDF8] p-2 shadow-[0_10px_24px_rgba(16,27,58,0.06)]">
          <textarea
            aria-label="Mensagem para o atendimento"
            autoCapitalize="sentences"
            autoComplete="new-password"
            autoCorrect="on"
            className="max-h-28 min-h-11 flex-1 resize-none bg-transparent px-3 py-2 text-base font-semibold leading-6 text-[#101B3A] outline-none placeholder:text-[#98A2B3] sm:text-sm sm:leading-5"
            data-1p-ignore="true"
            data-bwignore="true"
            data-form-type="other"
            data-lpignore="true"
            enterKeyHint="send"
            inputMode="text"
            name="taliya-chat-message"
            onChange={(event) => onInputChange(event.target.value)}
            onKeyDown={(event) => {
              if (event.key === "Enter" && !event.shiftKey) {
                event.preventDefault();
                onSend();
              }
            }}
            onFocus={handleInputFocus}
            placeholder="Pergunte sobre planos ou rotina..."
            ref={inputRef}
            rows={1}
            spellCheck
            value={input}
          />
          <button
            aria-label="Enviar mensagem"
            className="floating-send-button interactive-hit grid h-11 w-11 shrink-0 place-items-center rounded-full bg-[#101B3A] text-white shadow-[0_10px_22px_rgba(16,27,58,0.16)] transition hover:bg-[#18264F] focus:outline-none focus:ring-4 focus:ring-[#FFB21A]/25 disabled:cursor-not-allowed disabled:opacity-45"
            disabled={pending || !input.trim()}
            type="submit"
          >
            <SendIcon className="h-5 w-5" />
          </button>
        </div>
      </form>
    </section>
  );
}

function MessageBubble({ index, message }: { index: number; message: AiAttendantMessage }) {
  const isUser = message.role === "user";
  const isFallback = message.intent === "fallback";
  return (
    <div
      className={`floating-message-bubble max-w-[88%] rounded-[1.35rem] px-4 py-3 text-sm font-bold leading-6 shadow-[0_10px_22px_rgba(16,27,58,0.06)] ${
        isUser
          ? "floating-message-user ml-auto border border-[#101B3A] bg-[#101B3A] text-white"
          : isFallback
            ? "floating-message-error mr-auto border border-[#E5DED2] bg-[#FFFDF8] text-[#344054]"
          : "floating-message-consultor mr-auto border border-[#E5DED2] bg-white text-[#344054]"
      }`}
      style={{ animationDelay: `${Math.min(index, 3) * 42}ms` }}
    >
      {message.action ? (
        <a
          className="inline-flex min-h-10 items-center justify-center rounded-full bg-[#101B3A] px-4 text-sm font-black text-white transition hover:bg-[#18264F] focus:outline-none focus:ring-4 focus:ring-[#FFB21A]/25"
          href={message.action.href}
          rel="noreferrer"
          target="_blank"
        >
          {message.action.label}
        </a>
      ) : (
        message.content
      )}
    </div>
  );
}

function FallbackActions({
  config,
  onQuickReply,
}: {
  config: FloatingAgentConfig;
  onQuickReply: (quickReplyId: string, label: string) => void;
}) {
  const whatsapp = config.quickReplies.find((reply) => reply.id === "human_whatsapp_assist");
  const product = config.quickReplies.find((reply) => reply.id === "ask_product");

  return (
    <div className="floating-response-card floating-error-card mt-4 rounded-[1.55rem] border border-[#E5DED2] bg-white p-4 shadow-[0_12px_30px_rgba(16,27,58,0.06)]">
      <p className="text-sm font-black text-[#101B3A]">Da para continuar por outro caminho.</p>
      <p className="mt-1 text-xs font-semibold leading-5 text-[#667085]">A conversa ficou salva. Você pode tentar uma pergunta mais direta ou seguir para atendimento no WhatsApp.</p>
      <div className="mt-3 grid gap-2 sm:grid-cols-2">
        {product ? (
          <button className="interactive-hit min-h-11 rounded-full border border-[#E5DED2] bg-white px-3 text-xs font-black text-[#101B3A] transition hover:bg-[#FFFDF8]" onClick={() => onQuickReply(product.id, product.label)} type="button">
            Tentar de novo
          </button>
        ) : null}
        {whatsapp ? (
          <button className="interactive-hit min-h-11 rounded-full bg-[#101B3A] px-3 text-xs font-black text-white transition hover:bg-[#18264F]" onClick={() => onQuickReply(whatsapp.id, whatsapp.label)} type="button">
            Continuar no WhatsApp
          </button>
        ) : null}
      </div>
    </div>
  );
}

type NextAction = {
  draftOnly?: boolean;
  quickReplyId?: string;
  message: string;
  suggestion: string;
};

function NextBestAction({
  config,
  messages,
  onQuickReply,
  onSuggestedInput,
  response,
}: {
  config: FloatingAgentConfig;
  messages: AiAttendantMessage[];
  onQuickReply: (quickReplyId: string, label: string) => void;
  onSuggestedInput: (value: string) => void;
  response?: AiAttendantResponse;
}) {
  const action = chooseNextAction(config, messages, response);
  if (!action) return null;

  return (
    <button
      aria-label={`Enviar sugestão: ${action.suggestion}`}
      className="floating-next-suggestion interactive-hit group mt-4 flex w-full items-center gap-2.5 rounded-[1.15rem] border border-[#E5DED2] bg-white px-3 py-2.5 text-left shadow-[0_8px_18px_rgba(16,27,58,0.04)] transition hover:border-[#6E7F2C]/35 hover:bg-[#FFFDF8] focus:outline-none focus:ring-4 focus:ring-[#FFB21A]/20"
      onClick={() => {
        if (action.draftOnly) {
          onSuggestedInput(action.message);
          return;
        }
        onQuickReply(action.quickReplyId ?? "diagnostic_suggested_answer", action.message);
      }}
      type="button"
    >
      <span className="min-w-0 flex-1 text-sm font-bold leading-5 text-[#667085]">
        <span className="text-[#98A2B3]">Sugestao: </span>
        <span className="text-[#101B3A]">{action.suggestion}</span>
      </span>
      <span className="grid h-9 w-9 shrink-0 place-items-center rounded-full bg-[#101B3A] text-white transition group-hover:bg-[#18264F]">
        <ArrowRightIcon className="h-4 w-4 transition group-hover:translate-x-0.5" />
      </span>
    </button>
  );
}

function chooseNextAction(config: FloatingAgentConfig, messages: AiAttendantMessage[], response?: AiAttendantResponse): NextAction | null {
  const isPlansCopy = config.label === "Consultor";
  const findReply = (id: string) => config.quickReplies.find((reply) => reply.id === id);
  const transcript = messages
    .map((message) => message.content)
    .join(" ")
    .toLowerCase()
    .normalize("NFD")
    .replace(/\p{Diacritic}/gu, "");
  const hasRecommendations = Boolean(response?.recommendations?.length);
  const lastAssistantContent = ([...messages].reverse().find((message) => message.role === "assistant")?.content ?? "")
    .normalize("NFD")
    .replace(/\p{Diacritic}/gu, "");
  const isInitialDiagnosticOffer = messages.some(
    (message) =>
      message.role === "assistant" &&
      /diagnostico gratuito|diagnostico do seu studio|o que voce acha|o que você acha|mapear o que voce quer organizar no seu negocio/i.test(
        message.content
          .normalize("NFD")
          .replace(/\p{Diacritic}/gu, ""),
      ),
  );

  if (isInitialDiagnosticOffer && /diagnostico gratuito|diagnostico do seu studio|o que voce acha|o que você acha|mapear o que voce quer organizar no seu negocio/i.test(lastAssistantContent)) {
    return null;
  }

  const actionMap: Record<string, { suggestion: string }> = {
    describe_pain: {
      suggestion: isPlansCopy ? "Quero mapear minha rotina" : "Quero organizar minha rotina",
    },
    ask_agents: {
      suggestion: isPlansCopy ? "Quais rotinas resolveriam isso?" : "O que posso organizar com a Taliya?",
    },
    view_plans: {
      suggestion: "Abrir comparativo de planos",
    },
    human_whatsapp_assist: {
      suggestion: "Quero continuar pelo WhatsApp",
    },
    ask_product: {
      suggestion: "Me explica como funciona a Taliya",
    },
  };

  const lastAssistantQuestion = [...messages].reverse().find((message) => message.role === "assistant" && /\?/.test(message.content))?.content;
  const diagnosticQuestion = response?.nextQuestion && !response.conversionPath ? response.nextQuestion : lastAssistantQuestion;
  const diagnosticActive =
    response?.qualificationPatch?.diagnosticType === "crm_agent_diagnostic" ||
    response?.conversionPath === "crm_agent_diagnostic";
  if (response?.nextQuestion && isOfficialDiagnosticQuestion(response.nextQuestion)) return null;
  const diagnosticSuggestion = diagnosticQuestion ? diagnosticAnswerSuggestion(diagnosticQuestion, diagnosticActive, isPlansCopy) : null;
  if (diagnosticSuggestion) {
    return {
      draftOnly: diagnosticSuggestion.draftOnly,
      quickReplyId: diagnosticSuggestion.quickReplyId ?? "diagnostic_suggested_answer",
      message: diagnosticSuggestion.message,
      suggestion: diagnosticSuggestion.suggestion,
    };
  }

  let preferredId = "describe_pain";

  if (/\b(preco|valor|plano|planos|assinar|assinatura|contratar|checkout|pagar|pagamento|pix)\b/.test(transcript) || hasRecommendations) {
    preferredId = "view_plans";
  } else if (response?.nextQuestion && !response.conversionPath) {
    preferredId = "describe_pain";
  } else if (/\b(whatsapp|humano|pessoa|consultor|atendente)\b/.test(transcript)) {
    preferredId = "human_whatsapp_assist";
  } else if (/\b(agente|agenda|agendamento|atendimento|financeiro|reposicao|reposicoes|falta|faltas|venda|vendas|renovacao|renovacoes|servico|servicos|orcamento|orcamentos|cliente|clientes|recebimento|recebimentos|lembrete|lembretes|resumo|resumos|listagem|listagens|documento|documentos|marketing|instagram)\b/.test(transcript)) {
    preferredId = "ask_agents";
  } else if (messages.length <= 1) {
    preferredId = "ask_product";
  }

  const reply = findReply(preferredId) ?? findReply("describe_pain") ?? findReply("ask_product") ?? config.quickReplies[0];
  if (!reply) return null;

  const content = actionMap[reply.id] ?? actionMap.describe_pain;
  return {
    quickReplyId: reply.id,
    message: reply.label,
    suggestion: content.suggestion,
  };
}

function isOfficialDiagnosticQuestion(nextQuestion: string) {
  const normalized = nextQuestion
    .toLowerCase()
    .normalize("NFD")
    .replace(/\p{Diacritic}/gu, "");

  return /quantos alunos|alunos ativos|quantos clientes|clientes que atende|quais partes|dao trabalho|sistema|whatsapp, planilha|ver facilmente|tarefa.*leve|resolver isso agora|pesquisando por enquanto/.test(normalized);
}

function diagnosticAnswerSuggestion(nextQuestion: string, diagnosticActive: boolean, isPlansCopy: boolean) {
  const normalized = nextQuestion
    .toLowerCase()
    .normalize("NFD")
    .replace(/\p{Diacritic}/gu, "");

  if (/diagnostico gratuito|diagnostico do seu studio|o que voce acha|o que você acha/.test(normalized)) {
    return { quickReplyId: "start_crm_diagnostic", message: "Quero fazer diagnóstico gratuito", suggestion: "Quero fazer diagnóstico gratuito" };
  }
  if (!diagnosticActive) return null;
  if (/quais partes|dao trabalho|mais dao trabalho|agenda\/reposicoes|financeiro ou acompanhamento/.test(normalized)) {
    const answer = isPlansCopy ? "Vendas e interessados" : "Agenda e serviços";
    return { message: answer, suggestion: answer };
  }
  if (/me passa.*whatsapp|whatsapp ou email|email.*continuo|diagnostico salvo|contato/.test(normalized)) {
    return { draftOnly: true, message: "Meu WhatsApp é ", suggestion: "Deixar meu WhatsApp" };
  }
  if (/com quem eu falo|com quem falo|qual.*nome/.test(normalized)) return { draftOnly: true, message: "Meu nome é ", suggestion: "Responder meu nome" };
  if (/quantos alunos|alunos ativos|quantos clientes|clientes que atende|tamanho/.test(normalized)) {
    if (isPlansCopy) return { message: "Tenho cerca de 100 alunos", suggestion: "Tenho cerca de 100 alunos" };
    return { draftOnly: true, message: "Atendo cerca de ", suggestion: "Informar número de clientes" };
  }
  if (/ver facilmente|resolver no dia|prioridade/.test(normalized)) {
    const answer = isPlansCopy ? "Não consigo ver fácil o que precisa resolver" : "Tenho dificuldade para acompanhar minha rotina";
    return { message: answer, suggestion: answer };
  }
  if (/reposi|remarc/.test(normalized)) {
    const answer = isPlansCopy ? "Reposições viram muita troca de mensagem" : "Remarcações viram muita troca de mensagens";
    return { message: answer, suggestion: answer };
  }
  if (/conhecer o studio|virar aluno|acompanhar|novos clientes|interessados/.test(normalized)) {
    const answer = isPlansCopy ? "Perco interessados por demora no retorno" : "Às vezes demoro para responder novos clientes";
    return { message: answer, suggestion: answer };
  }
  if (/sistema|planilha|caderno|fica em algum/.test(normalized)) return { message: "Hoje uso WhatsApp e planilha", suggestion: "Hoje uso WhatsApp e planilha" };
  if (/qual tarefa|mais leve|tirar uma coisa|este mes|primeiro/.test(normalized)) {
    return isPlansCopy
      ? { message: "Quero aliviar WhatsApp e agenda primeiro", suggestion: "Aliviar WhatsApp e agenda" }
      : { message: "Quero organizar meus horários e clientes primeiro", suggestion: "Organizar horários e clientes" };
  }
  if (/resolver isso agora|pesquisando|por enquanto/.test(normalized)) return { message: "Quero resolver agora, se fizer sentido", suggestion: "Quero resolver agora, se fizer sentido" };
  return { message: "Quero continuar o diagnóstico", suggestion: "Continuar o diagnóstico" };
}

function formatAgentNames(agentIds: string[], isPlansCopy: boolean) {
  const labels: Record<string, string> = isPlansCopy
    ? {
      atendimento: "Atendimento",
      agenda: "Agenda",
      vendas: "Vendas",
      financeiro: "Financeiro",
      retencao: "Retenção",
      gestao: "Gestão",
      "historico-evolucao": "Histórico/Evolução",
    }
    : {
      atendimento: "Clientes",
      agenda: "Agenda",
      vendas: "Serviços e orçamentos",
      financeiro: "Recebimentos",
      retencao: "Lembretes",
      gestao: "Resumos e listagens",
      "historico-evolucao": "Documentos e histórico",
    };

  return agentIds.map((id) => labels[id] ?? id).join(" + ");
}

function AgentRecommendationLine({ label, muted, text, tone }: { label: string; muted?: boolean; text?: string; tone?: "pain" }) {
  if (!text) return null;
  return (
    <p className={`mt-2 leading-5 ${muted ? "text-[#667085]" : "text-[#344054]"}`}>
      <span className={`mr-1.5 font-black ${tone === "pain" ? "text-[#6E7F2C]" : "text-[#101B3A]"}`}>{label}:</span>
      {text}
    </p>
  );
}

function ConversionActions({
  analysisDestination,
  config,
  humanWhatsAppDestination,
  response,
  subscriptionPlan,
}: {
  analysisDestination: TrustedDestination;
  config: FloatingAgentConfig;
  humanWhatsAppDestination: TrustedDestination;
  response: AiAttendantResponse;
  subscriptionPlan?: PricingPlan;
}) {
  const conversionPath = response.conversionPath;
  if (!conversionPath || conversionPath === "waitlist_intent" || conversionPath === "crm_agent_diagnostic") return null;

  const action =
    conversionPath === "guided_demo" && !config.guidedDemoReady
      ? config.conversionCtas.humanWhatsApp
      : conversionPath === "view_plans" || conversionPath === "plan_recommendation"
      ? config.conversionCtas.viewPlans
      : conversionPath === "custom_agent_diagnostic_mapped"
      ? config.conversionCtas.viewPlans
      : conversionPath === "guided_demo"
        ? config.conversionCtas.guidedDemo
        : conversionPath === "checkout_intent"
          ? config.conversionCtas.checkoutIntent
          : conversionPath === "human_whatsapp_assist"
            ? config.conversionCtas.humanWhatsApp
            : conversionPath === "analysis_request"
              ? config.conversionCtas.analysis
              : conversionPath === "custom_agent_follow_up" || conversionPath === "mixed_subscription_plus_custom"
                ? config.conversionCtas.customAgent
                : conversionPath === "custom_agent_diagnostic_unclear"
                  ? config.conversionCtas.humanWhatsApp
                : config.conversionCtas.viewPlans;

  const destination = getTrustedDestination(config, response, action.systemDestination, subscriptionPlan, analysisDestination, humanWhatsAppDestination);
  if (!destination) return null;

  return (
    <div className="floating-response-card floating-handoff-card mt-4 rounded-[1.55rem] border border-[#D9E2B8] bg-white p-4 shadow-[0_14px_34px_rgba(16,27,58,0.08)]">
      <p className="text-[11px] font-black uppercase tracking-[0.22em] text-[#6E7F2C]">{conversionCardEyebrow(conversionPath)}</p>
      <p className="mt-1 text-sm font-black leading-5 text-[#101B3A]">{conversionCardTitle(conversionPath)}</p>
      <p className="mt-1 text-xs font-semibold leading-5 text-[#667085]">{conversionCardDescription(conversionPath, config.label === "Consultor")}</p>
      <a
        aria-label={destination.label}
        className="floating-conversion-cta interactive-hit mt-3 inline-flex min-h-11 w-full items-center justify-center gap-2 rounded-full bg-[#101B3A] px-4 text-sm font-black text-white shadow-[0_10px_22px_rgba(16,27,58,0.10)] transition hover:bg-[#18264F] focus:outline-none focus:ring-4 focus:ring-[#FFB21A]/20"
        href={destination.href}
      >
        <span className="truncate">{destination.label}</span>
        <ArrowRightIcon className="h-4 w-4 shrink-0" />
      </a>
    </div>
  );
}

function conversionCardEyebrow(conversionPath: NonNullable<AiAttendantResponse["conversionPath"]>) {
  if (conversionPath === "guided_demo") return "Demo";
  if (conversionPath === "human_whatsapp_assist") return "Atendimento";
  if (conversionPath === "analysis_request") return "Diagnóstico";
  if (conversionPath.includes("custom_agent")) return "Agente especifico";
  return "Próximo passo";
}

function conversionCardTitle(conversionPath: NonNullable<AiAttendantResponse["conversionPath"]>) {
  if (conversionPath === "guided_demo") return "Ver a Taliya funcionando";
  if (conversionPath === "checkout_intent") return "Continuar assinatura";
  if (conversionPath === "human_whatsapp_assist") return "Continuar com um consultor";
  if (conversionPath === "analysis_request") return "Fazer diagnóstico gratuito";
  if (conversionPath.includes("custom_agent")) return "Mapear uma necessidade especifica";
  return "Comparar planos da Taliya";
}

function conversionCardDescription(conversionPath: NonNullable<AiAttendantResponse["conversionPath"]>, isPlansCopy: boolean) {
  if (conversionPath === "guided_demo") return isPlansCopy ? "Veja o fluxo antes de decidir o melhor caminho para o studio." : "Veja o fluxo antes de decidir o melhor caminho para o seu negócio.";
  if (conversionPath === "checkout_intent") return "O atendimento segue com o plano selecionado e sua conversa salva.";
  if (conversionPath === "human_whatsapp_assist") return "A conversa vai com contexto para o atendimento não recomeçar do zero.";
  if (conversionPath === "analysis_request") return isPlansCopy ? "A Taliya entende a rotina do studio antes de recomendar um plano." : "A Taliya entende a rotina do seu negócio antes de recomendar um plano.";
  if (conversionPath.includes("custom_agent")) return "Boa opção quando sua operação precisa de algo além dos planos atuais.";
  return "Compare o que muda entre organizar, ativar um agente ou conectar o time completo.";
}

function getTrustedDestination(
  config: FloatingAgentConfig,
  response: AiAttendantResponse,
  systemDestination: string,
  subscriptionPlan?: PricingPlan,
  analysisDestination?: TrustedDestination,
  humanWhatsAppDestination?: TrustedDestination,
): TrustedDestination | { label: string; href: string } | null {
  if (systemDestination === "recommended_plan_checkout") {
    if (subscriptionPlan) return subscriptionPlan.primaryCta;
    if (response.subscription?.checkoutUrl) return { label: response.subscription.ctaLabel, href: response.subscription.checkoutUrl };
  }

  if (systemDestination === "configured_plan_comparison" || systemDestination === "fallback_plan_selection") {
    return withSelectedPlan(config.planComparisonDestination, response.subscription?.planId);
  }
  if (systemDestination === "configured_guided_demo") return config.guidedDemoReady ? config.guidedDemoDestination : humanWhatsAppDestination ?? null;
  if (systemDestination === "assisted_human_whatsapp") return subscriptionPlan?.secondaryHumanCta ?? humanWhatsAppDestination ?? null;
  if (systemDestination === "assisted_analysis") return analysisDestination ?? null;
  return null;
}

function withSelectedPlan(destination: TrustedDestination, planId?: string): TrustedDestination {
  if (!planId) return destination;

  try {
    const url = new URL(destination.href, "https://taliya.local");
    url.searchParams.set("plan", planId);
    return {
      ...destination,
      href: `${url.pathname}${url.search}${url.hash}`,
    };
  } catch {
    return destination;
  }
}

// Kept temporarily for compatibility while older chat copy is phased out.
// eslint-disable-next-line @typescript-eslint/no-unused-vars
function replyDescription(id: string) {
  if (id === "ask_product") return "Entenda Taliya sem compromisso";
  if (id === "describe_pain") return "Faltas, reposições, vendas, financeiro";
  if (id === "ask_agents") return "Veja quem cuida de cada rotina";
  if (id === "human_whatsapp_assist") return "Levar contexto da conversa";
  return "Continuar conversa";
}

// eslint-disable-next-line @typescript-eslint/no-unused-vars
function ReplyIcon({ id }: { id: string }) {
  if (id === "human_whatsapp_assist") return <PhoneIcon className="h-4 w-4" />;
  if (id === "ask_agents") return <GridIcon className="h-4 w-4" />;
  if (id === "describe_pain") return <SparkIcon className="h-4 w-4" />;
  return <MessageIcon className="h-4 w-4" />;
}

function CloseIcon({ className = "" }: { className?: string }) {
  return (
    <svg aria-hidden="true" className={className} fill="none" viewBox="0 0 24 24">
      <path d="m6 6 12 12M18 6 6 18" stroke="currentColor" strokeLinecap="round" strokeWidth="2.4" />
    </svg>
  );
}

function SendIcon({ className = "" }: { className?: string }) {
  return (
    <svg aria-hidden="true" className={className} fill="none" viewBox="0 0 24 24">
      <path d="M5 12h13M13 6l6 6-6 6" stroke="currentColor" strokeLinecap="round" strokeLinejoin="round" strokeWidth="2.4" />
    </svg>
  );
}

function ArrowRightIcon({ className = "" }: { className?: string }) {
  return (
    <svg aria-hidden="true" className={className} fill="none" viewBox="0 0 20 20">
      <path d="M4 10h12M11 5l5 5-5 5" stroke="currentColor" strokeLinecap="round" strokeLinejoin="round" strokeWidth="2.1" />
    </svg>
  );
}

function MessageIcon({ className = "" }: { className?: string }) {
  return (
    <svg aria-hidden="true" className={className} fill="none" viewBox="0 0 24 24">
      <path d="M5 6.5h14v8.8H9.4L5 18.5v-12Z" stroke="currentColor" strokeLinejoin="round" strokeWidth="2" />
    </svg>
  );
}

function SparkIcon({ className = "" }: { className?: string }) {
  return (
    <svg aria-hidden="true" className={className} fill="none" viewBox="0 0 24 24">
      <path d="m12 3 1.7 5.2L19 10l-5.3 1.8L12 17l-1.7-5.2L5 10l5.3-1.8L12 3Z" stroke="currentColor" strokeLinejoin="round" strokeWidth="2" />
    </svg>
  );
}

function GridIcon({ className = "" }: { className?: string }) {
  return (
    <svg aria-hidden="true" className={className} fill="none" viewBox="0 0 24 24">
      <path d="M5 5h6v6H5V5Zm8 0h6v6h-6V5ZM5 13h6v6H5v-6Zm8 0h6v6h-6v-6Z" stroke="currentColor" strokeLinejoin="round" strokeWidth="2" />
    </svg>
  );
}

function PhoneIcon({ className = "" }: { className?: string }) {
  return (
    <svg aria-hidden="true" className={className} fill="none" viewBox="0 0 24 24">
      <path
        d="M6.8 4.7 9 4.2c.6-.1 1.1.2 1.3.8l.9 2.4c.2.5 0 1-.4 1.3L9.7 9.6a10.2 10.2 0 0 0 4.7 4.7l.9-1.1c.3-.4.9-.6 1.3-.4l2.4.9c.6.2.9.8.8 1.3l-.5 2.2c-.1.6-.6 1-1.2 1A12.3 12.3 0 0 1 5.8 5.9c0-.6.4-1.1 1-1.2Z"
        stroke="currentColor"
        strokeLinecap="round"
        strokeLinejoin="round"
        strokeWidth="2"
      />
    </svg>
  );
}
