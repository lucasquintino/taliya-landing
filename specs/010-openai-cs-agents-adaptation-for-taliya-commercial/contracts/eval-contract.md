# Contract: Evaluation

## Eval Layers

### Layer 1: Deterministic Invariants

These failures block release regardless of judge score:

- cold greeting offers diagnostic, waitlist, name capture, phone capture, or plan list
- source opening violates `behavior-contract.md`
- direct question is not answered before steering
- invented checkout
- invented link
- incorrect price or plan claim
- missing product source for commercial facts
- asking WhatsApp user for phone number
- responding while human handoff is active
- duplicate reply to duplicate webhook
- waitlist side effect duplicated
- system prompt or secret leak
- diagnostic claims facts not in evidence
- diagnostic starts or continues with a dry question and no grounded feedback
- completed diagnostic omits hold message, CRM base, per-agent recommendations, dynamic plan line, or dynamic demo line
- completed diagnostic renders rejected old final formats
- completed diagnostic recommends plan before CRM/operational logic
- completed diagnostic skips demo bridge
- waitlist offered without clear intent to contract
- waitlist offered from demo curiosity alone
- mapped behavior lacks approved template ids
- diagnostic repeats a question already answered with sufficient evidence
- diagnostic completes before mandatory ledger completion
- Sales Inbox misses required fields for a meaningful turn
- widget or WhatsApp delivery produces a text wall
- eval exceeds max scenario/model-call/cost cap
- final approval based only on mock/smoke/string checks

Zero-cost local gates for templates, renderer, state transitions, diagnostic ledger, waitlist intent, Sales Inbox completeness, idempotency, ordering, and channel delivery must pass before broad real OpenAI evals run.

### Layer 2: Multi-Turn Scenario Runner

Scenarios must cover:

- cold "oi"
- cold "bom dia"
- reliable profile name
- unreliable profile name
- widget opening
- site CTA/forced message
- Instagram/Facebook opening
- diagnostic CTA opening
- direct price question
- price plus fit question
- ambiguous mixed message
- diagnostic accepted with rich context
- diagnostic requested with thin context
- diagnostic direct request with no reliable name
- diagnostic in progress with answer feedback before next question
- completed staged diagnostic with demo not yet offered
- completed staged diagnostic with demo already offered
- diagnostic uses pre-answered facts without repeating questions
- diagnostic rejected
- waitlist too early
- waitlist qualified by clear contract intent
- positive demo reaction plus clear next-step intent
- positive demo reaction without clear next-step intent
- diagnostic positive without contract intent
- direct buying intent
- human request
- manual WhatsApp Business App reply
- unsupported media
- prompt injection
- repeated/out-of-order conversation
- widget short-message delivery
- WhatsApp text/link equivalent for widget button
- Sales Inbox completeness

### Layer 2B: Real OpenAI Behavior Gate

Before production readiness, mapped P1 behavior scenarios must run with the real OpenAI provider and no mock fallback. The report must include full visible transcripts, route, specialist role, policy checks, usage, estimated cost, and blocking-failure status.

### Layer 3: LLM Quality Judge

Judge dimensions:

- directness
- naturalness
- usefulness
- commercial clarity
- evidence use
- diagnostic quality
- waitlist timing
- safety and honesty
- brevity and channel fit
- no robotic phrasing

Scores:

- 5: excellent
- 4: acceptable only if the transcript has no blocking failure and product-owner review agrees it matches the behavior contract
- 3: needs improvement
- 2: poor
- 1: blocking quality failure

Minimum gates:

- Final mapped P1 behavior scenarios average at least 4.2.
- No mapped P1 scenario may score below 4.0.
- Blocking failures fail regardless of average.

## Eval Output

Each eval report must include:

- run id
- agent key
- scenario ids
- transcript
- structured outputs
- tool calls
- handoffs
- guardrails
- product source versions
- model usage and cost
- deterministic invariant results
- judge scores and rationale
- skipped scenarios
- final pass/fail

## Budget Controls

Eval runner must support:

- dry run
- max scenarios
- max real model calls
- max estimated cost
- stop reason

Skipped scenarios are not failures, but they cannot count as passed.
