# Action Contract - Taliya Commercial Agent

Purpose: define the corrected Spec 011 conductor contract after the T011-105 paid failures. This contract keeps the agent LLM-first while making each turn state-aware, action-first, and harder for the model to break structurally.

## Core Principle

The core prepares the board. The LLM plays the turn.

Deterministic code may compute the current situation from persisted state, but it must not infer commercial meaning from raw lead text. The LLM must still interpret the inbound message and choose the action.

## Corrected Pipeline

```text
Channel Adapter
-> Runtime API
-> Turn Gate
-> Context Builder
-> Turn Situation Builder
-> LLM Action Conductor
-> Decision Compiler
-> Contract Validators
-> Focused Repair
-> Template Renderer
-> Persistence / Projection
-> Delivery / Outbox
```

## Turn Situation Builder

Allowed inputs:

- persisted runtime state;
- diagnostic ledger;
- waitlist, demo, and handoff state;
- channel/source metadata;
- latest inbound envelope, but not raw-text commercial interpretation;
- official product knowledge keys available to the turn;
- delivery/outbox state.

Allowed outputs:

- `mode`: entry, diagnostic, post_diagnostic, product, price, demo, waitlist, handoff, safety, delivery_deferred;
- `pending_question_key`, when the next diagnostic answer is expected;
- `completed_diagnostic_keys` and `missing_diagnostic_keys`;
- `allowed_actions`;
- `required_obligations`;
- `eligible_template_groups`;
- `official_fact_keys_available`;
- `state_constraints`;
- `forbidden_actions_now`.

Forbidden outputs:

- final commercial route from raw text;
- captured diagnostic slot from raw text;
- price/demo/objection/source/pain/waitlist intent from keyword matching;
- final customer-facing text;
- final template plan selected from raw text.

## Action Decision Schema

The LLM should return a small `ConductorActionDecision`, not a full render/state plan.

Required fields:

- `schema_version`;
- `decision_id`;
- `turn_id`;
- `selected_action`;
- `interpreted_intents`;
- `direct_question`;
- `direct_answer_obligations`;
- `captured_slots`;
- `product_fact_keys_used`;
- `numeric_interpretations`;
- `diagnostic_intent`;
- `demo_intent`;
- `waitlist_intent`;
- `handoff_intent`;
- `reply_goal`;
- `confidence`;
- `evidence`;
- `needs_clarification`;
- `repair_hints`.

The LLM must choose `selected_action` only from `TurnSituation.allowed_actions`.

The LLM must not return:

- final `previous_state/current_state/next_state`;
- final `template_plan`;
- final rendered text;
- whole-response variables;
- hidden commercial fallback text.

## Decision Compiler

The compiler converts a valid `ConductorActionDecision` plus `TurnSituation` into the existing validated runtime shape.

It owns deterministic derivation of:

- state transition;
- diagnostic ledger merge;
- required final diagnostic staged delivery;
- allowed template group expansion;
- required template variables when the source is official product knowledge or runtime state;
- Sales Inbox projection inputs;
- render plan skeleton.

It must not:

- override the LLM's interpreted commercial intent;
- turn raw-text keywords into commercial actions;
- invent customer-facing semantic prose;
- select a commercial action that the LLM did not choose.

## Mode Action Menus

### Entry

Allowed actions:

- `answer_general_interest`;
- `answer_source_opening`;
- `offer_diagnostic_from_pain`;
- `answer_direct_product_question`;
- `start_requested_diagnostic`;
- `handoff_requested`;
- `clarify_ambiguous_opening`.

### Diagnostic

Allowed actions:

- `capture_pending_diagnostic_answer`;
- `answer_direct_question_then_continue_diagnostic`;
- `ask_next_diagnostic_question`;
- `complete_diagnostic`;
- `clarify_ambiguous_diagnostic_answer`;
- `respect_diagnostic_refusal`;
- `handoff_requested`.

### Post Diagnostic

Allowed actions:

- `answer_product_question_with_saved_context`;
- `send_demo`;
- `answer_price_objection_with_context`;
- `offer_or_join_waitlist_if_eligible`;
- `handoff_requested`;
- `ask_demo_reaction`;
- `clarify_ambiguous_followup`.

### Product / Price / Demo

Allowed actions:

- `answer_price`;
- `answer_plan_fit_with_diagnostic_offer`;
- `answer_how_it_works`;
- `answer_whatsapp_scope`;
- `answer_integration_scope_safely`;
- `send_demo`;
- `answer_price_objection`;
- `offer_diagnostic_after_answer`;
- `clarify_product_question`;
- `handoff_requested`.

### Waitlist

Allowed actions:

- `offer_waitlist`;
- `collect_waitlist_missing_detail`;
- `join_waitlist`;
- `decline_waitlist`;
- `answer_question_then_continue_waitlist`;
- `handoff_requested`.

### Handoff

Allowed actions:

- `pause_for_human`;
- `resume_only_with_explicit_resume_event`;
- `suppress_ai_reply_while_human_active`.

## Anti-Determinism Boundary

The following are forbidden outside the LLM action decision:

- `if "demo" in text` deciding demo;
- `if "caro" in text` deciding objection;
- `if "agora" in text` deciding urgency;
- regex deciding price, plan, pain, diagnostic acceptance, waitlist, or handoff;
- template selection from raw customer text;
- state transition from raw customer text.

The following are allowed:

- using raw text as part of the LLM input;
- using normalized text for product-knowledge retrieval hints only;
- using raw text for safety/prompt-injection/unsupported-media boundaries;
- using persisted pending question to constrain the LLM action menu;
- compiling a chosen LLM action into deterministic state/rendering.

## Required Quality Gates

Before another paid T011-105 batch:

- local tests must prove the action menu is present for every major mode;
- local tests must prove every exposed `TurnAction` is explicitly compiled or operationally handled, with no pending action bucket before paid readiness;
- mixed-intent messages must still call the LLM;
- static audit must fail if raw-text keyword logic chooses commercial action;
- long conversation preflight must cover pending urgency, demo after failed final, price objection after diagnostic, waitlist intent, and how-it-works post-diagnostic;
- renderer missing-variable failures must be caught before render and repaired through action-level repair or compiler fallback to a valid approved action shape.
