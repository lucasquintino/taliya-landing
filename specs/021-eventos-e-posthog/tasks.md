# 021 — Instrumentação confiável e integração PostHog

**Status:** proposta de execução; implementação não iniciada nesta auditoria.
**Responsável:** Backend/frontend + analytics.
**Dependências:** 017, 018, 019, 020.

## Tarefas
- [ ] **T021-01** — Mapear eventos existentes para catálogo v3 com compatibilidade e corte de versão. Requisitos: R021-01. Recorte: [execution.md#t021-01](execution.md#t021-01).
- [ ] **T021-02** — Instrumentar produtores da landing, runtime, app e billing sem duplicar o mesmo evento client/server. Requisitos: R021-01, R021-02. Recorte: [execution.md#t021-02](execution.md#t021-02).
- [ ] **T021-03** — Conectar SDKs e preferências de coleta; associar identidade sem fingerprinting. Requisitos: R021-03, R021-04. Recorte: [execution.md#t021-03](execution.md#t021-03).
- [ ] **T021-04** — Implementar relay/outbox/dedup, alertas de atraso e rotina de reconciliação de marcos críticos. Requisitos: R021-05. Recorte: [execution.md#t021-04](execution.md#t021-04).
- [ ] **T021-05** — Configurar projeto PostHog conforme limites reais da conta; homologação usa mock/local ou projeto isolado autorizado. Requisitos: R021-04. Recorte: [execution.md#t021-05](execution.md#t021-05).
- [ ] **T021-06** — Executar jornadas canônicas e ataque de evento financeiro fabricado; conferir relatórios contra fonte real. Requisitos: R021-01, R021-02, R021-03, R021-04, R021-05. Recorte: [execution.md#t021-06](execution.md#t021-06).

Não marcar uma tarefa porque o arquivo existe. Acrescentar caminho do diff, comando e resultado verificável ao concluí-la. Se o código atual já atende, comprovar por teste e registrar reuso em vez de reimplementar.

## Preparação técnica de implementação — 2026-09-28

[Recorte executável](execution.md) detalha fontes atuais, caminhos propostos, interfaces, dados, falhas, dependências e verificação por tarefa. Prevalece sobre a lista de caminhos candidatos do snapshot quando houver divergência registrada. Requisitos e critérios de aceite permanecem integrais.

Esta preparação não altera o estado de execução nem libera dependências. Somente 013 está ativa. Comandos existentes e limites estão em [IMPLEMENTATION_READINESS](../../docs/taliya-sdd/IMPLEMENTATION_READINESS.md).
