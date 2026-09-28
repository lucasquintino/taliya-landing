# Prompt Standalone - 51A Shell Global Do Onboarding

Status: prompt v0.2 para nova conversa no ChatGPT/Gemini.
Data: 2026-05-14.

## Objetivo

Gerar uma nova versao do asset:

`51A_round-4.1J_onboarding_asset_shell-base.png`

Esta imagem deve ser o **shell global do Setup Inicial** do Taliya CRM.

Nao e uma pagina final.
Nao deve ter conteudo central real.
Nao deve mostrar formulario final, tabela final, importacao real ou revisao real.

Ela deve mostrar a casca reutilizavel que vai receber as paginas depois.

## Anexos Necessarios

Enviar estes anexos na nova conversa:

1. `D:/Downloads/taliya-crm-chatgpt-images-named-20260511-082508/02_round-1_visual-dna-tokens_duplicata.png`
   - Uso: referencia principal de design system.
   - Cores, tipografia, radius, sombras, cards, botoes, badges e espacamento.

2. `D:/Downloads/taliya-crm-chatgpt-images-named-20260511-082508/16_round-4.1S_app-shell_01_base-web.png`
   - Uso: referencia principal de shell/dashboard aprovado.
   - Fundo, estrutura de app, acabamento, densidade e hierarquia.
   - Nao copiar a sidebar operacional completa.

3. `D:/Downloads/ChatGPT Image May 14, 2026, 02_19_10 PM.png`
   - Uso: 51B aprovado conceitualmente.
   - O painel lateral direito do 51A deve encaixar esse chat contextual, nao um painel de cards.

4. `D:/Downloads/ChatGPT Image May 14, 2026, 12_42_02 PM.png`
   - Uso: versao anterior do shell de onboarding.
   - Usar apenas como referencia de arquitetura geral; corrigir a lateral do agente e esvaziar o centro.

## Prompt Para Colar No ChatGPT/Gemini

