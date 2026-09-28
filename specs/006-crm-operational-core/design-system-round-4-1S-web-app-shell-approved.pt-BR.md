# Design System Web - Rodada 4.1S - App Shell Base Aprovado

> Status: aprovado v0.1. Imagem aprovada: `16_round-4.1S_app-shell_01_base-web.png`. Origem local conhecida: `D:/Downloads/ChatGPT Image May 11, 2026, 09_50_19 AM.png`.

## Objetivo

Definir a moldura visual base do Taliya CRM web.

Esta imagem nao representa uma pagina final de negocio. Ela define a estrutura reutilizavel que todas as paginas web devem respeitar:

- janela/app container;
- sidebar compacta;
- topbar;
- navegacao contextual;
- botoes globais;
- titulo de pagina;
- containers principais vazios;
- area inferior parcialmente visivel;
- linguagem visual premium/minimalista.

## Decisao Visual

A imagem aprovada usa a composicao da referencia `crm_1.webp` como base visual e adapta para Taliya.

Manter nas proximas paginas:

- fundo externo cinza frio;
- janela central com sombra suave;
- bordas arredondadas;
- logo Taliya no topo esquerdo interno;
- sidebar compacta com botoes circulares;
- topbar leve;
- pills de navegacao;
- botao ativo preto;
- botoes circulares globais;
- avatar da usuaria;
- containers grandes e suaves;
- area inferior cortada indicando continuidade/scroll;
- pouco texto, alta clareza visual.

## Arquitetura De Navegacao

### Sidebar Esquerda

A sidebar esquerda representa **grupos principais** do CRM.

Ela deve:

- ficar compacta por padrao;
- usar apenas icones;
- ter botao de expandir/colapsar no topo da sidebar;
- poder mostrar labels apenas quando expandida ou em hover/flyout;
- nao duplicar as paginas da topbar;
- usar badges pequenos para alertas;
- manter utilidades de tema na parte inferior.

Grupos esperados:

- Hoje;
- Conversas;
- Agenda;
- Alunos;
- Vendas;
- Financeiro;
- Operacao;
- Agentes;
- Relatorios;
- Configuracoes.

### Topbar

A topbar representa **paginas dentro do grupo ativo**.

Exemplo aprovado no shell:

- Hoje;
- Tarefas;
- Aprovacoes;
- Incidentes;
- Jornadas;
- Auditoria;
- Relatorios.

Regra:

- apenas um item pode estar ativo por vez;
- o item ativo usa pill preto;
- itens inativos ficam como texto leve;
- a topbar muda conforme o grupo selecionado na sidebar.

### Botoes Globais

Os botoes do canto superior direito nao sao navegacao de pagina.

Eles representam utilidades globais:

- voltar para pagina anterior;
- busca global;
- mensagens;
- notificacoes;
- perfil/avatar.

## Containers Do Shell

O shell aprovado contem containers vazios de proposito.

Eles funcionam como slots:

- container principal;
- containers inferiores;
- areas de acao;
- zonas onde cada pagina vai inserir seu layout ideal.

Na imagem do shell, esses containers devem permanecer vazios. Em paginas reais, eles devem receber componentes especificos da pagina.

## Como Usar Nas Proximas Paginas

Ao gerar uma pagina web:

1. Usar `16_round-4.1S_app-shell_01_base-web.png` como base obrigatoria.
2. Manter sidebar, topbar, janela, fundo, radius, sombras e botoes globais.
3. Trocar apenas:
   - grupo ativo;
   - paginas da topbar;
   - titulo principal;
   - conteudo dentro dos containers.
4. O layout interno deve ser ideal para o conteudo da pagina, nao necessariamente clone de jornada.

## O Que Nao Fazer

- Nao transformar toda pagina em jornada conectada.
- Nao duplicar sidebar e topbar com os mesmos itens.
- Nao usar mais de um item ativo.
- Nao trocar a estrutura visual do shell sem nova decisao.
- Nao usar navegador Chrome real.
- Nao criar landing page.
- Nao substituir os botoes circulares por botoes retangulares grandes.
- Nao usar paleta nova.

## Observacoes Da Aprovacao

A imagem ainda usa `Jornadas` como contexto ativo para demonstrar o shell. Isso e aceitavel: o shell nao e uma pagina neutra abstrata, mas uma moldura validada em contexto.

Para proximas paginas, `Jornadas` deve ser substituido pelo titulo e topbar do grupo/pagina em geracao.

