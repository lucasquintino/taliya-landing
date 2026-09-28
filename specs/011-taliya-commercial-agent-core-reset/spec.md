# Spec 011 - Taliya Commercial Agent Core Reset

Status: implementation in progress, currently blocked at Phase 10 / T011-105 pending fresh paid golden/do-not-do evidence and final approval gates.

Scope: only the Taliya-owned commercial agent for leads coming from the floating widget and Taliya's own WhatsApp. This spec does not implement code, does not change `/pilates`, does not redesign UI, does not add multi-tenant behavior, and does not connect WhatsApps from client studios.

Scope clarification: this spec is not the Taliya CRM product implementation spec, not the Design System/component library spec, not the operational CRM agents spec, and not the demo/video production spec. It only defines how the Taliya-owned commercial lead agent must be reset so it can explain, qualify, diagnose, and route commercial leads without falling back into deterministic chatbot behavior.

## Executive Decision

The candidate architecture is directionally correct, but it must be adjusted before implementation.

Use:

`Channel Adapter -> Runtime API -> Turn Gate -> Context Builder -> Turn Situation Builder -> LLM Action Conductor -> Decision Compiler -> Contract Validators -> Focused Repair -> Template Renderer -> Persistence/Projection -> Delivery/Outbox`

Where:

- `Turn Gate` includes conversation lock, idempotency, human-pause checks, inbound sequencing, and deferred inbound handling while an outbound response is already being delivered.
- `Context Builder` includes compact memory, channel metadata, product knowledge retrieval, diagnostic ledger, waitlist/demo/handoff state, and Sales Inbox projection inputs.
- `Turn Situation Builder` computes the operational situation, pending state, allowed action menu, and required obligations from persisted state. It must not infer commercial meaning from raw lead text.
- `LLM Action Conductor` is the only commercial conversation brain for normal turns. It interprets the inbound message and chooses one allowed action from the current turn situation.
- `Decision Compiler` deterministically converts the LLM-selected action into state transition, diagnostic ledger updates, allowed template group expansion, and render-plan skeleton. It must not override the LLM's commercial interpretation or choose actions from raw lead text.
- `Specialists` are policy roles inside the conductor schema/prompt by default, not separate model calls on every turn.
- Extra model calls are allowed only for repair, low-confidence diagnostic reasoning, complex contradictory context, or eval/judge work.
- `Validators` may reject, request repair, or block unsafe output. They must not become a second commercial brain.
- `Template Renderer` renders approved language after the decision. It must not choose commercial route, infer facts, or silently invent semantic defaults.
- `Trace` is mandatory for every normal commercial turn. A turn without trace cannot be considered correct, even if the user-facing text looks good.

Do not copy the OpenAI customer-service demo as a literal multi-agent graph for every Taliya turn. Copy its separation of concerns: agents/policies declare capabilities, the runner owns orchestration, tools own side effects, guardrails are visible, context is explicit, and events are inspectable.

Do not patch the current commercial brain tactically. New commercial behavior must enter through regression case, schema/context/prompt/validator/eval, not through another condition in `runner.py`.

Correction after T011-105 evidence: the reset must not continue by adding more post-LLM repair branches for each paid failure. The next implementation correction is the action-first contract in `action-contract.md`: state-aware allowed actions, smaller LLM JSON, compiler-derived state/rendering, and static audit against raw-text deterministic commercial decisions.

## Required Audit Summary

### Contract Audit

The contracts in `specs/010-openai-cs-agents-adaptation-for-taliya-commercial/` remain the strongest source of truth for behavior. They correctly define:

- LLM-first commercial understanding.
- One normal model operation per turn.
- Structured decision JSON.
- Direct questions answered before steering.
- Diagnostic ledger and mandatory question coverage.
- Approved templates as language, not conversation logic.
- Product follow-up behavior without regex routing.
- Sales Inbox completeness as a correctness requirement.
- Waitlist gating after real fit/intent.
- Human handoff pause/resume.
- Channel parity between widget and Taliya WhatsApp.

However, Spec 010 also grew into a large accumulation of fixes. The reset must preserve its binding contracts while preventing them from becoming more `runner.py` branches. Spec 011 treats those contracts as policy, schemas, validators, and eval gates, not as permission to keep adding deterministic shortcuts.

