# Prompts Para Gerar Assets Reutilizaveis Do Setup Inicial

Status: pacote de prompts v0.1.
Data: 2026-05-14.

Uso: este arquivo pode ser usado de duas formas:

1. Geracao individual: copiar um prompt por vez e anexar somente os arquivos indicados naquele bloco.
2. Geracao em lote sequencial: enviar este arquivo inteiro ao ChatGPT/Gemini com todos os anexos base disponiveis e pedir para gerar as imagens uma por uma, na ordem definida.

Se usar geracao em lote sequencial, o modelo deve tratar cada imagem gerada como referencia obrigatoria para as proximas imagens que dependem dela.

## Objetivo

Gerar primeiro os componentes visuais reutilizaveis do Setup Inicial do Taliya CRM antes de gerar as paginas completas.

Esses assets serao reutilizados nas telas:

- `/onboarding`;
- `/onboarding/diagnostico`;
- `/onboarding/setup`;
- `/onboarding/configuracoes/[area]`;
- `/onboarding/configuracoes/consumo-aulas`;
- `/onboarding/importacao`;
- `/onboarding/revisao`;
- estados opcionais de publicacao/conclusao.

## Regra Global Para Todos Os Prompts

Use estas regras em todos os prompts:

- Produto: Taliya CRM, um CRM completo para studios de pilates.
- Contexto: Setup Inicial do CRM, nao operacao diaria.
- O setup usa shell proprio de onboarding, mais simples e guiado.
- O setup deve parecer leve, claro e orientado por agente.
- O agente de configuracao guia, explica, prepara rascunhos e aponta riscos.
- O agente nao publica sozinho.
- O agente nao ativa autonomia.
- O agente nao configura fluxo profundo.
- O agente nao inventa dado duvidoso.
- O humano Taliya pode orientar, mas nao configura por fora.
- Configuracao profunda de agentes fica para Agentes/Fluxos pos-go-live.
- Control Planes ficam fora do setup inicial.

Nao mostrar em nenhum asset:

- sidebar operacional completa do CRM;
- menu com Hoje, Agenda, Financeiro, Inbox, Alunos etc.;
- dashboard operacional;
- logs, traces, incidentes;
- builder de fluxo;
- modo manual/copiloto/autonomo por fluxo;
- agente ativo/rodando;
- automacao autonoma;
- tela escura, cyberpunk, futurista ou generica de IA.

## Instrucao Para Geracao Em Lote Sequencial

Use esta instrucao quando enviar este arquivo inteiro ao ChatGPT/Gemini:

> Voce vai gerar uma biblioteca de assets reutilizaveis para o Setup Inicial do Taliya CRM.
>
> Nao gere tudo como uma imagem unica.
>
> Gere uma imagem por vez, exatamente na ordem deste documento.
>
> Depois de gerar cada imagem, use a imagem recem-gerada como referencia visual obrigatoria para as proximas imagens que dependem dela.
>
> Mantenha consistencia visual entre todos os assets: mesmo shell, mesma linguagem visual, mesmas proporcoes, mesmos estilos de card, mesma topbar, mesma densidade e mesmos estados.
>
> O asset `51B_round-4.1J_onboarding_asset_agent-panel.png` ja foi aprovado conceitualmente como chat lateral do agente. Use esse 51B como referencia para regerar o `51A_round-4.1J_onboarding_asset_shell-base.png`.
>
> O `51A` define o shell visual global. Depois dele, todos os proximos assets devem herdar esse shell.
>
> Quando um prompt mencionar um asset gerado anteriormente como anexo, use a imagem que voce acabou de gerar nessa conversa.
>
> Se algum anexo externo nao estiver disponivel, use apenas os anexos enviados e preserve a decisao de produto descrita no prompt. Nao invente novo produto, rota ou arquitetura.
>
> Antes de cada imagem, mostre o nome exato do arquivo que sera gerado. Depois gere somente aquela imagem.
>
> Nao avance para a proxima imagem se eu pedir revisao da imagem atual.
>
> Se eu pedir para continuar, gere a proxima imagem da sequencia.

## Anexos Para Enviar No ChatGPT/Gemini Em Lote

Quando for gerar tudo em uma mesma conversa, envie todos os anexos base que voce tiver disponiveis logo no inicio.

Anexos recomendados:

1. `16_round-4.1S_app-shell_01_base-web.png`
   - Uso: DNA visual Taliya, proporcao, acabamento e tratamento de superficie.
   - Nao copiar a sidebar operacional completa.

2. Referencia visual da rodada 3B.1, se existir
   - Inputs, formularios, filtros e campos editaveis.

3. Referencia visual da rodada 3B.2, se existir
   - Drawers, modais, alertas, bloqueios e feedback.

4. Referencia visual da rodada 3B.4, se existir
   - Comunicacao, agente, painel de conversa e sugestoes.

5. Referencia visual da rodada 3B.5, se existir
   - Sistema, plano, permissoes, governanca e status.

6. Referencia visual da rodada 3C.1, se existir
   - Objetos, setup, importacao, dados e qualidade.

7. Referencia visual da rodada 3C.3, se existir
   - Auditoria, historico, agentes avancados e relatorios. Usar com cuidado no onboarding.

