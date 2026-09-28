# Taliya CRM - Contrato Detalhado De Integracoes Tecnicas

Status: contrato detalhado v1.
Data: 2026-05-25.

## Objetivo

Definir, de uma vez, como funcionam as integracoes tecnicas do Taliya CRM no MVP e no pos-go-live, sem misturar integracao com configuracao de negocio, agente, control plane ou billing da Taliya.

Este documento detalha:

1. WhatsApp Business.
2. Google Agenda.
3. Pagamentos Taliya / provedor financeiro.
4. E-mail.
5. Importacoes contextuais.

## Regras Gerais

Integracao tecnica e a camada que conecta o Taliya a um provedor ou fonte externa.

No MVP, essa camada **nao vira um hub separado de Integracoes para o dono**.

Ela aparece dentro da pagina que usa a conexao:

- WhatsApp em `/app/configuracoes/canais`;
- Pagamentos Taliya em `/app/configuracoes/financeiro/pagamentos`;
- Google Agenda/importacao em `/app/configuracoes/agenda` ou no job contextual;
- e-mail em `/app/configuracoes/canais` ou `/app/configuracoes/notificacoes`;
- importacoes dentro do contexto de Alunos, Turmas, Planos ou Agenda.

Ela responde:

- esta conectado?
- qual conta/numero/calendario/provedor esta conectado?
- qual permissao foi concedida?
- qual foi o ultimo evento?
- o que falhou?
- qual parte do CRM foi afetada?
- existe acao segura para reconectar, testar ou reprocessar?

Ela nao responde:

- qual plano o aluno compra;
- qual turma existe;
- qual mensagem automatica sera enviada;
- qual agente age sozinho;
- qual politica comercial o studio usa;
- qual plano Taliya o cliente contratou.

## Estrutura De Superficies

### Sem `/app/integracoes` como hub do MVP

Nao criar uma pagina central de integracoes para o dono no MVP.

Motivo:

- duplicaria Canais, Pagamentos, Agenda e Notificacoes;
- faria o dono sair do contexto onde precisa resolver o problema;
- deixaria a experiencia mais tecnica do que operacional;
- quebraria a regra de configuracao simples.

### Detalhe tecnico dentro da configuracao

Cada configuracao que depende de provedor pode abrir uma subarea/drawer tecnico.

Mostra:

- status;
- conta conectada;
- permissao concedida;
- areas afetadas;
- saude tecnica;
- ultimas falhas;
- acoes seguras;
- logs compactos quando necessario.

### Logs tecnicos compactos

Logs tecnicos filtraveis.

Mostra:

- eventos;
- status;
- erro legivel;
- objeto afetado;
- tentativa;
- idempotencia;
- acao possivel;
- incidente relacionado.

Onde fica:

- Canais: logs do WhatsApp/e-mail.
- Pagamentos e financeiro: logs do provedor financeiro.
- Agenda/importacao: logs da importacao ou calendario.
- Notificacoes: falhas de entrega interna.

## Status Padrao

| Status | Uso |
|---|---|
| `nao_conectada` | Nunca conectou ou foi removida. |
| `pendente` | Precisa de acao do dono, Taliya ou provedor. |
| `conectada` | Operando normalmente. |
| `limitada` | Funciona parcialmente. |
| `falhou` | Falha com impacto operacional. |
| `indisponivel` | Provedor fora ou instavel. |
| `pausada` | Pausada por seguranca. |
| `requer_reconexao` | Permissao expirou, foi revogada ou precisa novo login. |

## 1. WhatsApp Business

### Decisao

WhatsApp Business e integracao essencial do Taliya CRM.

Ela pode ficar pendente no Setup Inicial, mas o CRM deve deixar claro que recursos de Inbox, envios e agentes que dependem de WhatsApp so funcionam plenamente depois da conexao oficial.

### Onde Aparece

Para o dono:

- Setup Inicial, bloco Canais;
- `/app/configuracoes/canais`;
- `/app/inbox`;
- `/app/envios`;
- `/app/agentes` e `/app/fluxos`, quando houver agentes.