Spec 009 and Spec 002 remain useful for product behavior, channel expectations, Sales Inbox, and widget/WhatsApp flow, but any older deterministic interpreter/orchestrator/response-generator pattern is superseded by this reset. Spec 001 remains binding for protected `/pilates` behavior and positioning.

Spec 006 is binding for what the commercial agent may say about the Taliya CRM product itself. It is the source of truth for product pages, subscription/access flow, setup, navigation, operational agents, modes, decisions of cut, and visual-functional screen contracts. If Spec 010 describes how the agent behaves conversationally and Spec 006 describes what the product is, the conductor must respect both.

Language rule: use practical studio-owner language by default. The agent should prefer "sistema", "rotina", "base organizada", "atendimento", "agenda", "vendas", "alunos", "turmas", and "próximos passos" over technical phrasing. "CRM" may appear only when the lead uses/asks the term, when an approved template explicitly requires it, or when the message needs to name the system category clearly. It must not become the default customer-facing label.

### Implementation Audit

The current infrastructure is reusable; the current conversational core is not.

Reusable:

- `services/taliya-agent-runtime/app/main.py` as the Runtime API boundary, HMAC verification, request shape, idempotency cache, and health endpoints.
- Runtime schemas as a starting point for a stricter conductor decision contract.
- Product knowledge source, provided all product facts stay centralized there.
- Approved templates, provided selection stays with the LLM conductor and rendering stays mechanical.
- Existing validators, provided they become stricter and stop trusting weak "PASS" fields.
- Memory/persistence and Sales Inbox projection paths, provided they are made explicit outputs of the core.
- Widget and WhatsApp adapters, provided they remain channel adapters and do not interpret commercial intent.

Not reusable as core:

- `services/taliya-agent-runtime/app/runtime/runner.py` as the conversation brain. It is about 5,944 lines and contains route mutation, template selection, product intent inference, diagnostic advancement, waitlist decisions, fast paths, and customer-facing fallbacks in one file.
- Commercial text/token helpers that decide price, plan fit, pain-first, product follow-up, social openings, demo interest, diagnostic acceptance, or waitlist behavior.
- Old TS v2 semantic interpreter/response generator as any public fallback.

The observed bugs are consistent with this audit: internal text leaked, price was confused with student count, diagnostic questions were skipped or repeated, simple numeric answers failed, final diagnostics were truncated, chunks duplicated, "tudo bem" during delivery was over-interpreted, Sales Inbox drifted from runtime state, and evals marked bad behavior as PASS.

Implementation decision: do not refactor `runner.py` in place as the new core. Build a small new core beside it, quarantine the legacy runner, and cut over behind a controlled flag. The legacy runner may be used as a fixture, rollback reference, or historical comparison, but not as the active commercial brain for the reset.

### OpenAI Demo Audit

The local reference at `C:\Users\lucas\AppData\Local\Temp\openai-cs-agents-demo` is commit `bd7bfca`.

Useful patterns:

- `airline/agents.py` keeps agent roles, tools, handoffs, and guardrails declarative.
- `airline/context.py` keeps conversational state explicit and filtered before UI exposure.
- `airline/tools.py` keeps side effects in tools and returns tool results, not hidden branch behavior.
- `airline/guardrails.py` uses separate model-backed guardrail agents for relevance and jailbreak checks.
- `server.py` uses the SDK Runner as the orchestration brain, then records handoffs, tool calls, tool outputs, context updates, and guardrail results for the UI.
- The UI runner panel makes orchestration inspectable.

Mismatch with Taliya:

- The OpenAI demo is a demonstration app with mock airline data and streaming ChatKit UI. Taliya is a production commercial lead agent with approved voice, diagnostic obligations, Sales Inbox projection, WhatsApp delivery, cost constraints, and no public checkout.
- The demo can afford visible handoffs and multiple tool operations for operational tasks. Taliya should not pay for multiple specialists on ordinary commercial turns unless a repair/escalation path justifies it.
- The demo's tools can mutate context directly during a turn. Taliya should validate the structured decision before persistence/delivery side effects.

Conclusion: adapt the reference's responsibility split and event transparency, not its exact multi-agent topology.

Terminology note: in Taliya business language, a commercial demo and a product demo are the same customer-facing concept: a demonstration that helps the lead understand the product and advance commercially. This must not be confused with the OpenAI technical reference demo or with marketing/video production assets.

## Source Of Truth