```text
Quero gerar uma nova versao do asset de shell global do onboarding do Taliya CRM.

Nome do arquivo final:
51A_round-4.1J_onboarding_asset_shell-base.png

Objetivo:
Criar o shell global reutilizavel do Setup Inicial do Taliya CRM.

Esta imagem nao e uma pagina final.
Ela deve mostrar a casca do onboarding, sem conteudo central especifico.

O shell sera usado depois para gerar paginas como:
- onboarding;
- diagnostico;
- setup principal;
- configuracao por area;
- consumo de aulas;
- importacao;
- revisao/publicacao.

Use os anexos assim:

1. Use `02_round-1_visual-dna-tokens_duplicata.png` como referencia principal do design system:
- paleta;
- tipografia;
- radius;
- sombras;
- cards;
- botoes;
- badges;
- espacamento.

2. Use `16_round-4.1S_app-shell_01_base-web.png` como referencia principal de shell/dashboard aprovado:
- fundo geral;
- cor da superficie principal;
- hierarquia entre app background, paineis e cards;
- acabamento premium;
- densidade SaaS B2B;
- bordas e sombras discretas.

3. Use a imagem 51B aprovada como referencia obrigatoria para a lateral direita:
- a lateral direita deve ser o chat contextual do agente;
- nao criar painel de cards do agente;
- nao criar lista de proximos passos;
- nao colocar pendencias dentro do chat;
- nao colocar upload ou formulario dentro do chat.

4. Use a versao anterior do 51A apenas para pegar referencia de arquitetura:
- topbar de onboarding;
- stepper lateral esquerdo;
- area central;
- painel lateral direito;
- rodape global.

Decisao de produto:
- O setup inicial tem uma sequencia definida.
- O usuario nao escolhe livremente por onde comecar.
- O centro da pagina e onde a configuracao real acontece.
- O agente lateral apenas contextualiza, explica, alerta e responde duvidas.
- O agente nao publica sozinho.
- O agente nao configura fluxo profundo.
- O agente nao ativa automacao.

Estrutura obrigatoria do shell:

1. Topbar global do onboarding
- logo Taliya;
- nome do studio, exemplo `Studio Leticia`;
- status `Setup inicial em andamento`;
- progresso geral, exemplo `32%`;
- botao discreto `Ajuda`;
- avatar/usuario.

2. Stepper lateral esquerdo
- titulo `Etapas`;
- etapas: `Diagnostico`, `Dados`, `Agenda`, `Planos`, `Importacao`, `Revisao`;
- deve ocupar a altura util do container;
- deve parecer progresso do onboarding, nao sidebar operacional do CRM;
- pode mostrar uma etapa concluida, uma atual e etapas futuras;
- nao usar menu Hoje, Agenda, Financeiro, Inbox, Alunos etc.

3. Area central vazia/neutra
- criar uma grande area central para receber conteudo futuro;
- nao preencher com conteudo real de pagina;
- nao mostrar formulario real;
- nao mostrar tabela real;
- nao mostrar importacao real;
- nao mostrar revisao real;
- nao mostrar cards finais de impacto ou pendencias;
- usar placeholders estruturais discretos, como:
  - titulo generico `Area da etapa atual`;
  - subtitulo curto `Conteudo da pagina entra aqui`;
  - blocos neutros/slots sem dados reais.
- A area central deve deixar claro que e um container reutilizavel.

4. Lateral direita com chat do agente
- integrar o padrao 51B aprovado;
- cabecalho `Agente de configuracao`;
- status `Guiando setup`;
- primeira mensagem: `Esta etapa afeta agenda, cobranca e comunicacao inicial.`;
- segunda mensagem: `Estamos na etapa Dados do studio. Vou te avisar o que e obrigatorio e o que pode ficar para depois.`;
- terceira mensagem: `Use a area central para preencher, importar ou revisar dados. Eu acompanho daqui e explico qualquer duvida.`;
- chips pequenos de duvidas sugeridas:
  - `O que e obrigatorio?`
  - `Posso deixar para depois?`
  - `Como isso afeta a agenda?`
- campo: `Pergunte sobre esta etapa...`;
- ajuda humana discreta: `Precisa de ajuda humana? Agendar ajuda`.

5. Rodape global do setup
- barra discreta no rodape do shell;
- texto `Ambiente de Setup Inicial`;
- status `Rascunhos salvos automaticamente`;
- link/acao `Pendencias do setup`;
- pendencias aparecem no rodape/shell global, nao dentro do chat.

Direcao visual obrigatoria:
- seguir o design system Taliya;
- seguir o shell/dashboard aprovado;
- fundo principal em cinza claro, nao branco puro;
- paineis brancos sobre fundo cinza claro;
- bordas finas e suaves;
- sombras discretas;
- preto suave como cor principal de texto e acao;
- azul apenas como acento controlado;
- evitar azul saturado como tema dominante;
- evitar brilho/glow;
- evitar gradientes roxos;
- evitar aparencia generica de app de IA;
- usar radius consistente;
- usar espacamentos da escala 4, 8, 12, 16, 24, 32, 40;
- visual SaaS B2B premium, operacional, calmo e confiavel.

Nao mostrar:
- conteudo real de pagina no centro;
- formulario preenchido;
- tabela real;
- card real de impacto;
- card real de pendencias no centro;
- painel de cards do agente;
- lista de proximos passos do agente;
- pergunta `Por onde voce quer comecar?`;
- upload dentro do chat;
- pendencias dentro do chat;
- sidebar operacional completa do CRM;
- menu com Hoje, Agenda, Financeiro, Inbox, Alunos etc.;
- dashboard operacional;
- logs;
- traces;
- incidentes;
- Control Planes;
- builder de fluxo;
- modo manual/copiloto/autonomo por fluxo;
- automacao ativa;
- publicacao automatica;
- hero/landing page.

Resultado esperado:
Uma imagem 16:9 do shell global do onboarding, com topbar, stepper lateral esquerdo, area central vazia/neutra, chat lateral direito do agente integrado e rodape global.
O shell deve parecer pronto para receber qualquer pagina do Setup Inicial, sem ser uma pagina final em si.
```

## Criterios De Aprovacao

A imagem pode ser aprovada se:

- parece shell global de onboarding, nao pagina final;
- a area central esta livre/neutra;
- nao ha conteudo real de configuracao no centro;
- a lateral direita integra o chat do agente 51B;
- o chat nao vira painel de cards;
- pendencias ficam no shell/rodape, nao no chat;
- existe stepper lateral esquerdo de onboarding;
- nao aparece sidebar operacional completa;
- segue o design system Taliya;
- parece mais simples que o app principal, mas ainda premium e operacional.