O detalhe tecnico e os logs do WhatsApp ficam dentro de `/app/configuracoes/canais`, quando necessario.

### O Que O Usuario Faz

No Setup Inicial:

- informa o numero WhatsApp Business do studio;
- entende que a conexao oficial pode ficar para depois;
- continua o setup mesmo se WhatsApp ainda nao estiver conectado.

No pos-go-live:

- clica em conectar/reconectar WhatsApp;
- passa pelo fluxo oficial do provedor;
- confirma permissoes;
- testa envio/recebimento;
- acompanha status e falhas.

### O Que A Taliya Faz

- cria ou vincula a conexao tecnica;
- recebe webhooks de mensagem;
- registra conversa e mensagem;
- cria tentativa de envio;
- registra status de entrega/falha;
- aplica idempotencia;
- registra logs;
- cria pendencia quando a conexao falha;
- bloqueia ou degrada fluxos dependentes.

### Fonte Da Verdade

| Dado | Fonte |
|---|---|
| Contato, aluno, conversa e estado operacional | CRM Taliya |
| Mensagem recebida, status de entrega e falha tecnica | Provedor WhatsApp |
| Opt-out e permissao operacional | CRM Taliya, respeitando evento mais restritivo |
| Template aprovado quando exigido pelo canal | Provedor + CRM |

### Impactos No CRM

WhatsApp afeta:

- Inbox;
- Conversas;
- Envios;
- Atendimento;
- Vendas;
- Agenda;
- Financeiro;
- Notificacoes;
- Agentes/Fluxos;
- Uso/cotas.

### Falhas Padrao

| Falha | Resultado |
|---|---|
| Numero nao conectado | Inbox oficial e envios automatizados ficam indisponiveis. |
| Webhook nao chega | Mensagens podem atrasar ou nao aparecer. |
| Envio falhou | SendAttempt fica com erro e pode gerar tarefa/pendencia. |
| Template bloqueado | Envio externo fica limitado. |
| Permissao revogada | Integracao vira `requer_reconexao`. |
| Provedor indisponivel | Integracao vira `indisponivel` ou `falhou`. |

### Acoes Seguras

Permitidas para dono/admin:

- conectar;
- reconectar;
- testar envio;
- testar recebimento;
- pausar envio externo;
- abrir logs;
- abrir suporte;
- abrir incidente.

Permitidas para agente:

- explicar erro;
- explicar impacto;
- sugerir proxima acao;
- resumir logs;
- preparar ticket.

Nao permitido para agente:

- conectar sozinho;
- desconectar sozinho;
- conceder permissao;
- enviar mensagem sensivel sem regra/aprovacao;
- ignorar opt-out.

### O Que Nao Entra Aqui

- texto de mensagem automatica;
- cadencia de follow-up;
- modo manual/copiloto/autonomo;
- templates globais como builder;
- politica de atendimento;
- configuracao de agente.

Esses pontos vao para contexto operacional, comunicacao ou Agentes/Fluxos.

## 2. Google Agenda

### Decisao

Google Agenda entra no MVP como **importacao assistida por agente**.

Nao entra como sincronizacao viva obrigatoria.

Nao entra como fonte operacional de verdade.

Depois que a agenda do Taliya for publicada, o CRM Taliya vence.

### Onde Aparece

Para o dono:

- Diagnostico, como resposta possivel para onde esta a agenda atual;
- Setup Inicial, nos blocos Alunos e Turmas quando a fonte de dados for Google Agenda;
- importacoes contextuais em Alunos, Turmas e Agenda;
- `/app/configuracoes/agenda`, quando houver pendencia de calendario externo, permissao expirada ou importacao de calendario para revisar;
- logs compactos dentro do job contextual ou da configuracao de Agenda.

### O Que O Usuario Faz

No Setup Inicial:

- escolhe importar a partir do Google Agenda quando chegar no bloco correto;
- conecta a conta Google;
- escolhe calendario;
- escolhe periodo a importar;
- revisa rascunhos gerados pelo agente;
- aprova, corrige ou ignora sugestoes.