Se voce nao tiver todos os anexos, ainda pode comecar com o `16_round-4.1S_app-shell_01_base-web.png`; os outros melhoram consistencia dos componentes especificos.

## Prompt Mestre Para Colar Antes Do Arquivo Inteiro

Cole este texto no ChatGPT/Gemini antes ou junto do arquivo inteiro:

```text
Quero gerar uma biblioteca de imagens/assets reutilizaveis para o Setup Inicial do Taliya CRM.

Vou anexar todas as referencias visuais disponiveis agora e vou colar um arquivo com todos os prompts.

Siga estas regras:

1. Gere uma imagem por vez, na ordem do documento.
2. Use o 51B aprovado como referencia do chat lateral e comece pela nova versao de `51A_round-4.1J_onboarding_asset_shell-base.png`.
3. Depois de gerar uma imagem, trate essa imagem como referencia visual obrigatoria para as proximas imagens.
4. Quando o documento disser que um asset depende de outro, use o asset ja gerado nesta conversa.
5. Nao gere uma montagem unica com todos os assets.
6. Nao pule etapas.
7. Antes de cada imagem, diga o nome exato do arquivo que voce vai gerar.
8. Depois gere somente a imagem daquele asset.
9. Espere minha aprovacao ou pedido de continuidade antes de seguir para o proximo asset.
10. Mantenha consistencia visual em todos os assets: mesmo shell, mesma topbar, mesmos estilos de card, mesma densidade e mesma linguagem visual.
11. O setup inicial tem shell proprio de onboarding. Nao use a sidebar operacional completa do CRM.
12. O agente de configuracao guia, mas nao publica, nao ativa automacao e nao configura fluxo profundo.
13. Nao mostrar agente ativo/rodando, control planes, logs, incidentes ou builder de fluxo.
14. Use linguagem operacional simples em PT-BR.

Agora leia o arquivo completo de prompts e comece gerando apenas a nova versao do shell: `51A_round-4.1J_onboarding_asset_shell-base.png`, usando o 51B aprovado como referencia para a lateral direita.
```

Linguagem visual:

- profissional, calma, moderna e confiavel;
- interface SaaS B2B premium, mas simples;
- densidade media, nao landing page;
- poucos elementos decorativos;
- foco em fluxo guiado;
- cores alinhadas ao DNA visual Taliya;
- texto curto e legivel;
- cards com raio contido;
- sem hero, sem marketing, sem ilustracao abstrata.

Termos de UI preferidos:

- usar `Setup inicial`;
- usar `Pronto agora`;
- usar `Pendente seguro`;
- usar `Configurar depois`;
- usar `Previa de impacto`;
- usar `Regras de seguranca`;
- usar `Aprovacoes`;
- usar `Excecoes`;
- usar `Modelos de mensagem`;
- usar `Rotinas operacionais`;
- usar `Agente preparado`.

Evitar termos de UI:

- nao usar `Fluxos CRM`;
- nao usar `Politicas` como termo principal para o gestor;
- nao usar `Simulacao` no onboarding;
- nao usar `Autonomo` como status publicado no setup;
- nao usar `Ativo` para agente no setup.

## Biblioteca De Anexos

Use poucos anexos por prompt. Muitos anexos confundem o gerador.

### Anexos Base

`A1 - App shell Taliya aprovado`

- Arquivo sugerido: `16_round-4.1S_app-shell_01_base-web.png`.
- Uso: apenas DNA visual, proporcao, tratamento de superficie, topbar e acabamento.
- Importante: nao copiar a sidebar operacional completa.

`A2 - Componentes de formulario`

- Fonte visual: `design-system-round-3b1-web-inputs-forms-filters.pt-BR.md` ou imagem equivalente da rodada 3B.1.
- Uso: inputs, formularios, filtros, campos editaveis, estados.

`A3 - Overlays e feedback`

- Fonte visual: `design-system-round-3b2-web-overlays-feedback.pt-BR.md` ou imagem equivalente da rodada 3B.2.
- Uso: drawers, alertas, bloqueios, confirmacoes, estados de erro.

`A4 - Comunicacao/agentes`

- Fonte visual: `design-system-round-3b4-web-communication-agents.pt-BR.md` ou imagem equivalente da rodada 3B.4.
- Uso: painel do agente, conversa guiada, sugestoes, ajuda humana.

`A5 - Sistema/plano/governanca`

- Fonte visual: `design-system-round-3b5-web-system-plan-governance.pt-BR.md` ou imagem equivalente da rodada 3B.5.
- Uso: status, plano, permissao, cota, governanca simples.

`A6 - Objetos/setup/dados`

- Fonte visual: `design-system-round-3c1-web-objects-setup-data.pt-BR.md` ou imagem equivalente da rodada 3C.1.
- Uso: importacao, objetos, mapeamento, qualidade de dados.

`A7 - Auditoria/agentes avancados`

- Fonte visual: `design-system-round-3c3-web-advanced-agents-audit-reports.pt-BR.md` ou imagem equivalente da rodada 3C.3.
- Uso: auditoria, versionamento, estados sensiveis. Usar com cuidado no onboarding.

