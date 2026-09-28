# Design System Web - Rodada 4.0 - Blueprint De Todas As Paginas

> Status: blueprint v0.1 para geracao das paginas web finais. Este documento define o layout exato por superficie, quais componentes entram em cada zona e como as funcionalidades devem ser agrupadas.

## Objetivo

Transformar o mapa funcional do CRM web em blueprint de tela.

Este documento responde, para cada pagina/superficie:

- qual layout usar;
- o que fica no topo;
- o que fica na coluna esquerda;
- o que fica no centro;
- o que fica no painel direito;
- o que fica em rodape, drawer ou modal;
- quais componentes aprovados entram;
- quais estados e regras de agente/plano/cota precisam aparecer.

## Fontes

Usar em conjunto com:

- `final-screen-contract-matrix.pt-BR.md`;
- `web-screen-map.pt-BR.md`;
- `page-layout-zones.pt-BR.md`;
- `page-case-coverage.pt-BR.csv`;
- `screen-ux-depth-contract.pt-BR.md`;
- `route-agent-mode-entitlement-matrix.pt-BR.md`;
- `design-system-route-functionality-coverage-post-3c.pt-BR.md`;
- Rodadas de design system 1, 2B, 3A, 3B e 3C.

## Regra Global De Layout

Todas as paginas web usam o App Shell Web aprovado:

- sidebar compacta fixa;
- topbar leve;
- titulo de pagina alinhado a esquerda;
- area principal com fundo cinza frio;
- paineis suaves/translucidos;
- painel direito quando houver item selecionado;
- drawers/modais para edicao, detalhe longo e confirmacao.

## Zonas Padrao

| Zona | Papel |
| --- | --- |
| Topo | Titulo, busca, filtros essenciais, periodo, status e acao primaria. |
| Esquerda | Filtros, segmentos, filas, etapas, mini calendario ou navegacao interna. |
| Centro | Superficie principal: jornada, tabela, lista, calendario, pipeline, perfil ou builder. |
| Direita | Contexto do item selecionado, resumo, risco, sugestao, cota, permissao e acoes. |
| Inferior | Apoio secundario: atividade, graficos, historico curto ou itens relacionados. |
| Drawer | Edicao contextual, formulario, detalhes longos, logs, anexos e configuracao. |
| Modal | Confirmacao, acao sensivel, erro bloqueante, publish/preflight e aprovacao curta. |

## Componentes Base Por Referencia

| Codigo | Fonte | Componentes |
| --- | --- | --- |
| `2B` | App Shell | sidebar, topbar, titulo, canvas, painel direito. |
| `3A` | Referencia | botoes circulares, nav pill, cards, avatares, badges, conectores, tabela leve. |
| `3B.1` | Inputs | inputs, selects, textarea, chips, busca, filtros, formulario compacto. |
| `3B.2` | Feedback | modal, drawer, popover, tooltip, toast, empty, loading, error. |
| `3B.3` | Operacional | tabela completa, lista densa, kanban, calendario compacto, timeline, atividade. |
| `3B.4` | Comunicacao/agentes | inbox, conversa, composer, copiloto, aprovacao, handoff, confianca. |
| `3B.5` | Sistema | plano, cota, permissao, billing, integracao, auditoria, politica. |
| `3C.1` | Objetos/dados | wizard, importacao, duplicidade, perfil, relacoes, consentimento, timeline sensivel. |
| `3C.2` | Agenda/financeiro | calendario semanal, aula, turma, chamada, reposicao, documentos, conciliacao. |
| `3C.3` | Agentes/auditoria | flow builder, simulador, preflight, trace, incidente, diff, LGPD, relatorios. |

## Regras De Propriedade De Pagina

Algumas rotas aparecem como contexto em mais de uma superficie. Para evitar duplicidade ao gerar as paginas:

- `/app/recursos` pertence a **Recursos, Feriados E Disponibilidade**; em Grade/Turmas/Eventos, recurso aparece apenas como filtro, aviso de conflito e impacto.
- `/app/importacao` pertence a **Integracoes** depois do setup; no Onboarding, importacao aparece apenas como etapa inicial guiada.
- `/app/segmentos` e `/app/comunicados` pertencem a **Segmentos E Comunicados**; vendas, retencao e agenda apenas abrem essa superficie com filtros pre-aplicados.
- `/app/aprovacoes`, `/app/tarefas`, `/app/auditoria`, `/app/uso` e `/app/privacidade/*` sao superficies operacionais proprias, mesmo quando acionadas a partir de outra pagina.
- Drawers e modais nao viram paginas novas, exceto quando a rota ja estiver listada neste blueprint.

## Blueprints Por Pagina

### 1. Onboarding E Configuracao Inicial

| Item | Blueprint |
| --- | --- |
| Rotas | `/onboarding/claim/[activationId]`, `/onboarding/studio`, `/onboarding/importacao`, `/onboarding/agentes`, `/onboarding/revisao` |
| Layout | Wizard full-page dentro de shell leve, sem sidebar operacional ate abrir CRM. |
| Topo | Logo Taliya, progresso geral, status da conta, acao "Continuar depois" quando permitido. |
| Esquerda | Stepper/checklist de ativacao com etapas: conta, studio, importacao, equipe, agentes, revisao. |
| Centro | Formulario da etapa atual; importacao e mapeamento quando aplicavel. |
| Direita | Ajuda contextual, impacto do que falta, bloqueios e preview do que sera ativado. |
| Drawers/modais | Resolver duplicidade, mapear campo, convidar equipe, testar canal/agente, confirmar abrir CRM. |
| Componentes | `3C.1` wizard, checklist, importacao, mapeamento, duplicidade; `3B.1` forms; `3B.2` modal. |
| Estados | incompleto, bloqueado por dado, importando, duplicidade, erro, pronto. |
| IA/plano/cota | Sem agentes ativos por padrao; se houver plano com agentes, mostrar slots a configurar e caminho manual. |

### 2. Hoje

