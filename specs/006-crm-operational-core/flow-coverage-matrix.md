# Flow Coverage Matrix

This document maps the historical 91 configured flows to the CRM routes needed for manual, copilot and autonomous operation.

Round 1 review note:

```text
91 original flows
+ 5 strong candidate additions
= 96 strong candidate flows
+ 2 optional standalone-flow candidates under validation
= 98 possible flows if both optional candidates stay standalone
```

The 91-row matrix below remains the historical baseline. The additions after the matrix should be treated as the current product-review layer.

Legend:

- Primary route: where the case is normally worked.
- Support routes: detail, approval, audit, quota or transition routes.
- Core objects: minimum records needed.

## Atendimento

| Flow | Primary route | Support routes | Core objects |
| --- | --- | --- | --- |
| A1 Nova Conversa | `/app/inbox` | `/app/conversas/[id]`, `/app/contatos/[id]`, `/app/interessados/[id]`, `/app/operacao/[caseId]` | Conversation, Contact, OperationCase |
| A2 Duvidas Permitidas | `/app/inbox` | `/app/tarefas/[taskId]`, `/app/fluxos/[flowId]` when the answer belongs to a configured flow | Conversation, KnowledgeBase, Task |
| A3 Aluno Existente | `/app/inbox` | `/app/alunos/[id]`, `/app/conversas/[id]`, `/app/operacao/[caseId]` | Student, Conversation, OperationCase |
| A4 Fora Do Escopo | `/app/inbox` | `/app/tarefas/[taskId]`, `/app/auditoria/[eventId]` | Conversation, Task, AuditEvent |
| A5 Handoff Humano | `/app/tarefas` | `/app/tarefas/[taskId]`, `/app/conversas/[id]`, `/app/aprovacoes/[approvalId]` | Task, Conversation, Approval |
| A6 Consentimento/Opt-Out | `/app/contatos/[id]` | `/app/privacidade/solicitacoes`, `/app/auditoria/[eventId]` | Contact, Consent, AuditEvent |
| A7 Identidade/Midias | `/app/contatos/[id]` | `/app/dados/duplicidades`, `/app/historico/documentos`, `/app/financeiro` | Contact, DocumentRecord, Task |
| A8 Privacidade/Dados | `/app/privacidade/solicitacoes` | `/app/contatos/[id]`, `/app/auditoria/[eventId]` | PrivacyRequest, Contact, AuditEvent |
| A9 Telefone Compartilhado E Identidade | `/app/contatos` | `/app/alunos/[id]`, `/app/inbox`, `/app/dados/duplicidades` | Contact, Conversation, DataIssue |
| A10 Ciclo De Vida/SLA | `/app/inbox` | `/app/operacao`, `/app/tarefas/[taskId]`, `/app/relatorios` | Conversation, OperationCase, Task |

## Agenda

