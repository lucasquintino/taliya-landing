# Taliya CRM - 96 Simulacoes De Fluxos

Status: mapeamento completo v0.1.
Data: 2026-05-22.

Este documento define exatamente o que aparece na pagina `Testar fluxo` para cada um dos 96 fluxos.

Cada fluxo tem cenarios, visual central, execucao do teste, limite do agente, chamada humana/aprovacao/fallback e texto do Agente de Configuracao.

Regra principal: todos usam o mesmo esqueleto da tela de teste, mas nem todos usam celular. O visual central representa onde aquele fluxo realmente acontece.


## Agente: Atendimento


### Rotina: Conversas e triagem

#### Nova conversa

- ID interno: `A1`.
- Modo padrao: `Autonomo com excecoes`.
- Visual central: `Celular/conversa`.
- Usa celular: `sim`.

**Cenarios**

- `Mensagem simples nova`: Classifica assunto e abre atendimento.
- `Contato nao identificado`: Cria caso humano antes de responder.
- `Mensagem com desconto e reclamacao`: Chama equipe por assunto sensivel.
- `Canal ou cota bloqueia`: Para e cria pendencia no Inbox.

**Visual Do Caso**

celular com conversa simulada e cartao interno mostrando o resultado do fluxo

**Execucao Do Teste**

1. Inicio: O fluxo comeca quando uma nova mensagem chega por WhatsApp, inbox ou outro canal conectado e ainda nao tem destino claro.
2. Checagens: mensagem chegou por canal conectado; contato esta identificado ou pode receber resposta geral; assunto inicial foi reconhecido; fila de atendimento esta definida; limite de respostas nao foi atingido.
3. Decisao: No cenario `Mensagem simples nova`, a Taliya segue sem equipe porque nenhuma excecao foi encontrada.
4. Acao: Executa o caso valido: classificar a conversa, abrir atendimento e mandar para a fila certa.
5. Fim: A conversa fica classificada, o atendimento abre na fila correta e o historico mostra por que aquele destino foi escolhido. Se houver conflito de assunto, identidade ou fila, a conversa vira caso humano no Inbox.

**Limite Do Agente**

Nao responde conversa sensivel nem decide fila sem responsavel.

**Humano/Aprovacao/Fallback**

- Chama humano quando: contato nao foi identificado; mensagem mistura varios assuntos; pedido envolve desconto, saude, privacidade ou reclamacao; fila de atendimento nao tem responsavel; canal, cota, opt-out ou permissao bloqueia resposta.
- Pede aprovacao quando: Nao pede aprovacao no cenario principal; nas excecoes, chama humano em vez de aprovar automaticamente.
- Fallback do teste: Se o teste cair em `Canal ou cota bloqueia`, Para e cria pendencia no Inbox.

**Agente De Configuracao**

Neste teste, a Taliya executa Nova conversa apenas no cenario valido. Se aparecer `Contato nao identificado` ou `Mensagem com desconto e reclamacao`, chama a equipe.

#### Duvidas permitidas

- ID interno: `A2`.
- Modo padrao: `Autonomo`.
- Visual central: `Celular/conversa`.
- Usa celular: `sim`.

**Cenarios**

- `Pergunta esta na base`: Responde com conteudo aprovado.
- `Pergunta fora da base`: Cria tarefa de resposta.
- `Pedido de dado privado`: Chama equipe antes de responder.
- `Opt-out ou cota bloqueia`: Para sem enviar mensagem.

**Visual Do Caso**

celular com conversa simulada e cartao interno mostrando o resultado do fluxo

**Execucao Do Teste**

1. Inicio: O fluxo comeca quando um lead, aluno ou responsavel faz uma pergunta que pode estar na base aprovada do studio.
2. Checagens: pergunta esta na base permitida; resposta nao exige dado sensivel; contato pode receber resposta pelo canal; limite por conversa nao foi atingido; fallback esta definido.
3. Decisao: No cenario `Pergunta esta na base`, a Taliya conclui sem equipe porque as checagens obrigatorias passam.
4. Acao: Conclui a acao permitida: responder duvidas permitidas usando a base aprovada.
5. Fim: A resposta aprovada e enviada na conversa e a pergunta fica registrada como atendida pela base permitida. Se a pergunta sair da base, pedir dado privado ou exigir condicao especial, nasce uma tarefa de resposta para a equipe.

**Limite Do Agente**

Nao responde fora da base aprovada nem envia dado privado.

**Humano/Aprovacao/Fallback**

- Chama humano quando: Nao chama humano no cenario principal; se cair em `Opt-out ou cota bloqueia`, aplica fallback: Para sem enviar mensagem.
- Pede aprovacao quando: Nao pede aprovacao no cenario principal; se houver bloqueio, aplica o fallback definido.
- Fallback do teste: Se o teste cair em `Opt-out ou cota bloqueia`, Para sem enviar mensagem.

**Agente De Configuracao**

Neste teste, a Taliya conclui Duvidas permitidas quando as checagens passam. Se aparecer `Opt-out ou cota bloqueia`, ela para e cria pendencia.

#### Aluno existente

- ID interno: `A3`.
- Modo padrao: `Autonomo com excecoes`.
- Visual central: `Celular/conversa`.
- Usa celular: `sim`.

**Cenarios**

- `Aluno reconhecido`: Liga conversa ao cadastro correto.
- `Telefone atende dois alunos`: Segura dados e chama equipe.
- `Aluno contesta cadastro`: Cria revisao humana.
- `Permissao bloqueia contexto`: Para antes de expor informacao.

**Visual Do Caso**

celular com conversa simulada e cartao interno mostrando o resultado do fluxo

**Execucao Do Teste**

1. Inicio: O fluxo comeca quando uma conversa parece vir de aluno existente e precisa ser ligada ao cadastro certo antes de continuar.
2. Checagens: telefone corresponde a um aluno ou responsavel permitido; cadastro nao tem conflito de identidade; pedido usa dados permitidos; fila destino esta definida; botao de ajuda permanece disponivel.
3. Decisao: No cenario `Aluno reconhecido`, a Taliya segue sem equipe porque nenhuma excecao foi encontrada.
4. Acao: Executa o caso valido: reconhecer aluno existente e encaminhar atendimento com contexto.
5. Fim: A conversa fica ligada ao cadastro certo e o atendimento segue com contexto do aluno permitido para aquela fila. Se houver telefone compartilhado, duplicidade ou pedido sensivel, a Taliya segura os dados e cria revisao humana.

**Limite Do Agente**

Nao expoe contexto quando identidade ou cadastro estiverem duvidosos.

**Humano/Aprovacao/Fallback**

- Chama humano quando: telefone atende mais de um aluno; cadastro esta duplicado; pedido exige alteracao sensivel; aluno contesta informacao do CRM; canal, cota ou permissao bloqueia acao.
- Pede aprovacao quando: Nao pede aprovacao no cenario principal; nas excecoes, chama humano em vez de aprovar automaticamente.
- Fallback do teste: Se o teste cair em `Permissao bloqueia contexto`, Para antes de expor informacao.

**Agente De Configuracao**

Neste teste, a Taliya executa Aluno existente apenas no cenario valido. Se aparecer `Telefone atende dois alunos` ou `Aluno contesta cadastro`, chama a equipe.

#### Fora do escopo

- ID interno: `A4`.
- Modo padrao: `Autonomo`.
- Visual central: `Celular/conversa`.
- Usa celular: `sim`.

**Cenarios**

- `Pedido fora do CRM`: Responde com mensagem padrao.
- `Mensagem parece reclamacao`: Chama equipe.
- `Pessoa insiste em humano`: Cria caso para atendimento.
- `Canal falha`: Para e cria pendencia.

**Visual Do Caso**

celular com conversa simulada e cartao interno mostrando o resultado do fluxo

**Execucao Do Teste**

1. Inicio: O fluxo comeca quando a pessoa faz um pedido que nao pertence ao escopo operacional do CRM do studio.
2. Checagens: assunto nao pertence ao CRM do studio; resposta padrao esta aprovada; contato nao pediu humano; destino da tarefa ou caso esta definido; mensagem nao contem risco sensivel.
3. Decisao: No cenario `Pedido fora do CRM`, a Taliya conclui sem equipe porque as checagens obrigatorias passam.
4. Acao: Conclui a acao permitida: responder fora de escopo e criar destino correto.
5. Fim: A pessoa recebe a resposta padrao de fora do escopo e, quando fizer sentido, o pedido vira tarefa/caso no destino configurado. Se o texto indicar reclamacao, emergencia, saude ou dado pessoal, o caso vai para humano.

**Limite Do Agente**

Nao trata emergencia, saude, dado pessoal ou reclamacao como pedido simples.

**Humano/Aprovacao/Fallback**

- Chama humano quando: Nao chama humano no cenario principal; se cair em `Canal falha`, aplica fallback: Para e cria pendencia.
- Pede aprovacao quando: Nao pede aprovacao no cenario principal; se houver bloqueio, aplica o fallback definido.
- Fallback do teste: Se o teste cair em `Canal falha`, Para e cria pendencia.

**Agente De Configuracao**

Neste teste, a Taliya conclui Fora do escopo quando as checagens passam. Se aparecer `Canal falha`, ela para e cria pendencia.

#### Chamada humana

- ID interno: `A5`.
- Modo padrao: `Autonomo`.
- Visual central: `Celular/conversa`.
- Usa celular: `sim`.

**Cenarios**

- `Handoff comum`: Envia conversa para fila certa.
- `Fila nao existe`: Cria pendencia operacional.
- `Prioridade nao clara`: Pede decisao de triagem.
- `Responsavel indisponivel`: Mantem caso aguardando dono.

**Visual Do Caso**

celular com conversa simulada e cartao interno mostrando o resultado do fluxo

**Execucao Do Teste**

1. Inicio: O fluxo comeca quando uma conversa precisa sair da automacao e ir para uma pessoa da equipe.
2. Checagens: gatilho de humano foi detectado; fila destino esta definida; prioridade foi calculada; resumo obrigatorio foi gerado; responsavel pode assumir o caso.
3. Decisao: No cenario `Handoff comum`, a Taliya conclui sem equipe porque as checagens obrigatorias passam.
4. Acao: Conclui a acao permitida: chamar humano com resumo, fila e prioridade.
5. Fim: O humano recebe a conversa com resumo, prioridade e fila definida. Se a Taliya nao conseguir escolher fila, prioridade ou responsavel, o caso fica em pendencia operacional ate alguem assumir.

**Limite Do Agente**

Nao resolve o atendimento; entrega para humano com resumo, fila e prioridade.

**Humano/Aprovacao/Fallback**

- Chama humano quando: Nao chama humano no cenario principal; se cair em `Responsavel indisponivel`, aplica fallback: Mantem caso aguardando dono.
- Pede aprovacao quando: Nao pede aprovacao no cenario principal; se houver bloqueio, aplica o fallback definido.
- Fallback do teste: Se o teste cair em `Responsavel indisponivel`, Mantem caso aguardando dono.

**Agente De Configuracao**

Neste teste, a Taliya conclui Chamada humana quando as checagens passam. Se aparecer `Responsavel indisponivel`, ela para e cria pendencia.


### Rotina: Identidade e privacidade

#### Consentimento/opt-out

- ID interno: `A6`.
- Modo padrao: `Autonomo`.
- Visual central: `Celular/conversa`.
- Usa celular: `sim`.

**Cenarios**

- `Opt-out claro`: Registra preferencia de contato.
- `Pedido ambiguo`: Abre revisao.
- `Telefone compartilhado`: Nao aplica preferencia sem validar.
- `Permissao bloqueia registro`: Cria pendencia para responsavel.

**Visual Do Caso**

celular com conversa simulada e cartao interno mostrando o resultado do fluxo

**Execucao Do Teste**

1. Inicio: O fluxo comeca quando o contato pede consentimento, opt-out ou mudanca de preferencia de comunicacao.
2. Checagens: contato foi identificado; pedido de consentimento ou opt-out e claro; texto de confirmacao esta aprovado; responsavel de revisao existe para caso ambiguo; auditoria pode ser registrada.
3. Decisao: No cenario `Opt-out claro`, a Taliya conclui sem equipe porque as checagens obrigatorias passam.
4. Acao: Conclui a acao permitida: registrar consentimento, opt-out ou preferencia de contato.
5. Fim: A preferencia de contato, consentimento ou opt-out fica registrado no contato e passa a valer para os proximos envios. Se o pedido for ambiguo, envolver telefone compartilhado ou pedir dados pessoais, a revisao vai para responsavel.

**Limite Do Agente**

Nao altera preferencia de contato quando o pedido estiver ambiguo ou o telefone for compartilhado.

**Humano/Aprovacao/Fallback**

- Chama humano quando: Nao chama humano no cenario principal; se cair em `Permissao bloqueia registro`, aplica fallback: Cria pendencia para responsavel.
- Pede aprovacao quando: Nao pede aprovacao no cenario principal; se houver bloqueio, aplica o fallback definido.
- Fallback do teste: Se o teste cair em `Permissao bloqueia registro`, Cria pendencia para responsavel.

**Agente De Configuracao**

Neste teste, a Taliya conclui Consentimento/opt-out quando as checagens passam. Se aparecer `Permissao bloqueia registro`, ela para e cria pendencia.

#### Identidade/midias

- ID interno: `A7`.
- Modo padrao: `Autonomo com excecoes`.
- Visual central: `Celular/conversa`.
- Usa celular: `sim`.

**Cenarios**

- `Audio legivel`: Classifica midia e vincula ao atendimento.
- `Documento sensivel`: Abre revisao antes de usar.
- `Identidade nao confere`: Segura conteudo e chama equipe.
- `Arquivo nao aceito`: Para e registra bloqueio.

**Visual Do Caso**

celular com conversa simulada e cartao interno mostrando o resultado do fluxo

**Execucao Do Teste**

1. Inicio: O fluxo comeca quando a conversa recebe audio, imagem, documento ou outra midia que precisa ser interpretada com cuidado.
2. Checagens: midia e legivel; tipo de midia e aceito; contato esta identificado; conteudo nao traz dado sensivel inesperado; responsavel de revisao esta definido.
3. Decisao: No cenario `Audio legivel`, a Taliya segue sem equipe porque nenhuma excecao foi encontrada.
4. Acao: Executa o caso valido: tratar identidade, audio, imagem ou midia recebida.
5. Fim: A midia fica vinculada ao atendimento com classificacao segura e destino de revisao quando precisar. Se o arquivo for ilegivel, sensivel, nao aceito ou a identidade nao conferir, a Taliya nao usa o conteudo e abre revisao.

**Limite Do Agente**

Nao usa midia ilegivel, sensivel ou com identidade incerta.

**Humano/Aprovacao/Fallback**

- Chama humano quando: midia esta ilegivel; documento parece sensivel; identidade nao confere; arquivo nao e aceito; canal, cota ou permissao bloqueia acao.
- Pede aprovacao quando: Nao pede aprovacao no cenario principal; nas excecoes, chama humano em vez de aprovar automaticamente.
- Fallback do teste: Se o teste cair em `Arquivo nao aceito`, Para e registra bloqueio.

**Agente De Configuracao**

Neste teste, a Taliya executa Identidade/midias apenas no cenario valido. Se aparecer `Documento sensivel` ou `Identidade nao confere`, chama a equipe.

#### Privacidade/dados

- ID interno: `A8`.
- Modo padrao: `Autonomo com aprovacao`.
- Visual central: `Pedido de aprovacao`.
- Usa celular: `nao`.

**Cenarios**

- `Pedido de acesso a dados`: Monta aprovacao de privacidade.
- `Identidade nao confirmada`: Cria pendencia de validacao.
- `Pedido amplo de exclusao`: Exige aprovacao humana.
- `Aprovacao vence`: Mantem caso pendente.

**Visual Do Caso**

card de aprovacao com dados, impacto, decisao pendente e efeito se aprovado

**Execucao Do Teste**

1. Inicio: O fluxo comeca quando alguem pede acesso, exclusao, copia ou revisao de dados pessoais.
2. Checagens: solicitante foi identificado; tipo de pedido de dado foi classificado; dados envolvidos foram listados; SLA do caso esta definido; aprovador de privacidade esta definido.
3. Decisao: No cenario `Pedido de acesso a dados`, a Taliya nao aplica sozinha: monta um pedido de aprovacao para humano autorizado.
4. Pedido de aprovacao: Monta a aprovacao para revisar pedido de privacidade ou dados, mostrando solicitante foi identificado; tipo de pedido de dado foi classificado; dados envolvidos foram listados; SLA do caso esta definido.
5. Fim: O pedido de privacidade vira uma aprovacao com solicitante, tipo de dado, escopo e SLA. Se aprovado, a equipe executa a resposta de dados; se recusado ou vencido, o caso fica pendente para o responsavel de privacidade.

**Limite Do Agente**

Nao executa pedido de privacidade; monta aprovacao e caso para humano autorizado.

**Humano/Aprovacao/Fallback**

- Chama humano quando: identidade nao esta confirmada; pedido envolve exclusao ou exportacao ampla; ha menor ou responsavel envolvido; dado solicitado nao esta no escopo permitido; aprovacao vence ou permissao bloqueia.
- Pede aprovacao quando: No cenario principal, antes da acao principal.
- Fallback do teste: Se o teste cair em `Aprovacao vence`, Mantem caso pendente.

**Agente De Configuracao**

Neste teste, a Taliya monta a aprovacao de Privacidade/dados e nao aplica a mudanca sozinha. Se aparecer `Identidade nao confirmada` ou `Pedido amplo de exclusao`, o caso fica com a equipe.

#### Telefone compartilhado e identidade

- ID interno: `A9`.
- Modo padrao: `Autonomo com aprovacao`.
- Visual central: `Pedido de aprovacao`.
- Usa celular: `nao`.

**Cenarios**

- `Telefone compartilhado detectado`: Monta aprovacao de validacao.
- `Mais de um aluno possivel`: Nao expoe dados.
- `Responsavel diverge`: Chama responsavel de revisao.
- `Permissao bloqueia`: Mantem atendimento com humano.

**Visual Do Caso**

card de aprovacao com dados, impacto, decisao pendente e efeito se aprovado

**Execucao Do Teste**

1. Inicio: O fluxo comeca quando o mesmo telefone pode representar mais de um aluno, responsavel ou cadastro.
2. Checagens: telefone compartilhado foi detectado; alunos possiveis foram listados; regra de validacao esta definida; responsavel de revisao esta definido; nenhum dado sensivel sera revelado antes da validacao.
3. Decisao: No cenario `Telefone compartilhado detectado`, a Taliya nao aplica sozinha: monta um pedido de aprovacao para humano autorizado.
4. Pedido de aprovacao: Monta a aprovacao para validar identidade em telefone compartilhado, mostrando telefone compartilhado foi detectado; alunos possiveis foram listados; regra de validacao esta definida; responsavel de revisao esta definido.
5. Fim: O telefone compartilhado fica marcado e nenhum dado sensivel e exposto antes da validacao. Se a validacao nao separar claramente aluno, responsavel e permissao, o atendimento fica com humano.

**Limite Do Agente**

Nao revela dado antes de validar quem esta usando o telefone compartilhado.

**Humano/Aprovacao/Fallback**

- Chama humano quando: mais de um aluno pode ser o solicitante; validacao falha; responsavel diverge do cadastro; pedido tenta acessar historico privado; aprovacao vence ou permissao bloqueia.
- Pede aprovacao quando: No cenario principal, antes da acao principal.
- Fallback do teste: Se o teste cair em `Permissao bloqueia`, Mantem atendimento com humano.

**Agente De Configuracao**

Neste teste, a Taliya monta a aprovacao de Telefone compartilhado e identidade e nao aplica a mudanca sozinha. Se aparecer `Mais de um aluno possivel` ou `Responsavel diverge`, o caso fica com a equipe.


### Rotina: Conversas e triagem

#### Ciclo de vida/SLA

- ID interno: `A10`.
- Modo padrao: `Autonomo`.
- Visual central: `Celular/conversa`.
- Usa celular: `sim`.

**Cenarios**

- `SLA dentro do prazo`: Atualiza status e prioridade.
- `SLA vencido`: Cria alerta em Hoje/Tarefas.
- `Conversa sem dono`: Encaminha para fila humana.
- `Fila indisponivel`: Cria pendencia operacional.

**Visual Do Caso**

celular com conversa simulada e cartao interno mostrando o resultado do fluxo

**Execucao Do Teste**

1. Inicio: O fluxo comeca quando uma conversa, fila ou atendimento precisa ser acompanhado por prazo, dono e status.
2. Checagens: conversa tem status claro; tempo de SLA esta definido; fila destino existe; prioridade foi definida; alerta ainda esta dentro da politica do studio.
3. Decisao: No cenario `SLA dentro do prazo`, a Taliya conclui sem equipe porque as checagens obrigatorias passam.
4. Acao: Conclui a acao permitida: acompanhar SLA e ciclo de vida do atendimento.
5. Fim: A conversa recebe status, dono, prazo e alerta de SLA. Se o SLA vencer, ficar sem dono ou virar assunto sensivel, aparece em Hoje/Tarefas para continuidade humana.

**Limite Do Agente**

Nao resolve atendimento; controla SLA, dono, status e alerta.

**Humano/Aprovacao/Fallback**

- Chama humano quando: Nao chama humano no cenario principal; se cair em `Fila indisponivel`, aplica fallback: Cria pendencia operacional.
- Pede aprovacao quando: Nao pede aprovacao no cenario principal; se houver bloqueio, aplica o fallback definido.
- Fallback do teste: Se o teste cair em `Fila indisponivel`, Cria pendencia operacional.

**Agente De Configuracao**

Neste teste, a Taliya conclui Ciclo de vida/SLA quando as checagens passam. Se aparecer `Fila indisponivel`, ela para e cria pendencia.


## Agente: Agenda


### Rotina: Presenca e faltas

#### Confirmacao de presenca

- ID interno: `B1`.
- Modo padrao: `Autonomo`.
- Visual central: `Celular/conversa`.
- Usa celular: `sim`.

**Cenarios**

- `Confirmacao no horario`: Envia confirmacao e registra resposta.
- `Aula alterada`: Para antes de enviar.
- `Resposta conflitante`: Cria pendencia na aula.
- `WhatsApp bloqueia`: Nao envia e cria pendencia.

**Visual Do Caso**

celular com conversa simulada e cartao interno mostrando o resultado do fluxo

**Execucao Do Teste**

1. Inicio: O fluxo comeca quando chega o horario de confirmar presenca de alunos em uma aula publicada.
2. Checagens: aula existe na agenda; aluno esta vinculado a aula; horario do lembrete chegou; template aprovado esta disponivel; limite por aula nao foi atingido.
3. Decisao: No cenario `Confirmacao no horario`, a Taliya conclui sem equipe porque as checagens obrigatorias passam.
4. Acao: Conclui a acao permitida: enviar confirmacao de presenca e registrar resposta.
5. Fim: A confirmacao e enviada, a resposta do aluno atualiza a aula e quem nao respondeu fica visivel para acompanhamento. Se aula, aluno, resposta ou envio tiver conflito, a pendencia fica na aula.

**Limite Do Agente**

Nao altera aula; apenas envia confirmacao permitida e registra resposta.

**Humano/Aprovacao/Fallback**

- Chama humano quando: Nao chama humano no cenario principal; se cair em `WhatsApp bloqueia`, aplica fallback: Nao envia e cria pendencia.
- Pede aprovacao quando: Nao pede aprovacao no cenario principal; se houver bloqueio, aplica o fallback definido.
- Fallback do teste: Se o teste cair em `WhatsApp bloqueia`, Nao envia e cria pendencia.

**Agente De Configuracao**

Neste teste, a Taliya conclui Confirmacao de presenca quando as checagens passam. Se aparecer `WhatsApp bloqueia`, ela para e cria pendencia.

#### Falta com aviso

- ID interno: `B2`.
- Modo padrao: `Autonomo com excecoes`.
- Visual central: `Celular/conversa`.
- Usa celular: `sim`.

**Cenarios**

- `Aluno avisou no prazo`: Registra falta e cria tarefa de reposicao.
- `Aviso fora do prazo`: Chama equipe antes de registrar.
- `Aluno pede credito`: Chama equipe antes de decidir.
- `WhatsApp falha`: Para e cria pendencia.

**Visual Do Caso**

celular com conversa simulada e cartao interno mostrando o resultado do fluxo

**Execucao Do Teste**