Spec 011 preserves these contracts unless explicitly superseded here:

- `behavior-contract.md`
- `diagnostic-contract.md`
- `conversation-state-contract.md`
- `message-template-contract.md`
- `product-followup-delta-contract.md`
- `sales-inbox-contract.md`
- `reference-map.md`
- `current-runtime-gap-analysis.md`
- `action-contract.md`
- Product truth from `specs/006-crm-operational-core/`, especially product decisions, screen contracts, route/page maps, navigation, setup/subscription contracts, agent/mode matrices, and use-case coverage docs.
- Official product knowledge in `services/taliya-agent-runtime/app/shared/product_knowledge/`
- Widget/WhatsApp and Sales Inbox commitments from Specs 001, 002, and 009 that do not conflict with LLM-first behavior.

Spec 011 supersedes:

- Any template-first, regex-first, state-machine-first, or old v2 TS conversational decision path.
- Any runtime fallback that sends commercial answers without the LLM conductor, except allowed operational/safety/cold-greeting boundaries.
- Any eval definition that can PASS without checking transcript quality, structured decision, validators, Sales Inbox projection, and model usage.
- Any product explanation that contradicts Spec 006 or official product knowledge.
- Any implementation plan that refactors `runtime/runner.py` into the new commercial brain instead of creating a small new core with legacy quarantine.

## Non-Goals

- No landing page changes.
- No `/pilates` visual, layout, copy, CTA, animation, or section changes.
- No multi-tenant implementation.
- No connection to client/studio WhatsApp accounts.
- No checkout/payment flow.
- No full UI redesign of Sales Inbox.
- No Design System/component library inventory or implementation.
- No implementation of operational CRM agents for client studios.
- No production of demo videos, clickable product demos, or visual marketing assets. The commercial agent may talk about the approved Taliya product demo as a sales concept, but this spec does not create those assets.
- No further scope expansion inside this reset. Implementation is now underway under `tasks.md`, `coverage-map.md`, and `implementation-ledger.md`; any remaining work must continue one task at a time from the current task lock.

## Functional Requirements

### Core Boundaries

- FR-011-001: The runtime must expose one shared core for widget and Taliya-owned WhatsApp.
- FR-011-002: Channel adapters may normalize transport metadata, verify signatures, map attachments, and enqueue/deliver messages. They must not make commercial route, diagnostic, waitlist, product, price, plan, or demo decisions.
- FR-011-003: The Runtime API may authenticate, validate request shape, enforce idempotency, and call the core. It must not contain commercial conversation branches.
- FR-011-004: The Turn Gate must enforce one active turn per conversation, stable idempotency keys, human-pause no-reply behavior, delivery sequencing, and deferred inbound handling while a response is in progress.
- FR-011-005: Any inbound message received while chunks are still being delivered must be persisted and deferred. The system must finish the already-started outbound response, must not start a parallel response, and must process the deferred inbound message only as the next clean turn after the current delivery completes.

### Context Builder

- FR-011-006: Context Builder must assemble a compact, typed `TurnContext` from persisted memory, latest inbound message, prior outbound messages, diagnostic ledger, waitlist/demo/handoff state, source/channel metadata, and official product knowledge.
- FR-011-007: Product knowledge retrieval may use deterministic keys as retrieval hints only. Retrieval hints must never force the route, intent, answer, template, or diagnostic action.
- FR-011-008: Context must distinguish reliable facts, inferred facts, unverified identity, channel metadata, internal notes, and customer-visible language.
- FR-011-009: Internal labels such as "lead came from the site", "Reliable profile first name", schema keys, source ids, and route names must never be renderable customer text.

### Turn Situation And Action Contract

- FR-011-009A: Turn Situation Builder must derive `mode`, pending diagnostic question, completed/missing diagnostic keys, waitlist/demo/handoff status, allowed actions, required obligations, eligible template groups, and state constraints from persisted state and typed context.
- FR-011-009B: Turn Situation Builder must not infer price, demo, objection, pain, diagnostic acceptance, waitlist, handoff, source/social opening, or mixed-intent meaning from raw lead text. Raw text may be passed to the LLM and may be used only for retrieval hints or safety boundaries outside the LLM.
- FR-011-009C: Every normal commercial turn must provide the LLM with an explicit allowed-action menu. The LLM must choose one allowed action, not invent an unconstrained route/state/template combination.
- FR-011-009D: Decision Compiler must convert a valid LLM action decision into state transition, diagnostic ledger merge, template group expansion, render-plan skeleton, and projection inputs. It must not choose a commercial action that the LLM did not select.
- FR-011-009E: The action contract in `action-contract.md` is binding for all conversation modes: entry, diagnostic, post-diagnostic, product/price/demo, waitlist, handoff, and deferred delivery.

