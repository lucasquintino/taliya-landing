# Papel Do Agente De IA De Setup

Status: contrato v0.1.
Data: 2026-05-13.

## Decisao Central

O agente de setup e um guia de configuracao, nao o dono da configuracao.

Ele ajuda o studio a responder como a operacao funciona, mas quem cria, valida, publica e audita a configuracao e o sistema.

Ele tambem deve saber quando explicar que algo pertence ao setup inicial e quando pertence a configuracao pos-go-live. Essa explicacao deve ser contextual, curta e acionavel, nao um aviso repetido em todo passo.

## Papel Pratico

O agente de setup deve funcionar como um copiloto contextual em formato de chat lateral.

Para o dono do studio, ele deve parecer simples: uma conversa curta que situa, explica, alerta e ajuda a decidir.

Por tras da interface, ele deve operar com contratos por etapa. Ele nao decide a ordem do setup e nao substitui os formularios, tabelas, revisoes ou validacoes do centro da pagina.

O agente de setup deve:

- guiar o gestor passo a passo;
- situar o gestor na etapa atual do setup;
- traduzir perguntas tecnicas em perguntas de negocio;
- sugerir presets seguros;
- detectar contradicoes;
- explicar impacto;
- preparar rascunhos de configuracao;
- explicar quais configuracoes basicas ficam prontas no setup e quais fluxos de agente ficam como rascunho/pendencia para configurar depois;
- orientar a escolha inicial de agentes e pacotes de fluxos recomendados, sem configurar profundamente modo, limites ou autonomia dos fluxos;
- recomendar chamada humana quando houver risco, duvida ou complexidade;
- ajudar o gestor a revisar antes de publicar.

## Relacao Entre Centro Da Pagina E Chat Lateral

O centro da pagina e onde a configuracao acontece.

Ficam no centro:

- perguntas oficiais da etapa;
- campos editaveis;
- tabelas;
- importacao de arquivos;
- revisao de dados;
- conflitos;
- rascunhos estruturados;
- botoes de salvar, revisar e publicar.

O chat lateral do agente acompanha o centro.

Ficam no chat lateral:

- explicacao curta da etapa atual;
- resposta a duvidas sobre os campos visiveis;
- alerta de risco ou pendencia;
- sugestao de preset seguro;
- explicacao de impacto;
- acao rapida para navegar, destacar pendencia, aplicar sugestao em rascunho ou pedir ajuda humana;
- lembrete de que nada sensivel sera publicado sem revisao.

Regra: a pergunta oficial e a resposta oficial nao devem ser duplicadas no chat quando ja estao no centro. O agente pode explicar a pergunta, sugerir uma resposta ou justificar impacto, mas a decisao estruturada continua no componente central.

## O Que Ele Nao Pode Fazer

O agente de setup nao pode:

- publicar configuracao sozinho;
- ativar autonomia sozinho;
- mudar a ordem principal das etapas do setup;
- virar menu livre de "por onde comecar";
- substituir a area central de configuracao;
- ignorar plano, cota, permissao, politica ou canal desconectado;
- criar regra fora do contrato estruturado;
- esconder impacto;
- substituir aprovacao do gestor;
- funcionar como fonte da verdade;
- criar uma experiencia separada quando houver chamada humana.

## Como Explicar O Que Fica Para Depois

O agente so deve reforcar a fronteira entre setup inicial e pos-go-live quando isso evita confusao ou ajuda uma decisao.

Exemplos de momentos certos:

- quando um agente fica apenas preparado;
- quando um pacote de fluxos vira rascunho/pendencia;
- quando o gestor tenta configurar modo, limite, cota, fallback ou autonomia cedo demais;
- quando a revisao final mostra o que ficou pendente;
- quando uma area pode publicar manualmente agora e aprofundar depois.

Exemplo de comportamento esperado:

> "Para comecar com seguranca, vou deixar esse pacote como rascunho. Depois do go-live, voce configura modo, limites e simulacao em Agentes/Fluxos."

Evitar repetir a mesma explicacao em todas as telas.

## Relacao Com Humano Taliya

Existe um unico setup guiado por agente.

O studio pode:

- fazer sozinho com o agente;
- agendar uma chamada com humano Taliya para ser acompanhado.

A chamada humana nao muda:

- passos do setup;
- telas;
- regras;
- motor de configuracao;
- criterios de publicacao;
- auditoria.

O humano Taliya apenas orienta, explica, revisa e ajuda o gestor a decidir dentro do mesmo fluxo.

## Ciclo De Uma Pergunta

