# CRM-first Diagnostic And Widget Attention Plan

## Purpose

Define the next planning slice for the public sales attendant:

1. Replace the current "pain -> agent" diagnostic framing with an operation-wide diagnostic that sells Taliya as a complete CRM plus integrated AI agents.
2. Turn the "Quer ver como ficaria no seu studio?" path into a free diagnostic flow that captures lead context, identifies operational pains and recommends CRM modules, agents, plan and next step.
3. Make the closed floating widget more visible through restrained attention motion without making the landing feel spammy.

This document is part of Spec 2. It plans future implementation only; it does not redesign the approved `/pilates` landing layout.

## Product Rule

Taliya must be described as:

```text
CRM operacional completo para studios de Pilates, com agentes de IA integrados ao CRM.
```

The sales attendant must not sell agents as disconnected bots. The correct framing is:

1. The CRM organizes the studio operation.
2. The agents act on top of CRM records, rules, tasks, channels and permissions.
3. WhatsApp is an important channel, not the product itself.
4. The Base plan remains a complete CRM with zero active agents.

## Commercial Gate Rule

The CRM-first diagnostic is the main commercial funnel of the attendant.

When the visitor asks about price, plans, demo, WhatsApp, a human person, "too expensive" or "I want to subscribe", the agent must treat that as commercial interest, not as permission to skip diagnosis. Unless the diagnostic is already complete, the agent answers briefly, avoids a cold CTA and asks the next diagnostic question.

Final CTAs appear after the diagnostic report: plans, guided demo when available, WhatsApp consultor or checkout after explicit plan confirmation.

## Non-goals

- Do not redesign the approved `/pilates` visual layout.
- Do not create a fake guided demo before the real SaaS demo exists.
- Do not market the custom-agent diagnostic as live AI until that feature is specified and evaluated separately.
- Do not collect sensitive student data, payment credentials or billing documents in chat.

## Diagnostic Entry

The diagnostic entry should be the primary proof-oriented CTA for visitors who are interested but not ready to buy immediately.

Recommended copy direction:

- CTA label: `Diagnostico gratuito`
- Supporting idea: `Veja onde seu studio perde tempo e quais partes a Taliya organizaria primeiro.`

Entry metadata:

- `entryPath=diagnostic_cta`
- `sourceSection=studio_diagnostic`
- `conversionPath=crm_agent_diagnostic`
- carry `leadId` and `sessionId` when available

## Naming Boundary

There are two different diagnostic concepts in Spec 2:

| Flow | Purpose | Route/Mode | Primary output |
| --- | --- | --- | --- |
| CRM-first diagnostic | Diagnose the studio operation and sell the SaaS subscription path | normal attendant conversation, `entryPath=diagnostic_cta`, `conversionPath=crm_agent_diagnostic` | CRM + agents + plan + next step |
| Agente sob medida diagnostic | Classify an unmapped operation request, such as marketing or another custom agent | separate report mode, `entryPath=custom_agent_diagnostic` and `/api/landing/custom-agent-diagnostic` | mapped/custom/mixed/unclear report |

These flows must not share response schemas accidentally. The CRM-first diagnostic may use the normal attendant conversation engine. The Agente sob medida diagnostic remains a report-style mode with its own route and schema.

## Diagnostic Conversation Flow

The diagnostic must feel like a human consultant, not a form.

Rules:

- greet naturally;
- ask one question at a time;
- extract multiple answers when the visitor gives several data points at once;
- do not repeat questions already answered;
- give small useful reflections between questions;
- ask for contact after minimum interest, but continue if the visitor refuses;
- keep messages short and use common words;
- avoid early plan/price pressure;
- include buying timing to classify lead temperature.

Minimum interest is reached when the visitor does at least one of these:

- shares a real operational pain;
- clicks `Falar com consultor`, `Continuar no WhatsApp` or `Diagnostico gratuito`;
- asks about plans, price, demo, implementation or how to start;
- says they want to solve the issue now or soon;
- asks for a human or wants the result sent later.

After minimum interest, the agent may ask for WhatsApp/email with a short reason. If the visitor refuses, the diagnostic continues and the lead remains anonymous or partially identified.

### Core Questions

