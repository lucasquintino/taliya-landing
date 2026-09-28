# Prompt Standalone Arquivado - Previa De Impacto

Status: descontinuado v0.2. Nao gerar agora.
Data: 2026-05-14.

## Decisao Atual

Este prompt foi mantido apenas como historico de exploracao.

A decisao atual e **nao gerar uma previa de impacto standalone como asset separado**.

Atualizacao 2026-05-15: a identificacao `51D` passou a ser usada para a primeira tela real aprovada do setup, `Bloco 1 - Studio`, documentada em `setup-51D-bloco-1-studio-approved.pt-BR.md`.

Motivo:

- o 51C aprovado ja define a area central de configuracao guiada;
- a previa de impacto pode ser desenhada dentro das paginas finais quando for necessaria;
- gerar uma imagem intermediaria so para impacto criaria uma referencia sem necessidade;
- o comportamento de impacto ja aparece no 51C como espaco/slot e validacao inline.

Nao usar este prompt na fila atual de imagens.

## Objetivo

Gerar o asset:

`51D_round-4.1J_onboarding_asset_impact-preview.png`

Este asset deve mostrar a **Previa de impacto** dentro da area central de uma pagina de configuracao do Setup Inicial do Taliya CRM.

Nao e shell global.
Nao e chat do agente.
Nao e drawer de pendencia.
Nao e checklist/progresso.

## Anexos Necessarios

Enviar estes anexos:

1. `D:/Downloads/taliya-crm-chatgpt-images-named-20260511-082508/02_round-1_visual-dna-tokens_duplicata.png`
   - Uso: design system Taliya, cores, tipografia, radius, sombras, cards e espacamento.

2. `D:/Downloads/taliya-crm-chatgpt-images-named-20260511-082508/16_round-4.1S_app-shell_01_base-web.png`
   - Uso: referencia de acabamento e linguagem visual do shell/dashboard aprovado.

3. `D:/Downloads/ChatGPT Image May 14, 2026, 02_39_08 PM.png`
   - Uso: 51A shell global do onboarding aprovado.
   - Manter topbar, stepper, chat lateral e rodape.

4. `D:/Downloads/ChatGPT Image May 14, 2026, 02_19_10 PM.png`
   - Uso: 51B chat lateral aprovado.
   - Manter o agente como chat contextual, sem transformar o chat em area principal.

5. `D:/Downloads/taliya-crm-chatgpt-images-named-20260511-082508/08_round-3b1_inputs-formularios-filtros_aprovada.png`
   - Uso: campos, seletores, botoes e componentes de configuracao.

6. `D:/Downloads/taliya-crm-chatgpt-images-named-20260511-082508/12_round-3b5_sistema-plano-governanca_aprovada.png`
   - Uso: status, governanca, pronto agora, pendente seguro e informacoes de sistema.

Opcional se quiser reforcar feedback/alertas:

7. `D:/Downloads/taliya-crm-chatgpt-images-named-20260511-082508/09_round-3b2_overlays-feedback_aprovada.png`

## Prompt Para Colar No ChatGPT/Gemini

```text
Quero gerar uma imagem para o Taliya CRM.

Nome do arquivo final:
51D_round-4.1J_onboarding_asset_impact-preview.png

Objetivo:
Criar o componente "Previa de impacto" dentro da area central de uma pagina de configuracao do Setup Inicial.

Esta imagem deve usar o shell 51A aprovado e manter o chat 51B na lateral direita.

Importante:
- Nao gere um novo shell.
- Nao gere apenas um card isolado.
- Nao gere um drawer.
- Nao gere checklist/progresso.
- A previa de impacto deve ficar dentro da area central, perto da configuracao que ela explica.
- O chat do agente continua na lateral direita, mas nao e o foco principal.

Contexto da configuracao:
O dono do studio esta configurando consumo de aulas e reposicoes.

Configuracao escolhida:
"Pacote de 8 aulas por mes com reposicao ate 7 dias quando o aluno avisa com 12h de antecedencia."

Layout esperado:

1. Manter shell global 51A
- topbar do onboarding;
- stepper lateral esquerdo;
- rodape global;
- chat lateral direito do agente.

2. Area central da pagina
Mostrar uma pagina de configuracao de consumo de aulas, com:
- titulo: "Consumo de aulas";
- resumo da regra escolhida;
- alguns campos/seletores discretos no topo, como:
  - "Modelo: Pacote mensal";
  - "Aulas por mes: 8";
  - "Reposicao: ate 7 dias";
  - "Aviso minimo: 12h";
- abaixo ou ao lado, o componente "Previa de impacto".

3. Componente Previa de impacto
Titulo:
"Previa de impacto"

Subtitulo curto:
"Veja o que muda antes de salvar o rascunho."

Blocos do componente:

- "Agenda"
  Texto: "Faltas avisadas no prazo podem gerar direito de reposicao."

- "Alunos"
  Texto: "O perfil mostra aulas usadas, disponiveis e expiradas."

- "Financeiro"
  Texto: "A cobranca mensal continua separada do saldo de aulas."

- "Atendimento"
  Texto: "Mensagens de reposicao ficam como modelo inicial."

- "Pronto agora"
  Texto: "Regra base pode ser salva como rascunho."

- "Pode ficar para depois"
  Texto: "Excecoes de feriado e contratos antigos."

- "Exemplo pratico"
  Texto: "Se Ana avisar com 12h de antecedencia, o CRM sugere reposicao dentro de 7 dias."

Direcao visual:
- seguir design system Taliya;
- usar shell 51A aprovado;
- manter chat 51B integrado na direita;
- componente central claro e escaneavel;
- cards leves, bordas finas, sombras discretas;
- preto suave para texto;
- azul apenas como acento;
- verde para pronto/ok com moderação;
- amarelo/laranja leve para "pode ficar para depois", sem parecer erro;
- nao usar vermelho forte;
- nao criar graficos complexos;
- nao parecer dashboard;
- nao parecer simulador tecnico.

Nao mostrar:
- palavra "Simulacao";
- logs;
- traces;
- incidentes;
- Control Planes;
- builder de fluxo;
- autonomia;
- agente ativo/rodando;
- publicacao automatica;
- drawer de pendencia;
- checklist/progresso do setup;
- pendencias dentro do chat;
- upload dentro do chat;
- pergunta "Por onde voce quer comecar?".

Resultado esperado:
Uma tela 16:9 usando o shell de onboarding aprovado, com uma configuracao realista de consumo de aulas na area central e uma "Previa de impacto" clara, mostrando consequencias em Agenda, Alunos, Financeiro e Atendimento antes de salvar/publicar.
```

## Criterios De Aprovacao

A imagem pode ser aprovada se:

- a previa fica dentro da area central;
- o chat lateral nao vira protagonista;
- o componente explica impacto de uma configuracao concreta;
- separa `Pronto agora` de `Pode ficar para depois`;
- nao parece dashboard nem simulador tecnico;
- nao cria drawer de pendencia;
- respeita o shell 51A e o chat 51B aprovados.
