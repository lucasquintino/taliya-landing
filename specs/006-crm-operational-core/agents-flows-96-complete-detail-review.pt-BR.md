# Taliya CRM - 96 Fluxos Detalhados

Status: auditoria semantica completa v0.3.
Data: 2026-05-22.

Este documento detalha os 96 fluxos no padrao completo definido para `Falta com aviso`.

Cada fluxo tem objetivo, Inicio, Meio, Fim, ajustes, requisitos, encadeamento e simulacao.

A revisao v0.3 ajusta Inicio/Meio/Fim para o modo padrao real de cada fluxo e remove finais genericos:

- Autonomo conclui sozinho dentro dos limites e para quando nao consegue concluir.
- Autonomo com excecoes resolve sozinho o caso valido e chama a equipe quando sai dos limites.
- Autonomo com aprovacao monta pedido, mostra impacto e so aplica depois da aprovacao.
- O Fim descreve o resultado real daquele fluxo e o que acontece quando ele nao fecha.


## Agente: Atendimento


### Rotina: Conversas e triagem

#### Nova conversa

- ID interno: `A1`.
- Nome canonico: `Nova conversa`.
- Modo padrao: `Autonomo com excecoes`.
- Teto: `Autonomo com excecoes`.
- Objetivo: classificar a conversa, abrir atendimento e mandar para a fila certa.

**Inicio**

O fluxo comeca quando uma nova mensagem chega por WhatsApp, inbox ou outro canal conectado e ainda nao tem destino claro. Checagens deste fluxo: mensagem chegou por canal conectado; contato esta identificado ou pode receber resposta geral; assunto inicial foi reconhecido; fila de atendimento esta definida.

**Meio**

Trabalho do agente: classificar a conversa, abrir atendimento e mandar para a fila certa. Segue sem equipe se: mensagem chegou por canal conectado; contato esta identificado ou pode receber resposta geral; assunto inicial foi reconhecido; fila de atendimento esta definida; limite de respostas nao foi atingido.

Chama a equipe se: contato nao foi identificado; mensagem mistura varios assuntos; pedido envolve desconto, saude, privacidade ou reclamacao; fila de atendimento nao tem responsavel; canal, cota, opt-out ou permissao bloqueia resposta.

**Fim**

A conversa fica classificada, o atendimento abre na fila correta e o historico mostra por que aquele destino foi escolhido. Se houver conflito de assunto, identidade ou fila, a conversa vira caso humano no Inbox.

**Ajustes do studio**

- fila de atendimento.
- limite de respostas.
- quando chamar humano.

**Requisitos readonly**

- canal de conversa conectado.
- contato identificado quando necessario.
- templates/base permitidos.
- opt-out respeitado.
- permissao.
- cota.
- auditoria.

**Encadeamento**

/app/inbox; /app/tarefas; /app/operacao

**Simulacao deve mostrar**

mostrar gatilho, dados usados, decisao do modo escolhido, mensagem/acao, aprovacao ou chamada humana quando houver, fallback, cota e auditoria.

#### Duvidas permitidas

- ID interno: `A2`.
- Nome canonico: `Duvidas permitidas`.
- Modo padrao: `Autonomo`.
- Teto: `Autonomo`.
- Objetivo: responder duvidas permitidas usando a base aprovada.

**Inicio**

O fluxo comeca quando um lead, aluno ou responsavel faz uma pergunta que pode estar na base aprovada do studio. Checagens deste fluxo: pergunta esta na base permitida; resposta nao exige dado sensivel; contato pode receber resposta pelo canal; limite por conversa nao foi atingido.

**Meio**

Trabalho do agente: responder duvidas permitidas usando a base aprovada. Conclui sem fila humana se: pergunta esta na base permitida; resposta nao exige dado sensivel; contato pode receber resposta pelo canal; limite por conversa nao foi atingido; fallback esta definido.

Para e cria pendencia para a equipe se: pergunta nao esta na base; aluno pede condicao comercial especial; mensagem pede dado privado; conversa ficou confusa ou agressiva; canal, cota, opt-out ou permissao bloqueia resposta.

**Fim**

A resposta aprovada e enviada na conversa e a pergunta fica registrada como atendida pela base permitida. Se a pergunta sair da base, pedir dado privado ou exigir condicao especial, nasce uma tarefa de resposta para a equipe.

**Ajustes do studio**

- tom/template de resposta.
- limite por conversa.
- quando chamar humano.

**Requisitos readonly**

- canal de conversa conectado.
- contato identificado quando necessario.
- templates/base permitidos.
- opt-out respeitado.
- permissao.
- cota.
- auditoria.

**Encadeamento**

/app/inbox; tarefa de resposta

**Simulacao deve mostrar**

mostrar gatilho, dados usados, decisao do modo escolhido, mensagem/acao, aprovacao ou chamada humana quando houver, fallback, cota e auditoria.

#### Aluno existente

- ID interno: `A3`.
- Nome canonico: `Aluno existente`.
- Modo padrao: `Autonomo com excecoes`.
- Teto: `Autonomo com excecoes`.
- Objetivo: reconhecer aluno existente e encaminhar atendimento com contexto.

**Inicio**

O fluxo comeca quando uma conversa parece vir de aluno existente e precisa ser ligada ao cadastro certo antes de continuar. Checagens deste fluxo: telefone corresponde a um aluno ou responsavel permitido; cadastro nao tem conflito de identidade; pedido usa dados permitidos; fila destino esta definida.

**Meio**

Trabalho do agente: reconhecer aluno existente e encaminhar atendimento com contexto. Segue sem equipe se: telefone corresponde a um aluno ou responsavel permitido; cadastro nao tem conflito de identidade; pedido usa dados permitidos; fila destino esta definida; botao de ajuda permanece disponivel.

Chama a equipe se: telefone atende mais de um aluno; cadastro esta duplicado; pedido exige alteracao sensivel; aluno contesta informacao do CRM; canal, cota ou permissao bloqueia acao.

**Fim**

A conversa fica ligada ao cadastro certo e o atendimento segue com contexto do aluno permitido para aquela fila. Se houver telefone compartilhado, duplicidade ou pedido sensivel, a Taliya segura os dados e cria revisao humana.

**Ajustes do studio**

- fila de atendimento.
- dados que chamam humano.
- botao chamar humano.

**Requisitos readonly**

- canal de conversa conectado.
- contato identificado quando necessario.
- templates/base permitidos.
- opt-out respeitado.
- permissao.
- cota.
- auditoria.

**Encadeamento**

/app/inbox; /app/alunos/[id]; /app/tarefas

**Simulacao deve mostrar**

mostrar gatilho, dados usados, decisao do modo escolhido, mensagem/acao, aprovacao ou chamada humana quando houver, fallback, cota e auditoria.

#### Fora do escopo

- ID interno: `A4`.
- Nome canonico: `Fora do escopo`.
- Modo padrao: `Autonomo`.
- Teto: `Autonomo`.
- Objetivo: responder fora de escopo e criar destino correto.

**Inicio**

O fluxo comeca quando a pessoa pede algo que nao pertence ao escopo operacional do CRM do studio. Checagens deste fluxo: assunto nao pertence ao CRM do studio; resposta padrao esta aprovada; contato nao pediu humano; destino da tarefa ou caso esta definido.

**Meio**

Trabalho do agente: responder fora de escopo e criar destino correto. Conclui sem fila humana se: assunto nao pertence ao CRM do studio; resposta padrao esta aprovada; contato nao pediu humano; destino da tarefa ou caso esta definido; mensagem nao contem risco sensivel.

Para e cria pendencia para a equipe se: assunto parece reclamacao; mensagem envolve emergencia, saude ou dado pessoal; lead ou aluno insiste em humano; resposta padrao nao cobre o caso; canal, cota ou permissao bloqueia acao.

**Fim**

A pessoa recebe a resposta padrao de fora do escopo e, quando fizer sentido, o pedido vira tarefa/caso no destino configurado. Se o texto indicar reclamacao, emergencia, saude ou dado pessoal, o caso vai para humano.

**Ajustes do studio**

- resposta padrao.
- destino da tarefa/caso.

**Requisitos readonly**

- canal de conversa conectado.
- contato identificado quando necessario.
- templates/base permitidos.
- opt-out respeitado.
- permissao.
- cota.
- auditoria.

**Encadeamento**

/app/inbox; tarefa/caso

**Simulacao deve mostrar**

mostrar gatilho, dados usados, decisao do modo escolhido, mensagem/acao, aprovacao ou chamada humana quando houver, fallback, cota e auditoria.

#### Chamada humana

- ID interno: `A5`.
- Nome canonico: `Chamada humana`.
- Modo padrao: `Autonomo`.
- Teto: `Autonomo`.
- Objetivo: chamar humano com resumo, fila e prioridade.

**Inicio**

O fluxo comeca quando uma conversa precisa sair da automacao e ir para uma pessoa da equipe. Checagens deste fluxo: gatilho de humano foi detectado; fila destino esta definida; prioridade foi calculada; resumo obrigatorio foi gerado.

**Meio**

Trabalho do agente: chamar humano com resumo, fila e prioridade. Conclui sem fila humana se: gatilho de humano foi detectado; fila destino esta definida; prioridade foi calculada; resumo obrigatorio foi gerado; responsavel pode assumir o caso.

Para e cria pendencia para a equipe se: fila destino nao existe; prioridade nao pode ser definida; resumo ficou incompleto; caso exige dono ou admin especifico; canal, cota ou permissao bloqueia criacao.

**Fim**

O humano recebe a conversa com resumo, prioridade e fila definida. Se a Taliya nao conseguir escolher fila, prioridade ou responsavel, o caso fica em pendencia operacional ate alguem assumir.

**Ajustes do studio**

- fila de handoff.
- prioridade inicial.
- campos do resumo.

**Requisitos readonly**

- canal de conversa conectado.
- contato identificado quando necessario.
- templates/base permitidos.
- opt-out respeitado.
- permissao.
- cota.
- auditoria.

**Encadeamento**

/app/inbox; /app/operacao; fila humana

**Simulacao deve mostrar**

mostrar gatilho, dados usados, decisao do modo escolhido, mensagem/acao, aprovacao ou chamada humana quando houver, fallback, cota e auditoria.


### Rotina: Identidade e privacidade

#### Consentimento/opt-out

- ID interno: `A6`.
- Nome canonico: `Consentimento/opt-out`.
- Modo padrao: `Autonomo`.
- Teto: `Autonomo`.
- Objetivo: registrar consentimento, opt-out ou preferencia de contato.

**Inicio**

O fluxo comeca quando o contato pede consentimento, opt-out ou mudanca de preferencia de comunicacao. Checagens deste fluxo: contato foi identificado; pedido de consentimento ou opt-out e claro; texto de confirmacao esta aprovado; responsavel de revisao existe para caso ambiguo.

**Meio**

Trabalho do agente: registrar consentimento, opt-out ou preferencia de contato. Conclui sem fila humana se: contato foi identificado; pedido de consentimento ou opt-out e claro; texto de confirmacao esta aprovado; responsavel de revisao existe para caso ambiguo; auditoria pode ser registrada.

Para e cria pendencia para a equipe se: pedido e ambiguo; telefone e compartilhado; contato pede exclusao ou copia de dados; ha conflito entre responsavel e aluno; canal, cota ou permissao bloqueia confirmacao.

**Fim**

A preferencia de contato, consentimento ou opt-out fica registrado no contato e passa a valer para os proximos envios. Se o pedido for ambiguo, envolver telefone compartilhado ou pedir dados pessoais, a revisao vai para responsavel.

**Ajustes do studio**

- texto de confirmacao.
- responsavel de revisao em caso ambiguo.

**Requisitos readonly**

- canal de conversa conectado.
- contato identificado quando necessario.
- templates/base permitidos.
- opt-out respeitado.
- permissao.
- cota.
- auditoria.

**Encadeamento**

/app/contatos/[id]; auditoria; tarefa

**Simulacao deve mostrar**

mostrar gatilho, dados usados, decisao do modo escolhido, mensagem/acao, aprovacao ou chamada humana quando houver, fallback, cota e auditoria.

#### Identidade/midias

- ID interno: `A7`.
- Nome canonico: `Identidade/midias`.
- Modo padrao: `Autonomo com excecoes`.
- Teto: `Autonomo com excecoes`.
- Objetivo: tratar identidade, audio, imagem ou midia recebida.

**Inicio**

O fluxo comeca quando a conversa recebe audio, imagem, documento ou outra midia que precisa ser interpretada com cuidado. Checagens deste fluxo: midia e legivel; tipo de midia e aceito; contato esta identificado; conteudo nao traz dado sensivel inesperado.

**Meio**

Trabalho do agente: tratar identidade, audio, imagem ou midia recebida. Segue sem equipe se: midia e legivel; tipo de midia e aceito; contato esta identificado; conteudo nao traz dado sensivel inesperado; responsavel de revisao esta definido.

Chama a equipe se: midia esta ilegivel; documento parece sensivel; identidade nao confere; arquivo nao e aceito; canal, cota ou permissao bloqueia acao.

**Fim**

A midia fica vinculada ao atendimento com classificacao segura e destino de revisao quando precisar. Se o arquivo for ilegivel, sensivel, nao aceito ou a identidade nao conferir, a Taliya nao usa o conteudo e abre revisao.

**Ajustes do studio**

- responsavel de revisao.
- tipos de midia aceitos.

**Requisitos readonly**

- canal de conversa conectado.
- contato identificado quando necessario.
- templates/base permitidos.
- opt-out respeitado.
- permissao.
- cota.
- auditoria.

**Encadeamento**

/app/inbox; /app/dados/duplicidades; /app/historico/documentos

**Simulacao deve mostrar**

mostrar gatilho, dados usados, decisao do modo escolhido, mensagem/acao, aprovacao ou chamada humana quando houver, fallback, cota e auditoria.

#### Privacidade/dados

- ID interno: `A8`.
- Nome canonico: `Privacidade/dados`.
- Modo padrao: `Autonomo com aprovacao`.
- Teto: `Autonomo com aprovacao`.
- Objetivo: preparar pedido de privacidade ou dados para aprovacao.

**Inicio**

O fluxo comeca quando alguem pede acesso, exclusao, copia ou revisao de dados pessoais. Checagens deste fluxo: solicitante foi identificado; tipo de pedido de dado foi classificado; dados envolvidos foram listados; SLA do caso esta definido.

**Meio**

Pedido de aprovacao: preparar pedido de privacidade ou dados para aprovacao. O pedido mostra dados, impacto e proximo passo usando: solicitante foi identificado; tipo de pedido de dado foi classificado; dados envolvidos foram listados; SLA do caso esta definido; aprovador de privacidade esta definido.

Nao aplica sem aprovacao. Tambem cria pendencia para a equipe se: identidade nao esta confirmada; pedido envolve exclusao ou exportacao ampla; ha menor ou responsavel envolvido; dado solicitado nao esta no escopo permitido; aprovacao vence ou permissao bloqueia.

**Fim**

O pedido de privacidade vira uma aprovacao com solicitante, tipo de dado, escopo e SLA. Se aprovado, a equipe executa a resposta de dados; se recusado ou vencido, o caso fica pendente para o responsavel de privacidade.

**Ajustes do studio**

- aprovador de privacidade.
- SLA do caso.

**Requisitos readonly**

- canal de conversa conectado.
- contato identificado quando necessario.
- templates/base permitidos.
- opt-out respeitado.
- permissao.
- cota.
- auditoria.

**Encadeamento**

/app/operacao; /app/auditoria; aprovacao

**Simulacao deve mostrar**

mostrar gatilho, dados usados, decisao do modo escolhido, mensagem/acao, aprovacao ou chamada humana quando houver, fallback, cota e auditoria.

#### Telefone compartilhado e identidade

- ID interno: `A9`.
- Nome canonico: `Telefone compartilhado e identidade`.
- Modo padrao: `Autonomo com aprovacao`.
- Teto: `Autonomo com aprovacao`.
- Objetivo: validar telefone compartilhado antes de expor informacao.

**Inicio**

O fluxo comeca quando o mesmo telefone pode representar mais de um aluno, responsavel ou cadastro. Checagens deste fluxo: telefone compartilhado foi detectado; alunos possiveis foram listados; regra de validacao esta definida; responsavel de revisao esta definido.

**Meio**

Pedido de aprovacao: validar telefone compartilhado antes de expor informacao. O pedido mostra dados, impacto e proximo passo usando: telefone compartilhado foi detectado; alunos possiveis foram listados; regra de validacao esta definida; responsavel de revisao esta definido; nenhum dado sensivel sera revelado antes da validacao.

Nao aplica sem aprovacao. Tambem cria pendencia para a equipe se: mais de um aluno pode ser o solicitante; validacao falha; responsavel diverge do cadastro; pedido tenta acessar historico privado; aprovacao vence ou permissao bloqueia.

**Fim**

O telefone compartilhado fica marcado e nenhum dado sensivel e exposto antes da validacao. Se a validacao nao separar claramente aluno, responsavel e permissao, o atendimento fica com humano.

**Ajustes do studio**

- regra de validacao.
- responsavel de revisao.

**Requisitos readonly**

- canal de conversa conectado.
- contato identificado quando necessario.
- templates/base permitidos.
- opt-out respeitado.
- permissao.
- cota.
- auditoria.

**Encadeamento**

/app/contatos; /app/alunos/[id]; /app/dados/duplicidades

**Simulacao deve mostrar**

mostrar gatilho, dados usados, decisao do modo escolhido, mensagem/acao, aprovacao ou chamada humana quando houver, fallback, cota e auditoria.


### Rotina: Conversas e triagem

#### Ciclo de vida/SLA

- ID interno: `A10`.
- Nome canonico: `Ciclo de vida/SLA`.
- Modo padrao: `Autonomo`.
- Teto: `Autonomo`.
- Objetivo: acompanhar SLA e ciclo de vida do atendimento.

**Inicio**

O fluxo comeca quando uma conversa, fila ou atendimento precisa ser acompanhado por prazo, dono e status. Checagens deste fluxo: conversa tem status claro; tempo de SLA esta definido; fila destino existe; prioridade foi definida.

**Meio**

Trabalho do agente: acompanhar SLA e ciclo de vida do atendimento. Conclui sem fila humana se: conversa tem status claro; tempo de SLA esta definido; fila destino existe; prioridade foi definida; alerta ainda esta dentro da politica do studio.

Para e cria pendencia para a equipe se: SLA venceu; conversa ficou sem dono; prioridade ficou alta ou sensivel; fila destino nao existe; canal, cota ou permissao bloqueia alerta.

**Fim**

A conversa recebe status, dono, prazo e alerta de SLA. Se o SLA vencer, ficar sem dono ou virar assunto sensivel, aparece em Hoje/Tarefas para continuidade humana.

**Ajustes do studio**

- tempo de SLA.
- fila destino.
- prioridade.

**Requisitos readonly**

- canal de conversa conectado.
- contato identificado quando necessario.
- templates/base permitidos.
- opt-out respeitado.
- permissao.
- cota.
- auditoria.

**Encadeamento**

/app/inbox; /app/tarefas; /app/hoje

**Simulacao deve mostrar**

mostrar gatilho, dados usados, decisao do modo escolhido, mensagem/acao, aprovacao ou chamada humana quando houver, fallback, cota e auditoria.


## Agente: Agenda


### Rotina: Presenca e faltas

#### Confirmacao de presenca

- ID interno: `B1`.
- Nome canonico: `Confirmacao de presenca`.
- Modo padrao: `Autonomo`.
- Teto: `Autonomo`.
- Objetivo: enviar confirmacao de presenca e registrar resposta.

**Inicio**

O fluxo comeca quando chega o horario de confirmar presenca de alunos em uma aula publicada. Checagens deste fluxo: aula existe na agenda; aluno esta vinculado a aula; horario do lembrete chegou; template aprovado esta disponivel.

**Meio**

Trabalho do agente: enviar confirmacao de presenca e registrar resposta. Conclui sem fila humana se: aula existe na agenda; aluno esta vinculado a aula; horario do lembrete chegou; template aprovado esta disponivel; limite por aula nao foi atingido.

Para e cria pendencia para a equipe se: aula foi alterada ou cancelada; aluno nao esta identificado; ja existe resposta conflitante; aluno pede excecao ou troca; WhatsApp, cota ou permissao bloqueia envio.

**Fim**

A confirmacao e enviada, a resposta do aluno atualiza a aula e quem nao respondeu fica visivel para acompanhamento. Se aula, aluno, resposta ou envio tiver conflito, a pendencia fica na aula.

**Ajustes do studio**

- horario do lembrete.
- tom/template.
- limite por aula.

**Requisitos readonly**

- agenda publicada.
- aluno e aula identificados.
- regras da rotina publicadas.
- canal conectado quando houver mensagem.
- permissao.
- cota.
- auditoria.

**Encadeamento**

/app/agenda; /app/aulas/[id]; execucao

**Simulacao deve mostrar**

mostrar gatilho, dados usados, decisao do modo escolhido, mensagem/acao, aprovacao ou chamada humana quando houver, fallback, cota e auditoria.

#### Falta com aviso

- ID interno: `B2`.
- Nome canonico: `Falta com aviso`.
- Modo padrao: `Autonomo com excecoes`.
- Teto: `Autonomo com excecoes`.
- Objetivo: registrar falta avisada e encaminhar o proximo passo.

