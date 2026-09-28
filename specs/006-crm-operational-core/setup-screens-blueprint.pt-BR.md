# Setup E Configuracoes - Blueprint De Telas

Status: blueprint v0.1.
Data: 2026-05-13.

## Objetivo

Definir como o usuario configura o Taliya de forma pratica, simples e eficaz, sem transformar configuracao em uma parede tecnica.

## Principio de UX

O usuario nao "configura um motor". Ele responde como o studio funciona.

O sistema transforma essas respostas em configuracao estruturada, valida, mostra impacto e publica com aprovacao.

O onboarding deve deixar claro que e uma configuracao inicial quando isso ajuda a decisao do usuario. Essa clareza deve aparecer de forma contextual, nao como aviso repetido em toda tela.

## Estrutura macro

### Setup inicial

Rotas propostas:

| Rota | Proposito | Observacao |
|---|---|---|
| `/onboarding` | Primeiro passo pos-pagamento e retomada do setup interrompido. | No primeiro acesso, mostra a imagem 78: boas-vindas, nome do studio e Agente de Configuracao. Depois segue para o bloco `Studio` sem repetir o nome como campo principal. |
| `/onboarding/diagnostico` | Entender apenas o necessario para orientar defaults e proximos blocos. | Perguntas de porte, origem dos dados, tipos de planos oferecidos e como o studio lida com reposicoes. |
| `/onboarding/setup` | Configurar somente o essencial operacional. | Blocos curtos: Studio, Equipe, Agenda base, Canais e defaults informativos. Planos e consumo ficam na rota especifica de consumo de aulas. Nao e hub de configuracoes. |
| `/onboarding/importacao` | Trazer e revisar dados reais quando chegar nessa etapa. | Importacao sempre por dominio, uma por vez: alunos, agenda, turmas, planos, contatos ou financeiro basico. |
| `/onboarding/configuracoes/consumo-aulas` | Criar planos e configurar consumo/reposicao por plano. | O studio pode ter varios planos. Cada plano recebe configuracao propria de modelo, direito de aula, validade, consumo e reposicao. |
| `/onboarding/revisao` | Revisar e publicar o setup inicial com seguranca. | Mostra publicado agora, pendente seguro, bloqueado e pos-go-live. Publicacao pode ser estado interno desta rota. |
| `/onboarding/publicacao` | Opcional, apenas se a publicacao exigir tela propria. | Usar quando houver muitos estados de validacao, erro, auditoria ou confirmacao final. Caso contrario, fica dentro de `/onboarding/revisao`. |
| `/onboarding/concluido` | Opcional, estado final apos publicacao. | Pode ser rota, modal ou estado dentro de revisao; orienta entrada no CRM e proximos ajustes pos-go-live. |

Rota removida como conceito aberto:

| Rota | Decisao |
|---|---|
| `/onboarding/configuracoes/[area]` | Nao deve ser uma area livre para o cliente configurar qualquer dominio. Se existir tecnicamente, deve aceitar apenas areas liberadas pelo diagnostico e pelo contrato de escopo do Setup Inicial. |

## Detalhamento Das Paginas Do Setup Inicial

### `/onboarding`

Fluxo:

1. Usuario chega apos assinatura confirmada, normalmente vindo da imagem 77.
2. Tela mostra a imagem 78, com boas-vindas e pergunta apenas o nome do studio.
3. Usuario responde.
4. Sistema cria/identifica o espaco operacional do studio.
5. Agente de Configuracao ja aparece como guia lateral.
6. Agente da boas-vindas e explica:
   - vou te guiar pelo setup inicial;
   - vou sugerir defaults seguros;
   - o que for avancado fica para depois do go-live.

Se o usuario ja tinha iniciado o setup, a rota mostra retomada e proxima etapa. Se o setup ja foi publicado, redireciona para o CRM.

Contrato de handoff aprovado:

- [subscription-to-onboarding-handoff-audit.pt-BR.md](./subscription-to-onboarding-handoff-audit.pt-BR.md)

### `/onboarding/diagnostico`

