import { aiAttendantResponseJsonSchema, normalizeAiAttendantResponse } from "./schema";
import type { AiAttendantRequest, AiAttendantResponse } from "./schema";
import type { AiAttendantContext } from "./context";
import { createGuidedFallbackTurn } from "./fallback";

export type AiProviderResult =
  | {
      ok: true;
      response: AiAttendantResponse;
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

const DEFAULT_MODEL = "gpt-5.4-mini";
const PROVIDER_TIMEOUT_MS = 12000;

export async function callAiProvider(request: AiAttendantRequest, context: AiAttendantContext): Promise<AiProviderResult> {
  const startedAt = Date.now();
  const apiKey = process.env.OPENAI_API_KEY;
  const model = process.env.AI_ATTENDANT_MODEL || DEFAULT_MODEL;

  if (isMockProviderEnabled()) {
    return {
      ok: true,
      response: createGuidedFallbackTurn(context.nicheConfig, request, {
        category: "allowed",
        action: "respond",
        reason: "Deterministic mock provider for route-matrix validation.",
      }),
      usage: {
        inputTokens: 0,
        outputTokens: 0,
      },
      latencyMs: Date.now() - startedAt,
    };
  }

  if (!apiKey) {
    return {
      ok: false,
      reason: "missing_api_key",
      detail: "OPENAI_API_KEY is not configured.",
      latencyMs: Date.now() - startedAt,
    };
  }

  const controller = new AbortController();
  const timeout = setTimeout(() => controller.abort(), PROVIDER_TIMEOUT_MS);

  try {
    const response = await fetch("https://api.openai.com/v1/responses", {
      method: "POST",
      headers: {
        authorization: `Bearer ${apiKey}`,
        "content-type": "application/json",
      },
      body: JSON.stringify({
        model,
        input: [
          {
            role: "system",
            content: context.instructions,
          },
          {
            role: "user",
            content: JSON.stringify({
              userMessage: request.userMessage,
              quickReplyId: request.quickReplyId,
              channel: request.session.channel,
              recentMessages: request.session.messages.slice(-5).map((message) => ({
                role: message.role,
                content: message.content,
              })),
              selectedPainIds: request.session.selectedPainIds ?? [],
              recommendedAgentIds: request.session.recommendedAgentIds ?? [],
              qualificationDraft: compactQualificationDraft(request.session.qualificationDraft),
              pageSignals: request.pageSignals ?? {},
              commercialFacts: context.commercialFacts,
            }),
          },
        ],
        text: {
          format: {
            type: "json_schema",
            name: "ai_attendant_response",
            strict: false,
            schema: aiAttendantResponseJsonSchema,
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
    if (!outputText) {
      return {
        ok: false,
        reason: "invalid_output",
        detail: "Provider response did not include output text.",
        latencyMs: Date.now() - startedAt,
      };
    }

    const parsed = safeParseJson(outputText);
    const normalized = normalizeAiAttendantResponse(parsed);
    if (!normalized) {
      return {
        ok: false,
        reason: "invalid_output",
        detail: "Provider response did not match the attendant schema.",
        latencyMs: Date.now() - startedAt,
      };
    }

    return {
      ok: true,
      response: normalized,
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

function isMockProviderEnabled() {
  return (
    process.env.AI_ATTENDANT_PROVIDER === "mock" ||
    process.env.AI_ATTENDANT_MOCK_PROVIDER === "1" ||
    process.env.OPENAI_API_KEY === "mock"
  );
}

function extractOutputText(payload: Record<string, unknown>): string | null {
  if (typeof payload.output_text === "string") return payload.output_text;
  if (!Array.isArray(payload.output)) return null;

  for (const item of payload.output) {
    if (!isRecord(item) || !Array.isArray(item.content)) continue;
    for (const content of item.content) {
      if (!isRecord(content)) continue;
      if (typeof content.text === "string") return content.text;
      if (typeof content.output_text === "string") return content.output_text;
    }
  }

  return null;
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

function compactQualificationDraft(draft: AiAttendantRequest["session"]["qualificationDraft"]) {
  if (!draft) return {};
  return {
    name: draft.name,
    contactCaptureStatus: draft.contactCaptureStatus,
    activeStudentsRange: draft.activeStudentsRange,
    studioSizeRange: draft.studioSizeRange,
    operationalPains: draft.operationalPains,
    dailyVisibility: draft.dailyVisibility,
    replacementComplexity: draft.replacementComplexity,
    salesFollowupMaturity: draft.salesFollowupMaturity,
    currentSystem: draft.currentSystem,
    priorityGoal: draft.priorityGoal,
    buyingTiming: draft.buyingTiming,
    diagnosticType: draft.diagnosticType,
    diagnosticCompleted: draft.diagnosticCompleted,
    diagnosticCancelled: draft.diagnosticCancelled,
    recommendedPlan: draft.recommendedPlan,
    recommendedAgents: draft.recommendedAgents,
  };
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
