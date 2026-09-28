# T012-039/T012-041 Quality Judge Evidence Package Anchor Slice

Status: started / partial on 2026-06-12.

## Scope

This no-cost slice strengthens the Layer 3 quality-judge gate by adding a local
evidence package shape and making the quality-judge harness mandatory in the
T012-041 contract gate.

It does not run a real judge model, does not call OpenAI, and does not treat
mocked scores as release approval.

## Files

- `services/taliya-agent-runtime/app/core/taliya_commercial_sdk/quality_judge.py`
- `services/taliya-agent-runtime/tests/test_spec012_quality_judge.py`
- `services/taliya-agent-runtime/tests/test_spec012_sdk_contract_gate.py`

## Added Behavior

`export_quality_judge_evidence_package(...)` now packages a supplied
`QualityJudgeReport` into local JSON-friendly evidence matching the Spec 010
eval-contract shape:

- `schema=012.quality_judge_evidence.v1`;
- `run_id`;
- `agent_key`;
- scenario ids/counts;
- transcripts;
- structured outputs, tool calls, handoffs, and guardrail placeholders;
- deterministic invariant results;
- product source versions;
- model usage/cost;
- judge score dimensions, averages, minimums, and rationales;
- skipped scenarios;
- final status and release eligibility.

The package keeps `final_pass=False` unless the underlying report has
`status=passed` and `release_eligible=True`. Mocked proof mode still returns
`blocked_pending_real_judge`.

## Contract Gate

The T012-041 contract manifest now requires `test_spec012_quality_judge.py`,
including:

- mocked scores cannot release;
- real-model proof mode can pass only when thresholds hold;
- average below 4.2 fails;
- any dimension below 4.0 fails;
- deterministic blocking failures override judge score;
- missing dimensions fail;
- the eval-contract evidence package is exported without release approval.

## Validation

Commands run from `C:\Users\lucas\agentes-landing-system`:

```powershell
python -m pytest services/taliya-agent-runtime/tests/test_spec012_quality_judge.py services/taliya-agent-runtime/tests/test_spec012_sdk_contract_gate.py -q
```

Result: 9 passed.

```powershell
python -m ruff check services/taliya-agent-runtime/app/core/taliya_commercial_sdk/quality_judge.py services/taliya-agent-runtime/tests/test_spec012_quality_judge.py services/taliya-agent-runtime/tests/test_spec012_sdk_contract_gate.py
```

Result: all checks passed.

```powershell
python -m pytest services/taliya-agent-runtime/tests -k spec012 -q
```

Result: 235 passed, 716 deselected.

## Anti-Determinism Review

No local text heuristic, regex judge, or customer-message classifier was added.
The module only applies contract thresholds to supplied judge scores and
packages evidence. The final real judge remains a later eval-only provider
step after explicit paid approval.

## Paid-Call Status

No paid OpenAI call was made. Cost: `$0`.

## Still Open

T012-039 remains open overall for real judge provider/report execution,
3x real-provider repetition, real-model golden transcripts, shadow/cutover
evidence, and product-owner/manual review approval.
