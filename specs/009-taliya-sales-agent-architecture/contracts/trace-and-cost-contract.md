# Contract: Trace And Cost

## Trace Record

Every meaningful AI turn must create a trace record.

```ts
type AgentTrace = {
  id: string;
  leadId: string;
  conversationId: string;
  turnId: string;
  channel: "widget" | "whatsapp";
  normalizedInput: unknown;
  stateBefore: unknown;
  productSourceVersion?: string;
  semanticInterpretation?: unknown;
  orchestrationDecision?: unknown;
  toolActions: Array<{
    toolName: string;
    idempotencyKey: string;
    status: "pending" | "succeeded" | "failed" | "skipped";
  }>;
  guardrailResult: {
    status: "passed" | "blocked" | "modified";
    reasons: string[];
  };
  responseDraft?: unknown;
  validatedResponse?: unknown;
  stateAfter?: unknown;
  deliveryResult?: unknown;
  modelUsage: ModelUsageRecord[];
  costEstimateUsd: number;
  fallbackReason?: string;
  createdAt: string;
};
```

## Model Usage Record

```ts
type ModelUsageRecord = {
  operation: "interpretation" | "generation" | "judge" | "summary" | "recovery";
  model: string;
  inputTokens?: number;
  outputTokens?: number;
  estimatedCostUsd: number;
  budgetCategory:
    | "simple_answer"
    | "medium_qualified_lead"
    | "diagnostic_lead"
    | "long_complex_lead"
    | "evaluation_run";
  escalationReason?: string;
};
```

## Cost Policy

- Simple answer target: under US$0.005.
- Medium qualified lead target: under US$0.03 where possible.
- Review threshold: above US$0.05 for a medium lead.
- High-cost threshold: above US$0.10.
- Hard cap: at or above US$0.15 per lead conversation.

## Eval Run Budget Policy

Eval runs are separate from per-lead runtime caps. They must still be bounded:

- dry-run should be available for fixture validation with no model calls;
- max scenarios, max real-model calls and max estimated cost must be configurable;
- skipped scenarios must be reported separately and cannot count as passed.

## Hard Cap Behavior

When the conversation reaches or is projected to exceed US$0.15:

1. Stop automatic AI generation.
2. Preserve state, substate, summary and last unanswered question.
3. Log the cap event and model usage.
4. Mark lead for human/operator follow-up.
5. Send only the approved fallback if a reply is needed:

```txt
Vou deixar o que você já contou salvo por aqui.

Para não te responder de qualquer jeito, vamos retornar assim que possível.
```

## Sales Inbox Visibility

Sales Inbox must show:

- priority
- macro state
- waitlist status
- diagnostic summary
- next action
- human handoff status
- estimated conversation cost
- last trace or trace summary
- source/channel
- possible duplicate flags

## Blocking Failures

- Cost cap ignored.
- Stronger model escalation without logged reason.
- Product answer without source version.
- Guardrail block without logged reason.
- Trace missing adapter, interpretation, orchestration, tool/source, guardrail or delivery result.
