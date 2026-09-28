# Taliya CRM - Agente Agenda: Paginas, Conteudo E Dinamicas

Status: contrato funcional v0.1.
Data: 2026-05-21.

## Objetivo

Mapear todas as paginas do Agente Agenda em Agentes/Fluxos:

- o que existe em cada pagina;
- o que cada pagina mostra;
- o que cada acao faz;
- o que muda dinamicamente;
- como perfis de rotina configuram os fluxos;
- como o usuario personaliza fluxos sem precisar configurar todos manualmente.

Este documento segue as decisoes de:

- `agents-flows-routines-pages-final-contract.pt-BR.md`
- `agents-flows-routine-profile-map.pt-BR.md`

## Regra Central

```text
Agente Agenda nao tem configuracoes proprias.
Rotina organiza.
Perfil da rotina configura varios fluxos de uma vez.
Fluxo so e aberto quando precisa personalizar.
```

Responsaveis, aprovadores e filas humanas sao herdados da rotina.
O fluxo so mostra esses campos quando precisa trocar o padrao ou quando a aprovacao/excecao exige alguem especifico.

## Rotinas Do Agente Agenda

| Rotina | Fluxos |
|---|---|
| Presenca e faltas | B1 Confirmacao de presenca; B2 Falta com aviso; B3 No-show; B14 Correcao de presenca |
| Vagas, reposicoes e lista de espera | B4 Recuperar vaga aberta; B5 Reposicao/remarcacao; B6 Lista de espera; B13 Creditos reposicao |
| Grade e capacidade | B8 Mudanca horario fixo; B9 Cancelamento pelo studio; B10 Conflito capacidade; B11 Ajuste de grade |
| Primeira aula e aulas especiais | B15 Primeira aula; B16 Aula especial/workshop |
| Agenda experimental | B7 Disponibilidade experimental; B12 Experimental no-show |

Total: 5 rotinas, 16 fluxos.

## Paginas

### 1. Visao Geral Do Agente Agenda

Rota:

```text
/app/agentes/agenda
```

Funcao:

Mostrar as rotinas do Agente Agenda e levar o usuario para uma rotina.

Nao configura fluxo, rotina, canal, template ou tom.

Imagem aprovada:

```text
53_round-4.1L_agentes_02_agente-agenda-rotinas-aprovado.png
```

#### Conteudo Da Pagina

Topo:

- nome: Agente Agenda;
- breadcrumb: `Agentes / Agenda`;
- descricao curta: `Presenca, faltas, reposicoes, vagas e grade`;
- status pequeno do agente: contratado, nao contratado, pausado ou bloqueado;
- frase de orientacao opcional: `Escolha uma rotina para ajustar, simular ou publicar.`

Lista de rotinas:

- Presenca e faltas;
- Vagas, reposicoes e lista de espera;
- Grade e capacidade;
- Primeira aula e aulas especiais;
- Agenda experimental.

Cada card de rotina mostra:

- nome;
- descricao curta;
- quantidade de fluxos;
- status;
- CTA principal `Abrir rotina`.

Nao mostra:

- KPIs;
- cota;
- filtros;
- atividade recente;
- lista dos 16 fluxos;
- graficos;
- painel lateral;
- Agente de Configuracao;
- chat;
- drawer;
- configuracoes de modo;
- templates;
- tom de voz;
- aprovacoes detalhadas.

#### CTAs Por Card De Rotina

| Estado da rotina | CTA principal nesta pagina | Observacao |
|---|---|---|
| Nunca configurada | Abrir rotina | Ajuste, simulacao e publicacao acontecem dentro da rotina. |
| Rascunho | Abrir rotina | Nao mostrar botao separado de continuar ajuste. |
| Rascunho simulado | Abrir rotina | Estado usado na imagem aprovada para Presenca e faltas. |
| Publicada | Abrir rotina | Operacao e ajustes ficam dentro da rotina. |
| Com excecao | Abrir rotina | O card pode mostrar chip `Excecao aberta`. |
| Com aprovacao | Abrir rotina | O card pode mostrar chip `Aprovacao pendente`. |
| Com bloqueio | Abrir rotina | O card pode mostrar chip do bloqueio principal. |
| Pausada | Abrir rotina | Retomada fica dentro da rotina. |
| Nao contratada | Ver planos ou Ver preview | Nao permite publicar. |

#### Dinamicas

Regra visual:

A composicao da pagina nao muda. Em todos os cenarios, ela continua sendo cabecalho + 5 cards de rotina.

