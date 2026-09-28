# Taliya Agent Flow Deep Map

## Objetivo

Este documento e a fonte de verdade dos fluxos operacionais do MVP da Taliya para studios de Pilates.

A Taliya entrega fluxos prontos por agente. O studio nao desenha fluxos do zero; ele configura como cada agente se comporta dentro dos fluxos mapeados: tom, mensagens, autonomia, limites, aprovacao, responsavel, janelas de envio e excecoes.

## Principios Do Produto

- Atendimento classifica, responde duvidas permitidas e encaminha.
- Agenda organiza horarios, presenca, faltas, reposicoes, vagas e experimentais.
- Vendas conduz interessados, aula experimental, follow-up, objecoes e pre-matricula.
- Financeiro cuida de vencimentos, pagamentos, links, comprovantes e excecoes financeiras.
- Retencao detecta risco, inatividade, retorno, cancelamento e reativacao.
- Gestao prioriza, recomenda, consolida gargalos e organiza a fila humana.
- Historico/Evolucao fornece contexto interno seguro; nao envia orientacao clinica automatica.

## Canais

- `whatsapp`: conversa externa com aluno, interessado ou ex-aluno.
- `sistema`: Taliya em web ou app. A plataforma muda, mas a superficie operacional e a mesma: configuracao, financeiro, filas, relatorios, setup, auditoria, chamada, observacoes, contexto do aluno, tarefas e notificacoes.
- `hibrido`: combina WhatsApp com o sistema.

## Autonomia Padrao

- `automatico`: o agente pode agir sozinho dentro da regra configurada.
- `copiloto`: o agente prepara a acao e espera aprovacao.
- `customizado`: o studio define ate onde o agente pode ir automaticamente.
- `humano`: sempre exige pessoa responsavel.

## Estados Finais

- `resolvido`: fluxo terminou.
- `aguardando_contato`: espera aluno, interessado ou ex-aluno.
- `aguardando_equipe`: espera responsavel interno.
- `acao_registrada`: sistema foi atualizado.
- `tarefa_criada`: pendencia interna criada.
- `handoff_humano`: humano precisa assumir.
- `proximo_fluxo`: outro agente/fluxo continua.
- `sem_acao`: dado, permissao ou contexto insuficiente.
- `pausado`: opt-out, seguranca, limite ou politica bloqueou.

## Economia De Creditos

Todos os agentes seguem economia automatica por padrao:

- usar regra antes de IA;
- usar IA leve antes de modelo mais caro;
- nao reprocessar contexto ja resumido;
- decidir uso de WhatsApp pago por fluxo, com categoria, limite e aprovacao;
- evitar WhatsApp pago quando a prioridade do fluxo for baixa;
- agrupar acoes repetidas;
- pedir aprovacao para campanhas, lotes e mensagens caras;
- pausar acoes nao essenciais perto do limite de creditos;
- priorizar atendimento, agenda, financeiro e risco de retencao antes de mensagens cosmeticas.

## 1. Agente Atendimento

Responsabilidade: entrada e triagem. Atendimento entende a mensagem, responde apenas o que esta permitido e encaminha para o agente dono da rotina.

### A1. Nova Conversa

- Canal: `whatsapp`
- Autonomia padrao: `automatico`
- Trigger: mensagem de contato desconhecido ou interessado.

Subfluxos:

- Identificar contato
  - telefone de aluno -> A3.
  - telefone de interessado -> recuperar etapa comercial.
  - desconhecido -> criar contato leve.
  - sem nome -> perguntar somente se necessario.
- Classificar intencao
  - valores/planos -> Vendas C1.
  - horarios/disponibilidade -> Agenda B7.
  - aula experimental -> Vendas C2.
  - endereco/funcionamento -> A2.
  - humano -> A5.
  - confuso -> pedir uma clarificacao curta.
- Guardrail
  - saude, dor, lesao, desconto, excecao, cancelamento ou tom irritado -> A5.

Estados finais: `proximo_fluxo`, `aguardando_contato`, `handoff_humano`, `pausado`.

### A2. Duvidas Permitidas

- Canal: `whatsapp`
- Autonomia padrao: `automatico`
- Trigger: pergunta objetiva sobre dados publicos ou regras aprovadas.

Subfluxos:

- Dados publicos
  - endereco.
  - horario de funcionamento.
  - como funciona a aula experimental.
  - tipos de aula.
  - preparo para primeira aula.
- Dados operacionais
  - regra de reposicao.
  - regra de ausencia.
  - canais de contato.
  - horarios disponiveis em alto nivel.
- Dados comerciais
  - pergunta sobre valores -> Vendas C1.
  - pergunta sobre plano -> Vendas C1.
  - pergunta sobre matricula -> Vendas C6.
- Se a resposta nao existe
  - criar tarefa para completar base.
  - responder que a equipe vai confirmar.

Estados finais: `resolvido`, `proximo_fluxo`, `tarefa_criada`, `aguardando_contato`.

### A3. Aluno Existente

- Canal: `whatsapp`
- Autonomia padrao: `automatico`
- Trigger: aluno manda mensagem operacional.

Subfluxos:

- Agenda
  - falta -> Agenda B2.
  - reposicao -> Agenda B5.
  - confirmacao -> Agenda B1.
  - mudar horario fixo -> Agenda B8.
- Financeiro
  - link/Pix -> Financeiro D3.
  - vencimento -> Financeiro D1/D2.
  - plano -> Financeiro D5.
- Retencao
  - quer voltar -> Retencao E3.
  - quer parar/cancelar -> Retencao E4 + Financeiro D6.
  - insatisfacao -> Retencao E4.
- Historico
  - dor, lesao, restricao ou cuidado -> Historico G3 + A5.
- Ambiguidade
  - "nao vou conseguir" sem data -> perguntar qual aula.
  - "meu plano" sem detalhe -> perguntar se e pagamento, renovacao ou mudanca.

Estados finais: `proximo_fluxo`, `aguardando_contato`, `handoff_humano`.

### A4. Fora Do Escopo

- Canal: `whatsapp`
- Autonomia padrao: `customizado`
- Trigger: mensagem que nao pertence aos fluxos principais.

Subfluxos:

- fornecedor/parceria -> resposta padrao ou tarefa.
- vaga de emprego -> resposta padrao ou tarefa.
- spam -> pausar/ignorar.
- prompt injection -> bloquear e registrar.
- pedido clinico/medico -> A5.

Estados finais: `pausado`, `tarefa_criada`, `handoff_humano`.

### A5. Handoff Humano

- Canal: `hibrido`
- Autonomia padrao: `humano`
- Trigger: excecao, seguranca, baixa confianca ou pedido humano.

Subfluxos:

- Preparar resumo
  - quem e o contato.
  - historico recente.
  - intencao detectada.
  - motivo do handoff.
  - sugestao de resposta se permitido.
- Encaminhar
  - responsavel do fluxo.
  - fila geral.
  - dono do studio.
- Pausar
  - pausar automacao apenas naquela conversa quando necessario.

Estados finais: `handoff_humano`, `aguardando_equipe`, `tarefa_criada`.

### A6. Consentimento, Opt-Out E Janela De Atendimento

- Canal: `whatsapp` ou `sistema`
- Autonomia padrao: `automatico`
- Trigger: contato pede para parar mensagens, conversa fora de horario ou politica de consentimento exige controle.

Subfluxos:

- Opt-out
  - contato pede para parar -> registrar opt-out.
  - contato pede menos mensagens -> ajustar preferencia se permitido.
  - contato volta a chamar depois -> respeitar politica configurada.
- Janela de atendimento
  - dentro do horario -> seguir fluxo normal.
  - fora do horario -> resposta curta aprovada ou aguardar.
  - urgencia/sensivel fora do horario -> handoff/tarefa prioritaria.
- Consentimento
  - contato novo sem consentimento para campanhas -> nao inserir em campanhas.
  - aluno ativo com comunicacao operacional -> permitir mensagens operacionais configuradas.
  - campanha/reativacao -> exigir regra aprovada.

Estados finais: `pausado`, `acao_registrada`, `proximo_fluxo`, `tarefa_criada`.

### A7. Identidade, Duplicidade E Midias

- Canal: `whatsapp` ou `sistema`
- Autonomia padrao: `customizado`
- Trigger: contato nao identificado, telefone duplicado, audio, imagem, comprovante ou documento.

Subfluxos:

- Identidade
  - telefone bate com um aluno -> vincular conversa.
  - telefone bate com mais de um contato -> perguntar identificador minimo ou tarefa.
  - aluno usa telefone de responsavel/familiar -> vincular com cuidado.
  - contato novo parecido com cadastro existente -> sugerir merge para equipe.
- Midias
  - audio -> transcrever se permitido e seguir classificacao.
  - imagem/documento -> classificar tipo e encaminhar.
  - comprovante -> Financeiro D4.
  - documento clinico/sensivel -> Historico G6 + humano se necessario.
- Duplicidade
  - possivel duplicado -> nao criar novo aluno automaticamente.
  - merge de contato -> sempre copiloto/humano.

