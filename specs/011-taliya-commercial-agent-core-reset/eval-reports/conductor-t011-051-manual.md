# Conductor T011-051 Manual Validation

Task: `T011-051 - Encode logical specialist roles in policy pack`.

Date: 2026-05-30.

Proof level: isolated Spec 011 conductor-request proof with mocked provider. This does not yet prove real OpenAI behavior, extracted-fact evidence enforcement, model usage logging, validators, rendering, trace persistence, or public adapter cutover.

## Scope Checked

- No `/pilates` visual, layout, copy, or routing file was touched.
- No multi-tenant or client/studio WhatsApp path was touched.
- No runtime adapter, public API, production database migration, Sales Inbox UI, or `runtime/runner.py` code was touched.
- No deterministic commercial routing, regex, keyword classification, template-first response, diagnostic state machine, price logic, waitlist logic, demo logic, renderer, repair loop, or customer-facing fallback was added.
- The change is limited to a typed policy pack included in the one-call conductor provider request.

## Red Result Before Fix

Command from `services/taliya-agent-runtime`:

```powershell
python -m pytest tests/test_spec011_conductor_policy_pack.py -q
```

Observed result before implementation:

- `4 failed`.
- `ConductorProviderRequest` had no `specialist_policy` field.
- Mixed-intent contexts still called the provider, but there was no proof that the full role policy pack was present and stable.

This was the intended red failure for `T011-051`.

## Implementation Result

Added `services/taliya-agent-runtime/app/core/taliya_commercial/conductor_policy.py`:

- `SpecialistRolePolicy`
- `SpecialistPolicyPack`
- `get_specialist_policy_pack()`

Updated `services/taliya-agent-runtime/app/core/taliya_commercial/conductor.py`:

- `ConductorProviderRequest` now includes `specialist_policy`.
- `_build_provider_request(...)` injects the static policy pack into every provider call.
- Conductor instructions explicitly say the policy is guidance inside the single conductor call.

The policy pack has exactly six roles:

- `entry`
- `product`
- `diagnostic`
- `waitlist`
- `handoff`
- `safety`

The policy pack also declares:

- `normal_turn_call_strategy = "single_conductor_call"`
- `llm_selects_role_and_route = true`
- `code_must_not_preselect_role = true`

## Manual Scenario

Input contexts:

- `Quero preco, demo e saber se faz sentido para meu studio`
- `Quanto custa e tenho 120 alunos?`
- `Vim pelo Instagram, quero diagnostico e lista de espera`
- `Tenho 120 alunos, quero preco, diagnostico, demo e falar com humano`

Observed behavior:

- Each context still results in exactly one provider call.
- Every provider request includes all six role policies.
- The policy pack is identical across different inbound commercial texts.
- The provider, not code, returns the selected `role` and `route` in decision JSON.
- The policy text does not include hardcoded prices, plan-name copy, or customer-facing message snippets.
- The policy path has no text-branching, regex, keyword routing, or inbound normalization.

## Green Validation

Focused test:

```powershell
python -m pytest tests/test_spec011_conductor_policy_pack.py -q
```

Result: `4 passed`.

Nearest relevant isolated-core suite:

```powershell
python -m pytest tests/test_spec011_conductor_policy_pack.py tests/test_spec011_conductor_boundary.py tests/test_spec011_context_snapshot.py tests/test_spec011_identity_contact_reliability.py tests/test_spec011_internal_metadata_non_renderable.py tests/test_spec011_spec006_context.py tests/test_spec011_product_knowledge_context.py tests/test_spec011_context_builder.py tests/test_spec011_turn_gate_delivery_regressions.py tests/test_spec011_turn_gate_outbox.py tests/test_spec011_turn_gate_sequence.py tests/test_spec011_turn_gate_human_pause.py tests/test_spec011_turn_gate_idempotency.py tests/test_spec011_turn_gate_lock.py tests/test_spec011_sales_inbox_projection_cases.py tests/test_spec011_schema_versioning.py tests/test_spec011_template_registry.py tests/test_spec011_core_schemas.py tests/test_spec011_contract_schema_map.py tests/test_product_knowledge.py -q
```

Result: `93 passed`.

Ruff:

```powershell
python -m ruff check app/core/taliya_commercial tests/test_spec011_conductor_policy_pack.py tests/test_spec011_conductor_boundary.py tests/test_spec011_context_snapshot.py tests/test_spec011_identity_contact_reliability.py tests/test_spec011_internal_metadata_non_renderable.py tests/test_spec011_spec006_context.py tests/test_spec011_product_knowledge_context.py tests/test_spec011_context_builder.py tests/test_spec011_core_schemas.py
```

Result: `All checks passed!`

Static review:

```powershell
rg "if .*request\.message\.text|elif .*request\.message\.text|if .*inbound\.text|elif .*inbound\.text|if .*context\.inbound|elif .*context\.inbound|\bre\.|regex|normalized|keyword|if user says|when the message" app\core\taliya_commercial\conductor.py app\core\taliya_commercial\conductor_policy.py
```

Result: no text-branching, regex, keyword, or normalization routing patterns found in conductor policy path.

## Remaining Risk

This task proves only that the one-call conductor request includes a stable logical specialist policy pack. It does not yet:

- require evidence for extracted facts and numeric interpretations (`T011-052`);
- require full template plan variables (`T011-053`);
- require conductor self-checks (`T011-054`);
- log model usage (`T011-055`);
- run real OpenAI evals (`T011-103`, `T011-104`);
- validate or render the returned decision (`T011-060..T011-074`);
- persist production trace or Sales Inbox projection (`T011-080..T011-086`).
