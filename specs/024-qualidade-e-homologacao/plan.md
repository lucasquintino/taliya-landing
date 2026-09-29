# 024 — QA integrada, segurança, performance e evals

**Status:** proposta de execução; implementação não iniciada nesta auditoria.
**Responsável:** QA + backend/frontend + produto.
**Dependências:** 018, 019, 020, 021, 022, 023.

## Abordagem técnica
Provar a jornada completa com dados controlados e falhas deliberadas antes da liberação.

A abordagem de domínio e as interfaces propostas estão em `../../docs/taliya-sdd/03_ARQUITETURA_E_CONTRATOS.md`. A implementação deve referenciar as interfaces reais descobertas na 013; os caminhos abaixo pertencem ao ZIP inspecionado e são candidatos de integração, não prova da árvore atual.

## Pontos de integração observados
- `package.json`
- `scripts/`
- `services/taliya-agent-runtime/tests/`
- `specs/013–025 (novos artefatos)`

## Ordem de execução
1. Integrar testes e comandos ao CI real; separar offline, mocks, sandbox e execução paga.
2. Portar casos aproveitáveis da suíte anterior, substituir roteiros de Pilates e adicionar os casos deste plano.
3. Rodar cenários financeiros controlados nas quatro combinações do billing construído na 015 e conferir analytics/cliente/acesso.
4. Executar fault injection, segurança, teste manual acessível e baseline de desempenho/rede móvel.
5. Rodar bateria Luna/max com orçamento aprovado e rubric de correção/completude/brevidade; não usar somente juiz LLM.
6. Executar analyze/converge e resolver gaps; compilar dossiê sanitizado para gate de release.

## Dados, permissões e observabilidade
Cada mudança de estado material deve ter ator, autorização, recibo persistido e evento de domínio. Fronteiras entre bancos/serviços usam outbox e reconciliação, não uma transação distribuída presumida. Métricas públicas de browser não comprovam dinheiro ou acesso. Não registrar segredos ou dados de terceiros em prompts/analytics.

## Testes e rollback
Executar os casos `C024-01` a `C024-05` e a regressão dos contratos afetados. Usar feature flag da capacidade e migrações compatíveis para rollback; nenhuma volta ao roteiro Pilates. Registrar em `verification.md`.

## Esforço de referência
3–5 dias de engenharia focada, estimativa de planejamento, não prazo garantido. Não inclui espera por autorização, fornecimento de mídia ou acesso externo. Reestimar ao fechar 013.

## Preparação técnica de implementação — 2026-09-28

[Recorte executável](execution.md) detalha fontes atuais, caminhos propostos, interfaces, dados, falhas, dependências e verificação por tarefa. Prevalece sobre a lista de caminhos candidatos do snapshot quando houver divergência registrada. Requisitos e critérios de aceite permanecem integrais.

Esta preparação não altera o estado de execução nem libera dependências. Somente 013 está ativa. Comandos existentes e limites estão em [IMPLEMENTATION_READINESS](../../docs/taliya-sdd/IMPLEMENTATION_READINESS.md).