| Flow | Primary route | Support routes | Core objects |
| --- | --- | --- | --- |
| B1 Confirmacao De Presenca | `/app/aulas/[id]/chamada` | `/app/envios/[sendId]`, `/app/fluxos/execucoes/[runId]` | ClassSession, AttendanceRecord, SendAttempt |
| B2 Falta Com Aviso | `/app/aulas/[id]` | `/app/creditos-reposicao`, `/app/reposicoes`, `/app/operacao/[caseId]` | AttendanceRecord, MakeUpCredit, OperationCase |
| B3 No-Show | `/app/aulas/[id]/chamada` | `/app/retencao`, `/app/tarefas/[taskId]` | AttendanceRecord, RetentionSignal, Task |
| B4 Recuperar Vaga Aberta | `/app/reposicoes` | `/app/lista-espera`, `/app/envios/[sendId]`, `/app/aprovacoes/[approvalId]` | ClassSession, WaitlistEntry, SendAttempt |
| B5 Reposicao/Remarcacao | `/app/reposicoes` | `/app/creditos-reposicao`, `/app/aulas/[id]`, `/app/tarefas/[taskId]` | MakeUpCredit, ClassSession, Task |
| B6 Lista De Espera | `/app/lista-espera` | `/app/aulas/[id]`, `/app/envios/[sendId]` | WaitlistEntry, ClassSession, SendAttempt |
| B7 Disponibilidade Experimental | `/app/experimental` | `/app/agenda`, `/app/interessados/[id]` | InterestedPerson, ClassSession, OperationCase |
| B8 Mudanca Horario Fixo | `/app/alunos/[id]` | `/app/agenda`, `/app/financeiro`, `/app/aprovacoes/[approvalId]` | Student, ClassGroup, StudioPlan |
| B9 Cancelamento Pelo Studio | `/app/turmas/[id]` | `/app/aulas/[id]`, `/app/aprovacoes/[approvalId]`, `/app/envios` | ClassSession, Approval, SendAttempt |
| B10 Conflito Capacidade | `/app/turmas/[id]` | `/app/agenda`, `/app/operacao/[caseId]`, `/app/tarefas/[taskId]` | ClassGroup, OperationCase, Task |
| B11 Ajuste De Grade | `/app/grade` | `/app/turmas/[id]`, `/app/aprovacoes/[approvalId]`, `/app/auditoria/[eventId]` | ClassGroup, Approval, AuditEvent |
| B12 Experimental No-Show | `/app/experimental` | `/app/interessados/[id]`, `/app/vendas` | InterestedPerson, ClassSession, Task |
| B13 Creditos Reposicao | `/app/creditos-reposicao` | `/app/alunos/[id]`, `/app/reposicoes` | MakeUpCredit, Student, OperationCase |
| B14 Correcao Presenca | `/app/aulas/[id]/chamada` | `/app/auditoria/[eventId]`, `/app/creditos-reposicao` | AttendanceRecord, AuditEvent, MakeUpCredit |
| B15 Primeira Aula | `/app/matriculas` | `/app/aulas/[id]`, `/app/historico`, `/app/financeiro` | Student, ClassSession, Contract |
| B16 Aula Especial/Workshop | `/app/eventos` | `/app/agenda`, `/app/vendas`, `/app/financeiro` | Event, ClassSession, Payment |

## Vendas

| Flow | Primary route | Support routes | Core objects |
| --- | --- | --- | --- |
| C1 Valores E Planos | `/app/vendas` | `/app/interessados/[id]`, `/app/configuracoes/financeiro/modelos` | InterestedPerson, StudioPlan, Conversation |
| C2 Aula Experimental | `/app/experimental` | `/app/interessados/[id]`, `/app/agenda` | InterestedPerson, ClassSession, OperationCase |
| C3 Lembrete Experimental | `/app/experimental` | `/app/envios/[sendId]`, `/app/fluxos/execucoes/[runId]` | ClassSession, SendAttempt, FlowRun |
| C4 Pos-Aula Experimental | `/app/experimental` | `/app/interessados/[id]`, `/app/professores` | InterestedPerson, ClassSession, StudentHistoryEvent |
| C5 Follow-Up Comercial | `/app/vendas` | `/app/interessados/[id]`, `/app/envios`, `/app/tarefas/[taskId]` | InterestedPerson, Conversation, SendAttempt |
| C6 Pre-Matricula | `/app/matriculas` | `/app/interessados/[id]`, `/app/aprovacoes/[approvalId]` | InterestedPerson, Approval, Task |
| C7 Objecoes | `/app/vendas` | `/app/fluxos/[flowId]`, `/app/aprovacoes/[approvalId]` | Conversation, Template, Approval |
| C8 Origem/Qualificacao | `/app/interessados/[id]` | `/app/relatorios/vendas` | InterestedPerson, Contact, Timeline |
| C9 Perda Comercial | `/app/vendas/perdidos` | `/app/interessados/[id]` | InterestedPerson, LostReason |
| C10 Indicacao | `/app/indicacoes` | `/app/alunos/[id]`, `/app/interessados/[id]` | Referral, Student, InterestedPerson |
| C11 Checkout/Abandono | `/app/checkout-alunos` | `/app/financeiro/movimentacoes/[id]`, `/app/vendas` | StudentCheckout, Payment, InterestedPerson |
| C12 Demanda Sem Vaga | `/app/lista-espera` | `/app/agenda`, `/app/reposicoes`, `/app/vendas` | WaitlistEntry, DemandSignal, InterestedPerson |
| C13 Interessado Para Aluno | `/app/matriculas` | `/app/alunos/[id]`, `/app/agenda`, `/app/financeiro` | Student, InterestedPerson, Payment |
| C14 Upsell/Upgrade | `/app/alunos/[id]` | `/app/financeiro/movimentacoes`, `/app/aprovacoes/[approvalId]` | Student, StudioPlan, Approval |

