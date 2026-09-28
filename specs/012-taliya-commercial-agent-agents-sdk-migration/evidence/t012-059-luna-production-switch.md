# T012-059 Luna production switch

## Decision

T012-059 passed. Production is running `gpt-5.6-luna` on the Spec 012
action-first Agents SDK runtime.

## Recovery from attempt 1

The first switch attempt is recorded in
`t012-059-luna-switch-attempt-1.md`. Its smoke failed before model execution
because Supabase project `pxvabrsngfhebytdqxth` was `INACTIVE`. The existing
project was restored, reached `ACTIVE_HEALTHY`, accepted a direct SQL query,
and accepted a connection using the exact Railway `DATABASE_URL`. No schema or
table was recreated.

## Active deployments

- Railway service: `taliya-agent-runtime`.
- Railway deployment: `48ae1d84-63db-4633-8288-b8af40246e0f`.
- Railway image digest:
  `sha256:41ffef5ecf2c7c788acfe385ee86bea0d5fc4f6ec537c6a8e88ff3e7a759fb58`.
- Railway health: `ok=true`, model `gpt-5.6-luna`, reasoning `none`, OpenAI
  `2.44.0`, Agents SDK `0.18.0`, build SHA
  `5c15aed6a68a2907789e34843d7c4efd152cf927`.
- Vercel project: `lucasquintinos-projects/taliya-landing`.
- Vercel production deployment: `dpl_E7EPTbJoKiXuf5ekNq27W33PEcSB`.
- Vercel source: GitHub `master`, commit
  `5c15aed6a68a2907789e34843d7c4efd152cf927`.
- Public alias: `https://www.taliya.com.br`.

## Paid production smoke

- Session: `t012059_luna_prod_smoke_2_1785894540`.
- Runtime run: `run_fce0735f630f4f04aa8ee661569d44cc`.
- Trace: `trace_8968eb1eddce4080b5dc8a69650393e1`.
- Result: `succeeded`.
- Model operations: `2`.
- Repairs: `0`.
- Input tokens: `4,531`.
- Output tokens: `260`.
- Reported cost: `$0.006091`.

Complete exchange:

```text
lead: como funciona no WhatsApp?

assistant: Oi, tudo bem?

assistant: O aluno não precisa baixar aplicativo nem criar senha. Ele conversa
no WhatsApp; a Taliya registra a ação, atualiza o painel e avisa o responsável.

assistant: Se quiser ver isso funcionando na prática, aqui está uma
demonstração: https://www.taliya.com.br/pilates/planos/demonstracao
```

The answer used only `product.whatsapp_direct`, passed validators, used the
official demonstration link, leaked no internal language, and made no
unsupported product promise.

## Defects found and corrected without another paid turn

1. A direct WhatsApp answer was projected as `diagnostic_offered` even though
   the rendered copy did not offer a diagnostic. The compiler now derives that
   transition from the templates/enum that actually render an offer. The
   WhatsApp-only answer remains in `product_question`, so a later `sim` cannot
   be treated as acceptance of an offer the lead never saw.
2. Replaying the same runtime result produced timestamp-based public assistant
   IDs and duplicated Sales Inbox messages. Runtime replies now use stable IDs
   derived from the persisted run and message index.

Two production replays of the already-paid request returned the same three
assistant IDs. Supabase retained exactly three stable assistant rows after both
replays. Runtime usage remained one row and `$0.006091`; no second model call
or charge occurred.

## No-cost verification

- Focused compiler: `42 passed`.
- Widget adapter: `11 passed`.
- Full Spec 012: `294 passed / 718 deselected`.
- Active production gate: `526 passed`.
- Aggregate zero-cost gates: `6/6 passed`.
- TypeScript: passed.
- Focused ESLint and Ruff: passed.
- Local Next.js production build: passed.
- Vercel production build: passed.
- `git diff --check`: passed with line-ending warnings only.

The correction remains LLM-first. The LLM still interprets the product
question and selects the structured action/fact key. Deterministic code only
keeps persisted delivery idempotent and prevents state from claiming an offer
that was not rendered.