| Item | Blueprint |
| --- | --- |
| Rotas | `/app`, `/app/hoje` |
| Layout | Central diaria composta por subcontainers de trabalho do dia; detalhe abre em drawer lateral sob demanda. |
| Topo | Data, busca global, filtro por prioridade, indicador de cota, status de agentes, acao "Criar tarefa". |
| Esquerda | Coluna estreita com checklist do dia e proximas aulas; pode recolher em telas mais densas. |
| Centro | Subcontainers grandes por bloco acionavel: agora, proximas aulas, fila humana, tarefas de hoje, bloqueios, dinheiro e aprovacoes. |
| Direita | Sem painel direito fixo na primeira dobra; espaco pertence as prioridades. |
| Inferior | Gargalos de hoje, fila humana, bloqueios do dia, dinheiro que exige acao hoje; links discretos para Agenda ou Relatorios quando a analise nao for do dia. |
| Drawers/modais | Drawer lateral para detalhe da prioridade, vindo da esquerda ou sobre o canvas; aprovar acao, pausar automacao, resolver cota, abrir origem. |
| Componentes | `3A` cards; `3B.2` alerts; `3B.3` atividade/cards resumo; `3B.4` aprovacao; `3B.5` cota. |
| Estados | sem pendencia, urgente, critico, cota 70/90/100, bloqueado, aguardando humano. |
| IA/plano/cota | Sempre mostrar caminho manual; copiloto explica prioridade; autonomo apenas tarefa/lembrete seguro. |

### 3. Inbox E Conversas

| Item | Blueprint |
| --- | --- |
| Rotas | `/app/inbox`, `/app/conversas/[id]`, `/app/envios`, `/app/envios/[sendId]` |
| Layout | Tres colunas: lista de conversas, conversa selecionada, painel de contexto. |
| Topo | Busca, canal, status, responsavel, filtro de nao lidas, nova conversa/manual. |
| Esquerda | Inbox com tabs: todos, WhatsApp, email, interno, arquivados; lista por prioridade. |
| Centro | Conversa selecionada, mensagens, nota interna, sugestao do copiloto e composer. |
| Direita | Perfil vinculado, consentimento, resumo, tarefas, historico curto, confianca do agente. |
| Drawers/modais | Assumir do agente, editar sugestao, registrar opt-out, anexos, falha de envio, handoff. |
| Componentes | `3B.4` inbox/conversa/composer/copiloto; `3C.1` perfil/consentimento; `3C.2` anexo/upload; `3B.2` error/confirmacao. |
| Estados | novo, aguardando humano, agente respondendo, agente pausado, opt-out, falha de envio, sem permissao. |
| IA/plano/cota | Atendimento ativo se plano cobre; mostrar sugestao, cota e assumir manualmente. |

### 4. Contatos E Qualidade De Identidade

| Item | Blueprint |
| --- | --- |
| Rotas | `/app/contatos`, `/app/contatos/[id]` |
| Layout | Lista + detalhe em painel direito para contatos simples, incompletos ou duplicados. |
| Topo | Busca, filtros de tipo, origem, duplicidade e acao "Novo contato". |
| Esquerda | Segmentos: todos, alunos, interessados, conversas, duplicados, incompletos. |
| Centro | Lista densa de contatos com status, origem, telefone/e-mail e ultimo evento. |
| Direita | Perfil simples do contato, dados principais, origem, conflito de dados e acoes. |
| Drawers/modais | Editar contato, converter em aluno/interessado, resolver duplicidade, mesclar, arquivar. |
| Componentes | `3C.1` perfil, duplicidade, mapeamento; `3B.3` lista; `3B.1` forms. |
| Estados | duplicado, opt-out, dado incompleto, convertido, arquivado. |
| IA/plano/cota | Copiloto pode sugerir normalizacao; merge sensivel exige revisao humana e auditoria. |

### 5. Qualidade De Dados

| Item | Blueprint |
| --- | --- |
| Rotas | `/app/dados/qualidade`, `/app/dados/duplicidades` |
| Layout | Fila de saneamento com comparador e painel de impacto. |
| Topo | Tipo de problema, impacto operacional, filtro por objeto, responsavel e status. |
| Esquerda | Filas: duplicidades, ausentes, conflitos, bloqueios, arquivados. |
| Centro | Tabela/lista de problemas com severidade, objeto, acao sugerida e origem. |
| Direita | Antes/depois, campos afetados, fluxos bloqueados, sugestao e risco. |
| Drawers/modais | Mesclar registros, corrigir campo, manter separado, arquivar, pedir revisao. |
| Componentes | `3C.1` fila conflitos, duplicidade, mapeamento; `3C.3` diff; `3B.2` confirmacao. |
| Estados | incompleto, conflito, bloqueando, resolvido, aguardando revisao. |
| IA/plano/cota | Copiloto sugere correcao; sistema nao mescla dado sensivel sozinho. |

### 6. Alunos E Perfil Do Aluno

| Item | Blueprint |
| --- | --- |
| Rotas | `/app/alunos`, `/app/alunos/[id]` |
| Layout | Lista de alunos + workspace de perfil com abas e painel direito. |
| Topo | Busca, status, plano, risco, filtros, acao "Novo aluno" ou "Criar tarefa". |
| Esquerda | Segmentos: ativos, pausados, inadimplentes, risco, reposicao, sem proxima aula. |
| Centro | Perfil com cabecalho, abas resumo/agenda/financeiro/historico/documentos/tarefas. |
| Direita | Proximas acoes, conversa, risco, pagamentos, notas e historico curto. |
| Drawers/modais | Editar perfil, registrar nota, alterar plano, criar tarefa, atualizar dados. |
| Componentes | `3C.1` perfil/abas/timeline; `3C.2` agenda/documentos; `3B.4` conversa; `3B.3` atividade. |
| Estados | ativo, pausado, inadimplente, risco, sem turma, experimental, inativo. |
| IA/plano/cota | Resumo permitido se agente cobre; IA nao altera dados sensiveis sozinha. |

### 7. Historico Do Aluno

| Item | Blueprint |
| --- | --- |
| Rotas | `/app/alunos/[id]/linha-do-tempo`, `/app/historico`, `/app/historico/documentos` |
| Layout | Linha do tempo operacional com filtros e detalhe lateral. |
| Topo | Aluno, periodo, tipo de registro, origem e acao "Adicionar nota". |
| Esquerda | Tipos: notas, aulas, mensagens, pagamentos, documentos, tarefas e alteracoes. |
| Centro | Timeline com eventos operacionais, origem, autor e horario. |
| Direita | Detalhe do registro, anexos, origem, acao relacionada e auditoria curta. |
| Drawers/modais | Adicionar nota, anexar documento, corrigir registro, abrir origem. |
| Componentes | `3C.1` timeline; `3C.2` viewer/anexo; `3C.3` log/diff; `3B.2` modal. |
| Estados | comum, restrito por permissao, pendente, corrigido, arquivado. |
| IA/plano/cota | IA so resume contexto permitido; alteracoes sensiveis continuam auditadas. |

### 8. Professor E Notas