**Inicio**

O fluxo comeca quando o aluno avisa que nao vai comparecer a uma aula. Checagens deste fluxo: aluno foi identificado; aula existe na agenda; aviso chegou ate o prazo configurado; falta ainda nao foi registrada.

**Meio**

Trabalho do agente: registrar falta avisada e encaminhar o proximo passo. Segue sem equipe se: aluno foi identificado; aula existe na agenda; aviso chegou ate o prazo configurado; falta ainda nao foi registrada; mensagem usa template aprovado.

Chama a equipe se: aviso chega fora do prazo; nao encontra aluno ou aula; falta ja foi registrada; aluno pede excecao, credito, cancelamento ou reclama; WhatsApp, cota ou permissao bloqueiam o envio.

**Fim**

A falta avisada fica registrada na aula, a mensagem permitida e enviada e o caso abre a proxima tarefa de reposicao quando configurado. Se prazo, aluno, aula, credito ou envio nao fecharem, a equipe decide o proximo passo.

**Ajustes do studio**

- prazo para aviso.
- proximo passo apos falta.
- responsaveis por excecao.
- tom/template da mensagem.

**Requisitos readonly**

- agenda publicada.
- aluno e aula identificados.
- regras da rotina publicadas.
- canal conectado quando houver mensagem.
- permissao.
- cota.
- auditoria.

**Encadeamento**

/app/reposicoes; /app/aulas/[id]; tarefa

**Simulacao deve mostrar**

mostrar gatilho, dados usados, decisao do modo escolhido, mensagem/acao, aprovacao ou chamada humana quando houver, fallback, cota e auditoria.

#### Falta sem aviso

- ID interno: `B3`.
- Nome canonico: `Falta sem aviso`.
- Modo padrao: `Autonomo com excecoes`.
- Teto: `Autonomo com excecoes`.
- Objetivo: detectar falta sem aviso e abrir recuperacao ou tarefa.

**Inicio**

O fluxo comeca quando a aula termina e um aluno previsto nao apareceu nem avisou antes. Checagens deste fluxo: aula terminou; aluno estava previsto na chamada; presenca nao foi registrada; janela de tolerancia passou.

**Meio**

Trabalho do agente: detectar falta sem aviso e abrir recuperacao ou tarefa. Segue sem equipe se: aula terminou; aluno estava previsto na chamada; presenca nao foi registrada; janela de tolerancia passou; responsavel de acompanhamento esta definido.

Chama a equipe se: professor ainda nao fechou chamada; aluno avisou por outro canal; ha conflito de presenca; caso tem recorrencia ou risco de cancelamento; canal, cota ou permissao bloqueia contato.

**Fim**

A ausencia sem aviso fica marcada depois da janela de tolerancia e abre acompanhamento de recuperacao ou retencao. Se a chamada do professor, aviso paralelo ou historico do aluno nao baterem, a equipe revisa antes de contato.

**Ajustes do studio**

- quando vira tarefa de retencao.
- responsavel.

**Requisitos readonly**

- agenda publicada.
- aluno e aula identificados.
- regras da rotina publicadas.
- canal conectado quando houver mensagem.
- permissao.
- cota.
- auditoria.

**Encadeamento**

/app/aulas/[id]; /app/retencao; tarefa

**Simulacao deve mostrar**

mostrar gatilho, dados usados, decisao do modo escolhido, mensagem/acao, aprovacao ou chamada humana quando houver, fallback, cota e auditoria.


### Rotina: Vagas, reposicoes e lista de espera

#### Recuperar vaga aberta

- ID interno: `B4`.
- Nome canonico: `Recuperar vaga aberta`.
- Modo padrao: `Autonomo com excecoes`.
- Teto: `Autonomo com excecoes`.
- Objetivo: usar vaga aberta para convidar aluno elegivel.

**Inicio**

O fluxo comeca quando uma vaga abre em uma aula e pode ser oferecida a alguem elegivel. Checagens deste fluxo: vaga abriu em aula real; prioridade da lista esta definida; aluno elegivel tem credito ou direito; limite de convites nao foi atingido.

**Meio**

Trabalho do agente: usar vaga aberta para convidar aluno elegivel. Segue sem equipe se: vaga abriu em aula real; prioridade da lista esta definida; aluno elegivel tem credito ou direito; limite de convites nao foi atingido; convite usa mensagem aprovada.

Chama a equipe se: vaga fecha antes da resposta; ha empate ou lote grande; aluno nao tem credito claro; convite pode furar prioridade; canal, cota ou permissao bloqueia envio.

**Fim**

A vaga aberta gera convite para o aluno elegivel conforme prioridade e limite de convites. Se houver empate, lote grande, credito duvidoso ou risco de furar fila, a oferta fica parada para decisao.

**Ajustes do studio**

- prioridade da lista.
- limite de convites.
- aprovador se lote.

**Requisitos readonly**

- agenda publicada.
- aluno e aula identificados.
- regras da rotina publicadas.
- canal conectado quando houver mensagem.
- permissao.
- cota.
- auditoria.

**Encadeamento**

/app/lista-espera; /app/reposicoes; aprovacao/tarefa

**Simulacao deve mostrar**

mostrar gatilho, dados usados, decisao do modo escolhido, mensagem/acao, aprovacao ou chamada humana quando houver, fallback, cota e auditoria.

#### Reposicao/remarcacao

- ID interno: `B5`.
- Nome canonico: `Reposicao/remarcacao`.
- Modo padrao: `Autonomo com aprovacao`.
- Teto: `Autonomo com aprovacao`.
- Objetivo: preparar reposicao ou remarcacao para aprovacao.

**Inicio**

O fluxo comeca quando um aluno precisa repor ou remarcar uma aula dentro das regras do studio. Checagens deste fluxo: credito de reposicao existe; aula de destino tem capacidade; prazo da politica esta valido; impacto na agenda foi calculado.

**Meio**

Pedido de aprovacao: preparar reposicao ou remarcacao para aprovacao. O pedido mostra dados, impacto e proximo passo usando: credito de reposicao existe; aula de destino tem capacidade; prazo da politica esta valido; impacto na agenda foi calculado; aprovador esta definido.

Nao aplica sem aprovacao. Tambem cria pendencia para a equipe se: credito esta vencido ou contestado; aula destino esta lotada; mudanca afeta financeiro ou plano; ha conflito de horario; aprovacao vence ou permissao bloqueia.

**Fim**

A reposicao ou remarcacao vira pedido de aprovacao com credito, vaga, prazo e impacto na agenda. Se aprovado, a agenda muda; se recusado ou vencido, a solicitacao fica como tarefa em reposicoes.

**Ajustes do studio**

- aprovador.
- prazo maximo da reposicao.
- responsavel por excecao.

**Requisitos readonly**

- agenda publicada.
- aluno e aula identificados.
- regras da rotina publicadas.
- canal conectado quando houver mensagem.
- permissao.
- cota.
- auditoria.

**Encadeamento**

/app/reposicoes; /app/agenda; aprovacao

**Simulacao deve mostrar**

mostrar gatilho, dados usados, decisao do modo escolhido, mensagem/acao, aprovacao ou chamada humana quando houver, fallback, cota e auditoria.

#### Lista de espera

- ID interno: `B6`.
- Nome canonico: `Lista de espera`.
- Modo padrao: `Autonomo com excecoes`.
- Teto: `Autonomo com excecoes`.
- Objetivo: gerenciar lista de espera e convites.

**Inicio**

O fluxo comeca quando existe lista de espera e uma vaga compativel pode ser distribuida. Checagens deste fluxo: lista de espera existe; prioridade foi calculada; vaga compativel apareceu; limite de convites permite contato.

**Meio**

Trabalho do agente: gerenciar lista de espera e convites. Segue sem equipe se: lista de espera existe; prioridade foi calculada; vaga compativel apareceu; limite de convites permite contato; responsavel por excecao esta definido.

Chama a equipe se: prioridade empata; aluno nao responde no prazo; vaga deixa de existir; pedido envolve excecao de credito; canal, cota ou permissao bloqueia envio.

**Fim**

A lista de espera recebe convite para a vaga compativel e o status do aluno muda conforme resposta ou prazo. Se prioridade, vaga, credito ou envio nao fecharem, a equipe assume a distribuicao.

**Ajustes do studio**

- prioridade.
- limite de convites.
- responsavel por excecao.

**Requisitos readonly**

- agenda publicada.
- aluno e aula identificados.
- regras da rotina publicadas.
- canal conectado quando houver mensagem.
- permissao.
- cota.
- auditoria.

**Encadeamento**

/app/lista-espera; /app/tarefas

**Simulacao deve mostrar**

mostrar gatilho, dados usados, decisao do modo escolhido, mensagem/acao, aprovacao ou chamada humana quando houver, fallback, cota e auditoria.


### Rotina: Agenda experimental

#### Disponibilidade experimental

- ID interno: `B7`.
- Nome canonico: `Disponibilidade experimental`.
- Modo padrao: `Autonomo com excecoes`.
- Teto: `Autonomo com excecoes`.
- Objetivo: oferecer disponibilidade para aula experimental.

**Inicio**

O fluxo comeca quando um interessado precisa receber horarios possiveis para aula experimental. Checagens deste fluxo: interessado esta identificado; horarios oferecidos estao livres; responsavel comercial esta definido; limite de tentativas nao foi atingido.

**Meio**

Trabalho do agente: oferecer disponibilidade para aula experimental. Segue sem equipe se: interessado esta identificado; horarios oferecidos estao livres; responsavel comercial esta definido; limite de tentativas nao foi atingido; mensagem aprovada esta disponivel.

Chama a equipe se: interessado pede horario fora da regra; nao ha vaga compativel; lead ja tem experimental marcada; pedido envolve desconto ou excecao; canal, cota ou permissao bloqueia envio.

**Fim**

O interessado recebe horarios de experimental que existem de verdade e a resposta segue para agendamento comercial. Se nao houver vaga, houver experimental duplicada ou pedido especial, o comercial recebe tarefa.

**Ajustes do studio**

- responsavel comercial.
- horarios oferecidos.
- quando chamar humano.

**Requisitos readonly**

- agenda publicada.
- aluno e aula identificados.
- regras da rotina publicadas.
- canal conectado quando houver mensagem.
- permissao.
- cota.
- auditoria.

**Encadeamento**

/app/experimental; /app/agenda; tarefa

**Simulacao deve mostrar**

mostrar gatilho, dados usados, decisao do modo escolhido, mensagem/acao, aprovacao ou chamada humana quando houver, fallback, cota e auditoria.


### Rotina: Grade e capacidade

#### Mudanca horario fixo

- ID interno: `B8`.
- Nome canonico: `Mudanca horario fixo`.
- Modo padrao: `Autonomo com aprovacao`.
- Teto: `Autonomo com aprovacao`.
- Objetivo: preparar mudanca de horario fixo para aprovacao.

**Inicio**

O fluxo comeca quando um aluno pede ou precisa mudar seu horario fixo. Checagens deste fluxo: aluno e horario fixo foram identificados; novo horario existe; impacto em turma e capacidade foi calculado; mensagem de confirmacao esta pronta.

**Meio**

Pedido de aprovacao: preparar mudanca de horario fixo para aprovacao. O pedido mostra dados, impacto e proximo passo usando: aluno e horario fixo foram identificados; novo horario existe; impacto em turma e capacidade foi calculado; mensagem de confirmacao esta pronta; aprovador esta definido.

Nao aplica sem aprovacao. Tambem cria pendencia para a equipe se: novo horario gera conflito; aluno tem pendencia financeira ou credito afetado; mudanca impacta varios alunos; prazo minimo nao foi cumprido; aprovacao vence ou permissao bloqueia.

**Fim**

A mudanca de horario fixo vira aprovacao com novo horario, impacto em capacidade e mensagem de confirmacao. Se aprovada, o cadastro do aluno e a grade sao atualizados; se nao, fica tarefa para ajuste humano.

**Ajustes do studio**

- aprovador.
- prazo.
- mensagem de confirmacao.

**Requisitos readonly**

- agenda publicada.
- aluno e aula identificados.
- regras da rotina publicadas.
- canal conectado quando houver mensagem.
- permissao.
- cota.
- auditoria.

**Encadeamento**

/app/alunos/[id]; /app/agenda; aprovacao

**Simulacao deve mostrar**

mostrar gatilho, dados usados, decisao do modo escolhido, mensagem/acao, aprovacao ou chamada humana quando houver, fallback, cota e auditoria.

#### Cancelamento pelo studio

- ID interno: `B9`.
- Nome canonico: `Cancelamento pelo studio`.
- Modo padrao: `Autonomo com aprovacao`.
- Teto: `Autonomo com aprovacao`.
- Objetivo: preparar cancelamento pelo studio e comunicado.

**Inicio**

O fluxo comeca quando o studio precisa cancelar uma aula e comunicar os alunos afetados. Checagens deste fluxo: aula a cancelar existe; motivo foi informado; alunos afetados foram listados; reposicao ou credito foi calculado.

**Meio**

Pedido de aprovacao: preparar cancelamento pelo studio e comunicado. O pedido mostra dados, impacto e proximo passo usando: aula a cancelar existe; motivo foi informado; alunos afetados foram listados; reposicao ou credito foi calculado; aprovador esta definido.

Nao aplica sem aprovacao. Tambem cria pendencia para a equipe se: cancelamento afeta muitos alunos; ha aluno de primeira aula ou experimental; reposicao ou credito nao esta claro; comunicado nao cobre o caso; aprovacao vence ou permissao bloqueia.

**Fim**

O cancelamento pelo studio vira aprovacao com aula, motivo, alunos afetados e comunicado. Se aprovado, alunos recebem orientacao e reposicao/credito; se nao, a aula permanece sem alteracao automatica.

**Ajustes do studio**

- aprovador.
- template de comunicado.
- quem trata excecoes.

**Requisitos readonly**

- agenda publicada.
- aluno e aula identificados.
- regras da rotina publicadas.
- canal conectado quando houver mensagem.
- permissao.
- cota.
- auditoria.

**Encadeamento**

/app/aulas/[id]; /app/aprovacoes; /app/hoje

**Simulacao deve mostrar**

mostrar gatilho, dados usados, decisao do modo escolhido, mensagem/acao, aprovacao ou chamada humana quando houver, fallback, cota e auditoria.

#### Conflito capacidade

- ID interno: `B10`.
- Nome canonico: `Conflito capacidade`.
- Modo padrao: `Autonomo com aprovacao`.
- Teto: `Autonomo com aprovacao`.
- Objetivo: resolver conflito de capacidade com aprovacao.

**Inicio**

O fluxo comeca quando a agenda encontra conflito de capacidade, lotacao ou direito de vaga. Checagens deste fluxo: turma ou aula foi identificada; capacidade publicada existe; conflito foi calculado; prioridade do caso foi definida.

**Meio**

Pedido de aprovacao: resolver conflito de capacidade com aprovacao. O pedido mostra dados, impacto e proximo passo usando: turma ou aula foi identificada; capacidade publicada existe; conflito foi calculado; prioridade do caso foi definida; aprovador esta definido.

Nao aplica sem aprovacao. Tambem cria pendencia para a equipe se: capacidade real diverge da configurada; ha conflito entre alunos com direito similar; mudanca afeta grade ou professor; solucao exige remover aluno; aprovacao vence ou permissao bloqueia.

**Fim**

O conflito de capacidade vira aprovacao com quem foi afetado, prioridade e alternativa proposta. Se aprovado, a correcao ajusta vaga/turma; se nao, o conflito fica aberto para coordenacao.

**Ajustes do studio**

- aprovador.
- responsavel do caso.
- prioridade.

**Requisitos readonly**

- agenda publicada.
- aluno e aula identificados.
- regras da rotina publicadas.
- canal conectado quando houver mensagem.
- permissao.
- cota.
- auditoria.

**Encadeamento**

/app/turmas/[id]; /app/agenda; caso operacional

**Simulacao deve mostrar**

mostrar gatilho, dados usados, decisao do modo escolhido, mensagem/acao, aprovacao ou chamada humana quando houver, fallback, cota e auditoria.

#### Ajuste de grade

- ID interno: `B11`.
- Nome canonico: `Ajuste de grade`.
- Modo padrao: `Autonomo com aprovacao`.
- Teto: `Autonomo com aprovacao`.
- Objetivo: preparar ajuste de grade e simulacao de impacto.

**Inicio**

O fluxo comeca quando o studio quer alterar grade, horarios, professores ou vigencia da agenda. Checagens deste fluxo: mudanca de grade foi descrita; data de vigencia esta definida; impacto em aulas, alunos e professores foi simulado; comunicacao necessaria foi listada.

**Meio**

Pedido de aprovacao: preparar ajuste de grade e simulacao de impacto. O pedido mostra dados, impacto e proximo passo usando: mudanca de grade foi descrita; data de vigencia esta definida; impacto em aulas, alunos e professores foi simulado; comunicacao necessaria foi listada; aprovador esta definido.

Nao aplica sem aprovacao. Tambem cria pendencia para a equipe se: simulacao encontra conflito; impacto financeiro ou contratual aparece; data de vigencia e curta demais; alunos afetados nao foram resolvidos; aprovacao vence ou permissao bloqueia.

**Fim**

O ajuste de grade vira simulacao aprovada com vigencia, aulas, alunos, professores e comunicacao. Se aprovado, a grade muda na data definida; se houver conflito, a simulacao volta para revisao.

**Ajustes do studio**

- aprovador.
- data de vigencia.
- escopo da mudanca.

**Requisitos readonly**

- agenda publicada.
- aluno e aula identificados.
- regras da rotina publicadas.
- canal conectado quando houver mensagem.
- permissao.
- cota.
- auditoria.

**Encadeamento**

/app/grade; /app/aprovacoes; /app/operacao

**Simulacao deve mostrar**

mostrar gatilho, dados usados, decisao do modo escolhido, mensagem/acao, aprovacao ou chamada humana quando houver, fallback, cota e auditoria.


### Rotina: Agenda experimental

#### Experimental sem comparecimento

- ID interno: `B12`.
- Nome canonico: `Experimental sem comparecimento`.
- Modo padrao: `Autonomo com excecoes`.
- Teto: `Autonomo com excecoes`.
- Objetivo: tratar experimental sem comparecimento.

**Inicio**

O fluxo comeca quando um lead marcado para aula experimental nao comparece. Checagens deste fluxo: experimental estava marcada; lead nao compareceu; janela de tolerancia passou; cadencia comercial esta definida.

**Meio**

Trabalho do agente: tratar experimental sem comparecimento. Segue sem equipe se: experimental estava marcada; lead nao compareceu; janela de tolerancia passou; cadencia comercial esta definida; limite de contato nao foi atingido.

Chama a equipe se: lead avisou por outro canal; lead pede remarcacao fora da regra; nao ha nova vaga compativel; lead demonstra objecao sensivel; canal, cota ou permissao bloqueia contato.

**Fim**

O nao comparecimento ao experimental abre follow-up comercial ou remarcacao dentro da cadencia. Se o lead avisou por outro canal, pediu excecao ou nao ha vaga, o comercial decide a abordagem.

**Ajustes do studio**

- cadencia.
- responsavel comercial.
- limite de contato.

**Requisitos readonly**

- agenda publicada.
- aluno e aula identificados.
- regras da rotina publicadas.
- canal conectado quando houver mensagem.
- permissao.
- cota.
- auditoria.

**Encadeamento**

/app/experimental; /app/interessados/[id]; tarefa comercial

**Simulacao deve mostrar**

mostrar gatilho, dados usados, decisao do modo escolhido, mensagem/acao, aprovacao ou chamada humana quando houver, fallback, cota e auditoria.


### Rotina: Vagas, reposicoes e lista de espera

#### Creditos reposicao

- ID interno: `B13`.
- Nome canonico: `Creditos reposicao`.
- Modo padrao: `Autonomo com aprovacao`.
- Teto: `Autonomo com aprovacao`.
- Objetivo: preparar credito de reposicao para aprovacao.

**Inicio**

O fluxo comeca quando uma falta, remarcacao ou decisao operacional pode gerar credito de reposicao. Checagens deste fluxo: falta ou remarcacao geradora foi identificada; validade proposta esta definida; politica de credito esta publicada; destino de excecoes esta definido.

**Meio**

Pedido de aprovacao: preparar credito de reposicao para aprovacao. O pedido mostra dados, impacto e proximo passo usando: falta ou remarcacao geradora foi identificada; validade proposta esta definida; politica de credito esta publicada; destino de excecoes esta definido; aprovador esta definido.

Nao aplica sem aprovacao. Tambem cria pendencia para a equipe se: credito e contestado; validade foge da politica; credito afeta plano ou financeiro; ha duplicidade de credito; aprovacao vence ou permissao bloqueia.

**Fim**

O credito de reposicao vira aprovacao com origem, validade e politica aplicada. Se aprovado, o credito aparece para uso em reposicao; se contestado ou duplicado, fica com o responsavel.

**Ajustes do studio**

- aprovador.
- validade do credito.
- responsavel por excecao.

**Requisitos readonly**

- agenda publicada.
- aluno e aula identificados.
- regras da rotina publicadas.
- canal conectado quando houver mensagem.
- permissao.
- cota.
- auditoria.

