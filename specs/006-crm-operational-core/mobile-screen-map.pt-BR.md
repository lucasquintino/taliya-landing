# Mapa do app mobile - PT-BR

> Status: mapa reforcado e revisado. Esta versao percorre as 38 superficies do CRM e inclui no app tudo que pode ser necessario no dia a dia, excluindo somente configuracao pesada, auditoria longa, relatorios profundos e operacoes estruturais melhores no web.

## Veredito

O mapa mobile anterior ainda estava fraco.

Ele cobria a rotina obvia, mas deixava subentendido demais:

- setup inicial;
- configuracao essencial de agentes;
- turmas;
- eventos;
- qualidade de dados;
- retencao;
- cancelamentos;
- contratos/documentos;
- segmentos/comunicados;
- privacidade;
- auditoria resumida;
- status de integracoes;
- assinatura/billing como consulta;
- recursos/sala/professor indisponivel.

A regra corrigida e:

```text
Excluir do mobile somente o que for realmente desnecessario ou perigoso fora do web.
```

## Papel do app

O app mobile do Taliya e a superficie de execucao diaria.

Ele nao substitui o CRM web, mas precisa permitir que gestor, recepcao, professor e financeiro resolvam o dia sem abrir o computador para tudo.

O app precisa permitir:

- fazer setup guiado inicial;
- configurar o minimo necessario dos agentes;
- ajustar modo e limites basicos dos fluxos;
- testar configuracao essencial antes de ativar;
- abrir e fechar o dia;
- responder conversas;
- assumir atendimento do agente;
- operar agenda;
- ver turmas;
- fazer chamada;
- registrar falta/no-show;
- resolver reposicao;
- consultar aluno;
- registrar nota de professor;
- acompanhar interessado;
- acompanhar experimental;
- validar matricula rapida;
- tratar financeiro essencial;
- aprovar excecao;
- resolver tarefa;
- acompanhar caso operacional;
- acompanhar reclamacao;
- ver retencao e cancelamento em risco;
- ver falha de agente;
- pausar automacao em emergencia;
- entender cota quando ela bloquear trabalho;
- ver problema de dado que bloqueia fluxo;
- aprovar comunicado/segmento quando necessario;
- acompanhar solicitacao sensivel.

## Navegacao recomendada

O app deve ter 5 abas fixas e uma area "Mais".

| Aba | Papel | Telas principais dentro |
| --- | --- | --- |
| Hoje | Comando do dia | Hoje, Checklist do dia, Jornadas prioritarias, Notificacoes. |
| Inbox | Atendimento | Inbox, Conversa, Contato rapido, Falhas de envio. |
| Agenda | Aulas e rotina | Agenda, Turmas, Aula, Chamada, Reposicoes, Lista de espera, Eventos. |
| Operacao | Trabalho pendente | Tarefas, Aprovacoes, Caso operacional, Qualidade de dados, Reclamacoes. |
| Alunos | Consulta e acao rapida | Alunos, Perfil do aluno, Historico permitido, Professor. |
| Mais | Areas complementares | Setup, Configuracoes essenciais, Financeiro, Vendas rapidas, Retencao, Agentes, Cotas, Relatorios resumidos, Privacidade, Billing. |

> Nota: se a barra do app precisar ter exatamente 5 itens, "Mais" fica como quinto item e "Alunos" entra como busca global fixa no topo. Mas para produto, manter Alunos visivel tende a ser melhor.

## Jornada diaria no app

### 1. Abertura do dia

O usuario abre **Hoje** e ve:

- proximas aulas;
- turmas com vaga ou conflito;
- aulas com chamada pendente;
- conversas aguardando humano;
- reposicoes sem resposta;
- interessados quentes;
- experimentais do dia;
- pagamentos urgentes;
- aprovacoes pendentes;
- reclamacoes/casos sensiveis;
- fluxos de agente bloqueados;
- problemas de dados bloqueando rotina;
- alertas de cota;
- checklist de abertura.

Acoes:

- abrir aula/turma;
- ir para conversa;
- concluir tarefa;
- aprovar/rejeitar;
- assumir caso;
- pausar automacao;
- resolver bloqueio simples;
- marcar alerta como visto.

