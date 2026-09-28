# Taliya CRM - Revisao Completa Das Regras Por Modo

Status: documento de revisao v0.1.
Data: 2026-05-22.

Este documento e a versao legivel da matriz `agents-flows-detailed-mode-rules-matrix.pt-BR.csv`.
Ele existe para revisar os 96 fluxos sem depender de planilha.

Cada fluxo mostra o que aparece no bloco dinamico `Como funciona neste modo`.
Ajustes do studio continuam limitados ao que realmente muda o comportamento do fluxo.

## Como Ler

- `Modo padrao` e o que aparece primeiro na pagina do fluxo.
- `Teto` e o maximo de autonomia permitido para aquele fluxo.
- Modos marcados como `bloqueado` devem aparecer desabilitados na UI.
- `Ajustes relacionados` sao os controles editaveis daquele fluxo.
- `Requisitos readonly` sao checagens fixas/preflight; nao sao configuracoes do studio.


## Agente: Atendimento


### Rotina: Conversas e triagem

#### Nova conversa

- ID interno: `A1`.
- Modo padrao: `Autonomo com excecoes`.
- Teto: `Autonomo com excecoes`.

**Manual**

A Taliya cria uma tarefa para classificar a conversa, abrir atendimento e mandar para a fila certa; inclui no contexto: mensagem chegou por canal conectado; contato esta identificado ou pode receber resposta geral; assunto inicial foi reconhecido; a equipe executa e registra o resultado.

**Copiloto**

A Taliya sugere classificar a conversa, abrir atendimento e mandar para a fila certa; mostra como base: mensagem chegou por canal conectado; contato esta identificado ou pode receber resposta geral; assunto inicial foi reconhecido; a equipe decide se aceita, edita ou descarta.

**Autonomo com aprovacao**

A Taliya prepara nova conversa, valida: mensagem chegou por canal conectado; contato esta identificado ou pode receber resposta geral; assunto inicial foi reconhecido; fila de atendimento esta definida; depois pede aprovacao antes de concluir.

**Autonomo com excecoes**

Segue sozinho quando:

- mensagem chegou por canal conectado.
- contato esta identificado ou pode receber resposta geral.
- assunto inicial foi reconhecido.
- fila de atendimento esta definida.
- limite de respostas nao foi atingido.

Chama equipe quando:

- contato nao foi identificado.
- mensagem mistura varios assuntos.
- pedido envolve desconto, saude, privacidade ou reclamacao.
- fila de atendimento nao tem responsavel.
- canal, cota, opt-out ou permissao bloqueia resposta.

**Autonomo**

Conclui sozinho quando:

- bloqueado: acima do teto deste fluxo.

Para quando:

- bloqueado: acima do teto deste fluxo.

**Se parar**

criar tarefa/caso em /app/inbox; /app/tarefas; /app/operacao e manter auditoria do motivo.

**Ajustes relacionados**

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

#### Duvidas permitidas

- ID interno: `A2`.
- Modo padrao: `Autonomo`.
- Teto: `Autonomo`.

**Manual**

A Taliya cria uma tarefa para responder duvidas permitidas usando a base aprovada; inclui no contexto: pergunta esta na base permitida; resposta nao exige dado sensivel; contato pode receber resposta pelo canal; a equipe executa e registra o resultado.

**Copiloto**

A Taliya sugere responder duvidas permitidas usando a base aprovada; mostra como base: pergunta esta na base permitida; resposta nao exige dado sensivel; contato pode receber resposta pelo canal; a equipe decide se aceita, edita ou descarta.

**Autonomo com aprovacao**

A Taliya prepara duvidas permitidas, valida: pergunta esta na base permitida; resposta nao exige dado sensivel; contato pode receber resposta pelo canal; limite por conversa nao foi atingido; depois pede aprovacao antes de concluir.

**Autonomo com excecoes**

Segue sozinho quando:

- pergunta esta na base permitida.
- resposta nao exige dado sensivel.
- contato pode receber resposta pelo canal.
- limite por conversa nao foi atingido.
- fallback esta definido.

Chama equipe quando:

- pergunta nao esta na base.
- aluno pede condicao comercial especial.
- mensagem pede dado privado.
- conversa ficou confusa ou agressiva.
- canal, cota, opt-out ou permissao bloqueia resposta.

**Autonomo**

Conclui sozinho quando:

- pergunta esta na base permitida.
- resposta nao exige dado sensivel.
- contato pode receber resposta pelo canal.
- limite por conversa nao foi atingido.
- fallback esta definido.
- nenhuma regra exige aprovacao ou chamada humana.

Para quando:

- pergunta nao esta na base.
- aluno pede condicao comercial especial.
- mensagem pede dado privado.
- conversa ficou confusa ou agressiva.
- canal, cota, opt-out ou permissao bloqueia resposta.
- canal, permissao, cota, opt-out, integracao ou incidente bloqueia a conclusao.

**Se parar**

criar tarefa/caso em /app/inbox; tarefa de resposta e manter auditoria do motivo.

**Ajustes relacionados**

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

#### Aluno existente

- ID interno: `A3`.
- Modo padrao: `Autonomo com excecoes`.
- Teto: `Autonomo com excecoes`.

**Manual**

A Taliya cria uma tarefa para reconhecer aluno existente e encaminhar atendimento com contexto; inclui no contexto: telefone corresponde a um aluno ou responsavel permitido; cadastro nao tem conflito de identidade; pedido usa dados permitidos; a equipe executa e registra o resultado.

**Copiloto**

A Taliya sugere reconhecer aluno existente e encaminhar atendimento com contexto; mostra como base: telefone corresponde a um aluno ou responsavel permitido; cadastro nao tem conflito de identidade; pedido usa dados permitidos; a equipe decide se aceita, edita ou descarta.

**Autonomo com aprovacao**

A Taliya prepara aluno existente, valida: telefone corresponde a um aluno ou responsavel permitido; cadastro nao tem conflito de identidade; pedido usa dados permitidos; fila destino esta definida; depois pede aprovacao antes de concluir.

**Autonomo com excecoes**

Segue sozinho quando:

- telefone corresponde a um aluno ou responsavel permitido.
- cadastro nao tem conflito de identidade.
- pedido usa dados permitidos.
- fila destino esta definida.
- botao de ajuda permanece disponivel.

Chama equipe quando:

- telefone atende mais de um aluno.
- cadastro esta duplicado.
- pedido exige alteracao sensivel.
- aluno contesta informacao do CRM.
- canal, cota ou permissao bloqueia acao.

**Autonomo**

Conclui sozinho quando:

- bloqueado: acima do teto deste fluxo.

Para quando:

- bloqueado: acima do teto deste fluxo.

**Se parar**

criar tarefa/caso em /app/inbox; /app/alunos/[id]; /app/tarefas e manter auditoria do motivo.

**Ajustes relacionados**

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

#### Fora do escopo

- ID interno: `A4`.
- Modo padrao: `Autonomo`.
- Teto: `Autonomo`.

**Manual**

A Taliya cria uma tarefa para responder fora de escopo e criar destino correto; inclui no contexto: assunto nao pertence ao CRM do studio; resposta padrao esta aprovada; contato nao pediu humano; a equipe executa e registra o resultado.

**Copiloto**

A Taliya sugere responder fora de escopo e criar destino correto; mostra como base: assunto nao pertence ao CRM do studio; resposta padrao esta aprovada; contato nao pediu humano; a equipe decide se aceita, edita ou descarta.

**Autonomo com aprovacao**

A Taliya prepara fora do escopo, valida: assunto nao pertence ao CRM do studio; resposta padrao esta aprovada; contato nao pediu humano; destino da tarefa ou caso esta definido; depois pede aprovacao antes de concluir.

**Autonomo com excecoes**

Segue sozinho quando:

- assunto nao pertence ao CRM do studio.
- resposta padrao esta aprovada.
- contato nao pediu humano.
- destino da tarefa ou caso esta definido.
- mensagem nao contem risco sensivel.

Chama equipe quando:

- assunto parece reclamacao.
- mensagem envolve emergencia, saude ou dado pessoal.
- lead ou aluno insiste em humano.
- resposta padrao nao cobre o caso.
- canal, cota ou permissao bloqueia acao.

**Autonomo**

Conclui sozinho quando:

- assunto nao pertence ao CRM do studio.
- resposta padrao esta aprovada.
- contato nao pediu humano.
- destino da tarefa ou caso esta definido.
- mensagem nao contem risco sensivel.
- nenhuma regra exige aprovacao ou chamada humana.

Para quando:

- assunto parece reclamacao.
- mensagem envolve emergencia, saude ou dado pessoal.
- lead ou aluno insiste em humano.
- resposta padrao nao cobre o caso.
- canal, cota ou permissao bloqueia acao.
- canal, permissao, cota, opt-out, integracao ou incidente bloqueia a conclusao.

**Se parar**

criar tarefa/caso em /app/inbox; tarefa/caso e manter auditoria do motivo.

**Ajustes relacionados**

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

#### Chamada humana

- ID interno: `A5`.
- Modo padrao: `Autonomo`.
- Teto: `Autonomo`.

**Manual**

A Taliya cria uma tarefa para chamar humano com resumo, fila e prioridade; inclui no contexto: gatilho de humano foi detectado; fila destino esta definida; prioridade foi calculada; a equipe executa e registra o resultado.

**Copiloto**

A Taliya sugere chamar humano com resumo, fila e prioridade; mostra como base: gatilho de humano foi detectado; fila destino esta definida; prioridade foi calculada; a equipe decide se aceita, edita ou descarta.

**Autonomo com aprovacao**

A Taliya prepara chamada humana, valida: gatilho de humano foi detectado; fila destino esta definida; prioridade foi calculada; resumo obrigatorio foi gerado; depois pede aprovacao antes de concluir.

**Autonomo com excecoes**

Segue sozinho quando:

- gatilho de humano foi detectado.
- fila destino esta definida.
- prioridade foi calculada.
- resumo obrigatorio foi gerado.
- responsavel pode assumir o caso.

Chama equipe quando:

- fila destino nao existe.
- prioridade nao pode ser definida.
- resumo ficou incompleto.
- caso exige dono ou admin especifico.
- canal, cota ou permissao bloqueia criacao.

**Autonomo**

Conclui sozinho quando:

- gatilho de humano foi detectado.
- fila destino esta definida.
- prioridade foi calculada.
- resumo obrigatorio foi gerado.
- responsavel pode assumir o caso.
- nenhuma regra exige aprovacao ou chamada humana.

Para quando:

- fila destino nao existe.
- prioridade nao pode ser definida.
- resumo ficou incompleto.
- caso exige dono ou admin especifico.
- canal, cota ou permissao bloqueia criacao.
- canal, permissao, cota, opt-out, integracao ou incidente bloqueia a conclusao.

**Se parar**

criar tarefa/caso em /app/inbox; /app/operacao; fila humana e manter auditoria do motivo.

**Ajustes relacionados**

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


### Rotina: Identidade e privacidade

#### Consentimento/opt-out

- ID interno: `A6`.
- Modo padrao: `Autonomo`.
- Teto: `Autonomo`.

**Manual**

A Taliya cria uma tarefa para registrar consentimento, opt-out ou preferencia de contato; inclui no contexto: contato foi identificado; pedido de consentimento ou opt-out e claro; texto de confirmacao esta aprovado; a equipe executa e registra o resultado.

**Copiloto**

A Taliya sugere registrar consentimento, opt-out ou preferencia de contato; mostra como base: contato foi identificado; pedido de consentimento ou opt-out e claro; texto de confirmacao esta aprovado; a equipe decide se aceita, edita ou descarta.

**Autonomo com aprovacao**

A Taliya prepara consentimento/opt-out, valida: contato foi identificado; pedido de consentimento ou opt-out e claro; texto de confirmacao esta aprovado; responsavel de revisao existe para caso ambiguo; depois pede aprovacao antes de concluir.

**Autonomo com excecoes**

Segue sozinho quando:

- contato foi identificado.
- pedido de consentimento ou opt-out e claro.
- texto de confirmacao esta aprovado.
- responsavel de revisao existe para caso ambiguo.
- auditoria pode ser registrada.

Chama equipe quando:

- pedido e ambiguo.
- telefone e compartilhado.
- contato pede exclusao ou copia de dados.
- ha conflito entre responsavel e aluno.
- canal, cota ou permissao bloqueia confirmacao.

**Autonomo**

Conclui sozinho quando:

- contato foi identificado.
- pedido de consentimento ou opt-out e claro.
- texto de confirmacao esta aprovado.
- responsavel de revisao existe para caso ambiguo.
- auditoria pode ser registrada.
- nenhuma regra exige aprovacao ou chamada humana.

Para quando:

- pedido e ambiguo.
- telefone e compartilhado.
- contato pede exclusao ou copia de dados.
- ha conflito entre responsavel e aluno.
- canal, cota ou permissao bloqueia confirmacao.
- canal, permissao, cota, opt-out, integracao ou incidente bloqueia a conclusao.

**Se parar**

criar tarefa/caso em /app/contatos/[id]; auditoria; tarefa e manter auditoria do motivo.

**Ajustes relacionados**

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

#### Identidade/midias

- ID interno: `A7`.
- Modo padrao: `Autonomo com excecoes`.
- Teto: `Autonomo com excecoes`.

**Manual**

A Taliya cria uma tarefa para tratar identidade, audio, imagem ou midia recebida; inclui no contexto: midia e legivel; tipo de midia e aceito; contato esta identificado; a equipe executa e registra o resultado.

**Copiloto**

A Taliya sugere tratar identidade, audio, imagem ou midia recebida; mostra como base: midia e legivel; tipo de midia e aceito; contato esta identificado; a equipe decide se aceita, edita ou descarta.

**Autonomo com aprovacao**

A Taliya prepara identidade/midias, valida: midia e legivel; tipo de midia e aceito; contato esta identificado; conteudo nao traz dado sensivel inesperado; depois pede aprovacao antes de concluir.

**Autonomo com excecoes**

Segue sozinho quando:

- midia e legivel.
- tipo de midia e aceito.
- contato esta identificado.
- conteudo nao traz dado sensivel inesperado.
- responsavel de revisao esta definido.

Chama equipe quando:

- midia esta ilegivel.
- documento parece sensivel.
- identidade nao confere.
- arquivo nao e aceito.
- canal, cota ou permissao bloqueia acao.

**Autonomo**

Conclui sozinho quando:

- bloqueado: acima do teto deste fluxo.

Para quando:

- bloqueado: acima do teto deste fluxo.

**Se parar**

criar tarefa/caso em /app/inbox; /app/dados/duplicidades; /app/historico/documentos e manter auditoria do motivo.

**Ajustes relacionados**

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

#### Privacidade/dados

- ID interno: `A8`.
- Modo padrao: `Autonomo com aprovacao`.
- Teto: `Autonomo com aprovacao`.

**Manual**

A Taliya cria uma tarefa para preparar pedido de privacidade ou dados para aprovacao; inclui no contexto: solicitante foi identificado; tipo de pedido de dado foi classificado; dados envolvidos foram listados; a equipe executa e registra o resultado.

**Copiloto**

A Taliya sugere preparar pedido de privacidade ou dados para aprovacao; mostra como base: solicitante foi identificado; tipo de pedido de dado foi classificado; dados envolvidos foram listados; a equipe decide se aceita, edita ou descarta.

**Autonomo com aprovacao**

A Taliya prepara privacidade/dados, valida: solicitante foi identificado; tipo de pedido de dado foi classificado; dados envolvidos foram listados; SLA do caso esta definido; depois pede aprovacao antes de concluir.

**Autonomo com excecoes**

Segue sozinho quando:

- bloqueado: acima do teto deste fluxo.

Chama equipe quando:

- bloqueado: acima do teto deste fluxo.

**Autonomo**

Conclui sozinho quando:

- bloqueado: acima do teto deste fluxo.

Para quando:

- bloqueado: acima do teto deste fluxo.

**Se parar**

criar tarefa/caso em /app/operacao; /app/auditoria; aprovacao e manter auditoria do motivo.

**Ajustes relacionados**

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

#### Telefone compartilhado e identidade

- ID interno: `A9`.
- Modo padrao: `Autonomo com aprovacao`.
- Teto: `Autonomo com aprovacao`.

**Manual**

A Taliya cria uma tarefa para validar telefone compartilhado antes de expor informacao; inclui no contexto: telefone compartilhado foi detectado; alunos possiveis foram listados; regra de validacao esta definida; a equipe executa e registra o resultado.

**Copiloto**

A Taliya sugere validar telefone compartilhado antes de expor informacao; mostra como base: telefone compartilhado foi detectado; alunos possiveis foram listados; regra de validacao esta definida; a equipe decide se aceita, edita ou descarta.

**Autonomo com aprovacao**

A Taliya prepara telefone compartilhado e identidade, valida: telefone compartilhado foi detectado; alunos possiveis foram listados; regra de validacao esta definida; responsavel de revisao esta definido; depois pede aprovacao antes de concluir.

**Autonomo com excecoes**

Segue sozinho quando:

- bloqueado: acima do teto deste fluxo.

Chama equipe quando:

- bloqueado: acima do teto deste fluxo.

**Autonomo**

Conclui sozinho quando:

- bloqueado: acima do teto deste fluxo.

Para quando:

- bloqueado: acima do teto deste fluxo.

**Se parar**

criar tarefa/caso em /app/contatos; /app/alunos/[id]; /app/dados/duplicidades e manter auditoria do motivo.

**Ajustes relacionados**

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


### Rotina: Conversas e triagem

#### Ciclo de vida/SLA

- ID interno: `A10`.
- Modo padrao: `Autonomo`.
- Teto: `Autonomo`.

**Manual**

A Taliya cria uma tarefa para acompanhar SLA e ciclo de vida do atendimento; inclui no contexto: conversa tem status claro; tempo de SLA esta definido; fila destino existe; a equipe executa e registra o resultado.

**Copiloto**

A Taliya sugere acompanhar SLA e ciclo de vida do atendimento; mostra como base: conversa tem status claro; tempo de SLA esta definido; fila destino existe; a equipe decide se aceita, edita ou descarta.

**Autonomo com aprovacao**

A Taliya prepara ciclo de vida/SLA, valida: conversa tem status claro; tempo de SLA esta definido; fila destino existe; prioridade foi definida; depois pede aprovacao antes de concluir.

**Autonomo com excecoes**

Segue sozinho quando:

- conversa tem status claro.
- tempo de SLA esta definido.
- fila destino existe.
- prioridade foi definida.
- alerta ainda esta dentro da politica do studio.

Chama equipe quando:

- SLA venceu.
- conversa ficou sem dono.
- prioridade ficou alta ou sensivel.
- fila destino nao existe.
- canal, cota ou permissao bloqueia alerta.

**Autonomo**

Conclui sozinho quando:

- conversa tem status claro.
- tempo de SLA esta definido.
- fila destino existe.
- prioridade foi definida.
- alerta ainda esta dentro da politica do studio.
- nenhuma regra exige aprovacao ou chamada humana.

Para quando:

- SLA venceu.
- conversa ficou sem dono.
- prioridade ficou alta ou sensivel.
- fila destino nao existe.
- canal, cota ou permissao bloqueia alerta.
- canal, permissao, cota, opt-out, integracao ou incidente bloqueia a conclusao.