1. Inicio: O fluxo comeca quando o aluno avisa que nao vai comparecer a uma aula.
2. Checagens: aluno foi identificado; aula existe na agenda; aviso chegou ate o prazo configurado; falta ainda nao foi registrada; mensagem usa template aprovado.
3. Decisao: No cenario `Aluno avisou no prazo`, a Taliya segue sem equipe porque nenhuma excecao foi encontrada.
4. Acao: Executa o caso valido: registrar falta avisada e encaminhar o proximo passo.
5. Fim: A falta avisada fica registrada na aula, a mensagem permitida e enviada e o caso abre a proxima tarefa de reposicao quando configurado. Se prazo, aluno, aula, credito ou envio nao fecharem, a equipe decide o proximo passo.

**Limite Do Agente**

Nao escolhe vaga, credito ou horario de reposicao neste fluxo.

**Humano/Aprovacao/Fallback**

- Chama humano quando: aviso chega fora do prazo; nao encontra aluno ou aula; falta ja foi registrada; aluno pede excecao, credito, cancelamento ou reclama; WhatsApp, cota ou permissao bloqueiam o envio.
- Pede aprovacao quando: Nao pede aprovacao no cenario principal; nas excecoes, chama humano em vez de aprovar automaticamente.
- Fallback do teste: Se o teste cair em `WhatsApp falha`, Para e cria pendencia.

**Agente De Configuracao**

Neste teste, a Taliya executa Falta com aviso apenas no cenario valido. Se aparecer `Aviso fora do prazo` ou `Aluno pede credito`, chama a equipe.

#### Falta sem aviso

- ID interno: `B3`.
- Modo padrao: `Autonomo com excecoes`.
- Visual central: `Celular/conversa`.
- Usa celular: `sim`.

**Cenarios**

- `Aluno faltou sem avisar`: Marca ausencia e abre acompanhamento.
- `Chamada nao fechada`: Aguarda professor.
- `Aviso apareceu em outro canal`: Chama equipe para revisar.
- `Contato bloqueado`: Cria tarefa sem mensagem.

**Visual Do Caso**

celular com conversa simulada e cartao interno mostrando o resultado do fluxo

**Execucao Do Teste**

1. Inicio: O fluxo comeca quando a aula termina e um aluno previsto nao apareceu nem avisou antes.
2. Checagens: aula terminou; aluno estava previsto na chamada; presenca nao foi registrada; janela de tolerancia passou; responsavel de acompanhamento esta definido.
3. Decisao: No cenario `Aluno faltou sem avisar`, a Taliya segue sem equipe porque nenhuma excecao foi encontrada.
4. Acao: Executa o caso valido: detectar falta sem aviso e abrir recuperacao ou tarefa.
5. Fim: A ausencia sem aviso fica marcada depois da janela de tolerancia e abre acompanhamento de recuperacao ou retencao. Se a chamada do professor, aviso paralelo ou historico do aluno nao baterem, a equipe revisa antes de contato.

**Limite Do Agente**

Nao define retencao complexa; marca ausencia e abre acompanhamento.

**Humano/Aprovacao/Fallback**

- Chama humano quando: professor ainda nao fechou chamada; aluno avisou por outro canal; ha conflito de presenca; caso tem recorrencia ou risco de cancelamento; canal, cota ou permissao bloqueia contato.
- Pede aprovacao quando: Nao pede aprovacao no cenario principal; nas excecoes, chama humano em vez de aprovar automaticamente.
- Fallback do teste: Se o teste cair em `Contato bloqueado`, Cria tarefa sem mensagem.

**Agente De Configuracao**

Neste teste, a Taliya executa Falta sem aviso apenas no cenario valido. Se aparecer `Chamada nao fechada` ou `Aviso apareceu em outro canal`, chama a equipe.


### Rotina: Vagas, reposicoes e lista de espera

#### Recuperar vaga aberta

- ID interno: `B4`.
- Modo padrao: `Autonomo com excecoes`.
- Visual central: `Celular/conversa`.
- Usa celular: `sim`.

**Cenarios**

- `Vaga abriu com candidato claro`: Convida aluno elegivel.
- `Empate na prioridade`: Chama equipe.
- `Credito duvidoso`: Nao envia convite.
- `Canal falha`: Para e cria pendencia.

**Visual Do Caso**

celular com conversa simulada e cartao interno mostrando o resultado do fluxo

**Execucao Do Teste**

1. Inicio: O fluxo comeca quando uma vaga abre em uma aula e pode ser oferecida a alguem elegivel.
2. Checagens: vaga abriu em aula real; prioridade da lista esta definida; aluno elegivel tem credito ou direito; limite de convites nao foi atingido; convite usa mensagem aprovada.
3. Decisao: No cenario `Vaga abriu com candidato claro`, a Taliya segue sem equipe porque nenhuma excecao foi encontrada.
4. Acao: Executa o caso valido: usar vaga aberta para convidar aluno elegivel.
5. Fim: A vaga aberta gera convite para o aluno elegivel conforme prioridade e limite de convites. Se houver empate, lote grande, credito duvidoso ou risco de furar fila, a oferta fica parada para decisao.

**Limite Do Agente**

Nao consome credito nem altera prioridade quando houver empate.

**Humano/Aprovacao/Fallback**

- Chama humano quando: vaga fecha antes da resposta; ha empate ou lote grande; aluno nao tem credito claro; convite pode furar prioridade; canal, cota ou permissao bloqueia envio.
- Pede aprovacao quando: Nao pede aprovacao no cenario principal; nas excecoes, chama humano em vez de aprovar automaticamente.
- Fallback do teste: Se o teste cair em `Canal falha`, Para e cria pendencia.

**Agente De Configuracao**

Neste teste, a Taliya executa Recuperar vaga aberta apenas no cenario valido. Se aparecer `Empate na prioridade` ou `Credito duvidoso`, chama a equipe.

#### Reposicao/remarcacao

- ID interno: `B5`.
- Modo padrao: `Autonomo com aprovacao`.
- Visual central: `Pedido de aprovacao`.
- Usa celular: `nao`.

**Cenarios**

- `Reposicao dentro da politica`: Monta aprovacao de remarcacao.
- `Credito vencido`: Cria pendencia.
- `Aula destino lotada`: Nao propoe remarcacao.
- `Aprovacao vence`: Mantem solicitacao pendente.

**Visual Do Caso**

card de aprovacao com dados, impacto, decisao pendente e efeito se aprovado

**Execucao Do Teste**

1. Inicio: O fluxo comeca quando um aluno precisa repor ou remarcar uma aula dentro das regras do studio.
2. Checagens: credito de reposicao existe; aula de destino tem capacidade; prazo da politica esta valido; impacto na agenda foi calculado; aprovador esta definido.
3. Decisao: No cenario `Reposicao dentro da politica`, a Taliya nao aplica sozinha: monta um pedido de aprovacao para humano autorizado.
4. Pedido de aprovacao: Monta a aprovacao para aprovar reposicao ou remarcacao, mostrando credito de reposicao existe; aula de destino tem capacidade; prazo da politica esta valido; impacto na agenda foi calculado.
5. Fim: A reposicao ou remarcacao vira pedido de aprovacao com credito, vaga, prazo e impacto na agenda. Se aprovado, a agenda muda; se recusado ou vencido, a solicitacao fica como tarefa em reposicoes.

**Limite Do Agente**

Nao muda agenda antes da aprovacao.

**Humano/Aprovacao/Fallback**

- Chama humano quando: credito esta vencido ou contestado; aula destino esta lotada; mudanca afeta financeiro ou plano; ha conflito de horario; aprovacao vence ou permissao bloqueia.
- Pede aprovacao quando: No cenario principal, antes da acao principal.
- Fallback do teste: Se o teste cair em `Aprovacao vence`, Mantem solicitacao pendente.

**Agente De Configuracao**

Neste teste, a Taliya monta a aprovacao de Reposicao/remarcacao e nao aplica a mudanca sozinha. Se aparecer `Credito vencido` ou `Aula destino lotada`, o caso fica com a equipe.

#### Lista de espera

- ID interno: `B6`.
- Modo padrao: `Autonomo com excecoes`.
- Visual central: `Celular/conversa`.
- Usa celular: `sim`.

**Cenarios**

- `Vaga compativel apareceu`: Envia convite da lista de espera.
- `Aluno nao responde`: Atualiza prazo e proximo candidato.
- `Prioridade empata`: Chama equipe.
- `Envio bloqueado`: Para e cria pendencia.

**Visual Do Caso**

celular com conversa simulada e cartao interno mostrando o resultado do fluxo

**Execucao Do Teste**

1. Inicio: O fluxo comeca quando existe lista de espera e uma vaga compativel pode ser distribuida.
2. Checagens: lista de espera existe; prioridade foi calculada; vaga compativel apareceu; limite de convites permite contato; responsavel por excecao esta definido.
3. Decisao: No cenario `Vaga compativel apareceu`, a Taliya segue sem equipe porque nenhuma excecao foi encontrada.
4. Acao: Executa o caso valido: gerenciar lista de espera e convites.
5. Fim: A lista de espera recebe convite para a vaga compativel e o status do aluno muda conforme resposta ou prazo. Se prioridade, vaga, credito ou envio nao fecharem, a equipe assume a distribuicao.

**Limite Do Agente**

Nao fura prioridade nem confirma vaga sem resposta valida.

**Humano/Aprovacao/Fallback**

- Chama humano quando: prioridade empata; aluno nao responde no prazo; vaga deixa de existir; pedido envolve excecao de credito; canal, cota ou permissao bloqueia envio.
- Pede aprovacao quando: Nao pede aprovacao no cenario principal; nas excecoes, chama humano em vez de aprovar automaticamente.
- Fallback do teste: Se o teste cair em `Envio bloqueado`, Para e cria pendencia.

**Agente De Configuracao**

Neste teste, a Taliya executa Lista de espera apenas no cenario valido. Se aparecer `Aluno nao responde` ou `Prioridade empata`, chama a equipe.


### Rotina: Agenda experimental

#### Disponibilidade experimental

- ID interno: `B7`.
- Modo padrao: `Autonomo com excecoes`.
- Visual central: `Celular/conversa`.
- Usa celular: `sim`.

**Cenarios**

- `Horario experimental disponivel`: Oferece horarios reais ao lead.
- `Nao ha vaga`: Cria tarefa comercial.
- `Lead pede horario fora da regra`: Chama comercial.
- `Canal bloqueia`: Nao envia disponibilidade.

**Visual Do Caso**

celular com conversa simulada e cartao interno mostrando o resultado do fluxo

**Execucao Do Teste**

1. Inicio: O fluxo comeca quando um interessado precisa receber horarios possiveis para aula experimental.
2. Checagens: interessado esta identificado; horarios oferecidos estao livres; responsavel comercial esta definido; limite de tentativas nao foi atingido; mensagem aprovada esta disponivel.
3. Decisao: No cenario `Horario experimental disponivel`, a Taliya segue sem equipe porque nenhuma excecao foi encontrada.
4. Acao: Executa o caso valido: oferecer disponibilidade para aula experimental.
5. Fim: O interessado recebe horarios de experimental que existem de verdade e a resposta segue para agendamento comercial. Se nao houver vaga, houver experimental duplicada ou pedido especial, o comercial recebe tarefa.

**Limite Do Agente**

Nao promete vaga experimental indisponivel.

**Humano/Aprovacao/Fallback**

- Chama humano quando: interessado pede horario fora da regra; nao ha vaga compativel; lead ja tem experimental marcada; pedido envolve desconto ou excecao; canal, cota ou permissao bloqueia envio.
- Pede aprovacao quando: Nao pede aprovacao no cenario principal; nas excecoes, chama humano em vez de aprovar automaticamente.
- Fallback do teste: Se o teste cair em `Canal bloqueia`, Nao envia disponibilidade.

**Agente De Configuracao**

Neste teste, a Taliya executa Disponibilidade experimental apenas no cenario valido. Se aparecer `Nao ha vaga` ou `Lead pede horario fora da regra`, chama a equipe.


### Rotina: Grade e capacidade

#### Mudanca horario fixo

- ID interno: `B8`.
- Modo padrao: `Autonomo com aprovacao`.
- Visual central: `Pedido de aprovacao`.
- Usa celular: `nao`.

**Cenarios**

- `Novo horario disponivel`: Monta aprovacao de horario fixo.
- `Novo horario conflita`: Nao aplica mudanca.
- `Impacta varios alunos`: Pede decisao.
- `Aprovacao vence`: Mantem pedido pendente.

**Visual Do Caso**

card de aprovacao com dados, impacto, decisao pendente e efeito se aprovado

**Execucao Do Teste**

1. Inicio: O fluxo comeca quando um aluno pede ou precisa mudar seu horario fixo.
2. Checagens: aluno e horario fixo foram identificados; novo horario existe; impacto em turma e capacidade foi calculado; mensagem de confirmacao esta pronta; aprovador esta definido.
3. Decisao: No cenario `Novo horario disponivel`, a Taliya nao aplica sozinha: monta um pedido de aprovacao para humano autorizado.
4. Pedido de aprovacao: Monta a aprovacao para aprovar mudanca de horario fixo, mostrando aluno e horario fixo foram identificados; novo horario existe; impacto em turma e capacidade foi calculado; mensagem de confirmacao esta pronta.
5. Fim: A mudanca de horario fixo vira aprovacao com novo horario, impacto em capacidade e mensagem de confirmacao. Se aprovada, o cadastro do aluno e a grade sao atualizados; se nao, fica tarefa para ajuste humano.

**Limite Do Agente**

Nao troca horario fixo sem aprovacao.

**Humano/Aprovacao/Fallback**

- Chama humano quando: novo horario gera conflito; aluno tem pendencia financeira ou credito afetado; mudanca impacta varios alunos; prazo minimo nao foi cumprido; aprovacao vence ou permissao bloqueia.
- Pede aprovacao quando: No cenario principal, antes da acao principal.
- Fallback do teste: Se o teste cair em `Aprovacao vence`, Mantem pedido pendente.

**Agente De Configuracao**

Neste teste, a Taliya monta a aprovacao de Mudanca horario fixo e nao aplica a mudanca sozinha. Se aparecer `Novo horario conflita` ou `Impacta varios alunos`, o caso fica com a equipe.

#### Cancelamento pelo studio

- ID interno: `B9`.
- Modo padrao: `Autonomo com aprovacao`.
- Visual central: `Pedido de aprovacao`.
- Usa celular: `nao`.

**Cenarios**

- `Studio cancela aula simples`: Monta aprovacao e comunicado.
- `Muitos alunos afetados`: Exige decisao.
- `Credito/reposicao incerto`: Nao comunica sozinho.
- `Aprovacao vence`: Aula segue sem cancelamento automatico.

**Visual Do Caso**

card de aprovacao com dados, impacto, decisao pendente e efeito se aprovado

**Execucao Do Teste**

1. Inicio: O fluxo comeca quando o studio precisa cancelar uma aula e comunicar os alunos afetados.
2. Checagens: aula a cancelar existe; motivo foi informado; alunos afetados foram listados; reposicao ou credito foi calculado; aprovador esta definido.
3. Decisao: No cenario `Studio cancela aula simples`, a Taliya nao aplica sozinha: monta um pedido de aprovacao para humano autorizado.
4. Pedido de aprovacao: Monta a aprovacao para aprovar cancelamento pelo studio e comunicado, mostrando aula a cancelar existe; motivo foi informado; alunos afetados foram listados; reposicao ou credito foi calculado.
5. Fim: O cancelamento pelo studio vira aprovacao com aula, motivo, alunos afetados e comunicado. Se aprovado, alunos recebem orientacao e reposicao/credito; se nao, a aula permanece sem alteracao automatica.

**Limite Do Agente**

Nao cancela aula nem comunica alunos sem aprovacao.

**Humano/Aprovacao/Fallback**

- Chama humano quando: cancelamento afeta muitos alunos; ha aluno de primeira aula ou experimental; reposicao ou credito nao esta claro; comunicado nao cobre o caso; aprovacao vence ou permissao bloqueia.
- Pede aprovacao quando: No cenario principal, antes da acao principal.
- Fallback do teste: Se o teste cair em `Aprovacao vence`, Aula segue sem cancelamento automatico.

**Agente De Configuracao**

Neste teste, a Taliya monta a aprovacao de Cancelamento pelo studio e nao aplica a mudanca sozinha. Se aparecer `Muitos alunos afetados` ou `Credito/reposicao incerto`, o caso fica com a equipe.

#### Conflito capacidade

- ID interno: `B10`.
- Modo padrao: `Autonomo com aprovacao`.
- Visual central: `Pedido de aprovacao`.
- Usa celular: `nao`.

**Cenarios**

- `Conflito de lotacao claro`: Monta aprovacao de correcao.
- `Capacidade diverge`: Pede revisao.
- `Solucao remove aluno`: Exige aprovacao.
- `Permissao bloqueia`: Mantem conflito aberto.

**Visual Do Caso**

card de aprovacao com dados, impacto, decisao pendente e efeito se aprovado

**Execucao Do Teste**

1. Inicio: O fluxo comeca quando a agenda encontra conflito de capacidade, lotacao ou direito de vaga.
2. Checagens: turma ou aula foi identificada; capacidade publicada existe; conflito foi calculado; prioridade do caso foi definida; aprovador esta definido.
3. Decisao: No cenario `Conflito de lotacao claro`, a Taliya nao aplica sozinha: monta um pedido de aprovacao para humano autorizado.
4. Pedido de aprovacao: Monta a aprovacao para aprovar correcao de capacidade, mostrando turma ou aula foi identificada; capacidade publicada existe; conflito foi calculado; prioridade do caso foi definida.
5. Fim: O conflito de capacidade vira aprovacao com quem foi afetado, prioridade e alternativa proposta. Se aprovado, a correcao ajusta vaga/turma; se nao, o conflito fica aberto para coordenacao.

**Limite Do Agente**

Nao remove aluno nem altera capacidade sem aprovacao.

**Humano/Aprovacao/Fallback**

- Chama humano quando: capacidade real diverge da configurada; ha conflito entre alunos com direito similar; mudanca afeta grade ou professor; solucao exige remover aluno; aprovacao vence ou permissao bloqueia.
- Pede aprovacao quando: No cenario principal, antes da acao principal.
- Fallback do teste: Se o teste cair em `Permissao bloqueia`, Mantem conflito aberto.

**Agente De Configuracao**

Neste teste, a Taliya monta a aprovacao de Conflito capacidade e nao aplica a mudanca sozinha. Se aparecer `Capacidade diverge` ou `Solucao remove aluno`, o caso fica com a equipe.

#### Ajuste de grade

- ID interno: `B11`.
- Modo padrao: `Autonomo com aprovacao`.
- Visual central: `Pedido de aprovacao`.
- Usa celular: `nao`.

**Cenarios**

- `Mudanca de grade simulada`: Monta aprovacao de impacto.
- `Simulacao encontra conflito`: Volta para revisao.
- `Vigencia curta demais`: Nao publica mudanca.
- `Aprovacao vence`: Mantem grade atual.

**Visual Do Caso**

card de aprovacao com dados, impacto, decisao pendente e efeito se aprovado

**Execucao Do Teste**

1. Inicio: O fluxo comeca quando o studio quer alterar grade, horarios, professores ou vigencia da agenda.
2. Checagens: mudanca de grade foi descrita; data de vigencia esta definida; impacto em aulas, alunos e professores foi simulado; comunicacao necessaria foi listada; aprovador esta definido.
3. Decisao: No cenario `Mudanca de grade simulada`, a Taliya nao aplica sozinha: monta um pedido de aprovacao para humano autorizado.
4. Pedido de aprovacao: Monta a aprovacao para aprovar ajuste de grade, mostrando mudanca de grade foi descrita; data de vigencia esta definida; impacto em aulas, alunos e professores foi simulado; comunicacao necessaria foi listada.
5. Fim: O ajuste de grade vira simulacao aprovada com vigencia, aulas, alunos, professores e comunicacao. Se aprovado, a grade muda na data definida; se houver conflito, a simulacao volta para revisao.

**Limite Do Agente**

Nao publica grade sem aprovacao.

**Humano/Aprovacao/Fallback**

- Chama humano quando: simulacao encontra conflito; impacto financeiro ou contratual aparece; data de vigencia e curta demais; alunos afetados nao foram resolvidos; aprovacao vence ou permissao bloqueia.
- Pede aprovacao quando: No cenario principal, antes da acao principal.
- Fallback do teste: Se o teste cair em `Aprovacao vence`, Mantem grade atual.

**Agente De Configuracao**

Neste teste, a Taliya monta a aprovacao de Ajuste de grade e nao aplica a mudanca sozinha. Se aparecer `Simulacao encontra conflito` ou `Vigencia curta demais`, o caso fica com a equipe.


### Rotina: Agenda experimental

#### Experimental sem comparecimento

- ID interno: `B12`.
- Modo padrao: `Autonomo com excecoes`.
- Visual central: `Celular/conversa`.
- Usa celular: `sim`.

**Cenarios**

- `Lead faltou experimental`: Abre follow-up ou remarcacao.
- `Lead avisou por outro canal`: Chama comercial.
- `Nao ha nova vaga`: Cria tarefa comercial.
- `Canal bloqueia`: Nao envia contato.

**Visual Do Caso**

celular com conversa simulada e cartao interno mostrando o resultado do fluxo

**Execucao Do Teste**

1. Inicio: O fluxo comeca quando um lead marcado para aula experimental nao comparece.
2. Checagens: experimental estava marcada; lead nao compareceu; janela de tolerancia passou; cadencia comercial esta definida; limite de contato nao foi atingido.
3. Decisao: No cenario `Lead faltou experimental`, a Taliya segue sem equipe porque nenhuma excecao foi encontrada.
4. Acao: Executa o caso valido: tratar experimental sem comparecimento.
5. Fim: O nao comparecimento ao experimental abre follow-up comercial ou remarcacao dentro da cadencia. Se o lead avisou por outro canal, pediu excecao ou nao ha vaga, o comercial decide a abordagem.

**Limite Do Agente**

Nao decide desconto, remarcacao especial ou condicao comercial fora da politica.

**Humano/Aprovacao/Fallback**

- Chama humano quando: lead avisou por outro canal; lead pede remarcacao fora da regra; nao ha nova vaga compativel; lead demonstra objecao sensivel; canal, cota ou permissao bloqueia contato.
- Pede aprovacao quando: Nao pede aprovacao no cenario principal; nas excecoes, chama humano em vez de aprovar automaticamente.
- Fallback do teste: Se o teste cair em `Canal bloqueia`, Nao envia contato.

**Agente De Configuracao**

Neste teste, a Taliya executa Experimental sem comparecimento apenas no cenario valido. Se aparecer `Lead avisou por outro canal` ou `Nao ha nova vaga`, chama a equipe.


### Rotina: Vagas, reposicoes e lista de espera

#### Creditos reposicao

- ID interno: `B13`.
- Modo padrao: `Autonomo com aprovacao`.
- Visual central: `Pedido de aprovacao`.
- Usa celular: `nao`.

**Cenarios**

- `Credito valido proposto`: Monta aprovacao de credito.
- `Credito contestado`: Chama responsavel.
- `Duplicidade de credito`: Bloqueia criacao.
- `Aprovacao vence`: Mantem credito pendente.

**Visual Do Caso**

card de aprovacao com dados, impacto, decisao pendente e efeito se aprovado

**Execucao Do Teste**

1. Inicio: O fluxo comeca quando uma falta, remarcacao ou decisao operacional pode gerar credito de reposicao.
2. Checagens: falta ou remarcacao geradora foi identificada; validade proposta esta definida; politica de credito esta publicada; destino de excecoes esta definido; aprovador esta definido.
3. Decisao: No cenario `Credito valido proposto`, a Taliya nao aplica sozinha: monta um pedido de aprovacao para humano autorizado.
4. Pedido de aprovacao: Monta a aprovacao para aprovar credito de reposicao, mostrando falta ou remarcacao geradora foi identificada; validade proposta esta definida; politica de credito esta publicada; destino de excecoes esta definido.
5. Fim: O credito de reposicao vira aprovacao com origem, validade e politica aplicada. Se aprovado, o credito aparece para uso em reposicao; se contestado ou duplicado, fica com o responsavel.

**Limite Do Agente**

Nao cria credito antes da aprovacao.

**Humano/Aprovacao/Fallback**

- Chama humano quando: credito e contestado; validade foge da politica; credito afeta plano ou financeiro; ha duplicidade de credito; aprovacao vence ou permissao bloqueia.
- Pede aprovacao quando: No cenario principal, antes da acao principal.
- Fallback do teste: Se o teste cair em `Aprovacao vence`, Mantem credito pendente.

**Agente De Configuracao**

Neste teste, a Taliya monta a aprovacao de Creditos reposicao e nao aplica a mudanca sozinha. Se aparecer `Credito contestado` ou `Duplicidade de credito`, o caso fica com a equipe.


### Rotina: Presenca e faltas