O diagnostico nao configura. Ele apenas prepara defaults e decide visibilidade/ordem dos blocos.

Contrato detalhado aprovado:

- [setup-diagnostico-page-contract.pt-BR.md](./setup-diagnostico-page-contract.pt-BR.md)

Comportamento:

- uma pergunta por vez;
- opcoes em cards;
- progresso `Pergunta X de 5`;
- botao `Continuar` ativo apenas depois da resposta;
- resumo final;
- CTA `Continuar para o setup`.

Perguntas aprovadas:

- Quantos alunos ativos o studio tem hoje?
- Onde estao agenda, turmas ou horarios hoje?
- Onde estao alunos, planos e contatos hoje?
- Quais tipos de planos o studio oferece pro aluno?
- Como o studio lida com reposicoes?

Nao perguntar:

- se usa WhatsApp;
- se quer importar agora;
- se trabalha com horario fixo;
- se o plano tem agentes;
- quantas pessoas vao usar o Taliya;
- quais areas quer configurar primeiro.

### `/onboarding/setup`

O setup essencial e uma pagina de blocos curtos. Cada bloco salva rascunho, usa default seguro e deixa ajustes finos para depois.

Bloco `Studio`:

- nome do studio ja informado na imagem 78 e exibido no header/topo, sem repetir como campo principal;
- dias de funcionamento;
- horario geral de funcionamento;
- pausa/intervalo quando existir;
- previa da grade semanal;
- ajuste de horarios por dia quando necessario;
- unidade principal, se necessario;
- WhatsApp principal do studio;
- se houver mais de uma unidade, permitir adicionar unidade minima.

Bloco `Equipe`:

- dono/admin ja preenchido;
- adicionar pessoas que precisam acessar agora;
- papel simples: dono/admin, recepcao, professor, financeiro;
- permissoes finas ficam para pos-go-live.

Bloco `Agenda base`:

- tipos de aula;
- escolha operacional: cadastrar grade minima agora ou deixar para importacao;
- se cadastrar agora, apenas turma/aula, professor quando houver, dias/horarios e capacidade;
- horario fixo/turma recorrente e comportamento padrao do sistema, nao uma configuracao conceitual.

Bloco `Canais`:

- WhatsApp principal;
- conectar agora ou deixar manual;
- modelos, tom de voz, campanhas e automacao ficam para pos-go-live.

Bloco `Defaults e agentes`:

- mostra que tarefas, aprovacoes simples, auditoria e papeis padrao foram preparados automaticamente;
- mostra agentes do plano apenas como informacao/default, sem configuracao de fluxo;
- cria pendencias pos-go-live quando aplicavel.

### `/onboarding/importacao`

A importacao e sempre uma por vez.

Dominios possiveis:

- alunos;
- contatos/responsaveis;
- agenda;
- turmas;
- planos;
- financeiro basico.

Fluxo de cada importacao:

1. escolher dominio;
2. escolher fonte;
3. enviar arquivo, conectar fonte ou usar foto/PDF/print/caderno;
4. sistema extrai rascunho;
5. cada campo mostra origem e confianca;
6. usuario revisa;
7. sistema mostra duplicidades e conflitos;
8. usuario aprova, corrige, descarta ou deixa pendente;
9. so depois pode iniciar outra importacao.

### `/onboarding/configuracoes/consumo-aulas`

Esta pagina nao configura um unico modelo global para todo mundo.

Ela tem dois niveis:

1. default do studio, usado para preencher planos novos;
2. configuracao individual de cada plano.

Nivel do studio:

- modelo mais comum: mensalidade, pacote, hibrido ou avulso;
- reposicao padrao ligada/desligada;
- prazo padrao de reposicao;
- regra padrao de consumo.

Nivel de cada plano:

- nome do plano;
- tipo do plano;
- aulas por ciclo/pacote;
- validade/ciclo;
- valor, se o financeiro minimo estiver no setup;
- quando a aula e consumida;
- se permite reposicao;
- prazo de reposicao daquele plano;
- excecoes simples daquele plano.

