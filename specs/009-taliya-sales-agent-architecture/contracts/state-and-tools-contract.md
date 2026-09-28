# Contract: State, Substate And Tools

## Conversation State V2

```ts
type MacroState =
  | "new_lead"
  | "open_question"
  | "product_question"
  | "price_or_plan"
  | "diagnostic_offered"
  | "diagnostic_in_progress"
  | "diagnostic_completed"
  | "demo_interest"
  | "waitlist_offered"
  | "waitlist_pending_details"
  | "waitlist_joined"
  | "human_requested"
  | "human_active"
  | "closed";

type ConversationSubstate = {
  askedQuestions: string[];
  knownFacts: Record<string, unknown>;
  pendingQuestion: string | null;
  diagnosticStep: string | null;
  missingFields: string[];
  lastTopic: string | null;
  lastAnsweredDirectQuestion: string | null;
  sentiment: "neutral" | "curious" | "urgent" | "skeptical" | "irritated";
  confidence: "high" | "medium" | "low";
  lastSummary: string | null;
  queuedResponseStatus: "none" | "queued" | "suppressed" | "revalidate_required";
  cost: {
    estimatedConversationCostUsd: number;
    capStatus: "ok" | "review" | "high" | "hard_cap_blocked";
  };
};
```

## Required Tools

### `getProductKnowledge`

Returns official product knowledge with version.

### `interpretLeadMessage`

Extracts primary intent, secondary intents, direct questions, facts, urgency, sentiment, risk and confidence. May use default low-cost path unless escalation is justified.

### `updateLeadFacts`

Persists facts such as reliable name, phone/email, studio details, pain, current workflow, urgency and priority.

### `updateConversationState`

Atomically updates macro state and substate.

### `saveDiagnostic`

Persists diagnostic inputs and outputs. Must reject generic diagnostic completion.

### `markWaitlist`

Creates or updates waitlist status idempotently.

### `pauseForHuman`

Marks `human_requested` or `human_active`, saves summary and suppresses AI replies.

### `resumeFromHuman`

Requires explicit operator action. Revalidates queued state before AI resumes.

### `recordTrace`

Saves agent-loop trace, source versions, guardrails, delivery and cost.

### `recordCostCap`

Marks hard cap, preserves context, assigns human follow-up and blocks further automatic generation.

## Idempotency

Every tool action must receive:

```ts
type ToolActionInput<T> = {
  idempotencyKey: string;
  conversationId: string;
  leadId: string;
  payload: T;
};
```

Same key + same tool must not duplicate side effects.

## Atomicity Requirements

Atomic update required for:

- diagnostic completion
- waitlist offer/join/remove
- human handoff/pause/resume
- cost hard-cap block
- duplicate identity association

## Guarded Transitions

- `human_active` blocks automatic AI response.
- `waitlist_joined` must not return to `diagnostic_in_progress` unless the lead explicitly requests a new diagnostic.
- `closed` may reopen if lead returns with a new commercial message.
- `price_or_plan` can be a temporary state and then return to the prior diagnostic/waitlist context.