Estados finais: `acao_registrada`, `tarefa_criada`, `proximo_fluxo`, `handoff_humano`.

### A8. Privacidade, Dados E Preferencias Do Contato

- Canal: `whatsapp` ou `sistema`
- Autonomia padrao: `copiloto`
- Trigger: contato pede dados, exclusao, correcao cadastral, historico de mensagens ou mudanca de preferencia.

Subfluxos:

- Pedido de dados
  - aluno pede seus dados cadastrais -> validar identidade e criar tarefa/fluxo seguro.
  - responsavel/familiar pede dados de aluno -> validar permissao antes de responder.
  - interessado pede exclusao -> registrar solicitacao e pausar contato.
- Correcao cadastral
  - telefone.
  - nome.
  - email.
  - data de nascimento.
  - contato de emergencia/responsavel.
- Preferencias
  - prefere nao receber campanhas.
  - prefere horario especifico de contato.
  - prefere falar so com humano.
- Guardrail
  - nao enviar historico sensivel automaticamente.
  - nao expor dados de outro aluno.

Estados finais: `tarefa_criada`, `acao_registrada`, `pausado`, `handoff_humano`.

### A9. Conversas De Grupo, Familiares E Responsaveis

- Canal: `whatsapp`
- Autonomia padrao: `customizado`
- Trigger: mensagem vem de grupo, familiar, responsavel financeiro ou telefone compartilhado.

Subfluxos:

- Origem
  - grupo de WhatsApp.
  - responsavel financeiro.
  - familiar usando telefone proprio.
  - aluno usando telefone de outra pessoa.
- Caminhos
  - grupo -> evitar dados pessoais e direcionar para conversa individual.
  - responsavel autorizado -> seguir fluxo permitido.
  - responsavel nao autorizado -> pedir validacao/humano.
  - duvida operacional geral -> responder sem expor dados.
- Dados sensiveis
  - financeiro, saude, historico e frequencia nao devem ser expostos sem autorizacao.

Estados finais: `proximo_fluxo`, `aguardando_contato`, `handoff_humano`, `pausado`.

### A10. Ciclo De Vida Da Conversa E SLA

- Canal: `whatsapp` ou `sistema`
- Autonomia padrao: `automatico`
- Trigger: conversa fica aberta, contato responde depois de muito tempo, agente aguarda retorno ou SLA interno vence.

Subfluxos:

- Abertura
  - conversa nova.
  - conversa reaberta.
  - resposta a fluxo antigo.
  - mensagem recebida enquanto outro fluxo esta aguardando.
- Continuidade
  - ainda pertence ao mesmo fluxo -> retomar estado.
  - mudou de assunto -> reclassificar e iniciar novo fluxo.
  - existe acao pendente da equipe -> avisar responsavel.
  - existe mensagem agendada -> cancelar, reagendar ou atualizar.
- Encerramento
  - resolvida automaticamente.
  - sem resposta apos limite.
  - transferida para humano.
  - pausada por opt-out.
- SLA interno
  - interessado quente sem resposta -> Vendas C5.
  - aluno aguardando equipe -> Gestao F3.
  - conversa critica vencida -> tarefa prioritaria.

Estados finais: `resolvido`, `proximo_fluxo`, `tarefa_criada`, `aguardando_equipe`, `pausado`.

## 2. Agente Agenda

Responsabilidade: horarios, presenca, faltas, reposicoes, lista de espera, vagas abertas, aula experimental e mudanca de horario.

### B1. Confirmacao De Presenca

- Canal: `whatsapp`
- Autonomia padrao: `automatico`
- Trigger: janela configurada antes da aula.

Subfluxos:

- Enviar confirmacao
  - somente para aulas/planos configurados.
  - evitar insistencia se credito estiver baixo.
- Interpretar resposta
  - confirma -> marcar previsto.
  - nao vai -> B2.
  - quer remarcar -> B5.
  - pergunta endereco/preparo -> Atendimento A2.
  - nao responde -> uma tentativa ou encerrar.

Estados finais: `acao_registrada`, `aguardando_contato`, `proximo_fluxo`.

### B2. Falta Com Aviso

- Canal: `hibrido`
- Autonomia padrao: `customizado`
- Trigger: aluno avisa que nao vai.

Subfluxos:

- Identificar aula
  - aula clara no contexto -> seguir.
  - varias aulas possiveis -> pedir selecao.
  - nenhuma aula encontrada -> tarefa ou pergunta.
- Aplicar regra
  - dentro do prazo e plano permite -> criar credito.
  - fora do prazo -> registrar sem credito ou pedir aprovacao.
  - studio nao usa reposicao -> apenas registrar ausencia.
  - excecao -> A5.
- Liberar vaga
  - permitido -> B4.
  - nao permitido -> apenas registrar.
  - turma sensivel/restrita -> copiloto.

Estados finais: `acao_registrada`, `proximo_fluxo`, `handoff_humano`.

### B3. No-Show

- Canal: `sistema` ou `hibrido`
- Autonomia padrao: `customizado`
- Trigger: aula terminou sem presenca registrada.

Subfluxos:

- Origem
  - professor marcou falta.
  - check-in ausente.
  - turma encerrada.
- Acoes
  - primeira ocorrencia -> registrar e opcionalmente mensagem leve.
  - recorrente -> Retencao E1.
  - sem regra de contato -> tarefa interna.
  - justificativa sensivel depois -> A5/Historico G3.

Estados finais: `acao_registrada`, `tarefa_criada`, `proximo_fluxo`.

### B4. Recuperar Vaga Aberta

- Canal: `hibrido`
- Autonomia padrao: `customizado`
- Trigger: vaga aberta por falta, cancelamento ou lista de espera.

Subfluxos:

- Selecionar candidato
  - reposicao pendente.
  - lista de espera.
  - preferencia de horario.
  - aluno em risco que combina com turma.
- Politica de convite
  - um por vez.
  - lote limitado.
  - apenas sugestao para equipe.
- Resposta
  - aceita -> reservar e registrar.
  - recusa -> proximo candidato.
  - nao responde -> esperar janela e seguir.
  - pede outro horario -> B5.
- Economia
  - nao abrir conversa paga se vaga for de baixa prioridade.
  - limitar tentativas por vaga.

Estados finais: `resolvido`, `acao_registrada`, `aguardando_contato`, `sem_acao`.

### B5. Reposicao Ou Remarcacao

- Canal: `whatsapp`
- Autonomia padrao: `customizado`
- Trigger: aluno pede reposicao, remarcacao ou encaixe.

Subfluxos:

- Validar direito
  - tem credito.
  - nao tem credito.
  - credito vencido.
  - regra depende de aprovacao.
- Buscar horario
  - horario preferido.
  - horario equivalente.
  - turma com capacidade.
  - restricoes/professor.
- Concluir
  - aluno escolhe -> reservar.
  - sem opcao -> lista de espera/tarefa.
  - pedido especial -> A5.

Estados finais: `resolvido`, `tarefa_criada`, `handoff_humano`, `aguardando_contato`.

### B6. Lista De Espera

- Canal: `hibrido`
- Autonomia padrao: `customizado`
- Trigger: aluno quer horario cheio ou vaga abre.

Subfluxos:

- Entrada na lista
  - pedido do aluno.
  - adicionado pela equipe.
  - sugestao do sistema.
- Prioridade
  - ordem de entrada.
  - plano.
  - perfil de horario.
  - risco de retencao.
  - decisao manual.
- Convite
  - aceita -> reservar.
  - nao responde -> proximo.
  - ninguem aceita -> Gestao F1/F4.

Estados finais: `resolvido`, `aguardando_contato`, `sem_acao`, `proximo_fluxo`.

### B7. Disponibilidade Para Aula Experimental

- Canal: `hibrido`
- Autonomia padrao: `automatico`
- Trigger: Vendas ou Atendimento precisam de horario para interessado.

Subfluxos:

- Coleta minima
  - nome se necessario.
  - preferencia de turno.
  - primeira vez ou nao.
  - restricao apenas para encaminhar humano.
- Buscar vaga
  - horario experimental dedicado.
  - vaga em turma existente.
  - professor apto.
- Saidas
  - opcoes encontradas -> Vendas C2 confirma.
  - sem opcao -> tarefa ou alternativa.
  - restricao/saude -> A5.

Estados finais: `proximo_fluxo`, `tarefa_criada`, `aguardando_contato`, `handoff_humano`.

### B8. Mudanca De Horario Fixo

- Canal: `hibrido`
- Autonomia padrao: `customizado`
- Trigger: aluno pede troca de horario recorrente.

Subfluxos:

- Motivo
  - rotina/trabalho.
  - incompatibilidade com turma.
  - recomendacao da equipe.
  - insatisfacao.
- Caminhos
  - vaga equivalente -> sugerir troca.
  - sem vaga -> lista de espera.
  - muda frequencia/plano -> Financeiro D5.
  - insatisfacao -> Retencao E4.

Estados finais: `resolvido`, `tarefa_criada`, `proximo_fluxo`, `handoff_humano`.

### B9. Cancelamento Ou Alteracao Pelo Studio