### LLM Conductor

- FR-011-010: For normal commercial turns, the LLM action conductor is the only component that interprets the lead's commercial meaning and chooses the current action, detected intents, direct-question handling, slot capture, product-fact usage, diagnostic intent, waitlist intent, demo intent, handoff intent, and reply goal.
- FR-011-011: The conductor must return strict structured JSON. Free-form assistant text is not an accepted core output.
- FR-011-012: The conductor must always receive the applicable contract summary and official product facts needed for the turn.
- FR-011-013: The conductor must include evidence for extracted facts and must separate user-provided numbers from plan prices. Example: `497` in "plano de 497" is a price reference, not a student count.
- FR-011-014: The conductor must keep logical specialist roles: entry, product, diagnostic, waitlist, handoff, and safety. These are roles inside the decision, not mandatory separate model calls.
- FR-011-015: Direct commercial questions must be answered first before diagnostic, waitlist, or demo steering.
- FR-011-016: Mixed-intent messages must stay LLM-first and must not be decomposed by deterministic regex branches.
- FR-011-016A: The LLM must not be responsible for assembling the full final render plan, final state transition, or full template variable map for every turn. Those must be derived by the compiler from the LLM action and validated sources wherever deterministic derivation is possible without interpreting raw lead text.

### Allowed Determinism

- FR-011-017: Deterministic code may handle only operational/safety boundaries: idempotency, locks, human handoff pause/resume, explicit unsupported media, prompt injection/sensitive data blocking, empty widget opening, pure cold greeting, schema validation, template rendering, persistence, delivery, and cost/timeouts.
- FR-011-018: Deterministic code must not route or answer price, demo, plan fit, product explanation, social/source openings, pain-first turns, diagnostics, waitlist, product follow-up, objections, or mixed intents.
- FR-011-019: If a deterministic validator detects a commercial-contract violation, it must reject/block/repair; it must not silently rewrite the commercial decision into a new route.

### Validators And Repair

- FR-011-020: Validators must run before rendering and before persistence of outbound state.
- FR-011-021: Validators must check schema, required fields, state transition, direct-question answer, official product fact usage, diagnostic ledger completeness, no repeated diagnostic question, no skipped mandatory urgency, waitlist eligibility, demo gating, channel constraints, no internal text leak, and Sales Inbox projection completeness.
- FR-011-022: Renderer defaults that invent semantic content are forbidden. Missing semantic variables are validation failures.
- FR-011-023: Repair may call the model once with the validation errors and original context. A second failed repair must fall back to safe operational handoff/pause, not deterministic commercial copy.
- FR-011-024: Validator results must be persisted with severity, code, decision id, repair attempt count, and final disposition.

### Templates And Rendering

- FR-011-025: Approved templates are the voice layer. They may express approved language, chunk boundaries, channel variants, and required variables.
- FR-011-026: Templates must not contain branching logic that selects commercial strategy.
- FR-011-027: The renderer must render only conductor-selected templates that pass validator checks.
- FR-011-028: Final diagnostic rendering must preserve the approved staged order and must not truncate the last demo/next-step phrase.
- FR-011-029: WhatsApp rendering must respect no-buttons behavior, official links, chunk pacing, and the no-parallel-response rule for deferred inbound messages.

### Diagnostic

- FR-011-030: The diagnostic ledger must include and track all mandatory keys from the diagnostic contract: active students/size, main pain, pain detail, current process, priority, and urgency.
- FR-011-031: The agent must ask one diagnostic question at a time unless it is delivering the final staged diagnostic.
- FR-011-032: A simple answer like "120" to a pending student-count question must be accepted as an answer, not treated as misunderstanding.
- FR-011-033: An answered diagnostic field must not be asked again unless the conductor explicitly marks it ambiguous with evidence and the validator allows a clarification.
- FR-011-034: The final diagnostic must use natural, practical studio-owner language and must avoid weak/technical phrases banned by the diagnostic contract.

### Product, Price, Demo, Waitlist

