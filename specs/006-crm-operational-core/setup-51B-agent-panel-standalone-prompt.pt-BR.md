# Prompt Standalone - 51B Chat Lateral Do Agente De Configuracao

Status: prompt v0.2 para nova conversa no ChatGPT/Gemini.
Data: 2026-05-14.

## Objetivo

Gerar o asset:

`51B_round-4.1J_onboarding_asset_agent-panel.png`

Este asset deve mostrar somente o painel lateral direito em formato de **chat/copiloto contextual** do Agente de configuracao do Setup Inicial do Taliya CRM.

Nao e uma pagina completa.
Nao e um card institucional sobre o agente.
Nao e um mini dashboard.
E um chat lateral funcional, contextual e reutilizavel.

## Anexos Necessarios

Enviar estes anexos na nova conversa:

1. `D:/Downloads/taliya-crm-chatgpt-images-named-20260511-082508/02_round-1_visual-dna-tokens_duplicata.png`
   - Uso: referencia principal do design system Taliya.
   - Cores, tipografia, radius, sombras, cards, botoes, badges e espacamento.

2. `D:/Downloads/taliya-crm-chatgpt-images-named-20260511-082508/16_round-4.1S_app-shell_01_base-web.png`
   - Uso: referencia do shell/dashboard aprovado.
   - Usar acabamento, densidade, proporcao e linguagem visual.
   - Nao copiar a sidebar operacional completa.

4. `D:/Downloads/ChatGPT Image May 14, 2026, 12_19_48 PM.png`
   - Uso: referencia de personalidade do agente Taliya.
   - Usar como inspiracao de assistente amigavel, com headset e elementos da marca.
   - Nao copiar de forma infantil ou exagerada.

5. `D:/Downloads/taliya-crm-chatgpt-images-named-20260511-082508/09_round-3b2_overlays-feedback_aprovada.png`
   - Uso: overlays, feedback, estados, alertas e tratamento de componentes laterais.

6. `D:/Downloads/taliya-crm-chatgpt-images-named-20260511-082508/11_round-3b4_comunicacao-agentes_aprovada.png`
   - Uso: comunicacao, agente, conversa, sugestoes e copiloto.

7. `D:/Downloads/taliya-crm-chatgpt-images-named-20260511-082508/08_round-3b1_inputs-formularios-filtros_aprovada.png`
   - Uso: botoes, campos, opcoes e componentes de acao.

## Prompt Para Colar No ChatGPT/Gemini

