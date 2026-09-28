# Draft Audit - Are The AI Agent Flows 91, More, Or Less?

> Status: exploratory draft. Scope is limited to AI-agent flows integrated into Taliya. This does not audit the full CRM/product workflow catalog.

## Short Answer

The current number **91 is a valid baseline**, but it should be treated as the **minimum defensible catalog**, not the final count.

After auditing with a stricter "agent-flow" lens, the likely answer is:

```text
91 current canonical flows
+ 5 strong candidate missing flows
+ 2 optional candidate flows to validate
= 96 to 98 likely agent flows before final trimming
```

I would not reduce the catalog below 91 yet. Some current flows could be merged technically, but they are useful as separate studio-configurable behaviors. The bigger risk is missing important agent paths, not having too many.

## Counting Rule

A path counts as an AI-agent flow when it has all or most of these:

- clear trigger;
- single primary owner agent;
- business outcome different from neighboring flows;
- mode can differ: manual, copiloto, autonomous;
- configurable rules/templates/limits;
- required data;
- terminal states;
- cost/quota behavior;
- eval scenario;
- audit/log expectation.

A path should **not** be counted as a separate flow when it is only:

- a UI screen;
- a report;
- a helper tool;
- a sub-step inside a larger flow;
- a data field;
- a generic exception already covered by handoff, task, approval, or pause.

## Current Baseline

The existing matrix has 91 flows:

| Family | Count |
| --- | ---: |
| Atendimento | 10 |
| Agenda | 16 |
| Vendas | 14 |
| Financeiro | 14 |
| Retencao | 12 |
| Gestao | 13 |
| Historico/Evolucao | 12 |
| **Total** | **91** |

## Audit Result By Family

### Atendimento - Keep 10

Current count: 10.

Recommendation: keep 10.

Why:

- A1-A10 each have distinct trigger and safety behavior.
- A5 Handoff Humano may look like runtime plumbing, but it needs configuration: responsible queue, SLA, summary, pause behavior, and response to contact.
- A7 could eventually split into identity, media, and duplicates, but for v1 it is better as one flow with subflows.

Conclusion:

```text
Atendimento remains 10.
```

### Agenda - Keep 16

Current count: 16.

Recommendation: keep 16.

Reviewed but not accepted as a new flow:

| Candidate | Flow | Why It May Be Separate |
| --- | --- | --- |
| B17 | Substituicao De Professor | It may matter operationally, but in the current formulation it feels better as a subflow inside B9 Cancelamento Pelo Studio and B11 Ajuste De Grade, not as an independent configurable AI-agent flow. |

Why it is not counted now:

- It does not yet create a clearer agent promise than the existing Agenda flows.
- It risks pulling the catalog toward staff management before that is a confirmed agent scope.
- It can be handled by impacted-class analysis inside B9/B11 for now.

Conclusion:

```text
Agenda remains 16.
```

### Vendas - Keep 14, Add 1

Current count: 14.

Recommendation: add C15.

Strong candidate:

| Candidate | Flow | Why It May Be Separate |
| --- | --- | --- |
| C15 | Entrada Multicanal De Lead | A1 assumes WhatsApp entry and C8 records origin/qualification, but neither fully owns leads arriving from site form, Instagram/DM, referral form, manual walk-in registration, or imported campaign list. |

Why not just C8:

- C8 updates/qualifies origin.
- It does not define lead creation, duplicate check, owner assignment, initial routing, or first next action by source.

Conclusion:

```text
Vendas should likely become 15.
```

### Financeiro - Keep 14, Add 1

Current count: 14.

Recommendation: add D15.

Strong candidate:

| Candidate | Flow | Why It May Be Separate |
| --- | --- | --- |
| D15 | Encerramento Ou Alteracao Efetiva De Plano | E4 handles cancellation risk, E9 handles post-cancellation, D9 handles pause/trancamento, and D5 handles renewal. But the actual operational execution of ending/changing a student plan has distinct actions: stop future charges, adjust agenda, revoke/keep credits, end contract, record reason, and communicate final status. |

Why not just E4/E9:

- E4 is risk/human conversation.
- E9 is after cancellation.
- D15 would own the financial/operational state transition.

Conclusion:

```text
Financeiro should likely become 15.
```

### Retencao - Keep 12, Add 1 Strong, Validate 1 Optional

Current count: 12.

Recommendation: add E13, validate E14.

Strong candidate:

| Candidate | Flow | Why It May Be Separate |
| --- | --- | --- |
| E13 | Reclamacao E Recuperacao De Confianca | E6 catches satisfaction feedback and E4 catches cancellation risk, but a complaint has its own lifecycle: capture complaint, categorize cause, pause unsafe automation, assign owner, resolve, follow up, and mark trust recovered or not. |

Optional candidate:

| Candidate | Flow | Why It May Be Separate |
| --- | --- | --- |
| E14 | Primeira Semana Do Novo Aluno | B15 covers first class, but early churn often happens after the first purchase. This flow would monitor adaptation, first-week attendance, teacher notes, doubts, and early satisfaction. |

Conclusion:

```text
Retencao should likely become 13, possibly 14.
```

### Gestao - Keep 13, Add 2

Current count: 13.

Recommendation: add F14 and F15.

Strong candidates:

| Candidate | Flow | Why It May Be Separate |
| --- | --- | --- |
| F14 | Incidente De Automacao E Correcao Operacional | F11 handles integration/webhook failures, but not the case where automation technically succeeded and produced the wrong business action because data/rules/context were wrong. |
| F15 | Mudanca De Politica Ou Regra Operacional | F9 audits critical changes and F13 tests flows, but changing absence rules, make-up validity, price policy, cancellation policy, or communication policy needs impact simulation, effective date, rollout, and rollback. |

Why these matter:

- Agents will make mistakes or act on wrong data; the system needs a recovery/review loop.
- Policy changes alter many future agent decisions and should not be just a generic audit event.

Conclusion:

```text
Gestao should likely become 15.
```

### Historico/Evolucao - Keep 12, Validate 1 Optional

Current count: 12.

Recommendation: keep 12 for now, validate G13.

Optional candidate:

| Candidate | Flow | Why It May Be Separate |
| --- | --- | --- |
| G13 | Gate De Anamnese, Consentimento E Contato De Emergencia | G6 covers documents/anamnesis and G3 covers restrictions, but a studio may need a specific gate that blocks or warns before first class/automation when required intake, consent, emergency contact, or responsible validation is missing. |

Why optional:

- It may be a subflow of G6 + B15.
- It should become separate only if it has independent configuration, blocking rules, and owner.

Conclusion:

```text
Historico/Evolucao remains 12, possibly 13.
```

## Revised Count Scenarios

| Scenario | Count | Meaning |
| --- | ---: | --- |
| Strict current baseline | 91 | Current matrix accepted as canonical v0.1. |
| Add only strong gaps | 96 | Add C15, D15, E13, F14, F15. |
| Add strong + optional gaps | 98 | Also add E14 and G13 if product decides they are independent flows. |
| Collapse support/runtime flows | 82-86 | If handoff, audit, quota, imports, failures and test flows are treated as system capabilities instead of configurable agent flows. Not recommended for product configuration yet. |
| Count every subpath/exception | 180+ | If every branch inside the deep map is counted. Not recommended; it becomes unmanageable. |

## Recommended Product Decision

For now, use:

```text
96 candidate AI-agent flows
```

Where:

- 91 are current baseline;
- 5 are strong missing candidates;
- 2 remain optional and should be validated before becoming canonical.

Use this language:

```text
Taliya currently has 91 mapped agent flows and 5 strong candidate additions under review.
```

Avoid saying:

```text
Taliya has a closed final flow count.
```

## Strong Candidate Additions

| New ID | Proposed Flow | Owner Agent |
| --- | --- | --- |
| C15 | Entrada Multicanal De Lead | Vendas |
| D15 | Encerramento Ou Alteracao Efetiva De Plano | Financeiro |
| E13 | Reclamacao E Recuperacao De Confianca | Retencao |
| F14 | Incidente De Automacao E Correcao Operacional | Gestao |
| F15 | Mudanca De Politica Ou Regra Operacional | Gestao |

## Optional Candidate Additions

| New ID | Proposed Flow | Owner Agent | Decision Needed |
| --- | --- | --- | --- |
| E14 | Primeira Semana Do Novo Aluno | Retencao | Separate flow or subflow of B15/E6? |
| G13 | Gate De Anamnese, Consentimento E Contato De Emergencia | Historico/Evolucao | Separate flow or subflow of G6/B15? |

## Do Any Current Flows Look Like They Should Be Removed?

Not yet.

Some current flows are control-plane or runtime-ish, but they are still useful as studio-configurable agent behavior:

- A5 Handoff Humano;
- F7 Creditos/Limites;
- F9 Permissoes/Auditoria;
- F11 Falhas/Webhooks;
- F12 Importacao/Migracao;
- F13 Teste De Fluxo;
- G11 Permissao Historico.

They may not be "conversation flows", but they are agent governance flows. Since Taliya has agents integrated into a system, they should stay in the agent catalog until implementation proves they are better modeled as platform services.

## Next Validation Step

Before freezing the number, each candidate addition needs a mini flow card:

- trigger;
- owner agent;
- mode default;
- data required;
- action scope;
- handoff rules;
- quota/cost behavior;
- terminal states;
- routes/screens used;
- eval cases.

If a candidate cannot satisfy those fields, it should stay a subflow, not become a new canonical flow.