**Encadeamento**

/app/creditos-reposicao; /app/aprovacoes

**Simulacao deve mostrar**

mostrar gatilho, dados usados, decisao do modo escolhido, mensagem/acao, aprovacao ou chamada humana quando houver, fallback, cota e auditoria.


### Rotina: Presenca e faltas

#### Correcao presenca

- ID interno: `B14`.
- Nome canonico: `Correcao presenca`.
- Modo padrao: `Autonomo com aprovacao`.
- Teto: `Autonomo com aprovacao`.
- Objetivo: preparar correcao de presenca para aprovacao.

**Inicio**

O fluxo comeca quando alguem pede para corrigir uma presenca ja registrada. Checagens deste fluxo: aula e aluno foram identificados; correcao solicitada tem motivo; historico atual foi preservado; impacto da alteracao foi mostrado.

**Meio**

Pedido de aprovacao: preparar correcao de presenca para aprovacao. O pedido mostra dados, impacto e proximo passo usando: aula e aluno foram identificados; correcao solicitada tem motivo; historico atual foi preservado; impacto da alteracao foi mostrado; aprovador esta definido.

Nao aplica sem aprovacao. Tambem cria pendencia para a equipe se: motivo nao foi informado; correcao altera historico sensivel; ha conflito com professor ou aluno; impacto em credito ou financeiro aparece; aprovacao vence ou permissao bloqueia.

**Fim**

A correcao de presenca vira aprovacao com aula, aluno, motivo e impacto. Se aprovada, a chamada e atualizada preservando historico anterior; se houver impacto em credito/financeiro, fica pendente.

**Ajustes do studio**

- aprovador.
- motivo obrigatorio.
- prazo de aprovacao.

**Requisitos readonly**

- agenda publicada.
- aluno e aula identificados.
- regras da rotina publicadas.
- canal conectado quando houver mensagem.
- permissao.
- cota.
- auditoria.

**Encadeamento**

/app/aulas/[id]/chamada; /app/auditoria; aprovacao

**Simulacao deve mostrar**

mostrar gatilho, dados usados, decisao do modo escolhido, mensagem/acao, aprovacao ou chamada humana quando houver, fallback, cota e auditoria.


### Rotina: Primeira aula e aulas especiais

#### Primeira aula

- ID interno: `B15`.
- Nome canonico: `Primeira aula`.
- Modo padrao: `Autonomo com excecoes`.
- Teto: `Autonomo com excecoes`.
- Objetivo: acompanhar primeira aula e checklist inicial.

**Inicio**

O fluxo comeca quando um aluno esta perto da primeira aula e precisa de acompanhamento inicial. Checagens deste fluxo: aluno tem primeira aula identificada; checklist esta definido; professor ou responsavel esta atribuido; orientacoes foram preparadas.

**Meio**

Trabalho do agente: acompanhar primeira aula e checklist inicial. Segue sem equipe se: aluno tem primeira aula identificada; checklist esta definido; professor ou responsavel esta atribuido; orientacoes foram preparadas; nao ha restricao sensivel pendente.

Chama a equipe se: aluno tem cuidado sem revisao; professor nao esta definido; aula muda de horario; aluno pede remarcacao ou excecao; canal, cota ou permissao bloqueia contato.

**Fim**

A primeira aula recebe checklist, orientacao e responsavel definidos. Se houver cuidado, restricao, troca de aula ou professor indefinido, a equipe recebe tarefa antes do contato.

**Ajustes do studio**

- checklist.
- responsavel.
- quando chamar humano.

**Requisitos readonly**

- agenda publicada.
- aluno e aula identificados.
- regras da rotina publicadas.
- canal conectado quando houver mensagem.
- permissao.
- cota.
- auditoria.

**Encadeamento**

/app/aulas/[id]; /app/alunos/[id]; checklist/tarefa

**Simulacao deve mostrar**

mostrar gatilho, dados usados, decisao do modo escolhido, mensagem/acao, aprovacao ou chamada humana quando houver, fallback, cota e auditoria.

#### Aula especial/workshop

- ID interno: `B16`.
- Nome canonico: `Aula especial/workshop`.
- Modo padrao: `Autonomo com aprovacao`.
- Teto: `Autonomo com aprovacao`.
- Objetivo: preparar aula especial ou workshop para aprovacao.

**Inicio**

O fluxo comeca quando o studio cria ou altera uma aula especial, workshop ou evento. Checagens deste fluxo: evento foi descrito; capacidade esta definida; prazo e data estao claros; template de comunicacao esta pronto.

**Meio**

Pedido de aprovacao: preparar aula especial ou workshop para aprovacao. O pedido mostra dados, impacto e proximo passo usando: evento foi descrito; capacidade esta definida; prazo e data estao claros; template de comunicacao esta pronto; aprovador esta definido.

Nao aplica sem aprovacao. Tambem cria pendencia para a equipe se: capacidade e regra de inscricao conflitam; evento afeta grade regular; preco ou beneficio nao esta definido; comunicacao impacta muitos alunos; aprovacao vence ou permissao bloqueia.

**Fim**

A aula especial ou workshop vira aprovacao com data, capacidade, regra de inscricao e comunicacao. Se aprovado, o evento entra na agenda; se conflitar com grade, preco ou beneficio, fica em revisao.

**Ajustes do studio**

- aprovador.
- capacidade.
- template.
- prazo.

**Requisitos readonly**

- agenda publicada.
- aluno e aula identificados.
- regras da rotina publicadas.
- canal conectado quando houver mensagem.
- permissao.
- cota.
- auditoria.

**Encadeamento**

/app/eventos; /app/aprovacoes; tarefa

**Simulacao deve mostrar**

mostrar gatilho, dados usados, decisao do modo escolhido, mensagem/acao, aprovacao ou chamada humana quando houver, fallback, cota e auditoria.


## Agente: Vendas


### Rotina: Conversao e matricula

#### Valores e planos

- ID interno: `C1`.
- Nome canonico: `Valores e planos`.
- Modo padrao: `Autonomo com excecoes`.
- Teto: `Autonomo com excecoes`.
- Objetivo: responder sobre valores e planos aprovados.

**Inicio**

O fluxo comeca quando lead ou aluno pergunta sobre valores, planos ou condicoes comerciais aprovadas. Checagens deste fluxo: plano ou valor esta na base aprovada; lead ou aluno foi identificado quando necessario; nao ha pedido de desconto especial; resposta usa template permitido.

**Meio**

Trabalho do agente: responder sobre valores e planos aprovados. Segue sem equipe se: plano ou valor esta na base aprovada; lead ou aluno foi identificado quando necessario; nao ha pedido de desconto especial; resposta usa template permitido; limite de conversa nao foi atingido.

Chama a equipe se: lead pede desconto, promessa ou excecao; plano nao esta claro; pergunta mistura financeiro e contrato; resposta pode gerar compromisso comercial; canal, cota ou permissao bloqueia resposta.

**Fim**

O lead recebe valores e planos somente da base aprovada e a conversa fica pronta para proxima etapa comercial. Se pedir desconto, promessa ou condicao fora da base, o comercial assume.

**Ajustes do studio**

- tom/template de resposta.
- quando chamar humano.

**Requisitos readonly**

- lead/interessado identificado.
- origem registrada.
- planos e horarios disponiveis quando usados.
- canal conectado.
- opt-out.
- permissao.
- cota.
- auditoria.

**Encadeamento**

/app/inbox; /app/vendas; tarefa comercial

**Simulacao deve mostrar**

mostrar gatilho, dados usados, decisao do modo escolhido, mensagem/acao, aprovacao ou chamada humana quando houver, fallback, cota e auditoria.


### Rotina: Experimental e acompanhamento

#### Aula experimental

- ID interno: `C2`.
- Nome canonico: `Aula experimental`.
- Modo padrao: `Autonomo com excecoes`.
- Teto: `Autonomo com excecoes`.
- Objetivo: marcar ou preparar aula experimental.

**Inicio**

O fluxo comeca quando um lead quer marcar uma aula experimental. Checagens deste fluxo: lead esta identificado; horarios disponiveis existem; responsavel comercial esta definido; limite de tentativas permite contato.

**Meio**

Trabalho do agente: marcar ou preparar aula experimental. Segue sem equipe se: lead esta identificado; horarios disponiveis existem; responsavel comercial esta definido; limite de tentativas permite contato; lead nao tem experimental duplicada.

Chama a equipe se: lead pede horario indisponivel; nao ha vaga compativel; lead ja fez experimental recente; pedido envolve desconto ou excecao; canal, cota ou permissao bloqueia contato.

**Fim**

A aula experimental e marcada ou preparada com horario real, responsavel e dados do lead. Se horario, vaga, duplicidade ou excecao comercial nao fecharem, vira tarefa para o comercial.

**Ajustes do studio**

- horarios oferecidos.
- responsavel.
- limite de tentativas.

**Requisitos readonly**

- lead/interessado identificado.
- origem registrada.
- planos e horarios disponiveis quando usados.
- canal conectado.
- opt-out.
- permissao.
- cota.
- auditoria.

**Encadeamento**

/app/experimental; /app/agenda; tarefa

**Simulacao deve mostrar**

mostrar gatilho, dados usados, decisao do modo escolhido, mensagem/acao, aprovacao ou chamada humana quando houver, fallback, cota e auditoria.

#### Lembrete experimental

- ID interno: `C3`.
- Nome canonico: `Lembrete experimental`.
- Modo padrao: `Autonomo`.
- Teto: `Autonomo`.
- Objetivo: enviar lembrete de aula experimental.

**Inicio**

O fluxo comeca quando chega o horario de lembrar um lead sobre a aula experimental marcada. Checagens deste fluxo: experimental esta marcada; horario do lembrete chegou; lead tem canal permitido; template aprovado esta disponivel.

**Meio**

Trabalho do agente: enviar lembrete de aula experimental. Conclui sem fila humana se: experimental esta marcada; horario do lembrete chegou; lead tem canal permitido; template aprovado esta disponivel; lembrete ainda nao foi enviado.

Para e cria pendencia para a equipe se: aula foi remarcada ou cancelada; lead pediu opt-out; canal falhou; lead responde com objecao ou pedido de mudanca; cota ou permissao bloqueia envio.

**Fim**

O lembrete do experimental e enviado uma vez no horario configurado e o status do lead mostra que foi lembrado. Se a aula mudou, o lead pediu opt-out ou respondeu com mudanca, o fluxo para.

**Ajustes do studio**

- horario do lembrete.
- template.
- limite por aula.

**Requisitos readonly**

- lead/interessado identificado.
- origem registrada.
- planos e horarios disponiveis quando usados.
- canal conectado.
- opt-out.
- permissao.
- cota.
- auditoria.

**Encadeamento**

/app/experimental; execucao; tarefa manual

**Simulacao deve mostrar**

mostrar gatilho, dados usados, decisao do modo escolhido, mensagem/acao, aprovacao ou chamada humana quando houver, fallback, cota e auditoria.

#### Pos-aula experimental

- ID interno: `C4`.
- Nome canonico: `Pos-aula experimental`.
- Modo padrao: `Autonomo com excecoes`.
- Teto: `Autonomo com excecoes`.
- Objetivo: acompanhar lead depois da aula experimental.

**Inicio**

O fluxo comeca depois que uma aula experimental acontece e o lead precisa de acompanhamento comercial. Checagens deste fluxo: experimental foi concluida; presenca foi registrada; cadencia pos-aula esta definida; responsavel comercial esta atribuido.

**Meio**

Trabalho do agente: acompanhar lead depois da aula experimental. Segue sem equipe se: experimental foi concluida; presenca foi registrada; cadencia pos-aula esta definida; responsavel comercial esta atribuido; limite de contato nao foi atingido.

Chama a equipe se: lead nao compareceu; professor registrou observacao sensivel; lead pede desconto ou condicao especial; lead demonstra reclamacao; canal, cota ou permissao bloqueia contato.

**Fim**

Depois da experimental, o lead entra no acompanhamento comercial correto com presenca e proxima acao. Se houve falta, observacao sensivel, desconto ou reclamacao, o comercial decide.

**Ajustes do studio**

- cadencia.
- responsavel.
- quando virar tarefa.

**Requisitos readonly**

- lead/interessado identificado.
- origem registrada.
- planos e horarios disponiveis quando usados.
- canal conectado.
- opt-out.
- permissao.
- cota.
- auditoria.

**Encadeamento**

/app/interessados/[id]; /app/vendas; tarefa

**Simulacao deve mostrar**

mostrar gatilho, dados usados, decisao do modo escolhido, mensagem/acao, aprovacao ou chamada humana quando houver, fallback, cota e auditoria.

#### Follow-up comercial

- ID interno: `C5`.
- Nome canonico: `Follow-up comercial`.
- Modo padrao: `Autonomo com excecoes`.
- Teto: `Autonomo com excecoes`.
- Objetivo: conduzir follow-up comercial dentro da cadencia.

**Inicio**

O fluxo comeca quando um lead entra em uma etapa de follow-up comercial permitida pela cadencia. Checagens deste fluxo: lead esta em etapa elegivel; cadencia esta definida; ultima interacao permite novo contato; responsavel comercial esta definido.

**Meio**

Trabalho do agente: conduzir follow-up comercial dentro da cadencia. Segue sem equipe se: lead esta em etapa elegivel; cadencia esta definida; ultima interacao permite novo contato; responsavel comercial esta definido; limite de tentativas nao foi atingido.

Chama a equipe se: lead pediu humano ou parar contato; lead tem objecao sensivel; lead pede desconto ou garantia; conversa esfriou alem do limite; canal, cota ou permissao bloqueia contato.

**Fim**

O follow-up e enviado dentro da cadencia e a etapa comercial avanca conforme resposta ou ausencia de resposta. Se o lead pediu humano, desconto, garantia ou parar contato, o fluxo para.

**Ajustes do studio**

- cadencia.
- limite de tentativas.
- responsavel.

**Requisitos readonly**

- lead/interessado identificado.
- origem registrada.
- planos e horarios disponiveis quando usados.
- canal conectado.
- opt-out.
- permissao.
- cota.
- auditoria.

**Encadeamento**

/app/vendas; /app/tarefas; /app/inbox

**Simulacao deve mostrar**

mostrar gatilho, dados usados, decisao do modo escolhido, mensagem/acao, aprovacao ou chamada humana quando houver, fallback, cota e auditoria.


### Rotina: Conversao e matricula

#### Pre-matricula

- ID interno: `C6`.
- Nome canonico: `Pre-matricula`.
- Modo padrao: `Autonomo com aprovacao`.
- Teto: `Autonomo com aprovacao`.
- Objetivo: preparar pre-matricula para aprovacao.

**Inicio**

O fluxo comeca quando o lead aceita avancar para pre-matricula. Checagens deste fluxo: lead aceitou avancar; checklist de matricula esta completo; plano escolhido esta definido; responsavel comercial esta atribuido.

**Meio**

Pedido de aprovacao: preparar pre-matricula para aprovacao. O pedido mostra dados, impacto e proximo passo usando: lead aceitou avancar; checklist de matricula esta completo; plano escolhido esta definido; responsavel comercial esta atribuido; aprovador esta definido.

Nao aplica sem aprovacao. Tambem cria pendencia para a equipe se: dados obrigatorios faltam; plano ou valor diverge da proposta; ha desconto ou excecao; documento ou contrato nao esta pronto; aprovacao vence ou permissao bloqueia.

**Fim**

A pre-matricula vira aprovacao com plano, checklist, dados e responsavel. Se aprovada, segue para matricula/contrato; se faltarem dados, valor ou documento, fica pendente.

**Ajustes do studio**

- aprovador.
- checklist.
- responsavel comercial.

**Requisitos readonly**

- lead/interessado identificado.
- origem registrada.
- planos e horarios disponiveis quando usados.
- canal conectado.
- opt-out.
- permissao.
- cota.
- auditoria.

**Encadeamento**

/app/matriculas; /app/aprovacoes

**Simulacao deve mostrar**

mostrar gatilho, dados usados, decisao do modo escolhido, mensagem/acao, aprovacao ou chamada humana quando houver, fallback, cota e auditoria.

#### Objecoes

- ID interno: `C7`.
- Nome canonico: `Objecoes`.
- Modo padrao: `Autonomo com aprovacao`.
- Teto: `Autonomo com aprovacao`.
- Objetivo: preparar resposta para objecoes comerciais.

**Inicio**

O fluxo comeca quando o lead traz uma objecao comercial que precisa de resposta cuidadosa. Checagens deste fluxo: objecao foi classificada; base de respostas cobre o caso; limite de promessa esta definido; impacto comercial foi mostrado.

**Meio**

Pedido de aprovacao: preparar resposta para objecoes comerciais. O pedido mostra dados, impacto e proximo passo usando: objecao foi classificada; base de respostas cobre o caso; limite de promessa esta definido; impacto comercial foi mostrado; aprovador esta definido.

Nao aplica sem aprovacao. Tambem cria pendencia para a equipe se: objecao envolve preco, desconto ou garantia; lead compara concorrente com promessa sensivel; resposta nao existe na base; risco de promessa indevida aparece; aprovacao vence ou permissao bloqueia.

**Fim**

A objecao comercial vira resposta revisada com limite de promessa e impacto. Se aprovada, a resposta vai para o lead; se envolver desconto, garantia ou promessa indevida, fica com humano.

**Ajustes do studio**

- aprovador.
- base de respostas.
- limite de promessa.

**Requisitos readonly**

- lead/interessado identificado.
- origem registrada.
- planos e horarios disponiveis quando usados.
- canal conectado.
- opt-out.
- permissao.
- cota.
- auditoria.

**Encadeamento**

/app/conversas/[id]; /app/aprovacoes

**Simulacao deve mostrar**

mostrar gatilho, dados usados, decisao do modo escolhido, mensagem/acao, aprovacao ou chamada humana quando houver, fallback, cota e auditoria.


### Rotina: Captura e qualificacao

#### Origem/qualificacao

- ID interno: `C8`.
- Nome canonico: `Origem/qualificacao`.
- Modo padrao: `Autonomo com excecoes`.
- Teto: `Autonomo com excecoes`.
- Objetivo: qualificar origem e perfil do lead.

**Inicio**

O fluxo comeca quando um lead precisa ser qualificado por origem, perfil e dados minimos. Checagens deste fluxo: lead foi identificado; campos obrigatorios foram preenchidos; origem foi reconhecida; duplicidade foi verificada.

**Meio**

Trabalho do agente: qualificar origem e perfil do lead. Segue sem equipe se: lead foi identificado; campos obrigatorios foram preenchidos; origem foi reconhecida; duplicidade foi verificada; responsavel esta definido.

Chama a equipe se: lead duplicado; origem nao reconhecida; campos obrigatorios faltam; lead ja esta em outra etapa; canal, cota ou permissao bloqueia atualizacao.

**Fim**

O lead recebe origem, perfil, dono e campos minimos preenchidos. Se houver duplicidade, origem desconhecida ou etapa conflitante, a ficha fica pendente para limpeza.

**Ajustes do studio**

- campos obrigatorios.
- responsavel.
- regra de duplicidade.

**Requisitos readonly**

- lead/interessado identificado.
- origem registrada.
- planos e horarios disponiveis quando usados.
- canal conectado.
- opt-out.
- permissao.
- cota.
- auditoria.

**Encadeamento**

/app/interessados/[id]; /app/vendas/origens; tarefa

**Simulacao deve mostrar**

mostrar gatilho, dados usados, decisao do modo escolhido, mensagem/acao, aprovacao ou chamada humana quando houver, fallback, cota e auditoria.

#### Perda comercial

- ID interno: `C9`.
- Nome canonico: `Perda comercial`.
- Modo padrao: `Autonomo com aprovacao`.
- Teto: `Autonomo com aprovacao`.
- Objetivo: preparar perda comercial e motivo.

**Inicio**

O fluxo comeca quando um lead deve ser marcado como perdido ou sem continuidade comercial. Checagens deste fluxo: lead esta em etapa que permite perda; motivo foi informado; responsavel comercial esta definido; impacto em relatorio foi calculado.

**Meio**

Pedido de aprovacao: preparar perda comercial e motivo. O pedido mostra dados, impacto e proximo passo usando: lead esta em etapa que permite perda; motivo foi informado; responsavel comercial esta definido; impacto em relatorio foi calculado; aprovador existe quando perda for sensivel.

Nao aplica sem aprovacao. Tambem cria pendencia para a equipe se: perda envolve reclamacao; lead ainda tem acao aberta; motivo e sensivel ou ambiguo; perda afetaria indicacao ou campanha; aprovacao vence ou permissao bloqueia.

**Fim**

A perda comercial vira aprovacao com motivo e impacto nos relatorios. Se aprovada, o lead sai da cadencia; se ainda houver acao aberta ou motivo sensivel, o comercial revisa.

**Ajustes do studio**

- motivo.
- aprovador se perda sensivel.
- responsavel.

**Requisitos readonly**

- lead/interessado identificado.
- origem registrada.
- planos e horarios disponiveis quando usados.
- canal conectado.
- opt-out.
- permissao.
- cota.
- auditoria.

**Encadeamento**

/app/vendas; /app/interessados/[id]; aprovacao/tarefa

