# 021 — Instrumentação confiável e integração PostHog

**Status:** proposta de execução; implementação não iniciada nesta auditoria.
**Responsável:** Backend/frontend + analytics.
**Dependências:** 017, 018, 019, 020.

## Abordagem técnica
Registrar acontecimentos canônicos uma vez e conectar a jornada sem depender do modelo.

A abordagem de domínio e as interfaces propostas estão em `../../docs/taliya-sdd/03_ARQUITETURA_E_CONTRATOS.md`. A implementação deve referenciar as interfaces reais descobertas na 013; os caminhos abaixo pertencem ao ZIP inspecionado e são candidatos de integração, não prova da árvore atual.

## Pontos de integração observados
- `lib/landing/ai-attendant/funnel-events.ts`
- `app/api/landing/ai-attendant/events/route.ts`
- `lib/landing/ai-attendant/storage/postgres.ts`
- `components/landing/shared/FloatingAiAttendant.tsx`

## Ordem de execução
1. Mapear eventos existentes para catálogo v3 com compatibilidade e corte de versão.
2. Instrumentar produtores da landing, runtime, app e billing sem duplicar o mesmo evento client/server.
3. Conectar SDKs e preferências de coleta; associar identidade sem fingerprinting.
4. Implementar relay/outbox/dedup, alertas de atraso e rotina de reconciliação de marcos críticos.
5. Configurar projeto PostHog conforme limites reais da conta; homologação usa mock/local ou projeto isolado autorizado.
6. Executar jornadas canônicas e ataque de evento financeiro fabricado; conferir relatórios contra fonte real.

## Dados, permissões e observabilidade
Cada mudança de estado material deve ter ator, autorização, recibo persistido e evento de domínio. Fronteiras entre bancos/serviços usam outbox e reconciliação, não uma transação distribuída presumida. Métricas públicas de browser não comprovam dinheiro ou acesso. Não registrar segredos ou dados de terceiros em prompts/analytics.

## Testes e rollback
Executar os casos `C021-01` a `C021-05` e a regressão dos contratos afetados. Usar feature flag da capacidade e migrações compatíveis para rollback; nenhuma volta ao roteiro Pilates. Registrar em `verification.md`.

## Esforço de referência
2–4 dias de engenharia focada, estimativa de planejamento, não prazo garantido. Não inclui espera por autorização, fornecimento de mídia ou acesso externo. Reestimar ao fechar 013.

## Preparação técnica de implementação — 2026-09-28

[Recorte executável](execution.md) detalha fontes atuais, caminhos propostos, interfaces, dados, falhas, dependências e verificação por tarefa. Prevalece sobre a lista de caminhos candidatos do snapshot quando houver divergência registrada. Requisitos e critérios de aceite permanecem integrais.

Esta preparação não altera o estado de execução nem libera dependências. Somente 013 está ativa. Comandos existentes e limites estão em [IMPLEMENTATION_READINESS](../../docs/taliya-sdd/IMPLEMENTATION_READINESS.md).