- Canal: `hibrido`
- Autonomia padrao: `copiloto`
- Trigger: aula cancelada, professor ausente, feriado, manutencao, sala indisponivel ou mudanca de grade.

Subfluxos:

- Motivo
  - professor ausente.
  - feriado/recesso.
  - sala/equipamento indisponivel.
  - turma cancelada por baixa ocupacao.
  - ajuste manual da equipe.
- Impacto
  - alunos afetados.
  - creditos/reposicoes necessarios.
  - alternativas de horario.
  - professor substituto disponivel.
- Comunicacao
  - mensagem em lote exige aprovacao.
  - casos individuais podem ser automaticos se regra permitir.
  - aluno responde pedindo alternativa -> B5/B8.

Estados finais: `tarefa_criada`, `proximo_fluxo`, `acao_registrada`, `aguardando_contato`.

### B10. Conflito De Capacidade, Sala Ou Professor

- Canal: `sistema`
- Autonomia padrao: `copiloto`
- Trigger: overbooking, professor duplicado, sala cheia, equipamento indisponivel ou turma incompatvel.

Subfluxos:

- Conflito
  - mais alunos que capacidade.
  - professor em duas turmas.
  - sala/equipamento reservado em duplicidade.
  - aluno alocado em turma inadequada.
- Resolucao
  - sugerir troca.
  - criar tarefa para equipe.
  - avisar antes de enviar mensagem externa.
  - bloquear reserva automatica quando houver conflito.

Estados finais: `tarefa_criada`, `handoff_humano`, `sem_acao`.

### B11. Criacao Ou Ajuste De Grade

- Canal: `sistema`
- Autonomia padrao: `copiloto`
- Trigger: equipe altera turma, cria horario, muda professor, capacidade ou recorrencia.

Subfluxos:

- Mudanca
  - nova turma.
  - alteracao de capacidade.
  - alteracao de professor.
  - alteracao de recorrencia.
  - pausa temporaria da turma.
- Impacto
  - alunos fixos afetados.
  - lista de espera.
  - reposicoes possiveis.
  - mensagens necessarias.
- Saidas
  - sugerir impactos.
  - criar tarefas.
  - acionar comunicacao se aprovado.

Estados finais: `tarefa_criada`, `acao_registrada`, `proximo_fluxo`.

### B12. Aula Experimental No-Show Ou Reagendamento

- Canal: `hibrido`
- Autonomia padrao: `customizado`
- Trigger: interessado nao comparece, cancela ou pede remarcacao da experimental.

Subfluxos:

- No-show
  - primeira vez -> Vendas C5.
  - recorrente -> encerrar ou tarefa.
- Cancelamento com aviso
  - pedir nova preferencia -> B7.
  - sem interesse -> Vendas C9.
- Remarcacao
  - buscar nova vaga.
  - limitar tentativas.
  - evitar mensagens pagas repetidas.

Estados finais: `proximo_fluxo`, `aguardando_contato`, `tarefa_criada`, `resolvido`.

### B13. Vencimento E Uso De Creditos De Reposicao

- Canal: `sistema` ou `hibrido`
- Autonomia padrao: `customizado`
- Trigger: credito de reposicao criado, perto de vencer, usado, vencido ou acumulado.

Subfluxos:

- Criacao
  - criado por falta dentro da regra.
  - criado manualmente pela equipe.
  - criado por cancelamento do studio.
- Uso
  - aluno pede horario -> B5.
  - equipe encaixa aluno -> registrar uso.
  - credito usado parcialmente/indevido -> tarefa.
- Vencimento
  - avisar se regra permite.
  - nao avisar se baixo impacto/credito perto do limite.
  - vencido -> registrar ou pedir aprovacao para excecao.
- Acumulo
  - muitos creditos -> Retencao E1/Gestao F4.

Estados finais: `acao_registrada`, `proximo_fluxo`, `tarefa_criada`, `sem_acao`.

### B14. Presenca Manual, Correcao E Auditoria De Aula

- Canal: `sistema`
- Autonomia padrao: `copiloto`
- Trigger: professor corrige chamada, aluno contesta falta, presenca duplicada ou aula encerrada com dado inconsistente.

Subfluxos:

- Correcao
  - estava presente mas marcou falta.
  - faltou mas marcou presente.
  - professor esqueceu chamada.
  - aluno mudou de turma no dia.
- Impacto
  - reposicao gerada indevidamente.
  - risco de retencao incorreto.
  - financeiro/plano afetado.
- Caminhos
  - sugerir correcao.
  - registrar auditoria.
  - atualizar fluxos dependentes.

Estados finais: `acao_registrada`, `tarefa_criada`, `proximo_fluxo`.

### B15. Primeira Aula Como Aluno

- Canal: `hibrido`
- Autonomia padrao: `customizado`
- Trigger: pre-matricula vira aluno, pagamento/contrato confirmado ou equipe libera inicio.

Subfluxos:

- Preparacao
  - confirmar horario fixo.
  - confirmar professor/turma.
  - enviar orientacoes aprovadas.
  - criar contexto inicial para professor.
- Dados faltantes
  - anamnese/documento pendente -> Historico G6.
  - contrato pendente -> Financeiro D11.
  - pagamento pendente -> Financeiro D1/D3.
- Depois da primeira aula
  - compareceu -> Historico G2 + Vendas/Financeiro se ainda houver pendencia.
  - nao compareceu -> B12/C5.
  - pediu ajuste -> B8.

Estados finais: `acao_registrada`, `proximo_fluxo`, `tarefa_criada`, `aguardando_contato`.

### B16. Aula Avulsa, Evento, Workshop Ou Turma Especial

- Canal: `hibrido`
- Autonomia padrao: `customizado`
- Trigger: studio cria aula nao recorrente, evento, workshop, turma extra ou vaga especial.

Subfluxos:

- Tipo
  - aula avulsa.
  - workshop.
  - turma extra.
  - aula especial para reposicao.
- Publico
  - alunos ativos.
  - lista de espera.
  - interessados.
  - ex-alunos.
- Caminhos
  - oferta para lista aprovada -> Vendas/Retencao conforme publico.
  - reserva de vaga -> Agenda.
  - pagamento necessario -> Financeiro.
  - comunicacao em lote -> aprovacao obrigatoria.

Estados finais: `proximo_fluxo`, `tarefa_criada`, `acao_registrada`, `aguardando_contato`.

## 3. Agente Vendas

Responsabilidade: transformar interessado em aula experimental, pre-matricula ou oportunidade clara para a equipe finalizar.

### C1. Valores E Planos

- Canal: `whatsapp`
- Autonomia padrao: `customizado`
- Trigger: pergunta sobre preco, plano, pacote ou frequencia.

Subfluxos:

- Politica comercial
  - informar valor direto.
  - informar faixa.
  - qualificar antes.
  - direcionar para aula experimental.
  - chamar humano.
- Qualificacao leve
  - frequencia desejada.
  - turno preferido.
  - objetivo.
  - experiencia previa.
- Caminhos
  - quer experimental -> C2.
  - quer fechar -> C6.
  - objecao -> C7.
  - desconto/negociacao -> A5.

Estados finais: `aguardando_contato`, `proximo_fluxo`, `handoff_humano`.

### C2. Aula Experimental

- Canal: `hibrido`
- Autonomia padrao: `automatico`
- Trigger: interessado quer conhecer o studio.

Subfluxos:

- Preparar reserva
  - pedir dados minimos.
  - solicitar Agenda B7.
  - confirmar opcao escolhida.
  - registrar origem.
- Caminhos
  - reservado -> C3.
  - nao respondeu -> C5.
  - quer remarcar -> Agenda B7.
  - restricao/saude -> A5.

Estados finais: `acao_registrada`, `proximo_fluxo`, `aguardando_contato`, `handoff_humano`.

### C3. Lembrete De Aula Experimental

- Canal: `whatsapp`
- Autonomia padrao: `automatico`
- Trigger: janela antes da aula experimental.

Subfluxos:

- Respostas
  - confirma -> manter.
  - remarca -> Agenda B7.
  - cancela -> C5 ou encerrar.
  - nao responde -> lembrete unico ou tarefa.

Estados finais: `acao_registrada`, `aguardando_contato`, `proximo_fluxo`.

### C4. Pos-Aula Experimental

- Canal: `whatsapp`
- Autonomia padrao: `customizado`
- Trigger: aula experimental concluida.

Subfluxos:

- Contexto
  - compareceu.
  - professor adicionou nota.
  - horario preferido.
  - plano provavel.
- Caminhos
  - quer plano -> C6.
  - tem objecao -> C7.
  - quer horario -> Agenda B8.
  - nao responde -> C5.
  - saude/restricao -> A5.

Estados finais: `aguardando_contato`, `proximo_fluxo`, `handoff_humano`.

### C5. Follow-Up Comercial

- Canal: `whatsapp` ou `sistema`
- Autonomia padrao: `customizado`
- Trigger: interessado parado.

Subfluxos:

- Motivos
  - pediu preco e sumiu.
  - marcou experimental e nao confirmou.
  - fez experimental e nao fechou.
  - no-show experimental.