#### Correcao presenca

- ID interno: `B14`.
- Modo padrao: `Autonomo com aprovacao`.
- Visual central: `Pedido de aprovacao`.
- Usa celular: `nao`.

**Cenarios**

- `Correcao com motivo claro`: Monta aprovacao de presenca.
- `Motivo ausente`: Pede complemento.
- `Impacta credito/financeiro`: Chama equipe.
- `Aprovacao vence`: Nao altera chamada.

**Visual Do Caso**

card de aprovacao com dados, impacto, decisao pendente e efeito se aprovado

**Execucao Do Teste**

1. Inicio: O fluxo comeca quando alguem pede para corrigir uma presenca ja registrada.
2. Checagens: aula e aluno foram identificados; correcao solicitada tem motivo; historico atual foi preservado; impacto da alteracao foi mostrado; aprovador esta definido.
3. Decisao: No cenario `Correcao com motivo claro`, a Taliya nao aplica sozinha: monta um pedido de aprovacao para humano autorizado.
4. Pedido de aprovacao: Monta a aprovacao para aprovar correcao de presenca, mostrando aula e aluno foram identificados; correcao solicitada tem motivo; historico atual foi preservado; impacto da alteracao foi mostrado.
5. Fim: A correcao de presenca vira aprovacao com aula, aluno, motivo e impacto. Se aprovada, a chamada e atualizada preservando historico anterior; se houver impacto em credito/financeiro, fica pendente.

**Limite Do Agente**

Nao altera historico de presenca antes da aprovacao.

**Humano/Aprovacao/Fallback**

- Chama humano quando: motivo nao foi informado; correcao altera historico sensivel; ha conflito com professor ou aluno; impacto em credito ou financeiro aparece; aprovacao vence ou permissao bloqueia.
- Pede aprovacao quando: No cenario principal, antes da acao principal.
- Fallback do teste: Se o teste cair em `Aprovacao vence`, Nao altera chamada.

**Agente De Configuracao**

Neste teste, a Taliya monta a aprovacao de Correcao presenca e nao aplica a mudanca sozinha. Se aparecer `Motivo ausente` ou `Impacta credito/financeiro`, o caso fica com a equipe.


### Rotina: Primeira aula e aulas especiais

#### Primeira aula

- ID interno: `B15`.
- Modo padrao: `Autonomo com excecoes`.
- Visual central: `Celular/conversa`.
- Usa celular: `sim`.

**Cenarios**

- `Primeira aula proxima`: Envia orientacao e checklist.
- `Cuidado pendente`: Chama equipe antes de contato.
- `Professor indefinido`: Cria tarefa.
- `Canal bloqueia`: Nao envia orientacao.

**Visual Do Caso**

celular com conversa simulada e cartao interno mostrando o resultado do fluxo

**Execucao Do Teste**

1. Inicio: O fluxo comeca quando um aluno esta perto da primeira aula e precisa de acompanhamento inicial.
2. Checagens: aluno tem primeira aula identificada; checklist esta definido; professor ou responsavel esta atribuido; orientacoes foram preparadas; nao ha restricao sensivel pendente.
3. Decisao: No cenario `Primeira aula proxima`, a Taliya segue sem equipe porque nenhuma excecao foi encontrada.
4. Acao: Executa o caso valido: acompanhar primeira aula e checklist inicial.
5. Fim: A primeira aula recebe checklist, orientacao e responsavel definidos. Se houver cuidado, restricao, troca de aula ou professor indefinido, a equipe recebe tarefa antes do contato.

**Limite Do Agente**

Nao envia orientacao se houver cuidado, restricao ou professor indefinido.

**Humano/Aprovacao/Fallback**

- Chama humano quando: aluno tem cuidado sem revisao; professor nao esta definido; aula muda de horario; aluno pede remarcacao ou excecao; canal, cota ou permissao bloqueia contato.
- Pede aprovacao quando: Nao pede aprovacao no cenario principal; nas excecoes, chama humano em vez de aprovar automaticamente.
- Fallback do teste: Se o teste cair em `Canal bloqueia`, Nao envia orientacao.

**Agente De Configuracao**

Neste teste, a Taliya executa Primeira aula apenas no cenario valido. Se aparecer `Cuidado pendente` ou `Professor indefinido`, chama a equipe.

#### Aula especial/workshop

- ID interno: `B16`.
- Modo padrao: `Autonomo com aprovacao`.
- Visual central: `Pedido de aprovacao`.
- Usa celular: `nao`.

**Cenarios**

- `Workshop simples`: Monta aprovacao do evento.
- `Conflito com grade regular`: Volta para revisao.
- `Preco indefinido`: Nao publica evento.
- `Aprovacao vence`: Mantem evento em rascunho.

**Visual Do Caso**

card de aprovacao com dados, impacto, decisao pendente e efeito se aprovado

**Execucao Do Teste**

1. Inicio: O fluxo comeca quando o studio cria ou altera uma aula especial, workshop ou evento.
2. Checagens: evento foi descrito; capacidade esta definida; prazo e data estao claros; template de comunicacao esta pronto; aprovador esta definido.
3. Decisao: No cenario `Workshop simples`, a Taliya nao aplica sozinha: monta um pedido de aprovacao para humano autorizado.
4. Pedido de aprovacao: Monta a aprovacao para aprovar aula especial ou workshop, mostrando evento foi descrito; capacidade esta definida; prazo e data estao claros; template de comunicacao esta pronto.
5. Fim: A aula especial ou workshop vira aprovacao com data, capacidade, regra de inscricao e comunicacao. Se aprovado, o evento entra na agenda; se conflitar com grade, preco ou beneficio, fica em revisao.

**Limite Do Agente**

Nao publica evento/workshop antes da aprovacao.

**Humano/Aprovacao/Fallback**

- Chama humano quando: capacidade e regra de inscricao conflitam; evento afeta grade regular; preco ou beneficio nao esta definido; comunicacao impacta muitos alunos; aprovacao vence ou permissao bloqueia.
- Pede aprovacao quando: No cenario principal, antes da acao principal.
- Fallback do teste: Se o teste cair em `Aprovacao vence`, Mantem evento em rascunho.

**Agente De Configuracao**

Neste teste, a Taliya monta a aprovacao de Aula especial/workshop e nao aplica a mudanca sozinha. Se aparecer `Conflito com grade regular` ou `Preco indefinido`, o caso fica com a equipe.


## Agente: Vendas


### Rotina: Conversao e matricula

#### Valores e planos

- ID interno: `C1`.
- Modo padrao: `Autonomo com excecoes`.
- Visual central: `Celular/conversa`.
- Usa celular: `sim`.

**Cenarios**

- `Pergunta sobre plano aprovado`: Responde valores permitidos.
- `Lead pede desconto`: Chama comercial.
- `Pergunta mistura contrato`: Cria tarefa.
- `Cota bloqueia`: Nao envia resposta.

**Visual Do Caso**

celular com conversa simulada e cartao interno mostrando o resultado do fluxo

**Execucao Do Teste**

1. Inicio: O fluxo comeca quando lead ou aluno pergunta sobre valores, planos ou condicoes comerciais aprovadas.
2. Checagens: plano ou valor esta na base aprovada; lead ou aluno foi identificado quando necessario; nao ha pedido de desconto especial; resposta usa template permitido; limite de conversa nao foi atingido.
3. Decisao: No cenario `Pergunta sobre plano aprovado`, a Taliya segue sem equipe porque nenhuma excecao foi encontrada.
4. Acao: Executa o caso valido: responder sobre valores e planos aprovados.
5. Fim: O lead recebe valores e planos somente da base aprovada e a conversa fica pronta para proxima etapa comercial. Se pedir desconto, promessa ou condicao fora da base, o comercial assume.

**Limite Do Agente**

Nao negocia desconto ou condicao fora da base comercial aprovada.

**Humano/Aprovacao/Fallback**

- Chama humano quando: lead pede desconto, promessa ou excecao; plano nao esta claro; pergunta mistura financeiro e contrato; resposta pode gerar compromisso comercial; canal, cota ou permissao bloqueia resposta.
- Pede aprovacao quando: Nao pede aprovacao no cenario principal; nas excecoes, chama humano em vez de aprovar automaticamente.
- Fallback do teste: Se o teste cair em `Cota bloqueia`, Nao envia resposta.

**Agente De Configuracao**

Neste teste, a Taliya executa Valores e planos apenas no cenario valido. Se aparecer `Lead pede desconto` ou `Pergunta mistura contrato`, chama a equipe.


### Rotina: Experimental e acompanhamento

#### Aula experimental

- ID interno: `C2`.
- Modo padrao: `Autonomo com excecoes`.
- Visual central: `Celular/conversa`.
- Usa celular: `sim`.

**Cenarios**

- `Lead quer experimental`: Marca ou prepara aula experimental.
- `Horario indisponivel`: Oferece alternativa ou chama comercial.
- `Lead ja fez experimental`: Pede decisao.
- `Canal bloqueia`: Cria pendencia.

**Visual Do Caso**

celular com conversa simulada e cartao interno mostrando o resultado do fluxo

**Execucao Do Teste**

1. Inicio: O fluxo comeca quando um lead quer marcar uma aula experimental.
2. Checagens: lead esta identificado; horarios disponiveis existem; responsavel comercial esta definido; limite de tentativas permite contato; lead nao tem experimental duplicada.
3. Decisao: No cenario `Lead quer experimental`, a Taliya segue sem equipe porque nenhuma excecao foi encontrada.
4. Acao: Executa o caso valido: marcar ou preparar aula experimental.
5. Fim: A aula experimental e marcada ou preparada com horario real, responsavel e dados do lead. Se horario, vaga, duplicidade ou excecao comercial nao fecharem, vira tarefa para o comercial.

**Limite Do Agente**

Nao promete horario ou vaga indisponivel.

**Humano/Aprovacao/Fallback**

- Chama humano quando: lead pede horario indisponivel; nao ha vaga compativel; lead ja fez experimental recente; pedido envolve desconto ou excecao; canal, cota ou permissao bloqueia contato.
- Pede aprovacao quando: Nao pede aprovacao no cenario principal; nas excecoes, chama humano em vez de aprovar automaticamente.
- Fallback do teste: Se o teste cair em `Canal bloqueia`, Cria pendencia.

**Agente De Configuracao**

Neste teste, a Taliya executa Aula experimental apenas no cenario valido. Se aparecer `Horario indisponivel` ou `Lead ja fez experimental`, chama a equipe.

#### Lembrete experimental

- ID interno: `C3`.
- Modo padrao: `Autonomo`.
- Visual central: `Celular/conversa`.
- Usa celular: `sim`.

**Cenarios**

- `Lembrete no horario`: Envia lembrete do experimental.
- `Aula remarcada`: Para antes de enviar.
- `Lead pede mudanca`: Chama comercial.
- `Opt-out`: Nao envia.

**Visual Do Caso**

celular com conversa simulada e cartao interno mostrando o resultado do fluxo

**Execucao Do Teste**

1. Inicio: O fluxo comeca quando chega o horario de lembrar um lead sobre a aula experimental marcada.
2. Checagens: experimental esta marcada; horario do lembrete chegou; lead tem canal permitido; template aprovado esta disponivel; lembrete ainda nao foi enviado.
3. Decisao: No cenario `Lembrete no horario`, a Taliya conclui sem equipe porque as checagens obrigatorias passam.
4. Acao: Conclui a acao permitida: enviar lembrete de aula experimental.
5. Fim: O lembrete do experimental e enviado uma vez no horario configurado e o status do lead mostra que foi lembrado. Se a aula mudou, o lead pediu opt-out ou respondeu com mudanca, o fluxo para.

**Limite Do Agente**

Nao remarca experimental; lembra, para ou chama comercial.

**Humano/Aprovacao/Fallback**

- Chama humano quando: Nao chama humano no cenario principal; se cair em `Opt-out`, aplica fallback: Nao envia.
- Pede aprovacao quando: Nao pede aprovacao no cenario principal; se houver bloqueio, aplica o fallback definido.
- Fallback do teste: Se o teste cair em `Opt-out`, Nao envia.

**Agente De Configuracao**

Neste teste, a Taliya conclui Lembrete experimental quando as checagens passam. Se aparecer `Opt-out`, ela para e cria pendencia.

#### Pos-aula experimental

- ID interno: `C4`.
- Modo padrao: `Autonomo com excecoes`.
- Visual central: `Celular/conversa`.
- Usa celular: `sim`.

**Cenarios**

- `Experimental concluida`: Inicia acompanhamento pos-aula.
- `Lead faltou`: Encaminha para fluxo de falta experimental.
- `Observacao sensivel`: Chama comercial.
- `Canal bloqueia`: Cria tarefa.

**Visual Do Caso**

celular com conversa simulada e cartao interno mostrando o resultado do fluxo

**Execucao Do Teste**

1. Inicio: O fluxo comeca depois que uma aula experimental acontece e o lead precisa de acompanhamento comercial.
2. Checagens: experimental foi concluida; presenca foi registrada; cadencia pos-aula esta definida; responsavel comercial esta atribuido; limite de contato nao foi atingido.
3. Decisao: No cenario `Experimental concluida`, a Taliya segue sem equipe porque nenhuma excecao foi encontrada.
4. Acao: Executa o caso valido: acompanhar lead depois da aula experimental.
5. Fim: Depois da experimental, o lead entra no acompanhamento comercial correto com presenca e proxima acao. Se houve falta, observacao sensivel, desconto ou reclamacao, o comercial decide.

**Limite Do Agente**

Nao decide venda, desconto ou condicao de matricula.

**Humano/Aprovacao/Fallback**

- Chama humano quando: lead nao compareceu; professor registrou observacao sensivel; lead pede desconto ou condicao especial; lead demonstra reclamacao; canal, cota ou permissao bloqueia contato.
- Pede aprovacao quando: Nao pede aprovacao no cenario principal; nas excecoes, chama humano em vez de aprovar automaticamente.
- Fallback do teste: Se o teste cair em `Canal bloqueia`, Cria tarefa.

**Agente De Configuracao**

Neste teste, a Taliya executa Pos-aula experimental apenas no cenario valido. Se aparecer `Lead faltou` ou `Observacao sensivel`, chama a equipe.

#### Follow-up comercial

- ID interno: `C5`.
- Modo padrao: `Autonomo com excecoes`.
- Visual central: `Celular/conversa`.
- Usa celular: `sim`.

**Cenarios**

- `Follow-up permitido`: Envia contato da cadencia.
- `Lead pediu parar`: Bloqueia contato.
- `Lead pede desconto`: Chama comercial.
- `Canal/cota bloqueia`: Para e registra pendencia.

**Visual Do Caso**

celular com conversa simulada e cartao interno mostrando o resultado do fluxo

**Execucao Do Teste**

1. Inicio: O fluxo comeca quando um lead entra em uma etapa de follow-up comercial permitida pela cadencia.
2. Checagens: lead esta em etapa elegivel; cadencia esta definida; ultima interacao permite novo contato; responsavel comercial esta definido; limite de tentativas nao foi atingido.
3. Decisao: No cenario `Follow-up permitido`, a Taliya segue sem equipe porque nenhuma excecao foi encontrada.
4. Acao: Executa o caso valido: conduzir follow-up comercial dentro da cadencia.
5. Fim: O follow-up e enviado dentro da cadencia e a etapa comercial avanca conforme resposta ou ausencia de resposta. Se o lead pediu humano, desconto, garantia ou parar contato, o fluxo para.

**Limite Do Agente**

Nao continua contato se o lead pediu parar ou trouxe assunto sensivel.

**Humano/Aprovacao/Fallback**

- Chama humano quando: lead pediu humano ou parar contato; lead tem objecao sensivel; lead pede desconto ou garantia; conversa esfriou alem do limite; canal, cota ou permissao bloqueia contato.
- Pede aprovacao quando: Nao pede aprovacao no cenario principal; nas excecoes, chama humano em vez de aprovar automaticamente.
- Fallback do teste: Se o teste cair em `Canal/cota bloqueia`, Para e registra pendencia.

**Agente De Configuracao**

Neste teste, a Taliya executa Follow-up comercial apenas no cenario valido. Se aparecer `Lead pediu parar` ou `Lead pede desconto`, chama a equipe.


### Rotina: Conversao e matricula

#### Pre-matricula

- ID interno: `C6`.
- Modo padrao: `Autonomo com aprovacao`.
- Visual central: `Pedido de aprovacao`.
- Usa celular: `nao`.

**Cenarios**

- `Lead aceitou pre-matricula`: Monta aprovacao de pre-matricula.
- `Dados obrigatorios faltam`: Pede complemento.
- `Desconto na proposta`: Exige aprovacao.
- `Aprovacao vence`: Mantem lead pendente.

**Visual Do Caso**

card de aprovacao com dados, impacto, decisao pendente e efeito se aprovado

**Execucao Do Teste**

1. Inicio: O fluxo comeca quando o lead aceita avancar para pre-matricula.
2. Checagens: lead aceitou avancar; checklist de matricula esta completo; plano escolhido esta definido; responsavel comercial esta atribuido; aprovador esta definido.
3. Decisao: No cenario `Lead aceitou pre-matricula`, a Taliya nao aplica sozinha: monta um pedido de aprovacao para humano autorizado.
4. Pedido de aprovacao: Monta a aprovacao para aprovar pre-matricula, mostrando lead aceitou avancar; checklist de matricula esta completo; plano escolhido esta definido; responsavel comercial esta atribuido.
5. Fim: A pre-matricula vira aprovacao com plano, checklist, dados e responsavel. Se aprovada, segue para matricula/contrato; se faltarem dados, valor ou documento, fica pendente.

**Limite Do Agente**

Nao cria matricula antes da aprovacao.

**Humano/Aprovacao/Fallback**

- Chama humano quando: dados obrigatorios faltam; plano ou valor diverge da proposta; ha desconto ou excecao; documento ou contrato nao esta pronto; aprovacao vence ou permissao bloqueia.
- Pede aprovacao quando: No cenario principal, antes da acao principal.
- Fallback do teste: Se o teste cair em `Aprovacao vence`, Mantem lead pendente.

**Agente De Configuracao**

Neste teste, a Taliya monta a aprovacao de Pre-matricula e nao aplica a mudanca sozinha. Se aparecer `Dados obrigatorios faltam` ou `Desconto na proposta`, o caso fica com a equipe.

#### Objecoes

- ID interno: `C7`.
- Modo padrao: `Autonomo com aprovacao`.
- Visual central: `Celular/conversa`.
- Usa celular: `sim`.

**Cenarios**

- `Objecao comum`: Monta resposta para aprovacao.
- `Pedido de garantia`: Nao responde sozinho.
- `Resposta fora da base`: Chama comercial.
- `Aprovacao vence`: Mantem objecao aberta.

**Visual Do Caso**

celular com conversa simulada e cartao interno mostrando o resultado do fluxo

**Execucao Do Teste**

1. Inicio: O fluxo comeca quando o lead traz uma objecao comercial que precisa de resposta cuidadosa.
2. Checagens: objecao foi classificada; base de respostas cobre o caso; limite de promessa esta definido; impacto comercial foi mostrado; aprovador esta definido.
3. Decisao: No cenario `Objecao comum`, a Taliya nao aplica sozinha: monta um pedido de aprovacao para humano autorizado.
4. Pedido de aprovacao: Monta a aprovacao para aprovar resposta para objecao comercial, mostrando objecao foi classificada; base de respostas cobre o caso; limite de promessa esta definido; impacto comercial foi mostrado.
5. Fim: A objecao comercial vira resposta revisada com limite de promessa e impacto. Se aprovada, a resposta vai para o lead; se envolver desconto, garantia ou promessa indevida, fica com humano.

**Limite Do Agente**

Nao promete desconto, garantia ou condicao fora da base.

**Humano/Aprovacao/Fallback**

- Chama humano quando: objecao envolve preco, desconto ou garantia; lead compara concorrente com promessa sensivel; resposta nao existe na base; risco de promessa indevida aparece; aprovacao vence ou permissao bloqueia.
- Pede aprovacao quando: No cenario principal, antes da acao principal.
- Fallback do teste: Se o teste cair em `Aprovacao vence`, Mantem objecao aberta.

**Agente De Configuracao**

Neste teste, a Taliya monta a aprovacao de Objecoes e nao aplica a mudanca sozinha. Se aparecer `Pedido de garantia` ou `Resposta fora da base`, o caso fica com a equipe.


### Rotina: Captura e qualificacao

#### Origem/qualificacao

- ID interno: `C8`.
- Modo padrao: `Autonomo com excecoes`.
- Visual central: `Ficha de lead`.
- Usa celular: `nao`.

**Cenarios**

- `Lead novo com origem clara`: Cria ficha qualificada.
- `Lead duplicado`: Cria revisao.
- `Origem desconhecida`: Pede classificacao.
- `Campos faltando`: Mantem ficha incompleta.

**Visual Do Caso**

ficha do lead com origem, campos minimos, duplicidade e dono comercial

**Execucao Do Teste**

1. Inicio: O fluxo comeca quando um lead precisa ser qualificado por origem, perfil e dados minimos.
2. Checagens: lead foi identificado; campos obrigatorios foram preenchidos; origem foi reconhecida; duplicidade foi verificada; responsavel esta definido.
3. Decisao: No cenario `Lead novo com origem clara`, a Taliya segue sem equipe porque nenhuma excecao foi encontrada.
4. Acao: Executa o caso valido: qualificar origem e perfil do lead.
5. Fim: O lead recebe origem, perfil, dono e campos minimos preenchidos. Se houver duplicidade, origem desconhecida ou etapa conflitante, a ficha fica pendente para limpeza.

**Limite Do Agente**

Nao mescla lead duplicado nem corrige origem sem revisao.

**Humano/Aprovacao/Fallback**

- Chama humano quando: lead duplicado; origem nao reconhecida; campos obrigatorios faltam; lead ja esta em outra etapa; canal, cota ou permissao bloqueia atualizacao.
- Pede aprovacao quando: Nao pede aprovacao no cenario principal; nas excecoes, chama humano em vez de aprovar automaticamente.
- Fallback do teste: Se o teste cair em `Campos faltando`, Mantem ficha incompleta.

**Agente De Configuracao**

Neste teste, a Taliya executa Origem/qualificacao apenas no cenario valido. Se aparecer `Lead duplicado` ou `Origem desconhecida`, chama a equipe.

#### Perda comercial

- ID interno: `C9`.
- Modo padrao: `Autonomo com aprovacao`.
- Visual central: `Pedido de aprovacao`.
- Usa celular: `nao`.

**Cenarios**

- `Perda com motivo claro`: Monta aprovacao de perda.
- `Lead tem acao aberta`: Nao encerra.
- `Motivo sensivel`: Chama comercial.
- `Aprovacao vence`: Mantem lead ativo.

**Visual Do Caso**

card de aprovacao com dados, impacto, decisao pendente e efeito se aprovado

**Execucao Do Teste**

1. Inicio: O fluxo comeca quando um lead deve ser marcado como perdido ou sem continuidade comercial.
2. Checagens: lead esta em etapa que permite perda; motivo foi informado; responsavel comercial esta definido; impacto em relatorio foi calculado; aprovador existe quando perda for sensivel.
3. Decisao: No cenario `Perda com motivo claro`, a Taliya nao aplica sozinha: monta um pedido de aprovacao para humano autorizado.
4. Pedido de aprovacao: Monta a aprovacao para aprovar perda comercial, mostrando lead esta em etapa que permite perda; motivo foi informado; responsavel comercial esta definido; impacto em relatorio foi calculado.
5. Fim: A perda comercial vira aprovacao com motivo e impacto nos relatorios. Se aprovada, o lead sai da cadencia; se ainda houver acao aberta ou motivo sensivel, o comercial revisa.

**Limite Do Agente**

Nao encerra lead sem aprovacao quando ha sensibilidade.

**Humano/Aprovacao/Fallback**

- Chama humano quando: perda envolve reclamacao; lead ainda tem acao aberta; motivo e sensivel ou ambiguo; perda afetaria indicacao ou campanha; aprovacao vence ou permissao bloqueia.
- Pede aprovacao quando: No cenario principal, antes da acao principal.
- Fallback do teste: Se o teste cair em `Aprovacao vence`, Mantem lead ativo.

**Agente De Configuracao**

Neste teste, a Taliya monta a aprovacao de Perda comercial e nao aplica a mudanca sozinha. Se aparecer `Lead tem acao aberta` ou `Motivo sensivel`, o caso fica com a equipe.

#### Indicacao

- ID interno: `C10`.
- Modo padrao: `Autonomo com aprovacao`.
- Visual central: `Pedido de aprovacao`.
- Usa celular: `nao`.

**Cenarios**

