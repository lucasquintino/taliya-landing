import { randomUUID } from "crypto";
import type { AgentV2Trace } from "./agent-v2-types";
import { hasPostgresStorage, postgresQuery } from "./storage/postgres";

const memoryTraces = new Map<string, AgentV2Trace>();

export function createTraceId() {
  return `trace_${randomUUID()}`;
}

export async function recordAgentV2Trace(trace: AgentV2Trace) {
  if (hasPostgresStorage()) {
    await postgresQuery(
      `INSERT INTO agent_v2_traces (
        trace_id, lead_id, conversation_id, turn_id, channel, product_source_version,
        payload, cost_estimate_usd, created_at
      ) VALUES ($1, $2, $3, $4, $5, $6, $7::jsonb, $8, $9)
      ON CONFLICT (trace_id) DO UPDATE SET payload = EXCLUDED.payload`,
      [
        trace.id,
        trace.leadId,
        trace.conversationId,
        trace.turnId,
        trace.channel,
        trace.productSourceVersion,
        JSON.stringify(sanitizeTrace(trace)),
        trace.costEstimateUsd,
        trace.createdAt,
      ],
    );
  } else {
    memoryTraces.set(trace.id, sanitizeTrace(trace));
  }
  return trace;
}

export async function listAgentV2TracesForLead(leadId: string, limit = 5) {
  if (hasPostgresStorage()) {
    const result = await postgresQuery<{ payload: unknown }>(
      "SELECT payload FROM agent_v2_traces WHERE lead_id = $1 ORDER BY created_at DESC LIMIT $2",
      [leadId, limit],
    );
    return result.rows.flatMap((row) => (isRecord(row.payload) ? [row.payload as AgentV2Trace] : []));
  }
  return Array.from(memoryTraces.values()).filter((trace) => trace.leadId === leadId).slice(-limit).reverse();
}

function sanitizeTrace(trace: AgentV2Trace): AgentV2Trace {
  return {
    ...trace,
    normalizedInput: redact(trace.normalizedInput),
    responseDraft: redact(trace.responseDraft),
    validatedResponse: redact(trace.validatedResponse),
  };
}

function redact(input: unknown): unknown {
  if (typeof input === "string") {
    return input
      .replace(/\b\d{11}\b/g, "[cpf_redacted]")
      .replace(/\b\d{13,19}\b/g, "[number_redacted]")
      .slice(0, 4000);
  }
  if (Array.isArray(input)) return input.map(redact);
  if (!isRecord(input)) return input;
  return Object.fromEntries(Object.entries(input).map(([key, value]) => [/token|secret|password|credential/i.test(key) ? [key, "[redacted]"] : [key, redact(value)]]));
}

function isRecord(input: unknown): input is Record<string, unknown> {
  return typeof input === "object" && input !== null;
}

