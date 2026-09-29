# 017 — Cinco ferramentas e ciclo de leads/clientes

**Status:** proposta de execução; implementação não iniciada nesta auditoria.
**Responsável:** Backend comercial + app/billing.
**Dependências:** 014, 015, 016.

## Abordagem técnica
Conectar conversa, cadastro e assinatura com uma autoridade por operação.

A abordagem de domínio e as interfaces propostas estão em `../../docs/taliya-sdd/03_ARQUITETURA_E_CONTRATOS.md`. A implementação deve referenciar as interfaces reais descobertas na 013; os caminhos abaixo pertencem ao ZIP inspecionado e são candidatos de integração, não prova da árvore atual.

## Pontos de integração observados
- `app/api/landing/ai-attendant/route.ts`
- `lib/landing/ai-attendant/conversion.ts`
- `lib/landing/ai-attendant/leads.ts`
- `lib/landing/ai-attendant/sales-inbox-store.ts`
- `app/api/landing/ai-attendant/whatsapp/route.ts`

## Ordem de execução
1. Implementar handlers restritos com schemas, contexto autenticado, versões e recibos persistidos.
2. Reutilizar contato/lead store com patch allowlist e prova por message_id original.
3. Assinar eventos de domínio do app/billing ou consultar projeção via interfaces existentes; definir idempotência e reconciliação.
4. Desativar conversão antiga baseada no texto no caminho v2; mapear compatibilidade para UI sem preservar regras de diagnóstico.
5. Conectar navegação à contratação e cliente ativo à gestão/app, sem iniciar pagamento dentro da ferramenta.
6. Testar compra sem IA, criação assistida, renovação, falha e migração de contatos históricos.

## Dados, permissões e observabilidade
Cada mudança de estado material deve ter ator, autorização, recibo persistido e evento de domínio. Fronteiras entre bancos/serviços usam outbox e reconciliação, não uma transação distribuída presumida. Métricas públicas de browser não comprovam dinheiro ou acesso. Não registrar segredos ou dados de terceiros em prompts/analytics.

## Testes e rollback
Executar os casos `C017-01` a `C017-05` e a regressão dos contratos afetados. Usar feature flag da capacidade e migrações compatíveis para rollback; nenhuma volta ao roteiro Pilates. Registrar em `verification.md`.

## Esforço de referência
3–5 dias de engenharia focada, estimativa de planejamento, não prazo garantido. Não inclui espera por autorização, fornecimento de mídia ou acesso externo. Reestimar ao fechar 013.

## Preparação técnica de implementação — 2026-09-28

[Recorte executável](execution.md) detalha fontes atuais, caminhos propostos, interfaces, dados, falhas, dependências e verificação por tarefa. Prevalece sobre a lista de caminhos candidatos do snapshot quando houver divergência registrada. Requisitos e critérios de aceite permanecem integrais.

Esta preparação não altera o estado de execução nem libera dependências. Somente 013 está ativa. Comandos existentes e limites estão em [IMPLEMENTATION_READINESS](../../docs/taliya-sdd/IMPLEMENTATION_READINESS.md).
