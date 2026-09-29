# 017 — Cinco ferramentas e ciclo de leads/clientes

**Status:** proposta de execução; implementação não iniciada nesta auditoria.
**Responsável:** Backend comercial + app/billing.
**Dependências:** 014, 015, 016.

## Tarefas
- [ ] **T017-01** — Implementar handlers restritos com schemas, contexto autenticado, versões e recibos persistidos. Requisitos: R017-01. Recorte: [execution.md#t017-01](execution.md#t017-01).
- [ ] **T017-02** — Reutilizar contato/lead store com patch allowlist e prova por message_id original. Requisitos: R017-02. Recorte: [execution.md#t017-02](execution.md#t017-02).
- [ ] **T017-03** — Assinar eventos de domínio do app/billing ou consultar projeção via interfaces existentes; definir idempotência e reconciliação. Requisitos: R017-03, R017-04, R017-05. Recorte: [execution.md#t017-03](execution.md#t017-03).
- [ ] **T017-04** — Desativar conversão antiga baseada no texto no caminho v2; mapear compatibilidade para UI sem preservar regras de diagnóstico. Requisitos: R017-05. Recorte: [execution.md#t017-04](execution.md#t017-04).
- [ ] **T017-05** — Conectar navegação à contratação e cliente ativo à gestão/app, sem iniciar pagamento dentro da ferramenta. Requisitos: R017-01, R017-03, R017-04. Recorte: [execution.md#t017-05](execution.md#t017-05).
- [ ] **T017-06** — Testar compra sem IA, criação assistida, renovação, falha e migração de contatos históricos. Requisitos: R017-01, R017-02, R017-03, R017-04, R017-05. Recorte: [execution.md#t017-06](execution.md#t017-06).

Não marcar uma tarefa porque o arquivo existe. Acrescentar caminho do diff, comando e resultado verificável ao concluí-la. Se o código atual já atende, comprovar por teste e registrar reuso em vez de reimplementar.

## Preparação técnica de implementação — 2026-09-28

[Recorte executável](execution.md) detalha fontes atuais, caminhos propostos, interfaces, dados, falhas, dependências e verificação por tarefa. Prevalece sobre a lista de caminhos candidatos do snapshot quando houver divergência registrada. Requisitos e critérios de aceite permanecem integrais.

Esta preparação não altera o estado de execução nem libera dependências. Somente 013 está ativa. Comandos existentes e limites estão em [IMPLEMENTATION_READINESS](../../docs/taliya-sdd/IMPLEMENTATION_READINESS.md).