## Ordem De Geracao

Gerar nesta ordem:

1. Usar `51B` aprovado como referencia do chat lateral do agente.
2. Regerar `51A` Shell global do onboarding com o 51B integrado.
3. `51C` Area central de configuracao guiada.
4. `53A` Seletor de fonte de importacao.
5. `53B` Tabela de confianca por campo.
6. `54A` Card de agente preparado.
7. `55A` Resumo de revisao/publicacao.

Depois, se necessario:

- `51F` Ajuda Taliya;
- `52A` Pergunta guiada;
- `52B` Card de regra por area;
- `52C` Antes/depois;
- `53C` Drawer de conflito;
- `54B` Linha de pacote recomendado;
- `55B` Confirmacao de publicacao;
- `55C` Estado de sucesso.

---

# PROMPT 51A - Shell Base Do Onboarding

Nome do arquivo final:

`51A_round-4.1J_onboarding_asset_shell-base.png`

## Anexos Necessarios

Obrigatorios:

- `A1 - App shell Taliya aprovado`.
- `51B_round-4.1J_onboarding_asset_agent-panel.png` aprovado como chat lateral do agente.

Opcional:

- referencia Round 1 de Visual DNA/Tokens, se disponivel;
- versao anterior do 51A, apenas para entender a arquitetura que sera corrigida.

## Prompt Para ChatGPT

Crie uma imagem de interface web desktop para o Taliya CRM.

Esta imagem e um asset reutilizavel, nao uma pagina final.

Objetivo: criar o shell proprio do Setup Inicial do Taliya CRM para studios de pilates.

Contexto do produto:

- Taliya e um CRM completo para studios de pilates.
- Esta tela e do Setup Inicial.
- O setup ajuda o dono do studio a colocar o CRM para operar com seguranca.
- O setup e guiado por um agente de configuracao.
- O agente guia, explica e prepara rascunhos, mas nao publica sozinho.
- O dono pode seguir sozinho ou agendar ajuda humana Taliya.

Layout desejado:

- Interface desktop 16:9.
- Topo simples com marca Taliya, nome do studio e progresso geral.
- Nao usar sidebar operacional completa.
- Criar uma area central ampla, livre e neutra para receber conteudo futuro.
- A area central nao deve mostrar uma pagina real, formulario final, tabela real ou blocos finais de impacto.
- Incluir uma coluna lateral direita com o chat contextual do agente de configuracao, seguindo o padrao aprovado no 51B.
- Incluir um stepper/checklist lateral esquerdo simples de etapas do onboarding, sem parecer sidebar operacional do CRM.
- Incluir no topo ou canto superior uma acao discreta de `Ajuda Taliya`.
- Incluir um indicador de status do setup, por exemplo `Setup inicial em andamento`.
- Incluir progresso geral curto, por exemplo `32% concluido`.

Estrutura visual:

- Topbar limpa.
- Corpo em tres areas:
  - stepper lateral esquerdo de onboarding;
  - area principal grande e vazia para conteudo futuro;
  - chat lateral direito do agente.
- Rodape global discreto do setup com ambiente, autosave e pendencias globais.
- Fundo claro ou neutro sofisticado.
- Cards com bordas suaves e hierarquia clara.
- Visual calmo, organizado e premium.

Texto curto que pode aparecer:

- `Setup inicial`;
- `Studio Vida Movimento`;
- `32% concluido`;
- `Continuar configuracao`;
- `Ajuda Taliya`;
- `Agente de configuracao`;
- `Guiando setup`;
- `Pergunte sobre esta etapa...`;
- `Pendencias do setup`;
- `Rascunhos salvos automaticamente`.

Nao mostrar:

- menu lateral do CRM operacional;
- Hoje, Agenda, Financeiro, Inbox, Alunos;
- dashboard;
- graficos;
- conteudo central especifico de uma pagina;
- formulario preenchido;
- card grande de agente;
- lista de proximos passos do agente;
- pergunta `Por onde voce quer comecar?`;
- logs;
- incidentes;
- builder de fluxo;
- agente ativo/rodando;
- modo autonomo;
- tela escura futurista.

Importante:

- Use o anexo apenas como DNA visual Taliya.
- Nao copie a sidebar operacional do anexo.
- O resultado deve parecer um onboarding guiado, nao um painel operacional.

## Criterios De Aceite

A imagem esta correta se:

- parece um shell de onboarding;
- tem topbar simples;
- nao tem sidebar operacional completa;
- tem area central livre para conteudo futuro;
- tem stepper lateral esquerdo de onboarding;
- tem chat lateral do agente integrado, seguindo o 51B;
- nao tem conteudo final de pagina no centro;
- mostra progresso;
- parece Taliya, mas mais simples que o app principal.

---

# PROMPT 51B - Chat Lateral Do Agente De Configuracao

Nome do arquivo final:

`51B_round-4.1J_onboarding_asset_agent-panel.png`

## Anexos Necessarios

Obrigatorios:

- `51A_round-4.1J_onboarding_asset_shell-base.png`.
- `A4 - Comunicacao/agentes`.

Opcional:

- `A3 - Overlays e feedback`.

