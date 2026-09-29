# 022 — Painéis SaaS, definições e limites de custo

**Status:** proposta de execução; implementação não iniciada nesta auditoria.
**Responsável:** Analytics + produto.
**Dependências:** 021.

## Abordagem técnica
Entregar seis painéis utilizáveis com definições explícitas, sem construir BI no Internal.

A abordagem de domínio e as interfaces propostas estão em `../../docs/taliya-sdd/03_ARQUITETURA_E_CONTRATOS.md`. A implementação deve referenciar as interfaces reais descobertas na 013; os caminhos abaixo pertencem ao ZIP inspecionado e são candidatos de integração, não prova da árvore atual.

## Pontos de integração observados
- `lib/landing/ai-attendant/funnel-events.ts`
- `docs/ (novos contratos de métricas e configurações exportadas)`

## Ordem de execução
1. Versionar dicionário de métricas, denominadores e fontes de receita antes dos gráficos.
2. Construir os seis dashboards no PostHog com filters padrão e links de investigação.
3. Preparar consultas/snapshots analíticos sanitizados; evitar sincronizar banco inteiro ou ativar CDC sem revisão.
4. Conferir resultados com fixture financeira e casos anual/renovação/estorno/inadimplência.
5. Configurar custo/uso e alertas 70/85/95% do teto aprovado por produto; registrar limite do plano/projetos.
6. Documentar guia de leitura dos painéis e auditoria semanal de dados, sem duplicar no Internal.

## Dados, permissões e observabilidade
Cada mudança de estado material deve ter ator, autorização, recibo persistido e evento de domínio. Fronteiras entre bancos/serviços usam outbox e reconciliação, não uma transação distribuída presumida. Métricas públicas de browser não comprovam dinheiro ou acesso. Não registrar segredos ou dados de terceiros em prompts/analytics.

## Testes e rollback
Executar os casos `C022-01` a `C022-05` e a regressão dos contratos afetados. Usar feature flag da capacidade e migrações compatíveis para rollback; nenhuma volta ao roteiro Pilates. Registrar em `verification.md`.

## Esforço de referência
2–3 dias de engenharia focada, estimativa de planejamento, não prazo garantido. Não inclui espera por autorização, fornecimento de mídia ou acesso externo. Reestimar ao fechar 013.

## Preparação técnica de implementação — 2026-09-28

[Recorte executável](execution.md) detalha fontes atuais, caminhos propostos, interfaces, dados, falhas, dependências e verificação por tarefa. Prevalece sobre a lista de caminhos candidatos do snapshot quando houver divergência registrada. Requisitos e critérios de aceite permanecem integrais.

Esta preparação não altera o estado de execução nem libera dependências. Somente 013 está ativa. Comandos existentes e limites estão em [IMPLEMENTATION_READINESS](../../docs/taliya-sdd/IMPLEMENTATION_READINESS.md).
