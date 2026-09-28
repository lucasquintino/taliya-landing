import type { LeadPriority, LeadRecord, LeadStatus } from "./leads";
import { getFollowUpEligibility } from "./follow-up";
import { hasPostgresStorage, postgresQuery } from "./storage/postgres";

export type SalesLeadConversation = LeadRecord & {
  recentMessages: Array<{
    id: string;
    role: "user" | "assistant" | "system";
    content: string;
    createdAt: string;
  }>;
  aiPaused: boolean;
  followUpAt?: string;
  lastOperatorActionAt?: string;
  externalSyncStatus: "pending" | "synced" | "failed" | "skipped";
};

export type OperatorActionName =
  | "take_over"
  | "send_whatsapp_message"
  | "send_plan_page"
  | "send_checkout_link"
  | "schedule_follow_up"
  | "resume_ai"
  | "mark_waiting_customer"
  | "mark_won"
  | "mark_lost"
  | "mark_do_not_contact"
  | "edit_lead_summary";

export type OperatorActionRecord = {
  actionId: string;
  leadId: string;
  actorUserId: string;
  action: OperatorActionName;
  payload: Record<string, unknown>;
  beforeStatus: LeadStatus;
  afterStatus: LeadStatus;
  createdAt: string;
};

const memoryStore = globalThis as typeof globalThis & {
  __taliyaSalesLeads?: Map<string, SalesLeadConversation>;
  __taliyaSalesLeadAuditLog?: OperatorActionRecord[];
};

const leads = memoryStore.__taliyaSalesLeads ?? new Map<string, SalesLeadConversation>();
const auditLog = memoryStore.__taliyaSalesLeadAuditLog ?? [];
memoryStore.__taliyaSalesLeads = leads;
memoryStore.__taliyaSalesLeadAuditLog = auditLog;

export async function upsertSalesLead(lead: LeadRecord) {
  const existing = await getSalesLead(lead.leadId);
  const now = new Date().toISOString();

  const next: SalesLeadConversation = {
    ...lead,
    createdAt: existing?.createdAt ?? lead.createdAt,
    updatedAt: now,
    recentMessages: existing?.recentMessages ?? [],
    aiPaused: existing?.aiPaused ?? (lead.status === "human_active" || lead.status === "do_not_contact"),
    followUpAt: existing?.followUpAt,
    lastOperatorActionAt: existing?.lastOperatorActionAt,
    externalSyncStatus: existing?.externalSyncStatus ?? "pending",
    nextAction: runtimeOperatorNextAction(lead) ?? lead.nextAction,
    selectedPainIds: unique([...(existing?.selectedPainIds ?? []), ...lead.selectedPainIds]),
    recommendedAgentIds: mergeRecommendedAgentIds(existing, lead),
    priority: maxPriority(existing?.priority, lead.priority),
    urgency:
      maxPriority(existing?.priority, lead.priority) === "manual" || maxPriority(existing?.priority, lead.priority) === "hot"
        ? "alta"
        : maxPriority(existing?.priority, lead.priority) === "warm"
          ? "media"
          : "baixa",
  };

  if (hasPostgresStorage()) {
    await postgresQuery(
      `INSERT INTO sales_leads (
        lead_id, data, status, priority, channel, conversion_path, selected_plan_id,
        contact_normalized_whatsapp, contact_email, ai_paused, external_sync_status,
        contract_version, created_at, updated_at
      ) VALUES ($1, $2::jsonb, $3, $4, $5, $6, $7, $8, $9, $10, $11, $12, $13, $14)
      ON CONFLICT (lead_id) DO UPDATE SET
        data = EXCLUDED.data,
        status = EXCLUDED.status,
        priority = EXCLUDED.priority,
        channel = EXCLUDED.channel,
        conversion_path = EXCLUDED.conversion_path,
        selected_plan_id = EXCLUDED.selected_plan_id,
        contact_normalized_whatsapp = EXCLUDED.contact_normalized_whatsapp,
        contact_email = EXCLUDED.contact_email,
        ai_paused = EXCLUDED.ai_paused,
        external_sync_status = EXCLUDED.external_sync_status,
        contract_version = EXCLUDED.contract_version,
        updated_at = EXCLUDED.updated_at`,
      [
        next.leadId,
        JSON.stringify(next),
        next.status,
        next.priority,
        next.channel,
        next.conversionPath,
        next.selectedPlanId,
        next.contact.normalizedWhatsapp,
        next.contact.email ? normalizeEmail(next.contact.email) : undefined,
        next.aiPaused,
        next.externalSyncStatus,
        next.qualification.agentRuntimeContractVersion,
        next.createdAt,
        next.updatedAt,
      ],
    );
    await linkRuntimeConversationToLead(next);
  } else {
    leads.set(lead.leadId, next);
  }

  return next;
}