| Item | Blueprint |
| --- | --- |
| Rotas | `/app/professores`, `/app/professores/[teacherId]` |
| Layout | Agenda do professor + alunos da aula + notas pendentes. |
| Topo | Professor, dia, aulas, filtro por turma e status de notas. |
| Esquerda | Lista de aulas do professor e pendencias. |
| Centro | Cards de alunos da aula com contexto permitido e acoes de nota/handoff. |
| Direita | Detalhe do aluno, ultima nota permitida, lembrete, handoff e restricoes. |
| Drawers/modais | Registrar nota, criar handoff, marcar lembrete, pedir contexto adicional. |
| Componentes | `3C.2` aula; `3C.1` perfil/timeline; `3B.3` lista; `3B.4` handoff. |
| Estados | nota pendente, contexto restrito, aula sem chamada, sem permissao. |
| IA/plano/cota | Copiloto pode sugerir nota/handoff se permitido; professor nao ve financeiro/conversa completa. |

### 9. Agenda

| Item | Blueprint |
| --- | --- |
| Rotas | `/app/agenda` |
| Layout | Calendario operacional com painel de aula selecionada. |
| Topo | Dia/semana/mes, professor, turma, status, filtros e acao "Criar aula". |
| Esquerda | Mini calendario, filtros de professor/turma/sala/status. |
| Centro | Calendario semanal ou diario com aulas, conflitos, capacidade e vagas. |
| Direita | Aula selecionada: alunos, capacidade, chamada, conflitos, reposicoes e acoes. |
| Drawers/modais | Criar/editar aula, ver conflito, reservar vaga, avisar envolvidos. |
| Componentes | `3C.2` calendario semanal/card aula/conflito; `3B.1` filtros; `3B.2` drawer. |
| Estados | lotado, vaga aberta, conflito, feriado, professor/sala indisponivel. |
| IA/plano/cota | Encaixe/conflito programatico; IA explica ou redige convite se agente de agenda ativo. |

### 10. Grade, Turmas E Eventos

| Item | Blueprint |
| --- | --- |
| Rotas | `/app/grade`, `/app/turmas`, `/app/turmas/[id]`, `/app/eventos`, `/app/eventos/[eventId]` |
| Layout | Grade/turmas com calendario e painel de impacto. |
| Topo | Periodo, unidade, professor, recurso, acao "Criar turma/evento". |
| Esquerda | Lista de turmas, professores, recursos e eventos. |
| Centro | Grade semanal editavel com capacidade, horarios, eventos e indisponibilidades. |
| Direita | Impacto da mudanca, simulacao, alunos afetados, avisos necessarios. |
| Drawers/modais | Criar turma, editar horario, criar evento, abrir recurso relacionado, simular impacto. |
| Componentes | `3C.2` grade/turma/conflito; `3B.1` forms; `3C.3` diff; `3B.2` confirmacao. |
| Estados | capacidade excedida, recurso indisponivel, recesso, impacto pendente. |
| IA/plano/cota | Mudanca estrutural exige auditoria; IA apenas simula/explica quando permitido. |

### 11. Aula E Chamada

| Item | Blueprint |
| --- | --- |
| Rotas | `/app/aulas/[id]`, `/app/aulas/[id]/chamada` |
| Layout | Tela de execucao da aula com roster no centro. |
| Topo | Aula, horario, turma, professor, sala, status da chamada. |
| Esquerda | Alunos esperados e filtros: presentes, faltas, no-show, pendentes. |
| Centro | Roster de chamada com marcadores de presenca/falta/no-show/observacao. |
| Direita | Contexto do aluno selecionado, consequencias, credito de reposicao, historico permitido. |
| Drawers/modais | Corrigir chamada, registrar falta, criar reposicao, adicionar observacao. |
| Componentes | `3C.2` roster/card aula/reposicao; `3C.1` perfil/timeline; `3B.2` confirmacao. |
| Estados | chamada pendente, falta avisada, no-show, credito criado, correcao auditada. |
| IA/plano/cota | IA pode sugerir observacao/acao; chamada e correcao sao humanas/auditadas. |

### 12. Reposicoes E Lista De Espera

| Item | Blueprint |
| --- | --- |
| Rotas | `/app/reposicoes`, `/app/creditos-reposicao`, `/app/lista-espera` |
| Layout | Fila de pedidos + matcher de encaixe + convite. |
| Topo | Vagas, creditos, periodo, prioridade, filtro por turma/horario. |
| Esquerda | Filtros por credito, validade, disponibilidade, prioridade e status de convite. |
| Centro | Lista de pedidos, creditos e vagas disponiveis. |
| Direita | Matcher com candidatos, melhor encaixe, conflitos, convite e custo/cota. |
| Drawers/modais | Reservar vaga, convidar aluno, consumir credito, expirar credito, ver conflito. |
| Componentes | `3C.2` matcher/lista espera/conflito; `3B.4` mensagem; `3B.2` confirmacao. |
| Estados | sem vaga, conflito, aguardando resposta, credito vencido, convite falhou. |
| IA/plano/cota | Encontrar encaixe e programatico; IA redige/explica convite se agente ativo. |

### 13. Interessados E Vendas

| Item | Blueprint |
| --- | --- |
| Rotas | `/app/vendas`, `/app/interessados`, `/app/interessados/novo`, `/app/interessados/[id]` |
| Layout | Pipeline + painel do interessado. |
| Topo | Busca, etapa, origem, temperatura, filtro por proxima acao, novo interessado. |
| Esquerda | Etapas do funil, origem, segmentos e filtros rapidos. |
| Centro | Kanban/pipeline com cards de interessados e proxima acao. |
| Direita | Perfil do lead, conversa, objecoes, experimental, tarefas e sugestao. |
| Drawers/modais | Cadastrar/editar lead, qualificar, marcar perdido, converter, criar follow-up. |
| Componentes | `3B.3` kanban/lista; `3C.1` perfil; `3B.4` conversa/copiloto; `3B.1` forms. |
| Estados | novo, quente, sem resposta, sem vaga, perdido, opt-out. |
| IA/plano/cota | Vendas ativo gera rascunho/objecao/follow-up; autonomia respeita opt-out e cadencia. |

### 14. Aulas Experimentais