**Simulacao deve mostrar**

mostrar gatilho, dados usados, decisao do modo escolhido, mensagem/acao, aprovacao ou chamada humana quando houver, fallback, cota e auditoria.

#### Indicacao

- ID interno: `C10`.
- Nome canonico: `Indicacao`.
- Modo padrao: `Autonomo com aprovacao`.
- Teto: `Autonomo com aprovacao`.
- Objetivo: preparar indicacao e beneficio para aprovacao.

**Inicio**

O fluxo comeca quando uma indicacao ou beneficio de indicacao precisa ser analisado. Checagens deste fluxo: indicador e indicado foram identificados; regra de vinculo esta clara; beneficio permitido foi calculado; duplicidade foi verificada.

**Meio**

Pedido de aprovacao: preparar indicacao e beneficio para aprovacao. O pedido mostra dados, impacto e proximo passo usando: indicador e indicado foram identificados; regra de vinculo esta clara; beneficio permitido foi calculado; duplicidade foi verificada; aprovador esta definido.

Nao aplica sem aprovacao. Tambem cria pendencia para a equipe se: vinculo nao confere; beneficio foge da regra; indicado ja existe; indicacao envolve conflito comercial; aprovacao vence ou permissao bloqueia.

**Fim**

A indicacao vira aprovacao com indicador, indicado, regra de vinculo e beneficio calculado. Se aprovada, o beneficio entra no processo correto; se houver duplicidade ou conflito, fica pendente.

**Ajustes do studio**

- aprovador de beneficio.
- regra de vinculo.

**Requisitos readonly**

- lead/interessado identificado.
- origem registrada.
- planos e horarios disponiveis quando usados.
- canal conectado.
- opt-out.
- permissao.
- cota.
- auditoria.

**Encadeamento**

/app/indicacoes; /app/aprovacoes

**Simulacao deve mostrar**

mostrar gatilho, dados usados, decisao do modo escolhido, mensagem/acao, aprovacao ou chamada humana quando houver, fallback, cota e auditoria.


### Rotina: Conversao e matricula

#### Checkout/abandono

- ID interno: `C11`.
- Nome canonico: `Checkout/abandono`.
- Modo padrao: `Autonomo com excecoes`.
- Teto: `Autonomo com excecoes`.
- Objetivo: recuperar checkout ou abandono de matricula.

**Inicio**

O fluxo comeca quando um checkout, proposta ou matricula fica abandonado antes de concluir. Checagens deste fluxo: checkout abandonado foi identificado; cadencia permite contato; responsavel comercial esta definido; mensagem aprovada esta disponivel.

**Meio**

Trabalho do agente: recuperar checkout ou abandono de matricula. Segue sem equipe se: checkout abandonado foi identificado; cadencia permite contato; responsavel comercial esta definido; mensagem aprovada esta disponivel; lead nao pediu parar contato.

Chama a equipe se: pagamento falhou com motivo financeiro; lead pede desconto ou condicao especial; checkout esta expirado; lead responde com reclamacao; canal, cota ou permissao bloqueia contato.

**Fim**

O abandono de checkout recebe recuperacao dentro da cadencia e o lead continua no funil. Se houve falha financeira, desconto, reclamacao ou checkout expirado, o comercial assume.

**Ajustes do studio**

- cadencia.
- responsavel.
- limite de contato.

**Requisitos readonly**

- lead/interessado identificado.
- origem registrada.
- planos e horarios disponiveis quando usados.
- canal conectado.
- opt-out.
- permissao.
- cota.
- auditoria.

**Encadeamento**

/app/checkout-alunos; /app/vendas; tarefa

**Simulacao deve mostrar**

mostrar gatilho, dados usados, decisao do modo escolhido, mensagem/acao, aprovacao ou chamada humana quando houver, fallback, cota e auditoria.


### Rotina: Experimental e acompanhamento

#### Demanda sem vaga

- ID interno: `C12`.
- Nome canonico: `Demanda sem vaga`.
- Modo padrao: `Autonomo com excecoes`.
- Teto: `Autonomo com excecoes`.
- Objetivo: tratar demanda sem vaga e lista de interesse.

**Inicio**

O fluxo comeca quando um lead quer uma turma, horario ou vaga que o studio nao tem disponivel agora. Checagens deste fluxo: lead quer horario ou turma sem vaga; lista de espera foi definida; responsavel esta atribuido; regra de promessa esta clara.

**Meio**

Trabalho do agente: tratar demanda sem vaga e lista de interesse. Segue sem equipe se: lead quer horario ou turma sem vaga; lista de espera foi definida; responsavel esta atribuido; regra de promessa esta clara; mensagem nao promete vaga garantida.

Chama a equipe se: lead exige prazo ou garantia; nao ha alternativa compativel; lead e prioridade comercial especial; promessa poderia ser indevida; canal, cota ou permissao bloqueia contato.

**Fim**

A demanda sem vaga entra em lista de interesse sem promessa de vaga garantida. Se o lead exigir prazo, garantia ou tratamento especial, o comercial decide a resposta.

**Ajustes do studio**

- proximo passo sem vaga.
- responsavel.
- promessa permitida.

**Requisitos readonly**

- lead/interessado identificado.
- origem registrada.
- planos e horarios disponiveis quando usados.
- canal conectado.
- opt-out.
- permissao.
- cota.
- auditoria.

**Encadeamento**

/app/vendas; /app/lista-espera; tarefa

**Simulacao deve mostrar**

mostrar gatilho, dados usados, decisao do modo escolhido, mensagem/acao, aprovacao ou chamada humana quando houver, fallback, cota e auditoria.


### Rotina: Conversao e matricula

#### Interessado para aluno

- ID interno: `C13`.
- Nome canonico: `Interessado para aluno`.
- Modo padrao: `Autonomo com aprovacao`.
- Teto: `Autonomo com aprovacao`.
- Objetivo: preparar conversao de interessado em aluno.

**Inicio**

O fluxo comeca quando um interessado esta pronto para virar aluno no CRM. Checagens deste fluxo: interessado esta qualificado; plano escolhido foi definido; checklist de matricula esta completo; cadastro de aluno pode ser criado.

**Meio**

Pedido de aprovacao: preparar conversao de interessado em aluno. O pedido mostra dados, impacto e proximo passo usando: interessado esta qualificado; plano escolhido foi definido; checklist de matricula esta completo; cadastro de aluno pode ser criado; aprovador esta definido.

Nao aplica sem aprovacao. Tambem cria pendencia para a equipe se: dados obrigatorios faltam; plano ou valor nao confere; existe duplicidade de aluno; contrato ou pagamento falta; aprovacao vence ou permissao bloqueia.

**Fim**

A conversao de interessado em aluno vira aprovacao com plano, cadastro e checklist. Se aprovada, o aluno e criado no CRM; se contrato, pagamento, duplicidade ou dado faltar, fica pendente.

**Ajustes do studio**

- aprovador.
- checklist de matricula.
- responsavel comercial.

**Requisitos readonly**

- lead/interessado identificado.
- origem registrada.
- planos e horarios disponiveis quando usados.
- canal conectado.
- opt-out.
- permissao.
- cota.
- auditoria.

**Encadeamento**

/app/matriculas; /app/alunos/[id]; aprovacao

**Simulacao deve mostrar**

mostrar gatilho, dados usados, decisao do modo escolhido, mensagem/acao, aprovacao ou chamada humana quando houver, fallback, cota e auditoria.

#### Upsell/upgrade

- ID interno: `C14`.
- Nome canonico: `Upsell/upgrade`.
- Modo padrao: `Autonomo com aprovacao`.
- Teto: `Autonomo com aprovacao`.
- Objetivo: preparar proposta de upsell ou upgrade.

**Inicio**

O fluxo comeca quando um aluno pode receber proposta de upgrade, upsell ou mudanca de plano. Checagens deste fluxo: aluno elegivel foi identificado; plano destino esta definido; proposta usa template aprovado; responsavel comercial esta atribuido.

**Meio**

Pedido de aprovacao: preparar proposta de upsell ou upgrade. O pedido mostra dados, impacto e proximo passo usando: aluno elegivel foi identificado; plano destino esta definido; proposta usa template aprovado; responsavel comercial esta atribuido; aprovador esta definido.

Nao aplica sem aprovacao. Tambem cria pendencia para a equipe se: mudanca impacta financeiro atual; ha desconto ou cortesia; aluno tem pendencia ou reclamacao; proposta foge da regra; aprovacao vence ou permissao bloqueia.

**Fim**

O upsell ou upgrade vira proposta aprovada com plano destino e impacto financeiro. Se aprovada, a proposta e enviada ou aplicada conforme regra; se houver desconto, pendencia ou reclamacao, fica com humano.

**Ajustes do studio**

- aprovador.
- template de proposta.
- responsavel.

**Requisitos readonly**

- lead/interessado identificado.
- origem registrada.
- planos e horarios disponiveis quando usados.
- canal conectado.
- opt-out.
- permissao.
- cota.
- auditoria.

**Encadeamento**

/app/alunos/[id]; /app/aprovacoes; /app/vendas

**Simulacao deve mostrar**

mostrar gatilho, dados usados, decisao do modo escolhido, mensagem/acao, aprovacao ou chamada humana quando houver, fallback, cota e auditoria.


### Rotina: Captura e qualificacao

#### Entrada multicanal de lead

- ID interno: `C15`.
- Nome canonico: `Entrada multicanal de lead`.
- Modo padrao: `Autonomo com excecoes`.
- Teto: `Autonomo com excecoes`.
- Objetivo: capturar lead de multiplos canais e criar ficha unica.

**Inicio**

O fluxo comeca quando um lead entra por canal, formulario, importacao ou origem externa. Checagens deste fluxo: fonte e aceita; lead tem contato identificavel; duplicidade foi verificada; dono do lead esta definido.

**Meio**

Trabalho do agente: capturar lead de multiplos canais e criar ficha unica. Segue sem equipe se: fonte e aceita; lead tem contato identificavel; duplicidade foi verificada; dono do lead esta definido; campos minimos foram preenchidos.

Chama a equipe se: lead duplicado; fonte nao reconhecida; contato incompleto; lead ja pertence a outro responsavel; canal, cota ou permissao bloqueia criacao.

**Fim**

O lead de canal externo entra como ficha unica com origem, dono e campos minimos. Se duplicar, vier incompleto ou pertencer a outro responsavel, vai para revisao.

**Ajustes do studio**

- fontes aceitas.
- dono do lead.
- regra de duplicidade.

**Requisitos readonly**

- lead/interessado identificado.
- origem registrada.
- planos e horarios disponiveis quando usados.
- canal conectado.
- opt-out.
- permissao.
- cota.
- auditoria.

**Encadeamento**

/app/vendas/captura; /app/interessados; tarefa

**Simulacao deve mostrar**

mostrar gatilho, dados usados, decisao do modo escolhido, mensagem/acao, aprovacao ou chamada humana quando houver, fallback, cota e auditoria.


## Agente: Financeiro


### Rotina: Lembretes e pagamentos

#### Lembrete vencimento

- ID interno: `D1`.
- Nome canonico: `Lembrete vencimento`.
- Modo padrao: `Autonomo`.
- Teto: `Autonomo`.
- Objetivo: enviar lembrete de vencimento.

**Inicio**

O fluxo comeca quando uma cobranca esta perto do vencimento. Checagens deste fluxo: cobranca existe; vencimento esta proximo conforme horario configurado; aluno tem canal permitido; template aprovado esta disponivel.

**Meio**

Trabalho do agente: enviar lembrete de vencimento. Conclui sem fila humana se: cobranca existe; vencimento esta proximo conforme horario configurado; aluno tem canal permitido; template aprovado esta disponivel; limite por cobranca nao foi atingido.

Para e cria pendencia para a equipe se: cobranca foi paga ou cancelada; aluno pediu opt-out; valor ou vencimento diverge; mensagem falha; canal, cota ou permissao bloqueia envio.

**Fim**

O lembrete de vencimento e enviado antes do prazo e a cobranca mostra tentativa registrada. Se a cobranca foi paga, cancelada, diverge ou o aluno pediu opt-out, nao envia.

**Ajustes do studio**

- horario.
- template.
- limite por cobranca.

**Requisitos readonly**

- movimentacao financeira identificada.
- provedor financeiro ok quando usado.
- plano/contrato do aluno atualizado.
- permissao financeira.
- cota.
- auditoria.

**Encadeamento**

/app/financeiro/movimentacoes; execucao; tarefa

**Simulacao deve mostrar**

mostrar gatilho, dados usados, decisao do modo escolhido, mensagem/acao, aprovacao ou chamada humana quando houver, fallback, cota e auditoria.

#### Pagamento atrasado

- ID interno: `D2`.
- Nome canonico: `Pagamento atrasado`.
- Modo padrao: `Autonomo com excecoes`.
- Teto: `Autonomo com excecoes`.
- Objetivo: tratar pagamento atrasado e abrir cobranca ou tarefa.

**Inicio**

O fluxo comeca quando uma cobranca passa do vencimento e precisa de acao financeira. Checagens deste fluxo: movimentacao esta vencida; tentativas permitem novo contato; fila financeira esta definida; mensagem aprovada esta disponivel.

**Meio**

Trabalho do agente: tratar pagamento atrasado e abrir cobranca ou tarefa. Segue sem equipe se: movimentacao esta vencida; tentativas permitem novo contato; fila financeira esta definida; mensagem aprovada esta disponivel; nao ha disputa registrada.

Chama a equipe se: aluno contesta valor; pedido envolve acordo, desconto ou prazo especial; pagamento pode ter sido feito; provedor apresenta falha; canal, cota ou permissao bloqueia contato.

**Fim**

O atraso abre cobranca ou tarefa financeira conforme tentativas permitidas. Se o aluno contestar, pedir acordo/desconto ou o provedor falhar, a equipe financeira assume.

**Ajustes do studio**

- tentativas.
- fila financeira.
- sinais que chamam humano.

**Requisitos readonly**

- movimentacao financeira identificada.
- provedor financeiro ok quando usado.
- plano/contrato do aluno atualizado.
- permissao financeira.
- cota.
- auditoria.

**Encadeamento**

/app/financeiro/movimentacoes/[id]; tarefa financeira

**Simulacao deve mostrar**

mostrar gatilho, dados usados, decisao do modo escolhido, mensagem/acao, aprovacao ou chamada humana quando houver, fallback, cota e auditoria.

#### Pix/link

- ID interno: `D3`.
- Nome canonico: `Pix/link`.
- Modo padrao: `Autonomo com aprovacao`.
- Teto: `Autonomo com aprovacao`.
- Objetivo: preparar Pix ou link de pagamento para aprovacao.

**Inicio**

O fluxo comeca quando a equipe precisa enviar Pix, link ou instrucao de pagamento. Checagens deste fluxo: movimentacao esta identificada; valor esta dentro do limite; template esta aprovado; provedor financeiro esta ok.

**Meio**

Pedido de aprovacao: preparar Pix ou link de pagamento para aprovacao. O pedido mostra dados, impacto e proximo passo usando: movimentacao esta identificada; valor esta dentro do limite; template esta aprovado; provedor financeiro esta ok; aprovador esta definido.

Nao aplica sem aprovacao. Tambem cria pendencia para a equipe se: valor excede limite; movimentacao esta divergente; aluno pede condicao especial; provedor retorna erro; aprovacao vence ou permissao bloqueia.

**Fim**

O Pix ou link vira aprovacao com valor, cobranca, provedor e mensagem. Se aprovado, a instrucao e enviada; se valor/provedor/condicao divergirem, fica pendente.

**Ajustes do studio**

- aprovador.
- template.
- limite de valor.

**Requisitos readonly**

- movimentacao financeira identificada.
- provedor financeiro ok quando usado.
- plano/contrato do aluno atualizado.
- permissao financeira.
- cota.
- auditoria.

**Encadeamento**

/app/financeiro/movimentacoes; /app/aprovacoes

**Simulacao deve mostrar**

mostrar gatilho, dados usados, decisao do modo escolhido, mensagem/acao, aprovacao ou chamada humana quando houver, fallback, cota e auditoria.


### Rotina: Excecoes e documentos financeiros

#### Confirmacao pagamento

- ID interno: `D4`.
- Nome canonico: `Confirmacao pagamento`.
- Modo padrao: `Autonomo com aprovacao`.
- Teto: `Autonomo com aprovacao`.
- Objetivo: preparar confirmacao de pagamento para aprovacao.

**Inicio**

O fluxo comeca quando um aluno informa pagamento e a confirmacao precisa ser conferida. Checagens deste fluxo: movimentacao foi localizada; evidencia de pagamento foi anexada; valor e aluno conferem; responsavel financeiro esta definido.

**Meio**

Pedido de aprovacao: preparar confirmacao de pagamento para aprovacao. O pedido mostra dados, impacto e proximo passo usando: movimentacao foi localizada; evidencia de pagamento foi anexada; valor e aluno conferem; responsavel financeiro esta definido; aprovador esta definido.

Nao aplica sem aprovacao. Tambem cria pendencia para a equipe se: evidencia esta incompleta; valor nao confere; pagamento duplicado ou suspeito; provedor ainda nao conciliou; aprovacao vence ou permissao bloqueia.

**Fim**

A confirmacao de pagamento vira aprovacao com evidencia, aluno, valor e movimentacao. Se aprovada, a cobranca e baixada; se evidencia, valor ou conciliacao nao baterem, fica com financeiro.

**Ajustes do studio**

- aprovador.
- evidencia exigida.
- responsavel.

**Requisitos readonly**

- movimentacao financeira identificada.
- provedor financeiro ok quando usado.
- plano/contrato do aluno atualizado.
- permissao financeira.
- cota.
- auditoria.

**Encadeamento**

/app/financeiro/movimentacoes/[id]; aprovacao

**Simulacao deve mostrar**

mostrar gatilho, dados usados, decisao do modo escolhido, mensagem/acao, aprovacao ou chamada humana quando houver, fallback, cota e auditoria.


### Rotina: Ciclo do plano do aluno

#### Renovacao plano

- ID interno: `D5`.
- Nome canonico: `Renovacao plano`.
- Modo padrao: `Autonomo com aprovacao`.
- Teto: `Autonomo com aprovacao`.
- Objetivo: preparar renovacao de plano.

**Inicio**

O fluxo comeca quando um plano esta perto de renovar ou precisa iniciar novo ciclo. Checagens deste fluxo: plano atual e aluno foram identificados; antecedencia configurada chegou; novo ciclo foi calculado; template de renovacao esta aprovado.

**Meio**

Pedido de aprovacao: preparar renovacao de plano. O pedido mostra dados, impacto e proximo passo usando: plano atual e aluno foram identificados; antecedencia configurada chegou; novo ciclo foi calculado; template de renovacao esta aprovado; aprovador esta definido.

Nao aplica sem aprovacao. Tambem cria pendencia para a equipe se: aluno tem pendencia financeira; plano mudou de preco ou regra; aluno pediu pausa ou cancelamento; contrato precisa atualizacao; aprovacao vence ou permissao bloqueia.

**Fim**

A renovacao vira aprovacao com novo ciclo, plano e comunicacao. Se aprovada, o plano renova; se houver pendencia, pausa, cancelamento ou contrato novo, fica pendente.

**Ajustes do studio**

- aprovador.
- antecedencia.
- template.

**Requisitos readonly**

- movimentacao financeira identificada.
- provedor financeiro ok quando usado.
- plano/contrato do aluno atualizado.
- permissao financeira.
- cota.
- auditoria.

**Encadeamento**

/app/alunos/[id]; /app/financeiro; aprovacao

**Simulacao deve mostrar**

mostrar gatilho, dados usados, decisao do modo escolhido, mensagem/acao, aprovacao ou chamada humana quando houver, fallback, cota e auditoria.


### Rotina: Excecoes e documentos financeiros

#### Excecoes financeiras

- ID interno: `D6`.
- Nome canonico: `Excecoes financeiras`.
- Modo padrao: `Autonomo com aprovacao`.
- Teto: `Autonomo com aprovacao`.
- Objetivo: preparar excecao financeira para aprovacao.

**Inicio**

O fluxo comeca quando aparece pedido financeiro fora da regra comum. Checagens deste fluxo: tipo de excecao foi classificado; motivo foi informado; impacto financeiro foi calculado; prazo do caso esta definido.

**Meio**

Pedido de aprovacao: preparar excecao financeira para aprovacao. O pedido mostra dados, impacto e proximo passo usando: tipo de excecao foi classificado; motivo foi informado; impacto financeiro foi calculado; prazo do caso esta definido; aprovador obrigatorio esta definido.

Nao aplica sem aprovacao. Tambem cria pendencia para a equipe se: motivo esta incompleto; excecao ultrapassa limite; caso envolve contrato, bloqueio ou reclamacao; impacto em aluno ou turma nao esta claro; aprovacao vence ou permissao bloqueia.

**Fim**

A excecao financeira vira aprovacao com tipo, motivo, impacto e prazo. Se aprovada, a excecao e aplicada; se ultrapassar limite ou envolver contrato/reclamacao, fica com responsavel.

**Ajustes do studio**

- aprovador obrigatorio.
- tipos de excecao.
- prazo.

**Requisitos readonly**