O usuario pode criar varios planos e configurar cada um separadamente. Exemplo: `Mensal 2x semana`, `Pacote 8 aulas`, `Experimental`, `Avulsa`.

### Configuracoes depois do go-live

Rotas propostas:

| Rota | Proposito | Observacao |
|---|---|---|
| `/app/configuracoes` | Hub de configuracoes. | Entrada por area, status e pendencias. |
| `/app/configuracoes/studio` | Dados do studio, unidades, horarios e identidade. | Base operacional. |
| `/app/configuracoes/agenda` | Regras de agenda, aulas, turmas, chamada e no-show. | Nao duplica tela operacional de Agenda. |
| `/app/configuracoes/agenda/consumo-aulas` | Modelo de consumo, creditos e reposicoes. | Critico para "quebra-galho" e encaixes. |
| `/app/configuracoes/financeiro` | Cobrancas, vencimentos, meios de pagamento e conciliacao. | Separado de billing Taliya. |
| `/app/configuracoes/financeiro/modelos` | Modelos de cobranca do aluno. | Mensalidade, pacote, hibrido, avulso. |
| `/app/configuracoes/canais` | WhatsApp, email e canais internos. | Conexao e status. |
| `/app/configuracoes/templates` | Mensagens, modelos e comunicados. | Governanca de templates. |
| `/app/configuracoes/equipe` | Usuarios e papeis. | Equipe do studio. |
| `/app/configuracoes/permissoes` | Permissoes por papel e acao sensivel. | RBAC operacional. |
| `/app/configuracoes/notificacoes` | Alertas, canais internos e preferencias. | Quem recebe o que. |
| `/app/agentes` | Estado dos agentes, agentes contratados, areas cobertas e responsaveis. | Configuracao pos-go-live dos agentes. |
| `/app/agentes/[agentId]/fluxos` | Lista de fluxos vinculados a um agente. | Entrada para configurar fluxos. |
| `/app/agentes/[agentId]/fluxos/[flowId]` | Configuracao profunda do fluxo do agente. | Gatilho, condicao, acao, modo, limites, aprovacao, fallback, simulacao e publicacao. |

### Control planes relacionados

Estas rotas nao sao setup nem formulario de configuracao basica. Elas servem para governar execucao, risco, uso e auditoria do sistema em producao:

| Rota | Papel |
|---|---|
| `/app/agentes` | Estado dos agentes, fluxos, execucoes recentes, pausas emergenciais e riscos operacionais. |
| `/app/fluxos/execucoes/[runId]` | Detalhe de execucao, traces seguros, falhas, ferramentas, cota, erro e fallback manual. |
| `/app/operacao/incidentes` | Incidentes, bloqueios, riscos e problemas recorrentes. |
| `/app/operacao/incidentes/[incidentId]` | Causa, impacto, linha do tempo, correcao, prevencao e auditoria do incidente. |
| `/app/uso` | Cotas, uso, economia e limites. |
| `configuracao especifica da integracao` | Status, conexoes e falhas de integracao. |
| `/app/auditoria` | Logs, execucoes e trilhas de decisao. |

Regra:

- `/app/controle/*` era uma nomenclatura conceitual antiga e nao deve ser usada como rota final no MVP;
- Control Plane nao e builder de fluxo, configuracao pos-go-live nem setup;
- detalhes finais ficam em `control-planes-master-map.pt-BR.md`.

## Layout do setup principal

### Zona esquerda

Checklist de progresso:

- Diagnostico;
- Essenciais;
- Importacao;
- Consumo de aulas;
- Revisao e publicacao.

Cada item mostra:

- status;
- pendencias;
- bloqueio;
- se pode continuar ou precisa revisar.

Regra: o checklist/stepper nao deve virar menu de configuracoes. Ele mostra a sequencia obrigatoria do Setup Inicial, nao todas as areas configuraveis do CRM.

### Zona central

Area operacional da etapa atual.

E aqui que a configuracao real acontece.

Pode conter:

