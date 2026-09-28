# Design System Web - Rodada 1 - DNA visual e tokens

> Status: aprovado como base visual inicial. Este documento registra a prancha "Taliya CRM - Web Design System / Round 1: Visual DNA + Tokens" gerada em 2026-05-09.

## Objetivo

Definir a base visual do Taliya CRM web antes de criar componentes complexos ou telas finais.

Esta rodada cobre apenas:

- paleta base;
- escala tipografica base;
- escala de espacamento;
- escala de radius;
- sombras/elevation;
- botoes circulares;
- cards/panels base;
- avatares/badges;
- conectores/linhas;
- pequenos exemplos de composicao.

Nao cobre ainda:

- componentes funcionais completos;
- tabelas densas;
- formularios;
- modais;
- drawers;
- estados complexos;
- componentes de IA/cotas/permissao;
- telas finais.

## Paleta base

| Token | Valor | Uso |
| --- | --- | --- |
| `color.black.900` | `#10141A` | texto principal, logo, icones fortes, item ativo, botao selecionado. |
| `color.gray.100` | `#E4E4E4` | fundo geral, areas neutras e superfícies suaves. |
| `color.blue.400` | `#83A2DB` | conexoes, status positivo/neutro, badge azul, destaque operacional. |
| `color.red.400` | `#CE6969` | alerta, risco, badge vermelho, linha de excecao. |
| `color.white` | `#FFFFFF` | cards, paineis, botoes claros e areas internas. |

## Regras de cor

- O fundo deve ser claro, frio e pouco contrastado.
- O preto deve ser usado com parcimonia, principalmente para foco, selecao e chamadas fortes.
- Azul e vermelho sao acentos funcionais, nao cores decorativas dominantes.
- Superficies brancas devem parecer suaves, quase flutuando sobre o fundo.
- Bordas e sombras devem ser discretas.

## Tipografia

Fonte de referencia: Lufga ou geometrica premium similar.

| Token | Uso | Caracteristica visual |
| --- | --- | --- |
| `type.display` | palavra-marca, chamadas muito grandes | geometrica, limpa, peso alto, muita presenca. |
| `type.h1` | titulo principal de pagina | grande, bold, preto. |
| `type.h2` | titulo de secao | medio, semibold. |
| `type.h3` | titulo de card | compacto, semibold. |
| `type.body` | texto de conteudo | legivel, neutro, baixo ruido. |
| `type.small` | apoio e metadados | pequeno, cinza, discreto. |
| `type.caption` | detalhes sutis | muito pequeno, usado com cuidado. |

## Escala de espacamento

| Token | Valor |
| --- | ---: |
| `space.1` | `4px` |
| `space.2` | `8px` |
| `space.3` | `12px` |
| `space.4` | `16px` |
| `space.6` | `24px` |
| `space.8` | `32px` |
| `space.10` | `40px` |

## Regras de espacamento

- Usar bastante respiro interno em cards e paineis.
- Preferir poucos grupos bem espaçados a muitos elementos apertados.
- Componentes pequenos podem ser densos, mas dentro de containers amplos.
- A interface deve parecer operacional, mas nao pesada.

## Escala de radius

| Token | Valor | Uso |
| --- | ---: | --- |
| `radius.sm` | `8px` | badges, chips pequenos, elementos compactos. |
| `radius.md` | `12px` | inputs futuros, pequenas superficies. |
| `radius.lg` | `16px` | cards pequenos. |
| `radius.xl` | `20px` | cards internos. |
| `radius.2xl` | `24px` | paineis medios. |
| `radius.3xl` | `32px` | paineis grandes e containers principais. |
| `radius.full` | `999px` | botoes circulares, pills, avatares. |

## Sombras e elevation

| Token | Valor visual |
| --- | --- |
| `elevation.1` | `y: 2px`, `blur: 8px`, `#10141A` com `8%`. |
| `elevation.2` | `y: 6px`, `blur: 20px`, `#10141A` com `10%`. |
| `elevation.3` | `y: 12px`, `blur: 32px`, `#10141A` com `14%`. |

## Regras de sombra

- Sombra deve ser quase invisivel.
- A profundidade vem mais de contraste suave, radius e espacamento do que de sombra forte.
- Evitar sombras dramaticas ou dashboard escuro.

## Botoes circulares

| Estado | Aparencia |
| --- | --- |
| Default | circulo branco, borda cinza fina, icone preto. |
| Subtle | circulo cinza claro, sem contraste forte. |
| Selected | circulo preto, icone branco. |

Regras:

- Botoes circulares sao o padrao para acoes iconicas.
- Usar para busca, adicionar, calendario, navegar, abrir, menu e acoes rapidas.
- Para acoes destrutivas/sensiveis, nao confiar apenas no icone; futura rodada deve adicionar confirmacao.

## Cards e paineis

| Componente | Aparencia |
| --- | --- |
| Panel | card grande branco, radius alto, sombra sutil, header no topo. |
| Card | card medio branco, radius alto, divisoria suave. |
| Header card | card pequeno com titulo, subtitulo e area de apoio. |

Regras:

- Paineis agrupam areas funcionais.
- Cards internos agrupam tarefas, etapas ou pequenas entidades.
- Usar divisorias muito suaves.
- Evitar bordas escuras.

## Avatares e badges

| Elemento | Aparencia |
| --- | --- |
| Avatar | circular, imagem centralizada, borda/sombra sutil. |
| Badge azul | pequeno, circular, texto branco. |
| Badge vermelho | pequeno, circular, texto branco. |
| Badge neutro | cinza/white, usado para adicionar ou estado neutro. |

Regras:

- Avatares comunicam atribuicao e atividade.
- Badges devem ficar acoplados ao avatar, geralmente na parte inferior.
- Badge azul tende a representar status neutro/positivo.
- Badge vermelho tende a representar alerta/pendencia/risco.

## Conectores e linhas

| Tipo | Uso |
| --- | --- |
| Linha azul continua | caminho principal ou fluxo positivo/neutro. |
| Linha vermelha continua | excecao, alerta ou caminho de risco. |
| Linha cinza tracejada | estado pendente, opcional, inativo ou futuro. |
| Ponto de conexao | entrada/saida de etapa ou card. |

Regras:

- Conectores devem ser finos e leves.
- Devem comunicar jornada/processo, nao decoracao.
- Usar curvas suaves.
- Evitar excesso de linhas em telas densas.

## Pequenos exemplos de composicao

A prancha validou 3 composicoes iniciais:

1. Card de atividade com avatar, titulo, subtitulo, botao calendario e botao de acao selecionado.
2. Linha de jornada horizontal com avatar, etapa, conector e etapa ativa.
3. Navegacao horizontal compacta com pill preto ativo, icones e avatar.

## Direcao visual aprovada

O Taliya web deve parecer:

- premium;
- leve;
- operacional;
- limpo;
- denso sem parecer poluido;
- humano, com uso forte de avatares;
- orientado por jornada;
- claro, com contraste controlado.

## Regras para proximas rodadas

- Manter a paleta base como ancora.
- Manter radius alto como assinatura visual.
- Manter botoes circulares para acoes iconicas.
- Manter preto como foco/seleção, nao como cor dominante.
- Manter azul/vermelho como linguagem funcional.
- Manter conectores leves e curvos.
- Nao introduzir gradientes fortes, neon, roxo dominante ou sombras pesadas.
- Nao transformar a UI em dashboard corporativo tradicional.
- Todo componente novo deve parecer nativo desta prancha.
