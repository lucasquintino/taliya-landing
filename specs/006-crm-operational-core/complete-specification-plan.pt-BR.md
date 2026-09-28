# Plano concreto para arquitetura funcional e especificacao 100% - PT-BR

> Status: plano operacional. Este documento define as rodadas necessarias para sair do mapa atual e chegar em arquitetura funcional completa e especificacao profunda de web, app mobile, fluxos, casos de uso, permissoes, IA, cotas e auditoria.

## Objetivo

Sair do estado atual:

```text
mapa de produto coerente
web/mobile separados
38 paginas web
51 telas mobile
157 casos de uso
96 fluxos fortes de agentes
2 fluxos opcionais em decisao
```

Para o estado final:

```text
toda area do produto com arquitetura funcional definida
toda pagina/tela especificada
toda rota com dona
todo caso de uso coberto
todo fluxo com caminho manual/copiloto/autonomo
toda tela com conteudo, blocos, campos, botoes, estados e regras definidos
toda acao sensivel com permissao, cota, auditoria e fallback
todo objeto de negocio com ciclo de vida e fonte da verdade
toda politica operacional versionada quando afetar agente, regra ou decisao sensivel
todo caminho critico funcionando sem agentes ativos
toda integracao critica com comportamento de falha definido
todo suporte interno da Taliya com acesso, limite e auditoria definidos
nenhuma duplicidade importante
nenhuma lacuna invisivel
```

## Definicao de 100%

Nesta fase, "100%" significa pronto para design detalhado, prototipo navegavel, planejamento tecnico e implementacao planejada.

Nao significa codigo pronto.

Significa que, para cada area do produto, sabemos:

- quais objetos de negocio existem;
- quais jornadas entram e saem da area;
- quais regras de negocio mandam no comportamento;
- quais telas web e mobile sustentam a operacao;
- quais dados sao fonte de verdade;
- quais acoes sao manuais, com copiloto ou autonomas;
- quais integracoes, agentes, cotas, permissoes e auditorias participam;
- quais objetos de negocio existem e qual o ciclo de vida deles;
- qual sistema/tela/processo e fonte da verdade para cada dado;
- quais politicas operacionais afetam a area;
- como a area funciona no plano base com 0 agentes;
- como a area se comporta em falha, dado incompleto, integracao indisponivel ou limite de cota;
- quais metricas provam que a area esta funcionando;
- quais dependencias existem com outras areas;
- quais decisoes ainda estao abertas.

E, para cada tela/pagina/fluxo relevante, sabemos:

- para que existe;
- quem usa;
- qual rota/tela abre;
- quais dados mostra;
- quais campos edita;
- quais botoes existem;
- onde cada botao fica;
- qual acao cada botao executa;
- quais estados existem;
- quais permissoes aplicam;
- onde a IA aparece;
- quando consome cota;
- o que audita;
- qual fallback existe;
- qual equivalente web/mobile existe;
- quais casos de uso cobre;
- quais decisoes ainda foram conscientemente deixadas abertas.

## Artefatos finais obrigatorios

Ao final das rodadas, estes documentos devem existir:

| Documento | Papel |
| --- | --- |
| `functional-architecture.pt-BR.md` | Arquitetura funcional por area: objetos, jornadas, regras, dependencias e modos de operacao. |
| `canonical-data-model.pt-BR.md` | Objetos centrais, campos, relacoes, dados sensiveis e donos do dado. |
| `object-lifecycle-map.pt-BR.md` | Ciclo de vida de interessado, aluno, turma, aula, reposicao, pagamento, contrato, tarefa, caso, conversa, agente e execucao. |
| `source-of-truth-matrix.pt-BR.md` | Fonte da verdade por dado: CRM, agenda, financeiro, WhatsApp, integracao, importacao ou usuario. |
| `operational-policy-versioning.pt-BR.md` | Politicas de reposicao, cobranca, cancelamento, encaixe, comunicados, descontos, autonomia e escalonamento. |
| `integration-failure-contracts.pt-BR.md` | Contratos de integracao e comportamento quando WhatsApp, pagamento, calendario, importacao ou webhook falhar. |
| `zero-agent-operating-model.pt-BR.md` | Como o CRM funciona no plano base com 0 agentes ativos. |
| `agent-quality-evaluation.pt-BR.md` | Como medir acerto, erro, correcao, risco, economia e confianca dos agentes. |
| `migration-import-plan.pt-BR.md` | Entrada de studios vindos de planilha, sistema antigo, agenda manual ou base incompleta. |
| `taliya-internal-ops.pt-BR.md` | Operacao interna da Taliya: tenants, suporte, acesso autorizado, incidentes, planos e bloqueios. |
| `product-success-metrics.pt-BR.md` | Metricas de valor: ocupacao, conversao, faltas, inadimplencia, retencao, tempo economizado e risco reduzido. |
| `notification-template-governance.pt-BR.md` | Modelos de mensagem, notificacoes, consentimento, aprovacao, versao e canal. |
| `screen-specs-detailed.pt-BR.md` | Especificacao detalhada tela a tela. |
| `chatgpt-screen-generation-prompts.pt-BR.md` | Pacote de prompts para gerar paginas web e telas mobile no ChatGPT usando as referencias visuais aprovadas. |
| `route-screen-coverage.pt-BR.csv` | Toda rota ligada a pagina/tela dona. |
| `use-case-to-screen-coverage.pt-BR.csv` | Todo caso de uso ligado a tela, modo e fallback. |
| `agent-flow-screen-coverage.pt-BR.csv` | Todo fluxo de agente ligado a tela, gatilho, modo e auditoria. |
| `permissions-matrix.pt-BR.md` | Permissoes por papel e acao sensivel. |
| `action-button-taxonomy.pt-BR.md` | Padrao de botoes, acoes e confirmacoes. |
| `ui-state-taxonomy.pt-BR.md` | Estados globais: vazio, erro, bloqueado, sem permissao, cota, agente pausado. |
| `quota-touchpoints.pt-BR.md` | Onde cota aparece e muda comportamento. |
| `audit-touchpoints.pt-BR.md` | O que gera auditoria e como aparece. |
| `open-product-decisions.pt-BR.md` | Decisoes restantes, dono, impacto e status. |
| `final-consistency-audit.pt-BR.md` | Checagem final de cobertura e contradicoes. |

