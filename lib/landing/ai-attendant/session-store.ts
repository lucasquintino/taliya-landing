import type { AiAttendantMessage, QualificationDraft } from "./schema";
import { hasPostgresStorage, postgresQuery } from "./storage/postgres";

export type StoredWhatsAppSession = {
  channelSessionId: string;
  provider: "meta_whatsapp_cloud_api";
  providerContactId: string;
  phone?: string;
  phoneNumberId?: string;
  displayPhoneNumber?: string;
  status: "active" | "handoffReady" | "humanActive" | "optedOut" | "providerFailed" | "closed";
  processedProviderMessageIds: string[];
  messages: AiAttendantMessage[];
  qualification: QualificationDraft;
  selectedPainIds: string[];
  recommendedAgentIds: string[];
  optedInAt?: string;
  optedOutAt?: string;
  lastReplyAt?: string;
  lastEventAt?: string;
};

export type SessionStoreResult =
  | { ok: true; session: StoredWhatsAppSession; duplicate: boolean }
  | { ok: false; reason: string };

const whatsappSessions = new Map<string, StoredWhatsAppSession>();

export async function getOrCreateWhatsAppSession({
  providerContactId,
  phoneNumberId,
  displayPhoneNumber,
  phone,
}: {
  providerContactId: string;
  phoneNumberId?: string;
  displayPhoneNumber?: string;
  phone?: string;
}): Promise<StoredWhatsAppSession> {
  const key = sessionKey(providerContactId);
  const normalizedPhone = normalizePhone(phone);

  if (hasPostgresStorage()) {
    const existing = await postgresQuery<WhatsAppSessionRow>(
      "SELECT * FROM whatsapp_sessions WHERE provider_contact_id = $1 LIMIT 1",
      [providerContactId],
    );
    if (existing.rows[0]) {
      const session = rowToSession(existing.rows[0]);
      if ((normalizedPhone && !session.phone) || (phoneNumberId && !session.phoneNumberId) || (displayPhoneNumber && !session.displayPhoneNumber)) {
        await postgresQuery(
          `UPDATE whatsapp_sessions
           SET phone_normalized = COALESCE(phone_normalized, $2),
               phone_number_id = COALESCE(phone_number_id, $3),
               display_phone_number = COALESCE(display_phone_number, $4),
               updated_at = now()
           WHERE provider_contact_id = $1`,
          [providerContactId, normalizedPhone, phoneNumberId, displayPhoneNumber],
        );
        return {
          ...session,
          phone: session.phone ?? normalizedPhone,
          phoneNumberId: session.phoneNumberId ?? phoneNumberId,
          displayPhoneNumber: session.displayPhoneNumber ?? displayPhoneNumber,
        };
      }
      return session;
    }

    const session = createNewSession({ key, providerContactId, phone: normalizedPhone, phoneNumberId, displayPhoneNumber });
    await postgresQuery(
      `INSERT INTO whatsapp_sessions (
        channel_session_id, provider, provider_contact_id, phone_normalized, phone_number_id,
        display_phone_number, status, selected_pain_ids, recommended_agent_ids, qualification,
        messages, opted_in_at, created_at, updated_at
      ) VALUES ($1, $2, $3, $4, $5, $6, $7, $8::jsonb, $9::jsonb, $10::jsonb, $11::jsonb, $12, now(), now())
      ON CONFLICT (provider_contact_id) DO NOTHING`,
      [
        session.channelSessionId,
        session.provider,
        session.providerContactId,
        session.phone,
        session.phoneNumberId,
        session.displayPhoneNumber,
        session.status,
        JSON.stringify(session.selectedPainIds),
        JSON.stringify(session.recommendedAgentIds),
        JSON.stringify(session.qualification),
        JSON.stringify(session.messages),
        session.optedInAt,
      ],
    );
    const persisted = await postgresQuery<WhatsAppSessionRow>(
      "SELECT * FROM whatsapp_sessions WHERE provider_contact_id = $1 LIMIT 1",
      [providerContactId],
    );
    return persisted.rows[0] ? rowToSession(persisted.rows[0]) : session;
  }

  const existing = whatsappSessions.get(key);
  if (existing) {
    if (normalizedPhone && !existing.phone) existing.phone = normalizedPhone;
    if (phoneNumberId && !existing.phoneNumberId) existing.phoneNumberId = phoneNumberId;
    if (displayPhoneNumber && !existing.displayPhoneNumber) existing.displayPhoneNumber = displayPhoneNumber;
    return existing;
  }

  const session = createNewSession({ key, providerContactId, phone: normalizedPhone, phoneNumberId, displayPhoneNumber });
  whatsappSessions.set(key, session);
  return session;
}