- Cadencia
  - mensagem curta.
  - mensagem com ajuda concreta.
  - encerrar ou tarefa.
- Respostas
  - respondeu -> reclassificar.
  - sem resposta -> fechar sem perder historico.
  - opt-out -> pausar.

Estados finais: `aguardando_contato`, `tarefa_criada`, `pausado`, `resolvido`.

### C6. Pre-Matricula

- Canal: `hibrido`
- Autonomia padrao: `copiloto`
- Trigger: interessado quer entrar.

Subfluxos:

- Dados
  - nome completo.
  - plano/frequencia.
  - horario pretendido.
  - contato.
  - responsavel de finalizacao.
- Caminhos
  - checkout/link configurado -> Financeiro D3.
  - finalizacao manual -> tarefa para responsavel.
  - falta dado -> perguntar minimo.
  - excecao comercial -> A5.

Estados finais: `tarefa_criada`, `proximo_fluxo`, `acao_registrada`, `handoff_humano`.

### C7. Objecoes

- Canal: `whatsapp`
- Autonomia padrao: `customizado`
- Trigger: resistencia comercial.

Subfluxos:

- Tipos
  - preco.
  - falta de tempo.
  - inseguranca.
  - comparacao com outro studio.
  - "vou pensar".
- Caminhos
  - resposta aprovada -> responder.
  - quer pensar -> follow-up configurado.
  - negociacao/desconto -> A5.
  - nao quer mais -> encerrar com respeito.

Estados finais: `aguardando_contato`, `proximo_fluxo`, `handoff_humano`, `resolvido`.

### C8. Captura De Origem E Qualificacao Comercial

- Canal: `whatsapp` ou `sistema`
- Autonomia padrao: `automatico`
- Trigger: novo interessado entra no funil.

Subfluxos:

- Origem
  - Instagram.
  - indicacao.
  - trafego pago.
  - Google/site.
  - WhatsApp direto.
  - outro aluno.
- Qualificacao
  - objetivo.
  - turno.
  - frequencia.
  - experiencia previa.
  - urgencia.
- Saida
  - atualizar CRM.
  - ajustar follow-up.
  - sugerir agente/fluxo seguinte.

Estados finais: `acao_registrada`, `proximo_fluxo`, `aguardando_contato`.

### C9. Perda Comercial E Motivo

- Canal: `whatsapp` ou `sistema`
- Autonomia padrao: `customizado`
- Trigger: interessado diz que nao quer, escolheu outro studio, achou caro ou parou definitivamente.

Subfluxos:

- Motivos
  - preco.
  - horario.
  - distancia.
  - escolheu outro studio.
  - desistiu por enquanto.
  - sem resposta apos limite.
- Caminhos
  - registrar motivo.
  - criar lembrete futuro se permitido.
  - enviar encerramento respeitoso.
  - opt-out -> pausar.

Estados finais: `resolvido`, `acao_registrada`, `pausado`, `tarefa_criada`.

### C10. Indicacao E Conversao Por Aluno

- Canal: `whatsapp` ou `sistema`
- Autonomia padrao: `customizado`
- Trigger: aluno indica alguem ou interessado menciona indicacao.

Subfluxos:

- Indicado
  - criar interessado vinculado ao aluno.
  - seguir C1/C2.
  - registrar origem como indicacao.
- Aluno indicador
  - agradecer se permitido.
  - registrar beneficio se existir.
  - desconto/beneficio especial -> Financeiro D6/humano.

Estados finais: `acao_registrada`, `proximo_fluxo`, `handoff_humano`.

### C11. Checkout, Link De Contratacao E Abandono

- Canal: `hibrido`
- Autonomia padrao: `customizado`
- Trigger: interessado recebe link de contratacao, abre checkout, abandona ou conclui.

Subfluxos:

- Link
  - link de plano configurado.
  - link precisa ser gerado.
  - plano exige validacao humana.
- Abandono
  - abriu e nao pagou.
  - informou dados e nao concluiu.
  - link expirou.
- Conclusao
  - pagamento confirmado -> Financeiro D4/D5.
  - pagamento falhou -> Financeiro D7.
  - plano contratado -> Agenda B8/primeira turma.
- Guardrail
  - nao pressionar excessivamente.
  - limitar follow-up de abandono.

Estados finais: `proximo_fluxo`, `aguardando_contato`, `tarefa_criada`, `resolvido`.

### C12. Demanda Sem Vaga E Lista Comercial

- Canal: `whatsapp` ou `sistema`
- Autonomia padrao: `customizado`
- Trigger: interessado quer horario/plano que nao tem disponibilidade.

Subfluxos:

- Sem vaga
  - horario cheio.
  - turno indisponivel.
  - professor/turma inadequado.
  - unidade indisponivel.
- Caminhos
  - oferecer alternativa proxima.
  - inserir em lista comercial.
  - criar oportunidade para Gestao avaliar demanda.
  - avisar quando abrir vaga se consentimento permitir.
- Conversao
  - aceitou alternativa -> C2/C6.
  - quer esperar -> tarefa/lista.
  - desistiu -> C9.

Estados finais: `aguardando_contato`, `tarefa_criada`, `proximo_fluxo`, `resolvido`.

### C13. Transicao De Interessado Para Aluno

- Canal: `hibrido`
- Autonomia padrao: `copiloto`
- Trigger: pagamento, contrato ou decisao da equipe confirma nova matricula.

Subfluxos:

- Conversao
  - atualizar status de interessado para aluno.
  - preservar origem e historico comercial.
  - vincular plano e horarios.
  - criar checklist de inicio.
- Pendencias
  - pagamento pendente -> Financeiro.
  - contrato pendente -> Financeiro D11.
  - horario pendente -> Agenda B8/B15.
  - contexto inicial/anamnese -> Historico G6.
- Comunicacao
  - mensagem de boas-vindas aprovada.
  - avisar equipe/professor.
  - pausar follow-ups comerciais antigos.

Estados finais: `acao_registrada`, `proximo_fluxo`, `tarefa_criada`, `resolvido`.

### C14. Upsell, Upgrade E Mudanca Comercial De Plano

- Canal: `sistema` ou `whatsapp`
- Autonomia padrao: `copiloto`
- Trigger: aluno demonstra interesse em aumentar frequencia, trocar plano, incluir servico ou comprar aula extra.

Subfluxos:

- Interesse
  - aumentar frequencia.
  - trocar plano.
  - aula avulsa/workshop.
  - pacote adicional.
- Caminhos
  - disponibilidade necessaria -> Agenda.
  - preco/condicao -> Financeiro/Vendas C1.
  - aceite -> Financeiro D3/D5.
  - excecao/desconto -> humano.
- Guardrail
  - nao empurrar upgrade de forma automatica sensivel.
  - respeitar restricoes e contexto do aluno.

Estados finais: `proximo_fluxo`, `tarefa_criada`, `aguardando_contato`, `handoff_humano`.

## 4. Agente Financeiro

Responsabilidade: vencimentos, pagamentos, Pix/link, comprovantes, renovacoes, atraso e excecoes financeiras.

### D1. Lembrete De Vencimento

- Canal: `whatsapp`
- Autonomia padrao: `customizado`
- Trigger: vencimento proximo.

Subfluxos:

- Momento
  - antes do vencimento.
  - no dia.
  - apos vencimento leve.
- Economia
  - agrupar lembretes.
  - limitar mensagens.
  - nao enviar lembrete de baixa prioridade perto do limite.
- Respostas
  - pediu link -> D3.
  - pagou -> D4.
  - questionou valor -> D6.
  - sem resposta -> D2 ou encerrar.

Estados finais: `aguardando_contato`, `proximo_fluxo`, `tarefa_criada`.

### D2. Pagamento Atrasado

- Canal: `whatsapp` ou `sistema`
- Autonomia padrao: `customizado`
- Trigger: parcela vencida.

Subfluxos:

- Faixas
  - atraso leve -> lembrete cordial.
  - atraso medio -> lembrete com link.
  - acima do limite -> equipe.
  - recorrente -> Gestao F4/Retencao E4.
- Caminhos
  - pagou -> D4.
  - prometeu pagar -> registrar promessa e lembrete.
  - contestou -> A5.
  - sem resposta -> tarefa.

Estados finais: `aguardando_contato`, `tarefa_criada`, `handoff_humano`, `proximo_fluxo`.

### D3. Pix, Link Ou Segunda Via

- Canal: `whatsapp`
- Autonomia padrao: `automatico`
- Trigger: aluno pede pagamento ou fluxo financeiro solicita.

Subfluxos:

- Fonte
  - link ja existe.
  - link pode ser gerado.
  - somente instrucao Pix configurada.
- Guardrail
  - nunca coletar cartao/senha/dado sensivel.
  - comprovante sem conciliacao vira tarefa.
- Caminhos
  - enviar link/instrucao.
  - criar tarefa se nao ha dados.
  - bloquear dado sensivel.

Estados finais: `resolvido`, `tarefa_criada`, `pausado`, `aguardando_contato`.

### D4. Confirmacao De Pagamento

- Canal: `sistema` ou `hibrido`
- Autonomia padrao: `customizado`
- Trigger: webhook, comprovante ou baixa manual.