No pos-go-live:

- pode importar novamente um periodo;
- pode reconectar se a permissao expirar;
- pode remover acesso;
- pode revisar historico da importacao.

### O Que O Agente Faz

O agente ajuda a:

- ler eventos;
- encontrar padroes recorrentes;
- sugerir turmas;
- sugerir horarios;
- sugerir alunos/vinculos quando nomes aparecem;
- identificar eventos que parecem aula;
- separar eventos pessoais ou irrelevantes;
- marcar baixa confianca;
- criar pendencias revisaveis.

O agente nao publica sozinho.

### O Que A Taliya Faz

- conecta com permissao do usuario;
- le eventos do calendario escolhido;
- cria job de importacao;
- normaliza eventos;
- gera rascunhos;
- registra origem;
- calcula confianca;
- registra logs;
- nao sobrescreve dado critico sem revisao.

### Fonte Da Verdade

| Dado | Fonte |
|---|---|
| Eventos importados | Google Agenda como fonte de entrada |
| Turmas, aulas, alunos e agenda publicados | CRM Taliya |
| Conflitos e pendencias | CRM Taliya |
| Revisao/aprovacao | Usuario autorizado |

### Dados Que Podem Ser Extraidos

De um evento do Google Agenda, o Taliya pode tentar extrair:

- nome da turma;
- dia da semana;
- horario;
- recorrencia;
- duracao;
- professor, se aparecer;
- aluno, se aparecer;
- observacao;
- local, se existir;
- sinal de bloqueio/feriado, se o evento indicar isso.

### Dados Obrigatoriamente Revisaveis

Precisam de revisao quando:

- nome do aluno for incerto;
- evento tiver muitos nomes;
- evento parecer pessoal;
- recorrencia estiver incompleta;
- horario cair fora da janela do studio;
- turma sugerida conflitar com turma existente;
- aluno nao existir no CRM;
- mesmo evento parecer turma e agenda ao mesmo tempo.

### Falhas Padrao

| Falha | Resultado |
|---|---|
| Permissao Google expirada | Importacao para ate reconectar. |
| Calendario vazio | Agente orienta outro calendario/periodo. |
| Muitos eventos irrelevantes | Agente separa baixa confianca. |
| Evento duplicado | Vai para revisao. |
| Dados insuficientes | Vira pendencia, nao publica direto. |

### Acoes Seguras

Permitidas:

- conectar;
- escolher calendario;
- importar periodo;
- cancelar job;
- revisar rascunhos;
- aprovar rascunhos;
- remover acesso;
- ver logs.

Nao permitido:

- sincronizar vivo por padrao;
- escrever de volta no Google Agenda no MVP;
- criar turmas/alunos sem revisao quando houver baixa confianca;
- sobrescrever agenda publicada.

## 3. Pagamentos Taliya / Provedor Financeiro

### Decisao

Pagamentos Taliya e a integracao pos-go-live com o provedor financeiro para permitir automacoes financeiras dentro do CRM.

No Setup Inicial, Pagamentos Taliya nao e configurado.

No Setup Inicial, o studio so escolhe meios aceitos para operar manualmente no comeco:

- Pix;
- dinheiro;
- cartao.

No pos-go-live, Pagamentos Taliya pode ativar:

- Pix automatico;
- cartao online;
- recorrencia automatica;
- baixa automatica;
- webhooks;
- conciliacao.

O studio nao escolhe provedor. A Taliya oferece uma experiencia propria e escolhe/gerencia o provedor por tras.

### Onde Aparece

Para o dono:

- `/app/configuracoes/financeiro/pagamentos`;
- `/app/financeiro`;
- `/app/financeiro/movimentacoes`.

O detalhe tecnico e os logs do provedor financeiro ficam dentro de `/app/configuracoes/financeiro/pagamentos`, quando necessario.

No Setup Inicial:

- nao aparece como integracao ativa;
- nao inicia provedor;
- nao abre KYC;
- nao configura Pix automatico;
- nao configura cartao online;
- nao configura recorrencia;
- pode ser citado apenas como automacao financeira que ficara para depois.

### O Que O Usuario Faz

No Setup Inicial:

- seleciona meios aceitos;
- entende a operacao inicial de baixa manual;
- nao configura chave Pix, gateway, recorrencia ou KYC.

No pos-go-live:

- clica em ativar Pagamentos Taliya;
- entra no fluxo seguro do provedor/Taliya;
- informa dados legais/bancarios no ambiente apropriado;
- aguarda aprovacao/validacao;
- ativa capacidades disponiveis;
- acompanha falhas e conciliacao na propria pagina de Pagamentos e financeiro.

### O Que A Taliya Faz

- cria a relacao tecnica com o provedor;
- recebe webhooks;
- confirma pagamento;
- atualiza cobranca;
- registra baixa;
- libera saldo/aulas quando aplicavel;
- registra falhas;
- registra idempotencia;
- apoia conciliacao;
- cria pendencia quando pagamento nao casa com cobranca.

### Fonte Da Verdade

| Dado | Fonte |
|---|---|
| Plano, aluno, cobranca e regra comercial | CRM Taliya |
| Confirmacao tecnica de pagamento | Provedor financeiro |
| Baixa manual | Usuario autorizado no CRM |
| Baixa automatica | Webhook/processamento Taliya |
| Comprovante | Evidencia anexada, nao confirmacao final se houver divergencia |

### Fluxo Base

1. Plano gera cobranca.
2. Aluno paga por meio aceito.
3. Pagamento chega manualmente ou pelo provedor.
4. Taliya registra a baixa.
5. Cobranca fica paga.
6. Direito de aula/saldo e atualizado.

### Capacidades

| Capacidade | Entra onde | Observacao |
|---|---|---|
| Pix aceito | Setup Inicial | Apenas meio aceito para registro manual no comeco. |
| Dinheiro aceito | Setup Inicial | Apenas meio aceito para registro manual no comeco. |
| Cartao aceito | Setup Inicial | Apenas meio aceito para registro manual no comeco. |
| Pix automatico | Pagamentos Taliya | Depende de provedor/webhook. |
| Cartao online | Pagamentos Taliya | Depende de provedor. |
| Recorrencia automatica | Pagamentos Taliya | Debito/tentativa automatica. |
| Baixa automatica | Pagamentos Taliya | Confirmada por provedor. |
| Conciliacao | Pagamentos Taliya/Financeiro | Ajuda a casar pagamentos. |

### Falhas Padrao

| Falha | Resultado |
|---|---|
| Webhook nao chegou | Baixa automatica pode atrasar. |
| Pagamento sem match | Vai para conciliacao. |
| Cartao recusado | Cobranca segue em aberto/falha. |
| Recorrencia falhou | Cria pendencia e possivel cobranca/aviso. |
| Provedor indisponivel | Automacao financeira degrada. |
| Divergencia com comprovante | Fica em analise/revisao. |

### Acoes Seguras

Permitidas:

- ativar Pagamentos Taliya;
- testar conexao;
- ver status;
- ver logs;
- reprocessar webhook seguro;
- abrir conciliacao;
- abrir suporte/incidente.

Nao permitido para agente:

- ativar provedor sozinho;
- trocar conta recebedora;
- perdoar pagamento;
- conceder desconto;
- confirmar pagamento duvidoso sem regra/aprovacao;
- alterar Billing Taliya.

## 4. E-mail

### Decisao

Existem dois contextos diferentes.

### 4.1 E-mail Da Taliya Para Leads Da Propria Taliya

Esse e-mail pertence ao backoffice/comercial interno da Taliya.

Nao e configuracao do cliente.

Nao aparece em `/app/integracoes` do studio.

Onde aparece:

- `/internal/leads`;
- funil comercial da Taliya;
- automacoes/comunicacoes internas da Taliya, se existirem.

Funcao:

- falar com interessados em contratar Taliya;
- enviar acompanhamento comercial;
- apoiar onboarding antes do studio virar tenant ativo.

Nao impacta:

- CRM do studio;
- Canais do studio;
- Inbox do studio;
- configuracoes do studio.

### 4.2 E-mail Do Studio No CRM

So vira integracao tecnica se o Taliya enviar e-mail em nome do studio.

Se for apenas um e-mail cadastrado para contato, fica em Canais.

### Onde Aparece

Quando houver envio real em nome do studio:

- `/app/configuracoes/canais`;
- `/app/configuracoes/notificacoes`;
- logs compactos dentro da configuracao que usa o envio.

### Usos Possiveis No CRM

- convite de equipe;
- notificacao interna;
- comunicacao administrativa;
- e-mail transacional para aluno, se decidido depois.

### Fonte Da Verdade

| Dado | Fonte |
|---|---|
| E-mail de contato do studio | CRM Canais |
| Destinatario e contexto | CRM |
| Entrega/falha/bounce | Provedor de e-mail |
| Template/mensagem | Contexto que usa a mensagem |

### Falhas Padrao

| Falha | Resultado |
|---|---|
| Remetente nao verificado | Envio em nome do studio fica bloqueado. |
| Bounce | Notificacao/convite pode nao chegar. |
| Provedor indisponivel | Envio degrada. |
| E-mail invalido | Pendencia no usuario/contato. |

### Acoes Seguras

Permitidas:

- verificar remetente;
- testar envio;
- ver logs;
- reconectar;
- trocar e-mail de contato em Canais.

Nao permitido:

- campanha;
- disparo em massa sem regra propria;
- builder global de template;
- substituir Inbox.

## 5. Importacoes Contextuais

### Decisao

Importacao nao e uma integracao viva principal.

Ela e um mecanismo contextual para transformar fontes externas em rascunhos revisaveis.

No MVP, importacao aparece dentro das areas que precisam dela, principalmente:

- Alunos;
- Turmas;
- Planos, se necessario;
- Financeiro antigo, se existir depois;
- Setup Inicial.

### Fontes Aceitas

| Fonte | Uso |
|---|---|
| Planilha | Alunos, turmas, planos, contatos. |
| Google Agenda | Eventos, horarios, recorrencias, possiveis turmas/alunos. |
| Foto/anotacao | Caderno, ficha, print, quadro de horarios. |
| PDF | Lista exportada, documento antigo, grade. |
| Lista colada | Nomes, telefones, horarios. |
| Cadastro manual | Um item por vez. |

### Onde Aparece

Setup Inicial:

- bloco Alunos;
- bloco Turmas;
- indiretamente bloco Agenda, mas a agenda publicada deve nascer das turmas revisadas.

Pos-go-live:

- `/app/alunos`;
- `/app/turmas`;
- `/app/configuracoes/financeiro/modelos`, se importar planos;
- `/app/financeiro`, se importar financeiro antigo no futuro;
- rota de job/detalhe se necessario: `/app/importacao/[jobId]`.

### O Que O Usuario Faz

- escolhe a area;
- escolhe fonte;
- envia arquivo/foto ou conecta fonte;
- espera processamento;
- revisa rascunhos;
- corrige dados;
- aprova ou ignora itens;
- resolve duplicidades.

### O Que O Agente Faz

- interpreta fonte;
- extrai campos provaveis;
- sugere estrutura;
- identifica duplicidades;
- marca confianca;
- explica pendencias;
- ajuda a corrigir;
- nao publica sozinho.

### O Que A Taliya Faz

- cria job;
- armazena origem segura;
- processa dados;
- normaliza campos;
- calcula confianca;
- cria rascunhos;
- gera pendencias;
- registra log;
- preserva rastreabilidade da origem.

### Fonte Da Verdade

| Dado | Fonte |
|---|---|
| Arquivo/foto/lista original | Fonte de entrada |
| Rascunho extraido | Taliya importacao |
| Registro publicado | CRM da area responsavel |
| Revisao final | Usuario autorizado |

### Regras De Confianca

