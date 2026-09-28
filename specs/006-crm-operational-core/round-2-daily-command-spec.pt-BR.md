# Rodada 2 - Operacao diaria e mesa de comando - PT-BR

> Status: v0.1. Esta rodada define a base funcional e a primeira especificacao profunda das telas de Hoje, Jornadas/Operacao, Tarefas, Aprovacoes, Notificacoes, Checklist do dia, Caso operacional e Jornadas prioritarias.

## Objetivo operacional

Fazer o gestor/equipe abrir o Taliya e saber imediatamente o que precisa de atencao, quem e dono, qual risco existe, qual acao deve ser tomada e se o caminho e manual, copiloto ou autonomo.

## Limite desta v0.1

Esta versao orienta produto, rotas, objetos, estados e acoes principais. Ainda falta, em passada posterior:

- amarrar cada card/fila aos IDs exatos da matriz de 157 casos;
- definir colunas finais das listas;
- definir formulas finais de prioridade;
- escrever microcopy dos estados;
- fechar pesos de score/risco;
- detalhar responsividade visual e prompts finais de UI.

## Usuarios envolvidos

| Usuario | Papel na rodada |
| --- | --- |
| Dono/gestor | Abre o dia, prioriza, aprova, delega e fecha pendencias. |
| Admin | Opera filas, casos, tarefas e configuracoes leves. |
| Recepcao/operacao | Resolve atendimento, agenda, reposicoes, interessados e tarefas. |
| Financeiro | Resolve pagamentos urgentes, comprovantes e excecoes. |
| Professor | Ve tarefas/aulas pendentes relacionadas a chamada e notas permitidas. |
| Agente/runtime | Cria sinais, tarefas, casos, sugestoes, aprovacoes e alertas conforme modo. |

## Objetos de negocio

- Caso operacional;
- Tarefa;
- Aprovacao;
- Notificacao;
- Checklist;
- Problema de dados;
- Execucao de fluxo;
- Incidente de automacao;
- Conversa;
- Aula;
- Turma;
- Presenca;
- Reposicao;
- Pagamento;
- Interessado;
- Aluno;
- Reclamacao/caso sensivel;
- Lancamento de cota;
- Evento de auditoria.

## Jornadas cobertas

| Jornada | Resultado esperado |
| --- | --- |
| Abrir prioridades do dia | Usuario ve top pendencias por risco, prazo e impacto. |
| Ver fila humana | Itens aguardando pessoa aparecem com dono/fila. |
| Acompanhar tarefas | Usuario consegue assumir, delegar, concluir e reagendar. |
| Revisar aprovacoes | Usuario aprova, edita, rejeita ou pede dados. |
| Resolver caso operacional | Usuario entende origem, timeline, objeto afetado e proxima acao. |
| Ver alertas/notificacoes | Usuario abre origem, marca lido e prioriza. |
| Abrir/fechar checklist do dia | Equipe garante rotina minima de abertura/fechamento. |
| Monitorar gargalos | Gestor ve bloqueios recorrentes e vai para origem. |

## Regras de negocio

1. Todo item acionavel deve ter dono, fila ou motivo para estar sem dono.
2. Hoje nao deve ser apenas dashboard: deve ser mesa de comando com acoes.
3. Itens de alto risco sobem acima de itens recentes.
4. Aprovacao sensivel deve mostrar antes/depois, impacto, risco, cota e auditoria que sera gerada.
5. Caso operacional e a superficie padrao para problema que cruza areas.
6. Tarefa e trabalho humano; execucao de agente nao substitui tarefa quando exige decisao.
7. Notificacao sem proxima acao deve virar aviso informativo, nao poluir fila.
8. Em cota 90/100, Hoje deve explicar o que foi downgradado para tarefa/aprovacao.
9. No plano Base, todos os itens devem ter caminho manual.

## Politicas usadas

- prioridades e SLA;
- roteamento por papel/fila;
- economia de cota;
- permissao contextual;
- auditoria de acoes sensiveis;
- notificacoes por papel;
- pausa/handoff de agente.

## Telas web desta rodada

1. Hoje.
2. Jornadas e operacao.
3. Tarefas e operacao.
4. Aprovacoes.
5. Notificacoes.
6. Checklist do dia.
7. Caso operacional.
8. Qualidade de dados como origem/bloqueio contextual.

## Telas mobile desta rodada

1. Hoje.
2. Checklist do dia.
3. Notificacoes.
4. Busca global.
5. Tarefas.
6. Aprovacoes.
7. Caso operacional.
8. Jornadas prioritarias.
9. Qualidade de dados.