- FR-011-035: Product questions such as "como funciona", WhatsApp behavior, integration, security, comparisons, and out-of-profile requests must be interpreted by the conductor using official product knowledge.
- FR-011-036: Prices, plan names, product limits, launch promises, checkout/access behavior, setup behavior, operational agent claims, and mode claims must come only from official product knowledge and the binding Spec 006 product contracts.
- FR-011-037: The agent must not invent checkout, discounts, launch dates, VIP status, or availability.
- FR-011-038: Waitlist can be offered only after clear fit/intent defined by the preserved contracts.
- FR-011-039: Demo/product-demo links and demo follow-up must preserve state: not offered, offered, viewed/asked-about, and post-diagnostic. The agent must treat commercial demo and product demo as the same customer-facing sales concept, while keeping technical references and video-production assets out of scope.

### Sales Inbox And Persistence

- FR-011-040: Sales Inbox is a persisted projection of runtime state and events, not a separate conversation brain.
- FR-011-041: Every meaningful turn must persist inbound message, decision JSON, rendered outbound messages, validator report, model usage/cost, diagnostic ledger, waitlist/demo/handoff state, and Sales Inbox projection.
- FR-011-042: A conversation eval cannot PASS unless the corresponding Sales Inbox projection is complete and consistent with runtime state.
- FR-011-043: Identity and contact fields must distinguish customer-provided, operator-provided, channel-provided, inferred, and unverified values.
- FR-011-044: Adapter/Sales Inbox inferred facts must not re-enter the conductor context as reliable customer-provided facts. They may re-enter only with source, confidence, and `inferred`/`unverified` labels, or after the conductor validates them from conversation evidence.
- FR-011-045: For every commercial case family, the expected Sales Inbox projection must be specified as part of the regression/eval fixture. A good transcript with incomplete or inconsistent Sales Inbox projection is a FAIL.

### Evals And Observability

- FR-011-046: Every normal commercial turn must record model usage. If a commercial turn produces customer-facing output without model usage, the eval must fail unless it is an explicitly allowed operational/safety/cold-greeting case.
- FR-011-047: Eval reports must include transcript, decision JSON, rendered output, validator results, repair status, model usage, Sales Inbox projection, and pass/fail reason.
- FR-011-048: PASS is invalid if the response is low quality, missing required behavior, skipped a required check, or only passed a structural assertion.
- FR-011-049: Runner-style events must make conductor role, selected templates, validators, repair, tool side effects, persistence, and delivery visible to operators/developers.
- FR-011-050: Template variables that carry customer-facing prose must be typed, bounded, grounded in evidence/product knowledge, and validated. A generic `message_text`, `freeform_response`, or whole-response variable is forbidden.
- FR-011-051: Validators must not trust conductor self-check booleans alone. Direct-question handling, official-fact usage, diagnostic completeness, and Sales Inbox consistency must be corroborated by structured evidence and rendered-output checks; semantic quality gaps require judge/manual review before PASS.
- FR-011-052: Each normal commercial turn must persist a trace containing input, typed context, conductor JSON, selected templates, validator report, repair attempts, rendered final message, model usage, runtime state diff, delivery/outbox events, and Sales Inbox projection.
- FR-011-053: Any implementation that can affect widget or landing behavior must capture or confirm current desktop and mobile `/pilates` baseline before code changes and verify no visual/layout drift before cutover.
- FR-011-054: Public cutover is a full production cutover, not a canary rollout, because the current production behavior is considered worse than the reset risk. It must still be feature-flagged or otherwise instantly reversible. Production activation is blocked until eval gates pass, rollback is tested, and first-hours monitoring/abort criteria are ready.

### Operational Gates And Anti-Regression