async function linkRuntimeConversationToLead(lead: SalesLeadConversation) {
  const conversationId = lead.channelSessionId || lead.sessionId;
  if (!conversationId) return;

  await postgresQuery(
    `UPDATE agent_runtime_conversations
     SET lead_id = $2,
         channel_conversation_id = COALESCE(channel_conversation_id, $3),
         updated_at = now()
     WHERE id = $1
       AND (lead_id IS NULL OR lead_id = $2)`,
    [conversationId, lead.leadId, lead.channelSessionId],
  );
}

export async function listSalesLeads(filters: {
  status?: LeadStatus;
  priority?: LeadPriority;
  channel?: "web" | "whatsapp";
  conversionPath?: string;
  selectedPlanId?: string;
  nextAction?: string;
} = {}) {
  const values = hasPostgresStorage() ? await listPostgresLeads() : Array.from(leads.values());
  return values
    .filter((lead) => !filters.status || lead.status === filters.status)
    .filter((lead) => !filters.priority || lead.priority === filters.priority)
    .filter((lead) => !filters.channel || lead.channel === filters.channel)
    .filter((lead) => !filters.conversionPath || lead.conversionPath === filters.conversionPath)
    .filter((lead) => !filters.selectedPlanId || lead.selectedPlanId === filters.selectedPlanId)
    .filter((lead) => !filters.nextAction || lead.nextAction.toLowerCase().includes(filters.nextAction.toLowerCase()))
    .sort((a, b) => b.updatedAt.localeCompare(a.updatedAt));
}

export async function getSalesLead(leadId: string) {
  if (hasPostgresStorage()) {
    const result = await postgresQuery<SalesLeadRow>("SELECT * FROM sales_leads WHERE lead_id = $1 LIMIT 1", [leadId]);
    return result.rows[0] ? rowToLead(result.rows[0], await listMessages(leadId)) : null;
  }
  return leads.get(leadId) ?? null;
}

export async function deleteSalesLeadThread(leadId: string) {
  const lead = await getSalesLead(leadId);
  if (!lead) return null;

  const sessionIds = unique(compactStrings([lead.sessionId, lead.channelSessionId]));
  const providerContacts = unique([
    lead.contact.providerContactId,
    lead.contact.whatsapp?.replace(/\D/g, ""),
    lead.contact.normalizedWhatsapp?.replace(/\D/g, ""),
  ].filter((value): value is string => Boolean(value)));

  if (hasPostgresStorage()) {
    await removeRows("sales_lead_messages", "lead_id", [leadId]);
    await removeRows("operator_actions", "lead_id", [leadId]);
    await removeRows("ai_funnel_events", "lead_id", [leadId]);
    await removeRows("ai_funnel_events", "session_id", sessionIds);
    await removeRows("ai_usage_events", "session_id", sessionIds);
    await removeRows("whatsapp_message_outbox", "lead_id", [leadId]);
    await removeRows("whatsapp_message_outbox", "provider_contact_id", providerContacts);
    await removeRows("whatsapp_turn_queue", "channel_session_id", sessionIds);
    await removeRows("whatsapp_turn_queue", "provider_contact_id", providerContacts);
    await removeRows("whatsapp_turn_locks", "channel_session_id", sessionIds);
    await removeRows("whatsapp_provider_messages", "provider_contact_id", providerContacts);
    await removeRows("whatsapp_sessions", "provider_contact_id", providerContacts);
    await removeRows("sales_leads", "lead_id", [leadId]);
  } else {
    leads.delete(leadId);
    for (let index = auditLog.length - 1; index >= 0; index -= 1) {
      if (auditLog[index].leadId === leadId) auditLog.splice(index, 1);
    }
  }

  return {
    leadId,
    sessionIds,
    providerContacts,
  };
}

