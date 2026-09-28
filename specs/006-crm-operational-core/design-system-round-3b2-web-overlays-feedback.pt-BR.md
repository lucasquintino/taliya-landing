# Design System Web - Rodada 3B.2 - Overlays E Feedback

> Status: biblioteca visual v0.1 aprovada. Esta rodada documenta overlays, feedback e estados de resposta do sistema web.

## Objetivo

Definir componentes de feedback e sobreposicao do Taliya CRM web, mantendo o DNA visual das Rodadas 3A e 3B.1.

Esta rodada cobre:

- modal;
- drawer lateral;
- popover;
- tooltip;
- toast;
- alerta inline;
- confirmacao;
- empty state;
- loading/skeleton;
- error state.

## Decisao

A imagem da Rodada 3B.2 fica aprovada como v0.1.

Ela acertou:

- manteve o escopo restrito a overlays e feedback;
- usou inputs e botoes de forma coerente com a 3B.1;
- cobriu estados de sucesso, alerta, erro, informacao, loading e vazio;
- trouxe drawer, modal e popover sem mudar o estilo;
- manteve a linguagem premium e macia.

## Ressalvas

- A prancha continua um pouco branca demais quando comparada a referencia original.
- O drawer ficou visualmente estreito, bom para componente, mas deve ser testado em tela real.
- Estados destrutivos em vermelho devem ser usados com moderacao.
- Tooltips pretos estao bons, mas textos longos precisam quebrar sem perder leitura.
- Empty states nao devem virar ilustracoes grandes em paginas reais.
- Skeletons devem ser sutis e nao dominar a tela.

## Regras De Uso

- Modal deve ser usado para confirmacao, edicao curta ou acao sensivel.
- Drawer deve ser usado para edicao contextual sem sair da pagina.
- Popover deve conter opcoes curtas ou mini formularios.
- Toast deve ser temporario e nao substituir auditoria ou historico.
- Alerta inline deve ficar proximo ao problema.
- Empty state deve sempre oferecer proximo passo quando houver acao possivel.
- Error state deve explicar recuperacao: tentar novamente, reconectar ou abrir suporte.

## Nao Fazer

- Nao transformar modal em pagina completa.
- Nao usar drawer como tela principal.
- Nao empilhar muitos overlays.
- Nao usar vermelho para estados que nao sao erro, risco ou destruicao.
- Nao criar feedback que bloqueia operacao manual sem necessidade.

