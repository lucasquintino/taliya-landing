# Validators T011-069A Product Claims Manual Report

Status: passed for isolated Spec 011 core validator scope.

Task: `T011-069A - Validate product claims against official product knowledge and Spec 006 product contracts`.

## Scope

This task added product-claim validation over structured template variables. It
did not parse inbound text, choose routes, answer product questions, render
messages, repair decisions, produce fallback, change product knowledge, change
`/pilates`, cut over adapters, or touch `runtime/runner.py`.

## Red Baseline

Command:

```powershell
cd services/taliya-agent-runtime
python -m pytest tests/test_spec011_validators_product_claims.py -q
```

Observed before implementation:

```text
3 failed, 1 passed
```

Failures showed that a product-claim variable from `model_decision` was only
repairable, an officially unsupported claim passed, and a missing Spec 006
source did not get a product-claim source issue.

## Implemented Checks

- Product-claim variables such as `product_fact_summary`, price/plan/demo link
  variables, and recommendation range variables must use official product
  knowledge or Spec 006 as source.
- Product-claim evidence must resolve to a non-missing `TurnContext` product
  knowledge or Spec 006 ref.
- Product-claim values are checked against the structured official
  `unsupported_claims` list from product knowledge.
- Spec 006-grounded product claims pass when evidence matches the loaded
  contract ref.
- The validator returns `ValidatorResult` issues only.

## Validation

Focused:

```powershell
python -m pytest tests/test_spec011_validators_product_claims.py -q
```

Result: `4 passed`.

Nearby:

```powershell
python -m pytest tests/test_spec011_validators_product_claims.py tests/test_spec011_validators_policy_corroboration.py tests/test_spec011_validators_core.py tests/test_spec011_validators_diagnostic.py tests/test_spec011_validators_waitlist_demo_handoff.py tests/test_spec011_validators_leak_banned_phrases.py tests/test_spec011_validators_sales_inbox.py tests/test_spec011_product_knowledge_context.py tests/test_spec011_spec006_context.py tests/test_spec011_template_registry.py tests/test_spec011_schema_versioning.py tests/test_spec011_core_schemas.py -q
```

Result: `74 passed`.

Broad isolated Spec 011 core/conductor/validator/repair/fallback/policy/product suite:

```powershell
python -m pytest tests/test_spec011_validators_product_claims.py tests/test_spec011_validators_policy_corroboration.py tests/test_spec011_safe_fallback.py tests/test_spec011_repair_loop.py tests/test_spec011_validators_sales_inbox.py tests/test_spec011_validators_leak_banned_phrases.py tests/test_spec011_validators_waitlist_demo_handoff.py tests/test_spec011_validators_diagnostic.py tests/test_spec011_validators_core.py tests/test_spec011_conductor_demo_concept.py tests/test_spec011_conductor_language_policy.py tests/test_spec011_conductor_whole_response_fields.py tests/test_spec011_conductor_usage.py tests/test_spec011_conductor_self_checks.py tests/test_spec011_conductor_template_plan.py tests/test_spec011_conductor_evidence.py tests/test_spec011_conductor_policy_pack.py tests/test_spec011_conductor_boundary.py tests/test_spec011_context_snapshot.py tests/test_spec011_identity_contact_reliability.py tests/test_spec011_internal_metadata_non_renderable.py tests/test_spec011_spec006_context.py tests/test_spec011_product_knowledge_context.py tests/test_spec011_context_builder.py tests/test_spec011_turn_gate_delivery_regressions.py tests/test_spec011_turn_gate_outbox.py tests/test_spec011_turn_gate_sequence.py tests/test_spec011_turn_gate_human_pause.py tests/test_spec011_turn_gate_idempotency.py tests/test_spec011_turn_gate_lock.py tests/test_spec011_sales_inbox_projection_cases.py tests/test_spec011_schema_versioning.py tests/test_spec011_template_registry.py tests/test_spec011_core_schemas.py tests/test_spec011_contract_schema_map.py tests/test_product_knowledge.py -q
```

Result: `212 passed`.

Static:

```powershell
python -m ruff check app/core/taliya_commercial/validators.py tests/test_spec011_validators_product_claims.py tests/test_spec011_validators_policy_corroboration.py
git diff --check -- services/taliya-agent-runtime/app/core/taliya_commercial/validators.py services/taliya-agent-runtime/tests/test_spec011_validators_product_claims.py
```

Result: Ruff passed and diff whitespace check passed.

Targeted static review found no matches for inbound text parsing, regex
import/use, hardcoded official price literals, active render/delivery/persist
calls, runtime calls, or fallback-message construction in the product-claim
validator path.

## Anti-Drift Review

- Product claims are validated from structured variables and official context.
- The validator does not become a product-answer generator.
- Official product facts remain in product knowledge/Spec 006, not validators.
- Failed-path commercial-answer audit remains explicitly deferred to T011-069B.

Next task: `T011-069B - Validate failed paths do not produce deterministic commercial answers`.
