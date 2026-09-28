# T012-032B Routine Areas Delta Slice

Date: 2026-06-11

## Scope

Added no-cost action-first coverage for the `routine_areas` product-knowledge
delta key.

This slice keeps the LLM-first boundary:

- the model still chooses the action and declares `product_fact_keys_used`;
- deterministic code only resolves the declared official fact key, compiles the
  approved template, validates, renders, and commits after validation;
- no raw lead-text commercial routing, regex classifier, or template-first
  shortcut was added.

## Files Changed

- `services/taliya-agent-runtime/app/core/taliya_commercial_sdk/conductor_decision.py`
- `services/taliya-agent-runtime/app/core/taliya_commercial_sdk/decision_compiler.py`
- `services/taliya-agent-runtime/app/core/taliya_commercial_sdk/action_turn_runner.py`
- `services/taliya-agent-runtime/app/core/taliya_commercial_sdk/action_agents.py`
- `services/taliya-agent-runtime/tests/test_spec012_action_turn_runner.py`

## Behavior Covered

- `routine_areas` is now documented in the strict action-decision schema as an
  official product fact key.
- The compiler can map `routine_areas` to `product.overview_short`, so area/routine
  questions can be answered through an approved rendered template instead of direct
  SDK text.
- The official fact resolver formats the `routine_areas` dictionary from
  product knowledge into `product_fact_summary`, preserving
  `official_product_knowledge` source and `product_knowledge.routine_areas`
  evidence.
- A mocked SDK conversation proves a routine-area question is answered with
  official source content and zero paid OpenAI calls.

## Tests Run

- `python -m pytest services/taliya-agent-runtime/tests/test_spec012_action_turn_runner.py -q`
  - Result: `10 passed`

## Protected Scope Review

No `/pilates`, landing visual, Sales Inbox UI, multi-tenant, client/studio
WhatsApp, checkout, or public endpoint files were changed.

## Paid Call Review

No paid OpenAI call was made. The conversation proof uses `ScriptedFakeModel`.

## Open Items

T012-032B remains open overall. Remaining work includes broader product delta
fixtures/quality proof and any production endpoint integration only after the
allowed task gate.