### 2. Durante as aulas

O usuario usa **Agenda**, **Turmas**, **Aula** e **Chamada**.

Precisa conseguir:

- ver aula atual;
- ver turma;
- ver alunos esperados;
- ver capacidade/vagas;
- consultar contexto permitido;
- marcar presenca;
- marcar falta;
- registrar no-show;
- criar credito de reposicao;
- registrar observacao rapida;
- acionar reposicao/lista de espera;
- avisar turma quando permitido;
- ver conflito de professor/sala.

### 3. Durante atendimento

O usuario usa **Inbox**, **Conversa** e **Contato**.

Precisa conseguir:

- responder WhatsApp;
- assumir do agente;
- ver resumo da conversa;
- ver aluno/interessado vinculado;
- criar tarefa;
- abrir caso;
- pedir sugestao de resposta;
- registrar opt-out;
- pausar automacao daquela conversa;
- resolver falha de envio simples;
- abrir pagamento, aula, interessado ou aluno relacionado.

### 4. Durante operacao

O usuario usa **Operacao**, **Tarefas**, **Casos** e **Aprovacoes**.

Precisa conseguir:

- ver tarefas atrasadas;
- ver tarefas minhas;
- assumir/delegar;
- concluir;
- comentar;
- abrir caso operacional;
- aprovar acao sugerida;
- editar mensagem antes de aprovar;
- rejeitar com motivo;
- pedir mais dados;
- ver impacto/cota/risco;
- resolver bloqueio simples de dados;
- escalar caso sensivel.

### 5. Fechamento do dia

O usuario volta para **Hoje**.

Precisa ver:

- chamadas pendentes;
- conversas sem resposta;
- tarefas vencidas;
- pagamentos urgentes;
- aprovacoes expirando;
- casos sem dono;
- reposicoes pendentes;
- incidentes de agente;
- checklist de fechamento.

## Telas mobile necessarias

### Setup e configuracao essencial

| Tela | Profundidade | Conteudo obrigatorio | Acoes obrigatorias | Alertas/estados |
| --- | --- | --- | --- | --- |
| Setup inicial | Acao completa guiada | ativacao da conta, studio, horarios, canais, primeiro convite, checklist, progresso | continuar setup, salvar etapa, convidar equipe, pular etapa permitida, abrir CRM | incompleto, bloqueado por dado, pronto para operar |
| Importacao assistida | Acao parcial | opcoes de importacao, status, duplicidades, erros, progresso | iniciar importacao simples, revisar duplicidade, pedir ajuda, continuar depois | importando, erro, duplicidade, concluido |
| Configuracao inicial de agentes | Acao completa guiada | agentes do plano, objetivo, modo inicial, canal, limites, tom, janelas, regras basicas | escolher agente, ativar/pausar, definir modo, salvar, testar exemplo | bloqueado por plano, sem dados, pronto para testar |
| Configuracao rapida de fluxo | Acao controlada | fluxo, modo manual/copiloto/autonomo, limite, aprovacao, template, cota estimada | editar modo, editar limite, testar exemplo, salvar rascunho, publicar simples | rascunho, ativo, pausado, exige web para regra avancada |
| Configuracoes essenciais | Acao parcial | studio, equipe basica, horarios, canal, templates simples, notificacoes, privacidade basica | editar essencial, testar canal, salvar, pedir revisao | incompleto, sem permissao, salvo, exige web |

### Comando e navegacao

| Tela | Profundidade | Conteudo obrigatorio | Acoes obrigatorias | Alertas/estados |
| --- | --- | --- | --- | --- |
| Hoje | Acao completa | agenda do dia, prioridades, alertas, tarefas urgentes, aprovacoes, casos bloqueados, cota, agentes pausados | abrir item, concluir tarefa, aprovar, assumir, pausar automacao, ir para origem | sem pendencias, urgente, atrasado, cota 70/90/100, aguardando humano |
| Checklist do dia | Acao completa | abertura, fechamento, itens pendentes, responsavel, prazo | marcar feito, atribuir, comentar, abrir bloqueio | incompleto, atrasado, bloqueado |
| Notificacoes | Consulta + atalho | alertas operacionais, conversas, aprovacoes, falhas, cotas, riscos | abrir origem, marcar lida, priorizar | urgente, lida, expirada |
| Busca global | Consulta + acao rapida | alunos, contatos, conversas, aulas, turmas, tarefas, casos, interessados | abrir objeto, iniciar conversa, criar tarefa | sem resultado, sem permissao |

