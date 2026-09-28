# T012-038B Post-Diagnostic Demo Resume Runner Slice

Date: 2026-06-11

## Scope

Added mocked/no-cost action-first runner coverage for a lead returning after a
completed diagnostic and asking for the demo again.

Scenario:

- conversation state is `diagnostic_delivered`;
- diagnostic ledger and final fields are already complete;
- demo was previously offered;
- lead says `me manda a demo de novo`;
- mocked LLM emits structured `send_demo` with
  `product_fact_keys_used=["demo_link"]`;
- runner renders only `product.demo_direct` and does not restart the
  diagnostic.

## Files Changed

- `services/taliya-agent-runtime/tests/test_spec012_action_turn_runner.py`
- `services/taliya-agent-runtime/tests/test_spec012_sdk_contract_gate.py`
- `specs/012-taliya-commercial-agent-agents-sdk-migration/evidence/t012-038b-post-diagnostic-demo-resume-runner-slice.md`
- `specs/012-taliya-commercial-agent-agents-sdk-migration/implementation-ledger.md`

## Evidence

New test:

- `test_post_diagnostic_demo_resume_after_days_does_not_restart_diagnostic`

Contract-gate anchor:

- `test_spec012_sdk_contract_gate.py` now requires the new runner test.

Verified behavior:

- turn is `post_diagnostic`;
- known-state turn starts directly at `taliya_product_agent`;
- turn uses one mocked model operation;
- selected action is `send_demo`;
- templates are only `product.demo_direct`;
- rendered text includes the official demo link;
- rendered text does not reoffer diagnostic or ask active-students questions;
- diagnostic state remains completed;
- demo state remains offered;
- direct question is recorded as answered;
- total cost is `$0`.

## Tests

Run from repository root:

- `python -m pytest services/taliya-agent-runtime/tests/test_spec012_action_turn_runner.py -q`
  - result: 17 passed
- `python -m pytest services/taliya-agent-runtime/tests/test_spec012_sdk_contract_gate.py services/taliya-agent-runtime/tests/test_spec012_action_turn_runner.py -q`
  - result: 19 passed
- `python -m ruff check services/taliya-agent-runtime/tests/test_spec012_sdk_contract_gate.py services/taliya-agent-runtime/tests/test_spec012_action_turn_runner.py`
  - result: all checks passed
- `python -m pytest services/taliya-agent-runtime/tests -k spec012 -q`
  - result: 230 passed, 716 deselected

## Anti-Determinism Review

No raw lead-text demo/resume parser was added. The mocked LLM declares the
structured action and official fact key; code resolves the official demo link,
validates, renders the approved template, traces, and commits after validation.

## Protected Scope

No `/pilates`, landing visual, Sales Inbox UI, checkout implementation,
multi-tenant, public endpoint, or client/studio WhatsApp files were edited.

## Paid Calls

None. Cost: `$0`.

## Still Open

T012-038B remains open for the broader fixture matrix and real-model evidence
after explicit approval. T012-041 remains open for final contract verification
after endpoint/runtime integration and real-model/shadow gates.
