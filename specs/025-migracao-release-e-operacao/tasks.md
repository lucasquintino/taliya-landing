# 025 — Migração, publicação controlada e operação

**Status:** proposta de execução; implementação não iniciada nesta auditoria.
**Responsável:** Liderança técnica + operação/produto.
**Dependências:** 024.

## Tarefas
- [ ] **T025-01** — Ensaiar backup/migração/restore em homologação e reconciliar dados/sessões legadas. Requisitos: R025-01. Recorte: [execution.md#t025-01](execution.md#t025-01).
- [ ] **T025-02** — Registrar autorização de deploy, flags, versões e playbook de rollback; não executar por inferência do pedido de plano. Requisitos: R025-02, R025-03. Recorte: [execution.md#t025-02](execution.md#t025-02).
- [ ] **T025-03** — Liberar interno e coortes graduais com janela mínima e volume documentado; baixa amostra não vira aprovação estatística. Requisitos: R025-02. Recorte: [execution.md#t025-03](execution.md#t025-03).
- [ ] **T025-04** — Monitorar fila, latência, erros, incidentes, discrepâncias financeiras e gasto; pausar ao ultrapassar gate crítico. Requisitos: R025-04. Recorte: [execution.md#t025-04](execution.md#t025-04).
- [ ] **T025-05** — Treinar operador e fazer simulação de queda OpenAI/PostHog/banco/canal e takeover. Requisitos: R025-03, R025-04. Recorte: [execution.md#t025-05](execution.md#t025-05).
- [ ] **T025-06** — Consolidar evidências, fechar specs e publicar handoff; programar revisão operacional no sistema escolhido, não implicitamente no ChatGPT. Requisitos: R025-01, R025-02, R025-03, R025-04, R025-05. Recorte: [execution.md#t025-06](execution.md#t025-06).

Não marcar uma tarefa porque o arquivo existe. Acrescentar caminho do diff, comando e resultado verificável ao concluí-la. Se o código atual já atende, comprovar por teste e registrar reuso em vez de reimplementar.

## Preparação técnica de implementação — 2026-09-28

[Recorte executável](execution.md) detalha fontes atuais, caminhos propostos, interfaces, dados, falhas, dependências e verificação por tarefa. Prevalece sobre a lista de caminhos candidatos do snapshot quando houver divergência registrada. Requisitos e critérios de aceite permanecem integrais.

Esta preparação não altera o estado de execução nem libera dependências. Somente 013 está ativa. Comandos existentes e limites estão em [IMPLEMENTATION_READINESS](../../docs/taliya-sdd/IMPLEMENTATION_READINESS.md).