## Dimensoes que nao podem ficar implicitas

Cada rodada deve preencher, quando aplicavel, estas dimensoes. Se uma dimensao nao se aplicar, o documento deve dizer "nao se aplica" e explicar por que.

| Dimensao | Pergunta obrigatoria |
| --- | --- |
| Dados | Quais objetos, campos, relacoes e dados sensiveis existem aqui? |
| Ciclo de vida | Como o objeto nasce, muda, pausa, conclui, cancela, reabre ou arquiva? |
| Fonte da verdade | Quem manda no dado quando existem CRM, WhatsApp, integracao, importacao e edicao manual? |
| Plano 0 agentes | Como o gestor resolve isso sem nenhum agente ativo? |
| Manual/copiloto/autonomo | O que e humano, o que a IA prepara e o que a IA pode executar? |
| Politicas | Qual regra operacional controla a decisao e como ela e versionada? |
| Permissoes contextuais | Quem pode ver/fazer conforme papel, turma, unidade, professor, financeiro, suporte e consentimento? |
| Cotas e limites | O que consome cota, o que bloqueia e qual alternativa aparece? |
| Auditoria | O que precisa registrar autor, motivo, antes/depois, politica usada e impacto? |
| Excecoes | O que acontece em duplicidade, dado incompleto, erro, falta de permissao, cota ou integracao fora? |
| Integracoes | Qual sistema externo participa e qual fallback existe? |
| Mensagens | Qual texto/modelo/canal/consentimento/aprovacao aparece? |
| Qualidade de IA | Como medir acerto, erro, correcao, confianca, risco e economia? |
| Mobile | O que precisa funcionar no dia a dia pelo app, mesmo que resumido? |
| Suporte Taliya | O que o time interno pode ver/fazer e com qual autorizacao? |
| Metricas | Qual indicador mostra que essa parte gera valor real para o studio? |

## Regra central das rodadas

```text
rodada anterior cria contratos globais
rodada atual fecha arquitetura funcional da area
rodada atual fecha especificacao profunda das telas da area
rodada seguinte usa o que foi fechado
rodada final valida cobertura e contradicoes
rodada visual so acontece depois do produto 100% fechado
```

Exemplo:

- permissao definida na Rodada 0;
- arquitetura de atendimento fechada na Rodada 3;
- telas de atendimento detalhadas na propria Rodada 3;
- financeiro usa historico/contato ja definidos na Rodada 6;
- tudo e validado nas Rodadas 8, 9 e 10;
- so depois a Rodada 11 transforma as fichas em prompts visuais.

## Diretriz sobre referencias visuais

As referencias Dribbble aprovadas devem ser usadas depois da definicao funcional, como alvo de composicao visual para geracao das telas no ChatGPT.

Referencias:

- Web: `https://dribbble.com/shots/24659454-Customer-Journey-CRM-Dashboard`
- Mobile: `https://dribbble.com/shots/24537717-Sugar-CRM-Customer-Journey-Dashboard`

### Regra

```text
produto define escopo
ficha de tela define conteudo
referencia visual define composicao
ChatGPT gera a tela
```

As referencias nao podem:

- criar caso de uso novo so porque aparece bonito no layout;
- remover regra de negocio necessaria;
- esconder permissao, cota, auditoria ou fallback;
- enfraquecer o app mobile;
- transformar tela operacional em mockup decorativo.

As referencias devem orientar:

- estrutura visual de dashboard;
- mapas de jornada;
- cards;
- graficos;
- listas;
- funis;
- paineis laterais;
- hierarquia visual;
- densidade;
- navegacao web/mobile;
- padrao de telas com IA/agente.

O objetivo e reproduzir a logica de composicao, densidade e qualidade visual das referencias, adaptando todo conteudo, nomenclatura, dados, estados, marca e regras para Taliya.

## Saida obrigatoria de cada rodada funcional

Da Rodada 1 ate a Rodada 7, cada bloco precisa sair com duas entregas ao mesmo tempo:

```text
1. arquitetura funcional da area
2. especificacao profunda pagina por pagina e tela por tela
```

Nao existe rodada "so de mapa" e depois uma rodada separada "so de tela". O detalhamento profundo acontece junto com a decisao funcional da area.

### 1. Arquitetura funcional da area

