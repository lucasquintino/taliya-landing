# T012-038 Slice - Canonical Fixture Map

Date: 2026-06-11

## Scope

Started T012-038 with a no-cost canonical fixture map from Spec 011 into the
Spec 012 action-first migration.

Covered in this slice:

- all 9 Spec 011 golden transcript fixture IDs;
- all 8 Spec 011 do-not-do runtime fixture IDs;
- all 9 Spec 011 P0 real-OpenAI fixture IDs;
- all 3 Spec 011 do-not-do static fixture IDs;
- action-first owners and proof modes for each fixture.

This is a fixture-portability/inventory slice. It does not run paid model
traffic and does not claim the real-model golden gate is complete.

## Sources

- `specs/011-taliya-commercial-agent-core-reset/regression-cases.md`
- `scripts/fixtures/agent-runtime/spec-011-real-openai-p0.json`
- `scripts/fixtures/agent-runtime/spec-011-golden-transcripts.json`
- `scripts/fixtures/agent-runtime/spec-011-do-not-do-runtime.json`
- `specs/011-taliya-commercial-agent-core-reset/do-not-do-static-fixtures.json`
- `specs/011-taliya-commercial-agent-core-reset/eval-reports/agent-runtime-spec011-fixture-inventory.json`
- `specs/012-taliya-commercial-agent-agents-sdk-migration/tasks.md`
  - T012-038 requires canonical Spec 011 fixtures to replace the reconstructed
    spike scenarios as the paid-eval source of truth.

## Files Changed

- `specs/012-taliya-commercial-agent-agents-sdk-migration/canonical-fixture-map.json`
- `services/taliya-agent-runtime/tests/test_spec012_canonical_fixture_port.py`

## Behavior

The new `canonical-fixture-map.json` records, for each canonical fixture:

- the original fixture ID;
- the action-first owner modules/roles responsible for the behavior;
- whether proof is currently mocked/static or requires later real-model
  evidence.

The test suite loads the actual Spec 011 fixture files and fails if the Spec
012 map omits, renames, or invents fixture IDs.

## Tests

Run from `services/taliya-agent-runtime`:

- `python -m pytest tests\test_spec012_canonical_fixture_port.py -q`
  - result: 4 passed
- `python -m pytest tests\ -k spec012 -q`
  - result: 155 passed, 716 deselected
- `python -m ruff check app\core\taliya_commercial_sdk tests\test_spec012_canonical_fixture_port.py tests\test_spec012_turn_situation.py tests\test_spec012_action_agents.py tests\test_spec012_decision_compiler.py tests\test_spec012_action_turn_runner.py tests\test_spec012_action_validators_ported.py tests\test_spec012_static_audit.py tests\test_spec012_action_safety.py`
  - result: all checks passed

## Anti-Determinism Review

This slice adds no runtime commercial interpretation. The fixture map is
coverage metadata and test enforcement only. It explicitly marks runtime
golden/do-not-do/P0 fixtures as `real_model_required_later` so local mocked
coverage cannot be mistaken for paid real-model completion.

## Protected Scope

No `/pilates`, landing visual, Sales Inbox UI, checkout, multi-tenant, or
client/studio WhatsApp files were edited.

## Paid Calls

None.

## Still Open

- execute these canonical fixtures through the action-first mocked harness;
- add quality-judge/real-model gates only after explicit paid approval;
- connect fixture reports to Sales Inbox projection evidence after T012-035;
- keep `/pilates` baseline/no-drift for any future public widget cutover.
