# Setup Inicial - Auditoria Final Do Fluxo

Status: auditoria aprovada para implementacao v0.1.
Data: 2026-05-20.

## Objetivo

Auditar o Setup Inicial como conjunto, verificando se as telas, blocos, dados, pendencias, publicacao e limites de escopo se integram corretamente com o CRM Taliya, com as configuracoes pos-go-live, com Agentes/Fluxos e com Control Planes.

Este documento deve ser lido como mapa final do Setup Inicial antes de implementar telas.

Quando houver conflito entre este documento e artefatos antigos, este documento prevalece para o Setup Inicial.

## Veredito Geral

A arquitetura atual faz sentido.

O Setup Inicial esta no ponto certo quando:

- prepara o CRM para operar manualmente com seguranca;
- funciona com 0, 1, 3 ou 7 agentes;
- nao depende de agente para ativar o CRM;
- nao configura profundamente fluxos de agente;
- nao tenta resolver todas as configuracoes do produto;
- cria rascunhos, validacoes e pendencias rastreaveis;
- separa claramente `publicado agora`, `pendencias` e `depois do go-live`;
- usa o Agente de Configuracao como copiloto lateral, nao como formulario principal.

O maior risco encontrado e documental, nao arquitetural:

- alguns docs antigos ainda citam rotas separadas como `/onboarding/importacao` e `/onboarding/configuracoes/consumo-aulas`;
- alguns trechos antigos ainda sugerem configurar chave Pix, instrucao para aluno ou detalhes de pagamento no setup;
- alguns trechos antigos ainda falam de `8 blocos`.

Esses pontos foram superados pelas decisoes mais recentes.

## Decisao Canonica Atual

### Rotas Do Onboarding

O Setup Inicial deve ser entendido como uma trilha curta:

1. `/onboarding`
   - entrada pos-pagamento;
   - pergunta o nome do studio;
   - cria ou identifica o workspace;
   - apresenta o Agente de Configuracao depois do nome informado;
   - tambem serve para retomada se o usuario interromper o setup.

2. `/onboarding/diagnostico`
   - diagnostico rapido;
   - nao configura nada definitivo;
   - prepara defaults, importacoes e orientacao dos blocos.

3. `/onboarding/setup`
   - pagina principal com stepper de 9 blocos;
   - concentra Studio, Equipe, Canais, Planos, Pagamento, Alunos, Turmas, Agenda e Revisao.

4. `/onboarding/concluido`
   - opcional;
   - pode ser rota, modal ou estado final apos publicacao;
   - orienta entrada no CRM e proximos ajustes.

Rotas que nao devem existir como experiencia principal no Setup Inicial:

- `/onboarding/importacao`;
- `/onboarding/configuracoes/[area]`;
- `/onboarding/configuracoes/consumo-aulas`.

Importacao, planos e consumo entram nos blocos do `/onboarding/setup`.

### Sequencia Oficial De Blocos

Dentro de `/onboarding/setup`, a sequencia oficial e:

1. `Studio`;
2. `Equipe`;
3. `Canais`;
4. `Planos`;
5. `Pagamento`;
6. `Alunos`;
7. `Turmas`;
8. `Agenda`;
9. `Revisao`.

Referencias visuais aprovadas:

| Bloco | Imagem | Documento |
|---:|---|---|
| 1 | `51D_round-4.1J_onboarding_bloco-1-studio-aprovado.png` | `setup-51D-bloco-1-studio-approved.pt-BR.md` |
| 2 | `51E_round-4.1J_onboarding_bloco-2-equipe-aprovado.png` | `setup-51E-bloco-2-equipe-approved.pt-BR.md` |
| 3 | `51F_round-4.1J_onboarding_bloco-3-canais-aprovado.png` | `setup-51F-bloco-3-canais-approved.pt-BR.md` |
| 4 | `51G_round-4.1J_onboarding_bloco-4-planos-aprovado.png` | `setup-51G-bloco-4-planos-approved.pt-BR.md` |
| 5 | `51K_round-4.1J_onboarding_bloco-5-pagamento-aprovado.png` | `setup-51K-bloco-5-pagamento-approved.pt-BR.md` |
| 6 | `51H_round-4.1J_onboarding_bloco-5-alunos-aprovado.png` | `setup-51H-bloco-5-alunos-approved.pt-BR.md` |
| 7 | `51I_round-4.1J_onboarding_bloco-6-turmas-aprovado.png` | `setup-51I-bloco-6-turmas-approved.pt-BR.md` |
| 8 | `51J_round-4.1J_onboarding_bloco-7-agenda-aprovado.png` | `setup-51J-bloco-7-agenda-approved.pt-BR.md` |
| 9 | `51L_round-4.1J_onboarding_bloco-9-revisao-aprovado.png` | `setup-51L-bloco-9-revisao-approved.pt-BR.md` |

