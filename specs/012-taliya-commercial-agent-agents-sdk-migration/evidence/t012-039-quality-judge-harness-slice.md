# T012-039 quality-judge harness slice

Date: 2026-06-11

## Scope

Added the no-cost harness for the Spec 010 Layer 3 quality-judge gate in the
action-first SDK path.

This does not claim final quality approval. The final release gate still
requires real-model judge scores and product-owner/manual review. This slice
only proves the gate infrastructure and threshold logic are present.

## Files

- `services/taliya-agent-runtime/app/core/taliya_commercial_sdk/quality_judge.py`
- `services/taliya-agent-runtime/tests/test_spec012_quality_judge.py`

## Behavior Proven

- The harness uses the Spec 010 quality dimensions:
  directness, naturalness, usefulness, commercial clarity, evidence use,
  diagnostic quality, waitlist timing, safety and honesty, brevity/channel fit,
  and no robotic phrasing.
- The gate requires mapped P1 average >= `4.2`.
- Any mapped P1 scenario dimension below `4.0` fails.
- Any deterministic blocking failure fails regardless of judge score.
- Missing or malformed dimension payloads fail.
- Mocked proof mode can validate harness behavior but cannot mark release
  eligible; it returns `blocked_pending_real_judge`.
- Real-model proof mode can pass only when all thresholds hold and no blocking
  failures remain.

## Anti-Determinism Review

No local regex/text heuristic was added as the quality judge. The module accepts
judge scores from a provider and applies contract gates. Mocked tests use fixed
scores only to validate gate mechanics; they cannot become release evidence.

## Commands

- `python -m pytest tests\test_spec012_quality_judge.py -q`
  - `6 passed`
- `python -m pytest tests\test_spec012_quality_judge.py tests\test_spec012_canonical_action_first_mocked.py tests\test_spec012_sales_inbox_projection.py -q`
  - `18 passed`
- `python -m pytest tests\ -k spec012 -q`
  - `189 passed, 716 deselected`
- `python -m ruff check app\core\taliya_commercial_sdk\quality_judge.py tests\test_spec012_quality_judge.py`
  - passed

## Protected Scope

No `/pilates` layout, landing visual, Sales Inbox UI, multi-tenant, client or
studio WhatsApp integration, checkout, public endpoint cutover, or paid OpenAI
call was touched.

## Paid Calls

None. The real quality judge remains blocked until explicit paid approval.

## Still Open

- Wire the real judge provider/report exporter after paid approval.
- Run mapped P1 behavior scenarios 3x with real provider evidence.
- Product-owner/manual review package remains required before release.