Subfluxos:

- Fonte
  - webhook confiavel -> registrar.
  - comprovante -> tarefa/revisao ou regra configurada.
  - equipe marcou pago -> registrar.
- Caminhos
  - confirmado -> atualizar status.
  - plano precisa continuidade -> D5.
  - valor divergente -> A5.
  - duplicidade -> A5.

Estados finais: `acao_registrada`, `tarefa_criada`, `proximo_fluxo`, `handoff_humano`.

### D5. Renovacao De Plano

- Canal: `hibrido`
- Autonomia padrao: `copiloto`
- Trigger: plano vencendo, pagamento confirmado ou aluno quer renovar.

Subfluxos:

- Mesmo plano
  - se regra permite e dados confiaveis -> sugerir/registrar.
  - se precisa decisao -> tarefa.
- Mudanca
  - muda frequencia -> Agenda B8 + ajuste financeiro.
  - muda valor/plano -> equipe ou checkout.
  - pausa/cancela -> D6 + Retencao E4.

Estados finais: `acao_registrada`, `tarefa_criada`, `proximo_fluxo`, `handoff_humano`.

### D6. Excecoes Financeiras

- Canal: `hibrido`
- Autonomia padrao: `humano`
- Trigger: desconto, reembolso, pausa, cancelamento, contestacao, mudanca de vencimento.

Subfluxos:

- Politica simples
  - explicar regra aprovada.
  - criar tarefa se precisa aplicar.
- Decisao
  - desconto -> humano.
  - reembolso -> humano.
  - cancelamento/pausa -> Retencao E4 + humano.
  - contestacao -> humano.

Estados finais: `handoff_humano`, `tarefa_criada`, `proximo_fluxo`.

### D7. Falha De Pagamento Ou Recorrencia

- Canal: `hibrido`
- Autonomia padrao: `customizado`
- Trigger: cartao recusado, Pix expirado, link vencido, recorrencia falhou ou webhook de falha.

Subfluxos:

- Tipo de falha
  - cartao recusado.
  - Pix expirado.
  - boleto/link vencido.
  - recorrencia cancelada.
  - webhook inconsistente.
- Caminhos
  - gerar novo link se permitido.
  - avisar aluno com mensagem aprovada.
  - criar tarefa se falha recorrente.
  - divergencia tecnica -> equipe.

Estados finais: `proximo_fluxo`, `tarefa_criada`, `aguardando_contato`, `handoff_humano`.

### D8. Recibo, Nota Ou Comprovante Para Aluno

- Canal: `whatsapp` ou `sistema`
- Autonomia padrao: `customizado`
- Trigger: aluno pede recibo, nota, comprovante ou declaracao.

Subfluxos:

- Documento
  - recibo simples.
  - nota fiscal.
  - declaracao.
  - comprovante de pagamento.
- Caminhos
  - documento ja existe -> enviar se permitido.
  - precisa gerar -> tarefa ou integracao.
  - envolve dado fiscal/sensivel -> humano se regra exigir.

Estados finais: `resolvido`, `tarefa_criada`, `handoff_humano`.

### D9. Pausa Programada Ou Trancamento

- Canal: `hibrido`
- Autonomia padrao: `humano`
- Trigger: aluno quer pausar por viagem, saude, agenda ou motivo financeiro.

Subfluxos:

- Motivo
  - viagem.
  - saude.
  - financeiro.
  - agenda.
  - indefinido.
- Impacto
  - plano.
  - vencimento.
  - vagas fixas.
  - retorno previsto.
- Caminhos
  - explicar politica aprovada.
  - criar tarefa para decisao.
  - se retorno previsto -> Retencao E7.

Estados finais: `handoff_humano`, `tarefa_criada`, `proximo_fluxo`.

### D10. Conciliacao E Pendencia Financeira Interna

- Canal: `sistema`
- Autonomia padrao: `copiloto`
- Trigger: pagamento sem aluno, aluno sem pagamento, valor divergente ou baixa manual pendente.

Subfluxos:

- Divergencia
  - valor menor/maior.
  - aluno errado.
  - pagamento duplicado.
  - baixa nao confirmada.
- Caminhos
  - sugerir match.
  - criar tarefa para financeiro.
  - bloquear mensagem automatica ate resolver.

Estados finais: `tarefa_criada`, `sem_acao`, `handoff_humano`.

### D11. Contrato, Termos E Assinatura

- Canal: `hibrido`
- Autonomia padrao: `copiloto`
- Trigger: nova matricula, renovacao com termo, cancelamento, pausa ou pedido de contrato.

Subfluxos:

- Documento
  - contrato de matricula.
  - termo de renovacao.
  - termo de cancelamento.
  - aceite de regras.
- Caminhos
  - contrato padrao configurado -> enviar link/gerar tarefa.
  - exige revisao -> humano.
  - assinatura pendente -> lembrar se permitido.
  - assinatura concluida -> registrar.
- Guardrail
  - nao alterar termos legais automaticamente.
  - duvida juridica -> humano.

Estados finais: `acao_registrada`, `tarefa_criada`, `handoff_humano`, `aguardando_contato`.

### D12. Suspensao, Bloqueio Ou Liberacao De Acesso

- Canal: `sistema` ou `hibrido`
- Autonomia padrao: `humano`
- Trigger: inadimplencia acima do limite, cancelamento confirmado, fim de plano ou liberacao manual.

Subfluxos:

- Bloqueio
  - plano encerrado.
  - inadimplencia fora da regra.
  - cancelamento concluido.
  - pausa/trancamento ativo.
- Liberacao
  - pagamento confirmado.
  - excecao aprovada.
  - renovacao concluida.
- Caminhos
  - sugerir bloqueio/liberacao.
  - criar tarefa.
  - atualizar agenda somente apos aprovacao.
  - comunicar aluno apenas com mensagem aprovada.

Estados finais: `tarefa_criada`, `acao_registrada`, `handoff_humano`, `proximo_fluxo`.

### D13. Creditos, Bonus E Cortesias

- Canal: `sistema` ou `hibrido`
- Autonomia padrao: `humano`
- Trigger: equipe concede cortesia, credito manual, bonus de indicacao, ajuste comercial ou compensacao.

Subfluxos:

- Tipos
  - aula cortesia.
  - credito financeiro.
  - bonus por indicacao.
  - compensacao por erro do studio.
  - desconto pontual.
- Caminhos
  - registrar motivo.
  - definir validade.
  - vincular responsavel que aprovou.
  - refletir em Agenda/Financeiro.
- Guardrail
  - agente nao concede beneficio sozinho.
  - qualquer beneficio financeiro exige auditoria.

Estados finais: `acao_registrada`, `tarefa_criada`, `handoff_humano`, `proximo_fluxo`.

### D14. Fechamento Mensal E Relatorio Financeiro

- Canal: `sistema`
- Autonomia padrao: `automatico`
- Trigger: fim de mes, dono abre financeiro ou rotina de resumo.

Subfluxos:

- Indicadores
  - recebido.
  - pendente.
  - atrasado.
  - cancelado/pausado.
  - previsao de renovacao.
- Caminhos
  - gerar resumo.
  - destacar pendencias.
  - criar tarefas de cobranca.
  - enviar para Gestao F2/F5.

Estados finais: `acao_registrada`, `tarefa_criada`, `proximo_fluxo`, `sem_acao`.

## 5. Agente Retencao

Responsabilidade: risco, inatividade, retorno, cancelamento e reativacao sem pressionar o aluno.

### E1. Queda De Frequencia

- Canal: `sistema` ou `hibrido`
- Autonomia padrao: `customizado`
- Trigger: frequencia abaixo do padrao.

Subfluxos:

- Sinais
  - menos presencas.
  - faltas repetidas.
  - reposicoes acumuladas.
  - plano perto de vencer sem engajamento.
- Caminhos
  - baixo risco -> monitorar.
  - medio -> mensagem leve ou tarefa.
  - alto -> tarefa prioritaria.
  - motivo agenda -> Agenda.
  - motivo financeiro -> Financeiro.
  - saude -> A5/Historico G3.

Estados finais: `tarefa_criada`, `aguardando_contato`, `proximo_fluxo`, `handoff_humano`.

### E2. Aluno Inativo

- Canal: `whatsapp` ou `sistema`
- Autonomia padrao: `customizado`
- Trigger: aluno ativo sem presenca por janela configurada.

Subfluxos:

- Faixas
  - 7 dias.
  - 14 dias.
  - 21+ dias.
- Economia
  - priorizar alto risco.
  - evitar WhatsApp pago para baixo impacto.
  - criar lista para aprovacao em lote.
- Respostas
  - quer voltar -> E3.
  - ocupado -> follow-up leve.
  - problema pessoal/saude -> A5.
  - sem resposta -> encerrar/monitorar.

Estados finais: `aguardando_contato`, `proximo_fluxo`, `tarefa_criada`, `handoff_humano`.

### E3. Retorno

- Canal: `hibrido`
- Autonomia padrao: `customizado`
- Trigger: aluno inativo aceita voltar.

Subfluxos:

- Preferencia
  - horario antigo -> Agenda B8.
  - horario tranquilo -> Agenda B5/B8.
  - conversar antes -> A5.
  - restricao/dor -> Historico G3 + A5.
- Concluir
  - retorno marcado -> avisar professor.
  - sem horario -> tarefa/lista.

Estados finais: `acao_registrada`, `proximo_fluxo`, `tarefa_criada`, `handoff_humano`.

### E4. Risco De Cancelamento

- Canal: `hibrido`
- Autonomia padrao: `humano`
- Trigger: cancelamento, pausa, insatisfacao ou risco alto.

Subfluxos:

- Sinais
  - "vou cancelar".
  - "nao consigo mais ir".
  - reclamacao.
  - pausa.
  - inadimplencia + baixa frequencia.
- Caminhos
  - cancelamento direto -> humano.
  - problema de horario -> Agenda.
  - problema financeiro -> Financeiro.
  - experiencia ruim -> tarefa para dono/professor.
  - aberto a continuar -> sugestao para responsavel.

Estados finais: `handoff_humano`, `tarefa_criada`, `proximo_fluxo`.

### E5. Reativacao De Ex-Aluno

- Canal: `whatsapp` ou `sistema`
- Autonomia padrao: `copiloto`
- Trigger: ex-aluno elegivel para reativacao.

Subfluxos:

- Segmentos
  - saiu por agenda.
  - saiu por financeiro.
  - saiu por saude.
  - saiu sem motivo registrado.
- Execucao
  - lista sugerida para equipe.
  - campanha aprovada em lote limitado.
  - mensagem individual para casos prioritarios.
- Resposta
  - quer voltar -> Vendas C6 ou Agenda B7/B8.
  - quer saber valores -> Vendas C1.
  - opt-out -> pausar.
  - saude -> A5.

Estados finais: `tarefa_criada`, `proximo_fluxo`, `pausado`, `aguardando_contato`.

### E6. Satisfacao E Experiencia

- Canal: `whatsapp` ou `sistema`
- Autonomia padrao: `customizado`
- Trigger: aula experimental, retorno, reclamacao, queda de frequencia ou janela de pesquisa.

Subfluxos:

- Coleta
  - pergunta simples de experiencia.
  - avaliacao interna.
  - comentario aberto.
- Caminhos
  - feedback positivo -> registrar.
  - feedback neutro -> tarefa leve.
  - feedback negativo -> E4/humano.
  - menciona professor/turma -> Gestao F4 ou tarefa.

Estados finais: `acao_registrada`, `tarefa_criada`, `handoff_humano`, `proximo_fluxo`.

### E7. Retorno Programado Apos Pausa

- Canal: `hibrido`
- Autonomia padrao: `customizado`
- Trigger: pausa/trancamento tem data prevista de retorno.

Subfluxos:

- Antes da data
  - lembrete interno.
  - mensagem aprovada se permitido.
  - checar horario antigo.
- Caminhos
  - quer voltar -> E3.
  - precisa estender pausa -> Financeiro D9.
  - quer cancelar -> E4.
  - sem resposta -> tarefa/monitorar.

Estados finais: `proximo_fluxo`, `aguardando_contato`, `tarefa_criada`.

### E8. Risco Por Perfil De Uso

- Canal: `sistema`
- Autonomia padrao: `automatico`
- Trigger: combinacao de sinais indica risco sem mensagem explicita.

Subfluxos:

- Sinais combinados
  - baixa frequencia + atraso.
  - muitas remarcacoes + poucas presencas.
  - reclamacao + ausencia.
  - plano vencendo + sem engajamento.
- Caminhos
  - baixa prioridade -> monitorar.
  - media -> tarefa.
  - alta -> E2/E4.

Estados finais: `tarefa_criada`, `proximo_fluxo`, `sem_acao`.

### E9. Cancelamento Concluido E Pos-Cancelamento

- Canal: `sistema` ou `whatsapp`
- Autonomia padrao: `copiloto`
- Trigger: cancelamento aprovado/concluido pela equipe.

Subfluxos:

- Encerramento
  - registrar motivo final.
  - cancelar horarios futuros.
  - encerrar cobrancas futuras.
  - registrar data de saida.
- Comunicacao
  - mensagem de encerramento aprovada.
  - pedido de feedback opcional.
  - opt-out respeitado.
- Pos-cancelamento
  - elegivel para reativacao futura -> E5.
  - nao contatar -> pausar.
  - pendencia financeira -> Financeiro D2/D10.

Estados finais: `acao_registrada`, `proximo_fluxo`, `pausado`, `tarefa_criada`.

### E10. Marco De Engajamento E Celebracao

- Canal: `sistema` ou `whatsapp`
- Autonomia padrao: `customizado`
- Trigger: aluno completa marco relevante de presenca, retorno, consistencia ou objetivo.

Subfluxos:

- Marcos
  - voltou apos inatividade.
  - completou sequencia de presencas.
  - atingiu objetivo registrado.
  - aniversario de matricula.
- Caminhos
  - registrar internamente.
  - sugerir mensagem para equipe.
  - enviar mensagem se permitido e credito suficiente.
  - evitar se aluno tem restricao/situacao sensivel.

Estados finais: `acao_registrada`, `tarefa_criada`, `resolvido`, `sem_acao`.

### E11. Saude, Dor Ou Evento Pessoal Como Risco De Retencao

- Canal: `hibrido`
- Autonomia padrao: `humano`
- Trigger: aluno menciona dor, lesao, cirurgia, gravidez, luto, mudanca pessoal ou situacao delicada que afeta frequencia.

Subfluxos:

- Tipo
  - dor/lesao.
  - cirurgia/recuperacao.
  - gravidez.
  - mudanca de rotina/cidade.
  - situacao emocional/pessoal.
- Caminhos
  - registrar contexto sensivel em Historico G3.
  - pausar mensagens automaticas inadequadas.
  - criar tarefa para responsavel.
  - se houver retorno previsto -> E7.
- Guardrail
  - nao dar orientacao clinica.
  - nao usar esse contexto em mensagem comercial automatica.

Estados finais: `handoff_humano`, `tarefa_criada`, `proximo_fluxo`, `pausado`.

### E12. Segmentacao De Risco E Campanhas De Retencao

- Canal: `sistema`
- Autonomia padrao: `copiloto`
- Trigger: dono quer ver grupos de risco, campanha de retencao ou lista priorizada.

Subfluxos:

- Segmentos
  - risco por ausencia.
  - risco financeiro.
  - risco por experiencia.
  - risco por agenda.
  - ex-alunos elegiveis.
- Caminhos
  - gerar lista.
  - priorizar contatos.
  - sugerir mensagens aprovadas.
  - exigir aprovacao antes de envio em lote.

Estados finais: `tarefa_criada`, `proximo_fluxo`, `sem_acao`.

## 6. Agente Gestao

Responsabilidade: enxergar a operacao, priorizar, recomendar e organizar decisoes humanas. Gestao nao substitui os agentes donos dos fluxos.

### F1. Prioridades Do Dia

- Canal: `sistema`
- Autonomia padrao: `automatico`
- Trigger: inicio do dia ou dono abre Taliya.

Subfluxos:

- Entradas
  - vagas abertas.
  - experimentais quentes.
  - pagamentos vencidos.
  - alunos em risco.
  - handoffs.
- Caminhos
  - item acionavel -> abrir agente dono.
  - precisa decisao -> tarefa.
  - falta setup -> checklist.
  - tudo certo -> estado saudavel.

Estados finais: `tarefa_criada`, `proximo_fluxo`, `sem_acao`.

### F2. Dinheiro Na Mesa

- Canal: `sistema`
- Autonomia padrao: `automatico`
- Trigger: painel/calculadora/resumo.

Subfluxos:

- Componentes
  - vagas nao preenchidas.
  - inadimplencia.
  - planos vencendo.
  - interessados parados.
  - alunos inativos.
  - tempo operacional economizado.
- Saida
  - maior perda em agenda -> Agenda.
  - maior perda em vendas -> Vendas.
  - maior perda em financeiro -> Financeiro.
  - maior perda em retencao -> Retencao.

Estados finais: `proximo_fluxo`, `sem_acao`, `tarefa_criada`.

### F3. Fila Humana

- Canal: `sistema`
- Autonomia padrao: `automatico`
- Trigger: handoff, aprovacao ou excecao.

Subfluxos:

- Itens
  - aprovacoes.
  - excecoes.
  - conversas sensiveis.
  - configuracoes ausentes.
- Acoes
  - aprovar -> retomar fluxo.
  - editar -> enviar/registrar.
  - rejeitar -> fechar.
  - delegar -> responsavel.

Estados finais: `acao_registrada`, `aguardando_equipe`, `proximo_fluxo`, `resolvido`.

### F4. Gargalos Recorrentes

- Canal: `sistema`
- Autonomia padrao: `copiloto`
- Trigger: padrao operacional repetido.

Subfluxos:

- Padroes
  - turma sempre vazia.
  - aluno sempre falta.
  - interessados somem depois de preco.
  - muitos atrasos.
  - reposicoes acumuladas.
