# Quotas And Economy Mode

Canonical MVP map:

- `usage-quotas-master-map.pt-BR.md`.

Quotas are not only billing. They are operational governance.

The system must explain what was consumed, what was blocked, what was downgraded and what the studio can do next.

## Launch Plan Quotas

| Plan | Automation quota |
| --- | --- |
| Base | 0 active AI automation messages/month |
| 1 Agente | 1,500 AI messages/month hard cap |
| 3 Agentes | 5,000 AI messages/month hard cap |
| 7 Agentes | 15,000 AI messages/month hard cap |

Base still allows manual CRM records and tasks.

## Cost Origins

Every metered event must classify its origin:

| Origin | Examples |
| --- | --- |
| `ai` | classify, summarize, draft message, detect risk, recommend next action |
| `whatsapp_service` | reply inside active contact-initiated window |
| `whatsapp_utility` | operational reminder, schedule, payment or confirmation |
| `whatsapp_marketing` | reactivation, campaign, promotion, commercial follow-up |
| `batch_job` | campaign, digest, segmentation, mass processing |
| `media` | audio transcription, image/document processing |
| `history` | long context summarization, timeline compression |

## MVP Routes

| Route | Purpose |
| --- | --- |
| `/app/uso` | Usage overview, contracted quota, used/remaining quota, forecast, threshold alerts, economy behavior, downgrades and blocked work. |
| `/app/uso/extrato` | Usage ledger by flow, agent, channel, case and origin. |
| `/app/billing/add-ons` | Extra quota packs and commercial add-ons. |
| Agentes/Fluxos | Per-flow quota estimates, attempts and limits. |

Routes intentionally absorbed in the MVP:

| Old route | Decision |
| --- | --- |
| `/app/uso/cotas` | Absorbed into `/app/uso`. |
| `/app/uso/custos` | Absorbed into `/app/uso` and `/app/uso/extrato` as consumption origin. |
| `/app/uso/alertas` | Absorbed into `/app/uso`. |
| `/app/uso/pacotes` | Moved to `/app/billing/add-ons`. |
| `/app/uso/regras-economia` | Absorbed into `/app/uso`. |
| `/app/uso/limites-fluxo` | Moved to Agentes/Fluxos. |
| `/app/uso/limites-fluxo/[flowId]` | Moved to the flow configuration page. |

## Threshold Behavior

| Usage | Behavior |
| --- | --- |
| 0-69% | Normal behavior. |
| 70% | Preventive alert. Owner sees projected use. |
| 90% | Economy mode. Low-priority and expensive flows downgrade to task or copilot. |
| 100% | Hard cap. Paid automation stops. Manual CRM remains available. |
| Extra quota active | Eligible automation resumes according to economy rules. |

## Economy Priority

Every flow must define `prioridade_modo_economia`:

- essential;
- medium;
- low.

Essential examples:

- opt-out handling;
- handoff summaries;
- critical payment/status updates;
- class cancellation communication when approved;
- safety/risk flags.

Low-priority examples:

- celebration messages;
- low-risk reactivation;
- non-urgent reminders;
- broad campaigns;
- verbose summaries.

## Flow-Level Limits

Every flow can set:

- monthly credit limit;
- per-run credit limit;
- max attempts per contact;
- max external sends;
- whether it can start paid WhatsApp;
- whether it can run batch jobs;
- whether it can use media processing;
- what happens after limit.

After-limit actions:

- stop;
- create task;
- ask approval;
- call responsible queue;
- move to another flow;
- stay internal only.

## User-Facing Explanations

When a flow is blocked or downgraded, the UI must say:

- what stopped;
- why it stopped;
- what quota or rule was involved;
- what will still happen manually;
- what the user can do next.

Examples:

```text
Reativacao de ex-alunos virou aprovacao porque o studio chegou a 90% da cota mensal.
```

```text
Confirmacao de presenca continuou ativa porque esta rotina e essencial e usa mensagem utility configurada.
```

```text
O envio foi bloqueado porque a cota chegou a 100%. Criamos uma tarefa para sua equipe responder manualmente.
```

## Add-On Packs

Launch docs mention:

- one-time extra quota pack: +2k;
- recurring monthly extra quota pack: +5k.

Final prices and billing behavior require approval before paid launch.

## Acceptance Criteria

- Usage ledger identifies tenant, flow, agent, origin, run and case.
- At 90%, low-priority campaigns require approval or become tasks.
- At 100%, no paid automation runs without active extra quota.
- Manual CRM remains usable after quota cap.
- Owner can see why each blocked flow stopped.
- Flow simulator can estimate quota/cost origin before activation.
