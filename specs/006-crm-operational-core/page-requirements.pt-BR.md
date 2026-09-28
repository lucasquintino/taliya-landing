# Paginas necessarias e conteudo de cada pagina - PT-BR

> Status: mapa concreto de telas. Este documento responde quais paginas precisam existir para cobrir os 157 casos de uso e o que cada pagina precisa conter.

## Resposta direta

Os 157 casos de uso nao pedem 157 paginas.

Eles pedem:

- 12 entradas principais de menu no CRM web;
- 38 paginas ou superficies funcionais no total, contando onboarding, subpaginas, detalhes, centrais de caso, qualidade de dados e configuracoes;
- 12 telas/areas principais no app mobile, agrupando acoes do dia a dia;
- muitas acoes contextuais dentro das paginas, em vez de novas paginas para cada caso.

## Menu principal recomendado

| Menu | Por que existe |
| --- | --- |
| Hoje | Mesa de comando diaria do gestor. |
| Inbox | Atendimento, WhatsApp, conversas e handoff. |
| Alunos | Perfil, agenda, plano, historico permitido e contexto. |
| Agenda | Calendario, aula, chamada, reposicoes e vagas. |
| Vendas | Interessados, experimentais e conversao em aluno. |
| Financeiro | Pagamentos, cobrancas, contratos e casos financeiros. |
| Retencao | Risco, cancelamento, reativacao e satisfacao. |
| Operacao | Jornadas, casos, tarefas, aprovacoes, alertas e incidentes. |
| Agentes | Agentes, fluxos, simulacao, execucoes e incidentes. |
| Uso e cotas | Cotas, custos, modo economia e pacotes. |
| Relatorios | Paineis e exportacoes enxutas. |
| Configuracoes | Studio, equipe, permissoes, canais, regras e templates. |

## Todas as paginas e o que cada uma precisa ter

A coluna "Casos donos" mostra quantos casos foram mapeados diretamente para aquela pagina como dona principal. Algumas paginas com 0 casos donos ainda sao necessarias porque funcionam como tela de apoio, perfil, aprovacao ou configuracao usada por casos de outras paginas.

