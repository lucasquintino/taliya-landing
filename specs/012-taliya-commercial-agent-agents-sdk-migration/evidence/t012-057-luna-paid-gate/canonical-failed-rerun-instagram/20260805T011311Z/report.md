# T012-057 real-model transcripts

- Schema: `012.real_model_golden_transcripts.v1`
- Started at: `2026-08-05T01:13:11.721327+00:00`
- Finished at: `2026-08-05T01:13:16.666757+00:00`
- Model: `gpt-5.6-luna`
- Paid approval: `Aprovo o T012-057 com gpt-5.6-luna e teto cumulativo máximo de US$ 0,75.`
- Paid call status: `attempted_real_openai`
- Budget cap: `$0.01`
- Total cost: `$0.005639`
- Total model operations: `2`
- Passed scenarios: `1/1`
- Aborted: `False`

## Scenario Summary

- `final-instagram-interest`: passed (2 ops, $0.005639)

## Full Message Exchanges

### final-instagram-interest

Status: `passed`

**user:** vim pelo Instagram e gostaria de saber mais

**assistant:** Oi, tudo bem?

**assistant:** A Taliya é a IA do seu studio de Pilates para organizar agenda, reposições, cobranças, gestão, atendimento e acompanhamento em um só lugar.

**assistant:** Se fizer sentido, posso fazer um diagnóstico gratuito com poucas perguntas para entender a rotina, os gargalos e a prioridade do seu studio. O que você acha?

Checks:
- `PASS` turn_statuses_acceptable
- `PASS` includes:studio
- `PASS` excludes:lead came from the site
- `PASS` excludes:utm_source
- `PASS` excludes:source_label
- `PASS` template_present:opening.instagram_source
- `PASS` no_failed_turns
