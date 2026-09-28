import { hasPostgresStorage, postgresQuery } from "./storage/postgres";

const memoryKeys = new Set<string>();

export function createInboundIdempotencyKey({
  channel,
  conversationId,
  externalMessageId,
  text,
}: {
  channel: string;
  conversationId: string;
  externalMessageId?: string;
  text?: string;
}) {
  if (externalMessageId) return `${channel}:inbound:${externalMessageId}`;
  return `${channel}:inbound:${conversationId}:${hash(`${text ?? ""}`)}`;
}

export function createToolIdempotencyKey({
  conversationId,
  turnId,
  toolName,
}: {
  conversationId: string;
  turnId: string;
  toolName: string;
}) {
  return `tool:${conversationId}:${turnId}:${toolName}`;
}

export async function reserveAgentV2IdempotencyKey(key: string, scope: string) {
  if (hasPostgresStorage()) {
    const inserted = await postgresQuery<{ idempotency_key: string }>(
      `INSERT INTO agent_v2_idempotency (idempotency_key, scope, status, created_at, updated_at)
       VALUES ($1, $2, 'processing', now(), now())
       ON CONFLICT (idempotency_key) DO NOTHING
       RETURNING idempotency_key`,
      [key, scope],
    );
    return { duplicate: inserted.rows.length === 0 };
  }

  if (memoryKeys.has(key)) return { duplicate: true };
  memoryKeys.add(key);
  return { duplicate: false };
}

export async function completeAgentV2IdempotencyKey(key: string, status: "processed" | "skipped" | "failed" = "processed") {
  if (!hasPostgresStorage()) return;
  await postgresQuery(
    "UPDATE agent_v2_idempotency SET status = $2, updated_at = now() WHERE idempotency_key = $1",
    [key, status],
  );
}

function hash(value: string) {
  let output = 0;
  for (let index = 0; index < value.length; index += 1) {
    output = (output << 5) - output + value.charCodeAt(index);
    output |= 0;
  }
  return Math.abs(output).toString(36);
}