- movimentacao financeira identificada.
- provedor financeiro ok quando usado.
- plano/contrato do aluno atualizado.
- permissao financeira.
- cota.
- auditoria.

**Encadeamento**

/app/financeiro/movimentacoes; /app/aprovacoes; caso

**Simulacao deve mostrar**

mostrar gatilho, dados usados, decisao do modo escolhido, mensagem/acao, aprovacao ou chamada humana quando houver, fallback, cota e auditoria.


### Rotina: Lembretes e pagamentos

#### Falha pagamento

- ID interno: `D7`.
- Nome canonico: `Falha pagamento`.
- Modo padrao: `Autonomo com excecoes`.
- Teto: `Autonomo com excecoes`.
- Objetivo: tratar falha de pagamento.

**Inicio**

O fluxo comeca quando o provedor ou o CRM identifica falha de pagamento. Checagens deste fluxo: falha veio do provedor; tentativas permitem novo contato; fila financeira esta definida; mensagem aprovada esta disponivel.

**Meio**

Trabalho do agente: tratar falha de pagamento. Segue sem equipe se: falha veio do provedor; tentativas permitem novo contato; fila financeira esta definida; mensagem aprovada esta disponivel; nao ha disputa aberta.

Chama a equipe se: falha persiste apos tentativas; aluno contesta cobranca; provedor retorna erro tecnico; caso exige bloqueio ou liberacao; canal, cota ou permissao bloqueia contato.

**Fim**

A falha de pagamento gera contato ou tarefa conforme tentativas permitidas. Se a falha persistir, virar disputa ou depender do provedor, o financeiro assume.

**Ajustes do studio**

- fila financeira.
- tentativas.
- quando abrir caso.

**Requisitos readonly**

- movimentacao financeira identificada.
- provedor financeiro ok quando usado.
- plano/contrato do aluno atualizado.
- permissao financeira.
- cota.
- auditoria.

**Encadeamento**

/app/financeiro/movimentacoes/[id]; tarefa/caso

**Simulacao deve mostrar**

mostrar gatilho, dados usados, decisao do modo escolhido, mensagem/acao, aprovacao ou chamada humana quando houver, fallback, cota e auditoria.

#### Recibo/nota

- ID interno: `D8`.
- Nome canonico: `Recibo/nota`.
- Modo padrao: `Autonomo com excecoes`.
- Teto: `Autonomo com excecoes`.
- Objetivo: emitir ou preparar recibo/nota permitida.

**Inicio**

O fluxo comeca quando o aluno precisa de recibo, nota ou documento financeiro permitido. Checagens deste fluxo: pagamento foi confirmado; tipo de documento e permitido; dados do aluno conferem; responsavel esta definido.

**Meio**

Trabalho do agente: emitir ou preparar recibo/nota permitida. Segue sem equipe se: pagamento foi confirmado; tipo de documento e permitido; dados do aluno conferem; responsavel esta definido; fallback para tarefa existe.

Chama a equipe se: documento nao e permitido; dados fiscais faltam; pagamento nao esta conciliado; aluno pede documento especial; permissao ou provedor bloqueia emissao.

**Fim**

O recibo ou nota permitida e emitido/preparado e vinculado ao aluno. Se dados fiscais, permissao ou provedor nao fecharem, fica tarefa financeira.

**Ajustes do studio**

- responsavel.
- tipo de documento.
- quando abrir tarefa.

**Requisitos readonly**

- movimentacao financeira identificada.
- provedor financeiro ok quando usado.
- plano/contrato do aluno atualizado.
- permissao financeira.
- cota.
- auditoria.

**Encadeamento**

/app/financeiro/documentos; tarefa

**Simulacao deve mostrar**

mostrar gatilho, dados usados, decisao do modo escolhido, mensagem/acao, aprovacao ou chamada humana quando houver, fallback, cota e auditoria.


### Rotina: Ciclo do plano do aluno

#### Pausa/trancamento

- ID interno: `D9`.
- Nome canonico: `Pausa/trancamento`.
- Modo padrao: `Autonomo com aprovacao`.
- Teto: `Autonomo com aprovacao`.
- Objetivo: preparar pausa ou trancamento para aprovacao.

**Inicio**

O fluxo comeca quando o aluno pede pausa, trancamento ou interrupcao temporaria. Checagens deste fluxo: aluno e plano foram identificados; motivo foi informado; impacto em agenda e cobranca foi calculado; prazo esta definido.

**Meio**

Pedido de aprovacao: preparar pausa ou trancamento para aprovacao. O pedido mostra dados, impacto e proximo passo usando: aluno e plano foram identificados; motivo foi informado; impacto em agenda e cobranca foi calculado; prazo esta definido; aprovador esta definido.

Nao aplica sem aprovacao. Tambem cria pendencia para a equipe se: pedido afeta credito, contrato ou vencimento; aluno tem pendencia; motivo e sensivel; data solicitada conflita com regra; aprovacao vence ou permissao bloqueia.

**Fim**

A pausa ou trancamento vira aprovacao com periodo, motivo, impacto no plano e retorno previsto. Se aprovada, o plano muda; se impactar financeiro ou contrato, fica pendente.

**Ajustes do studio**

- aprovador.
- data de inicio/fim.
- prazo de aprovacao.

**Requisitos readonly**

- movimentacao financeira identificada.
- provedor financeiro ok quando usado.
- plano/contrato do aluno atualizado.
- permissao financeira.
- cota.
- auditoria.

**Encadeamento**

/app/financeiro; /app/alunos/[id]; aprovacao/caso

**Simulacao deve mostrar**

mostrar gatilho, dados usados, decisao do modo escolhido, mensagem/acao, aprovacao ou chamada humana quando houver, fallback, cota e auditoria.


### Rotina: Lembretes e pagamentos

#### Conciliacao interna

- ID interno: `D10`.
- Nome canonico: `Conciliacao interna`.
- Modo padrao: `Autonomo com aprovacao`.
- Teto: `Autonomo com aprovacao`.
- Objetivo: preparar conciliacao interna para aprovacao.

**Inicio**

O fluxo comeca quando um pagamento precisa ser conciliado com uma movimentacao interna. Checagens deste fluxo: movimentacao e pagamento candidato foram encontrados; confianca minima foi atingida; responsavel financeiro esta definido; impacto foi mostrado.

**Meio**

Pedido de aprovacao: preparar conciliacao interna para aprovacao. O pedido mostra dados, impacto e proximo passo usando: movimentacao e pagamento candidato foram encontrados; confianca minima foi atingida; responsavel financeiro esta definido; impacto foi mostrado; aprovador esta definido.

Nao aplica sem aprovacao. Tambem cria pendencia para a equipe se: confianca esta baixa; ha mais de um candidato; valor ou data divergem; provedor esta instavel; aprovacao vence ou permissao bloqueia.

**Fim**

A conciliacao interna vira aprovacao com candidato, confianca, valor, data e impacto. Se aprovada, movimentacao e pagamento ficam vinculados; se houver divergencia, fica com financeiro.

**Ajustes do studio**

- aprovador.
- confianca minima.
- responsavel.

**Requisitos readonly**

- movimentacao financeira identificada.
- provedor financeiro ok quando usado.
- plano/contrato do aluno atualizado.
- permissao financeira.
- cota.
- auditoria.

**Encadeamento**

/app/financeiro/movimentacoes; tarefa financeira

**Simulacao deve mostrar**

mostrar gatilho, dados usados, decisao do modo escolhido, mensagem/acao, aprovacao ou chamada humana quando houver, fallback, cota e auditoria.


### Rotina: Excecoes e documentos financeiros

#### Contrato/termos

- ID interno: `D11`.
- Nome canonico: `Contrato/termos`.
- Modo padrao: `Autonomo com aprovacao`.
- Teto: `Autonomo com aprovacao`.
- Objetivo: preparar contrato ou termos para aprovacao.

**Inicio**

O fluxo comeca quando contrato, termo ou documento precisa ser preparado para aluno ou plano. Checagens deste fluxo: template de contrato esta definido; dados do aluno e plano conferem; prazo de envio esta definido; responsavel esta atribuido.

**Meio**

Pedido de aprovacao: preparar contrato ou termos para aprovacao. O pedido mostra dados, impacto e proximo passo usando: template de contrato esta definido; dados do aluno e plano conferem; prazo de envio esta definido; responsavel esta atribuido; aprovador esta definido.

Nao aplica sem aprovacao. Tambem cria pendencia para a equipe se: template nao cobre o caso; dados obrigatorios faltam; plano ou valor diverge; aluno pede clausula especial; aprovacao vence ou permissao bloqueia.

**Fim**

Contrato ou termo vira aprovacao com aluno, plano, versao e dados usados. Se aprovado, o documento segue para envio/assinatura; se faltar dado ou versao, fica pendente.

**Ajustes do studio**

- aprovador.
- template.
- prazo.

**Requisitos readonly**

- movimentacao financeira identificada.
- provedor financeiro ok quando usado.
- plano/contrato do aluno atualizado.
- permissao financeira.
- cota.
- auditoria.

**Encadeamento**

/app/contratos; /app/aprovacoes

**Simulacao deve mostrar**

mostrar gatilho, dados usados, decisao do modo escolhido, mensagem/acao, aprovacao ou chamada humana quando houver, fallback, cota e auditoria.

#### Bloqueio/liberacao

- ID interno: `D12`.
- Nome canonico: `Bloqueio/liberacao`.
- Modo padrao: `Autonomo com aprovacao`.
- Teto: `Autonomo com aprovacao`.
- Objetivo: preparar bloqueio ou liberacao para aprovacao.

**Inicio**

O fluxo comeca quando o studio precisa bloquear ou liberar acesso por motivo financeiro. Checagens deste fluxo: aluno e motivo foram identificados; impacto financeiro foi calculado; motivo obrigatorio foi preenchido; prazo de aprovacao esta definido.

**Meio**

Pedido de aprovacao: preparar bloqueio ou liberacao para aprovacao. O pedido mostra dados, impacto e proximo passo usando: aluno e motivo foram identificados; impacto financeiro foi calculado; motivo obrigatorio foi preenchido; prazo de aprovacao esta definido; aprovador esta definido.

Nao aplica sem aprovacao. Tambem cria pendencia para a equipe se: motivo esta incompleto; bloqueio afeta aula ja marcada; liberacao contraria regra financeira; ha reclamacao ou disputa; aprovacao vence ou permissao bloqueia.

**Fim**

Bloqueio ou liberacao vira aprovacao com motivo, aluno, impacto e comunicacao. Se aprovado, o acesso muda; se houver contestacao, pagamento recente ou excecao, fica com humano.

**Ajustes do studio**

- aprovador.
- motivo obrigatorio.
- prazo de aprovacao.

**Requisitos readonly**

- movimentacao financeira identificada.
- provedor financeiro ok quando usado.
- plano/contrato do aluno atualizado.
- permissao financeira.
- cota.
- auditoria.

**Encadeamento**

/app/financeiro; /app/aprovacoes; auditoria

**Simulacao deve mostrar**

mostrar gatilho, dados usados, decisao do modo escolhido, mensagem/acao, aprovacao ou chamada humana quando houver, fallback, cota e auditoria.

#### Creditos/cortesias

- ID interno: `D13`.
- Nome canonico: `Creditos/cortesias`.
- Modo padrao: `Autonomo com aprovacao`.
- Teto: `Autonomo com aprovacao`.
- Objetivo: preparar credito ou cortesia para aprovacao.

**Inicio**

O fluxo comeca quando alguem pede credito, cortesia ou ajuste financeiro excepcional. Checagens deste fluxo: aluno foi identificado; motivo foi informado; limite de valor esta dentro da politica; impacto financeiro foi calculado.

**Meio**

Pedido de aprovacao: preparar credito ou cortesia para aprovacao. O pedido mostra dados, impacto e proximo passo usando: aluno foi identificado; motivo foi informado; limite de valor esta dentro da politica; impacto financeiro foi calculado; aprovador esta definido.

Nao aplica sem aprovacao. Tambem cria pendencia para a equipe se: valor excede limite; motivo e insuficiente; ha credito duplicado; cortesia afeta contrato ou plano; aprovacao vence ou permissao bloqueia.

**Fim**

Credito ou cortesia vira aprovacao com motivo, valor, validade e impacto. Se aprovado, o beneficio aparece no financeiro; se fugir da politica, fica com responsavel.

**Ajustes do studio**

- aprovador.
- limite de valor.
- motivo.

**Requisitos readonly**

- movimentacao financeira identificada.
- provedor financeiro ok quando usado.
- plano/contrato do aluno atualizado.
- permissao financeira.
- cota.
- auditoria.

**Encadeamento**

/app/financeiro; /app/aprovacoes

**Simulacao deve mostrar**

mostrar gatilho, dados usados, decisao do modo escolhido, mensagem/acao, aprovacao ou chamada humana quando houver, fallback, cota e auditoria.

#### Fechamento mensal

- ID interno: `D14`.
- Nome canonico: `Fechamento mensal`.
- Modo padrao: `Autonomo com excecoes`.
- Teto: `Autonomo com excecoes`.
- Objetivo: preparar fechamento mensal financeiro.

**Inicio**

O fluxo comeca quando chega o periodo de fechamento financeiro do mes. Checagens deste fluxo: periodo de fechamento esta definido; movimentacoes foram consolidadas; pendencias foram separadas; responsavel financeiro esta definido.

**Meio**

Trabalho do agente: preparar fechamento mensal financeiro. Segue sem equipe se: periodo de fechamento esta definido; movimentacoes foram consolidadas; pendencias foram separadas; responsavel financeiro esta definido; frequencia do resumo esta configurada.

Chama a equipe se: ha divergencia de conciliacao; movimentacao sem dono; provedor financeiro falhou; pendencia critica apareceu; permissao ou cota bloqueia analise.

**Fim**

O fechamento mensal separa consolidados, pendencias e alertas financeiros para o responsavel. Se conciliacao, provedor ou dado falhar, o fechamento fica incompleto e gera tarefa.

**Ajustes do studio**

- responsavel.
- frequencia.
- quando abrir tarefa.

**Requisitos readonly**

- movimentacao financeira identificada.
- provedor financeiro ok quando usado.
- plano/contrato do aluno atualizado.
- permissao financeira.
- cota.
- auditoria.

**Encadeamento**

/app/relatorios/financeiro; tarefa financeira

**Simulacao deve mostrar**

mostrar gatilho, dados usados, decisao do modo escolhido, mensagem/acao, aprovacao ou chamada humana quando houver, fallback, cota e auditoria.


### Rotina: Ciclo do plano do aluno

#### Encerramento ou alteracao efetiva de plano

- ID interno: `D15`.
- Nome canonico: `Encerramento ou alteracao efetiva de plano`.
- Modo padrao: `Autonomo com aprovacao`.
- Teto: `Autonomo com aprovacao`.
- Objetivo: preparar encerramento ou alteracao efetiva de plano.

**Inicio**

O fluxo comeca quando plano de aluno precisa ser encerrado ou alterado de forma efetiva. Checagens deste fluxo: plano atual foi identificado; mudanca solicitada foi descrita; impacto em agenda, cobranca e contrato foi calculado; checklist esta completo.

**Meio**

Pedido de aprovacao: preparar encerramento ou alteracao efetiva de plano. O pedido mostra dados, impacto e proximo passo usando: plano atual foi identificado; mudanca solicitada foi descrita; impacto em agenda, cobranca e contrato foi calculado; checklist esta completo; aprovador esta definido.

Nao aplica sem aprovacao. Tambem cria pendencia para a equipe se: impacto financeiro nao esta claro; aluno tem aulas ou creditos pendentes; contrato precisa revisao; pedido envolve cancelamento sensivel; aprovacao vence ou permissao bloqueia.

**Fim**

Encerramento ou alteracao de plano vira aprovacao com data efetiva, impacto financeiro e comunicacao. Se aprovado, o plano muda; se houver contrato, saldo ou pendencia, fica travado.

**Ajustes do studio**

- aprovador.
- checklist.
- template de comunicacao.

**Requisitos readonly**

- movimentacao financeira identificada.
- provedor financeiro ok quando usado.
- plano/contrato do aluno atualizado.
- permissao financeira.
- cota.
- auditoria.

**Encadeamento**

/app/financeiro; /app/alunos/[id]; aprovacao/caso

**Simulacao deve mostrar**

mostrar gatilho, dados usados, decisao do modo escolhido, mensagem/acao, aprovacao ou chamada humana quando houver, fallback, cota e auditoria.


## Agente: Retencao


### Rotina: Retencao preventiva

#### Queda frequencia

- ID interno: `E1`.
- Nome canonico: `Queda frequencia`.
- Modo padrao: `Autonomo com excecoes`.
- Teto: `Autonomo com excecoes`.
- Objetivo: detectar queda de frequencia e iniciar prevencao.

**Inicio**

O fluxo comeca quando a frequencia de um aluno cai abaixo do padrao esperado. Checagens deste fluxo: frequencia caiu conforme regra publicada; aluno esta ativo; responsavel esta definido; cadencia permite contato.

**Meio**

Trabalho do agente: detectar queda de frequencia e iniciar prevencao. Segue sem equipe se: frequencia caiu conforme regra publicada; aluno esta ativo; responsavel esta definido; cadencia permite contato; nao ha caso sensivel aberto.

Chama a equipe se: queda tem motivo ja registrado; aluno tem reclamacao ou saude/evento pessoal; risco de cancelamento aumentou; cadencia foi excedida; canal, cota ou permissao bloqueia contato.

**Fim**

A queda de frequencia abre contato preventivo ou tarefa de cuidado conforme regra. Se houver recorrencia, reclamacao, saude ou canal bloqueado, a equipe assume.

**Ajustes do studio**

- regra de queda.
- responsavel.
- cadencia.

**Requisitos readonly**

- aluno ou ex-aluno identificado.
- sinais de risco atualizados.
- historico disponivel conforme permissao.
- canal conectado.
- opt-out.
- cota.
- auditoria.

**Encadeamento**

/app/retencao/riscos; /app/alunos/[id]; tarefa

**Simulacao deve mostrar**

mostrar gatilho, dados usados, decisao do modo escolhido, mensagem/acao, aprovacao ou chamada humana quando houver, fallback, cota e auditoria.

#### Aluno inativo

- ID interno: `E2`.
- Nome canonico: `Aluno inativo`.
- Modo padrao: `Autonomo com excecoes`.
- Teto: `Autonomo com excecoes`.
- Objetivo: identificar aluno inativo e preparar retomada.

**Inicio**

O fluxo comeca quando um aluno ativo fica inativo por tempo relevante. Checagens deste fluxo: dias de inatividade atingiram o limite; aluno esta elegivel para contato; responsavel esta definido; limite de contato nao foi atingido.

**Meio**

Trabalho do agente: identificar aluno inativo e preparar retomada. Segue sem equipe se: dias de inatividade atingiram o limite; aluno esta elegivel para contato; responsavel esta definido; limite de contato nao foi atingido; mensagem aprovada esta disponivel.

Chama a equipe se: aluno pausou ou trancou; aluno pediu opt-out; ha pendencia financeira ou reclamacao; historico indica caso sensivel; canal, cota ou permissao bloqueia contato.

**Fim**

O aluno inativo entra em retomada permitida com responsavel e limite de contato. Se pausou, pediu opt-out, tem pendencia ou caso sensivel, o fluxo para.

**Ajustes do studio**

- dias de inatividade.
- responsavel.
- limite de contato.

**Requisitos readonly**

- aluno ou ex-aluno identificado.
- sinais de risco atualizados.
- historico disponivel conforme permissao.
- canal conectado.
- opt-out.
- cota.
- auditoria.

**Encadeamento**

/app/retencao/riscos; tarefa/aprovacao

**Simulacao deve mostrar**

mostrar gatilho, dados usados, decisao do modo escolhido, mensagem/acao, aprovacao ou chamada humana quando houver, fallback, cota e auditoria.

#### Retorno

- ID interno: `E3`.
- Nome canonico: `Retorno`.
- Modo padrao: `Autonomo com excecoes`.
- Teto: `Autonomo com excecoes`.
- Objetivo: organizar retorno de aluno.

**Inicio**

O fluxo comeca quando um aluno demonstra interesse em voltar. Checagens deste fluxo: aluno demonstrou interesse em voltar; regra de agenda permite encaixe; responsavel esta definido; opcoes de horario existem.

**Meio**

Trabalho do agente: organizar retorno de aluno. Segue sem equipe se: aluno demonstrou interesse em voltar; regra de agenda permite encaixe; responsavel esta definido; opcoes de horario existem; mensagem aprovada esta disponivel.

Chama a equipe se: nao ha horario compativel; aluno tem pendencia financeira; retorno exige avaliacao ou cuidado; aluno pede condicao especial; canal, cota ou permissao bloqueia contato.

**Fim**

O retorno do aluno organiza opcoes de agenda e proximo contato. Se nao houver horario, houver pendencia financeira ou cuidado especial, a equipe decide.

**Ajustes do studio**

- responsavel.
- tipo de retorno.
- quando chamar Agenda.

**Requisitos readonly**

- aluno ou ex-aluno identificado.
- sinais de risco atualizados.
- historico disponivel conforme permissao.
- canal conectado.
- opt-out.
- cota.
- auditoria.

**Encadeamento**

