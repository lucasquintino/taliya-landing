# T012-057 real-model transcripts

- Schema: `012.real_model_golden_transcripts.v1`
- Started at: `2026-08-05T01:26:46.381088+00:00`
- Finished at: `2026-08-05T01:26:56.189779+00:00`
- Model: `gpt-5.6-luna`
- Paid approval: `Aprovo o T012-057 com gpt-5.6-luna e teto cumulativo máximo de US$ 0,75.`
- Paid call status: `attempted_real_openai`
- Budget cap: `$0.01`
- Total cost: `$0.006085`
- Total model operations: `2`
- Passed scenarios: `1/1`
- Aborted: `False`

## Scenario Summary

- `final-whatsapp-question`: passed (2 ops, $0.006085)

## Full Message Exchanges

### final-whatsapp-question

Status: `passed`

**user:** como funciona no WhatsApp?

**assistant:** Oi, tudo bem?

**assistant:** O aluno não precisa baixar aplicativo nem criar senha. Ele conversa no WhatsApp; a Taliya registra a ação, atualiza o painel e avisa o responsável.

**assistant:** Se quiser ver isso funcionando na prática, aqui está uma demonstração: https://www.taliya.com.br/pilates/planos/demonstracao

Checks:
- `PASS` turn_statuses_acceptable
- `PASS` includes:WhatsApp
- `PASS` includes:aluno
- `PASS` includes:nao precisa baixar aplicativo
- `PASS` excludes:me passa o WhatsApp
- `PASS` excludes:manda o telefone
- `PASS` excludes:instalar app
- `PASS` template_present:product.whatsapp_direct
- `PASS` no_failed_turns
