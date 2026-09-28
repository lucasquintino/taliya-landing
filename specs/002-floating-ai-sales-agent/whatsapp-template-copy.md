# WhatsApp Template Copy: SaaS Sales

## Purpose

Define the v1 WhatsApp template set for SaaS sales, follow-up, payment/onboarding updates and opt-out.

These templates are drafts for Meta approval and must be reviewed against the current WhatsApp Business Platform rules before production use. Outside the allowed service window, proactive WhatsApp messages may be sent only when an approved template exists and the contact is eligible for follow-up.

Current template category model to use at submission time:

- `MARKETING`: commercial follow-up, plan recommendation, demo follow-up, custom-agent sales conversation and re-engagement.
- `UTILITY`: transactional/account/payment/onboarding/opt-out updates that are tied to an existing request or transaction.
- `AUTHENTICATION`: login/OTP only. Not used by these sales templates.

Language:

```text
pt_BR
```

Variables use `{{1}}`, `{{2}}` style placeholders so the final provider setup can map them to lead/studio/plan/context values.

## Global Rules

- Do not send templates after opt-out or `do_not_contact`.
- Do not include payment card data, raw billing documents or sensitive student data.
- Do not imply guaranteed financial results.
- Do not mention private pilot offers.
- Use trusted checkout, plan and onboarding links only.
- Prefer free-form reply inside the active WhatsApp service window.
- Use templates only for proactive/out-of-window messages or provider-required transactional updates.
- If a template is rejected, paused, disabled or not approved, the system must not send that proactive message outside the allowed conversation window.
- Every template send attempt must create a Sales Inbox event.

## V1 Template Inventory

| # | Internal name | Category | Owner | Primary trigger |
| ---: | --- | --- | --- | --- |
| 1 | `saa_sales_followup_pos_conversa` | MARKETING | n8n | Meaningful web/WhatsApp conversation stopped |
| 2 | `saa_sales_recomendacao_plano` | MARKETING | n8n/operator | Recommended plan exists and lead did not continue |
| 3 | `saa_sales_link_planos` | MARKETING | operator/n8n | Lead asked to compare plans and needs the plans link |
| 4 | `saa_sales_checkout_pendente` | UTILITY | billing/n8n | Checkout link created/sent but payment not confirmed |
| 5 | `saa_sales_demo_concluida` | MARKETING | n8n | Real guided demo completed and lead did not continue |
| 6 | `saa_sales_agente_sob_medida` | MARKETING | operator/n8n | Lead requested unmapped/custom operation |
| 7 | `saa_sales_humano_assumiu` | UTILITY | Sales Inbox | Human operator took over or will reply |
| 8 | `saa_sales_onboarding_pos_pagamento` | UTILITY | billing/system | Payment confirmed and onboarding link exists |
| 9 | `saa_sales_pagamento_nao_confirmado` | UTILITY | billing/n8n | Payment failed, expired or not completed |
| 10 | `saa_sales_optout_confirmacao` | UTILITY | system | Lead asked to stop proactive messages |
| 11 | `saa_sales_garantia_30_dias` | UTILITY | operator/system | Customer asks about guarantee after subscribing |
| 12 | `saa_sales_cota_limite_atingido` | UTILITY | product/system | Paying customer hit usage cap |

## Template 1: Post-Conversation Follow-Up

Internal name:

```text
saa_sales_followup_pos_conversa
```

Category: `MARKETING`

Purpose: follow up after a meaningful consultor conversation when the lead did not continue.

Trigger:

- lead is `warm` or `hot`;
- contact is allowed;
- no opt-out;
- no human-active block;
- no payment confirmed yet.

Variables:

- `{{1}}`: lead first name.
- `{{2}}`: main pain discussed.
- `{{3}}`: next recommended step.

Body:

```text
Oi, {{1}}. Aqui e da Taliya. Conversamos sobre {{2}} no seu studio e deixei separado o proximo passo mais indicado: {{3}}. Quer continuar por aqui?
```

Buttons:

- `Continuar`
- `Ver proximo passo`

## Template 2: Plan Recommendation Reminder

Internal name:

```text
saa_sales_recomendacao_plano
```

Category: `MARKETING`

Purpose: remind a qualified lead of the recommended plan.

Trigger:

- `recommendedPlanId` exists;
- lead is `plan_ready` or `checkout_ready`;
- lead did not open/sign after recommendation;
- no opt-out.

Variables:

- `{{1}}`: lead first name.
- `{{2}}`: main pain/profile.
- `{{3}}`: recommended plan name.
- `{{4}}`: short benefit summary.

Body:

```text
{{1}}, pelo que voce contou sobre {{2}}, o plano mais indicado para o seu studio e {{3}}. Ele ajuda com {{4}}. Quer ver o comparativo ou seguir para a assinatura segura?
```

Buttons:

- `Ver comparativo`
- `Assinar`

## Template 3: Plans Link

Internal name:

```text
saa_sales_link_planos
```

Category: `MARKETING`

Purpose: send the public plans page when the lead asked to compare plans or requested pricing context.

Trigger:

- lead explicitly asked for plans/prices/comparison;
- plan-display gate exists;
- no opt-out.

Variables:

- `{{1}}`: lead first name.
- `{{2}}`: trusted plans link.

Body:

```text
{{1}}, aqui esta o comparativo dos planos da Taliya: {{2}}. Se quiser, eu tambem posso te ajudar a escolher o melhor plano para o seu studio por aqui.
```

Buttons:

- `Abrir planos`
- `Me ajude a escolher`

## Template 4: Pending Checkout

Internal name:

```text
saa_sales_checkout_pendente
```

Category: `UTILITY`

Purpose: follow up when checkout was sent/opened but payment was not confirmed.

Trigger:

- trusted checkout exists;
- payment not confirmed;
- checkout still valid or can be regenerated;
- no opt-out.

Variables:

- `{{1}}`: lead first name.
- `{{2}}`: selected plan name.

Body:

```text
Oi, {{1}}. A assinatura do plano {{2}} ainda nao foi confirmada. O acesso so e liberado depois da confirmacao segura do pagamento. Quer receber o link novamente?
```

Buttons:

- `Enviar link`
- `Tirar duvida`

## Template 5: Guided Demo Completed

Internal name:

```text
saa_sales_demo_concluida
```

Category: `MARKETING`

Purpose: follow up after the real guided demo was completed.

Trigger:

- real guided demo completed;
- lead did not move to plan/checkout/WhatsApp after completion;
- no opt-out.

Variables:

- `{{1}}`: lead first name.
- `{{2}}`: demo scenario/pain.
- `{{3}}`: recommended next step.

Body:

```text
{{1}}, voce viu a Taliya funcionando no fluxo de {{2}}. O proximo passo recomendado e {{3}}. Quer ver o plano indicado ou falar com um consultor?
```

Buttons:

- `Ver plano`
- `Falar com consultor`

## Template 6: Custom Agent Request

Internal name:

```text
saa_sales_agente_sob_medida
```

Category: `MARKETING`

Purpose: follow up when the lead asked for an unmapped operation/custom agent.

Trigger:

- conversion path is `custom_agent_follow_up`;
- custom-agent request has operation summary;
- no opt-out.

Variables:

- `{{1}}`: lead first name.
- `{{2}}`: requested operation.

Body:

```text
Oi, {{1}}. Recebi seu interesse em um agente sob medida para {{2}}. Esse tipo de agente e tratado separadamente dos planos publicos. Quer me passar mais detalhes da operacao que voce quer automatizar?
```

Buttons:

- `Enviar detalhes`
- `Falar com consultor`

## Template 7: Human Takeover

Internal name:

```text
saa_sales_humano_assumiu
```

Category: `UTILITY`

Purpose: confirm that a human operator has taken or will take over the conversation.

Trigger:

- Sales Inbox status becomes `human_active` or `handoff_requested`;
- lead asked for human help or operator took over;
- no opt-out.

Variables:

- `{{1}}`: lead first name.
- `{{2}}`: expected response window, e.g. `ate 1 dia util`.

Body:

```text
{{1}}, recebi seu pedido para falar com uma pessoa. Um consultor vai continuar o atendimento por aqui em {{2}}. Enquanto isso, suas informacoes ja ficaram salvas para nao precisar repetir tudo.
```

Buttons:

- `Ok`

## Template 8: Post-Payment Onboarding

Internal name:

```text
saa_sales_onboarding_pos_pagamento
```