| Item | Blueprint |
| --- | --- |
| Rotas | `/app/experimental` |
| Layout | Agenda comercial + fila de pos-aula. |
| Topo | Dia, status, professor, origem, acao "Agendar experimental". |
| Esquerda | Status: agendada, lembrete, faltou, pos-aula, converter. |
| Centro | Agenda/lista de experimentais com professor, horario e status. |
| Direita | Detalhe do interessado, conversa, lembrete, pos-aula e conversao. |
| Drawers/modais | Agendar, remarcar, registrar falta, enviar lembrete, converter. |
| Componentes | `3C.2` aula/calendario; `3B.4` conversa; `3B.3` lista; `3B.2` confirmacao. |
| Estados | agendada, lembrete enviado, faltou, concluiu, converter agora. |
| IA/plano/cota | Lembrete seguro e pos-aula se Vendas/Agenda ativo; conversao sensivel revisada. |

### 15. Matriculas

| Item | Blueprint |
| --- | --- |
| Rotas | `/app/matriculas`, `/app/checkout-alunos` |
| Layout | Checklist de conversao com documentos e pagamento. |
| Topo | Status da pre-matricula, pendencias, plano escolhido, acao "Validar". |
| Esquerda | Checklist: dados, plano, contrato, pagamento, primeira aula. |
| Centro | Lista de matriculas em andamento ou detalhe da matricula selecionada. |
| Direita | Pendencias, documento, pagamento, primeira aula e tarefas geradas. |
| Drawers/modais | Validar dados, escolher plano, enviar contrato, anexar pagamento, converter aluno. |
| Componentes | `3C.1` checklist/perfil; `3C.2` documento/pagamento; `3B.2` confirmacao. |
| Estados | faltando dado, aguardando pagamento, contrato pendente, pronto para aluno. |
| IA/plano/cota | Copiloto pode checklist/rascunho; conversao e contrato seguem auditados. |

### 16. Vendas E Origens

| Item | Blueprint |
| --- | --- |
| Rotas | `/app/vendas/captura`, `/app/vendas/origens`, `/app/indicacoes`, `/app/vendas/perdidos` |
| Layout | Relatorio acionavel com origem, indicacao e demanda. |
| Topo | Periodo, origem, conversao, acao "Criar segmento". |
| Esquerda | Origens, campanhas, indicacoes, perdidos, demanda sem vaga. |
| Centro | Graficos, ranking e tabela de origens/indicacoes. |
| Direita | Detalhe da origem, leads relacionados, acao recomendada e segmento. |
| Drawers/modais | Revisar origem, criar segmento, abrir lista de espera, marcar origem ruim. |
| Componentes | `3C.3` relatorios/segmentos; `3B.3` tabela/ranking; `3B.1` filtros. |
| Estados | origem ruim, campanha sem dono, demanda reprimida, sem dados. |
| IA/plano/cota | Copiloto explica origem; envio/comunicado exige consentimento e aprovacao. |

### 17. Financeiro

| Item | Blueprint |
| --- | --- |
| Rotas | `/app/financeiro` |
| Layout | Visao geral financeira + filas principais de acao. Nao e tabela completa nem kanban. |
| Topo | Periodo, unidade, recebido, previsto, vencido, em atraso, conciliacao pendente, filtros e exportar quando permitido. |
| Esquerda | Filas principais: vencem hoje, atrasados, comprovantes pendentes, falhas, promessas e excecoes. |
| Centro | KPIs financeiros, prioridades financeiras e lista curta de itens que exigem acao. |
| Direita | Drawer contextual quando um item e selecionado: aluno, valor, vencimento, status, origem, comprovante, conversa, historico e acoes seguras. |
| Inferior | Sem bloco obrigatorio no MVP; detalhe operacional completo fica em Kanban e Movimentacoes. |
| Drawers/modais | Abrir cobranca, enviar lembrete, abrir conversa, confirmar pagamento com evidencia, criar tarefa, abrir aluno, exportar. |
| Componentes | `3B.3` tabela/cards; `3C.2` conciliacao/comprovante; `3B.5` permissao. |
| Estados | normal, atraso, conciliacao pendente, falha, sem permissao. |
| IA/plano/cota | Financeiro com travas; IA redige cobranca, mas acordos/descontos sao humanos. |

### 18. Financeiro - Kanban

| Item | Blueprint |
| --- | --- |
| Rotas | `/app/financeiro/kanban` |
| Layout | Operacao financeira por estagio, para volume e acompanhamento de cobrancas/pendencias. |
| Topo | Periodo, unidade, responsavel, tipo, risco, busca e filtros. |
| Esquerda | Filtros por responsavel, turma, plano, atraso, forma de pagamento, origem e agente. |
| Centro | Colunas: a vencer, vence hoje, em atraso, promessa de pagamento, comprovante enviado, conciliacao pendente, resolvido. |
| Direita | Drawer do card selecionado com aluno, valor, vencimento, canal, ultima acao, conversa, comprovante e historico. |
| Drawers/modais | Mover etapa, enviar lembrete, registrar promessa, confirmar pagamento, pedir comprovante, criar tarefa, pedir aprovacao ou escalar para Operacao quando sensivel. |
| Componentes | `3B.3` kanban/lista/cards; `3C.2` comprovante/conciliacao/moeda; `3B.4` mensagem; `3B.5` permissao financeira. |
| Estados | aberto, vence hoje, atrasado, falhou, promessa ativa, comprovante pendente, conciliacao pendente, resolvido. |
| IA/plano/cota | Agente pode priorizar e redigir; automacao so executa lembrete simples permitido. |

### 19. Financeiro - Movimentacoes

| Item | Blueprint |
| --- | --- |
| Rotas | `/app/financeiro/movimentacoes`, `/app/financeiro/movimentacoes/[id]` como drawer ou deep-link futuro |
| Layout | Tabela/lista completa de movimentacoes financeiras com filtragem por tipo operacional. |
| Topo | Periodo, vencimento, status, tipo de movimentacao, aluno, turma, plano, forma de pagamento, responsavel, busca, filtros e exportacao. |
| Esquerda | Filtros e segmentos: mensalidade, cobranca avulsa, parcela, pagamento recebido, falha, promessa, estorno, desconto, ajuste, conciliacao, comprovante pendente. |
| Centro | Tabela completa com aluno, valor, vencimento, status, tipo, plano, origem, metodo, comprovante, responsavel, ultima atividade e acoes. |
| Direita | Drawer do item selecionado: detalhe financeiro, comprovante/anexo, conversa vinculada, historico, auditoria e acoes. |
| Drawers/modais | Enviar lembrete/link, confirmar comprovante, conciliar, registrar promessa, marcar falha, criar tarefa, pedir aprovacao, exportar. |
| Componentes | `3C.2` comprovante/conciliacao/moeda; `3B.3` tabela; `3B.4` mensagem; `3B.5` permissao financeira; `3B.2` confirmacao. |
| Estados | previsto, aberto, pago, atrasado, falhou, sem identificacao, comprovante em analise, promessa ativa, estorno. |
| IA/plano/cota | Lembrete simples permitido se Financeiro ativo; disputa/acordo/desconto exige humano. |

