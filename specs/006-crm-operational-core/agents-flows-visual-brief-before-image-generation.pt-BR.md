# Taliya CRM - Brief Visual Para Imagens De Agentes/Fluxos

Status: direcao visual v0.1.
Data: 2026-05-22.

## Objetivo

Definir o que precisa estar claro antes de gerar imagens/wireframes de Agentes/Fluxos.

Este brief usa como referencia a pasta:

```text
D:\Downloads\taliya-crm-chatgpt-images-named-20260511-082508
```

Contrato visual de todas as paginas de rotina:

```text
agents-flows-routine-page-visual-contract.pt-BR.md
```

Referencias principais analisadas:

- `01_round-1_visual-dna-tokens_aprovada.png`
- `16_round-4.1S_app-shell_01_base-web.png`
- `07_round-3a_componentes-web-referencia_aprovada.png`
- `11_round-3b4_comunicacao-agentes_aprovada.png`
- `15_round-3c3_agentes-auditoria-relatorios_aprovada.png`
- `26_round-4.1F_agenda_01_calendario-operacional.png.png`
- `51C_round-4.1J_onboarding_workspace-configuracao-aprovado.png`
- `52_round-4.1L_agentes_01_catalogo-agentes-aprovado.png`
- `53_round-4.1L_agentes_02_agente-agenda-rotinas-aprovado.png`
- `54_round-4.1L_agentes_03_rotina-presenca-faltas-aprovado.png`

## Direcao Visual Final

Agentes/Fluxos deve parecer uma tela operacional do CRM, nao um painel tecnico de IA.

Direcao:

```text
Claro, denso, calmo, auditavel, com hierarquia forte e pouca decoracao.
```

O visual deve herdar:

- shell branco/cinza claro;
- sidebar iconica vertical;
- topbar limpa;
- botoes pretos para acao primaria;
- pills de status;
- cards brancos com borda sutil;
- paineis laterais para contexto, agente, simulacao ou decisao;
- azul para selecao/orientacao;
- verde para concluido/sucesso;
- laranja para atencao;
- vermelho para falha/bloqueio;
- roxo/azul suave apenas para copiloto/agente.

## Shell Base Obrigatorio

Usar como base visual:

```text
16_round-4.1S_app-shell_01_base-web.png
```

O shell das imagens de Agentes/Fluxos deve preservar:

- moldura/browser;
- logo Taliya no topo esquerdo;
- rail lateral vertical com icones circulares;
- topbar horizontal com secoes principais;
- botao/aba ativa em preto;
- busca, mensagens, notificacao e avatar no topo direito;
- fundo cinza claro;
- grandes paineis brancos arredondados;
- hierarquia com titulo grande no lado esquerdo;
- botoes circulares pequenos para acoes secundarias.

Adaptacao para Agentes/Fluxos:

```text
Item ativo da topbar: Agentes
Titulo da pagina: Agentes
```

Quando a imagem for de uma rotina, o titulo pode ser:

```text
Agente Agenda
Presenca e faltas
```

Mas a estrutura visual continua sendo a do shell base.

## Conteudo Por Tipo De Pagina

### 1. Pagina De Agentes

Rota:

```text
/app/agentes
```

Papel da tela:

Mostrar os agentes da familia Agentes/Fluxos e servir como entrada simples para cada area.

Esta tela nao e dashboard, nao e configuracao e nao e control plane.

Imagem aprovada:

```text
52_round-4.1L_agentes_01_catalogo-agentes-aprovado.png
```

Conteudo principal:

- titulo `Agentes`;
- subtitulo `Areas automatizadas do CRM`;
- grade dos 7 agentes canonicos;
- status resumido em cada card;
- quantidade de rotinas e fluxos em cada card;
- CTA por agente: `Ver agente`, ou `Abrir Agenda` quando Agenda estiver em foco.

Painel direito:

- nao usar Agente de Configuracao nesta pagina;
- esta pagina e catalogo/navegacao, nao configuracao;
- nao usar painel lateral de resumo.

Nao mostrar:

