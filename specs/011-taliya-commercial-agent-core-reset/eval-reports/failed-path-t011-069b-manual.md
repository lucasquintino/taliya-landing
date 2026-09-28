# Failed Path T011-069B Manual Report

Status: passed for isolated Spec 011 core failed-path guard scope.

Task: `T011-069B - Validate that failed LLM/validator/repair/timeout paths do not produce deterministic commercial answers`.

## Scope

This task added a structural guard for failed-path payloads. It does not parse
inbound text, choose routes, answer commercial questions, render messages,
persist traces, deliver output, change `/pilates`, cut over adapters, or touch
`runtime/runner.py`.

The guard validates typed failure/result objects and dict payloads. It allows
safe fallback/handoff disposition data, visible validator failures, and visible
repair failures. It blocks customer-facing copy, rendered output, commercial
route/state advancement, normal commercial templates, product/diagnostic/waitlist
answer variables, repaired decisions, accepted validator conversions, and
`commercial_answer_allowed=true`.

## Red Baseline

Command:

```powershell
cd services/taliya-agent-runtime
python -m pytest tests/test_spec011_failed_path_guards.py -q
```

Observed before implementation:

```text
ModuleNotFoundError: No module named 'app.core.taliya_commercial.failed_path_guards'
```

After the first green pass, a second red guard was added for dict-form payloads:

```text
2 failed, 5 passed
```

Those failures showed that dict payloads with `status=passed` /
`final_disposition=accepted` and `commercial_answer_allowed=true` were not yet
blocked.

## Implemented Checks

- `SafeFallbackResult(status=safe_fallback|handoff_required)` passes only when it
  carries approved fallback/handoff template ids and no copy.
- `ValidatorResult(status=blocked|failed|repairable)` remains visible and can
  pass the guard.
- `RepairResult(status=failed|blocked)` remains visible and can pass the guard.
- `ConductorDecision` embedded in a failed path is blocked.
- Object and dict payloads that convert failure into accepted or repaired state
  are blocked.
- Rendered messages, outbox/delivery payloads, free-form customer copy fields,
  product/diagnostic/waitlist template ids, commercial route/state advancement,
  and demo/price/plan variables are blocked.
- Dict payloads with `commercial_answer_allowed=true` are blocked.

## Validation

Focused:

```powershell
python -m pytest tests/test_spec011_failed_path_guards.py -q
```

Result: `7 passed`.

Nearby:

```powershell
python -m pytest tests/test_spec011_failed_path_guards.py tests/test_spec011_safe_fallback.py tests/test_spec011_repair_loop.py tests/test_spec011_validators_product_claims.py tests/test_spec011_validators_policy_corroboration.py tests/test_spec011_validators_sales_inbox.py tests/test_spec011_validators_leak_banned_phrases.py tests/test_spec011_validators_waitlist_demo_handoff.py tests/test_spec011_validators_diagnostic.py tests/test_spec011_validators_core.py -q
```

Result: `74 passed`.

Broad isolated Spec 011 core/conductor/validator/repair/fallback/policy/product/failed-path suite:

```powershell
python -m pytest tests/test_spec011_failed_path_guards.py tests/test_spec011_validators_product_claims.py tests/test_spec011_validators_policy_corroboration.py tests/test_spec011_safe_fallback.py tests/test_spec011_repair_loop.py tests/test_spec011_validators_sales_inbox.py tests/test_spec011_validators_leak_banned_phrases.py tests/test_spec011_validators_waitlist_demo_handoff.py tests/test_spec011_validators_diagnostic.py tests/test_spec011_validators_core.py tests/test_spec011_conductor_demo_concept.py tests/test_spec011_conductor_language_policy.py tests/test_spec011_conductor_whole_response_fields.py tests/test_spec011_conductor_usage.py tests/test_spec011_conductor_self_checks.py tests/test_spec011_conductor_template_plan.py tests/test_spec011_conductor_evidence.py tests/test_spec011_conductor_policy_pack.py tests/test_spec011_conductor_boundary.py tests/test_spec011_context_snapshot.py tests/test_spec011_identity_contact_reliability.py tests/test_spec011_internal_metadata_non_renderable.py tests/test_spec011_spec006_context.py tests/test_spec011_product_knowledge_context.py tests/test_spec011_context_builder.py tests/test_spec011_turn_gate_delivery_regressions.py tests/test_spec011_turn_gate_outbox.py tests/test_spec011_turn_gate_sequence.py tests/test_spec011_turn_gate_human_pause.py tests/test_spec011_turn_gate_idempotency.py tests/test_spec011_turn_gate_lock.py tests/test_spec011_sales_inbox_projection_cases.py tests/test_spec011_schema_versioning.py tests/test_spec011_template_registry.py tests/test_spec011_core_schemas.py tests/test_spec011_contract_schema_map.py tests/test_product_knowledge.py -q
```

Result: `219 passed`.

Static:

```powershell
python -m ruff check app/core/taliya_commercial/failed_path_guards.py tests/test_spec011_failed_path_guards.py app/core/taliya_commercial/fallback.py app/core/taliya_commercial/repair.py
rg -n "inbound|AgentRunRequest|RuntimeState|request|import re|regex|\.search\(|\.match\(|isdigit|runner|runtime\.runner|Outbox|SalesInboxProjection|RenderedMessage|TraceRecord|persist|send\(" app/core/taliya_commercial/failed_path_guards.py
rg -n "497|120|R\$|checkout|desconto|vip|data de abertura" app/core/taliya_commercial/failed_path_guards.py
```

Result: Ruff passed. Both static `rg` commands returned no matches.

## Anti-Drift Review

- The guard does not become a commercial brain: it inspects structured payloads
  only and never interprets inbound text.
- Failure paths can preserve failure evidence, but cannot answer a commercial
  question deterministically.
- Safe fallback remains structured disposition only; rendering, delivery,
  persistence, adapters, and production cutover remain later phases.
- Phase 6 is closed for isolated-core proof only.

Next task: `T011-070 - Refactor renderer to accept only validated template plans`.