### Atendimento

| Tela | Profundidade | Conteudo obrigatorio | Acoes obrigatorias | Alertas/estados |
| --- | --- | --- | --- | --- |
| Inbox | Acao completa | conversas por prioridade, status, canal, responsavel, vinculo, ultima mensagem | responder, assumir, filtrar, criar tarefa, abrir caso | novo, aguardando humano, agente pausado, sem consentimento |
| Conversa | Acao completa | mensagens, resumo, contato, aluno/lead vinculado, sugestao, anexos essenciais | enviar, editar sugestao, assumir, pausar agente, opt-out, abrir perfil/caso | falha de envio, opt-out, sem permissao, agente respondendo |
| Contato rapido | Consulta + acao | telefones, alunos vinculados, preferencias e bloqueios | ligar/abrir WhatsApp, editar essencial, vincular, validar identidade | duplicado, telefone compartilhado, sem permissao |
| Falhas de envio | Acao parcial | mensagem, contato, canal, motivo da falha, tentativa, origem | tentar de novo quando seguro, enviar manual, criar tarefa, abrir conversa | falhou, aguardando provedor, opt-out, janela fechada |

### Agenda, turmas e aulas

| Tela | Profundidade | Conteudo obrigatorio | Acoes obrigatorias | Alertas/estados |
| --- | --- | --- | --- | --- |
| Agenda | Acao completa | dia/semana, aulas, professor, turma, capacidade, conflitos, reposicoes | abrir aula, abrir turma, ver conflito, abrir reposicao, avisar envolvidos | lotado, vaga aberta, conflito, professor indisponivel |
| Turmas | Acao completa | turmas do dia/semana, professor, horario, capacidade, vagas, alunos, lista de espera, proxima aula | abrir turma, ver alunos, abrir proxima aula, ver vagas, encontrar encaixe, avisar turma | cheia, vaga aberta, conflito, professor/sala indisponivel |
| Aula | Acao completa | horario, turma, professor, alunos, status da chamada, contexto permitido | abrir chamada, avisar turma, registrar observacao, abrir turma/aluno | chamada pendente, aula cancelada, sala/professor indisponivel |
| Chamada | Acao completa | alunos esperados, presenca, falta, no-show, observacao, credito gerado | marcar presenca, corrigir, registrar falta/no-show, criar reposicao | falta avisada, no-show, credito criado, conflito |
| Reposicoes | Acao completa | pedidos, creditos, vagas, candidatos, conflitos, status de convite | encontrar encaixe, reservar, convidar, consumir credito, expirar credito | sem vaga, aguardando resposta, conflito, credito vencido |
| Lista de espera | Acao completa | interessados/alunos esperando vaga, disponibilidade, prioridade, origem | convidar, reservar, criar tarefa, marcar sem vaga | sem vaga, resposta pendente, prioridade alta |
| Eventos/workshops | Consulta + acao | evento, horario, capacidade, inscritos, pagamentos quando aplicavel, comunicacao | abrir evento, ver inscritos, confirmar presenca, enviar aviso aprovado | lotado, pagamento pendente, aviso pendente |
| Recursos e disponibilidade | Consulta + alerta | sala/equipamento/professor, indisponibilidade, aulas afetadas, periodo | ver impacto, abrir aula, avisar envolvidos se aprovado, criar tarefa | indisponivel, impacto pendente, conflito |

### Alunos, professor e historico

