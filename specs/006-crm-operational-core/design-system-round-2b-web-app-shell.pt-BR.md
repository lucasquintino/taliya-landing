# Design System Web - Rodada 2B - App Shell Web

> Status: contrato visual v0.1 aprovado a partir da imagem 2A.2. Este documento transforma o clone visual web base em regras reutilizaveis para as proximas rodadas.

## Objetivo

Definir a carcaca visual do CRM web do Taliya.

Esta rodada documenta:

- moldura geral da tela;
- sidebar compacta;
- topo de navegacao;
- titulo de pagina;
- canvas principal;
- faixa de avatares;
- cards conectados;
- painel lateral de status;
- paineis inferiores secundarios;
- densidade, atmosfera e regras de fidelidade visual.

Esta rodada nao define ainda todos os componentes do sistema inteiro. Componentes detalhados entram nas Rodadas 3A e 3B.

## Entradas Usadas

1. Referencia principal: Customer Journey CRM Dashboard.
2. Rodada 1: DNA visual e tokens.
3. Rodada 1.1: especificacao precisa dos tokens.
4. Rodada 2A: primeira tentativa de clone visual web base.
5. Rodada 2A.1: correcao inicial de fidelidade.
6. Rodada 2A.2: base visual aprovada com ressalvas.

## Decisao Da Rodada 2A.2

A imagem 2A.2 fica aprovada como base visual suficiente para seguir.

Ela nao e um clone perfeito, mas capturou o essencial:

- CRM web em uma moldura premium;
- fundo cinza frio;
- app shell com sidebar e topbar integradas;
- pagina "Customer Journeys";
- canvas principal com cards conectados;
- faixa de avatares;
- painel direito de status;
- paineis inferiores parcialmente visiveis;
- linguagem visual limpa, macia e SaaS.

As proximas rodadas devem preservar essa base, corrigindo quando possivel:

- reduzir excesso de branco;
- reduzir nitidez excessiva;
- deixar conectores mais sutis;
- compactar cards quando a tela ficar espacada demais;
- reduzir protagonismo dos paineis inferiores;
- evitar cara de mockup de navegador muito explicito.

## Principio Visual Do App Shell

O web app do Taliya deve parecer um CRM operacional premium, calmo e denso, nao uma landing page e nao uma prancha de componentes.

A tela deve transmitir:

- organizacao;
- controle;
- baixo ruido;
- operacao diaria;
- sensacao humana por avatares;
- automacao discreta por conectores, badges e estados;
- profundidade leve por sombras suaves.

## Estrutura Da Tela

### 1. Moldura Externa

A interface deve aparecer dentro de uma area ampla, com margem cinza ao redor.

Regras:

- usar fundo externo cinza frio;
- evitar tela colada nas bordas;
- evitar branco dominante fora dos paineis;
- manter sombra suave sob a janela;
- nao transformar a moldura em mockup de navegador pesado.

Valores guia:

| Item | Direcao |
| --- | --- |
| Fundo externo | `#E4E4E4` ou cinza frio proximo |
| Margem externa | generosa em imagens de apresentacao |
| Sombra da janela | suave, difusa, sem contraste forte |
| Canto da janela | radius alto, proximo de `24px` a `32px` |

### 2. Barra Superior De Janela

A barra superior pode existir para dar contexto de app web, mas deve ser discreta.

Elementos permitidos:

- controles circulares pequenos a esquerda;
- icones de navegacao simples;
- campo de URL compacto e central;
- menu discreto a direita.

Regras:

- nao deixar a barra alta demais;
- nao usar URL como elemento protagonista;
- nao aumentar contraste da borda superior;
- nao criar aparencia de navegador realista pesado.

### 3. Sidebar Compacta

A sidebar fica fixa a esquerda, integrada ao canvas.

Ela serve como navegacao primaria compacta por icones.

Composicao:

- coluna vertical com largura visual proxima de `72px`;
- botoes circulares empilhados;
- primeiro item logo abaixo do topo;
- grupos separados por respiro;
- acoes utilitarias proximas do rodape;
- item ativo em preto.

Estados:

| Estado | Aparencia |
| --- | --- |
| Default | botao circular branco/translucido, icone preto. |
| Hover/subtle | fundo um pouco mais marcado, sombra leve. |
| Active | fundo `#10141A`, icone branco. |
| Alert | badge vermelho pequeno no canto superior/direito. |
| Disabled | baixa opacidade e sem sombra. |

Regras:

- sidebar nao deve parecer menu textual;
- evitar labels persistentes;
- manter icones circulares;
- usar badges pequenos, nunca banners;
- preservar espacamento vertical calmo.

### 4. Topbar Do Produto

A topbar fica integrada ao topo da interface, abaixo ou junto da moldura superior.

Composicao:

- marca TALIYA a esquerda;
- navegacao horizontal central;
- item ativo em pill preto;
- acoes circulares a direita;
- avatar do usuario no extremo direito.

Navegacao base:

- Relacionamento;
- Oportunidades;
- Leads;
- Agenda;
- Casos;
- Relatorios;
- Propostas.

Estados:

| Estado | Aparencia |
| --- | --- |
| Nav default | texto escuro, sem borda, baixo contraste. |
| Nav active | pill preto, texto branco. |
| Acao default | botao circular claro. |
| Acao com alerta | badge vermelho pequeno. |
| Avatar ativo | avatar circular com possivel dot azul. |

Regras:

- topbar nao deve virar header grande;
- navegacao deve parecer leve;
- item ativo precisa ser claro, mas nao exagerado;
- acoes devem ficar em botoes circulares;
- nao usar retangulos com texto para acoes simples.

### 5. Titulo De Pagina

O titulo principal aparece abaixo da topbar, alinhado a esquerda com a area de conteudo.

Exemplo aprovado:

```text
Customer Journeys
```

Regras:

- titulo grande, forte e limpo;
- peso visual alto;
- sem subtitulo obrigatorio nessa tela base;
- nao transformar em hero;
- nao centralizar.

Token guia:

| Item | Valor |
| --- | --- |
| Fonte | Lufga ou geometrica similar |
| Tamanho | proximo de `40px` |
| Peso | `600` |
| Cor | `#10141A` |

### 6. Canvas Principal

O canvas principal e o grande painel arredondado que contem a jornada operacional.

Ele e o centro visual da tela.

Composicao:

- titulo interno curto;
- faixa de avatares no topo;
- toolbar de acoes circulares a direita;
- cards conectados no centro;
- painel lateral de status no lado direito;
- labels inferiores de etapas.

Exemplo de titulo interno:

```text
Novo atendimento
```

Regras:

- canvas deve dominar a primeira dobra;
- fundo deve ser cinza/branco frio, nao branco puro;
- radius alto;
- sombra quase imperceptivel;
- conteudo denso, mas respiravel;
- nao virar dashboard generico.

Valores guia:

| Item | Direcao |
| --- | --- |
| Fundo | `rgba(255,255,255,0.68)` sobre cinza frio |
| Radius | `32px` ou mais |
| Padding | `28px` a `40px` |
| Sombra | `shadow.1`, muito sutil |

### 7. Faixa De Avatares

A faixa de avatares mostra pessoas, contadores e estados.

Composicao:

- avatares circulares;
- badges numericos pequenos;
- alguns avatares com badge vermelho;
- acao de adicionar como botao pequeno;
- fundo em pill/translucido.

Regras:

- usar avatares humanos para manter sensacao relacional;
- manter badges pequenos;
- nao exagerar saturacao das fotos;
- faixa deve parecer encaixada no canvas principal.

### 8. Cards De Fluxo

Cards de fluxo representam etapas ou tarefas conectadas.

Tipos vistos na base:

- card com 2 tarefas grandes;
- card com lista de tarefas;
- card de resolucao com itens mistos;
- card de status no painel lateral.

Regras:

- cards internos devem ser compactos;
- usar radius alto, mas menor que o canvas;
- textos curtos;
- icones e avatares alinhados;
- evitar excesso de detalhe;
- nao transformar cada card em formulario.

Tokens guia:

| Item | Valor |
| --- | --- |
| Radius | `20px` a `24px` |
| Fundo | `rgba(255,255,255,0.82)` |
| Borda | `rgba(16,20,26,0.06)` |
| Sombra | discreta ou nenhuma |

### 9. Conectores

Conectores sao parte essencial do DNA visual.

Eles comunicam jornada, dependencias e movimento entre tarefas.

Regras:

- linhas finas;
- curvas suaves;
- nos pequenos;
- azul para fluxo principal/progresso;
- vermelho para excecao/pendencia;
- evitar aparencia de ferramenta tecnica de fluxograma;
- conectores devem ser secundarios aos cards.

Tokens guia:

| Item | Valor |
| --- | --- |
| Stroke padrao | `1.5px` |
| Stroke ativo | `2px` no maximo |
| No | `6px` |
| Azul | `#83A2DB` com opacidade quando possivel |
| Vermelho | `#CE6969` com opacidade quando possivel |

