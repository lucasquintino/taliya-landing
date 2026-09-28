import { createHmac, randomUUID, timingSafeEqual } from "crypto";
import type { AiAttendantResponse } from "./schema";
import type { WhatsAppInboundTurn } from "./channels";
import { whatsappReplyDelayMs } from "./delivery-timing";
import { hasPostgresStorage, postgresQuery } from "./storage/postgres";

export type WhatsAppUnsupportedInboundTurn = {
  provider: "meta_whatsapp_cloud_api";
  providerMessageId: string;
  providerContactId: string;
  fromPhone?: string;
  phoneNumberId?: string;
  displayPhoneNumber?: string;
  messageType: string;
  occurredAt: string;
  rawSignatureVerified: boolean;
};

export type WhatsAppBusinessAppEchoTurn = {
  provider: "meta_whatsapp_cloud_api";
  providerMessageId: string;
  providerContactId: string;
  toPhone?: string;
  fromBusinessPhone?: string;
  phoneNumberId?: string;
  displayPhoneNumber?: string;
  text?: string;
  messageType: string;
  occurredAt: string;
  rawSignatureVerified: boolean;
};

export type WhatsAppProviderStatusTurn = {
  provider: "meta_whatsapp_cloud_api";
  providerMessageId: string;
  providerStatus: string;
  recipientId?: string;
  phoneNumberId?: string;
  displayPhoneNumber?: string;
  occurredAt: string;
  errorCode?: string;
};

export type WhatsAppSendResult =
  | { ok: true; providerMessageId?: string; status: "sent" | "skipped" }
  | { ok: false; status: "failed"; reason: string };

export type WhatsAppSendSequenceResult =
  | { ok: true; providerMessageId?: string; providerMessageIds: string[]; status: "sent" | "skipped"; results: WhatsAppSendResult[] }
  | { ok: false; providerMessageId?: string; providerMessageIds: string[]; status: "failed"; reason: string; results: WhatsAppSendResult[] };

export function verifyMetaWebhookChallenge(url: string) {
  const params = new URL(url).searchParams;
  const mode = params.get("hub.mode");
  const token = params.get("hub.verify_token");
  const challenge = params.get("hub.challenge");

  if (mode !== "subscribe" || !challenge) return null;
  if (!process.env.META_WHATSAPP_WEBHOOK_VERIFY_TOKEN) return null;
  if (token !== process.env.META_WHATSAPP_WEBHOOK_VERIFY_TOKEN) return null;

  return challenge;
}

export function verifyMetaSignature(rawBody: string, signatureHeader: string | null) {
  const appSecret = process.env.META_WHATSAPP_APP_SECRET;
  if (!appSecret) return { ok: false, reason: "META_WHATSAPP_APP_SECRET is not configured." };
  if (!signatureHeader?.startsWith("sha256=")) return { ok: false, reason: "Missing x-hub-signature-256 header." };

  const expected = `sha256=${createHmac("sha256", appSecret).update(rawBody).digest("hex")}`;
  const expectedBuffer = Buffer.from(expected);
  const receivedBuffer = Buffer.from(signatureHeader);
  if (expectedBuffer.length !== receivedBuffer.length) return { ok: false, reason: "Invalid signature length." };

  return timingSafeEqual(expectedBuffer, receivedBuffer) ? { ok: true } : { ok: false, reason: "Invalid Meta webhook signature." };
}

export function verifyDualhookSharedSecret(url: string, secretHeader: string | null) {
  const secret = process.env.DUALHOOK_WEBHOOK_SECRET;
  if (!secret) return { ok: false, reason: "DUALHOOK_WEBHOOK_SECRET is not configured." };

  const params = new URL(url).searchParams;
  const receivedSecret = secretHeader || params.get("dualhook_secret") || params.get("webhook_secret");
  if (!receivedSecret) return { ok: false, reason: "Missing Dualhook shared webhook secret." };

  return safeSecretEquals(secret, receivedSecret) ? { ok: true } : { ok: false, reason: "Invalid Dualhook shared webhook secret." };
}

