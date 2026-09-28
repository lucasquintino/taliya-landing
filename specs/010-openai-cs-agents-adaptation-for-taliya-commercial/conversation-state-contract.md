# Conversation State Contract: Taliya Commercial Agent

**Status**: Binding for implementation.  
**Scope**: Taliya-owned commercial widget and Taliya-owned WhatsApp number only.

## Purpose

Conversation states control the commercial journey. They do not replace the LLM. The LLM must still interpret the user's message, choose the appropriate behavior, select templates, extract facts, and propose the next state. Validators enforce that the proposed transition is allowed.

## Canonical States

| State | Meaning | Allowed Next States | Tendency |
|-------|---------|---------------------|----------|
| `new_lead` | No meaningful lead message processed yet. | `greeting_only`, `general_interest`, `source_instagram`, `diagnostic_requested`, `pain_detected`, `product_question`, `human_requested`, `out_of_scope`, `safety_blocked` | Move to the most specific opening state. |
| `greeting_only` | Lead only greeted or asked "tudo bem". | `general_interest`, `product_question`, `pain_detected`, `diagnostic_requested`, `human_requested`, `out_of_scope` | Ask broad help question; do not offer diagnostic yet. |
| `general_interest` | Lead wants to know more but has not shared enough pain/context. | `diagnostic_offered`, `product_question`, `pain_detected`, `diagnostic_requested`, `human_requested` | Give short overview and softly offer diagnostic if useful. |
| `source_instagram` | Lead says they came from Instagram/Facebook/social ad. | `general_interest`, `diagnostic_offered`, `pain_detected`, `product_question`, `diagnostic_requested` | Briefly explain Taliya, then invite overview or pain-specific path. |
| `pain_detected` | Lead shared pain, bottleneck, urgency, or desired improvement. | `diagnostic_offered`, `diagnostic_in_progress`, `product_question`, `human_requested` | Strong tendency to offer/start diagnostic after answering direct questions. |
| `product_question` | Lead asks about product, WhatsApp, CRM, agents, setup, links, demo, checkout, plan, or price. | `diagnostic_offered`, `diagnostic_in_progress`, `buying_intent_detected`, `human_requested`, `out_of_scope` | Answer direct question first, then steer to diagnostic when relevant. |
| `price_question` | Lead asks price. | `diagnostic_offered`, `plan_question`, `buying_intent_detected`, `human_requested` | Answer official price/plan facts directly, then connect to diagnostic/fit. |
| `plan_question` | Lead asks plan or plan fit. | `diagnostic_offered`, `diagnostic_in_progress`, `buying_intent_detected` | Use official plan facts; if fit depends on context, offer diagnostic. |
| `demo_question` | Lead asks demo, call, presentation, or seeing it working. | `demo_offered`, `diagnostic_offered`, `buying_intent_detected`, `human_requested` | Answer official demo path; ask for context so the right demo can be suggested. |
| `demo_offered` | Demo CTA/link was offered or sent. | `demo_reaction_pending`, `diagnostic_offered`, `product_question`, `buying_intent_detected`, `human_requested` | Preserve demo state so future diagnostic close asks whether they looked at it. |
| `demo_reaction_pending` | Agent is waiting for or asking about the lead's demo reaction. | `product_question`, `diagnostic_offered`, `buying_intent_detected`, `human_requested` | Ask what they thought; do not offer waitlist unless next-step intent appears. |
| `demo_reacted_positive` | Lead reacted positively to demo with meaningful interest. | `buying_intent_detected`, `waitlist_eligible`, `product_question`, `human_requested` | Can contribute to waitlist eligibility only with clear next-step/contract intent. |
| `diagnostic_requested` | Lead explicitly asks for free diagnostic. | `diagnostic_in_progress`, `diagnostic_waiting_answer`, `human_requested` | Start diagnostic immediately using already-known facts. |
| `diagnostic_offered` | Agent offered diagnostic but lead has not accepted yet. | `diagnostic_in_progress`, `product_question`, `general_interest`, `human_requested` | Wait for acceptance or answer new direct questions. |
| `diagnostic_in_progress` | Diagnostic is active and mandatory questions are being answered. | `diagnostic_waiting_answer`, `diagnostic_ready`, `product_question`, `human_requested` | Ask exactly the next missing question; do not repeat answered facts. |
| `diagnostic_waiting_answer` | Agent asked a diagnostic question and waits for lead answer. | `diagnostic_in_progress`, `diagnostic_ready`, `product_question`, `human_requested` | Parse answer, update ledger, continue to next missing question. |
| `diagnostic_ready` | All mandatory diagnostic inputs are answered enough to produce recommendation. | `diagnostic_delivered`, `human_requested` | Deliver staged diagnostic: pain/context, CRM base, operational step, agents, plan, demo. |
| `diagnostic_delivered` | Lead received diagnostic and demo bridge. | `demo_reaction_pending`, `post_diagnostic_questions`, `buying_intent_detected`, `waitlist_eligible`, `product_question`, `human_requested` | Answer questions; waitlist only if clear contract intent appears after diagnostic/demo. |
| `post_diagnostic_questions` | Lead asks follow-up after diagnostic. | `buying_intent_detected`, `waitlist_eligible`, `product_question`, `human_requested` | Continue consultative sales, do not restart diagnostic. |
| `buying_intent_detected` | Lead shows clear intent to contract/start/proceed/be notified. | `waitlist_eligible`, `waitlist_offered`, `human_requested` | Offer waitlist if checkout is unavailable or onboarding is controlled. |
| `waitlist_eligible` | Policy says waitlist can be offered. | `waitlist_offered`, `product_question`, `human_requested` | Offer naturally with no fake scarcity or promises. |
| `waitlist_offered` | Waitlist was offered and lead has not accepted/declined yet. | `waitlist_pending_data`, `waitlist_joined`, `post_diagnostic_questions`, `human_requested` | If accepted, collect only missing actionable data. |
| `waitlist_pending_data` | Lead accepted waitlist but some useful details are missing. | `waitlist_joined`, `post_diagnostic_questions`, `human_requested` | Save partial status and ask only missing details one at a time. |
| `waitlist_joined` | Lead/studio is recorded on waitlist. | `post_diagnostic_questions`, `product_question`, `human_requested` | Continue answering questions; do not re-offer waitlist. |
| `human_requested` | Lead asked for a human. | `human_handoff` | Acknowledge and pause automation. |
| `human_handoff` | Handoff event created. | `paused_by_human` | No further AI replies until resume. |
| `paused_by_human` | Human/operator owns the conversation. | `general_interest`, `product_question`, `diagnostic_in_progress`, `waitlist_joined` | Resume only on explicit operator action. |
| `out_of_scope` | Lead asks outside Taliya commercial scope. | `general_interest`, `diagnostic_offered`, `human_requested` | Safe short answer; return to Taliya only if relevant. |
| `safety_blocked` | Prompt injection, sensitive data request, unsafe request, or policy violation. | `general_interest`, `human_requested`, `paused_by_human` | Refuse/redirect safely and log guardrail. |
| `unknown_or_low_confidence` | Model cannot confidently classify. | `general_interest`, `product_question`, `diagnostic_offered`, `human_requested` | Ask one clarification; do not advance high-impact state. |

