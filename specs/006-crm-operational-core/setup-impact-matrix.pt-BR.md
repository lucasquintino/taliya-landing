# Matriz De Impacto Das Configuracoes

Status: rascunho consolidado.
Data: 2026-05-13.

## Objetivo

Mapear como cada configuracao afeta telas, casos de uso, rotinas operacionais, agentes, tarefas, aprovacoes, cotas e auditoria.

## Leitura

- `Manual`: CRM funciona sem agente.
- `Copiloto`: agente sugere/prepara.
- `Autonomo`: agente executa apenas com preflight.

## Matriz principal

| Configuracao | Telas afetadas | Agentes/fluxos | Casos de uso | Tarefas/aprovacoes | Cota/auditoria |
|---|---|---|---|---|---|
| Horario comercial | Hoje, Agenda, Inbox, Agentes | Atendimento, Agenda, Financeiro, Vendas, Retencao | envio, lembrete, agendamento | tarefa fora de horario | auditoria se alterar janela |
| Permissoes | Todas | Todos | toda acao sensivel | aprovacao/bloqueio | auditoria obrigatoria |
| Turmas/capacidade | Agenda, Hoje, Alunos, Reposicoes | Agenda | encaixe, chamada, reposicao | conflito de vaga | auditoria em mudanca ampla |
| Falta/no-show | Hoje, Aula, Aluno, Retencao | Agenda, Retencao | chamada, risco, reposicao | tarefa se conflito | auditoria se corrigir |
| Regra de reposicao | Hoje, Agenda, Reposicoes, Aluno | Agenda, Atendimento | pedido de reposicao, vaga aberta | aprovacao se excecao | snapshot de politica |
| Modelo de cobranca | Financeiro, Aluno, Agenda | Financeiro, Agenda | matricula, cobranca, reposicao | aprovacao se mudar | auditoria, impacto financeiro |
| Consumo de aula | Aula, Aluno, Reposicoes, Financeiro | Agenda, Financeiro | chamada, pacote, credito | aprovacao se ajuste | snapshot e auditoria |
| Inadimplencia | Hoje, Financeiro, Agenda, Reposicoes | Financeiro, Agenda | bloquear/liberar aula, lembrar pagamento | tarefa/aprovacao | auditoria em excecao |
| WhatsApp conectado | Inbox, Canais, Agentes | Atendimento e demais externos | responder, lembrar, convidar | tarefa se desconectado | cota e envio auditado |
| Opt-out | Inbox, Privacidade, Comunicados | Todos externos | nao contatar, mensagem | bloqueio | privacidade vence |
| Modelos de mensagem | Inbox, Agentes, Comunicados | Todos externos | envio de mensagem | aprovacao se sensivel | cota e auditoria |
| Modo do fluxo pos-go-live | Agentes, Fluxos, Hoje, Operacao | Todos | todos os fluxos do agente | aprovacao de autonomia | auditoria, cota |
| Responsavel de fallback pos-go-live | Hoje, Tarefas, Incidentes | Todos | falha, handoff | cria tarefa | auditoria em incidente |
| Regra de seguranca/politica operacional | Politicas, Aprovacoes, Agentes | Todos | autonomia, sensivel | aprovar/publicar | versao e auditoria |
| Cota/economia | Hoje, Uso, Agentes, Aprovacoes | Todos ativos | bloquear/pausar automacao | tarefa se limite | ledger idempotente |
| Integracao/provedor | Integracoes, Canais, Financeiro | Fluxos que usam ferramenta | importar, enviar, conciliar | incidente/tarefa | logs e retry |

## Impacto por tela

| Tela | Configuracoes que mais afetam |
|---|---|
| Hoje | horarios, tarefas, filas, agenda, financeiro, cotas, agentes, regras de seguranca |
| Agenda | turmas, professores, capacidade, reposicao, consumo, feriados |
| Aulas/Chamada | presenca, no-show, consumo, professor, plano do aluno |
| Reposicoes | regra de reposicao, credito, vaga, financeiro, opt-out, agente Agenda |
| Alunos | plano, turma, presenca, financeiro, historico, consentimento |
| Financeiro | modelo de cobranca, metodo, vencimento, inadimplencia, conciliacao |
| Inbox | WhatsApp, opt-out, modelos de mensagem, agente Atendimento |
| Vendas | origem, cadencia, modelos de mensagem, opt-out, agente Vendas |
| Retencao | falta, risco, cancelamento, financeiro, mensagem, agente Retencao |
| Tarefas | roteamento, fallback, prioridade, permissoes |
| Checklists | modelos de rotina, responsavel, prazo |
| Aprovacoes | regras de seguranca, permissoes, excecoes, agentes |
| Agentes/Fluxos | entitlement, modo, regras de seguranca, cota, modelos de mensagem, fallback |
| Uso/Cotas | eventos de IA, mensagens, lotes, economia |
| Auditoria | todas as regras sensiveis |

## Impacto por agente

| Agente | Configuracoes criticas |
|---|---|
| Atendimento | WhatsApp, opt-out, modelos de mensagem, horarios, handoff |
| Agenda | turmas, vagas, reposicao, consumo, inadimplencia, janelas |
| Vendas | origem, cadencia, experimental, modelos de mensagem, opt-out |
| Financeiro | cobranca, vencimento, promessa, metodo, inadimplencia |
| Retencao | risco, cancelamento, reativacao, reclamacao, pausa de automacao |
| Historico/Professor | historico permitido, notas, permissao, privacidade |
| Gestao/Governanca | cotas, regras de seguranca, incidentes, relatorios, auditoria |

## Impacto por 0/1/3/7 agentes

| Configuracao | 0 agentes | 1 agente | 3 agentes | 7 agentes |
|---|---|---|---|---|
| Reposicao | Manual/programatico | IA se Agenda | IA no bundle padrao | IA completa com regra publicada |
| Financeiro | Manual/programatico | IA se Financeiro | Manual salvo troca | IA com travas |
| Modelos de mensagem | Usados por humano | Usados pelo agente ativo | Usados pelos 3 dominios | Usados por todos |
| Cotas | Sem consumo IA | Slot ativo | 3 slots | todos os agentes |
| Regras de seguranca | Padronizam humano | Limitam agente ativo | Limitam dominios ativos | Limitam todos |

## Aceite

Esta matriz esta correta quando:

- toda configuracao MVP tem pelo menos uma tela afetada;
- toda regra de agente aponta para politica/cota/permissao;
- todo impacto sensivel tem aprovacao/auditoria;
- 0 agentes aparece como caminho funcional.