| Menu principal | Grupo | Pagina | Tipo | Casos donos | O que precisa ter | Acoes essenciais | Estados essenciais | Mobile |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Nao | Entrada | Onboarding e configuracao inicial | Fluxo de ativacao | 6 | claim da conta paga; perfil do studio; checklist inicial; importacao; duplicidades; convite da equipe; revisao final | continuar setup; importar dados; resolver duplicidade; convidar equipe; abrir CRM | incompleto; bloqueado por dados; importacao com erro; pronto para operar | Setup guiado |
| Sim | Operacao diaria | Hoje | Dashboard operacional | 4 | prioridades do dia; dinheiro em aberto; fila humana; alertas; gargalos; resumo do dia/semana | abrir caso; delegar tarefa; aprovar acao; ver alerta; ir para origem do problema | sem pendencias; alerta critico; cota perto do limite; dados bloqueando automacao | Sim |
| Sim | Atendimento | Inbox e conversas | Workspace profundo | 6 | conversas WhatsApp; status; responsavel; aluno/interessado vinculado; resumo; historico; mensagens; anexos | responder; assumir do agente; pedir sugestao; classificar; criar tarefa; abrir caso; registrar opt-out | novo; aguardando humano; agente pausado; sem consentimento; mensagem falhou | Sim |
| Nao | Atendimento | Contatos | Lista herdada/contextual | 3 | contatos; telefones compartilhados; preferencias de contato; bloqueios; opt-out | editar contato; vincular aluno quando necessario; resolver telefone compartilhado | duplicado; sem permissao; opt-out; dados incompletos | Parcial. Sem modulo proprio de responsaveis/familia/consentimentos no MVP. |
| Nao | Operacao | Qualidade de dados | Fila de saneamento | 2 | duplicidades; dados obrigatorios ausentes; vinculos incorretos; contatos compartilhados; registros arquivados; dados bloqueando fluxo | mesclar; manter separado; corrigir vinculo; arquivar; reativar; desbloquear fluxo; pedir revisao | duplicado; incompleto; conflito; bloqueando automacao; aguardando revisao; resolvido | Aprovacao/consulta |
| Sim | Alunos | Alunos e perfil do aluno | Workspace profundo | 0 | lista de alunos; perfil; plano; agenda; pagamentos; presencas; reposicoes; riscos; tarefas; timeline resumida | abrir conversa; agendar; alterar plano; criar tarefa; registrar observacao; ver historico permitido | ativo; pausado; inadimplente; risco; dados sensiveis restritos | Sim |
| Nao | Alunos | Historico do aluno | Subarea sensivel | 8 | linha do tempo; documentos; anamnese; restricoes; objetivos; evolucao; permissoes de visibilidade | adicionar nota; anexar documento; corrigir historico; compartilhar contexto seguro; revisar permissao | sem permissao; dado sensivel; aguardando consentimento; revisao necessaria | Parcial |
| Nao | Alunos | Professor e notas | Tela operacional de professor | 4 | aulas do professor; contexto permitido; observacoes pendentes; lembretes; handoff entre professores | ver contexto; registrar nota; criar handoff; marcar lembrete | nota pendente; contexto restrito; aula sem chamada | Sim |
| Sim | Agenda | Agenda | Calendario operacional | 1 | calendario; dia; semana; aulas; conflitos; capacidade; filtros por professor/turma/status | abrir aula; criar aula; alterar horario; ver conflito; abrir reposicao | lotado; vaga aberta; conflito; feriado; professor indisponivel | Sim |
| Nao | Agenda | Grade, turmas e eventos | Configuracao operacional | 4 | grade recorrente; turmas; capacidade; professor opcional; eventos; workshops; bloqueios aplicados | criar turma; ajustar grade; criar evento; simular impacto; avisar turma; bloqueio apenas situacional | capacidade excedida; bloqueio aplicado; professor indisponivel; feriado/recesso | Consulta |
| Nao | Agenda | Aula e chamada | Tela de execucao | 7 | alunos da aula; presenca; faltas; no-show; observacoes; creditos gerados; contexto do professor | fazer chamada; corrigir presenca; registrar falta; abrir reposicao; adicionar observacao | chamada pendente; falta avisada; no-show; credito criado | Sim |
| Nao | Agenda | Reposicoes e lista de espera | Fila operacional | 5 | pedidos de reposicao; creditos; vagas abertas; lista de espera; candidatos para encaixe | encontrar encaixe; reservar vaga; convidar aluno; consumir credito; expirar credito | sem vaga; conflito de horario; aguardando resposta; credito vencido | Sim |
| Sim | Vendas | Interessados e vendas | Pipeline comercial | 7 | interessados; etapa; origem simples; proxima acao; conversas; qualificacao; objeções; follow-up | cadastrar no pipeline; qualificar; responder duvida; criar follow-up; filtrar perdido; converter | novo; quente; sem resposta; sem vaga; perdido | Parcial |
| Nao | Vendas | Aulas experimentais | Agenda comercial | 4 | experimentais agendadas; lembretes; faltas; pos-aula; remarques; professor relacionado | agendar; enviar lembrete; remarcar; fazer pos-aula; converter | agendada; lembrete enviado; faltou; concluiu; converter agora | Sim |
| Nao | Vendas | Matriculas | Checklist de conversao | 2 | pre-matricula simples; dados obrigatorios; plano escolhido; primeira aula; pagamento inicial quando exigido; metodos habilitados | criar pre-matricula; validar dados; escolher primeira aula; gerar/enviar cobranca inicial; converter aluno; gerar tarefas | faltando dado; pagamento pendente; pronto para aluno; bloqueado por conflito/aprovacao | Consulta |
| Sim | Financeiro | Financeiro | Visao geral | 2 | filas financeiras; prioridades; atrasados; falhas; excecoes; dinheiro em aberto; indicadores essenciais | abrir cobranca; ver pagamento; abrir excecao contextual; exportar | normal; atraso alto; conciliacao pendente; cota/automacao bloqueada | Consulta |
| Nao | Financeiro | Movimentacoes financeiras | Fila/tabela financeira | 6 | pagamentos; vencimentos; atrasos; Pix/link; conciliacao; falhas; comprovantes; ajustes | enviar lembrete; enviar link; confirmar; conciliar; criar promessa; criar tarefa; pedir aprovacao | aberto; pago; atrasado; falhou; sem identificacao | Parcial |
| Nao | Financeiro | Excecoes financeiras sensiveis | Sem pagina propria no MVP | 9 | excecoes; pausa; congelamento; bloqueio/liberacao; cortesia; acordos; disputas; reembolsos; alteracao de plano | resolver via Financeiro, Movimentacoes, Aprovacoes, Tarefas, Aluno ou Operacao | aguardando aprovacao; risco alto; acordo ativo; disputa | Aprovacao |
| Nao | Financeiro | Contratos e documentos financeiros | Documentos | 2 | contratos; termos; recibos; notas; comprovantes; anexos; status de assinatura/envio | ver; reenviar; anexar; baixar quando permitido; abrir aluno; abrir movimentacao; auditar | rascunho; pendente; enviado; visualizado; assinado; vencido; arquivado | Rota herdada em `/app/financeiro/documentos`; sem imagem propria no MVP. |
| Sim | Retencao | Retencao | Painel e fila | 10 | riscos; queda de frequencia; inativos; retorno; primeira semana; satisfacao; marcos | criar tarefa; preparar mensagem; abrir caso; segmentar risco; acompanhar retorno | risco baixo/medio/alto; novo aluno; inativo; retorno pendente | Parcial |
| Nao | Retencao | Cancelamentos e reativacao | Central de relacionamento | 3 | risco de cancelamento; cancelamentos; pausas; pos-cancelamento; ex-alunos; alunos pausados/inativos; reativacao | abrir plano de salvamento; registrar motivo; converter pausa; acompanhar pos-cancelamento; reservar vaga com validacao; iniciar reativacao | risco; salvamento; cancelado; ex-aluno elegivel; reativado; nao contatar | Parcial |
| Nao | Retencao | Reclamacoes e casos sensiveis | Central de caso sensivel | 3 | reclamacoes; severidade; dono; prazo; automacoes pausadas; resolucao; recuperacao de confianca | classificar; pausar automacao; escalar; responder; resolver; acompanhar recuperacao | novo; severo; aguardando dono; resolvido; confiança nao recuperada | Aprovacao |
| Sim | Operacao | Jornadas e operacao | Central operacional em mapa de jornadas | 8 | jornadas por etapa; casos; incidentes; alertas; dados bloqueando fluxo; problemas de integracao; comunicados operacionais | abrir caso; atribuir; mover etapa; pausar fluxo; corrigir dado; reprocessar; fechar | aberto; bloqueado; aguardando humano; incidente; resolvido | Sim |
| Nao | Operacao | Tarefas e operacao | Fila de tarefas | 3 | tarefas por dono; prazo; origem; caso vinculado; prioridade; SLA/prazo combinado | assumir; delegar; concluir; comentar; reagendar | atrasada; sem dono; aguardando aluno; concluida | Sim |
| Nao | Operacao | Aprovacoes | Fila de decisoes | 0 | acoes sugeridas; antes/depois; risco; custo; mensagem; impacto; quem pediu | aprovar; editar; rejeitar; pedir mais dados; executar | pendente; editada; aprovada; rejeitada; expirada | Sim |
| Sim | Agentes | Agentes e fluxos | Configuracao de agentes | 7 | agentes ativos; fluxos; modo manual/sugestao/automatico; regras; limites; templates | ativar; pausar; configurar; simular; editar regra; ver execucoes | bloqueado por plano; pausado; ativo; sem dados | Configuracao essencial |
| Nao | Agentes | Execucoes e incidentes de agentes | Observabilidade | 4 | execucoes; resultado; custo; ferramenta usada; erro; incidente; correcao; auditoria | explicar falha; abrir incidente; corrigir dado; reexecutar quando seguro; pausar fluxo | sucesso; aguardando aprovacao; bloqueado; falhou; incidente | Alerta |
| Sim | Uso | Uso, cotas e economia | Governanca de custo | 3 | cota usada; restante; origem do custo; alertas; modo economia; pacote extra; limite por fluxo | ver consumo; ajustar economia; comprar pacote; pausar baixa prioridade | 70%; 90%; 100%; pacote ativo; automacao convertida em tarefa | Consulta |
| Sim | Relatorios | Relatorios e exportacoes | Paineis enxutos | 8 | financeiro; vendas; ocupacao; origens; exportacoes; backup; contabilidade; previsao de caixa enxuta | filtrar; exportar; agendar relatorio; abrir casos relacionados | sem dados; exportando; pronto; sem permissao | Consulta |
| Sim | Configuracoes | Configuracoes | Configuracao web | 7 | studio; equipe; permissoes; canais; respostas; agenda; financeiro; vendas; retencao; privacidade; campos; notificacoes | editar; testar; salvar; ver impacto; auditar | incompleto; sem permissao; mudanca sensivel; salvo | Configuracao essencial |
| Nao | Configuracoes | Politicas operacionais | Regras versionadas | 0 | politicas de falta; reposicao; cancelamento; comunicacao; financeiro; data de vigencia; simulacao | criar versao; simular impacto; aprovar; publicar; reverter | rascunho; aguardando aprovacao; ativa; revertida | Nao |
| Nao | Agenda | Bloqueios de agenda, feriados e disponibilidade | Fluxo contextual | 4 | feriado; recesso; fechamento pontual; horario bloqueado; professor indisponivel; recurso opcional; impacto na agenda | criar bloqueio; simular aulas afetadas; criar tarefas; avisar envolvidos; reabrir disponibilidade | fechado; indisponivel; professor indisponivel; impacto pendente | Consulta |
| Nao | Comunicacao | Comunicados | Agente/superficie pos-MVP | 3 | publico simples; elegibilidade de canal; template; custo; aprovacao; status de envio | criar comunicado; validar publico/canal; aprovar envio; acompanhar falhas | publico invalido; canal indisponivel; aguardando aprovacao; enviado | Fora do MVP atual; nao pertence a Vendas/Interessados. |
| Nao | Administracao | Integracoes | Administracao tecnica enxuta | 2 | WhatsApp; pagamentos; importacao; status; logs; falhas; ultima sincronizacao | conectar; testar; ver log; reprocessar; abrir incidente | conectado; falhou; aguardando provedor; erro recorrente | Nao |
| Nao | Administracao | Auditoria | Trilha de seguranca | 1 | quem mudou; o que mudou; antes/depois; origem; objeto; horario; risco | filtrar; abrir objeto; exportar quando permitido | sem permissao; evento sensivel; alteracao critica | Consulta |
| Nao | Administracao | Privacidade e solicitacoes | Governanca sensivel | 4 | pedidos LGPD; opt-out; exportar/apagar/anonimizar; acesso do suporte; consentimentos | validar identidade; aprovar; executar; negar; auditar; expirar acesso | pendente; validando; executado; negado; acesso ativo | Aprovacao |
| Nao | Administracao | Assinatura e billing | Administracao enxuta | 2 | plano Taliya; faturas; add-ons; pacote de cota; status de pagamento | ver fatura; abrir portal; comprar pacote; atualizar plano | ativo; vencido; falha; pacote ativo | Consulta |

## App mobile necessario

| Tela mobile | O que precisa ter |
| --- | --- |
| Hoje | prioridades, alertas, tarefas, aprovacoes urgentes. |
| Inbox | conversas, resposta rapida, assumir do agente, anexos essenciais. |
| Agenda | agenda do dia, aula, reposicao, vaga aberta. |
| Chamada | lista da aula, presenca, falta, observacao rapida. |
| Aluno | perfil resumido, contato, plano, agenda, riscos e historico permitido. |
| Professor | contexto da aula, notas pendentes, observacao, handoff. |
| Tarefas | minhas tarefas, atrasadas, concluir, delegar. |
| Aprovacoes | aprovar, editar, rejeitar, ver risco e impacto. |
| Financeiro essencial | atraso, comprovante, link, aprovacao de excecao. |
| Reclamacoes/casos | caso sensivel, dono, prazo, resposta, pausa de automacao. |
| Agentes/alertas | incidente, fluxo pausado, execucao bloqueada, pausar emergencia. |
| Uso/cotas | consumo, alerta de limite, pacote, modo economia. |

## Cobertura dos 157 casos

A cobertura detalhada caso por caso esta em `page-case-coverage.pt-BR.csv`.