- perguntas oficiais;
- campos editaveis;
- seletores;
- tabelas;
- importacao de arquivos;
- revisao de dados encontrados;
- conflitos;
- rascunhos estruturados;
- impacto curto quando a etapa exigir;
- acoes de salvar, revisar, marcar para depois e publicar.

Nao deve conter:

- configuracoes avancadas;
- todas as opcoes existentes no CRM;
- permissoes finas;
- templates completos;
- fluxos de agente;
- cotas por fluxo;
- logs, traces ou auditoria operacional.

Exemplo correto:

- o centro pergunta como o studio lida com reposicao;
- o agente lateral explica por que isso importa;
- o usuario responde no centro;
- sistema preenche uma regra em rascunho;
- usuario edita em campos claros;
- sistema valida.

### Zona direita

Chat lateral do agente de configuracao:

- situa o usuario na etapa atual;
- explica campos e decisoes;
- responde duvidas sobre o que esta visivel no centro;
- alerta riscos, bloqueios e pendencias;
- sugere presets seguros;
- explica `pronto agora` versus `configurar depois` quando isso ajuda a decisao;
- recomenda ajuda humana Taliya quando fizer sentido.

O chat lateral pode explicar impacto, mas nao deve virar dashboard, formulario, lista de proximos passos ou area de pendencias.

Regra: nao duplicar no chat a pergunta oficial que ja esta no centro. O agente pode explicar, sugerir e orientar, mas a resposta estruturada fica no centro.

## Contrato Do Chat Lateral Por Pagina

Este contrato evita que o agente tente fazer tudo dentro do chat.

| Pagina | Centro da pagina | Chat lateral do agente |
|---|---|---|
| `/onboarding` | Imagem 78 com boas-vindas e campo unico de nome do studio. | Ja aparece como guia lateral; explica que identifica o studio e depois conduz dados principais, equipe, canais, planos, alunos, turmas e agenda. |
| `/onboarding/diagnostico` | Perguntas de porte/origem de dados: alunos ativos, fontes de agenda, fontes de alunos/planos, tipos de planos oferecidos e reposicoes. | Explica que isso serve para preparar defaults, nao para configurar tudo. |
| `/onboarding/setup` | Blocos essenciais: Studio, Equipe, Agenda base, Canais, Defaults/agentes informativos. Planos ficam em Consumo de aulas. | Orienta o passo atual, explica defaults, destaca bloqueios e lembra o que fica para configuracao pos-go-live. |
| `/onboarding/importacao` | Uma importacao por vez: dominio, fonte, upload/conexao/foto, confianca, revisao, conflitos e aprovacao. | Explica o que foi identificado, o que precisa revisao, como resolver conflitos e quando pedir ajuda humana. |
| `/onboarding/configuracoes/consumo-aulas` | Lista de planos + configuracao individual de cada plano: tipo, aulas, validade, consumo e reposicao. | Explica impacto em agenda, cobranca, saldo e reposicoes; alerta quando uma excecao deve virar pendencia. |
| `/onboarding/revisao` | Checklist final, pronto para publicar, pendente seguro, bloqueado, rascunho para depois e botao de publicar. | Resume riscos, explica pendencias, reforca publicacao parcial segura e aponta o destino pos-go-live quando houver. |
| `/onboarding/publicacao` | Validacao final, confirmacao, erros de publicacao, auditoria inicial e resultado. | Explica estados de publicacao, orienta correcao de erro e confirma o que foi publicado ou ficou pendente. |
| `/onboarding/concluido` | Confirmacao, entrada no CRM, proximos ajustes e pendencias pos-go-live. | Explica que o CRM ja pode operar e que ajustes profundos de agentes/fluxos ficam depois em Agentes/Fluxos. |

Regras para todas as paginas:

- o chat nunca vira formulario principal;
- o chat nunca muda a ordem das etapas;
- o chat nunca publica sozinho;
- o chat pode gerar sugestao ou rascunho, mas o centro mostra e o dono revisa;
- o chat responde duvidas sobre a etapa atual e pode explicar o que vem depois sem abrir configuracao avancada ali.