Cada area deve documentar:

- objetivo da area no CRM;
- objetos principais da area;
- jornadas que comecam, passam ou terminam ali;
- regras de negocio;
- eventos e gatilhos;
- decisoes que o gestor/equipe precisa tomar;
- decisoes que o sistema pode preparar sozinho;
- decisoes que um agente pode executar;
- dependencias com outras areas;
- dados obrigatorios;
- dados opcionais;
- excecoes;
- riscos;
- permissoes;
- cotas;
- auditoria;
- indicadores;
- relatorios ou visoes necessarias;
- diferenca entre web e mobile.

### 2. Especificacao profunda das telas

Cada pagina web e cada tela mobile da rodada deve documentar:

- layout funcional;
- zonas da tela;
- hierarquia do conteudo;
- componentes esperados;
- tabelas, listas, cards, paineis, modais e gavetas laterais;
- campos exibidos;
- campos editaveis;
- campos obrigatorios;
- campos sensiveis;
- botoes primarios;
- botoes secundarios;
- acoes rapidas;
- acoes em lote;
- filtros;
- busca;
- ordenacao;
- estados vazios;
- estados de carregamento;
- estados de erro;
- estados bloqueados por permissao;
- estados bloqueados por cota;
- estados bloqueados por dado incompleto;
- mensagens de confirmacao;
- comportamento manual;
- comportamento com copiloto;
- comportamento autonomo;
- onde aparece sugestao de IA;
- onde aparece execucao de agente;
- onde aparece motivo/confianca/historico da IA;
- fallback quando IA falha;
- fallback quando integracao falha;
- fallback quando WhatsApp falha;
- equivalente web/mobile;
- o que fica fora daquela tela.

### Criterio de aceite comum das Rodadas 1-7

Uma rodada so pode ser marcada como concluida quando:

- a arquitetura funcional da area estiver escrita;
- todas as paginas web daquela area tiverem ficha profunda;
- todas as telas mobile daquela area tiverem ficha profunda;
- cada ficha apontar casos de uso cobertos;
- cada ficha apontar fluxos de agente relacionados;
- cada acao sensivel tiver permissao, cota, auditoria e fallback;
- cada diferenca web/mobile tiver justificativa;
- toda pendencia estiver no documento de decisoes abertas.

## Estrutura padrao de ficha por tela

Toda tela/pagina detalhada deve seguir este formato:

```text
Nome
Tipo: web, mobile ou ambos
Objetivo
Usuario principal
Usuarios secundarios
Rotas relacionadas
Casos de uso cobertos
Fluxos de agente relacionados
Blocos da tela
Zona principal
Zona lateral/secundaria
Modais/gavetas relacionados
Componentes esperados
Campos exibidos
Campos editaveis
Campos obrigatorios
Campos sensiveis
Acoes/botoes
Posicao dos botoes
Acao manual
Acao com copiloto
Acao autonoma
Estados
Permissoes
IA/agentes
Cotas
Auditoria
Fallbacks
Web/mobile equivalente
Fora de escopo desta tela
Decisoes pendentes
```

## Estrutura padrao de arquitetura funcional por area

Toda area detalhada deve seguir este formato:

```text
Nome da area
Objetivo operacional
Objetos de negocio
Usuarios envolvidos
Jornadas cobertas
Entradas da area
Saidas da area
Fonte da verdade
Ciclo de vida dos objetos
Regras de negocio
Politicas operacionais relacionadas
Eventos e gatilhos
Decisoes humanas
Acoes programaticas
Acoes com IA/copiloto
Acoes autonomas
Operacao sem agentes
Dependencias com outras areas
Dados obrigatorios
Dados opcionais
Dados sensiveis
Excecoes
Riscos
Permissoes
Cotas
Auditoria
Integracoes
Comportamento quando integracao falha
Comportamento quando cota acaba
Comportamento quando dado esta incompleto
Qualidade de IA
Suporte Taliya
Indicadores
Relatorios/visoes
Web
Mobile
Decisoes pendentes
```

## Rodada 0 - Contratos globais

### Objetivo

Criar as regras comuns antes de detalhar telas.

### Status

Rodada 0 v0.1 criada em `round-0-foundation-audit.pt-BR.md`.

Os contratos existem como base para iniciar a Rodada 1, mas continuam revisaveis se as proximas rodadas encontrarem contradicoes.

### Entregas

- `permissions-matrix.pt-BR.md`
- `action-button-taxonomy.pt-BR.md`
- `ui-state-taxonomy.pt-BR.md`
- `quota-touchpoints.pt-BR.md`
- `audit-touchpoints.pt-BR.md`
- `canonical-data-model.pt-BR.md`
- `object-lifecycle-map.pt-BR.md`
- `source-of-truth-matrix.pt-BR.md`
- `operational-policy-versioning.pt-BR.md`
- `integration-failure-contracts.pt-BR.md`
- `zero-agent-operating-model.pt-BR.md`
- `agent-quality-evaluation.pt-BR.md`
- `migration-import-plan.pt-BR.md`
- `taliya-internal-ops.pt-BR.md`
- `product-success-metrics.pt-BR.md`
- `notification-template-governance.pt-BR.md`
- esqueleto de `open-product-decisions.pt-BR.md`
- esqueleto de `functional-architecture.pt-BR.md`
- esqueleto de `screen-specs-detailed.pt-BR.md`

