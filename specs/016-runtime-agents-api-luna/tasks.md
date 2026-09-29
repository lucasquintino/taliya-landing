# 016 — Runtime Agents API com Luna Max

**Status:** proposta de execução; implementação não iniciada nesta auditoria.
**Responsável:** Backend/IA.
**Dependências:** 014, 015.

## Tarefas
- [ ] **T016-01** — Criar adaptador v2 por trás da fronteira comercial atual, preservando linguagem e transporte úteis. Requisitos: R016-01, R016-02. Recorte: [execution.md#t016-01](execution.md#t016-01).
- [ ] **T016-02** — Homologar SDK/REST e payload na conta com ferramentas somente de leitura e custo limitado aprovado. Requisitos: R016-01, R016-04. Recorte: [execution.md#t016-02](execution.md#t016-02).
- [ ] **T016-03** — Implementar registry de versões e binding das sessões; desenhar migração de sessões abertas. Requisitos: R016-02. Recorte: [execution.md#t016-03](execution.md#t016-03).
- [ ] **T016-04** — Acoplar fila/worker existente, inbox/outbox, lease, retry e dead-letter; não usar after() como garantia de durabilidade. Requisitos: R016-03. Recorte: [execution.md#t016-04](execution.md#t016-04).
- [ ] **T016-05** — Consumir ações e eventos documentados, persistir resultados e reconstruir estado após desconexão. Requisitos: R016-03, R016-04. Recorte: [execution.md#t016-05](execution.md#t016-05).
- [ ] **T016-06** — Medir Luna/max, limites operacionais e fallback estático; registrar teste real e não somente JSON válido. Requisitos: R016-01, R016-02, R016-03, R016-04, R016-05. Recorte: [execution.md#t016-06](execution.md#t016-06).

Não marcar uma tarefa porque o arquivo existe. Acrescentar caminho do diff, comando e resultado verificável ao concluí-la. Se o código atual já atende, comprovar por teste e registrar reuso em vez de reimplementar.

## Preparação técnica de implementação — 2026-09-28

[Recorte executável](execution.md) detalha fontes atuais, caminhos propostos, interfaces, dados, falhas, dependências e verificação por tarefa. Prevalece sobre a lista de caminhos candidatos do snapshot quando houver divergência registrada. Requisitos e critérios de aceite permanecem integrais.

Esta preparação não altera o estado de execução nem libera dependências. Somente 013 está ativa. Comandos existentes e limites estão em [IMPLEMENTATION_READINESS](../../docs/taliya-sdd/IMPLEMENTATION_READINESS.md).
