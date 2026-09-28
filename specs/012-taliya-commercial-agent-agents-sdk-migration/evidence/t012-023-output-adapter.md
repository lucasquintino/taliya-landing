# T012-023 Evidence - SDK Output Adapter To TaliyaTurnProposal

## Scope Completed

Implemented the strict SDK proposal contract and adapter:

- `services/taliya-agent-runtime/app/core/taliya_commercial_sdk/output_schema.py`
- `services/taliya-agent-runtime/app/core/taliya_commercial_sdk/output_adapter.py`
- `services/taliya-agent-runtime/app/core/taliya_commercial_sdk/__init__.py`
- `services/taliya-agent-runtime/tests/test_spec012_sdk_output_adapter.py`

## Proof Type

Mocked/no-cost isolated spike.

## Tests And Checks

From `services/taliya-agent-runtime`:

```text
python -m pytest tests\test_spec012_sdk_output_adapter.py tests\test_spec012_sdk_agents.py tests\test_spec012_sdk_spike_isolation.py -q
...................                                                      [100%]
19 passed in 1.85s

python -m ruff check app\core\taliya_commercial_sdk tests\test_spec012_sdk_output_adapter.py tests\test_spec012_sdk_agents.py tests\test_spec012_sdk_spike_isolation.py
All checks passed!
```

## Adapter Evidence

- `TaliyaTurnProposal` includes the required Spec 012 top-level groups.
- `adapt_sdk_output_to_turn_proposal()` accepts only structured SDK final output.
- Free-form SDK final text is rejected with `sdk_final_output_must_be_structured_proposal`.
- Direct delivery fields such as `final_text`, `message`, and `full_response` are rejected before validation.
- Product claims require official fact refs and evidence.
- Delivery remains `render_plan_only`; direct SDK delivery is blocked.
- Mocked SDK run items can populate basic agent path entries for start/tool/handoff/final.
- Public runtime isolation remains covered; `app.main` does not import `taliya_commercial_sdk`.

## Anti-Determinism Review

No regex, token list, raw-text route parser, action compiler, or deterministic commercial shortcut was added. The adapter validates structure and safety boundaries only. It does not decide commercial route, infer intent from lead text, render final copy, commit state, or choose waitlist/diagnostic behavior.

## Protected Scope Review

No `/pilates`, landing visual, Sales Inbox UI, multi-tenant, client/studio WhatsApp, or checkout files were modified by this task.

## Paid-Call Status

No paid OpenAI call was run. The adapter was exercised with mocked SDK result objects only; no `Runner.run` call was executed.

## Open Risks

T012-024 must connect the proposal to a focused validator/render path for spike output without allowing SDK free-form text to bypass templates. T012-025 still owns the broader mocked SDK contract test pass.

## Next Task Lock

Next allowed task: T012-024 reuse a focused validator/render path for spike output.