- KPIs;
- filtros;
- chips de plano;
- cota;
- atividade recente;
- graficos;
- tabelas;
- resumo lateral;
- painel de Agente de Configuracao;
- chat;
- drawer;
- cards de upgrade;
- builder de fluxo;
- prompt;
- log tecnico;
- 96 fluxos soltos.

#### Imagem 1 - Composicao Exata

Estado recomendado:

```text
Plano: 7 agentes
Agentes contratados: Atendimento, Agenda, Vendas, Financeiro, Retencao, Gestao/Governanca, Historico/Evolucao
Agentes nao contratados: nenhum
Sem Agente de Configuracao
```

Motivo do estado:

- mostra a visao mais completa de Agentes/Fluxos;
- valida os 7 agentes canonicos;
- deixa claro que `/app/agentes` e uma pagina de catalogo/entrada;
- evita complexidade tecnica logo na primeira imagem.

Shell:

```text
Usar 16_round-4.1S_app-shell_01_base-web.png.
Topbar ativa: Agentes.
Titulo: Agentes.
```

Topo da area principal:

```text
Agentes
Areas automatizadas do CRM
```

Area principal:

Usar uma grade de 7 cards, todos com o mesmo tamanho.

O card `Historico/Evolucao` deve ter exatamente o mesmo modelo visual dos outros cards.
Nao deve virar card horizontal grande.

Cada card de agente deve ter:

- icone circular;
- nome do agente;
- papel em uma frase;
- quantidade de rotinas e fluxos;
- chip de status;
- CTA principal.

Cards:

```text
Atendimento
Ativo
Conversas, triagem, handoff e privacidade
2 rotinas Â· 10 fluxos
CTA: Ver agente

Agenda
Rascunho simulado
Presenca, faltas, reposicoes, vagas e grade
5 rotinas Â· 16 fluxos
CTA: Abrir Agenda

Vendas
Ativo
Leads, experimental, follow-up e matricula
3 rotinas Â· 15 fluxos
CTA: Ver agente

Financeiro
Ativo
Cobrancas, pagamentos, contratos e excecoes
3 rotinas Â· 15 fluxos
CTA: Ver agente

Retencao
Com atencao
Risco, cancelamento, reativacao e reclamacoes
2 rotinas Â· 13 fluxos
CTA: Ver agente

Gestao/Governanca
Ativo
Operacao, cotas, incidentes, auditoria e qualidade
3 rotinas Â· 15 fluxos
CTA: Ver agente

Historico/Evolucao
Ativo
Contexto de aula, notas, documentos e evolucao do aluno
2 rotinas Â· 12 fluxos
CTA: Ver agente
```

Composicao visual ideal:

```text
Topo: titulo + subtitulo
Centro: grade dos 7 agentes em cards iguais
Sem outras secoes
```

Hierarquia:

1. o usuario entende que esta na familia Agentes;
2. ve os 7 agentes canonicos;
3. entende que Agenda esta em foco;
4. sabe o proximo clique: `Abrir Agenda`.

Prompt especifico da imagem 1:

```text
Taliya CRM web app using the approved base shell. Active top navigation: Agentes. Page title: Agentes. Subtitle: Areas automatizadas do CRM. This page is only a clean catalog/entry point for agents, not a dashboard and not a configuration page. Light gray background, white rounded cards, premium operational CRM style. Do not show KPI cards, filters, plan chips, quota, activity feed, table, right summary panel, configuration agent, chat, drawer, upgrade cards, flow builder, prompt editor or technical logs. Show only a grid of seven equal agent cards: Atendimento, Agenda, Vendas, Financeiro, Retencao, Gestao/Governanca, Historico/Evolucao. Each card has a circular icon, agent name, short description, rotinas/fluxos count, status pill and bottom CTA. Agenda is highlighted with a thin blue border, status Rascunho simulado, and black primary button Abrir Agenda. Other cards use discreet Ver agente buttons. Use 3 columns on the first row, 3 columns on the second row, and 1 card on the third row aligned left without stretching. Keep generous whitespace and a calm, simple operational feel.
```
### 2. Pagina Do Agente

