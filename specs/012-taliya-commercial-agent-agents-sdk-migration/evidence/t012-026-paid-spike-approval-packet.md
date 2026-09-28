# T012-026 Evidence - Paid Spike Approval Packet

## Scope Confirmation

Closed T012-026 only: prepared the paid spike approval packet for T012-027.

No paid OpenAI call was run. No real-model spike scenario was executed. No public
endpoint cutover, no Spec 011 implementation, no `/pilates` visual/layout
change, no Sales Inbox UI change, no multi-tenant work, no client/studio
WhatsApp work, and no checkout work.

## Files Changed

- `specs/012-taliya-commercial-agent-agents-sdk-migration/paid-spike-approval-packet.md`
- `specs/012-taliya-commercial-agent-agents-sdk-migration/tasks.md`
- `specs/012-taliya-commercial-agent-agents-sdk-migration/implementation-ledger.md`
- `specs/012-taliya-commercial-agent-agents-sdk-migration/decision-log.md`
- `specs/012-taliya-commercial-agent-agents-sdk-migration/evidence/t012-026-paid-spike-approval-packet.md`

## Approval Packet Contents

The packet defines:

- frozen T012-027 scenario list;
- required report fields per scenario;
- model and cost estimate;
- requested approval ceiling;
- exact approval wording;
- preconditions before the first paid call;
- abort conditions;
- pass bar;
- explicit statement that the packet is not approval.

## Pricing Source

Pricing was checked on 2026-06-05 from OpenAI API pricing.

The packet uses `gpt-5.4-mini` as the preferred first paid spike model and
records:

- input: `$0.75 / 1M tokens`;
- cached input: `$0.075 / 1M tokens`;
- output: `$4.50 / 1M tokens`.

The packet requests approval for a `$1.00` estimated-cost ceiling, with a stop
condition if the model, pricing, or usage/cost reporting is unavailable or
materially different at T012-027 execution time.

## Tests And Static Checks

From `services/taliya-agent-runtime`:

```text
python -m pytest tests\test_spec012_sdk_mocked_contracts.py tests\test_spec012_sdk_validators_adapter.py tests\test_spec012_sdk_output_adapter.py tests\test_spec012_sdk_agents.py tests\test_spec012_sdk_spike_isolation.py -q
46 passed
```

```text
python -m ruff check app\core\taliya_commercial_sdk tests\test_spec012_sdk_mocked_contracts.py tests\test_spec012_sdk_validators_adapter.py tests\test_spec012_sdk_output_adapter.py tests\test_spec012_sdk_agents.py tests\test_spec012_sdk_spike_isolation.py
All checks passed!
```

## Proof Type

Design/approval-gate proof.

## Anti-Determinism Review

Passed for T012-026.

This task added approval documentation only. It did not add regex/token
commercial routing, deterministic commercial shortcuts, template-first
conversation decisions, or a runner that bypasses the LLM-first architecture.
The approval packet requires the paid spike to preserve structured SDK output,
validator/render boundaries, official product grounding, and no direct SDK text
delivery.

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

Current cost for T012-026: `$0.00`.

## Open Risks

- T012-027 still needs explicit user approval before any paid OpenAI call.
- The proposed cost is an estimate and must be checked again immediately before
  T012-027 execution.
- Real-model quality, trace usefulness, and SDK-vs-Spec-011 comparison remain
  unproven until T012-027 and T012-028.

## Next Task Lock

Current allowed next work: T012-027 only after explicit user approval for paid
OpenAI calls and budget.

Without explicit approval, stop before paid calls.