## Tela web: Hoje

| Campo | Definicao |
| --- | --- |
| Tipo | Web e mobile home. |
| Rotas | `/app`, `/app/hoje`. |
| Objetivo | Mostrar prioridades e permitir acao imediata. |
| Usuario principal | Dono/gestor; tambem admin e operacao. |
| Blocos | resumo do dia, agenda proxima, fila humana, tarefas urgentes, aprovacoes, casos bloqueados, dinheiro em aberto, cota/agentes, gargalos. |
| Campos exibidos | titulo do item, area, objeto afetado, dono/fila, prazo, risco, impacto, status, cota, origem. |
| Acoes | abrir item, assumir, delegar, concluir tarefa, aprovar, rejeitar, pausar automacao, abrir origem, marcar alerta visto. |
| Estados | sem pendencias, urgente, atrasado, sem dono, cota 70/90/100, agente pausado, dados bloqueando fluxo, suporte ativo. |
| Permissoes | cada card respeita permissao do objeto; card sensivel pode mostrar resumo restrito. |
| IA/agentes | mostram sugestao/proxima acao, mas acao sensivel vira aprovacao. |
| Cotas | alertas, downgrade e bloqueios aparecem como cards acionaveis. |
| Auditoria | acoes sensiveis geram evento; abertura/visualizacao nao precisa auditar por padrao. |
| Operacao sem agentes | cards continuam vindo de tarefas, registros e regras simples. |
| Fallback | se origem falhar, card abre caso operacional ou tarefa manual. |

## Tela web: Jornadas e operacao

| Campo | Definicao |
| --- | --- |
| Tipo | Web completo; mobile mostra jornadas prioritarias. |
| Rotas | `/app/operacao`, `/app/operacao/[caseId]`, `/app/operacao/incidentes`, `/app/operacao/incidentes/[incidentId]`. |
| Objetivo | Ver o trabalho do CRM por jornadas, etapas e casos. |
| Blocos | filtros, colunas/etapas, cards de caso, painel de contexto, timeline, incidentes, bloqueios de dados/integracao. |
| Campos exibidos | caso, tipo, area, objeto, status, etapa, dono, prioridade, prazo, risco, ultima atividade, proxima acao. |
| Acoes | abrir caso, atribuir, mover etapa, pausar fluxo, corrigir dado, reprocessar seguro, resolver, reabrir, escalar. |
| Estados | aberto, aguardando humano, aguardando contato, pendente aprovacao, bloqueado, incidente, resolvido, cancelado. |
| IA/agentes | agentes podem criar caso, sugerir etapa, explicar bloqueio e preparar acao. |
| Cotas | bloqueios/downgrades de agente aparecem no card. |
| Auditoria | mudanca de etapa sensivel, reprocessamento, pausa e resolucao auditam. |
| Fallback | caso sem objeto claro vira tarefa de triagem. |

## Tela web: Tarefas e operacao

| Campo | Definicao |
| --- | --- |
| Tipo | Web e mobile essencial. |
| Rotas | `/app/tarefas`, `/app/tarefas/[taskId]`, `/app/checklists`, `/app/checklists/[runId]`. |
| Objetivo | Organizar trabalho humano por dono, prazo, area e origem. |
| Blocos | minhas tarefas, por fila, atrasadas, sem dono, checklist, detalhe da tarefa, comentarios. |
| Campos exibidos | titulo, status, dono/fila, prazo, origem, caso, objeto afetado, prioridade, comentario recente. |
| Acoes | assumir, delegar, concluir, comentar, reagendar, cancelar, abrir origem, criar subtarefa simples. |
| Estados | aberta, em andamento, aguardando, atrasada, sem dono, concluida, cancelada. |
| IA/agentes | podem criar tarefa e sugerir resumo/proxima acao; nao concluem tarefa humana sem regra. |
| Auditoria | conclusao sensivel e delegacao de casos criticos auditam. |
| Operacao sem agentes | esta e a fila principal do plano Base. |

## Tela web: Aprovacoes

