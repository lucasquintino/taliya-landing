# Setup Inicial - 51A Shell Global Do Onboarding Aprovado

> Status: aprovado v0.2. Imagem de referencia: `51A_round-4.1J_onboarding_shell-global-aprovado.png`.

## Arquivo

Arquivo canonico:

`D:\Downloads\taliya-crm-chatgpt-images-named-20260511-082508\51A_round-4.1J_onboarding_shell-global-aprovado.png`

Arquivo local observado:

`D:\Downloads\ChatGPT Image May 14, 2026, 02_39_08 PM.png`

Arquivo consolidado em pasta nomeada:

`D:\Downloads\taliya-crm-chatgpt-images-named-20260511-082508\51A_round-4.1J_onboarding_shell-global-aprovado.png`

## Objetivo Da Imagem

Validar o **shell global do Setup Inicial** do Taliya CRM.

Esta imagem nao representa uma pagina final. Ela define a casca reutilizavel que sera usada pelas telas de onboarding e configuracao inicial:

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

O 51A e o shell base do onboarding.

Ele deve mostrar:

- topbar global do setup;
- stepper lateral esquerdo com sequencia obrigatoria;
- area central neutra para receber conteudo de cada pagina;
- chat lateral direito do agente, seguindo o 51B aprovado;
- rodape global com ambiente, autosave e pendencias.

Ele nao deve mostrar uma pagina final, formulario final, tabela real, importacao real, revisao real ou conteudo operacional do CRM.

## Estrutura Aprovada

### Topbar

Conteudos aprovados:

- logo Taliya;
- nome do studio;
- status `Setup inicial em andamento`;
- progresso geral;
- botao de ajuda;
- avatar/usuario.

### Stepper Lateral Esquerdo

O stepper lateral esquerdo foi aprovado porque deixa claro que o setup tem uma sequencia definida.

Etapas aprovadas:

- `Diagnostico`;
- `Dados`;
- `Agenda`;
- `Planos`;
- `Importacao`;
- `Revisao`.

Regras:

- ocupar a altura util do container;
- mostrar etapa concluida, etapa atual e etapas futuras;
- nao parecer sidebar operacional do CRM;
- nao mostrar menu Hoje, Agenda, Financeiro, Inbox, Alunos etc.

### Area Central

A area central deve ser neutra e reutilizavel.

Ela pode mostrar:

- titulo generico, como `Area da etapa atual`;
- subtitulo curto indicando que o conteudo entra ali;
- slots discretos para formulario, listas, importacao, revisao ou configuracao futura.

Ela nao deve mostrar:

- formulario real;
- tabela real;
- importacao real;
- revisao real;
- cards finais de impacto;
- cards finais de pendencia;
- conteudo especifico de uma pagina.

### Chat Lateral Direito

A lateral direita deve integrar o 51B aprovado como chat contextual do agente.

Deve conter:

- `Agente de configuracao`;
- status `Guiando setup`;
- mensagens curtas em baloes;
- chips de perguntas sugeridas;
- campo `Pergunte sobre esta etapa...`;
- ajuda humana discreta.

Regras:

- nao virar painel de cards;
- nao ter upload dentro do chat;
- nao ter pendencias dentro do chat;
- nao ter lista de proximos passos;
- nao competir com a area central.

### Rodape Global

O rodape global foi aprovado como local correto para informacoes do ambiente e pendencias gerais.

Conteudos aprovados:

- `Ambiente de Setup Inicial`;
- `Rascunhos salvos automaticamente`;
- `Pendencias do setup`.

Regra: pendencias globais do setup ficam no shell/rodape ou drawer, nao dentro do chat do agente.

## Ajustes Registrados Para Proximas Imagens

A imagem esta aprovada como base v0.1. Para proximas composicoes e refinamentos:

- remover o `X` do painel do agente quando ele estiver fixo no shell;
- trocar `Duvidas frequentes` por `Perguntas sugeridas`, ou remover o titulo;
- substituir os placeholders centrais pelo conteudo real apenas nas paginas finais;
- manter o stepper lateral esquerdo como sequencia obrigatoria;
- manter pendencias no rodape/drawer, nao no chat;
- manter o agente discreto e profissional;
- manter azul apenas como acento;
- preservar a densidade SaaS B2B e o design system Taliya.

## O Que Foi Rejeitado

Nao usar no 51A:

- sidebar operacional completa do CRM;
- menu Hoje/Agenda/Financeiro/Inbox/Alunos;
- conteudo real de pagina no centro;
- painel de cards do agente;
- pendencias dentro do chat;
- upload dentro do chat;
- pergunta `Por onde voce quer comecar?`;
- dashboard operacional;
- logs;
- traces;
- incidentes;
- Control Planes;
- builder de fluxo;
- automacao ativa.

## Relacao Com 51B

O 51A depende do 51B aprovado:

- [setup-51B-agent-chat-approved.pt-BR.md](./setup-51B-agent-chat-approved.pt-BR.md)

O 51B define como o agente aparece. O 51A define onde esse chat fica dentro do shell global.

## Criterio De Aceite

O 51A esta correto quando:

- parece shell global de onboarding;
- nao parece pagina final;
- tem area central neutra;
- tem stepper lateral esquerdo;
- integra o chat lateral do agente;
- usa rodape global para pendencias;
- nao mistura setup inicial com CRM operacional;
- segue o DNA visual Taliya.