- FR-011-055: Every real commercial bug must be converted into a regression case before implementation. The new test must fail against the current system before the fix is accepted.
- FR-011-056: The required fix path for a commercial bug is regression case -> schema/context/prompt/validator/eval -> implementation. A direct tactical branch in `runner.py` or any equivalent commercial brain is forbidden.
- FR-011-057: CI/static audit must fail if commercial intent routing or customer-facing commercial answer selection is introduced through regex/if/token matching outside explicitly allowed operational/safety/cold-greeting modules.
- FR-011-058: Static audit must treat price, plan, demo, diagnostic, waitlist, "como funciona", Instagram/source openings, pain/dor, WhatsApp product questions, student counts, plan fit, objections, and mixed intent as forbidden deterministic commercial routing categories.
- FR-011-059: Product facts must be locked to official product knowledge and Spec 006 product contracts. Promises, prices, links, limits, availability, launch dates, checkout behavior, and operational-agent claims must not live in prompts, templates, tests, or ad hoc code.
- FR-011-060: Prompt, policy-pack, template, and product-knowledge changes are code changes. They require a reason, expected impact, transcript diff/eval before and after, and approval evidence before release.
- FR-011-061: The conductor decision schema must be versioned. Any field, enum, or structure change requires compatibility/migration consideration and eval coverage.
- FR-011-062: Golden transcripts must be versioned for at least price, pain-first, Instagram/source opening, WhatsApp product question, diagnostic, waitlist, human handoff, post-demo/product-demo, and long conversation flows.
- FR-011-063: A "do not do" fixture set must cover forbidden behavior: early phone capture, invented checkout, invented discount/date/VIP status, invented integrations/certifications, collecting client/studio WhatsApp numbers, calling students "client customers" when context requires students/alunos, and treating `497` as active students.
- FR-011-064: Cost optimization must prove lower token/cost profile without removing model usage from normal commercial turns or degrading golden transcript outcomes.
- FR-011-065: The reset must run in shadow mode before customer-facing cutover. Shadow mode runs the new core in parallel without responding to the lead and compares conductor decision, trace, rendered plan, and Sales Inbox projection against expected behavior.
- FR-011-066: Rollback must be tested, not only documented. Disabling the new core must lead to a safe operational fallback or controlled legacy quarantine path, not re-enable the old deterministic commercial brain as the active public responder.
- FR-011-067: Production rollout must use full activation with a first-hours emergency watch, not a staged canary. Trace quality, handoff behavior, Sales Inbox completeness, cost, model usage, fallback rates, duplicate/interleaved delivery, and P0 behavior must be monitored immediately after cutover.
- FR-011-068: Human handoff behavior requires dedicated audit coverage: requesting human pauses AI, human-active state produces no AI reply, and resume occurs only with explicit state/event evidence.
- FR-011-069: Every sensitive decision must be recorded in an approval log with decision, rationale, rejected alternatives, impact, and affected docs/code areas.

## Prohibitions

The new spec forbids:

- Regex-first, if-first, state-machine-first, or template-first commercial understanding.
- Post-LLM deterministic rewrites of commercial route, diagnostic action, waitlist eligibility, product answer, price answer, plan fit, or template ids.
- Turn Situation or Decision Compiler logic that maps raw customer text keywords such as price, demo, caro, agora, Instagram, WhatsApp, dor, alunos, or lista into commercial actions.
- Commercial fast paths that bypass the conductor.
- Tactical commercial patches in `runner.py` or any equivalent orchestration file.
- Old TS v2 conversation engine fallback for public widget/WhatsApp turns.
- Silent renderer defaults for semantic variables.
- Product facts outside official product knowledge.
- Product facts in prompts, templates, tests, or hardcoded fallbacks when they belong in official product knowledge or Spec 006.
- Customer-facing internal metadata, schema labels, route labels, source labels, or prompt fragments.
- Eval PASS without transcript quality and Sales Inbox consistency.
- Untyped or unbounded template variables that act as free-form assistant messages.
- Treating adapter/Sales Inbox inferred facts as reliable conversation truth without source/confidence labels.
- Public cutover without shadow mode, tested feature flag rollback, first-hours emergency watch, and `/pilates` baseline gate where widget behavior is affected.
- Adding behavior to a large runner/orchestrator file when it belongs in policy, schema, validator, renderer, projection, or eval.
- Re-enabling the old deterministic commercial engine as the public rollback path.

## Acceptance Criteria