export function verifyDualhookSignature(rawBody: string, signatureHeader: string | null) {
  const secret = process.env.DUALHOOK_WEBHOOK_SECRET;
  if (!secret) return { ok: false, reason: "DUALHOOK_WEBHOOK_SECRET is not configured." };
  if (!signatureHeader?.startsWith("sha256=")) return { ok: false, reason: "Missing x-dualhook-signature header." };

  const expected = `sha256=${createHmac("sha256", secret).update(rawBody).digest("hex")}`;
  const expectedBuffer = Buffer.from(expected);
  const receivedBuffer = Buffer.from(signatureHeader);
  if (expectedBuffer.length !== receivedBuffer.length) return { ok: false, reason: "Invalid Dualhook signature length." };

  return timingSafeEqual(expectedBuffer, receivedBuffer) ? { ok: true } : { ok: false, reason: "Invalid Dualhook webhook signature." };
}

export function verifyExpectedWhatsAppPhoneNumber(rawBody: string) {
  const expectedPhoneNumberId = process.env.META_WHATSAPP_PHONE_NUMBER_ID;
  if (!expectedPhoneNumberId) return { ok: false, reason: "META_WHATSAPP_PHONE_NUMBER_ID is not configured." };

  const payload = safeParse(rawBody);
  if (!isRecord(payload) || payload.object !== "whatsapp_business_account" || !Array.isArray(payload.entry)) {
    return { ok: false, reason: "Invalid WhatsApp webhook payload shape." };
  }

  const phoneNumberIds = collectWebhookPhoneNumberIds(payload);
  if (!phoneNumberIds.length) return { ok: false, reason: "WhatsApp webhook payload is missing phone_number_id." };
  if (phoneNumberIds.every((phoneNumberId) => phoneNumberId === expectedPhoneNumberId)) return { ok: true };

  return { ok: false, reason: "WhatsApp webhook phone_number_id does not match this Taliya connection." };
}

function safeSecretEquals(expected: string, received: string) {
  const expectedBuffer = Buffer.from(expected);
  const receivedBuffer = Buffer.from(received);
  if (expectedBuffer.length !== receivedBuffer.length) return false;
  return timingSafeEqual(expectedBuffer, receivedBuffer);
}

export function parseMetaWhatsAppInbound(rawBody: string): WhatsAppInboundTurn[] {
  const payload = safeParse(rawBody);
  if (!isRecord(payload) || !Array.isArray(payload.entry)) return [];

  return payload.entry.flatMap((entry: unknown) => {
    if (!isRecord(entry) || !Array.isArray(entry.changes)) return [];
    return entry.changes.flatMap((change: unknown) => {
      if (!isRecord(change) || !isRecord(change.value) || !Array.isArray(change.value.messages)) return [];
      const metadata = getWebhookMetadata(change.value);
      return change.value.messages.flatMap((message: unknown) => {
        if (!isRecord(message)) return [];
        const text = getMessageText(message);
        if (!text || typeof message.id !== "string" || typeof message.from !== "string") return [];
        return [
          {
            provider: "meta_whatsapp_cloud_api" as const,
            providerMessageId: message.id,
            providerContactId: message.from,
            fromPhone: message.from,
            profileName: getContactProfileName(change.value as Record<string, unknown>, message.from),
            phoneNumberId: metadata.phoneNumberId,
            displayPhoneNumber: metadata.displayPhoneNumber,
            text,
            occurredAt: timestampToIso(message.timestamp),
            rawSignatureVerified: true,
          },
        ];
      });
    });
  });
}

export function parseMetaWhatsAppUnsupportedInbound(rawBody: string): WhatsAppUnsupportedInboundTurn[] {
  const payload = safeParse(rawBody);
  if (!isRecord(payload) || !Array.isArray(payload.entry)) return [];

  return payload.entry.flatMap((entry: unknown) => {
    if (!isRecord(entry) || !Array.isArray(entry.changes)) return [];
    return entry.changes.flatMap((change: unknown) => {
      if (!isRecord(change) || !isRecord(change.value) || !Array.isArray(change.value.messages)) return [];
      const metadata = getWebhookMetadata(change.value);
      return change.value.messages.flatMap((message: unknown) => {
        if (!isRecord(message)) return [];
        const text = getMessageText(message);
        if (text || typeof message.id !== "string" || typeof message.from !== "string") return [];
        return [
          {
            provider: "meta_whatsapp_cloud_api" as const,
            providerMessageId: message.id,
            providerContactId: message.from,
            fromPhone: message.from,
            phoneNumberId: metadata.phoneNumberId,
            displayPhoneNumber: metadata.displayPhoneNumber,
            messageType: getMessageType(message),
            occurredAt: timestampToIso(message.timestamp),
            rawSignatureVerified: true,
          },
        ];
      });
    });
  });
}