Nota: `51H`, `51I` e `51J` mantem nomes antigos de arquivo, mas representam oficialmente os blocos 6, 7 e 8.

## Diagnostico

O diagnostico esta correto como etapa anterior ao setup.

Ele deve ter 5 perguntas:

1. Quantos alunos ativos o studio tem hoje?
2. Onde estao agenda, turmas ou horarios hoje?
3. Onde estao alunos, planos e contatos hoje?
4. Quais tipos de planos o studio oferece pro aluno?
5. Como o studio lida com reposicoes?

O diagnostico nao deve perguntar:

- se usa WhatsApp;
- se quer importar agora;
- se trabalha com horarios fixos;
- se o plano tem agentes;
- quantas pessoas vao usar o Taliya;
- quais areas quer configurar primeiro.

Uso correto das respostas:

- preparar defaults;
- sugerir fontes nos blocos de Alunos e Turmas;
- ajustar expectativas de volume e revisao;
- orientar o agente lateral.

As respostas do diagnostico nao publicam configuracao.

## Auditoria Por Bloco

### Bloco 1 - Studio

Funcao:

- definir a base operacional minima do studio.

Entrada do usuario:

- nome do studio;
- dias de funcionamento;
- horario geral de abertura e fechamento;
- pausa do dia, se existir;
- ajustes por dia quando necessario.

Saida do bloco:

- janela semanal de funcionamento;
- regra base para validar turmas e agenda.

Obrigatorio para publicar:

- nome do studio;
- pelo menos um dia de funcionamento;
- horario de abertura e fechamento coerentes.

Pode ficar para depois:

- feriados;
- salas/recursos;
- multiplas unidades;
- identidade visual;
- regras especificas por sala/professor.

Risco auditado:

- documentos antigos citam unidade principal e multiplas unidades, mas MVP nao deve expor mais de uma unidade no setup.

Decisao:

- no MVP, nao configurar multiplas unidades no Setup Inicial.

### Bloco 2 - Equipe

Funcao:

- preparar acessos e responsaveis humanos.

Entrada do usuario:

- dono confirmado;
- pessoas adicionais, se houver;
- nome, e-mail, WhatsApp e papel.

Saida do bloco:

- equipe preparada em rascunho;
- convites preparados para envio na publicacao.

Obrigatorio para publicar:

- dono/admin confirmado.

Pode ficar para depois:

- adicionar mais equipe;
- permissoes finas;
- matriz de acesso;
- ajustes por usuario.

Regra importante:

- convite nao e enviado no bloco;
- convite so e enviado quando o setup inicial for publicado.

### Bloco 3 - Canais

Funcao:

- registrar canais oficiais e publicos do studio.

Entrada do usuario:

- WhatsApp Business do studio;
- e-mail do studio;
- canais publicos opcionais: Instagram, Facebook, TikTok, X e site.

Saida do bloco:

- canais registrados;
- pendencia de conexao oficial do WhatsApp, quando houver.

Obrigatorio para publicar:

- pelo menos canal administrativo suficiente para operar;
- e-mail do studio ou do dono.

Pode publicar com aviso:

- WhatsApp ainda nao conectado oficialmente;
- redes sociais incompletas.

Pode ficar para depois:

- conexao oficial do WhatsApp;
- templates;
- opt-out avancado;
- campanhas;
- automacoes de envio;
- provedores, tokens, webhooks.

Regra importante:

- WhatsApp pendente nao bloqueia o CRM inteiro;
- bloqueia apenas recursos que dependem de WhatsApp.

### Bloco 4 - Planos

Funcao:

- cadastrar os principais planos vendidos pelo studio.

Entrada do usuario:

- nome do plano;
- tipo;
- valor;
- quantidade/frequencia;
- recorrencia comercial;
- validade;
- reposicao simples.

Saida do bloco:

- catalogo inicial de planos;
- regras basicas de direito de aula, saldo, validade e reposicao.

Obrigatorio para publicar financeiro/consumo:

- pelo menos um plano valido, se o studio ja opera com planos;
- tipo do plano;
- valor ou indicacao de gratuito;
- quantidade/frequencia ou saldo;
- regra basica de reposicao.