## Layout De Configuracao Essencial

O Setup Inicial nao deve abrir todas as configuracoes por area.

Quando uma configuracao aparecer no onboarding, ela deve seguir o mesmo padrao:

- titulo simples;
- status da area;
- poucos cards de regras principais;
- campos minimos;
- presets visiveis quando ajudarem;
- validacao inline;
- pendencias simples;
- botao `Salvar rascunho`;
- botao `Continuar`;
- botao `Configurar depois`, apenas quando isso for seguro.

As telas do onboarding nao devem tentar substituir `/app/configuracoes/*`. No onboarding, cada bloco so coleta o minimo para publicar o CRM com seguranca. Ajustes completos, regras finas e mudancas depois do go-live pertencem as configuracoes do app.

Na UI, evitar termos tecnicos quando houver equivalente operacional:

- usar `Rotinas operacionais` em vez de `Fluxos CRM`;
- usar `Regras de seguranca`, `Aprovacoes` e `Excecoes` em vez de `Politicas`, quando for texto para o gestor;
- usar `Previa de impacto` em vez de `Simulacao`, exceto nas telas pos-go-live de Agentes/Fluxos ou Politicas.

## Pendencias rastreaveis

Toda pendencia criada no setup deve virar objeto rastreavel, nao apenas texto na tela.

Cada pendencia deve guardar:

- titulo;
- area;
- motivo;
- responsavel;
- destino correto para continuar;
- prioridade;
- se bloqueia publicacao ou nao;
- camada afetada;
- data/criador;
- status.

Exemplos de destino:

- `/app/agentes/[agentId]/fluxos` para configuracao profunda de fluxo;
- `/app/configuracoes/financeiro` para ajuste financeiro pos-go-live;
- `/app/dados/qualidade` ou area equivalente para conflitos de importacao;
- `configuracao especifica da integracao` para canal desconectado;
- `/app/politicas` para regra de seguranca versionada.

## Canais e agentes

Conectar canal ou aprovar modelo de mensagem no setup nao significa que automacao esta pronta.

A interface deve separar:

- canal conectado;
- modelo/manual de mensagem pronto;
- envio manual permitido;
- pacote de agente em rascunho;
- automacao externa pendente para Agentes/Fluxos.

## Importacao assistida pelo agente

O setup deve aceitar dados reais do jeito que studios pequenos normalmente tÃªm, sem exigir organizacao perfeita antes de comecar.

Entradas permitidas:

- planilha Excel, CSV ou Google Sheets exportado;
- exportacao de sistema antigo;
- Google Agenda ou agenda externa conectada;
- PDF ou documento escaneado;
- foto de caderno, ficha, quadro, lista impressa ou anotacao manual;
- print de conversa/lista quando o usuario tiver permissao para usar;
- digitacao manual assistida.

Fluxo correto:

1. Usuario envia arquivo, conecta fonte ou tira foto.
2. Agente explica o que conseguiu identificar.
3. Sistema cria rascunho estruturado.
4. Cada campo mostra origem e nivel de confianca.
5. Dono revisa, corrige ou descarta.
6. Sistema valida duplicidades, conflitos e campos obrigatorios.
7. Apenas dados aprovados entram na publicacao/importacao.
8. Dado duvidoso vira pendencia rastreavel.

Campos extraidos podem incluir:

- aluno;
- responsavel/contato;
- telefone;
- turma;
- horario;
- professor;
- plano;
- status financeiro;
- saldo/credito;
- observacao;
- origem do dado.

Estados de confianca:

- confianca alta;
- precisa revisar;
- nao entendi;
- conflito com dado existente;
- duplicidade provavel;
- dado sensivel, exige confirmacao.

Regra: o agente ajuda a ler e organizar, mas nao chuta dado ambÃ­guo e nao publica importacao sem revisao do dono.

## Chamada humana Taliya

A chamada humana nao cria outra experiencia.

Quando agendada, a tela mostra apenas:

- card com horario da chamada;
- resumo para o especialista;
- pendencias que devem ser discutidas;
- link para entrar na chamada;
- anotacoes/recomendacoes feitas durante a chamada.

