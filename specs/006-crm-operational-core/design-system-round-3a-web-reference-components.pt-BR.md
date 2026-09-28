# Design System Web - Rodada 3A - Componentes Web Presentes Na Referencia

> Status: biblioteca visual v0.1 aprovada. Esta rodada documenta os componentes que ja aparecem na referencia e na tela Taliya 2A.2.

## Objetivo

Catalogar os componentes web visiveis no App Shell Web aprovado, sem criar ainda os componentes que faltam para o CRM inteiro.

Esta rodada serve para:

- extrair os componentes existentes da tela base;
- padronizar estados visuais simples;
- preservar o DNA da referencia;
- orientar as proximas telas sem inventar um estilo novo.

Esta rodada nao e a fonte principal de atmosfera. A atmosfera continua sendo definida pela referencia original e pela tela Taliya 2A.2.

## Entradas Usadas

1. Referencia principal: Customer Journey CRM Dashboard.
2. Tela Taliya 2A.2: clone visual web base aprovado.
3. Rodada 1: DNA visual e tokens.
4. Rodada 1.1: especificacao precisa dos tokens.
5. Rodada 2B: contrato do App Shell Web.
6. Imagem da Rodada 3A: prancha de componentes presentes na referencia.

## Decisao Da Rodada 3A

A imagem da Rodada 3A fica aprovada como biblioteca v0.1 dos componentes presentes na referencia.

Ela acertou:

- botoes circulares;
- navegacao horizontal e nav pill;
- item de sidebar;
- avatares e badges;
- cards de fluxo;
- mini cards de status;
- painel grande/canvas;
- conectores;
- tabela leve;
- grafico semicircular;
- toolbar de painel;
- tokens principais no rodape.

Ressalva principal:

```text
3A define quais componentes existem e seus estados basicos.
3A nao deve ser usada sozinha como referencia de atmosfera.
```

Para atmosfera, densidade e suavidade, usar a ordem:

1. Referencia original: mood, cinza, densidade e suavidade.
2. Taliya 2A.2: identidade Taliya aplicada em tela real.
3. Rodada 3A: componentes isolados e variacoes basicas.

## Avaliacao Visual

### Pontos Fortes

- A prancha tem boa organizacao e leitura.
- Os componentes parecem derivados da tela aprovada.
- O sistema de botoes circulares ficou coerente.
- O nav pill preto preserva a linguagem da referencia.
- Avatares e badges continuam humanos e claros.
- Cards de fluxo cobrem as variacoes visiveis.
- O painel/canvas em miniatura ajuda a manter contexto.
- Tabela leve e status cards ficaram alinhados ao CRM.
- Tokens no rodape ajudam a evitar deriva visual.

### Ressalvas

- A prancha ficou mais branca do que a referencia original.
- Os componentes estao mais separados e catalogados, como e esperado em biblioteca.
- Os conectores ainda parecem um pouco tecnicos.
- Alguns cards ficaram nitidos e limpos demais.
- O contraste geral esta um pouco acima da base ref.

### Regra De Uso

Quando usar estes componentes em telas reais:

- voltar para o fundo cinza frio da referencia;
- manter baixo contraste;
- reduzir excesso de branco;
- compactar cards quando a tela parecer espacada;
- deixar conectores mais sutis;
- tratar os paineis inferiores como secundarios;
- evitar cara de UI kit.

## Componentes Aprovados

### 1. Botao Circular

Uso:

- acoes de topo;
- acoes de painel;
- calendario;
- busca;
- mensagem;
- notificacao;
- adicionar;
- exportar/compartilhar;
- configuracoes ou utilitarios.

Estados:

| Estado | Regra visual |
| --- | --- |
| Default | circulo claro, borda sutil, icone preto. |
| Hover/subtle | fundo levemente mais marcado, sombra suave. |
| Active/selected | fundo preto `#10141A`, icone branco. |
| Com alerta | badge vermelho pequeno no canto superior. |
| Disabled | opacidade baixa, sem sombra forte. |

Regras:

- manter formato circular;
- nao trocar por botao retangular quando houver icone claro;
- usar texto apenas quando a acao nao for autoexplicativa;
- manter badges pequenos.

### 2. Navegacao Horizontal / Nav Pill

Uso:

- topbar principal do CRM;
- grupos de navegacao no desktop.

Estados:

| Estado | Regra visual |
| --- | --- |
| Default | texto escuro, sem fundo. |
| Hover | fundo claro e arredondado, baixo contraste. |
| Ativo | pill preto, texto branco. |

Navegacao base:

- Relacionamento;
- Oportunidades;
- Leads;
- Agenda;
- Casos;
- Relatorios;
- Propostas.

Regras:

- manter item ativo claro;
- nao usar underline;
- nao usar abas quadradas;
- preservar respiro horizontal.

### 3. Item De Sidebar

Uso:

- navegacao primaria compacta por icone;
- atalhos utilitarios;
- status/alertas.

Estados:

| Estado | Regra visual |
| --- | --- |
| Default | botao circular branco/translucido. |
| Active | botao preto com icone branco. |
| Com alerta | badge vermelho pequeno. |
| Utilitario inferior | mesma linguagem, posicionado perto do rodape. |

Regras:

- nao exibir label persistente;
- manter coluna compacta;
- agrupar acoes por espacamento;
- usar tooltip em implementacao real.

### 4. Avatar E Badges

Uso:

- pessoas envolvidas;
- responsaveis;
- professores;
- atendentes;
- agentes representados por identidade visual futura;
- contadores de pendencias.

Variacoes:

- avatar simples;
- avatar com badge azul;
- avatar com badge vermelho;
- grupo de avatares;
- botao de adicionar avatar.

