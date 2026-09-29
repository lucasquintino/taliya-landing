# 019 — Vídeos, demonstrações e UGCs na experiência

**Status:** proposta de execução; implementação não iniciada nesta auditoria.
**Responsável:** Conteúdo + frontend.
**Dependências:** 015.

## Abordagem técnica
Integrar a biblioteca aprovada à landing e ao agente com reprodução e medição coerentes.

A abordagem de domínio e as interfaces propostas estão em `../../docs/taliya-sdd/03_ARQUITETURA_E_CONTRATOS.md`. A implementação deve referenciar as interfaces reais descobertas na 013; os caminhos abaixo pertencem ao ZIP inspecionado e são candidatos de integração, não prova da árvore atual.

## Pontos de integração observados
- `components/landing/sections/`
- `components/landing/shared/`
- `data/landing/`

## Ordem de execução
1. Inventariar arquivos de mídia entregues com direitos, classificação de UGC e relações com capacidades.
2. Preparar thumbnails, legendas/transcrições revisadas e tamanhos adequados usando hospedagem existente.
3. Construir um card/player reutilizável para landing e chat sem tocar na composição global.
4. Implementar medição de intervalos assistidos quando suportado e poucos marcos, sem evento por segundo.
5. Validar fallback sem vídeo, link quebrado, arquivo retirado e teclado/foco.
6. Registrar biblioteca de lançamento e procedimento de manutenção com responsável.

## Dados, permissões e observabilidade
Cada mudança de estado material deve ter ator, autorização, recibo persistido e evento de domínio. Fronteiras entre bancos/serviços usam outbox e reconciliação, não uma transação distribuída presumida. Métricas públicas de browser não comprovam dinheiro ou acesso. Não registrar segredos ou dados de terceiros em prompts/analytics.

## Testes e rollback
Executar os casos `C019-01` a `C019-05` e a regressão dos contratos afetados. Usar feature flag da capacidade e migrações compatíveis para rollback; nenhuma volta ao roteiro Pilates. Registrar em `verification.md`.

## Esforço de referência
1–3 dias de engenharia focada, estimativa de planejamento, não prazo garantido. Não inclui espera por autorização, fornecimento de mídia ou acesso externo. Reestimar ao fechar 013.

## Preparação técnica de implementação — 2026-09-28

[Recorte executável](execution.md) detalha fontes atuais, caminhos propostos, interfaces, dados, falhas, dependências e verificação por tarefa. Prevalece sobre a lista de caminhos candidatos do snapshot quando houver divergência registrada. Requisitos e critérios de aceite permanecem integrais.

Esta preparação não altera o estado de execução nem libera dependências. Somente 013 está ativa. Comandos existentes e limites estão em [IMPLEMENTATION_READINESS](../../docs/taliya-sdd/IMPLEMENTATION_READINESS.md).
