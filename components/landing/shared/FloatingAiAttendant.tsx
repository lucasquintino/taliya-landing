"use client";

import { useEffect, useMemo, useRef, useState } from "react";
import type { NicheLandingConfig } from "@/data/landing/niches/types";
import { widgetFirstResponseDelay, widgetNextResponseDelay } from "@/lib/landing/ai-attendant/delivery-timing";
import type { AiAttendantMessage, AiAttendantRequest, AiAttendantResponse, ConversionHandoff } from "@/lib/landing/ai-attendant/schema";
import { trackLandingEvent } from "@/lib/landing/tracking";
import { FloatingAiAttendantButton } from "./FloatingAiAttendantButton";
import { FloatingAiAttendantPanel } from "./FloatingAiAttendantPanel";

export function FloatingAiAttendant({
  config,
  compact: isCompact = false,
  hideLauncher = false,
  pageSignals,
}: {
  config: NicheLandingConfig;
  compact?: boolean;
  hideLauncher?: boolean;
  pageSignals: {
    selectedPainId?: string;
    selectedAgentId?: string;
    calculatorEstimate?: number;
  };
}) {
  const [isOpen, setIsOpen] = useState(false);
  const [messages, setMessages] = useState<AiAttendantMessage[]>(() => readStoredMessages(config.niche));
  const [selectedPainIds, setSelectedPainIds] = useState<string[]>(() => readStoredStringArray(config.niche, "selectedPainIds"));
  const [recommendedAgentIds, setRecommendedAgentIds] = useState<string[]>(() => readStoredStringArray(config.niche, "recommendedAgentIds"));
  const [qualificationDraft, setQualificationDraft] = useState<Record<string, string>>(() => readStoredStringRecord(config.niche, "qualificationDraft"));
  const [input, setInput] = useState("");
  const [pending, setPending] = useState(false);
  const [openingPending, setOpeningPending] = useState(false);
  const [attentionReady, setAttentionReady] = useState(false);
  const [launcherSettled, setLauncherSettled] = useState(false);
  const [viewportReady, setViewportReady] = useState(false);
  const [isMobileViewport, setIsMobileViewport] = useState(false);
  const [lastResponse, setLastResponse] = useState<AiAttendantResponse | undefined>();
  const [sessionId] = useState(() => readStoredSessionId(config.niche) ?? `anon_${createClientId()}`);
  const [leadId] = useState(() => readStoredLeadId(config.niche) ?? `lead_${createClientId()}`);
  const messagesRef = useRef<AiAttendantMessage[]>([]);
  const messageCounter = useRef(messages.length);
  const openingDeliveredRef = useRef(messages.length > 0);
  const firstMeaningfulMessageTrackedRef = useRef(messages.some((message) => message.role === "user" && message.content.trim().length >= 3));
  const attentionReadyRef = useRef(false);
  const isOpenRef = useRef(false);
  const attentionSoundPlayedRef = useRef(false);
  const openingTimerRef = useRef<number | null>(null);
  const attentionTimerRef = useRef<number | null>(null);
  const entryPathRef = useRef<AiAttendantRequest["session"]["entryPath"]>("widget");
  const sourceSectionRef = useRef("widget");

  const recommendedPlan = useMemo(
    () => config.subscription.plans.find((plan) => plan.id === config.subscription.recommendedPlanId) ?? config.subscription.plans.find((plan) => plan.recommended),
    [config.subscription.plans, config.subscription.recommendedPlanId],
  );

  useEffect(() => {
    const handleSalesOpen = (event: Event) => {
      if (!isSalesAgentEvent(event)) {
        open("widget");
        return;
      }

      open(event.detail.sourceSection ?? "widget", event.detail.message);
    };

    window.addEventListener("landing:open-sales-agent", handleSalesOpen);

    return () => {
      window.removeEventListener("landing:open-sales-agent", handleSalesOpen);
    };
  });

  useEffect(() => {
    messagesRef.current = messages;
    writeStoredChatState(config.niche, {
      messages,
      qualificationDraft,
      recommendedAgentIds,
      selectedPainIds,
      sessionId,
      leadId,
    });
  }, [config.niche, leadId, messages, qualificationDraft, recommendedAgentIds, selectedPainIds, sessionId]);

  useEffect(() => {
    attentionReadyRef.current = attentionReady;
  }, [attentionReady]);

  useEffect(() => {
    isOpenRef.current = isOpen;
  }, [isOpen]);

  useEffect(() => {
    const settleTimer = window.setTimeout(() => setLauncherSettled(true), 1700);
    return () => {
      window.clearTimeout(settleTimer);
      if (openingTimerRef.current) window.clearTimeout(openingTimerRef.current);
      if (attentionTimerRef.current) window.clearTimeout(attentionTimerRef.current);
    };
  }, []);

  useEffect(() => {
    const unlockAudio = () => {
      void unlockSoftMessageSound().then((unlocked) => {
        if (!unlocked || !attentionReadyRef.current || isOpenRef.current || attentionSoundPlayedRef.current) return;
        attentionSoundPlayedRef.current = playSoftMessageSound(0);
      });
    };

    window.addEventListener("pointerdown", unlockAudio, { once: true, passive: true });
    window.addEventListener("touchstart", unlockAudio, { once: true, passive: true });
    window.addEventListener("keydown", unlockAudio, { once: true });

    return () => {
      window.removeEventListener("pointerdown", unlockAudio);
      window.removeEventListener("touchstart", unlockAudio);
      window.removeEventListener("keydown", unlockAudio);
    };
  }, []);

  useEffect(() => {
    if (isOpen) return;

    const prefersReducedMotion = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
    if (prefersReducedMotion) return;

    const scheduleAttention = (delayMs: number) => {
      if (attentionTimerRef.current) window.clearTimeout(attentionTimerRef.current);
      attentionTimerRef.current = window.setTimeout(() => {
        setAttentionReady(true);
        attentionSoundPlayedRef.current = playSoftMessageSound(0);
        if (typeof navigator !== "undefined" && "vibrate" in navigator) navigator.vibrate(18);
      }, delayMs);
    };

    scheduleAttention(4200);

    return () => {
      if (attentionTimerRef.current) window.clearTimeout(attentionTimerRef.current);
    };
  }, [isOpen]);

  useEffect(() => {
    const mediaQuery = window.matchMedia("(max-width: 639px)");
    const updateViewport = () => {
      setIsMobileViewport(mediaQuery.matches);
      setViewportReady(true);
    };

    updateViewport();
    mediaQuery.addEventListener("change", updateViewport);
    window.addEventListener("resize", updateViewport);
    window.visualViewport?.addEventListener("resize", updateViewport);

    return () => {
      mediaQuery.removeEventListener("change", updateViewport);
      window.removeEventListener("resize", updateViewport);
      window.visualViewport?.removeEventListener("resize", updateViewport);
    };
  }, []);

  function open(sourceSection = "widget", openingMessageOverride?: string) {
    entryPathRef.current = mapEntryPath(sourceSection);
    sourceSectionRef.current = sourceSection;
    setAttentionReady(false);
    setIsOpen(true);
    void recordOperationalLandingEvent("widget_opened", sourceSection);
    const entryMessage = openingMessageOverride?.trim();
    const shouldSendEntryMessage = Boolean(entryMessage && (messagesRef.current.length || shouldForceEntryMessage(sourceSection)));

    if (shouldSendEntryMessage && entryMessage) {
      openingDeliveredRef.current = true;
      void submitMessage(entryMessage, quickReplyIdForSourceSection(sourceSection));
    } else {
      queueOpeningMessage(sourceSection, openingMessageOverride);
    }
    trackLandingEvent(config.tracking, "floating_agent_opened", { channel: "web", sourceSection, entryPath: entryPathRef.current });
  }

  async function recordOperationalLandingEvent(eventName: "widget_opened" | "cta_clicked", sourceSection: string) {
    try {
      await fetch("/api/landing/ai-attendant/events", {
        method: "POST",
        headers: { "content-type": "application/json" },
        body: JSON.stringify({
          eventName,
          occurrenceId: createClientId(),
          sessionId,
          leadId,
          channel: "web",
          sourcePage: window.location.pathname || config.route,
          sourceSection,
          metadata: readAcquisitionMetadata(),
        }),
        keepalive: true,
      });
    } catch {
      // Operational tracking must never block the commercial conversation.
    }
  }

  function close() {
    setIsOpen(false);
    trackLandingEvent(config.tracking, "floating_agent_closed", { channel: "web" });
  }

  function queueOpeningMessage(sourceSection: string, openingMessageOverride?: string) {
    if (messagesRef.current.length || openingDeliveredRef.current) return;

    openingDeliveredRef.current = true;
    setOpeningPending(true);
    playSoftMessageSound(0.42);

    openingTimerRef.current = window.setTimeout(async () => {
      const openingMessages =
        entryPathRef.current === "diagnostic_cta"
          ? openingMessagesForEntryPath(config, entryPathRef.current)
          : openingMessageOverride
            ? [openingMessageOverride]
            : openingMessagesForEntryPath(config, mapEntryPath(sourceSection));

      for (let index = 0; index < openingMessages.length; index += 1) {
        if (index > 0) await delay(680);
        playSoftMessageSound(0);
        const openingMessage: AiAttendantMessage = {
          id: nextMessageId(`assistant_opening_${index + 1}`),
          role: "assistant",
          content: openingMessages[index] ?? config.floatingAgent.greeting,
          intent: "answer_question",
        };

        setMessages((current) => (current.length && index === 0 ? current : [...current, openingMessage]));
      }

      setOpeningPending(false);
      trackLandingEvent(config.tracking, "floating_agent_message_delivered", {
        channel: "web",
        entryPath: entryPathRef.current,
        sourceSection,
        messageKind: "opening",
      });
    }, 420);
  }

  async function submitMessage(messageText: string, quickReplyId?: string) {
    const cleanMessage = messageText.trim();
    const currentMessages = messagesRef.current.length ? messagesRef.current : messages;
    const effectiveQuickReplyId = quickReplyId ?? (isDiagnosticStartMessage(cleanMessage) ? "start_crm_diagnostic" : undefined);
    if (!cleanMessage && !effectiveQuickReplyId) return;

    const userMessage: AiAttendantMessage | undefined = cleanMessage
      ? {
          id: nextMessageId("user"),
          role: "user",
          content: cleanMessage,
        }
      : undefined;

    const nextMessages = userMessage ? [...currentMessages, userMessage] : currentMessages;
    setMessages(nextMessages);
    setInput("");
    setPending(true);

    trackLandingEvent(config.tracking, effectiveQuickReplyId ? "floating_agent_quick_reply_clicked" : "floating_agent_message_sent", {
      channel: "web",
      entryPath: entryPathRef.current,
      quickReplyId: effectiveQuickReplyId,
      messageLength: cleanMessage.length,
      sourceSection: sourceSectionRef.current,
    });

    if (!firstMeaningfulMessageTrackedRef.current && cleanMessage.length >= 3) {
      firstMeaningfulMessageTrackedRef.current = true;
      trackLandingEvent(config.tracking, "first_meaningful_chat_message", {
        channel: "web",
        entryPath: entryPathRef.current,
        sourceSection: sourceSectionRef.current,
        messageLength: cleanMessage.length,
      });
    }

    try {
      const apiStartedAt = performance.now();
      const request: AiAttendantRequest = {
        session: {
          sessionId,
          leadId,
          channel: "web",
          niche: config.niche,
          entryPath: entryPathRef.current,
          sourceSection: sourceSectionRef.current,
          sourcePage: window.location.pathname || config.route,
          campaignStage: config.tracking.campaignStage,
          publicOfferMode: config.tracking.publicOfferMode,
          messages: nextMessages,
          selectedPainIds: unique([...selectedPainIds, ...compact([pageSignals.selectedPainId])]),
          recommendedAgentIds: unique([...recommendedAgentIds, ...compact([pageSignals.selectedAgentId])]),
          qualificationDraft,
        },
        userMessage: cleanMessage || undefined,
        quickReplyId: effectiveQuickReplyId,
        metadata: readAcquisitionMetadata(),
        pageSignals,
      };

      const response = await fetch("/api/landing/ai-attendant", {
        method: "POST",
        headers: { "content-type": "application/json" },
        body: JSON.stringify(request),
      });

      const payload = (await response.json()) as AiAttendantResponse | { error?: string };
      if (!response.ok || "error" in payload) {
        throw new Error("error" in payload && payload.error ? payload.error : "AI attendant request failed.");
      }
      const attendantResponse = payload as AiAttendantResponse;
      const apiLatencyMs = performance.now() - apiStartedAt;

      setLastResponse(attendantResponse);
      if (attendantResponse.capturedPainIds.length) {
        setSelectedPainIds((current) => unique([...current, ...attendantResponse.capturedPainIds]));
      }
      if (attendantResponse.recommendedAgentIds.length) {
        setRecommendedAgentIds((current) => unique([...current, ...attendantResponse.recommendedAgentIds]));
      }
      if (attendantResponse.qualificationPatch) {
        setQualificationDraft((current) => ({
          ...current,
          ...attendantResponse.qualificationPatch,
        }));
      }
      await deliverAssistantMessages(attendantResponse, apiLatencyMs);
      setPending(false);
      trackStructuredResponse(attendantResponse);
    } catch {
      const fallback: AiAttendantMessage = {
        id: nextMessageId("assistant_fallback"),
        role: "assistant",
        content: config.floatingAgent.fallbackMessages.providerFailure,
        intent: "fallback",
      };
      setMessages((current) => [...current, fallback]);
      trackLandingEvent(config.tracking, "floating_agent_fallback", {
        channel: "web",
        category: "client_request_failed",
      });
      setPending(false);
    }
  }

  async function deliverAssistantMessages(response: AiAttendantResponse, apiLatencyMs: number) {
    const assistantMessages = response.assistantMessages.flatMap((message) =>
      splitAssistantMessage(message).map((content, index) => ({
        ...message,
        id: index === 0 ? message.id : `${message.id}_part_${index + 1}`,
        content,
      })),
    );
    const isDiagnosticFinal = response.conversionPath === "crm_agent_diagnostic";
    const firstDelayMs = widgetFirstResponseDelay(apiLatencyMs, isDiagnosticFinal);

    await delay(firstDelayMs);

    for (let index = 0; index < assistantMessages.length; index += 1) {
      if (index > 0) {
        await delay(widgetNextResponseDelay(apiLatencyMs, assistantMessages[index]?.content.length ?? 0, index, isDiagnosticFinal));
      }
      const assistantMessage = assistantMessages[index];
      if (!assistantMessage) continue;
      playSoftMessageSound(0);
      setMessages((current) => [...current, assistantMessage]);
    }
  }

  function nextMessageId(prefix: string) {
    messageCounter.current += 1;
    return `${prefix}_${messageCounter.current}`;
  }

  function trackStructuredResponse(response: AiAttendantResponse) {
    if (response.capturedPainIds.length) {
      trackLandingEvent(config.tracking, "floating_agent_pain_captured", {
        channel: "web",
        entryPath: entryPathRef.current,
        sourceSection: sourceSectionRef.current,
        painIds: response.capturedPainIds,
      });
    }
    if (response.recommendedAgentIds.length) {
      trackLandingEvent(config.tracking, "floating_agent_agent_recommended", {
        channel: "web",
        entryPath: entryPathRef.current,
        sourceSection: sourceSectionRef.current,
        agentIds: response.recommendedAgentIds,
      });
    }
    if (response.qualificationPatch) {
      trackLandingEvent(config.tracking, "floating_agent_qualification_started", {
        channel: "web",
        entryPath: entryPathRef.current,
        sourceSection: sourceSectionRef.current,
        fields: Object.keys(response.qualificationPatch),
      });
    }
    if (response.conversionPath === "view_plans") {
      trackLandingEvent(config.tracking, "floating_agent_view_plans_cta", {
        channel: "web",
        entryPath: entryPathRef.current,
        sourceSection: sourceSectionRef.current,
      });
    }
    if (response.conversionPath === "guided_demo") {
      trackLandingEvent(config.tracking, "floating_agent_guided_demo_cta", {
        channel: "web",
        entryPath: entryPathRef.current,
        sourceSection: sourceSectionRef.current,
        guidedDemoReady: config.floatingAgent.guidedDemoReady,
      });
    }
    if (response.conversionPath === "plan_recommendation") {
      trackLandingEvent(config.tracking, "floating_agent_plan_recommendation_cta", {
        channel: "web",
        entryPath: entryPathRef.current,
        sourceSection: sourceSectionRef.current,
        planId: response.subscription?.planId,
      });
    }
    if (response.conversionPath === "checkout_intent") {
      trackLandingEvent(config.tracking, "floating_agent_checkout_cta", {
        channel: "web",
        entryPath: entryPathRef.current,
        sourceSection: sourceSectionRef.current,
        planId: response.subscription?.planId,
        destinationHref: response.subscription?.checkoutUrl,
      });
    }
    if (response.conversionPath === "waitlist_intent") {
      trackLandingEvent(config.tracking, "floating_agent_waitlist_intent", {
        channel: "web",
        entryPath: entryPathRef.current,
        sourceSection: sourceSectionRef.current,
        waitlistStatus: response.qualificationPatch?.waitlistStatus,
        commercialStage: response.qualificationPatch?.commercialStage,
      });
    }
    if (response.conversionPath === "analysis_request") {
      trackLandingEvent(config.tracking, "floating_agent_analysis_handoff", createSafeHandoffMetadata(response, "analysis_request", entryPathRef.current, sourceSectionRef.current));
    }
    if (response.conversionPath === "crm_agent_diagnostic") {
      trackLandingEvent(config.tracking, "floating_agent_diagnostic_handoff", {
        ...createSafeHandoffMetadata(response, "crm_agent_diagnostic", entryPathRef.current, sourceSectionRef.current),
        diagnosticType: response.qualificationPatch?.diagnosticType,
        leadTemperature: response.qualificationPatch?.leadTemperature,
      });
    }
    if (response.conversionPath === "human_whatsapp_assist") {
      trackLandingEvent(config.tracking, "floating_agent_human_whatsapp_handoff", createSafeHandoffMetadata(response, "human_whatsapp_assist", entryPathRef.current, sourceSectionRef.current));
    }
    if (
      response.conversionPath === "custom_agent_follow_up" ||
      response.conversionPath === "custom_agent_diagnostic_mapped" ||
      response.conversionPath === "mixed_subscription_plus_custom" ||
      response.conversionPath === "custom_agent_diagnostic_unclear"
    ) {
      trackLandingEvent(config.tracking, "floating_agent_diagnostic_handoff", {
        ...createSafeHandoffMetadata(response, response.conversionPath, entryPathRef.current, sourceSectionRef.current),
        diagnosticClassification: response.diagnosticClassification,
        diagnosticContextVariant: response.diagnosticContextVariant,
      });
    }
    if (response.guardrailDecision.category !== "allowed") {
      trackLandingEvent(config.tracking, "floating_agent_fallback", {
        channel: "web",
        entryPath: entryPathRef.current,
        sourceSection: sourceSectionRef.current,
        category: response.guardrailDecision.category,
        action: response.guardrailDecision.action,
      });
    }
  }

  if (!config.floatingAgent.enabled) return null;

  return isOpen ? (
    <FloatingAiAttendantPanel
      analysisDestination={config.assistedConversion.analysisDestination}
      config={config.floatingAgent}
      humanWhatsAppDestination={config.assistedConversion.humanWhatsAppDestination}
      input={input}
      messages={messages}
      onClose={close}
      onInputChange={setInput}
      onSuggestedInput={setInput}
      onQuickReply={(quickReplyId, label) => submitMessage(label, quickReplyId)}
      onSend={() => submitMessage(input)}
      pending={pending}
      openingPending={openingPending}
      response={lastResponse}
      subscriptionPlan={recommendedPlan}
    />
  ) : hideLauncher || !viewportReady ? (
    null
  ) : (
    <FloatingAiAttendantButton
      attention={attentionReady}
      compact={isCompact}
      config={config.floatingAgent}
      settled={launcherSettled}
      mobileOnly={isMobileViewport}
      mode={messages.length ? "active" : attentionReady ? "attention" : "idle"}
      onClick={() => open("widget")}
    />
  );
}

