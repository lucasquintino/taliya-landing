# Contract: Tools And Guardrails

## Tool Principles

- Tools are model-callable functions exposed to the agent runner.
- Tools are the only way to perform side effects.
- Side-effecting tools must be idempotent.
- Tool outputs must be concise, factual, and safe to return to the model.
- Tools validate inputs before persistence.

## Required Tools

### `get_product_knowledge`

Purpose: Return official commercial facts for plans, prices, demo, waitlist, availability, links, unsupported claims, and source version.

Side effects: none.

Must return:

- `source_version`
- requested facts
- missing facts
- unsupported claims

### `save_lead_facts`

Purpose: Persist facts extracted from the lead with evidence and confidence.

Side effects: updates lead facts and Sales Inbox projection.

Required idempotency key: yes.

### `save_diagnostic_record`

Purpose: Persist diagnostic state or final diagnostic output.

Side effects: creates or updates diagnostic record.

Required idempotency key: yes.

### `save_demo_engagement`

Purpose: Persist demo offer, official link/CTA source, channel rendering, and lead reaction.

Side effects: updates demo state and Sales Inbox projection.

Required idempotency key: yes.

### `mark_waitlist`

Purpose: Offer, update, join, decline, or remove waitlist state.

Side effects: updates waitlist and Sales Inbox projection.

Required idempotency key: yes.

### `pause_for_human`

Purpose: Pause automation for human handoff.

Side effects: sets human status and records handoff event.

Required idempotency key: yes.

### `resume_from_human`

Purpose: Resume automation after operator action.

Side effects: updates human status and restores last safe state.

Required idempotency key: yes.

### `record_runtime_note`

Purpose: Record trace or operator-relevant note without changing conversation behavior.

Side effects: appends trace or Sales Inbox note.

Required idempotency key: yes.

## Input Guardrails

Required guardrails:

- Relevance to Taliya/Pilates/commercial flow.
- Prompt injection and system prompt extraction.
- Abuse or unsafe content.
- Sensitive personal data overcollection.
- Unsupported media.
- Human-active pause.

## Output Guardrails

Required validators:

- Cold greeting-only openings cannot offer diagnostic, waitlist, name capture, phone capture, or plan lists.
- Source-specific openings must match `behavior-contract.md`.
- Direct questions must be answered before diagnostic, waitlist, or qualification.
- Diagnostic offer timing must match the behavior contract.
- Waitlist offer timing must match the behavior contract.
- No early contact capture before value or explicit follow-up/waitlist request.
- Reliable/unreliable profile-name policy must be enforced.
- Banned voice phrases from `behavior-contract.md` are flagged.
- Repeated question/fact requests are flagged when state already has the answer.
- Product source required for price/plan/demo/link/availability/checkout claims.
- No invented link or checkout.
- No WhatsApp phone request.
- No fake certainty in diagnostic.
- No "pelo que voce contou" style evidence framing unless evidence exists.
- Diagnostic start and in-progress turns must include grounded feedback before the next question.
- Completed diagnostic must follow staged order: hold, pain/context, CRM base, operational step, agents, plan, demo.
- Completed diagnostic must block old weak final formats from `diagnostic-contract.md`.
- Completed diagnostic final plan line must be dynamic and backed by product knowledge.
- Completed diagnostic final demo line must match persisted demo state.
- Demo curiosity alone cannot trigger waitlist.
- No system prompt, tool schema, secret, or internal policy leak.
- No response while human handoff is active.
- Message length and chunkability for both widget and WhatsApp.
- Widget button actions require validated widget support.
- WhatsApp actions must use approved text or official links instead of widget-only buttons.
- Trace/log redaction for secrets, signatures, system prompts, and unnecessary raw provider payloads.

## Guardrail Results

Every guardrail event must persist:

- guardrail name
- phase
- status
- reason
- evidence when safe
- whether output was blocked, repaired, or escalated

## Repair Policy

The runtime may attempt one repair for invalid structured output or minor style/length violation. It must not repair by inventing missing product facts. Product-source failures require tool refresh or block.

Behavior-contract failures may attempt one repair with the exact violation summarized to the model. If the repaired output still violates the contract, the runtime must suppress the unsafe answer and use a safe operational fallback or human handoff. It must not call the old deterministic v2 conversation brain.
