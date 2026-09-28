# Eval Plan - Spec 012 Agents SDK Migration

Revision 2026-06-10 (D-012-012, binding additions from spike evidence):

- The fixture source of truth is `011/regression-cases.md` plus
  `011/do-not-do-static-fixtures.json` (T012-038), extended by T012-038B with
  the uncovered cells: interruption matrix (question type x phase), answer
  correction, multiple answers in one message, objection mid-diagnostic,
  resume after days, and MESSY REAL-WORLD INPUT (typos, abbreviations like
  "qto fica?", slang, no punctuation) - interpretation is proven on clean
  Portuguese only.
- The release measure is the `010/contracts/eval-contract.md` gate: Layer 1
  deterministic invariants, Layer 2 multi-turn scenarios, Layer 2B real
  provider, Layer 3 quality judge (P1 average >= 4.2/5, none below 4.0).
  "Structural pass" is NEVER a success measure (spike lesson: ideal-conversation
  run 1 passed 12/12 structурal with a commercially broken conversation).
- Release-gate batteries run 3x consecutively (variance policy); development
  iterations are no-cost dry-runs only.
- A multi-turn conversation layer (commit-after-validation state between
  turns, per the spike `ideal_conversation` harness) is mandatory alongside
  single-turn scenarios.

Purpose: reuse the Spec 011 quality bar while adding SDK-specific proof: agents, handoffs, tools, guardrails, and run traces.

## Principle

PASS means the SDK agent actually serves the lead well. It does not mean only that the SDK ran, a schema parsed, or a handoff occurred.

## Eval Layers

### Layer 1 - Static Audit

Block:

- raw-text commercial routing outside SDK agents;
- old TS v2 public fallback;
- `runtime/runner.py` as public commercial brain;
- product facts in prompts/templates/tests/fallbacks outside official sources;
- generic whole-response template variables;
- renderer semantic defaults;
- SDK tools that commit production state during reasoning without explicit approval;
- huge new SDK runner/adapter files combining responsibilities.

### Layer 2 - SDK Contract Tests

Test without paid model calls:

- agent graph is declared;
- handoff relationships are explicit;
- tools are typed and classified read-only/proposal/commit;
- commit tools are not exposed to free SDK reasoning;
- output schema rejects free-form final messages;
- trace adapter captures SDK run items;
- runtime adapter does not deliver before validators.
- product claims without approved fact refs fail.
- RAG/product retrieval does not route commercial turns from raw lead text.

### Layer 3 - Mocked SDK Run Items

Use mocked SDK output/run items to test:

- tool-call mapping;
- handoff mapping;
- proposal adaptation;
- validator failures;
- renderer boundary;
- persistence/projection;
- shadow mode;
- rollback.

### Layer 4 - Real Model Spike

Run the spike scenarios from `spike-plan.md` with explicit budget approval.

Reports must include:

- input transcript;
- start agent;
- agent path/handoffs;
- tool calls and outputs;
- SDK final output;
- `TaliyaTurnProposal`;
- validator result;
- rendered messages;
- runtime state diff;
- Sales Inbox projection;
- usage/cost;
- pass/fail reason.

### Layer 5 - Golden And Do-Not-Do

Reuse Spec 011:

- golden transcripts;
- do-not-do fixtures;
- product-followup delta cases;
- diagnostic final cases;
- long conversation cases;
- Sales Inbox projection cases.
- RAG grounding cases for price, WhatsApp scope, missing facts, and unsupported claims.

The SDK path cannot pass release if any Spec 011 P0/P1 gate regresses.

### Layer 6 - Manual Review

Manual product-owner review remains mandatory for:

- final diagnostic transcripts;
- product/price/demo transcripts;
- waitlist transcripts;
- WhatsApp chunking/deferred inbound;
- trace samples;
- Sales Inbox projection samples.

## SDK-Specific PASS Invalidators

Mark FAIL if:

- SDK free-form output is delivered directly to lead;
- SDK tool commits unvalidated commercial state;
- SDK handoff is not persisted in trace;
- SDK agent path is missing from eval report;
- SDK trace cannot explain why a specialist answered;
- current-agent persistence causes stale specialist behavior;
- Taliya validators are skipped because SDK guardrails passed;
- model usage is missing on normal commercial turn;
- SDK path uses deterministic raw-text route before the model.

## Cost Reporting

Every SDK eval report must show:

- model;
- number of SDK model operations;
- tool calls;
- handoff count;
- repair/escalation count;
- input/output tokens where available;
- estimated cost;
- comparison to current Spec 011 run if available.

Cost alone cannot fail a good spike, but high cost must be visible before implementation.
