# Screen Inventory Tree - CRM Web And Mobile App

> Status: exploratory route inventory. This is not final UI architecture, but it groups current candidate screens by product surface.

## CRM Web

```text
public
  /
  /pilates
  /pilates/planos
  /pilates/demonstracao
  /checkout
  /assinatura/confirmando
  /assinatura/falha

auth/onboarding
  /login
  /onboarding/claim/[activationId]
  /onboarding/studio
  /onboarding/importacao
  /onboarding/agentes
  /onboarding/revisao

app shell
  /app
  /app/hoje
  /app/notificacoes

inbox and contacts
  /app/inbox
  /app/conversas/[id]
  /app/envios
  /app/envios/[sendId]
  /app/contatos
  /app/contatos/[id]

students and history
  /app/alunos
  /app/alunos/[id]
  /app/alunos/[id]/linha-do-tempo
  /app/historico
  /app/historico/documentos
  /app/historico/permissoes
  /app/professores

agenda
  /app/agenda
  /app/grade
  /app/turmas
  /app/turmas/[id]
  /app/aulas/[id]
  /app/aulas/[id]/chamada
  /app/reposicoes
  /app/creditos-reposicao
  /app/lista-espera
  /app/eventos

sales
  /app/vendas
  /app/vendas/captura
  /app/vendas/origens
  /app/interessados
  /app/interessados/novo
  /app/interessados/[id]
  /app/experimental
  /app/matriculas
  /app/checkout-alunos
  /app/indicacoes
  /app/vendas/perdidos
  /app/segmentos

finance
  /app/financeiro
  /app/financeiro/kanban
  /app/financeiro/movimentacoes
  /app/financeiro/movimentacoes/[id]
  /app/financeiro/documentos

retention and trust
  /app/retencao
  /app/retencao/riscos
  /app/retencao/reativacoes
  /app/cancelamentos
  /app/reclamacoes
  /app/reclamacoes/[caseId]

operations
  /app/operacao
  /app/operacao/[caseId]
  /app/operacao/incidentes
  /app/operacao/incidentes/[incidentId]
  /app/tarefas
  /app/tarefas/[taskId]
  /app/aprovacoes
  /app/aprovacoes/[approvalId]
  /app/checklists
  /app/comunicados

management and reports
  /app/dinheiro-na-mesa
  gargalos as report/origin-filter block, no dedicated MVP route
  capacidade as report/agenda-filter block, no dedicated MVP route
  /app/relatorios
  /app/relatorios/semana
  /app/relatorios/financeiro
  /app/relatorios/vendas
  /app/relatorios/risco
  /app/relatorios/agentes
  /app/relatorios/ocupacao

agents and runtime
  /app/agentes
  /app/agentes/[agentId]
  /app/agentes/[agentId]/fluxos
  /app/fluxos
  /app/fluxos/[flowId]
  /app/fluxos/[flowId]/simular
  /app/fluxos/execucoes/[runId]

usage and billing
  /app/uso
  /app/uso/extrato
  /app/billing
  /app/billing/add-ons
  /app/billing/invoices

data, integrations and governance
  /app/importacao
  /app/importacao/[jobId]
  configuracao especifica da integracao
  configuracao especifica da integracao
  /app/auditoria
  /app/auditoria/[eventId]
  /app/dados/qualidade
  /app/dados/duplicidades
  /app/exportacoes
  /app/privacidade/solicitacoes
  /app/suporte/acessos

settings
  /app/configuracoes
  /app/configuracoes/studio
  /app/configuracoes/equipe
  /app/configuracoes/permissoes
  /app/configuracoes/canais
  /app/configuracoes/financeiro/modelos
  /app/configuracoes/financeiro/pagamentos
  /app/configuracoes/agenda
  /app/configuracoes/notificacoes

policies
  /app/politicas
  /app/politicas/[policyId]
  /app/politicas/[policyId]/simular
```

## Mobile App

```text
mobile tabs
  Today
  Inbox
  Agenda
  Students
  Interested
  Tasks
  Approvals
  Finance
  History/Notes
  Notifications

mobile detail screens
  Conversation detail
  Student profile
  Student timeline
  Class session
  Attendance
  Make-up request
  Payment detail
  Complaint/case detail
  Task detail
  Approval detail
  Flow run summary
  Usage alert

mobile smart actions
  Prepare reply
  Human takeover
  Mark attendance
  Find fit for open slot
  Approve/reject proposal
  Add teacher note
  Create task
  Pause automation
  Send safe reminder
```

## Web-Only By Default

- full agent configuration;
- flow simulation setup;
- policy versioning;
- channel/integration connection;
- role/permission configuration;
- templates and knowledge base;
- custom fields;
- resource configuration;
- exports;
- billing administration.

## Likely Drawers/Modals Rather Than Pages

- Encontrar encaixe;
- Preparar cobranca;
- Preparar resposta;
- Analisar risco;
- Criar tarefa;
- Aprovar mensagem;
- Corrigir chamada;
- Registrar falta;
- Criar credito;
- Pausar automacao;
- Explicar execucao do fluxo.
