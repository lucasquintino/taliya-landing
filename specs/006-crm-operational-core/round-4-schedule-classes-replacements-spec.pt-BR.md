# Rodada 4 - Agenda, turmas, aulas e reposicoes - PT-BR

> Status: v0.1. Esta rodada define a base funcional e a primeira especificacao profunda das telas de Agenda, Turmas, Aula, Chamada, Reposicoes, Lista de espera, Eventos/workshops e Recursos/disponibilidade.

## Objetivo operacional

Fazer o gestor, recepcao e professor operarem um dia real de Pilates no Taliya: ver aulas, entender capacidade, fazer chamada, tratar faltas, gerar/usar creditos de reposicao, recuperar vaga aberta, resolver conflitos e avisar alunos sem depender de agente ativo.

## Limite desta v0.1

Esta versao orienta produto, rotas, objetos, estados e acoes principais. Ainda falta, em passada posterior:

- fechar formulas finais de encaixe e prioridade da lista de espera;
- definir politica padrao de credito de reposicao;
- decidir integracao com agenda externa;
- decidir escopo final de eventos/workshops no MVP;
- definir se bloqueios recorrentes avancados precisam configuracao propria alem do fluxo simples de Bloqueio de agenda;
- fechar microcopy de conflito, vaga, falta, no-show e credito;
- transformar esta rodada em prompts finais de UI.

## Usuarios envolvidos

| Usuario | Papel na rodada |
| --- | --- |
| Dono/gestor | Configura grade, capacidade, politicas, eventos e resolve excecoes. |
| Admin | Ajusta turmas, recursos, feriados, reposicoes e conflitos. |
| Recepcao/operacao | Opera agenda, encaixes, avisos, lista de espera, faltas e reposicoes. |
| Professor | Ve aulas permitidas, faz chamada, registra observacao e consulta contexto permitido. |
| Financeiro | Consulta impacto quando presenca/reposicao afeta plano, cobranca ou bloqueio. |
| Agente/runtime | Sugere convites, prioriza candidatos, cria tarefas/casos e envia mensagens quando permitido. |

## Objetos de negocio

- Grade semanal;
- Turma;
- Aula;
- Chamada/presenca;
- Credito de reposicao;
- Pedido de reposicao;
- Lista de espera;
- Evento/workshop;
- Recurso;
- Indisponibilidade;
- Aluno;
- Professor/membro da equipe;
- Contato;
- Conversa/mensagem;
- Template/modelo;
- Politica operacional;
- Tarefa;
- Caso operacional;
- Aprovacao;
- Notificacao;
- Evento de historico;
- Evento de auditoria;
- Execucao de fluxo;
- Lancamento de cota.

## Jornadas cobertas

| Jornada | Resultado esperado |
| --- | --- |
| Configurar regras da agenda | Studio define grade, tolerancia, reposicao, capacidade e limites antes da operacao. |
| Criar/ajustar grade semanal | Turmas recorrentes ficam claras, com professor, horario, capacidade e impacto. |
| Criar turma | Turma nasce com alunos, capacidade, horario, professor e status operacional. |
| Revisar agenda do dia | Usuario ve aulas, conflitos, vagas, chamadas pendentes e proximas acoes. |
| Abrir uma aula | Usuario ve alunos esperados, professor, sala/recurso, chamada, avisos e contexto. |
| Fazer chamada | Professor/recepcao marca presenca, falta avisada, no-show e observacao. |
| Confirmar presenca | Sistema registra confirmacao manual, por WhatsApp ou por agente conforme regra. |
| Registrar falta avisada | Falta pode gerar credito de reposicao conforme politica vigente. |
| Tratar falta sem aviso | No-show pode gerar tarefa, alerta de retencao ou regra financeira. |
| Receber pedido de reposicao | Pedido entra com aluno, credito, preferencia, prazo, conflito e status. |
| Controlar creditos de reposicao | Usuario ve origem, validade, status, aula de destino e politica aplicada. |
| Recuperar vaga aberta | Vaga gerada por falta/cancelamento aciona candidatos e convite seguro. |
| Encontrar encaixe | CRM calcula candidatos por regra; IA so explica, prioriza ou redige quando util. |
| Gerenciar lista de espera | Pessoas aguardando vaga entram por prioridade, horario, origem e consentimento. |
| Alterar horario fixo de aluno | Mudanca simula impacto em turma, plano, reposicoes e comunicacoes. |
| Cancelar ou alterar aula pelo studio | Impacto em alunos, professor, recursos e avisos fica visivel antes de publicar. |
| Resolver conflito de capacidade | Excesso, sobreposicao ou recurso indisponivel vira ajuste, aprovacao ou caso. |
| Conferir primeira aula do aluno | Novo aluno aparece em agenda/checklist com contexto e pendencias. |
| Gerenciar workshop/aula especial | Evento tem capacidade, inscricoes, lista, comunicacao e chamada. |
| Planejar feriado/recesso | Fechamento simula aulas afetadas e cria comunicacoes/tarefas. |
| Tratar indisponibilidade de professor/sala | Sistema mostra impacto, substituicao, cancelamento, aviso e caso. |

