# T012-048 product-owner approval

- Date: 2026-06-16
- Approval type: limited product-owner approval
- Scope approved: technical advance to simulated/no-cost shadow mode
- Public activation approved: no
- Real lead traffic approved: no
- Paid OpenAI calls approved by this decision: no

## User Approval

The user clarified that production has no real leads yet and that the full
real-traffic shadow preparation is not needed right now:

> nao temos leads reais ainda, n precisa de toda essa preparacao, o ambiente de
> producao n ta com leads ainda

Codex then restated the narrower approval scope as:

> Aprovar que a fase de validacao interna da T012-043 ate T012-047 esta
> suficiente e que podemos avancar para testes de integracao/simulacao, sem
> leads reais e sem ativacao publica.

Codex also proposed the explicit approval wording:

> Aprovo a T012-048 apenas como aprovacao para avancar tecnicamente para
> shadow/simulacao sem leads reais, sem ativacao publica e sem custo pago
> automatico.

The user approved:

> pode ser, aprovado

## Approved Next Step

This closes T012-048 only as permission to move from verification evidence to
simulated/no-cost shadow work. It authorizes T012-050 in simulated mode using
fixtures and injected no-cost SDK models.

## Explicit Non-Approvals

This approval does not authorize:

- public activation;
- real lead traffic shadowing;
- paid OpenAI calls;
- external provider trace export with lead text;
- `/pilates` visual/layout/copy changes;
- Sales Inbox UI changes;
- checkout/payment work;
- multi-tenant work;
- client/studio WhatsApp connection work.

## Evidence Already Available Before Approval

- T012-043: real-model golden transcripts passed 9/9.
- T012-044: do-not-do fixtures passed in no-cost Spec 012 gate.
- T012-045: mandatory trace package exported.
- T012-046: Sales Inbox projection package exported.
- T012-047: manual transcript review package prepared with decision pending.

## Closure

T012-048 is closed as a limited product-owner approval for simulated/no-cost
shadow mode only. T012-050 may proceed in simulated mode. Real traffic and
public activation still require later explicit approval.