**Se parar**

criar tarefa/caso em /app/inbox; /app/tarefas; /app/hoje e manter auditoria do motivo.

**Ajustes relacionados**

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


## Agente: Agenda


### Rotina: Presenca e faltas

#### Confirmacao de presenca

- ID interno: `B1`.
- Modo padrao: `Autonomo`.
- Teto: `Autonomo`.

**Manual**

A Taliya cria uma tarefa para enviar confirmacao de presenca e registrar resposta; inclui no contexto: aula existe na agenda; aluno esta vinculado a aula; horario do lembrete chegou; a equipe executa e registra o resultado.

**Copiloto**

A Taliya sugere enviar confirmacao de presenca e registrar resposta; mostra como base: aula existe na agenda; aluno esta vinculado a aula; horario do lembrete chegou; a equipe decide se aceita, edita ou descarta.

**Autonomo com aprovacao**

A Taliya prepara confirmacao de presenca, valida: aula existe na agenda; aluno esta vinculado a aula; horario do lembrete chegou; template aprovado esta disponivel; depois pede aprovacao antes de concluir.

**Autonomo com excecoes**

Segue sozinho quando:

- aula existe na agenda.
- aluno esta vinculado a aula.
- horario do lembrete chegou.
- template aprovado esta disponivel.
- limite por aula nao foi atingido.

Chama equipe quando:

- aula foi alterada ou cancelada.
- aluno nao esta identificado.
- ja existe resposta conflitante.
- aluno pede excecao ou troca.
- WhatsApp, cota ou permissao bloqueia envio.

**Autonomo**

Conclui sozinho quando:

- aula existe na agenda.
- aluno esta vinculado a aula.
- horario do lembrete chegou.
- template aprovado esta disponivel.
- limite por aula nao foi atingido.
- nenhuma regra exige aprovacao ou chamada humana.

Para quando:

- aula foi alterada ou cancelada.
- aluno nao esta identificado.
- ja existe resposta conflitante.
- aluno pede excecao ou troca.
- WhatsApp, cota ou permissao bloqueia envio.
- canal, permissao, cota, opt-out, integracao ou incidente bloqueia a conclusao.

**Se parar**

criar tarefa/caso em /app/agenda; /app/aulas/[id]; execucao e manter auditoria do motivo.

**Ajustes relacionados**

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

#### Falta com aviso

- ID interno: `B2`.
- Modo padrao: `Autonomo com excecoes`.
- Teto: `Autonomo com excecoes`.

**Manual**

A Taliya cria uma tarefa para registrar falta avisada e encaminhar o proximo passo; inclui no contexto: aluno foi identificado; aula existe na agenda; aviso chegou ate o prazo configurado; a equipe executa e registra o resultado.

**Copiloto**

A Taliya sugere registrar falta avisada e encaminhar o proximo passo; mostra como base: aluno foi identificado; aula existe na agenda; aviso chegou ate o prazo configurado; a equipe decide se aceita, edita ou descarta.

**Autonomo com aprovacao**

A Taliya prepara falta com aviso, valida: aluno foi identificado; aula existe na agenda; aviso chegou ate o prazo configurado; falta ainda nao foi registrada; depois pede aprovacao antes de concluir.

**Autonomo com excecoes**

Segue sozinho quando:

- aluno foi identificado.
- aula existe na agenda.
- aviso chegou ate o prazo configurado.
- falta ainda nao foi registrada.
- mensagem usa template aprovado.

Chama equipe quando:

- aviso chega fora do prazo.
- nao encontra aluno ou aula.
- falta ja foi registrada.
- aluno pede excecao, credito, cancelamento ou reclama.
- WhatsApp, cota ou permissao bloqueiam o envio.

**Autonomo**

Conclui sozinho quando:

- bloqueado: acima do teto deste fluxo.

Para quando:

- bloqueado: acima do teto deste fluxo.

**Se parar**

criar tarefa/caso em /app/reposicoes; /app/aulas/[id]; tarefa e manter auditoria do motivo.

**Ajustes relacionados**

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

#### Falta sem aviso

- ID interno: `B3`.
- Modo padrao: `Autonomo com excecoes`.
- Teto: `Autonomo com excecoes`.

**Manual**

A Taliya cria uma tarefa para detectar falta sem aviso e abrir recuperacao ou tarefa; inclui no contexto: aula terminou; aluno estava previsto na chamada; presenca nao foi registrada; a equipe executa e registra o resultado.

**Copiloto**

A Taliya sugere detectar falta sem aviso e abrir recuperacao ou tarefa; mostra como base: aula terminou; aluno estava previsto na chamada; presenca nao foi registrada; a equipe decide se aceita, edita ou descarta.

**Autonomo com aprovacao**

A Taliya prepara falta sem aviso, valida: aula terminou; aluno estava previsto na chamada; presenca nao foi registrada; janela de tolerancia passou; depois pede aprovacao antes de concluir.

**Autonomo com excecoes**

Segue sozinho quando:

- aula terminou.
- aluno estava previsto na chamada.
- presenca nao foi registrada.
- janela de tolerancia passou.
- responsavel de acompanhamento esta definido.

Chama equipe quando:

- professor ainda nao fechou chamada.
- aluno avisou por outro canal.
- ha conflito de presenca.
- caso tem recorrencia ou risco de cancelamento.
- canal, cota ou permissao bloqueia contato.

**Autonomo**

Conclui sozinho quando:

- bloqueado: acima do teto deste fluxo.

Para quando:

- bloqueado: acima do teto deste fluxo.

**Se parar**

criar tarefa/caso em /app/aulas/[id]; /app/retencao; tarefa e manter auditoria do motivo.

**Ajustes relacionados**

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


### Rotina: Vagas, reposicoes e lista de espera

#### Recuperar vaga aberta

- ID interno: `B4`.
- Modo padrao: `Autonomo com excecoes`.
- Teto: `Autonomo com excecoes`.

**Manual**

A Taliya cria uma tarefa para usar vaga aberta para convidar aluno elegivel; inclui no contexto: vaga abriu em aula real; prioridade da lista esta definida; aluno elegivel tem credito ou direito; a equipe executa e registra o resultado.

**Copiloto**

A Taliya sugere usar vaga aberta para convidar aluno elegivel; mostra como base: vaga abriu em aula real; prioridade da lista esta definida; aluno elegivel tem credito ou direito; a equipe decide se aceita, edita ou descarta.

**Autonomo com aprovacao**

A Taliya prepara recuperar vaga aberta, valida: vaga abriu em aula real; prioridade da lista esta definida; aluno elegivel tem credito ou direito; limite de convites nao foi atingido; depois pede aprovacao antes de concluir.

**Autonomo com excecoes**

Segue sozinho quando:

- vaga abriu em aula real.
- prioridade da lista esta definida.
- aluno elegivel tem credito ou direito.
- limite de convites nao foi atingido.
- convite usa mensagem aprovada.

Chama equipe quando:

- vaga fecha antes da resposta.
- ha empate ou lote grande.
- aluno nao tem credito claro.
- convite pode furar prioridade.
- canal, cota ou permissao bloqueia envio.

**Autonomo**

Conclui sozinho quando:

- bloqueado: acima do teto deste fluxo.

Para quando:

- bloqueado: acima do teto deste fluxo.

**Se parar**

criar tarefa/caso em /app/lista-espera; /app/reposicoes; aprovacao/tarefa e manter auditoria do motivo.

**Ajustes relacionados**

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

#### Reposicao/remarcacao

- ID interno: `B5`.
- Modo padrao: `Autonomo com aprovacao`.
- Teto: `Autonomo com aprovacao`.

**Manual**

A Taliya cria uma tarefa para preparar reposicao ou remarcacao para aprovacao; inclui no contexto: credito de reposicao existe; aula de destino tem capacidade; prazo da politica esta valido; a equipe executa e registra o resultado.

**Copiloto**

A Taliya sugere preparar reposicao ou remarcacao para aprovacao; mostra como base: credito de reposicao existe; aula de destino tem capacidade; prazo da politica esta valido; a equipe decide se aceita, edita ou descarta.

**Autonomo com aprovacao**

A Taliya prepara reposicao/remarcacao, valida: credito de reposicao existe; aula de destino tem capacidade; prazo da politica esta valido; impacto na agenda foi calculado; depois pede aprovacao antes de concluir.

**Autonomo com excecoes**

Segue sozinho quando:

- bloqueado: acima do teto deste fluxo.

Chama equipe quando:

- bloqueado: acima do teto deste fluxo.

**Autonomo**

Conclui sozinho quando:

- bloqueado: acima do teto deste fluxo.

Para quando:

- bloqueado: acima do teto deste fluxo.

**Se parar**

criar tarefa/caso em /app/reposicoes; /app/agenda; aprovacao e manter auditoria do motivo.

**Ajustes relacionados**

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

#### Lista de espera

- ID interno: `B6`.
- Modo padrao: `Autonomo com excecoes`.
- Teto: `Autonomo com excecoes`.

**Manual**

A Taliya cria uma tarefa para gerenciar lista de espera e convites; inclui no contexto: lista de espera existe; prioridade foi calculada; vaga compativel apareceu; a equipe executa e registra o resultado.

**Copiloto**

A Taliya sugere gerenciar lista de espera e convites; mostra como base: lista de espera existe; prioridade foi calculada; vaga compativel apareceu; a equipe decide se aceita, edita ou descarta.

**Autonomo com aprovacao**

A Taliya prepara lista de espera, valida: lista de espera existe; prioridade foi calculada; vaga compativel apareceu; limite de convites permite contato; depois pede aprovacao antes de concluir.

**Autonomo com excecoes**

Segue sozinho quando:

- lista de espera existe.
- prioridade foi calculada.
- vaga compativel apareceu.
- limite de convites permite contato.
- responsavel por excecao esta definido.

Chama equipe quando:

- prioridade empata.
- aluno nao responde no prazo.
- vaga deixa de existir.
- pedido envolve excecao de credito.
- canal, cota ou permissao bloqueia envio.

**Autonomo**

Conclui sozinho quando:

- bloqueado: acima do teto deste fluxo.

Para quando:

- bloqueado: acima do teto deste fluxo.

**Se parar**

criar tarefa/caso em /app/lista-espera; /app/tarefas e manter auditoria do motivo.

**Ajustes relacionados**

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


### Rotina: Agenda experimental

#### Disponibilidade experimental

- ID interno: `B7`.
- Modo padrao: `Autonomo com excecoes`.
- Teto: `Autonomo com excecoes`.

**Manual**

A Taliya cria uma tarefa para oferecer disponibilidade para aula experimental; inclui no contexto: interessado esta identificado; horarios oferecidos estao livres; responsavel comercial esta definido; a equipe executa e registra o resultado.

**Copiloto**

A Taliya sugere oferecer disponibilidade para aula experimental; mostra como base: interessado esta identificado; horarios oferecidos estao livres; responsavel comercial esta definido; a equipe decide se aceita, edita ou descarta.

**Autonomo com aprovacao**

A Taliya prepara disponibilidade experimental, valida: interessado esta identificado; horarios oferecidos estao livres; responsavel comercial esta definido; limite de tentativas nao foi atingido; depois pede aprovacao antes de concluir.

**Autonomo com excecoes**

Segue sozinho quando:

- interessado esta identificado.
- horarios oferecidos estao livres.
- responsavel comercial esta definido.
- limite de tentativas nao foi atingido.
- mensagem aprovada esta disponivel.

Chama equipe quando:

- interessado pede horario fora da regra.
- nao ha vaga compativel.
- lead ja tem experimental marcada.
- pedido envolve desconto ou excecao.
- canal, cota ou permissao bloqueia envio.

**Autonomo**

Conclui sozinho quando:

- bloqueado: acima do teto deste fluxo.

Para quando:

- bloqueado: acima do teto deste fluxo.

**Se parar**

criar tarefa/caso em /app/experimental; /app/agenda; tarefa e manter auditoria do motivo.

**Ajustes relacionados**

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


### Rotina: Grade e capacidade

#### Mudanca horario fixo

- ID interno: `B8`.
- Modo padrao: `Autonomo com aprovacao`.
- Teto: `Autonomo com aprovacao`.

**Manual**

A Taliya cria uma tarefa para preparar mudanca de horario fixo para aprovacao; inclui no contexto: aluno e horario fixo foram identificados; novo horario existe; impacto em turma e capacidade foi calculado; a equipe executa e registra o resultado.

**Copiloto**

A Taliya sugere preparar mudanca de horario fixo para aprovacao; mostra como base: aluno e horario fixo foram identificados; novo horario existe; impacto em turma e capacidade foi calculado; a equipe decide se aceita, edita ou descarta.

**Autonomo com aprovacao**

A Taliya prepara mudanca horario fixo, valida: aluno e horario fixo foram identificados; novo horario existe; impacto em turma e capacidade foi calculado; mensagem de confirmacao esta pronta; depois pede aprovacao antes de concluir.

**Autonomo com excecoes**

Segue sozinho quando:

- bloqueado: acima do teto deste fluxo.

Chama equipe quando:

- bloqueado: acima do teto deste fluxo.

**Autonomo**

Conclui sozinho quando:

- bloqueado: acima do teto deste fluxo.

Para quando:

- bloqueado: acima do teto deste fluxo.

**Se parar**

criar tarefa/caso em /app/alunos/[id]; /app/agenda; aprovacao e manter auditoria do motivo.

**Ajustes relacionados**

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

#### Cancelamento pelo studio

- ID interno: `B9`.
- Modo padrao: `Autonomo com aprovacao`.
- Teto: `Autonomo com aprovacao`.

**Manual**

A Taliya cria uma tarefa para preparar cancelamento pelo studio e comunicado; inclui no contexto: aula a cancelar existe; motivo foi informado; alunos afetados foram listados; a equipe executa e registra o resultado.

**Copiloto**

A Taliya sugere preparar cancelamento pelo studio e comunicado; mostra como base: aula a cancelar existe; motivo foi informado; alunos afetados foram listados; a equipe decide se aceita, edita ou descarta.

**Autonomo com aprovacao**

A Taliya prepara cancelamento pelo studio, valida: aula a cancelar existe; motivo foi informado; alunos afetados foram listados; reposicao ou credito foi calculado; depois pede aprovacao antes de concluir.

**Autonomo com excecoes**

Segue sozinho quando:

- bloqueado: acima do teto deste fluxo.

Chama equipe quando:

- bloqueado: acima do teto deste fluxo.

**Autonomo**

Conclui sozinho quando:

- bloqueado: acima do teto deste fluxo.

Para quando:

- bloqueado: acima do teto deste fluxo.

**Se parar**

criar tarefa/caso em /app/aulas/[id]; /app/aprovacoes; /app/hoje e manter auditoria do motivo.

**Ajustes relacionados**

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

#### Conflito capacidade

- ID interno: `B10`.
- Modo padrao: `Autonomo com aprovacao`.
- Teto: `Autonomo com aprovacao`.

**Manual**

A Taliya cria uma tarefa para resolver conflito de capacidade com aprovacao; inclui no contexto: turma ou aula foi identificada; capacidade publicada existe; conflito foi calculado; a equipe executa e registra o resultado.

**Copiloto**

A Taliya sugere resolver conflito de capacidade com aprovacao; mostra como base: turma ou aula foi identificada; capacidade publicada existe; conflito foi calculado; a equipe decide se aceita, edita ou descarta.

**Autonomo com aprovacao**

A Taliya prepara conflito capacidade, valida: turma ou aula foi identificada; capacidade publicada existe; conflito foi calculado; prioridade do caso foi definida; depois pede aprovacao antes de concluir.

**Autonomo com excecoes**

Segue sozinho quando:

- bloqueado: acima do teto deste fluxo.

Chama equipe quando:

- bloqueado: acima do teto deste fluxo.

**Autonomo**

Conclui sozinho quando:

- bloqueado: acima do teto deste fluxo.

Para quando:

- bloqueado: acima do teto deste fluxo.

**Se parar**

criar tarefa/caso em /app/turmas/[id]; /app/agenda; caso operacional e manter auditoria do motivo.

**Ajustes relacionados**

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

#### Ajuste de grade

- ID interno: `B11`.
- Modo padrao: `Autonomo com aprovacao`.
- Teto: `Autonomo com aprovacao`.

**Manual**

A Taliya cria uma tarefa para preparar ajuste de grade e simulacao de impacto; inclui no contexto: mudanca de grade foi descrita; data de vigencia esta definida; impacto em aulas, alunos e professores foi simulado; a equipe executa e registra o resultado.

**Copiloto**

A Taliya sugere preparar ajuste de grade e simulacao de impacto; mostra como base: mudanca de grade foi descrita; data de vigencia esta definida; impacto em aulas, alunos e professores foi simulado; a equipe decide se aceita, edita ou descarta.

**Autonomo com aprovacao**

A Taliya prepara ajuste de grade, valida: mudanca de grade foi descrita; data de vigencia esta definida; impacto em aulas, alunos e professores foi simulado; comunicacao necessaria foi listada; depois pede aprovacao antes de concluir.

**Autonomo com excecoes**

Segue sozinho quando:

- bloqueado: acima do teto deste fluxo.

Chama equipe quando:

- bloqueado: acima do teto deste fluxo.

**Autonomo**

Conclui sozinho quando:

- bloqueado: acima do teto deste fluxo.

Para quando:

- bloqueado: acima do teto deste fluxo.

**Se parar**

criar tarefa/caso em /app/grade; /app/aprovacoes; /app/operacao e manter auditoria do motivo.

**Ajustes relacionados**

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


### Rotina: Agenda experimental

#### Experimental sem comparecimento

- ID interno: `B12`.
- Modo padrao: `Autonomo com excecoes`.
- Teto: `Autonomo com excecoes`.

**Manual**

A Taliya cria uma tarefa para tratar experimental sem comparecimento; inclui no contexto: experimental estava marcada; lead nao compareceu; janela de tolerancia passou; a equipe executa e registra o resultado.

**Copiloto**

A Taliya sugere tratar experimental sem comparecimento; mostra como base: experimental estava marcada; lead nao compareceu; janela de tolerancia passou; a equipe decide se aceita, edita ou descarta.

**Autonomo com aprovacao**

A Taliya prepara experimental sem comparecimento, valida: experimental estava marcada; lead nao compareceu; janela de tolerancia passou; cadencia comercial esta definida; depois pede aprovacao antes de concluir.

**Autonomo com excecoes**

Segue sozinho quando:

- experimental estava marcada.
- lead nao compareceu.
- janela de tolerancia passou.
- cadencia comercial esta definida.
- limite de contato nao foi atingido.

Chama equipe quando:

- lead avisou por outro canal.
- lead pede remarcacao fora da regra.
- nao ha nova vaga compativel.
- lead demonstra objecao sensivel.
- canal, cota ou permissao bloqueia contato.

**Autonomo**

Conclui sozinho quando:

- bloqueado: acima do teto deste fluxo.

Para quando:

- bloqueado: acima do teto deste fluxo.

**Se parar**

criar tarefa/caso em /app/experimental; /app/interessados/[id]; tarefa comercial e manter auditoria do motivo.

**Ajustes relacionados**

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


### Rotina: Vagas, reposicoes e lista de espera

#### Creditos reposicao

- ID interno: `B13`.
- Modo padrao: `Autonomo com aprovacao`.
- Teto: `Autonomo com aprovacao`.

