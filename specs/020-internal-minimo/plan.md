# 020 — Taliya Internal mínimo e operação humana

**Status:** proposta de execução; implementação não iniciada nesta auditoria.
**Responsável:** Frontend/backend + operação.
**Dependências:** 014, 017.

## Abordagem técnica
Entregar duas áreas operacionais, sem duplicar CRM analítico ou financeiro.

A abordagem de domínio e as interfaces propostas estão em `../../docs/taliya-sdd/03_ARQUITETURA_E_CONTRATOS.md`. A implementação deve referenciar as interfaces reais descobertas na 013; os caminhos abaixo pertencem ao ZIP inspecionado e são candidatos de integração, não prova da árvore atual.

## Pontos de integração observados
- `components/internal/SalesInboxClient.tsx`
- `app/internal/sales-inbox/page.tsx`
- `app/api/internal/sales-inbox/leads/[leadId]/actions/route.ts`
- `app/api/internal/sales-inbox/[leadId]/handoff/route.ts`
- `next.config.ts`

## Ordem de execução
1. Resolver dono/domínio do Internal antes de escolher onde alterar o código.
2. Reaproveitar fila/ficha atuais retirando campos Pilates/diagnóstico e controles financeiros fictícios.
3. Implementar estados de atendimento com versão/lock; validar take_over/resume_ai no worker e na outbox.
4. Implementar entrega humana web se faltar; no WhatsApp revisar timestamp do último inbound e regras do provedor.
5. Adicionar pesquisa, filtros, notas operacionais mínimas e atalhos para serviços oficiais sem novos dashboards.
6. Treinar operação com cenário de erro e garantir auditoria de identidade, envio e pausa.

## Dados, permissões e observabilidade
Cada mudança de estado material deve ter ator, autorização, recibo persistido e evento de domínio. Fronteiras entre bancos/serviços usam outbox e reconciliação, não uma transação distribuída presumida. Métricas públicas de browser não comprovam dinheiro ou acesso. Não registrar segredos ou dados de terceiros em prompts/analytics.

## Testes e rollback
Executar os casos `C020-01` a `C020-05` e a regressão dos contratos afetados. Usar feature flag da capacidade e migrações compatíveis para rollback; nenhuma volta ao roteiro Pilates. Registrar em `verification.md`.

## Esforço de referência
3–4 dias de engenharia focada, estimativa de planejamento, não prazo garantido. Não inclui espera por autorização, fornecimento de mídia ou acesso externo. Reestimar ao fechar 013.

## Preparação técnica de implementação — 2026-09-28

[Recorte executável](execution.md) detalha fontes atuais, caminhos propostos, interfaces, dados, falhas, dependências e verificação por tarefa. Prevalece sobre a lista de caminhos candidatos do snapshot quando houver divergência registrada. Requisitos e critérios de aceite permanecem integrais.

Esta preparação não altera o estado de execução nem libera dependências. Somente 013 está ativa. Comandos existentes e limites estão em [IMPLEMENTATION_READINESS](../../docs/taliya-sdd/IMPLEMENTATION_READINESS.md).
