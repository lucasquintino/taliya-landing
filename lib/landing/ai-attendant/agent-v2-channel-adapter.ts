import type { AiAttendantRequest } from "./schema";
import type { AgentV2ConversationState } from "./agent-v2-types";
import { conversationIdForRequest } from "./agent-v2-state-compat";

export type AgentV2NormalizedInput = {
  channel: "widget" | "whatsapp";
  source: "direct" | "site" | "instagram" | "facebook" | "ad" | "unknown";
  conversationId: string;
  leadId?: string;
  externalMessageId?: string;
  idempotencyKey: string;
  text?: string;
  media?: {
    type: "audio" | "image" | "document" | "unknown";
    providerId?: string;
  };
  channelMetadata: {
    phoneNumberId?: string;
    whatsappFrom?: string;
    whatsappProfileName?: string;
    widgetSessionId?: string;
    pagePath?: string;
    entryIntent?: string;
  };
  receivedAt: string;
};

export function normalizeAgentV2Input(request: AiAttendantRequest): AgentV2NormalizedInput {
  const conversationId = conversationIdForRequest(request);
  const source = detectSource(request);
  const externalMessageId = request.session.externalContact?.providerMessageId;
  const channel = request.session.channel === "whatsapp" ? "whatsapp" : "widget";

  return {
    channel,
    source,
    conversationId,
    leadId: request.session.leadId,
    externalMessageId,
    idempotencyKey: `${channel}:${conversationId}:${request.session.messages.length}:${request.userMessage ?? request.quickReplyId ?? "turn"}`,
    text: request.userMessage,
    media: detectMedia(request.userMessage),
    channelMetadata: {
      phoneNumberId: request.session.externalContact?.phoneNumberId,
      whatsappFrom: request.session.externalContact?.phone,
      whatsappProfileName: request.session.qualificationDraft?.name,
      widgetSessionId: request.session.channel === "web" ? request.session.sessionId : undefined,
      pagePath: request.session.sourcePage,
      entryIntent: request.session.entryPath,
    },
    receivedAt: new Date().toISOString(),
  };
}

export function buildChannelDeliveryPlan(responseTexts: string[], state: AgentV2ConversationState) {
  if (state.channel === "whatsapp") {
    return {
      channel: "whatsapp" as const,
      messages: responseTexts.map((text) => ({ text, role: "assistant" as const, kind: "text" as const })),
      whatsappDelivery: {
        chunks: responseTexts.map((text) => ({ text, typingDelayMs: Math.min(7000, Math.max(1500, Math.ceil(text.length * 45))) })),
        maxChunks: 3 as const,
      },
    };
  }

  return {
    channel: "widget" as const,
    messages: responseTexts.map((text) => ({ text, role: "assistant" as const, kind: "text" as const })),
  };
}

function detectSource(request: AiAttendantRequest): AgentV2NormalizedInput["source"] {
  const text = `${request.userMessage ?? ""} ${request.session.sourceSection ?? ""} ${request.session.entryPath ?? ""}`.toLowerCase();
  if (/instagram/.test(text)) return "instagram";
  if (/facebook/.test(text)) return "facebook";
  if (/anuncio|ad|diagnostic_cta/.test(text)) return "ad";
  if (/site|\/pilates/.test(text)) return "site";
  return "direct";
}

function detectMedia(text?: string): AgentV2NormalizedInput["media"] {
  const normalized = (text ?? "").toLowerCase();
  if (/\[unsupported_whatsapp_message:audio\]|audio|áudio/.test(normalized)) return { type: "audio" };
  if (/\[unsupported_whatsapp_message:image\]|imagem|foto|print/.test(normalized)) return { type: "image" };
  if (/\[unsupported_whatsapp_message:document\]|documento|pdf/.test(normalized)) return { type: "document" };
  if (/\[unsupported_whatsapp_message:/.test(normalized)) return { type: "unknown" };
  return undefined;
}