## Prompt Para ChatGPT

Crie uma imagem de asset reutilizavel para o Taliya CRM.

Objetivo: desenhar o chat lateral do agente de configuracao usado no Setup Inicial.

Este asset deve ser mostrado dentro do shell de onboarding aprovado.

Contexto:

- O agente de configuracao guia o dono do studio durante o setup.
- Ele explica perguntas, aponta impacto, responde duvidas e prepara rascunhos.
- Ele nao publica sozinho.
- Ele nao ativa automacao.
- Ele nao configura fluxo profundo.
- Ele pode recomendar ajuda humana Taliya quando necessario.
- A ordem principal das etapas e definida pelo produto; o agente nao oferece menu livre de por onde comecar.
- A configuracao real acontece no centro da pagina; o chat lateral apenas orienta, explica, alerta e sugere.

Layout:

- Usar o shell de onboarding como base.
- Focar no painel lateral direito.
- Painel com cabecalho `Agente de configuracao`.
- Corpo em formato de chat contextual.
- Mensagens curtas em baloes.
- Primeira mensagem da etapa deve ser um balao de impacto.
- Depois, um balao contextualiza a etapa atual.
- Depois, um balao orienta que a acao principal acontece no centro da pagina.
- Nao colocar botoes de upload, formulario ou pendencias dentro do chat.
- Campo inferior: `Pergunte sobre esta etapa...`.
- Chips pequenos de duvidas sugeridas, nao acoes principais.
- Ajuda humana Taliya como link ou botao secundario discreto.
- Indicador simples do estado atual do agente.

Estado principal a representar:

- `Guiando setup`.

Pode mostrar um alerta leve de impacto, mas nao mostrar uma grade de estados.

Texto sugerido:

- `Agente de configuracao`;
- `Guiando setup`;
- `Esta etapa afeta agenda, cobranca e comunicacao inicial.`;
- `Estamos na etapa Dados do studio. Vou te avisar o que e obrigatorio e o que pode ficar para depois.`;
- `Use a area central para preencher, importar ou revisar dados. Eu acompanho daqui e explico qualquer duvida.`;
- `Pergunte sobre esta etapa...`;
- `O que e obrigatorio?`;
- `Posso deixar para depois?`;
- `Como isso afeta a agenda?`;
- `Ajuda humana`.

Nao mostrar:

- agente ativo;
- agente autonomo;
- agente publicando;
- agente executando tarefas;
- chat longo de atendimento generico;
- pergunta `Por onde voce quer comecar?`;
- lista de proximos passos competindo com a sequencia do setup;
- botoes de upload dentro do chat;
- botoes de configuracao principal dentro do chat;
- card de pendencias dentro do chat;
- linha de seguranca repetitiva dentro do chat;
- formulario principal dentro do painel;
- grade de estados do agente;
- card institucional sobre o agente;
- conversa de atendimento com aluno;
- logs ou traces.

## Criterios De Aceite

A imagem esta correta se:

- o agente parece copiloto contextual, nao executor;
- o painel parece chat lateral simples;
- as mensagens sao curtas e ligadas a etapa atual;
- as acoes sugeridas sao seguras e nao substituem o centro da pagina;
- existe ajuda humana discreta;
- o painel cabe em todas as paginas do onboarding;
- nao parece chatbot de suporte operacional nem dashboard paralelo.

---

# PROMPT 51C - Area Central De Configuracao Guiada

Prompt standalone completo em `setup-51C-configuration-workspace-standalone-prompt.pt-BR.md`.

Resumo: gerar a area central de configuracao guiada dentro do shell 51A, com exemplo de `Consumo de aulas`, campos, seletores, validacoes inline, acoes da etapa e slot reservado para a futura `Previa de impacto`.

Nao gerar checklist/progresso.

---

# PROMPT 51D - Nao Gerar Agora

Status: nao gerar agora.

Motivo: o 51C aprovado ja define a area central de configuracao guiada e inclui espaco para impacto quando necessario. A previa de impacto deve ser desenhada dentro das paginas finais, perto da configuracao concreta, sem criar asset intermediario obrigatorio nesta fase.

Regra futura: quando a previa aparecer, usar `Previa de impacto`, nao `Simulacao`; manter perto da configuracao; nao colocar no chat do agente; nao transformar em dashboard.

---

# PROMPT 51E - Removido Da Fila De Geracao

Status: nao gerar agora.

Motivo: depois da aprovacao do 51A e 51B, pendencias simples devem aparecer na propria tela, perto da configuracao que falta, ou no rodape global do shell. Quando for necessario abrir detalhe, o produto deve herdar padroes de drawer/modal ja aprovados, sem criar um asset proprio de pendencia neste momento.

Decisao: pular 51E. Nao usar 51E como dependencia para paginas finais nesta fase.

---

# PROMPT 51F - Ajuda Taliya Card/Modal

Nome do arquivo final:

`51F_round-4.1J_onboarding_asset_taliya-help-card-modal.png`

## Anexos Necessarios

Obrigatorios:

- `51A_round-4.1J_onboarding_asset_shell-base.png`.
- `A3 - Overlays e feedback`.

Opcional:

- `51B_round-4.1J_onboarding_asset_agent-panel.png`.

## Prompt Para ChatGPT

Crie uma imagem de asset reutilizavel para o Taliya CRM.

Objetivo: mostrar o card e modal/drawer de ajuda humana Taliya dentro do Setup Inicial.

Contexto:

- O studio pode fazer o setup sozinho com o agente.
- Ou pode agendar ajuda humana Taliya.
- A chamada humana nao cria outro fluxo.
- O humano orienta dentro do sistema, sem configurar por fora.

Mostrar:

- card compacto `Ajuda Taliya`;
- botao `Agendar chamada`;
- estado de chamada agendada;
- resumo para especialista;
- pendencias que devem ser discutidas;
- campo de anotacoes/recomendacoes;
- link de chamada.

Estados:

- sem chamada;
- chamada recomendada;
- chamada agendada;
- em revisao com Taliya;
- anotacoes recebidas.

Texto sugerido:

- `Ajuda Taliya`;
- `Podemos revisar esse setup com voce`;
- `Chamada agendada`;
- `Pendencias para discutir`;
- `O fluxo continua dentro do sistema`.

Nao mostrar:

- humano configurando por fora;
- tela de suporte generica;
- atendimento a aluno;
- chat operacional.

## Criterios De Aceite

A imagem esta correta se:

- fica claro que a ajuda humana e opcional;
- a experiencia continua a mesma;
- a chamada ajuda a revisar, nao substitui o sistema.

---

# PROMPT 52A - Card De Pergunta Guiada

Nome do arquivo final:

`52A_round-4.1J_onboarding_component_guided-question-card.png`

## Anexos Necessarios

Obrigatorios:

- `51A_round-4.1J_onboarding_asset_shell-base.png`.
- `A2 - Componentes de formulario`.

Opcional:

- `51B_round-4.1J_onboarding_asset_agent-panel.png`.

## Prompt Para ChatGPT

Crie um componente visual reutilizavel para perguntas guiadas do Setup Inicial do Taliya CRM.

Esse componente sera usado em diagnostico, setup e configuracoes por area.

Mostrar:

- pergunta em linguagem simples;
- opcoes de resposta;
- opcao `Nao sei ainda`;
- campo livre opcional;
- exemplo pratico;
- pequena previa de impacto;
- acao `Continuar`;
- acao secundaria `Pular por enquanto`, se seguro.

Exemplo de pergunta:

`Como voces registram presenca?`

Opcoes:

- `No papel`;
- `Na planilha`;
- `No sistema antigo`;
- `Ainda nao registramos`;
- `Nao sei ainda`.

Estados:

- respondida;
- nao sei ainda;
- incompleta;
- gera pendencia;
- recomenda ajuda Taliya.

Nao mostrar:

- termos tecnicos;
- pergunta sobre modo de fluxo;
- autonomia;
- configuracao profunda de agente.

## Criterios De Aceite

A imagem esta correta se:

- a pergunta parece simples;
- ha opcao de incerteza;
- mostra impacto sem poluir;
- funciona em varias paginas.

---

# PROMPT 52B - Card De Regra Por Area

Nome do arquivo final:

`52B_round-4.1J_onboarding_component_area-rule-card.png`

## Anexos Necessarios

Obrigatorios:

- `51A_round-4.1J_onboarding_asset_shell-base.png`.
- `A2 - Componentes de formulario`.

Opcional:

- `51C_round-4.1J_onboarding_asset_configuration-workspace.png`.

## Prompt Para ChatGPT

Crie um componente reutilizavel para cards de regra em paginas `/onboarding/configuracoes/[area]`.

Mostrar:

- nome da regra;
- status;
- valor atual em rascunho;
- impacto resumido;
- responsavel;
- acao `Editar`;
- acao `Marcar para depois`.

Exemplos de regras:

- `Prazo para avisar falta`;
- `Quem aprova excecoes`;
- `Janela de envio`;
- `Responsavel financeiro`.

Estados:

- rascunho;
- pronto;
- pronto parcialmente;
- pendente seguro;
- bloqueado;
- sensivel.

Nao mostrar:

- regra tecnica bruta;
- JSON;
- politica engine;
- builder.

## Criterios De Aceite

A imagem esta correta se:

- o card e reutilizavel;
- mostra status e impacto;
- nao parece configuracao tecnica demais.

---

# PROMPT 52C - Antes/Depois De Impacto

Nome do arquivo final:

`52C_round-4.1J_onboarding_component_before-after-impact.png`

## Anexos Necessarios

Obrigatorios:

- `51C_round-4.1J_onboarding_asset_configuration-workspace.png`.

Opcionais:

- `A3 - Overlays e feedback`.

## Prompt Para ChatGPT

Crie um componente reutilizavel para mostrar antes/depois de uma configuracao no Setup Inicial.

Nao chamar de simulacao.

Titulo do componente:

`Previa de impacto`

Mostrar:

- coluna `Antes`;
- coluna `Depois`;
- exemplo pratico;
- area afetada;
- alerta se houver risco;
- acao `Revisar regra`;

Exemplo:

- Antes: `Reposicao conferida manualmente`.
- Depois: `Sistema cria pendencia quando aluno avisa falta dentro do prazo`.