Category: `UTILITY`

Purpose: send onboarding link after trusted payment confirmation.

Trigger:

- billing webhook confirms trusted paid/received payment;
- pending tenant activation/onboarding link exists;
- contact is allowed for transactional message.

Variables:

- `{{1}}`: customer first name.
- `{{2}}`: secure onboarding link.

Body:

```text
Pagamento confirmado, {{1}}. Seu acesso a Taliya ja pode ser iniciado. Use este link seguro para configurar o studio com o setup guiado por Agente IA: {{2}}
```

Buttons:

- `Comecar setup`

## Template 9: Payment Not Confirmed

Internal name:

```text
saa_sales_pagamento_nao_confirmado
```

Category: `UTILITY`

Purpose: clarify that failed/expired/incomplete payment did not activate the plan.

Trigger:

- billing indicates failed, expired, incomplete or unpaid payment;
- selected plan exists;
- no paid entitlement was created.

Variables:

- `{{1}}`: lead first name.
- `{{2}}`: selected plan name.

Body:

```text
Oi, {{1}}. O pagamento do plano {{2}} ainda nao foi concluido, entao o acesso nao foi ativado. Se quiser tentar novamente, posso te enviar um novo link seguro de pagamento.
```

Buttons:

- `Novo link`
- `Tirar duvida`

## Template 10: Opt-Out Confirmation

Internal name:

```text
saa_sales_optout_confirmacao
```

Category: `UTILITY`

Purpose: confirm that proactive messages stopped after opt-out when allowed.

Trigger:

- lead sends stop/parar/sair/cancelar mensagens/nao quero or equivalent opt-out.

Variables:

- `{{1}}`: lead first name.

Body:

```text
Tudo certo, {{1}}. Nao enviaremos novas mensagens proativas sobre a Taliya neste contato. Se quiser voltar a conversar, e so chamar por aqui.
```

Buttons:

- none

## Template 11: 30-Day Guarantee Info

Internal name:

```text
saa_sales_garantia_30_dias
```

Category: `UTILITY`

Purpose: send guarantee information when requested by a subscribed or checkout-ready customer.

Trigger:

- customer asks about cancellation/refund/guarantee;
- trusted public-plan guarantee policy is configured;
- no private/custom plan terms apply.

Variables:

- `{{1}}`: customer first name.

Body:

```text
{{1}}, os planos publicos mensais da Taliya tem 30 dias de garantia na primeira assinatura. Se a Taliya nao fizer sentido para o seu studio nesse periodo, voce pode cancelar e solicitar reembolso conforme a politica dos planos publicos.
```

Buttons:

- `Entendi`
- `Falar com consultor`

## Template 12: Usage Cap Reached

Internal name:

```text
saa_sales_cota_limite_atingido
```

Category: `UTILITY`

Purpose: notify a paying customer that automated AI usage reached the plan cap.

Trigger:

- tenant reaches 100% of included AI message cap;
- add-on/upgrade path is configured;
- customer contact is allowed for account/utility updates.

Variables:

- `{{1}}`: customer first name.
- `{{2}}`: plan name.
- `{{3}}`: trusted quota/upgrade link or next action.

Body:

```text
{{1}}, seu plano {{2}} atingiu o limite de mensagens de IA deste ciclo. As automacoes extras ficam pausadas ate voce adicionar cota ou fazer upgrade. Proximo passo: {{3}}
```

Buttons:

- `Adicionar cota`
- `Ver upgrade`

## Anti-Duplicate Rule

Each proactive template send must use this idempotency key:

```text
leadId + templateName + triggerReason + cycleDate
```

If the key already exists as sent, sending is skipped.

## Sales Inbox Events

Each template attempt must record:

- `template_send_requested`
- `template_sent`
- `template_blocked_not_approved`
- `template_blocked_opt_out`
- `template_failed`
- `template_replied`

Events must include template name, category, lead ID, channel ID, status, provider message ID when available and failure reason when applicable.

## Approval Checklist

- Template variables mapped and validated.
- Category reviewed before submission.
- No unsupported guarantee or result claim.
- No private pilot mention.
- No raw sensitive data.
- Correct approved category selected in WhatsApp provider.
- Opt-out behavior tested.
- Idempotency key tested.
- Fallback exists when template is not approved.