## Regras de negocio

1. Agenda CRM e a fonte operacional de verdade para turmas, aulas, chamada e reposicoes.
2. Grade recorrente gera aulas, mas ajuste manual autorizado vence recorrencia no dia afetado.
3. Mudanca de turma, horario, professor, capacidade ou recurso deve mostrar impacto antes de publicar quando afetar alunos.
4. Turma com vaga pode acionar encaixe programatico, tarefa manual, copiloto ou agente conforme plano e modo.
5. Encontrar encaixe nao precisa de IA para calcular candidatos; IA entra para explicar prioridade, redigir convite e tratar excecao.
6. Chamada humana/correcao auditada vence classificacao automatica.
7. Falta avisada, no-show e cancelamento devem preservar origem e politica aplicada.
8. Credito de reposicao precisa guardar aula original, validade, status, aula de destino e motivo.
9. Convite externo para reposicao/lista de espera respeita consentimento, janela, template, cota e opt-out.
10. Lista de espera precisa ter prioridade, horario desejado, origem, status e proxima acao.
11. Professor so ve aulas/alunos permitidos e contexto autorizado.
12. Evento/workshop segue regra de capacidade, inscricao, comunicacao e chamada propria.
13. Feriado, recesso e indisponibilidade devem gerar simulacao de impacto.
14. Plano Base opera agenda, chamada, vagas e reposicoes manualmente.
15. Acao automatica que muda agenda ou envia mensagem externa exige politica, auditoria e fallback.
16. Consumo de aula e direito de reposicao seguem o contrato configuravel em `billing-lesson-consumption-models.pt-BR.md`; a agenda nao deve presumir que todo aluno usa mensalidade fixa, pacote de creditos ou reposicao padrao.

## Modos de execucao

| Modo | Como funciona nesta rodada |
| --- | --- |
| Manual | Usuario cria turma, ajusta aula, faz chamada, registra falta, gera credito, escolhe encaixe e envia mensagem manual. |
| Copiloto | Sistema/IA sugere candidatos, explica conflitos, redige convite, resume impacto e prepara tarefa/aprovacao. |
| Autonomo | Agente envia convites, confirma respostas ou cria tarefas apenas quando politica, consentimento, cota, template e risco permitem. |

## Entradas e saidas

| Tipo | Exemplos |
| --- | --- |
| Entradas | grade, horario, professor, capacidade, sala/recurso, chamada, falta, pedido WhatsApp, lista de espera, feriado, indisponibilidade. |
| Saidas | aula criada/alterada, chamada concluida, credito gerado/usado, vaga reservada, convite enviado, tarefa, caso, aprovacao, notificacao, auditoria. |

## Fonte da verdade

| Dado | Fonte da verdade |
| --- | --- |
| Grade/turma | CRM Agenda. |
| Aula | CRM Agenda; ajuste manual autorizado vence recorrencia. |
| Chamada/presenca | CRM Aula; correcao humana auditada vence automacao. |
| Reposicao | CRM Agenda/Reposicoes + politica vigente. |
| Lista de espera | CRM Agenda/Vendas, conforme origem. |
| Evento/workshop | CRM Agenda/Eventos. |
| Recurso/indisponibilidade | CRM Configuracoes/Recursos. |
| Aviso enviado | CRM Tentativa de envio + provedor de canal. |

## Eventos e gatilhos