export function parseMetaWhatsAppBusinessAppEchoes(rawBody: string): WhatsAppBusinessAppEchoTurn[] {
  const payload = safeParse(rawBody);
  if (!isRecord(payload) || !Array.isArray(payload.entry)) return [];

  return payload.entry.flatMap((entry: unknown) => {
    if (!isRecord(entry) || !Array.isArray(entry.changes)) return [];
    return entry.changes.flatMap((change: unknown) => {
      if (!isRecord(change) || change.field !== "smb_message_echoes" || !isRecord(change.value) || !Array.isArray(change.value.message_echoes)) return [];
      const metadata = getWebhookMetadata(change.value);
      return change.value.message_echoes.flatMap((message: unknown) => {
        if (!isRecord(message) || typeof message.id !== "string" || typeof message.to !== "string") return [];
        return [
          {
            provider: "meta_whatsapp_cloud_api" as const,
            providerMessageId: message.id,
            providerContactId: message.to,
            toPhone: message.to,
            fromBusinessPhone: typeof message.from === "string" ? message.from : undefined,
            phoneNumberId: metadata.phoneNumberId,
            displayPhoneNumber: metadata.displayPhoneNumber,
            text: getMessageText(message) || undefined,
            messageType: getMessageType(message),
            occurredAt: timestampToIso(message.timestamp),
            rawSignatureVerified: true,
          },
        ];
      });
    });
  });
}

export function parseMetaWhatsAppStatuses(rawBody: string): WhatsAppProviderStatusTurn[] {
  const payload = safeParse(rawBody);
  if (!isRecord(payload) || !Array.isArray(payload.entry)) return [];

  return payload.entry.flatMap((entry: unknown) => {
    if (!isRecord(entry) || !Array.isArray(entry.changes)) return [];
    return entry.changes.flatMap((change: unknown) => {
      if (!isRecord(change) || !isRecord(change.value) || !Array.isArray(change.value.statuses)) return [];
      const metadata = getWebhookMetadata(change.value);
      return change.value.statuses.flatMap((status: unknown) => {
        if (!isRecord(status) || typeof status.id !== "string" || typeof status.status !== "string") return [];
        return [
          {
            provider: "meta_whatsapp_cloud_api" as const,
            providerMessageId: status.id,
            providerStatus: status.status,
            recipientId: typeof status.recipient_id === "string" ? status.recipient_id : undefined,
            phoneNumberId: metadata.phoneNumberId,
            displayPhoneNumber: metadata.displayPhoneNumber,
            occurredAt: timestampToIso(status.timestamp),
            errorCode: getStatusErrorCode(status),
          },
        ];
      });
    });
  });
}

export async function sendMetaWhatsAppReply({
  content,
  replyToProviderMessageId,
  to,
  phoneNumberId,
  idempotencyKey,
  leadId,
  channelSessionId,
  providerContactId,
}: {
  content: string;
  replyToProviderMessageId: string;
  to: string;
  phoneNumberId?: string;
  idempotencyKey?: string;
  leadId?: string;
  channelSessionId?: string;
  providerContactId?: string;
}): Promise<WhatsAppSendResult> {
  return sendMetaWhatsAppText({ content, replyToProviderMessageId, to, phoneNumberId, idempotencyKey, leadId, channelSessionId, providerContactId });
}

