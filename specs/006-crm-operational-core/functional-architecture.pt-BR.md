# Arquitetura funcional - PT-BR

> Status: indice canonico v0.1. As Rodadas 1-7 ja preencheram as areas por referencia; este documento mantem a estrutura comum e aponta para as especificacoes profundas.

## Regra central

Cada area funcional deve explicar objetos, jornadas, regras, dados, permissoes, cotas, auditoria, agentes, excecoes, web, mobile e metricas antes de suas telas serem consideradas prontas.

## Areas funcionais

| Rodada | Area | Status |
| --- | --- | --- |
| 1 | Ativacao, setup e configuracao essencial | v0.1 em `round-1-activation-setup-spec.pt-BR.md` |
| 2 | Operacao diaria e mesa de comando | v0.1 em `round-2-daily-command-spec.pt-BR.md` |
| 3 | Atendimento, alunos, historico e professor | v0.1 em `round-3-attendance-students-history-spec.pt-BR.md` |
| 4 | Agenda, turmas, aulas e reposicoes | v0.1 em `round-4-schedule-classes-replacements-spec.pt-BR.md` |
| 5 | Vendas, experimental, matricula e comunicados | v0.1 em `round-5-sales-trials-enrollment-communications-spec.pt-BR.md` |
| 6 | Financeiro, contratos, retencao e casos sensiveis | v0.1 em `round-6-finance-retention-sensitive-spec.pt-BR.md` |
| 7 | Agentes, execucoes, cotas, relatorios, governanca e suporte Taliya | v0.1 em `round-7-agents-quotas-governance-spec.pt-BR.md` |

## Ficha padrao por area

```text
Nome da area
Objetivo operacional
Usuarios envolvidos
Objetos de negocio
Jornadas cobertas
Entradas da area
Saidas da area
Fonte da verdade
Ciclo de vida dos objetos
Regras de negocio
Politicas operacionais relacionadas
Eventos e gatilhos
Decisoes humanas
Acoes programaticas
Acoes com IA/copiloto
Acoes autonomas
Operacao sem agentes
Dependencias com outras areas
Dados obrigatorios
Dados opcionais
Dados sensiveis
Excecoes
Riscos
Permissoes
Cotas
Auditoria
Integracoes
Comportamento quando integracao falha
Comportamento quando cota acaba
Comportamento quando dado esta incompleto
Qualidade de IA
Suporte Taliya
Indicadores
Relatorios/visoes
Web
Mobile
Decisoes pendentes
```

## Contratos globais que toda area deve usar

| Contrato | Documento |
| --- | --- |
| Dados | `canonical-data-model.pt-BR.md` |
| Ciclos de vida | `object-lifecycle-map.pt-BR.md` |
| Fonte da verdade | `source-of-truth-matrix.pt-BR.md` |
| Permissoes | `permissions-matrix.pt-BR.md` |
| Botoes/acoes | `action-button-taxonomy.pt-BR.md` |
| Estados | `ui-state-taxonomy.pt-BR.md` |
| Cotas | `quota-touchpoints.pt-BR.md` |
| Auditoria | `audit-touchpoints.pt-BR.md` |
| Politicas | `operational-policy-versioning.pt-BR.md` |
| Falhas de integracao | `integration-failure-contracts.pt-BR.md` |
| Operacao sem agentes | `zero-agent-operating-model.pt-BR.md` |
| Qualidade de agentes | `agent-quality-evaluation.pt-BR.md` |
| Migracao/importacao | `migration-import-plan.pt-BR.md` |
| Suporte Taliya | `taliya-internal-ops.pt-BR.md` |
| Metricas | `product-success-metrics.pt-BR.md` |
| Mensagens | `notification-template-governance.pt-BR.md` |

## Criterio de aceite por area

Uma area so fecha quando:

- todos os objetos usados existem no modelo canonico ou entram como decisao aberta;
- cada objeto critico tem ciclo de vida;
- cada dado critico tem fonte da verdade;
- caminhos manuais existem para plano Base/0 agentes;
- acoes com IA respeitam modo manual/copiloto/autonomo;
- cotas aparecem onde afetam comportamento;
- acoes sensiveis geram auditoria;
- falhas viram estado/caso/tarefa/incidente;
- web e mobile estao definidos;
- metricas de valor estao ligadas a objetos reais.

## Areas preenchidas nas Rodadas 1-7

### Rodada 1 - Ativacao, setup e configuracao essencial

Status: v0.1 em `round-1-activation-setup-spec.pt-BR.md`.

Resumo:

- CRM deve abrir sem agentes ativos no plano Base.
- Conta paga vira workspace por claim/billing confirmado.
- Importacao e dados incompletos geram qualidade de dados, nao automacao cega.
- Agentes incluidos podem ser configurados/testados antes de ativar.
- Fluxos exigem preflight de dados, canal, template, cota, politica, permissao e fallback.
- App faz setup essencial; web governa configuracao profunda.