Rota:

```text
/app/agentes/[agentId]
```

Exemplo:

```text
/app/agentes/agenda
```

Papel da tela:

Mostrar a area operacional daquele agente e levar o usuario para uma rotina.

Esta tela nao e dashboard, nao e configuracao, nao e simulacao e nao e publicacao.

Imagem aprovada para Agenda:

```text
53_round-4.1L_agentes_02_agente-agenda-rotinas-aprovado.png
```

Conteudo principal:

- breadcrumb `Agentes / Agenda`;
- titulo `Agente Agenda`;
- subtitulo `Presenca, faltas, reposicoes, vagas e grade`;
- status pequeno do agente: `Contratado`, `Nao contratado`, `Pausado` ou `Bloqueado`;
- frase curta opcional: `Escolha uma rotina para ajustar, simular ou publicar.`;
- grade de rotinas do agente;
- cada rotina com nome, descricao curta, quantidade de fluxos, status e CTA `Abrir rotina`.

Para o Agente Agenda, rotinas:

| Rotina | Descricao | Fluxos |
|---|---|---:|
| Presenca e faltas | Confirmacao, falta avisada, no-show e correcao de presenca | 4 |
| Vagas, reposicoes e lista de espera | Vagas abertas, remarcacoes, creditos e lista de espera | 4 |
| Grade e capacidade | Horario fixo, cancelamento pelo studio, conflitos e ajustes de grade | 4 |
| Primeira aula e aulas especiais | Primeira aula, workshops e eventos especiais | 2 |
| Agenda experimental | Disponibilidade para experimental e no-show de experimental | 2 |

CTAs:

- usar somente `Abrir rotina` nos cards;
- nao mostrar `Simular`, `Publicar` ou `Resolver pendencias` nesta pagina.

Painel direito:

- nao usar Agente de Configuracao nesta pagina;
- nao usar painel lateral;
- nao usar resumo operacional.

Nao mostrar:

- KPIs;
- cota;
- filtros;
- atividade recente;
- lista dos 16 fluxos;
- grafico;
- painel lateral;
- Agente de Configuracao;
- chat;
- drawer;
- configuracoes de modo;
- templates;
- tom de voz;
- aprovacoes detalhadas.

#### Cenarios Da Pagina Do Agente

A pagina continua com a mesma composicao em todos os cenarios. O que muda e apenas:

- status do agente;
- status de cada card de rotina;
- texto do CTA quando o agente nao esta contratado ou esta bloqueado.

Prioridade visual dos status quando houver mais de um:

```text
Bloqueada > Pausada > Aprovacao pendente > Excecao aberta > Rascunho simulado > Rascunho > Publicada > Nao publicada
```