Nao mostrar:

- simulador tecnico;
- grafico complexo;
- automacao ativa.

## Criterios De Aceite

A imagem esta correta se:

- fica clara a mudanca;
- e simples;
- parece apoio de decisao, nao ferramenta tecnica.

---

# PROMPT 53A - Seletor De Fonte De Importacao

Nome do arquivo final:

`53A_round-4.1J_onboarding_import_source-selector.png`

## Anexos Necessarios

Obrigatorios:

- `51A_round-4.1J_onboarding_asset_shell-base.png`.
- `A6 - Objetos/setup/dados`.

Opcional:

- `51B_round-4.1J_onboarding_asset_agent-panel.png`.

## Prompt Para ChatGPT

Crie uma imagem de asset reutilizavel para a importacao do Setup Inicial do Taliya CRM.

Objetivo: desenhar o seletor de fonte de importacao.

Contexto:

- Studios podem ter dados em planilhas, agenda digital, sistema antigo, caderno, ficha, PDF, print ou anotacao.
- O agente ajuda a transformar esses dados em rascunho revisavel.
- O dono revisa antes de importar.

Mostrar opcoes:

- `Importar planilha`;
- `Conectar Google Agenda`;
- `Enviar foto ou PDF`;
- `Digitar manualmente`;
- `Comecar sem importar`.

Cada opcao deve mostrar:

- o que pode extrair;
- nivel de revisao esperado;
- aviso de privacidade quando necessario;
- acao principal.

Texto sugerido:

- `De onde vêm seus dados?`;
- `Voce pode importar agora ou completar depois`;
- `Fotos e PDFs viram rascunhos para revisar`;
- `Nada sera publicado sem sua confirmacao`.

Nao mostrar:

- importacao automatica sem revisao;
- promessa de acerto perfeito;
- linguagem OCR tecnica;
- dados sensiveis reais.

## Criterios De Aceite

A imagem esta correta se:

- mostra fontes digitais e fisicas;
- deixa claro que tudo vira rascunho;
- nao assusta o dono do studio;
- valoriza a ajuda do agente.

---

# PROMPT 53B - Tabela De Confianca Por Campo

Nome do arquivo final:

`53B_round-4.1J_onboarding_import_confidence-table.png`

## Anexos Necessarios

Obrigatorios:

- `51A_round-4.1J_onboarding_asset_shell-base.png`.
- `53A_round-4.1J_onboarding_import_source-selector.png`.
- `A6 - Objetos/setup/dados`.

Opcional:

- `A3 - Overlays e feedback`.

## Prompt Para ChatGPT

Crie uma imagem de asset reutilizavel para revisao de dados importados no Setup Inicial do Taliya CRM.

Objetivo: desenhar uma tabela de revisao com confianca por campo.

Contexto:

- O usuario enviou uma planilha, conectou uma agenda ou mandou foto/PDF/caderno.
- O agente ajudou a identificar dados.
- O sistema criou rascunhos.
- O dono precisa revisar antes de importar.

Tabela deve conter colunas:

- `Dado encontrado`;
- `Origem`;
- `Confianca`;
- `Sugestao do sistema`;
- `Campo editavel`;
- `Status`.

Exemplos de linhas:

- `Ana Paula` / `foto do caderno` / `alta` / `Aluno` / campo editavel / `Confirmado`;
- `Ter 8h` / `Google Agenda` / `alta` / `Turma Pilates Solo` / campo editavel / `Revisar`;
- `R$ 280` / `planilha` / `media` / `Mensalidade` / campo editavel / `Precisa revisar`;
- `Joao?` / `PDF escaneado` / `baixa` / `Nome incerto` / campo editavel / `Nao entendi`.

Estados de confianca:

- alta;
- media;
- baixa;
- precisa revisar;
- nao entendi;
- conflito;
- duplicidade provavel;
- dado sensivel.

Acoes:

- `Confirmar selecionados`;
- `Editar`;
- `Criar pendencia`;
- `Descartar sugestao`;
- `Importar parte segura`.

Nao mostrar:

- dados reais sensiveis;
- publicacao automatica;
- resolucao automatica de conflito;
- layout de planilha feia sem hierarquia.

## Criterios De Aceite

A imagem esta correta se:

- confianca por campo esta visivel;
- origem do dado esta clara;
- dono consegue revisar;
- ha importacao parcial segura;
- parece produto profissional, nao planilha crua.

---

# PROMPT 53C - Drawer De Conflito De Importacao

Nome do arquivo final:

`53C_round-4.1J_onboarding_import_conflict-drawer.png`

## Anexos Necessarios

Obrigatorios:

- `53B_round-4.1J_onboarding_import_confidence-table.png`.
- padrao herdado de drawer/modal existente.

Opcional:

- `A3 - Overlays e feedback`.

## Prompt Para ChatGPT

Crie um drawer reutilizavel para resolver conflito de importacao no Setup Inicial.

Contexto:

- A importacao encontrou dado duplicado, incerto ou contraditorio.
- O agente pode sugerir, mas o dono decide.

Tipos de conflito a representar:

- duplicidade;
- telefone compartilhado;
- aluno sem turma;
- turma sem horario;
- plano sem valor;
- status financeiro incerto;
- nome ilegivel;
- informacao contraditoria.

Layout:

- drawer lateral;
- titulo do conflito;
- origem dos dados;
- comparacao entre registro existente e sugestao importada;
- nivel de confianca;
- recomendacao do agente;
- acoes.

Acoes:

- `Aceitar sugestao`;
- `Editar`;
- `Mesclar`;
- `Manter separado`;
- `Criar pendencia`;
- `Descartar`.

Nao mostrar:

- decisao automatica sem dono;
- linguagem tecnica;
- erro fatal bloqueando tudo.

## Criterios De Aceite

A imagem esta correta se:

- o conflito e compreensivel;
- a decisao humana fica clara;
- existe saida segura para pendencia;
- nao bloqueia a importacao inteira.

---

# PROMPT 54A - Card De Agente Preparado

Nome do arquivo final:

`54A_round-4.1J_onboarding_agent-prepared-card.png`

## Anexos Necessarios

Obrigatorios:

- `51A_round-4.1J_onboarding_asset_shell-base.png`.
- `A4 - Comunicacao/agentes`.
- `A5 - Sistema/plano/governanca`.

Opcional:

- `51C_round-4.1J_onboarding_asset_configuration-workspace.png`.

## Prompt Para ChatGPT

Crie um card reutilizavel para representar agente preparado no Setup Inicial do Taliya CRM.

Contexto:

- O plano pode ter 0, 1, 3 ou 7 agentes.
- No setup inicial, agentes podem ser preparados, mas nao ficam ativos/rodando.
- Configuracao profunda fica para Agentes/Fluxos depois do go-live.

Mostrar:

- nome do agente;
- dominio;
- plano/slot;
- responsavel humano;
- status `Preparado`;
- pacotes recomendados em rascunho;
- destino pos-go-live.

Exemplos:

- `Agente Agenda`;
- `Responsavel: Mariana`;
- `Status: Preparado`;
- `2 pacotes em rascunho`;
- `Configurar depois em Agentes/Fluxos`.

Estados:

- nao incluso no plano;
- incluido mas nao preparado;
- preparado;
- rascunhos criados;
- pendente para Agentes/Fluxos;
- manual por enquanto.

Nao mostrar:

- ativo;
- rodando;
- autonomo;
- copiloto publicado;
- fluxo publicado;
- botao `Ativar autonomia`.

## Criterios De Aceite

A imagem esta correta se:

- fica impossivel confundir preparado com ativo;
- mostra responsavel humano;
- mostra rascunho/pendencia;
- aponta para pos-go-live sem pressionar o usuario.

---

# PROMPT 54B - Linha De Pacote Recomendado Em Rascunho

Nome do arquivo final:

`54B_round-4.1J_onboarding_agent-package-draft-row.png`

## Anexos Necessarios

Obrigatorios:

- `54A_round-4.1J_onboarding_agent-prepared-card.png`.

Opcional:

- padrao herdado de drawer/modal existente.

## Prompt Para ChatGPT

Crie um componente reutilizavel para linha de pacote recomendado de agente no Setup Inicial.

Mostrar:

- nome do pacote;
- area;
- motivo;
- responsavel;
- status `Rascunho`;
- destino pos-go-live;
- porque fica para depois.

Exemplo:

- pacote: `Reposicoes e encaixes`;
- area: `Agenda`;
- motivo: `Depende de regra de consumo e vaga real`;
- responsavel: `Mariana`;
- destino: `Agentes/Fluxos`;
- status: `Configurar depois`.

Nao mostrar:

- fluxo ativo;
- modo autonomo;
- publicacao;
- simulacao.

## Criterios De Aceite

A imagem esta correta se:

- parece item de rascunho;
- mostra motivo;
- mostra destino;
- nao parece automacao pronta.

---

# PROMPT 55A - Resumo De Camadas De Revisao/Publicacao

Nome do arquivo final:

`55A_round-4.1J_onboarding_review-layer-summary.png`

## Anexos Necessarios

Obrigatorios:

- `51A_round-4.1J_onboarding_asset_shell-base.png`.
- `51C_round-4.1J_onboarding_asset_configuration-workspace.png`.

Opcionais:

- `54A_round-4.1J_onboarding_agent-prepared-card.png`.

## Prompt Para ChatGPT

Crie um asset reutilizavel para a revisao e publicacao do Setup Inicial do Taliya CRM.

Objetivo: mostrar resumo das camadas que podem ser publicadas ou deixadas pendentes.

Camadas:

- `CRM manual`;
- `Agenda`;
- `Financeiro`;
- `Canais e modelos de mensagem`;
- `Regras de seguranca`;
- `Agentes preparados`;
- `Pendencias de Agentes/Fluxos`;

Estados:

- `Pronto agora`;
- `Publicado parcialmente`;
- `Pendente seguro`;
- `Configurar depois`;
- `Bloqueado`;
- `Revisar com Taliya`.

Cada camada deve mostrar:

- status;
- impacto;
- responsavel;
- se bloqueia publicacao;
- proxima acao.

