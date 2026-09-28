# Spec 012 - Taliya Commercial Agent On OpenAI Agents SDK

Status: implemented through T012-056. The Luna paid validation and production
migration tasks T012-057 through T012-060 remain pending.

Scope: only the Taliya-owned commercial lead agent for the floating widget and Taliya's own WhatsApp number. This spec does not change `/pilates`, does not redesign UI, does not add multi-tenant behavior, does not connect client/studio WhatsApp accounts, and does not implement checkout.

## Executive Decision

Spec 012 replaces the handcrafted Spec 011 conversational engine with an OpenAI Agents SDK based engine.

This is not a reset of the product behavior. Spec 011 and the preserved Spec 010 contracts remain the behavioral source of truth. Spec 012 changes the implementation strategy for the conversation motor.

Use:

`Channel Adapter -> Runtime API -> Turn Gate -> Context Builder -> OpenAI Agents SDK Runner -> Taliya Agents / Tools / Handoffs / Guardrails -> SDK Output Adapter -> Contract Validators -> Approved Renderer -> Persistence / Sales Inbox Projection -> Delivery / Outbox`

Key decision:

- The OpenAI Agents SDK owns agent orchestration, specialist handoffs, tool calls, guardrails, runner execution, run items, and tracing semantics.
- Taliya code owns product truth, context building, official knowledge retrieval, diagnostic state, validator enforcement, approved rendering, persistence, Sales Inbox projection, delivery/outbox, cost accounting, feature flags, and production gates.
- Official knowledge retrieval is the Taliya RAG layer. RAG provides grounded facts and source refs, but it must not become the commercial routing brain.
- The SDK final output must be a structured Taliya turn proposal, not an unvalidated free-form message sent directly to leads.
- Normal commercial understanding remains LLM-first. Deterministic code must not route, answer, or template-select commercial turns from raw lead text.

## Why This Spec Exists

Spec 011 correctly identified the old commercial core as too large, deterministic, and unstable. It also preserved the right behavioral contracts. However, the Spec 011 implementation grew a new custom agent framework:

- action conductor;
- turn situation/action menus;
- decision compiler;
- custom repair loop;
- custom trace;
- custom model I/O wrappers;
- custom orchestration around simulated specialist roles.

The latest failure pattern shows that the action-first path can select the right action while still failing at human commercial understanding. The agent becomes structurally safe but not sufficiently conversational.

Spec 012 keeps the Spec 011 quality gates, but stops implementing the agent framework by hand.

## Current-State Audit

The runtime already depends on `openai-agents` in `services/taliya-agent-runtime/pyproject.toml`. Local import confirms `agents` is installed and exposes `Agent`, `Runner`, `function_tool`, `handoff`, and `input_guardrail`.

The active public commercial endpoint is `/v1/taliya-commercial/turn`, which
calls the Spec 012 action-first Agents SDK runtime. It has no public fallback to
`run_spec011_agent_turn`. The legacy `/v1/agent-runs` path rejects public Taliya
commercial turns except explicit human runtime controls. Production remains on
the previously validated `gpt-5.4-mini` model until the T012-057 Luna gate
passes and T012-059 performs the explicit Railway model switch.

Reusable current infrastructure:

- `services/taliya-agent-runtime/app/main.py` as API shell, HMAC/idempotency boundary, registry check, feature flag, and runtime-control handler.
- Existing widget and Taliya-owned WhatsApp adapters as channel adapters.
- Existing memory/persistence infrastructure.
- Product knowledge sources and Spec 006 product contracts.
- Approved template inventory and template registry.
- Renderer channel rules and outbox/delivery rules.
- Sales Inbox projection contracts and storage.
- Static audit and eval harnesses, after adapting them to the SDK path.

Not reusable as the new conversation motor:

- `app/core/taliya_commercial/conductor.py`
- `app/core/taliya_commercial/turn_situation.py` as the normal-turn commercial constraint layer
- `app/core/taliya_commercial/decision_compiler.py` as the center of state/render derivation
- `app/core/taliya_commercial/repair.py` as the primary model repair engine
- any action-first contract that reduces the model to selecting a small enum before it has produced rich commercial understanding
- any simulated multi-agent or handoff behavior that the SDK should own natively

Reusable with adaptation:

- `schemas.py` as a source for new typed proposal/state schemas.
- `validators.py` as contract enforcement, but with reduction and split by responsibility.
- `runtime_adapter.py` only as reference for endpoint integration, not as the new orchestration core.
- `trace_store.py` and `trace_export.py` as local persistence/export adapters for SDK run items and Taliya-specific correctness artifacts.

## Preserved Source Of Truth

Spec 012 preserves these documents as binding behavior:

- `specs/010-openai-cs-agents-adaptation-for-taliya-commercial/behavior-contract.md`
- `specs/010-openai-cs-agents-adaptation-for-taliya-commercial/diagnostic-contract.md`
- `specs/010-openai-cs-agents-adaptation-for-taliya-commercial/conversation-state-contract.md`
- `specs/010-openai-cs-agents-adaptation-for-taliya-commercial/message-template-contract.md`
- `specs/010-openai-cs-agents-adaptation-for-taliya-commercial/product-followup-delta-contract.md`
- `specs/010-openai-cs-agents-adaptation-for-taliya-commercial/sales-inbox-contract.md`
- `specs/011-taliya-commercial-agent-core-reset/spec.md`
- `specs/011-taliya-commercial-agent-core-reset/regression-cases.md`
- `specs/011-taliya-commercial-agent-core-reset/eval-plan.md`
- `specs/011-taliya-commercial-agent-core-reset/coverage-map.md`
- Product truth from `specs/006-crm-operational-core/`
- Official product knowledge under `services/taliya-agent-runtime/app/shared/product_knowledge/`

Spec 012 supersedes only the Spec 011 implementation strategy for the conversation motor.

## Functional Requirements

### SDK Engine Boundary

- FR-012-001: The new commercial motor must be implemented as a new SDK-based core beside the current Spec 011 core. It must not mutate the current public endpoint until a feature flag, shadow mode, and eval gates are ready.
- FR-012-002: The SDK runner must execute Taliya agent definitions, handoffs, tools, and guardrails. It must not be hidden behind a custom action-first conductor.
- FR-012-003: A normal commercial turn must be handled by the SDK path unless it is an explicitly allowed operational/safety/cold-empty boundary.
- FR-012-004: The SDK final output must be adapted into a strict `TaliyaTurnProposal` or equivalent typed schema before validation/rendering.
- FR-012-005: The SDK must not send customer-facing text directly to widget or WhatsApp. All lead-facing output must pass Taliya validators and approved rendering.

### Agent Topology

- FR-012-010: The SDK topology must include explicit Taliya commercial agents or roles for entry, product, diagnostic, waitlist, handoff, and safety.
- FR-012-011: The runtime may start a turn from the persisted current agent when that current agent is known from state. This is operational state selection, not raw-text commercial routing.
- FR-012-012: First meaningful turns or unclear persisted-agent states should start at the Taliya triage agent.
- FR-012-013: SDK handoffs must be represented in persisted traces and Sales Inbox debug artifacts.
- FR-012-014: A handoff to a human is not only wording. It must persist human-active/pause state and suppress AI replies until explicit resume.

### Tools

- FR-012-020: SDK tools must be explicit, typed, and narrow.
- FR-012-021: Tools called during agent reasoning must be read-only or proposal-only by default.
- FR-012-022: Production state mutations must happen after validators pass, outside free model reasoning, unless a tool is explicitly classified as a safe operational side effect.
- FR-012-023: Product knowledge tools must read only official product knowledge and Spec 006 product contracts.
- FR-012-026: Product knowledge retrieval must follow `rag-policy.md`: every customer-facing product claim requires a fact ref and approved source id.
- FR-012-027: RAG/retrieval must not classify commercial intent, choose waitlist eligibility, choose diagnostic route, or generate final lead-facing text.
- FR-012-024: Diagnostic, waitlist, demo, and handoff tools may propose updates, but the runtime commits only validated updates.
- FR-012-025: Tools must not ask for client/studio WhatsApp numbers, invent checkout links, invent discounts, invent dates, or create product facts.

### Guardrails And Validators

- FR-012-030: SDK input guardrails must cover prompt injection, sensitive data, unsupported media, and out-of-scope abuse.
- FR-012-031: SDK guardrails do not replace Taliya contract validators.
- FR-012-032: Taliya validators must still check direct question first, official product facts, price/student-count separation, diagnostic completeness, no repeats, waitlist/demo gating, internal leaks, channel constraints, model usage, trace completeness, and Sales Inbox consistency.
- FR-012-033: A validator failure may trigger at most one SDK repair/escalation path before safe operational fallback/handoff.
- FR-012-034: Validators must not become a second commercial brain and must not rewrite the SDK-selected commercial meaning into a different route.

### Structured Output And Rendering

- FR-012-040: The SDK output schema must capture rich commercial understanding, not only a small selected action.
- FR-012-041: Required proposal fields include selected specialist/agent, direct-question handling, grounded answer obligations, extracted facts with evidence, diagnostic proposals, product fact refs, demo/waitlist/handoff proposals, selected approved response family/template ids, customer-facing semantic fragments when allowed, confidence, and risks/unknowns.
- FR-012-042: Whole-response free-form assistant text remains forbidden as the delivery source.
- FR-012-043: LLM-authored customer-facing fragments are allowed only as registered, bounded, evidence-grounded template variables.
- FR-012-044: The renderer must fail on missing semantic variables instead of using generic defaults.