| Cenario | Como aparece nesta pagina | CTA |
|---|---|---|
| Plano 7 com Agenda contratada | Status do agente `Contratado`; todos os cards abrem. | `Abrir rotina` |
| Plano 0 agentes | Status do agente `Nao contratado`; cards em preview, sem publicar. | `Ver preview` ou `Ver planos` |
| Plano 1 sem Agenda | Agenda aparece como nao contratada; CRM manual continua fora desta pagina. | `Ver planos` |
| Plano 1 com Agenda | Apenas rotinas de Agenda abrem; demais agentes ficam fora desta pagina. | `Abrir rotina` |
| Plano 3 com Agenda | Agenda abre normalmente; rotinas seguem seus status. | `Abrir rotina` |
| Downgrade remove Agenda | Status `Nao contratado`; rotinas pausadas por plano, historico preservado. | `Ver motivo` |
| Agente pausado | Status do agente `Pausado`; cards mostram rotina pausada quando aplicavel. | `Abrir rotina` |
| Agente bloqueado | Status `Bloqueado`; cards mantem composicao e mostram motivo resumido no status. | `Ver bloqueio` |
| Rotina nunca publicada | Chip `Nao publicada`. | `Abrir rotina` |
| Rotina em rascunho | Chip `Rascunho`. | `Abrir rotina` |
| Rotina simulada | Chip `Rascunho simulado`. | `Abrir rotina` |
| Rotina publicada | Chip `Publicada`. | `Abrir rotina` |
| Rotina com alteracao nao publicada | Chip `Rascunho`. Detalhe profundo fica dentro da rotina. | `Abrir rotina` |
| Rotina com fluxo personalizado | Chip pode mostrar `Personalizada`; detalhes ficam dentro da rotina. | `Abrir rotina` |
| Aprovacao pendente | Chip `Aprovacao pendente`; nao abrir painel nesta pagina. | `Abrir rotina` |
| Excecao aberta | Chip `Excecao aberta`; resolucao fica na rotina/operacao. | `Abrir rotina` |
| Bloqueio por WhatsApp/canal | Chip `Canal bloqueado`; conexao fica em Integracoes. | `Abrir rotina` |
| Bloqueio por cota | Chip `Cota bloqueada`; detalhe fica em Uso/Cotas. | `Abrir rotina` |
| Bloqueio por permissao | Chip `Permissao pendente`; ajuste fica em Configuracoes/Equipe ou rotina. | `Abrir rotina` |
| Bloqueio por dado ausente | Chip `Dado pendente`; correcao fica na origem do CRM. | `Abrir rotina` |
| Incidente pausou rotina | Chip `Pausada por incidente`; investigacao fica em Control Plane. | `Abrir rotina` |

### 3. Pagina Da Rotina

Rota:

```text
/app/agentes/[agentId]/rotinas/[routineId]
```

Exemplo:

```text
/app/agentes/agenda/rotinas/presenca-e-faltas
```

Papel da tela:

Ser a tela principal de entendimento e controle da rotina.

Imagem aprovada:

```text
54_round-4.1L_agentes_03_rotina-presenca-faltas-aprovado.png
```

Conteudo principal:

- breadcrumb: `Agentes > Agenda > Presenca e faltas`;
- titulo `Presenca e faltas`;
- status da rotina;
- seletor `Como essa rotina deve trabalhar?`:
  - Mais manual;
  - Equilibrado;
  - Mais autonomo;
- `Mais autonomo` selecionado como padrao;
- texto explicando que a escolha se aplica aos fluxos abaixo;
- cards explicativos dos fluxos da rotina;
- CTAs: `Simular rotina`, `Ajustar fluxos`, `Revisar para publicar`.

Fluxos na rotina Presenca e faltas:

| Fluxo na UI | Modo no Mais autonomo | Status |
|---|---|---|
| Confirmacao de presenca | Autonomo | Pronto |
| Falta com aviso | Autonomo com excecoes | Pronto |
| No-show | Autonomo com excecoes | Pronto |
| Correcao de presenca | Autonomo com aprovacao | Precisa aprovacao |

Regra dos cards:

- nao mostrar IDs internos como B1/B2/B3/B14;
- chip de modo e chip de status ficam lado a lado no topo do card;
- cada card tem explicacao humana;
- cada card tem detalhes operacionais: gatilho, acao e chamada humana/aprovacao/fallback;
- CTA do card: `Ver e ajustar`.

Painel direito:

- Agente de configuracao no padrao do Setup Inicial;
- explica o perfil selecionado;
- responde por que cada fluxo esta em cada modo;
- oferece perguntas como:
  - `O que muda no Equilibrado?`
  - `Por que correcao pede aprovacao?`
  - `Simular falta com aviso`
  - `O que falta para publicar?`

### 4. Ajustar Rotina E Fluxos

Rota:

```text
/app/agentes/[agentId]/rotinas/[routineId]/ajustar
```

Papel da tela:

Permitir trocar perfil da rotina e ajustar fluxo individual quando necessario.

Conteudo principal:

- cabecalho da rotina;
- perfil atual;
- aviso quando houver personalizacao;
- padroes herdados da rotina:
  - responsaveis padrao;
  - aprovadores padrao;
  - fila humana padrao;
  - prazo padrao, se houver;