- `Indicacao valida`: Monta aprovacao do beneficio.
- `Vinculo nao confere`: Bloqueia beneficio.
- `Indicado ja existe`: Pede revisao.
- `Aprovacao vence`: Mantem indicacao pendente.

**Visual Do Caso**

card de aprovacao com dados, impacto, decisao pendente e efeito se aprovado

**Execucao Do Teste**

1. Inicio: O fluxo comeca quando uma indicacao ou beneficio de indicacao precisa ser analisado.
2. Checagens: indicador e indicado foram identificados; regra de vinculo esta clara; beneficio permitido foi calculado; duplicidade foi verificada; aprovador esta definido.
3. Decisao: No cenario `Indicacao valida`, a Taliya nao aplica sozinha: monta um pedido de aprovacao para humano autorizado.
4. Pedido de aprovacao: Monta a aprovacao para aprovar indicacao e beneficio, mostrando indicador e indicado foram identificados; regra de vinculo esta clara; beneficio permitido foi calculado; duplicidade foi verificada.
5. Fim: A indicacao vira aprovacao com indicador, indicado, regra de vinculo e beneficio calculado. Se aprovada, o beneficio entra no processo correto; se houver duplicidade ou conflito, fica pendente.

**Limite Do Agente**

Nao concede beneficio de indicacao antes da aprovacao.

**Humano/Aprovacao/Fallback**

- Chama humano quando: vinculo nao confere; beneficio foge da regra; indicado ja existe; indicacao envolve conflito comercial; aprovacao vence ou permissao bloqueia.
- Pede aprovacao quando: No cenario principal, antes da acao principal.
- Fallback do teste: Se o teste cair em `Aprovacao vence`, Mantem indicacao pendente.

**Agente De Configuracao**

Neste teste, a Taliya monta a aprovacao de Indicacao e nao aplica a mudanca sozinha. Se aparecer `Vinculo nao confere` ou `Indicado ja existe`, o caso fica com a equipe.


### Rotina: Conversao e matricula

#### Checkout/abandono

- ID interno: `C11`.
- Modo padrao: `Autonomo com excecoes`.
- Visual central: `Celular/conversa`.
- Usa celular: `sim`.

**Cenarios**

- `Checkout abandonado`: Envia recuperacao permitida.
- `Falha financeira`: Chama comercial/financeiro.
- `Checkout expirado`: Cria tarefa.
- `Canal bloqueia`: Nao envia recuperacao.

**Visual Do Caso**

celular com conversa simulada e cartao interno mostrando o resultado do fluxo

**Execucao Do Teste**

1. Inicio: O fluxo comeca quando um checkout, proposta ou matricula fica abandonado antes de concluir.
2. Checagens: checkout abandonado foi identificado; cadencia permite contato; responsavel comercial esta definido; mensagem aprovada esta disponivel; lead nao pediu parar contato.
3. Decisao: No cenario `Checkout abandonado`, a Taliya segue sem equipe porque nenhuma excecao foi encontrada.
4. Acao: Executa o caso valido: recuperar checkout ou abandono de matricula.
5. Fim: O abandono de checkout recebe recuperacao dentro da cadencia e o lead continua no funil. Se houve falha financeira, desconto, reclamacao ou checkout expirado, o comercial assume.

**Limite Do Agente**

Nao corrige falha financeira nem concede desconto; chama comercial ou financeiro.

**Humano/Aprovacao/Fallback**

- Chama humano quando: pagamento falhou com motivo financeiro; lead pede desconto ou condicao especial; checkout esta expirado; lead responde com reclamacao; canal, cota ou permissao bloqueia contato.
- Pede aprovacao quando: Nao pede aprovacao no cenario principal; nas excecoes, chama humano em vez de aprovar automaticamente.
- Fallback do teste: Se o teste cair em `Canal bloqueia`, Nao envia recuperacao.

**Agente De Configuracao**

Neste teste, a Taliya executa Checkout/abandono apenas no cenario valido. Se aparecer `Falha financeira` ou `Checkout expirado`, chama a equipe.


### Rotina: Experimental e acompanhamento

#### Demanda sem vaga

- ID interno: `C12`.
- Modo padrao: `Autonomo com excecoes`.
- Visual central: `Celular/conversa`.
- Usa celular: `sim`.

**Cenarios**

- `Demanda sem vaga`: Cria lista de interesse.
- `Lead exige garantia`: Chama comercial.
- `Nao ha alternativa`: Mantem demanda aberta.
- `Canal bloqueia`: Nao envia mensagem.

**Visual Do Caso**

celular com conversa simulada e cartao interno mostrando o resultado do fluxo

**Execucao Do Teste**

1. Inicio: O fluxo comeca quando um lead quer uma turma, horario ou vaga que o studio nao tem disponivel agora.
2. Checagens: lead quer horario ou turma sem vaga; lista de espera foi definida; responsavel esta atribuido; regra de promessa esta clara; mensagem nao promete vaga garantida.
3. Decisao: No cenario `Demanda sem vaga`, a Taliya segue sem equipe porque nenhuma excecao foi encontrada.
4. Acao: Executa o caso valido: tratar demanda sem vaga e lista de interesse.
5. Fim: A demanda sem vaga entra em lista de interesse sem promessa de vaga garantida. Se o lead exigir prazo, garantia ou tratamento especial, o comercial decide a resposta.

**Limite Do Agente**

Nao promete vaga, turma ou prazo de abertura.

**Humano/Aprovacao/Fallback**

- Chama humano quando: lead exige prazo ou garantia; nao ha alternativa compativel; lead e prioridade comercial especial; promessa poderia ser indevida; canal, cota ou permissao bloqueia contato.
- Pede aprovacao quando: Nao pede aprovacao no cenario principal; nas excecoes, chama humano em vez de aprovar automaticamente.
- Fallback do teste: Se o teste cair em `Canal bloqueia`, Nao envia mensagem.

**Agente De Configuracao**

Neste teste, a Taliya executa Demanda sem vaga apenas no cenario valido. Se aparecer `Lead exige garantia` ou `Nao ha alternativa`, chama a equipe.


### Rotina: Conversao e matricula

#### Interessado para aluno

- ID interno: `C13`.
- Modo padrao: `Autonomo com aprovacao`.
- Visual central: `Pedido de aprovacao`.
- Usa celular: `nao`.

**Cenarios**

- `Interessado pronto`: Monta aprovacao de conversao.
- `Contrato faltando`: Nao cria aluno.
- `Aluno duplicado`: Pede revisao.
- `Aprovacao vence`: Mantem interessado pendente.

**Visual Do Caso**

card de aprovacao com dados, impacto, decisao pendente e efeito se aprovado

**Execucao Do Teste**

1. Inicio: O fluxo comeca quando um interessado esta pronto para virar aluno no CRM.
2. Checagens: interessado esta qualificado; plano escolhido foi definido; checklist de matricula esta completo; cadastro de aluno pode ser criado; aprovador esta definido.
3. Decisao: No cenario `Interessado pronto`, a Taliya nao aplica sozinha: monta um pedido de aprovacao para humano autorizado.
4. Pedido de aprovacao: Monta a aprovacao para aprovar conversao de interessado em aluno, mostrando interessado esta qualificado; plano escolhido foi definido; checklist de matricula esta completo; cadastro de aluno pode ser criado.
5. Fim: A conversao de interessado em aluno vira aprovacao com plano, cadastro e checklist. Se aprovada, o aluno e criado no CRM; se contrato, pagamento, duplicidade ou dado faltar, fica pendente.

**Limite Do Agente**

Nao cria aluno antes da aprovacao.

**Humano/Aprovacao/Fallback**

- Chama humano quando: dados obrigatorios faltam; plano ou valor nao confere; existe duplicidade de aluno; contrato ou pagamento falta; aprovacao vence ou permissao bloqueia.
- Pede aprovacao quando: No cenario principal, antes da acao principal.
- Fallback do teste: Se o teste cair em `Aprovacao vence`, Mantem interessado pendente.

**Agente De Configuracao**

Neste teste, a Taliya monta a aprovacao de Interessado para aluno e nao aplica a mudanca sozinha. Se aparecer `Contrato faltando` ou `Aluno duplicado`, o caso fica com a equipe.

#### Upsell/upgrade

- ID interno: `C14`.
- Modo padrao: `Autonomo com aprovacao`.
- Visual central: `Celular/conversa`.
- Usa celular: `sim`.

**Cenarios**

- `Aluno elegivel para upgrade`: Monta proposta de upgrade.
- `Impacto financeiro`: Exige aprovacao.
- `Aluno tem reclamacao`: Chama comercial.
- `Aprovacao vence`: Nao envia proposta.

**Visual Do Caso**

celular com conversa simulada e cartao interno mostrando o resultado do fluxo

**Execucao Do Teste**

1. Inicio: O fluxo comeca quando um aluno pode receber proposta de upgrade, upsell ou mudanca de plano.
2. Checagens: aluno elegivel foi identificado; plano destino esta definido; proposta usa template aprovado; responsavel comercial esta atribuido; aprovador esta definido.
3. Decisao: No cenario `Aluno elegivel para upgrade`, a Taliya nao aplica sozinha: monta um pedido de aprovacao para humano autorizado.
4. Pedido de aprovacao: Monta a aprovacao para aprovar proposta de upsell ou upgrade, mostrando aluno elegivel foi identificado; plano destino esta definido; proposta usa template aprovado; responsavel comercial esta atribuido.
5. Fim: O upsell ou upgrade vira proposta aprovada com plano destino e impacto financeiro. Se aprovada, a proposta e enviada ou aplicada conforme regra; se houver desconto, pendencia ou reclamacao, fica com humano.

**Limite Do Agente**

Nao aplica upgrade nem proposta sensivel antes da aprovacao.

**Humano/Aprovacao/Fallback**

- Chama humano quando: mudanca impacta financeiro atual; ha desconto ou cortesia; aluno tem pendencia ou reclamacao; proposta foge da regra; aprovacao vence ou permissao bloqueia.
- Pede aprovacao quando: No cenario principal, antes da acao principal.
- Fallback do teste: Se o teste cair em `Aprovacao vence`, Nao envia proposta.

**Agente De Configuracao**

Neste teste, a Taliya monta a aprovacao de Upsell/upgrade e nao aplica a mudanca sozinha. Se aparecer `Impacto financeiro` ou `Aluno tem reclamacao`, o caso fica com a equipe.


### Rotina: Captura e qualificacao

#### Entrada multicanal de lead

- ID interno: `C15`.
- Modo padrao: `Autonomo com excecoes`.
- Visual central: `Celular/conversa`.
- Usa celular: `sim`.

**Cenarios**

- `Lead chegou por formulario`: Cria ficha unica.
- `Lead duplicado`: Abre revisao.
- `Contato incompleto`: Mantem pendente.
- `Fonte nao reconhecida`: Pede classificacao.

**Visual Do Caso**

celular com conversa simulada e cartao interno mostrando o resultado do fluxo

**Execucao Do Teste**

1. Inicio: O fluxo comeca quando um lead entra por canal, formulario, importacao ou origem externa.
2. Checagens: fonte e aceita; lead tem contato identificavel; duplicidade foi verificada; dono do lead esta definido; campos minimos foram preenchidos.
3. Decisao: No cenario `Lead chegou por formulario`, a Taliya segue sem equipe porque nenhuma excecao foi encontrada.
4. Acao: Executa o caso valido: capturar lead de multiplos canais e criar ficha unica.
5. Fim: O lead de canal externo entra como ficha unica com origem, dono e campos minimos. Se duplicar, vier incompleto ou pertencer a outro responsavel, vai para revisao.

**Limite Do Agente**

Nao decide dono comercial quando o lead esta duplicado, incompleto ou conflitando.

**Humano/Aprovacao/Fallback**

- Chama humano quando: lead duplicado; fonte nao reconhecida; contato incompleto; lead ja pertence a outro responsavel; canal, cota ou permissao bloqueia criacao.
- Pede aprovacao quando: Nao pede aprovacao no cenario principal; nas excecoes, chama humano em vez de aprovar automaticamente.
- Fallback do teste: Se o teste cair em `Fonte nao reconhecida`, Pede classificacao.

**Agente De Configuracao**

Neste teste, a Taliya executa Entrada multicanal de lead apenas no cenario valido. Se aparecer `Lead duplicado` ou `Contato incompleto`, chama a equipe.


## Agente: Financeiro


### Rotina: Lembretes e pagamentos

#### Lembrete vencimento

- ID interno: `D1`.
- Modo padrao: `Autonomo`.
- Visual central: `Celular/conversa`.
- Usa celular: `sim`.

**Cenarios**

- `Vencimento proximo`: Envia lembrete de cobranca.
- `Cobranca ja paga`: Nao envia.
- `Valor diverge`: Chama financeiro.
- `Opt-out/canal bloqueia`: Para sem contato.

**Visual Do Caso**

celular com conversa simulada e cartao interno mostrando o resultado do fluxo

**Execucao Do Teste**

1. Inicio: O fluxo comeca quando uma cobranca esta perto do vencimento.
2. Checagens: cobranca existe; vencimento esta proximo conforme horario configurado; aluno tem canal permitido; template aprovado esta disponivel; limite por cobranca nao foi atingido.
3. Decisao: No cenario `Vencimento proximo`, a Taliya conclui sem equipe porque as checagens obrigatorias passam.
4. Acao: Conclui a acao permitida: enviar lembrete de vencimento.
5. Fim: O lembrete de vencimento e enviado antes do prazo e a cobranca mostra tentativa registrada. Se a cobranca foi paga, cancelada, diverge ou o aluno pediu opt-out, nao envia.

**Limite Do Agente**

Nao cobra se a cobranca ja foi paga, cancelada ou bloqueada para contato.

**Humano/Aprovacao/Fallback**

- Chama humano quando: Nao chama humano no cenario principal; se cair em `Opt-out/canal bloqueia`, aplica fallback: Para sem contato.
- Pede aprovacao quando: Nao pede aprovacao no cenario principal; se houver bloqueio, aplica o fallback definido.
- Fallback do teste: Se o teste cair em `Opt-out/canal bloqueia`, Para sem contato.

**Agente De Configuracao**

Neste teste, a Taliya conclui Lembrete vencimento quando as checagens passam. Se aparecer `Opt-out/canal bloqueia`, ela para e cria pendencia.

#### Pagamento atrasado

- ID interno: `D2`.
- Modo padrao: `Autonomo com excecoes`.
- Visual central: `Celular/conversa`.
- Usa celular: `sim`.

**Cenarios**

- `Pagamento atrasado comum`: Abre cobranca ou tarefa.
- `Aluno contesta valor`: Chama financeiro.
- `Pedido de acordo`: Exige decisao.
- `Provedor falha`: Cria pendencia.

**Visual Do Caso**

celular com conversa simulada e cartao interno mostrando o resultado do fluxo

**Execucao Do Teste**

1. Inicio: O fluxo comeca quando uma cobranca passa do vencimento e precisa de acao financeira.
2. Checagens: movimentacao esta vencida; tentativas permitem novo contato; fila financeira esta definida; mensagem aprovada esta disponivel; nao ha disputa registrada.
3. Decisao: No cenario `Pagamento atrasado comum`, a Taliya segue sem equipe porque nenhuma excecao foi encontrada.
4. Acao: Executa o caso valido: tratar pagamento atrasado e abrir cobranca ou tarefa.
5. Fim: O atraso abre cobranca ou tarefa financeira conforme tentativas permitidas. Se o aluno contestar, pedir acordo/desconto ou o provedor falhar, a equipe financeira assume.

**Limite Do Agente**

Nao negocia acordo, desconto ou prazo especial.

**Humano/Aprovacao/Fallback**

- Chama humano quando: aluno contesta valor; pedido envolve acordo, desconto ou prazo especial; pagamento pode ter sido feito; provedor apresenta falha; canal, cota ou permissao bloqueia contato.
- Pede aprovacao quando: Nao pede aprovacao no cenario principal; nas excecoes, chama humano em vez de aprovar automaticamente.
- Fallback do teste: Se o teste cair em `Provedor falha`, Cria pendencia.

**Agente De Configuracao**

Neste teste, a Taliya executa Pagamento atrasado apenas no cenario valido. Se aparecer `Aluno contesta valor` ou `Pedido de acordo`, chama a equipe.

#### Pix/link

- ID interno: `D3`.
- Modo padrao: `Autonomo com aprovacao`.
- Visual central: `Celular/conversa`.
- Usa celular: `sim`.

**Cenarios**

- `Link dentro do limite`: Monta aprovacao de Pix/link.
- `Valor excede limite`: Bloqueia envio.
- `Provedor retorna erro`: Cria pendencia.
- `Aprovacao vence`: Nao envia link.

**Visual Do Caso**

celular com conversa simulada e cartao interno mostrando o resultado do fluxo

**Execucao Do Teste**

1. Inicio: O fluxo comeca quando a equipe precisa enviar Pix, link ou instrucao de pagamento.
2. Checagens: movimentacao esta identificada; valor esta dentro do limite; template esta aprovado; provedor financeiro esta ok; aprovador esta definido.
3. Decisao: No cenario `Link dentro do limite`, a Taliya nao aplica sozinha: monta um pedido de aprovacao para humano autorizado.
4. Pedido de aprovacao: Monta a aprovacao para aprovar envio de Pix ou link de pagamento, mostrando movimentacao esta identificada; valor esta dentro do limite; template esta aprovado; provedor financeiro esta ok.
5. Fim: O Pix ou link vira aprovacao com valor, cobranca, provedor e mensagem. Se aprovado, a instrucao e enviada; se valor/provedor/condicao divergirem, fica pendente.

**Limite Do Agente**

Nao envia Pix/link antes da aprovacao.

**Humano/Aprovacao/Fallback**

- Chama humano quando: valor excede limite; movimentacao esta divergente; aluno pede condicao especial; provedor retorna erro; aprovacao vence ou permissao bloqueia.
- Pede aprovacao quando: No cenario principal, antes da acao principal.
- Fallback do teste: Se o teste cair em `Aprovacao vence`, Nao envia link.

**Agente De Configuracao**

Neste teste, a Taliya monta a aprovacao de Pix/link e nao aplica a mudanca sozinha. Se aparecer `Valor excede limite` ou `Provedor retorna erro`, o caso fica com a equipe.


### Rotina: Excecoes e documentos financeiros

#### Confirmacao pagamento

- ID interno: `D4`.
- Modo padrao: `Autonomo com aprovacao`.
- Visual central: `Pedido de aprovacao`.
- Usa celular: `nao`.

**Cenarios**

- `Comprovante coerente`: Monta aprovacao de pagamento.
- `Valor nao confere`: Chama financeiro.
- `Pagamento duplicado`: Bloqueia baixa.
- `Aprovacao vence`: Nao baixa cobranca.

**Visual Do Caso**

card de aprovacao com dados, impacto, decisao pendente e efeito se aprovado

**Execucao Do Teste**

1. Inicio: O fluxo comeca quando um aluno informa pagamento e a confirmacao precisa ser conferida.
2. Checagens: movimentacao foi localizada; evidencia de pagamento foi anexada; valor e aluno conferem; responsavel financeiro esta definido; aprovador esta definido.
3. Decisao: No cenario `Comprovante coerente`, a Taliya nao aplica sozinha: monta um pedido de aprovacao para humano autorizado.
4. Pedido de aprovacao: Monta a aprovacao para aprovar confirmacao de pagamento, mostrando movimentacao foi localizada; evidencia de pagamento foi anexada; valor e aluno conferem; responsavel financeiro esta definido.
5. Fim: A confirmacao de pagamento vira aprovacao com evidencia, aluno, valor e movimentacao. Se aprovada, a cobranca e baixada; se evidencia, valor ou conciliacao nao baterem, fica com financeiro.

**Limite Do Agente**

Nao baixa cobranca antes da aprovacao.

**Humano/Aprovacao/Fallback**

- Chama humano quando: evidencia esta incompleta; valor nao confere; pagamento duplicado ou suspeito; provedor ainda nao conciliou; aprovacao vence ou permissao bloqueia.
- Pede aprovacao quando: No cenario principal, antes da acao principal.
- Fallback do teste: Se o teste cair em `Aprovacao vence`, Nao baixa cobranca.

**Agente De Configuracao**

Neste teste, a Taliya monta a aprovacao de Confirmacao pagamento e nao aplica a mudanca sozinha. Se aparecer `Valor nao confere` ou `Pagamento duplicado`, o caso fica com a equipe.


### Rotina: Ciclo do plano do aluno

#### Renovacao plano

- ID interno: `D5`.
- Modo padrao: `Autonomo com aprovacao`.
- Visual central: `Pedido de aprovacao`.
- Usa celular: `nao`.

**Cenarios**

- `Renovacao no prazo`: Monta aprovacao de renovacao.
- `Aluno tem pendencia`: Chama financeiro.
- `Contrato precisa atualizar`: Nao renova.
- `Aprovacao vence`: Mantem plano atual.

**Visual Do Caso**

card de aprovacao com dados, impacto, decisao pendente e efeito se aprovado

**Execucao Do Teste**

1. Inicio: O fluxo comeca quando um plano esta perto de renovar ou precisa iniciar novo ciclo.
2. Checagens: plano atual e aluno foram identificados; antecedencia configurada chegou; novo ciclo foi calculado; template de renovacao esta aprovado; aprovador esta definido.
3. Decisao: No cenario `Renovacao no prazo`, a Taliya nao aplica sozinha: monta um pedido de aprovacao para humano autorizado.
4. Pedido de aprovacao: Monta a aprovacao para aprovar renovacao de plano, mostrando plano atual e aluno foram identificados; antecedencia configurada chegou; novo ciclo foi calculado; template de renovacao esta aprovado.
5. Fim: A renovacao vira aprovacao com novo ciclo, plano e comunicacao. Se aprovada, o plano renova; se houver pendencia, pausa, cancelamento ou contrato novo, fica pendente.

**Limite Do Agente**

Nao renova plano antes da aprovacao.

**Humano/Aprovacao/Fallback**

- Chama humano quando: aluno tem pendencia financeira; plano mudou de preco ou regra; aluno pediu pausa ou cancelamento; contrato precisa atualizacao; aprovacao vence ou permissao bloqueia.
- Pede aprovacao quando: No cenario principal, antes da acao principal.
- Fallback do teste: Se o teste cair em `Aprovacao vence`, Mantem plano atual.

**Agente De Configuracao**

Neste teste, a Taliya monta a aprovacao de Renovacao plano e nao aplica a mudanca sozinha. Se aparecer `Aluno tem pendencia` ou `Contrato precisa atualizar`, o caso fica com a equipe.


### Rotina: Excecoes e documentos financeiros

#### Excecoes financeiras

- ID interno: `D6`.
- Modo padrao: `Autonomo com aprovacao`.
- Visual central: `Pedido de aprovacao`.
- Usa celular: `nao`.

**Cenarios**

- `Excecao com motivo`: Monta aprovacao financeira.
- `Excecao excede limite`: Bloqueia aplicacao.
- `Impacto incerto`: Pede complemento.
- `Aprovacao vence`: Mantem caso aberto.

**Visual Do Caso**

card de aprovacao com dados, impacto, decisao pendente e efeito se aprovado

**Execucao Do Teste**

1. Inicio: O fluxo comeca quando aparece pedido financeiro fora da regra comum.
2. Checagens: tipo de excecao foi classificado; motivo foi informado; impacto financeiro foi calculado; prazo do caso esta definido; aprovador obrigatorio esta definido.
3. Decisao: No cenario `Excecao com motivo`, a Taliya nao aplica sozinha: monta um pedido de aprovacao para humano autorizado.
4. Pedido de aprovacao: Monta a aprovacao para aprovar excecao financeira, mostrando tipo de excecao foi classificado; motivo foi informado; impacto financeiro foi calculado; prazo do caso esta definido.
5. Fim: A excecao financeira vira aprovacao com tipo, motivo, impacto e prazo. Se aprovada, a excecao e aplicada; se ultrapassar limite ou envolver contrato/reclamacao, fica com responsavel.

**Limite Do Agente**

Nao aplica excecao financeira antes da aprovacao.

**Humano/Aprovacao/Fallback**

- Chama humano quando: motivo esta incompleto; excecao ultrapassa limite; caso envolve contrato, bloqueio ou reclamacao; impacto em aluno ou turma nao esta claro; aprovacao vence ou permissao bloqueia.
- Pede aprovacao quando: No cenario principal, antes da acao principal.
- Fallback do teste: Se o teste cair em `Aprovacao vence`, Mantem caso aberto.

**Agente De Configuracao**

Neste teste, a Taliya monta a aprovacao de Excecoes financeiras e nao aplica a mudanca sozinha. Se aparecer `Excecao excede limite` ou `Impacto incerto`, o caso fica com a equipe.