**Manual**

A Taliya cria uma tarefa para preparar credito de reposicao para aprovacao; inclui no contexto: falta ou remarcacao geradora foi identificada; validade proposta esta definida; politica de credito esta publicada; a equipe executa e registra o resultado.

**Copiloto**

A Taliya sugere preparar credito de reposicao para aprovacao; mostra como base: falta ou remarcacao geradora foi identificada; validade proposta esta definida; politica de credito esta publicada; a equipe decide se aceita, edita ou descarta.

**Autonomo com aprovacao**

A Taliya prepara creditos reposicao, valida: falta ou remarcacao geradora foi identificada; validade proposta esta definida; politica de credito esta publicada; destino de excecoes esta definido; depois pede aprovacao antes de concluir.

**Autonomo com excecoes**

Segue sozinho quando:

- bloqueado: acima do teto deste fluxo.

Chama equipe quando:

- bloqueado: acima do teto deste fluxo.

**Autonomo**

Conclui sozinho quando:

- bloqueado: acima do teto deste fluxo.

Para quando:

- bloqueado: acima do teto deste fluxo.

**Se parar**

criar tarefa/caso em /app/creditos-reposicao; /app/aprovacoes e manter auditoria do motivo.

**Ajustes relacionados**

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


### Rotina: Presenca e faltas

#### Correcao presenca

- ID interno: `B14`.
- Modo padrao: `Autonomo com aprovacao`.
- Teto: `Autonomo com aprovacao`.

**Manual**

A Taliya cria uma tarefa para preparar correcao de presenca para aprovacao; inclui no contexto: aula e aluno foram identificados; correcao solicitada tem motivo; historico atual foi preservado; a equipe executa e registra o resultado.

**Copiloto**

A Taliya sugere preparar correcao de presenca para aprovacao; mostra como base: aula e aluno foram identificados; correcao solicitada tem motivo; historico atual foi preservado; a equipe decide se aceita, edita ou descarta.

**Autonomo com aprovacao**

A Taliya prepara correcao presenca, valida: aula e aluno foram identificados; correcao solicitada tem motivo; historico atual foi preservado; impacto da alteracao foi mostrado; depois pede aprovacao antes de concluir.

**Autonomo com excecoes**

Segue sozinho quando:

- bloqueado: acima do teto deste fluxo.

Chama equipe quando:

- bloqueado: acima do teto deste fluxo.

**Autonomo**

Conclui sozinho quando:

- bloqueado: acima do teto deste fluxo.

Para quando:

- bloqueado: acima do teto deste fluxo.

**Se parar**

criar tarefa/caso em /app/aulas/[id]/chamada; /app/auditoria; aprovacao e manter auditoria do motivo.

**Ajustes relacionados**

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


### Rotina: Primeira aula e aulas especiais

#### Primeira aula

- ID interno: `B15`.
- Modo padrao: `Autonomo com excecoes`.
- Teto: `Autonomo com excecoes`.

**Manual**

A Taliya cria uma tarefa para acompanhar primeira aula e checklist inicial; inclui no contexto: aluno tem primeira aula identificada; checklist esta definido; professor ou responsavel esta atribuido; a equipe executa e registra o resultado.

**Copiloto**

A Taliya sugere acompanhar primeira aula e checklist inicial; mostra como base: aluno tem primeira aula identificada; checklist esta definido; professor ou responsavel esta atribuido; a equipe decide se aceita, edita ou descarta.

**Autonomo com aprovacao**

A Taliya prepara primeira aula, valida: aluno tem primeira aula identificada; checklist esta definido; professor ou responsavel esta atribuido; orientacoes foram preparadas; depois pede aprovacao antes de concluir.

**Autonomo com excecoes**

Segue sozinho quando:

- aluno tem primeira aula identificada.
- checklist esta definido.
- professor ou responsavel esta atribuido.
- orientacoes foram preparadas.
- nao ha restricao sensivel pendente.

Chama equipe quando:

- aluno tem cuidado sem revisao.
- professor nao esta definido.
- aula muda de horario.
- aluno pede remarcacao ou excecao.
- canal, cota ou permissao bloqueia contato.

**Autonomo**

Conclui sozinho quando:

- bloqueado: acima do teto deste fluxo.

Para quando:

- bloqueado: acima do teto deste fluxo.

**Se parar**

criar tarefa/caso em /app/aulas/[id]; /app/alunos/[id]; checklist/tarefa e manter auditoria do motivo.

**Ajustes relacionados**

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

#### Aula especial/workshop

- ID interno: `B16`.
- Modo padrao: `Autonomo com aprovacao`.
- Teto: `Autonomo com aprovacao`.

**Manual**

A Taliya cria uma tarefa para preparar aula especial ou workshop para aprovacao; inclui no contexto: evento foi descrito; capacidade esta definida; prazo e data estao claros; a equipe executa e registra o resultado.

**Copiloto**

A Taliya sugere preparar aula especial ou workshop para aprovacao; mostra como base: evento foi descrito; capacidade esta definida; prazo e data estao claros; a equipe decide se aceita, edita ou descarta.

**Autonomo com aprovacao**

A Taliya prepara aula especial/workshop, valida: evento foi descrito; capacidade esta definida; prazo e data estao claros; template de comunicacao esta pronto; depois pede aprovacao antes de concluir.

**Autonomo com excecoes**

Segue sozinho quando:

- bloqueado: acima do teto deste fluxo.

Chama equipe quando:

- bloqueado: acima do teto deste fluxo.

**Autonomo**

Conclui sozinho quando:

- bloqueado: acima do teto deste fluxo.

Para quando:

- bloqueado: acima do teto deste fluxo.

**Se parar**

criar tarefa/caso em /app/eventos; /app/aprovacoes; tarefa e manter auditoria do motivo.

**Ajustes relacionados**

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


## Agente: Vendas


### Rotina: Conversao e matricula

#### Valores e planos

- ID interno: `C1`.
- Modo padrao: `Autonomo com excecoes`.
- Teto: `Autonomo com excecoes`.

**Manual**

A Taliya cria uma tarefa para responder sobre valores e planos aprovados; inclui no contexto: plano ou valor esta na base aprovada; lead ou aluno foi identificado quando necessario; nao ha pedido de desconto especial; a equipe executa e registra o resultado.

**Copiloto**

A Taliya sugere responder sobre valores e planos aprovados; mostra como base: plano ou valor esta na base aprovada; lead ou aluno foi identificado quando necessario; nao ha pedido de desconto especial; a equipe decide se aceita, edita ou descarta.

**Autonomo com aprovacao**

A Taliya prepara valores e planos, valida: plano ou valor esta na base aprovada; lead ou aluno foi identificado quando necessario; nao ha pedido de desconto especial; resposta usa template permitido; depois pede aprovacao antes de concluir.

**Autonomo com excecoes**

Segue sozinho quando:

- plano ou valor esta na base aprovada.
- lead ou aluno foi identificado quando necessario.
- nao ha pedido de desconto especial.
- resposta usa template permitido.
- limite de conversa nao foi atingido.

Chama equipe quando:

- lead pede desconto, promessa ou excecao.
- plano nao esta claro.
- pergunta mistura financeiro e contrato.
- resposta pode gerar compromisso comercial.
- canal, cota ou permissao bloqueia resposta.

**Autonomo**

Conclui sozinho quando:

- bloqueado: acima do teto deste fluxo.

Para quando:

- bloqueado: acima do teto deste fluxo.

**Se parar**

criar tarefa/caso em /app/inbox; /app/vendas; tarefa comercial e manter auditoria do motivo.

**Ajustes relacionados**

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


### Rotina: Experimental e acompanhamento

#### Aula experimental

- ID interno: `C2`.
- Modo padrao: `Autonomo com excecoes`.
- Teto: `Autonomo com excecoes`.

**Manual**

A Taliya cria uma tarefa para marcar ou preparar aula experimental; inclui no contexto: lead esta identificado; horarios disponiveis existem; responsavel comercial esta definido; a equipe executa e registra o resultado.

**Copiloto**

A Taliya sugere marcar ou preparar aula experimental; mostra como base: lead esta identificado; horarios disponiveis existem; responsavel comercial esta definido; a equipe decide se aceita, edita ou descarta.

**Autonomo com aprovacao**

A Taliya prepara aula experimental, valida: lead esta identificado; horarios disponiveis existem; responsavel comercial esta definido; limite de tentativas permite contato; depois pede aprovacao antes de concluir.

**Autonomo com excecoes**

Segue sozinho quando:

- lead esta identificado.
- horarios disponiveis existem.
- responsavel comercial esta definido.
- limite de tentativas permite contato.
- lead nao tem experimental duplicada.

Chama equipe quando:

- lead pede horario indisponivel.
- nao ha vaga compativel.
- lead ja fez experimental recente.
- pedido envolve desconto ou excecao.
- canal, cota ou permissao bloqueia contato.

**Autonomo**

Conclui sozinho quando:

- bloqueado: acima do teto deste fluxo.

Para quando:

- bloqueado: acima do teto deste fluxo.

**Se parar**

criar tarefa/caso em /app/experimental; /app/agenda; tarefa e manter auditoria do motivo.

**Ajustes relacionados**

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

#### Lembrete experimental

- ID interno: `C3`.
- Modo padrao: `Autonomo`.
- Teto: `Autonomo`.

**Manual**

A Taliya cria uma tarefa para enviar lembrete de aula experimental; inclui no contexto: experimental esta marcada; horario do lembrete chegou; lead tem canal permitido; a equipe executa e registra o resultado.

**Copiloto**

A Taliya sugere enviar lembrete de aula experimental; mostra como base: experimental esta marcada; horario do lembrete chegou; lead tem canal permitido; a equipe decide se aceita, edita ou descarta.

**Autonomo com aprovacao**

A Taliya prepara lembrete experimental, valida: experimental esta marcada; horario do lembrete chegou; lead tem canal permitido; template aprovado esta disponivel; depois pede aprovacao antes de concluir.

**Autonomo com excecoes**

Segue sozinho quando:

- experimental esta marcada.
- horario do lembrete chegou.
- lead tem canal permitido.
- template aprovado esta disponivel.
- lembrete ainda nao foi enviado.

Chama equipe quando:

- aula foi remarcada ou cancelada.
- lead pediu opt-out.
- canal falhou.
- lead responde com objecao ou pedido de mudanca.
- cota ou permissao bloqueia envio.

**Autonomo**

Conclui sozinho quando:

- experimental esta marcada.
- horario do lembrete chegou.
- lead tem canal permitido.
- template aprovado esta disponivel.
- lembrete ainda nao foi enviado.
- nenhuma regra exige aprovacao ou chamada humana.

Para quando:

- aula foi remarcada ou cancelada.
- lead pediu opt-out.
- canal falhou.
- lead responde com objecao ou pedido de mudanca.
- cota ou permissao bloqueia envio.
- canal, permissao, cota, opt-out, integracao ou incidente bloqueia a conclusao.

**Se parar**

criar tarefa/caso em /app/experimental; execucao; tarefa manual e manter auditoria do motivo.

**Ajustes relacionados**

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

#### Pos-aula experimental

- ID interno: `C4`.
- Modo padrao: `Autonomo com excecoes`.
- Teto: `Autonomo com excecoes`.

**Manual**

A Taliya cria uma tarefa para acompanhar lead depois da aula experimental; inclui no contexto: experimental foi concluida; presenca foi registrada; cadencia pos-aula esta definida; a equipe executa e registra o resultado.

**Copiloto**

A Taliya sugere acompanhar lead depois da aula experimental; mostra como base: experimental foi concluida; presenca foi registrada; cadencia pos-aula esta definida; a equipe decide se aceita, edita ou descarta.

**Autonomo com aprovacao**

A Taliya prepara pos-aula experimental, valida: experimental foi concluida; presenca foi registrada; cadencia pos-aula esta definida; responsavel comercial esta atribuido; depois pede aprovacao antes de concluir.

**Autonomo com excecoes**

Segue sozinho quando:

- experimental foi concluida.
- presenca foi registrada.
- cadencia pos-aula esta definida.
- responsavel comercial esta atribuido.
- limite de contato nao foi atingido.

Chama equipe quando:

- lead nao compareceu.
- professor registrou observacao sensivel.
- lead pede desconto ou condicao especial.
- lead demonstra reclamacao.
- canal, cota ou permissao bloqueia contato.

**Autonomo**

Conclui sozinho quando:

- bloqueado: acima do teto deste fluxo.

Para quando:

- bloqueado: acima do teto deste fluxo.

**Se parar**

criar tarefa/caso em /app/interessados/[id]; /app/vendas; tarefa e manter auditoria do motivo.

**Ajustes relacionados**

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

#### Follow-up comercial

- ID interno: `C5`.
- Modo padrao: `Autonomo com excecoes`.
- Teto: `Autonomo com excecoes`.

**Manual**

A Taliya cria uma tarefa para conduzir follow-up comercial dentro da cadencia; inclui no contexto: lead esta em etapa elegivel; cadencia esta definida; ultima interacao permite novo contato; a equipe executa e registra o resultado.

**Copiloto**

A Taliya sugere conduzir follow-up comercial dentro da cadencia; mostra como base: lead esta em etapa elegivel; cadencia esta definida; ultima interacao permite novo contato; a equipe decide se aceita, edita ou descarta.

**Autonomo com aprovacao**

A Taliya prepara follow-up comercial, valida: lead esta em etapa elegivel; cadencia esta definida; ultima interacao permite novo contato; responsavel comercial esta definido; depois pede aprovacao antes de concluir.

**Autonomo com excecoes**

Segue sozinho quando:

- lead esta em etapa elegivel.
- cadencia esta definida.
- ultima interacao permite novo contato.
- responsavel comercial esta definido.
- limite de tentativas nao foi atingido.

Chama equipe quando:

- lead pediu humano ou parar contato.
- lead tem objecao sensivel.
- lead pede desconto ou garantia.
- conversa esfriou alem do limite.
- canal, cota ou permissao bloqueia contato.

**Autonomo**

Conclui sozinho quando:

- bloqueado: acima do teto deste fluxo.

Para quando:

- bloqueado: acima do teto deste fluxo.

**Se parar**

criar tarefa/caso em /app/vendas; /app/tarefas; /app/inbox e manter auditoria do motivo.

**Ajustes relacionados**

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


### Rotina: Conversao e matricula

#### Pre-matricula

- ID interno: `C6`.
- Modo padrao: `Autonomo com aprovacao`.
- Teto: `Autonomo com aprovacao`.

**Manual**

A Taliya cria uma tarefa para preparar pre-matricula para aprovacao; inclui no contexto: lead aceitou avancar; checklist de matricula esta completo; plano escolhido esta definido; a equipe executa e registra o resultado.

**Copiloto**

A Taliya sugere preparar pre-matricula para aprovacao; mostra como base: lead aceitou avancar; checklist de matricula esta completo; plano escolhido esta definido; a equipe decide se aceita, edita ou descarta.

**Autonomo com aprovacao**

A Taliya prepara pre-matricula, valida: lead aceitou avancar; checklist de matricula esta completo; plano escolhido esta definido; responsavel comercial esta atribuido; depois pede aprovacao antes de concluir.

**Autonomo com excecoes**

Segue sozinho quando:

- bloqueado: acima do teto deste fluxo.

Chama equipe quando:

- bloqueado: acima do teto deste fluxo.

**Autonomo**

Conclui sozinho quando:

- bloqueado: acima do teto deste fluxo.

Para quando:

- bloqueado: acima do teto deste fluxo.

**Se parar**

criar tarefa/caso em /app/matriculas; /app/aprovacoes e manter auditoria do motivo.

**Ajustes relacionados**

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

#### Objecoes

- ID interno: `C7`.
- Modo padrao: `Autonomo com aprovacao`.
- Teto: `Autonomo com aprovacao`.

**Manual**

A Taliya cria uma tarefa para preparar resposta para objecoes comerciais; inclui no contexto: objecao foi classificada; base de respostas cobre o caso; limite de promessa esta definido; a equipe executa e registra o resultado.

**Copiloto**

A Taliya sugere preparar resposta para objecoes comerciais; mostra como base: objecao foi classificada; base de respostas cobre o caso; limite de promessa esta definido; a equipe decide se aceita, edita ou descarta.

**Autonomo com aprovacao**

A Taliya prepara objecoes, valida: objecao foi classificada; base de respostas cobre o caso; limite de promessa esta definido; impacto comercial foi mostrado; depois pede aprovacao antes de concluir.

**Autonomo com excecoes**

Segue sozinho quando:

- bloqueado: acima do teto deste fluxo.

Chama equipe quando:

- bloqueado: acima do teto deste fluxo.

**Autonomo**

Conclui sozinho quando:

- bloqueado: acima do teto deste fluxo.

Para quando:

- bloqueado: acima do teto deste fluxo.

**Se parar**

criar tarefa/caso em /app/conversas/[id]; /app/aprovacoes e manter auditoria do motivo.

**Ajustes relacionados**

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


### Rotina: Captura e qualificacao

#### Origem/qualificacao

- ID interno: `C8`.
- Modo padrao: `Autonomo com excecoes`.
- Teto: `Autonomo com excecoes`.

**Manual**

A Taliya cria uma tarefa para qualificar origem e perfil do lead; inclui no contexto: lead foi identificado; campos obrigatorios foram preenchidos; origem foi reconhecida; a equipe executa e registra o resultado.

**Copiloto**

A Taliya sugere qualificar origem e perfil do lead; mostra como base: lead foi identificado; campos obrigatorios foram preenchidos; origem foi reconhecida; a equipe decide se aceita, edita ou descarta.

**Autonomo com aprovacao**

A Taliya prepara origem/qualificacao, valida: lead foi identificado; campos obrigatorios foram preenchidos; origem foi reconhecida; duplicidade foi verificada; depois pede aprovacao antes de concluir.

**Autonomo com excecoes**

Segue sozinho quando:

- lead foi identificado.
- campos obrigatorios foram preenchidos.
- origem foi reconhecida.
- duplicidade foi verificada.
- responsavel esta definido.

Chama equipe quando:

- lead duplicado.
- origem nao reconhecida.
- campos obrigatorios faltam.
- lead ja esta em outra etapa.
- canal, cota ou permissao bloqueia atualizacao.

**Autonomo**

Conclui sozinho quando:

- bloqueado: acima do teto deste fluxo.

Para quando:

- bloqueado: acima do teto deste fluxo.

**Se parar**

criar tarefa/caso em /app/interessados/[id]; /app/vendas/origens; tarefa e manter auditoria do motivo.

**Ajustes relacionados**

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

#### Perda comercial

- ID interno: `C9`.
- Modo padrao: `Autonomo com aprovacao`.
- Teto: `Autonomo com aprovacao`.

**Manual**

A Taliya cria uma tarefa para preparar perda comercial e motivo; inclui no contexto: lead esta em etapa que permite perda; motivo foi informado; responsavel comercial esta definido; a equipe executa e registra o resultado.

**Copiloto**

A Taliya sugere preparar perda comercial e motivo; mostra como base: lead esta em etapa que permite perda; motivo foi informado; responsavel comercial esta definido; a equipe decide se aceita, edita ou descarta.

**Autonomo com aprovacao**