- lista de fluxos com modo selecionavel;
- ao abrir um fluxo, mostrar:
  - comportamento por modo;
  - ajustes visiveis;
  - dependencias fixas;
  - bloqueios;
  - fallback;
  - simulacao rapida.

Importante:

```text
Canal, integracao, permissao, dado e cota aparecem como dependencia/leitura, nao como campo editavel.
```

Painel direito:

- Agente de configuracao;
- explica consequencia da mudanca;
- alerta se trocar modo exige nova simulacao;
- pode sugerir ajuste, mas nao publica.

### 5. Pagina Do Fluxo

Rota:

```text
/app/agentes/[agentId]/rotinas/[routineId]/fluxos/[flowId]
```

Motivo:

```text
O painel direito ja pertence ao Agente de Configuracao.
Por isso, detalhe de fluxo nao deve abrir como drawer lateral concorrendo com o agente.
```

A pagina do fluxo usa o mesmo shell base e mantem o Agente de Configuracao no painel direito.

Exemplo:

```text
/app/agentes/agenda/rotinas/presenca-e-faltas/fluxos/falta-com-aviso
```

Papel da tela:

Mostrar exatamente como um fluxo especifico funciona, sem perder o contexto da rotina.

Conteudo principal:

- nome do fluxo, sem ID interno;
- breadcrumb: `Agentes > Agenda > Presenca e faltas > Falta com aviso`;
- objetivo;
- rotina de origem;
- modo atual;
- origem do modo: perfil ou ajuste individual;
- maior modo permitido, refletido nos modos bloqueados;
- seletor compacto de modo, sem texto longo nos cards;
- bloco dinamico `Como funciona neste modo`;
- ajustes visiveis realmente importantes;
- template/tom, se houver comunicacao;
- aprovador/fila humana, se sair do padrao herdado;
- fallback;
- preflight compacto no header, sem card grande de requisitos;
- status da ultima simulacao;
- auditoria prevista.

CTAs:

- `Simular este fluxo`;
- `Voltar ao perfil da rotina`;
- `Salvar rascunho`;
- `Ver execucoes`.

Painel direito:

- Agente de configuracao;
- explica este fluxo;
- responde por que este modo esta selecionado;
- sugere simulacoes;
- explica dependencias e fallback;
- nao publica sozinho.

### 6. Simular Rotina

Rota:

```text
/app/agentes/[agentId]/rotinas/[routineId]/simular
```

Papel da tela:

Ensaiar o fluxo real antes de publicar.

Conteudo principal:

- cenarios na esquerda;
- celular/conversa ou objeto do CRM no centro;
- linha de execucao/gates na direita;
- resultado da simulacao;
- custo/cota estimada;
- fallback;
- auditoria prevista.

Painel direito:

- Agente de configuracao;
- explica o que a simulacao provou;
- sugere corrigir bloqueios;
- nunca aprova/publica sozinho.

### 7. Publicar Rotina

Rota:

```text
/app/agentes/[agentId]/rotinas/[routineId]/publicar
```

Papel da tela:

Revisao final antes de publicar a rotina.

Conteudo principal:

- versao que sera publicada;
- perfil da rotina;
- fluxos que seguem o perfil;
- fluxos personalizados;
- o que vai acontecer sozinho;
- o que pede aprovacao;
- o que chama humano;
- o que continua manual;
- preflight;
- bloqueios;
- auditoria prevista;
- CTA primario `Publicar rotina`.

Painel direito:

- Agente de configuracao;
- explica riscos e bloqueios;
- responde perguntas;
- nao confirma publicacao pelo usuario.

Imagem aprovada:

```text
59_round-4.1L_agentes_06_publicar-rotina-presenca-faltas-aprovado.png
```

Contrato detalhado:

```text
agents-flows-publish-routine-page-contract.pt-BR.md
```

Decisao aprovada: os cards dos fluxos devem resumir tudo que importa da pagina `Ver e ajustar fluxo`: inicio, faz, para/chama equipe ou aprovacao, ajustes principais e continua em. O bloco inferior se chama `O que sera ativado`, nao `Confirmacoes finais`.