Pode ficar para depois:

- descontos;
- cupons;
- contratos personalizados;
- comissoes;
- nota fiscal;
- inadimplencia avancada;
- excecoes financeiras sensiveis.

Regra importante:

- plano nao define forma de pagamento;
- plano nao define horario fixo;
- horario fixo aparece depois em Turmas/Agenda.

### Bloco 5 - Pagamento

Funcao:

- selecionar meios aceitos no comeco e explicar operacao financeira inicial.

Entrada do usuario:

- selecionar `Pix`, `Dinheiro` e/ou `Cartao`.

Saida do bloco:

- meios aceitos no inicio;
- entendimento operacional de que a baixa inicial e manual no Taliya;
- Pagamentos Taliya marcado como pos-go-live.

Obrigatorio para publicar:

- pelo menos um meio de pagamento selecionado quando houver planos pagos.

Pode ficar para depois:

- chave Pix;
- maquininha;
- conta bancaria;
- Pix automatico;
- cartao online;
- link de pagamento;
- boleto;
- provedor/gateway;
- recorrencia automatica;
- conciliacao;
- KYC.

Regra importante:

- nenhum meio abre configuracao propria no Setup Inicial;
- comprovante sempre pode ser anexado no registro de baixa;
- mensagens/instrucoes para aluno ficam para comunicacao/automacoes depois do go-live.

Modelo conceitual correto:

- plano gera cobranca;
- pagamento quita cobranca;
- baixa confirma pagamento;
- pagamento confirmado libera aulas ou saldo.

### Bloco 6 - Alunos

Funcao:

- montar a base inicial de alunos ativos.

Entrada do usuario:

- arquivos;
- planilhas;
- exportacoes;
- fotos/anotacoes;
- caderno/ficha/print;
- lista colada;
- cadastro manual.

Saida do bloco:

- tabela consolidada de alunos preparados;
- fontes adicionadas;
- duplicidades e pendencias;
- todos entram como `Ativo`.

Obrigatorio para publicar aluno:

- nome;
- WhatsApp ou telefone.

Pode publicar com aviso:

- aluno sem plano;
- duplicidade provavel, se nao afetar o cadastro minimo;
- dado opcional incompleto.

Bloqueia publicacao daquele aluno:

- sem nome;
- sem contato;
- conflito que impeça identificar a pessoa.

Pode ficar para depois:

- historico financeiro;
- historico de aulas;
- ficha clinica completa;
- tags;
- documentos;
- segmentacao;
- ex-alunos/leads/cancelados.

Regra importante:

- horarios e turmas serao vinculados depois;
- importacao assistida nunca publica dado ambiguo sem revisao do dono.

### Bloco 7 - Turmas

Funcao:

- preparar estruturas recorrentes de turma e horario fixo.

Entrada do usuario:

- arquivos;
- fotos de grade;
- listas coladas;
- cadastro manual;
- opcao de nao ter turmas prontas, usando grade/agenda como fonte para montar turmas.

Saida do bloco:

- turmas preparadas;
- dias e horarios recorrentes;
- capacidade;
- professor opcional;
- alunos vinculados quando possivel.

Obrigatorio para publicar turma:

- dias da semana;
- horario de inicio;
- horario de fim;
- capacidade.

Pode publicar com aviso:

- sem professor;
- sem alunos;
- aluno citado nao encontrado;
- turma fora da janela de funcionamento, se marcada como aviso e nao bloqueio.

Bloqueia publicacao daquela turma:

- sem dia;
- sem horario;
- sem capacidade;
- horario invalido.

Pode ficar para depois:

- chamada;
- presenca;
- reposicoes;
- encaixes;
- lista de espera;
- bloqueios avancados;
- feriados complexos;
- agentes operando agenda.

Regra importante:

- turma ainda nao e agenda final;
- a agenda sera montada no Bloco 8.

### Bloco 8 - Agenda

Funcao:

- revisar a semana base gerada a partir das turmas preparadas.

Entrada do usuario:

- revisao visual;
- selecao de item no controle da semana;
- voltar para Turmas quando erro vem da origem.

Saida do bloco:

- semana base pronta para revisao final;
- pendencias integradas na grade;
- visao de como cada turma virou ocorrencias.

Obrigatorio para publicar agenda:

- semana base gerada;
- turmas validas suficientes;
- ocorrencias coerentes com dias/horarios;
- bloqueios criticos resolvidos.

