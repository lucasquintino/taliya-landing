# 025 — Migração, publicação controlada e operação

**Status:** proposta de execução; implementação não iniciada nesta auditoria.
**Responsável:** Liderança técnica + operação/produto.
**Dependências:** 024.

## Abordagem técnica
Encerrar com serviço operável, rollback seguro e indicadores confiáveis, não apenas código compilando.

A abordagem de domínio e as interfaces propostas estão em `../../docs/taliya-sdd/03_ARQUITETURA_E_CONTRATOS.md`. A implementação deve referenciar as interfaces reais descobertas na 013; os caminhos abaixo pertencem ao ZIP inspecionado e são candidatos de integração, não prova da árvore atual.

## Pontos de integração observados
- `next.config.ts`
- `variáveis e pipelines de deploy atuais (mapear na 013)`
- `AGENTS.md`
- `docs de operação e status`

## Ordem de execução
1. Ensaiar backup/migração/restore em homologação e reconciliar dados/sessões legadas.
2. Registrar autorização de deploy, flags, versões e playbook de rollback; não executar por inferência do pedido de plano.
3. Liberar interno e coortes graduais com janela mínima e volume documentado; baixa amostra não vira aprovação estatística.
4. Monitorar fila, latência, erros, incidentes, discrepâncias financeiras e gasto; pausar ao ultrapassar gate crítico.
5. Treinar operador e fazer simulação de queda OpenAI/PostHog/banco/canal e takeover.
6. Consolidar evidências, fechar specs e publicar handoff; programar revisão operacional no sistema escolhido, não implicitamente no ChatGPT.

## Dados, permissões e observabilidade
Cada mudança de estado material deve ter ator, autorização, recibo persistido e evento de domínio. Fronteiras entre bancos/serviços usam outbox e reconciliação, não uma transação distribuída presumida. Métricas públicas de browser não comprovam dinheiro ou acesso. Não registrar segredos ou dados de terceiros em prompts/analytics.

## Testes e rollback
Executar os casos `C025-01` a `C025-05` e a regressão dos contratos afetados. Usar feature flag da capacidade e migrações compatíveis para rollback; nenhuma volta ao roteiro Pilates. Registrar em `verification.md`.

## Esforço de referência
1–2 dias de engenharia focada, estimativa de planejamento, não prazo garantido. Não inclui espera por autorização, fornecimento de mídia ou acesso externo. Reestimar ao fechar 013.

## Preparação técnica de implementação — 2026-09-28

[Recorte executável](execution.md) detalha fontes atuais, caminhos propostos, interfaces, dados, falhas, dependências e verificação por tarefa. Prevalece sobre a lista de caminhos candidatos do snapshot quando houver divergência registrada. Requisitos e critérios de aceite permanecem integrais.

Esta preparação não altera o estado de execução nem libera dependências. Somente 013 está ativa. Comandos existentes e limites estão em [IMPLEMENTATION_READINESS](../../docs/taliya-sdd/IMPLEMENTATION_READINESS.md).
