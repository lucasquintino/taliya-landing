import type { AiAttendantRequest, AiAttendantResponse } from "./schema";
import { hasPostgresStorage, postgresQuery } from "./storage/postgres";

type FunnelEventInput = {
  eventName: string;
  request: AiAttendantRequest;
  response?: AiAttendantResponse;
  leadId?: string;
  payload?: Record<string, unknown>;
};

type LandingInteractionEventInput = {
  eventName: "widget_opened" | "cta_clicked";
  occurrenceId: string;
  sessionId: string;
  leadId?: string;
  channel?: string;
  sourcePage?: string;
  sourceSection?: string;
  metadata?: Record<string, unknown>;
};

const memoryEvents: Array<Record<string, unknown>> = [];

export async function recordFunnelEvent({ eventName, request, response, leadId, payload = {} }: FunnelEventInput) {
  const commercialStage = response?.qualificationPatch?.commercialStage ?? request.session.qualificationDraft?.commercialStage;
  const conversionPath = response?.conversionPath;
  const occurrenceId =
    response?.qualificationPatch?.agentRuntimeRunId ??
    request.session.externalContact?.providerMessageId ??
    [...request.session.messages].reverse().find((message) => message.role === "user")?.id ??
    `${request.session.messages.length}:${hashString(request.userMessage?.trim() ?? eventName)}`;
  const idempotencyKey = [
    request.session.channel,
    request.session.channelSessionId ?? request.session.sessionId,
    eventName,
    occurrenceId,
  ].join(":");
  const eventId = `funnel_${hashString(idempotencyKey)}`;
  const safePayload = sanitizePayload({
    ...payload,
    waitlistStatus: response?.qualificationPatch?.waitlistStatus,
    diagnosticStatus: response?.qualificationPatch?.diagnosticStatus,
    demoStatus: response?.qualificationPatch?.demoStatus,
    sourcePage: request.session.sourcePage,
    sourceSection: request.session.sourceSection,
    entryPath: request.session.entryPath,
    ...acquisitionMetadata(request.metadata),
  });
  const acquisition = acquisitionMetadata(request.metadata);

  if (hasPostgresStorage()) {
    await postgresQuery(
      `INSERT INTO ai_funnel_events (
        event_id, idempotency_key, session_id, lead_id, channel, event_name,
        commercial_stage, conversion_path, anonymous_session_id, message_id,
        run_id, trace_id, page_path, source_section, cta_id, referrer,
        utm_source, utm_medium, utm_campaign, utm_content, utm_term,
        payload, created_at
      ) VALUES (
        $1, $2, $3, $4, $5, $6, $7, $8, $9, $10, $11, $12, $13, $14,
        $15, $16, $17, $18, $19, $20, $21, $22::jsonb, now()
      )
      ON CONFLICT (idempotency_key) DO NOTHING`,
      [
        eventId,
        idempotencyKey,
        request.session.sessionId,
        leadId ?? request.session.leadId,
        request.session.channel,
        eventName,
        commercialStage,
        conversionPath,
        readMetadataString(request.metadata, "anonymousSessionId") ?? request.session.sessionId,
        occurrenceId,
        response?.qualificationPatch?.agentRuntimeRunId,
        response?.qualificationPatch?.agentRuntimeTraceId,
        request.session.sourcePage,
        request.session.sourceSection,
        readMetadataString(request.metadata, "ctaId"),
        acquisition.referrer,
        acquisition.utmSource,
        acquisition.utmMedium,
        acquisition.utmCampaign,
        acquisition.utmContent,
        acquisition.utmTerm,
        JSON.stringify(safePayload),
      ],
    );
  } else if (!memoryEvents.some((event) => event.idempotencyKey === idempotencyKey)) {
    memoryEvents.push({
      eventId,
      idempotencyKey,
      sessionId: request.session.sessionId,
      leadId: leadId ?? request.session.leadId,
      channel: request.session.channel,
      eventName,
      commercialStage,
      conversionPath,
      payload: safePayload,
      createdAt: new Date().toISOString(),
    });
  }

  return { eventId, idempotencyKey };
}

export async function recordLandingInteractionEvent(input: LandingInteractionEventInput) {
  const acquisition = acquisitionMetadata(input.metadata);
  const idempotencyKey = [input.channel ?? "web", input.sessionId, input.eventName, input.occurrenceId].join(":");
  const eventId = `funnel_${hashString(idempotencyKey)}`;
  const payload = sanitizePayload({
    sourcePage: input.sourcePage,
    sourceSection: input.sourceSection,
    ...acquisition,
  });

  if (hasPostgresStorage()) {
    await postgresQuery(
      `INSERT INTO ai_funnel_events (
        event_id, idempotency_key, session_id, lead_id, channel, event_name,
        anonymous_session_id, message_id, page_path, source_section, cta_id,
        referrer, utm_source, utm_medium, utm_campaign, utm_content, utm_term,
        payload, created_at
      ) VALUES (
        $1, $2, $3, $4, $5, $6, $7, $8, $9, $10, $11, $12, $13, $14,
        $15, $16, $17, $18::jsonb, now()
      ) ON CONFLICT (idempotency_key) DO NOTHING`,
      [
        eventId,
        idempotencyKey,
        input.sessionId,
        input.leadId,
        input.channel ?? "web",
        input.eventName,
        readMetadataString(input.metadata, "anonymousSessionId") ?? input.sessionId,
        input.occurrenceId,
        input.sourcePage,
        input.sourceSection,
        readMetadataString(input.metadata, "ctaId") ?? input.sourceSection,
        acquisition.referrer,
        acquisition.utmSource,
        acquisition.utmMedium,
        acquisition.utmCampaign,
        acquisition.utmContent,
        acquisition.utmTerm,
        JSON.stringify(payload),
      ],
    );
  } else if (!memoryEvents.some((event) => event.idempotencyKey === idempotencyKey)) {
    memoryEvents.push({
      eventId,
      idempotencyKey,
      sessionId: input.sessionId,
      leadId: input.leadId,
      channel: input.channel ?? "web",
      eventName: input.eventName,
      payload,
      createdAt: new Date().toISOString(),
    });
  }

  return { eventId, idempotencyKey };
}

function acquisitionMetadata(metadata?: Record<string, unknown>) {
  return {
    referrer: readMetadataString(metadata, "referrer"),
    utmSource: readMetadataString(metadata, "utmSource"),
    utmMedium: readMetadataString(metadata, "utmMedium"),
    utmCampaign: readMetadataString(metadata, "utmCampaign"),
    utmContent: readMetadataString(metadata, "utmContent"),
    utmTerm: readMetadataString(metadata, "utmTerm"),
  };
}

function readMetadataString(metadata: Record<string, unknown> | undefined, key: string) {
  const value = metadata?.[key];
  return typeof value === "string" && value.trim() ? value.trim().slice(0, 500) : undefined;
}

function sanitizePayload(payload: Record<string, unknown>) {
  return Object.fromEntries(
    Object.entries(payload).filter(([key, value]) => {
      if (/token|secret|password|card|cvv/i.test(key)) return false;
      return value === undefined || value === null || ["string", "number", "boolean"].includes(typeof value);
    }),
  );
}

function hashString(value: string) {
  let hash = 0;
  for (let index = 0; index < value.length; index += 1) {
    hash = (hash << 5) - hash + value.charCodeAt(index);
    hash |= 0;
  }
  return Math.abs(hash).toString(36);
}
