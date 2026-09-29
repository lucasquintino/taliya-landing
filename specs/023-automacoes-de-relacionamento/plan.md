# 023 — Automações enxutas de relacionamento

**Status:** proposta de execução; implementação não iniciada nesta auditoria.
**Responsável:** Operação + backend/analytics.
**Dependências:** 017, 020, 021, 022.

## Abordagem técnica
Recuperar jornadas elegíveis com regras previsíveis e um único responsável por cada mensagem.

A abordagem de domínio e as interfaces propostas estão em `../../docs/taliya-sdd/03_ARQUITETURA_E_CONTRATOS.md`. A implementação deve referenciar as interfaces reais descobertas na 013; os caminhos abaixo pertencem ao ZIP inspecionado e são candidatos de integração, não prova da árvore atual.

## Pontos de integração observados
- `lib/landing/ai-attendant/n8n.ts`
- `serviços existentes de notificações e billing (mapear na 013)`

## Ordem de execução
1. Inventariar todas as notificações atuais e designar um emissor por categoria.
2. Configurar Workflows quando disponível ou reutilizar a automação já adotada sem criar motor paralelo.
3. Criar webhook de solicitação autenticado e revalidação server-side antes da entrega pelo provedor existente.
4. Criar templates curtos com link seguro, cancelamento de contato e nenhum desconto inventado.
5. Testar supressão em corrida com pagamento/opt-out/pausa humana e limites do provedor.
6. Liberar de forma controlada somente após aprovação de mensagem, canal e volume; documentar kill switch.

## Dados, permissões e observabilidade
Cada mudança de estado material deve ter ator, autorização, recibo persistido e evento de domínio. Fronteiras entre bancos/serviços usam outbox e reconciliação, não uma transação distribuída presumida. Métricas públicas de browser não comprovam dinheiro ou acesso. Não registrar segredos ou dados de terceiros em prompts/analytics.

## Testes e rollback
Executar os casos `C023-01` a `C023-05` e a regressão dos contratos afetados. Usar feature flag da capacidade e migrações compatíveis para rollback; nenhuma volta ao roteiro Pilates. Registrar em `verification.md`.

## Esforço de referência
1–2 dias de engenharia focada, estimativa de planejamento, não prazo garantido. Não inclui espera por autorização, fornecimento de mídia ou acesso externo. Reestimar ao fechar 013.

## Preparação técnica de implementação — 2026-09-28

[Recorte executável](execution.md) detalha fontes atuais, caminhos propostos, interfaces, dados, falhas, dependências e verificação por tarefa. Prevalece sobre a lista de caminhos candidatos do snapshot quando houver divergência registrada. Requisitos e critérios de aceite permanecem integrais.

Esta preparação não altera o estado de execução nem libera dependências. Somente 013 está ativa. Comandos existentes e limites estão em [IMPLEMENTATION_READINESS](../../docs/taliya-sdd/IMPLEMENTATION_READINESS.md).
