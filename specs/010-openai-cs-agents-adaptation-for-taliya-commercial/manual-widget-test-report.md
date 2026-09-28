# Manual Widget Test Report

**Current interpretation**: historical local smoke evidence only. This report does not approve final behavior readiness after the final product-owner correction. Final approval requires tasks T206-T226, zero-cost gates, quota-limited real OpenAI correction scenarios, updated mapped behavior transcripts, Sales Inbox completeness, and product-owner transcript approval.

Date: 2026-05-22

Target: `http://localhost:3999/api/landing/ai-attendant`

Runtime: local `taliya-agent-runtime` on `http://127.0.0.1:8088`, provider `mock`, HMAC `dev-secret`.

## Summary

- Price question: passed. The widget route called the runtime, answered official prices directly, and returned `agentRuntimeProductSourceVersion`.
- Thin diagnostic: passed. The agent did not fake a completed diagnosis and asked one focused question.
- Waitlist: passed. Buying intent offered waitlist; acceptance without studio/city stayed `pending_details` instead of pretending the lead was fully joined.

## Transcripts

### widget-price

Lead: quanto custa e serve para studio pequeno?

Taliya: Claro. Hoje os planos da Taliya para studios de Pilates comecam em R$ 197/mes no Base, R$ 497/mes no Essencial, R$ 897/mes no Avance e R$ 1.497/mes no Completo. Se voce me contar o que mais pesa na rotina, eu te ajudo a entender qual faixa faz mais sentido.

Runtime: `taliya_commercial_product_agent`, product source `taliya-commercial-2026-05-22`.

### widget-diagnostic-thin

Lead: quero um diagnostico

Taliya: Qual parte da rotina mais pesa hoje: agenda, reposicoes, interessados, mensalidades ou alunos inativos?

Runtime: `taliya_commercial_diagnostic_agent`, diagnostic status `in_progress`.

### widget-waitlist

Lead: Quero assinar agora

Taliya: Hoje a Taliya esta trabalhando com um numero pequeno de studios e nao libera assinatura direta por aqui. Se fizer sentido, posso colocar seu studio na lista de espera e a equipe chama quando abrir uma proxima janela.

Lead: Pode colocar

Taliya: Combinado. Para deixar a lista de espera acionavel, ainda preciso do nome do studio e cidade/estado. Pode me mandar nessa mesma mensagem?

Runtime: `taliya_commercial_waitlist_agent`, waitlist status `pending_details`, missing fields `studio_name, city_state`.

