# 014 — Identidade, dados e segurança de base

**Status:** proposta de execução; implementação não iniciada nesta auditoria.
**Responsável:** Backend + segurança.
**Dependências:** 013.

## Tarefas
- [ ] **T014-01** — Mapear entidades existentes; definir relações e projeções comerciais sem duplicar identidade ou billing. Requisitos: R014-02. Recorte: [execution.md#t014-01](execution.md#t014-01).
- [ ] **T014-02** — Integrar staff auth e RBAC viewer/operator/admin; eliminar token da URL e header de ator não confiável. Requisitos: R014-01. Recorte: [execution.md#t014-02](execution.md#t014-02).
- [ ] **T014-03** — Adicionar sessão web opaca e validação server-side de posse; vincular conta somente após autenticação. Requisitos: R014-02, R014-03. Recorte: [execution.md#t014-03](execution.md#t014-03).
- [ ] **T014-04** — Migrar somente tabelas/índices necessários com rollback; revisar pool/TLS e permissões dos leitores analíticos. Requisitos: R014-04. Recorte: [execution.md#t014-04](execution.md#t014-04).
- [ ] **T014-05** — Implementar saneamento de logs, estados de consentimento e caminho auditável de exclusão. Requisitos: R014-05. Recorte: [execution.md#t014-05](execution.md#t014-05).
- [ ] **T014-06** — Executar testes de autorização/IDOR/merge/produção sem banco; registrar evidências. Requisitos: R014-01, R014-02, R014-03, R014-04, R014-05. Recorte: [execution.md#t014-06](execution.md#t014-06).

Não marcar uma tarefa porque o arquivo existe. Acrescentar caminho do diff, comando e resultado verificável ao concluí-la. Se o código atual já atende, comprovar por teste e registrar reuso em vez de reimplementar.

## Preparação técnica de implementação — 2026-09-28

[Recorte executável](execution.md) detalha fontes atuais, caminhos propostos, interfaces, dados, falhas, dependências e verificação por tarefa. Prevalece sobre a lista de caminhos candidatos do snapshot quando houver divergência registrada. Requisitos e critérios de aceite permanecem integrais.

Esta preparação não altera o estado de execução nem libera dependências. Somente 013 está ativa. Comandos existentes e limites estão em [IMPLEMENTATION_READINESS](../../docs/taliya-sdd/IMPLEMENTATION_READINESS.md).