| Campo | Definicao |
| --- | --- |
| Tipo | Web e mobile essencial. |
| Rotas | `/app/aprovacoes`, `/app/aprovacoes/[approvalId]`. |
| Objetivo | Decidir acoes propostas por agente, sistema ou usuario. |
| Blocos | fila, detalhe da proposta, antes/depois, mensagem, impacto, risco, cota, politica usada, historico. |
| Campos exibidos | tipo, solicitante, objeto, proposta, custo/cota, risco, prazo, politica, motivo, status. |
| Acoes | aprovar, editar, rejeitar, pedir mais dados, executar, abrir origem. |
| Estados | pendente, editada, aprovada, rejeitada, expirada, bloqueada por permissao/cota/dado. |
| Permissoes | decisor precisa permissao do objeto e da acao. |
| IA/agentes | preparam proposta e justificativa; decisao humana em itens sensiveis. |
| Auditoria | toda decisao gera evento com antes/depois e ator. |
| Fallback | se faltar dado, vira tarefa/problema de dados. |

## Tela web: Notificacoes

| Campo | Definicao |
| --- | --- |
| Tipo | Web e mobile atalho. |
| Rotas | `/app/notificacoes`. |
| Objetivo | Concentrar alertas sem virar fila duplicada de tarefas. |
| Blocos | novas, urgentes, lidas, por area, por tipo, configuracao de preferencia. |
| Campos exibidos | titulo, area, objeto, prioridade, data, origem, acao recomendada. |
| Acoes | abrir origem, marcar lida, silenciar tipo permitido, priorizar, criar tarefa. |
| Estados | nova, lida, urgente, expirada, sem permissao, origem resolvida. |
| Regra | notificacao acionavel deve apontar origem; se exige trabalho, criar tarefa/caso. |

## Tela web: Checklist do dia

| Campo | Definicao |
| --- | --- |
| Tipo | Web e mobile acao completa. |
| Rotas | `/app/checklists`, `/app/checklists/[runId]`. |
| Objetivo | Garantir abertura/fechamento e rotinas recorrentes. |
| Blocos | checklist de abertura, fechamento, setup, itens pendentes, responsavel, prazo, bloqueios. |
| Acoes | marcar feito, atribuir, comentar, abrir bloqueio, reabrir item, concluir checklist. |
| Estados | incompleto, atrasado, bloqueado, concluido, reaberto. |
| IA/agentes | podem lembrar, detectar pendencia e criar item; nao marcar feito sem evidencia/regra. |
| Auditoria | itens criticos de fechamento podem auditar. |

## Tela web/mobile: Caso operacional

| Campo | Definicao |
| --- | --- |
| Tipo | Web completo; mobile parcial/completo conforme risco. |
| Rotas | `/app/operacao/[caseId]`. |
| Objetivo | Resolver um problema concreto com contexto, dono e proxima acao. |
| Blocos | resumo, objeto afetado, dono, prazo, status, timeline, tarefas, aprovacoes, mensagens, auditoria resumida. |
| Acoes | comentar, atribuir, criar tarefa, pedir aprovacao, resolver, reabrir, escalar, pausar automacao, abrir origem. |
| Estados | aberto, bloqueado, aguardando humano, aguardando contato, incidente, resolvido, reaberto. |
| Permissoes | contexto sensivel fica restrito; acao respeita objeto vinculado. |
| Cotas | mostra se cota causou bloqueio ou downgrade. |
| Auditoria | resolucao, reabertura, escalonamento e acao sensivel. |

Nota: no web, Caso operacional e uma superficie de detalhe dentro de Jornadas e operacao, nao um novo menu principal.

## Telas mobile

### Hoje

| Campo | Definicao |
| --- | --- |
| Profundidade | Acao completa. |
| Conteudo | agenda do dia, prioridades, alertas, tarefas urgentes, aprovacoes, casos bloqueados, cota, agentes pausados. |
| Acoes | abrir item, concluir tarefa, aprovar, assumir, pausar automacao, ir para origem. |
| Estados | sem pendencias, urgente, atrasado, cota 70/90/100, aguardando humano. |

### Checklist do dia

| Campo | Definicao |
| --- | --- |
| Profundidade | Acao completa. |
| Conteudo | abertura, fechamento, itens pendentes, responsavel, prazo. |
| Acoes | marcar feito, atribuir, comentar, abrir bloqueio. |
| Estados | incompleto, atrasado, bloqueado, concluido. |

### Notificacoes

| Campo | Definicao |
| --- | --- |
| Profundidade | Consulta + atalho. |
| Conteudo | alertas operacionais, conversas, aprovacoes, falhas, cotas, riscos. |
| Acoes | abrir origem, marcar lida, priorizar, criar tarefa. |
| Estados | urgente, lida, expirada, sem permissao. |

### Busca global