### Deve definir

- papeis: dono, admin, recepcao/operacao, financeiro, professor, suporte Taliya, agente/runtime;
- niveis de permissao: ver, criar, editar, aprovar, executar, exportar, auditar, pausar automacao;
- permissoes contextuais por unidade, turma, professor, area financeira, dados sensiveis, suporte e consentimento;
- objetos canonicos: studio, unidade, usuario, papel, aluno, responsavel, interessado, turma, aula, presenca, reposicao, lista de espera, evento, pagamento, cobranca, contrato, documento, tarefa, caso, conversa, mensagem, segmento, comunicado, agente, fluxo, execucao, incidente, politica, cota, auditoria, integracao, plano e assinatura;
- ciclos de vida dos objetos centrais;
- fonte da verdade de cada dado importante;
- regra de resolucao de conflito entre importacao, edicao manual, integracao, WhatsApp e agente;
- operacao manual completa no plano base com 0 agentes;
- politica de versionamento para regras operacionais usadas por humanos e agentes;
- governanca de modelos de mensagem, consentimento, opt-out e aprovacao;
- estados globais;
- botoes padrao;
- niveis de risco;
- quando IA sugere, prepara, executa ou bloqueia;
- como medir qualidade do agente: acerto, erro, correcao, confianca, risco, economia, tempo e reabertura;
- quando cota aparece;
- quando auditoria e obrigatoria;
- regra de fallback quando acao nao pode rodar;
- comportamento padrao quando WhatsApp, pagamento, calendario, importacao, webhook ou integracao externa falhar;
- escopo da operacao interna Taliya: acesso autorizado, suporte, incidentes, tenant, plano, bloqueio e auditoria;
- metricas principais de sucesso para provar valor ao gestor.

### Criterio de aceite

Nenhuma tela critica pode ser detalhada antes de ter esses contratos minimos. A partir daqui, toda rodada precisa alimentar tanto `functional-architecture.pt-BR.md` quanto `screen-specs-detailed.pt-BR.md`.

Rodada 0 so fecha se as perguntas abaixo tiverem resposta:

- Quais sao os objetos canonicos do CRM?
- Qual e o ciclo de vida de cada objeto critico?
- Qual e a fonte da verdade de cada dado critico?
- Como resolver conflito de dado?
- Como tudo funciona sem agentes?
- Quais politicas precisam ser versionadas?
- Quais integracoes podem falhar e como o produto se recupera?
- Como medir qualidade dos agentes?
- Como o suporte Taliya acessa e opera sem violar privacidade?
- Quais metricas provam valor para o gestor?

## Rodada 1 - Ativacao, setup e configuracao essencial

### Status

Rodada 1 v0.1 criada em `round-1-activation-setup-spec.pt-BR.md`.

Esta versao fecha a base funcional para revisao: onboarding web, setup mobile, importacao, configuracao essencial, agentes iniciais, cotas e qualidade de dados.

### Telas/paginas

Web:

- Onboarding e configuracao inicial
- Configuracoes
- Agentes e fluxos
- Uso, cotas e economia
- Qualidade de dados

Mobile:

- Setup inicial
- Importacao assistida
- Configuracao inicial de agentes
- Configuracao rapida de fluxo
- Configuracoes essenciais
- Agentes e fluxos
- Cotas

### Objetivo

Garantir que o studio consegue ativar e comecar a operar pelo web ou pelo app.

### Deve responder

- o que e obrigatorio antes de abrir o CRM;
- o que pode ficar para depois;
- como configurar agente no app sem expor configuracao avancada;
- como testar um fluxo simples;
- quando pedir web;
- como lidar com duplicidade/importacao;
- quais cotas aparecem no setup;
- quais permissoes iniciais existem.

### Criterio de aceite

Um gestor deve conseguir sair de "conta paga" para "CRM pronto para operar" sem buraco de arquitetura, sem buraco de rota e sem buraco de tela. Cada tela de setup/configuracao precisa ter conteudo, botoes, estados, permissoes, cotas, auditoria e fallback definidos.

## Rodada 2 - Operacao diaria e mesa de comando

### Status

Rodada 2 v0.1 criada em `round-2-daily-command-spec.pt-BR.md`.

Esta versao fecha a base funcional para revisao: Hoje, Operacao/Jornadas, Tarefas, Aprovacoes, Notificacoes, Checklist do dia, Caso operacional e jornadas prioritarias no mobile.

### Telas/paginas

Web:

- Hoje
- Jornadas e operacao
- Tarefas e operacao
- Aprovacoes
- Notificacoes
- Checklist do dia
- Caso operacional
- Qualidade de dados

Mobile:

- Hoje
- Checklist do dia
- Notificacoes
- Busca global
- Tarefas
- Aprovacoes
- Caso operacional
- Jornadas prioritarias
- Qualidade de dados

### Objetivo

Definir a mesa de comando diaria.

### Deve responder

- o que aparece primeiro no dia;
- criterio de prioridade;
- tipos de cartao;
- quando vira tarefa;
- quando vira caso;
- quando vira aprovacao;
- como mover etapa;
- o que aparece no mobile;
- como mostrar risco, cota, dono e prazo.

### Criterio de aceite

