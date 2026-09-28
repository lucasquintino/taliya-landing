# Design System Web - Rodada 3B.1 - Inputs, Formularios E Filtros

> Status: biblioteca visual v0.1 aprovada. Esta rodada documenta os componentes de entrada de dados, formularios e filtros que faltavam no sistema web.

## Objetivo

Definir os componentes basicos de entrada e filtragem do Taliya CRM web, mantendo a linguagem visual aprovada nas Rodadas 1, 2B e 3A.

Esta rodada complementa a 3A. Ela nao cria componentes de overlay, visualizacoes operacionais, comunicacao, agentes, billing, cotas ou governanca.

## Entradas Usadas

1. Rodada 3A: componentes web presentes na referencia.
2. Tela Taliya 2A.2: identidade aplicada em tela real.
3. Referencia original: atmosfera, cinza frio, suavidade, densidade e baixo contraste.
4. Imagem da Rodada 3B.1: prancha de inputs, formularios e filtros.

## Decisao Da Rodada 3B.1

A imagem da Rodada 3B.1 fica aprovada como biblioteca v0.1 de:

- input de texto;
- textarea;
- select/dropdown;
- checkbox;
- toggle;
- controle segmentado;
- seletor compacto de data e hora;
- chips e filtros;
- busca avancada;
- formulario compacto.

Ela acertou:

- ficou dentro do escopo;
- nao misturou modal, chat, agente, billing, cotas ou tabela completa;
- cobriu estados suficientes para design e implementacao futura;
- manteve relacao visual com a 3A e a 2A.2;
- criou um formulario compacto util;
- criou uma busca avancada compativel com CRM.

## Ressalvas Aprovadas

A prancha e aprovada, mas com observacoes obrigatorias para uso em telas reais:

- ficou um pouco com cara de UI kit, aceitavel por ser prancha;
- ficou branca demais quando comparada a referencia original;
- o foco preto em input ficou forte demais para algumas telas;
- o select aberto ficou um pouco generico;
- o vermelho de erro ficou funcional, mas pode estar saturado;
- alguns labels e textos ficaram pequenos;
- em paginas reais, os componentes devem herdar fundo cinza frio e superficies translucidas.

Regra principal:

```text
3B.1 define estados e anatomia de inputs, formularios e filtros.
3B.1 nao deve ser usada sozinha como referencia de atmosfera.
```

Para atmosfera, usar:

1. Referencia original;
2. Tela Taliya 2A.2;
3. Rodada 3A;
4. Rodada 3B.1 para anatomia dos campos.

## Componentes Aprovados

### 1. Input De Texto

Estados:

| Estado | Regra visual |
| --- | --- |
| Default | campo claro, borda sutil, placeholder discreto. |
| Focus | borda mais forte; em tela real pode ser preto suavizado ou azul sutil. |
| Preenchido | texto principal, icone opcional a direita. |
| Erro | borda vermelha, icone de alerta, mensagem curta. |
| Disabled | fundo claro opaco, texto reduzido, sem sombra. |

Regras:

- usar labels externos quando houver risco de ambiguidade;
- evitar placeholder como unica instrucao;
- erro deve explicar acao corretiva;
- foco nao deve dominar a tela.

### 2. Textarea

Estados:

- default;
- focus;
- preenchido;
- erro.

Regras:

- usar para mensagem, observacao, descricao e resumo;
- manter altura compacta por padrao;
- usar resize discreto quando existir;
- erro deve ficar logo abaixo do campo.

### 3. Select / Dropdown

Estados:

- fechado;
- aberto;
- item selecionado;
- item disabled.

Regras:

- menu deve manter radius e sombra suave;
- item selecionado pode usar azul suave;
- item disabled deve ter baixa opacidade;
- evitar lista alta demais em paineis compactos.

### 4. Checkbox

Estados:

- unchecked;
- checked;
- disabled.

Regras:

- usar para selecao multipla e confirmacoes simples;
- label deve ser clicavel;
- disabled precisa continuar legivel;
- nao usar checkbox para acao imediata sensivel.

### 5. Toggle

Estados:

- off;
- on;
- disabled.

Regras:

- usar para lig/deslig de configuracao;
- on pode usar preto no design atual;
- em telas de configuracao sensivel, acompanhar com texto claro;
- evitar toggle para escolha entre mais de duas opcoes.

### 6. Controle Segmentado

Uso:

- status rapido;
- filtros de visao;
- modo de lista;
- escolhas mutuamente exclusivas.

Estados:

- opcao default;
- opcao ativa;
- tres opcoes.

Regras:

- ativo em pill preto;
- grupo em superficie clara;
- labels curtos;
- nao usar para muitas opcoes.

### 7. Seletor Compacto De Data E Hora

Variacoes:

- campo de data;
- campo de horario;
- selecionado.

Regras:

- usar icones pequenos;
- formato deve ser localizavel em PT-BR;
- evitar calendario completo nesta rodada;
- calendario completo entra na 3B.3.

### 8. Chips / Filtros

Variacoes:

- chip padrao;
- chip ativo;
- chip removivel;
- chip com contador.

Regras:

- chips devem ser compactos;
- ativo pode usar azul suave;
- removivel usa icone pequeno;
- contador deve ser badge pequeno, nao pill grande.

### 9. Busca Avancada

Partes:

- campo de busca;
- icone de busca;
- filtros aplicados;
- botao circular de filtro/acao;
- contador de resultados.

Regras:

- busca deve ficar horizontal e densa;
- filtros aplicados aparecem como chips;
- contador deve ser discreto;
- nao transformar em painel complexo nesta rodada.

### 10. Formulario Compacto

Partes:

- label;
- input;
- select;
- textarea curta;
- toggle;
- acoes no rodape.

Regras:

- usar layout horizontal quando couber;
- manter labels curtos;
- acoes principais no rodape ou fim do grupo;
- botao principal pode ser pill preto;
- botao secundario deve ser claro e sutil.

## Regras De Uso Em Telas Reais

Quando usar componentes da 3B.1:

- aplicar sobre fundo cinza frio, nao branco puro;
- usar superficies translucidas quando possivel;
- reduzir contraste do foco se muitos campos aparecerem juntos;
- usar vermelho com moderacao;
- manter labels legiveis;
- preservar densidade;
- nao abrir dropdowns ou menus com visual de sistema generico.

## Nao Fazer

Nao usar a 3B.1 para:

- criar modal;
- criar drawer;
- criar chat;
- criar calendario completo;
- criar kanban;
- criar tabela completa;
- criar agente/copiloto;
- criar cotas;
- criar billing;
- criar permissoes;
- criar tela final de produto;
- justificar fundo branco dominante.

## Relacao Com As Proximas Rodadas

A partir da 3B.2, a imagem aprovada da 3B.1 deve entrar como anexo adicional.

Motivo:

- overlays usam inputs;
- tabelas usam filtros;
- calendario usa campos de data;
- chat e agente usam textarea/campo de mensagem;
- billing e configuracoes usam formulario compacto, toggle e select.

Ordem recomendada:

1. 3B.2: overlays e feedback;
2. 3B.3: visualizacoes operacionais;
3. 3B.4: comunicacao e agentes;
4. 3B.5: sistema, plano e governanca.