O fluxo, as regras e a publicacao continuam iguais.

## Agente de configuracao transversal

O mesmo agente de IA de configuracao deve estar presente em tres momentos, com papeis diferentes:

| Momento | Papel do agente | Limite |
|---|---|---|
| Setup inicial | Guia implantacao, explica perguntas, sugere presets e prepara rascunhos. | Nao configura profundamente fluxo de agente. |
| Configuracoes pos-go-live | Ajuda a alterar regras de um sistema ja rodando e guia configuracao profunda de fluxos em Agentes/Fluxos. | Nao publica regra sensivel sem validacao, impacto e aprovacao. |
| Control planes | Explica falhas, bloqueios, cotas, incidentes e auditoria. | Nao substitui builder de fluxo; leva o usuario para a tela correta de ajuste. |

Regra: o agente conversa e orienta; o sistema estrutura, valida, publica e audita.

No setup inicial, essa conversa deve aparecer como chat lateral contextual. Ele nao e um atendimento generico, nao e um menu de etapas e nao e a area principal de configuracao.

Padrao visual/comportamental do chat:

- cabecalho compacto com `Agente de configuracao` e status atual;
- mensagens curtas do agente;
- baloes de explicacao e alerta;
- perguntas sugeridas quando ajudarem o usuario a tirar duvidas;
- campo `Pergunte sobre esta etapa...`;
- ajuda humana discreta;
- no maximo um alerta principal por vez.

Exemplos de mensagens:

> "Estamos na etapa Dados do studio. Vou marcar o que e obrigatorio para publicar e o que pode ficar para depois."

> "Essa escolha afeta agenda, reposicoes e cobranca. Se houver excecao, podemos salvar como pendencia segura."

> "Isso fica em Agentes/Fluxos depois do go-live. Aqui vou preparar apenas o rascunho inicial."

## Estados essenciais

- Nao iniciado.
- Em entrevista.
- Dados pendentes.
- Rascunho gerado.
- Validando.
- Pronto para revisar.
- Chamada Taliya agendada.
- Em revisao com Taliya.
- Aguardando aprovacao do gestor.
- Publicado.
- Publicado parcialmente.
- Bloqueado por risco.
- Bloqueado por plano/cota.
- Reconfiguracao em rascunho.

## Regras de simplificacao

- Nao mostrar configuracoes avancadas antes de resolver o basico.
- Usar presets para reduzir perguntas.
- Mostrar exemplos reais do studio sempre que possivel.
- Explicar impacto antes de pedir aprovacao.
- Explicar "pronto agora" versus "configurar depois" apenas quando houver risco de confusao ou decisao pendente.
- Permitir publicar CRM manual antes de agentes.
- Nao configurar profundamente fluxo de agente dentro do setup inicial.
- Deixar claro quando um agente foi apenas preparado e quando um fluxo ainda precisa configuracao pos-go-live.
- Nao misturar setup inicial com operacao diaria.
- Nao esconder bloqueios criticos em tooltip.

## Clareza contextual sobre o que fica para depois

Nao usar banner permanente dizendo que o setup e inicial.

Mostrar a fronteira apenas nos momentos em que ela muda a decisao:

- na entrada do onboarding, uma frase curta de enquadramento;
- no setup principal, painel de impacto com `pronto agora` e `para depois`;
- em configuracao por area, aviso somente se a area deixar algo avancado para pos-go-live;
- em agentes, indicar quando agente ficou preparado e fluxos ficaram em rascunho/pendencia;
- na revisao/publicacao, lista objetiva de publicado agora, publicado parcialmente, pendente seguro e configurar depois.

O agente de configuracao deve explicar isso do mesmo jeito: contextual, curto e ligado ao passo atual.

## O que nao deve existir no MVP

- duas experiencias separadas de setup;
- tela tecnica de regras brutas;
- agente publicando configuracao sozinho;
- humano Taliya configurando por fora;
- dependencia de IA para ativar CRM;
- rota separada para cada micro-regra.