export async function appendSalesLeadMessage(
  leadId: string,
  message: {
    id: string;
    role: "user" | "assistant" | "system";
    content: string;
    createdAt?: string;
  },
) {
  return appendSalesLeadMessages(leadId, [message]);
}

export async function appendSalesLeadMessages(
  leadId: string,
  messages: Array<{
    id: string;
    role: "user" | "assistant" | "system";
    content: string;
    createdAt?: string;
    conversationId?: string;
    channelSessionId?: string;
    providerMessageId?: string;
    channel?: "web" | "widget" | "whatsapp";
    direction?: "inbound" | "outbound" | "internal";
    messageType?: "text" | "unsupported_media" | "postback" | "system";
    deliveryStatus?: string;
    runId?: string;
    traceId?: string;
    safetyFlags?: string[];
    isSensitive?: boolean;
    unsupportedMedia?: boolean;
    isProblematic?: boolean;
    metadata?: Record<string, unknown>;
  }>,
) {
  const lead = await getSalesLead(leadId);
  if (!lead) return null;

  const safeMessages = messages
    .map((message) => ({
      id: message.id,
      role: message.role,
      content: sanitizeMessageContent(message.content),
      createdAt: message.createdAt ?? new Date().toISOString(),
      conversationId: message.conversationId ?? message.channelSessionId ?? lead.channelSessionId,
      channelSessionId: message.channelSessionId ?? lead.channelSessionId,
      providerMessageId: message.providerMessageId ?? message.id,
      channel: message.channel ?? lead.channel,
      direction: message.direction ?? (message.role === "assistant" ? "outbound" : message.role === "user" ? "inbound" : "internal"),
      messageType: message.messageType ?? (message.role === "system" ? "system" : "text"),
      deliveryStatus: message.deliveryStatus ?? (message.role === "assistant" ? "delivered" : "received"),
      runId: message.runId,
      traceId: message.traceId,
      safetyFlags: message.safetyFlags ?? [],
      isSensitive: message.isSensitive ?? false,
      unsupportedMedia: message.unsupportedMedia ?? false,
      isProblematic: message.isProblematic ?? false,
      metadata: message.metadata ?? {},
    }))
    .filter((message) => message.id && message.content);
  if (!safeMessages.length) return lead;
  const mergedMessages = new Map<string, SalesLeadConversation["recentMessages"][number]>();
  for (const message of lead.recentMessages) mergedMessages.set(message.id, message);
  for (const message of safeMessages) {
    mergedMessages.set(message.id, {
      id: message.id,
      role: message.role,
      content: message.content,
      createdAt: message.createdAt,
    });
  }

  const updated: SalesLeadConversation = {
    ...lead,
    recentMessages: Array.from(mergedMessages.values()).slice(-40),
    updatedAt: new Date().toISOString(),
  };

  if (hasPostgresStorage()) {
    const values: unknown[] = [];
    const rows = safeMessages.map((message, index) => {
      const offset = index * 19;
      values.push(
        message.id, leadId, message.channelSessionId, message.conversationId,
        message.providerMessageId, message.role, message.channel, message.direction,
        message.messageType, message.deliveryStatus, message.runId, message.traceId,
        JSON.stringify(message.safetyFlags), message.isSensitive, message.unsupportedMedia,
        message.isProblematic, message.content, JSON.stringify(message.metadata), message.createdAt,
      );
      return `(${Array.from({ length: 19 }, (_, valueIndex) => `$${offset + valueIndex + 1}`).join(", ")})`;
    });
    await postgresQuery(
      `INSERT INTO sales_lead_messages (
         message_id, lead_id, channel_session_id, conversation_id, provider_message_id,
         role, channel, direction, message_type, delivery_status, run_id, trace_id,
         safety_flags, is_sensitive, unsupported_media, is_problematic,
         safe_content, metadata, created_at
       )
       VALUES ${rows.join(", ")}
       ON CONFLICT (message_id) DO NOTHING`,
      values,
    );
    await postgresQuery(
      "UPDATE sales_leads SET data = $2::jsonb, updated_at = $3 WHERE lead_id = $1",
      [leadId, JSON.stringify(updated), updated.updatedAt],
    );
  } else {
    leads.set(leadId, updated);
  }

  return updated;
}

