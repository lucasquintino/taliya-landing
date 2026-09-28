import type { AiAttendantChannel, AiAttendantRequest } from "./schema";

export type ConversationChannel = {
  channel: AiAttendantChannel;
  capabilities: Array<"render_quick_replies" | "send_text_reply" | "handoff_to_form" | "handoff_to_follow_up">;
  sessionKey: string;
  replyPolicy: "allow_automatic_reply" | "stop_automatic_reply" | "human_handoff_only";
  source: "landing_widget" | "meta_whatsapp_cloud_api";
};

export type WhatsAppInboundTurn = {
  provider: "meta_whatsapp_cloud_api";
  providerMessageId: string;
  providerContactId: string;
  fromPhone?: string;
  profileName?: string;
  phoneNumberId?: string;
  displayPhoneNumber?: string;
  text: string;
  occurredAt: string;
  rawSignatureVerified: boolean;
};

export function createWebChannel(sessionId: string): ConversationChannel {
  return {
    channel: "web",
    capabilities: ["render_quick_replies", "send_text_reply", "handoff_to_form", "handoff_to_follow_up"],
    sessionKey: sessionId,
    replyPolicy: "allow_automatic_reply",
    source: "landing_widget",
  };
}

export function createWhatsAppChannel(turn: WhatsAppInboundTurn, optedOut: boolean): ConversationChannel {
  return {
    channel: "whatsapp",
    capabilities: ["send_text_reply", "handoff_to_follow_up"],
    sessionKey: `wa_${turn.providerContactId}`,
    replyPolicy: optedOut ? "stop_automatic_reply" : "allow_automatic_reply",
    source: "meta_whatsapp_cloud_api",
  };
}

export function normalizeWhatsAppTurnToRequest({
  baseRequest,
  turn,
  messages,
  qualificationDraft,
  selectedPainIds,
  recommendedAgentIds,
  optedOut,
}: {
  baseRequest: Pick<AiAttendantRequest["session"], "campaignStage" | "publicOfferMode">;
  turn: WhatsAppInboundTurn;
  messages: AiAttendantRequest["session"]["messages"];
  qualificationDraft?: AiAttendantRequest["session"]["qualificationDraft"];
  selectedPainIds: string[];
  recommendedAgentIds: string[];
  optedOut: boolean;
}): AiAttendantRequest {
  const reliableProfileName = getReliableWhatsAppProfileName(turn.profileName);
  const nextQualificationDraft =
    reliableProfileName && !qualificationDraft?.name
      ? {
          ...qualificationDraft,
          name: reliableProfileName,
          leadSourceChannel: "whatsapp" as const,
        }
      : qualificationDraft;

  return {
    session: {
      sessionId: `wa_${turn.providerContactId}`,
      channel: "whatsapp",
      channelSessionId: turn.providerContactId,
      entryPath: "whatsapp_cta",
      niche: "pilates",
      sourcePage: "whatsapp",
      campaignStage: baseRequest.campaignStage,
      publicOfferMode: baseRequest.publicOfferMode,
      messages,
      qualificationDraft: nextQualificationDraft,
      selectedPainIds,
      recommendedAgentIds,
      externalContact: {
        type: "whatsapp",
        phone: turn.fromPhone,
        providerContactId: turn.providerContactId,
        providerMessageId: turn.providerMessageId,
        phoneNumberId: turn.phoneNumberId,
        displayPhoneNumber: turn.displayPhoneNumber,
        optedOut,
      },
    },
    userMessage: turn.text,
  };
}

function getReliableWhatsAppProfileName(profileName?: string) {
  const clean = profileName?.replace(/\s+/g, " ").trim();
  if (!clean || clean.length < 2 || clean.length > 40) return undefined;
  if (/[^\p{L}\s.'-]/u.test(clean)) return undefined;
  const words = clean.split(/\s+/);
  if (words.length > 3) return undefined;
  if (words.length === 1 && words[0].length < 2) return undefined;
  const normalized = clean
    .toLowerCase()
    .normalize("NFD")
    .replace(/\p{Diacritic}/gu, "");
  if (/\b(studio|estudio|pilates|oficial|atendimento|recepcao|secretaria|agenda|comercial)\b/.test(normalized)) return undefined;
  return clean;
}
