# T012-057 real-model transcripts

- Schema: `012.real_model_golden_transcripts.v1`
- Started at: `2026-08-05T00:34:34.000728+00:00`
- Finished at: `2026-08-05T00:34:47.003331+00:00`
- Model: `gpt-5.6-luna`
- Paid approval: `Aprovo o T012-057 com gpt-5.6-luna e teto cumulativo máximo de US$ 0,75.`
- Paid call status: `attempted_real_openai`
- Budget cap: `$0.08`
- Total cost: `$0.011370`
- Total model operations: `4`
- Passed scenarios: `1/3`
- Aborted: `True`
- Abort reason: `runtime_error_in_luna-waitlist-hesitation`

## Scenario Summary

- `luna-price-objection-context`: passed (4 ops, $0.011370)
- `luna-waitlist-hesitation`: runtime_error (0 ops, $0.000000)
  Issues: SalesInboxProjectionBuildError: Sales Inbox projection failed validation: sales_inbox_diagnostic_fields_missing:[{"code":"sales_inbox_diagnostic_fields_missing","severity":"P0","message":"completed diagnostic projection missing required fields: diagnostic_ledger_complete, final_plan_or_range, final_demo_line","path":"sales_inbox_projection.fields"}]

## Full Message Exchanges

### luna-price-objection-context

Status: `passed`

**user:** quanto custa?

**assistant:** Oi, tudo bem?

**assistant:** Base: R$ 197/mês. Essencial: R$ 497/mês. Avance: R$ 897/mês. Completo: R$ 1.497/mês.

**assistant:** Se fizer sentido para você, estamos oferecendo um diagnóstico gratuito para o seu studio. Assim você entende se algum dos nossos planos te atenderia.

**assistant:** Com poucas perguntas, eu entendo a rotina do studio e te devolvo o que organizar primeiro, quais agentes fariam sentido e qual plano vale comparar.

**assistant:** O que você acha?

**user:** hmm, talvez fique pesado

**assistant:** Entendo. É um valor para olhar com calma mesmo.

**assistant:** O ponto é que a Taliya não é só mais uma ferramenta: ela ajuda nas rotinas que fazem o studio girar, como WhatsApp, retorno de interessados, agenda, reposições, cobranças e acompanhamento.

**assistant:** Para decidir sem pressa, podemos usar o diagnóstico gratuito para comparar prioridade e plano, ou deixar seu interesse na lista de espera se você já quiser seguir.

Checks:
- `PASS` turn_statuses_acceptable
- `PASS` includes:R$ 197
- `PASS` includes:valor para olhar com calma
- `PASS` excludes:rotina pesada
- `PASS` excludes:agenda pesada
- `PASS` excludes:reposição pesada
- `PASS` excludes:checkout
- `PASS` excludes:desconto
- `PASS` template_present:product.price_direct
- `PASS` template_present:product.price_objection_value
- `PASS` no_failed_turns

### luna-waitlist-hesitation

Status: `runtime_error`

_No rendered exchange was recorded._
