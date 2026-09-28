# T012-057 real-model transcripts

- Schema: `012.real_model_golden_transcripts.v1`
- Started at: `2026-08-05T01:13:43.550795+00:00`
- Finished at: `2026-08-05T01:13:46.697316+00:00`
- Model: `gpt-5.6-luna`
- Paid approval: `Aprovo o T012-057 com gpt-5.6-luna e teto cumulativo máximo de US$ 0,75.`
- Paid call status: `attempted_real_openai`
- Budget cap: `$0.01`
- Total cost: `$0.003570`
- Total model operations: `1`
- Passed scenarios: `1/1`
- Aborted: `False`

## Scenario Summary

- `final-waitlist-joined`: passed (1 ops, $0.003570)

## Full Message Exchanges

### final-waitlist-joined

Status: `passed`

**user:** pode colocar o Studio Viva em Vitoria ES

**assistant:** Perfeito, deixei seu interesse registrado para a equipe da Taliya.

**assistant:** Studio: Studio Viva.

**assistant:** Cidade/estado: Vitória, ES.

Checks:
- `PASS` turn_statuses_acceptable
- `PASS` includes:Studio Viva
- `PASS` includes:Vitoria
- `PASS` excludes:checkout
- `PASS` excludes:VIP
- `PASS` excludes:desconto
- `PASS` no_failed_turns