O que muda:

- status do agente no topo;
- chip de status de cada rotina;
- CTA quando o agente nao esta contratado ou esta bloqueado.

Prioridade dos status no card:

```text
Bloqueada > Pausada > Aprovacao pendente > Excecao aberta > Rascunho simulado > Rascunho > Publicada > Nao publicada
```

| Cenario | Como aparece nesta pagina | Para onde continua |
|---|---|---|
| Plano 7 com Agenda contratada | Status `Contratado`; cards abrem normalmente. | Rotina. |
| Plano 0 agentes | Status `Nao contratado`; cards em preview/upgrade. | Planos ou preview. |
| Plano 1 sem Agenda | Agenda nao contratada; sem publicacao. | Planos ou troca de agente quando permitido. |
| Plano 1 com Agenda | Agenda abre normalmente; outras areas nao importam aqui. | Rotina. |
| Plano 3 com Agenda | Agenda abre normalmente no bundle. | Rotina. |
| Downgrade remove Agenda | Agente fica nao contratado; rotinas pausadas por entitlement. | Motivo do plano e historico. |
| Agente pausado manualmente | Status `Pausado`; cards continuam acessiveis para revisao. | Rotina. |
| Agente bloqueado | Status `Bloqueado`; card mostra bloqueio resumido. | Rotina ou origem do bloqueio. |
| WhatsApp/canal caiu | Rotinas dependentes de envio mostram `Canal bloqueado`. | Integracoes ou rotina. |
| Cota acabou | Rotinas com consumo mostram `Cota bloqueada`. | Uso/Cotas ou rotina. |
| Permissao ausente | Rotina mostra `Permissao pendente`. | Configuracoes/Equipe ou rotina. |
| Dado obrigatorio ausente | Rotina mostra `Dado pendente`. | Origem do CRM ou rotina. |
| Aprovacao pendente | Rotina mostra `Aprovacao pendente`. | Rotina ou Aprovacoes. |
| Excecao aberta | Rotina mostra `Excecao aberta`. | Rotina ou Operacao. |
| Incidente pausou rotina | Rotina mostra `Pausada por incidente`. | Incidente/control plane. |
| Fluxo personalizado | Rotina pode mostrar `Personalizada`. | Rotina. |

Se o Agente Agenda nao esta contratado:

- cards aparecem como preview/upgrade;
- nao permite publicar;
- pode mostrar simulacao de exemplo;
- caminho manual do CRM continua existindo.

Se WhatsApp caiu:

- rotinas com envio externo mostram bloqueio;
- modos autonomos que dependem de mensagem ficam indisponiveis para publicacao;
- Manual e Copiloto continuam disponiveis quando fizer sentido.

Se cota acabou:

- mostra alerta de cota;
- fluxos autonomos com consumo ficam bloqueados ou degradam pelo fallback publicado;
- card leva para Uso/Cotas.

Se ha rascunho:

- mostra "mudancas nao publicadas";
- CTA vira "Continuar ajuste".

Se ha fluxo personalizado:

- mostra "Mais autonomo personalizado" quando algum fluxo diferir do comportamento escolhido;
- mostra quantos fluxos diferem do perfil.

### 2. Pagina Da Rotina

Rota:

```text
/app/agentes/agenda/rotinas/[routineId]
```

Exemplo:

```text
/app/agentes/agenda/rotinas/presenca-e-faltas
```

Funcao:

Mostrar a rotina, seu comportamento de operacao e os fluxos incluidos.

Essa e a pagina mais importante para o dono entender o que vai acontecer.

Imagem aprovada para o modelo:

```text
54_round-4.1L_agentes_03_rotina-presenca-faltas-aprovado.png
```

#### Conteudo Da Pagina

Topo:

- nome da rotina;
- descricao curta;
- status;
- comportamento atual: Mais manual, Equilibrado, Mais autonomo ou Personalizado.

Bloco obrigatorio: comportamento da rotina.

```text
Como essa rotina deve trabalhar?

[Mais manual] [Equilibrado] [Mais autonomo]
```

Regra:

- Mais autonomo e o padrao visual quando o plano e o preflight permitem;
- a escolha se aplica aos fluxos abaixo;
- cada fluxo pode ser ajustado individualmente;
- ajuste individual deixa a rotina como personalizada.

Cards dos fluxos:

- nao mostram ID interno no titulo;
- mostram chip de modo e chip de status lado a lado no topo;
- explicam o que vai acontecer em linguagem humana;
- mostram detalhes operacionais curtos: gatilho, acao e chamada humana/aprovacao/fallback;
- CTA: `Ver e ajustar`.

