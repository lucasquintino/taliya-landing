# Matriz Rota X Plano X Agente X Modo - PT-BR

> Status: contrato final v0.2 de produto. Esta versao substitui a matriz v0.1 que ainda citava paginas removidas. Nao cria arquitetura tecnica; define somente como cada superficie se comporta com 0, 1, 3 e 7 agentes.

## Regra De Leitura

- `0 agentes`: CRM completo, sem IA ativa.
- `1 agente`: IA ativa somente se o slot escolhido cobre o dominio da superficie.
- `3 agentes`: bundle recomendado Atendimento + Agenda + Vendas, salvo troca deliberada.
- `7 agentes`: todos os dominios ativos.
- `Manual`: sempre deve existir para caminho critico.
- `Copiloto`: prepara sugestao, resumo, mensagem, prioridade, classificacao ou explicacao.
- `Autonomo`: executa apenas baixo risco e dentro de politica, cota, permissao, auditoria e fallback.
- Rotas antigas removidas devem seguir `agents-flows-final-route-remap.pt-BR.md`.

## Matriz Canonica

| Superficie | Rotas/destino final | Dominio de agente | 0 agentes | 1 agente | 3 agentes | 7 agentes | Manual | Copiloto | Autonomo | Bloqueio/cota/auditoria |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Conta basica pre-assinatura | Criar conta com Google, Microsoft ou e-mail com link seguro; entrar com Google, Microsoft ou e-mail/senha; antes do CRM | Gestao/Governanca | Conta criada, CRM bloqueado. | Igual, sem agente ate assinatura. | Igual. | Igual. | Criar conta, entrar, sair. | Nao. | Nao. | Sem acesso ao CRM antes da assinatura confirmada. |
| Assinatura Taliya | `/app/billing` depois do login; checkout externo do provedor antes da liberacao | Gestao/Governanca | Plano Base/billing manual. | 1 slot. | 3 slots. | 7 slots. | Ver plano, trocar, portal, pacote. | Explica plano/limite. | Nao. | Billing confiavel decide entitlement. |
| Onboarding e configuracao inicial | `/onboarding/*` | Gestao/Governanca | Setup manual/programatico. | Configura 1 slot. | Configura 3 slots. | Configura 7 slots. | Completo. | Sugere preset se agente ativo. | Nao. | Claim, importacao e agente auditados. |
| Hoje | `/app/hoje` | Gestao/Governanca + dominios ativos | Prioridade programatica. | Sugere nos cards do agente ativo. | Sugere Atendimento/Agenda/Vendas. | Sugere todos os dominios. | Abrir, delegar, aprovar, pausar. | Prioriza, resume e explica. | So tarefas/lembretes seguros. | Cota 70/90/100 e auditoria em acao sensivel. |
| Inbox e conversas | `/app/inbox`, conversa/drawer contextual | Atendimento | Manual. | IA se slot = Atendimento. | Ativo no bundle padrao. | Ativo. | Responder, assumir, tarefa, opt-out. | Resumo, rascunho, classificacao. | Resposta segura permitida. | Identidade, opt-out, cota e envio auditado. |
| Identidade, contatos e consentimentos | Contextual em Inbox, Alunos, Interessados e Aprovacoes | Atendimento | Manual. | IA se Atendimento. | Ativo no bundle padrao. | Ativo. | Editar, validar, vincular, opt-out. | Sugere duplicidade/vinculo operacional. | Nao para vinculo sensivel. | Sem pagina Contatos; telefone compartilhado e dado sensivel exigem confirmacao. |
| Qualidade de dados | Contextual em Onboarding/importacao, Hoje, Tarefas, Aprovacoes e origem do erro | Gestao/Governanca | Fila manual/contextual. | IA se Gestao ou dominio afetado. | Parcial se afeta dominios ativos. | Ativo. | Corrigir, mesclar, revisar. | Sugere merge/correcao. | Nao em merge sensivel. | Sem pagina Qualidade; saneamento sensivel auditado. |
| Alunos e perfil | `/app/alunos`, `/app/alunos/[id]` | Historico/Professor + dominios relacionados | Manual. | IA se slot relacionado. | Parcial por Atendimento/Agenda/Vendas. | Ativo. | Conversar, tarefa, agendar, nota. | Resume contexto permitido. | Nao. | Historico sensivel protegido. |
| Historico do aluno | Aba/timeline no perfil do aluno e contexto de aula | Historico/Professor | Manual restrito. | IA se Historico/Professor. | Bloqueado salvo troca de slot. | Ativo. | Nota, anexo, correcao. | Resumo permitido. | Nao. | Sem pagina Historico; dado sensivel bruto bloqueado. |
| Professor e notas | Contextual em Aula, Chamada, Turmas, Agenda e Perfil | Historico/Professor | Manual. | IA se Historico/Professor. | Bloqueado salvo troca. | Ativo. | Nota, handoff, lembrete. | Sugere nota/handoff. | Lembrete seguro. | Sem pagina Professor; professor nao ve financeiro/conversa completa. |
| Agenda | `/app/agenda` | Agenda | Programatico/manual. | IA se Agenda. | Ativo no bundle padrao. | Ativo. | Criar/alterar aula, conflito. | Explica conflito e sugere acao. | Lembrete seguro. | Mudanca de agenda auditada. |
| Grade, turmas e eventos | `/app/grade`, `/app/turmas`; eventos contextuais em Agenda/Turmas/Aula | Agenda | Manual/programatico. | IA se Agenda. | Ativo no bundle padrao. | Ativo. | Criar turma, ajustar grade, evento contextual. | Simular impacto. | Nao em mudanca estrutural. | Mudanca estrutural exige auditoria. |
| Aula e chamada | `/app/aulas/[id]`; chamada dentro da aula | Agenda + Historico/Professor | Manual completo. | IA se Agenda ou Historico. | Agenda ativo; historico bloqueado salvo troca. | Ativo. | Chamada, falta, nota. | Sugere reposicao/nota. | Lembrete seguro. | Correcao de chamada auditada. |
| Reposicoes e creditos | `/app/reposicoes` | Agenda | Encaixe programatico. | IA se Agenda. | Ativo no bundle padrao. | Ativo. | Encontrar encaixe, reservar, convidar. | Redige/explica convite. | Convite seguro permitido. | Cota, consentimento e regra de reposicao. |
| Lista de espera geral | Contextual em Vendas/Interessados, Agenda/Turmas, Hoje/Tarefas | Agenda + Vendas | Manual/contextual. | IA se Agenda ou Vendas. | Ativo no bundle padrao. | Ativo. | Registrar interesse, avisar vaga, criar tarefa. | Sugere prioridade/mensagem. | Convite seguro se regra clara. | Sem pagina propria; prioridade e opt-out auditados. |
| Interessados e vendas | `/app/vendas`, `/app/interessados` | Vendas | Manual/programatico. | IA se Vendas. | Ativo no bundle padrao. | Ativo. | Cadastrar, qualificar, follow-up. | Rascunho e objecao. | Follow-up seguro. | Opt-out e limite de cadencia. |
| Aulas experimentais | `/app/aulas-experimentais` | Vendas + Agenda | Manual/programatico. | IA se Vendas/Agenda. | Ativo no bundle padrao. | Ativo. | Agendar, lembrar, remarcar. | Pos-aula e lembrete. | Lembrete seguro. | Cota e opt-out. |
| Matriculas | `/app/matriculas` | Vendas | Manual. | IA se Vendas. | Ativo no bundle padrao. | Ativo. | Validar, converter, tarefa. | Checklist e rascunho. | Nao converter sensivel. | Sem checkout de alunos proprio; contrato/pagamento auditados. |
| Vendas e origens | Contextual em Vendas, Interessados e Relatorios | Vendas | Manual/relatorio. | IA se Vendas. | Ativo no bundle padrao. | Ativo. | Revisar origem, indicacao, captura. | Explica origem. | Nao. | Sem autonomia sensivel. |
| Financeiro | `/app/financeiro` | Financeiro | Manual/programatico. | IA se Financeiro. | Bloqueado salvo troca. | Ativo. | Abrir cobranca, ver fila, exportar. | Rascunho/analise. | So lembrete seguro. | Permissao financeira e auditoria. |
| Financeiro - kanban | `/app/financeiro/kanban` | Financeiro | Manual/programatico. | IA se Financeiro. | Bloqueado salvo troca. | Ativo. | Mover etapa, lembrar, registrar promessa. | Prioriza e redige cobranca. | Lembrete simples permitido. | Disputa/acordo humano. |
| Financeiro - movimentacoes | `/app/financeiro/movimentacoes` | Financeiro | Manual/programatico. | IA se Financeiro. | Bloqueado salvo troca. | Ativo. | Lembrar, link, confirmar, conciliar, filtrar. | Rascunho de cobranca e resumo. | Lembrete simples permitido. | Confirmacao exige evidencia; disputa/acordo humano. |
| Excecoes financeiras sensiveis | Financeiro, Aprovacoes, Tarefas, Aluno e Operacao | Financeiro | Manual com aprovacao/tarefa contextual. | IA se Financeiro, copiloto apenas. | Bloqueado salvo troca. | Copiloto ativo. | Simular, aprovar, rejeitar, criar tarefa. | Explica impacto. | Nao. | Autonomia bloqueada; auditoria obrigatoria. |
| Contratos e documentos financeiros | Contextual em Financeiro, Matriculas, Aluno e anexos/detalhes | Financeiro | Manual. | IA se Financeiro. | Bloqueado salvo troca. | Ativo. | Ver, reenviar, anexar, baixar quando permitido. | Checklist/status. | Nao em assinatura/status sensivel. | Sem pagina propria; documento auditado. |
| Retencao | `/app/retencao` | Retencao | Score programatico. | IA se Retencao. | Bloqueado salvo troca. | Ativo. | Tarefa, mensagem, caso. | Sugere abordagem. | Contato seguro permitido. | Risco explicavel e cota. |
| Cancelamentos e reativacao | `/app/cancelamentos`, `/app/retencao/reativacoes` | Retencao | Manual. | IA se Retencao, copiloto. | Bloqueado salvo troca. | Copiloto ativo. | Registrar, plano, converter pausa, reservar vaga com validacao, reativar. | Rascunho/plano/oportunidade. | Nao em cancelamento ativo; nao se `nao contatar`. | Automacao pausada e decisao humana. |
| Reclamacoes e casos sensiveis | `/app/reclamacoes`, detalhe contextual | Retencao | Manual. | IA se Retencao, copiloto. | Bloqueado salvo troca. | Copiloto ativo. | Classificar, escalar, responder com revisao, resolver com confirmacao. | Sugere resposta e organiza contexto. | Nao em alta severidade. | Severidade, dono, automacao pausada e auditoria. |
| Jornadas e operacao | `/app/operacao`, caso/detalhe contextual | Gestao/Governanca | Manual/programatico. | IA se Gestao ou dominio do caso. | Parcial por dominios ativos. | Ativo. | Abrir, atribuir, mover. | Prioriza e resume. | Tarefa segura. | Caso/fluxo auditado. |
| Tarefas e checklists | `/app/tarefas`, `/app/checklists` | Gestao/Governanca | Manual. | IA se Gestao ou dominio. | Parcial. | Ativo. | Assumir, concluir, delegar. | Sugere prioridade. | Criar tarefa segura. | Auditoria leve. |
| Aprovacoes | `/app/aprovacoes` | Todos os dominios | Manual. | IA se dominio ativo. | Parcial. | Ativo. | Aprovar, editar, rejeitar. | Explica antes/depois. | Nao aprova sozinha. | Auditoria obrigatoria. |
| Agentes e fluxos | `/app/agentes`, `/app/fluxos` | Gestao/Governanca | Preview/bloqueado. | Configura 1 slot. | Configura 3 slots. | Configura 7 slots. | Ativar, pausar, simular. | Sugere configuracao. | Fluxos seguros. | Entitlement, cota e auditoria. |
| Execucoes e incidentes de agentes | `/app/fluxos/execucoes/[runId]`; incidentes contextuais em Operacao/Suporte | Gestao/Governanca | Sem execucoes reais. | Execucoes do slot ativo. | Execucoes dos 3 slots. | Todas. | Corrigir, pausar, abrir suporte. | Explica falha. | Reprocessar seguro. | Idempotencia e auditoria. |
| Uso, cotas e economia | `/app/uso` | Gestao/Governanca | Uso IA zerado. | Cota do slot ativo. | Cota dos slots ativos. | Cota completa. | Pausar baixa prioridade, pacote. | Sugere economia. | Nao. | Eventos de uso idempotentes. |
| Relatorios e Dinheiro na Mesa | `/app/relatorios`, `/app/dinheiro-na-mesa` | Gestao/Governanca | Relatorios normais. | Agente ativo entra em relatorio. | 3 agentes em relatorio. | Todos. | Filtrar, exportar localmente. | Explica tendencia. | Nao exporta sozinho. | Exportacao local auditada quando sensivel. |
| Configuracoes | `/app/configuracoes/*` | Gestao/Governanca | Manual. | Configura slot ativo e CRM. | Configura 3 slots e CRM. | Configura todos. | Editar, testar, salvar. | Sugere impacto. | Nao em permissao/regra sensivel. | Auditoria forte. |
| Politicas operacionais | Configuracoes por area, Agentes/Fluxos e Aprovacoes | Gestao/Governanca | Manual. | Politicas do slot/area ativa. | Politicas dos dominios ativos. | Todas. | Versionar, simular, publicar quando permitido. | Simula impacto. | Nao publica sozinha. | Sem pagina propria; versionamento auditado. |
| Recursos, feriados e disponibilidade | `/app/configuracoes/agenda` | Agenda | Manual/programatico. | IA se Agenda. | Ativo no bundle padrao. | Ativo. | Bloquear, simular, avisar. | Explica impacto. | Aviso seguro aprovado. | Sem pagina propria; mudanca auditada. |
| Segmentos e comunicados | Pos-MVP; filtros contextuais em Vendas/Retencao/Relatorios quando necessario | Vendas + Retencao | Manual/contextual limitado. | IA se Vendas/Retencao no contexto. | Vendas ativo; Retencao salvo troca. | Ativo no contexto. | Filtrar, validar, aprovar acao local. | Sugere publico/texto contextual. | Envio livre nao entra no MVP. | Sem paginas proprias; consentimento e cota. |
| Integracoes | Configuracoes de canal, pagamentos, agenda, importacao e notificacoes | Gestao/Governanca | Manual/config. | IA se Gestao. | Parcial. | Ativo. | Conectar, testar, reprocessar. | Explica falha. | Reprocessar seguro. | Sem hub proprio; logs e idempotencia. |
| Auditoria | Trilha contextual em telas, aprovacoes, execucoes, suporte e backoffice interno | Gestao/Governanca | Completa/contextual. | Completa + eventos do slot. | Eventos dos 3 slots. | Todos. | Abrir trilha, filtrar localmente, exportar onde permitido. | Resumo permitido. | Nao. | Sem pagina propria para studio; acesso restrito. |
| Privacidade e solicitacoes | Termos/consentimentos contextuais, Aprovacoes e Suporte | Gestao/Governanca | Manual. | IA bloqueada salvo resumo permitido. | Bloqueada salvo resumo. | Copiloto restrito. | Validar, aprovar, executar quando aplicavel. | Checklist/rascunho. | Nao. | LGPD e grants auditados; sem pagina propria para studio. |
| Suporte | `/app/suporte` via topbar global | Suporte/Taliya | Abrir chamado/manual. | Pode anexar contexto do agente ativo. | Pode anexar contexto dos 3 slots. | Contexto completo permitido por permissao. | Chamado, conversa, anexos, status. | Resume incidente e sugere categoria. | Nao resolve acao sensivel sozinho. | Suporte nao atende alunos; acesso e grants auditados. |

## Regras De Bloqueio Por Plano

| Situacao | Comportamento |
| --- | --- |
| Acao pertence a agente nao incluso | Mostrar bloqueado por plano, explicar agente necessario e oferecer caminho manual. |
| Agente incluso mas nao configurado | Mostrar configurar/testar, manter caminho manual. |
| Agente pausado | Mostrar motivo, retomar se permitido, manter caminho manual. |
| Cota 100% | Bloquear automacao paga, manter manual e pacote/upgrade. |
| Acao sensivel | Mesmo com agente incluso, exigir permissao, confirmacao e auditoria. |
| Assinatura Taliya nao confirmada | Bloquear CRM e mostrar estado de assinatura pendente/erro, com acesso apenas a conta/billing/suporte quando aplicavel. |

## Aceite

Uma superficie esta pronta quando deixa claro:

- o que acontece no plano Base;
- qual agente cobre a acao;
- o que muda com 1, 3 e 7 agentes;
- qual modo esta disponivel;
- o que fica bloqueado por plano, cota, permissao ou risco;
- qual caminho manual continua disponivel;
- se o destino e pagina propria, contexto, topbar global ou pos-MVP.
