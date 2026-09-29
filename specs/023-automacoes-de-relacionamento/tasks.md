# 023 — Automações enxutas de relacionamento

**Status:** proposta de execução; implementação não iniciada nesta auditoria.
**Responsável:** Operação + backend/analytics.
**Dependências:** 017, 020, 021, 022.

## Tarefas
- [ ] **T023-01** — Inventariar todas as notificações atuais e designar um emissor por categoria. Requisitos: R023-03. Recorte: [execution.md#t023-01](execution.md#t023-01).
- [ ] **T023-02** — Configurar Workflows quando disponível ou reutilizar a automação já adotada sem criar motor paralelo. Requisitos: R023-01. Recorte: [execution.md#t023-02](execution.md#t023-02).
- [ ] **T023-03** — Criar webhook de solicitação autenticado e revalidação server-side antes da entrega pelo provedor existente. Requisitos: R023-02. Recorte: [execution.md#t023-03](execution.md#t023-03).
- [ ] **T023-04** — Criar templates curtos com link seguro, cancelamento de contato e nenhum desconto inventado. Requisitos: R023-01, R023-04. Recorte: [execution.md#t023-04](execution.md#t023-04).
- [ ] **T023-05** — Testar supressão em corrida com pagamento/opt-out/pausa humana e limites do provedor. Requisitos: R023-02, R023-03, R023-04. Recorte: [execution.md#t023-05](execution.md#t023-05).
- [ ] **T023-06** — Liberar de forma controlada somente após aprovação de mensagem, canal e volume; documentar kill switch. Requisitos: R023-01, R023-02, R023-03, R023-04, R023-05. Recorte: [execution.md#t023-06](execution.md#t023-06).

Não marcar uma tarefa porque o arquivo existe. Acrescentar caminho do diff, comando e resultado verificável ao concluí-la. Se o código atual já atende, comprovar por teste e registrar reuso em vez de reimplementar.

## Preparação técnica de implementação — 2026-09-28

[Recorte executável](execution.md) detalha fontes atuais, caminhos propostos, interfaces, dados, falhas, dependências e verificação por tarefa. Prevalece sobre a lista de caminhos candidatos do snapshot quando houver divergência registrada. Requisitos e critérios de aceite permanecem integrais.

Esta preparação não altera o estado de execução nem libera dependências. Somente 013 está ativa. Comandos existentes e limites estão em [IMPLEMENTATION_READINESS](../../docs/taliya-sdd/IMPLEMENTATION_READINESS.md).
