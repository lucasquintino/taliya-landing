# T012-060 Luna production watch and migration closeout

## Decision

T012-060 is complete under the approved no-real-leads production scope. Luna
remains active. No synthetic paid conversation was generated merely to extend
an empty monitoring window.

## Exact production identity

- GitHub branch: `master`.
- Git commit: `5c15aed6a68a2907789e34843d7c4efd152cf927`.
- Vercel project: `lucasquintinos-projects/taliya-landing`.
- Vercel deployment: `dpl_E7EPTbJoKiXuf5ekNq27W33PEcSB` (`READY`).
- Public aliases: `https://www.taliya.com.br` and `https://taliya.com.br`.
- Railway project: `steadfast-acceptance`.
- Railway service: `taliya-agent-runtime`.
- Railway deployment: `48ae1d84-63db-4633-8288-b8af40246e0f`
  (`SUCCESS`).
- Railway image digest:
  `sha256:41ffef5ecf2c7c788acfe385ee86bea0d5fc4f6ec537c6a8e88ff3e7a759fb58`.

Railway `/healthz` returned:

```json
{
  "ok": true,
  "service": "taliya-agent-runtime",
  "environment": "production",
  "build_sha": "5c15aed6a68a2907789e34843d7c4efd152cf927",
  "model": "gpt-5.6-luna",
  "reasoning_effort": "none",
  "openai_sdk_version": "2.44.0",
  "agents_sdk_version": "0.18.0"
}
```

## Production transcript and persistence

The single approved paid production smoke remains the complete production
conversation used for migration acceptance:

```text
lead: como funciona no WhatsApp?

assistant: Oi, tudo bem?

assistant: O aluno não precisa baixar aplicativo nem criar senha. Ele conversa
no WhatsApp; a Taliya registra a ação, atualiza o painel e avisa o responsável.

assistant: Se quiser ver isso funcionando na prática, aqui está uma
demonstração: https://www.taliya.com.br/pilates/planos/demonstracao
```

Persisted evidence:

- conversation: `t012059_luna_prod_smoke_2_1785894540`;
- run: `run_fce0735f630f4f04aa8ee661569d44cc`;
- trace: `trace_8968eb1eddce4080b5dc8a69650393e1`;
- status: `succeeded`;
- model: `gpt-5.6-luna`;
- model operations: `2`;
- repairs: `0`;
- input tokens: `4,531`;
- output tokens: `260`;
- cost: `$0.006091`.

Two no-cost public replays returned the same three stable assistant IDs. The
runtime persisted one run and one conversation charge; no new runtime run or
cost appeared after the smoke. Older timestamp-based duplicate assistant rows
remain isolated to this explicitly named test lead and predate the idempotency
fix.

## Operational watch

- Supabase project `pxvabrsngfhebytdqxth`: `ACTIVE_HEALTHY`.
- Railway 5xx after final activation: none found.
- Vercel production 5xx during the closeout check: none found.
- New runtime runs after the paid smoke: `0`.
- Additional cost after the paid smoke: `$0`.
- New real leads available for transcript review: `0`.

The earlier runbook recommended a two-hour active watch for real traffic. This
production environment has no real leads, as previously recorded by the user.
Waiting without traffic would not add behavioral evidence, while generating
synthetic Luna turns would spend the approved budget without product value.
The migration therefore closes on the observable production checks above;
future real conversations are routine production monitoring.

## Final approved-budget accounting

- Approved cumulative ceiling: `$0.750000`.
- Reported cumulative spend: `$0.691486`.
- Conservative unreconciled reserve: `$0.020000`.
- Operationally accounted total: `$0.711486`.
- Remaining approved ceiling: `$0.038514`.

No paid call was made during T012-060.

## Scope and architecture

The production agent remains LLM-first. No raw lead-text commercial router,
template-first brain, direct free-form SDK delivery, or legacy commercial
fallback was added. No `/pilates` visual, Sales Inbox UI, checkout,
multi-tenant, or client/studio WhatsApp surface was changed for this closeout.

## Closure

Spec 012 implementation and the Luna production migration are complete. The
next work is ordinary monitoring of real production traffic and separately
approved product iteration, not another migration task.
