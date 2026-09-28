# Taliya CRM - Revisao Inicio Meio Fim Por Modo

Status: documento de revisao v0.1.
Data: 2026-05-22.

Este documento e a versao legivel de `agents-flows-lifecycle-mode-matrix.pt-BR.csv`.

Cada fluxo aparece com os cinco modos. Modos acima do teto ficam marcados como bloqueados.


## Agente: Atendimento


### Rotina: Conversas e triagem


#### Nova conversa

**Manual** (habilitado)

- Inicio: O fluxo comeca quando surge um caso para classificar a conversa, abrir atendimento e mandar para a fila certa. A Taliya identifica o caso e organiza o contexto principal: mensagem chegou por canal conectado; contato esta identificado ou pode receber resposta geral; assunto inicial foi reconhecido.
- Meio: A Taliya cria tarefa, checklist ou caso para a equipe classificar a conversa, abrir atendimento e mandar para a fila certa. A decisao e a execucao principal ficam com o humano.
- Fim: O fluxo termina quando a equipe registra o resultado. A Taliya salva auditoria e, se nao puder seguir, criar tarefa/caso em /app/inbox; /app/tarefas; /app/operacao e manter auditoria do motivo.
- Ajustes afetados: fila de atendimento; limite de respostas; quando chamar humano
- Encadeamento: /app/inbox; /app/tarefas; /app/operacao

**Copiloto** (habilitado)

- Inicio: O fluxo comeca quando surge um caso para classificar a conversa, abrir atendimento e mandar para a fila certa. A Taliya identifica o contexto e mostra a base da sugestao: mensagem chegou por canal conectado; contato esta identificado ou pode receber resposta geral; assunto inicial foi reconhecido.
- Meio: A Taliya sugere classificar a conversa, abrir atendimento e mandar para a fila certa, prepara texto/resumo/proximo passo e mostra os dados usados. A equipe pode aceitar, editar ou descartar antes de executar.
- Fim: Se a equipe aceitar, a acao e registrada conforme a decisao humana. Se editar ou descartar, a Taliya registra a decisao e mantem continuidade em /app/inbox; /app/tarefas; /app/operacao.
- Ajustes afetados: fila de atendimento; limite de respostas; quando chamar humano
- Encadeamento: /app/inbox; /app/tarefas; /app/operacao

**Autonomo com aprovacao** (habilitado)

- Inicio: O fluxo comeca quando surge um caso para classificar a conversa, abrir atendimento e mandar para a fila certa. A Taliya identifica o caso, confere mensagem chegou por canal conectado; contato esta identificado ou pode receber resposta geral; assunto inicial foi reconhecido e prepara a revisao.
- Meio: A Taliya valida mensagem chegou por canal conectado; contato esta identificado ou pode receber resposta geral; assunto inicial foi reconhecido; fila de atendimento esta definida e prepara classificar a conversa, abrir atendimento e mandar para a fila certa. Antes de concluir, mostra impacto/preview e pede aprovacao.
- Fim: Se aprovado, a acao e concluida e auditada. Se recusado, vencido ou incompleto, criar tarefa/caso em /app/inbox; /app/tarefas; /app/operacao e manter auditoria do motivo.
- Ajustes afetados: fila de atendimento; limite de respostas; quando chamar humano
- Encadeamento: /app/inbox; /app/tarefas; /app/operacao

**Autonomo com excecoes** (habilitado)

- Inicio: O fluxo comeca quando surge um caso para classificar a conversa, abrir atendimento e mandar para a fila certa. A Taliya identifica o caso e valida os dados principais: mensagem chegou por canal conectado; contato esta identificado ou pode receber resposta geral; assunto inicial foi reconhecido.
- Meio: A Taliya executa sozinha quando mensagem chegou por canal conectado; contato esta identificado ou pode receber resposta geral; assunto inicial foi reconhecido; fila de atendimento esta definida; limite de respostas nao foi atingido. Ela chama a equipe quando contato nao foi identificado; mensagem mistura varios assuntos; pedido envolve desconto, saude, privacidade ou reclamacao; fila de atendimento nao tem responsavel; canal, cota, opt-out ou permissao bloqueia resposta.
- Fim: No caso comum, a acao `classificar a conversa, abrir atendimento e mandar para a fila certa` fica registrada e auditada. Se houver excecao, criar tarefa/caso em /app/inbox; /app/tarefas; /app/operacao e manter auditoria do motivo.
- Ajustes afetados: fila de atendimento; limite de respostas; quando chamar humano
- Encadeamento: /app/inbox; /app/tarefas; /app/operacao

**Autonomo** (bloqueado)

- Inicio: Este modo fica bloqueado para Nova conversa.
- Meio: A Taliya nao conclui end-to-end porque este modo esta acima do teto do fluxo.
- Fim: Use o maior modo habilitado para automatizar o caso comum sem ultrapassar os limites publicados.
- Ajustes afetados: fila de atendimento; limite de respostas; quando chamar humano
- Encadeamento: /app/inbox; /app/tarefas; /app/operacao


#### Duvidas permitidas

**Manual** (habilitado)

- Inicio: O fluxo comeca quando surge um caso para responder duvidas permitidas usando a base aprovada. A Taliya identifica o caso e organiza o contexto principal: pergunta esta na base permitida; resposta nao exige dado sensivel; contato pode receber resposta pelo canal.
- Meio: A Taliya cria tarefa, checklist ou caso para a equipe responder duvidas permitidas usando a base aprovada. A decisao e a execucao principal ficam com o humano.
- Fim: O fluxo termina quando a equipe registra o resultado. A Taliya salva auditoria e, se nao puder seguir, criar tarefa/caso em /app/inbox; tarefa de resposta e manter auditoria do motivo.
- Ajustes afetados: tom/template de resposta; limite por conversa; quando chamar humano
- Encadeamento: /app/inbox; tarefa de resposta

**Copiloto** (habilitado)

- Inicio: O fluxo comeca quando surge um caso para responder duvidas permitidas usando a base aprovada. A Taliya identifica o contexto e mostra a base da sugestao: pergunta esta na base permitida; resposta nao exige dado sensivel; contato pode receber resposta pelo canal.
- Meio: A Taliya sugere responder duvidas permitidas usando a base aprovada, prepara texto/resumo/proximo passo e mostra os dados usados. A equipe pode aceitar, editar ou descartar antes de executar.
- Fim: Se a equipe aceitar, a acao e registrada conforme a decisao humana. Se editar ou descartar, a Taliya registra a decisao e mantem continuidade em /app/inbox; tarefa de resposta.
- Ajustes afetados: tom/template de resposta; limite por conversa; quando chamar humano
- Encadeamento: /app/inbox; tarefa de resposta

**Autonomo com aprovacao** (habilitado)

- Inicio: O fluxo comeca quando surge um caso para responder duvidas permitidas usando a base aprovada. A Taliya identifica o caso, confere pergunta esta na base permitida; resposta nao exige dado sensivel; contato pode receber resposta pelo canal e prepara a revisao.
- Meio: A Taliya valida pergunta esta na base permitida; resposta nao exige dado sensivel; contato pode receber resposta pelo canal; limite por conversa nao foi atingido e prepara responder duvidas permitidas usando a base aprovada. Antes de concluir, mostra impacto/preview e pede aprovacao.
- Fim: Se aprovado, a acao e concluida e auditada. Se recusado, vencido ou incompleto, criar tarefa/caso em /app/inbox; tarefa de resposta e manter auditoria do motivo.
- Ajustes afetados: tom/template de resposta; limite por conversa; quando chamar humano
- Encadeamento: /app/inbox; tarefa de resposta

**Autonomo com excecoes** (habilitado)

- Inicio: O fluxo comeca quando surge um caso para responder duvidas permitidas usando a base aprovada. A Taliya identifica o caso e valida os dados principais: pergunta esta na base permitida; resposta nao exige dado sensivel; contato pode receber resposta pelo canal.
- Meio: A Taliya executa sozinha quando pergunta esta na base permitida; resposta nao exige dado sensivel; contato pode receber resposta pelo canal; limite por conversa nao foi atingido; fallback esta definido. Ela chama a equipe quando pergunta nao esta na base; aluno pede condicao comercial especial; mensagem pede dado privado; conversa ficou confusa ou agressiva; canal, cota, opt-out ou permissao bloqueia resposta.
- Fim: No caso comum, a acao `responder duvidas permitidas usando a base aprovada` fica registrada e auditada. Se houver excecao, criar tarefa/caso em /app/inbox; tarefa de resposta e manter auditoria do motivo.
- Ajustes afetados: tom/template de resposta; limite por conversa; quando chamar humano
- Encadeamento: /app/inbox; tarefa de resposta

**Autonomo** (habilitado)

- Inicio: O fluxo comeca quando surge um caso para responder duvidas permitidas usando a base aprovada. A Taliya identifica o caso e confirma pergunta esta na base permitida; resposta nao exige dado sensivel; contato pode receber resposta pelo canal.
- Meio: A Taliya conclui responder duvidas permitidas usando a base aprovada quando pergunta esta na base permitida; resposta nao exige dado sensivel; contato pode receber resposta pelo canal; limite por conversa nao foi atingido; fallback esta definido. Ela para quando pergunta nao esta na base; aluno pede condicao comercial especial; mensagem pede dado privado; conversa ficou confusa ou agressiva; canal, cota, opt-out ou permissao bloqueia resposta.
- Fim: A acao e concluida, a auditoria fica salva e a continuidade segue em /app/inbox; tarefa de resposta. Se houver bloqueio, criar tarefa/caso em /app/inbox; tarefa de resposta e manter auditoria do motivo.
- Ajustes afetados: tom/template de resposta; limite por conversa; quando chamar humano
- Encadeamento: /app/inbox; tarefa de resposta


#### Aluno existente

**Manual** (habilitado)

- Inicio: O fluxo comeca quando surge um caso para reconhecer aluno existente e encaminhar atendimento com contexto. A Taliya identifica o caso e organiza o contexto principal: telefone corresponde a um aluno ou responsavel permitido; cadastro nao tem conflito de identidade; pedido usa dados permitidos.
- Meio: A Taliya cria tarefa, checklist ou caso para a equipe reconhecer aluno existente e encaminhar atendimento com contexto. A decisao e a execucao principal ficam com o humano.
- Fim: O fluxo termina quando a equipe registra o resultado. A Taliya salva auditoria e, se nao puder seguir, criar tarefa/caso em /app/inbox; /app/alunos/[id]; /app/tarefas e manter auditoria do motivo.
- Ajustes afetados: fila de atendimento; dados que chamam humano; botao chamar humano
- Encadeamento: /app/inbox; /app/alunos/[id]; /app/tarefas

**Copiloto** (habilitado)

- Inicio: O fluxo comeca quando surge um caso para reconhecer aluno existente e encaminhar atendimento com contexto. A Taliya identifica o contexto e mostra a base da sugestao: telefone corresponde a um aluno ou responsavel permitido; cadastro nao tem conflito de identidade; pedido usa dados permitidos.
- Meio: A Taliya sugere reconhecer aluno existente e encaminhar atendimento com contexto, prepara texto/resumo/proximo passo e mostra os dados usados. A equipe pode aceitar, editar ou descartar antes de executar.
- Fim: Se a equipe aceitar, a acao e registrada conforme a decisao humana. Se editar ou descartar, a Taliya registra a decisao e mantem continuidade em /app/inbox; /app/alunos/[id]; /app/tarefas.
- Ajustes afetados: fila de atendimento; dados que chamam humano; botao chamar humano
- Encadeamento: /app/inbox; /app/alunos/[id]; /app/tarefas

**Autonomo com aprovacao** (habilitado)

- Inicio: O fluxo comeca quando surge um caso para reconhecer aluno existente e encaminhar atendimento com contexto. A Taliya identifica o caso, confere telefone corresponde a um aluno ou responsavel permitido; cadastro nao tem conflito de identidade; pedido usa dados permitidos e prepara a revisao.
- Meio: A Taliya valida telefone corresponde a um aluno ou responsavel permitido; cadastro nao tem conflito de identidade; pedido usa dados permitidos; fila destino esta definida e prepara reconhecer aluno existente e encaminhar atendimento com contexto. Antes de concluir, mostra impacto/preview e pede aprovacao.
- Fim: Se aprovado, a acao e concluida e auditada. Se recusado, vencido ou incompleto, criar tarefa/caso em /app/inbox; /app/alunos/[id]; /app/tarefas e manter auditoria do motivo.
- Ajustes afetados: fila de atendimento; dados que chamam humano; botao chamar humano
- Encadeamento: /app/inbox; /app/alunos/[id]; /app/tarefas

**Autonomo com excecoes** (habilitado)

- Inicio: O fluxo comeca quando surge um caso para reconhecer aluno existente e encaminhar atendimento com contexto. A Taliya identifica o caso e valida os dados principais: telefone corresponde a um aluno ou responsavel permitido; cadastro nao tem conflito de identidade; pedido usa dados permitidos.
- Meio: A Taliya executa sozinha quando telefone corresponde a um aluno ou responsavel permitido; cadastro nao tem conflito de identidade; pedido usa dados permitidos; fila destino esta definida; botao de ajuda permanece disponivel. Ela chama a equipe quando telefone atende mais de um aluno; cadastro esta duplicado; pedido exige alteracao sensivel; aluno contesta informacao do CRM; canal, cota ou permissao bloqueia acao.
- Fim: No caso comum, a acao `reconhecer aluno existente e encaminhar atendimento com contexto` fica registrada e auditada. Se houver excecao, criar tarefa/caso em /app/inbox; /app/alunos/[id]; /app/tarefas e manter auditoria do motivo.
- Ajustes afetados: fila de atendimento; dados que chamam humano; botao chamar humano
- Encadeamento: /app/inbox; /app/alunos/[id]; /app/tarefas

**Autonomo** (bloqueado)

- Inicio: Este modo fica bloqueado para Aluno existente.
- Meio: A Taliya nao conclui end-to-end porque este modo esta acima do teto do fluxo.
- Fim: Use o maior modo habilitado para automatizar o caso comum sem ultrapassar os limites publicados.
- Ajustes afetados: fila de atendimento; dados que chamam humano; botao chamar humano
- Encadeamento: /app/inbox; /app/alunos/[id]; /app/tarefas


#### Fora do escopo

**Manual** (habilitado)

- Inicio: O fluxo comeca quando surge um caso para responder fora de escopo e criar destino correto. A Taliya identifica o caso e organiza o contexto principal: assunto nao pertence ao CRM do studio; resposta padrao esta aprovada; contato nao pediu humano.
- Meio: A Taliya cria tarefa, checklist ou caso para a equipe responder fora de escopo e criar destino correto. A decisao e a execucao principal ficam com o humano.
- Fim: O fluxo termina quando a equipe registra o resultado. A Taliya salva auditoria e, se nao puder seguir, criar tarefa/caso em /app/inbox; tarefa/caso e manter auditoria do motivo.
- Ajustes afetados: resposta padrao; destino da tarefa/caso
- Encadeamento: /app/inbox; tarefa/caso

**Copiloto** (habilitado)

- Inicio: O fluxo comeca quando surge um caso para responder fora de escopo e criar destino correto. A Taliya identifica o contexto e mostra a base da sugestao: assunto nao pertence ao CRM do studio; resposta padrao esta aprovada; contato nao pediu humano.
- Meio: A Taliya sugere responder fora de escopo e criar destino correto, prepara texto/resumo/proximo passo e mostra os dados usados. A equipe pode aceitar, editar ou descartar antes de executar.
- Fim: Se a equipe aceitar, a acao e registrada conforme a decisao humana. Se editar ou descartar, a Taliya registra a decisao e mantem continuidade em /app/inbox; tarefa/caso.
- Ajustes afetados: resposta padrao; destino da tarefa/caso
- Encadeamento: /app/inbox; tarefa/caso

**Autonomo com aprovacao** (habilitado)

- Inicio: O fluxo comeca quando surge um caso para responder fora de escopo e criar destino correto. A Taliya identifica o caso, confere assunto nao pertence ao CRM do studio; resposta padrao esta aprovada; contato nao pediu humano e prepara a revisao.
- Meio: A Taliya valida assunto nao pertence ao CRM do studio; resposta padrao esta aprovada; contato nao pediu humano; destino da tarefa ou caso esta definido e prepara responder fora de escopo e criar destino correto. Antes de concluir, mostra impacto/preview e pede aprovacao.
- Fim: Se aprovado, a acao e concluida e auditada. Se recusado, vencido ou incompleto, criar tarefa/caso em /app/inbox; tarefa/caso e manter auditoria do motivo.
- Ajustes afetados: resposta padrao; destino da tarefa/caso
- Encadeamento: /app/inbox; tarefa/caso

**Autonomo com excecoes** (habilitado)

- Inicio: O fluxo comeca quando surge um caso para responder fora de escopo e criar destino correto. A Taliya identifica o caso e valida os dados principais: assunto nao pertence ao CRM do studio; resposta padrao esta aprovada; contato nao pediu humano.
- Meio: A Taliya executa sozinha quando assunto nao pertence ao CRM do studio; resposta padrao esta aprovada; contato nao pediu humano; destino da tarefa ou caso esta definido; mensagem nao contem risco sensivel. Ela chama a equipe quando assunto parece reclamacao; mensagem envolve emergencia, saude ou dado pessoal; lead ou aluno insiste em humano; resposta padrao nao cobre o caso; canal, cota ou permissao bloqueia acao.
- Fim: No caso comum, a acao `responder fora de escopo e criar destino correto` fica registrada e auditada. Se houver excecao, criar tarefa/caso em /app/inbox; tarefa/caso e manter auditoria do motivo.
- Ajustes afetados: resposta padrao; destino da tarefa/caso
- Encadeamento: /app/inbox; tarefa/caso

**Autonomo** (habilitado)

- Inicio: O fluxo comeca quando surge um caso para responder fora de escopo e criar destino correto. A Taliya identifica o caso e confirma assunto nao pertence ao CRM do studio; resposta padrao esta aprovada; contato nao pediu humano.
- Meio: A Taliya conclui responder fora de escopo e criar destino correto quando assunto nao pertence ao CRM do studio; resposta padrao esta aprovada; contato nao pediu humano; destino da tarefa ou caso esta definido; mensagem nao contem risco sensivel. Ela para quando assunto parece reclamacao; mensagem envolve emergencia, saude ou dado pessoal; lead ou aluno insiste em humano; resposta padrao nao cobre o caso; canal, cota ou permissao bloqueia acao.
- Fim: A acao e concluida, a auditoria fica salva e a continuidade segue em /app/inbox; tarefa/caso. Se houver bloqueio, criar tarefa/caso em /app/inbox; tarefa/caso e manter auditoria do motivo.
- Ajustes afetados: resposta padrao; destino da tarefa/caso
- Encadeamento: /app/inbox; tarefa/caso


#### Chamada humana

**Manual** (habilitado)

- Inicio: O fluxo comeca quando surge um caso para chamar humano com resumo, fila e prioridade. A Taliya identifica o caso e organiza o contexto principal: gatilho de humano foi detectado; fila destino esta definida; prioridade foi calculada.
- Meio: A Taliya cria tarefa, checklist ou caso para a equipe chamar humano com resumo, fila e prioridade. A decisao e a execucao principal ficam com o humano.
- Fim: O fluxo termina quando a equipe registra o resultado. A Taliya salva auditoria e, se nao puder seguir, criar tarefa/caso em /app/inbox; /app/operacao; fila humana e manter auditoria do motivo.
- Ajustes afetados: fila de handoff; prioridade inicial; campos do resumo
- Encadeamento: /app/inbox; /app/operacao; fila humana

**Copiloto** (habilitado)

- Inicio: O fluxo comeca quando surge um caso para chamar humano com resumo, fila e prioridade. A Taliya identifica o contexto e mostra a base da sugestao: gatilho de humano foi detectado; fila destino esta definida; prioridade foi calculada.
- Meio: A Taliya sugere chamar humano com resumo, fila e prioridade, prepara texto/resumo/proximo passo e mostra os dados usados. A equipe pode aceitar, editar ou descartar antes de executar.
- Fim: Se a equipe aceitar, a acao e registrada conforme a decisao humana. Se editar ou descartar, a Taliya registra a decisao e mantem continuidade em /app/inbox; /app/operacao; fila humana.
- Ajustes afetados: fila de handoff; prioridade inicial; campos do resumo
- Encadeamento: /app/inbox; /app/operacao; fila humana

**Autonomo com aprovacao** (habilitado)

- Inicio: O fluxo comeca quando surge um caso para chamar humano com resumo, fila e prioridade. A Taliya identifica o caso, confere gatilho de humano foi detectado; fila destino esta definida; prioridade foi calculada e prepara a revisao.
- Meio: A Taliya valida gatilho de humano foi detectado; fila destino esta definida; prioridade foi calculada; resumo obrigatorio foi gerado e prepara chamar humano com resumo, fila e prioridade. Antes de concluir, mostra impacto/preview e pede aprovacao.
- Fim: Se aprovado, a acao e concluida e auditada. Se recusado, vencido ou incompleto, criar tarefa/caso em /app/inbox; /app/operacao; fila humana e manter auditoria do motivo.
- Ajustes afetados: fila de handoff; prioridade inicial; campos do resumo
- Encadeamento: /app/inbox; /app/operacao; fila humana

**Autonomo com excecoes** (habilitado)

- Inicio: O fluxo comeca quando surge um caso para chamar humano com resumo, fila e prioridade. A Taliya identifica o caso e valida os dados principais: gatilho de humano foi detectado; fila destino esta definida; prioridade foi calculada.
- Meio: A Taliya executa sozinha quando gatilho de humano foi detectado; fila destino esta definida; prioridade foi calculada; resumo obrigatorio foi gerado; responsavel pode assumir o caso. Ela chama a equipe quando fila destino nao existe; prioridade nao pode ser definida; resumo ficou incompleto; caso exige dono ou admin especifico; canal, cota ou permissao bloqueia criacao.
- Fim: No caso comum, a acao `chamar humano com resumo, fila e prioridade` fica registrada e auditada. Se houver excecao, criar tarefa/caso em /app/inbox; /app/operacao; fila humana e manter auditoria do motivo.
- Ajustes afetados: fila de handoff; prioridade inicial; campos do resumo
- Encadeamento: /app/inbox; /app/operacao; fila humana

**Autonomo** (habilitado)

- Inicio: O fluxo comeca quando surge um caso para chamar humano com resumo, fila e prioridade. A Taliya identifica o caso e confirma gatilho de humano foi detectado; fila destino esta definida; prioridade foi calculada.
- Meio: A Taliya conclui chamar humano com resumo, fila e prioridade quando gatilho de humano foi detectado; fila destino esta definida; prioridade foi calculada; resumo obrigatorio foi gerado; responsavel pode assumir o caso. Ela para quando fila destino nao existe; prioridade nao pode ser definida; resumo ficou incompleto; caso exige dono ou admin especifico; canal, cota ou permissao bloqueia criacao.
- Fim: A acao e concluida, a auditoria fica salva e a continuidade segue em /app/inbox; /app/operacao; fila humana. Se houver bloqueio, criar tarefa/caso em /app/inbox; /app/operacao; fila humana e manter auditoria do motivo.
- Ajustes afetados: fila de handoff; prioridade inicial; campos do resumo
- Encadeamento: /app/inbox; /app/operacao; fila humana


### Rotina: Identidade e privacidade


#### Consentimento/opt-out

**Manual** (habilitado)

- Inicio: O fluxo comeca quando surge um caso para registrar consentimento, opt-out ou preferencia de contato. A Taliya identifica o caso e organiza o contexto principal: contato foi identificado; pedido de consentimento ou opt-out e claro; texto de confirmacao esta aprovado.
- Meio: A Taliya cria tarefa, checklist ou caso para a equipe registrar consentimento, opt-out ou preferencia de contato. A decisao e a execucao principal ficam com o humano.
- Fim: O fluxo termina quando a equipe registra o resultado. A Taliya salva auditoria e, se nao puder seguir, criar tarefa/caso em /app/contatos/[id]; auditoria; tarefa e manter auditoria do motivo.
- Ajustes afetados: texto de confirmacao; responsavel de revisao em caso ambiguo
- Encadeamento: /app/contatos/[id]; auditoria; tarefa

**Copiloto** (habilitado)

- Inicio: O fluxo comeca quando surge um caso para registrar consentimento, opt-out ou preferencia de contato. A Taliya identifica o contexto e mostra a base da sugestao: contato foi identificado; pedido de consentimento ou opt-out e claro; texto de confirmacao esta aprovado.
- Meio: A Taliya sugere registrar consentimento, opt-out ou preferencia de contato, prepara texto/resumo/proximo passo e mostra os dados usados. A equipe pode aceitar, editar ou descartar antes de executar.
- Fim: Se a equipe aceitar, a acao e registrada conforme a decisao humana. Se editar ou descartar, a Taliya registra a decisao e mantem continuidade em /app/contatos/[id]; auditoria; tarefa.
- Ajustes afetados: texto de confirmacao; responsavel de revisao em caso ambiguo
- Encadeamento: /app/contatos/[id]; auditoria; tarefa

**Autonomo com aprovacao** (habilitado)

- Inicio: O fluxo comeca quando surge um caso para registrar consentimento, opt-out ou preferencia de contato. A Taliya identifica o caso, confere contato foi identificado; pedido de consentimento ou opt-out e claro; texto de confirmacao esta aprovado e prepara a revisao.
- Meio: A Taliya valida contato foi identificado; pedido de consentimento ou opt-out e claro; texto de confirmacao esta aprovado; responsavel de revisao existe para caso ambiguo e prepara registrar consentimento, opt-out ou preferencia de contato. Antes de concluir, mostra impacto/preview e pede aprovacao.
- Fim: Se aprovado, a acao e concluida e auditada. Se recusado, vencido ou incompleto, criar tarefa/caso em /app/contatos/[id]; auditoria; tarefa e manter auditoria do motivo.
- Ajustes afetados: texto de confirmacao; responsavel de revisao em caso ambiguo
- Encadeamento: /app/contatos/[id]; auditoria; tarefa

**Autonomo com excecoes** (habilitado)

- Inicio: O fluxo comeca quando surge um caso para registrar consentimento, opt-out ou preferencia de contato. A Taliya identifica o caso e valida os dados principais: contato foi identificado; pedido de consentimento ou opt-out e claro; texto de confirmacao esta aprovado.
- Meio: A Taliya executa sozinha quando contato foi identificado; pedido de consentimento ou opt-out e claro; texto de confirmacao esta aprovado; responsavel de revisao existe para caso ambiguo; auditoria pode ser registrada. Ela chama a equipe quando pedido e ambiguo; telefone e compartilhado; contato pede exclusao ou copia de dados; ha conflito entre responsavel e aluno; canal, cota ou permissao bloqueia confirmacao.
- Fim: No caso comum, a acao `registrar consentimento, opt-out ou preferencia de contato` fica registrada e auditada. Se houver excecao, criar tarefa/caso em /app/contatos/[id]; auditoria; tarefa e manter auditoria do motivo.
- Ajustes afetados: texto de confirmacao; responsavel de revisao em caso ambiguo
- Encadeamento: /app/contatos/[id]; auditoria; tarefa

**Autonomo** (habilitado)

- Inicio: O fluxo comeca quando surge um caso para registrar consentimento, opt-out ou preferencia de contato. A Taliya identifica o caso e confirma contato foi identificado; pedido de consentimento ou opt-out e claro; texto de confirmacao esta aprovado.
- Meio: A Taliya conclui registrar consentimento, opt-out ou preferencia de contato quando contato foi identificado; pedido de consentimento ou opt-out e claro; texto de confirmacao esta aprovado; responsavel de revisao existe para caso ambiguo; auditoria pode ser registrada. Ela para quando pedido e ambiguo; telefone e compartilhado; contato pede exclusao ou copia de dados; ha conflito entre responsavel e aluno; canal, cota ou permissao bloqueia confirmacao.
- Fim: A acao e concluida, a auditoria fica salva e a continuidade segue em /app/contatos/[id]; auditoria; tarefa. Se houver bloqueio, criar tarefa/caso em /app/contatos/[id]; auditoria; tarefa e manter auditoria do motivo.
- Ajustes afetados: texto de confirmacao; responsavel de revisao em caso ambiguo
- Encadeamento: /app/contatos/[id]; auditoria; tarefa


#### Identidade/midias

**Manual** (habilitado)

- Inicio: O fluxo comeca quando surge um caso para tratar identidade, audio, imagem ou midia recebida. A Taliya identifica o caso e organiza o contexto principal: midia e legivel; tipo de midia e aceito; contato esta identificado.
- Meio: A Taliya cria tarefa, checklist ou caso para a equipe tratar identidade, audio, imagem ou midia recebida. A decisao e a execucao principal ficam com o humano.
- Fim: O fluxo termina quando a equipe registra o resultado. A Taliya salva auditoria e, se nao puder seguir, criar tarefa/caso em /app/inbox; /app/dados/duplicidades; /app/historico/documentos e manter auditoria do motivo.
- Ajustes afetados: responsavel de revisao; tipos de midia aceitos
- Encadeamento: /app/inbox; /app/dados/duplicidades; /app/historico/documentos

**Copiloto** (habilitado)

- Inicio: O fluxo comeca quando surge um caso para tratar identidade, audio, imagem ou midia recebida. A Taliya identifica o contexto e mostra a base da sugestao: midia e legivel; tipo de midia e aceito; contato esta identificado.
- Meio: A Taliya sugere tratar identidade, audio, imagem ou midia recebida, prepara texto/resumo/proximo passo e mostra os dados usados. A equipe pode aceitar, editar ou descartar antes de executar.
- Fim: Se a equipe aceitar, a acao e registrada conforme a decisao humana. Se editar ou descartar, a Taliya registra a decisao e mantem continuidade em /app/inbox; /app/dados/duplicidades; /app/historico/documentos.
- Ajustes afetados: responsavel de revisao; tipos de midia aceitos
- Encadeamento: /app/inbox; /app/dados/duplicidades; /app/historico/documentos

**Autonomo com aprovacao** (habilitado)

- Inicio: O fluxo comeca quando surge um caso para tratar identidade, audio, imagem ou midia recebida. A Taliya identifica o caso, confere midia e legivel; tipo de midia e aceito; contato esta identificado e prepara a revisao.
- Meio: A Taliya valida midia e legivel; tipo de midia e aceito; contato esta identificado; conteudo nao traz dado sensivel inesperado e prepara tratar identidade, audio, imagem ou midia recebida. Antes de concluir, mostra impacto/preview e pede aprovacao.
- Fim: Se aprovado, a acao e concluida e auditada. Se recusado, vencido ou incompleto, criar tarefa/caso em /app/inbox; /app/dados/duplicidades; /app/historico/documentos e manter auditoria do motivo.
- Ajustes afetados: responsavel de revisao; tipos de midia aceitos
- Encadeamento: /app/inbox; /app/dados/duplicidades; /app/historico/documentos

**Autonomo com excecoes** (habilitado)

- Inicio: O fluxo comeca quando surge um caso para tratar identidade, audio, imagem ou midia recebida. A Taliya identifica o caso e valida os dados principais: midia e legivel; tipo de midia e aceito; contato esta identificado.
- Meio: A Taliya executa sozinha quando midia e legivel; tipo de midia e aceito; contato esta identificado; conteudo nao traz dado sensivel inesperado; responsavel de revisao esta definido. Ela chama a equipe quando midia esta ilegivel; documento parece sensivel; identidade nao confere; arquivo nao e aceito; canal, cota ou permissao bloqueia acao.
- Fim: No caso comum, a acao `tratar identidade, audio, imagem ou midia recebida` fica registrada e auditada. Se houver excecao, criar tarefa/caso em /app/inbox; /app/dados/duplicidades; /app/historico/documentos e manter auditoria do motivo.
- Ajustes afetados: responsavel de revisao; tipos de midia aceitos
- Encadeamento: /app/inbox; /app/dados/duplicidades; /app/historico/documentos

**Autonomo** (bloqueado)

- Inicio: Este modo fica bloqueado para Identidade/midias.
- Meio: A Taliya nao conclui end-to-end porque este modo esta acima do teto do fluxo.
- Fim: Use o maior modo habilitado para automatizar o caso comum sem ultrapassar os limites publicados.
- Ajustes afetados: responsavel de revisao; tipos de midia aceitos
- Encadeamento: /app/inbox; /app/dados/duplicidades; /app/historico/documentos


#### Privacidade/dados

**Manual** (habilitado)

- Inicio: O fluxo comeca quando surge um caso para preparar pedido de privacidade ou dados para aprovacao. A Taliya identifica o caso e organiza o contexto principal: solicitante foi identificado; tipo de pedido de dado foi classificado; dados envolvidos foram listados.
- Meio: A Taliya cria tarefa, checklist ou caso para a equipe preparar pedido de privacidade ou dados para aprovacao. A decisao e a execucao principal ficam com o humano.
- Fim: O fluxo termina quando a equipe registra o resultado. A Taliya salva auditoria e, se nao puder seguir, criar tarefa/caso em /app/operacao; /app/auditoria; aprovacao e manter auditoria do motivo.
- Ajustes afetados: aprovador de privacidade; SLA do caso
- Encadeamento: /app/operacao; /app/auditoria; aprovacao

**Copiloto** (habilitado)

- Inicio: O fluxo comeca quando surge um caso para preparar pedido de privacidade ou dados para aprovacao. A Taliya identifica o contexto e mostra a base da sugestao: solicitante foi identificado; tipo de pedido de dado foi classificado; dados envolvidos foram listados.
- Meio: A Taliya sugere preparar pedido de privacidade ou dados para aprovacao, prepara texto/resumo/proximo passo e mostra os dados usados. A equipe pode aceitar, editar ou descartar antes de executar.
- Fim: Se a equipe aceitar, a acao e registrada conforme a decisao humana. Se editar ou descartar, a Taliya registra a decisao e mantem continuidade em /app/operacao; /app/auditoria; aprovacao.
- Ajustes afetados: aprovador de privacidade; SLA do caso
- Encadeamento: /app/operacao; /app/auditoria; aprovacao

**Autonomo com aprovacao** (habilitado)

- Inicio: O fluxo comeca quando surge um caso para preparar pedido de privacidade ou dados para aprovacao. A Taliya identifica o caso, confere solicitante foi identificado; tipo de pedido de dado foi classificado; dados envolvidos foram listados e prepara a revisao.
- Meio: A Taliya valida solicitante foi identificado; tipo de pedido de dado foi classificado; dados envolvidos foram listados; SLA do caso esta definido e prepara preparar pedido de privacidade ou dados para aprovacao. Antes de concluir, mostra impacto/preview e pede aprovacao.
- Fim: Se aprovado, a acao e concluida e auditada. Se recusado, vencido ou incompleto, criar tarefa/caso em /app/operacao; /app/auditoria; aprovacao e manter auditoria do motivo.
- Ajustes afetados: aprovador de privacidade; SLA do caso
- Encadeamento: /app/operacao; /app/auditoria; aprovacao

**Autonomo com excecoes** (bloqueado)

- Inicio: Este modo fica bloqueado para Privacidade/dados.
- Meio: A Taliya nao executa com excecoes porque o teto deste fluxo e menor.
- Fim: O usuario deve escolher um modo permitido para este fluxo.
- Ajustes afetados: aprovador de privacidade; SLA do caso
- Encadeamento: /app/operacao; /app/auditoria; aprovacao

**Autonomo** (bloqueado)

- Inicio: Este modo fica bloqueado para Privacidade/dados.
- Meio: A Taliya nao conclui end-to-end porque este modo esta acima do teto do fluxo.
- Fim: Use o maior modo habilitado para automatizar o caso comum sem ultrapassar os limites publicados.
- Ajustes afetados: aprovador de privacidade; SLA do caso
- Encadeamento: /app/operacao; /app/auditoria; aprovacao


#### Telefone compartilhado e identidade

**Manual** (habilitado)

- Inicio: O fluxo comeca quando surge um caso para validar telefone compartilhado antes de expor informacao. A Taliya identifica o caso e organiza o contexto principal: telefone compartilhado foi detectado; alunos possiveis foram listados; regra de validacao esta definida.
- Meio: A Taliya cria tarefa, checklist ou caso para a equipe validar telefone compartilhado antes de expor informacao. A decisao e a execucao principal ficam com o humano.
- Fim: O fluxo termina quando a equipe registra o resultado. A Taliya salva auditoria e, se nao puder seguir, criar tarefa/caso em /app/contatos; /app/alunos/[id]; /app/dados/duplicidades e manter auditoria do motivo.
- Ajustes afetados: regra de validacao; responsavel de revisao
- Encadeamento: /app/contatos; /app/alunos/[id]; /app/dados/duplicidades

**Copiloto** (habilitado)

- Inicio: O fluxo comeca quando surge um caso para validar telefone compartilhado antes de expor informacao. A Taliya identifica o contexto e mostra a base da sugestao: telefone compartilhado foi detectado; alunos possiveis foram listados; regra de validacao esta definida.
- Meio: A Taliya sugere validar telefone compartilhado antes de expor informacao, prepara texto/resumo/proximo passo e mostra os dados usados. A equipe pode aceitar, editar ou descartar antes de executar.
- Fim: Se a equipe aceitar, a acao e registrada conforme a decisao humana. Se editar ou descartar, a Taliya registra a decisao e mantem continuidade em /app/contatos; /app/alunos/[id]; /app/dados/duplicidades.
- Ajustes afetados: regra de validacao; responsavel de revisao
- Encadeamento: /app/contatos; /app/alunos/[id]; /app/dados/duplicidades

**Autonomo com aprovacao** (habilitado)

- Inicio: O fluxo comeca quando surge um caso para validar telefone compartilhado antes de expor informacao. A Taliya identifica o caso, confere telefone compartilhado foi detectado; alunos possiveis foram listados; regra de validacao esta definida e prepara a revisao.
- Meio: A Taliya valida telefone compartilhado foi detectado; alunos possiveis foram listados; regra de validacao esta definida; responsavel de revisao esta definido e prepara validar telefone compartilhado antes de expor informacao. Antes de concluir, mostra impacto/preview e pede aprovacao.
- Fim: Se aprovado, a acao e concluida e auditada. Se recusado, vencido ou incompleto, criar tarefa/caso em /app/contatos; /app/alunos/[id]; /app/dados/duplicidades e manter auditoria do motivo.
- Ajustes afetados: regra de validacao; responsavel de revisao
- Encadeamento: /app/contatos; /app/alunos/[id]; /app/dados/duplicidades

**Autonomo com excecoes** (bloqueado)

- Inicio: Este modo fica bloqueado para Telefone compartilhado e identidade.
- Meio: A Taliya nao executa com excecoes porque o teto deste fluxo e menor.
- Fim: O usuario deve escolher um modo permitido para este fluxo.
- Ajustes afetados: regra de validacao; responsavel de revisao
- Encadeamento: /app/contatos; /app/alunos/[id]; /app/dados/duplicidades

**Autonomo** (bloqueado)

- Inicio: Este modo fica bloqueado para Telefone compartilhado e identidade.
- Meio: A Taliya nao conclui end-to-end porque este modo esta acima do teto do fluxo.
- Fim: Use o maior modo habilitado para automatizar o caso comum sem ultrapassar os limites publicados.
- Ajustes afetados: regra de validacao; responsavel de revisao
- Encadeamento: /app/contatos; /app/alunos/[id]; /app/dados/duplicidades


### Rotina: Conversas e triagem


#### Ciclo de vida/SLA

**Manual** (habilitado)

- Inicio: O fluxo comeca quando surge um caso para acompanhar SLA e ciclo de vida do atendimento. A Taliya identifica o caso e organiza o contexto principal: conversa tem status claro; tempo de SLA esta definido; fila destino existe.
- Meio: A Taliya cria tarefa, checklist ou caso para a equipe acompanhar SLA e ciclo de vida do atendimento. A decisao e a execucao principal ficam com o humano.
- Fim: O fluxo termina quando a equipe registra o resultado. A Taliya salva auditoria e, se nao puder seguir, criar tarefa/caso em /app/inbox; /app/tarefas; /app/hoje e manter auditoria do motivo.
- Ajustes afetados: tempo de SLA; fila destino; prioridade
- Encadeamento: /app/inbox; /app/tarefas; /app/hoje

**Copiloto** (habilitado)

- Inicio: O fluxo comeca quando surge um caso para acompanhar SLA e ciclo de vida do atendimento. A Taliya identifica o contexto e mostra a base da sugestao: conversa tem status claro; tempo de SLA esta definido; fila destino existe.
- Meio: A Taliya sugere acompanhar SLA e ciclo de vida do atendimento, prepara texto/resumo/proximo passo e mostra os dados usados. A equipe pode aceitar, editar ou descartar antes de executar.
- Fim: Se a equipe aceitar, a acao e registrada conforme a decisao humana. Se editar ou descartar, a Taliya registra a decisao e mantem continuidade em /app/inbox; /app/tarefas; /app/hoje.
- Ajustes afetados: tempo de SLA; fila destino; prioridade
- Encadeamento: /app/inbox; /app/tarefas; /app/hoje

**Autonomo com aprovacao** (habilitado)

- Inicio: O fluxo comeca quando surge um caso para acompanhar SLA e ciclo de vida do atendimento. A Taliya identifica o caso, confere conversa tem status claro; tempo de SLA esta definido; fila destino existe e prepara a revisao.
- Meio: A Taliya valida conversa tem status claro; tempo de SLA esta definido; fila destino existe; prioridade foi definida e prepara acompanhar SLA e ciclo de vida do atendimento. Antes de concluir, mostra impacto/preview e pede aprovacao.
- Fim: Se aprovado, a acao e concluida e auditada. Se recusado, vencido ou incompleto, criar tarefa/caso em /app/inbox; /app/tarefas; /app/hoje e manter auditoria do motivo.
- Ajustes afetados: tempo de SLA; fila destino; prioridade
- Encadeamento: /app/inbox; /app/tarefas; /app/hoje

**Autonomo com excecoes** (habilitado)

- Inicio: O fluxo comeca quando surge um caso para acompanhar SLA e ciclo de vida do atendimento. A Taliya identifica o caso e valida os dados principais: conversa tem status claro; tempo de SLA esta definido; fila destino existe.
- Meio: A Taliya executa sozinha quando conversa tem status claro; tempo de SLA esta definido; fila destino existe; prioridade foi definida; alerta ainda esta dentro da politica do studio. Ela chama a equipe quando SLA venceu; conversa ficou sem dono; prioridade ficou alta ou sensivel; fila destino nao existe; canal, cota ou permissao bloqueia alerta.
- Fim: No caso comum, a acao `acompanhar SLA e ciclo de vida do atendimento` fica registrada e auditada. Se houver excecao, criar tarefa/caso em /app/inbox; /app/tarefas; /app/hoje e manter auditoria do motivo.
- Ajustes afetados: tempo de SLA; fila destino; prioridade
- Encadeamento: /app/inbox; /app/tarefas; /app/hoje

**Autonomo** (habilitado)

- Inicio: O fluxo comeca quando surge um caso para acompanhar SLA e ciclo de vida do atendimento. A Taliya identifica o caso e confirma conversa tem status claro; tempo de SLA esta definido; fila destino existe.
- Meio: A Taliya conclui acompanhar SLA e ciclo de vida do atendimento quando conversa tem status claro; tempo de SLA esta definido; fila destino existe; prioridade foi definida; alerta ainda esta dentro da politica do studio. Ela para quando SLA venceu; conversa ficou sem dono; prioridade ficou alta ou sensivel; fila destino nao existe; canal, cota ou permissao bloqueia alerta.
- Fim: A acao e concluida, a auditoria fica salva e a continuidade segue em /app/inbox; /app/tarefas; /app/hoje. Se houver bloqueio, criar tarefa/caso em /app/inbox; /app/tarefas; /app/hoje e manter auditoria do motivo.
- Ajustes afetados: tempo de SLA; fila destino; prioridade
- Encadeamento: /app/inbox; /app/tarefas; /app/hoje


## Agente: Agenda


### Rotina: Presenca e faltas


#### Confirmacao de presenca

**Manual** (habilitado)

- Inicio: O fluxo comeca quando surge um caso para enviar confirmacao de presenca e registrar resposta. A Taliya identifica o caso e organiza o contexto principal: aula existe na agenda; aluno esta vinculado a aula; horario do lembrete chegou.
- Meio: A Taliya cria tarefa, checklist ou caso para a equipe enviar confirmacao de presenca e registrar resposta. A decisao e a execucao principal ficam com o humano.
- Fim: O fluxo termina quando a equipe registra o resultado. A Taliya salva auditoria e, se nao puder seguir, criar tarefa/caso em /app/agenda; /app/aulas/[id]; execucao e manter auditoria do motivo.
- Ajustes afetados: horario do lembrete; tom/template; limite por aula
- Encadeamento: /app/agenda; /app/aulas/[id]; execucao

**Copiloto** (habilitado)

- Inicio: O fluxo comeca quando surge um caso para enviar confirmacao de presenca e registrar resposta. A Taliya identifica o contexto e mostra a base da sugestao: aula existe na agenda; aluno esta vinculado a aula; horario do lembrete chegou.
- Meio: A Taliya sugere enviar confirmacao de presenca e registrar resposta, prepara texto/resumo/proximo passo e mostra os dados usados. A equipe pode aceitar, editar ou descartar antes de executar.
- Fim: Se a equipe aceitar, a acao e registrada conforme a decisao humana. Se editar ou descartar, a Taliya registra a decisao e mantem continuidade em /app/agenda; /app/aulas/[id]; execucao.
- Ajustes afetados: horario do lembrete; tom/template; limite por aula
- Encadeamento: /app/agenda; /app/aulas/[id]; execucao

**Autonomo com aprovacao** (habilitado)

- Inicio: O fluxo comeca quando surge um caso para enviar confirmacao de presenca e registrar resposta. A Taliya identifica o caso, confere aula existe na agenda; aluno esta vinculado a aula; horario do lembrete chegou e prepara a revisao.
- Meio: A Taliya valida aula existe na agenda; aluno esta vinculado a aula; horario do lembrete chegou; template aprovado esta disponivel e prepara enviar confirmacao de presenca e registrar resposta. Antes de concluir, mostra impacto/preview e pede aprovacao.
- Fim: Se aprovado, a acao e concluida e auditada. Se recusado, vencido ou incompleto, criar tarefa/caso em /app/agenda; /app/aulas/[id]; execucao e manter auditoria do motivo.
- Ajustes afetados: horario do lembrete; tom/template; limite por aula
- Encadeamento: /app/agenda; /app/aulas/[id]; execucao

**Autonomo com excecoes** (habilitado)

- Inicio: O fluxo comeca quando surge um caso para enviar confirmacao de presenca e registrar resposta. A Taliya identifica o caso e valida os dados principais: aula existe na agenda; aluno esta vinculado a aula; horario do lembrete chegou.
- Meio: A Taliya executa sozinha quando aula existe na agenda; aluno esta vinculado a aula; horario do lembrete chegou; template aprovado esta disponivel; limite por aula nao foi atingido. Ela chama a equipe quando aula foi alterada ou cancelada; aluno nao esta identificado; ja existe resposta conflitante; aluno pede excecao ou troca; WhatsApp, cota ou permissao bloqueia envio.
- Fim: No caso comum, a acao `enviar confirmacao de presenca e registrar resposta` fica registrada e auditada. Se houver excecao, criar tarefa/caso em /app/agenda; /app/aulas/[id]; execucao e manter auditoria do motivo.
- Ajustes afetados: horario do lembrete; tom/template; limite por aula
- Encadeamento: /app/agenda; /app/aulas/[id]; execucao

**Autonomo** (habilitado)

- Inicio: O fluxo comeca quando surge um caso para enviar confirmacao de presenca e registrar resposta. A Taliya identifica o caso e confirma aula existe na agenda; aluno esta vinculado a aula; horario do lembrete chegou.
- Meio: A Taliya conclui enviar confirmacao de presenca e registrar resposta quando aula existe na agenda; aluno esta vinculado a aula; horario do lembrete chegou; template aprovado esta disponivel; limite por aula nao foi atingido. Ela para quando aula foi alterada ou cancelada; aluno nao esta identificado; ja existe resposta conflitante; aluno pede excecao ou troca; WhatsApp, cota ou permissao bloqueia envio.
- Fim: A acao e concluida, a auditoria fica salva e a continuidade segue em /app/agenda; /app/aulas/[id]; execucao. Se houver bloqueio, criar tarefa/caso em /app/agenda; /app/aulas/[id]; execucao e manter auditoria do motivo.
- Ajustes afetados: horario do lembrete; tom/template; limite por aula
- Encadeamento: /app/agenda; /app/aulas/[id]; execucao


#### Falta com aviso

**Manual** (habilitado)

- Inicio: O fluxo comeca quando surge um caso para registrar falta avisada e encaminhar o proximo passo. A Taliya identifica o caso e organiza o contexto principal: aluno foi identificado; aula existe na agenda; aviso chegou ate o prazo configurado.
- Meio: A Taliya cria tarefa, checklist ou caso para a equipe registrar falta avisada e encaminhar o proximo passo. A decisao e a execucao principal ficam com o humano.
- Fim: O fluxo termina quando a equipe registra o resultado. A Taliya salva auditoria e, se nao puder seguir, criar tarefa/caso em /app/reposicoes; /app/aulas/[id]; tarefa e manter auditoria do motivo.
- Ajustes afetados: prazo para aviso; proximo passo apos falta; responsaveis por excecao; tom/template da mensagem
- Encadeamento: /app/reposicoes; /app/aulas/[id]; tarefa

**Copiloto** (habilitado)

- Inicio: O fluxo comeca quando surge um caso para registrar falta avisada e encaminhar o proximo passo. A Taliya identifica o contexto e mostra a base da sugestao: aluno foi identificado; aula existe na agenda; aviso chegou ate o prazo configurado.
- Meio: A Taliya sugere registrar falta avisada e encaminhar o proximo passo, prepara texto/resumo/proximo passo e mostra os dados usados. A equipe pode aceitar, editar ou descartar antes de executar.
- Fim: Se a equipe aceitar, a acao e registrada conforme a decisao humana. Se editar ou descartar, a Taliya registra a decisao e mantem continuidade em /app/reposicoes; /app/aulas/[id]; tarefa.
- Ajustes afetados: prazo para aviso; proximo passo apos falta; responsaveis por excecao; tom/template da mensagem
- Encadeamento: /app/reposicoes; /app/aulas/[id]; tarefa

**Autonomo com aprovacao** (habilitado)

- Inicio: O fluxo comeca quando surge um caso para registrar falta avisada e encaminhar o proximo passo. A Taliya identifica o caso, confere aluno foi identificado; aula existe na agenda; aviso chegou ate o prazo configurado e prepara a revisao.
- Meio: A Taliya valida aluno foi identificado; aula existe na agenda; aviso chegou ate o prazo configurado; falta ainda nao foi registrada e prepara registrar falta avisada e encaminhar o proximo passo. Antes de concluir, mostra impacto/preview e pede aprovacao.
- Fim: Se aprovado, a acao e concluida e auditada. Se recusado, vencido ou incompleto, criar tarefa/caso em /app/reposicoes; /app/aulas/[id]; tarefa e manter auditoria do motivo.
- Ajustes afetados: prazo para aviso; proximo passo apos falta; responsaveis por excecao; tom/template da mensagem
- Encadeamento: /app/reposicoes; /app/aulas/[id]; tarefa

**Autonomo com excecoes** (habilitado)

- Inicio: O fluxo comeca quando surge um caso para registrar falta avisada e encaminhar o proximo passo. A Taliya identifica o caso e valida os dados principais: aluno foi identificado; aula existe na agenda; aviso chegou ate o prazo configurado.
- Meio: A Taliya executa sozinha quando aluno foi identificado; aula existe na agenda; aviso chegou ate o prazo configurado; falta ainda nao foi registrada; mensagem usa template aprovado. Ela chama a equipe quando aviso chega fora do prazo; nao encontra aluno ou aula; falta ja foi registrada; aluno pede excecao, credito, cancelamento ou reclama; WhatsApp, cota ou permissao bloqueiam o envio.
- Fim: No caso comum, a acao `registrar falta avisada e encaminhar o proximo passo` fica registrada e auditada. Se houver excecao, criar tarefa/caso em /app/reposicoes; /app/aulas/[id]; tarefa e manter auditoria do motivo.
- Ajustes afetados: prazo para aviso; proximo passo apos falta; responsaveis por excecao; tom/template da mensagem
- Encadeamento: /app/reposicoes; /app/aulas/[id]; tarefa

**Autonomo** (bloqueado)

- Inicio: Este modo fica bloqueado para Falta com aviso.
- Meio: A Taliya nao conclui end-to-end porque este modo esta acima do teto do fluxo.
- Fim: Use o maior modo habilitado para automatizar o caso comum sem ultrapassar os limites publicados.
- Ajustes afetados: prazo para aviso; proximo passo apos falta; responsaveis por excecao; tom/template da mensagem
- Encadeamento: /app/reposicoes; /app/aulas/[id]; tarefa


#### Falta sem aviso

**Manual** (habilitado)

- Inicio: O fluxo comeca quando surge um caso para detectar falta sem aviso e abrir recuperacao ou tarefa. A Taliya identifica o caso e organiza o contexto principal: aula terminou; aluno estava previsto na chamada; presenca nao foi registrada.
- Meio: A Taliya cria tarefa, checklist ou caso para a equipe detectar falta sem aviso e abrir recuperacao ou tarefa. A decisao e a execucao principal ficam com o humano.
- Fim: O fluxo termina quando a equipe registra o resultado. A Taliya salva auditoria e, se nao puder seguir, criar tarefa/caso em /app/aulas/[id]; /app/retencao; tarefa e manter auditoria do motivo.
- Ajustes afetados: quando vira tarefa de retencao; responsavel
- Encadeamento: /app/aulas/[id]; /app/retencao; tarefa

**Copiloto** (habilitado)

- Inicio: O fluxo comeca quando surge um caso para detectar falta sem aviso e abrir recuperacao ou tarefa. A Taliya identifica o contexto e mostra a base da sugestao: aula terminou; aluno estava previsto na chamada; presenca nao foi registrada.
- Meio: A Taliya sugere detectar falta sem aviso e abrir recuperacao ou tarefa, prepara texto/resumo/proximo passo e mostra os dados usados. A equipe pode aceitar, editar ou descartar antes de executar.
- Fim: Se a equipe aceitar, a acao e registrada conforme a decisao humana. Se editar ou descartar, a Taliya registra a decisao e mantem continuidade em /app/aulas/[id]; /app/retencao; tarefa.
- Ajustes afetados: quando vira tarefa de retencao; responsavel
- Encadeamento: /app/aulas/[id]; /app/retencao; tarefa

**Autonomo com aprovacao** (habilitado)

- Inicio: O fluxo comeca quando surge um caso para detectar falta sem aviso e abrir recuperacao ou tarefa. A Taliya identifica o caso, confere aula terminou; aluno estava previsto na chamada; presenca nao foi registrada e prepara a revisao.
- Meio: A Taliya valida aula terminou; aluno estava previsto na chamada; presenca nao foi registrada; janela de tolerancia passou e prepara detectar falta sem aviso e abrir recuperacao ou tarefa. Antes de concluir, mostra impacto/preview e pede aprovacao.
- Fim: Se aprovado, a acao e concluida e auditada. Se recusado, vencido ou incompleto, criar tarefa/caso em /app/aulas/[id]; /app/retencao; tarefa e manter auditoria do motivo.
- Ajustes afetados: quando vira tarefa de retencao; responsavel
- Encadeamento: /app/aulas/[id]; /app/retencao; tarefa

**Autonomo com excecoes** (habilitado)

- Inicio: O fluxo comeca quando surge um caso para detectar falta sem aviso e abrir recuperacao ou tarefa. A Taliya identifica o caso e valida os dados principais: aula terminou; aluno estava previsto na chamada; presenca nao foi registrada.
- Meio: A Taliya executa sozinha quando aula terminou; aluno estava previsto na chamada; presenca nao foi registrada; janela de tolerancia passou; responsavel de acompanhamento esta definido. Ela chama a equipe quando professor ainda nao fechou chamada; aluno avisou por outro canal; ha conflito de presenca; caso tem recorrencia ou risco de cancelamento; canal, cota ou permissao bloqueia contato.
- Fim: No caso comum, a acao `detectar falta sem aviso e abrir recuperacao ou tarefa` fica registrada e auditada. Se houver excecao, criar tarefa/caso em /app/aulas/[id]; /app/retencao; tarefa e manter auditoria do motivo.
- Ajustes afetados: quando vira tarefa de retencao; responsavel
- Encadeamento: /app/aulas/[id]; /app/retencao; tarefa

**Autonomo** (bloqueado)

- Inicio: Este modo fica bloqueado para Falta sem aviso.
- Meio: A Taliya nao conclui end-to-end porque este modo esta acima do teto do fluxo.
- Fim: Use o maior modo habilitado para automatizar o caso comum sem ultrapassar os limites publicados.
- Ajustes afetados: quando vira tarefa de retencao; responsavel
- Encadeamento: /app/aulas/[id]; /app/retencao; tarefa


### Rotina: Vagas, reposicoes e lista de espera


#### Recuperar vaga aberta

**Manual** (habilitado)

- Inicio: O fluxo comeca quando surge um caso para usar vaga aberta para convidar aluno elegivel. A Taliya identifica o caso e organiza o contexto principal: vaga abriu em aula real; prioridade da lista esta definida; aluno elegivel tem credito ou direito.
- Meio: A Taliya cria tarefa, checklist ou caso para a equipe usar vaga aberta para convidar aluno elegivel. A decisao e a execucao principal ficam com o humano.
- Fim: O fluxo termina quando a equipe registra o resultado. A Taliya salva auditoria e, se nao puder seguir, criar tarefa/caso em /app/lista-espera; /app/reposicoes; aprovacao/tarefa e manter auditoria do motivo.
- Ajustes afetados: prioridade da lista; limite de convites; aprovador se lote
- Encadeamento: /app/lista-espera; /app/reposicoes; aprovacao/tarefa

**Copiloto** (habilitado)

- Inicio: O fluxo comeca quando surge um caso para usar vaga aberta para convidar aluno elegivel. A Taliya identifica o contexto e mostra a base da sugestao: vaga abriu em aula real; prioridade da lista esta definida; aluno elegivel tem credito ou direito.
- Meio: A Taliya sugere usar vaga aberta para convidar aluno elegivel, prepara texto/resumo/proximo passo e mostra os dados usados. A equipe pode aceitar, editar ou descartar antes de executar.
- Fim: Se a equipe aceitar, a acao e registrada conforme a decisao humana. Se editar ou descartar, a Taliya registra a decisao e mantem continuidade em /app/lista-espera; /app/reposicoes; aprovacao/tarefa.
- Ajustes afetados: prioridade da lista; limite de convites; aprovador se lote
- Encadeamento: /app/lista-espera; /app/reposicoes; aprovacao/tarefa

**Autonomo com aprovacao** (habilitado)

- Inicio: O fluxo comeca quando surge um caso para usar vaga aberta para convidar aluno elegivel. A Taliya identifica o caso, confere vaga abriu em aula real; prioridade da lista esta definida; aluno elegivel tem credito ou direito e prepara a revisao.
- Meio: A Taliya valida vaga abriu em aula real; prioridade da lista esta definida; aluno elegivel tem credito ou direito; limite de convites nao foi atingido e prepara usar vaga aberta para convidar aluno elegivel. Antes de concluir, mostra impacto/preview e pede aprovacao.
- Fim: Se aprovado, a acao e concluida e auditada. Se recusado, vencido ou incompleto, criar tarefa/caso em /app/lista-espera; /app/reposicoes; aprovacao/tarefa e manter auditoria do motivo.
- Ajustes afetados: prioridade da lista; limite de convites; aprovador se lote
- Encadeamento: /app/lista-espera; /app/reposicoes; aprovacao/tarefa

**Autonomo com excecoes** (habilitado)

- Inicio: O fluxo comeca quando surge um caso para usar vaga aberta para convidar aluno elegivel. A Taliya identifica o caso e valida os dados principais: vaga abriu em aula real; prioridade da lista esta definida; aluno elegivel tem credito ou direito.
- Meio: A Taliya executa sozinha quando vaga abriu em aula real; prioridade da lista esta definida; aluno elegivel tem credito ou direito; limite de convites nao foi atingido; convite usa mensagem aprovada. Ela chama a equipe quando vaga fecha antes da resposta; ha empate ou lote grande; aluno nao tem credito claro; convite pode furar prioridade; canal, cota ou permissao bloqueia envio.
- Fim: No caso comum, a acao `usar vaga aberta para convidar aluno elegivel` fica registrada e auditada. Se houver excecao, criar tarefa/caso em /app/lista-espera; /app/reposicoes; aprovacao/tarefa e manter auditoria do motivo.
- Ajustes afetados: prioridade da lista; limite de convites; aprovador se lote
- Encadeamento: /app/lista-espera; /app/reposicoes; aprovacao/tarefa

**Autonomo** (bloqueado)

- Inicio: Este modo fica bloqueado para Recuperar vaga aberta.
- Meio: A Taliya nao conclui end-to-end porque este modo esta acima do teto do fluxo.
- Fim: Use o maior modo habilitado para automatizar o caso comum sem ultrapassar os limites publicados.
- Ajustes afetados: prioridade da lista; limite de convites; aprovador se lote
- Encadeamento: /app/lista-espera; /app/reposicoes; aprovacao/tarefa


#### Reposicao/remarcacao

**Manual** (habilitado)

- Inicio: O fluxo comeca quando surge um caso para preparar reposicao ou remarcacao para aprovacao. A Taliya identifica o caso e organiza o contexto principal: credito de reposicao existe; aula de destino tem capacidade; prazo da politica esta valido.
- Meio: A Taliya cria tarefa, checklist ou caso para a equipe preparar reposicao ou remarcacao para aprovacao. A decisao e a execucao principal ficam com o humano.
- Fim: O fluxo termina quando a equipe registra o resultado. A Taliya salva auditoria e, se nao puder seguir, criar tarefa/caso em /app/reposicoes; /app/agenda; aprovacao e manter auditoria do motivo.
- Ajustes afetados: aprovador; prazo maximo da reposicao; responsavel por excecao
- Encadeamento: /app/reposicoes; /app/agenda; aprovacao

**Copiloto** (habilitado)

- Inicio: O fluxo comeca quando surge um caso para preparar reposicao ou remarcacao para aprovacao. A Taliya identifica o contexto e mostra a base da sugestao: credito de reposicao existe; aula de destino tem capacidade; prazo da politica esta valido.
- Meio: A Taliya sugere preparar reposicao ou remarcacao para aprovacao, prepara texto/resumo/proximo passo e mostra os dados usados. A equipe pode aceitar, editar ou descartar antes de executar.
- Fim: Se a equipe aceitar, a acao e registrada conforme a decisao humana. Se editar ou descartar, a Taliya registra a decisao e mantem continuidade em /app/reposicoes; /app/agenda; aprovacao.
- Ajustes afetados: aprovador; prazo maximo da reposicao; responsavel por excecao
- Encadeamento: /app/reposicoes; /app/agenda; aprovacao

**Autonomo com aprovacao** (habilitado)

- Inicio: O fluxo comeca quando surge um caso para preparar reposicao ou remarcacao para aprovacao. A Taliya identifica o caso, confere credito de reposicao existe; aula de destino tem capacidade; prazo da politica esta valido e prepara a revisao.
- Meio: A Taliya valida credito de reposicao existe; aula de destino tem capacidade; prazo da politica esta valido; impacto na agenda foi calculado e prepara preparar reposicao ou remarcacao para aprovacao. Antes de concluir, mostra impacto/preview e pede aprovacao.
- Fim: Se aprovado, a acao e concluida e auditada. Se recusado, vencido ou incompleto, criar tarefa/caso em /app/reposicoes; /app/agenda; aprovacao e manter auditoria do motivo.
- Ajustes afetados: aprovador; prazo maximo da reposicao; responsavel por excecao
- Encadeamento: /app/reposicoes; /app/agenda; aprovacao

**Autonomo com excecoes** (bloqueado)

- Inicio: Este modo fica bloqueado para Reposicao/remarcacao.
- Meio: A Taliya nao executa com excecoes porque o teto deste fluxo e menor.
- Fim: O usuario deve escolher um modo permitido para este fluxo.
- Ajustes afetados: aprovador; prazo maximo da reposicao; responsavel por excecao
- Encadeamento: /app/reposicoes; /app/agenda; aprovacao

**Autonomo** (bloqueado)

- Inicio: Este modo fica bloqueado para Reposicao/remarcacao.
- Meio: A Taliya nao conclui end-to-end porque este modo esta acima do teto do fluxo.
- Fim: Use o maior modo habilitado para automatizar o caso comum sem ultrapassar os limites publicados.
- Ajustes afetados: aprovador; prazo maximo da reposicao; responsavel por excecao
- Encadeamento: /app/reposicoes; /app/agenda; aprovacao


#### Lista de espera

**Manual** (habilitado)

- Inicio: O fluxo comeca quando surge um caso para gerenciar lista de espera e convites. A Taliya identifica o caso e organiza o contexto principal: lista de espera existe; prioridade foi calculada; vaga compativel apareceu.
- Meio: A Taliya cria tarefa, checklist ou caso para a equipe gerenciar lista de espera e convites. A decisao e a execucao principal ficam com o humano.
- Fim: O fluxo termina quando a equipe registra o resultado. A Taliya salva auditoria e, se nao puder seguir, criar tarefa/caso em /app/lista-espera; /app/tarefas e manter auditoria do motivo.
- Ajustes afetados: prioridade; limite de convites; responsavel por excecao
- Encadeamento: /app/lista-espera; /app/tarefas

**Copiloto** (habilitado)

- Inicio: O fluxo comeca quando surge um caso para gerenciar lista de espera e convites. A Taliya identifica o contexto e mostra a base da sugestao: lista de espera existe; prioridade foi calculada; vaga compativel apareceu.
- Meio: A Taliya sugere gerenciar lista de espera e convites, prepara texto/resumo/proximo passo e mostra os dados usados. A equipe pode aceitar, editar ou descartar antes de executar.
- Fim: Se a equipe aceitar, a acao e registrada conforme a decisao humana. Se editar ou descartar, a Taliya registra a decisao e mantem continuidade em /app/lista-espera; /app/tarefas.
- Ajustes afetados: prioridade; limite de convites; responsavel por excecao
- Encadeamento: /app/lista-espera; /app/tarefas

**Autonomo com aprovacao** (habilitado)

- Inicio: O fluxo comeca quando surge um caso para gerenciar lista de espera e convites. A Taliya identifica o caso, confere lista de espera existe; prioridade foi calculada; vaga compativel apareceu e prepara a revisao.
- Meio: A Taliya valida lista de espera existe; prioridade foi calculada; vaga compativel apareceu; limite de convites permite contato e prepara gerenciar lista de espera e convites. Antes de concluir, mostra impacto/preview e pede aprovacao.
- Fim: Se aprovado, a acao e concluida e auditada. Se recusado, vencido ou incompleto, criar tarefa/caso em /app/lista-espera; /app/tarefas e manter auditoria do motivo.
- Ajustes afetados: prioridade; limite de convites; responsavel por excecao
- Encadeamento: /app/lista-espera; /app/tarefas

**Autonomo com excecoes** (habilitado)

- Inicio: O fluxo comeca quando surge um caso para gerenciar lista de espera e convites. A Taliya identifica o caso e valida os dados principais: lista de espera existe; prioridade foi calculada; vaga compativel apareceu.
- Meio: A Taliya executa sozinha quando lista de espera existe; prioridade foi calculada; vaga compativel apareceu; limite de convites permite contato; responsavel por excecao esta definido. Ela chama a equipe quando prioridade empata; aluno nao responde no prazo; vaga deixa de existir; pedido envolve excecao de credito; canal, cota ou permissao bloqueia envio.
- Fim: No caso comum, a acao `gerenciar lista de espera e convites` fica registrada e auditada. Se houver excecao, criar tarefa/caso em /app/lista-espera; /app/tarefas e manter auditoria do motivo.
- Ajustes afetados: prioridade; limite de convites; responsavel por excecao
- Encadeamento: /app/lista-espera; /app/tarefas

**Autonomo** (bloqueado)

- Inicio: Este modo fica bloqueado para Lista de espera.
- Meio: A Taliya nao conclui end-to-end porque este modo esta acima do teto do fluxo.
- Fim: Use o maior modo habilitado para automatizar o caso comum sem ultrapassar os limites publicados.
- Ajustes afetados: prioridade; limite de convites; responsavel por excecao
- Encadeamento: /app/lista-espera; /app/tarefas


### Rotina: Agenda experimental


#### Disponibilidade experimental

**Manual** (habilitado)

- Inicio: O fluxo comeca quando surge um caso para oferecer disponibilidade para aula experimental. A Taliya identifica o caso e organiza o contexto principal: interessado esta identificado; horarios oferecidos estao livres; responsavel comercial esta definido.
- Meio: A Taliya cria tarefa, checklist ou caso para a equipe oferecer disponibilidade para aula experimental. A decisao e a execucao principal ficam com o humano.
- Fim: O fluxo termina quando a equipe registra o resultado. A Taliya salva auditoria e, se nao puder seguir, criar tarefa/caso em /app/experimental; /app/agenda; tarefa e manter auditoria do motivo.
- Ajustes afetados: responsavel comercial; horarios oferecidos; quando chamar humano
- Encadeamento: /app/experimental; /app/agenda; tarefa

**Copiloto** (habilitado)

- Inicio: O fluxo comeca quando surge um caso para oferecer disponibilidade para aula experimental. A Taliya identifica o contexto e mostra a base da sugestao: interessado esta identificado; horarios oferecidos estao livres; responsavel comercial esta definido.
- Meio: A Taliya sugere oferecer disponibilidade para aula experimental, prepara texto/resumo/proximo passo e mostra os dados usados. A equipe pode aceitar, editar ou descartar antes de executar.
- Fim: Se a equipe aceitar, a acao e registrada conforme a decisao humana. Se editar ou descartar, a Taliya registra a decisao e mantem continuidade em /app/experimental; /app/agenda; tarefa.
- Ajustes afetados: responsavel comercial; horarios oferecidos; quando chamar humano
- Encadeamento: /app/experimental; /app/agenda; tarefa

**Autonomo com aprovacao** (habilitado)

- Inicio: O fluxo comeca quando surge um caso para oferecer disponibilidade para aula experimental. A Taliya identifica o caso, confere interessado esta identificado; horarios oferecidos estao livres; responsavel comercial esta definido e prepara a revisao.
- Meio: A Taliya valida interessado esta identificado; horarios oferecidos estao livres; responsavel comercial esta definido; limite de tentativas nao foi atingido e prepara oferecer disponibilidade para aula experimental. Antes de concluir, mostra impacto/preview e pede aprovacao.
- Fim: Se aprovado, a acao e concluida e auditada. Se recusado, vencido ou incompleto, criar tarefa/caso em /app/experimental; /app/agenda; tarefa e manter auditoria do motivo.
- Ajustes afetados: responsavel comercial; horarios oferecidos; quando chamar humano
- Encadeamento: /app/experimental; /app/agenda; tarefa

**Autonomo com excecoes** (habilitado)

- Inicio: O fluxo comeca quando surge um caso para oferecer disponibilidade para aula experimental. A Taliya identifica o caso e valida os dados principais: interessado esta identificado; horarios oferecidos estao livres; responsavel comercial esta definido.
- Meio: A Taliya executa sozinha quando interessado esta identificado; horarios oferecidos estao livres; responsavel comercial esta definido; limite de tentativas nao foi atingido; mensagem aprovada esta disponivel. Ela chama a equipe quando interessado pede horario fora da regra; nao ha vaga compativel; lead ja tem experimental marcada; pedido envolve desconto ou excecao; canal, cota ou permissao bloqueia envio.
- Fim: No caso comum, a acao `oferecer disponibilidade para aula experimental` fica registrada e auditada. Se houver excecao, criar tarefa/caso em /app/experimental; /app/agenda; tarefa e manter auditoria do motivo.
- Ajustes afetados: responsavel comercial; horarios oferecidos; quando chamar humano
- Encadeamento: /app/experimental; /app/agenda; tarefa

**Autonomo** (bloqueado)

- Inicio: Este modo fica bloqueado para Disponibilidade experimental.
- Meio: A Taliya nao conclui end-to-end porque este modo esta acima do teto do fluxo.
- Fim: Use o maior modo habilitado para automatizar o caso comum sem ultrapassar os limites publicados.
- Ajustes afetados: responsavel comercial; horarios oferecidos; quando chamar humano
- Encadeamento: /app/experimental; /app/agenda; tarefa


### Rotina: Grade e capacidade


#### Mudanca horario fixo

**Manual** (habilitado)

- Inicio: O fluxo comeca quando surge um caso para preparar mudanca de horario fixo para aprovacao. A Taliya identifica o caso e organiza o contexto principal: aluno e horario fixo foram identificados; novo horario existe; impacto em turma e capacidade foi calculado.
- Meio: A Taliya cria tarefa, checklist ou caso para a equipe preparar mudanca de horario fixo para aprovacao. A decisao e a execucao principal ficam com o humano.
- Fim: O fluxo termina quando a equipe registra o resultado. A Taliya salva auditoria e, se nao puder seguir, criar tarefa/caso em /app/alunos/[id]; /app/agenda; aprovacao e manter auditoria do motivo.
- Ajustes afetados: aprovador; prazo; mensagem de confirmacao
- Encadeamento: /app/alunos/[id]; /app/agenda; aprovacao

**Copiloto** (habilitado)

- Inicio: O fluxo comeca quando surge um caso para preparar mudanca de horario fixo para aprovacao. A Taliya identifica o contexto e mostra a base da sugestao: aluno e horario fixo foram identificados; novo horario existe; impacto em turma e capacidade foi calculado.
- Meio: A Taliya sugere preparar mudanca de horario fixo para aprovacao, prepara texto/resumo/proximo passo e mostra os dados usados. A equipe pode aceitar, editar ou descartar antes de executar.
- Fim: Se a equipe aceitar, a acao e registrada conforme a decisao humana. Se editar ou descartar, a Taliya registra a decisao e mantem continuidade em /app/alunos/[id]; /app/agenda; aprovacao.
- Ajustes afetados: aprovador; prazo; mensagem de confirmacao
- Encadeamento: /app/alunos/[id]; /app/agenda; aprovacao

**Autonomo com aprovacao** (habilitado)

- Inicio: O fluxo comeca quando surge um caso para preparar mudanca de horario fixo para aprovacao. A Taliya identifica o caso, confere aluno e horario fixo foram identificados; novo horario existe; impacto em turma e capacidade foi calculado e prepara a revisao.
- Meio: A Taliya valida aluno e horario fixo foram identificados; novo horario existe; impacto em turma e capacidade foi calculado; mensagem de confirmacao esta pronta e prepara preparar mudanca de horario fixo para aprovacao. Antes de concluir, mostra impacto/preview e pede aprovacao.
- Fim: Se aprovado, a acao e concluida e auditada. Se recusado, vencido ou incompleto, criar tarefa/caso em /app/alunos/[id]; /app/agenda; aprovacao e manter auditoria do motivo.
- Ajustes afetados: aprovador; prazo; mensagem de confirmacao
- Encadeamento: /app/alunos/[id]; /app/agenda; aprovacao

**Autonomo com excecoes** (bloqueado)

- Inicio: Este modo fica bloqueado para Mudanca horario fixo.
- Meio: A Taliya nao executa com excecoes porque o teto deste fluxo e menor.
- Fim: O usuario deve escolher um modo permitido para este fluxo.
- Ajustes afetados: aprovador; prazo; mensagem de confirmacao
- Encadeamento: /app/alunos/[id]; /app/agenda; aprovacao

**Autonomo** (bloqueado)

- Inicio: Este modo fica bloqueado para Mudanca horario fixo.
- Meio: A Taliya nao conclui end-to-end porque este modo esta acima do teto do fluxo.
- Fim: Use o maior modo habilitado para automatizar o caso comum sem ultrapassar os limites publicados.
- Ajustes afetados: aprovador; prazo; mensagem de confirmacao
- Encadeamento: /app/alunos/[id]; /app/agenda; aprovacao


#### Cancelamento pelo studio

**Manual** (habilitado)

- Inicio: O fluxo comeca quando surge um caso para preparar cancelamento pelo studio e comunicado. A Taliya identifica o caso e organiza o contexto principal: aula a cancelar existe; motivo foi informado; alunos afetados foram listados.
- Meio: A Taliya cria tarefa, checklist ou caso para a equipe preparar cancelamento pelo studio e comunicado. A decisao e a execucao principal ficam com o humano.
- Fim: O fluxo termina quando a equipe registra o resultado. A Taliya salva auditoria e, se nao puder seguir, criar tarefa/caso em /app/aulas/[id]; /app/aprovacoes; /app/hoje e manter auditoria do motivo.
- Ajustes afetados: aprovador; template de comunicado; quem trata excecoes
- Encadeamento: /app/aulas/[id]; /app/aprovacoes; /app/hoje

**Copiloto** (habilitado)

- Inicio: O fluxo comeca quando surge um caso para preparar cancelamento pelo studio e comunicado. A Taliya identifica o contexto e mostra a base da sugestao: aula a cancelar existe; motivo foi informado; alunos afetados foram listados.
- Meio: A Taliya sugere preparar cancelamento pelo studio e comunicado, prepara texto/resumo/proximo passo e mostra os dados usados. A equipe pode aceitar, editar ou descartar antes de executar.
- Fim: Se a equipe aceitar, a acao e registrada conforme a decisao humana. Se editar ou descartar, a Taliya registra a decisao e mantem continuidade em /app/aulas/[id]; /app/aprovacoes; /app/hoje.
- Ajustes afetados: aprovador; template de comunicado; quem trata excecoes
- Encadeamento: /app/aulas/[id]; /app/aprovacoes; /app/hoje

**Autonomo com aprovacao** (habilitado)

- Inicio: O fluxo comeca quando surge um caso para preparar cancelamento pelo studio e comunicado. A Taliya identifica o caso, confere aula a cancelar existe; motivo foi informado; alunos afetados foram listados e prepara a revisao.
- Meio: A Taliya valida aula a cancelar existe; motivo foi informado; alunos afetados foram listados; reposicao ou credito foi calculado e prepara preparar cancelamento pelo studio e comunicado. Antes de concluir, mostra impacto/preview e pede aprovacao.
- Fim: Se aprovado, a acao e concluida e auditada. Se recusado, vencido ou incompleto, criar tarefa/caso em /app/aulas/[id]; /app/aprovacoes; /app/hoje e manter auditoria do motivo.
- Ajustes afetados: aprovador; template de comunicado; quem trata excecoes
- Encadeamento: /app/aulas/[id]; /app/aprovacoes; /app/hoje

**Autonomo com excecoes** (bloqueado)

- Inicio: Este modo fica bloqueado para Cancelamento pelo studio.
- Meio: A Taliya nao executa com excecoes porque o teto deste fluxo e menor.
- Fim: O usuario deve escolher um modo permitido para este fluxo.
- Ajustes afetados: aprovador; template de comunicado; quem trata excecoes
- Encadeamento: /app/aulas/[id]; /app/aprovacoes; /app/hoje

**Autonomo** (bloqueado)

- Inicio: Este modo fica bloqueado para Cancelamento pelo studio.
- Meio: A Taliya nao conclui end-to-end porque este modo esta acima do teto do fluxo.
- Fim: Use o maior modo habilitado para automatizar o caso comum sem ultrapassar os limites publicados.
- Ajustes afetados: aprovador; template de comunicado; quem trata excecoes
- Encadeamento: /app/aulas/[id]; /app/aprovacoes; /app/hoje


#### Conflito capacidade

**Manual** (habilitado)

- Inicio: O fluxo comeca quando surge um caso para resolver conflito de capacidade com aprovacao. A Taliya identifica o caso e organiza o contexto principal: turma ou aula foi identificada; capacidade publicada existe; conflito foi calculado.
- Meio: A Taliya cria tarefa, checklist ou caso para a equipe resolver conflito de capacidade com aprovacao. A decisao e a execucao principal ficam com o humano.
- Fim: O fluxo termina quando a equipe registra o resultado. A Taliya salva auditoria e, se nao puder seguir, criar tarefa/caso em /app/turmas/[id]; /app/agenda; caso operacional e manter auditoria do motivo.
- Ajustes afetados: aprovador; responsavel do caso; prioridade
- Encadeamento: /app/turmas/[id]; /app/agenda; caso operacional

**Copiloto** (habilitado)

- Inicio: O fluxo comeca quando surge um caso para resolver conflito de capacidade com aprovacao. A Taliya identifica o contexto e mostra a base da sugestao: turma ou aula foi identificada; capacidade publicada existe; conflito foi calculado.
- Meio: A Taliya sugere resolver conflito de capacidade com aprovacao, prepara texto/resumo/proximo passo e mostra os dados usados. A equipe pode aceitar, editar ou descartar antes de executar.
- Fim: Se a equipe aceitar, a acao e registrada conforme a decisao humana. Se editar ou descartar, a Taliya registra a decisao e mantem continuidade em /app/turmas/[id]; /app/agenda; caso operacional.
- Ajustes afetados: aprovador; responsavel do caso; prioridade
- Encadeamento: /app/turmas/[id]; /app/agenda; caso operacional

**Autonomo com aprovacao** (habilitado)

- Inicio: O fluxo comeca quando surge um caso para resolver conflito de capacidade com aprovacao. A Taliya identifica o caso, confere turma ou aula foi identificada; capacidade publicada existe; conflito foi calculado e prepara a revisao.
- Meio: A Taliya valida turma ou aula foi identificada; capacidade publicada existe; conflito foi calculado; prioridade do caso foi definida e prepara resolver conflito de capacidade com aprovacao. Antes de concluir, mostra impacto/preview e pede aprovacao.
- Fim: Se aprovado, a acao e concluida e auditada. Se recusado, vencido ou incompleto, criar tarefa/caso em /app/turmas/[id]; /app/agenda; caso operacional e manter auditoria do motivo.
- Ajustes afetados: aprovador; responsavel do caso; prioridade
- Encadeamento: /app/turmas/[id]; /app/agenda; caso operacional

**Autonomo com excecoes** (bloqueado)

- Inicio: Este modo fica bloqueado para Conflito capacidade.
- Meio: A Taliya nao executa com excecoes porque o teto deste fluxo e menor.
- Fim: O usuario deve escolher um modo permitido para este fluxo.
- Ajustes afetados: aprovador; responsavel do caso; prioridade
- Encadeamento: /app/turmas/[id]; /app/agenda; caso operacional

**Autonomo** (bloqueado)

- Inicio: Este modo fica bloqueado para Conflito capacidade.
- Meio: A Taliya nao conclui end-to-end porque este modo esta acima do teto do fluxo.
- Fim: Use o maior modo habilitado para automatizar o caso comum sem ultrapassar os limites publicados.
- Ajustes afetados: aprovador; responsavel do caso; prioridade
- Encadeamento: /app/turmas/[id]; /app/agenda; caso operacional


#### Ajuste de grade

**Manual** (habilitado)

- Inicio: O fluxo comeca quando surge um caso para preparar ajuste de grade e simulacao de impacto. A Taliya identifica o caso e organiza o contexto principal: mudanca de grade foi descrita; data de vigencia esta definida; impacto em aulas, alunos e professores foi simulado.
- Meio: A Taliya cria tarefa, checklist ou caso para a equipe preparar ajuste de grade e simulacao de impacto. A decisao e a execucao principal ficam com o humano.
- Fim: O fluxo termina quando a equipe registra o resultado. A Taliya salva auditoria e, se nao puder seguir, criar tarefa/caso em /app/grade; /app/aprovacoes; /app/operacao e manter auditoria do motivo.
- Ajustes afetados: aprovador; data de vigencia; escopo da mudanca
- Encadeamento: /app/grade; /app/aprovacoes; /app/operacao

**Copiloto** (habilitado)

- Inicio: O fluxo comeca quando surge um caso para preparar ajuste de grade e simulacao de impacto. A Taliya identifica o contexto e mostra a base da sugestao: mudanca de grade foi descrita; data de vigencia esta definida; impacto em aulas, alunos e professores foi simulado.
- Meio: A Taliya sugere preparar ajuste de grade e simulacao de impacto, prepara texto/resumo/proximo passo e mostra os dados usados. A equipe pode aceitar, editar ou descartar antes de executar.
- Fim: Se a equipe aceitar, a acao e registrada conforme a decisao humana. Se editar ou descartar, a Taliya registra a decisao e mantem continuidade em /app/grade; /app/aprovacoes; /app/operacao.
- Ajustes afetados: aprovador; data de vigencia; escopo da mudanca
- Encadeamento: /app/grade; /app/aprovacoes; /app/operacao

**Autonomo com aprovacao** (habilitado)

- Inicio: O fluxo comeca quando surge um caso para preparar ajuste de grade e simulacao de impacto. A Taliya identifica o caso, confere mudanca de grade foi descrita; data de vigencia esta definida; impacto em aulas, alunos e professores foi simulado e prepara a revisao.
- Meio: A Taliya valida mudanca de grade foi descrita; data de vigencia esta definida; impacto em aulas, alunos e professores foi simulado; comunicacao necessaria foi listada e prepara preparar ajuste de grade e simulacao de impacto. Antes de concluir, mostra impacto/preview e pede aprovacao.
- Fim: Se aprovado, a acao e concluida e auditada. Se recusado, vencido ou incompleto, criar tarefa/caso em /app/grade; /app/aprovacoes; /app/operacao e manter auditoria do motivo.
- Ajustes afetados: aprovador; data de vigencia; escopo da mudanca
- Encadeamento: /app/grade; /app/aprovacoes; /app/operacao

**Autonomo com excecoes** (bloqueado)

- Inicio: Este modo fica bloqueado para Ajuste de grade.
- Meio: A Taliya nao executa com excecoes porque o teto deste fluxo e menor.
- Fim: O usuario deve escolher um modo permitido para este fluxo.
- Ajustes afetados: aprovador; data de vigencia; escopo da mudanca
- Encadeamento: /app/grade; /app/aprovacoes; /app/operacao

**Autonomo** (bloqueado)

- Inicio: Este modo fica bloqueado para Ajuste de grade.
- Meio: A Taliya nao conclui end-to-end porque este modo esta acima do teto do fluxo.
- Fim: Use o maior modo habilitado para automatizar o caso comum sem ultrapassar os limites publicados.
- Ajustes afetados: aprovador; data de vigencia; escopo da mudanca
- Encadeamento: /app/grade; /app/aprovacoes; /app/operacao


### Rotina: Agenda experimental


#### Experimental sem comparecimento

**Manual** (habilitado)

- Inicio: O fluxo comeca quando surge um caso para tratar experimental sem comparecimento. A Taliya identifica o caso e organiza o contexto principal: experimental estava marcada; lead nao compareceu; janela de tolerancia passou.
- Meio: A Taliya cria tarefa, checklist ou caso para a equipe tratar experimental sem comparecimento. A decisao e a execucao principal ficam com o humano.
- Fim: O fluxo termina quando a equipe registra o resultado. A Taliya salva auditoria e, se nao puder seguir, criar tarefa/caso em /app/experimental; /app/interessados/[id]; tarefa comercial e manter auditoria do motivo.
- Ajustes afetados: cadencia; responsavel comercial; limite de contato
- Encadeamento: /app/experimental; /app/interessados/[id]; tarefa comercial

**Copiloto** (habilitado)

- Inicio: O fluxo comeca quando surge um caso para tratar experimental sem comparecimento. A Taliya identifica o contexto e mostra a base da sugestao: experimental estava marcada; lead nao compareceu; janela de tolerancia passou.
- Meio: A Taliya sugere tratar experimental sem comparecimento, prepara texto/resumo/proximo passo e mostra os dados usados. A equipe pode aceitar, editar ou descartar antes de executar.
- Fim: Se a equipe aceitar, a acao e registrada conforme a decisao humana. Se editar ou descartar, a Taliya registra a decisao e mantem continuidade em /app/experimental; /app/interessados/[id]; tarefa comercial.
- Ajustes afetados: cadencia; responsavel comercial; limite de contato
- Encadeamento: /app/experimental; /app/interessados/[id]; tarefa comercial

**Autonomo com aprovacao** (habilitado)

- Inicio: O fluxo comeca quando surge um caso para tratar experimental sem comparecimento. A Taliya identifica o caso, confere experimental estava marcada; lead nao compareceu; janela de tolerancia passou e prepara a revisao.
- Meio: A Taliya valida experimental estava marcada; lead nao compareceu; janela de tolerancia passou; cadencia comercial esta definida e prepara tratar experimental sem comparecimento. Antes de concluir, mostra impacto/preview e pede aprovacao.
- Fim: Se aprovado, a acao e concluida e auditada. Se recusado, vencido ou incompleto, criar tarefa/caso em /app/experimental; /app/interessados/[id]; tarefa comercial e manter auditoria do motivo.
- Ajustes afetados: cadencia; responsavel comercial; limite de contato
- Encadeamento: /app/experimental; /app/interessados/[id]; tarefa comercial

**Autonomo com excecoes** (habilitado)

- Inicio: O fluxo comeca quando surge um caso para tratar experimental sem comparecimento. A Taliya identifica o caso e valida os dados principais: experimental estava marcada; lead nao compareceu; janela de tolerancia passou.
- Meio: A Taliya executa sozinha quando experimental estava marcada; lead nao compareceu; janela de tolerancia passou; cadencia comercial esta definida; limite de contato nao foi atingido. Ela chama a equipe quando lead avisou por outro canal; lead pede remarcacao fora da regra; nao ha nova vaga compativel; lead demonstra objecao sensivel; canal, cota ou permissao bloqueia contato.
- Fim: No caso comum, a acao `tratar experimental sem comparecimento` fica registrada e auditada. Se houver excecao, criar tarefa/caso em /app/experimental; /app/interessados/[id]; tarefa comercial e manter auditoria do motivo.
- Ajustes afetados: cadencia; responsavel comercial; limite de contato
- Encadeamento: /app/experimental; /app/interessados/[id]; tarefa comercial

**Autonomo** (bloqueado)

- Inicio: Este modo fica bloqueado para Experimental sem comparecimento.
- Meio: A Taliya nao conclui end-to-end porque este modo esta acima do teto do fluxo.
- Fim: Use o maior modo habilitado para automatizar o caso comum sem ultrapassar os limites publicados.
- Ajustes afetados: cadencia; responsavel comercial; limite de contato
- Encadeamento: /app/experimental; /app/interessados/[id]; tarefa comercial


### Rotina: Vagas, reposicoes e lista de espera


#### Creditos reposicao

**Manual** (habilitado)

- Inicio: O fluxo comeca quando surge um caso para preparar credito de reposicao para aprovacao. A Taliya identifica o caso e organiza o contexto principal: falta ou remarcacao geradora foi identificada; validade proposta esta definida; politica de credito esta publicada.
- Meio: A Taliya cria tarefa, checklist ou caso para a equipe preparar credito de reposicao para aprovacao. A decisao e a execucao principal ficam com o humano.
- Fim: O fluxo termina quando a equipe registra o resultado. A Taliya salva auditoria e, se nao puder seguir, criar tarefa/caso em /app/creditos-reposicao; /app/aprovacoes e manter auditoria do motivo.
- Ajustes afetados: aprovador; validade do credito; responsavel por excecao
- Encadeamento: /app/creditos-reposicao; /app/aprovacoes

**Copiloto** (habilitado)

- Inicio: O fluxo comeca quando surge um caso para preparar credito de reposicao para aprovacao. A Taliya identifica o contexto e mostra a base da sugestao: falta ou remarcacao geradora foi identificada; validade proposta esta definida; politica de credito esta publicada.
- Meio: A Taliya sugere preparar credito de reposicao para aprovacao, prepara texto/resumo/proximo passo e mostra os dados usados. A equipe pode aceitar, editar ou descartar antes de executar.
- Fim: Se a equipe aceitar, a acao e registrada conforme a decisao humana. Se editar ou descartar, a Taliya registra a decisao e mantem continuidade em /app/creditos-reposicao; /app/aprovacoes.
- Ajustes afetados: aprovador; validade do credito; responsavel por excecao
- Encadeamento: /app/creditos-reposicao; /app/aprovacoes

**Autonomo com aprovacao** (habilitado)

- Inicio: O fluxo comeca quando surge um caso para preparar credito de reposicao para aprovacao. A Taliya identifica o caso, confere falta ou remarcacao geradora foi identificada; validade proposta esta definida; politica de credito esta publicada e prepara a revisao.
- Meio: A Taliya valida falta ou remarcacao geradora foi identificada; validade proposta esta definida; politica de credito esta publicada; destino de excecoes esta definido e prepara preparar credito de reposicao para aprovacao. Antes de concluir, mostra impacto/preview e pede aprovacao.
- Fim: Se aprovado, a acao e concluida e auditada. Se recusado, vencido ou incompleto, criar tarefa/caso em /app/creditos-reposicao; /app/aprovacoes e manter auditoria do motivo.
- Ajustes afetados: aprovador; validade do credito; responsavel por excecao
- Encadeamento: /app/creditos-reposicao; /app/aprovacoes

**Autonomo com excecoes** (bloqueado)

- Inicio: Este modo fica bloqueado para Creditos reposicao.
- Meio: A Taliya nao executa com excecoes porque o teto deste fluxo e menor.
- Fim: O usuario deve escolher um modo permitido para este fluxo.
- Ajustes afetados: aprovador; validade do credito; responsavel por excecao
- Encadeamento: /app/creditos-reposicao; /app/aprovacoes

**Autonomo** (bloqueado)

- Inicio: Este modo fica bloqueado para Creditos reposicao.
- Meio: A Taliya nao conclui end-to-end porque este modo esta acima do teto do fluxo.
- Fim: Use o maior modo habilitado para automatizar o caso comum sem ultrapassar os limites publicados.
- Ajustes afetados: aprovador; validade do credito; responsavel por excecao
- Encadeamento: /app/creditos-reposicao; /app/aprovacoes


### Rotina: Presenca e faltas


#### Correcao presenca

**Manual** (habilitado)

- Inicio: O fluxo comeca quando surge um caso para preparar correcao de presenca para aprovacao. A Taliya identifica o caso e organiza o contexto principal: aula e aluno foram identificados; correcao solicitada tem motivo; historico atual foi preservado.
- Meio: A Taliya cria tarefa, checklist ou caso para a equipe preparar correcao de presenca para aprovacao. A decisao e a execucao principal ficam com o humano.
- Fim: O fluxo termina quando a equipe registra o resultado. A Taliya salva auditoria e, se nao puder seguir, criar tarefa/caso em /app/aulas/[id]/chamada; /app/auditoria; aprovacao e manter auditoria do motivo.
- Ajustes afetados: aprovador; motivo obrigatorio; prazo de aprovacao
- Encadeamento: /app/aulas/[id]/chamada; /app/auditoria; aprovacao

**Copiloto** (habilitado)

- Inicio: O fluxo comeca quando surge um caso para preparar correcao de presenca para aprovacao. A Taliya identifica o contexto e mostra a base da sugestao: aula e aluno foram identificados; correcao solicitada tem motivo; historico atual foi preservado.
- Meio: A Taliya sugere preparar correcao de presenca para aprovacao, prepara texto/resumo/proximo passo e mostra os dados usados. A equipe pode aceitar, editar ou descartar antes de executar.
- Fim: Se a equipe aceitar, a acao e registrada conforme a decisao humana. Se editar ou descartar, a Taliya registra a decisao e mantem continuidade em /app/aulas/[id]/chamada; /app/auditoria; aprovacao.
- Ajustes afetados: aprovador; motivo obrigatorio; prazo de aprovacao
- Encadeamento: /app/aulas/[id]/chamada; /app/auditoria; aprovacao

**Autonomo com aprovacao** (habilitado)

- Inicio: O fluxo comeca quando surge um caso para preparar correcao de presenca para aprovacao. A Taliya identifica o caso, confere aula e aluno foram identificados; correcao solicitada tem motivo; historico atual foi preservado e prepara a revisao.
- Meio: A Taliya valida aula e aluno foram identificados; correcao solicitada tem motivo; historico atual foi preservado; impacto da alteracao foi mostrado e prepara preparar correcao de presenca para aprovacao. Antes de concluir, mostra impacto/preview e pede aprovacao.
- Fim: Se aprovado, a acao e concluida e auditada. Se recusado, vencido ou incompleto, criar tarefa/caso em /app/aulas/[id]/chamada; /app/auditoria; aprovacao e manter auditoria do motivo.
- Ajustes afetados: aprovador; motivo obrigatorio; prazo de aprovacao
- Encadeamento: /app/aulas/[id]/chamada; /app/auditoria; aprovacao

**Autonomo com excecoes** (bloqueado)

- Inicio: Este modo fica bloqueado para Correcao presenca.
- Meio: A Taliya nao executa com excecoes porque o teto deste fluxo e menor.
- Fim: O usuario deve escolher um modo permitido para este fluxo.
- Ajustes afetados: aprovador; motivo obrigatorio; prazo de aprovacao
- Encadeamento: /app/aulas/[id]/chamada; /app/auditoria; aprovacao

**Autonomo** (bloqueado)

- Inicio: Este modo fica bloqueado para Correcao presenca.
- Meio: A Taliya nao conclui end-to-end porque este modo esta acima do teto do fluxo.
- Fim: Use o maior modo habilitado para automatizar o caso comum sem ultrapassar os limites publicados.
- Ajustes afetados: aprovador; motivo obrigatorio; prazo de aprovacao
- Encadeamento: /app/aulas/[id]/chamada; /app/auditoria; aprovacao


### Rotina: Primeira aula e aulas especiais


#### Primeira aula

**Manual** (habilitado)

- Inicio: O fluxo comeca quando surge um caso para acompanhar primeira aula e checklist inicial. A Taliya identifica o caso e organiza o contexto principal: aluno tem primeira aula identificada; checklist esta definido; professor ou responsavel esta atribuido.
- Meio: A Taliya cria tarefa, checklist ou caso para a equipe acompanhar primeira aula e checklist inicial. A decisao e a execucao principal ficam com o humano.
- Fim: O fluxo termina quando a equipe registra o resultado. A Taliya salva auditoria e, se nao puder seguir, criar tarefa/caso em /app/aulas/[id]; /app/alunos/[id]; checklist/tarefa e manter auditoria do motivo.
- Ajustes afetados: checklist; responsavel; quando chamar humano
- Encadeamento: /app/aulas/[id]; /app/alunos/[id]; checklist/tarefa

**Copiloto** (habilitado)

- Inicio: O fluxo comeca quando surge um caso para acompanhar primeira aula e checklist inicial. A Taliya identifica o contexto e mostra a base da sugestao: aluno tem primeira aula identificada; checklist esta definido; professor ou responsavel esta atribuido.
- Meio: A Taliya sugere acompanhar primeira aula e checklist inicial, prepara texto/resumo/proximo passo e mostra os dados usados. A equipe pode aceitar, editar ou descartar antes de executar.
- Fim: Se a equipe aceitar, a acao e registrada conforme a decisao humana. Se editar ou descartar, a Taliya registra a decisao e mantem continuidade em /app/aulas/[id]; /app/alunos/[id]; checklist/tarefa.
- Ajustes afetados: checklist; responsavel; quando chamar humano
- Encadeamento: /app/aulas/[id]; /app/alunos/[id]; checklist/tarefa

**Autonomo com aprovacao** (habilitado)

- Inicio: O fluxo comeca quando surge um caso para acompanhar primeira aula e checklist inicial. A Taliya identifica o caso, confere aluno tem primeira aula identificada; checklist esta definido; professor ou responsavel esta atribuido e prepara a revisao.
- Meio: A Taliya valida aluno tem primeira aula identificada; checklist esta definido; professor ou responsavel esta atribuido; orientacoes foram preparadas e prepara acompanhar primeira aula e checklist inicial. Antes de concluir, mostra impacto/preview e pede aprovacao.
- Fim: Se aprovado, a acao e concluida e auditada. Se recusado, vencido ou incompleto, criar tarefa/caso em /app/aulas/[id]; /app/alunos/[id]; checklist/tarefa e manter auditoria do motivo.
- Ajustes afetados: checklist; responsavel; quando chamar humano
- Encadeamento: /app/aulas/[id]; /app/alunos/[id]; checklist/tarefa

**Autonomo com excecoes** (habilitado)

- Inicio: O fluxo comeca quando surge um caso para acompanhar primeira aula e checklist inicial. A Taliya identifica o caso e valida os dados principais: aluno tem primeira aula identificada; checklist esta definido; professor ou responsavel esta atribuido.
- Meio: A Taliya executa sozinha quando aluno tem primeira aula identificada; checklist esta definido; professor ou responsavel esta atribuido; orientacoes foram preparadas; nao ha restricao sensivel pendente. Ela chama a equipe quando aluno tem cuidado sem revisao; professor nao esta definido; aula muda de horario; aluno pede remarcacao ou excecao; canal, cota ou permissao bloqueia contato.
- Fim: No caso comum, a acao `acompanhar primeira aula e checklist inicial` fica registrada e auditada. Se houver excecao, criar tarefa/caso em /app/aulas/[id]; /app/alunos/[id]; checklist/tarefa e manter auditoria do motivo.
- Ajustes afetados: checklist; responsavel; quando chamar humano
- Encadeamento: /app/aulas/[id]; /app/alunos/[id]; checklist/tarefa

**Autonomo** (bloqueado)

- Inicio: Este modo fica bloqueado para Primeira aula.
- Meio: A Taliya nao conclui end-to-end porque este modo esta acima do teto do fluxo.
- Fim: Use o maior modo habilitado para automatizar o caso comum sem ultrapassar os limites publicados.
- Ajustes afetados: checklist; responsavel; quando chamar humano
- Encadeamento: /app/aulas/[id]; /app/alunos/[id]; checklist/tarefa


#### Aula especial/workshop

**Manual** (habilitado)

- Inicio: O fluxo comeca quando surge um caso para preparar aula especial ou workshop para aprovacao. A Taliya identifica o caso e organiza o contexto principal: evento foi descrito; capacidade esta definida; prazo e data estao claros.
- Meio: A Taliya cria tarefa, checklist ou caso para a equipe preparar aula especial ou workshop para aprovacao. A decisao e a execucao principal ficam com o humano.
- Fim: O fluxo termina quando a equipe registra o resultado. A Taliya salva auditoria e, se nao puder seguir, criar tarefa/caso em /app/eventos; /app/aprovacoes; tarefa e manter auditoria do motivo.
- Ajustes afetados: aprovador; capacidade; template; prazo
- Encadeamento: /app/eventos; /app/aprovacoes; tarefa

**Copiloto** (habilitado)

- Inicio: O fluxo comeca quando surge um caso para preparar aula especial ou workshop para aprovacao. A Taliya identifica o contexto e mostra a base da sugestao: evento foi descrito; capacidade esta definida; prazo e data estao claros.
- Meio: A Taliya sugere preparar aula especial ou workshop para aprovacao, prepara texto/resumo/proximo passo e mostra os dados usados. A equipe pode aceitar, editar ou descartar antes de executar.
- Fim: Se a equipe aceitar, a acao e registrada conforme a decisao humana. Se editar ou descartar, a Taliya registra a decisao e mantem continuidade em /app/eventos; /app/aprovacoes; tarefa.
- Ajustes afetados: aprovador; capacidade; template; prazo
- Encadeamento: /app/eventos; /app/aprovacoes; tarefa

**Autonomo com aprovacao** (habilitado)

- Inicio: O fluxo comeca quando surge um caso para preparar aula especial ou workshop para aprovacao. A Taliya identifica o caso, confere evento foi descrito; capacidade esta definida; prazo e data estao claros e prepara a revisao.
- Meio: A Taliya valida evento foi descrito; capacidade esta definida; prazo e data estao claros; template de comunicacao esta pronto e prepara preparar aula especial ou workshop para aprovacao. Antes de concluir, mostra impacto/preview e pede aprovacao.
- Fim: Se aprovado, a acao e concluida e auditada. Se recusado, vencido ou incompleto, criar tarefa/caso em /app/eventos; /app/aprovacoes; tarefa e manter auditoria do motivo.
- Ajustes afetados: aprovador; capacidade; template; prazo
- Encadeamento: /app/eventos; /app/aprovacoes; tarefa

**Autonomo com excecoes** (bloqueado)

- Inicio: Este modo fica bloqueado para Aula especial/workshop.
- Meio: A Taliya nao executa com excecoes porque o teto deste fluxo e menor.
- Fim: O usuario deve escolher um modo permitido para este fluxo.
- Ajustes afetados: aprovador; capacidade; template; prazo
- Encadeamento: /app/eventos; /app/aprovacoes; tarefa

**Autonomo** (bloqueado)

- Inicio: Este modo fica bloqueado para Aula especial/workshop.
- Meio: A Taliya nao conclui end-to-end porque este modo esta acima do teto do fluxo.
- Fim: Use o maior modo habilitado para automatizar o caso comum sem ultrapassar os limites publicados.
- Ajustes afetados: aprovador; capacidade; template; prazo
- Encadeamento: /app/eventos; /app/aprovacoes; tarefa


## Agente: Vendas


### Rotina: Conversao e matricula


#### Valores e planos

**Manual** (habilitado)

- Inicio: O fluxo comeca quando surge um caso para responder sobre valores e planos aprovados. A Taliya identifica o caso e organiza o contexto principal: plano ou valor esta na base aprovada; lead ou aluno foi identificado quando necessario; nao ha pedido de desconto especial.
- Meio: A Taliya cria tarefa, checklist ou caso para a equipe responder sobre valores e planos aprovados. A decisao e a execucao principal ficam com o humano.
- Fim: O fluxo termina quando a equipe registra o resultado. A Taliya salva auditoria e, se nao puder seguir, criar tarefa/caso em /app/inbox; /app/vendas; tarefa comercial e manter auditoria do motivo.
- Ajustes afetados: tom/template de resposta; quando chamar humano
- Encadeamento: /app/inbox; /app/vendas; tarefa comercial

**Copiloto** (habilitado)

- Inicio: O fluxo comeca quando surge um caso para responder sobre valores e planos aprovados. A Taliya identifica o contexto e mostra a base da sugestao: plano ou valor esta na base aprovada; lead ou aluno foi identificado quando necessario; nao ha pedido de desconto especial.
- Meio: A Taliya sugere responder sobre valores e planos aprovados, prepara texto/resumo/proximo passo e mostra os dados usados. A equipe pode aceitar, editar ou descartar antes de executar.
- Fim: Se a equipe aceitar, a acao e registrada conforme a decisao humana. Se editar ou descartar, a Taliya registra a decisao e mantem continuidade em /app/inbox; /app/vendas; tarefa comercial.
- Ajustes afetados: tom/template de resposta; quando chamar humano
- Encadeamento: /app/inbox; /app/vendas; tarefa comercial

**Autonomo com aprovacao** (habilitado)

- Inicio: O fluxo comeca quando surge um caso para responder sobre valores e planos aprovados. A Taliya identifica o caso, confere plano ou valor esta na base aprovada; lead ou aluno foi identificado quando necessario; nao ha pedido de desconto especial e prepara a revisao.
- Meio: A Taliya valida plano ou valor esta na base aprovada; lead ou aluno foi identificado quando necessario; nao ha pedido de desconto especial; resposta usa template permitido e prepara responder sobre valores e planos aprovados. Antes de concluir, mostra impacto/preview e pede aprovacao.
- Fim: Se aprovado, a acao e concluida e auditada. Se recusado, vencido ou incompleto, criar tarefa/caso em /app/inbox; /app/vendas; tarefa comercial e manter auditoria do motivo.
- Ajustes afetados: tom/template de resposta; quando chamar humano
- Encadeamento: /app/inbox; /app/vendas; tarefa comercial

**Autonomo com excecoes** (habilitado)

- Inicio: O fluxo comeca quando surge um caso para responder sobre valores e planos aprovados. A Taliya identifica o caso e valida os dados principais: plano ou valor esta na base aprovada; lead ou aluno foi identificado quando necessario; nao ha pedido de desconto especial.
- Meio: A Taliya executa sozinha quando plano ou valor esta na base aprovada; lead ou aluno foi identificado quando necessario; nao ha pedido de desconto especial; resposta usa template permitido; limite de conversa nao foi atingido. Ela chama a equipe quando lead pede desconto, promessa ou excecao; plano nao esta claro; pergunta mistura financeiro e contrato; resposta pode gerar compromisso comercial; canal, cota ou permissao bloqueia resposta.
- Fim: No caso comum, a acao `responder sobre valores e planos aprovados` fica registrada e auditada. Se houver excecao, criar tarefa/caso em /app/inbox; /app/vendas; tarefa comercial e manter auditoria do motivo.
- Ajustes afetados: tom/template de resposta; quando chamar humano
- Encadeamento: /app/inbox; /app/vendas; tarefa comercial

**Autonomo** (bloqueado)

- Inicio: Este modo fica bloqueado para Valores e planos.
- Meio: A Taliya nao conclui end-to-end porque este modo esta acima do teto do fluxo.
- Fim: Use o maior modo habilitado para automatizar o caso comum sem ultrapassar os limites publicados.
- Ajustes afetados: tom/template de resposta; quando chamar humano
- Encadeamento: /app/inbox; /app/vendas; tarefa comercial


### Rotina: Experimental e acompanhamento


#### Aula experimental

**Manual** (habilitado)

- Inicio: O fluxo comeca quando surge um caso para marcar ou preparar aula experimental. A Taliya identifica o caso e organiza o contexto principal: lead esta identificado; horarios disponiveis existem; responsavel comercial esta definido.
- Meio: A Taliya cria tarefa, checklist ou caso para a equipe marcar ou preparar aula experimental. A decisao e a execucao principal ficam com o humano.
- Fim: O fluxo termina quando a equipe registra o resultado. A Taliya salva auditoria e, se nao puder seguir, criar tarefa/caso em /app/experimental; /app/agenda; tarefa e manter auditoria do motivo.
- Ajustes afetados: horarios oferecidos; responsavel; limite de tentativas
- Encadeamento: /app/experimental; /app/agenda; tarefa

**Copiloto** (habilitado)

- Inicio: O fluxo comeca quando surge um caso para marcar ou preparar aula experimental. A Taliya identifica o contexto e mostra a base da sugestao: lead esta identificado; horarios disponiveis existem; responsavel comercial esta definido.
- Meio: A Taliya sugere marcar ou preparar aula experimental, prepara texto/resumo/proximo passo e mostra os dados usados. A equipe pode aceitar, editar ou descartar antes de executar.
- Fim: Se a equipe aceitar, a acao e registrada conforme a decisao humana. Se editar ou descartar, a Taliya registra a decisao e mantem continuidade em /app/experimental; /app/agenda; tarefa.
- Ajustes afetados: horarios oferecidos; responsavel; limite de tentativas
- Encadeamento: /app/experimental; /app/agenda; tarefa

**Autonomo com aprovacao** (habilitado)

- Inicio: O fluxo comeca quando surge um caso para marcar ou preparar aula experimental. A Taliya identifica o caso, confere lead esta identificado; horarios disponiveis existem; responsavel comercial esta definido e prepara a revisao.
- Meio: A Taliya valida lead esta identificado; horarios disponiveis existem; responsavel comercial esta definido; limite de tentativas permite contato e prepara marcar ou preparar aula experimental. Antes de concluir, mostra impacto/preview e pede aprovacao.
- Fim: Se aprovado, a acao e concluida e auditada. Se recusado, vencido ou incompleto, criar tarefa/caso em /app/experimental; /app/agenda; tarefa e manter auditoria do motivo.
- Ajustes afetados: horarios oferecidos; responsavel; limite de tentativas
- Encadeamento: /app/experimental; /app/agenda; tarefa

**Autonomo com excecoes** (habilitado)

- Inicio: O fluxo comeca quando surge um caso para marcar ou preparar aula experimental. A Taliya identifica o caso e valida os dados principais: lead esta identificado; horarios disponiveis existem; responsavel comercial esta definido.
- Meio: A Taliya executa sozinha quando lead esta identificado; horarios disponiveis existem; responsavel comercial esta definido; limite de tentativas permite contato; lead nao tem experimental duplicada. Ela chama a equipe quando lead pede horario indisponivel; nao ha vaga compativel; lead ja fez experimental recente; pedido envolve desconto ou excecao; canal, cota ou permissao bloqueia contato.
- Fim: No caso comum, a acao `marcar ou preparar aula experimental` fica registrada e auditada. Se houver excecao, criar tarefa/caso em /app/experimental; /app/agenda; tarefa e manter auditoria do motivo.
- Ajustes afetados: horarios oferecidos; responsavel; limite de tentativas
- Encadeamento: /app/experimental; /app/agenda; tarefa

**Autonomo** (bloqueado)

- Inicio: Este modo fica bloqueado para Aula experimental.
- Meio: A Taliya nao conclui end-to-end porque este modo esta acima do teto do fluxo.
- Fim: Use o maior modo habilitado para automatizar o caso comum sem ultrapassar os limites publicados.
- Ajustes afetados: horarios oferecidos; responsavel; limite de tentativas
- Encadeamento: /app/experimental; /app/agenda; tarefa


#### Lembrete experimental

**Manual** (habilitado)

- Inicio: O fluxo comeca quando surge um caso para enviar lembrete de aula experimental. A Taliya identifica o caso e organiza o contexto principal: experimental esta marcada; horario do lembrete chegou; lead tem canal permitido.
- Meio: A Taliya cria tarefa, checklist ou caso para a equipe enviar lembrete de aula experimental. A decisao e a execucao principal ficam com o humano.
- Fim: O fluxo termina quando a equipe registra o resultado. A Taliya salva auditoria e, se nao puder seguir, criar tarefa/caso em /app/experimental; execucao; tarefa manual e manter auditoria do motivo.
- Ajustes afetados: horario do lembrete; template; limite por aula
- Encadeamento: /app/experimental; execucao; tarefa manual

**Copiloto** (habilitado)

- Inicio: O fluxo comeca quando surge um caso para enviar lembrete de aula experimental. A Taliya identifica o contexto e mostra a base da sugestao: experimental esta marcada; horario do lembrete chegou; lead tem canal permitido.
- Meio: A Taliya sugere enviar lembrete de aula experimental, prepara texto/resumo/proximo passo e mostra os dados usados. A equipe pode aceitar, editar ou descartar antes de executar.
- Fim: Se a equipe aceitar, a acao e registrada conforme a decisao humana. Se editar ou descartar, a Taliya registra a decisao e mantem continuidade em /app/experimental; execucao; tarefa manual.
- Ajustes afetados: horario do lembrete; template; limite por aula
- Encadeamento: /app/experimental; execucao; tarefa manual

**Autonomo com aprovacao** (habilitado)

- Inicio: O fluxo comeca quando surge um caso para enviar lembrete de aula experimental. A Taliya identifica o caso, confere experimental esta marcada; horario do lembrete chegou; lead tem canal permitido e prepara a revisao.
- Meio: A Taliya valida experimental esta marcada; horario do lembrete chegou; lead tem canal permitido; template aprovado esta disponivel e prepara enviar lembrete de aula experimental. Antes de concluir, mostra impacto/preview e pede aprovacao.
- Fim: Se aprovado, a acao e concluida e auditada. Se recusado, vencido ou incompleto, criar tarefa/caso em /app/experimental; execucao; tarefa manual e manter auditoria do motivo.
- Ajustes afetados: horario do lembrete; template; limite por aula
- Encadeamento: /app/experimental; execucao; tarefa manual

**Autonomo com excecoes** (habilitado)

- Inicio: O fluxo comeca quando surge um caso para enviar lembrete de aula experimental. A Taliya identifica o caso e valida os dados principais: experimental esta marcada; horario do lembrete chegou; lead tem canal permitido.
- Meio: A Taliya executa sozinha quando experimental esta marcada; horario do lembrete chegou; lead tem canal permitido; template aprovado esta disponivel; lembrete ainda nao foi enviado. Ela chama a equipe quando aula foi remarcada ou cancelada; lead pediu opt-out; canal falhou; lead responde com objecao ou pedido de mudanca; cota ou permissao bloqueia envio.
- Fim: No caso comum, a acao `enviar lembrete de aula experimental` fica registrada e auditada. Se houver excecao, criar tarefa/caso em /app/experimental; execucao; tarefa manual e manter auditoria do motivo.
- Ajustes afetados: horario do lembrete; template; limite por aula
- Encadeamento: /app/experimental; execucao; tarefa manual

**Autonomo** (habilitado)

- Inicio: O fluxo comeca quando surge um caso para enviar lembrete de aula experimental. A Taliya identifica o caso e confirma experimental esta marcada; horario do lembrete chegou; lead tem canal permitido.
- Meio: A Taliya conclui enviar lembrete de aula experimental quando experimental esta marcada; horario do lembrete chegou; lead tem canal permitido; template aprovado esta disponivel; lembrete ainda nao foi enviado. Ela para quando aula foi remarcada ou cancelada; lead pediu opt-out; canal falhou; lead responde com objecao ou pedido de mudanca; cota ou permissao bloqueia envio.
- Fim: A acao e concluida, a auditoria fica salva e a continuidade segue em /app/experimental; execucao; tarefa manual. Se houver bloqueio, criar tarefa/caso em /app/experimental; execucao; tarefa manual e manter auditoria do motivo.
- Ajustes afetados: horario do lembrete; template; limite por aula
- Encadeamento: /app/experimental; execucao; tarefa manual


#### Pos-aula experimental

**Manual** (habilitado)

- Inicio: O fluxo comeca quando surge um caso para acompanhar lead depois da aula experimental. A Taliya identifica o caso e organiza o contexto principal: experimental foi concluida; presenca foi registrada; cadencia pos-aula esta definida.
- Meio: A Taliya cria tarefa, checklist ou caso para a equipe acompanhar lead depois da aula experimental. A decisao e a execucao principal ficam com o humano.
- Fim: O fluxo termina quando a equipe registra o resultado. A Taliya salva auditoria e, se nao puder seguir, criar tarefa/caso em /app/interessados/[id]; /app/vendas; tarefa e manter auditoria do motivo.
- Ajustes afetados: cadencia; responsavel; quando virar tarefa
- Encadeamento: /app/interessados/[id]; /app/vendas; tarefa

**Copiloto** (habilitado)

- Inicio: O fluxo comeca quando surge um caso para acompanhar lead depois da aula experimental. A Taliya identifica o contexto e mostra a base da sugestao: experimental foi concluida; presenca foi registrada; cadencia pos-aula esta definida.
- Meio: A Taliya sugere acompanhar lead depois da aula experimental, prepara texto/resumo/proximo passo e mostra os dados usados. A equipe pode aceitar, editar ou descartar antes de executar.
- Fim: Se a equipe aceitar, a acao e registrada conforme a decisao humana. Se editar ou descartar, a Taliya registra a decisao e mantem continuidade em /app/interessados/[id]; /app/vendas; tarefa.
- Ajustes afetados: cadencia; responsavel; quando virar tarefa
- Encadeamento: /app/interessados/[id]; /app/vendas; tarefa

**Autonomo com aprovacao** (habilitado)

- Inicio: O fluxo comeca quando surge um caso para acompanhar lead depois da aula experimental. A Taliya identifica o caso, confere experimental foi concluida; presenca foi registrada; cadencia pos-aula esta definida e prepara a revisao.
- Meio: A Taliya valida experimental foi concluida; presenca foi registrada; cadencia pos-aula esta definida; responsavel comercial esta atribuido e prepara acompanhar lead depois da aula experimental. Antes de concluir, mostra impacto/preview e pede aprovacao.
- Fim: Se aprovado, a acao e concluida e auditada. Se recusado, vencido ou incompleto, criar tarefa/caso em /app/interessados/[id]; /app/vendas; tarefa e manter auditoria do motivo.
- Ajustes afetados: cadencia; responsavel; quando virar tarefa
- Encadeamento: /app/interessados/[id]; /app/vendas; tarefa

**Autonomo com excecoes** (habilitado)

- Inicio: O fluxo comeca quando surge um caso para acompanhar lead depois da aula experimental. A Taliya identifica o caso e valida os dados principais: experimental foi concluida; presenca foi registrada; cadencia pos-aula esta definida.
- Meio: A Taliya executa sozinha quando experimental foi concluida; presenca foi registrada; cadencia pos-aula esta definida; responsavel comercial esta atribuido; limite de contato nao foi atingido. Ela chama a equipe quando lead nao compareceu; professor registrou observacao sensivel; lead pede desconto ou condicao especial; lead demonstra reclamacao; canal, cota ou permissao bloqueia contato.
- Fim: No caso comum, a acao `acompanhar lead depois da aula experimental` fica registrada e auditada. Se houver excecao, criar tarefa/caso em /app/interessados/[id]; /app/vendas; tarefa e manter auditoria do motivo.
- Ajustes afetados: cadencia; responsavel; quando virar tarefa
- Encadeamento: /app/interessados/[id]; /app/vendas; tarefa

**Autonomo** (bloqueado)

- Inicio: Este modo fica bloqueado para Pos-aula experimental.
- Meio: A Taliya nao conclui end-to-end porque este modo esta acima do teto do fluxo.
- Fim: Use o maior modo habilitado para automatizar o caso comum sem ultrapassar os limites publicados.
- Ajustes afetados: cadencia; responsavel; quando virar tarefa
- Encadeamento: /app/interessados/[id]; /app/vendas; tarefa


#### Follow-up comercial

**Manual** (habilitado)

- Inicio: O fluxo comeca quando surge um caso para conduzir follow-up comercial dentro da cadencia. A Taliya identifica o caso e organiza o contexto principal: lead esta em etapa elegivel; cadencia esta definida; ultima interacao permite novo contato.
- Meio: A Taliya cria tarefa, checklist ou caso para a equipe conduzir follow-up comercial dentro da cadencia. A decisao e a execucao principal ficam com o humano.
- Fim: O fluxo termina quando a equipe registra o resultado. A Taliya salva auditoria e, se nao puder seguir, criar tarefa/caso em /app/vendas; /app/tarefas; /app/inbox e manter auditoria do motivo.
- Ajustes afetados: cadencia; limite de tentativas; responsavel
- Encadeamento: /app/vendas; /app/tarefas; /app/inbox

**Copiloto** (habilitado)

- Inicio: O fluxo comeca quando surge um caso para conduzir follow-up comercial dentro da cadencia. A Taliya identifica o contexto e mostra a base da sugestao: lead esta em etapa elegivel; cadencia esta definida; ultima interacao permite novo contato.
- Meio: A Taliya sugere conduzir follow-up comercial dentro da cadencia, prepara texto/resumo/proximo passo e mostra os dados usados. A equipe pode aceitar, editar ou descartar antes de executar.
- Fim: Se a equipe aceitar, a acao e registrada conforme a decisao humana. Se editar ou descartar, a Taliya registra a decisao e mantem continuidade em /app/vendas; /app/tarefas; /app/inbox.
- Ajustes afetados: cadencia; limite de tentativas; responsavel
- Encadeamento: /app/vendas; /app/tarefas; /app/inbox

**Autonomo com aprovacao** (habilitado)

- Inicio: O fluxo comeca quando surge um caso para conduzir follow-up comercial dentro da cadencia. A Taliya identifica o caso, confere lead esta em etapa elegivel; cadencia esta definida; ultima interacao permite novo contato e prepara a revisao.
- Meio: A Taliya valida lead esta em etapa elegivel; cadencia esta definida; ultima interacao permite novo contato; responsavel comercial esta definido e prepara conduzir follow-up comercial dentro da cadencia. Antes de concluir, mostra impacto/preview e pede aprovacao.
- Fim: Se aprovado, a acao e concluida e auditada. Se recusado, vencido ou incompleto, criar tarefa/caso em /app/vendas; /app/tarefas; /app/inbox e manter auditoria do motivo.
- Ajustes afetados: cadencia; limite de tentativas; responsavel
- Encadeamento: /app/vendas; /app/tarefas; /app/inbox

**Autonomo com excecoes** (habilitado)

- Inicio: O fluxo comeca quando surge um caso para conduzir follow-up comercial dentro da cadencia. A Taliya identifica o caso e valida os dados principais: lead esta em etapa elegivel; cadencia esta definida; ultima interacao permite novo contato.
- Meio: A Taliya executa sozinha quando lead esta em etapa elegivel; cadencia esta definida; ultima interacao permite novo contato; responsavel comercial esta definido; limite de tentativas nao foi atingido. Ela chama a equipe quando lead pediu humano ou parar contato; lead tem objecao sensivel; lead pede desconto ou garantia; conversa esfriou alem do limite; canal, cota ou permissao bloqueia contato.
- Fim: No caso comum, a acao `conduzir follow-up comercial dentro da cadencia` fica registrada e auditada. Se houver excecao, criar tarefa/caso em /app/vendas; /app/tarefas; /app/inbox e manter auditoria do motivo.
- Ajustes afetados: cadencia; limite de tentativas; responsavel
- Encadeamento: /app/vendas; /app/tarefas; /app/inbox

**Autonomo** (bloqueado)

- Inicio: Este modo fica bloqueado para Follow-up comercial.
- Meio: A Taliya nao conclui end-to-end porque este modo esta acima do teto do fluxo.
- Fim: Use o maior modo habilitado para automatizar o caso comum sem ultrapassar os limites publicados.
- Ajustes afetados: cadencia; limite de tentativas; responsavel
- Encadeamento: /app/vendas; /app/tarefas; /app/inbox


### Rotina: Conversao e matricula


#### Pre-matricula

**Manual** (habilitado)

- Inicio: O fluxo comeca quando surge um caso para preparar pre-matricula para aprovacao. A Taliya identifica o caso e organiza o contexto principal: lead aceitou avancar; checklist de matricula esta completo; plano escolhido esta definido.
- Meio: A Taliya cria tarefa, checklist ou caso para a equipe preparar pre-matricula para aprovacao. A decisao e a execucao principal ficam com o humano.
- Fim: O fluxo termina quando a equipe registra o resultado. A Taliya salva auditoria e, se nao puder seguir, criar tarefa/caso em /app/matriculas; /app/aprovacoes e manter auditoria do motivo.
- Ajustes afetados: aprovador; checklist; responsavel comercial
- Encadeamento: /app/matriculas; /app/aprovacoes

**Copiloto** (habilitado)

- Inicio: O fluxo comeca quando surge um caso para preparar pre-matricula para aprovacao. A Taliya identifica o contexto e mostra a base da sugestao: lead aceitou avancar; checklist de matricula esta completo; plano escolhido esta definido.
- Meio: A Taliya sugere preparar pre-matricula para aprovacao, prepara texto/resumo/proximo passo e mostra os dados usados. A equipe pode aceitar, editar ou descartar antes de executar.
- Fim: Se a equipe aceitar, a acao e registrada conforme a decisao humana. Se editar ou descartar, a Taliya registra a decisao e mantem continuidade em /app/matriculas; /app/aprovacoes.
- Ajustes afetados: aprovador; checklist; responsavel comercial
- Encadeamento: /app/matriculas; /app/aprovacoes

**Autonomo com aprovacao** (habilitado)

- Inicio: O fluxo comeca quando surge um caso para preparar pre-matricula para aprovacao. A Taliya identifica o caso, confere lead aceitou avancar; checklist de matricula esta completo; plano escolhido esta definido e prepara a revisao.
- Meio: A Taliya valida lead aceitou avancar; checklist de matricula esta completo; plano escolhido esta definido; responsavel comercial esta atribuido e prepara preparar pre-matricula para aprovacao. Antes de concluir, mostra impacto/preview e pede aprovacao.
- Fim: Se aprovado, a acao e concluida e auditada. Se recusado, vencido ou incompleto, criar tarefa/caso em /app/matriculas; /app/aprovacoes e manter auditoria do motivo.
- Ajustes afetados: aprovador; checklist; responsavel comercial
- Encadeamento: /app/matriculas; /app/aprovacoes

**Autonomo com excecoes** (bloqueado)

- Inicio: Este modo fica bloqueado para Pre-matricula.
- Meio: A Taliya nao executa com excecoes porque o teto deste fluxo e menor.
- Fim: O usuario deve escolher um modo permitido para este fluxo.
- Ajustes afetados: aprovador; checklist; responsavel comercial
- Encadeamento: /app/matriculas; /app/aprovacoes

**Autonomo** (bloqueado)

- Inicio: Este modo fica bloqueado para Pre-matricula.
- Meio: A Taliya nao conclui end-to-end porque este modo esta acima do teto do fluxo.
- Fim: Use o maior modo habilitado para automatizar o caso comum sem ultrapassar os limites publicados.
- Ajustes afetados: aprovador; checklist; responsavel comercial
- Encadeamento: /app/matriculas; /app/aprovacoes


#### Objecoes

**Manual** (habilitado)

- Inicio: O fluxo comeca quando surge um caso para preparar resposta para objecoes comerciais. A Taliya identifica o caso e organiza o contexto principal: objecao foi classificada; base de respostas cobre o caso; limite de promessa esta definido.
- Meio: A Taliya cria tarefa, checklist ou caso para a equipe preparar resposta para objecoes comerciais. A decisao e a execucao principal ficam com o humano.
- Fim: O fluxo termina quando a equipe registra o resultado. A Taliya salva auditoria e, se nao puder seguir, criar tarefa/caso em /app/conversas/[id]; /app/aprovacoes e manter auditoria do motivo.
- Ajustes afetados: aprovador; base de respostas; limite de promessa
- Encadeamento: /app/conversas/[id]; /app/aprovacoes

**Copiloto** (habilitado)

- Inicio: O fluxo comeca quando surge um caso para preparar resposta para objecoes comerciais. A Taliya identifica o contexto e mostra a base da sugestao: objecao foi classificada; base de respostas cobre o caso; limite de promessa esta definido.
- Meio: A Taliya sugere preparar resposta para objecoes comerciais, prepara texto/resumo/proximo passo e mostra os dados usados. A equipe pode aceitar, editar ou descartar antes de executar.
- Fim: Se a equipe aceitar, a acao e registrada conforme a decisao humana. Se editar ou descartar, a Taliya registra a decisao e mantem continuidade em /app/conversas/[id]; /app/aprovacoes.
- Ajustes afetados: aprovador; base de respostas; limite de promessa
- Encadeamento: /app/conversas/[id]; /app/aprovacoes

**Autonomo com aprovacao** (habilitado)

- Inicio: O fluxo comeca quando surge um caso para preparar resposta para objecoes comerciais. A Taliya identifica o caso, confere objecao foi classificada; base de respostas cobre o caso; limite de promessa esta definido e prepara a revisao.
- Meio: A Taliya valida objecao foi classificada; base de respostas cobre o caso; limite de promessa esta definido; impacto comercial foi mostrado e prepara preparar resposta para objecoes comerciais. Antes de concluir, mostra impacto/preview e pede aprovacao.
- Fim: Se aprovado, a acao e concluida e auditada. Se recusado, vencido ou incompleto, criar tarefa/caso em /app/conversas/[id]; /app/aprovacoes e manter auditoria do motivo.
- Ajustes afetados: aprovador; base de respostas; limite de promessa
- Encadeamento: /app/conversas/[id]; /app/aprovacoes

**Autonomo com excecoes** (bloqueado)

- Inicio: Este modo fica bloqueado para Objecoes.
- Meio: A Taliya nao executa com excecoes porque o teto deste fluxo e menor.
- Fim: O usuario deve escolher um modo permitido para este fluxo.
- Ajustes afetados: aprovador; base de respostas; limite de promessa
- Encadeamento: /app/conversas/[id]; /app/aprovacoes

**Autonomo** (bloqueado)

- Inicio: Este modo fica bloqueado para Objecoes.
- Meio: A Taliya nao conclui end-to-end porque este modo esta acima do teto do fluxo.
- Fim: Use o maior modo habilitado para automatizar o caso comum sem ultrapassar os limites publicados.
- Ajustes afetados: aprovador; base de respostas; limite de promessa
- Encadeamento: /app/conversas/[id]; /app/aprovacoes


### Rotina: Captura e qualificacao


#### Origem/qualificacao

**Manual** (habilitado)

- Inicio: O fluxo comeca quando surge um caso para qualificar origem e perfil do lead. A Taliya identifica o caso e organiza o contexto principal: lead foi identificado; campos obrigatorios foram preenchidos; origem foi reconhecida.
- Meio: A Taliya cria tarefa, checklist ou caso para a equipe qualificar origem e perfil do lead. A decisao e a execucao principal ficam com o humano.
- Fim: O fluxo termina quando a equipe registra o resultado. A Taliya salva auditoria e, se nao puder seguir, criar tarefa/caso em /app/interessados/[id]; /app/vendas/origens; tarefa e manter auditoria do motivo.
- Ajustes afetados: campos obrigatorios; responsavel; regra de duplicidade
- Encadeamento: /app/interessados/[id]; /app/vendas/origens; tarefa

**Copiloto** (habilitado)

- Inicio: O fluxo comeca quando surge um caso para qualificar origem e perfil do lead. A Taliya identifica o contexto e mostra a base da sugestao: lead foi identificado; campos obrigatorios foram preenchidos; origem foi reconhecida.
- Meio: A Taliya sugere qualificar origem e perfil do lead, prepara texto/resumo/proximo passo e mostra os dados usados. A equipe pode aceitar, editar ou descartar antes de executar.
- Fim: Se a equipe aceitar, a acao e registrada conforme a decisao humana. Se editar ou descartar, a Taliya registra a decisao e mantem continuidade em /app/interessados/[id]; /app/vendas/origens; tarefa.
- Ajustes afetados: campos obrigatorios; responsavel; regra de duplicidade
- Encadeamento: /app/interessados/[id]; /app/vendas/origens; tarefa

**Autonomo com aprovacao** (habilitado)

- Inicio: O fluxo comeca quando surge um caso para qualificar origem e perfil do lead. A Taliya identifica o caso, confere lead foi identificado; campos obrigatorios foram preenchidos; origem foi reconhecida e prepara a revisao.
- Meio: A Taliya valida lead foi identificado; campos obrigatorios foram preenchidos; origem foi reconhecida; duplicidade foi verificada e prepara qualificar origem e perfil do lead. Antes de concluir, mostra impacto/preview e pede aprovacao.
- Fim: Se aprovado, a acao e concluida e auditada. Se recusado, vencido ou incompleto, criar tarefa/caso em /app/interessados/[id]; /app/vendas/origens; tarefa e manter auditoria do motivo.
- Ajustes afetados: campos obrigatorios; responsavel; regra de duplicidade
- Encadeamento: /app/interessados/[id]; /app/vendas/origens; tarefa

**Autonomo com excecoes** (habilitado)

- Inicio: O fluxo comeca quando surge um caso para qualificar origem e perfil do lead. A Taliya identifica o caso e valida os dados principais: lead foi identificado; campos obrigatorios foram preenchidos; origem foi reconhecida.
- Meio: A Taliya executa sozinha quando lead foi identificado; campos obrigatorios foram preenchidos; origem foi reconhecida; duplicidade foi verificada; responsavel esta definido. Ela chama a equipe quando lead duplicado; origem nao reconhecida; campos obrigatorios faltam; lead ja esta em outra etapa; canal, cota ou permissao bloqueia atualizacao.
- Fim: No caso comum, a acao `qualificar origem e perfil do lead` fica registrada e auditada. Se houver excecao, criar tarefa/caso em /app/interessados/[id]; /app/vendas/origens; tarefa e manter auditoria do motivo.
- Ajustes afetados: campos obrigatorios; responsavel; regra de duplicidade
- Encadeamento: /app/interessados/[id]; /app/vendas/origens; tarefa

**Autonomo** (bloqueado)

- Inicio: Este modo fica bloqueado para Origem/qualificacao.
- Meio: A Taliya nao conclui end-to-end porque este modo esta acima do teto do fluxo.
- Fim: Use o maior modo habilitado para automatizar o caso comum sem ultrapassar os limites publicados.
- Ajustes afetados: campos obrigatorios; responsavel; regra de duplicidade
- Encadeamento: /app/interessados/[id]; /app/vendas/origens; tarefa


#### Perda comercial

**Manual** (habilitado)

- Inicio: O fluxo comeca quando surge um caso para preparar perda comercial e motivo. A Taliya identifica o caso e organiza o contexto principal: lead esta em etapa que permite perda; motivo foi informado; responsavel comercial esta definido.
- Meio: A Taliya cria tarefa, checklist ou caso para a equipe preparar perda comercial e motivo. A decisao e a execucao principal ficam com o humano.
- Fim: O fluxo termina quando a equipe registra o resultado. A Taliya salva auditoria e, se nao puder seguir, criar tarefa/caso em /app/vendas; /app/interessados/[id]; aprovacao/tarefa e manter auditoria do motivo.
- Ajustes afetados: motivo; aprovador se perda sensivel; responsavel
- Encadeamento: /app/vendas; /app/interessados/[id]; aprovacao/tarefa

**Copiloto** (habilitado)

- Inicio: O fluxo comeca quando surge um caso para preparar perda comercial e motivo. A Taliya identifica o contexto e mostra a base da sugestao: lead esta em etapa que permite perda; motivo foi informado; responsavel comercial esta definido.
- Meio: A Taliya sugere preparar perda comercial e motivo, prepara texto/resumo/proximo passo e mostra os dados usados. A equipe pode aceitar, editar ou descartar antes de executar.
- Fim: Se a equipe aceitar, a acao e registrada conforme a decisao humana. Se editar ou descartar, a Taliya registra a decisao e mantem continuidade em /app/vendas; /app/interessados/[id]; aprovacao/tarefa.
- Ajustes afetados: motivo; aprovador se perda sensivel; responsavel
- Encadeamento: /app/vendas; /app/interessados/[id]; aprovacao/tarefa

**Autonomo com aprovacao** (habilitado)

- Inicio: O fluxo comeca quando surge um caso para preparar perda comercial e motivo. A Taliya identifica o caso, confere lead esta em etapa que permite perda; motivo foi informado; responsavel comercial esta definido e prepara a revisao.
- Meio: A Taliya valida lead esta em etapa que permite perda; motivo foi informado; responsavel comercial esta definido; impacto em relatorio foi calculado e prepara preparar perda comercial e motivo. Antes de concluir, mostra impacto/preview e pede aprovacao.
- Fim: Se aprovado, a acao e concluida e auditada. Se recusado, vencido ou incompleto, criar tarefa/caso em /app/vendas; /app/interessados/[id]; aprovacao/tarefa e manter auditoria do motivo.
- Ajustes afetados: motivo; aprovador se perda sensivel; responsavel
- Encadeamento: /app/vendas; /app/interessados/[id]; aprovacao/tarefa

**Autonomo com excecoes** (bloqueado)

- Inicio: Este modo fica bloqueado para Perda comercial.
- Meio: A Taliya nao executa com excecoes porque o teto deste fluxo e menor.
- Fim: O usuario deve escolher um modo permitido para este fluxo.
- Ajustes afetados: motivo; aprovador se perda sensivel; responsavel
- Encadeamento: /app/vendas; /app/interessados/[id]; aprovacao/tarefa

**Autonomo** (bloqueado)

- Inicio: Este modo fica bloqueado para Perda comercial.
- Meio: A Taliya nao conclui end-to-end porque este modo esta acima do teto do fluxo.
- Fim: Use o maior modo habilitado para automatizar o caso comum sem ultrapassar os limites publicados.
- Ajustes afetados: motivo; aprovador se perda sensivel; responsavel
- Encadeamento: /app/vendas; /app/interessados/[id]; aprovacao/tarefa


#### Indicacao

**Manual** (habilitado)

- Inicio: O fluxo comeca quando surge um caso para preparar indicacao e beneficio para aprovacao. A Taliya identifica o caso e organiza o contexto principal: indicador e indicado foram identificados; regra de vinculo esta clara; beneficio permitido foi calculado.
- Meio: A Taliya cria tarefa, checklist ou caso para a equipe preparar indicacao e beneficio para aprovacao. A decisao e a execucao principal ficam com o humano.
- Fim: O fluxo termina quando a equipe registra o resultado. A Taliya salva auditoria e, se nao puder seguir, criar tarefa/caso em /app/indicacoes; /app/aprovacoes e manter auditoria do motivo.
- Ajustes afetados: aprovador de beneficio; regra de vinculo
- Encadeamento: /app/indicacoes; /app/aprovacoes

**Copiloto** (habilitado)

- Inicio: O fluxo comeca quando surge um caso para preparar indicacao e beneficio para aprovacao. A Taliya identifica o contexto e mostra a base da sugestao: indicador e indicado foram identificados; regra de vinculo esta clara; beneficio permitido foi calculado.
- Meio: A Taliya sugere preparar indicacao e beneficio para aprovacao, prepara texto/resumo/proximo passo e mostra os dados usados. A equipe pode aceitar, editar ou descartar antes de executar.
- Fim: Se a equipe aceitar, a acao e registrada conforme a decisao humana. Se editar ou descartar, a Taliya registra a decisao e mantem continuidade em /app/indicacoes; /app/aprovacoes.
- Ajustes afetados: aprovador de beneficio; regra de vinculo
- Encadeamento: /app/indicacoes; /app/aprovacoes

**Autonomo com aprovacao** (habilitado)

- Inicio: O fluxo comeca quando surge um caso para preparar indicacao e beneficio para aprovacao. A Taliya identifica o caso, confere indicador e indicado foram identificados; regra de vinculo esta clara; beneficio permitido foi calculado e prepara a revisao.
- Meio: A Taliya valida indicador e indicado foram identificados; regra de vinculo esta clara; beneficio permitido foi calculado; duplicidade foi verificada e prepara preparar indicacao e beneficio para aprovacao. Antes de concluir, mostra impacto/preview e pede aprovacao.
- Fim: Se aprovado, a acao e concluida e auditada. Se recusado, vencido ou incompleto, criar tarefa/caso em /app/indicacoes; /app/aprovacoes e manter auditoria do motivo.
- Ajustes afetados: aprovador de beneficio; regra de vinculo
- Encadeamento: /app/indicacoes; /app/aprovacoes

**Autonomo com excecoes** (bloqueado)

- Inicio: Este modo fica bloqueado para Indicacao.
- Meio: A Taliya nao executa com excecoes porque o teto deste fluxo e menor.
- Fim: O usuario deve escolher um modo permitido para este fluxo.
- Ajustes afetados: aprovador de beneficio; regra de vinculo
- Encadeamento: /app/indicacoes; /app/aprovacoes

**Autonomo** (bloqueado)

- Inicio: Este modo fica bloqueado para Indicacao.
- Meio: A Taliya nao conclui end-to-end porque este modo esta acima do teto do fluxo.
- Fim: Use o maior modo habilitado para automatizar o caso comum sem ultrapassar os limites publicados.
- Ajustes afetados: aprovador de beneficio; regra de vinculo
- Encadeamento: /app/indicacoes; /app/aprovacoes


### Rotina: Conversao e matricula


#### Checkout/abandono

**Manual** (habilitado)

- Inicio: O fluxo comeca quando surge um caso para recuperar checkout ou abandono de matricula. A Taliya identifica o caso e organiza o contexto principal: checkout abandonado foi identificado; cadencia permite contato; responsavel comercial esta definido.
- Meio: A Taliya cria tarefa, checklist ou caso para a equipe recuperar checkout ou abandono de matricula. A decisao e a execucao principal ficam com o humano.
- Fim: O fluxo termina quando a equipe registra o resultado. A Taliya salva auditoria e, se nao puder seguir, criar tarefa/caso em /app/checkout-alunos; /app/vendas; tarefa e manter auditoria do motivo.
- Ajustes afetados: cadencia; responsavel; limite de contato
- Encadeamento: /app/checkout-alunos; /app/vendas; tarefa

**Copiloto** (habilitado)

- Inicio: O fluxo comeca quando surge um caso para recuperar checkout ou abandono de matricula. A Taliya identifica o contexto e mostra a base da sugestao: checkout abandonado foi identificado; cadencia permite contato; responsavel comercial esta definido.
- Meio: A Taliya sugere recuperar checkout ou abandono de matricula, prepara texto/resumo/proximo passo e mostra os dados usados. A equipe pode aceitar, editar ou descartar antes de executar.
- Fim: Se a equipe aceitar, a acao e registrada conforme a decisao humana. Se editar ou descartar, a Taliya registra a decisao e mantem continuidade em /app/checkout-alunos; /app/vendas; tarefa.
- Ajustes afetados: cadencia; responsavel; limite de contato
- Encadeamento: /app/checkout-alunos; /app/vendas; tarefa

**Autonomo com aprovacao** (habilitado)

- Inicio: O fluxo comeca quando surge um caso para recuperar checkout ou abandono de matricula. A Taliya identifica o caso, confere checkout abandonado foi identificado; cadencia permite contato; responsavel comercial esta definido e prepara a revisao.
- Meio: A Taliya valida checkout abandonado foi identificado; cadencia permite contato; responsavel comercial esta definido; mensagem aprovada esta disponivel e prepara recuperar checkout ou abandono de matricula. Antes de concluir, mostra impacto/preview e pede aprovacao.
- Fim: Se aprovado, a acao e concluida e auditada. Se recusado, vencido ou incompleto, criar tarefa/caso em /app/checkout-alunos; /app/vendas; tarefa e manter auditoria do motivo.
- Ajustes afetados: cadencia; responsavel; limite de contato
- Encadeamento: /app/checkout-alunos; /app/vendas; tarefa

**Autonomo com excecoes** (habilitado)

- Inicio: O fluxo comeca quando surge um caso para recuperar checkout ou abandono de matricula. A Taliya identifica o caso e valida os dados principais: checkout abandonado foi identificado; cadencia permite contato; responsavel comercial esta definido.
- Meio: A Taliya executa sozinha quando checkout abandonado foi identificado; cadencia permite contato; responsavel comercial esta definido; mensagem aprovada esta disponivel; lead nao pediu parar contato. Ela chama a equipe quando pagamento falhou com motivo financeiro; lead pede desconto ou condicao especial; checkout esta expirado; lead responde com reclamacao; canal, cota ou permissao bloqueia contato.
- Fim: No caso comum, a acao `recuperar checkout ou abandono de matricula` fica registrada e auditada. Se houver excecao, criar tarefa/caso em /app/checkout-alunos; /app/vendas; tarefa e manter auditoria do motivo.
- Ajustes afetados: cadencia; responsavel; limite de contato
- Encadeamento: /app/checkout-alunos; /app/vendas; tarefa

**Autonomo** (bloqueado)

- Inicio: Este modo fica bloqueado para Checkout/abandono.
- Meio: A Taliya nao conclui end-to-end porque este modo esta acima do teto do fluxo.
- Fim: Use o maior modo habilitado para automatizar o caso comum sem ultrapassar os limites publicados.
- Ajustes afetados: cadencia; responsavel; limite de contato
- Encadeamento: /app/checkout-alunos; /app/vendas; tarefa


### Rotina: Experimental e acompanhamento


#### Demanda sem vaga

**Manual** (habilitado)

- Inicio: O fluxo comeca quando surge um caso para tratar demanda sem vaga e lista de interesse. A Taliya identifica o caso e organiza o contexto principal: lead quer horario ou turma sem vaga; lista de espera foi definida; responsavel esta atribuido.
- Meio: A Taliya cria tarefa, checklist ou caso para a equipe tratar demanda sem vaga e lista de interesse. A decisao e a execucao principal ficam com o humano.
- Fim: O fluxo termina quando a equipe registra o resultado. A Taliya salva auditoria e, se nao puder seguir, criar tarefa/caso em /app/vendas; /app/lista-espera; tarefa e manter auditoria do motivo.
- Ajustes afetados: proximo passo sem vaga; responsavel; promessa permitida
- Encadeamento: /app/vendas; /app/lista-espera; tarefa

**Copiloto** (habilitado)

- Inicio: O fluxo comeca quando surge um caso para tratar demanda sem vaga e lista de interesse. A Taliya identifica o contexto e mostra a base da sugestao: lead quer horario ou turma sem vaga; lista de espera foi definida; responsavel esta atribuido.
- Meio: A Taliya sugere tratar demanda sem vaga e lista de interesse, prepara texto/resumo/proximo passo e mostra os dados usados. A equipe pode aceitar, editar ou descartar antes de executar.
- Fim: Se a equipe aceitar, a acao e registrada conforme a decisao humana. Se editar ou descartar, a Taliya registra a decisao e mantem continuidade em /app/vendas; /app/lista-espera; tarefa.
- Ajustes afetados: proximo passo sem vaga; responsavel; promessa permitida
- Encadeamento: /app/vendas; /app/lista-espera; tarefa

**Autonomo com aprovacao** (habilitado)

- Inicio: O fluxo comeca quando surge um caso para tratar demanda sem vaga e lista de interesse. A Taliya identifica o caso, confere lead quer horario ou turma sem vaga; lista de espera foi definida; responsavel esta atribuido e prepara a revisao.
- Meio: A Taliya valida lead quer horario ou turma sem vaga; lista de espera foi definida; responsavel esta atribuido; regra de promessa esta clara e prepara tratar demanda sem vaga e lista de interesse. Antes de concluir, mostra impacto/preview e pede aprovacao.
- Fim: Se aprovado, a acao e concluida e auditada. Se recusado, vencido ou incompleto, criar tarefa/caso em /app/vendas; /app/lista-espera; tarefa e manter auditoria do motivo.
- Ajustes afetados: proximo passo sem vaga; responsavel; promessa permitida
- Encadeamento: /app/vendas; /app/lista-espera; tarefa

**Autonomo com excecoes** (habilitado)

- Inicio: O fluxo comeca quando surge um caso para tratar demanda sem vaga e lista de interesse. A Taliya identifica o caso e valida os dados principais: lead quer horario ou turma sem vaga; lista de espera foi definida; responsavel esta atribuido.
- Meio: A Taliya executa sozinha quando lead quer horario ou turma sem vaga; lista de espera foi definida; responsavel esta atribuido; regra de promessa esta clara; mensagem nao promete vaga garantida. Ela chama a equipe quando lead exige prazo ou garantia; nao ha alternativa compativel; lead e prioridade comercial especial; promessa poderia ser indevida; canal, cota ou permissao bloqueia contato.
- Fim: No caso comum, a acao `tratar demanda sem vaga e lista de interesse` fica registrada e auditada. Se houver excecao, criar tarefa/caso em /app/vendas; /app/lista-espera; tarefa e manter auditoria do motivo.
- Ajustes afetados: proximo passo sem vaga; responsavel; promessa permitida
- Encadeamento: /app/vendas; /app/lista-espera; tarefa

**Autonomo** (bloqueado)

- Inicio: Este modo fica bloqueado para Demanda sem vaga.
- Meio: A Taliya nao conclui end-to-end porque este modo esta acima do teto do fluxo.
- Fim: Use o maior modo habilitado para automatizar o caso comum sem ultrapassar os limites publicados.
- Ajustes afetados: proximo passo sem vaga; responsavel; promessa permitida
- Encadeamento: /app/vendas; /app/lista-espera; tarefa


### Rotina: Conversao e matricula


#### Interessado para aluno

**Manual** (habilitado)

- Inicio: O fluxo comeca quando surge um caso para preparar conversao de interessado em aluno. A Taliya identifica o caso e organiza o contexto principal: interessado esta qualificado; plano escolhido foi definido; checklist de matricula esta completo.
- Meio: A Taliya cria tarefa, checklist ou caso para a equipe preparar conversao de interessado em aluno. A decisao e a execucao principal ficam com o humano.
- Fim: O fluxo termina quando a equipe registra o resultado. A Taliya salva auditoria e, se nao puder seguir, criar tarefa/caso em /app/matriculas; /app/alunos/[id]; aprovacao e manter auditoria do motivo.
- Ajustes afetados: aprovador; checklist de matricula; responsavel comercial
- Encadeamento: /app/matriculas; /app/alunos/[id]; aprovacao

**Copiloto** (habilitado)

- Inicio: O fluxo comeca quando surge um caso para preparar conversao de interessado em aluno. A Taliya identifica o contexto e mostra a base da sugestao: interessado esta qualificado; plano escolhido foi definido; checklist de matricula esta completo.
- Meio: A Taliya sugere preparar conversao de interessado em aluno, prepara texto/resumo/proximo passo e mostra os dados usados. A equipe pode aceitar, editar ou descartar antes de executar.
- Fim: Se a equipe aceitar, a acao e registrada conforme a decisao humana. Se editar ou descartar, a Taliya registra a decisao e mantem continuidade em /app/matriculas; /app/alunos/[id]; aprovacao.
- Ajustes afetados: aprovador; checklist de matricula; responsavel comercial
- Encadeamento: /app/matriculas; /app/alunos/[id]; aprovacao

**Autonomo com aprovacao** (habilitado)

- Inicio: O fluxo comeca quando surge um caso para preparar conversao de interessado em aluno. A Taliya identifica o caso, confere interessado esta qualificado; plano escolhido foi definido; checklist de matricula esta completo e prepara a revisao.
- Meio: A Taliya valida interessado esta qualificado; plano escolhido foi definido; checklist de matricula esta completo; cadastro de aluno pode ser criado e prepara preparar conversao de interessado em aluno. Antes de concluir, mostra impacto/preview e pede aprovacao.
- Fim: Se aprovado, a acao e concluida e auditada. Se recusado, vencido ou incompleto, criar tarefa/caso em /app/matriculas; /app/alunos/[id]; aprovacao e manter auditoria do motivo.
- Ajustes afetados: aprovador; checklist de matricula; responsavel comercial
- Encadeamento: /app/matriculas; /app/alunos/[id]; aprovacao

**Autonomo com excecoes** (bloqueado)

- Inicio: Este modo fica bloqueado para Interessado para aluno.
- Meio: A Taliya nao executa com excecoes porque o teto deste fluxo e menor.
- Fim: O usuario deve escolher um modo permitido para este fluxo.
- Ajustes afetados: aprovador; checklist de matricula; responsavel comercial
- Encadeamento: /app/matriculas; /app/alunos/[id]; aprovacao

**Autonomo** (bloqueado)

- Inicio: Este modo fica bloqueado para Interessado para aluno.
- Meio: A Taliya nao conclui end-to-end porque este modo esta acima do teto do fluxo.
- Fim: Use o maior modo habilitado para automatizar o caso comum sem ultrapassar os limites publicados.
- Ajustes afetados: aprovador; checklist de matricula; responsavel comercial
- Encadeamento: /app/matriculas; /app/alunos/[id]; aprovacao


#### Upsell/upgrade

**Manual** (habilitado)

- Inicio: O fluxo comeca quando surge um caso para preparar proposta de upsell ou upgrade. A Taliya identifica o caso e organiza o contexto principal: aluno elegivel foi identificado; plano destino esta definido; proposta usa template aprovado.
- Meio: A Taliya cria tarefa, checklist ou caso para a equipe preparar proposta de upsell ou upgrade. A decisao e a execucao principal ficam com o humano.
- Fim: O fluxo termina quando a equipe registra o resultado. A Taliya salva auditoria e, se nao puder seguir, criar tarefa/caso em /app/alunos/[id]; /app/aprovacoes; /app/vendas e manter auditoria do motivo.
- Ajustes afetados: aprovador; template de proposta; responsavel
- Encadeamento: /app/alunos/[id]; /app/aprovacoes; /app/vendas

**Copiloto** (habilitado)

- Inicio: O fluxo comeca quando surge um caso para preparar proposta de upsell ou upgrade. A Taliya identifica o contexto e mostra a base da sugestao: aluno elegivel foi identificado; plano destino esta definido; proposta usa template aprovado.
- Meio: A Taliya sugere preparar proposta de upsell ou upgrade, prepara texto/resumo/proximo passo e mostra os dados usados. A equipe pode aceitar, editar ou descartar antes de executar.
- Fim: Se a equipe aceitar, a acao e registrada conforme a decisao humana. Se editar ou descartar, a Taliya registra a decisao e mantem continuidade em /app/alunos/[id]; /app/aprovacoes; /app/vendas.
- Ajustes afetados: aprovador; template de proposta; responsavel
- Encadeamento: /app/alunos/[id]; /app/aprovacoes; /app/vendas

**Autonomo com aprovacao** (habilitado)

- Inicio: O fluxo comeca quando surge um caso para preparar proposta de upsell ou upgrade. A Taliya identifica o caso, confere aluno elegivel foi identificado; plano destino esta definido; proposta usa template aprovado e prepara a revisao.
- Meio: A Taliya valida aluno elegivel foi identificado; plano destino esta definido; proposta usa template aprovado; responsavel comercial esta atribuido e prepara preparar proposta de upsell ou upgrade. Antes de concluir, mostra impacto/preview e pede aprovacao.
- Fim: Se aprovado, a acao e concluida e auditada. Se recusado, vencido ou incompleto, criar tarefa/caso em /app/alunos/[id]; /app/aprovacoes; /app/vendas e manter auditoria do motivo.
- Ajustes afetados: aprovador; template de proposta; responsavel
- Encadeamento: /app/alunos/[id]; /app/aprovacoes; /app/vendas

**Autonomo com excecoes** (bloqueado)

- Inicio: Este modo fica bloqueado para Upsell/upgrade.
- Meio: A Taliya nao executa com excecoes porque o teto deste fluxo e menor.
- Fim: O usuario deve escolher um modo permitido para este fluxo.
- Ajustes afetados: aprovador; template de proposta; responsavel
- Encadeamento: /app/alunos/[id]; /app/aprovacoes; /app/vendas

**Autonomo** (bloqueado)

- Inicio: Este modo fica bloqueado para Upsell/upgrade.
- Meio: A Taliya nao conclui end-to-end porque este modo esta acima do teto do fluxo.
- Fim: Use o maior modo habilitado para automatizar o caso comum sem ultrapassar os limites publicados.
- Ajustes afetados: aprovador; template de proposta; responsavel
- Encadeamento: /app/alunos/[id]; /app/aprovacoes; /app/vendas


### Rotina: Captura e qualificacao


#### Entrada multicanal de lead

**Manual** (habilitado)

- Inicio: O fluxo comeca quando surge um caso para capturar lead de multiplos canais e criar ficha unica. A Taliya identifica o caso e organiza o contexto principal: fonte e aceita; lead tem contato identificavel; duplicidade foi verificada.
- Meio: A Taliya cria tarefa, checklist ou caso para a equipe capturar lead de multiplos canais e criar ficha unica. A decisao e a execucao principal ficam com o humano.
- Fim: O fluxo termina quando a equipe registra o resultado. A Taliya salva auditoria e, se nao puder seguir, criar tarefa/caso em /app/vendas/captura; /app/interessados; tarefa e manter auditoria do motivo.
- Ajustes afetados: fontes aceitas; dono do lead; regra de duplicidade
- Encadeamento: /app/vendas/captura; /app/interessados; tarefa

**Copiloto** (habilitado)

- Inicio: O fluxo comeca quando surge um caso para capturar lead de multiplos canais e criar ficha unica. A Taliya identifica o contexto e mostra a base da sugestao: fonte e aceita; lead tem contato identificavel; duplicidade foi verificada.
- Meio: A Taliya sugere capturar lead de multiplos canais e criar ficha unica, prepara texto/resumo/proximo passo e mostra os dados usados. A equipe pode aceitar, editar ou descartar antes de executar.
- Fim: Se a equipe aceitar, a acao e registrada conforme a decisao humana. Se editar ou descartar, a Taliya registra a decisao e mantem continuidade em /app/vendas/captura; /app/interessados; tarefa.
- Ajustes afetados: fontes aceitas; dono do lead; regra de duplicidade
- Encadeamento: /app/vendas/captura; /app/interessados; tarefa

**Autonomo com aprovacao** (habilitado)

- Inicio: O fluxo comeca quando surge um caso para capturar lead de multiplos canais e criar ficha unica. A Taliya identifica o caso, confere fonte e aceita; lead tem contato identificavel; duplicidade foi verificada e prepara a revisao.
- Meio: A Taliya valida fonte e aceita; lead tem contato identificavel; duplicidade foi verificada; dono do lead esta definido e prepara capturar lead de multiplos canais e criar ficha unica. Antes de concluir, mostra impacto/preview e pede aprovacao.
- Fim: Se aprovado, a acao e concluida e auditada. Se recusado, vencido ou incompleto, criar tarefa/caso em /app/vendas/captura; /app/interessados; tarefa e manter auditoria do motivo.
- Ajustes afetados: fontes aceitas; dono do lead; regra de duplicidade
- Encadeamento: /app/vendas/captura; /app/interessados; tarefa

**Autonomo com excecoes** (habilitado)

- Inicio: O fluxo comeca quando surge um caso para capturar lead de multiplos canais e criar ficha unica. A Taliya identifica o caso e valida os dados principais: fonte e aceita; lead tem contato identificavel; duplicidade foi verificada.
- Meio: A Taliya executa sozinha quando fonte e aceita; lead tem contato identificavel; duplicidade foi verificada; dono do lead esta definido; campos minimos foram preenchidos. Ela chama a equipe quando lead duplicado; fonte nao reconhecida; contato incompleto; lead ja pertence a outro responsavel; canal, cota ou permissao bloqueia criacao.
- Fim: No caso comum, a acao `capturar lead de multiplos canais e criar ficha unica` fica registrada e auditada. Se houver excecao, criar tarefa/caso em /app/vendas/captura; /app/interessados; tarefa e manter auditoria do motivo.
- Ajustes afetados: fontes aceitas; dono do lead; regra de duplicidade
- Encadeamento: /app/vendas/captura; /app/interessados; tarefa

**Autonomo** (bloqueado)

- Inicio: Este modo fica bloqueado para Entrada multicanal de lead.
- Meio: A Taliya nao conclui end-to-end porque este modo esta acima do teto do fluxo.
- Fim: Use o maior modo habilitado para automatizar o caso comum sem ultrapassar os limites publicados.
- Ajustes afetados: fontes aceitas; dono do lead; regra de duplicidade
- Encadeamento: /app/vendas/captura; /app/interessados; tarefa


## Agente: Financeiro


### Rotina: Lembretes e pagamentos


#### Lembrete vencimento

**Manual** (habilitado)

- Inicio: O fluxo comeca quando surge um caso para enviar lembrete de vencimento. A Taliya identifica o caso e organiza o contexto principal: cobranca existe; vencimento esta proximo conforme horario configurado; aluno tem canal permitido.
- Meio: A Taliya cria tarefa, checklist ou caso para a equipe enviar lembrete de vencimento. A decisao e a execucao principal ficam com o humano.
- Fim: O fluxo termina quando a equipe registra o resultado. A Taliya salva auditoria e, se nao puder seguir, criar tarefa/caso em /app/financeiro/movimentacoes; execucao; tarefa e manter auditoria do motivo.
- Ajustes afetados: horario; template; limite por cobranca
- Encadeamento: /app/financeiro/movimentacoes; execucao; tarefa

**Copiloto** (habilitado)

- Inicio: O fluxo comeca quando surge um caso para enviar lembrete de vencimento. A Taliya identifica o contexto e mostra a base da sugestao: cobranca existe; vencimento esta proximo conforme horario configurado; aluno tem canal permitido.
- Meio: A Taliya sugere enviar lembrete de vencimento, prepara texto/resumo/proximo passo e mostra os dados usados. A equipe pode aceitar, editar ou descartar antes de executar.
- Fim: Se a equipe aceitar, a acao e registrada conforme a decisao humana. Se editar ou descartar, a Taliya registra a decisao e mantem continuidade em /app/financeiro/movimentacoes; execucao; tarefa.
- Ajustes afetados: horario; template; limite por cobranca
- Encadeamento: /app/financeiro/movimentacoes; execucao; tarefa

**Autonomo com aprovacao** (habilitado)

- Inicio: O fluxo comeca quando surge um caso para enviar lembrete de vencimento. A Taliya identifica o caso, confere cobranca existe; vencimento esta proximo conforme horario configurado; aluno tem canal permitido e prepara a revisao.
- Meio: A Taliya valida cobranca existe; vencimento esta proximo conforme horario configurado; aluno tem canal permitido; template aprovado esta disponivel e prepara enviar lembrete de vencimento. Antes de concluir, mostra impacto/preview e pede aprovacao.
- Fim: Se aprovado, a acao e concluida e auditada. Se recusado, vencido ou incompleto, criar tarefa/caso em /app/financeiro/movimentacoes; execucao; tarefa e manter auditoria do motivo.
- Ajustes afetados: horario; template; limite por cobranca
- Encadeamento: /app/financeiro/movimentacoes; execucao; tarefa

**Autonomo com excecoes** (habilitado)

- Inicio: O fluxo comeca quando surge um caso para enviar lembrete de vencimento. A Taliya identifica o caso e valida os dados principais: cobranca existe; vencimento esta proximo conforme horario configurado; aluno tem canal permitido.
- Meio: A Taliya executa sozinha quando cobranca existe; vencimento esta proximo conforme horario configurado; aluno tem canal permitido; template aprovado esta disponivel; limite por cobranca nao foi atingido. Ela chama a equipe quando cobranca foi paga ou cancelada; aluno pediu opt-out; valor ou vencimento diverge; mensagem falha; canal, cota ou permissao bloqueia envio.
- Fim: No caso comum, a acao `enviar lembrete de vencimento` fica registrada e auditada. Se houver excecao, criar tarefa/caso em /app/financeiro/movimentacoes; execucao; tarefa e manter auditoria do motivo.
- Ajustes afetados: horario; template; limite por cobranca
- Encadeamento: /app/financeiro/movimentacoes; execucao; tarefa

**Autonomo** (habilitado)

- Inicio: O fluxo comeca quando surge um caso para enviar lembrete de vencimento. A Taliya identifica o caso e confirma cobranca existe; vencimento esta proximo conforme horario configurado; aluno tem canal permitido.
- Meio: A Taliya conclui enviar lembrete de vencimento quando cobranca existe; vencimento esta proximo conforme horario configurado; aluno tem canal permitido; template aprovado esta disponivel; limite por cobranca nao foi atingido. Ela para quando cobranca foi paga ou cancelada; aluno pediu opt-out; valor ou vencimento diverge; mensagem falha; canal, cota ou permissao bloqueia envio.
- Fim: A acao e concluida, a auditoria fica salva e a continuidade segue em /app/financeiro/movimentacoes; execucao; tarefa. Se houver bloqueio, criar tarefa/caso em /app/financeiro/movimentacoes; execucao; tarefa e manter auditoria do motivo.
- Ajustes afetados: horario; template; limite por cobranca
- Encadeamento: /app/financeiro/movimentacoes; execucao; tarefa


#### Pagamento atrasado

**Manual** (habilitado)

- Inicio: O fluxo comeca quando surge um caso para tratar pagamento atrasado e abrir cobranca ou tarefa. A Taliya identifica o caso e organiza o contexto principal: movimentacao esta vencida; tentativas permitem novo contato; fila financeira esta definida.
- Meio: A Taliya cria tarefa, checklist ou caso para a equipe tratar pagamento atrasado e abrir cobranca ou tarefa. A decisao e a execucao principal ficam com o humano.
- Fim: O fluxo termina quando a equipe registra o resultado. A Taliya salva auditoria e, se nao puder seguir, criar tarefa/caso em /app/financeiro/movimentacoes/[id]; tarefa financeira e manter auditoria do motivo.
- Ajustes afetados: tentativas; fila financeira; sinais que chamam humano
- Encadeamento: /app/financeiro/movimentacoes/[id]; tarefa financeira

**Copiloto** (habilitado)

- Inicio: O fluxo comeca quando surge um caso para tratar pagamento atrasado e abrir cobranca ou tarefa. A Taliya identifica o contexto e mostra a base da sugestao: movimentacao esta vencida; tentativas permitem novo contato; fila financeira esta definida.
- Meio: A Taliya sugere tratar pagamento atrasado e abrir cobranca ou tarefa, prepara texto/resumo/proximo passo e mostra os dados usados. A equipe pode aceitar, editar ou descartar antes de executar.
- Fim: Se a equipe aceitar, a acao e registrada conforme a decisao humana. Se editar ou descartar, a Taliya registra a decisao e mantem continuidade em /app/financeiro/movimentacoes/[id]; tarefa financeira.
- Ajustes afetados: tentativas; fila financeira; sinais que chamam humano
- Encadeamento: /app/financeiro/movimentacoes/[id]; tarefa financeira

**Autonomo com aprovacao** (habilitado)

- Inicio: O fluxo comeca quando surge um caso para tratar pagamento atrasado e abrir cobranca ou tarefa. A Taliya identifica o caso, confere movimentacao esta vencida; tentativas permitem novo contato; fila financeira esta definida e prepara a revisao.
- Meio: A Taliya valida movimentacao esta vencida; tentativas permitem novo contato; fila financeira esta definida; mensagem aprovada esta disponivel e prepara tratar pagamento atrasado e abrir cobranca ou tarefa. Antes de concluir, mostra impacto/preview e pede aprovacao.
- Fim: Se aprovado, a acao e concluida e auditada. Se recusado, vencido ou incompleto, criar tarefa/caso em /app/financeiro/movimentacoes/[id]; tarefa financeira e manter auditoria do motivo.
- Ajustes afetados: tentativas; fila financeira; sinais que chamam humano
- Encadeamento: /app/financeiro/movimentacoes/[id]; tarefa financeira

**Autonomo com excecoes** (habilitado)

- Inicio: O fluxo comeca quando surge um caso para tratar pagamento atrasado e abrir cobranca ou tarefa. A Taliya identifica o caso e valida os dados principais: movimentacao esta vencida; tentativas permitem novo contato; fila financeira esta definida.
- Meio: A Taliya executa sozinha quando movimentacao esta vencida; tentativas permitem novo contato; fila financeira esta definida; mensagem aprovada esta disponivel; nao ha disputa registrada. Ela chama a equipe quando aluno contesta valor; pedido envolve acordo, desconto ou prazo especial; pagamento pode ter sido feito; provedor apresenta falha; canal, cota ou permissao bloqueia contato.
- Fim: No caso comum, a acao `tratar pagamento atrasado e abrir cobranca ou tarefa` fica registrada e auditada. Se houver excecao, criar tarefa/caso em /app/financeiro/movimentacoes/[id]; tarefa financeira e manter auditoria do motivo.
- Ajustes afetados: tentativas; fila financeira; sinais que chamam humano
- Encadeamento: /app/financeiro/movimentacoes/[id]; tarefa financeira

**Autonomo** (bloqueado)

- Inicio: Este modo fica bloqueado para Pagamento atrasado.
- Meio: A Taliya nao conclui end-to-end porque este modo esta acima do teto do fluxo.
- Fim: Use o maior modo habilitado para automatizar o caso comum sem ultrapassar os limites publicados.
- Ajustes afetados: tentativas; fila financeira; sinais que chamam humano
- Encadeamento: /app/financeiro/movimentacoes/[id]; tarefa financeira


#### Pix/link

**Manual** (habilitado)

- Inicio: O fluxo comeca quando surge um caso para preparar Pix ou link de pagamento para aprovacao. A Taliya identifica o caso e organiza o contexto principal: movimentacao esta identificada; valor esta dentro do limite; template esta aprovado.
- Meio: A Taliya cria tarefa, checklist ou caso para a equipe preparar Pix ou link de pagamento para aprovacao. A decisao e a execucao principal ficam com o humano.
- Fim: O fluxo termina quando a equipe registra o resultado. A Taliya salva auditoria e, se nao puder seguir, criar tarefa/caso em /app/financeiro/movimentacoes; /app/aprovacoes e manter auditoria do motivo.
- Ajustes afetados: aprovador; template; limite de valor
- Encadeamento: /app/financeiro/movimentacoes; /app/aprovacoes

**Copiloto** (habilitado)

- Inicio: O fluxo comeca quando surge um caso para preparar Pix ou link de pagamento para aprovacao. A Taliya identifica o contexto e mostra a base da sugestao: movimentacao esta identificada; valor esta dentro do limite; template esta aprovado.
- Meio: A Taliya sugere preparar Pix ou link de pagamento para aprovacao, prepara texto/resumo/proximo passo e mostra os dados usados. A equipe pode aceitar, editar ou descartar antes de executar.
- Fim: Se a equipe aceitar, a acao e registrada conforme a decisao humana. Se editar ou descartar, a Taliya registra a decisao e mantem continuidade em /app/financeiro/movimentacoes; /app/aprovacoes.
- Ajustes afetados: aprovador; template; limite de valor
- Encadeamento: /app/financeiro/movimentacoes; /app/aprovacoes

**Autonomo com aprovacao** (habilitado)

- Inicio: O fluxo comeca quando surge um caso para preparar Pix ou link de pagamento para aprovacao. A Taliya identifica o caso, confere movimentacao esta identificada; valor esta dentro do limite; template esta aprovado e prepara a revisao.
- Meio: A Taliya valida movimentacao esta identificada; valor esta dentro do limite; template esta aprovado; provedor financeiro esta ok e prepara preparar Pix ou link de pagamento para aprovacao. Antes de concluir, mostra impacto/preview e pede aprovacao.
- Fim: Se aprovado, a acao e concluida e auditada. Se recusado, vencido ou incompleto, criar tarefa/caso em /app/financeiro/movimentacoes; /app/aprovacoes e manter auditoria do motivo.
- Ajustes afetados: aprovador; template; limite de valor
- Encadeamento: /app/financeiro/movimentacoes; /app/aprovacoes

**Autonomo com excecoes** (bloqueado)

- Inicio: Este modo fica bloqueado para Pix/link.
- Meio: A Taliya nao executa com excecoes porque o teto deste fluxo e menor.
- Fim: O usuario deve escolher um modo permitido para este fluxo.
- Ajustes afetados: aprovador; template; limite de valor
- Encadeamento: /app/financeiro/movimentacoes; /app/aprovacoes

**Autonomo** (bloqueado)

- Inicio: Este modo fica bloqueado para Pix/link.
- Meio: A Taliya nao conclui end-to-end porque este modo esta acima do teto do fluxo.
- Fim: Use o maior modo habilitado para automatizar o caso comum sem ultrapassar os limites publicados.
- Ajustes afetados: aprovador; template; limite de valor
- Encadeamento: /app/financeiro/movimentacoes; /app/aprovacoes


### Rotina: Excecoes e documentos financeiros


#### Confirmacao pagamento

**Manual** (habilitado)

- Inicio: O fluxo comeca quando surge um caso para preparar confirmacao de pagamento para aprovacao. A Taliya identifica o caso e organiza o contexto principal: movimentacao foi localizada; evidencia de pagamento foi anexada; valor e aluno conferem.
- Meio: A Taliya cria tarefa, checklist ou caso para a equipe preparar confirmacao de pagamento para aprovacao. A decisao e a execucao principal ficam com o humano.
- Fim: O fluxo termina quando a equipe registra o resultado. A Taliya salva auditoria e, se nao puder seguir, criar tarefa/caso em /app/financeiro/movimentacoes/[id]; aprovacao e manter auditoria do motivo.
- Ajustes afetados: aprovador; evidencia exigida; responsavel
- Encadeamento: /app/financeiro/movimentacoes/[id]; aprovacao

**Copiloto** (habilitado)

- Inicio: O fluxo comeca quando surge um caso para preparar confirmacao de pagamento para aprovacao. A Taliya identifica o contexto e mostra a base da sugestao: movimentacao foi localizada; evidencia de pagamento foi anexada; valor e aluno conferem.
- Meio: A Taliya sugere preparar confirmacao de pagamento para aprovacao, prepara texto/resumo/proximo passo e mostra os dados usados. A equipe pode aceitar, editar ou descartar antes de executar.
- Fim: Se a equipe aceitar, a acao e registrada conforme a decisao humana. Se editar ou descartar, a Taliya registra a decisao e mantem continuidade em /app/financeiro/movimentacoes/[id]; aprovacao.
- Ajustes afetados: aprovador; evidencia exigida; responsavel
- Encadeamento: /app/financeiro/movimentacoes/[id]; aprovacao

**Autonomo com aprovacao** (habilitado)

- Inicio: O fluxo comeca quando surge um caso para preparar confirmacao de pagamento para aprovacao. A Taliya identifica o caso, confere movimentacao foi localizada; evidencia de pagamento foi anexada; valor e aluno conferem e prepara a revisao.
- Meio: A Taliya valida movimentacao foi localizada; evidencia de pagamento foi anexada; valor e aluno conferem; responsavel financeiro esta definido e prepara preparar confirmacao de pagamento para aprovacao. Antes de concluir, mostra impacto/preview e pede aprovacao.
- Fim: Se aprovado, a acao e concluida e auditada. Se recusado, vencido ou incompleto, criar tarefa/caso em /app/financeiro/movimentacoes/[id]; aprovacao e manter auditoria do motivo.
- Ajustes afetados: aprovador; evidencia exigida; responsavel
- Encadeamento: /app/financeiro/movimentacoes/[id]; aprovacao

**Autonomo com excecoes** (bloqueado)

- Inicio: Este modo fica bloqueado para Confirmacao pagamento.
- Meio: A Taliya nao executa com excecoes porque o teto deste fluxo e menor.
- Fim: O usuario deve escolher um modo permitido para este fluxo.
- Ajustes afetados: aprovador; evidencia exigida; responsavel
- Encadeamento: /app/financeiro/movimentacoes/[id]; aprovacao

**Autonomo** (bloqueado)

- Inicio: Este modo fica bloqueado para Confirmacao pagamento.
- Meio: A Taliya nao conclui end-to-end porque este modo esta acima do teto do fluxo.
- Fim: Use o maior modo habilitado para automatizar o caso comum sem ultrapassar os limites publicados.
- Ajustes afetados: aprovador; evidencia exigida; responsavel
- Encadeamento: /app/financeiro/movimentacoes/[id]; aprovacao


### Rotina: Ciclo do plano do aluno


#### Renovacao plano

**Manual** (habilitado)

- Inicio: O fluxo comeca quando surge um caso para preparar renovacao de plano. A Taliya identifica o caso e organiza o contexto principal: plano atual e aluno foram identificados; antecedencia configurada chegou; novo ciclo foi calculado.
- Meio: A Taliya cria tarefa, checklist ou caso para a equipe preparar renovacao de plano. A decisao e a execucao principal ficam com o humano.
- Fim: O fluxo termina quando a equipe registra o resultado. A Taliya salva auditoria e, se nao puder seguir, criar tarefa/caso em /app/alunos/[id]; /app/financeiro; aprovacao e manter auditoria do motivo.
- Ajustes afetados: aprovador; antecedencia; template
- Encadeamento: /app/alunos/[id]; /app/financeiro; aprovacao

**Copiloto** (habilitado)

- Inicio: O fluxo comeca quando surge um caso para preparar renovacao de plano. A Taliya identifica o contexto e mostra a base da sugestao: plano atual e aluno foram identificados; antecedencia configurada chegou; novo ciclo foi calculado.
- Meio: A Taliya sugere preparar renovacao de plano, prepara texto/resumo/proximo passo e mostra os dados usados. A equipe pode aceitar, editar ou descartar antes de executar.
- Fim: Se a equipe aceitar, a acao e registrada conforme a decisao humana. Se editar ou descartar, a Taliya registra a decisao e mantem continuidade em /app/alunos/[id]; /app/financeiro; aprovacao.
- Ajustes afetados: aprovador; antecedencia; template
- Encadeamento: /app/alunos/[id]; /app/financeiro; aprovacao

**Autonomo com aprovacao** (habilitado)

- Inicio: O fluxo comeca quando surge um caso para preparar renovacao de plano. A Taliya identifica o caso, confere plano atual e aluno foram identificados; antecedencia configurada chegou; novo ciclo foi calculado e prepara a revisao.
- Meio: A Taliya valida plano atual e aluno foram identificados; antecedencia configurada chegou; novo ciclo foi calculado; template de renovacao esta aprovado e prepara preparar renovacao de plano. Antes de concluir, mostra impacto/preview e pede aprovacao.
- Fim: Se aprovado, a acao e concluida e auditada. Se recusado, vencido ou incompleto, criar tarefa/caso em /app/alunos/[id]; /app/financeiro; aprovacao e manter auditoria do motivo.
- Ajustes afetados: aprovador; antecedencia; template
- Encadeamento: /app/alunos/[id]; /app/financeiro; aprovacao

**Autonomo com excecoes** (bloqueado)

- Inicio: Este modo fica bloqueado para Renovacao plano.
- Meio: A Taliya nao executa com excecoes porque o teto deste fluxo e menor.
- Fim: O usuario deve escolher um modo permitido para este fluxo.
- Ajustes afetados: aprovador; antecedencia; template
- Encadeamento: /app/alunos/[id]; /app/financeiro; aprovacao

**Autonomo** (bloqueado)

- Inicio: Este modo fica bloqueado para Renovacao plano.
- Meio: A Taliya nao conclui end-to-end porque este modo esta acima do teto do fluxo.
- Fim: Use o maior modo habilitado para automatizar o caso comum sem ultrapassar os limites publicados.
- Ajustes afetados: aprovador; antecedencia; template
- Encadeamento: /app/alunos/[id]; /app/financeiro; aprovacao


### Rotina: Excecoes e documentos financeiros


#### Excecoes financeiras

**Manual** (habilitado)

- Inicio: O fluxo comeca quando surge um caso para preparar excecao financeira para aprovacao. A Taliya identifica o caso e organiza o contexto principal: tipo de excecao foi classificado; motivo foi informado; impacto financeiro foi calculado.
- Meio: A Taliya cria tarefa, checklist ou caso para a equipe preparar excecao financeira para aprovacao. A decisao e a execucao principal ficam com o humano.
- Fim: O fluxo termina quando a equipe registra o resultado. A Taliya salva auditoria e, se nao puder seguir, criar tarefa/caso em /app/financeiro/movimentacoes; /app/aprovacoes; caso e manter auditoria do motivo.
- Ajustes afetados: aprovador obrigatorio; tipos de excecao; prazo
- Encadeamento: /app/financeiro/movimentacoes; /app/aprovacoes; caso

**Copiloto** (habilitado)

- Inicio: O fluxo comeca quando surge um caso para preparar excecao financeira para aprovacao. A Taliya identifica o contexto e mostra a base da sugestao: tipo de excecao foi classificado; motivo foi informado; impacto financeiro foi calculado.
- Meio: A Taliya sugere preparar excecao financeira para aprovacao, prepara texto/resumo/proximo passo e mostra os dados usados. A equipe pode aceitar, editar ou descartar antes de executar.
- Fim: Se a equipe aceitar, a acao e registrada conforme a decisao humana. Se editar ou descartar, a Taliya registra a decisao e mantem continuidade em /app/financeiro/movimentacoes; /app/aprovacoes; caso.
- Ajustes afetados: aprovador obrigatorio; tipos de excecao; prazo
- Encadeamento: /app/financeiro/movimentacoes; /app/aprovacoes; caso

**Autonomo com aprovacao** (habilitado)

- Inicio: O fluxo comeca quando surge um caso para preparar excecao financeira para aprovacao. A Taliya identifica o caso, confere tipo de excecao foi classificado; motivo foi informado; impacto financeiro foi calculado e prepara a revisao.
- Meio: A Taliya valida tipo de excecao foi classificado; motivo foi informado; impacto financeiro foi calculado; prazo do caso esta definido e prepara preparar excecao financeira para aprovacao. Antes de concluir, mostra impacto/preview e pede aprovacao.
- Fim: Se aprovado, a acao e concluida e auditada. Se recusado, vencido ou incompleto, criar tarefa/caso em /app/financeiro/movimentacoes; /app/aprovacoes; caso e manter auditoria do motivo.
- Ajustes afetados: aprovador obrigatorio; tipos de excecao; prazo
- Encadeamento: /app/financeiro/movimentacoes; /app/aprovacoes; caso

**Autonomo com excecoes** (bloqueado)

- Inicio: Este modo fica bloqueado para Excecoes financeiras.
- Meio: A Taliya nao executa com excecoes porque o teto deste fluxo e menor.
- Fim: O usuario deve escolher um modo permitido para este fluxo.
- Ajustes afetados: aprovador obrigatorio; tipos de excecao; prazo
- Encadeamento: /app/financeiro/movimentacoes; /app/aprovacoes; caso

**Autonomo** (bloqueado)

- Inicio: Este modo fica bloqueado para Excecoes financeiras.
- Meio: A Taliya nao conclui end-to-end porque este modo esta acima do teto do fluxo.
- Fim: Use o maior modo habilitado para automatizar o caso comum sem ultrapassar os limites publicados.
- Ajustes afetados: aprovador obrigatorio; tipos de excecao; prazo
- Encadeamento: /app/financeiro/movimentacoes; /app/aprovacoes; caso


### Rotina: Lembretes e pagamentos


#### Falha pagamento

**Manual** (habilitado)

- Inicio: O fluxo comeca quando surge um caso para tratar falha de pagamento. A Taliya identifica o caso e organiza o contexto principal: falha veio do provedor; tentativas permitem novo contato; fila financeira esta definida.
- Meio: A Taliya cria tarefa, checklist ou caso para a equipe tratar falha de pagamento. A decisao e a execucao principal ficam com o humano.
- Fim: O fluxo termina quando a equipe registra o resultado. A Taliya salva auditoria e, se nao puder seguir, criar tarefa/caso em /app/financeiro/movimentacoes/[id]; tarefa/caso e manter auditoria do motivo.
- Ajustes afetados: fila financeira; tentativas; quando abrir caso
- Encadeamento: /app/financeiro/movimentacoes/[id]; tarefa/caso

**Copiloto** (habilitado)

- Inicio: O fluxo comeca quando surge um caso para tratar falha de pagamento. A Taliya identifica o contexto e mostra a base da sugestao: falha veio do provedor; tentativas permitem novo contato; fila financeira esta definida.
- Meio: A Taliya sugere tratar falha de pagamento, prepara texto/resumo/proximo passo e mostra os dados usados. A equipe pode aceitar, editar ou descartar antes de executar.
- Fim: Se a equipe aceitar, a acao e registrada conforme a decisao humana. Se editar ou descartar, a Taliya registra a decisao e mantem continuidade em /app/financeiro/movimentacoes/[id]; tarefa/caso.
- Ajustes afetados: fila financeira; tentativas; quando abrir caso
- Encadeamento: /app/financeiro/movimentacoes/[id]; tarefa/caso

**Autonomo com aprovacao** (habilitado)

- Inicio: O fluxo comeca quando surge um caso para tratar falha de pagamento. A Taliya identifica o caso, confere falha veio do provedor; tentativas permitem novo contato; fila financeira esta definida e prepara a revisao.
- Meio: A Taliya valida falha veio do provedor; tentativas permitem novo contato; fila financeira esta definida; mensagem aprovada esta disponivel e prepara tratar falha de pagamento. Antes de concluir, mostra impacto/preview e pede aprovacao.
- Fim: Se aprovado, a acao e concluida e auditada. Se recusado, vencido ou incompleto, criar tarefa/caso em /app/financeiro/movimentacoes/[id]; tarefa/caso e manter auditoria do motivo.
- Ajustes afetados: fila financeira; tentativas; quando abrir caso
- Encadeamento: /app/financeiro/movimentacoes/[id]; tarefa/caso

**Autonomo com excecoes** (habilitado)

- Inicio: O fluxo comeca quando surge um caso para tratar falha de pagamento. A Taliya identifica o caso e valida os dados principais: falha veio do provedor; tentativas permitem novo contato; fila financeira esta definida.
- Meio: A Taliya executa sozinha quando falha veio do provedor; tentativas permitem novo contato; fila financeira esta definida; mensagem aprovada esta disponivel; nao ha disputa aberta. Ela chama a equipe quando falha persiste apos tentativas; aluno contesta cobranca; provedor retorna erro tecnico; caso exige bloqueio ou liberacao; canal, cota ou permissao bloqueia contato.
- Fim: No caso comum, a acao `tratar falha de pagamento` fica registrada e auditada. Se houver excecao, criar tarefa/caso em /app/financeiro/movimentacoes/[id]; tarefa/caso e manter auditoria do motivo.
- Ajustes afetados: fila financeira; tentativas; quando abrir caso
- Encadeamento: /app/financeiro/movimentacoes/[id]; tarefa/caso

**Autonomo** (bloqueado)

- Inicio: Este modo fica bloqueado para Falha pagamento.
- Meio: A Taliya nao conclui end-to-end porque este modo esta acima do teto do fluxo.
- Fim: Use o maior modo habilitado para automatizar o caso comum sem ultrapassar os limites publicados.
- Ajustes afetados: fila financeira; tentativas; quando abrir caso
- Encadeamento: /app/financeiro/movimentacoes/[id]; tarefa/caso


#### Recibo/nota

**Manual** (habilitado)

- Inicio: O fluxo comeca quando surge um caso para emitir ou preparar recibo/nota permitida. A Taliya identifica o caso e organiza o contexto principal: pagamento foi confirmado; tipo de documento e permitido; dados do aluno conferem.
- Meio: A Taliya cria tarefa, checklist ou caso para a equipe emitir ou preparar recibo/nota permitida. A decisao e a execucao principal ficam com o humano.
- Fim: O fluxo termina quando a equipe registra o resultado. A Taliya salva auditoria e, se nao puder seguir, criar tarefa/caso em /app/financeiro/documentos; tarefa e manter auditoria do motivo.
- Ajustes afetados: responsavel; tipo de documento; quando abrir tarefa
- Encadeamento: /app/financeiro/documentos; tarefa

**Copiloto** (habilitado)

- Inicio: O fluxo comeca quando surge um caso para emitir ou preparar recibo/nota permitida. A Taliya identifica o contexto e mostra a base da sugestao: pagamento foi confirmado; tipo de documento e permitido; dados do aluno conferem.
- Meio: A Taliya sugere emitir ou preparar recibo/nota permitida, prepara texto/resumo/proximo passo e mostra os dados usados. A equipe pode aceitar, editar ou descartar antes de executar.
- Fim: Se a equipe aceitar, a acao e registrada conforme a decisao humana. Se editar ou descartar, a Taliya registra a decisao e mantem continuidade em /app/financeiro/documentos; tarefa.
- Ajustes afetados: responsavel; tipo de documento; quando abrir tarefa
- Encadeamento: /app/financeiro/documentos; tarefa

**Autonomo com aprovacao** (habilitado)

- Inicio: O fluxo comeca quando surge um caso para emitir ou preparar recibo/nota permitida. A Taliya identifica o caso, confere pagamento foi confirmado; tipo de documento e permitido; dados do aluno conferem e prepara a revisao.
- Meio: A Taliya valida pagamento foi confirmado; tipo de documento e permitido; dados do aluno conferem; responsavel esta definido e prepara emitir ou preparar recibo/nota permitida. Antes de concluir, mostra impacto/preview e pede aprovacao.
- Fim: Se aprovado, a acao e concluida e auditada. Se recusado, vencido ou incompleto, criar tarefa/caso em /app/financeiro/documentos; tarefa e manter auditoria do motivo.
- Ajustes afetados: responsavel; tipo de documento; quando abrir tarefa
- Encadeamento: /app/financeiro/documentos; tarefa

**Autonomo com excecoes** (habilitado)

- Inicio: O fluxo comeca quando surge um caso para emitir ou preparar recibo/nota permitida. A Taliya identifica o caso e valida os dados principais: pagamento foi confirmado; tipo de documento e permitido; dados do aluno conferem.
- Meio: A Taliya executa sozinha quando pagamento foi confirmado; tipo de documento e permitido; dados do aluno conferem; responsavel esta definido; fallback para tarefa existe. Ela chama a equipe quando documento nao e permitido; dados fiscais faltam; pagamento nao esta conciliado; aluno pede documento especial; permissao ou provedor bloqueia emissao.
- Fim: No caso comum, a acao `emitir ou preparar recibo/nota permitida` fica registrada e auditada. Se houver excecao, criar tarefa/caso em /app/financeiro/documentos; tarefa e manter auditoria do motivo.
- Ajustes afetados: responsavel; tipo de documento; quando abrir tarefa
- Encadeamento: /app/financeiro/documentos; tarefa

**Autonomo** (bloqueado)

- Inicio: Este modo fica bloqueado para Recibo/nota.
- Meio: A Taliya nao conclui end-to-end porque este modo esta acima do teto do fluxo.
- Fim: Use o maior modo habilitado para automatizar o caso comum sem ultrapassar os limites publicados.
- Ajustes afetados: responsavel; tipo de documento; quando abrir tarefa
- Encadeamento: /app/financeiro/documentos; tarefa


### Rotina: Ciclo do plano do aluno


#### Pausa/trancamento

**Manual** (habilitado)

- Inicio: O fluxo comeca quando surge um caso para preparar pausa ou trancamento para aprovacao. A Taliya identifica o caso e organiza o contexto principal: aluno e plano foram identificados; motivo foi informado; impacto em agenda e cobranca foi calculado.
- Meio: A Taliya cria tarefa, checklist ou caso para a equipe preparar pausa ou trancamento para aprovacao. A decisao e a execucao principal ficam com o humano.
- Fim: O fluxo termina quando a equipe registra o resultado. A Taliya salva auditoria e, se nao puder seguir, criar tarefa/caso em /app/financeiro; /app/alunos/[id]; aprovacao/caso e manter auditoria do motivo.
- Ajustes afetados: aprovador; data de inicio/fim; prazo de aprovacao
- Encadeamento: /app/financeiro; /app/alunos/[id]; aprovacao/caso

**Copiloto** (habilitado)

- Inicio: O fluxo comeca quando surge um caso para preparar pausa ou trancamento para aprovacao. A Taliya identifica o contexto e mostra a base da sugestao: aluno e plano foram identificados; motivo foi informado; impacto em agenda e cobranca foi calculado.
- Meio: A Taliya sugere preparar pausa ou trancamento para aprovacao, prepara texto/resumo/proximo passo e mostra os dados usados. A equipe pode aceitar, editar ou descartar antes de executar.
- Fim: Se a equipe aceitar, a acao e registrada conforme a decisao humana. Se editar ou descartar, a Taliya registra a decisao e mantem continuidade em /app/financeiro; /app/alunos/[id]; aprovacao/caso.
- Ajustes afetados: aprovador; data de inicio/fim; prazo de aprovacao
- Encadeamento: /app/financeiro; /app/alunos/[id]; aprovacao/caso

**Autonomo com aprovacao** (habilitado)

- Inicio: O fluxo comeca quando surge um caso para preparar pausa ou trancamento para aprovacao. A Taliya identifica o caso, confere aluno e plano foram identificados; motivo foi informado; impacto em agenda e cobranca foi calculado e prepara a revisao.
- Meio: A Taliya valida aluno e plano foram identificados; motivo foi informado; impacto em agenda e cobranca foi calculado; prazo esta definido e prepara preparar pausa ou trancamento para aprovacao. Antes de concluir, mostra impacto/preview e pede aprovacao.
- Fim: Se aprovado, a acao e concluida e auditada. Se recusado, vencido ou incompleto, criar tarefa/caso em /app/financeiro; /app/alunos/[id]; aprovacao/caso e manter auditoria do motivo.
- Ajustes afetados: aprovador; data de inicio/fim; prazo de aprovacao
- Encadeamento: /app/financeiro; /app/alunos/[id]; aprovacao/caso

**Autonomo com excecoes** (bloqueado)

- Inicio: Este modo fica bloqueado para Pausa/trancamento.
- Meio: A Taliya nao executa com excecoes porque o teto deste fluxo e menor.
- Fim: O usuario deve escolher um modo permitido para este fluxo.
- Ajustes afetados: aprovador; data de inicio/fim; prazo de aprovacao
- Encadeamento: /app/financeiro; /app/alunos/[id]; aprovacao/caso

**Autonomo** (bloqueado)

- Inicio: Este modo fica bloqueado para Pausa/trancamento.
- Meio: A Taliya nao conclui end-to-end porque este modo esta acima do teto do fluxo.
- Fim: Use o maior modo habilitado para automatizar o caso comum sem ultrapassar os limites publicados.
- Ajustes afetados: aprovador; data de inicio/fim; prazo de aprovacao
- Encadeamento: /app/financeiro; /app/alunos/[id]; aprovacao/caso


### Rotina: Lembretes e pagamentos


#### Conciliacao interna

**Manual** (habilitado)

- Inicio: O fluxo comeca quando surge um caso para preparar conciliacao interna para aprovacao. A Taliya identifica o caso e organiza o contexto principal: movimentacao e pagamento candidato foram encontrados; confianca minima foi atingida; responsavel financeiro esta definido.
- Meio: A Taliya cria tarefa, checklist ou caso para a equipe preparar conciliacao interna para aprovacao. A decisao e a execucao principal ficam com o humano.
- Fim: O fluxo termina quando a equipe registra o resultado. A Taliya salva auditoria e, se nao puder seguir, criar tarefa/caso em /app/financeiro/movimentacoes; tarefa financeira e manter auditoria do motivo.
- Ajustes afetados: aprovador; confianca minima; responsavel
- Encadeamento: /app/financeiro/movimentacoes; tarefa financeira

**Copiloto** (habilitado)

- Inicio: O fluxo comeca quando surge um caso para preparar conciliacao interna para aprovacao. A Taliya identifica o contexto e mostra a base da sugestao: movimentacao e pagamento candidato foram encontrados; confianca minima foi atingida; responsavel financeiro esta definido.
- Meio: A Taliya sugere preparar conciliacao interna para aprovacao, prepara texto/resumo/proximo passo e mostra os dados usados. A equipe pode aceitar, editar ou descartar antes de executar.
- Fim: Se a equipe aceitar, a acao e registrada conforme a decisao humana. Se editar ou descartar, a Taliya registra a decisao e mantem continuidade em /app/financeiro/movimentacoes; tarefa financeira.
- Ajustes afetados: aprovador; confianca minima; responsavel
- Encadeamento: /app/financeiro/movimentacoes; tarefa financeira

**Autonomo com aprovacao** (habilitado)

- Inicio: O fluxo comeca quando surge um caso para preparar conciliacao interna para aprovacao. A Taliya identifica o caso, confere movimentacao e pagamento candidato foram encontrados; confianca minima foi atingida; responsavel financeiro esta definido e prepara a revisao.
- Meio: A Taliya valida movimentacao e pagamento candidato foram encontrados; confianca minima foi atingida; responsavel financeiro esta definido; impacto foi mostrado e prepara preparar conciliacao interna para aprovacao. Antes de concluir, mostra impacto/preview e pede aprovacao.
- Fim: Se aprovado, a acao e concluida e auditada. Se recusado, vencido ou incompleto, criar tarefa/caso em /app/financeiro/movimentacoes; tarefa financeira e manter auditoria do motivo.
- Ajustes afetados: aprovador; confianca minima; responsavel
- Encadeamento: /app/financeiro/movimentacoes; tarefa financeira

**Autonomo com excecoes** (bloqueado)

- Inicio: Este modo fica bloqueado para Conciliacao interna.
- Meio: A Taliya nao executa com excecoes porque o teto deste fluxo e menor.
- Fim: O usuario deve escolher um modo permitido para este fluxo.
- Ajustes afetados: aprovador; confianca minima; responsavel
- Encadeamento: /app/financeiro/movimentacoes; tarefa financeira

**Autonomo** (bloqueado)

- Inicio: Este modo fica bloqueado para Conciliacao interna.
- Meio: A Taliya nao conclui end-to-end porque este modo esta acima do teto do fluxo.
- Fim: Use o maior modo habilitado para automatizar o caso comum sem ultrapassar os limites publicados.
- Ajustes afetados: aprovador; confianca minima; responsavel
- Encadeamento: /app/financeiro/movimentacoes; tarefa financeira


### Rotina: Excecoes e documentos financeiros


#### Contrato/termos

**Manual** (habilitado)

- Inicio: O fluxo comeca quando surge um caso para preparar contrato ou termos para aprovacao. A Taliya identifica o caso e organiza o contexto principal: template de contrato esta definido; dados do aluno e plano conferem; prazo de envio esta definido.
- Meio: A Taliya cria tarefa, checklist ou caso para a equipe preparar contrato ou termos para aprovacao. A decisao e a execucao principal ficam com o humano.
- Fim: O fluxo termina quando a equipe registra o resultado. A Taliya salva auditoria e, se nao puder seguir, criar tarefa/caso em /app/contratos; /app/aprovacoes e manter auditoria do motivo.
- Ajustes afetados: aprovador; template; prazo
- Encadeamento: /app/contratos; /app/aprovacoes

**Copiloto** (habilitado)

- Inicio: O fluxo comeca quando surge um caso para preparar contrato ou termos para aprovacao. A Taliya identifica o contexto e mostra a base da sugestao: template de contrato esta definido; dados do aluno e plano conferem; prazo de envio esta definido.
- Meio: A Taliya sugere preparar contrato ou termos para aprovacao, prepara texto/resumo/proximo passo e mostra os dados usados. A equipe pode aceitar, editar ou descartar antes de executar.
- Fim: Se a equipe aceitar, a acao e registrada conforme a decisao humana. Se editar ou descartar, a Taliya registra a decisao e mantem continuidade em /app/contratos; /app/aprovacoes.
- Ajustes afetados: aprovador; template; prazo
- Encadeamento: /app/contratos; /app/aprovacoes

**Autonomo com aprovacao** (habilitado)

- Inicio: O fluxo comeca quando surge um caso para preparar contrato ou termos para aprovacao. A Taliya identifica o caso, confere template de contrato esta definido; dados do aluno e plano conferem; prazo de envio esta definido e prepara a revisao.
- Meio: A Taliya valida template de contrato esta definido; dados do aluno e plano conferem; prazo de envio esta definido; responsavel esta atribuido e prepara preparar contrato ou termos para aprovacao. Antes de concluir, mostra impacto/preview e pede aprovacao.
- Fim: Se aprovado, a acao e concluida e auditada. Se recusado, vencido ou incompleto, criar tarefa/caso em /app/contratos; /app/aprovacoes e manter auditoria do motivo.
- Ajustes afetados: aprovador; template; prazo
- Encadeamento: /app/contratos; /app/aprovacoes

**Autonomo com excecoes** (bloqueado)

- Inicio: Este modo fica bloqueado para Contrato/termos.
- Meio: A Taliya nao executa com excecoes porque o teto deste fluxo e menor.
- Fim: O usuario deve escolher um modo permitido para este fluxo.
- Ajustes afetados: aprovador; template; prazo
- Encadeamento: /app/contratos; /app/aprovacoes

**Autonomo** (bloqueado)

- Inicio: Este modo fica bloqueado para Contrato/termos.
- Meio: A Taliya nao conclui end-to-end porque este modo esta acima do teto do fluxo.
- Fim: Use o maior modo habilitado para automatizar o caso comum sem ultrapassar os limites publicados.
- Ajustes afetados: aprovador; template; prazo
- Encadeamento: /app/contratos; /app/aprovacoes


#### Bloqueio/liberacao

**Manual** (habilitado)

- Inicio: O fluxo comeca quando surge um caso para preparar bloqueio ou liberacao para aprovacao. A Taliya identifica o caso e organiza o contexto principal: aluno e motivo foram identificados; impacto financeiro foi calculado; motivo obrigatorio foi preenchido.
- Meio: A Taliya cria tarefa, checklist ou caso para a equipe preparar bloqueio ou liberacao para aprovacao. A decisao e a execucao principal ficam com o humano.
- Fim: O fluxo termina quando a equipe registra o resultado. A Taliya salva auditoria e, se nao puder seguir, criar tarefa/caso em /app/financeiro; /app/aprovacoes; auditoria e manter auditoria do motivo.
- Ajustes afetados: aprovador; motivo obrigatorio; prazo de aprovacao
- Encadeamento: /app/financeiro; /app/aprovacoes; auditoria

**Copiloto** (habilitado)

- Inicio: O fluxo comeca quando surge um caso para preparar bloqueio ou liberacao para aprovacao. A Taliya identifica o contexto e mostra a base da sugestao: aluno e motivo foram identificados; impacto financeiro foi calculado; motivo obrigatorio foi preenchido.
- Meio: A Taliya sugere preparar bloqueio ou liberacao para aprovacao, prepara texto/resumo/proximo passo e mostra os dados usados. A equipe pode aceitar, editar ou descartar antes de executar.
- Fim: Se a equipe aceitar, a acao e registrada conforme a decisao humana. Se editar ou descartar, a Taliya registra a decisao e mantem continuidade em /app/financeiro; /app/aprovacoes; auditoria.
- Ajustes afetados: aprovador; motivo obrigatorio; prazo de aprovacao
- Encadeamento: /app/financeiro; /app/aprovacoes; auditoria

**Autonomo com aprovacao** (habilitado)

- Inicio: O fluxo comeca quando surge um caso para preparar bloqueio ou liberacao para aprovacao. A Taliya identifica o caso, confere aluno e motivo foram identificados; impacto financeiro foi calculado; motivo obrigatorio foi preenchido e prepara a revisao.
- Meio: A Taliya valida aluno e motivo foram identificados; impacto financeiro foi calculado; motivo obrigatorio foi preenchido; prazo de aprovacao esta definido e prepara preparar bloqueio ou liberacao para aprovacao. Antes de concluir, mostra impacto/preview e pede aprovacao.
- Fim: Se aprovado, a acao e concluida e auditada. Se recusado, vencido ou incompleto, criar tarefa/caso em /app/financeiro; /app/aprovacoes; auditoria e manter auditoria do motivo.
- Ajustes afetados: aprovador; motivo obrigatorio; prazo de aprovacao
- Encadeamento: /app/financeiro; /app/aprovacoes; auditoria

**Autonomo com excecoes** (bloqueado)

- Inicio: Este modo fica bloqueado para Bloqueio/liberacao.
- Meio: A Taliya nao executa com excecoes porque o teto deste fluxo e menor.
- Fim: O usuario deve escolher um modo permitido para este fluxo.
- Ajustes afetados: aprovador; motivo obrigatorio; prazo de aprovacao
- Encadeamento: /app/financeiro; /app/aprovacoes; auditoria

**Autonomo** (bloqueado)

- Inicio: Este modo fica bloqueado para Bloqueio/liberacao.
- Meio: A Taliya nao conclui end-to-end porque este modo esta acima do teto do fluxo.
- Fim: Use o maior modo habilitado para automatizar o caso comum sem ultrapassar os limites publicados.
- Ajustes afetados: aprovador; motivo obrigatorio; prazo de aprovacao
- Encadeamento: /app/financeiro; /app/aprovacoes; auditoria


#### Creditos/cortesias

**Manual** (habilitado)

- Inicio: O fluxo comeca quando surge um caso para preparar credito ou cortesia para aprovacao. A Taliya identifica o caso e organiza o contexto principal: aluno foi identificado; motivo foi informado; limite de valor esta dentro da politica.
- Meio: A Taliya cria tarefa, checklist ou caso para a equipe preparar credito ou cortesia para aprovacao. A decisao e a execucao principal ficam com o humano.
- Fim: O fluxo termina quando a equipe registra o resultado. A Taliya salva auditoria e, se nao puder seguir, criar tarefa/caso em /app/financeiro; /app/aprovacoes e manter auditoria do motivo.
- Ajustes afetados: aprovador; limite de valor; motivo
- Encadeamento: /app/financeiro; /app/aprovacoes

**Copiloto** (habilitado)

- Inicio: O fluxo comeca quando surge um caso para preparar credito ou cortesia para aprovacao. A Taliya identifica o contexto e mostra a base da sugestao: aluno foi identificado; motivo foi informado; limite de valor esta dentro da politica.
- Meio: A Taliya sugere preparar credito ou cortesia para aprovacao, prepara texto/resumo/proximo passo e mostra os dados usados. A equipe pode aceitar, editar ou descartar antes de executar.
- Fim: Se a equipe aceitar, a acao e registrada conforme a decisao humana. Se editar ou descartar, a Taliya registra a decisao e mantem continuidade em /app/financeiro; /app/aprovacoes.
- Ajustes afetados: aprovador; limite de valor; motivo
- Encadeamento: /app/financeiro; /app/aprovacoes

**Autonomo com aprovacao** (habilitado)

- Inicio: O fluxo comeca quando surge um caso para preparar credito ou cortesia para aprovacao. A Taliya identifica o caso, confere aluno foi identificado; motivo foi informado; limite de valor esta dentro da politica e prepara a revisao.
- Meio: A Taliya valida aluno foi identificado; motivo foi informado; limite de valor esta dentro da politica; impacto financeiro foi calculado e prepara preparar credito ou cortesia para aprovacao. Antes de concluir, mostra impacto/preview e pede aprovacao.
- Fim: Se aprovado, a acao e concluida e auditada. Se recusado, vencido ou incompleto, criar tarefa/caso em /app/financeiro; /app/aprovacoes e manter auditoria do motivo.
- Ajustes afetados: aprovador; limite de valor; motivo
- Encadeamento: /app/financeiro; /app/aprovacoes

**Autonomo com excecoes** (bloqueado)

- Inicio: Este modo fica bloqueado para Creditos/cortesias.
- Meio: A Taliya nao executa com excecoes porque o teto deste fluxo e menor.
- Fim: O usuario deve escolher um modo permitido para este fluxo.
- Ajustes afetados: aprovador; limite de valor; motivo
- Encadeamento: /app/financeiro; /app/aprovacoes

**Autonomo** (bloqueado)

- Inicio: Este modo fica bloqueado para Creditos/cortesias.
- Meio: A Taliya nao conclui end-to-end porque este modo esta acima do teto do fluxo.
- Fim: Use o maior modo habilitado para automatizar o caso comum sem ultrapassar os limites publicados.
- Ajustes afetados: aprovador; limite de valor; motivo
- Encadeamento: /app/financeiro; /app/aprovacoes


#### Fechamento mensal

**Manual** (habilitado)

- Inicio: O fluxo comeca quando surge um caso para preparar fechamento mensal financeiro. A Taliya identifica o caso e organiza o contexto principal: periodo de fechamento esta definido; movimentacoes foram consolidadas; pendencias foram separadas.
- Meio: A Taliya cria tarefa, checklist ou caso para a equipe preparar fechamento mensal financeiro. A decisao e a execucao principal ficam com o humano.
- Fim: O fluxo termina quando a equipe registra o resultado. A Taliya salva auditoria e, se nao puder seguir, criar tarefa/caso em /app/relatorios/financeiro; tarefa financeira e manter auditoria do motivo.
- Ajustes afetados: responsavel; frequencia; quando abrir tarefa
- Encadeamento: /app/relatorios/financeiro; tarefa financeira

**Copiloto** (habilitado)

- Inicio: O fluxo comeca quando surge um caso para preparar fechamento mensal financeiro. A Taliya identifica o contexto e mostra a base da sugestao: periodo de fechamento esta definido; movimentacoes foram consolidadas; pendencias foram separadas.
- Meio: A Taliya sugere preparar fechamento mensal financeiro, prepara texto/resumo/proximo passo e mostra os dados usados. A equipe pode aceitar, editar ou descartar antes de executar.
- Fim: Se a equipe aceitar, a acao e registrada conforme a decisao humana. Se editar ou descartar, a Taliya registra a decisao e mantem continuidade em /app/relatorios/financeiro; tarefa financeira.
- Ajustes afetados: responsavel; frequencia; quando abrir tarefa
- Encadeamento: /app/relatorios/financeiro; tarefa financeira

**Autonomo com aprovacao** (habilitado)

- Inicio: O fluxo comeca quando surge um caso para preparar fechamento mensal financeiro. A Taliya identifica o caso, confere periodo de fechamento esta definido; movimentacoes foram consolidadas; pendencias foram separadas e prepara a revisao.
- Meio: A Taliya valida periodo de fechamento esta definido; movimentacoes foram consolidadas; pendencias foram separadas; responsavel financeiro esta definido e prepara preparar fechamento mensal financeiro. Antes de concluir, mostra impacto/preview e pede aprovacao.
- Fim: Se aprovado, a acao e concluida e auditada. Se recusado, vencido ou incompleto, criar tarefa/caso em /app/relatorios/financeiro; tarefa financeira e manter auditoria do motivo.
- Ajustes afetados: responsavel; frequencia; quando abrir tarefa
- Encadeamento: /app/relatorios/financeiro; tarefa financeira

**Autonomo com excecoes** (habilitado)

- Inicio: O fluxo comeca quando surge um caso para preparar fechamento mensal financeiro. A Taliya identifica o caso e valida os dados principais: periodo de fechamento esta definido; movimentacoes foram consolidadas; pendencias foram separadas.
- Meio: A Taliya executa sozinha quando periodo de fechamento esta definido; movimentacoes foram consolidadas; pendencias foram separadas; responsavel financeiro esta definido; frequencia do resumo esta configurada. Ela chama a equipe quando ha divergencia de conciliacao; movimentacao sem dono; provedor financeiro falhou; pendencia critica apareceu; permissao ou cota bloqueia analise.
- Fim: No caso comum, a acao `preparar fechamento mensal financeiro` fica registrada e auditada. Se houver excecao, criar tarefa/caso em /app/relatorios/financeiro; tarefa financeira e manter auditoria do motivo.
- Ajustes afetados: responsavel; frequencia; quando abrir tarefa
- Encadeamento: /app/relatorios/financeiro; tarefa financeira

**Autonomo** (bloqueado)

- Inicio: Este modo fica bloqueado para Fechamento mensal.
- Meio: A Taliya nao conclui end-to-end porque este modo esta acima do teto do fluxo.
- Fim: Use o maior modo habilitado para automatizar o caso comum sem ultrapassar os limites publicados.
- Ajustes afetados: responsavel; frequencia; quando abrir tarefa
- Encadeamento: /app/relatorios/financeiro; tarefa financeira


### Rotina: Ciclo do plano do aluno


#### Encerramento ou alteracao efetiva de plano

**Manual** (habilitado)

- Inicio: O fluxo comeca quando surge um caso para preparar encerramento ou alteracao efetiva de plano. A Taliya identifica o caso e organiza o contexto principal: plano atual foi identificado; mudanca solicitada foi descrita; impacto em agenda, cobranca e contrato foi calculado.
- Meio: A Taliya cria tarefa, checklist ou caso para a equipe preparar encerramento ou alteracao efetiva de plano. A decisao e a execucao principal ficam com o humano.
- Fim: O fluxo termina quando a equipe registra o resultado. A Taliya salva auditoria e, se nao puder seguir, criar tarefa/caso em /app/financeiro; /app/alunos/[id]; aprovacao/caso e manter auditoria do motivo.
- Ajustes afetados: aprovador; checklist; template de comunicacao
- Encadeamento: /app/financeiro; /app/alunos/[id]; aprovacao/caso

**Copiloto** (habilitado)

- Inicio: O fluxo comeca quando surge um caso para preparar encerramento ou alteracao efetiva de plano. A Taliya identifica o contexto e mostra a base da sugestao: plano atual foi identificado; mudanca solicitada foi descrita; impacto em agenda, cobranca e contrato foi calculado.
- Meio: A Taliya sugere preparar encerramento ou alteracao efetiva de plano, prepara texto/resumo/proximo passo e mostra os dados usados. A equipe pode aceitar, editar ou descartar antes de executar.
- Fim: Se a equipe aceitar, a acao e registrada conforme a decisao humana. Se editar ou descartar, a Taliya registra a decisao e mantem continuidade em /app/financeiro; /app/alunos/[id]; aprovacao/caso.
- Ajustes afetados: aprovador; checklist; template de comunicacao
- Encadeamento: /app/financeiro; /app/alunos/[id]; aprovacao/caso

**Autonomo com aprovacao** (habilitado)

- Inicio: O fluxo comeca quando surge um caso para preparar encerramento ou alteracao efetiva de plano. A Taliya identifica o caso, confere plano atual foi identificado; mudanca solicitada foi descrita; impacto em agenda, cobranca e contrato foi calculado e prepara a revisao.
- Meio: A Taliya valida plano atual foi identificado; mudanca solicitada foi descrita; impacto em agenda, cobranca e contrato foi calculado; checklist esta completo e prepara preparar encerramento ou alteracao efetiva de plano. Antes de concluir, mostra impacto/preview e pede aprovacao.
- Fim: Se aprovado, a acao e concluida e auditada. Se recusado, vencido ou incompleto, criar tarefa/caso em /app/financeiro; /app/alunos/[id]; aprovacao/caso e manter auditoria do motivo.
- Ajustes afetados: aprovador; checklist; template de comunicacao
- Encadeamento: /app/financeiro; /app/alunos/[id]; aprovacao/caso

**Autonomo com excecoes** (bloqueado)

- Inicio: Este modo fica bloqueado para Encerramento ou alteracao efetiva de plano.
- Meio: A Taliya nao executa com excecoes porque o teto deste fluxo e menor.
- Fim: O usuario deve escolher um modo permitido para este fluxo.
- Ajustes afetados: aprovador; checklist; template de comunicacao
- Encadeamento: /app/financeiro; /app/alunos/[id]; aprovacao/caso

**Autonomo** (bloqueado)

- Inicio: Este modo fica bloqueado para Encerramento ou alteracao efetiva de plano.
- Meio: A Taliya nao conclui end-to-end porque este modo esta acima do teto do fluxo.
- Fim: Use o maior modo habilitado para automatizar o caso comum sem ultrapassar os limites publicados.
- Ajustes afetados: aprovador; checklist; template de comunicacao
- Encadeamento: /app/financeiro; /app/alunos/[id]; aprovacao/caso


## Agente: Retencao


### Rotina: Retencao preventiva


#### Queda frequencia

**Manual** (habilitado)

- Inicio: O fluxo comeca quando surge um caso para detectar queda de frequencia e iniciar prevencao. A Taliya identifica o caso e organiza o contexto principal: frequencia caiu conforme regra publicada; aluno esta ativo; responsavel esta definido.
- Meio: A Taliya cria tarefa, checklist ou caso para a equipe detectar queda de frequencia e iniciar prevencao. A decisao e a execucao principal ficam com o humano.
- Fim: O fluxo termina quando a equipe registra o resultado. A Taliya salva auditoria e, se nao puder seguir, criar tarefa/caso em /app/retencao/riscos; /app/alunos/[id]; tarefa e manter auditoria do motivo.
- Ajustes afetados: regra de queda; responsavel; cadencia
- Encadeamento: /app/retencao/riscos; /app/alunos/[id]; tarefa

**Copiloto** (habilitado)

- Inicio: O fluxo comeca quando surge um caso para detectar queda de frequencia e iniciar prevencao. A Taliya identifica o contexto e mostra a base da sugestao: frequencia caiu conforme regra publicada; aluno esta ativo; responsavel esta definido.
- Meio: A Taliya sugere detectar queda de frequencia e iniciar prevencao, prepara texto/resumo/proximo passo e mostra os dados usados. A equipe pode aceitar, editar ou descartar antes de executar.
- Fim: Se a equipe aceitar, a acao e registrada conforme a decisao humana. Se editar ou descartar, a Taliya registra a decisao e mantem continuidade em /app/retencao/riscos; /app/alunos/[id]; tarefa.
- Ajustes afetados: regra de queda; responsavel; cadencia
- Encadeamento: /app/retencao/riscos; /app/alunos/[id]; tarefa

**Autonomo com aprovacao** (habilitado)

- Inicio: O fluxo comeca quando surge um caso para detectar queda de frequencia e iniciar prevencao. A Taliya identifica o caso, confere frequencia caiu conforme regra publicada; aluno esta ativo; responsavel esta definido e prepara a revisao.
- Meio: A Taliya valida frequencia caiu conforme regra publicada; aluno esta ativo; responsavel esta definido; cadencia permite contato e prepara detectar queda de frequencia e iniciar prevencao. Antes de concluir, mostra impacto/preview e pede aprovacao.
- Fim: Se aprovado, a acao e concluida e auditada. Se recusado, vencido ou incompleto, criar tarefa/caso em /app/retencao/riscos; /app/alunos/[id]; tarefa e manter auditoria do motivo.
- Ajustes afetados: regra de queda; responsavel; cadencia
- Encadeamento: /app/retencao/riscos; /app/alunos/[id]; tarefa

**Autonomo com excecoes** (habilitado)

- Inicio: O fluxo comeca quando surge um caso para detectar queda de frequencia e iniciar prevencao. A Taliya identifica o caso e valida os dados principais: frequencia caiu conforme regra publicada; aluno esta ativo; responsavel esta definido.
- Meio: A Taliya executa sozinha quando frequencia caiu conforme regra publicada; aluno esta ativo; responsavel esta definido; cadencia permite contato; nao ha caso sensivel aberto. Ela chama a equipe quando queda tem motivo ja registrado; aluno tem reclamacao ou saude/evento pessoal; risco de cancelamento aumentou; cadencia foi excedida; canal, cota ou permissao bloqueia contato.
- Fim: No caso comum, a acao `detectar queda de frequencia e iniciar prevencao` fica registrada e auditada. Se houver excecao, criar tarefa/caso em /app/retencao/riscos; /app/alunos/[id]; tarefa e manter auditoria do motivo.
- Ajustes afetados: regra de queda; responsavel; cadencia
- Encadeamento: /app/retencao/riscos; /app/alunos/[id]; tarefa

**Autonomo** (bloqueado)

- Inicio: Este modo fica bloqueado para Queda frequencia.
- Meio: A Taliya nao conclui end-to-end porque este modo esta acima do teto do fluxo.
- Fim: Use o maior modo habilitado para automatizar o caso comum sem ultrapassar os limites publicados.
- Ajustes afetados: regra de queda; responsavel; cadencia
- Encadeamento: /app/retencao/riscos; /app/alunos/[id]; tarefa


#### Aluno inativo

**Manual** (habilitado)

- Inicio: O fluxo comeca quando surge um caso para identificar aluno inativo e preparar retomada. A Taliya identifica o caso e organiza o contexto principal: dias de inatividade atingiram o limite; aluno esta elegivel para contato; responsavel esta definido.
- Meio: A Taliya cria tarefa, checklist ou caso para a equipe identificar aluno inativo e preparar retomada. A decisao e a execucao principal ficam com o humano.
- Fim: O fluxo termina quando a equipe registra o resultado. A Taliya salva auditoria e, se nao puder seguir, criar tarefa/caso em /app/retencao/riscos; tarefa/aprovacao e manter auditoria do motivo.
- Ajustes afetados: dias de inatividade; responsavel; limite de contato
- Encadeamento: /app/retencao/riscos; tarefa/aprovacao

**Copiloto** (habilitado)

- Inicio: O fluxo comeca quando surge um caso para identificar aluno inativo e preparar retomada. A Taliya identifica o contexto e mostra a base da sugestao: dias de inatividade atingiram o limite; aluno esta elegivel para contato; responsavel esta definido.
- Meio: A Taliya sugere identificar aluno inativo e preparar retomada, prepara texto/resumo/proximo passo e mostra os dados usados. A equipe pode aceitar, editar ou descartar antes de executar.
- Fim: Se a equipe aceitar, a acao e registrada conforme a decisao humana. Se editar ou descartar, a Taliya registra a decisao e mantem continuidade em /app/retencao/riscos; tarefa/aprovacao.
- Ajustes afetados: dias de inatividade; responsavel; limite de contato
- Encadeamento: /app/retencao/riscos; tarefa/aprovacao

**Autonomo com aprovacao** (habilitado)

- Inicio: O fluxo comeca quando surge um caso para identificar aluno inativo e preparar retomada. A Taliya identifica o caso, confere dias de inatividade atingiram o limite; aluno esta elegivel para contato; responsavel esta definido e prepara a revisao.
- Meio: A Taliya valida dias de inatividade atingiram o limite; aluno esta elegivel para contato; responsavel esta definido; limite de contato nao foi atingido e prepara identificar aluno inativo e preparar retomada. Antes de concluir, mostra impacto/preview e pede aprovacao.
- Fim: Se aprovado, a acao e concluida e auditada. Se recusado, vencido ou incompleto, criar tarefa/caso em /app/retencao/riscos; tarefa/aprovacao e manter auditoria do motivo.
- Ajustes afetados: dias de inatividade; responsavel; limite de contato
- Encadeamento: /app/retencao/riscos; tarefa/aprovacao

**Autonomo com excecoes** (habilitado)

- Inicio: O fluxo comeca quando surge um caso para identificar aluno inativo e preparar retomada. A Taliya identifica o caso e valida os dados principais: dias de inatividade atingiram o limite; aluno esta elegivel para contato; responsavel esta definido.
- Meio: A Taliya executa sozinha quando dias de inatividade atingiram o limite; aluno esta elegivel para contato; responsavel esta definido; limite de contato nao foi atingido; mensagem aprovada esta disponivel. Ela chama a equipe quando aluno pausou ou trancou; aluno pediu opt-out; ha pendencia financeira ou reclamacao; historico indica caso sensivel; canal, cota ou permissao bloqueia contato.
- Fim: No caso comum, a acao `identificar aluno inativo e preparar retomada` fica registrada e auditada. Se houver excecao, criar tarefa/caso em /app/retencao/riscos; tarefa/aprovacao e manter auditoria do motivo.
- Ajustes afetados: dias de inatividade; responsavel; limite de contato
- Encadeamento: /app/retencao/riscos; tarefa/aprovacao

**Autonomo** (bloqueado)

- Inicio: Este modo fica bloqueado para Aluno inativo.
- Meio: A Taliya nao conclui end-to-end porque este modo esta acima do teto do fluxo.
- Fim: Use o maior modo habilitado para automatizar o caso comum sem ultrapassar os limites publicados.
- Ajustes afetados: dias de inatividade; responsavel; limite de contato
- Encadeamento: /app/retencao/riscos; tarefa/aprovacao


#### Retorno

**Manual** (habilitado)

- Inicio: O fluxo comeca quando surge um caso para organizar retorno de aluno. A Taliya identifica o caso e organiza o contexto principal: aluno demonstrou interesse em voltar; regra de agenda permite encaixe; responsavel esta definido.
- Meio: A Taliya cria tarefa, checklist ou caso para a equipe organizar retorno de aluno. A decisao e a execucao principal ficam com o humano.
- Fim: O fluxo termina quando a equipe registra o resultado. A Taliya salva auditoria e, se nao puder seguir, criar tarefa/caso em /app/retencao; /app/agenda; tarefa e manter auditoria do motivo.
- Ajustes afetados: responsavel; tipo de retorno; quando chamar Agenda
- Encadeamento: /app/retencao; /app/agenda; tarefa

**Copiloto** (habilitado)

- Inicio: O fluxo comeca quando surge um caso para organizar retorno de aluno. A Taliya identifica o contexto e mostra a base da sugestao: aluno demonstrou interesse em voltar; regra de agenda permite encaixe; responsavel esta definido.
- Meio: A Taliya sugere organizar retorno de aluno, prepara texto/resumo/proximo passo e mostra os dados usados. A equipe pode aceitar, editar ou descartar antes de executar.
- Fim: Se a equipe aceitar, a acao e registrada conforme a decisao humana. Se editar ou descartar, a Taliya registra a decisao e mantem continuidade em /app/retencao; /app/agenda; tarefa.
- Ajustes afetados: responsavel; tipo de retorno; quando chamar Agenda
- Encadeamento: /app/retencao; /app/agenda; tarefa

**Autonomo com aprovacao** (habilitado)

- Inicio: O fluxo comeca quando surge um caso para organizar retorno de aluno. A Taliya identifica o caso, confere aluno demonstrou interesse em voltar; regra de agenda permite encaixe; responsavel esta definido e prepara a revisao.
- Meio: A Taliya valida aluno demonstrou interesse em voltar; regra de agenda permite encaixe; responsavel esta definido; opcoes de horario existem e prepara organizar retorno de aluno. Antes de concluir, mostra impacto/preview e pede aprovacao.
- Fim: Se aprovado, a acao e concluida e auditada. Se recusado, vencido ou incompleto, criar tarefa/caso em /app/retencao; /app/agenda; tarefa e manter auditoria do motivo.
- Ajustes afetados: responsavel; tipo de retorno; quando chamar Agenda
- Encadeamento: /app/retencao; /app/agenda; tarefa

**Autonomo com excecoes** (habilitado)

- Inicio: O fluxo comeca quando surge um caso para organizar retorno de aluno. A Taliya identifica o caso e valida os dados principais: aluno demonstrou interesse em voltar; regra de agenda permite encaixe; responsavel esta definido.
- Meio: A Taliya executa sozinha quando aluno demonstrou interesse em voltar; regra de agenda permite encaixe; responsavel esta definido; opcoes de horario existem; mensagem aprovada esta disponivel. Ela chama a equipe quando nao ha horario compativel; aluno tem pendencia financeira; retorno exige avaliacao ou cuidado; aluno pede condicao especial; canal, cota ou permissao bloqueia contato.
- Fim: No caso comum, a acao `organizar retorno de aluno` fica registrada e auditada. Se houver excecao, criar tarefa/caso em /app/retencao; /app/agenda; tarefa e manter auditoria do motivo.
- Ajustes afetados: responsavel; tipo de retorno; quando chamar Agenda
- Encadeamento: /app/retencao; /app/agenda; tarefa

**Autonomo** (bloqueado)

- Inicio: Este modo fica bloqueado para Retorno.
- Meio: A Taliya nao conclui end-to-end porque este modo esta acima do teto do fluxo.
- Fim: Use o maior modo habilitado para automatizar o caso comum sem ultrapassar os limites publicados.
- Ajustes afetados: responsavel; tipo de retorno; quando chamar Agenda
- Encadeamento: /app/retencao; /app/agenda; tarefa


### Rotina: Casos sensiveis


#### Risco cancelamento

**Manual** (habilitado)

- Inicio: O fluxo comeca quando surge um caso para preparar caso de risco de cancelamento para aprovacao. A Taliya identifica o caso e organiza o contexto principal: sinal de cancelamento foi detectado; dono do caso esta definido; automacoes conflitantes foram pausadas.
- Meio: A Taliya cria tarefa, checklist ou caso para a equipe preparar caso de risco de cancelamento para aprovacao. A decisao e a execucao principal ficam com o humano.
- Fim: O fluxo termina quando a equipe registra o resultado. A Taliya salva auditoria e, se nao puder seguir, criar tarefa/caso em /app/cancelamentos; /app/operacao; aprovacao/caso e manter auditoria do motivo.
- Ajustes afetados: dono do caso; aprovador; pausa de automacoes
- Encadeamento: /app/cancelamentos; /app/operacao; aprovacao/caso

**Copiloto** (habilitado)

- Inicio: O fluxo comeca quando surge um caso para preparar caso de risco de cancelamento para aprovacao. A Taliya identifica o contexto e mostra a base da sugestao: sinal de cancelamento foi detectado; dono do caso esta definido; automacoes conflitantes foram pausadas.
- Meio: A Taliya sugere preparar caso de risco de cancelamento para aprovacao, prepara texto/resumo/proximo passo e mostra os dados usados. A equipe pode aceitar, editar ou descartar antes de executar.
- Fim: Se a equipe aceitar, a acao e registrada conforme a decisao humana. Se editar ou descartar, a Taliya registra a decisao e mantem continuidade em /app/cancelamentos; /app/operacao; aprovacao/caso.
- Ajustes afetados: dono do caso; aprovador; pausa de automacoes
- Encadeamento: /app/cancelamentos; /app/operacao; aprovacao/caso

**Autonomo com aprovacao** (habilitado)

- Inicio: O fluxo comeca quando surge um caso para preparar caso de risco de cancelamento para aprovacao. A Taliya identifica o caso, confere sinal de cancelamento foi detectado; dono do caso esta definido; automacoes conflitantes foram pausadas e prepara a revisao.
- Meio: A Taliya valida sinal de cancelamento foi detectado; dono do caso esta definido; automacoes conflitantes foram pausadas; contexto foi resumido e prepara preparar caso de risco de cancelamento para aprovacao. Antes de concluir, mostra impacto/preview e pede aprovacao.
- Fim: Se aprovado, a acao e concluida e auditada. Se recusado, vencido ou incompleto, criar tarefa/caso em /app/cancelamentos; /app/operacao; aprovacao/caso e manter auditoria do motivo.
- Ajustes afetados: dono do caso; aprovador; pausa de automacoes
- Encadeamento: /app/cancelamentos; /app/operacao; aprovacao/caso

**Autonomo com excecoes** (bloqueado)

- Inicio: Este modo fica bloqueado para Risco cancelamento.
- Meio: A Taliya nao executa com excecoes porque o teto deste fluxo e menor.
- Fim: O usuario deve escolher um modo permitido para este fluxo.
- Ajustes afetados: dono do caso; aprovador; pausa de automacoes
- Encadeamento: /app/cancelamentos; /app/operacao; aprovacao/caso

**Autonomo** (bloqueado)

- Inicio: Este modo fica bloqueado para Risco cancelamento.
- Meio: A Taliya nao conclui end-to-end porque este modo esta acima do teto do fluxo.
- Fim: Use o maior modo habilitado para automatizar o caso comum sem ultrapassar os limites publicados.
- Ajustes afetados: dono do caso; aprovador; pausa de automacoes
- Encadeamento: /app/cancelamentos; /app/operacao; aprovacao/caso


#### Reativacao ex-aluno

**Manual** (habilitado)

- Inicio: O fluxo comeca quando surge um caso para preparar reativacao de ex-aluno para aprovacao. A Taliya identifica o caso e organiza o contexto principal: ex-aluno esta no segmento permitido; cadencia permite contato; mensagem esta aprovada.
- Meio: A Taliya cria tarefa, checklist ou caso para a equipe preparar reativacao de ex-aluno para aprovacao. A decisao e a execucao principal ficam com o humano.
- Fim: O fluxo termina quando a equipe registra o resultado. A Taliya salva auditoria e, se nao puder seguir, criar tarefa/caso em /app/retencao/reativacoes; /app/aprovacoes e manter auditoria do motivo.
- Ajustes afetados: aprovador; segmento permitido; cadencia
- Encadeamento: /app/retencao/reativacoes; /app/aprovacoes

**Copiloto** (habilitado)

- Inicio: O fluxo comeca quando surge um caso para preparar reativacao de ex-aluno para aprovacao. A Taliya identifica o contexto e mostra a base da sugestao: ex-aluno esta no segmento permitido; cadencia permite contato; mensagem esta aprovada.
- Meio: A Taliya sugere preparar reativacao de ex-aluno para aprovacao, prepara texto/resumo/proximo passo e mostra os dados usados. A equipe pode aceitar, editar ou descartar antes de executar.
- Fim: Se a equipe aceitar, a acao e registrada conforme a decisao humana. Se editar ou descartar, a Taliya registra a decisao e mantem continuidade em /app/retencao/reativacoes; /app/aprovacoes.
- Ajustes afetados: aprovador; segmento permitido; cadencia
- Encadeamento: /app/retencao/reativacoes; /app/aprovacoes

**Autonomo com aprovacao** (habilitado)

- Inicio: O fluxo comeca quando surge um caso para preparar reativacao de ex-aluno para aprovacao. A Taliya identifica o caso, confere ex-aluno esta no segmento permitido; cadencia permite contato; mensagem esta aprovada e prepara a revisao.
- Meio: A Taliya valida ex-aluno esta no segmento permitido; cadencia permite contato; mensagem esta aprovada; responsavel esta definido e prepara preparar reativacao de ex-aluno para aprovacao. Antes de concluir, mostra impacto/preview e pede aprovacao.
- Fim: Se aprovado, a acao e concluida e auditada. Se recusado, vencido ou incompleto, criar tarefa/caso em /app/retencao/reativacoes; /app/aprovacoes e manter auditoria do motivo.
- Ajustes afetados: aprovador; segmento permitido; cadencia
- Encadeamento: /app/retencao/reativacoes; /app/aprovacoes

**Autonomo com excecoes** (bloqueado)

- Inicio: Este modo fica bloqueado para Reativacao ex-aluno.
- Meio: A Taliya nao executa com excecoes porque o teto deste fluxo e menor.
- Fim: O usuario deve escolher um modo permitido para este fluxo.
- Ajustes afetados: aprovador; segmento permitido; cadencia
- Encadeamento: /app/retencao/reativacoes; /app/aprovacoes

**Autonomo** (bloqueado)

- Inicio: Este modo fica bloqueado para Reativacao ex-aluno.
- Meio: A Taliya nao conclui end-to-end porque este modo esta acima do teto do fluxo.
- Fim: Use o maior modo habilitado para automatizar o caso comum sem ultrapassar os limites publicados.
- Ajustes afetados: aprovador; segmento permitido; cadencia
- Encadeamento: /app/retencao/reativacoes; /app/aprovacoes


### Rotina: Retencao preventiva


#### Satisfacao

**Manual** (habilitado)

- Inicio: O fluxo comeca quando surge um caso para acompanhar satisfacao e abrir cuidado quando necessario. A Taliya identifica o caso e organiza o contexto principal: janela de satisfacao chegou; aluno esta elegivel; responsavel esta definido.
- Meio: A Taliya cria tarefa, checklist ou caso para a equipe acompanhar satisfacao e abrir cuidado quando necessario. A decisao e a execucao principal ficam com o humano.
- Fim: O fluxo termina quando a equipe registra o resultado. A Taliya salva auditoria e, se nao puder seguir, criar tarefa/caso em /app/retencao; /app/reclamacoes; tarefa e manter auditoria do motivo.
- Ajustes afetados: janela; responsavel; quando abrir reclamacao
- Encadeamento: /app/retencao; /app/reclamacoes; tarefa

**Copiloto** (habilitado)

- Inicio: O fluxo comeca quando surge um caso para acompanhar satisfacao e abrir cuidado quando necessario. A Taliya identifica o contexto e mostra a base da sugestao: janela de satisfacao chegou; aluno esta elegivel; responsavel esta definido.
- Meio: A Taliya sugere acompanhar satisfacao e abrir cuidado quando necessario, prepara texto/resumo/proximo passo e mostra os dados usados. A equipe pode aceitar, editar ou descartar antes de executar.
- Fim: Se a equipe aceitar, a acao e registrada conforme a decisao humana. Se editar ou descartar, a Taliya registra a decisao e mantem continuidade em /app/retencao; /app/reclamacoes; tarefa.
- Ajustes afetados: janela; responsavel; quando abrir reclamacao
- Encadeamento: /app/retencao; /app/reclamacoes; tarefa

**Autonomo com aprovacao** (habilitado)

- Inicio: O fluxo comeca quando surge um caso para acompanhar satisfacao e abrir cuidado quando necessario. A Taliya identifica o caso, confere janela de satisfacao chegou; aluno esta elegivel; responsavel esta definido e prepara a revisao.
- Meio: A Taliya valida janela de satisfacao chegou; aluno esta elegivel; responsavel esta definido; mensagem aprovada esta disponivel e prepara acompanhar satisfacao e abrir cuidado quando necessario. Antes de concluir, mostra impacto/preview e pede aprovacao.
- Fim: Se aprovado, a acao e concluida e auditada. Se recusado, vencido ou incompleto, criar tarefa/caso em /app/retencao; /app/reclamacoes; tarefa e manter auditoria do motivo.
- Ajustes afetados: janela; responsavel; quando abrir reclamacao
- Encadeamento: /app/retencao; /app/reclamacoes; tarefa

**Autonomo com excecoes** (habilitado)

- Inicio: O fluxo comeca quando surge um caso para acompanhar satisfacao e abrir cuidado quando necessario. A Taliya identifica o caso e valida os dados principais: janela de satisfacao chegou; aluno esta elegivel; responsavel esta definido.
- Meio: A Taliya executa sozinha quando janela de satisfacao chegou; aluno esta elegivel; responsavel esta definido; mensagem aprovada esta disponivel; nao ha reclamacao aberta. Ela chama a equipe quando resposta indica reclamacao; nota baixa ou texto sensivel; aluno menciona saude, professor ou cobranca; ja existe caso aberto; canal, cota ou permissao bloqueia contato.
- Fim: No caso comum, a acao `acompanhar satisfacao e abrir cuidado quando necessario` fica registrada e auditada. Se houver excecao, criar tarefa/caso em /app/retencao; /app/reclamacoes; tarefa e manter auditoria do motivo.
- Ajustes afetados: janela; responsavel; quando abrir reclamacao
- Encadeamento: /app/retencao; /app/reclamacoes; tarefa

**Autonomo** (bloqueado)

- Inicio: Este modo fica bloqueado para Satisfacao.
- Meio: A Taliya nao conclui end-to-end porque este modo esta acima do teto do fluxo.
- Fim: Use o maior modo habilitado para automatizar o caso comum sem ultrapassar os limites publicados.
- Ajustes afetados: janela; responsavel; quando abrir reclamacao
- Encadeamento: /app/retencao; /app/reclamacoes; tarefa


#### Retorno apos pausa

**Manual** (habilitado)

- Inicio: O fluxo comeca quando surge um caso para preparar retorno apos pausa. A Taliya identifica o caso e organiza o contexto principal: fim da pausa esta proximo; aluno esta elegivel para retorno; opcoes de agenda existem.
- Meio: A Taliya cria tarefa, checklist ou caso para a equipe preparar retorno apos pausa. A decisao e a execucao principal ficam com o humano.
- Fim: O fluxo termina quando a equipe registra o resultado. A Taliya salva auditoria e, se nao puder seguir, criar tarefa/caso em /app/retencao; /app/agenda; tarefa e manter auditoria do motivo.
- Ajustes afetados: antecedencia; responsavel; quando chamar Agenda
- Encadeamento: /app/retencao; /app/agenda; tarefa

**Copiloto** (habilitado)

- Inicio: O fluxo comeca quando surge um caso para preparar retorno apos pausa. A Taliya identifica o contexto e mostra a base da sugestao: fim da pausa esta proximo; aluno esta elegivel para retorno; opcoes de agenda existem.
- Meio: A Taliya sugere preparar retorno apos pausa, prepara texto/resumo/proximo passo e mostra os dados usados. A equipe pode aceitar, editar ou descartar antes de executar.
- Fim: Se a equipe aceitar, a acao e registrada conforme a decisao humana. Se editar ou descartar, a Taliya registra a decisao e mantem continuidade em /app/retencao; /app/agenda; tarefa.
- Ajustes afetados: antecedencia; responsavel; quando chamar Agenda
- Encadeamento: /app/retencao; /app/agenda; tarefa

**Autonomo com aprovacao** (habilitado)

- Inicio: O fluxo comeca quando surge um caso para preparar retorno apos pausa. A Taliya identifica o caso, confere fim da pausa esta proximo; aluno esta elegivel para retorno; opcoes de agenda existem e prepara a revisao.
- Meio: A Taliya valida fim da pausa esta proximo; aluno esta elegivel para retorno; opcoes de agenda existem; responsavel esta definido e prepara preparar retorno apos pausa. Antes de concluir, mostra impacto/preview e pede aprovacao.
- Fim: Se aprovado, a acao e concluida e auditada. Se recusado, vencido ou incompleto, criar tarefa/caso em /app/retencao; /app/agenda; tarefa e manter auditoria do motivo.
- Ajustes afetados: antecedencia; responsavel; quando chamar Agenda
- Encadeamento: /app/retencao; /app/agenda; tarefa

**Autonomo com excecoes** (habilitado)

- Inicio: O fluxo comeca quando surge um caso para preparar retorno apos pausa. A Taliya identifica o caso e valida os dados principais: fim da pausa esta proximo; aluno esta elegivel para retorno; opcoes de agenda existem.
- Meio: A Taliya executa sozinha quando fim da pausa esta proximo; aluno esta elegivel para retorno; opcoes de agenda existem; responsavel esta definido; antecedencia configurada chegou. Ela chama a equipe quando aluno pede estender pausa; agenda nao tem vaga; ha pendencia financeira; retorno exige cuidado ou professor especifico; canal, cota ou permissao bloqueia contato.
- Fim: No caso comum, a acao `preparar retorno apos pausa` fica registrada e auditada. Se houver excecao, criar tarefa/caso em /app/retencao; /app/agenda; tarefa e manter auditoria do motivo.
- Ajustes afetados: antecedencia; responsavel; quando chamar Agenda
- Encadeamento: /app/retencao; /app/agenda; tarefa

**Autonomo** (bloqueado)

- Inicio: Este modo fica bloqueado para Retorno apos pausa.
- Meio: A Taliya nao conclui end-to-end porque este modo esta acima do teto do fluxo.
- Fim: Use o maior modo habilitado para automatizar o caso comum sem ultrapassar os limites publicados.
- Ajustes afetados: antecedencia; responsavel; quando chamar Agenda
- Encadeamento: /app/retencao; /app/agenda; tarefa


### Rotina: Casos sensiveis


#### Risco por perfil

**Manual** (habilitado)

- Inicio: O fluxo comeca quando surge um caso para preparar acao de risco por perfil para aprovacao. A Taliya identifica o caso e organiza o contexto principal: segmento de risco foi identificado; uso do segmento esta permitido; acao proposta foi definida.
- Meio: A Taliya cria tarefa, checklist ou caso para a equipe preparar acao de risco por perfil para aprovacao. A decisao e a execucao principal ficam com o humano.
- Fim: O fluxo termina quando a equipe registra o resultado. A Taliya salva auditoria e, se nao puder seguir, criar tarefa/caso em /app/retencao/riscos; aprovacao/tarefa e manter auditoria do motivo.
- Ajustes afetados: aprovador; uso do segmento; responsavel
- Encadeamento: /app/retencao/riscos; aprovacao/tarefa

**Copiloto** (habilitado)

- Inicio: O fluxo comeca quando surge um caso para preparar acao de risco por perfil para aprovacao. A Taliya identifica o contexto e mostra a base da sugestao: segmento de risco foi identificado; uso do segmento esta permitido; acao proposta foi definida.
- Meio: A Taliya sugere preparar acao de risco por perfil para aprovacao, prepara texto/resumo/proximo passo e mostra os dados usados. A equipe pode aceitar, editar ou descartar antes de executar.
- Fim: Se a equipe aceitar, a acao e registrada conforme a decisao humana. Se editar ou descartar, a Taliya registra a decisao e mantem continuidade em /app/retencao/riscos; aprovacao/tarefa.
- Ajustes afetados: aprovador; uso do segmento; responsavel
- Encadeamento: /app/retencao/riscos; aprovacao/tarefa

**Autonomo com aprovacao** (habilitado)

- Inicio: O fluxo comeca quando surge um caso para preparar acao de risco por perfil para aprovacao. A Taliya identifica o caso, confere segmento de risco foi identificado; uso do segmento esta permitido; acao proposta foi definida e prepara a revisao.
- Meio: A Taliya valida segmento de risco foi identificado; uso do segmento esta permitido; acao proposta foi definida; responsavel esta definido e prepara preparar acao de risco por perfil para aprovacao. Antes de concluir, mostra impacto/preview e pede aprovacao.
- Fim: Se aprovado, a acao e concluida e auditada. Se recusado, vencido ou incompleto, criar tarefa/caso em /app/retencao/riscos; aprovacao/tarefa e manter auditoria do motivo.
- Ajustes afetados: aprovador; uso do segmento; responsavel
- Encadeamento: /app/retencao/riscos; aprovacao/tarefa

**Autonomo com excecoes** (bloqueado)

- Inicio: Este modo fica bloqueado para Risco por perfil.
- Meio: A Taliya nao executa com excecoes porque o teto deste fluxo e menor.
- Fim: O usuario deve escolher um modo permitido para este fluxo.
- Ajustes afetados: aprovador; uso do segmento; responsavel
- Encadeamento: /app/retencao/riscos; aprovacao/tarefa

**Autonomo** (bloqueado)

- Inicio: Este modo fica bloqueado para Risco por perfil.
- Meio: A Taliya nao conclui end-to-end porque este modo esta acima do teto do fluxo.
- Fim: Use o maior modo habilitado para automatizar o caso comum sem ultrapassar os limites publicados.
- Ajustes afetados: aprovador; uso do segmento; responsavel
- Encadeamento: /app/retencao/riscos; aprovacao/tarefa


#### Pos-cancelamento

**Manual** (habilitado)

- Inicio: O fluxo comeca quando surge um caso para preparar pos-cancelamento para aprovacao. A Taliya identifica o caso e organiza o contexto principal: cancelamento foi registrado; janela de contato esta definida; responsavel esta atribuido.
- Meio: A Taliya cria tarefa, checklist ou caso para a equipe preparar pos-cancelamento para aprovacao. A decisao e a execucao principal ficam com o humano.
- Fim: O fluxo termina quando a equipe registra o resultado. A Taliya salva auditoria e, se nao puder seguir, criar tarefa/caso em /app/cancelamentos; /app/aprovacoes; tarefa e manter auditoria do motivo.
- Ajustes afetados: aprovador; quando contatar; responsavel
- Encadeamento: /app/cancelamentos; /app/aprovacoes; tarefa

**Copiloto** (habilitado)

- Inicio: O fluxo comeca quando surge um caso para preparar pos-cancelamento para aprovacao. A Taliya identifica o contexto e mostra a base da sugestao: cancelamento foi registrado; janela de contato esta definida; responsavel esta atribuido.
- Meio: A Taliya sugere preparar pos-cancelamento para aprovacao, prepara texto/resumo/proximo passo e mostra os dados usados. A equipe pode aceitar, editar ou descartar antes de executar.
- Fim: Se a equipe aceitar, a acao e registrada conforme a decisao humana. Se editar ou descartar, a Taliya registra a decisao e mantem continuidade em /app/cancelamentos; /app/aprovacoes; tarefa.
- Ajustes afetados: aprovador; quando contatar; responsavel
- Encadeamento: /app/cancelamentos; /app/aprovacoes; tarefa

**Autonomo com aprovacao** (habilitado)

- Inicio: O fluxo comeca quando surge um caso para preparar pos-cancelamento para aprovacao. A Taliya identifica o caso, confere cancelamento foi registrado; janela de contato esta definida; responsavel esta atribuido e prepara a revisao.
- Meio: A Taliya valida cancelamento foi registrado; janela de contato esta definida; responsavel esta atribuido; mensagem nao reabre conflito e prepara preparar pos-cancelamento para aprovacao. Antes de concluir, mostra impacto/preview e pede aprovacao.
- Fim: Se aprovado, a acao e concluida e auditada. Se recusado, vencido ou incompleto, criar tarefa/caso em /app/cancelamentos; /app/aprovacoes; tarefa e manter auditoria do motivo.
- Ajustes afetados: aprovador; quando contatar; responsavel
- Encadeamento: /app/cancelamentos; /app/aprovacoes; tarefa

**Autonomo com excecoes** (bloqueado)

- Inicio: Este modo fica bloqueado para Pos-cancelamento.
- Meio: A Taliya nao executa com excecoes porque o teto deste fluxo e menor.
- Fim: O usuario deve escolher um modo permitido para este fluxo.
- Ajustes afetados: aprovador; quando contatar; responsavel
- Encadeamento: /app/cancelamentos; /app/aprovacoes; tarefa

**Autonomo** (bloqueado)

- Inicio: Este modo fica bloqueado para Pos-cancelamento.
- Meio: A Taliya nao conclui end-to-end porque este modo esta acima do teto do fluxo.
- Fim: Use o maior modo habilitado para automatizar o caso comum sem ultrapassar os limites publicados.
- Ajustes afetados: aprovador; quando contatar; responsavel
- Encadeamento: /app/cancelamentos; /app/aprovacoes; tarefa


### Rotina: Retencao preventiva


#### Marco engajamento

**Manual** (habilitado)

- Inicio: O fluxo comeca quando surge um caso para reconhecer marco de engajamento e acionar contato leve. A Taliya identifica o caso e organiza o contexto principal: marco configurado aconteceu; aluno esta ativo; tipo de marco esta permitido.
- Meio: A Taliya cria tarefa, checklist ou caso para a equipe reconhecer marco de engajamento e acionar contato leve. A decisao e a execucao principal ficam com o humano.
- Fim: O fluxo termina quando a equipe registra o resultado. A Taliya salva auditoria e, se nao puder seguir, criar tarefa/caso em /app/retencao; tarefa e manter auditoria do motivo.
- Ajustes afetados: tipo de marco; responsavel; limite de contato
- Encadeamento: /app/retencao; tarefa

**Copiloto** (habilitado)

- Inicio: O fluxo comeca quando surge um caso para reconhecer marco de engajamento e acionar contato leve. A Taliya identifica o contexto e mostra a base da sugestao: marco configurado aconteceu; aluno esta ativo; tipo de marco esta permitido.
- Meio: A Taliya sugere reconhecer marco de engajamento e acionar contato leve, prepara texto/resumo/proximo passo e mostra os dados usados. A equipe pode aceitar, editar ou descartar antes de executar.
- Fim: Se a equipe aceitar, a acao e registrada conforme a decisao humana. Se editar ou descartar, a Taliya registra a decisao e mantem continuidade em /app/retencao; tarefa.
- Ajustes afetados: tipo de marco; responsavel; limite de contato
- Encadeamento: /app/retencao; tarefa

**Autonomo com aprovacao** (habilitado)

- Inicio: O fluxo comeca quando surge um caso para reconhecer marco de engajamento e acionar contato leve. A Taliya identifica o caso, confere marco configurado aconteceu; aluno esta ativo; tipo de marco esta permitido e prepara a revisao.
- Meio: A Taliya valida marco configurado aconteceu; aluno esta ativo; tipo de marco esta permitido; responsavel esta definido e prepara reconhecer marco de engajamento e acionar contato leve. Antes de concluir, mostra impacto/preview e pede aprovacao.
- Fim: Se aprovado, a acao e concluida e auditada. Se recusado, vencido ou incompleto, criar tarefa/caso em /app/retencao; tarefa e manter auditoria do motivo.
- Ajustes afetados: tipo de marco; responsavel; limite de contato
- Encadeamento: /app/retencao; tarefa

**Autonomo com excecoes** (habilitado)

- Inicio: O fluxo comeca quando surge um caso para reconhecer marco de engajamento e acionar contato leve. A Taliya identifica o caso e valida os dados principais: marco configurado aconteceu; aluno esta ativo; tipo de marco esta permitido.
- Meio: A Taliya executa sozinha quando marco configurado aconteceu; aluno esta ativo; tipo de marco esta permitido; responsavel esta definido; limite de contato nao foi atingido. Ela chama a equipe quando aluno tem caso sensivel aberto; marco conflita com baixa frequencia; mensagem poderia soar inadequada; aluno pediu opt-out; canal, cota ou permissao bloqueia contato.
- Fim: No caso comum, a acao `reconhecer marco de engajamento e acionar contato leve` fica registrada e auditada. Se houver excecao, criar tarefa/caso em /app/retencao; tarefa e manter auditoria do motivo.
- Ajustes afetados: tipo de marco; responsavel; limite de contato
- Encadeamento: /app/retencao; tarefa

**Autonomo** (bloqueado)

- Inicio: Este modo fica bloqueado para Marco engajamento.
- Meio: A Taliya nao conclui end-to-end porque este modo esta acima do teto do fluxo.
- Fim: Use o maior modo habilitado para automatizar o caso comum sem ultrapassar os limites publicados.
- Ajustes afetados: tipo de marco; responsavel; limite de contato
- Encadeamento: /app/retencao; tarefa


### Rotina: Casos sensiveis


#### Saude/evento pessoal

**Manual** (habilitado)

- Inicio: O fluxo comeca quando surge um caso para preparar caso de saude ou evento pessoal para aprovacao. A Taliya identifica o caso e organiza o contexto principal: evento foi identificado; visibilidade esta definida; dono do caso foi atribuido.
- Meio: A Taliya cria tarefa, checklist ou caso para a equipe preparar caso de saude ou evento pessoal para aprovacao. A decisao e a execucao principal ficam com o humano.
- Fim: O fluxo termina quando a equipe registra o resultado. A Taliya salva auditoria e, se nao puder seguir, criar tarefa/caso em /app/operacao; /app/historico; caso e manter auditoria do motivo.
- Ajustes afetados: dono do caso; visibilidade; aprovador
- Encadeamento: /app/operacao; /app/historico; caso

**Copiloto** (habilitado)

- Inicio: O fluxo comeca quando surge um caso para preparar caso de saude ou evento pessoal para aprovacao. A Taliya identifica o contexto e mostra a base da sugestao: evento foi identificado; visibilidade esta definida; dono do caso foi atribuido.
- Meio: A Taliya sugere preparar caso de saude ou evento pessoal para aprovacao, prepara texto/resumo/proximo passo e mostra os dados usados. A equipe pode aceitar, editar ou descartar antes de executar.
- Fim: Se a equipe aceitar, a acao e registrada conforme a decisao humana. Se editar ou descartar, a Taliya registra a decisao e mantem continuidade em /app/operacao; /app/historico; caso.
- Ajustes afetados: dono do caso; visibilidade; aprovador
- Encadeamento: /app/operacao; /app/historico; caso

**Autonomo com aprovacao** (habilitado)

- Inicio: O fluxo comeca quando surge um caso para preparar caso de saude ou evento pessoal para aprovacao. A Taliya identifica o caso, confere evento foi identificado; visibilidade esta definida; dono do caso foi atribuido e prepara a revisao.
- Meio: A Taliya valida evento foi identificado; visibilidade esta definida; dono do caso foi atribuido; nenhum contato automatico sera feito sem revisao e prepara preparar caso de saude ou evento pessoal para aprovacao. Antes de concluir, mostra impacto/preview e pede aprovacao.
- Fim: Se aprovado, a acao e concluida e auditada. Se recusado, vencido ou incompleto, criar tarefa/caso em /app/operacao; /app/historico; caso e manter auditoria do motivo.
- Ajustes afetados: dono do caso; visibilidade; aprovador
- Encadeamento: /app/operacao; /app/historico; caso

**Autonomo com excecoes** (bloqueado)

- Inicio: Este modo fica bloqueado para Saude/evento pessoal.
- Meio: A Taliya nao executa com excecoes porque o teto deste fluxo e menor.
- Fim: O usuario deve escolher um modo permitido para este fluxo.
- Ajustes afetados: dono do caso; visibilidade; aprovador
- Encadeamento: /app/operacao; /app/historico; caso

**Autonomo** (bloqueado)

- Inicio: Este modo fica bloqueado para Saude/evento pessoal.
- Meio: A Taliya nao conclui end-to-end porque este modo esta acima do teto do fluxo.
- Fim: Use o maior modo habilitado para automatizar o caso comum sem ultrapassar os limites publicados.
- Ajustes afetados: dono do caso; visibilidade; aprovador
- Encadeamento: /app/operacao; /app/historico; caso


#### Segmentacao risco

**Manual** (habilitado)

- Inicio: O fluxo comeca quando surge um caso para preparar segmentacao de risco para aprovacao. A Taliya identifica o caso e organiza o contexto principal: segmento foi definido; acao permitida foi escolhida; dados usados foram listados.
- Meio: A Taliya cria tarefa, checklist ou caso para a equipe preparar segmentacao de risco para aprovacao. A decisao e a execucao principal ficam com o humano.
- Fim: O fluxo termina quando a equipe registra o resultado. A Taliya salva auditoria e, se nao puder seguir, criar tarefa/caso em /app/retencao/riscos; /app/aprovacoes e manter auditoria do motivo.
- Ajustes afetados: aprovador; segmento; acao permitida
- Encadeamento: /app/retencao/riscos; /app/aprovacoes

**Copiloto** (habilitado)

- Inicio: O fluxo comeca quando surge um caso para preparar segmentacao de risco para aprovacao. A Taliya identifica o contexto e mostra a base da sugestao: segmento foi definido; acao permitida foi escolhida; dados usados foram listados.
- Meio: A Taliya sugere preparar segmentacao de risco para aprovacao, prepara texto/resumo/proximo passo e mostra os dados usados. A equipe pode aceitar, editar ou descartar antes de executar.
- Fim: Se a equipe aceitar, a acao e registrada conforme a decisao humana. Se editar ou descartar, a Taliya registra a decisao e mantem continuidade em /app/retencao/riscos; /app/aprovacoes.
- Ajustes afetados: aprovador; segmento; acao permitida
- Encadeamento: /app/retencao/riscos; /app/aprovacoes

**Autonomo com aprovacao** (habilitado)

- Inicio: O fluxo comeca quando surge um caso para preparar segmentacao de risco para aprovacao. A Taliya identifica o caso, confere segmento foi definido; acao permitida foi escolhida; dados usados foram listados e prepara a revisao.
- Meio: A Taliya valida segmento foi definido; acao permitida foi escolhida; dados usados foram listados; responsavel esta definido e prepara preparar segmentacao de risco para aprovacao. Antes de concluir, mostra impacto/preview e pede aprovacao.
- Fim: Se aprovado, a acao e concluida e auditada. Se recusado, vencido ou incompleto, criar tarefa/caso em /app/retencao/riscos; /app/aprovacoes e manter auditoria do motivo.
- Ajustes afetados: aprovador; segmento; acao permitida
- Encadeamento: /app/retencao/riscos; /app/aprovacoes

**Autonomo com excecoes** (bloqueado)

- Inicio: Este modo fica bloqueado para Segmentacao risco.
- Meio: A Taliya nao executa com excecoes porque o teto deste fluxo e menor.
- Fim: O usuario deve escolher um modo permitido para este fluxo.
- Ajustes afetados: aprovador; segmento; acao permitida
- Encadeamento: /app/retencao/riscos; /app/aprovacoes

**Autonomo** (bloqueado)

- Inicio: Este modo fica bloqueado para Segmentacao risco.
- Meio: A Taliya nao conclui end-to-end porque este modo esta acima do teto do fluxo.
- Fim: Use o maior modo habilitado para automatizar o caso comum sem ultrapassar os limites publicados.
- Ajustes afetados: aprovador; segmento; acao permitida
- Encadeamento: /app/retencao/riscos; /app/aprovacoes


#### Reclamacao e recuperacao de confianca

**Manual** (habilitado)

- Inicio: O fluxo comeca quando surge um caso para preparar recuperacao de reclamacao para aprovacao. A Taliya identifica o caso e organiza o contexto principal: reclamacao foi registrada; dono do caso esta definido; automacoes foram pausadas.
- Meio: A Taliya cria tarefa, checklist ou caso para a equipe preparar recuperacao de reclamacao para aprovacao. A decisao e a execucao principal ficam com o humano.
- Fim: O fluxo termina quando a equipe registra o resultado. A Taliya salva auditoria e, se nao puder seguir, criar tarefa/caso em /app/reclamacoes; /app/operacao; /app/aprovacoes e manter auditoria do motivo.
- Ajustes afetados: dono do caso; aprovador; pausa automatica
- Encadeamento: /app/reclamacoes; /app/operacao; /app/aprovacoes

**Copiloto** (habilitado)

- Inicio: O fluxo comeca quando surge um caso para preparar recuperacao de reclamacao para aprovacao. A Taliya identifica o contexto e mostra a base da sugestao: reclamacao foi registrada; dono do caso esta definido; automacoes foram pausadas.
- Meio: A Taliya sugere preparar recuperacao de reclamacao para aprovacao, prepara texto/resumo/proximo passo e mostra os dados usados. A equipe pode aceitar, editar ou descartar antes de executar.
- Fim: Se a equipe aceitar, a acao e registrada conforme a decisao humana. Se editar ou descartar, a Taliya registra a decisao e mantem continuidade em /app/reclamacoes; /app/operacao; /app/aprovacoes.
- Ajustes afetados: dono do caso; aprovador; pausa automatica
- Encadeamento: /app/reclamacoes; /app/operacao; /app/aprovacoes

**Autonomo com aprovacao** (habilitado)

- Inicio: O fluxo comeca quando surge um caso para preparar recuperacao de reclamacao para aprovacao. A Taliya identifica o caso, confere reclamacao foi registrada; dono do caso esta definido; automacoes foram pausadas e prepara a revisao.
- Meio: A Taliya valida reclamacao foi registrada; dono do caso esta definido; automacoes foram pausadas; resumo e proposta foram preparados e prepara preparar recuperacao de reclamacao para aprovacao. Antes de concluir, mostra impacto/preview e pede aprovacao.
- Fim: Se aprovado, a acao e concluida e auditada. Se recusado, vencido ou incompleto, criar tarefa/caso em /app/reclamacoes; /app/operacao; /app/aprovacoes e manter auditoria do motivo.
- Ajustes afetados: dono do caso; aprovador; pausa automatica
- Encadeamento: /app/reclamacoes; /app/operacao; /app/aprovacoes

**Autonomo com excecoes** (bloqueado)

- Inicio: Este modo fica bloqueado para Reclamacao e recuperacao de confianca.
- Meio: A Taliya nao executa com excecoes porque o teto deste fluxo e menor.
- Fim: O usuario deve escolher um modo permitido para este fluxo.
- Ajustes afetados: dono do caso; aprovador; pausa automatica
- Encadeamento: /app/reclamacoes; /app/operacao; /app/aprovacoes

**Autonomo** (bloqueado)

- Inicio: Este modo fica bloqueado para Reclamacao e recuperacao de confianca.
- Meio: A Taliya nao conclui end-to-end porque este modo esta acima do teto do fluxo.
- Fim: Use o maior modo habilitado para automatizar o caso comum sem ultrapassar os limites publicados.
- Ajustes afetados: dono do caso; aprovador; pausa automatica
- Encadeamento: /app/reclamacoes; /app/operacao; /app/aprovacoes


## Agente: Gestao/Governanca


### Rotina: Comando operacional


#### Prioridades dia

**Manual** (habilitado)

- Inicio: O fluxo comeca quando surge um caso para montar prioridades do dia. A Taliya identifica o caso e organiza o contexto principal: fontes operacionais estao atualizadas; horario do resumo chegou; responsavel esta definido.
- Meio: A Taliya cria tarefa, checklist ou caso para a equipe montar prioridades do dia. A decisao e a execucao principal ficam com o humano.
- Fim: O fluxo termina quando a equipe registra o resultado. A Taliya salva auditoria e, se nao puder seguir, criar tarefa/caso em /app/hoje; /app/tarefas e manter auditoria do motivo.
- Ajustes afetados: horario do resumo; responsavel; fontes exibidas
- Encadeamento: /app/hoje; /app/tarefas

**Copiloto** (habilitado)

- Inicio: O fluxo comeca quando surge um caso para montar prioridades do dia. A Taliya identifica o contexto e mostra a base da sugestao: fontes operacionais estao atualizadas; horario do resumo chegou; responsavel esta definido.
- Meio: A Taliya sugere montar prioridades do dia, prepara texto/resumo/proximo passo e mostra os dados usados. A equipe pode aceitar, editar ou descartar antes de executar.
- Fim: Se a equipe aceitar, a acao e registrada conforme a decisao humana. Se editar ou descartar, a Taliya registra a decisao e mantem continuidade em /app/hoje; /app/tarefas.
- Ajustes afetados: horario do resumo; responsavel; fontes exibidas
- Encadeamento: /app/hoje; /app/tarefas

**Autonomo com aprovacao** (habilitado)

- Inicio: O fluxo comeca quando surge um caso para montar prioridades do dia. A Taliya identifica o caso, confere fontes operacionais estao atualizadas; horario do resumo chegou; responsavel esta definido e prepara a revisao.
- Meio: A Taliya valida fontes operacionais estao atualizadas; horario do resumo chegou; responsavel esta definido; tarefas e aprovacoes foram consolidadas e prepara montar prioridades do dia. Antes de concluir, mostra impacto/preview e pede aprovacao.
- Fim: Se aprovado, a acao e concluida e auditada. Se recusado, vencido ou incompleto, criar tarefa/caso em /app/hoje; /app/tarefas e manter auditoria do motivo.
- Ajustes afetados: horario do resumo; responsavel; fontes exibidas
- Encadeamento: /app/hoje; /app/tarefas

**Autonomo com excecoes** (habilitado)

- Inicio: O fluxo comeca quando surge um caso para montar prioridades do dia. A Taliya identifica o caso e valida os dados principais: fontes operacionais estao atualizadas; horario do resumo chegou; responsavel esta definido.
- Meio: A Taliya executa sozinha quando fontes operacionais estao atualizadas; horario do resumo chegou; responsavel esta definido; tarefas e aprovacoes foram consolidadas; nada critico impede leitura. Ela chama a equipe quando fonte importante falhou; ha incidente critico; dado principal esta desatualizado; responsavel nao esta definido; permissao ou cota bloqueia resumo.
- Fim: No caso comum, a acao `montar prioridades do dia` fica registrada e auditada. Se houver excecao, criar tarefa/caso em /app/hoje; /app/tarefas e manter auditoria do motivo.
- Ajustes afetados: horario do resumo; responsavel; fontes exibidas
- Encadeamento: /app/hoje; /app/tarefas

**Autonomo** (habilitado)

- Inicio: O fluxo comeca quando surge um caso para montar prioridades do dia. A Taliya identifica o caso e confirma fontes operacionais estao atualizadas; horario do resumo chegou; responsavel esta definido.
- Meio: A Taliya conclui montar prioridades do dia quando fontes operacionais estao atualizadas; horario do resumo chegou; responsavel esta definido; tarefas e aprovacoes foram consolidadas; nada critico impede leitura. Ela para quando fonte importante falhou; ha incidente critico; dado principal esta desatualizado; responsavel nao esta definido; permissao ou cota bloqueia resumo.
- Fim: A acao e concluida, a auditoria fica salva e a continuidade segue em /app/hoje; /app/tarefas. Se houver bloqueio, criar tarefa/caso em /app/hoje; /app/tarefas e manter auditoria do motivo.
- Ajustes afetados: horario do resumo; responsavel; fontes exibidas
- Encadeamento: /app/hoje; /app/tarefas


#### Dinheiro na mesa

**Manual** (habilitado)

- Inicio: O fluxo comeca quando surge um caso para identificar dinheiro na mesa e abrir proxima acao. A Taliya identifica o caso e organiza o contexto principal: oportunidade financeira foi detectada; frequencia do alerta permite envio; responsavel esta definido.
- Meio: A Taliya cria tarefa, checklist ou caso para a equipe identificar dinheiro na mesa e abrir proxima acao. A decisao e a execucao principal ficam com o humano.
- Fim: O fluxo termina quando a equipe registra o resultado. A Taliya salva auditoria e, se nao puder seguir, criar tarefa/caso em /app/dinheiro-na-mesa; /app/financeiro; tarefa e manter auditoria do motivo.
- Ajustes afetados: frequencia; responsavel; quando abrir tarefa
- Encadeamento: /app/dinheiro-na-mesa; /app/financeiro; tarefa

**Copiloto** (habilitado)

- Inicio: O fluxo comeca quando surge um caso para identificar dinheiro na mesa e abrir proxima acao. A Taliya identifica o contexto e mostra a base da sugestao: oportunidade financeira foi detectada; frequencia do alerta permite envio; responsavel esta definido.
- Meio: A Taliya sugere identificar dinheiro na mesa e abrir proxima acao, prepara texto/resumo/proximo passo e mostra os dados usados. A equipe pode aceitar, editar ou descartar antes de executar.
- Fim: Se a equipe aceitar, a acao e registrada conforme a decisao humana. Se editar ou descartar, a Taliya registra a decisao e mantem continuidade em /app/dinheiro-na-mesa; /app/financeiro; tarefa.
- Ajustes afetados: frequencia; responsavel; quando abrir tarefa
- Encadeamento: /app/dinheiro-na-mesa; /app/financeiro; tarefa

**Autonomo com aprovacao** (habilitado)

- Inicio: O fluxo comeca quando surge um caso para identificar dinheiro na mesa e abrir proxima acao. A Taliya identifica o caso, confere oportunidade financeira foi detectada; frequencia do alerta permite envio; responsavel esta definido e prepara a revisao.
- Meio: A Taliya valida oportunidade financeira foi detectada; frequencia do alerta permite envio; responsavel esta definido; acao sugerida nao altera financeiro sozinha e prepara identificar dinheiro na mesa e abrir proxima acao. Antes de concluir, mostra impacto/preview e pede aprovacao.
- Fim: Se aprovado, a acao e concluida e auditada. Se recusado, vencido ou incompleto, criar tarefa/caso em /app/dinheiro-na-mesa; /app/financeiro; tarefa e manter auditoria do motivo.
- Ajustes afetados: frequencia; responsavel; quando abrir tarefa
- Encadeamento: /app/dinheiro-na-mesa; /app/financeiro; tarefa

**Autonomo com excecoes** (habilitado)

- Inicio: O fluxo comeca quando surge um caso para identificar dinheiro na mesa e abrir proxima acao. A Taliya identifica o caso e valida os dados principais: oportunidade financeira foi detectada; frequencia do alerta permite envio; responsavel esta definido.
- Meio: A Taliya executa sozinha quando oportunidade financeira foi detectada; frequencia do alerta permite envio; responsavel esta definido; acao sugerida nao altera financeiro sozinha; dados financeiros estao disponiveis. Ela chama a equipe quando valor esta incerto; caso depende de acordo ou desconto; movimentacao esta em disputa; responsavel nao existe; permissao ou cota bloqueia analise.
- Fim: No caso comum, a acao `identificar dinheiro na mesa e abrir proxima acao` fica registrada e auditada. Se houver excecao, criar tarefa/caso em /app/dinheiro-na-mesa; /app/financeiro; tarefa e manter auditoria do motivo.
- Ajustes afetados: frequencia; responsavel; quando abrir tarefa
- Encadeamento: /app/dinheiro-na-mesa; /app/financeiro; tarefa

**Autonomo** (bloqueado)

- Inicio: Este modo fica bloqueado para Dinheiro na mesa.
- Meio: A Taliya nao conclui end-to-end porque este modo esta acima do teto do fluxo.
- Fim: Use o maior modo habilitado para automatizar o caso comum sem ultrapassar os limites publicados.
- Ajustes afetados: frequencia; responsavel; quando abrir tarefa
- Encadeamento: /app/dinheiro-na-mesa; /app/financeiro; tarefa


#### Fila humana

**Manual** (habilitado)

- Inicio: O fluxo comeca quando surge um caso para organizar fila humana e prioridades. A Taliya identifica o caso e organiza o contexto principal: itens humanos foram encontrados; filas estao configuradas; prioridade foi calculada.
- Meio: A Taliya cria tarefa, checklist ou caso para a equipe organizar fila humana e prioridades. A decisao e a execucao principal ficam com o humano.
- Fim: O fluxo termina quando a equipe registra o resultado. A Taliya salva auditoria e, se nao puder seguir, criar tarefa/caso em /app/operacao; /app/aprovacoes; /app/tarefas e manter auditoria do motivo.
- Ajustes afetados: filas; prioridade; responsaveis
- Encadeamento: /app/operacao; /app/aprovacoes; /app/tarefas

**Copiloto** (habilitado)

- Inicio: O fluxo comeca quando surge um caso para organizar fila humana e prioridades. A Taliya identifica o contexto e mostra a base da sugestao: itens humanos foram encontrados; filas estao configuradas; prioridade foi calculada.
- Meio: A Taliya sugere organizar fila humana e prioridades, prepara texto/resumo/proximo passo e mostra os dados usados. A equipe pode aceitar, editar ou descartar antes de executar.
- Fim: Se a equipe aceitar, a acao e registrada conforme a decisao humana. Se editar ou descartar, a Taliya registra a decisao e mantem continuidade em /app/operacao; /app/aprovacoes; /app/tarefas.
- Ajustes afetados: filas; prioridade; responsaveis
- Encadeamento: /app/operacao; /app/aprovacoes; /app/tarefas

**Autonomo com aprovacao** (habilitado)

- Inicio: O fluxo comeca quando surge um caso para organizar fila humana e prioridades. A Taliya identifica o caso, confere itens humanos foram encontrados; filas estao configuradas; prioridade foi calculada e prepara a revisao.
- Meio: A Taliya valida itens humanos foram encontrados; filas estao configuradas; prioridade foi calculada; responsaveis existem e prepara organizar fila humana e prioridades. Antes de concluir, mostra impacto/preview e pede aprovacao.
- Fim: Se aprovado, a acao e concluida e auditada. Se recusado, vencido ou incompleto, criar tarefa/caso em /app/operacao; /app/aprovacoes; /app/tarefas e manter auditoria do motivo.
- Ajustes afetados: filas; prioridade; responsaveis
- Encadeamento: /app/operacao; /app/aprovacoes; /app/tarefas

**Autonomo com excecoes** (habilitado)

- Inicio: O fluxo comeca quando surge um caso para organizar fila humana e prioridades. A Taliya identifica o caso e valida os dados principais: itens humanos foram encontrados; filas estao configuradas; prioridade foi calculada.
- Meio: A Taliya executa sozinha quando itens humanos foram encontrados; filas estao configuradas; prioridade foi calculada; responsaveis existem; nenhum item exige permissao ausente. Ela chama a equipe quando item sem dono; prioridade conflita entre filas; incidente aberto exige pausa; aprovacao vencida acumulou; permissao ou cota bloqueia atualizacao.
- Fim: No caso comum, a acao `organizar fila humana e prioridades` fica registrada e auditada. Se houver excecao, criar tarefa/caso em /app/operacao; /app/aprovacoes; /app/tarefas e manter auditoria do motivo.
- Ajustes afetados: filas; prioridade; responsaveis
- Encadeamento: /app/operacao; /app/aprovacoes; /app/tarefas

**Autonomo** (habilitado)

- Inicio: O fluxo comeca quando surge um caso para organizar fila humana e prioridades. A Taliya identifica o caso e confirma itens humanos foram encontrados; filas estao configuradas; prioridade foi calculada.
- Meio: A Taliya conclui organizar fila humana e prioridades quando itens humanos foram encontrados; filas estao configuradas; prioridade foi calculada; responsaveis existem; nenhum item exige permissao ausente. Ela para quando item sem dono; prioridade conflita entre filas; incidente aberto exige pausa; aprovacao vencida acumulou; permissao ou cota bloqueia atualizacao.
- Fim: A acao e concluida, a auditoria fica salva e a continuidade segue em /app/operacao; /app/aprovacoes; /app/tarefas. Se houver bloqueio, criar tarefa/caso em /app/operacao; /app/aprovacoes; /app/tarefas e manter auditoria do motivo.
- Ajustes afetados: filas; prioridade; responsaveis
- Encadeamento: /app/operacao; /app/aprovacoes; /app/tarefas


#### Gargalos

**Manual** (habilitado)

- Inicio: O fluxo comeca quando surge um caso para detectar gargalos operacionais. A Taliya identifica o caso e organiza o contexto principal: metricas foram atualizadas; frequencia do alerta permite analise; tipo de alerta esta definido.
- Meio: A Taliya cria tarefa, checklist ou caso para a equipe detectar gargalos operacionais. A decisao e a execucao principal ficam com o humano.
- Fim: O fluxo termina quando a equipe registra o resultado. A Taliya salva auditoria e, se nao puder seguir, criar tarefa/caso em /app/relatorios; /app/operacao; tarefa e manter auditoria do motivo.
- Ajustes afetados: frequencia; responsavel; tipo de alerta
- Encadeamento: /app/relatorios; /app/operacao; tarefa

**Copiloto** (habilitado)

- Inicio: O fluxo comeca quando surge um caso para detectar gargalos operacionais. A Taliya identifica o contexto e mostra a base da sugestao: metricas foram atualizadas; frequencia do alerta permite analise; tipo de alerta esta definido.
- Meio: A Taliya sugere detectar gargalos operacionais, prepara texto/resumo/proximo passo e mostra os dados usados. A equipe pode aceitar, editar ou descartar antes de executar.
- Fim: Se a equipe aceitar, a acao e registrada conforme a decisao humana. Se editar ou descartar, a Taliya registra a decisao e mantem continuidade em /app/relatorios; /app/operacao; tarefa.
- Ajustes afetados: frequencia; responsavel; tipo de alerta
- Encadeamento: /app/relatorios; /app/operacao; tarefa

**Autonomo com aprovacao** (habilitado)

- Inicio: O fluxo comeca quando surge um caso para detectar gargalos operacionais. A Taliya identifica o caso, confere metricas foram atualizadas; frequencia do alerta permite analise; tipo de alerta esta definido e prepara a revisao.
- Meio: A Taliya valida metricas foram atualizadas; frequencia do alerta permite analise; tipo de alerta esta definido; responsavel esta atribuido e prepara detectar gargalos operacionais. Antes de concluir, mostra impacto/preview e pede aprovacao.
- Fim: Se aprovado, a acao e concluida e auditada. Se recusado, vencido ou incompleto, criar tarefa/caso em /app/relatorios; /app/operacao; tarefa e manter auditoria do motivo.
- Ajustes afetados: frequencia; responsavel; tipo de alerta
- Encadeamento: /app/relatorios; /app/operacao; tarefa

**Autonomo com excecoes** (habilitado)

- Inicio: O fluxo comeca quando surge um caso para detectar gargalos operacionais. A Taliya identifica o caso e valida os dados principais: metricas foram atualizadas; frequencia do alerta permite analise; tipo de alerta esta definido.
- Meio: A Taliya executa sozinha quando metricas foram atualizadas; frequencia do alerta permite analise; tipo de alerta esta definido; responsavel esta atribuido; acao sugerida e operacional. Ela chama a equipe quando dado esta incompleto; gargalo envolve financeiro, grade ou incidente; alerta e critico; responsavel nao definido; permissao ou cota bloqueia analise.
- Fim: No caso comum, a acao `detectar gargalos operacionais` fica registrada e auditada. Se houver excecao, criar tarefa/caso em /app/relatorios; /app/operacao; tarefa e manter auditoria do motivo.
- Ajustes afetados: frequencia; responsavel; tipo de alerta
- Encadeamento: /app/relatorios; /app/operacao; tarefa

**Autonomo** (bloqueado)

- Inicio: Este modo fica bloqueado para Gargalos.
- Meio: A Taliya nao conclui end-to-end porque este modo esta acima do teto do fluxo.
- Fim: Use o maior modo habilitado para automatizar o caso comum sem ultrapassar os limites publicados.
- Ajustes afetados: frequencia; responsavel; tipo de alerta
- Encadeamento: /app/relatorios; /app/operacao; tarefa


#### Resumo semanal

**Manual** (habilitado)

- Inicio: O fluxo comeca quando surge um caso para gerar resumo semanal. A Taliya identifica o caso e organiza o contexto principal: periodo da semana fechou; secoes do resumo estao configuradas; destinatarios internos estao definidos.
- Meio: A Taliya cria tarefa, checklist ou caso para a equipe gerar resumo semanal. A decisao e a execucao principal ficam com o humano.
- Fim: O fluxo termina quando a equipe registra o resultado. A Taliya salva auditoria e, se nao puder seguir, criar tarefa/caso em /app/relatorios/semana; /app/hoje e manter auditoria do motivo.
- Ajustes afetados: dia/hora; destinatarios internos; secoes
- Encadeamento: /app/relatorios/semana; /app/hoje

**Copiloto** (habilitado)

- Inicio: O fluxo comeca quando surge um caso para gerar resumo semanal. A Taliya identifica o contexto e mostra a base da sugestao: periodo da semana fechou; secoes do resumo estao configuradas; destinatarios internos estao definidos.
- Meio: A Taliya sugere gerar resumo semanal, prepara texto/resumo/proximo passo e mostra os dados usados. A equipe pode aceitar, editar ou descartar antes de executar.
- Fim: Se a equipe aceitar, a acao e registrada conforme a decisao humana. Se editar ou descartar, a Taliya registra a decisao e mantem continuidade em /app/relatorios/semana; /app/hoje.
- Ajustes afetados: dia/hora; destinatarios internos; secoes
- Encadeamento: /app/relatorios/semana; /app/hoje

**Autonomo com aprovacao** (habilitado)

- Inicio: O fluxo comeca quando surge um caso para gerar resumo semanal. A Taliya identifica o caso, confere periodo da semana fechou; secoes do resumo estao configuradas; destinatarios internos estao definidos e prepara a revisao.
- Meio: A Taliya valida periodo da semana fechou; secoes do resumo estao configuradas; destinatarios internos estao definidos; dados principais estao atualizados e prepara gerar resumo semanal. Antes de concluir, mostra impacto/preview e pede aprovacao.
- Fim: Se aprovado, a acao e concluida e auditada. Se recusado, vencido ou incompleto, criar tarefa/caso em /app/relatorios/semana; /app/hoje e manter auditoria do motivo.
- Ajustes afetados: dia/hora; destinatarios internos; secoes
- Encadeamento: /app/relatorios/semana; /app/hoje

**Autonomo com excecoes** (habilitado)

- Inicio: O fluxo comeca quando surge um caso para gerar resumo semanal. A Taliya identifica o caso e valida os dados principais: periodo da semana fechou; secoes do resumo estao configuradas; destinatarios internos estao definidos.
- Meio: A Taliya executa sozinha quando periodo da semana fechou; secoes do resumo estao configuradas; destinatarios internos estao definidos; dados principais estao atualizados; nenhum incidente impede resumo. Ela chama a equipe quando fonte de dados falhou; secoes obrigatorias vazias; destinatario sem permissao; incidente critico em aberto; cota ou permissao bloqueia envio.
- Fim: No caso comum, a acao `gerar resumo semanal` fica registrada e auditada. Se houver excecao, criar tarefa/caso em /app/relatorios/semana; /app/hoje e manter auditoria do motivo.
- Ajustes afetados: dia/hora; destinatarios internos; secoes
- Encadeamento: /app/relatorios/semana; /app/hoje

**Autonomo** (habilitado)

- Inicio: O fluxo comeca quando surge um caso para gerar resumo semanal. A Taliya identifica o caso e confirma periodo da semana fechou; secoes do resumo estao configuradas; destinatarios internos estao definidos.
- Meio: A Taliya conclui gerar resumo semanal quando periodo da semana fechou; secoes do resumo estao configuradas; destinatarios internos estao definidos; dados principais estao atualizados; nenhum incidente impede resumo. Ela para quando fonte de dados falhou; secoes obrigatorias vazias; destinatario sem permissao; incidente critico em aberto; cota ou permissao bloqueia envio.
- Fim: A acao e concluida, a auditoria fica salva e a continuidade segue em /app/relatorios/semana; /app/hoje. Se houver bloqueio, criar tarefa/caso em /app/relatorios/semana; /app/hoje e manter auditoria do motivo.
- Ajustes afetados: dia/hora; destinatarios internos; secoes
- Encadeamento: /app/relatorios/semana; /app/hoje


#### Qualidade dados

**Manual** (habilitado)

- Inicio: O fluxo comeca quando surge um caso para detectar qualidade de dados e abrir tarefa de correcao. A Taliya identifica o caso e organiza o contexto principal: tipo de dado a revisar pertence aos campos monitorados; duplicidade ou lacuna foi detectada; prioridade foi calculada.
- Meio: A Taliya cria tarefa, checklist ou caso para a equipe detectar qualidade de dados e abrir tarefa de correcao. A decisao e a execucao principal ficam com o humano.
- Fim: O fluxo termina quando a equipe registra o resultado. A Taliya salva auditoria e, se nao puder seguir, criar tarefa/caso em /app/dados/qualidade; /app/dados/duplicidades; tarefa e manter auditoria do motivo.
- Ajustes afetados: responsavel; tipos de dado; prioridade
- Encadeamento: /app/dados/qualidade; /app/dados/duplicidades; tarefa

**Copiloto** (habilitado)

- Inicio: O fluxo comeca quando surge um caso para detectar qualidade de dados e abrir tarefa de correcao. A Taliya identifica o contexto e mostra a base da sugestao: tipo de dado a revisar pertence aos campos monitorados; duplicidade ou lacuna foi detectada; prioridade foi calculada.
- Meio: A Taliya sugere detectar qualidade de dados e abrir tarefa de correcao, prepara texto/resumo/proximo passo e mostra os dados usados. A equipe pode aceitar, editar ou descartar antes de executar.
- Fim: Se a equipe aceitar, a acao e registrada conforme a decisao humana. Se editar ou descartar, a Taliya registra a decisao e mantem continuidade em /app/dados/qualidade; /app/dados/duplicidades; tarefa.
- Ajustes afetados: responsavel; tipos de dado; prioridade
- Encadeamento: /app/dados/qualidade; /app/dados/duplicidades; tarefa

**Autonomo com aprovacao** (habilitado)

- Inicio: O fluxo comeca quando surge um caso para detectar qualidade de dados e abrir tarefa de correcao. A Taliya identifica o caso, confere tipo de dado a revisar pertence aos campos monitorados; duplicidade ou lacuna foi detectada; prioridade foi calculada e prepara a revisao.
- Meio: A Taliya valida tipo de dado a revisar pertence aos campos monitorados; duplicidade ou lacuna foi detectada; prioridade foi calculada; responsavel esta definido e prepara detectar qualidade de dados e abrir tarefa de correcao. Antes de concluir, mostra impacto/preview e pede aprovacao.
- Fim: Se aprovado, a acao e concluida e auditada. Se recusado, vencido ou incompleto, criar tarefa/caso em /app/dados/qualidade; /app/dados/duplicidades; tarefa e manter auditoria do motivo.
- Ajustes afetados: responsavel; tipos de dado; prioridade
- Encadeamento: /app/dados/qualidade; /app/dados/duplicidades; tarefa

**Autonomo com excecoes** (habilitado)

- Inicio: O fluxo comeca quando surge um caso para detectar qualidade de dados e abrir tarefa de correcao. A Taliya identifica o caso e valida os dados principais: tipo de dado a revisar pertence aos campos monitorados; duplicidade ou lacuna foi detectada; prioridade foi calculada.
- Meio: A Taliya executa sozinha quando tipo de dado a revisar pertence aos campos monitorados; duplicidade ou lacuna foi detectada; prioridade foi calculada; responsavel esta definido; correcao automatica nao altera dado sensivel. Ela chama a equipe quando correcao pode fundir cadastros; dado envolve historico protegido; conflito nao tem dono claro; volume e alto demais; permissao ou cota bloqueia analise.
- Fim: No caso comum, a acao `detectar qualidade de dados e abrir tarefa de correcao` fica registrada e auditada. Se houver excecao, criar tarefa/caso em /app/dados/qualidade; /app/dados/duplicidades; tarefa e manter auditoria do motivo.
- Ajustes afetados: responsavel; tipos de dado; prioridade
- Encadeamento: /app/dados/qualidade; /app/dados/duplicidades; tarefa

**Autonomo** (bloqueado)

- Inicio: Este modo fica bloqueado para Qualidade dados.
- Meio: A Taliya nao conclui end-to-end porque este modo esta acima do teto do fluxo.
- Fim: Use o maior modo habilitado para automatizar o caso comum sem ultrapassar os limites publicados.
- Ajustes afetados: responsavel; tipos de dado; prioridade
- Encadeamento: /app/dados/qualidade; /app/dados/duplicidades; tarefa


### Rotina: Governanca de agentes


#### Creditos/limites

**Manual** (habilitado)

- Inicio: O fluxo comeca quando surge um caso para monitorar creditos, limites e cotas. A Taliya identifica o caso e organiza o contexto principal: uso foi atualizado; alertas 70/90/100 estao configurados; responsavel esta definido.
- Meio: A Taliya cria tarefa, checklist ou caso para a equipe monitorar creditos, limites e cotas. A decisao e a execucao principal ficam com o humano.
- Fim: O fluxo termina quando a equipe registra o resultado. A Taliya salva auditoria e, se nao puder seguir, criar tarefa/caso em /app/uso; /app/uso/cotas; /app/hoje e manter auditoria do motivo.
- Ajustes afetados: limiares de alerta; responsavel; mensagem interna
- Encadeamento: /app/uso; /app/uso/cotas; /app/hoje

**Copiloto** (habilitado)

- Inicio: O fluxo comeca quando surge um caso para monitorar creditos, limites e cotas. A Taliya identifica o contexto e mostra a base da sugestao: uso foi atualizado; alertas 70/90/100 estao configurados; responsavel esta definido.
- Meio: A Taliya sugere monitorar creditos, limites e cotas, prepara texto/resumo/proximo passo e mostra os dados usados. A equipe pode aceitar, editar ou descartar antes de executar.
- Fim: Se a equipe aceitar, a acao e registrada conforme a decisao humana. Se editar ou descartar, a Taliya registra a decisao e mantem continuidade em /app/uso; /app/uso/cotas; /app/hoje.
- Ajustes afetados: limiares de alerta; responsavel; mensagem interna
- Encadeamento: /app/uso; /app/uso/cotas; /app/hoje

**Autonomo com aprovacao** (habilitado)

- Inicio: O fluxo comeca quando surge um caso para monitorar creditos, limites e cotas. A Taliya identifica o caso, confere uso foi atualizado; alertas 70/90/100 estao configurados; responsavel esta definido e prepara a revisao.
- Meio: A Taliya valida uso foi atualizado; alertas 70/90/100 estao configurados; responsavel esta definido; limite comercial foi lido do billing e prepara monitorar creditos, limites e cotas. Antes de concluir, mostra impacto/preview e pede aprovacao.
- Fim: Se aprovado, a acao e concluida e auditada. Se recusado, vencido ou incompleto, criar tarefa/caso em /app/uso; /app/uso/cotas; /app/hoje e manter auditoria do motivo.
- Ajustes afetados: limiares de alerta; responsavel; mensagem interna
- Encadeamento: /app/uso; /app/uso/cotas; /app/hoje

**Autonomo com excecoes** (habilitado)

- Inicio: O fluxo comeca quando surge um caso para monitorar creditos, limites e cotas. A Taliya identifica o caso e valida os dados principais: uso foi atualizado; alertas 70/90/100 estao configurados; responsavel esta definido.
- Meio: A Taliya executa sozinha quando uso foi atualizado; alertas 70/90/100 estao configurados; responsavel esta definido; limite comercial foi lido do billing; mensagem interna esta pronta. Ela chama a equipe quando cota atingiu limite critico; billing diverge do uso; responsavel nao definido; addon ou upgrade precisa decisao; permissao bloqueia leitura.
- Fim: No caso comum, a acao `monitorar creditos, limites e cotas` fica registrada e auditada. Se houver excecao, criar tarefa/caso em /app/uso; /app/uso/cotas; /app/hoje e manter auditoria do motivo.
- Ajustes afetados: limiares de alerta; responsavel; mensagem interna
- Encadeamento: /app/uso; /app/uso/cotas; /app/hoje

**Autonomo** (habilitado)

- Inicio: O fluxo comeca quando surge um caso para monitorar creditos, limites e cotas. A Taliya identifica o caso e confirma uso foi atualizado; alertas 70/90/100 estao configurados; responsavel esta definido.
- Meio: A Taliya conclui monitorar creditos, limites e cotas quando uso foi atualizado; alertas 70/90/100 estao configurados; responsavel esta definido; limite comercial foi lido do billing; mensagem interna esta pronta. Ela para quando cota atingiu limite critico; billing diverge do uso; responsavel nao definido; addon ou upgrade precisa decisao; permissao bloqueia leitura.
- Fim: A acao e concluida, a auditoria fica salva e a continuidade segue em /app/uso; /app/uso/cotas; /app/hoje. Se houver bloqueio, criar tarefa/caso em /app/uso; /app/uso/cotas; /app/hoje e manter auditoria do motivo.
- Ajustes afetados: limiares de alerta; responsavel; mensagem interna
- Encadeamento: /app/uso; /app/uso/cotas; /app/hoje


#### Performance

**Manual** (habilitado)

- Inicio: O fluxo comeca quando surge um caso para monitorar performance dos agentes. A Taliya identifica o caso e organiza o contexto principal: metricas foram coletadas; frequencia permite novo relatorio; responsavel esta definido.
- Meio: A Taliya cria tarefa, checklist ou caso para a equipe monitorar performance dos agentes. A decisao e a execucao principal ficam com o humano.
- Fim: O fluxo termina quando a equipe registra o resultado. A Taliya salva auditoria e, se nao puder seguir, criar tarefa/caso em /app/relatorios/agentes; /app/agentes; tarefa e manter auditoria do motivo.
- Ajustes afetados: frequencia; responsavel; metricas exibidas
- Encadeamento: /app/relatorios/agentes; /app/agentes; tarefa

**Copiloto** (habilitado)

- Inicio: O fluxo comeca quando surge um caso para monitorar performance dos agentes. A Taliya identifica o contexto e mostra a base da sugestao: metricas foram coletadas; frequencia permite novo relatorio; responsavel esta definido.
- Meio: A Taliya sugere monitorar performance dos agentes, prepara texto/resumo/proximo passo e mostra os dados usados. A equipe pode aceitar, editar ou descartar antes de executar.
- Fim: Se a equipe aceitar, a acao e registrada conforme a decisao humana. Se editar ou descartar, a Taliya registra a decisao e mantem continuidade em /app/relatorios/agentes; /app/agentes; tarefa.
- Ajustes afetados: frequencia; responsavel; metricas exibidas
- Encadeamento: /app/relatorios/agentes; /app/agentes; tarefa

**Autonomo com aprovacao** (habilitado)

- Inicio: O fluxo comeca quando surge um caso para monitorar performance dos agentes. A Taliya identifica o caso, confere metricas foram coletadas; frequencia permite novo relatorio; responsavel esta definido e prepara a revisao.
- Meio: A Taliya valida metricas foram coletadas; frequencia permite novo relatorio; responsavel esta definido; indicadores configurados existem e prepara monitorar performance dos agentes. Antes de concluir, mostra impacto/preview e pede aprovacao.
- Fim: Se aprovado, a acao e concluida e auditada. Se recusado, vencido ou incompleto, criar tarefa/caso em /app/relatorios/agentes; /app/agentes; tarefa e manter auditoria do motivo.
- Ajustes afetados: frequencia; responsavel; metricas exibidas
- Encadeamento: /app/relatorios/agentes; /app/agentes; tarefa

**Autonomo com excecoes** (habilitado)

- Inicio: O fluxo comeca quando surge um caso para monitorar performance dos agentes. A Taliya identifica o caso e valida os dados principais: metricas foram coletadas; frequencia permite novo relatorio; responsavel esta definido.
- Meio: A Taliya executa sozinha quando metricas foram coletadas; frequencia permite novo relatorio; responsavel esta definido; indicadores configurados existem; acao sugerida nao altera politica sozinha. Ela chama a equipe quando queda forte de performance; falha ou incidente correlacionado; amostra insuficiente; acao exige mudar fluxo ou politica; permissao ou cota bloqueia analise.
- Fim: No caso comum, a acao `monitorar performance dos agentes` fica registrada e auditada. Se houver excecao, criar tarefa/caso em /app/relatorios/agentes; /app/agentes; tarefa e manter auditoria do motivo.
- Ajustes afetados: frequencia; responsavel; metricas exibidas
- Encadeamento: /app/relatorios/agentes; /app/agentes; tarefa

**Autonomo** (bloqueado)

- Inicio: Este modo fica bloqueado para Performance.
- Meio: A Taliya nao conclui end-to-end porque este modo esta acima do teto do fluxo.
- Fim: Use o maior modo habilitado para automatizar o caso comum sem ultrapassar os limites publicados.
- Ajustes afetados: frequencia; responsavel; metricas exibidas
- Encadeamento: /app/relatorios/agentes; /app/agentes; tarefa


#### Permissoes/auditoria

**Manual** (habilitado)

- Inicio: O fluxo comeca quando surge um caso para preparar revisao de permissoes ou auditoria para aprovacao. A Taliya identifica o caso e organiza o contexto principal: evento de auditoria foi identificado; tipo de evento esta dentro do escopo; responsavel esta definido.
- Meio: A Taliya cria tarefa, checklist ou caso para a equipe preparar revisao de permissoes ou auditoria para aprovacao. A decisao e a execucao principal ficam com o humano.
- Fim: O fluxo termina quando a equipe registra o resultado. A Taliya salva auditoria e, se nao puder seguir, criar tarefa/caso em /app/auditoria; /app/configuracoes/permissoes; aprovacao e manter auditoria do motivo.
- Ajustes afetados: aprovador; tipos de evento; responsavel
- Encadeamento: /app/auditoria; /app/configuracoes/permissoes; aprovacao

**Copiloto** (habilitado)

- Inicio: O fluxo comeca quando surge um caso para preparar revisao de permissoes ou auditoria para aprovacao. A Taliya identifica o contexto e mostra a base da sugestao: evento de auditoria foi identificado; tipo de evento esta dentro do escopo; responsavel esta definido.
- Meio: A Taliya sugere preparar revisao de permissoes ou auditoria para aprovacao, prepara texto/resumo/proximo passo e mostra os dados usados. A equipe pode aceitar, editar ou descartar antes de executar.
- Fim: Se a equipe aceitar, a acao e registrada conforme a decisao humana. Se editar ou descartar, a Taliya registra a decisao e mantem continuidade em /app/auditoria; /app/configuracoes/permissoes; aprovacao.
- Ajustes afetados: aprovador; tipos de evento; responsavel
- Encadeamento: /app/auditoria; /app/configuracoes/permissoes; aprovacao

**Autonomo com aprovacao** (habilitado)

- Inicio: O fluxo comeca quando surge um caso para preparar revisao de permissoes ou auditoria para aprovacao. A Taliya identifica o caso, confere evento de auditoria foi identificado; tipo de evento esta dentro do escopo; responsavel esta definido e prepara a revisao.
- Meio: A Taliya valida evento de auditoria foi identificado; tipo de evento esta dentro do escopo; responsavel esta definido; impacto foi resumido e prepara preparar revisao de permissoes ou auditoria para aprovacao. Antes de concluir, mostra impacto/preview e pede aprovacao.
- Fim: Se aprovado, a acao e concluida e auditada. Se recusado, vencido ou incompleto, criar tarefa/caso em /app/auditoria; /app/configuracoes/permissoes; aprovacao e manter auditoria do motivo.
- Ajustes afetados: aprovador; tipos de evento; responsavel
- Encadeamento: /app/auditoria; /app/configuracoes/permissoes; aprovacao

**Autonomo com excecoes** (bloqueado)

- Inicio: Este modo fica bloqueado para Permissoes/auditoria.
- Meio: A Taliya nao executa com excecoes porque o teto deste fluxo e menor.
- Fim: O usuario deve escolher um modo permitido para este fluxo.
- Ajustes afetados: aprovador; tipos de evento; responsavel
- Encadeamento: /app/auditoria; /app/configuracoes/permissoes; aprovacao

**Autonomo** (bloqueado)

- Inicio: Este modo fica bloqueado para Permissoes/auditoria.
- Meio: A Taliya nao conclui end-to-end porque este modo esta acima do teto do fluxo.
- Fim: Use o maior modo habilitado para automatizar o caso comum sem ultrapassar os limites publicados.
- Ajustes afetados: aprovador; tipos de evento; responsavel
- Encadeamento: /app/auditoria; /app/configuracoes/permissoes; aprovacao


### Rotina: Comando operacional


#### Capacidade/crescimento

**Manual** (habilitado)

- Inicio: O fluxo comeca quando surge um caso para detectar capacidade e crescimento. A Taliya identifica o caso e organiza o contexto principal: ocupacao foi calculada; limite de alerta foi atingido ou esta proximo; responsavel esta definido.
- Meio: A Taliya cria tarefa, checklist ou caso para a equipe detectar capacidade e crescimento. A decisao e a execucao principal ficam com o humano.
- Fim: O fluxo termina quando a equipe registra o resultado. A Taliya salva auditoria e, se nao puder seguir, criar tarefa/caso em /app/relatorios/ocupacao; /app/agenda; tarefa e manter auditoria do motivo.
- Ajustes afetados: frequencia; responsavel; limite de alerta
- Encadeamento: /app/relatorios/ocupacao; /app/agenda; tarefa

**Copiloto** (habilitado)

- Inicio: O fluxo comeca quando surge um caso para detectar capacidade e crescimento. A Taliya identifica o contexto e mostra a base da sugestao: ocupacao foi calculada; limite de alerta foi atingido ou esta proximo; responsavel esta definido.
- Meio: A Taliya sugere detectar capacidade e crescimento, prepara texto/resumo/proximo passo e mostra os dados usados. A equipe pode aceitar, editar ou descartar antes de executar.
- Fim: Se a equipe aceitar, a acao e registrada conforme a decisao humana. Se editar ou descartar, a Taliya registra a decisao e mantem continuidade em /app/relatorios/ocupacao; /app/agenda; tarefa.
- Ajustes afetados: frequencia; responsavel; limite de alerta
- Encadeamento: /app/relatorios/ocupacao; /app/agenda; tarefa

**Autonomo com aprovacao** (habilitado)

- Inicio: O fluxo comeca quando surge um caso para detectar capacidade e crescimento. A Taliya identifica o caso, confere ocupacao foi calculada; limite de alerta foi atingido ou esta proximo; responsavel esta definido e prepara a revisao.
- Meio: A Taliya valida ocupacao foi calculada; limite de alerta foi atingido ou esta proximo; responsavel esta definido; acao sugerida nao altera grade sozinha e prepara detectar capacidade e crescimento. Antes de concluir, mostra impacto/preview e pede aprovacao.
- Fim: Se aprovado, a acao e concluida e auditada. Se recusado, vencido ou incompleto, criar tarefa/caso em /app/relatorios/ocupacao; /app/agenda; tarefa e manter auditoria do motivo.
- Ajustes afetados: frequencia; responsavel; limite de alerta
- Encadeamento: /app/relatorios/ocupacao; /app/agenda; tarefa

**Autonomo com excecoes** (habilitado)

- Inicio: O fluxo comeca quando surge um caso para detectar capacidade e crescimento. A Taliya identifica o caso e valida os dados principais: ocupacao foi calculada; limite de alerta foi atingido ou esta proximo; responsavel esta definido.
- Meio: A Taliya executa sozinha quando ocupacao foi calculada; limite de alerta foi atingido ou esta proximo; responsavel esta definido; acao sugerida nao altera grade sozinha; dados de agenda estao atualizados. Ela chama a equipe quando capacidade ultrapassa limite; crescimento exige nova turma ou horario; dados de agenda conflitam; impacto financeiro aparece; permissao ou cota bloqueia analise.
- Fim: No caso comum, a acao `detectar capacidade e crescimento` fica registrada e auditada. Se houver excecao, criar tarefa/caso em /app/relatorios/ocupacao; /app/agenda; tarefa e manter auditoria do motivo.
- Ajustes afetados: frequencia; responsavel; limite de alerta
- Encadeamento: /app/relatorios/ocupacao; /app/agenda; tarefa

**Autonomo** (bloqueado)

- Inicio: Este modo fica bloqueado para Capacidade/crescimento.
- Meio: A Taliya nao conclui end-to-end porque este modo esta acima do teto do fluxo.
- Fim: Use o maior modo habilitado para automatizar o caso comum sem ultrapassar os limites publicados.
- Ajustes afetados: frequencia; responsavel; limite de alerta
- Encadeamento: /app/relatorios/ocupacao; /app/agenda; tarefa


### Rotina: Integracoes e importacao


#### Falhas/webhooks

**Manual** (habilitado)

- Inicio: O fluxo comeca quando surge um caso para tratar falhas, webhooks e retries seguros. A Taliya identifica o caso e organiza o contexto principal: falha tecnica foi identificada; severidade esta definida; retry seguro e permitido.
- Meio: A Taliya cria tarefa, checklist ou caso para a equipe tratar falhas, webhooks e retries seguros. A decisao e a execucao principal ficam com o humano.
- Fim: O fluxo termina quando a equipe registra o resultado. A Taliya salva auditoria e, se nao puder seguir, criar tarefa/caso em configuracao especifica da integracao; /app/operacao/incidentes e manter auditoria do motivo.
- Ajustes afetados: responsavel; severidade; quando tentar novamente
- Encadeamento: configuracao especifica da integracao; /app/operacao/incidentes

**Copiloto** (habilitado)

- Inicio: O fluxo comeca quando surge um caso para tratar falhas, webhooks e retries seguros. A Taliya identifica o contexto e mostra a base da sugestao: falha tecnica foi identificada; severidade esta definida; retry seguro e permitido.
- Meio: A Taliya sugere tratar falhas, webhooks e retries seguros, prepara texto/resumo/proximo passo e mostra os dados usados. A equipe pode aceitar, editar ou descartar antes de executar.
- Fim: Se a equipe aceitar, a acao e registrada conforme a decisao humana. Se editar ou descartar, a Taliya registra a decisao e mantem continuidade em configuracao especifica da integracao; /app/operacao/incidentes.
- Ajustes afetados: responsavel; severidade; quando tentar novamente
- Encadeamento: configuracao especifica da integracao; /app/operacao/incidentes

**Autonomo com aprovacao** (habilitado)

- Inicio: O fluxo comeca quando surge um caso para tratar falhas, webhooks e retries seguros. A Taliya identifica o caso, confere falha tecnica foi identificada; severidade esta definida; retry seguro e permitido e prepara a revisao.
- Meio: A Taliya valida falha tecnica foi identificada; severidade esta definida; retry seguro e permitido; responsavel esta atribuido e prepara tratar falhas, webhooks e retries seguros. Antes de concluir, mostra impacto/preview e pede aprovacao.
- Fim: Se aprovado, a acao e concluida e auditada. Se recusado, vencido ou incompleto, criar tarefa/caso em configuracao especifica da integracao; /app/operacao/incidentes e manter auditoria do motivo.
- Ajustes afetados: responsavel; severidade; quando tentar novamente
- Encadeamento: configuracao especifica da integracao; /app/operacao/incidentes

**Autonomo com excecoes** (habilitado)

- Inicio: O fluxo comeca quando surge um caso para tratar falhas, webhooks e retries seguros. A Taliya identifica o caso e valida os dados principais: falha tecnica foi identificada; severidade esta definida; retry seguro e permitido.
- Meio: A Taliya executa sozinha quando falha tecnica foi identificada; severidade esta definida; retry seguro e permitido; responsavel esta atribuido; log tecnico esta disponivel. Ela chama a equipe quando retry pode duplicar efeito; falha persiste; severidade e alta; provedor esta indisponivel; permissao ou limite bloqueia mitigacao.
- Fim: No caso comum, a acao `tratar falhas, webhooks e retries seguros` fica registrada e auditada. Se houver excecao, criar tarefa/caso em configuracao especifica da integracao; /app/operacao/incidentes e manter auditoria do motivo.
- Ajustes afetados: responsavel; severidade; quando tentar novamente
- Encadeamento: configuracao especifica da integracao; /app/operacao/incidentes

**Autonomo** (bloqueado)

- Inicio: Este modo fica bloqueado para Falhas/webhooks.
- Meio: A Taliya nao conclui end-to-end porque este modo esta acima do teto do fluxo.
- Fim: Use o maior modo habilitado para automatizar o caso comum sem ultrapassar os limites publicados.
- Ajustes afetados: responsavel; severidade; quando tentar novamente
- Encadeamento: configuracao especifica da integracao; /app/operacao/incidentes


#### Importacao/migracao

**Manual** (habilitado)

- Inicio: O fluxo comeca quando surge um caso para preparar importacao ou migracao para aprovacao. A Taliya identifica o caso e organiza o contexto principal: lote foi identificado; amostra foi validada; impacto em dados foi resumido.
- Meio: A Taliya cria tarefa, checklist ou caso para a equipe preparar importacao ou migracao para aprovacao. A decisao e a execucao principal ficam com o humano.
- Fim: O fluxo termina quando a equipe registra o resultado. A Taliya salva auditoria e, se nao puder seguir, criar tarefa/caso em /app/importacao/[jobId]; /app/dados/qualidade; aprovacao e manter auditoria do motivo.
- Ajustes afetados: aprovador; lote; responsavel
- Encadeamento: /app/importacao/[jobId]; /app/dados/qualidade; aprovacao

**Copiloto** (habilitado)

- Inicio: O fluxo comeca quando surge um caso para preparar importacao ou migracao para aprovacao. A Taliya identifica o contexto e mostra a base da sugestao: lote foi identificado; amostra foi validada; impacto em dados foi resumido.
- Meio: A Taliya sugere preparar importacao ou migracao para aprovacao, prepara texto/resumo/proximo passo e mostra os dados usados. A equipe pode aceitar, editar ou descartar antes de executar.
- Fim: Se a equipe aceitar, a acao e registrada conforme a decisao humana. Se editar ou descartar, a Taliya registra a decisao e mantem continuidade em /app/importacao/[jobId]; /app/dados/qualidade; aprovacao.
- Ajustes afetados: aprovador; lote; responsavel
- Encadeamento: /app/importacao/[jobId]; /app/dados/qualidade; aprovacao

**Autonomo com aprovacao** (habilitado)

- Inicio: O fluxo comeca quando surge um caso para preparar importacao ou migracao para aprovacao. A Taliya identifica o caso, confere lote foi identificado; amostra foi validada; impacto em dados foi resumido e prepara a revisao.
- Meio: A Taliya valida lote foi identificado; amostra foi validada; impacto em dados foi resumido; responsavel esta definido e prepara preparar importacao ou migracao para aprovacao. Antes de concluir, mostra impacto/preview e pede aprovacao.
- Fim: Se aprovado, a acao e concluida e auditada. Se recusado, vencido ou incompleto, criar tarefa/caso em /app/importacao/[jobId]; /app/dados/qualidade; aprovacao e manter auditoria do motivo.
- Ajustes afetados: aprovador; lote; responsavel
- Encadeamento: /app/importacao/[jobId]; /app/dados/qualidade; aprovacao

**Autonomo com excecoes** (bloqueado)

- Inicio: Este modo fica bloqueado para Importacao/migracao.
- Meio: A Taliya nao executa com excecoes porque o teto deste fluxo e menor.
- Fim: O usuario deve escolher um modo permitido para este fluxo.
- Ajustes afetados: aprovador; lote; responsavel
- Encadeamento: /app/importacao/[jobId]; /app/dados/qualidade; aprovacao

**Autonomo** (bloqueado)

- Inicio: Este modo fica bloqueado para Importacao/migracao.
- Meio: A Taliya nao conclui end-to-end porque este modo esta acima do teto do fluxo.
- Fim: Use o maior modo habilitado para automatizar o caso comum sem ultrapassar os limites publicados.
- Ajustes afetados: aprovador; lote; responsavel
- Encadeamento: /app/importacao/[jobId]; /app/dados/qualidade; aprovacao


### Rotina: Governanca de agentes


#### Teste de fluxo

**Manual** (habilitado)

- Inicio: O fluxo comeca quando surge um caso para rodar teste de fluxo em simulacao. A Taliya identifica o caso e organiza o contexto principal: cenario de teste foi escolhido; dados de exemplo estao disponiveis; fluxo nao publica acao real.
- Meio: A Taliya cria tarefa, checklist ou caso para a equipe rodar teste de fluxo em simulacao. A decisao e a execucao principal ficam com o humano.
- Fim: O fluxo termina quando a equipe registra o resultado. A Taliya salva auditoria e, se nao puder seguir, criar tarefa/caso em /app/fluxos/[flowId]/simular; /app/fluxos/[flowId] e manter auditoria do motivo.
- Ajustes afetados: exemplos de simulacao; responsavel
- Encadeamento: /app/fluxos/[flowId]/simular; /app/fluxos/[flowId]

**Copiloto** (habilitado)

- Inicio: O fluxo comeca quando surge um caso para rodar teste de fluxo em simulacao. A Taliya identifica o contexto e mostra a base da sugestao: cenario de teste foi escolhido; dados de exemplo estao disponiveis; fluxo nao publica acao real.
- Meio: A Taliya sugere rodar teste de fluxo em simulacao, prepara texto/resumo/proximo passo e mostra os dados usados. A equipe pode aceitar, editar ou descartar antes de executar.
- Fim: Se a equipe aceitar, a acao e registrada conforme a decisao humana. Se editar ou descartar, a Taliya registra a decisao e mantem continuidade em /app/fluxos/[flowId]/simular; /app/fluxos/[flowId].
- Ajustes afetados: exemplos de simulacao; responsavel
- Encadeamento: /app/fluxos/[flowId]/simular; /app/fluxos/[flowId]

**Autonomo com aprovacao** (habilitado)

- Inicio: O fluxo comeca quando surge um caso para rodar teste de fluxo em simulacao. A Taliya identifica o caso, confere cenario de teste foi escolhido; dados de exemplo estao disponiveis; fluxo nao publica acao real e prepara a revisao.
- Meio: A Taliya valida cenario de teste foi escolhido; dados de exemplo estao disponiveis; fluxo nao publica acao real; responsavel por revisao esta definido e prepara rodar teste de fluxo em simulacao. Antes de concluir, mostra impacto/preview e pede aprovacao.
- Fim: Se aprovado, a acao e concluida e auditada. Se recusado, vencido ou incompleto, criar tarefa/caso em /app/fluxos/[flowId]/simular; /app/fluxos/[flowId] e manter auditoria do motivo.
- Ajustes afetados: exemplos de simulacao; responsavel
- Encadeamento: /app/fluxos/[flowId]/simular; /app/fluxos/[flowId]

**Autonomo com excecoes** (habilitado)

- Inicio: O fluxo comeca quando surge um caso para rodar teste de fluxo em simulacao. A Taliya identifica o caso e valida os dados principais: cenario de teste foi escolhido; dados de exemplo estao disponiveis; fluxo nao publica acao real.
- Meio: A Taliya executa sozinha quando cenario de teste foi escolhido; dados de exemplo estao disponiveis; fluxo nao publica acao real; responsavel por revisao esta definido; resultado pode ser salvo. Ela chama a equipe quando cenario usa dado real sensivel; teste tenta publicar acao; resultado falha preflight; fluxo tem dependencia indisponivel; permissao ou cota bloqueia teste.
- Fim: No caso comum, a acao `rodar teste de fluxo em simulacao` fica registrada e auditada. Se houver excecao, criar tarefa/caso em /app/fluxos/[flowId]/simular; /app/fluxos/[flowId] e manter auditoria do motivo.
- Ajustes afetados: exemplos de simulacao; responsavel
- Encadeamento: /app/fluxos/[flowId]/simular; /app/fluxos/[flowId]

**Autonomo** (habilitado)

- Inicio: O fluxo comeca quando surge um caso para rodar teste de fluxo em simulacao. A Taliya identifica o caso e confirma cenario de teste foi escolhido; dados de exemplo estao disponiveis; fluxo nao publica acao real.
- Meio: A Taliya conclui rodar teste de fluxo em simulacao quando cenario de teste foi escolhido; dados de exemplo estao disponiveis; fluxo nao publica acao real; responsavel por revisao esta definido; resultado pode ser salvo. Ela para quando cenario usa dado real sensivel; teste tenta publicar acao; resultado falha preflight; fluxo tem dependencia indisponivel; permissao ou cota bloqueia teste.
- Fim: A acao e concluida, a auditoria fica salva e a continuidade segue em /app/fluxos/[flowId]/simular; /app/fluxos/[flowId]. Se houver bloqueio, criar tarefa/caso em /app/fluxos/[flowId]/simular; /app/fluxos/[flowId] e manter auditoria do motivo.
- Ajustes afetados: exemplos de simulacao; responsavel
- Encadeamento: /app/fluxos/[flowId]/simular; /app/fluxos/[flowId]


#### Incidente de automacao e correcao operacional

**Manual** (habilitado)

- Inicio: O fluxo comeca quando surge um caso para tratar incidente de automacao e correcao operacional. A Taliya identifica o caso e organiza o contexto principal: incidente foi detectado; severidade esta definida; auto-pausa e permitida para o fluxo.
- Meio: A Taliya cria tarefa, checklist ou caso para a equipe tratar incidente de automacao e correcao operacional. A decisao e a execucao principal ficam com o humano.
- Fim: O fluxo termina quando a equipe registra o resultado. A Taliya salva auditoria e, se nao puder seguir, criar tarefa/caso em /app/operacao/incidentes/[incidentId]; /app/fluxos/execucoes/[runId] e manter auditoria do motivo.
- Ajustes afetados: severidade; responsavel; auto-pausa
- Encadeamento: /app/operacao/incidentes/[incidentId]; /app/fluxos/execucoes/[runId]

**Copiloto** (habilitado)

- Inicio: O fluxo comeca quando surge um caso para tratar incidente de automacao e correcao operacional. A Taliya identifica o contexto e mostra a base da sugestao: incidente foi detectado; severidade esta definida; auto-pausa e permitida para o fluxo.
- Meio: A Taliya sugere tratar incidente de automacao e correcao operacional, prepara texto/resumo/proximo passo e mostra os dados usados. A equipe pode aceitar, editar ou descartar antes de executar.
- Fim: Se a equipe aceitar, a acao e registrada conforme a decisao humana. Se editar ou descartar, a Taliya registra a decisao e mantem continuidade em /app/operacao/incidentes/[incidentId]; /app/fluxos/execucoes/[runId].
- Ajustes afetados: severidade; responsavel; auto-pausa
- Encadeamento: /app/operacao/incidentes/[incidentId]; /app/fluxos/execucoes/[runId]

**Autonomo com aprovacao** (habilitado)

- Inicio: O fluxo comeca quando surge um caso para tratar incidente de automacao e correcao operacional. A Taliya identifica o caso, confere incidente foi detectado; severidade esta definida; auto-pausa e permitida para o fluxo e prepara a revisao.
- Meio: A Taliya valida incidente foi detectado; severidade esta definida; auto-pausa e permitida para o fluxo; responsavel esta atribuido e prepara tratar incidente de automacao e correcao operacional. Antes de concluir, mostra impacto/preview e pede aprovacao.
- Fim: Se aprovado, a acao e concluida e auditada. Se recusado, vencido ou incompleto, criar tarefa/caso em /app/operacao/incidentes/[incidentId]; /app/fluxos/execucoes/[runId] e manter auditoria do motivo.
- Ajustes afetados: severidade; responsavel; auto-pausa
- Encadeamento: /app/operacao/incidentes/[incidentId]; /app/fluxos/execucoes/[runId]

**Autonomo com excecoes** (habilitado)

- Inicio: O fluxo comeca quando surge um caso para tratar incidente de automacao e correcao operacional. A Taliya identifica o caso e valida os dados principais: incidente foi detectado; severidade esta definida; auto-pausa e permitida para o fluxo.
- Meio: A Taliya executa sozinha quando incidente foi detectado; severidade esta definida; auto-pausa e permitida para o fluxo; responsavel esta atribuido; execucao relacionada foi encontrada. Ela chama a equipe quando incidente afeta varios fluxos; auto-pausa nao e permitida; correcao exige rollback; falha envolve integracao externa; permissao bloqueia mitigacao.
- Fim: No caso comum, a acao `tratar incidente de automacao e correcao operacional` fica registrada e auditada. Se houver excecao, criar tarefa/caso em /app/operacao/incidentes/[incidentId]; /app/fluxos/execucoes/[runId] e manter auditoria do motivo.
- Ajustes afetados: severidade; responsavel; auto-pausa
- Encadeamento: /app/operacao/incidentes/[incidentId]; /app/fluxos/execucoes/[runId]

**Autonomo** (bloqueado)

- Inicio: Este modo fica bloqueado para Incidente de automacao e correcao operacional.
- Meio: A Taliya nao conclui end-to-end porque este modo esta acima do teto do fluxo.
- Fim: Use o maior modo habilitado para automatizar o caso comum sem ultrapassar os limites publicados.
- Ajustes afetados: severidade; responsavel; auto-pausa
- Encadeamento: /app/operacao/incidentes/[incidentId]; /app/fluxos/execucoes/[runId]


#### Mudanca de politica ou regra operacional

**Manual** (habilitado)

- Inicio: O fluxo comeca quando surge um caso para preparar mudanca de politica ou regra operacional. A Taliya identifica o caso e organiza o contexto principal: politica ou regra foi identificada; data de vigencia esta definida; simulacao de impacto foi feita.
- Meio: A Taliya cria tarefa, checklist ou caso para a equipe preparar mudanca de politica ou regra operacional. A decisao e a execucao principal ficam com o humano.
- Fim: O fluxo termina quando a equipe registra o resultado. A Taliya salva auditoria e, se nao puder seguir, criar tarefa/caso em /app/politicas/[policyId]; /app/aprovacoes; auditoria e manter auditoria do motivo.
- Ajustes afetados: aprovador; data de vigencia; resumo da mudanca
- Encadeamento: /app/politicas/[policyId]; /app/aprovacoes; auditoria

**Copiloto** (habilitado)

- Inicio: O fluxo comeca quando surge um caso para preparar mudanca de politica ou regra operacional. A Taliya identifica o contexto e mostra a base da sugestao: politica ou regra foi identificada; data de vigencia esta definida; simulacao de impacto foi feita.
- Meio: A Taliya sugere preparar mudanca de politica ou regra operacional, prepara texto/resumo/proximo passo e mostra os dados usados. A equipe pode aceitar, editar ou descartar antes de executar.
- Fim: Se a equipe aceitar, a acao e registrada conforme a decisao humana. Se editar ou descartar, a Taliya registra a decisao e mantem continuidade em /app/politicas/[policyId]; /app/aprovacoes; auditoria.
- Ajustes afetados: aprovador; data de vigencia; resumo da mudanca
- Encadeamento: /app/politicas/[policyId]; /app/aprovacoes; auditoria

**Autonomo com aprovacao** (habilitado)

- Inicio: O fluxo comeca quando surge um caso para preparar mudanca de politica ou regra operacional. A Taliya identifica o caso, confere politica ou regra foi identificada; data de vigencia esta definida; simulacao de impacto foi feita e prepara a revisao.
- Meio: A Taliya valida politica ou regra foi identificada; data de vigencia esta definida; simulacao de impacto foi feita; comunicacao interna esta pronta e prepara preparar mudanca de politica ou regra operacional. Antes de concluir, mostra impacto/preview e pede aprovacao.
- Fim: Se aprovado, a acao e concluida e auditada. Se recusado, vencido ou incompleto, criar tarefa/caso em /app/politicas/[policyId]; /app/aprovacoes; auditoria e manter auditoria do motivo.
- Ajustes afetados: aprovador; data de vigencia; resumo da mudanca
- Encadeamento: /app/politicas/[policyId]; /app/aprovacoes; auditoria

**Autonomo com excecoes** (bloqueado)

- Inicio: Este modo fica bloqueado para Mudanca de politica ou regra operacional.
- Meio: A Taliya nao executa com excecoes porque o teto deste fluxo e menor.
- Fim: O usuario deve escolher um modo permitido para este fluxo.
- Ajustes afetados: aprovador; data de vigencia; resumo da mudanca
- Encadeamento: /app/politicas/[policyId]; /app/aprovacoes; auditoria

**Autonomo** (bloqueado)

- Inicio: Este modo fica bloqueado para Mudanca de politica ou regra operacional.
- Meio: A Taliya nao conclui end-to-end porque este modo esta acima do teto do fluxo.
- Fim: Use o maior modo habilitado para automatizar o caso comum sem ultrapassar os limites publicados.
- Ajustes afetados: aprovador; data de vigencia; resumo da mudanca
- Encadeamento: /app/politicas/[policyId]; /app/aprovacoes; auditoria


## Agente: Historico/Evolucao


### Rotina: Aula com contexto


#### Contexto antes aula

**Manual** (habilitado)

- Inicio: O fluxo comeca quando surge um caso para preparar contexto antes da aula para professor. A Taliya identifica o caso e organiza o contexto principal: aula e professor foram identificados; alunos da aula foram listados; visibilidade do historico permite uso.
- Meio: A Taliya cria tarefa, checklist ou caso para a equipe preparar contexto antes da aula para professor. A decisao e a execucao principal ficam com o humano.
- Fim: O fluxo termina quando a equipe registra o resultado. A Taliya salva auditoria e, se nao puder seguir, criar tarefa/caso em /app/professores; /app/aulas/[id]; tarefa e manter auditoria do motivo.
- Ajustes afetados: visibilidade; professor; quando chamar humano
- Encadeamento: /app/professores; /app/aulas/[id]; tarefa

**Copiloto** (habilitado)

- Inicio: O fluxo comeca quando surge um caso para preparar contexto antes da aula para professor. A Taliya identifica o contexto e mostra a base da sugestao: aula e professor foram identificados; alunos da aula foram listados; visibilidade do historico permite uso.
- Meio: A Taliya sugere preparar contexto antes da aula para professor, prepara texto/resumo/proximo passo e mostra os dados usados. A equipe pode aceitar, editar ou descartar antes de executar.
- Fim: Se a equipe aceitar, a acao e registrada conforme a decisao humana. Se editar ou descartar, a Taliya registra a decisao e mantem continuidade em /app/professores; /app/aulas/[id]; tarefa.
- Ajustes afetados: visibilidade; professor; quando chamar humano
- Encadeamento: /app/professores; /app/aulas/[id]; tarefa

**Autonomo com aprovacao** (habilitado)

- Inicio: O fluxo comeca quando surge um caso para preparar contexto antes da aula para professor. A Taliya identifica o caso, confere aula e professor foram identificados; alunos da aula foram listados; visibilidade do historico permite uso e prepara a revisao.
- Meio: A Taliya valida aula e professor foram identificados; alunos da aula foram listados; visibilidade do historico permite uso; contexto nao inclui dado protegido indevido e prepara preparar contexto antes da aula para professor. Antes de concluir, mostra impacto/preview e pede aprovacao.
- Fim: Se aprovado, a acao e concluida e auditada. Se recusado, vencido ou incompleto, criar tarefa/caso em /app/professores; /app/aulas/[id]; tarefa e manter auditoria do motivo.
- Ajustes afetados: visibilidade; professor; quando chamar humano
- Encadeamento: /app/professores; /app/aulas/[id]; tarefa

**Autonomo com excecoes** (habilitado)

- Inicio: O fluxo comeca quando surge um caso para preparar contexto antes da aula para professor. A Taliya identifica o caso e valida os dados principais: aula e professor foram identificados; alunos da aula foram listados; visibilidade do historico permite uso.
- Meio: A Taliya executa sozinha quando aula e professor foram identificados; alunos da aula foram listados; visibilidade do historico permite uso; contexto nao inclui dado protegido indevido; professor pode receber o resumo. Ela chama a equipe quando aluno tem restricao sensivel; professor sem permissao para dado; historico esta incompleto; aula foi alterada; permissao ou cota bloqueia resumo.
- Fim: No caso comum, a acao `preparar contexto antes da aula para professor` fica registrada e auditada. Se houver excecao, criar tarefa/caso em /app/professores; /app/aulas/[id]; tarefa e manter auditoria do motivo.
- Ajustes afetados: visibilidade; professor; quando chamar humano
- Encadeamento: /app/professores; /app/aulas/[id]; tarefa

**Autonomo** (bloqueado)

- Inicio: Este modo fica bloqueado para Contexto antes aula.
- Meio: A Taliya nao conclui end-to-end porque este modo esta acima do teto do fluxo.
- Fim: Use o maior modo habilitado para automatizar o caso comum sem ultrapassar os limites publicados.
- Ajustes afetados: visibilidade; professor; quando chamar humano
- Encadeamento: /app/professores; /app/aulas/[id]; tarefa


#### Observacao pos-aula

**Manual** (habilitado)

- Inicio: O fluxo comeca quando surge um caso para lembrar e organizar observacao pos-aula. A Taliya identifica o caso e organiza o contexto principal: aula terminou; professor foi identificado; tipos de nota permitidos estao definidos.
- Meio: A Taliya cria tarefa, checklist ou caso para a equipe lembrar e organizar observacao pos-aula. A decisao e a execucao principal ficam com o humano.
- Fim: O fluxo termina quando a equipe registra o resultado. A Taliya salva auditoria e, se nao puder seguir, criar tarefa/caso em /app/aulas/[id]; /app/historico; tarefa e manter auditoria do motivo.
- Ajustes afetados: lembrete; professor; tipos de nota
- Encadeamento: /app/aulas/[id]; /app/historico; tarefa

**Copiloto** (habilitado)

- Inicio: O fluxo comeca quando surge um caso para lembrar e organizar observacao pos-aula. A Taliya identifica o contexto e mostra a base da sugestao: aula terminou; professor foi identificado; tipos de nota permitidos estao definidos.
- Meio: A Taliya sugere lembrar e organizar observacao pos-aula, prepara texto/resumo/proximo passo e mostra os dados usados. A equipe pode aceitar, editar ou descartar antes de executar.
- Fim: Se a equipe aceitar, a acao e registrada conforme a decisao humana. Se editar ou descartar, a Taliya registra a decisao e mantem continuidade em /app/aulas/[id]; /app/historico; tarefa.
- Ajustes afetados: lembrete; professor; tipos de nota
- Encadeamento: /app/aulas/[id]; /app/historico; tarefa

**Autonomo com aprovacao** (habilitado)

- Inicio: O fluxo comeca quando surge um caso para lembrar e organizar observacao pos-aula. A Taliya identifica o caso, confere aula terminou; professor foi identificado; tipos de nota permitidos estao definidos e prepara a revisao.
- Meio: A Taliya valida aula terminou; professor foi identificado; tipos de nota permitidos estao definidos; lembrete esta dentro do horario e prepara lembrar e organizar observacao pos-aula. Antes de concluir, mostra impacto/preview e pede aprovacao.
- Fim: Se aprovado, a acao e concluida e auditada. Se recusado, vencido ou incompleto, criar tarefa/caso em /app/aulas/[id]; /app/historico; tarefa e manter auditoria do motivo.
- Ajustes afetados: lembrete; professor; tipos de nota
- Encadeamento: /app/aulas/[id]; /app/historico; tarefa

**Autonomo com excecoes** (habilitado)

- Inicio: O fluxo comeca quando surge um caso para lembrar e organizar observacao pos-aula. A Taliya identifica o caso e valida os dados principais: aula terminou; professor foi identificado; tipos de nota permitidos estao definidos.
- Meio: A Taliya executa sozinha quando aula terminou; professor foi identificado; tipos de nota permitidos estao definidos; lembrete esta dentro do horario; nota ainda nao foi registrada. Ela chama a equipe quando professor nao tem permissao; nota envolve restricao ou cuidado; aula nao foi fechada; aluno teve evento sensivel; canal, cota ou permissao bloqueia lembrete.
- Fim: No caso comum, a acao `lembrar e organizar observacao pos-aula` fica registrada e auditada. Se houver excecao, criar tarefa/caso em /app/aulas/[id]; /app/historico; tarefa e manter auditoria do motivo.
- Ajustes afetados: lembrete; professor; tipos de nota
- Encadeamento: /app/aulas/[id]; /app/historico; tarefa

**Autonomo** (bloqueado)

- Inicio: Este modo fica bloqueado para Observacao pos-aula.
- Meio: A Taliya nao conclui end-to-end porque este modo esta acima do teto do fluxo.
- Fim: Use o maior modo habilitado para automatizar o caso comum sem ultrapassar os limites publicados.
- Ajustes afetados: lembrete; professor; tipos de nota
- Encadeamento: /app/aulas/[id]; /app/historico; tarefa


### Rotina: Historico protegido


#### Restricao/cuidado

**Manual** (habilitado)

- Inicio: O fluxo comeca quando surge um caso para preparar restricao ou cuidado para aprovacao. A Taliya identifica o caso e organiza o contexto principal: aluno foi identificado; restricao ou cuidado foi classificado; visibilidade esta definida.
- Meio: A Taliya cria tarefa, checklist ou caso para a equipe preparar restricao ou cuidado para aprovacao. A decisao e a execucao principal ficam com o humano.
- Fim: O fluxo termina quando a equipe registra o resultado. A Taliya salva auditoria e, se nao puder seguir, criar tarefa/caso em /app/historico; /app/alunos/[id]; caso/aprovacao e manter auditoria do motivo.
- Ajustes afetados: aprovador; visibilidade; dono do caso
- Encadeamento: /app/historico; /app/alunos/[id]; caso/aprovacao

**Copiloto** (habilitado)

- Inicio: O fluxo comeca quando surge um caso para preparar restricao ou cuidado para aprovacao. A Taliya identifica o contexto e mostra a base da sugestao: aluno foi identificado; restricao ou cuidado foi classificado; visibilidade esta definida.
- Meio: A Taliya sugere preparar restricao ou cuidado para aprovacao, prepara texto/resumo/proximo passo e mostra os dados usados. A equipe pode aceitar, editar ou descartar antes de executar.
- Fim: Se a equipe aceitar, a acao e registrada conforme a decisao humana. Se editar ou descartar, a Taliya registra a decisao e mantem continuidade em /app/historico; /app/alunos/[id]; caso/aprovacao.
- Ajustes afetados: aprovador; visibilidade; dono do caso
- Encadeamento: /app/historico; /app/alunos/[id]; caso/aprovacao

**Autonomo com aprovacao** (habilitado)

- Inicio: O fluxo comeca quando surge um caso para preparar restricao ou cuidado para aprovacao. A Taliya identifica o caso, confere aluno foi identificado; restricao ou cuidado foi classificado; visibilidade esta definida e prepara a revisao.
- Meio: A Taliya valida aluno foi identificado; restricao ou cuidado foi classificado; visibilidade esta definida; dono do caso esta atribuido e prepara preparar restricao ou cuidado para aprovacao. Antes de concluir, mostra impacto/preview e pede aprovacao.
- Fim: Se aprovado, a acao e concluida e auditada. Se recusado, vencido ou incompleto, criar tarefa/caso em /app/historico; /app/alunos/[id]; caso/aprovacao e manter auditoria do motivo.
- Ajustes afetados: aprovador; visibilidade; dono do caso
- Encadeamento: /app/historico; /app/alunos/[id]; caso/aprovacao

**Autonomo com excecoes** (bloqueado)

- Inicio: Este modo fica bloqueado para Restricao/cuidado.
- Meio: A Taliya nao executa com excecoes porque o teto deste fluxo e menor.
- Fim: O usuario deve escolher um modo permitido para este fluxo.
- Ajustes afetados: aprovador; visibilidade; dono do caso
- Encadeamento: /app/historico; /app/alunos/[id]; caso/aprovacao

**Autonomo** (bloqueado)

- Inicio: Este modo fica bloqueado para Restricao/cuidado.
- Meio: A Taliya nao conclui end-to-end porque este modo esta acima do teto do fluxo.
- Fim: Use o maior modo habilitado para automatizar o caso comum sem ultrapassar os limites publicados.
- Ajustes afetados: aprovador; visibilidade; dono do caso
- Encadeamento: /app/historico; /app/alunos/[id]; caso/aprovacao


### Rotina: Aula com contexto


#### Objetivo/evolucao

**Manual** (habilitado)

- Inicio: O fluxo comeca quando surge um caso para acompanhar objetivo e evolucao do aluno. A Taliya identifica o caso e organiza o contexto principal: aluno foi identificado; objetivo ou evolucao esta dentro dos tipos permitidos; frequencia de acompanhamento esta definida.
- Meio: A Taliya cria tarefa, checklist ou caso para a equipe acompanhar objetivo e evolucao do aluno. A decisao e a execucao principal ficam com o humano.
- Fim: O fluxo termina quando a equipe registra o resultado. A Taliya salva auditoria e, se nao puder seguir, criar tarefa/caso em /app/alunos/[id]/linha-do-tempo; tarefa e manter auditoria do motivo.
- Ajustes afetados: professor/responsavel; frequencia; quando abrir tarefa
- Encadeamento: /app/alunos/[id]/linha-do-tempo; tarefa

**Copiloto** (habilitado)

- Inicio: O fluxo comeca quando surge um caso para acompanhar objetivo e evolucao do aluno. A Taliya identifica o contexto e mostra a base da sugestao: aluno foi identificado; objetivo ou evolucao esta dentro dos tipos permitidos; frequencia de acompanhamento esta definida.
- Meio: A Taliya sugere acompanhar objetivo e evolucao do aluno, prepara texto/resumo/proximo passo e mostra os dados usados. A equipe pode aceitar, editar ou descartar antes de executar.
- Fim: Se a equipe aceitar, a acao e registrada conforme a decisao humana. Se editar ou descartar, a Taliya registra a decisao e mantem continuidade em /app/alunos/[id]/linha-do-tempo; tarefa.
- Ajustes afetados: professor/responsavel; frequencia; quando abrir tarefa
- Encadeamento: /app/alunos/[id]/linha-do-tempo; tarefa

**Autonomo com aprovacao** (habilitado)

- Inicio: O fluxo comeca quando surge um caso para acompanhar objetivo e evolucao do aluno. A Taliya identifica o caso, confere aluno foi identificado; objetivo ou evolucao esta dentro dos tipos permitidos; frequencia de acompanhamento esta definida e prepara a revisao.
- Meio: A Taliya valida aluno foi identificado; objetivo ou evolucao esta dentro dos tipos permitidos; frequencia de acompanhamento esta definida; professor ou responsavel esta atribuido e prepara acompanhar objetivo e evolucao do aluno. Antes de concluir, mostra impacto/preview e pede aprovacao.
- Fim: Se aprovado, a acao e concluida e auditada. Se recusado, vencido ou incompleto, criar tarefa/caso em /app/alunos/[id]/linha-do-tempo; tarefa e manter auditoria do motivo.
- Ajustes afetados: professor/responsavel; frequencia; quando abrir tarefa
- Encadeamento: /app/alunos/[id]/linha-do-tempo; tarefa

**Autonomo com excecoes** (habilitado)

- Inicio: O fluxo comeca quando surge um caso para acompanhar objetivo e evolucao do aluno. A Taliya identifica o caso e valida os dados principais: aluno foi identificado; objetivo ou evolucao esta dentro dos tipos permitidos; frequencia de acompanhamento esta definida.
- Meio: A Taliya executa sozinha quando aluno foi identificado; objetivo ou evolucao esta dentro dos tipos permitidos; frequencia de acompanhamento esta definida; professor ou responsavel esta atribuido; historico permitido esta disponivel. Ela chama a equipe quando evolucao envolve saude ou restricao; professor sem permissao; dado historico esta conflitante; acao exige contato sensivel; permissao ou cota bloqueia resumo.
- Fim: No caso comum, a acao `acompanhar objetivo e evolucao do aluno` fica registrada e auditada. Se houver excecao, criar tarefa/caso em /app/alunos/[id]/linha-do-tempo; tarefa e manter auditoria do motivo.
- Ajustes afetados: professor/responsavel; frequencia; quando abrir tarefa
- Encadeamento: /app/alunos/[id]/linha-do-tempo; tarefa

**Autonomo** (bloqueado)

- Inicio: Este modo fica bloqueado para Objetivo/evolucao.
- Meio: A Taliya nao conclui end-to-end porque este modo esta acima do teto do fluxo.
- Fim: Use o maior modo habilitado para automatizar o caso comum sem ultrapassar os limites publicados.
- Ajustes afetados: professor/responsavel; frequencia; quando abrir tarefa
- Encadeamento: /app/alunos/[id]/linha-do-tempo; tarefa


### Rotina: Historico protegido


#### Contexto para agente

**Manual** (habilitado)

- Inicio: O fluxo comeca quando surge um caso para preparar contexto permitido para agente. A Taliya identifica o caso e organiza o contexto principal: escopo de dados foi definido; dados permitidos foram listados; objetivo de uso esta claro.
- Meio: A Taliya cria tarefa, checklist ou caso para a equipe preparar contexto permitido para agente. A decisao e a execucao principal ficam com o humano.
- Fim: O fluxo termina quando a equipe registra o resultado. A Taliya salva auditoria e, se nao puder seguir, criar tarefa/caso em /app/historico/permissoes; /app/aprovacoes e manter auditoria do motivo.
- Ajustes afetados: aprovador; dados permitidos; escopo
- Encadeamento: /app/historico/permissoes; /app/aprovacoes

**Copiloto** (habilitado)

- Inicio: O fluxo comeca quando surge um caso para preparar contexto permitido para agente. A Taliya identifica o contexto e mostra a base da sugestao: escopo de dados foi definido; dados permitidos foram listados; objetivo de uso esta claro.
- Meio: A Taliya sugere preparar contexto permitido para agente, prepara texto/resumo/proximo passo e mostra os dados usados. A equipe pode aceitar, editar ou descartar antes de executar.
- Fim: Se a equipe aceitar, a acao e registrada conforme a decisao humana. Se editar ou descartar, a Taliya registra a decisao e mantem continuidade em /app/historico/permissoes; /app/aprovacoes.
- Ajustes afetados: aprovador; dados permitidos; escopo
- Encadeamento: /app/historico/permissoes; /app/aprovacoes

**Autonomo com aprovacao** (habilitado)

- Inicio: O fluxo comeca quando surge um caso para preparar contexto permitido para agente. A Taliya identifica o caso, confere escopo de dados foi definido; dados permitidos foram listados; objetivo de uso esta claro e prepara a revisao.
- Meio: A Taliya valida escopo de dados foi definido; dados permitidos foram listados; objetivo de uso esta claro; aprovador esta definido e prepara preparar contexto permitido para agente. Antes de concluir, mostra impacto/preview e pede aprovacao.
- Fim: Se aprovado, a acao e concluida e auditada. Se recusado, vencido ou incompleto, criar tarefa/caso em /app/historico/permissoes; /app/aprovacoes e manter auditoria do motivo.
- Ajustes afetados: aprovador; dados permitidos; escopo
- Encadeamento: /app/historico/permissoes; /app/aprovacoes

**Autonomo com excecoes** (bloqueado)

- Inicio: Este modo fica bloqueado para Contexto para agente.
- Meio: A Taliya nao executa com excecoes porque o teto deste fluxo e menor.
- Fim: O usuario deve escolher um modo permitido para este fluxo.
- Ajustes afetados: aprovador; dados permitidos; escopo
- Encadeamento: /app/historico/permissoes; /app/aprovacoes

**Autonomo** (bloqueado)

- Inicio: Este modo fica bloqueado para Contexto para agente.
- Meio: A Taliya nao conclui end-to-end porque este modo esta acima do teto do fluxo.
- Fim: Use o maior modo habilitado para automatizar o caso comum sem ultrapassar os limites publicados.
- Ajustes afetados: aprovador; dados permitidos; escopo
- Encadeamento: /app/historico/permissoes; /app/aprovacoes


#### Documentos/anamnese

**Manual** (habilitado)

- Inicio: O fluxo comeca quando surge um caso para preparar documentos ou anamnese para aprovacao. A Taliya identifica o caso e organiza o contexto principal: documento exigido foi identificado; aluno foi identificado; responsavel esta definido.
- Meio: A Taliya cria tarefa, checklist ou caso para a equipe preparar documentos ou anamnese para aprovacao. A decisao e a execucao principal ficam com o humano.
- Fim: O fluxo termina quando a equipe registra o resultado. A Taliya salva auditoria e, se nao puder seguir, criar tarefa/caso em /app/historico/documentos; /app/aprovacoes; tarefa e manter auditoria do motivo.
- Ajustes afetados: aprovador; documentos exigidos; responsavel
- Encadeamento: /app/historico/documentos; /app/aprovacoes; tarefa

**Copiloto** (habilitado)

- Inicio: O fluxo comeca quando surge um caso para preparar documentos ou anamnese para aprovacao. A Taliya identifica o contexto e mostra a base da sugestao: documento exigido foi identificado; aluno foi identificado; responsavel esta definido.
- Meio: A Taliya sugere preparar documentos ou anamnese para aprovacao, prepara texto/resumo/proximo passo e mostra os dados usados. A equipe pode aceitar, editar ou descartar antes de executar.
- Fim: Se a equipe aceitar, a acao e registrada conforme a decisao humana. Se editar ou descartar, a Taliya registra a decisao e mantem continuidade em /app/historico/documentos; /app/aprovacoes; tarefa.
- Ajustes afetados: aprovador; documentos exigidos; responsavel
- Encadeamento: /app/historico/documentos; /app/aprovacoes; tarefa

**Autonomo com aprovacao** (habilitado)

- Inicio: O fluxo comeca quando surge um caso para preparar documentos ou anamnese para aprovacao. A Taliya identifica o caso, confere documento exigido foi identificado; aluno foi identificado; responsavel esta definido e prepara a revisao.
- Meio: A Taliya valida documento exigido foi identificado; aluno foi identificado; responsavel esta definido; visibilidade esta clara e prepara preparar documentos ou anamnese para aprovacao. Antes de concluir, mostra impacto/preview e pede aprovacao.
- Fim: Se aprovado, a acao e concluida e auditada. Se recusado, vencido ou incompleto, criar tarefa/caso em /app/historico/documentos; /app/aprovacoes; tarefa e manter auditoria do motivo.
- Ajustes afetados: aprovador; documentos exigidos; responsavel
- Encadeamento: /app/historico/documentos; /app/aprovacoes; tarefa

**Autonomo com excecoes** (bloqueado)

- Inicio: Este modo fica bloqueado para Documentos/anamnese.
- Meio: A Taliya nao executa com excecoes porque o teto deste fluxo e menor.
- Fim: O usuario deve escolher um modo permitido para este fluxo.
- Ajustes afetados: aprovador; documentos exigidos; responsavel
- Encadeamento: /app/historico/documentos; /app/aprovacoes; tarefa

**Autonomo** (bloqueado)

- Inicio: Este modo fica bloqueado para Documentos/anamnese.
- Meio: A Taliya nao conclui end-to-end porque este modo esta acima do teto do fluxo.
- Fim: Use o maior modo habilitado para automatizar o caso comum sem ultrapassar os limites publicados.
- Ajustes afetados: aprovador; documentos exigidos; responsavel
- Encadeamento: /app/historico/documentos; /app/aprovacoes; tarefa


#### Correcao historico

**Manual** (habilitado)

- Inicio: O fluxo comeca quando surge um caso para preparar correcao de historico para aprovacao. A Taliya identifica o caso e organiza o contexto principal: evento historico foi identificado; motivo obrigatorio foi informado; valor anterior foi preservado.
- Meio: A Taliya cria tarefa, checklist ou caso para a equipe preparar correcao de historico para aprovacao. A decisao e a execucao principal ficam com o humano.
- Fim: O fluxo termina quando a equipe registra o resultado. A Taliya salva auditoria e, se nao puder seguir, criar tarefa/caso em /app/historico; /app/auditoria; aprovacao e manter auditoria do motivo.
- Ajustes afetados: aprovador; motivo obrigatorio; prazo de aprovacao
- Encadeamento: /app/historico; /app/auditoria; aprovacao

**Copiloto** (habilitado)

- Inicio: O fluxo comeca quando surge um caso para preparar correcao de historico para aprovacao. A Taliya identifica o contexto e mostra a base da sugestao: evento historico foi identificado; motivo obrigatorio foi informado; valor anterior foi preservado.
- Meio: A Taliya sugere preparar correcao de historico para aprovacao, prepara texto/resumo/proximo passo e mostra os dados usados. A equipe pode aceitar, editar ou descartar antes de executar.
- Fim: Se a equipe aceitar, a acao e registrada conforme a decisao humana. Se editar ou descartar, a Taliya registra a decisao e mantem continuidade em /app/historico; /app/auditoria; aprovacao.
- Ajustes afetados: aprovador; motivo obrigatorio; prazo de aprovacao
- Encadeamento: /app/historico; /app/auditoria; aprovacao

**Autonomo com aprovacao** (habilitado)

- Inicio: O fluxo comeca quando surge um caso para preparar correcao de historico para aprovacao. A Taliya identifica o caso, confere evento historico foi identificado; motivo obrigatorio foi informado; valor anterior foi preservado e prepara a revisao.
- Meio: A Taliya valida evento historico foi identificado; motivo obrigatorio foi informado; valor anterior foi preservado; impacto da correcao foi mostrado e prepara preparar correcao de historico para aprovacao. Antes de concluir, mostra impacto/preview e pede aprovacao.
- Fim: Se aprovado, a acao e concluida e auditada. Se recusado, vencido ou incompleto, criar tarefa/caso em /app/historico; /app/auditoria; aprovacao e manter auditoria do motivo.
- Ajustes afetados: aprovador; motivo obrigatorio; prazo de aprovacao
- Encadeamento: /app/historico; /app/auditoria; aprovacao

**Autonomo com excecoes** (bloqueado)

- Inicio: Este modo fica bloqueado para Correcao historico.
- Meio: A Taliya nao executa com excecoes porque o teto deste fluxo e menor.
- Fim: O usuario deve escolher um modo permitido para este fluxo.
- Ajustes afetados: aprovador; motivo obrigatorio; prazo de aprovacao
- Encadeamento: /app/historico; /app/auditoria; aprovacao

**Autonomo** (bloqueado)

- Inicio: Este modo fica bloqueado para Correcao historico.
- Meio: A Taliya nao conclui end-to-end porque este modo esta acima do teto do fluxo.
- Fim: Use o maior modo habilitado para automatizar o caso comum sem ultrapassar os limites publicados.
- Ajustes afetados: aprovador; motivo obrigatorio; prazo de aprovacao
- Encadeamento: /app/historico; /app/auditoria; aprovacao


### Rotina: Aula com contexto


#### Repasse entre professores

**Manual** (habilitado)

- Inicio: O fluxo comeca quando surge um caso para preparar repasse entre professores. A Taliya identifica o caso e organiza o contexto principal: professor origem e destino foram identificados; campos do resumo estao definidos; alunos ou aulas relacionados foram listados.
- Meio: A Taliya cria tarefa, checklist ou caso para a equipe preparar repasse entre professores. A decisao e a execucao principal ficam com o humano.
- Fim: O fluxo termina quando a equipe registra o resultado. A Taliya salva auditoria e, se nao puder seguir, criar tarefa/caso em /app/professores; /app/tarefas e manter auditoria do motivo.
- Ajustes afetados: professor destino; campos do resumo; quando chamar humano
- Encadeamento: /app/professores; /app/tarefas

**Copiloto** (habilitado)

- Inicio: O fluxo comeca quando surge um caso para preparar repasse entre professores. A Taliya identifica o contexto e mostra a base da sugestao: professor origem e destino foram identificados; campos do resumo estao definidos; alunos ou aulas relacionados foram listados.
- Meio: A Taliya sugere preparar repasse entre professores, prepara texto/resumo/proximo passo e mostra os dados usados. A equipe pode aceitar, editar ou descartar antes de executar.
- Fim: Se a equipe aceitar, a acao e registrada conforme a decisao humana. Se editar ou descartar, a Taliya registra a decisao e mantem continuidade em /app/professores; /app/tarefas.
- Ajustes afetados: professor destino; campos do resumo; quando chamar humano
- Encadeamento: /app/professores; /app/tarefas

**Autonomo com aprovacao** (habilitado)

- Inicio: O fluxo comeca quando surge um caso para preparar repasse entre professores. A Taliya identifica o caso, confere professor origem e destino foram identificados; campos do resumo estao definidos; alunos ou aulas relacionados foram listados e prepara a revisao.
- Meio: A Taliya valida professor origem e destino foram identificados; campos do resumo estao definidos; alunos ou aulas relacionados foram listados; visibilidade do historico permite repasse e prepara preparar repasse entre professores. Antes de concluir, mostra impacto/preview e pede aprovacao.
- Fim: Se aprovado, a acao e concluida e auditada. Se recusado, vencido ou incompleto, criar tarefa/caso em /app/professores; /app/tarefas e manter auditoria do motivo.
- Ajustes afetados: professor destino; campos do resumo; quando chamar humano
- Encadeamento: /app/professores; /app/tarefas

**Autonomo com excecoes** (habilitado)

- Inicio: O fluxo comeca quando surge um caso para preparar repasse entre professores. A Taliya identifica o caso e valida os dados principais: professor origem e destino foram identificados; campos do resumo estao definidos; alunos ou aulas relacionados foram listados.
- Meio: A Taliya executa sozinha quando professor origem e destino foram identificados; campos do resumo estao definidos; alunos ou aulas relacionados foram listados; visibilidade do historico permite repasse; mensagem interna esta pronta. Ela chama a equipe quando professor destino sem permissao; resumo inclui dado protegido; aula ou professor mudou; contexto esta incompleto; permissao ou cota bloqueia repasse.
- Fim: No caso comum, a acao `preparar repasse entre professores` fica registrada e auditada. Se houver excecao, criar tarefa/caso em /app/professores; /app/tarefas e manter auditoria do motivo.
- Ajustes afetados: professor destino; campos do resumo; quando chamar humano
- Encadeamento: /app/professores; /app/tarefas

**Autonomo** (bloqueado)

- Inicio: Este modo fica bloqueado para Repasse entre professores.
- Meio: A Taliya nao conclui end-to-end porque este modo esta acima do teto do fluxo.
- Fim: Use o maior modo habilitado para automatizar o caso comum sem ultrapassar os limites publicados.
- Ajustes afetados: professor destino; campos do resumo; quando chamar humano
- Encadeamento: /app/professores; /app/tarefas


#### Lembrete professor

**Manual** (habilitado)

- Inicio: O fluxo comeca quando surge um caso para enviar lembrete para professor. A Taliya identifica o caso e organiza o contexto principal: professor foi identificado; horario ou frequencia chegou; destino do lembrete esta definido.
- Meio: A Taliya cria tarefa, checklist ou caso para a equipe enviar lembrete para professor. A decisao e a execucao principal ficam com o humano.
- Fim: O fluxo termina quando a equipe registra o resultado. A Taliya salva auditoria e, se nao puder seguir, criar tarefa/caso em /app/professores; /app/tarefas e manter auditoria do motivo.
- Ajustes afetados: horario; frequencia; destino
- Encadeamento: /app/professores; /app/tarefas

**Copiloto** (habilitado)

- Inicio: O fluxo comeca quando surge um caso para enviar lembrete para professor. A Taliya identifica o contexto e mostra a base da sugestao: professor foi identificado; horario ou frequencia chegou; destino do lembrete esta definido.
- Meio: A Taliya sugere enviar lembrete para professor, prepara texto/resumo/proximo passo e mostra os dados usados. A equipe pode aceitar, editar ou descartar antes de executar.
- Fim: Se a equipe aceitar, a acao e registrada conforme a decisao humana. Se editar ou descartar, a Taliya registra a decisao e mantem continuidade em /app/professores; /app/tarefas.
- Ajustes afetados: horario; frequencia; destino
- Encadeamento: /app/professores; /app/tarefas

**Autonomo com aprovacao** (habilitado)

- Inicio: O fluxo comeca quando surge um caso para enviar lembrete para professor. A Taliya identifica o caso, confere professor foi identificado; horario ou frequencia chegou; destino do lembrete esta definido e prepara a revisao.
- Meio: A Taliya valida professor foi identificado; horario ou frequencia chegou; destino do lembrete esta definido; conteudo nao inclui dado protegido indevido e prepara enviar lembrete para professor. Antes de concluir, mostra impacto/preview e pede aprovacao.
- Fim: Se aprovado, a acao e concluida e auditada. Se recusado, vencido ou incompleto, criar tarefa/caso em /app/professores; /app/tarefas e manter auditoria do motivo.
- Ajustes afetados: horario; frequencia; destino
- Encadeamento: /app/professores; /app/tarefas

**Autonomo com excecoes** (habilitado)

- Inicio: O fluxo comeca quando surge um caso para enviar lembrete para professor. A Taliya identifica o caso e valida os dados principais: professor foi identificado; horario ou frequencia chegou; destino do lembrete esta definido.
- Meio: A Taliya executa sozinha quando professor foi identificado; horario ou frequencia chegou; destino do lembrete esta definido; conteudo nao inclui dado protegido indevido; lembrete ainda nao foi enviado. Ela chama a equipe quando professor sem canal ou permissao; lembrete duplicado; conteudo depende de dado protegido; aula foi alterada; canal, cota ou permissao bloqueia envio.
- Fim: No caso comum, a acao `enviar lembrete para professor` fica registrada e auditada. Se houver excecao, criar tarefa/caso em /app/professores; /app/tarefas e manter auditoria do motivo.
- Ajustes afetados: horario; frequencia; destino
- Encadeamento: /app/professores; /app/tarefas

**Autonomo** (habilitado)

- Inicio: O fluxo comeca quando surge um caso para enviar lembrete para professor. A Taliya identifica o caso e confirma professor foi identificado; horario ou frequencia chegou; destino do lembrete esta definido.
- Meio: A Taliya conclui enviar lembrete para professor quando professor foi identificado; horario ou frequencia chegou; destino do lembrete esta definido; conteudo nao inclui dado protegido indevido; lembrete ainda nao foi enviado. Ela para quando professor sem canal ou permissao; lembrete duplicado; conteudo depende de dado protegido; aula foi alterada; canal, cota ou permissao bloqueia envio.
- Fim: A acao e concluida, a auditoria fica salva e a continuidade segue em /app/professores; /app/tarefas. Se houver bloqueio, criar tarefa/caso em /app/professores; /app/tarefas e manter auditoria do motivo.
- Ajustes afetados: horario; frequencia; destino
- Encadeamento: /app/professores; /app/tarefas


### Rotina: Historico protegido


#### Compartilhar contexto

**Manual** (habilitado)

- Inicio: O fluxo comeca quando surge um caso para preparar compartilhamento de contexto. A Taliya identifica o caso e organiza o contexto principal: destinatario foi identificado; dados permitidos foram selecionados; objetivo do compartilhamento esta claro.
- Meio: A Taliya cria tarefa, checklist ou caso para a equipe preparar compartilhamento de contexto. A decisao e a execucao principal ficam com o humano.
- Fim: O fluxo termina quando a equipe registra o resultado. A Taliya salva auditoria e, se nao puder seguir, criar tarefa/caso em /app/aprovacoes; /app/conversas/[id] e manter auditoria do motivo.
- Ajustes afetados: aprovador; destinatario; dados permitidos
- Encadeamento: /app/aprovacoes; /app/conversas/[id]

**Copiloto** (habilitado)

- Inicio: O fluxo comeca quando surge um caso para preparar compartilhamento de contexto. A Taliya identifica o contexto e mostra a base da sugestao: destinatario foi identificado; dados permitidos foram selecionados; objetivo do compartilhamento esta claro.
- Meio: A Taliya sugere preparar compartilhamento de contexto, prepara texto/resumo/proximo passo e mostra os dados usados. A equipe pode aceitar, editar ou descartar antes de executar.
- Fim: Se a equipe aceitar, a acao e registrada conforme a decisao humana. Se editar ou descartar, a Taliya registra a decisao e mantem continuidade em /app/aprovacoes; /app/conversas/[id].
- Ajustes afetados: aprovador; destinatario; dados permitidos
- Encadeamento: /app/aprovacoes; /app/conversas/[id]

**Autonomo com aprovacao** (habilitado)

- Inicio: O fluxo comeca quando surge um caso para preparar compartilhamento de contexto. A Taliya identifica o caso, confere destinatario foi identificado; dados permitidos foram selecionados; objetivo do compartilhamento esta claro e prepara a revisao.
- Meio: A Taliya valida destinatario foi identificado; dados permitidos foram selecionados; objetivo do compartilhamento esta claro; preview foi gerado e prepara preparar compartilhamento de contexto. Antes de concluir, mostra impacto/preview e pede aprovacao.
- Fim: Se aprovado, a acao e concluida e auditada. Se recusado, vencido ou incompleto, criar tarefa/caso em /app/aprovacoes; /app/conversas/[id] e manter auditoria do motivo.
- Ajustes afetados: aprovador; destinatario; dados permitidos
- Encadeamento: /app/aprovacoes; /app/conversas/[id]

**Autonomo com excecoes** (bloqueado)

- Inicio: Este modo fica bloqueado para Compartilhar contexto.
- Meio: A Taliya nao executa com excecoes porque o teto deste fluxo e menor.
- Fim: O usuario deve escolher um modo permitido para este fluxo.
- Ajustes afetados: aprovador; destinatario; dados permitidos
- Encadeamento: /app/aprovacoes; /app/conversas/[id]

**Autonomo** (bloqueado)

- Inicio: Este modo fica bloqueado para Compartilhar contexto.
- Meio: A Taliya nao conclui end-to-end porque este modo esta acima do teto do fluxo.
- Fim: Use o maior modo habilitado para automatizar o caso comum sem ultrapassar os limites publicados.
- Ajustes afetados: aprovador; destinatario; dados permitidos
- Encadeamento: /app/aprovacoes; /app/conversas/[id]


#### Permissao historico

**Manual** (habilitado)

- Inicio: O fluxo comeca quando surge um caso para preparar permissao de historico. A Taliya identifica o caso e organiza o contexto principal: papel ou perfil foi identificado; escopo de visibilidade esta definido; impacto foi mostrado.
- Meio: A Taliya cria tarefa, checklist ou caso para a equipe preparar permissao de historico. A decisao e a execucao principal ficam com o humano.
- Fim: O fluxo termina quando a equipe registra o resultado. A Taliya salva auditoria e, se nao puder seguir, criar tarefa/caso em /app/historico/permissoes; /app/configuracoes/permissoes; auditoria e manter auditoria do motivo.
- Ajustes afetados: aprovador; papel; escopo de visibilidade
- Encadeamento: /app/historico/permissoes; /app/configuracoes/permissoes; auditoria

**Copiloto** (habilitado)

- Inicio: O fluxo comeca quando surge um caso para preparar permissao de historico. A Taliya identifica o contexto e mostra a base da sugestao: papel ou perfil foi identificado; escopo de visibilidade esta definido; impacto foi mostrado.
- Meio: A Taliya sugere preparar permissao de historico, prepara texto/resumo/proximo passo e mostra os dados usados. A equipe pode aceitar, editar ou descartar antes de executar.
- Fim: Se a equipe aceitar, a acao e registrada conforme a decisao humana. Se editar ou descartar, a Taliya registra a decisao e mantem continuidade em /app/historico/permissoes; /app/configuracoes/permissoes; auditoria.
- Ajustes afetados: aprovador; papel; escopo de visibilidade
- Encadeamento: /app/historico/permissoes; /app/configuracoes/permissoes; auditoria

**Autonomo com aprovacao** (habilitado)

- Inicio: O fluxo comeca quando surge um caso para preparar permissao de historico. A Taliya identifica o caso, confere papel ou perfil foi identificado; escopo de visibilidade esta definido; impacto foi mostrado e prepara a revisao.
- Meio: A Taliya valida papel ou perfil foi identificado; escopo de visibilidade esta definido; impacto foi mostrado; responsavel esta atribuido e prepara preparar permissao de historico. Antes de concluir, mostra impacto/preview e pede aprovacao.
- Fim: Se aprovado, a acao e concluida e auditada. Se recusado, vencido ou incompleto, criar tarefa/caso em /app/historico/permissoes; /app/configuracoes/permissoes; auditoria e manter auditoria do motivo.
- Ajustes afetados: aprovador; papel; escopo de visibilidade
- Encadeamento: /app/historico/permissoes; /app/configuracoes/permissoes; auditoria

**Autonomo com excecoes** (bloqueado)

- Inicio: Este modo fica bloqueado para Permissao historico.
- Meio: A Taliya nao executa com excecoes porque o teto deste fluxo e menor.
- Fim: O usuario deve escolher um modo permitido para este fluxo.
- Ajustes afetados: aprovador; papel; escopo de visibilidade
- Encadeamento: /app/historico/permissoes; /app/configuracoes/permissoes; auditoria

**Autonomo** (bloqueado)

- Inicio: Este modo fica bloqueado para Permissao historico.
- Meio: A Taliya nao conclui end-to-end porque este modo esta acima do teto do fluxo.
- Fim: Use o maior modo habilitado para automatizar o caso comum sem ultrapassar os limites publicados.
- Ajustes afetados: aprovador; papel; escopo de visibilidade
- Encadeamento: /app/historico/permissoes; /app/configuracoes/permissoes; auditoria


### Rotina: Aula com contexto


#### Linha do tempo

**Manual** (habilitado)

- Inicio: O fluxo comeca quando surge um caso para organizar linha do tempo do aluno. A Taliya identifica o caso e organiza o contexto principal: aluno foi identificado; tipos de evento estao permitidos; filtro padrao esta definido.
- Meio: A Taliya cria tarefa, checklist ou caso para a equipe organizar linha do tempo do aluno. A decisao e a execucao principal ficam com o humano.
- Fim: O fluxo termina quando a equipe registra o resultado. A Taliya salva auditoria e, se nao puder seguir, criar tarefa/caso em /app/alunos/[id]/linha-do-tempo; tarefa e manter auditoria do motivo.
- Ajustes afetados: tipos de evento; filtro padrao; responsavel
- Encadeamento: /app/alunos/[id]/linha-do-tempo; tarefa

**Copiloto** (habilitado)

- Inicio: O fluxo comeca quando surge um caso para organizar linha do tempo do aluno. A Taliya identifica o contexto e mostra a base da sugestao: aluno foi identificado; tipos de evento estao permitidos; filtro padrao esta definido.
- Meio: A Taliya sugere organizar linha do tempo do aluno, prepara texto/resumo/proximo passo e mostra os dados usados. A equipe pode aceitar, editar ou descartar antes de executar.
- Fim: Se a equipe aceitar, a acao e registrada conforme a decisao humana. Se editar ou descartar, a Taliya registra a decisao e mantem continuidade em /app/alunos/[id]/linha-do-tempo; tarefa.
- Ajustes afetados: tipos de evento; filtro padrao; responsavel
- Encadeamento: /app/alunos/[id]/linha-do-tempo; tarefa

**Autonomo com aprovacao** (habilitado)

- Inicio: O fluxo comeca quando surge um caso para organizar linha do tempo do aluno. A Taliya identifica o caso, confere aluno foi identificado; tipos de evento estao permitidos; filtro padrao esta definido e prepara a revisao.
- Meio: A Taliya valida aluno foi identificado; tipos de evento estao permitidos; filtro padrao esta definido; responsavel esta atribuido e prepara organizar linha do tempo do aluno. Antes de concluir, mostra impacto/preview e pede aprovacao.
- Fim: Se aprovado, a acao e concluida e auditada. Se recusado, vencido ou incompleto, criar tarefa/caso em /app/alunos/[id]/linha-do-tempo; tarefa e manter auditoria do motivo.
- Ajustes afetados: tipos de evento; filtro padrao; responsavel
- Encadeamento: /app/alunos/[id]/linha-do-tempo; tarefa

**Autonomo com excecoes** (habilitado)

- Inicio: O fluxo comeca quando surge um caso para organizar linha do tempo do aluno. A Taliya identifica o caso e valida os dados principais: aluno foi identificado; tipos de evento estao permitidos; filtro padrao esta definido.
- Meio: A Taliya executa sozinha quando aluno foi identificado; tipos de evento estao permitidos; filtro padrao esta definido; responsavel esta atribuido; historico pode ser exibido sem dado indevido. Ela chama a equipe quando evento protegido aparece; historico conflita ou esta incompleto; usuario nao tem permissao; filtro mostra dado sensivel; permissao ou cota bloqueia exibicao.
- Fim: No caso comum, a acao `organizar linha do tempo do aluno` fica registrada e auditada. Se houver excecao, criar tarefa/caso em /app/alunos/[id]/linha-do-tempo; tarefa e manter auditoria do motivo.
- Ajustes afetados: tipos de evento; filtro padrao; responsavel
- Encadeamento: /app/alunos/[id]/linha-do-tempo; tarefa

**Autonomo** (bloqueado)

- Inicio: Este modo fica bloqueado para Linha do tempo.
- Meio: A Taliya nao conclui end-to-end porque este modo esta acima do teto do fluxo.
- Fim: Use o maior modo habilitado para automatizar o caso comum sem ultrapassar os limites publicados.
- Ajustes afetados: tipos de evento; filtro padrao; responsavel
- Encadeamento: /app/alunos/[id]/linha-do-tempo; tarefa