1. `Com quem eu falo?`
2. `Hoje seu studio tem mais ou menos quantos alunos ativos?`
3. `Hoje quais partes mais dao trabalho no studio? Pode citar mais de uma: WhatsApp, agenda, reposicoes, faltas, vendas, financeiro, renovacao, alunos sumindo ou equipe perdida.`
4. `Hoje voce consegue ver facilmente o que precisa ser resolvido no dia?`
5. `As reposicoes hoje sao faceis de controlar ou ainda viram troca de mensagem e encaixe manual?`
6. `Quando alguem chama interessado no WhatsApp, voces conseguem acompanhar ate virar aluno?`
7. `Hoje voce usa algum sistema para agenda, alunos ou financeiro, ou boa parte fica no WhatsApp, planilha e caderno?`
8. `Se voce pudesse tirar uma coisa da sua mao este mes, o que seria?`
9. `Voces estao buscando resolver isso agora ou ainda estao so pesquisando opcoes?`
10. `Qual WhatsApp ou email voce prefere deixar para eu salvar esse diagnostico e te mandar o proximo passo?`

### Adaptive Follow-ups

Use at most one adaptive follow-up before producing the diagnostic unless the visitor asks to continue.

| Signal | Follow-up |
| --- | --- |
| WhatsApp pain | `Esse WhatsApp pesa mais com alunos atuais ou com interessados novos?` |
| Financial pain | `Hoje voce percebe rapido quem esta atrasado ou com plano vencendo?` |
| Absences pain | `Voces percebem rapido quando um aluno comeca a faltar mais que o normal?` |
| Sales pain | `Quando a pessoa faz aula experimental, voces acompanham depois ou depende de lembrar manualmente?` |
| Replacement pain | `O problema maior e achar horario disponivel ou controlar quem ainda tem reposicao para fazer?` |

## Diagnostic State Model

Suggested states:

- `started`
- `collect_name`
- `collect_studio_size`
- `collect_pains`
- `collect_daily_visibility`
- `collect_replacements`
- `collect_sales_followup`
- `collect_current_system`
- `collect_priority_goal`
- `collect_buying_timing`
- `collect_contact`
- `adaptive_follow_up`
- `diagnosis_ready`
- `recommend_plan`
- `next_step`

The state machine must allow skipping, partial answers and direct requests such as "me mostra os planos", "quero falar com humano" or "quero assinar".

Free-text interpretation rule:

- The diagnostic must not depend on quick replies to progress. A visitor can answer naturally, ambiguously or with partial context, and the AI response layer must classify whether the turn answers the current field, asks a side question, requests price/plans, requests human help, cancels the diagnostic or belongs to Agente sob medida.
- Deterministic extraction is allowed for safety and consistency, but it must not be the only way to advance. The agent should use AI interpretation to avoid repeating questions that were already answered in natural language.
- If the visitor asks a side question during the diagnostic, the agent answers briefly and then either resumes the current diagnostic question, reroutes to the correct path or stops the diagnostic if requested.

## Lead Payload Additions

The lead upsert payload should include:

- `diagnosticType`: `crm_agent_diagnostic`
- `studioSizeRange`
- `operationalPains`
- `crmPainAreas`
- `agentPainAreas`
- `dailyVisibility`
- `replacementComplexity`
- `salesFollowupMaturity`
- `currentSystem`
- `priorityGoal`
- `buyingTiming`: `now`, `soon`, `researching` or `unknown`
- `leadTemperature`: `hot`, `warm` or `cold`
- `recommendedCrmModules`
- `recommendedAgents`
- `recommendedPlan`
- `diagnosticSummary`
- `nextStep`
- `contactCaptureStatus`

Lead temperature rules:

- `hot`: wants to solve now, asks price/plan/demo/consultor/checkout, or gives clear urgent pain.
- `warm`: has clear pain and context, but is comparing or planning soon.
- `cold`: researching, vague pain, no contact or no clear next step.

## Final Diagnostic Structure

The final diagnostic must identify pains and persuade by connecting each pain to both CRM organization and agent action.

Required sections:

1. `Resumo do seu studio`
2. `Dores que apareceram`
3. `O que isso esta custando na rotina`
4. `O que a Taliya organizaria no CRM`
5. `Quais agentes entram depois`
6. `Como ficaria na pratica`
7. `Plano mais coerente`
8. `Proximo passo`

Chat delivery rule:

- In the chat widget, these sections may be compressed into fewer short messages so the conversation stays natural, but the information order must remain: hold message, bottleneck, CRM base, agents, plan, next step.
- The diagnostic should start with a short hold message indicating that enough information was collected, then appear in separated messages/cards with visible typing cadence where the channel supports it.
- Recommended agents must be shown one at a time. Each agent item must include: the pain it resolves, why it was recommended from the diagnostic and how it acts in practice.

### Pain Mapping