### 8. Estados E Variacoes Obrigatorias

Antes de gerar novas imagens, consultar:

```text
agents-flows-state-variant-map.pt-BR.md
agents-flows-remaining-definition-audit.pt-BR.md
```

O caminho feliz ja esta coberto pelas imagens `52` a `59`.

O proximo conjunto visual deve cobrir estados alternativos, principalmente:

1. publicar rotina bloqueada por preflight;
2. rotina publicada;
3. pausa/retomada/rollback;
4. detalhe de execucao;
5. incidente que pausou fluxo/rotina;
6. plano 0 agentes;
7. plano 1 agente sem Agenda contratada.

## O Que Nao Fazer

Nao gerar:

- hero;
- tela de marketing;
- cards enormes explicativos;
- canvas tecnico de node builder como tela principal;
- diagrama de fluxo como primeira experiencia;
- configurador cheio de campos;
- painel escuro;
- tela com gradiente decorativo;
- textos longos dentro dos cards;
- 96 fluxos visiveis de uma vez.

## Tela Inicial Para Gerar Primeiro

Comecar por:

```text
Agente Agenda > Rotina Presenca e faltas
```

Motivo:

- valida perfil da rotina;
- valida modos por fluxo;
- valida simulacao;
- valida publicacao;
- valida aprovacao;
- valida excecao;
- valida dependencia de WhatsApp;
- valida continuidade humana.

## Estado Da Tela Recomendada

Imagem 1 deve mostrar:

```text
Pagina da rotina Presenca e faltas
Perfil atual: Equilibrado
Status: Rascunho simulado ou pronto para simular
WhatsApp: conectado
Cota: OK
1 aprovacao pendente
1 fluxo personalizado ou nenhum, dependendo da versao
CTA principal: Simular rotina
CTA secundaria: Ajustar rotina
```

Fluxos visiveis:

| Fluxo | Modo no perfil Equilibrado | Estado visual |
|---|---|---|
| Confirmacao de presenca | Autonomo | Pronto |
| Falta com aviso | Autonomo com excecoes | Pronto |
| No-show | Copiloto | Sugestao humana |
| Correcao de presenca | Autonomo com aprovacao | Aprovacao |

## Layout Da Pagina Da Rotina

Estrutura recomendada:

```text
Sidebar esquerda
Topbar global
Conteudo central largo
Painel direito com Agente de Configuracao
Barra inferior discreta quando houver rascunho/publicacao pendente
```

Conteudo central:

1. cabecalho da rotina;
2. seletor de perfil;
3. resumo do impacto do perfil;
4. tabela/lista compacta de fluxos;
5. bloco de operacao de hoje;
6. bloqueios e atencoes.

Painel direito:

- agente de configuracao, no mesmo padrao visual do Setup Inicial;
- explicacao curta do perfil escolhido;
- proximas acoes;
- pendencias;
- atalhos para simular/publicar.

Regra obrigatoria:

```text
O painel direito de Agentes/Fluxos deve usar o mesmo padrao do Agente de Configuracao do Setup Inicial.
```

Referencias visuais:

```text
51B_round-4.1J_onboarding_agente-configuracao-chat-aprovado.png
51C_round-4.1J_onboarding_workspace-configuracao-aprovado.png
```

Adaptacao para Agentes/Fluxos:

- titulo: `Agente de configuracao`;
- subtitulo/status: `Ajudando em Agentes/Fluxos`;
- bolinha verde quando disponivel;
- cards de explicacao curtos;
- perguntas sugeridas como botoes contornados;
- campo de pergunta no rodape;
- botao circular preto de envio;
- pode explicar perfil, modo, bloqueio, simulacao, publicacao e fallback;
- pode preparar rascunho e sugerir ajuste;
- nunca publica sozinho;
- nunca altera modo sem simulacao;
- nunca ignora plano, cota, permissao, integracao ou fallback.

Exemplo de conteudo no painel:

```text
Agente de configuracao
Ajudando em Agentes/Fluxos

Esta rotina controla presenca, falta avisada, no-show e correcao de chamada.

Com Equilibrado, eu posso te mostrar o que roda sozinho, o que vira sugestao e onde a equipe aprova.

[O que muda no Equilibrado?]
[Por que B3 esta em Copiloto?]
[Simular falta com aviso]
```

## Como Mostrar Perfil Da Rotina

O seletor deve ser um controle segmentado, nao cards grandes:

```text
[Mais manual] [Equilibrado] [Mais autonomo]
```

Abaixo dele, uma caixa curta:

```text
Com Equilibrado, esta rotina vai:
- confirmar presencas simples automaticamente;
- tratar falta avisada e chamar humano se sair do padrao;
- sugerir acompanhamento de no-show;
- pedir aprovacao para corrigir presenca.
```

Precisa ficar claro:

```text
Perfil muda varios fluxos.
Modo muda um fluxo especifico.
Ajuste individual e excecao.
```

## Como Mostrar Fluxos

Usar lista/tabela compacta, parecida com aprovacao/operacao, nao cards grandes.

Cada linha de fluxo deve ter:

- ID curto;
- nome;
- modo;
- origem do modo;
- status;
- comportamento em uma frase;
- dependencias pequenas;
- acoes iconicas/curtas.

Exemplo:

```text
B1  Confirmacao de presenca
Modo: Autonomo
Origem: Perfil Equilibrado
Status: Pronto
Comportamento: envia confirmacao quando aula, aluno, WhatsApp e cota estao OK.
[Simular] [Ajustar]
```

## Como Mostrar Bloqueios

Bloqueio deve ser contextual e simples.

Exemplo:

```text
WhatsApp desconectado
Este fluxo nao consegue enviar confirmacoes.
Enquanto isso, ele fica em Manual.
[Conectar WhatsApp] [Simular manual]
```

Nao abrir configuracao tecnica dentro de Agentes/Fluxos.

## Como Mostrar Humano Entrando

Usar os mesmos estados do CRM:

| Situacao | Visual |
|---|---|
| Aprovacao | pill azul/laranja, CTA "Revisar aprovacao" |
| Excecao | pill laranja, CTA "Resolver excecao" |
| Fallback manual | tarefa/checklist criada |
| Incidente | vermelho discreto, link para incidente |
| Cota/bloqueio | aviso com caminho manual |

No topo da rotina, mostrar resumo:

```text
Precisa de atencao
2 aprovacoes
1 excecao
1 fluxo pausado
```

## Como Mostrar Simulacao

A simulacao deve parecer um ensaio real.

Layout recomendado:

```text
Coluna esquerda: cenarios
Centro: celular/conversa ou objeto do CRM
Coluna direita: linha de execucao + gates
Rodape: CTAs de simulacao
```

Nao criar cards separados de `Dados da simulacao` ou `Resultado da simulacao`.
O que foi usado e o que aconteceu devem aparecer dentro dos cenarios, do visual central e da linha de execucao.

Para Presenca e faltas:

- confirmar presenca antes da aula;
- aluno avisa falta;
- aula termina com no-show;
- humano corrige presenca.

O celular deve aparecer apenas quando houver mensagem.
Quando for fluxo interno, mostrar estado no CRM, nao celular fake.

Imagem aprovada para Simular fluxo:

```text
58_round-4.1L_agentes_05_teste-fluxo-falta-com-aviso-aprovado.png
```

Observacao: a imagem esta aprovada em estrutura e layout. Na versao final, trocar a nomenclatura de `Teste/Testar` para `Simular/Simulacao`: rota `/simular`, titulo `Simular Falta com aviso`, card `Execucao da simulacao`, chip `Simulacao segura`, CTA `Rodar simulacao novamente` e painel direito `Explicando a simulacao`.

Contrato detalhado:

```text
agents-flows-test-simulation-page-contract.pt-BR.md
```

## Como Mostrar Publicacao

