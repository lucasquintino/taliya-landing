import type { AiAttendantChannel, GuardrailCategory } from "./schema";
import { hasPostgresStorage, postgresQuery } from "./storage/postgres";

type UsageRecord = {
  id: string;
  sessionId: string;
  channel: AiAttendantChannel;
  niche: string;
  provider: "openai" | "meta_whatsapp_cloud_api" | "internal";
  model?: string;
  status: "success" | "fallback" | "guardrail_blocked" | "timeout" | "provider_error" | "rate_limited" | "skipped";
  latencyMs?: number;
  inputTokenCount?: number;
  outputTokenCount?: number;
  fallbackOrGuardrailCategory?: GuardrailCategory;
  idempotencyKey?: string;
  createdAt: string;
};

const sessionHits = new Map<string, number[]>();
const dailyHits = new Map<string, number>();
const usageEvents: UsageRecord[] = [];

const DEFAULT_PER_SESSION_LIMIT = 45;
const DEFAULT_DAILY_LIMIT = 1500;
const WINDOW_MS = 60_000;

export function isAiAttendantDisabled() {
  return process.env.AI_ATTENDANT_DISABLED === "1" || process.env.AI_ATTENDANT_DISABLED === "true";
}

export async function checkRateLimit({
  channel,
  niche,
  sessionId,
}: {
  channel: AiAttendantChannel;
  niche: string;
  sessionId: string;
}) {
  const perSessionLimit = numberFromEnv(channel === "whatsapp" ? "AI_ATTENDANT_WHATSAPP_RATE_LIMIT_PER_MINUTE" : "AI_ATTENDANT_WEB_RATE_LIMIT_PER_MINUTE", DEFAULT_PER_SESSION_LIMIT);
  const dailyLimit = numberFromEnv("AI_ATTENDANT_DAILY_REQUEST_CAP", DEFAULT_DAILY_LIMIT);
  const now = Date.now();

  if (hasPostgresStorage()) {
    const sessionResult = await incrementPostgresCounter({
      key: `${channel}:${sessionId}:${Math.floor(now / WINDOW_MS)}`,
      scope: "session",
      windowMs: WINDOW_MS,
    });
    if (sessionResult > perSessionLimit) {
      return { allowed: false, reason: "per_session_rate_limit" };
    }

    const day = new Date().toISOString().slice(0, 10);
    const dailyResult = await incrementPostgresCounter({
      key: `${niche}:${day}`,
      scope: "niche_daily",
      windowMs: 24 * 60 * 60 * 1000,
    });
    if (dailyResult > dailyLimit) {
      return { allowed: false, reason: "daily_cap" };
    }
    return { allowed: true };
  }

  const key = `${channel}:${sessionId}`;
  const recent = (sessionHits.get(key) ?? []).filter((timestamp) => now - timestamp < WINDOW_MS);

  if (recent.length >= perSessionLimit) {
    return { allowed: false, reason: "per_session_rate_limit" };
  }

  const dailyKey = `${niche}:${new Date().toISOString().slice(0, 10)}`;
  const todayCount = dailyHits.get(dailyKey) ?? 0;
  if (todayCount >= dailyLimit) {
    return { allowed: false, reason: "daily_cap" };
  }

  recent.push(now);
  sessionHits.set(key, recent);
  dailyHits.set(dailyKey, todayCount + 1);
  return { allowed: true };
}

export async function logAiUsageEvent(event: Omit<UsageRecord, "id" | "createdAt">) {
  const record: UsageRecord = {
    id: `usage_${Date.now()}_${usageEvents.length}`,
    createdAt: new Date().toISOString(),
    ...event,
  };
  usageEvents.push(record);
  if (usageEvents.length > 1000) usageEvents.splice(0, usageEvents.length - 1000);

  if (process.env.NODE_ENV !== "test") {
    console.log("[ai-attendant:usage]", record);
  }

  if (hasPostgresStorage()) {
    await postgresQuery(
      `INSERT INTO ai_usage_events (
        usage_id, session_id, channel, niche, provider, model, status, latency_ms,
        input_token_count, output_token_count, fallback_or_guardrail_category,
        idempotency_key, created_at
      ) VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9, $10, $11, $12, $13)
      ON CONFLICT (usage_id) DO NOTHING`,
      [
        record.id,
        record.sessionId,
        record.channel,
        record.niche,
        record.provider,
        record.model,
        record.status,
        record.latencyMs,
        record.inputTokenCount,
        record.outputTokenCount,
        record.fallbackOrGuardrailCategory,
        record.idempotencyKey,
        record.createdAt,
      ],
    );
  }

  return record;
}

async function incrementPostgresCounter({
  key,
  scope,
  windowMs,
}: {
  key: string;
  scope: "session" | "whatsapp_contact" | "niche_daily";
  windowMs: number;
}) {
  const windowStart = new Date();
  const expiresAt = new Date(Date.now() + windowMs);
  const result = await postgresQuery<{ count: number }>(
    `INSERT INTO rate_limit_counters (counter_key, scope, count, window_start, expires_at, updated_at)
     VALUES ($1, $2, 1, $3, $4, now())
     ON CONFLICT (counter_key) DO UPDATE SET
       count = rate_limit_counters.count + 1,
       expires_at = EXCLUDED.expires_at,
       updated_at = now()
     RETURNING count`,
    [key, scope, windowStart, expiresAt],
  );
  await postgresQuery("DELETE FROM rate_limit_counters WHERE expires_at < now()");
  return result.rows[0]?.count ?? 1;
}

function numberFromEnv(key: string, fallback: number) {
  const value = Number(process.env[key]);
  return Number.isFinite(value) && value > 0 ? value : fallback;
}