export async function sendMetaWhatsAppReplySequence({
  contents,
  replyToProviderMessageId,
  to,
  phoneNumberId,
  idempotencyKey,
  leadId,
  channelSessionId,
  providerContactId,
}: {
  contents: string[];
  replyToProviderMessageId: string;
  to: string;
  phoneNumberId?: string;
  idempotencyKey?: string;
  leadId?: string;
  channelSessionId?: string;
  providerContactId?: string;
}): Promise<WhatsAppSendSequenceResult> {
  const cleanContents = contents.map((content) => content.trim()).filter(Boolean);
  const results: WhatsAppSendResult[] = [];
  const providerMessageIds: string[] = [];

  for (const [index, content] of cleanContents.entries()) {
    await waitForWhatsAppReplyDelay(content, {
      index,
      messageId: replyToProviderMessageId,
      phoneNumberId,
    });

    const result = await sendMetaWhatsAppText({
      content,
      replyToProviderMessageId,
      to,
      phoneNumberId,
      idempotencyKey: idempotencyKey ? `${idempotencyKey}:${index + 1}` : undefined,
      leadId,
      channelSessionId,
      providerContactId,
    });
    results.push(result);

    if (result.ok && result.providerMessageId) providerMessageIds.push(result.providerMessageId);
    if (!result.ok) {
      return {
        ok: false,
        status: "failed",
        reason: result.reason,
        providerMessageId: providerMessageIds[0],
        providerMessageIds,
        results,
      };
    }
  }

  return {
    ok: true,
    status: results.some((result) => result.ok && result.status === "sent") ? "sent" : "skipped",
    providerMessageId: providerMessageIds[0],
    providerMessageIds,
    results,
  };
}

export async function withMetaWhatsAppTypingKeepAlive<T>(
  args: {
    messageId?: string;
    phoneNumberId?: string;
    intervalMs?: number;
  },
  fn: () => Promise<T>,
) {
  const stopTyping = startMetaWhatsAppTypingKeepAlive(args);
  try {
    return await fn();
  } finally {
    stopTyping();
  }
}

export function startMetaWhatsAppTypingKeepAlive({
  messageId,
  phoneNumberId,
  intervalMs,
  initialDelayMs,
}: {
  messageId?: string;
  phoneNumberId?: string;
  intervalMs?: number;
  initialDelayMs?: number;
}) {
  let stopped = false;
  let timer: ReturnType<typeof setTimeout> | undefined;
  const repeatMs = Math.max(1200, intervalMs ?? 5000);

  const tick = async () => {
    if (stopped) return;
    await sendMetaWhatsAppTypingIndicator({ messageId, phoneNumberId });
    if (!stopped) timer = setTimeout(tick, repeatMs);
  };

  if (initialDelayMs && initialDelayMs > 0) {
    timer = setTimeout(tick, initialDelayMs);
  } else {
    void tick();
  }

  return () => {
    stopped = true;
    if (timer) clearTimeout(timer);
  };
}

export async function sendMetaWhatsAppTypingIndicator({
  messageId,
  phoneNumberId: requestedPhoneNumberId,
  graphVersion: requestedGraphVersion,
}: {
  messageId?: string;
  phoneNumberId?: string;
  graphVersion?: string;
}) {
  const token = process.env.META_WHATSAPP_ACCESS_TOKEN;
  const phoneNumberId = requestedPhoneNumberId ?? process.env.META_WHATSAPP_PHONE_NUMBER_ID;
  if (!messageId || !token || !phoneNumberId || token === "mock") return { ok: true, status: "skipped" as const };

  const graphVersion = requestedGraphVersion ?? metaWhatsAppGraphVersion();
  try {
    const response = await fetch(`https://graph.facebook.com/${graphVersion}/${phoneNumberId}/messages`, {
      method: "POST",
      headers: {
        authorization: `Bearer ${token}`,
        "content-type": "application/json",
      },
      body: JSON.stringify({
        messaging_product: "whatsapp",
        status: "read",
        message_id: messageId,
        typing_indicator: {
          type: "text",
        },
      }),
    });

    if (!response.ok) {
      const reason = (await response.text()).slice(0, 500);
      console.warn("[whatsapp-typing] failed", { graphVersion, phoneNumberId, reason });
      return { ok: false, status: "failed" as const, reason };
    }
    const body = await response.text();
    console.info("[whatsapp-typing] sent", {
      graphVersion,
      phoneNumberId,
      messageId,
      body: body.slice(0, 500),
    });
    return { ok: true, status: "sent" as const, body: body.slice(0, 500) };
  } catch (error) {
    const reason = error instanceof Error ? error.message : "Typing indicator failed.";
    console.warn("[whatsapp-typing] failed", { graphVersion, phoneNumberId, reason });
    return { ok: false, status: "failed" as const, reason };
  }
}

