# T012-032B Slice - Post-Diagnostic Memory And Policy

Date: 2026-06-11

## Scope

Advanced T012-032B with no-cost action-first coverage for:

- compact post-diagnostic context in the turn situation;
- general objection and conversation-resume policy in the product agent;
- diagnostic-refusal policy in the diagnostic agent;
- mocked compiler proof that a diagnostic refusal with a direct price question
  answers price without re-offering diagnostic in the same turn.

This is an isolated SDK-core slice. It does not add public endpoint cutover and
does not run paid OpenAI calls.

## Sources

- `specs/010-openai-cs-agents-adaptation-for-taliya-commercial/product-followup-delta-contract.md`
  - post-diagnostic context payload;
  - general objections handled by LLM + policy first, without deterministic
    branches/templates in the first pass;
  - diagnostic refusal must respect the refusal and answer the direct question.
- `specs/010-openai-cs-agents-adaptation-for-taliya-commercial/behavior-contract.md`
  - post-diagnostic memory fields and refusal/resume behavior.
- `specs/012-taliya-commercial-agent-agents-sdk-migration/conformity-matrix.pt-BR.md`
  - maps post-diagnostic compact context, new intents, refusal, resume, and
    objections to T012-032B.
- `.agents/skills/taliya-llm-first-agent/SKILL.md`
  - LLM remains the commercial brain; deterministic code may package state and
    validate/render, but must not classify commercial meaning from raw text.

## Files Changed

- `services/taliya-agent-runtime/app/core/taliya_commercial_sdk/turn_situation.py`
- `services/taliya-agent-runtime/app/core/taliya_commercial_sdk/action_agents.py`
- `services/taliya-agent-runtime/tests/test_spec012_turn_situation.py`
- `services/taliya-agent-runtime/tests/test_spec012_action_agents.py`
- `services/taliya-agent-runtime/tests/test_spec012_decision_compiler.py`

## Behavior

`TurnSituation` now exposes `post_diagnostic_context` only when persisted state
is already post-diagnostic. The context is compact and source-limited:

- `pain_context_human`;
- `likely_cause`;
- `first_recommended_step`;
- `recommended_area`;
- `indicated_agents`;
- `recommended_plan_or_range`;
- `demo_status`;
- `waitlist_status`;
- `unknowns`.

The product agent instruction explicitly covers general objections and
conversation resume using that saved context. The diagnostic agent instruction
explicitly covers diagnostic refusal: answer the direct matter when present and
do not offer diagnostic again in the same turn.

## Tests

Run from `services/taliya-agent-runtime`:

- `python -m pytest tests\test_spec012_turn_situation.py tests\test_spec012_action_agents.py tests\test_spec012_decision_compiler.py -q`
  - result: 32 passed
- `python -m pytest tests\ -k spec012 -q`
  - result: 143 passed, 716 deselected
- `python -m ruff check app\core\taliya_commercial_sdk tests\test_spec012_turn_situation.py tests\test_spec012_action_agents.py tests\test_spec012_decision_compiler.py tests\test_spec012_action_turn_runner.py tests\test_spec012_action_validators_ported.py tests\test_spec012_static_audit.py tests\test_spec012_action_safety.py`
  - result: all checks passed

## Anti-Determinism Review

No raw lead-text route, regex, or token list was added. The compact context is
derived only from persisted diagnostic/demo/waitlist state. General objection,
conversation resume, and diagnostic refusal remain LLM-selected structured
intents/actions; deterministic code only packages memory, compiles the selected
action, and enforces the no-reoffer form boundary in tests.

## Protected Scope

No `/pilates`, landing visual, Sales Inbox UI, checkout, multi-tenant, or
client/studio WhatsApp files were edited.

## Paid Calls

None.

## Still Open

- broaden general-objection and conversation-resume fixtures;
- implement/verify name policy;
- complete the canonical Spec 011 fixture port under T012-038;
- gather real-model evidence only after explicit paid approval.