| Gatilho | Comportamento esperado |
| --- | --- |
| Inicio do dia | Agenda cria prioridades: chamada pendente, conflito, vaga aberta, aula sem professor, reposicao pendente. |
| Falta avisada | Aplicar politica, gerar credito se elegivel e procurar encaixe/abrir tarefa. |
| No-show | Registrar presenca, atualizar risco e criar tarefa se regra pedir. |
| Vaga aberta | Calcular candidatos programaticamente e preparar convite manual/copiloto/autonomo. |
| Pedido de reposicao | Validar credito, horario, conflito e consentimento. |
| Aula alterada/cancelada | Simular impacto, pedir aprovacao quando sensivel e avisar envolvidos. |
| Professor/recurso indisponivel | Mostrar aulas afetadas e opcoes de substituicao, cancelamento ou tarefa. |
| Feriado/recesso publicado | Gerar impacto em aulas, reposicoes, comunicados e tarefas. |
| Chamada atrasada | Notificar professor/operacao e subir para Hoje. |
| Evento lotado | Abrir lista de espera ou bloquear novas inscricoes. |

## Telas web desta rodada

1. Agenda.
2. Grade, turmas e eventos.
3. Aula e chamada.
4. Reposicoes e encaixe.
5. Bloqueios de agenda, feriados e indisponibilidade.

## Telas mobile desta rodada

1. Agenda.
2. Turmas.
3. Aula.
4. Chamada.
5. Reposicoes.
6. Lista de espera futura/consulta, se entrar no produto.
7. Eventos/workshops.
8. Bloqueios, feriados e disponibilidade.

## Tela web: Agenda

| Campo | Definicao |
| --- | --- |
| Tipo | Web calendario operacional; mobile acao completa. |
| Rotas | `/app/agenda`. |
| Objetivo | Mostrar dia/semana de aulas, conflitos, vagas, chamadas pendentes e acoes imediatas. |
| Usuario principal | Recepcao/operacao. |
| Usuarios secundarios | Dono, admin, professor, financeiro parcial. |
| Blocos | calendario dia/semana, filtros, aulas, conflitos, capacidade, vagas abertas, reposicoes pendentes, chamadas pendentes, painel de detalhe. |
| Campos exibidos | horario, aula, turma, professor, sala/recurso, capacidade, vagas, chamada, status, conflitos, reposicoes, alertas. |
| Campos editaveis | data/horario quando permitido, professor, sala/recurso, capacidade pontual, status, observacao operacional. |
| Acoes | abrir aula, criar aula, alterar horario, abrir turma, fazer chamada, ver conflito, abrir reposicao, encontrar encaixe, avisar envolvidos. |
| Estados | normal, lotado, vaga aberta, conflito, chamada pendente, feriado, professor indisponivel, sala indisponivel, aula cancelada. |
| Permissoes | professor ve apenas aulas permitidas; operacao ajusta rotina; mudancas amplas exigem admin/dono. |
| IA/agentes | sugerir prioridades, explicar conflito e preparar mensagem; calculo de vaga/encaixe e programatico. |
| Cotas | explicacao/redacao/envio por IA consomem cota; calendario e calculo de vaga nao. |
| Auditoria | alteracao de aula, professor, capacidade, cancelamento e aviso externo. |
| Fallback | sem cota/canal, criar tarefa e permitir aviso manual. |
| Operacao sem agentes | agenda, chamada, reposicao, encaixe e aviso manual funcionam. |

## Tela web: Grade, turmas e eventos

