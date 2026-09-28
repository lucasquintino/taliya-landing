# Real OpenAI Eval Report

**Current interpretation**: historical smoke/integration evidence only. This report does not approve final behavior readiness after the corrective behavior audit.

Date: 2026-05-22

Command:

```powershell
npm run eval:agent-runtime:real-openai
```

Runtime:

- Provider: `openai`
- Model: `gpt-5.4-mini`
- Mock: disabled/refused by runner
- Database writes: disabled by default for this eval; runtime state used in memory
- Transcript: `eval-reports/agent-runtime-real-openai-latest.md`
- JSON report: `eval-reports/agent-runtime-real-openai-latest.json`

## Result

- Smoke gate: pass
- Scenarios: 12
- Passed: 12
- Failed: 0
- Input tokens: 26,319
- Output tokens: 2,989
- Estimated cost: US$0.012557

## Covered Conversation Flows

- direct price and plan question
- mixed pain plus price question on WhatsApp
- plan-fit question with concrete studio context
- WhatsApp lead follow-up pain
- thin diagnostic request
- rich diagnostic context
- official demo link
- checkout request while checkout is unavailable
- waitlist join with studio/city/contact details
- waitlist acceptance with missing details
- human handoff and second-turn silence
- one-word ambiguous agenda message

## Fixes Made During Real Eval

- Added a real OpenAI eval runner that loads local secrets without printing them and refuses `mock`.
- Added complete transcript and JSON report output for real-provider conversations.
- Relaxed checkout guardrail to allow product-sourced statements that checkout is unavailable, while still blocking invented checkout/payment links.
- Strengthened runtime prompt rules so checkout/buying intent offers waitlist immediately.
- Strengthened runtime prompt rules so pending waitlist details ask for studio name and city/state.
- Added runtime normalization so a lead that accepts waitlist with actionable details is recorded as `joined` even when the LLM is overly cautious.

## Remaining Production Gaps

- This is a smoke-quality gate, not the final behavior corpus.
- It does not cover the required opening/source/name/diagnostic-first matrix from `behavior-contract.md`.
- Full confidence requires the real OpenAI behavior eval defined in `eval-plan.md`.
- Persistence against the configured Postgres database was not enabled in this eval.
- Production deployment to Railway/Vercel and real WhatsApp smoke tests are still gated by explicit confirmation.