- Acoes
  - sugerir ajuste de regra.
  - sugerir ajuste de mensagem.
  - criar tarefa de gestao.
  - acionar agente correspondente.

Estados finais: `tarefa_criada`, `proximo_fluxo`, `sem_acao`.

### F5. Resumo Semanal

- Canal: `sistema` ou notificacao interna.
- Autonomia padrao: `automatico`
- Trigger: janela semanal configurada.

Subfluxos:

- Conteudo
  - resolvido.
  - pendente.
  - perdas.
  - economia.
  - recomendacoes.
- Acoes
  - enviar resumo.
  - criar tarefas.
  - sugerir ajustes.
  - nao fazer nada.

Estados finais: `resolvido`, `tarefa_criada`, `sem_acao`.

### F6. Qualidade Dos Dados E Setup

- Canal: `sistema`
- Autonomia padrao: `automatico`
- Trigger: fluxo nao consegue agir por falta de dados ou setup incompleto.

Subfluxos:

- Dados faltando
  - horarios.
  - planos.
  - precos.
  - regras de reposicao.
  - responsaveis.
  - links de pagamento.
  - politicas de mensagem.
- Caminhos
  - criar checklist.
  - priorizar dado bloqueador.
  - impedir fluxo automatico ate completar.

Estados finais: `tarefa_criada`, `sem_acao`, `pausado`.

### F7. Uso De Creditos E Limites Operacionais

- Canal: `sistema`
- Autonomia padrao: `automatico`
- Trigger: consumo atinge limite, previsao de estouro ou acao cara e solicitada.

Subfluxos:

- Alertas
  - 70%.
  - 90%.
  - 100%.
  - previsao de acabar antes do fim do mes.
- Acoes
  - ativar modo economia.
  - pausar baixa prioridade.
  - pedir aprovacao para lotes/campanhas.
  - sugerir pacote extra.

Estados finais: `acao_registrada`, `tarefa_criada`, `pausado`.

### F8. Performance Por Agente E Responsavel

- Canal: `sistema`
- Autonomia padrao: `automatico`
- Trigger: dono abre painel ou resumo periodico.

Subfluxos:

- Indicadores
  - fluxos resolvidos.
  - pendencias abertas.
  - handoffs.
  - tempo de resposta.
  - gargalos por responsavel.
- Caminhos
  - recomendar ajuste.
  - criar tarefa de gestao.
  - acionar fluxo dono.

Estados finais: `tarefa_criada`, `proximo_fluxo`, `sem_acao`.

### F9. Permissoes, Auditoria E Alteracoes Criticas

- Canal: `sistema`
- Autonomia padrao: `automatico`
- Trigger: usuario muda regra, aprova acao critica, altera responsavel, muda plano ou ativa/desativa fluxo.

Subfluxos:

- Alteracoes
  - configuracao de agente.
  - regra financeira.
  - regra de reposicao.
  - responsavel por handoff.
  - permissao de equipe.
- Auditoria
  - quem alterou.
  - o que mudou.
  - quando mudou.
  - impacto previsto.
- Caminhos
  - registrar auditoria.
  - bloquear alteracao sem permissao.
  - avisar dono em mudanca critica.

Estados finais: `acao_registrada`, `pausado`, `tarefa_criada`.

### F10. Planejamento De Capacidade E Crescimento

- Canal: `sistema`
- Autonomia padrao: `copiloto`
- Trigger: ocupacao alta/baixa, lista de espera crescente, demanda por horario ou turma subutilizada.

Subfluxos:

- Sinais
  - turma cheia recorrente.
  - lista de espera.
  - horario com baixa ocupacao.
  - demanda comercial sem vaga.
- Caminhos
  - sugerir abrir turma.
  - sugerir ajustar horario.
  - sugerir campanha para horario vazio.
  - acionar Agenda/Vendas/Retencao.

Estados finais: `tarefa_criada`, `proximo_fluxo`, `sem_acao`.

### F11. Falhas Operacionais, Integracoes E Webhooks

- Canal: `sistema`
- Autonomia padrao: `automatico`
- Trigger: WhatsApp, pagamento, agenda, IA, fila, job ou integracao falha.

Subfluxos:

- Falhas
  - mensagem nao enviada.
  - webhook duplicado.
  - pagamento sem confirmacao.
  - job atrasado.
  - IA indisponivel.
  - limite de provedor.
- Caminhos
  - retry automatico se seguro.
  - criar tarefa tecnica/operacional.
  - pausar fluxo afetado.
  - avisar responsavel se impacto em aluno.
- Guardrail
  - nao duplicar mensagem/pagamento.
  - usar idempotencia antes de retry.

Estados finais: `tarefa_criada`, `pausado`, `acao_registrada`, `sem_acao`.

### F12. Importacao, Migracao E Higienizacao Inicial

- Canal: `sistema`
- Autonomia padrao: `copiloto`
- Trigger: novo studio importa alunos, agenda, planos, pagamentos ou historico.

Subfluxos:

- Importacao
  - planilha.
  - sistema antigo.
  - cadastro manual.
  - WhatsApp/historico parcial.
- Higienizacao
  - contatos duplicados.
  - alunos sem plano.
  - horarios sem professor.
  - pagamentos sem status.
  - regras faltantes.
- Caminhos
  - criar checklist.
  - bloquear fluxos dependentes ate dado minimo.
  - sugerir merges.
  - registrar pendencias de setup.

Estados finais: `tarefa_criada`, `acao_registrada`, `sem_acao`, `pausado`.

### F13. Configuracao E Teste De Fluxo Antes De Ativar

- Canal: `sistema`
- Autonomia padrao: `copiloto`
- Trigger: studio altera configuracao, ativa agente ou quer simular comportamento.

Subfluxos:

- Configuracao
  - tom.
  - mensagem.
  - autonomia.
  - limite.
  - responsavel.
  - janela.
- Teste
  - simular conversa.
  - simular falta/reposicao.
  - simular cobranca.
  - validar handoff.
- Caminhos
  - aprovado -> ativar.
  - falhou teste -> manter inativo.
  - incompleto -> checklist.

Estados finais: `acao_registrada`, `tarefa_criada`, `pausado`, `sem_acao`.

## 7. Agente Historico/Evolucao

Responsabilidade: organizar contexto do aluno para equipe e agentes. E um agente primariamente interno. Nao envia orientacao clinica automatica ao aluno.

### G1. Contexto Antes Da Aula

- Canal: `sistema`
- Autonomia padrao: `automatico`
- Trigger: professor abre turma ou preparacao antes da aula.

Subfluxos:

- Dados
  - ultima presenca.
  - ultima observacao.
  - restricoes registradas.
  - preferencias.
  - objetivo.
  - frequencia recente.
- Caminhos
  - contexto completo -> resumo interno.
  - falta contexto -> pedir anotacao futura.
  - restricao importante -> destacar internamente.
  - pedido de interpretacao clinica -> bloquear.

Estados finais: `acao_registrada`, `tarefa_criada`, `pausado`.

### G2. Observacao Pos-Aula

- Canal: `sistema`
- Autonomia padrao: `automatico`
- Trigger: aula encerrada ou professor adiciona nota.

Subfluxos:

- Entrada
  - texto.
  - voz transcrita.
  - campos guiados.
  - presenca/falta.
- Caminhos
  - nota simples -> salvar.
  - indica risco de frequencia -> Retencao E1.
  - indica ajuste de horario -> Agenda B8.
  - indica restricao -> G3.

Estados finais: `acao_registrada`, `proximo_fluxo`, `tarefa_criada`.

### G3. Restricao Ou Cuidado Importante

- Canal: `sistema`
- Autonomia padrao: `copiloto`
- Trigger: restricao, dor, lesao, gravidez, limitacao ou cuidado.

Subfluxos:

- Acoes internas
  - registrar.
  - destacar para professor.
  - mostrar antes da aula.
  - limitar sugestoes de agenda se necessario.
- Guardrail
  - nao orientar aluno automaticamente.
  - se aluno perguntou no WhatsApp -> A5.
  - se exige decisao profissional -> humano.

Estados finais: `acao_registrada`, `handoff_humano`, `pausado`.

### G4. Objetivo E Evolucao

- Canal: `sistema`
- Autonomia padrao: `automatico`
- Trigger: intervalo de revisao ou nota de professor.

Subfluxos:

- Caminhos
  - atualizar objetivo.
  - marcar objetivo desatualizado.
  - sugerir revisao.
  - relacionar baixa evolucao com risco de retencao.

Estados finais: `acao_registrada`, `tarefa_criada`, `proximo_fluxo`.

### G5. Contexto Para Outro Agente

- Canal: `sistema` ou `hibrido`
- Autonomia padrao: `automatico`
- Trigger: outro agente precisa de contexto seguro.

Subfluxos:

- Solicitantes
  - Atendimento.
  - Agenda.
  - Retencao.
  - Gestao.
- Caminhos
  - contexto seguro -> entregar resumo interno.
  - contexto sensivel -> retornar bloqueio/handoff.
  - sem contexto -> tarefa.

Estados finais: `proximo_fluxo`, `tarefa_criada`, `handoff_humano`, `sem_acao`.