| Campo | Definicao |
| --- | --- |
| Tipo | Web configuracao operacional; mobile consulta + acoes essenciais. |
| Rotas | `/app/grade`, `/app/turmas`, `/app/turmas/[id]`, `/app/eventos`, `/app/eventos/[eventId]`, `/app/configuracoes/politicas/agenda`, `/app/configuracoes/politicas/reposicoes`. |
| Objetivo | Criar e ajustar estrutura recorrente do studio, turmas, capacidade, professor opcional e eventos especiais. |
| Usuario principal | Dono/admin. |
| Usuarios secundarios | Recepcao/operacao; professor consulta turmas permitidas. |
| Blocos | grade semanal, lista de turmas, detalhe da turma, alunos, capacidade/vagas, professor, regras de agenda/reposicao, historico de mudancas, eventos/workshops, simulacao de impacto. |
| Campos exibidos | turma, dia, horario, professor quando houver, capacidade, alunos fixos, vagas, proxima aula, status, bloqueios aplicados. |
| Campos editaveis | nome, horario, capacidade, professor opcional, alunos fixos, recurso opcional, status, regra de evento, inscricoes. |
| Acoes | criar turma, ajustar grade, pausar/encerrar turma, mover aluno, configurar regra, simular impacto, criar evento, abrir lista, avisar turma. Bloqueio e acao secundaria/situacional via menu ou contexto de indisponibilidade. |
| Estados | rascunho, ativa, cheia, com vaga, pausada, encerrada, capacidade excedida, bloqueio aplicado, feriado/recesso. |
| Permissoes | mudanca estrutural exige admin/dono; recepcao pode ajustes permitidos; professor consulta. |
| IA/agentes | sugerir redistribuicao, detectar excesso, redigir comunicado e criar tarefas. |
| Cotas | sugestao/redacao/envio consomem cota; simulacao estrutural simples nao. |
| Auditoria | mudanca de grade, capacidade, professor, aluno fixo, regra de agenda/reposicao, evento e comunicacao. |
| Fallback | mudanca insegura vira aprovacao/caso operacional. |

## Tela web: Aula e chamada

| Campo | Definicao |
| --- | --- |
| Tipo | Web execucao; mobile acao completa. |
| Rotas | `/app/aulas/[id]`. Chamada abre como painel/drawer contextual, sem pagina separada nesta rodada. |
| Objetivo | Operar uma aula concreta: alunos esperados, chamada, faltas, contexto permitido e efeitos de reposicao. |
| Usuario principal | Professor. |
| Usuarios secundarios | Recepcao/operacao, admin. |
| Blocos | resumo da aula, alunos esperados, chamada, contexto permitido, observacoes, creditos gerados, tarefas, comunicacoes, auditoria resumida. |
| Campos exibidos | horario, turma, professor, sala, alunos, presenca, falta, no-show, reposicao, observacao, restricao permitida, credito gerado. |
| Campos editaveis | presenca, falta, no-show, observacao, correcao permitida, nota, status da chamada. |
| Acoes | fazer chamada, marcar presenca, registrar falta avisada, marcar no-show, corrigir presenca, criar reposicao, abrir aluno, registrar observacao, avisar aluno/responsavel. |
| Estados | agendada, aberta, chamada pendente, chamada concluida, falta avisada, no-show, credito criado, aula cancelada, corrigida. |
| Permissoes | professor faz chamada em aulas permitidas; correcao sensivel pode exigir admin. |
| IA/agentes | lembrar chamada, sugerir observacao estruturada, explicar consequencia e preparar aviso. |
| Cotas | lembrete por regra nao consome IA; redacao/resumo com IA e envio automatico consomem. |
| Auditoria | correcao de presenca, cancelamento, geracao/uso de credito e aviso externo. |
| Fallback | sem professor/app, recepcao consegue fazer chamada no web/mobile. |

## Tela web: Reposicoes e encaixe

| Campo | Definicao |
| --- | --- |
| Tipo | Web fila operacional; mobile acao completa. |
| Rotas | `/app/reposicoes`. Creditos aparecem dentro da reposicao; lista de espera geral nao e pagina principal desta rodada. |
| Objetivo | Controlar pedidos de reposicao, direito/credito, vagas abertas, candidatos e convites de encaixe. |
| Usuario principal | Recepcao/operacao. |
| Usuarios secundarios | Dono/admin, professor consulta. |
| Blocos | pedidos, direito/credito, vagas, candidatos, convites, respostas, conflitos, detalhe da reposicao. |
| Campos exibidos | aluno, credito, validade, origem, politica, horario desejado, vaga, prioridade, conflito, status do convite, consentimento. |
| Campos editaveis | prioridade, horario desejado, observacao, status, reserva, cancelamento, motivo. |
| Acoes | encontrar encaixe, reservar vaga, convidar aluno, consumir credito, expirar credito, cancelar credito, criar tarefa, abrir conversa, abrir aula. |
| Estados | disponivel, reservado, usado, expirado, cancelado, sem vaga, conflito de horario, aguardando resposta, resposta recusada. |
| Permissoes | operacao resolve rotina; excecao de politica exige admin/dono. |
| IA/agentes | explicar ranking, redigir convite, acompanhar resposta e criar tarefa; ranking basico e programatico. |
| Cotas | envio/sugestao por IA consome cota; calculo de candidatos nao. |
| Auditoria | geracao, reserva, uso, expiracao manual, cancelamento e excecao de politica. |
| Fallback | se envio automatico bloquear, manter reserva/tarefa manual. |