### Rodada 2 - Operacao diaria e mesa de comando

Status: v0.1 em `round-2-daily-command-spec.pt-BR.md`.

Resumo:

- Hoje vira mesa de comando acionavel, nao apenas dashboard.
- Notificacao informa; tarefa exige trabalho; aprovacao decide; caso organiza problema.
- Todo item importante precisa origem, dono/fila, risco, prazo e proxima acao.
- Cota, dado e integracao bloqueada viram tarefa, aprovacao ou caso manual.
- Plano Base segue operavel com casos/tarefas/checklists sem automacao ativa.

### Rodada 3 - Atendimento, alunos, historico e professor

Status: v0.1 em `round-3-attendance-students-history-spec.pt-BR.md`.

Resumo:

- Inbox e CRM de contatos sustentam WhatsApp sem transformar WhatsApp no produto inteiro.
- Conversa precisa ter identidade, consentimento, dono/fila, estado, risco e proxima acao.
- Telefone compartilhado, responsavel, opt-out e duplicidade viram regras centrais de seguranca.
- Aluno tem perfil operacional com agenda, plano, tarefas, riscos e historico permitido.
- Historico sensivel tem permissao, visibilidade, correcao, compartilhamento seguro e auditoria.
- Professor opera aula/notas/contexto permitido principalmente pelo app, sem ver dado indevido.
- Plano Base segue completo: atendimento, contatos, alunos, historico permitido e notas funcionam manualmente.

### Rodada 4 - Agenda, turmas, aulas e reposicoes

Status: v0.1 em `round-4-schedule-classes-replacements-spec.pt-BR.md`.

Resumo:

- Agenda CRM e a fonte operacional de verdade para turmas, aulas, chamada e reposicoes.
- Um dia de aulas precisa operar no app e ser administrado no web.
- Encontrar encaixe e calculo programatico; IA entra para explicar, priorizar, redigir e lidar com excecao.
- Chamada, falta, no-show, credito de reposicao e correcao precisam preservar politica e auditoria.
- Turma mostra capacidade, vagas, alunos, professor, lista de espera e proxima aula.
- Feriado, recesso, sala/equipamento ou professor indisponivel precisam simular impacto.
- Plano Base segue completo com agenda, chamada, lista, reposicoes e avisos manuais.

### Rodada 5 - Vendas, experimental, matricula e comunicados

Status: v0.1 em `round-5-sales-trials-enrollment-communications-spec.pt-BR.md`.

Resumo:

- Todo interessado precisa de origem, etapa, dono/fila e proxima acao.
- Experimental conecta vendas e agenda, incluindo lembrete, falta, remarcacao e pos-aula.
- Pre-matricula evita converter aluno com dado, plano, contrato, pagamento ou primeira aula indefinidos.
- Conversao preserva origem, conversa e historico comercial.
- Demanda sem horario vira lista de espera, segmento ou tarefa, nao perda silenciosa.
- Comunicados em massa exigem publico, consentimento, template, custo, aprovacao e auditoria.
- Plano Base opera pipeline, experimental, matricula e comunicados manuais sem agentes.

### Rodada 6 - Financeiro, contratos, retencao e casos sensiveis

Status: v0.1 em `round-6-finance-retention-sensitive-spec.pt-BR.md`.

Resumo:

- Dinheiro, contrato, reputacao, cancelamento, reclamacao, privacidade e suporte sao superficies sensiveis.
- Pagamento/cobranca precisa evidenciar status, comprovante, link, conciliacao, promessa e falha.
- Excecoes financeiras exigem impacto, aprovacao e auditoria; agente nunca decide sozinho.
- Retencao precisa explicar sinais de risco e proxima acao.
- Cancelamento/reativacao preserva motivo, impacto, comunicacao e elegibilidade.
- Reclamacao sensivel pausa automacoes e exige dono, prazo e resposta controlada.
- LGPD/acesso de suporte exigem identidade, escopo, prazo e auditoria.

### Rodada 7 - Agentes, execucoes, cotas, relatorios, governanca e suporte Taliya

Status: v0.1 em `round-7-agents-quotas-governance-spec.pt-BR.md`.

Resumo:

- Agente nunca e magia: toda acao tem modo, politica, permissao, cota, auditoria e fallback.
- Fluxo autonomo exige preflight de dados, canal, template, consentimento, cota, politica e risco.
- Execucoes mostram ferramentas, custo, resultado, erro, output seguro e proxima acao.
- Cotas 70/90/100 geram alerta, economia, downgrade ou bloqueio com caminho manual.
- Politicas sao versionadas, simuladas, aprovadas e auditadas.
- Integracoes, relatorios, billing e suporte interno Taliya ficam com status, origem e recuperacao.
- Plano Base segue CRM completo com 0 agentes ativos.
