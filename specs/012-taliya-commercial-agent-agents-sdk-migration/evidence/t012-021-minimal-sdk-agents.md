# T012-021 Evidence - Minimal SDK Agents

## Scope Completed

Implemented minimal Taliya Agents SDK definitions from the Spec 012 behavior contracts:

- `services/taliya-agent-runtime/app/core/taliya_commercial_sdk/agents.py`
- `services/taliya-agent-runtime/app/core/taliya_commercial_sdk/__init__.py`
- `services/taliya-agent-runtime/tests/test_spec012_sdk_agents.py`

The module declares:

- `taliya_triage_agent`
- `taliya_entry_agent`
- `taliya_product_agent`
- `taliya_diagnostic_agent`
- `taliya_waitlist_agent`
- `taliya_handoff_agent`

## Proof Type

Mocked/no-cost isolated spike.

## Tests And Checks

From `services/taliya-agent-runtime`:

```text
python -m pytest tests\test_spec012_sdk_agents.py tests\test_spec012_sdk_spike_isolation.py -q
.......                                                                  [100%]
7 passed in 1.78s

python -m ruff check app\core\taliya_commercial_sdk tests\test_spec012_sdk_agents.py tests\test_spec012_sdk_spike_isolation.py
All checks passed!
```

## SDK Evidence

- `build_sdk_agent_specs()` returns the six-agent Spec 012 topology in design-lock order.
- `build_sdk_agents(model="gpt-test-no-call")` instantiates real `agents.Agent` objects and wires handoff object references.
- Agent tools are intentionally empty in T012-021; T012-022 owns read-only/proposal-only tools.
- Agent instructions explicitly require LLM-first commercial understanding, structured proposals, official product facts, approved rendering after validation, and no direct final delivery.
- Public runtime isolation remains covered by `test_spec012_sdk_spike_isolation.py` and `test_spec012_sdk_agents.py`.

## Anti-Determinism Review

No regex, token list, raw-text router, action compiler, or deterministic commercial shortcut was added. The handoff graph expresses specialist ownership only; commercial meaning remains for the SDK model run. The tests assert that the instructions preserve LLM-first boundaries and do not include regex-style shortcut language.

## Protected Scope Review

No `/pilates`, landing visual, Sales Inbox UI, multi-tenant, client/studio WhatsApp, or checkout files were modified by this task.

## Paid-Call Status

No paid OpenAI call was run. Agents were instantiated locally only; no `Runner.run` call was executed.

## Open Risks

T012-022 must add SDK tools without making them hidden routers or state mutators. T012-023 still owns the strict `TaliyaTurnProposal` adapter, so the current agent instructions cannot be treated as deliverable customer output.

## Next Task Lock

Next allowed task: T012-022 implement read-only/proposal-only tools.