### 20. Excecoes Financeiras No MVP

| Item | Blueprint |
| --- | --- |
| Rotas | Sem rota propria. Resolver por `/app/financeiro`, `/app/financeiro/kanban`, `/app/financeiro/movimentacoes`, `/app/aprovacoes`, `/app/tarefas`, `/app/alunos/[id]` e `/app/operacao`. |
| Layout | Excecoes financeiras aparecem como item de fila, card, movimentacao, aprovacao ou tarefa contextual. |
| Topo | Herdado da superficie onde a excecao nasceu. |
| Esquerda | Filtros/filas existentes: excecoes, ajustes, descontos, estornos, promessas, atrasos ou bloqueios. |
| Centro | Lista, kanban ou tabela da rota dona. Nao existe central separada no MVP. |
| Direita | Drawer com impacto, aluno, contrato/pagamento, risco, politica, historico e auditoria. |
| Drawers/modais | Simular impacto quando necessario, aprovar, rejeitar, pedir dados, executar, registrar motivo, criar tarefa. |
| Componentes | `3C.2` simulador financeiro; `3C.3` diff/auditoria; `3B.2` confirmacao. |
| Estados | aguardando aprovacao, risco alto, disputa, acordo ativo, rejeitado. |
| IA/plano/cota | Autonomia bloqueada; copiloto explica impacto e prepara rascunho. |

### 21. Contratos E Documentos Financeiros

| Item | Blueprint |
| --- | --- |
| Rotas | `/app/financeiro/documentos`; deep-links de contrato so se a implementacao exigir. |
| Layout | Rota herdada, sem imagem nova: lista de documentos + viewer/detalhe e historico. |
| Topo | Topbar da familia Financeiro com `Visao geral`, `Kanban`, `Movimentacoes`, `Documentos`; busca, tipo, status, aluno, acao "Enviar documento". |
| Esquerda | Tipos: contratos, termos, recibos, notas, vencidos, pendentes. |
| Centro | Lista/tabela de documentos financeiros, contratos, recibos, notas, comprovantes e anexos. |
| Direita | Preview, status, assinatura, envio, anexo, aluno/movimentacao relacionada e historico curto. |
| Drawers/modais | Ver, enviar, reenviar, anexar, baixar quando permitido, arquivar, criar tarefa, auditar, ver erro. |
| Componentes | `3C.2` viewer/upload/comprovante; `3B.3` tabela; `3C.3` auditoria. |
| Estados | rascunho, pendente, enviado, visualizado, assinado, vencido, cancelado, arquivado, erro de envio, sem permissao. |
| IA/plano/cota | Status manual/link externo; nenhuma autonomia em assinatura sensivel. |

### 22. Retencao

| Item | Blueprint |
| --- | --- |
| Rotas | `/app/retencao`, `/app/retencao/riscos` |
| Layout | Painel de risco com filas e plano de acao. |
| Topo | Risco, periodo, grupo, filtros, acao "Criar tarefa". |
| Esquerda | Segmentos: alto risco, inativos, primeira semana, queda frequencia, satisfacao. |
| Centro | Cards/lista de alunos em risco com motivo, score e proxima acao. |
| Direita | Plano de acao, historico curto, mensagem sugerida, responsavel e tarefa. |
| Drawers/modais | Criar tarefa, preparar mensagem, abrir caso, marcar acompanhamento. |
| Componentes | `3B.3` cards/lista; `3B.4` sugestao/mensagem; `3C.1` perfil/timeline. |
| Estados | risco baixo/medio/alto, inativo, retorno pendente, novo aluno. |
| IA/plano/cota | Copiloto sugere abordagem; contato autonomo so seguro e com politica. |

### 23. Cancelamentos E Reativacao

| Item | Blueprint |
| --- | --- |
| Rotas | `/app/cancelamentos`, `/app/retencao/reativacoes` |
| Layout | Duas superficies irmas: cancelamentos para pedido ativo de saida/pausa; reativacoes para ex-aluno, pausado ou inativo elegivel para retorno. |
| Topo | Status, motivo, elegibilidade, periodo, plano anterior e responsavel. |
| Esquerda | Segmentos: novos pedidos, em salvamento, pausa solicitada, recuperados, elegiveis para retorno, pausados vencendo, sem resposta, nao contatar. |
| Centro | Lista/tabela operacional com pedido de saida ou oportunidade de retorno. |
| Direita | Motivo, historico, plano de salvamento ou oportunidade de retorno, restricoes, proxima tentativa e automacao pausada quando sensivel. |
| Drawers/modais | Registrar motivo, confirmar cancelamento com confirmacao forte, converter em pausa, reservar vaga com validacao, iniciar reativacao, marcar nao contatar. |
| Componentes | `3B.3` tabela/lista; `3B.4` comunicacao; `3C.1` perfil/timeline; `3B.2` confirmacao. |
| Estados | pedido aberto, salvamento, pausa solicitada, cancelado, recuperado, ex-aluno elegivel, retorno pendente, reativado, nao contatar, automacao pausada. |
| IA/plano/cota | Cancelamento ativo e sensivel; autonomia pausada, copiloto apenas. |

### 24. Reclamacoes E Casos Sensiveis

| Item | Blueprint |
| --- | --- |
| Rotas | `/app/reclamacoes`, `/app/reclamacoes/[caseId]` |
| Layout | Central de caso sensivel com resposta e auditoria. |
| Topo | Severidade, prazo, responsavel, status, filtro por risco. |
| Esquerda | Filas por severidade, sem dono, vencendo, resolvido, recuperacao. |
| Centro | Cards/lista de reclamacoes e casos sensiveis. |
| Direita | Plano de resposta, historico, pausa de automacao, auditoria, proxima acao. |
| Drawers/modais | Classificar, escalar, pausar automacao, responder, resolver, registrar motivo. |
| Componentes | `3B.2` alertas/confirmacao; `3B.4` resposta; `3C.3` auditoria/diff. |
| Estados | novo, severo, sem dono, resolvido, recuperacao pendente. |
| IA/plano/cota | Copiloto rascunha; autonomia bloqueada em severo/reclamacao. |

