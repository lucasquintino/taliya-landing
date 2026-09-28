# T012-020 Evidence - Isolated SDK Prototype Path

## Scope Completed

Created an isolated Spec 012 SDK spike package without public cutover:

- `services/taliya-agent-runtime/app/core/taliya_commercial_sdk/__init__.py`
- `services/taliya-agent-runtime/app/core/taliya_commercial_sdk/isolation.py`
- `services/taliya-agent-runtime/app/core/taliya_commercial_sdk/spike_runner.py`
- `services/taliya-agent-runtime/tests/test_spec012_sdk_spike_isolation.py`

## Proof Type

Mocked/no-cost isolated spike.

## Tests And Checks

From `services/taliya-agent-runtime`:

```text
python -m pytest tests\test_spec012_sdk_spike_isolation.py -q
...                                                                      [100%]
3 passed in 1.35s

python -m ruff check app\core\taliya_commercial_sdk tests\test_spec012_sdk_spike_isolation.py
All checks passed!
```

## Isolation Evidence

- No `/v1/taliya-commercial/sdk-spike` route was added.
- `app.main` still imports `run_spec011_agent_turn` and does not import `taliya_commercial_sdk`.
- `run_isolated_sdk_spike()` requires an injected mocked runner for T012-020.
- If no mocked runner is injected, paid SDK execution raises `SdkSpikePaidCallBlocked`.
- `OPENAI_API_KEY` is not required for the mocked test.

## Anti-Determinism Review

No commercial routing, price handling, demo handling, diagnostic handling, waitlist handling, source-opening handling, or mixed-intent interpretation was implemented. The new code only creates an isolated execution boundary and paid-call guard for future SDK orchestration.

## Protected Scope Review

No `/pilates`, landing visual, Sales Inbox UI, multi-tenant, client/studio WhatsApp, or checkout files were modified by this task.

## Paid-Call Status

No paid OpenAI call was run. Paid calls remain blocked until mocked spike work is green and the user explicitly approves a paid spike budget.

## Open Risks

T012-021 must add real SDK agent definitions without turning instructions/tools into deterministic commercial shortcuts. T012-023 still owns the strict `TaliyaTurnProposal` adapter.

## Next Task Lock

Next allowed task: T012-021 implement minimal Taliya agents with instructions from behavior contracts.
