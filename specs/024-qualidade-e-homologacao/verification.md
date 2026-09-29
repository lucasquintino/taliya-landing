# 024 — Verificação e evidências

**Estado:** casos especificados; nenhum caso de aceitação foi executado nesta auditoria.

## C024-01 · R024-01
**Cenário:** Executar CI de unidade, contrato, integração e E2E; verificar que skips/mocks não são apresentados como integração real aprovada.

**Resultado exigido:** Build, lint, tipos e testes do código tocado passam no CI; testes antigos têm destino explícito: preservar/adaptar/arquivar.

**Evidência a produzir:** commit/ambiente, procedimento ou comando, dados sanitizados, resultado observado e responsável.

## C024-02 · R024-02
**Cenário:** Rodar conversas Luna/max com múltiplas mensagens, intenções, recusa, limitações e ataques; revisar rubric e repetir casos críticos.

**Resultado exigido:** Os 68 casos vigentes do plano e cenários reutilizáveis anteriores têm resultado; casos críticos repetidos não podem falhar; amostra de linguagem recebe revisão humana.

**Evidência a produzir:** commit/ambiente, procedimento ou comando, dados sanitizados, resultado observado e responsável.

## C024-03 · R024-03
**Cenário:** Executar mensal/anual com cartão/Pix Automático em sandbox após implementar a 015 e conferir conta, projeção comercial e analytics.

**Resultado exigido:** Mensal/anual × cartão/Pix Automático, retorno, falha, cancelamento e reembolso têm evidência sandbox; produção depende de gate próprio. Retorno de navegador não comprova pagamento.

**Evidência a produzir:** commit/ambiente, procedimento ou comando, dados sanitizados, resultado observado e responsável.

## C024-04 · R024-04
**Cenário:** Aplicar falhas de provedor, worker, banco e canal; realizar testes de autorização, acessibilidade e desempenho nas superfícies alteradas.

**Resultado exigido:** IDOR, injeção, URL arbitrária, repetição, takeover, desconexão, fila, cookies e restauração possuem evidências.

**Evidência a produzir:** commit/ambiente, procedimento ou comando, dados sanitizados, resultado observado e responsável.

## C024-05 · R024-05
**Cenário:** Revisar analyze/converge e o dossiê; inserir uma falha crítica controlada para comprovar que bloqueia o gate e não é removida por mudança silenciosa do teste.

**Resultado exigido:** Nenhum P0/P1 de lançamento aberto; metas não atingidas geram correção ou exceção explícita, não marcação verde por criar documentação.

**Evidência a produzir:** commit/ambiente, procedimento ou comando, dados sanitizados, resultado observado e responsável.

## Regressões adicionais da frente
- Suíte crítica inteira passa sem falsos sucessos nem teste mutado para concordar com implementação errada.
- Conversa com múltiplas mensagens/intenções é respondida sem diagnóstico obrigatório.
- Quatro combinações financeiras levam à conta correta e não duplicam cliente.
- Falha de um provedor não bloqueia outras superfícies e estado fica recuperável.
- Evidência permite a outra pessoa repetir os testes e diferenciar mock de resultado real.

Os IDs de caso são estáveis; o detalhamento técnico cresce com os contratos reais. Mock não comprova chamada externa, análise estática não comprova produção.

## Preparação técnica de implementação — 2026-09-28

[Recorte executável](execution.md) detalha fontes atuais, caminhos propostos, interfaces, dados, falhas, dependências e verificação por tarefa. Prevalece sobre a lista de caminhos candidatos do snapshot quando houver divergência registrada. Requisitos e critérios de aceite permanecem integrais.

Esta preparação não altera o estado de execução nem libera dependências. Somente 013 está ativa. Comandos existentes e limites estão em [IMPLEMENTATION_READINESS](../../docs/taliya-sdd/IMPLEMENTATION_READINESS.md).