function compact(values: Array<string | undefined>) {
  return values.filter((value): value is string => Boolean(value));
}

function unique(values: string[]) {
  return Array.from(new Set(values.filter(Boolean)));
}

function delay(milliseconds: number) {
  return new Promise<void>((resolve) => {
    window.setTimeout(resolve, milliseconds);
  });
}

function splitAssistantMessage(message: AiAttendantMessage) {
  const content = message.content.trim();
  if (!content || content.length <= 420) return content ? [content] : [];
  const sentences = content
    .split(/(?<=[.!?])\s+/)
    .map((part) => part.trim())
    .filter(Boolean);
  const chunks: string[] = [];
  let current = "";

  for (const sentence of sentences.length ? sentences : [content]) {
    if (!current) {
      current = sentence;
    } else if (`${current} ${sentence}`.length > 420) {
      chunks.push(current);
      current = sentence;
    } else {
      current = `${current} ${sentence}`;
    }
  }

  if (current) chunks.push(current);
  return chunks.flatMap((chunk) => (chunk.length <= 420 ? [chunk] : chunk.match(/.{1,420}/g) ?? [chunk])).slice(0, 3);
}

function storageKey(niche: string) {
  return `taliya:floating-chat:${niche}`;
}

function createClientId() {
  if (typeof crypto !== "undefined" && "randomUUID" in crypto) {
    return crypto.randomUUID().replaceAll("-", "");
  }

  return `${Date.now().toString(36)}_${Math.random().toString(36).slice(2, 12)}`;
}