| Tela | Profundidade | Conteudo obrigatorio | Acoes obrigatorias | Alertas/estados |
| --- | --- | --- | --- | --- |
| Alunos | Consulta + acao | busca, filtros rapidos, status, risco, plano, proxima aula | abrir perfil, iniciar conversa, criar tarefa | inadimplente, risco, pausado, sem permissao |
| Perfil do aluno | Consulta + acao | dados essenciais, contato, plano, agenda, pagamentos, presencas, reposicoes, riscos, historico permitido | conversar, agendar, criar tarefa, registrar nota, abrir financeiro/agenda | ativo, pausado, inadimplente, risco, dado sensivel |
| Historico permitido | Consulta restrita + nota | notas recentes, restricoes permitidas, documentos essenciais, consentimentos | adicionar nota, anexar quando permitido, pedir revisao | sem permissao, dado sensivel, aguardando consentimento |
| Professor | Acao completa | aulas do dia, alunos, notas pendentes, contexto permitido, handoff | registrar nota, criar handoff, marcar lembrete | nota pendente, contexto restrito, aula sem chamada |

### Vendas e matriculas

| Tela | Profundidade | Conteudo obrigatorio | Acoes obrigatorias | Alertas/estados |
| --- | --- | --- | --- | --- |
| Interessados | Acao parcial | leads quentes, proxima acao, origem, experimental, conversa | responder, criar follow-up, agendar experimental, marcar perdido | novo, quente, sem resposta, sem vaga |
| Experimental | Acao completa | experimentais do dia, lembrete, faltou, pos-aula, professor | lembrar, remarcar, registrar falta, fazer pos-aula, converter | lembrete pendente, faltou, converter agora |
| Matricula rapida | Consulta + aprovacao | dados pendentes, plano, contrato, pagamento, primeira aula | validar pendencia, aprovar conversao, criar tarefa | faltando dado, aguardando pagamento |
| Origens e indicacoes | Consulta | origem do interessado, indicacao, campanha, qualidade, demanda sem vaga | abrir interessado, criar tarefa, marcar origem ruim | origem ruim, demanda reprimida |
| Segmentos e comunicados | Aprovacao | publico, elegibilidade, template, consentimento, custo, status de envio | aprovar, editar mensagem, rejeitar, acompanhar falhas | sem consentimento, publico invalido, envio falhou |

### Financeiro

| Tela | Profundidade | Conteudo obrigatorio | Acoes obrigatorias | Alertas/estados |
| --- | --- | --- | --- | --- |
| Financeiro essencial | Consulta + acao controlada | atrasos, comprovantes, links, cobrancas, promessas, excecoes pendentes | enviar link, confirmar quando permitido, registrar promessa, abrir aprovacao | atrasado, falha, sem comprovante, risco financeiro |
| Pagamento/cobranca | Acao controlada | aluno, valor, vencimento, status, historico curto, conversa | enviar lembrete, reenviar link, confirmar comprovante, criar tarefa | pago, aberto, atrasado, falhou |
| Excecoes financeiras sensiveis | Sem tela propria; aparece em Financeiro essencial, Aprovacoes, Tarefas ou Aluno | excecao, impacto, contrato/pagamento afetado, risco, motivo e origem | aprovar, rejeitar, pedir mais dados, registrar motivo, abrir aluno/movimentacao | aguardando aprovacao, risco alto, disputa |
| Contratos/documentos | Consulta + acao simples | contrato, recibo, termo, status, assinatura/envio, aluno | ver, reenviar, anexar quando permitido, abrir aluno | pendente, enviado, assinado, vencido |

### Operacao, retencao e casos