export async function sendMetaWhatsAppText({
  content,
  replyToProviderMessageId,
  to,
  phoneNumberId: requestedPhoneNumberId,
  idempotencyKey,
  leadId,
  channelSessionId,
  providerContactId,
}: {
  content: string;
  replyToProviderMessageId?: string;
  to: string;
  phoneNumberId?: string;
  idempotencyKey?: string;
  leadId?: string;
  channelSessionId?: string;
  providerContactId?: string;
}): Promise<WhatsAppSendResult> {
  const token = process.env.META_WHATSAPP_ACCESS_TOKEN;
  const phoneNumberId = requestedPhoneNumberId ?? process.env.META_WHATSAPP_PHONE_NUMBER_ID;
  const outbox = await reserveOutboxMessage({
    content,
    replyToProviderMessageId,
    to,
    phoneNumberId,
    idempotencyKey,
    leadId,
    channelSessionId,
    providerContactId,
  });

  if (outbox?.alreadyFinal) {
    return {
      ok: true,
      status: outbox.status === "sent" ? "sent" : "skipped",
      providerMessageId: outbox.providerMessageId,
    };
  }

  if (!token || !phoneNumberId) {
    await markOutboxSkipped(outbox?.outboxId, "META_WHATSAPP_ACCESS_TOKEN or phone_number_id is not configured.");
    return { ok: true, status: "skipped" };
  }

  if (token === "mock") {
    const providerMessageId = `mock_whatsapp_${randomUUID()}`;
    await markOutboxSent(outbox?.outboxId, providerMessageId);
    return {
      ok: true,
      status: "sent",
      providerMessageId,
    };
  }

  const graphVersion = metaWhatsAppGraphVersion();
  const response = await fetch(`https://graph.facebook.com/${graphVersion}/${phoneNumberId}/messages`, {
    method: "POST",
    headers: {
      authorization: `Bearer ${token}`,
      "content-type": "application/json",
    },
    body: JSON.stringify({
      messaging_product: "whatsapp",
      recipient_type: "individual",
      to,
      type: "text",
      text: {
        preview_url: false,
        body: content.slice(0, 3800),
      },
    }),
  });

  if (!response.ok) {
    const reason = (await response.text()).slice(0, 500);
    await markOutboxFailed(outbox?.outboxId, reason);
    return { ok: false, status: "failed", reason };
  }

  const payload = (await response.json()) as Record<string, unknown>;
  const providerMessageId = Array.isArray(payload.messages) && isRecord(payload.messages[0]) && typeof payload.messages[0].id === "string" ? payload.messages[0].id : undefined;
  await markOutboxSent(outbox?.outboxId, providerMessageId);
  return { ok: true, status: "sent", providerMessageId };
}

function metaWhatsAppGraphVersion() {
  return process.env.META_WHATSAPP_GRAPH_VERSION || "v22.0";
}

export async function recordWhatsAppOutboxProviderStatus({
  providerMessageId,
  providerStatus,
  errorCode,
}: {
  providerMessageId: string;
  providerStatus: string;
  errorCode?: string;
}) {
  if (!hasPostgresStorage()) return;
  const outboxStatus = providerStatus === "failed" ? "failed" : providerStatus === "read" ? "read" : providerStatus === "delivered" ? "delivered" : undefined;
  if (!outboxStatus) return;
  await postgresQuery(
    `UPDATE whatsapp_message_outbox
     SET status = $2, last_error = COALESCE($3, last_error), updated_at = now()
     WHERE provider_message_id = $1`,
    [providerMessageId, outboxStatus, errorCode],
  );
}

export function responseToWhatsAppText(response: AiAttendantResponse) {
  return responseToWhatsAppTexts(response).join("\n\n").slice(0, 3800);
}

export function responseToWhatsAppTexts(response: AiAttendantResponse) {
  const messages = response.assistantMessages
    .flatMap((message) => splitHumanMessage(message.content.trim(), 260))
    .filter(Boolean);
  const stagedDiagnosticDelivery = response.qualificationPatch?.agentRuntimeTemplateIds?.includes("diagnostic.deliver_") ?? false;
  return messages.slice(0, stagedDiagnosticDelivery ? 14 : 3).map((message) => message.slice(0, 1200));
}

export function isWithinWhatsAppCustomerServiceWindow(occurredAt: string, now = Date.now()) {
  const timestamp = Date.parse(occurredAt);
  if (!Number.isFinite(timestamp)) return false;
  return now - timestamp <= 24 * 60 * 60 * 1000;
}

