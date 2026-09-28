# T012-025 Evidence - No-Cost Mocked SDK Contract Tests

## Scope Confirmation

Closed T012-025 only: no-cost/mocked SDK contract tests for the isolated Spec 012
Agents SDK spike.

No public endpoint cutover, no paid OpenAI call, no Spec 011 implementation, no
`/pilates` visual/layout change, no Sales Inbox UI change, no multi-tenant work,
no client/studio WhatsApp work, and no checkout work.

## Files Changed

- `services/taliya-agent-runtime/tests/test_spec012_sdk_mocked_contracts.py`
- `specs/012-taliya-commercial-agent-agents-sdk-migration/tasks.md`
- `specs/012-taliya-commercial-agent-agents-sdk-migration/implementation-ledger.md`

## Contract Coverage

The mocked contract suite covers all required spike scenarios from `spike-plan.md`:

1. Cold greeting: `oi`
2. Pain-first WhatsApp response-late context
3. Price-first direct question
4. Price plus pain mixed intent
5. Diagnostic start
6. Simple numeric diagnostic answer: `120`
7. Diagnostic urgency final with staged diagnostic render plan
8. WhatsApp product scope question
9. Demo request
10. Waitlist curiosity without contract intent
11. Clear waitlist/contract intent
12. Human handoff request
13. Do-not-do: `plano de 497` remains `plan_price`, not student count
14. Do-not-do: checkout/discount/date/VIP remains unsupported/unpromised
15. Delivery concurrency simulation remains render-plan-only and defer-proposed

Each scenario travels through:

- injected mocked SDK runner;
- `run_isolated_sdk_spike`;
- `adapt_sdk_output_to_turn_proposal`;
- `validate_and_render_spike_output`;
- approved template renderer preview.

## Tests And Static Checks

From `services/taliya-agent-runtime`:

```text
python -m pytest tests\test_spec012_sdk_mocked_contracts.py -q
21 passed
```

```text
python -m pytest tests\test_spec012_sdk_mocked_contracts.py tests\test_spec012_sdk_validators_adapter.py tests\test_spec012_sdk_output_adapter.py tests\test_spec012_sdk_agents.py tests\test_spec012_sdk_spike_isolation.py -q
46 passed
```

```text
python -m ruff check app\core\taliya_commercial_sdk tests\test_spec012_sdk_mocked_contracts.py tests\test_spec012_sdk_validators_adapter.py tests\test_spec012_sdk_output_adapter.py tests\test_spec012_sdk_agents.py tests\test_spec012_sdk_spike_isolation.py
All checks passed!
```

## Proof Type

Mocked isolated spike proof.

## Anti-Determinism Review

Passed for T012-025.

The new tests do not add commercial raw-text routing, regex/token shortcuts, or
template-first decision code. They use structured mocked SDK outputs as fixtures
to verify that the SDK spike boundary accepts only `TaliyaTurnProposal`, blocks
direct free-form delivery, validates official product refs, renders only
approved templates, and keeps state changes proposal-only.

The test suite includes an explicit no-real-runner guard against `Runner.run`,
paid override usage, and direct model construction inside the mocked contracts.

## Protected Scope Diff Result

Protected scope unchanged:

- no `/pilates` files touched;
- no landing visual files touched;
- no Sales Inbox UI touched;
- no multi-tenant code touched;
- no client/studio WhatsApp code touched;
- no checkout code touched.

## Paid-Call Status

No paid OpenAI call was run.

Mocked scenario usage reports:

- `model`: `mocked-sdk-no-cost`
- `model_operations`: `0`
- `cost_usd`: `0`

## Open Risks

- This proves structural contracts only. It does not prove real model quality,
  transcript quality, SDK trace usefulness, or cost.
- Paid spike remains blocked until T012-026 approval packet is prepared and the
  user explicitly approves a budget/run.
- Delivery concurrency is only represented as a proposal; runtime delivery gate
  proof remains locked to later integration tasks.

## Next Task Lock

Current allowed next work: T012-026 prepare paid spike approval packet.

Do not run paid SDK scenarios until explicit user approval.