Pode publicar com aviso:

- fora da janela do studio;
- professor pendente;
- aluno pendente;
- aviso de capacidade, quando nao bloquear.

Bloqueia publicacao:

- ausencia de semana base quando o studio precisa de agenda;
- turma sem horario/capacidade;
- conflito que impossibilite montar ocorrencia.

Pode ficar para depois:

- reposicoes;
- encaixes;
- chamada;
- lista de espera;
- bloqueios avancados;
- feriados complexos;
- envio automatico de mensagens.

Regra importante:

- este bloco nao permite importacao externa;
- importacao de agenda/grade que revela turmas deve entrar no Bloco 7.

### Bloco 9 - Revisao

Funcao:

- conferir antes da publicacao.

Entrada do usuario:

- revisar publicado agora;
- revisar pendencias;
- entender depois do go-live;
- confirmar publicacao.

Saida do bloco:

- publicacao do setup inicial;
- convites de equipe enviados;
- pendencias rastreaveis criadas;
- areas avancadas direcionadas para pos-go-live.

Obrigatorio para publicar:

- confirmacao explicita do dono;
- ausencia de bloqueio real;
- dados minimos das camadas que serao publicadas.

Pode publicar com aviso:

- WhatsApp nao conectado;
- alunos sem plano;
- turma sem professor;
- Pagamentos Taliya nao ativado;
- fluxos de agentes nao configurados.

Bloqueia publicacao:

- aluno que seria publicado sem nome/contato;
- turma sem dia/horario/capacidade;
- nenhum meio de pagamento quando houver planos pagos;
- ausencia de dono/admin;
- ausencia de nome do studio;
- agenda essencial impossivel de montar.

Regra importante:

- se houver bloqueio real, `Publicar setup inicial` fica desabilitado;
- o CTA principal deve virar `Resolver bloqueios`;
- pendencias com aviso nao bloqueiam necessariamente a publicacao.

## Integracao Entre Blocos

### Cadeia Operacional Principal

O setup forma esta cadeia:

1. `Studio` define a janela de funcionamento.
2. `Equipe` define quem responde pelo sistema.
3. `Canais` define como o studio pode ser encontrado/comunicar.
4. `Planos` define o que o aluno compra.
5. `Pagamento` define meios aceitos e operacao inicial de baixa.
6. `Alunos` cria a base de alunos ativos.
7. `Turmas` cria estruturas recorrentes e vinculos.
8. `Agenda` transforma turmas em semana base.
9. `Revisao` separa publicado agora, pendencias e depois do go-live.

### Dependencias Criticas

| Dependencia | Motivo |
|---|---|
| Studio antes de Turmas/Agenda | horarios gerais validam turmas e semana base |
| Planos antes de Pagamento | primeiro define o que vende, depois como registra pagamento |
| Planos antes de Alunos completos | aluno pode ser vinculado a plano |
| Alunos antes de Turmas | turma pode vincular alunos existentes |
| Turmas antes de Agenda | agenda e gerada a partir das turmas |
| Agenda antes de Revisao | revisao precisa mostrar semana que sera publicada |

### Ordem Validada

A ordem atual esta correta.

Nao deve mover:

- `Pagamento` para antes de `Planos`;
- `Agenda` para antes de `Turmas`;
- `Revisao` para uma tela configuravel;
- importacao para uma rota solta fora do fluxo.

## Pendencias E Publicacao

Toda pendencia deve virar objeto rastreavel.

Campos minimos da pendencia:

- titulo;
- area;
- motivo;
- responsavel;
- destino correto para continuar;
- prioridade;
- bloqueia publicacao: sim/nao;
- camada afetada;
- origem;
- status.

Classes de pendencia:

1. `Bloqueia publicacao`
   - impede publicar a camada ou item afetado.
2. `Pode publicar com aviso`
   - permite operacao inicial, mas registra risco/ajuste.
3. `Fica para depois`
   - nao pertence ao Setup Inicial; vai para Configuracoes, Agentes/Fluxos ou Control Planes.

## O Que Publica Agora

Ao concluir o Setup Inicial, o CRM deve publicar:

- workspace do studio;
- dono/admin;
- equipe preparada e convites enviados;
- canais cadastrados;
- planos principais;
- meios de pagamento aceitos;
- alunos ativos aprovados;
- turmas validas;
- semana base da agenda;
- pendencias rastreaveis;
- defaults seguros de operacao.

## O Que Fica Para Pos-Go-Live

Vai para Configuracoes do CRM:

- ajustes finos de studio;
- permissoes detalhadas;
- feriados e salas;
- regras avancadas de agenda;
- templates completos;
- notificacoes;
- campos customizados;
- financeiro avancado.

Vai para Pagamentos Taliya:

- Pix automatico;
- cartao online;
- recorrencia automatica;
- link/checkout;
- webhooks;
- conciliacao.

Vai para Agentes/Fluxos:

- modo manual/copiloto/autonomo;
- ativacao de fluxo;
- aprovacao por acao;
- fallback;
- limites;
- cotas por fluxo;
- simulacao;
- publicacao de automacoes.

Vai para Control Planes:

- execucoes;
- traces;
- logs;
- incidentes;
- cotas em uso;
- auditoria operacional;
- risco;
- pausas emergenciais.

## Papel Do Agente De Configuracao

O agente lateral esta bem definido.

Ele deve:

- contextualizar a etapa;
- explicar impacto;
- responder duvidas;
- sugerir defaults;
- apontar bloqueios;
- diferenciar pronto agora de depois do go-live;
- recomendar ajuda humana quando fizer sentido.

Ele nao deve:

- virar formulario principal;
- duplicar perguntas do centro;
- mudar ordem das etapas;
- publicar sozinho;
- configurar fluxos de agente;
- abrir control planes;
- esconder bloqueios em conversa.

## Operacao Com 0, 1, 3 Ou 7 Agentes

A arquitetura cobre todos os casos.

Com 0 agentes:

- CRM opera manualmente;
- Hoje, Alunos, Agenda, Financeiro e Tarefas funcionam sem dependencia de IA;
- setup continua valido.

Com agentes inclusos:

- agentes podem aparecer apenas como informacao/preparacao;
- pacotes recomendados podem virar rascunho/pendencia pos-go-live;
- fluxos nao sao ativados no Setup Inicial.

Regra:

- autonomia de agente nunca e publicada no Setup Inicial.

## Auditoria De Conflitos Encontrados

### Conflito 1 - Rotas antigas de importacao e consumo

Alguns docs antigos ainda citam:

- `/onboarding/importacao`;
- `/onboarding/configuracoes/consumo-aulas`.

Decisao final:

- importacao entra nos blocos `Alunos` e `Turmas`;
- planos e consumo entram no bloco `Planos`;
- pagamento entra no bloco `Pagamento`;
- nao criar essas rotas como experiencia principal do MVP.

### Conflito 2 - Pagamento pedindo detalhes demais

Alguns trechos antigos citavam:

- chave Pix;
- instrucao para aluno;
- responsavel por confirmar;
- configuracao por meio.

Decisao final:

- no Setup Inicial, Pagamento so seleciona meios aceitos;
- comprovante sempre permitido;
- instrucoes para aluno ficam para comunicacao/automacoes depois;
- detalhes tecnicos ficam para Pagamentos Taliya pos-go-live.

### Conflito 3 - Numeracao antiga 8 blocos

Imagens antigas mostram 8 blocos.

Decisao final:

- sequencia oficial tem 9 blocos;
- `Pagamento` e o Bloco 5;
- `Alunos`, `Turmas` e `Agenda` devem ser reinterpretados como blocos 6, 7 e 8.

### Conflito 4 - Unidade principal/multiplas unidades

Alguns documentos antigos citam unidade principal e mais de uma unidade.

Decisao final:

- nao configurar multiplas unidades no MVP do Setup Inicial;
- isso vai para Configuracoes do CRM depois.

### Conflito 5 - Tipos de aula

Alguns documentos antigos citam tipos principais de aula.

Decisao final:

- no MVP, nao abrir configuracao de tipos de aula;
- tudo pode ser tratado como aula, com planos/turmas/agenda dando o contexto operacional;
- tipos/modalidades podem virar configuracao pos-go-live.

## Lacunas Reais Ainda Pendentes

Estas lacunas nao bloqueiam a arquitetura, mas precisam ser decididas antes da implementacao completa:

1. `Publicacao parcial`
   - definir se o MVP publica itens seguros por camada ou se exige resolver bloqueios antes de publicar tudo.
   - recomendacao: permitir aviso, mas nao publicar item com bloqueio real.

2. `Objeto de pendencia`
   - definir schema tecnico da pendencia rastreavel.
   - recomendacao: criar entidade unica para pendencias do setup e pos-go-live.

3. `Destino pos-go-live`
   - definir rotas finais para Pagamentos Taliya, Agentes/Fluxos, Control Planes e Configuracoes.