### Rotina: Lembretes e pagamentos

#### Falha pagamento

- ID interno: `D7`.
- Modo padrao: `Autonomo com excecoes`.
- Visual central: `Celular/conversa`.
- Usa celular: `sim`.

**Cenarios**

- `Falha de pagamento tratavel`: Envia orientacao ou cria tarefa.
- `Falha persiste`: Chama financeiro.
- `Aluno contesta cobranca`: Para contato.
- `Provedor indisponivel`: Abre pendencia.

**Visual Do Caso**

celular com conversa simulada e cartao interno mostrando o resultado do fluxo

**Execucao Do Teste**

1. Inicio: O fluxo comeca quando o provedor ou o CRM identifica falha de pagamento.
2. Checagens: falha veio do provedor; tentativas permitem novo contato; fila financeira esta definida; mensagem aprovada esta disponivel; nao ha disputa aberta.
3. Decisao: No cenario `Falha de pagamento tratavel`, a Taliya segue sem equipe porque nenhuma excecao foi encontrada.
4. Acao: Executa o caso valido: tratar falha de pagamento.
5. Fim: A falha de pagamento gera contato ou tarefa conforme tentativas permitidas. Se a falha persistir, virar disputa ou depender do provedor, o financeiro assume.

**Limite Do Agente**

Nao insiste em cobranca se a falha persistir ou o aluno contestar.

**Humano/Aprovacao/Fallback**

- Chama humano quando: falha persiste apos tentativas; aluno contesta cobranca; provedor retorna erro tecnico; caso exige bloqueio ou liberacao; canal, cota ou permissao bloqueia contato.
- Pede aprovacao quando: Nao pede aprovacao no cenario principal; nas excecoes, chama humano em vez de aprovar automaticamente.
- Fallback do teste: Se o teste cair em `Provedor indisponivel`, Abre pendencia.

**Agente De Configuracao**

Neste teste, a Taliya executa Falha pagamento apenas no cenario valido. Se aparecer `Falha persiste` ou `Aluno contesta cobranca`, chama a equipe.

#### Recibo/nota

- ID interno: `D8`.
- Modo padrao: `Autonomo com excecoes`.
- Visual central: `Celular/conversa`.
- Usa celular: `sim`.

**Cenarios**

- `Recibo permitido`: Emite ou prepara documento.
- `Dados fiscais faltam`: Cria tarefa.
- `Permissao bloqueia`: Nao emite.
- `Provedor falha`: Abre pendencia financeira.

**Visual Do Caso**

celular com conversa simulada e cartao interno mostrando o resultado do fluxo

**Execucao Do Teste**

1. Inicio: O fluxo comeca quando o aluno precisa de recibo, nota ou documento financeiro permitido.
2. Checagens: pagamento foi confirmado; tipo de documento e permitido; dados do aluno conferem; responsavel esta definido; fallback para tarefa existe.
3. Decisao: No cenario `Recibo permitido`, a Taliya segue sem equipe porque nenhuma excecao foi encontrada.
4. Acao: Executa o caso valido: emitir ou preparar recibo/nota permitida.
5. Fim: O recibo ou nota permitida e emitido/preparado e vinculado ao aluno. Se dados fiscais, permissao ou provedor nao fecharem, fica tarefa financeira.

**Limite Do Agente**

Nao emite documento sem dados fiscais, permissao e provedor funcionando.

**Humano/Aprovacao/Fallback**

- Chama humano quando: documento nao e permitido; dados fiscais faltam; pagamento nao esta conciliado; aluno pede documento especial; permissao ou provedor bloqueia emissao.
- Pede aprovacao quando: Nao pede aprovacao no cenario principal; nas excecoes, chama humano em vez de aprovar automaticamente.
- Fallback do teste: Se o teste cair em `Provedor falha`, Abre pendencia financeira.

**Agente De Configuracao**

Neste teste, a Taliya executa Recibo/nota apenas no cenario valido. Se aparecer `Dados fiscais faltam` ou `Permissao bloqueia`, chama a equipe.


### Rotina: Ciclo do plano do aluno

#### Pausa/trancamento

- ID interno: `D9`.
- Modo padrao: `Autonomo com aprovacao`.
- Visual central: `Pedido de aprovacao`.
- Usa celular: `nao`.

**Cenarios**

- `Pausa dentro da politica`: Monta aprovacao de pausa.
- `Impacto financeiro`: Exige decisao.
- `Periodo invalido`: Pede ajuste.
- `Aprovacao vence`: Mantem plano ativo.

**Visual Do Caso**

card de aprovacao com dados, impacto, decisao pendente e efeito se aprovado

**Execucao Do Teste**

1. Inicio: O fluxo comeca quando o aluno pede pausa, trancamento ou interrupcao temporaria.
2. Checagens: aluno e plano foram identificados; motivo foi informado; impacto em agenda e cobranca foi calculado; prazo esta definido; aprovador esta definido.
3. Decisao: No cenario `Pausa dentro da politica`, a Taliya nao aplica sozinha: monta um pedido de aprovacao para humano autorizado.
4. Pedido de aprovacao: Monta a aprovacao para aprovar pausa ou trancamento, mostrando aluno e plano foram identificados; motivo foi informado; impacto em agenda e cobranca foi calculado; prazo esta definido.
5. Fim: A pausa ou trancamento vira aprovacao com periodo, motivo, impacto no plano e retorno previsto. Se aprovada, o plano muda; se impactar financeiro ou contrato, fica pendente.

**Limite Do Agente**

Nao pausa ou tranca plano antes da aprovacao.

**Humano/Aprovacao/Fallback**

- Chama humano quando: pedido afeta credito, contrato ou vencimento; aluno tem pendencia; motivo e sensivel; data solicitada conflita com regra; aprovacao vence ou permissao bloqueia.
- Pede aprovacao quando: No cenario principal, antes da acao principal.
- Fallback do teste: Se o teste cair em `Aprovacao vence`, Mantem plano ativo.

**Agente De Configuracao**

Neste teste, a Taliya monta a aprovacao de Pausa/trancamento e nao aplica a mudanca sozinha. Se aparecer `Impacto financeiro` ou `Periodo invalido`, o caso fica com a equipe.


### Rotina: Lembretes e pagamentos

#### Conciliacao interna

- ID interno: `D10`.
- Modo padrao: `Autonomo com aprovacao`.
- Visual central: `Pedido de aprovacao`.
- Usa celular: `nao`.

**Cenarios**

- `Conciliacao com alta confianca`: Monta aprovacao de conciliacao.
- `Mais de um candidato`: Chama financeiro.
- `Valor diverge`: Bloqueia vinculo.
- `Aprovacao vence`: Nao concilia.

**Visual Do Caso**

card de aprovacao com dados, impacto, decisao pendente e efeito se aprovado

**Execucao Do Teste**

1. Inicio: O fluxo comeca quando um pagamento precisa ser conciliado com uma movimentacao interna.
2. Checagens: movimentacao e pagamento candidato foram encontrados; confianca minima foi atingida; responsavel financeiro esta definido; impacto foi mostrado; aprovador esta definido.
3. Decisao: No cenario `Conciliacao com alta confianca`, a Taliya nao aplica sozinha: monta um pedido de aprovacao para humano autorizado.
4. Pedido de aprovacao: Monta a aprovacao para aprovar conciliacao interna, mostrando movimentacao e pagamento candidato foram encontrados; confianca minima foi atingida; responsavel financeiro esta definido; impacto foi mostrado.
5. Fim: A conciliacao interna vira aprovacao com candidato, confianca, valor, data e impacto. Se aprovada, movimentacao e pagamento ficam vinculados; se houver divergencia, fica com financeiro.

**Limite Do Agente**

Nao vincula pagamento e movimentacao antes da aprovacao.

**Humano/Aprovacao/Fallback**

- Chama humano quando: confianca esta baixa; ha mais de um candidato; valor ou data divergem; provedor esta instavel; aprovacao vence ou permissao bloqueia.
- Pede aprovacao quando: No cenario principal, antes da acao principal.
- Fallback do teste: Se o teste cair em `Aprovacao vence`, Nao concilia.

**Agente De Configuracao**

Neste teste, a Taliya monta a aprovacao de Conciliacao interna e nao aplica a mudanca sozinha. Se aparecer `Mais de um candidato` ou `Valor diverge`, o caso fica com a equipe.


### Rotina: Excecoes e documentos financeiros

#### Contrato/termos

- ID interno: `D11`.
- Modo padrao: `Autonomo com aprovacao`.
- Visual central: `Pedido de aprovacao`.
- Usa celular: `nao`.

**Cenarios**

- `Contrato pronto`: Monta aprovacao do documento.
- `Versao faltando`: Bloqueia envio.
- `Dados incompletos`: Pede complemento.
- `Aprovacao vence`: Mantem documento em rascunho.

**Visual Do Caso**

card de aprovacao com dados, impacto, decisao pendente e efeito se aprovado

**Execucao Do Teste**

1. Inicio: O fluxo comeca quando contrato, termo ou documento precisa ser preparado para aluno ou plano.
2. Checagens: template de contrato esta definido; dados do aluno e plano conferem; prazo de envio esta definido; responsavel esta atribuido; aprovador esta definido.
3. Decisao: No cenario `Contrato pronto`, a Taliya nao aplica sozinha: monta um pedido de aprovacao para humano autorizado.
4. Pedido de aprovacao: Monta a aprovacao para aprovar contrato ou termos, mostrando template de contrato esta definido; dados do aluno e plano conferem; prazo de envio esta definido; responsavel esta atribuido.
5. Fim: Contrato ou termo vira aprovacao com aluno, plano, versao e dados usados. Se aprovado, o documento segue para envio/assinatura; se faltar dado ou versao, fica pendente.

**Limite Do Agente**

Nao envia contrato/termo antes da aprovacao.

**Humano/Aprovacao/Fallback**

- Chama humano quando: template nao cobre o caso; dados obrigatorios faltam; plano ou valor diverge; aluno pede clausula especial; aprovacao vence ou permissao bloqueia.
- Pede aprovacao quando: No cenario principal, antes da acao principal.
- Fallback do teste: Se o teste cair em `Aprovacao vence`, Mantem documento em rascunho.

**Agente De Configuracao**

Neste teste, a Taliya monta a aprovacao de Contrato/termos e nao aplica a mudanca sozinha. Se aparecer `Versao faltando` ou `Dados incompletos`, o caso fica com a equipe.

#### Bloqueio/liberacao

- ID interno: `D12`.
- Modo padrao: `Autonomo com aprovacao`.
- Visual central: `Pedido de aprovacao`.
- Usa celular: `nao`.

**Cenarios**

- `Liberacao com motivo claro`: Monta aprovacao de acesso.
- `Pagamento recente contestado`: Chama financeiro.
- `Impacto nao claro`: Bloqueia mudanca.
- `Aprovacao vence`: Nao altera acesso.

**Visual Do Caso**

card de aprovacao com dados, impacto, decisao pendente e efeito se aprovado

**Execucao Do Teste**

1. Inicio: O fluxo comeca quando o studio precisa bloquear ou liberar acesso por motivo financeiro.
2. Checagens: aluno e motivo foram identificados; impacto financeiro foi calculado; motivo obrigatorio foi preenchido; prazo de aprovacao esta definido; aprovador esta definido.
3. Decisao: No cenario `Liberacao com motivo claro`, a Taliya nao aplica sozinha: monta um pedido de aprovacao para humano autorizado.
4. Pedido de aprovacao: Monta a aprovacao para aprovar bloqueio ou liberacao, mostrando aluno e motivo foram identificados; impacto financeiro foi calculado; motivo obrigatorio foi preenchido; prazo de aprovacao esta definido.
5. Fim: Bloqueio ou liberacao vira aprovacao com motivo, aluno, impacto e comunicacao. Se aprovado, o acesso muda; se houver contestacao, pagamento recente ou excecao, fica com humano.

**Limite Do Agente**

Nao bloqueia nem libera acesso antes da aprovacao.

**Humano/Aprovacao/Fallback**

- Chama humano quando: motivo esta incompleto; bloqueio afeta aula ja marcada; liberacao contraria regra financeira; ha reclamacao ou disputa; aprovacao vence ou permissao bloqueia.
- Pede aprovacao quando: No cenario principal, antes da acao principal.
- Fallback do teste: Se o teste cair em `Aprovacao vence`, Nao altera acesso.

**Agente De Configuracao**

Neste teste, a Taliya monta a aprovacao de Bloqueio/liberacao e nao aplica a mudanca sozinha. Se aparecer `Pagamento recente contestado` ou `Impacto nao claro`, o caso fica com a equipe.

#### Creditos/cortesias

- ID interno: `D13`.
- Modo padrao: `Autonomo com aprovacao`.
- Visual central: `Pedido de aprovacao`.
- Usa celular: `nao`.

**Cenarios**

- `Cortesia dentro da politica`: Monta aprovacao do beneficio.
- `Valor foge da politica`: Bloqueia aplicacao.
- `Motivo incompleto`: Pede complemento.
- `Aprovacao vence`: Nao aplica credito.

**Visual Do Caso**

card de aprovacao com dados, impacto, decisao pendente e efeito se aprovado

**Execucao Do Teste**

1. Inicio: O fluxo comeca quando alguem pede credito, cortesia ou ajuste financeiro excepcional.
2. Checagens: aluno foi identificado; motivo foi informado; limite de valor esta dentro da politica; impacto financeiro foi calculado; aprovador esta definido.
3. Decisao: No cenario `Cortesia dentro da politica`, a Taliya nao aplica sozinha: monta um pedido de aprovacao para humano autorizado.
4. Pedido de aprovacao: Monta a aprovacao para aprovar credito ou cortesia, mostrando aluno foi identificado; motivo foi informado; limite de valor esta dentro da politica; impacto financeiro foi calculado.
5. Fim: Credito ou cortesia vira aprovacao com motivo, valor, validade e impacto. Se aprovado, o beneficio aparece no financeiro; se fugir da politica, fica com responsavel.

**Limite Do Agente**

Nao aplica credito ou cortesia antes da aprovacao.

**Humano/Aprovacao/Fallback**

- Chama humano quando: valor excede limite; motivo e insuficiente; ha credito duplicado; cortesia afeta contrato ou plano; aprovacao vence ou permissao bloqueia.
- Pede aprovacao quando: No cenario principal, antes da acao principal.
- Fallback do teste: Se o teste cair em `Aprovacao vence`, Nao aplica credito.

**Agente De Configuracao**

Neste teste, a Taliya monta a aprovacao de Creditos/cortesias e nao aplica a mudanca sozinha. Se aparecer `Valor foge da politica` ou `Motivo incompleto`, o caso fica com a equipe.

#### Fechamento mensal

- ID interno: `D14`.
- Modo padrao: `Autonomo com excecoes`.
- Visual central: `Fechamento financeiro`.
- Usa celular: `nao`.

**Cenarios**

- `Fechamento sem divergencia`: Separa consolidados e pendencias.
- `Conciliacao divergente`: Cria tarefa.
- `Provedor falhou`: Marca fechamento incompleto.
- `Permissao bloqueia`: Nao gera fechamento final.

**Visual Do Caso**

painel de fechamento com consolidados, pendencias e divergencias

**Execucao Do Teste**

1. Inicio: O fluxo comeca quando chega o periodo de fechamento financeiro do mes.
2. Checagens: periodo de fechamento esta definido; movimentacoes foram consolidadas; pendencias foram separadas; responsavel financeiro esta definido; frequencia do resumo esta configurada.
3. Decisao: No cenario `Fechamento sem divergencia`, a Taliya segue sem equipe porque nenhuma excecao foi encontrada.
4. Acao: Executa o caso valido: preparar fechamento mensal financeiro.
5. Fim: O fechamento mensal separa consolidados, pendencias e alertas financeiros para o responsavel. Se conciliacao, provedor ou dado falhar, o fechamento fica incompleto e gera tarefa.

**Limite Do Agente**

Nao fecha o mes se conciliacao, provedor ou permissao impedirem a conferencia.

**Humano/Aprovacao/Fallback**

- Chama humano quando: ha divergencia de conciliacao; movimentacao sem dono; provedor financeiro falhou; pendencia critica apareceu; permissao ou cota bloqueia analise.
- Pede aprovacao quando: Nao pede aprovacao no cenario principal; nas excecoes, chama humano em vez de aprovar automaticamente.
- Fallback do teste: Se o teste cair em `Permissao bloqueia`, Nao gera fechamento final.

**Agente De Configuracao**

Neste teste, a Taliya executa Fechamento mensal apenas no cenario valido. Se aparecer `Conciliacao divergente` ou `Provedor falhou`, chama a equipe.


### Rotina: Ciclo do plano do aluno

#### Encerramento ou alteracao efetiva de plano

- ID interno: `D15`.
- Modo padrao: `Autonomo com aprovacao`.
- Visual central: `Pedido de aprovacao`.
- Usa celular: `nao`.

**Cenarios**

- `Alteracao efetiva clara`: Monta aprovacao de plano.
- `Saldo pendente`: Bloqueia mudanca.
- `Contrato afetado`: Chama financeiro.
- `Aprovacao vence`: Mantem plano atual.

**Visual Do Caso**

card de aprovacao com dados, impacto, decisao pendente e efeito se aprovado

**Execucao Do Teste**

1. Inicio: O fluxo comeca quando plano de aluno precisa ser encerrado ou alterado de forma efetiva.
2. Checagens: plano atual foi identificado; mudanca solicitada foi descrita; impacto em agenda, cobranca e contrato foi calculado; checklist esta completo; aprovador esta definido.
3. Decisao: No cenario `Alteracao efetiva clara`, a Taliya nao aplica sozinha: monta um pedido de aprovacao para humano autorizado.
4. Pedido de aprovacao: Monta a aprovacao para aprovar encerramento ou alteracao de plano, mostrando plano atual foi identificado; mudanca solicitada foi descrita; impacto em agenda, cobranca e contrato foi calculado; checklist esta completo.
5. Fim: Encerramento ou alteracao de plano vira aprovacao com data efetiva, impacto financeiro e comunicacao. Se aprovado, o plano muda; se houver contrato, saldo ou pendencia, fica travado.

**Limite Do Agente**

Nao efetiva alteracao de plano antes da aprovacao.

**Humano/Aprovacao/Fallback**

- Chama humano quando: impacto financeiro nao esta claro; aluno tem aulas ou creditos pendentes; contrato precisa revisao; pedido envolve cancelamento sensivel; aprovacao vence ou permissao bloqueia.
- Pede aprovacao quando: No cenario principal, antes da acao principal.
- Fallback do teste: Se o teste cair em `Aprovacao vence`, Mantem plano atual.

**Agente De Configuracao**

Neste teste, a Taliya monta a aprovacao de Encerramento ou alteracao efetiva de plano e nao aplica a mudanca sozinha. Se aparecer `Saldo pendente` ou `Contrato afetado`, o caso fica com a equipe.


## Agente: Retencao


### Rotina: Retencao preventiva

#### Queda frequencia

- ID interno: `E1`.
- Modo padrao: `Autonomo com excecoes`.
- Visual central: `Celular/conversa`.
- Usa celular: `sim`.

**Cenarios**

- `Frequencia caiu`: Abre cuidado preventivo.
- `Recorrencia alta`: Chama equipe.
- `Sinal de saude`: Nao envia mensagem automatica.
- `Canal bloqueia`: Cria tarefa.

**Visual Do Caso**

celular com conversa simulada e cartao interno mostrando o resultado do fluxo

**Execucao Do Teste**

1. Inicio: O fluxo comeca quando a frequencia de um aluno cai abaixo do padrao esperado.
2. Checagens: frequencia caiu conforme regra publicada; aluno esta ativo; responsavel esta definido; cadencia permite contato; nao ha caso sensivel aberto.
3. Decisao: No cenario `Frequencia caiu`, a Taliya segue sem equipe porque nenhuma excecao foi encontrada.
4. Acao: Executa o caso valido: detectar queda de frequencia e iniciar prevencao.
5. Fim: A queda de frequencia abre contato preventivo ou tarefa de cuidado conforme regra. Se houver recorrencia, reclamacao, saude ou canal bloqueado, a equipe assume.

**Limite Do Agente**

Nao trata recorrencia, saude ou reclamacao sozinho.

**Humano/Aprovacao/Fallback**

- Chama humano quando: queda tem motivo ja registrado; aluno tem reclamacao ou saude/evento pessoal; risco de cancelamento aumentou; cadencia foi excedida; canal, cota ou permissao bloqueia contato.
- Pede aprovacao quando: Nao pede aprovacao no cenario principal; nas excecoes, chama humano em vez de aprovar automaticamente.
- Fallback do teste: Se o teste cair em `Canal bloqueia`, Cria tarefa.

**Agente De Configuracao**

Neste teste, a Taliya executa Queda frequencia apenas no cenario valido. Se aparecer `Recorrencia alta` ou `Sinal de saude`, chama a equipe.

#### Aluno inativo

- ID interno: `E2`.
- Modo padrao: `Autonomo com excecoes`.
- Visual central: `Celular/conversa`.
- Usa celular: `sim`.

**Cenarios**

- `Aluno inativo elegivel`: Inicia retomada permitida.
- `Aluno pausou`: Para contato.
- `Pendencia financeira`: Chama equipe.
- `Opt-out`: Nao envia.

**Visual Do Caso**

celular com conversa simulada e cartao interno mostrando o resultado do fluxo

**Execucao Do Teste**

1. Inicio: O fluxo comeca quando um aluno ativo fica inativo por tempo relevante.
2. Checagens: dias de inatividade atingiram o limite; aluno esta elegivel para contato; responsavel esta definido; limite de contato nao foi atingido; mensagem aprovada esta disponivel.
3. Decisao: No cenario `Aluno inativo elegivel`, a Taliya segue sem equipe porque nenhuma excecao foi encontrada.
4. Acao: Executa o caso valido: identificar aluno inativo e preparar retomada.
5. Fim: O aluno inativo entra em retomada permitida com responsavel e limite de contato. Se pausou, pediu opt-out, tem pendencia ou caso sensivel, o fluxo para.

**Limite Do Agente**

Nao contata aluno pausado, com opt-out ou com pendencia sensivel.

**Humano/Aprovacao/Fallback**

- Chama humano quando: aluno pausou ou trancou; aluno pediu opt-out; ha pendencia financeira ou reclamacao; historico indica caso sensivel; canal, cota ou permissao bloqueia contato.
- Pede aprovacao quando: Nao pede aprovacao no cenario principal; nas excecoes, chama humano em vez de aprovar automaticamente.
- Fallback do teste: Se o teste cair em `Opt-out`, Nao envia.

**Agente De Configuracao**

Neste teste, a Taliya executa Aluno inativo apenas no cenario valido. Se aparecer `Aluno pausou` ou `Pendencia financeira`, chama a equipe.

#### Retorno

- ID interno: `E3`.
- Modo padrao: `Autonomo com excecoes`.
- Visual central: `Celular/conversa`.
- Usa celular: `sim`.

**Cenarios**

- `Aluno quer voltar`: Organiza retorno.
- `Sem horario compativel`: Cria tarefa.
- `Pendencia financeira`: Chama equipe.
- `Cuidado especial`: Pede revisao.

**Visual Do Caso**

celular com conversa simulada e cartao interno mostrando o resultado do fluxo

**Execucao Do Teste**

1. Inicio: O fluxo comeca quando um aluno demonstra interesse em voltar.
2. Checagens: aluno demonstrou interesse em voltar; regra de agenda permite encaixe; responsavel esta definido; opcoes de horario existem; mensagem aprovada esta disponivel.
3. Decisao: No cenario `Aluno quer voltar`, a Taliya segue sem equipe porque nenhuma excecao foi encontrada.
4. Acao: Executa o caso valido: organizar retorno de aluno.
5. Fim: O retorno do aluno organiza opcoes de agenda e proximo contato. Se nao houver horario, houver pendencia financeira ou cuidado especial, a equipe decide.

**Limite Do Agente**

Nao escolhe retorno sem vaga, sem resolver pendencias ou sem revisar cuidado especial.

**Humano/Aprovacao/Fallback**

- Chama humano quando: nao ha horario compativel; aluno tem pendencia financeira; retorno exige avaliacao ou cuidado; aluno pede condicao especial; canal, cota ou permissao bloqueia contato.
- Pede aprovacao quando: Nao pede aprovacao no cenario principal; nas excecoes, chama humano em vez de aprovar automaticamente.
- Fallback do teste: Se o teste cair em `Cuidado especial`, Pede revisao.

**Agente De Configuracao**

Neste teste, a Taliya executa Retorno apenas no cenario valido. Se aparecer `Sem horario compativel` ou `Pendencia financeira`, chama a equipe.


