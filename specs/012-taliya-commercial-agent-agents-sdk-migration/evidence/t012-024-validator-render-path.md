# T012-024 Evidence - Focused Validator/Render Path

## Scope Completed

Implemented a focused spike-only validator/render path for `TaliyaTurnProposal`:

- `services/taliya-agent-runtime/app/core/taliya_commercial_sdk/validators_adapter.py`
- `services/taliya-agent-runtime/app/core/taliya_commercial_sdk/__init__.py`
- `services/taliya-agent-runtime/tests/test_spec012_sdk_validators_adapter.py`

## Proof Type

Mocked/no-cost isolated spike.

## Tests And Checks

From `services/taliya-agent-runtime`:

```text
python -m pytest tests\test_spec012_sdk_validators_adapter.py tests\test_spec012_sdk_output_adapter.py tests\test_spec012_sdk_agents.py tests\test_spec012_sdk_spike_isolation.py -q
.........................                                                [100%]
25 passed in 1.96s

python -m ruff check app\core\taliya_commercial_sdk tests\test_spec012_sdk_validators_adapter.py tests\test_spec012_sdk_output_adapter.py tests\test_spec012_sdk_agents.py tests\test_spec012_sdk_spike_isolation.py
All checks passed!
```

## Validator/Render Evidence

- `validate_and_render_spike_output()` validates a structured `TaliyaTurnProposal`.
- Direct-question obligations must be marked answered before steering.
- Approved template ids are converted into existing Spec 011 `RenderPlan`/`RenderPlanItem` types.
- Template variables are validated through existing `TemplateVariableValue` and the approved template registry.
- Rendering uses existing `render_validated_template_plan()` with a `ValidatorResult(status="passed")`.
- Rendered output is `rendered_preview` only; `public_delivery=false` and `commits_state=false`.
- Unknown templates and missing required variables fail closed with no preview.

## Anti-Determinism Review

No regex, token list, raw-text route parser, action compiler, or deterministic commercial shortcut was added. The adapter validates proposal safety and renders approved templates only after the SDK/model-selected template proposal. It does not infer route, choose commercial meaning, commit waitlist/diagnostic/handoff state, or deliver final SDK free-form text.

## Protected Scope Review

No `/pilates`, landing visual, Sales Inbox UI, multi-tenant, client/studio WhatsApp, or checkout files were modified by this task.

## Paid-Call Status

No paid OpenAI call was run. The path was exercised with mocked `TaliyaTurnProposal` objects only; no `Runner.run` call was executed.

## Open Risks

T012-025 must run broader no-cost/mocked SDK contract tests across the isolated spike path. T012-024 does not yet prove real model behavior or paid spike readiness.

## Next Task Lock

Next allowed task: T012-025 run no-cost/mocked SDK contract tests.