## Tela web: Bloqueios de agenda, feriados e indisponibilidade

| Campo | Definicao |
| --- | --- |
| Tipo | Fluxo contextual dentro de Agenda/Grade; mobile consulta + alerta. |
| Rotas | Sem pagina principal propria nesta rodada. Inicia em `/app/agenda`, `/app/grade`, `/app/turmas/[id]` ou aula/turma afetada. Catalogo futuro pode morar em `/app/configuracoes/recursos`. |
| Objetivo | Criar feriado, recesso, fechamento pontual, indisponibilidade de professor, bloqueio de horario ou recurso opcional que afete aulas. |
| Usuario principal | Dono/admin. |
| Usuarios secundarios | Recepcao/operacao. |
| Blocos | tipo de bloqueio, periodo, escopo, aulas afetadas, simulacao de impacto, compensacao/reposicao quando aplicavel, plano de aviso. |
| Campos exibidos | tipo, periodo, escopo, professor opcional, recurso opcional, motivo, aulas afetadas, alunos afetados, status, comunicacao pendente. |
| Campos editaveis | periodo, escopo, professor opcional, recurso opcional, motivo, recorrencia, status, compensacao e plano de aviso. |
| Acoes | criar bloqueio, criar feriado/recesso, marcar professor indisponivel, simular impacto, seguir politica, gerar credito, nao gerar credito, revisar aluno por aluno, criar tarefas, avisar envolvidos, reabrir disponibilidade. |
| Estados | disponivel, indisponivel, fechado, impacto pendente, comunicado pendente, resolvido. |
| Permissoes | configuracao estrutural exige admin/dono; operacao pode abrir caso/tarefa. |
| IA/agentes | resumir impacto, explicar compensacao e redigir aviso; nao decide compensacao sensivel sozinho. |
| Cotas | redacao/envio por IA consome cota; simulacao de aulas afetadas nao. |
| Auditoria | fechamento, bloqueio, comunicacao, reabertura e alteracao de professor/recurso opcional. |
| Fallback | se decisao nao estiver clara, criar caso operacional. |

## Telas mobile

### Agenda

| Campo | Definicao |
| --- | --- |
| Profundidade | Acao completa. |
| Conteudo | dia/semana, aulas, professor, turma, capacidade, conflitos, reposicoes, chamada pendente. |
| Acoes | abrir aula, abrir turma, ver conflito, abrir reposicao, avisar envolvidos, encontrar encaixe. |
| Estados | lotado, vaga aberta, conflito, chamada pendente, professor indisponivel. |

### Turmas

| Campo | Definicao |
| --- | --- |
| Profundidade | Acao completa para rotina; estrutural parcial. |
| Conteudo | turmas do dia/semana, professor, horario, capacidade, vagas, alunos, lista de espera, proxima aula. |
| Acoes | abrir turma, ver alunos, abrir proxima aula, ver vagas, encontrar encaixe, avisar turma. |
| Estados | cheia, vaga aberta, conflito, professor/sala indisponivel. |

### Aula

| Campo | Definicao |
| --- | --- |
| Profundidade | Acao completa. |
| Conteudo | horario, turma, professor, alunos, status da chamada, contexto permitido, observacoes. |
| Acoes | abrir chamada, avisar turma, registrar observacao, abrir turma/aluno, abrir reposicao. |
| Estados | chamada pendente, aula cancelada, sala/professor indisponivel, conflito. |

### Chamada

| Campo | Definicao |
| --- | --- |
| Profundidade | Acao completa. |
| Conteudo | alunos esperados, presenca, falta, no-show, observacao, credito gerado, contexto permitido. |
| Acoes | marcar presenca, corrigir, registrar falta/no-show, criar reposicao, adicionar observacao. |
| Estados | falta avisada, no-show, credito criado, chamada concluida, correcao pendente. |

### Reposicoes