A Taliya prepara perda comercial, valida: lead esta em etapa que permite perda; motivo foi informado; responsavel comercial esta definido; impacto em relatorio foi calculado; depois pede aprovacao antes de concluir.

**Autonomo com excecoes**

Segue sozinho quando:

- bloqueado: acima do teto deste fluxo.

Chama equipe quando:

- bloqueado: acima do teto deste fluxo.

**Autonomo**

Conclui sozinho quando:

- bloqueado: acima do teto deste fluxo.

Para quando:

- bloqueado: acima do teto deste fluxo.

**Se parar**

criar tarefa/caso em /app/vendas; /app/interessados/[id]; aprovacao/tarefa e manter auditoria do motivo.

**Ajustes relacionados**

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

#### Indicacao

- ID interno: `C10`.
- Modo padrao: `Autonomo com aprovacao`.
- Teto: `Autonomo com aprovacao`.

**Manual**

A Taliya cria uma tarefa para preparar indicacao e beneficio para aprovacao; inclui no contexto: indicador e indicado foram identificados; regra de vinculo esta clara; beneficio permitido foi calculado; a equipe executa e registra o resultado.

**Copiloto**

A Taliya sugere preparar indicacao e beneficio para aprovacao; mostra como base: indicador e indicado foram identificados; regra de vinculo esta clara; beneficio permitido foi calculado; a equipe decide se aceita, edita ou descarta.

**Autonomo com aprovacao**

A Taliya prepara indicacao, valida: indicador e indicado foram identificados; regra de vinculo esta clara; beneficio permitido foi calculado; duplicidade foi verificada; depois pede aprovacao antes de concluir.

**Autonomo com excecoes**

Segue sozinho quando:

- bloqueado: acima do teto deste fluxo.

Chama equipe quando:

- bloqueado: acima do teto deste fluxo.

**Autonomo**

Conclui sozinho quando:

- bloqueado: acima do teto deste fluxo.

Para quando:

- bloqueado: acima do teto deste fluxo.

**Se parar**

criar tarefa/caso em /app/indicacoes; /app/aprovacoes e manter auditoria do motivo.

**Ajustes relacionados**

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


### Rotina: Conversao e matricula

#### Checkout/abandono

- ID interno: `C11`.
- Modo padrao: `Autonomo com excecoes`.
- Teto: `Autonomo com excecoes`.

**Manual**

A Taliya cria uma tarefa para recuperar checkout ou abandono de matricula; inclui no contexto: checkout abandonado foi identificado; cadencia permite contato; responsavel comercial esta definido; a equipe executa e registra o resultado.

**Copiloto**

A Taliya sugere recuperar checkout ou abandono de matricula; mostra como base: checkout abandonado foi identificado; cadencia permite contato; responsavel comercial esta definido; a equipe decide se aceita, edita ou descarta.

**Autonomo com aprovacao**

A Taliya prepara checkout/abandono, valida: checkout abandonado foi identificado; cadencia permite contato; responsavel comercial esta definido; mensagem aprovada esta disponivel; depois pede aprovacao antes de concluir.

**Autonomo com excecoes**

Segue sozinho quando:

- checkout abandonado foi identificado.
- cadencia permite contato.
- responsavel comercial esta definido.
- mensagem aprovada esta disponivel.
- lead nao pediu parar contato.

Chama equipe quando:

- pagamento falhou com motivo financeiro.
- lead pede desconto ou condicao especial.
- checkout esta expirado.
- lead responde com reclamacao.
- canal, cota ou permissao bloqueia contato.

**Autonomo**

Conclui sozinho quando:

- bloqueado: acima do teto deste fluxo.

Para quando:

- bloqueado: acima do teto deste fluxo.

**Se parar**

criar tarefa/caso em /app/checkout-alunos; /app/vendas; tarefa e manter auditoria do motivo.

**Ajustes relacionados**

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


### Rotina: Experimental e acompanhamento

#### Demanda sem vaga

- ID interno: `C12`.
- Modo padrao: `Autonomo com excecoes`.
- Teto: `Autonomo com excecoes`.

**Manual**

A Taliya cria uma tarefa para tratar demanda sem vaga e lista de interesse; inclui no contexto: lead quer horario ou turma sem vaga; lista de espera foi definida; responsavel esta atribuido; a equipe executa e registra o resultado.

**Copiloto**

A Taliya sugere tratar demanda sem vaga e lista de interesse; mostra como base: lead quer horario ou turma sem vaga; lista de espera foi definida; responsavel esta atribuido; a equipe decide se aceita, edita ou descarta.

**Autonomo com aprovacao**

A Taliya prepara demanda sem vaga, valida: lead quer horario ou turma sem vaga; lista de espera foi definida; responsavel esta atribuido; regra de promessa esta clara; depois pede aprovacao antes de concluir.

**Autonomo com excecoes**

Segue sozinho quando:

- lead quer horario ou turma sem vaga.
- lista de espera foi definida.
- responsavel esta atribuido.
- regra de promessa esta clara.
- mensagem nao promete vaga garantida.

Chama equipe quando:

- lead exige prazo ou garantia.
- nao ha alternativa compativel.
- lead e prioridade comercial especial.
- promessa poderia ser indevida.
- canal, cota ou permissao bloqueia contato.

**Autonomo**

Conclui sozinho quando:

- bloqueado: acima do teto deste fluxo.

Para quando:

- bloqueado: acima do teto deste fluxo.

**Se parar**

criar tarefa/caso em /app/vendas; /app/lista-espera; tarefa e manter auditoria do motivo.

**Ajustes relacionados**

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


### Rotina: Conversao e matricula

#### Interessado para aluno

- ID interno: `C13`.
- Modo padrao: `Autonomo com aprovacao`.
- Teto: `Autonomo com aprovacao`.

**Manual**

A Taliya cria uma tarefa para preparar conversao de interessado em aluno; inclui no contexto: interessado esta qualificado; plano escolhido foi definido; checklist de matricula esta completo; a equipe executa e registra o resultado.

**Copiloto**

A Taliya sugere preparar conversao de interessado em aluno; mostra como base: interessado esta qualificado; plano escolhido foi definido; checklist de matricula esta completo; a equipe decide se aceita, edita ou descarta.

**Autonomo com aprovacao**

A Taliya prepara interessado para aluno, valida: interessado esta qualificado; plano escolhido foi definido; checklist de matricula esta completo; cadastro de aluno pode ser criado; depois pede aprovacao antes de concluir.

**Autonomo com excecoes**

Segue sozinho quando:

- bloqueado: acima do teto deste fluxo.

Chama equipe quando:

- bloqueado: acima do teto deste fluxo.

**Autonomo**

Conclui sozinho quando:

- bloqueado: acima do teto deste fluxo.

Para quando:

- bloqueado: acima do teto deste fluxo.

**Se parar**

criar tarefa/caso em /app/matriculas; /app/alunos/[id]; aprovacao e manter auditoria do motivo.

**Ajustes relacionados**

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

#### Upsell/upgrade

- ID interno: `C14`.
- Modo padrao: `Autonomo com aprovacao`.
- Teto: `Autonomo com aprovacao`.

**Manual**

A Taliya cria uma tarefa para preparar proposta de upsell ou upgrade; inclui no contexto: aluno elegivel foi identificado; plano destino esta definido; proposta usa template aprovado; a equipe executa e registra o resultado.

**Copiloto**

A Taliya sugere preparar proposta de upsell ou upgrade; mostra como base: aluno elegivel foi identificado; plano destino esta definido; proposta usa template aprovado; a equipe decide se aceita, edita ou descarta.

**Autonomo com aprovacao**

A Taliya prepara upsell/upgrade, valida: aluno elegivel foi identificado; plano destino esta definido; proposta usa template aprovado; responsavel comercial esta atribuido; depois pede aprovacao antes de concluir.

**Autonomo com excecoes**

Segue sozinho quando:

- bloqueado: acima do teto deste fluxo.

Chama equipe quando:

- bloqueado: acima do teto deste fluxo.

**Autonomo**

Conclui sozinho quando:

- bloqueado: acima do teto deste fluxo.

Para quando:

- bloqueado: acima do teto deste fluxo.

**Se parar**

criar tarefa/caso em /app/alunos/[id]; /app/aprovacoes; /app/vendas e manter auditoria do motivo.

**Ajustes relacionados**

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


### Rotina: Captura e qualificacao

#### Entrada multicanal de lead

- ID interno: `C15`.
- Modo padrao: `Autonomo com excecoes`.
- Teto: `Autonomo com excecoes`.

**Manual**

A Taliya cria uma tarefa para capturar lead de multiplos canais e criar ficha unica; inclui no contexto: fonte e aceita; lead tem contato identificavel; duplicidade foi verificada; a equipe executa e registra o resultado.

**Copiloto**

A Taliya sugere capturar lead de multiplos canais e criar ficha unica; mostra como base: fonte e aceita; lead tem contato identificavel; duplicidade foi verificada; a equipe decide se aceita, edita ou descarta.

**Autonomo com aprovacao**

A Taliya prepara entrada multicanal de lead, valida: fonte e aceita; lead tem contato identificavel; duplicidade foi verificada; dono do lead esta definido; depois pede aprovacao antes de concluir.

**Autonomo com excecoes**

Segue sozinho quando:

- fonte e aceita.
- lead tem contato identificavel.
- duplicidade foi verificada.
- dono do lead esta definido.
- campos minimos foram preenchidos.

Chama equipe quando:

- lead duplicado.
- fonte nao reconhecida.
- contato incompleto.
- lead ja pertence a outro responsavel.
- canal, cota ou permissao bloqueia criacao.

**Autonomo**

Conclui sozinho quando:

- bloqueado: acima do teto deste fluxo.

Para quando:

- bloqueado: acima do teto deste fluxo.

**Se parar**

criar tarefa/caso em /app/vendas/captura; /app/interessados; tarefa e manter auditoria do motivo.

**Ajustes relacionados**

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


## Agente: Financeiro


### Rotina: Lembretes e pagamentos

#### Lembrete vencimento

- ID interno: `D1`.
- Modo padrao: `Autonomo`.
- Teto: `Autonomo`.

**Manual**

A Taliya cria uma tarefa para enviar lembrete de vencimento; inclui no contexto: cobranca existe; vencimento esta proximo conforme horario configurado; aluno tem canal permitido; a equipe executa e registra o resultado.

**Copiloto**

A Taliya sugere enviar lembrete de vencimento; mostra como base: cobranca existe; vencimento esta proximo conforme horario configurado; aluno tem canal permitido; a equipe decide se aceita, edita ou descarta.

**Autonomo com aprovacao**

A Taliya prepara lembrete vencimento, valida: cobranca existe; vencimento esta proximo conforme horario configurado; aluno tem canal permitido; template aprovado esta disponivel; depois pede aprovacao antes de concluir.

**Autonomo com excecoes**

Segue sozinho quando:

- cobranca existe.
- vencimento esta proximo conforme horario configurado.
- aluno tem canal permitido.
- template aprovado esta disponivel.
- limite por cobranca nao foi atingido.

Chama equipe quando:

- cobranca foi paga ou cancelada.
- aluno pediu opt-out.
- valor ou vencimento diverge.
- mensagem falha.
- canal, cota ou permissao bloqueia envio.

**Autonomo**

Conclui sozinho quando:

- cobranca existe.
- vencimento esta proximo conforme horario configurado.
- aluno tem canal permitido.
- template aprovado esta disponivel.
- limite por cobranca nao foi atingido.
- nenhuma regra exige aprovacao ou chamada humana.

Para quando:

- cobranca foi paga ou cancelada.
- aluno pediu opt-out.
- valor ou vencimento diverge.
- mensagem falha.
- canal, cota ou permissao bloqueia envio.
- canal, permissao, cota, opt-out, integracao ou incidente bloqueia a conclusao.

**Se parar**

criar tarefa/caso em /app/financeiro/movimentacoes; execucao; tarefa e manter auditoria do motivo.

**Ajustes relacionados**

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

#### Pagamento atrasado

- ID interno: `D2`.
- Modo padrao: `Autonomo com excecoes`.
- Teto: `Autonomo com excecoes`.

**Manual**

A Taliya cria uma tarefa para tratar pagamento atrasado e abrir cobranca ou tarefa; inclui no contexto: movimentacao esta vencida; tentativas permitem novo contato; fila financeira esta definida; a equipe executa e registra o resultado.

**Copiloto**

A Taliya sugere tratar pagamento atrasado e abrir cobranca ou tarefa; mostra como base: movimentacao esta vencida; tentativas permitem novo contato; fila financeira esta definida; a equipe decide se aceita, edita ou descarta.

**Autonomo com aprovacao**

A Taliya prepara pagamento atrasado, valida: movimentacao esta vencida; tentativas permitem novo contato; fila financeira esta definida; mensagem aprovada esta disponivel; depois pede aprovacao antes de concluir.

**Autonomo com excecoes**

Segue sozinho quando:

- movimentacao esta vencida.
- tentativas permitem novo contato.
- fila financeira esta definida.
- mensagem aprovada esta disponivel.
- nao ha disputa registrada.

Chama equipe quando:

- aluno contesta valor.
- pedido envolve acordo, desconto ou prazo especial.
- pagamento pode ter sido feito.
- provedor apresenta falha.
- canal, cota ou permissao bloqueia contato.

**Autonomo**

Conclui sozinho quando:

- bloqueado: acima do teto deste fluxo.

Para quando:

- bloqueado: acima do teto deste fluxo.

**Se parar**

criar tarefa/caso em /app/financeiro/movimentacoes/[id]; tarefa financeira e manter auditoria do motivo.

**Ajustes relacionados**

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

#### Pix/link

- ID interno: `D3`.
- Modo padrao: `Autonomo com aprovacao`.
- Teto: `Autonomo com aprovacao`.

**Manual**

A Taliya cria uma tarefa para preparar Pix ou link de pagamento para aprovacao; inclui no contexto: movimentacao esta identificada; valor esta dentro do limite; template esta aprovado; a equipe executa e registra o resultado.

**Copiloto**

A Taliya sugere preparar Pix ou link de pagamento para aprovacao; mostra como base: movimentacao esta identificada; valor esta dentro do limite; template esta aprovado; a equipe decide se aceita, edita ou descarta.

**Autonomo com aprovacao**

A Taliya prepara pix/link, valida: movimentacao esta identificada; valor esta dentro do limite; template esta aprovado; provedor financeiro esta ok; depois pede aprovacao antes de concluir.

**Autonomo com excecoes**

Segue sozinho quando:

- bloqueado: acima do teto deste fluxo.

Chama equipe quando:

- bloqueado: acima do teto deste fluxo.

**Autonomo**

Conclui sozinho quando:

- bloqueado: acima do teto deste fluxo.

Para quando:

- bloqueado: acima do teto deste fluxo.

**Se parar**

criar tarefa/caso em /app/financeiro/movimentacoes; /app/aprovacoes e manter auditoria do motivo.

**Ajustes relacionados**

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


### Rotina: Excecoes e documentos financeiros

#### Confirmacao pagamento

- ID interno: `D4`.
- Modo padrao: `Autonomo com aprovacao`.
- Teto: `Autonomo com aprovacao`.

**Manual**

A Taliya cria uma tarefa para preparar confirmacao de pagamento para aprovacao; inclui no contexto: movimentacao foi localizada; evidencia de pagamento foi anexada; valor e aluno conferem; a equipe executa e registra o resultado.

**Copiloto**

A Taliya sugere preparar confirmacao de pagamento para aprovacao; mostra como base: movimentacao foi localizada; evidencia de pagamento foi anexada; valor e aluno conferem; a equipe decide se aceita, edita ou descarta.

**Autonomo com aprovacao**

A Taliya prepara confirmacao pagamento, valida: movimentacao foi localizada; evidencia de pagamento foi anexada; valor e aluno conferem; responsavel financeiro esta definido; depois pede aprovacao antes de concluir.

**Autonomo com excecoes**

Segue sozinho quando:

- bloqueado: acima do teto deste fluxo.

Chama equipe quando:

- bloqueado: acima do teto deste fluxo.

**Autonomo**

Conclui sozinho quando:

- bloqueado: acima do teto deste fluxo.

Para quando:

- bloqueado: acima do teto deste fluxo.

**Se parar**

criar tarefa/caso em /app/financeiro/movimentacoes/[id]; aprovacao e manter auditoria do motivo.

**Ajustes relacionados**

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


### Rotina: Ciclo do plano do aluno

#### Renovacao plano

- ID interno: `D5`.
- Modo padrao: `Autonomo com aprovacao`.
- Teto: `Autonomo com aprovacao`.

**Manual**

A Taliya cria uma tarefa para preparar renovacao de plano; inclui no contexto: plano atual e aluno foram identificados; antecedencia configurada chegou; novo ciclo foi calculado; a equipe executa e registra o resultado.

**Copiloto**

A Taliya sugere preparar renovacao de plano; mostra como base: plano atual e aluno foram identificados; antecedencia configurada chegou; novo ciclo foi calculado; a equipe decide se aceita, edita ou descarta.

**Autonomo com aprovacao**

A Taliya prepara renovacao plano, valida: plano atual e aluno foram identificados; antecedencia configurada chegou; novo ciclo foi calculado; template de renovacao esta aprovado; depois pede aprovacao antes de concluir.

**Autonomo com excecoes**

Segue sozinho quando:

- bloqueado: acima do teto deste fluxo.

Chama equipe quando:

- bloqueado: acima do teto deste fluxo.

**Autonomo**

Conclui sozinho quando:

- bloqueado: acima do teto deste fluxo.

Para quando:

- bloqueado: acima do teto deste fluxo.

**Se parar**

criar tarefa/caso em /app/alunos/[id]; /app/financeiro; aprovacao e manter auditoria do motivo.

**Ajustes relacionados**

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


### Rotina: Excecoes e documentos financeiros

#### Excecoes financeiras

- ID interno: `D6`.
- Modo padrao: `Autonomo com aprovacao`.
- Teto: `Autonomo com aprovacao`.

**Manual**

A Taliya cria uma tarefa para preparar excecao financeira para aprovacao; inclui no contexto: tipo de excecao foi classificado; motivo foi informado; impacto financeiro foi calculado; a equipe executa e registra o resultado.

**Copiloto**

A Taliya sugere preparar excecao financeira para aprovacao; mostra como base: tipo de excecao foi classificado; motivo foi informado; impacto financeiro foi calculado; a equipe decide se aceita, edita ou descarta.

**Autonomo com aprovacao**

A Taliya prepara excecoes financeiras, valida: tipo de excecao foi classificado; motivo foi informado; impacto financeiro foi calculado; prazo do caso esta definido; depois pede aprovacao antes de concluir.

**Autonomo com excecoes**

Segue sozinho quando:

- bloqueado: acima do teto deste fluxo.

Chama equipe quando:

- bloqueado: acima do teto deste fluxo.

**Autonomo**

Conclui sozinho quando:

- bloqueado: acima do teto deste fluxo.

Para quando:

- bloqueado: acima do teto deste fluxo.

**Se parar**

criar tarefa/caso em /app/financeiro/movimentacoes; /app/aprovacoes; caso e manter auditoria do motivo.

**Ajustes relacionados**

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


### Rotina: Lembretes e pagamentos

#### Falha pagamento

- ID interno: `D7`.
- Modo padrao: `Autonomo com excecoes`.
- Teto: `Autonomo com excecoes`.