/app/retencao; /app/agenda; tarefa

**Simulacao deve mostrar**

mostrar gatilho, dados usados, decisao do modo escolhido, mensagem/acao, aprovacao ou chamada humana quando houver, fallback, cota e auditoria.


### Rotina: Casos sensiveis

#### Risco cancelamento

- ID interno: `E4`.
- Nome canonico: `Risco cancelamento`.
- Modo padrao: `Autonomo com aprovacao`.
- Teto: `Autonomo com aprovacao`.
- Objetivo: preparar caso de risco de cancelamento para aprovacao.

**Inicio**

O fluxo comeca quando aparecem sinais de risco de cancelamento. Checagens deste fluxo: sinal de cancelamento foi detectado; dono do caso esta definido; automacoes conflitantes foram pausadas; contexto foi resumido.

**Meio**

Pedido de aprovacao: preparar caso de risco de cancelamento para aprovacao. O pedido mostra dados, impacto e proximo passo usando: sinal de cancelamento foi detectado; dono do caso esta definido; automacoes conflitantes foram pausadas; contexto foi resumido; aprovador esta definido.

Nao aplica sem aprovacao. Tambem cria pendencia para a equipe se: aluno ja pediu cancelamento formal; caso envolve reclamacao ou saude; proposta de retencao exige beneficio; historico e sensivel; aprovacao vence ou permissao bloqueia.

**Fim**

O risco de cancelamento vira aprovacao com contexto, dono e automacoes conflitantes pausadas. Se aprovado, a acao de retencao segue; se for cancelamento formal ou caso sensivel, fica com responsavel.

**Ajustes do studio**

- dono do caso.
- aprovador.
- pausa de automacoes.

**Requisitos readonly**

- aluno ou ex-aluno identificado.
- sinais de risco atualizados.
- historico disponivel conforme permissao.
- canal conectado.
- opt-out.
- cota.
- auditoria.

**Encadeamento**

/app/cancelamentos; /app/operacao; aprovacao/caso

**Simulacao deve mostrar**

mostrar gatilho, dados usados, decisao do modo escolhido, mensagem/acao, aprovacao ou chamada humana quando houver, fallback, cota e auditoria.

#### Reativacao ex-aluno

- ID interno: `E5`.
- Nome canonico: `Reativacao ex-aluno`.
- Modo padrao: `Autonomo com aprovacao`.
- Teto: `Autonomo com aprovacao`.
- Objetivo: preparar reativacao de ex-aluno para aprovacao.

**Inicio**

O fluxo comeca quando um ex-aluno entra em segmento permitido para reativacao. Checagens deste fluxo: ex-aluno esta no segmento permitido; cadencia permite contato; mensagem esta aprovada; responsavel esta definido.

**Meio**

Pedido de aprovacao: preparar reativacao de ex-aluno para aprovacao. O pedido mostra dados, impacto e proximo passo usando: ex-aluno esta no segmento permitido; cadencia permite contato; mensagem esta aprovada; responsavel esta definido; aprovador esta definido.

Nao aplica sem aprovacao. Tambem cria pendencia para a equipe se: ex-aluno pediu opt-out; historico tem reclamacao sensivel; segmento nao permite campanha; beneficio ou condicao especial foi sugerido; aprovacao vence ou permissao bloqueia.

**Fim**

A reativacao de ex-aluno vira aprovacao com segmento, mensagem e responsavel. Se aprovada, o contato e liberado; se houver opt-out, reclamacao ou beneficio especial, fica bloqueado.

**Ajustes do studio**

- aprovador.
- segmento permitido.
- cadencia.

**Requisitos readonly**

- aluno ou ex-aluno identificado.
- sinais de risco atualizados.
- historico disponivel conforme permissao.
- canal conectado.
- opt-out.
- cota.
- auditoria.

**Encadeamento**

/app/retencao/reativacoes; /app/aprovacoes

**Simulacao deve mostrar**

mostrar gatilho, dados usados, decisao do modo escolhido, mensagem/acao, aprovacao ou chamada humana quando houver, fallback, cota e auditoria.


### Rotina: Retencao preventiva

#### Satisfacao

- ID interno: `E6`.
- Nome canonico: `Satisfacao`.
- Modo padrao: `Autonomo com excecoes`.
- Teto: `Autonomo com excecoes`.
- Objetivo: acompanhar satisfacao e abrir cuidado quando necessario.

**Inicio**

O fluxo comeca quando chega a janela de medir satisfacao ou cuidado com o aluno. Checagens deste fluxo: janela de satisfacao chegou; aluno esta elegivel; responsavel esta definido; mensagem aprovada esta disponivel.

**Meio**

Trabalho do agente: acompanhar satisfacao e abrir cuidado quando necessario. Segue sem equipe se: janela de satisfacao chegou; aluno esta elegivel; responsavel esta definido; mensagem aprovada esta disponivel; nao ha reclamacao aberta.

Chama a equipe se: resposta indica reclamacao; nota baixa ou texto sensivel; aluno menciona saude, professor ou cobranca; ja existe caso aberto; canal, cota ou permissao bloqueia contato.

**Fim**

A satisfacao e coletada ou acompanhada e, se houver sinal ruim, abre cuidado. Se a resposta citar reclamacao, saude, professor ou cobranca, vai para humano.

**Ajustes do studio**

- janela.
- responsavel.
- quando abrir reclamacao.

**Requisitos readonly**

- aluno ou ex-aluno identificado.
- sinais de risco atualizados.
- historico disponivel conforme permissao.
- canal conectado.
- opt-out.
- cota.
- auditoria.

**Encadeamento**

/app/retencao; /app/reclamacoes; tarefa

**Simulacao deve mostrar**

mostrar gatilho, dados usados, decisao do modo escolhido, mensagem/acao, aprovacao ou chamada humana quando houver, fallback, cota e auditoria.

#### Retorno apos pausa

- ID interno: `E7`.
- Nome canonico: `Retorno apos pausa`.
- Modo padrao: `Autonomo com excecoes`.
- Teto: `Autonomo com excecoes`.
- Objetivo: preparar retorno apos pausa.

**Inicio**

O fluxo comeca quando uma pausa esta perto de terminar. Checagens deste fluxo: fim da pausa esta proximo; aluno esta elegivel para retorno; opcoes de agenda existem; responsavel esta definido.

**Meio**

Trabalho do agente: preparar retorno apos pausa. Segue sem equipe se: fim da pausa esta proximo; aluno esta elegivel para retorno; opcoes de agenda existem; responsavel esta definido; antecedencia configurada chegou.

Chama a equipe se: aluno pede estender pausa; agenda nao tem vaga; ha pendencia financeira; retorno exige cuidado ou professor especifico; canal, cota ou permissao bloqueia contato.

**Fim**

O retorno apos pausa prepara contato e opcoes de agenda antes do fim da pausa. Se o aluno pedir extensao, nao houver vaga ou houver pendencia, vira tarefa.

**Ajustes do studio**

- antecedencia.
- responsavel.
- quando chamar Agenda.

**Requisitos readonly**

- aluno ou ex-aluno identificado.
- sinais de risco atualizados.
- historico disponivel conforme permissao.
- canal conectado.
- opt-out.
- cota.
- auditoria.

**Encadeamento**

/app/retencao; /app/agenda; tarefa

**Simulacao deve mostrar**

mostrar gatilho, dados usados, decisao do modo escolhido, mensagem/acao, aprovacao ou chamada humana quando houver, fallback, cota e auditoria.


### Rotina: Casos sensiveis

#### Risco por perfil

- ID interno: `E8`.
- Nome canonico: `Risco por perfil`.
- Modo padrao: `Autonomo com aprovacao`.
- Teto: `Autonomo com aprovacao`.
- Objetivo: preparar acao de risco por perfil para aprovacao.

**Inicio**

O fluxo comeca quando um perfil ou segmento indica risco de evasao. Checagens deste fluxo: segmento de risco foi identificado; uso do segmento esta permitido; acao proposta foi definida; responsavel esta definido.

**Meio**

Pedido de aprovacao: preparar acao de risco por perfil para aprovacao. O pedido mostra dados, impacto e proximo passo usando: segmento de risco foi identificado; uso do segmento esta permitido; acao proposta foi definida; responsavel esta definido; aprovador esta definido.

Nao aplica sem aprovacao. Tambem cria pendencia para a equipe se: segmento e sensivel; acao pode parecer invasiva; dados usados nao estao permitidos; aluno tem caso aberto; aprovacao vence ou permissao bloqueia.

**Fim**

A acao por perfil de risco vira aprovacao com segmento, dados usados e abordagem. Se aprovada, a acao segue; se parecer invasiva ou usar dado sensivel, fica bloqueada.

**Ajustes do studio**

- aprovador.
- uso do segmento.
- responsavel.

**Requisitos readonly**

- aluno ou ex-aluno identificado.
- sinais de risco atualizados.
- historico disponivel conforme permissao.
- canal conectado.
- opt-out.
- cota.
- auditoria.

**Encadeamento**

/app/retencao/riscos; aprovacao/tarefa

**Simulacao deve mostrar**

mostrar gatilho, dados usados, decisao do modo escolhido, mensagem/acao, aprovacao ou chamada humana quando houver, fallback, cota e auditoria.

#### Pos-cancelamento

- ID interno: `E9`.
- Nome canonico: `Pos-cancelamento`.
- Modo padrao: `Autonomo com aprovacao`.
- Teto: `Autonomo com aprovacao`.
- Objetivo: preparar pos-cancelamento para aprovacao.

**Inicio**

O fluxo comeca depois que um cancelamento foi registrado e ainda pode haver cuidado pos-cancelamento. Checagens deste fluxo: cancelamento foi registrado; janela de contato esta definida; responsavel esta atribuido; mensagem nao reabre conflito.

**Meio**

Pedido de aprovacao: preparar pos-cancelamento para aprovacao. O pedido mostra dados, impacto e proximo passo usando: cancelamento foi registrado; janela de contato esta definida; responsavel esta atribuido; mensagem nao reabre conflito; aprovador esta definido.

Nao aplica sem aprovacao. Tambem cria pendencia para a equipe se: cancelamento teve reclamacao; aluno pediu nao ser contatado; motivo envolve saude ou evento pessoal; beneficio de retorno seria oferecido; aprovacao vence ou permissao bloqueia.

**Fim**

O pos-cancelamento vira aprovacao com janela, motivo e mensagem cuidadosa. Se aprovado, o contato e liberado; se houve reclamacao, saude ou pedido de nao contato, fica bloqueado.

**Ajustes do studio**

- aprovador.
- quando contatar.
- responsavel.

**Requisitos readonly**

- aluno ou ex-aluno identificado.
- sinais de risco atualizados.
- historico disponivel conforme permissao.
- canal conectado.
- opt-out.
- cota.
- auditoria.

**Encadeamento**

/app/cancelamentos; /app/aprovacoes; tarefa

**Simulacao deve mostrar**

mostrar gatilho, dados usados, decisao do modo escolhido, mensagem/acao, aprovacao ou chamada humana quando houver, fallback, cota e auditoria.


### Rotina: Retencao preventiva

#### Marco engajamento

- ID interno: `E10`.
- Nome canonico: `Marco engajamento`.
- Modo padrao: `Autonomo com excecoes`.
- Teto: `Autonomo com excecoes`.
- Objetivo: reconhecer marco de engajamento e acionar contato leve.

**Inicio**

O fluxo comeca quando um aluno atinge um marco de engajamento permitido. Checagens deste fluxo: marco configurado aconteceu; aluno esta ativo; tipo de marco esta permitido; responsavel esta definido.

**Meio**

Trabalho do agente: reconhecer marco de engajamento e acionar contato leve. Segue sem equipe se: marco configurado aconteceu; aluno esta ativo; tipo de marco esta permitido; responsavel esta definido; limite de contato nao foi atingido.

Chama a equipe se: aluno tem caso sensivel aberto; marco conflita com baixa frequencia; mensagem poderia soar inadequada; aluno pediu opt-out; canal, cota ou permissao bloqueia contato.

**Fim**

O marco de engajamento gera contato leve ou registro positivo. Se houver caso sensivel, baixa frequencia ou opt-out, a mensagem nao sai.

**Ajustes do studio**

- tipo de marco.
- responsavel.
- limite de contato.

**Requisitos readonly**

- aluno ou ex-aluno identificado.
- sinais de risco atualizados.
- historico disponivel conforme permissao.
- canal conectado.
- opt-out.
- cota.
- auditoria.

**Encadeamento**

/app/retencao; tarefa

**Simulacao deve mostrar**

mostrar gatilho, dados usados, decisao do modo escolhido, mensagem/acao, aprovacao ou chamada humana quando houver, fallback, cota e auditoria.


### Rotina: Casos sensiveis

#### Saude/evento pessoal

- ID interno: `E11`.
- Nome canonico: `Saude/evento pessoal`.
- Modo padrao: `Autonomo com aprovacao`.
- Teto: `Autonomo com aprovacao`.
- Objetivo: preparar caso de saude ou evento pessoal para aprovacao.

**Inicio**

O fluxo comeca quando aparece informacao de saude, evento pessoal ou cuidado sensivel. Checagens deste fluxo: evento foi identificado; visibilidade esta definida; dono do caso foi atribuido; nenhum contato automatico sera feito sem revisao.

**Meio**

Pedido de aprovacao: preparar caso de saude ou evento pessoal para aprovacao. O pedido mostra dados, impacto e proximo passo usando: evento foi identificado; visibilidade esta definida; dono do caso foi atribuido; nenhum contato automatico sera feito sem revisao; aprovador esta definido.

Nao aplica sem aprovacao. Tambem cria pendencia para a equipe se: informacao e sensivel ou incompleta; responsavel adequado nao esta claro; acao proposta pode expor dado privado; aluno pede sigilo; aprovacao vence ou permissao bloqueia.

**Fim**

Saude ou evento pessoal vira aprovacao com visibilidade, dono e cuidado proposto. Se aprovado, apenas a acao permitida segue; se houver sigilo ou dado incompleto, fica com humano.

**Ajustes do studio**

- dono do caso.
- visibilidade.
- aprovador.

**Requisitos readonly**

- aluno ou ex-aluno identificado.
- sinais de risco atualizados.
- historico disponivel conforme permissao.
- canal conectado.
- opt-out.
- cota.
- auditoria.

**Encadeamento**

/app/operacao; /app/historico; caso

**Simulacao deve mostrar**

mostrar gatilho, dados usados, decisao do modo escolhido, mensagem/acao, aprovacao ou chamada humana quando houver, fallback, cota e auditoria.

#### Segmentacao risco

- ID interno: `E12`.
- Nome canonico: `Segmentacao risco`.
- Modo padrao: `Autonomo com aprovacao`.
- Teto: `Autonomo com aprovacao`.
- Objetivo: preparar segmentacao de risco para aprovacao.

**Inicio**

O fluxo comeca quando o studio quer usar segmentacao de risco para acao operacional. Checagens deste fluxo: segmento foi definido; acao permitida foi escolhida; dados usados foram listados; responsavel esta definido.

**Meio**

Pedido de aprovacao: preparar segmentacao de risco para aprovacao. O pedido mostra dados, impacto e proximo passo usando: segmento foi definido; acao permitida foi escolhida; dados usados foram listados; responsavel esta definido; aprovador esta definido.

Nao aplica sem aprovacao. Tambem cria pendencia para a equipe se: segmento usa dado sensivel; acao nao esta permitida; alunos afetados sao muitos; risco de contato indevido aparece; aprovacao vence ou permissao bloqueia.

**Fim**

A segmentacao de risco vira aprovacao com dados usados, alunos afetados e acao permitida. Se aprovada, a acao segue; se usar dado sensivel ou volume alto, fica bloqueada.

**Ajustes do studio**

- aprovador.
- segmento.
- acao permitida.

**Requisitos readonly**

- aluno ou ex-aluno identificado.
- sinais de risco atualizados.
- historico disponivel conforme permissao.
- canal conectado.
- opt-out.
- cota.
- auditoria.

**Encadeamento**

/app/retencao/riscos; /app/aprovacoes

**Simulacao deve mostrar**

mostrar gatilho, dados usados, decisao do modo escolhido, mensagem/acao, aprovacao ou chamada humana quando houver, fallback, cota e auditoria.

#### Reclamacao e recuperacao de confianca

- ID interno: `E13`.
- Nome canonico: `Reclamacao e recuperacao de confianca`.
- Modo padrao: `Autonomo com aprovacao`.
- Teto: `Autonomo com aprovacao`.
- Objetivo: preparar recuperacao de reclamacao para aprovacao.

**Inicio**

O fluxo comeca quando uma reclamacao precisa de recuperacao de confianca. Checagens deste fluxo: reclamacao foi registrada; dono do caso esta definido; automacoes foram pausadas; resumo e proposta foram preparados.

**Meio**

Pedido de aprovacao: preparar recuperacao de reclamacao para aprovacao. O pedido mostra dados, impacto e proximo passo usando: reclamacao foi registrada; dono do caso esta definido; automacoes foram pausadas; resumo e proposta foram preparados; aprovador esta definido.

Nao aplica sem aprovacao. Tambem cria pendencia para a equipe se: reclamacao envolve professor, saude ou financeiro; aluno esta irritado ou pede cancelamento; proposta exige beneficio; risco reputacional alto; aprovacao vence ou permissao bloqueia.

**Fim**

A reclamacao vira aprovacao com resumo, dono, proposta e automacoes pausadas. Se aprovada, a recuperacao segue; se envolver professor, saude, financeiro ou beneficio, fica com responsavel.

**Ajustes do studio**

- dono do caso.
- aprovador.
- pausa automatica.

**Requisitos readonly**

- aluno ou ex-aluno identificado.
- sinais de risco atualizados.
- historico disponivel conforme permissao.
- canal conectado.
- opt-out.
- cota.
- auditoria.

**Encadeamento**

/app/reclamacoes; /app/operacao; /app/aprovacoes

**Simulacao deve mostrar**

mostrar gatilho, dados usados, decisao do modo escolhido, mensagem/acao, aprovacao ou chamada humana quando houver, fallback, cota e auditoria.


## Agente: Gestao/Governanca


### Rotina: Comando operacional

#### Prioridades dia

- ID interno: `F1`.
- Nome canonico: `Prioridades dia`.
- Modo padrao: `Autonomo`.
- Teto: `Autonomo`.
- Objetivo: montar prioridades do dia.

**Inicio**

O fluxo comeca quando chega o horario de montar as prioridades operacionais do dia. Checagens deste fluxo: fontes operacionais estao atualizadas; horario do resumo chegou; responsavel esta definido; tarefas e aprovacoes foram consolidadas.

**Meio**

Trabalho do agente: montar prioridades do dia. Conclui sem fila humana se: fontes operacionais estao atualizadas; horario do resumo chegou; responsavel esta definido; tarefas e aprovacoes foram consolidadas; nada critico impede leitura.

Para e cria pendencia para a equipe se: fonte importante falhou; ha incidente critico; dado principal esta desatualizado; responsavel nao esta definido; permissao ou cota bloqueia resumo.

**Fim**

As prioridades do dia aparecem em Hoje com tarefas, aprovacoes e alertas ordenados. Se fonte critica falhar ou dado estiver desatualizado, o resumo marca pendencia.

**Ajustes do studio**

- horario do resumo.
- responsavel.
- fontes exibidas.

**Requisitos readonly**

- dados operacionais atualizados.
- permissoes administrativas.
- fontes de uso/logs disponiveis.
- politica publicada quando houver.
- cota.
- auditoria.

**Encadeamento**

/app/hoje; /app/tarefas

**Simulacao deve mostrar**

mostrar gatilho, dados usados, decisao do modo escolhido, mensagem/acao, aprovacao ou chamada humana quando houver, fallback, cota e auditoria.

#### Dinheiro na mesa

- ID interno: `F2`.
- Nome canonico: `Dinheiro na mesa`.
- Modo padrao: `Autonomo com excecoes`.
- Teto: `Autonomo com excecoes`.
- Objetivo: identificar dinheiro na mesa e abrir proxima acao.

**Inicio**

O fluxo comeca quando o CRM identifica oportunidade financeira parada ou dinheiro na mesa. Checagens deste fluxo: oportunidade financeira foi detectada; frequencia do alerta permite envio; responsavel esta definido; acao sugerida nao altera financeiro sozinha.

**Meio**

Trabalho do agente: identificar dinheiro na mesa e abrir proxima acao. Segue sem equipe se: oportunidade financeira foi detectada; frequencia do alerta permite envio; responsavel esta definido; acao sugerida nao altera financeiro sozinha; dados financeiros estao disponiveis.

Chama a equipe se: valor esta incerto; caso depende de acordo ou desconto; movimentacao esta em disputa; responsavel nao existe; permissao ou cota bloqueia analise.

**Fim**

A oportunidade financeira vira proxima acao para responsavel sem alterar dinheiro sozinha. Se valor, disputa, desconto ou responsavel nao fecharem, fica tarefa.

**Ajustes do studio**

- frequencia.
- responsavel.
- quando abrir tarefa.

**Requisitos readonly**

- dados operacionais atualizados.
- permissoes administrativas.
- fontes de uso/logs disponiveis.
- politica publicada quando houver.
- cota.
- auditoria.

**Encadeamento**

