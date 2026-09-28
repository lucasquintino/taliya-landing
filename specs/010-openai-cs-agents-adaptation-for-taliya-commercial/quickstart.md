# Quickstart: OpenAI CS Agents Adaptation For Taliya Commercial

## 1. Read Required Context

Before implementation, read:

- `AGENTS.md`
- `specs/010-openai-cs-agents-adaptation-for-taliya-commercial/spec.md`
- `specs/010-openai-cs-agents-adaptation-for-taliya-commercial/plan.md`
- `specs/010-openai-cs-agents-adaptation-for-taliya-commercial/tasks.md`
- `specs/010-openai-cs-agents-adaptation-for-taliya-commercial/behavior-contract.md`
- `specs/010-openai-cs-agents-adaptation-for-taliya-commercial/conversation-state-contract.md`
- `specs/010-openai-cs-agents-adaptation-for-taliya-commercial/message-template-contract.md`
- `specs/010-openai-cs-agents-adaptation-for-taliya-commercial/diagnostic-contract.md`
- `specs/010-openai-cs-agents-adaptation-for-taliya-commercial/sales-inbox-contract.md`
- `specs/010-openai-cs-agents-adaptation-for-taliya-commercial/eval-plan.md`
- `specs/010-openai-cs-agents-adaptation-for-taliya-commercial/reference-map.md`
- `specs/010-openai-cs-agents-adaptation-for-taliya-commercial/current-runtime-gap-analysis.md`
- `specs/009-taliya-sales-agent-architecture/spec.md`
- `specs/009-taliya-sales-agent-architecture/plan.md`
- `specs/009-taliya-sales-agent-architecture/tasks.md`
- `specs/002-floating-ai-sales-agent/spec.md`
- `specs/002-floating-ai-sales-agent/tasks.md`
- `specs/001-niche-landing-system/spec.md`
- docs under `docs/landing-agentes-pilates/source/`
- relevant Next.js docs in `node_modules/next/dist/docs/` before editing Next route/runtime code

## 2. Protected Landing Rule

Do not redesign, reorder, restyle, or visually alter `/pilates`.

Allowed only when preserving the approved layout:

- CTA wiring
- metadata/config alignment
- tracking/schema alignment
- route gates
- accessibility fixes
- responsive bug fixes
- agent integration fixes

Capture or confirm desktop and mobile `/pilates` baseline before implementation changes that can affect landing behavior.

## 3. Reference Check

Before writing runtime code, inspect the OpenAI reference:

```text
https://github.com/openai/openai-cs-agents-demo
```

Confirm these mappings:

- reference `agents.py` -> Taliya `agents.py`
- reference `tools.py` -> Taliya tools
- reference `guardrails.py` -> Taliya guardrails
- reference `context.py` -> Taliya context
- reference `server.py` -> Taliya FastAPI runtime server
- reference `memory_store.py` -> Taliya Postgres memory store

## 4. Implementation Order

The final implementation must follow tasks T206-T226 in `tasks.md` before deploy work.

1. Treat the five binding contracts as source of truth.
2. Add zero-cost tests for states, templates, renderer, diagnostic ledger, waitlist intent, names, idempotency, ordering, delivery, and Sales Inbox.
3. Implement canonical state helpers.
4. Implement approved template registry.
5. Implement channel-aware renderer.
6. Expand structured output with previous/current/next state, `template_ids`, variables, render plan, and diagnostic ledger.
7. Update prompts so the LLM acts as interpreter/director and chooses templates.
8. Implement diagnostic ledger and no-repeat behavior.
9. Enforce waitlist only after clear intent to contract.
10. Enforce real-person-name-only policy.
11. Enforce JSON repair once and safe fallback without state advancement.
12. Update widget and WhatsApp delivery mapping for short messages, typing/delay, widget buttons, and WhatsApp text/links.
13. Update Sales Inbox projection completeness.
14. Run zero-cost gates.
15. Run quota-limited real OpenAI smoke only after zero-cost gates pass.
16. Run full mapped behavior matrix only after smoke passes and cost limits are configured.
17. Record product-owner transcript approval before production cutover.

## 5. Local Commands

Commands will be finalized during implementation. Expected groups:

```bash
# Existing app checks
npm run lint
npm run eval:whatsapp-webhook
npm run eval:message-delivery-matrix

# New runtime checks
cd services/taliya-agent-runtime
pytest

# New eval checks
npm run eval:agent-runtime
npm run eval:agent-runtime:quality
npm run eval:agent-runtime:delivery
npm run eval:agent-runtime:zero-cost-gates
```

## 6. Production Gate

Production replacement requires:

- runtime tests pass
- HMAC contract tests pass
- product knowledge tests pass
- structured output tests pass
- guardrail tests pass
- channel adapter tests pass
- template/renderer/state/diagnostic-ledger tests pass
- Sales Inbox completeness tests pass
- zero-cost gates pass before broad real OpenAI runs
- deterministic invariants pass
- LLM judge scores pass
- quota-limited real OpenAI smoke passes
- full mapped behavior matrix passes
- widget manual tests pass
- real WhatsApp smoke tests pass after deploy
- product owner approves transcripts

No legacy deterministic conversation fallback is allowed.

## 7. Production Confirmation Rule

Autonomous implementation is allowed for local files, tests, fixtures, local migrations, and non-production verification. Before any real production database migration, Railway deploy, Vercel deploy, live WhatsApp configuration change, or live WhatsApp message test, stop and request explicit user confirmation.