```text
Quero gerar uma nova imagem para o Taliya CRM.

Nome do arquivo final:
51B_round-4.1J_onboarding_asset_agent-panel.png

Objetivo:
Criar somente o painel lateral direito em formato de chat/copiloto contextual do Agente de configuracao usado no Setup Inicial do Taliya CRM.

Este asset sera reutilizado em varias telas do onboarding:
- diagnostico;
- setup principal;
- configuracao por area;
- consumo de aulas;
- importacao;
- revisao/publicacao segura.

Importante:
Nao gere a tela inteira.
Nao gere topbar.
Nao gere stepper.
Nao gere rodape.
Nao gere area principal.
Gere apenas o painel lateral do agente, isolado, em proporcao vertical.

Use os anexos assim:

1. Use `02_round-1_visual-dna-tokens_duplicata.png` como referencia principal do design system:
- cores base;
- tipografia;
- cards;
- radius;
- sombras;
- botoes;
- badges;
- espacamentos.

2. Use `16_round-4.1S_app-shell_01_base-web.png` como referencia do shell/dashboard aprovado:
- acabamento visual;
- densidade SaaS B2B;
- proporcao de componentes;
- linguagem premium e limpa.


4. Use a imagem do agente Taliya apenas como inspiracao de personalidade:
- amigavel;
- humano;
- prestativo;
- com headset;
- com elementos azul/branco da marca.

Nao copie como mascote infantil.
Nao usar olhos exagerados, textura de brinquedo, pose chamativa ou aparencia de desenho infantil.
O agente deve parecer um assistente profissional dentro de um SaaS B2B.

Funcao real do painel:
O painel e um chat/copiloto contextual de configuracao.
Ele explica a etapa atual, responde duvidas, alerta riscos, sugere presets seguros, prepara rascunhos e aponta pendencias.
Ele nao e uma pagina "sobre o agente".
Ele nao e um dashboard lateral.
Ele nao e um menu livre de etapas.

Arquitetura do setup:
- A ordem principal das etapas e definida pelo produto.
- O usuario nao escolhe livremente por onde comecar.
- A configuracao real acontece no centro da pagina: perguntas oficiais, formularios, tabelas, importacao, revisao, conflitos e publicacao.
- O chat lateral acompanha o centro: explica, alerta, guia, responde e sugere.
- Se uma pergunta oficial esta no centro da pagina, ela nao deve ser duplicada como formulario no chat.
- O agente pode comentar a pergunta, explicar impacto ou sugerir uma resposta, mas a decisao estruturada continua no centro.

Estrutura desejada do painel:

1. Cabecalho compacto
- Titulo: "Agente de configuracao"
- Avatar Taliya pequeno/medio, profissional e integrado ao painel
- Status: "Guiando setup"
- O avatar nao deve dominar o painel.

2. Corpo em chat contextual
- O painel deve parecer uma conversa operacional simples.
- Usar baloes de mensagem do agente.
- Nao criar cards grandes empilhados como dashboard.
- Nao criar lista grande de secoes.
- Nao criar chat longo; mostrar poucas mensagens bem escolhidas.

3. Primeira mensagem da etapa: impacto
- A primeira mensagem visivel do chat deve ser um balao curto de impacto.
- Ela deve aparecer como a primeira fala do agente naquela etapa.
- Nao deve ser um card separado.
- O balao deve parecer uma mensagem viva/contextual, nao um card comum.
- Deve ter indicacao visual de animacao discreta, como:
  - tres pontos de digitacao;
  - leve pulso no canto;
  - pequenas linhas/arcos sutis de movimento;
  - marcador "agora" discreto.
- Texto do balao:
  "Esta etapa afeta agenda, cobranca e comunicacao inicial."
- A intencao e situar o usuario antes de ele mexer no centro da pagina.

4. Balao contextual
- Depois da mensagem de impacto, mostrar um balao de contexto.
- Texto:
  "Estamos na etapa Dados do studio. Vou te avisar o que e obrigatorio e o que pode ficar para depois."

5. Balao de orientacao sobre o centro da pagina
- Este balao deve explicar que a acao principal acontece no centro, nao dentro do chat.
- Nao colocar botoes de upload dentro do chat.
- Nao colocar formulario dentro do chat.
- Texto:
  "Use a area central para preencher, importar ou revisar dados. Eu acompanho daqui e explico qualquer duvida."
- Pode ter um marcador visual discreto apontando para a area central, mas sem seta grande chamativa.

6. Campo de pergunta
- Rodape fixo do painel:
  Placeholder: "Pergunte sobre esta etapa..."
- Deve parecer um campo de chat simples e profissional.
- Pode ter icone de enviar.

7. Chips de duvidas sugeridas
- Abaixo ou acima do campo de pergunta, mostrar chips pequenos com possiveis duvidas do usuario.
- Eles nao sao acoes principais.
- Eles sao sugestoes de perguntas que o usuario pode fazer ao agente.
- Exemplos:
  - "O que e obrigatorio?"
  - "Posso deixar para depois?"
  - "Como isso afeta a agenda?"
- Os chips devem ser pequenos, discretos e opcionais.

8. Ajuda humana Taliya
- Link ou botao secundario discreto perto do rodape:
  "Precisa de ajuda humana? Agendar ajuda"
- Deve deixar claro que humano Taliya guia/revisa junto, mas a configuracao continua dentro do sistema.

Direcao visual obrigatoria:
- seguir o design system Taliya;
- seguir o shell aprovado do dashboard e do onboarding;
- branco e cinza claro como base;
- preto suave para texto e acao principal;
- azul apenas como acento controlado;
- bordas finas;
- sombras discretas;
- radius consistente;
- densidade SaaS B2B;
- interface limpa, premium, confiavel e operacional;
- nada futurista, cyberpunk ou generico de IA.

Sobre os baloes animados:
- Como a imagem e estatica, represente a animacao com sinais visuais sutis.
- Nao exagerar.
- Nao usar efeitos chamativos.
- A sensacao deve ser: "o agente esta interagindo agora".
- Os baloes precisam ser claramente diferentes de cards comuns.

Nao mostrar:
- tela inteira;
- topbar;
- stepper;
- rodape;
- dashboard operacional;
- sidebar completa do CRM;
- logs;
- traces;
- incidentes;
- Control Planes;
- builder de fluxo;
- modo manual/copiloto/autonomo por fluxo;
- agente executando automacao;
- publicacao automatica;
- pergunta "Por onde voce quer comecar?";
- lista "Proximo passo sugerido";
- lista grande de sugestoes de setup;
- botoes de upload dentro do chat;
- botoes de configuracao principal dentro do chat;
- card de pendencias dentro do chat;
- linha de seguranca repetitiva dentro do chat;
- card grande de ajuda humana;
- formulario principal dentro do painel;
- grade grande de "Estados do agente";
- card institucional sobre quem e o agente.

Resultado esperado:
Um painel lateral isolado, funcional e reutilizavel, mostrando o Agente de configuracao como chat/copiloto contextual do Setup Inicial.
O painel deve parecer parte natural do Taliya CRM e deve estar pronto para ser reaproveitado nas proximas imagens do onboarding.
```

## Criterios De Aprovacao

A imagem pode ser aprovada se:

- mostra somente o painel do agente;
- segue melhor o design system Round 1;
- a mensagem contextual aparece como balao animado;
- a sugestao/alerta principal aparece como balao animado;
- o painel mostra como o agente funciona na pratica;
- nao vira uma pagina sobre o agente;
- nao vira mini dashboard;
- nao compete com o centro da pagina;
- nao fica infantil;
- nao mostra automacao ativa;
- nao sugere publicacao sem revisao.
