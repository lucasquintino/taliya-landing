# Design System Web - Rodada 1.1 - Especificacao precisa de tokens

> Status: complemento aprovado da Rodada 1. Este documento transforma a prancha visual em tokens v0.1 para orientar as proximas rodadas sem mudar a direcao visual.

## Objetivo

Definir medidas e regras objetivas para os tokens base do Taliya CRM web.

Esta rodada nao cria novos componentes. Ela apenas refina:

- tipografia;
- layout;
- radius;
- espacamento;
- sombras;
- bordas;
- botoes circulares;
- avatares;
- badges;
- conectores;
- estados basicos.

## Principio visual

O Taliya web deve manter:

- fundo claro frio;
- superficies brancas suaves;
- baixo contraste premium;
- radius alto;
- sombras discretas;
- preto como foco/seleção;
- azul e vermelho como acentos funcionais;
- componentes circulares;
- avatares humanos;
- conectores leves.

## Cores

| Token | Valor | Uso |
| --- | --- | --- |
| `color.black.900` | `#10141A` | texto principal, icones fortes, item selecionado, botao ativo. |
| `color.gray.100` | `#E4E4E4` | fundo principal e superficie neutra. |
| `color.blue.400` | `#83A2DB` | status azul, conexao, badge positivo/neutro. |
| `color.red.400` | `#CE6969` | alerta, risco, excecao e badge vermelho. |
| `color.white` | `#FFFFFF` | cards, paineis, botoes claros. |
| `color.border` | `rgba(16, 20, 26, 0.10)` | bordas leves. |
| `color.border.subtle` | `rgba(16, 20, 26, 0.06)` | divisorias internas. |
| `color.text.primary` | `#10141A` | texto principal. |
| `color.text.secondary` | `rgba(16, 20, 26, 0.62)` | texto de apoio. |
| `color.text.muted` | `rgba(16, 20, 26, 0.42)` | legenda e metadado. |

## Tipografia

Fonte primaria: Lufga.

Fallback: fonte geometrica premium similar, com x-height alto e curvas suaves.

| Token | Tamanho | Line-height | Peso | Uso |
| --- | ---: | ---: | ---: | --- |
| `type.display` | `72px` | `80px` | `600` | marca, prancha, hero de design system. |
| `type.pageTitle` | `40px` | `48px` | `600` | titulo principal de tela. |
| `type.sectionTitle` | `24px` | `32px` | `600` | titulo de painel/secao. |
| `type.cardTitle` | `18px` | `24px` | `600` | titulo de card. |
| `type.body` | `15px` | `22px` | `400` | texto padrao. |
| `type.bodyStrong` | `15px` | `22px` | `600` | acao, item importante, nome. |
| `type.small` | `13px` | `18px` | `400` | apoio, descricao curta. |
| `type.caption` | `11px` | `14px` | `400` | legenda, metadado curto. |
| `type.badge` | `11px` | `12px` | `600` | badge circular/pill. |
| `type.button` | `14px` | `18px` | `500` | botoes e nav pills. |

## Regras tipograficas

- Usar pesos 400, 500, 600 e 700 apenas quando necessario.
- Evitar texto muito escuro para metadados.
- Titulo grande deve ter bastante respiro.
- Texto dentro de cards pequenos deve ser curto.
- Evitar letter spacing negativo.

## Escala de espacamento

| Token | Valor | Uso |
| --- | ---: | --- |
| `space.1` | `4px` | micro-gap, ajuste fino. |
| `space.2` | `8px` | gap entre icone e texto, badge. |
| `space.3` | `12px` | gap compacto. |
| `space.4` | `16px` | padding compacto/card pequeno. |
| `space.5` | `20px` | padding de card medio. |
| `space.6` | `24px` | gap de grid e padding padrao. |
| `space.8` | `32px` | padding de painel. |
| `space.10` | `40px` | gap grande entre blocos. |
| `space.12` | `48px` | respiro de composicao grande. |

## Layout web base

| Token | Valor | Uso |
| --- | ---: | --- |
| `layout.sidebar.compact` | `72px` | sidebar vertical com icones circulares. |
| `layout.topbar.height` | `72px` | barra superior minimalista. |
| `layout.page.paddingX` | `32px` | margem lateral interna. |
| `layout.page.paddingY` | `28px` | margem vertical interna. |
| `layout.grid.gap` | `24px` | gap entre paineis. |
| `layout.panel.gap` | `20px` | gap dentro de grupos. |
| `layout.contextPanel.width` | `320px` | painel lateral futuro. |
| `layout.content.maxWidth` | `1440px` | largura maxima recomendada de canvas. |

## Radius

| Token | Valor | Uso |
| --- | ---: | --- |
| `radius.2xs` | `6px` | micro badges ou elementos muito pequenos. |
| `radius.xs` | `8px` | chips pequenos. |
| `radius.sm` | `12px` | inputs e pills menores. |
| `radius.md` | `16px` | cards pequenos. |
| `radius.lg` | `20px` | cards internos. |
| `radius.xl` | `24px` | paineis medios. |
| `radius.2xl` | `32px` | paineis grandes. |
| `radius.full` | `999px` | avatares, botoes circulares, nav pill. |

## Bordas

| Token | Valor |
| --- | --- |
| `border.width.default` | `1px` |
| `border.width.strong` | `1.5px` |
| `border.color.default` | `rgba(16, 20, 26, 0.10)` |
| `border.color.subtle` | `rgba(16, 20, 26, 0.06)` |
| `border.color.active` | `rgba(16, 20, 26, 0.22)` |
| `border.color.blue` | `rgba(131, 162, 219, 0.70)` |
| `border.color.red` | `rgba(206, 105, 105, 0.70)` |

