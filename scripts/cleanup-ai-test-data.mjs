#!/usr/bin/env node

import { Pool } from "pg";

const sessionArg = arg("session");
const phoneArg = normalizePhone(arg("phone"));
const providerContactArg = normalizePhone(arg("provider-contact"));
const confirm = process.argv.includes("--confirm");

if (!process.env.DATABASE_URL) {
  console.error("DATABASE_URL is required.");
  process.exit(1);
}

if (!sessionArg && !phoneArg && !providerContactArg) {
  console.error("Provide at least one scoped selector: --session=..., --phone=... or --provider-contact=...");
  process.exit(1);
}

const pool = new Pool({
  connectionString: process.env.DATABASE_URL,
  max: 1,
  ssl: process.env.DATABASE_SSL === "true" ? { rejectUnauthorized: false } : undefined,
});

try {
  const scope = await resolveScope();
  const report = confirm ? await deleteScope(scope) : await previewScope(scope);
  console.log(JSON.stringify({ mode: confirm ? "deleted" : "dry-run", scope, report }, null, 2));
  if (!confirm) console.log("Run again with --confirm to delete only the scoped rows above.");
} finally {
  await pool.end();
}

async function resolveScope() {
  const sessionIds = new Set(sessionArg ? [sessionArg] : []);
  const providerContacts = new Set(providerContactArg ? [providerContactArg] : []);
  const phones = new Set(phoneArg ? phoneVariants(phoneArg) : []);
  const leadIds = new Set();

  if (phones.size || providerContacts.size || sessionIds.size) {
    const leads = await pool.query(
      `
        SELECT lead_id, data, contact_normalized_whatsapp
        FROM sales_leads
        WHERE
          ($1::text IS NOT NULL AND data->>'sessionId' = $1)
          OR ($2::text IS NOT NULL AND contact_normalized_whatsapp = $2)
          OR ($3::text IS NOT NULL AND data->'contact'->>'providerContactId' = $3)
      `,
      [sessionArg ?? null, phoneArg ?? null, providerContactArg ?? null],
    );

    for (const row of leads.rows) {
      leadIds.add(row.lead_id);
      if (row.data?.sessionId) sessionIds.add(row.data.sessionId);
      if (row.data?.contact?.providerContactId) providerContacts.add(normalizePhone(row.data.contact.providerContactId) ?? row.data.contact.providerContactId);
      if (row.contact_normalized_whatsapp) phones.add(row.contact_normalized_whatsapp);
    }
  }

  if (phones.size || providerContacts.size || sessionIds.size) {
    const sessions = await pool.query(
      `
        SELECT channel_session_id, provider_contact_id, phone_normalized
        FROM whatsapp_sessions
        WHERE
          ($1::text IS NOT NULL AND channel_session_id = $1)
          OR ($2::text IS NOT NULL AND phone_normalized = $2)
          OR ($3::text IS NOT NULL AND provider_contact_id = $3)
      `,
      [sessionArg ?? null, phoneArg ?? null, providerContactArg ?? null],
    );

    for (const row of sessions.rows) {
      sessionIds.add(row.channel_session_id);
      providerContacts.add(row.provider_contact_id);
      if (row.phone_normalized) phones.add(row.phone_normalized);
    }
  }

  return {
    leadIds: [...leadIds],
    sessionIds: [...sessionIds],
    providerContacts: [...providerContacts],
    phones: [...phones],
  };
}

function phoneVariants(value) {
  const normalized = normalizePhone(value);
  if (!normalized) return [];
  return [normalized, `+${normalized}`];
}

async function previewScope(scope) {
  return {
    salesLeadMessages: await count("sales_lead_messages", "lead_id", scope.leadIds),
    operatorActions: await count("operator_actions", "lead_id", scope.leadIds),
    funnelEventsByLead: await count("ai_funnel_events", "lead_id", scope.leadIds),
    funnelEventsBySession: await count("ai_funnel_events", "session_id", scope.sessionIds),
    usageEvents: await count("ai_usage_events", "session_id", scope.sessionIds),
    outboxByLead: await count("whatsapp_message_outbox", "lead_id", scope.leadIds),
    outboxByContact: await count("whatsapp_message_outbox", "provider_contact_id", scope.providerContacts),
    whatsappTurnQueueBySession: await count("whatsapp_turn_queue", "channel_session_id", scope.sessionIds),
    whatsappTurnQueueByContact: await count("whatsapp_turn_queue", "provider_contact_id", scope.providerContacts),
    whatsappTurnLocks: await count("whatsapp_turn_locks", "channel_session_id", scope.sessionIds),
    providerMessages: await count("whatsapp_provider_messages", "provider_contact_id", scope.providerContacts),
    whatsappSessions: await count("whatsapp_sessions", "provider_contact_id", scope.providerContacts),
    salesLeads: await count("sales_leads", "lead_id", scope.leadIds),
  };
}

async function deleteScope(scope) {
  const report = {};
  report.salesLeadMessages = await remove("sales_lead_messages", "lead_id", scope.leadIds);
  report.operatorActions = await remove("operator_actions", "lead_id", scope.leadIds);
  report.funnelEventsByLead = await remove("ai_funnel_events", "lead_id", scope.leadIds);
  report.funnelEventsBySession = await remove("ai_funnel_events", "session_id", scope.sessionIds);
  report.usageEvents = await remove("ai_usage_events", "session_id", scope.sessionIds);
  report.outboxByLead = await remove("whatsapp_message_outbox", "lead_id", scope.leadIds);
  report.outboxByContact = await remove("whatsapp_message_outbox", "provider_contact_id", scope.providerContacts);
  report.whatsappTurnQueueBySession = await remove("whatsapp_turn_queue", "channel_session_id", scope.sessionIds);
  report.whatsappTurnQueueByContact = await remove("whatsapp_turn_queue", "provider_contact_id", scope.providerContacts);
  report.whatsappTurnLocks = await remove("whatsapp_turn_locks", "channel_session_id", scope.sessionIds);
  report.providerMessages = await remove("whatsapp_provider_messages", "provider_contact_id", scope.providerContacts);
  report.whatsappSessions = await remove("whatsapp_sessions", "provider_contact_id", scope.providerContacts);
  report.salesLeads = await remove("sales_leads", "lead_id", scope.leadIds);
  return report;
}

async function count(table, column, values) {
  if (!values.length) return 0;
  try {
    const result = await pool.query(`SELECT count(*)::int AS count FROM ${table} WHERE ${column} = ANY($1::text[])`, [values]);
    return result.rows[0]?.count ?? 0;
  } catch (error) {
    if (error?.code === "42P01") return 0;
    throw error;
  }
}

async function remove(table, column, values) {
  if (!values.length) return 0;
  try {
    const result = await pool.query(`DELETE FROM ${table} WHERE ${column} = ANY($1::text[])`, [values]);
    return result.rowCount ?? 0;
  } catch (error) {
    if (error?.code === "42P01") return 0;
    throw error;
  }
}

function arg(name) {
  const prefix = `--${name}=`;
  return process.argv.find((item) => item.startsWith(prefix))?.slice(prefix.length);
}

function normalizePhone(value) {
  if (!value) return undefined;
  const digits = value.replace(/\D/g, "");
  return digits || undefined;
}