## Transition Rules

- A cold `greeting_only` state must not transition directly to `diagnostic_offered`, `waitlist_offered`, `waitlist_joined`, or contact capture unless the same user turn contains more than greeting.
- `diagnostic_ready` requires the diagnostic ledger to satisfy [diagnostic-contract.md](./diagnostic-contract.md).
- `diagnostic_ready` must also have enough product knowledge to support the dynamic plan/range recommendation, or it must state the missing official fact and avoid recommending a plan.
- `diagnostic_delivered` must persist demo state and must not skip the demo bridge.
- `demo_offered`, `demo_reaction_pending`, and `demo_reacted_positive` are commercial education states, not waitlist states.
- `waitlist_eligible` requires clear intent to contract, not merely curiosity.
- Demo curiosity alone cannot transition to `waitlist_eligible`.
- `human_handoff` and `paused_by_human` suppress AI delivery until explicit resume.
- `safety_blocked` cannot execute product, waitlist, or diagnostic side effects in the same turn.
- `product_question`, `price_question`, `plan_question`, and `demo_question` must answer directly before proposing diagnostic or waitlist.
- Product explanation, comparison, integration/scope, security/data, out-of-profile, diagnostic-refusal, and conversation-resume turns are interpreted by the LLM and validated by policy; they must not be routed by deterministic commercial regex.
- After `diagnostic_delivered`, follow-up turns must receive compact post-diagnostic context and must not restart diagnostic unless the lead explicitly asks for a new diagnostic.
- `post_diagnostic_questions` must use saved diagnostic memory when relevant, answer direct questions first, and offer waitlist only after clear start/contract intent.
- `waitlist_joined` must continue answering product questions without re-offering waitlist or repeating waitlist status on every answer.
- Diagnostic refusal must keep the state in a product/helpful conversation path and must not immediately return to `diagnostic_offered` in the same assistant turn.

## State Output Requirements

Every successful model turn must return:

- previous state;
- proposed current state;
- proposed next state;
- transition reason;
- evidence for the transition;
- blocking guardrail flags;
- whether the transition is high-impact.

High-impact transitions are:

- diagnostic completion;
- waitlist offer;
- waitlist join;
- human handoff;
- safety block;
- cost-cap stop.

High-impact transitions require validator approval before persistence or delivery.