### 25. Jornadas E Operacao

| Item | Blueprint |
| --- | --- |
| Rotas | `/app/operacao`, `/app/operacao/[caseId]` |
| Layout | Mapa visual de jornadas com cards conectados e painel de caso. |
| Topo | Status, area, responsavel, etapa, busca, filtro de bloqueios. |
| Esquerda | Etapas, tipos de caso, donos, alertas e filtros. |
| Centro | Canvas de jornadas com cards conectados, filas e bloqueios. |
| Direita | Caso selecionado, historico curto, sugestao, risco, cota, acoes manuais. |
| Inferior | Incidentes, gargalos e atividade operacional. |
| Drawers/modais | Atribuir, mover etapa, pausar fluxo, corrigir dado, reprocessar, fechar. |
| Componentes | `2B` canvas; `3A` conectores/cards; `3B.3` atividade; `3C.3` trace/incidente. |
| Estados | aberto, bloqueado, aguardando humano, incidente, resolvido. |
| IA/plano/cota | Manual sempre; copiloto prioriza/resume; autonomo apenas tarefa segura. |

### 26. Tarefas

| Item | Blueprint |
| --- | --- |
| Rotas | `/app/tarefas`, `/app/tarefas/[taskId]` |
| Layout | Fila/lista priorizada com detalhe contextual. |
| Topo | Responsavel, prazo, prioridade, origem, acao "Criar tarefa". |
| Esquerda | Donos, status, etiquetas, atrasadas, minhas tarefas e tarefas sem dono. |
| Centro | Lista densa de tarefas. Kanban e opcional futuro, nao o padrao base. |
| Direita | Detalhe da tarefa, origem, comentarios, checklist/subtarefas e historico. |
| Drawers/modais | Assumir, delegar, concluir, comentar, reagendar, abrir origem. |
| Componentes | `3B.3` lista/kanban; `3B.2` drawer; `3C.1` checklist; `3B.4` comentario. |
| Estados | atrasada, sem dono, aguardando, concluida, bloqueada. |
| IA/plano/cota | Copiloto sugere prioridade; autonomo pode criar tarefa segura. |

### 26.1 Checklists

| Item | Blueprint |
| --- | --- |
| Rotas | `/app/checklists`, `/app/checklists/[runId]` |
| Layout | Lista de execucoes de rotinas com detalhe lateral do checklist selecionado. |
| Topo | Tipo, status, responsavel, busca, acao "Criar checklist". |
| Esquerda | Hoje, Abertura, Fechamento, Agenda, Financeiro, Alunos, Agentes e Setup. |
| Centro | Lista de execucoes com tipo, progresso, responsavel, prazo, status, proximo passo e ultima atividade. |
| Direita | Execucao selecionada com passos, bloqueio, comentario, historico curto e acoes. |
| Drawers/modais | Continuar, criar tarefa a partir de passo, concluir, reabrir, abrir origem. |
| Componentes | `3B.3` lista; `3B.2` drawer; `3C.1` checklist; `3B.2` feedback. |
| Estados | pendente, em andamento, bloqueado, em revisao, concluido, atrasado, reaberto. |
| IA/plano/cota | CRM funciona sem agentes; copiloto pode sugerir passos e detectar bloqueios; autonomia so marca passo com evidencia objetiva. |

### 27. Aprovacoes

| Item | Blueprint |
| --- | --- |
| Rotas | `/app/aprovacoes`, `/app/aprovacoes/[approvalId]` |
| Layout | Fila de decisoes com painel de antes/depois e risco. |
| Topo | Risco, origem, prazo, custo/cota, filtro de tipo. |
| Esquerda | Tipos: mensagens, financeiro, agenda, agente, comunicado, privacidade. |
| Centro | Fila de aprovacoes com status, responsavel, prazo e impacto. |
| Direita | Proposta, antes/depois, mensagem, risco, custo/cota, botoes decisao. |
| Drawers/modais | Aprovar, editar, rejeitar, pedir dados, abrir origem, ver auditoria. Execucao ocorre depois da aprovacao quando politica e modo permitirem. |
| Componentes | `3B.4` aprovacao; `3C.3` diff/preflight; `3B.2` confirmacao; `3B.5` cota. |
| Estados | pendente, editada, aprovada, rejeitada, expirada, bloqueada. |
| IA/plano/cota | Agente nunca aprova sozinho; cota e auditoria sempre visiveis. |

### 28. Agentes E Fluxos

| Item | Blueprint |
| --- | --- |
| Rotas | `/app/agentes`, `/app/agentes/[agentId]`, `/app/agentes/[agentId]/fluxos`, `/app/fluxos`, `/app/fluxos/[flowId]`, `/app/fluxos/[flowId]/simular` |
| Layout | Console de agentes com builder/simulador no centro e governanca no painel. |
| Topo | Agente, modo, status, plano, cota, acao "Simular/Publicar". |
| Esquerda | Lista de agentes, fluxos, status, rascunhos, bloqueados por plano. |
| Centro | Cards de fluxo ou builder com etapas, modo, condicao, acao e fallback. |
| Direita | Regras, limites, templates, preflight, ultima execucao, qualidade e permissoes. |
| Drawers/modais | Configurar modo, testar exemplo, editar regra/template, publicar, pausar. |
| Componentes | `3C.3` builder/simulador/preflight; `3B.5` plano/cota/politica; `3B.1` forms. |
| Estados | bloqueado por plano, rascunho, ativo, pausado, sem dados, cota 100. |
| IA/plano/cota | Mostrar 0/1/3/7 agentes, slot coberto, modo manual/copiloto/autonomo e fallback. |

### 29. Execucoes E Incidentes De Agentes

| Item | Blueprint |
| --- | --- |
| Rotas | `/app/fluxos/execucoes/[runId]`, `/app/operacao/incidentes`, `/app/operacao/incidentes/[incidentId]` |
| Layout | Observabilidade operacional: lista de execucoes + trace/incidente. |
| Topo | Periodo, agente, fluxo, status, custo, filtro de erro. |
| Esquerda | Filtros: sucesso, falhou, incidente, pausado, reprocessavel. |
| Centro | Lista/tabela de execucoes e incidentes. |
| Direita | Trace, ferramenta usada, custo, erro, causa, impacto, fallback. |
| Drawers/modais | Explicar falha, criar incidente, corrigir dado, reprocessar seguro, pausar fluxo. |
| Componentes | `3C.3` trace/incidente/evals; `3B.2` error; `3B.5` cota/auditoria. |
| Estados | sucesso, falhou, incidente, pendente, reprocessando, bloqueado. |
| IA/plano/cota | Reprocessamento seguro/idempotente; mostrar custo/cota e auditoria. |

