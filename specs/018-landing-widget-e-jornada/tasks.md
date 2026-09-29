# 018 — Landing, widget e integração à assinatura

**Status:** proposta de execução; implementação não iniciada nesta auditoria.
**Responsável:** Frontend + design/QA.
**Dependências:** 015, 017.

## Tarefas
- [ ] **T018-01** — Mapear cada CTA atual e destino existente; alterar somente handlers e conteúdo necessário ao contrato. Requisitos: R018-01. Recorte: [execution.md#t018-01](execution.md#t018-01).
- [ ] **T018-02** — Atualizar widget para nova resposta, cards e estado assíncrono com IDs estáveis. Requisitos: R018-02, R018-03. Recorte: [execution.md#t018-02](execution.md#t018-02).
- [ ] **T018-03** — Implementar retomada/autenticação sem confiar em sessionId do navegador; preservar conversa autorizada. Requisitos: R018-03, R018-04. Recorte: [execution.md#t018-03](execution.md#t018-03).
- [ ] **T018-04** — Fazer baseline visual e corrigir foco/teclado/safe-area/scroll/tamanhos/contraste no recorte alterado. Requisitos: R018-02, R018-04. Recorte: [execution.md#t018-04](execution.md#t018-04).
- [ ] **T018-05** — Revisar FAQ, oferta, metadata, redirects e indexação com a mesma fonte de produto. Requisitos: R018-05. Recorte: [execution.md#t018-05](execution.md#t018-05).
- [ ] **T018-06** — Executar regressão de contratação direta e assistida em mobile/desktop e registrar capturas. Requisitos: R018-01, R018-02, R018-03, R018-04, R018-05. Recorte: [execution.md#t018-06](execution.md#t018-06).

Não marcar uma tarefa porque o arquivo existe. Acrescentar caminho do diff, comando e resultado verificável ao concluí-la. Se o código atual já atende, comprovar por teste e registrar reuso em vez de reimplementar.

## Preparação técnica de implementação — 2026-09-28

[Recorte executável](execution.md) detalha fontes atuais, caminhos propostos, interfaces, dados, falhas, dependências e verificação por tarefa. Prevalece sobre a lista de caminhos candidatos do snapshot quando houver divergência registrada. Requisitos e critérios de aceite permanecem integrais.

Esta preparação não altera o estado de execução nem libera dependências. Somente 013 está ativa. Comandos existentes e limites estão em [IMPLEMENTATION_READINESS](../../docs/taliya-sdd/IMPLEMENTATION_READINESS.md).
