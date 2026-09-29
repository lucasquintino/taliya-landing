# 022 — Verificação e evidências

**Estado:** casos especificados; nenhum caso de aceitação foi executado nesta auditoria.

## C022-01 · R022-01
**Cenário:** Carregar dataset de homologação conhecido e revisar as seis áreas de dashboard, filtros, fontes e períodos.

**Resultado exigido:** Cada painel tem perguntas, denominadores, filtros, unidade, janela, timezone e fonte; negócios e usuários não se confundem.

**Evidência a produzir:** commit/ambiente, procedimento ou comando, dados sanitizados, resultado observado e responsável.

## C022-02 · R022-02
**Cenário:** Comparar compradores diretos, compradores com chat e compradores com vídeo; todos devem integrar o funil principal sem etapa opcional obrigatória.

**Resultado exigido:** Compra direta permanece no denominador correto; agent_assisted indica associação, não ganho causal comprovado.

**Evidência a produzir:** commit/ambiente, procedimento ou comando, dados sanitizados, resultado observado e responsável.

## C022-03 · R022-03
**Cenário:** Conferir fixture de pagamentos, anual, renovação, inadimplência, cancelamento e estorno; revisar denominadores, coortes maduras e atribuição sem causalidade.

**Resultado exigido:** Anual é normalizado; cancelamento pedido difere do acesso encerrado; reembolso pedido/concluído é separado; coortes imaturas não recebem taxa inventada.

**Evidência a produzir:** commit/ambiente, procedimento ou comando, dados sanitizados, resultado observado e responsável.

## C022-04 · R022-04
**Cenário:** Projetar consumo observado por módulo, aproximar-se dos limites e simular teto; conferir alertas e que billing não depende do analytics.

**Resultado exigido:** Estimativa usa volume real e addons; teto US$50 é proposta sujeita à aprovação; Group Analytics/replay/Workflows não são ativados automaticamente.

**Evidência a produzir:** commit/ambiente, procedimento ou comando, dados sanitizados, resultado observado e responsável.

## C022-05 · R022-05
**Cenário:** Contar negócios pagantes/ativados com dois usuários por negócio, sem habilitar Group Analytics automaticamente; avaliar addon em configuração separada aprovada.

**Resultado exigido:** business_id existe na origem; consultas/exports canônicos fornecem agregação por negócio; Group Analytics só entra após teste de necessidade/custo.

**Evidência a produzir:** commit/ambiente, procedimento ou comando, dados sanitizados, resultado observado e responsável.

## Regressões adicionais da frente
- 100 pagamentos de teste canônicos geram exatamente valores/contas esperados no dataset de homologação.
- Renovação não aparece como novo cliente e anual não infla MRR por 12.
- Coorte sem janela madura mostra indisponibilidade e tamanho, não zero enganoso.
- Primeiro/último toque e agent_assisted usam a janela documentada sem causalidade presumida.
- Grupo pago e projeção de gastos só são ativados com aprovação; atingir teto não altera billing.

Os IDs de caso são estáveis; o detalhamento técnico cresce com os contratos reais. Mock não comprova chamada externa, análise estática não comprova produção.

## Preparação técnica de implementação — 2026-09-28

[Recorte executável](execution.md) detalha fontes atuais, caminhos propostos, interfaces, dados, falhas, dependências e verificação por tarefa. Prevalece sobre a lista de caminhos candidatos do snapshot quando houver divergência registrada. Requisitos e critérios de aceite permanecem integrais.

Esta preparação não altera o estado de execução nem libera dependências. Somente 013 está ativa. Comandos existentes e limites estão em [IMPLEMENTATION_READINESS](../../docs/taliya-sdd/IMPLEMENTATION_READINESS.md).
