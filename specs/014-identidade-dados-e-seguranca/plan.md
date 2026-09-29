# 014 — Identidade, dados e segurança de base

**Status:** proposta de execução; implementação não iniciada nesta auditoria.
**Responsável:** Backend + segurança.
**Dependências:** 013.

## Abordagem técnica
Garantir que cada escrita pertença ao contato/negócio correto e que a operação administrativa seja autenticada.

A abordagem de domínio e as interfaces propostas estão em `../../docs/taliya-sdd/03_ARQUITETURA_E_CONTRATOS.md`. A implementação deve referenciar as interfaces reais descobertas na 013; os caminhos abaixo pertencem ao ZIP inspecionado e são candidatos de integração, não prova da árvore atual.

## Pontos de integração observados
- `app/api/internal/sales-inbox/auth.ts`
- `app/internal/sales-inbox/page.tsx`
- `lib/landing/ai-attendant/sales-inbox-store.ts`
- `lib/landing/ai-attendant/storage/postgres.ts`
- `lib/landing/ai-attendant/schema.ts`

## Ordem de execução
1. Mapear entidades existentes; definir relações e projeções comerciais sem duplicar identidade ou billing.
2. Integrar staff auth e RBAC viewer/operator/admin; eliminar token da URL e header de ator não confiável.
3. Adicionar sessão web opaca e validação server-side de posse; vincular conta somente após autenticação.
4. Migrar somente tabelas/índices necessários com rollback; revisar pool/TLS e permissões dos leitores analíticos.
5. Implementar saneamento de logs, estados de consentimento e caminho auditável de exclusão.
6. Executar testes de autorização/IDOR/merge/produção sem banco; registrar evidências.

## Dados, permissões e observabilidade
Cada mudança de estado material deve ter ator, autorização, recibo persistido e evento de domínio. Fronteiras entre bancos/serviços usam outbox e reconciliação, não uma transação distribuída presumida. Métricas públicas de browser não comprovam dinheiro ou acesso. Não registrar segredos ou dados de terceiros em prompts/analytics.

## Testes e rollback
Executar os casos `C014-01` a `C014-05` e a regressão dos contratos afetados. Usar feature flag da capacidade e migrações compatíveis para rollback; nenhuma volta ao roteiro Pilates. Registrar em `verification.md`.

## Esforço de referência
3–4 dias de engenharia focada, estimativa de planejamento, não prazo garantido. Não inclui espera por autorização, fornecimento de mídia ou acesso externo. Reestimar ao fechar 013.

## Preparação técnica de implementação — 2026-09-28

[Recorte executável](execution.md) detalha fontes atuais, caminhos propostos, interfaces, dados, falhas, dependências e verificação por tarefa. Prevalece sobre a lista de caminhos candidatos do snapshot quando houver divergência registrada. Requisitos e critérios de aceite permanecem integrais.

Esta preparação não altera o estado de execução nem libera dependências. Somente 013 está ativa. Comandos existentes e limites estão em [IMPLEMENTATION_READINESS](../../docs/taliya-sdd/IMPLEMENTATION_READINESS.md).