export async function updateSalesLeadSyncStatus(
  leadId: string,
  externalSyncStatus: SalesLeadConversation["externalSyncStatus"],
  metadata: Record<string, unknown> = {},
) {
  const lead = await getSalesLead(leadId);
  if (!lead) return null;

  const updated: SalesLeadConversation = {
    ...lead,
    externalSyncStatus,
    updatedAt: new Date().toISOString(),
  };

  if (hasPostgresStorage()) {
    await postgresQuery(
      "UPDATE sales_leads SET data = $2::jsonb, external_sync_status = $3, updated_at = $4 WHERE lead_id = $1",
      [leadId, JSON.stringify(updated), externalSyncStatus, updated.updatedAt],
    );
  } else {
    leads.set(leadId, updated);
  }

  if (externalSyncStatus === "failed") {
    await recordOperatorAction({
      actionId: `sync_${Date.now()}`,
      leadId,
      actorUserId: "system:n8n",
      action: "edit_lead_summary",
      payload: sanitizeActionPayload({ syncStatus: externalSyncStatus, ...metadata }),
      beforeStatus: lead.status,
      afterStatus: lead.status,
      createdAt: updated.updatedAt,
    });
  }

  return updated;
}

export async function findSalesLeadForWhatsApp({
  phone,
  providerContactId,
}: {
  phone?: string;
  providerContactId?: string;
}) {
  const normalizedPhone = normalizePhone(phone);
  const providerIdentifier = providerContactId ? `providerContact:${providerContactId}` : undefined;
  const whatsappIdentifier = normalizedPhone ? `whatsapp:${normalizedPhone}` : undefined;
  const allLeads = await listSalesLeads();

  return (
    allLeads.find(
      (lead) =>
        (providerIdentifier && lead.merge.strongIdentifiers.includes(providerIdentifier)) ||
        (whatsappIdentifier && lead.merge.strongIdentifiers.includes(whatsappIdentifier)) ||
        (providerContactId && lead.contact.providerContactId === providerContactId) ||
        (normalizedPhone && lead.contact.normalizedWhatsapp === normalizedPhone),
    ) ?? null
  );
}

export async function findSalesLeadForSession(sessionId: string) {
  if (hasPostgresStorage()) {
    const result = await postgresQuery<SalesLeadRow>(
      "SELECT * FROM sales_leads WHERE data->>'sessionId' = $1 ORDER BY updated_at DESC LIMIT 1",
      [sessionId],
    );
    const row = result.rows[0];
    return row ? rowToLead(row, await listMessages(row.lead_id)) : null;
  }
  const allLeads = await listSalesLeads();
  return allLeads.find((lead) => lead.sessionId === sessionId) ?? null;
}

export async function listOperatorActions(leadId: string) {
  if (hasPostgresStorage()) {
    const result = await postgresQuery<OperatorActionRow>(
      "SELECT * FROM operator_actions WHERE lead_id = $1 ORDER BY created_at DESC",
      [leadId],
    );
    return result.rows.map(rowToAction);
  }
  return auditLog.filter((entry) => entry.leadId === leadId).sort((a, b) => b.createdAt.localeCompare(a.createdAt));
}

export async function applyOperatorAction({
  action,
  actorUserId,
  leadId,
  payload,
}: {
  action: OperatorActionName;
  actorUserId: string;
  leadId: string;
  payload: Record<string, unknown>;
}) {
  const lead = await getSalesLead(leadId);
  if (!lead) return { ok: false as const, reason: "lead_not_found" };
  if (action === "schedule_follow_up") {
    const eligibility = getFollowUpEligibility(lead);
    if (!eligibility.allowed) return { ok: false as const, reason: `follow_up_blocked_${eligibility.reason}` };
  }

  const beforeStatus = lead.status;
  const afterStatus = statusAfterAction(action, beforeStatus);
  const now = new Date().toISOString();
  const updated: SalesLeadConversation = {
    ...lead,
    status: afterStatus,
    aiPaused: action === "take_over" ? true : action === "resume_ai" ? false : action === "mark_do_not_contact" ? true : lead.aiPaused,
    humanActive: action === "take_over" ? true : action === "resume_ai" ? false : lead.humanActive,
    closureState: action === "take_over" ? "human_active" : action === "resume_ai" ? "waiting_user" : lead.closureState,
    followUpAt: action === "schedule_follow_up" && typeof payload.followUpAt === "string" ? payload.followUpAt : lead.followUpAt,
    summary: action === "edit_lead_summary" && typeof payload.summary === "string" ? payload.summary.slice(0, 1200) : lead.summary,
    nextAction:
      action === "take_over"
        ? "Operador assumiu a conversa; IA pausada ate retomada explicita."
        : action === "resume_ai"
          ? "IA reativada por operador; proxima mensagem do lead pode ser respondida automaticamente."
          : lead.nextAction,
    lastOperatorActionAt: now,
    updatedAt: now,
    externalSyncStatus: "pending",
  };

  if (hasPostgresStorage()) {
    await postgresQuery(
      `UPDATE sales_leads
       SET data = $2::jsonb, status = $3, ai_paused = $4, external_sync_status = 'pending', updated_at = $5
       WHERE lead_id = $1`,
      [leadId, JSON.stringify(updated), updated.status, updated.aiPaused, now],
    );
  } else {
    leads.set(leadId, updated);
  }

  const record: OperatorActionRecord = {
    actionId: `action_${Date.now()}_${Math.random().toString(36).slice(2, 8)}`,
    leadId,
    actorUserId,
    action,
    payload: sanitizeActionPayload(payload),
    beforeStatus,
    afterStatus,
    createdAt: now,
  };
  await recordOperatorAction(record);

  return { ok: true as const, lead: updated, action: record };
}