/app/dinheiro-na-mesa; /app/financeiro; tarefa

**Simulacao deve mostrar**

mostrar gatilho, dados usados, decisao do modo escolhido, mensagem/acao, aprovacao ou chamada humana quando houver, fallback, cota e auditoria.

#### Fila humana

- ID interno: `F3`.
- Nome canonico: `Fila humana`.
- Modo padrao: `Autonomo`.
- Teto: `Autonomo`.
- Objetivo: organizar fila humana e prioridades.

**Inicio**

O fluxo comeca quando ha tarefas, aprovacoes ou casos humanos acumulados. Checagens deste fluxo: itens humanos foram encontrados; filas estao configuradas; prioridade foi calculada; responsaveis existem.

**Meio**

Trabalho do agente: organizar fila humana e prioridades. Conclui sem fila humana se: itens humanos foram encontrados; filas estao configuradas; prioridade foi calculada; responsaveis existem; nenhum item exige permissao ausente.

Para e cria pendencia para a equipe se: item sem dono; prioridade conflita entre filas; incidente aberto exige pausa; aprovacao vencida acumulou; permissao ou cota bloqueia atualizacao.

**Fim**

A fila humana fica ordenada por prioridade, dono e prazo. Se item sem dono, aprovacao vencida ou incidente aparecer, a operacao recebe alerta.

**Ajustes do studio**

- filas.
- prioridade.
- responsaveis.

**Requisitos readonly**

- dados operacionais atualizados.
- permissoes administrativas.
- fontes de uso/logs disponiveis.
- politica publicada quando houver.
- cota.
- auditoria.

**Encadeamento**

/app/operacao; /app/aprovacoes; /app/tarefas

**Simulacao deve mostrar**

mostrar gatilho, dados usados, decisao do modo escolhido, mensagem/acao, aprovacao ou chamada humana quando houver, fallback, cota e auditoria.

#### Gargalos

- ID interno: `F4`.
- Nome canonico: `Gargalos`.
- Modo padrao: `Autonomo com excecoes`.
- Teto: `Autonomo com excecoes`.
- Objetivo: detectar gargalos operacionais.

**Inicio**

O fluxo comeca quando indicadores mostram gargalo operacional. Checagens deste fluxo: metricas foram atualizadas; frequencia do alerta permite analise; tipo de alerta esta definido; responsavel esta atribuido.

**Meio**

Trabalho do agente: detectar gargalos operacionais. Segue sem equipe se: metricas foram atualizadas; frequencia do alerta permite analise; tipo de alerta esta definido; responsavel esta atribuido; acao sugerida e operacional.

Chama a equipe se: dado esta incompleto; gargalo envolve financeiro, grade ou incidente; alerta e critico; responsavel nao definido; permissao ou cota bloqueia analise.

**Fim**

O gargalo operacional vira alerta com metrica, causa provavel e responsavel. Se tocar financeiro, grade, incidente ou dado incompleto, vira investigacao humana.

**Ajustes do studio**

- frequencia.
- responsavel.
- tipo de alerta.

**Requisitos readonly**

- dados operacionais atualizados.
- permissoes administrativas.
- fontes de uso/logs disponiveis.
- politica publicada quando houver.
- cota.
- auditoria.

**Encadeamento**

/app/relatorios; /app/operacao; tarefa

**Simulacao deve mostrar**

mostrar gatilho, dados usados, decisao do modo escolhido, mensagem/acao, aprovacao ou chamada humana quando houver, fallback, cota e auditoria.

#### Resumo semanal

- ID interno: `F5`.
- Nome canonico: `Resumo semanal`.
- Modo padrao: `Autonomo`.
- Teto: `Autonomo`.
- Objetivo: gerar resumo semanal.

**Inicio**

O fluxo comeca quando a semana fecha e o studio precisa de resumo executivo. Checagens deste fluxo: periodo da semana fechou; secoes do resumo estao configuradas; destinatarios internos estao definidos; dados principais estao atualizados.

**Meio**

Trabalho do agente: gerar resumo semanal. Conclui sem fila humana se: periodo da semana fechou; secoes do resumo estao configuradas; destinatarios internos estao definidos; dados principais estao atualizados; nenhum incidente impede resumo.

Para e cria pendencia para a equipe se: fonte de dados falhou; secoes obrigatorias vazias; destinatario sem permissao; incidente critico em aberto; cota ou permissao bloqueia envio.

**Fim**

O resumo semanal e enviado/gerado para destinatarios permitidos com secoes configuradas. Se fonte, permissao ou incidente critico falhar, o resumo fica pendente.

**Ajustes do studio**

- dia/hora.
- destinatarios internos.
- secoes.

**Requisitos readonly**

- dados operacionais atualizados.
- permissoes administrativas.
- fontes de uso/logs disponiveis.
- politica publicada quando houver.
- cota.
- auditoria.

**Encadeamento**

/app/relatorios/semana; /app/hoje

**Simulacao deve mostrar**

mostrar gatilho, dados usados, decisao do modo escolhido, mensagem/acao, aprovacao ou chamada humana quando houver, fallback, cota e auditoria.

#### Qualidade dados

- ID interno: `F6`.
- Nome canonico: `Qualidade dados`.
- Modo padrao: `Autonomo com excecoes`.
- Teto: `Autonomo com excecoes`.
- Objetivo: detectar qualidade de dados e abrir tarefa de correcao.

**Inicio**

O fluxo comeca quando o CRM detecta dado incompleto, duplicado ou inconsistente. Checagens deste fluxo: tipo de dado a revisar pertence aos campos monitorados; duplicidade ou lacuna foi detectada; prioridade foi calculada; responsavel esta definido.

**Meio**

Trabalho do agente: detectar qualidade de dados e abrir tarefa de correcao. Segue sem equipe se: tipo de dado a revisar pertence aos campos monitorados; duplicidade ou lacuna foi detectada; prioridade foi calculada; responsavel esta definido; correcao automatica nao altera dado sensivel.

Chama a equipe se: correcao pode fundir cadastros; dado envolve historico protegido; conflito nao tem dono claro; volume e alto demais; permissao ou cota bloqueia analise.

**Fim**

A falha de qualidade de dados abre tarefa de correcao com prioridade e campo afetado. Se envolver fusao, historico protegido ou alto volume, vai para revisao.

**Ajustes do studio**

- responsavel.
- tipos de dado.
- prioridade.

**Requisitos readonly**

- dados operacionais atualizados.
- permissoes administrativas.
- fontes de uso/logs disponiveis.
- politica publicada quando houver.
- cota.
- auditoria.

**Encadeamento**

/app/dados/qualidade; /app/dados/duplicidades; tarefa

**Simulacao deve mostrar**

mostrar gatilho, dados usados, decisao do modo escolhido, mensagem/acao, aprovacao ou chamada humana quando houver, fallback, cota e auditoria.


### Rotina: Governanca de agentes

#### Creditos/limites

- ID interno: `F7`.
- Nome canonico: `Creditos/limites`.
- Modo padrao: `Autonomo`.
- Teto: `Autonomo`.
- Objetivo: monitorar creditos, limites e cotas.

**Inicio**

O fluxo comeca quando uso, creditos, limites ou cotas precisam ser monitorados. Checagens deste fluxo: uso foi atualizado; alertas 70/90/100 estao configurados; responsavel esta definido; limite comercial foi lido do billing.

**Meio**

Trabalho do agente: monitorar creditos, limites e cotas. Conclui sem fila humana se: uso foi atualizado; alertas 70/90/100 estao configurados; responsavel esta definido; limite comercial foi lido do billing; mensagem interna esta pronta.

Para e cria pendencia para a equipe se: cota atingiu limite critico; billing diverge do uso; responsavel nao definido; addon ou upgrade precisa decisao; permissao bloqueia leitura.

**Fim**

Uso, creditos e cotas recebem alerta nos limites configurados e aparecem em Uso/Cotas. Se billing divergir ou upgrade/add-on exigir decisao, vai para admin.

**Ajustes do studio**

- limiares de alerta.
- responsavel.
- mensagem interna.

**Requisitos readonly**

- dados operacionais atualizados.
- permissoes administrativas.
- fontes de uso/logs disponiveis.
- politica publicada quando houver.
- cota.
- auditoria.

**Encadeamento**

/app/uso; /app/uso/cotas; /app/hoje

**Simulacao deve mostrar**

mostrar gatilho, dados usados, decisao do modo escolhido, mensagem/acao, aprovacao ou chamada humana quando houver, fallback, cota e auditoria.

#### Performance

- ID interno: `F8`.
- Nome canonico: `Performance`.
- Modo padrao: `Autonomo com excecoes`.
- Teto: `Autonomo com excecoes`.
- Objetivo: monitorar performance dos agentes.

**Inicio**

O fluxo comeca quando indicadores de agentes precisam ser acompanhados. Checagens deste fluxo: metricas foram coletadas; frequencia permite novo relatorio; responsavel esta definido; indicadores configurados existem.

**Meio**

Trabalho do agente: monitorar performance dos agentes. Segue sem equipe se: metricas foram coletadas; frequencia permite novo relatorio; responsavel esta definido; indicadores configurados existem; acao sugerida nao altera politica sozinha.

Chama a equipe se: queda forte de performance; falha ou incidente correlacionado; amostra insuficiente; acao exige mudar fluxo ou politica; permissao ou cota bloqueia analise.

**Fim**

A performance dos agentes vira relatorio ou alerta com indicador afetado. Se queda forte, amostra insuficiente ou incidente correlacionado aparecer, abre investigacao.

**Ajustes do studio**

- frequencia.
- responsavel.
- metricas exibidas.

**Requisitos readonly**

- dados operacionais atualizados.
- permissoes administrativas.
- fontes de uso/logs disponiveis.
- politica publicada quando houver.
- cota.
- auditoria.

**Encadeamento**

/app/relatorios/agentes; /app/agentes; tarefa

**Simulacao deve mostrar**

mostrar gatilho, dados usados, decisao do modo escolhido, mensagem/acao, aprovacao ou chamada humana quando houver, fallback, cota e auditoria.

#### Permissoes/auditoria

- ID interno: `F9`.
- Nome canonico: `Permissoes/auditoria`.
- Modo padrao: `Autonomo com aprovacao`.
- Teto: `Autonomo com aprovacao`.
- Objetivo: preparar revisao de permissoes ou auditoria para aprovacao.

**Inicio**

O fluxo comeca quando evento de permissao ou auditoria exige revisao. Checagens deste fluxo: evento de auditoria foi identificado; tipo de evento esta dentro do escopo; responsavel esta definido; impacto foi resumido.

**Meio**

Pedido de aprovacao: preparar revisao de permissoes ou auditoria para aprovacao. O pedido mostra dados, impacto e proximo passo usando: evento de auditoria foi identificado; tipo de evento esta dentro do escopo; responsavel esta definido; impacto foi resumido; aprovador esta definido.

Nao aplica sem aprovacao. Tambem cria pendencia para a equipe se: evento e critico; mudanca de permissao seria necessaria; ha suspeita de acesso indevido; dados de auditoria incompletos; aprovacao vence ou permissao bloqueia.

**Fim**

Permissao ou evento de auditoria vira aprovacao com impacto e responsavel. Se houver suspeita de acesso indevido ou mudanca de permissao, nao aplica sem aprovacao.

**Ajustes do studio**

- aprovador.
- tipos de evento.
- responsavel.

**Requisitos readonly**

- dados operacionais atualizados.
- permissoes administrativas.
- fontes de uso/logs disponiveis.
- politica publicada quando houver.
- cota.
- auditoria.

**Encadeamento**

/app/auditoria; /app/configuracoes/permissoes; aprovacao

**Simulacao deve mostrar**

mostrar gatilho, dados usados, decisao do modo escolhido, mensagem/acao, aprovacao ou chamada humana quando houver, fallback, cota e auditoria.


### Rotina: Comando operacional

#### Capacidade/crescimento

- ID interno: `F10`.
- Nome canonico: `Capacidade/crescimento`.
- Modo padrao: `Autonomo com excecoes`.
- Teto: `Autonomo com excecoes`.
- Objetivo: detectar capacidade e crescimento.

**Inicio**

O fluxo comeca quando ocupacao, capacidade ou crescimento chegam perto de limite relevante. Checagens deste fluxo: ocupacao foi calculada; limite de alerta foi atingido ou esta proximo; responsavel esta definido; acao sugerida nao altera grade sozinha.

**Meio**

Trabalho do agente: detectar capacidade e crescimento. Segue sem equipe se: ocupacao foi calculada; limite de alerta foi atingido ou esta proximo; responsavel esta definido; acao sugerida nao altera grade sozinha; dados de agenda estao atualizados.

Chama a equipe se: capacidade ultrapassa limite; crescimento exige nova turma ou horario; dados de agenda conflitam; impacto financeiro aparece; permissao ou cota bloqueia analise.

**Fim**

Capacidade e crescimento viram alerta com ocupacao, limite e acao sugerida. Se exigir nova turma, horario ou impacto financeiro, fica para decisao.

**Ajustes do studio**

- frequencia.
- responsavel.
- limite de alerta.

**Requisitos readonly**

- dados operacionais atualizados.
- permissoes administrativas.
- fontes de uso/logs disponiveis.
- politica publicada quando houver.
- cota.
- auditoria.

**Encadeamento**

/app/relatorios/ocupacao; /app/agenda; tarefa

**Simulacao deve mostrar**

mostrar gatilho, dados usados, decisao do modo escolhido, mensagem/acao, aprovacao ou chamada humana quando houver, fallback, cota e auditoria.


### Rotina: Integracoes e importacao

#### Falhas/webhooks

- ID interno: `F11`.
- Nome canonico: `Falhas/webhooks`.
- Modo padrao: `Autonomo com excecoes`.
- Teto: `Autonomo com excecoes`.
- Objetivo: tratar falhas, webhooks e retries seguros.

**Inicio**

O fluxo comeca quando integracao, webhook ou tentativa tecnica falha. Checagens deste fluxo: falha tecnica foi identificada; severidade esta definida; retry seguro e permitido; responsavel esta atribuido.

**Meio**

Trabalho do agente: tratar falhas, webhooks e retries seguros. Segue sem equipe se: falha tecnica foi identificada; severidade esta definida; retry seguro e permitido; responsavel esta atribuido; log tecnico esta disponivel.

Chama a equipe se: retry pode duplicar efeito; falha persiste; severidade e alta; provedor esta indisponivel; permissao ou limite bloqueia mitigacao.

**Fim**

Falha tecnica ou webhook recebe retry seguro quando permitido e registro no log da integracao. Se houver risco de duplicar efeito, provedor instavel ou severidade alta, vai para incidente.

**Ajustes do studio**

- responsavel.
- severidade.
- quando tentar novamente.

**Requisitos readonly**

- dados operacionais atualizados.
- permissoes administrativas.
- fontes de uso/logs disponiveis.
- politica publicada quando houver.
- cota.
- auditoria.

**Encadeamento**

configuracao especifica da integracao; /app/operacao/incidentes

**Simulacao deve mostrar**

mostrar gatilho, dados usados, decisao do modo escolhido, mensagem/acao, aprovacao ou chamada humana quando houver, fallback, cota e auditoria.

#### Importacao/migracao

- ID interno: `F12`.
- Nome canonico: `Importacao/migracao`.
- Modo padrao: `Autonomo com aprovacao`.
- Teto: `Autonomo com aprovacao`.
- Objetivo: preparar importacao ou migracao para aprovacao.

**Inicio**

O fluxo comeca quando uma importacao ou migracao precisa ser validada. Checagens deste fluxo: lote foi identificado; amostra foi validada; impacto em dados foi resumido; responsavel esta definido.

**Meio**

Pedido de aprovacao: preparar importacao ou migracao para aprovacao. O pedido mostra dados, impacto e proximo passo usando: lote foi identificado; amostra foi validada; impacto em dados foi resumido; responsavel esta definido; aprovador esta definido.

Nao aplica sem aprovacao. Tambem cria pendencia para a equipe se: duplicidades ou conflitos aparecem; lote e grande demais; campos obrigatorios faltam; rollback nao esta claro; aprovacao vence ou permissao bloqueia.

**Fim**

Importacao ou migracao vira aprovacao com amostra, conflitos, impacto e rollback. Se aprovada, o lote segue; se houver duplicidade ou campo faltando, fica bloqueado.

**Ajustes do studio**

- aprovador.
- lote.
- responsavel.

**Requisitos readonly**

- dados operacionais atualizados.
- permissoes administrativas.
- fontes de uso/logs disponiveis.
- politica publicada quando houver.
- cota.
- auditoria.

**Encadeamento**

/app/importacao/[jobId]; /app/dados/qualidade; aprovacao

**Simulacao deve mostrar**

mostrar gatilho, dados usados, decisao do modo escolhido, mensagem/acao, aprovacao ou chamada humana quando houver, fallback, cota e auditoria.


### Rotina: Governanca de agentes

#### Teste de fluxo

- ID interno: `F13`.
- Nome canonico: `Teste de fluxo`.
- Modo padrao: `Autonomo`.
- Teto: `Autonomo`.
- Objetivo: rodar teste de fluxo em simulacao.

**Inicio**

O fluxo comeca quando alguem testa um fluxo antes de publicar ou alterar operacao. Checagens deste fluxo: cenario de teste foi escolhido; dados de exemplo estao disponiveis; fluxo nao publica acao real; responsavel por revisao esta definido.

**Meio**

Trabalho do agente: rodar teste de fluxo em simulacao. Conclui sem fila humana se: cenario de teste foi escolhido; dados de exemplo estao disponiveis; fluxo nao publica acao real; responsavel por revisao esta definido; resultado pode ser salvo.

Para e cria pendencia para a equipe se: cenario usa dado real sensivel; teste tenta publicar acao; resultado falha preflight; fluxo tem dependencia indisponivel; permissao ou cota bloqueia teste.

**Fim**

O teste roda em simulacao, mostra caminho do fluxo e nao publica acao real. Se usar dado sensivel, falhar preflight ou tentar executar de verdade, o teste para.

**Ajustes do studio**

- exemplos de simulacao.
- responsavel.

**Requisitos readonly**

- dados operacionais atualizados.
- permissoes administrativas.
- fontes de uso/logs disponiveis.
- politica publicada quando houver.
- cota.
- auditoria.

**Encadeamento**

/app/fluxos/[flowId]/simular; /app/fluxos/[flowId]

**Simulacao deve mostrar**

mostrar gatilho, dados usados, decisao do modo escolhido, mensagem/acao, aprovacao ou chamada humana quando houver, fallback, cota e auditoria.

#### Incidente de automacao e correcao operacional

- ID interno: `F14`.
- Nome canonico: `Incidente de automacao e correcao operacional`.
- Modo padrao: `Autonomo com excecoes`.
- Teto: `Autonomo com excecoes`.
- Objetivo: tratar incidente de automacao e correcao operacional.

**Inicio**

O fluxo comeca quando uma automacao falha, gera incidente ou precisa de correcao operacional. Checagens deste fluxo: incidente foi detectado; severidade esta definida; auto-pausa e permitida para o fluxo; responsavel esta atribuido.

**Meio**

Trabalho do agente: tratar incidente de automacao e correcao operacional. Segue sem equipe se: incidente foi detectado; severidade esta definida; auto-pausa e permitida para o fluxo; responsavel esta atribuido; execucao relacionada foi encontrada.

Chama a equipe se: incidente afeta varios fluxos; auto-pausa nao e permitida; correcao exige rollback; falha envolve integracao externa; permissao bloqueia mitigacao.

**Fim**

O incidente de automacao pausa ou mitiga o fluxo quando permitido e abre a execucao relacionada. Se afetar varios fluxos, exigir rollback ou depender de integracao, vai para incidente humano.

**Ajustes do studio**

- severidade.
- responsavel.
- auto-pausa.

**Requisitos readonly**

- dados operacionais atualizados.
- permissoes administrativas.
- fontes de uso/logs disponiveis.
- politica publicada quando houver.
- cota.
- auditoria.

**Encadeamento**

/app/operacao/incidentes/[incidentId]; /app/fluxos/execucoes/[runId]

**Simulacao deve mostrar**

mostrar gatilho, dados usados, decisao do modo escolhido, mensagem/acao, aprovacao ou chamada humana quando houver, fallback, cota e auditoria.

#### Mudanca de politica ou regra operacional

- ID interno: `F15`.
- Nome canonico: `Mudanca de politica ou regra operacional`.
- Modo padrao: `Autonomo com aprovacao`.
- Teto: `Autonomo com aprovacao`.
- Objetivo: preparar mudanca de politica ou regra operacional.

**Inicio**

O fluxo comeca quando politica, regra ou comportamento operacional precisa mudar. Checagens deste fluxo: politica ou regra foi identificada; data de vigencia esta definida; simulacao de impacto foi feita; comunicacao interna esta pronta.

**Meio**

Pedido de aprovacao: preparar mudanca de politica ou regra operacional. O pedido mostra dados, impacto e proximo passo usando: politica ou regra foi identificada; data de vigencia esta definida; simulacao de impacto foi feita; comunicacao interna esta pronta; aprovador esta definido.

Nao aplica sem aprovacao. Tambem cria pendencia para a equipe se: impacto afeta muitos fluxos; simulacao mostra conflito; vigencia e curta demais; comunicacao nao foi revisada; aprovacao vence ou permissao bloqueia.