## Financeiro

| Flow | Primary route | Support routes | Core objects |
| --- | --- | --- | --- |
| D1 Lembrete Vencimento | `/app/financeiro/movimentacoes` | `/app/financeiro/movimentacoes/[id]`, `/app/envios/[sendId]` | Payment, Charge, SendAttempt |
| D2 Pagamento Atrasado | `/app/financeiro/movimentacoes` | `/app/financeiro/movimentacoes/[id]`, `/app/aprovacoes/[approvalId]` | Payment, Charge, Approval |
| D3 Pix/Link | `/app/financeiro/movimentacoes/[id]` | `/app/envios/[sendId]`, `/app/configuracoes/financeiro/pagamentos` | Payment, SendAttempt, PaymentDestination |
| D4 Confirmacao Pagamento | `/app/financeiro/movimentacoes/[id]` | `/app/financeiro/movimentacoes`, `/app/auditoria/[eventId]` | Payment, AuditEvent, IntegrationLog |
| D5 Renovacao Plano | `/app/financeiro/movimentacoes` | `/app/agenda`, `/app/aprovacoes/[approvalId]` | StudioPlan, Payment, Approval |
| D6 Excecoes Financeiras | `/app/financeiro/movimentacoes` | `/app/aprovacoes/[approvalId]`, `/app/tarefas/[taskId]`, `/app/auditoria/[eventId]` | FinancialException, Task, AuditEvent |
| D7 Falha Pagamento | `/app/financeiro/movimentacoes/[id]` | `/app/financeiro/movimentacoes`, `/app/tarefas/[taskId]` | Payment, Charge, Task |
| D8 Recibo/Nota | `/app/financeiro/documentos` | `/app/financeiro/movimentacoes/[id]`, `/app/envios/[sendId]` | DocumentRecord, Payment, SendAttempt |
| D9 Pausa/Trancamento | `/app/financeiro/movimentacoes` | `/app/cancelamentos`, `/app/alunos/[id]` | FinancialException, Student, OperationCase |
| D10 Conciliacao Interna | `/app/financeiro/movimentacoes` | `/app/tarefas/[taskId]` | Payment, ReconciliationCase, Task |
| D11 Contrato/Termos | `/app/contratos/[id]` | `/app/envios/[sendId]`, `/app/auditoria/[eventId]` | Contract, SendAttempt, AuditEvent |
| D12 Bloqueio/Liberacao | `/app/financeiro/movimentacoes` | `/app/alunos/[id]`, `/app/auditoria/[eventId]` | Student, FinancialException, AuditEvent |
| D13 Creditos/Cortesias | `/app/financeiro/movimentacoes` | `/app/creditos-reposicao`, `/app/auditoria/[eventId]` | FinancialException, MakeUpCredit, AuditEvent |
| D14 Fechamento Mensal | `/app/relatorios/financeiro` | `/app/relatorios/semana`, `/app/dinheiro-na-mesa` | Report, Payment, OperationCase |

## Retencao