### 10. Painel Direito De Status

O painel direito mostra status resumidos e proximas tarefas.

Composicao:

- grade compacta de mini cards;
- card ativo preto;
- cards claros ao redor;
- textos curtos;
- numeros pequenos.

Exemplos:

- Em andamento;
- Proximo passo;
- Comunicacao;
- Verificacao;
- Notificacao;
- Satisfacao.

Regras:

- painel deve ser compacto;
- card preto deve ser o ponto focal;
- nao usar metricas demais;
- nao competir com cards de fluxo;
- manter o painel dentro do canvas principal.

### 11. Paineis Inferiores

Os paineis inferiores aparecem como continuidade da tela.

Eles indicam profundidade do produto, mas nao devem dominar a imagem base.

Tipos vistos:

- conhecimento sugerido;
- jornada de tickets;
- tabela leve;
- grafico semicircular.

Regras:

- devem aparecer parcialmente na primeira imagem base;
- podem ser cortados pela dobra inferior;
- nao detalhar demais;
- nao competir com canvas principal;
- manter mesma linguagem de radius e sombra.

## Conteudo E Linguagem

Para imagens de design system e exploracao visual, usar textos curtos.

Preferir:

- "Novo atendimento";
- "Identificar necessidade";
- "Validar prioridade";
- "Alocar responsavel";
- "Estimar proximo passo";
- "Comunicar cliente";
- "Resolver pendencia";
- "Em andamento";
- "Proximo passo".

Evitar:

- textos longos;
- regras reais complexas;
- nomes tecnicos internos;
- explicacoes dentro da interface;
- copy que transforme a tela em tutorial.

## O Que Nao Fazer

Nao usar esta rodada para:

- criar landing page;
- criar prancha de componentes;
- criar wireframe;
- criar dashboard generico;
- alterar direcao visual;
- adicionar cores dominantes novas;
- criar hero;
- mostrar tudo que o CRM faz;
- detalhar cotas, billing, permissoes ou agentes;
- transformar o app shell em documentacao visual.

## Checklist De Fidelidade Visual

Antes de aprovar uma nova tela web baseada neste shell, verificar:

- A tela parece um CRM em uso, nao uma prancha?
- O fundo geral e cinza frio, nao branco puro?
- A sidebar esta compacta, circular e discreta?
- A topbar esta leve e integrada?
- O titulo de pagina esta forte, mas nao virou hero?
- O canvas principal domina a composicao?
- Os cards internos estao compactos?
- Os conectores estao sutis?
- O painel direito esta dentro da mesma linguagem?
- A parte inferior esta secundaria?
- A tela lembra a referencia principal transformada em Taliya?

## Relacao Com As Proximas Rodadas

### Rodada 3A - Componentes Web Que Aparecem Na Referencia

Deve extrair e documentar:

- botao circular;
- nav pill;
- avatar e badge;
- card de fluxo;
- mini card de status;
- painel grande;
- tabela leve;
- grafico semicircular;
- conector;
- toolbar de painel.

### Rodada 3B - Componentes Web Que Faltam No Sistema Inteiro

Deve criar componentes que nao aparecem na referencia, como:

- formulario;
- input;
- select;
- filtros;
- busca avancada;
- modal;
- drawer;
- tabs;
- kanban;
- calendario;
- chat/WhatsApp;
- agente/copiloto;
- cotas;
- permissoes;
- billing;
- configuracoes.

### Rodada 4 - Paginas Web Por Familia

Deve aplicar este shell em familias reais de paginas:

- Hoje e Operacao;
- Agenda e Turmas;
- Alunos, Responsaveis e Historico;
- Leads, Vendas e Matriculas;
- Financeiro e Retencao;
- Agentes, Fluxos e Execucoes;
- Relatorios;
- Configuracoes.

## Prompt Base Para Reuso

```text
Use o App Shell Web aprovado do Taliya CRM como base visual.

A tela deve parecer um CRM SaaS premium em uso, com fundo cinza frio, sidebar compacta, topbar leve, titulo grande alinhado a esquerda, canvas principal arredondado, botoes circulares, avatares, badges, cards compactos e conectores sutis.

Nao criar prancha de design system.
Nao criar landing page.
Nao criar wireframe.
Nao deixar o fundo branco demais.
Nao transformar a tela em dashboard generico.

Preserve a atmosfera da referencia: cinza, macia, densa, premium e de baixo contraste.
```