export function isValidOperatorAction(input: string): input is OperatorActionName {
  return (
    input === "take_over" ||
    input === "send_whatsapp_message" ||
    input === "send_plan_page" ||
    input === "send_checkout_link" ||
    input === "schedule_follow_up" ||
    input === "resume_ai" ||
    input === "mark_waiting_customer" ||
    input === "mark_won" ||
    input === "mark_lost" ||
    input === "mark_do_not_contact" ||
    input === "edit_lead_summary"
  );
}

async function listPostgresLeads() {
  const result = await postgresQuery<SalesLeadRow>("SELECT * FROM sales_leads ORDER BY updated_at DESC");
  return result.rows.map((row) => rowToLead(row, []));
}

async function listMessages(leadId: string): Promise<SalesLeadConversation["recentMessages"]> {
  const result = await postgresQuery<SalesLeadMessageRow>(
    "SELECT * FROM sales_lead_messages WHERE lead_id = $1 ORDER BY created_at DESC LIMIT 40",
    [leadId],
  );
  return result.rows
    .reverse()
    .map((row) => ({
      id: row.message_id,
      role: row.role,
      content: row.safe_content,
      createdAt: toIso(row.created_at) ?? new Date().toISOString(),
    }));
}

async function recordOperatorAction(record: OperatorActionRecord) {
  if (hasPostgresStorage()) {
    await postgresQuery(
      `INSERT INTO operator_actions (action_id, lead_id, actor_user_id, action, payload, before_status, after_status, created_at)
       VALUES ($1, $2, $3, $4, $5::jsonb, $6, $7, $8)
       ON CONFLICT (action_id) DO NOTHING`,
      [
        record.actionId,
        record.leadId,
        record.actorUserId,
        record.action,
        JSON.stringify(record.payload),
        record.beforeStatus,
        record.afterStatus,
        record.createdAt,
      ],
    );
  } else {
    auditLog.push(record);
  }
}

function rowToLead(row: SalesLeadRow, messages: SalesLeadConversation["recentMessages"]): SalesLeadConversation {
  const data = isRecord(row.data) ? (row.data as SalesLeadConversation) : undefined;
  if (!data) throw new Error(`Invalid sales lead row data for ${row.lead_id}`);
  return {
    ...data,
    status: row.status as LeadStatus,
    priority: row.priority as LeadPriority,
    aiPaused: row.ai_paused,
    externalSyncStatus: row.external_sync_status,
    recentMessages: messages.length ? messages : data.recentMessages ?? [],
    updatedAt: toIso(row.updated_at) ?? data.updatedAt,
    createdAt: toIso(row.created_at) ?? data.createdAt,
  };
}

function rowToAction(row: OperatorActionRow): OperatorActionRecord {
  return {
    actionId: row.action_id,
    leadId: row.lead_id,
    actorUserId: row.actor_user_id,
    action: row.action as OperatorActionName,
    payload: isRecord(row.payload) ? row.payload : {},
    beforeStatus: row.before_status as LeadStatus,
    afterStatus: row.after_status as LeadStatus,
    createdAt: toIso(row.created_at) ?? new Date().toISOString(),
  };
}