### G6. Documentos, Anexos E Anamnese

- Canal: `sistema` ou `hibrido`
- Autonomia padrao: `copiloto`
- Trigger: aluno envia documento, equipe anexa arquivo, professor pede ficha ou avaliacao.

Subfluxos:

- Tipo
  - anamnese.
  - avaliacao.
  - foto.
  - atestado.
  - documento administrativo.
- Caminhos
  - armazenar com permissao correta.
  - destacar para professor.
  - bloquear uso em mensagem externa automatica.
  - se for financeiro/contrato -> Financeiro ou Gestao.

Estados finais: `acao_registrada`, `tarefa_criada`, `handoff_humano`.

### G7. Correcao Ou Atualizacao De Historico

- Canal: `sistema`
- Autonomia padrao: `copiloto`
- Trigger: dado errado, nota duplicada, restricao desatualizada ou equipe corrige informacao.

Subfluxos:

- Tipo
  - corrigir nota.
  - remover duplicidade.
  - atualizar restricao.
  - alterar objetivo.
- Caminhos
  - registrar auditoria.
  - pedir confirmacao para informacao sensivel.
  - atualizar contexto usado por outros agentes.

Estados finais: `acao_registrada`, `tarefa_criada`, `handoff_humano`.

### G8. Handoff Entre Professores Ou Equipe

- Canal: `sistema`
- Autonomia padrao: `automatico`
- Trigger: troca de professor, substituicao, aluno muda turma ou existe cuidado importante.

Subfluxos:

- Contexto de handoff
  - ultimos combinados.
  - preferencias.
  - restricoes.
  - objetivo.
  - pontos de atencao.
- Caminhos
  - gerar resumo interno.
  - destacar cuidado importante.
  - criar tarefa para professor confirmar leitura.

Estados finais: `acao_registrada`, `tarefa_criada`, `sem_acao`.

### G9. Rotina De Anotacao E Lembrete Para Professor

- Canal: `sistema`
- Autonomia padrao: `automatico`
- Trigger: aula terminou sem nota, aluno tem cuidado importante ou professor esqueceu acompanhamento.

Subfluxos:

- Lembrete
  - turma encerrada sem observacao.
  - aluno com restricao sem atualizacao recente.
  - objetivo vencido.
  - retorno apos pausa/inatividade.
- Caminhos
  - pedir nota curta.
  - sugerir campos guiados.
  - pular se baixa prioridade.
  - criar tarefa para professor.

Estados finais: `tarefa_criada`, `acao_registrada`, `sem_acao`.

### G10. Compartilhamento Seguro De Contexto Com Aluno

- Canal: `whatsapp` ou `sistema`
- Autonomia padrao: `copiloto`
- Trigger: aluno pede resumo, evolucao, historico, ficha ou observacao.

Subfluxos:

- Pedido
  - resumo de frequencia.
  - historico de aulas.
  - observacoes do professor.
  - orientacao sobre dor/exercicio.
- Caminhos
  - dados administrativos seguros -> preparar resposta.
  - observacao interna -> pedir aprovacao.
  - conteudo clinico/orientacao -> humano.
  - exportacao/documento -> tarefa.

Estados finais: `tarefa_criada`, `handoff_humano`, `resolvido`, `aguardando_contato`.

### G11. Permissao De Visibilidade Do Historico

- Canal: `sistema`
- Autonomia padrao: `automatico`
- Trigger: professor, recepcao, financeiro ou gestor acessa historico do aluno.

Subfluxos:

- Papeis
  - professor.
  - recepcao.
  - financeiro.
  - dono/gestor.
  - suporte interno.
- Dados
  - observacoes de aula.
  - restricoes.
  - dados financeiros.
  - documentos.
  - notas internas sensiveis.
- Caminhos
  - mostrar apenas o necessario para o papel.
  - ocultar dado sensivel.
  - registrar acesso se dado critico.
  - bloquear acesso sem permissao.

Estados finais: `acao_registrada`, `pausado`, `sem_acao`.

### G12. Linha Do Tempo Unificada Do Aluno

- Canal: `sistema`
- Autonomia padrao: `automatico`
- Trigger: equipe abre perfil, agente precisa de contexto ou Gestao consolida risco.

Subfluxos:

- Eventos
  - presenca/falta.
  - reposicao.
  - pagamento.
  - conversa importante.
  - objetivo/evolucao.
  - restricao.
  - cancelamento/pausa.
- Caminhos
  - resumir para equipe.
  - filtrar por papel.
  - fornecer contexto seguro para agente.
  - detectar lacunas ou conflitos.

Estados finais: `acao_registrada`, `proximo_fluxo`, `sem_acao`, `tarefa_criada`.

## Transicoes Oficiais

| Origem | Condicao | Destino |
| --- | --- | --- |
| Atendimento | valores, planos, matricula | Vendas |
| Atendimento | horarios, faltas, reposicoes | Agenda |
| Atendimento | pagamento, vencimento, link | Financeiro |
| Atendimento | aluno sumido, retorno, cancelamento | Retencao |
| Atendimento | dor, restricao, contexto | Historico/Evolucao + humano |
| Atendimento | comprovante, documento ou midia | Financeiro ou Historico/Evolucao |
| Agenda | faltas recorrentes | Retencao |
| Agenda | vaga nao preenchida | Gestao |
| Agenda | cancelamento pelo studio | Gestao + Atendimento/Vendas se houver comunicacao |
| Agenda | primeira aula confirmada | Historico/Evolucao + Vendas/Financeiro se houver pendencia |
| Agenda | aula especial/workshop | Vendas/Financeiro |
| Agenda | horario experimental encontrado | Vendas |
| Vendas | precisa de disponibilidade | Agenda |
| Vendas | pre-matricula pronta | Financeiro ou equipe |
| Vendas | interessado virou aluno | Agenda + Financeiro + Historico/Evolucao |
| Vendas | checkout abandonado/falhou | Financeiro/Vendas follow-up |
| Vendas | demanda sem vaga | Agenda/Gestao |
| Vendas | upgrade/upsell | Agenda/Financeiro |
| Vendas | perda por preco/agenda | Gestao |
| Vendas | interessado parado | Vendas C5 ou Retencao se ja teve vinculo |
| Financeiro | pausa/cancelamento | Retencao + humano |
| Financeiro | mudanca de frequencia | Agenda |
| Financeiro | contrato/termo pendente | Gestao/fila humana |
| Financeiro | bloqueio/liberacao de acesso | Agenda/Gestao |
| Financeiro | credito/cortesia aprovada | Agenda/Gestao |
| Financeiro | fechamento mensal | Gestao |
| Financeiro | falha recorrente ou conciliacao | Gestao |
| Retencao | aluno quer voltar | Agenda |
| Retencao | ex-aluno quer contratar | Vendas |
| Retencao | saude/restricao | Historico/Evolucao + humano |
| Retencao | pausa com retorno previsto | Financeiro + Agenda |
| Retencao | cancelamento concluido | Financeiro/Agenda/Gestao |
| Retencao | lista/campanha de risco | Atendimento/Vendas/Agenda conforme segmento |
| Historico/Evolucao | risco de frequencia | Retencao |
| Historico/Evolucao | documento financeiro/administrativo | Financeiro/Gestao |
| Historico/Evolucao | aluno pede contexto sensivel | Atendimento + humano |
| Historico/Evolucao | historico unificado mostra conflito | Gestao ou agente dono |
| Gestao | prioridade selecionada | agente dono do fluxo |
| Gestao | integracao falha | agente afetado + tarefa operacional |
| Gestao | setup/importacao incompleto | bloquear fluxos dependentes |

## Matriz De Configuracao A Criar

Cada fluxo acima deve virar configuracao com:

- ativo/inativo;
- canal permitido;
- autonomia padrao;
- tom de voz;
- estilo de mensagem;
- permissao de WhatsApp externo;
- permissao para iniciar conversa paga;
- categoria de mensagem: interna, service, utility ou marketing;
- regra de campanha/lote/reativacao;
- limite de creditos;
- limite de tentativas;
- prioridade no modo economia;
- janela de envio;
- dados obrigatorios;
- responsavel;
- pontos de aprovacao;
- criterio de handoff;
- criterio de pausa;
- proximos fluxos permitidos;
- templates aprovados;
- logs obrigatorios.

## Criterios De Completude Para Seguir Para Configuracoes

Este mapa esta pronto para virar configuracao individual de studio quando cada fluxo tiver:

- dono unico do fluxo;
- canal permitido;
- autonomia padrao;
- subfluxos de sucesso;
- subfluxos de espera;
- subfluxos de excecao;
- subfluxos de seguranca;
- impacto em outros agentes;
- estados finais padronizados;
- dados obrigatorios;
- criterio de economia de creditos;
- criterio de handoff;
- criterio de pausa.

Casos infinitamente especificos que surgirem na operacao devem entrar como:

- configuracao de comportamento dentro de um fluxo existente; ou
- tarefa/handoff dentro de Gestao; ou
- solicitacao futura de agente sob medida se estiver fora dos 7 agentes principais.