### Evals, Shadow Mode, And Release

- FR-012-050: The Spec 011 golden transcripts and do-not-do fixtures must be reused as the first SDK behavior gate.
- FR-012-051: The SDK path must be evaluated in an isolated spike before any public cutover work.
- FR-012-052: Spike output must compare the SDK path against the current Spec 011 path for the same inputs, using transcript, structured proposal, tool calls, handoffs, validators, rendered output, Sales Inbox projection, model usage, and cost.
- FR-012-053: The SDK path must run in shadow mode before customer-facing activation.
- FR-012-054: Production activation remains blocked until static audit, local tests, real-model golden/do-not-do evidence, trace export, Sales Inbox export, rollback proof, manual review, and approval log pass.

## Prohibitions

Spec 012 forbids:

- treating OpenAI Agents SDK as a wrapper around the current action-first conductor;
- sending SDK free-form output directly to leads;
- allowing SDK tools to commit commercial state before validation;
- recreating `DecisionCompiler` as the new hidden brain;
- recreating `repair.py` as a huge tactical repair library;
- deterministic raw-text routing for price, plan, demo, diagnostic, waitlist, pain-first, source opening, objection, WhatsApp product question, or mixed intent;
- product facts in prompts/templates/fallbacks outside official product knowledge or Spec 006;
- using RAG retrieval as deterministic commercial routing;
- weakening Spec 011 validators or eval gates to make the SDK path pass;
- public cutover without shadow mode and rollback proof;
- re-enabling legacy runner or old TS v2 commercial responder as rollback.

## Acceptance Criteria

- AC-012-001: The SDK migration can be implemented without changing `/pilates`.
- AC-012-002: The SDK spike proves whether Agents SDK produces better commercial understanding than the current action-first path on critical scenarios.
- AC-012-003: Every preserved Spec 010/011 behavior contract maps to an SDK agent instruction, tool, guardrail, validator, renderer, persistence rule, or eval.
- AC-012-004: The new SDK core has no module that combines commercial interpretation, validation, rendering, persistence, and delivery.
- AC-012-005: Normal commercial turns show model usage and SDK run trace unless explicitly exempt.
- AC-012-006: Tool calls, handoffs, guardrails, final proposal, validators, renderer output, runtime diff, and Sales Inbox projection are persisted in the mandatory trace.
- AC-012-007: The SDK path passes the same golden/do-not-do gates before any production activation.
- AC-012-008: Rollback disables the SDK path without restoring the old deterministic commercial brain.
- AC-012-009: Every implementation task is closed in `implementation-ledger.md` with evidence, anti-determinism review, protected-scope diff result, and next task lock.
- AC-012-010: `coverage-map.md` has no uncovered P0/P1 behavior before SDK core implementation, shadow mode, or production activation.
- AC-012-011: Product-answer evals fail when a customer-facing product claim lacks an approved fact ref from the RAG/product knowledge layer.

## Implementation Control Guarantees

Spec 012 implementation must use these control files:

- `decision-log.md` records D-012 decisions before related code starts.
- `coverage-map.md` maps behavior and architecture requirements to owners, tasks, and evidence.
- `implementation-ledger.md` records task closure, evidence, review, protected-scope diff, and next task lock.

Hard rules:

- No SDK implementation code before Phase 0 decisions are recorded.
- No paid OpenAI/SDK run before explicit user approval for the run or budget.
- No task closes without evidence and anti-determinism review.
- No task closes if it creates or hides deterministic raw-text commercial routing.
- No release gate passes with uncovered P0/P1 behavior in `coverage-map.md`.
- No public activation without spike pass, shadow pass, rollback proof, manual review, and approval log.

## Decisions Requiring Confirmation

- D-012-001: Confirm OpenAI Agents SDK as the selected motor for Spec 012.
- D-012-002: Confirm whether normal turns may use real SDK handoffs when needed, with cost caps, instead of forcing one model operation in every case.
- D-012-003: Confirm the exact SDK topology: triage plus specialists as handoffs, agents-as-tools, or a hybrid.
- D-012-004: Confirm that production state mutation during SDK reasoning is disallowed except explicit safe operational tools.
- D-012-005: Confirm the spike scenario set and paid budget before any real OpenAI SDK runs.
- D-012-006: Confirm whether to keep the current Spec 011 endpoint name with an internal engine flag or introduce a separate SDK endpoint during shadow mode.
- D-012-007: Confirm trace retention and whether SDK traces may include any lead text in external tracing systems before production use.

## References

- OpenAI Agents SDK guide: https://developers.openai.com/api/docs/guides/agents
- OpenAI Agents Python SDK: https://github.com/openai/openai-agents-python
- OpenAI Agent evals guide: https://developers.openai.com/api/docs/guides/agent-evals
- Local reference: `C:\Users\lucas\AppData\Local\Temp\openai-cs-agents-demo`