### Rotina: Casos sensiveis

#### Risco cancelamento

- ID interno: `E4`.
- Modo padrao: `Autonomo com aprovacao`.
- Visual central: `Pedido de aprovacao`.
- Usa celular: `nao`.

**Cenarios**

- `Sinal de cancelamento`: Monta aprovacao de retencao.
- `Cancelamento formal`: Nao automatiza.
- `Caso sensivel`: Chama responsavel.
- `Aprovacao vence`: Mantem caso aberto.

**Visual Do Caso**

card de aprovacao com dados, impacto, decisao pendente e efeito se aprovado

**Execucao Do Teste**

1. Inicio: O fluxo comeca quando aparecem sinais de risco de cancelamento.
2. Checagens: sinal de cancelamento foi detectado; dono do caso esta definido; automacoes conflitantes foram pausadas; contexto foi resumido; aprovador esta definido.
3. Decisao: No cenario `Sinal de cancelamento`, a Taliya nao aplica sozinha: monta um pedido de aprovacao para humano autorizado.
4. Pedido de aprovacao: Monta a aprovacao para aprovar acao de retencao, mostrando sinal de cancelamento foi detectado; dono do caso esta definido; automacoes conflitantes foram pausadas; contexto foi resumido.
5. Fim: O risco de cancelamento vira aprovacao com contexto, dono e automacoes conflitantes pausadas. Se aprovado, a acao de retencao segue; se for cancelamento formal ou caso sensivel, fica com responsavel.

**Limite Do Agente**

Nao executa retencao sensivel sem aprovacao.

**Humano/Aprovacao/Fallback**

- Chama humano quando: aluno ja pediu cancelamento formal; caso envolve reclamacao ou saude; proposta de retencao exige beneficio; historico e sensivel; aprovacao vence ou permissao bloqueia.
- Pede aprovacao quando: No cenario principal, antes da acao principal.
- Fallback do teste: Se o teste cair em `Aprovacao vence`, Mantem caso aberto.

**Agente De Configuracao**

Neste teste, a Taliya monta a aprovacao de Risco cancelamento e nao aplica a mudanca sozinha. Se aparecer `Cancelamento formal` ou `Caso sensivel`, o caso fica com a equipe.

#### Reativacao ex-aluno

- ID interno: `E5`.
- Modo padrao: `Autonomo com aprovacao`.
- Visual central: `Celular/conversa`.
- Usa celular: `sim`.

**Cenarios**

- `Ex-aluno elegivel`: Monta aprovacao de reativacao.
- `Opt-out`: Bloqueia contato.
- `Historico com reclamacao`: Chama responsavel.
- `Aprovacao vence`: Nao libera contato.

**Visual Do Caso**

celular com conversa simulada e cartao interno mostrando o resultado do fluxo

**Execucao Do Teste**

1. Inicio: O fluxo comeca quando um ex-aluno entra em segmento permitido para reativacao.
2. Checagens: ex-aluno esta no segmento permitido; cadencia permite contato; mensagem esta aprovada; responsavel esta definido; aprovador esta definido.
3. Decisao: No cenario `Ex-aluno elegivel`, a Taliya nao aplica sozinha: monta um pedido de aprovacao para humano autorizado.
4. Pedido de aprovacao: Monta a aprovacao para aprovar reativacao de ex-aluno, mostrando ex-aluno esta no segmento permitido; cadencia permite contato; mensagem esta aprovada; responsavel esta definido.
5. Fim: A reativacao de ex-aluno vira aprovacao com segmento, mensagem e responsavel. Se aprovada, o contato e liberado; se houver opt-out, reclamacao ou beneficio especial, fica bloqueado.

**Limite Do Agente**

Nao contata ex-aluno antes da aprovacao.

**Humano/Aprovacao/Fallback**

- Chama humano quando: ex-aluno pediu opt-out; historico tem reclamacao sensivel; segmento nao permite campanha; beneficio ou condicao especial foi sugerido; aprovacao vence ou permissao bloqueia.
- Pede aprovacao quando: No cenario principal, antes da acao principal.
- Fallback do teste: Se o teste cair em `Aprovacao vence`, Nao libera contato.

**Agente De Configuracao**

Neste teste, a Taliya monta a aprovacao de Reativacao ex-aluno e nao aplica a mudanca sozinha. Se aparecer `Opt-out` ou `Historico com reclamacao`, o caso fica com a equipe.


### Rotina: Retencao preventiva

#### Satisfacao

- ID interno: `E6`.
- Modo padrao: `Autonomo com excecoes`.
- Visual central: `Celular/conversa`.
- Usa celular: `sim`.

**Cenarios**

- `Pesquisa de satisfacao`: Coleta sinal e abre cuidado se preciso.
- `Nota baixa`: Chama equipe.
- `Texto cita professor`: Cria caso sensivel.
- `Canal bloqueia`: Nao envia pesquisa.

**Visual Do Caso**

celular com conversa simulada e cartao interno mostrando o resultado do fluxo

**Execucao Do Teste**

1. Inicio: O fluxo comeca quando chega a janela de medir satisfacao ou cuidado com o aluno.
2. Checagens: janela de satisfacao chegou; aluno esta elegivel; responsavel esta definido; mensagem aprovada esta disponivel; nao ha reclamacao aberta.
3. Decisao: No cenario `Pesquisa de satisfacao`, a Taliya segue sem equipe porque nenhuma excecao foi encontrada.
4. Acao: Executa o caso valido: acompanhar satisfacao e abrir cuidado quando necessario.
5. Fim: A satisfacao e coletada ou acompanhada e, se houver sinal ruim, abre cuidado. Se a resposta citar reclamacao, saude, professor ou cobranca, vai para humano.

**Limite Do Agente**

Nao responde reclamacao, saude, professor ou cobranca sozinho.

**Humano/Aprovacao/Fallback**

- Chama humano quando: resposta indica reclamacao; nota baixa ou texto sensivel; aluno menciona saude, professor ou cobranca; ja existe caso aberto; canal, cota ou permissao bloqueia contato.
- Pede aprovacao quando: Nao pede aprovacao no cenario principal; nas excecoes, chama humano em vez de aprovar automaticamente.
- Fallback do teste: Se o teste cair em `Canal bloqueia`, Nao envia pesquisa.

**Agente De Configuracao**

Neste teste, a Taliya executa Satisfacao apenas no cenario valido. Se aparecer `Nota baixa` ou `Texto cita professor`, chama a equipe.

#### Retorno apos pausa

- ID interno: `E7`.
- Modo padrao: `Autonomo com excecoes`.
- Visual central: `Celular/conversa`.
- Usa celular: `sim`.

**Cenarios**

- `Pausa perto do fim`: Prepara retorno.
- `Aluno pede extensao`: Chama equipe.
- `Sem vaga`: Cria tarefa.
- `Pendencia financeira`: Bloqueia contato automatico.

**Visual Do Caso**

celular com conversa simulada e cartao interno mostrando o resultado do fluxo

**Execucao Do Teste**

1. Inicio: O fluxo comeca quando uma pausa esta perto de terminar.
2. Checagens: fim da pausa esta proximo; aluno esta elegivel para retorno; opcoes de agenda existem; responsavel esta definido; antecedencia configurada chegou.
3. Decisao: No cenario `Pausa perto do fim`, a Taliya segue sem equipe porque nenhuma excecao foi encontrada.
4. Acao: Executa o caso valido: preparar retorno apos pausa.
5. Fim: O retorno apos pausa prepara contato e opcoes de agenda antes do fim da pausa. Se o aluno pedir extensao, nao houver vaga ou houver pendencia, vira tarefa.

**Limite Do Agente**

Nao decide extensao de pausa, vaga de retorno ou pendencia financeira.

**Humano/Aprovacao/Fallback**

- Chama humano quando: aluno pede estender pausa; agenda nao tem vaga; ha pendencia financeira; retorno exige cuidado ou professor especifico; canal, cota ou permissao bloqueia contato.
- Pede aprovacao quando: Nao pede aprovacao no cenario principal; nas excecoes, chama humano em vez de aprovar automaticamente.
- Fallback do teste: Se o teste cair em `Pendencia financeira`, Bloqueia contato automatico.

**Agente De Configuracao**

Neste teste, a Taliya executa Retorno apos pausa apenas no cenario valido. Se aparecer `Aluno pede extensao` ou `Sem vaga`, chama a equipe.


### Rotina: Casos sensiveis

#### Risco por perfil

- ID interno: `E8`.
- Modo padrao: `Autonomo com aprovacao`.
- Visual central: `Pedido de aprovacao`.
- Usa celular: `nao`.

**Cenarios**

- `Segmento de risco permitido`: Monta aprovacao de acao.
- `Dado sensivel usado`: Bloqueia acao.
- `Acao invasiva`: Pede revisao.
- `Aprovacao vence`: Nao executa acao.

**Visual Do Caso**

card de aprovacao com dados, impacto, decisao pendente e efeito se aprovado

**Execucao Do Teste**

1. Inicio: O fluxo comeca quando um perfil ou segmento indica risco de evasao.
2. Checagens: segmento de risco foi identificado; uso do segmento esta permitido; acao proposta foi definida; responsavel esta definido; aprovador esta definido.
3. Decisao: No cenario `Segmento de risco permitido`, a Taliya nao aplica sozinha: monta um pedido de aprovacao para humano autorizado.
4. Pedido de aprovacao: Monta a aprovacao para aprovar acao por perfil de risco, mostrando segmento de risco foi identificado; uso do segmento esta permitido; acao proposta foi definida; responsavel esta definido.
5. Fim: A acao por perfil de risco vira aprovacao com segmento, dados usados e abordagem. Se aprovada, a acao segue; se parecer invasiva ou usar dado sensivel, fica bloqueada.

**Limite Do Agente**

Nao usa perfil de risco sem aprovacao.

**Humano/Aprovacao/Fallback**

- Chama humano quando: segmento e sensivel; acao pode parecer invasiva; dados usados nao estao permitidos; aluno tem caso aberto; aprovacao vence ou permissao bloqueia.
- Pede aprovacao quando: No cenario principal, antes da acao principal.
- Fallback do teste: Se o teste cair em `Aprovacao vence`, Nao executa acao.

**Agente De Configuracao**

Neste teste, a Taliya monta a aprovacao de Risco por perfil e nao aplica a mudanca sozinha. Se aparecer `Dado sensivel usado` ou `Acao invasiva`, o caso fica com a equipe.

#### Pos-cancelamento

- ID interno: `E9`.
- Modo padrao: `Autonomo com aprovacao`.
- Visual central: `Celular/conversa`.
- Usa celular: `sim`.

**Cenarios**

- `Pos-cancelamento permitido`: Monta aprovacao de contato.
- `Aluno pediu nao contato`: Bloqueia mensagem.
- `Cancelamento com reclamacao`: Chama responsavel.
- `Aprovacao vence`: Nao libera contato.

**Visual Do Caso**

celular com conversa simulada e cartao interno mostrando o resultado do fluxo

**Execucao Do Teste**

1. Inicio: O fluxo comeca depois que um cancelamento foi registrado e ainda pode haver cuidado pos-cancelamento.
2. Checagens: cancelamento foi registrado; janela de contato esta definida; responsavel esta atribuido; mensagem nao reabre conflito; aprovador esta definido.
3. Decisao: No cenario `Pos-cancelamento permitido`, a Taliya nao aplica sozinha: monta um pedido de aprovacao para humano autorizado.
4. Pedido de aprovacao: Monta a aprovacao para aprovar contato pos-cancelamento, mostrando cancelamento foi registrado; janela de contato esta definida; responsavel esta atribuido; mensagem nao reabre conflito.
5. Fim: O pos-cancelamento vira aprovacao com janela, motivo e mensagem cuidadosa. Se aprovado, o contato e liberado; se houve reclamacao, saude ou pedido de nao contato, fica bloqueado.

**Limite Do Agente**

Nao recontata aluno cancelado sem aprovacao.

**Humano/Aprovacao/Fallback**

- Chama humano quando: cancelamento teve reclamacao; aluno pediu nao ser contatado; motivo envolve saude ou evento pessoal; beneficio de retorno seria oferecido; aprovacao vence ou permissao bloqueia.
- Pede aprovacao quando: No cenario principal, antes da acao principal.
- Fallback do teste: Se o teste cair em `Aprovacao vence`, Nao libera contato.

**Agente De Configuracao**

Neste teste, a Taliya monta a aprovacao de Pos-cancelamento e nao aplica a mudanca sozinha. Se aparecer `Aluno pediu nao contato` ou `Cancelamento com reclamacao`, o caso fica com a equipe.


### Rotina: Retencao preventiva

#### Marco engajamento

- ID interno: `E10`.
- Modo padrao: `Autonomo com excecoes`.
- Visual central: `Celular/conversa`.
- Usa celular: `sim`.

**Cenarios**

- `Marco positivo`: Registra marco e aciona contato leve.
- `Caso sensivel aberto`: Nao envia.
- `Baixa frequencia conflita`: Chama equipe.
- `Opt-out`: Bloqueia contato.

**Visual Do Caso**

celular com conversa simulada e cartao interno mostrando o resultado do fluxo

**Execucao Do Teste**

1. Inicio: O fluxo comeca quando um aluno atinge um marco de engajamento permitido.
2. Checagens: marco configurado aconteceu; aluno esta ativo; tipo de marco esta permitido; responsavel esta definido; limite de contato nao foi atingido.
3. Decisao: No cenario `Marco positivo`, a Taliya segue sem equipe porque nenhuma excecao foi encontrada.
4. Acao: Executa o caso valido: reconhecer marco de engajamento e acionar contato leve.
5. Fim: O marco de engajamento gera contato leve ou registro positivo. Se houver caso sensivel, baixa frequencia ou opt-out, a mensagem nao sai.

**Limite Do Agente**

Nao envia contato leve se houver caso sensivel, baixa frequencia conflitante ou opt-out.

**Humano/Aprovacao/Fallback**

- Chama humano quando: aluno tem caso sensivel aberto; marco conflita com baixa frequencia; mensagem poderia soar inadequada; aluno pediu opt-out; canal, cota ou permissao bloqueia contato.
- Pede aprovacao quando: Nao pede aprovacao no cenario principal; nas excecoes, chama humano em vez de aprovar automaticamente.
- Fallback do teste: Se o teste cair em `Opt-out`, Bloqueia contato.

**Agente De Configuracao**

Neste teste, a Taliya executa Marco engajamento apenas no cenario valido. Se aparecer `Caso sensivel aberto` ou `Baixa frequencia conflita`, chama a equipe.


### Rotina: Casos sensiveis

#### Saude/evento pessoal

- ID interno: `E11`.
- Modo padrao: `Autonomo com aprovacao`.
- Visual central: `Pedido de aprovacao`.
- Usa celular: `nao`.

**Cenarios**

- `Evento pessoal identificado`: Monta aprovacao de cuidado.
- `Aluno pediu sigilo`: Bloqueia exposicao.
- `Dado incompleto`: Pede revisao.
- `Aprovacao vence`: Mantem caso restrito.

**Visual Do Caso**

card de aprovacao com dados, impacto, decisao pendente e efeito se aprovado

**Execucao Do Teste**

1. Inicio: O fluxo comeca quando aparece informacao de saude, evento pessoal ou cuidado sensivel.
2. Checagens: evento foi identificado; visibilidade esta definida; dono do caso foi atribuido; nenhum contato automatico sera feito sem revisao; aprovador esta definido.
3. Decisao: No cenario `Evento pessoal identificado`, a Taliya nao aplica sozinha: monta um pedido de aprovacao para humano autorizado.
4. Pedido de aprovacao: Monta a aprovacao para aprovar cuidado por saude ou evento pessoal, mostrando evento foi identificado; visibilidade esta definida; dono do caso foi atribuido; nenhum contato automatico sera feito sem revisao.
5. Fim: Saude ou evento pessoal vira aprovacao com visibilidade, dono e cuidado proposto. Se aprovado, apenas a acao permitida segue; se houver sigilo ou dado incompleto, fica com humano.

**Limite Do Agente**

Nao expoe informacao de saude ou evento pessoal.

**Humano/Aprovacao/Fallback**

- Chama humano quando: informacao e sensivel ou incompleta; responsavel adequado nao esta claro; acao proposta pode expor dado privado; aluno pede sigilo; aprovacao vence ou permissao bloqueia.
- Pede aprovacao quando: No cenario principal, antes da acao principal.
- Fallback do teste: Se o teste cair em `Aprovacao vence`, Mantem caso restrito.

**Agente De Configuracao**

Neste teste, a Taliya monta a aprovacao de Saude/evento pessoal e nao aplica a mudanca sozinha. Se aparecer `Aluno pediu sigilo` ou `Dado incompleto`, o caso fica com a equipe.

#### Segmentacao risco

- ID interno: `E12`.
- Modo padrao: `Autonomo com aprovacao`.
- Visual central: `Pedido de aprovacao`.
- Usa celular: `nao`.

**Cenarios**

- `Segmento definido`: Monta aprovacao de segmentacao.
- `Volume alto`: Pede revisao.
- `Dado sensivel`: Bloqueia uso.
- `Aprovacao vence`: Nao executa acao.

**Visual Do Caso**

card de aprovacao com dados, impacto, decisao pendente e efeito se aprovado

**Execucao Do Teste**

1. Inicio: O fluxo comeca quando o studio quer usar segmentacao de risco para acao operacional.
2. Checagens: segmento foi definido; acao permitida foi escolhida; dados usados foram listados; responsavel esta definido; aprovador esta definido.
3. Decisao: No cenario `Segmento definido`, a Taliya nao aplica sozinha: monta um pedido de aprovacao para humano autorizado.
4. Pedido de aprovacao: Monta a aprovacao para aprovar segmentacao de risco, mostrando segmento foi definido; acao permitida foi escolhida; dados usados foram listados; responsavel esta definido.
5. Fim: A segmentacao de risco vira aprovacao com dados usados, alunos afetados e acao permitida. Se aprovada, a acao segue; se usar dado sensivel ou volume alto, fica bloqueada.

**Limite Do Agente**

Nao executa segmentacao de risco sem aprovacao.

**Humano/Aprovacao/Fallback**

- Chama humano quando: segmento usa dado sensivel; acao nao esta permitida; alunos afetados sao muitos; risco de contato indevido aparece; aprovacao vence ou permissao bloqueia.
- Pede aprovacao quando: No cenario principal, antes da acao principal.
- Fallback do teste: Se o teste cair em `Aprovacao vence`, Nao executa acao.

**Agente De Configuracao**

Neste teste, a Taliya monta a aprovacao de Segmentacao risco e nao aplica a mudanca sozinha. Se aparecer `Volume alto` ou `Dado sensivel`, o caso fica com a equipe.

#### Reclamacao e recuperacao de confianca

- ID interno: `E13`.
- Modo padrao: `Autonomo com aprovacao`.
- Visual central: `Pedido de aprovacao`.
- Usa celular: `nao`.

**Cenarios**

- `Reclamacao registrada`: Monta aprovacao de recuperacao.
- `Envolve professor`: Chama responsavel.
- `Proposta exige beneficio`: Exige aprovacao.
- `Aprovacao vence`: Mantem caso aberto.

**Visual Do Caso**

card de aprovacao com dados, impacto, decisao pendente e efeito se aprovado

**Execucao Do Teste**

1. Inicio: O fluxo comeca quando uma reclamacao precisa de recuperacao de confianca.
2. Checagens: reclamacao foi registrada; dono do caso esta definido; automacoes foram pausadas; resumo e proposta foram preparados; aprovador esta definido.
3. Decisao: No cenario `Reclamacao registrada`, a Taliya nao aplica sozinha: monta um pedido de aprovacao para humano autorizado.
4. Pedido de aprovacao: Monta a aprovacao para aprovar recuperacao de reclamacao, mostrando reclamacao foi registrada; dono do caso esta definido; automacoes foram pausadas; resumo e proposta foram preparados.
5. Fim: A reclamacao vira aprovacao com resumo, dono, proposta e automacoes pausadas. Se aprovada, a recuperacao segue; se envolver professor, saude, financeiro ou beneficio, fica com responsavel.

**Limite Do Agente**

Nao oferece beneficio nem resposta de recuperacao sem aprovacao.

**Humano/Aprovacao/Fallback**

- Chama humano quando: reclamacao envolve professor, saude ou financeiro; aluno esta irritado ou pede cancelamento; proposta exige beneficio; risco reputacional alto; aprovacao vence ou permissao bloqueia.
- Pede aprovacao quando: No cenario principal, antes da acao principal.
- Fallback do teste: Se o teste cair em `Aprovacao vence`, Mantem caso aberto.

**Agente De Configuracao**

Neste teste, a Taliya monta a aprovacao de Reclamacao e recuperacao de confianca e nao aplica a mudanca sozinha. Se aparecer `Envolve professor` ou `Proposta exige beneficio`, o caso fica com a equipe.


## Agente: Gestao/Governanca


### Rotina: Comando operacional

#### Prioridades dia

- ID interno: `F1`.
- Modo padrao: `Autonomo`.
- Visual central: `Hoje/prioridades`.
- Usa celular: `nao`.

**Cenarios**

- `Resumo diario pronto`: Monta prioridades do dia.
- `Fonte critica falhou`: Marca pendencia.
- `Incidente critico`: Destaca alerta.
- `Permissao bloqueia`: Nao mostra fonte restrita.

**Visual Do Caso**

lista operacional de prioridades do dia com alertas e origem

**Execucao Do Teste**

1. Inicio: O fluxo comeca quando chega o horario de montar as prioridades operacionais do dia.
2. Checagens: fontes operacionais estao atualizadas; horario do resumo chegou; responsavel esta definido; tarefas e aprovacoes foram consolidadas; nada critico impede leitura.
3. Decisao: No cenario `Resumo diario pronto`, a Taliya conclui sem equipe porque as checagens obrigatorias passam.
4. Acao: Conclui a acao permitida: montar prioridades do dia.
5. Fim: As prioridades do dia aparecem em Hoje com tarefas, aprovacoes e alertas ordenados. Se fonte critica falhar ou dado estiver desatualizado, o resumo marca pendencia.

**Limite Do Agente**

Nao mostra prioridade baseada em fonte falha, incidente critico ou permissao restrita.

**Humano/Aprovacao/Fallback**

- Chama humano quando: Nao chama humano no cenario principal; se cair em `Permissao bloqueia`, aplica fallback: Nao mostra fonte restrita.
- Pede aprovacao quando: Nao pede aprovacao no cenario principal; se houver bloqueio, aplica o fallback definido.
- Fallback do teste: Se o teste cair em `Permissao bloqueia`, Nao mostra fonte restrita.

**Agente De Configuracao**

Neste teste, a Taliya conclui Prioridades dia quando as checagens passam. Se aparecer `Permissao bloqueia`, ela para e cria pendencia.

#### Dinheiro na mesa

- ID interno: `F2`.
- Modo padrao: `Autonomo com excecoes`.
- Visual central: `Dinheiro na mesa`.
- Usa celular: `nao`.

**Cenarios**

- `Oportunidade clara`: Abre proxima acao financeira.
- `Valor incerto`: Cria tarefa.
- `Disputa aberta`: Nao sugere cobranca.
- `Responsavel ausente`: Mantem pendente.

**Visual Do Caso**

lista de oportunidades financeiras com responsavel e proxima acao

**Execucao Do Teste**

1. Inicio: O fluxo comeca quando o CRM identifica oportunidade financeira parada ou dinheiro na mesa.
2. Checagens: oportunidade financeira foi detectada; frequencia do alerta permite envio; responsavel esta definido; acao sugerida nao altera financeiro sozinha; dados financeiros estao disponiveis.
3. Decisao: No cenario `Oportunidade clara`, a Taliya segue sem equipe porque nenhuma excecao foi encontrada.
4. Acao: Executa o caso valido: identificar dinheiro na mesa e abrir proxima acao.
5. Fim: A oportunidade financeira vira proxima acao para responsavel sem alterar dinheiro sozinha. Se valor, disputa, desconto ou responsavel nao fecharem, fica tarefa.

**Limite Do Agente**

Nao altera financeiro nem cobra; abre proxima acao para responsavel.

**Humano/Aprovacao/Fallback**

- Chama humano quando: valor esta incerto; caso depende de acordo ou desconto; movimentacao esta em disputa; responsavel nao existe; permissao ou cota bloqueia analise.
- Pede aprovacao quando: Nao pede aprovacao no cenario principal; nas excecoes, chama humano em vez de aprovar automaticamente.
- Fallback do teste: Se o teste cair em `Responsavel ausente`, Mantem pendente.

**Agente De Configuracao**