Pode seguir com aviso:

- aluno sem plano;
- professor ausente;
- observacao incompleta;
- origem pouco clara mas nao critica.

Precisa revisao:

- telefone faltando;
- possivel duplicidade;
- turma sem horario;
- evento ambiguo;
- plano nao reconhecido;
- aluno nao encontrado.

Bloqueia publicacao:

- aluno sem nome ou contato minimo;
- turma sem dia/horario/capacidade quando for publicar turma;
- agenda essencial impossivel de montar;
- conflito critico nao resolvido.

### Falhas Padrao

| Falha | Resultado |
|---|---|
| Arquivo ilegivel | Pedir nova fonte ou revisao manual. |
| Foto ruim | Agente pede recorte/foto melhor. |
| Muitos duplicados | Criar fila de revisao. |
| Baixa confianca | Nao publica direto. |
| Job falhou | Permite reprocessar se seguro. |
| Fonte sem dados uteis | Orienta fonte alternativa. |

### Acoes Seguras

Permitidas:

- reprocessar job;
- aprovar rascunho;
- editar rascunho;
- ignorar item;
- mesclar duplicidade;
- abrir pendencia;
- ver origem.

Nao permitido:

- sobrescrever dados sensiveis sem revisao;
- mesclar aluno em baixa confianca;
- publicar importacao inteira sem validacao minima;
- transformar planilha permanente em fonte viva do CRM.

## Mapa De Dependencias

| Integracao | Depende de | Afeta | Se falhar |
|---|---|---|---|
| WhatsApp Business | Provedor WhatsApp, numero oficial, permissao | Inbox, Envios, Atendimento, Agentes | Pausa/degrada envios e fluxos dependentes |
| Google Agenda | Conta Google, calendario, permissao de leitura | Importacao, Alunos, Turmas, Agenda | Importacao para; CRM segue operando |
| Pagamentos Taliya | Provedor financeiro, webhook, conta validada | Financeiro, cobrancas, saldo/aulas | Baixa automatica para; baixa manual continua |
| E-mail do studio | Remetente/provedor, se houver envio real | Convites, notificacoes, comunicacoes | Envio por e-mail falha; CRM segue |
| Importacoes | Arquivo/fonte/job/processamento | Alunos, Turmas, Planos, Agenda | Rascunhos nao entram; dados existentes seguem |

## Relacao Com Agentes/Fluxos

Agente pode usar integracao como ferramenta ou dependencia.

Mas a configuracao de autonomia nao fica em Integracoes.

Exemplos:

- agente de atendimento depende de WhatsApp conectado;
- agente de agenda pode usar dados importados do Google Agenda;
- agente financeiro pode depender de Pagamentos Taliya;
- agente de configuracao ajuda a explicar erros e orientar conexao.

Se a integracao falhar:

- o agente deve saber que a ferramenta esta indisponivel;
- o fluxo deve degradar;
- o CRM deve abrir pendencia/incidente quando necessario;
- o usuario deve ser levado ao lugar correto.

## Relacao Com Control Planes

Integracoes embutidas mostram saude tecnica por provedor no contexto da configuracao.

Control Planes mostram impacto operacional.

Exemplo:

- Configuracao de Canais mostra webhook do WhatsApp falhando.
- Control Plane mostra quais envios, fluxos e alunos foram afetados.

## Decisao Final

No MVP:

- WhatsApp Business e integracao essencial.
- Google Agenda entra como importacao assistida por agente.
- Pagamentos Taliya entra como integracao pos-go-live com provedor financeiro para automacao financeira.
- E-mail da Taliya para leads e interno e nao pertence ao CRM do studio.
- E-mail do studio so vira integracao se houver envio real em nome do studio.
- Importacao e contextual e revisavel, nao conexao viva.
- Nao existe hub visual `/app/integracoes` para o dono.
- Detalhes tecnicos aparecem dentro da configuracao especifica.

Isso fecha o mapa de Integracoes Tecnicas sem criar complexidade desnecessaria para o dono do studio.