function readAcquisitionMetadata() {
  if (typeof window === "undefined") return {};
  const params = new URLSearchParams(window.location.search);
  return {
    anonymousSessionId: readOrCreateLandingSessionId(),
    referrer: document.referrer || undefined,
    utmSource: params.get("utm_source") || undefined,
    utmMedium: params.get("utm_medium") || undefined,
    utmCampaign: params.get("utm_campaign") || undefined,
    utmContent: params.get("utm_content") || undefined,
    utmTerm: params.get("utm_term") || undefined,
  };
}

function readOrCreateLandingSessionId() {
  const key = "taliya:landing-session";
  const existing = window.sessionStorage.getItem(key);
  if (existing) return existing;
  const created = `landing_${createClientId()}`;
  window.sessionStorage.setItem(key, created);
  return created;
}

function isLegacyReactSessionId(value: string) {
  return /^anon__r_\d+_$/.test(value);
}

function isLegacyReactLeadId(value: string) {
  return /^lead__r_\d+_$/.test(value);
}

function isLegacyStoredChat(parsed: { sessionId?: unknown; leadId?: unknown }) {
  return (
    (typeof parsed.sessionId === "string" && isLegacyReactSessionId(parsed.sessionId)) ||
    (typeof parsed.leadId === "string" && isLegacyReactLeadId(parsed.leadId))
  );
}