Neste teste, a Taliya executa Dinheiro na mesa apenas no cenario valido. Se aparecer `Valor incerto` ou `Disputa aberta`, chama a equipe.

#### Fila humana

- ID interno: `F3`.
- Modo padrao: `Autonomo`.
- Visual central: `Fila humana`.
- Usa celular: `nao`.

**Cenarios**

- `Fila com itens`: Ordena prioridades humanas.
- `Item sem dono`: Cria alerta.
- `Aprovacao vencida`: Sobe prioridade.
- `Incidente aberto`: Marca bloqueio.

**Visual Do Caso**

fila de tarefas, aprovacoes e casos humanos ordenados por prioridade

**Execucao Do Teste**

1. Inicio: O fluxo comeca quando ha tarefas, aprovacoes ou casos humanos acumulados.
2. Checagens: itens humanos foram encontrados; filas estao configuradas; prioridade foi calculada; responsaveis existem; nenhum item exige permissao ausente.
3. Decisao: No cenario `Fila com itens`, a Taliya conclui sem equipe porque as checagens obrigatorias passam.
4. Acao: Conclui a acao permitida: organizar fila humana e prioridades.
5. Fim: A fila humana fica ordenada por prioridade, dono e prazo. Se item sem dono, aprovacao vencida ou incidente aparecer, a operacao recebe alerta.

**Limite Do Agente**

Nao resolve itens da fila; ordena, destaca bloqueios e alerta responsaveis.

**Humano/Aprovacao/Fallback**

- Chama humano quando: Nao chama humano no cenario principal; se cair em `Incidente aberto`, aplica fallback: Marca bloqueio.
- Pede aprovacao quando: Nao pede aprovacao no cenario principal; se houver bloqueio, aplica o fallback definido.
- Fallback do teste: Se o teste cair em `Incidente aberto`, Marca bloqueio.

**Agente De Configuracao**

Neste teste, a Taliya conclui Fila humana quando as checagens passam. Se aparecer `Incidente aberto`, ela para e cria pendencia.

#### Gargalos

- ID interno: `F4`.
- Modo padrao: `Autonomo com excecoes`.
- Visual central: `Gargalo operacional`.
- Usa celular: `nao`.

**Cenarios**

- `Gargalo detectado`: Cria alerta operacional.
- `Dado incompleto`: Pede investigacao.
- `Toca financeiro/grade`: Chama responsavel.
- `Permissao bloqueia`: Oculta detalhe restrito.

**Visual Do Caso**

painel de indicador, causa provavel e responsavel pela investigacao

**Execucao Do Teste**

1. Inicio: O fluxo comeca quando indicadores mostram gargalo operacional.
2. Checagens: metricas foram atualizadas; frequencia do alerta permite analise; tipo de alerta esta definido; responsavel esta atribuido; acao sugerida e operacional.
3. Decisao: No cenario `Gargalo detectado`, a Taliya segue sem equipe porque nenhuma excecao foi encontrada.
4. Acao: Executa o caso valido: detectar gargalos operacionais.
5. Fim: O gargalo operacional vira alerta com metrica, causa provavel e responsavel. Se tocar financeiro, grade, incidente ou dado incompleto, vira investigacao humana.

**Limite Do Agente**

Nao corrige gargalo; aponta causa provavel e abre investigacao.

**Humano/Aprovacao/Fallback**

- Chama humano quando: dado esta incompleto; gargalo envolve financeiro, grade ou incidente; alerta e critico; responsavel nao definido; permissao ou cota bloqueia analise.
- Pede aprovacao quando: Nao pede aprovacao no cenario principal; nas excecoes, chama humano em vez de aprovar automaticamente.
- Fallback do teste: Se o teste cair em `Permissao bloqueia`, Oculta detalhe restrito.

**Agente De Configuracao**

Neste teste, a Taliya executa Gargalos apenas no cenario valido. Se aparecer `Dado incompleto` ou `Toca financeiro/grade`, chama a equipe.

#### Resumo semanal

- ID interno: `F5`.
- Modo padrao: `Autonomo`.
- Visual central: `Resumo semanal`.
- Usa celular: `nao`.

**Cenarios**

- `Semana fechada`: Gera resumo semanal.
- `Fonte falhou`: Resumo fica pendente.
- `Destinatario sem permissao`: Nao envia.
- `Incidente critico`: Marca bloqueio.

**Visual Do Caso**

preview do resumo executivo com secoes e destinatarios internos

**Execucao Do Teste**

1. Inicio: O fluxo comeca quando a semana fecha e o studio precisa de resumo executivo.
2. Checagens: periodo da semana fechou; secoes do resumo estao configuradas; destinatarios internos estao definidos; dados principais estao atualizados; nenhum incidente impede resumo.
3. Decisao: No cenario `Semana fechada`, a Taliya conclui sem equipe porque as checagens obrigatorias passam.
4. Acao: Conclui a acao permitida: gerar resumo semanal.
5. Fim: O resumo semanal e enviado/gerado para destinatarios permitidos com secoes configuradas. Se fonte, permissao ou incidente critico falhar, o resumo fica pendente.

**Limite Do Agente**

Nao envia resumo se fonte, permissao ou incidente critico falhar.

**Humano/Aprovacao/Fallback**

- Chama humano quando: Nao chama humano no cenario principal; se cair em `Incidente critico`, aplica fallback: Marca bloqueio.
- Pede aprovacao quando: Nao pede aprovacao no cenario principal; se houver bloqueio, aplica o fallback definido.
- Fallback do teste: Se o teste cair em `Incidente critico`, Marca bloqueio.

**Agente De Configuracao**

Neste teste, a Taliya conclui Resumo semanal quando as checagens passam. Se aparecer `Incidente critico`, ela para e cria pendencia.

#### Qualidade dados

- ID interno: `F6`.
- Modo padrao: `Autonomo com excecoes`.
- Visual central: `Qualidade de dados`.
- Usa celular: `nao`.

**Cenarios**

- `Duplicidade encontrada`: Abre tarefa de correcao.
- `Fusao sensivel`: Chama revisao.
- `Alto volume`: Cria lote de tarefas.
- `Permissao bloqueia`: Nao altera dado.

**Visual Do Caso**

lista de duplicidades, campos ausentes e tarefas de correcao

**Execucao Do Teste**

1. Inicio: O fluxo comeca quando o CRM detecta dado incompleto, duplicado ou inconsistente.
2. Checagens: tipo de dado a revisar pertence aos campos monitorados; duplicidade ou lacuna foi detectada; prioridade foi calculada; responsavel esta definido; correcao automatica nao altera dado sensivel.
3. Decisao: No cenario `Duplicidade encontrada`, a Taliya segue sem equipe porque nenhuma excecao foi encontrada.
4. Acao: Executa o caso valido: detectar qualidade de dados e abrir tarefa de correcao.
5. Fim: A falha de qualidade de dados abre tarefa de correcao com prioridade e campo afetado. Se envolver fusao, historico protegido ou alto volume, vai para revisao.

**Limite Do Agente**

Nao mescla nem corrige dado sensivel automaticamente.

**Humano/Aprovacao/Fallback**

- Chama humano quando: correcao pode fundir cadastros; dado envolve historico protegido; conflito nao tem dono claro; volume e alto demais; permissao ou cota bloqueia analise.
- Pede aprovacao quando: Nao pede aprovacao no cenario principal; nas excecoes, chama humano em vez de aprovar automaticamente.
- Fallback do teste: Se o teste cair em `Permissao bloqueia`, Nao altera dado.

**Agente De Configuracao**

Neste teste, a Taliya executa Qualidade dados apenas no cenario valido. Se aparecer `Fusao sensivel` ou `Alto volume`, chama a equipe.


### Rotina: Governanca de agentes

#### Creditos/limites

- ID interno: `F7`.
- Modo padrao: `Autonomo`.
- Visual central: `Uso/cotas`.
- Usa celular: `nao`.

**Cenarios**

- `Cota em alerta`: Registra alerta de uso.
- `Billing diverge`: Chama admin.
- `Upgrade necessario`: Cria acao para dono.
- `Permissao bloqueia`: Nao mostra detalhe.

**Visual Do Caso**

cartao de cota, alertas 70/90/100 e acao para dono/admin

**Execucao Do Teste**

1. Inicio: O fluxo comeca quando uso, creditos, limites ou cotas precisam ser monitorados.
2. Checagens: uso foi atualizado; alertas 70/90/100 estao configurados; responsavel esta definido; limite comercial foi lido do billing; mensagem interna esta pronta.
3. Decisao: No cenario `Cota em alerta`, a Taliya conclui sem equipe porque as checagens obrigatorias passam.
4. Acao: Conclui a acao permitida: monitorar creditos, limites e cotas.
5. Fim: Uso, creditos e cotas recebem alerta nos limites configurados e aparecem em Uso/Cotas. Se billing divergir ou upgrade/add-on exigir decisao, vai para admin.

**Limite Do Agente**

Nao compra pacote, altera plano ou libera cota; alerta dono/admin.

**Humano/Aprovacao/Fallback**

- Chama humano quando: Nao chama humano no cenario principal; se cair em `Permissao bloqueia`, aplica fallback: Nao mostra detalhe.
- Pede aprovacao quando: Nao pede aprovacao no cenario principal; se houver bloqueio, aplica o fallback definido.
- Fallback do teste: Se o teste cair em `Permissao bloqueia`, Nao mostra detalhe.

**Agente De Configuracao**

Neste teste, a Taliya conclui Creditos/limites quando as checagens passam. Se aparecer `Permissao bloqueia`, ela para e cria pendencia.

#### Performance

- ID interno: `F8`.
- Modo padrao: `Autonomo com excecoes`.
- Visual central: `Performance de agentes`.
- Usa celular: `nao`.

**Cenarios**

- `Performance normal`: Gera relatorio de agentes.
- `Queda forte`: Abre investigacao.
- `Amostra insuficiente`: Marca incerteza.
- `Incidente correlacionado`: Vincula incidente.

**Visual Do Caso**

relatorio de indicadores, queda detectada e origem da investigacao

**Execucao Do Teste**

1. Inicio: O fluxo comeca quando indicadores de agentes precisam ser acompanhados.
2. Checagens: metricas foram coletadas; frequencia permite novo relatorio; responsavel esta definido; indicadores configurados existem; acao sugerida nao altera politica sozinha.
3. Decisao: No cenario `Performance normal`, a Taliya segue sem equipe porque nenhuma excecao foi encontrada.
4. Acao: Executa o caso valido: monitorar performance dos agentes.
5. Fim: A performance dos agentes vira relatorio ou alerta com indicador afetado. Se queda forte, amostra insuficiente ou incidente correlacionado aparecer, abre investigacao.

**Limite Do Agente**

Nao muda politica de agente; abre investigacao quando houver queda ou amostra fraca.

**Humano/Aprovacao/Fallback**

- Chama humano quando: queda forte de performance; falha ou incidente correlacionado; amostra insuficiente; acao exige mudar fluxo ou politica; permissao ou cota bloqueia analise.
- Pede aprovacao quando: Nao pede aprovacao no cenario principal; nas excecoes, chama humano em vez de aprovar automaticamente.
- Fallback do teste: Se o teste cair em `Incidente correlacionado`, Vincula incidente.

**Agente De Configuracao**

Neste teste, a Taliya executa Performance apenas no cenario valido. Se aparecer `Queda forte` ou `Amostra insuficiente`, chama a equipe.

#### Permissoes/auditoria

- ID interno: `F9`.
- Modo padrao: `Autonomo com aprovacao`.
- Visual central: `Pedido de aprovacao`.
- Usa celular: `nao`.

**Cenarios**

- `Evento de auditoria`: Monta aprovacao de revisao.
- `Suspeita de acesso`: Escala responsavel.
- `Mudanca de permissao`: Exige aprovacao.
- `Aprovacao vence`: Mantem permissao atual.

**Visual Do Caso**

card de aprovacao com dados, impacto, decisao pendente e efeito se aprovado

**Execucao Do Teste**

1. Inicio: O fluxo comeca quando evento de permissao ou auditoria exige revisao.
2. Checagens: evento de auditoria foi identificado; tipo de evento esta dentro do escopo; responsavel esta definido; impacto foi resumido; aprovador esta definido.
3. Decisao: No cenario `Evento de auditoria`, a Taliya nao aplica sozinha: monta um pedido de aprovacao para humano autorizado.
4. Pedido de aprovacao: Monta a aprovacao para aprovar revisao de permissao ou auditoria, mostrando evento de auditoria foi identificado; tipo de evento esta dentro do escopo; responsavel esta definido; impacto foi resumido.
5. Fim: Permissao ou evento de auditoria vira aprovacao com impacto e responsavel. Se houver suspeita de acesso indevido ou mudanca de permissao, nao aplica sem aprovacao.

**Limite Do Agente**

Nao muda permissao sem aprovacao.

**Humano/Aprovacao/Fallback**

- Chama humano quando: evento e critico; mudanca de permissao seria necessaria; ha suspeita de acesso indevido; dados de auditoria incompletos; aprovacao vence ou permissao bloqueia.
- Pede aprovacao quando: No cenario principal, antes da acao principal.
- Fallback do teste: Se o teste cair em `Aprovacao vence`, Mantem permissao atual.

**Agente De Configuracao**

Neste teste, a Taliya monta a aprovacao de Permissoes/auditoria e nao aplica a mudanca sozinha. Se aparecer `Suspeita de acesso` ou `Mudanca de permissao`, o caso fica com a equipe.


### Rotina: Comando operacional

#### Capacidade/crescimento

- ID interno: `F10`.
- Modo padrao: `Autonomo com excecoes`.
- Visual central: `Capacidade/crescimento`.
- Usa celular: `nao`.

**Cenarios**

- `Capacidade perto do limite`: Cria alerta de ocupacao.
- `Exige nova turma`: Chama gestao.
- `Impacto financeiro`: Pede decisao.
- `Dados de agenda conflitam`: Bloqueia sugestao.

**Visual Do Caso**

ocupacao por turma/horario com limite, alerta e acao sugerida

**Execucao Do Teste**

1. Inicio: O fluxo comeca quando ocupacao, capacidade ou crescimento chegam perto de limite relevante.
2. Checagens: ocupacao foi calculada; limite de alerta foi atingido ou esta proximo; responsavel esta definido; acao sugerida nao altera grade sozinha; dados de agenda estao atualizados.
3. Decisao: No cenario `Capacidade perto do limite`, a Taliya segue sem equipe porque nenhuma excecao foi encontrada.
4. Acao: Executa o caso valido: detectar capacidade e crescimento.
5. Fim: Capacidade e crescimento viram alerta com ocupacao, limite e acao sugerida. Se exigir nova turma, horario ou impacto financeiro, fica para decisao.

**Limite Do Agente**

Nao cria turma, horario ou sala; alerta gestao sobre capacidade.

**Humano/Aprovacao/Fallback**

- Chama humano quando: capacidade ultrapassa limite; crescimento exige nova turma ou horario; dados de agenda conflitam; impacto financeiro aparece; permissao ou cota bloqueia analise.
- Pede aprovacao quando: Nao pede aprovacao no cenario principal; nas excecoes, chama humano em vez de aprovar automaticamente.
- Fallback do teste: Se o teste cair em `Dados de agenda conflitam`, Bloqueia sugestao.

**Agente De Configuracao**

Neste teste, a Taliya executa Capacidade/crescimento apenas no cenario valido. Se aparecer `Exige nova turma` ou `Impacto financeiro`, chama a equipe.


### Rotina: Integracoes e importacao

#### Falhas/webhooks

- ID interno: `F11`.
- Modo padrao: `Autonomo com excecoes`.
- Visual central: `Logs de integracao`.
- Usa celular: `nao`.

**Cenarios**

- `Webhook falhou com retry seguro`: Executa retry permitido.
- `Risco de duplicar efeito`: Nao reprocessa.
- `Provedor indisponivel`: Abre incidente.
- `Limite bloqueia`: Mantem falha pendente.

**Visual Do Caso**

linha de falha tecnica com retry seguro, provedor e severidade

**Execucao Do Teste**

1. Inicio: O fluxo comeca quando integracao, webhook ou tentativa tecnica falha.
2. Checagens: falha tecnica foi identificada; severidade esta definida; retry seguro e permitido; responsavel esta atribuido; log tecnico esta disponivel.
3. Decisao: No cenario `Webhook falhou com retry seguro`, a Taliya segue sem equipe porque nenhuma excecao foi encontrada.
4. Acao: Executa o caso valido: tratar falhas, webhooks e retries seguros.
5. Fim: Falha tecnica ou webhook recebe retry seguro quando permitido e registro no log da integracao. Se houver risco de duplicar efeito, provedor instavel ou severidade alta, vai para incidente.

**Limite Do Agente**

Nao reprocessa quando houver risco de duplicidade ou provedor indisponivel.

**Humano/Aprovacao/Fallback**

- Chama humano quando: retry pode duplicar efeito; falha persiste; severidade e alta; provedor esta indisponivel; permissao ou limite bloqueia mitigacao.
- Pede aprovacao quando: Nao pede aprovacao no cenario principal; nas excecoes, chama humano em vez de aprovar automaticamente.
- Fallback do teste: Se o teste cair em `Limite bloqueia`, Mantem falha pendente.

**Agente De Configuracao**

Neste teste, a Taliya executa Falhas/webhooks apenas no cenario valido. Se aparecer `Risco de duplicar efeito` ou `Provedor indisponivel`, chama a equipe.

#### Importacao/migracao

- ID interno: `F12`.
- Modo padrao: `Autonomo com aprovacao`.
- Visual central: `Pedido de aprovacao`.
- Usa celular: `nao`.

**Cenarios**

- `Lote validado`: Monta aprovacao de importacao.
- `Duplicidades aparecem`: Bloqueia lote.
- `Rollback incerto`: Pede revisao.
- `Aprovacao vence`: Nao importa.

**Visual Do Caso**

card de aprovacao com dados, impacto, decisao pendente e efeito se aprovado

**Execucao Do Teste**

1. Inicio: O fluxo comeca quando uma importacao ou migracao precisa ser validada.
2. Checagens: lote foi identificado; amostra foi validada; impacto em dados foi resumido; responsavel esta definido; aprovador esta definido.
3. Decisao: No cenario `Lote validado`, a Taliya nao aplica sozinha: monta um pedido de aprovacao para humano autorizado.
4. Pedido de aprovacao: Monta a aprovacao para aprovar importacao ou migracao, mostrando lote foi identificado; amostra foi validada; impacto em dados foi resumido; responsavel esta definido.
5. Fim: Importacao ou migracao vira aprovacao com amostra, conflitos, impacto e rollback. Se aprovada, o lote segue; se houver duplicidade ou campo faltando, fica bloqueado.

**Limite Do Agente**

Nao importa lote antes da aprovacao.

**Humano/Aprovacao/Fallback**

- Chama humano quando: duplicidades ou conflitos aparecem; lote e grande demais; campos obrigatorios faltam; rollback nao esta claro; aprovacao vence ou permissao bloqueia.
- Pede aprovacao quando: No cenario principal, antes da acao principal.
- Fallback do teste: Se o teste cair em `Aprovacao vence`, Nao importa.

**Agente De Configuracao**

Neste teste, a Taliya monta a aprovacao de Importacao/migracao e nao aplica a mudanca sozinha. Se aparecer `Duplicidades aparecem` ou `Rollback incerto`, o caso fica com a equipe.


### Rotina: Governanca de agentes

#### Teste de fluxo

- ID interno: `F13`.
- Modo padrao: `Autonomo`.
- Visual central: `Simulador de fluxo`.
- Usa celular: `nao`.

**Cenarios**

- `Teste seguro escolhido`: Roda simulacao sem publicar.
- `Dado sensivel real`: Bloqueia teste.
- `Preflight falha`: Mostra pendencia.
- `Tentativa de executar real`: Para imediatamente.

**Visual Do Caso**

painel de teste seguro mostrando que nenhuma acao real sera publicada

**Execucao Do Teste**

1. Inicio: O fluxo comeca quando alguem testa um fluxo antes de publicar ou alterar operacao.
2. Checagens: cenario de teste foi escolhido; dados de exemplo estao disponiveis; fluxo nao publica acao real; responsavel por revisao esta definido; resultado pode ser salvo.
3. Decisao: No cenario `Teste seguro escolhido`, a Taliya conclui sem equipe porque as checagens obrigatorias passam.
4. Acao: Conclui a acao permitida: rodar teste de fluxo em simulacao.
5. Fim: O teste roda em simulacao, mostra caminho do fluxo e nao publica acao real. Se usar dado sensivel, falhar preflight ou tentar executar de verdade, o teste para.

**Limite Do Agente**

Nao publica nem executa acao real durante a simulacao.

**Humano/Aprovacao/Fallback**

- Chama humano quando: Nao chama humano no cenario principal; se cair em `Tentativa de executar real`, aplica fallback: Para imediatamente.
- Pede aprovacao quando: Nao pede aprovacao no cenario principal; se houver bloqueio, aplica o fallback definido.
- Fallback do teste: Se o teste cair em `Tentativa de executar real`, Para imediatamente.

**Agente De Configuracao**

Neste teste, a Taliya conclui Teste de fluxo quando as checagens passam. Se aparecer `Tentativa de executar real`, ela para e cria pendencia.

#### Incidente de automacao e correcao operacional

- ID interno: `F14`.
- Modo padrao: `Autonomo com excecoes`.
- Visual central: `Incidente/execucao`.
- Usa celular: `nao`.

**Cenarios**

- `Incidente simples`: Pausa ou mitiga fluxo permitido.
- `Afeta varios fluxos`: Abre incidente humano.
- `Exige rollback`: Chama responsavel.
- `Integracao falha`: Vincula log tecnico.

**Visual Do Caso**

cartao de incidente com execucao relacionada, pausa e mitigacao

**Execucao Do Teste**

1. Inicio: O fluxo comeca quando uma automacao falha, gera incidente ou precisa de correcao operacional.
2. Checagens: incidente foi detectado; severidade esta definida; auto-pausa e permitida para o fluxo; responsavel esta atribuido; execucao relacionada foi encontrada.
3. Decisao: No cenario `Incidente simples`, a Taliya segue sem equipe porque nenhuma excecao foi encontrada.
4. Acao: Executa o caso valido: tratar incidente de automacao e correcao operacional.
5. Fim: O incidente de automacao pausa ou mitiga o fluxo quando permitido e abre a execucao relacionada. Se afetar varios fluxos, exigir rollback ou depender de integracao, vai para incidente humano.

**Limite Do Agente**

Nao faz rollback amplo; pausa ou mitiga somente o que estiver permitido.

**Humano/Aprovacao/Fallback**

- Chama humano quando: incidente afeta varios fluxos; auto-pausa nao e permitida; correcao exige rollback; falha envolve integracao externa; permissao bloqueia mitigacao.
- Pede aprovacao quando: Nao pede aprovacao no cenario principal; nas excecoes, chama humano em vez de aprovar automaticamente.
- Fallback do teste: Se o teste cair em `Integracao falha`, Vincula log tecnico.

**Agente De Configuracao**

Neste teste, a Taliya executa Incidente de automacao e correcao operacional apenas no cenario valido. Se aparecer `Afeta varios fluxos` ou `Exige rollback`, chama a equipe.

#### Mudanca de politica ou regra operacional

- ID interno: `F15`.
- Modo padrao: `Autonomo com aprovacao`.
- Visual central: `Pedido de aprovacao`.
- Usa celular: `nao`.

**Cenarios**

- `Regra nova simulada`: Monta aprovacao de politica.
- `Impacto em muitos fluxos`: Pede revisao.
- `Vigencia curta`: Bloqueia publicacao.
- `Aprovacao vence`: Mantem politica atual.

**Visual Do Caso**

card de aprovacao com dados, impacto, decisao pendente e efeito se aprovado

**Execucao Do Teste**

1. Inicio: O fluxo comeca quando politica, regra ou comportamento operacional precisa mudar.
2. Checagens: politica ou regra foi identificada; data de vigencia esta definida; simulacao de impacto foi feita; comunicacao interna esta pronta; aprovador esta definido.
3. Decisao: No cenario `Regra nova simulada`, a Taliya nao aplica sozinha: monta um pedido de aprovacao para humano autorizado.
4. Pedido de aprovacao: Monta a aprovacao para aprovar mudanca de politica ou regra, mostrando politica ou regra foi identificada; data de vigencia esta definida; simulacao de impacto foi feita; comunicacao interna esta pronta.
5. Fim: Mudanca de politica vira aprovacao com simulacao, vigencia e comunicacao. Se aprovada, a nova versao fica pronta para publicar; se houver conflito, volta para revisao.

**Limite Do Agente**