Publicacao deve parecer revisao final, parecida com onboarding/revisao.

Mostrar:

- versao que sera publicada;
- perfil da rotina;
- fluxos que seguem o perfil;
- fluxos personalizados;
- vai acontecer sozinho;
- vai pedir aprovacao;
- vai chamar humano;
- continua manual;
- preflight;
- auditoria prevista.

CTA primario:

```text
Publicar rotina
```

Nao usar:

```text
Ativar rotina
```

Imagem aprovada para Publicar rotina:

```text
59_round-4.1L_agentes_06_publicar-rotina-presenca-faltas-aprovado.png
```

## Imagens Ja Aprovadas Neste Lote

Primeiro lote aprovado:

1. Pagina da rotina `Presenca e faltas`.
2. Ajustar rotina e fluxos.
3. Pagina do fluxo `Falta com aviso`.
4. Simular fluxo com celular/conversa e linha de execucao.
5. Publicar rotina com preflight.

Observacao:

A imagem `59_round-4.1L_agentes_06_publicar-rotina-presenca-faltas-aprovado.png` ja cobre a pagina base de `Publicar rotina` em estado pronto para publicar.

## Variacoes Sem Nova Imagem

Nao gerar imagem nova para:

1. `Publicar rotina` bloqueada por preflight/cota/integracao/permissao/simulacao desatualizada.
2. Rotina publicada.
3. Rotina publicada com excecao aberta.
4. Fluxo sem integracao.
5. Fluxo com cota insuficiente.
6. Fluxo com aprovacao pendente.
7. Fluxo pausado.
8. Plano 0/1/3 agentes vendo partes bloqueadas/upgrade.

Essas variacoes devem ser resolvidas nos documentos de contrato e implementadas como estados dos layouts aprovados.

Contrato operacional completo:

```text
agents-flows-operational-variation-contract.pt-BR.md
```

Contrato de `Simular rotina` sem pagina nova:

```text
agents-flows-routine-simulation-result-contract.pt-BR.md
```

Observacao:

A imagem `58_round-4.1L_agentes_05_teste-fluxo-falta-com-aviso-aprovado.png` ja cobre `Simular fluxo`. Ela nao e uma tela de `Simular rotina`, porque simula o fluxo especifico `Falta com aviso`.

Por enquanto, `Simular rotina` deve ser tratado como uma acao da pagina da rotina que valida o conjunto e atualiza o preflight para `Publicar rotina`, sem imagem propria nova.

## Checklist Antes De Gerar Cada Imagem

Toda imagem deve responder:

- Qual tela e esta?
- Qual rotina/fluxo esta sendo configurado?
- Qual perfil esta selecionado?
- O que muda com esse perfil?
- Quais fluxos aparecem?
- Qual modo cada fluxo usa?
- O que esta pronto, bloqueado, pendente ou aguardando humano?
- Onde o usuario clica agora?
- O que e configuravel e o que e apenas dependencia?

Se a imagem nao responder isso em poucos segundos, ela ainda nao esta pronta.

## Prompt Visual Base

Quando for gerar imagem, usar esta direcao:

```text
Taliya CRM web app, operational SaaS interface for a pilates studio CRM.
Light background, white cards with subtle borders, compact dashboard density, left vertical icon sidebar, clean topbar, black primary CTA, blue selected states, green success pills, orange attention pills, red failure pills, small avatars, rounded 12px panels, minimal shadows, structured tables/lists, right side Agente de Configuracao panel matching the setup onboarding assistant, no marketing hero, no decorative gradients.
Screen: Agente Agenda > Rotina Presenca e faltas.
Show routine profile segmented control: Mais manual, Equilibrado, Mais autonomo selected.
Show four flows: Confirmacao de presenca with chip Autonomo, Falta com aviso with chip Autonomo com excecoes, No-show with chip Autonomo com excecoes, Correcao de presenca with chip Autonomo com aprovacao.
Do not show internal IDs like B1 or B2.
Make it clear that profile changes multiple flows, and each flow can still be opened with Ver e ajustar to change only that flow.
```