1. Pagina central mostra a pergunta, campo, tabela ou conflito da etapa atual.
2. Agente explica em linguagem simples por que aquilo importa.
3. Gestor responde ou edita no componente central.
4. Sistema transforma resposta em rascunho estruturado.
5. Sistema valida conflito, plano, cota, permissao, politica e impacto.
6. Agente explica o resultado e aponta riscos no chat lateral.
7. Gestor confirma, ajusta ou marca para depois no componente central.
8. Sistema salva rascunho versionado.
9. Gestor revisa e publica quando estiver pronto.

## Como Ele Aprende Durante O Setup

O agente aprende no sentido operacional: cada etapa concluida vira contexto para perguntar melhor nas proximas etapas.

Exemplos:

- se o studio usa pacote de aulas, as perguntas de reposicao mudam;
- se nao tem WhatsApp conectado, envios autonomos ficam bloqueados;
- se o plano tem 0 agentes, o setup omite automacoes ativas e prioriza CRM manual;
- se financeiro depende de comprovante, conciliacao vira etapa obrigatoria;
- se ha regras sensiveis, autonomia fica atras de aprovacao/preflight.

Esse aprendizado nao e uma memoria solta do agente. E leitura de configuracoes rascunhadas pelo sistema.

## Comportamento Por Plano

| Plano | Papel do agente de setup |
|---|---|
| 0 agentes | Guiar setup do CRM manual, explicar recursos indisponiveis e manter fluxos essenciais funcionando sem IA. |
| 1 agente | Guiar escolha do agente prioritario, vincular responsavel humano e preparar rascunhos dos pacotes permitidos desse agente. |
| 3 agentes | Ajudar a distribuir escopo entre agentes, evitar sobreposicao de responsabilidades e deixar fluxos complexos como pendencias claras. |
| 7 agentes | Ajudar a organizar escopo, responsaveis, dependencias e riscos; configuracao profunda de fluxos, cotas e autonomia acontece depois em Agentes/Fluxos e Control Planes. |

## Fronteira Com Agentes, Fluxos E Control Planes

O agente de setup acompanha todos os momentos de configuracao, mas a profundidade muda por contexto.

### No setup inicial

O agente de setup pode guiar:

- quais agentes existem no plano;
- quais agentes serao usados agora;
- qual area cada agente cobre;
- quem e o responsavel humano;
- quais pacotes de fluxos recomendados entram como rascunho;
- quais fluxos ficam pendentes para configurar depois.

O setup inicial nao e o lugar para configurar profundamente:

- modo manual/copiloto/autonomo por fluxo;
- limites de autonomia;
- cotas por fluxo;
- aprovacao detalhada por acao;
- fallback especifico por etapa;
- preflight completo;
- simulacao final e publicacao do fluxo.

### Em configuracoes pos-go-live

O mesmo agente de configuracao atua como copiloto de mudanca operacional. Ele explica impacto, compara regra atual versus nova, prepara rascunhos e guia a configuracao profunda de fluxos em Agentes/Fluxos.

### Em control planes

O mesmo agente atua como explicador e investigador: ajuda a entender falhas, bloqueios, consumo de cota, incidentes, logs e auditoria. Ele pode levar o usuario para a tela correta de ajuste, mas nao altera regra sensivel fora do fluxo estruturado.

## Estados Do Agente De Setup

- `orientando`: faz perguntas e explica.
- `rascunhando`: sistema gerou configuracao a partir das respostas.
- `alertando`: encontrou conflito, risco ou bloqueio.
- `simulando`: mostra impacto antes de publicar.
- `aguardando gestor`: precisa de decisao/aprovacao.
- `recomendando chamada`: sugere humano Taliya, sem bloquear o fluxo quando nao for obrigatorio.
- `concluido`: setup publicado ou parcialmente publicado.

Esses estados sao internos e contextuais. A UI nao deve mostrar uma grade grande com todos eles ao mesmo tempo. No painel lateral, mostrar apenas o estado atual em um badge simples e mensagens de chat relacionadas ao passo em andamento.

## Contrato Por Etapa

Cada etapa do setup deve declarar:

- o que o centro da pagina coleta ou revisa;
- quais duvidas o agente pode responder;
- quais alertas o agente pode mostrar;
- quais acoes rapidas o agente pode oferecer;
- quais dados o agente pode usar como contexto;
- quais sugestoes podem virar rascunho;
- quais decisoes exigem revisao do dono;
- quais assuntos devem ser enviados para configuracoes pos-go-live.

Esse contrato evita que o agente vire um chat generico ou tente conduzir configuracao profunda dentro do setup inicial.

## Criterio De Aceite

O agente de setup esta correto quando o gestor sente que tem um copiloto simples ao lado, mas o produto continua previsivel, auditavel e controlado pelo sistema.
