# Research: OpenAI CS Agents Adaptation For Taliya Commercial

## Decision: Use A Separate Python Agent Runtime On Railway

**Rationale**: The mandatory reference is a Python backend built around explicit agents, tools, guardrails, context, memory, runner events, and streamed execution. A separate Python service lets the implementation copy that structure directly while keeping the existing Next.js app focused on landing, widget, WhatsApp webhook, and Sales Inbox.

**Alternatives considered**:

- Keep the new agent inside Next.js: rejected because the previous attempt already drifted into deterministic orchestration and template-first response generation.
- Host Python inside Vercel functions: rejected because a persistent service with clearer logs, health checks, and deployment boundaries is more appropriate for this runtime.
- Use an external no-code automation layer: rejected because the Taliya app and Postgres must remain the source of truth.

## Decision: Keep Next/Vercel As Channel And UI Layer

**Rationale**: The current app already owns `/pilates`, widget rendering, WhatsApp webhook normalization, Sales Inbox, lead storage, and channel delivery. Replacing those would increase risk and could violate the protected landing rule.

**Alternatives considered**:

- Move webhook and widget endpoints into Railway: rejected because it would duplicate existing public routing and increase landing integration risk.
- Replace Sales Inbox with a new agent trace UI: rejected for this feature; Sales Inbox should be extended instead.

## Decision: Use Generic `taliya-agent-runtime` Naming

**Rationale**: Taliya will later need configuration and studio operation agents. The runtime should not be named or structured as if the commercial agent is the only agent forever.

**Alternatives considered**:

- `taliya-sales-agent`: rejected because it creates naming debt before future agents are added.
- One runtime per agent from day one: rejected because it fragments shared memory, guardrails, auth, observability, and deploys too early.

## Decision: Use `POST /v1/agent-runs` With `agent_key`

**Rationale**: A generic run endpoint supports future agents while keeping the current scope explicit through `agent_key: "taliya_commercial"`.

**Alternatives considered**:

- `POST /v1/taliya/sales-agent/turn`: rejected because the endpoint name does not age well with multiple agents.
- One endpoint per agent: rejected for now because shared validation, auth, tracing, and evals are easier through a common contract.

## Decision: Start With One Active Agent Key, `taliya_commercial`

**Rationale**: The feature must solve the commercial lead experience for Taliya's own Pilates SaaS first. Future agents should be reserved by naming and registry design only.

**Alternatives considered**:

- Implement configuration agent now: rejected as scope creep.
- Implement seven studio agents now: rejected by explicit user decision.
- Implement multi-tenant studio runtime now: rejected by explicit user decision.

## Decision: Adapt The OpenAI Demo Structure File-For-File

**Rationale**: The previous implementation treated the reference as inspiration and drifted. The new work must map demo concepts to Taliya files so review can catch architecture drift early.

**Alternatives considered**:

- Keep current interpreter/orchestrator/generator names: rejected because they encode the deterministic architecture that needs to be replaced.
- Build a new bespoke abstraction: rejected because the reference already provides the target pattern.

## Decision: HMAC Authentication Between Next And Railway

**Rationale**: The runtime will be called by public-facing routes. HMAC over timestamp and raw body protects against replay and body tampering better than a bearer-only shared secret.

**Alternatives considered**:

- Bearer token only: rejected because it does not bind the token to the body.
- Public unauthenticated endpoint: rejected.
- mTLS: rejected for now as operationally heavier than needed.

## Decision: Generic `agent_runtime_*` Tables

**Rationale**: Runtime records must survive future agents. Names such as `agent_v2_*` or `sales_agent_*` would encode the old implementation or the current commercial-only scope.

**Alternatives considered**:

- Reuse `agent_v2_*` tables as primary runtime storage: rejected because they carry the wrong mental model and would confuse future development.
- Replace all Sales Inbox tables immediately: rejected because existing lead/message persistence is useful and lower risk.

## Decision: Product Knowledge Is A Tool-Backed Source Of Truth

**Rationale**: Price, plans, links, demo status, waitlist status, availability, and unsupported claims must be controlled by product data and validators, not prompts.

**Alternatives considered**:

- Put product facts directly in prompts: rejected because prompts drift and are hard to audit.
- Hardcode price text in response templates: rejected because templates are the official voice, not the source of product truth or the conversation brain.

## Decision: Use Default And Strong Model Classes

**Rationale**: Commercial quality should be strong, but cost must remain controlled. The default model handles normal conversation; a stronger model is reserved for complex diagnostics, low-confidence ambiguous turns, safety-sensitive recovery, and eval judging.

**Alternatives considered**:

- Always use strongest model: rejected for cost control.
- Always use cheapest model: rejected because quality is the goal of this replacement.

## Decision: No Legacy Conversational Rollback

**Rationale**: There are no active production users depending on the current runtime. Keeping deterministic v2 as fallback would preserve the architecture failure and hide regressions.

**Alternatives considered**:

- Legacy fallback flag: rejected.
- Shadow or canary rollout: rejected as unnecessary for this context.
- Operational pause/fallback only: accepted for API outage, human handoff, cost cap, or unsafe output.

## Decision: Evals Must Judge Conversation Quality

**Rationale**: The current eval suite passed even though the agent sounded robotic. The replacement must fail on evasiveness, generic diagnostics, unnatural wording, fake certainty, or bad timing even when expected keywords are present.

**Alternatives considered**:

- Snippet-only assertions: rejected as insufficient.
- Manual review only: rejected because regressions need repeatable gates.
- LLM judge only: rejected because hard invariants need deterministic blocking checks.
