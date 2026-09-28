# Release Readiness

Date: 2026-05-23

## Current Release Decision

Status: **production candidate exists and product-followup delta is implemented; production deployed; final approval still blocked by product-owner transcript approval and live WhatsApp smoke**.

The Taliya commercial agent implementation is the current production candidate for widget and WhatsApp. The local code path uses the new LLM-first runtime, not the old deterministic v2 conversational engine, and the latest local tests validate runtime behavior, persistence, Sales Inbox projection, waitlist, handoff, and protected `/pilates` integration.

Product-owner review later identified missing or partial behavior around "como funciona", post-diagnostic follow-up, comparison with current tools, WhatsApp/integration scope, security/data, out-of-profile leads, diagnostic refusal, and conversation resume. These gaps are captured in `product-followup-delta-contract.md`; implementation tasks T232-T259 now pass with local and real OpenAI evidence. Product-owner approval task T260 remains intentionally open until the transcript package is explicitly accepted.

Railway and Vercel production deployment were executed; live WhatsApp production smoke remains pending.

## Current Evidence

- Python runtime tests: passed, `167 passed`.
- Runtime Python tests: passed, `167 passed`.
- Next lint: passed, `npm run lint`.
- Next production build: passed, `npm run build`.
- Zero-cost gates: passed, `6/6`.
- Real OpenAI final correction matrix: passed, `8/8`, saved in `eval-reports/agent-runtime-real-openai-final-corrections-latest.json` and `.md`.
- Real OpenAI product-followup delta matrix: passed, `6/6`, saved in `eval-reports/agent-runtime-real-openai-product-followup-delta-latest.json` and `.md`.
- Widget visual smoke: passed on desktop and mobile, with demo CTA rendered as a widget action.
- Sales Inbox local smoke with real Postgres/OpenAI: passed on session `prod_widget_smoke_lead_20260523135540`, lead `lead_j5f1qa`.
- Production Postgres/Supabase migration: applied successfully, including corrected unique idempotency index.
- Single-lead-per-session regression: fixed and validated. Diagnostic, waitlist, and handoff now update the same Sales Inbox lead for the same session.
- Postgres SQL paths are implemented for runtime memory, diagnostic records, waitlist records, handoff status, and Sales Inbox projection.
- Official diagnostic script correction: local tests passed after replacing the rejected first diagnostic question with `Hoje seu studio tem mais ou menos quantos alunos ativos?`, tightening the diagnostic ledger so a name alone is not treated as an answer, and restoring the six approved diagnostic questions.

## 2026-05-29 Audit Update

- Python runtime tests: passed, `226 passed`.
- Local runtime eval matrix: passed across conversations, invariants, product knowledge, diagnostic, quality judge, waitlist, handoff, delivery, Sales Inbox, cost, naming, and report generation.
- Next production build: passed, `npm run build`.
- Next lint: failed outside the commercial runtime because `demo-kits/demo-02-interessados/render-frames.js` and `render-video.js` use CommonJS `require()`.
- Real OpenAI release gate before contextual-slot correction: failed, `10/12`, saved in `eval-reports/agent-runtime-real-openai-latest.md` and `.json`.
- Real OpenAI release gate after contextual-slot correction: passed, `12/12`, saved in `eval-reports/agent-runtime-real-openai-latest.md` and `.json`.
- Railway production runtime deploy after validation: succeeded, deployment `292699c1-4e81-458f-96fd-01c7d18be355`; `/healthz` returned `ok: true`, `environment: production`.
- WhatsApp site CTA hotfix after live report: passed focused regression, full Python runtime suite (`226 passed`), local runtime eval matrix, real OpenAI isolated scenario (`1/1`), real OpenAI full fixture with the new WhatsApp acceptance scenario (`13/13`), and `npm run build`; Railway runtime deployment `bae5af9c-a7da-4b01-a7fa-9c1364b8777d` is online and `/healthz` returned `ok: true`.

The two original real-provider failures were quality/context regressions, not safety failures: `real-plan-fit-with-context` did not reuse the lead's `80 alunos` and `reposicao` context in the visible reply, and `real-one-word-agenda` did not reuse `Agenda` in the visible reply. The contextual-slot correction preserves the approved template direction while passing those real-provider checks.

## Runtime Architecture Clarification

The current production candidate is an LLM-first conductor runtime with explicit specialist roles, not a full multi-call SDK handoff loop between separate specialist agents on every turn.

In normal turns, one model operation returns structured JSON with route, current specialist role, detected intents, facts, diagnostic/waitlist/handoff state, template IDs, and template variables. The runtime validates that output, renders approved templates, executes idempotent tool boundaries, persists state, and delivers channel-specific messages. Human handoff is a real operational pause/resume boundary. Specialist role changes are logical and traceable, but they are not currently separate SDK agent-to-agent handoff executions in the normal path.

This architecture is acceptable for the current scope if it remains LLM-first and eval-gated. It should be described as "LLM-first conductor with specialist roles" rather than "full multi-agent SDK handoff runtime" until the runtime is intentionally changed.

## Latest Sales Inbox Smoke Assertions

Latest local smoke result:

```text
singleLeadPerSession: true
diagnosticSaved: true
waitlistSaved: true
contactSaved: true
studioSaved: true
citySaved: true
conversationSaved: true
handoffPaused: true
```

Latest lead summary:

```text
leadId: lead_j5f1qa
sessionId: prod_widget_smoke_lead_20260523135540
status: human_active
conversionPath: human_whatsapp_assist
waitlistStatus: joined
diagnosticStatus: completed
contact: Lucas, 11999999999
studioName: Flow Pilates
cityState: Sao Paulo
recentMessages: 23
```

## Production Gate Blockers

- Product-owner approval for the Product Explanation And Follow-Up Delta transcript package is pending; implementation tasks T232-T259 are complete and T260 remains an external approval gate.
- Product-owner transcript approval is still pending after the official diagnostic script correction.
- Live WhatsApp/Meta/Dualhook smoke has not been run after the latest correction.
- Final production approval should not be recorded until the latest transcript package and live WhatsApp smoke are accepted.

## Required Cutover Sequence

1. Product owner reviews the new product-followup delta transcript package.
2. Record product-owner approval or requested changes in `product-owner-transcript-review.md`.
3. Deploy the exact reviewed code to Railway and Vercel only after explicit confirmation if production is not already on this commit.
4. Run live smoke tests: widget to Sales Inbox, WhatsApp inbound/outbound, idempotency, chunk order, waitlist, handoff, and operator pause.

## Remaining Risk

The biggest remaining risks are transcript approval and live WhatsApp verification. A wrong webhook secret, Meta/Dualhook callback mismatch, or stale production deploy could make WhatsApp fail even though the code and local runtime are passing.

## Decision

The agent can move to final production approval only after the product owner approves the product-followup delta transcripts, the exact reviewed commit is deployed, and live WhatsApp smoke passes.