| Pain | CRM layer | Agent layer |
| --- | --- | --- |
| WhatsApp baguncado | Inbox, contatos, conversas, tarefas | Atendimento |
| Reposicoes confusas | Agenda, aulas, creditos, vagas, regras | Agenda |
| Interessados sem follow-up | Vendas, pipeline, experimental, origem | Vendas |
| Pagamentos e renovacoes manuais | Financeiro, planos, cobrancas, vencimentos | Financeiro |
| Alunos sumindo ou cancelando | Retencao, frequencia, risco, historico | Retencao |
| Dono sem visao do dia | Hoje, Operacao, tarefas, prioridades, relatorios | Gestao/Governanca |
| Professor sem contexto | Perfil do aluno, historico permitido, notas | Historico/Professor |

## Plan Recommendation Rules

- Recommend Base when the visitor mainly wants CRM organization and does not want active automation yet.
- Recommend 1 Agente when there is one narrow operational pain.
- Recommend 3 Agentes when the pain cluster is mainly Atendimento + Agenda + Vendas.
- Recommend 7 Agentes when the visitor has broad operation pain, wants the complete system, has high buying timing, or mentions several connected areas.
- The recommendation should explain why lower plans may still be valid, but should not treat all plans as equal.

## Widget Attention Motion

The closed widget must become more noticeable without feeling aggressive.

Desktop:

- default to the full closed widget when space allows;
- use a subtle "breath" halo or border glow;
- every 18-25 seconds, if closed and idle, do one gentle nudge: 4-6px lift, tiny tilt and return;
- optionally rotate short microcopy such as `Diagnostico gratuito`, `Veja onde seu studio perde tempo` or `Tire uma duvida rapida`.

Mobile:

- keep only the message icon;
- use a soft pulse on the outline;
- show a small unread-style badge after a short idle delay;
- open with context-aware first message.

Limits:

- run attention motion only while the chat is closed;
- max 3 attention nudges per session;
- pause after click, close or recent interaction;
- respect `prefers-reduced-motion`;
- no automatic sound;
- no aggressive shake;
- no large tooltip covering content.

## Implementation Order

1. Update source-of-truth docs and approved answer knowledge so Taliya is consistently CRM + agents.
2. Update `data-model.md`, `floating-agent-ui-contract.md`, `conversation-route-matrix.md` and eval fixtures with `diagnostic_cta` and `crm_agent_diagnostic`.
3. Add diagnostic entry metadata, state model and lead payload fields.
4. Implement the diagnostic question flow in the conversation engine.
5. Generate the final diagnostic response using CRM + agent mapping.
6. Wire diagnostic CTA/entry into the landing without redesigning the approved layout.
7. Add lead upsert support for diagnostic fields in Sales Inbox/n8n optional automation/Sales Inbox.
8. Add closed-widget attention motion with reduced-motion support.
9. Add eval fixtures and manual test scripts.
10. Run QA: lint, build, conversation evals, mobile/desktop screenshots, lead upsert smoke.

## Acceptance Criteria

- The agent never describes Taliya as "not a CRM"; it describes Taliya as CRM operacional + agentes integrados.
- The diagnostic asks the core questions naturally and does not repeat already answered fields.
- The diagnostic can finish with partial data and still produce a useful recommendation.
- The final diagnostic names CRM modules and agents for every identified pain.
- Contact capture happens after minimum interest and does not block the diagnostic when refused.
- Lead records include diagnostic context, buying timing, lead temperature and next step.
- The widget attention motion increases visibility while respecting reduced motion and session limits.
- `/pilates` approved layout is preserved; only CTA wiring, behavior and motion are touched.

## Test Scenarios

1. Cold researcher: "estou so pesquisando".
2. Hot buyer: "quero resolver isso agora".
3. CRM-only buyer: "quero organizar alunos, agenda e financeiro, mas sem IA ainda".
4. Replacement pain: "120 alunos e reposicoes viraram caos".
5. WhatsApp pain: "perco mensagem e interessado no WhatsApp".
6. Sales pain: "muita gente pergunta e nao fecha".
7. Finance pain: "mensalidade e renovacao passam batido".
8. Broad pain: "WhatsApp, reposicoes, vendas, financeiro e alunos sumindo".
9. Contact refusal: visitor declines WhatsApp/email.
10. Existing system: visitor already uses another agenda/CRM.
11. Human request: visitor wants consultor before finishing diagnostic.
12. Mobile widget attention: icon pulses/badge appears, no layout overlap.
13. Desktop widget attention: full widget nudges subtly, no distraction.
