# Auditoria por referencias visuais - PT-BR

> Status: rodada de revisao baseada nas referencias Dribbble indicadas pelo usuario. As referencias usadas foram:
>
> - Customer Journey CRM Dashboard: https://dribbble.com/shots/24659454-Customer-Journey-CRM-Dashboard
> - Sugar CRM - Customer Journey Dashboard mobile/app: https://dribbble.com/shots/24537717-Sugar-CRM-Customer-Journey-Dashboard

## Veredito

Ainda nao estava 100% antes desta rodada.

Os documentos ja cobriam bem os 157 casos de uso, os 96 fluxos fortes de agentes e a separacao entre CRM manual, copiloto e autonomo. O que faltava era transformar essa cobertura em um padrao de produto mais parecido com as referencias: menos "CRM de tabelas" e mais "CRM por jornadas", com cartoes, etapas, responsaveis, contexto lateral e acoes rapidas.

## O que as referencias obrigam o Taliya a ter

1. Um menu principal simples, fixo e visual.
2. Uma pagina central chamada por jornadas, casos ou etapas, nao somente listas.
3. Cartoes operacionais com pessoa, status, etapa, responsavel, prazo, risco e proxima acao.
4. Um painel lateral de contexto para o item selecionado.
5. Abas e filtros no topo para mudar a visao sem trocar de pagina.
6. Acoes pequenas e contextuais nos cartoes.
7. Um modo mobile com cartoes verticais, detalhe em tela cheia e acoes fixas no rodape.
8. Sugestoes de IA dentro do fluxo, mas sem depender de agente ativo.
9. Indicadores de cota/custo quando uma acao pode consumir IA, mensagem ou automacao.
10. Historico, auditoria e permissao visiveis quando a acao for sensivel.

## O que manter

Manter 12 entradas principais no CRM web:

- Hoje
- Inbox
- Alunos
- Agenda
- Vendas
- Financeiro
- Retencao
- Operacao
- Agentes
- Uso e cotas
- Relatorios
- Configuracoes

Manter 38 paginas ou superficies funcionais. Os casos de uso nao pedem uma pagina por caso; eles pedem paginas fortes, com acoes contextuais. A pagina adicional em relacao a rodada visual e "Qualidade de dados", sem menu principal proprio.

Manter o app mobile como ferramenta de operacao diaria, nao como espelho completo do admin web. Mobile precisa resolver atendimento, agenda, chamada, tarefas, aprovacao e alertas.

## O que ajustar

### 1. Operacao vira a casa das jornadas

Antes: "Operacao e alertas".

Agora: "Jornadas e operacao".

Motivo: a referencia mostra um mapa de jornada como tela central. No Taliya, isso deve virar a superficie onde o gestor acompanha casos atravessando areas: agenda, financeiro, retencao, vendas, atendimento e agentes.

Essa mudanca nao cria menu novo. Ela muda a forma da pagina.

### 2. Toda pagina importante precisa de painel lateral

Nas paginas profundas, ao clicar em aluno, aula, lead, pagamento, caso ou tarefa, a direita deve abrir um painel com:

- resumo do objeto;
- linha do tempo curta;
- proxima melhor acao;
- sugestao do copiloto quando aplicavel;
- botoes manuais equivalentes;
- risco, permissao e cota quando existirem.

### 3. Tabelas deixam de ser a experiencia principal

Tabelas continuam uteis para financeiro, relatorios, auditoria e exportacao, mas nao podem ser a unica forma de operar o CRM.

As telas principais devem começar por:

- cartoes de jornada;
- listas priorizadas;
- calendario;
- fila de decisoes;
- mapa de etapas.

### 4. App mobile precisa ser por cartoes

O app deve seguir o padrao da referencia mobile:

- topo com titulo, busca/filtro e acoes pequenas;
- cartoes grandes de jornada, aula, conversa, tarefa ou caso;
- detalhe em tela cheia ao tocar;
- acao principal fixa no rodape;
- navegacao curta para as areas do dia.

## O que remover ou evitar

Evitar:

- criar pagina separada para cada fluxo;
- criar menu principal demais;
- transformar o produto em painel de agentes;
- esconder a operacao manual atras da IA;
- fazer mobile com telas administrativas longas;
- depender de nomes tecnicos como "workflow", "execution", "payload", "run" na versao de produto;
- usar tabela como primeira tela de jornadas, vendas, retencao ou operacao.

## O que faltava e foi adicionado nesta rodada

1. A pagina "Operacao e alertas" foi ajustada para "Jornadas e operacao".
2. Foi criado um mapa de zonas por pagina em `page-layout-zones.pt-BR.md`.
3. Foi mantida a cobertura de 157 casos de uso em `page-case-coverage.pt-BR.csv`.
4. A auditoria visual manteve 12 menus principais. A auditoria ponta a ponta posterior ajustou a contagem para 38 paginas/superficies, adicionando "Qualidade de dados" como superficie de apoio sem menu proprio.
5. Foi definido que o padrao visual principal do CRM web e:
   - menu lateral;
   - topo com filtros;
   - centro com jornada/lista/calendario;
   - painel direito de contexto;
   - acoes por cartao.
6. Foi definido que o padrao principal do app e:
   - lista de cartoes;
   - detalhe em tela cheia;
   - acao fixa;
   - poucos atalhos principais.

## Conclusao

Com esta rodada, o mapa fica coerente com a proposta: Taliya e um CRM completo para studio de Pilates, com agentes integrados, mas capaz de operar com 0 agentes ativos.

O produto nao deve ser desenhado como "painel de automacoes". Deve ser desenhado como "mesa de operacao do studio", onde IA aparece como ajuda, sugestao ou execucao automatica quando o plano, a cota, a permissao e o risco permitirem.
