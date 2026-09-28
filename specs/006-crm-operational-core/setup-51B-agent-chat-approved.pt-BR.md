# Setup Inicial - 51B Chat Lateral Do Agente Aprovado

> Status: aprovado conceitualmente v0.2. Imagem de referencia: `51B_round-4.1J_onboarding_agente-configuracao-chat-aprovado.png`.

## Arquivo

Arquivo canonico:

`D:\Downloads\taliya-crm-chatgpt-images-named-20260511-082508\51B_round-4.1J_onboarding_agente-configuracao-chat-aprovado.png`

Arquivo local observado:

`D:\Downloads\ChatGPT Image May 14, 2026, 02_19_10 PM.png`

Arquivo consolidado em pasta nomeada:

`D:\Downloads\taliya-crm-chatgpt-images-named-20260511-082508\51B_round-4.1J_onboarding_agente-configuracao-chat-aprovado.png`

## Objetivo Da Imagem

Validar o comportamento do painel lateral direito do **Agente de configuracao** no Setup Inicial.

Esta imagem nao representa uma pagina completa. Ela define o componente reutilizavel de chat lateral que sera encaixado no shell de onboarding e reaproveitado nas paginas:

- `/onboarding`;
- `/onboarding/diagnostico`;
- `/onboarding/setup`;
- `/onboarding/configuracoes/[area]`;
- `/onboarding/configuracoes/consumo-aulas`;
- `/onboarding/importacao`;
- `/onboarding/revisao`;
- `/onboarding/publicacao` ou estado equivalente;
- `/onboarding/concluido` ou estado equivalente.

## Decisao Principal

O painel lateral do agente deve funcionar como **chat/copiloto contextual**, nao como dashboard, formulario, painel de pendencias ou menu de etapas.

No primeiro acesso em `/onboarding`, o painel do agente nao precisa aparecer antes da primeira resposta. O fluxo aprovado e:

1. usuario informa o nome do studio;
2. sistema cria/identifica o workspace;
3. painel do Agente de Configuracao surge;
4. agente da boas-vindas e explica seu papel no setup.

O centro da pagina continua sendo onde a configuracao real acontece:

- perguntas oficiais;
- campos;
- tabelas;
- upload/importacao;
- revisao;
- conflitos;
- rascunhos;
- publicacao.

O chat lateral acompanha:

- contextualiza a etapa;
- explica impacto;
- responde duvidas;
- orienta o uso do centro;
- sugere perguntas possiveis;
- encaminha ajuda humana quando necessario.

## Estrutura Aprovada

### Cabecalho

Deve conter:

- marca/avatar discreto do agente;
- titulo `Agente de configuracao`;
- status simples, como `Guiando setup`;
- menu discreto, se necessario.

Evitar:

- avatar grande demais;
- mascote infantil;
- botao `X` quando o painel for fixo no shell;
- controles que deem a entender que o agente pode ser desligado durante o setup obrigatorio.

### Primeira mensagem da etapa

A primeira fala do agente deve ser o impacto da etapa.

Exemplo aprovado:

> "Esta etapa afeta agenda, cobranca e comunicacao inicial."

Regra: esta mensagem deve aparecer como balao de chat, nao como card pesado.

### Segunda mensagem

Contextualiza onde o usuario esta.

Exemplo aprovado:

> "Estamos na etapa Dados do studio. Vou te avisar o que e obrigatorio e o que pode ficar para depois."

### Terceira mensagem

Explica que a acao principal esta no centro da pagina.

Exemplo aprovado:

> "Use a area central para preencher, importar ou revisar dados. Eu acompanho daqui e explico qualquer duvida."

Esta mensagem e importante para evitar que o chat vire o lugar principal de configuracao.

### Chips De Duvidas Sugeridas

Os chips nao sao acoes principais. Eles sao exemplos de perguntas que o usuario pode fazer ao agente.

Exemplos aprovados:

- `O que e obrigatorio?`
- `Posso deixar para depois?`
- `Como isso afeta a agenda?`

### Campo De Pergunta

Deve ficar no rodape do painel.

Placeholder aprovado:

`Pergunte sobre esta etapa...`

### Ajuda Humana

Ajuda humana deve aparecer de forma discreta.

Exemplo aprovado:

`Precisa de ajuda humana? Agendar ajuda`

Nao usar card grande de ajuda humana neste asset.

## O Que Foi Rejeitado Nesta Iteracao

Nao usar no 51B:

- card de pendencias dentro do chat;
- lista de proximos passos;
- pergunta `Por onde voce quer comecar?`;
- botoes de upload dentro do chat;
- formulario principal dentro do chat;
- bloco fixo `Nada sera publicado sem sua revisao`;
- dica rapida com like/dislike;
- grade de estados do agente;
- card institucional explicando quem e o agente;
- dashboard lateral.

## Ajustes Visuais Registrados

A imagem atual esta aprovada para seguir como referencia conceitual. Para as proximas composicoes, aplicar estes cuidados:

- encaixar o painel dentro do shell 51A, sem parecer modal solto;
- manter baloes mais leves que cards comuns;
- reduzir branco puro quando estiver dentro do shell;
- usar azul apenas como acento;
- manter bordas finas, sombra discreta e densidade SaaS B2B;
- evitar excesso de espaco vertical quando o painel estiver dentro de uma pagina completa;
- alinhar tipografia, radius e elevacao ao design system Taliya.

## Relacao Com 51A

O shell `51A_round-4.1J_onboarding_asset_shell-base.png` deve ser revisado depois desta decisao.

Novo 51A deve reservar a lateral direita para este chat contextual, nao para um painel de cards do agente.

## Criterio De Aceite

O 51B esta correto quando:

- parece um chat lateral de setup;
- nao compete com a area central;
- nao vira painel de pendencias;
- nao permite publicar ou configurar profundamente pelo chat;
- deixa claro que o agente acompanha e explica;
- pode ser reutilizado em todas as etapas do setup inicial.