**Manual**

A Taliya cria uma tarefa para tratar falha de pagamento; inclui no contexto: falha veio do provedor; tentativas permitem novo contato; fila financeira esta definida; a equipe executa e registra o resultado.

**Copiloto**

A Taliya sugere tratar falha de pagamento; mostra como base: falha veio do provedor; tentativas permitem novo contato; fila financeira esta definida; a equipe decide se aceita, edita ou descarta.

**Autonomo com aprovacao**

A Taliya prepara falha pagamento, valida: falha veio do provedor; tentativas permitem novo contato; fila financeira esta definida; mensagem aprovada esta disponivel; depois pede aprovacao antes de concluir.

**Autonomo com excecoes**

Segue sozinho quando:

- falha veio do provedor.
- tentativas permitem novo contato.
- fila financeira esta definida.
- mensagem aprovada esta disponivel.
- nao ha disputa aberta.

Chama equipe quando:

- falha persiste apos tentativas.
- aluno contesta cobranca.
- provedor retorna erro tecnico.
- caso exige bloqueio ou liberacao.
- canal, cota ou permissao bloqueia contato.

**Autonomo**

Conclui sozinho quando:

- bloqueado: acima do teto deste fluxo.

Para quando:

- bloqueado: acima do teto deste fluxo.

**Se parar**

criar tarefa/caso em /app/financeiro/movimentacoes/[id]; tarefa/caso e manter auditoria do motivo.

**Ajustes relacionados**

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

#### Recibo/nota

- ID interno: `D8`.
- Modo padrao: `Autonomo com excecoes`.
- Teto: `Autonomo com excecoes`.

**Manual**

A Taliya cria uma tarefa para emitir ou preparar recibo/nota permitida; inclui no contexto: pagamento foi confirmado; tipo de documento e permitido; dados do aluno conferem; a equipe executa e registra o resultado.

**Copiloto**

A Taliya sugere emitir ou preparar recibo/nota permitida; mostra como base: pagamento foi confirmado; tipo de documento e permitido; dados do aluno conferem; a equipe decide se aceita, edita ou descarta.

**Autonomo com aprovacao**

A Taliya prepara recibo/nota, valida: pagamento foi confirmado; tipo de documento e permitido; dados do aluno conferem; responsavel esta definido; depois pede aprovacao antes de concluir.

**Autonomo com excecoes**

Segue sozinho quando:

- pagamento foi confirmado.
- tipo de documento e permitido.
- dados do aluno conferem.
- responsavel esta definido.
- fallback para tarefa existe.

Chama equipe quando:

- documento nao e permitido.
- dados fiscais faltam.
- pagamento nao esta conciliado.
- aluno pede documento especial.
- permissao ou provedor bloqueia emissao.

**Autonomo**

Conclui sozinho quando:

- bloqueado: acima do teto deste fluxo.

Para quando:

- bloqueado: acima do teto deste fluxo.

**Se parar**

criar tarefa/caso em /app/financeiro/documentos; tarefa e manter auditoria do motivo.

**Ajustes relacionados**

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


### Rotina: Ciclo do plano do aluno

#### Pausa/trancamento

- ID interno: `D9`.
- Modo padrao: `Autonomo com aprovacao`.
- Teto: `Autonomo com aprovacao`.

**Manual**

A Taliya cria uma tarefa para preparar pausa ou trancamento para aprovacao; inclui no contexto: aluno e plano foram identificados; motivo foi informado; impacto em agenda e cobranca foi calculado; a equipe executa e registra o resultado.

**Copiloto**

A Taliya sugere preparar pausa ou trancamento para aprovacao; mostra como base: aluno e plano foram identificados; motivo foi informado; impacto em agenda e cobranca foi calculado; a equipe decide se aceita, edita ou descarta.

**Autonomo com aprovacao**

A Taliya prepara pausa/trancamento, valida: aluno e plano foram identificados; motivo foi informado; impacto em agenda e cobranca foi calculado; prazo esta definido; depois pede aprovacao antes de concluir.

**Autonomo com excecoes**

Segue sozinho quando:

- bloqueado: acima do teto deste fluxo.

Chama equipe quando:

- bloqueado: acima do teto deste fluxo.

**Autonomo**

Conclui sozinho quando:

- bloqueado: acima do teto deste fluxo.

Para quando:

- bloqueado: acima do teto deste fluxo.

**Se parar**

criar tarefa/caso em /app/financeiro; /app/alunos/[id]; aprovacao/caso e manter auditoria do motivo.

**Ajustes relacionados**

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


### Rotina: Lembretes e pagamentos

#### Conciliacao interna

- ID interno: `D10`.
- Modo padrao: `Autonomo com aprovacao`.
- Teto: `Autonomo com aprovacao`.

**Manual**

A Taliya cria uma tarefa para preparar conciliacao interna para aprovacao; inclui no contexto: movimentacao e pagamento candidato foram encontrados; confianca minima foi atingida; responsavel financeiro esta definido; a equipe executa e registra o resultado.

**Copiloto**

A Taliya sugere preparar conciliacao interna para aprovacao; mostra como base: movimentacao e pagamento candidato foram encontrados; confianca minima foi atingida; responsavel financeiro esta definido; a equipe decide se aceita, edita ou descarta.

**Autonomo com aprovacao**

A Taliya prepara conciliacao interna, valida: movimentacao e pagamento candidato foram encontrados; confianca minima foi atingida; responsavel financeiro esta definido; impacto foi mostrado; depois pede aprovacao antes de concluir.

**Autonomo com excecoes**

Segue sozinho quando:

- bloqueado: acima do teto deste fluxo.

Chama equipe quando:

- bloqueado: acima do teto deste fluxo.

**Autonomo**

Conclui sozinho quando:

- bloqueado: acima do teto deste fluxo.

Para quando:

- bloqueado: acima do teto deste fluxo.

**Se parar**

criar tarefa/caso em /app/financeiro/movimentacoes; tarefa financeira e manter auditoria do motivo.

**Ajustes relacionados**

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


### Rotina: Excecoes e documentos financeiros

#### Contrato/termos

- ID interno: `D11`.
- Modo padrao: `Autonomo com aprovacao`.
- Teto: `Autonomo com aprovacao`.

**Manual**

A Taliya cria uma tarefa para preparar contrato ou termos para aprovacao; inclui no contexto: template de contrato esta definido; dados do aluno e plano conferem; prazo de envio esta definido; a equipe executa e registra o resultado.

**Copiloto**

A Taliya sugere preparar contrato ou termos para aprovacao; mostra como base: template de contrato esta definido; dados do aluno e plano conferem; prazo de envio esta definido; a equipe decide se aceita, edita ou descarta.

**Autonomo com aprovacao**

A Taliya prepara contrato/termos, valida: template de contrato esta definido; dados do aluno e plano conferem; prazo de envio esta definido; responsavel esta atribuido; depois pede aprovacao antes de concluir.

**Autonomo com excecoes**

Segue sozinho quando:

- bloqueado: acima do teto deste fluxo.

Chama equipe quando:

- bloqueado: acima do teto deste fluxo.

**Autonomo**

Conclui sozinho quando:

- bloqueado: acima do teto deste fluxo.

Para quando:

- bloqueado: acima do teto deste fluxo.

**Se parar**

criar tarefa/caso em /app/contratos; /app/aprovacoes e manter auditoria do motivo.

**Ajustes relacionados**

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

#### Bloqueio/liberacao

- ID interno: `D12`.
- Modo padrao: `Autonomo com aprovacao`.
- Teto: `Autonomo com aprovacao`.

**Manual**

A Taliya cria uma tarefa para preparar bloqueio ou liberacao para aprovacao; inclui no contexto: aluno e motivo foram identificados; impacto financeiro foi calculado; motivo obrigatorio foi preenchido; a equipe executa e registra o resultado.

**Copiloto**

A Taliya sugere preparar bloqueio ou liberacao para aprovacao; mostra como base: aluno e motivo foram identificados; impacto financeiro foi calculado; motivo obrigatorio foi preenchido; a equipe decide se aceita, edita ou descarta.

**Autonomo com aprovacao**

A Taliya prepara bloqueio/liberacao, valida: aluno e motivo foram identificados; impacto financeiro foi calculado; motivo obrigatorio foi preenchido; prazo de aprovacao esta definido; depois pede aprovacao antes de concluir.

**Autonomo com excecoes**

Segue sozinho quando:

- bloqueado: acima do teto deste fluxo.

Chama equipe quando:

- bloqueado: acima do teto deste fluxo.

**Autonomo**

Conclui sozinho quando:

- bloqueado: acima do teto deste fluxo.

Para quando:

- bloqueado: acima do teto deste fluxo.

**Se parar**

criar tarefa/caso em /app/financeiro; /app/aprovacoes; auditoria e manter auditoria do motivo.

**Ajustes relacionados**

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

#### Creditos/cortesias

- ID interno: `D13`.
- Modo padrao: `Autonomo com aprovacao`.
- Teto: `Autonomo com aprovacao`.

**Manual**

A Taliya cria uma tarefa para preparar credito ou cortesia para aprovacao; inclui no contexto: aluno foi identificado; motivo foi informado; limite de valor esta dentro da politica; a equipe executa e registra o resultado.

**Copiloto**

A Taliya sugere preparar credito ou cortesia para aprovacao; mostra como base: aluno foi identificado; motivo foi informado; limite de valor esta dentro da politica; a equipe decide se aceita, edita ou descarta.

**Autonomo com aprovacao**

A Taliya prepara creditos/cortesias, valida: aluno foi identificado; motivo foi informado; limite de valor esta dentro da politica; impacto financeiro foi calculado; depois pede aprovacao antes de concluir.

**Autonomo com excecoes**

Segue sozinho quando:

- bloqueado: acima do teto deste fluxo.

Chama equipe quando:

- bloqueado: acima do teto deste fluxo.

**Autonomo**

Conclui sozinho quando:

- bloqueado: acima do teto deste fluxo.

Para quando:

- bloqueado: acima do teto deste fluxo.

**Se parar**

criar tarefa/caso em /app/financeiro; /app/aprovacoes e manter auditoria do motivo.

**Ajustes relacionados**

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

#### Fechamento mensal

- ID interno: `D14`.
- Modo padrao: `Autonomo com excecoes`.
- Teto: `Autonomo com excecoes`.

**Manual**

A Taliya cria uma tarefa para preparar fechamento mensal financeiro; inclui no contexto: periodo de fechamento esta definido; movimentacoes foram consolidadas; pendencias foram separadas; a equipe executa e registra o resultado.

**Copiloto**

A Taliya sugere preparar fechamento mensal financeiro; mostra como base: periodo de fechamento esta definido; movimentacoes foram consolidadas; pendencias foram separadas; a equipe decide se aceita, edita ou descarta.

**Autonomo com aprovacao**

A Taliya prepara fechamento mensal, valida: periodo de fechamento esta definido; movimentacoes foram consolidadas; pendencias foram separadas; responsavel financeiro esta definido; depois pede aprovacao antes de concluir.

**Autonomo com excecoes**

Segue sozinho quando:

- periodo de fechamento esta definido.
- movimentacoes foram consolidadas.
- pendencias foram separadas.
- responsavel financeiro esta definido.
- frequencia do resumo esta configurada.

Chama equipe quando:

- ha divergencia de conciliacao.
- movimentacao sem dono.
- provedor financeiro falhou.
- pendencia critica apareceu.
- permissao ou cota bloqueia analise.

**Autonomo**

Conclui sozinho quando:

- bloqueado: acima do teto deste fluxo.

Para quando:

- bloqueado: acima do teto deste fluxo.

**Se parar**

criar tarefa/caso em /app/relatorios/financeiro; tarefa financeira e manter auditoria do motivo.

**Ajustes relacionados**

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


### Rotina: Ciclo do plano do aluno

#### Encerramento ou alteracao efetiva de plano

- ID interno: `D15`.
- Modo padrao: `Autonomo com aprovacao`.
- Teto: `Autonomo com aprovacao`.

**Manual**

A Taliya cria uma tarefa para preparar encerramento ou alteracao efetiva de plano; inclui no contexto: plano atual foi identificado; mudanca solicitada foi descrita; impacto em agenda, cobranca e contrato foi calculado; a equipe executa e registra o resultado.

**Copiloto**

A Taliya sugere preparar encerramento ou alteracao efetiva de plano; mostra como base: plano atual foi identificado; mudanca solicitada foi descrita; impacto em agenda, cobranca e contrato foi calculado; a equipe decide se aceita, edita ou descarta.

**Autonomo com aprovacao**

A Taliya prepara encerramento ou alteracao efetiva de plano, valida: plano atual foi identificado; mudanca solicitada foi descrita; impacto em agenda, cobranca e contrato foi calculado; checklist esta completo; depois pede aprovacao antes de concluir.

**Autonomo com excecoes**

Segue sozinho quando:

- bloqueado: acima do teto deste fluxo.

Chama equipe quando:

- bloqueado: acima do teto deste fluxo.

**Autonomo**

Conclui sozinho quando:

- bloqueado: acima do teto deste fluxo.

Para quando:

- bloqueado: acima do teto deste fluxo.

**Se parar**

criar tarefa/caso em /app/financeiro; /app/alunos/[id]; aprovacao/caso e manter auditoria do motivo.

**Ajustes relacionados**

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


## Agente: Retencao


### Rotina: Retencao preventiva

#### Queda frequencia

- ID interno: `E1`.
- Modo padrao: `Autonomo com excecoes`.
- Teto: `Autonomo com excecoes`.

**Manual**

A Taliya cria uma tarefa para detectar queda de frequencia e iniciar prevencao; inclui no contexto: frequencia caiu conforme regra publicada; aluno esta ativo; responsavel esta definido; a equipe executa e registra o resultado.

**Copiloto**

A Taliya sugere detectar queda de frequencia e iniciar prevencao; mostra como base: frequencia caiu conforme regra publicada; aluno esta ativo; responsavel esta definido; a equipe decide se aceita, edita ou descarta.

**Autonomo com aprovacao**

A Taliya prepara queda frequencia, valida: frequencia caiu conforme regra publicada; aluno esta ativo; responsavel esta definido; cadencia permite contato; depois pede aprovacao antes de concluir.

**Autonomo com excecoes**

Segue sozinho quando:

- frequencia caiu conforme regra publicada.
- aluno esta ativo.
- responsavel esta definido.
- cadencia permite contato.
- nao ha caso sensivel aberto.

Chama equipe quando:

- queda tem motivo ja registrado.
- aluno tem reclamacao ou saude/evento pessoal.
- risco de cancelamento aumentou.
- cadencia foi excedida.
- canal, cota ou permissao bloqueia contato.

**Autonomo**

Conclui sozinho quando:

- bloqueado: acima do teto deste fluxo.

Para quando:

- bloqueado: acima do teto deste fluxo.

**Se parar**

criar tarefa/caso em /app/retencao/riscos; /app/alunos/[id]; tarefa e manter auditoria do motivo.

**Ajustes relacionados**

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

#### Aluno inativo

- ID interno: `E2`.
- Modo padrao: `Autonomo com excecoes`.
- Teto: `Autonomo com excecoes`.

**Manual**

A Taliya cria uma tarefa para identificar aluno inativo e preparar retomada; inclui no contexto: dias de inatividade atingiram o limite; aluno esta elegivel para contato; responsavel esta definido; a equipe executa e registra o resultado.

**Copiloto**

A Taliya sugere identificar aluno inativo e preparar retomada; mostra como base: dias de inatividade atingiram o limite; aluno esta elegivel para contato; responsavel esta definido; a equipe decide se aceita, edita ou descarta.

**Autonomo com aprovacao**

A Taliya prepara aluno inativo, valida: dias de inatividade atingiram o limite; aluno esta elegivel para contato; responsavel esta definido; limite de contato nao foi atingido; depois pede aprovacao antes de concluir.

**Autonomo com excecoes**

Segue sozinho quando:

- dias de inatividade atingiram o limite.
- aluno esta elegivel para contato.
- responsavel esta definido.
- limite de contato nao foi atingido.
- mensagem aprovada esta disponivel.

Chama equipe quando:

- aluno pausou ou trancou.
- aluno pediu opt-out.
- ha pendencia financeira ou reclamacao.
- historico indica caso sensivel.
- canal, cota ou permissao bloqueia contato.

**Autonomo**

Conclui sozinho quando:

- bloqueado: acima do teto deste fluxo.

Para quando:

- bloqueado: acima do teto deste fluxo.

**Se parar**

criar tarefa/caso em /app/retencao/riscos; tarefa/aprovacao e manter auditoria do motivo.

**Ajustes relacionados**

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

#### Retorno

- ID interno: `E3`.
- Modo padrao: `Autonomo com excecoes`.
- Teto: `Autonomo com excecoes`.

**Manual**

A Taliya cria uma tarefa para organizar retorno de aluno; inclui no contexto: aluno demonstrou interesse em voltar; regra de agenda permite encaixe; responsavel esta definido; a equipe executa e registra o resultado.

**Copiloto**

A Taliya sugere organizar retorno de aluno; mostra como base: aluno demonstrou interesse em voltar; regra de agenda permite encaixe; responsavel esta definido; a equipe decide se aceita, edita ou descarta.

**Autonomo com aprovacao**

A Taliya prepara retorno, valida: aluno demonstrou interesse em voltar; regra de agenda permite encaixe; responsavel esta definido; opcoes de horario existem; depois pede aprovacao antes de concluir.

**Autonomo com excecoes**

Segue sozinho quando:

- aluno demonstrou interesse em voltar.
- regra de agenda permite encaixe.
- responsavel esta definido.
- opcoes de horario existem.
- mensagem aprovada esta disponivel.

Chama equipe quando:

- nao ha horario compativel.
- aluno tem pendencia financeira.
- retorno exige avaliacao ou cuidado.
- aluno pede condicao especial.
- canal, cota ou permissao bloqueia contato.

**Autonomo**

Conclui sozinho quando:

- bloqueado: acima do teto deste fluxo.

Para quando:

- bloqueado: acima do teto deste fluxo.

**Se parar**

criar tarefa/caso em /app/retencao; /app/agenda; tarefa e manter auditoria do motivo.

**Ajustes relacionados**

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


### Rotina: Casos sensiveis

#### Risco cancelamento

- ID interno: `E4`.
- Modo padrao: `Autonomo com aprovacao`.
- Teto: `Autonomo com aprovacao`.

**Manual**

A Taliya cria uma tarefa para preparar caso de risco de cancelamento para aprovacao; inclui no contexto: sinal de cancelamento foi detectado; dono do caso esta definido; automacoes conflitantes foram pausadas; a equipe executa e registra o resultado.

**Copiloto**

A Taliya sugere preparar caso de risco de cancelamento para aprovacao; mostra como base: sinal de cancelamento foi detectado; dono do caso esta definido; automacoes conflitantes foram pausadas; a equipe decide se aceita, edita ou descarta.

**Autonomo com aprovacao**

A Taliya prepara risco cancelamento, valida: sinal de cancelamento foi detectado; dono do caso esta definido; automacoes conflitantes foram pausadas; contexto foi resumido; depois pede aprovacao antes de concluir.

**Autonomo com excecoes**

Segue sozinho quando:

- bloqueado: acima do teto deste fluxo.