### 30. Uso, Cotas E Economia

| Item | Blueprint |
| --- | --- |
| Rotas | `/app/uso`, `/app/uso/cotas`, `/app/uso/custos`, `/app/uso/extrato`, `/app/uso/alertas`, `/app/uso/pacotes`, `/app/uso/regras-economia`, `/app/uso/limites-fluxo`, `/app/uso/limites-fluxo/[flowId]` |
| Layout | Governanca de uso com graficos, extrato e acoes de economia. |
| Topo | Cota usada, restante, previsao, status 70/90/100, pacote ativo. |
| Esquerda | Tipos de consumo: agente, fluxo, canal, mensagens, execucoes, pacotes. |
| Centro | Grafico/lista de consumo por area/fluxo e extrato. |
| Direita | Acoes de economia, limites por fluxo, pacote extra, bloqueios e fallback. |
| Drawers/modais | Comprar pacote, ajustar economia, pausar baixa prioridade, ver execucao. |
| Componentes | `3B.5` cotas/plano; `3C.3` relatorio/trace; `3B.3` tabela/graficos. |
| Estados | 70, 90, 100, pacote ativo, automacao convertida em tarefa. |
| IA/plano/cota | Cota 100 bloqueia automacao paga; manual continua disponivel. |

### 31. Relatorios E Exportacoes

| Item | Blueprint |
| --- | --- |
| Rotas | `/app/relatorios`, `/app/relatorios/semana`, `/app/relatorios/financeiro`, `/app/relatorios/vendas`, `/app/relatorios/risco`, `/app/relatorios/agentes`, `/app/relatorios/ocupacao`, `/app/dinheiro-na-mesa`, `/app/exportacoes`, `/app/exportacoes/[jobId]` |
| Layout | Painel de relatorios acionaveis com drilldown e exportacoes. |
| Topo | Periodo, area, salvar filtro, exportar, agendar relatorio. |
| Esquerda | Tipos: semana, financeiro, vendas, ocupacao, risco, agentes, exportacoes. |
| Centro | Graficos, tabelas e rankings com links para origem. |
| Direita | Explicacao, filtros salvos, origem relacionada, job de exportacao. |
| Drawers/modais | Exportar, agendar, abrir origem, ver job, baixar arquivo. |
| Componentes | `3C.3` relatorios/exportacoes; `3B.3` tabela/cards; `3B.1` filtros. |
| Estados | sem dados, exportando, pronto, falhou, sem permissao. |
| IA/plano/cota | Copiloto explica tendencia; exportacao nao ocorre autonomamente. |

Nota MVP: `Gargalos` e `Capacidade` nao sao rotas dedicadas. Eles aparecem como blocos/indicadores em Relatorios e abrem Operacao, Tarefas, Aprovacoes, Inbox, Agenda, Turmas, Grade ou Reposicoes com filtros aplicados.

### 32. Configuracoes

| Item | Blueprint |
| --- | --- |
| Rotas | `/app/configuracoes/*` |
| Layout | Menu de secoes + formulario + impacto/auditoria. |
| Topo | Busca, area, status, salvar, testar, ver impacto. |
| Esquerda | Secoes: studio, equipe, permissoes, canais, agenda, financeiro, vendas, retencao, privacidade, campos, notificacoes. |
| Centro | Formulario da secao selecionada. |
| Direita | Impacto, teste, auditoria, antes/depois, permissao e ultima alteracao. |
| Drawers/modais | Convidar equipe, alterar permissao, testar canal, salvar sensivel, reverter. |
| Componentes | `3B.1` forms; `3B.5` permissao/integracao/politica; `3C.3` diff/auditoria. |
| Estados | incompleto, sem permissao, mudanca sensivel, salvo, erro de teste. |
| IA/plano/cota | Copiloto sugere impacto/config; mudanca sensivel exige confirmacao. |

### 33. Politicas Operacionais

| Item | Blueprint |
| --- | --- |
| Rotas | `/app/politicas`, `/app/politicas/[policyId]`, `/app/politicas/[policyId]/simular`, `/app/configuracoes/politicas` |
| Layout | Editor versionado de regras com simulacao e historico. |
| Topo | Politica, versao, vigencia, status, simular, publicar. |
| Esquerda | Tipos: falta, reposicao, cancelamento, comunicacao, financeiro, agentes. |
| Centro | Editor de regras em linguagem simples e condicoes. |
| Direita | Simulacao de impacto, antes/depois, historico de versoes e auditoria. |
| Drawers/modais | Criar versao, simular, aprovar, publicar, reverter. |
| Componentes | `3C.3` modo/preflight/diff; `3B.5` politicas; `3B.1` forms. |
| Estados | rascunho, aguardando aprovacao, ativa, revertida, bloqueada. |
| IA/plano/cota | Nao publica sozinha; copiloto simula impacto. |

### 34. Recursos, Feriados E Disponibilidade

| Item | Blueprint |
| --- | --- |
| Rotas | `/app/recursos`, `/app/recursos/[resourceId]`, `/app/configuracoes/recursos` |
| Layout | Calendario de disponibilidade + impacto em aulas. |
| Topo | Periodo, recurso, professor, sala, acao "Bloquear recurso". |
| Esquerda | Recursos, salas, equipamentos, professores, feriados, recessos. |
| Centro | Calendario/disponibilidade com bloqueios e eventos afetados. |
| Direita | Impacto, aulas afetadas, alunos, avisos necessarios, simulacao. |
| Drawers/modais | Bloquear recurso, criar feriado, simular impacto, avisar envolvidos. |
| Componentes | `3C.2` conflito/calendario; `3B.1` forms; `3B.2` confirmacao. |
| Estados | fechado, recurso indisponivel, professor indisponivel, impacto pendente. |
| IA/plano/cota | Aviso seguro pode ser sugerido; mudanca estrutural auditada. |

### 35. Segmentos E Comunicados

