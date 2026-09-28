# T012-032 Evidence - Validator Port Slice: Waitlist, Demo, Handoff

## Scope Confirmation

This closes a no-cost implementation slice inside T012-032 only. T012-032
remains open until the full Spec 011 validator set plus the 010 voice rules are
ported and evidenced.

No paid OpenAI call was run. No public endpoint cutover, no `/pilates`
visual/layout change, no Sales Inbox UI change, no multi-tenant work, no
client/studio WhatsApp work, and no checkout work.

## Files Changed

- `services/taliya-agent-runtime/app/core/taliya_commercial_sdk/action_validators.py`
- `services/taliya-agent-runtime/tests/test_spec012_action_validators_ported.py`
- `specs/012-taliya-commercial-agent-agents-sdk-migration/evidence/t012-032-validator-port-waitlist-demo-handoff-slice.md`
- `specs/012-taliya-commercial-agent-agents-sdk-migration/implementation-ledger.md`

## Coverage Added

Added action-first validator coverage for these Spec 011 behaviors:

- waitlist offer cannot be treated as eligible when the LLM's structured
  `waitlist_intent` is only `curiosity`, including demo-curiosity context;
- waitlist offer is accepted when the LLM declares clear contract intent;
- demo offer path requires the official demo template;
- human handoff request requires a reason/composition and produces pause
  proposal state;
- handoff with reason and acknowledge template remains valid.

## Implementation Note

The bridge from action-first `CompiledTurn` to the legacy Spec 011 validator no
longer marks `offer_waitlist` as eligible by action alone. Eligibility now
depends on the LLM's structured waitlist intent (`contract_intent`, `accepts`,
or `provides_detail`) or on the explicit `join_waitlist` action.

This preserves the action-first boundary: the LLM still owns the commercial
meaning; deterministic validation only enforces timing and eligibility.

## Tests And Static Checks

From `services/taliya-agent-runtime`:

```text
python -m pytest tests\test_spec012_action_validators_ported.py -q
5 passed
```

```text
python -m pytest tests\test_spec012_action_turn_runner.py::test_full_funnel_segment_with_state_evolution tests\test_spec012_action_validators_ported.py -q
6 passed
```

```text
python -m pytest tests\ -k spec012 -q
112 passed, 716 deselected
```

```text
python -m ruff check app\core\taliya_commercial_sdk tests\test_spec012_action_validators_ported.py
All checks passed!
```

## Proof Type

Mocked/no-cost implementation proof.

## Anti-Determinism Review

Passed for this slice.

No raw-text commercial routing, regex routing, or template-first decision logic
was added. The only deterministic change is a validator bridge correction:
action alone no longer proves waitlist eligibility when the model's structured
intent says curiosity.

## Protected Scope Diff Result

Protected scope unchanged:

- no `/pilates` files touched;
- no landing visual files touched;
- no Sales Inbox UI touched;
- no multi-tenant code touched;
- no client/studio WhatsApp code touched;
- no checkout code touched.

## Paid-Call Status

No paid OpenAI call was run. Cost: `$0.00`.

## Open T012-032 Work

Remaining T012-032 scope still includes full evidence for:

- timing/shape validator coverage beyond the slice above;
- internal/source label leak coverage;
- full banned-phrase and owner-language rules;
- no-CRM-for-lay-lead coverage;
- rejected final formats;
- thin-context "pelo que voce contou" block;
- full answer-adequacy map coverage.

## Next Task Lock

Current allowed next work: continue T012-032 validator port with another
no-cost mocked/tested slice.