function getMessageText(message: Record<string, unknown>) {
  if (isRecord(message.text) && typeof message.text.body === "string") return message.text.body.trim();
  if (typeof message.button === "object" && isRecord(message.button) && typeof message.button.text === "string") return message.button.text.trim();
  if (typeof message.interactive === "object" && isRecord(message.interactive)) {
    const buttonReply = message.interactive.button_reply;
    if (isRecord(buttonReply) && typeof buttonReply.title === "string") return buttonReply.title.trim();
  }
  return "";
}

function getMessageType(message: Record<string, unknown>) {
  if (typeof message.type === "string" && message.type.trim()) return message.type.trim().slice(0, 64);
  return "unknown";
}

function getWebhookMetadata(value: Record<string, unknown>) {
  const metadata = isRecord(value.metadata) ? value.metadata : {};
  return {
    phoneNumberId: typeof metadata.phone_number_id === "string" ? metadata.phone_number_id : undefined,
    displayPhoneNumber: typeof metadata.display_phone_number === "string" ? metadata.display_phone_number : undefined,
  };
}

function getContactProfileName(value: Record<string, unknown>, waId: string) {
  if (!Array.isArray(value.contacts)) return undefined;
  const contact = value.contacts.find((item) => isRecord(item) && item.wa_id === waId);
  if (!isRecord(contact) || !isRecord(contact.profile)) return undefined;
  return typeof contact.profile.name === "string" ? contact.profile.name.trim() : undefined;
}

function collectWebhookPhoneNumberIds(payload: Record<string, unknown>) {
  const values: string[] = [];
  if (!Array.isArray(payload.entry)) return values;

  for (const entry of payload.entry) {
    if (!isRecord(entry) || !Array.isArray(entry.changes)) continue;
    for (const change of entry.changes) {
      if (!isRecord(change) || !isRecord(change.value) || !isRecord(change.value.metadata)) continue;
      const phoneNumberId = change.value.metadata.phone_number_id;
      if (typeof phoneNumberId === "string" && phoneNumberId.trim()) values.push(phoneNumberId);
    }
  }

  return values;
}

async function waitForWhatsAppReplyDelay(
  content: string,
  typing?: {
    index?: number;
    messageId?: string;
    phoneNumberId?: string;
  },
) {
  if (process.env.NODE_ENV === "test" || process.env.META_WHATSAPP_ACCESS_TOKEN === "mock") return;
  const configured = Number(process.env.AI_ATTENDANT_WHATSAPP_REPLY_DELAY_MS);
  const proportionalDelay = whatsappReplyDelayMs(content, typing?.index ?? 0);
  const configuredDelay = Number.isFinite(configured) && configured >= 0 ? configured : proportionalDelay;
  const delayMs = Math.min(6500, Math.max(500, configuredDelay));
  await new Promise((resolve) => setTimeout(resolve, delayMs));
}

function splitHumanMessage(content: string, maxLength: number) {
  if (!content || content.length <= maxLength) return content ? [content] : [];
  const paragraphs = content.split(/\n{2,}/).map((part) => part.trim()).filter(Boolean);
  const source = paragraphs.length > 1 ? paragraphs : [content];
  return source.flatMap((part) => splitParagraph(part, maxLength));
}

function splitParagraph(content: string, maxLength: number) {
  if (!content || content.length <= maxLength) return content ? [content] : [];
  const sentences = content
    .split(/(?<=[.!?])\s+/)
    .map((part) => part.trim())
    .filter(Boolean);
  const chunks: string[] = [];
  let current = "";
  for (const sentence of sentences.length ? sentences : [content]) {
    if (!current) {
      current = sentence;
      continue;
    }
    if (`${current} ${sentence}`.length > maxLength) {
      chunks.push(current);
      current = sentence;
    } else {
      current = `${current} ${sentence}`;
    }
  }
  if (current) chunks.push(current);
  return chunks.flatMap((chunk) => (chunk.length <= maxLength ? [chunk] : chunk.match(new RegExp(`.{1,${maxLength}}`, "g")) ?? [chunk]));
}

function getStatusErrorCode(status: Record<string, unknown>) {
  if (!Array.isArray(status.errors)) return undefined;
  const first = status.errors[0];
  if (!isRecord(first)) return undefined;
  if (typeof first.code === "number") return String(first.code);
  if (typeof first.code === "string") return first.code;
  return undefined;
}