| Tela | Profundidade | Conteudo obrigatorio | Acoes obrigatorias | Alertas/estados |
| --- | --- | --- | --- | --- |
| Tarefas | Acao completa | minhas tarefas, por prazo, por origem, por caso, atrasadas | assumir, concluir, delegar, comentar, reagendar | atrasada, sem dono, aguardando aluno |
| Aprovacoes | Acao completa | proposta, antes/depois, impacto, risco, custo/cota, mensagem, solicitante | aprovar, editar, rejeitar, pedir mais dados | pendente, editada, expirada, risco alto |
| Caso operacional | Acao parcial/completa | resumo, dono, prazo, origem, timeline curta, proxima acao | comentar, atribuir, resolver, escalar, abrir origem | bloqueado, aguardando humano, incidente, resolvido |
| Jornadas prioritarias | Consulta + acao | cartoes de jornada urgentes, etapa, dono, risco, prazo | abrir caso, mover etapa simples, assumir, delegar | risco alto, sem dono, bloqueado |
| Qualidade de dados | Aprovacao/consulta | duplicidade, dado ausente, vinculo incorreto, fluxo bloqueado, objetos afetados | corrigir simples, mesclar se seguro, criar tarefa, pedir revisao | duplicado, incompleto, bloqueando automacao |
| Retencao | Consulta + acao | alunos em risco, queda de frequencia, inativos, primeira semana, retorno pendente | abrir aluno, criar tarefa, preparar contato, acompanhar retorno | risco baixo/medio/alto, inativo |
| Cancelamentos e reativacao | Acao controlada | pedido de cancelamento, motivo, aluno, plano, risco, elegibilidade | registrar motivo, abrir plano de salvamento, iniciar reativacao aprovada | risco, cancelado, nao contatar |
| Reclamacao/caso sensivel | Acao controlada | severidade, dono, prazo, historico curto, resposta, automacao pausada | responder, escalar, pausar automacao, acompanhar recuperacao | severo, aguardando dono, resolvido, confianca pendente |

### Agentes, cotas e governanca leve

| Tela | Profundidade | Conteudo obrigatorio | Acoes obrigatorias | Alertas/estados |
| --- | --- | --- | --- | --- |
| Agentes/alertas | Consulta + emergencia | fluxos pausados, bloqueados, incidentes, execucoes falhas, custo alto | pausar emergencia, abrir incidente, ver explicacao, reprocessar se seguro | falhou, bloqueado, incidente, cota alta |
| Agentes e fluxos | Configuracao essencial | agentes ativos, fluxos principais, modo, limites basicos, templates, ultima execucao | ativar, pausar, mudar modo, editar limite simples, testar exemplo, abrir configuracao avancada no web | bloqueado por plano, pausado, ativo, sem dados |
| Execucao de agente | Consulta + acao segura | fluxo, resultado, custo, ferramenta usada, erro, objeto afetado | ver explicacao, abrir incidente, reprocessar se seguro, pausar fluxo | sucesso, falhou, bloqueado, aguardando aprovacao |
| Cotas | Consulta + acao simples | consumo, limite, previsao, origem do custo, alertas, pacote, modo economia | ver motivo, comprar/solicitar pacote, pausar baixa prioridade | 70%, 90%, 100%, pacote ativo |
| Relatorios resumidos | Consulta | indicadores essenciais de dinheiro, vendas, ocupacao, risco, agentes | abrir origem, compartilhar resumo, exportar depois no web | sem dados, atualizado, alerta |
| Auditoria resumida | Consulta sensivel | evento sensivel, quem mudou, objeto, horario, antes/depois resumido | abrir objeto, reportar problema | sem permissao, evento critico |
| Privacidade/solicitacoes | Aprovacao sensivel | solicitacao LGPD, opt-out, acesso de suporte, prazo, identidade | aprovar, negar, expirar acesso, abrir detalhe | pendente, validando, acesso ativo |
| Integracoes/status | Consulta + alerta | WhatsApp, pagamentos, importacao, ultima sincronizacao, falhas | abrir incidente, reprocessar quando seguro, avisar responsavel | conectado, falhou, provedor indisponivel |
| Assinatura/billing | Consulta + acao simples | plano, status, fatura, pacote de cota, falha de pagamento | ver fatura, abrir portal, solicitar pacote | ativo, vencido, falha, pacote ativo |

## O que fica fora do mobile como fluxo principal

Fora do mobile nao significa invisivel. Significa que nao vira fluxo principal de execucao no app.