**Fim**

Mudanca de politica vira aprovacao com simulacao, vigencia e comunicacao. Se aprovada, a nova versao fica pronta para publicar; se houver conflito, volta para revisao.

**Ajustes do studio**

- aprovador.
- data de vigencia.
- resumo da mudanca.

**Requisitos readonly**

- dados operacionais atualizados.
- permissoes administrativas.
- fontes de uso/logs disponiveis.
- politica publicada quando houver.
- cota.
- auditoria.

**Encadeamento**

/app/politicas/[policyId]; /app/aprovacoes; auditoria

**Simulacao deve mostrar**

mostrar gatilho, dados usados, decisao do modo escolhido, mensagem/acao, aprovacao ou chamada humana quando houver, fallback, cota e auditoria.


## Agente: Historico/Evolucao


### Rotina: Aula com contexto

#### Contexto antes aula

- ID interno: `G1`.
- Nome canonico: `Contexto antes aula`.
- Modo padrao: `Autonomo com excecoes`.
- Teto: `Autonomo com excecoes`.
- Objetivo: preparar contexto antes da aula para professor.

**Inicio**

O fluxo comeca antes de uma aula, quando o professor precisa de contexto permitido. Checagens deste fluxo: aula e professor foram identificados; alunos da aula foram listados; visibilidade do historico permite uso; contexto nao inclui dado protegido indevido.

**Meio**

Trabalho do agente: preparar contexto antes da aula para professor. Segue sem equipe se: aula e professor foram identificados; alunos da aula foram listados; visibilidade do historico permite uso; contexto nao inclui dado protegido indevido; professor pode receber o resumo.

Chama a equipe se: aluno tem restricao sensivel; professor sem permissao para dado; historico esta incompleto; aula foi alterada; permissao ou cota bloqueia resumo.

**Fim**

O professor recebe contexto permitido antes da aula sem dado protegido indevido. Se houver restricao sensivel, permissao faltando ou aula alterada, o resumo nao sai.

**Ajustes do studio**

- visibilidade.
- professor.
- quando chamar humano.

**Requisitos readonly**

- aluno/aula/professor identificados.
- permissao de historico.
- visibilidade definida.
- documentos permitidos quando houver.
- cota.
- auditoria.

**Encadeamento**

/app/professores; /app/aulas/[id]; tarefa

**Simulacao deve mostrar**

mostrar gatilho, dados usados, decisao do modo escolhido, mensagem/acao, aprovacao ou chamada humana quando houver, fallback, cota e auditoria.

#### Observacao pos-aula

- ID interno: `G2`.
- Nome canonico: `Observacao pos-aula`.
- Modo padrao: `Autonomo com excecoes`.
- Teto: `Autonomo com excecoes`.
- Objetivo: lembrar e organizar observacao pos-aula.

**Inicio**

O fluxo comeca depois da aula, quando uma observacao precisa ser registrada. Checagens deste fluxo: aula terminou; professor foi identificado; tipos de nota permitidos estao definidos; lembrete esta dentro do horario.

**Meio**

Trabalho do agente: lembrar e organizar observacao pos-aula. Segue sem equipe se: aula terminou; professor foi identificado; tipos de nota permitidos estao definidos; lembrete esta dentro do horario; nota ainda nao foi registrada.

Chama a equipe se: professor nao tem permissao; nota envolve restricao ou cuidado; aula nao foi fechada; aluno teve evento sensivel; canal, cota ou permissao bloqueia lembrete.

**Fim**

Depois da aula, o professor recebe lembrete e a observacao permitida entra no historico. Se a nota envolver cuidado, restricao ou evento sensivel, vai para revisao.

**Ajustes do studio**

- lembrete.
- professor.
- tipos de nota.

**Requisitos readonly**

- aluno/aula/professor identificados.
- permissao de historico.
- visibilidade definida.
- documentos permitidos quando houver.
- cota.
- auditoria.

**Encadeamento**

/app/aulas/[id]; /app/historico; tarefa

**Simulacao deve mostrar**

mostrar gatilho, dados usados, decisao do modo escolhido, mensagem/acao, aprovacao ou chamada humana quando houver, fallback, cota e auditoria.


### Rotina: Historico protegido

#### Restricao/cuidado

- ID interno: `G3`.
- Nome canonico: `Restricao/cuidado`.
- Modo padrao: `Autonomo com aprovacao`.
- Teto: `Autonomo com aprovacao`.
- Objetivo: preparar restricao ou cuidado para aprovacao.

**Inicio**

O fluxo comeca quando restricao, cuidado ou informacao sensivel precisa ser revisada. Checagens deste fluxo: aluno foi identificado; restricao ou cuidado foi classificado; visibilidade esta definida; dono do caso esta atribuido.

**Meio**

Pedido de aprovacao: preparar restricao ou cuidado para aprovacao. O pedido mostra dados, impacto e proximo passo usando: aluno foi identificado; restricao ou cuidado foi classificado; visibilidade esta definida; dono do caso esta atribuido; aprovador esta definido.

Nao aplica sem aprovacao. Tambem cria pendencia para a equipe se: informacao e sensivel ou incompleta; visibilidade nao esta clara; acao pode expor dado privado; professor ou responsavel diverge; aprovacao vence ou permissao bloqueia.

**Fim**

Restricao ou cuidado vira aprovacao com aluno, visibilidade, dono e acao proposta. Se aprovada, o historico protegido e atualizado; se houver dado incompleto, fica pendente.

**Ajustes do studio**

- aprovador.
- visibilidade.
- dono do caso.

**Requisitos readonly**

- aluno/aula/professor identificados.
- permissao de historico.
- visibilidade definida.
- documentos permitidos quando houver.
- cota.
- auditoria.

**Encadeamento**

/app/historico; /app/alunos/[id]; caso/aprovacao

**Simulacao deve mostrar**

mostrar gatilho, dados usados, decisao do modo escolhido, mensagem/acao, aprovacao ou chamada humana quando houver, fallback, cota e auditoria.


### Rotina: Aula com contexto

#### Objetivo/evolucao

- ID interno: `G4`.
- Nome canonico: `Objetivo/evolucao`.
- Modo padrao: `Autonomo com excecoes`.
- Teto: `Autonomo com excecoes`.
- Objetivo: acompanhar objetivo e evolucao do aluno.

**Inicio**

O fluxo comeca quando objetivo ou evolucao do aluno precisa ser acompanhado. Checagens deste fluxo: aluno foi identificado; objetivo ou evolucao esta dentro dos tipos permitidos; frequencia de acompanhamento esta definida; professor ou responsavel esta atribuido.

**Meio**

Trabalho do agente: acompanhar objetivo e evolucao do aluno. Segue sem equipe se: aluno foi identificado; objetivo ou evolucao esta dentro dos tipos permitidos; frequencia de acompanhamento esta definida; professor ou responsavel esta atribuido; historico permitido esta disponivel.

Chama a equipe se: evolucao envolve saude ou restricao; professor sem permissao; dado historico esta conflitante; acao exige contato sensivel; permissao ou cota bloqueia resumo.

**Fim**

Objetivo ou evolucao fica acompanhado no historico permitido e gera proximo cuidado quando configurado. Se tocar saude, restricao ou permissao de professor, vai para revisao.

**Ajustes do studio**

- professor/responsavel.
- frequencia.
- quando abrir tarefa.

**Requisitos readonly**

- aluno/aula/professor identificados.
- permissao de historico.
- visibilidade definida.
- documentos permitidos quando houver.
- cota.
- auditoria.

**Encadeamento**

/app/alunos/[id]/linha-do-tempo; tarefa

**Simulacao deve mostrar**

mostrar gatilho, dados usados, decisao do modo escolhido, mensagem/acao, aprovacao ou chamada humana quando houver, fallback, cota e auditoria.


### Rotina: Historico protegido

#### Contexto para agente

- ID interno: `G5`.
- Nome canonico: `Contexto para agente`.
- Modo padrao: `Autonomo com aprovacao`.
- Teto: `Autonomo com aprovacao`.
- Objetivo: preparar contexto permitido para agente.

**Inicio**

O fluxo comeca quando algum agente precisa de contexto de historico permitido. Checagens deste fluxo: escopo de dados foi definido; dados permitidos foram listados; objetivo de uso esta claro; aprovador esta definido.

**Meio**

Pedido de aprovacao: preparar contexto permitido para agente. O pedido mostra dados, impacto e proximo passo usando: escopo de dados foi definido; dados permitidos foram listados; objetivo de uso esta claro; aprovador esta definido; nenhum dado protegido sera liberado sem aprovacao.

Nao aplica sem aprovacao. Tambem cria pendencia para a equipe se: escopo amplo demais; dados incluem historico protegido; objetivo de uso nao esta claro; politica de privacidade conflita; aprovacao vence ou permissao bloqueia.

**Fim**

O contexto para outro agente vira aprovacao com escopo, dados e finalidade. Se aprovado, o agente recebe apenas o permitido; se amplo ou protegido demais, fica bloqueado.

**Ajustes do studio**

- aprovador.
- dados permitidos.
- escopo.

**Requisitos readonly**

- aluno/aula/professor identificados.
- permissao de historico.
- visibilidade definida.
- documentos permitidos quando houver.
- cota.
- auditoria.

**Encadeamento**

/app/historico/permissoes; /app/aprovacoes

**Simulacao deve mostrar**

mostrar gatilho, dados usados, decisao do modo escolhido, mensagem/acao, aprovacao ou chamada humana quando houver, fallback, cota e auditoria.

#### Documentos/anamnese

- ID interno: `G6`.
- Nome canonico: `Documentos/anamnese`.
- Modo padrao: `Autonomo com aprovacao`.
- Teto: `Autonomo com aprovacao`.
- Objetivo: preparar documentos ou anamnese para aprovacao.

**Inicio**

O fluxo comeca quando documento, anamnese ou arquivo do aluno precisa de revisao. Checagens deste fluxo: documento exigido foi identificado; aluno foi identificado; responsavel esta definido; visibilidade esta clara.

**Meio**

Pedido de aprovacao: preparar documentos ou anamnese para aprovacao. O pedido mostra dados, impacto e proximo passo usando: documento exigido foi identificado; aluno foi identificado; responsavel esta definido; visibilidade esta clara; aprovador esta definido.

Nao aplica sem aprovacao. Tambem cria pendencia para a equipe se: documento sensivel ou incompleto; anamnese exige revisao humana; arquivo nao e permitido; dados conflitam com historico; aprovacao vence ou permissao bloqueia.

**Fim**

Documento ou anamnese vira aprovacao com aluno, arquivo, visibilidade e responsavel. Se aprovado, fica disponivel no historico permitido; se sensivel/incompleto, vai para revisao.

**Ajustes do studio**

- aprovador.
- documentos exigidos.
- responsavel.

**Requisitos readonly**

- aluno/aula/professor identificados.
- permissao de historico.
- visibilidade definida.
- documentos permitidos quando houver.
- cota.
- auditoria.

**Encadeamento**

/app/historico/documentos; /app/aprovacoes; tarefa

**Simulacao deve mostrar**

mostrar gatilho, dados usados, decisao do modo escolhido, mensagem/acao, aprovacao ou chamada humana quando houver, fallback, cota e auditoria.

#### Correcao historico

- ID interno: `G7`.
- Nome canonico: `Correcao historico`.
- Modo padrao: `Autonomo com aprovacao`.
- Teto: `Autonomo com aprovacao`.
- Objetivo: preparar correcao de historico para aprovacao.

**Inicio**

O fluxo comeca quando alguem pede correcao de historico. Checagens deste fluxo: evento historico foi identificado; motivo obrigatorio foi informado; valor anterior foi preservado; impacto da correcao foi mostrado.

**Meio**

Pedido de aprovacao: preparar correcao de historico para aprovacao. O pedido mostra dados, impacto e proximo passo usando: evento historico foi identificado; motivo obrigatorio foi informado; valor anterior foi preservado; impacto da correcao foi mostrado; aprovador esta definido.

Nao aplica sem aprovacao. Tambem cria pendencia para a equipe se: motivo esta incompleto; correcao afeta dado protegido; professor ou aluno divergem; evento original nao pode ser localizado; aprovacao vence ou permissao bloqueia.

**Fim**

A correcao de historico vira aprovacao preservando valor anterior, motivo e impacto. Se aprovada, o historico muda com rastro; se houver divergencia, fica pendente.

**Ajustes do studio**

- aprovador.
- motivo obrigatorio.
- prazo de aprovacao.

**Requisitos readonly**

- aluno/aula/professor identificados.
- permissao de historico.
- visibilidade definida.
- documentos permitidos quando houver.
- cota.
- auditoria.

**Encadeamento**

/app/historico; /app/auditoria; aprovacao

**Simulacao deve mostrar**

mostrar gatilho, dados usados, decisao do modo escolhido, mensagem/acao, aprovacao ou chamada humana quando houver, fallback, cota e auditoria.


### Rotina: Aula com contexto

#### Repasse entre professores

- ID interno: `G8`.
- Nome canonico: `Repasse entre professores`.
- Modo padrao: `Autonomo com excecoes`.
- Teto: `Autonomo com excecoes`.
- Objetivo: preparar repasse entre professores.

**Inicio**

O fluxo comeca quando professor precisa repassar contexto para outro professor. Checagens deste fluxo: professor origem e destino foram identificados; campos do resumo estao definidos; alunos ou aulas relacionados foram listados; visibilidade do historico permite repasse.

**Meio**

Trabalho do agente: preparar repasse entre professores. Segue sem equipe se: professor origem e destino foram identificados; campos do resumo estao definidos; alunos ou aulas relacionados foram listados; visibilidade do historico permite repasse; mensagem interna esta pronta.

Chama a equipe se: professor destino sem permissao; resumo inclui dado protegido; aula ou professor mudou; contexto esta incompleto; permissao ou cota bloqueia repasse.

**Fim**

O repasse entre professores envia resumo permitido para o professor destino. Se incluir dado protegido, destino sem permissao ou contexto incompleto, o repasse para.

**Ajustes do studio**

- professor destino.
- campos do resumo.
- quando chamar humano.

**Requisitos readonly**

- aluno/aula/professor identificados.
- permissao de historico.
- visibilidade definida.
- documentos permitidos quando houver.
- cota.
- auditoria.

**Encadeamento**

/app/professores; /app/tarefas

**Simulacao deve mostrar**

mostrar gatilho, dados usados, decisao do modo escolhido, mensagem/acao, aprovacao ou chamada humana quando houver, fallback, cota e auditoria.

#### Lembrete professor

- ID interno: `G9`.
- Nome canonico: `Lembrete professor`.
- Modo padrao: `Autonomo`.
- Teto: `Autonomo`.
- Objetivo: enviar lembrete para professor.

**Inicio**

O fluxo comeca quando professor precisa receber lembrete operacional. Checagens deste fluxo: professor foi identificado; horario ou frequencia chegou; destino do lembrete esta definido; conteudo nao inclui dado protegido indevido.

**Meio**

Trabalho do agente: enviar lembrete para professor. Conclui sem fila humana se: professor foi identificado; horario ou frequencia chegou; destino do lembrete esta definido; conteudo nao inclui dado protegido indevido; lembrete ainda nao foi enviado.

Para e cria pendencia para a equipe se: professor sem canal ou permissao; lembrete duplicado; conteudo depende de dado protegido; aula foi alterada; canal, cota ou permissao bloqueia envio.

**Fim**

O lembrete do professor e enviado no horario/frequencia configurado e marcado como feito. Se aula mudou, canal falhou ou conteudo depender de dado protegido, nao envia.

**Ajustes do studio**

- horario.
- frequencia.
- destino.

**Requisitos readonly**

- aluno/aula/professor identificados.
- permissao de historico.
- visibilidade definida.
- documentos permitidos quando houver.
- cota.
- auditoria.

**Encadeamento**

/app/professores; /app/tarefas

**Simulacao deve mostrar**

mostrar gatilho, dados usados, decisao do modo escolhido, mensagem/acao, aprovacao ou chamada humana quando houver, fallback, cota e auditoria.


### Rotina: Historico protegido

#### Compartilhar contexto

- ID interno: `G10`.
- Nome canonico: `Compartilhar contexto`.
- Modo padrao: `Autonomo com aprovacao`.
- Teto: `Autonomo com aprovacao`.
- Objetivo: preparar compartilhamento de contexto.

**Inicio**

O fluxo comeca quando contexto do aluno precisa ser compartilhado com alguem. Checagens deste fluxo: destinatario foi identificado; dados permitidos foram selecionados; objetivo do compartilhamento esta claro; preview foi gerado.

**Meio**

Pedido de aprovacao: preparar compartilhamento de contexto. O pedido mostra dados, impacto e proximo passo usando: destinatario foi identificado; dados permitidos foram selecionados; objetivo do compartilhamento esta claro; preview foi gerado; aprovador esta definido.

Nao aplica sem aprovacao. Tambem cria pendencia para a equipe se: destinatario nao tem permissao; dados incluem historico protegido; objetivo e ambiguo; aluno pediu restricao de compartilhamento; aprovacao vence ou permissao bloqueia.

**Fim**

O compartilhamento de contexto vira aprovacao com destinatario, dados e finalidade. Se aprovado, o contexto e compartilhado; se houver restricao ou permissao faltando, fica bloqueado.

**Ajustes do studio**

- aprovador.
- destinatario.
- dados permitidos.

**Requisitos readonly**

- aluno/aula/professor identificados.
- permissao de historico.
- visibilidade definida.
- documentos permitidos quando houver.
- cota.
- auditoria.

**Encadeamento**

/app/aprovacoes; /app/conversas/[id]

**Simulacao deve mostrar**

mostrar gatilho, dados usados, decisao do modo escolhido, mensagem/acao, aprovacao ou chamada humana quando houver, fallback, cota e auditoria.

#### Permissao historico

- ID interno: `G11`.
- Nome canonico: `Permissao historico`.
- Modo padrao: `Autonomo com aprovacao`.
- Teto: `Autonomo com aprovacao`.
- Objetivo: preparar permissao de historico.

**Inicio**

O fluxo comeca quando permissao de historico precisa ser alterada ou revisada. Checagens deste fluxo: papel ou perfil foi identificado; escopo de visibilidade esta definido; impacto foi mostrado; responsavel esta atribuido.

**Meio**

Pedido de aprovacao: preparar permissao de historico. O pedido mostra dados, impacto e proximo passo usando: papel ou perfil foi identificado; escopo de visibilidade esta definido; impacto foi mostrado; responsavel esta atribuido; aprovador esta definido.

Nao aplica sem aprovacao. Tambem cria pendencia para a equipe se: escopo amplo demais; papel nao deveria ver dado protegido; conflito com permissao global; evento de auditoria e sensivel; aprovacao vence ou permissao bloqueia.

**Fim**

Permissao de historico vira aprovacao com papel, escopo e impacto. Se aprovada, a visibilidade muda; se conflitar com permissao global ou dado protegido, fica pendente.

**Ajustes do studio**

- aprovador.
- papel.
- escopo de visibilidade.

**Requisitos readonly**

- aluno/aula/professor identificados.
- permissao de historico.
- visibilidade definida.
- documentos permitidos quando houver.
- cota.
- auditoria.

**Encadeamento**

/app/historico/permissoes; /app/configuracoes/permissoes; auditoria

**Simulacao deve mostrar**

mostrar gatilho, dados usados, decisao do modo escolhido, mensagem/acao, aprovacao ou chamada humana quando houver, fallback, cota e auditoria.


### Rotina: Aula com contexto

#### Linha do tempo

- ID interno: `G12`.
- Nome canonico: `Linha do tempo`.
- Modo padrao: `Autonomo com excecoes`.
- Teto: `Autonomo com excecoes`.
- Objetivo: organizar linha do tempo do aluno.

**Inicio**

O fluxo comeca quando a linha do tempo do aluno precisa ser organizada ou exibida. Checagens deste fluxo: aluno foi identificado; tipos de evento estao permitidos; filtro padrao esta definido; responsavel esta atribuido.

**Meio**

Trabalho do agente: organizar linha do tempo do aluno. Segue sem equipe se: aluno foi identificado; tipos de evento estao permitidos; filtro padrao esta definido; responsavel esta atribuido; historico pode ser exibido sem dado indevido.

Chama a equipe se: evento protegido aparece; historico conflita ou esta incompleto; usuario nao tem permissao; filtro mostra dado sensivel; permissao ou cota bloqueia exibicao.

**Fim**

A linha do tempo do aluno fica organizada com eventos permitidos e filtro seguro. Se aparecer evento protegido, conflito ou falta de permissao, a exibicao restringe e abre revisao.

**Ajustes do studio**

- tipos de evento.
- filtro padrao.
- responsavel.

**Requisitos readonly**

- aluno/aula/professor identificados.
- permissao de historico.
- visibilidade definida.
- documentos permitidos quando houver.
- cota.
- auditoria.

**Encadeamento**

/app/alunos/[id]/linha-do-tempo; tarefa

**Simulacao deve mostrar**

mostrar gatilho, dados usados, decisao do modo escolhido, mensagem/acao, aprovacao ou chamada humana quando houver, fallback, cota e auditoria.