Nenhum caso importante deve ficar perdido fora de Hoje, Jornadas, Tarefas ou Aprovacoes. Cada card, fila, alerta, tarefa, aprovacao e caso operacional precisa ter origem, dono, acao esperada, estado e destino definidos.

## Rodada 3 - Atendimento, alunos, historico e professor

Status: v0.1 em `round-3-attendance-students-history-spec.pt-BR.md`.

### Telas/paginas

Web:

- Inbox e conversas
- Contatos
- Alunos e perfil do aluno
- Historico do aluno
- Professor e notas

Mobile:

- Inbox
- Conversa
- Contato rapido
- Falhas de envio
- Alunos
- Perfil do aluno
- Historico permitido
- Professor

### Objetivo

Fechar o nucleo CRM humano.

### Deve responder

- como vincular conversa a aluno/interessado;
- como assumir do agente;
- opt-out;
- telefone compartilhado e identidade ambigua;
- permissoes de historico;
- notas de professor;
- contexto permitido;
- falhas de envio;
- quais dados sensiveis ficam escondidos.

### Criterio de aceite

Recepcao e professor conseguem operar atendimento e contexto do aluno sem expor dado indevido. Cada conversa, perfil, historico, nota e falha de envio precisa ter regra de visibilidade, acao possivel e fallback.

## Rodada 4 - Agenda, turmas, aulas e reposicoes

Status: v0.1 em `round-4-schedule-classes-replacements-spec.pt-BR.md`.

### Telas/paginas

Web:

- Agenda
- Grade, turmas e eventos
- Aula e chamada
- Reposicoes e lista de espera
- Recursos, feriados e disponibilidade

Mobile:

- Agenda
- Turmas
- Aula
- Chamada
- Reposicoes
- Lista de espera
- Eventos/workshops
- Recursos e disponibilidade

### Objetivo

Definir o core operacional de Pilates.

### Deve responder

- como agenda mostra dia/semana;
- como turma mostra capacidade/vagas;
- como fazer chamada;
- falta/no-show;
- credito de reposicao;
- encontrar encaixe;
- lista de espera;
- professor/sala indisponivel;
- eventos/workshops;
- avisos de turma.

### Criterio de aceite

Um dia de aulas deve poder ser operado no mobile e administrado no web. Agenda, turma, aula, chamada, reposicao, lista de espera e encaixe precisam estar definidos em nivel de tela, com botoes manuais e assistidos.

## Rodada 5 - Vendas, experimental, matricula e comunicados

Status: v0.1 em `round-5-sales-trials-enrollment-communications-spec.pt-BR.md`.

### Telas/paginas

Web:

- Interessados e vendas
- Aulas experimentais
- Matriculas
- Vendas e origens
- Segmentos e comunicados

Mobile:

- Interessados
- Experimental
- Matricula rapida
- Origens e indicacoes
- Segmentos e comunicados

### Objetivo

Converter interessado em aluno sem quebrar agenda, financeiro e CRM.

### Deve responder

- etapas do pipeline;
- origem/campanha/indicacao;
- experimental;
- lembrete;
- falta/remarcacao;
- pos-aula;
- conversao em aluno;
- matricula rapida;
- comunicados e consentimento;
- aprovacao de mensagens em massa.

### Criterio de aceite

Todo lead deve ter proxima acao clara e caminho ate aluno ou perdido. Pipeline, experimental, matricula, origem, indicacao e comunicado precisam ter telas com campos, etapas, acoes, estados e regras de consentimento.

## Rodada 6 - Financeiro, contratos, retencao e casos sensiveis

Status: v0.2 em `round-6-finance-retention-sensitive-spec.pt-BR.md`.

### Telas/paginas

Web:

- Financeiro
- Kanban financeiro
- Movimentacoes financeiras
- Excecoes financeiras sensiveis sem pagina propria no MVP
- Contratos e documentos financeiros
- Retencao
- Cancelamentos e reativacao
- Reclamacoes e casos sensiveis
- Privacidade e solicitacoes

Mobile:

- Financeiro essencial
- Pagamento/cobranca
- Excecoes financeiras via aprovacao/tarefa contextual
- Contratos/documentos
- Retencao
- Cancelamentos e reativacao
- Reclamacao/caso sensivel
- Privacidade/solicitacoes

### Objetivo

Cobrir dinheiro, contrato, risco, cancelamento, reclamacao e LGPD.

### Deve responder

- o que financeiro pode fazer no app;
- o que exige aprovacao;
- promessa de pagamento;
- comprovante;
- bloqueio/liberacao;
- desconto/cortesia;
- disputa/reembolso;
- contrato/documento;
- aluno em risco;
- cancelamento;
- reativacao;
- reclamacao;
- opt-out/LGPD/acesso de suporte.

### Criterio de aceite

Nenhuma acao financeira, reputacional ou sensivel pode ocorrer sem permissao, impacto e auditoria. As telas precisam deixar explicito o que pode ser feito no app, o que exige web, o que exige aprovacao e o que nunca pode ser autonomo.

## Rodada 7 - Agentes, execucoes, cotas, relatorios e governanca

Status: v0.1 em `round-7-agents-quotas-governance-spec.pt-BR.md`.

### Telas/paginas

Web:

- Agentes e fluxos
- Execucoes e incidentes de agentes
- Uso, cotas e economia
- Relatorios e exportacoes
- Politicas operacionais
- Integracoes
- Auditoria
- Assinatura e billing
- Suporte interno Taliya

Mobile:

- Agentes/alertas
- Agentes e fluxos
- Execucao de agente
- Cotas
- Relatorios resumidos
- Auditoria resumida
- Integracoes/status
- Assinatura/billing
- Suporte/autorizacao de acesso

### Objetivo

Fechar confiabilidade do sistema, governanca dos agentes e operacao interna da Taliya.

### Deve responder

- configuracao essencial vs avancada de agente;
- modo manual/copiloto/autonomo;
- simulacao simples vs profunda;
- execucao;
- incidente;
- reprocessamento seguro;
- cota 70/90/100;
- modo economia;
- relatorio resumido vs profundo;
- politica versionada;
- integracao falhou;
- auditoria;
- billing e pacotes;
- como suporte Taliya acessa uma conta com autorizacao;
- como registrar incidente interno;
- como bloquear/desbloquear tenant, plano, agente ou integracao;
- como provar qualidade do agente por fluxo;
- como comparar execucao automatica com resolucao manual.

### Criterio de aceite

Agentes nao podem parecer "magicos": toda acao precisa de modo, limite, cota, auditoria e fallback. Toda tela de agente/execucao/cota/integracao precisa mostrar configuracao, status, motivo, proxima acao e recuperacao de falha. A operacao interna Taliya precisa ter limite claro para suporte, acesso autorizado, incidente, tenant, plano e auditoria.

## Rodada 8 - Cobertura cruzada

### Objetivo

Criar matrizes de cobertura e achar buracos.

### Entregas

- `route-screen-coverage.pt-BR.csv`
- `use-case-to-screen-coverage.pt-BR.csv`
- `agent-flow-screen-coverage.pt-BR.csv`

### Checks

- toda area funcional tem arquitetura definida;
- todo objeto canonico aparece no modelo de dados;
- todo objeto critico tem ciclo de vida;
- todo dado critico tem fonte da verdade;
- toda regra operacional sensivel tem politica e versao;
- todo caminho critico tem alternativa sem agentes;
- toda rota tem pagina/tela dona;
- toda pagina web tem ficha;
- toda tela mobile tem ficha;
- todo caso de uso tem tela e modo;
- todo fluxo de agente tem rota/tela, modo e fallback;
- todo caso sensivel tem permissao e auditoria;
- todo uso de IA tem cota ou justificativa de nao medir;
- todo fluxo de IA tem criterio de qualidade/erro/correcao;
- todo mobile tem equivalente web quando precisar;
- todo web-first tem motivo claro;
- toda integracao critica tem contrato de falha;
- toda acao de suporte Taliya tem autorizacao e auditoria;
- toda mensagem automatica ou em massa tem modelo, canal, consentimento e aprovacao quando necessario;
- toda metrica principal tem origem de dado.

### Criterio de aceite

Zero area sem arquitetura, zero objeto sem dono, zero rota orfa, zero caso sem tela, zero fluxo de agente sem superficie, zero pagina/tela sem especificacao profunda, zero caminho critico dependente exclusivamente de agente e zero acao sensivel sem permissao/auditoria.

## Rodada 9 - Simulacoes de usuario

### Objetivo

Testar o produto como gestor/equipe antes de dizer que esta 100%.

### Simulacoes obrigatorias

1. Studio compra e ativa pelo app.
2. Studio compra e ativa pelo web.
3. Gestor abre o dia.
4. Recepcao responde WhatsApp.
5. Professor opera aula e chamada.
6. Turma tem vaga e precisa encaixe.
7. Interessado vira experimental.
8. Experimental vira matricula.
9. Pagamento atrasa.
10. Comprovante chega.
11. Aluno pede cancelamento.
12. Aluno reclama.
13. Agente falha.
14. Cota chega a 90%.
15. Cota chega a 100%.
16. Dado duplicado bloqueia fluxo.
17. Professor/sala fica indisponivel.
18. LGPD/opt-out/acesso de suporte.
19. Comunicados em massa precisam aprovacao.
20. Gestor fecha o dia.
21. Studio importa base inicial de planilha.
22. Studio opera uma semana com 0 agentes ativos.
23. Gestor muda uma politica de reposicao/cobranca e verifica impacto.
24. WhatsApp ou integracao critica fica indisponivel.
25. Suporte Taliya acessa conta com autorizacao e resolve incidente.
26. Gestor revisa qualidade de um agente e corrige comportamento.
27. Gestor compara resultado manual vs copiloto vs autonomo.
28. Mensagem automatica precisa ser pausada por opt-out/consentimento.

Cada simulacao deve validar:

- arquitetura funcional;
- objeto e ciclo de vida afetado;
- fonte da verdade;
- politica operacional usada;
- tela web usada;
- tela mobile usada, quando aplicavel;
- conteudo visivel;
- botoes disponiveis;
- permissoes;
- cotas;
- auditoria;
- comportamento manual;
- comportamento com copiloto;
- comportamento autonomo;
- operacao sem agentes quando for caminho critico;
- qualidade/erro/correcao de IA quando houver agente;
- suporte Taliya quando houver acesso interno;
- metrica impactada;
- fallback.

### Criterio de aceite

Cada simulacao deve terminar em:

