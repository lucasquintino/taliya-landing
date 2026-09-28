# T012-032B Slice - Delta Contract Compiler Coverage

Date: 2026-06-11

## Scope

Started T012-032B with no-cost action-first coverage for the product follow-up
delta contract.

Covered in this slice:

- structured actions for comparison, security/data, availability/onboarding,
  and out-of-profile product routes;
- compiler mapping from those LLM-selected actions to approved product
  templates;
- official-fact summary selection from `product_fact_keys_used`;
- required template-variable enforcement for new and existing compiler plans;
- no-checkout/no-discount/no-exact-date guard coverage for availability.

This is an isolated compiler/runner slice. It does not add public endpoint
cutover and does not run paid OpenAI calls.

## Sources

- `specs/010-openai-cs-agents-adaptation-for-taliya-commercial/product-followup-delta-contract.md`
  - requires the model to remain the conversation brain;
  - forbids raw-text branches such as `if text contains "planilha"`;
  - adds product keys for how-it-works, WhatsApp scope, integration scope,
    comparisons, security/data, availability/onboarding, and out-of-profile;
  - adds the product follow-up templates and safe promise limits.
- `specs/012-taliya-commercial-agent-agents-sdk-migration/conformity-matrix.pt-BR.md`
  - maps the new product knowledge keys, delta templates, and new intents to
    T012-032B.
- `specs/012-taliya-commercial-agent-agents-sdk-migration/design-lock-v2-action-first.md`
  - preserves the action-first pipeline: LLM action decision, compiler
    expansion, validators, renderer, then commit.
- `.agents/skills/taliya-llm-first-agent/SKILL.md`
  - deterministic code may validate/render/retrieve official facts, but must
    not become the commercial interpretation brain.

## Files Changed

- `services/taliya-agent-runtime/app/core/taliya_commercial_sdk/conductor_decision.py`
- `services/taliya-agent-runtime/app/core/taliya_commercial_sdk/decision_compiler.py`
- `services/taliya-agent-runtime/app/core/taliya_commercial_sdk/action_validators.py`
- `services/taliya-agent-runtime/app/core/taliya_commercial_sdk/action_turn_runner.py`
- `services/taliya-agent-runtime/tests/test_spec012_conductor_decision.py`
- `services/taliya-agent-runtime/tests/test_spec012_decision_compiler.py`
- `services/taliya-agent-runtime/tests/test_spec012_action_turn_runner.py`

## Behavior

The LLM can now select explicit product-follow-up actions:

- `answer_comparison_current_tool`;
- `answer_security_and_data`;
- `answer_availability_and_onboarding`;
- `answer_out_of_profile`.

The compiler maps those actions to approved templates and state transitions.
The resolver uses the structured `product_fact_keys_used` list to choose the
official product summary, instead of inspecting the lead's raw text.

This keeps meaning selection in the LLM and leaves deterministic code with the
allowed jobs: action expansion, official fact retrieval, template-variable
enforcement, validation, and rendering.

## Tests

Run from `services/taliya-agent-runtime`:

- `python -m pytest tests\test_spec012_decision_compiler.py -q`
  - result: 13 passed
- `python -m pytest tests\test_spec012_action_turn_runner.py tests\test_spec012_decision_compiler.py -q`
  - result: 19 passed
- `python -m pytest tests\ -k spec012 -q`
  - result: 136 passed, 716 deselected
- `python -m ruff check app\core\taliya_commercial_sdk tests\test_spec012_decision_compiler.py tests\test_spec012_action_turn_runner.py tests\test_spec012_conductor_decision.py tests\test_spec012_action_validators_ported.py tests\test_spec012_static_audit.py tests\test_spec012_action_safety.py`
  - result: all checks passed

## Anti-Determinism Review

No raw lead-text commercial router was added. The new product routes are
reachable only through the structured `ConductorActionDecision` action and
`product_fact_keys_used` fields selected by the LLM. The compiler does not
contain a `current_user_text` parameter and does not infer comparison,
security, availability, or out-of-profile from text tokens.

The added deterministic checks are form and safety boundaries: required
template variables, official-fact sourcing, and rejected unsafe promises.

## Protected Scope

No `/pilates`, landing visual, Sales Inbox UI, checkout, multi-tenant, or
client/studio WhatsApp files were edited.

## Paid Calls

None.

## Still Open

- complete the remaining T012-032B delta items: post-diagnostic compact
  context, conversation resume, general objections, diagnostic refusal
  strengthening, and name-policy behavior;
- add broader mocked canonical fixtures under T012-038/038B for messy inputs,
  corrections, and diagnostic interruptions;
- later, after explicit approval only, gather real LLM evidence for the new
  commercial product-follow-up routes.