type ReservedOutboxMessage = {
  outboxId: string;
  alreadyFinal: boolean;
  status?: string;
  providerMessageId?: string;
};

async function reserveOutboxMessage({
  content,
  replyToProviderMessageId,
  to,
  phoneNumberId,
  idempotencyKey,
  leadId,
  channelSessionId,
  providerContactId,
}: {
  content: string;
  replyToProviderMessageId?: string;
  to: string;
  phoneNumberId?: string;
  idempotencyKey?: string;
  leadId?: string;
  channelSessionId?: string;
  providerContactId?: string;
}): Promise<ReservedOutboxMessage | undefined> {
  if (!hasPostgresStorage() || !idempotencyKey) return undefined;
  const outboxId = `wa_out_${randomUUID()}`;
  const inserted = await postgresQuery<WhatsAppOutboxRow>(
    `INSERT INTO whatsapp_message_outbox (
      outbox_id, lead_id, channel_session_id, provider_contact_id, phone_number_id,
      to_phone, content, reply_to_provider_message_id, idempotency_key, status,
      attempt_count, created_at, updated_at
    ) VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9, 'queued', 0, now(), now())
    ON CONFLICT (idempotency_key) DO NOTHING
    RETURNING outbox_id, status, provider_message_id`,
    [outboxId, leadId, channelSessionId, providerContactId ?? to, phoneNumberId, to, content.slice(0, 3800), replyToProviderMessageId, idempotencyKey],
  );

  if (inserted.rows[0]) {
    await postgresQuery(
      "UPDATE whatsapp_message_outbox SET attempt_count = attempt_count + 1, status = 'sending', updated_at = now() WHERE outbox_id = $1",
      [inserted.rows[0].outbox_id],
    );
    return { outboxId: inserted.rows[0].outbox_id, alreadyFinal: false };
  }

  const existing = await postgresQuery<WhatsAppOutboxRow>(
    "SELECT outbox_id, status, provider_message_id FROM whatsapp_message_outbox WHERE idempotency_key = $1 LIMIT 1",
    [idempotencyKey],
  );
  const row = existing.rows[0];
  if (!row) return undefined;
  if (["sent", "skipped", "delivered", "read"].includes(row.status)) {
    return { outboxId: row.outbox_id, alreadyFinal: true, status: row.status, providerMessageId: row.provider_message_id ?? undefined };
  }
  return { outboxId: row.outbox_id, alreadyFinal: true, status: row.status, providerMessageId: row.provider_message_id ?? undefined };
}

async function markOutboxSent(outboxId: string | undefined, providerMessageId?: string) {
  if (!outboxId || !hasPostgresStorage()) return;
  await postgresQuery(
    `UPDATE whatsapp_message_outbox
     SET status = 'sent', provider_message_id = COALESCE($2, provider_message_id), updated_at = now()
     WHERE outbox_id = $1`,
    [outboxId, providerMessageId],
  );
}

async function markOutboxSkipped(outboxId: string | undefined, reason: string) {
  if (!outboxId || !hasPostgresStorage()) return;
  await postgresQuery(
    `UPDATE whatsapp_message_outbox
     SET status = 'skipped', last_error = $2, updated_at = now()
     WHERE outbox_id = $1`,
    [outboxId, reason.slice(0, 500)],
  );
}

async function markOutboxFailed(outboxId: string | undefined, reason: string) {
  if (!outboxId || !hasPostgresStorage()) return;
  await postgresQuery(
    `UPDATE whatsapp_message_outbox
     SET status = 'failed',
         last_error = $2,
         next_attempt_at = now() + interval '5 minutes',
         updated_at = now()
     WHERE outbox_id = $1`,
    [outboxId, reason.slice(0, 500)],
  );
}

type WhatsAppOutboxRow = {
  outbox_id: string;
  status: string;
  provider_message_id?: string | null;
};

function timestampToIso(timestamp: unknown) {
  const value = Number(timestamp);
  if (Number.isFinite(value)) return new Date(value * 1000).toISOString();
  return new Date().toISOString();
}

function safeParse(rawBody: string) {
  try {
    return JSON.parse(rawBody);
  } catch {
    return null;
  }
}

function isRecord(input: unknown): input is Record<string, unknown> {
  return typeof input === "object" && input !== null;
}
