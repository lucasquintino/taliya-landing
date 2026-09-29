# 020 — Taliya Internal mínimo e operação humana

**Status:** proposta de execução; implementação não iniciada nesta auditoria.
**Responsável:** Frontend/backend + operação.
**Dependências:** 014, 017.

## Tarefas
- [ ] **T020-01** — Resolver dono/domínio do Internal antes de escolher onde alterar o código. Requisitos: R020-01. Recorte: [execution.md#t020-01](execution.md#t020-01).
- [ ] **T020-02** — Reaproveitar fila/ficha atuais retirando campos Pilates/diagnóstico e controles financeiros fictícios. Requisitos: R020-02, R020-05. Recorte: [execution.md#t020-02](execution.md#t020-02).
- [ ] **T020-03** — Implementar estados de atendimento com versão/lock; validar take_over/resume_ai no worker e na outbox. Requisitos: R020-04. Recorte: [execution.md#t020-03](execution.md#t020-03).
- [ ] **T020-04** — Implementar entrega humana web se faltar; no WhatsApp revisar timestamp do último inbound e regras do provedor. Requisitos: R020-03. Recorte: [execution.md#t020-04](execution.md#t020-04).
- [ ] **T020-05** — Adicionar pesquisa, filtros, notas operacionais mínimas e atalhos para serviços oficiais sem novos dashboards. Requisitos: R020-02, R020-05. Recorte: [execution.md#t020-05](execution.md#t020-05).
- [ ] **T020-06** — Treinar operação com cenário de erro e garantir auditoria de identidade, envio e pausa. Requisitos: R020-01, R020-02, R020-03, R020-04, R020-05. Recorte: [execution.md#t020-06](execution.md#t020-06).

Não marcar uma tarefa porque o arquivo existe. Acrescentar caminho do diff, comando e resultado verificável ao concluí-la. Se o código atual já atende, comprovar por teste e registrar reuso em vez de reimplementar.

## Preparação técnica de implementação — 2026-09-28

[Recorte executável](execution.md) detalha fontes atuais, caminhos propostos, interfaces, dados, falhas, dependências e verificação por tarefa. Prevalece sobre a lista de caminhos candidatos do snapshot quando houver divergência registrada. Requisitos e critérios de aceite permanecem integrais.

Esta preparação não altera o estado de execução nem libera dependências. Somente 013 está ativa. Comandos existentes e limites estão em [IMPLEMENTATION_READINESS](../../docs/taliya-sdd/IMPLEMENTATION_READINESS.md).