| Area | Mobile ainda mostra? | O que fica fora |
| --- | --- | --- |
| Configuracao avancada de agentes | Sim, setup guiado, modo, limite e teste simples | simulacao profunda, regra complexa, versao/rollback completo, analise longa de execucoes |
| Politicas operacionais | Sim, bloqueio/impacto resumido | criar politica, versionar regra, simular impacto complexo |
| Integracoes | Sim, conectar/testar canal essencial, status e falha | reconfigurar credenciais avancadas, revisar logs longos |
| Auditoria | Sim, resumo sensivel | busca longa, filtros avancados, exportacao |
| Importacao/exportacao | Sim, alerta de job/falha se afetar rotina | iniciar importacao grande, baixar exportacao, backup |
| Permissoes de equipe | Sim, convite basico, "sem permissao" e pedido de revisao | editar matriz completa de papel/permissao |
| Canais/templates | Sim, falha de canal/template | configurar canal, aprovar template grande |
| Relatorios profundos | Sim, resumo acionavel | BI, tabelas longas, exportacoes |
| Billing completo | Sim, status/fatura/pacote | gestao completa de assinatura |
| Campos customizados | Nao, salvo reflexo no formulario | criar campo, mudar metadados |
| Recursos/salas/equipamentos | Sim, indisponibilidade e impacto | configuracao estrutural |

## Profundidade por papel

| Papel | Mobile precisa permitir | Nao deve mostrar por padrao |
| --- | --- | --- |
| Dono/gestor | tudo do dia, aprovacoes, financeiro essencial, cotas, agentes, casos sensiveis, privacidade, billing resumido | configuracao pesada fora do Mais/web |
| Recepcao/operacao | inbox, agenda, turmas, reposicoes, tarefas, alunos, interessados, qualidade de dados simples | financeiro sensivel, historico restrito, billing |
| Professor | agenda, turmas/aulas permitidas, chamada quando permitido, aluno permitido, notas, handoff | financeiro, vendas completas, dados sensiveis nao permitidos |
| Financeiro | financeiro essencial, cobrancas, comprovantes, aprovacoes financeiras, aluno financeiro, contratos/documentos | historico sensivel de saude |
| Admin | operacao, tarefas, aprovacoes permitidas, alertas, qualidade de dados, integracoes/status | billing se nao tiver permissao |

## Estados obrigatorios no mobile

| Estado | Onde aparece |
| --- | --- |
| Sem pendencias | Hoje, tarefas, aprovacoes. |
| Urgente | Hoje, notificacoes, casos, reclamacoes. |
| Aguardando humano | Inbox, casos, agentes. |
| Agente pausado | Inbox, agentes, casos. |
| Cota perto do limite | Hoje, cotas, agentes. |
| Cota esgotada | Hoje, cotas, aprovacoes, agentes. |
| Sem permissao | Aluno, historico, financeiro, aprovacao. |
| Dados bloqueando fluxo | Hoje, casos, agentes, qualidade de dados. |
| Falha de envio | Inbox, conversa, agentes. |
| Risco alto | Retencao, reclamacoes, financeiro, aprovacoes. |
| Chamada pendente | Hoje, agenda, aula. |
| Reposicao pendente | Hoje, agenda, reposicoes. |
| Comprovante pendente | Hoje, financeiro. |
| Turma com vaga | Hoje, agenda, turmas. |
| Evento lotado | Agenda, eventos. |
| Integracao falhou | Hoje, agentes, integracoes/status. |
| Acesso de suporte ativo | Hoje, privacidade/solicitacoes. |
| Setup incompleto | Hoje, Setup inicial, Configuracoes essenciais. |
| Agente sem configuracao | Hoje, Configuracao inicial de agentes, Agentes e fluxos. |

## Regra de seguranca mobile

Se uma acao for sensivel, o app deve mostrar antes de executar:

- o que vai mudar;
- quem sera afetado;
- custo/cota se existir;
- risco;
- permissao exigida;
- possibilidade de editar ou negar;
- registro de auditoria.

O app deve ser rapido, mas nao pode ser cego.

## Conclusao

O app mobile precisa ser completo para ativar e operar o dia a dia, nao completo para administracao estrutural.

Decisao final desta rodada:

```text
mobile ativa o studio e opera o dia a dia;
web aprofunda, governa e audita.
```

Essa versao inclui todas as areas que podem virar acao, consulta, aprovacao ou alerta util no celular. O que ficou fora e apenas o que exige tela grande, revisao longa, configuracao sensivel ou operacao rara.
