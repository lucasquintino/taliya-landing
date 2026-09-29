# 024 — QA integrada, segurança, performance e evals

**Status:** proposta de execução; implementação não iniciada nesta auditoria.
**Responsável:** QA + backend/frontend + produto.
**Dependências:** 018, 019, 020, 021, 022, 023.

## Tarefas
- [ ] **T024-01** — Integrar testes e comandos ao CI real; separar offline, mocks, sandbox e execução paga. Requisitos: R024-01. Recorte: [execution.md#t024-01](execution.md#t024-01).
- [ ] **T024-02** — Portar casos aproveitáveis da suíte anterior, substituir roteiros de Pilates e adicionar os casos deste plano. Requisitos: R024-01, R024-02. Recorte: [execution.md#t024-02](execution.md#t024-02).
- [ ] **T024-03** — Rodar cenários financeiros controlados nas quatro combinações do billing construído na 015 e conferir analytics/cliente/acesso. Requisitos: R024-03. Recorte: [execution.md#t024-03](execution.md#t024-03).
- [ ] **T024-04** — Executar fault injection, segurança, teste manual acessível e baseline de desempenho/rede móvel. Requisitos: R024-04. Recorte: [execution.md#t024-04](execution.md#t024-04).
- [ ] **T024-05** — Rodar bateria Luna/max com orçamento aprovado e rubric de correção/completude/brevidade; não usar somente juiz LLM. Requisitos: R024-02, R024-05. Recorte: [execution.md#t024-05](execution.md#t024-05).
- [ ] **T024-06** — Executar analyze/converge e resolver gaps; compilar dossiê sanitizado para gate de release. Requisitos: R024-01, R024-02, R024-03, R024-04, R024-05. Recorte: [execution.md#t024-06](execution.md#t024-06).

Não marcar uma tarefa porque o arquivo existe. Acrescentar caminho do diff, comando e resultado verificável ao concluí-la. Se o código atual já atende, comprovar por teste e registrar reuso em vez de reimplementar.

## Preparação técnica de implementação — 2026-09-28

[Recorte executável](execution.md) detalha fontes atuais, caminhos propostos, interfaces, dados, falhas, dependências e verificação por tarefa. Prevalece sobre a lista de caminhos candidatos do snapshot quando houver divergência registrada. Requisitos e critérios de aceite permanecem integrais.

Esta preparação não altera o estado de execução nem libera dependências. Somente 013 está ativa. Comandos existentes e limites estão em [IMPLEMENTATION_READINESS](../../docs/taliya-sdd/IMPLEMENTATION_READINESS.md).