Nao publica politica antes da aprovacao.

**Humano/Aprovacao/Fallback**

- Chama humano quando: impacto afeta muitos fluxos; simulacao mostra conflito; vigencia e curta demais; comunicacao nao foi revisada; aprovacao vence ou permissao bloqueia.
- Pede aprovacao quando: No cenario principal, antes da acao principal.
- Fallback do teste: Se o teste cair em `Aprovacao vence`, Mantem politica atual.

**Agente De Configuracao**

Neste teste, a Taliya monta a aprovacao de Mudanca de politica ou regra operacional e nao aplica a mudanca sozinha. Se aparecer `Impacto em muitos fluxos` ou `Vigencia curta`, o caso fica com a equipe.


## Agente: Historico/Evolucao


### Rotina: Aula com contexto

#### Contexto antes aula

- ID interno: `G1`.
- Modo padrao: `Autonomo com excecoes`.
- Visual central: `Celular/conversa`.
- Usa celular: `sim`.

**Cenarios**

- `Contexto permitido`: Envia resumo ao professor.
- `Restricao sensivel`: Remove dado e chama revisao.
- `Professor sem permissao`: Nao envia resumo.
- `Aula alterada`: Atualiza contexto.

**Visual Do Caso**

celular com conversa simulada e cartao interno mostrando o resultado do fluxo

**Execucao Do Teste**

1. Inicio: O fluxo comeca antes de uma aula, quando o professor precisa de contexto permitido.
2. Checagens: aula e professor foram identificados; alunos da aula foram listados; visibilidade do historico permite uso; contexto nao inclui dado protegido indevido; professor pode receber o resumo.
3. Decisao: No cenario `Contexto permitido`, a Taliya segue sem equipe porque nenhuma excecao foi encontrada.
4. Acao: Executa o caso valido: preparar contexto antes da aula para professor.
5. Fim: O professor recebe contexto permitido antes da aula sem dado protegido indevido. Se houver restricao sensivel, permissao faltando ou aula alterada, o resumo nao sai.

**Limite Do Agente**

Nao expoe dado protegido ao professor.

**Humano/Aprovacao/Fallback**

- Chama humano quando: aluno tem restricao sensivel; professor sem permissao para dado; historico esta incompleto; aula foi alterada; permissao ou cota bloqueia resumo.
- Pede aprovacao quando: Nao pede aprovacao no cenario principal; nas excecoes, chama humano em vez de aprovar automaticamente.
- Fallback do teste: Se o teste cair em `Aula alterada`, Atualiza contexto.

**Agente De Configuracao**

Neste teste, a Taliya executa Contexto antes aula apenas no cenario valido. Se aparecer `Restricao sensivel` ou `Professor sem permissao`, chama a equipe.

#### Observacao pos-aula

- ID interno: `G2`.
- Modo padrao: `Autonomo com excecoes`.
- Visual central: `Celular/conversa`.
- Usa celular: `sim`.

**Cenarios**

- `Aula terminou`: Lembra professor e organiza nota.
- `Nota sensivel`: Vai para revisao.
- `Professor sem permissao`: Nao aceita nota.
- `Canal bloqueia`: Cria pendencia.

**Visual Do Caso**

celular com conversa simulada e cartao interno mostrando o resultado do fluxo

**Execucao Do Teste**

1. Inicio: O fluxo comeca depois da aula, quando uma observacao precisa ser registrada.
2. Checagens: aula terminou; professor foi identificado; tipos de nota permitidos estao definidos; lembrete esta dentro do horario; nota ainda nao foi registrada.
3. Decisao: No cenario `Aula terminou`, a Taliya segue sem equipe porque nenhuma excecao foi encontrada.
4. Acao: Executa o caso valido: lembrar e organizar observacao pos-aula.
5. Fim: Depois da aula, o professor recebe lembrete e a observacao permitida entra no historico. Se a nota envolver cuidado, restricao ou evento sensivel, vai para revisao.

**Limite Do Agente**

Nao aceita nota sensivel ou de professor sem permissao sem revisao.

**Humano/Aprovacao/Fallback**

- Chama humano quando: professor nao tem permissao; nota envolve restricao ou cuidado; aula nao foi fechada; aluno teve evento sensivel; canal, cota ou permissao bloqueia lembrete.
- Pede aprovacao quando: Nao pede aprovacao no cenario principal; nas excecoes, chama humano em vez de aprovar automaticamente.
- Fallback do teste: Se o teste cair em `Canal bloqueia`, Cria pendencia.

**Agente De Configuracao**

Neste teste, a Taliya executa Observacao pos-aula apenas no cenario valido. Se aparecer `Nota sensivel` ou `Professor sem permissao`, chama a equipe.


### Rotina: Historico protegido

#### Restricao/cuidado

- ID interno: `G3`.
- Modo padrao: `Autonomo com aprovacao`.
- Visual central: `Pedido de aprovacao`.
- Usa celular: `nao`.

**Cenarios**

- `Restricao classificada`: Monta aprovacao de cuidado.
- `Visibilidade incerta`: Pede revisao.
- `Dado incompleto`: Mantem pendente.
- `Aprovacao vence`: Nao altera historico.

**Visual Do Caso**

card de aprovacao com dados, impacto, decisao pendente e efeito se aprovado

**Execucao Do Teste**

1. Inicio: O fluxo comeca quando restricao, cuidado ou informacao sensivel precisa ser revisada.
2. Checagens: aluno foi identificado; restricao ou cuidado foi classificado; visibilidade esta definida; dono do caso esta atribuido; aprovador esta definido.
3. Decisao: No cenario `Restricao classificada`, a Taliya nao aplica sozinha: monta um pedido de aprovacao para humano autorizado.
4. Pedido de aprovacao: Monta a aprovacao para aprovar restricao ou cuidado, mostrando aluno foi identificado; restricao ou cuidado foi classificado; visibilidade esta definida; dono do caso esta atribuido.
5. Fim: Restricao ou cuidado vira aprovacao com aluno, visibilidade, dono e acao proposta. Se aprovada, o historico protegido e atualizado; se houver dado incompleto, fica pendente.

**Limite Do Agente**

Nao altera historico protegido antes da aprovacao.

**Humano/Aprovacao/Fallback**

- Chama humano quando: informacao e sensivel ou incompleta; visibilidade nao esta clara; acao pode expor dado privado; professor ou responsavel diverge; aprovacao vence ou permissao bloqueia.
- Pede aprovacao quando: No cenario principal, antes da acao principal.
- Fallback do teste: Se o teste cair em `Aprovacao vence`, Nao altera historico.

**Agente De Configuracao**

Neste teste, a Taliya monta a aprovacao de Restricao/cuidado e nao aplica a mudanca sozinha. Se aparecer `Visibilidade incerta` ou `Dado incompleto`, o caso fica com a equipe.


### Rotina: Aula com contexto

#### Objetivo/evolucao

- ID interno: `G4`.
- Modo padrao: `Autonomo com excecoes`.
- Visual central: `Historico do aluno`.
- Usa celular: `nao`.

**Cenarios**

- `Objetivo acompanhado`: Atualiza evolucao permitida.
- `Toca saude/restricao`: Chama revisao.
- `Professor sem permissao`: Oculta detalhe.
- `Historico conflita`: Cria tarefa.

**Visual Do Caso**

perfil do aluno com objetivo/evolucao permitida e proximo cuidado

**Execucao Do Teste**

1. Inicio: O fluxo comeca quando objetivo ou evolucao do aluno precisa ser acompanhado.
2. Checagens: aluno foi identificado; objetivo ou evolucao esta dentro dos tipos permitidos; frequencia de acompanhamento esta definida; professor ou responsavel esta atribuido; historico permitido esta disponivel.
3. Decisao: No cenario `Objetivo acompanhado`, a Taliya segue sem equipe porque nenhuma excecao foi encontrada.
4. Acao: Executa o caso valido: acompanhar objetivo e evolucao do aluno.
5. Fim: Objetivo ou evolucao fica acompanhado no historico permitido e gera proximo cuidado quando configurado. Se tocar saude, restricao ou permissao de professor, vai para revisao.

**Limite Do Agente**

Nao registra evolucao sensivel sem revisao.

**Humano/Aprovacao/Fallback**

- Chama humano quando: evolucao envolve saude ou restricao; professor sem permissao; dado historico esta conflitante; acao exige contato sensivel; permissao ou cota bloqueia resumo.
- Pede aprovacao quando: Nao pede aprovacao no cenario principal; nas excecoes, chama humano em vez de aprovar automaticamente.
- Fallback do teste: Se o teste cair em `Historico conflita`, Cria tarefa.

**Agente De Configuracao**

Neste teste, a Taliya executa Objetivo/evolucao apenas no cenario valido. Se aparecer `Toca saude/restricao` ou `Professor sem permissao`, chama a equipe.


### Rotina: Historico protegido

#### Contexto para agente

- ID interno: `G5`.
- Modo padrao: `Autonomo com aprovacao`.
- Visual central: `Pedido de aprovacao`.
- Usa celular: `nao`.

**Cenarios**

- `Escopo permitido`: Monta aprovacao de contexto para agente.
- `Escopo amplo`: Bloqueia liberacao.
- `Dado protegido`: Pede revisao.
- `Aprovacao vence`: Nao libera contexto.

**Visual Do Caso**

card de aprovacao com dados, impacto, decisao pendente e efeito se aprovado

**Execucao Do Teste**

1. Inicio: O fluxo comeca quando algum agente precisa de contexto de historico permitido.
2. Checagens: escopo de dados foi definido; dados permitidos foram listados; objetivo de uso esta claro; aprovador esta definido; nenhum dado protegido sera liberado sem aprovacao.
3. Decisao: No cenario `Escopo permitido`, a Taliya nao aplica sozinha: monta um pedido de aprovacao para humano autorizado.
4. Pedido de aprovacao: Monta a aprovacao para aprovar contexto para agente, mostrando escopo de dados foi definido; dados permitidos foram listados; objetivo de uso esta claro; aprovador esta definido.
5. Fim: O contexto para outro agente vira aprovacao com escopo, dados e finalidade. Se aprovado, o agente recebe apenas o permitido; se amplo ou protegido demais, fica bloqueado.

**Limite Do Agente**

Nao libera contexto para agente antes da aprovacao.

**Humano/Aprovacao/Fallback**

- Chama humano quando: escopo amplo demais; dados incluem historico protegido; objetivo de uso nao esta claro; politica de privacidade conflita; aprovacao vence ou permissao bloqueia.
- Pede aprovacao quando: No cenario principal, antes da acao principal.
- Fallback do teste: Se o teste cair em `Aprovacao vence`, Nao libera contexto.

**Agente De Configuracao**

Neste teste, a Taliya monta a aprovacao de Contexto para agente e nao aplica a mudanca sozinha. Se aparecer `Escopo amplo` ou `Dado protegido`, o caso fica com a equipe.

#### Documentos/anamnese

- ID interno: `G6`.
- Modo padrao: `Autonomo com aprovacao`.
- Visual central: `Pedido de aprovacao`.
- Usa celular: `nao`.

**Cenarios**

- `Documento identificado`: Monta aprovacao de documento.
- `Anamnese sensivel`: Chama revisao.
- `Arquivo nao permitido`: Bloqueia anexo.
- `Aprovacao vence`: Nao libera documento.

**Visual Do Caso**

card de aprovacao com dados, impacto, decisao pendente e efeito se aprovado

**Execucao Do Teste**

1. Inicio: O fluxo comeca quando documento, anamnese ou arquivo do aluno precisa de revisao.
2. Checagens: documento exigido foi identificado; aluno foi identificado; responsavel esta definido; visibilidade esta clara; aprovador esta definido.
3. Decisao: No cenario `Documento identificado`, a Taliya nao aplica sozinha: monta um pedido de aprovacao para humano autorizado.
4. Pedido de aprovacao: Monta a aprovacao para aprovar documento ou anamnese, mostrando documento exigido foi identificado; aluno foi identificado; responsavel esta definido; visibilidade esta clara.
5. Fim: Documento ou anamnese vira aprovacao com aluno, arquivo, visibilidade e responsavel. Se aprovado, fica disponivel no historico permitido; se sensivel/incompleto, vai para revisao.

**Limite Do Agente**

Nao libera documento/anamnese sem aprovacao.

**Humano/Aprovacao/Fallback**

- Chama humano quando: documento sensivel ou incompleto; anamnese exige revisao humana; arquivo nao e permitido; dados conflitam com historico; aprovacao vence ou permissao bloqueia.
- Pede aprovacao quando: No cenario principal, antes da acao principal.
- Fallback do teste: Se o teste cair em `Aprovacao vence`, Nao libera documento.

**Agente De Configuracao**

Neste teste, a Taliya monta a aprovacao de Documentos/anamnese e nao aplica a mudanca sozinha. Se aparecer `Anamnese sensivel` ou `Arquivo nao permitido`, o caso fica com a equipe.

#### Correcao historico

- ID interno: `G7`.
- Modo padrao: `Autonomo com aprovacao`.
- Visual central: `Pedido de aprovacao`.
- Usa celular: `nao`.

**Cenarios**

- `Correcao com motivo`: Monta aprovacao de historico.
- `Evento nao localizado`: Cria pendencia.
- `Dado protegido`: Exige revisao.
- `Aprovacao vence`: Nao corrige historico.

**Visual Do Caso**

card de aprovacao com dados, impacto, decisao pendente e efeito se aprovado

**Execucao Do Teste**

1. Inicio: O fluxo comeca quando alguem pede correcao de historico.
2. Checagens: evento historico foi identificado; motivo obrigatorio foi informado; valor anterior foi preservado; impacto da correcao foi mostrado; aprovador esta definido.
3. Decisao: No cenario `Correcao com motivo`, a Taliya nao aplica sozinha: monta um pedido de aprovacao para humano autorizado.
4. Pedido de aprovacao: Monta a aprovacao para aprovar correcao de historico, mostrando evento historico foi identificado; motivo obrigatorio foi informado; valor anterior foi preservado; impacto da correcao foi mostrado.
5. Fim: A correcao de historico vira aprovacao preservando valor anterior, motivo e impacto. Se aprovada, o historico muda com rastro; se houver divergencia, fica pendente.

**Limite Do Agente**

Nao corrige historico antes da aprovacao.

**Humano/Aprovacao/Fallback**

- Chama humano quando: motivo esta incompleto; correcao afeta dado protegido; professor ou aluno divergem; evento original nao pode ser localizado; aprovacao vence ou permissao bloqueia.
- Pede aprovacao quando: No cenario principal, antes da acao principal.
- Fallback do teste: Se o teste cair em `Aprovacao vence`, Nao corrige historico.

**Agente De Configuracao**

Neste teste, a Taliya monta a aprovacao de Correcao historico e nao aplica a mudanca sozinha. Se aparecer `Evento nao localizado` ou `Dado protegido`, o caso fica com a equipe.


### Rotina: Aula com contexto

#### Repasse entre professores

- ID interno: `G8`.
- Modo padrao: `Autonomo com excecoes`.
- Visual central: `Celular/conversa`.
- Usa celular: `sim`.

**Cenarios**

- `Repasse permitido`: Envia resumo ao professor destino.
- `Destino sem permissao`: Nao envia.
- `Resumo inclui dado protegido`: Chama revisao.
- `Contexto incompleto`: Cria pendencia.

**Visual Do Caso**

celular com conversa simulada e cartao interno mostrando o resultado do fluxo

**Execucao Do Teste**

1. Inicio: O fluxo comeca quando professor precisa repassar contexto para outro professor.
2. Checagens: professor origem e destino foram identificados; campos do resumo estao definidos; alunos ou aulas relacionados foram listados; visibilidade do historico permite repasse; mensagem interna esta pronta.
3. Decisao: No cenario `Repasse permitido`, a Taliya segue sem equipe porque nenhuma excecao foi encontrada.
4. Acao: Executa o caso valido: preparar repasse entre professores.
5. Fim: O repasse entre professores envia resumo permitido para o professor destino. Se incluir dado protegido, destino sem permissao ou contexto incompleto, o repasse para.

**Limite Do Agente**

Nao repassa dado protegido ou contexto para professor sem permissao.

**Humano/Aprovacao/Fallback**

- Chama humano quando: professor destino sem permissao; resumo inclui dado protegido; aula ou professor mudou; contexto esta incompleto; permissao ou cota bloqueia repasse.
- Pede aprovacao quando: Nao pede aprovacao no cenario principal; nas excecoes, chama humano em vez de aprovar automaticamente.
- Fallback do teste: Se o teste cair em `Contexto incompleto`, Cria pendencia.

**Agente De Configuracao**

Neste teste, a Taliya executa Repasse entre professores apenas no cenario valido. Se aparecer `Destino sem permissao` ou `Resumo inclui dado protegido`, chama a equipe.

#### Lembrete professor

- ID interno: `G9`.
- Modo padrao: `Autonomo`.
- Visual central: `Celular/conversa`.
- Usa celular: `sim`.

**Cenarios**

- `Lembrete no horario`: Envia lembrete ao professor.
- `Aula alterada`: Para envio.
- `Conteudo protegido`: Chama revisao.
- `Canal bloqueia`: Nao envia.

**Visual Do Caso**

celular com conversa simulada e cartao interno mostrando o resultado do fluxo

**Execucao Do Teste**

1. Inicio: O fluxo comeca quando professor precisa receber lembrete operacional.
2. Checagens: professor foi identificado; horario ou frequencia chegou; destino do lembrete esta definido; conteudo nao inclui dado protegido indevido; lembrete ainda nao foi enviado.
3. Decisao: No cenario `Lembrete no horario`, a Taliya conclui sem equipe porque as checagens obrigatorias passam.
4. Acao: Conclui a acao permitida: enviar lembrete para professor.
5. Fim: O lembrete do professor e enviado no horario/frequencia configurado e marcado como feito. Se aula mudou, canal falhou ou conteudo depender de dado protegido, nao envia.

**Limite Do Agente**

Nao envia lembrete com conteudo protegido ou aula alterada.

**Humano/Aprovacao/Fallback**

- Chama humano quando: Nao chama humano no cenario principal; se cair em `Canal bloqueia`, aplica fallback: Nao envia.
- Pede aprovacao quando: Nao pede aprovacao no cenario principal; se houver bloqueio, aplica o fallback definido.
- Fallback do teste: Se o teste cair em `Canal bloqueia`, Nao envia.

**Agente De Configuracao**

Neste teste, a Taliya conclui Lembrete professor quando as checagens passam. Se aparecer `Canal bloqueia`, ela para e cria pendencia.


### Rotina: Historico protegido

#### Compartilhar contexto

- ID interno: `G10`.
- Modo padrao: `Autonomo com aprovacao`.
- Visual central: `Pedido de aprovacao`.
- Usa celular: `nao`.

**Cenarios**

- `Compartilhamento permitido`: Monta aprovacao de contexto.
- `Destinatario sem permissao`: Bloqueia envio.
- `Aluno restringiu compartilhamento`: Chama revisao.
- `Aprovacao vence`: Nao compartilha.

**Visual Do Caso**

card de aprovacao com dados, impacto, decisao pendente e efeito se aprovado

**Execucao Do Teste**

1. Inicio: O fluxo comeca quando contexto do aluno precisa ser compartilhado com alguem.
2. Checagens: destinatario foi identificado; dados permitidos foram selecionados; objetivo do compartilhamento esta claro; preview foi gerado; aprovador esta definido.
3. Decisao: No cenario `Compartilhamento permitido`, a Taliya nao aplica sozinha: monta um pedido de aprovacao para humano autorizado.
4. Pedido de aprovacao: Monta a aprovacao para aprovar compartilhamento de contexto, mostrando destinatario foi identificado; dados permitidos foram selecionados; objetivo do compartilhamento esta claro; preview foi gerado.
5. Fim: O compartilhamento de contexto vira aprovacao com destinatario, dados e finalidade. Se aprovado, o contexto e compartilhado; se houver restricao ou permissao faltando, fica bloqueado.

**Limite Do Agente**

Nao compartilha contexto antes da aprovacao.

**Humano/Aprovacao/Fallback**

- Chama humano quando: destinatario nao tem permissao; dados incluem historico protegido; objetivo e ambiguo; aluno pediu restricao de compartilhamento; aprovacao vence ou permissao bloqueia.
- Pede aprovacao quando: No cenario principal, antes da acao principal.
- Fallback do teste: Se o teste cair em `Aprovacao vence`, Nao compartilha.

**Agente De Configuracao**

Neste teste, a Taliya monta a aprovacao de Compartilhar contexto e nao aplica a mudanca sozinha. Se aparecer `Destinatario sem permissao` ou `Aluno restringiu compartilhamento`, o caso fica com a equipe.

#### Permissao historico

- ID interno: `G11`.
- Modo padrao: `Autonomo com aprovacao`.
- Visual central: `Pedido de aprovacao`.
- Usa celular: `nao`.

**Cenarios**

- `Escopo de permissao claro`: Monta aprovacao de permissao.
- `Escopo amplo demais`: Bloqueia mudanca.
- `Conflito com permissao global`: Chama admin.
- `Aprovacao vence`: Mantem permissao atual.

**Visual Do Caso**

card de aprovacao com dados, impacto, decisao pendente e efeito se aprovado

**Execucao Do Teste**

1. Inicio: O fluxo comeca quando permissao de historico precisa ser alterada ou revisada.
2. Checagens: papel ou perfil foi identificado; escopo de visibilidade esta definido; impacto foi mostrado; responsavel esta atribuido; aprovador esta definido.
3. Decisao: No cenario `Escopo de permissao claro`, a Taliya nao aplica sozinha: monta um pedido de aprovacao para humano autorizado.
4. Pedido de aprovacao: Monta a aprovacao para aprovar permissao de historico, mostrando papel ou perfil foi identificado; escopo de visibilidade esta definido; impacto foi mostrado; responsavel esta atribuido.
5. Fim: Permissao de historico vira aprovacao com papel, escopo e impacto. Se aprovada, a visibilidade muda; se conflitar com permissao global ou dado protegido, fica pendente.

**Limite Do Agente**

Nao muda permissao de historico antes da aprovacao.

**Humano/Aprovacao/Fallback**

- Chama humano quando: escopo amplo demais; papel nao deveria ver dado protegido; conflito com permissao global; evento de auditoria e sensivel; aprovacao vence ou permissao bloqueia.
- Pede aprovacao quando: No cenario principal, antes da acao principal.
- Fallback do teste: Se o teste cair em `Aprovacao vence`, Mantem permissao atual.

**Agente De Configuracao**

Neste teste, a Taliya monta a aprovacao de Permissao historico e nao aplica a mudanca sozinha. Se aparecer `Escopo amplo demais` ou `Conflito com permissao global`, o caso fica com a equipe.


### Rotina: Aula com contexto

#### Linha do tempo

- ID interno: `G12`.
- Modo padrao: `Autonomo com excecoes`.
- Visual central: `Linha do tempo`.
- Usa celular: `nao`.

**Cenarios**

- `Linha do tempo segura`: Organiza eventos permitidos.
- `Evento protegido aparece`: Restringe exibicao.
- `Historico conflita`: Abre revisao.
- `Usuario sem permissao`: Oculta linha do tempo.

**Visual Do Caso**

linha do tempo do aluno com eventos permitidos e filtros seguros

**Execucao Do Teste**

1. Inicio: O fluxo comeca quando a linha do tempo do aluno precisa ser organizada ou exibida.
2. Checagens: aluno foi identificado; tipos de evento estao permitidos; filtro padrao esta definido; responsavel esta atribuido; historico pode ser exibido sem dado indevido.
3. Decisao: No cenario `Linha do tempo segura`, a Taliya segue sem equipe porque nenhuma excecao foi encontrada.
4. Acao: Executa o caso valido: organizar linha do tempo do aluno.
5. Fim: A linha do tempo do aluno fica organizada com eventos permitidos e filtro seguro. Se aparecer evento protegido, conflito ou falta de permissao, a exibicao restringe e abre revisao.

**Limite Do Agente**

Nao exibe evento protegido, conflitado ou sem permissao.

**Humano/Aprovacao/Fallback**

- Chama humano quando: evento protegido aparece; historico conflita ou esta incompleto; usuario nao tem permissao; filtro mostra dado sensivel; permissao ou cota bloqueia exibicao.
- Pede aprovacao quando: Nao pede aprovacao no cenario principal; nas excecoes, chama humano em vez de aprovar automaticamente.
- Fallback do teste: Se o teste cair em `Usuario sem permissao`, Oculta linha do tempo.

**Agente De Configuracao**

Neste teste, a Taliya executa Linha do tempo apenas no cenario valido. Se aparecer `Evento protegido aparece` ou `Historico conflita`, chama a equipe.