function readStoredSessionId(niche: string) {
  if (typeof window === "undefined") return null;

  try {
    const rawValue = window.sessionStorage.getItem(storageKey(niche));
    if (!rawValue) return null;

    const parsed = JSON.parse(rawValue) as { sessionId?: unknown };
    if (typeof parsed.sessionId !== "string" || !parsed.sessionId || isLegacyReactSessionId(parsed.sessionId)) return null;
    return parsed.sessionId;
  } catch {
    return null;
  }
}

function readStoredLeadId(niche: string) {
  if (typeof window === "undefined") return null;

  try {
    const rawValue = window.sessionStorage.getItem(storageKey(niche));
    if (!rawValue) return null;

    const parsed = JSON.parse(rawValue) as { leadId?: unknown };
    if (typeof parsed.leadId !== "string" || !parsed.leadId || isLegacyReactLeadId(parsed.leadId)) return null;
    return parsed.leadId;
  } catch {
    return null;
  }
}

function readStoredMessages(niche: string): AiAttendantMessage[] {
  if (typeof window === "undefined") return [];

  try {
    const rawValue = window.sessionStorage.getItem(storageKey(niche));
    if (!rawValue) return [];

    const parsed = JSON.parse(rawValue) as { sessionId?: unknown; leadId?: unknown; messages?: unknown };
    if (isLegacyStoredChat(parsed)) return [];
    if (!Array.isArray(parsed.messages)) return [];

    return parsed.messages.filter(isStoredMessage).slice(-24);
  } catch {
    return [];
  }
}