export async function registerProviderMessage({
  providerContactId,
  providerMessageId,
  phoneNumberId,
  displayPhoneNumber,
  phone,
}: {
  providerContactId: string;
  providerMessageId: string;
  phoneNumberId?: string;
  displayPhoneNumber?: string;
  phone?: string;
}): Promise<SessionStoreResult> {
  const session = await getOrCreateWhatsAppSession({ providerContactId, phone, phoneNumberId, displayPhoneNumber });

  if (hasPostgresStorage()) {
    const inserted = await postgresQuery<{ provider_message_id: string }>(
      `INSERT INTO whatsapp_provider_messages (
        provider_message_id, channel_session_id, provider_contact_id, phone_number_id,
        direction, status, created_at
      ) VALUES ($1, $2, $3, $4, 'inbound', 'received', now())
      ON CONFLICT (provider_message_id) DO NOTHING
      RETURNING provider_message_id`,
      [providerMessageId, session.channelSessionId, providerContactId, phoneNumberId ?? session.phoneNumberId],
    );

    if (!inserted.rows.length) {
      return { ok: true, session, duplicate: true };
    }

    await postgresQuery(
      "UPDATE whatsapp_sessions SET last_event_at = now(), updated_at = now() WHERE provider_contact_id = $1",
      [providerContactId],
    );
    return { ok: true, session, duplicate: false };
  }

  const duplicate = session.processedProviderMessageIds.includes(providerMessageId);
  if (!duplicate) {
    session.processedProviderMessageIds.push(providerMessageId);
    session.lastEventAt = new Date().toISOString();
    if (session.processedProviderMessageIds.length > 200) {
      session.processedProviderMessageIds = session.processedProviderMessageIds.slice(-100);
    }
  }

  return { ok: true, session, duplicate };
}

export async function markProviderMessageProcessed(providerMessageId: string, status: "processed" | "replied" | "failed", errorCode?: string) {
  if (!hasPostgresStorage()) return;
  await postgresQuery(
    "UPDATE whatsapp_provider_messages SET status = $2, error_code = $3, processed_at = now() WHERE provider_message_id = $1",
    [providerMessageId, status, errorCode],
  );
}

export async function recordProviderStatus({
  providerMessageId,
  providerStatus,
  errorCode,
}: {
  providerMessageId: string;
  providerStatus: string;
  errorCode?: string;
}) {
  if (!hasPostgresStorage()) return;
  await postgresQuery(
    `UPDATE whatsapp_provider_messages
     SET provider_status = $2, error_code = COALESCE($3, error_code), processed_at = now()
     WHERE provider_message_id = $1`,
    [providerMessageId, providerStatus, errorCode],
  );
}

export async function appendWhatsAppMessages(providerContactId: string, messages: AiAttendantMessage[]) {
  const session = await getOrCreateWhatsAppSession({ providerContactId });
  session.messages = [...session.messages, ...messages].slice(-20);
  session.lastReplyAt = new Date().toISOString();

  if (hasPostgresStorage()) {
    await postgresQuery(
      `UPDATE whatsapp_sessions
       SET messages = $2::jsonb, last_reply_at = $3, updated_at = now()
       WHERE provider_contact_id = $1`,
      [providerContactId, JSON.stringify(session.messages), session.lastReplyAt],
    );
  }

  return session;
}