Para Presenca e faltas:

| Fluxo na UI | Modo no Mais autonomo | Status |
|---|---|---|
| Confirmacao de presenca | Autonomo | Pronto |
| Falta com aviso | Autonomo com excecoes | Pronto |
| No-show | Autonomo com excecoes | Pronto |
| Correcao de presenca | Autonomo com aprovacao | Precisa aprovacao |

Acoes:

- Simular rotina;
- Ajustar fluxos;
- Revisar para publicar.

#### Dinamicas Ao Trocar Perfil

Quando o usuario troca de perfil:

- a tabela recalcula os modos dos fluxos;
- mostra antes/depois;
- explica o impacto em linguagem simples;
- preserva ajustes individuais existentes;
- marca a rotina como personalizada se houver ajuste individual;
- exige nova simulacao antes de publicar;
- cria ou atualiza rascunho.

Se clicar em "Aplicar perfil a todos":

- remove personalizacoes individuais;
- todos os fluxos voltam ao modo definido pelo perfil;
- exige nova simulacao antes de publicar.

#### Perfis Por Rotina

##### Presenca E Faltas

| Fluxo | Mais manual | Equilibrado | Mais autonomo |
|---|---|---|---|
| B1 Confirmacao de presenca | Copiloto | Direto | Direto |
| B2 Falta com aviso | Manual | Excecoes | Excecoes |
| B3 No-show | Manual | Copiloto | Excecoes |
| B14 Correcao presenca | Manual | Aprovacao | Aprovacao |

Explicacao:

- Mais manual: equipe conduz presenca e faltas; agente ajuda sob demanda.
- Equilibrado: confirmacao simples roda sozinha; falta avisada roda com excecoes; no-show vira sugestao; correcao pede aprovacao.
- Mais autonomo: confirmacao, falta clara e no-show comum rodam com excecoes; correcao auditavel continua com aprovacao.

##### Vagas, Reposicoes E Lista De Espera

| Fluxo | Mais manual | Equilibrado | Mais autonomo |
|---|---|---|---|
| B4 Recuperar vaga aberta | Copiloto | Copiloto | Excecoes |
| B5 Reposicao/remarcacao | Manual | Aprovacao | Aprovacao |
| B6 Lista de espera | Copiloto | Excecoes | Excecoes |
| B13 Creditos reposicao | Manual | Aprovacao | Aprovacao |

Explicacao:

- Mais manual: agente sugere vagas e reposicoes; equipe confirma.
- Equilibrado: lista de espera roda em casos claros; vaga aberta vira sugestao; reposicao e credito pedem aprovacao.
- Mais autonomo: agente conduz o que estiver dentro da regra e chama humano para excecoes ou impacto em credito.

##### Grade E Capacidade

| Fluxo | Mais manual | Equilibrado | Mais autonomo |
|---|---|---|---|
| B8 Mudanca horario fixo | Manual | Aprovacao | Aprovacao |
| B9 Cancelamento pelo studio | Manual | Aprovacao | Aprovacao |
| B10 Conflito capacidade | Copiloto | Aprovacao | Aprovacao |
| B11 Ajuste de grade | Manual | Aprovacao | Aprovacao |

Explicacao:

- Mais manual: rotina organiza impacto e tarefas.
- Equilibrado: agente prepara mudanca e para em aprovacao.
- Mais autonomo: agente adianta simulacao, comunicacao e preparo, mas mudanca estrutural continua exigindo aprovacao.

##### Primeira Aula E Aulas Especiais

| Fluxo | Mais manual | Equilibrado | Mais autonomo |
|---|---|---|---|
| B15 Primeira aula | Copiloto | Excecoes | Excecoes |
| B16 Aula especial/workshop | Manual | Aprovacao | Aprovacao |

Explicacao:

- Mais manual: agente organiza checklist e sugestoes.
- Equilibrado: primeira aula roda com excecoes; workshop pede aprovacao.
- Mais autonomo: primeira aula conduz casos normais; eventos continuam com aprovacao antes de publicar/comunicar.

##### Agenda Experimental

| Fluxo | Mais manual | Equilibrado | Mais autonomo |
|---|---|---|---|
| B7 Disponibilidade experimental | Copiloto | Copiloto | Excecoes |
| B12 Experimental no-show | Copiloto | Excecoes | Excecoes |

Explicacao:

- Mais manual: agente sugere horarios e abordagens.
- Equilibrado: agente sugere disponibilidade e conduz no-show experimental com excecoes.
- Mais autonomo: disponibilidade e no-show experimental rodam com excecoes e limites de contato.

### 3. Ajustar Rotina E Fluxos

Rota:

```text
/app/agentes/agenda/rotinas/[routineId]/ajustar
```

Funcao:

Ajustar o perfil da rotina e, se necessario, personalizar fluxos individuais.

Essa pagina nao deve parecer um builder de 16 fluxos.

#### Conteudo Da Pagina

Topo:

- rotina;
- perfil atual;
- se esta personalizado ou nao;
- resumo do que o perfil faz;
- alerta de bloqueios.

Bloco de perfil:

- seletor: Mais manual, Equilibrado, Mais autonomo;
- resumo do impacto;
- botao: Aplicar perfil a todos, se houver personalizacoes.

Lista de fluxos:

- nome;
- modo atual;
- origem: perfil ou ajuste individual;
- status;
- bloqueio;
- CTA: Ajustar fluxo.

Painel/drawer do fluxo:

- objetivo;
- modo atual;
- seletor de modo, limitado pelo teto do fluxo;
- origem do modo;
- como funciona no modo escolhido;
- ajustes visiveis quando necessario;
- dependencias fixas;
- fallback;
- simulacao rapida do fluxo.

#### Ajustes Visiveis Por Fluxo

##### Presenca E Faltas

| Fluxo | Ajustes visiveis quando necessario | Fixo/dependencia |
|---|---|---|
| B1 Confirmacao de presenca | quando confirmar; template/tom; tentativas; acao se nao responder; fila de excecao | WhatsApp se houver envio; aula/aluno ativos; opt-out; auditoria |
| B2 Falta com aviso | prazo para aviso; oferecer reposicao; template/tom; fila de excecao | aula existente; regra base de chamada; registro da falta |
| B3 No-show | quando considerar no-show; criar tarefa de recuperacao; template/tom; fila para casos sensiveis | chamada encerrada; aluno/aula vinculados; auditoria |
| B14 Correcao presenca | aprovador; prazo; motivo obrigatorio; fallback se ninguem aprovar | correcao exige motivo; motivos base; usuario autorizado; auditoria |

##### Vagas, Reposicoes E Lista De Espera

| Fluxo | Ajustes visiveis quando necessario | Fixo/dependencia |
|---|---|---|
| B4 Recuperar vaga aberta | antecedencia para oferecer vaga; limite de convites; template/tom; fila de excecao | capacidade da aula; elegibilidade; prioridade base; consentimento |
| B5 Reposicao/remarcacao | aprovador; prazo limite; template/tom; fallback | credito e politica vigente; conflito de agenda; auditoria |
| B6 Lista de espera | tempo para responder; limite de convites; template/tom; fila de excecao | capacidade real; prioridade e ordem auditavel; consentimento |
| B13 Creditos reposicao | aprovador; validade se variar; aviso ao aluno se houver | saldo/credito auditavel; situacoes elegiveis; motivo obrigatorio |

##### Grade E Capacidade

| Fluxo | Ajustes visiveis quando necessario | Fixo/dependencia |
|---|---|---|
| B8 Mudanca horario fixo | aprovador; antecedencia minima; template/tom de aviso; fila de excecao | impacto em aluno/turma; simulacao de conflito |
| B9 Cancelamento pelo studio | aprovador; template/tom de comunicado; prazo minimo | aula afetada; alunos impactados; opcoes oferecidas definidas pelo produto |
| B10 Conflito capacidade | aprovador; responsavel do caso | limite de capacidade; prioridade base; conflito detectado pelo CRM |
| B11 Ajuste de grade | aprovador; data de vigencia; comunicacao necessaria | simulacao obrigatoria; limite de alteracao definido pelo produto |

##### Primeira Aula E Aulas Especiais

| Fluxo | Ajustes visiveis quando necessario | Fixo/dependencia |
|---|---|---|
| B15 Primeira aula | lembrete; template/tom; fila de excecao | aluno/aula vinculados; checklist e gates obrigatorios |
| B16 Aula especial/workshop | aprovador; capacidade operacional; template/tom; prazo | evento/aula especial; limite de vagas; regra base de lista |

##### Agenda Experimental