function writeStoredChatState(
  niche: string,
  state: {
    sessionId: string;
    leadId: string;
    messages: AiAttendantMessage[];
    selectedPainIds: string[];
    recommendedAgentIds: string[];
    qualificationDraft: Record<string, string>;
  },
) {
  if (typeof window === "undefined") return;

  try {
    window.sessionStorage.setItem(
      storageKey(niche),
      JSON.stringify({
        sessionId: state.sessionId,
        leadId: state.leadId,
        messages: state.messages.slice(-24),
        selectedPainIds: state.selectedPainIds,
        recommendedAgentIds: state.recommendedAgentIds,
        qualificationDraft: state.qualificationDraft,
        updatedAt: new Date().toISOString(),
      }),
    );
  } catch {
    // Best-effort continuity only; storage failure must never block the sales chat.
  }
}

function readStoredStringArray(niche: string, key: "selectedPainIds" | "recommendedAgentIds") {
  if (typeof window === "undefined") return [];

  try {
    const rawValue = window.sessionStorage.getItem(storageKey(niche));
    if (!rawValue) return [];

    const parsed = JSON.parse(rawValue) as Record<string, unknown>;
    if (isLegacyStoredChat(parsed)) return [];
    return Array.isArray(parsed[key]) ? parsed[key].filter((item): item is string => typeof item === "string") : [];
  } catch {
    return [];
  }
}

