# T012-039 Quality Judge Harness Closure

Status: completed on 2026-06-15 for harness/gate implementation.

## Scope

This no-cost closure implements the Layer 3 quality-judge harness required by
the binding Spec 010 eval contract. It applies thresholds to supplied judge
scores and prevents structural or mocked success from becoming release
approval.

Real judge/provider execution remains deferred to the paid real-model eval
phase.

## Files

- `services/taliya-agent-runtime/app/core/taliya_commercial_sdk/quality_judge.py`
- `services/taliya-agent-runtime/tests/test_spec012_quality_judge.py`
- `services/taliya-agent-runtime/tests/test_spec012_sdk_contract_gate.py`

## Proof

- Required dimensions are explicit.
- P1 mapped scenarios require average >= 4.2.
- Any dimension below 4.0 blocks the gate.
- Blocking failures override high judge scores.
- Missing dimensions or missing scores fail.
- Mocked proof mode can exercise the harness but returns
  `blocked_pending_real_judge`, never release approval.
- Real-model proof mode can pass only when all thresholds hold.
- Evidence package schema `012.quality_judge_evidence.v1` captures scenarios,
  judge scores/rationales, deterministic invariant results, product source
  versions, model usage, status, and final pass.

## Validation

Most recent full validation from `C:\Users\lucas\agentes-landing-system`:

```powershell
python -m pytest services/taliya-agent-runtime/tests -k spec012 -q
```

Result: 242 passed, 716 deselected.

Focused quality-judge anchors are required by
`test_spec012_sdk_contract_gate.py`.

## Anti-Determinism Review

The harness does not judge by local regex or text heuristics. It only gates
supplied judge scores/rationales and deterministic blocking failures. It does
not affect runtime commercial routing or customer copy.

## Paid-Call Status

No paid OpenAI call was made. Cost: `$0`.

## Next Paid Boundary

Real judge/provider scoring remains blocked until explicit paid approval.