| Item | Blueprint |
| --- | --- |
| Rotas | `/app/segmentos`, `/app/segmentos/[segmentId]`, `/app/comunicados`, `/app/comunicados/[broadcastId]` |
| Layout | Construtor de publico + preview + aprovacao de envio. |
| Topo | Publico, canal, status, custo, acao "Aprovar envio". |
| Esquerda | Segmentos salvos, filtros de elegibilidade, campanhas e status. |
| Centro | Construtor de publico, audiencia elegivel/inelegivel, template e preview. |
| Direita | Consentimento, custo estimado, falhas previstas, aprovacao e cota. |
| Drawers/modais | Criar segmento, editar template, validar publico, aprovar, acompanhar falhas. |
| Componentes | `3C.3` segmentos/comunicados; `3B.1` filtros/forms; `3B.4` mensagem; `3B.5` cota/permissao. |
| Estados | publico invalido, sem consentimento, aguardando aprovacao, enviado, falhou. |
| IA/plano/cota | Envio exige consentimento, custo/cota e aprovacao quando sensivel. |

### 36. Integracoes

| Item | Blueprint |
| --- | --- |
| Rotas | `configuracao especifica da integracao`, `configuracao especifica da integracao`, `/app/importacao`, `/app/importacao/[jobId]` |
| Layout | Cartoes de conectores + logs/importacao. |
| Topo | Status geral, ultima sincronizacao, filtro de erro, acao "Conectar". |
| Esquerda | WhatsApp, pagamentos, calendario, importacao, logs, erros recorrentes. |
| Centro | Cartoes de integracoes com status, teste e acoes. |
| Direita | Log curto, falhas, reprocessamento, incidente e configuracao. |
| Drawers/modais | Conectar, testar, reprocessar, abrir incidente, mapear importacao. |
| Componentes | `3B.5` integracoes; `3C.1` importacao/mapeamento; `3C.3` logs/reprocessamento. |
| Estados | conectado, falhou, provedor indisponivel, aguardando, erro recorrente. |
| IA/plano/cota | Reprocessamento seguro; logs auditados; IA apenas explica falha. |

### 37. Auditoria

| Item | Blueprint |
| --- | --- |
| Rotas | `/app/auditoria`, `/app/auditoria/[eventId]` |
| Layout | Tabela de eventos + detalhe antes/depois. |
| Topo | Periodo, usuario, objeto, risco, origem, exportar. |
| Esquerda | Filtros por tipo, risco, area, ator, origem e objeto. |
| Centro | Lista/tabela de eventos auditaveis. |
| Direita | Antes/depois, ator, origem, horario, objeto, permissao e link de origem. |
| Drawers/modais | Abrir objeto, exportar, pedir acesso, ver evento completo. |
| Componentes | `3C.3` log/diff; `3B.3` tabela; `3B.5` permissao. |
| Estados | sem permissao, evento sensivel, alteracao critica, sem dados. |
| IA/plano/cota | IA pode resumir somente eventos permitidos; auditoria e fonte de verdade. |

### 38. Privacidade E Solicitacoes

| Item | Blueprint |
| --- | --- |
| Rotas | `/app/privacidade/solicitacoes`, `/app/privacidade/solicitacoes/[requestId]`, `/app/suporte/acessos`, `/app/suporte/acessos/[grantId]` |
| Layout | Fila sensivel LGPD/grants com validacao e execucao. |
| Topo | Status, tipo, prazo, risco, permissao, acao "Validar". |
| Esquerda | Tipos: exportacao, anonimizar, apagar, opt-out, grant suporte, consentimento. |
| Centro | Fila de solicitacoes e acessos temporarios. |
| Direita | Validacao, identidade, escopo, antes/depois, auditoria e prazo. |
| Drawers/modais | Validar identidade, aprovar, negar, executar, revogar, expirar acesso. |
| Componentes | `3C.3` LGPD/grant/auditoria; `3C.1` consentimento/mascaramento; `3B.2` confirmacao. |
| Estados | pendente, validando, executado, negado, acesso ativo, expirado. |
| IA/plano/cota | Copiloto restrito a checklist/rascunho; execucao sensivel sempre humana/auditada. |

### 39. Assinatura E Billing

| Item | Blueprint |
| --- | --- |
| Rotas | `/app/billing`, `/app/billing/add-ons`, `/app/billing/invoices` |
| Layout | Administracao de plano Taliya com faturas, pacotes e agentes. |
| Topo | Plano atual, status, agentes inclusos, proxima cobranca, acao "Ver planos". |
| Esquerda | Produtos: plano, agentes, pacotes de cota, faturas, metodo pagamento. |
| Centro | Plano atual, slots de agentes, faturas, add-ons e pacotes. |
| Direita | Upgrade/downgrade, impacto, bloqueios por plano, cota e historico. |
| Drawers/modais | Abrir portal, comprar pacote, atualizar plano, trocar agente, ver fatura. |
| Componentes | `3B.5` plano/billing/cota/0 agentes; `3C.3` exportacao/log; `3B.2` confirmacao. |
| Estados | ativo, vencido, falha, pacote ativo, 0 agentes, bloqueado por plano. |
| IA/plano/cota | Billing decide entitlement; plano Base continua CRM completo manual. |

## Agrupamento Para Geracao De Imagens Web

Para gerar as telas finais, usar estas familias:

| Rodada | Familias | Paginas |
| --- | --- | --- |
| 4A | Hoje + Operacao | Hoje, Jornadas, Tarefas, Aprovacoes |
| 4B | Atendimento + Alunos | Inbox, Conversas, Contatos, Alunos, Historico, Professor |
| 4C | Agenda | Agenda, Turmas, Aula, Chamada, Reposicoes, Recursos |
| 4D | Vendas + Retencao | Vendas, Interessados, Experimental, Matriculas, Retencao, Cancelamentos, Reclamacoes |
| 4E | Financeiro + Documentos | Financeiro, Kanban financeiro, Movimentacoes, excecoes financeiras sem pagina propria, Contratos/documentos |
| 4F | Agentes + Uso | Agentes, Fluxos, Execucoes, Incidentes, Uso/cotas |
| 4G | Relatorios + Admin | Relatorios, Configuracoes, Politicas, Segmentos, Integracoes, Auditoria, Privacidade, Billing |
| 4H | Auditoria final web | Revisao cruzada das 38 superficies e 157 casos |

## Regras Para Prompts Visuais Da Rodada 4

Cada prompt de pagina deve conter:

- nome da pagina e rota;
- familia;
- layout escolhido;
- blocos por zona;
- componentes obrigatorios;
- estados obrigatorios;
- caminho manual;
- comportamento com 0 agentes;
- comportamento com agente ativo/bloqueado;
- cota/permissao/auditoria quando aplicavel;
- o que nao deve aparecer.

## Decisao Final

Este blueprint fecha a preparacao para gerar paginas web.

Proximo passo:

```text
Rodada 4A - gerar telas web de Hoje + Operacao.
```
