# T012-043 real-model golden transcripts

- Schema: `012.real_model_golden_transcripts.v1`
- Started at: `2026-06-15T19:33:52.463382+00:00`
- Finished at: `2026-06-15T19:34:40.520784+00:00`
- Model: `gpt-5.4-mini`
- Paid approval: `User approved paid T012-043 test in chat on 2026-06-15: 'aprovado o teste pago'.`
- Paid call status: `attempted_real_openai`
- Budget cap: `$1.00`
- Total cost: `$0.044396`
- Total model operations: `19`
- Passed scenarios: `7/9`
- Aborted: `False`

## Scenario Summary

- `final-price-first`: passed (2 ops, $0.004300)
- `final-price-plus-pain`: passed (2 ops, $0.004874)
- `final-pain-first`: passed (2 ops, $0.004595)
- `final-instagram-interest`: passed (2 ops, $0.004412)
- `final-whatsapp-question`: passed (2 ops, $0.004062)
- `step3g-long-conversation`: failed (3 ops, $0.008221)
  Issues: turn_statuses_acceptable; includes:R$ 497: missing expected rendered text; includes:diagnostico: missing expected rendered text; includes:demonstra: missing expected rendered text; no_failed_turns: price_question_missing_price_answer, price_question_missing_diagnostic_hook, price_question_missing_diagnostic_offer
- `final-waitlist-joined`: passed (1 ops, $0.002626)
- `final-human-request-silent-after`: passed (2 ops, $0.003972)
- `final-demo-request`: failed (3 ops, $0.007333)
  Issues: turn_statuses_acceptable; includes:/pilates/planos/demonstracao: missing expected rendered text; includes:demo: missing expected rendered text; no_failed_turns: demo_direct_question_flags_missing

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

Status: `passed`

**user:** tenho reposicao baguncada na agenda e queria saber preco

**assistant:** Oi, tudo bem?

Base: R$ 197/mes. Essencial: R$ 497/mes. Avance: R$ 897/mes. Completo: R$ 1.497/mes.

**assistant:** Como você comentou que a reposição está bagunçada na agenda, faz sentido olhar um plano que ajude a organizar isso com mais clareza.

Posso fazer um diagnostico gratuito com poucas perguntas e te devolver o que organizar primeiro, quais agentes fariam sentido e qual plano vale comparar.

**assistant:** O que voce acha?

Checks:
- `PASS` turn_statuses_acceptable
- `PASS` includes:R$ 497 - missing expected rendered text
- `PASS` includes:reposi - missing expected rendered text
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

**assistant:** Você está perdendo interessados porque as respostas no WhatsApp estão demorando e a conversa esfria antes de virar agenda.

Posso fazer um diagnostico gratuito com poucas perguntas e te devolver o que organizar primeiro, quais agentes fariam sentido e qual plano vale comparar.

**assistant:** O que voce acha?

Checks:
- `PASS` turn_statuses_acceptable
- `PASS` includes:diagnostico gratuito - missing expected rendered text
- `PASS` includes:WhatsApp - missing expected rendered text
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

Status: `failed`

_No rendered exchange was recorded._

### final-waitlist-joined

Status: `passed`

**user:** pode colocar o Studio Viva em Vitoria ES

**assistant:** Perfeito, deixei seu interesse registrado para a equipe da Taliya.

**assistant:** Studio: Studio Viva.

**assistant:** Cidade/estado: Vitória, ES.

Checks:
- `PASS` turn_statuses_acceptable
- `PASS` includes:Studio Viva - missing expected rendered text
- `PASS` includes:Vitoria - missing expected rendered text
- `PASS` excludes:checkout - banned rendered text present
- `PASS` excludes:VIP - banned rendered text present
- `PASS` excludes:desconto - banned rendered text present
- `PASS` no_failed_turns

### final-human-request-silent-after

Status: `passed`

**user:** quero falar com uma pessoa

**assistant:** Claro. Vou deixar uma pessoa assumir daqui.

**assistant:** Tambem deixo o contexto salvo para voce nao precisar repetir tudo.

Checks:
- `PASS` turn_statuses_acceptable
- `PASS` includes:pessoa - missing expected rendered text
- `PASS` excludes:diagnostico gratuito - banned rendered text present
- `PASS` excludes:checkout - banned rendered text present
- `PASS` second_turn_silent - second turn rendered a message or was not suppressed
- `PASS` no_failed_turns

### final-demo-request

Status: `failed`

_No rendered exchange was recorded._