- AC-011-001: Architecture and tasks can be implemented without changing `/pilates`.
- AC-011-002: A normal widget turn and a normal WhatsApp turn use the same conductor/core.
- AC-011-003: The current bug list is represented in regression cases.
- AC-011-004: No future implementation task requires connecting client/studio WhatsApps.
- AC-011-005: Every preserved Spec 010 contract has an explicit home in the new architecture.
- AC-011-006: Every allowed deterministic path is enumerated and testable.
- AC-011-006A: Every major conversation mode has a documented action menu and tests proving the LLM receives that menu and chooses an allowed action.
- AC-011-006B: Static audit fails if raw-text keyword logic chooses commercial action, diagnostic slot, waitlist/demo/handoff action, or template group outside the LLM action decision.
- AC-011-007: The reset has an anti-monster rule: no module may own more than one pipeline responsibility, and no helper may both interpret commercial meaning and produce customer-facing text.
- AC-011-008: Template variables are registered with type, max shape, grounding source, and validator rules before implementation.
- AC-011-009: Widget cutover tasks include `/pilates` desktop/mobile baseline confirmation and rollback proof.
- AC-011-010: Every real bug targeted by the reset has a regression case that fails against the current system before code changes.
- AC-011-011: Static audit can block forbidden commercial regex/if/template-first routing in CI.
- AC-011-012: Every normal commercial turn emits the mandatory trace fields and model usage.
- AC-011-013: Golden transcripts and "do not do" fixtures are versioned and included in release gates.
- AC-011-014: Shadow mode and full-production emergency watch are required before/at production activation; staged canary is intentionally not required for this reset.
- AC-011-015: Rollback proof shows the old deterministic commercial brain does not become the active public responder.
- AC-011-016: Each task closure satisfies the Definition of Done below.

## Definition Of Done

No implementation task under Spec 011 is complete unless all applicable items are true:

- A regression case or fixture exists for the behavior.
- For real bug fixes, the new regression test fails against the current system before the fix.
- Unit/contract tests pass for touched deterministic components.
- Static audit shows no new forbidden commercial regex/if/template-first path.
- Normal commercial turns include model usage unless explicitly allowed as operational/safety/cold-greeting.
- Mandatory trace contains input, context, conductor JSON, selected templates, validators, repair, final message, model usage, delivery events, and Sales Inbox projection.
- Sales Inbox projection is complete and consistent with runtime state.
- Template variables are typed, bounded, grounded, and registered; no generic free-form response variable is introduced.
- Product facts come from official product knowledge and Spec 006 product contracts.
- Golden transcripts do not regress, including transcript, decision JSON, rendered text, and Sales Inbox projection.
- Human handoff state remains correct when touched.
- `/pilates` desktop/mobile baseline shows no visual/layout drift when widget or landing behavior is affected.
- Feature flag and rollback behavior remain intact when cutover path is touched.
- Product-owner approval is recorded for the required transcript groups before production activation.
- `coverage-map.md` is updated with linked evidence for every affected requirement, regression case, and acceptance criterion.

## Decisions Requiring Confirmation Before Implementation

- D-011-001: Confirm the recommended one-conductor architecture instead of full multi-agent SDK handoffs on normal turns.
- D-011-002: Confirm implementation details for the already recommended path: create a new small core beside `runtime/runner.py`, quarantine legacy runner, and cut over behind a controlled flag. Refactoring `runner.py` in place is rejected for this reset.
- D-011-003: Confirm hard size/ownership limits for the new core modules. Recommendation: each module owns one responsibility; any file approaching 700 lines requires split/review.
- D-011-004: Confirm exact approved customer-facing wording variants for the diagnostic "CRM base" concept. Binding default: use plain studio language such as "base organizada" and "sistema" unless the lead asks about CRM or an approved template explicitly requires CRM.
- D-011-005: Confirm repair-call budget. Recommendation: one repair call per failed conductor turn, then safe operational fallback/handoff.
- D-011-006: Confirm the minimum real-OpenAI eval suite size and budget before production approval.
- D-011-007: Confirm whether later Sales Inbox implementation may add/adjust data fields without redesigning the UI.
- D-011-008: Confirm production cutover/rollback plan after the docs and eval gates are approved.
- D-011-009: Confirm whether semantic quality verification should use a separate judge model, manual review only, or both. Recommendation: deterministic validators first, then judge for broad transcript triage, then manual product-owner approval for release.
- D-011-010: Confirm the minimum shadow-mode duration/sample size before full production cutover.
- D-011-011: Confirm the full-cutover abort criteria and production monitoring dashboard fields.
- D-011-012: Confirm the approval-log owner and where approval evidence is stored.
- D-011-013: Confirm the action-first correction before another paid T011-105 attempt: add Turn Situation Builder, smaller `ConductorActionDecision`, Decision Compiler, and action-level repair so paid evidence is not used to discover more unconstrained render-plan failures.