export async function updateWhatsAppSessionState(
  providerContactId: string,
  patch: Partial<Pick<StoredWhatsAppSession, "selectedPainIds" | "recommendedAgentIds" | "qualification" | "status" | "optedOutAt">>,
) {
  const session = await getOrCreateWhatsAppSession({ providerContactId });
  Object.assign(session, patch);

  if (hasPostgresStorage()) {
    await postgresQuery(
      `UPDATE whatsapp_sessions
       SET selected_pain_ids = $2::jsonb,
           recommended_agent_ids = $3::jsonb,
           qualification = $4::jsonb,
           status = $5,
           opted_out_at = $6,
           updated_at = now()
       WHERE provider_contact_id = $1`,
      [
        providerContactId,
        JSON.stringify(session.selectedPainIds),
        JSON.stringify(session.recommendedAgentIds),
        JSON.stringify(session.qualification),
        session.status,
        session.optedOutAt,
      ],
    );
  }

  return session;
}

export async function markWhatsAppOptOut(providerContactId: string) {
  return updateWhatsAppSessionState(providerContactId, {
    status: "optedOut",
    optedOutAt: new Date().toISOString(),
  });
}

function sessionKey(providerContactId: string) {
  return `wa_${providerContactId}`;
}

function createNewSession({
  key,
  providerContactId,
  phone,
  phoneNumberId,
  displayPhoneNumber,
}: {
  key: string;
  providerContactId: string;
  phone?: string;
  phoneNumberId?: string;
  displayPhoneNumber?: string;
}): StoredWhatsAppSession {
  return {
    channelSessionId: key,
    provider: "meta_whatsapp_cloud_api",
    providerContactId,
    phone,
    phoneNumberId,
    displayPhoneNumber,
    status: "active",
    processedProviderMessageIds: [],
    messages: [],
    qualification: {},
    selectedPainIds: [],
    recommendedAgentIds: [],
    optedInAt: new Date().toISOString(),
  };
}

type WhatsAppSessionRow = {
  channel_session_id: string;
  provider: "meta_whatsapp_cloud_api";
  provider_contact_id: string;
  phone_normalized?: string | null;
  phone_number_id?: string | null;
  display_phone_number?: string | null;
  status: StoredWhatsAppSession["status"];
  selected_pain_ids: unknown;
  recommended_agent_ids: unknown;
  qualification: unknown;
  messages: unknown;
  opted_in_at?: Date | string | null;
  opted_out_at?: Date | string | null;
  last_reply_at?: Date | string | null;
  last_event_at?: Date | string | null;
};

function rowToSession(row: WhatsAppSessionRow): StoredWhatsAppSession {
  return {
    channelSessionId: row.channel_session_id,
    provider: row.provider,
    providerContactId: row.provider_contact_id,
    phone: row.phone_normalized ?? undefined,
    phoneNumberId: row.phone_number_id ?? undefined,
    displayPhoneNumber: row.display_phone_number ?? undefined,
    status: row.status,
    processedProviderMessageIds: [],
    messages: Array.isArray(row.messages) ? (row.messages as AiAttendantMessage[]) : [],
    qualification: isRecord(row.qualification) ? (row.qualification as QualificationDraft) : {},
    selectedPainIds: parseStringArray(row.selected_pain_ids),
    recommendedAgentIds: parseStringArray(row.recommended_agent_ids),
    optedInAt: toIso(row.opted_in_at),
    optedOutAt: toIso(row.opted_out_at),
    lastReplyAt: toIso(row.last_reply_at),
    lastEventAt: toIso(row.last_event_at),
  };
}

function parseStringArray(value: unknown) {
  return Array.isArray(value) ? value.filter((item): item is string => typeof item === "string") : [];
}

function toIso(value: Date | string | null | undefined) {
  if (!value) return undefined;
  return value instanceof Date ? value.toISOString() : value;
}

function normalizePhone(phone?: string) {
  if (!phone) return undefined;
  const digits = phone.replace(/\D/g, "");
  if (!digits) return undefined;
  return digits.startsWith("55") ? `+${digits}` : `+55${digits}`;
}

function isRecord(input: unknown): input is Record<string, unknown> {
  return typeof input === "object" && input !== null;
}