| Campo | Definicao |
| --- | --- |
| Profundidade | Consulta + acao rapida. |
| Conteudo | alunos, contatos, conversas, aulas, turmas, tarefas, casos, interessados. |
| Acoes | abrir objeto, iniciar conversa quando permitido, criar tarefa. |
| Estados | sem resultado, sem permissao, resultado sensivel restrito. |

### Tarefas

| Campo | Definicao |
| --- | --- |
| Profundidade | Acao completa. |
| Conteudo | minhas tarefas, por prazo, por origem, por caso, atrasadas. |
| Acoes | assumir, concluir, delegar, comentar, reagendar. |
| Estados | atrasada, sem dono, aguardando aluno, concluida. |

### Aprovacoes

| Campo | Definicao |
| --- | --- |
| Profundidade | Acao completa. |
| Conteudo | proposta, antes/depois, impacto, risco, custo/cota, mensagem, solicitante. |
| Acoes | aprovar, editar, rejeitar, pedir mais dados. |
| Estados | pendente, editada, expirada, risco alto, sem permissao. |

### Caso operacional

| Campo | Definicao |
| --- | --- |
| Profundidade | Acao parcial/completa. |
| Conteudo | resumo, dono, prazo, origem, timeline curta, proxima acao. |
| Acoes | comentar, atribuir, resolver, escalar, abrir origem. |
| Estados | bloqueado, aguardando humano, incidente, resolvido. |

### Jornadas prioritarias

| Campo | Definicao |
| --- | --- |
| Profundidade | Consulta + acao. |
| Conteudo | cards de jornada urgentes, etapa, dono, risco, prazo. |
| Acoes | abrir caso, mover etapa simples, assumir, delegar. |
| Estados | risco alto, sem dono, bloqueado. |

### Qualidade de dados

| Campo | Definicao |
| --- | --- |
| Profundidade | Aprovacao/consulta. |
| Conteudo | duplicidade, dado ausente, vinculo incorreto, fluxo bloqueado, objetos afetados. |
| Acoes | corrigir simples, mesclar se seguro, criar tarefa, pedir revisao. |
| Estados | duplicado, incompleto, bloqueando automacao. |

## Priorizacao inicial do Hoje

Ordem recomendada:

1. risco alto ou caso sensivel;
2. aprovacao expirando;
3. aula/chamada do dia bloqueada;
4. conversa aguardando humano;
5. pagamento urgente/comprovante pendente;
6. reposicao/lista de espera com prazo;
7. fluxo bloqueado por dado/cota/integracao;
8. tarefas atrasadas;
9. oportunidades de receita;
10. resumo/gargalos.

## Cobertura de contratos da Rodada 0

| Contrato | Aplicacao nesta rodada |
| --- | --- |
| Dados | Caso, tarefa, aprovacao, notificacao, checklist, objetos de origem. |
| Ciclo de vida | Caso, tarefa, aprovacao, conversa, aula, pagamento e fluxo. |
| Fonte da verdade | Cada card aponta origem; Hoje nao vira fonte primaria. |
| Permissoes | Cards sensiveis respeitam objeto e papel. |
| Botoes | Assumir, delegar, aprovar, rejeitar, resolver, pausar, abrir origem. |
| Estados | Urgente, atrasado, bloqueado, sem dono, cota, sem permissao. |
| Cotas | Downgrade e bloqueios aparecem como trabalho acionavel. |
| Auditoria | Decisoes e mudancas sensiveis auditam. |
| 0 agentes | Tudo vira tarefa/caso/manual quando agente nao existe. |

## Decisoes abertas encontradas

| Tema | Encaminhamento |
| --- | --- |
| Formula de prioridade | Criar v0.2 com pesos por risco, prazo, dinheiro e impacto operacional. |
| Notificacao vs tarefa | Manter regra: notificacao informa; tarefa exige trabalho. Refinar por area nas proximas rodadas. |
| Caso operacional generico demais | Proximas rodadas devem criar tipos de caso por area sem explodir menus. |
| Busca global mobile | Confirmar se fica fixa no topo ou dentro da aba Mais quando desenhar navegacao. |

## Criterio de aceite da rodada

Rodada 2 esta pronta para revisao quando:

- Hoje tem cards acionaveis, nao apenas indicadores;
- toda pendencia importante tem origem e dono/fila;
- notificacao, tarefa, aprovacao e caso nao se confundem;
- mobile resolve tarefas e aprovacoes do dia;
- cota/dado/integracao bloqueada vira caminho manual;
- plano Base continua operavel.