| Fluxo | Ajustes visiveis quando necessario | Fixo/dependencia |
|---|---|---|
| B7 Disponibilidade experimental | janela de horarios oferecidos; limite de ofertas; template/tom; quando chamar humano | agenda real; consentimento; interessado vinculado |
| B12 Experimental no-show | quando abordar; tentativas; template/tom; encaminhamento humano | aula experimental registrada; historico do interessado; opt-out |

#### Dinamicas

Ao trocar o perfil:

- recalcula os modos;
- mostra diferenca;
- preserva ajustes individuais;
- exige nova simulacao.

Ao trocar o modo de um fluxo:

- mostra comportamento real naquele modo;
- muda ajustes visiveis;
- marca fluxo como ajuste individual;
- marca rotina como personalizada.

Se o modo escolhido ultrapassa o teto:

- nao aparece como opcao.

Se falta dado, canal, integracao, permissao ou cota:

- o modo aparece bloqueado com motivo;
- a tela sugere modo possivel: Manual ou Copiloto.

### 4. Simular Rotina

Rota:

```text
/app/agentes/agenda/rotinas/[routineId]/simular
```

Funcao:

Ensaiar o caminho real da rotina antes de publicar.

Simulacao nao mostra "resultado bonito". Ela mostra o que o fluxo faria no CRM e na comunicacao.

#### Conteudo Da Pagina

Coluna esquerda: cenario.

- rotina;
- perfil;
- fluxo testado;
- modo testado;
- aluno/interessado/aula ficticia ou real de teste;
- situacao do cenario;
- bloqueios;
- botao Rodar simulacao.

Centro: experiencia real.

- celular/WhatsApp quando houver mensagem;
- painel da aula/agenda quando houver mudanca interna;
- tarefa/aprovacao/excecao quando houver humano;
- status do aluno/aula.

Coluna direita: linha de execucao.

- gatilho;
- dados checados;
- integracao/canal/cota;
- acao preparada ou executada;
- ponto de aprovacao;
- ponto de excecao;
- fallback;
- auditoria.

#### Cenarios Por Rotina

Presenca e faltas:

- aluno confirma presenca;
- aluno nao responde;
- aluno avisa falta;
- aluno pede troca de horario;
- aluno falta sem avisar;
- humano corrige presenca;
- WhatsApp indisponivel;
- cota insuficiente.

Vagas, reposicoes e lista de espera:

- vaga abre antes da aula;
- aluno aceita vaga;
- aluno nao responde;
- pedido de reposicao dentro da regra;
- pedido de reposicao fora da regra;
- credito perto de vencer;
- lista de espera sem elegivel.

Grade e capacidade:

- troca de horario fixo;
- cancelamento pelo studio;
- conflito de capacidade;
- ajuste de grade com impacto;
- aprovador rejeita;
- aluno afetado responde com duvida.

Primeira aula e aulas especiais:

- primeira aula com tudo ok;
- primeira aula com documento/gate faltando;
- workshop dentro da capacidade;
- workshop lotado;
- aprovador rejeita evento.

Agenda experimental:

- interessado pede horario disponivel;
- interessado pede horario indisponivel;
- no-show experimental;
- interessado responde com objecao;
- limite de contato atingido.

#### Dinamicas

Se perfil muda:

- simulacao anterior fica invalida;
- precisa rodar novamente antes de publicar.

Se fluxo personalizado muda:

- simulacao desse fluxo fica invalida;
- publicacao mostra pendencia.

Se cenario passa:

- status: simulado;
- pode ir para publicacao.

Se cenario falha:

- mostra motivo;
- mostra se precisa ajustar fluxo, reduzir modo ou resolver integracao/cota.

### 5. Publicar Versao

Rota:

```text
/app/agentes/agenda/rotinas/[routineId]/publicar
```

Funcao:

Transformar o rascunho simulado em versao ativa.

#### Conteudo Da Pagina

Resumo:

- rotina;
- perfil;
- versao nova;
- versao atual, se houver;
- fluxos que seguem o perfil;
- fluxos personalizados;
- ultima simulacao valida.

Quadro "O que muda ao publicar":

- vai acontecer sozinho;
- vai pedir aprovacao;
- vai chamar humano;
- continua manual/copiloto;
- fica bloqueado, se houver.

Preflight:

- permissao;
- perfil definido;
- modos validos;
- simulacao valida;
- template/tom quando houver mensagem;
- aprovador quando houver aprovacao;
- fila humana quando houver excecao;
- fallback;
- dados obrigatorios;
- integracao/canal;
- cota;
- auditoria.

Confirmacao:

- quem publica;
- impacto;
- botao Publicar versao.

#### Dinamicas

Se tudo passou:

- permite publicar;
- cria snapshot versionado;
- registra auditoria;
- rotina passa para Publicada.

Se falta simulacao:

- bloqueia publicacao;
- CTA: Simular agora.

Se falta template/tom:

- bloqueia fluxos com mensagem;
- permite ajustar.

Se falta aprovador/fila:

- bloqueia fluxos de aprovacao/excecao;
- CTA: Definir roteamento humano.

Se falta integracao/cota:

- bloqueia modo autonomo afetado;
- sugere reduzir modo ou resolver dependencia.

### 6. Execucoes Da Rotina

Rota:

```text
/app/agentes/agenda/rotinas/[routineId]/execucoes
```

Funcao:

Mostrar o que aconteceu com a rotina.

Nao configura nada.

#### Conteudo Da Pagina

Filtros:

- periodo;
- fluxo;
- modo;
- status;
- aluno;
- aula;
- com aprovacao;
- com excecao;
- com falha.

Tabela:

- horario;
- fluxo;
- perfil publicado na epoca;
- modo;
- aluno/aula;
- acao;
- status;
- humano chamado;
- cota usada;
- link para detalhe.

#### Dinamicas

Se execucao concluiu:

- CTA: Ver detalhes.

Se aguardando aprovacao:

- CTA: Revisar aprovacao.

Se chamou humano:

- CTA: Resolver excecao.

Se falhou:

- CTA: Ver falha;
- se seguro, Tentar novamente;
- senao, Criar tarefa manual.

### 7. Detalhe Da Execucao

Rota global:

```text
/app/fluxos/execucoes/[runId]
```

Funcao:

Explicar uma execucao especifica.

E Control Plane, nao configuracao.

#### Conteudo

- agente: Agenda;
- rotina;
- perfil publicado;
- fluxo;
- versao;
- modo;
- gatilho;
- dados usados;
- mensagem/acao feita;
- aprovacao, se houve;
- excecao, se houve;
- humano chamado;
- fallback;
- cota;
- auditoria;
- links para aula, aluno, tarefa, aprovacao ou conversa.

### 8. Modais E Drawers

Estas superficies nao precisam ser paginas completas.

#### Pausar Rotina

Mostra:

- o que vai parar;
- o que continua manual;
- execucoes em andamento;
- quem esta pausando;
- motivo.

Efeito:

- para autonomos da rotina;
- preserva historico;
- registra auditoria.

#### Pausar Fluxo

Mostra:

- fluxo afetado;
- motivo;
- fallback;
- impacto.

Efeito:

- para apenas aquele fluxo;
- rotina pode continuar com os demais.

#### Voltar Versao

Mostra:

- versao atual;
- versao anterior;
- diferencas;
- impacto.

Efeito:

- volta para snapshot anterior;
- exige permissao;
- exige simulacao se houver dependencia nova;
- registra auditoria.

#### Resolver Excecao

Mostra:

- contexto;
- mensagem/resposta, se houver;
- o que o agente tentou fazer;
- por que chamou humano;
- acoes possiveis.

Acoes possiveis:

- resolver;
- responder;
- transformar em tarefa;
- ajustar fluxo;
- pausar fluxo;
- abrir incidente.

#### Revisar Aprovacao

Mostra:

- acao preparada;
- impacto;
- dados usados;
- simulacao;
- aprovar;
- rejeitar;
- pedir ajuste.

## Estados Principais

### Rotina

- Nao configurada;
- Rascunho;
- Simulada;
- Publicada;
- Publicada com rascunho;
- Pausada;
- Com bloqueio;
- Com incidente.

### Fluxo

- Segue perfil;
- Personalizado;
- Bloqueado;
- Simulado;
- Ativo;
- Pausado;
- Aguardando aprovacao;
- Com excecao;
- Com falha.

### Publicacao

- Nao pronta;
- Pronta para simular;
- Simulada;
- Pronta para publicar;
- Publicada;
- Bloqueada.

## Resumo De UX

O usuario deve entender a rotina nesta ordem:

```text
1. Escolho o perfil da rotina.
2. Vejo o que muda.
3. Vejo quais fluxos ficaram em cada modo.
4. Personalizo um fluxo so se precisar.
5. Simulo o caminho real.
6. Publico uma versao.
7. Acompanho excecoes, aprovacoes e execucoes.
```

O usuario nao deve sentir que precisa configurar 16 fluxos do Agente Agenda.
