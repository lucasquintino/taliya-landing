# Contract: Agent Loop

## Purpose

Define the required sequence for every inbound lead event. Channel routes may adapt transport, but they must not bypass the shared agent loop for commercial reasoning.

## Loop Steps

1. Normalize channel input.
2. Deduplicate by stable event/message id.
3. Load lead, conversation, macro state and substate.
4. Enforce pause/cost/abuse pre-checks.
5. Retrieve official product knowledge when commercial facts may be needed.
6. Interpret semantics: intent, facts, direct questions, urgency, sentiment, risk and confidence.
7. Orchestrate the next action and tool plan.
8. Validate planned tools against deterministic guardrails.
9. Execute idempotent tool actions.
10. Generate response from selected action, compact state and official facts.
11. Validate response against hard guardrails.
12. Persist state, substate, trace, cost and intended delivery.
13. Deliver through channel adapter.
14. Record delivery result.

## Input

```ts
type AgentLoopInput = {
  channel: "widget" | "whatsapp";
  source: "direct" | "site" | "instagram" | "facebook" | "ad" | "unknown";
  conversationId?: string;
  leadId?: string;
  externalMessageId?: string;
  idempotencyKey: string;
  text?: string;
  media?: {
    type: "audio" | "image" | "document" | "unknown";
    providerId?: string;
  };
  channelMetadata: {
    phoneNumberId?: string;
    whatsappFrom?: string;
    whatsappProfileName?: string;
    widgetSessionId?: string;
    pagePath?: string;
    entryIntent?: string;
  };
  receivedAt: string;
};
```

## Output

```ts
type AgentLoopOutput = {
  processed: boolean;
  duplicate: boolean;
  leadId?: string;
  conversationId?: string;
  stateBefore?: ConversationStateV2;
  stateAfter?: ConversationStateV2;
  delivery?: ChannelDeliveryPlan;
  traceId?: string;
  costEstimateUsd?: number;
  blockedReason?: string;
};
```

## Required Behavior

- Duplicate input must return `processed: true`, `duplicate: true` and must not create a duplicate reply.
- If `human_active`, record inbound message but do not call AI generation.
- If cost hard cap is reached or projected, do not call response generation; preserve state and use approved fallback only when needed.
- Every response must be generated after orchestration and guardrail validation, never directly inside a channel adapter.

## Blocking Failures

- Channel adapter answers a commercial question directly.
- Response is delivered before persistence/trace.
- Direct question is steered away without answer.
- AI replies while human is active.
- Cost cap is ignored.