function readStoredStringRecord(niche: string, key: "qualificationDraft") {
  if (typeof window === "undefined") return {};

  try {
    const rawValue = window.sessionStorage.getItem(storageKey(niche));
    if (!rawValue) return {};

    const parsed = JSON.parse(rawValue) as Record<string, unknown>;
    if (isLegacyStoredChat(parsed)) return {};
    const value = parsed[key];
    if (!value || typeof value !== "object") return {};

    return Object.fromEntries(Object.entries(value).filter((entry): entry is [string, string] => typeof entry[1] === "string"));
  } catch {
    return {};
  }
}

function isStoredMessage(value: unknown): value is AiAttendantMessage {
  if (!value || typeof value !== "object") return false;

  const message = value as Partial<AiAttendantMessage>;
  return typeof message.id === "string" && (message.role === "assistant" || message.role === "user") && typeof message.content === "string";
}

type SalesAgentOpenEvent = CustomEvent<{ sourceSection?: string; message?: string }>;

function isSalesAgentEvent(event: Event): event is SalesAgentOpenEvent {
  return "detail" in event;
}

function mapEntryPath(sourceSection: string): AiAttendantRequest["session"]["entryPath"] {
  if (sourceSection === "faq_doubt_cta") return "widget";
  if (sourceSection === "studio_diagnostic" || sourceSection === "crm_agent_diagnostic") return "diagnostic_cta";
  if (sourceSection.includes("custom_agent") || sourceSection.includes("diagnostic")) return "custom_agent_diagnostic";
  if (sourceSection.includes("whatsapp")) return "whatsapp_cta";
  if (sourceSection.includes("demo")) return "guided_demo";
  if (sourceSection.includes("assinar") || sourceSection.includes("subscribe")) return "plans_page";
  if (sourceSection.includes("plan")) return "plans_page";
  if (sourceSection.includes("sales") || sourceSection.includes("consultor")) return "consultor_cta";
  if (sourceSection === "widget") return "widget";
  return "unknown";
}