Chama equipe quando:

- bloqueado: acima do teto deste fluxo.

**Autonomo**

Conclui sozinho quando:

- bloqueado: acima do teto deste fluxo.

Para quando:

- bloqueado: acima do teto deste fluxo.

**Se parar**

criar tarefa/caso em /app/cancelamentos; /app/operacao; aprovacao/caso e manter auditoria do motivo.

**Ajustes relacionados**

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

#### Reativacao ex-aluno

- ID interno: `E5`.
- Modo padrao: `Autonomo com aprovacao`.
- Teto: `Autonomo com aprovacao`.

**Manual**

A Taliya cria uma tarefa para preparar reativacao de ex-aluno para aprovacao; inclui no contexto: ex-aluno esta no segmento permitido; cadencia permite contato; mensagem esta aprovada; a equipe executa e registra o resultado.

**Copiloto**

A Taliya sugere preparar reativacao de ex-aluno para aprovacao; mostra como base: ex-aluno esta no segmento permitido; cadencia permite contato; mensagem esta aprovada; a equipe decide se aceita, edita ou descarta.

**Autonomo com aprovacao**

A Taliya prepara reativacao ex-aluno, valida: ex-aluno esta no segmento permitido; cadencia permite contato; mensagem esta aprovada; responsavel esta definido; depois pede aprovacao antes de concluir.

**Autonomo com excecoes**

Segue sozinho quando:

- bloqueado: acima do teto deste fluxo.

Chama equipe quando:

- bloqueado: acima do teto deste fluxo.

**Autonomo**

Conclui sozinho quando:

- bloqueado: acima do teto deste fluxo.

Para quando:

- bloqueado: acima do teto deste fluxo.

**Se parar**

criar tarefa/caso em /app/retencao/reativacoes; /app/aprovacoes e manter auditoria do motivo.

**Ajustes relacionados**

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


### Rotina: Retencao preventiva

#### Satisfacao

- ID interno: `E6`.
- Modo padrao: `Autonomo com excecoes`.
- Teto: `Autonomo com excecoes`.

**Manual**

A Taliya cria uma tarefa para acompanhar satisfacao e abrir cuidado quando necessario; inclui no contexto: janela de satisfacao chegou; aluno esta elegivel; responsavel esta definido; a equipe executa e registra o resultado.

**Copiloto**

A Taliya sugere acompanhar satisfacao e abrir cuidado quando necessario; mostra como base: janela de satisfacao chegou; aluno esta elegivel; responsavel esta definido; a equipe decide se aceita, edita ou descarta.

**Autonomo com aprovacao**

A Taliya prepara satisfacao, valida: janela de satisfacao chegou; aluno esta elegivel; responsavel esta definido; mensagem aprovada esta disponivel; depois pede aprovacao antes de concluir.

**Autonomo com excecoes**

Segue sozinho quando:

- janela de satisfacao chegou.
- aluno esta elegivel.
- responsavel esta definido.
- mensagem aprovada esta disponivel.
- nao ha reclamacao aberta.

Chama equipe quando:

- resposta indica reclamacao.
- nota baixa ou texto sensivel.
- aluno menciona saude, professor ou cobranca.
- ja existe caso aberto.
- canal, cota ou permissao bloqueia contato.

**Autonomo**

Conclui sozinho quando:

- bloqueado: acima do teto deste fluxo.

Para quando:

- bloqueado: acima do teto deste fluxo.

**Se parar**

criar tarefa/caso em /app/retencao; /app/reclamacoes; tarefa e manter auditoria do motivo.

**Ajustes relacionados**

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

#### Retorno apos pausa

- ID interno: `E7`.
- Modo padrao: `Autonomo com excecoes`.
- Teto: `Autonomo com excecoes`.

**Manual**

A Taliya cria uma tarefa para preparar retorno apos pausa; inclui no contexto: fim da pausa esta proximo; aluno esta elegivel para retorno; opcoes de agenda existem; a equipe executa e registra o resultado.

**Copiloto**

A Taliya sugere preparar retorno apos pausa; mostra como base: fim da pausa esta proximo; aluno esta elegivel para retorno; opcoes de agenda existem; a equipe decide se aceita, edita ou descarta.

**Autonomo com aprovacao**

A Taliya prepara retorno apos pausa, valida: fim da pausa esta proximo; aluno esta elegivel para retorno; opcoes de agenda existem; responsavel esta definido; depois pede aprovacao antes de concluir.

**Autonomo com excecoes**

Segue sozinho quando:

- fim da pausa esta proximo.
- aluno esta elegivel para retorno.
- opcoes de agenda existem.
- responsavel esta definido.
- antecedencia configurada chegou.

Chama equipe quando:

- aluno pede estender pausa.
- agenda nao tem vaga.
- ha pendencia financeira.
- retorno exige cuidado ou professor especifico.
- canal, cota ou permissao bloqueia contato.

**Autonomo**

Conclui sozinho quando:

- bloqueado: acima do teto deste fluxo.

Para quando:

- bloqueado: acima do teto deste fluxo.

**Se parar**

criar tarefa/caso em /app/retencao; /app/agenda; tarefa e manter auditoria do motivo.

**Ajustes relacionados**

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


### Rotina: Casos sensiveis

#### Risco por perfil

- ID interno: `E8`.
- Modo padrao: `Autonomo com aprovacao`.
- Teto: `Autonomo com aprovacao`.

**Manual**

A Taliya cria uma tarefa para preparar acao de risco por perfil para aprovacao; inclui no contexto: segmento de risco foi identificado; uso do segmento esta permitido; acao proposta foi definida; a equipe executa e registra o resultado.

**Copiloto**

A Taliya sugere preparar acao de risco por perfil para aprovacao; mostra como base: segmento de risco foi identificado; uso do segmento esta permitido; acao proposta foi definida; a equipe decide se aceita, edita ou descarta.

**Autonomo com aprovacao**

A Taliya prepara risco por perfil, valida: segmento de risco foi identificado; uso do segmento esta permitido; acao proposta foi definida; responsavel esta definido; depois pede aprovacao antes de concluir.

**Autonomo com excecoes**

Segue sozinho quando:

- bloqueado: acima do teto deste fluxo.

Chama equipe quando:

- bloqueado: acima do teto deste fluxo.

**Autonomo**

Conclui sozinho quando:

- bloqueado: acima do teto deste fluxo.

Para quando:

- bloqueado: acima do teto deste fluxo.

**Se parar**

criar tarefa/caso em /app/retencao/riscos; aprovacao/tarefa e manter auditoria do motivo.

**Ajustes relacionados**

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

#### Pos-cancelamento

- ID interno: `E9`.
- Modo padrao: `Autonomo com aprovacao`.
- Teto: `Autonomo com aprovacao`.

**Manual**

A Taliya cria uma tarefa para preparar pos-cancelamento para aprovacao; inclui no contexto: cancelamento foi registrado; janela de contato esta definida; responsavel esta atribuido; a equipe executa e registra o resultado.

**Copiloto**

A Taliya sugere preparar pos-cancelamento para aprovacao; mostra como base: cancelamento foi registrado; janela de contato esta definida; responsavel esta atribuido; a equipe decide se aceita, edita ou descarta.

**Autonomo com aprovacao**

A Taliya prepara pos-cancelamento, valida: cancelamento foi registrado; janela de contato esta definida; responsavel esta atribuido; mensagem nao reabre conflito; depois pede aprovacao antes de concluir.

**Autonomo com excecoes**

Segue sozinho quando:

- bloqueado: acima do teto deste fluxo.

Chama equipe quando:

- bloqueado: acima do teto deste fluxo.

**Autonomo**

Conclui sozinho quando:

- bloqueado: acima do teto deste fluxo.

Para quando:

- bloqueado: acima do teto deste fluxo.

**Se parar**

criar tarefa/caso em /app/cancelamentos; /app/aprovacoes; tarefa e manter auditoria do motivo.

**Ajustes relacionados**

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


### Rotina: Retencao preventiva

#### Marco engajamento

- ID interno: `E10`.
- Modo padrao: `Autonomo com excecoes`.
- Teto: `Autonomo com excecoes`.

**Manual**

A Taliya cria uma tarefa para reconhecer marco de engajamento e acionar contato leve; inclui no contexto: marco configurado aconteceu; aluno esta ativo; tipo de marco esta permitido; a equipe executa e registra o resultado.

**Copiloto**

A Taliya sugere reconhecer marco de engajamento e acionar contato leve; mostra como base: marco configurado aconteceu; aluno esta ativo; tipo de marco esta permitido; a equipe decide se aceita, edita ou descarta.

**Autonomo com aprovacao**

A Taliya prepara marco engajamento, valida: marco configurado aconteceu; aluno esta ativo; tipo de marco esta permitido; responsavel esta definido; depois pede aprovacao antes de concluir.

**Autonomo com excecoes**

Segue sozinho quando:

- marco configurado aconteceu.
- aluno esta ativo.
- tipo de marco esta permitido.
- responsavel esta definido.
- limite de contato nao foi atingido.

Chama equipe quando:

- aluno tem caso sensivel aberto.
- marco conflita com baixa frequencia.
- mensagem poderia soar inadequada.
- aluno pediu opt-out.
- canal, cota ou permissao bloqueia contato.

**Autonomo**

Conclui sozinho quando:

- bloqueado: acima do teto deste fluxo.

Para quando:

- bloqueado: acima do teto deste fluxo.

**Se parar**

criar tarefa/caso em /app/retencao; tarefa e manter auditoria do motivo.

**Ajustes relacionados**

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


### Rotina: Casos sensiveis

#### Saude/evento pessoal

- ID interno: `E11`.
- Modo padrao: `Autonomo com aprovacao`.
- Teto: `Autonomo com aprovacao`.

**Manual**

A Taliya cria uma tarefa para preparar caso de saude ou evento pessoal para aprovacao; inclui no contexto: evento foi identificado; visibilidade esta definida; dono do caso foi atribuido; a equipe executa e registra o resultado.

**Copiloto**

A Taliya sugere preparar caso de saude ou evento pessoal para aprovacao; mostra como base: evento foi identificado; visibilidade esta definida; dono do caso foi atribuido; a equipe decide se aceita, edita ou descarta.

**Autonomo com aprovacao**

A Taliya prepara saude/evento pessoal, valida: evento foi identificado; visibilidade esta definida; dono do caso foi atribuido; nenhum contato automatico sera feito sem revisao; depois pede aprovacao antes de concluir.

**Autonomo com excecoes**

Segue sozinho quando:

- bloqueado: acima do teto deste fluxo.

Chama equipe quando:

- bloqueado: acima do teto deste fluxo.

**Autonomo**

Conclui sozinho quando:

- bloqueado: acima do teto deste fluxo.

Para quando:

- bloqueado: acima do teto deste fluxo.

**Se parar**

criar tarefa/caso em /app/operacao; /app/historico; caso e manter auditoria do motivo.

**Ajustes relacionados**

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

#### Segmentacao risco

- ID interno: `E12`.
- Modo padrao: `Autonomo com aprovacao`.
- Teto: `Autonomo com aprovacao`.

**Manual**

A Taliya cria uma tarefa para preparar segmentacao de risco para aprovacao; inclui no contexto: segmento foi definido; acao permitida foi escolhida; dados usados foram listados; a equipe executa e registra o resultado.

**Copiloto**

A Taliya sugere preparar segmentacao de risco para aprovacao; mostra como base: segmento foi definido; acao permitida foi escolhida; dados usados foram listados; a equipe decide se aceita, edita ou descarta.

**Autonomo com aprovacao**

A Taliya prepara segmentacao risco, valida: segmento foi definido; acao permitida foi escolhida; dados usados foram listados; responsavel esta definido; depois pede aprovacao antes de concluir.

**Autonomo com excecoes**

Segue sozinho quando:

- bloqueado: acima do teto deste fluxo.

Chama equipe quando:

- bloqueado: acima do teto deste fluxo.

**Autonomo**

Conclui sozinho quando:

- bloqueado: acima do teto deste fluxo.

Para quando:

- bloqueado: acima do teto deste fluxo.

**Se parar**

criar tarefa/caso em /app/retencao/riscos; /app/aprovacoes e manter auditoria do motivo.

**Ajustes relacionados**

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

#### Reclamacao e recuperacao de confianca

- ID interno: `E13`.
- Modo padrao: `Autonomo com aprovacao`.
- Teto: `Autonomo com aprovacao`.

**Manual**

A Taliya cria uma tarefa para preparar recuperacao de reclamacao para aprovacao; inclui no contexto: reclamacao foi registrada; dono do caso esta definido; automacoes foram pausadas; a equipe executa e registra o resultado.

**Copiloto**

A Taliya sugere preparar recuperacao de reclamacao para aprovacao; mostra como base: reclamacao foi registrada; dono do caso esta definido; automacoes foram pausadas; a equipe decide se aceita, edita ou descarta.

**Autonomo com aprovacao**

A Taliya prepara reclamacao e recuperacao de confianca, valida: reclamacao foi registrada; dono do caso esta definido; automacoes foram pausadas; resumo e proposta foram preparados; depois pede aprovacao antes de concluir.

**Autonomo com excecoes**

Segue sozinho quando:

- bloqueado: acima do teto deste fluxo.

Chama equipe quando:

- bloqueado: acima do teto deste fluxo.

**Autonomo**

Conclui sozinho quando:

- bloqueado: acima do teto deste fluxo.

Para quando:

- bloqueado: acima do teto deste fluxo.

**Se parar**

criar tarefa/caso em /app/reclamacoes; /app/operacao; /app/aprovacoes e manter auditoria do motivo.

**Ajustes relacionados**

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


## Agente: Gestao/Governanca


### Rotina: Comando operacional

#### Prioridades dia

- ID interno: `F1`.
- Modo padrao: `Autonomo`.
- Teto: `Autonomo`.

**Manual**

A Taliya cria uma tarefa para montar prioridades do dia; inclui no contexto: fontes operacionais estao atualizadas; horario do resumo chegou; responsavel esta definido; a equipe executa e registra o resultado.

**Copiloto**

A Taliya sugere montar prioridades do dia; mostra como base: fontes operacionais estao atualizadas; horario do resumo chegou; responsavel esta definido; a equipe decide se aceita, edita ou descarta.

**Autonomo com aprovacao**

A Taliya prepara prioridades dia, valida: fontes operacionais estao atualizadas; horario do resumo chegou; responsavel esta definido; tarefas e aprovacoes foram consolidadas; depois pede aprovacao antes de concluir.

**Autonomo com excecoes**

Segue sozinho quando:

- fontes operacionais estao atualizadas.
- horario do resumo chegou.
- responsavel esta definido.
- tarefas e aprovacoes foram consolidadas.
- nada critico impede leitura.

Chama equipe quando:

- fonte importante falhou.
- ha incidente critico.
- dado principal esta desatualizado.
- responsavel nao esta definido.
- permissao ou cota bloqueia resumo.

**Autonomo**

Conclui sozinho quando:

- fontes operacionais estao atualizadas.
- horario do resumo chegou.
- responsavel esta definido.
- tarefas e aprovacoes foram consolidadas.
- nada critico impede leitura.
- nenhuma regra exige aprovacao ou chamada humana.

Para quando:

- fonte importante falhou.
- ha incidente critico.
- dado principal esta desatualizado.
- responsavel nao esta definido.
- permissao ou cota bloqueia resumo.
- canal, permissao, cota, opt-out, integracao ou incidente bloqueia a conclusao.

**Se parar**

criar tarefa/caso em /app/hoje; /app/tarefas e manter auditoria do motivo.

**Ajustes relacionados**

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

#### Dinheiro na mesa

- ID interno: `F2`.
- Modo padrao: `Autonomo com excecoes`.
- Teto: `Autonomo com excecoes`.

**Manual**

A Taliya cria uma tarefa para identificar dinheiro na mesa e abrir proxima acao; inclui no contexto: oportunidade financeira foi detectada; frequencia do alerta permite envio; responsavel esta definido; a equipe executa e registra o resultado.

**Copiloto**

A Taliya sugere identificar dinheiro na mesa e abrir proxima acao; mostra como base: oportunidade financeira foi detectada; frequencia do alerta permite envio; responsavel esta definido; a equipe decide se aceita, edita ou descarta.

**Autonomo com aprovacao**

A Taliya prepara dinheiro na mesa, valida: oportunidade financeira foi detectada; frequencia do alerta permite envio; responsavel esta definido; acao sugerida nao altera financeiro sozinha; depois pede aprovacao antes de concluir.

**Autonomo com excecoes**

Segue sozinho quando:

- oportunidade financeira foi detectada.
- frequencia do alerta permite envio.
- responsavel esta definido.
- acao sugerida nao altera financeiro sozinha.
- dados financeiros estao disponiveis.

Chama equipe quando:

- valor esta incerto.
- caso depende de acordo ou desconto.
- movimentacao esta em disputa.
- responsavel nao existe.
- permissao ou cota bloqueia analise.

**Autonomo**

Conclui sozinho quando:

- bloqueado: acima do teto deste fluxo.

Para quando:

- bloqueado: acima do teto deste fluxo.

**Se parar**

criar tarefa/caso em /app/dinheiro-na-mesa; /app/financeiro; tarefa e manter auditoria do motivo.

**Ajustes relacionados**

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

#### Fila humana

- ID interno: `F3`.
- Modo padrao: `Autonomo`.
- Teto: `Autonomo`.

**Manual**

A Taliya cria uma tarefa para organizar fila humana e prioridades; inclui no contexto: itens humanos foram encontrados; filas estao configuradas; prioridade foi calculada; a equipe executa e registra o resultado.

**Copiloto**

A Taliya sugere organizar fila humana e prioridades; mostra como base: itens humanos foram encontrados; filas estao configuradas; prioridade foi calculada; a equipe decide se aceita, edita ou descarta.

**Autonomo com aprovacao**

A Taliya prepara fila humana, valida: itens humanos foram encontrados; filas estao configuradas; prioridade foi calculada; responsaveis existem; depois pede aprovacao antes de concluir.

**Autonomo com excecoes**

Segue sozinho quando:

- itens humanos foram encontrados.
- filas estao configuradas.
- prioridade foi calculada.
- responsaveis existem.
- nenhum item exige permissao ausente.

Chama equipe quando:

- item sem dono.
- prioridade conflita entre filas.
- incidente aberto exige pausa.
- aprovacao vencida acumulou.
- permissao ou cota bloqueia atualizacao.

**Autonomo**

Conclui sozinho quando:

- itens humanos foram encontrados.
- filas estao configuradas.
- prioridade foi calculada.
- responsaveis existem.
- nenhum item exige permissao ausente.
- nenhuma regra exige aprovacao ou chamada humana.

Para quando:

- item sem dono.
- prioridade conflita entre filas.
- incidente aberto exige pausa.
- aprovacao vencida acumulou.
- permissao ou cota bloqueia atualizacao.
- canal, permissao, cota, opt-out, integracao ou incidente bloqueia a conclusao.

**Se parar**

criar tarefa/caso em /app/operacao; /app/aprovacoes; /app/tarefas e manter auditoria do motivo.

**Ajustes relacionados**

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

#### Gargalos

- ID interno: `F4`.
- Modo padrao: `Autonomo com excecoes`.
- Teto: `Autonomo com excecoes`.

**Manual**