Regras:

- badges devem sobrepor o canto inferior direito;
- azul indica progresso/neutro/ok;
- vermelho indica pendencia/risco;
- fotos devem manter tratamento suave;
- grupos devem ficar em pill/translucido quando estiverem no topo do canvas.

### 5. Card De Fluxo

Uso:

- etapas de jornada;
- tarefas dentro de uma jornada;
- passos de atendimento;
- passos de resolucao;
- itens acionaveis dentro de um canvas.

Variacoes aprovadas:

- card com 2 tarefas;
- card com lista de tarefas;
- card com avatar;
- card com check;
- card com botao circular;
- card com menu de opcoes.

Regras:

- textos curtos;
- avatar ou icone a esquerda;
- acao/status a direita;
- radius alto;
- borda sutil;
- sombra baixa;
- evitar formularios dentro do card.

### 6. Mini Card De Status

Uso:

- painel direito;
- resumo de etapa;
- contadores pequenos;
- proximas tarefas;
- pendencias curtas.

Variacoes:

- card claro;
- card ativo preto;
- card com numero;
- card com texto curto;
- grade 2x3.

Regras:

- card preto deve indicar foco/selecionado;
- nao carregar muitos numeros;
- manter labels curtos;
- usar grade compacta.

### 7. Painel Grande / Canvas

Uso:

- container principal de uma jornada;
- area de operacao visual;
- agrupamento de cards conectados.

Composicao:

- titulo interno;
- toolbar circular;
- cards de fluxo;
- conectores;
- painel direito compacto.

Regras:

- deve parecer parte de uma tela real;
- fundo cinza/branco frio, nao branco puro;
- radius alto;
- sombra quase invisivel;
- nao virar card dentro de card em telas reais.

### 8. Conectores

Uso:

- indicar sequencia;
- dependencias;
- fluxo principal;
- excecoes;
- conexoes entre cards.

Variacoes:

- linha azul continua;
- linha vermelha continua;
- linha azul com no;
- linha vermelha com no;
- conector curvo;
- conector pontilhado.

Regras:

- conectores devem ser sutis;
- evitar aparencia de software tecnico de fluxograma;
- usar opacidade quando possivel;
- nao competir com o texto dos cards.

### 9. Tabela Leve

Uso:

- conhecimento sugerido;
- listas pequenas;
- registros recentes;
- metadados operacionais;
- tabelas secundarias.

Partes:

- header discreto;
- linhas com divisorias suaves;
- icone favorito;
- status pill;
- metadados curtos;
- paginacao simples quando necessario.

Regras:

- nao usar bordas pesadas;
- manter altura de linha confortavel;
- status com texto + cor;
- usar tabela completa apenas em telas de lista, nao dentro do canvas principal.

### 10. Grafico Semicircular

Uso:

- resumo visual secundario;
- comparacao simples;
- status agregado;
- painel inferior.

Variacoes:

- grafico azul;
- grafico vermelho;
- numero sobreposto;
- label central curto.

Regras:

- manter como elemento secundario;
- nao transformar a tela em analytics pesado;
- usar poucos dados;
- evitar paleta adicional.

### 11. Toolbar De Painel

Uso:

- adicionar;
- exportar/compartilhar;
- calendario;
- busca quando fizer sentido;
- menu contextual.

Regras:

- usar botoes circulares;
- manter grupo pequeno;
- nao misturar muitos tipos de botao;
- posicionar no canto superior direito do painel.

## Tokens Confirmados Pela 3A

| Grupo | Direcao confirmada |
| --- | --- |
| Cor principal | `#10141A` para foco, texto forte e estado ativo. |
| Fundo | `#E4E4E4` como base, com cuidado para nao clarear demais. |
| Azul | `#83A2DB` para progresso, conectores e badges. |
| Vermelho | `#CE6969` para alerta, excecao e badges. |
| Superficie | branco suave/translucido, nunca branco chapado dominante. |
| Radius | alto em botoes, cards e paineis. |
| Sombra | muito sutil, sem profundidade dramatica. |
| Tipografia | geometrica tipo Lufga, limpa e arredondada. |

## Nao Fazer

Nao usar a 3A para:

- gerar paginas finais diretamente sem consultar 2A.2;
- justificar fundo branco dominante;
- criar componentes fora de escopo da referencia;
- trocar o estilo visual;
- aumentar contraste;
- transformar o CRM em UI kit;
- criar landing page;
- criar componentes mobile;
- definir chat, agentes, cotas, billing, permissoes ou configuracoes.

## Relacao Com A Rodada 3B

A Rodada 3B deve criar os componentes que o CRM inteiro precisa e que nao aparecem na referencia.

Entram na 3B:

- inputs;
- formularios;
- filtros;
- busca avancada;
- select/dropdown;
- tabs;
- modal;
- drawer;
- toast/alerta;
- empty state;
- loading/skeleton;
- tabela completa;
- kanban;
- calendario;
- chat/WhatsApp;
- painel de agente/copiloto;
- cotas/limites;
- permissoes;
- billing/plano;
- configuracoes.

Regra para a 3B:

```text
Criar componentes novos sem abandonar o DNA da referencia.
```

## Prompt Base Para Reuso

```text
Use a Rodada 3A como biblioteca dos componentes ja aprovados do Taliya CRM Web.

Ela define botoes circulares, nav pill, sidebar item, avatares, badges, cards de fluxo, mini cards de status, canvas, conectores, tabela leve, grafico semicircular e toolbar.

Mas nao use a 3A sozinha como referencia de atmosfera.
Para atmosfera, use a referencia original e a tela Taliya 2A.2.

Evite branco dominante, UI kit generico, contraste alto e conectores tecnicos demais.
```