- resolvido;
- tarefa criada;
- aprovacao criada;
- caso criado;
- bloqueado com explicacao;
- decisao aberta registrada.

Nada pode simplesmente desaparecer.

## Rodada 10 - Fechamento final

### Objetivo

Consolidar tudo e congelar uma versao candidata.

### Entregas

- `final-consistency-audit.pt-BR.md`
- `final-product-decisions.pt-BR.md`
- versao final de `functional-architecture.pt-BR.md`
- versao final de `screen-specs-detailed.pt-BR.md`
- atualizacao do `README.pt-BR.md`
- marcacao de documentos obsoletos ou substituidos

### Checks finais

- contagens batem;
- toda area funcional tem arquitetura;
- toda pagina/tela tem especificacao profunda;
- modelo de dados canonico fechado;
- ciclos de vida fechados;
- fontes da verdade fechadas;
- politicas operacionais versionadas;
- operacao 0 agentes validada;
- contratos de falha de integracao fechados;
- qualidade de agentes fechada;
- migracao/importacao inicial fechada;
- suporte interno Taliya fechado;
- metricas de sucesso fechadas;
- governanca de mensagens/notificacoes fechada;
- documentos nao se contradizem;
- web/mobile estao alinhados;
- setup e configuracao essencial existem no app;
- configuracao avancada existe no web;
- 157 casos cobertos;
- 96 fluxos fortes cobertos;
- E14/G13 decididos ou explicitamente pendentes;
- permissoes fechadas;
- cotas fechadas;
- auditoria fechada;
- mobile nao ficou fraco;
- web nao virou menu infinito.

### Criterio de aceite

So chamar de 100% quando o documento final disser:

```text
Nao ha lacunas invisiveis conhecidas.
Pendencias restantes sao decisoes conscientes, com dono e impacto.
```

## Rodada 11 - Pacote para gerar telas no ChatGPT

### Objetivo

Transformar a especificacao funcional 100% em prompts prontos para gerar as paginas web e telas mobile no ChatGPT, usando as referencias visuais aprovadas como alvo de composicao.

Esta rodada nao redefine escopo, nao cria casos de uso e nao muda regras de negocio. Ela traduz a ficha funcional de cada tela para uma instrucao visual clara.

### Entregas

- `chatgpt-screen-generation-prompts.pt-BR.md`
- prompt base web;
- prompt base mobile;
- prompt por pagina web;
- prompt por tela mobile;
- prompt para estados vazios, erro, carregamento, bloqueio, cota e sem permissao;
- prompt para telas com IA/agente;
- prompt para telas de operacao sem agentes;
- prompt para jornada/dashboard;
- prompt para tela operacional densa;
- prompt para tela de configuracao;
- prompt para tela sensivel com auditoria/aprovacao.

### Deve definir

- como aplicar a referencia web em paginas Taliya;
- como aplicar a referencia mobile em telas Taliya;
- quais componentes da referencia viram padrao: sidebar, topo, cards, mapa de jornada, graficos, funil, paineis, listas e acoes;
- como adaptar a referencia para Pilates;
- como representar agentes de IA dentro da interface;
- como representar manual, copiloto e autonomo;
- como representar cota, auditoria, permissao e bloqueio sem poluir a tela;
- como manter o app mobile suficientemente operacional;
- como evitar que o ChatGPT invente regra de negocio ausente;
- como exigir que cada tela use apenas conteudo vindo da ficha oficial.

### Estrutura padrao de prompt por tela

```text
Nome da tela
Tipo: web ou mobile
Referencia visual: web ou mobile
Objetivo da tela
Usuario principal
Contexto de uso
Conteudo obrigatorio
Blocos e zonas
Componentes obrigatorios
Botoes e posicao
Estados obrigatorios
Comportamento manual
Comportamento copiloto
Comportamento autonomo
Cotas/auditoria/permissao
Dados de exemplo
Restricoes: nao inventar regra, nao remover bloco, nao simplificar fluxo critico
Resultado esperado
```

### Criterio de aceite

O pacote so fecha quando cada pagina/tela tiver um prompt capaz de gerar a interface sem inventar produto.

Se o prompt depender de "imagine os campos" ou "crie a regra", a ficha funcional ainda nao esta pronta e deve voltar para a rodada responsavel.

## Controle de conflito entre rodadas

### Regra 1 - Um documento canonico por assunto

Se uma decisao muda, atualizar o documento canonico e marcar o antigo como superado.

Documentos canonicos:

| Assunto | Documento canonico |
| --- | --- |
| Lista web/mobile | `web-mobile-review-simulation.pt-BR.md` |
| Mobile detalhado | `mobile-screen-map.pt-BR.md` |
| Web detalhado | `web-screen-map.pt-BR.md` |
| Arquitetura funcional | `functional-architecture.pt-BR.md` |
| Modelo de dados | `canonical-data-model.pt-BR.md` |
| Ciclos de vida | `object-lifecycle-map.pt-BR.md` |
| Fonte da verdade | `source-of-truth-matrix.pt-BR.md` |
| Politicas versionadas | `operational-policy-versioning.pt-BR.md` |
| Falhas de integracao | `integration-failure-contracts.pt-BR.md` |
| Operacao sem agentes | `zero-agent-operating-model.pt-BR.md` |
| Qualidade de agentes | `agent-quality-evaluation.pt-BR.md` |
| Migracao/importacao | `migration-import-plan.pt-BR.md` |
| Operacao interna Taliya | `taliya-internal-ops.pt-BR.md` |
| Metricas de sucesso | `product-success-metrics.pt-BR.md` |
| Mensagens/notificacoes | `notification-template-governance.pt-BR.md` |
| Prompts para telas | `chatgpt-screen-generation-prompts.pt-BR.md` |
| Cobertura por pagina | `page-requirements.pt-BR.md` |
| Casos de uso | `product-master-map-v2.pt-BR.md` |
| Profundidade | `product-depth-matrix.pt-BR.md` |
| Decisoes abertas | `open-product-decisions.pt-BR.md` |
| Especificacao final | `screen-specs-detailed.pt-BR.md` |

### Regra 2 - Toda mudanca exige check de impacto

Ao adicionar/remover tela, verificar:

- rota;
- objeto de negocio;
- ciclo de vida;
- fonte da verdade;
- caso de uso;
- fluxo de agente;
- mobile;
- permissao;
- cota;
- auditoria;
- politica versionada;
- operacao sem agentes;
- integracao/falha;
- suporte Taliya;
- metrica impactada;
- docs relacionados.

### Regra 3 - Nenhuma rodada reabre tudo sem motivo

Uma rodada pode abrir issue para outra, mas nao deve reescrever area que nao e dela.

Exemplo:

- Rodada 4 encontra problema financeiro;
- registra em decisoes abertas;
- Rodada 6 resolve.

### Regra 4 - Final de toda rodada tem mini-auditoria

Cada rodada termina com:

- o que foi fechado;
- o que mudou nos mapas;
- lacunas encontradas;
- decisoes abertas;
- documentos atualizados.

## Sequencia recomendada

```text
0. Contratos globais, dados, politicas, fontes da verdade e operacao 0 agentes
1. Arquitetura + telas de ativacao/setup/agentes essenciais
2. Arquitetura + telas de operacao diaria
3. Arquitetura + telas de atendimento/alunos/historico
4. Arquitetura + telas de agenda/turmas/aulas
5. Arquitetura + telas de vendas/matricula
6. Arquitetura + telas de financeiro/retencao/sensiveis
7. Arquitetura + telas de agentes/cotas/governanca/suporte Taliya
8. Cobertura cruzada de arquitetura, dados, rotas, telas, casos e fluxos
9. Simulacoes de usuario em web/app/manual/copiloto/autonomo/0 agentes
10. Fechamento final
11. Pacote de prompts para gerar paginas/telas no ChatGPT usando as referencias visuais
```

## Estimativa de esforco

| Rodada | Peso | Motivo |
| --- | --- | --- |
| 0 | Muito alto | Define contratos usados por tudo: dados, fonte da verdade, permissoes, politicas, cotas, auditoria, integracoes, suporte e 0 agentes. |
| 1 | Medio | Setup e agentes essenciais sao centrais, mas escopo controlado. |
| 2 | Alto | Mesa de operacao impacta todas as areas. |
| 3 | Alto | CRM humano, historico e permissao. |
| 4 | Alto | Core operacional de Pilates. |
| 5 | Medio | Vendas depende de agenda/contatos. |
| 6 | Alto | Financeiro e sensiveis exigem travas. |
| 7 | Alto | Agentes, cotas, suporte interno, qualidade e auditoria fecham confiabilidade. |
| 8 | Alto | Cruza arquitetura, dados, telas, casos, agentes, politicas e metricas. |
| 9 | Alto | Simulacao guiada de cenarios reais, falhas, 0 agentes e suporte. |
| 10 | Medio | Consolidacao e limpeza. |
| 11 | Medio | Transforma a especificacao final em prompts visuais sem alterar escopo. |

## Como saber que terminamos

Terminamos quando estas perguntas tiverem resposta objetiva:

- Quais telas existem no web?
- Quais telas existem no app?
- Qual arquitetura funcional sustenta cada area?
- Quais objetos de negocio existem?
- Qual ciclo de vida cada objeto critico segue?
- Qual e a fonte da verdade de cada dado critico?
- Qual rota abre cada tela?
- O que existe dentro de cada tela?
- Onde ficam os blocos, botoes, listas, filtros, cards, modais e estados?
- Qual caso de uso cada tela cobre?
- Qual fluxo de agente aparece onde?
- Quem pode ver/fazer cada acao?
- Quais acoes consomem cota?
- Quais acoes exigem aprovacao?
- Quais acoes geram auditoria?
- Quais politicas operacionais controlam cada decisao?
- O que funciona sem agentes?
- Como medir qualidade dos agentes?
- Como importar/migrar um studio real?
- Como o suporte Taliya acessa e opera?
- Quais integracoes podem falhar e como o sistema reage?
- Quais mensagens/modelos/notificacoes existem e quem aprova?
- Quais metricas provam valor?
- O que acontece quando falha?
- O que e web-first?
- O que e mobile-first?
- O que esta fora e por que?
- Qual prompt gera cada pagina web?
- Qual prompt gera cada tela mobile?
- Como garantir que a UI gerada segue as referencias sem inventar produto?

Se alguma resposta depender de "a gente ve depois", ainda nao esta 100%.
