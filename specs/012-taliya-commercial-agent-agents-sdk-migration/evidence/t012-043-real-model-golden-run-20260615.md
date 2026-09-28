# T012-043 real-model golden transcripts - paid run 2026-06-15

Status: executed, failed gate, not complete.

Paid approval:

- User approved the paid T012-043 test on 2026-06-15 with
  `aprovado o teste pago`.
- User then approved reusing the existing `OPENAI_API_KEY` from local
  `.env.local`.

Run command:

```powershell
python scripts\eval-agent-runtime-spec012-real-model-golden.py --max-total-cost-usd 1.00
```

Run summary:

- Model: `gpt-5.4-mini`
- Budget cap: `$1.00`
- Cost: `$0.092661`
- Model operations: `36`
- Scenarios executed: `9/9`
- Scenarios passed: `6/9`
- Scenarios failed: `3/9`
- Aborted: `false`

Passed scenarios:

- `final-price-first`
- `final-pain-first`
- `final-instagram-interest`
- `final-whatsapp-question`
- `final-human-request-silent-after`
- `final-demo-request`

Failed scenarios:

- `final-price-plus-pain`
  - The LLM selected the price answer path without satisfying the required
    contextual price hook.
  - Failure labels include `price_plus_context_requires_context_hook`.
  - Missing expected rendered evidence: `R$ 497`, `reposicao`,
    `diagnostico gratuito`, and template
    `diagnostic.price_hook_with_context`.
- `step3g-long-conversation`
  - The long diagnostic funnel failed during final diagnostic delivery.
  - Failure labels include missing official facts/variables:
    `indicated_agents`, `recommended_plan_or_range`, and
    `diagnostic.deliver_plan_recommendation:recommended_plan_or_range`.
  - Missing expected rendered evidence: `demonstra`.
- `final-waitlist-joined`
  - The run completed, but the rendered answer did not preserve the studio
    identity/location expected by the golden fixture.
  - Missing expected rendered evidence: `Studio Viva`, `Vitoria`.

Evidence written:

- Full JSON:
  `specs/012-taliya-commercial-agent-agents-sdk-migration/evidence/t012-043-real-model-golden-transcripts/20260615T150020Z/report.json`
- Full Markdown transcript report:
  `specs/012-taliya-commercial-agent-agents-sdk-migration/evidence/t012-043-real-model-golden-transcripts/20260615T150020Z/report.md`
- Per-scenario JSON files in the same directory.

Verification after run:

- `python -m pytest services/taliya-agent-runtime/tests -k spec012 -q`
  -> `242 passed, 716 deselected`.
- `python -m ruff check scripts\eval-agent-runtime-spec012-real-model-golden.py services\taliya-agent-runtime\app\core\taliya_commercial_sdk\action_turn_runner.py services\taliya-agent-runtime\tests\test_spec012_runtime_adapter.py services\taliya-agent-runtime\tests\test_spec012_sdk_contract_gate.py`
  -> passed.

Completion decision:

T012-043 remains open. The real-model golden transcripts were executed and
saved, but the release gate failed at `6/9`. Do not advance to T012-044 until
the three failures are corrected with no-cost tests first and the paid golden
run is repeated.