function statusAfterAction(action: OperatorActionName, current: LeadStatus): LeadStatus {
  if (action === "take_over") return "human_active";
  if (action === "send_whatsapp_message" || action === "mark_waiting_customer") return "waiting_customer";
  if (action === "send_checkout_link") return "checkout_sent";
  if (action === "schedule_follow_up") return "follow_up_scheduled";
  if (action === "resume_ai") return "ai_active";
  if (action === "mark_won") return "won";
  if (action === "mark_lost") return "lost";
  if (action === "mark_do_not_contact") return "do_not_contact";
  return current;
}

function runtimeOperatorNextAction(lead: LeadRecord) {
  const cost = lead.agentRuntime?.estimatedCostUsd;
  if (typeof cost === "number" && cost >= 0.15) {
    return "Custo do runtime atingiu o limite duro; IA deve ficar pausada e operador deve revisar.";
  }
  if (lead.agentRuntime?.productSourceWarning) {
    return "Resposta comercial sem versao de product knowledge; operador deve revisar antes de seguir.";
  }
  return undefined;
}

function mergeRecommendedAgentIds(existing: SalesLeadConversation | null, lead: LeadRecord) {
  if (lead.diagnosticStatus !== "completed" && lead.commercialStage.startsWith("diagnostic_")) {
    return [];
  }
  return unique([...(existing?.recommendedAgentIds ?? []), ...lead.recommendedAgentIds]);
}

function maxPriority(current: LeadPriority | undefined, next: LeadPriority): LeadPriority {
  const rank: Record<LeadPriority, number> = { cold: 0, warm: 1, hot: 2, manual: 3 };
  return current && rank[current] > rank[next] ? current : next;
}

function unique(values: string[]) {
  return Array.from(new Set(values.filter(Boolean)));
}

function compactStrings(values: Array<string | undefined>) {
  return values.filter((value): value is string => Boolean(value));
}

async function removeRows(table: string, column: string, values: string[]) {
  if (!values.length) return 0;
  try {
    const result = await postgresQuery(`DELETE FROM ${table} WHERE ${column} = ANY($1::text[])`, [values]);
    return result.rowCount ?? 0;
  } catch (error) {
    if (isRecord(error) && error.code === "42P01") return 0;
    throw error;
  }
}

function sanitizeActionPayload(payload: Record<string, unknown>) {
  const safe: Record<string, unknown> = {};
  for (const [key, value] of Object.entries(payload)) {
    if (/secret|token|password|card|cvv|credential/i.test(key)) continue;
    if (typeof value === "string") {
      safe[key] = value.slice(0, 1200);
    } else if (typeof value === "number" || typeof value === "boolean" || value === null) {
      safe[key] = value;
    }
  }
  return safe;
}

function sanitizeMessageContent(content: string) {
  return content
    .replace(/\b\d{13,19}\b/g, "[numero_sensivel]")
    .replace(/\b\d{3,4}\b(?=.*\b(cvv|cartao|cartoes|codigo|cod)\b)/gi, "[codigo_sensivel]")
    .slice(0, 3800);
}

function normalizePhone(phone?: string) {
  if (!phone) return undefined;
  const digits = phone.replace(/\D/g, "");
  if (!digits) return undefined;
  return digits.startsWith("55") ? `+${digits}` : `+55${digits}`;
}

function normalizeEmail(email: string) {
  return email.trim().toLowerCase();
}

function toIso(value: Date | string | null | undefined) {
  if (!value) return undefined;
  return value instanceof Date ? value.toISOString() : value;
}

function isRecord(input: unknown): input is Record<string, unknown> {
  return typeof input === "object" && input !== null;
}

type SalesLeadRow = {
  lead_id: string;
  data: unknown;
  status: string;
  priority: string;
  ai_paused: boolean;
  external_sync_status: SalesLeadConversation["externalSyncStatus"];
  contract_version?: string | null;
  created_at: Date | string;
  updated_at: Date | string;
};

type SalesLeadMessageRow = {
  message_id: string;
  role: "user" | "assistant" | "system";
  safe_content: string;
  created_at: Date | string;
};

type OperatorActionRow = {
  action_id: string;
  lead_id: string;
  actor_user_id: string;
  action: string;
  payload: unknown;
  before_status: string;
  after_status: string;
  created_at: Date | string;
};
