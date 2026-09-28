# T012-057 real-model transcripts

- Schema: `012.real_model_golden_transcripts.v1`
- Started at: `2026-08-05T00:49:09.744180+00:00`
- Finished at: `2026-08-05T00:49:16.093280+00:00`
- Model: `gpt-5.6-luna`
- Paid approval: `Aprovo o T012-057 com gpt-5.6-luna e teto cumulativo máximo de US$ 0,75.`
- Paid call status: `attempted_real_openai`
- Budget cap: `$0.03`
- Total cost: `$0.007805`
- Total model operations: `2`
- Passed scenarios: `1/1`
- Aborted: `False`

## Scenario Summary

- `luna-waitlist-hesitation`: passed (2 ops, $0.007805)

## Full Message Exchanges

### luna-waitlist-hesitation

Status: `passed`

**user:** quero começar, me coloca na lista

**assistant:** Perfeito. Posso deixar seu interesse registrado na lista.

**assistant:** Hoje a entrada acontece por uma lista para um número pequeno de studios. Posso deixar o interesse registrado sem prometer entrada imediata, data ou condição especial.

**user:** talvez, antes eu queria entender melhor

**assistant:** Claro. O que você quer entender melhor antes de decidir?

Checks:
- `PASS` turn_statuses_acceptable
- `PASS` includes:O que você quer entender melhor antes de decidir?
- `PASS` excludes:qual é o nome do studio
- `PASS` excludes:deixei seu studio na lista
- `PASS` excludes:checkout
- `PASS` excludes:desconto
- `PASS` template_present:waitlist.offer_after_contract_intent
- `PASS` template_present:waitlist.pause_decision
- `PASS` no_failed_turns
