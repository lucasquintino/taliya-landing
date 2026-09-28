# Design Lock - Spec 012

Status: PARTIALLY SUPERSEDED on 2026-06-10 by `design-lock-v2-action-first.md`
(D-012-012). This document remains valid for the SDK motor choice, scope
boundaries, trace/cost policy, and abort criteria. The LLM-template boundary
described here (SDK output adapted to a full `TaliyaTurnProposal` chosen by
the model) is superseded: production follows the action-first pipeline. On
any conflict, v2 wins.

Original status: locked for isolated SDK spike. Production implementation still requires spike evidence.

This document closes the no-code design lock for the Agents SDK path. It is based on the local `openai-agents` package check and the official Agents SDK docs read on 2026-06-05.

## SDK Baseline

- Local package: `agents` version `0.17.3`.
- Verified symbols: `Agent`, `Runner`, `function_tool`, `handoff`, `input_guardrail`, `output_guardrail`, `RunContextWrapper`.
- Official docs used: Agents SDK overview, orchestration/handoffs, guardrails, results/state, and agent evals.

## Core Decision

Use OpenAI Agents SDK as the commercial orchestration motor.

The SDK owns:

- agent definitions;
- specialist handoffs;
- tool invocation semantics;
- input/output guardrails;
- runner execution;
- SDK run items and trace visibility.

Taliya owns:

- channel adapters;
- turn gate, lock, idempotency;
- context builder;
- product knowledge sources;
- RAG/retrieval policy and official fact refs;
- strict proposal schema;
- contract validators;
- approved template renderer;
- state commits;
- Sales Inbox projection;
- delivery/outbox;
- feature flags, shadow mode, rollback, and eval gates.

## Target Topology

Use a hybrid topology:

- `taliya_triage_agent` starts first-turn or unclear-state conversations.
- `taliya_entry_agent` handles cold, source/social, widget opening, and broad interest turns.
- `taliya_product_agent` handles product, price, WhatsApp scope, demo, integration, security, and objections.
- `taliya_diagnostic_agent` conducts the diagnostic and proposes ledger updates.
- `taliya_waitlist_agent` handles qualified waitlist/buying intent.
- `taliya_handoff_agent` handles human handoff and pause proposals.
- `taliya_safety_guardrails` run before and after SDK reasoning where appropriate.

Starting agent policy:

- If persisted `current_sdk_agent` is known and not stale, start there.
- If there is no reliable current agent, start at `taliya_triage_agent`.
- This is state-based operational selection, not raw-text commercial routing.
- Commercial meaning still comes from the SDK agent run.

Handoff policy:

- Real SDK handoffs are allowed when the current agent needs another specialist.
- Normal known-state turns should usually require one model operation.
- Triage plus specialist handoff is allowed for unclear or first meaningful turns.
- Repair/escalation is capped at one additional model operation.

## TaliyaTurnProposal Schema

The SDK final output must adapt to `TaliyaTurnProposal`.

The schema is a proposal, not a rendered response and not a state commit.

Required top-level fields:

```text
turn_id
conversation_id
channel
starting_agent
agent_path
commercial_understanding
answer_obligations
product_claims
diagnostic_proposal
demo_proposal
waitlist_proposal
handoff_proposal
template_proposal
safety
state_patch_proposal
sales_inbox_projection_proposal
delivery_proposal
confidence
risks
usage
```

Required semantics:

- `agent_path` records SDK agents, handoffs, tools, and guardrail outcomes.
- `commercial_understanding` includes intents, direct question, pain/context, source context, mixed intent, extracted facts, and evidence snippets.
- `answer_obligations` lists what must be answered before steering.
- `product_claims` contains only claims tied to official product fact refs.
- `diagnostic_proposal` proposes ledger updates and next/final diagnostic status with evidence.
- `template_proposal` contains approved template ids and typed variables only.
- `state_patch_proposal` is non-committed and must pass validators before persistence.
- `delivery_proposal` is a chunk/render plan, not final raw SDK text.
- `usage` records model operations, tokens when available, handoffs, repairs, and estimated cost.

Forbidden fields:

- whole-response `final_text` for direct delivery;
- untyped generic `message`;
- unchecked product facts;
- state commit flags controlled directly by model reasoning;
- hidden route/action enum that becomes the real brain.

## Validator Boundary

Validators must enforce:

- direct question first;
- official product claims only, with claim-to-fact-ref grounding;
- no price/student-count confusion;
- diagnostic completeness and no repeated questions;
- no internal/source label leakage;
- no premature waitlist;
- human handoff pause state;
- renderer variable completeness;
- Sales Inbox projection consistency;
- trace completeness and model usage.

Validators must not:

- infer commercial route from raw lead text;
- rewrite SDK-selected commercial meaning into another route;
- become a new decision compiler;
- contain a large repair library for conversational quality.

## Renderer Boundary

Renderer input is:

- approved template ids;
- typed, bounded semantic variables;
- official product fact refs;
- validated state/proposal.

Renderer must fail if:

- required variables are missing;
- product facts lack official refs;
- a whole free-form SDK response is presented as output;
- generic fallback copy would hide a missing variable.

## RAG Boundary

The RAG layer is explicit in `rag-policy.md`.

RAG retrieves official facts and source refs. It does not classify lead intent, choose the commercial route, choose waitlist eligibility, or write the final answer. The SDK agent decides what facts are needed and proposes grounded claims. Validators enforce `claim -> fact_ref -> source_id -> validator result` before rendering.

## Cost And Model Policy

Design target:

- normal known-state commercial turn: one SDK model operation;
- first unclear turn: triage plus one handoff allowed;
- repair/escalation: at most one extra model operation;
- no eval/judge call in production path unless explicitly approved later;
- no deterministic commercial shortcut to reduce cost.

Paid run policy:

- mocked/no-cost spike must pass first;
- paid spike packet must estimate model operations and cost;
- user must approve paid run before execution;
- every paid run records exact usage/cost in the ledger.

## Abort Criteria

Abort or redesign before production SDK implementation if:

- SDK path needs a new large custom compiler to work;
- SDK path cannot beat Spec 011 on conversational understanding in critical spike scenarios;
- output quality only works by delivering SDK free-form text directly;
- tool side effects cannot be kept read-only/proposal-only during reasoning;
- cost can only be controlled by adding deterministic commercial routing;
- trace/run items cannot support evals, debugging, and Sales Inbox projection;
- static audit cannot distinguish SDK orchestration from handcrafted action-first orchestration.

## First Implementation Step Allowed

Only after this design lock:

1. create isolated SDK spike files under the planned SDK module path;
2. keep public endpoint unchanged;
3. use mocked/no-cost tests first;
4. do not run paid OpenAI calls until approval;
5. update `implementation-ledger.md` after the task closes.
