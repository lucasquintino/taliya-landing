# 019 — Verificação e evidências

**Estado:** casos especificados; nenhum caso de aceitação foi executado nesta auditoria.

## C019-01 · R019-01
**Cenário:** Publicar a biblioteca inicial com arquivos realmente entregues; conferir direitos, aprovação e classificação de prova social.

**Resultado exigido:** Catálogo entregue contém explicação geral, demonstrações prioritárias reais e UGCs aprovados; indisponíveis ficam ocultos.

**Evidência a produzir:** commit/ambiente, procedimento ou comando, dados sanitizados, resultado observado e responsável.

## C019-02 · R019-02
**Cenário:** Pedir várias demonstrações e tentar assinar sem assistir; validar máximo de um card por resposta e CTA independente.

**Resultado exigido:** Cards reutilizam o DS; o agente seleciona ID aprovado e o vídeo não cria barreira ao checkout.

**Evidência a produzir:** commit/ambiente, procedimento ou comando, dados sanitizados, resultado observado e responsável.

## C019-03 · R019-03
**Cenário:** Abrir página em rede móvel e sem autorização analítica; verificar carregamento sob demanda, áudio, dados enviados, foco e legendas.

**Resultado exigido:** Thumbnail/lazy load, reprodução voluntária, legendas e alternativa textual; embeds não burlam preferência de cookies.

**Evidência a produzir:** commit/ambiente, procedimento ou comando, dados sanitizados, resultado observado e responsável.

## C019-04 · R019-04
**Cenário:** Exibir, clicar, iniciar, avançar por seek e assistir intervalos reais; abrir link externo sem telemetria; conferir marcos sem falsa conclusão.

**Resultado exigido:** video_completed exige observação verificável do player; link externo sem telemetria não registra conclusão.

**Evidência a produzir:** commit/ambiente, procedimento ou comando, dados sanitizados, resultado observado e responsável.

## C019-05 · R019-05
**Cenário:** Retirar e substituir material publicado; conferir invalidação na landing e no chat e execução do procedimento por responsável.

**Resultado exigido:** Autor de conteúdo edita catálogo versionado com revisão; publicação/retirada é auditável; não há CMS/editor novo obrigatório.

**Evidência a produzir:** commit/ambiente, procedimento ou comando, dados sanitizados, resultado observado e responsável.

## Regressões adicionais da frente
- Material selecionado existe e sua prova social corresponde à classificação.
- Avançar o vídeo até o final não equivale a assistir 90% do conteúdo.
- Abrir link externo não dispara video_started/completed sem evidência.
- Vídeo não carrega bytes pesados nem reproduz som antes da ação permitida.
- Material retirado some do chat e da página sem deploy improvisado ou URL fabricada.

Os IDs de caso são estáveis; o detalhamento técnico cresce com os contratos reais. Mock não comprova chamada externa, análise estática não comprova produção.

## Preparação técnica de implementação — 2026-09-28

[Recorte executável](execution.md) detalha fontes atuais, caminhos propostos, interfaces, dados, falhas, dependências e verificação por tarefa. Prevalece sobre a lista de caminhos candidatos do snapshot quando houver divergência registrada. Requisitos e critérios de aceite permanecem integrais.

Esta preparação não altera o estado de execução nem libera dependências. Somente 013 está ativa. Comandos existentes e limites estão em [IMPLEMENTATION_READINESS](../../docs/taliya-sdd/IMPLEMENTATION_READINESS.md).