| Flow | Primary route | Support routes | Core objects |
| --- | --- | --- | --- |
| E1 Queda Frequencia | `/app/retencao/riscos` | `/app/alunos/[id]`, `/app/tarefas/[taskId]` | RetentionSignal, Student, Task |
| E2 Aluno Inativo | `/app/retencao` | `/app/alunos/[id]`, `/app/envios/[sendId]` | Student, RetentionSignal, SendAttempt |
| E3 Retorno | `/app/retencao` | `/app/agenda`, `/app/alunos/[id]` | Student, ClassSession, OperationCase |
| E4 Risco Cancelamento | `/app/cancelamentos` | `/app/tarefas/[taskId]`, `/app/alunos/[id]` | CancellationCase, Student, Task |
| E5 Reativacao Ex-Aluno | `/app/retencao/reativacoes` | `/app/aprovacoes/[approvalId]`, `/app/envios`, `/app/alunos/[id]` | ReactivationCase, Approval, SendAttempt, Student |
| E6 Satisfacao | `/app/reclamacoes` quando sensivel; `/app/retencao` quando preventivo | `/app/tarefas/[taskId]`, `/app/alunos/[id]` | FeedbackSignal, ComplaintCase, RetentionSignal, Task, Student |
| E7 Retorno Apos Pausa | `/app/retencao` | `/app/agenda`, `/app/financeiro` | Student, ClassSession, Payment |
| E8 Risco Por Perfil | `/app/retencao/riscos` | `/app/relatorios/risco` | RetentionSignal, Report |
| E9 Pos-Cancelamento | `/app/cancelamentos` | `/app/retencao`, `/app/financeiro` | CancellationCase, Student, Payment |
| E10 Marco Engajamento | `/app/retencao` | `/app/alunos/[id]/linha-do-tempo`, `/app/envios` | StudentHistoryEvent, SendAttempt |
| E11 Saude/Evento Pessoal | `/app/historico` | `/app/tarefas/[taskId]`, `/app/alunos/[id]` | StudentHistoryEvent, Task, Student |
| E12 Segmentacao Risco | `/app/retencao` | `/app/relatorios`, `/app/aprovacoes/[approvalId]` | RetentionSignal, Report, Approval |

## Gestao

| Flow | Primary route | Support routes | Core objects |
| --- | --- | --- | --- |
| F1 Prioridades Dia | `/app/hoje` | `/app/operacao`, `/app/tarefas` | OperationCase, Task, Priority |
| F2 Dinheiro Na Mesa | `/app/dinheiro-na-mesa` | `/app/relatorios`, `/app/operacao` | Report, Opportunity, OperationCase |
| F3 Fila Humana | `/app/aprovacoes` | `/app/tarefas`, `/app/operacao/[caseId]` | Approval, Task, OperationCase |
| F4 Gargalos | `/app/relatorios` | `/app/operacao`, `/app/tarefas/[taskId]`, `/app/aprovacoes` | Bottleneck, Report, Task |
| F5 Resumo Semanal | `/app/relatorios/semana` | `/app/notificacoes` | Report, Notification |
| F6 Qualidade Dados | `/app/dados/qualidade` | `/onboarding/importacao`, `/app/tarefas/[taskId]` | DataQualityIssue, Task |
| F7 Creditos/Limites | `/app/uso/alertas` | `/app/uso/cotas`, `/app/billing/add-ons` | QuotaLedgerEntry, Alert |
| F8 Performance | `/app/relatorios/agentes` | `/app/agentes/[agentId]`, `/app/fluxos/execucoes/[runId]` | FlowRun, Report |
| F9 Permissoes/Auditoria | `/app/auditoria` | `/app/configuracoes/permissoes`, `/app/auditoria/[eventId]` | AuditEvent, Membership |
| F10 Capacidade/Crescimento | `/app/relatorios/ocupacao` | `/app/agenda`, `/app/turmas/[id]`, `/app/reposicoes` | CapacitySignal, Report, Task |
| F11 Falhas/Webhooks | `configuracao especifica da integracao` | `/app/operacao/[caseId]`, `/app/envios/[sendId]` | IntegrationLog, OperationCase |
| F12 Importacao/Migracao | `/app/importacao/[jobId]` | `/app/dados/duplicidades`, `/app/dados/qualidade` | ImportJob, DataQualityIssue |
| F13 Teste De Fluxo | `/app/fluxos/[flowId]/simular` | `/app/fluxos/[flowId]`, `/app/dados/qualidade` | FlowConfiguration, SimulationResult |

## Historico/Evolucao