## Sombras

| Token | Valor |
| --- | --- |
| `shadow.1` | `0 2px 8px rgba(16, 20, 26, 0.08)` |
| `shadow.2` | `0 6px 20px rgba(16, 20, 26, 0.10)` |
| `shadow.3` | `0 12px 32px rgba(16, 20, 26, 0.14)` |
| `shadow.innerSoft` | `inset 0 1px 0 rgba(255, 255, 255, 0.70)` |

## Superficies

| Token | Valor visual | Uso |
| --- | --- | --- |
| `surface.page` | `#E4E4E4` | fundo geral. |
| `surface.panel` | `rgba(255, 255, 255, 0.72)` | painel grande. |
| `surface.card` | `rgba(255, 255, 255, 0.88)` | cards internos. |
| `surface.button` | `rgba(255, 255, 255, 0.82)` | botoes claros. |
| `surface.subtle` | `rgba(16, 20, 26, 0.04)` | areas neutras. |
| `surface.selected` | `#10141A` | item ativo. |

## Cards e paineis

| Componente | Width/height sugerido | Padding | Radius | Borda | Sombra |
| --- | --- | --- | --- | --- | --- |
| Panel grande | fluido | `32px` | `32px` | subtle | `shadow.1` |
| Panel medio | fluido | `24px` | `24px` | subtle | `shadow.1` |
| Card interno | fluido | `20px` | `20px` | default | `shadow.1` |
| Mini card | fluido | `16px` | `16px` | subtle | none ou `shadow.1` |
| Task card compacto | fluido | `14px 16px` | `16px` | subtle | none |

## Botoes circulares

| Token | Tamanho | Icone | Uso |
| --- | ---: | ---: | --- |
| `iconButton.sm` | `36px` | `16px` | acoes dentro de cards pequenos. |
| `iconButton.md` | `44px` | `18px` | acoes padrao. |
| `iconButton.lg` | `52px` | `20px` | acoes de topo/painel. |
| `iconButton.xl` | `60px` | `22px` | destaque raro. |

Estados:

| Estado | Aparencia |
| --- | --- |
| default | fundo branco/translucido, borda default, icone preto. |
| hover | fundo um pouco mais claro, borda active, leve elevation. |
| selected | fundo preto, icone branco, sem borda visivel. |
| subtle | fundo `surface.subtle`, borda quase invisivel. |
| disabled | opacidade `40%`, sem sombra, cursor inativo. |

## Avatares

| Token | Tamanho | Uso |
| --- | ---: | --- |
| `avatar.xs` | `24px` | tabela, metadado. |
| `avatar.sm` | `32px` | linhas compactas. |
| `avatar.md` | `44px` | cards. |
| `avatar.lg` | `56px` | avatar strip e destaque. |
| `avatar.xl` | `72px` | perfil/destaque futuro. |

## Badges

| Token | Tamanho | Texto | Uso |
| --- | ---: | ---: | --- |
| `badge.dot` | `8px` | nenhum | status simples. |
| `badge.count.sm` | `18px` | `10px` | contador em avatar pequeno. |
| `badge.count.md` | `22px` | `11px` | contador padrao. |
| `badge.pill` | auto, min `28px` height | `12px` | status textual. |

Regras:

- Badge em avatar fica no canto inferior direito.
- Badge pode sobrepor levemente o avatar.
- Azul representa neutro/ok/progresso.
- Vermelho representa pendencia/risco.

## Conectores

| Token | Valor |
| --- | --- |
| `connector.stroke` | `1.5px` |
| `connector.stroke.active` | `2px` |
| `connector.node` | `6px` |
| `connector.node.active` | `8px` |
| `connector.color.blue` | `#83A2DB` |
| `connector.color.red` | `#CE6969` |
| `connector.color.muted` | `rgba(16, 20, 26, 0.22)` |
| `connector.dash` | `6px 6px` |

Regras:

- Usar curvas suaves.
- Linha azul = caminho principal.
- Linha vermelha = excecao/risco.
- Linha cinza tracejada = pendente/inativo.
- Conector nao deve competir com o conteudo.

## Estados basicos

| Estado | Regra visual |
| --- | --- |
| default | fundo branco, borda sutil, texto primario/secundario. |
| hover | leve elevacao e borda um pouco mais visivel. |
| selected | preto `#10141A`, texto/icone branco. |
| active | igual selected ou badge azul quando o item continua em progresso. |
| disabled | opacidade reduzida, sem sombra, sem contraste forte. |
| subtle | fundo cinza claro, borda quase invisivel. |
| warning | usar acento quente futuro; se nao definido, usar vermelho com baixa opacidade. |
| danger | vermelho `#CE6969`, nunca em excesso. |
| success | usar verde suave futuro, sem quebrar a paleta. |
| paused | cinza com icone/status discreto. |
| blocked | borda/icone escuro com opacidade e texto explicativo. |

## Tokens que ainda nao devem ser expandidos

Nao detalhar ainda nesta etapa:

- formularios completos;
- tabela densa;
- modais;
- drawers;
- componentes de IA;
- componentes de cota;
- componentes de permissao;
- componentes mobile.

Esses entram em rodadas especificas.

## Checklist para Rodada 2

Ao gerar App Shell Web, usar:

- sidebar compacta `72px`;
- topbar `72px`;
- page padding `32px` horizontal;
- radius alto em todos os containers;
- nav pill preto para item ativo;
- botoes circulares `44px` ou `52px`;
- fundo `#E4E4E4`;
- superficies brancas translúcidas;
- sombras `shadow.1` no maximo para containers comuns.