| Campo | Definicao |
| --- | --- |
| Profundidade | Acao completa. |
| Conteudo | pedidos, creditos, vagas, candidatos, conflitos, status de convite, validade. |
| Acoes | encontrar encaixe, reservar, convidar, consumir credito, expirar credito, abrir conversa. |
| Estados | sem vaga, aguardando resposta, conflito, credito vencido, reservado. |

### Lista de espera

| Campo | Definicao |
| --- | --- |
| Profundidade | Acao completa. |
| Conteudo | alunos/interessados esperando vaga, horario desejado, prioridade, origem, consentimento. |
| Acoes | convidar, reservar, criar tarefa, marcar sem vaga, abrir perfil/conversa. |
| Estados | sem vaga, resposta pendente, prioridade alta, sem consentimento. |

### Eventos/workshops

| Campo | Definicao |
| --- | --- |
| Profundidade | Acao parcial/completa conforme escopo do MVP. |
| Conteudo | eventos, capacidade, inscritos, lista, professor, data, chamada, comunicacao. |
| Acoes | abrir evento, inscrever, chamar, avisar inscritos, abrir lista. |
| Estados | rascunho, aberto, lotado, cancelado, chamada pendente. |

### Bloqueios, feriados e disponibilidade

| Campo | Definicao |
| --- | --- |
| Profundidade | Consulta + alerta. |
| Conteudo | feriado, recesso, fechamento pontual, horario bloqueado, professor indisponivel, recurso opcional, aulas afetadas, periodo, impacto. |
| Acoes | ver impacto, abrir aula, criar tarefa, avisar envolvidos se aprovado. |
| Estados | indisponivel, impacto pendente, conflito, comunicado pendente. |

## Cobertura de contratos da Rodada 0

| Contrato | Aplicacao nesta rodada |
| --- | --- |
| Dados | Usa grade, turma, aula, chamada, presenca, credito, lista, recurso, aluno, conversa e politica. |
| Ciclo de vida | Turma, aula, presenca, credito, lista de espera, evento e indisponibilidade. |
| Fonte da verdade | CRM Agenda vence; presenca humana auditada vence automacao; politica vigente explica reposicao. |
| Permissoes | Professor ve aulas permitidas; mudanca estrutural exige admin/dono. |
| Botoes | Abrir aula, fazer chamada, encontrar encaixe, reservar, convidar, avisar, simular impacto, corrigir. |
| Estados | Vaga aberta, cheia, chamada pendente, falta avisada, no-show, credito criado, conflito, indisponivel. |
| Cotas | Envio/sugestao IA consome; calculo programatico de encaixe nao. |
| Auditoria | Chamada corrigida, aula cancelada, mudanca de turma/capacidade, credito e aviso externo. |
| 0 agentes | Agenda, chamada, vagas, lista, reposicoes e avisos manuais funcionam. |

## Decisoes abertas encontradas

| Tema | Encaminhamento |
| --- | --- |
| Politica padrao de reposicao | Definir validade, limite mensal, no-show, falta avisada e excecoes. |
| Modelo de cobranca e consumo | Usar `billing-lesson-consumption-models.pt-BR.md` como fonte para mensalidade, pacote, aula avulsa, contrato, consumo e creditos. |
| Encaixe programatico | Definir formula: horario, perfil, turma, prioridade, validade, conflito e ordem de convite. |
| Disponibilidade de professor | Definir se MVP tera calendario completo de disponibilidade ou apenas indisponibilidades pontuais. |
| Eventos/workshops | Definir se entram como aula especial simples ou modulo de eventos mais completo. |

## Criterio de aceite da rodada

Rodada 4 esta pronta para revisao quando:

- agenda do dia/semana mostra aulas, conflitos, vagas e chamada pendente;
- turma mostra capacidade, alunos, vagas, professor, lista e proxima aula;
- aula/chamada funcionam no app para professor e recepcao;
- falta, no-show e correcao preservam politica, origem e auditoria;
- credito de reposicao tem origem, validade, status e destino;
- encontrar encaixe tem caminho programatico, manual, copiloto e autonomo;
- lista de espera tem prioridade, consentimento, convite e resposta;
- feriado/recesso/recurso/professor indisponivel mostram impacto;
- plano Base opera tudo sem agentes ativos.
