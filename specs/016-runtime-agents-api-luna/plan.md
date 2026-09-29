# 016 — Runtime Agents API com Luna Max

**Status:** proposta de execução; implementação não iniciada nesta auditoria.
**Responsável:** Backend/IA.
**Dependências:** 014, 015.

## Abordagem técnica
Trocar o núcleo comercial antigo por execução gerenciada com um agente único e continuidade confiável.

A abordagem de domínio e as interfaces propostas estão em `../../docs/taliya-sdd/03_ARQUITETURA_E_CONTRATOS.md`. A implementação deve referenciar as interfaces reais descobertas na 013; os caminhos abaixo pertencem ao ZIP inspecionado e são candidatos de integração, não prova da árvore atual.

## Pontos de integração observados
- `lib/landing/ai-attendant/runtime-client.ts`
- `services/taliya-agent-runtime/app/main.py`
- `services/taliya-agent-runtime/app/core/taliya_commercial_sdk/action_agents.py`
- `services/taliya-agent-runtime/pyproject.toml`

## Ordem de execução
1. Criar adaptador v2 por trás da fronteira comercial atual, preservando linguagem e transporte úteis.
2. Homologar SDK/REST e payload na conta com ferramentas somente de leitura e custo limitado aprovado.
3. Implementar registry de versões e binding das sessões; desenhar migração de sessões abertas.
4. Acoplar fila/worker existente, inbox/outbox, lease, retry e dead-letter; não usar after() como garantia de durabilidade.
5. Consumir ações e eventos documentados, persistir resultados e reconstruir estado após desconexão.
6. Medir Luna/max, limites operacionais e fallback estático; registrar teste real e não somente JSON válido.

## Dados, permissões e observabilidade
Cada mudança de estado material deve ter ator, autorização, recibo persistido e evento de domínio. Fronteiras entre bancos/serviços usam outbox e reconciliação, não uma transação distribuída presumida. Métricas públicas de browser não comprovam dinheiro ou acesso. Não registrar segredos ou dados de terceiros em prompts/analytics.

## Testes e rollback
Executar os casos `C016-01` a `C016-05` e a regressão dos contratos afetados. Usar feature flag da capacidade e migrações compatíveis para rollback; nenhuma volta ao roteiro Pilates. Registrar em `verification.md`.

## Esforço de referência
3–5 dias de engenharia focada, estimativa de planejamento, não prazo garantido. Não inclui espera por autorização, fornecimento de mídia ou acesso externo. Reestimar ao fechar 013.

## Preparação técnica de implementação — 2026-09-28

[Recorte executável](execution.md) detalha fontes atuais, caminhos propostos, interfaces, dados, falhas, dependências e verificação por tarefa. Prevalece sobre a lista de caminhos candidatos do snapshot quando houver divergência registrada. Requisitos e critérios de aceite permanecem integrais.

Esta preparação não altera o estado de execução nem libera dependências. Somente 013 está ativa. Comandos existentes e limites estão em [IMPLEMENTATION_READINESS](../../docs/taliya-sdd/IMPLEMENTATION_READINESS.md).