A Taliya cria uma tarefa para detectar gargalos operacionais; inclui no contexto: metricas foram atualizadas; frequencia do alerta permite analise; tipo de alerta esta definido; a equipe executa e registra o resultado.

**Copiloto**

A Taliya sugere detectar gargalos operacionais; mostra como base: metricas foram atualizadas; frequencia do alerta permite analise; tipo de alerta esta definido; a equipe decide se aceita, edita ou descarta.

**Autonomo com aprovacao**

A Taliya prepara gargalos, valida: metricas foram atualizadas; frequencia do alerta permite analise; tipo de alerta esta definido; responsavel esta atribuido; depois pede aprovacao antes de concluir.

**Autonomo com excecoes**

Segue sozinho quando:

- metricas foram atualizadas.
- frequencia do alerta permite analise.
- tipo de alerta esta definido.
- responsavel esta atribuido.
- acao sugerida e operacional.

Chama equipe quando:

- dado esta incompleto.
- gargalo envolve financeiro, grade ou incidente.
- alerta e critico.
- responsavel nao definido.
- permissao ou cota bloqueia analise.

**Autonomo**

Conclui sozinho quando:

- bloqueado: acima do teto deste fluxo.

Para quando:

- bloqueado: acima do teto deste fluxo.

**Se parar**

criar tarefa/caso em /app/relatorios; /app/operacao; tarefa e manter auditoria do motivo.

**Ajustes relacionados**

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

#### Resumo semanal

- ID interno: `F5`.
- Modo padrao: `Autonomo`.
- Teto: `Autonomo`.

**Manual**

A Taliya cria uma tarefa para gerar resumo semanal; inclui no contexto: periodo da semana fechou; secoes do resumo estao configuradas; destinatarios internos estao definidos; a equipe executa e registra o resultado.

**Copiloto**

A Taliya sugere gerar resumo semanal; mostra como base: periodo da semana fechou; secoes do resumo estao configuradas; destinatarios internos estao definidos; a equipe decide se aceita, edita ou descarta.

**Autonomo com aprovacao**

A Taliya prepara resumo semanal, valida: periodo da semana fechou; secoes do resumo estao configuradas; destinatarios internos estao definidos; dados principais estao atualizados; depois pede aprovacao antes de concluir.

**Autonomo com excecoes**

Segue sozinho quando:

- periodo da semana fechou.
- secoes do resumo estao configuradas.
- destinatarios internos estao definidos.
- dados principais estao atualizados.
- nenhum incidente impede resumo.

Chama equipe quando:

- fonte de dados falhou.
- secoes obrigatorias vazias.
- destinatario sem permissao.
- incidente critico em aberto.
- cota ou permissao bloqueia envio.

**Autonomo**

Conclui sozinho quando:

- periodo da semana fechou.
- secoes do resumo estao configuradas.
- destinatarios internos estao definidos.
- dados principais estao atualizados.
- nenhum incidente impede resumo.
- nenhuma regra exige aprovacao ou chamada humana.

Para quando:

- fonte de dados falhou.
- secoes obrigatorias vazias.
- destinatario sem permissao.
- incidente critico em aberto.
- cota ou permissao bloqueia envio.
- canal, permissao, cota, opt-out, integracao ou incidente bloqueia a conclusao.

**Se parar**

criar tarefa/caso em /app/relatorios/semana; /app/hoje e manter auditoria do motivo.

**Ajustes relacionados**

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

#### Qualidade dados

- ID interno: `F6`.
- Modo padrao: `Autonomo com excecoes`.
- Teto: `Autonomo com excecoes`.

**Manual**

A Taliya cria uma tarefa para detectar qualidade de dados e abrir tarefa de correcao; inclui no contexto: tipo de dado a revisar pertence aos campos monitorados; duplicidade ou lacuna foi detectada; prioridade foi calculada; a equipe executa e registra o resultado.

**Copiloto**

A Taliya sugere detectar qualidade de dados e abrir tarefa de correcao; mostra como base: tipo de dado a revisar pertence aos campos monitorados; duplicidade ou lacuna foi detectada; prioridade foi calculada; a equipe decide se aceita, edita ou descarta.

**Autonomo com aprovacao**

A Taliya prepara qualidade dados, valida: tipo de dado a revisar pertence aos campos monitorados; duplicidade ou lacuna foi detectada; prioridade foi calculada; responsavel esta definido; depois pede aprovacao antes de concluir.

**Autonomo com excecoes**

Segue sozinho quando:

- tipo de dado a revisar pertence aos campos monitorados.
- duplicidade ou lacuna foi detectada.
- prioridade foi calculada.
- responsavel esta definido.
- correcao automatica nao altera dado sensivel.

Chama equipe quando:

- correcao pode fundir cadastros.
- dado envolve historico protegido.
- conflito nao tem dono claro.
- volume e alto demais.
- permissao ou cota bloqueia analise.

**Autonomo**

Conclui sozinho quando:

- bloqueado: acima do teto deste fluxo.

Para quando:

- bloqueado: acima do teto deste fluxo.

**Se parar**

criar tarefa/caso em /app/dados/qualidade; /app/dados/duplicidades; tarefa e manter auditoria do motivo.

**Ajustes relacionados**

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


### Rotina: Governanca de agentes

#### Creditos/limites

- ID interno: `F7`.
- Modo padrao: `Autonomo`.
- Teto: `Autonomo`.

**Manual**

A Taliya cria uma tarefa para monitorar creditos, limites e cotas; inclui no contexto: uso foi atualizado; alertas 70/90/100 estao configurados; responsavel esta definido; a equipe executa e registra o resultado.

**Copiloto**

A Taliya sugere monitorar creditos, limites e cotas; mostra como base: uso foi atualizado; alertas 70/90/100 estao configurados; responsavel esta definido; a equipe decide se aceita, edita ou descarta.

**Autonomo com aprovacao**

A Taliya prepara creditos/limites, valida: uso foi atualizado; alertas 70/90/100 estao configurados; responsavel esta definido; limite comercial foi lido do billing; depois pede aprovacao antes de concluir.

**Autonomo com excecoes**

Segue sozinho quando:

- uso foi atualizado.
- alertas 70/90/100 estao configurados.
- responsavel esta definido.
- limite comercial foi lido do billing.
- mensagem interna esta pronta.

Chama equipe quando:

- cota atingiu limite critico.
- billing diverge do uso.
- responsavel nao definido.
- addon ou upgrade precisa decisao.
- permissao bloqueia leitura.

**Autonomo**

Conclui sozinho quando:

- uso foi atualizado.
- alertas 70/90/100 estao configurados.
- responsavel esta definido.
- limite comercial foi lido do billing.
- mensagem interna esta pronta.
- nenhuma regra exige aprovacao ou chamada humana.

Para quando:

- cota atingiu limite critico.
- billing diverge do uso.
- responsavel nao definido.
- addon ou upgrade precisa decisao.
- permissao bloqueia leitura.
- canal, permissao, cota, opt-out, integracao ou incidente bloqueia a conclusao.

**Se parar**

criar tarefa/caso em /app/uso; /app/uso/cotas; /app/hoje e manter auditoria do motivo.

**Ajustes relacionados**

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

#### Performance

- ID interno: `F8`.
- Modo padrao: `Autonomo com excecoes`.
- Teto: `Autonomo com excecoes`.

**Manual**

A Taliya cria uma tarefa para monitorar performance dos agentes; inclui no contexto: metricas foram coletadas; frequencia permite novo relatorio; responsavel esta definido; a equipe executa e registra o resultado.

**Copiloto**

A Taliya sugere monitorar performance dos agentes; mostra como base: metricas foram coletadas; frequencia permite novo relatorio; responsavel esta definido; a equipe decide se aceita, edita ou descarta.

**Autonomo com aprovacao**

A Taliya prepara performance, valida: metricas foram coletadas; frequencia permite novo relatorio; responsavel esta definido; indicadores configurados existem; depois pede aprovacao antes de concluir.

**Autonomo com excecoes**

Segue sozinho quando:

- metricas foram coletadas.
- frequencia permite novo relatorio.
- responsavel esta definido.
- indicadores configurados existem.
- acao sugerida nao altera politica sozinha.

Chama equipe quando:

- queda forte de performance.
- falha ou incidente correlacionado.
- amostra insuficiente.
- acao exige mudar fluxo ou politica.
- permissao ou cota bloqueia analise.

**Autonomo**

Conclui sozinho quando:

- bloqueado: acima do teto deste fluxo.

Para quando:

- bloqueado: acima do teto deste fluxo.

**Se parar**

criar tarefa/caso em /app/relatorios/agentes; /app/agentes; tarefa e manter auditoria do motivo.

**Ajustes relacionados**

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

#### Permissoes/auditoria

- ID interno: `F9`.
- Modo padrao: `Autonomo com aprovacao`.
- Teto: `Autonomo com aprovacao`.

**Manual**

A Taliya cria uma tarefa para preparar revisao de permissoes ou auditoria para aprovacao; inclui no contexto: evento de auditoria foi identificado; tipo de evento esta dentro do escopo; responsavel esta definido; a equipe executa e registra o resultado.

**Copiloto**

A Taliya sugere preparar revisao de permissoes ou auditoria para aprovacao; mostra como base: evento de auditoria foi identificado; tipo de evento esta dentro do escopo; responsavel esta definido; a equipe decide se aceita, edita ou descarta.

**Autonomo com aprovacao**

A Taliya prepara permissoes/auditoria, valida: evento de auditoria foi identificado; tipo de evento esta dentro do escopo; responsavel esta definido; impacto foi resumido; depois pede aprovacao antes de concluir.

**Autonomo com excecoes**

Segue sozinho quando:

- bloqueado: acima do teto deste fluxo.

Chama equipe quando:

- bloqueado: acima do teto deste fluxo.

**Autonomo**

Conclui sozinho quando:

- bloqueado: acima do teto deste fluxo.

Para quando:

- bloqueado: acima do teto deste fluxo.

**Se parar**

criar tarefa/caso em /app/auditoria; /app/configuracoes/permissoes; aprovacao e manter auditoria do motivo.

**Ajustes relacionados**

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


### Rotina: Comando operacional

#### Capacidade/crescimento

- ID interno: `F10`.
- Modo padrao: `Autonomo com excecoes`.
- Teto: `Autonomo com excecoes`.

**Manual**

A Taliya cria uma tarefa para detectar capacidade e crescimento; inclui no contexto: ocupacao foi calculada; limite de alerta foi atingido ou esta proximo; responsavel esta definido; a equipe executa e registra o resultado.

**Copiloto**

A Taliya sugere detectar capacidade e crescimento; mostra como base: ocupacao foi calculada; limite de alerta foi atingido ou esta proximo; responsavel esta definido; a equipe decide se aceita, edita ou descarta.

**Autonomo com aprovacao**

A Taliya prepara capacidade/crescimento, valida: ocupacao foi calculada; limite de alerta foi atingido ou esta proximo; responsavel esta definido; acao sugerida nao altera grade sozinha; depois pede aprovacao antes de concluir.

**Autonomo com excecoes**

Segue sozinho quando:

- ocupacao foi calculada.
- limite de alerta foi atingido ou esta proximo.
- responsavel esta definido.
- acao sugerida nao altera grade sozinha.
- dados de agenda estao atualizados.

Chama equipe quando:

- capacidade ultrapassa limite.
- crescimento exige nova turma ou horario.
- dados de agenda conflitam.
- impacto financeiro aparece.
- permissao ou cota bloqueia analise.

**Autonomo**

Conclui sozinho quando:

- bloqueado: acima do teto deste fluxo.

Para quando:

- bloqueado: acima do teto deste fluxo.

**Se parar**

criar tarefa/caso em /app/relatorios/ocupacao; /app/agenda; tarefa e manter auditoria do motivo.

**Ajustes relacionados**

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


### Rotina: Integracoes e importacao

#### Falhas/webhooks

- ID interno: `F11`.
- Modo padrao: `Autonomo com excecoes`.
- Teto: `Autonomo com excecoes`.

**Manual**

A Taliya cria uma tarefa para tratar falhas, webhooks e retries seguros; inclui no contexto: falha tecnica foi identificada; severidade esta definida; retry seguro e permitido; a equipe executa e registra o resultado.

**Copiloto**

A Taliya sugere tratar falhas, webhooks e retries seguros; mostra como base: falha tecnica foi identificada; severidade esta definida; retry seguro e permitido; a equipe decide se aceita, edita ou descarta.

**Autonomo com aprovacao**

A Taliya prepara falhas/webhooks, valida: falha tecnica foi identificada; severidade esta definida; retry seguro e permitido; responsavel esta atribuido; depois pede aprovacao antes de concluir.

**Autonomo com excecoes**

Segue sozinho quando:

- falha tecnica foi identificada.
- severidade esta definida.
- retry seguro e permitido.
- responsavel esta atribuido.
- log tecnico esta disponivel.

Chama equipe quando:

- retry pode duplicar efeito.
- falha persiste.
- severidade e alta.
- provedor esta indisponivel.
- permissao ou limite bloqueia mitigacao.

**Autonomo**

Conclui sozinho quando:

- bloqueado: acima do teto deste fluxo.

Para quando:

- bloqueado: acima do teto deste fluxo.

**Se parar**

criar tarefa/caso em configuracao especifica da integracao; /app/operacao/incidentes e manter auditoria do motivo.

**Ajustes relacionados**

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

#### Importacao/migracao

- ID interno: `F12`.
- Modo padrao: `Autonomo com aprovacao`.
- Teto: `Autonomo com aprovacao`.

**Manual**

A Taliya cria uma tarefa para preparar importacao ou migracao para aprovacao; inclui no contexto: lote foi identificado; amostra foi validada; impacto em dados foi resumido; a equipe executa e registra o resultado.

**Copiloto**

A Taliya sugere preparar importacao ou migracao para aprovacao; mostra como base: lote foi identificado; amostra foi validada; impacto em dados foi resumido; a equipe decide se aceita, edita ou descarta.

**Autonomo com aprovacao**

A Taliya prepara importacao/migracao, valida: lote foi identificado; amostra foi validada; impacto em dados foi resumido; responsavel esta definido; depois pede aprovacao antes de concluir.

**Autonomo com excecoes**

Segue sozinho quando:

- bloqueado: acima do teto deste fluxo.

Chama equipe quando:

- bloqueado: acima do teto deste fluxo.

**Autonomo**

Conclui sozinho quando:

- bloqueado: acima do teto deste fluxo.

Para quando:

- bloqueado: acima do teto deste fluxo.

**Se parar**

criar tarefa/caso em /app/importacao/[jobId]; /app/dados/qualidade; aprovacao e manter auditoria do motivo.

**Ajustes relacionados**

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


### Rotina: Governanca de agentes

#### Teste de fluxo

- ID interno: `F13`.
- Modo padrao: `Autonomo`.
- Teto: `Autonomo`.

**Manual**

A Taliya cria uma tarefa para rodar teste de fluxo em simulacao; inclui no contexto: cenario de teste foi escolhido; dados de exemplo estao disponiveis; fluxo nao publica acao real; a equipe executa e registra o resultado.

**Copiloto**

A Taliya sugere rodar teste de fluxo em simulacao; mostra como base: cenario de teste foi escolhido; dados de exemplo estao disponiveis; fluxo nao publica acao real; a equipe decide se aceita, edita ou descarta.

**Autonomo com aprovacao**

A Taliya prepara teste de fluxo, valida: cenario de teste foi escolhido; dados de exemplo estao disponiveis; fluxo nao publica acao real; responsavel por revisao esta definido; depois pede aprovacao antes de concluir.

**Autonomo com excecoes**

Segue sozinho quando:

- cenario de teste foi escolhido.
- dados de exemplo estao disponiveis.
- fluxo nao publica acao real.
- responsavel por revisao esta definido.
- resultado pode ser salvo.

Chama equipe quando:

- cenario usa dado real sensivel.
- teste tenta publicar acao.
- resultado falha preflight.
- fluxo tem dependencia indisponivel.
- permissao ou cota bloqueia teste.

**Autonomo**

Conclui sozinho quando:

- cenario de teste foi escolhido.
- dados de exemplo estao disponiveis.
- fluxo nao publica acao real.
- responsavel por revisao esta definido.
- resultado pode ser salvo.
- nenhuma regra exige aprovacao ou chamada humana.

Para quando:

- cenario usa dado real sensivel.
- teste tenta publicar acao.
- resultado falha preflight.
- fluxo tem dependencia indisponivel.
- permissao ou cota bloqueia teste.
- canal, permissao, cota, opt-out, integracao ou incidente bloqueia a conclusao.

**Se parar**

criar tarefa/caso em /app/fluxos/[flowId]/simular; /app/fluxos/[flowId] e manter auditoria do motivo.

**Ajustes relacionados**

- exemplos de simulacao.
- responsavel.

**Requisitos readonly**

- dados operacionais atualizados.
- permissoes administrativas.
- fontes de uso/logs disponiveis.
- politica publicada quando houver.
- cota.
- auditoria.

#### Incidente de automacao e correcao operacional

- ID interno: `F14`.
- Modo padrao: `Autonomo com excecoes`.
- Teto: `Autonomo com excecoes`.

**Manual**

A Taliya cria uma tarefa para tratar incidente de automacao e correcao operacional; inclui no contexto: incidente foi detectado; severidade esta definida; auto-pausa e permitida para o fluxo; a equipe executa e registra o resultado.

**Copiloto**

A Taliya sugere tratar incidente de automacao e correcao operacional; mostra como base: incidente foi detectado; severidade esta definida; auto-pausa e permitida para o fluxo; a equipe decide se aceita, edita ou descarta.

**Autonomo com aprovacao**

A Taliya prepara incidente de automacao e correcao operacional, valida: incidente foi detectado; severidade esta definida; auto-pausa e permitida para o fluxo; responsavel esta atribuido; depois pede aprovacao antes de concluir.

**Autonomo com excecoes**

Segue sozinho quando:

- incidente foi detectado.
- severidade esta definida.
- auto-pausa e permitida para o fluxo.
- responsavel esta atribuido.
- execucao relacionada foi encontrada.

Chama equipe quando:

- incidente afeta varios fluxos.
- auto-pausa nao e permitida.
- correcao exige rollback.
- falha envolve integracao externa.
- permissao bloqueia mitigacao.

**Autonomo**

Conclui sozinho quando:

- bloqueado: acima do teto deste fluxo.

Para quando:

- bloqueado: acima do teto deste fluxo.

**Se parar**

criar tarefa/caso em /app/operacao/incidentes/[incidentId]; /app/fluxos/execucoes/[runId] e manter auditoria do motivo.

**Ajustes relacionados**

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

#### Mudanca de politica ou regra operacional

- ID interno: `F15`.
- Modo padrao: `Autonomo com aprovacao`.
- Teto: `Autonomo com aprovacao`.

**Manual**

A Taliya cria uma tarefa para preparar mudanca de politica ou regra operacional; inclui no contexto: politica ou regra foi identificada; data de vigencia esta definida; simulacao de impacto foi feita; a equipe executa e registra o resultado.

**Copiloto**

A Taliya sugere preparar mudanca de politica ou regra operacional; mostra como base: politica ou regra foi identificada; data de vigencia esta definida; simulacao de impacto foi feita; a equipe decide se aceita, edita ou descarta.