function quickReplyIdForSourceSection(sourceSection: string) {
  if (sourceSection === "studio_diagnostic" || sourceSection === "crm_agent_diagnostic") return "start_crm_diagnostic";
  if (sourceSection.includes("plan")) return "view_plans";
  if (sourceSection.includes("whatsapp")) return "human_whatsapp_assist";
  if (sourceSection.includes("demo")) return "guided_demo";
  if (sourceSection.includes("assinar") || sourceSection.includes("subscribe")) return "waitlist_intent";
  if (sourceSection.includes("custom_agent")) return "custom_agent_interest";
  if (sourceSection.includes("sales") || sourceSection.includes("consultor")) return "consultor_cta";
  return "entry_message";
}

function shouldForceEntryMessage(sourceSection: string) {
  return sourceSection === "studio_diagnostic" || sourceSection === "crm_agent_diagnostic";
}

function isDiagnosticStartMessage(message: string) {
  return /diagnostico|diagnositco|diagnóstico|raio[-\s]?x|mapear meu studio|mapear minha rotina|mapear o que voc[eê] quer organizar no seu neg[oó]cio|organizar minha rotina|fazer diagnostico|fazer diagnositco|quero diagnostico|quero diagnositco|diagnostico gratuito|diagnositco gratuito/i.test(message);
}