4. `Dados importados de fonte fisica`
   - definir limites de confianca, revisao obrigatoria e armazenamento de origem.

5. `Convites de equipe`
   - definir evento exato que envia convites: publicacao total, publicacao parcial ou publicacao da camada CRM.

6. `Bloqueios por camada`
   - definir se bloqueio em aluno impede todo setup ou apenas aquele aluno.
   - recomendacao: bloquear o item afetado; bloquear todo setup apenas quando a camada minima fica inviavel.

## Documentos Com Trechos Legados A Revisar

Estes documentos ainda podem conter decisoes antigas. Eles continuam uteis como historico e contexto, mas nao devem prevalecer sobre esta auditoria final:

- `setup-screens-blueprint.pt-BR.md`
  - ainda descreve rotas separadas de importacao e consumo de aulas;
  - ainda descreve blocos antigos de `/onboarding/setup`;
  - deve ser atualizado para refletir a sequencia oficial de 9 blocos.

- `setup-initial-configuration-scope.pt-BR.md`
  - ainda cita alguns itens que foram simplificados depois, como multiplas unidades, tipos de aula e detalhes minimos de pagamento;
  - deve manter o principio de escopo, mas alinhar exemplos ao fluxo final.

- `setup-configuration-inventory.pt-BR.md`
  - e inventario interno e nao lista de campos do onboarding;
  - deve continuar sendo lido com essa ressalva.

- `setup-partial-publishing-rules.pt-BR.md`
  - ainda esta em rascunho consolidado;
  - precisa ser convertido em contrato tecnico de publicacao parcial antes da implementacao backend.

Antes de implementar, o time deve usar esta auditoria como fonte final e consultar os documentos acima apenas para contexto.

## Checklist De Implementacao

Antes de implementar UI:

- usar sequencia oficial de 9 blocos;
- usar `51A`, `51B` e `51C` como base visual;
- ajustar numeracao de `51H`, `51I` e `51J` em codigo;
- nao criar rotas soltas de importacao/consumo;
- manter o agente lateral contextual;
- criar pendencias como objetos rastreaveis;
- separar bloqueio, aviso e depois do go-live;
- garantir que `Publicar setup inicial` exige confirmacao;
- desabilitar publicacao quando houver bloqueio real;
- salvar rascunho por bloco;
- auditar mudancas sensiveis.

Antes de implementar backend:

- modelar workspace/studio;
- modelar equipe e convites preparados;
- modelar canais;
- modelar planos;
- modelar meios aceitos;
- modelar alunos ativos;
- modelar turmas;
- modelar agenda semanal base;
- modelar pendencias;
- modelar publicacao/versionamento do setup;
- modelar auditoria inicial.

Antes de implementar agentes:

- nao ativar fluxos no Setup Inicial;
- expor apenas o Agente de Configuracao lateral;
- criar pendencias pos-go-live para agentes/fluxos quando aplicavel;
- manter control planes fora do setup.

## Criterios De Aceite Do Setup Como Conjunto

O Setup Inicial esta pronto para implementacao quando:

- o usuario consegue sair do pagamento e iniciar `/onboarding`;
- o nome do studio cria o contexto inicial;
- o diagnostico prepara defaults sem configurar;
- os 9 blocos guiam o usuario em ordem;
- cada bloco tem poucos campos e validacao clara;
- importacoes viram rascunho revisavel;
- fontes fisicas e digitais sao aceitas;
- cada pendencia tem destino;
- a revisao mostra publicado agora, pendencias e depois do go-live;
- publicacao exige confirmacao;
- CRM manual funciona mesmo sem agentes;
- agentes e automacoes profundas ficam para pos-go-live;
- control planes nao aparecem como builder de fluxo;
- o usuario entende que o setup inicial e suficiente para comecar, mas nao e o fim das configuracoes.

## Conclusao

O Setup Inicial esta arquiteturalmente consistente.

Ele ficou simples no que pede ao usuario e robusto no que valida por tras.

O ponto mais importante para a implementacao e respeitar a fronteira:

- Setup Inicial publica o CRM operacional minimo.
- Configuracoes pos-go-live refinam o CRM.
- Agentes/Fluxos configuram autonomia.
- Control Planes governam execucao, risco, uso e auditoria.

Se essa fronteira for mantida, o Taliya pode comecar simples sem parecer fraco, e pode crescer depois sem confundir o dono do studio no primeiro acesso.