Texto sugerido:

- `Revisao do setup`;
- `Publicar camadas seguras`;
- `Nada sera publicado sem sua confirmacao`;
- `Agentes ficam preparados, nao ativos`;
- `Pendencias ficam rastreaveis para depois`.

Nao mostrar:

- publicacao automatica pelo agente;
- autonomia;
- fluxo ativo profundo;
- logs.

## Criterios De Aceite

A imagem esta correta se:

- revisao e publicacao aparecem como uma experiencia;
- camadas estao claras;
- pendencias tem destino;
- agente nao parece executor;
- o usuario entende que pode abrir o CRM mesmo com pendencias seguras.

---

# PROMPT 55B - Confirmacao De Publicacao

Nome do arquivo final:

`55B_round-4.1J_onboarding_publish-confirmation-modal.png`

## Anexos Necessarios

Obrigatorios:

- `55A_round-4.1J_onboarding_review-layer-summary.png`.
- `A3 - Overlays e feedback`.

## Prompt Para ChatGPT

Crie um modal reutilizavel de confirmacao de publicacao para o Setup Inicial.

Mostrar:

- o que sera publicado;
- o que nao sera publicado;
- pendencias rastreaveis;
- confirmacao do gestor;
- auditoria;
- acao `Publicar camadas seguras`.

Estados:

- aguardando confirmacao;
- publicando;
- publicado;
- publicado parcialmente;
- falhou.

Texto sugerido:

- `Publicar camadas seguras?`;
- `O CRM manual ficara disponivel`;
- `Agentes continuarao preparados, nao ativos`;
- `Voce podera configurar fluxos depois`;
- `Confirmo e quero publicar`.

Nao mostrar:

- agente publicando sozinho;
- autonomia;
- irreversibilidade dramatica.

## Criterios De Aceite

A imagem esta correta se:

- a confirmacao e clara;
- mostra o que fica de fora;
- nao assusta;
- reforca auditoria e controle.

---

# PROMPT 55C - Estado De Sucesso

Nome do arquivo final:

`55C_round-4.1J_onboarding_success-state.png`

## Anexos Necessarios

Obrigatorios:

- `51A_round-4.1J_onboarding_asset_shell-base.png`.
- `55A_round-4.1J_onboarding_review-layer-summary.png`.

Opcional:

- `51B_round-4.1J_onboarding_asset_agent-panel.png`.

## Prompt Para ChatGPT

Crie um estado/modal de sucesso para o fim do Setup Inicial do Taliya CRM.

Mostrar:

- setup publicado;
- CRM pronto para abrir;
- resumo do que foi publicado;
- pendencias seguras;
- proximos passos;
- botao `Abrir CRM`;
- botao `Ver pendencias pos-go-live`;
- botao `Agendar ajuda Taliya`.

Estados possiveis:

- publicado completo;
- publicado parcialmente;
- publicado com pendencias de agentes;
- publicado sem agentes;
- publicado com importacao pendente.

Texto sugerido:

- `Setup inicial publicado`;
- `Seu CRM ja pode operar com seguranca`;
- `Alguns ajustes ficaram para depois`;
- `Abrir CRM`;
- `Ver pendencias`;
- `Configurar agentes depois`.

Nao mostrar:

- celebracao exagerada;
- hero marketing;
- agente autonomo;
- dashboard operacional.

## Criterios De Aceite

A imagem esta correta se:

- comunica sucesso com calma;
- mostra pendencias sem parecer falha;
- convida a abrir o CRM;
- nao parece landing page.

---

# Mapa De Anexos Por Asset

| Asset | Anexos obrigatorios | Anexos opcionais |
|---|---|---|
| 51A Shell base | A1, 51B aprovado | Visual DNA/Tokens |
| 51B Agente | 51A, A4 | A3 |
| 51C Configuracao central | 51A, 51B, A2, A3 | A5 |
| 51D Impacto | Nao gerar agora | Usar dentro das paginas finais quando necessario |
| 51E Pendencia | Nao gerar agora | Herdar drawer/modal existente |
| 51F Ajuda Taliya | 51A, A3 | 51B |
| 52A Pergunta guiada | 51A, A2 | 51B |
| 52B Regra por area | 51A, A2 | 51C |
| 52C Antes/depois | 51C | A3 |
| 53A Fonte importacao | 51A, A6 | 51B |
| 53B Confianca por campo | 51A, 53A, A6 | A3 |
| 53C Conflito importacao | 53B | A3, drawer/modal existente |
| 54A Agente preparado | 51A, A4, A5 | 51C |
| 54B Pacote rascunho | 54A | 51C |
| 55A Revisao camadas | 51A, 54A | 51C |
| 55B Confirmacao | 55A, A3 | nenhum |
| 55C Sucesso | 51A, 55A | 51B |

## Checklist Antes De Gerar Paginas Finais

Antes de gerar `/onboarding`, `/onboarding/diagnostico`, `/onboarding/setup` etc., os assets abaixo devem estar aprovados:

- 51A;
- 51B;
- 51C;
- 53A;
- 53B;
- 54A;
- 55A.

Sem esses assets, as paginas finais tendem a ficar inconsistentes.
