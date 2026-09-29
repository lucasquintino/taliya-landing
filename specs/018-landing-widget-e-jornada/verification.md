# 018 — Verificação e evidências

**Estado:** casos especificados; nenhum caso de aceitação foi executado nesta auditoria.

## C018-01 · R018-01
**Cenário:** Desligar o serviço de IA e acionar CTA principal; comparar com CTA secundário de dúvidas e preservar mensal/anual na autenticação.

**Resultado exigido:** Começar agora abre o fluxo existente; tirar dúvidas abre chat. Escolha mensal/anual e contexto permitidos são preservados.

**Evidência a produzir:** commit/ambiente, procedimento ou comando, dados sanitizados, resultado observado e responsável.

## C018-02 · R018-02
**Cenário:** Comparar capturas mobile/desktop com baseline de tokens, proporções e componentes; verificar ausência de redesign fora do recorte.

**Resultado exigido:** Diferenças desktop/mobile são aprovadas; nenhum redesign geral, substituição de carrosséis/tabs ou reconstrução do app.

**Evidência a produzir:** commit/ambiente, procedimento ou comando, dados sanitizados, resultado observado e responsável.

## C018-03 · R018-03
**Cenário:** Percorrer abertura, processamento, resposta, erro, expiração, retomada e pausa humana; recarregar página sem duplicar mensagens.

**Resultado exigido:** Fechado/aberto/vazio/enviando/esperando/erro/offline/reconectando/humano possuem comportamento testado, sem spinner infinito.

**Evidência a produzir:** commit/ambiente, procedimento ou comando, dados sanitizados, resultado observado e responsável.

## C018-04 · R018-04
**Cenário:** Usar teclado/leitor de tela, adulterar referência de navegação e tentar retomar outra conversa; conferir foco, autorização e redirecionamento permitido.

**Resultado exigido:** URLs vêm do backend; teclado, foco, leitura, toque e retorno após login funcionam; tokens não entram em analytics/referrer.

**Evidência a produzir:** commit/ambiente, procedimento ou comando, dados sanitizados, resultado observado e responsável.

## C018-05 · R018-05
**Cenário:** Revisar FAQ, preço, garantia, metadata, redirects e conteúdo indexável contra a fonte comercial atual.

**Resultado exigido:** Metadados/structured data e rotas não anunciam legado; privadas ficam protegidas e noindex; não há promessa de indexação garantida.

**Evidência a produzir:** commit/ambiente, procedimento ou comando, dados sanitizados, resultado observado e responsável.

## Regressões adicionais da frente
- Contratação direta funciona com serviço de IA desligado.
- Trocar mensal/anual e entrar na conta preserva a modalidade válida.
- Conversa reinicia ou retoma com clareza após expiração, sem mostrar dados de outro visitante.
- Falha recuperável não duplica mensagem nem cobra outra vez.
- Teclado, leitor de tela e viewport móvel operam chat, mídia e CTAs sem regressão.

Os IDs de caso são estáveis; o detalhamento técnico cresce com os contratos reais. Mock não comprova chamada externa, análise estática não comprova produção.

## Preparação técnica de implementação — 2026-09-28

[Recorte executável](execution.md) detalha fontes atuais, caminhos propostos, interfaces, dados, falhas, dependências e verificação por tarefa. Prevalece sobre a lista de caminhos candidatos do snapshot quando houver divergência registrada. Requisitos e critérios de aceite permanecem integrais.

Esta preparação não altera o estado de execução nem libera dependências. Somente 013 está ativa. Comandos existentes e limites estão em [IMPLEMENTATION_READINESS](../../docs/taliya-sdd/IMPLEMENTATION_READINESS.md).
