# T012-038/T012-038B Canonical Fixture Closure

Status: completed on 2026-06-15 for mocked/no-cost fixture coverage.

## Scope

This closure ports the binding Spec 011 canonical fixture sources into the Spec
012 action-first migration and extends mocked coverage for previously uncovered
conversation cells. Real-model validation remains explicitly deferred to
T012-043.

No paid provider call, public cutover, shadow traffic, `/pilates`
visual/copy/layout, Sales Inbox UI, checkout, multi-tenant, or client/studio
WhatsApp change was made.

## Sources

- `specs/011-taliya-commercial-agent-core-reset/regression-cases.md`
- `scripts/fixtures/agent-runtime/spec-011-golden-transcripts.json`
- `scripts/fixtures/agent-runtime/spec-011-do-not-do-runtime.json`
- `scripts/fixtures/agent-runtime/spec-011-real-openai-p0.json`
- `specs/011-taliya-commercial-agent-core-reset/do-not-do-static-fixtures.json`
- `specs/012-taliya-commercial-agent-agents-sdk-migration/canonical-fixture-map.json`

## T012-038 Proof

- Canonical fixture map matches all Spec 011 golden, do-not-do runtime, P0, and
  static fixture ids.
- Regression ids referenced by fixtures exist in Spec 011 regression cases.
- Every fixture has action-first ownership metadata and proof-mode metadata.
- Runtime fixtures are marked both `mocked` and `real_model_required_later`, so
  paid validation remains explicit and cannot be mistaken for already done.
- Mocked action-first execution covers the golden fixtures including price,
  price+pain, pain-first, Instagram/source opening, WhatsApp scope, demo,
  waitlist, human handoff, and long conversation.
- Mocked do-not-do/P0 execution covers early phone capture, checkout/payment,
  date/VIP/discount, integration scope, security/data, studio WhatsApp
  connection capture, wrong student language, price 497 not student count,
  metadata leak, urgency-before-final, short diagnostic answer, final
  diagnostic length/plain language, Sales Inbox consistency, and false-pass
  protection.

## T012-038B Proof

- Messy input cells: `qto fica?`, `tem como ver ai mn`, and post-diagnostic
  `qto ficava msm?`.
- Diagnostic correction: "na verdade sao 80, nao 120".
- Multiple diagnostic answers in one message.
- Product-question interruption matrix during diagnostic: how it works,
  integration/specific system, security/data, availability/checkout,
  out-of-profile/student, and comparison/current tool.
- Objection mid-diagnostic, including price objection.
- Resume after days with completed diagnostic memory.
- Waitlist pending product question then missing-detail continuation.
- Post-diagnostic demo resume without restarting diagnostic.
- Post-waitlist product resume preserving joined status and avoiding waitlist
  reoffer.

## Validation

Most recent full validation from `C:\Users\lucas\agentes-landing-system`:

```powershell
python -m pytest services/taliya-agent-runtime/tests -k spec012 -q
```

Result: 242 passed, 716 deselected.

Relevant anchored suites include:

- `test_spec012_canonical_fixture_port.py`
- `test_spec012_canonical_action_first_mocked.py`
- `test_spec012_canonical_do_not_do_mocked.py`
- `test_spec012_canonical_p0_mocked.py`
- `test_spec012_decision_compiler.py`
- `test_spec012_action_turn_runner.py`
- `test_spec012_sdk_contract_gate.py`

## Anti-Determinism Review

Messy phrases and canonical user texts appear only as fixtures. They are not
used as runtime regex/token routing. Mocked LLM outputs provide structured
`ConductorActionDecision`; deterministic code only expands, validates, renders,
traces, and commits accepted actions.

## Paid-Call Status

No paid OpenAI call was made. Cost: `$0`.

## Next Paid Boundary

T012-043 real-model golden transcripts remain blocked until explicit paid
approval.
