import type { AgentV2ConversationState } from "./agent-v2-types";
import { hasPostgresStorage, postgresQuery } from "./storage/postgres";

const memoryStates = new Map<string, AgentV2ConversationState>();

export async function loadAgentV2State(conversationId: string) {
  if (hasPostgresStorage()) {
    const result = await postgresQuery<{ payload: unknown }>(
      "SELECT payload FROM agent_v2_conversation_states WHERE conversation_id = $1 LIMIT 1",
      [conversationId],
    );
    const payload = result.rows[0]?.payload;
    return isRecord(payload) ? (payload as AgentV2ConversationState) : null;
  }
  return memoryStates.get(conversationId) ?? null;
}

export async function saveAgentV2State(state: AgentV2ConversationState) {
  const next = {
    ...state,
    updatedAt: new Date().toISOString(),
  };
  if (hasPostgresStorage()) {
    await postgresQuery(
      `INSERT INTO agent_v2_conversation_states (
        conversation_id, lead_id, channel, macro_state, priority, human_status, payload, updated_at
      ) VALUES ($1, $2, $3, $4, $5, $6, $7::jsonb, now())
      ON CONFLICT (conversation_id) DO UPDATE SET
        lead_id = EXCLUDED.lead_id,
        channel = EXCLUDED.channel,
        macro_state = EXCLUDED.macro_state,
        priority = EXCLUDED.priority,
        human_status = EXCLUDED.human_status,
        payload = EXCLUDED.payload,
        updated_at = now()`,
      [next.conversationId, next.leadId, next.channel, next.macroState, next.priority, next.humanStatus, JSON.stringify(next)],
    );
  } else {
    memoryStates.set(next.conversationId, next);
  }
  return next;
}

function isRecord(input: unknown): input is Record<string, unknown> {
  return typeof input === "object" && input !== null;
}

