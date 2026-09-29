# 018 — Landing, widget e integração à assinatura

**Status:** proposta de execução; implementação não iniciada nesta auditoria.
**Responsável:** Frontend + design/QA.
**Dependências:** 015, 017.

## Abordagem técnica
Permitir contratar diretamente ou receber ajuda sem mudar a identidade visual aprovada.

A abordagem de domínio e as interfaces propostas estão em `../../docs/taliya-sdd/03_ARQUITETURA_E_CONTRATOS.md`. A implementação deve referenciar as interfaces reais descobertas na 013; os caminhos abaixo pertencem ao ZIP inspecionado e são candidatos de integração, não prova da árvore atual.

## Pontos de integração observados
- `components/landing/NicheLandingPage.tsx`
- `components/landing/shared/FloatingAiAttendant.tsx`
- `data/landing/niches/pilates.ts`
- `app/page.tsx`
- `app/robots.ts`
- `app/sitemap.ts`
- `next.config.ts`

## Ordem de execução
1. Mapear cada CTA atual e destino existente; alterar somente handlers e conteúdo necessário ao contrato.
2. Atualizar widget para nova resposta, cards e estado assíncrono com IDs estáveis.
3. Implementar retomada/autenticação sem confiar em sessionId do navegador; preservar conversa autorizada.
4. Fazer baseline visual e corrigir foco/teclado/safe-area/scroll/tamanhos/contraste no recorte alterado.
5. Revisar FAQ, oferta, metadata, redirects e indexação com a mesma fonte de produto.
6. Executar regressão de contratação direta e assistida em mobile/desktop e registrar capturas.

## Dados, permissões e observabilidade
Cada mudança de estado material deve ter ator, autorização, recibo persistido e evento de domínio. Fronteiras entre bancos/serviços usam outbox e reconciliação, não uma transação distribuída presumida. Métricas públicas de browser não comprovam dinheiro ou acesso. Não registrar segredos ou dados de terceiros em prompts/analytics.

## Testes e rollback
Executar os casos `C018-01` a `C018-05` e a regressão dos contratos afetados. Usar feature flag da capacidade e migrações compatíveis para rollback; nenhuma volta ao roteiro Pilates. Registrar em `verification.md`.

## Esforço de referência
2–4 dias de engenharia focada, estimativa de planejamento, não prazo garantido. Não inclui espera por autorização, fornecimento de mídia ou acesso externo. Reestimar ao fechar 013.

## Preparação técnica de implementação — 2026-09-28

[Recorte executável](execution.md) detalha fontes atuais, caminhos propostos, interfaces, dados, falhas, dependências e verificação por tarefa. Prevalece sobre a lista de caminhos candidatos do snapshot quando houver divergência registrada. Requisitos e critérios de aceite permanecem integrais.

Esta preparação não altera o estado de execução nem libera dependências. Somente 013 está ativa. Comandos existentes e limites estão em [IMPLEMENTATION_READINESS](../../docs/taliya-sdd/IMPLEMENTATION_READINESS.md).
