# T012-032C Slice - SDK-Path Safety Guardrails

Date: 2026-06-11

## Scope

Closed T012-032C with a deterministic, pre-SDK operational safety boundary
for the action-first runner.

Covered:

- prompt injection;
- unsupported media;
- sensitive data;
- medical/health advice outside scope.

This slice is mocked/no-cost and isolated. It does not add public endpoint
cutover.

## Sources

- `spec.md` FR-012-030: SDK input guardrails must cover prompt injection,
  sensitive data, unsupported media, and out-of-scope abuse.
- `decision-log.md` D-012-010: these guardrails were deferred from the spike
  and remain mandatory before shadow/cutover.
- `reference-map.md`: input guardrails include prompt injection, sensitive
  data, unsupported media, and out-of-scope abuse.
- `design-lock.md`: `taliya_safety_guardrails` run before/after SDK reasoning
  where appropriate.
- Approved template registry / renderer templates:
  - `safety.prompt_injection`;
  - `safety.unsupported_media`;
  - `safety.sensitive_data`;
  - `safety.no_medical_advice`.
- `taliya-llm-first-agent` allowed determinism: prompt injection, sensitive
  data, and unsupported media are operational/safety boundaries.

## Files Changed

- `services/taliya-agent-runtime/app/core/taliya_commercial_sdk/action_safety.py`
- `services/taliya-agent-runtime/app/core/taliya_commercial_sdk/action_turn_runner.py`
- `services/taliya-agent-runtime/tests/test_spec012_action_safety.py`

## Behavior

`classify_safety_boundary()` runs before the SDK in the isolated action runner.
When it returns a boundary:

- no SDK/LLM call is made;
- the approved safety template is rendered by the existing renderer;
- local state records `safety_blocked` and `safety_reason`;
- the transcript receives the user input and rendered safety reply.

The matcher now normalizes accents before checking the narrow safety phrase
sets, so inputs such as `instruções`, `cartão`, `médico` and `lesão` are
covered without adding commercial raw-text routing.

Runner-level tests now prove zero SDK/LLM behavior for all four outcomes:
`prompt_injection`, `unsupported_media`, `sensitive_data`, and
`medical_advice`.

## Tests

Run from `services/taliya-agent-runtime`:

- `python -m pytest tests\test_spec012_action_safety.py -q`
  - result: 11 passed
- `python -m pytest tests\ -k spec012 -q`
  - result: 193 passed, 716 deselected
- `python -m ruff check app\core\taliya_commercial_sdk\action_safety.py tests\test_spec012_action_safety.py`
  - result: all checks passed

## Anti-Determinism Review

The safety preguard is intentionally not a commercial classifier. It does not
decide price/demo/plan/pain/diagnostic/waitlist intent. It only blocks narrow
operational safety cases before reasoning, which is explicitly allowed by the
project skill and Spec 012.

## Protected Scope

No `/pilates`, landing visual, Sales Inbox UI, checkout, multi-tenant, or
client/studio WhatsApp files were edited.

## Paid Calls

None.

## Follow-Up Outside This Closure

- Broaden safety eval fixtures with any product-owner-approved phrases;
- integrate message-type metadata from public adapters only when endpoint
  cutover/shadow tasks are allowed;
- add safety cases to the canonical fixture/eval suite under T012-038/038B.
