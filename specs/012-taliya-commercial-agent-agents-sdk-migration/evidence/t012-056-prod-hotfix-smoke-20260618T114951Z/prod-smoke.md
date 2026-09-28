# T012-056 production hotfix smoke

- Started: 2026-06-18T11:49:51.725Z
- Finished: 2026-06-18T11:50:43.633Z
- Runtime: https://taliya-agent-runtime-production.up.railway.app
- Cost cap: $0.15
- Total reported cost: $0.026891
- Final verdict: PASS

## direct-diagnostic-100

Goal: Direct diagnostic CTA then numeric answer must not fallback/500 on second turn.
Conversation: spec012-prod-smoke-20260618T114951Z-direct-diagnostic-100

### Turn 1

User: Quero fazer diagn?stico gratuito

Assistant: Oi, tudo bem?

Em que posso ajudar?
Assistant: Claro, faço sim. Para te devolver algo útil, vou entender rapidinho como está a rotina do studio hoje.
Assistant: Hoje seu studio tem mais ou menos quantos alunos ativos?

Status: HTTP 200, runtime succeeded, action start_requested_diagnostic, route entry, diagnostic not_started
Usage: model gpt-5.4-mini, input 0, output 0, cost $0.003928

### Turn 2

User: 100

Assistant: Entendi. Já dá para ter uma noção do tamanho do studio.
Assistant: Quais partes mais dão trabalho hoje: WhatsApp, agenda/reposições, vendas, financeiro ou acompanhamento dos alunos?

Status: HTTP 200, runtime succeeded, action capture_pending_diagnostic_answer, route entry, diagnostic not_started
Usage: model gpt-5.4-mini, input 0, output 0, cost $0.002543

Checks:
- no_500_on_second_turn: PASS
- no_instability_fallback_on_second_turn: PASS
- asks_next_diagnostic_question_after_100: PASS

Quality review:
- Boa: o segundo turno saiu de 500/fallback e avancou naturalmente do numero de alunos para a proxima pergunta de rotina.

## opening-acceptance-no-name

Goal: Widget opening acceptance must start diagnostic without asking lead name.
Conversation: spec012-prod-smoke-20260618T114951Z-opening-acceptance-no-name

### Turn 1

User: (empty widget opening)

Assistant: Oi! Pode me mandar sua mensagem ou dúvida para eu entender como posso te ajudar?

Status: HTTP 200, runtime succeeded, action clarify_ambiguous_opening, route entry, diagnostic not_started
Usage: model gpt-5.4-mini, input 0, output 0, cost $0.007193

### Turn 2

User: quero sim

Assistant: Claro, faço sim. Para te devolver algo útil, vou entender rapidinho como está a rotina do studio hoje.
Assistant: Hoje seu studio tem mais ou menos quantos alunos ativos?

Status: HTTP 200, runtime succeeded, action start_requested_diagnostic, route entry, diagnostic not_started
Usage: model gpt-5.4-mini, input 0, output 0, cost $0.003847

Checks:
- no_name_question_after_acceptance: PASS
- starts_diagnostic_after_acceptance: PASS

Quality review:
- Boa: aceitou o diagnostico e foi direto para a primeira pergunta util, sem capturar nome cedo.

## ambiguous-diagnostic-answer

Goal: Ambiguous diagnostic answer must be clarified instead of accepted as answered.
Conversation: spec012-prod-smoke-20260618T114951Z-ambiguous-diagnostic-answer

### Turn 1

User: Quero fazer diagn?stico gratuito

Assistant: Oi, tudo bem?

Em que posso ajudar?
Assistant: Claro, faço sim. Para te devolver algo útil, vou entender rapidinho como está a rotina do studio hoje.
Assistant: Hoje seu studio tem mais ou menos quantos alunos ativos?

Status: HTTP 200, runtime succeeded, action start_requested_diagnostic, route entry, diagnostic not_started
Usage: model gpt-5.4-mini, input 0, output 0, cost $0.003938

### Turn 2

User: 100

Assistant: Entendi. Já dá para ter uma noção do tamanho do studio.
Assistant: Quais partes mais dão trabalho hoje: WhatsApp, agenda/reposições, vendas, financeiro ou acompanhamento dos alunos?

Status: HTTP 200, runtime succeeded, action capture_pending_diagnostic_answer, route entry, diagnostic not_started
Usage: model gpt-5.4-mini, input 0, output 0, cost $0.002548

### Turn 3

User: depende do dia

Assistant: Você quer dizer que a maior dificuldade muda bastante? Me fala a principal em média, mesmo que seja aproximada.

Status: HTTP 200, runtime succeeded, action clarify_ambiguous_diagnostic_answer, route entry, diagnostic not_started
Usage: model gpt-5.4-mini, input 0, output 0, cost $0.002893

Checks:
- no_500_on_ambiguous_turn: PASS
- clarifies_ambiguous_answer: PASS
- does_not_advance_as_answered: PASS

Check notes:
- clarifies_ambiguous_answer: Manual conversational review corrected the local matcher: assistant said "Voc? quer dizer que a maior dificuldade muda bastante? Me fala a principal em m?dia...", which is a valid clarification of an ambiguous diagnostic answer.

Quality review:
- PASS: a resposta ambigua nao foi aceita como suficiente; o agente escolheu clarify_ambiguous_diagnostic_answer e pediu uma resposta principal/aproximada no mesmo slot.

## Final Verdict

- All production turn requests returned HTTP 200/runtime succeeded.
- No user-facing instability fallback appeared.
- Diagnostic acceptance no longer asks for name before diagnostic.
- Ambiguous diagnostic answer is clarified instead of being accepted as answered.