# T012-043 real-model golden transcripts

- Schema: `012.real_model_golden_transcripts.v1`
- Started at: `2026-06-15T17:20:44.542652+00:00`
- Finished at: `2026-06-15T17:22:00.623312+00:00`
- Model: `gpt-5.4-mini`
- Paid approval: `User approved paid T012-043 test in chat on 2026-06-15: 'aprovado o teste pago'.`
- Paid call status: `attempted_real_openai`
- Budget cap: `$1.00`
- Total cost: `$0.021497`
- Total model operations: `10`
- Passed scenarios: `4/9`
- Aborted: `True`
- Abort reason: `runtime_error_in_step3g-long-conversation`

## Scenario Summary

- `final-price-first`: passed (2 ops, $0.004200)
- `final-price-plus-pain`: failed (2 ops, $0.004575)
  Issues: includes:reposicoes: missing expected rendered text
- `final-pain-first`: passed (2 ops, $0.004352)
- `final-instagram-interest`: passed (2 ops, $0.004160)
- `final-whatsapp-question`: passed (2 ops, $0.004209)
- `step3g-long-conversation`: runtime_error (0 ops, $0.000000)
  Issues: SalesInboxProjectionBuildError: Sales Inbox projection failed validation: sales_inbox_diagnostic_status_mismatch:[{"code":"sales_inbox_diagnostic_status_mismatch","severity":"P0","message":"Sales Inbox diagnostic status does not match decision/context","path":"sales_inbox_projection.diagnostic_status"}]

## Full Message Exchanges

### final-price-first

Status: `passed`

**user:** quanto custa?

**assistant:** Oi, tudo bem?

Base: R$ 197/mes. Essencial: R$ 497/mes. Avance: R$ 897/mes. Completo: R$ 1.497/mes.

**assistant:** Se fizer sentido para voce, estamos oferecendo um diagnostico gratuito para o seu studio. Assim voce entende se algum dos nossos planos te atenderia.

Com poucas perguntas, eu entendo a rotina do studio e te devolvo o que organizar primeiro, quais agentes fariam sentido e qual plano vale comparar.

**assistant:** O que voce acha?

Checks:
- `PASS` turn_statuses_acceptable
- `PASS` includes:R$ 197 - missing expected rendered text
- `PASS` includes:R$ 497 - missing expected rendered text
- `PASS` includes:R$ 897 - missing expected rendered text
- `PASS` includes:R$ 1.497 - missing expected rendered text
- `PASS` excludes:checkout - banned rendered text present
- `PASS` excludes:link de pagamento - banned rendered text present
- `PASS` excludes:Reliable profile first name - banned rendered text present
- `PASS` template_present:product.price_direct - template was not selected
- `PASS` template_present:diagnostic.price_hook - template was not selected
- `PASS` no_failed_turns

### final-price-plus-pain

Status: `failed`

**user:** tenho reposicao baguncada na agenda e queria saber preco

**assistant:** Oi, tudo bem?

Base: R$ 197/mes. Essencial: R$ 497/mes. Avance: R$ 897/mes. Completo: R$ 1.497/mes.

**assistant:** Como você está com a reposição bagunçada na agenda, posso te mostrar o plano que ajuda a organizar esse fluxo sem virar mais trabalho pra equipe.

Posso fazer um diagnostico gratuito com poucas perguntas e te devolver o que organizar primeiro, quais agentes fariam sentido e qual plano vale comparar.

**assistant:** O que voce acha?

Checks:
- `PASS` turn_statuses_acceptable
- `PASS` includes:R$ 497 - missing expected rendered text
- `FAIL` includes:reposicoes - missing expected rendered text
- `PASS` includes:diagnostico gratuito - missing expected rendered text
- `PASS` excludes:497 alunos - banned rendered text present
- `PASS` excludes:checkout - banned rendered text present
- `PASS` excludes:lista VIP - banned rendered text present
- `PASS` template_present:product.price_direct - template was not selected
- `PASS` template_present:diagnostic.price_hook_with_context - template was not selected
- `PASS` no_failed_turns

### final-pain-first

Status: `passed`

**user:** perco muitos interessados no WhatsApp porque a equipe demora para responder

**assistant:** Oi, tudo bem?

Em que posso ajudar?

**assistant:** Você está perdendo oportunidades porque o WhatsApp demora para responder e os interessados esfriam antes de alguém falar com eles.

Posso fazer um diagnostico gratuito com poucas perguntas e te devolver o que organizar primeiro, quais agentes fariam sentido e qual plano vale comparar.

**assistant:** O que voce acha?

Checks:
- `PASS` turn_statuses_acceptable
- `PASS` includes:diagnostico gratuito - missing expected rendered text
- `PASS` includes:interessados - missing expected rendered text
- `PASS` excludes:lead loses - banned rendered text present
- `PASS` excludes:interested leads - banned rendered text present
- `PASS` excludes:team takes too long - banned rendered text present
- `PASS` excludes:clientes - banned rendered text present
- `PASS` excludes:consumidores - banned rendered text present
- `PASS` excludes:alunos ativos - banned rendered text present
- `PASS` template_present:diagnostic.offer_soft - template was not selected
- `PASS` no_failed_turns

### final-instagram-interest

Status: `passed`

**user:** vim pelo Instagram e gostaria de saber mais

**assistant:** Oi, tudo bem?

**assistant:** A Taliya e a IA do seu studio de Pilates para organizar agenda, reposicoes, cobrancas, gestao, atendimento e acompanhamento em um so lugar.

**assistant:** Se fizer sentido, posso fazer um diagnostico gratuito com poucas perguntas para entender a rotina, os gargalos e a prioridade do seu studio. O que voce acha?

Checks:
- `PASS` turn_statuses_acceptable
- `PASS` includes:studio - missing expected rendered text
- `PASS` excludes:lead came from the site - banned rendered text present
- `PASS` excludes:utm_source - banned rendered text present
- `PASS` excludes:source_label - banned rendered text present
- `PASS` template_present:opening.instagram_source - template was not selected
- `PASS` no_failed_turns

### final-whatsapp-question

Status: `passed`

**user:** como funciona no WhatsApp?

**assistant:** Oi, tudo bem?

**assistant:** O aluno nao precisa baixar aplicativo nem criar senha. Ele conversa no WhatsApp; a Taliya registra a acao, atualiza o painel e avisa o responsavel. Para atuar nas conversas de alunos, o WhatsApp Business do studio precisa estar conectado/configurado. Nao prometa configuracao automatica no chat comercial.

**assistant:** Ver demonstracao: https://www.taliya.com.br/pilates/planos/demonstracao

Checks:
- `PASS` turn_statuses_acceptable
- `PASS` includes:WhatsApp - missing expected rendered text
- `PASS` includes:aluno - missing expected rendered text
- `PASS` includes:nao precisa baixar aplicativo - missing expected rendered text
- `PASS` excludes:me passa o WhatsApp - banned rendered text present
- `PASS` excludes:manda o telefone - banned rendered text present
- `PASS` excludes:instalar app - banned rendered text present
- `PASS` template_present:product.whatsapp_direct - template was not selected
- `PASS` no_failed_turns

### step3g-long-conversation

Status: `runtime_error`

_No rendered exchange was recorded._