function openingMessagesForEntryPath(config: NicheLandingConfig, entryPath: AiAttendantRequest["session"]["entryPath"]) {
  const isPlansPage = typeof window !== "undefined" && window.location.pathname.replace(/\/+$/, "") === "/pilates/planos";
  const pageCopy = (landing: string, plans: string) => isPlansPage ? plans : landing;

  if (entryPath === "consultor_cta") {
    return [pageCopy(
      "Vi que você quer falar com a equipe. Eu te ajudo por aqui e deixo seu atendimento salvo. Qual WhatsApp ou e-mail você prefere usar?",
      "Vi que você quer falar com um consultor. Eu te ajudo por aqui e deixo seu atendimento salvo. Qual WhatsApp ou email você prefere usar?",
    )];
  }

  if (entryPath === "whatsapp_cta") {
    return ["Perfeito. Para continuar pelo WhatsApp com o contexto desta conversa, qual número você prefere usar?"];
  }

  if (entryPath === "guided_demo") {
    return [
      config.floatingAgent.guidedDemoReady
        ? pageCopy(
          "Boa. Vou te guiar pela demonstração como se fosse o seu negócio. Antes de começar, qual WhatsApp ou e-mail você prefere deixar?",
          "Boa. Vou te guiar pela demonstração como se fosse seu studio. Antes de começar, qual WhatsApp ou email você prefere deixar?",
        )
        : pageCopy(
          "A demonstração real ainda não está pronta. Posso te explicar o fluxo e deixar seu atendimento salvo. Qual WhatsApp ou e-mail você prefere usar?",
          "A demonstração real ainda não está pronta. Posso te explicar o fluxo e deixar seu atendimento salvo. Qual WhatsApp ou email você prefere usar?",
        ),
    ];
  }

  if (entryPath === "plans_page") {
    return [pageCopy(
      "Claro. Eu te ajudo a comparar os planos para o seu negócio. Para deixar essa recomendação salva, qual WhatsApp ou e-mail você prefere usar?",
      "Claro. Eu te ajudo a comparar os planos. Para deixar essa recomendação salva, qual WhatsApp ou email você prefere usar?",
    )];
  }

  if (entryPath === "diagnostic_cta") {
    return [pageCopy(
      "Vamos entender a rotina do seu negócio em poucos passos. Primeiro: com quem eu falo?",
      "Boa. Vou fazer um diagnóstico gratuito do seu studio em poucos passos. Primeiro: com quem eu falo?",
    )];
  }

  if (entryPath === "custom_agent_diagnostic") {
    return ["Posso ver se isso cabe nas rotinas atuais ou se vira algo sob medida. Para deixar a análise salva, qual WhatsApp ou email você prefere usar?"];
  }

  return [
    "Oi. Estou aqui para te acompanhar e responder dúvidas sobre a Taliya.",
    pageCopy(
      "Se quiser, posso ajudar a mapear o que você quer organizar no seu negócio. O que precisa de atenção primeiro?",
      "Se fizer sentido para você, podemos fazer um diagnóstico gratuito do seu studio. O que você acha?",
    ),
  ];
}

let floatingAudioContext: AudioContext | null = null;

function getFloatingAudioContext() {
  if (typeof window === "undefined") return null;

  const AudioContextClass =
    window.AudioContext ||
    (window as Window & { webkitAudioContext?: typeof AudioContext }).webkitAudioContext;
  if (!AudioContextClass) return null;

  floatingAudioContext ??= new AudioContextClass();
  return floatingAudioContext;
}

async function unlockSoftMessageSound() {
  try {
    const audioContext = getFloatingAudioContext();
    if (!audioContext) return false;

    if (audioContext.state === "suspended") await audioContext.resume();

    const source = audioContext.createBufferSource();
    source.buffer = audioContext.createBuffer(1, 1, audioContext.sampleRate);
    source.connect(audioContext.destination);
    source.start(0);

    return audioContext.state === "running";
  } catch {
    return false;
  }
}

function playSoftMessageSound(delaySeconds = 0) {
  try {
    const audioContext = getFloatingAudioContext();
    if (!audioContext) return false;

    if (audioContext.state === "suspended") {
      void audioContext.resume().then(() => {
        if (audioContext.state === "running") playSoftMessageSound(delaySeconds);
      });
      return false;
    }

    const startAt = audioContext.currentTime + delaySeconds;
    const gain = audioContext.createGain();
    gain.gain.setValueAtTime(0.0001, startAt);
    gain.gain.exponentialRampToValueAtTime(0.045, startAt + 0.018);
    gain.gain.exponentialRampToValueAtTime(0.0001, startAt + 0.18);
    gain.connect(audioContext.destination);

    [740, 980].forEach((frequency, index) => {
      const oscillator = audioContext.createOscillator();
      oscillator.type = "sine";
      oscillator.frequency.setValueAtTime(frequency, startAt + index * 0.035);
      oscillator.connect(gain);
      oscillator.start(startAt + index * 0.035);
      oscillator.stop(startAt + 0.18 + index * 0.035);
    });

    return true;
  } catch {
    // Audio is an enhancement and can be blocked by browser settings.
    return false;
  }
}

function createSafeHandoffMetadata(
  response: AiAttendantResponse,
  conversionPath: ConversionHandoff["conversionPath"],
  entryPath: AiAttendantRequest["session"]["entryPath"],
  sourceSection: string,
) {
  return {
    channel: "web",
    entryPath,
    sourceSection,
    conversionPath,
    selectedPainIds: response.capturedPainIds,
    recommendedAgentIds: response.recommendedAgentIds,
    hasQualificationPatch: Boolean(response.qualificationPatch),
  };
}
