# T012-043 real-model golden transcripts - blocked before paid call

Status: blocked, not complete.

The user explicitly approved the paid T012-043 test on 2026-06-15 with:
`aprovado o teste pago`.

What was prepared:

- Added `scripts/eval-agent-runtime-spec012-real-model-golden.py`.
- The runner loads the 9 canonical Spec 011 golden transcripts from
  `scripts/fixtures/agent-runtime/spec-011-golden-transcripts.json`.
- The runner uses the isolated action-first SDK conversation loop through
  `run_action_conversation(..., paid_openai_approved=True)`.
- The runner enforces a conservative `$1.00` local cap for this approved run.
- The runner writes per-scenario JSON, aggregate JSON, and aggregate Markdown.
- The Markdown report includes the full message exchanges for every executed
  scenario.

No-cost validation:

- `python -m ruff check scripts\eval-agent-runtime-spec012-real-model-golden.py`
  -> passed.
- `python scripts\eval-agent-runtime-spec012-real-model-golden.py --preflight-only --max-total-cost-usd 1.00`
  -> passed.

Paid attempt result:

- Command: `python scripts\eval-agent-runtime-spec012-real-model-golden.py --max-total-cost-usd 1.00`
- Result: blocked before OpenAI call.
- Reason: `OPENAI_API_KEY is not available in the environment or runtime .env.`
- Cost: `$0.000000`.
- Model operations: `0`.
- Real transcripts produced: `0`.

Evidence written:

- `specs/012-taliya-commercial-agent-agents-sdk-migration/evidence/t012-043-real-model-golden-transcripts/preflight-20260615T145129Z/preflight.json`
- `specs/012-taliya-commercial-agent-agents-sdk-migration/evidence/t012-043-real-model-golden-transcripts/preflight-20260615T145129Z/preflight.md`
- `specs/012-taliya-commercial-agent-agents-sdk-migration/evidence/t012-043-real-model-golden-transcripts/20260615T145211Z/report.json`
- `specs/012-taliya-commercial-agent-agents-sdk-migration/evidence/t012-043-real-model-golden-transcripts/20260615T145211Z/report.md`

Completion decision:

T012-043 remains open. The paid test was approved and attempted, but the
required provider credential was absent, so the real-model golden transcripts
were not generated.

Next exact step:

Provide `OPENAI_API_KEY` to the runtime environment without committing it, then
run:

```powershell
python scripts\eval-agent-runtime-spec012-real-model-golden.py --max-total-cost-usd 1.00
```