**Autonomo com aprovacao**

A Taliya prepara mudanca de politica ou regra operacional, valida: politica ou regra foi identificada; data de vigencia esta definida; simulacao de impacto foi feita; comunicacao interna esta pronta; depois pede aprovacao antes de concluir.

**Autonomo com excecoes**

Segue sozinho quando:

- bloqueado: acima do teto deste fluxo.

Chama equipe quando:

- bloqueado: acima do teto deste fluxo.

**Autonomo**

Conclui sozinho quando:

- bloqueado: acima do teto deste fluxo.

Para quando:

- bloqueado: acima do teto deste fluxo.

**Se parar**

criar tarefa/caso em /app/politicas/[policyId]; /app/aprovacoes; auditoria e manter auditoria do motivo.

**Ajustes relacionados**

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


## Agente: Historico/Evolucao


### Rotina: Aula com contexto

#### Contexto antes aula

- ID interno: `G1`.
- Modo padrao: `Autonomo com excecoes`.
- Teto: `Autonomo com excecoes`.

**Manual**

A Taliya cria uma tarefa para preparar contexto antes da aula para professor; inclui no contexto: aula e professor foram identificados; alunos da aula foram listados; visibilidade do historico permite uso; a equipe executa e registra o resultado.

**Copiloto**

A Taliya sugere preparar contexto antes da aula para professor; mostra como base: aula e professor foram identificados; alunos da aula foram listados; visibilidade do historico permite uso; a equipe decide se aceita, edita ou descarta.

**Autonomo com aprovacao**

A Taliya prepara contexto antes aula, valida: aula e professor foram identificados; alunos da aula foram listados; visibilidade do historico permite uso; contexto nao inclui dado protegido indevido; depois pede aprovacao antes de concluir.

**Autonomo com excecoes**

Segue sozinho quando:

- aula e professor foram identificados.
- alunos da aula foram listados.
- visibilidade do historico permite uso.
- contexto nao inclui dado protegido indevido.
- professor pode receber o resumo.

Chama equipe quando:

- aluno tem restricao sensivel.
- professor sem permissao para dado.
- historico esta incompleto.
- aula foi alterada.
- permissao ou cota bloqueia resumo.

**Autonomo**

Conclui sozinho quando:

- bloqueado: acima do teto deste fluxo.

Para quando:

- bloqueado: acima do teto deste fluxo.

**Se parar**

criar tarefa/caso em /app/professores; /app/aulas/[id]; tarefa e manter auditoria do motivo.

**Ajustes relacionados**

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

#### Observacao pos-aula

- ID interno: `G2`.
- Modo padrao: `Autonomo com excecoes`.
- Teto: `Autonomo com excecoes`.

**Manual**

A Taliya cria uma tarefa para lembrar e organizar observacao pos-aula; inclui no contexto: aula terminou; professor foi identificado; tipos de nota permitidos estao definidos; a equipe executa e registra o resultado.

**Copiloto**

A Taliya sugere lembrar e organizar observacao pos-aula; mostra como base: aula terminou; professor foi identificado; tipos de nota permitidos estao definidos; a equipe decide se aceita, edita ou descarta.

**Autonomo com aprovacao**

A Taliya prepara observacao pos-aula, valida: aula terminou; professor foi identificado; tipos de nota permitidos estao definidos; lembrete esta dentro do horario; depois pede aprovacao antes de concluir.

**Autonomo com excecoes**

Segue sozinho quando:

- aula terminou.
- professor foi identificado.
- tipos de nota permitidos estao definidos.
- lembrete esta dentro do horario.
- nota ainda nao foi registrada.

Chama equipe quando:

- professor nao tem permissao.
- nota envolve restricao ou cuidado.
- aula nao foi fechada.
- aluno teve evento sensivel.
- canal, cota ou permissao bloqueia lembrete.

**Autonomo**

Conclui sozinho quando:

- bloqueado: acima do teto deste fluxo.

Para quando:

- bloqueado: acima do teto deste fluxo.

**Se parar**

criar tarefa/caso em /app/aulas/[id]; /app/historico; tarefa e manter auditoria do motivo.

**Ajustes relacionados**

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


### Rotina: Historico protegido

#### Restricao/cuidado

- ID interno: `G3`.
- Modo padrao: `Autonomo com aprovacao`.
- Teto: `Autonomo com aprovacao`.

**Manual**

A Taliya cria uma tarefa para preparar restricao ou cuidado para aprovacao; inclui no contexto: aluno foi identificado; restricao ou cuidado foi classificado; visibilidade esta definida; a equipe executa e registra o resultado.

**Copiloto**

A Taliya sugere preparar restricao ou cuidado para aprovacao; mostra como base: aluno foi identificado; restricao ou cuidado foi classificado; visibilidade esta definida; a equipe decide se aceita, edita ou descarta.

**Autonomo com aprovacao**

A Taliya prepara restricao/cuidado, valida: aluno foi identificado; restricao ou cuidado foi classificado; visibilidade esta definida; dono do caso esta atribuido; depois pede aprovacao antes de concluir.

**Autonomo com excecoes**

Segue sozinho quando:

- bloqueado: acima do teto deste fluxo.

Chama equipe quando:

- bloqueado: acima do teto deste fluxo.

**Autonomo**

Conclui sozinho quando:

- bloqueado: acima do teto deste fluxo.

Para quando:

- bloqueado: acima do teto deste fluxo.

**Se parar**

criar tarefa/caso em /app/historico; /app/alunos/[id]; caso/aprovacao e manter auditoria do motivo.

**Ajustes relacionados**

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


### Rotina: Aula com contexto

#### Objetivo/evolucao

- ID interno: `G4`.
- Modo padrao: `Autonomo com excecoes`.
- Teto: `Autonomo com excecoes`.

**Manual**

A Taliya cria uma tarefa para acompanhar objetivo e evolucao do aluno; inclui no contexto: aluno foi identificado; objetivo ou evolucao esta dentro dos tipos permitidos; frequencia de acompanhamento esta definida; a equipe executa e registra o resultado.

**Copiloto**

A Taliya sugere acompanhar objetivo e evolucao do aluno; mostra como base: aluno foi identificado; objetivo ou evolucao esta dentro dos tipos permitidos; frequencia de acompanhamento esta definida; a equipe decide se aceita, edita ou descarta.

**Autonomo com aprovacao**

A Taliya prepara objetivo/evolucao, valida: aluno foi identificado; objetivo ou evolucao esta dentro dos tipos permitidos; frequencia de acompanhamento esta definida; professor ou responsavel esta atribuido; depois pede aprovacao antes de concluir.

**Autonomo com excecoes**

Segue sozinho quando:

- aluno foi identificado.
- objetivo ou evolucao esta dentro dos tipos permitidos.
- frequencia de acompanhamento esta definida.
- professor ou responsavel esta atribuido.
- historico permitido esta disponivel.

Chama equipe quando:

- evolucao envolve saude ou restricao.
- professor sem permissao.
- dado historico esta conflitante.
- acao exige contato sensivel.
- permissao ou cota bloqueia resumo.

**Autonomo**

Conclui sozinho quando:

- bloqueado: acima do teto deste fluxo.

Para quando:

- bloqueado: acima do teto deste fluxo.

**Se parar**

criar tarefa/caso em /app/alunos/[id]/linha-do-tempo; tarefa e manter auditoria do motivo.

**Ajustes relacionados**

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


### Rotina: Historico protegido

#### Contexto para agente

- ID interno: `G5`.
- Modo padrao: `Autonomo com aprovacao`.
- Teto: `Autonomo com aprovacao`.

**Manual**

A Taliya cria uma tarefa para preparar contexto permitido para agente; inclui no contexto: escopo de dados foi definido; dados permitidos foram listados; objetivo de uso esta claro; a equipe executa e registra o resultado.

**Copiloto**

A Taliya sugere preparar contexto permitido para agente; mostra como base: escopo de dados foi definido; dados permitidos foram listados; objetivo de uso esta claro; a equipe decide se aceita, edita ou descarta.

**Autonomo com aprovacao**

A Taliya prepara contexto para agente, valida: escopo de dados foi definido; dados permitidos foram listados; objetivo de uso esta claro; aprovador esta definido; depois pede aprovacao antes de concluir.

**Autonomo com excecoes**

Segue sozinho quando:

- bloqueado: acima do teto deste fluxo.

Chama equipe quando:

- bloqueado: acima do teto deste fluxo.

**Autonomo**

Conclui sozinho quando:

- bloqueado: acima do teto deste fluxo.

Para quando:

- bloqueado: acima do teto deste fluxo.

**Se parar**

criar tarefa/caso em /app/historico/permissoes; /app/aprovacoes e manter auditoria do motivo.

**Ajustes relacionados**

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

#### Documentos/anamnese

- ID interno: `G6`.
- Modo padrao: `Autonomo com aprovacao`.
- Teto: `Autonomo com aprovacao`.

**Manual**

A Taliya cria uma tarefa para preparar documentos ou anamnese para aprovacao; inclui no contexto: documento exigido foi identificado; aluno foi identificado; responsavel esta definido; a equipe executa e registra o resultado.

**Copiloto**

A Taliya sugere preparar documentos ou anamnese para aprovacao; mostra como base: documento exigido foi identificado; aluno foi identificado; responsavel esta definido; a equipe decide se aceita, edita ou descarta.

**Autonomo com aprovacao**

A Taliya prepara documentos/anamnese, valida: documento exigido foi identificado; aluno foi identificado; responsavel esta definido; visibilidade esta clara; depois pede aprovacao antes de concluir.

**Autonomo com excecoes**

Segue sozinho quando:

- bloqueado: acima do teto deste fluxo.

Chama equipe quando:

- bloqueado: acima do teto deste fluxo.

**Autonomo**

Conclui sozinho quando:

- bloqueado: acima do teto deste fluxo.

Para quando:

- bloqueado: acima do teto deste fluxo.

**Se parar**

criar tarefa/caso em /app/historico/documentos; /app/aprovacoes; tarefa e manter auditoria do motivo.

**Ajustes relacionados**

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

#### Correcao historico

- ID interno: `G7`.
- Modo padrao: `Autonomo com aprovacao`.
- Teto: `Autonomo com aprovacao`.

**Manual**

A Taliya cria uma tarefa para preparar correcao de historico para aprovacao; inclui no contexto: evento historico foi identificado; motivo obrigatorio foi informado; valor anterior foi preservado; a equipe executa e registra o resultado.

**Copiloto**

A Taliya sugere preparar correcao de historico para aprovacao; mostra como base: evento historico foi identificado; motivo obrigatorio foi informado; valor anterior foi preservado; a equipe decide se aceita, edita ou descarta.

**Autonomo com aprovacao**

A Taliya prepara correcao historico, valida: evento historico foi identificado; motivo obrigatorio foi informado; valor anterior foi preservado; impacto da correcao foi mostrado; depois pede aprovacao antes de concluir.

**Autonomo com excecoes**

Segue sozinho quando:

- bloqueado: acima do teto deste fluxo.

Chama equipe quando:

- bloqueado: acima do teto deste fluxo.

**Autonomo**

Conclui sozinho quando:

- bloqueado: acima do teto deste fluxo.

Para quando:

- bloqueado: acima do teto deste fluxo.

**Se parar**

criar tarefa/caso em /app/historico; /app/auditoria; aprovacao e manter auditoria do motivo.

**Ajustes relacionados**

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


### Rotina: Aula com contexto

#### Repasse entre professores

- ID interno: `G8`.
- Modo padrao: `Autonomo com excecoes`.
- Teto: `Autonomo com excecoes`.

**Manual**

A Taliya cria uma tarefa para preparar repasse entre professores; inclui no contexto: professor origem e destino foram identificados; campos do resumo estao definidos; alunos ou aulas relacionados foram listados; a equipe executa e registra o resultado.

**Copiloto**

A Taliya sugere preparar repasse entre professores; mostra como base: professor origem e destino foram identificados; campos do resumo estao definidos; alunos ou aulas relacionados foram listados; a equipe decide se aceita, edita ou descarta.

**Autonomo com aprovacao**

A Taliya prepara repasse entre professores, valida: professor origem e destino foram identificados; campos do resumo estao definidos; alunos ou aulas relacionados foram listados; visibilidade do historico permite repasse; depois pede aprovacao antes de concluir.

**Autonomo com excecoes**

Segue sozinho quando:

- professor origem e destino foram identificados.
- campos do resumo estao definidos.
- alunos ou aulas relacionados foram listados.
- visibilidade do historico permite repasse.
- mensagem interna esta pronta.

Chama equipe quando:

- professor destino sem permissao.
- resumo inclui dado protegido.
- aula ou professor mudou.
- contexto esta incompleto.
- permissao ou cota bloqueia repasse.

**Autonomo**

Conclui sozinho quando:

- bloqueado: acima do teto deste fluxo.

Para quando:

- bloqueado: acima do teto deste fluxo.

**Se parar**

criar tarefa/caso em /app/professores; /app/tarefas e manter auditoria do motivo.

**Ajustes relacionados**

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

#### Lembrete professor

- ID interno: `G9`.
- Modo padrao: `Autonomo`.
- Teto: `Autonomo`.

**Manual**

A Taliya cria uma tarefa para enviar lembrete para professor; inclui no contexto: professor foi identificado; horario ou frequencia chegou; destino do lembrete esta definido; a equipe executa e registra o resultado.

**Copiloto**

A Taliya sugere enviar lembrete para professor; mostra como base: professor foi identificado; horario ou frequencia chegou; destino do lembrete esta definido; a equipe decide se aceita, edita ou descarta.

**Autonomo com aprovacao**

A Taliya prepara lembrete professor, valida: professor foi identificado; horario ou frequencia chegou; destino do lembrete esta definido; conteudo nao inclui dado protegido indevido; depois pede aprovacao antes de concluir.

**Autonomo com excecoes**

Segue sozinho quando:

- professor foi identificado.
- horario ou frequencia chegou.
- destino do lembrete esta definido.
- conteudo nao inclui dado protegido indevido.
- lembrete ainda nao foi enviado.

Chama equipe quando:

- professor sem canal ou permissao.
- lembrete duplicado.
- conteudo depende de dado protegido.
- aula foi alterada.
- canal, cota ou permissao bloqueia envio.

**Autonomo**

Conclui sozinho quando:

- professor foi identificado.
- horario ou frequencia chegou.
- destino do lembrete esta definido.
- conteudo nao inclui dado protegido indevido.
- lembrete ainda nao foi enviado.
- nenhuma regra exige aprovacao ou chamada humana.

Para quando:

- professor sem canal ou permissao.
- lembrete duplicado.
- conteudo depende de dado protegido.
- aula foi alterada.
- canal, cota ou permissao bloqueia envio.
- canal, permissao, cota, opt-out, integracao ou incidente bloqueia a conclusao.

**Se parar**

criar tarefa/caso em /app/professores; /app/tarefas e manter auditoria do motivo.

**Ajustes relacionados**

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


### Rotina: Historico protegido

#### Compartilhar contexto

- ID interno: `G10`.
- Modo padrao: `Autonomo com aprovacao`.
- Teto: `Autonomo com aprovacao`.

**Manual**

A Taliya cria uma tarefa para preparar compartilhamento de contexto; inclui no contexto: destinatario foi identificado; dados permitidos foram selecionados; objetivo do compartilhamento esta claro; a equipe executa e registra o resultado.

**Copiloto**

A Taliya sugere preparar compartilhamento de contexto; mostra como base: destinatario foi identificado; dados permitidos foram selecionados; objetivo do compartilhamento esta claro; a equipe decide se aceita, edita ou descarta.

**Autonomo com aprovacao**

A Taliya prepara compartilhar contexto, valida: destinatario foi identificado; dados permitidos foram selecionados; objetivo do compartilhamento esta claro; preview foi gerado; depois pede aprovacao antes de concluir.

**Autonomo com excecoes**

Segue sozinho quando:

- bloqueado: acima do teto deste fluxo.

Chama equipe quando:

- bloqueado: acima do teto deste fluxo.

**Autonomo**

Conclui sozinho quando:

- bloqueado: acima do teto deste fluxo.

Para quando:

- bloqueado: acima do teto deste fluxo.

**Se parar**

criar tarefa/caso em /app/aprovacoes; /app/conversas/[id] e manter auditoria do motivo.

**Ajustes relacionados**

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

#### Permissao historico

- ID interno: `G11`.
- Modo padrao: `Autonomo com aprovacao`.
- Teto: `Autonomo com aprovacao`.

**Manual**

A Taliya cria uma tarefa para preparar permissao de historico; inclui no contexto: papel ou perfil foi identificado; escopo de visibilidade esta definido; impacto foi mostrado; a equipe executa e registra o resultado.

**Copiloto**

A Taliya sugere preparar permissao de historico; mostra como base: papel ou perfil foi identificado; escopo de visibilidade esta definido; impacto foi mostrado; a equipe decide se aceita, edita ou descarta.

**Autonomo com aprovacao**

A Taliya prepara permissao historico, valida: papel ou perfil foi identificado; escopo de visibilidade esta definido; impacto foi mostrado; responsavel esta atribuido; depois pede aprovacao antes de concluir.

**Autonomo com excecoes**

Segue sozinho quando:

- bloqueado: acima do teto deste fluxo.

Chama equipe quando:

- bloqueado: acima do teto deste fluxo.

**Autonomo**

Conclui sozinho quando:

- bloqueado: acima do teto deste fluxo.

Para quando:

- bloqueado: acima do teto deste fluxo.

**Se parar**

criar tarefa/caso em /app/historico/permissoes; /app/configuracoes/permissoes; auditoria e manter auditoria do motivo.

**Ajustes relacionados**

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


### Rotina: Aula com contexto

#### Linha do tempo

- ID interno: `G12`.
- Modo padrao: `Autonomo com excecoes`.
- Teto: `Autonomo com excecoes`.

**Manual**

A Taliya cria uma tarefa para organizar linha do tempo do aluno; inclui no contexto: aluno foi identificado; tipos de evento estao permitidos; filtro padrao esta definido; a equipe executa e registra o resultado.

**Copiloto**

A Taliya sugere organizar linha do tempo do aluno; mostra como base: aluno foi identificado; tipos de evento estao permitidos; filtro padrao esta definido; a equipe decide se aceita, edita ou descarta.

**Autonomo com aprovacao**

A Taliya prepara linha do tempo, valida: aluno foi identificado; tipos de evento estao permitidos; filtro padrao esta definido; responsavel esta atribuido; depois pede aprovacao antes de concluir.

**Autonomo com excecoes**

Segue sozinho quando:

- aluno foi identificado.
- tipos de evento estao permitidos.
- filtro padrao esta definido.
- responsavel esta atribuido.
- historico pode ser exibido sem dado indevido.

Chama equipe quando:

- evento protegido aparece.
- historico conflita ou esta incompleto.
- usuario nao tem permissao.
- filtro mostra dado sensivel.
- permissao ou cota bloqueia exibicao.

**Autonomo**

Conclui sozinho quando:

- bloqueado: acima do teto deste fluxo.

Para quando:

- bloqueado: acima do teto deste fluxo.

**Se parar**

criar tarefa/caso em /app/alunos/[id]/linha-do-tempo; tarefa e manter auditoria do motivo.

**Ajustes relacionados**

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