| Flow | Primary route | Support routes | Core objects |
| --- | --- | --- | --- |
| G1 Contexto Antes Aula | `/app/professores` | `/app/aulas/[id]`, `/app/historico` | ClassSession, StudentHistoryEvent |
| G2 Observacao Pos-Aula | `/app/professores` | `/app/historico`, `/app/alunos/[id]/linha-do-tempo` | StudentHistoryEvent, ClassSession |
| G3 Restricao/Cuidado | `/app/historico` | `/app/alunos/[id]`, `/app/tarefas/[taskId]` | StudentHistoryEvent, Task |
| G4 Objetivo/Evolucao | `/app/alunos/[id]/linha-do-tempo` | `/app/historico` | StudentHistoryEvent, Student |
| G5 Contexto Para Agente | `/app/historico` | `/app/fluxos/execucoes/[runId]` | StudentHistoryEvent, FlowRun |
| G6 Documentos/Anamnese | `/app/historico/documentos` | `/app/alunos/[id]`, `/app/aprovacoes/[approvalId]` | DocumentRecord, Student, Approval |
| G7 Correcao Historico | `/app/historico` | `/app/auditoria/[eventId]` | StudentHistoryEvent, AuditEvent |
| G8 Handoff Professores | `/app/professores` | `/app/tarefas/[taskId]` | Task, StudentHistoryEvent |
| G9 Lembrete Professor | `/app/professores` | `/app/notificacoes`, `/app/tarefas/[taskId]` | Notification, Task |
| G10 Compartilhar Contexto | `/app/historico` | `/app/aprovacoes/[approvalId]`, `/app/inbox` | Approval, Conversation |
| G11 Permissao Historico | `/app/historico/permissoes` | `/app/configuracoes/permissoes`, `/app/auditoria/[eventId]` | Membership, AuditEvent |
| G12 Linha Do Tempo | `/app/alunos/[id]/linha-do-tempo` | `/app/historico` | StudentHistoryEvent, Student |

## Strong Candidate Additions After 91-Flow Baseline

| Flow | Primary route | Support routes | Core objects |
| --- | --- | --- | --- |
| C15 Entrada Multicanal De Lead | `/app/vendas/captura` | `/app/interessados`, `/app/vendas/origens`, `/app/dados/duplicidades`, `/app/tarefas/[taskId]` | InterestedPerson, Contact, SourceMetric, Task |
| D15 Encerramento Ou Alteracao Efetiva De Plano | `/app/financeiro/movimentacoes` | `/app/alunos/[id]`, `/app/agenda`, `/app/auditoria/[eventId]` | StudentPlan, OperationCase, Payment, AuditEvent |
| E13 Reclamacao E Recuperacao De Confianca | `/app/reclamacoes` | `/app/reclamacoes/[caseId]`, `/app/operacao/[caseId]`, `/app/aprovacoes/[approvalId]`, `/app/auditoria/[eventId]` | ComplaintCase, OperationCase, Task, AuditEvent |
| F14 Incidente De Automacao E Correcao Operacional | `/app/operacao/incidentes` | `/app/operacao/incidentes/[incidentId]`, `/app/fluxos/execucoes/[runId]`, `/app/dados/qualidade`, `/app/auditoria/[eventId]` | IncidentCase, FlowRun, DataQualityIssue, AuditEvent |
| F15 Mudanca De Politica Ou Regra Operacional | `/app/politicas` | `/app/politicas/[policyId]`, `/app/politicas/[policyId]/simular`, `/app/aprovacoes/[approvalId]`, `/app/auditoria/[eventId]` | PolicyVersion, Approval, AuditEvent |

## Optional Standalone-Flow Candidates

These are accepted product needs, but not yet accepted as standalone agent flows.

| Flow | Current recommendation | Primary route if standalone | Core objects |
| --- | --- | --- | --- |
| E14 Primeira Semana Do Novo Aluno | Keep as use case/checklist until a standalone flow card proves independent configuration is needed. | `/app/retencao` or `/app/alunos/[id]` | Student, Task, StudentHistoryEvent |
| G13 Gate De Anamnese, Consentimento E Contato De Emergencia | Keep as intake/data-quality/history gate until standalone flow ownership is proven. | `/app/historico/documentos` or `/app/dados/qualidade` | IntakeGate, DocumentRecord, Student, Approval |

## Coverage Conclusion

The 91 flows require more than module routes. They require:

- operation cases;
- task detail;
- approval detail;
- send detail;
- flow execution detail;
- audit detail;
- usage ledger;
- integration logs;
- object-specific detail pages.

Without these transactional routes, manual, copilot and autonomous modes cannot be operated or debugged safely.

Round 1 conclusion: use 96 as the strong current flow number, and keep 98 only as the possible count if E14 and G13 become standalone agent flows.
