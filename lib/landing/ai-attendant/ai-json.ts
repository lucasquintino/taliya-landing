const DEFAULT_JSON_MODEL = "gpt-5-mini";
const DEFAULT_TIMEOUT_MS = 8000;

export type AiJsonResult<T> =
  | {
      ok: true;
      value: T;
      usage?: {
        inputTokens?: number;
        outputTokens?: number;
      };
      latencyMs: number;
    }
  | {
      ok: false;
      reason: "missing_api_key" | "timeout" | "provider_error" | "invalid_output";
      detail?: string;
      latencyMs: number;
    };

export async function callAiJson<T>({
  name,
  system,
  user,
  schema,
  timeoutMs = DEFAULT_TIMEOUT_MS,
}: {
  name: string;
  system: string;
  user: unknown;
  schema: object;
  timeoutMs?: number;
}): Promise<AiJsonResult<T>> {
  const startedAt = Date.now();
  const apiKey = process.env.OPENAI_API_KEY;
  if (isMockProviderEnabled() || !apiKey) {
    return {
      ok: false,
      reason: "missing_api_key",
      detail: "OPENAI_API_KEY is not configured or mock provider is enabled.",
      latencyMs: Date.now() - startedAt,
    };
  }

  const controller = new AbortController();
  const timeout = setTimeout(() => controller.abort(), timeoutMs);

  try {
    const response = await fetch("https://api.openai.com/v1/responses", {
      method: "POST",
      headers: {
        authorization: `Bearer ${apiKey}`,
        "content-type": "application/json",
      },
      body: JSON.stringify({
        model: process.env.AI_ATTENDANT_JSON_MODEL || DEFAULT_JSON_MODEL,
        input: [
          { role: "system", content: system },
          { role: "user", content: JSON.stringify(user) },
        ],
        text: {
          format: {
            type: "json_schema",
            name,
            strict: false,
            schema,
          },
        },
      }),
      signal: controller.signal,
    });

    if (!response.ok) {
      return {
        ok: false,
        reason: "provider_error",
        detail: await safeReadText(response),
        latencyMs: Date.now() - startedAt,
      };
    }

    const payload = (await response.json()) as Record<string, unknown>;
    const outputText = extractOutputText(payload);
    const parsed = safeParseJson(outputText);
    if (parsed === null) {
      return {
        ok: false,
        reason: "invalid_output",
        detail: "Provider response did not include valid JSON.",
        latencyMs: Date.now() - startedAt,
      };
    }

    return {
      ok: true,
      value: parsed as T,
      usage: extractUsage(payload),
      latencyMs: Date.now() - startedAt,
    };
  } catch (error) {
    return {
      ok: false,
      reason: error instanceof DOMException && error.name === "AbortError" ? "timeout" : "provider_error",
      detail: error instanceof Error ? error.message : "Unknown provider error.",
      latencyMs: Date.now() - startedAt,
    };
  } finally {
    clearTimeout(timeout);
  }
}

export function isMockProviderEnabled() {
  return (
    process.env.AI_ATTENDANT_PROVIDER === "mock" ||
    process.env.AI_ATTENDANT_MOCK_PROVIDER === "1" ||
    process.env.OPENAI_API_KEY === "mock"
  );
}

function extractOutputText(payload: Record<string, unknown>): string {
  if (typeof payload.output_text === "string") return payload.output_text;
  if (!Array.isArray(payload.output)) return "";

  for (const item of payload.output) {
    if (!isRecord(item) || !Array.isArray(item.content)) continue;
    for (const content of item.content) {
      if (!isRecord(content)) continue;
      if (typeof content.text === "string") return content.text;
      if (typeof content.output_text === "string") return content.output_text;
    }
  }

  return "";
}

function extractUsage(payload: Record<string, unknown>): { inputTokens?: number; outputTokens?: number } | undefined {
  if (!isRecord(payload.usage)) return undefined;
  return {
    inputTokens: typeof payload.usage.input_tokens === "number" ? payload.usage.input_tokens : undefined,
    outputTokens: typeof payload.usage.output_tokens === "number" ? payload.usage.output_tokens : undefined,
  };
}

function safeParseJson(text: string): unknown {
  try {
    return JSON.parse(text);
  } catch {
    return null;
  }
}

async function safeReadText(response: Response) {
  try {
    return (await response.text()).slice(0, 500);
  } catch {
    return "Unable to read provider error.";
  }
}

function isRecord(input: unknown): input is Record<string, unknown> {
  return typeof input === "object" && input !== null;
}
